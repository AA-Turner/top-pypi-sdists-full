"""End-to-end integration test for the flat-to-nested spec migration workflow.

Exercises the full nest pipeline — flat spec discovery, relationship graph
construction, plan computation, cross-reference scanning, and atomic execution
— against a real temporary git repository, with only the GitHub relationship
detector stubbed out.
"""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any
from unittest.mock import patch

import pytest
import yaml

from agentic_devtools.cli.speckit.nest.crossref import scan_crossrefs
from agentic_devtools.cli.speckit.nest.discovery import (
    build_relationship_graph,
    scan_existing_targets,
    scan_flat_specs,
)
from agentic_devtools.cli.speckit.nest.execution import execute_migration
from agentic_devtools.cli.speckit.nest.plan import compute_migration_plan
from agentic_devtools.cli.speckit.nest.readme_index import INDEX_START_MARKER
from agentic_devtools.hierarchy.models import ChildInfo, HierarchyLevel, HierarchyMetadata

_DETECTOR = "agentic_devtools.cli.speckit.nest.discovery.GitHubHierarchyDetector"


def _git(repo: Path, *args: str) -> None:
    """Run a git command inside ``repo``, raising on failure."""
    subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True, text=True)


def _git_output(repo: Path, *args: str) -> str:
    """Run a git command inside ``repo`` and return its stripped stdout."""
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


@pytest.fixture
def repo(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Create a git repository containing three flat spec directories.

    The GitHub hierarchy is: epic ``#10`` → feature ``#20`` → task ``#30``.
    The working directory is switched to the repository root because the nest
    execution layer issues its git commands against the current directory,
    exactly as the CLI does when invoked from a repository root.
    """
    repo_path = tmp_path / "repo"
    specs = repo_path / "specs"
    specs.mkdir(parents=True)

    (specs / "10-epic").mkdir()
    (specs / "10-epic" / "spec.md").write_text(
        "# Epic\n\nSee [feature](../20-feature/spec.md) for details.\n",
        encoding="utf-8",
    )
    (specs / "20-feature").mkdir()
    (specs / "20-feature" / "spec.md").write_text("# Feature\n", encoding="utf-8")
    (specs / "30-task").mkdir()
    (specs / "30-task" / "spec.md").write_text("# Task\n", encoding="utf-8")

    _git(repo_path, "init", "--initial-branch", "main")
    _git(repo_path, "config", "user.email", "nest@example.com")
    _git(repo_path, "config", "user.name", "Nest Test")
    _git(repo_path, "add", "--all")
    _git(repo_path, "commit", "-m", "chore: seed flat specs")
    monkeypatch.chdir(repo_path)
    return repo_path


class _FakeDetector:
    """Stub detector returning a fixed epic → feature → task hierarchy."""

    _METADATA = {
        10: HierarchyMetadata(
            level=HierarchyLevel.EPIC,
            parent=None,
            children=[ChildInfo(number=20, title="Feature spec", order=0)],
            informational_children=[],
        ),
        20: HierarchyMetadata(
            level=HierarchyLevel.FEATURE,
            parent=10,
            children=[ChildInfo(number=30, title="Task spec", order=0)],
            informational_children=[],
        ),
        30: HierarchyMetadata(level=HierarchyLevel.TASK, parent=20, children=[], informational_children=[]),
    }

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Accept and ignore the detector's constructor arguments."""

    def validate_repository_access(self) -> None:
        """No-op: the fake detector always has access."""

    def build_metadata(self, issue_number: int) -> HierarchyMetadata:
        """Return the canned metadata for ``issue_number``."""
        return self._METADATA[issue_number]


class TestNestMigrationWorkflow:
    """Full flat-to-nested migration against a real git repository."""

    def _run(self, repo: Path) -> None:
        """Run the complete nest pipeline against ``repo``."""
        specs_root = repo / "specs"
        flat_specs = scan_flat_specs(specs_root)
        existing_targets = scan_existing_targets(specs_root)

        with patch(_DETECTOR, _FakeDetector):
            discovery = build_relationship_graph("owner", "repo", flat_specs)

        plan = compute_migration_plan(
            discovery.graph,
            flat_specs,
            specs_root,
            existing_targets=existing_targets,
        )
        crossref_updates = scan_crossrefs(plan.moves, specs_root)
        execute_migration(plan, specs_root, crossref_updates)

    def test_moves_specs_into_nested_hierarchy(self, repo: Path) -> None:
        """Flat directories are relocated into the epic/feature/task tree."""
        self._run(repo)

        specs = repo / "specs"
        assert (specs / "10" / "spec.md").exists()
        assert (specs / "10" / "20" / "spec.md").exists()
        assert (specs / "10" / "20" / "30" / "spec.md").exists()
        assert not (specs / "10-epic").exists()
        assert not (specs / "20-feature").exists()
        assert not (specs / "30-task").exists()

    def test_writes_hierarchy_files_with_github_titles(self, repo: Path) -> None:
        """hierarchy.yml records children using the exact GitHub titles."""
        self._run(repo)

        parsed = yaml.safe_load((repo / "specs" / "10" / "hierarchy.yml").read_text(encoding="utf-8"))

        assert parsed["children"][0]["key"] == "20"
        assert parsed["children"][0]["title"] == "Feature spec"

    def test_rewrites_cross_references_to_new_paths(self, repo: Path) -> None:
        """Markdown links pointing at moved specs are rewritten in place."""
        self._run(repo)

        content = (repo / "specs" / "10" / "spec.md").read_text(encoding="utf-8")

        assert "20-feature" not in content
        assert "20/spec.md" in content

    def test_updates_the_specs_readme_index(self, repo: Path) -> None:
        """A marker-delimited hierarchy index is written to specs/README.md."""
        self._run(repo)

        content = (repo / "specs" / "README.md").read_text(encoding="utf-8")

        assert INDEX_START_MARKER in content
        assert "`10/20/30`" in content

    def test_creates_exactly_one_commit(self, repo: Path) -> None:
        """The whole migration lands as a single conventional commit."""
        before = _git_output(repo, "rev-list", "--count", "HEAD")

        self._run(repo)

        after = _git_output(repo, "rev-list", "--count", "HEAD")
        assert int(after) - int(before) == 1
        assert _git_output(repo, "log", "-1", "--pretty=%s").startswith("refactor(#10):")

    def test_leaves_a_clean_working_tree(self, repo: Path) -> None:
        """Nothing is left staged or untracked after a successful migration."""
        self._run(repo)

        assert _git_output(repo, "status", "--porcelain") == ""

    def test_rolls_back_when_the_commit_fails(self, repo: Path) -> None:
        """A failure after writes begin restores the original flat layout."""
        head_before = _git_output(repo, "rev-parse", "HEAD")

        with (
            patch(
                "agentic_devtools.cli.speckit.nest.execution.create_commit",
                side_effect=RuntimeError("commit boom"),
            ),
            pytest.raises(RuntimeError),
        ):
            self._run(repo)

        assert _git_output(repo, "rev-parse", "HEAD") == head_before
        assert (repo / "specs" / "10-epic" / "spec.md").exists()
        assert not (repo / "specs" / "10" / "spec.md").exists()
        assert _git_output(repo, "status", "--porcelain") == ""
