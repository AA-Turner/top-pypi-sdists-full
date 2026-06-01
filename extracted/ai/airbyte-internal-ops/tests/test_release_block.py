# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Unit tests for the release_block module."""

from __future__ import annotations

import tempfile
from pathlib import Path

import pytest
import yaml

from airbyte_ops_mcp.airbyte_repo.list_connectors import CONNECTOR_PATH_PREFIX
from airbyte_ops_mcp.airbyte_repo.release_block import (
    BLOCK_RELEASE_FILE_NAME,
    ReleaseBlockInfo,
    ReleaseBlockListResult,
    ReleaseBlockResult,
    add_release_block,
    clear_release_block,
    get_release_block,
    list_release_blocks,
)


def _create_fake_repo(tmpdir: str, connector_names: list[str]) -> Path:
    """Create a minimal fake repo structure with connector directories."""
    repo_path = Path(tmpdir)
    connectors_dir = repo_path / CONNECTOR_PATH_PREFIX
    connectors_dir.mkdir(parents=True, exist_ok=True)
    for name in connector_names:
        (connectors_dir / name).mkdir(parents=True, exist_ok=True)
    return repo_path


# ---------- add_release_block tests ----------


@pytest.mark.unit
def test_add_release_block_success() -> None:
    """Test successfully adding a release block marker."""
    with tempfile.TemporaryDirectory() as tmpdir:
        repo = _create_fake_repo(tmpdir, ["source-faker"])
        result = add_release_block(
            repo_path=str(repo),
            connector_name="source-faker",
            reason="Version 5.0.1 yanked due to regression",
            yanked_version="5.0.1",
            blocked_by="aj@airbyte.io",
        )

        assert result.success is True
        assert result.action == "add"
        assert "source-faker" in result.message

        # Verify the file was created with correct content
        block_file = (
            repo / CONNECTOR_PATH_PREFIX / "source-faker" / BLOCK_RELEASE_FILE_NAME
        )
        assert block_file.exists()

        content = yaml.safe_load(block_file.read_text())
        assert content["reason"] == "Version 5.0.1 yanked due to regression"
        assert content["yanked_version"] == "5.0.1"
        assert content["blocked_by"] == "aj@airbyte.io"
        assert "blocked_at" in content
        assert "instructions" in content


@pytest.mark.unit
def test_add_release_block_already_exists() -> None:
    """Test adding a release block when one already exists."""
    with tempfile.TemporaryDirectory() as tmpdir:
        repo = _create_fake_repo(tmpdir, ["source-faker"])

        # Create the block first
        block_file = (
            repo / CONNECTOR_PATH_PREFIX / "source-faker" / BLOCK_RELEASE_FILE_NAME
        )
        block_file.write_text("reason: existing block\n")

        result = add_release_block(
            repo_path=str(repo),
            connector_name="source-faker",
            reason="New reason",
        )

        assert result.success is False
        assert "already exists" in result.message


@pytest.mark.unit
def test_add_release_block_invalid_connector() -> None:
    """Test adding a release block for a nonexistent connector."""
    with tempfile.TemporaryDirectory() as tmpdir:
        repo = _create_fake_repo(tmpdir, [])
        result = add_release_block(
            repo_path=str(repo),
            connector_name="source-nonexistent",
            reason="Some reason",
        )

        assert result.success is False
        assert "not found" in result.message


@pytest.mark.unit
def test_add_release_block_without_optional_fields() -> None:
    """Test adding a release block without yanked_version and blocked_by."""
    with tempfile.TemporaryDirectory() as tmpdir:
        repo = _create_fake_repo(tmpdir, ["source-faker"])
        result = add_release_block(
            repo_path=str(repo),
            connector_name="source-faker",
            reason="General block reason",
        )

        assert result.success is True

        block_file = (
            repo / CONNECTOR_PATH_PREFIX / "source-faker" / BLOCK_RELEASE_FILE_NAME
        )
        content = yaml.safe_load(block_file.read_text())
        assert content["reason"] == "General block reason"
        assert "yanked_version" not in content
        assert "blocked_by" not in content


# ---------- clear_release_block tests ----------


@pytest.mark.unit
def test_clear_release_block_success() -> None:
    """Test successfully clearing a release block."""
    with tempfile.TemporaryDirectory() as tmpdir:
        repo = _create_fake_repo(tmpdir, ["source-faker"])

        # Create the block first
        block_file = (
            repo / CONNECTOR_PATH_PREFIX / "source-faker" / BLOCK_RELEASE_FILE_NAME
        )
        block_file.write_text("reason: test block\n")

        result = clear_release_block(
            repo_path=str(repo),
            connector_name="source-faker",
        )

        assert result.success is True
        assert result.action == "clear"
        assert not block_file.exists()


@pytest.mark.unit
def test_clear_release_block_no_block() -> None:
    """Test clearing a release block when none exists."""
    with tempfile.TemporaryDirectory() as tmpdir:
        repo = _create_fake_repo(tmpdir, ["source-faker"])
        result = clear_release_block(
            repo_path=str(repo),
            connector_name="source-faker",
        )

        assert result.success is False
        assert "No release block" in result.message


@pytest.mark.unit
def test_clear_release_block_invalid_connector() -> None:
    """Test clearing a release block for a nonexistent connector."""
    with tempfile.TemporaryDirectory() as tmpdir:
        repo = _create_fake_repo(tmpdir, [])
        result = clear_release_block(
            repo_path=str(repo),
            connector_name="source-nonexistent",
        )

        assert result.success is False
        assert "not found" in result.message


# ---------- get_release_block tests ----------


@pytest.mark.unit
def test_get_release_block_exists() -> None:
    """Test reading an existing release block."""
    with tempfile.TemporaryDirectory() as tmpdir:
        repo = _create_fake_repo(tmpdir, ["source-faker"])

        block_content = {
            "reason": "Yanked version 5.0.1",
            "yanked_version": "5.0.1",
            "blocked_at": "2026-04-08T15:00:00Z",
            "blocked_by": "aj@airbyte.io",
            "instructions": "Remove this file after fix.",
        }
        block_file = (
            repo / CONNECTOR_PATH_PREFIX / "source-faker" / BLOCK_RELEASE_FILE_NAME
        )
        block_file.write_text(yaml.dump(block_content))

        info = get_release_block(str(repo), "source-faker")

        assert info is not None
        assert info.connector_name == "source-faker"
        assert info.reason == "Yanked version 5.0.1"
        assert info.yanked_version == "5.0.1"
        assert info.blocked_at == "2026-04-08T15:00:00Z"
        assert info.blocked_by == "aj@airbyte.io"


@pytest.mark.unit
def test_get_release_block_not_exists() -> None:
    """Test reading a release block that doesn't exist."""
    with tempfile.TemporaryDirectory() as tmpdir:
        repo = _create_fake_repo(tmpdir, ["source-faker"])
        info = get_release_block(str(repo), "source-faker")
        assert info is None


@pytest.mark.unit
def test_get_release_block_invalid_yaml() -> None:
    """Test reading a release block with invalid YAML."""
    with tempfile.TemporaryDirectory() as tmpdir:
        repo = _create_fake_repo(tmpdir, ["source-faker"])
        block_file = (
            repo / CONNECTOR_PATH_PREFIX / "source-faker" / BLOCK_RELEASE_FILE_NAME
        )
        block_file.write_text("[invalid: yaml: content")

        info = get_release_block(str(repo), "source-faker")
        assert info is not None
        assert info.connector_name == "source-faker"
        assert "unable to parse" in info.reason


# ---------- list_release_blocks tests ----------


@pytest.mark.unit
def test_list_release_blocks_none() -> None:
    """Test listing when no connectors are blocked."""
    with tempfile.TemporaryDirectory() as tmpdir:
        repo = _create_fake_repo(tmpdir, ["source-faker", "source-postgres"])
        result = list_release_blocks(str(repo))

        assert result.count == 0
        assert result.blocked_connectors == []


@pytest.mark.unit
def test_list_release_blocks_some_blocked() -> None:
    """Test listing when some connectors are blocked."""
    with tempfile.TemporaryDirectory() as tmpdir:
        repo = _create_fake_repo(
            tmpdir, ["source-faker", "source-postgres", "destination-s3"]
        )

        # Block source-faker and destination-s3
        for name in ["source-faker", "destination-s3"]:
            block_file = repo / CONNECTOR_PATH_PREFIX / name / BLOCK_RELEASE_FILE_NAME
            block_file.write_text(
                yaml.dump({"reason": f"{name} is blocked", "yanked_version": "1.0.0"})
            )

        result = list_release_blocks(str(repo))

        assert result.count == 2
        names = [b.connector_name for b in result.blocked_connectors]
        assert "source-faker" in names
        assert "destination-s3" in names
        assert "source-postgres" not in names


@pytest.mark.unit
def test_list_release_blocks_missing_connectors_dir() -> None:
    """Test listing when the connectors directory doesn't exist."""
    with tempfile.TemporaryDirectory() as tmpdir:
        result = list_release_blocks(tmpdir)
        assert result.count == 0
        assert result.blocked_connectors == []


# ---------- ReleaseBlockInfo / ReleaseBlockResult serialization ----------


@pytest.mark.unit
def test_release_block_info_to_dict() -> None:
    """Test ReleaseBlockInfo.to_dict() serialization."""
    info = ReleaseBlockInfo(
        connector_name="source-faker",
        reason="Yanked",
        yanked_version="5.0.1",
        blocked_at="2026-04-08T15:00:00Z",
        blocked_by="aj@airbyte.io",
    )
    d = info.to_dict()
    assert d["connector_name"] == "source-faker"
    assert d["reason"] == "Yanked"
    assert d["yanked_version"] == "5.0.1"
    assert d["blocked_at"] == "2026-04-08T15:00:00Z"
    assert d["blocked_by"] == "aj@airbyte.io"


@pytest.mark.unit
def test_release_block_info_to_dict_minimal() -> None:
    """Test ReleaseBlockInfo.to_dict() with only required fields."""
    info = ReleaseBlockInfo(
        connector_name="source-faker",
        reason="Blocked",
    )
    d = info.to_dict()
    assert d["connector_name"] == "source-faker"
    assert d["reason"] == "Blocked"
    assert "yanked_version" not in d
    assert "blocked_at" not in d
    assert "blocked_by" not in d


@pytest.mark.unit
def test_release_block_result_to_dict() -> None:
    """Test ReleaseBlockResult.to_dict() serialization."""
    result = ReleaseBlockResult(
        connector_name="source-faker",
        action="add",
        success=True,
        message="Done",
        block_file_path="/some/path",
    )
    d = result.to_dict()
    assert d["connector_name"] == "source-faker"
    assert d["action"] == "add"
    assert d["success"] is True
    assert d["block_file_path"] == "/some/path"


@pytest.mark.unit
def test_release_block_list_result_to_dict() -> None:
    """Test ReleaseBlockListResult.to_dict() serialization."""
    result = ReleaseBlockListResult(
        blocked_connectors=[
            ReleaseBlockInfo(connector_name="source-faker", reason="Blocked"),
        ],
        count=1,
    )
    d = result.to_dict()
    assert d["count"] == 1
    assert len(d["blocked_connectors"]) == 1
    assert d["blocked_connectors"][0]["connector_name"] == "source-faker"
