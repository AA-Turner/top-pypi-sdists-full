# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Tests for GitHub CLI commands."""

from __future__ import annotations

import json
from unittest.mock import patch

import cyclopts
import pytest

from airbyte_ops_mcp.cli.app import app


def invoke_cli(tokens: list[str]) -> int:
    """Run the `airbyte-ops` app and return its exit code."""
    try:
        app(tokens=tokens, exit_on_error=False)
    except cyclopts.exceptions.CycloptsError:
        return 1
    except SystemExit as exc:
        return int(exc.code or 0)
    return 0


@pytest.mark.unit
def test_gh_connector_help(capsys: pytest.CaptureFixture[str]) -> None:
    exit_code = invoke_cli(["gh", "connector", "get-version", "--help"])
    output = capsys.readouterr()

    assert exit_code == 0
    assert "ref" in output.out
    assert "owner" in output.out
    assert "repo" in output.out


@pytest.mark.unit
def test_gh_connector_ref_required() -> None:
    exit_code = invoke_cli(["gh", "connector", "get-version", "--name", "source-test"])

    assert exit_code != 0


@pytest.mark.unit
def test_gh_connector_get_version(capsys: pytest.CaptureFixture[str]) -> None:
    metadata_yaml = "data:\n  dockerImageTag: 1.2.3-rc.1\n"

    with patch(
        "airbyte_ops_mcp.connector_metadata.get_file_contents_at_ref",
        return_value=metadata_yaml,
    ):
        exit_code = invoke_cli(
            [
                "gh",
                "connector",
                "get-version",
                "--name",
                "source-test",
                "--ref",
                "master",
            ]
        )
    output = capsys.readouterr()

    assert exit_code == 0
    assert output.out.strip() == "1.2.3-rc.1"


@pytest.mark.unit
def test_gh_connector_list_modified_only_matrix(
    capsys: pytest.CaptureFixture[str],
) -> None:
    with patch(
        "airbyte_ops_mcp.cli.gh.get_modified_connectors_from_github",
        return_value=["source-faker"],
    ) as mock_list_changed:
        exit_code = invoke_cli(
            [
                "gh",
                "connector",
                "list",
                "--modified-only",
                "--pr",
                "123",
                "--gh-token",
                "test-token",
                "--output-format",
                "json-gh-matrix",
            ]
        )
    output = capsys.readouterr()

    assert exit_code == 0
    assert json.loads(output.out) == {"connector": ["source-faker"]}
    mock_list_changed.assert_called_once_with(
        pr_number=123,
        pr_owner="airbytehq",
        pr_repo="airbyte",
        gh_token="test-token",
    )


@pytest.mark.unit
def test_gh_connector_list_modified_only_empty_matrix(
    capsys: pytest.CaptureFixture[str],
) -> None:
    with patch(
        "airbyte_ops_mcp.cli.gh.get_modified_connectors_from_github",
        return_value=[],
    ) as mock_list_changed:
        exit_code = invoke_cli(
            [
                "gh",
                "connector",
                "list",
                "--modified-only",
                "--pr",
                "https://github.com/test-org/test-repo/pull/123",
                "--owner",
                "ignored-owner",
                "--repo",
                "ignored-repo",
                "--gh-token",
                "test-token",
                "--output-format",
                "json-gh-matrix",
            ]
        )
    output = capsys.readouterr()

    assert exit_code == 0
    assert json.loads(output.out) == {"connector": [""]}
    mock_list_changed.assert_called_once_with(
        pr_number=123,
        pr_owner="test-org",
        pr_repo="test-repo",
        gh_token="test-token",
    )


@pytest.mark.unit
def test_gh_connector_list_requires_modified_only() -> None:
    exit_code = invoke_cli(["gh", "connector", "list", "--pr", "123"])

    assert exit_code != 0


@pytest.mark.unit
def test_gh_connector_list_handles_github_errors() -> None:
    with patch(
        "airbyte_ops_mcp.cli.gh.get_modified_connectors_from_github",
        side_effect=ValueError("No GitHub token found."),
    ):
        exit_code = invoke_cli(
            [
                "gh",
                "connector",
                "list",
                "--modified-only",
                "--pr",
                "123",
                "--output-format",
                "json-gh-matrix",
            ]
        )

    assert exit_code != 0


@pytest.mark.unit
def test_gh_connector_info_dpath(capsys: pytest.CaptureFixture[str]) -> None:
    metadata_yaml = "data:\n  definitionId: abc123\n  dockerImageTag: 1.2.3-rc.1\n"

    with patch(
        "airbyte_ops_mcp.connector_metadata.get_file_contents_at_ref",
        return_value=metadata_yaml,
    ):
        exit_code = invoke_cli(
            [
                "gh",
                "connector",
                "info",
                "--name",
                "source-test",
                "--ref",
                "master",
                "--dpath",
                "data/definitionId",
            ]
        )
    output = capsys.readouterr()

    assert exit_code == 0
    assert output.out.strip() == "abc123"


@pytest.mark.unit
def test_gh_connector_info_json(capsys: pytest.CaptureFixture[str]) -> None:
    metadata_yaml = """
data:
  dockerImageTag: 1.2.3-rc.1
  supportLevel: certified
  tags:
    - language:python
"""

    with patch(
        "airbyte_ops_mcp.connector_metadata.get_file_contents_at_ref",
        return_value=metadata_yaml,
    ):
        exit_code = invoke_cli(
            [
                "gh",
                "connector",
                "info",
                "--name",
                "source-test",
                "--ref",
                "master",
            ]
        )
    output = capsys.readouterr()

    assert exit_code == 0
    parsed_output = json.loads(output.out)
    assert parsed_output == {
        "data": {
            "dockerImageTag": "1.2.3-rc.1",
            "supportLevel": "certified",
            "tags": ["language:python"],
        }
    }
