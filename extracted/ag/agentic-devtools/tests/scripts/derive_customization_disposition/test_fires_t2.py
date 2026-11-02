"""Tests for fires_t2 in derive_customization_disposition."""

from __future__ import annotations

from tests.scripts.derive_customization_disposition import REPO_ROOT, derive, unit


def test_glob_matching_a_tracked_file_fires() -> None:
    """T2 requires the glob to match at least one tracked file."""
    tracked = derive.tracked_files(REPO_ROOT)
    assert derive.fires_t2(unit(body="Applies to `scripts/*.py`.\n"), REPO_ROOT, tracked) is True


def test_glob_matching_nothing_does_not_fire() -> None:
    """A glob that matches nothing scopes nothing."""
    tracked = derive.tracked_files(REPO_ROOT)
    assert derive.fires_t2(unit(body="Applies to `nowhere/*.py`.\n"), REPO_ROOT, tracked) is False
