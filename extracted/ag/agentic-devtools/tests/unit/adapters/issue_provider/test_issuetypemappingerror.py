"""Tests for IssueTypeMappingError."""

from __future__ import annotations

import pytest

from agentic_devtools.adapters.issue_provider import IssueTypeMappingError


class TestIssueTypeMappingError:
    """IssueTypeMappingError is a ValueError subclass."""

    def test_is_value_error_subclass(self):
        """IssueTypeMappingError must be catchable as ValueError for protocol consistency."""
        assert issubclass(IssueTypeMappingError, ValueError)

    def test_is_exception_subclass(self):
        """IssueTypeMappingError is still an Exception."""
        assert issubclass(IssueTypeMappingError, Exception)

    def test_raise_and_catch_as_value_error(self):
        """Raising IssueTypeMappingError can be caught by except ValueError."""
        with pytest.raises(ValueError, match="unsupported"):
            raise IssueTypeMappingError("unsupported issue type")

    def test_raise_and_catch_as_issue_type_mapping_error(self):
        """Raising IssueTypeMappingError can still be caught by its own type."""
        with pytest.raises(IssueTypeMappingError, match="unsupported"):
            raise IssueTypeMappingError("unsupported issue type")

    def test_message_preserved(self):
        """IssueTypeMappingError preserves the message string."""
        exc = IssueTypeMappingError("type 'x' has no mapping")
        assert "type 'x' has no mapping" in str(exc)
