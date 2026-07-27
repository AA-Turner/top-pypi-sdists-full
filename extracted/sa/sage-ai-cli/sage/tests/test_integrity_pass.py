"""Tests for the cross-file integrity pass."""

from __future__ import annotations

from pathlib import Path
from typing import Callable

import pytest

from sage.core.integrity_pass import (
    IntegrityReport,
    _python_files_under,
    run_integrity_pass,
)


def _gen(responses: list[str]) -> Callable[[str], str]:
    it = iter(responses)
    return lambda _: next(it, "")


def _make_project(tmp_path: Path) -> Path:
    """Create a minimal backend project with a known dangling-import bug."""
    backend = tmp_path / "backend"
    pkg = backend / "app"
    pkg.mkdir(parents=True)
    (pkg / "__init__.py").write_text("")
    (pkg / "models.py").write_text(
        "from sqlmodel import SQLModel\n\n"
        "class User(SQLModel, table=True):\n"
        "    id: int\n"
    )
    # api.py imports `get_user_by_id` from models but models doesn't export it
    (pkg / "api.py").write_text(
        "from app.models import User, get_user_by_id\n\n"
        "def list_users():\n"
        "    return get_user_by_id(1)\n"
    )
    return backend


class TestPythonFilesUnder:
    def test_collects_files_recursively(self, tmp_path: Path) -> None:
        backend = _make_project(tmp_path)
        files = _python_files_under(backend)
        # Returns keys like 'app/api.py' (relative to backend)
        paths = set(files.keys())
        assert "app/api.py" in paths
        assert "app/models.py" in paths
        assert "app/__init__.py" in paths

    def test_skips_venv_and_caches(self, tmp_path: Path) -> None:
        backend = _make_project(tmp_path)
        venv = backend / "venv" / "lib"
        venv.mkdir(parents=True)
        (venv / "junk.py").write_text("x")
        cache = backend / "app" / "__pycache__"
        cache.mkdir()
        (cache / "models.cpython.pyc").write_text("x")

        files = _python_files_under(backend)
        for p in files:
            assert "venv" not in p
            assert "__pycache__" not in p


class TestRunIntegrityPass:
    def test_no_dangling_means_no_fixes(self, tmp_path: Path) -> None:
        backend = _make_project(tmp_path)
        # Fix the dangling import first
        (backend / "app" / "api.py").write_text(
            "from app.models import User\n\ndef list_users(): return User\n"
        )
        report = run_integrity_pass(
            tmp_path,
            generate=_gen([]),
            log=lambda _: None,
            enable_ruff_fix=False,
            enable_lint_pass=False,
        )
        assert report.dangling_fixes == 0

    def test_repairs_dangling_import(self, tmp_path: Path) -> None:
        backend = _make_project(tmp_path)
        # LLM stub returns a corrected api.py that drops the bad import
        fixed_api = "from app.models import User\n\ndef list_users(): return User\n"
        report = run_integrity_pass(
            tmp_path,
            generate=_gen([fixed_api]),
            log=lambda _: None,
            enable_ruff_fix=False,
            enable_lint_pass=False,
        )
        assert report.dangling_fixes == 1
        # File was rewritten
        actual = (backend / "app" / "api.py").read_text()
        assert "get_user_by_id" not in actual
        assert "User" in actual

    def test_returns_zero_when_no_backend(self, tmp_path: Path) -> None:
        report = run_integrity_pass(
            tmp_path,
            generate=_gen([]),
            log=lambda _: None,
        )
        assert report.dangling_fixes == 0
        assert report.lint_fixes == 0
        assert report.files_scanned == 0

    def test_handles_unparseable_files_gracefully(self, tmp_path: Path) -> None:
        backend = _make_project(tmp_path)
        # Write an unparseable file
        (backend / "app" / "broken.py").write_text("def broken(:::\n")
        # Should NOT crash
        report = run_integrity_pass(
            tmp_path,
            generate=_gen([""] * 10),
            log=lambda _: None,
            enable_ruff_fix=False,
            enable_lint_pass=False,
        )
        # Pipeline survives the broken file
        assert report.files_scanned >= 3

    def test_skips_empty_generate_response(self, tmp_path: Path) -> None:
        backend = _make_project(tmp_path)
        # Generator returns empty — file should NOT be replaced with empty
        report = run_integrity_pass(
            tmp_path,
            generate=_gen([""]),
            log=lambda _: None,
            enable_ruff_fix=False,
            enable_lint_pass=False,
        )
        # No fix counted (length < 20)
        assert report.dangling_fixes == 0
        # Original file preserved
        original = (backend / "app" / "api.py").read_text()
        assert "get_user_by_id" in original
