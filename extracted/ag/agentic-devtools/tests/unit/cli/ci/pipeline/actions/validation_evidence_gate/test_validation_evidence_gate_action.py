"""Tests for ValidationEvidenceGateAction."""

from unittest.mock import MagicMock, call, patch

import pytest

from agentic_devtools.cli.ci.models import COPILOT_REVIEWER_LOGIN, IssueCommentInfo
from agentic_devtools.cli.ci.pipeline.actions.validation_evidence_gate import ValidationEvidenceGateAction
from agentic_devtools.cli.ci.pipeline.models import ActionDecision, ActionResult
from agentic_devtools.cli.ci.pipeline.snapshot_models import DerivedState, PRStateSnapshot
from agentic_devtools.cli.ci.pipeline.validation_evidence import (
    BLOCKER_MARKER,
    EVIDENCE_REQUIRED_LABEL,
    FOLLOWUP_KEY,
    GATE_STATE_KEY,
    RECOVERY_MARKER,
    EvidenceGateState,
    build_blocker_comment,
    build_recovery_request,
    find_head_evidence,
)
from agentic_devtools.cli.shared.retry import ProviderRateLimitError

HEAD_SHA = "0123456789abcdef0123456789abcdef01234567"
OLDER_SHA = "fedcba9876543210fedcba9876543210fedcba98"
ACTION_MODULE = "agentic_devtools.cli.ci.pipeline.actions.validation_evidence_gate"


def _snapshot(
    *,
    head_sha: str = HEAD_SHA,
    labels: list[str] | None = None,
    is_draft: bool = True,
    has_changes: bool = True,
) -> PRStateSnapshot:
    return PRStateSnapshot(
        pr_number=42,
        pr_id=4200,
        head_sha=head_sha,
        head_branch="feature/validation",
        base_repo_full_name="owner/repo",
        labels=labels if labels is not None else [EVIDENCE_REQUIRED_LABEL],
        is_draft=is_draft,
        has_changes=has_changes,
    )


def _provider(
    comments: list[IssueCommentInfo] | None = None,
    linked_labels: list[str] | None = None,
) -> MagicMock:
    provider = MagicMock()
    provider.list_issue_comments.return_value = comments or []
    provider.list_linked_issue_labels.return_value = linked_labels or []
    return provider


def _evaluate(
    snapshot: PRStateSnapshot,
    provider: MagicMock,
    *,
    active_session: bool | None = False,
) -> tuple[ActionResult, DerivedState, MagicMock]:
    derived = DerivedState(snapshot)
    derived.set("provider", provider)
    with patch(f"{ACTION_MODULE}.is_copilot_session_active_via_agent_task", return_value=active_session) as detector:
        result = ValidationEvidenceGateAction().evaluate(snapshot, derived)
    return result, derived, detector


def _comment(
    author: str,
    body: str,
    created_at: str = "2026-10-27T10:00:00Z",
) -> IssueCommentInfo:
    return IssueCommentInfo(id=1, author=author, body=body, created_at=created_at)


class TestValidationEvidenceGateAction:
    def test_action_contract(self) -> None:
        action = ValidationEvidenceGateAction()

        assert action.name == "validation_evidence_gate"
        assert action.may_invalidate_snapshot is False
        assert action.runs_after_invalidation is True

    @pytest.mark.parametrize(("is_draft", "has_changes"), [(False, True), (True, False)])
    def test_not_applicable_preconditions_make_no_provider_calls(self, is_draft: bool, has_changes: bool) -> None:
        provider = _provider()
        snapshot = _snapshot(is_draft=is_draft, has_changes=has_changes)

        result, derived, _ = _evaluate(snapshot, provider)

        assert result.decision is ActionDecision.SKIP
        assert derived.get(GATE_STATE_KEY) is EvidenceGateState.NOT_APPLICABLE
        provider.list_linked_issue_labels.assert_not_called()
        provider.list_issue_comments.assert_not_called()

    def test_sets_unknown_before_linked_label_lookup(self) -> None:
        provider = _provider()
        provider.list_linked_issue_labels.side_effect = ValueError("unavailable")
        snapshot = _snapshot(labels=[])
        derived = DerivedState(snapshot)
        derived.set("provider", provider)

        with patch.object(derived, "set", wraps=derived.set) as set_state:
            result = ValidationEvidenceGateAction().evaluate(snapshot, derived)

        assert result.decision is ActionDecision.SKIP
        assert derived.get(GATE_STATE_KEY) is EvidenceGateState.UNKNOWN
        assert set_state.call_args_list[0] == call(GATE_STATE_KEY, EvidenceGateState.UNKNOWN)

    def test_linked_issue_label_opts_in_and_pr_label_avoids_linked_lookup(self) -> None:
        linked_provider = _provider(linked_labels=[EVIDENCE_REQUIRED_LABEL])
        linked_result, linked_derived, _ = _evaluate(_snapshot(labels=[]), linked_provider)
        pr_provider = _provider()
        pr_result, pr_derived, _ = _evaluate(_snapshot(), pr_provider)

        assert linked_result.decision is ActionDecision.EXECUTE
        assert linked_derived.get(GATE_STATE_KEY) is EvidenceGateState.MISSING
        linked_provider.list_linked_issue_labels.assert_called_once_with(42)
        assert pr_result.decision is ActionDecision.EXECUTE
        assert pr_derived.get(GATE_STATE_KEY) is EvidenceGateState.MISSING
        pr_provider.list_linked_issue_labels.assert_not_called()

    def test_no_opt_in_is_not_applicable(self) -> None:
        provider = _provider()

        result, derived, detector = _evaluate(_snapshot(labels=[]), provider)

        assert result.decision is ActionDecision.SKIP
        assert derived.get(GATE_STATE_KEY) is EvidenceGateState.NOT_APPLICABLE
        provider.list_linked_issue_labels.assert_called_once_with(42)
        provider.list_issue_comments.assert_not_called()
        detector.assert_not_called()

    def test_invalid_sha_stays_unknown_without_loading_comments(self) -> None:
        provider = _provider()

        result, derived, detector = _evaluate(_snapshot(head_sha="not-a-full-sha"), provider)

        assert result.decision is ActionDecision.SKIP
        assert derived.get(GATE_STATE_KEY) is EvidenceGateState.UNKNOWN
        provider.list_issue_comments.assert_not_called()
        detector.assert_not_called()

    def test_current_head_evidence_satisfies_gate_after_quoted_request(self) -> None:
        evidence = _comment("Copilot", f"> @copilot please add evidence\n\n## Validation evidence\n{HEAD_SHA[:7]}")
        assert find_head_evidence([evidence], HEAD_SHA) is evidence
        provider = _provider(comments=[evidence])

        result, derived, detector = _evaluate(_snapshot(), provider)

        assert result.decision is ActionDecision.SKIP
        assert derived.get(GATE_STATE_KEY) is EvidenceGateState.SATISFIED
        detector.assert_not_called()

    def test_evidence_for_older_head_does_not_satisfy_gate(self) -> None:
        provider = _provider(comments=[_comment("Copilot", f"## Validation evidence\n{OLDER_SHA}")])

        result, derived, detector = _evaluate(_snapshot(), provider)

        assert result.decision is ActionDecision.EXECUTE
        assert derived.get(GATE_STATE_KEY) is EvidenceGateState.MISSING
        detector.assert_called_once()

    def test_copilot_evidence_author_counts_but_ccr_reviewer_does_not(self) -> None:
        accepted = _comment("Copilot", f"## Validation evidence\n{HEAD_SHA}")
        provider = _provider(comments=[accepted])
        result, derived, _ = _evaluate(_snapshot(), provider)
        assert derived.get(GATE_STATE_KEY) is EvidenceGateState.SATISFIED
        assert result.decision is ActionDecision.SKIP

        provider = _provider(comments=[_comment(COPILOT_REVIEWER_LOGIN, f"## Validation evidence\n{HEAD_SHA}")])
        result, derived, _ = _evaluate(_snapshot(), provider)
        assert derived.get(GATE_STATE_KEY) is EvidenceGateState.MISSING
        assert result.decision is ActionDecision.EXECUTE

    @pytest.mark.parametrize("active_session", [True, None])
    def test_active_or_unknown_writer_inventory_suppresses_followup(self, active_session: bool | None) -> None:
        provider = _provider()

        result, derived, detector = _evaluate(_snapshot(), provider, active_session=active_session)

        assert result.decision is ActionDecision.SKIP
        assert derived.get(GATE_STATE_KEY) is EvidenceGateState.MISSING
        detector.assert_called_once_with(
            "owner/repo",
            42,
            head_branch="feature/validation",
            pr_id=4200,
            head_sha=HEAD_SHA,
            provider=provider,
        )
        assert derived.get(FOLLOWUP_KEY) is None

    def test_first_missing_evidence_requests_one_recovery(self) -> None:
        result, derived, _ = _evaluate(_snapshot(), _provider())

        assert result.decision is ActionDecision.EXECUTE
        assert derived.get(GATE_STATE_KEY) is EvidenceGateState.MISSING
        assert derived.get(FOLLOWUP_KEY) == "recovery"

    def test_existing_blocker_prevents_any_later_followup(self) -> None:
        comments = [
            _comment("human", RECOVERY_MARKER, "2026-10-27T09:00:00Z"),
            _comment("human", BLOCKER_MARKER),
            _comment("Copilot", "I replied", "2026-10-27T11:00:00Z"),
        ]
        provider = _provider(comments=comments)

        result, derived, _ = _evaluate(_snapshot(), provider)

        assert result.decision is ActionDecision.SKIP
        assert derived.get(GATE_STATE_KEY) is EvidenceGateState.MISSING
        assert derived.get(FOLLOWUP_KEY) is None

    def test_waits_until_an_evidence_author_replies_after_recovery(self) -> None:
        recovery = _comment("human", RECOVERY_MARKER, "2026-10-27T09:00:00Z")
        comments = [recovery]
        provider = _provider(comments=comments)

        result, derived, _ = _evaluate(_snapshot(), provider)

        assert result.decision is ActionDecision.SKIP
        assert "awaiting" in result.details.casefold()
        assert derived.get(GATE_STATE_KEY) is EvidenceGateState.MISSING
        assert derived.get(FOLLOWUP_KEY) is None

    @pytest.mark.parametrize("reply_time", ["not-a-timestamp", "2026-10-27T11:00:00"])
    def test_malformed_or_offset_free_reply_does_not_unlock_blocker(self, reply_time: str) -> None:
        comments = [
            _comment("human", RECOVERY_MARKER, "2026-10-27T09:00:00Z"),
            _comment("Copilot", "I replied", reply_time),
        ]
        result, derived, _ = _evaluate(_snapshot(), _provider(comments=comments))

        assert result.decision is ActionDecision.SKIP
        assert "awaiting" in result.details.casefold()
        assert derived.get(FOLLOWUP_KEY) is None

    def test_evidence_author_reply_unlocks_one_blocker(self) -> None:
        comments = [
            _comment("human", RECOVERY_MARKER, "2026-10-27T09:00:00Z"),
            _comment("Copilot", "I replied without evidence", "2026-10-27T11:00:00+00:00"),
        ]

        result, derived, _ = _evaluate(_snapshot(), _provider(comments=comments))

        assert result.decision is ActionDecision.EXECUTE
        assert derived.get(FOLLOWUP_KEY) == "blocker"

    @pytest.mark.parametrize("is_rate_limit", [False, True])
    def test_provider_rate_limit_flag_controls_evaluate_reraise(self, is_rate_limit: bool) -> None:
        provider = _provider()
        provider.list_issue_comments.side_effect = ProviderRateLimitError(is_rate_limit=is_rate_limit)

        if is_rate_limit:
            with pytest.raises(ProviderRateLimitError):
                _evaluate(_snapshot(), provider)
        else:
            result, derived, _ = _evaluate(_snapshot(), provider)
            assert result.decision is ActionDecision.SKIP
            assert derived.get(GATE_STATE_KEY) is EvidenceGateState.UNKNOWN

    def test_non_rate_limit_provider_error_leaves_evaluate_unknown(self) -> None:
        provider = _provider()
        provider.list_linked_issue_labels.side_effect = RuntimeError("provider unavailable")

        result, derived, _ = _evaluate(_snapshot(labels=[]), provider)

        assert result.decision is ActionDecision.SKIP
        assert derived.get(GATE_STATE_KEY) is EvidenceGateState.UNKNOWN

    @pytest.mark.parametrize(
        ("followup", "expected_body"),
        [("recovery", build_recovery_request(HEAD_SHA)), ("blocker", build_blocker_comment(HEAD_SHA))],
    )
    def test_execute_posts_the_current_head_recovery_or_blocker(self, followup: str, expected_body: str) -> None:
        provider = _provider()
        snapshot = _snapshot()
        derived = DerivedState(snapshot)
        derived.set(GATE_STATE_KEY, EvidenceGateState.MISSING)
        derived.set(FOLLOWUP_KEY, followup)

        result = ValidationEvidenceGateAction().execute(provider, snapshot, derived)

        assert result.decision is ActionDecision.EXECUTE
        assert result.invalidates_snapshot is False
        assert derived.get(GATE_STATE_KEY) is EvidenceGateState.MISSING
        provider.post_comment.assert_called_once_with(42, expected_body)
        assert HEAD_SHA in provider.post_comment.call_args.args[1]
        if followup == "recovery":
            assert expected_body.startswith("@copilot")
            assert expected_body.rstrip().endswith(RECOVERY_MARKER)
        else:
            assert not expected_body.startswith("@copilot")
            assert expected_body.rstrip().endswith(BLOCKER_MARKER)

    def test_execute_fails_without_posting_for_unknown_followup(self) -> None:
        provider = _provider()
        snapshot = _snapshot()
        derived = DerivedState(snapshot)
        derived.set(FOLLOWUP_KEY, "unknown")

        result = ValidationEvidenceGateAction().execute(provider, snapshot, derived)

        assert result.decision is ActionDecision.FAILED
        provider.post_comment.assert_not_called()

    @pytest.mark.parametrize("is_rate_limit", [False, True])
    def test_execute_handles_posting_errors_by_rate_limit_status(self, is_rate_limit: bool) -> None:
        provider = _provider()
        provider.post_comment.side_effect = ProviderRateLimitError(is_rate_limit=is_rate_limit)
        snapshot = _snapshot()
        derived = DerivedState(snapshot)
        derived.set(FOLLOWUP_KEY, "recovery")

        if is_rate_limit:
            with pytest.raises(ProviderRateLimitError):
                ValidationEvidenceGateAction().execute(provider, snapshot, derived)
        else:
            result = ValidationEvidenceGateAction().execute(provider, snapshot, derived)
            assert result.decision is ActionDecision.FAILED

    def test_execute_fails_for_an_ordinary_posting_error(self) -> None:
        provider = _provider()
        provider.post_comment.side_effect = RuntimeError("posting unavailable")
        snapshot = _snapshot()
        derived = DerivedState(snapshot)
        derived.set(FOLLOWUP_KEY, "blocker")

        result = ValidationEvidenceGateAction().execute(provider, snapshot, derived)

        assert result.decision is ActionDecision.FAILED

    def test_recovery_budget_and_blocker_marker_are_bounded(self) -> None:
        provider = _provider()
        snapshot = _snapshot()
        action = ValidationEvidenceGateAction()
        derived = DerivedState(snapshot)
        derived.set("provider", provider)

        with patch(f"{ACTION_MODULE}.is_copilot_session_active_via_agent_task", return_value=False):
            first = action.evaluate(snapshot, derived)
            action.execute(provider, snapshot, derived)
            provider.list_issue_comments.return_value = [_comment("human", RECOVERY_MARKER, "2026-10-27T09:00:00Z")]
            waiting = action.evaluate(snapshot, derived)
            provider.list_issue_comments.return_value.append(
                _comment("Copilot", "No evidence was supplied", "2026-10-27T11:00:00Z")
            )
            blocker = action.evaluate(snapshot, derived)
            action.execute(provider, snapshot, derived)
            provider.list_issue_comments.return_value.append(_comment("human", BLOCKER_MARKER))
            provider.list_issue_comments.return_value.append(
                _comment("Copilot", "Another reply", "2026-10-27T12:00:00Z")
            )
            blocked = action.evaluate(snapshot, derived)

        assert first.decision is ActionDecision.EXECUTE
        assert waiting.decision is ActionDecision.SKIP
        assert blocker.decision is ActionDecision.EXECUTE
        assert blocked.decision is ActionDecision.SKIP
        assert derived.get(FOLLOWUP_KEY) == "blocker"
        assert provider.post_comment.call_count == 2
