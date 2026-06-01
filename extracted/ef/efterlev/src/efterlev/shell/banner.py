"""ASCII banner rendered on shell entry.

Uses the classic figlet "standard" font rendering of "Efterlev".
Earlier attempts at literal interpretations of the efterlev.org
logotype (box-drawing characters at v0.1.132; block characters at
v0.1.133) either fragmented on common terminals (box-drawing) or
read as too-bold and unrelated to the logo (block). The figlet
standard font renders reliably across terminals, is instantly
recognizable, and stays compact enough that the banner doesn't
dominate the session.

Single source of truth: the banner is pure data. To refine the
glyphs, edit BANNER_LINES — no logic touches.
"""

from __future__ import annotations

BANNER_LINES: tuple[str, ...] = (
    "   _____  __ _            _            ",
    "  | ____|/ _| |_ ___ _ __| | _____   __",
    "  |  _| | |_| __/ _ \\ '__| |/ _ \\ \\ / /",
    "  | |___|  _| ||  __/ |  | |  __/\\ V / ",
    "  |_____|_|  \\__\\___|_|  |_|\\___| \\_/  ",
)


def render_banner() -> str:
    """Return the banner as a multi-line string, no trailing newline."""
    return "\n".join(BANNER_LINES)
