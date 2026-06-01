# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Unit tests for Python connector dependency generation in registry/_python_deps_analysis.py."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any
from unittest.mock import patch

import pytest

from airbyte_ops_mcp.registry._constants import CONNECTOR_DEPENDENCY_FILE_NAME
from airbyte_ops_mcp.registry._python_deps_analysis import (
    _build_dependencies_json,
    _is_python_connector,
    _run_docker_pip_freeze,
    extract_cdk_version_from_dependencies,
    generate_python_dependencies_file,
)

# ---------------------------------------------------------------------------
# _is_python_connector
# ---------------------------------------------------------------------------


@pytest.mark.unit
@pytest.mark.parametrize(
    "metadata_data,expected",
    [
        pytest.param(
            {"tags": ["language:python", "certified"]},
            True,
            id="python_tag_present",
        ),
        pytest.param(
            {"tags": ["language:java", "certified"]},
            False,
            id="java_tag_only",
        ),
        pytest.param(
            {"tags": []},
            False,
            id="empty_tags",
        ),
        pytest.param(
            {},
            False,
            id="no_tags_key",
        ),
        pytest.param(
            {"tags": ["language:python"]},
            True,
            id="python_only_tag",
        ),
        pytest.param(
            {"tags": ["language:low-code", "language:python"]},
            True,
            id="python_among_multiple_language_tags",
        ),
    ],
)
def test_is_python_connector(metadata_data: dict[str, Any], expected: bool) -> None:
    assert _is_python_connector(metadata_data) == expected


# ---------------------------------------------------------------------------
# run_docker_pip_freeze
# ---------------------------------------------------------------------------


@pytest.mark.unit
@pytest.mark.parametrize(
    "stdout,expected",
    [
        pytest.param(
            "airbyte-cdk==1.2.3\nrequests==2.31.0\n",
            [
                {"package_name": "airbyte-cdk", "version": "1.2.3"},
                {"package_name": "requests", "version": "2.31.0"},
            ],
            id="normal_output",
        ),
        pytest.param(
            "airbyte-cdk==1.2.3\n# editable install\nrequests==2.31.0\n",
            [
                {"package_name": "airbyte-cdk", "version": "1.2.3"},
                {"package_name": "requests", "version": "2.31.0"},
            ],
            id="skips_non_pinned_lines",
        ),
        pytest.param(
            "airbyte-cdk==1.2.3\n# Editable install with no version control (source-faker==7.0.4)\nrequests==2.31.0\n",
            [
                {"package_name": "airbyte-cdk", "version": "1.2.3"},
                {"package_name": "requests", "version": "2.31.0"},
            ],
            id="strips_editable_install_comment_with_equals",
        ),
        pytest.param(
            "",
            [],
            id="empty_output",
        ),
        pytest.param(
            "pkg-with-extras[foo]==1.0.0\n",
            [{"package_name": "pkg-with-extras[foo]", "version": "1.0.0"}],
            id="package_with_extras",
        ),
    ],
)
def test_run_docker_pip_freeze(
    stdout: str,
    expected: list[dict[str, str]],
) -> None:
    fake_result = subprocess.CompletedProcess(
        args=[], returncode=0, stdout=stdout, stderr=""
    )
    with patch(
        "airbyte_ops_mcp.registry._python_deps_analysis.subprocess.run",
        return_value=fake_result,
    ):
        assert _run_docker_pip_freeze("airbyte/source-test:1.0.0") == expected


@pytest.mark.unit
def test_run_docker_pip_freeze_raises_on_failure() -> None:
    fake_result = subprocess.CompletedProcess(
        args=[], returncode=1, stdout="", stderr="some error"
    )
    with patch(
        "airbyte_ops_mcp.registry._python_deps_analysis.subprocess.run",
        return_value=fake_result,
    ), pytest.raises(RuntimeError, match="docker pip freeze failed"):
        _run_docker_pip_freeze("airbyte/source-test:1.0.0")


# ---------------------------------------------------------------------------
# build_dependencies_json
# ---------------------------------------------------------------------------


@pytest.mark.unit
def test_build_dependencies_json() -> None:
    deps = [{"package_name": "airbyte-cdk", "version": "1.0.0"}]
    result = _build_dependencies_json(
        connector_name="source-test",
        version="2.0.0",
        docker_repository="airbyte/source-test",
        definition_id="abc-123",
        dependencies=deps,
    )
    assert result["connector_technical_name"] == "source-test"
    assert result["connector_repository"] == "airbyte/source-test"
    assert result["connector_version"] == "2.0.0"
    assert result["connector_definition_id"] == "abc-123"
    assert result["dependencies"] == deps
    assert "generation_time" in result


# ---------------------------------------------------------------------------
# extract_cdk_version_from_dependencies
# ---------------------------------------------------------------------------


@pytest.mark.unit
@pytest.mark.parametrize(
    "dependencies_json,expected",
    [
        pytest.param(
            {
                "dependencies": [
                    {"package_name": "airbyte-cdk", "version": "1.2.3"},
                    {"package_name": "requests", "version": "2.31.0"},
                ]
            },
            "python:1.2.3",
            id="cdk_found",
        ),
        pytest.param(
            {
                "dependencies": [
                    {"package_name": "requests", "version": "2.31.0"},
                ]
            },
            None,
            id="cdk_not_found",
        ),
        pytest.param(
            {"dependencies": []},
            None,
            id="empty_dependencies",
        ),
        pytest.param(
            {},
            None,
            id="no_dependencies_key",
        ),
    ],
)
def test_extract_cdk_version_from_dependencies(
    dependencies_json: dict[str, Any],
    expected: str | None,
) -> None:
    assert extract_cdk_version_from_dependencies(dependencies_json) == expected


# ---------------------------------------------------------------------------
# generate_python_dependencies_file
# ---------------------------------------------------------------------------


@pytest.mark.unit
def test_generate_python_dependencies_file_writes_json(tmp_path: Path) -> None:
    metadata_data = {
        "dockerRepository": "airbyte/source-test",
        "dockerImageTag": "1.0.0",
        "definitionId": "def-456",
    }
    fake_pip_output = "airbyte-cdk==2.0.0\nrequests==2.31.0\n"
    fake_result = subprocess.CompletedProcess(
        args=[], returncode=0, stdout=fake_pip_output, stderr=""
    )

    with patch(
        "airbyte_ops_mcp.registry._python_deps_analysis.subprocess.run",
        return_value=fake_result,
    ):
        result = generate_python_dependencies_file(
            metadata_data=metadata_data,
            docker_image="airbyte/source-test:1.0.0",
            output_dir=tmp_path,
        )

    assert result is not None
    assert result["connector_technical_name"] == "source-test"
    assert result["connector_version"] == "1.0.0"
    assert len(result["dependencies"]) == 2

    deps_file = tmp_path / CONNECTOR_DEPENDENCY_FILE_NAME
    assert deps_file.exists()
    written = json.loads(deps_file.read_text())
    assert written["connector_technical_name"] == "source-test"


@pytest.mark.unit
def test_generate_python_dependencies_file_returns_none_on_docker_failure(
    tmp_path: Path,
) -> None:
    metadata_data = {
        "dockerRepository": "airbyte/source-test",
        "dockerImageTag": "1.0.0",
        "definitionId": "def-456",
    }
    fake_result = subprocess.CompletedProcess(
        args=[], returncode=1, stdout="", stderr="docker error"
    )

    with patch(
        "airbyte_ops_mcp.registry._python_deps_analysis.subprocess.run",
        return_value=fake_result,
    ):
        result = generate_python_dependencies_file(
            metadata_data=metadata_data,
            docker_image="airbyte/source-test:1.0.0",
            output_dir=tmp_path,
        )

    assert result is None
    assert not (tmp_path / CONNECTOR_DEPENDENCY_FILE_NAME).exists()


@pytest.mark.unit
def test_generate_python_dependencies_file_returns_none_on_empty_deps(
    tmp_path: Path,
) -> None:
    metadata_data = {
        "dockerRepository": "airbyte/source-test",
        "dockerImageTag": "1.0.0",
        "definitionId": "def-456",
    }
    fake_result = subprocess.CompletedProcess(
        args=[], returncode=0, stdout="", stderr=""
    )

    with patch(
        "airbyte_ops_mcp.registry._python_deps_analysis.subprocess.run",
        return_value=fake_result,
    ):
        result = generate_python_dependencies_file(
            metadata_data=metadata_data,
            docker_image="airbyte/source-test:1.0.0",
            output_dir=tmp_path,
        )

    assert result is None
    assert not (tmp_path / CONNECTOR_DEPENDENCY_FILE_NAME).exists()
