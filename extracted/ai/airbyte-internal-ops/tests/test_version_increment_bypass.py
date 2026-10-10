# Copyright (c) 2025 Airbyte, Inc., all rights reserved.

"""Tests for skipping CheckVersionIncrement when only unreleased files changed."""

import subprocess
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from airbyte_ops_mcp.airbyte_repo.list_connectors import get_changed_files
from airbyte_ops_mcp.connector_qa.checks.version import (
    CheckVersionIncrement,
    _is_production_path,
)
from airbyte_ops_mcp.connector_qa.models import CheckStatus

_VERSION_MODULE = "airbyte_ops_mcp.connector_qa.checks.version.CheckVersionIncrement"
_CONNECTOR_DIR = "airbyte-integrations/connectors/source-mock"


@pytest.fixture
def mock_connector(tmp_path):
    return MagicMock(
        code_directory=str(tmp_path),
        technical_name="source-mock",
        metadata={"dockerImageTag": "1.0.0"},
    )


@pytest.mark.parametrize(
    "path, expected",
    [
        pytest.param("unit_tests/test_streams.py", False, id="unit-tests"),
        pytest.param("unit_tests/__init__.py", False, id="unit-tests-init"),
        pytest.param("integration_tests/config.json", False, id="integration-tests"),
        pytest.param("acceptance-test-config.yml", False, id="acceptance-config"),
        pytest.param("README.md", False, id="readme"),
        pytest.param("erd/source.dbml", False, id="erd"),
        pytest.param("src/test/java/Foo.java", False, id="java-tests"),
        pytest.param("src/test-integration/java/Foo.java", False, id="java-it"),
        pytest.param("metadata.yaml", True, id="metadata"),
        pytest.param("manifest.yaml", True, id="manifest"),
        pytest.param("source_mock/source.py", True, id="source-code"),
        pytest.param("pyproject.toml", True, id="pyproject"),
        pytest.param(".dockerignore", True, id="dockerignore"),
        pytest.param("build.gradle", True, id="gradle"),
        pytest.param("src/main/java/Foo.java", True, id="java-main"),
        pytest.param("unit_tests_helper.py", True, id="prefix-is-not-dir"),
        pytest.param("docs/README.md", True, id="nested-readme"),
    ],
)
def test_is_production_path(path, expected):
    assert _is_production_path(path) is expected


@patch(f"{_VERSION_MODULE}._get_master_metadata")
@patch(f"{_VERSION_MODULE}._get_changed_files")
def test_test_only_change_skips(mock_changed, mock_master, mock_connector):
    """A change limited to tests needs no version increment."""
    mock_changed.return_value = ["acceptance-test-config.yml", "unit_tests/test_x.py"]

    result = CheckVersionIncrement()._run(mock_connector)

    assert result.status == CheckStatus.SKIPPED
    assert "No production code changed" in result.message
    assert "unit_tests/test_x.py" in result.message
    mock_master.assert_not_called()


@pytest.mark.parametrize(
    "changed_files",
    [
        pytest.param(["unit_tests/test_x.py", "manifest.yaml"], id="mixed"),
        pytest.param(["metadata.yaml"], id="metadata-only"),
        pytest.param([], id="no-changes-detected"),
        pytest.param(None, id="changes-unknown"),
    ],
)
@patch(f"{_VERSION_MODULE}._get_master_metadata")
@patch(f"{_VERSION_MODULE}._get_changed_files")
def test_other_changes_still_require_increment(
    mock_changed, mock_master, mock_connector, changed_files
):
    """Anything else, including an undetermined diff, keeps the existing check."""
    mock_changed.return_value = changed_files
    mock_master.return_value = {"dockerImageTag": "1.0.0"}

    result = CheckVersionIncrement()._run(mock_connector)

    assert result.status == CheckStatus.FAILED
    assert "was not incremented" in result.message


def _git(cwd: Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True)


@pytest.fixture
def repo(tmp_path, monkeypatch):
    """A repo whose `origin/master` holds one connector, checked out on a branch."""
    monkeypatch.delenv("GITHUB_BASE_REF", raising=False)
    connector_dir = tmp_path / _CONNECTOR_DIR
    (connector_dir / "unit_tests").mkdir(parents=True)
    (connector_dir / "manifest.yaml").write_text("version: 1\n")
    (connector_dir / "unit_tests" / "test_x.py").write_text("")
    (tmp_path / "README.md").write_text("")
    _git(tmp_path, "init", "-q", "-b", "master")
    _git(tmp_path, "add", ".")
    _git(
        tmp_path,
        "-c",
        "user.name=test",
        "-c",
        "user.email=test@example.com",
        "commit",
        "-q",
        "-m",
        "init",
    )
    _git(tmp_path, "update-ref", "refs/remotes/origin/master", "HEAD")
    _git(tmp_path, "checkout", "-q", "-b", "feature")
    return tmp_path


def test_get_changed_files_from_git(repo):
    """Committed, uncommitted and untracked changes are all reported."""
    connector_dir = repo / _CONNECTOR_DIR
    (connector_dir / "unit_tests" / "test_x.py").write_text("x = 1\n")
    _git(repo, "add", ".")
    _git(
        repo,
        "-c",
        "user.name=test",
        "-c",
        "user.email=test@example.com",
        "commit",
        "-q",
        "-m",
        "test change",
    )
    (connector_dir / "acceptance-test-config.yml").write_text("")
    (repo / "README.md").write_text("outside the connector\n")

    changed = CheckVersionIncrement._get_changed_files(
        MagicMock(code_directory=connector_dir)
    )

    assert changed == ["acceptance-test-config.yml", "unit_tests/test_x.py"]


def test_get_changed_files_keeps_non_ascii_paths_verbatim(repo):
    """Git would quote non-ASCII paths, which then never match the bypass list."""
    connector_dir = repo / _CONNECTOR_DIR
    (connector_dir / "unit_tests" / "test_café.py").write_text("")
    _git(repo, "add", ".")
    _git(
        repo,
        "-c",
        "user.name=test",
        "-c",
        "user.email=test@example.com",
        "commit",
        "-q",
        "-m",
        "non-ascii test",
    )
    (connector_dir / "unit_tests" / "test_naïve.py").write_text("")

    changed = CheckVersionIncrement._get_changed_files(
        MagicMock(code_directory=connector_dir)
    )

    assert changed == ["unit_tests/test_café.py", "unit_tests/test_naïve.py"]
    assert not any(_is_production_path(path) for path in changed)


def test_get_changed_files_reports_both_sides_of_a_move(repo):
    """Moving released code into a test directory is not a test-only change."""
    connector_dir = repo / _CONNECTOR_DIR
    _git(connector_dir, "mv", "manifest.yaml", "unit_tests/manifest.yaml")
    _git(
        repo,
        "-c",
        "user.name=test",
        "-c",
        "user.email=test@example.com",
        "commit",
        "-q",
        "-m",
        "move",
    )

    changed = CheckVersionIncrement._get_changed_files(
        MagicMock(code_directory=connector_dir)
    )

    assert changed == ["manifest.yaml", "unit_tests/manifest.yaml"]


def test_get_changed_files_prefers_upstream(repo):
    """On a fork checkout, `upstream` is the base, not the fork's own master."""
    connector_dir = repo / _CONNECTOR_DIR
    # A test change that upstream master already has, but the fork's master lacks.
    (connector_dir / "unit_tests" / "test_x.py").write_text("x = 1\n")
    _git(repo, "add", ".")
    _git(
        repo,
        "-c",
        "user.name=test",
        "-c",
        "user.email=test@example.com",
        "commit",
        "-q",
        "-m",
        "upstream change",
    )
    _git(repo, "update-ref", "refs/remotes/upstream/master", "HEAD")
    (connector_dir / "manifest.yaml").write_text("version: 2\n")

    changed = CheckVersionIncrement._get_changed_files(
        MagicMock(code_directory=connector_dir)
    )

    assert changed == ["manifest.yaml"]


def test_get_changed_files_without_base_branch(repo, monkeypatch):
    """A base branch that was not fetched means the changes are unknown."""
    monkeypatch.setenv("GITHUB_BASE_REF", "main")

    changed = CheckVersionIncrement._get_changed_files(
        MagicMock(code_directory=repo / _CONNECTOR_DIR)
    )

    assert changed is None


def test_get_changed_files_helper_raises_on_unknown_base_ref(repo):
    """The helper never falls back to a plain diff, so callers can fail closed."""
    with pytest.raises(subprocess.CalledProcessError):
        get_changed_files(repo / _CONNECTOR_DIR, "origin/main")


def test_get_changed_files_outside_git(tmp_path):
    assert (
        CheckVersionIncrement._get_changed_files(MagicMock(code_directory=tmp_path))
        is None
    )
