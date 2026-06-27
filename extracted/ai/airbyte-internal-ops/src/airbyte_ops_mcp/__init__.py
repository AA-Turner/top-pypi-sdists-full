"""Airbyte Admin MCP - MCP and API interfaces that let the agents do the admin work.

.. include:: ../../../README.md
"""

from importlib.metadata import PackageNotFoundError, version

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

try:
    __version__ = version("airbyte-internal-ops")
except PackageNotFoundError:
    __version__ = "0.0.0"


def hello() -> str:
    """Return a friendly greeting."""
    return "Hello from airbyte-internal-ops!"


__all__ = [
    "__version__",
    "airbyte_repo",
    "cli",
    "cloud_admin",
    "connection_config_retriever",
    "constants",
    "hello",
    "mcp",
    "prod_db_access",
    "registry",
    "regression_tests",
]
