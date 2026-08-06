"""Core operations for connection-level worker resource requirements."""

from __future__ import annotations

import logging
import re
from enum import StrEnum
from typing import Any, Callable

import requests
from airbyte import constants
from airbyte.exceptions import PyAirbyteInputError

from airbyte_ops_mcp.cloud_admin.api_client import make_config_api_request
from airbyte_ops_mcp.cloud_admin.guardrails import (
    build_tier_warning,
    validate_admin_and_authorization,
    validate_tier_filter,
)
from airbyte_ops_mcp.cloud_admin.models import (
    ConnectionResourceRequirementsInfo,
    ConnectionResourceRequirementsOperationResult,
)
from airbyte_ops_mcp.cloud_admin.version_overrides import ResolvedCloudAuth
from airbyte_ops_mcp.prod_db_access.queries import query_connection_workspace_details
from airbyte_ops_mcp.slack_api import SlackAPIError
from airbyte_ops_mcp.slack_posting import post_channel_message
from airbyte_ops_mcp.tier_cache import TierFilter, get_org_tier

logger = logging.getLogger(__name__)

_RESOURCE_REQUIREMENTS_SLACK_CHANNEL = "C06D5RCLBV4"
# This is above the current 3 CPU / 8 GiB standard tier while limiting shared-worker impact.
MAX_CPU_CORES = 4.0
MAX_MEMORY_BYTES = 16 * 1024**3
_RUNG_OFF_LADDER = "OFF_LADDER"
_CPU_PATTERN = re.compile(r"^(?:[0-9]+m|0|[0-9]+(?:\.[0-9]+)?|[0-9]*\.[0-9]+)$")
_MEMORY_PATTERN = re.compile(
    r"^(?P<number>0|[0-9]+(?:\.[0-9]+)?|[0-9]*\.[0-9]+)"
    r"(?P<unit>Ki|Mi|Gi)?$"
)
_MEMORY_MULTIPLIERS = {
    "": 1,
    "Ki": 1024,
    "Mi": 1024**2,
    "Gi": 1024**3,
}


class MemoryRung(StrEnum):
    """Supported memory limit rungs."""

    DEFAULT = "DEFAULT"
    ONE_GI = "1Gi"
    ONE_POINT_FIVE_GI = "1.5Gi"
    TWO_GI = "2Gi"
    THREE_GI = "3Gi"
    FOUR_GI = "4Gi"
    FIVE_GI = "5Gi"
    SIX_GI = "6Gi"
    SEVEN_GI = "7Gi"
    EIGHT_GI = "8Gi"


class CpuRung(StrEnum):
    """Supported CPU limit rungs."""

    DEFAULT = "DEFAULT"
    ONE = "1"
    TWO = "2"
    THREE = "3"
    FOUR = "4"


class DiskRung(StrEnum):
    """Supported ephemeral-storage limit rungs."""

    DEFAULT = "DEFAULT"
    TWO_GI = "2Gi"
    FIVE_GI = "5Gi"
    TEN_GI = "10Gi"
    FIFTEEN_GI = "15Gi"
    TWENTY_GI = "20Gi"


def _parse_cpu(value: str) -> float:
    if not _CPU_PATTERN.fullmatch(value):
        raise PyAirbyteInputError(message=f"Invalid CPU quantity: {value}.")
    if value.endswith("m"):
        return float(value[:-1]) / 1000
    return float(value)


def _parse_memory(value: str) -> int:
    match = _MEMORY_PATTERN.fullmatch(value)
    if match is None:
        raise PyAirbyteInputError(message=f"Invalid memory quantity: {value}.")
    return int(
        float(match.group("number")) * _MEMORY_MULTIPLIERS[match.group("unit") or ""]
    )


def _rung_values(
    rung_type: type[CpuRung] | type[MemoryRung] | type[DiskRung],
) -> tuple[str, ...]:
    return tuple(rung.value for rung in rung_type if rung.value != "DEFAULT")


def _rung_requirements(
    rung: CpuRung | MemoryRung | DiskRung | None,
    *,
    request_key: str,
    limit_key: str,
) -> dict[str, str]:
    if rung is None or rung.value == "DEFAULT":
        return {}
    return {
        request_key: rung.value,
        limit_key: rung.value,
    }


def _ladder_status(
    value: str | None,
    *,
    rung_type: type[CpuRung] | type[MemoryRung] | type[DiskRung],
    parser: Callable[[str], float | int],
) -> tuple[str, str | None]:
    rungs = _rung_values(rung_type)
    if value is None:
        return "DEFAULT", rungs[0]
    try:
        parsed = parser(value)
    except PyAirbyteInputError:
        return _RUNG_OFF_LADDER, None
    for index, rung in enumerate(rungs):
        if parsed == parser(rung):
            return rung, rungs[index + 1] if index + 1 < len(rungs) else None
        if parsed < parser(rung):
            return _RUNG_OFF_LADDER, rung
    return _RUNG_OFF_LADDER, None


def _validate_requirements(
    *,
    cpu_request: str | None = None,
    cpu_limit: str | None = None,
    memory_request: str | None = None,
    memory_limit: str | None = None,
    ephemeral_storage_request: str | None = None,
    ephemeral_storage_limit: str | None = None,
) -> None:
    cpu_values = {
        "cpu_request": cpu_request,
        "cpu_limit": cpu_limit,
    }
    parsed_cpu: dict[str, float] = {}
    for name, value in cpu_values.items():
        if value is None:
            continue
        parsed = _parse_cpu(value)
        if parsed > MAX_CPU_CORES:
            raise PyAirbyteInputError(
                message=f"{name} exceeds the maximum of {MAX_CPU_CORES:g} CPU cores.",
            )
        parsed_cpu[name] = parsed
    if (
        parsed_cpu.get("cpu_request") is not None
        and parsed_cpu.get("cpu_limit") is not None
        and parsed_cpu["cpu_request"] > parsed_cpu["cpu_limit"]
    ):
        raise PyAirbyteInputError(message="cpu_request cannot exceed cpu_limit.")

    memory_values = {
        "memory_request": memory_request,
        "memory_limit": memory_limit,
    }
    parsed_memory: dict[str, int] = {}
    for name, value in memory_values.items():
        if value is None:
            continue
        parsed = _parse_memory(value)
        if parsed > MAX_MEMORY_BYTES:
            max_memory = f"{MAX_MEMORY_BYTES / 1024**3:g}Gi"
            raise PyAirbyteInputError(
                message=f"{name} exceeds the maximum of {max_memory}.",
            )
        parsed_memory[name] = parsed
    if (
        parsed_memory.get("memory_request") is not None
        and parsed_memory.get("memory_limit") is not None
        and parsed_memory["memory_request"] > parsed_memory["memory_limit"]
    ):
        raise PyAirbyteInputError(message="memory_request cannot exceed memory_limit.")
    storage_values = {
        "ephemeral_storage_request": ephemeral_storage_request,
        "ephemeral_storage_limit": ephemeral_storage_limit,
    }
    parsed_storage: dict[str, int] = {}
    for name, value in storage_values.items():
        if value is None:
            continue
        parsed_storage[name] = _parse_memory(value)
    if (
        parsed_storage.get("ephemeral_storage_request") is not None
        and parsed_storage.get("ephemeral_storage_limit") is not None
        and parsed_storage["ephemeral_storage_request"]
        > parsed_storage["ephemeral_storage_limit"]
    ):
        raise PyAirbyteInputError(
            message=(
                "ephemeral_storage_request cannot exceed ephemeral_storage_limit."
            ),
        )


def _requirements_from_connection(
    connection: dict[str, Any],
    connection_id: str,
) -> ConnectionResourceRequirementsInfo:
    requirements = connection.get("resourceRequirements") or {}
    values = {
        "cpu_request": requirements.get("cpu_request"),
        "cpu_limit": requirements.get("cpu_limit"),
        "memory_request": requirements.get("memory_request"),
        "memory_limit": requirements.get("memory_limit"),
        "ephemeral_storage_request": requirements.get("ephemeral_storage_request"),
        "ephemeral_storage_limit": requirements.get("ephemeral_storage_limit"),
    }
    overridden = any(value is not None for value in values.values())
    cpu_rung, next_cpu_rung = _ladder_status(
        values["cpu_limit"],
        rung_type=CpuRung,
        parser=_parse_cpu,
    )
    memory_rung, next_memory_rung = _ladder_status(
        values["memory_limit"],
        rung_type=MemoryRung,
        parser=_parse_memory,
    )
    disk_rung, next_disk_rung = _ladder_status(
        values["ephemeral_storage_limit"],
        rung_type=DiskRung,
        parser=_parse_memory,
    )
    return ConnectionResourceRequirementsInfo(
        connection_id=connection_id,
        **values,
        cpu_rung=cpu_rung,
        next_cpu_rung=next_cpu_rung,
        memory_rung=memory_rung,
        next_memory_rung=next_memory_rung,
        disk_rung=disk_rung,
        next_disk_rung=next_disk_rung,
        was_overridden=overridden,
        is_on_defaults=not overridden,
    )


def _get_connection(
    *,
    auth: ResolvedCloudAuth,
    connection_id: str,
    config_api_root: str,
) -> dict[str, Any]:
    payload = {"connectionId": connection_id}
    return make_config_api_request(
        path="/connections/get",
        json=payload,
        operation="get connection resource requirements",
        extra_context={"connection_id": connection_id},
        client_id=auth.client_id,
        client_secret=auth.client_secret,
        bearer_token=auth.bearer_token,
        config_api_root=config_api_root,
    )


def get_connection_resource_requirements(
    *,
    auth: ResolvedCloudAuth,
    connection_id: str,
    config_api_root: str | None = None,
) -> ConnectionResourceRequirementsInfo:
    """Get connection-level resource requirements from `POST /v1/connections/get`."""
    connection = _get_connection(
        auth=auth,
        connection_id=connection_id,
        config_api_root=config_api_root or constants.CLOUD_CONFIG_API_ROOT,
    )
    return _requirements_from_connection(connection, connection_id)


def _notify_slack(
    *,
    connection_id: str,
    admin_user_email: str | None,
    previous: ConnectionResourceRequirementsInfo,
    current: ConnectionResourceRequirementsInfo,
    issue_url: str,
    override_reason: str,
    ai_agent_session_url: str | None,
) -> None:
    lines = [
        "🧰 *Connection Resource Requirements — Updated*",
        f">*Connection:* `{connection_id}`",
    ]
    for label, before, after in (
        ("CPU request", previous.cpu_request, current.cpu_request),
        ("CPU limit", previous.cpu_limit, current.cpu_limit),
        ("Memory request", previous.memory_request, current.memory_request),
        ("Memory limit", previous.memory_limit, current.memory_limit),
        (
            "Ephemeral-storage request",
            previous.ephemeral_storage_request,
            current.ephemeral_storage_request,
        ),
        (
            "Ephemeral-storage limit",
            previous.ephemeral_storage_limit,
            current.ephemeral_storage_limit,
        ),
    ):
        lines.append(f">*{label}:* `{before or 'default'}` → `{after or 'default'}`")
    if override_reason:
        lines.append(f">*Reason:* {override_reason}")
    if issue_url:
        lines.append(f">*Issue:* {issue_url}")
    if ai_agent_session_url:
        lines.append(f">*AI Session:* <{ai_agent_session_url}|View Session>")
    if admin_user_email:
        lines.append(f">*Approved by:* {admin_user_email}")
    try:
        post_channel_message(_RESOURCE_REQUIREMENTS_SLACK_CHANNEL, "\n".join(lines))
    except (SlackAPIError, requests.RequestException):
        logger.warning(
            "Failed to post connection-resource-requirements notification to Slack",
            exc_info=True,
        )


def set_connection_resource_requirements(
    *,
    auth: ResolvedCloudAuth,
    connection_id: str,
    workspace_id: str,
    cpu_rung: CpuRung | None,
    memory_rung: MemoryRung | None,
    disk_rung: DiskRung | None,
    unset: bool,
    override_reason: str | None,
    issue_url: str,
    approval_comment_url: str | None,
    customer_tier_filter: TierFilter,
    cpu_impact_acknowledged: bool = False,
    ai_agent_session_url: str | None = None,
    config_api_root: str | None = None,
    user_email: str | None = None,
) -> ConnectionResourceRequirementsOperationResult:
    """Set or clear connection-level worker resource requirements.

    CPU, memory, and ephemeral-storage use bounded absolute rungs. Clearing sends
    an empty `resourceRequirements` object. Changes apply to the next sync
    attempt; an in-flight attempt keeps its current pod sizing. Partial updates
    preserve previously configured values that are not supplied. Selecting
    `DEFAULT` clears that dimension so platform defaults apply. The production
    profile called `Boosted` corresponds to selecting 4 CPU and 4Gi memory.
    """
    config_root = config_api_root or constants.CLOUD_CONFIG_API_ROOT
    if not issue_url.startswith("https://github.com/"):
        raise PyAirbyteInputError(
            message="issue_url must be a valid GitHub URL (https://github.com/...).",
        )
    if not override_reason or len(override_reason.strip()) < 10:
        raise PyAirbyteInputError(
            message=("override_reason is required and must be at least 10 characters."),
        )
    if unset and any(value is not None for value in (cpu_rung, memory_rung, disk_rung)):
        raise PyAirbyteInputError(
            message="unset cannot be combined with resource values.",
        )
    if not unset and not any(
        value is not None for value in (cpu_rung, memory_rung, disk_rung)
    ):
        raise PyAirbyteInputError(
            message="At least one resource value is required unless unset=True.",
        )
    admin_user_email, auth_error = validate_admin_and_authorization(
        issue_url=issue_url,
        approval_comment_url=approval_comment_url,
        user_email=user_email,
    )
    if auth_error:
        return ConnectionResourceRequirementsOperationResult(
            success=False,
            message=auth_error,
            connection_id=connection_id,
        )
    rows = query_connection_workspace_details([connection_id])
    if not rows:
        return ConnectionResourceRequirementsOperationResult(
            success=False,
            message="Connection was not found in the production database.",
            connection_id=connection_id,
        )
    context = rows[0]
    if str(context["workspace_id"]) != workspace_id:
        return ConnectionResourceRequirementsOperationResult(
            success=False,
            message="Connection does not belong to the specified workspace.",
            connection_id=connection_id,
        )
    organization_id = str(context["organization_id"])
    tier_result = get_org_tier(organization_id, allow_degraded=True)
    tier_warning = build_tier_warning(tier_result.customer_tier)
    tier_ok, tier_error = validate_tier_filter(
        tier_result.customer_tier,
        customer_tier_filter,
        source_health=tier_result.source_health,
        organization_id=organization_id,
    )
    if not tier_ok:
        return ConnectionResourceRequirementsOperationResult(
            success=False,
            message=tier_error or "Tier filter mismatch.",
            connection_id=connection_id,
            customer_tier=tier_result.customer_tier,
            tier_warning=tier_warning,
        )

    previous = get_connection_resource_requirements(
        auth=auth,
        connection_id=connection_id,
        config_api_root=config_root,
    )
    effective_values = (
        {}
        if unset
        else {
            **(
                {
                    "cpu_request": previous.cpu_request,
                    "cpu_limit": previous.cpu_limit,
                }
                if cpu_rung is None
                else _rung_requirements(
                    cpu_rung,
                    request_key="cpu_request",
                    limit_key="cpu_limit",
                )
            ),
            **(
                {
                    "memory_request": previous.memory_request,
                    "memory_limit": previous.memory_limit,
                }
                if memory_rung is None
                else _rung_requirements(
                    memory_rung,
                    request_key="memory_request",
                    limit_key="memory_limit",
                )
            ),
            **(
                {
                    "ephemeral_storage_request": previous.ephemeral_storage_request,
                    "ephemeral_storage_limit": previous.ephemeral_storage_limit,
                }
                if disk_rung is None
                else _rung_requirements(
                    disk_rung,
                    request_key="ephemeral_storage_request",
                    limit_key="ephemeral_storage_limit",
                )
            ),
        }
    )
    effective_values = {
        key: value for key, value in effective_values.items() if value is not None
    }
    _validate_requirements(**effective_values)
    effective_cpu_request = effective_values.get("cpu_request")
    effective_cpu_limit = effective_values.get("cpu_limit")
    cpu_is_raised = any(
        new_value is not None
        and (old_value is None or _parse_cpu(new_value) > _parse_cpu(old_value))
        for new_value, old_value in (
            (effective_cpu_request, previous.cpu_request),
            (effective_cpu_limit, previous.cpu_limit),
        )
    )
    if cpu_is_raised and not cpu_impact_acknowledged:
        raise PyAirbyteInputError(
            message=(
                "cpu_impact_acknowledged=True is required when raising CPU; "
                "each data worker consumes shared capacity."
            ),
        )

    values = effective_values
    payload = {"connectionId": connection_id, "resourceRequirements": values}
    updated = _requirements_from_connection(
        make_config_api_request(
            path="/connections/update",
            json=payload,
            operation="update connection resource requirements",
            extra_context={"connection_id": connection_id},
            client_id=auth.client_id,
            client_secret=auth.client_secret,
            bearer_token=auth.bearer_token,
            config_api_root=config_root,
        ),
        connection_id,
    )
    _notify_slack(
        connection_id=connection_id,
        admin_user_email=admin_user_email,
        previous=previous,
        current=updated,
        issue_url=issue_url,
        override_reason=override_reason,
        ai_agent_session_url=ai_agent_session_url,
    )
    return ConnectionResourceRequirementsOperationResult(
        success=True,
        message=(
            "Connection resource requirements updated. New values apply to the "
            "next sync attempt; an in-flight attempt keeps its current pod sizing."
        ),
        connection_id=connection_id,
        previous_cpu_request=previous.cpu_request,
        previous_cpu_limit=previous.cpu_limit,
        previous_memory_request=previous.memory_request,
        previous_memory_limit=previous.memory_limit,
        new_cpu_request=updated.cpu_request,
        new_cpu_limit=updated.cpu_limit,
        new_memory_request=updated.memory_request,
        new_memory_limit=updated.memory_limit,
        previous_ephemeral_storage_request=previous.ephemeral_storage_request,
        previous_ephemeral_storage_limit=previous.ephemeral_storage_limit,
        new_ephemeral_storage_request=updated.ephemeral_storage_request,
        new_ephemeral_storage_limit=updated.ephemeral_storage_limit,
        was_overridden_before=previous.was_overridden,
        is_overridden_after=updated.was_overridden,
        customer_tier=tier_result.customer_tier,
        tier_warning=tier_warning,
    )
