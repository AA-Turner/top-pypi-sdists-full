"""Test semantic classification while loading the critique snapshot fields."""

from unittest.mock import MagicMock, patch

import pytest

from agentic_devtools.cli.ci.critique_adjudicator import CritiqueHeadlineClassification
from agentic_devtools.cli.ci.models import PRMetadata, ReviewCommentInfo, ReviewInfo
from agentic_devtools.cli.ci.pipeline.actions.critique_dispatch import zero_findings_headline
from agentic_devtools.cli.ci.pipeline.critique_gate import critique_gate_exception_passed
from agentic_devtools.cli.ci.pipeline.critique_snapshot import current_zero_findings_headline
from agentic_devtools.cli.ci.pipeline.gate_verdict import REASON_CLEAN, REASON_NEW_CCR_NOT_APPROVED, CopilotGateVerdict
from agentic_devtools.cli.ci.pipeline.snapshot_builder import build_pr_state_snapshot


def _make_provider() -> MagicMock:
    provider = MagicMock()
    provider.count_commits_behind.return_value = 0
    provider.get_approver_login.return_value = ""
    provider.compute_diff_files = None
    return provider


def _current_review_provider(
    comments: list[ReviewCommentInfo],
    thread_states: object,
    *,
    body: str = "",
    provider: MagicMock | None = None,
) -> MagicMock:
    provider = provider or _make_provider()
    provider.get_pr_metadata.return_value = PRMetadata(
        number=1,
        title="Test PR",
        head_branch="feature",
        head_sha="head-sha",
        base_branch="main",
        requested_reviewers=[],
    )
    provider.list_pr_files.return_value = ["a.py"]
    provider.list_check_runs.return_value = []
    provider.list_reviews.return_value = [
        ReviewInfo(
            id=12,
            user="Copilot",
            state="CHANGES_REQUESTED",
            body=body,
            commit_sha="head-sha",
        ),
    ]
    provider.list_review_comments.return_value = comments
    provider.list_review_threads_by_thread_id.return_value = thread_states
    provider.list_pr_issue_events.return_value = []
    provider.count_commits_above_merge_base.return_value = 1
    return provider


class TestCurrentZeroFindingsHeadline:
    """Cover the snapshot classification handoff."""

    @pytest.mark.parametrize(
        ("verdict", "reviews", "head", "changed", "count", "count_review", "filtered", "overview"),
        [
            (None, [], "head", False, 0, 100, False, (True, "A defect remains.")),
            (
                CopilotGateVerdict(False, "other", 100, body_comment_count=0),
                [],
                "head",
                False,
                0,
                100,
                False,
                (True, "A defect remains."),
            ),
            (
                CopilotGateVerdict(False, REASON_NEW_CCR_NOT_APPROVED, 100, body_comment_count=1),
                [],
                "head",
                False,
                0,
                100,
                False,
                (True, "A defect remains."),
            ),
            (
                CopilotGateVerdict(False, REASON_NEW_CCR_NOT_APPROVED, 100, 0, suppressed_count=1),
                [],
                "head",
                False,
                0,
                100,
                False,
                (True, "A defect remains."),
            ),
            (
                CopilotGateVerdict(False, REASON_NEW_CCR_NOT_APPROVED, 100, 0),
                [],
                "head",
                True,
                0,
                100,
                False,
                (True, "A defect remains."),
            ),
            (
                CopilotGateVerdict(False, REASON_NEW_CCR_NOT_APPROVED, 100, 0),
                [],
                "",
                False,
                0,
                100,
                False,
                (True, "A defect remains."),
            ),
            (
                CopilotGateVerdict(False, REASON_NEW_CCR_NOT_APPROVED, 100, 0),
                [],
                "head",
                False,
                0,
                100,
                False,
                (True, "A defect remains."),
            ),
            (
                CopilotGateVerdict(False, REASON_NEW_CCR_NOT_APPROVED, 100, 0),
                [ReviewInfo(100, "Copilot", "COMMENTED", "overview", "old")],
                "head",
                False,
                0,
                100,
                False,
                (True, "A defect remains."),
            ),
            (
                CopilotGateVerdict(False, REASON_NEW_CCR_NOT_APPROVED, 100, 0),
                [ReviewInfo(100, "Copilot", "COMMENTED", "overview", "head")],
                "head",
                False,
                1,
                100,
                False,
                (True, "A defect remains."),
            ),
            (
                CopilotGateVerdict(False, REASON_NEW_CCR_NOT_APPROVED, 100, 0),
                [ReviewInfo(100, "Copilot", "COMMENTED", "overview", "head")],
                "head",
                False,
                0,
                100,
                False,
                None,
            ),
            (
                CopilotGateVerdict(False, REASON_NEW_CCR_NOT_APPROVED, 100, 0),
                [ReviewInfo(100, "Copilot", "COMMENTED", "overview", "head")],
                "head",
                False,
                0,
                100,
                False,
                (False, None),
            ),
            (
                CopilotGateVerdict(False, REASON_NEW_CCR_NOT_APPROVED, 100, 0),
                [ReviewInfo(100, "Copilot", "COMMENTED", "overview", "head")],
                "head",
                False,
                0,
                100,
                False,
                (True, None),
            ),
        ],
    )
    def test_ineligible_context_returns_empty_headline(
        self, verdict, reviews, head, changed, count, count_review, filtered, overview
    ) -> None:
        with patch(
            "agentic_devtools.cli.ci.pipeline.critique_snapshot.parse_ccr_overview_summary",
            return_value=overview,
        ):
            result = current_zero_findings_headline(verdict, reviews, head, changed, count, count_review, filtered)

        assert result == ("", "")

    @pytest.mark.parametrize(
        ("count", "count_review", "filtered"),
        [(None, None, None), (0, 99, False), (0, 100, None)],
    )
    def test_unknown_comment_inventory_does_not_hide_eligible_current_head_headline(
        self, count, count_review, filtered
    ) -> None:
        headline = "A concrete parser regression remains."
        verdict = CopilotGateVerdict(False, REASON_NEW_CCR_NOT_APPROVED, 100, body_comment_count=0)
        review = ReviewInfo(100, "Copilot", "COMMENTED", "overview", "head")
        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.critique_snapshot.parse_ccr_overview_summary",
                return_value=(True, headline),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.critique_snapshot.classify_critique_headline",
                return_value=CritiqueHeadlineClassification(verdict="critique"),
            ),
        ):
            result = current_zero_findings_headline(verdict, [review], "head", False, count, count_review, filtered)

        assert result == (headline, "critique")

    def test_semantically_classifies_only_the_zero_findings_headline(self) -> None:
        headline = "Previously reported parser regressions remain unresolved and can lose findings or block promotion."
        provider = _current_review_provider(
            [],
            {},
            body=(
                "<!-- ccr-overview-v2 -->\n"
                "### 🟡 Not ready to approve\n\n"
                f"{headline}\n\n"
                "**Comments generated:** 0\n"
                "**No open issues** 🎉"
            ),
        )
        provider.list_issue_comments.return_value = []

        with patch(
            "agentic_devtools.cli.ci.pipeline.critique_snapshot.classify_critique_headline",
            return_value=CritiqueHeadlineClassification(verdict="critique"),
        ) as classify:
            snapshot = build_pr_state_snapshot(provider, 1, promote_findings=False)

        assert snapshot.critique_headline_classification == "critique"
        classify.assert_called_once_with(headline)

    def test_footer_free_overview_uses_known_empty_api_inventory(self) -> None:
        headline = "Previously reported parser regressions remain unresolved."
        provider = _current_review_provider(
            [],
            {},
            body=(f"<!-- ccr-overview-v2 -->\n### 🔵 Needs a closer look\n\n{headline}\n\n**No open issues** 🎉"),
        )
        provider.list_issue_comments.return_value = []
        verdict = CopilotGateVerdict(True, REASON_CLEAN, 12, body_comment_count=None)

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.critique_snapshot.classify_critique_headline",
                return_value=CritiqueHeadlineClassification(verdict="critique"),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.snapshot_builder.evaluate_copilot_gate_verdict",
                return_value=verdict,
            ),
        ):
            snapshot = build_pr_state_snapshot(provider, 1, promote_findings=False)

        assert snapshot.critique_headline_classification == "critique"
        assert snapshot.effective_review_comment_count == 0
        assert zero_findings_headline(snapshot) == (12, headline)
        assert critique_gate_exception_passed(snapshot, unresolved_threads=0) is False

    def test_issue_comment_fetch_failure_marks_critique_task_state_unavailable(self) -> None:
        headline = "Broad modernization and limited baseline verification require final human review."
        provider = _current_review_provider(
            [],
            {},
            body=f"<!-- ccr-overview-v2 -->\n### Needs a closer look\n\n{headline}\n\n0 open findings",
        )
        provider.list_issue_comments.side_effect = RuntimeError("comments unavailable")
        verdict = CopilotGateVerdict(False, REASON_NEW_CCR_NOT_APPROVED, 12, body_comment_count=0)

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.critique_snapshot.classify_critique_headline",
                return_value=CritiqueHeadlineClassification(verdict="approval_worthy"),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.snapshot_builder.evaluate_copilot_gate_verdict",
                return_value=verdict,
            ),
        ):
            snapshot = build_pr_state_snapshot(provider, 1, promote_findings=False)

        assert snapshot.critique_headline_classification == "approval_worthy"
        assert snapshot.critique_task_state_available is False
        assert critique_gate_exception_passed(snapshot, unresolved_threads=0) is False

    def test_missing_issue_comment_reader_marks_critique_task_state_unavailable(self) -> None:
        headline = "Broad modernization and limited baseline verification require final human review."
        provider = _current_review_provider(
            [],
            {},
            body=f"<!-- ccr-overview-v2 -->\n### Needs a closer look\n\n{headline}\n\n0 open findings",
        )
        provider.list_issue_comments = None
        verdict = CopilotGateVerdict(False, REASON_NEW_CCR_NOT_APPROVED, 12, body_comment_count=0)

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.critique_snapshot.classify_critique_headline",
                return_value=CritiqueHeadlineClassification(verdict="approval_worthy"),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.snapshot_builder.evaluate_copilot_gate_verdict",
                return_value=verdict,
            ),
        ):
            snapshot = build_pr_state_snapshot(provider, 1, promote_findings=False)

        assert snapshot.critique_headline_classification == "approval_worthy"
        assert snapshot.critique_task_state_available is False
