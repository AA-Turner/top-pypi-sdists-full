"""Shared Claude Code transcript → ATIF span conversion.

Single source of truth for turning Claude Code turn data into ATIF step
spans, used by two callers that must never drift:

- **Live**: the ``claude-code`` agent parses stream-json stdout events and
  tails sub-agent JSONL transcripts under ``~/.claude/projects``, emitting
  spans as the session runs (``agents/claude-code``).
- **Replay**: ``plato chronos import claude-code`` replays an on-disk Claude
  Code project directory (main ``<session-id>.jsonl`` + ``subagents/`` tree)
  into a freshly minted Chronos session, stamping spans at their historical
  transcript timestamps.

The on-disk transcript envelope (``{"type": ..., "message": {...}}``) matches
the stdout stream-json envelope, so one event parser
(:meth:`ClaudeTranscriptEmitter.emit_event`) serves both; on-disk-only record
types (``file-history-snapshot``, ``attachment``, ``queue-operation``, …) are
filtered by :func:`normalize_transcript_record`.
"""

from __future__ import annotations

import asyncio
import json
import logging
from collections.abc import Callable
from contextlib import suppress
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

from opentelemetry import context as otel_context
from opentelemetry import trace as otel_trace
from opentelemetry.trace import NonRecordingSpan, Span, SpanContext, TraceFlags, Tracer

from plato.otel import DeferredStepSpan, emit_step, start_deferred_step_span
from plato.utils.tool_execution import (
    ToolExecutionRecorderLike,
    ToolExecutionStatus,
    claude_mcp_tool_origin,
    open_tool_execution,
    tool_call_payload,
)

logger = logging.getLogger(__name__)

SYSTEM_REMINDER_OPEN = "<system-reminder>"
SYSTEM_REMINDER_CLOSE = "</system-reminder>"

# Transcript record ``type`` values that carry a turn we trace. Everything else
# (``attachment`` deltas, ``summary``, ``system`` housekeeping, …) is skipped.
_TRACED_RECORD_TYPES = frozenset({"user", "assistant", "result"})

_AGENT_GLOB = "agent-*.jsonl"
_META_SUFFIX = ".meta.json"


def is_system_reminder_message(message: str) -> bool:
    """True when a user-visible message is a wrapped system reminder."""
    stripped = message.strip()
    return stripped.startswith(SYSTEM_REMINDER_OPEN) and stripped.endswith(SYSTEM_REMINDER_CLOSE)


def normalize_locally_emitted_message(message: str) -> str:
    """Normalization applied before matching locally injected messages."""
    return message.strip()


def tool_call_path(tool_input: dict[str, Any]) -> str | None:
    """Best-effort file path extracted from a tool call's input."""
    for key in ("file_path", "path", "filepath"):
        value = tool_input.get(key)
        if isinstance(value, str) and value:
            return value
    return None


def parse_timestamp_ns(record: Any) -> int | None:
    """Convert a transcript record's ISO8601 ``timestamp`` to unix nanoseconds.

    Returns ``None`` if absent or unparseable. Used to stamp spans at their true
    wall-clock position in the trace rather than at parse time — otherwise the
    1s poller's read time leaks into the timeline and sub-agent spans can sort
    before the tool call that spawned them.
    """
    if not isinstance(record, dict):
        return None
    raw = record.get("timestamp")
    if not isinstance(raw, str) or not raw:
        return None
    # ``fromisoformat`` accepts the trailing ``Z`` on 3.11+; normalize anyway.
    try:
        dt = datetime.fromisoformat(raw.replace("Z", "+00:00"))
    except ValueError:
        return None
    return int(dt.timestamp() * 1_000_000_000)


def normalize_transcript_record(record: Any) -> dict[str, Any] | None:
    """Map an on-disk transcript line to the event shape ``emit_event`` wants.

    Returns the event dict (``{"type", "message", ...}``) for records that
    carry a traceable turn, or ``None`` for records to skip (attachments,
    unknown shapes). The envelope already matches the stdout stream-json shape,
    so this is a filter rather than a transform.
    """
    if not isinstance(record, dict):
        return None
    record_type = record.get("type")
    if record_type not in _TRACED_RECORD_TYPES:
        return None
    # ``result`` records carry their text at top level; ``user``/``assistant``
    # carry a ``message`` envelope. Require the field the parser will read.
    if record_type in {"user", "assistant"} and not isinstance(record.get("message"), dict):
        return None
    return record


def read_subagent_meta(transcript_path: Path) -> dict[str, Any]:
    """Read the ``agent-<id>.meta.json`` sitting next to a transcript, if any."""
    # transcript is ``agent-<id>.jsonl`` -> meta is ``agent-<id>.meta.json``.
    meta_path = transcript_path.parent / (transcript_path.stem + _META_SUFFIX)
    if not meta_path.exists():
        return {}
    try:
        data = json.loads(meta_path.read_text())
    except (OSError, json.JSONDecodeError):
        logger.debug("Could not read sub-agent meta at %s", meta_path, exc_info=True)
        return {}
    return data if isinstance(data, dict) else {}


def agent_id_from_path(transcript_path: Path) -> str:
    """Extract ``<agentId>`` from an ``agent-<agentId>.jsonl`` path."""
    stem = transcript_path.stem  # agent-<id>
    return stem[len("agent-") :] if stem.startswith("agent-") else stem


def read_workflow_journal(journal_path: Path) -> dict[str, str]:
    """Parse a workflow ``journal.jsonl`` into ``{agentId: result_text}``.

    Only ``result`` entries contribute; ``started`` entries are ignored. The
    last result wins per agent.
    """
    results: dict[str, str] = {}
    if not journal_path.exists():
        return results
    try:
        for line in journal_path.read_text().splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(rec, dict) and rec.get("type") == "result":
                agent_id = rec.get("agentId")
                if isinstance(agent_id, str):
                    results[agent_id] = str(rec.get("result", ""))
    except OSError:
        logger.debug("Could not read workflow journal at %s", journal_path, exc_info=True)
    return results


def discover_subagent_transcripts(subagents_dir: Path) -> list[Path]:
    """Find every ``agent-*.jsonl`` under a session's ``subagents/`` tree.

    Covers both direct Task/background transcripts (``subagents/agent-*.jsonl``)
    and workflow sub-agents (``subagents/workflows/wf_*/agent-*.jsonl``).
    """
    if not subagents_dir.is_dir():
        return []
    return sorted(subagents_dir.rglob(_AGENT_GLOB))


def workflow_results_for(subagents_dir: Path) -> dict[str, str]:
    """Aggregate ``{agentId: result}`` from every workflow journal under a dir."""
    results: dict[str, str] = {}
    for journal in subagents_dir.rglob("journal.jsonl"):
        results.update(read_workflow_journal(journal))
    return results


@dataclass
class PendingClaudeToolCall:
    """Pending Claude tool call paired from tool_use to tool_result."""

    name: str
    tool_input: dict[str, Any] = field(default_factory=dict)
    execution: Any | None = None  # ActiveToolExecution when a recorder is attached
    step_id: int | None = None


class StreamUsageAccountant:
    """Accumulates token usage from Claude Code stream-json events.

    Claude Code can emit multiple ``assistant`` envelopes for one logical
    turn (e.g. a thinking block envelope and a text block envelope), each
    carrying the *same* running-snapshot ``usage``. Naively summing across
    envelopes double-counts inputs/cache and miscounts outputs (the
    streamed envelopes report ``output_tokens`` as a stop-marker placeholder
    like 0 or 1; only the ``result`` event carries the true final count).

    This accountant dedupes by ``message.id`` so each turn contributes its
    streamed usage at most once. When a ``result`` event is recorded, its
    final usage and ``total_cost_usd`` replace the streamed estimates.
    """

    def __init__(self, *, cost_fn, authoritative_streamed_cost: bool = False):
        # When True (OpenRouter generation-stats resolution), the per-turn
        # BILLED costs folded in via ``record_resolved_usage`` are the cost
        # source of truth: the result event's ``total_cost_usd`` — the CLI's
        # list-price ESTIMATE, which can differ from billed by an order of
        # magnitude — never overrides the total. It is exposed separately as
        # ``atif.agent.cost_estimate_usd`` by ``apply_to_span`` so the root
        # cost always equals the sum of per-step cost attributes.
        self._authoritative_streamed_cost = authoritative_streamed_cost
        self._cost_fn = cost_fn
        self._seen_message_ids: set[str] = set()
        self._turn_count = 0
        self._streamed_prompt_tokens = 0
        self._streamed_output_tokens = 0
        self._streamed_cache_read_tokens = 0
        self._streamed_cache_creation_tokens = 0
        self._streamed_cost_usd = 0.0
        self._result_prompt_tokens: int | None = None
        self._result_output_tokens: int | None = None
        self._result_cache_read_tokens: int | None = None
        self._result_cache_creation_tokens: int | None = None
        self._result_cost_usd: float | None = None

    def record_assistant(self, event: dict[str, Any]) -> None:
        message = event.get("message") or {}
        message_id = message.get("id")
        if isinstance(message_id, str) and message_id in self._seen_message_ids:
            return
        if isinstance(message_id, str) and message_id:
            self._seen_message_ids.add(message_id)
        self._turn_count += 1

        usage = message.get("usage") or {}
        uncached = usage.get("input_tokens", 0) or 0
        cache_read = usage.get("cache_read_input_tokens", 0) or 0
        cache_create = usage.get("cache_creation_input_tokens", 0) or 0
        output = usage.get("output_tokens", 0) or 0

        self._streamed_prompt_tokens += uncached + cache_read + cache_create
        self._streamed_output_tokens += output
        self._streamed_cache_read_tokens += cache_read
        self._streamed_cache_creation_tokens += cache_create

        cost = self._cost_fn(
            uncached_input_tokens=uncached,
            cache_read_tokens=cache_read,
            cache_write_tokens=cache_create,
            output_tokens=output,
        )
        if cost is not None:
            self._streamed_cost_usd += cost

    def record_result(self, event: dict[str, Any]) -> None:
        usage = event.get("usage") or {}
        if usage:
            uncached = usage.get("input_tokens", 0) or 0
            cache_read = usage.get("cache_read_input_tokens", 0) or 0
            cache_create = usage.get("cache_creation_input_tokens", 0) or 0
            output = usage.get("output_tokens", 0) or 0
            self._result_prompt_tokens = uncached + cache_read + cache_create
            self._result_output_tokens = output
            self._result_cache_read_tokens = cache_read
            self._result_cache_creation_tokens = cache_create
        cost = event.get("total_cost_usd")
        if cost is None:
            cost = event.get("cost_usd")
        if cost is not None:
            self._result_cost_usd = float(cost)

    @property
    def turn_count(self) -> int:
        return self._turn_count

    @property
    def prompt_tokens(self) -> int:
        if self._result_prompt_tokens is not None:
            return self._result_prompt_tokens
        return self._streamed_prompt_tokens

    @property
    def output_tokens(self) -> int:
        if self._result_output_tokens is not None:
            return self._result_output_tokens
        return self._streamed_output_tokens

    @property
    def cache_read_tokens(self) -> int:
        if self._result_cache_read_tokens is not None:
            return self._result_cache_read_tokens
        return self._streamed_cache_read_tokens

    @property
    def cache_creation_tokens(self) -> int:
        if self._result_cache_creation_tokens is not None:
            return self._result_cache_creation_tokens
        return self._streamed_cache_creation_tokens

    @property
    def cost_usd(self) -> float:
        if self._authoritative_streamed_cost:
            return self._streamed_cost_usd
        if self._result_cost_usd is not None:
            return self._result_cost_usd
        return self._streamed_cost_usd

    def record_resolved_usage(
        self,
        *,
        prompt_tokens: int,
        completion_tokens: int,
        cache_read_tokens: int = 0,
        cost_usd: float | None = None,
    ) -> None:
        """Fold post-hoc resolved per-turn usage into the streamed totals.

        Used for turns whose stream envelopes carried no usage (custom
        endpoints like OpenRouter) once their true numbers are fetched from
        the provider's generation-stats API. Keeps run totals meaningful even
        when the final ``result`` event never arrives (crash mid-run); when
        the result event does arrive, its TOKEN totals still override these
        (same counting basis), while cost precedence follows
        ``authoritative_streamed_cost``.
        """
        self._streamed_prompt_tokens += prompt_tokens
        self._streamed_output_tokens += completion_tokens
        self._streamed_cache_read_tokens += cache_read_tokens
        if cost_usd:
            self._streamed_cost_usd += cost_usd

    @property
    def cost_from_result_event(self) -> bool:
        return self._result_cost_usd is not None

    def apply_to_span(self, root_span) -> None:
        """Set ATIF token attributes on the root span from best-known totals."""
        if self.cost_usd > 0:
            root_span.set_attribute("atif.agent.cost_usd", self.cost_usd)
        if self._authoritative_streamed_cost and self._result_cost_usd:
            # Keep the CLI's list-price estimate visible without letting it
            # masquerade as the billed total: the root cost above stays equal
            # to the sum of per-step billed cost attributes.
            root_span.set_attribute("atif.agent.cost_estimate_usd", self._result_cost_usd)
        if self.prompt_tokens > 0:
            root_span.set_attribute("atif.agent.prompt_tokens", self.prompt_tokens)
        if self.output_tokens > 0:
            root_span.set_attribute("atif.agent.completion_tokens", self.output_tokens)
        if self.cache_read_tokens > 0:
            root_span.set_attribute("atif.agent.cache_read_tokens", self.cache_read_tokens)
        if self.cache_creation_tokens > 0:
            root_span.set_attribute("atif.agent.cache_write_tokens", self.cache_creation_tokens)
        root_span.set_attribute("atif.agent.turn_count", self.turn_count)


class ClaudeTranscriptEmitter:
    """Converts Claude Code turn events into ATIF step spans.

    One instance per (session, tracer). ``model_name`` is the fallback when an
    event doesn't carry its own ``message.model``; ``workspace_dir`` seeds the
    working-directory hint on tool spans; ``cost_fn`` (same kwargs contract as
    :class:`StreamUsageAccountant`) computes per-turn cost or returns ``None``.

    ``use_transcript_timestamps=True`` stamps every emitted span at the
    event's own ``timestamp`` (offline replay); events without a timestamp
    fall back to live now-stamping, so the flag is safe for mixed input.

    ``tool_result_text_resolver`` post-processes the text content of each
    tool_result observation — the replay path uses it to inline full
    ``<persisted-output>`` payloads from ``tool-results/``. ``None`` leaves
    content untouched (live behavior).
    """

    def __init__(
        self,
        tracer: Tracer,
        *,
        model_name: str,
        workspace_dir: str | None = None,
        cost_fn: Callable[..., float | None] | None = None,
        use_transcript_timestamps: bool = False,
        tool_result_text_resolver: Callable[[str], str] | None = None,
        defer_unattributed_usage: bool = False,
    ):
        self.tracer = tracer
        self.model_name = model_name
        self.workspace_dir = workspace_dir
        self._cost_fn = cost_fn
        self.use_transcript_timestamps = use_transcript_timestamps
        self._tool_result_text_resolver = tool_result_text_resolver
        # When True, the first step span of a turn whose envelopes carry no
        # usage is created with true timestamps but held un-exported
        # (deferred export) while an external resolver (the claude-code
        # agent's OpenRouter generation-stats fetcher) fetches the turn's
        # real usage; ``resolve_deferred_usage`` merges it into the span and
        # exports it, ``flush_deferred_usage`` exports bare on timeout or
        # teardown. The result-step aggregate fallback is skipped so the two
        # mechanisms can't double-count.
        self.defer_unattributed_usage = defer_unattributed_usage
        # message.id -> step_id of the turn's deferred usage-carrier span.
        # Drained by the agent's resolver scheduler.
        self.unattributed_turns: dict[str, int] = {}
        self._unattributed_seen: set[str] = set()
        # message.id -> the held (un-exported) usage-carrier span.
        self._deferred_spans: dict[str, DeferredStepSpan] = {}
        # Turns whose usage never resolved (flushed bare). Surfaced on the
        # root span as ``atif.agent.unresolved_usage_turns`` so a root total
        # below the true spend is explainable from span data alone.
        self.unresolved_usage_turns = 0
        # Every tool_use span's identity, kept for the session's lifetime (not
        # popped on result) so sub-agent wrapper spans can be parented under
        # the Task/Workflow tool call that spawned them via meta ``toolUseId``.
        self.tool_span_contexts: dict[str, SpanContext] = {}
        # Running count of spans this emitter has opened. Offline replay keys
        # its BatchSpanProcessor flush cadence on this (spans, not input
        # records — one record can emit many spans).
        self.spans_emitted = 0
        # True once any assistant envelope carried real (nonzero) usage.
        # Custom Anthropic-compatible endpoints (e.g. OpenRouter) zero out
        # per-message usage in the live stream — real usage arrives only on
        # the final ``result`` event — so this gates the result-step
        # aggregate-usage fallback in ``emit_event``.
        self._stream_usage_seen = False
        # message.ids whose streamed usage already landed on a step; later
        # envelopes of the same turn repeat the snapshot and must stay bare.
        self._usage_attributed_message_ids: set[str] = set()

    def compute_cost(
        self,
        *,
        uncached_input_tokens: int,
        cache_read_tokens: int,
        cache_write_tokens: int,
        output_tokens: int,
    ) -> float | None:
        """Delegate to the configured cost function (``None`` = no cost)."""
        if self._cost_fn is None:
            return None
        return self._cost_fn(
            uncached_input_tokens=uncached_input_tokens,
            cache_read_tokens=cache_read_tokens,
            cache_write_tokens=cache_write_tokens,
            output_tokens=output_tokens,
        )

    def parent_context_for_tool_use(self, tool_use_id: str | None) -> SpanContext | None:
        """Span context of a previously emitted tool_use step, if known."""
        if not tool_use_id:
            return None
        return self.tool_span_contexts.get(tool_use_id)

    def _deferral_carrier(self, message_id: Any) -> bool:
        """True when this zero-usage turn still needs its usage-carrier span.

        Only the turn's FIRST span is deferred and carries the resolved
        usage; later envelopes of the same message emit immediately.
        """
        if not self.defer_unattributed_usage:
            return False
        if not isinstance(message_id, str) or not message_id:
            return False
        return message_id not in self._unattributed_seen

    def _register_deferred_turn(self, message_id: str, step_id: int, deferred: DeferredStepSpan) -> None:
        self._unattributed_seen.add(message_id)
        self.unattributed_turns[message_id] = step_id
        self._deferred_spans[message_id] = deferred

    def resolve_deferred_usage(
        self,
        message_id: str,
        *,
        prompt_tokens: int,
        completion_tokens: int,
        cache_read_tokens: int = 0,
        cost_usd: float | None = None,
        usage_source: str | None = None,
    ) -> bool:
        """Merge resolved usage into the turn's held span and export it.

        Returns False when the turn has no held span (already flushed, or
        never deferred).
        """
        deferred = self._deferred_spans.pop(message_id, None)
        if deferred is None:
            return False
        deferred.finish(
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            cache_read_tokens=cache_read_tokens,
            cost_usd=cost_usd,
            usage_source=usage_source,
        )
        return True

    def flush_deferred_usage(self, message_id: str | None = None) -> None:
        """Export held span(s) without usage (resolution failed / teardown)."""
        if message_id is not None:
            deferred = self._deferred_spans.pop(message_id, None)
            if deferred is not None:
                deferred.finish()
                self.unresolved_usage_turns += 1
            return
        while self._deferred_spans:
            _, deferred = self._deferred_spans.popitem()
            deferred.finish()
            self.unresolved_usage_turns += 1

    def _resolve_tool_result_text(self, text: str) -> str:
        if not text or self._tool_result_text_resolver is None:
            return text
        try:
            return self._tool_result_text_resolver(text)
        except Exception:
            logger.warning("tool_result text resolver failed; keeping original", exc_info=True)
            return text

    def parse_tool_result(
        self,
        tool_use_id: str,
        tool_name: str,
        tool_input: dict[str, Any],
        content: Any,
    ) -> tuple[dict[str, Any], str | None, str | None]:
        """Normalize a Claude tool_result block into observation payload + optional image."""
        file_path = tool_call_path(tool_input)
        text_parts: list[str] = []
        attachments: list[dict[str, Any]] = []
        screenshot: str | None = None
        screenshot_format: str | None = None

        if isinstance(content, list):
            for item in content:
                if isinstance(item, str):
                    text_parts.append(item)
                    continue
                if not isinstance(item, dict):
                    text_parts.append(json.dumps(item, default=str))
                    continue

                item_type = item.get("type")
                if item_type == "text":
                    text_parts.append(item.get("text", ""))
                    continue
                if item_type == "image":
                    source = item.get("source", {})
                    if isinstance(source, dict):
                        data = source.get("data")
                        media_type = source.get("media_type")
                        if isinstance(data, str) and data:
                            if screenshot is None:
                                screenshot = data
                                screenshot_format = media_type if isinstance(media_type, str) else "image/png"
                            attachments.append(
                                {
                                    "type": "image",
                                    "base64": data,
                                    "media_type": media_type,
                                    **({"file_path": file_path} if file_path else {}),
                                }
                            )
                            continue
                attachments.append(item)
        elif isinstance(content, str):
            # Claude Code delivers MCP tool results as a JSON string shaped like
            # {"content": [{"type": "image", "data": "...", "mimeType": "..."}, ...]}
            # Peek inside to extract a screenshot for atif.step.screenshot without
            # changing what goes into the observation text.
            try:
                parsed = json.loads(content)
            except (json.JSONDecodeError, TypeError):
                parsed = None
            if isinstance(parsed, dict) and isinstance(parsed.get("content"), list):
                for item in parsed["content"]:
                    if isinstance(item, dict) and item.get("type") == "image":
                        data = item.get("data")
                        media_type = item.get("mimeType") or item.get("media_type")
                        if isinstance(data, str) and data and screenshot is None:
                            screenshot = data
                            screenshot_format = media_type if isinstance(media_type, str) else "image/jpeg"
            text_parts.append(content)
        else:
            text_parts.append(json.dumps(content, default=str))

        text_content = "\n".join(part for part in text_parts if part).strip()
        text_content = self._resolve_tool_result_text(text_content)
        if not text_content:
            if attachments and file_path:
                text_content = f"Read image file: {file_path}"
            elif attachments:
                text_content = f"{tool_name} returned {len(attachments)} attachment(s)"

        result: dict[str, Any] = {
            "source_call_id": tool_use_id,
            "content": text_content,
            "tool_name": tool_name,
        }
        if file_path:
            result["file_path"] = file_path
        if attachments:
            result["attachments"] = attachments
        if tool_name.lower() in {"read", "read_file"} and file_path:
            result["kind"] = "file"
            if attachments:
                result["kind"] = "image"

        return result, screenshot, screenshot_format

    def emit_event(
        self,
        event: dict[str, Any],
        pending_tool_calls: dict[str, PendingClaudeToolCall],
        step_counter: list[int],
        tool_execution_recorder: ToolExecutionRecorderLike | None = None,
        pending_locally_emitted_messages: set[str] | None = None,
    ) -> None:
        """Emit ATIF step spans for one Claude Code event.

        Args:
            event: Parsed JSON event (stream-json stdout or transcript record)
            pending_tool_calls: Map of tool_use_id -> pending tool execution state
            step_counter: Mutable list with single int for step ID tracking
            tool_execution_recorder: Optional recorder for tool attribution
            pending_locally_emitted_messages: Messages injected locally that
                should be suppressed when echoed back by --replay-user-messages
        """
        event_type = event.get("type", "unknown")
        ts_ns = parse_timestamp_ns(event) if self.use_transcript_timestamps else None

        def next_step() -> int:
            step_counter[0] += 1
            return step_counter[0]

        def current_step() -> int:
            return step_counter[0]

        if event_type == "assistant":
            message = event.get("message", {})
            content_blocks = message.get("content", [])
            if not isinstance(content_blocks, list):
                content_blocks = [content_blocks]
            usage = message.get("usage", {})

            # Collect text/thinking for the assistant message, then emit one
            # separate step span per tool_use so each tool has a durable span_id.
            text_parts: list[str] = []
            thinking_parts: list[str] = []
            tool_uses: list[tuple[str, str, dict[str, Any]]] = []

            for block in content_blocks:
                if isinstance(block, str):
                    text_parts.append(block)
                    continue
                if not isinstance(block, dict):
                    text_parts.append(json.dumps(block, default=str))
                    continue
                block_type = block.get("type", "")
                if block_type == "text":
                    text_parts.append(block.get("text", ""))
                elif block_type == "thinking":
                    thinking_parts.append(block.get("thinking", ""))
                elif block_type == "tool_use":
                    tool_id = block.get("id", "")
                    tool_name = block.get("name", "unknown")
                    tool_input = block.get("input", {})
                    normalized_input = tool_input if isinstance(tool_input, dict) else {}
                    pending_tool_calls[tool_id] = PendingClaudeToolCall(
                        name=tool_name,
                        tool_input=normalized_input,
                    )
                    tool_uses.append((tool_id, tool_name, normalized_input))

            text = "\n".join(text_parts)
            reasoning = "\n".join(thinking_parts) if thinking_parts else None
            uncached_input_tokens = usage.get("input_tokens", 0) or 0
            cache_read_tokens = usage.get("cache_read_input_tokens", 0) or 0
            cache_write_tokens = usage.get("cache_creation_input_tokens", 0) or 0
            prompt_tokens = uncached_input_tokens + cache_read_tokens + cache_write_tokens
            completion_tokens = usage.get("output_tokens")
            if prompt_tokens or completion_tokens:
                self._stream_usage_seen = True
                cost_usd = self.compute_cost(
                    uncached_input_tokens=uncached_input_tokens,
                    cache_read_tokens=cache_read_tokens,
                    cache_write_tokens=cache_write_tokens,
                    output_tokens=completion_tokens or 0,
                )
            else:
                # No usage signal in the envelope: custom Anthropic-compatible
                # endpoints (e.g. OpenRouter) report zeros/nulls per message,
                # with real usage only on the final ``result`` event. Emit no
                # token attributes rather than fake zeros; the result step
                # carries the invocation aggregate (see the result branch).
                prompt_tokens = None
                completion_tokens = None
                cache_read_tokens = None
                cache_write_tokens = None
                cost_usd = None

            # Claude Code emits one assistant envelope per content block
            # (thinking, then text / tool_use) and every envelope of the turn
            # repeats the SAME running usage snapshot (see
            # StreamUsageAccountant). Only the first envelope of a turn may
            # carry that usage onto a step, or step sums double-count.
            message_id = message.get("id")
            usage_repeated = False
            if prompt_tokens is not None and isinstance(message_id, str) and message_id:
                if message_id in self._usage_attributed_message_ids:
                    usage_repeated = True
                    prompt_tokens = None
                    completion_tokens = None
                    cache_read_tokens = None
                    cache_write_tokens = None
                    cost_usd = None
                elif text or reasoning or tool_uses:
                    self._usage_attributed_message_ids.add(message_id)

            usage_unattributed = prompt_tokens is None and not usage_repeated

            if text or reasoning:
                self.spans_emitted += 1
                step_id = next_step()
                if usage_unattributed and self._deferral_carrier(message.get("id")):
                    # Deferred export: the span exists now (true timestamps,
                    # children can already reference it) but exports once the
                    # resolver merges the turn's real usage — or bare on
                    # timeout/teardown.
                    deferred = start_deferred_step_span(
                        self.tracer,
                        step_id,
                        "agent",
                        text,
                        model_name=message.get("model", self.model_name),
                        reasoning=reasoning,
                    )
                    self._register_deferred_turn(message["id"], step_id, deferred)
                else:
                    emit_step(
                        self.tracer,
                        step_id=step_id,
                        source="agent",
                        message=text,
                        model_name=message.get("model", self.model_name),
                        reasoning=reasoning,
                        prompt_tokens=prompt_tokens,
                        completion_tokens=completion_tokens,
                        cache_read_tokens=cache_read_tokens,
                        cache_write_tokens=cache_write_tokens,
                        cost_usd=cost_usd,
                        start_time_ns=ts_ns,
                    )

            for index, (tool_id, tool_name, tool_input) in enumerate(tool_uses):
                origin, mcp_server = claude_mcp_tool_origin(tool_name)
                start_record = None
                if tool_execution_recorder is not None:
                    start_record = tool_execution_recorder.consume_start_record(
                        tool_use_id=tool_id,
                    )
                span_kwargs: dict[str, object] = {
                    "prompt_tokens": prompt_tokens if index == 0 and not text and not reasoning else None,
                    "completion_tokens": completion_tokens if index == 0 and not text and not reasoning else None,
                    "cache_read_tokens": cache_read_tokens if index == 0 and not text and not reasoning else None,
                    "cache_write_tokens": cache_write_tokens if index == 0 and not text and not reasoning else None,
                    "cost_usd": cost_usd if index == 0 and not text and not reasoning else None,
                }
                if ts_ns is not None:
                    span_kwargs["start_time_ns"] = ts_ns
                self.spans_emitted += 1
                tool_step_id = next_step()
                deferred_tool = None
                if (
                    index == 0
                    and not text
                    and not reasoning
                    and usage_unattributed
                    and self._deferral_carrier(message.get("id"))
                ):
                    # Tool-only turn: the tool span is the turn's usage
                    # carrier — create it now (children/results can reference
                    # it immediately), export once usage resolves.
                    deferred_tool = start_deferred_step_span(
                        self.tracer,
                        tool_step_id,
                        "agent",
                        "",
                        model_name=message.get("model", self.model_name),
                        tool_calls=[
                            tool_call_payload(
                                tool_call_id=tool_id,
                                function_name=tool_name,
                                arguments=tool_input,
                                origin=origin,
                                mcp_server=mcp_server,
                            )
                        ],
                    )
                    self._register_deferred_turn(message["id"], tool_step_id, deferred_tool)
                pending_execution = open_tool_execution(
                    tracer=self.tracer,
                    step_id=tool_step_id,
                    tool_id=tool_id,
                    tool_name=tool_name,
                    tool_arguments=tool_input,
                    model_name=message.get("model", self.model_name),
                    recorder=tool_execution_recorder,
                    started_at=start_record.observed_at if start_record is not None else None,
                    path_hints=[path for path in [tool_call_path(tool_input)] if path is not None],
                    working_directory=self.workspace_dir,
                    span_kwargs=span_kwargs,
                    tool_span=deferred_tool.span if deferred_tool is not None else None,
                    origin=origin,
                    mcp_server=mcp_server,
                )
                pending_tool_calls[tool_id].step_id = pending_execution.step_id
                pending_tool_calls[tool_id].execution = pending_execution.execution
                if pending_execution.trace_id and pending_execution.span_id:
                    self.tool_span_contexts[tool_id] = SpanContext(
                        trace_id=int(pending_execution.trace_id, 16),
                        span_id=int(pending_execution.span_id, 16),
                        is_remote=False,
                        trace_flags=TraceFlags(0x01),
                    )

        elif event_type == "user":
            message = event.get("message", {})
            content_blocks = message.get("content", [])
            if not isinstance(content_blocks, list):
                content_blocks = [content_blocks]

            text_parts: list[str] = []
            for block in content_blocks:
                if isinstance(block, str):
                    text_parts.append(block)
                    continue
                if not isinstance(block, dict):
                    text_parts.append(json.dumps(block, default=str))
                    continue
                block_type = block.get("type")
                if block_type == "tool_result":
                    tool_use_id = block.get("tool_use_id", "")
                    pending = pending_tool_calls.pop(tool_use_id, None) or PendingClaudeToolCall(name="unknown")
                    tool_name = pending.name
                    tool_input = pending.tool_input
                    result, screenshot, screenshot_format = self.parse_tool_result(
                        tool_use_id=tool_use_id,
                        tool_name=tool_name,
                        tool_input=tool_input,
                        content=block.get("content", ""),
                    )
                    if pending.execution is not None and tool_execution_recorder is not None:
                        tool_execution_recorder.finish(
                            pending.execution,
                            status=(
                                ToolExecutionStatus.FAILED
                                if bool(block.get("is_error"))
                                else ToolExecutionStatus.COMPLETED
                            ),
                        )
                    self.spans_emitted += 1
                    emit_step(
                        self.tracer,
                        step_id=pending.step_id or current_step(),
                        source="system",
                        message="",
                        observation={"results": [result]},
                        screenshot=screenshot,
                        screenshot_format=screenshot_format,
                        start_time_ns=ts_ns,
                    )
                elif block_type == "text":
                    text_parts.append(block.get("text", ""))

            user_text = "\n".join(part for part in text_parts if part).strip()
            if user_text:
                normalized_user_text = normalize_locally_emitted_message(user_text)
                if (
                    pending_locally_emitted_messages is not None
                    and normalized_user_text in pending_locally_emitted_messages
                ):
                    pending_locally_emitted_messages.discard(normalized_user_text)
                    return
                self.spans_emitted += 1
                emit_step(
                    self.tracer,
                    step_id=next_step(),
                    source="system" if is_system_reminder_message(user_text) else "user",
                    message=user_text,
                    start_time_ns=ts_ns,
                )

        elif event_type == "result":
            usage = event.get("usage") or {}
            uncached_input_tokens = usage.get("input_tokens", 0) or 0
            cache_read_tokens = usage.get("cache_read_input_tokens", 0) or 0
            cache_write_tokens = usage.get("cache_creation_input_tokens", 0) or 0
            prompt_tokens = uncached_input_tokens + cache_read_tokens + cache_write_tokens
            completion_tokens = usage.get("output_tokens", 0) or 0
            token_kwargs: dict[str, Any] = {}
            if (
                not self._stream_usage_seen
                and not self.defer_unattributed_usage
                and (prompt_tokens or completion_tokens)
            ):
                # Aggregate fallback: no assistant envelope carried usage this
                # invocation (custom endpoints like OpenRouter zero them out),
                # so attach the result event's whole-invocation totals here.
                # These are aggregates over every turn of the CLI invocation,
                # NOT per-turn numbers — flagged via ``usage_source`` so
                # consumers can tell them apart. Step-sums still equal the run
                # total, since every other step carried no token attributes.
                cost_usd = event.get("total_cost_usd")
                if cost_usd is None:
                    cost_usd = self.compute_cost(
                        uncached_input_tokens=uncached_input_tokens,
                        cache_read_tokens=cache_read_tokens,
                        cache_write_tokens=cache_write_tokens,
                        output_tokens=completion_tokens,
                    )
                token_kwargs = {
                    "prompt_tokens": prompt_tokens,
                    "completion_tokens": completion_tokens,
                    "cache_read_tokens": cache_read_tokens,
                    "cache_write_tokens": cache_write_tokens,
                    "cost_usd": cost_usd,
                    "usage_source": "result_event_aggregate",
                }
            self.spans_emitted += 1
            emit_step(
                self.tracer,
                step_id=next_step(),
                source="agent",
                message=str(event.get("result", "")),
                model_name=self.model_name,
                start_time_ns=ts_ns,
                **token_kwargs,
            )


@dataclass
class _SubagentState:
    """Per-transcript tracking for incremental (tailed) parsing."""

    transcript_path: Path
    agent_id: str
    meta: dict[str, Any]
    byte_offset: int = 0
    # Undecoded tail bytes from the last read. Kept as bytes (not str) so a
    # multi-byte UTF-8 char or whole record split across two reads is
    # reassembled rather than corrupted by a premature decode.
    leftover: bytes = b""
    span: Span | None = None
    pending_tool_calls: dict[str, Any] = field(default_factory=dict)
    step_counter: list[int] = field(default_factory=lambda: [0])
    finalized: bool = False
    # Whether this transcript belongs to the current run (cached once decided
    # from a record carrying sessionId/cwd). None = undecided.
    matched: bool | None = None
    # True wall-clock window from transcript timestamps (unix ns), used to
    # stamp the wrapper span so it sits at its real position in the timeline.
    first_ts_ns: int | None = None
    last_ts_ns: int | None = None


class SubagentTraceEmitter:
    """Emits nested spans for sub-agent transcripts under a parent span.

    Each sub-agent gets one ``atif.kind=agent`` wrapper span parented to
    ``root_span`` (or, when ``parent_resolver`` maps the sub-agent's spawning
    ``toolUseId`` to a known tool span, under that tool span); its turns are
    emitted as ``atif.step`` spans nested under that wrapper. Step spans end
    immediately (crash-safe export); the wrapper span is ended on
    :meth:`finalize_all` or when a workflow result is seen.

    Parenting is explicit (``set_span_in_context``) rather than ambient, so the
    emitter works correctly when driven from a separate asyncio task whose OTel
    context does not inherit the main loop's current span.
    """

    def __init__(
        self,
        emitter: ClaudeTranscriptEmitter,
        root_span: Span,
        *,
        expected_session_id: str | None = None,
        expected_cwd: str | None = None,
        parent_resolver: Callable[[dict[str, Any]], SpanContext | None] | None = None,
    ):
        self._emitter = emitter
        self._tracer = emitter.tracer
        self._root_span = root_span
        self._parent_resolver = parent_resolver
        self._states: dict[str, _SubagentState] = {}
        # Scope which transcripts we trace. A VM should only ever host one
        # Claude session at a time, but ``~/.claude/projects`` is global and an
        # mtime gate alone can replay a *different* run's recently-touched
        # transcript under this session's root span. We additionally match each
        # transcript's embedded ``sessionId`` (preferred) / ``cwd`` against the
        # current run. ``expected_session_id`` may be set after construction —
        # the main loop learns the Claude session id from the init event.
        self.expected_session_id = expected_session_id
        self.expected_cwd = expected_cwd

    def _record_matches(self, state: _SubagentState, record: Any) -> bool:
        """Decide whether a transcript belongs to the current run.

        Decision is cached on the state once a record carries an identifying
        field. With no scoping configured, everything matches (back-compat).
        """
        if state.matched is not None:
            return state.matched
        if not self.expected_session_id and not self.expected_cwd:
            return True
        rec_session = record.get("sessionId") if isinstance(record, dict) else None
        rec_cwd = record.get("cwd") if isinstance(record, dict) else None
        if self.expected_session_id and rec_session:
            state.matched = rec_session == self.expected_session_id
            return state.matched
        if self.expected_cwd and rec_cwd:
            state.matched = rec_cwd == self.expected_cwd
            return state.matched
        # This record carried no identifier yet; allow it provisionally without
        # caching, so a later record can still decide.
        return True

    # -- span lifecycle ----------------------------------------------------

    def _ensure_state(self, transcript_path: Path) -> _SubagentState:
        key = str(transcript_path)
        state = self._states.get(key)
        if state is None:
            agent_id = agent_id_from_path(transcript_path)
            meta = read_subagent_meta(transcript_path)
            state = _SubagentState(transcript_path=transcript_path, agent_id=agent_id, meta=meta)
            self._states[key] = state
        return state

    def _parent_context(self, state: _SubagentState):
        """Context to parent this sub-agent's wrapper span under."""
        if self._parent_resolver is not None:
            span_context = self._parent_resolver(state.meta)
            if span_context is not None:
                return otel_trace.set_span_in_context(NonRecordingSpan(span_context))
        return otel_trace.set_span_in_context(self._root_span)

    def _open_agent_span(self, state: _SubagentState) -> Span:
        if state.span is not None:
            return state.span
        parent_ctx = self._parent_context(state)
        agent_type = state.meta.get("agentType") or "subagent"
        # Use start_span (not start_as_current_span): we never want this
        # long-lived wrapper span to become the *ambient* current span — it
        # would wrongly re-parent unrelated main-loop work for its entire
        # lifetime. We attach it as current only transiently in _emit_record.
        # Because start_span does not auto-end, finalize() must call span.end()
        # explicitly — otherwise the BatchSpanProcessor never exports it and
        # every child step orphans (the bug this replaced).
        #
        # Stamp start_time from the first transcript timestamp so the wrapper
        # sits at the sub-agent's real start, not the poller's read time.
        span = self._tracer.start_span(
            f"subagent.{agent_type}",
            context=parent_ctx,
            start_time=state.first_ts_ns,
        )
        span.set_attribute("atif.kind", "agent")
        span.set_attribute("atif.agent.name", agent_type)
        span.set_attribute("plato.subagent.id", state.agent_id)
        span.set_attribute("plato.subagent.agent_type", agent_type)
        description = state.meta.get("description")
        if isinstance(description, str) and description:
            span.set_attribute("plato.subagent.description", description)
        tool_use_id = state.meta.get("toolUseId")
        if isinstance(tool_use_id, str) and tool_use_id:
            # Correlates this sub-agent back to the spawning Task tool call in
            # the parent transcript.
            span.set_attribute("plato.subagent.tool_use_id", tool_use_id)
        state.span = span
        return span

    def _emit_record(self, state: _SubagentState, event: dict[str, Any]) -> None:
        """Emit one normalized transcript record as nested step span(s)."""
        ts_ns = parse_timestamp_ns(event)
        if ts_ns is not None:
            if state.first_ts_ns is None:
                state.first_ts_ns = ts_ns
            state.last_ts_ns = ts_ns
        agent_span = self._open_agent_span(state)
        # Attach the wrapper span as the current context so the step spans the
        # reused block parser opens nest under it.
        token = otel_context.attach(otel_trace.set_span_in_context(agent_span))
        try:
            self._emitter.emit_event(
                event,
                state.pending_tool_calls,
                state.step_counter,
            )
        finally:
            otel_context.detach(token)

    # -- public feed API ---------------------------------------------------

    def feed_record(self, transcript_path: Path, record: Any) -> bool:
        """Feed one parsed transcript record. Returns True if it produced a step."""
        state = self._ensure_state(transcript_path)
        if not self._record_matches(state, record):
            return False
        event = normalize_transcript_record(record)
        if event is None:
            return False
        self._emit_record(state, event)
        return True

    def finalize(self, transcript_path: Path, result_text: str | None = None) -> None:
        """End the wrapper span for one sub-agent, optionally tagging its result."""
        state = self._states.get(str(transcript_path))
        if state is None or state.finalized:
            return
        if state.span is not None:
            if result_text:
                state.span.set_attribute("plato.subagent.result", result_text)
            # start_span does not auto-end; end explicitly so the span is
            # queued for export and its children nest under it. End at the last
            # transcript timestamp so the wrapper's duration reflects the real
            # sub-agent run, not the gap until session teardown.
            state.span.end(end_time=state.last_ts_ns)
        state.finalized = True

    def finalize_all(self, results: dict[str, str] | None = None) -> None:
        """End every open wrapper span (call at session end)."""
        results = results or {}
        for state in list(self._states.values()):
            self.finalize(state.transcript_path, results.get(state.agent_id))

    # -- incremental file reading (used by the tailer) ---------------------

    def consume_new_lines(self, transcript_path: Path) -> int:
        """Read and emit any complete new lines appended to a transcript.

        Tracks a per-file byte offset so each call only parses bytes appended
        since the last call. Incomplete trailing bytes (no newline yet, or a
        record split mid-write across two reads) are held in ``leftover`` as
        raw bytes and reassembled on the next call — so nothing is lost or
        corrupted by a premature decode. Only a genuinely malformed
        newline-terminated line (bad UTF-8 or bad JSON) is dropped. Returns the
        number of records emitted.
        """
        state = self._ensure_state(transcript_path)
        try:
            with transcript_path.open("rb") as fh:
                fh.seek(state.byte_offset)
                chunk = fh.read()
                state.byte_offset = fh.tell()
        except OSError:
            logger.debug("Could not read sub-agent transcript %s", transcript_path, exc_info=True)
            return 0

        if not chunk:
            return 0

        buffer = state.leftover + chunk
        emitted = 0
        while b"\n" in buffer:
            raw, buffer = buffer.split(b"\n", 1)
            raw = raw.strip()
            if not raw:
                continue
            try:
                line = raw.decode("utf-8")
                record = json.loads(line)
            except (UnicodeDecodeError, json.JSONDecodeError):
                # A complete (newline-terminated) but malformed line — genuinely
                # corrupt, not a split write; drop it.
                continue
            if self.feed_record(transcript_path, record):
                emitted += 1
        state.leftover = buffer
        return emitted


async def tail_subagents(
    emitter: SubagentTraceEmitter,
    projects_base: Path,
    *,
    started_at: float,
    stop_event: asyncio.Event,
    poll_interval: float = 1.0,
    mtime_slack: float = 5.0,
) -> None:
    """Poll ``projects_base`` for sub-agent transcripts and emit spans live.

    Each tick rglobs for ``agent-*.jsonl`` modified at/after this session
    started (``mtime_slack`` guards clock skew / pre-touch), then consumes only
    the bytes appended since the last tick. Cheap: a directory walk plus a
    short ``read()`` of the delta per active file. Runs until ``stop_event`` is
    set, then does one final drain so the tail end of each transcript is
    captured even if the agent exited between ticks.

    Never raises: transcript IO is best-effort observability, not core agent
    behavior, so all errors are swallowed and logged.
    """
    cutoff = started_at - mtime_slack

    def _scan() -> None:
        for path in projects_base.rglob(_AGENT_GLOB):
            try:
                if path.stat().st_mtime < cutoff:
                    continue
            except OSError:
                continue
            try:
                emitter.consume_new_lines(path)
            except Exception:
                logger.debug("Sub-agent tail failed for %s", path, exc_info=True)

    try:
        while not stop_event.is_set():
            _scan()
            try:
                await asyncio.wait_for(stop_event.wait(), timeout=poll_interval)
            except TimeoutError:
                pass
        # Final drain after the stop signal so no trailing lines are lost.
        _scan()
    except asyncio.CancelledError:
        # Best-effort final drain even on cancellation (e.g. process teardown).
        with suppress(Exception):
            _scan()
        raise
    finally:
        results: dict[str, str] = {}
        for journal in projects_base.rglob("journal.jsonl"):
            with suppress(Exception):
                results.update(read_workflow_journal(journal))
        emitter.finalize_all(results)
