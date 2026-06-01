# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Base image bumping utilities for Airbyte connectors.

This module provides functionality to update the base Docker image
reference in a connector's `metadata.yaml` file to the latest stable version.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path

import semver
import yaml

from airbyte_ops_mcp.airbyte_repo.bump_version import (
    ConnectorNotFoundError,
    get_connector_path,
)
from airbyte_ops_mcp.airbyte_repo.list_connectors import (
    CONNECTOR_PATH_PREFIX,
    METADATA_FILE_NAME,
)
from airbyte_ops_mcp.docker_hub import get_docker_hub_tags_and_digests

logger = logging.getLogger(__name__)


class BaseImageError(Exception):
    """Base exception for base image operations."""


class NoBaseImageInMetadataError(BaseImageError):
    """Raised when no base image address is found in `metadata.yaml`."""


class BaseImageParseError(BaseImageError):
    """Raised when the current base image address cannot be parsed."""


class NoStableVersionFoundError(BaseImageError):
    """Raised when no stable base image version is found on DockerHub."""


@dataclass
class BumpBaseImageResult:
    """Result of a base image bump operation."""

    connector: str
    previous_base_image: str | None
    new_base_image: str | None
    updated: bool
    dry_run: bool
    files_modified: list[str] = field(default_factory=list)
    message: str = ""


def _extract_docker_repo_from_base_image(base_image_address: str) -> str:
    """Extract the Docker image repository from a base image address.

    Given `docker.io/airbyte/python-connector-base:1.2.3@sha256:...`,
    returns `airbyte/python-connector-base`.

    Raises:
        BaseImageParseError: If the Docker image repository cannot be parsed
            from the address.
    """
    try:
        # Strip scheme prefix (e.g. "docker.io/")
        without_digest = base_image_address.split("@")[0]
        without_tag = without_digest.rsplit(":", 1)[0]
        # Remove registry prefix like "docker.io/"
        parts = without_tag.split("/", 1)
        if len(parts) == 2 and "." in parts[0]:
            # Has registry prefix like docker.io/airbyte/repo
            return parts[1]
        return without_tag
    except (IndexError, ValueError) as exc:
        raise BaseImageParseError(
            f"Cannot parse Docker image repository from base image address: '{base_image_address}'."
        ) from exc


def _parse_stable_tags(
    tags_and_digests: dict[str, str],
) -> list[tuple[semver.VersionInfo, str, str]]:
    """Parse all stable (non-prerelease) semver tags with their digests."""
    result: list[tuple[semver.VersionInfo, str, str]] = []
    for tag, digest in tags_and_digests.items():
        try:
            version = semver.VersionInfo.parse(tag)
        except ValueError:
            continue
        if version.prerelease:
            continue
        if digest:
            result.append((version, tag, digest))
    return result


def _find_latest_stable_tag(
    tags_and_digests: dict[str, str],
    *,
    major: int | None = None,
) -> tuple[str, str] | None:
    """Find the latest stable (non-prerelease) semver tag and its digest.

    Args:
        tags_and_digests: Mapping of tag strings to digest strings.
        major: If provided, only consider tags with this major version.
            This enables "respect major version boundary" behaviour.

    Returns:
        A `(tag, digest)` tuple for the latest stable version, or `None`
        if no matching stable version is found.
    """
    valid_versions = _parse_stable_tags(tags_and_digests)

    if major is not None:
        valid_versions = [v for v in valid_versions if v[0].major == major]

    if not valid_versions:
        return None

    best = max(valid_versions, key=lambda v: v[0])
    return best[1], best[2]


def _extract_major_from_base_image(base_image_address: str) -> int | None:
    """Extract the major version from a base image address.

    Accepts addresses like `docker.io/repo:1.2.3@sha256:...` and returns the
    major component (`1` in this example), or `None` if parsing fails.
    """
    # The tag sits between the last ':' and an optional '@'
    try:
        without_digest = base_image_address.split("@")[0]
        tag = without_digest.rsplit(":", 1)[1]
        version = semver.VersionInfo.parse(tag)
    except (IndexError, ValueError):
        return None
    return version.major


def get_latest_base_image_address(
    docker_repo: str,
    *,
    current_major: int | None = None,
) -> str:
    """Fetch the latest stable base image address from DockerHub.

    The returned address has the form `docker.io/<repo>:<tag>@<digest>`.

    Args:
        docker_repo: Docker image repository (e.g. `airbyte/python-connector-base`).
        current_major: If provided, restrict to tags sharing this major version
            ("respect major version boundary" mode).  Pass `None` to get the
            absolute latest tag regardless of major version.

    Raises:
        NoStableVersionFoundError: If no stable version tag is found.
    """
    tags_and_digests = get_docker_hub_tags_and_digests(
        docker_repo, retries=3, wait_sec=10
    )

    result = _find_latest_stable_tag(tags_and_digests, major=current_major)
    if result is None:
        raise NoStableVersionFoundError(
            f"No stable version found for Docker image '{docker_repo}'"
            + (
                f" with major version {current_major}."
                if current_major is not None
                else "."
            )
        )

    tag, digest = result
    return f"docker.io/{docker_repo}:{tag}@{digest}"


def bump_base_image(
    repo_path: str | Path,
    connector_name: str,
    force_latest: bool = False,
    dry_run: bool = False,
) -> BumpBaseImageResult:
    """Update the base image in a connector's `metadata.yaml`.

    The base image repository is derived from the existing address in
    `metadata.yaml`, so the connector must already have a base image set.

    Two modes are supported:

    * **Default** (`force_latest=False`): Bump to the latest stable tag
      that shares the same *major* version as the current base image.
      This treats major version bumps as breaking-change boundaries.
    * **Force-latest** (`force_latest=True`): Bump to the absolute latest
      stable tag regardless of semver / major version.

    Args:
        repo_path: Path to the Airbyte monorepo.
        connector_name: Technical name of the connector (e.g. `source-github`).
        force_latest: If `True`, ignore the major-version boundary and bump
            to the absolute latest stable base image.
        dry_run: If `True`, report what would change without modifying files.

    Returns:
        A `BumpBaseImageResult` describing the outcome.

    Raises:
        ConnectorNotFoundError: If the connector directory does not exist.
        NoBaseImageInMetadataError: If no base image is present in `metadata.yaml`.
        BaseImageParseError: If the repository or version cannot be parsed
            from the current base image address.
        BaseImageError: If the current base image tag cannot be parsed as
            semver in default mode (pass `--force-latest` to bypass).
        NoStableVersionFoundError: If no stable base image version is found.
    """
    repo_path = Path(repo_path)
    connector_path = get_connector_path(repo_path, connector_name)

    # Read current metadata
    metadata_file = connector_path / METADATA_FILE_NAME
    if not metadata_file.exists():
        raise ConnectorNotFoundError(
            f"metadata.yaml not found for connector '{connector_name}'."
        )

    raw_metadata = metadata_file.read_text()
    metadata = yaml.safe_load(raw_metadata)

    current_base_image = (
        metadata.get("data", {}).get("connectorBuildOptions", {}).get("baseImage")
    )

    if current_base_image is None:
        raise NoBaseImageInMetadataError(
            f"No base image address found in metadata.yaml for connector "
            f"'{connector_name}'."
        )

    # Derive the Docker image repository from the existing base image address
    docker_repo = _extract_docker_repo_from_base_image(current_base_image)

    # Determine major-version constraint for default mode
    current_major: int | None = None
    if not force_latest and current_base_image is not None:
        current_major = _extract_major_from_base_image(current_base_image)
        if current_major is None:
            raise BaseImageError(
                f"Cannot parse major version from current base image "
                f"'{current_base_image}'. Use --force-latest to bump to the "
                f"absolute latest version regardless of major version."
            )

    # Fetch latest base image (constrained to current major when not --force-latest)
    latest_base_image = get_latest_base_image_address(
        docker_repo,
        current_major=current_major,
    )

    # Check if already up to date
    if current_base_image == latest_base_image:
        return BumpBaseImageResult(
            connector=connector_name,
            previous_base_image=current_base_image,
            new_base_image=latest_base_image,
            updated=False,
            dry_run=dry_run,
            message=f"Base image is already up to date: {latest_base_image}",
        )

    if dry_run:
        return BumpBaseImageResult(
            connector=connector_name,
            previous_base_image=current_base_image,
            new_base_image=latest_base_image,
            updated=False,
            dry_run=True,
            files_modified=[
                f"{CONNECTOR_PATH_PREFIX}/{connector_name}/{METADATA_FILE_NAME}"
            ],
            message="Dry run: would update base image.",
        )

    # Update metadata.yaml
    new_raw_metadata = raw_metadata.replace(current_base_image, latest_base_image)
    metadata_file.write_text(new_raw_metadata)

    return BumpBaseImageResult(
        connector=connector_name,
        previous_base_image=current_base_image,
        new_base_image=latest_base_image,
        updated=True,
        dry_run=False,
        files_modified=[
            f"{CONNECTOR_PATH_PREFIX}/{connector_name}/{METADATA_FILE_NAME}"
        ],
        message=f"Updated base image to {latest_base_image}.",
    )
