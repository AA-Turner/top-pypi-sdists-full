"""Tests for _extract_footnotes_body in record_discovery_baseline."""

from __future__ import annotations

from tests.scripts.record_discovery_baseline import baseline


def test_returns_placeholder_when_footnotes_section_is_absent():
    """A document with no Footnotes heading returns the default placeholder."""
    assert baseline._extract_footnotes_body("no footnotes here") == "- None recorded."


def test_returns_placeholder_when_footnotes_section_is_empty():
    """An empty Footnotes section (only blank lines) returns the default placeholder."""
    document = "## Footnotes\n\n\n"
    assert baseline._extract_footnotes_body(document) == "- None recorded."


def test_returns_placeholder_when_footnotes_body_is_default():
    """The default placeholder is returned unchanged."""
    document = "## Footnotes\n\n- None recorded.\n"
    assert baseline._extract_footnotes_body(document) == "- None recorded."


def test_returns_recorded_footnote_entries():
    """Non-default footnote content is returned verbatim (stripped)."""
    document = "## Footnotes\n\n- /agdt.foo — not offered by VS Code Copilot Chat.\n"
    assert baseline._extract_footnotes_body(document) == "- /agdt.foo — not offered by VS Code Copilot Chat."


def test_stops_at_the_next_section_heading():
    """Content after a subsequent ## heading is not included in the footnote body."""
    document = "## Footnotes\n\n- note\n\n## Other\n\nextra\n"
    assert baseline._extract_footnotes_body(document) == "- note"
