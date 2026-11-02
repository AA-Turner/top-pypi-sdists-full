"""Tests for RetryableError class."""

from agentic_devtools.cli.shared.retry import RetryableError


class TestRetryableError:
    """Tests for the RetryableError exception."""

    def test_default_message_empty(self) -> None:
        """Default message is empty string."""
        err = RetryableError()
        assert str(err) == ""

    def test_custom_message(self) -> None:
        """Custom message is preserved."""
        err = RetryableError("transient failure")
        assert str(err) == "transient failure"

    def test_retry_after_none_by_default(self) -> None:
        """retry_after defaults to None."""
        err = RetryableError("fail")
        assert err.retry_after is None

    def test_retry_after_set(self) -> None:
        """retry_after attribute is set when provided."""
        err = RetryableError("fail", retry_after=5.0)
        assert err.retry_after == 5.0

    def test_retry_after_zero(self) -> None:
        """retry_after can be zero."""
        err = RetryableError("fail", retry_after=0.0)
        assert err.retry_after == 0.0

    def test_is_exception(self) -> None:
        """RetryableError is an Exception subclass."""
        assert issubclass(RetryableError, Exception)

    def test_metadata_preserves_rate_limit_fields(self) -> None:
        err = RetryableError(
            "limited",
            retry_after=5,
            reset_timestamp=100,
            remaining=0,
            provider="github",
            credential_identity="GH_TOKEN",
            source="retry-after",
        )
        assert err.metadata.provider == "github"
        assert err.metadata.credential_identity == "GH_TOKEN"
        assert err.metadata.remaining == 0
