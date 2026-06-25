"""Named color constants and palettes matching joshuampeck.com."""

from matplotlib.colors import LinearSegmentedColormap

# Brand colors
NAVY = "#1B2A4A"
GOLD = "#C8A951"
GOLD_DARK = "#A8891F"
CREAM = "#F8F7F4"
SILK = "#E5E3DF"
INK = "#1A1A1A"
MUTED = "#6B7280"
WHITE = "#FFFFFF"

# Dark-theme surface tokens
CHARCOAL = "#252A36"   # primary dark background
GRID_DARK = "#3A4150"  # subtle gridline tuned for CHARCOAL

# Status colors
RED = "#E74C3C"
YELLOW = "#F1C40F"
GREEN = "#27AE60"

# Light gold variant for dark-mode contrast
GOLD_LIGHT = "#E8D5A3"

# Color cycles for multi-series charts
PALETTE = [NAVY, GOLD, RED, GREEN, MUTED, GOLD_DARK, YELLOW]
PALETTE_DARK = [GOLD, GOLD_LIGHT, RED, GREEN, CREAM, YELLOW, MUTED]

# Sequential colormaps
CMAP_GOLD = LinearSegmentedColormap.from_list(
    "peck_gold", [CREAM, GOLD, NAVY]
)
CMAP_NAVY = LinearSegmentedColormap.from_list(
    "peck_navy", [NAVY, GOLD]
)
