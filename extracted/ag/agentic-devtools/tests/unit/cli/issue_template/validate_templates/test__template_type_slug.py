"""Tests for _template_type_slug()."""

from __future__ import annotations

from agentic_devtools.cli.issue_template.validate_templates import _template_type_slug


class TestTemplateTypeSlug:
    """Tests for deriving a type slug from a registered template filename."""

    def test_default_template_returns_none(self) -> None:
        """The default template name has no type slug."""
        assert _template_type_slug("issue-template.md") is None

    def test_typed_template_returns_slug(self) -> None:
        """A typed template name returns its slug."""
        assert _template_type_slug("issue-template-bug.md") == "bug"

    def test_non_matching_returns_none(self) -> None:
        """A non issue-template filename returns None."""
        assert _template_type_slug("spec-template.md") is None
