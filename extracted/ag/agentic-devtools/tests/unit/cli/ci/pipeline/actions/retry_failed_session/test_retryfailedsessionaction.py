"""Tests for bounded failed-session retry and escalation."""

from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from agentic_devtools.cli.ci.guards import AGENT_FAILED_LABEL
from agentic_devtools.cli.ci.models import ClosingIssue, IssueCommentInfo
from agentic_devtools.cli.ci.pipeline.actions.retry_failed_session import RetryFailedSessionAction
from agentic_devtools.cli.ci.pipeline.models import ActionDecision
from agentic_devtools.cli.ci.pipeline.session_detector import SessionOutcome, SessionState
from agentic_devtools.cli.ci.pipeline.snapshot_models import DerivedState
from agentic_devtools.cli.shared.retry import ProviderRateLimitError
from tests.unit.cli.ci.pipeline.actions.retry_failed_session._retry_fixtures import _provider, _snapshot

MODULE = "agentic_devtools.cli.ci.pipeline.actions.retry_failed_session"


@pytest.mark.parametrize("retry_limit", [True, -1, 6, "2"])
def test_rejects_invalid_retry_limit(retry_limit: Any) -> None:
    with pytest.raises(ValueError, match="between 0 and 5"):
        RetryFailedSessionAction(_provider(), retry_limit=retry_limit)


def test_skips_when_latest_session_is_not_failed() -> None:
    provider = _provider()
    action = RetryFailedSessionAction(provider)
    snapshot = _snapshot()
    derived = DerivedState(snapshot)
    with patch(f"{MODULE}.get_latest_session_state", return_value=SessionState(SessionOutcome.FINISHED)):
        result = action.evaluate(snapshot, derived)
    assert result.decision is ActionDecision.SKIP
    assert derived.get("latest_session_state").outcome is SessionOutcome.FINISHED


def test_blocks_pipeline_when_session_is_active_on_non_wip_draft() -> None:
    class ProviderWithActiveTask(MagicMock):
        def list_agent_tasks(self, repo: str) -> list[object]:
            assert repo == "org/repo"
            return [{"id": "task-running", "state": "in_progress", "pullRequestNumber": 12}]

    provider = ProviderWithActiveTask()
    provider.get_dispatch_login.return_value = "workflow-bot"
    action = RetryFailedSessionAction(provider)
    snapshot = _snapshot(is_draft=True, title="Resume work")
    derived = DerivedState(snapshot)
    result = action.evaluate(snapshot, derived)

    assert result.decision is ActionDecision.BLOCKED
    assert "active" in result.details.lower()
    assert derived.get("latest_session_state") == SessionState(SessionOutcome.ACTIVE, task_id="task-running")
    assert action.terminates_run is True


@pytest.mark.parametrize("outcome", [SessionOutcome.NONE, SessionOutcome.UNKNOWN])
def test_handles_no_session_and_unknown_outcomes_safely(outcome: SessionOutcome) -> None:
    provider = _provider()
    action = RetryFailedSessionAction(provider)
    snapshot = _snapshot()
    derived = DerivedState(snapshot)
    with patch(f"{MODULE}.get_latest_session_state", return_value=SessionState(outcome)):
        result = action.evaluate(snapshot, derived)
    assert result.decision is (ActionDecision.BLOCKED if outcome is SessionOutcome.UNKNOWN else ActionDecision.SKIP)
    assert derived.get("latest_session_state").outcome is outcome
    assert "active" not in result.details.lower() and result.preconditions.get("session_active") is not True


@pytest.mark.parametrize(
    ("lifecycle_active", "expected_outcome", "expected_preconditions"),
    [
        (True, SessionOutcome.ACTIVE, {"session_active": True}),
        (None, SessionOutcome.UNKNOWN, {"session_outcome_known": False}),
    ],
)
def test_preserves_timeline_failure_identity_when_aggregate_lifecycle_blocks(
    lifecycle_active: bool | None,
    expected_outcome: SessionOutcome,
    expected_preconditions: dict[str, bool],
) -> None:
    provider = _provider()
    action = RetryFailedSessionAction(provider)
    snapshot = _snapshot()
    derived = DerivedState(snapshot)
    failed_state = SessionState(
        SessionOutcome.FAILED,
        failure_event_id=42,
        failure_created_at="2026-10-16T00:01:00Z",
    )

    with (
        patch(f"{MODULE}.get_latest_session_state", return_value=failed_state),
        patch(f"{MODULE}.is_copilot_session_active_via_agent_task", return_value=lifecycle_active),
    ):
        result = action.evaluate(snapshot, derived)

    assert result.decision is ActionDecision.BLOCKED
    assert result.preconditions == expected_preconditions
    assert derived.get("latest_session_state") == SessionState(
        expected_outcome,
        failure_event_id=42,
        failure_created_at="2026-10-16T00:01:00Z",
    )


def test_blocks_failed_retry_for_unsafe_fork() -> None:
    provider = _provider()
    action = RetryFailedSessionAction(provider)
    snapshot = _snapshot(head_repo_full_name="external/repo")
    result = action.evaluate(snapshot, DerivedState(snapshot))
    assert result.decision is ActionDecision.BLOCKED
    assert "fork" in result.details.lower()


@pytest.mark.parametrize(
    ("overrides", "expected"),
    [
        ({"labels": ["ai-pr-loop-ignore"]}, "exclusion"),
        ({"files": [".github/workflows/ai-pr-loop.yml"]}, "privileged"),
        ({"files": ["Dockerfile"]}, "docker"),
    ],
)
@pytest.mark.parametrize("initial_env", [None, "1"])
def test_blocks_failed_retry_for_other_unsafe_prs(
    overrides: dict[str, Any], expected: str, monkeypatch: pytest.MonkeyPatch, initial_env: str | None
) -> None:
    if initial_env is None:
        monkeypatch.delenv("AGDT_ALLOW_PRIVILEGED_PATHS", raising=False)
    else:
        monkeypatch.setenv("AGDT_ALLOW_PRIVILEGED_PATHS", initial_env)
    monkeypatch.delenv("AGDT_ALLOW_PRIVILEGED_PATHS", raising=False)
    snapshot = _snapshot(**overrides)
    result = RetryFailedSessionAction(_provider()).evaluate(snapshot, DerivedState(snapshot))
    assert result.decision is ActionDecision.BLOCKED
    assert expected in result.details.lower()


def test_blocks_failed_session_without_stable_identity() -> None:
    provider = _provider()
    snapshot = _snapshot()
    with patch(f"{MODULE}.get_latest_session_state", return_value=SessionState(SessionOutcome.FAILED)):
        result = RetryFailedSessionAction(provider).evaluate(snapshot, DerivedState(snapshot))
    assert result.decision is ActionDecision.BLOCKED
    assert "identity" in result.details


def test_blocks_failed_session_without_dispatch_identity() -> None:
    provider = _provider()
    provider.get_dispatch_login.return_value = ""
    snapshot = _snapshot()
    with patch(
        f"{MODULE}.get_latest_session_state",
        return_value=SessionState(SessionOutcome.FAILED, failure_event_id=1),
    ):
        result = RetryFailedSessionAction(provider).evaluate(snapshot, DerivedState(snapshot))
    assert result.decision is ActionDecision.BLOCKED
    assert "trusted" in result.details


def test_blocks_when_retry_marker_inventory_fails() -> None:
    provider = _provider()
    provider.list_issue_comments.side_effect = RuntimeError("comments unavailable")
    snapshot = _snapshot()
    with patch(
        f"{MODULE}.get_latest_session_state",
        return_value=SessionState(SessionOutcome.FAILED, failure_event_id=1),
    ):
        result = RetryFailedSessionAction(provider).evaluate(snapshot, DerivedState(snapshot))
    assert result.decision is ActionDecision.BLOCKED
    assert "marker" in result.details


def test_reraises_rate_limit_when_retry_marker_inventory_fails() -> None:
    provider = _provider()
    provider.list_issue_comments.side_effect = ProviderRateLimitError(provider="github", is_rate_limit=True)
    snapshot = _snapshot()
    with patch(
        f"{MODULE}.get_latest_session_state",
        return_value=SessionState(SessionOutcome.FAILED, failure_event_id=1),
    ):
        with pytest.raises(ProviderRateLimitError):
            RetryFailedSessionAction(provider).evaluate(snapshot, DerivedState(snapshot))


def test_blocks_when_failure_already_has_retry_marker() -> None:
    provider = _provider()
    provider.list_issue_comments.return_value = [
        IssueCommentInfo(
            1,
            "workflow-bot",
            "<!-- agdt:agent-retry:41:1 -->",
            created_at="2026-01-01T00:02:00Z",
        )
    ]
    action = RetryFailedSessionAction(provider)
    snapshot = _snapshot()
    with (
        patch(f"{MODULE}.is_agent_retry_confirmation_expired", return_value=False),
        patch(
            f"{MODULE}.get_latest_session_state",
            return_value=SessionState(
                SessionOutcome.FAILED,
                failure_event_id=41,
                failure_created_at="2026-01-01T00:01:00Z",
            ),
        ),
    ):
        result = action.evaluate(snapshot, DerivedState(snapshot))
    assert result.decision is ActionDecision.BLOCKED
    assert "already has" in result.details


def test_escalates_instead_of_retrying_when_retry_confirmation_expires() -> None:
    provider = _provider()
    provider.list_issue_comments.return_value = [
        IssueCommentInfo(
            1,
            "workflow-bot",
            "<!-- agdt:agent-retry:41:1 -->",
            created_at="2026-01-01T00:02:00Z",
        )
    ]
    action = RetryFailedSessionAction(provider)
    snapshot = _snapshot()
    derived = DerivedState(snapshot)
    with (
        patch(f"{MODULE}.is_agent_retry_confirmation_expired", return_value=True),
        patch(
            f"{MODULE}.get_latest_session_state",
            return_value=SessionState(
                SessionOutcome.FAILED,
                failure_event_id=41,
                failure_created_at="2026-01-01T00:01:00Z",
            ),
        ),
    ):
        result = action.evaluate(snapshot, derived)

    assert result.decision is ActionDecision.EXECUTE
    assert "confirmation window expired" in result.details.lower()
    assert derived.get("agent_retry_mode") == "escalate"
    execution = action.execute(provider, snapshot, derived)
    body = provider.post_comment_as_pr_token.call_args.args[1]
    assert execution.decision is ActionDecision.EXECUTE
    assert execution.preconditions["retry_dispatched"] is False
    assert "not confirmed by a new Copilot session" in body
    assert "confirmation window" in body
    provider.dispatch_agent_retry.assert_not_called()
    provider.add_label.assert_called_once_with(12, AGENT_FAILED_LABEL)


def test_dispatches_marker_first_retry_with_linked_issue_context() -> None:
    provider = _provider()
    provider.list_closing_issues.return_value = [
        ClosingIssue(4257, "Retry agent", "## Refined Specification\n\nImplement recovery.")
    ]
    provider.list_issue_comments.return_value = [
        IssueCommentInfo(2, "workflow-bot", "@copilot Please fix the failing checks.\n\nOriginal findings")
    ]
    action = RetryFailedSessionAction(provider, retry_limit=2)
    snapshot = _snapshot()
    derived = DerivedState(snapshot)
    with patch(
        f"{MODULE}.get_latest_session_state",
        return_value=SessionState(SessionOutcome.FAILED, task_id="task-abc", failure_event_id=42),
    ):
        evaluated = action.evaluate(snapshot, derived)
    assert evaluated.decision is ActionDecision.EXECUTE
    result = action.execute(provider, snapshot, derived)
    prompt = provider.dispatch_agent_retry.call_args.args[1]
    assert result.decision is ActionDecision.EXECUTE
    assert prompt.startswith(
        "<!-- agdt:agent-retry:task-abc:1 -->\n"
        "<!-- agdt:agent-retry-alias:42 -->\n"
        "<!-- agdt:agent-retry-identity:task:task-abc -->\n"
        "<!-- agdt:agent-retry-identity:event:42 -->"
    )
    assert "Implement recovery." in prompt
    assert "Original findings" in prompt
    assert "Pull request title" in prompt


def test_retry_prompt_prioritizes_previous_repair_context_over_linked_issue_body() -> None:
    provider = _provider()
    provider.list_closing_issues.return_value = [ClosingIssue(4257, "Retry agent", "Refined issue specification")]
    snapshot = _snapshot()
    derived = DerivedState(snapshot)
    derived.set("agent_retry_dispatch_login", "workflow-bot")
    derived.set(
        "agent_retry_comments",
        [IssueCommentInfo(2, "workflow-bot", "@copilot Please fix this exact finding.")],
    )

    prompt = RetryFailedSessionAction(provider)._build_retry_prompt(snapshot, derived, "42", 1, 2)

    assert prompt.index("## Previous repair task context") < prompt.index("## Linked issue #4257")


def test_task_id_is_used_when_timeline_failure_id_is_missing() -> None:
    provider = _provider()
    action = RetryFailedSessionAction(provider, retry_limit=1)
    snapshot = _snapshot()
    derived = DerivedState(snapshot)
    with patch(
        f"{MODULE}.get_latest_session_state",
        return_value=SessionState(SessionOutcome.FAILED, task_id="task-abc"),
    ):
        assert action.evaluate(snapshot, derived).decision is ActionDecision.EXECUTE
    action.execute(provider, snapshot, derived)
    prompt = provider.dispatch_agent_retry.call_args.args[1]
    assert prompt.startswith("<!-- agdt:agent-retry:task-abc:1 -->")


def test_retry_prompt_recovers_original_agent_task_prompt_before_fallback_context() -> None:
    provider = _provider()
    provider.get_agent_task_prompt.return_value = "@copilot Fix the exact failing test."
    provider.list_closing_issues.return_value = [ClosingIssue(4257, "Retry agent", "Older issue context")]
    provider.list_issue_comments.return_value = [IssueCommentInfo(2, "workflow-bot", "@copilot Older repair findings")]
    action = RetryFailedSessionAction(provider, retry_limit=2)
    snapshot = _snapshot()
    derived = DerivedState(snapshot)
    with patch(
        f"{MODULE}.get_latest_session_state",
        return_value=SessionState(SessionOutcome.FAILED, task_id="task-abc"),
    ):
        action.evaluate(snapshot, derived)

    action.execute(provider, snapshot, derived)
    prompt = provider.dispatch_agent_retry.call_args.args[1]

    provider.get_agent_task_prompt.assert_called_once_with("task-abc")
    assert "Fix the exact failing test." in prompt
    assert "Older repair findings" not in prompt
    assert "Older issue context" not in prompt


def test_retry_prompt_falls_back_when_agent_task_prompt_is_unavailable() -> None:
    provider = _provider()
    provider.get_agent_task_prompt.side_effect = RuntimeError("task details unavailable")
    action = RetryFailedSessionAction(provider, retry_limit=2)
    snapshot = _snapshot()
    derived = DerivedState(snapshot)
    with patch(
        f"{MODULE}.get_latest_session_state",
        return_value=SessionState(SessionOutcome.FAILED, task_id="task-abc"),
    ):
        action.evaluate(snapshot, derived)

    action.execute(provider, snapshot, derived)
    prompt = provider.dispatch_agent_retry.call_args.args[1]

    assert "Original task description" in prompt


def test_retry_prompt_reraises_agent_task_prompt_rate_limit() -> None:
    provider = _provider()
    provider.get_agent_task_prompt.side_effect = ProviderRateLimitError(provider="github", is_rate_limit=True)
    action = RetryFailedSessionAction(provider, retry_limit=2)
    snapshot = _snapshot()
    derived = DerivedState(snapshot)
    with patch(
        f"{MODULE}.get_latest_session_state",
        return_value=SessionState(SessionOutcome.FAILED, task_id="task-abc"),
    ):
        action.evaluate(snapshot, derived)

    with pytest.raises(ProviderRateLimitError):
        action.execute(provider, snapshot, derived)


def test_retry_comment_persists_timeline_failure_alias_for_task_identity() -> None:
    provider = _provider()
    action = RetryFailedSessionAction(provider)
    snapshot = _snapshot()
    derived = DerivedState(snapshot)
    with patch(
        f"{MODULE}.get_latest_session_state",
        return_value=SessionState(SessionOutcome.FAILED, failure_event_id=42, task_id="task-abc"),
    ):
        assert action.evaluate(snapshot, derived).decision is ActionDecision.EXECUTE
    action.execute(provider, snapshot, derived)

    prompt = provider.dispatch_agent_retry.call_args.args[1]
    assert prompt.startswith("<!-- agdt:agent-retry:task-abc:1 -->")
    assert "<!-- agdt:agent-retry-alias:42 -->" in prompt


def test_retry_marker_alias_blocks_when_session_lookup_falls_back_to_timeline() -> None:
    provider = _provider()
    provider.list_issue_comments.return_value = [
        IssueCommentInfo(
            1,
            "workflow-bot",
            "<!-- agdt:agent-retry:task-abc:1 -->\n<!-- agdt:agent-retry-alias:42 -->",
        )
    ]
    action = RetryFailedSessionAction(provider)
    snapshot = _snapshot()
    with patch(
        f"{MODULE}.get_latest_session_state",
        return_value=SessionState(SessionOutcome.FAILED, failure_event_id=42),
    ):
        result = action.evaluate(snapshot, DerivedState(snapshot))
    assert result.decision is ActionDecision.BLOCKED
    assert "already has" in result.details


def test_blocks_task_retry_when_only_an_unrelated_timeline_marker_exists() -> None:
    provider = _provider()
    provider.list_issue_comments.return_value = [IssueCommentInfo(1, "workflow-bot", "<!-- agdt:agent-retry:42:1 -->")]
    action = RetryFailedSessionAction(provider)
    snapshot = _snapshot()
    with patch(
        f"{MODULE}.get_latest_session_state",
        return_value=SessionState(SessionOutcome.FAILED, task_id="task-abc"),
    ):
        result = action.evaluate(snapshot, DerivedState(snapshot))

    assert result.decision is ActionDecision.BLOCKED
    assert "cannot correlate" in result.details.lower()
    provider.dispatch_agent_retry.assert_not_called()


def test_blocks_unmatched_task_retry_when_session_lookup_falls_back_to_timeline() -> None:
    provider = _provider()
    provider.list_issue_comments.return_value = [
        IssueCommentInfo(1, "workflow-bot", "<!-- agdt:agent-retry:task-a:1 -->")
    ]
    action = RetryFailedSessionAction(provider)
    snapshot = _snapshot()
    with patch(
        f"{MODULE}.get_latest_session_state",
        return_value=SessionState(SessionOutcome.FAILED, failure_event_id=42),
    ):
        result = action.evaluate(snapshot, DerivedState(snapshot))

    assert result.decision is ActionDecision.BLOCKED
    assert "cannot correlate" in result.details.lower()
    provider.dispatch_agent_retry.assert_not_called()


@pytest.mark.parametrize(
    ("retry_limit", "expected_mode", "marker", "state"),
    [
        (
            2,
            "retry",
            IssueCommentInfo(
                1,
                "workflow-bot",
                "<!-- agdt:agent-retry:task-old:1 -->",
                created_at="2026-01-01T00:02:00Z",
            ),
            SessionState(
                SessionOutcome.FAILED,
                failure_event_id=42,
                failure_created_at="2026-01-01T00:03:00Z",
            ),
        ),
        (
            1,
            "escalate",
            IssueCommentInfo(
                1,
                "workflow-bot",
                "<!-- agdt:agent-retry:task-old:1 -->",
                created_at="2026-01-01T00:02:00Z",
            ),
            SessionState(
                SessionOutcome.FAILED,
                failure_event_id=42,
                failure_created_at="2026-01-01T00:03:00Z",
            ),
        ),
        (
            2,
            "retry",
            IssueCommentInfo(
                1,
                "workflow-bot",
                "<!-- agdt:agent-retry:42:1 -->",
                created_at="2026-01-01T00:02:00Z",
            ),
            SessionState(
                SessionOutcome.FAILED,
                failure_event_id=43,
                task_id="task-new",
                failure_created_at="2026-01-01T00:03:00Z",
            ),
        ),
        (
            1,
            "escalate",
            IssueCommentInfo(
                1,
                "workflow-bot",
                "<!-- agdt:agent-retry:42:1 -->",
                created_at="2026-01-01T00:02:00Z",
            ),
            SessionState(
                SessionOutcome.FAILED,
                failure_event_id=43,
                task_id="task-new",
                failure_created_at="2026-01-01T00:03:00Z",
            ),
        ),
    ],
)
def test_retries_or_escalates_a_newer_failure_after_source_switch(
    retry_limit: int,
    expected_mode: str,
    marker: IssueCommentInfo,
    state: SessionState,
) -> None:
    provider = _provider()
    provider.list_issue_comments.return_value = [marker]
    action = RetryFailedSessionAction(provider, retry_limit=retry_limit)
    snapshot = _snapshot()
    derived = DerivedState(snapshot)
    with patch(
        f"{MODULE}.get_latest_session_state",
        return_value=state,
    ):
        result = action.evaluate(snapshot, derived)

    assert result.decision is ActionDecision.EXECUTE
    assert derived.get("agent_retry_mode") == expected_mode


def test_existing_timeline_marker_blocks_retry_when_both_failure_ids_are_known() -> None:
    provider = _provider()
    provider.list_issue_comments.return_value = [IssueCommentInfo(1, "workflow-bot", "<!-- agdt:agent-retry:42:1 -->")]
    action = RetryFailedSessionAction(provider)
    snapshot = _snapshot()
    with patch(
        f"{MODULE}.get_latest_session_state",
        return_value=SessionState(SessionOutcome.FAILED, failure_event_id=42, task_id="task-abc"),
    ):
        derived = DerivedState(snapshot)
        result = action.evaluate(snapshot, derived)

    assert result.decision is ActionDecision.BLOCKED
    assert derived.get("agent_retry_failure_aliases") is None


def test_execute_fails_when_evaluation_state_is_missing() -> None:
    snapshot = _snapshot()
    result = RetryFailedSessionAction(_provider()).execute(_provider(), snapshot, DerivedState(snapshot))
    assert result.decision is ActionDecision.FAILED
    assert "evaluation state" in result.error


def test_execute_delegates_admitted_initial_delivery_without_generic_failed_retry() -> None:
    provider = _provider()
    snapshot = _snapshot()
    derived = DerivedState(snapshot)
    derived.set("initial_delivery_mode", "retry")
    with patch(f"{MODULE}.InitialDeliveryRecovery") as recovery:
        result = RetryFailedSessionAction(provider).execute(provider, snapshot, derived)
    assert result is recovery.return_value.execute.return_value
    recovery.return_value.execute.assert_called_once_with(provider, snapshot, derived)
    provider.dispatch_agent_retry.assert_not_called()


def test_retry_dispatch_failure_is_reported() -> None:
    provider = _provider()
    provider.dispatch_agent_retry.side_effect = RuntimeError("dispatch unavailable")
    action = RetryFailedSessionAction(provider, retry_limit=1)
    snapshot = _snapshot()
    derived = DerivedState(snapshot)
    with patch(
        f"{MODULE}.get_latest_session_state",
        return_value=SessionState(SessionOutcome.FAILED, failure_event_id=10),
    ):
        action.evaluate(snapshot, derived)
    result = action.execute(provider, snapshot, derived)
    assert result.decision is ActionDecision.FAILED
    assert result.error == "dispatch unavailable"


def test_retry_dispatch_reraises_rate_limit() -> None:
    provider = _provider()
    provider.dispatch_agent_retry.side_effect = ProviderRateLimitError(provider="github", is_rate_limit=True)
    action = RetryFailedSessionAction(provider, retry_limit=1)
    snapshot = _snapshot()
    derived = DerivedState(snapshot)
    with patch(
        f"{MODULE}.get_latest_session_state",
        return_value=SessionState(SessionOutcome.FAILED, failure_event_id=10),
    ):
        action.evaluate(snapshot, derived)
    with pytest.raises(ProviderRateLimitError):
        action.execute(provider, snapshot, derived)


def test_escalates_after_retry_budget_and_posts_human_readable_comment() -> None:
    provider = _provider()
    provider.list_issue_comments.return_value = [
        IssueCommentInfo(1, "workflow-bot", "<!-- agdt:agent-retry:10:1 -->"),
        IssueCommentInfo(2, "workflow-bot", "<!-- agdt:agent-retry:11:2 -->"),
    ]
    action = RetryFailedSessionAction(provider, retry_limit=2)
    snapshot = _snapshot()
    derived = DerivedState(snapshot)
    with patch(
        f"{MODULE}.get_latest_session_state",
        return_value=SessionState(SessionOutcome.FAILED, failure_event_id=12),
    ):
        evaluated = action.evaluate(snapshot, derived)
    assert evaluated.decision is ActionDecision.EXECUTE
    assert "exhausted" in evaluated.details
    result = action.execute(provider, snapshot, derived)
    body = provider.post_comment_as_pr_token.call_args.args[1]
    assert result.decision is ActionDecision.EXECUTE
    assert result.preconditions["retry_dispatched"] is False
    assert body.startswith("<!-- agdt:agent-retry-escalation:12 -->")
    assert "3 Copilot coding-agent session(s) failed" in body
    assert "Failure identities: 10, 11, 12" in body
    assert "retry budget" in body
    provider.add_label.assert_called_once_with(12, AGENT_FAILED_LABEL)


def test_completes_escalation_when_label_exists_but_comment_is_missing() -> None:
    provider = _provider()
    action = RetryFailedSessionAction(provider, retry_limit=2)
    snapshot = _snapshot(labels=[AGENT_FAILED_LABEL])
    derived = DerivedState(snapshot)
    with patch(
        f"{MODULE}.get_latest_session_state",
        return_value=SessionState(SessionOutcome.FAILED, failure_event_id=12),
    ):
        evaluated = action.evaluate(snapshot, derived)
    assert evaluated.decision is ActionDecision.EXECUTE
    assert "Complete" in evaluated.details
    result = action.execute(provider, snapshot, derived)
    assert result.decision is ActionDecision.EXECUTE
    assert result.preconditions["retry_dispatched"] is False
    assert provider.post_comment_as_pr_token.call_args.args[1].startswith("<!-- agdt:agent-retry-escalation:12 -->")


def test_blocks_when_label_and_escalation_marker_are_already_present() -> None:
    provider = _provider()
    provider.list_issue_comments.return_value = [
        IssueCommentInfo(1, "workflow-bot", "<!-- agdt:agent-retry-escalation:12 -->\nEscalated")
    ]
    action = RetryFailedSessionAction(provider)
    snapshot = _snapshot(labels=[AGENT_FAILED_LABEL])
    with patch(
        f"{MODULE}.get_latest_session_state",
        return_value=SessionState(SessionOutcome.FAILED, failure_event_id=12),
    ):
        result = action.evaluate(snapshot, DerivedState(snapshot))
    assert result.decision is ActionDecision.BLOCKED
    assert "already complete" in result.details


def test_escalation_identity_reader_ignores_untrusted_and_malformed_comments() -> None:
    comments = [
        object(),
        IssueCommentInfo(1, "other-user", "<!-- agdt:agent-retry-escalation:foreign-id -->"),
        IssueCommentInfo(2, "workflow-bot", ""),
        IssueCommentInfo(3, "workflow-bot", "@copilot Please fix this issue."),
        IssueCommentInfo(
            4,
            "workflow-bot",
            "<!-- agdt:agent-retry-escalation:task-abc -->\n"
            "<!-- agdt:agent-retry-escalation-pr:12 -->\n"
            "Human text\n<!-- agdt:agent-retry-escalation-alias:42 -->",
        ),
        IssueCommentInfo(5, "workflow-bot", "<!-- agdt:agent-retry-escalation:task-only -->"),
    ]

    assert RetryFailedSessionAction._escalation_identities(comments, "workflow-bot") == {
        "task-abc",
        "pr:12",
        "task-only",
    }
    assert RetryFailedSessionAction._escalation_identities(comments, "") == set()
    assert RetryFailedSessionAction._escalation_identities(None, "workflow-bot") == set()


@pytest.mark.parametrize(
    "aliases",
    ["malformed", ["task-abc", "", None, 42]],
    ids=["non-list", "invalid-alias-values"],
)
def test_escalation_skips_malformed_or_duplicate_aliases(aliases: object) -> None:
    provider = _provider()
    action = RetryFailedSessionAction(provider, retry_limit=0)
    snapshot = _snapshot()
    derived = DerivedState(snapshot)
    derived.set("agent_retry_mode", "escalate")
    derived.set("agent_retry_failure_id", "task-abc")
    derived.set("agent_retry_failure_aliases", aliases)
    derived.set("agent_retry_comments", [])
    derived.set("agent_retry_dispatch_login", "workflow-bot")

    result = action.execute(provider, snapshot, derived)

    assert result.decision is ActionDecision.EXECUTE
    body = provider.post_comment_as_pr_token.call_args.args[1]
    assert body.startswith(
        "<!-- agdt:agent-retry-escalation:task-abc -->\n<!-- agdt:agent-retry-escalation-pr:12 -->\n\n"
    )
    assert "agdt:agent-retry-escalation-alias:" not in body


def test_quoted_escalation_marker_does_not_force_escalation_during_evaluation() -> None:
    provider = _provider()
    provider.list_issue_comments.return_value = [
        IssueCommentInfo(
            1,
            "workflow-bot",
            "@copilot Please address this finding.\n\nQuoted repair context:\n<!-- agdt:agent-retry-escalation:12 -->",
        )
    ]
    action = RetryFailedSessionAction(provider, retry_limit=2)
    snapshot = _snapshot()
    derived = DerivedState(snapshot)
    with patch(
        f"{MODULE}.get_latest_session_state",
        return_value=SessionState(SessionOutcome.FAILED, failure_event_id=12),
    ):
        result = action.evaluate(snapshot, derived)

    assert result.decision is ActionDecision.EXECUTE
    assert derived.get("agent_retry_mode") == "retry"


def test_quoted_escalation_marker_does_not_suppress_escalation_comment() -> None:
    provider = _provider()
    provider.list_issue_comments.return_value = [
        IssueCommentInfo(1, "workflow-bot", "<!-- agdt:agent-retry:10:1 -->"),
        IssueCommentInfo(2, "workflow-bot", "<!-- agdt:agent-retry:11:1 -->"),
        IssueCommentInfo(
            3,
            "workflow-bot",
            "@copilot Please fix this finding.\n\nQuoted repair context:\n<!-- agdt:agent-retry-escalation:12 -->",
        ),
    ]
    action = RetryFailedSessionAction(provider, retry_limit=2)
    snapshot = _snapshot()
    derived = DerivedState(snapshot)
    with patch(
        f"{MODULE}.get_latest_session_state",
        return_value=SessionState(SessionOutcome.FAILED, failure_event_id=12),
    ):
        action.evaluate(snapshot, derived)

    result = action.execute(provider, snapshot, derived)

    assert result.decision is ActionDecision.EXECUTE
    assert provider.post_comment_as_pr_token.call_count == 1
    assert provider.post_comment_as_pr_token.call_args.args[1].startswith("<!-- agdt:agent-retry-escalation:12 -->")


@pytest.mark.parametrize("body", ["", "A normal comment\n\nwith multiple lines"])
def test_non_dispatch_comments_are_not_repair_context(body: str) -> None:
    assert RetryFailedSessionAction._is_dispatched_repair_comment(body) is False


def test_retries_failed_label_write_without_duplicating_existing_escalation() -> None:
    provider = _provider()
    provider.add_label.side_effect = RuntimeError("label unavailable")
    provider.list_issue_comments.return_value = [
        IssueCommentInfo(
            1,
            "workflow-bot",
            "<!-- agdt:agent-retry-escalation:12 -->\nHuman-readable escalation",
        )
    ]
    action = RetryFailedSessionAction(provider, retry_limit=0)
    snapshot = _snapshot()
    derived = DerivedState(snapshot)
    with patch(
        f"{MODULE}.get_latest_session_state",
        return_value=SessionState(SessionOutcome.FAILED, failure_event_id=12),
    ):
        action.evaluate(snapshot, derived)
    result = action.execute(provider, snapshot, derived)
    assert result.decision is ActionDecision.FAILED
    provider.post_comment_as_pr_token.assert_not_called()
    provider.add_label.assert_called_once()


@pytest.mark.parametrize("first_failure_event_id", [42, None], ids=["correlated", "task-only"])
def test_source_switch_after_partial_escalation_retries_label_without_duplicate_comment(
    first_failure_event_id: int | None,
) -> None:
    provider = _provider()
    provider.add_label.side_effect = [RuntimeError("label unavailable"), None]
    action = RetryFailedSessionAction(provider, retry_limit=0)
    snapshot = _snapshot()
    first_derived = DerivedState(snapshot)
    second_derived = DerivedState(snapshot)
    states = [
        SessionState(
            SessionOutcome.FAILED,
            failure_event_id=first_failure_event_id,
            task_id="task-abc",
            failure_created_at="2026-01-01T00:03:00Z",
        ),
        SessionState(
            SessionOutcome.FAILED,
            failure_event_id=42,
            failure_created_at="2026-01-01T00:03:00Z",
        ),
    ]
    with patch(f"{MODULE}.get_latest_session_state", side_effect=states):
        assert action.evaluate(snapshot, first_derived).decision is ActionDecision.EXECUTE
        assert action.execute(provider, snapshot, first_derived).decision is ActionDecision.FAILED
        escalation_body = provider.post_comment_as_pr_token.call_args.args[1]
        provider.list_issue_comments.return_value = [IssueCommentInfo(9, "workflow-bot", escalation_body)]

        assert action.evaluate(snapshot, second_derived).decision is ActionDecision.EXECUTE
        result = action.execute(provider, snapshot, second_derived)

    assert result.decision is ActionDecision.EXECUTE
    assert escalation_body.startswith("<!-- agdt:agent-retry-escalation:task-abc -->\n")
    assert "<!-- agdt:agent-retry-escalation-pr:12 -->" in escalation_body
    if first_failure_event_id is not None:
        assert "<!-- agdt:agent-retry-escalation-alias:42 -->" in escalation_body
    else:
        assert "agdt:agent-retry-escalation-alias:" not in escalation_body
    provider.post_comment_as_pr_token.assert_called_once()
    assert provider.add_label.call_count == 2


def test_escalation_comment_failure_is_reported() -> None:
    provider = _provider()
    provider.post_comment_as_pr_token.side_effect = RuntimeError("comment unavailable")
    action = RetryFailedSessionAction(provider, retry_limit=0)
    snapshot = _snapshot()
    derived = DerivedState(snapshot)
    with patch(
        f"{MODULE}.get_latest_session_state",
        return_value=SessionState(SessionOutcome.FAILED, failure_event_id=12),
    ):
        action.evaluate(snapshot, derived)
    result = action.execute(provider, snapshot, derived)
    assert result.decision is ActionDecision.FAILED
    assert "failed to post escalation" in result.error
    provider.add_label.assert_not_called()


def test_escalation_label_rate_limit_is_reraised() -> None:
    provider = _provider()
    provider.add_label.side_effect = ProviderRateLimitError(provider="github", is_rate_limit=True)
    action = RetryFailedSessionAction(provider, retry_limit=0)
    snapshot = _snapshot()
    derived = DerivedState(snapshot)
    with patch(
        f"{MODULE}.get_latest_session_state",
        return_value=SessionState(SessionOutcome.FAILED, failure_event_id=12),
    ):
        action.evaluate(snapshot, derived)
    with pytest.raises(ProviderRateLimitError):
        action.execute(provider, snapshot, derived)


def test_escalation_comment_rate_limit_is_reraised() -> None:
    provider = _provider()
    provider.post_comment_as_pr_token.side_effect = ProviderRateLimitError(
        provider="github",
        is_rate_limit=True,
    )
    action = RetryFailedSessionAction(provider, retry_limit=0)
    snapshot = _snapshot()
    derived = DerivedState(snapshot)
    with patch(
        f"{MODULE}.get_latest_session_state",
        return_value=SessionState(SessionOutcome.FAILED, failure_event_id=12),
    ):
        action.evaluate(snapshot, derived)
    with pytest.raises(ProviderRateLimitError):
        action.execute(provider, snapshot, derived)


def test_retry_without_recoverable_context_includes_title_and_explanation() -> None:
    provider = _provider()
    provider.get_pr_body.return_value = ""
    action = RetryFailedSessionAction(provider, retry_limit=1)
    snapshot = _snapshot(title="[WIP] resume task")
    derived = DerivedState(snapshot)
    with patch(
        f"{MODULE}.get_latest_session_state",
        return_value=SessionState(SessionOutcome.FAILED, failure_event_id=77),
    ):
        action.evaluate(snapshot, derived)
    action.execute(provider, snapshot, derived)
    prompt = provider.dispatch_agent_retry.call_args.args[1]
    assert "resume task" in prompt
    assert "No linked issue, prior repair context, or PR description could be recovered." in prompt


def test_retry_prompt_handles_missing_title_and_malformed_repair_context() -> None:
    provider = _provider()
    provider.get_pr_body.return_value = ""
    snapshot = _snapshot(title="")
    derived = DerivedState(snapshot)
    derived.set("agent_retry_comments", None)
    derived.set("agent_retry_dispatch_login", None)

    prompt = RetryFailedSessionAction(provider)._build_retry_prompt(snapshot, derived, "7", 1, 2)

    assert "## Pull request title" not in prompt
    assert "No linked issue, prior repair context, or PR description could be recovered." in prompt


def test_retry_uses_pr_description_when_no_linked_issue_or_repair_context_exists() -> None:
    provider = _provider()
    snapshot = _snapshot()
    derived = DerivedState(snapshot)
    derived.set("agent_retry_dispatch_login", "workflow-bot")
    assert "Original task description" in RetryFailedSessionAction(provider)._build_retry_prompt(
        snapshot,
        derived,
        "7",
        1,
        2,
    )


def test_retry_ignores_dedup_tracker_comment_as_repair_context() -> None:
    """The dedup tracker comment carries no findings and must not be used as context."""
    provider = _provider()
    snapshot = _snapshot()
    derived = DerivedState(snapshot)
    derived.set("agent_retry_dispatch_login", "workflow-bot")
    derived.set(
        "agent_retry_comments",
        [
            IssueCommentInfo(
                1, "workflow-bot", "<!-- repair-dispatch:deadbeef:1:writer -->\nDispatch tracking for `deadbeef`"
            )
        ],
    )
    prompt = RetryFailedSessionAction(provider)._build_retry_prompt(snapshot, derived, "7", 1, 2)
    assert "Dispatch tracking" not in prompt
    assert "Original task description" in prompt


def test_retry_ignores_its_own_agent_retry_and_escalation_comments_as_repair_context() -> None:
    provider = _provider()
    snapshot = _snapshot()
    derived = DerivedState(snapshot)
    derived.set("agent_retry_dispatch_login", "workflow-bot")
    derived.set(
        "agent_retry_comments",
        [
            IssueCommentInfo(1, "workflow-bot", "<!-- agdt:agent-retry:7:1 -->\n\n@copilot Please resume."),
            IssueCommentInfo(
                3,
                "workflow-bot",
                "@copilot\n\n<!-- agdt:agent-retry:8:1 -->\n\nPlease resume with the same task.",
            ),
            IssueCommentInfo(
                2,
                "workflow-bot",
                "<!-- agdt:agent-retry-escalation:7 -->\n\nEscalated after exhausting retries.",
            ),
        ],
    )
    prompt = RetryFailedSessionAction(provider)._build_retry_prompt(snapshot, derived, "7", 1, 2)
    assert "Please resume." not in prompt
    assert "Please resume with the same task." not in prompt
    assert "Escalated after exhausting retries." not in prompt
    assert "Original task description" in prompt


def test_retry_preserves_repair_context_that_quotes_a_retry_marker() -> None:
    provider = _provider()
    snapshot = _snapshot()
    derived = DerivedState(snapshot)
    derived.set("agent_retry_dispatch_login", "workflow-bot")
    derived.set(
        "agent_retry_comments",
        [
            IssueCommentInfo(
                1,
                "workflow-bot",
                "@copilot Please fix the quoted finding.\n\n"
                "## Finding\n\n"
                "```text\n<!-- agdt:agent-retry:task-abc:1 -->\n```",
            )
        ],
    )

    prompt = RetryFailedSessionAction(provider)._build_retry_prompt(snapshot, derived, "8", 1, 2)

    assert "Please fix the quoted finding." in prompt
    assert "<!-- agdt:agent-retry:task-abc:1 -->" in prompt


def test_retry_uses_conflict_repair_comment_as_repair_context() -> None:
    provider = _provider()
    snapshot = _snapshot()
    derived = DerivedState(snapshot)
    derived.set("agent_retry_dispatch_login", "workflow-bot")
    derived.set(
        "agent_retry_comments",
        [
            IssueCommentInfo(
                1,
                "workflow-bot",
                "@copilot Resolve merge conflicts.\n\n<!-- agdt:conflict-repair:abc:def -->",
            )
        ],
    )
    prompt = RetryFailedSessionAction(provider)._build_retry_prompt(snapshot, derived, "7", 1, 2)
    assert "Resolve merge conflicts." in prompt


@pytest.mark.parametrize(
    "header",
    [
        "<!-- agdt:agent-retry:7:1 -->",
        "<!-- agdt:agent-retry-escalation:7 -->",
    ],
)
def test_retry_and_escalation_context_do_not_become_conflict_repair_context(header: str) -> None:
    provider = _provider()
    snapshot = _snapshot()
    derived = DerivedState(snapshot)
    derived.set("agent_retry_dispatch_login", "workflow-bot")
    derived.set(
        "agent_retry_comments",
        [
            IssueCommentInfo(
                1,
                "workflow-bot",
                f"{header}\n\n@copilot Please resume the same task.\n\n"
                "<!-- agdt:conflict-repair:abc:def:2026-01-01T00:00:00Z -->",
            )
        ],
    )

    prompt = RetryFailedSessionAction(provider)._build_retry_prompt(snapshot, derived, "8", 1, 2)

    assert "Please resume the same task." not in prompt
    assert "Original task description" in prompt


def test_retry_context_lookup_failure_falls_back_to_pr_description() -> None:
    provider = _provider()
    provider.list_closing_issues.side_effect = RuntimeError("linked issue lookup failed")
    snapshot = _snapshot()
    derived = DerivedState(snapshot)
    prompt = RetryFailedSessionAction(provider)._build_retry_prompt(snapshot, derived, "7", 1, 2)
    assert "Original task description" in prompt


def test_retry_context_lookup_reraises_rate_limit() -> None:
    provider = _provider()
    provider.list_closing_issues.side_effect = ProviderRateLimitError(provider="github", is_rate_limit=True)
    snapshot = _snapshot()
    with pytest.raises(ProviderRateLimitError):
        RetryFailedSessionAction(provider)._build_retry_prompt(snapshot, DerivedState(snapshot), "7", 1, 2)


def test_retry_description_lookup_failure_keeps_context_note() -> None:
    provider = _provider()
    provider.list_closing_issues.side_effect = RuntimeError("linked issue lookup failed")
    provider.get_pr_body.side_effect = RuntimeError("PR body unavailable")
    snapshot = _snapshot()
    prompt = RetryFailedSessionAction(provider)._build_retry_prompt(snapshot, DerivedState(snapshot), "7", 1, 2)
    assert "No linked issue, prior repair context, or PR description could be recovered." in prompt


def test_retry_description_lookup_reraises_rate_limit() -> None:
    provider = _provider()
    provider.list_closing_issues.side_effect = RuntimeError("linked issue lookup failed")
    provider.get_pr_body.side_effect = ProviderRateLimitError(provider="github", is_rate_limit=True)
    snapshot = _snapshot()
    with pytest.raises(ProviderRateLimitError):
        RetryFailedSessionAction(provider)._build_retry_prompt(snapshot, DerivedState(snapshot), "7", 1, 2)
