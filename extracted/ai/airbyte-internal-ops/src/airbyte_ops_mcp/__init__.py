"""Airbyte Admin MCP - MCP and API interfaces that let the agents do the admin work.

.. include:: ../../../README.md
"""

from airbyte_ops_mcp import (
    airbyte_repo,
    cli,
    cloud_admin,
    connection_config_retriever,
    constants,
    mcp,
    prod_db_access,
    registry,
    regression_tests,
)

__version__ = "0.1.0"


def hello() -> str:
    """Return a friendly greeting."""
    return "Hello from airbyte-internal-ops!"


def get_version() -> str:
    """Return the current version."""
    return __version__


__all__ = [
    "__version__",
    "airbyte_repo",
    "cli",
    "cloud_admin",
    "connection_config_retriever",
    "constants",
    "get_version",
    "hello",
    "mcp",
    "prod_db_access",
    "registry",
    "regression_tests",
]
