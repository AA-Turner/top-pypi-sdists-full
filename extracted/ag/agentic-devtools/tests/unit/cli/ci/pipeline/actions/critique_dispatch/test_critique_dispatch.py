"""Tests for critique dispatch eligibility and task markers."""

from collections.abc import Iterator
from dataclasses import replace
from unittest.mock import MagicMock, patch

import pytest

from agentic_devtools.cli.ci.models import COPILOT_REVIEWER_LOGIN, IssueCommentInfo, ReviewCommentInfo, ReviewInfo
from agentic_devtools.cli.ci.pipeline.actions import critique_dispatch
from agentic_devtools.cli.ci.pipeline.actions.approve import ApproveAction
from agentic_devtools.cli.ci.pipeline.actions.dispatch_repair import DispatchRepairAction
from agentic_devtools.cli.ci.pipeline.gate_verdict import REASON_NEW_CCR_NOT_APPROVED, CopilotGateVerdict
from agentic_devtools.cli.ci.pipeline.models import ActionDecision
from agentic_devtools.cli.ci.pipeline.repair_attempts import RepairAttemptTracker
from agentic_devtools.cli.ci.pipeline.snapshot_models import DerivedState, PRStateSnapshot
from agentic_devtools.cli.ci.provider import RepairDispatchNotAttemptedError


@pytest.fixture(autouse=True)
def _mock_inactive_session_detector() -> Iterator[None]:
    """Default all tests to known-inactive session inventory."""
    with (
        patch(
            "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.is_copilot_session_active_via_agent_task",
            return_value=False,
        ),
        patch("agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.RepairDispatchLedger.begin"),
        patch("agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.RepairDispatchLedger.record"),
        patch("agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.RepairDispatchLedger.reconcile"),
    ):
        yield


@pytest.fixture(autouse=True)
def _valid_provider_evidence() -> Iterator[None]:
    """Provide in-memory task markers for critique dispatch tests."""
    mock_type = MagicMock

    def configured_mock(*args, **kwargs):
        if "id" in kwargs:
            return ReviewCommentInfo(
                id=kwargs["id"],
                path=kwargs.get("path", ""),
                body=kwargs.get("body", ""),
                html_url=kwargs.get("html_url", ""),
                source_review_id=kwargs.get("source_review_id", 0),
                author_login=kwargs.get("author_login", ""),
                in_reply_to_id=kwargs.get("in_reply_to_id"),
            )
        provider = mock_type(*args, **kwargs)
        stored: dict[int, str] = {}

        def find_comment(pr_number: int, marker: str):
            return next(((key, body) for key, body in stored.items() if marker in body), None)

        def list_issue_comments(pr_number: int) -> list[IssueCommentInfo]:
            return [
                IssueCommentInfo(id=comment_id, author="github-actions[bot]", body=body)
                for comment_id, body in stored.items()
            ]

        def post_comment(pr_number: int, body: str) -> int:
            key = len(stored) + 1
            stored[key] = body
            return key

        def update_comment(comment_id: int, body: str) -> None:
            stored[comment_id] = body

        provider.find_comment.side_effect = find_comment
        provider.get_pr_token_login.return_value = "github-actions[bot]"
        provider.list_issue_comments.side_effect = list_issue_comments
        provider.list_review_comments.return_value = []
        provider.list_review_thread_states.return_value = {}
        provider.post_comment.side_effect = post_comment
        provider.post_comment_as_pr_token.side_effect = post_comment
        provider.update_comment.side_effect = update_comment
        provider.update_comment_as_pr_token.side_effect = update_comment
        return provider

    with patch(__name__ + ".MagicMock", side_effect=configured_mock):
        yield


class TestCritiqueDispatchIntegration:
    """Test critique-specific dispatch behavior through the action boundary."""

    def _zero_finding_overview_snapshot(
        self,
        body: str,
        *,
        head_sha: str = "head",
        classification: str = "critique",
    ) -> PRStateSnapshot:
        review = ReviewInfo(
            id=100,
            user=COPILOT_REVIEWER_LOGIN,
            state="COMMENTED",
            body=body,
            commit_sha=head_sha,
            submitted_at="2026-10-19T12:00:00Z",
        )
        return PRStateSnapshot(
            pr_number=42,
            base_repo_full_name="owner/repo",
            head_sha="head",
            ci_status="passing",
            review_state="APPROVED",
            copilot_review_id=100,
            copilot_review_inline_count=0,
            effective_review_comment_count=0,
            effective_review_comment_count_review_id=100,
            effective_review_comment_filter_applied=False,
            critique_headline_classification=classification,
            reviews=[review],
            copilot_gate_verdict=CopilotGateVerdict(
                passed=False,
                reason=REASON_NEW_CCR_NOT_APPROVED,
                review_id=100,
                body_comment_count=0,
            ),
        )

    def test_critique_headline_dispatches_exact_prompt_and_skips_approval(self) -> None:
        headline = "Previously reported parser regressions remain unresolved and can lose findings or block promotion."
        body = f"<!-- ccr-overview-v2 -->\n\n### 🔵 Needs a closer look\n\n{headline}\n\n**No open issues** 🎉"
        snapshot = self._zero_finding_overview_snapshot(body)
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider.dispatch_repair.return_value = "task:owner/repo:77"

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
                return_value=(False, 0),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.critique_task_binding.bind_critique_task_id"
            ) as bind_task_id,
        ):
            result = DispatchRepairAction().execute(provider, snapshot, derived)

        assert result.decision is ActionDecision.EXECUTE, result.error
        bind_task_id.assert_called_once()
        assert bind_task_id.call_args.args[:2] == (provider, snapshot)
        assert bind_task_id.call_args.args[2][1:] == (100, 1)
        assert bind_task_id.call_args.args[3] == "77"
        assert provider.dispatch_repair.call_args.kwargs["agent_task_prompt"] == (
            "@copilot please address the following critique of this pr:\n\n" + headline
        )
        provider.post_comment_as_pr_token.assert_called_once()
        assert derived.get("repair_dispatched") is True
        approval = ApproveAction().evaluate(snapshot, derived)
        assert approval.decision is ActionDecision.SKIP
        assert approval.details == "Repair dispatched — deferring approval"

    def test_pre_creation_failure_cancels_critique_task_marker(self) -> None:
        headline = "Previously reported parser regressions remain unresolved and can lose findings or block promotion."
        body = f"<!-- ccr-overview-v2 -->\n\n### 🔵 Needs a closer look\n\n{headline}\n\n0 open findings"
        snapshot = self._zero_finding_overview_snapshot(body)
        provider = MagicMock()
        provider.dispatch_repair.side_effect = RepairDispatchNotAttemptedError("Agent Tasks API disabled")

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
                return_value=(False, 0),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_cycle_limit",
                return_value=(False, 0),
            ),
        ):
            result = DispatchRepairAction().execute(provider, snapshot, DerivedState(snapshot))

        assert result.decision is ActionDecision.FAILED
        comments = provider.list_issue_comments(42)
        assert any(
            "ai-pr-loop:critique-task-cancelled pr=42 head=head review=100 attempt=1" in comment.body
            for comment in comments
        )
        assert not any(
            "ai-pr-loop:critique-task pr=42 head=head review=100 attempt=1" in comment.body for comment in comments
        )

    def test_invalid_critique_task_marker_receipt_fails_dispatch(self) -> None:
        headline = "Previously reported parser regressions remain unresolved and can lose findings or block promotion."
        body = f"<!-- ccr-overview-v2 -->\n\n### 🔵 Needs a closer look\n\n{headline}\n\n0 open findings"
        snapshot = self._zero_finding_overview_snapshot(body)
        provider = MagicMock()
        provider.post_comment_as_pr_token.side_effect = None
        provider.post_comment_as_pr_token.return_value = 0

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
                return_value=(False, 0),
            ),
        ):
            result = DispatchRepairAction().execute(provider, snapshot, DerivedState(snapshot))

        assert result.decision is ActionDecision.FAILED
        assert "Critique task marker write failed" in result.error
        provider.dispatch_repair.assert_not_called()

    def test_critique_task_cancellation_rejects_changed_comment_identity(self) -> None:
        headline = "Previously reported parser regressions remain unresolved and can lose findings or block promotion."
        body = f"<!-- ccr-overview-v2 -->\n\n### 🔵 Needs a closer look\n\n{headline}\n\n0 open findings"
        snapshot = self._zero_finding_overview_snapshot(body)
        provider = MagicMock()
        provider.dispatch_repair.side_effect = RepairDispatchNotAttemptedError("Agent Tasks API disabled")
        provider.update_comment_as_pr_token.side_effect = None
        provider.update_comment_as_pr_token.return_value = 999

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
                return_value=(False, 0),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_cycle_limit",
                return_value=(False, 0),
            ),
        ):
            result = DispatchRepairAction().execute(provider, snapshot, DerivedState(snapshot))

        assert result.decision is ActionDecision.FAILED
        assert "Critique task cancellation changed the comment identity" in result.error

    def test_critique_task_cancellation_requires_confirmed_readback(self) -> None:
        headline = "Previously reported parser regressions remain unresolved and can lose findings or block promotion."
        body = f"<!-- ccr-overview-v2 -->\n\n### 🔵 Needs a closer look\n\n{headline}\n\n0 open findings"
        snapshot = self._zero_finding_overview_snapshot(body)
        provider = MagicMock()
        provider.dispatch_repair.side_effect = RepairDispatchNotAttemptedError("Agent Tasks API disabled")
        original_find_comment = provider.find_comment.side_effect

        def hide_cancellation_marker(pr_number: int, marker: str):
            if "critique-task-cancelled" in marker:
                return None
            return original_find_comment(pr_number, marker)

        provider.find_comment.side_effect = hide_cancellation_marker
        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
                return_value=(False, 0),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_cycle_limit",
                return_value=(False, 0),
            ),
        ):
            result = DispatchRepairAction().execute(provider, snapshot, DerivedState(snapshot))

        assert result.decision is ActionDecision.FAILED
        assert "Critique task cancellation could not be confirmed" in result.error

    def test_rebutted_critique_on_same_head_and_headline_is_not_dispatched_again(self) -> None:
        headline = "Previously reported parser regressions remain unresolved and can lose findings or block promotion."
        body = f"<!-- ccr-overview-v2 -->\n\n### 🔵 Needs a closer look\n\n{headline}\n\n0 open findings"
        snapshot = replace(
            self._zero_finding_overview_snapshot(body),
            critique_adjudicated_review_id=99,
            critique_adjudicated_head_sha="head",
            critique_adjudicated_headline=headline,
            critique_adjudicated_verdict="rebutted",
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()

        result = DispatchRepairAction().execute(provider, snapshot, derived)

        assert result.decision is ActionDecision.SKIP
        assert "already rebutted" in result.details
        provider.dispatch_repair.assert_not_called()

    def test_active_critique_task_blocks_dispatch(self) -> None:
        headline = "Previously reported parser regressions remain unresolved and can lose findings or block promotion."
        body = f"<!-- ccr-overview-v2 -->\n### 🔵 Needs a closer look\n\n{headline}\n\n0 open findings"
        snapshot = self._zero_finding_overview_snapshot(body)
        derived = DerivedState(snapshot)
        provider = MagicMock()
        derived.set("provider", provider)

        with patch(
            "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.is_copilot_session_active_via_agent_task",
            return_value=True,
        ):
            result = DispatchRepairAction().evaluate(snapshot, derived)

        assert result.decision is ActionDecision.SKIP
        assert result.preconditions["no_active_session"] is False

    def test_younger_critique_task_without_task_marker_blocks_dispatch(self) -> None:
        headline = "Previously reported parser regressions remain unresolved and can lose findings or block promotion."
        body = f"<!-- ccr-overview-v2 -->\n### 🔵 Needs a closer look\n\n{headline}\n\n0 open findings"
        snapshot = self._zero_finding_overview_snapshot(body)
        provider = MagicMock()
        RepairAttemptTracker(provider, 42, "head").reserve({"critique:100:1"})
        assert not any("<!-- ai-pr-loop:critique-task " in comment.body for comment in provider.list_issue_comments(42))
        derived = DerivedState(snapshot)
        derived.set("provider", provider)

        with patch(
            "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.is_copilot_session_active_via_agent_task",
            return_value=True,
        ):
            result = DispatchRepairAction().evaluate(snapshot, derived)

        assert result.decision is ActionDecision.SKIP
        assert result.preconditions["no_active_session"] is False
        provider.dispatch_repair.assert_not_called()

    def test_unconfirmed_critique_attempt_without_task_marker_does_not_dispatch_again(self) -> None:
        headline = "Previously reported parser regressions remain unresolved and can lose findings or block promotion."
        body = f"<!-- ccr-overview-v2 -->\n### 🔵 Needs a closer look\n\n{headline}\n\n0 open findings"
        snapshot = self._zero_finding_overview_snapshot(body)
        provider = MagicMock()
        RepairAttemptTracker(provider, 42, "head").reserve({"critique:100:1"})
        assert not any("<!-- ai-pr-loop:critique-task " in comment.body for comment in provider.list_issue_comments(42))

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
                return_value=(False, 0),
            ),
        ):
            result = DispatchRepairAction().execute(provider, snapshot, DerivedState(snapshot))

        assert result.decision is ActionDecision.SKIP
        assert "No unattempted findings" in result.details
        provider.dispatch_repair.assert_not_called()

    def test_needs_repair_adjudication_allows_one_critique_followup(self) -> None:
        headline = "Previously reported parser regressions remain unresolved and can lose findings or block promotion."
        body = f"<!-- ccr-overview-v2 -->\n### 🔵 Needs a closer look\n\n{headline}\n\n0 open findings"
        snapshot = replace(
            self._zero_finding_overview_snapshot(body),
            critique_adjudicated_review_id=100,
            critique_adjudicated_head_sha="head",
            critique_adjudicated_headline=headline,
            critique_adjudicated_verdict="needs_repair",
            critique_followup_instruction="Add a regression test for the parser boundary case.",
        )
        provider = MagicMock()
        provider.dispatch_repair.return_value = "task:owner/repo:77"
        RepairAttemptTracker(provider, 42, "head").reserve({"critique:100:1"})

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
                return_value=(False, 0),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.critique_task_binding.bind_critique_task_id"
            ) as bind_task_id,
        ):
            result = DispatchRepairAction().execute(provider, snapshot, DerivedState(snapshot))

        assert result.decision is ActionDecision.EXECUTE, result.error
        bind_task_id.assert_called_once()
        assert bind_task_id.call_args.args[:2] == (provider, snapshot)
        assert bind_task_id.call_args.args[2][1:] == (100, 2)
        assert bind_task_id.call_args.args[3] == "77"
        assert provider.dispatch_repair.call_args.kwargs["agent_task_prompt"] == (
            "@copilot please address the following critique of this pr:\n\n"
            "Add a regression test for the parser boundary case."
        )

    def test_critique_task_cap_blocks_a_third_head_attempt(self) -> None:
        headline = "Previously reported parser regressions remain unresolved and can lose findings or block promotion."
        body = f"<!-- ccr-overview-v2 -->\n### 🔵 Needs a closer look\n\n{headline}\n\n0 open findings"
        snapshot = self._zero_finding_overview_snapshot(body)
        provider = MagicMock()
        RepairAttemptTracker(provider, 42, "head").reserve({"critique:100:1", "critique:100:2"})

        result = DispatchRepairAction().execute(provider, snapshot, DerivedState(snapshot))

        assert result.decision is ActionDecision.SKIP
        assert result.details == "Critique repair task cap reached for this HEAD"
        provider.dispatch_repair.assert_not_called()

    @pytest.mark.parametrize(
        "body",
        [
            "not a CCR overview",
            "<!-- ccr-overview-v2 -->\n### Needs a closer look\n\nA concern remains.\n\n1 open issue",
        ],
    )
    def test_known_empty_overview_rejects_unparseable_or_nonempty_reviews(self, body: str) -> None:
        snapshot = self._zero_finding_overview_snapshot(body)

        assert critique_dispatch.known_empty_zero_findings_overview(snapshot) is None

    def test_known_empty_overview_requires_the_matching_review(self) -> None:
        body = "<!-- ccr-overview-v2 -->\n### Needs a closer look\n\nA concern remains.\n\n0 open findings"
        snapshot = replace(self._zero_finding_overview_snapshot(body), reviews=[])

        assert critique_dispatch.known_empty_zero_findings_overview(snapshot) is None

    def test_approval_worthy_zero_finding_headline_keeps_existing_path(self) -> None:
        body = (
            "<!-- ccr-overview-v2 -->\n"
            "### ✅ Ready to approve\n\n"
            "This PR is ready to merge; it only needs human approval.\n\n"
            "0 open findings"
        )
        snapshot = self._zero_finding_overview_snapshot(body, classification="approval_worthy")

        result = DispatchRepairAction().evaluate(snapshot, DerivedState(snapshot))

        assert result.decision is ActionDecision.SKIP
        assert result.preconditions["needs_repair"] is False

    def test_human_review_only_sentence_with_critique_heading_is_approval_worthy(self) -> None:
        headline = "Broad modernization and limited baseline verification require final human review."
        body = f"<!-- ccr-overview-v2 -->\n### 🔵 Needs a closer look\n\n{headline}\n\n0 open findings"
        snapshot = self._zero_finding_overview_snapshot(body, classification="approval_worthy")

        result = DispatchRepairAction().evaluate(snapshot, DerivedState(snapshot))

        assert result.decision is ActionDecision.SKIP
        assert result.preconditions["needs_repair"] is False

    def test_unparseable_zero_finding_headline_is_logged_without_dispatch(self, caplog) -> None:
        body = "<!-- ccr-overview-v2 -->\n**No open issues** 🎉"
        snapshot = self._zero_finding_overview_snapshot(body)
        provider = MagicMock()

        result = DispatchRepairAction().execute(provider, snapshot, DerivedState(snapshot))

        assert result.decision is ActionDecision.SKIP
        provider.dispatch_repair.assert_not_called()
        assert "zero-open-findings CCR overview has no parseable headline" in caplog.text

    def test_approval_worthy_overview_is_skipped_during_dispatch(self) -> None:
        body = (
            "<!-- ccr-overview-v2 -->\n"
            "### 🔵 Needs a closer look\n\n"
            "Broad modernization and limited baseline verification require final human review.\n\n"
            "0 open findings"
        )
        snapshot = self._zero_finding_overview_snapshot(body, classification="approval_worthy")

        result = critique_dispatch.zero_findings_repair_skip("dispatch_repair", snapshot, False)

        assert result is not None
        assert result.decision is ActionDecision.SKIP

    def test_log_noncritique_overview_does_not_log_for_a_critique(self, caplog) -> None:
        headline = "Previously reported parser regressions remain unresolved and can lose findings or block promotion."
        body = f"<!-- ccr-overview-v2 -->\n### 🔵 Needs a closer look\n\n{headline}\n\n0 open findings"
        snapshot = self._zero_finding_overview_snapshot(body)

        critique_dispatch.log_noncritique_overview(snapshot)

        assert "zero-open-findings CCR overview" not in caplog.text

    def test_critique_overview_for_an_older_head_does_not_dispatch(self) -> None:
        body = "<!-- ccr-overview-v2 -->\n### 🔵 Needs a closer look\n\nA concern remains.\n\n0 open findings"
        snapshot = self._zero_finding_overview_snapshot(body, head_sha="old-head")
        provider = MagicMock()
        result = DispatchRepairAction().execute(provider, snapshot, DerivedState(snapshot))

        assert result.decision is ActionDecision.SKIP
        provider.dispatch_repair.assert_not_called()
