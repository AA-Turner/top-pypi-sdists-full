"""OpenAI-shaped chat messages (what verl, ART, TRL and Miles hold) as sample turns: each assistant tool call with its
id, name and arguments, each tool result linked by `tool_call_id`, reasoning apart from content."""

from __future__ import annotations

import json
from collections.abc import Iterable, Mapping
from typing import Any

#: Chat role -> `MessageSource`. Gym observations arrive as `user` (DESIGN.md "Turns as sent").
SOURCES = {"system": "system", "user": "user", "assistant": "model", "tool": "tool", "function": "tool"}
#: Where engines and parsers put the model's reasoning apart from its content (vLLM/SGLang, OpenAI, Anthropic-style).
REASONING_KEYS = ("reasoning_content", "reasoning", "thinking")


def build_turns(messages: Iterable[Any], *, should_number_ids: bool = False) -> list[dict]:
    """``messages`` (dicts or objects with OpenAI's fields) as turns: one turn per assistant reply, holding the
    messages since the last reply; trailing messages are a last turn. Each turn's `tool_calls` names every call its
    reply asked for (id + name; the run's stats come from `RolloutCapture.record_tool_run`).

    ``should_number_ids``: for a framework that gives no call id but appends results in call order (verl): a call
    with none gets `probe-<turn>-<i>`, and the i-th following tool message without a `tool_call_id` links to it."""
    turns: list[dict] = []
    current: list[dict] = []
    pending: list[str] = []
    for item in messages:
        message = to_message(item)
        if message is None:
            continue
        if message["role"] == "tool" and "tool_call_id" not in message and should_number_ids and pending:
            message["tool_call_id"] = pending.pop(0)
        current.append(message)
        if message["role"] != "assistant":
            continue
        calls = message.get("tool_calls") or []
        if should_number_ids:
            for index, call in enumerate(calls):
                call.setdefault("id", f"probe-{len(turns)}-{index}")
        pending = [call["id"] for call in calls if call.get("id")] if should_number_ids else []
        turns.append({"messages": current, "tool_calls": [{"id": call["id"], "name": call["name"]}
                                                          if call.get("id") else {"name": call["name"]}
                                                          for call in calls]})  # fmt: skip
        current = []
    if current:
        turns.append({"messages": current, "tool_calls": []})
    return [turn if turn["tool_calls"] else {"messages": turn["messages"]} for turn in turns]


def to_message(item: Any) -> dict | None:
    """One message in the contract's shape (`Message`), or None for something that is not one."""
    role = _get(item, "role")
    if not isinstance(role, str) or not role:
        return None
    message: dict[str, Any] = {"role": role, "source": SOURCES.get(role, "environment"),
                               "content": get_text(_get(item, "content"))}  # fmt: skip
    if role == "assistant":
        message["is_trainable"] = True
    for name in ("name", "tool_call_id"):
        value = _get(item, name)
        if isinstance(value, str) and value:
            message[name] = value
    reasoning = next((value for key in REASONING_KEYS if isinstance(value := _get(item, key), str) and value), None)
    if reasoning is not None:
        message["reasoning"] = reasoning
    calls = [call for call in (to_tool_call(raw) for raw in _get(item, "tool_calls") or ()) if call is not None]
    if calls:
        message["tool_calls"] = calls
    return message


def to_tool_call(item: Any) -> dict | None:
    """One OpenAI tool call (`{id, type, function: {name, arguments}}`, or flat `{id, name, arguments}`) as a
    `MessageToolCall` (`wire.to_message_tool_call`, the one converter `log()` uses too)."""
    from ..wire import to_message_tool_call

    return to_message_tool_call(item)


def get_text(content: Any) -> str:
    """A message's content as text: a string as is, a list of parts as their texts, anything else as JSON."""
    if content is None:
        return ""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        texts = [str(_get(part, "text")) for part in content if _get(part, "text") is not None]
        if texts:
            return "\n".join(texts)
    return json.dumps(content, default=str, ensure_ascii=False)


def _get(target: Any, name: str) -> Any:
    return target.get(name) if isinstance(target, Mapping) else getattr(target, name, None)
