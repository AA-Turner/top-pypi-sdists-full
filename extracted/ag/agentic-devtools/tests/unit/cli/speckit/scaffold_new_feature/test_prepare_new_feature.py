"""Tests for ``prepare_new_feature``."""

import json
import os
from collections.abc import Generator
from pathlib import Path
from unittest.mock import patch

import pytest
import yaml

from agentic_devtools.cli.speckit.scaffold_new_feature import (
    PRESET_TEMPLATE_RELATIVE_PATH,
    _acquire_hierarchy_lock,
    prepare_new_feature,
)


@pytest.fixture(autouse=True)
def _restore_env() -> Generator[None]:
    """Snapshot and restore os.environ to prevent env leaks between tests."""
    snapshot = os.environ.copy()
    try:
        yield
    finally:
        os.environ.clear()
        os.environ.update(snapshot)


class TestPrepareNewFeature:
    """prepare_new_feature creates a feature directory and spec metadata."""

    def test_creates_flat_feature_directory_with_explicit_issue_number(self, tmp_path: Path) -> None:
        with patch("agentic_devtools.cli.speckit.scaffold_new_feature._create_or_checkout_branch"):
            result = prepare_new_feature(
                repo_root=tmp_path,
                feature_description="Add login flow",
                feature_number=42,
                flat=True,
                dry_run=True,
            )

        # "Add" and "to" are stop words; "login" and "flow" are kept
        expected_dir = tmp_path / "specs" / "42-login-flow"
        assert result.feature_dir == expected_dir
        assert result.branch_name == "42-login-flow"

    def test_creates_nested_feature_under_parent_dir(self, tmp_path: Path) -> None:
        parent_dir = tmp_path / "specs" / "1-parent-feature"
        parent_dir.mkdir(parents=True)

        with (
            patch("agentic_devtools.cli.speckit.scaffold_new_feature._create_or_checkout_branch"),
            patch("agentic_devtools.cli.speckit.scaffold_new_feature.detect_parent_hierarchy", return_value=None),
        ):
            result = prepare_new_feature(
                repo_root=tmp_path,
                feature_description="Add nested child",
                feature_number=2,
                parent_feature_number=1,
                dry_run=True,
            )

        assert result.parent_dir == parent_dir
        assert result.feature_dir == parent_dir / "2"

    def test_explicit_parent_writes_resolved_parent_key_in_child_hierarchy(self, tmp_path: Path) -> None:
        parent_dir = tmp_path / "specs" / "001-parent-feature"
        parent_dir.mkdir(parents=True)

        with (
            patch("agentic_devtools.cli.speckit.scaffold_new_feature._create_or_checkout_branch"),
            patch("agentic_devtools.cli.speckit.scaffold_new_feature.detect_parent_hierarchy", return_value=None),
        ):
            result = prepare_new_feature(
                repo_root=tmp_path,
                feature_description="Add nested child",
                feature_number=2,
                parent_feature_number=1,
                dry_run=False,
            )

        hierarchy_data = yaml.safe_load((result.feature_dir / "hierarchy.yml").read_text(encoding="utf-8"))
        assert hierarchy_data["parent"] != "001"
        assert hierarchy_data["parent"] == "1"

    def test_rejects_blank_description(self, tmp_path: Path) -> None:
        with pytest.raises(ValueError, match="required"):
            prepare_new_feature(repo_root=tmp_path, feature_description="   ")

    def test_rejects_non_positive_feature_number(self, tmp_path: Path) -> None:
        with pytest.raises(ValueError, match="feature_number"):
            prepare_new_feature(repo_root=tmp_path, feature_description="Feature", feature_number=0)

    def test_rejects_non_positive_parent_feature_number(self, tmp_path: Path) -> None:
        with pytest.raises(ValueError, match="parent_feature_number"):
            prepare_new_feature(repo_root=tmp_path, feature_description="Feature", parent_feature_number=0)

    def test_prepare_new_feature_uses_short_name_and_no_parent_info(self, tmp_path: Path) -> None:
        with (
            patch("agentic_devtools.cli.speckit.scaffold_new_feature._create_or_checkout_branch"),
            patch(
                "agentic_devtools.cli.speckit.scaffold_new_feature.detect_parent_hierarchy",
                return_value={"status": "ok"},
            ),
        ):
            result = prepare_new_feature(
                repo_root=tmp_path,
                feature_description="Add feature",
                feature_number=9,
                short_name="small-name",
                dry_run=True,
            )

        assert result.branch_name == "9-small-name"
        assert result.parent_dir is None
        assert result.hierarchy_level is None

    def test_prepare_new_feature_uses_verified_phase_one_hierarchy(self, tmp_path: Path) -> None:
        with (
            patch("agentic_devtools.cli.speckit.scaffold_new_feature._create_or_checkout_branch"),
            patch(
                "agentic_devtools.cli.speckit.scaffold_new_feature.detect_parent_hierarchy",
                return_value={"parent": None, "level": "task"},
            ),
        ):
            result = prepare_new_feature(
                repo_root=tmp_path,
                feature_description="Parentless Task",
                feature_number=99006,
                verified_hierarchy_level="feature",
            )

        assert result.hierarchy_level == "feature"
        metadata = json.loads((result.feature_dir / "feature.json").read_text(encoding="utf-8"))
        assert metadata["HIERARCHY_LEVEL"] == "feature"

    def test_verified_no_parent_skips_detector_parent_selection(self, tmp_path: Path) -> None:
        unrelated_parent = tmp_path / "specs" / "17-unrelated-parent"
        unrelated_parent.mkdir(parents=True)
        existing_hierarchy = unrelated_parent / "hierarchy.yml"
        existing_hierarchy.write_text(
            "title: Unrelated\nlevel: feature\nparent: null\nchildren: []\n",
            encoding="utf-8",
        )

        with (
            patch("agentic_devtools.cli.speckit.scaffold_new_feature._create_or_checkout_branch"),
            patch(
                "agentic_devtools.cli.speckit.scaffold_new_feature.detect_parent_hierarchy",
                side_effect=AssertionError("verified parentless issue must not run parent detection"),
            ),
        ):
            result = prepare_new_feature(
                repo_root=tmp_path,
                feature_description="Parentless Task",
                feature_number=99006,
                verified_hierarchy_level="feature",
                verified_parent_number="",
            )

        assert result.hierarchy_level == "feature"
        assert result.parent_dir is None
        assert result.feature_dir == tmp_path / "specs" / "99006-parentless-task"
        assert existing_hierarchy.read_text(encoding="utf-8") == (
            "title: Unrelated\nlevel: feature\nparent: null\nchildren: []\n"
        )

    def test_reuses_resolved_directory_for_downgraded_task(self, tmp_path: Path) -> None:
        existing_dir = tmp_path / "specs" / "10-parent" / "42"
        existing_dir.mkdir(parents=True)
        (existing_dir / "tasks.md").write_text("# Existing tasks\n", encoding="utf-8")
        (existing_dir / "hierarchy.yml").write_text(
            "title: Old task\nlevel: task\nparent: 10\nchildren: []\n",
            encoding="utf-8",
        )

        with patch("agentic_devtools.cli.speckit.scaffold_new_feature._create_or_checkout_branch"):
            result = prepare_new_feature(
                repo_root=tmp_path,
                feature_description="Standalone feature",
                feature_number=42,
                verified_hierarchy_level="feature",
                verified_parent_number="",
                reuse_spec_dir="specs/10-parent/42",
            )

        assert result.feature_dir == existing_dir
        assert (existing_dir / "tasks.md").read_text(encoding="utf-8") == "# Existing tasks\n"
        assert (existing_dir / "spec.md").is_file()
        assert not (tmp_path / "specs" / "42-standalone-feature").exists()
        metadata = yaml.safe_load((existing_dir / "hierarchy.yml").read_text(encoding="utf-8"))
        assert metadata["level"] == "feature"
        assert "parent" not in metadata

    def test_reuse_creates_feature_metadata_when_hierarchy_file_is_absent(self, tmp_path: Path) -> None:
        existing_dir = tmp_path / "specs" / "10-parent" / "42"
        existing_dir.mkdir(parents=True)
        (existing_dir / "tasks.md").write_text("# Existing tasks\n", encoding="utf-8")

        with patch("agentic_devtools.cli.speckit.scaffold_new_feature._create_or_checkout_branch"):
            result = prepare_new_feature(
                repo_root=tmp_path,
                feature_description="Standalone feature",
                feature_number=42,
                verified_hierarchy_level="feature",
                verified_parent_number="",
                reuse_spec_dir="specs/10-parent/42",
            )

        metadata = yaml.safe_load((existing_dir / "hierarchy.yml").read_text(encoding="utf-8"))
        assert result.feature_dir == existing_dir
        assert metadata["level"] == "feature"
        assert "parent" not in metadata

    def test_reuse_dry_run_does_not_create_or_update_scaffold_files(self, tmp_path: Path) -> None:
        existing_dir = tmp_path / "specs" / "10-parent" / "42"
        existing_dir.mkdir(parents=True)
        (existing_dir / "tasks.md").write_text("# Existing tasks\n", encoding="utf-8")

        with patch("agentic_devtools.cli.speckit.scaffold_new_feature._create_or_checkout_branch"):
            result = prepare_new_feature(
                repo_root=tmp_path,
                feature_description="Standalone feature",
                feature_number=42,
                verified_hierarchy_level="feature",
                verified_parent_number="",
                reuse_spec_dir="specs/10-parent/42",
                dry_run=True,
            )

        assert result.feature_dir == existing_dir
        assert not (existing_dir / "spec.md").exists()
        assert not (existing_dir / "hierarchy.yml").exists()

    @pytest.mark.parametrize(
        ("reuse_spec_dir", "verified_hierarchy_level", "verified_parent_number", "message"),
        [
            ("specs/10-parent/42", "task", "", "verified parentless Feature"),
            ("specs/10-parent/42", "feature", None, "verified parentless Feature"),
            ("specs/../42", "feature", "", "safe repository-relative path"),
            ("other/42", "feature", "", "safe repository-relative path"),
            ("specs//42", "feature", "", "safe repository-relative path"),
            ("specs", "feature", "", "safe repository-relative path"),
            (r"specs\10-parent\42", "feature", "", "safe repository-relative path"),
            ("specs/10-parent/43", "feature", "", "must identify issue #42"),
        ],
    )
    def test_rejects_invalid_reuse_spec_directory(
        self,
        tmp_path: Path,
        reuse_spec_dir: str,
        verified_hierarchy_level: str,
        verified_parent_number: str | None,
        message: str,
    ) -> None:
        with pytest.raises(ValueError, match=message):
            prepare_new_feature(
                repo_root=tmp_path,
                feature_description="Standalone feature",
                feature_number=42,
                verified_hierarchy_level=verified_hierarchy_level,
                verified_parent_number=verified_parent_number,
                reuse_spec_dir=reuse_spec_dir,
                dry_run=True,
            )

    @pytest.mark.parametrize("create_directory", [False, True])
    def test_rejects_reuse_path_without_existing_task_artifacts(self, tmp_path: Path, create_directory: bool) -> None:
        existing_dir = tmp_path / "specs" / "10-parent" / "42"
        if create_directory:
            existing_dir.mkdir(parents=True)

        with pytest.raises(ValueError, match="existing Task directory"):
            prepare_new_feature(
                repo_root=tmp_path,
                feature_description="Standalone feature",
                feature_number=42,
                verified_hierarchy_level="feature",
                verified_parent_number="",
                reuse_spec_dir="specs/10-parent/42",
                dry_run=True,
            )

    def test_rejects_reuse_directory_with_symlinked_path_component(self, tmp_path: Path) -> None:
        outside = tmp_path / "outside"
        outside.mkdir()
        specs_dir = tmp_path / "specs"
        specs_dir.mkdir()
        (specs_dir / "10-parent").symlink_to(outside, target_is_directory=True)

        with pytest.raises(ValueError, match="symlink"):
            prepare_new_feature(
                repo_root=tmp_path,
                feature_description="Standalone feature",
                feature_number=42,
                verified_hierarchy_level="feature",
                verified_parent_number="",
                reuse_spec_dir="specs/10-parent/42",
                dry_run=True,
            )

    def test_verified_parent_number_selects_parent_before_child_detection(self, tmp_path: Path) -> None:
        parent_dir = tmp_path / "specs" / "17-parent-feature"
        parent_dir.mkdir(parents=True)

        def _detect(number: int, repo_root: Path | None = None) -> dict[str, str]:
            assert number == 17
            return {"level": "feature", "title": "Parent Feature"}

        with (
            patch("agentic_devtools.cli.speckit.scaffold_new_feature._create_or_checkout_branch"),
            patch("agentic_devtools.cli.speckit.scaffold_new_feature.detect_parent_hierarchy", side_effect=_detect),
        ):
            result = prepare_new_feature(
                repo_root=tmp_path,
                feature_description="Nested Task",
                feature_number=99007,
                verified_hierarchy_level="task",
                verified_parent_number="17",
            )

        assert result.parent_dir == parent_dir
        assert result.feature_dir == parent_dir / "99007"

    def test_prepare_new_feature_rejects_unsupported_verified_hierarchy(self, tmp_path: Path) -> None:
        with pytest.raises(ValueError, match="must be epic, feature, or task"):
            prepare_new_feature(
                repo_root=tmp_path,
                feature_description="Invalid hierarchy",
                feature_number=99007,
                verified_hierarchy_level="unknown",
            )

    def test_prepare_new_feature_requires_verified_hierarchy_to_be_issue_scoped(self, tmp_path: Path) -> None:
        with pytest.raises(ValueError, match="requires an explicit issue"):
            prepare_new_feature(
                repo_root=tmp_path,
                feature_description="Missing issue",
                verified_hierarchy_level="feature",
            )

    def test_prepare_new_feature_rejects_invalid_verified_parent_number(self, tmp_path: Path) -> None:
        with pytest.raises(ValueError, match="verified_parent_number"):
            prepare_new_feature(
                repo_root=tmp_path,
                feature_description="Invalid parent",
                feature_number=99008,
                verified_hierarchy_level="feature",
                verified_parent_number="../17",
            )

    def test_prepare_new_feature_requires_verified_hierarchy_for_parent_decision(self, tmp_path: Path) -> None:
        with pytest.raises(ValueError, match="requires verified_hierarchy_level"):
            prepare_new_feature(
                repo_root=tmp_path,
                feature_description="Unverified hierarchy",
                feature_number=99009,
                verified_parent_number="",
            )

    def test_prepare_new_feature_warns_when_hierarchy_detection_fails(self, tmp_path: Path) -> None:
        with (
            patch("agentic_devtools.cli.speckit.scaffold_new_feature._create_or_checkout_branch"),
            patch("agentic_devtools.cli.speckit.scaffold_new_feature.detect_parent_hierarchy", return_value=None),
            pytest.warns(UserWarning, match="Hierarchy detection failed; falling back to flat directory creation"),
        ):
            result = prepare_new_feature(
                repo_root=tmp_path,
                feature_description="Add feature",
                feature_number=9,
                dry_run=True,
            )

        assert result.parent_dir is None

    def test_prepare_new_feature_handles_dry_run_nested_parent(self, tmp_path: Path) -> None:
        parent_dir = tmp_path / "specs" / "1-parent"
        parent_dir.mkdir(parents=True)

        with (
            patch("agentic_devtools.cli.speckit.scaffold_new_feature._create_or_checkout_branch"),
            patch(
                "agentic_devtools.cli.speckit.scaffold_new_feature.detect_parent_hierarchy",
                return_value={"parent": "1"},
            ),
        ):
            result = prepare_new_feature(
                repo_root=tmp_path,
                feature_description="Add nested dry run",
                feature_number=2,
                dry_run=True,
            )

        assert result.parent_dir == parent_dir
        assert result.feature_dir == parent_dir / "2"
        assert result.hierarchy_level is None
        assert not result.feature_dir.exists()

    def test_prepare_new_feature_uses_detected_parent(self, tmp_path: Path) -> None:
        parent_dir = tmp_path / "specs" / "1-parent"
        parent_dir.mkdir(parents=True)

        with (
            patch("agentic_devtools.cli.speckit.scaffold_new_feature._create_or_checkout_branch"),
            patch(
                "agentic_devtools.cli.speckit.scaffold_new_feature.detect_parent_hierarchy",
                return_value={"parent": "1"},
            ),
        ):
            result = prepare_new_feature(
                repo_root=tmp_path,
                feature_description="Add child",
                feature_number=2,
                dry_run=True,
            )

        assert result.parent_dir == parent_dir
        assert result.feature_dir == parent_dir / "2"
        assert result.hierarchy_level is None

    def test_prepare_new_feature_creates_missing_explicit_parent(self, tmp_path: Path) -> None:
        with (
            patch("agentic_devtools.cli.speckit.scaffold_new_feature._create_or_checkout_branch"),
            patch(
                "agentic_devtools.cli.speckit.scaffold_new_feature.detect_parent_hierarchy",
                return_value={"title": "Parent Title", "level": "epic"},
            ),
        ):
            result = prepare_new_feature(
                repo_root=tmp_path,
                feature_description="Add child",
                feature_number=2,
                parent_feature_number=1,
                dry_run=False,
            )

        assert result.parent_dir == (tmp_path / "specs" / "1-parent-title")
        assert (result.parent_dir / "spec.md").exists()
        assert (tmp_path / ".specify" / "feature.json").exists()

    def test_prepare_new_feature_explicit_parent_uses_child_own_detected_level(self, tmp_path: Path) -> None:
        # The explicit-parent path must resolve the child's own detected level by querying
        # the detector with the child's feature_number, not by deriving it from the parent's
        # level. Here the parent is an "epic" but the child issue is itself classified as a
        # "feature" (not "task"), which the legacy script preserves via a separate detector
        # call for the child issue.
        parent_dir = tmp_path / "specs" / "1-parent"
        parent_dir.mkdir(parents=True)

        def _detect(number: int, repo_root: Path | None = None) -> dict[str, str]:
            if number == 2:
                return {"level": "feature", "title": "Child Feature"}
            return {"level": "epic", "title": "Parent"}

        with (
            patch("agentic_devtools.cli.speckit.scaffold_new_feature._create_or_checkout_branch"),
            patch(
                "agentic_devtools.cli.speckit.scaffold_new_feature.detect_parent_hierarchy",
                side_effect=_detect,
            ),
        ):
            result = prepare_new_feature(
                repo_root=tmp_path,
                feature_description="Add child",
                feature_number=2,
                parent_feature_number=1,
                dry_run=True,
            )

        assert result.hierarchy_level == "feature"

    def test_prepare_new_feature_falls_back_to_flat_when_parent_exceeds_max_depth(self, tmp_path: Path) -> None:
        # Parent at depth 3 (specs/0-epic/5-feature/1-nested/) would push child to depth 4,
        # exceeding the three-level Epic→Feature→Task cap.
        deep_parent = tmp_path / "specs" / "0-epic" / "5-feature" / "1-nested"
        deep_parent.mkdir(parents=True)

        with (
            patch("agentic_devtools.cli.speckit.scaffold_new_feature._create_or_checkout_branch"),
            patch("agentic_devtools.cli.speckit.scaffold_new_feature.detect_parent_hierarchy", return_value=None),
            pytest.warns(UserWarning, match="Maximum nesting depth"),
        ):
            result = prepare_new_feature(
                repo_root=tmp_path,
                feature_description="Add deep task",
                feature_number=2,
                parent_feature_number=1,
                dry_run=True,
            )

        # Should fall back to flat allocation using branch_name
        assert result.parent_dir is None
        assert result.feature_dir == tmp_path / "specs" / "2-deep-task"

    def test_prepare_new_feature_preserves_detected_level_without_parent(self, tmp_path: Path) -> None:
        with (
            patch("agentic_devtools.cli.speckit.scaffold_new_feature._create_or_checkout_branch"),
            patch(
                "agentic_devtools.cli.speckit.scaffold_new_feature.detect_parent_hierarchy",
                return_value={"level": "feature", "title": "Standalone Feature"},
            ),
        ):
            result = prepare_new_feature(
                repo_root=tmp_path,
                feature_description="Standalone feature",
                feature_number=42,
                dry_run=False,
            )

        assert result.parent_dir is None
        assert result.hierarchy_level == "feature"
        feature_metadata = json.loads((result.feature_dir / "feature.json").read_text(encoding="utf-8"))
        assert feature_metadata["HIERARCHY_LEVEL"] == "feature"

    def test_prepare_new_feature_preserves_detected_level_when_explicit_parent_falls_back(self, tmp_path: Path) -> None:
        deep_parent = tmp_path / "specs" / "0-epic" / "5-feature" / "1-nested"
        deep_parent.mkdir(parents=True)

        def _detect(number: int, repo_root: Path | None = None) -> dict[str, str]:
            if number == 2:
                return {"level": "feature", "title": "Child Feature"}
            return {"level": "task", "title": "Parent Task"}

        with (
            patch("agentic_devtools.cli.speckit.scaffold_new_feature._create_or_checkout_branch"),
            patch("agentic_devtools.cli.speckit.scaffold_new_feature.detect_parent_hierarchy", side_effect=_detect),
            pytest.warns(UserWarning, match="Maximum nesting depth"),
        ):
            result = prepare_new_feature(
                repo_root=tmp_path,
                feature_description="Add deep task",
                feature_number=2,
                parent_feature_number=1,
                dry_run=False,
            )

        assert result.parent_dir is None
        assert result.hierarchy_level == "feature"
        feature_metadata = json.loads((result.feature_dir / "feature.json").read_text(encoding="utf-8"))
        assert feature_metadata["HIERARCHY_LEVEL"] == "feature"

    def test_prepare_new_feature_preserves_detected_level_when_auto_parent_exceeds_max_depth(
        self, tmp_path: Path
    ) -> None:
        deep_parent = tmp_path / "specs" / "0-epic" / "5-feature" / "1-nested"
        deep_parent.mkdir(parents=True)

        def _detect(number: int, repo_root: Path | None = None) -> dict[str, str]:
            if number == 2:
                return {"parent": "1", "level": "task", "title": "Child Task"}
            return {"level": "feature", "title": "Parent Feature"}

        with (
            patch("agentic_devtools.cli.speckit.scaffold_new_feature._create_or_checkout_branch"),
            patch("agentic_devtools.cli.speckit.scaffold_new_feature.detect_parent_hierarchy", side_effect=_detect),
            pytest.warns(UserWarning, match="Maximum nesting depth"),
        ):
            result = prepare_new_feature(
                repo_root=tmp_path,
                feature_description="Add auto detected task",
                feature_number=2,
                dry_run=False,
            )

        assert result.parent_dir is None
        assert result.hierarchy_level == "task"
        feature_metadata = json.loads((result.feature_dir / "feature.json").read_text(encoding="utf-8"))
        assert feature_metadata["HIERARCHY_LEVEL"] == "task"

    def test_prepare_new_feature_releases_hierarchy_lock_when_parent_update_fails(self, tmp_path: Path) -> None:
        parent_dir = tmp_path / "specs" / "1-parent"
        parent_dir.mkdir(parents=True)

        def _detect(number: int, repo_root: Path | None = None) -> dict[str, str]:
            if number == 2:
                return {"level": "task", "title": "Child Task"}
            return {"level": "epic", "title": "Parent Epic"}

        with (
            patch("agentic_devtools.cli.speckit.scaffold_new_feature._create_or_checkout_branch"),
            patch("agentic_devtools.cli.speckit.scaffold_new_feature.detect_parent_hierarchy", side_effect=_detect),
            patch(
                "agentic_devtools.cli.speckit.scaffold_new_feature.create_hierarchy_yml",
                side_effect=[None, RuntimeError("parent update failed")],
            ),
            pytest.raises(RuntimeError, match="parent update failed"),
        ):
            prepare_new_feature(
                repo_root=tmp_path,
                feature_description="Child task",
                feature_number=2,
                parent_feature_number=1,
                dry_run=False,
            )

        lock_fd = _acquire_hierarchy_lock(parent_dir / ".hierarchy.yml.lock", timeout_seconds=0)
        os.close(lock_fd)

    def test_prepare_new_feature_creates_missing_auto_detected_parent(self, tmp_path: Path) -> None:
        # No parent directory exists — the auto-detected parent should be stubbed out.
        with (
            patch("agentic_devtools.cli.speckit.scaffold_new_feature._create_or_checkout_branch"),
            patch(
                "agentic_devtools.cli.speckit.scaffold_new_feature.detect_parent_hierarchy",
                return_value={"parent": "1"},
            ),
        ):
            result = prepare_new_feature(
                repo_root=tmp_path,
                feature_description="Child feature",
                feature_number=2,
                dry_run=True,
            )

        # Parent dir should be resolved even though it was missing
        assert result.parent_dir is not None
        assert result.feature_dir == result.parent_dir / "2"
        parent_dir = tmp_path / "specs" / "1-parent"
        parent_dir.mkdir(parents=True)
        with (
            patch("agentic_devtools.cli.speckit.scaffold_new_feature._create_or_checkout_branch"),
            patch(
                "agentic_devtools.cli.speckit.scaffold_new_feature.detect_parent_hierarchy",
                return_value={"parent": "1"},
            ),
        ):
            result = prepare_new_feature(
                repo_root=tmp_path,
                feature_description="Nested Child",
                feature_number=2,
                dry_run=False,
            )
        assert (result.feature_dir / "hierarchy.yml").exists()
        assert (parent_dir / "hierarchy.yml").exists()

    def test_prepare_new_feature_flat_creates_files_not_dry_run(self, tmp_path: Path) -> None:
        with patch("agentic_devtools.cli.speckit.scaffold_new_feature._create_or_checkout_branch"):
            result = prepare_new_feature(
                repo_root=tmp_path,
                feature_description="Add login flow",
                feature_number=42,
                flat=True,
                dry_run=False,
            )
        assert result.feature_dir == tmp_path / "specs" / "42-login-flow"
        assert result.spec_file.read_text(encoding="utf-8") == ""
        metadata = json.loads((result.feature_dir / "feature.json").read_text(encoding="utf-8"))
        assert metadata["NUMBER_SOURCE"] == "explicit"

    def test_prepare_new_feature_creates_flat_fallback_when_no_parent_detected(self, tmp_path: Path) -> None:
        with (
            patch("agentic_devtools.cli.speckit.scaffold_new_feature._create_or_checkout_branch"),
            patch(
                "agentic_devtools.cli.speckit.scaffold_new_feature.detect_parent_hierarchy",
                return_value={"status": "ok"},
            ),
        ):
            result = prepare_new_feature(
                repo_root=tmp_path,
                feature_description="Add login flow",
                feature_number=42,
                dry_run=False,
            )
        assert result.feature_dir == tmp_path / "specs" / "42-login-flow"
        assert (result.feature_dir / "spec.md").exists()
        assert result.hierarchy_level is None

    def test_prepare_new_feature_flat_uses_template_when_present(self, tmp_path: Path) -> None:
        template_path = tmp_path / PRESET_TEMPLATE_RELATIVE_PATH
        template_path.parent.mkdir(parents=True)
        template_path.write_text("# Template\n", encoding="utf-8")
        with patch("agentic_devtools.cli.speckit.scaffold_new_feature._create_or_checkout_branch"):
            result = prepare_new_feature(
                repo_root=tmp_path,
                feature_description="Add template feature",
                feature_number=43,
                flat=True,
                dry_run=False,
            )
        assert result.spec_file.read_text(encoding="utf-8") == "# Template\n"

    def test_prepare_new_feature_flat_fallback_uses_template_when_present(self, tmp_path: Path) -> None:
        template_path = tmp_path / PRESET_TEMPLATE_RELATIVE_PATH
        template_path.parent.mkdir(parents=True)
        template_path.write_text("# Template\n", encoding="utf-8")
        with (
            patch("agentic_devtools.cli.speckit.scaffold_new_feature._create_or_checkout_branch"),
            patch(
                "agentic_devtools.cli.speckit.scaffold_new_feature.detect_parent_hierarchy",
                return_value={"status": "ok"},
            ),
        ):
            result = prepare_new_feature(
                repo_root=tmp_path,
                feature_description="Add template feature",
                feature_number=43,
                dry_run=False,
            )
        assert result.spec_file.read_text(encoding="utf-8") == "# Template\n"

    def test_prepare_new_feature_parent_stub_ignores_template_resolving_outside_repo(self, tmp_path: Path) -> None:
        template_path = tmp_path / PRESET_TEMPLATE_RELATIVE_PATH
        template_path.parent.mkdir(parents=True)
        template_path.write_text("# Should not copy\n", encoding="utf-8")
        real_resolve = Path.resolve

        def _fake_resolve(self: Path, *args, **kwargs) -> Path:
            if self == template_path:
                return tmp_path.parent / "outside-spec-template.md"
            return real_resolve(self, *args, **kwargs)

        def _detect(number: int, repo_root: Path | None = None) -> dict[str, str]:
            if number == 2:
                return {"level": "task", "title": "Child Task"}
            return {"level": "epic", "title": "Parent Epic"}

        with (
            patch("pathlib.Path.resolve", new=_fake_resolve),
            patch("agentic_devtools.cli.speckit.scaffold_new_feature._create_or_checkout_branch"),
            patch("agentic_devtools.cli.speckit.scaffold_new_feature.detect_parent_hierarchy", side_effect=_detect),
        ):
            result = prepare_new_feature(
                repo_root=tmp_path,
                feature_description="Child task",
                feature_number=2,
                parent_feature_number=1,
                dry_run=False,
            )

        parent_spec = tmp_path / "specs" / "1-parent-epic" / "spec.md"
        assert parent_spec.read_text(encoding="utf-8") == ""
        assert result.spec_file.read_text(encoding="utf-8") == ""

    def test_prepare_new_feature_auto_detected_parent_stub_ignores_template_resolving_outside_repo(
        self, tmp_path: Path
    ) -> None:
        template_path = tmp_path / PRESET_TEMPLATE_RELATIVE_PATH
        template_path.parent.mkdir(parents=True)
        template_path.write_text("# Should not copy\n", encoding="utf-8")
        real_resolve = Path.resolve

        def _fake_resolve(self: Path, *args, **kwargs) -> Path:
            if self == template_path:
                return tmp_path.parent / "outside-spec-template.md"
            return real_resolve(self, *args, **kwargs)

        def _detect(number: int, repo_root: Path | None = None) -> dict[str, str]:
            if number == 2:
                return {"parent": "1", "level": "task"}
            return {"level": "epic", "title": "Parent Epic"}

        with (
            patch("pathlib.Path.resolve", new=_fake_resolve),
            patch("agentic_devtools.cli.speckit.scaffold_new_feature._create_or_checkout_branch"),
            patch("agentic_devtools.cli.speckit.scaffold_new_feature.detect_parent_hierarchy", side_effect=_detect),
        ):
            result = prepare_new_feature(
                repo_root=tmp_path,
                feature_description="Child task",
                feature_number=2,
                dry_run=False,
            )

        parent_spec = tmp_path / "specs" / "1-parent-epic" / "spec.md"
        assert parent_spec.read_text(encoding="utf-8") == ""
        assert result.spec_file.read_text(encoding="utf-8") == ""

    def test_prepare_new_feature_flat_fallback_creates_empty_spec_when_no_template(self, tmp_path: Path) -> None:
        with (
            patch("agentic_devtools.cli.speckit.scaffold_new_feature._create_or_checkout_branch"),
            patch(
                "agentic_devtools.cli.speckit.scaffold_new_feature.detect_parent_hierarchy",
                return_value={"status": "ok"},
            ),
        ):
            result = prepare_new_feature(
                repo_root=tmp_path,
                feature_description="Add login flow",
                feature_number=42,
                dry_run=False,
            )
        assert result.spec_file.read_text(encoding="utf-8") == ""

    def test_prepare_new_feature_flat_skips_spec_when_already_exists(self, tmp_path: Path) -> None:
        feature_dir = tmp_path / "specs" / "42-login-flow"
        feature_dir.mkdir(parents=True)
        (feature_dir / "spec.md").write_text("# Existing\n", encoding="utf-8")
        with patch("agentic_devtools.cli.speckit.scaffold_new_feature._create_or_checkout_branch"):
            result = prepare_new_feature(
                repo_root=tmp_path,
                feature_description="Add login flow",
                feature_number=42,
                flat=True,
                dry_run=False,
            )
        assert result.spec_file.read_text(encoding="utf-8") == "# Existing\n"

    def test_prepare_new_feature_flat_fallback_skips_spec_when_already_exists(self, tmp_path: Path) -> None:
        feature_dir = tmp_path / "specs" / "42-login-flow"
        feature_dir.mkdir(parents=True)
        (feature_dir / "spec.md").write_text("# Existing\n", encoding="utf-8")
        with (
            patch("agentic_devtools.cli.speckit.scaffold_new_feature._create_or_checkout_branch"),
            patch(
                "agentic_devtools.cli.speckit.scaffold_new_feature.detect_parent_hierarchy",
                return_value={"status": "ok"},
            ),
        ):
            result = prepare_new_feature(
                repo_root=tmp_path,
                feature_description="Add login flow",
                feature_number=42,
                dry_run=False,
            )
        assert result.spec_file.read_text(encoding="utf-8") == "# Existing\n"

    def test_prepare_new_feature_existing_parent_uses_detected_parent_hierarchy_metadata(self, tmp_path: Path) -> None:
        parent_dir = tmp_path / "specs" / "1-existing-parent"
        parent_dir.mkdir(parents=True)

        def _detect(number: int, repo_root: Path | None = None) -> dict[str, str]:
            if number == 2:
                return {"level": "task"}
            if number == 1:
                return {"title": "Parent Epic", "level": "epic"}
            return {}

        with (
            patch("agentic_devtools.cli.speckit.scaffold_new_feature._create_or_checkout_branch"),
            patch("agentic_devtools.cli.speckit.scaffold_new_feature.detect_parent_hierarchy", side_effect=_detect),
        ):
            prepare_new_feature(
                repo_root=tmp_path,
                feature_description="Nested Child",
                feature_number=2,
                parent_feature_number=1,
                dry_run=False,
            )

        hierarchy_data = yaml.safe_load((parent_dir / "hierarchy.yml").read_text(encoding="utf-8"))
        assert hierarchy_data["title"] == "Parent Epic"
        assert hierarchy_data["level"] == "epic"

    def test_prepare_new_feature_auto_numbering_does_not_run_parent_detection(self, tmp_path: Path) -> None:
        with (
            patch("agentic_devtools.cli.speckit.scaffold_new_feature._create_or_checkout_branch"),
            patch("agentic_devtools.cli.speckit.scaffold_new_feature._detect_next_feature_number", return_value=1),
            patch("agentic_devtools.cli.speckit.scaffold_new_feature.detect_parent_hierarchy") as detect_mock,
        ):
            result = prepare_new_feature(repo_root=tmp_path, feature_description="Add login flow", dry_run=True)
        detect_mock.assert_not_called()
        assert result.feature_dir == tmp_path / "specs" / "001-login-flow"
