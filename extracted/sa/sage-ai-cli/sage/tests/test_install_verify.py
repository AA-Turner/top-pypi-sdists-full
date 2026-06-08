"""Tests for install_verify.

This module is the "actually install and run the code" layer the user
demanded. Tests cover:

  - Project discovery by walking the tree (not hardcoded layout).
  - Step execution returns structured results with logs.
  - Steps are gated on whether the relevant tool/file exists.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from unittest.mock import patch

import pytest

from sage.core.install_verify import (
    DiscoveredProject,
    StepResult,
    discover_projects,
    run_step,
    verify_project,
)


class TestDiscoverProjects:
    def test_finds_python_project_by_requirements(self, tmp_path: Path) -> None:
        backend = tmp_path / "backend"
        backend.mkdir()
        (backend / "requirements.txt").write_text("fastapi==0.115.6\n")
        projects = discover_projects(tmp_path)
        assert any(p.kind == "python" and p.root == backend for p in projects)

    def test_finds_python_project_by_pyproject(self, tmp_path: Path) -> None:
        backend = tmp_path / "backend"
        backend.mkdir()
        (backend / "pyproject.toml").write_text(
            '[project]\nname = "x"\nversion = "0"\nrequires-python = ">=3.10"\n'
        )
        projects = discover_projects(tmp_path)
        assert any(p.kind == "python" for p in projects)

    def test_finds_node_project_by_package_json(self, tmp_path: Path) -> None:
        frontend = tmp_path / "frontend"
        frontend.mkdir()
        (frontend / "package.json").write_text('{"name":"x"}')
        projects = discover_projects(tmp_path)
        assert any(p.kind == "node" and p.root == frontend for p in projects)

    def test_finds_both_in_sibling_layout(self, tmp_path: Path) -> None:
        (tmp_path / "frontend").mkdir()
        (tmp_path / "frontend" / "package.json").write_text('{"name":"f"}')
        (tmp_path / "backend").mkdir()
        (tmp_path / "backend" / "requirements.txt").write_text("fastapi\n")
        projects = discover_projects(tmp_path)
        kinds = {p.kind for p in projects}
        assert kinds == {"python", "node"}

    def test_ignores_nested_node_modules(self, tmp_path: Path) -> None:
        # A package.json INSIDE node_modules should not be treated as a project
        nested = tmp_path / "frontend" / "node_modules" / "lib"
        nested.mkdir(parents=True)
        (nested / "package.json").write_text('{"name":"lib"}')
        # but the real one IS a project
        (tmp_path / "frontend" / "package.json").write_text('{"name":"f"}')
        projects = discover_projects(tmp_path)
        roots = [p.root for p in projects]
        assert tmp_path / "frontend" in roots
        assert nested not in roots

    def test_ignores_venv(self, tmp_path: Path) -> None:
        venv = tmp_path / "backend" / "venv" / "lib"
        venv.mkdir(parents=True)
        # The venv may contain pyproject.tomls for installed packages
        (venv / "pyproject.toml").write_text('[project]\nname="installed"\nversion="0"\nrequires-python=">=3"\n')
        (tmp_path / "backend").joinpath("requirements.txt").write_text("fastapi\n")
        projects = discover_projects(tmp_path)
        for p in projects:
            assert "venv" not in p.root.parts


class TestRunStep:
    def test_returns_ok_for_successful_command(self, tmp_path: Path) -> None:
        result = run_step("test", ["python", "-c", "print('ok')"], cwd=tmp_path)
        assert result.ok
        assert "ok" in result.log

    def test_captures_failure_log(self, tmp_path: Path) -> None:
        result = run_step("fail", ["python", "-c", "import sys; sys.exit(3)"], cwd=tmp_path)
        assert not result.ok
        assert result.returncode == 3

    def test_returns_skipped_when_command_missing(self, tmp_path: Path) -> None:
        result = run_step("missing", ["definitely_not_a_real_command_xyzzy"], cwd=tmp_path)
        assert not result.ok
        assert result.returncode != 0  # FileNotFoundError → marked as failure


class TestVerifyProject:
    def test_python_project_runs_pip_and_pytest(self, tmp_path: Path) -> None:
        backend = tmp_path / "backend"
        backend.mkdir()
        (backend / "requirements.txt").write_text("")  # no real deps
        (backend / "pyproject.toml").write_text(
            "[build-system]\nrequires = [\"setuptools>=68.0\"]\n"
            "build-backend = \"setuptools.build_meta\"\n\n"
            '[project]\nname = "x"\nversion = "0"\nrequires-python = ">=3.10"\n'
        )
        # tiny passing test
        tests = backend / "tests"
        tests.mkdir()
        (tests / "__init__.py").write_text("")
        (tests / "test_smoke.py").write_text("def test_ok():\n    assert True\n")

        project = DiscoveredProject(kind="python", root=backend)
        results = verify_project(project)
        step_names = [r.name for r in results]
        assert "pip install" in step_names or any("install" in n for n in step_names)
        assert any("test" in n for n in step_names)
