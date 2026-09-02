"""Tests for ``prepare_plan``."""

from pathlib import Path
from unittest.mock import patch

import pytest

from agentic_devtools.cli.speckit.scaffold_common import ActiveFeature, FeatureResolutionError
from agentic_devtools.cli.speckit.scaffold_plan import prepare_plan


class TestPreparePlan:
    """prepare_plan creates the feature directory and seeds plan.md."""

    def test_creates_feature_directory(self, tmp_path: Path) -> None:
        active = ActiveFeature(
            repo_root=tmp_path,
            feature_dir=tmp_path / "specs" / "042-x",
            branch="042-x",
            has_git=True,
        )

        with patch("agentic_devtools.cli.speckit.scaffold_plan.resolve_plan_template", return_value=None):
            prepare_plan(active)

        assert active.feature_dir.is_dir()

    def test_seeds_plan_md_from_template(self, tmp_path: Path) -> None:
        template = tmp_path / "template.md"
        template.write_text("# Template Content", encoding="utf-8")
        active = ActiveFeature(
            repo_root=tmp_path,
            feature_dir=tmp_path / "specs" / "042-x",
            branch="042-x",
            has_git=True,
        )

        with patch("agentic_devtools.cli.speckit.scaffold_plan.resolve_plan_template", return_value=template):
            impl_plan = prepare_plan(active)

        assert impl_plan == active.feature_dir / "plan.md"
        assert impl_plan.read_text(encoding="utf-8") == "# Template Content"

    def test_creates_empty_plan_md_when_no_template(self, tmp_path: Path) -> None:
        active = ActiveFeature(
            repo_root=tmp_path,
            feature_dir=tmp_path / "specs" / "042-x",
            branch="042-x",
            has_git=True,
        )

        with patch("agentic_devtools.cli.speckit.scaffold_plan.resolve_plan_template", return_value=None):
            impl_plan = prepare_plan(active)

        assert impl_plan.exists()
        assert impl_plan.read_text(encoding="utf-8") == ""

    def test_does_not_overwrite_existing_plan_md(self, tmp_path: Path) -> None:
        active = ActiveFeature(
            repo_root=tmp_path,
            feature_dir=tmp_path / "specs" / "042-x",
            branch="042-x",
            has_git=True,
        )
        active.feature_dir.mkdir(parents=True)
        (active.feature_dir / "plan.md").write_text("existing content", encoding="utf-8")

        impl_plan = prepare_plan(active)

        assert impl_plan.read_text(encoding="utf-8") == "existing content"

    def test_rejects_feature_dir_resolving_outside_repo_root(self, tmp_path: Path) -> None:
        repo_root = tmp_path / "repo"
        repo_root.mkdir()
        outside_specs = tmp_path / "outside-specs"
        outside_specs.mkdir()
        (repo_root / "specs").symlink_to(outside_specs)
        active = ActiveFeature(
            repo_root=repo_root,
            feature_dir=repo_root / "specs" / "042-x",
            branch="042-x",
            has_git=True,
        )

        with pytest.raises(FeatureResolutionError, match="outside the repository root"):
            prepare_plan(active)

    def test_rejects_non_file_plan_md(self, tmp_path: Path) -> None:
        active = ActiveFeature(
            repo_root=tmp_path,
            feature_dir=tmp_path / "specs" / "042-x",
            branch="042-x",
            has_git=True,
        )
        active.feature_dir.mkdir(parents=True)
        (active.feature_dir / "plan.md").mkdir()

        with pytest.raises(FeatureResolutionError, match="Refusing to seed non-file plan.md"):
            prepare_plan(active)

    def test_rejects_symlinked_plan_md(self, tmp_path: Path) -> None:
        active = ActiveFeature(
            repo_root=tmp_path,
            feature_dir=tmp_path / "specs" / "042-x",
            branch="042-x",
            has_git=True,
        )
        active.feature_dir.mkdir(parents=True)
        target = tmp_path / "outside-plan.md"
        (active.feature_dir / "plan.md").symlink_to(target)

        with pytest.raises(FeatureResolutionError, match="Refusing to seed symlinked plan.md"):
            prepare_plan(active)

    def test_dry_run_skips_directory_creation(self, tmp_path: Path) -> None:
        active = ActiveFeature(
            repo_root=tmp_path,
            feature_dir=tmp_path / "specs" / "042-x",
            branch="042-x",
            has_git=True,
        )

        with patch("agentic_devtools.cli.speckit.scaffold_plan.resolve_plan_template", return_value=None):
            result = prepare_plan(active, dry_run=True)

        assert not active.feature_dir.exists()
        assert result == active.feature_dir / "plan.md"

    def test_dry_run_skips_plan_md_creation(self, tmp_path: Path) -> None:
        active = ActiveFeature(
            repo_root=tmp_path,
            feature_dir=tmp_path / "specs" / "042-x",
            branch="042-x",
            has_git=True,
        )
        active.feature_dir.mkdir(parents=True)

        template = tmp_path / "template.md"
        template.write_text("# Template Content", encoding="utf-8")
        with patch("agentic_devtools.cli.speckit.scaffold_plan.resolve_plan_template", return_value=template):
            result = prepare_plan(active, dry_run=True)

        assert not (active.feature_dir / "plan.md").exists()
        assert result == active.feature_dir / "plan.md"

    def test_dry_run_still_rejects_symlinked_plan_md(self, tmp_path: Path) -> None:
        active = ActiveFeature(
            repo_root=tmp_path,
            feature_dir=tmp_path / "specs" / "042-x",
            branch="042-x",
            has_git=True,
        )
        active.feature_dir.mkdir(parents=True)
        target = tmp_path / "outside-plan.md"
        (active.feature_dir / "plan.md").symlink_to(target)

        with pytest.raises(FeatureResolutionError, match="Refusing to seed symlinked plan.md"):
            prepare_plan(active, dry_run=True)

    def test_dry_run_still_rejects_outside_repo_root(self, tmp_path: Path) -> None:
        repo_root = tmp_path / "repo"
        repo_root.mkdir()
        outside_specs = tmp_path / "outside-specs"
        outside_specs.mkdir()
        (repo_root / "specs").symlink_to(outside_specs)
        active = ActiveFeature(
            repo_root=repo_root,
            feature_dir=repo_root / "specs" / "042-x",
            branch="042-x",
            has_git=True,
        )

        with pytest.raises(FeatureResolutionError, match="outside the repository root"):
            prepare_plan(active, dry_run=True)
