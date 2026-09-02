"""Hybrid metadata contract validator for hosted discovery results.

This module is private to the spec_kitty_tracker.discovery package. It is
imported and called by spec_kitty_tracker.discovery.__init__'s public
discover_workspaces / discover_resources functions after the per-provider
adapter returns and before the result is handed back to the caller.

See kitty-specs/006-hosted-discovery-contract-hardening/contracts/
discovery-contract.md §4 for the full rule list.
"""

from __future__ import annotations

import json
from typing import Any

from spec_kitty_tracker.discovery.types import (
    DiscoveredResource,
    DiscoveredWorkspace,
    DiscoveryResult,
)
from spec_kitty_tracker.errors import DiscoveryContractError

_NORMALIZED_WORKSPACE_KEYS: tuple[str, ...] = ("workspace_handle", "workspace_url")
_NORMALIZED_RESOURCE_KEYS: tuple[str, ...] = ("display_key", "resource_url")


def _is_optional_str(value: Any) -> bool:
    """True iff value is None or str. Used by WS-008/WS-009/RS-011/RS-012."""
    return value is None or isinstance(value, str)


def _is_json_serializable(value: Any) -> bool:
    """True iff value survives a json.dumps + json.loads round-trip equal."""
    try:
        round_tripped = json.loads(json.dumps(value))
    except (TypeError, ValueError):
        return False
    return round_tripped == value  # type: ignore[no-any-return]


def validate_workspace_contract(workspace: DiscoveredWorkspace) -> None:
    """Apply rules WS-001..WS-009 to a single workspace.

    Raises DiscoveryContractError on the first violation.
    """
    provider = getattr(workspace, "provider", None) or "<unknown>"
    _require_non_empty_str(workspace.id, provider, "workspace", "id", "WS-001")
    _require_non_empty_str(workspace.name, provider, "workspace", "name", "WS-002")
    if not isinstance(workspace.display, str):
        raise DiscoveryContractError(
            f"workspace.display must be str, got {type(workspace.display).__name__}",
            provider=provider,
            kind="workspace",
            field_path="display",
            reason="WS-003",
        )
    _require_non_empty_str(workspace.kind, provider, "workspace", "kind", "WS-004")
    _require_non_empty_str(workspace.provider, provider, "workspace", "provider", "WS-005")

    ctx = workspace.provider_context
    if ctx is None:
        return  # provider_context is allowed to be None
    if not isinstance(ctx, dict):
        raise DiscoveryContractError(
            f"workspace.provider_context must be dict or None, got {type(ctx).__name__}",
            provider=provider,
            kind="workspace",
            field_path="provider_context",
            reason="WS-006",
        )
    if not _is_json_serializable(ctx):
        raise DiscoveryContractError(
            "workspace.provider_context must be JSON-serializable",
            provider=provider,
            kind="workspace",
            field_path="provider_context",
            reason="WS-007",
        )
    if "workspace_handle" in ctx and not _is_optional_str(ctx["workspace_handle"]):
        raise DiscoveryContractError(
            f"workspace_handle must be str | None, got {type(ctx['workspace_handle']).__name__}",
            provider=provider,
            kind="workspace",
            field_path="provider_context.workspace_handle",
            reason="WS-008",
        )
    if "workspace_url" in ctx and not _is_optional_str(ctx["workspace_url"]):
        raise DiscoveryContractError(
            f"workspace_url must be str | None, got {type(ctx['workspace_url']).__name__}",
            provider=provider,
            kind="workspace",
            field_path="provider_context.workspace_url",
            reason="WS-009",
        )


def validate_resource_contract(resource: DiscoveredResource) -> None:
    """Apply rules RS-001..RS-012 to a single resource.

    Raises DiscoveryContractError on the first violation.
    """
    provider = getattr(resource, "provider", None) or "<unknown>"
    _require_non_empty_str(resource.provider, provider, "resource", "provider", "RS-001")
    _require_non_empty_str(
        resource.parent_workspace_id, provider, "resource", "parent_workspace_id", "RS-002"
    )
    _require_non_empty_str(resource.resource_type, provider, "resource", "resource_type", "RS-003")
    _require_non_empty_str(resource.stable_ref, provider, "resource", "stable_ref", "RS-004")
    _require_non_empty_str(resource.display_name, provider, "resource", "display_name", "RS-005")

    cp = resource.connector_params
    if not isinstance(cp, dict):
        raise DiscoveryContractError(
            f"resource.connector_params must be dict, got {type(cp).__name__}",
            provider=provider,
            kind="resource",
            field_path="connector_params",
            reason="RS-006",
        )
    if not cp:
        raise DiscoveryContractError(
            "resource.connector_params must be non-empty",
            provider=provider,
            kind="resource",
            field_path="connector_params",
            reason="RS-007",
        )
    if not _is_json_serializable(cp):
        raise DiscoveryContractError(
            "resource.connector_params must be JSON-serializable",
            provider=provider,
            kind="resource",
            field_path="connector_params",
            reason="RS-008",
        )

    rm = resource.routing_metadata
    if not isinstance(rm, dict):
        raise DiscoveryContractError(
            f"resource.routing_metadata must be dict, got {type(rm).__name__}",
            provider=provider,
            kind="resource",
            field_path="routing_metadata",
            reason="RS-009",
        )
    if not _is_json_serializable(rm):
        raise DiscoveryContractError(
            "resource.routing_metadata must be JSON-serializable",
            provider=provider,
            kind="resource",
            field_path="routing_metadata",
            reason="RS-010",
        )
    if "display_key" in rm and not _is_optional_str(rm["display_key"]):
        raise DiscoveryContractError(
            f"display_key must be str | None, got {type(rm['display_key']).__name__}",
            provider=provider,
            kind="resource",
            field_path="routing_metadata.display_key",
            reason="RS-011",
        )
    if "resource_url" in rm and not _is_optional_str(rm["resource_url"]):
        raise DiscoveryContractError(
            f"resource_url must be str | None, got {type(rm['resource_url']).__name__}",
            provider=provider,
            kind="resource",
            field_path="routing_metadata.resource_url",
            reason="RS-012",
        )


def validate_workspace_result(
    result: DiscoveryResult[DiscoveredWorkspace],
) -> None:
    """Validate envelope shape (DR-001..DR-003), then each item (WS-*)."""
    _validate_envelope(result)
    for index, ws in enumerate(result.items):
        try:
            validate_workspace_contract(ws)
        except DiscoveryContractError as exc:
            # Re-raise with item index in the field_path for traceability
            raise DiscoveryContractError(
                str(exc),
                provider=exc.provider,
                kind=exc.kind,
                field_path=f"items[{index}].{exc.field_path}",
                reason=exc.reason,
            ) from exc


def validate_resource_result(
    result: DiscoveryResult[DiscoveredResource],
) -> None:
    """Validate envelope shape (DR-001..DR-003), then each item (RS-*)."""
    _validate_envelope(result)
    for index, res in enumerate(result.items):
        try:
            validate_resource_contract(res)
        except DiscoveryContractError as exc:
            raise DiscoveryContractError(
                str(exc),
                provider=exc.provider,
                kind=exc.kind,
                field_path=f"items[{index}].{exc.field_path}",
                reason=exc.reason,
            ) from exc


# ---------------------------------------------------------------------------
# Private helpers
# ---------------------------------------------------------------------------


def _require_non_empty_str(
    value: Any,
    provider: str,
    kind: str,
    field_path: str,
    reason: str,
) -> None:
    if not isinstance(value, str) or not value:
        raise DiscoveryContractError(
            f"{kind}.{field_path} must be a non-empty str, got {type(value).__name__} ({value!r})",
            provider=provider,
            kind=kind,
            field_path=field_path,
            reason=reason,
        )


def _validate_envelope(result: Any) -> None:
    if not isinstance(result, DiscoveryResult):
        raise DiscoveryContractError(
            f"adapter must return DiscoveryResult, got {type(result).__name__}",
            kind="result",
            field_path="<root>",
            reason="DR-001",
        )
    if not isinstance(result.items, list):
        raise DiscoveryContractError(
            f"DiscoveryResult.items must be list, got {type(result.items).__name__}",
            kind="result",
            field_path="items",
            reason="DR-002",
        )
    if not isinstance(result.truncated, bool):
        raise DiscoveryContractError(
            f"DiscoveryResult.truncated must be bool, got {type(result.truncated).__name__}",
            kind="result",
            field_path="truncated",
            reason="DR-003",
        )
