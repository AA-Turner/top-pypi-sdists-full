"""Tests for ``_detect_next_feature_number``."""

import json
from pathlib import Path
from unittest.mock import patch

from agentic_devtools.cli.speckit.scaffold_new_feature import _detect_next_feature_number


def test_detect_next_feature_number_reads_existing_numbers(tmp_path: Path) -> None:
    specs_dir = tmp_path / "specs"
    feature_dir = specs_dir / "007-something"
    feature_dir.mkdir(parents=True)
    (feature_dir / "feature.json").write_text(json.dumps({"FEATURE_NUM": "7"}), encoding="utf-8")
    with patch(
        "subprocess.run",
        return_value=type(
            "Completed", (), {"stdout": "refs/heads/001-first\nrefs/heads/010-latest\n", "returncode": 0}
        )(),
    ):
        assert _detect_next_feature_number(tmp_path) == 11


def test_detect_next_feature_number_handles_empty_repo(tmp_path: Path) -> None:
    with patch("subprocess.run", side_effect=OSError):
        assert _detect_next_feature_number(tmp_path) == 1


def test_detect_next_feature_number_uses_only_dir_prefix_not_feature_json(tmp_path: Path) -> None:
    # The allocator must match the legacy bash behaviour: only the three-digit directory
    # prefix contributes to the sequence. Stale or inconsistent feature.json metadata
    # (e.g. FEATURE_NUM=100 in a 007-x directory) must not jump the sequence forward.
    stale_dir = tmp_path / "specs" / "007-stale"
    stale_dir.mkdir(parents=True)
    (stale_dir / "feature.json").write_text(json.dumps({"FEATURE_NUM": "100"}), encoding="utf-8")
    with patch("subprocess.run", return_value=type("Completed", (), {"stdout": "", "returncode": 0})()):
        assert _detect_next_feature_number(tmp_path) == 8


def test_detect_next_feature_number_scans_legacy_dirs_without_feature_json(tmp_path: Path) -> None:
    # Legacy directories may not have feature.json but still occupy numbers
    specs_dir = tmp_path / "specs"
    legacy_dir = specs_dir / "007-legacy-feature"
    legacy_dir.mkdir(parents=True)
    # A non-numeric directory should be ignored (exercises the if-match-false branch)
    (specs_dir / "templates").mkdir()
    # No feature.json in the numeric directory
    with patch("subprocess.run", return_value=type("Completed", (), {"stdout": "", "returncode": 0})()):
        assert _detect_next_feature_number(tmp_path) == 8


def test_detect_next_feature_number_ignores_explicit_issue_directories(tmp_path: Path) -> None:
    # An explicit-issue directory (e.g. scaffolded with --issue 3933) uses an issue number,
    # not the legacy sequence, and must not participate in legacy auto-number allocation.
    specs_dir = tmp_path / "specs"
    explicit_dir = specs_dir / "3933-explicit-issue"
    explicit_dir.mkdir(parents=True)
    (explicit_dir / "feature.json").write_text(json.dumps({"FEATURE_NUM": "3933"}), encoding="utf-8")
    # A nested task directory under a parent feature also uses issue metadata, not the
    # legacy namespace, even though its own name happens to match the three-digit pattern.
    nested_task_dir = explicit_dir / "004-nested-task"
    nested_task_dir.mkdir(parents=True)
    (nested_task_dir / "feature.json").write_text(json.dumps({"FEATURE_NUM": "4"}), encoding="utf-8")
    with patch("subprocess.run", return_value=type("Completed", (), {"stdout": "", "returncode": 0})()):
        assert _detect_next_feature_number(tmp_path) == 1


def test_detect_next_feature_number_ignores_explicit_three_digit_directory_and_branch(tmp_path: Path) -> None:
    specs_dir = tmp_path / "specs"
    explicit_dir = specs_dir / "123-explicit-issue"
    explicit_dir.mkdir(parents=True)
    (explicit_dir / "feature.json").write_text(
        json.dumps({"FEATURE_NUM": "123", "BRANCH_NAME": "123-explicit-issue", "NUMBER_SOURCE": "explicit"}),
        encoding="utf-8",
    )
    (specs_dir / "124-explicit-without-branch").mkdir()
    (specs_dir / "124-explicit-without-branch" / "feature.json").write_text(
        json.dumps({"NUMBER_SOURCE": "explicit", "BRANCH_NAME": None}), encoding="utf-8"
    )
    (specs_dir / "125-malformed").mkdir()
    (specs_dir / "125-malformed" / "feature.json").write_text("{", encoding="utf-8")
    with patch(
        "subprocess.run",
        return_value=type(
            "Completed", (), {"stdout": "refs/heads/123-explicit-issue\nrefs/heads/007-legacy\n", "returncode": 0}
        )(),
    ):
        assert _detect_next_feature_number(tmp_path) == 126


def test_detect_next_feature_number_includes_remote_branches(tmp_path: Path) -> None:
    # Full remote refs include the remote name before the legacy branch name.
    with patch(
        "subprocess.run",
        return_value=type(
            "Completed",
            (),
            {
                "stdout": "refs/heads/005-local\nrefs/remotes/origin/042-remote-feature\n",
                "returncode": 0,
            },
        )(),
    ):
        assert _detect_next_feature_number(tmp_path) == 43


def test_detect_next_feature_number_ignores_namespaced_local_branches(tmp_path: Path) -> None:
    with patch(
        "subprocess.run",
        return_value=type(
            "Completed",
            (),
            {
                "stdout": ("refs/heads/feature/042-local\nrefs/remotes/origin/041/remote-nested\nrefs/tags/999-tag\n"),
                "returncode": 0,
            },
        )(),
    ):
        assert _detect_next_feature_number(tmp_path) == 1


def test_detect_next_feature_number_skips_fetch_in_dry_run(tmp_path: Path) -> None:
    # With dry_run=True the git fetch should be skipped; only for-each-ref is called.
    calls: list[list[str]] = []

    def record(cmd: list[str], **_: object) -> object:
        calls.append(list(cmd))
        return type("Completed", (), {"stdout": "refs/heads/003-existing\n", "returncode": 0})()

    with patch("subprocess.run", side_effect=record):
        result = _detect_next_feature_number(tmp_path, dry_run=True)

    assert result == 4
    # Only the for-each-ref invocation should be present; no fetch call.
    assert all("fetch" not in cmd for cmd in calls)
