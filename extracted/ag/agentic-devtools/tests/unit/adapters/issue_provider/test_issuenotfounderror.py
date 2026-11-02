"""Tests for IssueNotFoundError."""

from __future__ import annotations

import pytest

from agentic_devtools.adapters.issue_provider import IssueNotFoundError


class TestIssueNotFoundError:
    """IssueNotFoundError remains compatible with ValueError handlers."""

    def test_is_value_error_subclass(self) -> None:
        """Callers can catch definitive not-found results as ValueError."""
        assert issubclass(IssueNotFoundError, ValueError)

    def test_raise_and_catch_as_value_error(self) -> None:
        """Existing ValueError catch sites still accept IssueNotFoundError."""
        with pytest.raises(ValueError, match="missing"):
            raise IssueNotFoundError("missing")

    def test_raise_and_catch_as_issue_not_found_error(self) -> None:
        """Callers can still catch the more specific not-found subclass."""
        with pytest.raises(IssueNotFoundError, match="missing"):
            raise IssueNotFoundError("missing")
