"""Tests for DispatchRepairAction."""

from dataclasses import replace
from unittest.mock import MagicMock, patch

import pytest

from agentic_devtools.cli.ci.models import ReviewCommentInfo, ReviewInfo
from agentic_devtools.cli.ci.pipeline.actions.dispatch_repair import (
    DispatchRepairAction,
)
from agentic_devtools.cli.ci.pipeline.gate_verdict import (
    REASON_AWAITING_FRESH,
    REASON_CLEAN,
    REASON_CONTENT_CHANGED,
    REASON_HAS_COMMENTS,
    REASON_NEW_CCR_NOT_APPROVED,
    REASON_SUPPRESSED_COMMENTS,
    REASON_UNPARSED_SUPPRESSION,
    CopilotGateVerdict,
)
from agentic_devtools.cli.ci.pipeline.models import ActionDecision
from agentic_devtools.cli.ci.pipeline.snapshot import DerivedState, PRStateSnapshot
from agentic_devtools.cli.shared.retry import ProviderRateLimitError


class TestDispatchRepairAction:
    """Tests for dispatch repair action evaluation."""

    def _execute_review_dispatch(
        self,
        provider: MagicMock,
        comments: list[ReviewCommentInfo],
        thread_states: dict[int, tuple[bool, bool]] | None = None,
    ) -> list[ReviewCommentInfo]:
        snapshot = PRStateSnapshot(
            pr_number=42,
            ci_status="passing",
            head_sha="abc123",
            review_state="CHANGES_REQUESTED",
            copilot_review_id=100,
            check_runs=[],
        )
        derived = DerivedState(snapshot)
        provider.list_review_comments.return_value = comments
        provider.list_review_thread_states.return_value = thread_states if thread_states is not None else {}
        provider.dispatch_repair.return_value = 77

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.is_duplicate_trigger",
                return_value=False,
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
                return_value=(False, 0),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_cycle_limit",
                return_value=(False, 1),
            ),
        ):
            result = DispatchRepairAction().execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.EXECUTE
        return provider.dispatch_repair.call_args.kwargs["review_comments"]

    def test_excludes_answered_cloud_coding_agent_root_and_reply(self) -> None:
        root = ReviewCommentInfo(
            id=101,
            path="src/foo.py",
            body="Fix this",
            html_url="https://example.test/root",
            author_login="copilot-pull-request-reviewer[bot]",
        )
        reply = ReviewCommentInfo(
            id=202,
            path="src/foo.py",
            body="Implemented.",
            html_url="https://example.test/reply",
            author_login="copilot-swe-agent[bot]",
            in_reply_to_id=101,
        )
        snapshot = PRStateSnapshot(
            pr_number=42,
            ci_status="passing",
            head_sha="abc123",
            review_state="CHANGES_REQUESTED",
            copilot_review_id=100,
            check_runs=[],
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider.list_review_comments.return_value = [root, reply]
        provider.list_review_thread_states.return_value = {101: (False, True), 202: (False, True)}
        provider.dispatch_repair.return_value = 77

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.is_duplicate_trigger",
                return_value=False,
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
                return_value=(False, 0),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_cycle_limit",
                return_value=(False, 1),
            ),
        ):
            result = DispatchRepairAction().execute(provider, snapshot, derived)

        # All comments were filtered (root suppressed, reply dropped) and CI is
        # passing with no declared suppressed findings — repair must be skipped.
        assert result.decision == ActionDecision.SKIP
        provider.dispatch_repair.assert_not_called()

    def test_keeps_unresolved_root_without_cloud_coding_agent_response(self) -> None:
        root = ReviewCommentInfo(
            id=101,
            path="src/foo.py",
            body="Fix this",
            html_url="https://example.test/root",
            author_login="copilot-pull-request-reviewer[bot]",
        )
        provider = MagicMock()

        comments = self._execute_review_dispatch(provider, [root], {101: (False, False)})

        assert comments == [root]

    def test_drops_resolved_root_without_response(self) -> None:
        root = ReviewCommentInfo(id=101, path="src/foo.py", body="Fix this", html_url="")
        snapshot = PRStateSnapshot(
            pr_number=42,
            ci_status="passing",
            head_sha="abc123",
            review_state="CHANGES_REQUESTED",
            copilot_review_id=100,
            check_runs=[],
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider.list_review_comments.return_value = [root]
        provider.list_review_thread_states.return_value = {101: (True, False)}
        provider.dispatch_repair.return_value = 77

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.is_duplicate_trigger",
                return_value=False,
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
                return_value=(False, 0),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_cycle_limit",
                return_value=(False, 1),
            ),
        ):
            result = DispatchRepairAction().execute(provider, snapshot, derived)

        # The root is resolved so it is filtered out; CI is passing and there are
        # no declared suppressed findings — repair must be skipped.
        assert result.decision == ActionDecision.SKIP
        provider.dispatch_repair.assert_not_called()

    def test_invalid_cloud_reply_does_not_suppress_root(self) -> None:
        root = ReviewCommentInfo(id=101, path="src/foo.py", body="Fix this", html_url="")
        empty_reply = ReviewCommentInfo(
            id=202,
            path="src/foo.py",
            body=" ",
            html_url="",
            author_login="copilot-swe-agent[bot]",
            in_reply_to_id=101,
        )
        provider = MagicMock()

        comments = self._execute_review_dispatch(
            provider,
            [root, empty_reply],
            {101: (False, True), 202: (False, True)},
        )

        # The empty reply is a Cloud Coding Agent reply with a valid parent and is
        # always dropped regardless of body content. The root is not suppressed
        # because the reply body is empty, so it is retained as a repair candidate.
        assert comments == [root]

    def test_stuck_prior_threads_skips_when_owner_reviews_are_fully_filtered(self) -> None:
        """Stuck-thread dispatch is skipped when ownership filtering leaves no owner reviews."""
        root = ReviewCommentInfo(
            id=101,
            path="src/foo.py",
            body="Fix this",
            html_url="https://example.test/root",
            author_login="copilot-pull-request-reviewer[bot]",
        )
        reply = ReviewCommentInfo(
            id=202,
            path="src/foo.py",
            body="Implemented.",
            html_url="https://example.test/reply",
            author_login="copilot-swe-agent[bot]",
            in_reply_to_id=101,
        )
        snapshot = PRStateSnapshot(
            pr_number=42,
            ci_status="passing",
            head_sha="abc123",
            copilot_review_id=0,
            unresolved_threads=1,
            repairable_threads=1,
            reviews=[
                ReviewInfo(
                    id=12,
                    user="Copilot",
                    state="CHANGES_REQUESTED",
                    commit_sha="old111",
                    submitted_at="2024-01-01T11:00:00Z",
                )
            ],
            check_runs=[],
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider.list_review_threads_by_thread_id.return_value = {"thread-1": (False, (101, 202))}
        provider.list_review_comments.return_value = [root, reply]
        provider.dispatch_repair.return_value = 77

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.is_duplicate_trigger",
                return_value=False,
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
                return_value=(False, 0),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_cycle_limit",
                return_value=(False, 1),
            ),
        ):
            result = DispatchRepairAction().execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.SKIP
        provider.dispatch_repair.assert_not_called()
        provider.list_review_comments.assert_called_once_with(42, 12)

    def test_stuck_fully_filtered_reviews_use_review_context_for_shortfall_dispatch(self) -> None:
        """Shortfall dispatches retain a review ID when all stuck reviews are filtered."""
        root = ReviewCommentInfo(
            id=101,
            path="src/foo.py",
            body="Fix this",
            html_url="https://example.test/root",
            author_login="copilot-pull-request-reviewer[bot]",
        )
        reply = ReviewCommentInfo(
            id=202,
            path="src/foo.py",
            body="Implemented.",
            html_url="https://example.test/reply",
            author_login="copilot-swe-agent[bot]",
            in_reply_to_id=101,
        )
        snapshot = PRStateSnapshot(
            pr_number=42,
            ci_status="passing",
            head_sha="abc123",
            copilot_review_id=0,
            unresolved_threads=1,
            repairable_threads=1,
            reviews=[
                ReviewInfo(
                    id=12,
                    user="Copilot",
                    state="CHANGES_REQUESTED",
                    commit_sha="old111",
                    submitted_at="2024-01-01T11:00:00Z",
                    body="### Comments suppressed due to low confidence (2)\n\nreview body",
                )
            ],
            check_runs=[],
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider.list_review_threads_by_thread_id.return_value = {"thread-1": (False, (101, 202))}
        provider.list_review_comments.return_value = [root, reply]
        provider.dispatch_repair.return_value = 77

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.is_duplicate_trigger",
                return_value=False,
            ) as mock_is_duplicate_trigger,
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
                return_value=(False, 0),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_cycle_limit",
                return_value=(False, 1),
            ),
        ):
            result = DispatchRepairAction().execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.EXECUTE
        assert provider.dispatch_repair.call_args.kwargs["review_id"] == 12
        mock_is_duplicate_trigger.assert_called_once_with(provider, 42, 12)

    def test_keeps_synthetic_entry_when_thread_is_answered(self) -> None:
        root = ReviewCommentInfo(id=101, path="src/foo.py", body="Fix this", html_url="")
        reply = ReviewCommentInfo(
            id=202,
            path="src/foo.py",
            body="Implemented.",
            html_url="",
            author_login="copilot-swe-agent",
            in_reply_to_id=101,
        )
        synthetic = ReviewCommentInfo(
            id=-1, path="README.md", body="Suppressed finding", html_url="", is_suppressed=True
        )
        provider = MagicMock()

        comments = self._execute_review_dispatch(
            provider,
            [root, reply, synthetic],
            {101: (False, True), 202: (False, True)},
        )

        assert comments == [synthetic]

    def test_human_reply_does_not_suppress_root(self) -> None:
        root = ReviewCommentInfo(id=101, path="src/foo.py", body="Fix this", html_url="")
        human_reply = ReviewCommentInfo(
            id=202,
            path="src/foo.py",
            body="Can you clarify?",
            html_url="",
            author_login="octocat",
            in_reply_to_id=101,
        )
        provider = MagicMock()

        comments = self._execute_review_dispatch(
            provider,
            [root, human_reply],
            {101: (False, True), 202: (False, True)},
        )

        assert comments == [root, human_reply]

    def test_thread_state_failure_keeps_possible_root(self) -> None:
        root = ReviewCommentInfo(id=101, path="src/foo.py", body="Fix this", html_url="")
        provider = MagicMock()
        provider.list_review_thread_states.side_effect = RuntimeError("unavailable")

        comments = self._execute_review_dispatch(provider, [root])

        assert comments == [root]

    def test_fetch_failure_disables_filtered_skip(self) -> None:
        """When list_review_comments raises, dispatch is fail-open even with CI passing."""
        snapshot = PRStateSnapshot(
            pr_number=42,
            ci_status="passing",
            head_sha="abc123",
            review_state="CHANGES_REQUESTED",
            copilot_review_id=100,
            check_runs=[],
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider.list_review_comments.side_effect = RuntimeError("network error")
        provider.dispatch_repair.return_value = 77

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.is_duplicate_trigger",
                return_value=False,
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
                return_value=(False, 0),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_cycle_limit",
                return_value=(False, 1),
            ),
        ):
            result = DispatchRepairAction().execute(provider, snapshot, derived)

        # Fetch failed — must not skip; dispatch fail-open so transient errors
        # do not silently drop real work.
        assert result.decision == ActionDecision.EXECUTE
        provider.dispatch_repair.assert_called_once()

    def test_declared_suppressed_findings_prevent_filtered_skip(self) -> None:
        """Declared suppressed findings must still dispatch even when all inline comments are filtered."""
        snapshot = PRStateSnapshot(
            pr_number=42,
            ci_status="passing",
            head_sha="abc123",
            review_state="CHANGES_REQUESTED",
            copilot_review_id=100,
            check_runs=[],
            reviews=[
                ReviewInfo(
                    id=100,
                    user="Copilot",
                    state="CHANGES_REQUESTED",
                    body="### Comments suppressed due to low confidence (2)\n\nsome prose",
                )
            ],
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()
        # All inline comments are filtered (e.g., all resolved)
        provider.list_review_comments.return_value = []
        provider.dispatch_repair.return_value = 77

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.is_duplicate_trigger",
                return_value=False,
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
                return_value=(False, 0),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_cycle_limit",
                return_value=(False, 1),
            ),
        ):
            result = DispatchRepairAction().execute(provider, snapshot, derived)

        # Declared suppressed count > 0 — repair must run so the agent receives
        # a shortfall notice for the unrecovered author comments.
        assert result.decision == ActionDecision.EXECUTE
        provider.dispatch_repair.assert_called_once()

    def test_empty_review_collection_is_not_skipped(self) -> None:
        """A review that was empty from the start (not filtered empty) must still dispatch.

        An empty-from-the-start collection is not evidence of all-replied work;
        the review may still carry context that the agent needs (body, link).
        """
        snapshot = PRStateSnapshot(
            pr_number=42,
            ci_status="passing",
            head_sha="abc123",
            review_state="CHANGES_REQUESTED",
            copilot_review_id=100,
            check_runs=[],
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider.list_review_comments.return_value = []
        provider.list_review_thread_states.return_value = {}
        provider.dispatch_repair.return_value = 77

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.is_duplicate_trigger",
                return_value=False,
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
                return_value=(False, 0),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_cycle_limit",
                return_value=(False, 1),
            ),
        ):
            result = DispatchRepairAction().execute(provider, snapshot, derived)

        # Review was empty from the start — not made empty by filtering — so
        # the guard must not suppress dispatch.
        assert result.decision == ActionDecision.EXECUTE
        provider.dispatch_repair.assert_called_once()

    def test_execute_when_ci_failing_even_with_active_session(self) -> None:
        """Session gate removed: active_session=True does NOT cause skip."""
        snapshot = PRStateSnapshot(pr_number=1, active_session=True, ci_status="failing")
        derived = DerivedState(snapshot)
        action = DispatchRepairAction()
        result = action.evaluate(snapshot, derived)
        assert result.decision == ActionDecision.EXECUTE

    def test_preconditions_do_not_contain_no_active_session(self) -> None:
        """no_active_session key must be absent from preconditions."""
        snapshot = PRStateSnapshot(pr_number=1, ci_status="failing")
        derived = DerivedState(snapshot)
        action = DispatchRepairAction()
        result = action.evaluate(snapshot, derived)
        assert "no_active_session" not in result.preconditions

    def test_execute_when_review_actionable_with_active_session(self) -> None:
        """Session gate removed: actionable review + active_session=True returns EXECUTE."""
        snapshot = PRStateSnapshot(
            pr_number=1,
            ci_status="passing",
            active_session=True,
            review_state="CHANGES_REQUESTED",
            copilot_review_id=100,
        )
        derived = DerivedState(snapshot)
        action = DispatchRepairAction()
        result = action.evaluate(snapshot, derived)
        assert result.decision == ActionDecision.EXECUTE

    def test_skip_when_ci_passing_and_no_review(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=1,
            ci_status="passing",
            review_state="APPROVED",
            copilot_review_id=1,
        )
        derived = DerivedState(snapshot)
        action = DispatchRepairAction()
        result = action.evaluate(snapshot, derived)
        assert result.decision == ActionDecision.SKIP
        assert "no actionable" in result.details.lower() or "passing" in result.details.lower()

    def test_skip_when_effective_review_work_is_empty(self) -> None:
        """A stale review with no effective comments does not trigger repair."""
        snapshot = PRStateSnapshot(
            pr_number=3993,
            ci_status="passing",
            review_state="CHANGES_REQUESTED",
            copilot_review_id=5409561506,
            copilot_review_inline_count=-1,
            effective_review_comment_count=0,
            effective_review_comment_count_review_id=5409561506,
        )
        result = DispatchRepairAction().evaluate(snapshot, DerivedState(snapshot))

        assert result.decision == ActionDecision.SKIP
        assert result.preconditions["review_actionable"] is True
        assert result.preconditions["effective_review_work"] is False
        assert "effective review work" in result.details.lower()

    def test_execute_skips_when_effective_review_work_is_empty(self) -> None:
        """Direct execution also skips stale review work before posting a repair."""
        snapshot = PRStateSnapshot(
            pr_number=3993,
            ci_status="passing",
            review_state="CHANGES_REQUESTED",
            copilot_review_id=5409561506,
            effective_review_comment_count=0,
            effective_review_comment_count_review_id=5409561506,
        )
        provider = MagicMock()

        result = DispatchRepairAction().execute(provider, snapshot, DerivedState(snapshot))

        assert result.decision == ActionDecision.SKIP
        assert "effective review work" in result.details.lower()
        provider.dispatch_repair.assert_not_called()

    def test_failing_ci_dispatches_when_effective_review_work_is_empty(self) -> None:
        """CI failure remains an independent repair reason when review work is stale."""
        snapshot = PRStateSnapshot(
            pr_number=3993,
            ci_status="failing",
            review_state="CHANGES_REQUESTED",
            copilot_review_id=5409561506,
            copilot_review_inline_count=-1,
            effective_review_comment_count=0,
            effective_review_comment_count_review_id=5409561506,
        )
        result = DispatchRepairAction().evaluate(snapshot, DerivedState(snapshot))

        assert result.decision == ActionDecision.EXECUTE
        assert result.preconditions["ci_failing"] is True
        assert result.preconditions["effective_review_work"] is False

    def test_dispatches_when_effective_current_review_work_remains(self) -> None:
        """A current review with effective comments still triggers repair."""
        snapshot = PRStateSnapshot(
            pr_number=1,
            ci_status="passing",
            review_state="CHANGES_REQUESTED",
            copilot_review_id=100,
            copilot_review_inline_count=-1,
            effective_review_comment_count=1,
            effective_review_comment_count_review_id=100,
        )
        result = DispatchRepairAction().evaluate(snapshot, DerivedState(snapshot))

        assert result.decision == ActionDecision.EXECUTE
        assert result.preconditions["review_actionable"] is True
        assert result.preconditions["effective_review_work"] is True

    def test_skips_new_ccr_review_when_reported_comments_are_all_filtered(self) -> None:
        """A new-CCR review with no remaining reported comments does not dispatch."""
        snapshot = PRStateSnapshot(
            pr_number=1,
            ci_status="passing",
            review_state="COMMENTED",
            copilot_review_id=100,
            copilot_review_inline_count=0,
            effective_review_comment_count=0,
            effective_review_comment_count_review_id=100,
            effective_review_comment_filter_applied=True,
            copilot_gate_verdict=CopilotGateVerdict(
                passed=False,
                reason=REASON_NEW_CCR_NOT_APPROVED,
                review_id=100,
                body_comment_count=3,
            ),
        )
        result = DispatchRepairAction().evaluate(snapshot, DerivedState(snapshot))

        assert result.decision == ActionDecision.SKIP
        assert result.preconditions["review_actionable"] is True
        assert result.preconditions["effective_review_work"] is False

    def test_dispatches_new_ccr_body_only_work_when_effective_inventory_is_empty(self) -> None:
        """Unknown inline work in a new-CCR body remains fail-open."""
        snapshot = PRStateSnapshot(
            pr_number=1,
            ci_status="passing",
            review_state="COMMENTED",
            copilot_review_id=100,
            copilot_review_inline_count=0,
            effective_review_comment_count=0,
            effective_review_comment_count_review_id=100,
            copilot_gate_verdict=CopilotGateVerdict(
                passed=False,
                reason=REASON_NEW_CCR_NOT_APPROVED,
                review_id=100,
                body_comment_count=0,
            ),
        )
        result = DispatchRepairAction().evaluate(snapshot, DerivedState(snapshot))

        assert result.decision == ActionDecision.EXECUTE
        assert result.preconditions["effective_review_work"] is True

    def test_dispatches_new_ccr_when_body_count_positive_without_filter_evidence(self) -> None:
        """A positive body count with no recorded filtering remains fail-open."""
        snapshot = PRStateSnapshot(
            pr_number=1,
            ci_status="passing",
            review_state="COMMENTED",
            copilot_review_id=100,
            copilot_review_inline_count=0,
            effective_review_comment_count=0,
            effective_review_comment_count_review_id=100,
            effective_review_comment_filter_applied=False,
            copilot_gate_verdict=CopilotGateVerdict(
                passed=False,
                reason=REASON_NEW_CCR_NOT_APPROVED,
                review_id=100,
                body_comment_count=3,
            ),
        )

        result = DispatchRepairAction().evaluate(snapshot, DerivedState(snapshot))

        assert result.decision == ActionDecision.EXECUTE
        assert result.preconditions["effective_review_work"] is True

    def test_dispatches_when_effective_count_source_review_differs_from_actionable_review(self) -> None:
        """Count data from a different review id must not suppress actionable work."""
        snapshot = PRStateSnapshot(
            pr_number=1,
            ci_status="passing",
            review_state="COMMENTED",
            copilot_review_id=100,
            copilot_review_inline_count=0,
            effective_review_comment_count=0,
            effective_review_comment_count_review_id=100,
            copilot_gate_verdict=CopilotGateVerdict(
                passed=False,
                reason=REASON_HAS_COMMENTS,
                review_id=200,
                body_comment_count=1,
            ),
        )

        result = DispatchRepairAction().evaluate(snapshot, DerivedState(snapshot))

        assert result.decision == ActionDecision.EXECUTE
        assert result.preconditions["review_actionable"] is True
        assert result.preconditions["effective_review_work"] is True

    def test_skip_message_includes_non_failing_ci_status(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=1,
            ci_status="pending",
            review_state="APPROVED",
            copilot_review_id=1,
        )
        derived = DerivedState(snapshot)
        action = DispatchRepairAction()
        result = action.evaluate(snapshot, derived)
        assert result.decision == ActionDecision.SKIP
        assert "ci_status=pending" in result.details.lower()

    def test_execute_when_ci_failing(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=1,
            ci_status="failing",
            active_session=False,
        )
        derived = DerivedState(snapshot)
        action = DispatchRepairAction()
        result = action.evaluate(snapshot, derived)
        assert result.decision == ActionDecision.EXECUTE

    def test_execute_when_review_actionable(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=1,
            ci_status="passing",
            active_session=False,
            review_state="CHANGES_REQUESTED",
            copilot_review_id=100,
        )
        derived = DerivedState(snapshot)
        action = DispatchRepairAction()
        result = action.evaluate(snapshot, derived)
        assert result.decision == ActionDecision.EXECUTE

    def test_execute_when_prior_review_threads_are_stuck(self) -> None:
        """Action executes when repairable threads exist, even if blocking thread count is 0."""
        snapshot = PRStateSnapshot(
            pr_number=1,
            ci_status="passing",
            head_sha="head123",
            copilot_review_id=0,
            unresolved_threads=0,  # Zero blocking threads
            repairable_threads=2,  # But repairable threads exist
            reviews=[
                ReviewInfo(id=10, user="Copilot", state="CHANGES_REQUESTED", commit_sha="old123"),
            ],
        )
        derived = DerivedState(snapshot)
        action = DispatchRepairAction()
        result = action.evaluate(snapshot, derived)
        assert result.decision == ActionDecision.EXECUTE
        assert result.preconditions.get("stuck_prior_threads") is True

    def test_evaluate_when_only_verdict_owned_repairable_threads_exist(self) -> None:
        """A verdict-owned unresolved thread should still trigger the stuck-thread repair path."""
        snapshot = PRStateSnapshot(
            pr_number=1,
            ci_status="passing",
            head_sha="head123",
            copilot_review_id=0,
            unresolved_threads=0,
            repairable_threads=1,
            copilot_gate_verdict=CopilotGateVerdict(
                passed=False,
                reason=REASON_CONTENT_CHANGED,
                review_id=100,
            ),
            reviews=[
                ReviewInfo(id=100, user="Copilot", state="COMMENTED", commit_sha="old123"),
            ],
        )
        derived = DerivedState(snapshot)
        action = DispatchRepairAction()
        result = action.evaluate(snapshot, derived)
        assert result.decision == ActionDecision.EXECUTE
        assert result.preconditions.get("stuck_prior_threads") is True

    def test_skip_when_threads_exist_but_no_prior_copilot_review(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=1,
            ci_status="passing",
            head_sha="head123",
            copilot_review_id=0,
            unresolved_threads=2,
            repairable_threads=2,
            reviews=[
                ReviewInfo(id=10, user="alice", state="CHANGES_REQUESTED", commit_sha="old123"),
            ],
        )
        derived = DerivedState(snapshot)
        action = DispatchRepairAction()
        result = action.evaluate(snapshot, derived)
        assert result.decision == ActionDecision.SKIP
        assert result.preconditions.get("stuck_prior_threads") is False

    def test_execute_when_prior_synthetic_review_threads_are_stuck(self) -> None:
        """Trusted synthetic review on a prior commit contributes to stuck_prior_threads."""
        from agentic_devtools.cli.ci.pipeline.gate_verdict import SYNTHETIC_MARKER, TRUSTED_SYNTHETIC_USERS

        synthetic_user = next(iter(TRUSTED_SYNTHETIC_USERS))
        snapshot = PRStateSnapshot(
            pr_number=1,
            ci_status="passing",
            head_sha="head123",
            copilot_review_id=0,
            unresolved_threads=2,
            repairable_threads=2,
            reviews=[
                ReviewInfo(
                    id=10,
                    user=synthetic_user,
                    state="CHANGES_REQUESTED",
                    commit_sha="old123",
                    body=f"Review feedback. {SYNTHETIC_MARKER}",
                ),
            ],
        )
        derived = DerivedState(snapshot)
        action = DispatchRepairAction()
        result = action.evaluate(snapshot, derived)
        assert result.decision == ActionDecision.EXECUTE
        assert result.preconditions.get("stuck_prior_threads") is True

    def test_execute_when_commented_review_inline_count_unknown(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=1,
            ci_status="passing",
            active_session=False,
            review_state="COMMENTED",
            copilot_review_id=100,
            copilot_review_inline_count=-1,
        )
        derived = DerivedState(snapshot)
        action = DispatchRepairAction()
        result = action.evaluate(snapshot, derived)
        assert result.decision == ActionDecision.EXECUTE

    def test_skip_when_ci_pending_even_if_review_actionable(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=1,
            ci_status="pending",
            active_session=False,
            review_state="COMMENTED",
            copilot_review_id=100,
            copilot_review_inline_count=1,
        )
        derived = DerivedState(snapshot)
        action = DispatchRepairAction()
        result = action.evaluate(snapshot, derived)
        assert result.decision == ActionDecision.SKIP
        assert "pending" in result.details.lower()

    def test_execute_dispatches_repair(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=42,
            ci_status="failing",
            head_sha="abc123",
            copilot_review_id=0,
            check_runs=[],
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider.dispatch_repair.return_value = 999

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
                return_value=(False, 0),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_cycle_limit",
                return_value=(False, 1),
            ),
        ):
            action = DispatchRepairAction()
            result = action.execute(provider, snapshot, derived)
            assert result.decision == ActionDecision.EXECUTE
            provider.dispatch_repair.assert_called_once()

    def test_execute_uses_ci_only_dedup_limit_of_one(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=42,
            ci_status="failing",
            head_sha="abc123",
            copilot_review_id=0,
            check_runs=[],
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider.dispatch_repair.return_value = 999

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
                return_value=(False, 0),
            ) as mock_check_deduplication,
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_cycle_limit",
                return_value=(False, 1),
            ),
        ):
            action = DispatchRepairAction()
            result = action.execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.EXECUTE
        mock_check_deduplication.assert_called_once_with(provider, 42, "abc123", max_dispatches=1)

    def test_execute_uses_default_dedup_limit_when_review_actionable(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=42,
            ci_status="passing",
            head_sha="abc123",
            review_state="CHANGES_REQUESTED",
            copilot_review_id=12,
            check_runs=[],
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider.list_review_comments.return_value = [MagicMock(id=1)]
        provider.dispatch_repair.return_value = 77

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.is_duplicate_trigger",
                return_value=False,
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
                return_value=(False, 0),
            ) as mock_check_deduplication,
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_cycle_limit",
                return_value=(False, 1),
            ),
        ):
            action = DispatchRepairAction()
            result = action.execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.EXECUTE
        mock_check_deduplication.assert_called_once_with(provider, 42, "abc123")

    def test_skip_when_dedup_limit_reached(self) -> None:
        snapshot = PRStateSnapshot(pr_number=1, ci_status="failing", head_sha="abc123")
        derived = DerivedState(snapshot)
        provider = MagicMock()

        with patch(
            "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
            return_value=(True, 3),
        ):
            action = DispatchRepairAction()
            result = action.execute(provider, snapshot, derived)
            assert result.decision == ActionDecision.SKIP
            assert "dedup" in result.details.lower()
            assert result.limit_reached is True

    def test_skip_when_cycle_limit_reached(self) -> None:
        snapshot = PRStateSnapshot(pr_number=1, ci_status="failing", head_sha="abc123")
        derived = DerivedState(snapshot)
        provider = MagicMock()

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
                return_value=(False, 0),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_cycle_limit",
                return_value=(True, 5),
            ),
        ):
            action = DispatchRepairAction()
            result = action.execute(provider, snapshot, derived)
            assert result.decision == ActionDecision.SKIP
            assert "cycle" in result.details.lower()
            assert result.limit_reached is True

    def test_failed_checks_uses_actionable_subset_only(self) -> None:
        """execute() passes only actionable failed checks to dispatch_repair."""
        from agentic_devtools.cli.ci.models import CheckRunStatus

        snapshot = PRStateSnapshot(
            pr_number=42,
            ci_status="failing",
            ci_failed_checks=["Targeted Checks ✅"],
            head_sha="abc123",
            check_runs=[
                CheckRunStatus(id=1, name="Targeted Checks ✅", status="completed", conclusion="failure"),
                CheckRunStatus(id=2, name="flaky-optional", status="completed", conclusion="failure"),
            ],
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider.dispatch_repair.return_value = 1

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
                return_value=(False, 0),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_cycle_limit",
                return_value=(False, 1),
            ),
        ):
            action = DispatchRepairAction()
            action.execute(provider, snapshot, derived)

        call_kwargs = provider.dispatch_repair.call_args
        passed_checks = call_kwargs.kwargs.get("failed_checks") or call_kwargs.args[3]
        check_names = [cr.name for cr in passed_checks]
        assert "Targeted Checks ✅" in check_names
        assert "flaky-optional" not in check_names

    def test_execute_sets_repair_dispatched_on_derived(self) -> None:
        """execute() must set derived.repair_dispatched after successful dispatch."""
        snapshot = PRStateSnapshot(
            pr_number=42,
            ci_status="failing",
            head_sha="abc123",
            copilot_review_id=0,
            check_runs=[],
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider.dispatch_repair.return_value = 999

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
                return_value=(False, 0),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_cycle_limit",
                return_value=(False, 1),
            ),
        ):
            action = DispatchRepairAction()
            result = action.execute(provider, snapshot, derived)
            assert result.decision == ActionDecision.EXECUTE
            assert derived.repair_dispatched is True

    def test_failed_when_deduplication_check_raises(self) -> None:
        snapshot = PRStateSnapshot(pr_number=1, ci_status="failing", head_sha="abc123")
        derived = DerivedState(snapshot)
        provider = MagicMock()

        with patch(
            "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
            side_effect=RuntimeError("dedup boom"),
        ):
            action = DispatchRepairAction()
            result = action.execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.FAILED
        assert "Deduplication check failed" in result.details

    def test_failed_when_cycle_limit_check_raises(self) -> None:
        snapshot = PRStateSnapshot(pr_number=1, ci_status="failing", head_sha="abc123")
        derived = DerivedState(snapshot)
        provider = MagicMock()

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
                return_value=(False, 0),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_cycle_limit",
                side_effect=RuntimeError("cycle boom"),
            ),
        ):
            action = DispatchRepairAction()
            result = action.execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.FAILED
        assert "Cycle limit check failed" in result.details

    def test_execute_dispatches_review_only_and_fetches_review_comments(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=42,
            ci_status="passing",
            head_sha="abc123",
            review_state="CHANGES_REQUESTED",
            copilot_review_id=12,
            check_runs=[],
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider.list_review_comments.return_value = [MagicMock(id=1)]
        provider.dispatch_repair.return_value = 77

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.is_duplicate_trigger",
                return_value=False,
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
                return_value=(False, 0),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_cycle_limit",
                return_value=(False, 1),
            ),
        ):
            action = DispatchRepairAction()
            result = action.execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.EXECUTE
        call_kwargs = provider.dispatch_repair.call_args.kwargs
        assert call_kwargs["repair_type"] == "review"
        assert call_kwargs["review_comments"] == [provider.list_review_comments.return_value[0]]

    def test_execute_dispatches_review_for_stuck_prior_threads(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=42,
            ci_status="passing",
            head_sha="head123",
            copilot_review_id=0,
            unresolved_threads=2,
            repairable_threads=2,
            reviews=[
                ReviewInfo(
                    id=11, user="Copilot", state="COMMENTED", commit_sha="old111", submitted_at="2024-01-01T10:00:00Z"
                ),
                ReviewInfo(
                    id=12,
                    user="Copilot",
                    state="CHANGES_REQUESTED",
                    commit_sha="old222",
                    submitted_at="2024-01-01T11:00:00Z",
                ),
            ],
            check_runs=[],
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()
        review_comment_a = MagicMock(id=101)
        review_comment_b = MagicMock(id=102)
        review_comment_b_duplicate = MagicMock(id=102)
        review_comment_suppressed_a = MagicMock(id=-1)
        review_comment_suppressed_b = MagicMock(id=-1)
        provider.list_review_comments.side_effect = [
            [review_comment_b, review_comment_suppressed_a],
            [review_comment_a, review_comment_b_duplicate, review_comment_suppressed_b],
        ]
        provider.dispatch_repair.return_value = 88

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.is_duplicate_trigger",
                return_value=False,
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
                return_value=(False, 0),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_cycle_limit",
                return_value=(False, 1),
            ),
        ):
            action = DispatchRepairAction()
            result = action.execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.EXECUTE
        call_kwargs = provider.dispatch_repair.call_args.kwargs
        assert call_kwargs["repair_type"] == "review"
        assert call_kwargs["review_id"] == 12
        assert call_kwargs["review_comments"] == [
            review_comment_b,
            review_comment_suppressed_a,
            review_comment_a,
            review_comment_suppressed_b,
        ]
        provider.list_review_comments.assert_any_call(42, 12)
        provider.list_review_comments.assert_any_call(42, 11)

    def test_execute_dispatches_verdict_review_when_it_is_the_only_repairable_provenance(self) -> None:
        verdict = CopilotGateVerdict(passed=False, reason=REASON_CONTENT_CHANGED, review_id=99)
        snapshot = PRStateSnapshot(
            pr_number=42,
            ci_status="passing",
            head_sha="head123",
            copilot_review_id=0,
            unresolved_threads=0,
            repairable_threads=1,
            copilot_gate_verdict=verdict,
            reviews=[
                ReviewInfo(
                    id=99,
                    user="Copilot",
                    state="COMMENTED",
                    commit_sha="old333",
                    submitted_at="2024-01-01T12:00:00Z",
                ),
            ],
            check_runs=[],
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()
        verdict_comment = MagicMock(id=203)
        provider.list_review_comments.return_value = [verdict_comment]
        provider.dispatch_repair.return_value = 88

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.is_duplicate_trigger",
                return_value=False,
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
                return_value=(False, 0),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_cycle_limit",
                return_value=(False, 1),
            ),
        ):
            result = DispatchRepairAction().execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.EXECUTE
        call_kwargs = provider.dispatch_repair.call_args.kwargs
        assert call_kwargs["repair_type"] == "review"
        assert call_kwargs["review_id"] == 99
        assert call_kwargs["review_comments"] == [verdict_comment]
        provider.list_review_comments.assert_called_once_with(42, 99)

    def test_execute_includes_verdict_review_comments_when_both_actionable_and_stuck_prior(self) -> None:
        """When review_actionable and stuck_prior_threads are both true, the verdict-owned review's
        comments must appear in the repair payload alongside the prior-review comments."""
        verdict = CopilotGateVerdict(passed=False, reason=REASON_HAS_COMMENTS, review_id=99)
        snapshot = PRStateSnapshot(
            pr_number=42,
            ci_status="passing",
            head_sha="head123",
            copilot_review_id=0,
            unresolved_threads=3,
            repairable_threads=3,
            copilot_gate_verdict=verdict,
            reviews=[
                ReviewInfo(
                    id=11, user="Copilot", state="COMMENTED", commit_sha="old111", submitted_at="2024-01-01T10:00:00Z"
                ),
                ReviewInfo(
                    id=12,
                    user="Copilot",
                    state="CHANGES_REQUESTED",
                    commit_sha="old222",
                    submitted_at="2024-01-01T11:00:00Z",
                ),
                ReviewInfo(
                    id=99,
                    user="Copilot",
                    state="COMMENTED",
                    commit_sha="old333",
                    submitted_at="2024-01-01T12:00:00Z",
                ),
            ],
            check_runs=[],
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()
        prior_comment_11 = MagicMock(id=201)
        prior_comment_12 = MagicMock(id=202)
        verdict_comment_99 = MagicMock(id=203)
        provider.list_review_comments.side_effect = [
            [prior_comment_12],
            [prior_comment_11],
            [verdict_comment_99],
        ]
        provider.dispatch_repair.return_value = 88

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.is_duplicate_trigger",
                return_value=False,
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
                return_value=(False, 0),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_cycle_limit",
                return_value=(False, 1),
            ),
        ):
            action = DispatchRepairAction()
            result = action.execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.EXECUTE
        call_kwargs = provider.dispatch_repair.call_args.kwargs
        assert call_kwargs["repair_type"] == "review"
        # review_context_id is the verdict review (99)
        assert call_kwargs["review_id"] == 99
        # All three reviews' comments must be present
        assert prior_comment_11 in call_kwargs["review_comments"]
        assert prior_comment_12 in call_kwargs["review_comments"]
        assert verdict_comment_99 in call_kwargs["review_comments"]
        provider.list_review_comments.assert_any_call(42, 11)
        provider.list_review_comments.assert_any_call(42, 12)
        provider.list_review_comments.assert_any_call(42, 99)

    def test_execute_stuck_prior_threads_uses_stable_order_for_missing_or_invalid_timestamps(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=42,
            ci_status="passing",
            head_sha="head123",
            copilot_review_id=0,
            unresolved_threads=2,
            repairable_threads=2,
            reviews=[
                ReviewInfo(id=11, user="Copilot", state="CHANGES_REQUESTED", commit_sha="old111", submitted_at=""),
                ReviewInfo(
                    id=12,
                    user="Copilot",
                    state="CHANGES_REQUESTED",
                    commit_sha="old222",
                    submitted_at=None,  # type: ignore[arg-type]
                ),
                ReviewInfo(
                    id=13,
                    user="Copilot",
                    state="CHANGES_REQUESTED",
                    commit_sha="old333",
                    submitted_at=123,  # type: ignore[arg-type]
                ),
            ],
            check_runs=[],
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider.list_review_comments.return_value = []
        provider.dispatch_repair.return_value = 89

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.is_duplicate_trigger",
                return_value=False,
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
                return_value=(False, 0),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_cycle_limit",
                return_value=(False, 1),
            ),
        ):
            action = DispatchRepairAction()
            result = action.execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.EXECUTE
        call_kwargs = provider.dispatch_repair.call_args.kwargs
        assert call_kwargs["review_id"] == 13

    def test_execute_skips_stuck_threads_when_review_id_dedup_matches_prior_review(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=42,
            ci_status="passing",
            head_sha="head123",
            copilot_review_id=0,
            unresolved_threads=2,
            repairable_threads=2,
            reviews=[
                ReviewInfo(id=12, user="Copilot", state="CHANGES_REQUESTED", commit_sha="old222"),
            ],
            check_runs=[],
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()

        with patch(
            "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.is_duplicate_trigger",
            return_value=True,
        ):
            action = DispatchRepairAction()
            result = action.execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.SKIP
        assert "12" in result.details
        provider.dispatch_repair.assert_not_called()

    def test_execute_stuck_prior_threads_uses_unresolved_thread_owner_for_dedup_and_context(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=42,
            ci_status="passing",
            head_sha="head123",
            copilot_review_id=0,
            unresolved_threads=0,
            repairable_threads=1,
            reviews=[
                ReviewInfo(
                    id=10,
                    user="Copilot",
                    state="COMMENTED",
                    commit_sha="old111",
                    submitted_at="2024-01-01T10:00:00Z",
                ),
                ReviewInfo(
                    id=11,
                    user="Copilot",
                    state="APPROVED",
                    commit_sha="old222",
                    submitted_at="2024-01-01T11:00:00Z",
                ),
            ],
            check_runs=[],
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()
        owner_comment = ReviewCommentInfo(id=101, path="a.py", body="owner unresolved", html_url="")
        newer_comment = ReviewCommentInfo(id=111, path="a.py", body="newer review, no thread", html_url="")
        provider.list_review_threads_by_thread_id.return_value = {"thread-1": (False, (101,))}
        provider.list_review_comments.side_effect = [
            [newer_comment],  # review 11
            [owner_comment],  # review 10
        ]
        provider.dispatch_repair.return_value = 123

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.is_duplicate_trigger",
                side_effect=lambda _provider, _pr, review_id: review_id == 11,
            ) as duplicate_mock,
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
                return_value=(False, 0),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_cycle_limit",
                return_value=(False, 1),
            ),
        ):
            result = DispatchRepairAction().execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.EXECUTE
        duplicate_mock.assert_called_once_with(provider, 42, 10)
        dispatch_kwargs = provider.dispatch_repair.call_args.kwargs
        assert dispatch_kwargs["review_id"] == 10
        assert dispatch_kwargs["review_comments"] == [owner_comment]

    def test_execute_stuck_prior_threads_dispatches_second_owner_when_first_is_already_marked(self) -> None:
        """Dispatch uses the next unmarked owner when the newest owner already has a marker."""
        snapshot = PRStateSnapshot(
            pr_number=42,
            ci_status="passing",
            head_sha="head123",
            copilot_review_id=0,
            unresolved_threads=0,
            repairable_threads=2,
            reviews=[
                ReviewInfo(
                    id=10,
                    user="Copilot",
                    state="COMMENTED",
                    commit_sha="old111",
                    submitted_at="2024-01-01T10:00:00Z",
                ),
                ReviewInfo(
                    id=20,
                    user="Copilot",
                    state="COMMENTED",
                    commit_sha="old222",
                    submitted_at="2024-01-01T12:00:00Z",
                ),
            ],
            check_runs=[],
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()
        comment_20 = ReviewCommentInfo(id=201, path="a.py", body="review 20 comment", html_url="")
        comment_10 = ReviewCommentInfo(id=101, path="b.py", body="review 10 comment", html_url="")
        # Both reviews own separate unresolved threads.
        provider.list_review_threads_by_thread_id.return_value = {
            "thread-1": (False, (201,)),
            "thread-2": (False, (101,)),
        }
        # Reviews are sorted newest-first (20 then 10), so list_review_comments is called in that order.
        provider.list_review_comments.side_effect = [
            [comment_20],  # review 20
            [comment_10],  # review 10
        ]
        provider.dispatch_repair.return_value = 123

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.is_duplicate_trigger",
                side_effect=lambda _provider, _pr, review_id: review_id == 20,
            ) as duplicate_mock,
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
                return_value=(False, 0),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_cycle_limit",
                return_value=(False, 1),
            ),
        ):
            result = DispatchRepairAction().execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.EXECUTE
        # Review 20 is checked first (newest-first order) → marked → review 10 checked next.
        assert duplicate_mock.call_count == 2
        assert duplicate_mock.call_args_list[0].args == (provider, 42, 20)
        assert duplicate_mock.call_args_list[1].args == (provider, 42, 10)
        dispatch_kwargs = provider.dispatch_repair.call_args.kwargs
        assert dispatch_kwargs["review_id"] == 10

    def test_execute_stuck_prior_threads_skips_when_all_owner_reviews_already_marked(self) -> None:
        """Dispatch is skipped when every repairable owner review already has a trigger marker."""
        snapshot = PRStateSnapshot(
            pr_number=42,
            ci_status="passing",
            head_sha="head123",
            copilot_review_id=0,
            unresolved_threads=0,
            repairable_threads=2,
            reviews=[
                ReviewInfo(
                    id=10,
                    user="Copilot",
                    state="COMMENTED",
                    commit_sha="old111",
                    submitted_at="2024-01-01T10:00:00Z",
                ),
                ReviewInfo(
                    id=20,
                    user="Copilot",
                    state="COMMENTED",
                    commit_sha="old222",
                    submitted_at="2024-01-01T12:00:00Z",
                ),
            ],
            check_runs=[],
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()
        comment_20 = ReviewCommentInfo(id=201, path="a.py", body="review 20 comment", html_url="")
        comment_10 = ReviewCommentInfo(id=101, path="b.py", body="review 10 comment", html_url="")
        provider.list_review_threads_by_thread_id.return_value = {
            "thread-1": (False, (201,)),
            "thread-2": (False, (101,)),
        }
        provider.list_review_comments.side_effect = [
            [comment_20],  # review 20
            [comment_10],  # review 10
        ]

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.is_duplicate_trigger",
                return_value=True,
            ) as duplicate_mock,
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
                return_value=(False, 0),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_cycle_limit",
                return_value=(False, 1),
            ),
        ):
            result = DispatchRepairAction().execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.SKIP
        assert "all repairable owner reviews" in result.details
        # Both owner reviews should have been checked before giving up.
        assert duplicate_mock.call_count == 2
        provider.dispatch_repair.assert_not_called()

    def test_execute_stuck_prior_threads_fails_open_when_dedup_check_raises_for_candidate(self) -> None:
        """When is_duplicate_trigger raises for the first candidate, dispatch proceeds fail-open with that candidate."""
        snapshot = PRStateSnapshot(
            pr_number=42,
            ci_status="passing",
            head_sha="head123",
            copilot_review_id=0,
            unresolved_threads=0,
            repairable_threads=2,
            reviews=[
                ReviewInfo(
                    id=10,
                    user="Copilot",
                    state="COMMENTED",
                    commit_sha="old111",
                    submitted_at="2024-01-01T10:00:00Z",
                ),
                ReviewInfo(
                    id=20,
                    user="Copilot",
                    state="COMMENTED",
                    commit_sha="old222",
                    submitted_at="2024-01-01T12:00:00Z",
                ),
            ],
            check_runs=[],
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()
        comment_20 = ReviewCommentInfo(id=201, path="a.py", body="review 20 comment", html_url="")
        comment_10 = ReviewCommentInfo(id=101, path="b.py", body="review 10 comment", html_url="")
        provider.list_review_threads_by_thread_id.return_value = {
            "thread-1": (False, (201,)),
            "thread-2": (False, (101,)),
        }
        provider.list_review_comments.side_effect = [
            [comment_20],  # review 20
            [comment_10],  # review 10
        ]
        provider.dispatch_repair.return_value = 123

        def _dedup_raises_for_20(_provider: object, _pr: int, review_id: int) -> bool:
            if review_id == 20:
                raise RuntimeError("API error")
            return False

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.is_duplicate_trigger",
                side_effect=_dedup_raises_for_20,
            ) as duplicate_mock,
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
                return_value=(False, 0),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_cycle_limit",
                return_value=(False, 1),
            ),
        ):
            result = DispatchRepairAction().execute(provider, snapshot, derived)

        # Fail-open: dispatch proceeds with the candidate whose check raised.
        assert result.decision == ActionDecision.EXECUTE
        # Only review 20 was checked before the exception triggered fail-open.
        duplicate_mock.assert_called_once_with(provider, 42, 20)
        dispatch_kwargs = provider.dispatch_repair.call_args.kwargs
        assert dispatch_kwargs["review_id"] == 20

    def test_execute_continues_when_review_comments_fetch_fails(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=42,
            ci_status="passing",
            head_sha="abc123",
            review_state="CHANGES_REQUESTED",
            copilot_review_id=12,
            check_runs=[],
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider.list_review_comments.side_effect = RuntimeError("comments boom")
        provider.dispatch_repair.return_value = 88

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.is_duplicate_trigger",
                return_value=False,
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
                return_value=(False, 0),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_cycle_limit",
                return_value=(False, 1),
            ),
        ):
            action = DispatchRepairAction()
            result = action.execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.EXECUTE
        assert provider.dispatch_repair.call_args.kwargs["review_comments"] == []

    def test_failed_when_dispatch_repair_raises(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=42,
            ci_status="failing",
            head_sha="abc123",
            check_runs=[],
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider.dispatch_repair.side_effect = RuntimeError("dispatch boom")

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
                return_value=(False, 0),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_cycle_limit",
                return_value=(False, 1),
            ),
        ):
            action = DispatchRepairAction()
            result = action.execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.FAILED
        assert "dispatch_repair call failed" in result.details

    def test_reraises_rate_limit_when_dispatch_repair_raises(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=42,
            ci_status="failing",
            head_sha="abc123",
            check_runs=[],
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider.dispatch_repair.side_effect = ProviderRateLimitError(
            provider="github",
            credential_identity="SPECKIT_PR_TOKEN",
        )

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
                return_value=(False, 0),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_cycle_limit",
                return_value=(False, 1),
            ),
        ):
            action = DispatchRepairAction()
            with pytest.raises(ProviderRateLimitError):
                action.execute(provider, snapshot, derived)

    def test_reraises_rate_limit_when_fetching_review_comments(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=42,
            ci_status="passing",
            head_sha="abc123",
            review_state="CHANGES_REQUESTED",
            copilot_review_id=12,
            check_runs=[],
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider.list_review_comments.side_effect = ProviderRateLimitError(
            provider="github",
            credential_identity="SPECKIT_PR_TOKEN",
            source="x-ratelimit-reset",
        )

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.is_duplicate_trigger",
                return_value=False,
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
                return_value=(False, 0),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_cycle_limit",
                return_value=(False, 1),
            ),
        ):
            action = DispatchRepairAction()
            with pytest.raises(ProviderRateLimitError):
                action.execute(provider, snapshot, derived)

    def test_execute_dispatches_both_when_ci_failing_and_review_actionable(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=42,
            ci_status="failing",
            head_sha="abc123",
            review_state="CHANGES_REQUESTED",
            copilot_review_id=12,
            check_runs=[],
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider.list_review_comments.return_value = [MagicMock(id=1)]
        provider.dispatch_repair.return_value = 99

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.is_duplicate_trigger",
                return_value=False,
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
                return_value=(False, 0),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_cycle_limit",
                return_value=(False, 1),
            ),
        ):
            action = DispatchRepairAction()
            result = action.execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.EXECUTE
        assert provider.dispatch_repair.call_args.kwargs["repair_type"] == "both"

    def test_execute_ci_failing_stale_review_not_blocked_by_review_id_dedup(self) -> None:
        """CI-failing repair is not blocked by stale-review dedup when effective review work is empty."""
        # The stale review (copilot_review_id=9000) already has a trigger marker, but
        # CI is failing.  Because effective review work is 0, review_context_id must be
        # cleared so the review-ID dedup path is bypassed and the CI repair proceeds.
        snapshot = PRStateSnapshot(
            pr_number=42,
            ci_status="failing",
            head_sha="abc123",
            review_state="CHANGES_REQUESTED",
            copilot_review_id=9000,
            copilot_review_inline_count=-1,
            effective_review_comment_count=0,
            effective_review_comment_count_review_id=9000,
            check_runs=[],
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider.dispatch_repair.return_value = 99

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.is_duplicate_trigger",
                return_value=True,  # stale review already has a trigger marker
            ) as mock_dedup,
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
                return_value=(False, 0),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_cycle_limit",
                return_value=(False, 1),
            ),
        ):
            result = DispatchRepairAction().execute(provider, snapshot, derived)

        # review_context_id is 0 (cleared), so is_duplicate_trigger is never called
        assert result.decision == ActionDecision.EXECUTE
        mock_dedup.assert_not_called()

    def test_execute_ci_failing_stale_review_dispatches_without_review_id(self) -> None:
        """CI-only dispatch does not attach a stale review ID when effective review work is empty."""
        snapshot = PRStateSnapshot(
            pr_number=42,
            ci_status="failing",
            head_sha="sha999",
            review_state="CHANGES_REQUESTED",
            copilot_review_id=7777,
            copilot_review_inline_count=-1,
            effective_review_comment_count=0,
            effective_review_comment_count_review_id=7777,
            check_runs=[],
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider.dispatch_repair.return_value = 55

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.is_duplicate_trigger",
                return_value=False,
            ) as mock_dedup,
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
                return_value=(False, 0),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_cycle_limit",
                return_value=(False, 1),
            ),
        ):
            result = DispatchRepairAction().execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.EXECUTE
        # review_context_id=0 → review-ID dedup is never invoked
        mock_dedup.assert_not_called()
        # dispatch_repair should be called with repair_type="ci" and review_id=0 (no stale review)
        call_kwargs = provider.dispatch_repair.call_args.kwargs
        assert call_kwargs.get("review_id", 0) == 0

    def test_execute_when_duplicate_trigger_exists_for_review_id(self) -> None:
        """FR-012: Duplicate trigger for same review_id is treated as already dispatched."""
        snapshot = PRStateSnapshot(
            pr_number=42,
            ci_status="passing",
            head_sha="abc123",
            review_state="CHANGES_REQUESTED",
            copilot_review_id=4401589029,
            check_runs=[],
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()

        with patch(
            "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.is_duplicate_trigger",
            return_value=True,
        ):
            action = DispatchRepairAction()
            result = action.execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.SKIP
        assert "review_id=4401589029" in result.details
        assert getattr(derived, "repair_dispatched", False) is False
        provider.dispatch_repair.assert_not_called()

    def test_execute_when_review_id_dedup_check_raises_fail_open(self) -> None:
        """Review-ID dedup check failure proceeds fail-open (dispatches anyway)."""
        snapshot = PRStateSnapshot(
            pr_number=42,
            ci_status="passing",
            head_sha="abc123",
            review_state="CHANGES_REQUESTED",
            copilot_review_id=100,
            check_runs=[],
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()
        # Provide a non-CCA review comment so the re-evaluation guard does not
        # short-circuit execution before the dedup fail-open path is reached.
        provider.list_review_comments.return_value = [MagicMock(id=101)]
        provider.dispatch_repair.return_value = 200

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.is_duplicate_trigger",
                side_effect=RuntimeError("API error"),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
                return_value=(False, 0),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_cycle_limit",
                return_value=(False, 1),
            ),
        ):
            action = DispatchRepairAction()
            result = action.execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.EXECUTE
        provider.dispatch_repair.assert_called_once()

    def test_exclusion_context_filters_review_comments(self) -> None:
        """ExclusionContext filters out already-applied comments from dispatch."""
        from agentic_devtools.cli.ci.pipeline.exclusion import ExclusionContext

        snapshot = PRStateSnapshot(
            pr_number=1,
            ci_status="failing",
            head_sha="abc123",
            review_state="CHANGES_REQUESTED",
            copilot_review_id=100,
            copilot_review_inline_count=3,
            check_runs=[],
        )
        derived = DerivedState(snapshot)
        exclusion_ctx = ExclusionContext(resolved_comment_ids={101, 102})
        derived.set("exclusion_context", exclusion_ctx)

        provider = MagicMock()
        provider.list_review_comments.return_value = [
            MagicMock(id=101),
            MagicMock(id=102),
            MagicMock(id=103),
        ]
        provider.dispatch_repair.return_value = 999

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.is_duplicate_trigger",
                return_value=False,
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
                return_value=(False, 0),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_cycle_limit",
                return_value=(False, 1),
            ),
        ):
            action = DispatchRepairAction()
            result = action.execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.EXECUTE
        call_kwargs = provider.dispatch_repair.call_args
        review_comments = call_kwargs.kwargs.get("review_comments") or call_kwargs[0][4]
        assert len(review_comments) == 1

    def test_exclusion_context_skips_repair_when_all_excluded_ci_passing(self) -> None:
        """SKIP when all review comments excluded and CI is passing."""
        from agentic_devtools.cli.ci.pipeline.exclusion import ExclusionContext

        snapshot = PRStateSnapshot(
            pr_number=1,
            ci_status="passing",
            head_sha="abc123",
            review_state="CHANGES_REQUESTED",
            copilot_review_id=100,
            copilot_review_inline_count=2,
            check_runs=[],
        )
        derived = DerivedState(snapshot)
        exclusion_ctx = ExclusionContext(resolved_comment_ids={101, 102})
        derived.set("exclusion_context", exclusion_ctx)

        provider = MagicMock()
        provider.list_review_comments.return_value = [
            MagicMock(id=101),
            MagicMock(id=102),
        ]

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.is_duplicate_trigger",
                return_value=False,
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
                return_value=(False, 0),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_cycle_limit",
                return_value=(False, 1),
            ),
        ):
            action = DispatchRepairAction()
            result = action.execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.SKIP
        assert "auto-applied" in result.details.lower()

    def test_exclusion_context_does_not_skip_declared_shortfall_when_all_inline_comments_are_excluded(self) -> None:
        """Declared suppressed findings must still dispatch a shortfall notice."""
        from agentic_devtools.cli.ci.pipeline.exclusion import ExclusionContext

        snapshot = PRStateSnapshot(
            pr_number=1,
            ci_status="passing",
            head_sha="abc123",
            review_state="CHANGES_REQUESTED",
            copilot_review_id=100,
            copilot_review_inline_count=2,
            reviews=[
                ReviewInfo(
                    id=100,
                    user="Copilot",
                    state="CHANGES_REQUESTED",
                    body="### Comments suppressed due to low confidence (2)\n\nreview body",
                )
            ],
            check_runs=[],
        )
        derived = DerivedState(snapshot)
        exclusion_ctx = ExclusionContext(resolved_comment_ids={101, 102})
        derived.set("exclusion_context", exclusion_ctx)

        provider = MagicMock()
        provider.list_review_comments.return_value = [
            MagicMock(id=101),
            MagicMock(id=102),
        ]
        provider.dispatch_repair.return_value = 999

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.is_duplicate_trigger",
                return_value=False,
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
                return_value=(False, 0),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_cycle_limit",
                return_value=(False, 1),
            ),
        ):
            action = DispatchRepairAction()
            result = action.execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.EXECUTE
        call_kwargs = provider.dispatch_repair.call_args.kwargs
        assert call_kwargs["review_comments"] == []
        assert call_kwargs["declared_author_comment_count"] == 2
        assert call_kwargs["declared_author_comment_counts_by_review"] == {100: 2}

    def test_exclusion_context_no_matching_ids_still_dispatches(self) -> None:
        """Dispatch when exclusion context IDs don't match any review comments."""
        from agentic_devtools.cli.ci.pipeline.exclusion import ExclusionContext

        snapshot = PRStateSnapshot(
            pr_number=1,
            ci_status="passing",
            head_sha="abc123",
            review_state="CHANGES_REQUESTED",
            copilot_review_id=100,
            copilot_review_inline_count=2,
            check_runs=[],
        )
        derived = DerivedState(snapshot)
        # Exclusion context has IDs that don't match actual review comments
        exclusion_ctx = ExclusionContext(resolved_comment_ids={999, 998})
        derived.set("exclusion_context", exclusion_ctx)

        provider = MagicMock()
        provider.list_review_comments.return_value = [
            MagicMock(id=101),
            MagicMock(id=102),
        ]
        provider.dispatch_repair.return_value = 999

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.is_duplicate_trigger",
                return_value=False,
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
                return_value=(False, 0),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_cycle_limit",
                return_value=(False, 1),
            ),
        ):
            action = DispatchRepairAction()
            result = action.execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.EXECUTE

    def test_exclusion_context_does_not_skip_when_ci_unknown(self) -> None:
        """Do not SKIP on unknown CI status even when all review comments are excluded."""
        from agentic_devtools.cli.ci.pipeline.exclusion import ExclusionContext

        snapshot = PRStateSnapshot(
            pr_number=1,
            ci_status="unknown",
            head_sha="abc123",
            review_state="CHANGES_REQUESTED",
            copilot_review_id=100,
            copilot_review_inline_count=2,
            check_runs=[],
        )
        derived = DerivedState(snapshot)
        exclusion_ctx = ExclusionContext(resolved_comment_ids={101, 102})
        derived.set("exclusion_context", exclusion_ctx)

        provider = MagicMock()
        provider.list_review_comments.return_value = [
            MagicMock(id=101),
            MagicMock(id=102),
        ]
        provider.dispatch_repair.return_value = 999

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.is_duplicate_trigger",
                return_value=False,
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
                return_value=(False, 0),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_cycle_limit",
                return_value=(False, 1),
            ),
        ):
            action = DispatchRepairAction()
            result = action.execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.EXECUTE
        provider.dispatch_repair.assert_called_once()


class TestDispatchRepairDeferralCheck:
    """Tests for deferral marker check in execute."""

    def test_skips_dispatch_when_active_deferral_marker(self) -> None:
        """Lines 138-147: active deferral marker causes skip."""
        snapshot = PRStateSnapshot(
            pr_number=1,
            ci_status="failing",
            copilot_review_id=100,
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.deferral.read_active_deferral",
                return_value={"review_id": "100", "active": True},
            ),
            patch("agentic_devtools.cli.ci.pipeline.deferral.deactivate_deferral_marker") as mock_deactivate,
        ):
            action = DispatchRepairAction()
            result = action.execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.SKIP
        assert "Deferred" in result.details
        mock_deactivate.assert_called_once_with(provider, 1, 100)

    def test_proceeds_when_no_active_deferral_marker(self) -> None:
        """Branch 138->162: no active deferral, falls through to normal flow."""
        snapshot = PRStateSnapshot(
            pr_number=1,
            ci_status="failing",
            copilot_review_id=100,
            review_state="CHANGES_REQUESTED",
            reviews=[
                ReviewInfo(id=100, user="Copilot", state="CHANGES_REQUESTED"),
            ],
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider.find_comment.return_value = (None, None)

        with patch(
            "agentic_devtools.cli.ci.pipeline.deferral.read_active_deferral",
            return_value=None,
        ):
            action = DispatchRepairAction()
            result = action.execute(provider, snapshot, derived)

        # Should proceed past deferral check (not SKIP due to deferral)
        assert "Deferred" not in result.details

    def test_proceeds_when_deferral_marker_cannot_be_deactivated(self) -> None:
        """Failed deferral consumption must not stall repair dispatch."""
        snapshot = PRStateSnapshot(
            pr_number=42,
            ci_status="failing",
            head_sha="abc123",
            copilot_review_id=100,
            check_runs=[],
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider.dispatch_repair.return_value = 999

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.deferral.read_active_deferral",
                return_value={"review_id": "100", "active": True},
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.deferral.deactivate_deferral_marker",
                return_value=False,
            ),
            patch("agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.logger.warning") as mock_warning,
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
                return_value=(False, 0),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_cycle_limit",
                return_value=(False, 1),
            ),
        ):
            action = DispatchRepairAction()
            result = action.execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.EXECUTE
        provider.dispatch_repair.assert_called_once()
        mock_warning.assert_called_once()

    def test_proceeds_when_deferral_check_raises(self) -> None:
        """Deferral lookup failures log a warning and do not block dispatch."""
        snapshot = PRStateSnapshot(
            pr_number=42,
            ci_status="failing",
            head_sha="abc123",
            copilot_review_id=100,
            check_runs=[],
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider.dispatch_repair.return_value = 999

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.deferral.read_active_deferral",
                side_effect=RuntimeError("boom"),
            ),
            patch("agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.logger.warning") as mock_warning,
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
                return_value=(False, 0),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_cycle_limit",
                return_value=(False, 1),
            ),
        ):
            action = DispatchRepairAction()
            result = action.execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.EXECUTE
        provider.dispatch_repair.assert_called_once()
        mock_warning.assert_called_once()


class TestDispatchRepairNewCcrActionability:
    """A content-blocking gate verdict makes a 0-inline COMMENTED review actionable.

    Guards the new-CCR-format gap: a "Not ready to approve" verdict heading or
    body-only suppressed comments block the gate while exposing no inline
    comments through the API. Such a PR must still trigger repair (otherwise it
    is blocked forever), while freshness reasons must NOT trigger repair.
    """

    def _snapshot(self, verdict: CopilotGateVerdict | None) -> PRStateSnapshot:
        return PRStateSnapshot(
            pr_number=1,
            ci_status="passing",
            active_session=False,
            review_state="COMMENTED",
            copilot_review_id=100,
            copilot_review_inline_count=0,
            copilot_gate_verdict=verdict,
        )

    def _evaluate(self, verdict: CopilotGateVerdict | None):
        snapshot = self._snapshot(verdict)
        return DispatchRepairAction().evaluate(snapshot, DerivedState(snapshot))

    def test_execute_new_ccr_not_approved_zero_inline(self) -> None:
        """'Not ready to approve' with 0 inline comments is actionable."""
        verdict = CopilotGateVerdict(passed=False, reason=REASON_NEW_CCR_NOT_APPROVED, review_id=100)
        result = self._evaluate(verdict)
        assert result.decision == ActionDecision.EXECUTE
        assert result.preconditions["review_actionable"] is True

    def test_execute_suppressed_comments_zero_inline(self) -> None:
        """Body-only suppressed comments (0 inline) are actionable."""
        verdict = CopilotGateVerdict(passed=False, reason=REASON_SUPPRESSED_COMMENTS, review_id=100, suppressed_count=8)
        result = self._evaluate(verdict)
        assert result.decision == ActionDecision.EXECUTE
        assert result.preconditions["review_actionable"] is True

    def test_execute_has_comments_zero_inline(self) -> None:
        """A body reporting posted comments (0 inline via API) is actionable."""
        verdict = CopilotGateVerdict(passed=False, reason=REASON_HAS_COMMENTS, review_id=100, body_comment_count=3)
        result = self._evaluate(verdict)
        assert result.decision == ActionDecision.EXECUTE
        assert result.preconditions["review_actionable"] is True

    def test_execute_has_comments_when_empty_inventory_has_no_filter_evidence(self) -> None:
        """A positive body count with an unfiltered empty inventory remains actionable."""
        verdict = CopilotGateVerdict(passed=False, reason=REASON_HAS_COMMENTS, review_id=100, body_comment_count=3)
        snapshot = replace(
            self._snapshot(verdict),
            effective_review_comment_count=0,
            effective_review_comment_count_review_id=100,
            effective_review_comment_filter_applied=False,
        )

        result = DispatchRepairAction().evaluate(snapshot, DerivedState(snapshot))

        assert result.decision == ActionDecision.EXECUTE
        assert result.preconditions["effective_review_work"] is True

    def test_skip_when_gate_verdict_passed(self) -> None:
        """A clean (passed) verdict is not actionable."""
        verdict = CopilotGateVerdict(passed=True, reason=REASON_CLEAN, review_id=100)
        result = self._evaluate(verdict)
        assert result.decision == ActionDecision.SKIP
        assert result.preconditions["review_actionable"] is False

    def test_skip_when_freshness_reason_content_changed(self) -> None:
        """Content-changed is a freshness reason — needs a new review, not repair."""
        verdict = CopilotGateVerdict(passed=False, reason=REASON_CONTENT_CHANGED, review_id=100)
        result = self._evaluate(verdict)
        assert result.decision == ActionDecision.SKIP
        assert result.preconditions["review_actionable"] is False

    def test_skip_when_freshness_reason_awaiting_fresh(self) -> None:
        """Awaiting-fresh is a freshness reason — needs a new review, not repair."""
        verdict = CopilotGateVerdict(passed=False, reason=REASON_AWAITING_FRESH, review_id=100)
        result = self._evaluate(verdict)
        assert result.decision == ActionDecision.SKIP
        assert result.preconditions["review_actionable"] is False

    def test_execute_when_review_id_differs_from_head(self) -> None:
        """A blocking verdict whose review id differs from copilot_review_id is actionable.

        The effective review the gate evaluated may be a prior-commit review selected
        by diff-hash freshness (whose id differs from ``copilot_review_id``), so the
        widened, identity-agnostic actionability must still dispatch a repair.
        """
        verdict = CopilotGateVerdict(passed=False, reason=REASON_NEW_CCR_NOT_APPROVED, review_id=999)
        result = self._evaluate(verdict)
        assert result.decision == ActionDecision.EXECUTE
        assert result.preconditions["review_actionable"] is True

    def test_execute_suppressed_only_approved_state_is_actionable(self) -> None:
        """A suppressed-only review submitted as APPROVED is actionable (state-agnostic)."""
        verdict = CopilotGateVerdict(passed=False, reason=REASON_SUPPRESSED_COMMENTS, review_id=100, suppressed_count=2)
        snapshot = PRStateSnapshot(
            pr_number=1,
            ci_status="passing",
            review_state="APPROVED",
            copilot_review_id=100,
            copilot_review_inline_count=0,
            copilot_gate_verdict=verdict,
        )
        result = DispatchRepairAction().evaluate(snapshot, DerivedState(snapshot))
        assert result.decision == ActionDecision.EXECUTE
        assert result.preconditions["review_actionable"] is True

    def test_execute_new_ccr_not_approved_approved_state_is_actionable(self) -> None:
        """A new-CCR 'Not ready to approve' submitted as APPROVED is actionable (state-agnostic)."""
        verdict = CopilotGateVerdict(
            passed=False,
            reason=REASON_NEW_CCR_NOT_APPROVED,
            review_id=100,
            body_comment_count=0,
            suppressed_count=1,
        )
        snapshot = PRStateSnapshot(
            pr_number=1,
            ci_status="passing",
            review_state="APPROVED",
            copilot_review_id=100,
            copilot_review_inline_count=0,
            copilot_gate_verdict=verdict,
        )
        result = DispatchRepairAction().evaluate(snapshot, DerivedState(snapshot))
        assert result.decision == ActionDecision.EXECUTE
        assert result.preconditions["review_actionable"] is True

    def test_execute_unparsed_suppression_is_actionable(self) -> None:
        """A REASON_UNPARSED_SUPPRESSION gate verdict (zero recovered entries) is actionable.

        Without this, a body-only COMMENTED review that declares suppressed
        comments but whose entries could not be parsed would never trigger
        repair — preserving the exact permanent stall this PR is intended to fix.
        """
        verdict = CopilotGateVerdict(
            passed=False, reason=REASON_UNPARSED_SUPPRESSION, review_id=100, suppressed_count=0
        )
        snapshot = PRStateSnapshot(
            pr_number=1,
            ci_status="passing",
            review_state="COMMENTED",
            copilot_review_id=100,
            copilot_review_inline_count=0,
            copilot_gate_verdict=verdict,
        )
        result = DispatchRepairAction().evaluate(snapshot, DerivedState(snapshot))
        assert result.decision == ActionDecision.EXECUTE
        assert result.preconditions["review_actionable"] is True

    def test_execute_dispatches_review_repair_for_effective_review_id(self) -> None:
        """A suppressed-only APPROVED review with a mismatching id dispatches a 'review' repair.

        The repair (and its review-comment fetch) must target the gate's effective
        review id (999), not ``copilot_review_id`` (100).
        """
        verdict = CopilotGateVerdict(passed=False, reason=REASON_SUPPRESSED_COMMENTS, review_id=999, suppressed_count=3)
        snapshot = PRStateSnapshot(
            pr_number=42,
            ci_status="passing",
            head_sha="abc123",
            review_state="APPROVED",
            copilot_review_id=100,
            copilot_review_inline_count=0,
            copilot_gate_verdict=verdict,
            check_runs=[],
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider.list_review_comments.return_value = [MagicMock(id=-1)]
        provider.dispatch_repair.return_value = 77

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.is_duplicate_trigger",
                return_value=False,
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
                return_value=(False, 0),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_cycle_limit",
                return_value=(False, 1),
            ),
        ):
            result = DispatchRepairAction().execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.EXECUTE
        call_kwargs = provider.dispatch_repair.call_args.kwargs
        assert call_kwargs["repair_type"] == "review"
        assert call_kwargs["review_id"] == 999
        provider.list_review_comments.assert_called_once_with(42, 999)

    def test_skip_when_duplicate_trigger_for_effective_review_id(self) -> None:
        """The per-review-id dedup guard still prevents repeated dispatch on the widened path."""
        verdict = CopilotGateVerdict(passed=False, reason=REASON_SUPPRESSED_COMMENTS, review_id=999, suppressed_count=3)
        snapshot = PRStateSnapshot(
            pr_number=42,
            ci_status="passing",
            head_sha="abc123",
            review_state="APPROVED",
            copilot_review_id=100,
            copilot_review_inline_count=0,
            copilot_gate_verdict=verdict,
            check_runs=[],
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.is_duplicate_trigger",
                return_value=True,
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
                return_value=(False, 0),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_cycle_limit",
                return_value=(False, 1),
            ),
        ):
            result = DispatchRepairAction().execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.SKIP
        assert "review_id=999" in result.details
        provider.dispatch_repair.assert_not_called()

    def test_execute_new_ccr_not_approved_positive_body_comment_count(self) -> None:
        """New CCR not-approve with body_comment_count > 0 is still actionable via content-blocking path."""
        verdict = CopilotGateVerdict(
            passed=False, reason=REASON_NEW_CCR_NOT_APPROVED, review_id=100, body_comment_count=3
        )
        result = self._evaluate(verdict)
        assert result.decision == ActionDecision.EXECUTE
        assert result.preconditions["review_actionable"] is True


class TestDispatchRepairSuppressedDeferralCheck:
    """Tests for the read-only suppressed-comment deferral check in execute."""

    @staticmethod
    def _suppressed_snapshot(
        *,
        ci_status: str = "passing",
        copilot_review_id: int = 0,
        head_sha: str = "",
        unresolved_threads: int = 0,
        repairable_threads: int = 0,
        reviews: list[ReviewInfo] | None = None,
    ) -> PRStateSnapshot:
        return PRStateSnapshot(
            pr_number=1,
            ci_status=ci_status,
            head_sha=head_sha,
            copilot_review_id=copilot_review_id,
            unresolved_threads=unresolved_threads,
            repairable_threads=repairable_threads,
            reviews=reviews or [],
            copilot_gate_verdict=CopilotGateVerdict(
                passed=False,
                reason=REASON_SUPPRESSED_COMMENTS,
                review_id=100,
                body_comment_count=0,
                suppressed_count=2,
            ),
        )

    def test_skips_dispatch_when_suppressed_deferral_is_recorded(self) -> None:
        snapshot = self._suppressed_snapshot()
        derived = DerivedState(snapshot)
        provider = MagicMock()

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.deferral.read_active_deferral",
                return_value=None,
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.read_active_suppressed_deferral",
                return_value={"review_id": "100", "issue": 4242, "active": True},
            ),
        ):
            result = DispatchRepairAction().execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.SKIP
        assert "triage issue" in result.details
        provider.dispatch_repair.assert_not_called()

    def test_does_not_skip_ci_repair_when_suppressed_deferral_is_recorded(self) -> None:
        snapshot = self._suppressed_snapshot(ci_status="failing")
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider.dispatch_repair.return_value = 777

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.deferral.read_active_deferral",
                return_value=None,
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.read_active_suppressed_deferral",
                return_value={"review_id": "100", "issue": 4242, "active": True},
            ) as mock_read,
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
                return_value=(False, 0),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_cycle_limit",
                return_value=(False, 1),
            ),
        ):
            result = DispatchRepairAction().execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.EXECUTE
        mock_read.assert_not_called()
        provider.dispatch_repair.assert_called_once()

    def test_does_not_skip_stuck_prior_threads_when_suppressed_deferral_is_recorded(self) -> None:
        snapshot = self._suppressed_snapshot(
            copilot_review_id=0,
            unresolved_threads=2,
            repairable_threads=2,
            head_sha="head123",
            reviews=[ReviewInfo(id=10, user="Copilot", state="CHANGES_REQUESTED", commit_sha="old123")],
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider.dispatch_repair.return_value = 888

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.deferral.read_active_deferral",
                return_value=None,
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.read_active_suppressed_deferral",
                return_value={"review_id": "100", "issue": 4242, "active": True},
            ) as mock_read,
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
                return_value=(False, 0),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_cycle_limit",
                return_value=(False, 1),
            ),
        ):
            result = DispatchRepairAction().execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.EXECUTE
        mock_read.assert_not_called()
        provider.dispatch_repair.assert_called_once()

    def test_marker_is_never_consumed(self) -> None:
        """The suppressed marker is durable evidence — it must not be deactivated."""
        snapshot = self._suppressed_snapshot()
        derived = DerivedState(snapshot)

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.deferral.read_active_deferral",
                return_value=None,
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.read_active_suppressed_deferral",
                return_value={"review_id": "100", "active": True},
            ),
            patch("agentic_devtools.cli.ci.pipeline.deferral.deactivate_deferral_marker") as mock_deactivate,
        ):
            DispatchRepairAction().execute(MagicMock(), snapshot, derived)

        mock_deactivate.assert_not_called()

    def test_autofix_marker_is_still_consumed_when_deferral_exists(self) -> None:
        snapshot = self._suppressed_snapshot(copilot_review_id=100)
        derived = DerivedState(snapshot)
        provider = MagicMock()

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.deferral.read_active_deferral",
                return_value={"review_id": "100", "active": True},
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.deferral.deactivate_deferral_marker",
                return_value=True,
            ) as mock_deactivate,
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.read_active_suppressed_deferral",
                return_value={"review_id": "100", "active": True},
            ),
        ):
            result = DispatchRepairAction().execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.SKIP
        mock_deactivate.assert_called_once_with(provider, 1, 100)

    def test_proceeds_when_deferral_check_raises(self) -> None:
        """Fail-open: an unreadable marker must not stall repair dispatch."""
        snapshot = self._suppressed_snapshot()
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider.find_comment.return_value = (None, None)

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.deferral.read_active_deferral",
                return_value=None,
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.read_active_suppressed_deferral",
                side_effect=RuntimeError("API down"),
            ),
        ):
            result = DispatchRepairAction().execute(provider, snapshot, derived)

        assert "triage issue" not in result.details

    def test_no_deferral_check_without_actionable_review(self) -> None:
        snapshot = PRStateSnapshot(pr_number=1, ci_status="failing")
        derived = DerivedState(snapshot)

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.deferral.read_active_deferral",
                return_value=None,
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.read_active_suppressed_deferral",
            ) as mock_read,
        ):
            DispatchRepairAction().execute(MagicMock(), snapshot, derived)

        mock_read.assert_not_called()

    def test_declared_suppressed_count_is_passed_to_the_dispatch(self) -> None:
        """The gate blocks on the declared count, so the dispatch must carry it."""
        snapshot = PRStateSnapshot(
            pr_number=42,
            ci_status="passing",
            head_sha="abc123",
            review_state="CHANGES_REQUESTED",
            copilot_review_id=12,
            reviews=[
                ReviewInfo(
                    id=12,
                    user="Copilot",
                    state="CHANGES_REQUESTED",
                    body="### Comments suppressed due to low confidence (4)\n\nprose",
                )
            ],
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider.list_review_comments.return_value = []
        provider.dispatch_repair.return_value = 77

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.is_duplicate_trigger",
                return_value=False,
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
                return_value=(False, 0),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_cycle_limit",
                return_value=(False, 1),
            ),
        ):
            action = DispatchRepairAction()
            action.execute(provider, snapshot, derived)

        assert provider.dispatch_repair.call_args.kwargs["declared_author_comment_count"] == 4
        assert provider.dispatch_repair.call_args.kwargs["declared_author_comment_counts_by_review"] == {12: 4}

    def test_declared_suppressed_counts_are_preserved_per_prior_review(self) -> None:
        """Stuck prior threads must carry a per-review shortfall map, not just an aggregate total."""
        snapshot = PRStateSnapshot(
            pr_number=42,
            ci_status="passing",
            head_sha="head123",
            copilot_review_id=0,
            unresolved_threads=2,
            repairable_threads=2,
            reviews=[
                ReviewInfo(
                    id=11,
                    user="Copilot",
                    state="CHANGES_REQUESTED",
                    commit_sha="old111",
                    submitted_at="2024-01-01T10:00:00Z",
                    body="### Comments suppressed due to low confidence (1)\n\nolder review",
                ),
                ReviewInfo(
                    id=12,
                    user="Copilot",
                    state="CHANGES_REQUESTED",
                    commit_sha="old222",
                    submitted_at="2024-01-01T11:00:00Z",
                    body="### Comments suppressed due to low confidence (2)\n\nnewer review",
                ),
            ],
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider.list_review_comments.return_value = []
        provider.dispatch_repair.return_value = 77

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.is_duplicate_trigger",
                return_value=False,
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
                return_value=(False, 0),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_cycle_limit",
                return_value=(False, 1),
            ),
        ):
            action = DispatchRepairAction()
            action.execute(provider, snapshot, derived)

        call_kwargs = provider.dispatch_repair.call_args.kwargs
        assert call_kwargs["declared_author_comment_count"] == 3
        assert call_kwargs["declared_author_comment_counts_by_review"] == {12: 2, 11: 1}

    def test_declared_suppressed_count_is_zero_for_a_ci_only_dispatch(self) -> None:
        """No review context means no declared count to plumb."""
        snapshot = PRStateSnapshot(pr_number=42, ci_status="failing", head_sha="abc123")
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider.dispatch_repair.return_value = 77

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
                return_value=(False, 0),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_cycle_limit",
                return_value=(False, 1),
            ),
        ):
            action = DispatchRepairAction()
            action.execute(provider, snapshot, derived)

        assert provider.dispatch_repair.call_args.kwargs["declared_author_comment_count"] == 0
        assert provider.dispatch_repair.call_args.kwargs["declared_author_comment_counts_by_review"] == {}
