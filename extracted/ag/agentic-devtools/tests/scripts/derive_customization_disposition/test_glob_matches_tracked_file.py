"""Tests for glob_matches_tracked_file in derive_customization_disposition."""

from __future__ import annotations

from pathlib import Path

from tests.scripts.derive_customization_disposition import REPO_ROOT, derive


def test_matching_glob_is_true() -> None:
    """T2 requires the glob to match at least one tracked file."""
    tracked = derive.tracked_files(REPO_ROOT)
    assert derive.glob_matches_tracked_file("scripts/*.py", REPO_ROOT, tracked) is True


def test_non_matching_glob_is_false() -> None:
    """A glob matching nothing does not satisfy T2."""
    tracked = derive.tracked_files(REPO_ROOT)
    assert derive.glob_matches_tracked_file("no-such-directory/*.py", REPO_ROOT, tracked) is False


def test_empty_glob_is_false() -> None:
    """An empty pattern would otherwise raise inside pathlib."""
    assert derive.glob_matches_tracked_file("/", REPO_ROOT, frozenset()) is False


def test_invalid_glob_is_false(tmp_path: Path) -> None:
    """A pattern pathlib rejects is reported as no match, not raised."""
    assert derive.glob_matches_tracked_file("**a/*.py", tmp_path, frozenset()) is False


def test_untracked_file_does_not_satisfy_t2(tmp_path: Path) -> None:
    """A glob that matches a file on disk but not in the tracked set does not fire T2."""
    untracked = tmp_path / "src" / "module.py"
    untracked.parent.mkdir(parents=True)
    untracked.write_text("# untracked\n", encoding="utf-8")
    # tracked set is empty — nothing is tracked in tmp_path
    assert derive.glob_matches_tracked_file("src/*.py", tmp_path, frozenset()) is False


def test_tracked_file_missing_from_worktree_still_satisfies_t2(tmp_path: Path) -> None:
    """T2 is defined on tracked files, even when the file is absent on disk."""
    tracked = frozenset({"src/module.py"})
    assert derive.glob_matches_tracked_file("src/*.py", tmp_path, tracked) is True


def test_absent_tracked_file_in_nested_dir_does_not_match_shallow_glob(tmp_path: Path) -> None:
    """Right-anchored PurePosixPath.match() would make ``nested/src/module.py``
    satisfy ``src/*.py``; the absent-file path uses root-relative matching to
    avoid this false positive."""
    # tracked path has an extra leading component not in the glob
    tracked = frozenset({"nested/src/module.py"})
    assert derive.glob_matches_tracked_file("src/*.py", tmp_path, tracked) is False
