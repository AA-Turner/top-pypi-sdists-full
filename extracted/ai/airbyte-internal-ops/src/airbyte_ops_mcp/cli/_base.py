# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Base CLI application instance.

This module contains the root App instance that all domain modules import from.
It should have no imports from other cli modules to avoid circular dependencies.
"""

from __future__ import annotations

from fastmcp_extensions.cli import App, cli_app

from airbyte_ops_mcp._sentry import _SENTRY_DSN
from airbyte_ops_mcp.telemetry import _DEFAULT_SEGMENT_WRITE_KEY

_DOCS_URL = "https://airbytehq.github.io/airbyte-ops-mcp/airbyte_ops_mcp/cli.html"
_REPO_URL = "https://github.com/airbytehq/airbyte-ops-mcp"

app = cli_app(
    name="airbyte-ops",
    help_text=(
        "Airbyte operations CLI for managing connectors, cloud deployments,"
        " and workflows."
    ),
    package_name="airbyte-internal-ops",
    sentry_dsn=_SENTRY_DSN,
    segment_write_key=_DEFAULT_SEGMENT_WRITE_KEY,
    segment_user_id="airbyte-ops-cli",
    docs_url=_DOCS_URL,
    repo_url=_REPO_URL,
)
app.version_flags = ["--version"]

__all__ = ["App", "app"]
