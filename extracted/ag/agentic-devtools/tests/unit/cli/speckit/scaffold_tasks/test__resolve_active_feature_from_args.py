"""Tests for ``_resolve_active_feature_from_args``."""

from pathlib import Path
from unittest.mock import patch

import pytest

from agentic_devtools.cli.speckit.scaffold_common import (
    SPECIFY_FEATURE_DIRECTORY_ENV,
    ActiveFeature,
    FeatureResolutionError,
)
from agentic_devtools.cli.speckit.scaffold_tasks import _resolve_active_feature_from_args


def test_resolve_active_feature_from_args_uses_resolver_when_spec_dir_missing() -> None:
    expected = ActiveFeature(repo_root=Path("/repo"), feature_dir=Path("/repo/specs/1"), branch="1", has_git=True)
    with patch("agentic_devtools.cli.speckit.scaffold_tasks.resolve_active_feature", return_value=expected):
        assert _resolve_active_feature_from_args(None) == expected


def test_resolve_active_feature_from_args_rejects_outside_repo(tmp_path: Path) -> None:
    with patch("agentic_devtools.cli.speckit.scaffold_tasks.get_repo_root", return_value=tmp_path):
        with pytest.raises(FeatureResolutionError, match="outside repository specs directory"):
            _resolve_active_feature_from_args("../outside")


def test_resolve_active_feature_from_args_rejects_non_specs_path(tmp_path: Path) -> None:
    with patch("agentic_devtools.cli.speckit.scaffold_tasks.get_repo_root", return_value=tmp_path):
        with pytest.raises(FeatureResolutionError, match="outside repository specs directory"):
            _resolve_active_feature_from_args("myfeature")


def test_resolve_active_feature_from_args_returns_active_feature_for_valid_spec_dir(tmp_path: Path) -> None:
    with patch("agentic_devtools.cli.speckit.scaffold_tasks.get_repo_root", return_value=tmp_path):
        active = _resolve_active_feature_from_args("specs/42")
    assert active.feature_dir == (tmp_path / "specs" / "42")


def test_resolve_active_feature_from_args_preserves_branch_from_active_metadata(tmp_path: Path, monkeypatch) -> None:
    repo_root = tmp_path
    feature_dir = repo_root / "specs" / "100-parent" / "200"
    feature_dir.mkdir(parents=True)
    metadata_dir = repo_root / ".specify"
    metadata_dir.mkdir(parents=True)
    (metadata_dir / "feature.json").write_text(
        '{"feature_directory":"specs/100-parent/200","branch_name":"200-child-feature"}',
        encoding="utf-8",
    )
    monkeypatch.delenv(SPECIFY_FEATURE_DIRECTORY_ENV, raising=False)
    with patch("agentic_devtools.cli.speckit.scaffold_tasks.get_repo_root", return_value=repo_root):
        active = _resolve_active_feature_from_args("specs/100-parent/200")
    assert active.feature_dir == feature_dir
    assert active.branch == "200-child-feature"


def test_resolve_active_feature_from_args_matches_git_branch_prefix_when_metadata_unavailable(tmp_path: Path) -> None:
    feature_dir = tmp_path / "specs" / "200"
    feature_dir.mkdir(parents=True)
    with (
        patch("agentic_devtools.cli.speckit.scaffold_tasks.get_repo_root", return_value=tmp_path),
        patch(
            "agentic_devtools.cli.speckit.scaffold_tasks.resolve_active_feature",
            side_effect=FeatureResolutionError("broken metadata"),
        ),
        patch("agentic_devtools.cli.speckit.scaffold_tasks.has_git_repo", return_value=True),
        patch("agentic_devtools.cli.speckit.scaffold_tasks.get_current_branch", return_value="200-child-feature"),
    ):
        active = _resolve_active_feature_from_args("specs/200")
    assert active.branch == "200-child-feature"


def test_resolve_active_feature_from_args_keeps_dir_name_when_git_branch_unavailable(tmp_path: Path) -> None:
    feature_dir = tmp_path / "specs" / "200"
    feature_dir.mkdir(parents=True)
    with (
        patch("agentic_devtools.cli.speckit.scaffold_tasks.get_repo_root", return_value=tmp_path),
        patch(
            "agentic_devtools.cli.speckit.scaffold_tasks.resolve_active_feature",
            side_effect=FeatureResolutionError("broken metadata"),
        ),
        patch("agentic_devtools.cli.speckit.scaffold_tasks.has_git_repo", return_value=True),
        patch("agentic_devtools.cli.speckit.scaffold_tasks.get_current_branch", return_value=None),
    ):
        active = _resolve_active_feature_from_args("specs/200")
    assert active.branch == "200"


def test_resolve_active_feature_from_args_rejects_symlinked_spec_dir(tmp_path: Path) -> None:
    target = tmp_path / "specs" / "42-real"
    target.mkdir(parents=True)
    link = tmp_path / "specs" / "42-link"
    link.symlink_to(target)
    with patch("agentic_devtools.cli.speckit.scaffold_tasks.get_repo_root", return_value=tmp_path):
        with pytest.raises(FeatureResolutionError, match="symlink"):
            _resolve_active_feature_from_args("specs/42-link")


def test_resolve_active_feature_from_args_keeps_dir_name_when_git_prefix_mismatches(tmp_path: Path) -> None:
    feature_dir = tmp_path / "specs" / "200"
    feature_dir.mkdir(parents=True)
    with (
        patch("agentic_devtools.cli.speckit.scaffold_tasks.get_repo_root", return_value=tmp_path),
        patch(
            "agentic_devtools.cli.speckit.scaffold_tasks.resolve_active_feature",
            side_effect=FeatureResolutionError("broken metadata"),
        ),
        patch("agentic_devtools.cli.speckit.scaffold_tasks.has_git_repo", return_value=True),
        patch("agentic_devtools.cli.speckit.scaffold_tasks.get_current_branch", return_value="main"),
    ):
        active = _resolve_active_feature_from_args("specs/200")
    assert active.branch == "200"
