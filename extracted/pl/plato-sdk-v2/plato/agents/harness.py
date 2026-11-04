"""Helpers shared by the native-CLI agent harnesses under ``agents/``.

Each of these existed as a copy in several harnesses (grok-build, antigravity,
mimo-code, muse-spark, opencode, qwen-code, codex). They are deliberately
small and behaviour-preserving: a harness that needs something different
keeps its own version.
"""

from __future__ import annotations

import asyncio
import hashlib
import importlib.metadata
import json
import logging
import os
import re
import signal
from collections.abc import Iterable, Mapping
from contextlib import suppress
from pathlib import Path
from typing import Any

from opentelemetry.context import Context
from opentelemetry.trace import (
    NonRecordingSpan,
    Span,
    SpanContext,
    TraceFlags,
    Tracer,
    set_span_in_context,
)

from plato.tools.mcp import McpRemoteServer

logger = logging.getLogger(__name__)

# ---- versions ---------------------------------------------------------------


def plato_sdk_version() -> str:
    """The installed ``plato-sdk-v2`` version, or ``"unknown"``."""
    try:
        return importlib.metadata.version("plato-sdk-v2")
    except importlib.metadata.PackageNotFoundError:
        return "unknown"


def agent_version(distribution: str) -> str:
    """The installed version of an agent distribution, or ``"unknown"``."""
    try:
        return importlib.metadata.version(distribution)
    except importlib.metadata.PackageNotFoundError:
        return "unknown"


# What `<cli> --version` reports, e.g. "1.18.3" or "0.20.0-rc.1".
CLI_VERSION_PATTERN = re.compile(r"\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.]+)?")


async def probe_cli_version(binary: str, env: Mapping[str, str] | None = None) -> str:
    """Return the version ``<binary> --version`` reports.

    The runtime image installs the latest CLI release, so this probe is the
    record of which version a run used (it goes on the root span). A CLI that
    cannot run or does not report a version fails startup here rather than
    producing an untraceable run.
    """
    try:
        process = await asyncio.create_subprocess_exec(
            binary,
            "--version",
            env=dict(env) if env is not None else None,
            stdin=asyncio.subprocess.DEVNULL,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT,
        )
    except OSError as exc:
        raise RuntimeError(f"{binary} CLI not found - ensure the runtime image includes it ({exc})") from exc
    stdout, _ = await asyncio.wait_for(process.communicate(), timeout=120)
    output = stdout.decode(errors="replace")
    match = CLI_VERSION_PATTERN.search(output) if process.returncode == 0 else None
    if match is None:
        raise RuntimeError(f"{binary} --version failed (exit {process.returncode}): {output}")
    return match.group(0)


# ---- processes ----------------------------------------------------------------


async def stop_process_group(process: asyncio.subprocess.Process, *, grace_seconds: float = 5.0) -> None:
    """Reap a CLI started with ``start_new_session=True`` and its process group.

    SIGTERM the group, wait ``grace_seconds``, SIGKILL on timeout; a final
    SIGKILL covers a tool child that outlived its parent, so nothing keeps
    running after this run released its workspace and sidecars.
    """
    with suppress(ProcessLookupError):
        os.killpg(process.pid, signal.SIGTERM)
    try:
        await asyncio.wait_for(process.wait(), timeout=grace_seconds)
    except TimeoutError:
        with suppress(ProcessLookupError):
            os.killpg(process.pid, signal.SIGKILL)
        await process.wait()
    finally:
        with suppress(ProcessLookupError):
            os.killpg(process.pid, signal.SIGKILL)


# ---- final answer -----------------------------------------------------------


OutputSignature = tuple[int, int, int, int, bytes]


def output_signature(path: Path) -> OutputSignature | None:
    """Identify the current contents of ``path``, or None when it does not exist.

    Detects a fresh agent-authored answer, including same-size rewrites.
    """
    try:
        with path.open("rb") as output:
            stat = os.fstat(output.fileno())
            digest = hashlib.file_digest(output, "sha256").digest()
            return (stat.st_ino, stat.st_mtime_ns, stat.st_ctime_ns, stat.st_size, digest)
    except FileNotFoundError:
        return None


def save_final_reply(path: Path, previous: OutputSignature | None, text: str) -> bool:
    """Write the agent's final reply to ``path`` unless the agent wrote it itself.

    Worlds may ask the agent to write structured output to this file. A fresh
    agent-written file takes precedence over a brief final reply; an untouched
    answer from an earlier run is stale (even on continuation) and is replaced.
    Returns whether the reply was written.
    """
    if output_signature(path) in (None, previous):
        path.write_text(text)
        return True
    return False


# ---- logs -----------------------------------------------------------------------


class JsonlTail:
    """Incrementally read complete lines from a JSONL file that is being appended to."""

    def __init__(self, path: Path, *, from_end: bool = False) -> None:
        self.path = path
        self._offset = path.stat().st_size if from_end and path.exists() else 0
        self._partial = b""

    def read_lines(self) -> list[bytes]:
        """Complete, non-blank lines appended since the last call."""
        try:
            with self.path.open("rb") as log:
                log.seek(self._offset)
                data = log.read()
        except FileNotFoundError:
            return []
        self._offset += len(data)
        lines = (self._partial + data).split(b"\n")
        self._partial = lines.pop()
        return [line for line in lines if line.strip()]

    def read(self) -> list[dict[str, Any]]:
        """New JSON object records; other lines are logged and skipped."""
        records: list[dict[str, Any]] = []
        for line in self.read_lines():
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                logger.warning("Unparseable JSONL line in %s", self.path)
                continue
            if isinstance(record, dict):
                records.append(record)
        return records


# ---- pricing ----------------------------------------------------------------------


def litellm_cost(
    model_keys: Iterable[str],
    prompt_tokens: int,
    completion_tokens: int,
    cache_read_tokens: int = 0,
) -> float | None:
    """Price a request from litellm's model map, or None when the model is unpriced.

    ``model_keys`` are tried in order (e.g. ``"gemini/<model>"``, ``"<model>"``).
    Cached input is billed at the cache-read rate (the input rate when the map
    has none) and subtracted from the non-cached input; ``completion_tokens``
    must already include reasoning tokens where the provider bills them as
    output. ``litellm`` is imported on first use: it is slow to import and
    most harnesses never price through it.
    """
    from litellm import model_cost

    pricing: Mapping[str, Any] = {}
    for key in model_keys:
        candidate = model_cost.get(key)
        if candidate:
            pricing = candidate
            break
    if not pricing:
        return None
    input_rate = pricing.get("input_cost_per_token", 0) or 0
    output_rate = pricing.get("output_cost_per_token", 0) or 0
    cache_rate = pricing.get("cache_read_input_token_cost", input_rate) or 0
    non_cached_input = max(0, prompt_tokens - cache_read_tokens)
    cost = non_cached_input * input_rate + cache_read_tokens * cache_rate + completion_tokens * output_rate
    return cost or None


# ---- MCP ------------------------------------------------------------------------


def require_resolved_mcp_url(name: str, server: McpRemoteServer) -> str:
    """The server's literal URL; raise when it is still an ``{env, path, port}`` alias.

    Worlds resolve aliases to a booted sim's connect URL before the agent
    parses its config. Reaching an alias here means the world never resolved
    it, so fail loudly rather than hand the CLI something it cannot dial.
    """
    if not isinstance(server.url, str):
        raise ValueError(
            f"mcp server {name!r}: url is an unresolved env reference {server.url!r}; "
            "the world must resolve {env, path, port} aliases before the agent starts"
        )
    return server.url


# ---- subagent spans ----------------------------------------------------------


def span_context_from_ids(trace_id: str, span_id: str) -> Context:
    """A parent context for spans that must nest under an already-exported span.

    ``trace_id``/``span_id`` are the lowercase hex ids
    (:func:`plato.utils.tool_execution.span_trace_id` / ``span_span_id``) of,
    e.g., the tool step that spawned a subagent.
    """
    return set_span_in_context(
        NonRecordingSpan(
            SpanContext(
                trace_id=int(trace_id, 16),
                span_id=int(span_id, 16),
                is_remote=False,
                trace_flags=TraceFlags(TraceFlags.SAMPLED),
            )
        )
    )


def start_subagent_span(
    tracer: Tracer,
    *,
    harness: str,
    agent_type: str,
    subagent_id: str,
    model_name: str,
    context: Context | None,
    description: str | None = None,
    tool_use_id: str | None = None,
    start_time_ns: int | None = None,
    attributes: Mapping[str, Any] | None = None,
) -> Span:
    """Open the ``atif.kind=agent`` span one subagent's steps are emitted under.

    ``context`` is normally the spawn call's step span
    (:func:`span_context_from_ids`), so the subagent sits inside the session
    trace under the call that started it.
    """
    span = tracer.start_span(f"subagent.{agent_type}", context=context, start_time=start_time_ns)
    span.set_attribute("atif.kind", "agent")
    span.set_attribute("atif.agent.name", f"{harness}:{agent_type}")
    span.set_attribute("atif.agent.model_name", model_name)
    span.set_attribute("plato.subagent.id", subagent_id)
    span.set_attribute("plato.subagent.agent_type", agent_type)
    if description:
        span.set_attribute("plato.subagent.description", description)
    if tool_use_id:
        span.set_attribute("plato.subagent.tool_use_id", tool_use_id)
    for key, value in (attributes or {}).items():
        span.set_attribute(key, value)
    return span


def finish_subagent_span(
    span: Span,
    *,
    tokens: Mapping[str, int] | None = None,
    turn_count: int | None = None,
    cost_usd: float | None = None,
    end_time_ns: int | None = None,
    prefix: str = "plato.subagent",
    turn_count_key: str = "atif.agent.turn_count",
) -> None:
    """Record a subagent's totals on its span and end it.

    ``tokens`` maps ATIF token names (``prompt_tokens`` …) to totals; zero
    values are not recorded. ``cost_usd`` is recorded only when given (a
    subagent whose model is unpriced carries no cost attribute).
    """
    for key, value in (tokens or {}).items():
        if value:
            span.set_attribute(f"{prefix}.{key}", value)
    if turn_count is not None:
        span.set_attribute(turn_count_key, turn_count)
    if cost_usd is not None:
        span.set_attribute(f"{prefix}.cost_usd", cost_usd)
    span.end(end_time=end_time_ns)
