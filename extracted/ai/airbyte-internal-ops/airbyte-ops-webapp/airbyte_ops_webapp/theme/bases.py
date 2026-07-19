"""Thematic base components for the Airbyte Ops Webapp.

Every class here is a thin, styled subclass of a Prefab built-in that bakes in
the Airbyte look. The `Ab` prefix marks a component as Airbyte-defined, so at
any call site `Ab*` is ours and bare names (`Div`, `Text`, `Link`, `Badge`,
...) are Prefab built-ins.

Styling is applied two ways, both additive over what the caller passes:

- A semantic `css_class` (`AB_CLASS`) is prepended to any caller `css_class`.
- A default inline `style` dict (`_ab_style`) is merged *under* any caller
  `style`, so callers always win on conflicts.

Inline styles are used for the themed surfaces (backgrounds, borders, gradients)
because the Prefab renderer runs the app inside an iframe that only honors
inline styles and Tailwind utilities — stylesheet rules from the app `Theme`
never reach it. Callers keep composing Tailwind utilities via `css_class`.
"""

from __future__ import annotations

from typing import Any, ClassVar

from prefab_ui.components import Div, Link, Span, Text
from pydantic import Field

from airbyte_ops_webapp.theme.tokens import (
    AIRBYTE_DARK_CARD,
    AIRBYTE_DARK_PANEL,
    AIRBYTE_INK,
    AIRBYTE_LAVENDER,
    AIRBYTE_PRIMARY,
    AIRBYTE_SECONDARY,
    CODE_SURFACE_CLASS,
    DETAIL_BOX_CLASS,
    ENV_BANNER_CLASS,
    ERROR_CARD_CLASS,
    HERO_CARD_CLASS,
    MOCK_CARD_CLASS,
    PAGE_SURFACE_CLASS,
    PANEL_CARD_CLASS,
    PREVIEW_CARD_CLASS,
    PRIMARY_LINK_CLASS,
    STAT_VALUE_CLASS,
    STATUS_CARD_CLASS,
    SUCCESS_CARD_CLASS,
    TABLE_SCROLL_CLASS,
    TOOL_CARD_CLASS,
    TOOL_ICON_CLASS,
    VERSION_FOOTER_CLASS,
    _is_light_theme,
)

_MONO_FONT = "ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace"
_ERROR_ACCENT = "#ff6b6b"


def _merge_css(*classes: str | None) -> str | None:
    """Join non-empty class strings with a space, returning `None` if empty."""
    merged = " ".join(c for c in classes if c)
    return merged or None


# ── Inline style builders ──────────────────────────────────────────────
# These reproduce the themed surfaces as inline style dicts (see module
# docstring for why inline rather than CSS classes).


def _page_style() -> dict[str, str]:
    if _is_light_theme():
        return {
            "background": "#FFFFFF",
            "color": AIRBYTE_INK,
            "minHeight": "100vh",
            "padding": "1.5rem",
        }
    return {
        "background": AIRBYTE_INK,
        "color": "#FFFFFF",
        "minHeight": "100vh",
        "padding": "1.5rem",
    }


def _card_style(*, accent: str | None = None) -> dict[str, str]:
    if _is_light_theme():
        border = accent or AIRBYTE_LAVENDER
        return {
            "background": "#FFFFFF",
            "border": f"1px solid {border}",
            "borderRadius": "0.75rem",
            "boxShadow": "0 10px 15px -3px rgba(20, 15, 67, 0.08)",
            "color": AIRBYTE_INK,
            "padding": "1rem",
        }
    border = accent or "rgba(206, 203, 242, 0.3)"
    return {
        "background": AIRBYTE_DARK_PANEL,
        "border": f"1px solid {border}",
        "borderRadius": "0.75rem",
        "boxShadow": "0 10px 15px -3px rgba(0, 0, 0, 0.35)",
        "color": "#FFFFFF",
        "padding": "1rem",
    }


def _table_scroll_style() -> dict[str, str]:
    return {
        "width": "100%",
        "minWidth": "0",
        "maxHeight": "70vh",
        "overflow": "auto",
    }


def _hero_style() -> dict[str, str]:
    style = _card_style(accent="transparent")
    style["background"] = "#FFFFFF" if _is_light_theme() else AIRBYTE_DARK_CARD
    return style


def _tool_card_style(*, accent: str | None = None) -> dict[str, str]:
    style = _card_style(accent=accent)
    style.update({"height": "100%", "padding": "0.5rem"})
    return style


def _tool_icon_style(*, accent: str = AIRBYTE_PRIMARY) -> dict[str, str]:
    return {
        "alignItems": "center",
        "background": f"color-mix(in srgb, {accent} 34%, transparent)",
        "borderRadius": "0.75rem",
        "color": AIRBYTE_INK if _is_light_theme() else "#FFFFFF",
        "display": "flex",
        "fontWeight": "700",
        "height": "2.75rem",
        "justifyContent": "center",
        "letterSpacing": "0.04em",
        "width": "2.75rem",
    }


def _primary_link_style() -> dict[str, str]:
    return {
        "alignItems": "center",
        "background": AIRBYTE_PRIMARY,
        "borderRadius": "0.625rem",
        "color": "#FFFFFF",
        "display": "inline-flex",
        "fontWeight": "700",
        "gap": "0.5rem",
        "padding": "0.75rem 1rem",
        "textDecoration": "none",
        "width": "fit-content",
    }


def _code_surface_style() -> dict[str, str]:
    if _is_light_theme():
        return {
            "background": "#F7F6FF",
            "border": f"1px solid {AIRBYTE_LAVENDER}",
            "borderRadius": "0.375rem",
            "color": AIRBYTE_INK,
            "fontFamily": _MONO_FONT,
            "fontSize": "0.8125rem",
            "lineHeight": "1.5",
            "overflowX": "auto",
            "padding": "0.75rem",
            "whiteSpace": "pre-wrap",
        }
    return {
        "background": "#0F0B33",
        "border": "1px solid rgba(206, 203, 242, 0.3)",
        "borderRadius": "0.375rem",
        "color": AIRBYTE_LAVENDER,
        "fontFamily": _MONO_FONT,
        "fontSize": "0.8125rem",
        "lineHeight": "1.5",
        "overflowX": "auto",
        "padding": "0.75rem",
        "whiteSpace": "pre-wrap",
    }


def _detail_box_style() -> dict[str, str]:
    return {
        "marginTop": "0.75rem",
        "padding": "16px",
        "backgroundColor": "#1a1545",
        "border": "1px solid rgba(206, 203, 242, 0.2)",
        "borderRadius": "6px",
        "fontSize": "0.85rem",
    }


def _version_footer_style() -> dict[str, str]:
    return {
        "display": "flex",
        "alignItems": "center",
        "justifyContent": "center",
        "gap": "0.75rem",
        "padding": "0.75rem 1rem",
        "fontSize": "0.75rem",
        "opacity": "0.5",
        "color": "#ccc",
    }


def _banner_style(gradient: str) -> dict[str, str]:
    return {
        "background": gradient,
        "color": "#fff",
        "display": "flex",
        "alignItems": "center",
        "justifyContent": "center",
        "gap": "0.5rem",
        "padding": "0.375rem 1rem",
        "fontSize": "0.8125rem",
        "fontWeight": "600",
        "letterSpacing": "0.02em",
        "textAlign": "center",
        "width": "100%",
    }


# ── Styled-default mixin ───────────────────────────────────────────────


class _StyledDefault:
    """Mixin that bakes a default `css_class` and inline `style` onto a Prefab
    component.

    Subclasses set `AB_CLASS` (prepended to any caller `css_class`) and/or
    override `_ab_style()` (merged *under* any caller `style`, so callers always
    win on conflicts).
    """

    AB_CLASS: ClassVar[str] = ""

    def _ab_style(self) -> dict[str, str] | None:
        """Return the default inline style for this component, or `None`."""
        return None

    def model_post_init(self, __context: Any) -> None:
        if self.AB_CLASS:
            self.css_class = _merge_css(self.AB_CLASS, self.css_class)  # type: ignore[attr-defined]
        default_style = self._ab_style()
        if default_style:
            merged = {**default_style, **(self.style or {})}  # type: ignore[attr-defined]
            self.style = merged  # type: ignore[attr-defined]
        super().model_post_init(__context)  # type: ignore[misc]


# ── Page surface ───────────────────────────────────────────────────────


class AbPage(_StyledDefault, Div):
    """Full-height page surface that paints the themed background."""

    AB_CLASS: ClassVar[str] = PAGE_SURFACE_CLASS

    def _ab_style(self) -> dict[str, str]:
        return _page_style()


# ── Card / surface hierarchy ───────────────────────────────────────────


class AbCard(_StyledDefault, Div):
    """Base panel surface: rounded, bordered, themed background and padding."""

    AB_CLASS: ClassVar[str] = PANEL_CARD_CLASS

    def _ab_style(self) -> dict[str, str]:
        return _card_style()


class AbHeroCard(_StyledDefault, Div):
    """Gradient hero banner surface used at the top of each page."""

    AB_CLASS: ClassVar[str] = HERO_CARD_CLASS

    def _ab_style(self) -> dict[str, str]:
        return _hero_style()


class AbToolCard(_StyledDefault, Div):
    """Panel surface for home-page tool tiles (tighter padding, full height).

    The `accent` sets the border tint, matching the tile's icon accent.
    """

    AB_CLASS: ClassVar[str] = f"{PANEL_CARD_CLASS} {TOOL_CARD_CLASS}"
    accent: str = Field(default=AIRBYTE_PRIMARY, exclude=True)

    def _ab_style(self) -> dict[str, str]:
        return _tool_card_style(accent=self.accent)


class AbStatusCard(_StyledDefault, Div):
    """Panel surface for at-a-glance status/metric tiles."""

    AB_CLASS: ClassVar[str] = STATUS_CARD_CLASS

    def _ab_style(self) -> dict[str, str]:
        return _card_style()


class AbPreviewCard(_StyledDefault, Div):
    """Panel surface for previews and loading states (primary accent border)."""

    AB_CLASS: ClassVar[str] = PREVIEW_CARD_CLASS

    def _ab_style(self) -> dict[str, str]:
        return _card_style(accent=AIRBYTE_PRIMARY)


class AbSuccessCard(_StyledDefault, Div):
    """Panel surface for success results (secondary accent border)."""

    AB_CLASS: ClassVar[str] = SUCCESS_CARD_CLASS

    def _ab_style(self) -> dict[str, str]:
        return _card_style(accent=AIRBYTE_SECONDARY)


class AbErrorCard(_StyledDefault, Div):
    """Panel surface for error results (red accent border)."""

    AB_CLASS: ClassVar[str] = ERROR_CARD_CLASS

    def _ab_style(self) -> dict[str, str]:
        return _card_style(accent=_ERROR_ACCENT)


class AbMockCard(_StyledDefault, Div):
    """Panel surface highlighting mock-mode content (secondary accent border)."""

    AB_CLASS: ClassVar[str] = MOCK_CARD_CLASS

    def _ab_style(self) -> dict[str, str]:
        return _card_style(accent=AIRBYTE_SECONDARY)


class AbCodeSurface(_StyledDefault, Div):
    """Monospace code/JSON surface with a subtle inset background."""

    AB_CLASS: ClassVar[str] = CODE_SURFACE_CLASS

    def _ab_style(self) -> dict[str, str]:
        return _code_surface_style()


class AbTableScroll(_StyledDefault, Div):
    """Height-capped, both-axis scroll region for wrapping a wide/tall `DataTable`.

    The Prefab renderer wraps every table in a `.pf-table-container` that is
    relaxed to `overflow: visible` (in `RENDERER_OVERRIDE_CSS`) so its sticky
    header can escape to the nearest real scroll parent. A `DataTable` placed
    directly in a card therefore has *no* scroll parent, so wide tables bleed
    past the card's right edge with no way to scroll to the clipped columns.
    Wrapping the table in this component supplies that scroll parent: wide tables
    scroll horizontally instead of overflowing, tall tables scroll vertically,
    and the sticky header pins to this wrapper. Use it for any `DataTable` not
    already inside a height-capped scroll parent (e.g. a modal or CVM panel).
    """

    AB_CLASS: ClassVar[str] = TABLE_SCROLL_CLASS

    def _ab_style(self) -> dict[str, str]:
        return _table_scroll_style()


class AbDetailBox(_StyledDefault, Div):
    """Inset detail panel used for expanded rows and metadata dumps."""

    AB_CLASS: ClassVar[str] = DETAIL_BOX_CLASS

    def _ab_style(self) -> dict[str, str]:
        return _detail_box_style()


class AbVersionFooter(_StyledDefault, Div):
    """Subtle centered footer for deployed version metadata."""

    AB_CLASS: ClassVar[str] = VERSION_FOOTER_CLASS

    def _ab_style(self) -> dict[str, str]:
        return _version_footer_style()


class AbToolIcon(_StyledDefault, Div):
    """Rounded icon tile whose fill tints toward `accent`.

    Wrap an `Svg` or emoji `Text`; the accent drives a translucent
    `color-mix` background while the base supplies size and centering.
    """

    AB_CLASS: ClassVar[str] = TOOL_ICON_CLASS
    accent: str = Field(default=AIRBYTE_PRIMARY, exclude=True)

    def _ab_style(self) -> dict[str, str]:
        return _tool_icon_style(accent=self.accent)


class AbEnvBanner(_StyledDefault, Div):
    """Full-width environment banner (mock mode, build preview) with a gradient."""

    AB_CLASS: ClassVar[str] = ENV_BANNER_CLASS
    gradient: str = Field(exclude=True)

    def _ab_style(self) -> dict[str, str]:
        return _banner_style(self.gradient)


# ── Links ──────────────────────────────────────────────────────────────


class AbPrimaryLink(_StyledDefault, Link):
    """Primary call-to-action link styled as a filled button."""

    AB_CLASS: ClassVar[str] = PRIMARY_LINK_CLASS

    def _ab_style(self) -> dict[str, str]:
        return _primary_link_style()


# ── Typography ─────────────────────────────────────────────────────────


class AbStatValue(_StyledDefault, Text):
    """Prominent numeric/status value."""

    AB_CLASS: ClassVar[str] = STAT_VALUE_CLASS


class AbSectionTitle(_StyledDefault, Text):
    """Card/section heading."""

    AB_CLASS: ClassVar[str] = "text-lg font-bold"


class AbFieldLabel(_StyledDefault, Text):
    """Muted label describing an adjacent value or input."""

    AB_CLASS: ClassVar[str] = "text-sm opacity-70"


class AbFieldValue(_StyledDefault, Text):
    """Emphasized value or form field label."""

    AB_CLASS: ClassVar[str] = "text-sm font-medium"


class AbCardLabel(_StyledDefault, Text):
    """Small uppercase-weight caption for status-card fields."""

    AB_CLASS: ClassVar[str] = "text-xs font-semibold opacity-70"


class AbCardValue(_StyledDefault, Text):
    """Primary value shown inside a status card."""

    AB_CLASS: ClassVar[str] = "text-xl font-bold"


class AbCardMeta(_StyledDefault, Text):
    """Muted secondary metadata line inside a card."""

    AB_CLASS: ClassVar[str] = "text-xs opacity-60"


class AbFieldCaption(_StyledDefault, Span):
    """Uppercase gray caption for label/value detail rows."""

    AB_CLASS: ClassVar[str] = (
        "block text-[0.7rem] font-semibold uppercase tracking-[0.03em] text-[#9ca3af]"
    )


class AbDetailValue(_StyledDefault, Span):
    """Detail value paired with `AbFieldCaption` (wraps on long tokens)."""

    AB_CLASS: ClassVar[str] = "block text-[0.85rem] text-[#e5e7eb] break-all"


class AbScopeBadge(_StyledDefault, Span):
    """Pill badge marking a pin scope."""

    AB_CLASS: ClassVar[str] = (
        "inline-block px-2 py-px rounded-full text-xs font-medium "
        "bg-[rgba(93,81,213,0.3)] text-[#CECBF2]"
    )
