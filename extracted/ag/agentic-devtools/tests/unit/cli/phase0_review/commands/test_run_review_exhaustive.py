"""Tests for commands.run_review nominal and exhaustive paths."""

import hashlib
import json
from unittest.mock import patch

import pytest

from agentic_devtools import state
from agentic_devtools.cli.phase0_review import commands
from agentic_devtools.cli.phase0_review.commands import run_review


def test_run_review_approves_matching_case(make_review_case, tmp_path):
    payload, integrity = make_review_case()
    report = run_review(repo_root=tmp_path, input_path=payload, integrity_path=integrity)
    assert report.endswith("APPROVED\nconfidence: 100%")


def test_run_review_reports_every_discrepancy(make_review_case, tmp_path):
    payload, integrity = make_review_case(issue_title="Wrong")
    report = run_review(repo_root=tmp_path, input_path=payload, integrity_path=integrity)
    assert report.endswith("CHANGES REQUESTED")
    assert report.count('Field "title"') == 2


def test_run_review_reports_missing_and_malformed_inputs(tmp_path):
    missing = run_review(
        repo_root=tmp_path,
        input_path=tmp_path / "missing.json",
        integrity_path=tmp_path / "missing-integrity.json",
    )
    assert "Missing input" in missing
    directory = run_review(repo_root=tmp_path, input_path=tmp_path, integrity_path=tmp_path)
    assert directory.count("Malformed input") == 1


def test_run_review_handles_repository_state_and_invalid_artifacts(make_review_case, tmp_path, temp_state_dir, capsys):
    with patch.object(commands, "get_repo_root", return_value=None):
        assert "repository root" in run_review()

    payload, integrity = make_review_case()
    state.set_value("phase0.factualReviewInputPath", str(payload))
    state.set_value("phase0.integrityPath", str(integrity))
    with patch.object(commands, "get_repo_root", return_value=tmp_path):
        commands.phase0_review_command()
    assert "APPROVED" in capsys.readouterr().out

    invalid = tmp_path / "invalid-payload.json"
    invalid.write_text("{")
    report = run_review(repo_root=tmp_path, input_path=invalid, integrity_path=integrity)
    assert "valid UTF-8 JSON" in report

    escaped = run_review(repo_root=tmp_path, input_path="../escape.json", integrity_path=integrity)
    assert "outside the repository" in escaped
    empty = run_review(repo_root=tmp_path, input_path=123, integrity_path=integrity)
    assert "state key is absent or empty" in empty

    with patch.object(commands, "run_review", return_value="## Verdict\nCHANGES REQUESTED"):
        with pytest.raises(SystemExit, match="1"):
            commands.phase0_review_command()

    with patch.object(commands, "run_review", return_value="## Verdict\nAPPROVED\nfooter"):
        commands.phase0_review_command()

    with patch.object(commands, "run_review", return_value="prefix ## Verdict suffix\nAPPROVED"):
        commands.phase0_review_command()
    assert "ERROR" not in capsys.readouterr().out

    with patch.object(commands, "run_review", return_value="no verdict heading here"):
        with pytest.raises(SystemExit, match="1"):
            commands.phase0_review_command()
    assert "ERROR: report is missing a complete verdict section" in capsys.readouterr().out

    with patch.object(commands, "run_review", return_value="## Verdict"):
        with pytest.raises(SystemExit, match="1"):
            commands.phase0_review_command()
    assert "ERROR: report is missing a complete verdict section" in capsys.readouterr().out


def test_run_review_reports_invalid_utf8_artifact_and_non_mapping_source(make_review_case, tmp_path):
    payload, integrity = make_review_case()
    (tmp_path / "template.md").write_bytes(b"\xff")
    report = run_review(repo_root=tmp_path, input_path=payload, integrity_path=integrity)
    assert "readable UTF-8" in report

    payload.write_text('{"schema_version":"phase0_factual_review_input/v1","source":[],"issue_md":{},"template":{}}')
    report = run_review(repo_root=tmp_path, input_path=payload, integrity_path=None)
    assert "source is an object" in report


def test_run_review_bails_when_issue_md_or_snapshot_is_not_utf8(make_review_case, tmp_path):
    payload, integrity = make_review_case()
    (tmp_path / "issue.md").write_bytes(b"\xff\xfe invalid utf-8")
    report = run_review(repo_root=tmp_path, input_path=payload, integrity_path=integrity)
    assert "readable UTF-8" in report
    assert "CHANGES REQUESTED" in report

    payload2, integrity2 = make_review_case()
    (tmp_path / "structure_snapshot.md").write_bytes(b"\xff\xfe invalid utf-8")
    report2 = run_review(repo_root=tmp_path, input_path=payload2, integrity_path=integrity2)
    assert "readable UTF-8" in report2
    assert "CHANGES REQUESTED" in report2


def test_run_review_skips_comparison_when_loaded_source_is_not_mapping(make_review_case, tmp_path):
    payload, integrity = make_review_case()
    data = json.loads(payload.read_text())
    data["source"] = []
    payload.write_text(json.dumps(data))
    metadata = json.loads(integrity.read_text())
    metadata["payload_sha256"] = hashlib.sha256(payload.read_bytes()).hexdigest()
    integrity.write_text(json.dumps(metadata))
    report = run_review(repo_root=tmp_path, input_path=payload, integrity_path=integrity)
    assert "source is an object" in report


def test_state_artifact_io_errors_are_missing_inputs(tmp_path):
    with patch("pathlib.Path.exists", side_effect=OSError("denied")):
        report = run_review(repo_root=tmp_path, input_path="payload.json")
    assert 'Missing input: "factual-review payload"' in report

    with patch.object(commands, "resolve_safe_path", return_value=(None, None)):
        report = run_review(repo_root=tmp_path, input_path="payload.json")
    assert "path was not resolved" in report


def test_artifact_read_io_error_is_missing_input(make_review_case, tmp_path):
    payload, integrity = make_review_case()
    original = commands.Path.read_bytes

    def read_bytes(path):
        if path.name == "issue.md":
            raise OSError("denied")
        return original(path)

    with patch.object(commands.Path, "read_bytes", read_bytes):
        report = run_review(repo_root=tmp_path, input_path=payload, integrity_path=integrity)
    assert 'Missing input: "issue_md.path"' in report
