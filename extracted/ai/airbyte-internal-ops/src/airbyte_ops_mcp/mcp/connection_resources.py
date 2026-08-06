"""MCP tools for connection-level worker resource requirements."""

from __future__ import annotations

from typing import Annotated

from fastmcp import Context, FastMCP
from fastmcp_extensions import mcp_tool, register_mcp_tools
from pydantic import Field

from airbyte_ops_mcp.cloud_admin.connection_resources import (
    CpuRung,
    DiskRung,
    MemoryRung,
)
from airbyte_ops_mcp.cloud_admin.connection_resources import (
    get_connection_resource_requirements as get_connection_resource_requirements_core,
)
from airbyte_ops_mcp.cloud_admin.connection_resources import (
    set_connection_resource_requirements as set_connection_resource_requirements_core,
)
from airbyte_ops_mcp.cloud_admin.models import (
    ConnectionResourceRequirementsInfo,
    ConnectionResourceRequirementsOperationResult,
)
from airbyte_ops_mcp.mcp.cloud_auth import resolve_cloud_auth
from airbyte_ops_mcp.tier_cache import TierFilter


@mcp_tool(read_only=True, idempotent=True, open_world=True)
def get_connection_resource_requirements(
    connection_id: Annotated[str, Field(description="The Airbyte Cloud connection ID")],
    config_api_root: Annotated[
        str | None,
        Field(description="Optional Config API root override."),
    ] = None,
    *,
    ctx: Context,
) -> ConnectionResourceRequirementsInfo:
    """Get connection-level resource requirements.

    Returns the explicit CPU and memory values, plus whether the connection
    inherits platform defaults.
    """
    return get_connection_resource_requirements_core(
        auth=resolve_cloud_auth(ctx),
        connection_id=connection_id,
        config_api_root=config_api_root,
    )


@mcp_tool(destructive=True, idempotent=False, open_world=True)
def set_connection_resource_requirements(
    connection_id: Annotated[str, Field(description="The Airbyte Cloud connection ID")],
    workspace_id: Annotated[
        str,
        Field(description="The workspace that must own the connection"),
    ],
    approval_comment_url: Annotated[
        str,
        Field(description="Slack or GitHub approval record URL"),
    ],
    issue_url: Annotated[
        str,
        Field(description="GitHub issue URL providing context for this operation"),
    ],
    override_reason: Annotated[
        str,
        Field(description="Reason for the change; at least 10 characters"),
    ],
    cpu_rung: Annotated[
        CpuRung | None,
        Field(
            description=(
                "Absolute CPU limit rung. Omit to preserve the current dimension; "
                "`DEFAULT` clears it."
            )
        ),
    ] = None,
    memory_rung: Annotated[
        MemoryRung | None,
        Field(
            description=(
                "Absolute memory limit rung. Omit to preserve the current dimension; "
                "`DEFAULT` clears it."
            )
        ),
    ] = None,
    disk_rung: Annotated[
        DiskRung | None,
        Field(
            description=(
                "Absolute ephemeral-storage limit rung. Omit to preserve the current "
                "dimension; `DEFAULT` clears it."
            )
        ),
    ] = None,
    unset: Annotated[
        bool,
        Field(
            description="Clear the connection override and inherit platform defaults."
        ),
    ] = False,
    customer_tier_filter: Annotated[
        TierFilter,
        Field(description="Required customer tier filter; defaults to `TIER_2`."),
    ] = "TIER_2",
    cpu_impact_acknowledged: Annotated[
        bool,
        Field(
            description=(
                "Acknowledge shared worker capacity impact when increasing CPU."
            )
        ),
    ] = False,
    ai_agent_session_url: Annotated[
        str | None,
        Field(
            description="Optional URL for the AI agent session performing the change."
        ),
    ] = None,
    config_api_root: Annotated[
        str | None,
        Field(description="Optional Config API root override."),
    ] = None,
    *,
    ctx: Context,
) -> ConnectionResourceRequirementsOperationResult:
    """Set or clear connection-level worker resource requirements.

    CPU, memory, and ephemeral-storage use bounded absolute rungs. Omit a dimension
    to preserve its current values, or select `DEFAULT` to inherit platform
    defaults for that dimension. Setting CPU above the current value requires
    `cpu_impact_acknowledged=True` because each data worker consumes shared
    capacity. The production profile called `Boosted` corresponds to selecting
    4 CPU and 4Gi memory. Changes apply to the next sync attempt; an in-flight
    attempt keeps its current pod sizing. Clearing sends an empty
    resource-requirements object.
    """
    return set_connection_resource_requirements_core(
        auth=resolve_cloud_auth(ctx),
        connection_id=connection_id,
        workspace_id=workspace_id,
        cpu_rung=cpu_rung,
        memory_rung=memory_rung,
        disk_rung=disk_rung,
        unset=unset,
        override_reason=override_reason,
        issue_url=issue_url,
        approval_comment_url=approval_comment_url,
        customer_tier_filter=customer_tier_filter,
        cpu_impact_acknowledged=cpu_impact_acknowledged,
        ai_agent_session_url=ai_agent_session_url,
        config_api_root=config_api_root,
    )


def register_connection_resource_tools(app: FastMCP) -> None:
    """Register connection resource requirement tools with the FastMCP app."""
    register_mcp_tools(app, mcp_module=__name__)
