"""A watched Miles agent rollout's turns, read from Miles' own session server (W30 spike M4): `GET {session server}/
sessions/{id}` serves every finished model call of an open session (`rollout/session/sessions.py:142-144`), so Probe
adds nothing to the model path. The session is the one `OpenAIEndpointTracer.create` opens inside the rollout's task
(`agentic_tool_call.py:63`); its wrap ties it to the running try."""

from __future__ import annotations

import asyncio
import functools
import logging
import threading
from collections.abc import Callable, Mapping
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Any

from .engines import CURRENT

if TYPE_CHECKING:
    from .rollout import Rollout

log = logging.getLogger(__name__)

#: How often a watched session is read again.
POLL_SECONDS = 2.0
SESSION_TIMEOUT_S = 5.0
_MARK = "__probe_wrapped__"


def to_turns(answer: Mapping[str, Any]) -> list[dict]:
    """A `GetSessionResponse` (`rollout/session/types.py:48-61`) as the conversation so far: the newest record's request
    messages (they carry the history) and its reply, each a turn (`role`, `content`, `tool_name`, `tokens`, `at`)."""
    records = [record for record in answer.get("records") or () if isinstance(record, Mapping)]
    if not records:
        return []
    last = records[-1]
    request = last.get("request") if isinstance(last.get("request"), Mapping) else {}
    response = last.get("response") if isinstance(last.get("response"), Mapping) else {}
    at = _to_iso(last.get("timestamp"))
    turns = [_to_turn(message, at) for message in request.get("messages") or () if isinstance(message, Mapping)]
    choices = response.get("choices") or [{}]
    reply = choices[0].get("message") if isinstance(choices[0], Mapping) else None
    if isinstance(reply, Mapping):
        turn = _to_turn(reply, at)
        usage = response.get("usage") if isinstance(response.get("usage"), Mapping) else {}
        if isinstance(usage.get("completion_tokens"), int):
            turn["tokens"] = usage["completion_tokens"]
        turns.append(turn)
    return turns


def _to_turn(message: Mapping[str, Any], at: str | None) -> dict:
    content = message.get("content")
    calls = [call for call in message.get("tool_calls") or () if isinstance(call, Mapping)]
    turn: dict[str, Any] = {"role": str(message.get("role") or "assistant"), "content": content if content else calls}
    name = message.get("name")
    if not name and calls and isinstance(calls[0].get("function"), Mapping):
        name = calls[0]["function"].get("name")
    if name:
        turn["tool_name"] = str(name)
    if at:
        turn["at"] = at
    return turn


def _to_iso(value: Any) -> str | None:
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return datetime.fromtimestamp(value, tz=timezone.utc).isoformat()
    return None


class SessionWatcher:
    """One thread for the process, only while a rollout is watched: each pass reads every watched rollout's session
    and sends the turns it has not sent (`log_turns`). ``get_writer()`` is the rollout producer's `run.samples`."""

    def __init__(self, get_writer: Callable[[], Any]) -> None:
        self._get_writer = get_writer
        self._watched: dict[str, tuple[Rollout, int]] = {}
        self._lock = threading.Lock()
        self._read_lock = threading.Lock()
        self._wake = threading.Event()
        self._thread: threading.Thread | None = None

    def watch(self, rollout: Rollout) -> None:
        """Send this rollout's conversation so far, then each new turn, while it is watched."""
        with self._lock:
            self._watched[rollout.key] = (rollout, 0)
            if self._thread is None or not self._thread.is_alive():
                self._thread = threading.Thread(target=self._run, name="probe-miles-sessions", daemon=True)
                self._thread.start()
        self._wake.set()

    def read_last(self, rollout: Rollout) -> None:
        """Read a watched rollout's session once more before Miles collects it (its last turns), on the caller's
        thread."""
        if self.is_watching(rollout.key):
            self._read_one(rollout)

    def is_watching(self, key: str) -> bool:
        with self._lock:
            return key in self._watched

    def _run(self) -> None:
        while True:
            with self._lock:
                if not self._watched:
                    self._thread = None
                    return
                watched = [rollout for rollout, _sent in self._watched.values()]
            for rollout in watched:
                self._read_one(rollout)
            self._wake.wait(POLL_SECONDS)
            self._wake.clear()

    def _read_one(self, rollout: Rollout) -> None:
        """One read and its new turns, one at a time (the poll and the last read before collect never send a turn
        twice)."""
        with self._read_lock:
            self._read_and_send(rollout)

    def _read_and_send(self, rollout: Rollout) -> None:
        writer = self._get_writer()
        with self._lock:
            found = self._watched.get(rollout.key)
        if found is None:
            return
        if writer is None or rollout.is_ended or not writer.is_watched(rollout.key):
            with self._lock:
                self._watched.pop(rollout.key, None)
            return
        if not rollout.session_url or not rollout.session_id:
            return  # its session is not open yet
        sent = found[1]
        try:
            import httpx

            from probe.foundation.tls.tls import ssl_context

            answer = httpx.get(f"{rollout.session_url}/sessions/{rollout.session_id}", timeout=SESSION_TIMEOUT_S,
                               verify=ssl_context())
            answer.raise_for_status()
            turns = to_turns(answer.json())
        except Exception as exc:  # noqa: BLE001 -- the session closed, or its server is busy: the next pass tries again
            log.debug("probe: Miles session %s of sample %s could not be read: %s", rollout.session_id, rollout.key, exc)
            return
        new = turns[sent:] if len(turns) >= sent else turns  # a shorter conversation (compacted): send it whole
        if new:
            writer.log_turns(rollout.key, new)
        with self._lock:
            if rollout.key in self._watched:
                self._watched[rollout.key] = (rollout, len(turns))


def wrap_endpoint_tracer(module: Any, on_session: Callable[[Rollout, Any], None], watcher: SessionWatcher) -> None:
    """`OpenAIEndpointTracer` (`generate_utils/openai_endpoint_utils.py:29-130`), once: the session `create` opens is
    the running try's (``on_session(rollout, tracer)``), and a watched one is read once more before `collect_samples`
    takes it (the agent's last turns land then)."""
    cls = getattr(module, "OpenAIEndpointTracer", None)
    _wrap_collect(cls, watcher)
    found = getattr(cls, "__dict__", {}).get("create")
    original = found.__func__ if isinstance(found, staticmethod) else found
    if not callable(original) or getattr(original, _MARK, False):
        return

    @functools.wraps(original)
    async def create(*args: Any, **kwargs: Any) -> Any:
        tracer = await original(*args, **kwargs)
        rollout = CURRENT.get()
        if rollout is not None:
            try:
                on_session(rollout, tracer)
            except Exception as exc:  # noqa: BLE001 -- a watch is never worth a rollout
                log.debug("probe: a Miles session note failed: %s", exc)
        return tracer

    setattr(create, _MARK, True)
    cls.create = staticmethod(create)


def _wrap_collect(cls: Any, watcher: SessionWatcher) -> None:
    original = getattr(cls, "collect_samples", None)
    if not callable(original) or getattr(original, _MARK, False):
        return

    @functools.wraps(original)
    async def collect_samples(self: Any, *args: Any, **kwargs: Any) -> Any:
        rollout = CURRENT.get()
        if rollout is not None and watcher.is_watching(rollout.key):
            try:
                await asyncio.to_thread(watcher.read_last, rollout)
            except Exception as exc:  # noqa: BLE001 -- a watch is never worth a rollout
                log.debug("probe: the last read of a Miles session failed: %s", exc)
        return await original(self, *args, **kwargs)

    setattr(collect_samples, _MARK, True)
    cls.collect_samples = collect_samples
