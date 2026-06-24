"""Helpers for saving figures at common social/web dimensions."""

import os

# Target pixel dimensions and DPI for each format
_PRESETS = {
    "social": {"width_in": 12.0, "height_in": 6.3, "dpi": 100},   # 1200x630
    "blog":   {"width_in": 8.0,  "height_in": 4.8, "dpi": 100},   # 800x480
    "slide":  {"width_in": 19.2, "height_in": 10.8, "dpi": 100},  # 1920x1080
}


def _save(fig, name, preset, path=".", fmt="png"):
    p = _PRESETS[preset]
    fig.set_size_inches(p["width_in"], p["height_in"])
    filepath = os.path.join(path, f"{name}.{fmt}")
    fig.savefig(filepath, dpi=p["dpi"], bbox_inches="tight")
    return filepath


def save_for_social(fig, name, path=".", fmt="png"):
    """Save figure at 1200x630 px (Open Graph / social cards)."""
    return _save(fig, name, "social", path, fmt)


def save_for_blog(fig, name, path=".", fmt="png"):
    """Save figure at 800x480 px for blog posts."""
    return _save(fig, name, "blog", path, fmt)


def save_for_slide(fig, name, path=".", fmt="png"):
    """Save figure at 1920x1080 px for presentations."""
    return _save(fig, name, "slide", path, fmt)
