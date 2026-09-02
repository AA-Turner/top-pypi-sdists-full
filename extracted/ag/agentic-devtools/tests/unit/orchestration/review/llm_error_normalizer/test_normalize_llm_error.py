"""Tests for normalize_llm_error() context manager."""

from __future__ import annotations

import pytest

from agentic_devtools.orchestration.review.llm_error_normalizer import (
    TransientLLMError,
    _extract_status_code,
    _is_transient,
    normalize_llm_error,
)


class TestNormalizeLlmError:
    """Tests for the LLM error normalizer."""

    def test_no_error_passes_through(self) -> None:
        """No exception means the context manager does nothing."""
        with normalize_llm_error():
            result = 42
        assert result == 42

    def test_transient_429_becomes_transient_llm_error(self) -> None:
        """HTTP 429 exception is re-raised as TransientLLMError."""

        class FakeRateLimitError(Exception):
            status_code = 429

        with pytest.raises(TransientLLMError) as exc_info:
            with normalize_llm_error():
                raise FakeRateLimitError("rate limited")

        assert exc_info.value.status_code == 429

    def test_transient_502_becomes_transient_llm_error(self) -> None:
        """HTTP 502 exception is re-raised as TransientLLMError."""

        class FakeServerError(Exception):
            status_code = 502

        with pytest.raises(TransientLLMError):
            with normalize_llm_error():
                raise FakeServerError("bad gateway")

    def test_transient_503_becomes_transient_llm_error(self) -> None:
        """HTTP 503 exception is re-raised as TransientLLMError."""

        class FakeServiceUnavailable(Exception):
            status_code = 503

        with pytest.raises(TransientLLMError):
            with normalize_llm_error():
                raise FakeServiceUnavailable("unavailable")

    def test_non_transient_400_passes_through(self) -> None:
        """HTTP 400 exception passes through unchanged."""

        class FakeBadRequest(Exception):
            status_code = 400

        with pytest.raises(FakeBadRequest):
            with normalize_llm_error():
                raise FakeBadRequest("bad request")

    def test_non_transient_401_passes_through(self) -> None:
        """HTTP 401 exception passes through unchanged."""

        class FakeUnauthorized(Exception):
            status_code = 401

        with pytest.raises(FakeUnauthorized):
            with normalize_llm_error():
                raise FakeUnauthorized("unauthorized")

    def test_already_normalized_passes_through(self) -> None:
        """TransientLLMError is re-raised without double-wrapping."""
        with pytest.raises(TransientLLMError) as exc_info:
            with normalize_llm_error():
                raise TransientLLMError("already transient", status_code=429)

        assert exc_info.value.status_code == 429

    def test_rate_limit_error_by_class_name(self) -> None:
        """RateLimitError class name triggers transient detection."""

        class RateLimitError(Exception):
            pass

        with pytest.raises(TransientLLMError):
            with normalize_llm_error():
                raise RateLimitError("too many requests")

    def test_api_connection_error_by_class_name(self) -> None:
        """APIConnectionError class name is also treated as transient."""

        class APIConnectionError(Exception):
            pass

        with pytest.raises(TransientLLMError):
            with normalize_llm_error():
                raise APIConnectionError("socket reset")

    def test_generic_exception_passes_through(self) -> None:
        """Generic ValueError passes through unchanged."""
        with pytest.raises(ValueError):
            with normalize_llm_error():
                raise ValueError("not an HTTP error")


class TestExtractStatusCode:
    """Tests for _extract_status_code helper."""

    def test_direct_status_code_attribute(self) -> None:
        """Extracts status_code from direct attribute."""

        class Exc(Exception):
            status_code = 503

        assert _extract_status_code(Exc()) == 503

    def test_response_attribute(self) -> None:
        """Extracts status_code from response attribute."""

        class Response:
            status_code = 429

        class Exc(Exception):
            response = Response()

        assert _extract_status_code(Exc()) == 429

    def test_response_attribute_with_non_integer_status_returns_none(self) -> None:
        """Non-integer response status codes are ignored."""

        class Response:
            status_code = "429"

        class Exc(Exception):
            response = Response()

        assert _extract_status_code(Exc()) is None

    def test_no_status_code(self) -> None:
        """Returns None when no status code is available."""
        assert _extract_status_code(ValueError("test")) is None


class TestIsTransient:
    """Tests for _is_transient helper."""

    def test_429_is_transient(self) -> None:
        """HTTP 429 is transient."""

        class Exc(Exception):
            status_code = 429

        assert _is_transient(Exc()) is True

    def test_400_is_not_transient(self) -> None:
        """HTTP 400 is not transient."""

        class Exc(Exception):
            status_code = 400

        assert _is_transient(Exc()) is False

    def test_internal_server_error_class_name(self) -> None:
        """InternalServerError class name is transient."""

        class InternalServerError(Exception):
            pass

        assert _is_transient(InternalServerError()) is True
