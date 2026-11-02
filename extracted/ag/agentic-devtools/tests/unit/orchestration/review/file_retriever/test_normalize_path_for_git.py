"""Tests for normalize_path_for_git function."""

from __future__ import annotations

from agentic_devtools.orchestration.review.file_retriever import normalize_path_for_git


class TestNormalizePathForGit:
    """Tests for git path normalization."""

    def test_strips_leading_slash(self) -> None:
        assert normalize_path_for_git("/src/app.py") == "src/app.py"

    def test_no_change_without_slash(self) -> None:
        assert normalize_path_for_git("src/app.py") == "src/app.py"
