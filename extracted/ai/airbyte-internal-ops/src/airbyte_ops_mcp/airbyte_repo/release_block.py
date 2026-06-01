# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Release block operations for connectors in the Airbyte monorepo.

This module provides functions to create, remove, and list `block-release.yaml`
marker files in connector directories. When present, a marker prevents the
publish pipeline from releasing the connector.

The marker file format:

```yaml
reason: "Version 5.0.1 yanked due to regression in OAuth flow"
yanked_version: "5.0.1"
blocked_at: "2026-04-08T15:00:00Z"
blocked_by: "aj@airbyte.io"
instructions: |
  This connector's release is blocked due to a known issue.
  ...
```
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

from airbyte_ops_mcp.airbyte_repo.list_connectors import CONNECTOR_PATH_PREFIX

logger = logging.getLogger(__name__)

BLOCK_RELEASE_FILE_NAME = "block-release.yaml"


@dataclass
class ReleaseBlockInfo:
    """Parsed content of a `block-release.yaml` marker file."""

    connector_name: str
    reason: str
    yanked_version: str | None = None
    blocked_at: str | None = None
    blocked_by: str | None = None
    instructions: str | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to a dictionary for JSON serialization."""
        result: dict[str, Any] = {
            "connector_name": self.connector_name,
            "reason": self.reason,
        }
        if self.yanked_version:
            result["yanked_version"] = self.yanked_version
        if self.blocked_at:
            result["blocked_at"] = self.blocked_at
        if self.blocked_by:
            result["blocked_by"] = self.blocked_by
        if self.instructions:
            result["instructions"] = self.instructions
        return result


@dataclass
class ReleaseBlockResult:
    """Result of a release block add/clear operation."""

    connector_name: str
    action: str  # "add" or "clear"
    success: bool
    message: str
    block_file_path: str | None = None
    block_file_data: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to a dictionary for JSON serialization."""
        return {
            "connector_name": self.connector_name,
            "action": self.action,
            "success": self.success,
            "message": self.message,
            "block_file_path": self.block_file_path,
            "block_file_data": self.block_file_data,
        }


@dataclass
class ReleaseBlockListResult:
    """Result of listing blocked connectors."""

    blocked_connectors: list[ReleaseBlockInfo] = field(default_factory=list)
    count: int = 0

    def to_dict(self) -> dict[str, Any]:
        """Convert to a dictionary for JSON serialization."""
        return {
            "blocked_connectors": [b.to_dict() for b in self.blocked_connectors],
            "count": self.count,
        }


def _get_block_file_path(repo_path: str | Path, connector_name: str) -> Path:
    """Get the path to a connector's `block-release.yaml` file."""
    return (
        Path(repo_path)
        / CONNECTOR_PATH_PREFIX
        / connector_name
        / BLOCK_RELEASE_FILE_NAME
    )


def _validate_connector_dir(repo_path: str | Path, connector_name: str) -> Path:
    """Validate that a connector directory exists and return its path.

    Args:
        repo_path: Path to the Airbyte monorepo.
        connector_name: Technical name of the connector (e.g., `source-faker`).

    Returns:
        Path to the connector directory.

    Raises:
        ValueError: If the connector directory does not exist.
    """
    connector_dir = Path(repo_path) / CONNECTOR_PATH_PREFIX / connector_name
    if not connector_dir.is_dir():
        raise ValueError(
            f"Connector directory not found: {connector_dir}. "
            f"Make sure '{connector_name}' is a valid connector name."
        )
    return connector_dir


def add_release_block(
    repo_path: str | Path,
    connector_name: str,
    reason: str,
    yanked_version: str | None = None,
    blocked_by: str | None = None,
) -> ReleaseBlockResult:
    """Create a `block-release.yaml` marker file for a connector.

    Args:
        repo_path: Path to the Airbyte monorepo.
        connector_name: Technical name of the connector (e.g., `source-faker`).
        reason: Human-readable reason for blocking.
        yanked_version: Optional version that was yanked.
        blocked_by: Optional email or identifier of the person requesting the block.

    Returns:
        `ReleaseBlockResult` with details of the operation.
    """
    try:
        _validate_connector_dir(repo_path, connector_name)
    except ValueError as e:
        return ReleaseBlockResult(
            connector_name=connector_name,
            action="add",
            success=False,
            message=str(e),
        )

    block_file = _get_block_file_path(repo_path, connector_name)

    if block_file.exists():
        return ReleaseBlockResult(
            connector_name=connector_name,
            action="add",
            success=False,
            message=f"Release block already exists for {connector_name}.",
            block_file_path=str(block_file),
        )

    timestamp = datetime.now(tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    block_content: dict[str, Any] = {
        "reason": reason,
    }
    if yanked_version:
        block_content["yanked_version"] = yanked_version
    block_content["blocked_at"] = timestamp
    if blocked_by:
        block_content["blocked_by"] = blocked_by
    block_content["instructions"] = (
        "This connector's release is blocked due to a known issue.\n"
        "The broken code from the yanked version still lives on master.\n"
        "To unblock, use the 'block-release.yml' workflow with action=unblock\n"
        "or merge a PR that deletes this file.\n"
    )

    block_file.write_text(
        yaml.dump(block_content, default_flow_style=False, sort_keys=False)
    )

    logger.info("Added release block for %s: %s", connector_name, reason)

    return ReleaseBlockResult(
        connector_name=connector_name,
        action="add",
        success=True,
        message=f"Successfully added release block for {connector_name}.",
        block_file_path=str(block_file),
        block_file_data=block_content,
    )


def clear_release_block(
    repo_path: str | Path,
    connector_name: str,
) -> ReleaseBlockResult:
    """Remove the `block-release.yaml` marker file for a connector.

    Args:
        repo_path: Path to the Airbyte monorepo.
        connector_name: Technical name of the connector (e.g., `source-faker`).

    Returns:
        `ReleaseBlockResult` with details of the operation.
    """
    try:
        _validate_connector_dir(repo_path, connector_name)
    except ValueError as e:
        return ReleaseBlockResult(
            connector_name=connector_name,
            action="clear",
            success=False,
            message=str(e),
        )

    block_file = _get_block_file_path(repo_path, connector_name)

    if not block_file.exists():
        return ReleaseBlockResult(
            connector_name=connector_name,
            action="clear",
            success=False,
            message=f"No release block found for {connector_name}.",
        )

    previous_contents = block_file.read_text()
    try:
        previous_data: dict[str, Any] | None = yaml.safe_load(previous_contents)
        if not isinstance(previous_data, dict):
            previous_data = None
    except Exception:
        previous_data = None

    block_file.unlink()

    logger.info(
        "Cleared release block for %s. Previous marker contents:\n%s",
        connector_name,
        previous_contents,
    )

    return ReleaseBlockResult(
        connector_name=connector_name,
        action="clear",
        success=True,
        message=f"Successfully cleared release block for {connector_name}.",
        block_file_path=str(block_file),
        block_file_data=previous_data,
    )


def get_release_block(
    repo_path: str | Path,
    connector_name: str,
) -> ReleaseBlockInfo | None:
    """Read the release block info for a single connector.

    Args:
        repo_path: Path to the Airbyte monorepo.
        connector_name: Technical name of the connector.

    Returns:
        `ReleaseBlockInfo` if a block exists, `None` otherwise.
    """
    block_file = _get_block_file_path(repo_path, connector_name)

    if not block_file.exists():
        return None

    try:
        content = yaml.safe_load(block_file.read_text())
    except Exception:
        logger.warning("Failed to parse %s", block_file, exc_info=True)
        return ReleaseBlockInfo(
            connector_name=connector_name,
            reason="(unable to parse block-release.yaml)",
        )

    if not isinstance(content, dict):
        return ReleaseBlockInfo(
            connector_name=connector_name,
            reason="(invalid block-release.yaml format)",
        )

    return ReleaseBlockInfo(
        connector_name=connector_name,
        reason=content.get("reason", "(no reason provided)"),
        yanked_version=content.get("yanked_version"),
        blocked_at=content.get("blocked_at"),
        blocked_by=content.get("blocked_by"),
        instructions=content.get("instructions"),
    )


def list_release_blocks(
    repo_path: str | Path,
) -> ReleaseBlockListResult:
    """Scan the monorepo for all connectors with a `block-release.yaml` marker.

    Args:
        repo_path: Path to the Airbyte monorepo.

    Returns:
        `ReleaseBlockListResult` with all blocked connectors.
    """
    connectors_dir = Path(repo_path) / CONNECTOR_PATH_PREFIX

    if not connectors_dir.is_dir():
        logger.warning("Connectors directory not found: %s", connectors_dir)
        return ReleaseBlockListResult()

    blocked: list[ReleaseBlockInfo] = []

    for connector_dir in sorted(connectors_dir.iterdir()):
        if not connector_dir.is_dir():
            continue

        block_file = connector_dir / BLOCK_RELEASE_FILE_NAME
        if not block_file.exists():
            continue

        info = get_release_block(repo_path, connector_dir.name)
        if info is not None:
            blocked.append(info)

    return ReleaseBlockListResult(
        blocked_connectors=blocked,
        count=len(blocked),
    )
