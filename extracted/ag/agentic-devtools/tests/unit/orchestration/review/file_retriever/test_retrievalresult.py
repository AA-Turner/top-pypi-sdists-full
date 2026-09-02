"""Tests for RetrievalResult dataclass."""

from __future__ import annotations

from agentic_devtools.orchestration.review.file_retriever import RetrievalResult


class TestRetrievalResult:
    """Tests for RetrievalResult dataclass defaults and fields."""

    def test_default_context_status_is_success(self) -> None:
        """Default context_status is 'success'."""
        result = RetrievalResult()
        assert result.context_status == "success"

    def test_content_defaults_to_none(self) -> None:
        """Default content is None."""
        result = RetrievalResult()
        assert result.content is None

    def test_fields_set_correctly(self) -> None:
        """Fields set during construction are accessible."""
        result = RetrievalResult(content="hello", context_status="unavailable", context_status_reason="some_reason")
        assert result.content == "hello"
        assert result.context_status == "unavailable"
        assert result.context_status_reason == "some_reason"

    def test_estimated_tokens_defaults_to_zero(self) -> None:
        """Default estimated_tokens is 0."""
        result = RetrievalResult()
        assert result.estimated_tokens == 0

    def test_file_size_defaults_to_zero(self) -> None:
        """Default file_size is 0."""
        result = RetrievalResult()
        assert result.file_size == 0
