"""A HOST NOTE DRAINED AT THE START OF HER TURN rides BEFORE her typed text, never after it.

Live guard ``scripts/check_request_ends_with_typed_text.py`` on v0.2.2539 (system_error 599b42da,
2026-11-18): an anthropic send ended ``The person APPROVED and applied your proposed change (...)``.
The Studio's proposal decision (``workflow_conductor/proposals.decision_note``) is queued for the
conversation's Turn-Boundary Inbox; the first boundary of her next turn drains it
(``dynamic_drain.drain_pending_injections``) and APPENDS it as a host turn after her message, so the
request ended with the server's words. Every inbox host note (a helper's report, a wake, agent mail)
drained there had the same order. The send boundary now places a host note that directly follows a
person turn right before her own words (``typed_text_last.notes_before_her_words``), on every send of
the loop alike, so the cached prefix holds.
"""

from __future__ import annotations

from typing import Any

from matrx_ai.config import MessageList, TextContent, UnifiedConfig, UnifiedMessage
from matrx_ai.config.message_config import (
    ToolCallContent,
    ToolResultContent,
    host_authored_user_turn,
)
from matrx_ai.config.send_boundary import order_for_wire
from matrx_ai.config.typed_text_last import typed_text_problem
from matrx_ai.providers.anthropic.translator import AnthropicTranslator
from matrx_ai.testing.profile_factory import make_profile

TYPED = "Now add a step that emails the summary."
NOTE = "The person APPROVED and applied your proposed change (Add step). It is saved in the workflow now."


def _config() -> UnifiedConfig:
    history = [
        UnifiedMessage(role="user", content=[TextContent(text="Build me a workflow.")], id="m1", position=0),
        UnifiedMessage(role="assistant", content=[TextContent(text="Proposed: Add step.")], id="m2", position=1),
    ]
    config = UnifiedConfig(model="m", messages=MessageList(_messages=history))
    config.system_instruction = "You are a careful assistant. " * 40
    config.messages.append_or_extend_user_input(TYPED)
    # What the inbox drain does at the turn's first boundary.
    config.messages.append(host_authored_user_turn(NOTE, reason="injection:system_message"))
    return config


def _send(config: UnifiedConfig) -> dict[str, Any]:
    profile = make_profile(model_name="claude-opus-5-5", wire_format="anthropic_chat")
    prep = order_for_wire(config, profile)
    return AnthropicTranslator().build_request(prep.wire_config if prep.wire_config is not None else config, profile)


def _texts(message: dict[str, Any]) -> list[str]:
    content = message["content"]
    return [content] if isinstance(content, str) else [b.get("text") or "" for b in content if isinstance(b, dict)]


def _strip_marks(messages: list[dict[str, Any]]) -> list[Any]:
    return [
        {**m, "content": [{k: v for k, v in b.items() if k != "cache_control"} for b in m["content"]]}
        if isinstance(m["content"], list)
        else m
        for m in messages
    ]


def test_the_send_ends_with_her_typed_text_and_carries_the_note_before_it() -> None:
    request = _send(_config())
    last = request["messages"][-1]
    assert last["role"] == "user"
    texts = _texts(last)
    assert texts[-1].rstrip().endswith(TYPED), f"the request does not end with her words: {texts[-1][-200:]!r}"
    assert NOTE in "\n".join(texts[:-1]), "the host note was lost"
    assert repr(request["messages"]).count("APPROVED and applied") == 1


def test_the_ledger_is_never_reordered() -> None:
    config = _config()
    _send(config)
    assert config.messages[-1].metadata.get("authored_by") == "host"


def test_the_next_send_of_the_loop_keeps_the_same_prefix() -> None:
    config = _config()
    first = _send(config)
    turn_len = len(first["messages"])
    config.messages.append(
        UnifiedMessage(role="assistant", content=[ToolCallContent(id="c1", name="memory", arguments={"q": "x"})])
    )
    config.messages.append(
        UnifiedMessage(role="tool", content=[ToolResultContent(tool_use_id="c1", call_id="c1", name="memory", content="done")])
    )
    second = _send(config)
    assert _strip_marks(second["messages"][:turn_len]) == _strip_marks(first["messages"])


def test_the_in_process_guard_names_a_note_riding_after_her_words() -> None:
    config = _config()
    problem = typed_text_problem(list(config.messages))
    assert problem is not None and "APPROVED" in problem
