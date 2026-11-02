"""Tests for is_supported_language (FR-014, SC-007)."""

from agentic_devtools.orchestration.review.suggestion_syntax import is_supported_language


class TestIsSupportedLanguage:
    def test_supported(self):
        assert is_supported_language("a.py") is True

    def test_unsupported(self):
        assert is_supported_language("a.rs") is False
