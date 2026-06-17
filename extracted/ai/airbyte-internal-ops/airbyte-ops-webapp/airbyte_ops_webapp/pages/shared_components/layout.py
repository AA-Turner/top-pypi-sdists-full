"""Shared layout UI components."""

from __future__ import annotations

from prefab_ui.components import (
    H1,
    Badge,
    CardContent,
    CardHeader,
    Column,
    Div,
    Link,
    Row,
    Span,
    Svg,
    Text,
)
from prefab_ui.components.control_flow import If
from prefab_ui.rx import STATE

from airbyte_ops_webapp.pages.shared_components.auth import render_auth_status
from airbyte_ops_webapp.theme import (
    AIRBYTE_LOGO_CLASS,
    AIRBYTE_SECONDARY,
    BREADCRUMB_NAV_CLASS,
    HERO_CARD_CLASS,
    MOCK_CARD_CLASS,
    _airbyte_logo_svg,
    _card_style,
    _hero_style,
)

OPS_HOME_PATH = "/home"
OPS_HOME_LABEL = "Ops Home"


def render_page_hero(
    *,
    title: str,
    description: str,
    show_auth_controls: bool = False,
) -> None:
    with (
        Div(css_class=HERO_CARD_CLASS, style=_hero_style()),
        CardHeader(),
        Row(
            align="start",
            justify="between",
            gap=4,
            css_class="airbyte-hero-header",
        ),
    ):
        with Column(gap=2, css_class="airbyte-hero-copy"):
            H1(title)
            Text(description)
        with Column(align="end", gap=2, css_class="airbyte-hero-actions"):
            Svg(
                _airbyte_logo_svg(),
                width="160px",
                height="64px",
                cssClass=AIRBYTE_LOGO_CLASS,
            )
            Badge(
                "Internal Operations",
                css_class="w-fit bg-[#D763EC] text-white",
            )
            if show_auth_controls:
                render_auth_status()


def render_breadcrumb_nav(*, current_page: str) -> None:
    """Render a breadcrumb navigation row above the page hero.

    Shows `Ops Home / Current Page` with Ops Home as a clickable link.
    On the home page itself, only the current label is shown (no link).
    """
    with Div(css_class=BREADCRUMB_NAV_CLASS):
        if current_page == OPS_HOME_LABEL:
            Span(f"⚙️ {OPS_HOME_LABEL}", css_class="breadcrumb-current")
        else:
            Link(
                f"⚙️ {OPS_HOME_LABEL}",
                href=OPS_HOME_PATH,
                target="_top",
            )
            Span(" / ", css_class="breadcrumb-separator")
            Span(current_page, css_class="breadcrumb-current")


def render_mock_mode_banner() -> None:
    with (
        If(STATE.is_mock_only),
        Div(
            css_class=MOCK_CARD_CLASS,
            style=_card_style(accent=AIRBYTE_SECONDARY),
        ),
        CardContent(),
    ):
        Text(
            "Mock mode is enabled. The app uses demo data, loads no "
            "credentials, and apply completes without changing Airbyte Cloud."
        )
