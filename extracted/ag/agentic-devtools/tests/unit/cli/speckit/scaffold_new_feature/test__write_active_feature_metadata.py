"""Tests for ``_write_active_feature_metadata``."""

import json
from pathlib import Path

from agentic_devtools.cli.speckit import scaffold_common
from agentic_devtools.cli.speckit.scaffold_common import SPECIFY_FEATURE_DIRECTORY_ENV
from agentic_devtools.cli.speckit.scaffold_new_feature import _write_active_feature_metadata


def test_writes_nested_posix_metadata_consumed_by_resolve_active_feature(tmp_path: Path, monkeypatch) -> None:
    repo_root = tmp_path
    feature_dir = repo_root / "specs" / "100-parent" / "200"
    feature_dir.mkdir(parents=True)
    monkeypatch.delenv(SPECIFY_FEATURE_DIRECTORY_ENV, raising=False)
    monkeypatch.setattr(scaffold_common, "has_git_repo", lambda root: False)

    _write_active_feature_metadata(repo_root, feature_dir, "200-child-feature")

    metadata_path = repo_root / ".specify" / "feature.json"
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    assert metadata == {
        "feature_directory": "specs/100-parent/200",
        "branch_name": "200-child-feature",
    }

    active = scaffold_common.resolve_active_feature(repo_root)
    assert active.feature_dir == feature_dir
    assert active.branch == "200-child-feature"
