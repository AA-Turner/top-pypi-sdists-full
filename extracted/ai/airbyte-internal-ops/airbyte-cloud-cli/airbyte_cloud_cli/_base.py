# Copyright (c) 2026 Airbyte, Inc., all rights reserved.
"""Base application for the `airbyte-cloud` CLI."""

from __future__ import annotations

import importlib.metadata
from typing import Any

from cyclopts import App as _CyclOptsApp


class App(_CyclOptsApp):
    """Cyclopts App subclass with subcommand `--version` passthrough."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        kwargs.setdefault("version_flags", [])
        super().__init__(*args, **kwargs)


def _get_package_version() -> str:
    """Return the installed package version, or `dev` if not installed."""
    for pkg_name in ("airbyte-cloud-cli", "airbyte-internal-ops", "airbyte-ops-mcp"):
        try:
            return importlib.metadata.version(pkg_name)
        except importlib.metadata.PackageNotFoundError:
            continue
    return "dev"


app = App(
    name="airbyte-cloud",
    help="Internal Airbyte Cloud CLI for workspaces, sources, destinations, connections, and jobs.",
    version=_get_package_version(),
    version_flags=["--version"],
)
