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
SAGE = "#8A9A6B"

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


# ── TrueCode Capital palette ──────────────────────────────────────────────
# Additive: every token above keeps its original value so the existing
# charts render unchanged. Source of truth for everything below is
# Branding/truecode-visual-style-guide.md.

# Core tokens
PAPER = "#252A36"      # --paper, primary dark ground (same value as CHARCOAL)
ACCENT = "#CFB023"     # --accent, the brand gold — one highlighted series only
INK_SOFT = "#9AA0A8"   # --ink-soft, secondary text, eyebrow, footer, labels
RULE = "#4B4F54"       # --rule, borders and dividers

# Gold ramp
ACCENT_DARK = "#8C7920"
ACCENT_LIGHT = "#E0CC70"
ACCENT_PALE = "#F1E7BD"

# Navy ramp
NAVY_DARK = "#172C49"
NAVY_BASE = "#1B365D"
NAVY_LIGHT = "#6B7C96"
NAVY_PALE = "#BBC3CE"

# Neutral ramp, slate → white
NEUTRAL_900 = "#252A36"
NEUTRAL_800 = "#3F444E"
NEUTRAL_700 = "#62666E"
NEUTRAL_600 = "#878A90"
NEUTRAL_500 = "#A8AAAF"
NEUTRAL_400 = "#C2C3C7"
NEUTRAL_300 = "#D8D9DB"
NEUTRAL_200 = "#E9EAEB"
NEUTRAL_100 = "#F6F6F7"

# Semantic data & status colors. Gold is brand, never direction — the guide
# is explicit that "up" is green, not gold.
POSITIVE = "#3F8F6B"
NEGATIVE = "#B0473F"
WARNING = "#CFB023"
INFO = "#3A6EA5"
NEUTRAL = "#878A90"

# Categorical sequence, ordered for maximum separation early. SAGE above
# already carries the guide's value, so it is reused rather than redefined.
TEAL = "#3A8A86"
CLAY = "#B06A3F"
SLATE = "#6B7C96"
PLUM = "#7D5A7A"
SAND = "#D8C9A0"
CHART_SEQ = [ACCENT, NAVY_BASE, TEAL, CLAY, SLATE, SAGE, PLUM, SAND]

# Diverging ramp: negative ↔ neutral ↔ positive
CMAP_TC_DIVERGING = LinearSegmentedColormap.from_list(
    "truecode_diverging",
    [NEGATIVE, "#D99C96", NEUTRAL_100, "#93C3AA", POSITIVE],
)

# Sequential navy ramp, light → dark
CMAP_TC_NAVY = LinearSegmentedColormap.from_list(
    "truecode_navy", [NAVY_PALE, NAVY_LIGHT, NAVY_BASE, NAVY_DARK]
)

# Second-tier negative, for a chart that stacks two different negative
# quantities. Keeps NEGATIVE for the primary series and gives the recessive
# one its own red. SOFT is the diverging ramp's light step; DEEP is derived
# from NEGATIVE toward PAPER.
NEGATIVE_SOFT = "#D99C96"
NEGATIVE_DEEP = "#7F3D3C"
