"""Shared helpers for Connector Version Manager page and components."""

from __future__ import annotations

import json
import os
from dataclasses import asdict
from typing import Any

from airbyte.exceptions import PyAirbyteInputError
from airbyte_ops_mcp.connector_ops.rollouts._helpers import get_connector_rollout_config
from airbyte_ops_mcp.connector_ops.rollouts.constants import CustomerTier
from prefab_ui.actions import AppendState, SetState, ShowToast
from prefab_ui.components import ComboboxOption, SelectOption
from prefab_ui.rx import ERROR, RESULT

from airbyte_ops_webapp.auth.mock_session import mock_oauth_is_authenticated
from airbyte_ops_webapp.models import ConnectorOption, ScopeType
from airbyte_ops_webapp.services.connector_version_manager.adapter import (
    OpsMcpAdapter,
    _cloud_scope_url,
    _fmt_date,
)
from airbyte_ops_webapp.services.connector_version_manager.demo_mode import (
    MockPinningAdapter,
)
from airbyte_ops_webapp.state import (
    AIRBYTE_BEARER_TOKEN_ENV_VAR,
    AIRBYTE_CONFIG_API_ROOT_ENV_VAR,
    mock_only_enabled,
)

DEFAULT_ADMIN_USER_EMAIL = "devin-local@example.com"
DEFAULT_ADMIN_USER_ID = "00000000-0000-0000-0000-000000000000"
CONTEXT_ERROR = "Connector context failed to load."
APPLY_ERROR = "Apply change failed. No connector version override was applied."
SCOPE_PLACEHOLDER_SUFFIX = "_example"

# Canonical empty-state dicts for rollout and pin selection.
# Used in initial state, success handlers, and context resets.
EMPTY_ROLLOUT_STATE: dict[str, str] = {
    "rollout_id": "",
    "connector_id": "",
    "connector_name": "",
    "connector_type": "source",
    "docker_repository": "",
    "state": "",
    "rc_docker_image_tag": "",
    "initial_docker_image_tag": "",
    "current_target_rollout_pct": "",
    "final_target_rollout_pct": "",
    "created_at": "",
    "updated_at": "",
}
EMPTY_PIN_STATE: dict[str, str] = {
    "scope_type": "",
    "scope_id": "",
    "scope_url": "",
    "origin_type": "",
    "origin_name": "",
    "description": "",
    "created_at": "",
    "created_at_display": "",
    "expires_at": "",
    "expires_at_display": "",
    "reference_url": "",
    "scope_name": "",
}


# ---------------------------------------------------------------------------
# Adapter construction
# ---------------------------------------------------------------------------


def auth_available(bearer_token_override: str | None = None) -> bool:
    if mock_only_enabled():
        return mock_oauth_is_authenticated()
    if os.getenv(AIRBYTE_BEARER_TOKEN_ENV_VAR):
        return True
    return bool(bearer_token_override)


def is_scope_placeholder(value: str) -> bool:
    normalized = value.strip()
    return bool(normalized and normalized.endswith(SCOPE_PLACEHOLDER_SUFFIX))


def scope_context_available(
    adapter: OpsMcpAdapter,
    scope_type: ScopeType,
    scope_id: str,
    actor_workspace_id: str,
) -> bool:
    if isinstance(adapter, MockPinningAdapter):
        return True
    if not scope_id.strip() or is_scope_placeholder(scope_id):
        return False
    if scope_type == "actor":
        return bool(actor_workspace_id.strip()) and not is_scope_placeholder(
            actor_workspace_id
        )
    return True


def get_adapter(bearer_token_override: str | None = None) -> OpsMcpAdapter:
    if mock_only_enabled():
        return MockPinningAdapter()
    bearer_token = bearer_token_override or os.getenv(AIRBYTE_BEARER_TOKEN_ENV_VAR)
    return OpsMcpAdapter(
        bearer_token=bearer_token,
        config_api_root=os.getenv(AIRBYTE_CONFIG_API_ROOT_ENV_VAR)
        or "https://cloud.airbyte.com/api/v1",
    )


# ---------------------------------------------------------------------------
# Data formatting
# ---------------------------------------------------------------------------


def connector_rows(query: str) -> list[dict[str, str]]:
    return [asdict(connector) for connector in get_adapter().search_connectors(query)]


def connector_options(query: str) -> list[dict[str, str]]:
    return [
        {
            "label": f"{connector['name']} ({connector['latest_version']})",
            "value": connector["id"],
        }
        for connector in connector_rows(query)
    ]


def recent_release_options() -> list[dict[str, str]]:
    try:
        releases = get_adapter().list_recent_releases()
    except Exception:
        return [{"label": "Recent releases unavailable", "value": ""}]
    return [
        {
            "label": (
                f"{release.connector_name} {release.docker_image_tag}"
                f" — {release.last_published[:10]}"
            ),
            "value": f"{release.connector_id}|{release.docker_image_tag}",
        }
        for release in releases
    ]


def progressive_rollout_options() -> list[dict[str, str]]:
    try:
        rollouts = get_adapter().list_progressive_rollouts()
    except Exception:
        return [{"label": "Progressive rollouts unavailable", "value": ""}]
    return [
        {
            "label": (
                f"{rollout.connector_name} {rollout.rc_docker_image_tag}"
                f" — {rollout.state}"
                f" — target {rollout.current_target_rollout_pct or '0'}%"
            ),
            "value": f"{rollout.connector_id}|{rollout.rc_docker_image_tag}",
        }
        for rollout in rollouts
    ]


def _is_autopilot(connector_id: str, rc_version: str | None) -> bool:
    """Check the registry rolloutConfiguration to determine autopilot status."""
    try:
        config = get_connector_rollout_config(connector_id, rc_version=rc_version)
        return config.default_rollout_mode.value == "autopilot"
    except Exception:
        return False


def progressive_rollout_rows() -> list[dict[str, Any]]:
    """Build dashboard table rows for active progressive rollouts."""
    try:
        rollouts = get_adapter().list_progressive_rollouts()
    except Exception:
        return []
    rows = rows_from_dataclasses(rollouts)
    for row in rows:
        connector_id = row.get("connector_id", "")
        rc_tag = row.get("rc_docker_image_tag")
        row["autopilot_display"] = (
            "ON" if _is_autopilot(connector_id, rc_tag) else "OFF"
        )
        row["rc_pin_count_display"] = str(row.get("rc_pin_count", 0))
        row["tier_display"] = CustomerTier(row.get("tier", "TIER_2")).label
    return rows


def latest_version_rows() -> list[dict[str, Any]]:
    """Build rows for the Latest Versions tab (one row per connector, GA only)."""
    try:
        connectors = get_adapter().search_connectors("")
    except Exception:
        return []
    return [asdict(c) for c in connectors]


def recent_release_rows() -> list[dict[str, Any]]:
    """Build DataTable rows for the Recent Releases tab (last 30 days, max 50)."""
    try:
        releases = get_adapter().list_recent_releases(limit=50)
    except Exception:
        return []
    rows = rows_from_dataclasses(releases)
    for row in rows:
        row["connector_and_version"] = (
            f"{row.get('connector_name', '')} {row.get('docker_image_tag', '')}"
        )
    return rows


def pinned_version_rows() -> list[dict[str, Any]]:
    """Build rows for the Pinned Versions tab (cross-connector, versions with pins)."""
    try:
        raw = get_adapter().list_versions_with_pins()
    except Exception:
        return []
    rows: list[dict[str, Any]] = []
    for row in raw:
        docker_repo = row.get("docker_repository", "")
        canonical_name = (
            docker_repo.rsplit("/", 1)[-1]
            if docker_repo
            else row.get("connector_name", "")
        )
        rows.append(
            {
                **row,
                "connector_id": row.get("connector_definition_id", ""),
                "connector_name": canonical_name,
                "pin_count_display": str(row.get("pin_count", 0)),
                "actor_pins_display": str(row.get("actor_pins", 0)),
                "workspace_pins_display": str(row.get("workspace_pins", 0)),
                "org_pins_display": str(row.get("org_pins", 0)),
            }
        )
    return rows


def admin_user_options() -> list[dict[str, str]]:
    if mock_only_enabled():
        return [{"label": DEFAULT_ADMIN_USER_EMAIL, "value": DEFAULT_ADMIN_USER_EMAIL}]
    try:
        admin_users = list(get_adapter().list_instance_admin_users())
    except Exception:
        admin_users = []
    if not admin_users:
        admin_users = [
            {
                "email": DEFAULT_ADMIN_USER_EMAIL,
                "userId": DEFAULT_ADMIN_USER_ID,
            }
        ]
    return [
        {
            "label": f"{admin_user['email']} ({admin_user['userId']})",
            "value": admin_user["email"],
        }
        for admin_user in admin_users
    ]


def first_admin_user_email() -> str:
    options = admin_user_options()
    return options[0]["value"] if options else DEFAULT_ADMIN_USER_EMAIL


def _format_date_display(value: str) -> str:
    """Format an ISO datetime string to `yyyy-mm-dd (ddd)`."""
    return _fmt_date(value)


def rows_from_dataclasses(rows: Any) -> list[dict[str, Any]]:
    normalized_rows = []
    for row in rows:
        row_dict = asdict(row)
        if "last_published" in row_dict:
            row_dict["last_published_display"] = _format_date_display(
                str(row_dict["last_published"])
            )
        if "updated_at" in row_dict:
            row_dict["updated_at_display"] = _format_date_display(
                str(row_dict["updated_at"])
            )
        normalized_rows.append(row_dict)
    return normalized_rows


def json_text(value: Any) -> str:
    return json.dumps(value, indent=2, sort_keys=True)


def empty_connector() -> dict[str, str]:
    return {
        "id": "",
        "name": "",
        "connector_type": "source",
        "latest_version": "",
        "docker_repository": "",
    }


# ---------------------------------------------------------------------------
# UI option renderers
# ---------------------------------------------------------------------------


def render_select_options(options: list[dict[str, str]]) -> None:
    for option in options:
        SelectOption(label=option["label"], value=option["value"])


def render_combobox_options(options: list[dict[str, str]]) -> None:
    for option in options:
        ComboboxOption(option["label"], value=option["value"])


# ---------------------------------------------------------------------------
# State action builders
# ---------------------------------------------------------------------------


def start_tool_call(message: str) -> list[SetState]:
    return [
        SetState("is_loading", True),
        SetState("loading_message", message),
        SetState("tool_error", ""),
    ]


def finish_tool_call() -> list[SetState]:
    return [
        SetState("is_loading", False),
        SetState("loading_message", ""),
        SetState("tool_error", ""),
    ]


def fail_tool_call(message: Any) -> list[Any]:
    return [
        SetState("is_loading", False),
        SetState("loading_message", ""),
        SetState("tool_error", message),
        ShowToast("Tool call failed", description=message, variant="error"),
        AppendState("notifications", message),
        SetState("has_unviewed_notifications", True),
    ]


def rollout_action_success_actions() -> list[Any]:
    """Post-action feedback for successful rollout operations.

    Shows a success toast, appends to the notifications panel, marks
    notifications as unviewed, and clears the stale rollout selection.
    """
    return [
        *finish_tool_call(),
        SetState("rollout_action_result", RESULT.rollout_action_result),
        SetState("rollout_action_success", RESULT.rollout_action_success),
        ShowToast(
            "Rollout action completed",
            description=RESULT.rollout_action_result,
            variant="success",
        ),
        AppendState("notifications", RESULT.rollout_action_result),
        SetState("has_unviewed_notifications", True),
        SetState("selected_rollout", EMPTY_ROLLOUT_STATE),
        SetState("rollout_action", ""),
    ]


def context_success_actions() -> list[Any]:
    return [
        *finish_tool_call(),
        SetState("selected_connector", RESULT.connector),
        SetState("target_version", RESULT.connector.latest_version),
        SetState("versions", RESULT.versions),
        SetState("active_rollouts", RESULT.active_rollouts),
        SetState("current_state", RESULT.current_state),
        SetState("current_state_markdown", RESULT.current_state_markdown),
        SetState("ancestor_configs", RESULT.ancestor_configs),
        SetState("descendant_configs", RESULT.descendant_configs),
        SetState("resolved_context_label", RESULT.resolved_context_label),
        SetState("context_guid", RESULT.context_guid),
        SetState("scope_type", RESULT.scope_type),
        SetState("scope_id", RESULT.scope_id),
        SetState("actor_workspace_id", RESULT.actor_workspace_id),
        SetState("context_error", RESULT.context_error),
        SetState("rollout_error", RESULT.rollout_error),
        SetState("selected_rollout", EMPTY_ROLLOUT_STATE),
        SetState("rollout_action", ""),
        SetState("rollout_action_result", ""),
        SetState("rollout_action_success", False),
        SetState("rollout_modal_open", False),
    ]


def context_error_toast_actions() -> list[Any]:
    """Toast + bell notification for context errors.

    Only used by the explicit "Refresh context" button, not on automatic
    connector selection, so users aren't spammed with toasts on page load.
    """
    return [
        ShowToast(
            RESULT.context_error,
            variant="warning",
            duration=6000,
        ),
        AppendState("notifications", RESULT.context_error),
        SetState("has_unviewed_notifications", True),
    ]


def fail_context_actions() -> list[Any]:
    return [
        SetState("context_loading", False),
        *fail_tool_call(ERROR),
        SetState("context_error", ERROR),
        AppendState("notifications", ERROR),
        SetState("has_unviewed_notifications", True),
    ]


# ---------------------------------------------------------------------------
# Tool-layer helpers
# ---------------------------------------------------------------------------


def connector_context_placeholder(message: str) -> dict[str, Any]:
    current_state = {"message": message}
    return {
        "connector": empty_connector(),
        "versions": [],
        "active_rollouts": [],
        "current_state": current_state,
        "current_state_markdown": json_text(current_state),
        "ancestor_configs": [],
        "descendant_configs": [],
        "resolved_context_label": "",
        "context_guid": "",
        "context_error": message,
        "rollout_error": "",
        "scope_type": "workspace",
        "scope_id": "",
        "actor_workspace_id": "",
    }


def fallback_current_state(
    connector: ConnectorOption,
    versions: list[dict[str, Any]],
) -> dict[str, Any]:
    latest_version = connector.latest_version
    return {
        "connector_id": connector.id,
        "connector_name": connector.name,
        "connector_type": connector.connector_type,
        "latest_version": latest_version,
        "active_version": latest_version,
        "is_version_pinned": False,
        "active_scope": "",
        "active_scope_id": "",
        "ancestor_configurations": [],
        "descendant_configurations": [],
    }


def context_error_message(error: Exception) -> str:
    message = str(error)
    if "401" in message or "Unauthorized" in message:
        return (
            "Airbyte Cloud rejected the scoped-configuration request. "
            "Sign out and back in with Airbyte."
        )
    return "Scoped configuration context could not be loaded."


def scope_context_needed_message() -> str:
    return (
        "Enter a Context GUID in Connector pinning tools and refresh to load "
        "scoped pin context."
    )


def version_rows_or_empty(
    adapter: OpsMcpAdapter,
    connector: ConnectorOption,
) -> tuple[list[dict[str, Any]], str]:
    try:
        return rows_from_dataclasses(adapter.list_versions(connector.id)), ""
    except PyAirbyteInputError as error:
        return [], context_error_message(error)


def rollout_rows_or_empty(
    adapter: OpsMcpAdapter,
    connector: ConnectorOption,
) -> tuple[list[dict[str, Any]], str]:
    try:
        rows = rows_from_dataclasses(adapter.list_active_rollouts(connector.id))
    except Exception:
        return [], "Progressive rollout status could not be loaded."
    for row in rows:
        connector_id = row.get("connector_id", "")
        rc_tag = row.get("rc_docker_image_tag")
        row["autopilot_display"] = (
            "ON" if _is_autopilot(connector_id, rc_tag) else "OFF"
        )
        row["rc_pin_count_display"] = str(row.get("rc_pin_count", 0))
    return rows, ""


def target_ids(
    *,
    adapter: OpsMcpAdapter,
    scope_type: ScopeType,
    scope_id: str,
    actor_workspace_id: str,
) -> tuple[str, str | None, str | None]:
    if scope_type == "organization":
        return scope_id, None, None
    if scope_type == "actor":
        organization_id = (
            adapter.resolve_organization_id("workspace", actor_workspace_id)
            if actor_workspace_id
            else ""
        )
        return organization_id, actor_workspace_id or None, scope_id
    return adapter.resolve_organization_id("workspace", scope_id), scope_id, None


def cloud_scope_url(
    *,
    scope_type: ScopeType,
    scope_id: str,
    workspace_id: str = "",
    actor_type: str = "",
) -> str:
    """Build an Airbyte Cloud URL for viewing the target scope."""
    return _cloud_scope_url(
        scope_type=scope_type,
        scope_id=scope_id,
        workspace_id=workspace_id,
        actor_type=actor_type,
    )
