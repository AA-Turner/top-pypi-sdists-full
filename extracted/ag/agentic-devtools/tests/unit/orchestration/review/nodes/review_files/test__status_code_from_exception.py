"""Tests for _status_code_from_exception."""

from __future__ import annotations

from types import SimpleNamespace

from agentic_devtools.orchestration.review.nodes.review_files import (
    _status_code_from_exception,
)


class TestStatusCodeFromException:
    """Tests for _status_code_from_exception."""

    def test_reads_response_status_code(self) -> None:
        """response.status_code integer is returned directly."""
        exc = RuntimeError("boom")
        exc.response = SimpleNamespace(status_code=403)  # type: ignore[attr-defined]

        assert _status_code_from_exception(exc) == 403

    def test_ignores_non_integer_response_code(self) -> None:
        """Non-integer response status codes are ignored and None is returned."""
        exc = RuntimeError("boom")
        exc.response = SimpleNamespace(status_code="403")  # type: ignore[attr-defined]

        assert _status_code_from_exception(exc) is None

    def test_returns_none_when_no_response_attribute(self) -> None:
        """Exception without a response attribute returns None."""
        assert _status_code_from_exception(ValueError("no response")) is None
