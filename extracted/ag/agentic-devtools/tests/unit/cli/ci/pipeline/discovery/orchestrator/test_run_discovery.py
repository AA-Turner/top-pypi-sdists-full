"""Tests for run_discovery orchestrator."""

from __future__ import annotations

import os
from unittest.mock import MagicMock, patch

from agentic_devtools.cli.ci.pipeline.discovery.models import (
    DiscoveryAttempt,
    DiscoveryOutcome,
)
from agentic_devtools.cli.ci.pipeline.discovery.orchestrator import run_discovery
from agentic_devtools.cli.ci.pipeline.snapshot import PRStateSnapshot
from agentic_devtools.cli.ci.pipeline.suggestions import SuggestedChange


class TestRunDiscovery:
    """Tests for the run_discovery orchestrator function."""

    def test_returns_graphql_results_when_found(self) -> None:
        """GraphQL strategy result short-circuits subsequent strategies."""
        snapshot = PRStateSnapshot(
            pr_number=1,
            review_state="CHANGES_REQUESTED",
            copilot_review_id=100,
            copilot_review_inline_count=1,
        )
        provider = MagicMock()
        suggestion = SuggestedChange(
            suggestion_id="SC1",
            outdated=False,
            comment_database_id=101,
            thread_id="T1",
        )
        graphql_attempt = DiscoveryAttempt(method="graphql", outcome=DiscoveryOutcome.SUCCESS, suggestion_count=1)

        with (
            patch("agentic_devtools.cli.ci.pipeline.discovery.orchestrator.graphql_discover") as mock_graphql,
            patch("agentic_devtools.cli.ci.pipeline.discovery.orchestrator.rest_discover") as mock_rest,
            patch("agentic_devtools.cli.ci.pipeline.discovery.orchestrator.html_discover") as mock_html,
        ):
            mock_graphql.return_value = ([suggestion], graphql_attempt, "PR_NODE_1")
            suggestions, attempts, pr_node_id = run_discovery(provider, snapshot, repo="owner/repo")

        assert len(suggestions) == 1
        assert suggestions[0].suggestion_id == "SC1"
        assert pr_node_id == "PR_NODE_1"
        assert len(attempts) == 1
        assert attempts[0].method == "graphql"
        mock_rest.assert_not_called()
        mock_html.assert_not_called()

    def test_falls_through_to_rest_when_graphql_empty(self) -> None:
        """REST strategy is tried when GraphQL returns empty."""
        snapshot = PRStateSnapshot(
            pr_number=1,
            review_state="CHANGES_REQUESTED",
            copilot_review_id=100,
            copilot_review_inline_count=1,
        )
        provider = MagicMock()
        suggestion = SuggestedChange(
            suggestion_id="SC2",
            outdated=False,
            comment_database_id=201,
            thread_id="T2",
            discovery_source="rest",
        )
        graphql_attempt = DiscoveryAttempt(method="graphql", outcome=DiscoveryOutcome.EMPTY, suggestion_count=0)
        rest_attempt = DiscoveryAttempt(method="rest", outcome=DiscoveryOutcome.SUCCESS, suggestion_count=1)

        with (
            patch("agentic_devtools.cli.ci.pipeline.discovery.orchestrator.graphql_discover") as mock_graphql,
            patch("agentic_devtools.cli.ci.pipeline.discovery.orchestrator.rest_discover") as mock_rest,
            patch("agentic_devtools.cli.ci.pipeline.discovery.orchestrator.html_discover") as mock_html,
        ):
            mock_graphql.return_value = ([], graphql_attempt, "")
            mock_rest.return_value = ([suggestion], rest_attempt)
            suggestions, attempts, pr_node_id = run_discovery(provider, snapshot, repo="owner/repo")

        assert len(suggestions) == 1
        assert suggestions[0].discovery_source == "rest"
        assert len(attempts) == 2
        mock_html.assert_not_called()

    def test_falls_through_to_html_when_rest_empty(self) -> None:
        """HTML strategy is tried when both GraphQL and REST return empty."""
        snapshot = PRStateSnapshot(
            pr_number=1,
            review_state="CHANGES_REQUESTED",
            copilot_review_id=100,
            copilot_review_inline_count=1,
        )
        provider = MagicMock()
        suggestion = SuggestedChange(
            suggestion_id="SC3",
            outdated=False,
            comment_database_id=301,
            thread_id="T3",
            discovery_source="html",
        )
        graphql_attempt = DiscoveryAttempt(method="graphql", outcome=DiscoveryOutcome.EMPTY, suggestion_count=0)
        rest_attempt = DiscoveryAttempt(method="rest", outcome=DiscoveryOutcome.EMPTY, suggestion_count=0)
        html_attempt = DiscoveryAttempt(method="html", outcome=DiscoveryOutcome.SUCCESS, suggestion_count=1)

        with (
            patch("agentic_devtools.cli.ci.pipeline.discovery.orchestrator.graphql_discover") as mock_graphql,
            patch("agentic_devtools.cli.ci.pipeline.discovery.orchestrator.rest_discover") as mock_rest,
            patch("agentic_devtools.cli.ci.pipeline.discovery.orchestrator.html_discover") as mock_html,
        ):
            mock_graphql.return_value = ([], graphql_attempt, "")
            mock_rest.return_value = ([], rest_attempt)
            mock_html.return_value = ([suggestion], html_attempt)
            suggestions, attempts, pr_node_id = run_discovery(provider, snapshot, repo="owner/repo")

        assert len(suggestions) == 1
        assert suggestions[0].discovery_source == "html"
        assert len(attempts) == 3

    def test_all_empty_returns_empty_with_all_attempts(self) -> None:
        """Returns empty when all strategies fail (no retry - no recent review)."""
        snapshot = PRStateSnapshot(
            pr_number=1,
            review_state="CHANGES_REQUESTED",
            copilot_review_id=100,
            copilot_review_inline_count=0,
        )
        provider = MagicMock()
        graphql_attempt = DiscoveryAttempt(method="graphql", outcome=DiscoveryOutcome.EMPTY, suggestion_count=0)
        rest_attempt = DiscoveryAttempt(method="rest", outcome=DiscoveryOutcome.EMPTY, suggestion_count=0)
        html_attempt = DiscoveryAttempt(method="html", outcome=DiscoveryOutcome.EMPTY, suggestion_count=0)

        with (
            patch("agentic_devtools.cli.ci.pipeline.discovery.orchestrator.graphql_discover") as mock_graphql,
            patch("agentic_devtools.cli.ci.pipeline.discovery.orchestrator.rest_discover") as mock_rest,
            patch("agentic_devtools.cli.ci.pipeline.discovery.orchestrator.html_discover") as mock_html,
        ):
            mock_graphql.return_value = ([], graphql_attempt, "")
            mock_rest.return_value = ([], rest_attempt)
            mock_html.return_value = ([], html_attempt)
            suggestions, attempts, pr_node_id = run_discovery(provider, snapshot)

        assert suggestions == []
        assert len(attempts) == 3
        assert pr_node_id == ""

    def test_skips_rest_when_no_copilot_review_id(self) -> None:
        """REST strategy skipped when no copilot_review_id."""
        snapshot = PRStateSnapshot(
            pr_number=1,
            review_state="CHANGES_REQUESTED",
            copilot_review_id=0,
            copilot_review_inline_count=0,
        )
        provider = MagicMock()
        graphql_attempt = DiscoveryAttempt(method="graphql", outcome=DiscoveryOutcome.EMPTY, suggestion_count=0)
        html_attempt = DiscoveryAttempt(method="html", outcome=DiscoveryOutcome.EMPTY, suggestion_count=0)

        with (
            patch("agentic_devtools.cli.ci.pipeline.discovery.orchestrator.graphql_discover") as mock_graphql,
            patch("agentic_devtools.cli.ci.pipeline.discovery.orchestrator.rest_discover") as mock_rest,
            patch("agentic_devtools.cli.ci.pipeline.discovery.orchestrator.html_discover") as mock_html,
        ):
            mock_graphql.return_value = ([], graphql_attempt, "")
            mock_html.return_value = ([], html_attempt)
            suggestions, attempts, _node_id = run_discovery(provider, snapshot)

        assert suggestions == []
        mock_rest.assert_not_called()
        mock_html.assert_not_called()
        # Should have 2 attempts: graphql + html
        assert len(attempts) == 2
        assert attempts[1].method == "html-scrape"
        assert attempts[1].outcome is DiscoveryOutcome.EMPTY
        assert attempts[1].details.get("skipped") is True

    def test_graphql_node_id_propagated(self) -> None:
        """PR node ID from GraphQL is propagated even when it returns empty."""
        snapshot = PRStateSnapshot(
            pr_number=1,
            review_state="CHANGES_REQUESTED",
            copilot_review_id=100,
            copilot_review_inline_count=1,
        )
        provider = MagicMock()
        graphql_attempt = DiscoveryAttempt(method="graphql", outcome=DiscoveryOutcome.EMPTY, suggestion_count=0)
        rest_attempt = DiscoveryAttempt(method="rest", outcome=DiscoveryOutcome.EMPTY, suggestion_count=0)
        html_attempt = DiscoveryAttempt(method="html", outcome=DiscoveryOutcome.EMPTY, suggestion_count=0)

        with (
            patch("agentic_devtools.cli.ci.pipeline.discovery.orchestrator.graphql_discover") as mock_graphql,
            patch("agentic_devtools.cli.ci.pipeline.discovery.orchestrator.rest_discover") as mock_rest,
            patch("agentic_devtools.cli.ci.pipeline.discovery.orchestrator.html_discover") as mock_html,
        ):
            mock_graphql.return_value = ([], graphql_attempt, "PR_abc123")
            mock_rest.return_value = ([], rest_attempt)
            mock_html.return_value = ([], html_attempt)
            _suggestions, _attempts, pr_node_id = run_discovery(provider, snapshot, repo="owner/repo")

        assert pr_node_id == "PR_abc123"

    @patch.dict("os.environ", {"APPLY_SUGGESTIONS_RETRY_DELAY_SECONDS": "1"}, clear=False)
    def test_retries_once_when_round_is_all_empty_and_recent_review(self) -> None:
        """Retries only when the full round is inconclusive/empty."""
        snapshot = PRStateSnapshot(
            pr_number=1,
            review_state="CHANGES_REQUESTED",
            copilot_review_id=100,
            copilot_review_inline_count=1,
        )
        provider = MagicMock()
        graphql_attempt = DiscoveryAttempt(method="graphql", outcome=DiscoveryOutcome.EMPTY)
        rest_attempt = DiscoveryAttempt(method="rest", outcome=DiscoveryOutcome.EMPTY)
        html_attempt = DiscoveryAttempt(method="html", outcome=DiscoveryOutcome.EMPTY)

        with (
            patch("agentic_devtools.cli.ci.pipeline.discovery.orchestrator.graphql_discover") as mock_graphql,
            patch("agentic_devtools.cli.ci.pipeline.discovery.orchestrator.rest_discover") as mock_rest,
            patch("agentic_devtools.cli.ci.pipeline.discovery.orchestrator.html_discover") as mock_html,
            patch("agentic_devtools.cli.ci.pipeline.discovery.orchestrator._should_retry", return_value=True),
            patch("agentic_devtools.cli.ci.pipeline.discovery.orchestrator.time.sleep"),
        ):
            mock_graphql.return_value = ([], graphql_attempt, "")
            mock_rest.return_value = ([], rest_attempt)
            mock_html.return_value = ([], html_attempt)

            suggestions, attempts, _ = run_discovery(provider, snapshot, repo="owner/repo")

        assert suggestions == []
        assert len(attempts) == 6
        assert mock_graphql.call_count == 2
        assert mock_rest.call_count == 2
        assert mock_html.call_count == 2

    @patch.dict("os.environ", {"APPLY_SUGGESTIONS_RETRY_DELAY_SECONDS": "1"}, clear=False)
    def test_does_not_retry_when_round_contains_error(self) -> None:
        """No retry when any strategy returns non-empty outcome."""
        snapshot = PRStateSnapshot(
            pr_number=1,
            review_state="CHANGES_REQUESTED",
            copilot_review_id=100,
            copilot_review_inline_count=1,
        )
        provider = MagicMock()
        graphql_attempt = DiscoveryAttempt(method="graphql", outcome=DiscoveryOutcome.ERROR, error_message="boom")
        rest_attempt = DiscoveryAttempt(method="rest", outcome=DiscoveryOutcome.EMPTY)
        html_attempt = DiscoveryAttempt(method="html", outcome=DiscoveryOutcome.EMPTY)

        with (
            patch("agentic_devtools.cli.ci.pipeline.discovery.orchestrator.graphql_discover") as mock_graphql,
            patch("agentic_devtools.cli.ci.pipeline.discovery.orchestrator.rest_discover") as mock_rest,
            patch("agentic_devtools.cli.ci.pipeline.discovery.orchestrator.html_discover") as mock_html,
            patch("agentic_devtools.cli.ci.pipeline.discovery.orchestrator._should_retry", return_value=True),
            patch("agentic_devtools.cli.ci.pipeline.discovery.orchestrator.time.sleep") as mock_sleep,
        ):
            mock_graphql.return_value = ([], graphql_attempt, "")
            mock_rest.return_value = ([], rest_attempt)
            mock_html.return_value = ([], html_attempt)

            suggestions, attempts, _ = run_discovery(provider, snapshot, repo="owner/repo")

        assert suggestions == []
        assert len(attempts) == 3
        assert mock_graphql.call_count == 1
        assert mock_rest.call_count == 1
        assert mock_html.call_count == 1
        mock_sleep.assert_not_called()


def _empty_round_patches():
    """Patch graphql/rest/html_discover to all return empty for one round."""
    graphql_attempt = DiscoveryAttempt(method="graphql", outcome=DiscoveryOutcome.EMPTY)
    rest_attempt = DiscoveryAttempt(method="rest", outcome=DiscoveryOutcome.EMPTY)
    html_attempt = DiscoveryAttempt(method="html", outcome=DiscoveryOutcome.EMPTY)
    p_graphql = patch("agentic_devtools.cli.ci.pipeline.discovery.orchestrator.graphql_discover")
    p_rest = patch("agentic_devtools.cli.ci.pipeline.discovery.orchestrator.rest_discover")
    p_html = patch("agentic_devtools.cli.ci.pipeline.discovery.orchestrator.html_discover")
    return p_graphql, p_rest, p_html, graphql_attempt, rest_attempt, html_attempt


class TestRunDiscoveryBrowserTier:
    """Tests for the opt-in 4th (browser) discovery tier in run_discovery."""

    def _snapshot(self) -> PRStateSnapshot:
        return PRStateSnapshot(
            pr_number=1,
            review_state="CHANGES_REQUESTED",
            copilot_review_id=100,
            copilot_review_inline_count=0,
        )

    def test_browser_tier_not_called_when_flag_off(self) -> None:
        """Zero-regression: with the flag off, browser_discover is never called."""
        snapshot = self._snapshot()
        provider = MagicMock()
        p_graphql, p_rest, p_html, g_att, r_att, h_att = _empty_round_patches()
        env = {k: v for k, v in os.environ.items() if k != "ENABLE_BROWSER_APPLY_SUGGESTIONS"}
        with (
            patch.dict("os.environ", env, clear=True),
            p_graphql as mock_graphql,
            p_rest as mock_rest,
            p_html as mock_html,
            patch("agentic_devtools.cli.ci.pipeline.discovery.orchestrator.browser_discover") as mock_browser,
        ):
            mock_graphql.return_value = ([], g_att, "")
            mock_rest.return_value = ([], r_att)
            mock_html.return_value = ([], h_att)
            suggestions, attempts, _ = run_discovery(provider, snapshot, repo="owner/repo")

        assert suggestions == []
        assert len(attempts) == 3
        mock_browser.assert_not_called()

    def test_browser_tier_signals_candidates_when_flag_on(self) -> None:
        """With the flag on and all tiers empty, browser signals candidates via DiscoveryAttempt.

        browser_discover() is a fail-open signal-only tier: it never returns a populated
        suggestions list (always returns []). Candidates are signalled via
        DiscoveryAttempt.outcome == SUCCESS and DiscoveryAttempt.suggestion_count.
        """
        snapshot = self._snapshot()
        provider = MagicMock()
        p_graphql, p_rest, p_html, g_att, r_att, h_att = _empty_round_patches()
        browser_attempt = DiscoveryAttempt(method="browser-apply", outcome=DiscoveryOutcome.SUCCESS, suggestion_count=1)
        with (
            patch.dict("os.environ", {"ENABLE_BROWSER_APPLY_SUGGESTIONS": "true"}),
            p_graphql as mock_graphql,
            p_rest as mock_rest,
            p_html as mock_html,
            patch("agentic_devtools.cli.ci.pipeline.discovery.orchestrator.browser_discover") as mock_browser,
        ):
            mock_graphql.return_value = ([], g_att, "")
            mock_rest.return_value = ([], r_att)
            mock_html.return_value = ([], h_att)
            mock_browser.return_value = ([], browser_attempt)
            suggestions, attempts, _ = run_discovery(provider, snapshot, repo="owner/repo")

        assert suggestions == []
        assert len(attempts) == 4
        assert attempts[3].method == "browser-apply"
        assert attempts[3].outcome == DiscoveryOutcome.SUCCESS
        assert attempts[3].suggestion_count == 1
        mock_browser.assert_called_once_with(provider, 1, "owner/repo")

    def test_browser_tier_empty_falls_through(self) -> None:
        """With the flag on but browser empty, discovery falls through to empty."""
        snapshot = self._snapshot()
        provider = MagicMock()
        p_graphql, p_rest, p_html, g_att, r_att, h_att = _empty_round_patches()
        browser_attempt = DiscoveryAttempt(method="browser-apply", outcome=DiscoveryOutcome.EMPTY)
        with (
            patch.dict("os.environ", {"ENABLE_BROWSER_APPLY_SUGGESTIONS": "true"}),
            p_graphql as mock_graphql,
            p_rest as mock_rest,
            p_html as mock_html,
            patch("agentic_devtools.cli.ci.pipeline.discovery.orchestrator.browser_discover") as mock_browser,
        ):
            mock_graphql.return_value = ([], g_att, "")
            mock_rest.return_value = ([], r_att)
            mock_html.return_value = ([], h_att)
            mock_browser.return_value = ([], browser_attempt)
            suggestions, attempts, _ = run_discovery(provider, snapshot, repo="owner/repo")

        assert suggestions == []
        assert len(attempts) == 4
        mock_browser.assert_called_once_with(provider, 1, "owner/repo")

    @patch.dict("os.environ", {"APPLY_SUGGESTIONS_RETRY_DELAY_SECONDS": "1"}, clear=False)
    def test_browser_error_does_not_block_retry_when_primary_tiers_empty(self) -> None:
        """Retry still happens when browser tier errors after empty primary tiers."""
        snapshot = self._snapshot()
        provider = MagicMock()
        p_graphql, p_rest, p_html, g_att, r_att, h_att = _empty_round_patches()
        browser_attempt = DiscoveryAttempt(
            method="browser-apply",
            outcome=DiscoveryOutcome.ERROR,
            error_message="playwright failed",
        )
        with (
            patch.dict("os.environ", {"ENABLE_BROWSER_APPLY_SUGGESTIONS": "true"}),
            p_graphql as mock_graphql,
            p_rest as mock_rest,
            p_html as mock_html,
            patch("agentic_devtools.cli.ci.pipeline.discovery.orchestrator.browser_discover") as mock_browser,
            patch("agentic_devtools.cli.ci.pipeline.discovery.orchestrator._should_retry", return_value=True),
            patch("agentic_devtools.cli.ci.pipeline.discovery.orchestrator.time.sleep") as mock_sleep,
        ):
            mock_graphql.return_value = ([], g_att, "")
            mock_rest.return_value = ([], r_att)
            mock_html.return_value = ([], h_att)
            mock_browser.return_value = ([], browser_attempt)

            suggestions, attempts, _ = run_discovery(provider, snapshot, repo="owner/repo")

        assert suggestions == []
        assert len(attempts) == 8
        assert mock_graphql.call_count == 2
        assert mock_rest.call_count == 2
        assert mock_html.call_count == 2
        assert mock_browser.call_count == 2
        mock_sleep.assert_called_once_with(1)

    def test_browser_tier_skipped_when_html_signals_success(self) -> None:
        """Browser tier is skipped when HTML signalled candidates (not all empty)."""
        snapshot = self._snapshot()
        provider = MagicMock()
        graphql_attempt = DiscoveryAttempt(method="graphql", outcome=DiscoveryOutcome.EMPTY)
        rest_attempt = DiscoveryAttempt(method="rest", outcome=DiscoveryOutcome.EMPTY)
        html_attempt = DiscoveryAttempt(method="html", outcome=DiscoveryOutcome.SUCCESS, suggestion_count=1)
        with (
            patch.dict("os.environ", {"ENABLE_BROWSER_APPLY_SUGGESTIONS": "true"}),
            patch("agentic_devtools.cli.ci.pipeline.discovery.orchestrator.graphql_discover") as mock_graphql,
            patch("agentic_devtools.cli.ci.pipeline.discovery.orchestrator.rest_discover") as mock_rest,
            patch("agentic_devtools.cli.ci.pipeline.discovery.orchestrator.html_discover") as mock_html,
            patch("agentic_devtools.cli.ci.pipeline.discovery.orchestrator.browser_discover") as mock_browser,
        ):
            mock_graphql.return_value = ([], graphql_attempt, "")
            mock_rest.return_value = ([], rest_attempt)
            mock_html.return_value = ([], html_attempt)
            suggestions, attempts, _ = run_discovery(provider, snapshot, repo="owner/repo")

        assert suggestions == []
        assert len(attempts) == 3
        mock_browser.assert_not_called()

    def test_browser_tier_skipped_when_repo_empty(self) -> None:
        """Browser tier is skipped when no repo is known (even with the flag on)."""
        snapshot = self._snapshot()
        provider = MagicMock()
        p_graphql, p_rest, p_html, g_att, r_att, h_att = _empty_round_patches()
        with (
            patch.dict("os.environ", {"ENABLE_BROWSER_APPLY_SUGGESTIONS": "true"}),
            p_graphql as mock_graphql,
            p_rest as mock_rest,
            p_html as mock_html,
            patch("agentic_devtools.cli.ci.pipeline.discovery.orchestrator.browser_discover") as mock_browser,
        ):
            mock_graphql.return_value = ([], g_att, "")
            mock_rest.return_value = ([], r_att)
            mock_html.return_value = ([], h_att)
            suggestions, attempts, _ = run_discovery(provider, snapshot)

        assert suggestions == []
        mock_browser.assert_not_called()
