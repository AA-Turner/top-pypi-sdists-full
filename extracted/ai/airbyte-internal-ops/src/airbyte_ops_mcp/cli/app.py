# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Main CLI application entry point.

This module imports all domain modules (triggering command registration)
and provides the main() function for the CLI entry point.
"""

# These imports are intentional side-effects: each domain module registers its
# commands and command groups with the root app when imported. The order of
# imports is not significant as long as all sibling modules are imported before
# the app is invoked.
from airbyte_ops_mcp.cli import (
    cloud,  # noqa: F401
    cloud_connector_rollout,  # noqa: F401
    devin,  # noqa: F401
    dockerhub,  # noqa: F401
    gh,  # noqa: F401
    local,  # noqa: F401
    registry,  # noqa: F401
    roster,  # noqa: F401
    secrets,  # noqa: F401
)
from airbyte_ops_mcp.cli._base import app


def main() -> None:
    """Main entry point for the airbyte-ops CLI."""
    app()


if __name__ == "__main__":
    main()
