"""Tests for _truncate_content_item function."""

from __future__ import annotations

from agentic_devtools.orchestration.review.content_assembler import _truncate_content_item


class TestTruncateContentItem:
    """Tests for the content-item truncation helper."""

    def test_returns_none_for_non_positive_budget(self) -> None:
        """max_chars=0 returns None (nothing fits)."""
        item = {"path": "tests/test_app.py", "content": "abc"}
        assert _truncate_content_item(item, max_chars=0) is None

    def test_returns_none_when_only_path_fits(self) -> None:
        """Returns None when there is no room for any content beyond the path prefix."""
        item = {"path": "tests/test_app.py", "content": "abc"}
        assert _truncate_content_item(item, max_chars=len("tests/test_app.py\n")) is None

    def test_truncates_content_to_fit(self) -> None:
        """Content is truncated so that path + content fits within max_chars."""
        item = {"path": "a.py", "content": "x" * 100}
        prefix = "a.py\n"
        max_chars = len(prefix) + 10
        result = _truncate_content_item(item, max_chars=max_chars)
        assert result is not None
        assert result["path"] == "a.py"
        assert len(result["content"]) == 10
