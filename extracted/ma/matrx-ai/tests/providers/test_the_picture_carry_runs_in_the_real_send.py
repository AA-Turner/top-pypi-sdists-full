"""The assistant-turn media carry, driven through the REAL send boundary (CGU-10 AND-V IMG5).

Findings this file closes (``common-docs/systems/chat/projects/chat-ground-up/CGU-10-verification-2026-11-11img5.md``):

1. SP1 — removing the ``assistant_turn_media`` step from ``prepare_for_send`` passed every test,
   because the builder's tests call ``_carry_assistant_media`` directly. Here every case runs
   ``prepare_for_send(stage=loop)`` end to end; only the catalog profile lookup is replaced.
2. The carry is RECORDED when something moved — ``SendPrep.carried_media``, the step name, and
   the request row's ``metadata.assistant_media_carried`` — and never on a send where nothing
   moved.
3. A model the catalog declares ``strict_role_alternation`` never gets two user turns in a row:
   the carried picture leads the person's turn instead.
4. Moonshot's assistant-turn row, Anthropic's last layer, and the carried turn's host / hidden
   markers each have a case of their own.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import pytest

from matrx_ai.catalog import resolve as catalog_resolve
from matrx_ai.config import (
    MessageList,
    TextContent,
    UnifiedConfig,
    UnifiedMessage,
    context_preflight,
)
from matrx_ai.config.assistant_turn_media import CARRIED_MEDIA_KEY, carry_assistant_media
from matrx_ai.config.context_trim import TrimPolicy
from matrx_ai.config.media_config import ImageContent
from matrx_ai.config.message_config import HOST_AUTHORED_BY
from matrx_ai.config.send_boundary import STAGE_LOOP, prepare_for_send, reset_loop_state
from matrx_ai.testing.profile_factory import make_profile

_PNG = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
_FILE_ID = "5d64da50-0000-4000-8000-0000000000a5"
CONVERSATION_ID = "conv-img5-carry"
REQUEST_ID = "img5-carry-request"

_CHAT = {"input": ["text", "image"], "output": ["text"], "features": ["function_calling"], "interaction": "turn"}
_STRICT = {**_CHAT, "features": ["function_calling", "strict_role_alternation"]}


def _picture() -> ImageContent:
    return ImageContent(base64_data=_PNG, mime_type="image/png", file_id=_FILE_ID)


def _history(*, picture: bool = True) -> list[UnifiedMessage]:
    answer: list[Any] = [TextContent(text="Here it is.")]
    if picture:
        answer.append(_picture())
    return [
        UnifiedMessage(role="user", content=[TextContent(text="Make a red square.")]),
        UnifiedMessage(role="assistant", content=answer),
        UnifiedMessage(role="user", content=[TextContent(text="Describe what you made.")]),
    ]


def _role(message: Any) -> str:
    role = getattr(message, "role", None)
    return str(getattr(role, "value", role))


def _images(message: Any) -> int:
    return sum(isinstance(part, ImageContent) for part in (getattr(message, "content", None) or []))


@pytest.fixture
def route(monkeypatch):
    """Point the boundary's catalog lookup at a test profile; everything else is the real thing."""
    chosen: dict[str, Any] = {}

    async def _profile(model: str, **_kw: Any) -> Any:
        return make_profile(model_name=model, wire_format=chosen["wire"], capabilities=chosen["caps"])

    monkeypatch.setattr(catalog_resolve, "resolve_call_profile", _profile)
    monkeypatch.setattr(context_preflight, "_declared_window", lambda _ref: None)
    reset_loop_state(CONVERSATION_ID, REQUEST_ID)

    def _set(wire: str, caps: dict[str, Any] | None = None) -> None:
        chosen["wire"] = wire
        chosen["caps"] = caps or _CHAT

    yield _set
    reset_loop_state(CONVERSATION_ID, REQUEST_ID)


async def _send(history: list[UnifiedMessage], *, iteration: int = 1) -> tuple[Any, UnifiedConfig]:
    config = UnifiedConfig(model="m-img5", messages=MessageList(_messages=history))
    prep = await prepare_for_send(
        config,
        stage=STAGE_LOOP,
        conversation_id=CONVERSATION_ID,
        request_id=REQUEST_ID,
        iteration=iteration,
        policy=TrimPolicy(),
    )
    return prep, config


def _wire(prep: Any, config: UnifiedConfig) -> list[Any]:
    return list((prep.wire_config if prep.wire_config is not None else config).messages)


# ── 1. the real send carries the picture (SP1) ────────────────────────────────


@pytest.mark.asyncio
@pytest.mark.parametrize("wire", ["anthropic_chat", "openai_chat", "groq_chat", "moonshot_chat"])
async def test_prepare_for_send_carries_a_made_picture_to_a_user_turn(route, wire: str) -> None:
    route(wire)
    history = _history()
    prep, config = await _send(history)
    messages = _wire(prep, config)
    assert all(_images(m) == 0 for m in messages if _role(m) == "assistant"), messages
    assistant_at = next(i for i, m in enumerate(messages) if _role(m) == "assistant")
    assert sum(_images(m) for m in messages[assistant_at + 1 :] if _role(m) == "user") == 1, messages
    # The stored conversation still holds the picture on its own turn.
    assert _images(history[1]) == 1


# ── 2. the carry is recorded, only when it moved something ───────────────────


@pytest.mark.asyncio
async def test_a_carry_is_recorded_on_the_prep_and_the_request_row(route, monkeypatch) -> None:
    from matrx_ai.context import app_context

    ctx = SimpleNamespace(metadata={})
    monkeypatch.setattr(app_context, "try_get_app_context", lambda: ctx)
    route("anthropic_chat")
    prep, _ = await _send(_history(), iteration=2)
    assert "assistant_turn_media" in prep.steps
    assert prep.carried_media == [{"kind": "image", "at": 1, "file_id": _FILE_ID}]
    assert ctx.metadata["carried_media_by_iteration"] == {2: prep.carried_media}


@pytest.mark.asyncio
async def test_a_send_with_nothing_to_carry_records_nothing(route, monkeypatch) -> None:
    from matrx_ai.context import app_context

    ctx = SimpleNamespace(metadata={})
    monkeypatch.setattr(app_context, "try_get_app_context", lambda: ctx)
    route("anthropic_chat")
    prep, _ = await _send(_history(picture=False))
    assert "assistant_turn_media" not in prep.steps
    assert prep.carried_media is None
    assert "carried_media_by_iteration" not in ctx.metadata


@pytest.mark.asyncio
async def test_the_request_row_stores_what_moved(route) -> None:
    """The real send under a real AppContext, then the real row builder: iteration 2's row holds
    ``metadata.assistant_media_carried``; the other rows hold nothing."""
    from matrx_ai.config.usage_config import TokenUsage
    from matrx_ai.context.app_context import AppContext, clear_app_context, set_app_context
    from matrx_ai.orchestrator.requests import AIMatrixRequest, CompletedRequest

    route("anthropic_chat")
    ctx = AppContext(emitter=None, user_id="u1")
    token = set_app_context(ctx)
    try:
        prep, _ = await _send(_history(), iteration=2)
        request = AIMatrixRequest(
            conversation_id="c1",
            config=UnifiedConfig(model="m-img5", messages=[{"role": "user", "content": "hi"}]),
            usage_history=[
                TokenUsage(input_tokens=10, output_tokens=5, matrx_model_name="m-img5", api="anthropic")
                for _ in range(3)
            ],
        )
        rows = CompletedRequest(request=request, iterations=3, final_response=None).to_storage_dict()["requests"]
    finally:
        clear_app_context(token)
    by_iter = {r["iteration"]: (r.get("metadata") or {}).get("assistant_media_carried") for r in rows}
    assert by_iter == {1: None, 2: prep.carried_media, 3: None}


# ── 3. strict role alternation (T4) ──────────────────────────────────────────


@pytest.mark.asyncio
async def test_a_strict_alternation_model_never_gets_two_user_turns_in_a_row(route) -> None:
    route("groq_chat", _STRICT)
    prep, config = await _send(_history())
    messages = _wire(prep, config)
    roles = [_role(m) for m in messages if _role(m) in ("user", "assistant")]
    assert all(a != b for a, b in zip(roles, roles[1:], strict=False)), roles
    last = messages[-1]
    assert _role(last) == "user" and _images(last) == 1
    # Her words still end the request, and her turn is not relabelled as the host's.
    assert last.content[-1].text == "Describe what you made."
    assert (last.metadata or {}).get("authored_by") != HOST_AUTHORED_BY
    assert prep.carried_media == [{"kind": "image", "at": 1, "file_id": _FILE_ID, "merged": True}]


def test_strict_alternation_after_tool_results_merges_into_the_next_user_turn() -> None:
    from matrx_ai.config.message_config import ToolCallContent, ToolResultContent

    history = [
        UnifiedMessage(role="user", content=[TextContent(text="Draw, then look it up.")]),
        UnifiedMessage(role="assistant", content=[_picture(), ToolCallContent(id="t1", name="search", arguments={})]),
        UnifiedMessage(role="tool", content=[ToolResultContent(tool_use_id="t1", call_id="t1", content="ok")]),
        UnifiedMessage(role="user", content=[TextContent(text="Now?")]),
    ]
    carried = carry_assistant_media(history, "groq_chat", strict_alternation=True)
    assert carried is not None
    assert [_role(m) for m in carried] == ["user", "assistant", "tool", "user"]
    assert _images(carried[3]) == 1 and carried[3].content[-1].text == "Now?"
    assert _images(history[3]) == 0  # the stored turn is untouched


# ── 4. narrow lines (SP4b, SP8, SP12/SP13) ───────────────────────────────────


def test_moonshot_refuses_media_on_an_assistant_turn() -> None:
    assert carry_assistant_media(_history(), "moonshot_chat") is not None


def test_the_carried_turn_is_the_hosts_and_hidden_from_the_person() -> None:
    carried = carry_assistant_media(_history(), "anthropic_chat")
    assert carried is not None
    turn = carried[2]
    assert _role(turn) == "user" and _images(turn) == 1
    assert turn.metadata["authored_by"] == HOST_AUTHORED_BY
    assert turn.metadata["is_visible_to_user"] is False
    assert turn.metadata[CARRIED_MEDIA_KEY] is True


@pytest.mark.parametrize("kind", ["image", "document"])
def test_anthropics_last_layer_names_an_image_or_document_on_an_assistant_turn(kind: str) -> None:
    from matrx_ai.providers.anthropic.translator import _no_media_on_an_assistant_turn

    block = {"type": kind, "source": {"type": "base64", "media_type": "image/png", "data": _PNG}}
    out = _no_media_on_an_assistant_turn([{"type": "text", "text": "Here it is."}, block])
    assert [b["type"] for b in out] == ["text", "text"]
    assert f'kind="{kind}"' in out[1]["text"]
