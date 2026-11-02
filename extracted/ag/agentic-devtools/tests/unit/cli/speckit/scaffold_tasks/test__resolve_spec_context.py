"""Tests for ``_resolve_spec_context``."""

from pathlib import Path

import pytest

from agentic_devtools.cli.speckit.scaffold_common import ActiveFeature, FeatureResolutionError
from agentic_devtools.cli.speckit.scaffold_tasks import _resolve_spec_context


def test_resolve_spec_context_returns_none_for_feature_level(tmp_path: Path) -> None:
    active = ActiveFeature(repo_root=tmp_path, feature_dir=tmp_path / "specs" / "42", branch="42", has_git=True)
    assert _resolve_spec_context(active, "feature", None) is None


def test_resolve_spec_context_rejects_flat_feature_without_spec_context(tmp_path: Path) -> None:
    # feature directly under specs/ has no parent spec dir; should get a clear diagnostic
    active = ActiveFeature(repo_root=tmp_path, feature_dir=tmp_path / "specs" / "42", branch="42", has_git=True)
    with pytest.raises(FeatureResolutionError, match="requires a nested feature spec"):
        _resolve_spec_context(active, "task", None)


def test_resolve_spec_context_rejects_inferred_parent_outside_specs(tmp_path: Path) -> None:
    external = tmp_path / "external"
    external.mkdir()
    external_parent = external / "10-parent"
    external_parent.mkdir()
    repo = tmp_path / "repo"
    (repo / "specs").mkdir(parents=True)
    # resolved parent_dir escapes specs_root (exercised here via a symlinked subdirectory,
    # but the guard catches any out-of-tree resolved path, not only symlink escapes)
    parent_link = repo / "specs" / "10-parent"
    parent_link.symlink_to(external_parent)
    active = ActiveFeature(repo_root=repo, feature_dir=parent_link / "42-task", branch="42-task", has_git=True)
    with pytest.raises(
        FeatureResolutionError, match="Inferred spec-context resolves outside repository specs directory"
    ):
        _resolve_spec_context(active, "task", None)


def test_resolve_spec_context_rejects_missing_task_parent_spec(tmp_path: Path) -> None:
    parent_dir = tmp_path / "specs" / "10-parent"
    parent_dir.mkdir(parents=True)
    # no spec.md in parent_dir — should fail with missing-spec message
    active = ActiveFeature(repo_root=tmp_path, feature_dir=parent_dir / "42-task", branch="42-task", has_git=True)
    with pytest.raises(FeatureResolutionError, match="requires a regular, non-symlinked parent spec.md"):
        _resolve_spec_context(active, "task", None)


def test_resolve_spec_context_rejects_missing_task_parent_plan(tmp_path: Path) -> None:
    parent_dir = tmp_path / "specs" / "10-parent"
    parent_dir.mkdir(parents=True)
    (parent_dir / "spec.md").write_text("# Parent\n", encoding="utf-8")
    # no plan.md — should fail
    active = ActiveFeature(repo_root=tmp_path, feature_dir=parent_dir / "42-task", branch="42-task", has_git=True)
    with pytest.raises(FeatureResolutionError, match="requires a regular, non-symlinked parent plan.md"):
        _resolve_spec_context(active, "task", None)


def test_resolve_spec_context_accepts_directory_arg(tmp_path: Path) -> None:
    parent_dir = tmp_path / "specs" / "10-parent"
    parent_dir.mkdir(parents=True)
    (parent_dir / "spec.md").write_text("# Parent\n", encoding="utf-8")
    (parent_dir / "plan.md").write_text("# Plan\n", encoding="utf-8")
    active = ActiveFeature(repo_root=tmp_path, feature_dir=tmp_path / "specs" / "42", branch="42", has_git=True)
    result = _resolve_spec_context(active, "task", str(parent_dir))
    assert result is not None
    spec_path, plan_path = result
    assert spec_path == (parent_dir / "spec.md").resolve()
    assert plan_path == (parent_dir / "plan.md").resolve()


def test_resolve_spec_context_rejects_context_outside_specs(tmp_path: Path) -> None:
    outside_dir = tmp_path / "outside"
    outside_dir.mkdir()
    (outside_dir / "spec.md").write_text("# Outside\n", encoding="utf-8")
    active = ActiveFeature(repo_root=tmp_path, feature_dir=tmp_path / "specs" / "42", branch="42", has_git=True)
    with pytest.raises(FeatureResolutionError, match="outside repository specs directory"):
        _resolve_spec_context(active, "task", str(outside_dir))


def test_resolve_spec_context_rejects_symlinked_specs_root(tmp_path: Path) -> None:
    external = tmp_path / "external"
    external.mkdir()
    parent_dir = external / "10-parent"
    parent_dir.mkdir()
    (parent_dir / "spec.md").write_text("# Parent\n", encoding="utf-8")
    (parent_dir / "plan.md").write_text("# Plan\n", encoding="utf-8")
    repo = tmp_path / "repo"
    repo.mkdir()
    specs_link = repo / "specs"
    specs_link.symlink_to(external)
    context_dir = specs_link / "10-parent"
    active = ActiveFeature(repo_root=repo, feature_dir=repo / "specs" / "42", branch="42", has_git=True)
    with pytest.raises(FeatureResolutionError, match="resolves outside the repository root"):
        _resolve_spec_context(active, "task", str(context_dir))


def test_resolve_spec_context_rejects_specs_root_context(tmp_path: Path) -> None:
    specs_root = tmp_path / "specs"
    specs_root.mkdir()
    (specs_root / "spec.md").write_text("# Root Spec\n", encoding="utf-8")
    (specs_root / "plan.md").write_text("# Root Plan\n", encoding="utf-8")
    active = ActiveFeature(repo_root=tmp_path, feature_dir=tmp_path / "specs" / "42", branch="42", has_git=True)
    with pytest.raises(FeatureResolutionError, match="must point to a directory below repository specs directory"):
        _resolve_spec_context(active, "task", str(specs_root))
