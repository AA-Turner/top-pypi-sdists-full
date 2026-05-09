"""Tests for sage.core.startup_hints."""

from __future__ import annotations

from pathlib import Path

from sage.core.startup_hints import run_startup_devops_hints


def test_devops_hints_empty_without_git_repo(tmp_path: Path) -> None:
    assert run_startup_devops_hints(tmp_path) == []
