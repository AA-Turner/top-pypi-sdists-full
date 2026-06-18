"""Shared layout UI components."""

from __future__ import annotations

from prefab_ui.components import (
    H1,
    Badge,
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
    BREADCRUMB_NAV_CLASS,
    ENV_BANNER_CLASS,
    HERO_CARD_CLASS,
    _airbyte_logo_svg,
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


_MOCK_BANNER_GRADIENT = "linear-gradient(90deg, #a855f7 0%, #d763ec 100%)"
_PREVIEW_BANNER_GRADIENT = "linear-gradient(90deg, #d97706 0%, #f59e0b 100%)"


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


def _dot_style() -> dict[str, str]:
    return {
        "width": "7px",
        "height": "7px",
        "borderRadius": "50%",
        "background": "#fbbf24",
        "display": "inline-block",
    }


def render_environment_banners() -> None:
    """Render top-line banners for mock mode and/or preview deploys."""
    with (
        If(STATE.is_mock_only),
        Div(
            css_class=ENV_BANNER_CLASS,
            style=_banner_style(_MOCK_BANNER_GRADIENT),
        ),
    ):
        Span("", style=_dot_style())
        Text(
            "Mock Mode \u2014 Demo data only. "
            "No credentials loaded. Apply actions are simulated."
        )
    with (
        If(STATE.is_preview_deploy),
        Div(
            css_class=ENV_BANNER_CLASS,
            style=_banner_style(_PREVIEW_BANNER_GRADIENT),
        ),
    ):
        Span("", style=_dot_style())
        with If(STATE.preview_pr_url):
            Text(
                "\U0001f535 Build Preview \u2014 "
                "This release candidate preview was built from "
            )
            Link(
                "PR #" + STATE.preview_pr_number,
                href=STATE.preview_pr_url,
                target="_blank",
                style={"color": "#fff", "textDecoration": "underline"},
            )
            Text(". Please provide any feedback on the GitHub PR ")
            Link(
                "here",
                href=STATE.preview_pr_url,
                target="_blank",
                style={"color": "#fff", "textDecoration": "underline"},
            )
            Text(".")
        with If(~STATE.preview_pr_url):
            Text("\U0001f535 Build Preview \u2014 You are using a pre-release build.")
