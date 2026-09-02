"""Tests for _record_run_outcome."""

import json
from pathlib import Path

import agentic_devtools.cli.copilot.auto_start as auto_start_module
from agentic_devtools.cli.copilot.auto_start import _record_run_outcome


def _state_file(tmp_path: Path, content: str = "{}") -> Path:
    state_dir = tmp_path / "state"
    state_dir.mkdir()
    path = state_dir / "state.json"
    path.write_text(content, encoding="utf-8")
    return path


class TestRecordRunOutcome:
    def test_records_status_and_exit_code(self, tmp_path):
        path = _state_file(tmp_path)

        _record_run_outcome(path, "run-1", "failed", 1)

        state = json.loads(path.read_text(encoding="utf-8"))
        assert state["copilot"]["auto_start_run_outcomes"]["run-1"] == {
            "status": "failed",
            "exit_code": 1,
        }

    def test_records_status_without_exit_code(self, tmp_path):
        path = _state_file(tmp_path, json.dumps({"copilot": {"model_id": "x"}}))

        _record_run_outcome(path, "run-1", "running")

        state = json.loads(path.read_text(encoding="utf-8"))
        assert state["copilot"]["auto_start_run_outcomes"]["run-1"] == {"status": "running"}
        assert state["copilot"]["model_id"] == "x"

    def test_normalizes_invalid_state_shapes(self, tmp_path):
        path = _state_file(tmp_path, json.dumps({"copilot": {"auto_start_run_outcomes": []}}))

        _record_run_outcome(path, "run-1", "completed", 0)

        state = json.loads(path.read_text(encoding="utf-8"))
        assert state["copilot"]["auto_start_run_outcomes"]["run-1"]["status"] == "completed"

    def test_recovers_from_corrupt_json(self, tmp_path):
        path = _state_file(tmp_path, "{invalid")

        _record_run_outcome(path, "run-1", "running")

        state = json.loads(path.read_text(encoding="utf-8"))
        assert state["copilot"]["auto_start_run_outcomes"]["run-1"]["status"] == "running"

    def test_recovers_from_non_dict_state(self, tmp_path):
        path = _state_file(tmp_path, json.dumps(["invalid"]))

        _record_run_outcome(path, "run-1", "running")

        state = json.loads(path.read_text(encoding="utf-8"))
        assert state["copilot"]["auto_start_run_outcomes"]["run-1"]["status"] == "running"

    def test_swallows_locking_errors(self, tmp_path, monkeypatch, capsys):
        path = _state_file(tmp_path)

        def fail_lock(_):
            raise OSError("locked")

        monkeypatch.setattr(auto_start_module, "locked_state_file", fail_lock)

        _record_run_outcome(path, "run-1", "running")

        assert "could not persist run outcome" in capsys.readouterr().err
