"""Regression: a directory with code files but no .git / pyproject.toml
must still be treated as a project so retrieve uses a per-project
GraphRAG index, not the contaminated home DB.

Observed 2026-05-18: orchestrator-driven sessions in
/tmp/drydock_100/<safe>/ that have a main.py but no .git fell back to
~/.drydock/graphrag.sqlite, which indexed drydock's own /data3/drydock
docs. The model "retrieved" drydock design notes when the user asked
about an entirely different project.
"""
from __future__ import annotations

from pathlib import Path

import pytest

from drydock.core.tools.builtins.retrieve import (
    _looks_like_project,
    _resolve_db_path,
)


def test_explicit_marker_recognized(tmp_path: Path) -> None:
    (tmp_path / ".git").mkdir()
    assert _looks_like_project(tmp_path) is True


def test_pyproject_recognized(tmp_path: Path) -> None:
    (tmp_path / "pyproject.toml").write_text("[project]\nname='x'\n")
    assert _looks_like_project(tmp_path) is True


def test_bare_python_file_recognized(tmp_path: Path) -> None:
    """The bug: a dir with just a .py file used to NOT count as a project."""
    (tmp_path / "main.py").write_text("print('hi')\n")
    assert _looks_like_project(tmp_path) is True


def test_bare_markdown_recognized(tmp_path: Path) -> None:
    (tmp_path / "README.md").write_text("# project\n")
    assert _looks_like_project(tmp_path) is True


def test_empty_dir_not_a_project(tmp_path: Path) -> None:
    assert _looks_like_project(tmp_path) is False


def test_only_unrelated_files_not_a_project(tmp_path: Path) -> None:
    (tmp_path / "data.csv").write_text("a,b\n1,2\n")
    (tmp_path / "image.png").write_bytes(b"\x89PNG")
    assert _looks_like_project(tmp_path) is False


def test_resolve_db_path_uses_project_dir_with_only_python(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The end-to-end shape: a python-bearing dir should resolve to its
    own .drydock/graphrag.sqlite, not the home one."""
    (tmp_path / "main.py").write_text("x = 1\n")
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("DRYDOCK_GRAPHRAG_DB", raising=False)
    p = _resolve_db_path("")
    assert p == tmp_path / ".drydock" / "graphrag.sqlite"
