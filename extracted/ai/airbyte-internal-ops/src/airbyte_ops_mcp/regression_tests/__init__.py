# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Live tests module for running connector validation and regression tests.

This module provides tools for testing Airbyte connectors against live data
without using Dagger. It uses Docker SDK directly for container orchestration.
"""

from airbyte_ops_mcp.regression_tests.connection_fetcher import (
    ConnectionData,
    fetch_connection_data,
)
from airbyte_ops_mcp.regression_tests.connection_secret_retriever import (
    SecretRetrievalError,
    enrich_config_with_secrets,
    is_secret_retriever_enabled,
    retrieve_unmasked_config,
    should_use_secret_retriever,
)
from airbyte_ops_mcp.regression_tests.models import (
    Command,
    ConnectorUnderTest,
    ExecutionResult,
    TargetOrControl,
)

__all__ = [
    "Command",
    "ConnectionData",
    "ConnectorUnderTest",
    "ExecutionResult",
    "SecretRetrievalError",
    "TargetOrControl",
    "enrich_config_with_secrets",
    "fetch_connection_data",
    "is_secret_retriever_enabled",
    "retrieve_unmasked_config",
    "should_use_secret_retriever",
]
