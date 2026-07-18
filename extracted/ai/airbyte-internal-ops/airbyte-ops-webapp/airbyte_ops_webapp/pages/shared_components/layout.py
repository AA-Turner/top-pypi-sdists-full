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
    ENV_BANNER_DOT_CLASS,
    ENV_BANNER_LINK_CLASS,
    VERSION_FOOTER_LINK_CLASS,
    AbEnvBanner,
    AbHeroCard,
    AbVersionFooter,
    _airbyte_logo_svg,
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
        AbHeroCard(),
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


def render_environment_banners() -> None:
    """Render top-line banners for mock mode and/or preview deploys."""
    with (
        If(STATE.is_mock_only),
        AbEnvBanner(gradient=_MOCK_BANNER_GRADIENT),
    ):
        Span("", css_class=ENV_BANNER_DOT_CLASS)
        Text(
            "Mock Mode \u2014 Demo data only. "
            "No credentials loaded. Apply actions are simulated."
        )
    with (
        If(STATE.is_preview_deploy),
        AbEnvBanner(gradient=_PREVIEW_BANNER_GRADIENT),
    ):
        Span("", css_class=ENV_BANNER_DOT_CLASS)
        with If(STATE.preview_pr_url):
            Text(
                "\U0001f535 Build Preview \u2014 "
                "This release candidate preview was built from "
            )
            Link(
                "PR #" + STATE.preview_pr_number,
                href=STATE.preview_pr_url,
                target="_blank",
                css_class=ENV_BANNER_LINK_CLASS,
            )
            Text(". Please provide any feedback on the GitHub PR ")
            Link(
                "here",
                href=STATE.preview_pr_url,
                target="_blank",
                css_class=ENV_BANNER_LINK_CLASS,
            )
            Text(".")
        with If(~STATE.preview_pr_url):
            Text("\U0001f535 Build Preview \u2014 You are using a pre-release build.")


def render_version_footer() -> None:
    """Render a subtle footer showing deployed version info."""
    with AbVersionFooter():
        with If(STATE.ops_package_version):
            Text("v" + STATE.ops_package_version)
        with If(STATE.ops_package_version & STATE.deploy_sha):
            Text("\u00b7")
        with If(STATE.deploy_sha):
            Link(
                STATE.deploy_sha,
                href=STATE.deploy_sha_url,
                target="_blank",
                css_class=VERSION_FOOTER_LINK_CLASS,
            )
        with If(~STATE.deploy_sha & ~STATE.ops_package_version):
            Text("version unknown")
