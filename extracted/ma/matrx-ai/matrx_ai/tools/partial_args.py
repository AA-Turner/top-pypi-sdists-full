"""Tool-argument stream hook: a tool hears each completed element of its arguments as they stream.

Providers stream a tool call's arguments as JSON text deltas (Anthropic ``input_json_delta``,
OpenAI ``response.function_call_arguments.delta``). A tool that wants to act before the call
finishes — the workflow author showing proposed steps while the model is still writing them —
registers here for the array paths it cares about (``nodes_upsert``, or ``definition.nodes`` —
paths are dotted through objects from the root) and the scalars it needs to interpret them
(``workflow_id``, ``numbering``):

    register_partial_args("workflow_author", PartialArgsSpec(arrays=("nodes_upsert",),
                          scalars=("workflow_id",)), factory)

``factory(call)`` builds one listener per tool call; the listener hears ``element(path, value)``
once per completed array element (``path`` = ``"nodes_upsert[*]"``), ``scalar(key, value)``
once per completed watched scalar, and ``close(completed=...)`` once when the arguments end
(``completed=False``: the stream stopped mid-call).

This is not a prompt mutation and never touches the send boundary: it only READS the deltas the
provider already streams. A listener failure costs the listener, never the stream — it is logged
loudly and that listener is dropped. A tool with no registration costs nothing (no buffering).
Per-stream state is keyed by the stream's emitter (``reasoning_stream_state`` rule: a provider
client is shared process-wide, so nothing lives on the parser instance).
"""

from __future__ import annotations

import json
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any, Protocol
from weakref import WeakKeyDictionary

from matrx_utils import vcprint


class PartialArgsListener(Protocol):
    async def element(self, path: str, value: Any) -> None: ...

    async def scalar(self, key: str, value: Any) -> None: ...

    async def close(self, *, completed: bool) -> None: ...


@dataclass(frozen=True)
class PartialArgsSpec:
    arrays: tuple[str, ...] = ()
    scalars: tuple[str, ...] = ()


@dataclass(frozen=True)
class PartialToolCall:
    tool_name: str
    call_id: str
    emitter: Any


ListenerFactory = Callable[[PartialToolCall], PartialArgsListener | None]

_REGISTRY: dict[str, tuple[PartialArgsSpec, ListenerFactory]] = {}


def register_partial_args(tool_name: str, spec: PartialArgsSpec, factory: ListenerFactory) -> None:
    """Register (or replace) the one partial-argument listener factory for ``tool_name``."""
    _REGISTRY[tool_name] = (spec, factory)


def unregister_partial_args(tool_name: str) -> None:
    _REGISTRY.pop(tool_name, None)


# Tools whose WHOLE input is announced to the client the moment the model finishes writing it
# (``tool_started`` with ``args_ready``), before the reply ends and the call is dispatched. A page
# edit (``apply_surface_write``) is one: the person sees each edit as the model writes it, not all
# of them together when the reply is over. Announcing changes nothing about dispatch: the call is
# still authorised, recorded and delegated in ``handle_tool_calls``, and answered only then.
_READY_TOOLS: set[str] = {"apply_surface_write"}


def announce_ready_args(tool_name: str) -> None:
    """Announce ``tool_name``'s whole input to the client as soon as the model finishes writing it."""
    _READY_TOOLS.add(tool_name)


class _NoListener:
    async def element(self, path: str, value: Any) -> None:
        return None

    async def scalar(self, key: str, value: Any) -> None:
        return None

    async def close(self, *, completed: bool) -> None:
        return None


async def _announce_ready(emitter: Any, call: PartialToolCall, text: str) -> None:
    """The call's input is whole: hand it to the client now. A failure costs the early look, never the stream."""
    try:
        arguments = json.loads(text)
        if not isinstance(arguments, dict):
            return
        await emitter.send_tool_event(
            {
                "event": "tool_started",
                "call_id": call.call_id,
                "tool_name": call.tool_name,
                "message": "Ready",
                "data": {"arguments": arguments, "args_ready": True},
            }
        )
    except Exception as exc:  # noqa: BLE001 — an announcement never breaks the stream
        vcprint(f"[PARTIAL ARGS] could not announce the finished input of {call.tool_name}: {exc!r}", color="red")


def has_partial_args(tool_name: str) -> bool:
    return tool_name in _REGISTRY


class _Frame:
    """One open container: ``path`` is its dotted address from the root (None inside an array that
    nobody watches), ``key`` the object key whose value comes next, ``watched`` = its elements are
    reported, ``elem_start`` = where the current element began."""

    __slots__ = ("is_obj", "path", "key", "expect_key", "watched", "elem_start")

    def __init__(self, is_obj: bool, path: str | None, watched: bool = False) -> None:
        self.is_obj = is_obj
        self.path = path
        self.key: str | None = None
        self.expect_key = is_obj
        self.watched = watched
        self.elem_start: int | None = None


def _join(path: str | None, key: str | None) -> str | None:
    if path is None or key is None:
        return None
    return key if path == "" else f"{path}.{key}"


class _Scanner:
    """Incremental scanner over a streaming JSON object: reports completed scalars and completed
    elements of watched arrays, each addressed by its dotted path from the root through objects
    (``workflow_id``, ``definition.nodes``). One pass over the text, O(length)."""

    def __init__(self, spec: PartialArgsSpec) -> None:
        self.spec = spec
        self.text = ""
        self.stack: list[_Frame] = []
        self.in_str = False
        self.esc = False
        self.str_start = 0
        self.str_is_key = False
        self.bare_start: int | None = None  # a number / true / false / null in progress

    def feed(self, chunk: str) -> list[tuple[str, str, Any]]:
        out: list[tuple[str, str, Any]] = []
        base = len(self.text)
        self.text += chunk
        for offset, ch in enumerate(chunk):
            i = base + offset
            if self.in_str:
                if self.esc:
                    self.esc = False
                elif ch == "\\":
                    self.esc = True
                elif ch == '"':
                    self.in_str = False
                    if self.str_is_key:
                        top = self.stack[-1]
                        try:
                            top.key = json.loads(self.text[self.str_start : i + 1])
                        except ValueError:
                            top.key = None
                    else:
                        self._value_done(out, self.str_start, i + 1, container=False)
                continue
            if ch in " \t\r\n":
                continue
            if self.bare_start is not None and ch in ",}]":
                start, self.bare_start = self.bare_start, None
                self._value_done(out, start, i, container=False)
            if ch == '"':
                self.in_str = True
                self.str_start = i
                top = self.stack[-1] if self.stack else None
                self.str_is_key = top is not None and top.is_obj and top.expect_key
                if not self.str_is_key:
                    self._value_begins(i)
            elif ch in "{[":
                top = self.stack[-1] if self.stack else None
                self._value_begins(i)
                if top is None:
                    path: str | None = ""
                elif top.is_obj:
                    path = _join(top.path, top.key)
                else:
                    path = None
                self.stack.append(_Frame(ch == "{", path, watched=ch == "[" and path in self.spec.arrays))
            elif ch in "}]":
                frame = self.stack.pop() if self.stack else None
                if frame is not None and self.stack:
                    self._value_done(out, None, i + 1, container=True)
            elif ch == ":":
                if self.stack and self.stack[-1].is_obj:
                    self.stack[-1].expect_key = False
            elif ch == ",":
                if self.stack and self.stack[-1].is_obj:
                    self.stack[-1].expect_key = True
            elif self.bare_start is None and self.stack:
                self.bare_start = i
                self._value_begins(i)
        return out

    def _value_begins(self, i: int) -> None:
        top = self.stack[-1] if self.stack else None
        if top is not None and top.watched and top.elem_start is None:
            top.elem_start = i

    def _value_done(self, out: list[tuple[str, str, Any]], start: int | None, end: int, *, container: bool) -> None:
        top = self.stack[-1] if self.stack else None
        if top is None:
            return
        if top.watched:
            begin, top.elem_start = top.elem_start, None
            if begin is not None:
                _decode(out, "element", f"{top.path}[*]", self.text[begin:end])
            return
        if top.is_obj and not container and start is not None:
            name = _join(top.path, top.key)
            if name is not None and name in self.spec.scalars:
                _decode(out, "scalar", name, self.text[start:end])


def _decode(out: list[tuple[str, str, Any]], kind: str, name: str, raw: str) -> None:
    try:
        out.append((kind, name, json.loads(raw)))
    except ValueError:
        return


@dataclass
class _Tracked:
    call: PartialToolCall
    scanner: _Scanner
    listener: PartialArgsListener
    done: bool = False


@dataclass
class _StreamState:
    calls: dict[Any, _Tracked] = field(default_factory=dict)


_STATE: WeakKeyDictionary[Any, _StreamState] = WeakKeyDictionary()
_FALLBACK: dict[int, _StreamState] = {}


def _state_for(emitter: Any) -> _StreamState:
    try:
        state = _STATE.get(emitter)
        if state is None:
            state = _StreamState()
            _STATE[emitter] = state
        return state
    except TypeError:
        return _FALLBACK.setdefault(id(emitter), _StreamState())


def _drop(state: _StreamState, key: Any, exc: BaseException) -> None:
    tracked = state.calls.pop(key, None)
    name = tracked.call.tool_name if tracked else "?"
    vcprint(
        f"[PARTIAL ARGS] listener for {name} failed and was dropped (the tool call is unaffected): {exc!r}",
        color="red",
    )


async def _announce_call(emitter: Any, *, tool_name: str, call_id: str) -> None:
    """Tell the client a tool call has begun. A failure costs the announcement, never the stream."""
    if emitter is None or not tool_name or not call_id:
        return
    try:
        await emitter.send_tool_event(
            {
                "event": "tool_started",
                "call_id": call_id,
                "tool_name": tool_name,
                "message": "Preparing",
                "data": {"arguments": {}},
            }
        )
    except Exception as exc:  # noqa: BLE001 — an announcement never breaks the stream
        vcprint(f"[PARTIAL ARGS] could not announce {tool_name}: {exc!r}", color="red")


async def tool_args_started(emitter: Any, key: Any, *, tool_name: str, call_id: str) -> None:
    """A provider saw a tool call begin. ``key`` is the provider's per-stream index for it.

    A previous call still open under the same key is closed as not completed first.

    Every tool call is announced here, so its card shows while the model is still writing the
    input. The tool executor's own ``tool_started`` follows with the full arguments.
    """
    await _announce_call(emitter, tool_name=tool_name, call_id=call_id)
    if emitter is None or not call_id or (tool_name not in _REGISTRY and tool_name not in _READY_TOOLS):
        return
    state = _state_for(emitter)
    if key in state.calls:
        await tool_args_finished(emitter, key, completed=False)
    call = PartialToolCall(tool_name=tool_name, call_id=call_id, emitter=emitter)
    if tool_name not in _REGISTRY:
        # Only its finished input is wanted: buffer the text, hear nothing along the way.
        state.calls[key] = _Tracked(call=call, scanner=_Scanner(PartialArgsSpec()), listener=_NoListener())
        return
    spec, factory = _REGISTRY[tool_name]
    try:
        listener = factory(call)
    except Exception as exc:  # noqa: BLE001 — a listener never breaks the stream
        vcprint(f"[PARTIAL ARGS] factory for {tool_name} failed: {exc!r}", color="red")
        listener = None
    if listener is None:
        if tool_name not in _READY_TOOLS:
            return
        listener = _NoListener()
    state.calls[key] = _Tracked(call=call, scanner=_Scanner(spec), listener=listener)


async def tool_args_delta(emitter: Any, key: Any, text: str) -> None:
    """A delta of the call's argument JSON."""
    if not text or emitter is None:
        return
    state = _STATE.get(emitter) if _safe_weak(emitter) else _FALLBACK.get(id(emitter))
    if state is None:
        return
    tracked = state.calls.get(key)
    if tracked is None:
        return
    try:
        for kind, name, value in tracked.scanner.feed(text):
            if kind == "element":
                await tracked.listener.element(name, value)
            else:
                await tracked.listener.scalar(name, value)
    except Exception as exc:  # noqa: BLE001
        _drop(state, key, exc)


async def tool_args_finished(emitter: Any, key: Any, *, completed: bool = True) -> None:
    """The call's arguments ended (``completed=False``: the stream stopped mid-call, or what it wrote
    is not one whole JSON object — a cut-off call never runs, so its listener hears it as unfinished)."""
    if emitter is None:
        return
    state = _STATE.get(emitter) if _safe_weak(emitter) else _FALLBACK.get(id(emitter))
    if state is None:
        return
    tracked = state.calls.pop(key, None)
    if tracked is None:
        return
    if completed and not _whole_object(tracked.scanner.text):
        completed = False
    if completed and tracked.call.tool_name in _READY_TOOLS:
        await _announce_ready(emitter, tracked.call, tracked.scanner.text)
    try:
        await tracked.listener.close(completed=completed)
    except Exception as exc:  # noqa: BLE001
        vcprint(f"[PARTIAL ARGS] close for {tracked.call.tool_name} failed: {exc!r}", color="red")


async def tool_args_stream_ended(emitter: Any) -> None:
    """The provider stream ended: every call still open did not complete."""
    if emitter is None:
        return
    state = _STATE.get(emitter) if _safe_weak(emitter) else _FALLBACK.get(id(emitter))
    if state is None:
        return
    for key in list(state.calls):
        await tool_args_finished(emitter, key, completed=False)


def _whole_object(text: str) -> bool:
    try:
        return isinstance(json.loads(text), dict)
    except ValueError:
        return False


def _safe_weak(emitter: Any) -> bool:
    try:
        _STATE.get(emitter)
        return True
    except TypeError:
        return False
