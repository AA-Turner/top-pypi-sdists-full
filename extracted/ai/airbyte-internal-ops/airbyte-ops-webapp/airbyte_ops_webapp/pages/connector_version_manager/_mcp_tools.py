"""Tool definitions for the Connector Version Manager page."""

from __future__ import annotations

import re
from dataclasses import asdict
from typing import Any

from airbyte.exceptions import PyAirbyteInputError
from airbyte_ops_mcp.cloud_admin import api_client as cloud_api
from fastmcp import FastMCPApp

from airbyte_ops_webapp.models import OverridePlan, ScopeType
from airbyte_ops_webapp.pages.connector_version_manager._helpers import (
    DEFAULT_ADMIN_USER_ID,
    auth_available,
    build_active_releases,
    cloud_scope_url,
    connector_context_placeholder,
    connector_options,
    connector_rows,
    context_error_message,
    fallback_current_state,
    get_adapter,
    json_text,
    pinned_version_rows,
    progressive_rollout_rows,
    recent_release_rows,
    rollout_rows_or_empty,
    rows_from_dataclasses,
    scope_context_available,
    scope_context_needed_message,
    target_ids,
    version_rows_or_empty,
    versions_with_pins_or_empty,
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

# Number of pins fetched per "Load More" click.
_PIN_BATCH_SIZE = 100


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


# ---------------------------------------------------------------------------
# Lazy tab-loading tools
# ---------------------------------------------------------------------------


@connector_version_manager_app.tool()
def load_recent_releases_tab() -> dict[str, Any]:
    """Load Recent Releases tab data on demand (lazy)."""
    return {"rows": recent_release_rows()}


@connector_version_manager_app.tool()
def load_active_rollouts_tab() -> dict[str, Any]:
    """Load Active Rollouts tab data on demand (lazy)."""
    return {"rows": progressive_rollout_rows()}


@connector_version_manager_app.tool()
def load_pinned_versions_tab() -> dict[str, Any]:
    """Load Pinned Versions tab data on demand (lazy)."""
    return {"rows": pinned_version_rows()}


# ---------------------------------------------------------------------------
# Connector search & context tools
# ---------------------------------------------------------------------------


@connector_version_manager_app.tool()
def search_connectors(query: str = "") -> dict[str, Any]:
    """Search connector definitions by name, definition ID, or Docker repository."""
    connectors = connector_rows(query)
    return {
        "connectors": connectors,
        "connector_options": connector_options(query),
        "selected_connector_id": connectors[0]["id"] if connectors else "",
    }


@connector_version_manager_app.tool()
def resolve_scope_guid(
    connector_id: str,
    context_guid: str,
    auth_bearer_token: str = "",
) -> dict[str, Any]:
    """Validate a GUID and resolve it to a scope type with friendly name."""
    uuid_pattern = re.compile(
        r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}"
        r"-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$"
    )
    normalized = context_guid.strip()
    if not normalized:
        return {
            "scope_type": "",
            "scope_id": "",
            "scope_name": "",
            "scope_url": "",
            "resolved_context_label": "",
            "context_error": "",
            "is_valid_uuid": False,
            "actor_workspace_id": "",
            "workspace_name": "",
            "workspace_url": "",
            "organization_name": "",
            "organization_url": "",
        }
    if not uuid_pattern.match(normalized):
        return {
            "scope_type": "",
            "scope_id": "",
            "scope_name": "",
            "scope_url": "",
            "resolved_context_label": "",
            "context_error": "Invalid UUID format.",
            "is_valid_uuid": False,
            "actor_workspace_id": "",
            "workspace_name": "",
            "workspace_url": "",
            "organization_name": "",
            "organization_url": "",
        }
    adapter = get_adapter(auth_bearer_token or None)
    try:
        connector = adapter.get_connector(connector_id)
    except ValueError:
        return {
            "scope_type": "",
            "scope_id": normalized,
            "scope_name": "",
            "scope_url": "",
            "resolved_context_label": "",
            "context_error": f"Unknown connector ID: {connector_id}",
            "is_valid_uuid": True,
            "actor_workspace_id": "",
            "workspace_name": "",
            "workspace_url": "",
            "organization_name": "",
            "organization_url": "",
        }
    try:
        resolution = adapter.resolve_context_guid(
            connector=connector,
            context_guid=normalized,
        )
    except PyAirbyteInputError as error:
        return {
            "scope_type": "",
            "scope_id": normalized,
            "scope_name": "",
            "scope_url": "",
            "resolved_context_label": "",
            "context_error": context_error_message(error),
            "is_valid_uuid": True,
            "actor_workspace_id": "",
            "workspace_name": "",
            "workspace_url": "",
            "organization_name": "",
            "organization_url": "",
        }
    scope_url = cloud_scope_url(
        scope_type=resolution.scope_type,
        scope_id=resolution.scope_id,
        workspace_id=resolution.workspace_id or "",
        actor_type=resolution.actor_type,
    )
    if resolution.scope_name:
        label = f'"{resolution.scope_name}" {resolution.scope_type.title()}'
    else:
        label = resolution.scope_type.title()
    workspace_url = ""
    if resolution.workspace_id and resolution.scope_type != "workspace":
        workspace_url = cloud_scope_url(
            scope_type="workspace",
            scope_id=resolution.workspace_id,
        )
    organization_url = ""
    if resolution.organization_id and resolution.scope_type != "organization":
        organization_url = cloud_scope_url(
            scope_type="organization",
            scope_id=resolution.organization_id,
        )
    return {
        "scope_type": resolution.scope_type,
        "scope_id": resolution.scope_id,
        "scope_name": resolution.scope_name,
        "scope_url": scope_url,
        "resolved_context_label": label,
        "context_error": "",
        "is_valid_uuid": True,
        "actor_workspace_id": resolution.workspace_id or "",
        "workspace_name": resolution.workspace_name,
        "workspace_url": workspace_url,
        "organization_name": resolution.organization_name,
        "organization_url": organization_url,
    }


def _add_description_display(pin_rows: list[dict[str, Any]], max_len: int = 40) -> None:
    """Add truncated `description_display` to each pin row in place."""
    for row in pin_rows:
        desc = row.get("description", "")
        row["description_display"] = (
            (desc[:max_len] + "\u2026") if len(desc) > max_len else desc
        )


def _build_context_result(
    *,
    connector: object,
    versions: list[dict[str, Any]],
    active_rollouts: list[dict[str, Any]],
    pin_enriched: list[dict[str, Any]],
    current_state: dict[str, Any],
    ancestor_configs: list[dict[str, Any]] | None = None,
    descendant_configs: list[dict[str, Any]] | None = None,
    resolved_context_label: str = "",
    context_guid: str = "",
    context_error: str = "",
    rollout_error: str = "",
    scope_type: ScopeType = "workspace",
    scope_id: str = "",
    actor_workspace_id: str = "",
) -> dict[str, Any]:
    """Assemble the standard context result dict."""
    return {
        "connector": asdict(connector)
        if not isinstance(connector, dict)
        else connector,
        "versions": versions,
        "active_releases": build_active_releases(
            versions, active_rollouts, pin_enriched
        ),
        "active_rollouts": active_rollouts,
        "current_state": current_state,
        "current_state_markdown": json_text(current_state),
        "ancestor_configs": ancestor_configs or [],
        "descendant_configs": descendant_configs or [],
        "resolved_context_label": resolved_context_label,
        "context_guid": context_guid,
        "context_error": context_error,
        "rollout_error": rollout_error,
        "scope_type": scope_type,
        "scope_id": scope_id,
        "actor_workspace_id": actor_workspace_id,
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
    pin_enriched = versions_with_pins_or_empty(adapter, connector)
    ctx_kwargs: dict[str, Any] = {
        "connector": connector,
        "active_rollouts": active_rollouts,
        "pin_enriched": pin_enriched,
        "rollout_error": rollout_error,
        "context_guid": context_guid,
        "scope_type": scope_type,
        "scope_id": scope_id,
        "actor_workspace_id": actor_workspace_id,
    }
    if not auth_available(auth_bearer_token or None):
        versions, _version_error = version_rows_or_empty(adapter, connector)
        sign_in_msg = "Sign in with Airbyte to load scoped configuration context."
        return _build_context_result(
            **ctx_kwargs,
            versions=versions,
            current_state={"message": sign_in_msg},
            context_error=sign_in_msg,
        )
    versions, version_error = version_rows_or_empty(adapter, connector)
    ctx_kwargs["versions"] = versions
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
            ctx_kwargs.update(
                scope_type=scope_type,
                scope_id=scope_id,
                actor_workspace_id=actor_workspace_id,
            )
            if resolution.scope_name:
                resolved_context_label = (
                    f'"{resolution.scope_name}" {scope_type.title()}'
                )
            else:
                resolved_context_label = scope_type.title()
        except PyAirbyteInputError as error:
            return _build_context_result(
                **ctx_kwargs,
                current_state=fallback_current_state(connector, versions),
                context_error=context_error_message(error),
            )
    if not scope_context_available(adapter, scope_type, scope_id, actor_workspace_id):
        return _build_context_result(
            **ctx_kwargs,
            current_state=fallback_current_state(connector, versions),
            resolved_context_label=resolved_context_label,
            context_error=version_error or scope_context_needed_message(),
        )
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
        return _build_context_result(
            **ctx_kwargs,
            current_state=fallback_current_state(connector, versions),
            resolved_context_label=resolved_context_label,
            context_error=context_error_message(error),
        )
    return _build_context_result(
        **ctx_kwargs,
        current_state=asdict(current_state),
        ancestor_configs=rows_from_dataclasses(current_state.ancestor_configurations),
        descendant_configs=rows_from_dataclasses(
            current_state.descendant_configurations
        ),
        resolved_context_label=resolved_context_label,
        context_error=version_error,
    )


def _load_context_from_compound_value(
    compound_value: str,
    scope_type: ScopeType = "workspace",
    scope_id: str = "",
    actor_workspace_id: str = "",
    context_guid: str = "",
    auth_bearer_token: str = "",
) -> dict[str, Any]:
    """Shared helper: split a `connector_id|version` value, load context."""
    connector_id, _separator, version = compound_value.partition("|")
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
def load_recent_release_context(
    release_value: str,
    scope_type: ScopeType = "workspace",
    scope_id: str = "",
    actor_workspace_id: str = "",
    context_guid: str = "",
    auth_bearer_token: str = "",
) -> dict[str, Any]:
    """Load connector context from a recent release combobox selection."""
    return _load_context_from_compound_value(
        release_value,
        scope_type,
        scope_id,
        actor_workspace_id,
        context_guid,
        auth_bearer_token,
    )


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
    return _load_context_from_compound_value(
        rollout_value,
        scope_type,
        scope_id,
        actor_workspace_id,
        context_guid,
        auth_bearer_token,
    )


@connector_version_manager_app.tool()
def load_connector_version_context(
    connector_id: str,
    version_tag: str = "",
    scope_type: ScopeType = "workspace",
    scope_id: str = "",
    actor_workspace_id: str = "",
    context_guid: str = "",
    auth_bearer_token: str = "",
) -> dict[str, Any]:
    """Load connector context and auto-resolve pins for a specific version.

    Combines `load_connector_context` + `load_version_pins` into a single
    call so that clicking a row in the version selector tabs populates both
    the rollout status and pin detail sections in one round-trip.
    """
    context = load_connector_context(
        connector_id=connector_id,
        scope_type=scope_type,
        scope_id=scope_id,
        actor_workspace_id=actor_workspace_id,
        context_guid=context_guid,
        auth_bearer_token=auth_bearer_token,
    )
    context["selected_connector_id"] = connector_id
    context["target_version"] = version_tag or context["connector"].get(
        "latest_version", ""
    )

    # Resolve version_id from the versions list
    resolved_version_id = ""
    for v in context.get("versions", []):
        if v.get("docker_image_tag") == version_tag:
            resolved_version_id = v.get("version_id", "")
            break

    adapter = get_adapter(auth_bearer_token or None)

    # Load pins if we resolved a version_id
    if resolved_version_id:
        pins, total = adapter.list_version_pins(
            resolved_version_id,
            limit=_PIN_BATCH_SIZE,
        )
        pin_rows = rows_from_dataclasses(pins)
        _add_description_display(pin_rows)
        context["version_pins"] = pin_rows
        context["version_pins_total"] = total
        context["version_pins_offset"] = _PIN_BATCH_SIZE
        context["show_load_more_pins"] = total > _PIN_BATCH_SIZE
        context["all_pins_loaded"] = len(pin_rows) >= total
        context["selected_version_id"] = resolved_version_id
        context["selected_version_tag"] = version_tag
    else:
        context["version_pins"] = []
        context["version_pins_total"] = 0
        context["version_pins_offset"] = 0
        context["show_load_more_pins"] = False
        context["all_pins_loaded"] = True
        context["selected_version_id"] = ""
        context["selected_version_tag"] = version_tag

    return context


@connector_version_manager_app.tool()
def load_version_pins(
    version_id: str,
    version_tag: str = "",
    auth_bearer_token: str = "",
    offset: int = 0,
) -> dict[str, Any]:
    """Load more pins for a connector version (accumulating).

    Fetches all pins from row 0 through `offset + _PIN_BATCH_SIZE` so the
    client can replace its list with the full accumulated result.
    """
    new_end = offset + _PIN_BATCH_SIZE
    adapter = get_adapter(auth_bearer_token or None)
    pins, total = adapter.list_version_pins(version_id, limit=new_end, offset=0)
    pin_rows = rows_from_dataclasses(pins)
    _add_description_display(pin_rows)
    return {
        "version_pins": pin_rows,
        "version_pins_total": total,
        "version_pins_offset": new_end,
        "show_load_more_pins": total > _PIN_BATCH_SIZE,
        "all_pins_loaded": len(pin_rows) >= total,
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
def remove_selected_pins(
    selected_pins: list[dict[str, str]],
    connector_id: str,
    connector_name: str,
    connector_type: str,
    version_id: str = "",
    version_tag: str = "",
    auth_bearer_token: str = "",
    override_reason: str = "Bulk pin removal via Connector Version Manager",
    reference_url: str = "",
    approval_comment_url: str = "",
    user_email: str | None = None,
    customer_tier_filter: str = "TIER_2",
) -> dict[str, Any]:
    """Remove (unset) version overrides for each selected pin.

    Iterates over `selected_pins` and calls `apply_override` with
    `action="unset"` for each one. For actor-scope pins, resolves
    the actor's `workspace_id` via the Config API before unsetting.
    """
    adapter = get_adapter(auth_bearer_token or None)
    removed = 0
    errors: list[str] = []

    for pin in selected_pins:
        pin_scope_type: ScopeType = pin.get("scope_type", "workspace")
        pin_scope_id = pin.get("scope_id", "")
        if not pin_scope_id:
            errors.append("Skipped pin with empty scope_id.")
            continue

        actor_workspace_id = ""
        if pin_scope_type == "actor":
            actor_workspace_id = _resolve_actor_workspace(
                adapter=adapter,
                connector_id=connector_id,
                connector_type=connector_type,
                actor_id=pin_scope_id,
            )
            if not actor_workspace_id:
                errors.append(f"Could not resolve workspace for actor {pin_scope_id}.")
                continue

        try:
            result = adapter.apply_override(
                _override_plan(
                    adapter=adapter,
                    connector_id=connector_id,
                    connector_name=connector_name,
                    connector_type=connector_type,
                    scope_type=pin_scope_type,
                    scope_id=pin_scope_id,
                    actor_workspace_id=actor_workspace_id,
                    action="unset",
                    version="",
                    override_reason=override_reason,
                    reference_url=reference_url,
                    approval_comment_url=approval_comment_url,
                    user_email=user_email,
                    customer_tier_filter=customer_tier_filter,
                    force=False,
                )
            )
            if result.success:
                removed += 1
            else:
                errors.append(f"{pin_scope_type}:{pin_scope_id} — {result.message}")
        except PyAirbyteInputError as exc:
            errors.append(f"{pin_scope_type}:{pin_scope_id} — {exc}")

    # Reload pins after removal so UI reflects current state
    pin_rows: list[dict[str, Any]] = []
    total = 0
    if version_id:
        pins_list, total = adapter.list_version_pins(
            version_id,
            limit=_PIN_BATCH_SIZE,
        )
        pin_rows = rows_from_dataclasses(pins_list)
        _add_description_display(pin_rows)

    summary = f"Removed {removed} of {len(selected_pins)} pin(s)."
    if errors:
        summary += " Errors: " + "; ".join(errors)

    return {
        "remove_message": summary,
        "remove_success": removed > 0 and not errors,
        "version_pins": pin_rows,
        "version_pins_total": total,
        "version_pins_offset": _PIN_BATCH_SIZE,
        "show_load_more_pins": total > _PIN_BATCH_SIZE,
        "all_pins_loaded": len(pin_rows) >= total,
        "selected_version_id": version_id,
        "selected_version_tag": version_tag,
    }


def _resolve_actor_workspace(
    *,
    adapter: OpsMcpAdapter,
    connector_id: str,
    connector_type: str,
    actor_id: str,
) -> str:
    """Resolve the workspace_id for an actor-scope pin via the Config API."""
    try:
        connector = adapter.get_connector(connector_id)
    except ValueError:
        return ""
    try:
        resolution = adapter.resolve_context_guid(
            connector=connector,
            context_guid=actor_id,
        )
        return resolution.workspace_id or ""
    except PyAirbyteInputError:
        return ""


@connector_version_manager_app.tool()
def advance_rollout(
    rollout_id: str,
    connector_id: str,
    docker_repository: str,
    docker_image_tag: str,
    target_percentage: str = "",
    auth_bearer_token: str = "",
    user_email: str = "",
) -> dict[str, Any]:
    """Advance a connector rollout to the next stage."""
    adapter = get_adapter(auth_bearer_token or None)
    config_api_root = adapter.config_api_root

    updated_by = _resolve_updated_by(
        user_email=user_email,
        bearer_token=auth_bearer_token or None,
        config_api_root=config_api_root,
    )

    parsed_pct = int(target_percentage) if target_percentage.strip() else None

    try:
        cloud_api.progress_connector_rollout(
            docker_repository=docker_repository,
            docker_image_tag=docker_image_tag,
            actor_definition_id=connector_id,
            rollout_id=rollout_id,
            updated_by=updated_by,
            config_api_root=config_api_root,
            target_percentage=parsed_pct,
            bearer_token=auth_bearer_token or None,
        )
    except PyAirbyteInputError as exc:
        return {
            "rollout_action_result": f"Failed to advance rollout: {exc}",
            "rollout_action_success": False,
        }

    pct_msg = f" to {parsed_pct}%" if parsed_pct else ""
    return {
        "rollout_action_result": (
            f"Successfully advanced rollout{pct_msg} for "
            f"{docker_repository}:{docker_image_tag}."
        ),
        "rollout_action_success": True,
    }


@connector_version_manager_app.tool()
def finalize_rollout(
    rollout_id: str,
    connector_id: str,
    docker_repository: str,
    docker_image_tag: str,
    state: str,
    auth_bearer_token: str = "",
    user_email: str = "",
) -> dict[str, Any]:
    """Finalize a connector rollout (promote, cancel, or rollback).

    `state` must be one of: `succeeded`, `canceled`, `failed_rolled_back`.
    """
    adapter = get_adapter(auth_bearer_token or None)
    config_api_root = adapter.config_api_root

    updated_by = _resolve_updated_by(
        user_email=user_email,
        bearer_token=auth_bearer_token or None,
        config_api_root=config_api_root,
    )

    try:
        cloud_api.finalize_connector_rollout(
            docker_repository=docker_repository,
            docker_image_tag=docker_image_tag,
            actor_definition_id=connector_id,
            rollout_id=rollout_id,
            updated_by=updated_by,
            state=state,
            config_api_root=config_api_root,
            bearer_token=auth_bearer_token or None,
        )
    except PyAirbyteInputError as exc:
        return {
            "rollout_action_result": f"Failed to finalize rollout: {exc}",
            "rollout_action_success": False,
        }

    action_label = {
        "succeeded": "promoted",
        "canceled": "canceled",
        "failed_rolled_back": "rolled back",
    }.get(state, state)

    return {
        "rollout_action_result": (
            f"Successfully {action_label} rollout for "
            f"{docker_repository}:{docker_image_tag}."
        ),
        "rollout_action_success": True,
    }


def _resolve_updated_by(
    *,
    user_email: str,
    bearer_token: str | None,
    config_api_root: str,
) -> str:
    """Resolve a user UUID from email, falling back to a default admin ID."""
    if not user_email:
        return DEFAULT_ADMIN_USER_ID

    try:
        return cloud_api.get_user_id_by_email(
            email=user_email,
            config_api_root=config_api_root,
            bearer_token=bearer_token,
        )
    except PyAirbyteInputError:
        return DEFAULT_ADMIN_USER_ID


@connector_version_manager_app.tool()
def search_orgs_workspaces(
    query: str = "",
) -> dict[str, Any]:
    """Search organizations and workspaces by name (case-insensitive substring)."""
    return search_organizations_and_workspaces(query=query)
