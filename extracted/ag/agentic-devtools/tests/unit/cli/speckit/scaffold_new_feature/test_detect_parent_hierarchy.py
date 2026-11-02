"""Tests for ``detect_parent_hierarchy``."""

from pathlib import Path
from unittest.mock import patch

from agentic_devtools.cli.speckit.scaffold_new_feature import detect_parent_hierarchy


def test_detect_parent_hierarchy_parses_cli_output(tmp_path: Path) -> None:
    with (
        patch("agentic_devtools.cli.speckit.scaffold_new_feature._repo_slug_from_git", return_value="owner/repo"),
        patch(
            "subprocess.run",
            return_value=type(
                "Completed",
                (),
                {"returncode": 0, "stdout": "status=ok\nparent=1\nlevel=feature\ntitle=Issue 1\n"},
            )(),
        ),
    ):
        payload = detect_parent_hierarchy(2, repo_root=tmp_path)
    assert payload == {"status": "ok", "parent": "1", "level": "feature", "title": "Issue 1"}


def test_detect_parent_hierarchy_normalizes_null_sentinel(tmp_path: Path) -> None:
    with (
        patch("agentic_devtools.cli.speckit.scaffold_new_feature._repo_slug_from_git", return_value="owner/repo"),
        patch(
            "subprocess.run",
            return_value=type(
                "Completed",
                (),
                {"returncode": 0, "stdout": "status=ok\nparent=null\nlevel=epic\ntitle=Top Level\n"},
            )(),
        ),
    ):
        payload = detect_parent_hierarchy(1, repo_root=tmp_path)
    assert payload is not None
    assert payload["parent"] is None
    assert payload["level"] == "epic"


def test_detect_parent_hierarchy_returns_none_without_repo_slug(tmp_path: Path) -> None:
    with patch("agentic_devtools.cli.speckit.scaffold_new_feature._repo_slug_from_git", return_value=None):
        assert detect_parent_hierarchy(2, repo_root=tmp_path) is None
