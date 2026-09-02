"""Tests for ``resolve_active_feature``."""

from pathlib import Path
from unittest.mock import patch

import pytest

from agentic_devtools.cli.speckit import scaffold_common
from agentic_devtools.cli.speckit.scaffold_common import (
    SPECIFY_FEATURE_DIRECTORY_ENV,
    FeatureResolutionError,
    resolve_active_feature,
)


class TestResolveActiveFeature:
    """resolve_active_feature applies the documented resolution order."""

    def test_env_var_takes_precedence(self, tmp_path: Path, monkeypatch) -> None:
        monkeypatch.setenv(SPECIFY_FEATURE_DIRECTORY_ENV, "042-from-env")
        monkeypatch.setattr(scaffold_common, "has_git_repo", lambda root: True)
        monkeypatch.setattr(scaffold_common, "get_current_branch", lambda root: "main")

        active = resolve_active_feature(tmp_path)

        assert active.feature_dir == tmp_path / "specs" / "042-from-env"
        assert active.branch == "042-from-env"
        assert active.has_git is True

    def test_env_var_bare_name_under_symlinked_specs_root_raises(self, tmp_path: Path, monkeypatch) -> None:
        repo_root = tmp_path / "repo"
        repo_root.mkdir()
        outside_specs = tmp_path / "outside-specs"
        outside_specs.mkdir()
        monkeypatch.setenv(SPECIFY_FEATURE_DIRECTORY_ENV, "042-from-env")
        monkeypatch.setattr(scaffold_common, "has_git_repo", lambda root: True)
        monkeypatch.setattr(scaffold_common, "get_current_branch", lambda root: "main")

        with (
            patch.object(Path, "resolve", side_effect=[outside_specs / "042-from-env", outside_specs, repo_root]),
            pytest.raises(FeatureResolutionError, match=r"outside the repository root"),
        ):
            resolve_active_feature(repo_root)

    def test_env_var_explicit_relative_path_remains_opt_in(self, tmp_path: Path, monkeypatch) -> None:
        repo_root = tmp_path / "repo"
        repo_root.mkdir()
        monkeypatch.setenv(SPECIFY_FEATURE_DIRECTORY_ENV, "custom/042-from-env")
        monkeypatch.setattr(scaffold_common, "has_git_repo", lambda root: False)

        active = resolve_active_feature(repo_root)

        assert active.feature_dir == repo_root / "custom" / "042-from-env"
        assert active.branch == "042-from-env"

    def test_feature_json_used_when_env_absent(self, tmp_path: Path, monkeypatch) -> None:
        monkeypatch.delenv(SPECIFY_FEATURE_DIRECTORY_ENV, raising=False)
        specify_dir = tmp_path / ".specify"
        specify_dir.mkdir()
        (specify_dir / "feature.json").write_text('{"feature_directory": "042-from-json"}', encoding="utf-8")
        monkeypatch.setattr(scaffold_common, "has_git_repo", lambda root: False)

        active = resolve_active_feature(tmp_path)

        assert active.feature_dir == tmp_path / "specs" / "042-from-json"
        assert active.branch == "042-from-json"

    def test_feature_json_supports_specs_relative_path(self, tmp_path: Path, monkeypatch) -> None:
        monkeypatch.delenv(SPECIFY_FEATURE_DIRECTORY_ENV, raising=False)
        specify_dir = tmp_path / ".specify"
        specify_dir.mkdir()
        (specify_dir / "feature.json").write_text(
            '{"feature_directory": "specs/042-from-json-path"}',
            encoding="utf-8",
        )
        monkeypatch.setattr(scaffold_common, "has_git_repo", lambda root: False)

        active = resolve_active_feature(tmp_path)

        assert active.feature_dir == tmp_path / "specs" / "042-from-json-path"
        assert active.branch == "042-from-json-path"

    def test_git_branch_matches_existing_prefixed_dir(self, tmp_path: Path, monkeypatch) -> None:
        monkeypatch.delenv(SPECIFY_FEATURE_DIRECTORY_ENV, raising=False)
        existing = tmp_path / "specs" / "042-existing-feature"
        existing.mkdir(parents=True)
        monkeypatch.setattr(scaffold_common, "has_git_repo", lambda root: True)
        monkeypatch.setattr(scaffold_common, "get_current_branch", lambda root: "042-existing-feature")

        active = resolve_active_feature(tmp_path)

        assert active.feature_dir == existing
        assert active.branch == "042-existing-feature"
        assert active.has_git is True

    def test_git_branch_matches_existing_nested_prefixed_dir(self, tmp_path: Path, monkeypatch) -> None:
        monkeypatch.delenv(SPECIFY_FEATURE_DIRECTORY_ENV, raising=False)
        existing = tmp_path / "specs" / "010-parent" / "042-existing-feature"
        existing.mkdir(parents=True)
        monkeypatch.setattr(scaffold_common, "has_git_repo", lambda root: True)
        monkeypatch.setattr(scaffold_common, "get_current_branch", lambda root: "042-existing-feature")

        active = resolve_active_feature(tmp_path)

        assert active.feature_dir == existing
        assert active.branch == "042-existing-feature"

    def test_git_branch_with_no_matching_dir_falls_back_to_branch_name(self, tmp_path: Path, monkeypatch) -> None:
        monkeypatch.delenv(SPECIFY_FEATURE_DIRECTORY_ENV, raising=False)
        monkeypatch.setattr(scaffold_common, "has_git_repo", lambda root: True)
        monkeypatch.setattr(scaffold_common, "get_current_branch", lambda root: "099-new-feature")

        active = resolve_active_feature(tmp_path)

        assert active.feature_dir == tmp_path / "specs" / "099-new-feature"
        assert active.branch == "099-new-feature"

    def test_git_branch_fallback_symlink_escaping_repo_root_raises(self, tmp_path: Path, monkeypatch) -> None:
        monkeypatch.delenv(SPECIFY_FEATURE_DIRECTORY_ENV, raising=False)
        outside = tmp_path / "outside"
        outside.mkdir()
        specs_dir = tmp_path / "specs"
        specs_dir.mkdir()
        (specs_dir / "099-new-feature").mkdir()
        monkeypatch.setattr(scaffold_common, "has_git_repo", lambda root: True)
        monkeypatch.setattr(scaffold_common, "get_current_branch", lambda root: "099-new-feature")

        with (
            patch.object(Path, "resolve", side_effect=[outside / "099-new-feature", specs_dir, tmp_path]),
            pytest.raises(FeatureResolutionError, match=r"outside specs/"),
        ):
            resolve_active_feature(tmp_path)

    def test_git_branch_without_numeric_prefix_uses_main_fallback(self, tmp_path: Path, monkeypatch) -> None:
        monkeypatch.delenv(SPECIFY_FEATURE_DIRECTORY_ENV, raising=False)
        monkeypatch.setattr(scaffold_common, "has_git_repo", lambda root: True)
        monkeypatch.setattr(scaffold_common, "get_current_branch", lambda root: "main")

        active = resolve_active_feature(tmp_path)

        assert active.feature_dir == tmp_path / "specs" / "main"
        assert active.branch == "main"

    def test_main_fallback_under_symlinked_specs_root_raises(self, tmp_path: Path, monkeypatch) -> None:
        repo_root = tmp_path / "repo"
        repo_root.mkdir()
        monkeypatch.delenv(SPECIFY_FEATURE_DIRECTORY_ENV, raising=False)
        outside_specs = tmp_path / "outside-specs"
        outside_specs.mkdir()
        monkeypatch.setattr(scaffold_common, "has_git_repo", lambda root: True)
        monkeypatch.setattr(scaffold_common, "get_current_branch", lambda root: "main")

        with (
            patch.object(Path, "resolve", side_effect=[outside_specs / "main", outside_specs, repo_root]),
            pytest.raises(FeatureResolutionError, match=r"outside the repository root"),
        ):
            resolve_active_feature(repo_root)

    def test_git_branch_without_numeric_prefix_uses_latest_numbered_fallback(self, tmp_path: Path, monkeypatch) -> None:
        monkeypatch.delenv(SPECIFY_FEATURE_DIRECTORY_ENV, raising=False)
        (tmp_path / "specs" / "001-a").mkdir(parents=True)
        (tmp_path / "specs" / "042-b").mkdir(parents=True)
        monkeypatch.setattr(scaffold_common, "has_git_repo", lambda root: True)
        monkeypatch.setattr(scaffold_common, "get_current_branch", lambda root: "copilot/repair-branch")

        active = resolve_active_feature(tmp_path)

        assert active.feature_dir == tmp_path / "specs" / "042-b"
        assert active.branch == "042-b"

    def test_multiple_prefix_matches_raise(self, tmp_path: Path, monkeypatch) -> None:
        monkeypatch.delenv(SPECIFY_FEATURE_DIRECTORY_ENV, raising=False)
        (tmp_path / "specs" / "042-a").mkdir(parents=True)
        (tmp_path / "specs" / "042-b").mkdir(parents=True)
        monkeypatch.setattr(scaffold_common, "has_git_repo", lambda root: True)
        monkeypatch.setattr(scaffold_common, "get_current_branch", lambda root: "042-new")

        with pytest.raises(FeatureResolutionError):
            resolve_active_feature(tmp_path)

    def test_non_git_fallback_uses_latest_numbered_dir(self, tmp_path: Path, monkeypatch) -> None:
        monkeypatch.delenv(SPECIFY_FEATURE_DIRECTORY_ENV, raising=False)
        (tmp_path / "specs" / "001-a").mkdir(parents=True)
        (tmp_path / "specs" / "042-b").mkdir(parents=True)
        monkeypatch.setattr(scaffold_common, "has_git_repo", lambda root: False)

        active = resolve_active_feature(tmp_path)

        assert active.feature_dir == tmp_path / "specs" / "042-b"
        assert active.branch == "042-b"
        assert active.has_git is False

    def test_final_fallback_is_main(self, tmp_path: Path, monkeypatch) -> None:
        monkeypatch.delenv(SPECIFY_FEATURE_DIRECTORY_ENV, raising=False)
        monkeypatch.setattr(scaffold_common, "has_git_repo", lambda root: False)

        active = resolve_active_feature(tmp_path)

        assert active.feature_dir == tmp_path / "specs" / "main"
        assert active.branch == "main"

    def test_feature_json_traversal_path_raises(self, tmp_path: Path, monkeypatch) -> None:
        monkeypatch.delenv(SPECIFY_FEATURE_DIRECTORY_ENV, raising=False)
        specify_dir = tmp_path / ".specify"
        specify_dir.mkdir()
        (specify_dir / "feature.json").write_text(
            '{"feature_directory": "../../outside"}',
            encoding="utf-8",
        )
        monkeypatch.setattr(scaffold_common, "has_git_repo", lambda root: False)

        with pytest.raises(FeatureResolutionError, match=r"outside specs/"):
            resolve_active_feature(tmp_path)

    def test_feature_json_symlink_escaping_specs_raises(self, tmp_path: Path, monkeypatch) -> None:
        monkeypatch.delenv(SPECIFY_FEATURE_DIRECTORY_ENV, raising=False)
        outside = tmp_path / "outside"
        outside.mkdir()
        specs_dir = tmp_path / "specs"
        specs_dir.mkdir()
        specify_dir = tmp_path / ".specify"
        specify_dir.mkdir()
        (specify_dir / "feature.json").write_text(
            '{"feature_directory": "escape-link"}',
            encoding="utf-8",
        )
        monkeypatch.setattr(scaffold_common, "has_git_repo", lambda root: False)

        with (
            patch.object(Path, "resolve", side_effect=[outside, specs_dir, tmp_path]),
            pytest.raises(FeatureResolutionError, match=r"outside specs/"),
        ):
            resolve_active_feature(tmp_path)

    def test_defaults_repo_root_to_get_repo_root(self, tmp_path: Path, monkeypatch) -> None:
        monkeypatch.delenv(SPECIFY_FEATURE_DIRECTORY_ENV, raising=False)
        monkeypatch.setattr(scaffold_common, "get_repo_root", lambda: tmp_path)
        monkeypatch.setattr(scaffold_common, "has_git_repo", lambda root: False)

        active = resolve_active_feature()

        assert active.repo_root == tmp_path

    # Repository-standard type/ISSUE-KEY/description branch format tests

    def test_github_type_key_branch_matches_existing_prefixed_dir(self, tmp_path: Path, monkeypatch) -> None:
        monkeypatch.delenv(SPECIFY_FEATURE_DIRECTORY_ENV, raising=False)
        (tmp_path / "specs" / "2249-squash-fix").mkdir(parents=True)
        monkeypatch.setattr(scaffold_common, "has_git_repo", lambda root: True)
        monkeypatch.setattr(scaffold_common, "get_current_branch", lambda root: "fix/2249/squash-fix")

        active = resolve_active_feature(tmp_path)

        assert active.feature_dir == tmp_path / "specs" / "2249-squash-fix"
        assert active.branch == "fix/2249/squash-fix"

    def test_github_type_key_branch_with_no_matching_dir_uses_numeric_key_fallback(
        self, tmp_path: Path, monkeypatch
    ) -> None:
        monkeypatch.delenv(SPECIFY_FEATURE_DIRECTORY_ENV, raising=False)
        (tmp_path / "specs").mkdir(parents=True)
        monkeypatch.setattr(scaffold_common, "has_git_repo", lambda root: True)
        monkeypatch.setattr(scaffold_common, "get_current_branch", lambda root: "fix/2249/squash-fix")

        active = resolve_active_feature(tmp_path)

        # Fallback uses the numeric key, not the full branch name
        assert active.feature_dir == tmp_path / "specs" / "2249"
        assert active.branch == "fix/2249/squash-fix"

    def test_jira_type_key_branch_matches_existing_prefixed_dir(self, tmp_path: Path, monkeypatch) -> None:
        monkeypatch.delenv(SPECIFY_FEATURE_DIRECTORY_ENV, raising=False)
        (tmp_path / "specs" / "1234-add-webhook").mkdir(parents=True)
        monkeypatch.setattr(scaffold_common, "has_git_repo", lambda root: True)
        monkeypatch.setattr(scaffold_common, "get_current_branch", lambda root: "feature/PROJECT-1234/add-webhook")

        active = resolve_active_feature(tmp_path)

        assert active.feature_dir == tmp_path / "specs" / "1234-add-webhook"
        assert active.branch == "feature/PROJECT-1234/add-webhook"

    def test_type_key_branch_with_no_prefix_falls_through_to_latest_numbered(self, tmp_path: Path, monkeypatch) -> None:
        """Branch with no numeric key (e.g. copilot/repair-branch) still uses latest numbered dir.

        The active branch recorded on ActiveFeature is the latest-numbered *directory
        name* (``"042-b"``), not the raw git branch, because the code reaches the
        ``_latest_numbered_feature_dir`` fallback path which passes the directory name
        as the branch argument.  This is the same pre-existing behavior verified by
        ``test_git_branch_without_numeric_prefix_uses_latest_numbered_fallback``.
        """
        monkeypatch.delenv(SPECIFY_FEATURE_DIRECTORY_ENV, raising=False)
        (tmp_path / "specs" / "042-b").mkdir(parents=True)
        monkeypatch.setattr(scaffold_common, "has_git_repo", lambda root: True)
        monkeypatch.setattr(scaffold_common, "get_current_branch", lambda root: "copilot/repair-branch")

        active = resolve_active_feature(tmp_path)

        assert active.feature_dir == tmp_path / "specs" / "042-b"
        # branch is the directory name, not the raw git branch, because the code
        # falls through to the latest-numbered-dir fallback path.
        assert active.branch == "042-b"
