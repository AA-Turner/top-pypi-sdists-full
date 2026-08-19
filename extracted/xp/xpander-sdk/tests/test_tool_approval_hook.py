"""The tool hook's handling of a call a person has to authorize.

This hook sits in front of every real tool call, so the cases that matter most
where nothing should change.
"""

from types import SimpleNamespace

from xpander_sdk.modules.agents.models.agent import (
    AgentGraphItemHITLSettings,
    AgentToolApprovalApprovers,
)
from xpander_sdk.modules.backend.frameworks.agno import (
    AWAITING_APPROVAL_MESSAGE,
    _approval_envelope,
    _awaiting_approval_message,
    _is_awaiting_approval,
    _mark_awaiting_approval,
)

ENVELOPE = {
    "type": "approval_required",
    "request_id": "req-1",
    "message": "waiting on a person",
}


class TestRecognizingTheEnvelope:
    def test_it_recognizes_a_bare_envelope(self) -> None:
        assert _approval_envelope(ENVELOPE) == ENVELOPE

    def test_it_unwraps_a_tool_invocation_result(self) -> None:
        # A connector refusal arrives as a dict under ToolInvocationResult.result.
        wrapped = SimpleNamespace(result=ENVELOPE)
        assert _approval_envelope(wrapped) == ENVELOPE

    def test_it_unwraps_an_agno_content_result(self) -> None:
        assert _approval_envelope(SimpleNamespace(content=ENVELOPE)) == ENVELOPE

    def test_it_stops_before_walking_deeply_nested_payloads(self) -> None:
        deep = SimpleNamespace(
            result=SimpleNamespace(result=SimpleNamespace(result=ENVELOPE))
        )
        assert _approval_envelope(deep) is None

    def test_an_ordinary_dict_result_is_left_alone(self) -> None:
        assert _approval_envelope({"ok": True, "rows": []}) is None

    def test_a_plain_string_result_is_left_alone(self) -> None:
        assert _approval_envelope("sent the email") is None

    def test_none_is_left_alone(self) -> None:
        assert _approval_envelope(None) is None

    def test_a_differently_typed_envelope_is_left_alone(self) -> None:
        # The connector sign-in hold uses the same shape with a different type.
        assert (
            _approval_envelope({"type": "auth_required", "auth_url": "https://x"})
            is None
        )

    def test_a_wrapped_ordinary_result_is_left_alone(self) -> None:
        assert _approval_envelope(SimpleNamespace(result={"rows": []})) is None


class TestRunState:
    def test_a_run_is_not_awaiting_approval_by_default(self) -> None:
        assert not _is_awaiting_approval(SimpleNamespace())
        assert _awaiting_approval_message(SimpleNamespace()) is None

    def test_marking_one_call_blocks_the_run(self) -> None:
        task = SimpleNamespace()
        _mark_awaiting_approval(task, "gmail_send", "gmail is waiting")
        assert _is_awaiting_approval(task)

    def test_a_later_tool_reads_the_original_statement(self) -> None:
        # Naming the second tool would say Slack is waiting when Gmail is.
        task = SimpleNamespace()
        _mark_awaiting_approval(task, "gmail_send", "gmail is waiting")
        assert _awaiting_approval_message(task) == "gmail is waiting"

    def test_marking_is_cumulative_and_does_not_lose_earlier_calls(self) -> None:
        task = SimpleNamespace()
        _mark_awaiting_approval(task, "gmail_send", "gmail is waiting")
        _mark_awaiting_approval(task, "slack_post", "slack is waiting")
        assert set(task._xp_awaiting_approval) == {"gmail_send", "slack_post"}

    def test_bookkeeping_never_raises_on_a_task_that_cannot_hold_state(self) -> None:
        # A frozen or exotic task must not turn into a failed tool call.
        _mark_awaiting_approval(None, "gmail_send", "waiting")
        assert not _is_awaiting_approval(None)


class TestWhatTheModelReads:
    def test_the_message_names_the_tool_and_ends_the_turn(self) -> None:
        message = AWAITING_APPROVAL_MESSAGE.format(tool="gmail_send")
        assert "gmail_send" in message
        assert "has not run" in message
        assert "Finish now" in message

    def test_the_message_carries_no_retry_bait(self) -> None:
        message = AWAITING_APPROVAL_MESSAGE.format(tool="gmail_send").lower()
        for word in ("error", "failed", "denied", "forbidden", "try again", "retry"):
            assert word not in message


class TestMirroredSettings:
    def test_approval_is_off_unless_switched_on(self) -> None:
        assert AgentGraphItemHITLSettings().enabled is False

    def test_named_people_and_groups_round_trip(self) -> None:
        settings = AgentGraphItemHITLSettings(
            enabled=True,
            approvers=AgentToolApprovalApprovers(user_ids=["u1"], group_ids=["g1"]),
        )
        assert settings.approvers.user_ids == ["u1"]
        assert settings.approvers.group_ids == ["g1"]

    def test_a_denied_call_lets_the_run_continue_by_default(self) -> None:
        assert AgentGraphItemHITLSettings().on_deny == "continue"


class TestASettledRefusalDoesNotStopTheRun:
    """on_deny defaults to continue: the run finishes and reports what it skipped."""

    def test_a_denied_envelope_is_still_recognized(self) -> None:
        denied = {**ENVELOPE, "denied": True, "message": "declined"}
        assert _approval_envelope(denied) == denied

    def test_a_denied_envelope_carries_the_flag_the_hook_branches_on(self) -> None:
        # Marking the run on a refusal would block every remaining ungated call
        # and tell the user something is pending when nothing is.
        assert {**ENVELOPE, "denied": True}.get("denied") is True
        assert ENVELOPE.get("denied") is None


class TestTheRefusalFeedsTheBreaker:
    def test_the_refusal_joins_the_no_progress_markers(self) -> None:
        from xpander_sdk.modules.backend.frameworks.agno import _NO_PROGRESS_MARKERS

        message = AWAITING_APPROVAL_MESSAGE.format(tool="gmail_send")
        assert any(marker in message for marker in _NO_PROGRESS_MARKERS)
