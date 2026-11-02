"""Tests for tracked_files in derive_customization_disposition."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

import pytest

from tests.scripts.derive_customization_disposition import REPO_ROOT, derive


def test_returns_frozenset_of_paths() -> None:
    """Returns a frozenset of relative POSIX paths when git is available."""
    result = derive.tracked_files(REPO_ROOT)
    assert isinstance(result, frozenset)
    assert "scripts/derive_customization_disposition.py" in result


def test_raises_on_git_failure(tmp_path: Path) -> None:
    """Raises RuntimeError when git ls-files fails instead of silently returning empty."""
    with pytest.raises(RuntimeError, match="git ls-files failed"):
        derive.tracked_files(tmp_path)


def test_raises_on_oserror(tmp_path: Path) -> None:
    """Raises RuntimeError when git is not available (OSError)."""
    with patch("subprocess.run", side_effect=OSError("git not found")):
        with pytest.raises(RuntimeError, match="git ls-files failed"):
            derive.tracked_files(tmp_path)
