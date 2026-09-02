"""Tests for _extract_http_status_code."""

from __future__ import annotations

from types import SimpleNamespace

from agentic_devtools.orchestration.nodes._issue_retrieval import _extract_http_status_code


class TestExtractHttpStatusCode:
    """Tests for HTTP status extraction from provider exceptions."""

    def test_direct_status_code_attribute_is_used(self) -> None:
        """An integer ``status_code`` attribute on the exception is returned directly."""
        exc = RuntimeError("boom")
        setattr(exc, "status_code", 404)

        assert _extract_http_status_code(exc) == 404

    def test_non_integer_status_code_attribute_falls_through(self) -> None:
        """A non-integer ``status_code`` attribute is ignored in favour of the response."""
        exc = RuntimeError("boom")
        setattr(exc, "status_code", "404")
        setattr(exc, "response", SimpleNamespace(status_code=401))

        assert _extract_http_status_code(exc) == 401

    def test_response_status_code_is_used(self) -> None:
        """The response object's integer ``status_code`` is returned when present."""
        exc = RuntimeError("boom")
        setattr(exc, "response", SimpleNamespace(status_code=403))

        assert _extract_http_status_code(exc) == 403

    def test_message_http_pattern_is_parsed(self) -> None:
        """A ``HTTP <code>`` message fragment is parsed when no attributes exist."""
        assert _extract_http_status_code(RuntimeError("HTTP 404 for PROJ-401")) == 404

    def test_message_status_pattern_is_parsed(self) -> None:
        """A ``status code: <code>`` message fragment is parsed when no attributes exist."""
        assert _extract_http_status_code(RuntimeError("status code: 401")) == 401

    def test_bare_digits_in_issue_key_are_not_matched(self) -> None:
        """Digits inside an issue key or URL do not produce a false status match."""
        assert _extract_http_status_code(RuntimeError("failed for PROJ-404")) is None
