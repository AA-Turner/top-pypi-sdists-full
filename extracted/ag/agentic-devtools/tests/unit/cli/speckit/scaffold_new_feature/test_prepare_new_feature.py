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
def _restore_env() -> Generator[None, None, None]:
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
