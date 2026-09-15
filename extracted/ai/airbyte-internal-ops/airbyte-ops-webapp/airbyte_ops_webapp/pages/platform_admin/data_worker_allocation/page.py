"""Data Worker Allocation page."""

from __future__ import annotations

from fastmcp import FastMCP
from prefab_ui.app import PrefabApp
from prefab_ui.components import CardContent, Column, Grid, Markdown, Text
from prefab_ui.components.control_flow import If
from prefab_ui.rx import STATE

from airbyte_ops_webapp.app_shell import build_ops_app
from airbyte_ops_webapp.auth.oauth import hydrate_oauth_action, oauth_config
from airbyte_ops_webapp.pages.platform_admin.data_worker_allocation._mcp_tools import (
    data_worker_allocation_app,
)
from airbyte_ops_webapp.pages.platform_admin.data_worker_allocation._state import (
    DataWorkerAllocationPageState,
)
from airbyte_ops_webapp.pages.platform_admin.data_worker_allocation.agents import (
    DATA_WORKER_ALLOCATION_AGENTS_CALLOUT,
)
from airbyte_ops_webapp.pages.platform_admin.data_worker_allocation.allocation_actions import (
    render_allocation_actions,
)
from airbyte_ops_webapp.pages.platform_admin.data_worker_allocation.allocation_overview import (
    render_allocation_overview,
)
from airbyte_ops_webapp.pages.platform_admin.data_worker_allocation.defaults import (
    DATA_WORKER_ALLOCATION_EMOJI,
    DATA_WORKER_ALLOCATION_TOOL_NAME,
)
from airbyte_ops_webapp.pages.platform_admin.data_worker_allocation.org_lookup import (
    render_org_lookup,
)
from airbyte_ops_webapp.pages.platform_admin.data_worker_allocation.result_modal import (
    render_result_modal,
)
from airbyte_ops_webapp.pages.platform_admin.defaults import (
    PLATFORM_ADMIN_EMOJI,
    PLATFORM_ADMIN_PATH,
)
from airbyte_ops_webapp.pages.shared_components.layout import (
    render_breadcrumb_nav,
    render_environment_banners,
    render_page_hero,
    render_version_footer,
)
from airbyte_ops_webapp.theme import PAGE_CLASS, AbErrorCard, AbPage, AbPreviewCard


@data_worker_allocation_app.ui(
    name=DATA_WORKER_ALLOCATION_TOOL_NAME,
    title="Data Worker Allocation",
    description="Manage organization Data Worker allocation capacity.",
)
def data_worker_allocation() -> PrefabApp:
    """Open the Data Worker Allocation page."""
    current_oauth_config = oauth_config()
    state = DataWorkerAllocationPageState.from_env(
        oauth_config=current_oauth_config
    ).to_prefab_state()
    with (
        build_ops_app(
            title="Data Worker Allocation",
            state=state,
            oauth_issuer=current_oauth_config.issuer,
        ) as app,
        AbPage(onMount=[hydrate_oauth_action()]),
        Column(gap=5, css_class=PAGE_CLASS),
    ):
        render_environment_banners()
        render_breadcrumb_nav(
            current_page=f"{DATA_WORKER_ALLOCATION_EMOJI} Data Worker Allocation",
            parent=(
                f"{PLATFORM_ADMIN_EMOJI} Platform Admin",
                PLATFORM_ADMIN_PATH,
            ),
        )
        render_page_hero(
            title=f"{DATA_WORKER_ALLOCATION_EMOJI} Data Worker Allocation",
            description=(
                "Review, add, and remove organization Data Worker capacity by "
                "dataplane group."
            ),
            show_auth_controls=True,
            agents_callout=DATA_WORKER_ALLOCATION_AGENTS_CALLOUT,
        )
        with If(STATE.loading_message), AbPreviewCard(), CardContent(), Column(gap=1):
            Markdown("**Loading**")
            Text(STATE.loading_message)
        with If(STATE.tool_error), AbErrorCard(), CardContent(), Column(gap=1):
            Markdown("**Tool call failed**")
            Text(STATE.tool_error)
        render_org_lookup()
        with If(STATE.org_loaded), Grid(columns=[3, 2], gap=4):
            render_allocation_overview()
            render_allocation_actions()
        render_result_modal()
        render_version_footer()
    return app


def register_data_worker_allocation_app(mcp: FastMCP) -> None:
    """Register the Data Worker Allocation app with the MCP server."""
    mcp.add_provider(data_worker_allocation_app)
