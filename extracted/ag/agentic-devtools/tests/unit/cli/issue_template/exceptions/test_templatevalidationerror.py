"""Tests for agentic_devtools.cli.issue_template.exceptions.TemplateValidationError."""

from __future__ import annotations

from agentic_devtools.cli.issue_template.exceptions import TemplateValidationError


class TestTemplateValidationError:
    """Tests for the TemplateValidationError exception class."""

    def test_is_exception_subclass(self) -> None:
        """TemplateValidationError is a subclass of Exception."""
        assert issubclass(TemplateValidationError, Exception)

    def test_can_be_raised_and_caught(self) -> None:
        """TemplateValidationError can be raised and caught."""
        try:
            raise TemplateValidationError("missing required property")
        except TemplateValidationError as exc:
            assert str(exc) == "missing required property"

    def test_message_preserved(self) -> None:
        """The error message is preserved in the exception."""
        exc = TemplateValidationError("Missing required properties: 'severity'")
        assert "severity" in str(exc)
