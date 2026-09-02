"""Tests for ``scaffold_new_feature_command``."""

from pathlib import Path
from unittest.mock import patch

import pytest

from agentic_devtools.cli.speckit import scaffold_new_feature
from agentic_devtools.cli.speckit.scaffold_new_feature import FeatureScaffoldResult


def test_scaffold_new_feature_command_json_output(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    result = FeatureScaffoldResult(
        repo_root=tmp_path,
        feature_dir=tmp_path / "specs" / "42-x",
        spec_file=tmp_path / "specs" / "42-x" / "spec.md",
        branch_name="42-x",
        feature_number="42",
        parent_dir=None,
        hierarchy_level=None,
    )
    monkeypatch.setattr(scaffold_new_feature, "is_dry_run", lambda: False)
    monkeypatch.setattr(scaffold_new_feature, "prepare_new_feature", lambda **kwargs: result)
    with patch("builtins.print") as print_mock:
        scaffold_new_feature.scaffold_new_feature_command(["--json", "Add login"])
    assert '"FEATURE_NUM": "42"' in print_mock.call_args[0][0]


def test_scaffold_new_feature_command_parent_requires_issue(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(scaffold_new_feature, "is_dry_run", lambda: False)
    with pytest.raises(SystemExit) as exc_info:
        scaffold_new_feature.scaffold_new_feature_command(["--parent", "1", "Add login"])
    assert exc_info.value.code != 0


def test_scaffold_new_feature_command_flat_parent_does_not_require_issue(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    result = FeatureScaffoldResult(
        repo_root=tmp_path,
        feature_dir=tmp_path / "specs" / "42-x",
        spec_file=tmp_path / "specs" / "42-x" / "spec.md",
        branch_name="42-x",
        feature_number="42",
        parent_dir=None,
        hierarchy_level=None,
    )
    monkeypatch.setattr(scaffold_new_feature, "is_dry_run", lambda: False)
    monkeypatch.setattr(scaffold_new_feature, "prepare_new_feature", lambda **kwargs: result)
    # --flat with --parent should NOT require --issue
    scaffold_new_feature.scaffold_new_feature_command(["--flat", "--parent", "1", "Add login"])


def test_scaffold_new_feature_command_plain_and_dry_run_output(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    result = FeatureScaffoldResult(
        repo_root=tmp_path,
        feature_dir=tmp_path / "specs" / "42-x",
        spec_file=tmp_path / "specs" / "42-x" / "spec.md",
        branch_name="42-x",
        feature_number="42",
        parent_dir=None,
        hierarchy_level=None,
    )
    monkeypatch.setattr(scaffold_new_feature, "prepare_new_feature", lambda **kwargs: result)
    monkeypatch.setattr(scaffold_new_feature, "is_dry_run", lambda: True)
    with patch("builtins.print") as print_mock:
        scaffold_new_feature.scaffold_new_feature_command(["Add login"])
    assert "[DRY RUN]" in print_mock.call_args[0][0]
