"""The tool hook's handling of a call a person has to authorize.

This hook sits in front of every real tool call, so the cases that matter most
where nothing should change.
"""

import asyncio
import time

from pathlib import Path
from types import SimpleNamespace
from typing import Any, Dict

import pytest

from xpander_sdk.modules.agents.models.agent import (
    AgentGraphItemHITLSettings,
    AgentToolApprovalApprovers,
)
from xpander_sdk.modules.backend.frameworks import agno as agno_module
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


class TestASuppressedAttemptIsNotAnEvent:
    """A held run must not read as an agent retrying against its own gate."""

    @staticmethod
    def _guard_block() -> str:
        """The awaiting-approval guard, up to the next guard that follows it."""
        source = Path(agno_module.__file__).read_text()
        start = source.index("_is_awaiting_approval(task)")
        end = source.index("_is_tool_disabled(task, eff_name)", start)
        return source[start:end]

    def test_the_approval_block_reports_nothing(self) -> None:
        """The guard writes no activity entry for a call it refused."""
        # A suppressed attempt logged as a failed call reads as a retry against the gate.
        assert "_report_blocked_call" not in self._guard_block()

    def test_the_guard_after_it_still_reports(self) -> None:
        """Only the approval case is quiet; every other guard still emits."""
        # Silence was the original bug there: a stuck run looked like nothing was happening.
        source = Path(agno_module.__file__).read_text()
        after = source[source.index("_is_tool_disabled(task, eff_name)") :]
        assert "_report_blocked_call" in after[:2000]


class TestHoldingASelfApproveCallOpen:
    """Nobody was asked but the person watching, so the call waits instead of the run parking."""

    def _agent(self) -> SimpleNamespace:
        """The minimum an agent needs to be polled against: an id and a configuration."""
        return SimpleNamespace(id="agent-1", configuration=SimpleNamespace())

    @pytest.mark.asyncio
    async def test_it_returns_the_decision_once_the_person_answers(
        self, monkeypatch
    ) -> None:
        answers = [{"settled": False}, {"settled": True, "approved": True}]

        class _Client:
            """A platform that answers pending, then settled."""

            def __init__(self, **_kw) -> None:
                pass

            async def make_request(self, **_kw) -> Dict[str, Any]:
                """Return the next scripted status."""
                return answers.pop(0)

        monkeypatch.setattr(agno_module, "APIClient", _Client)
        monkeypatch.setattr(agno_module, "SELF_APPROVE_POLL_SECONDS", 0)
        out = await agno_module._await_self_approval(self._agent(), "req-1", 30)
        assert out == {"settled": True, "approved": True}

    @pytest.mark.asyncio
    async def test_it_gives_up_at_the_window_rather_than_holding_forever(
        self, monkeypatch
    ) -> None:
        class _Client:
            """A platform where nobody ever answers."""

            def __init__(self, **_kw) -> None:
                pass

            async def make_request(self, **_kw) -> Dict[str, Any]:
                """Never settle."""
                return {"settled": False}

        monkeypatch.setattr(agno_module, "APIClient", _Client)
        monkeypatch.setattr(agno_module, "SELF_APPROVE_POLL_SECONDS", 0)
        # None is not a failure: the caller falls through and parks exactly as it always did.
        assert (
            await agno_module._await_self_approval(self._agent(), "req-1", 0.05) is None
        )

    @pytest.mark.asyncio
    async def test_a_platform_blip_costs_the_poll_and_not_the_hold(
        self, monkeypatch
    ) -> None:
        calls = {"n": 0}

        class _Client:
            def __init__(self, **_kw):
                pass

            async def make_request(self, **_kw) -> Dict[str, Any]:
                """Fail once, then settle."""
                calls["n"] += 1
                if calls["n"] == 1:
                    raise RuntimeError("connection reset")
                return {"settled": True, "approved": True}

        monkeypatch.setattr(agno_module, "APIClient", _Client)
        monkeypatch.setattr(agno_module, "SELF_APPROVE_POLL_SECONDS", 0)
        out = await agno_module._await_self_approval(self._agent(), "req-1", 30)
        assert out and out["approved"] is True

    @pytest.mark.asyncio
    async def test_no_window_means_no_hold_at_all(self, monkeypatch) -> None:
        # An envelope with no wait_seconds is the old shape and must behave like the old shape.
        called = {"n": 0}

        class _Client:
            """Records that it was constructed at all, which it must not be."""

            def __init__(self, **_kw) -> None:
                called["n"] += 1

            async def make_request(self, **_kw) -> Dict[str, Any]:
                """Would settle, if it were ever reached."""
                return {"settled": True, "approved": True}

        monkeypatch.setattr(agno_module, "APIClient", _Client)
        assert (
            await agno_module._await_self_approval(self._agent(), "req-1", None) is None
        )
        assert (
            await agno_module._await_self_approval(self._agent(), "req-1", "nonsense")
            is None
        )
        assert called["n"] == 0

    @pytest.mark.asyncio
    async def test_it_never_holds_longer_than_its_own_ceiling(
        self, monkeypatch
    ) -> None:
        # The window comes off the wire, so an absurd value must not strand a worker.
        waited = []

        class _Client:
            """A platform that never settles, to prove the ceiling ends the hold."""

            def __init__(self, **_kw) -> None:
                pass

            async def make_request(self, **_kw) -> Dict[str, Any]:
                """Never settle."""
                waited.append(1)
                return {"settled": False}

        monkeypatch.setattr(agno_module, "APIClient", _Client)
        monkeypatch.setattr(agno_module, "SELF_APPROVE_POLL_SECONDS", 0)
        monkeypatch.setattr(agno_module, "SELF_APPROVE_MAX_WAIT_SECONDS", 0.05)
        assert (
            await agno_module._await_self_approval(self._agent(), "req-1", 10_000)
            is None
        )

    @pytest.mark.asyncio
    async def test_one_slow_poll_cannot_outlive_the_window(self, monkeypatch) -> None:
        """A hung request must end with the hold, not with the client's own long timeout."""

        class _Client:
            """A platform that accepts the request and never answers it."""

            def __init__(self, **_kw) -> None:
                pass

            async def make_request(self, **_kw) -> Dict[str, Any]:
                """Hang for far longer than any hold window."""
                await asyncio.sleep(60)
                return {"settled": True, "approved": True}

        monkeypatch.setattr(agno_module, "APIClient", _Client)
        monkeypatch.setattr(agno_module, "SELF_APPROVE_POLL_SECONDS", 0)
        started = time.monotonic()
        assert (
            await agno_module._await_self_approval(self._agent(), "req-1", 0.2) is None
        )
        assert time.monotonic() - started < 5


class TestWhatTheModelReadsWhenSomeoneSaysNo:
    """A decline is a settled fact with a next step, never an error to retry against."""

    def test_it_names_the_decider_and_offers_a_way_on(self) -> None:
        message = agno_module._declined_message(
            {"decided_by_name": "Dana Cohen"}, "gmail_send"
        )
        assert "Dana Cohen declined" in message
        assert "gmail_send" in message
        assert "answer now" in message

    def test_it_carries_the_reason_when_one_was_given(self) -> None:
        message = agno_module._declined_message(
            {"decided_by_name": "Dana", "decision_note": "wrong recipient list"},
            "gmail_send",
        )
        assert 'They said: "wrong recipient list"' in message

    def test_it_reads_fine_when_nobody_is_named(self) -> None:
        message = agno_module._declined_message({}, "gmail_send")
        assert message.startswith("The person who was asked declined")
