"""Behavioral tests for resolve-cascade-target.sh."""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT_PATH = REPO_ROOT / ".github" / "scripts" / "speckit-trigger" / "resolve-cascade-target.sh"
BASH_PATH = shutil.which("bash")
HAS_BASH = BASH_PATH is not None


def _run_resolver(specs_dir: Path, issue_number: int) -> subprocess.CompletedProcess[str]:
    return subprocess.run(  # noqa: S603
        [BASH_PATH or "bash", str(SCRIPT_PATH), "--issue", str(issue_number), "--spec-base-path", str(specs_dir)],
        capture_output=True,
        text=True,
    )


@pytest.mark.skipif(not HAS_BASH, reason="bash is required for resolve-cascade-target shell tests")
class TestResolveCascadeTarget:
    """Verify fail-closed hierarchy resolution behavior."""

    def test_rejects_duplicate_issue_hierarchy_candidates(self, tmp_path: Path) -> None:
        specs_dir = tmp_path / "specs"
        for name in ("42-feature-a", "42-feature-b"):
            issue_dir = specs_dir / name
            issue_dir.mkdir(parents=True)
            (issue_dir / "hierarchy.yml").write_text("level: feature\n", encoding="utf-8")

        result = _run_resolver(specs_dir, 42)

        assert result.returncode == 1
        assert "Multiple hierarchy.yml candidates found for issue #42" in result.stderr

    def test_rejects_duplicate_parent_hierarchy_candidates(self, tmp_path: Path) -> None:
        specs_dir = tmp_path / "specs"
        task_dir = specs_dir / "42-task"
        task_dir.mkdir(parents=True)
        (task_dir / "hierarchy.yml").write_text("level: task\nparent: 7\n", encoding="utf-8")
        for name in ("7-feature-a", "7-feature-b"):
            parent_dir = specs_dir / name
            parent_dir.mkdir(parents=True)
            (parent_dir / "hierarchy.yml").write_text("level: feature\n", encoding="utf-8")

        result = _run_resolver(specs_dir, 42)

        assert result.returncode == 1
        assert "Multiple parent hierarchy.yml candidates found for task #42" in result.stderr

    def test_rejects_task_that_declares_itself_as_parent(self, tmp_path: Path) -> None:
        specs_dir = tmp_path / "specs"
        task_dir = specs_dir / "42-task"
        task_dir.mkdir(parents=True)
        (task_dir / "hierarchy.yml").write_text("level: task\nparent: 42\n", encoding="utf-8")

        result = _run_resolver(specs_dir, 42)

        assert result.returncode == 1
        assert "declares itself as parent" in result.stderr

    def test_resolves_parent_number_with_hash_prefix(self, tmp_path: Path) -> None:
        specs_dir = tmp_path / "specs"
        task_dir = specs_dir / "42-task"
        task_dir.mkdir(parents=True)
        (task_dir / "hierarchy.yml").write_text('level: task\nparent: "#7" # parent issue\n', encoding="utf-8")

        parent_dir = specs_dir / "7-feature"
        parent_dir.mkdir(parents=True)
        parent_hierarchy = parent_dir / "hierarchy.yml"
        parent_hierarchy.write_text("level: feature\n", encoding="utf-8")

        result = _run_resolver(specs_dir, 42)

        assert result.returncode == 0
        assert "MODE=next-sibling" in result.stdout
        assert f"HIERARCHY_YML={parent_hierarchy}" in result.stdout

    def test_rejects_conflicting_declared_parent_for_nested_task(self, tmp_path: Path) -> None:
        specs_dir = tmp_path / "specs"
        task_dir = specs_dir / "7-feature" / "42-task"
        task_dir.mkdir(parents=True)
        (task_dir / "hierarchy.yml").write_text("level: task\nparent: 8\n", encoding="utf-8")

        parent_dir = specs_dir / "7-feature"
        (parent_dir / "hierarchy.yml").write_text("level: feature\n", encoding="utf-8")

        result = _run_resolver(specs_dir, 42)

        assert result.returncode == 1
        assert "declares parent #8, but nested hierarchy infers a different parent directory" in result.stderr

    def test_rejects_duplicate_declared_parent_candidates_for_nested_task(self, tmp_path: Path) -> None:
        specs_dir = tmp_path / "specs"
        task_dir = specs_dir / "8-feature" / "42-task"
        task_dir.mkdir(parents=True)
        (task_dir / "hierarchy.yml").write_text("level: task\nparent: 8\n", encoding="utf-8")

        parent_dir = specs_dir / "8-feature"
        (parent_dir / "hierarchy.yml").write_text("level: feature\n", encoding="utf-8")
        for name in ("8-feature-a", "8-feature-b"):
            declared_parent_dir = specs_dir / name
            declared_parent_dir.mkdir(parents=True)
            (declared_parent_dir / "hierarchy.yml").write_text("level: feature\n", encoding="utf-8")

        result = _run_resolver(specs_dir, 42)

        assert result.returncode == 1
        assert "Multiple parent hierarchy.yml candidates found for task #42" in result.stderr

    def test_rejects_malformed_level_declaration(self, tmp_path: Path) -> None:
        specs_dir = tmp_path / "specs"
        issue_dir = specs_dir / "42-feature"
        issue_dir.mkdir(parents=True)
        (issue_dir / "hierarchy.yml").write_text('level: "feature\n', encoding="utf-8")

        result = _run_resolver(specs_dir, 42)

        assert result.returncode == 1
        assert "Empty hierarchy level" in result.stderr

    def test_rejects_duplicate_level_declarations(self, tmp_path: Path) -> None:
        specs_dir = tmp_path / "specs"
        issue_dir = specs_dir / "42-feature"
        issue_dir.mkdir(parents=True)
        (issue_dir / "hierarchy.yml").write_text("level: feature\nlevel: task\n", encoding="utf-8")

        result = _run_resolver(specs_dir, 42)

        assert result.returncode == 1
        assert "must contain exactly one 'level:' field" in result.stderr
