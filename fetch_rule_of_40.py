"""Pull quarterly revenue and free cash flow from Massive (ex-Polygon.io).

Writes one datestamped CSV per ticker into datafiles/. The chart script reads
those files and never touches the network.

Credentials come from the environment: MASSIVE_API_KEY (or POLYGON_API_KEY).
Run: uv run python fetch_rule_of_40.py CRM NOW DDOG
"""

import argparse
import os
import sys
from datetime import date
from pathlib import Path

import pandas as pd
import requests

# Polygon.io rebranded to Massive on 2025-10-30. api.polygon.io still resolves
# during the transition window; api.massive.com is the current base.
BASE_URL = "https://api.massive.com"
INCOME_PATH = "/stocks/financials/v1/income-statements"
CASHFLOW_PATH = "/stocks/financials/v1/cash-flow-statements"

OUT = Path(__file__).parent / "datafiles"

# Discrete quarters, unsmoothed. The API can aggregate to TTM server-side,
# but these charts plot the raw quarterly figures.
TIMEFRAME = "quarterly"


def _api_key():
    key = os.environ.get("MASSIVE_API_KEY") or os.environ.get("POLYGON_API_KEY")
    if not key:
        sys.exit(
            "No API key found. Export MASSIVE_API_KEY (or POLYGON_API_KEY) "
            "with your Massive REST key and re-run."
        )
    return key


def _get_all(path, params, key):
    """GET every page of a Massive endpoint, following next_url."""
    headers = {"Authorization": f"Bearer {key}"}
    url = BASE_URL + path
    rows = []

    while url:
        resp = requests.get(url, params=params, headers=headers, timeout=30)
        resp.raise_for_status()
        payload = resp.json()
        rows.extend(payload.get("results") or [])

        # next_url comes back fully-formed and already carries the query, so
        # params must be dropped or they'd be duplicated onto it.
        url = payload.get("next_url")
        params = None

    return rows


def _to_frame(rows, fields):
    """Flatten API rows to a frame keyed on (ticker, period_end).

    Each row carries a `tickers` list — a CIK can map to several symbols, so it
    is exploded to one row per ticker.
    """
    records = []
    for r in rows:
        for ticker in r.get("tickers") or []:
            rec = {
                "ticker": ticker,
                "period_end": r.get("period_end"),
                "fiscal_year": r.get("fiscal_year"),
                "fiscal_quarter": r.get("fiscal_quarter"),
            }
            rec.update({f: r.get(f) for f in fields})
            records.append(rec)

    df = pd.DataFrame(records)
    if df.empty:
        return df
    df["period_end"] = pd.to_datetime(df["period_end"])
    return df


def fetch(tickers, years, key):
    """Return a frame of quarterly revenue/CFO/capex/FCF for each ticker."""
    # DateOffset rather than date.replace(year=...), which raises on Feb 29.
    start = (pd.Timestamp.today() - pd.DateOffset(years=years)).date().isoformat()
    common = {
        "tickers.any_of": ",".join(tickers),
        "timeframe": TIMEFRAME,
        "period_end.gte": start,
        "sort": "period_end.asc",
        "limit": 1000,
    }

    income = _to_frame(_get_all(INCOME_PATH, dict(common), key), ["revenue"])
    cashflow = _to_frame(
        _get_all(CASHFLOW_PATH, dict(common), key),
        ["net_cash_from_operating_activities",
         "purchase_of_property_plant_and_equipment"],
    )

    if income.empty or cashflow.empty:
        sys.exit(f"No {TIMEFRAME} data returned for {', '.join(tickers)}.")

    df = income.merge(
        cashflow.drop(columns=["fiscal_year", "fiscal_quarter"]),
        on=["ticker", "period_end"],
        how="inner",
    )

    df = df.rename(columns={
        "net_cash_from_operating_activities": "cfo",
        "purchase_of_property_plant_and_equipment": "capex",
    })

    # A PP&E purchase is unambiguously a cash outflow, but vendors differ on
    # whether they sign it negative. abs() makes the math convention-agnostic.
    missing = df["capex"].isna()
    for _, row in df[missing].iterrows():
        print(f"warning: {row['ticker']} {row['period_end'].date()} has no "
              f"capex; treating as 0", file=sys.stderr)
    df["capex"] = df["capex"].fillna(0).abs()
    df["fcf"] = df["cfo"] - df["capex"]

    return df.sort_values(["ticker", "period_end"])


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("tickers", nargs="+", help="one or more stock tickers")
    parser.add_argument("--years", type=int, default=7,
                        help="years of history to pull (default: 7 — the chart "
                             "shows 5 and needs a 4-quarter YoY lookback)")
    parser.add_argument("--outdir", type=Path, default=OUT,
                        help="directory for the CSVs (default: datafiles/)")
    args = parser.parse_args()

    tickers = [t.upper() for t in args.tickers]
    df = fetch(tickers, args.years, _api_key())

    args.outdir.mkdir(exist_ok=True)
    stamp = date.today().strftime("%Y%m%d")
    cols = ["period_end", "fiscal_year", "fiscal_quarter",
            "revenue", "cfo", "capex", "fcf"]

    for ticker in tickers:
        sub = df[df["ticker"] == ticker]
        if sub.empty:
            print(f"warning: no data for {ticker}", file=sys.stderr)
            continue
        path = args.outdir / f"rule_of_40_{ticker}_{stamp}.csv"
        sub[cols].to_csv(path, index=False, date_format="%Y-%m-%d")
        print(f"wrote {path} ({len(sub)} quarters)")


if __name__ == "__main__":
    main()
