"""UI color palette and theme for Rich integration.

This module centralizes the color scheme and provides a Rich theme object
for consistent styling of Markdown and other Rich-rendered content.

The palette is aligned with the variables in `dreadnode.tcss`.
"""

from __future__ import annotations

import os

# --- Color Palette -----------------------------------------------------------
# Single source of truth for both render paths. `dreadnode.tcss` declares its
# `$` variables as aliases of the `$dn-*` theme variables that `app.py` feeds
# from the constants below, so a value changed here reaches the stylesheet on
# its own. Never write a literal hex into the stylesheet — it would be correct
# for only one theme.


def _is_light() -> bool:
    """Whether ``DREADNODE_TUI_THEME`` selects the light palette.

    Any other value — unset, misspelled, or explicitly ``dark`` — selects dark.
    """
    return os.environ.get("DREADNODE_TUI_THEME", "dark").strip().lower() == "light"


# Read once at import. The palette is baked into the module constants below and
# into the Textual theme registered at app start, so it cannot change without
# restarting the process.
IS_LIGHT = _is_light()

BG = "#ffffff" if IS_LIGHT else "#17191c"
BG_LIGHT = "#f4f5f7" if IS_LIGHT else "#1f2226"
BG_LIGHTER = "#e8eaed" if IS_LIGHT else "#292c31"

# Foreground ramp — four tiers walking away from the background in even ~17 L*
# (perceptual lightness) steps, so each tier is equally distinguishable. Dark
# starts at a crisp, faintly cool near-white (L*97) and steps down; light
# mirrors that spacing upward from near-black. The top three tiers clear WCAG
# AA against BG in both themes; FG_FAINTEST is the quiet tail at roughly 3:1.
FG = "#1f2328" if IS_LIGHT else "#f2f7fc"
FG_SUBTLE = "#57606a" if IS_LIGHT else "#c2c7cc"
FG_MUTED = "#6e7781" if IS_LIGHT else "#95999e"
FG_FAINTEST = "#8c959f" if IS_LIGHT else "#696d72"

# Inline `code` and fenced blocks — prose-colored text on a raised background
# "pill". The pill carries the "this is code" affordance, so the text stays in
# the prose family instead of a saturated accent (which is reserved for tool
# calls). Aliased to the palette by design; set to a literal hex to diverge.
CODE = FG
CODE_BG = BG_LIGHT

# Links — always underlined. Dark keeps them in the prose family so the
# underline alone carries the affordance; light needs a conventional blue,
# because near-black on white is indistinguishable from body copy. Warm accent
# is reserved for tool calls, so links stay quiet and hover to $accent.
LINK = "#0969da" if IS_LIGHT else FG

BORDER = "#d0d7de" if IS_LIGHT else "#2b343f"
BORDER_LIGHT = "#afb8c1" if IS_LIGHT else "#434a55"

INFO = "#0969da" if IS_LIGHT else "#4689bf"
SUCCESS = "#1a7f37" if IS_LIGHT else "#68c147"
WARNING = "#9a6700" if IS_LIGHT else "#c8ac4a"
ERROR = "#cf222e" if IS_LIGHT else "#e44f4f"

# Extended palette — platform screens, data visualization
BRAND = "#bc4c34" if IS_LIGHT else "#ca5e44"
ACCENT = "#cf4b2f" if IS_LIGHT else "#ef562f"
PURPLE = "#8250df" if IS_LIGHT else "#a650fb"
TEAL = "#0b7d75" if IS_LIGHT else "#20dfc8"

SYNTAX_THEME = "default" if IS_LIGHT else "monokai"


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
