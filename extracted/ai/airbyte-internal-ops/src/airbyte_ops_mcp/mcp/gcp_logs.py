# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""MCP tools for GCP Cloud Logging operations.

This module provides MCP tools for querying GCP Cloud Logging,
particularly for looking up error details by error ID.

## MCP reference

.. include:: ../../../docs/mcp-generated/gcp_logs.md
    :start-line: 2
"""

from __future__ import annotations

__all__: list[str] = []

from typing import Annotated

from fastmcp import FastMCP
from fastmcp_extensions import mcp_tool, register_mcp_tools
from pydantic import Field

from airbyte_ops_mcp.gcp_logs import (
    GCPLogSearchResult,
    GCPSeverity,
    fetch_error_logs,
)
from airbyte_ops_mcp.gcp_logs.error_lookup import DEFAULT_GCP_PROJECT


@mcp_tool(
    read_only=True,
    idempotent=True,
)
def lookup_cloud_backend_error(
    error_id: Annotated[
        str,
        Field(
            description=(
                "The error ID (UUID) to search for. This is typically returned "
                "in API error responses as {'errorId': '...'}"
            )
        ),
    ],
    project: Annotated[
        str,
        Field(
            default=DEFAULT_GCP_PROJECT,
            description=(
                "GCP project ID to search in. Defaults to 'prod-ab-cloud-proj' "
                "(Airbyte Cloud production)."
            ),
        ),
    ],
    lookback_days: Annotated[
        int,
        Field(
            default=7,
            description="Number of days to look back in logs. Defaults to 7.",
        ),
    ],
    min_severity_filter: Annotated[
        GCPSeverity | None,
        Field(
            default=None,
            description="Optional minimum severity level to filter logs.",
        ),
    ],
    max_log_entries: Annotated[
        int,
        Field(
            default=200,
            description="Maximum number of log entries to return. Defaults to 200.",
        ),
    ],
) -> GCPLogSearchResult:
    """Look up error details from GCP Cloud Logging by error ID.

    When an Airbyte Cloud API returns an error response with only an error ID
    (e.g., {"errorId": "3173452e-8f22-4286-a1ec-b0f16c1e078a"}), this tool
    fetches the full stack trace and error details from GCP Cloud Logging.

    The tool searches for log entries containing the error ID and fetches
    related entries (multi-line stack traces) from the same timestamp and pod.

    Requires GCP credentials with Logs Viewer role on the target project.
    """
    return fetch_error_logs(
        error_id=error_id,
        project=project,
        lookback_days=lookback_days,
        min_severity_filter=min_severity_filter,
        max_log_entries=max_log_entries,
    )


def register_gcp_logs_tools(app: FastMCP) -> None:
    """Register GCP logs tools with the FastMCP app."""
    register_mcp_tools(app)
