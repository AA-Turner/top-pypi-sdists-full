# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""MotherDuck diagnostics: query history, recent queries, and active connections."""

from airbyte_ops_mcp.motherduck_diagnostics.connection import (
    execute_admin_query,
)
from airbyte_ops_mcp.motherduck_diagnostics.models import (
    MotherDuckActiveConnectionsResult,
    MotherDuckConnectionFilters,
    MotherDuckConnectionInfo,
    MotherDuckQueryFilters,
    MotherDuckQueryRecord,
    MotherDuckQueryResult,
    QueryTextTreatment,
)
from airbyte_ops_mcp.motherduck_diagnostics.queries import (
    query_active_connections,
    query_motherduck_queries,
)

__all__ = [
    "MotherDuckActiveConnectionsResult",
    "MotherDuckConnectionFilters",
    "MotherDuckConnectionInfo",
    "MotherDuckQueryFilters",
    "MotherDuckQueryRecord",
    "MotherDuckQueryResult",
    "QueryTextTreatment",
    "execute_admin_query",
    "query_active_connections",
    "query_motherduck_queries",
]
