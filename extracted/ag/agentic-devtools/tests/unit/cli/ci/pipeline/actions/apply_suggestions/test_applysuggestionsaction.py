"""Tests for ApplySuggestionsAction."""

import os
from typing import cast
from unittest.mock import MagicMock, patch

import pytest

from agentic_devtools.cli.ci.pipeline.actions.apply_suggestions import (
    ApplySuggestionsAction,
    _apply_copilot_autofix_suggestions,
    _format_discovery_details,
    _html_scrape_succeeded,
    _post_deferral_if_needed,
)
from agentic_devtools.cli.ci.pipeline.discovery.models import (
    DiscoveryAttempt,
    DiscoveryOutcome,
)
from agentic_devtools.cli.ci.pipeline.exclusion import ExclusionContext
from agentic_devtools.cli.ci.pipeline.models import ActionDecision, ActionResult
from agentic_devtools.cli.ci.pipeline.snapshot import DerivedState, PRStateSnapshot
from agentic_devtools.cli.shared.retry import ProviderRateLimitError


class TestApplySuggestionsActionEvaluate:
    """Tests for ApplySuggestionsAction.evaluate()."""

    @patch.dict(os.environ, {"ENABLE_AUTO_APPLY_SUGGESTIONS": "true"}, clear=False)
    def test_skip_when_no_actionable_review(self) -> None:
        """SKIP when review state is APPROVED."""
        snapshot = PRStateSnapshot(
            pr_number=1,
            review_state="APPROVED",
            copilot_review_id=1,
            copilot_review_inline_count=0,
        )
        derived = DerivedState(snapshot)
        action = ApplySuggestionsAction()
        result = action.evaluate(snapshot, derived)
        assert result.decision == ActionDecision.SKIP

    @patch.dict(os.environ, {"ENABLE_AUTO_APPLY_SUGGESTIONS": "true"}, clear=False)
    def test_skip_when_no_review_id(self) -> None:
        """SKIP when copilot_review_id is 0."""
        snapshot = PRStateSnapshot(
            pr_number=1,
            review_state="CHANGES_REQUESTED",
            copilot_review_id=0,
        )
        derived = DerivedState(snapshot)
        action = ApplySuggestionsAction()
        result = action.evaluate(snapshot, derived)
        assert result.decision == ActionDecision.SKIP

    @patch.dict(os.environ, {"ENABLE_AUTO_APPLY_SUGGESTIONS": "true"}, clear=False)
    def test_execute_when_changes_requested_with_inline(self) -> None:
        """EXECUTE when CHANGES_REQUESTED with inline comments."""
        snapshot = PRStateSnapshot(
            pr_number=1,
            review_state="CHANGES_REQUESTED",
            copilot_review_id=100,
            copilot_review_inline_count=3,
        )
        derived = DerivedState(snapshot)
        action = ApplySuggestionsAction()
        result = action.evaluate(snapshot, derived)
        assert result.decision == ActionDecision.EXECUTE

    @patch.dict(os.environ, {"ENABLE_AUTO_APPLY_SUGGESTIONS": "true"}, clear=False)
    def test_execute_when_changes_requested_without_inline(self) -> None:
        """EXECUTE when CHANGES_REQUESTED even with inline count explicitly set to 0."""
        snapshot = PRStateSnapshot(
            pr_number=1,
            review_state="CHANGES_REQUESTED",
            copilot_review_id=100,
            copilot_review_inline_count=0,
        )
        derived = DerivedState(snapshot)
        action = ApplySuggestionsAction()
        result = action.evaluate(snapshot, derived)
        assert result.decision == ActionDecision.EXECUTE

    @patch.dict(os.environ, {"ENABLE_AUTO_APPLY_SUGGESTIONS": "true"}, clear=False)
    def test_execute_when_no_actionable_review_but_repairable_threads_exist(self) -> None:
        """EXECUTE when no new actionable review exists, but repairable threads do (even if blocking is 0)."""
        snapshot = PRStateSnapshot(
            pr_number=1,
            review_state="APPROVED",
            copilot_review_id=100,
            copilot_review_inline_count=0,
            unresolved_threads=0,  # Zero blocking threads
            repairable_threads=2,  # But repairable threads exist
        )
        derived = DerivedState(snapshot)
        action = ApplySuggestionsAction()
        result = action.evaluate(snapshot, derived)
        assert result.decision == ActionDecision.EXECUTE

    @patch.dict(os.environ, {"ENABLE_AUTO_APPLY_SUGGESTIONS": "true"}, clear=False)
    def test_execute_when_commented_with_inline(self) -> None:
        """EXECUTE when COMMENTED with inline comments."""
        snapshot = PRStateSnapshot(
            pr_number=1,
            review_state="COMMENTED",
            copilot_review_id=100,
            copilot_review_inline_count=2,
        )
        derived = DerivedState(snapshot)
        action = ApplySuggestionsAction()
        result = action.evaluate(snapshot, derived)
        assert result.decision == ActionDecision.EXECUTE

    @patch.dict(os.environ, {"ENABLE_AUTO_APPLY_SUGGESTIONS": "true"}, clear=False)
    def test_skip_when_commented_without_inline(self) -> None:
        """SKIP when COMMENTED and inline count is explicitly zero."""
        snapshot = PRStateSnapshot(
            pr_number=1,
            review_state="COMMENTED",
            copilot_review_id=100,
            copilot_review_inline_count=0,
        )
        derived = DerivedState(snapshot)
        action = ApplySuggestionsAction()
        result = action.evaluate(snapshot, derived)
        assert result.decision == ActionDecision.SKIP

    @patch.dict(os.environ, {"ENABLE_AUTO_APPLY_SUGGESTIONS": "true"}, clear=False)
    def test_execute_when_commented_inline_count_is_none(self) -> None:
        """EXECUTE when COMMENTED and inline count is unknown/None (fail-closed)."""
        snapshot = PRStateSnapshot(
            pr_number=1,
            review_state="COMMENTED",
            copilot_review_id=100,
            copilot_review_inline_count=cast(int, None),
        )
        derived = DerivedState(snapshot)
        action = ApplySuggestionsAction()
        result = action.evaluate(snapshot, derived)
        assert result.decision == ActionDecision.EXECUTE

    @patch.dict(os.environ, {"ENABLE_AUTO_APPLY_SUGGESTIONS": "true"}, clear=False)
    def test_execute_when_unknown_inline_count(self) -> None:
        """EXECUTE when inline count is -1 (unknown, fail-closed)."""
        snapshot = PRStateSnapshot(
            pr_number=1,
            review_state="CHANGES_REQUESTED",
            copilot_review_id=100,
            copilot_review_inline_count=-1,
        )
        derived = DerivedState(snapshot)
        action = ApplySuggestionsAction()
        result = action.evaluate(snapshot, derived)
        assert result.decision == ActionDecision.EXECUTE

    @patch.dict(os.environ, {"ENABLE_AUTO_APPLY_SUGGESTIONS": ""}, clear=False)
    def test_skip_when_feature_disabled_empty_string(self) -> None:
        """SKIP when ENABLE_AUTO_APPLY_SUGGESTIONS is empty string."""
        snapshot = PRStateSnapshot(
            pr_number=1,
            review_state="CHANGES_REQUESTED",
            copilot_review_id=100,
            copilot_review_inline_count=3,
        )
        derived = DerivedState(snapshot)
        action = ApplySuggestionsAction()
        result = action.evaluate(snapshot, derived)
        assert result.decision == ActionDecision.SKIP
        assert "disabled" in result.details.lower()
        assert result.preconditions["feature_enabled"] is False

    @patch.dict(os.environ, {"ENABLE_AUTO_APPLY_SUGGESTIONS": "false"}, clear=False)
    def test_skip_when_feature_explicitly_false(self) -> None:
        """SKIP when ENABLE_AUTO_APPLY_SUGGESTIONS is 'false'."""
        snapshot = PRStateSnapshot(
            pr_number=1,
            review_state="CHANGES_REQUESTED",
            copilot_review_id=100,
            copilot_review_inline_count=3,
        )
        derived = DerivedState(snapshot)
        action = ApplySuggestionsAction()
        result = action.evaluate(snapshot, derived)
        assert result.decision == ActionDecision.SKIP
        assert result.preconditions["feature_enabled"] is False

    @patch.dict(os.environ, {}, clear=True)
    def test_skip_when_env_var_not_set(self) -> None:
        """SKIP when ENABLE_AUTO_APPLY_SUGGESTIONS env var is not present at all."""
        snapshot = PRStateSnapshot(
            pr_number=1,
            review_state="CHANGES_REQUESTED",
            copilot_review_id=100,
            copilot_review_inline_count=3,
        )
        derived = DerivedState(snapshot)
        action = ApplySuggestionsAction()
        result = action.evaluate(snapshot, derived)
        assert result.decision == ActionDecision.SKIP
        assert result.preconditions["feature_enabled"] is False

    @patch.dict(os.environ, {"ENABLE_AUTO_APPLY_SUGGESTIONS": "true"}, clear=False)
    def test_proceeds_when_feature_enabled_lowercase(self) -> None:
        """Proceeds past feature gate when ENABLE_AUTO_APPLY_SUGGESTIONS='true'."""
        snapshot = PRStateSnapshot(
            pr_number=1,
            review_state="CHANGES_REQUESTED",
            copilot_review_id=100,
            copilot_review_inline_count=3,
        )
        derived = DerivedState(snapshot)
        action = ApplySuggestionsAction()
        result = action.evaluate(snapshot, derived)
        # Should NOT skip due to feature gate — may EXECUTE or SKIP for other reasons
        assert result.preconditions.get("feature_enabled") is True

    @patch.dict(os.environ, {"ENABLE_AUTO_APPLY_SUGGESTIONS": "TRUE"}, clear=False)
    def test_proceeds_when_feature_enabled_uppercase(self) -> None:
        """Proceeds past feature gate when ENABLE_AUTO_APPLY_SUGGESTIONS='TRUE' (case-insensitive)."""
        snapshot = PRStateSnapshot(
            pr_number=1,
            review_state="CHANGES_REQUESTED",
            copilot_review_id=100,
            copilot_review_inline_count=3,
        )
        derived = DerivedState(snapshot)
        action = ApplySuggestionsAction()
        result = action.evaluate(snapshot, derived)
        assert result.preconditions.get("feature_enabled") is True

    @patch.dict(os.environ, {"ENABLE_AUTO_APPLY_SUGGESTIONS": "True"}, clear=False)
    def test_proceeds_when_feature_enabled_mixed_case(self) -> None:
        """Proceeds past feature gate when ENABLE_AUTO_APPLY_SUGGESTIONS='True' (mixed case)."""
        snapshot = PRStateSnapshot(
            pr_number=1,
            review_state="CHANGES_REQUESTED",
            copilot_review_id=100,
            copilot_review_inline_count=3,
        )
        derived = DerivedState(snapshot)
        action = ApplySuggestionsAction()
        result = action.evaluate(snapshot, derived)
        assert result.preconditions.get("feature_enabled") is True


class TestApplySuggestionsActionExecute:
    """Tests for ApplySuggestionsAction.execute()."""

    def test_skip_when_no_suggestions_found(self) -> None:
        """SKIP when fetch returns no applicable suggestions."""
        snapshot = PRStateSnapshot(
            pr_number=1,
            review_state="CHANGES_REQUESTED",
            copilot_review_id=100,
            copilot_review_inline_count=3,
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider._repo = ""
        provider.list_issue_comments.return_value = []
        provider.find_comment.return_value = None

        with (
            patch("agentic_devtools.cli.ci.pipeline.actions.apply_suggestions.run_discovery") as mock_fetch,
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.apply_suggestions._apply_copilot_autofix_suggestions"
            ) as mock_fallback,
        ):
            # No discovery attempts → html-scrape never ran → fallback must not be called
            mock_fetch.return_value = ([], [], "PR_1")
            mock_fallback.return_value = None
            action = ApplySuggestionsAction()
            result = action.execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.SKIP
        assert "No applicable suggestions" in result.details
        mock_fallback.assert_not_called()

    def test_skip_when_threshold_exceeded(self) -> None:
        """SKIP when suggestion count exceeds threshold."""
        from agentic_devtools.cli.ci.pipeline.suggestions import SuggestedChange

        snapshot = PRStateSnapshot(
            pr_number=1,
            review_state="CHANGES_REQUESTED",
            copilot_review_id=100,
            copilot_review_inline_count=60,
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider._repo = ""
        provider.list_issue_comments.return_value = []

        # Create 51 suggestions (exceeds 50 threshold)
        suggestions = [
            SuggestedChange(
                suggestion_id=f"SC{i}",
                outdated=False,
                comment_database_id=i,
                thread_id=f"T{i}",
            )
            for i in range(51)
        ]

        with patch("agentic_devtools.cli.ci.pipeline.actions.apply_suggestions.run_discovery") as mock_fetch:
            mock_fetch.return_value = (suggestions, [], "PR_1")
            action = ApplySuggestionsAction()
            result = action.execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.SKIP
        assert "exceeds threshold" in result.details

    def test_execute_successful_batch_apply(self) -> None:
        """EXECUTE with invalidates_snapshot=True on successful apply."""
        from agentic_devtools.cli.ci.pipeline.suggestions import (
            ApplySuggestionsResult,
            SuggestedChange,
        )

        snapshot = PRStateSnapshot(
            pr_number=1,
            review_state="CHANGES_REQUESTED",
            copilot_review_id=100,
            copilot_review_inline_count=2,
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider.list_issue_comments.return_value = []

        suggestions = [
            SuggestedChange(
                suggestion_id="SC1",
                outdated=False,
                comment_database_id=101,
                thread_id="T1",
            ),
            SuggestedChange(
                suggestion_id="SC2",
                outdated=False,
                comment_database_id=102,
                thread_id="T2",
            ),
        ]

        with (
            patch("agentic_devtools.cli.ci.pipeline.actions.apply_suggestions.run_discovery") as mock_fetch,
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.apply_suggestions.apply_suggestions_with_bisection"
            ) as mock_apply,
        ):
            mock_fetch.return_value = (suggestions, [], "PR_1")
            mock_apply.return_value = ApplySuggestionsResult(
                applied_ids=["SC1", "SC2"],
                commit_shas=["abc1234"],
            )
            action = ApplySuggestionsAction()
            result = action.execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.EXECUTE
        assert result.invalidates_snapshot is True
        assert "Applied 2 suggestions" in result.details

        # Verify ExclusionContext was set
        exclusion_ctx = derived.get("exclusion_context")
        assert exclusion_ctx is not None
        assert exclusion_ctx.resolved_comment_ids == {101, 102}

    def test_skip_when_fetch_raises_exception(self) -> None:
        """SKIP (not FAILED) when discovery raises per FR-010."""
        from agentic_devtools.cli.ci.pipeline.discovery.models import (
            DiscoveryAttempt,
            DiscoveryOutcome,
        )

        snapshot = PRStateSnapshot(
            pr_number=1,
            review_state="CHANGES_REQUESTED",
            copilot_review_id=100,
            copilot_review_inline_count=3,
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider.list_issue_comments.return_value = []
        provider.find_comment.return_value = None

        error_attempt = DiscoveryAttempt(
            method="graphql",
            outcome=DiscoveryOutcome.ERROR,
            error_message="API error",
        )

        with (
            patch("agentic_devtools.cli.ci.pipeline.actions.apply_suggestions.run_discovery") as mock_fetch,
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.apply_suggestions._apply_copilot_autofix_suggestions"
            ) as mock_fallback,
        ):
            # graphql=ERROR, no html-scrape attempt → fallback must not be called
            mock_fetch.return_value = ([], [error_attempt], "")
            mock_fallback.return_value = None
            action = ApplySuggestionsAction()
            result = action.execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.SKIP
        assert "No applicable suggestions" in result.details
        mock_fallback.assert_not_called()

    def test_copilot_autofix_fallback_executes_when_no_standard_suggestions(self) -> None:
        """Copilot autofix fallback returns EXECUTE when it applies suggestions."""
        snapshot = PRStateSnapshot(
            pr_number=1,
            review_state="CHANGES_REQUESTED",
            copilot_review_id=100,
            copilot_review_inline_count=3,
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider.list_issue_comments.return_value = []

        fallback_action_result = ActionResult(
            name="apply_suggestions",
            decision=ActionDecision.EXECUTE,
            preconditions={"suggestions_found": True, "within_threshold": True},
            details="Copilot autofix: applied 1 suggestion(s)",
            invalidates_snapshot=True,
        )

        html_success_attempt = DiscoveryAttempt(
            method="html-scrape",
            outcome=DiscoveryOutcome.SUCCESS,
            suggestion_count=2,
        )

        with (
            patch("agentic_devtools.cli.ci.pipeline.actions.apply_suggestions.run_discovery") as mock_fetch,
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.apply_suggestions._apply_copilot_autofix_suggestions"
            ) as mock_fallback,
        ):
            # html-scrape=SUCCESS signals candidate autofix entries → fallback must be invoked
            mock_fetch.return_value = ([], [html_success_attempt], "")
            mock_fallback.return_value = {
                "action_result": fallback_action_result,
                "exclusion_ctx": ExclusionContext(resolved_comment_ids={101}),
            }
            action = ApplySuggestionsAction()
            result = action.execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.EXECUTE
        assert result.invalidates_snapshot is True
        assert derived.get("autofix_applied_this_iteration") is True
        assert derived.get("exclusion_context") is not None
        mock_fallback.assert_called_once()

    def test_copilot_autofix_fallback_exception_treated_as_skip(self) -> None:
        """Copilot autofix fallback exception is treated as skip (fail-open)."""
        snapshot = PRStateSnapshot(
            pr_number=1,
            review_state="CHANGES_REQUESTED",
            copilot_review_id=100,
            copilot_review_inline_count=3,
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider.list_issue_comments.return_value = []
        provider.find_comment.return_value = None

        html_success_attempt = DiscoveryAttempt(
            method="html-scrape",
            outcome=DiscoveryOutcome.SUCCESS,
            suggestion_count=1,
        )

        with (
            patch("agentic_devtools.cli.ci.pipeline.actions.apply_suggestions.run_discovery") as mock_fetch,
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.apply_suggestions._apply_copilot_autofix_suggestions"
            ) as mock_fallback,
        ):
            # html-scrape=SUCCESS → fallback is invoked, then raises
            mock_fetch.return_value = ([], [html_success_attempt], "")
            mock_fallback.side_effect = RuntimeError("Page scraping failed")
            action = ApplySuggestionsAction()
            result = action.execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.SKIP
        assert "No applicable suggestions" in result.details
        mock_fallback.assert_called_once()

    def test_copilot_autofix_fallback_skip_does_not_set_autofix_flag(self) -> None:
        """When fallback returns SKIP, autofix_applied_this_iteration is NOT set."""
        snapshot = PRStateSnapshot(
            pr_number=1,
            review_state="CHANGES_REQUESTED",
            copilot_review_id=100,
            copilot_review_inline_count=3,
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider.list_issue_comments.return_value = []

        fallback_action_result = ActionResult(
            name="apply_suggestions",
            decision=ActionDecision.SKIP,
            preconditions={"suggestions_found": True, "within_threshold": True},
            details="Copilot autofix: all 2 suggestions conflicted/stale",
        )

        html_success_attempt = DiscoveryAttempt(
            method="html-scrape",
            outcome=DiscoveryOutcome.SUCCESS,
            suggestion_count=2,
        )

        with (
            patch("agentic_devtools.cli.ci.pipeline.actions.apply_suggestions.run_discovery") as mock_fetch,
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.apply_suggestions._apply_copilot_autofix_suggestions"
            ) as mock_fallback,
        ):
            # html-scrape=SUCCESS → fallback is invoked and returns SKIP
            mock_fetch.return_value = ([], [html_success_attempt], "")
            mock_fallback.return_value = {
                "action_result": fallback_action_result,
                "exclusion_ctx": None,
            }
            action = ApplySuggestionsAction()
            result = action.execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.SKIP
        assert derived.get("autofix_applied_this_iteration") is None
        mock_fallback.assert_called_once()

    @patch.dict(os.environ, {"ENABLE_AUTO_APPLY_SUGGESTIONS": "true"}, clear=False)
    def test_legacy_fallback_not_called_when_html_scrape_empty(self) -> None:
        """Fallback is NOT invoked when html-scrape already returned EMPTY.

        Avoids a redundant second scrape of the PR page when the HTML strategy
        has already confirmed there is nothing to apply.
        """
        snapshot = PRStateSnapshot(
            pr_number=1,
            review_state="CHANGES_REQUESTED",
            copilot_review_id=100,
            copilot_review_inline_count=0,
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider.list_issue_comments.return_value = []

        html_empty_attempt = DiscoveryAttempt(
            method="html-scrape",
            outcome=DiscoveryOutcome.EMPTY,
        )

        with (
            patch("agentic_devtools.cli.ci.pipeline.actions.apply_suggestions.run_discovery") as mock_fetch,
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.apply_suggestions._apply_copilot_autofix_suggestions"
            ) as mock_fallback,
        ):
            mock_fetch.return_value = ([], [html_empty_attempt], "")
            action = ApplySuggestionsAction()
            result = action.execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.SKIP
        mock_fallback.assert_not_called()

    def test_partial_application_on_conflict(self) -> None:
        """Partial apply result is used when some suggestions conflict."""
        from agentic_devtools.cli.ci.pipeline.suggestions import (
            ApplySuggestionsResult,
            SuggestedChange,
        )

        snapshot = PRStateSnapshot(
            pr_number=1,
            review_state="CHANGES_REQUESTED",
            copilot_review_id=100,
            copilot_review_inline_count=2,
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider.list_issue_comments.return_value = []

        suggestions = [
            SuggestedChange(
                suggestion_id="SC1",
                outdated=False,
                comment_database_id=101,
                thread_id="T1",
            ),
            SuggestedChange(
                suggestion_id="SC2",
                outdated=False,
                comment_database_id=102,
                thread_id="T2",
            ),
        ]

        with (
            patch("agentic_devtools.cli.ci.pipeline.actions.apply_suggestions.run_discovery") as mock_fetch,
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.apply_suggestions.apply_suggestions_with_bisection"
            ) as mock_bisect,
        ):
            mock_fetch.return_value = (suggestions, [], "PR_1")
            mock_bisect.return_value = ApplySuggestionsResult(
                applied_ids=["SC1"],
                skipped_ids=["SC2"],
                commit_shas=["abc1234"],
            )
            action = ApplySuggestionsAction()
            result = action.execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.EXECUTE
        assert result.invalidates_snapshot is True
        mock_bisect.assert_called_once()

    def test_comment_excluded_only_when_all_suggestions_applied(self) -> None:
        """Comment is excluded only if ALL its suggestions are applied; partial apply leaves it visible."""
        from agentic_devtools.cli.ci.pipeline.suggestions import (
            ApplySuggestionsResult,
            SuggestedChange,
        )

        snapshot = PRStateSnapshot(
            pr_number=1,
            review_state="CHANGES_REQUESTED",
            copilot_review_id=100,
            copilot_review_inline_count=2,
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider.list_issue_comments.return_value = []

        # Comment 101 has two suggestions; only SC1 will be applied, SC2 conflicts
        suggestions = [
            SuggestedChange(
                suggestion_id="SC1",
                outdated=False,
                comment_database_id=101,
                thread_id="T1",
            ),
            SuggestedChange(
                suggestion_id="SC2",
                outdated=False,
                comment_database_id=101,
                thread_id="T1",
            ),
            # Comment 102 has one suggestion that is fully applied
            SuggestedChange(
                suggestion_id="SC3",
                outdated=False,
                comment_database_id=102,
                thread_id="T2",
            ),
        ]

        with (
            patch("agentic_devtools.cli.ci.pipeline.actions.apply_suggestions.run_discovery") as mock_fetch,
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.apply_suggestions.apply_suggestions_with_bisection"
            ) as mock_bisect,
        ):
            mock_fetch.return_value = (suggestions, [], "PR_1")
            mock_bisect.return_value = ApplySuggestionsResult(
                applied_ids=["SC1", "SC3"],
                skipped_ids=["SC2"],
                commit_shas=["abc1234"],
            )
            action = ApplySuggestionsAction()
            result = action.execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.EXECUTE
        exclusion_ctx = derived.get("exclusion_context")
        assert exclusion_ctx is not None
        # Comment 101 has an unapplied suggestion (SC2) — must NOT be excluded
        assert 101 not in exclusion_ctx.resolved_comment_ids
        # Comment 102 had its only suggestion applied — must be excluded
        assert 102 in exclusion_ctx.resolved_comment_ids

    def test_skip_when_batch_apply_raises_exception(self) -> None:
        """SKIP (not FAILED) when apply raises exception."""
        from agentic_devtools.cli.ci.pipeline.suggestions import SuggestedChange

        snapshot = PRStateSnapshot(
            pr_number=1,
            review_state="CHANGES_REQUESTED",
            copilot_review_id=100,
            copilot_review_inline_count=1,
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider.list_issue_comments.return_value = []
        suggestions = [
            SuggestedChange(
                suggestion_id="SC1",
                outdated=False,
                comment_database_id=101,
                thread_id="T1",
            )
        ]

        with (
            patch("agentic_devtools.cli.ci.pipeline.actions.apply_suggestions.run_discovery") as mock_fetch,
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.apply_suggestions.apply_suggestions_with_bisection"
            ) as mock_apply,
        ):
            mock_fetch.return_value = (suggestions, [], "PR_1")
            mock_apply.side_effect = RuntimeError("rate limited")
            action = ApplySuggestionsAction()
            result = action.execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.SKIP
        assert "Failed to apply suggestions" in result.details

    def test_reraises_rate_limit_from_batch_apply(self) -> None:
        """ProviderRateLimitError must propagate to the pipeline runner."""
        from agentic_devtools.cli.ci.pipeline.suggestions import SuggestedChange

        snapshot = PRStateSnapshot(
            pr_number=1,
            review_state="CHANGES_REQUESTED",
            copilot_review_id=100,
            copilot_review_inline_count=1,
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider.list_issue_comments.return_value = []
        suggestions = [
            SuggestedChange(
                suggestion_id="SC1",
                outdated=False,
                comment_database_id=101,
                thread_id="T1",
            )
        ]

        with (
            patch("agentic_devtools.cli.ci.pipeline.actions.apply_suggestions.run_discovery") as mock_fetch,
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.apply_suggestions.apply_suggestions_with_bisection"
            ) as mock_apply,
        ):
            mock_fetch.return_value = (suggestions, [], "PR_1")
            mock_apply.side_effect = ProviderRateLimitError(
                provider="github",
                credential_identity="SPECKIT_PR_TOKEN",
            )
            action = ApplySuggestionsAction()
            with pytest.raises(ProviderRateLimitError):
                action.execute(provider, snapshot, derived)

    def test_skip_when_bisection_applies_nothing(self) -> None:
        """SKIP when apply returns nothing (all conflicted)."""
        from agentic_devtools.cli.ci.pipeline.suggestions import (
            ApplySuggestionsResult,
            SuggestedChange,
        )

        snapshot = PRStateSnapshot(
            pr_number=1,
            review_state="CHANGES_REQUESTED",
            copilot_review_id=100,
            copilot_review_inline_count=2,
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider.list_issue_comments.return_value = []

        suggestions = [
            SuggestedChange(
                suggestion_id="SC1",
                outdated=False,
                comment_database_id=101,
                thread_id="T1",
            ),
        ]

        with (
            patch("agentic_devtools.cli.ci.pipeline.actions.apply_suggestions.run_discovery") as mock_fetch,
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.apply_suggestions.apply_suggestions_with_bisection"
            ) as mock_bisect,
        ):
            mock_fetch.return_value = (suggestions, [], "PR_1")
            mock_bisect.return_value = ApplySuggestionsResult(
                skipped_ids=["SC1"],
                error="Single suggestion conflict",
            )
            action = ApplySuggestionsAction()
            result = action.execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.SKIP
        assert "No suggestions applied" in result.details

    def test_post_summary_comment_with_skipped(self) -> None:
        """Summary comment includes skipped count."""
        from agentic_devtools.cli.ci.pipeline.suggestions import (
            ApplySuggestionsResult,
            SuggestedChange,
        )

        snapshot = PRStateSnapshot(
            pr_number=1,
            review_state="CHANGES_REQUESTED",
            copilot_review_id=100,
            copilot_review_inline_count=3,
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider.list_issue_comments.return_value = []

        suggestions = [
            SuggestedChange(
                suggestion_id="SC1",
                outdated=False,
                comment_database_id=101,
                thread_id="T1",
            ),
            SuggestedChange(
                suggestion_id="SC2",
                outdated=False,
                comment_database_id=102,
                thread_id="T2",
            ),
            SuggestedChange(
                suggestion_id="SC3",
                outdated=False,
                comment_database_id=103,
                thread_id="T3",
            ),
        ]

        with (
            patch("agentic_devtools.cli.ci.pipeline.actions.apply_suggestions.run_discovery") as mock_fetch,
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.apply_suggestions.apply_suggestions_with_bisection"
            ) as mock_apply,
        ):
            mock_fetch.return_value = (suggestions, [], "PR_1")
            mock_apply.return_value = ApplySuggestionsResult(
                applied_ids=["SC1", "SC2"],
                skipped_ids=["SC3"],
                commit_shas=["abc1234"],
            )
            action = ApplySuggestionsAction()
            result = action.execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.EXECUTE
        # Verify post_comment was called with skipped info
        comment_body = provider.post_comment.call_args[0][1]
        assert "1 suggestion" in comment_body
        assert "could not be applied" in comment_body

    def test_post_summary_comment_failure_does_not_crash(self) -> None:
        """post_comment failure is logged but does not crash."""
        from agentic_devtools.cli.ci.pipeline.suggestions import (
            ApplySuggestionsResult,
            SuggestedChange,
        )

        snapshot = PRStateSnapshot(
            pr_number=1,
            review_state="CHANGES_REQUESTED",
            copilot_review_id=100,
            copilot_review_inline_count=1,
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider.list_issue_comments.return_value = []
        provider.post_comment.side_effect = RuntimeError("Network error")

        suggestions = [
            SuggestedChange(
                suggestion_id="SC1",
                outdated=False,
                comment_database_id=101,
                thread_id="T1",
            ),
        ]

        with (
            patch("agentic_devtools.cli.ci.pipeline.actions.apply_suggestions.run_discovery") as mock_fetch,
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.apply_suggestions.apply_suggestions_with_bisection"
            ) as mock_apply,
        ):
            mock_fetch.return_value = (suggestions, [], "PR_1")
            mock_apply.return_value = ApplySuggestionsResult(
                applied_ids=["SC1"],
                commit_shas=["abc1234"],
            )
            action = ApplySuggestionsAction()
            result = action.execute(provider, snapshot, derived)

        # Should still succeed despite post_comment failure
        assert result.decision == ActionDecision.EXECUTE

    def test_post_summary_no_sha_list_when_pending_refresh(self) -> None:
        """Summary omits commit list when only pending_refresh sha present."""
        from agentic_devtools.cli.ci.pipeline.suggestions import (
            ApplySuggestionsResult,
            SuggestedChange,
        )

        snapshot = PRStateSnapshot(
            pr_number=1,
            review_state="CHANGES_REQUESTED",
            copilot_review_id=100,
            copilot_review_inline_count=1,
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider.list_issue_comments.return_value = []

        suggestions = [
            SuggestedChange(
                suggestion_id="SC1",
                outdated=False,
                comment_database_id=101,
                thread_id="T1",
            ),
        ]

        with (
            patch("agentic_devtools.cli.ci.pipeline.actions.apply_suggestions.run_discovery") as mock_fetch,
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.apply_suggestions.apply_suggestions_with_bisection"
            ) as mock_apply,
        ):
            mock_fetch.return_value = (suggestions, [], "PR_1")
            mock_apply.return_value = ApplySuggestionsResult(
                applied_ids=["SC1"],
                commit_shas=["pending_refresh"],
            )
            action = ApplySuggestionsAction()
            result = action.execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.EXECUTE
        comment_body = provider.post_comment.call_args[0][1]
        # Should not include commit sha when only "pending_refresh"
        assert "pending_refresh" not in comment_body

    def test_post_summary_no_commit_shas(self) -> None:
        """Summary comment when commit_shas is empty."""
        from agentic_devtools.cli.ci.pipeline.suggestions import (
            ApplySuggestionsResult,
            SuggestedChange,
        )

        snapshot = PRStateSnapshot(
            pr_number=1,
            review_state="CHANGES_REQUESTED",
            copilot_review_id=100,
            copilot_review_inline_count=1,
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider.list_issue_comments.return_value = []

        suggestions = [
            SuggestedChange(
                suggestion_id="SC1",
                outdated=False,
                comment_database_id=101,
                thread_id="T1",
            ),
        ]

        with (
            patch("agentic_devtools.cli.ci.pipeline.actions.apply_suggestions.run_discovery") as mock_fetch,
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.apply_suggestions.apply_suggestions_with_bisection"
            ) as mock_apply,
        ):
            mock_fetch.return_value = (suggestions, [], "PR_1")
            mock_apply.return_value = ApplySuggestionsResult(
                applied_ids=["SC1"],
                commit_shas=[],
            )
            action = ApplySuggestionsAction()
            result = action.execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.EXECUTE
        comment_body = provider.post_comment.call_args[0][1]
        assert "Auto-applied 1 suggestion" in comment_body
        assert "commit" not in comment_body

    def test_skip_when_autofix_cycle_limit_reached(self) -> None:
        """SKIP when prior autofix count >= _MAX_AUTOFIX_CYCLES."""
        snapshot = PRStateSnapshot(
            pr_number=1,
            review_state="CHANGES_REQUESTED",
            copilot_review_id=100,
            copilot_review_inline_count=3,
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()

        # Simulate 20 prior autofix comments
        mock_comments = [MagicMock(body="🔧 **Auto-applied 2 suggestions** in commit `abc1234`") for _ in range(20)]
        provider.list_issue_comments.return_value = mock_comments

        action = ApplySuggestionsAction()
        result = action.execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.SKIP
        assert "cycle limit" in result.details.lower()
        assert result.preconditions.get("cycle_limit_reached") is True

    def test_proceeds_when_under_cycle_limit(self) -> None:
        """Proceeds past cycle limit when count < _MAX_AUTOFIX_CYCLES."""
        snapshot = PRStateSnapshot(
            pr_number=1,
            review_state="CHANGES_REQUESTED",
            copilot_review_id=100,
            copilot_review_inline_count=3,
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()

        # Simulate 5 prior autofix comments (under limit)
        mock_comments = [MagicMock(body="🔧 **Auto-applied 1 suggestion** in commit `abc1234`") for _ in range(5)]
        provider.list_issue_comments.return_value = mock_comments

        with patch("agentic_devtools.cli.ci.pipeline.actions.apply_suggestions.run_discovery") as mock_fetch:
            mock_fetch.return_value = ([], [], "PR_1")
            action = ApplySuggestionsAction()
            result = action.execute(provider, snapshot, derived)

        # Should pass cycle check but SKIP due to no suggestions
        assert result.decision == ActionDecision.SKIP
        assert "No applicable suggestions" in result.details

    def test_proceeds_when_cycle_count_check_fails(self) -> None:
        """Fail-open: proceeds when list_issue_comments raises exception."""
        snapshot = PRStateSnapshot(
            pr_number=1,
            review_state="CHANGES_REQUESTED",
            copilot_review_id=100,
            copilot_review_inline_count=3,
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider.list_issue_comments.side_effect = RuntimeError("API error")

        with patch("agentic_devtools.cli.ci.pipeline.actions.apply_suggestions.run_discovery") as mock_fetch:
            mock_fetch.return_value = ([], [], "PR_1")
            action = ApplySuggestionsAction()
            result = action.execute(provider, snapshot, derived)

        # Should proceed past cycle check (fail-open) and SKIP for no suggestions
        assert result.decision == ActionDecision.SKIP
        assert "No applicable suggestions" in result.details

    def test_non_autofix_comments_not_counted(self) -> None:
        """Only comments with the autofix prefix are counted toward cycle limit."""
        snapshot = PRStateSnapshot(
            pr_number=1,
            review_state="CHANGES_REQUESTED",
            copilot_review_id=100,
            copilot_review_inline_count=3,
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()

        # Mix of autofix comments and regular comments
        mock_comments = [
            MagicMock(body="🔧 **Auto-applied 1 suggestion** in commit `abc1234`"),
            MagicMock(body="Regular comment about the PR"),
            MagicMock(body="Another regular comment"),
            MagicMock(body=None),  # Edge case: None body
        ]
        provider.list_issue_comments.return_value = mock_comments

        with patch("agentic_devtools.cli.ci.pipeline.actions.apply_suggestions.run_discovery") as mock_fetch:
            mock_fetch.return_value = ([], [], "PR_1")
            action = ApplySuggestionsAction()
            result = action.execute(provider, snapshot, derived)

        # Only 1 autofix comment (under limit of 20), so should proceed
        assert result.decision == ActionDecision.SKIP
        assert "No applicable suggestions" in result.details


def test_count_prior_autofix_comments_helper() -> None:
    """_count_prior_autofix_comments counts only autofix summary comments."""
    from agentic_devtools.cli.ci.pipeline.actions.apply_suggestions import _count_prior_autofix_comments

    provider = MagicMock()
    provider.list_issue_comments.return_value = [
        MagicMock(body="🔧 **Auto-applied 2 suggestions** in commit `abc1234`"),
        MagicMock(body="Regular comment"),
        MagicMock(body="🔧 **Auto-applied 1 suggestion**"),
        MagicMock(body=None),
        MagicMock(body=""),
    ]

    count = _count_prior_autofix_comments(provider, 42)
    assert count == 2


def test_count_prior_autofix_comments_returns_zero_on_exception() -> None:
    """Returns 0 when list_issue_comments raises."""
    from agentic_devtools.cli.ci.pipeline.actions.apply_suggestions import _count_prior_autofix_comments

    provider = MagicMock()
    provider.list_issue_comments.side_effect = RuntimeError("API error")

    count = _count_prior_autofix_comments(provider, 42)
    assert count == 0


class TestApplyCopilotAutofixSuggestions:
    """Tests for _apply_copilot_autofix_suggestions fallback function."""

    def test_returns_none_when_no_suggestions(self) -> None:
        """Returns None when apply_pr_suggestions reports 0 applied, 0 skipped."""
        provider = MagicMock()
        provider._repo = "owner/repo"
        snapshot = PRStateSnapshot(pr_number=1)

        with patch("agentic_devtools.cli.github.apply_thread_autofix.apply_pr_suggestions") as mock_apply:
            mock_apply.return_value = {
                "applied": 0,
                "skipped": 0,
                "conflict_comment_ids": [],
                "commit": None,
                "files_changed": [],
                "resolution": None,
            }
            result = _apply_copilot_autofix_suggestions(provider, snapshot)

        assert result is None

    def test_returns_execute_when_applied(self) -> None:
        """Returns action_result with EXECUTE when suggestions are applied."""
        provider = MagicMock()
        provider._repo = "owner/repo"
        snapshot = PRStateSnapshot(pr_number=1)

        with patch("agentic_devtools.cli.github.apply_thread_autofix.apply_pr_suggestions") as mock_apply:
            mock_apply.return_value = {
                "applied": 2,
                "skipped": 1,
                "conflict_comment_ids": [999],
                "commit": "abc123def456",
                "files_changed": ["file.py"],
                "resolution": {"replied": 2, "resolved": 2},
            }
            result = _apply_copilot_autofix_suggestions(provider, snapshot)

        assert result is not None
        assert result["action_result"].decision == ActionDecision.EXECUTE
        assert result["action_result"].invalidates_snapshot is True
        assert "applied 2" in result["action_result"].details

    def test_returns_skip_when_all_conflicted(self) -> None:
        """Returns SKIP when all suggestions are skipped (conflicts)."""
        provider = MagicMock()
        provider._repo = "owner/repo"
        snapshot = PRStateSnapshot(pr_number=1)

        with patch("agentic_devtools.cli.github.apply_thread_autofix.apply_pr_suggestions") as mock_apply:
            mock_apply.return_value = {
                "applied": 0,
                "skipped": 3,
                "conflict_comment_ids": [1, 2, 3],
                "commit": None,
                "files_changed": [],
                "resolution": None,
            }
            result = _apply_copilot_autofix_suggestions(provider, snapshot)

        assert result is not None
        assert result["action_result"].decision == ActionDecision.SKIP
        assert "conflicted" in result["action_result"].details

    def test_returns_none_on_system_exit(self) -> None:
        """Returns None when apply_pr_suggestions calls sys.exit."""
        provider = MagicMock()
        provider._repo = "owner/repo"
        snapshot = PRStateSnapshot(pr_number=1)

        with patch("agentic_devtools.cli.github.apply_thread_autofix.apply_pr_suggestions") as mock_apply:
            mock_apply.side_effect = SystemExit(1)
            result = _apply_copilot_autofix_suggestions(provider, snapshot)

        assert result is None

    def test_returns_none_on_exception(self) -> None:
        """Returns None when apply_pr_suggestions raises."""
        provider = MagicMock()
        provider._repo = "owner/repo"
        snapshot = PRStateSnapshot(pr_number=1)

        with patch("agentic_devtools.cli.github.apply_thread_autofix.apply_pr_suggestions") as mock_apply:
            mock_apply.side_effect = RuntimeError("Network error")
            result = _apply_copilot_autofix_suggestions(provider, snapshot)

        assert result is None

    def test_uses_github_repository_env_when_no_repo_attr(self) -> None:
        """Falls back to GITHUB_REPOSITORY env var when provider has no _repo."""
        provider = MagicMock(spec=[])  # No _repo attribute
        snapshot = PRStateSnapshot(pr_number=1)

        with (
            patch("agentic_devtools.cli.github.apply_thread_autofix.apply_pr_suggestions") as mock_apply,
            patch.dict("os.environ", {"GITHUB_REPOSITORY": "env/repo"}),
        ):
            mock_apply.return_value = {
                "applied": 1,
                "skipped": 0,
                "conflict_comment_ids": [],
                "commit": "abc123",
                "files_changed": ["f.py"],
                "resolution": None,
            }
            _apply_copilot_autofix_suggestions(provider, snapshot)

        mock_apply.assert_called_once()
        assert mock_apply.call_args.kwargs["repo"] == "env/repo"

    def test_returns_none_when_repo_cannot_be_determined(self) -> None:
        """Returns None early when neither provider._repo nor GITHUB_REPOSITORY is set."""
        provider = MagicMock(spec=[])  # No _repo attribute
        snapshot = PRStateSnapshot(pr_number=1)

        with (
            patch("agentic_devtools.cli.github.apply_thread_autofix.apply_pr_suggestions") as mock_apply,
            patch.dict("os.environ", {}, clear=True),
        ):
            result = _apply_copilot_autofix_suggestions(provider, snapshot)

        mock_apply.assert_not_called()
        assert result is None


class TestHtmlScrapeSucceeded:
    """Tests for _html_scrape_succeeded helper."""

    def test_returns_false_for_empty_attempts(self) -> None:
        assert _html_scrape_succeeded([]) is False

    def test_returns_false_when_html_scrape_is_empty(self) -> None:
        attempts = [DiscoveryAttempt(method="html-scrape", outcome=DiscoveryOutcome.EMPTY)]
        assert _html_scrape_succeeded(attempts) is False

    def test_returns_false_when_html_scrape_is_error(self) -> None:
        attempts = [DiscoveryAttempt(method="html-scrape", outcome=DiscoveryOutcome.ERROR)]
        assert _html_scrape_succeeded(attempts) is False

    def test_returns_false_when_no_html_scrape_attempt(self) -> None:
        attempts = [DiscoveryAttempt(method="graphql", outcome=DiscoveryOutcome.SUCCESS)]
        assert _html_scrape_succeeded(attempts) is False

    def test_returns_true_when_html_scrape_is_success(self) -> None:
        attempts = [DiscoveryAttempt(method="html-scrape", outcome=DiscoveryOutcome.SUCCESS, suggestion_count=3)]
        assert _html_scrape_succeeded(attempts) is True

    def test_returns_true_when_one_of_many_is_html_success(self) -> None:
        attempts = [
            DiscoveryAttempt(method="graphql", outcome=DiscoveryOutcome.EMPTY),
            DiscoveryAttempt(method="rest-rederivation", outcome=DiscoveryOutcome.EMPTY),
            DiscoveryAttempt(method="html-scrape", outcome=DiscoveryOutcome.SUCCESS, suggestion_count=1),
        ]
        assert _html_scrape_succeeded(attempts) is True


class TestFormatDiscoveryDetails:
    """Tests for _format_discovery_details helper."""

    def test_returns_no_attempts_when_empty(self) -> None:
        snapshot = PRStateSnapshot(pr_number=1, copilot_review_inline_count=0)
        result = _format_discovery_details([], snapshot)
        assert result == "no discovery attempts"

    def test_includes_suggestion_count_for_success(self) -> None:
        snapshot = PRStateSnapshot(pr_number=1, copilot_review_inline_count=2)
        attempts = [
            DiscoveryAttempt(
                method="graphql",
                outcome=DiscoveryOutcome.SUCCESS,
                suggestion_count=3,
            )
        ]
        result = _format_discovery_details(attempts, snapshot)
        assert "graphql=success(3)" in result
        assert "inline_comments=2" in result

    def test_includes_error_message(self) -> None:
        snapshot = PRStateSnapshot(pr_number=1, copilot_review_inline_count=1)
        attempts = [
            DiscoveryAttempt(
                method="rest-rederivation",
                outcome=DiscoveryOutcome.ERROR,
                error_message="API timeout occurred",
            )
        ]
        result = _format_discovery_details(attempts, snapshot)
        assert "rest-rederivation=error(API timeout occurred)" in result

    def test_error_message_whitespace_normalized(self) -> None:
        """Newlines and extra spaces in error_message are collapsed to single spaces."""
        snapshot = PRStateSnapshot(pr_number=1, copilot_review_inline_count=1)
        attempts = [
            DiscoveryAttempt(
                method="graphql",
                outcome=DiscoveryOutcome.ERROR,
                error_message="line one\nline two\n  extra  spaces  ",
            )
        ]
        result = _format_discovery_details(attempts, snapshot)
        assert "graphql=error(line one line two extra spaces)" in result

    def test_error_message_truncated_at_200(self) -> None:
        """error_message longer than 200 chars is truncated after whitespace normalization."""
        snapshot = PRStateSnapshot(pr_number=1, copilot_review_inline_count=0)
        long_msg = "x" * 250
        attempts = [
            DiscoveryAttempt(
                method="graphql",
                outcome=DiscoveryOutcome.ERROR,
                error_message=long_msg,
            )
        ]
        result = _format_discovery_details(attempts, snapshot)
        assert f"graphql=error({'x' * 200})" in result
        assert "x" * 201 not in result

    def test_no_suffix_when_no_error_and_no_suggestion_count(self) -> None:
        """Branch 361->363: neither error_message nor suggestion_count."""
        snapshot = PRStateSnapshot(pr_number=1, copilot_review_inline_count=0)
        attempts = [
            DiscoveryAttempt(
                method="graphql",
                outcome=DiscoveryOutcome.EMPTY,
                suggestion_count=0,
            )
        ]
        result = _format_discovery_details(attempts, snapshot)
        assert "graphql=empty" in result
        assert "()" not in result


class TestPostDeferralIfNeeded:
    """Tests for deferral posting branch in execute."""

    @patch.dict(os.environ, {"ENABLE_AUTO_APPLY_SUGGESTIONS": "true"}, clear=False)
    def test_deferral_posted_when_all_attempts_empty(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=1,
            review_state="CHANGES_REQUESTED",
            copilot_review_id=100,
            copilot_review_inline_count=2,
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider.list_issue_comments.return_value = []

        attempts = [
            DiscoveryAttempt(method="graphql", outcome=DiscoveryOutcome.EMPTY),
            DiscoveryAttempt(method="rest-rederivation", outcome=DiscoveryOutcome.EMPTY),
        ]

        with (
            patch("agentic_devtools.cli.ci.pipeline.actions.apply_suggestions.run_discovery") as mock_discovery,
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.apply_suggestions._apply_copilot_autofix_suggestions"
            ) as mock_fallback,
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.apply_suggestions._post_deferral_if_needed"
            ) as mock_deferral,
        ):
            mock_discovery.return_value = ([], attempts, "PR_1")
            mock_fallback.return_value = None
            action = ApplySuggestionsAction()
            result = action.execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.SKIP
        mock_deferral.assert_called_once_with(provider, snapshot)

    @patch.dict(os.environ, {"ENABLE_AUTO_APPLY_SUGGESTIONS": "true"}, clear=False)
    def test_no_deferral_posted_when_inline_count_zero(self) -> None:
        """No deferral when COMMENTED review has confirmed zero inline comments.

        With an empty discovery-attempts list _all_discovery_attempts_empty returns
        False, so the deferral guard is not reached for any snapshot.  The real
        "confirmed zero" guard is exercised by
        test_no_deferral_posted_when_commented_with_confirmed_zero_inline_count.
        """
        snapshot = PRStateSnapshot(
            pr_number=1,
            review_state="COMMENTED",
            copilot_review_id=100,
            copilot_review_inline_count=0,  # confirmed zero
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider.list_issue_comments.return_value = []

        with (
            patch("agentic_devtools.cli.ci.pipeline.actions.apply_suggestions.run_discovery") as mock_discovery,
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.apply_suggestions._apply_copilot_autofix_suggestions"
            ) as mock_fallback,
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.apply_suggestions._post_deferral_if_needed"
            ) as mock_deferral,
        ):
            mock_discovery.return_value = ([], [], "PR_1")
            mock_fallback.return_value = None
            action = ApplySuggestionsAction()
            result = action.execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.SKIP
        mock_deferral.assert_not_called()

    @patch.dict(os.environ, {"ENABLE_AUTO_APPLY_SUGGESTIONS": "true"}, clear=False)
    def test_no_deferral_posted_when_commented_with_confirmed_zero_inline_count(self) -> None:
        """No deferral when COMMENTED review has confirmed zero inline comments, even with attempts."""
        snapshot = PRStateSnapshot(
            pr_number=1,
            review_state="COMMENTED",
            copilot_review_id=100,
            copilot_review_inline_count=0,  # confirmed zero: fetch succeeded with 0
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider.list_issue_comments.return_value = []

        attempts = [
            DiscoveryAttempt(method="graphql", outcome=DiscoveryOutcome.EMPTY),
            DiscoveryAttempt(method="rest-rederivation", outcome=DiscoveryOutcome.EMPTY),
        ]

        with (
            patch("agentic_devtools.cli.ci.pipeline.actions.apply_suggestions.run_discovery") as mock_discovery,
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.apply_suggestions._apply_copilot_autofix_suggestions"
            ) as mock_fallback,
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.apply_suggestions._post_deferral_if_needed"
            ) as mock_deferral,
        ):
            mock_discovery.return_value = ([], attempts, "PR_1")
            mock_fallback.return_value = None
            action = ApplySuggestionsAction()
            result = action.execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.SKIP
        mock_deferral.assert_not_called()

    @patch.dict(os.environ, {"ENABLE_AUTO_APPLY_SUGGESTIONS": "true"}, clear=False)
    def test_deferral_posted_for_changes_requested_with_zero_inline_count(self) -> None:
        """Deferral IS posted for CHANGES_REQUESTED even when inline_count=0.

        The snapshot builder does not count inline comments for CHANGES_REQUESTED
        reviews, so inline_count=0 means "not tracked" (not "confirmed zero").
        When all discovery attempts return EMPTY, deferral must be posted.
        """
        snapshot = PRStateSnapshot(
            pr_number=1,
            review_state="CHANGES_REQUESTED",
            copilot_review_id=100,
            copilot_review_inline_count=0,  # not tracked for CHANGES_REQUESTED
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider.list_issue_comments.return_value = []

        attempts = [
            DiscoveryAttempt(method="graphql", outcome=DiscoveryOutcome.EMPTY),
            DiscoveryAttempt(method="rest-rederivation", outcome=DiscoveryOutcome.EMPTY),
        ]

        with (
            patch("agentic_devtools.cli.ci.pipeline.actions.apply_suggestions.run_discovery") as mock_discovery,
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.apply_suggestions._apply_copilot_autofix_suggestions"
            ) as mock_fallback,
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.apply_suggestions._post_deferral_if_needed"
            ) as mock_deferral,
        ):
            mock_discovery.return_value = ([], attempts, "PR_1")
            mock_fallback.return_value = None
            action = ApplySuggestionsAction()
            result = action.execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.SKIP
        mock_deferral.assert_called_once_with(provider, snapshot)

    @patch.dict(os.environ, {"ENABLE_AUTO_APPLY_SUGGESTIONS": "true"}, clear=False)
    def test_no_deferral_posted_when_discovery_reports_error(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=1,
            review_state="CHANGES_REQUESTED",
            copilot_review_id=100,
            copilot_review_inline_count=2,
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider.list_issue_comments.return_value = []

        attempts = [DiscoveryAttempt(method="graphql", outcome=DiscoveryOutcome.ERROR, error_message="boom")]

        with (
            patch("agentic_devtools.cli.ci.pipeline.actions.apply_suggestions.run_discovery") as mock_discovery,
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.apply_suggestions._apply_copilot_autofix_suggestions"
            ) as mock_fallback,
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.apply_suggestions._post_deferral_if_needed"
            ) as mock_deferral,
        ):
            mock_discovery.return_value = ([], attempts, "PR_1")
            mock_fallback.return_value = None
            action = ApplySuggestionsAction()
            result = action.execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.SKIP
        mock_deferral.assert_not_called()

    @patch.dict(os.environ, {"ENABLE_AUTO_APPLY_SUGGESTIONS": "true"}, clear=False)
    def test_no_deferral_posted_when_anchored_without_replacement(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=1,
            review_state="CHANGES_REQUESTED",
            copilot_review_id=100,
            copilot_review_inline_count=2,
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider.list_issue_comments.return_value = []

        attempts = [
            DiscoveryAttempt(
                method="rest-rederivation",
                outcome=DiscoveryOutcome.ANCHORED_NO_REPLACEMENT,
            )
        ]

        with (
            patch("agentic_devtools.cli.ci.pipeline.actions.apply_suggestions.run_discovery") as mock_discovery,
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.apply_suggestions._apply_copilot_autofix_suggestions"
            ) as mock_fallback,
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.apply_suggestions._post_deferral_if_needed"
            ) as mock_deferral,
        ):
            mock_discovery.return_value = ([], attempts, "PR_1")
            mock_fallback.return_value = None
            action = ApplySuggestionsAction()
            result = action.execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.SKIP
        mock_deferral.assert_not_called()

    def test_logs_warning_when_post_deferral_marker_raises(self) -> None:
        """Deferral helper logs and swallows posting failures."""
        snapshot = PRStateSnapshot(pr_number=1, copilot_review_id=100)
        provider = MagicMock()

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.deferral.post_deferral_marker",
                side_effect=RuntimeError("boom"),
            ),
            patch("agentic_devtools.cli.ci.pipeline.actions.apply_suggestions.logger.warning") as mock_warning,
        ):
            _post_deferral_if_needed(provider, snapshot)

        mock_warning.assert_called_once()

    def test_post_deferral_re_raises_rate_limit_error(self) -> None:
        snapshot = PRStateSnapshot(pr_number=1, copilot_review_id=100)
        provider = MagicMock()

        with patch(
            "agentic_devtools.cli.ci.pipeline.deferral.post_deferral_marker",
            side_effect=ProviderRateLimitError(is_rate_limit=True),
        ):
            with pytest.raises(ProviderRateLimitError):
                _post_deferral_if_needed(provider, snapshot)

    @patch.dict(os.environ, {"ENABLE_AUTO_APPLY_SUGGESTIONS": "true"}, clear=False)
    def test_execute_re_raises_rate_limit_from_apply_suggestions(self) -> None:
        from agentic_devtools.cli.ci.pipeline.suggestions import SuggestedChange

        snapshot = PRStateSnapshot(
            pr_number=1,
            review_state="CHANGES_REQUESTED",
            copilot_review_id=100,
            copilot_review_inline_count=3,
        )
        provider = MagicMock()
        suggestions = [SuggestedChange(suggestion_id="S1", outdated=False, comment_database_id=1, thread_id="T1")]

        with (
            patch("agentic_devtools.cli.ci.pipeline.actions.apply_suggestions.run_discovery") as mock_discovery,
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.apply_suggestions.apply_suggestions_with_bisection",
                side_effect=ProviderRateLimitError(is_rate_limit=True),
            ),
        ):
            mock_discovery.return_value = (suggestions, [], "PR_1")
            with pytest.raises(ProviderRateLimitError):
                ApplySuggestionsAction().execute(provider, snapshot, DerivedState(snapshot))
