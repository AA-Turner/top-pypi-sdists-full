"""Tests for _is_provider_wide_failure."""

from __future__ import annotations

from types import SimpleNamespace

from agentic_devtools.orchestration.review.nodes.review_files import (
    _is_provider_wide_failure,
)


class TestIsProviderWideFailure:
    """Tests for _is_provider_wide_failure."""

    def test_is_provider_wide_failure_for_authentication_error(self) -> None:
        """AuthenticationError is treated as provider-wide."""
        from agentic_devtools.orchestration.llm.errors import AuthenticationError

        assert _is_provider_wide_failure(AuthenticationError("bad key"))

    def test_is_provider_wide_failure_for_unavailable_model(self) -> None:
        """Unavailable model errors are provider-wide."""
        from agentic_devtools.orchestration.llm.errors import ModelNotAvailableError

        assert _is_provider_wide_failure(ModelNotAvailableError())

    def test_is_provider_wide_failure_for_http_403_response(self) -> None:
        """Exception with response.status_code=403 is treated as provider-wide."""
        exc = RuntimeError("boom")
        exc.response = SimpleNamespace(status_code=403)  # type: ignore[attr-defined]

        assert _is_provider_wide_failure(exc)

    def test_is_provider_wide_failure_for_http_404_status_code(self) -> None:
        """Exception with status_code=404 (model-not-found, deployment-not-found) is provider-wide."""
        exc = RuntimeError("model not found")
        exc.status_code = 404  # type: ignore[attr-defined]

        assert _is_provider_wide_failure(exc)

    def test_is_provider_wide_failure_for_http_404_response(self) -> None:
        """Exception with response.status_code=404 is treated as provider-wide."""
        exc = RuntimeError("deployment not found")
        exc.response = SimpleNamespace(status_code=404)  # type: ignore[attr-defined]

        assert _is_provider_wide_failure(exc)

    def test_is_provider_wide_failure_for_retry_exhausted_error(self) -> None:
        """RetryExhaustedError remains file-scoped, not provider-wide."""
        from agentic_devtools.orchestration.llm.errors import RetryExhaustedError

        assert not _is_provider_wide_failure(RetryExhaustedError(attempts=3))

    def test_is_provider_wide_failure_for_rate_limit_exhausted_error(self) -> None:
        """RateLimitExhaustedError remains file-scoped, not provider-wide."""
        from agentic_devtools.orchestration.llm.errors import RateLimitExhaustedError

        assert not _is_provider_wide_failure(RateLimitExhaustedError(attempts=3))

    def test_is_provider_wide_failure_for_transient_llm_error(self) -> None:
        """TransientLLMError escaping inner retries remains file-scoped."""
        from agentic_devtools.orchestration.review.llm_error_normalizer import TransientLLMError

        assert not _is_provider_wide_failure(TransientLLMError("rate limit", status_code=429))

    def test_is_provider_wide_failure_chained_retry_exhausted_error(self) -> None:
        """Chained RetryExhaustedError remains file-scoped."""
        from agentic_devtools.orchestration.llm.errors import RetryExhaustedError

        outer = ValueError("wrapper")
        outer.__cause__ = RetryExhaustedError(attempts=3)  # type: ignore[assignment]
        assert not _is_provider_wide_failure(outer)

    def test_is_provider_wide_failure_chained_authentication_error(self) -> None:
        """AuthenticationError chained as __cause__ is detected as provider-wide."""
        from agentic_devtools.orchestration.llm.errors import AuthenticationError

        outer = ValueError("wrapper")
        outer.__cause__ = AuthenticationError("bad key")  # type: ignore[assignment]
        assert _is_provider_wide_failure(outer)

    def test_is_provider_wide_failure_returns_false_for_value_error(self) -> None:
        """A plain ValueError (e.g. parse failure) is not treated as provider-wide."""
        assert not _is_provider_wide_failure(ValueError("bad json"))
