"""Tests for split_frontmatter in derive_customization_disposition."""

from __future__ import annotations

from tests.scripts.derive_customization_disposition import derive


def test_splits_frontmatter_from_body() -> None:
    """The YAML block and the body are returned separately."""
    frontmatter, body = derive.split_frontmatter("---\nagent: agdt.x\n---\n# Title\n")
    assert frontmatter.strip() == "agent: agdt.x"
    assert body.strip() == "# Title"


def test_file_without_frontmatter_is_all_body() -> None:
    """A file with no frontmatter yields an empty frontmatter and the whole text."""
    assert derive.split_frontmatter("# Title\n") == ("", "# Title\n")


def test_unterminated_frontmatter_is_all_body() -> None:
    """An unterminated block is not frontmatter, so nothing is stripped."""
    text = "---\nagent: agdt.x\n"
    assert derive.split_frontmatter(text) == ("", text)
