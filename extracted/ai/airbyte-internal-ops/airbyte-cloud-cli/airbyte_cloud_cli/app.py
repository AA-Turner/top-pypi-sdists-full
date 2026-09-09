# Copyright (c) 2026 Airbyte, Inc., all rights reserved.
"""Main entry point for the `airbyte-cloud` CLI."""

from __future__ import annotations

import sys

from airbyte.exceptions import PyAirbyteError, PyAirbyteInternalError

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
    try:
        app()
    except PyAirbyteInternalError:
        raise
    except PyAirbyteError as error:
        print(error.get_message(), file=sys.stderr)
        if error.guidance:
            print(f"Guidance: {error.guidance}", file=sys.stderr)
        if error.help_url:
            print(f"More info: {error.help_url}", file=sys.stderr)
        raise SystemExit(1) from None


if __name__ == "__main__":
    main()
