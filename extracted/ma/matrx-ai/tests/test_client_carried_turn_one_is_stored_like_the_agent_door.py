"""A client-carried door's turn 1 is stored exactly like the agent door's (PB-03, 2026-10-16).

The Builder's Test run (``/ai/manual``) sends the authored template and the typed turn as two
messages. Only the trigger (the typed one) was persisted, so turn 2 reloaded a history without
the filled "Order name: …" message and the agent answered NOT PROVIDED. The agent door stores ONE
user message: template block(s) + typed block, ``user_content`` = only the typed words.
"""

from __future__ import annotations

from matrx_ai.config.message_config import MessageList, TextContent, UnifiedMessage
from matrx_ai.config.template_substitution import (
    authored_template_messages,
    fold_typed_turn_into_template,
)
from matrx_ai.config.unified_config import UnifiedConfig

V = {"order_name": "Benedita Raposo"}
WIRE = [
    {"role": "system", "content": "You keep the cake card."},
    {"role": "user", "content": "Order name: {{order_name}}"},
    {"role": "user", "content": "Two-tier cake, pickup Saturday."},
]


def _turn_one(wire: list[dict], count: int) -> UnifiedConfig:
    """chat_run's own steps for a stored first turn: build, select, fill, fold."""
    config = UnifiedConfig.from_dict({"model": "m", "messages": wire}, authored_message_count=count)
    template = authored_template_messages(wire, count, config.messages)
    config.replace_variables(V, template_messages=template)
    fold_typed_turn_into_template(config.messages, template)
    return config


def _agent_door_shape() -> dict:
    messages = MessageList(_messages=[UnifiedMessage(role="user", content=[TextContent(text="Order name: Benedita Raposo")])])
    messages.append_or_extend_user_text("Two-tier cake, pickup Saturday.", own_block=True)
    return messages[0].to_storage_dict()


def test_turn_one_stores_the_filled_template_with_the_typed_turn() -> None:
    stored = _turn_one(WIRE, 2).to_storage_dict()["messages"]
    assert len(stored) == 1, "the typed turn must join the template; alone, only it is persisted"
    assert [b["text"] for b in stored[0]["content"]] == ["Order name: Benedita Raposo", "Two-tier cake, pickup Saturday."]
    assert stored[0]["user_content"] == [{"type": "text", "text": "Two-tier cake, pickup Saturday."}]


def test_the_stored_turn_equals_the_agent_doors() -> None:
    stored = _turn_one(WIRE, 2).to_storage_dict()["messages"][0]
    door = _agent_door_shape()
    assert stored["content"] == door["content"]
    assert stored["user_content"] == door["user_content"]


def test_typed_text_is_never_filled_by_the_fold() -> None:
    wire = [*WIRE[:2], {"role": "user", "content": "quote {{order_name}}"}]
    stored = _turn_one(wire, 2).to_storage_dict()["messages"][0]
    assert stored["content"][-1]["text"] == "quote {{order_name}}"


def test_nothing_folds_when_the_template_ends_on_an_assistant_turn_or_history_follows() -> None:
    assistant_last = [WIRE[0], {"role": "user", "content": "U {{order_name}}"}, {"role": "assistant", "content": "A"},
                      {"role": "user", "content": "typed"}]
    assert len(_turn_one(assistant_last, 3).messages) == 3
    history_between = [*WIRE[:2], {"role": "assistant", "content": "prev"}, {"role": "user", "content": "typed"}]
    assert len(_turn_one(history_between, 2).messages) == 3
    assert len(_turn_one(WIRE, 0).messages) == 3  # system stays history, nothing authored
