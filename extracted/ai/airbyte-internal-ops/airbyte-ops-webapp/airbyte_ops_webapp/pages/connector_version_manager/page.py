"""Connector Version Manager page.

Orchestrates the top-level layout. Each section is rendered by a dedicated
component module to keep the page definition readable and each component
individually maintainable.
"""

# ruff: noqa: SIM117

from __future__ import annotations

from dataclasses import asdict

from fastmcp import FastMCP
from prefab_ui.app import PrefabApp
from prefab_ui.components import (
    Column,
    Div,
    Row,
)
from prefab_ui.components.control_flow import If
from prefab_ui.rx import STATE

from airbyte_ops_webapp.app_shell import build_ops_app
from airbyte_ops_webapp.auth.oauth import hydrate_oauth_action, oauth_config
from airbyte_ops_webapp.pages.connector_version_manager._helpers import (
    EMPTY_ROLLOUT_SUMMARY,
    connector_options,
    connector_rows,
    empty_connector,
    get_adapter,
    latest_version_rows,
)
from airbyte_ops_webapp.pages.connector_version_manager._mcp_tools import (
    connector_version_manager_app,
    load_connector_context,
)
from airbyte_ops_webapp.pages.connector_version_manager._state import (
    ConnectorVersionManagerPageState,
)
from airbyte_ops_webapp.pages.connector_version_manager.agents import (
    CONNECTOR_VERSION_MANAGER_AGENTS_CALLOUT,
)
from airbyte_ops_webapp.pages.connector_version_manager.connector_overview import (
    render_rollout_status_section,
)
from airbyte_ops_webapp.pages.connector_version_manager.connector_selector import (
    render_connector_selector,
)
from airbyte_ops_webapp.pages.connector_version_manager.defaults import (
    CONNECTOR_VERSION_MANAGER_EMOJI,
    CONNECTOR_VERSION_MANAGER_TOOL_NAME,
    default_connector_query,
)
from airbyte_ops_webapp.pages.connector_version_manager.pin_modal import (
    render_pin_modal,
)
from airbyte_ops_webapp.pages.connector_version_manager.version_list import (
    render_pin_detail,
)
from airbyte_ops_webapp.pages.shared_components.layout import (
    render_breadcrumb_nav,
    render_environment_banners,
    render_page_hero,
    render_version_footer,
)
from airbyte_ops_webapp.state import (
    OAuthConfigState,
    mock_only_enabled,
)
from airbyte_ops_webapp.theme import (
    PAGE_CLASS,
    AbPage,
)

# ---------------------------------------------------------------------------
# UI definition
# ---------------------------------------------------------------------------


@connector_version_manager_app.ui(
    name=CONNECTOR_VERSION_MANAGER_TOOL_NAME,
    title="Connector Version Manager",
    description="Open the Airbyte Connector Version Manager app.",
)
def connector_version_manager(
    query: str = "",
    connector_name: str = "",
    connector: str = "",
    connector_id: str | None = None,
    scope_type: str = "workspace",
    scope_id: str = "",
    actor_workspace_id: str = "",
) -> PrefabApp:
    """Open the connector version manager."""
    adapter = get_adapter()
    current_oauth_config = oauth_config()
    initial_scope_id = scope_id or ("workspace_example" if mock_only_enabled() else "")
    connector_query = default_connector_query(
        query=query,
        connector_name=connector_name,
        connector=connector,
    )
    connectors = connector_rows(connector_query)
    default_connector_from_args = bool(
        query.strip()
        or connector_name.strip()
        or connector.strip()
        or (connector_id or "").strip()
    )
    selected_connector_id = connector_id or (
        connectors[0]["id"] if default_connector_from_args and connectors else ""
    )
    selected_connector = empty_connector()
    if selected_connector_id:
        try:
            selected_connector = asdict(adapter.get_connector(selected_connector_id))
        except ValueError:
            selected_connector = empty_connector()
    context = load_connector_context(
        selected_connector["id"],
        scope_type,
        initial_scope_id,
        actor_workspace_id,
        context_guid=initial_scope_id,
    ).model_dump(mode="json")

    state = _build_initial_state(
        connectors=connectors,
        selected_connector=selected_connector,
        context=context,
        connector_query=connector_query,
        default_connector_from_args=default_connector_from_args,
        current_oauth_config=current_oauth_config,
    )

    with build_ops_app(
        title="Connector Version Manager",
        state=state,
        oauth_issuer=current_oauth_config.issuer,
    ) as app:
        with AbPage(
            onMount=[hydrate_oauth_action()],
        ):
            with Column(gap=5, css_class=PAGE_CLASS):
                render_environment_banners()
                render_breadcrumb_nav(
                    current_page=f"{CONNECTOR_VERSION_MANAGER_EMOJI} Connector Version Manager",
                )
                render_page_hero(
                    title=f"{CONNECTOR_VERSION_MANAGER_EMOJI} Connector Version Manager",
                    description=(
                        "Review connector state, manage scoped overrides, "
                        "and apply production pin changes."
                    ),
                    show_auth_controls=True,
                    agents_callout=CONNECTOR_VERSION_MANAGER_AGENTS_CALLOUT,
                )
                render_connector_selector(state)

                with If(STATE.selected_connector.id.__or__(STATE.context_loading)):
                    # Responsive two-panel layout: the panels sit side by side
                    # when the tab is wide enough and stack when it is not.
                    # Widths flow from content via flex-grow + min-width rather
                    # than a fixed column ratio.
                    rollout_detail_condition = STATE.active_rollouts.length().__and__(
                        STATE.rollout_summary.rc_version.__eq__(
                            STATE.selected_version_tag
                        )
                    )
                    with Row(gap=4, align="start", css_class="flex-wrap"):
                        with Div(
                            css_class=rollout_detail_condition.then(
                                "min-w-[min(35rem,calc(100vw-6rem))] grow-[3] "
                                "basis-[min(35rem,calc(100vw-6rem))] "
                                "max-w-[36rem] shrink-0",
                                "min-w-[18rem] grow basis-[22rem] max-w-[34rem]",
                            )
                        ):
                            render_rollout_status_section(css_class="w-full")
                        with Div(
                            css_class=[
                                "min-w-[24rem]",
                                rollout_detail_condition.then(
                                    STATE.version_pins_total.__gt__(0).then(
                                        "basis-0 grow-[4]", "basis-0 grow"
                                    ),
                                    "basis-[30rem] grow-[2]",
                                ),
                            ]
                        ):
                            render_pin_detail(css_class="w-full")
                    render_pin_modal(state)
                render_version_footer()

    return app


# ---------------------------------------------------------------------------
# State initialization
# ---------------------------------------------------------------------------


def _build_initial_state(
    *,
    connectors: list[dict[str, str]],
    selected_connector: dict[str, str],
    context: dict[str, object],
    connector_query: str,
    default_connector_from_args: bool,
    current_oauth_config: OAuthConfigState,
) -> dict[str, object]:
    """Build the page's initial Prefab state through its typed model.

    `ConnectorVersionManagerPageState` supplies the typed defaults for every
    key (see `_state`); the overrides below inject the values resolved at page
    build (the connector search results, the selected connector, and the loaded
    connector context) over those defaults. Building through the model keeps the
    initial-state keys in lockstep with the page's `SetState` keys — the
    `tests/test_page_state.py` guardrail fails the build if they drift.
    """
    base = ConnectorVersionManagerPageState.from_env(
        oauth_config=current_oauth_config,
        default_connector_from_args=default_connector_from_args,
    ).to_prefab_state()
    return {
        **base,
        "query": connector_query,
        "connectors": connectors,
        "connector_options": connector_options(""),
        "latest_version_rows": latest_version_rows(),
        "selected_connector_id": selected_connector["id"],
        "selected_connector": selected_connector,
        "scope_type": context["scope_type"],
        "scope_id": context["scope_id"],
        "context_guid": context["context_guid"],
        "resolved_context_label": context["resolved_context_label"],
        "actor_workspace_id": context["actor_workspace_id"],
        "target_version": selected_connector["latest_version"],
        "versions": context["versions"],
        "active_rollouts": context["active_rollouts"],
        "rollout_summary": context.get("rollout_summary", EMPTY_ROLLOUT_SUMMARY),
        "current_state": context["current_state"],
        "current_state_markdown": context["current_state_markdown"],
        "ancestor_configs": context["ancestor_configs"],
        "descendant_configs": context["descendant_configs"],
        "rollout_error": context["rollout_error"],
    }


def register_connector_version_manager_app(mcp: FastMCP) -> None:
    """Register the connector version manager app with the MCP server."""
    mcp.add_provider(connector_version_manager_app)
