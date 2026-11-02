"""Tests for ADCP exception hierarchy."""

from __future__ import annotations

from adcp.exceptions import (
    ADCPAuthenticationError,
    ADCPConnectionError,
    ADCPError,
    ADCPSimpleAPIError,
    ADCPTaskError,
    ADCPTimeoutError,
)


class TestIsRetryable:
    """Tests for is_retryable property."""

    def test_base_error_not_retryable(self) -> None:
        assert ADCPError("fail").is_retryable is False

    def test_connection_error_retryable(self) -> None:
        assert ADCPConnectionError("fail").is_retryable is True

    def test_timeout_error_retryable(self) -> None:
        assert ADCPTimeoutError("fail").is_retryable is True

    def test_auth_error_not_retryable(self) -> None:
        assert ADCPAuthenticationError("fail").is_retryable is False


class TestADCPTaskError:
    """Tests for ADCPTaskError."""

    def test_basic_task_error(self) -> None:
        class FakeError:
            code = "INVALID_BUDGET"
            message = "Budget too low"

        err = ADCPTaskError("create_media_buy", [FakeError()])
        assert err.operation == "create_media_buy"
        assert len(err.errors) == 1
        assert err.error_codes == ["INVALID_BUDGET"]
        assert "Budget too low" in str(err)

    def test_multiple_errors(self) -> None:
        class Err1:
            code = "INVALID_BUDGET"
            message = "Budget too low"

        class Err2:
            code = "MISSING_CREATIVE"
            message = "No creatives"

        err = ADCPTaskError("create_media_buy", [Err1(), Err2()])
        assert err.error_codes == ["INVALID_BUDGET", "MISSING_CREATIVE"]
        assert "+1 more" in str(err)

    def test_empty_errors(self) -> None:
        err = ADCPTaskError("get_products", [])
        assert err.error_codes == []
        assert "get_products failed" in str(err)

    def test_errors_without_code(self) -> None:
        class NoCode:
            message = "something went wrong"

        err = ADCPTaskError("get_products", [NoCode()])
        assert err.error_codes == []

    def test_importable_from_top_level(self) -> None:
        from adcp import ADCPTaskError

        assert ADCPTaskError is not None

    def test_retryable_with_transient_code(self) -> None:
        class RateLimited:
            code = "RATE_LIMITED"
            message = "Too many requests"

        err = ADCPTaskError("get_products", [RateLimited()])
        assert err.is_retryable is True

    def test_not_retryable_with_terminal_code(self) -> None:
        class NotFound:
            code = "ACCOUNT_NOT_FOUND"
            message = "Not found"

        err = ADCPTaskError("get_products", [NotFound()])
        assert err.is_retryable is False


class TestADCPSimpleAPIError:
    """Tests for ADCPSimpleAPIError preserving errors."""

    def test_preserves_errors(self) -> None:
        errors = [{"code": "ERR1", "message": "fail"}]
        err = ADCPSimpleAPIError("get_products", "fail", errors=errors)
        assert err.errors == errors
        assert err.operation == "get_products"

    def test_defaults_to_empty_errors(self) -> None:
        err = ADCPSimpleAPIError("get_products", "fail")
        assert err.errors == []


class TestSuggestionFormat:
    """Test that suggestions use plain text, not emoji."""

    def test_no_emoji_in_suggestion(self) -> None:
        err = ADCPError("fail", suggestion="try this")
        assert "\U0001f4a1" not in str(err)  # no lightbulb emoji
        assert "Suggestion:" in str(err)
