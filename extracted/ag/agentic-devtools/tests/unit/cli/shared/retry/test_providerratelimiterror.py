"""Tests for ProviderRateLimitError class."""

from agentic_devtools.cli.shared.retry import ProviderRateLimitError


class TestProviderRateLimitError:
    """Tests for the ProviderRateLimitError exception."""

    def test_default_message(self) -> None:
        """Default message without retry_after_seconds."""
        err = ProviderRateLimitError()
        assert "rate limit exhausted" in str(err).lower()
        assert err.retry_after_seconds is None

    def test_message_with_retry_after(self) -> None:
        """Message includes retry-after seconds when provided."""
        err = ProviderRateLimitError(retry_after_seconds=30.0)
        assert "30" in str(err)
        assert err.retry_after_seconds == 30.0

    def test_retry_after_zero(self) -> None:
        """retry_after_seconds can be zero."""
        err = ProviderRateLimitError(retry_after_seconds=0.0)
        assert err.retry_after_seconds == 0.0

    def test_is_exception(self) -> None:
        """ProviderRateLimitError is an Exception subclass."""
        assert issubclass(ProviderRateLimitError, Exception)

    def test_preserves_sanitized_provider_metadata(self) -> None:
        """Provider identity and timing metadata survive terminal conversion."""
        err = ProviderRateLimitError(
            reset_timestamp=200,
            remaining=0,
            provider="github",
            credential_identity="COPILOT_GITHUB_TOKEN",
            source="x-ratelimit-reset",
        )
        assert err.metadata.reset_timestamp == 200
        assert err.metadata.remaining == 0
        assert "COPILOT_GITHUB_TOKEN" in str(err)
        assert "secret-token" not in str(err)
