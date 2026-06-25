"""Matplotlib style configuration matching joshuampeck.com."""

import contextlib

from cycler import cycler

from colors import (
    CHARCOAL, CREAM, GOLD, GRID_DARK, INK, MUTED, NAVY,
    PALETTE, PALETTE_DARK, SILK, WHITE,
)

_FONTS = {
    "sans-serif": ["Roboto", "Helvetica", "Arial", "DejaVu Sans", "sans-serif"],
    "serif":      ["DM Serif Display", "Playfair Display", "Georgia",
                   "DejaVu Serif", "serif"],
    "monospace":  ["DM Mono", "Menlo", "Monaco", "Consolas",
                   "DejaVu Sans Mono", "Courier New", "monospace"],
}


def _base_params():
    return {
        "font.family": "sans-serif",
        "font.sans-serif": _FONTS["sans-serif"],
        "font.serif": _FONTS["serif"],
        "font.monospace": _FONTS["monospace"],
        "font.size": 12,
        "axes.titlesize": 16,
        "axes.titleweight": "bold",
        "axes.labelsize": 13,
        "axes.axisbelow": True,
        "axes.grid": True,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.linewidth": 0.8,
        "grid.alpha": 0.3,
        "grid.linewidth": 0.8,
        "grid.linestyle": "--",
        "lines.linewidth": 2.0,
        "lines.markersize": 6,
        "legend.frameon": False,
        "legend.fontsize": 11,
        "figure.figsize": [10, 6],
        "figure.dpi": 150,
        "savefig.dpi": 200,
        "savefig.bbox": "tight",
        "xtick.labelsize": 11,
        "ytick.labelsize": 11,
        "xtick.direction": "out",
        "ytick.direction": "out",
    }


def _light_params():
    return {
        "axes.facecolor": CREAM,
        "figure.facecolor": CREAM,
        "savefig.facecolor": CREAM,
        "axes.edgecolor": SILK,
        "axes.labelcolor": INK,
        "text.color": INK,
        "xtick.color": MUTED,
        "ytick.color": MUTED,
        "grid.color": SILK,
        "axes.prop_cycle": cycler("color", PALETTE),
    }


def _dark_params():
    return {
        "axes.facecolor": CHARCOAL,
        "figure.facecolor": CHARCOAL,
        "savefig.facecolor": CHARCOAL,
        "axes.edgecolor": GRID_DARK,
        "axes.labelcolor": WHITE,
        "text.color": WHITE,
        "xtick.color": WHITE,
        "ytick.color": WHITE,
        "grid.color": GRID_DARK,
        "axes.prop_cycle": cycler("color", PALETTE_DARK),
    }


def apply(mode="light"):
    """Apply peckcharts style globally.

    Args:
        mode: "light" (cream background) or "dark" (navy background).
    """
    import matplotlib.pyplot as plt

    params = _base_params()
    params.update(_dark_params() if mode == "dark" else _light_params())
    plt.rcParams.update(params)


def set_title(ax, title, subtitle=None, *, color=None, subtitle_color=None):
    """Apply the project title style to an axes.

    Bold serif title (DM Serif Display) with an optional normal-weight sans
    subtitle (Roboto) immediately below. Left-aligned with the axes.
    """
    import matplotlib.pyplot as plt

    title_color = color or plt.rcParams["text.color"]
    sub_color = subtitle_color or plt.rcParams["text.color"]

    if subtitle:
        # The subtitle sits in matplotlib's normal title slot; the bold title
        # is drawn above it via ax.text so vertical spacing is automatic and
        # bbox_inches="tight" crops correctly. wrap=True lets long titles
        # break at the figure-edge instead of clipping.
        ax.set_title(subtitle, loc="left", pad=4,
                     fontsize=12, fontweight="normal",
                     fontfamily="sans-serif", color=sub_color)
        t = ax.text(0.0, 1.05, title, transform=ax.transAxes,
                    ha="left", va="bottom",
                    fontsize=20, fontweight="bold",
                    fontfamily="serif", color=title_color)
        t.set_wrap(True)
    else:
        ax.set_title(title, loc="left", pad=8,
                     fontsize=20, fontweight="bold",
                     fontfamily="serif", color=title_color)


@contextlib.contextmanager
def context(mode="light"):
    """Temporarily apply peckcharts style within a with-block."""
    import matplotlib.pyplot as plt

    with plt.rc_context():
        apply(mode)
        yield


def reset():
    """Restore matplotlib defaults."""
    import matplotlib.pyplot as plt

    plt.rcdefaults()
