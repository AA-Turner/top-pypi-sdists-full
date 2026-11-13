"""verl's `ToolAgentLoop` (`experimental/agent_loop/tool_agent_loop.py`, pinned `b17218ba58a6`) wrapped on the class
as its module loads: `_handle_pending_state` hands the loop's `AgentData` to the recording, `_handle_generating_state`
keeps each model call (and re-parses a reply the loop ended before parsing, F4), `_call_tool` times each call and
decides whether it worked (`tool_runs.py`). Fail open: a wrap that cannot record runs verl's method as it is."""

from __future__ import annotations

import functools
import logging
import time
from typing import Any

from ..wrapping import guard, is_wrapped, make_install, set_wrapped
from .recording import ModelTurn, get_recording
from .tool_runs import get_tool_outcome

logger = logging.getLogger(__name__)

TOOL_LOOP_MODULE = "verl.experimental.agent_loop.tool_agent_loop"
TOOL_LOOP_CLASS = "ToolAgentLoop"
PENDING = "_handle_pending_state"
GENERATING = "_handle_generating_state"
CALL_TOOL = "_call_tool"

_HAS_WARNED = False


def wrap_tool_agent_loop(cls: type) -> bool:
    """The three methods on ``cls`` (the class that defines them), once; all or none."""
    originals = {name: cls.__dict__.get(name) for name in (PENDING, GENERATING, CALL_TOOL)}
    if not all(callable(method) for method in originals.values()):
        return False
    if any(is_wrapped(method) for method in originals.values()):
        return False
    for name, make in ((PENDING, _wrap_pending), (GENERATING, _wrap_generating), (CALL_TOOL, _wrap_call_tool)):
        set_wrapped(cls, name, functools.wraps(originals[name])(make(originals[name])))
    return True


def _wrap_pending(original: Any) -> Any:
    async def _handle_pending_state(self: Any, agent_data: Any, *args: Any, **kwargs: Any) -> Any:
        recording = get_recording()
        if recording is not None:
            guard(recording.start, self, agent_data)
        return await original(self, agent_data, *args, **kwargs)

    return _handle_pending_state


def _wrap_generating(original: Any) -> Any:
    async def _handle_generating_state(self: Any, agent_data: Any, *args: Any, **kwargs: Any) -> Any:
        recording = get_recording()
        if recording is None or recording.agent_data is not agent_data:
            return await original(self, agent_data, *args, **kwargs)
        try:
            messages_before = len(agent_data.messages)
            mask_before = len(agent_data.response_mask)
        except Exception as exc:  # noqa: BLE001 -- an `AgentData` without them: verl's method runs unrecorded
            _warn_unreadable(exc)
            return await original(self, agent_data, *args, **kwargs)
        recording.take_dropped()
        state = await original(self, agent_data, *args, **kwargs)
        try:
            await _keep_turn(recording, self, agent_data, messages_before, mask_before)
        except Exception as exc:  # noqa: BLE001 -- fail open: the loop runs on, this turn is not recorded
            logger.debug("probe: a verl model turn was not recorded (%s: %s)", type(exc).__name__, exc)
        return state

    return _handle_generating_state


def _warn_unreadable(exc: Exception) -> None:
    global _HAS_WARNED
    if not _HAS_WARNED:
        _HAS_WARNED = True
        logger.warning("Probe could not read verl's AgentData (%s: %s); its model turns are not recorded as messages",
                       type(exc).__name__, exc)


async def _keep_turn(recording: Any, loop: Any, agent_data: Any, messages_before: int, mask_before: int) -> None:
    """One model call: the message verl appended with the calls it parsed, or, when the loop ended before parsing
    (`tool_agent_loop.py:291-296`: past `response_length`, or a turn cap), the reply re-parsed by the loop's own tool
    parser from the tokens the loop kept (the output is cut at `response_length`, `:197-198`)."""
    ids = [int(token) for token in agent_data.response_ids]
    limit = int(loop.max_parallel_calls) if getattr(loop, "max_parallel_calls", None) else None
    appended = agent_data.messages[messages_before] if len(agent_data.messages) > messages_before else None
    if appended is not None:
        calls = list(agent_data.tool_calls or [])[:limit]
        recording.turns.append(ModelTurn(ids, ids, appended, calls, recording.take_dropped()))
        return
    budget = max(0, int(loop.response_length) - mask_before)
    trained = ids[:budget]
    active = getattr(agent_data, "_active_tools", loop.tools)
    content, calls = await loop.tool_parser.extract_tool_calls(trained, [tool.tool_schema for tool in active.values()])
    recording.turns.append(ModelTurn(ids, trained, None, list(calls or [])[:limit], recording.take_dropped(),
                                     content=content or ""))


def _wrap_call_tool(original: Any) -> Any:
    async def _call_tool(self: Any, tool_call: Any, tools_kwargs: Any, agent_data: Any, *args: Any,
                         **kwargs: Any) -> Any:
        recording = get_recording()
        if recording is None or recording.agent_data is not agent_data:
            return await original(self, tool_call, tools_kwargs, agent_data, *args, **kwargs)
        call_id = guard(recording.get_call_id, tool_call)
        started = time.perf_counter()
        try:
            result = await original(self, tool_call, tools_kwargs, agent_data, *args, **kwargs)
        except BaseException as exc:
            guard(_record, recording, call_id, tool_call, False, time.perf_counter() - started,
                  f"{type(exc).__name__}: {exc}")
            raise
        response = result[0] if isinstance(result, tuple) and result else None
        outcome = guard(get_tool_outcome, tool_call, getattr(agent_data, "_active_tools", self.tools), response)
        if outcome is not None:
            guard(_record, recording, call_id, tool_call, outcome.is_ok, time.perf_counter() - started, outcome.error)
        return result

    return _call_tool


def _record(recording: Any, call_id: str | None, tool_call: Any, is_ok: bool | None, seconds: float,
            error: str | None) -> None:
    recording.capture.record_tool_run(call_id, str(getattr(tool_call, "name", "")), is_ok=is_ok,
                                      duration_s=max(0.0, seconds), error=error)


install = make_install(TOOL_LOOP_CLASS, wrap_tool_agent_loop)
