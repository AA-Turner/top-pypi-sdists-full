# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Detect changed connectors in the Airbyte monorepo.

This module provides functionality to detect which connectors have been modified
by comparing git diffs between branches.
"""

from __future__ import annotations

import logging
import re
import subprocess
from dataclasses import dataclass
from enum import StrEnum
from functools import lru_cache
from pathlib import Path
from typing import Any

import requests
import yaml

from airbyte_ops_mcp.github_api import GitHubAPIError, get_pr_changed_files
from airbyte_ops_mcp.registry._enums import ConnectorLanguage, ConnectorType

CONNECTOR_PATH_PREFIX = "airbyte-integrations/connectors"
METADATA_FILE_NAME = "metadata.yaml"
GIT_DEFAULT_BRANCH = "origin/master"

logger = logging.getLogger(__name__)


class ConnectorSubtype(StrEnum):
    """Connector subtypes based on data source category."""

    API = "api"
    DATABASE = "database"
    FILE = "file"
    CUSTOM = "custom"


def _extract_connector_names(changed_files: list[str]) -> list[str]:
    """Extract unique connector names from a list of changed file paths.

    Args:
        changed_files: File paths relative to the repo root.

    Returns:
        Sorted list of connector technical names.
    """
    changed_connectors: set[str] = set()
    for file_path in changed_files:
        if file_path.startswith(CONNECTOR_PATH_PREFIX + "/"):
            # e.g. "airbyte-integrations/connectors/source-faker/..." -> "source-faker"
            path_parts = file_path.split("/")
            if len(path_parts) >= 3:
                changed_connectors.add(path_parts[2])
    return sorted(changed_connectors)


def get_modified_connectors(
    repo_path: str | Path,
    base_ref: str = GIT_DEFAULT_BRANCH,
    head_ref: str = "HEAD",
) -> list[str]:
    """Get list of connector IDs modified according to a local git diff.

    This is the *local-only* fallback used when the GitHub API path is not
    available (e.g. no PR number or no token).  It uses `git merge-base`
    when possible so that only changes introduced on the head branch are
    reported, falling back to a plain two-ref diff when the merge-base
    cannot be determined (shallow clones without enough history).

    Prefer `get_modified_connectors_from_github` whenever a PR number
    is known, as it avoids shallow-clone pitfalls entirely.

    Args:
        repo_path: Path to the Airbyte monorepo.
        base_ref: Base git reference to compare against.
        head_ref: Head git reference to compare.

    Returns:
        Sorted list of connector technical names.
    """
    repo_path = Path(repo_path)

    # Try to find the merge-base so the diff only contains changes introduced
    # on the head branch, avoiding false positives from unrelated base-branch
    # commits.  Falls back to a plain two-ref diff when unavailable.
    effective_base = base_ref
    try:
        mb_result = subprocess.run(
            ["git", "merge-base", base_ref, head_ref],
            cwd=repo_path,
            capture_output=True,
            text=True,
            check=True,
            timeout=30,
        )
        effective_base = mb_result.stdout.strip()
        logger.debug("Using merge-base %s for diff", effective_base)
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
        logger.debug(
            "Could not determine merge-base for %s..%s; falling back to plain diff",
            base_ref,
            head_ref,
        )

    try:
        result = subprocess.run(
            ["git", "diff", "--name-only", effective_base, head_ref],
            cwd=repo_path,
            capture_output=True,
            text=True,
            check=True,
            timeout=30,
        )
        changed_files = result.stdout.strip().split("\n")
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to get git diff: {e.stderr}") from e
    except subprocess.TimeoutExpired as e:
        raise RuntimeError("Git diff command timed out after 30 seconds") from e

    return _extract_connector_names(changed_files)


def format_github_actions_connector_matrix(
    connectors: list[str],
) -> dict[str, list[str]]:
    """Format connector names as a GitHub Actions matrix.

    GitHub Actions matrix generation needs at least one value. Return an empty
    connector placeholder when no connectors changed so callers can pair this
    with an `if` guard on the matrix job.
    """
    return {"connector": connectors or [""]}


def get_modified_connectors_from_github(
    pr_number: int,
    pr_owner: str,
    pr_repo: str,
    gh_token: str,
) -> list[str]:
    """Get list of connector IDs modified in a PR via the GitHub API.

    This is the preferred path when a PR number is known because it is
    immune to shallow-clone depth issues and always returns an accurate
    diff (only the files the PR actually changes).

    Args:
        pr_number: Pull request number.
        pr_owner: Repository owner (e.g. `"airbytehq"`).
        pr_repo: Repository name (e.g. `"airbyte"`).
        gh_token: GitHub API token (must be provided explicitly).

    Returns:
        Sorted list of connector technical names.

    Raises:
        GitHubAPIError: If the API request fails.
    """
    logger.info(
        "Fetching changed files for PR %s/%s#%d via GitHub API",
        pr_owner,
        pr_repo,
        pr_number,
    )
    changed_files = get_pr_changed_files(pr_owner, pr_repo, pr_number, token=gh_token)
    return _extract_connector_names(changed_files)


@lru_cache(maxsize=128)
def get_certified_connectors(repo_path: str | Path) -> set[str]:
    """Get set of all certified connector IDs from metadata.

    This function reads the metadata.yaml file for each connector to determine
    which connectors have "certified" support level.

    Args:
        repo_path: Path to the Airbyte monorepo

    Returns:
        Set of certified connector technical names

    Example:
        >>> certified = get_certified_connectors("/path/to/airbyte")
        >>> "source-postgres" in certified
        True
    """
    repo_path = Path(repo_path)
    connectors_dir = repo_path / CONNECTOR_PATH_PREFIX

    if not connectors_dir.exists():
        raise ValueError(f"Connectors directory not found: {connectors_dir}")

    certified_connectors = set()

    # Iterate through all connector directories
    for connector_dir in connectors_dir.iterdir():
        if not connector_dir.is_dir():
            continue

        metadata_file = connector_dir / METADATA_FILE_NAME
        if not metadata_file.exists():
            continue

        # Read metadata to check support level
        try:
            import yaml

            with open(metadata_file) as f:
                metadata = yaml.safe_load(f)

            support_level = metadata.get("data", {}).get("supportLevel")
            if support_level == "certified":
                certified_connectors.add(connector_dir.name)
        except Exception:
            # Skip connectors with invalid metadata
            continue

    return certified_connectors


def get_all_connectors(repo_path: str | Path) -> set[str]:
    """Get set of all connector IDs in the repository.

    Args:
        repo_path: Path to the Airbyte monorepo

    Returns:
        Set of all connector technical names

    Example:
        >>> all_connectors = get_all_connectors("/path/to/airbyte")
        >>> "source-faker" in all_connectors
        True
    """
    repo_path = Path(repo_path)
    connectors_dir = repo_path / CONNECTOR_PATH_PREFIX

    if not connectors_dir.exists():
        raise ValueError(f"Connectors directory not found: {connectors_dir}")

    return {p.name for p in connectors_dir.iterdir() if p.is_dir()}


def get_connector_metadata(
    repo_path: str | Path,
    connector_name: str,
) -> dict[str, Any] | None:
    """Get metadata for a specific connector.

    Args:
        repo_path: Path to the Airbyte monorepo
        connector_name: Technical name of the connector (e.g., "source-faker")

    Returns:
        The connector's metadata dict (the 'data' section), or None if not found

    Example:
        >>> metadata = get_connector_metadata("/path/to/airbyte", "source-faker")
        >>> metadata.get("supportLevel")
        'certified'
    """
    repo_path = Path(repo_path)
    connector_dir = repo_path / CONNECTOR_PATH_PREFIX / connector_name
    metadata_file = connector_dir / METADATA_FILE_NAME

    if not metadata_file.exists():
        return None

    try:
        with open(metadata_file) as f:
            metadata = yaml.safe_load(f)
        return metadata.get("data", {})
    except Exception:
        return None


def get_connectors_by_language(
    repo_path: str | Path,
    language: ConnectorLanguage,
) -> set[str]:
    """Get set of all connector IDs for a specific language.

    This function reads connector directories to determine which connectors
    use the specified language.

    Args:
        repo_path: Path to the Airbyte monorepo
        language: Language to filter by

    Returns:
        Set of connector technical names using the specified language

    Example:
        >>> python_connectors = get_connectors_by_language(
        ...     "/path/to/airbyte", ConnectorLanguage.PYTHON
        ... )
        >>> "source-faker" in python_connectors
        True
    """
    repo_path = Path(repo_path)
    connectors_dir = repo_path / CONNECTOR_PATH_PREFIX

    if not connectors_dir.exists():
        raise ValueError(f"Connectors directory not found: {connectors_dir}")

    language_value = language.value
    connectors_by_language = set()

    # Iterate through all connector directories
    for connector_dir in connectors_dir.iterdir():
        if not connector_dir.is_dir():
            continue

        # Determine language based on file structure
        connector_name = connector_dir.name
        detected_language = _detect_connector_language(connector_dir, connector_name)

        if detected_language == language_value:
            connectors_by_language.add(connector_dir.name)

    return connectors_by_language


def get_connectors_by_type(
    repo_path: str | Path,
    connector_type: ConnectorType,
) -> set[str]:
    """Get set of all connector IDs for a specific type (source or destination).

    This function reads connector directories to determine which connectors
    match the specified type based on their metadata.yaml or name prefix.

    Args:
        repo_path: Path to the Airbyte monorepo
        connector_type: Type to filter by (source or destination)

    Returns:
        Set of connector technical names matching the specified type

    Example:
        >>> source_connectors = get_connectors_by_type(
        ...     "/path/to/airbyte", ConnectorType.SOURCE
        ... )
        >>> "source-postgres" in source_connectors
        True
    """
    repo_path = Path(repo_path)
    connectors_dir = repo_path / CONNECTOR_PATH_PREFIX

    if not connectors_dir.exists():
        raise ValueError(f"Connectors directory not found: {connectors_dir}")

    type_value = connector_type.value
    connectors_by_type = set()

    for connector_dir in connectors_dir.iterdir():
        if not connector_dir.is_dir():
            continue

        connector_name = connector_dir.name

        # First try to get type from metadata.yaml
        metadata = get_connector_metadata(repo_path, connector_name)
        if metadata:
            metadata_type = metadata.get("connectorType")
            if metadata_type == type_value:
                connectors_by_type.add(connector_name)
                continue

        # Fallback to name prefix detection
        if connector_name.startswith(f"{type_value}-"):
            connectors_by_type.add(connector_name)

    return connectors_by_type


def get_connectors_by_subtype(
    repo_path: str | Path,
    connector_subtype: ConnectorSubtype,
) -> set[str]:
    """Get set of all connector IDs for a specific subtype (api, database, file, etc.).

    This function reads connector metadata.yaml files to determine which connectors
    match the specified subtype.

    Args:
        repo_path: Path to the Airbyte monorepo
        connector_subtype: Subtype to filter by (api, database, file, custom)

    Returns:
        Set of connector technical names matching the specified subtype

    Example:
        >>> database_connectors = get_connectors_by_subtype(
        ...     "/path/to/airbyte", ConnectorSubtype.DATABASE
        ... )
        >>> "source-postgres" in database_connectors
        True
    """
    repo_path = Path(repo_path)
    connectors_dir = repo_path / CONNECTOR_PATH_PREFIX

    if not connectors_dir.exists():
        raise ValueError(f"Connectors directory not found: {connectors_dir}")

    subtype_value = connector_subtype.value
    connectors_by_subtype = set()

    for connector_dir in connectors_dir.iterdir():
        if not connector_dir.is_dir():
            continue

        connector_name = connector_dir.name
        metadata = get_connector_metadata(repo_path, connector_name)

        if metadata:
            metadata_subtype = metadata.get("connectorSubtype")
            if metadata_subtype == subtype_value:
                connectors_by_subtype.add(connector_name)

    return connectors_by_subtype


@lru_cache(maxsize=1024)
def _detect_connector_language(connector_dir: Path, connector_name: str) -> str | None:
    """Detect the language of a connector based on its file structure.

    Args:
        connector_dir: Path to the connector directory
        connector_name: Technical name of the connector

    Returns:
        Language string (python, java, low-code, manifest-only) or None
    """
    # Check for manifest-only (manifest.yaml at root)
    if (connector_dir / "manifest.yaml").is_file():
        return "manifest-only"

    # Check for low-code (manifest.yaml in source directory)
    source_dir = connector_dir / connector_name.replace("-", "_")
    if (source_dir / "manifest.yaml").is_file():
        return "low-code"

    # Check for Python (setup.py or pyproject.toml)
    if (connector_dir / "setup.py").is_file() or (
        connector_dir / "pyproject.toml"
    ).is_file():
        return "python"

    # Check for Java/Kotlin (src/main/java or src/main/kotlin)
    if (connector_dir / "src" / "main" / "java").exists() or (
        connector_dir / "src" / "main" / "kotlin"
    ).exists():
        return "java"

    return None


@lru_cache(maxsize=128)
def get_connectors_with_local_cdk(repo_path: str | Path) -> set[str]:
    """Get set of connectors using local CDK reference instead of published version.

    This function detects connectors that are configured to use a local CDK
    checkout rather than a published CDK version. The detection method differs
    by connector language:
    - Python: Checks for path-based dependency in pyproject.toml
    - Java/Kotlin: Checks for useLocalCdk=true in build.gradle files

    Args:
        repo_path: Path to the Airbyte monorepo

    Returns:
        Set of connector technical names using local CDK reference

    Example:
        >>> local_cdk_connectors = get_connectors_with_local_cdk("/path/to/airbyte")
        >>> "destination-motherduck" in local_cdk_connectors
        True
    """
    repo_path = Path(repo_path)
    connectors_dir = repo_path / CONNECTOR_PATH_PREFIX

    if not connectors_dir.exists():
        raise ValueError(f"Connectors directory not found: {connectors_dir}")

    local_cdk_connectors = set()

    # Iterate through all connector directories
    for connector_dir in connectors_dir.iterdir():
        if not connector_dir.is_dir():
            continue

        connector_name = connector_dir.name
        detected_language = _detect_connector_language(connector_dir, connector_name)

        # Check for local CDK based on language
        if detected_language in ("python", "low-code") and _has_local_cdk_python(
            connector_dir
        ):
            # Python connectors: check pyproject.toml for path-based CDK dependency
            local_cdk_connectors.add(connector_name)
        elif detected_language == "java" and _has_local_cdk_java(connector_dir):
            # Java/Kotlin connectors: check build.gradle for useLocalCdk=true
            local_cdk_connectors.add(connector_name)

    return local_cdk_connectors


def _has_local_cdk_python(connector_dir: Path) -> bool:
    """Check if a Python connector uses local CDK reference.

    Args:
        connector_dir: Path to the connector directory

    Returns:
        True if connector uses local CDK reference
    """
    pyproject_file = connector_dir / "pyproject.toml"
    if not pyproject_file.exists():
        return False

    try:
        content = pyproject_file.read_text()
        # Look for path-based airbyte-cdk dependency
        # Pattern: airbyte-cdk = { path = "..." } or airbyte-cdk = {path = "..."}
        return bool(re.search(r"airbyte-cdk\s*=\s*\{[^}]*path\s*=", content))
    except Exception:
        return False


def _has_local_cdk_java(connector_dir: Path) -> bool:
    """Check if a Java/Kotlin connector uses local CDK reference.

    Mirrors the implementation from airbyte-ci/connectors/connector_ops/connector_ops/utils.py

    Args:
        connector_dir: Path to the connector directory

    Returns:
        True if connector uses local CDK reference
    """
    # Check both build.gradle and build.gradle.kts
    for build_file_name in ("build.gradle", "build.gradle.kts"):
        build_file = connector_dir / build_file_name
        if not build_file.exists():
            continue

        try:
            # Read file and strip inline comments
            contents = "\n".join(
                [
                    line.split("//")[0]  # Remove inline comments
                    for line in build_file.read_text().split("\n")
                ]
            )
            # Remove spaces and check for useLocalCdk=true
            contents = contents.replace(" ", "")
            if "useLocalCdk=true" in contents:
                return True
        except Exception:
            continue

    return False


@dataclass
class ConnectorListResult:
    """Result of listing connectors with filters."""

    connectors: list[str]
    count: int


def list_connectors(
    repo_path: str | Path,
    certified: bool | None = None,
    modified: bool | None = None,
    language_filter: set[str] | None = None,
    language_exclude: set[str] | None = None,
    connector_type: str | None = None,
    connector_subtype: str | None = None,
    base_ref: str | None = None,
    head_ref: str | None = None,
    pr_number: int | None = None,
    pr_owner: str | None = None,
    pr_repo: str | None = None,
    gh_token: str | None = None,
) -> ConnectorListResult:
    """List connectors in the Airbyte monorepo with flexible filtering.

    This is the core capability function that encapsulates all filtering logic.
    Both CLI and MCP layers should use this function.

    When `modified` filtering is requested and both `gh_token` and full PR
    context (`pr_number`, `pr_owner`, `pr_repo`) are provided, the
    GitHub API is used to determine changed files — this is the most reliable
    method and avoids shallow-clone pitfalls.  Falls back to local `git diff`
    when the token is not provided or PR context is incomplete.

    Args:
        repo_path: Path to the Airbyte monorepo
        certified: Filter by certification status (True=certified only,
            False=non-certified only, None=all)
        modified: Filter by modification status (True=modified only,
            False=not-modified only, None=all)
        language_filter: Set of languages to include (python, java, low-code, manifest-only)
        language_exclude: Set of languages to exclude (mutually exclusive with language_filter)
        connector_type: Filter by connector type (source, destination, or None for all)
        connector_subtype: Filter by connector subtype (api, database, file, custom, or None for all)
        base_ref: Base git reference for modification detection (default: GIT_DEFAULT_BRANCH, e.g. "origin/master")
        head_ref: Head git reference for modification detection (default: "HEAD")
        pr_number: Pull request number (enables GitHub API path for modification detection)
        pr_owner: Repository owner for PR (e.g. "airbytehq")
        pr_repo: Repository name for PR (e.g. "airbyte")
        gh_token: GitHub API token. When provided together with PR context,
            the GitHub API is used instead of local git diff.

    Returns:
        ConnectorListResult with sorted list of connector names and count

    Raises:
        ValueError: If both language_filter and language_exclude are provided
    """
    # Validate mutual exclusivity of language filters
    if language_filter is not None and language_exclude is not None:
        raise ValueError(
            "Cannot specify both language_filter and language_exclude. "
            "Only one language filter parameter is accepted."
        )

    # Start with all connectors
    result = get_all_connectors(repo_path)

    # Apply certified filter
    if certified is not None:
        certified_set = get_certified_connectors(repo_path)
        if certified:
            # Include only certified
            result &= certified_set
        else:
            # Include only non-certified
            result -= certified_set

    # Apply modified filter
    if modified is not None:
        changed_set: set[str] | None = None

        # Use GitHub API when token and full PR context are explicitly provided
        if (
            gh_token is not None
            and pr_number is not None
            and pr_owner is not None
            and pr_repo is not None
        ):
            try:
                changed_set = set(
                    get_modified_connectors_from_github(
                        pr_number, pr_owner, pr_repo, gh_token=gh_token
                    )
                )
            except (GitHubAPIError, requests.RequestException):
                logger.warning(
                    "GitHub API call failed for PR %s/%s#%d; "
                    "falling back to local git diff",
                    pr_owner,
                    pr_repo,
                    pr_number,
                    exc_info=True,
                )

        # Fallback to local git diff
        if changed_set is None:
            base = base_ref if base_ref is not None else GIT_DEFAULT_BRANCH
            head = head_ref if head_ref is not None else "HEAD"
            changed_set = set(get_modified_connectors(repo_path, base, head))

        if modified:
            # Include only modified
            result &= changed_set
        else:
            # Include only not-modified
            result -= changed_set

    # Apply language include filter
    if language_filter:
        # Get connectors for all specified languages and union them
        lang_result: set[str] = set()
        for lang in language_filter:
            lang_result |= get_connectors_by_language(
                repo_path, ConnectorLanguage(lang)
            )
        result &= lang_result

    # Apply language exclude filter
    if language_exclude:
        # Get connectors for all specified languages and exclude them
        for lang in language_exclude:
            excluded = get_connectors_by_language(repo_path, ConnectorLanguage(lang))
            result -= excluded

    # Apply connector type filter
    if connector_type is not None:
        type_set = get_connectors_by_type(repo_path, ConnectorType(connector_type))
        result &= type_set

    # Apply connector subtype filter
    if connector_subtype is not None:
        subtype_set = get_connectors_by_subtype(
            repo_path, ConnectorSubtype(connector_subtype)
        )
        result &= subtype_set

    return ConnectorListResult(
        connectors=sorted(result),
        count=len(result),
    )
