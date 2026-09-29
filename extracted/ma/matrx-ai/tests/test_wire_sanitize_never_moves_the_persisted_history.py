"""The provider-payload sanitizer shapes the WIRE copy, never the live history.

THE INCIDENT (Lane AZ, 2026-09-28): admin@admin.com's permanent staff thread
``3af9e95c-699d-5e78-a506-736e4768273e`` stopped writing ``chat.message`` rows.
Its user rows stopped on 2026-09-21 and every row stopped on 2026-09-26 16:03Z,
while every turn still ran, answered the phone and wrote ``chat.tool_call``.

The history of that thread carried orphan ``tool_result`` messages (and an
empty assistant row) from earlier broken turns. ``BaseTranslator.build_request``
runs ``MessageList.sanitize()`` on the config it is handed, and
``_build_provider_wire_config`` handed it a SHALLOW copy — the same
``MessageList`` object the executor counts. So the sanitizer DELETED k old
messages from the live list in the middle of the turn. The executor's
bookkeeping is positional (``trigger_position = pre_count - 1``,
``committed_position = trigger_position - 1``, and the barrier writes only
positions above it), so after the reply was appended:

* k = 1 — the person's message slid below the high-water mark and was never
  written; only the reply was (09-21 → 09-26: assistant rows, no user rows);
* k >= 2 — ``post_count - 1 <= committed_position`` and the barrier returned
  early: nothing at all was written (09-26 16:03Z onward).

Any conversation whose history ever acquired a message the sanitizer drops was
exposed; the permanent thread is where one old corruption lives forever.

These guards FAIL against the pre-fix wire copy and pass now.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

from matrx_ai.config.enums import Role
from matrx_ai.config.message_config import MessageList, UnifiedMessage
from matrx_ai.config.tools_config import ToolResultContent
from matrx_ai.config.unified_config import UnifiedConfig
from matrx_ai.config.unified_content import TextContent
from matrx_ai.providers.base_translator import BaseTranslator
from matrx_ai.providers.unified_client import _build_provider_wire_config


class _PayloadCapture(BaseTranslator):
    """The real ``build_request`` chokepoint; assembly just records what it got."""

    def __init__(self) -> None:
        self.sent: list[UnifiedMessage] = []

    def _assemble_request(self, config: UnifiedConfig, route_ctx: Any = "") -> Any:
        self.sent = list(config.messages)
        return {"messages": len(self.sent)}


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


def _permanent_thread_config() -> UnifiedConfig:
    """The shape of 3af9e95c at 2026-09-28: old orphan results, then this turn's text."""
    # History is loaded AFTER construction, exactly as the resolver does it
    # (``config.messages.clear(); config.messages.extend(rebuilt)``), so the
    # hydration-time sanitize never sees it.
    config = UnifiedConfig(model="claude-sonnet-5", messages=MessageList([]))
    config.messages.extend(
        [
            UnifiedMessage(role=Role.USER, content=[TextContent(text="what's in my workspace?")]),
            UnifiedMessage(role=Role.ASSISTANT, content=[TextContent(text="Your workspace has…")]),
            _orphan_result("toolu_01JesXFtFByL9XYNfq7osTAg"),
            _orphan_result("toolu_012DjopkitjjiDMes8NjQ2sd"),
            UnifiedMessage(role=Role.USER, content=[TextContent(text="run uname -a")]),
        ]
    )
    return config


def _profile() -> SimpleNamespace:
    return SimpleNamespace(provider_model_id="claude-sonnet-5-wire", model_name="claude-sonnet-5")


def test_building_the_payload_never_removes_a_message_from_the_live_history() -> None:
    config = _permanent_thread_config()
    live_before = list(config.messages)

    translator = _PayloadCapture()
    translator.build_request(_build_provider_wire_config(config, _profile()), _profile())

    # The provider still gets the clean payload…
    assert len(translator.sent) == 3, [m.role for m in translator.sent]
    assert all(not isinstance(c, ToolResultContent) for m in translator.sent for c in m.content)
    # …and the executor's list is untouched: same length, same objects, same order.
    assert len(config.messages) == len(live_before), (
        "the sanitizer deleted messages from the LIVE history — every position the "
        "executor holds for this turn is now wrong and the barrier drops its rows"
    )
    assert all(a is b for a, b in zip(config.messages, live_before, strict=True))


def test_the_turn_barrier_still_sees_this_turns_rows_after_a_dirty_history() -> None:
    """The executor's positional arithmetic, run exactly as ``_persist_turn_and_commit`` does."""
    config = _permanent_thread_config()
    pre_execution_message_count = len(config.messages)
    trigger_position = pre_execution_message_count - 1
    committed_position = trigger_position - 1

    _PayloadCapture().build_request(_build_provider_wire_config(config, _profile()), _profile())
    config.messages.append(
        UnifiedMessage(role=Role.ASSISTANT, content=[TextContent(text="Linux 4792…")])
    )

    post_count = len(config.messages)
    assert post_count - 1 > committed_position, (
        "the per-turn barrier would early-return and write NOTHING for this turn"
    )
    trigger = config.messages[trigger_position]
    assert trigger.role == Role.USER and trigger.content[0].text == "run uname -a", (
        "the person's message is no longer at the trigger position — it is never written"
    )


def test_the_wire_copy_keeps_the_turn_context_channel() -> None:
    config = _permanent_thread_config()
    config.messages.attach_turn_context("<ctx>now</ctx>", slot="probe")

    wire = _build_provider_wire_config(config, _profile())

    assert wire.messages is not config.messages
    assert wire.messages._turn_context_blocks == config.messages._turn_context_blocks
    assert wire.model == "claude-sonnet-5-wire" and config.model == "claude-sonnet-5"


# ── Layer 2: the executor screams when anything shifts the live history mid-turn ──


def _state_for(config: UnifiedConfig) -> tuple[Any, Any]:
    from matrx_ai.orchestrator.execution_state import ExecutionState

    state = ExecutionState()
    state.pre_execution_message_count = len(config.messages)
    state.trigger_position = len(config.messages) - 1
    state.trigger_message = config.messages[state.trigger_position]
    request = SimpleNamespace(config=config, request_id=None, conversation_id=None)
    return state, request


def test_the_barrier_screams_when_earlier_history_is_removed_mid_turn(monkeypatch) -> None:
    import asyncio

    import matrx_connect.streaming.error_capture as error_capture
    from matrx_ai.orchestrator import executor

    captured: list[dict[str, Any]] = []

    async def _capture(exc: BaseException, **kwargs: Any) -> None:
        captured.append({"exc": exc, **kwargs})

    monkeypatch.setattr(error_capture, "capture_error", _capture)

    config = _permanent_thread_config()
    state, request = _state_for(config)

    assert asyncio.run(executor._scream_if_history_shifted(request, state, seam="t")) is False
    assert captured == []

    # What the pre-fix sanitizer did to the live list: two old orphan rows gone.
    del config.messages._messages[2:4]

    assert asyncio.run(executor._scream_if_history_shifted(request, state, seam="t")) is True
    assert [c["kind"] for c in captured] == [executor.HISTORY_SHIFTED_KIND]
    assert captured[0]["payload"]["moved_to"] == 2
