# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""CDK dependency bumping utilities for Airbyte connectors.

This module provides functionality to update the CDK (Connector Development Kit)
dependency version in a connector's project configuration files.
"""

from __future__ import annotations

import logging
import re
import subprocess
from dataclasses import dataclass, field
from pathlib import Path

import requests

from airbyte_ops_mcp.airbyte_repo.bump_version import (
    get_connector_path,
)
from airbyte_ops_mcp.airbyte_repo.list_connectors import (
    CONNECTOR_PATH_PREFIX,
    _detect_connector_language,
)

logger = logging.getLogger(__name__)

PYPROJECT_FILE_NAME = "pyproject.toml"
POETRY_LOCK_FILE_NAME = "poetry.lock"
BUILD_GRADLE_FILE_NAME = "build.gradle"


class CdkBumpError(Exception):
    """Base exception for CDK bump operations."""


class NoCdkDependencyError(CdkBumpError):
    """Raised when no CDK dependency is found in the connector's project files."""


class UnsupportedLanguageError(CdkBumpError):
    """Raised when the connector language is not supported for CDK bumps."""


@dataclass
class BumpCdkResult:
    """Result of a CDK bump operation."""

    connector: str
    language: str
    previous_version: str | None
    new_version: str | None
    updated: bool
    dry_run: bool
    files_modified: list[str] = field(default_factory=list)
    message: str = ""


JAVA_CDK_VERSION_PROPERTIES_PATH = (
    "airbyte-cdk/java/airbyte-cdk/core/src/main/resources/version.properties"
)


def get_latest_java_cdk_version(connector_path: Path) -> str:
    """Read the latest Java CDK version from the monorepo's `version.properties`.

    The Java CDK is not published to a public registry; its version is defined
    in the monorepo at `airbyte-cdk/java/airbyte-cdk/core/src/main/resources/version.properties`.

    Args:
        connector_path: Path to the connector directory (used to locate the monorepo root).

    Raises:
        CdkBumpError: If the version.properties file cannot be found or read.
    """
    # Walk up from the connector directory to find the monorepo root.
    # Connector paths are typically: <repo>/airbyte-integrations/connectors/<name>
    repo_root = connector_path.parent.parent.parent
    version_file = repo_root / JAVA_CDK_VERSION_PROPERTIES_PATH
    if not version_file.exists():
        raise CdkBumpError(
            f"Java CDK version.properties not found at {version_file}. "
            "Ensure the Airbyte monorepo is checked out."
        )
    for line in version_file.read_text().splitlines():
        line = line.strip()
        if line.startswith("version="):
            return line.split("=", 1)[1].strip()
    raise CdkBumpError(f"No 'version' key found in {version_file}.")


def get_latest_python_cdk_version() -> str:
    """Fetch the latest published version of `airbyte-cdk` from PyPI.

    Raises:
        CdkBumpError: If the PyPI API request fails.
    """
    cdk_pypi_url = "https://pypi.org/pypi/airbyte-cdk/json"
    try:
        response = requests.get(cdk_pypi_url, timeout=30)
        response.raise_for_status()
        package_info = response.json()
        return package_info["info"]["version"]
    except requests.RequestException as exc:
        msg = f"Failed to fetch latest airbyte-cdk version from PyPI: {exc}"
        raise CdkBumpError(msg) from exc


# Matches both forms of the airbyte-cdk dependency line:
#   airbyte-cdk = ">=6.0,<7.0"                              (string)
#   airbyte-cdk = {version = "^7.0.4", extras = [...]}       (dict)
_PYTHON_CDK_VERSION_RE = re.compile(
    r"^(?P<prefix>airbyte-cdk\s*=\s*)"
    r"(?:"
    r'"(?P<str_ver>[^"]*)"'  # string form
    r"|"
    r"(?P<dict_before>\{[^}]*version\s*=\s*)"
    r'"(?P<dict_ver>[^"]*)"'  # version inside dict
    r"(?P<dict_after>[^}]*\})"
    r")",
    re.MULTILINE,
)


def _get_current_python_cdk_version(pyproject_path: Path) -> str | None:
    """Extract the current `airbyte-cdk` version constraint from `pyproject.toml`.

    Uses regex to read the version without parsing/round-tripping TOML.

    Returns:
        The version constraint string, or `None` if not found.
    """
    if not pyproject_path.exists():
        return None
    content = pyproject_path.read_text()
    match = _PYTHON_CDK_VERSION_RE.search(content)
    if match is None:
        return None
    return match.group("str_ver") or match.group("dict_ver")


def _update_python_cdk_version(
    pyproject_path: Path,
    new_version: str,
) -> None:
    """Update the `airbyte-cdk` dependency version in `pyproject.toml`.

    Handles both simple string constraints and dict-style dependency specs.
    Uses regex to surgically replace only the version string, guaranteeing
    a minimal diff with no formatting side-effects.
    """
    content = pyproject_path.read_text()

    def _replacer(m: re.Match[str]) -> str:
        if m.group("str_ver") is not None:
            # String form: airbyte-cdk = "OLD" -> airbyte-cdk = "NEW"
            return f'{m.group("prefix")}"{new_version}"'
        # Dict form: preserve everything except the version value
        return (
            f"{m.group('prefix')}"
            f"{m.group('dict_before')}"
            f'"{new_version}"'
            f"{m.group('dict_after')}"
        )

    updated = _PYTHON_CDK_VERSION_RE.sub(_replacer, content, count=1)
    pyproject_path.write_text(updated)


def _get_current_java_cdk_version(build_gradle_path: Path) -> str | None:
    """Extract the current CDK version from a `build.gradle` file.

    Returns:
        The version string, or `None` if not found.
    """
    if not build_gradle_path.exists():
        return None
    content = build_gradle_path.read_text()
    match = re.search(
        r"cdkVersionRequired\s*=\s*['\"](?P<version>[0-9]+\.[0-9]+\.[0-9]+)['\"]",
        content,
    )
    if match:
        return match.group("version")
    return None


def _update_java_cdk_version(
    build_gradle_path: Path,
    new_version: str,
) -> None:
    """Update the CDK version in a `build.gradle` file."""
    content = build_gradle_path.read_text()
    updated = re.sub(
        r"(cdkVersionRequired\s*=\s*['\"])[0-9]+\.[0-9]+\.[0-9]+(['\"])",
        rf"\g<1>{new_version}\g<2>",
        content,
    )
    # Also disable useLocalCdk if present
    updated = re.sub(
        r"useLocalCdk\s*=\s*true",
        "useLocalCdk = false",
        updated,
    )
    build_gradle_path.write_text(updated)


def _compute_latest_constraint(latest_version: str) -> str:
    """Build a PEP 440 constraint pinned to the latest version with major upper bound.

    Example: `_compute_latest_constraint("7.13.0")` → `">=7.13.0,<8.0.0"`.
    """
    major = int(latest_version.split(".")[0])
    return f">={latest_version},<{major + 1}.0.0"


def bump_cdk(
    repo_path: str | Path,
    connector_name: str,
    force_latest: bool = False,
    dry_run: bool = False,
) -> BumpCdkResult:
    """Update the CDK dependency version for a connector.

    Two modes are supported:

    * **Default** (`force_latest=False`): Refresh the lock file so it
      resolves the newest CDK version that satisfies the *existing*
      constraint.  The constraint in `pyproject.toml` (or `build.gradle`)
      is **not** changed.
    * **Force-latest** (`force_latest=True`): Rewrite the constraint to
      `>=LATEST,<NEXT_MAJOR` and refresh the lock file.  Extras (e.g.
      `file-based`) are preserved.

    Args:
        repo_path: Path to the Airbyte monorepo.
        connector_name: Technical name of the connector (e.g. `source-github`).
        force_latest: If `True`, rewrite the version constraint to track the
            latest CDK release.  If `False`, only refresh the lock file.
        dry_run: If `True`, report what would change without modifying files.

    Returns:
        A `BumpCdkResult` describing the outcome.

    Raises:
        ConnectorNotFoundError: If the connector directory does not exist.
        UnsupportedLanguageError: If the connector language does not support CDK bumps.
        NoCdkDependencyError: If no CDK dependency is found.
        CdkBumpError: On other CDK bump failures.
    """
    repo_path = Path(repo_path)
    connector_path = get_connector_path(repo_path, connector_name)

    language = _detect_connector_language(connector_path, connector_name)
    if language is None:
        raise UnsupportedLanguageError(
            f"Cannot detect language for connector '{connector_name}'."
        )

    if language in ("python", "low-code"):
        return _bump_cdk_python(
            connector_path=connector_path,
            connector_name=connector_name,
            language=language,
            force_latest=force_latest,
            dry_run=dry_run,
        )
    elif language == "java":
        return _bump_cdk_java(
            connector_path=connector_path,
            connector_name=connector_name,
            force_latest=force_latest,
            dry_run=dry_run,
        )
    elif language == "manifest-only":
        return BumpCdkResult(
            connector=connector_name,
            language=language,
            previous_version=None,
            new_version=None,
            updated=False,
            dry_run=dry_run,
            message="Manifest-only connectors do not have a CDK dependency to bump.",
        )
    else:
        raise UnsupportedLanguageError(
            f"CDK bump is not supported for language '{language}'."
        )


def _refresh_poetry_lock(
    connector_path: Path,
    *,
    package: str = "airbyte-cdk",
) -> bool:
    """Run `poetry update <package>` to refresh the lock file.

    Returns `True` if the lock file was actually modified, `False` otherwise.
    """
    poetry_lock_path = connector_path / POETRY_LOCK_FILE_NAME
    if not poetry_lock_path.exists():
        return False
    original_content = poetry_lock_path.read_text()
    try:
        subprocess.run(
            ["poetry", "update", package, "--lock"],
            cwd=str(connector_path),
            check=True,
            capture_output=True,
            timeout=120,
        )
    except (
        subprocess.CalledProcessError,
        FileNotFoundError,
        subprocess.TimeoutExpired,
    ) as exc:
        logger.warning("Could not update poetry.lock: %s", exc)
        return False
    return poetry_lock_path.read_text() != original_content


def _bump_cdk_python(
    connector_path: Path,
    connector_name: str,
    language: str,
    force_latest: bool,
    dry_run: bool,
) -> BumpCdkResult:
    """Bump CDK for a Python or low-code connector.

    In *force-latest* mode the constraint in `pyproject.toml` is rewritten
    to `>=LATEST,<NEXT_MAJOR` and the lock file is refreshed.  Extras
    (e.g. `["file-based"]`) are preserved because only the `version` key
    in the TOML dict is updated.

    In *default* mode the constraint is left untouched and only the lock
    file is refreshed (`poetry update airbyte-cdk --lock`).
    """
    pyproject_path = connector_path / PYPROJECT_FILE_NAME
    if not pyproject_path.exists():
        raise NoCdkDependencyError(
            f"No {PYPROJECT_FILE_NAME} found for connector '{connector_name}'."
        )

    current_version = _get_current_python_cdk_version(pyproject_path)
    if current_version is None:
        raise NoCdkDependencyError(
            f"No airbyte-cdk dependency found in {PYPROJECT_FILE_NAME} for '{connector_name}'."
        )

    files_modified: list[str] = []

    if force_latest:
        # --force-latest: rewrite constraint to >=X.Y.Z,<NEXT_MAJOR.0.0
        latest_cdk = get_latest_python_cdk_version()
        new_version = _compute_latest_constraint(latest_cdk)

        if current_version == new_version:
            return BumpCdkResult(
                connector=connector_name,
                language=language,
                previous_version=current_version,
                new_version=new_version,
                updated=False,
                dry_run=dry_run,
                message=f"CDK constraint is already {new_version}.",
            )

        if dry_run:
            lock_exists = (connector_path / POETRY_LOCK_FILE_NAME).exists()
            dry_run_files = [
                f"{CONNECTOR_PATH_PREFIX}/{connector_name}/{PYPROJECT_FILE_NAME}"
            ]
            if lock_exists:
                dry_run_files.append(
                    f"{CONNECTOR_PATH_PREFIX}/{connector_name}/{POETRY_LOCK_FILE_NAME}"
                )
            return BumpCdkResult(
                connector=connector_name,
                language=language,
                previous_version=current_version,
                new_version=new_version,
                updated=False,
                dry_run=True,
                files_modified=dry_run_files,
                message=(
                    f"Dry run: would update airbyte-cdk constraint "
                    f"from {current_version} to {new_version}."
                ),
            )

        _update_python_cdk_version(pyproject_path, new_version)
        files_modified.append(
            f"{CONNECTOR_PATH_PREFIX}/{connector_name}/{PYPROJECT_FILE_NAME}"
        )

        if _refresh_poetry_lock(connector_path):
            files_modified.append(
                f"{CONNECTOR_PATH_PREFIX}/{connector_name}/{POETRY_LOCK_FILE_NAME}"
            )

        return BumpCdkResult(
            connector=connector_name,
            language=language,
            previous_version=current_version,
            new_version=new_version,
            updated=True,
            dry_run=False,
            files_modified=files_modified,
            message=(
                f"Updated airbyte-cdk constraint from {current_version} to {new_version}."
            ),
        )

    # Default mode: refresh lock file only, constraint unchanged
    if dry_run:
        lock_exists = (connector_path / POETRY_LOCK_FILE_NAME).exists()
        return BumpCdkResult(
            connector=connector_name,
            language=language,
            previous_version=current_version,
            new_version=current_version,
            updated=False,
            dry_run=True,
            files_modified=(
                [f"{CONNECTOR_PATH_PREFIX}/{connector_name}/{POETRY_LOCK_FILE_NAME}"]
                if lock_exists
                else []
            ),
            message=(
                f"Dry run: would refresh poetry.lock for airbyte-cdk "
                f"(constraint {current_version} unchanged)."
                if lock_exists
                else f"No poetry.lock found for '{connector_name}'."
            ),
        )

    lock_updated = _refresh_poetry_lock(connector_path)
    if lock_updated:
        files_modified.append(
            f"{CONNECTOR_PATH_PREFIX}/{connector_name}/{POETRY_LOCK_FILE_NAME}"
        )

    return BumpCdkResult(
        connector=connector_name,
        language=language,
        previous_version=current_version,
        new_version=current_version,
        updated=lock_updated,
        dry_run=False,
        files_modified=files_modified,
        message=(
            f"Refreshed poetry.lock for airbyte-cdk (constraint {current_version} unchanged)."
            if lock_updated
            else "poetry.lock not found or could not be updated."
        ),
    )


def _bump_cdk_java(
    connector_path: Path,
    connector_name: str,
    force_latest: bool,
    dry_run: bool,
) -> BumpCdkResult:
    """Bump CDK for a Java connector.

    Java connectors pin an exact CDK version in `build.gradle` and have no
    lock-file or constraint-range mechanism.  Both default and `--force-latest`
    modes update `cdkVersionRequired` to the version from `version.properties`.
    """
    build_gradle_path = connector_path / BUILD_GRADLE_FILE_NAME
    if not build_gradle_path.exists():
        raise NoCdkDependencyError(
            f"No {BUILD_GRADLE_FILE_NAME} found for connector '{connector_name}'."
        )

    current_version = _get_current_java_cdk_version(build_gradle_path)
    if current_version is None:
        raise NoCdkDependencyError(
            f"No cdkVersionRequired found in {BUILD_GRADLE_FILE_NAME} for '{connector_name}'."
        )

    latest_cdk = get_latest_java_cdk_version(connector_path)
    new_version = latest_cdk

    if current_version == new_version:
        return BumpCdkResult(
            connector=connector_name,
            language="java",
            previous_version=current_version,
            new_version=new_version,
            updated=False,
            dry_run=dry_run,
            message=f"CDK is already at {new_version}.",
        )

    if dry_run:
        return BumpCdkResult(
            connector=connector_name,
            language="java",
            previous_version=current_version,
            new_version=new_version,
            updated=False,
            dry_run=True,
            files_modified=[
                f"{CONNECTOR_PATH_PREFIX}/{connector_name}/{BUILD_GRADLE_FILE_NAME}"
            ],
            message=f"Dry run: would update CDK from {current_version} to {new_version}.",
        )

    _update_java_cdk_version(build_gradle_path, new_version)

    return BumpCdkResult(
        connector=connector_name,
        language="java",
        previous_version=current_version,
        new_version=new_version,
        updated=True,
        dry_run=False,
        files_modified=[
            f"{CONNECTOR_PATH_PREFIX}/{connector_name}/{BUILD_GRADLE_FILE_NAME}"
        ],
        message=f"Updated CDK from {current_version} to {new_version}.",
    )
