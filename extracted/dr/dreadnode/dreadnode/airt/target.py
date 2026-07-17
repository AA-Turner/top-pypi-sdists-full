"""AIRT target output contract — unified on the SDK's existing structures.

A red-team *target* (single chat model, custom agent, or multi-agent system)
returns one of the SDK's own, multimodal-ready types — we do **not** invent a
bespoke wrapper, so the same structures used across generators / agents /
evaluations flow straight into AIRT findings, and multimodal probing works for
free.

Accepted target return shapes (all normalized by :func:`extract_response_text`
and :func:`extract_tool_calls`):

- ``str`` — plain text response (back-compat, single chat model).
- :class:`~dreadnode.generators.message.Message` — a single agent turn.
  ``content`` is multimodal (``content_parts`` = text/image/audio/video) and
  ``tool_calls`` are native. **The idiomatic choice for a single-agent target.**
- :class:`~dreadnode.agents.trajectory.Trajectory` or ``list[Message]`` — a full
  or multi-agent run. Tool calls live on assistant messages; tool *results* are
  ``role="tool"`` messages linked by ``tool_call_id``; per-agent attribution is
  read from ``Message.metadata["agent"]``. **The idiomatic choice for a
  multi-agent target.**
- ``dict`` with ``content``/``response`` + ``tool_calls`` (+ optional
  ``agent``/``result`` per call) — for HTTP/custom agent JSON responses.

Example — single-agent target::

    import dreadnode as dn
    from dreadnode.generators.message import Message

    @dn.task
    async def target(prompt: str) -> Message:
        return await my_agent.chat(prompt)  # a Message with content + tool_calls

Example — multi-agent target (per-agent tool attribution)::

    from dreadnode.generators.message import Message

    @dn.task
    async def target(prompt: str) -> list[Message]:
        run = await my_mesh.run(prompt)
        return [
            Message(role="assistant", content=t.text, tool_calls=t.tool_calls,
                    metadata={"agent": t.agent_name})
            for t in run.turns
        ] + [
            Message(role="tool", tool_call_id=r.call_id, content=r.result)
            for r in run.tool_results
        ]
"""

import typing as t

from dreadnode.agents.trajectory import Trajectory
from dreadnode.generators.message import Message

# The full set of shapes an AIRT target may return.
TargetOutput = "str | Message | Trajectory | list[Message] | dict[str, t.Any]"


def _text_of(message: Message) -> str:
    """Best-effort text of a Message (multimodal-safe)."""
    content = getattr(message, "content", None)
    if isinstance(content, str):
        return content
    return str(content) if content is not None else ""


def _messages_of(output: t.Any) -> "list[Message] | None":
    """Return a Message list for Trajectory / list[Message] outputs, else None."""
    if isinstance(output, Trajectory):
        return list(output.messages)
    if isinstance(output, list) and output and all(isinstance(m, Message) for m in output):
        return output
    return None


def extract_response_text(output: t.Any) -> str:
    """Extract the human-readable response text from any accepted target output."""
    if output is None:
        return ""
    if isinstance(output, str):
        return output
    if isinstance(output, Message):
        return _text_of(output)

    messages = _messages_of(output)
    if messages is not None:
        # Last non-empty assistant/text message is the response.
        for msg in reversed(messages):
            if getattr(msg, "role", None) == "tool":
                continue
            text = _text_of(msg)
            if text:
                return text
        return ""

    if isinstance(output, dict):
        for key in ("content", "response", "output", "text"):
            value = output.get(key)
            if isinstance(value, str):
                return value
        return str(output)

    for attr in ("content", "output", "text"):
        value = getattr(output, attr, None)
        if isinstance(value, str):
            return value
    return str(output)


def _tool_call_entry(tc: t.Any, *, agent: str = "", result: str = "") -> "dict[str, t.Any] | None":
    """Normalize one tool call (dict or ToolCall-like) to {name, arguments, agent?, result?}."""
    entry: dict[str, t.Any] = {}
    if isinstance(tc, dict):
        func = tc.get("function")
        if isinstance(func, dict):  # OpenAI-style
            entry["name"] = func.get("name", "")
            entry["arguments"] = func.get("arguments", "")
        else:  # flat dict
            entry["name"] = tc.get("name") or tc.get("tool") or ""
            entry["arguments"] = tc.get("arguments") or tc.get("args") or ""
        agent = tc.get("agent", agent)
        if tc.get("result") is not None:
            result = tc["result"]
    else:  # ToolCall / object
        func = getattr(tc, "function", None)
        if func is not None:
            entry["name"] = getattr(func, "name", "") or ""
            entry["arguments"] = getattr(func, "arguments", "") or ""
        else:
            entry["name"] = getattr(tc, "name", "") or ""
            entry["arguments"] = getattr(tc, "arguments", "") or ""
        agent = getattr(tc, "agent", "") or agent
        if getattr(tc, "result", None) is not None:
            result = tc.result

    if not entry.get("name"):
        return None
    if agent:
        entry["agent"] = agent
    if result != "":
        entry["result"] = result if isinstance(result, str) else str(result)
    return entry


def _tool_call_id(tc: t.Any) -> str:
    if isinstance(tc, dict):
        return str(tc.get("id", ""))
    return str(getattr(tc, "id", "") or "")


def extract_tool_calls(output: t.Any) -> "list[dict[str, t.Any]]":
    """Extract executed tool calls as ``{name, arguments, agent?, result?}`` dicts.

    Works across single-agent (Message), multi-agent (Trajectory / list[Message]
    — pairing ``role='tool'`` results by ``tool_call_id`` and reading
    ``metadata['agent']``), and dict/object outputs.
    """
    messages = _messages_of(output)
    if messages is not None:
        # Map tool_call_id -> result text from role="tool" messages.
        results: dict[str, str] = {}
        for msg in messages:
            if getattr(msg, "role", None) == "tool":
                call_id = str(getattr(msg, "tool_call_id", "") or "")
                if call_id:
                    results[call_id] = _text_of(msg)
        normalized: list[dict[str, t.Any]] = []
        for msg in messages:
            agent = ""
            metadata = getattr(msg, "metadata", None)
            if isinstance(metadata, dict):
                agent = str(metadata.get("agent", "") or "")
            for tc in getattr(msg, "tool_calls", None) or []:
                entry = _tool_call_entry(tc, agent=agent, result=results.get(_tool_call_id(tc), ""))
                if entry:
                    normalized.append(entry)
        return normalized

    if isinstance(output, Message):
        agent = ""
        if isinstance(getattr(output, "metadata", None), dict):
            agent = str(output.metadata.get("agent", "") or "")
        raw = getattr(output, "tool_calls", None) or []
        return [e for tc in raw if (e := _tool_call_entry(tc, agent=agent))]

    if isinstance(output, dict):
        raw = output.get("tool_calls") or []
    elif isinstance(output, list):
        raw = output
    else:
        raw = getattr(output, "tool_calls", None) or []

    return [e for tc in raw if (e := _tool_call_entry(tc))]
