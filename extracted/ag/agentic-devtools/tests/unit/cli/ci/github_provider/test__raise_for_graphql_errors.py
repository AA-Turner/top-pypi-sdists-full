"""Tests for _raise_for_graphql_errors."""

import pytest

from agentic_devtools.cli.ci.github_provider import _raise_for_graphql_errors


class TestRaiseForGraphqlErrors:
    """Tests for GraphQL error payload handling."""

    def test_ignores_non_dict_payload(self) -> None:
        _raise_for_graphql_errors([], context="GraphQL context")

    def test_ignores_missing_or_empty_errors(self) -> None:
        _raise_for_graphql_errors({}, context="GraphQL context")
        _raise_for_graphql_errors({"errors": []}, context="GraphQL context")

    def test_raises_generic_message_when_errors_have_no_dicts(self) -> None:
        with pytest.raises(RuntimeError, match="Unknown GraphQL error"):
            _raise_for_graphql_errors({"errors": ["bad-shape"]}, context="GraphQL context")

    def test_raises_using_dict_messages_when_errors_mix_dicts_and_other_values(self) -> None:
        with pytest.raises(RuntimeError, match="real error"):
            _raise_for_graphql_errors(
                {"errors": [{"message": "real error"}, "bad-shape"]},
                context="GraphQL context",
            )

    def test_raises_retryable_error_when_error_type_is_rate_limited(self) -> None:
        from agentic_devtools.cli.ci.retry import RetryableError

        with pytest.raises(RetryableError, match="API rate limit exceeded") as exc_info:
            _raise_for_graphql_errors(
                {"errors": [{"type": "RATE_LIMITED", "message": "API rate limit exceeded"}]},
                context="GraphQL context",
            )
        assert exc_info.value.is_rate_limit is True

    def test_rate_limited_type_carries_provider_and_credential_identity(self) -> None:
        from agentic_devtools.cli.ci.retry import RetryableError

        with pytest.raises(RetryableError) as exc_info:
            _raise_for_graphql_errors(
                {"errors": [{"type": "RATE_LIMITED", "message": "API rate limit exceeded"}]},
                context="GraphQL context",
                provider="github",
                credential_identity="COPILOT_GITHUB_TOKEN",
            )
        err = exc_info.value
        assert err.is_rate_limit is True
        assert err.provider == "github"
        assert err.credential_identity == "COPILOT_GITHUB_TOKEN"
        assert err.source == "graphql-rate-limited"

    def test_rate_limited_selects_retry_after_source_when_retry_after_is_set(self) -> None:
        from agentic_devtools.cli.ci.retry import RetryableError

        with pytest.raises(RetryableError) as exc_info:
            _raise_for_graphql_errors(
                {"errors": [{"type": "RATE_LIMITED", "message": "API rate limit exceeded"}]},
                context="GraphQL context",
                retry_after=60.0,
                reset_timestamp=None,
            )
        err = exc_info.value
        assert err.is_rate_limit is True
        assert err.source == "retry-after"

    def test_rate_limited_selects_reset_timestamp_source_when_only_reset_timestamp_is_set(self) -> None:
        from agentic_devtools.cli.ci.retry import RetryableError

        with pytest.raises(RetryableError) as exc_info:
            _raise_for_graphql_errors(
                {"errors": [{"type": "RATE_LIMITED", "message": "API rate limit exceeded"}]},
                context="GraphQL context",
                retry_after=None,
                reset_timestamp=1787664000.0,
            )
        err = exc_info.value
        assert err.is_rate_limit is True
        assert err.source == "x-ratelimit-reset"

    def test_raises_retryable_error_when_message_contains_rate_limit(self) -> None:
        from agentic_devtools.cli.ci.retry import RetryableError

        with pytest.raises(RetryableError, match="rate limit") as exc_info:
            _raise_for_graphql_errors(
                {"errors": [{"message": "rate limit exceeded, please wait"}]},
                context="GraphQL context",
            )
        assert exc_info.value.is_rate_limit is True

    def test_raises_retryable_error_when_message_contains_internal_server_error(self) -> None:
        from agentic_devtools.cli.ci.retry import RetryableError

        with pytest.raises(RetryableError, match="internal server error") as exc_info:
            _raise_for_graphql_errors(
                {"errors": [{"message": "internal server error occurred"}]},
                context="GraphQL context",
            )
        assert exc_info.value.is_rate_limit is False

    def test_raises_retryable_error_when_message_contains_temporarily_unavailable(self) -> None:
        from agentic_devtools.cli.ci.retry import RetryableError

        with pytest.raises(RetryableError, match="temporarily unavailable") as exc_info:
            _raise_for_graphql_errors(
                {"errors": [{"message": "service temporarily unavailable"}]},
                context="GraphQL context",
            )
        assert exc_info.value.is_rate_limit is False

    def test_does_not_classify_domain_error_with_embedded_status_code_as_transient(self) -> None:
        """A bare status code in a domain message must not trigger transient retry.

        A message such as "Could not resolve to an Issue with the number of 503"
        contains '503' but refers to an entity lookup failure, not a server error.
        """
        with pytest.raises(RuntimeError, match="503"):
            _raise_for_graphql_errors(
                {"errors": [{"message": "Could not resolve to an Issue with the number of 503"}]},
                context="GraphQL context",
            )

    def test_raises_runtime_error_for_non_transient_graphql_error(self) -> None:
        with pytest.raises(RuntimeError, match="field not found"):
            _raise_for_graphql_errors(
                {"errors": [{"message": "field not found"}]},
                context="GraphQL context",
            )

    def test_raises_runtime_error_for_untyped_message_and_type_values(self) -> None:
        """Non-string ``message``/``type`` values must not raise TypeError/AttributeError."""
        with pytest.raises(RuntimeError, match="503"):
            _raise_for_graphql_errors(
                {"errors": [{"message": None, "type": 7}, {"message": 503}]},
                context="GraphQL context",
            )
