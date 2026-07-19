# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""MCP tools for MotherDuck query diagnostics.

Provides tools for querying MotherDuck QUERY_HISTORY, RECENT_QUERIES,
and active server connections. Requires org admin credentials via the
`MOTHERDUCK_ADMIN_TOKEN` environment variable.

## MCP reference

.. include:: ../../../docs/mcp-generated/motherduck_diagnostics.md
    :start-line: 2
"""

from __future__ import annotations

__all__: list[str] = []

from typing import Annotated

from fastmcp import FastMCP
from fastmcp_extensions import mcp_tool, register_mcp_tools
from pydantic import Field

from airbyte_ops_mcp.motherduck_diagnostics.models import (
    MotherDuckActiveConnectionsResult,
    MotherDuckConnectionFilters,
    MotherDuckQueryFilters,
    MotherDuckQueryResult,
    QueryTextTreatment,
)
from airbyte_ops_mcp.motherduck_diagnostics.queries import (
    query_active_connections,
)
from airbyte_ops_mcp.motherduck_diagnostics.queries import (
    query_motherduck_queries as _query_motherduck_queries,
)


@mcp_tool(
    read_only=True,
    idempotent=True,
)
def query_motherduck_queries(
    filters: Annotated[
        MotherDuckQueryFilters,
        Field(description="Structured query filters."),
    ],
    realtime: Annotated[
        bool,
        Field(
            default=False,
            description=(
                "If true, query RECENT_QUERIES (active + just-completed). "
                "If false, query QUERY_HISTORY (historical, slight delay)."
            ),
        ),
    ] = False,
    limit: Annotated[
        int,
        Field(
            default=1000,
            description="Number of rows to return.",
        ),
    ] = 1000,
    include_query_text: Annotated[
        bool | QueryTextTreatment,
        Field(
            default=True,
            description=(
                "Controls QUERY_TEXT inclusion. "
                "False omits entirely. "
                "True applies default treatment (1000 char limit, redact string constants). "
                "Pass a QueryTextTreatment object for fine-grained control."
            ),
        ),
    ] = True,
) -> MotherDuckQueryResult:
    """Query MotherDuck query execution data for diagnostics.

    Supports two modes via the `realtime` toggle:

    - `realtime=false` (default): Queries QUERY_HISTORY -- historical data with
      slight delay. Best for performance analysis, error pattern mining, cold
      start investigation.
    - `realtime=true`: Queries RECENT_QUERIES -- currently running + just-completed
      queries not yet in QUERY_HISTORY. Best for live debugging, detecting stuck
      queries.

    The response includes `query_hash` (SHA-256 of normalized SQL for deduplication),
    `query_metadata` (parsed from leading `/* {...} */` comments), and `query_subtype`
    (regex-derived statement classification like select/insert/copy).
    """
    return _query_motherduck_queries(
        filters,
        realtime=realtime,
        limit=limit,
        include_query_text=include_query_text,
    )


@mcp_tool(
    read_only=True,
    idempotent=True,
)
def query_motherduck_active_connections(
    filters: Annotated[
        MotherDuckConnectionFilters,
        Field(description="Structured connection filters."),
    ],
    include_query_text: Annotated[
        bool | QueryTextTreatment,
        Field(
            default=True,
            description=(
                "Controls client_query text inclusion. "
                "False omits entirely. "
                "True applies default treatment (1000 char limit, redact string constants). "
                "Pass a QueryTextTreatment object for fine-grained control."
            ),
        ),
    ] = True,
) -> MotherDuckActiveConnectionsResult:
    """List active MotherDuck server connections.

    Calls `md_active_server_connections()` to show which ducklings currently
    have active transactions. Useful for debugging connection pool exhaustion,
    orphaned sessions, or verifying expected service accounts are live.

    Use the `client_connection_id` from results to filter the query history
    tool via `filters.query_connection_id` for correlated diagnostics.

    The `client_query` field (currently running SQL) receives the same text
    treatment as the query history tool: truncation, string constant redaction,
    metadata extraction, hashing, and subtype detection.
    """
    return query_active_connections(filters, include_query_text=include_query_text)


def register_motherduck_diagnostics_tools(app: FastMCP) -> None:
    """Register MotherDuck diagnostics tools with the FastMCP app."""
    register_mcp_tools(app, mcp_module=__name__)
