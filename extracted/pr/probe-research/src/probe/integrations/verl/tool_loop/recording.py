"""One verl agent loop's recording: its `RolloutCapture` (ambient, so its tools' `probe.samples.attach_*` find it),
the `ToolAgentLoop` and `AgentData` it ran on, and per model call the ids, the message the loop appended, the parsed
calls and the blocks the parser dropped. At the loop's end it builds the messages as the loop built them (ids D3,
arguments F2, reasoning F3, dropped calls F1, the cut reply F4) and exports the capture as one stamp."""

from __future__ import annotations

import contextvars
import json
import logging
from collections.abc import Iterator, Mapping, MutableMapping
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import Any

from .executor import run_in_executor
from .reasoning import split_reasoning
from .stamps import FILES_FIELD, FINISH_FIELD, HANDLE_FIELD, read_stamp, to_stamp

logger = logging.getLogger(__name__)

#: The finish reason a loop that ran past `response_length` reads (F4).
LENGTH = "length"
#: The error of a call in a reply the loop ended before running (past `response_length`, or a turn cap; F4).
NOT_RUN_ERROR = "the loop ended before running it"
_RECORDING: contextvars.ContextVar[LoopRecording | None] = contextvars.ContextVar("probe_verl_tool_loop", default=None)


def get_recording() -> LoopRecording | None:
    """The agent loop this code runs in (live.py opened it), else None."""
    return _RECORDING.get()


@dataclass
class ModelTurn:
    """One model call of a tool loop: its ids (``trained_ids``: the part the loop kept, F4), the assistant message the
    loop appended (None when it ended before parsing: a length cut or a turn cap), the calls as parsed
    (`FunctionCall`s, F2), the blocks the parser dropped (F1), and for a reply the loop never appended its content."""

    response_ids: list[int]
    trained_ids: list[int]
    message: Mapping[str, Any] | None
    calls: list[Any] = field(default_factory=list)
    dropped: list[str] = field(default_factory=list)
    content: str = ""


class LoopRecording:
    """One agent loop's capture and what its `ToolAgentLoop` did. Its wraps (`tool_loop.py`, `parser.py`) write here;
    `finish` turns it into the loop's stamp."""

    def __init__(self, capture: Any) -> None:
        self.capture = capture
        self.loop: Any = None
        self.agent_data: Any = None
        self.turns: list[ModelTurn] = []
        self.is_cut = False
        self._dropped: list[str] = []

    @contextmanager
    def enter(self) -> Iterator[LoopRecording]:
        """The recording and its capture as this loop's ambient context: the tasks it starts (`asyncio.gather` of its
        tools) inherit both."""
        token = _RECORDING.set(self)
        try:
            with self.capture:
                yield self
        finally:
            _RECORDING.reset(token)

    # -- what the wraps keep ---------------------------------------------------------------------------
    def start(self, loop: Any, agent_data: Any) -> None:
        """`ToolAgentLoop._handle_pending_state` ran: the loop and its `AgentData` (local to `run`)."""
        if self.agent_data is None:
            self.loop, self.agent_data = loop, agent_data

    def keep_dropped(self, blocks: list[str]) -> None:
        self._dropped.extend(blocks)

    def take_dropped(self) -> list[str]:
        dropped, self._dropped = self._dropped, []
        return dropped

    def get_call_id(self, tool_call: Any) -> str:
        """The id of a call the loop is running: the framework's, else `probe-<assistant turn>-<i>` (D3), the turn
        being the newest assistant message (verl appends it before it runs the calls) and ``i`` the call's place."""
        named = getattr(tool_call, "tool_call_id", None)
        if isinstance(named, str) and named:
            return named
        messages = getattr(self.agent_data, "messages", None) or []
        turn = sum(1 for message in messages if _is_assistant(message)) - 1
        calls = list(getattr(self.agent_data, "tool_calls", None) or [])
        index = next((place for place, call in enumerate(calls) if call is tool_call), len(calls))
        return f"probe-{max(turn, 0)}-{index}"

    # -- the loop's end ------------------------------------------------------------------------------
    def stamp_handle(self, worker: Any, outputs: Any) -> None:
        """Before verl scores the loop: when a reward loop worker will (`agent_loop.py:1057-1116`), its last output
        carries the handle, which reaches the worker as `tool_extra_fields` (D11)."""
        if not outputs or getattr(worker, "reward_loop_worker_handles", None) is None:
            return
        final = outputs[-1]
        extra = getattr(final, "extra_fields", None)
        if getattr(final, "reward_score", None) is None and isinstance(extra, MutableMapping):
            extra[HANDLE_FIELD] = json.dumps(self.capture.to_handle())

    async def finish(self, outputs: Any) -> str:
        """After verl scored the loop: the reward worker's files joined, the messages set, the capture exported (on
        Probe's own threads: it waits for uploads). The stamp, `""` for nothing."""
        self._take_reward_files(outputs)
        if self.agent_data is not None:
            turns, failed = await run_in_executor(self._build_turns)
            self.capture.set_turns(turns)
            for call_id, name, error in failed:
                self.capture.record_tool_run(call_id, name, is_ok=False, error=error)
        payload = await run_in_executor(self.capture.export)
        if self._is_past_length():
            payload[FINISH_FIELD] = LENGTH
        return to_stamp(payload)

    def _take_reward_files(self, outputs: Any) -> None:
        final = outputs[-1] if outputs else None
        extra = getattr(final, "extra_fields", None)
        if not isinstance(extra, MutableMapping):
            return
        extra.pop(HANDLE_FIELD, None)
        info = extra.get("reward_extra_info")
        found = read_stamp(info.pop(FILES_FIELD, None)) if isinstance(info, MutableMapping) else None
        if found:
            self.capture.add_files(found.get("files") or [], failed=int(found.get("failed") or 0))

    def _is_past_length(self) -> bool:
        """F4: verl's own cut, `len(response_mask) >= response_length` (`tool_agent_loop.py:292`); the server says
        `completed` either way."""
        limit = getattr(self.loop, "response_length", None)
        mask = getattr(self.agent_data, "response_mask", None)
        return isinstance(limit, int) and mask is not None and len(mask) >= limit

    def _build_turns(self) -> tuple[list[dict], list[tuple[str, str, str]]]:
        """The sample's turns from the messages as the loop built them, plus the calls that never ran, each recorded
        failed as (id, name, error): the ones the parser dropped (F1), and the ones in a reply the loop ended before
        running (F4)."""
        from probe.sdk.run.samples.rollout import build_turns

        from .parser import DROPPED_ERROR

        replies = {id(turn.message): turn for turn in self.turns if turn.message is not None}
        messages: list[Any] = []
        dropped: list[tuple[int, str, str]] = []
        turn_index = 0
        for message in list(getattr(self.agent_data, "messages", None) or []):
            reply = replies.get(id(message)) if _is_assistant(message) else None
            if reply is not None:
                messages.append(self._to_assistant(message.get("content"), reply, turn_index, dropped))
            else:
                messages.append(message)
            turn_index += _is_assistant(message)
        failed: list[tuple[str, str, str]] = []
        for reply in self.turns:
            if reply.message is None:  # ended before the loop parsed it: never in `messages`, its calls never ran
                message = self._to_assistant(reply.content, reply, turn_index, dropped)
                messages.append(message)
                failed += [(call["id"], call["function"]["name"], NOT_RUN_ERROR) for call in message.get("tool_calls", [])]
                turn_index += 1
        turns = build_turns(messages, should_number_ids=True)
        for place, call_id, block in dropped:
            if place < len(turns) and turns[place]["messages"] and _is_assistant(turns[place]["messages"][-1]):
                turns[place]["messages"][-1].setdefault("tool_calls", []).append(
                    {"id": call_id, "name": "", "arguments": block})
                turns[place].setdefault("tool_calls", []).append({"id": call_id, "name": ""})
                failed.append((call_id, "", DROPPED_ERROR))
        return turns, failed

    def _to_assistant(self, content: Any, reply: ModelTurn, turn: int, dropped: list) -> dict:
        text = content if isinstance(content, str) else ("" if content is None else str(content))
        text, reasoning = split_reasoning(text, reply.trained_ids, getattr(self.loop, "tokenizer", None))
        calls = []
        for index, call in enumerate(reply.calls):
            named = getattr(call, "tool_call_id", None)
            calls.append({"id": named if isinstance(named, str) and named else f"probe-{turn}-{index}",
                          "type": "function", "function": {"name": str(getattr(call, "name", "")),
                                                           "arguments": _as_text(getattr(call, "arguments", ""))}})
        dropped += [(turn, f"probe-{turn}-{len(calls) + place}", block) for place, block in enumerate(reply.dropped)]
        message: dict[str, Any] = {"role": "assistant", "content": text}
        if reasoning is not None:
            message["reasoning"] = reasoning
        if calls:
            message["tool_calls"] = calls
        return message


def _is_assistant(message: Any) -> bool:
    return isinstance(message, Mapping) and message.get("role") == "assistant"


def _as_text(value: Any) -> str:
    if isinstance(value, str):
        return value
    return "" if value is None else json.dumps(value, ensure_ascii=False, default=str)
