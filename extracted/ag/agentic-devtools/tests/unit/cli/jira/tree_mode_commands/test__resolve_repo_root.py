"""Tests for ``_resolve_repo_root`` (issue #2118).

``_resolve_repo_root`` derives the repository root via
``git rev-parse --show-toplevel`` and raises ``PipelineValidationError`` when
the working directory is not inside a Git repository or the command returns no
output.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

import agentic_devtools.cli.jira.tree_mode_commands as tmc


class TestResolveRepoRoot:
    def test_returns_path_from_git_output(self, monkeypatch):
        completed = subprocess.CompletedProcess(args=[], returncode=0, stdout="/work/repo\n", stderr="")
        monkeypatch.setattr(tmc.subprocess, "run", lambda *a, **k: completed)
        assert tmc._resolve_repo_root() == Path("/work/repo")

    def test_raises_when_not_a_git_repo(self, monkeypatch):
        def _raise(*a, **k):
            raise subprocess.CalledProcessError(128, ["git"])

        monkeypatch.setattr(tmc.subprocess, "run", _raise)
        with pytest.raises(tmc.PipelineValidationError) as exc_info:
            tmc._resolve_repo_root()
        assert "not inside a Git repository" in str(exc_info.value)
        assert exc_info.value.cause is not None

    def test_raises_on_missing_git_binary(self, monkeypatch):
        def _raise(*a, **k):
            raise FileNotFoundError("git not found")

        monkeypatch.setattr(tmc.subprocess, "run", _raise)
        with pytest.raises(tmc.PipelineValidationError):
            tmc._resolve_repo_root()

    def test_raises_on_empty_output(self, monkeypatch):
        completed = subprocess.CompletedProcess(args=[], returncode=0, stdout="  \n", stderr="")
        monkeypatch.setattr(tmc.subprocess, "run", lambda *a, **k: completed)
        with pytest.raises(tmc.PipelineValidationError) as exc_info:
            tmc._resolve_repo_root()
        assert "no output" in str(exc_info.value)
