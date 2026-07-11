# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Tests for the `airbyte-ops local connector list` CLI command."""

from __future__ import annotations

from pathlib import Path

import cyclopts
import pytest
import yaml

from airbyte_ops_mcp.airbyte_repo.list_connectors import (
    CONNECTOR_PATH_PREFIX,
    METADATA_FILE_NAME,
)
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


def _write_connector(repo_path: Path, name: str, metadata: dict) -> None:
    """Create `<repo>/airbyte-integrations/connectors/<name>/metadata.yaml`."""
    connector_dir = repo_path / CONNECTOR_PATH_PREFIX / name
    connector_dir.mkdir(parents=True, exist_ok=True)
    (connector_dir / METADATA_FILE_NAME).write_text(
        yaml.safe_dump(metadata, sort_keys=False)
    )


def _autopilot_metadata(name: str, *, enabled: bool) -> dict:
    """Build metadata with autopilot rollout fully enabled or disabled."""
    return {
        "data": {
            "name": name,
            "dockerImageTag": "1.0.0",
            "releases": {
                "rolloutConfiguration": {
                    "defaultRolloutMode": "autopilot",
                    "enableProgressiveRollout": enabled,
                }
            },
        }
    }


@pytest.fixture
def repo_with_mixed_rollout(tmp_path: Path) -> Path:
    """A fake monorepo with autopilot-enabled, disabled, and unconfigured connectors."""
    _write_connector(
        tmp_path, "source-enabled", _autopilot_metadata("source-enabled", enabled=True)
    )
    _write_connector(
        tmp_path,
        "source-disabled",
        _autopilot_metadata("source-disabled", enabled=False),
    )
    _write_connector(
        tmp_path,
        "source-unconfigured",
        {"data": {"name": "source-unconfigured", "dockerImageTag": "1.0.0"}},
    )
    return tmp_path


@pytest.mark.unit
def test_list_autopilot_enabled_true(
    repo_with_mixed_rollout: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """`--autopilot-enabled=true` keeps only fully-enabled connectors."""
    exit_code = invoke_cli(
        [
            "local",
            "connector",
            "list",
            "--repo-path",
            str(repo_with_mixed_rollout),
            "--autopilot-enabled=true",
        ]
    )
    output = capsys.readouterr().out

    assert exit_code == 0
    assert output.split() == ["source-enabled"]


@pytest.mark.unit
def test_list_autopilot_enabled_false(
    repo_with_mixed_rollout: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """`--autopilot-enabled=false` keeps connectors without rollouts enabled."""
    exit_code = invoke_cli(
        [
            "local",
            "connector",
            "list",
            "--repo-path",
            str(repo_with_mixed_rollout),
            "--autopilot-enabled=false",
        ]
    )
    output = capsys.readouterr().out

    assert exit_code == 0
    assert output.split() == ["source-disabled", "source-unconfigured"]


@pytest.mark.unit
def test_list_without_autopilot_filter_returns_all(
    repo_with_mixed_rollout: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Omitting the filter leaves the rollout status unfiltered."""
    exit_code = invoke_cli(
        [
            "local",
            "connector",
            "list",
            "--repo-path",
            str(repo_with_mixed_rollout),
        ]
    )
    output = capsys.readouterr().out

    assert exit_code == 0
    assert output.split() == [
        "source-disabled",
        "source-enabled",
        "source-unconfigured",
    ]
