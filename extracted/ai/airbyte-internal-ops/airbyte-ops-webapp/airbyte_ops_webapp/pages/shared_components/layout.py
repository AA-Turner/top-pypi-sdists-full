"""Shared layout UI components."""

from prefab_ui.components import (
    H1,
    Badge,
    CardContent,
    CardHeader,
    Column,
    Div,
    Row,
    Svg,
    Text,
)
from prefab_ui.components.control_flow import If
from prefab_ui.rx import STATE

from airbyte_ops_webapp.pages.shared_components.auth import render_compact_auth_controls
from airbyte_ops_webapp.theme import (
    AIRBYTE_LOGO_CLASS,
    AIRBYTE_SECONDARY,
    HERO_CARD_CLASS,
    MOCK_CARD_CLASS,
    _airbyte_logo_svg,
    _card_style,
    _hero_style,
)


def render_page_hero(
    *,
    title: str,
    description: str,
    show_auth_controls: bool = False,
) -> None:
    with (
        Div(css_class=HERO_CARD_CLASS, style=_hero_style()),
        CardHeader(),
        Column(gap=3),
    ):
        with (
            Row(
                align="center",
                justify="end",
                gap=3,
                css_class="airbyte-hero-header",
            ),
            Column(align="end", gap=2),
        ):
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
                render_compact_auth_controls()
        H1(title)
        Text(description)


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
