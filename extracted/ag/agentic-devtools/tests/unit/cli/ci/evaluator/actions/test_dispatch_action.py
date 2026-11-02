"""Tests for dispatch_action()."""

from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from agentic_devtools.cli.ci.critique_adjudicator import CritiqueAdjudicationRecord, CritiqueTask
from agentic_devtools.cli.ci.evaluator.actions import dispatch_action
from agentic_devtools.cli.ci.evaluator.classifier import classify_post_agent_state
from agentic_devtools.cli.ci.evaluator.models import (
    CommentInfo,
    PostAgentAction,
    PostAgentClassification,
    PostAgentSnapshot,
)
from agentic_devtools.cli.ci.guards import AGENT_FAILED_LABEL


class TestDispatchAction:
    """Tests for evaluator action dispatch behavior."""

    def test_preserves_concurrent_classification_for_no_action(self):
        """No-action handler must keep the input concurrent classification."""
        provider = MagicMock()
        snapshot = PostAgentSnapshot(pr_number=42, repo="owner/repo", has_sentinel=True)

        result = dispatch_action(
            PostAgentClassification.concurrent_evaluation_skipped,
            provider,
            snapshot,
            dry_run=True,
        )

        assert result.classification == PostAgentClassification.concurrent_evaluation_skipped

    def test_dispatches_non_no_action_handler(self):
        """Non-no_action classifications dispatch to their mapped handler."""
        provider = MagicMock()
        snapshot = PostAgentSnapshot(pr_number=42, repo="owner/repo")

        result = dispatch_action(
            PostAgentClassification.threads_resolved_no_sentinel,
            provider,
            snapshot,
            dry_run=True,
        )

        assert result.action_taken == PostAgentAction.synthesize_sentinel

    def test_sentinel_with_needs_human_record_restores_label_without_ai(self):
        """An exact needs-human outcome restores its label despite a generic sentinel."""
        task = CritiqueTask(42, "head", 100, 1, "2026-10-19T12:00:00Z")
        record = CritiqueAdjudicationRecord(42, "head", 100, 1, "needs_human", "Human review is required.")
        snapshot = PostAgentSnapshot(
            pr_number=42,
            has_sentinel=True,
            current_head_sha="head",
            review_id=100,
            latest_agent_comment=CommentInfo(99, body="Reply.", created_at="2026-10-19T12:01:00Z"),
            critique_task=task,
            critique_task_completed=True,
            critique_adjudications=(record,),
        )
        provider = MagicMock()
        provider.get_pr_metadata.return_value = SimpleNamespace(head_sha="head")

        classification = classify_post_agent_state(snapshot)
        with patch("agentic_devtools.cli.ci.evaluator.critique_actions.run_critique_adjudication") as run_ai:
            result = dispatch_action(classification, provider, snapshot)

        assert classification == PostAgentClassification.critique_adjudication
        assert result.action_taken == PostAgentAction.adjudicate_critique
        assert result.success is True
        provider.add_label.assert_called_once_with(42, AGENT_FAILED_LABEL)
        provider.post_comment_as_pr_token.assert_not_called()
        run_ai.assert_not_called()

    def test_agent_claims_without_head_change_routes_to_rereview(self):
        """No post-review change should route to re-review, not auto-resolution."""
        provider = MagicMock()
        snapshot = PostAgentSnapshot(
            pr_number=42,
            repo="owner/repo",
            head_changed_since_review=False,
        )

        result = dispatch_action(
            PostAgentClassification.agent_claims_fixed_no_sentinel,
            provider,
            snapshot,
            dry_run=True,
        )

        assert result.action_taken == PostAgentAction.trigger_re_review

    def test_agent_claims_without_head_change_preserves_classification(self):
        """Classification must remain agent_claims_fixed_no_sentinel when routed to re-review."""
        provider = MagicMock()
        snapshot = PostAgentSnapshot(
            pr_number=42,
            repo="owner/repo",
            head_changed_since_review=False,
        )

        result = dispatch_action(
            PostAgentClassification.agent_claims_fixed_no_sentinel,
            provider,
            snapshot,
            dry_run=True,
        )

        assert result.classification == PostAgentClassification.agent_claims_fixed_no_sentinel

    def test_agent_claims_with_head_change_routes_to_verify(self):
        """Post-review changes with agent claim should use verify-and-resolve."""
        provider = MagicMock()
        snapshot = PostAgentSnapshot(
            pr_number=42,
            repo="owner/repo",
            head_changed_since_review=True,
        )

        result = dispatch_action(
            PostAgentClassification.agent_claims_fixed_no_sentinel,
            provider,
            snapshot,
            dry_run=True,
        )

        assert result.action_taken == PostAgentAction.verify_and_resolve
