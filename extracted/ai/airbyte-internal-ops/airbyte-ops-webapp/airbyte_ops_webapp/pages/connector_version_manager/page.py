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
    Grid,
)
from prefab_ui.components.control_flow import If
from prefab_ui.rx import STATE

from airbyte_ops_webapp.app_shell import build_ops_app
from airbyte_ops_webapp.auth.google_oauth import hydrate_google_oauth_action
from airbyte_ops_webapp.auth.oauth import hydrate_oauth_action, oauth_config
from airbyte_ops_webapp.pages.connector_version_manager._helpers import (
    EMPTY_PIN_STATE,
    EMPTY_ROLLOUT_STATE,
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
)
from airbyte_ops_webapp.pages.shared_components.org_lookup_modal import (
    org_lookup_modal_state,
)
from airbyte_ops_webapp.state import (
    mock_only_enabled,
    preview_deploy_enabled,
    preview_pr_number,
    preview_pr_url,
)
from airbyte_ops_webapp.theme import (
    PAGE_CLASS,
    _page_style,
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
    )

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
        oauth_issuer=str(current_oauth_config["issuer"]),
    ) as app:
        with Div(
            style=_page_style(),
            onMount=[hydrate_oauth_action(), hydrate_google_oauth_action()],
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
                )
                render_connector_selector(state)

                with If(STATE.selected_connector.id):
                    with Grid(columns=[1, 2], gap=4):
                        render_rollout_status_section()
                        render_pin_detail()
                    render_pin_modal(state)

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
    current_oauth_config: dict[str, object],
) -> dict[str, object]:
    return {
        **org_lookup_modal_state(),
        "accepts_default_connector": True,
        "default_connector_from_args": default_connector_from_args,
        "query": connector_query,
        "connectors": connectors,
        "connector_options": connector_options(""),
        "latest_version_rows": latest_version_rows(),
        "recent_release_rows": [],
        "recent_release_value": "",
        "recent_release_options": [],
        "progressive_rollout_value": "",
        "progressive_rollout_options": [],
        "progressive_rollout_rows": [],
        "pinned_version_rows": [],
        "pin_origin_filter": "all",
        "recent_release_rows_loaded": False,
        "progressive_rollout_rows_loaded": False,
        "pinned_version_rows_loaded": False,
        "selector_tab": "active-rollouts",
        "selected_connector_id": selected_connector["id"],
        "selected_connector": selected_connector,
        "scope_type": context["scope_type"],
        "scope_id": context["scope_id"],
        "context_guid": context["context_guid"],
        "resolved_context_label": context["resolved_context_label"],
        "scope_url": "",
        "actor_workspace_id": context["actor_workspace_id"],
        "action": "set",
        "target_version": selected_connector["latest_version"],
        "override_reason": "",
        "reference_url": "",
        "customer_tier_filter": "TIER_2",
        "auth_bearer_token": "",
        "versions": context["versions"],
        "active_rollouts": context["active_rollouts"],
        "rollout_summary": context.get("rollout_summary", EMPTY_ROLLOUT_SUMMARY),
        "current_state": context["current_state"],
        "current_state_markdown": context["current_state_markdown"],
        "ancestor_configs": context["ancestor_configs"],
        "descendant_configs": context["descendant_configs"],
        "context_error": "",
        "notifications": [],
        "has_unviewed_notifications": False,
        "rollout_error": context["rollout_error"],
        "preview_json": "",
        "preview_warnings": "",
        "apply_result_json": "",
        "apply_message": "",
        "apply_success": False,
        "is_loading": False,
        "loading_message": "",
        "tool_error": "",
        "is_mock_only": mock_only_enabled(),
        "is_preview_deploy": preview_deploy_enabled(),
        "preview_pr_number": preview_pr_number(),
        "preview_pr_url": preview_pr_url(),
        "oauth_config": current_oauth_config,
        "oauth_enabled": current_oauth_config["enabled"],
        "oauth_authenticated": False,
        "oauth_status": "",
        "oauth_user_email": "",
        "google_authenticated": False,
        "google_user_email": "",
        "google_access_token": "",
        "google_status": "",
        "pin_modal_open": False,
        "locate_pin_modal_open": False,
        # --- Rollout action state ---
        "rollout_modal_open": False,
        "rollout_action": "",
        "rollout_action_result": "",
        "rollout_action_success": False,
        "rollout_target_percentage": "",
        "selected_rollout": EMPTY_ROLLOUT_STATE,
        # --- Version pin detail state ---
        "context_loading": False,
        "selected_version_tag": "",
        "selected_version_id": "",
        "selected_version_release_date": "",
        "latest_version_release_date": "",
        "version_pins": [],
        "version_pins_total": 0,
        "version_pins_offset": 0,
        "show_load_more_pins": False,
        "all_pins_loaded": True,
        "selected_pin_index": -1,
        "selected_pin_checks": [],
        "remove_pins_modal_open": False,
        "selected_pin": EMPTY_PIN_STATE,
        "resolved_pin_scope_name": "",
        "resolved_pin_scope_url": "",
        "resolved_pin_workspace_name": "",
        "resolved_pin_workspace_url": "",
        "resolved_pin_org_name": "",
        "resolved_pin_org_url": "",
    }


def register_connector_version_manager_app(mcp: FastMCP) -> None:
    """Register the connector version manager app with the MCP server."""
    mcp.add_provider(connector_version_manager_app)
