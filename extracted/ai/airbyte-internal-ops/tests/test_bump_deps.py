# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Unit tests for the bump_deps module."""

from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from airbyte_ops_mcp.airbyte_repo.bump_deps import (
    DepsError,
    _get_outdated_packages,
    bump_deps,
)


def _make_connector(
    tmpdir: str,
    connector_name: str,
    *,
    has_lock: bool = True,
) -> Path:
    """Create a minimal connector directory with pyproject.toml and optional lock file."""
    connector = Path(tmpdir) / "airbyte-integrations" / "connectors" / connector_name
    connector.mkdir(parents=True)
    (connector / "pyproject.toml").write_text(
        '[tool.poetry]\nname = "test"\nversion = "0.1.0"\n'
        '\n[tool.poetry.dependencies]\npython = "^3.9"\n'
        'airbyte-cdk = ">=7.0,<8.0"\nrequests = "*"\npydantic = "^2.0"\n'
    )
    if has_lock:
        (connector / "poetry.lock").write_text("# lock content v1\n")
    return connector


# ---------------------------------------------------------------------------
# Non-Poetry connectors are a no-op
# ---------------------------------------------------------------------------


@pytest.mark.unit
@patch("airbyte_ops_mcp.airbyte_repo.bump_deps._detect_connector_language")
def test_manifest_only_is_noop(mock_lang):
    mock_lang.return_value = "manifest-only"
    with tempfile.TemporaryDirectory() as tmpdir:
        connector = Path(tmpdir) / "airbyte-integrations" / "connectors" / "source-test"
        connector.mkdir(parents=True)
        result = bump_deps(tmpdir, "source-test")

    assert result.updated is False
    assert "does not use Poetry" in result.message


@pytest.mark.unit
@patch("airbyte_ops_mcp.airbyte_repo.bump_deps._detect_connector_language")
def test_java_is_noop(mock_lang):
    mock_lang.return_value = "java"
    with tempfile.TemporaryDirectory() as tmpdir:
        connector = Path(tmpdir) / "airbyte-integrations" / "connectors" / "source-test"
        connector.mkdir(parents=True)
        result = bump_deps(tmpdir, "source-test")

    assert result.updated is False


# ---------------------------------------------------------------------------
# Missing poetry.lock returns early
# ---------------------------------------------------------------------------


@pytest.mark.unit
@patch("airbyte_ops_mcp.airbyte_repo.bump_deps._detect_connector_language")
def test_no_lock_file_returns_early(mock_lang):
    mock_lang.return_value = "python"
    with tempfile.TemporaryDirectory() as tmpdir:
        _make_connector(tmpdir, "source-test", has_lock=False)
        result = bump_deps(tmpdir, "source-test")

    assert result.updated is False
    assert "No poetry.lock" in result.message


# ---------------------------------------------------------------------------
# Dry run reports correct files
# ---------------------------------------------------------------------------


@pytest.mark.unit
@patch("airbyte_ops_mcp.airbyte_repo.bump_deps._detect_connector_language")
def test_dry_run_reports_lock_file(mock_lang):
    mock_lang.return_value = "python"
    with tempfile.TemporaryDirectory() as tmpdir:
        _make_connector(tmpdir, "source-test")
        result = bump_deps(tmpdir, "source-test", dry_run=True)

    assert result.dry_run is True
    assert len(result.files_modified) == 1
    assert "poetry.lock" in result.files_modified[0]
    assert "source-test" in result.files_modified[0]


# ---------------------------------------------------------------------------
# _get_outdated_packages
# ---------------------------------------------------------------------------


OUTDATED_OUTPUT = (
    "airbyte-cdk                         (!) 7.10.1    7.15.0      \n"
    "pytest                              (!) 8.4.2     9.0.2       \n"
    "responses                           (!) 0.23.3    0.26.0      \n"
)


@pytest.mark.unit
@patch("airbyte_ops_mcp.airbyte_repo.bump_deps.subprocess.run")
def test_get_outdated_packages_parses_output(mock_run):
    mock_run.return_value = subprocess.CompletedProcess(
        args=[], returncode=0, stdout=OUTDATED_OUTPUT, stderr=""
    )
    result = _get_outdated_packages(Path("/fake/connector"), "source-test")
    assert result == ["airbyte-cdk", "pytest", "responses"]
    call_args = mock_run.call_args[0][0]
    assert call_args == ["poetry", "show", "--outdated", "--top-level", "--no-ansi"]


@pytest.mark.unit
@patch("airbyte_ops_mcp.airbyte_repo.bump_deps.subprocess.run")
def test_get_outdated_packages_empty(mock_run):
    mock_run.return_value = subprocess.CompletedProcess(
        args=[], returncode=0, stdout="", stderr=""
    )
    result = _get_outdated_packages(Path("/fake/connector"), "source-test")
    assert result == []


@pytest.mark.unit
@patch("airbyte_ops_mcp.airbyte_repo.bump_deps.subprocess.run")
def test_get_outdated_packages_failure_raises(mock_run):
    mock_run.side_effect = subprocess.CalledProcessError(1, "poetry", stderr="boom")
    with pytest.raises(DepsError, match="failed"):
        _get_outdated_packages(Path("/fake/connector"), "source-test")


# ---------------------------------------------------------------------------
# Actual update uses outdated-package check instead of file diff
# ---------------------------------------------------------------------------


@pytest.mark.unit
@patch("airbyte_ops_mcp.airbyte_repo.bump_deps._detect_connector_language")
@patch("airbyte_ops_mcp.airbyte_repo.bump_deps._get_outdated_packages")
@patch("airbyte_ops_mcp.airbyte_repo.bump_deps.subprocess.run")
def test_no_outdated_packages_skips_update(mock_run, mock_outdated, mock_lang):
    """When no packages are outdated, skip poetry update entirely -> updated=False."""
    mock_lang.return_value = "python"
    mock_outdated.return_value = []

    with tempfile.TemporaryDirectory() as tmpdir:
        _make_connector(tmpdir, "source-test")
        result = bump_deps(tmpdir, "source-test")

    assert result.updated is False
    assert result.outdated_packages == []
    assert "already up to date" in result.message
    # poetry update --lock should NOT have been called
    mock_run.assert_not_called()


@pytest.mark.unit
@patch("airbyte_ops_mcp.airbyte_repo.bump_deps._detect_connector_language")
@patch("airbyte_ops_mcp.airbyte_repo.bump_deps._get_outdated_packages")
@patch("airbyte_ops_mcp.airbyte_repo.bump_deps.subprocess.run")
def test_outdated_packages_triggers_update(mock_run, mock_outdated, mock_lang):
    """When packages are outdated, run poetry update and report updated=True."""
    mock_lang.return_value = "python"
    mock_outdated.return_value = ["airbyte-cdk", "requests"]
    mock_run.return_value = subprocess.CompletedProcess(args=[], returncode=0)

    with tempfile.TemporaryDirectory() as tmpdir:
        _make_connector(tmpdir, "source-test")
        result = bump_deps(tmpdir, "source-test")

    assert result.updated is True
    assert result.outdated_packages == ["airbyte-cdk", "requests"]
    assert len(result.files_modified) == 1
    # Verify poetry update --lock was called
    call_args = mock_run.call_args[0][0]
    assert call_args == ["poetry", "update", "--lock"]


# ---------------------------------------------------------------------------
# Subprocess failure raises DepsError
# ---------------------------------------------------------------------------


@pytest.mark.unit
@patch("airbyte_ops_mcp.airbyte_repo.bump_deps._detect_connector_language")
@patch("airbyte_ops_mcp.airbyte_repo.bump_deps._get_outdated_packages")
@patch("airbyte_ops_mcp.airbyte_repo.bump_deps.subprocess.run")
def test_poetry_update_failure_raises(mock_run, mock_outdated, mock_lang):
    mock_lang.return_value = "python"
    mock_outdated.return_value = ["airbyte-cdk"]
    mock_run.side_effect = subprocess.CalledProcessError(1, "poetry", stderr="boom")

    with tempfile.TemporaryDirectory() as tmpdir:
        _make_connector(tmpdir, "source-test")
        with pytest.raises(DepsError, match="failed"):
            bump_deps(tmpdir, "source-test")
