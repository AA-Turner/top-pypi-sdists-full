"""Tests for ``content_words``."""

from __future__ import annotations

from agentic_devtools.cli.checks.customization_quality import content_words


class TestContentWords:
    def test_lowercases_and_drops_short_words_and_stopwords(self) -> None:
        """Words of 3+ characters that are not stopwords survive, lowercased."""
        assert content_words("Use WHEN the Release notes ship") == {"release", "notes", "ship"}

    def test_returns_an_empty_set_for_text_without_content_words(self) -> None:
        """Text made only of stopwords and punctuation yields nothing."""
        assert content_words("the and -- for") == set()
