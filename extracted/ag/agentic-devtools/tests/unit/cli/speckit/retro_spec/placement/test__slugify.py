"""Tests for _slugify in retro_spec/placement.py."""

from __future__ import annotations

from agentic_devtools.cli.speckit.retro_spec.placement import _slugify


class TestSlugify:
    """Tests for the _slugify helper."""

    def test_lowercases_and_replaces_spaces_with_hyphens(self) -> None:
        """Normal title becomes a lowercase hyphenated slug."""
        assert _slugify("Add Webhook Support") == "add-webhook-support"

    def test_strips_leading_and_trailing_hyphens(self) -> None:
        """Leading/trailing punctuation is stripped after conversion."""
        assert _slugify("--Title--") == "title"

    def test_collapses_multiple_punctuation_runs(self) -> None:
        """Multiple consecutive non-alphanumeric chars become a single hyphen."""
        assert _slugify("foo  --  bar") == "foo-bar"

    def test_caps_at_80_characters(self) -> None:
        """Slugs longer than 80 characters are truncated without a trailing hyphen."""
        long_title = "word " * 25  # 125 chars
        slug = _slugify(long_title)
        assert len(slug) <= 80
        assert not slug.endswith("-")

    def test_all_punctuation_returns_fallback(self) -> None:
        """A title made entirely of punctuation returns the 'spec' fallback."""
        assert _slugify("!!!???") == "spec"

    def test_empty_string_returns_fallback(self) -> None:
        """An empty string returns the 'spec' fallback."""
        assert _slugify("") == "spec"

    def test_preserves_digits(self) -> None:
        """Digits pass through the slug unchanged."""
        assert _slugify("Issue 42 fix") == "issue-42-fix"
