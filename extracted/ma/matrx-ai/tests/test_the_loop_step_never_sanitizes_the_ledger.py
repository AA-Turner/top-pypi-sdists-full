"""The loop step never sanitizes the executor's ledger, and a shifted ledger stops the turn.

THE INCIDENT (Lane AZ2, 2026-09-28): admin@admin.com's permanent staff thread
``3af9e95c-699d-5e78-a506-736e4768273e`` wrote no ``chat.message`` from
2026-09-26 16:03Z, even after Lane AZ's wire-copy fix (``0529a0e186``) shipped:
``ops.system_error`` kind ``persisted_history_shifted`` fired 419 times on that
thread between 07:34Z and 14:05Z, every one "trigger message was at position 141
… now at 136". The second in-place mutator was the loop step itself:
``AIMatrixRequest.add_response`` built the next config with
``dataclasses.replace(config, messages=…)``, ``replace`` re-ran
``UnifiedConfig.__post_init__``, and its hydration pass ran
``MessageList.sanitize()`` on the NEW LIVE list — deleting the thread's five old
orphan/emptied rows mid-turn. The executor's cursors are list indices and
``chat.message.position`` IS that index, so the barrier wrote nothing.

Two independent layers, each tested here:
1. ``add_response`` never sanitizes: the earlier history keeps every object at
   its index (fails against ``replace``).
2. The per-turn barrier REFUSES to persist a shifted ledger: it raises the same
   ``PersistenceBarrierError`` every failed barrier raises, so the turn fails
   honestly instead of answering while saving nothing (fails against the
   scream-and-continue barrier).
"""

from __future__ import annotations

import asyncio
from typing import Any

import pytest

from matrx_ai.config.enums import Role
from matrx_ai.config.message_config import MessageList, UnifiedMessage
from matrx_ai.config.tools_config import ToolCallContent, ToolResultContent
from matrx_ai.config.unified_config import UnifiedConfig, UnifiedResponse
from matrx_ai.config.unified_content import TextContent
from matrx_ai.orchestrator.requests import AIMatrixRequest


def _orphan_result(call_id: str) -> UnifiedMessage:
    return UnifiedMessage(
        role=Role.TOOL,
        content=[
            ToolResultContent(
                tool_use_id=call_id,
                call_id=call_id,
                name="shell_execute",
                content="Linux 47925faabf58 6.1.159",
            )
        ],
    )


def _permanent_thread_request() -> AIMatrixRequest:
    """3af9e95c's shape on 2026-09-28: old orphan rows, an emptied assistant row, then this turn."""
    config = UnifiedConfig(model="claude-sonnet-5", messages=MessageList([]))
    # Loaded after construction, exactly as the resolver does, so hydration never saw it.
    config.messages.extend(
        [
            UnifiedMessage(role=Role.USER, content=[TextContent(text="what's in my workspace?")]),
            UnifiedMessage(role=Role.ASSISTANT, content=[TextContent(text="Your workspace has…")]),
            _orphan_result("toolu_01JesXFtFByL9XYNfq7osTAg"),
            UnifiedMessage(role=Role.ASSISTANT, content=[]),
            _orphan_result("toolu_01H4e8GCx7BftjTZeheVcSPW"),
            _orphan_result("toolu_012DjopkitjjiDMes8NjQ2sd"),
            UnifiedMessage(role=Role.USER, content=[TextContent(text="run uname -a")]),
        ]
    )
    return AIMatrixRequest(conversation_id="3af9e95c", config=config, request_id="r-1")


def _tool_call_response() -> UnifiedResponse:
    return UnifiedResponse(
        messages=[
            UnifiedMessage(
                role=Role.ASSISTANT,
                content=[
                    ToolCallContent(
                        id="toolu_new", name="shell_execute", arguments={"command": "uname -a"}
                    )
                ],
            )
        ]
    )


def _this_turns_result() -> list[ToolResultContent]:
    return [
        ToolResultContent(
            tool_use_id="toolu_new", call_id="toolu_new", name="shell_execute", content="Linux box"
        )
    ]


def test_the_loop_step_keeps_every_earlier_message_at_its_index() -> None:
    request = _permanent_thread_request()
    ledger_before = list(request.config.messages)

    updated = AIMatrixRequest.add_response(request, _tool_call_response(), _this_turns_result())

    after = list(updated.config.messages)
    assert len(after) == len(ledger_before) + 2, (
        "the loop step removed or inserted history — every cursor the executor holds "
        f"for this turn is now wrong ({len(ledger_before)} + 2 expected, got {len(after)})"
    )
    assert all(a is b for a, b in zip(after, ledger_before, strict=False)), (
        "an earlier message moved: chat.message.position is the list index"
    )
    # The config is still the normalized one, not a re-hydrated stranger.
    assert updated.config.model == request.config.model
    assert updated.config.messages is not request.config.messages


def test_the_barrier_arithmetic_still_holds_after_the_loop_step() -> None:
    request = _permanent_thread_request()
    pre_execution_message_count = len(request.config.messages)
    trigger_position = pre_execution_message_count - 1
    committed_position = trigger_position - 1
    trigger = request.config.messages[trigger_position]

    updated = AIMatrixRequest.add_response(request, _tool_call_response(), _this_turns_result())

    assert updated.config.messages[trigger_position] is trigger
    assert len(updated.config.messages) - 1 > committed_position


def _shifted_turn() -> tuple[Any, Any]:
    from matrx_ai.orchestrator.execution_state import ExecutionState

    request = _permanent_thread_request()
    state = ExecutionState()
    state.pre_execution_message_count = len(request.config.messages)
    state.trigger_position = state.pre_execution_message_count - 1
    state.committed_position = state.trigger_position - 1
    state.trigger_message = request.config.messages[state.trigger_position]
    # What replace()+sanitize did on the live list: old rows gone mid-turn.
    del request.config.messages._messages[2:6]
    request.config.messages.append(
        UnifiedMessage(role=Role.ASSISTANT, content=[TextContent(text="Linux box")])
    )
    return request, state


def test_the_barrier_refuses_to_persist_a_shifted_ledger(monkeypatch) -> None:
    import matrx_connect.streaming.error_capture as error_capture

    from matrx_ai.orchestrator import executor
    from matrx_ai.persistence.coordinator import PersistenceBarrierError

    captured: list[dict[str, Any]] = []

    async def _capture(exc: BaseException, **kwargs: Any) -> None:
        captured.append({"exc": exc, **kwargs})

    async def _must_not_persist(*_a: Any, **_k: Any) -> None:
        raise AssertionError("a shifted ledger reached persist_completed_request")

    monkeypatch.setattr(error_capture, "capture_error", _capture)
    monkeypatch.setattr(executor, "persist_completed_request", _must_not_persist)

    request, state = _shifted_turn()

    with pytest.raises(PersistenceBarrierError) as raised:
        asyncio.run(
            executor._persist_turn_and_commit(
                current_request=request,
                iteration=1,
                final_response=UnifiedResponse(messages=[]),
                trigger_position=state.trigger_position,
                pre_execution_message_count=state.pre_execution_message_count,
                debug=False,
                state=state,
            )
        )

    assert raised.value.reason == executor.HISTORY_SHIFTED_KIND
    assert raised.value.conversation_id == "3af9e95c"
    assert [c["kind"] for c in captured] == [executor.HISTORY_SHIFTED_KIND]


def test_an_unshifted_turn_is_not_refused(monkeypatch) -> None:
    """The refusal must be specific: a clean turn passes the check and reaches persistence."""
    import matrx_connect.streaming.error_capture as error_capture

    from matrx_ai.orchestrator import executor

    reached: list[bool] = []

    class _Reached(Exception):
        pass

    async def _capture(exc: BaseException, **kwargs: Any) -> None:
        raise AssertionError(f"a clean turn screamed: {exc}")

    async def _persist(*_a: Any, **_k: Any) -> None:
        reached.append(True)
        raise _Reached

    monkeypatch.setattr(error_capture, "capture_error", _capture)
    monkeypatch.setattr(executor, "persist_completed_request", _persist)

    from matrx_ai.orchestrator.execution_state import ExecutionState

    request = _permanent_thread_request()
    state = ExecutionState()
    state.pre_execution_message_count = len(request.config.messages)
    state.trigger_position = state.pre_execution_message_count - 1
    state.committed_position = state.trigger_position - 1
    state.trigger_message = request.config.messages[state.trigger_position]
    request = AIMatrixRequest.add_response(request, _tool_call_response(), _this_turns_result())

    with pytest.raises(_Reached):
        asyncio.run(
            executor._persist_turn_and_commit(
                current_request=request,
                iteration=1,
                final_response=UnifiedResponse(messages=[]),
                trigger_position=state.trigger_position,
                pre_execution_message_count=state.pre_execution_message_count,
                debug=False,
                state=state,
            )
        )
    assert reached == [True]
