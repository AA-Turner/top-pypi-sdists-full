"""Tests for render_summary_comment."""

from unittest.mock import MagicMock, patch

import pytest

from agentic_devtools.cli.ci.pipeline.models import (
    ActionDecision,
    ActionResult,
    PipelineRunSummary,
)
from agentic_devtools.cli.ci.pipeline.snapshot import PRStateSnapshot
from agentic_devtools.cli.ci.pipeline.summary import (
    SUMMARY_SENTINEL,
    post_summary_comment,
    render_summary_comment,
)
from agentic_devtools.cli.shared.retry import ProviderRateLimitError


class TestRenderSummaryComment:
    """Tests for the summary comment renderer."""

    def test_contains_sentinel(self) -> None:
        summary = PipelineRunSummary()
        comment = render_summary_comment(summary)
        assert SUMMARY_SENTINEL in comment

    def test_contains_run_url(self) -> None:
        summary = PipelineRunSummary(run_url="https://github.com/org/repo/actions/runs/12345")
        comment = render_summary_comment(summary)
        assert "View Logs" in comment
        assert "12345" in comment

    def test_header_without_trigger_reason_or_url(self) -> None:
        summary = PipelineRunSummary()
        comment = render_summary_comment(summary)
        assert "#### 🤖 AI PR Loop Run" in comment
        assert "Trigger Reason" not in comment
        assert "View Logs" not in comment

    def test_header_with_trigger_reason(self) -> None:
        summary = PipelineRunSummary(trigger_reason="ci_completion")
        comment = render_summary_comment(summary)
        assert "#### 🤖 AI PR Loop Run — Trigger Reason: ci_completion" in comment

    def test_header_with_trigger_reason_and_url(self) -> None:
        summary = PipelineRunSummary(
            trigger_reason="agent_session_finished",
            run_url="https://github.com/org/repo/actions/runs/99",
        )
        comment = render_summary_comment(summary)
        assert "#### 🤖 AI PR Loop Run — Trigger Reason: agent_session_finished — [View Logs](" in comment

    def test_header_trigger_reason_is_single_line_and_html_escaped(self) -> None:
        summary = PipelineRunSummary(trigger_reason="ci_done\n<details>pwn</details>\r\nnext")
        comment = render_summary_comment(summary)
        assert "Trigger Reason: ci_done &lt;details&gt;pwn&lt;/details&gt; next" in comment
        assert "Trigger Reason: ci_done\n" not in comment

    def test_header_run_url_strips_newlines(self) -> None:
        summary = PipelineRunSummary(run_url="https://github.com/org/repo/actions/runs/99\n\r")
        comment = render_summary_comment(summary)
        assert "[View Logs](https://github.com/org/repo/actions/runs/99)" in comment
        assert "\n\r" not in comment

    def test_actions_table_is_collapsed(self) -> None:
        results = [
            ActionResult(name="guards", decision=ActionDecision.EXECUTE, details="All guards passed"),
        ]
        summary = PipelineRunSummary(results=results)
        comment = render_summary_comment(summary)
        assert "<summary>Actions table</summary>" in comment
        assert "| Action | Preconditions | Result |" in comment
        assert "</details>" in comment

    def test_outer_details_wraps_inner_sections(self) -> None:
        results = [
            ActionResult(name="guards", decision=ActionDecision.EXECUTE, details="All guards passed"),
        ]
        snapshot = PRStateSnapshot(head_sha="abc1234567890", commit_count=1, ci_status="passing")
        summary = PipelineRunSummary(results=results, snapshot=snapshot)
        comment = render_summary_comment(summary)
        assert "<summary>Details</summary>" in comment
        outer = comment.index("<summary>Details</summary>")
        # Header and sentinel stay above the outer Details wrapper.
        assert comment.index("#### \U0001f916 AI PR Loop Run") < outer
        # Both inner sections appear after the outer Details summary.
        assert outer < comment.index("<summary>Actions table</summary>")
        assert outer < comment.index("<summary>State snapshot</summary>")

    def test_contains_action_table(self) -> None:
        results = [
            ActionResult(name="guards", decision=ActionDecision.EXECUTE, details="All guards passed"),
            ActionResult(name="publish", decision=ActionDecision.SKIP, details="Not a draft"),
            ActionResult(name="merge", decision=ActionDecision.EXECUTE, details="PR merged"),
        ]
        summary = PipelineRunSummary(results=results)
        comment = render_summary_comment(summary)
        assert "guards" in comment
        assert "publish" in comment
        assert "merge" in comment
        assert "skipped" in comment
        assert "Not a draft" in comment
        assert "**executed**" in comment

    def test_contains_state_snapshot(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=42,
            head_sha="abc1234567890",
            commit_count=2,
            ci_status="passing",
            active_session=False,
            unresolved_threads=0,
        )
        summary = PipelineRunSummary(snapshot=snapshot)
        comment = render_summary_comment(summary)
        assert "<summary>State snapshot</summary>" in comment
        assert "abc1234" in comment
        assert "Commits above merge-base: 2" in comment
        assert "CI: passing" in comment

    def test_guard_blocked_rendering(self) -> None:
        results = [
            ActionResult(name="guards", decision=ActionDecision.BLOCKED, details="PR is from a fork"),
            ActionResult(name="publish", decision=ActionDecision.BLOCKED_BY_GUARD, details="Blocked by guards"),
        ]
        summary = PipelineRunSummary(results=results)
        comment = render_summary_comment(summary)
        assert "blocked" in comment
        assert "🚫" in comment

    def test_failed_rendering_includes_failure_details_and_error(self) -> None:
        summary = PipelineRunSummary(
            results=[
                ActionResult(
                    name="merge",
                    decision=ActionDecision.FAILED,
                    details="Exception during execution",
                    error="merge API timeout",
                )
            ]
        )
        comment = render_summary_comment(summary)
        assert "**failed**" in comment
        assert "Exception during execution" in comment
        assert "merge API timeout" in comment

    def test_table_cells_with_pipes_and_newlines_are_sanitized(self) -> None:
        """Pipe and newline characters in cell values must not break the table."""
        summary = PipelineRunSummary(
            results=[
                ActionResult(
                    name="merge",
                    decision=ActionDecision.FAILED,
                    details="step1\r\nstep2\rstep3",
                    error="timeout | retry failed",
                )
            ]
        )
        comment = render_summary_comment(summary)
        # Newlines must be replaced with <br>; raw newline within detail must not appear
        assert "step1<br>step2<br>step3" in comment
        assert "step1\r\nstep2\rstep3" not in comment
        # Pipe characters must be escaped; unescaped form must not appear in rendered error
        assert "timeout \\| retry failed" in comment
        assert "timeout | retry failed" not in comment

    def test_format_preconditions_returns_dash_when_no_preconditions(self) -> None:
        """_format_preconditions must return '—' when preconditions dict is empty."""
        result = ActionResult(
            name="guards",
            decision=ActionDecision.SKIP,
            details="some detail text that should only appear in Result column",
            preconditions={},
        )
        summary = PipelineRunSummary(results=[result])
        comment = render_summary_comment(summary)
        # The detail text must appear in the Result column, but not duplicated in Preconditions
        assert "some detail text" in comment
        # Preconditions column should show '—', not the detail text
        assert "⬜ —" in comment

    def test_format_preconditions_all_passed_rendered(self) -> None:
        summary = PipelineRunSummary(
            results=[
                ActionResult(
                    name="guards",
                    decision=ActionDecision.SKIP,
                    preconditions={"ci_passing": True},
                    details="all good",
                )
            ]
        )
        comment = render_summary_comment(summary)
        assert "all passed" in comment

    def test_format_preconditions_shows_failed_key(self) -> None:
        summary = PipelineRunSummary(
            results=[
                ActionResult(
                    name="approve",
                    decision=ActionDecision.SKIP,
                    preconditions={"ci_passing": True, "approved": False},
                    details="not approved",
                )
            ]
        )
        comment = render_summary_comment(summary)
        assert "✗ approved" in comment

    def test_format_preconditions_shows_every_failed_key(self) -> None:
        """A composite skip must render all failing preconditions, not just the first."""
        summary = PipelineRunSummary(
            results=[
                ActionResult(
                    name="merge",
                    decision=ActionDecision.SKIP,
                    preconditions={
                        "ci_passing": False,
                        "approved": True,
                        "threads_resolved": False,
                        "label_present": False,
                    },
                    details="blocked",
                )
            ]
        )
        comment = render_summary_comment(summary)
        assert "✗ ci_passing, ✗ threads_resolved, ✗ label_present" in comment

    def test_format_preconditions_clips_at_extended_bound(self) -> None:
        """Long precondition lists clip at 120 characters, not 60."""
        preconditions = {f"failing_precondition_key_{index}": False for index in range(12)}
        summary = PipelineRunSummary(
            results=[
                ActionResult(
                    name="merge",
                    decision=ActionDecision.SKIP,
                    preconditions=preconditions,
                    details="blocked",
                )
            ]
        )
        comment = render_summary_comment(summary)
        expected = ", ".join(f"✗ {key}" for key in preconditions)[:120]
        assert expected in comment
        assert ", ".join(f"✗ {key}" for key in preconditions)[:121] not in comment

    def test_failed_result_includes_error_without_details(self) -> None:
        summary = PipelineRunSummary(
            results=[
                ActionResult(
                    name="merge",
                    decision=ActionDecision.FAILED,
                    details="",
                    error="boom",
                )
            ]
        )
        comment = render_summary_comment(summary)
        assert "error: boom" in comment

    def test_render_state_snapshot_inline_suffix_only_for_commented_or_nonzero(self) -> None:
        """'(N inline)' suffix must only appear for COMMENTED state or non-zero count."""
        # COMMENTED with count: should show suffix
        snapshot_commented = PRStateSnapshot(
            head_sha="abc1234567890",
            review_state="COMMENTED",
            copilot_review_inline_count=3,
        )
        summary_commented = PipelineRunSummary(snapshot=snapshot_commented)
        comment_commented = render_summary_comment(summary_commented)
        assert "3 inline" in comment_commented

        # APPROVED with zero count: must NOT show suffix
        snapshot_approved = PRStateSnapshot(
            head_sha="abc1234567890",
            review_state="APPROVED",
            copilot_review_inline_count=0,
        )
        summary_approved = PipelineRunSummary(snapshot=snapshot_approved)
        comment_approved = render_summary_comment(summary_approved)
        assert "0 inline" not in comment_approved
        assert "inline" not in comment_approved

        # Non-zero count with non-COMMENTED state: should still show suffix
        snapshot_nonzero = PRStateSnapshot(
            head_sha="abc1234567890",
            review_state="CHANGES_REQUESTED",
            copilot_review_inline_count=2,
        )
        summary_nonzero = PipelineRunSummary(snapshot=snapshot_nonzero)
        comment_nonzero = render_summary_comment(summary_nonzero)
        assert "2 inline" in comment_nonzero

    def test_render_state_snapshot_unresolved_threads_count_when_known(self) -> None:
        """A known thread count renders as a plain integer."""
        snapshot = PRStateSnapshot(head_sha="abc1234567890", unresolved_threads=2)
        summary = PipelineRunSummary(snapshot=snapshot)
        comment = render_summary_comment(summary)
        assert "- Unresolved threads: 2" in comment

    def test_render_state_snapshot_unresolved_threads_degraded(self) -> None:
        """A degraded thread count renders as a blocking sentinel with the fallback count."""
        snapshot = PRStateSnapshot(
            head_sha="abc1234567890",
            unresolved_threads=1,
            unresolved_threads_degraded=True,
        )
        summary = PipelineRunSummary(snapshot=snapshot)
        comment = render_summary_comment(summary)
        assert "- Unresolved threads: degraded / unknown (blocking sentinel 1)" in comment

    def test_render_state_snapshot_derived_unresolved_threads_none(self) -> None:
        """A ``None`` derived count leaves the line unchanged."""
        snapshot = PRStateSnapshot(head_sha="abc1234567890", unresolved_threads=2)
        summary = PipelineRunSummary(snapshot=snapshot, derived_unresolved_threads=None)
        comment = render_summary_comment(summary)
        assert "- Unresolved threads: 2\n" in comment
        assert "gates saw" not in comment

    def test_render_state_snapshot_derived_unresolved_threads_equal(self) -> None:
        """A derived count equal to the snapshot count leaves the line unchanged."""
        snapshot = PRStateSnapshot(head_sha="abc1234567890", unresolved_threads=2)
        summary = PipelineRunSummary(snapshot=snapshot, derived_unresolved_threads=2)
        comment = render_summary_comment(summary)
        assert "- Unresolved threads: 2\n" in comment
        assert "gates saw" not in comment

    def test_render_state_snapshot_derived_unresolved_threads_differs(self) -> None:
        """A differing derived count is named in a parenthetical."""
        snapshot = PRStateSnapshot(head_sha="abc1234567890", unresolved_threads=1)
        summary = PipelineRunSummary(snapshot=snapshot, derived_unresolved_threads=71)
        comment = render_summary_comment(summary)
        assert "- Unresolved threads: 1 (gates saw: 71)" in comment

    def test_render_state_snapshot_derived_unresolved_threads_differs_when_degraded(self) -> None:
        """The parenthetical is appended to the degraded rendering too."""
        snapshot = PRStateSnapshot(
            head_sha="abc1234567890",
            unresolved_threads=1,
            unresolved_threads_degraded=True,
        )
        summary = PipelineRunSummary(snapshot=snapshot, derived_unresolved_threads=71)
        comment = render_summary_comment(summary)
        assert "- Unresolved threads: degraded / unknown (blocking sentinel 1) (gates saw: 71)" in comment

    def test_render_state_snapshot_inline_unknown_suffix(self) -> None:
        snapshot = PRStateSnapshot(
            head_sha="abc1234567890",
            review_state="COMMENTED",
            copilot_review_inline_count=-1,
        )
        summary = PipelineRunSummary(snapshot=snapshot)
        comment = render_summary_comment(summary)
        assert "inline unknown" in comment

    def test_html_metacharacters_are_escaped_in_table_and_snapshot(self) -> None:
        summary = PipelineRunSummary(
            results=[
                ActionResult(
                    name="merge</details>",
                    decision=ActionDecision.SKIP,
                    details="bad <tag> & raw",
                )
            ],
            snapshot=PRStateSnapshot(
                head_sha="abc1234</details>",
                ci_status="pending > unknown",
                review_state="COMMENTED </summary>",
                labels=["x&y", "</details>"],
            ),
        )

        comment = render_summary_comment(summary)

        assert "merge&lt;/details&gt;" in comment
        assert "bad &lt;tag&gt; &amp; raw" in comment
        assert "COMMENTED &lt;/summary&gt;" in comment
        assert "x&amp;y, &lt;/details&gt;" in comment
        assert "merge</details>" not in comment
        assert "bad <tag> & raw" not in comment

    def test_post_summary_comment_continues_when_collapse_raises(self) -> None:
        provider = MagicMock()
        summary = PipelineRunSummary()

        with patch(
            "agentic_devtools.cli.ci.pipeline.summary.collapse_prior_summaries",
            side_effect=RuntimeError("collapse boom"),
        ):
            assert post_summary_comment(provider, pr_number=42, summary=summary) is True

        provider.post_comment.assert_called_once()

    def test_post_summary_comment_returns_false_when_post_fails(self) -> None:
        provider = MagicMock()
        provider.post_comment.side_effect = RuntimeError("post boom")
        summary = PipelineRunSummary()

        with patch(
            "agentic_devtools.cli.ci.pipeline.summary.collapse_prior_summaries",
            return_value=0,
        ):
            assert post_summary_comment(provider, pr_number=42, summary=summary) is False

    def test_post_summary_comment_reraises_rate_limit_when_post_fails(self) -> None:
        provider = MagicMock()
        provider.post_comment.side_effect = ProviderRateLimitError(
            provider="github",
            credential_identity="SPECKIT_PR_TOKEN",
        )
        summary = PipelineRunSummary()

        with patch(
            "agentic_devtools.cli.ci.pipeline.summary.collapse_prior_summaries",
            return_value=0,
        ):
            with pytest.raises(ProviderRateLimitError):
                post_summary_comment(provider, pr_number=42, summary=summary)

    def test_post_summary_comment_reraises_rate_limit_when_collapsing_fails(self) -> None:
        provider = MagicMock()
        summary = PipelineRunSummary()

        with patch(
            "agentic_devtools.cli.ci.pipeline.summary.collapse_prior_summaries",
            side_effect=ProviderRateLimitError(
                provider="github",
                credential_identity="SPECKIT_PR_TOKEN",
            ),
        ):
            with pytest.raises(ProviderRateLimitError):
                post_summary_comment(provider, pr_number=42, summary=summary)

    def test_post_summary_comment_logs_collapsed_count_when_nonzero(self) -> None:
        provider = MagicMock()
        summary = PipelineRunSummary()

        with patch(
            "agentic_devtools.cli.ci.pipeline.summary.collapse_prior_summaries",
            return_value=2,
        ):
            assert post_summary_comment(provider, pr_number=42, summary=summary) is True
