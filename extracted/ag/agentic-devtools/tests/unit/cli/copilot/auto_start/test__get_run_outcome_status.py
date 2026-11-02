"""Tests for _get_run_outcome_status."""

import json

from agentic_devtools.cli.copilot.auto_start import _get_run_outcome_status


def test_returns_status(tmp_path):
    """Returns the persisted status for the requested run."""
    state_file = tmp_path / "state.json"
    state_file.write_text(
        json.dumps({"copilot": {"auto_start_run_outcomes": {"run-1": {"status": "running"}}}}),
        encoding="utf-8",
    )

    assert _get_run_outcome_status(state_file, "run-1") == "running"


def test_returns_none_for_missing_or_invalid_outcome(tmp_path):
    """Returns None when the requested outcome is missing or malformed."""
    state_file = tmp_path / "state.json"
    state_file.write_text(json.dumps({"copilot": {"auto_start_run_outcomes": []}}), encoding="utf-8")

    assert _get_run_outcome_status(state_file, "run-1") is None


def test_returns_none_for_invalid_state_shapes(tmp_path):
    """Returns None for invalid state, Copilot, or outcome structures."""
    state_file = tmp_path / "state.json"
    for content in (
        "[]",
        json.dumps({"copilot": []}),
        json.dumps({"copilot": {"auto_start_run_outcomes": {"run-1": []}}}),
        json.dumps({"copilot": {"auto_start_run_outcomes": {"run-1": {"status": 1}}}}),
    ):
        state_file.write_text(content, encoding="utf-8")
        assert _get_run_outcome_status(state_file, "run-1") is None


def test_returns_none_for_invalid_json(tmp_path):
    """Returns None when the state file contains invalid JSON."""
    state_file = tmp_path / "state.json"
    state_file.write_text("{", encoding="utf-8")

    assert _get_run_outcome_status(state_file, "run-1") is None
