"""Tests for ``FeatureScaffoldResult``."""

from pathlib import Path

from agentic_devtools.cli.speckit.scaffold_new_feature import FeatureScaffoldResult


def test_to_dict_uses_posix_paths(tmp_path: Path) -> None:
    result = FeatureScaffoldResult(
        repo_root=tmp_path,
        feature_dir=tmp_path / "specs" / "42-add-login",
        spec_file=tmp_path / "specs" / "42-add-login" / "spec.md",
        branch_name="42-add-login",
        feature_number="42",
        parent_dir=None,
        hierarchy_level=None,
    )
    payload = result.to_dict()
    assert payload["FEATURE_DIR"].endswith("/specs/42-add-login")
