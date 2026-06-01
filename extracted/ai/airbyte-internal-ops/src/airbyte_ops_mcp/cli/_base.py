# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Base CLI application instance.

This module contains the root App instance that all domain modules import from.
It should have no imports from other cli modules to avoid circular dependencies.
"""

from __future__ import annotations

import importlib.metadata
from typing import Any

from cyclopts import App as _CyclOptsApp


class App(_CyclOptsApp):
    """Cyclopts App subclass that disables the default `--version` flag.

    Cyclopts registers `--version` as a meta-command on **every** `App`
    instance by default.  When a subcommand also accepts `--version` as a
    regular parameter (e.g. `artifacts publish --version 1.2.3`), the
    meta-command intercepts the token first, prints the package version, and
    exits — silently swallowing the real command.

    This subclass sets `version_flags` to an empty list so that no `App`
    in the tree inadvertently shadows a subcommand's `--version` parameter.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        kwargs.setdefault("version_flags", [])
        super().__init__(*args, **kwargs)


def _get_package_version() -> str:
    """Return the installed package version, or 'dev' if not installed."""
    for pkg_name in ("airbyte-internal-ops", "airbyte-ops-mcp"):
        try:
            return importlib.metadata.version(pkg_name)
        except importlib.metadata.PackageNotFoundError:
            continue
    return "dev"


_DOCS_URL = "https://airbytehq.github.io/airbyte-ops-mcp/airbyte_ops_mcp/cli.html"
_REPO_URL = "https://github.com/airbytehq/airbyte-ops-mcp"

app = App(
    name="airbyte-ops",
    help=(
        "Airbyte operations CLI for managing connectors, cloud deployments,"
        " and workflows.\n\n"
        f"Documentation: {_DOCS_URL}\n"
        f"Repository:    {_REPO_URL}"
    ),
    version=_get_package_version(),
    version_flags=["--version"],
)
