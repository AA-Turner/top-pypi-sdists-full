"""Tests for contract.validate_paths."""

import json
from pathlib import Path
from unittest.mock import patch

from agentic_devtools.cli.phase0_review import contract
from agentic_devtools.cli.phase0_review.contract import load_contract, validate_paths


def test_validate_paths_rejects_escape_git_directory_and_missing(make_review_case, tmp_path):
    payload_path, _ = make_review_case()
    data = json.loads(payload_path.read_text())
    data["issue_md"]["path"] = "../escape/issue.md"
    data["template"]["selected_path"] = ".git/config"
    data["template"]["structure_snapshot_path"] = "missing.md"
    _, findings = validate_paths(data, tmp_path)
    text = "\n".join(item.text for item in findings)
    assert "outside the repository" in text
    assert ".git subtree" in text
    assert "does not exist" in text

    data = load_contract(payload_path).data
    assert data is not None
    data["issue_md"]["path"] = "."
    _, findings = validate_paths(data, tmp_path)
    assert any("regular file" in item.text for item in findings)


def test_validate_paths_skips_invalid_shapes_and_reports_absolute_oversized_and_io(make_review_case, tmp_path):
    payload_path, _ = make_review_case()
    data = json.loads(payload_path.read_text())
    data["issue_md"] = []
    data["template"]["selected_path"] = str(tmp_path / "template.md")
    (tmp_path / "structure_snapshot.md").write_bytes(b"x" * 200001)
    _, findings = validate_paths(data, tmp_path)
    text = "\n".join(item.text for item in findings)
    assert "repository-relative" in text
    assert "at most 200000 bytes" in text

    data = json.loads(payload_path.read_text())
    real_exists = Path.exists

    def broken_exists(path):
        if path.name == "issue.md":
            raise OSError("denied")
        return real_exists(path)

    with patch.object(Path, "exists", broken_exists):
        _, findings = validate_paths(data, tmp_path)
    assert any("unreadable" in item.text for item in findings)

    with patch.object(contract, "resolve_safe_path", return_value=(None, None)):
        _, findings = validate_paths(data, tmp_path)
    assert all("path was not resolved" in item.text for item in findings)
