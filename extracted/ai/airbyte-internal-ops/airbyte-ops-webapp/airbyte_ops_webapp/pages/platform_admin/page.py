"""Platform Admin hub page."""

from __future__ import annotations

from fastmcp import FastMCP, FastMCPApp
from prefab_ui.app import PrefabApp
from prefab_ui.components import H3, Badge, CardContent, Column, Grid, Text
from prefab_ui.components.control_flow import If
from prefab_ui.rx import STATE

from airbyte_ops_webapp.app_shell import build_ops_app
from airbyte_ops_webapp.auth.oauth import hydrate_oauth_action, oauth_config
from airbyte_ops_webapp.pages.authorization.defaults import OPS_AUTHORIZATION_PATH
from airbyte_ops_webapp.pages.platform_admin.agents import (
    PLATFORM_ADMIN_AGENTS_CALLOUT,
)
from airbyte_ops_webapp.pages.platform_admin.data_worker_allocation.defaults import (
    DATA_WORKER_ALLOCATION_EMOJI,
    DATA_WORKER_ALLOCATION_PATH,
)
from airbyte_ops_webapp.pages.platform_admin.defaults import (
    PLATFORM_ADMIN_EMOJI,
    PLATFORM_ADMIN_LABEL,
    PLATFORM_ADMIN_TOOL_NAME,
)
from airbyte_ops_webapp.pages.shared_components.layout import (
    render_breadcrumb_nav,
    render_emoji_icon,
    render_environment_banners,
    render_page_hero,
    render_version_footer,
)
from airbyte_ops_webapp.state import OpsPageState
from airbyte_ops_webapp.theme import (
    AIRBYTE_LAVENDER,
    AIRBYTE_SECONDARY,
    PAGE_CLASS,
    AbPage,
    AbPrimaryLink,
    AbToolCard,
)

platform_admin_app = FastMCPApp("Platform Admin")


def _render_data_worker_allocation_card() -> None:
    with AbToolCard(), CardContent(), Column(gap=3):
        render_emoji_icon(DATA_WORKER_ALLOCATION_EMOJI)
        H3("Data Worker Allocation")
        Text(
            "Review organization capacity by dataplane group, and add or remove "
            "Data Worker capacity."
        )
        with If(~STATE.oauth_authenticated):
            Badge(
                "Sign-in required",
                css_class="w-fit bg-[#CECBF2] text-[#140F43]",
            )
            AbPrimaryLink(
                "Log in with Airbyte",
                href=OPS_AUTHORIZATION_PATH,
                target="_top",
            )
        with If(STATE.oauth_authenticated):
            Badge("Ready", variant="success")
            AbPrimaryLink(
                "Open tool",
                href=DATA_WORKER_ALLOCATION_PATH,
                target="_top",
            )


def _render_more_tools_card() -> None:
    with AbToolCard(accent=AIRBYTE_LAVENDER), CardContent(), Column(gap=3):
        render_emoji_icon("✨", accent=AIRBYTE_SECONDARY)
        H3("More admin tools coming soon")
        Text("Additional instance-admin workflows will appear here.")
        Badge("Coming soon", css_class="w-fit bg-[#CECBF2] text-[#140F43]")


@platform_admin_app.ui(
    name=PLATFORM_ADMIN_TOOL_NAME,
    title=PLATFORM_ADMIN_LABEL,
    description="Open the Platform Admin hub.",
)
def platform_admin() -> PrefabApp:
    """Open the Platform Admin hub."""
    current_oauth_config = oauth_config()
    state = OpsPageState.from_env(oauth_config=current_oauth_config).to_prefab_state()
    with (
        build_ops_app(
            title="Platform Admin",
            state=state,
            oauth_issuer=current_oauth_config.issuer,
        ) as app,
        AbPage(onMount=[hydrate_oauth_action()]),
        Column(gap=5, css_class=PAGE_CLASS),
    ):
        render_environment_banners()
        render_breadcrumb_nav(
            current_page=f"{PLATFORM_ADMIN_EMOJI} {PLATFORM_ADMIN_LABEL}",
        )
        render_page_hero(
            title=f"{PLATFORM_ADMIN_EMOJI} {PLATFORM_ADMIN_LABEL}",
            description=(
                "Instance-admin operations against the Airbyte Cloud Config API."
            ),
            show_auth_controls=True,
            agents_callout=PLATFORM_ADMIN_AGENTS_CALLOUT,
        )
        with Grid(columns=3, gap=4):
            _render_data_worker_allocation_card()
            _render_more_tools_card()
        render_version_footer()
    return app


def register_platform_admin_app(mcp: FastMCP) -> None:
    """Register the Platform Admin app with the MCP server."""
    mcp.add_provider(platform_admin_app)
