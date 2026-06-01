# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Dependency bumping utilities for Airbyte connectors.

This module provides functionality to update all Poetry-managed dependencies
for connectors, refreshing the lock file to the latest versions allowed by
existing constraints.
"""

from __future__ import annotations

import subprocess
from dataclasses import dataclass, field
from pathlib import Path

from airbyte_ops_mcp.airbyte_repo.bump_version import (
    get_connector_path,
)
from airbyte_ops_mcp.airbyte_repo.list_connectors import (
    CONNECTOR_PATH_PREFIX,
    _detect_connector_language,
)

PYPROJECT_FILE_NAME = "pyproject.toml"
POETRY_LOCK_FILE_NAME = "poetry.lock"


class DepsError(Exception):
    """Base exception for dependency bump operations."""


@dataclass
class BumpDepsResult:
    """Result of a dependency bump operation."""

    connector: str
    language: str | None
    updated: bool
    dry_run: bool
    files_modified: list[str] = field(default_factory=list)
    message: str = ""
    outdated_packages: list[str] = field(default_factory=list)


def _get_outdated_packages(
    connector_path: Path,
    connector_name: str,
) -> list[str]:
    """Return a list of outdated top-level dependency names.

    Runs `poetry show --outdated --top-level --no-ansi` and parses the
    output.  Each line has the format::

        <package>  (!) <current>  <latest>  ...

    We return just the package names (first column).  An empty list means
    all dependencies are already at the latest allowed version.
    """
    try:
        proc = subprocess.run(
            ["poetry", "show", "--outdated", "--top-level", "--no-ansi"],
            cwd=str(connector_path),
            check=True,
            capture_output=True,
            text=True,
            timeout=300,
        )
    except FileNotFoundError as exc:
        raise DepsError(
            "Poetry is not installed or not on PATH. Cannot check outdated packages."
        ) from exc
    except subprocess.CalledProcessError as exc:
        raise DepsError(
            f"'poetry show --outdated' failed for connector '{connector_name}': "
            f"{exc.stderr or exc}"
        ) from exc
    except subprocess.TimeoutExpired as exc:
        raise DepsError(
            f"'poetry show --outdated' timed out for connector '{connector_name}'."
        ) from exc

    packages: list[str] = []
    for line in proc.stdout.strip().splitlines():
        parts = line.split()
        if parts:
            packages.append(parts[0])
    return packages


def bump_deps(
    repo_path: str | Path,
    connector_name: str,
    dry_run: bool = False,
) -> BumpDepsResult:
    """Update all dependencies for a connector.

    For Python / low-code connectors using Poetry, this runs
    `poetry update --lock` to refresh the lock file with the latest
    versions allowed by existing constraints in `pyproject.toml`.

    For connectors that do not use Poetry (manifest-only, Java, etc.),
    this is a no-op.

    Args:
        repo_path: Path to the Airbyte monorepo.
        connector_name: Technical name of the connector (e.g. `source-github`).
        dry_run: If `True`, report what would change without modifying files.

    Returns:
        A `BumpDepsResult` describing the outcome.

    Raises:
        ConnectorNotFoundError: If the connector directory does not exist.
        DepsError: On update failures.
    """
    repo_path = Path(repo_path)
    connector_path = get_connector_path(repo_path, connector_name)

    language = _detect_connector_language(connector_path, connector_name)

    # Only Poetry-based connectors have deps to update
    if language not in ("python", "low-code"):
        return BumpDepsResult(
            connector=connector_name,
            language=language,
            updated=False,
            dry_run=dry_run,
            message=(
                f"Connector '{connector_name}' (language={language}) does not use "
                f"Poetry. No dependencies to update."
            ),
        )

    pyproject_path = connector_path / PYPROJECT_FILE_NAME
    if not pyproject_path.exists():
        return BumpDepsResult(
            connector=connector_name,
            language=language,
            updated=False,
            dry_run=dry_run,
            message=f"No {PYPROJECT_FILE_NAME} found for connector '{connector_name}'.",
        )

    poetry_lock_path = connector_path / POETRY_LOCK_FILE_NAME
    if not poetry_lock_path.exists():
        return BumpDepsResult(
            connector=connector_name,
            language=language,
            updated=False,
            dry_run=dry_run,
            message=f"No {POETRY_LOCK_FILE_NAME} found for connector '{connector_name}'.",
        )

    if dry_run:
        return BumpDepsResult(
            connector=connector_name,
            language=language,
            updated=False,
            dry_run=True,
            files_modified=[
                f"{CONNECTOR_PATH_PREFIX}/{connector_name}/{POETRY_LOCK_FILE_NAME}"
            ],
            message="Dry run: would run 'poetry update --lock' to update dependencies.",
        )

    # Check for outdated packages before running the update.
    # This avoids false positives from Poetry reformatting the lock file
    # without actually changing any dependency versions.
    outdated_packages = _get_outdated_packages(connector_path, connector_name)

    if not outdated_packages:
        return BumpDepsResult(
            connector=connector_name,
            language=language,
            updated=False,
            dry_run=False,
            outdated_packages=[],
            message="Dependencies are already up to date.",
        )

    try:
        subprocess.run(
            ["poetry", "update", "--lock"],
            cwd=str(connector_path),
            check=True,
            capture_output=True,
            text=True,
            timeout=300,
        )
    except FileNotFoundError as exc:
        raise DepsError(
            "Poetry is not installed or not on PATH. Cannot update dependencies."
        ) from exc
    except subprocess.CalledProcessError as exc:
        raise DepsError(
            f"'poetry update --lock' failed for connector '{connector_name}': "
            f"{exc.stderr or exc}"
        ) from exc
    except subprocess.TimeoutExpired as exc:
        raise DepsError(
            f"'poetry update --lock' timed out for connector '{connector_name}'."
        ) from exc

    return BumpDepsResult(
        connector=connector_name,
        language=language,
        updated=True,
        dry_run=False,
        files_modified=[
            f"{CONNECTOR_PATH_PREFIX}/{connector_name}/{POETRY_LOCK_FILE_NAME}"
        ],
        outdated_packages=outdated_packages,
        message="Updated dependencies via 'poetry update --lock'.",
    )
