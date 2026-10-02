"""The daemon's own record of what its agents did: one folder per session.

    <state>/probe/daemon/sessions/<sid>/
        worker.log      the worker's log (what the process did, its warnings)
        writer.jsonl    the writer agent's full trace, one JSON object per line
        reader.jsonl    the reader agent's, where it runs
        <agent>.cursor  how far the shipper has uploaded that trace (`shipper.py`)

EVERY LINE STANDS ALONE. Each carries `ts` (UTC), `agent`, `run` (the bite, or
the reader's turn), `trace_id` (`<sid>:<agent>:<run>`) and, for a step inside
the run, its own `span_id` and its `parent_id` -- so a line can be read, or
uploaded and turned into one event (`app/observability/daemon_trace.py`),
without any line before it. The types:

    run_start     a run begins: trigger, conversation, events shown
    instructions  the job description: first in each worker process, then whenever
                  it changes (a `call` names it by `instructions_sha`)
    tools         the tool definitions the model is offered, the same way
    call_start    a model call was sent: its round and context size (so a call
                  still waiting is visible)
    call          the call answered: `input` = what this call ADDS to the
                  conversation (the prompt, tool results, retry prompts -- in
                  full), `output` = the answer (text, thinking, tool calls,
                  usage), latency, dollars. Pydantic AI's own message JSON.
    tool          one tool run: its arguments, duration, outcome and full result
    history_rewritten
                  the conversation's first message changed (a compaction): the
                  new head, summary included
    model_error   a model call that raised: what it was sent, how long it took
    run_end       the run's outcome, as the store closed it

Each model call is logged as its DELTA, never its whole context: a 1M-token
conversation re-sent every round would grow the file quadratically. A tool's
result is in the file twice -- its `tool` line and the next call's `input` --
the price of lines that stand alone.

What is here is exactly what the model gateway was sent and answered -- the
events and tool outputs were scrubbed for secrets before the model saw them
(`store.scrub`, `tools`) -- so this folder holds nothing that did not already
leave the machine. It is the researcher's (0700 / 0600) and is deleted with the
session's store (`worker.sweep_stale`).

Tracing never fails a bite: a write that raises turns the trace off for the
process, logged once. `PROBE_DAEMON_TRACE=off` turns it off; a file stops at
MAX_TRACE_BYTES with one `trace_full` line.
"""

from __future__ import annotations

import hashlib
import json
import logging
import math
import os
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from probe.daemon.store import state_dir, store_path

log = logging.getLogger("probe.daemon")

ENV_TRACE = "PROBE_DAEMON_TRACE"
ENV_TRACE_MAX_MB = "PROBE_DAEMON_TRACE_MAX_MB"
#: A trace file stops growing here (one `trace_full` line says so).
MAX_TRACE_BYTES = 256 * 1024 * 1024
#: How long a session's folder (and store) is kept after its last write: the
#: sweep (`worker.sweep_stale`) and the shipper's orphan drain share it.
KEEP_S = 30 * 86400
WORKER_LOG = "worker.log"
#: Loggers that write one INFO line per HTTP request: the trace has every model call.
NOISY_LOGGERS = ("httpx", "httpx2", "mcp.client.streamable_http")


def sessions_dir() -> Path:
    return state_dir() / "sessions"


def session_dir(session_id: str) -> Path:
    """The session's folder, named as its store is (`store_path`)."""
    return sessions_dir() / store_path(session_id).stem


def enabled() -> bool:
    return os.environ.get(ENV_TRACE, "on").strip().lower() not in ("0", "off", "false", "no")


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


def _max_bytes() -> int:
    try:
        return int(float(os.environ[ENV_TRACE_MAX_MB]) * 1024 * 1024)
    except (KeyError, ValueError):
        return MAX_TRACE_BYTES


def _private_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)
    try:
        os.chmod(path, 0o700)
    except OSError:
        pass


def log_handlers(session_id: str) -> list[logging.Handler]:
    """The worker's log handlers: everything into the session's `worker.log`,
    warnings and worse on stderr too (capture keeps that as `<sid>.log`). A
    folder that cannot be made leaves stderr alone, at every level."""
    stderr = logging.StreamHandler()
    try:
        folder = session_dir(session_id)
        _private_dir(folder)
        into_file = logging.FileHandler(folder / WORKER_LOG, encoding="utf-8")
    except OSError:
        return [stderr]
    stderr.setLevel(logging.WARNING)
    return [into_file, stderr]


def quiet_noisy_loggers() -> None:
    if logging.getLogger().getEffectiveLevel() > logging.DEBUG:
        for name in NOISY_LOGGERS:
            logging.getLogger(name).setLevel(logging.WARNING)


class TraceFile:
    """One agent's trace file for one session. `write` never raises."""

    def __init__(self, session_id: str, agent: str, *, max_bytes: int | None = None) -> None:
        self.session_id = session_id
        self.agent = agent
        self.path = session_dir(session_id) / f"{agent}.jsonl"
        self.max_bytes = _max_bytes() if max_bytes is None else max_bytes
        self.off = not enabled()
        self._size: int | None = None
        #: The run (bite, or reader turn) the next lines belong to (`start_run`).
        self.run: int | None = None
        self._run_facts: tuple[int, float, dict[str, Any]] | None = None
        #: What was last written of what repeats: the job description, the tools.
        self.instructions_sha: str | None = None
        self.tools_sha: str | None = None
        #: The last model call's context: its size, and its first message (a new
        #: first message = the history was rewritten, a compaction's summary).
        #: The message itself is kept to skip re-hashing an unchanged head.
        self.context_messages = 0
        self.head_sha: str | None = None
        self.head_message: Any = None

    def trace_id(self, run: int | None = None) -> str:
        return f"{self.session_id}:{self.agent}:{self.run if run is None else run}"

    def start_run(self, run: int, **facts: Any) -> None:
        """A run begins: later lines belong to it."""
        self.run = run
        self._run_facts = (run, time.monotonic(), facts)
        self.write({"type": "run_start", **facts})

    def end_run(self, run: int, **facts: Any) -> None:
        """The run's end, with how it started (so `run_end` alone tells the run)."""
        started: dict[str, Any] = {}
        latency: dict[str, Any] = {}
        if self._run_facts is not None and self._run_facts[0] == run:
            started = dict(self._run_facts[2])
            latency = {"latency_ms": int((time.monotonic() - self._run_facts[1]) * 1000)}
        self.write({"type": "run_end", "run": run, "trace_id": self.trace_id(run), **started, **latency, **facts})

    def write(self, record: dict[str, Any]) -> None:
        if self.off:
            return
        try:
            ids = {"run": self.run, "trace_id": self.trace_id()}
            line = _encode({"ts": _now(), "agent": self.agent, **ids, **record})
            # A stray surrogate (a file name that is not UTF-8) is escaped, not fatal.
            data = (line + "\n").encode("utf-8", errors="backslashreplace")
            if self._size is None:
                _private_dir(self.path.parent)
                self._size = self.path.stat().st_size if self.path.exists() else 0
            if self._size + len(data) > self.max_bytes:
                data = (json.dumps({"ts": _now(), "agent": self.agent, "type": "trace_full",
                                    "max_bytes": self.max_bytes}) + "\n").encode("utf-8")
                self.off = True
                log.warning("the %s trace reached %s bytes: no more lines this process", self.agent, self.max_bytes)
            fd = os.open(self.path, os.O_WRONLY | os.O_APPEND | os.O_CREAT, 0o600)
            try:
                os.write(fd, data)
            finally:
                os.close(fd)
            self._size += len(data)
        except OSError as exc:  # the folder or the disk: stop for this process
            self.off = True
            log.warning("the %s trace is off for this process: %s: %s", self.agent, type(exc).__name__, exc)
        except Exception as exc:  # noqa: BLE001 -- one line that cannot be written: that line only
            log.warning("a %s trace line was not written: %s: %s", self.agent, type(exc).__name__, exc)


def finite(value: Any) -> Any:
    if isinstance(value, float) and not math.isfinite(value):
        return None
    if isinstance(value, dict):
        return {k: finite(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [finite(v) for v in value]
    return value


def _encode(value: Any) -> str:
    """Strict JSON: a NaN or Infinity (a tool's metrics) becomes null, so every
    line is JSON any reader -- and the upload -- accepts."""
    try:
        return json.dumps(value, default=str, ensure_ascii=False, allow_nan=False)
    except ValueError:
        return json.dumps(finite(value), default=str, ensure_ascii=False, allow_nan=False)


def _dump(message: Any) -> dict[str, Any]:
    """A Pydantic AI message as its own JSON, None fields left out."""
    from pydantic_ai.messages import ModelMessagesTypeAdapter

    return _drop_none(ModelMessagesTypeAdapter.dump_python([message], mode="json")[0])


def _drop_none(value: Any) -> Any:
    if isinstance(value, dict):
        return {k: _drop_none(v) for k, v in value.items() if v is not None and v != {}}
    if isinstance(value, list):
        return [_drop_none(v) for v in value]
    return value


def _sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _tool_defs(params: Any) -> list[dict[str, Any]]:
    defs = [*(getattr(params, "function_tools", None) or []), *(getattr(params, "output_tools", None) or [])]
    return [{"name": d.name, "description": d.description, "parameters": d.parameters_json_schema} for d in defs]


def _ms(since: float) -> int:
    return int((time.monotonic() - since) * 1000)


@dataclass
class Recording:
    """What `agent.TraceRecorder` does: writes a run's model calls and tool runs
    to `trace`. The capability itself lives in `agent.py`, beside the others:
    this module is imported without the `daemon` extra (`probe daemon status`,
    the sweep, the shipper), so it never imports Pydantic AI at load."""

    trace: TraceFile
    rounds: int = 0

    def _span(self, n: int) -> str:
        return f"{self.trace.trace_id()}:r{n}"

    # -- model calls ---------------------------------------------------------
    async def wrap_model_request(self, ctx: Any, *, request_context: Any, handler: Any) -> Any:
        if self.trace.off:
            return await handler(request_context)
        self.rounds += 1
        n = self.rounds
        sent: dict[str, Any] = {}
        self._safely(self._request, request_context, n, sent)
        started = time.monotonic()
        try:
            response = await handler(request_context)
        except Exception as exc:
            self.trace.write({"type": "model_error", "round": n, "span_id": self._span(n),
                              "parent_id": self.trace.trace_id(), "latency_ms": _ms(started),
                              "status": getattr(exc, "status_code", None),
                              "error": f"{type(exc).__name__}: {exc}"[:4000], **sent})
            raise
        self._safely(self._response, response, n, _ms(started), sent)
        return response

    def _request(self, request_context: Any, n: int, sent: dict[str, Any]) -> None:
        """Before the call: a changed head (compaction), the job description and
        tools when they change, `call_start`; `sent` gets what the call adds."""
        from pydantic_ai.messages import ModelRequest, ModelResponse

        messages = list(request_context.messages)
        first = messages[0] if messages else None
        if first is not self.trace.head_message:
            head: list = []
            for message in messages:
                if not isinstance(message, ModelRequest):
                    break
                head.append(_dump(message))
            head_sha = _sha(json.dumps(head[:1], sort_keys=True, default=str))
            if self.trace.head_sha is not None and head_sha != self.trace.head_sha:
                self.trace.write({"type": "history_rewritten", "round": n, "span_id": f"{self._span(n)}:compaction",
                                  "parent_id": self.trace.trace_id(), "messages_before": self.trace.context_messages,
                                  "messages_after": len(messages), "head": head})
            self.trace.head_sha = head_sha
            self.trace.head_message = first
        self.trace.context_messages = len(messages)
        tools = _tool_defs(getattr(request_context, "model_request_parameters", None))
        tools_sha = _sha(json.dumps(tools, sort_keys=True, default=str))
        if tools and tools_sha != self.trace.tools_sha:
            self.trace.tools_sha = tools_sha
            self.trace.write({"type": "tools", "sha256": tools_sha, "span_id": f"{self._span(n)}:tools",
                              "parent_id": self.trace.trace_id(), "tools": tools})
        # What this call adds: every request after the model's last answer.
        last_answer = max((i for i, m in enumerate(messages) if isinstance(m, ModelResponse)), default=-1)
        added = [m for m in messages[last_answer + 1:] if isinstance(m, ModelRequest)]
        instructions = (added[-1].instructions if added else None) or ""
        if instructions and _sha(instructions) != self.trace.instructions_sha:
            self.trace.instructions_sha = _sha(instructions)
            self.trace.write({"type": "instructions", "sha256": self.trace.instructions_sha,
                              "span_id": f"{self._span(n)}:instructions", "parent_id": self.trace.trace_id(),
                              "text": instructions})
        parts: list = []
        for message in added:
            body = _dump(message)
            parts.extend(body.get("parts", []))
        sent["input"] = parts
        sent["instructions_sha"] = self.trace.instructions_sha
        self.trace.write({"type": "call_start", "round": n, "span_id": self._span(n),
                          "context_messages": len(messages)})

    def _response(self, response: Any, n: int, latency_ms: int, sent: dict[str, Any]) -> None:
        from probe.daemon import usage as usage_mod

        self.trace.write({"type": "call", "round": n, "span_id": self._span(n), "parent_id": self.trace.trace_id(),
                          "latency_ms": latency_ms, "cost_usd": usage_mod.response_cost(response), **sent,
                          "output": _dump(response)})

    # -- tool runs -----------------------------------------------------------
    async def wrap_tool_execute(self, ctx: Any, *, call: Any, tool_def: Any, args: Any, handler: Any) -> Any:
        if self.trace.off:
            return await handler(args)
        started = time.monotonic()
        n = self.rounds
        base = {"type": "tool", "round": n, "span_id": f"{self._span(n)}:{call.tool_call_id}",
                "parent_id": self._span(n), "tool": call.tool_name, "call_id": call.tool_call_id,
                "args": _args(call, args)}
        try:
            result = await handler(args)
        except Exception as exc:
            self.trace.write({**base, "duration_ms": _ms(started), "outcome": type(exc).__name__,
                              "error": str(exc)[:4000]})
            raise
        self.trace.write({**base, "duration_ms": _ms(started), "outcome": "ok", "result": result})
        return result

    def _safely(self, fn: Any, *args: Any) -> None:
        try:
            fn(*args)
        except Exception as exc:  # noqa: BLE001 -- tracing never fails a bite
            log.warning("a %s trace line was not written: %s: %s", self.trace.agent, type(exc).__name__, exc)


def _args(call: Any, validated: Any) -> Any:
    """The call's arguments as the model sent them (a dict), else as validated."""
    try:
        return call.args_as_dict()
    except Exception:  # noqa: BLE001 -- a malformed argument string is still worth showing
        return validated if isinstance(validated, dict) else str(getattr(call, "args", validated))
