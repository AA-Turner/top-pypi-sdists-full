"""Tests for the ``ActiveFeature`` dataclass."""

from dataclasses import FrozenInstanceError
from pathlib import Path

import pytest

from agentic_devtools.cli.speckit.scaffold_common import ActiveFeature


class TestActiveFeature:
    """ActiveFeature is a frozen dataclass carrying the resolved feature context."""

    def test_stores_all_fields(self) -> None:
        active = ActiveFeature(
            repo_root=Path("/repo"),
            feature_dir=Path("/repo/specs/001-x"),
            branch="001-x",
            has_git=True,
        )
        assert active.repo_root == Path("/repo")
        assert active.feature_dir == Path("/repo/specs/001-x")
        assert active.branch == "001-x"
        assert active.has_git is True

    def test_is_frozen(self) -> None:
        active = ActiveFeature(
            repo_root=Path("/repo"),
            feature_dir=Path("/repo/specs/001-x"),
            branch="001-x",
            has_git=True,
        )
        with pytest.raises(FrozenInstanceError):
            active.branch = "other"  # type: ignore[misc]
