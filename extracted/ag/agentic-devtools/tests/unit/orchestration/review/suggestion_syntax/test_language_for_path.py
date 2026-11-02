"""Tests for language_for_path (FR-014, SC-007)."""

from agentic_devtools.orchestration.review.suggestion_syntax import language_for_path


class TestLanguageForPath:
    def test_python_extension(self):
        assert language_for_path("src/main.py") == "python"
        assert language_for_path("Stub.PYI") == "python"

    def test_unsupported_extension(self):
        assert language_for_path("src/main.ts") is None

    def test_extension_substring_not_matched(self):
        # ".spy" must not be treated as ".py".
        assert language_for_path("src/main.spy") is None
        assert language_for_path("notpy") is None
