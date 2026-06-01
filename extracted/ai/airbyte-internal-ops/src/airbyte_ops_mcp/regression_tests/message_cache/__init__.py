# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Message cache for storing Airbyte messages from connector executions.

This module provides a DuckDB-based message cache for persisting and querying
Airbyte messages produced during connector test runs.

Based on airbyte-ci implementation:
https://github.com/airbytehq/airbyte/tree/master/airbyte-ci/connectors/live-tests/src/live_tests/commons/backends
"""

from airbyte_ops_mcp.regression_tests.message_cache.duckdb_cache import (
    DuckDbMessageCache,
)

__all__ = [
    "DuckDbMessageCache",
]
