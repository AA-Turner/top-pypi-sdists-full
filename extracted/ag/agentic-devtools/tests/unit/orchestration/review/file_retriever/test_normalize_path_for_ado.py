"""Tests for normalize_path_for_ado function."""

from __future__ import annotations

from agentic_devtools.orchestration.review.file_retriever import normalize_path_for_ado


class TestNormalizePathForAdo:
    """Tests for ADO path normalization."""

    def test_adds_leading_slash(self) -> None:
        assert normalize_path_for_ado("src/app.py") == "/src/app.py"

    def test_no_change_with_slash(self) -> None:
        assert normalize_path_for_ado("/src/app.py") == "/src/app.py"
