# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Unit tests for autopilot rollout enablement in `progressive_rollout`."""

from __future__ import annotations

import tempfile
from pathlib import Path

import pytest
import yaml

from airbyte_ops_mcp.airbyte_repo.bump_version import ConnectorNotFoundError
from airbyte_ops_mcp.airbyte_repo.list_connectors import (
    CONNECTOR_PATH_PREFIX,
    METADATA_FILE_NAME,
)
from airbyte_ops_mcp.airbyte_repo.progressive_rollout import (
    AUTOPILOT_ROLLOUT_MODE,
    disable_autopilot_rollout,
    enable_autopilot_rollout,
    is_autopilot_rollout_enabled,
)


def _write_connector_metadata(repo_path: Path, name: str, metadata: dict) -> Path:
    """Create a connector directory with the given metadata.yaml contents."""
    connector_dir = repo_path / CONNECTOR_PATH_PREFIX / name
    connector_dir.mkdir(parents=True, exist_ok=True)
    metadata_file = connector_dir / METADATA_FILE_NAME
    metadata_file.write_text(yaml.safe_dump(metadata, sort_keys=False))
    return metadata_file


def _read_rollout_config(metadata_file: Path) -> dict:
    parsed = yaml.safe_load(metadata_file.read_text())
    return parsed["data"]["releases"]["rolloutConfiguration"]


@pytest.mark.unit
def test_enable_autopilot_on_bare_metadata() -> None:
    """Adds rolloutConfiguration + autopilotConfig when none exists."""
    with tempfile.TemporaryDirectory() as tmp:
        repo = Path(tmp)
        metadata_file = _write_connector_metadata(
            repo,
            "source-test",
            {"data": {"dockerImageTag": "1.0.0"}},
        )

        result = enable_autopilot_rollout(repo, "source-test")

        assert result.modified is True
        assert result.default_rollout_mode == AUTOPILOT_ROLLOUT_MODE
        assert result.progressive_rollout_enabled is True
        assert result.strategy == "fast"

        parsed = yaml.safe_load(metadata_file.read_text())
        assert parsed["data"]["dockerImageTag"] == "1.0.0"

        rollout = parsed["data"]["releases"]["rolloutConfiguration"]
        assert rollout["defaultRolloutMode"] == "autopilot"
        assert rollout["enableProgressiveRollout"] is True
        assert rollout["autopilotConfig"] == {
            "autoStart": True,
            "autoPromoteStages": True,
            "strategy": "fast",
        }


@pytest.mark.unit
def test_enable_autopilot_preserves_existing_rollout_keys() -> None:
    """Preserves sibling rolloutConfiguration keys like enableProgressiveRollout."""
    with tempfile.TemporaryDirectory() as tmp:
        repo = Path(tmp)
        metadata_file = _write_connector_metadata(
            repo,
            "source-test",
            {
                "data": {
                    "dockerImageTag": "1.0.0",
                    "releases": {
                        "rolloutConfiguration": {
                            "enableProgressiveRollout": True,
                        }
                    },
                }
            },
        )

        enable_autopilot_rollout(repo, "source-test", strategy="slow")

        rollout = _read_rollout_config(metadata_file)
        assert rollout["enableProgressiveRollout"] is True
        assert rollout["defaultRolloutMode"] == "autopilot"
        assert rollout["autopilotConfig"]["strategy"] == "slow"


@pytest.mark.unit
def test_enable_autopilot_idempotent() -> None:
    """A second run reports no modification."""
    with tempfile.TemporaryDirectory() as tmp:
        repo = Path(tmp)
        _write_connector_metadata(
            repo,
            "source-test",
            {"data": {"dockerImageTag": "1.0.0"}},
        )

        first = enable_autopilot_rollout(repo, "source-test")
        second = enable_autopilot_rollout(repo, "source-test")

        assert first.modified is True
        assert second.modified is False


@pytest.mark.unit
def test_enable_autopilot_dry_run_does_not_write() -> None:
    """Dry run reports the change but leaves the file untouched."""
    with tempfile.TemporaryDirectory() as tmp:
        repo = Path(tmp)
        metadata_file = _write_connector_metadata(
            repo,
            "source-test",
            {"data": {"dockerImageTag": "1.0.0"}},
        )
        before = metadata_file.read_text()

        result = enable_autopilot_rollout(repo, "source-test", dry_run=True)

        assert result.modified is True
        assert result.dry_run is True
        assert metadata_file.read_text() == before


@pytest.mark.unit
def test_enable_autopilot_invalid_strategy() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        repo = Path(tmp)
        _write_connector_metadata(
            repo,
            "source-test",
            {"data": {"dockerImageTag": "1.0.0"}},
        )

        with pytest.raises(ValueError, match="Unknown autopilot strategy"):
            enable_autopilot_rollout(repo, "source-test", strategy="turbo")


@pytest.mark.unit
def test_enable_autopilot_connector_not_found() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        repo = Path(tmp)
        with pytest.raises(ConnectorNotFoundError):
            enable_autopilot_rollout(repo, "source-missing")


@pytest.mark.unit
def test_enable_autopilot_preserves_existing_autopilot_config() -> None:
    """Without explicit overrides, existing autopilotConfig values are kept."""
    with tempfile.TemporaryDirectory() as tmp:
        repo = Path(tmp)
        metadata_file = _write_connector_metadata(
            repo,
            "source-test",
            {
                "data": {
                    "dockerImageTag": "1.0.0",
                    "releases": {
                        "rolloutConfiguration": {
                            "defaultRolloutMode": "manual",
                            "autopilotConfig": {
                                "autoStart": False,
                                "autoPromoteStages": False,
                                "strategy": "slow",
                            },
                        }
                    },
                }
            },
        )

        result = enable_autopilot_rollout(repo, "source-test")

        assert result.modified is True  # defaultRolloutMode flipped to autopilot
        assert result.strategy == "slow"
        assert result.auto_start is False
        assert result.auto_promote_stages is False

        rollout = _read_rollout_config(metadata_file)
        assert rollout["defaultRolloutMode"] == "autopilot"
        assert rollout["autopilotConfig"] == {
            "autoStart": False,
            "autoPromoteStages": False,
            "strategy": "slow",
        }


@pytest.mark.unit
def test_enable_autopilot_explicit_strategy_overrides_existing() -> None:
    """An explicit strategy override replaces the existing value."""
    with tempfile.TemporaryDirectory() as tmp:
        repo = Path(tmp)
        metadata_file = _write_connector_metadata(
            repo,
            "source-test",
            {
                "data": {
                    "releases": {
                        "rolloutConfiguration": {
                            "defaultRolloutMode": "autopilot",
                            "autopilotConfig": {
                                "autoStart": True,
                                "autoPromoteStages": True,
                                "strategy": "slow",
                            },
                        }
                    },
                }
            },
        )

        result = enable_autopilot_rollout(repo, "source-test", strategy="fast")

        assert result.modified is True
        assert result.strategy == "fast"
        rollout = _read_rollout_config(metadata_file)
        assert rollout["autopilotConfig"]["strategy"] == "fast"


@pytest.mark.unit
def test_disable_autopilot_clears_flag_and_retains_config() -> None:
    """Disable only clears the toggle; mode + autopilotConfig are left intact."""
    with tempfile.TemporaryDirectory() as tmp:
        repo = Path(tmp)
        metadata_file = _write_connector_metadata(
            repo,
            "source-test",
            {
                "data": {
                    "releases": {
                        "rolloutConfiguration": {
                            "defaultRolloutMode": "autopilot",
                            "enableProgressiveRollout": True,
                            "autopilotConfig": {
                                "autoStart": True,
                                "autoPromoteStages": True,
                                "strategy": "slow",
                            },
                        }
                    },
                }
            },
        )

        result = disable_autopilot_rollout(repo, "source-test")

        assert result.modified is True
        assert result.progressive_rollout_enabled is False

        rollout = _read_rollout_config(metadata_file)
        assert rollout["enableProgressiveRollout"] is False
        # defaultRolloutMode + autopilotConfig are retained (inert, lossless).
        assert rollout["defaultRolloutMode"] == "autopilot"
        assert rollout["autopilotConfig"] == {
            "autoStart": True,
            "autoPromoteStages": True,
            "strategy": "slow",
        }


@pytest.mark.unit
def test_disable_autopilot_no_rollout_config_is_noop() -> None:
    """Disabling a connector with no rolloutConfiguration is a no-op."""
    with tempfile.TemporaryDirectory() as tmp:
        repo = Path(tmp)
        metadata_file = _write_connector_metadata(
            repo,
            "source-test",
            {"data": {"dockerImageTag": "1.0.0"}},
        )
        before = metadata_file.read_text()

        result = disable_autopilot_rollout(repo, "source-test")

        assert result.modified is False
        assert metadata_file.read_text() == before


@pytest.mark.unit
def test_disable_autopilot_idempotent() -> None:
    """A second disable reports no modification."""
    with tempfile.TemporaryDirectory() as tmp:
        repo = Path(tmp)
        _write_connector_metadata(
            repo,
            "source-test",
            {
                "data": {
                    "releases": {
                        "rolloutConfiguration": {
                            "defaultRolloutMode": "autopilot",
                            "enableProgressiveRollout": True,
                        }
                    },
                }
            },
        )

        first = disable_autopilot_rollout(repo, "source-test")
        second = disable_autopilot_rollout(repo, "source-test")

        assert first.modified is True
        assert second.modified is False


@pytest.mark.unit
def test_enable_then_disable_round_trip_is_lossless() -> None:
    """Enable writes config + flag; disable clears only the flag, keeping config."""
    with tempfile.TemporaryDirectory() as tmp:
        repo = Path(tmp)
        metadata_file = _write_connector_metadata(
            repo,
            "source-test",
            {"data": {"dockerImageTag": "1.0.0"}},
        )

        enable_autopilot_rollout(repo, "source-test", strategy="slow")
        disable_autopilot_rollout(repo, "source-test")

        rollout = _read_rollout_config(metadata_file)
        assert rollout["enableProgressiveRollout"] is False
        assert rollout["defaultRolloutMode"] == "autopilot"
        assert rollout["autopilotConfig"]["strategy"] == "slow"

        # Re-enabling flips the toggle back on and preserves the retained config.
        result = enable_autopilot_rollout(repo, "source-test")
        assert result.progressive_rollout_enabled is True
        assert result.strategy == "slow"
        rollout = _read_rollout_config(metadata_file)
        assert rollout["enableProgressiveRollout"] is True


@pytest.mark.unit
@pytest.mark.parametrize(
    "data,expected",
    [
        pytest.param(
            {
                "releases": {
                    "rolloutConfiguration": {
                        "defaultRolloutMode": "autopilot",
                        "enableProgressiveRollout": True,
                    }
                }
            },
            True,
            id="autopilot_mode_and_flag_on",
        ),
        pytest.param(
            {
                "releases": {
                    "rolloutConfiguration": {
                        "defaultRolloutMode": "autopilot",
                        "enableProgressiveRollout": False,
                    }
                }
            },
            False,
            id="autopilot_mode_but_flag_off",
        ),
        pytest.param(
            {
                "releases": {
                    "rolloutConfiguration": {
                        "defaultRolloutMode": "manual",
                        "enableProgressiveRollout": True,
                    }
                }
            },
            False,
            id="flag_on_but_not_autopilot_mode",
        ),
        pytest.param(
            {"releases": {"rolloutConfiguration": {"defaultRolloutMode": "autopilot"}}},
            False,
            id="autopilot_mode_but_flag_absent",
        ),
        pytest.param(
            {"releases": {"rolloutConfiguration": {}}},
            False,
            id="empty_rollout_configuration",
        ),
        pytest.param(
            {"releases": {}},
            False,
            id="no_rollout_configuration",
        ),
        pytest.param(
            {},
            False,
            id="no_releases",
        ),
    ],
)
def test_is_autopilot_rollout_enabled(data: dict, expected: bool) -> None:
    """`is_autopilot_rollout_enabled` requires both autopilot mode and the toggle."""
    assert is_autopilot_rollout_enabled(data) is expected
