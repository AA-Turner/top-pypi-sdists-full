"""Tests for writing SpecKit hierarchy results to stdout and Actions outputs."""

import json

from agentic_devtools.cli.speckit.resolve_hierarchy import Resolution, _write_outputs


def test_write_outputs_always_prints_json_and_appends_actions_outputs(tmp_path, monkeypatch, capsys) -> None:
    resolution = Resolution("task", "specs/42-task", "specs/10-parent/spec.md", "10", "parent-spec-found")
    monkeypatch.delenv("GITHUB_OUTPUT", raising=False)
    _write_outputs(resolution)
    assert json.loads(capsys.readouterr().out) == {
        "hierarchy_level": "task",
        "spec_dir": "specs/42-task",
        "spec_context": "specs/10-parent/spec.md",
        "parent_number": "10",
        "reason": "parent-spec-found",
    }

    output = tmp_path / "github-output"
    monkeypatch.setenv("GITHUB_OUTPUT", str(output))
    _write_outputs(Resolution("feature", "specs/42\nnoise", "", "", "task-without-parent"))
    assert output.read_text(encoding="utf-8").splitlines() == [
        "hierarchy_level=feature",
        "spec_dir=specs/42noise",
        "spec_context=",
        "parent_number=",
        "reason=task-without-parent",
    ]
