"""Matplotlib style configuration matching joshuampeck.com."""

import contextlib

from cycler import cycler

from colors import CREAM, GOLD, INK, MUTED, NAVY, PALETTE, PALETTE_DARK, SILK

_FONTS = {
    "sans-serif": ["Source Sans 3", "Source Sans Pro", "Helvetica", "sans-serif"],
    "serif": ["Playfair Display", "Georgia", "serif"],
    "monospace": ["DM Mono", "Consolas", "monospace"],
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
        "axes.facecolor": NAVY,
        "figure.facecolor": NAVY,
        "savefig.facecolor": NAVY,
        "axes.edgecolor": "#2A3D66",
        "axes.labelcolor": CREAM,
        "text.color": CREAM,
        "xtick.color": SILK,
        "ytick.color": SILK,
        "grid.color": "#2A3D66",
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
