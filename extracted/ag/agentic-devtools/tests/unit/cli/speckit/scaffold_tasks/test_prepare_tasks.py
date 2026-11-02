"""Tests for ``prepare_tasks``."""

from pathlib import Path
from unittest.mock import patch

import pytest

from agentic_devtools.cli.speckit.scaffold_common import ActiveFeature, FeatureResolutionError
from agentic_devtools.cli.speckit.scaffold_tasks import prepare_tasks


class TestPrepareTasks:
    """prepare_tasks seeds tasks.md from the repo template or an empty file."""

    def test_creates_tasks_md_from_template(self, tmp_path: Path) -> None:
        template = tmp_path / "template.md"
        template.write_text("# Template Content", encoding="utf-8")
        active = ActiveFeature(
            repo_root=tmp_path, feature_dir=tmp_path / "specs" / "042-x", branch="042-x", has_git=True
        )
        with patch("agentic_devtools.cli.speckit.scaffold_tasks.resolve_tasks_template", return_value=template):
            tasks_path = prepare_tasks(active)
        assert tasks_path.read_text(encoding="utf-8") == "# Template Content"

    def test_rejects_non_file_tasks_md(self, tmp_path: Path) -> None:
        active = ActiveFeature(
            repo_root=tmp_path, feature_dir=tmp_path / "specs" / "042-x", branch="042-x", has_git=True
        )
        active.feature_dir.mkdir(parents=True)
        (active.feature_dir / "tasks.md").mkdir()
        with pytest.raises(FeatureResolutionError, match="Refusing to seed non-file tasks.md"):
            prepare_tasks(active)

    def test_rejects_symlinked_tasks_md(self, tmp_path: Path) -> None:
        active = ActiveFeature(
            repo_root=tmp_path, feature_dir=tmp_path / "specs" / "042-x", branch="042-x", has_git=True
        )
        active.feature_dir.mkdir(parents=True)
        real_tasks = tmp_path / "outside-tasks.md"
        real_tasks.write_text("outside", encoding="utf-8")
        (active.feature_dir / "tasks.md").symlink_to(real_tasks)
        with pytest.raises(FeatureResolutionError, match="Refusing to seed symlinked tasks.md"):
            prepare_tasks(active)

    def test_prepare_tasks_when_template_is_missing_creates_empty_file(self, tmp_path: Path) -> None:
        active = ActiveFeature(
            repo_root=tmp_path, feature_dir=tmp_path / "specs" / "042-x", branch="042-x", has_git=True
        )
        with patch("agentic_devtools.cli.speckit.scaffold_tasks.resolve_tasks_template", return_value=None):
            prepared = prepare_tasks(active)
        assert prepared.read_text(encoding="utf-8") == ""

    def test_rejects_outside_repo_root(self, tmp_path: Path) -> None:
        repo_root = tmp_path / "repo"
        repo_root.mkdir()
        (repo_root / "specs").mkdir()
        outside_feature_dir = tmp_path / "outside-specs" / "042-x"
        outside_feature_dir.mkdir(parents=True)
        active = ActiveFeature(repo_root=repo_root, feature_dir=outside_feature_dir, branch="042-x", has_git=True)
        with pytest.raises(FeatureResolutionError, match="outside the repository root"):
            prepare_tasks(active)

    def test_rejects_feature_dir_outside_specs_root(self, tmp_path: Path) -> None:
        repo_root = tmp_path / "repo"
        repo_root.mkdir()
        (repo_root / "specs").mkdir()
        outside_specs_feature = repo_root / "docs" / "42-x"
        outside_specs_feature.mkdir(parents=True)
        active = ActiveFeature(repo_root=repo_root, feature_dir=outside_specs_feature, branch="42-x", has_git=True)
        with pytest.raises(FeatureResolutionError, match="outside repository specs directory"):
            prepare_tasks(active)

    def test_rejects_specs_root_as_feature_dir(self, tmp_path: Path) -> None:
        (tmp_path / "specs").mkdir()
        active = ActiveFeature(repo_root=tmp_path, feature_dir=tmp_path / "specs", branch="specs", has_git=True)
        with pytest.raises(FeatureResolutionError, match="strict descendant of the repository specs directory"):
            prepare_tasks(active)

    def test_rejects_symlinked_specs_root(self, tmp_path: Path) -> None:
        repo_root = tmp_path / "repo"
        repo_root.mkdir()
        external_specs = tmp_path / "external-specs"
        (external_specs / "42-x").mkdir(parents=True)
        (repo_root / "specs").symlink_to(external_specs)
        active = ActiveFeature(
            repo_root=repo_root, feature_dir=repo_root / "specs" / "42-x", branch="42-x", has_git=True
        )
        with pytest.raises(
            FeatureResolutionError, match="Repository specs directory resolves outside the repository root"
        ):
            prepare_tasks(active)

    def test_dry_run_skips_directory_creation(self, tmp_path: Path) -> None:
        active = ActiveFeature(
            repo_root=tmp_path, feature_dir=tmp_path / "specs" / "042-x", branch="042-x", has_git=True
        )
        prepared = prepare_tasks(active, dry_run=True)
        assert prepared == active.feature_dir / "tasks.md"
        assert not active.feature_dir.exists()

    @pytest.mark.parametrize("dry_run", [False, True])
    def test_rejects_symlinked_or_non_directory_feature_path(self, tmp_path: Path, dry_run: bool) -> None:
        feature_file = tmp_path / "specs" / "042-x"
        feature_file.parent.mkdir(parents=True)
        feature_file.write_text("not a directory", encoding="utf-8")
        active = ActiveFeature(repo_root=tmp_path, feature_dir=feature_file, branch="042-x", has_git=True)
        with pytest.raises(FeatureResolutionError, match="symlinked or non-directory feature path"):
            prepare_tasks(active, dry_run=dry_run)

    def test_does_not_overwrite_existing_tasks_md(self, tmp_path: Path) -> None:
        active = ActiveFeature(
            repo_root=tmp_path, feature_dir=tmp_path / "specs" / "042-x", branch="042-x", has_git=True
        )
        active.feature_dir.mkdir(parents=True)
        tasks_path = active.feature_dir / "tasks.md"
        tasks_path.write_text("existing content", encoding="utf-8")
        prepared = prepare_tasks(active)
        assert prepared == tasks_path
        assert tasks_path.read_text(encoding="utf-8") == "existing content"
