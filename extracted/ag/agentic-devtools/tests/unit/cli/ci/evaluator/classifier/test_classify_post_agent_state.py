"""Exhaustive unit tests for classify_post_agent_state()."""

from agentic_devtools.cli.ci.critique_adjudicator import CritiqueAdjudicationRecord, CritiqueTask
from agentic_devtools.cli.ci.evaluator.classifier import _parse_timestamp, classify_post_agent_state
from agentic_devtools.cli.ci.evaluator.models import (
    CommentInfo,
    PostAgentClassification,
    PostAgentSnapshot,
    ThreadInfo,
)


class TestClassifyPostAgentState:
    """Tests covering all seven classification branches."""

    def test_parse_timestamp_rejects_empty_and_malformed_values(self):
        assert _parse_timestamp("") is None
        assert _parse_timestamp("   ") is None
        assert _parse_timestamp("not a timestamp") is None

    def test_parse_timestamp_normalizes_naive_and_preserves_aware_values(self):
        assert _parse_timestamp("2026-10-19T12:00:00").utcoffset().total_seconds() == 0
        assert _parse_timestamp("2026-10-19T12:00:00+02:00").utcoffset().total_seconds() == 7200

    def test_concurrent_evaluation_skipped(self):
        """Lock held by another run → concurrent_evaluation_skipped."""
        snap = PostAgentSnapshot(pr_number=1, lock_holder="other-run-123")
        assert classify_post_agent_state(snap) == PostAgentClassification.concurrent_evaluation_skipped

    def test_complete_with_sentinel(self):
        """Sentinel present → complete."""
        snap = PostAgentSnapshot(pr_number=1, has_sentinel=True)
        assert classify_post_agent_state(snap) == PostAgentClassification.complete

    def test_complete_with_sentinel_and_lock(self):
        """Sentinel present but lock held → concurrent_evaluation_skipped (lock takes priority)."""
        snap = PostAgentSnapshot(pr_number=1, has_sentinel=True, lock_holder="other")
        assert classify_post_agent_state(snap) == PostAgentClassification.concurrent_evaluation_skipped

    def test_repair_satisfied_no_changes(self):
        """Repair-satisfied marker present, no head change → repair_satisfied_no_changes."""
        threads = (ThreadInfo(comment_id=1, is_resolved=False),)
        snap = PostAgentSnapshot(
            pr_number=1,
            threads=threads,
            has_repair_satisfied_marker=True,
            review_id=42,
            repair_satisfied_review_id=42,
            head_changed_since_review=False,
        )
        assert classify_post_agent_state(snap) == PostAgentClassification.repair_satisfied_no_changes

    def test_repair_satisfied_ignored_when_head_changed(self):
        """Repair-satisfied marker present but head changed → NOT repair_satisfied."""
        threads = (ThreadInfo(comment_id=1, is_resolved=False),)
        snap = PostAgentSnapshot(
            pr_number=1,
            threads=threads,
            has_repair_satisfied_marker=True,
            repair_satisfied_review_id=42,
            head_changed_since_review=True,
        )
        # head_changed + unresolved → changes_made_threads_unresolved
        assert classify_post_agent_state(snap) == PostAgentClassification.changes_made_threads_unresolved

    def test_repair_satisfied_takes_priority_over_agent_claims_fixed(self):
        """Repair-satisfied marker takes priority over agent_claims_fixed_no_sentinel."""
        threads = (ThreadInfo(comment_id=1, is_resolved=False),)
        comment = CommentInfo(id=99, author="copilot[bot]", body="No changes needed")
        snap = PostAgentSnapshot(
            pr_number=1,
            threads=threads,
            latest_agent_comment=comment,
            has_repair_satisfied_marker=True,
            review_id=42,
            repair_satisfied_review_id=42,
            head_changed_since_review=False,
        )
        assert classify_post_agent_state(snap) == PostAgentClassification.repair_satisfied_no_changes

    def test_repair_satisfied_ignored_on_review_id_mismatch(self):
        """Mismatched review-id marker is ignored and falls through."""
        threads = (ThreadInfo(comment_id=1, is_resolved=False),)
        snap = PostAgentSnapshot(
            pr_number=1,
            threads=threads,
            has_repair_satisfied_marker=True,
            review_id=101,
            repair_satisfied_review_id=42,
            head_changed_since_review=False,
        )
        assert classify_post_agent_state(snap) == PostAgentClassification.agent_silent

    def test_threads_resolved_no_sentinel(self):
        """All threads resolved, no sentinel → threads_resolved_no_sentinel."""
        threads = (
            ThreadInfo(comment_id=1, is_resolved=True),
            ThreadInfo(comment_id=2, is_resolved=True),
        )
        snap = PostAgentSnapshot(pr_number=1, threads=threads)
        assert classify_post_agent_state(snap) == PostAgentClassification.threads_resolved_no_sentinel

    def test_agent_claims_fixed_no_sentinel(self):
        """Agent comment present, no head change, unresolved threads."""
        threads = (ThreadInfo(comment_id=1, is_resolved=False),)
        comment = CommentInfo(id=99, author="copilot[bot]", body="Already fixed")
        snap = PostAgentSnapshot(
            pr_number=1,
            threads=threads,
            latest_agent_comment=comment,
            head_changed_since_review=False,
        )
        assert classify_post_agent_state(snap) == PostAgentClassification.agent_claims_fixed_no_sentinel

    def test_changes_made_threads_unresolved(self):
        """Head changed, unresolved threads → changes_made_threads_unresolved."""
        threads = (ThreadInfo(comment_id=1, is_resolved=False),)
        snap = PostAgentSnapshot(
            pr_number=1,
            threads=threads,
            head_changed_since_review=True,
        )
        assert classify_post_agent_state(snap) == PostAgentClassification.changes_made_threads_unresolved

    def test_agent_silent_no_threads(self):
        """No sentinel, no threads, no comment → agent_silent."""
        snap = PostAgentSnapshot(pr_number=1)
        assert classify_post_agent_state(snap) == PostAgentClassification.agent_silent

    def test_agent_silent_with_head_change_no_threads(self):
        """Head changed but no unresolved threads (empty) → agent_silent."""
        snap = PostAgentSnapshot(pr_number=1, head_changed_since_review=True)
        assert classify_post_agent_state(snap) == PostAgentClassification.agent_silent

    def test_agent_claims_fixed_overrides_changes_made(self):
        """Agent comment without head change takes priority over changes_made."""
        threads = (ThreadInfo(comment_id=1, is_resolved=False),)
        comment = CommentInfo(id=99, body="Done")
        snap = PostAgentSnapshot(
            pr_number=1,
            threads=threads,
            latest_agent_comment=comment,
            head_changed_since_review=False,
        )
        assert classify_post_agent_state(snap) == PostAgentClassification.agent_claims_fixed_no_sentinel

    def test_changes_made_with_agent_comment(self):
        """Head changed with agent comment still classifies as changes_made."""
        threads = (ThreadInfo(comment_id=1, is_resolved=False),)
        comment = CommentInfo(id=99, body="Fixed")
        snap = PostAgentSnapshot(
            pr_number=1,
            threads=threads,
            latest_agent_comment=comment,
            head_changed_since_review=True,
        )
        # head_changed + unresolved → changes_made (rule 5), even if agent commented
        assert classify_post_agent_state(snap) == PostAgentClassification.changes_made_threads_unresolved

    def test_completed_critique_reply_is_adjudicated_before_repair_satisfied(self):
        task = CritiqueTask(1, "head", 42, 1, "2026-10-19T12:00:00Z")
        comment = CommentInfo(99, body="The concern is already covered.", created_at="2026-10-19T12:01:00Z")
        snap = PostAgentSnapshot(
            pr_number=1,
            current_head_sha="head",
            review_id=42,
            latest_agent_comment=comment,
            critique_task=task,
            critique_task_completed=True,
            has_repair_satisfied_marker=True,
            repair_satisfied_review_id=42,
        )

        assert classify_post_agent_state(snap) == PostAgentClassification.critique_adjudication

    def test_progress_comment_does_not_adjudicate_an_active_or_unknown_task(self):
        task = CritiqueTask(1, "head", 42, 1, "2026-10-19T12:00:00Z", "task-123")
        comment = CommentInfo(99, body="Progress update: investigating.", created_at="2026-10-19T12:01:00Z")
        for completion in (False, None):
            snap = PostAgentSnapshot(
                pr_number=1,
                current_head_sha="head",
                review_id=42,
                latest_agent_comment=comment,
                critique_task=task,
                critique_task_completed=completion,
            )

            assert classify_post_agent_state(snap) == PostAgentClassification.critique_task_pending

    def test_generic_sentinel_does_not_suppress_newer_critique_reply_adjudication(self):
        task = CritiqueTask(1, "head", 42, 1, "2026-10-19T12:00:00Z")
        snap = PostAgentSnapshot(
            pr_number=1,
            has_sentinel=True,
            current_head_sha="head",
            review_id=42,
            latest_agent_comment=CommentInfo(99, body="No change is needed.", created_at="2026-10-19T12:01:00Z"),
            critique_task=task,
            critique_task_completed=True,
        )

        assert classify_post_agent_state(snap) == PostAgentClassification.critique_adjudication

    def test_sentinel_completes_only_when_the_exact_task_was_adjudicated(self):
        task = CritiqueTask(1, "head", 42, 2, "2026-10-19T12:00:00Z")
        record = CritiqueAdjudicationRecord(1, "head", 42, 2, "rebutted", "The evidence does not support the critique.")
        snap = PostAgentSnapshot(
            pr_number=1,
            has_sentinel=True,
            current_head_sha="head",
            review_id=42,
            latest_agent_comment=CommentInfo(99, body="No change is needed.", created_at="2026-10-19T12:01:00Z"),
            critique_task=task,
            critique_task_completed=True,
            critique_adjudications=(record,),
        )

        assert classify_post_agent_state(snap) == PostAgentClassification.complete

    def test_sentinel_does_not_skip_needs_human_label_restoration(self):
        task = CritiqueTask(1, "head", 42, 1, "2026-10-19T12:00:00Z")
        record = CritiqueAdjudicationRecord(1, "head", 42, 1, "needs_human", "Human review is required.")
        snap = PostAgentSnapshot(
            pr_number=1,
            has_sentinel=True,
            current_head_sha="head",
            review_id=42,
            latest_agent_comment=CommentInfo(99, body="Reply.", created_at="2026-10-19T12:01:00Z"),
            critique_task=task,
            critique_task_completed=True,
            critique_adjudications=(record,),
        )

        assert classify_post_agent_state(snap) == PostAgentClassification.critique_adjudication

    def test_sentinel_for_another_task_attempt_does_not_suppress_adjudication(self):
        task = CritiqueTask(1, "head", 42, 2, "2026-10-19T12:00:00Z")
        earlier_attempt = CritiqueAdjudicationRecord(1, "head", 42, 1, "rebutted", "Earlier attempt.")
        snap = PostAgentSnapshot(
            pr_number=1,
            has_sentinel=True,
            current_head_sha="head",
            review_id=42,
            latest_agent_comment=CommentInfo(99, body="No change is needed.", created_at="2026-10-19T12:01:00Z"),
            critique_task=task,
            critique_task_completed=True,
            critique_adjudications=(earlier_attempt,),
        )

        assert classify_post_agent_state(snap) == PostAgentClassification.critique_adjudication

    def test_rebutted_current_task_does_not_reach_silent_agent_fallback(self):
        task = CritiqueTask(1, "head", 42, 1, "2026-10-19T12:00:00Z")
        record = CritiqueAdjudicationRecord(1, "head", 42, 1, "rebutted", "No code defect was found.")
        snap = PostAgentSnapshot(
            pr_number=1,
            current_head_sha="head",
            review_id=42,
            latest_agent_comment=CommentInfo(99, body="No change is needed.", created_at="2026-10-19T12:01:00Z"),
            critique_task=task,
            critique_task_completed=True,
            critique_adjudications=(record,),
        )

        assert classify_post_agent_state(snap) == PostAgentClassification.complete

    def test_critique_reply_must_be_current_and_newer_than_task(self):
        task = CritiqueTask(1, "head", 42, 1, "2026-10-19T12:00:00Z")
        snap = PostAgentSnapshot(
            pr_number=1,
            current_head_sha="head",
            review_id=42,
            latest_agent_comment=CommentInfo(99, body="Reply", created_at="2026-10-19T11:59:00Z"),
            critique_task=task,
            critique_task_completed=True,
        )
        assert classify_post_agent_state(snap) == PostAgentClassification.agent_silent

        moved = PostAgentSnapshot(
            pr_number=1,
            current_head_sha="new-head",
            review_id=42,
            latest_agent_comment=CommentInfo(99, body="Reply", created_at="2026-10-19T12:01:00Z"),
            critique_task=task,
            critique_task_completed=True,
        )
        assert classify_post_agent_state(moved) == PostAgentClassification.agent_silent

    def test_critique_task_attempt_is_adjudicated_once_except_needs_human_label_retry(self):
        task = CritiqueTask(1, "head", 42, 1, "2026-10-19T12:00:00Z")
        comment = CommentInfo(99, body="Reply", created_at="2026-10-19T12:01:00Z")
        record = CritiqueAdjudicationRecord(1, "head", 42, 1, "rebutted", "Evidence supports the reply.")
        snap = PostAgentSnapshot(
            pr_number=1,
            current_head_sha="head",
            review_id=42,
            threads=(ThreadInfo(comment_id=1, is_resolved=False),),
            latest_agent_comment=comment,
            critique_task=task,
            critique_task_completed=True,
            critique_adjudications=(record,),
        )
        assert classify_post_agent_state(snap) == PostAgentClassification.agent_claims_fixed_no_sentinel

        needs_human = CritiqueAdjudicationRecord(1, "head", 42, 1, "needs_human", "Insufficient evidence.")
        snap = PostAgentSnapshot(
            pr_number=1,
            current_head_sha="head",
            review_id=42,
            threads=(ThreadInfo(comment_id=1, is_resolved=False),),
            latest_agent_comment=comment,
            critique_task=task,
            critique_task_completed=True,
            critique_adjudications=(needs_human,),
        )
        assert classify_post_agent_state(snap) == PostAgentClassification.critique_adjudication
