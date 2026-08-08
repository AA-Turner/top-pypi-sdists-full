# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Prod DB Access module for querying Airbyte Cloud Prod DB Replica.

This module provides:
- sql.py: SQL query templates and schema documentation
- db_engine.py: Database connection and engine management
- queries.py: Query execution functions
"""

from airbyte_ops_mcp.prod_db_access.db_engine import get_pool
from airbyte_ops_mcp.prod_db_access.queries import query_versions_with_pins
from airbyte_ops_mcp.prod_db_access.sql import (
    SELECT_ACTORS_PINNED_TO_VERSION,
    SELECT_CONNECTIONS_BY_CONNECTOR,
    SELECT_CONNECTOR_VERSIONS,
    SELECT_DATAPLANES_LIST,
    SELECT_DESTINATION_SUCCESSFUL_SYNCS_FOR_VERSION,
    SELECT_DESTINATION_SYNC_RESULTS_FOR_VERSION,
    SELECT_NEW_CONNECTOR_RELEASES,
    SELECT_ORG_WORKSPACES,
    SELECT_SOURCE_SUCCESSFUL_SYNCS_FOR_VERSION,
    SELECT_SOURCE_SYNC_RESULTS_FOR_VERSION,
    SELECT_VERSION_ID_BY_TAG,
    SELECT_VERSION_INFO_BY_ID,
    SELECT_VERSIONS_WITH_PINS,
    SELECT_VERSIONS_WITH_PINS_BY_DEFINITION,
    SELECT_WORKSPACE_INFO,
)

__all__ = [
    "SELECT_ACTORS_PINNED_TO_VERSION",
    "SELECT_CONNECTIONS_BY_CONNECTOR",
    "SELECT_CONNECTOR_VERSIONS",
    "SELECT_DATAPLANES_LIST",
    "SELECT_DESTINATION_SUCCESSFUL_SYNCS_FOR_VERSION",
    "SELECT_DESTINATION_SYNC_RESULTS_FOR_VERSION",
    "SELECT_NEW_CONNECTOR_RELEASES",
    "SELECT_ORG_WORKSPACES",
    "SELECT_SOURCE_SUCCESSFUL_SYNCS_FOR_VERSION",
    "SELECT_SOURCE_SYNC_RESULTS_FOR_VERSION",
    "SELECT_VERSIONS_WITH_PINS",
    "SELECT_VERSIONS_WITH_PINS_BY_DEFINITION",
    "SELECT_VERSION_ID_BY_TAG",
    "SELECT_VERSION_INFO_BY_ID",
    "SELECT_WORKSPACE_INFO",
    "get_pool",
    "query_versions_with_pins",
]
