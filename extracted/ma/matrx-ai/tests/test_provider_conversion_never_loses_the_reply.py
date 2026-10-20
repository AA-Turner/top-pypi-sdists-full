"""A provider-side media conversion never replaces the executor's history, and a shifted
history never loses the reply.

THE INCIDENT (defect 50, PB-05, 2026-10-19, conversation 21f6c74c-c4cc-4c78-bab7-85772c4080bc;
same signature 2026-10-18 on 1b499921…, request d24ef18f…): a brand-new conversation whose
first message carried attachments the model cannot read natively (a .docx, a .csv, a .txt…).
``UnifiedAIClient._execute_dispatch`` converts unsupported media to text before dispatch and
ASSIGNED the converted list back to ``request.config.messages``. When the send boundary built
no wire clone (no picklist / fence swaps this send), ``request.config`` IS the executor's live
config, so the whole history was swapped for new message objects. The turn barrier found its
trigger message "gone" (``persisted_history_shifted``: position 0, 1 -> 2 messages), raised
``PersistenceBarrierError``, and the reply the person had just watched stream was never stored.
Audio transcription had the identical assignment.

Two layers, both proven red before the fix:
1. the provider path converts on its own list — the live history keeps its objects;
2. if ANY future mutator shifts the history mid-turn, the barrier restores the history it
   recorded, records the shift, and still stores the reply.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import pytest
from matrx_connect import AppContext
from matrx_connect.context.app_context import _app_context, set_app_context

from matrx_ai.config import MessageList, TextContent, UnifiedConfig, UnifiedMessage
from matrx_ai.config.media_config import ImageContent
from matrx_ai.processing.media_fallback import handler
from matrx_ai.providers.unified_client import UnifiedAIClient
from matrx_ai.testing.profile_factory import make_profile

_TEXT_ONLY_CAPS = {
    "input": ["text"],
    "output": ["text"],
    "features": ["function_calling"],
    "interaction": "turn",
}


class _Emitter:
    async def send_warning(self, payload: Any) -> None:  # pragma: no cover - not under test
        pass

    async def send_info(self, payload: Any) -> None:  # pragma: no cover
        pass

    async def send_data(self, payload: Any) -> None:  # pragma: no cover
        pass


def _first_turn_config() -> UnifiedConfig:
    """The PB-05 shape: ONE user message with text + an attachment the model can't read."""
    config = UnifiedConfig.from_dict(
        {
            "model": "text-only-model",
            "messages": [
                {"role": "user", "content": [{"type": "text", "text": "Receiving line, please."}]}
            ],
        }
    )
    config.messages[0].content.append(ImageContent(base64_data="eA==", mime_type="image/jpeg"))
    config.messages.attach_turn_context("<live_date>today</live_date>", slot="probe")
    return config


async def _dispatch(monkeypatch: pytest.MonkeyPatch, config: UnifiedConfig) -> dict[str, Any]:
    profile = make_profile(
        model_name="text-only-model", wire_format="openai_chat", capabilities=dict(_TEXT_ONLY_CAPS)
    )
    sent: dict[str, Any] = {}

    async def _resolve(*_a: Any, **_k: Any):
        return profile

    async def _image_to_text(content: Any, ctx: Any) -> handler.ResolverResult:
        return handler.ResolverResult(
            replacement=TextContent(text="[Image OCR]\nLodi Orchards pallet tag"),
            action="extracted",
            user_message="Image converted to text.",
        )

    class _Provider:
        async def execute(self, wire_config: Any, _profile: Any, _debug: bool) -> Any:
            sent["messages"] = list(wire_config.messages)
            sent["turn_context"] = dict(wire_config.messages._turn_context_blocks)
            return SimpleNamespace(usage=None, messages=[])

    async def _client(_self: Any, _name: str) -> Any:
        return _Provider()

    async def _net(thunk: Any, **_k: Any) -> Any:
        return await thunk()

    import matrx_ai.catalog.resolve as resolve_mod

    monkeypatch.setattr(resolve_mod, "resolve_tts_call_profile", _resolve)
    monkeypatch.setattr(UnifiedAIClient, "_get_provider_client", _client)
    monkeypatch.setattr(UnifiedAIClient, "_dispatch_with_billing_net", staticmethod(_net))
    monkeypatch.setattr(handler, "_RESOLVERS", {handler.MediaContainer.IMAGE: _image_to_text})

    token = set_app_context(AppContext(emitter=_Emitter(), metadata={}))
    try:
        # No wire clone this send: the client is handed the executor's own config.
        request = SimpleNamespace(config=config, debug=False, add_usage=lambda _u: None)
        await UnifiedAIClient()._execute_dispatch(request)
    finally:
        _app_context.reset(token)
    return sent


@pytest.mark.asyncio
async def test_media_conversion_never_replaces_the_live_history(monkeypatch) -> None:
    config = _first_turn_config()
    ledger_list = config.messages
    ledger_items = list(config.messages)

    sent = await _dispatch(monkeypatch, config)

    # The executor's history is untouched: same list, same objects, original media…
    assert config.messages is ledger_list, (
        "the provider path replaced config.messages — the executor's trigger message is "
        "gone and the turn barrier refuses to store the reply (persisted_history_shifted)"
    )
    assert all(a is b for a, b in zip(config.messages, ledger_items, strict=True))
    assert any(isinstance(c, ImageContent) for c in config.messages[0].content)
    # …while the provider got the converted text…
    wire_parts = [c for m in sent["messages"] for c in m.content]
    assert any(isinstance(c, TextContent) and "pallet tag" in c.text for c in wire_parts)
    assert not any(isinstance(c, ImageContent) for c in wire_parts)
    # …with the turn's context channel still attached (the converted list dropped it).
    assert sent["turn_context"] == {"probe": "<live_date>today</live_date>"}


# ── Layer 2: a shifted history is restored and the reply is still stored ──


def _barrier_harness(monkeypatch: pytest.MonkeyPatch):
    from matrx_ai.orchestrator import executor

    persisted: list[Any] = []
    captured: list[dict[str, Any]] = []

    async def _persist(completed: Any, **kwargs: Any) -> None:
        persisted.append(
            {
                "messages": list(completed.request.config.messages),
                "start": completed.result_start_position,
                "end": completed.result_end_position,
                **kwargs,
            }
        )

    async def _capture(exc: BaseException, **kwargs: Any) -> None:
        captured.append({"exc": exc, **kwargs})

    async def _noop(*_a: Any, **_k: Any) -> None:
        return None

    import matrx_ai.config.usage_config as usage_config
    import matrx_ai.persistence.queue_helpers as queue_helpers
    import matrx_connect.streaming.error_capture as error_capture

    monkeypatch.setattr(executor, "persist_completed_request", _persist)
    monkeypatch.setattr(error_capture, "capture_error", _capture)
    monkeypatch.setattr(usage_config, "ensure_pricing_lookup", _noop)
    monkeypatch.setattr(queue_helpers, "get_coordinator", lambda: None)
    return executor, persisted, captured


def _start(request: Any, trigger_position: int) -> Any:
    """The executor's turn-start bookkeeping, exactly the fields it records."""
    from matrx_ai.orchestrator.execution_state import ExecutionState

    state = ExecutionState()
    messages = request.config.messages
    state.current_request = request
    state.pre_execution_message_count = len(messages)
    state.trigger_position = trigger_position
    state.trigger_message = messages[trigger_position]
    try:
        state.recorded_history = list(messages)
    except AttributeError:  # the pre-fix state had no recorded history (red run)
        pass
    return state


def _started_turn(executor: Any):
    from matrx_ai.orchestrator.requests import AIMatrixRequest

    config = _first_turn_config()
    request = AIMatrixRequest(conversation_id="conv-pb05", config=config, request_id="req-pb05")
    state = _start(request, 0)
    state.committed_position = -1
    return request, state


@pytest.mark.asyncio
async def test_the_exact_pb05_shift_still_stores_the_reply(monkeypatch) -> None:
    """1 message at start, history replaced wholesale, reply appended -> 2: stored, recorded."""
    executor, persisted, captured = _barrier_harness(monkeypatch)
    request, state = _started_turn(executor)
    trigger = request.config.messages[0]

    # What the provider path did: a NEW list of NEW message objects in place of the history.
    request.config.messages = MessageList(
        _messages=[UnifiedMessage(role="user", content=[TextContent(text="[converted]")])]
    )
    reply = UnifiedMessage(role="assistant", content=[TextContent(text="Receiving line ready.")])
    request.config.messages.append(reply)
    response = SimpleNamespace(messages=[reply], finish_reason="stop")

    await executor._persist_turn_and_commit(
        current_request=request,
        iteration=1,
        final_response=response,
        trigger_position=0,
        pre_execution_message_count=1,
        debug=False,
        state=state,
    )

    assert len(persisted) == 1, "the barrier refused the turn — the reply was never stored"
    stored = persisted[0]["messages"]
    assert stored[0] is trigger, "the person's original message must be what is stored"
    assert stored[1] is reply
    assert persisted[0]["end"] == 1
    assert state.committed_position == 1
    # The shift is still recorded, and says it was repaired.
    assert [c["kind"] for c in captured] == [executor.HISTORY_SHIFTED_KIND]
    assert captured[0]["payload"]["restored"] is True


@pytest.mark.asyncio
async def test_earlier_history_removed_mid_turn_is_restored_before_storing(monkeypatch) -> None:
    executor, persisted, _captured = _barrier_harness(monkeypatch)
    from matrx_ai.orchestrator.requests import AIMatrixRequest

    config = UnifiedConfig(model="m", messages=MessageList([]))
    history = [
        UnifiedMessage(role="user", content=[TextContent(text="one")]),
        UnifiedMessage(role="assistant", content=[TextContent(text="two")]),
        UnifiedMessage(role="user", content=[TextContent(text="three")]),
    ]
    config.messages.extend(history)
    request = AIMatrixRequest(conversation_id="c", config=config, request_id="r")
    state = _start(request, 2)
    state.committed_position = 1

    del config.messages._messages[1]  # a mutator dropped an earlier row
    reply = UnifiedMessage(role="assistant", content=[TextContent(text="four")])
    config.messages.append(reply)

    await executor._persist_turn_and_commit(
        current_request=request,
        iteration=1,
        final_response=SimpleNamespace(messages=[reply], finish_reason="stop"),
        trigger_position=2,
        pre_execution_message_count=3,
        debug=False,
        state=state,
    )

    assert persisted, "the reply was not stored"
    assert all(a is b for a, b in zip(persisted[0]["messages"], [*history, reply], strict=True))


@pytest.mark.asyncio
async def test_an_unrecoverable_shift_still_stops_honestly(monkeypatch) -> None:
    """Only when the recorded history cannot be lined up again does the turn stop."""
    from matrx_ai.persistence.coordinator import PersistenceBarrierError

    executor, persisted, captured = _barrier_harness(monkeypatch)
    from matrx_ai.orchestrator.requests import AIMatrixRequest

    config = UnifiedConfig(model="m", messages=MessageList([]))
    first = UnifiedMessage(role="user", content=[TextContent(text="one")])
    last = UnifiedMessage(role="user", content=[TextContent(text="two")])
    config.messages.extend([first, last])
    request = AIMatrixRequest(conversation_id="c", config=config, request_id="r")
    state = _start(request, 1)

    # The last recorded message is replaced but an earlier one survives: no safe alignment.
    config.messages._messages[1] = UnifiedMessage(role="user", content=[TextContent(text="x")])
    config.messages.append(UnifiedMessage(role="assistant", content=[TextContent(text="r")]))

    with pytest.raises(PersistenceBarrierError):
        await executor._persist_turn_and_commit(
            current_request=request,
            iteration=1,
            final_response=SimpleNamespace(messages=[], finish_reason="stop"),
            trigger_position=1,
            pre_execution_message_count=2,
            debug=False,
            state=state,
        )
    assert persisted == []
    assert captured and captured[0]["payload"]["restored"] is False
