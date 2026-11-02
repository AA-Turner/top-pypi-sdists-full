"""Tests for _normalize_content_items function."""

from __future__ import annotations

from agentic_devtools.orchestration.review.content_assembler import _normalize_content_items


class TestNormalizeContentItems:
    """Tests for the content-item normalisation helper."""

    def test_returns_empty_for_non_list(self) -> None:
        """Non-list input is treated as an empty list."""
        assert _normalize_content_items({"path": "x"}) == []

    def test_valid_items_are_preserved(self) -> None:
        """Valid {path, content} dicts pass through unchanged."""
        items = [{"path": "a.py", "content": "x"}]
        assert _normalize_content_items(items) == items

    def test_invalid_items_are_discarded(self) -> None:
        """Non-dict items and dicts with non-string values are discarded."""
        items = [
            "bad",
            {"path": 1, "content": "x"},
            {"path": "ok.py", "content": "ok"},
        ]
        assert _normalize_content_items(items) == [{"path": "ok.py", "content": "ok"}]
