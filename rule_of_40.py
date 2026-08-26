"""Plot the two components of the Rule of 40 as a signed stacked area chart.

Revenue growth and FCF margin stack from zero — upward when positive, downward
when negative — so each band's thickness is its true magnitude. A gold line
draws the actual Rule of 40 score on top.

Reads the datestamped CSVs written by fetch_rule_of_40.py; no network access.
Run: uv run python rule_of_40.py CRM NOW DDOG
"""

import argparse
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import PercentFormatter

import colors
import style
from export import save_for_social

SOURCE_URL = "https://massive.com/"
AUTHOR_URL = "joshuampeck.com · @joshpeck"

# joshuampeck.com "eyebrow" style — DM Mono medium, gold, uppercased and tracked.
EYEBROW_KW = dict(
    fontfamily="monospace",
    fontsize=9,   # 9px → ~6.75pt
    fontweight=100,
    color=colors.ACCENT,
)


def _eyebrow(text):
    return "".join(text.upper())


DATA = Path(__file__).parent / "datafiles"
OUT = Path(__file__).parent / "figures"

# The Rule of 40 threshold itself.
THRESHOLD = 40


def latest_datafile(ticker):
    """Newest datestamped CSV for a ticker. Filenames sort by date lexically."""
    matches = sorted(DATA.glob(f"rule_of_40_{ticker}_*.csv"))
    if not matches:
        sys.exit(f"No data for {ticker}. Run: "
                 f"uv run python fetch_rule_of_40.py {ticker}")
    return matches[-1]


def components(csv, years):
    """Read a quarterly levels CSV and derive growth %, FCF margin %, score."""
    df = pd.read_csv(csv, parse_dates=["period_end"])
    df = df.set_index("period_end").sort_index()

    # Guard against an older TTM-schema pull being read as if it were
    # quarterly, which would silently produce a wrong chart.
    if "revenue_ttm" in df.columns:
        parts = csv.stem.split("_")
        hint = parts[3] if len(parts) > 3 else "<TICKER>"
        sys.exit(f"{csv.name} holds TTM figures from an older pull. Re-run: "
                 f"uv run python fetch_rule_of_40.py {hint}")

    # Raw quarterly figures, unsmoothed. Growth still compares against the
    # same quarter a year back — 4 rows — so seasonality doesn't masquerade
    # as a trend the way a quarter-on-quarter comparison would.
    df["growth"] = (df["revenue"] / df["revenue"].shift(4) - 1) * 100
    df["margin"] = df["fcf"] / df["revenue"] * 100
    df["r40"] = df["growth"] + df["margin"]

    df = df.dropna(subset=["growth", "margin"])
    cutoff = df.index[-1] - pd.DateOffset(years=years)
    return df[df.index >= cutoff]


def signed_stack(ax, x, growth, margin):
    """Stack two signed series away from zero in both directions.

    matplotlib's stackplot assumes non-negative inputs; a negative FCF margin
    would eat into the growth band and misstate both. Splitting each series
    into positive and negative parts and stacking them separately keeps every
    band's height equal to its own magnitude.
    """
    growth_pos, growth_neg = growth.clip(lower=0), growth.clip(upper=0)
    margin_pos, margin_neg = margin.clip(lower=0), margin.clip(upper=0)

    ax.fill_between(x, 0, growth_pos, color=colors.SLATE, alpha=0.55,
                    linewidth=0, label="Revenue growth (YoY)")
    ax.fill_between(x, growth_pos, growth_pos + margin_pos, color=colors.POSITIVE,
                    alpha=0.5, linewidth=0, label="FCF margin")

    # Each band gets its own red below zero. A shrinking top line and cash
    # burn are different failures, and CLAY separates from NEGATIVE by hue
    # rather than lightness, which is what holds up where the two bands stack
    # directly against each other. Both are labelled only when they actually
    # appear, so the usual all-positive chart keeps a three-entry legend.
    ax.fill_between(x, 0, growth_neg, color=colors.CLAY, alpha=0.55, linewidth=0,
                    label="Revenue growth, negative" if (growth < 0).any()
                    else "_nolegend_")
    ax.fill_between(x, growth_neg, growth_neg + margin_neg, color=colors.NEGATIVE,
                    alpha=0.5, linewidth=0,
                    label="FCF margin, negative" if (margin < 0).any()
                    else "_nolegend_")


def chart(ticker, df, title=None):
    fig, ax = plt.subplots()
    x = df.index

    signed_stack(ax, x, df["growth"], df["margin"])
    ax.plot(x, df["r40"], color=colors.ACCENT, linewidth=2.4,
            label="Rule of 40 score")

    ax.axhline(0, color=colors.RULE, linewidth=1.0)
    ax.axhline(THRESHOLD, color=colors.CREAM, linewidth=0.7, linestyle=":",
               alpha=0.5)
    ax.text(x[-1], THRESHOLD, f"  {THRESHOLD}", va="center", ha="left",
            fontsize=10, color=colors.CREAM, alpha=0.7)

    last = df.iloc[-1]
    verdict = "clears" if last["r40"] >= THRESHOLD else "below"
    style.set_title(
        ax,
        title or f"{ticker} {verdict} the Rule of 40 at {last['r40']:.0f}%",
        subtitle=(f"{last['growth']:.0f}% revenue growth + "
                  f"{last['margin']:.0f}% FCF margin, quarter ended "
                  f"{last.name:%b %Y}"),
    )
    # Guarantee the threshold line and the zero line both sit inside the axes
    # with breathing room, rather than flush against a spine.
    lo, hi = ax.get_ylim()
    ax.set_ylim(min(lo, -4), max(hi, THRESHOLD * 1.15))

    ax.set_ylabel("Contribution to score")
    ax.set_xlabel("")
    ax.yaxis.set_major_formatter(PercentFormatter(xmax=100, decimals=0))
    ax.margins(x=0.01)
    ax.legend(loc="upper left")

    # Footer: source on the left, author on the right, in the website's
    # eyebrow style. url= is honored by vector backends (PDF / SVG); PNG
    # silently ignores it.
    fig.text(0.01, 0.01, _eyebrow(f"Data: {SOURCE_URL}"),
             ha="left", va="bottom", url=SOURCE_URL, **EYEBROW_KW)
    fig.text(0.99, 0.01, _eyebrow(f"By: {AUTHOR_URL}"),
             ha="right", va="bottom", url=AUTHOR_URL, **EYEBROW_KW)

    return fig


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("tickers", nargs="+", help="one or more stock tickers")
    parser.add_argument("--years", type=int, default=5,
                        help="years of history to plot (default: 5)")
    parser.add_argument("--title", help="override the auto-generated title")
    parser.add_argument("--datafile", type=Path,
                        help="pin an exact CSV (single ticker only)")
    args = parser.parse_args()

    tickers = [t.upper() for t in args.tickers]
    if args.datafile and len(tickers) > 1:
        sys.exit("--datafile only makes sense with a single ticker.")

    style.apply("dark")
    OUT.mkdir(exist_ok=True)

    for ticker in tickers:
        csv = args.datafile or latest_datafile(ticker)
        df = components(csv, args.years)
        if df.empty:
            print(f"warning: not enough history for {ticker}", file=sys.stderr)
            continue

        fig = chart(ticker, df, args.title)
        name = f"rule_of_40_{ticker}"
        print(f"wrote {save_for_social(fig, name, path=str(OUT))}")
        print(f"wrote {save_for_social(fig, name, path=str(OUT), fmt='pdf')}")
        plt.close(fig)


if __name__ == "__main__":
    main()
