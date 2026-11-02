"""Tests for agentic_devtools.cli.issue_template.exceptions.TemplateNotFoundError."""

from __future__ import annotations

from agentic_devtools.cli.issue_template.exceptions import TemplateNotFoundError


class TestTemplateNotFoundError:
    """Tests for the TemplateNotFoundError exception class."""

    def test_is_exception_subclass(self) -> None:
        """TemplateNotFoundError is a subclass of Exception."""
        assert issubclass(TemplateNotFoundError, Exception)

    def test_can_be_raised_and_caught(self) -> None:
        """TemplateNotFoundError can be raised and caught."""
        try:
            raise TemplateNotFoundError("template missing")
        except TemplateNotFoundError as exc:
            assert str(exc) == "template missing"

    def test_message_preserved(self) -> None:
        """The error message is preserved in the exception."""
        exc = TemplateNotFoundError("file not found: issue-template.md")
        assert "file not found" in str(exc)
