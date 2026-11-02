"""Tests for ``_create_or_checkout_branch``."""

from pathlib import Path
from unittest.mock import patch

from agentic_devtools.cli.speckit.scaffold_new_feature import _create_or_checkout_branch


def test_refreshes_origin_before_reusing_remote_branch(tmp_path: Path) -> None:
    calls: list[list[str]] = []

    def run(args: list[str], **_: object) -> object:
        calls.append(args)
        if args[-1:] == ["refs/heads/42-feature"]:
            return type("Completed", (), {"returncode": 1, "stderr": ""})()
        if args[:4] == ["git", "-C", str(tmp_path), "fetch"]:
            return type("Completed", (), {"returncode": 0, "stderr": ""})()
        if args[-1:] == ["refs/remotes/origin/42-feature"]:
            return type("Completed", (), {"returncode": 0, "stderr": ""})()
        return type("Completed", (), {"returncode": 0, "stderr": ""})()

    with patch("subprocess.run", side_effect=run):
        _create_or_checkout_branch(
            tmp_path,
            "42-feature",
            allow_existing_branch=True,
            dry_run=False,
        )

    assert ["git", "-C", str(tmp_path), "fetch", "origin", "--prune", "--quiet"] in calls
    assert calls[-1] == ["git", "-C", str(tmp_path), "checkout", "--track", "origin/42-feature"]


def test_refreshes_origin_before_rejecting_existing_remote_branch(tmp_path: Path) -> None:
    calls: list[list[str]] = []

    def run(args: list[str], **_: object) -> object:
        calls.append(args)
        if args[-1:] == ["refs/heads/42-feature"]:
            return type("Completed", (), {"returncode": 1, "stderr": ""})()
        if args[:4] == ["git", "-C", str(tmp_path), "fetch"]:
            return type("Completed", (), {"returncode": 0, "stderr": ""})()
        if args[-1:] == ["refs/remotes/origin/42-feature"]:
            return type("Completed", (), {"returncode": 0, "stderr": ""})()
        return type("Completed", (), {"returncode": 0, "stderr": ""})()

    with patch("subprocess.run", side_effect=run):
        try:
            _create_or_checkout_branch(
                tmp_path,
                "42-feature",
                allow_existing_branch=False,
                dry_run=False,
            )
        except ValueError as exc:
            assert "already exists" in str(exc)
        else:  # pragma: no cover - defensive: branch reuse must be rejected
            raise AssertionError("Expected existing remote branch to be rejected")

    assert ["git", "-C", str(tmp_path), "fetch", "origin", "--prune", "--quiet"] in calls


def test_creates_branch_when_refreshed_remote_branch_is_missing(tmp_path: Path) -> None:
    calls: list[list[str]] = []

    def run(args: list[str], **_: object) -> object:
        calls.append(args)
        if args[-1:] in (["refs/heads/42-feature"], ["refs/remotes/origin/42-feature"]):
            return type("Completed", (), {"returncode": 1, "stderr": ""})()
        return type("Completed", (), {"returncode": 0, "stderr": ""})()

    with patch("subprocess.run", side_effect=run):
        _create_or_checkout_branch(
            tmp_path,
            "42-feature",
            allow_existing_branch=True,
            dry_run=False,
        )

    assert calls[-1] == ["git", "-C", str(tmp_path), "checkout", "-b", "42-feature"]
