"""Tests for loading supervisor configuration."""

import json

import pytest

from agentic_devtools.cli.ci.supervisor import SupervisorConfig
from agentic_devtools.cli.ci.supervisor_command import load_supervisor_config


def test_load_supervisor_config_returns_defaults_without_path(tmp_path) -> None:
    config = load_supervisor_config(tmp_path / "missing.json")

    assert config.max_candidates == 10
    assert config.thresholds == SupervisorConfig()
    assert config.mode == "report_only"


def test_load_supervisor_config_reads_thresholds_and_limit(tmp_path) -> None:
    path = tmp_path / "config.json"
    path.write_text(
        json.dumps(
            {
                "mode": "diagnose_only",
                "max_candidates": 3,
                "thresholds": {
                    "loop_stale_seconds": 60,
                    "task_stale_seconds": 120,
                    "review_wait_seconds": 180,
                },
            }
        ),
        encoding="utf-8",
    )

    config = load_supervisor_config(path)

    assert config.mode == "diagnose_only"
    assert config.max_candidates == 3
    assert config.thresholds == SupervisorConfig(60, 120, 180)


def test_load_supervisor_config_rejects_malformed_values(tmp_path) -> None:
    path = tmp_path / "config.json"
    path.write_text(json.dumps({"max_candidates": 0}), encoding="utf-8")

    with pytest.raises(ValueError, match="max_candidates"):
        load_supervisor_config(path)


@pytest.mark.parametrize(
    "payload,match",
    [
        ("not-json", "could not load"),
        ("[]", "JSON object"),
        (json.dumps({"mode": ""}), "mode"),
        (json.dumps({"thresholds": []}), "thresholds"),
        (json.dumps({"thresholds": {"loop_stale_seconds": 0}}), "loop_stale_seconds"),
    ],
)
def test_load_supervisor_config_rejects_malformed_documents(tmp_path, payload: str, match: str) -> None:
    path = tmp_path / "config.json"
    path.write_text(payload, encoding="utf-8")

    with pytest.raises(ValueError, match=match):
        load_supervisor_config(path)
