"""Tool definitions for the Connector Version Manager page."""

from __future__ import annotations

from dataclasses import asdict
from typing import Any

from airbyte.exceptions import PyAirbyteInputError
from fastmcp import FastMCPApp

from airbyte_ops_webapp.models import OverridePlan, ScopeType
from airbyte_ops_webapp.pages.connector_version_manager._helpers import (
    auth_available,
    connector_context_placeholder,
    context_error_message,
    fallback_current_state,
    get_adapter,
    json_text,
    rollout_rows_or_empty,
    rows_from_dataclasses,
    scope_context_available,
    scope_context_needed_message,
    target_ids,
    version_rows_or_empty,
)
from airbyte_ops_webapp.pages.shared_components.org_search import (
    search_organizations_and_workspaces,
)
from airbyte_ops_webapp.services.connector_version_manager.adapter import (
    OpsMcpAdapter,
    operation_result_to_json,
)
from airbyte_ops_webapp.services.connector_version_manager.demo_mode import (
    MockPinningAdapter,
)

connector_version_manager_app = FastMCPApp("Connector Version Manager")


def _override_plan(
    *,
    adapter: OpsMcpAdapter,
    connector_id: str,
    connector_name: str,
    connector_type: str,
    scope_type: ScopeType,
    scope_id: str,
    actor_workspace_id: str,
    action: str,
    version: str,
    override_reason: str,
    reference_url: str,
    approval_comment_url: str,
    user_email: str | None,
    customer_tier_filter: str,
    force: bool,
) -> OverridePlan:
    organization_id, workspace_id, actor_id = target_ids(
        adapter=adapter,
        scope_type=scope_type,
        scope_id=scope_id,
        actor_workspace_id=actor_workspace_id,
    )
    return OverridePlan(
        action=action,
        connector_id=connector_id,
        connector_name=connector_name,
        connector_type=connector_type,
        scope_type=scope_type,
        organization_id=organization_id,
        workspace_id=workspace_id or None,
        actor_id=actor_id or None,
        scope_id=scope_id,
        version=None if action == "unset" else version,
        override_reason=override_reason,
        override_reason_reference_url=reference_url,
        approval_comment_url=approval_comment_url,
        user_email=user_email,
        customer_tier_filter=customer_tier_filter,
        force=force,
    )


@connector_version_manager_app.tool()
def search_connectors(query: str = "") -> dict[str, Any]:
    """Search connector definitions by name, definition ID, or Docker repository."""
    from airbyte_ops_webapp.pages.connector_version_manager._helpers import (
        connector_options,
        connector_rows,
    )

    connectors = connector_rows(query)
    return {
        "connectors": connectors,
        "connector_options": connector_options(query),
        "selected_connector_id": connectors[0]["id"] if connectors else "",
    }


@connector_version_manager_app.tool()
def load_connector_context(
    connector_id: str,
    scope_type: ScopeType = "workspace",
    scope_id: str = "",
    actor_workspace_id: str = "",
    context_guid: str = "",
    auth_bearer_token: str = "",
) -> dict[str, Any]:
    """Load connector versions and scoped pin context."""
    if not connector_id:
        return connector_context_placeholder(
            "Search for and select a connector before loading scope context."
        )
    adapter = get_adapter(auth_bearer_token or None)
    try:
        connector = adapter.get_connector(connector_id)
    except ValueError:
        return connector_context_placeholder(f"Unknown connector ID: {connector_id}")
    active_rollouts, rollout_error = rollout_rows_or_empty(adapter, connector)
    if not auth_available(auth_bearer_token or None):
        versions, _version_error = version_rows_or_empty(adapter, connector)
        current_state = {
            "message": "Sign in with Airbyte to load scoped configuration context.",
        }
        return {
            "connector": asdict(connector),
            "versions": versions,
            "active_rollouts": active_rollouts,
            "current_state": current_state,
            "current_state_markdown": json_text(current_state),
            "ancestor_configs": [],
            "descendant_configs": [],
            "resolved_context_label": "",
            "context_guid": context_guid,
            "context_error": current_state["message"],
            "rollout_error": rollout_error,
            "scope_type": scope_type,
            "scope_id": scope_id,
            "actor_workspace_id": actor_workspace_id,
        }
    versions, version_error = version_rows_or_empty(adapter, connector)
    resolved_context_label = ""
    if context_guid.strip():
        try:
            resolution = adapter.resolve_context_guid(
                connector=connector,
                context_guid=context_guid,
            )
            scope_type = resolution.scope_type
            scope_id = resolution.scope_id
            actor_workspace_id = resolution.workspace_id or ""
            resolved_context_label = scope_type.title()
        except PyAirbyteInputError as error:
            current_state_dict = fallback_current_state(connector, versions)
            return {
                "connector": asdict(connector),
                "versions": versions,
                "active_rollouts": active_rollouts,
                "current_state": current_state_dict,
                "current_state_markdown": json_text(current_state_dict),
                "ancestor_configs": [],
                "descendant_configs": [],
                "resolved_context_label": "",
                "context_guid": context_guid,
                "context_error": str(error),
                "rollout_error": rollout_error,
                "scope_type": scope_type,
                "scope_id": scope_id,
                "actor_workspace_id": actor_workspace_id,
            }
    if not scope_context_available(adapter, scope_type, scope_id, actor_workspace_id):
        current_state_dict = fallback_current_state(connector, versions)
        return {
            "connector": asdict(connector),
            "versions": versions,
            "active_rollouts": active_rollouts,
            "current_state": current_state_dict,
            "current_state_markdown": json_text(current_state_dict),
            "ancestor_configs": [],
            "descendant_configs": [],
            "resolved_context_label": resolved_context_label,
            "context_guid": context_guid,
            "context_error": version_error or scope_context_needed_message(),
            "rollout_error": rollout_error,
            "scope_type": scope_type,
            "scope_id": scope_id,
            "actor_workspace_id": actor_workspace_id,
        }
    workspace_id = scope_id if scope_type == "workspace" else actor_workspace_id
    try:
        if isinstance(adapter, MockPinningAdapter):
            current_state = adapter.get_current_context(
                connector_id=connector.id,
                scope_type=scope_type,
                scope_id=scope_id,
            )
        else:
            current_state = adapter.get_current_context(
                connector_id=connector.id,
                scope_type=scope_type,
                scope_id=scope_id,
                workspace_id=workspace_id,
            )
    except PyAirbyteInputError as error:
        context_error = context_error_message(error)
        current_state_dict = fallback_current_state(connector, versions)
        return {
            "connector": asdict(connector),
            "versions": versions,
            "active_rollouts": active_rollouts,
            "current_state": current_state_dict,
            "current_state_markdown": json_text(current_state_dict),
            "ancestor_configs": [],
            "descendant_configs": [],
            "resolved_context_label": resolved_context_label,
            "context_guid": context_guid,
            "context_error": context_error,
            "rollout_error": rollout_error,
            "scope_type": scope_type,
            "scope_id": scope_id,
            "actor_workspace_id": actor_workspace_id,
        }
    return {
        "connector": asdict(connector),
        "versions": versions,
        "active_rollouts": active_rollouts,
        "current_state": asdict(current_state),
        "current_state_markdown": json_text(asdict(current_state)),
        "ancestor_configs": rows_from_dataclasses(
            current_state.ancestor_configurations
        ),
        "descendant_configs": rows_from_dataclasses(
            current_state.descendant_configurations
        ),
        "resolved_context_label": resolved_context_label,
        "context_guid": context_guid,
        "context_error": version_error,
        "rollout_error": rollout_error,
        "scope_type": scope_type,
        "scope_id": scope_id,
        "actor_workspace_id": actor_workspace_id,
    }


@connector_version_manager_app.tool()
def load_recent_release_context(
    release_value: str,
    scope_type: ScopeType = "workspace",
    scope_id: str = "",
    actor_workspace_id: str = "",
    context_guid: str = "",
    auth_bearer_token: str = "",
) -> dict[str, Any]:
    """Load connector context from a recent release combobox selection."""
    connector_id, _separator, version = release_value.partition("|")
    context = load_connector_context(
        connector_id=connector_id,
        scope_type=scope_type,
        scope_id=scope_id,
        actor_workspace_id=actor_workspace_id,
        context_guid=context_guid,
        auth_bearer_token=auth_bearer_token,
    )
    context["selected_connector_id"] = connector_id
    context["target_version"] = version
    return context


@connector_version_manager_app.tool()
def load_progressive_rollout_context(
    rollout_value: str,
    scope_type: ScopeType = "workspace",
    scope_id: str = "",
    actor_workspace_id: str = "",
    context_guid: str = "",
    auth_bearer_token: str = "",
) -> dict[str, Any]:
    """Load connector context from a progressive rollout selection."""
    connector_id, _separator, version = rollout_value.partition("|")
    context = load_connector_context(
        connector_id=connector_id,
        scope_type=scope_type,
        scope_id=scope_id,
        actor_workspace_id=actor_workspace_id,
        context_guid=context_guid,
        auth_bearer_token=auth_bearer_token,
    )
    context["selected_connector_id"] = connector_id
    context["target_version"] = version
    return context


@connector_version_manager_app.tool()
def load_version_pins(
    version_id: str,
    version_tag: str = "",
    auth_bearer_token: str = "",
    limit: int = 25,
    offset: int = 0,
) -> dict[str, Any]:
    """Load pins for a specific connector version."""
    adapter = get_adapter(auth_bearer_token or None)
    pins, total = adapter.list_version_pins(version_id, limit=limit, offset=offset)
    return {
        "version_pins": rows_from_dataclasses(pins),
        "version_pins_total": total,
        "version_pins_offset": offset + limit,
        "selected_version_id": version_id,
        "selected_version_tag": version_tag,
    }


@connector_version_manager_app.tool()
def apply_override(
    connector_id: str,
    connector_name: str,
    connector_type: str,
    scope_type: ScopeType,
    scope_id: str,
    action: str,
    version: str,
    override_reason: str,
    reference_url: str,
    approval_comment_url: str,
    user_email: str | None,
    auth_bearer_token: str = "",
    actor_workspace_id: str = "",
    customer_tier_filter: str = "TIER_2",
    force: bool = False,
) -> dict[str, Any]:
    """Apply a connector version override after user confirmation."""
    adapter = get_adapter(auth_bearer_token or None)
    result = adapter.apply_override(
        _override_plan(
            adapter=adapter,
            connector_id=connector_id,
            connector_name=connector_name,
            connector_type=connector_type,
            scope_type=scope_type,
            scope_id=scope_id,
            actor_workspace_id=actor_workspace_id,
            action=action,
            version=version,
            override_reason=override_reason,
            reference_url=reference_url,
            approval_comment_url=approval_comment_url,
            user_email=user_email,
            customer_tier_filter=customer_tier_filter,
            force=force,
        )
    )
    return {
        "apply_result_json": operation_result_to_json(result),
        "apply_message": result.message,
        "apply_success": result.success,
    }


@connector_version_manager_app.tool()
def search_orgs_workspaces(
    query: str = "",
) -> dict[str, Any]:
    """Search organizations and workspaces by name (case-insensitive substring)."""
    return search_organizations_and_workspaces(query=query)
