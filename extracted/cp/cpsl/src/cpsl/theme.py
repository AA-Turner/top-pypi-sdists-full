"""Declarative theming for subdomain apps.

Provides a ``Theme`` dataclass that controls colors, typography, border radii,
and branding (logo / tagline). Includes built-in presets that can be used as
starting points.

Usage::

    app = cpsl.App(name="my-app")
    app.theme(preset="light", accent="#e09145", logo="assets/logo.png")
"""

from __future__ import annotations

from dataclasses import dataclass, fields, asdict
from typing import Any, Literal


Radius = Literal["sm", "md", "lg"]
"""Border-radius scale applied to cards, inputs, and containers."""

PresetName = Literal["dark", "light", "midnight", "warm"]
"""Names of the built-in theme presets."""


@dataclass
class Theme:
    """Visual theme for a Capsule subdomain app.

    All color fields accept CSS color values (hex recommended, e.g.
    ``"#1565c0"``).  Font fields accept any valid CSS ``font-family``
    value — a single family name or a comma-separated fallback stack
    (e.g. ``"Inter, system-ui, sans-serif"``).

    Use ``app.theme(preset="dark")`` to start from a built-in preset,
    then override individual fields::

        app.theme(preset="dark", accent="#e09145", font_sans="Inter")

    Or build a fully custom theme by setting every field::

        app.theme(
            primary="#1565c0",
            accent="#d97706",
            background="#ffffff",
            foreground="#1a1d21",
            ...
        )

    Attributes:
        preset: The preset name used to build this theme (``"dark"``,
            ``"light"``, ``"midnight"``, ``"warm"``). Sent to the
            frontend so the UI can default to the correct light/dark
            mode and toggle properly.
        logo: Path to a logo image (relative to app root) or a URL.
        logo_background: Background color behind the logo (hex, e.g.
            ``"#3B6EC2"``). Useful for transparent SVGs/PNGs that need
            contrast against the sidebar.
        tagline: Short text displayed below the app name in the sidebar.
        title: Browser and link-preview title. Falls back to app name.
        description: Meta/OpenGraph/Twitter description.
        site_name: OpenGraph site name.
        preview_image: OpenGraph/Twitter preview image URL or asset path.
        favicon: Browser favicon URL or asset path.
        primary: Interactive elements — links, buttons, focus rings.
        accent: Warm highlight for emphasis — use sparingly.
        background: Page background color.
        foreground: Primary text color.
        sidebar: Sidebar / navigation background.
        surface: Raised surface color for cards, panels, popovers.
        border: Borders, dividers, and separators.
        muted: Secondary / de-emphasized text.
        danger: Destructive actions and error states.
        success: Success states and confirmations.
        font_sans: CSS ``font-family`` for body text (e.g. ``"DM Sans"``
            or ``"Inter, system-ui, sans-serif"``).
        font_mono: CSS ``font-family`` for code and data values.
        radius: Border-radius scale — ``"sm"``, ``"md"``, or ``"lg"``.
    """

    # preset name — forwarded to the frontend for light/dark default
    preset: PresetName | None = None

    # branding
    logo: str | None = None
    logo_background: str | None = None
    tagline: str | None = None
    title: str | None = None
    description: str | None = None
    site_name: str | None = None
    preview_image: str | None = None
    favicon: str | None = None

    # colors (CSS color values, hex recommended)
    primary: str | None = None
    accent: str | None = None
    background: str | None = None
    foreground: str | None = None
    sidebar: str | None = None
    surface: str | None = None
    border: str | None = None
    muted: str | None = None
    danger: str | None = None
    success: str | None = None

    # typography (CSS font-family values)
    font_sans: str | None = None
    font_mono: str | None = None

    # shape
    radius: Radius | None = None

    def to_dict(self) -> dict[str, Any]:
        return {k: v for k, v in asdict(self).items() if v is not None}

    def merge(self, overrides: dict[str, Any]) -> Theme:
        """Return a new Theme with non-None overrides applied on top."""
        base = asdict(self)
        for k, v in overrides.items():
            if v is not None and k in base:
                base[k] = v
        return Theme(**base)


# ---------------------------------------------------------------------------
# Built-in presets
# ---------------------------------------------------------------------------

_DEFAULT_FONT_SANS = '"Inter", ui-sans-serif, system-ui, sans-serif'

PRESETS: dict[PresetName, Theme] = {
    "dark": Theme(
        primary="#60a5fa",
        accent="#60a5fa",
        background="#1a1a1a",
        foreground="#f0f0f0",
        sidebar="#1a1a1a",
        surface="#232323",
        border="#303030",
        muted="#969696",
        danger="#f87171",
        success="#86efac",
        font_sans=_DEFAULT_FONT_SANS,
    ),
    "light": Theme(
        primary="#2563eb",
        accent="#d97706",
        background="#faf9f6",
        foreground="#16140f",
        sidebar="#faf9f6",
        surface="#f2f1ed",
        border="#dcdad4",
        muted="#6b665b",
        danger="#dc2626",
        success="#16a34a",
        font_sans=_DEFAULT_FONT_SANS,
    ),
    "midnight": Theme(
        primary="#38bdf8",
        accent="#a78bfa",
        background="#0f172a",
        foreground="#e2e8f0",
        sidebar="#0f172a",
        surface="#1e293b",
        border="#293449",
        muted="#94a3b8",
        danger="#f87171",
        success="#34d399",
        font_sans=_DEFAULT_FONT_SANS,
    ),
    "warm": Theme(
        primary="#b45309",
        accent="#dc8b4f",
        background="#fdf8f0",
        foreground="#292524",
        sidebar="#fdf8f0",
        surface="#faebd7",
        border="#d6cfc7",
        muted="#78716c",
        danger="#b91c1c",
        success="#15803d",
        font_sans=_DEFAULT_FONT_SANS,
    ),
}


def resolve_theme(
    preset: PresetName | None = None,
    **overrides: Any,
) -> Theme:
    """Build a Theme from an optional preset plus keyword overrides.

    Args:
        preset: One of ``"dark"``, ``"light"``, ``"midnight"``, ``"warm"``.
        **overrides: Any ``Theme`` field to override (e.g. ``accent="#e09145"``).

    Raises:
        ValueError: If ``preset`` is not recognized or an override key
            does not match a ``Theme`` field.
    """
    valid_fields = {f.name for f in fields(Theme)}
    bad = set(overrides) - valid_fields
    if bad:
        raise ValueError(f"Unknown theme fields: {', '.join(sorted(bad))}")

    if preset is not None:
        if preset not in PRESETS:
            raise ValueError(f"Unknown preset '{preset}'. Available: {', '.join(sorted(PRESETS))}")
        base = PRESETS[preset]
        result = base.merge(overrides)
        result.preset = preset
        return result

    return Theme(**{k: v for k, v in overrides.items() if v is not None})
