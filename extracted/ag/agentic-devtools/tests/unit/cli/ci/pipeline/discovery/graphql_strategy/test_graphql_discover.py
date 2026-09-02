"""Tests for graphql_discover function."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

from agentic_devtools.cli.ci.pipeline.discovery.graphql_strategy import graphql_discover
from agentic_devtools.cli.ci.pipeline.discovery.models import DiscoveryOutcome
from agentic_devtools.cli.ci.pipeline.suggestions import SuggestedChange
from agentic_devtools.cli.shared.retry import ProviderRateLimitError


class TestGraphqlDiscover:
    """Tests for graphql_discover function."""

    def test_returns_suggestions_on_success(self) -> None:
        """Tags discovery_source and returns SUCCESS attempt."""
        provider = MagicMock()
        suggestion = SuggestedChange(
            suggestion_id="SC1",
            outdated=False,
            comment_database_id=1,
            thread_id="T1",
            path="file.py",
            start_line=1,
            end_line=2,
            replacement="new_code()",
        )

        with patch(
            "agentic_devtools.cli.ci.pipeline.discovery.graphql_strategy.fetch_applicable_suggestions"
        ) as mock_fetch:
            mock_fetch.return_value = ([suggestion], "PR_NODE_123")
            suggestions, attempt, pr_node_id = graphql_discover(provider, 42)

        assert len(suggestions) == 1
        assert suggestions[0].discovery_source == "graphql"
        assert attempt.outcome == DiscoveryOutcome.SUCCESS
        assert attempt.method == "graphql"
        assert attempt.suggestion_count == 1
        assert pr_node_id == "PR_NODE_123"

    def test_returns_empty_attempt_when_no_suggestions(self) -> None:
        """Returns EMPTY outcome when fetch returns no suggestions."""
        provider = MagicMock()

        with patch(
            "agentic_devtools.cli.ci.pipeline.discovery.graphql_strategy.fetch_applicable_suggestions"
        ) as mock_fetch:
            mock_fetch.return_value = ([], "PR_NODE_456")
            suggestions, attempt, pr_node_id = graphql_discover(provider, 42)

        assert suggestions == []
        assert attempt.outcome == DiscoveryOutcome.EMPTY
        assert attempt.method == "graphql"
        assert pr_node_id == "PR_NODE_456"

    def test_returns_error_attempt_on_exception(self) -> None:
        """Returns ERROR outcome when fetch raises an exception."""
        provider = MagicMock()

        with patch(
            "agentic_devtools.cli.ci.pipeline.discovery.graphql_strategy.fetch_applicable_suggestions"
        ) as mock_fetch:
            mock_fetch.side_effect = RuntimeError("GraphQL timeout")
            suggestions, attempt, pr_node_id = graphql_discover(provider, 42)

        assert suggestions == []
        assert attempt.outcome == DiscoveryOutcome.ERROR
        assert attempt.method == "graphql"
        assert "GraphQL timeout" in attempt.error_message
        assert pr_node_id == ""

    def test_propagates_rate_limit_error(self) -> None:
        """Rate-limit errors escape discovery so the caller can persist cooldown state."""
        provider = MagicMock()
        error = ProviderRateLimitError(provider="github")

        with patch(
            "agentic_devtools.cli.ci.pipeline.discovery.graphql_strategy.fetch_applicable_suggestions",
            side_effect=error,
        ):
            try:
                graphql_discover(provider, 42)
            except ProviderRateLimitError as raised:
                assert raised is error
            else:
                raise AssertionError("ProviderRateLimitError should be propagated")

    def test_duration_ms_is_non_negative(self) -> None:
        """Duration is captured regardless of outcome."""
        provider = MagicMock()

        with patch(
            "agentic_devtools.cli.ci.pipeline.discovery.graphql_strategy.fetch_applicable_suggestions"
        ) as mock_fetch:
            mock_fetch.return_value = ([], "")
            _suggestions, attempt, _pr_node_id = graphql_discover(provider, 1)

        assert attempt.duration_ms >= 0
