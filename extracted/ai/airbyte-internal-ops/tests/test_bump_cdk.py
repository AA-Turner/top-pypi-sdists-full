# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Unit tests for the bump_cdk module."""

from __future__ import annotations

import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from airbyte_ops_mcp.airbyte_repo.bump_cdk import (
    CdkBumpError,
    UnsupportedLanguageError,
    _compute_latest_constraint,
    _get_current_java_cdk_version,
    _get_current_python_cdk_version,
    _update_java_cdk_version,
    _update_python_cdk_version,
    bump_cdk,
    get_latest_java_cdk_version,
)

# ---------------------------------------------------------------------------
# _compute_latest_constraint
# ---------------------------------------------------------------------------


@pytest.mark.unit
@pytest.mark.parametrize(
    "version,expected",
    [
        pytest.param("7.13.0", ">=7.13.0,<8.0.0", id="major_7"),
        pytest.param("0.90.0", ">=0.90.0,<1.0.0", id="major_0"),
        pytest.param("1.0.0", ">=1.0.0,<2.0.0", id="major_1"),
    ],
)
def test_compute_latest_constraint(version: str, expected: str):
    assert _compute_latest_constraint(version) == expected


# ---------------------------------------------------------------------------
# _get_current_python_cdk_version
# ---------------------------------------------------------------------------


@pytest.mark.unit
def test_get_current_python_cdk_version_string_dep():
    with tempfile.TemporaryDirectory() as tmpdir:
        pyproject = Path(tmpdir) / "pyproject.toml"
        pyproject.write_text('[tool.poetry.dependencies]\nairbyte-cdk = ">=6.0,<7.0"\n')
        assert _get_current_python_cdk_version(pyproject) == ">=6.0,<7.0"


@pytest.mark.unit
def test_get_current_python_cdk_version_dict_dep_with_extras():
    with tempfile.TemporaryDirectory() as tmpdir:
        pyproject = Path(tmpdir) / "pyproject.toml"
        pyproject.write_text(
            "[tool.poetry.dependencies]\n"
            'airbyte-cdk = {version = "^7.0.4", extras = ["file-based"]}\n'
        )
        assert _get_current_python_cdk_version(pyproject) == "^7.0.4"


@pytest.mark.unit
def test_get_current_python_cdk_version_missing_returns_none():
    with tempfile.TemporaryDirectory() as tmpdir:
        pyproject = Path(tmpdir) / "pyproject.toml"
        pyproject.write_text('[tool.poetry.dependencies]\nrequests = "*"\n')
        assert _get_current_python_cdk_version(pyproject) is None


# ---------------------------------------------------------------------------
# _update_python_cdk_version (preserves extras via regex)
# ---------------------------------------------------------------------------


@pytest.mark.unit
def test_update_python_cdk_version_preserves_extras():
    with tempfile.TemporaryDirectory() as tmpdir:
        pyproject = Path(tmpdir) / "pyproject.toml"
        pyproject.write_text(
            "[tool.poetry.dependencies]\n"
            'airbyte-cdk = {version = "^7.0.4", extras = ["file-based"]}\n'
        )
        _update_python_cdk_version(pyproject, ">=7.13.0,<8.0.0")

        content = pyproject.read_text()
        assert ">=7.13.0,<8.0.0" in content
        assert "file-based" in content  # extras preserved


# ---------------------------------------------------------------------------
# _get_current_java_cdk_version / _update_java_cdk_version
# ---------------------------------------------------------------------------

GRADLE_CONTENT = """\
ext {
    cdkVersionRequired = '0.44.5'
    useLocalCdk = true
}
"""


@pytest.mark.unit
def test_get_current_java_cdk_version():
    with tempfile.TemporaryDirectory() as tmpdir:
        gradle = Path(tmpdir) / "build.gradle"
        gradle.write_text(GRADLE_CONTENT)
        assert _get_current_java_cdk_version(gradle) == "0.44.5"


@pytest.mark.unit
def test_update_java_cdk_version_and_disables_local():
    with tempfile.TemporaryDirectory() as tmpdir:
        gradle = Path(tmpdir) / "build.gradle"
        gradle.write_text(GRADLE_CONTENT)
        _update_java_cdk_version(gradle, "0.48.18")

        content = gradle.read_text()
        assert "0.48.18" in content
        assert "useLocalCdk = false" in content


# ---------------------------------------------------------------------------
# get_latest_java_cdk_version
# ---------------------------------------------------------------------------


@pytest.mark.unit
def test_get_latest_java_cdk_version_reads_version_properties():
    with tempfile.TemporaryDirectory() as tmpdir:
        # Simulate monorepo structure:
        # <repo>/airbyte-integrations/connectors/<name>
        connector = Path(tmpdir) / "airbyte-integrations" / "connectors" / "source-test"
        connector.mkdir(parents=True)
        version_file = (
            Path(tmpdir)
            / "airbyte-cdk"
            / "java"
            / "airbyte-cdk"
            / "core"
            / "src"
            / "main"
            / "resources"
        )
        version_file.mkdir(parents=True)
        (version_file / "version.properties").write_text("version=0.48.18\n")

        assert get_latest_java_cdk_version(connector) == "0.48.18"


@pytest.mark.unit
def test_get_latest_java_cdk_version_missing_file_raises():
    with tempfile.TemporaryDirectory() as tmpdir:
        connector = Path(tmpdir) / "airbyte-integrations" / "connectors" / "source-test"
        connector.mkdir(parents=True)
        with pytest.raises(CdkBumpError, match=r"version\.properties not found"):
            get_latest_java_cdk_version(connector)


# ---------------------------------------------------------------------------
# bump_cdk: manifest-only is a no-op
# ---------------------------------------------------------------------------


@pytest.mark.unit
@patch("airbyte_ops_mcp.airbyte_repo.bump_cdk._detect_connector_language")
def test_bump_cdk_manifest_only_noop(mock_lang):
    mock_lang.return_value = "manifest-only"
    with tempfile.TemporaryDirectory() as tmpdir:
        connector = Path(tmpdir) / "airbyte-integrations" / "connectors" / "source-test"
        connector.mkdir(parents=True)
        result = bump_cdk(tmpdir, "source-test")

    assert result.updated is False
    assert "Manifest-only" in result.message


# ---------------------------------------------------------------------------
# bump_cdk: dry-run default mode without poetry.lock
# ---------------------------------------------------------------------------


@pytest.mark.unit
@patch("airbyte_ops_mcp.airbyte_repo.bump_cdk._detect_connector_language")
def test_bump_cdk_default_dry_run_no_lock_file(mock_lang):
    """Default dry-run should report empty files_modified when no poetry.lock exists."""
    mock_lang.return_value = "python"
    with tempfile.TemporaryDirectory() as tmpdir:
        connector = Path(tmpdir) / "airbyte-integrations" / "connectors" / "source-test"
        connector.mkdir(parents=True)
        (connector / "pyproject.toml").write_text(
            '[tool.poetry.dependencies]\nairbyte-cdk = ">=6.0,<7.0"\n'
        )
        # No poetry.lock created
        result = bump_cdk(tmpdir, "source-test", dry_run=True)

    assert result.dry_run is True
    assert result.files_modified == []
    assert "No poetry.lock" in result.message


# ---------------------------------------------------------------------------
# bump_cdk: unsupported language raises
# ---------------------------------------------------------------------------


@pytest.mark.unit
@patch("airbyte_ops_mcp.airbyte_repo.bump_cdk._detect_connector_language")
def test_bump_cdk_unsupported_language_raises(mock_lang):
    mock_lang.return_value = None
    with tempfile.TemporaryDirectory() as tmpdir:
        connector = Path(tmpdir) / "airbyte-integrations" / "connectors" / "source-test"
        connector.mkdir(parents=True)
        with pytest.raises(UnsupportedLanguageError):
            bump_cdk(tmpdir, "source-test")
