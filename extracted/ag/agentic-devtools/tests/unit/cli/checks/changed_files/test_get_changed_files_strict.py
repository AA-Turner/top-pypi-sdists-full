"""Tests for strict committed changed-file acquisition."""

from __future__ import annotations

import os
import subprocess
from pathlib import Path
from unittest.mock import patch

import pytest

from agentic_devtools.cli.checks.changed_files import DiffUnavailableError, get_strict_committed_changed_files
from agentic_devtools.git_env import sanitize_git_environment

MODULE = "agentic_devtools.cli.checks.changed_files"
STRICT_COMMAND = ["git", "diff", "--name-only", "-z", "--diff-filter=d", "origin/main...HEAD", "--"]


@pytest.mark.parametrize("cwd", [None, "/repo", Path("/repo")])
def test_exact_command_and_working_directory(cwd):
    paths = [".github/workflows/check.yml", "README.md", "agentic_devtools/_version.py"]
    output = b"\0".join(os.fsencode(path) for path in paths) + b"\0"
    with patch(f"{MODULE}.subprocess.run") as run:
        run.return_value = subprocess.CompletedProcess(STRICT_COMMAND, 0, output)

        assert get_strict_committed_changed_files(cwd) == paths

    run.assert_called_once_with(
        STRICT_COMMAND,
        capture_output=True,
        check=True,
        cwd=str(cwd) if cwd is not None else None,
        shell=False,
    )


def test_nul_delimited_output_preserves_special_filename_bytes():
    paths = ["tab\tname.txt", "line\nbreak.txt", 'quote"and\\escape.txt', "literal\\t.txt"]
    output = b"\0".join(os.fsencode(path) for path in paths) + b"\0"
    with patch(f"{MODULE}.subprocess.run") as run:
        run.return_value = subprocess.CompletedProcess(STRICT_COMMAND, 0, output)

        assert get_strict_committed_changed_files() == paths


@pytest.mark.parametrize("output", [b"", b"\0"])
def test_empty_successful_diff(output):
    with patch(f"{MODULE}.subprocess.run") as run:
        run.return_value = subprocess.CompletedProcess(STRICT_COMMAND, 0, output)

        assert get_strict_committed_changed_files() == []

    run.assert_called_once()


@pytest.mark.parametrize(
    "error",
    [
        FileNotFoundError("git not found"),
        PermissionError("cannot execute git"),
        OSError("invalid working directory"),
        subprocess.CalledProcessError(128, STRICT_COMMAND, stderr="unknown revision origin/main"),
        subprocess.CalledProcessError(128, STRICT_COMMAND, stderr="no merge base"),
        subprocess.CalledProcessError(1, STRICT_COMMAND, stderr="diff failed"),
    ],
)
def test_failure_is_actionable_and_never_falls_back(error, tmp_path):
    with patch(f"{MODULE}.subprocess.run", side_effect=error) as run:
        with pytest.raises(DiffUnavailableError, match="git fetch origin main") as raised:
            get_strict_committed_changed_files(tmp_path)

    assert raised.value.__cause__ is error
    assert str(error) in str(raised.value)
    run.assert_called_once_with(STRICT_COMMAND, capture_output=True, check=True, cwd=str(tmp_path), shell=False)


@pytest.fixture
def committed_repo(tmp_path):
    """Create a local base ref and a HEAD change without remote access."""

    def git(*args):
        return subprocess.run(
            ["git", *args],
            cwd=tmp_path,
            capture_output=True,
            text=True,
            check=True,
            shell=False,
            env=sanitize_git_environment(os.environ),
        )

    git("init")
    git("config", "--local", "user.name", "Strict Diff Test")
    git("config", "--local", "user.email", "strict-diff@example.invalid")
    git("config", "--local", "commit.gpgsign", "false")
    for name in ("committed.txt", "deleted.txt", "staged.txt", "unstaged.txt"):
        (tmp_path / name).write_text(f"base {name}\n", encoding="utf-8")
    git("add", ".")
    git("commit", "-m", "base")
    git("update-ref", "refs/remotes/origin/main", "HEAD")
    (tmp_path / "committed.txt").write_text("committed change\n", encoding="utf-8")
    (tmp_path / "deleted.txt").unlink()
    git("add", "-A")
    git("commit", "-m", "committed change and deletion")
    (tmp_path / "staged.txt").write_text("staged change\n", encoding="utf-8")
    git("add", "staged.txt")
    (tmp_path / "unstaged.txt").write_text("unstaged change\n", encoding="utf-8")
    (tmp_path / "untracked.txt").write_text("untracked change\n", encoding="utf-8")
    return tmp_path


def test_only_committed_paths_are_returned(committed_repo, monkeypatch):
    monkeypatch.chdir(committed_repo)
    real_run = subprocess.run
    with patch(f"{MODULE}.subprocess.run", wraps=real_run) as run:
        assert get_strict_committed_changed_files() == ["committed.txt"]

    run.assert_called_once_with(STRICT_COMMAND, capture_output=True, check=True, cwd=None, shell=False)


def test_committed_deletion_is_filtered(committed_repo):
    unfiltered = subprocess.run(
        ["git", "diff", "--name-only", "origin/main...HEAD", "--"],
        cwd=committed_repo,
        env=sanitize_git_environment(os.environ),
        capture_output=True,
        text=True,
        check=True,
        shell=False,
    )
    assert "deleted.txt" in unfiltered.stdout.splitlines()
    assert get_strict_committed_changed_files(committed_repo) == ["committed.txt"]


def test_unicode_committed_filename_is_decoded(committed_repo):
    filename = "café.txt"
    (committed_repo / filename).write_text("unicode path\n", encoding="utf-8")
    subprocess.run(
        ["git", "add", "--", filename],
        cwd=committed_repo,
        env=sanitize_git_environment(os.environ),
        capture_output=True,
        text=True,
        check=True,
        shell=False,
    )
    subprocess.run(
        ["git", "commit", "--only", "-m", "add unicode filename", "--", filename],
        cwd=committed_repo,
        env=sanitize_git_environment(os.environ),
        capture_output=True,
        text=True,
        check=True,
        shell=False,
    )

    assert get_strict_committed_changed_files(committed_repo) == ["café.txt", "committed.txt"]


def test_missing_base_raises_without_fallback(committed_repo):
    subprocess.run(
        ["git", "update-ref", "-d", "refs/remotes/origin/main"],
        cwd=committed_repo,
        env=sanitize_git_environment(os.environ),
        capture_output=True,
        text=True,
        check=True,
        shell=False,
    )
    real_run = subprocess.run
    with patch(f"{MODULE}.subprocess.run", wraps=real_run) as run:
        with pytest.raises(DiffUnavailableError, match="git fetch origin main") as raised:
            get_strict_committed_changed_files(committed_repo)

    assert isinstance(raised.value.__cause__, subprocess.CalledProcessError)
    run.assert_called_once_with(STRICT_COMMAND, capture_output=True, check=True, cwd=str(committed_repo), shell=False)
