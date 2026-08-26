"""Plot the 30Y mortgage – 10Y Treasury spread with a smoothed overlay.

Raw weekly series is shown faintly; a centered rolling mean is the highlight.
Run: uv run python mortgage_spread_smoothed.py
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import PercentFormatter

import colors
import style
from export import save_for_social

SOURCE_URL = "https://fred.stlouisfed.org/"
AUTHOR_URL = "joshuampeck.com · @joshpeck"
TITLE = "Long-term downtrend in food prices has flattened and is slightly increasing"
SUBTITLE = "Currently 11% above lowest reading in Dec 2021"

# joshuampeck.com "eyebrow" style — DM Mono medium, gold, uppercased and tracked.
EYEBROW_KW = dict(
    fontfamily="monospace",
    fontsize=9,   # 9px → ~6.75pt
    fontweight=100,
    color=colors.GOLD,
)


def _eyebrow(text):
    return "".join(text.upper())

CSV = Path(__file__).parent / "datafiles" / "CUSR0000SAF11_M2SL.csv"
OUT = Path(__file__).parent / "figures"

# Smoothing window in weeks. Weekly data → 26 ≈ 6 months, 52 ≈ 1 year.
WINDOW = 26


def main():
    style.apply("dark")

    df = pd.read_csv(CSV, parse_dates=["observation_date"])
    df = df.set_index("observation_date").sort_index()
    spread = df["CUSR0000SAF11_M2SL"]

    # Centered rolling mean — symmetric so peaks/troughs don't shift in time.
    smooth = spread.rolling(WINDOW, center=True, min_periods=WINDOW // 2).mean()

    fig, ax = plt.subplots()

    ax.plot(spread.index, spread, color=colors.MUTED, linewidth=0.8,
            alpha=0.55, label="Weekly")
    ax.plot(smooth.index, smooth, color=colors.GOLD, linewidth=2.2,
            label=f"{WINDOW}-week rolling mean")

    # Reference lines: min, mean, max of the raw weekly spread.
    last_x = spread.index[-1]
    for level, label in [
        (spread.min(), "min"),
        (spread.mean(), "avg"),
        (spread.max(), "max"),
    ]:
        ax.axhline(level, color=colors.CREAM, linewidth=0.7, linestyle=":",
                   alpha=0.5)
        ax.text(last_x, level, f"  {label} {level:.04f}%",
                va="center", ha="left", fontsize=10,
                color=colors.CREAM, alpha=0.7)

    style.set_title(
        ax,
        TITLE,
        subtitle=SUBTITLE,
    )
    ax.set_ylabel("Ratio")
    ax.set_xlabel("")
    ax.yaxis.set_major_formatter(PercentFormatter(xmax=100, decimals=3))
    ax.margins(x=0.01)
    ax.legend(loc="upper left")

    # Footer: source on the left, author on the right, in the website's
    # eyebrow style. url= is honored by vector backends (PDF / SVG); PNG
    # silently ignores it.
    fig.text(0.01, 0.01, _eyebrow(f"Data: {SOURCE_URL}"),
             ha="left", va="bottom", url=SOURCE_URL, **EYEBROW_KW)
    fig.text(0.99, 0.01, _eyebrow(f"By: {AUTHOR_URL}"),
             ha="right", va="bottom", url=AUTHOR_URL, **EYEBROW_KW)

    OUT.mkdir(exist_ok=True)
    png = save_for_social(fig, "food_prices_vs_m2", path=str(OUT))
    pdf = save_for_social(fig, "food_prices_vs_m2", path=str(OUT),
                          fmt="pdf")
    print(f"wrote {png}")
    print(f"wrote {pdf}")


if __name__ == "__main__":
    main()
