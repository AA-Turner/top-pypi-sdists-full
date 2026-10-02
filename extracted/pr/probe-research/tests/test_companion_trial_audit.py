"""The daemon-mode trial audit (plan T21): the acceptance bar a re-run must clear."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

AGENT = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location("companion_trial_audit", AGENT / "scripts" / "companion_trial_audit.py")
audit_mod = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = audit_mod
_spec.loader.exec_module(audit_mod)

P = "pro" + "be"


def _session(tmp_path: Path, calls: list[tuple[str, dict, str, bool]]) -> Path:
    """`[(tool, input, result text, is_error)]` as a Claude Code transcript."""
    lines = []
    for i, (tool, args, result, error) in enumerate(calls):
        lines.append({"type": "assistant", "timestamp": f"2026-09-23T08:00:{i * 2:02d}Z", "message": {
            "content": [{"type": "tool_use", "id": f"t{i}", "name": tool, "input": args}]}})
        lines.append({"type": "user", "timestamp": f"2026-09-23T08:00:{i * 2 + 1:02d}Z", "message": {
            "content": [{"type": "tool_result", "tool_use_id": f"t{i}", "content": result, "is_error": error}]}})
    path = tmp_path / "t.jsonl"
    path.write_text("\n".join(json.dumps(line) for line in lines) + "\n")
    return path


def test_a_session_that_just_does_the_work_passes(tmp_path):
    path = _session(tmp_path, [
        ("Bash", {"command": f"{P} project create digits-sweep-daemon-2 --kind training"}, "created", False),
        ("Bash", {"command": f"{P} group create svm-sweep --project digits-sweep-daemon-2"}, "created", False),
        ("Bash", {"command": f"cd ~/trials/digits-daemon-2 && {P} exec --project x -- python run.py"}, "ok", False),
    ])
    result = audit_mod.audit(path)
    assert result["checks"] == {"no_gate_source_reads": True, "group_create_not_refused": True,
                                "no_directed_creates": True, "fewer_calls_than_baseline": True}
    assert audit_mod.main([str(path)]) == 0


def test_the_first_trials_failures_are_each_caught(tmp_path):
    path = _session(tmp_path, [
        ("Bash", {"command": "sed -n 1,60p $P/cli/write_gate.py"}, "...", False),
        ("Bash", {"command": f"{P} project create digits --kind training --directed"}, "created", False),
        ("Bash", {"command": f"{P} group create --help"}, "usage", False),  # reading flags is not a create
        ("Bash", {"command": f"{P} group create svm --project digits"}, "refused: the daemon records", True),
    ])
    result = audit_mod.audit(path)
    assert result["checks"]["no_gate_source_reads"] is False
    assert result["checks"]["no_directed_creates"] is False
    assert result["checks"]["group_create_not_refused"] is False
    assert [g["command"] for g in result["group_creates"]] == [f"{P} group create svm --project digits"]
    assert audit_mod.main([str(path)]) == 1


def test_a_group_create_that_failed_on_the_agents_own_bad_id_is_not_a_refusal(tmp_path):
    path = _session(tmp_path, [("Bash", {"command": f"{P} group create svm --experiment ''"}, "error: Not Found", True)])
    result = audit_mod.audit(path)
    assert result["checks"]["group_create_not_refused"] is True
    assert result["group_creates"][0]["error"] is True and result["group_creates"][0]["refused"] is False
