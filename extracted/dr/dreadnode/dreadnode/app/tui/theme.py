"""UI color palette and theme for Rich integration.

This module centralizes the color scheme and provides a Rich theme object
for consistent styling of Markdown and other Rich-rendered content.

The palette is aligned with the variables in `dreadnode.tcss`.
"""

from __future__ import annotations

# --- Color Palette -----------------------------------------------------------
# Single source of truth.  When changing values here, also update the matching
# CSS variables in dreadnode.tcss (they cannot be auto-generated).

BG = "#0b0f14"
BG_LIGHT = "#0f141c"
BG_LIGHTER = "#141922"

FG = "#e2e7ec"
FG_SUBTLE = "#c1c6cc"
FG_MUTED = "#9da0a5"
FG_FAINTEST = "#686d73"

BORDER = "#2b343f"
BORDER_LIGHT = "#434a55"

INFO = "#4689bf"
SUCCESS = "#68c147"
WARNING = "#c8ac4a"
ERROR = "#e44f4f"

# Extended palette — platform screens, data visualization
BRAND = "#ca5e44"
ACCENT = "#ef562f"
PURPLE = "#a650fb"
TEAL = "#20dfc8"


# --- Graphic (paste new art here; wordmark is auto-composed to the right) ---

GRAPHIC = r""""""
# GRAPHIC = r"""
#           █ █████
#         ████ ██████
#        ██████ ██████
#        ███ ███    ██
#        ████████  ███
#        ██████████ ██
#        ▓██████████ ▓
#         ▓▓▓█████▓▓▓
#     ██     ██▓██     ██
#    ██     ██▓▓▓██     ██
#    ▓██████▓▓   ▓▓██████▓
#  ██ ▓▓▓▓▓▓   ░   ▓▓▓▓▓▓ ██
# ██    ██   ░ ░ ░   ██    ██
# ▓█████▓▓ ░ ░   ░ ░ ▓▓█████▓
#  ▓▓▓▓▓   ░   ░   ░   ▓▓▓▓▓
#            ░   ░
#          ░       ░
# """.strip("\n")

# --- Wordmarks (two sizes of "DREADNODE" in block text) ---------------------

WORDMARK_L = r"""
██████   ██████   ███████   █████   ██████   ██   ██  ██████  ██████   ███████
██   ██  ██   ██  ██       ██   ██  ██   ██  ███  ██  ██  ██  ██   ██  ██
██   ██  █████    █████    ███████  ██   ██  ██ ████  ██  ██  ██   ██  █████
██   ██  ██  ██   ██       ██   ██  ██   ██  ██  ███  ██  ██  ██   ██  ██
██████   ██   ██  ███████  ██   ██  ██████   ██   ██  ██████  ██████   ███████
""".strip("\n")

WORDMARK_M = r"""
▗▄▄▄ ▗▄▄▖ ▗▄▄▄▖ ▗▄▖ ▗▄▄▄ ▗▖  ▗▖ ▗▄▖ ▗▄▄▄ ▗▄▄▄▖
▐▌  █▐▌ ▐▌▐▌   ▐▌ ▐▌▐▌  █▐▛▚▖▐▌▐▌ ▐▌▐▌  █▐▌
▐▌  █▐▛▀▚▖▐▛▀▀▘▐▛▀▜▌▐▌  █▐▌ ▝▜▌▐▌ ▐▌▐▌  █▐▛▀▀▘
▐▙▄▄▀▐▌ ▐▌▐▙▄▄▖▐▌ ▐▌▐▙▄▄▀▐▌  ▐▌▝▚▄▞▘▐▙▄▄▀▐▙▄▄▖
""".strip("\n")


# --- Composition helpers ----------------------------------------------------


def _pad(raw: str) -> str:
    """Right-pad every line to the widest line so the logo forms a solid rectangle."""
    lines = raw.splitlines()
    w = max(len(line) for line in lines)
    return "\n".join(line.ljust(w) for line in lines)


def _compose(graphic: str, wordmark: str, gap: int = 8) -> str:
    """Place *wordmark* vertically centred to the right of *graphic* with *gap* spaces."""
    g_lines = _pad(graphic).splitlines()
    w_lines = _pad(wordmark).splitlines()
    top = (len(g_lines) - len(w_lines)) // 2
    out: list[str] = []
    for i, gl in enumerate(g_lines):
        wi = i - top
        if 0 <= wi < len(w_lines):
            out.append(gl + " " * gap + w_lines[wi])
        else:
            out.append(gl)
    return _pad("\n".join(out))


# --- Composed logos (breakpoints auto-computed) -----------------------------

L_LOGO = _pad(WORDMARK_L)
M_LOGO = _pad(WORDMARK_M)

# Minimum terminal widths to show each logo variant (padded width + 2).
# Ordered largest → smallest; below M, fall back to plain text "DREADNODE".
LOGOS: list[tuple[int, str]] = [
    (len(L_LOGO.splitlines()[0]) + 2, L_LOGO),
    (len(M_LOGO.splitlines()[0]) + 2, M_LOGO),
]


def pick_logo(width: int) -> str | None:
    """Return the largest logo that fits in *width*, or ``None`` to fall back to text."""
    for min_w, logo in LOGOS:
        if width >= min_w:
            return logo
    return None
