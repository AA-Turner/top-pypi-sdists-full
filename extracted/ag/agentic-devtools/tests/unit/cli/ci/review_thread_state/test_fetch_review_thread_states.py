"""Tests for fetch_review_thread_states()."""

from unittest.mock import MagicMock

from agentic_devtools.cli.ci.review_thread_state import fetch_review_thread_states


class TestFetchReviewThreadStates:
    """Tests for capability-aware review-thread-state fetching."""

    def test_returns_provider_states_when_supported(self) -> None:
        """A supported provider yields its mapping with degraded=False."""
        provider = MagicMock()
        provider.list_review_thread_states.return_value = {10: (True, True), 11: (False, False)}

        result = fetch_review_thread_states(provider, 42)

        assert result.states == {10: (True, True), 11: (False, False)}
        assert result.degraded is False
        assert result.reason == ""
        provider.list_review_thread_states.assert_called_once_with(42)

    def test_empty_mapping_from_supported_provider_is_not_degraded(self) -> None:
        """An empty mapping from a supporting provider is a real answer, not degraded."""
        provider = MagicMock()
        provider.list_review_thread_states.return_value = {}

        result = fetch_review_thread_states(provider, 42)

        assert result.states == {}
        assert result.degraded is False

    def test_degraded_when_provider_lacks_attribute(self) -> None:
        """A provider without the method degrades instead of reporting no threads."""
        provider = MagicMock()
        del provider.list_review_thread_states

        result = fetch_review_thread_states(provider, 42)

        assert result.states == {}
        assert result.degraded is True
        assert "does not expose" in result.reason

    def test_degraded_when_attribute_is_not_callable(self) -> None:
        """A non-callable attribute is treated as a missing capability."""
        provider = MagicMock()
        provider.list_review_thread_states = None

        result = fetch_review_thread_states(provider, 42)

        assert result.states == {}
        assert result.degraded is True

    def test_degraded_when_provider_raises_not_implemented(self) -> None:
        """The base-class default raise is reported as a missing implementation."""
        provider = MagicMock()
        provider.list_review_thread_states.side_effect = NotImplementedError(
            "AzureDevOpsProvider does not implement list_review_thread_states"
        )

        result = fetch_review_thread_states(provider, 42)

        assert result.states == {}
        assert result.degraded is True
        assert "does not implement" in result.reason

    def test_degraded_when_lookup_raises(self) -> None:
        """A failed lookup degrades and records the truncated failure detail."""
        provider = MagicMock()
        provider.list_review_thread_states.side_effect = RuntimeError("HTTP 502 bad gateway")

        result = fetch_review_thread_states(provider, 42)

        assert result.states == {}
        assert result.degraded is True
        assert "HTTP 502 bad gateway" in result.reason

    def test_degraded_reason_is_truncated(self) -> None:
        """Long provider errors are truncated so the reason stays summary-sized."""
        provider = MagicMock()
        provider.list_review_thread_states.side_effect = RuntimeError("x" * 500)

        result = fetch_review_thread_states(provider, 42)

        assert result.degraded is True
        assert result.reason.count("x") == 200

    def test_degraded_when_provider_returns_non_mapping(self) -> None:
        """A non-mapping return value cannot be trusted and degrades."""
        provider = MagicMock()
        provider.list_review_thread_states.return_value = [(10, True)]

        result = fetch_review_thread_states(provider, 42)

        assert result.states == {}
        assert result.degraded is True
        assert "expected a mapping" in result.reason

    def test_degraded_when_mapping_has_non_int_key(self) -> None:
        """A mapping keyed by a non-int comment id degrades instead of returning data."""
        provider = MagicMock()
        provider.list_review_thread_states.return_value = {"10": (True, False)}

        result = fetch_review_thread_states(provider, 42)

        assert result.states == {}
        assert result.degraded is True
        assert "invalid state mapping" in result.reason

    def test_degraded_when_mapping_value_is_not_a_tuple(self) -> None:
        """A mapping whose value is not a tuple degrades instead of returning data."""
        provider = MagicMock()
        provider.list_review_thread_states.return_value = {10: [True, False]}

        result = fetch_review_thread_states(provider, 42)

        assert result.states == {}
        assert result.degraded is True
        assert "invalid state mapping" in result.reason

    def test_degraded_when_mapping_tuple_has_wrong_length(self) -> None:
        """A mapping whose tuple has a length other than 2 degrades."""
        provider = MagicMock()
        provider.list_review_thread_states.return_value = {10: (True,)}

        result = fetch_review_thread_states(provider, 42)

        assert result.states == {}
        assert result.degraded is True
        assert "invalid state mapping" in result.reason

    def test_degraded_when_flag_is_not_bool(self) -> None:
        """A mapping with a non-bool flag value (e.g. 1 or 'yes') degrades."""
        provider = MagicMock()
        provider.list_review_thread_states.return_value = {10: (1, False)}

        result = fetch_review_thread_states(provider, 42)

        assert result.states == {}
        assert result.degraded is True
        assert "invalid state mapping" in result.reason
