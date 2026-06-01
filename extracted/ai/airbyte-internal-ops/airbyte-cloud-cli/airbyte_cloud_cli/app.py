# Copyright (c) 2026 Airbyte, Inc., all rights reserved.
"""Main entry point for the `airbyte-cloud` CLI."""

from __future__ import annotations

# These imports intentionally register command groups on the root app.
from airbyte_cloud_cli import (  # noqa: F401
    connections,
    destinations,
    jobs,
    sources,
    workspaces,
)
from airbyte_cloud_cli._base import app


def main() -> None:
    """Run the `airbyte-cloud` CLI."""
    app()


if __name__ == "__main__":
    main()
