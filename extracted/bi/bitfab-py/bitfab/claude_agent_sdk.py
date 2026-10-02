"""Claude Agent SDK handler for Bitfab tracing.

Hooks into the Claude Agent SDK's lifecycle to capture LLM turns,
tool invocations, and subagent execution as Bitfab spans.

Uses two integration surfaces:
  1. SDK hooks (PreToolUse, PostToolUse, etc.) for tool/subagent lifecycle
  2. Stream wrapping for LLM turn capture from the message stream
"""

from __future__ import annotations

import logging
import uuid
from collections.abc import AsyncIterator
from typing import Any, Callable, TypedDict

from bitfab.constants import DEFAULT_SERVICE_URL
from bitfab.http import HttpClient
from bitfab.processor_payload import finalize_span_payload, finalize_trace_payload
from bitfab.serialize import to_json_safe, to_json_safe_report
from bitfab.span_origin import make_span_origin
from bitfab.timestamp import now_iso_timestamp

logger = logging.getLogger(__name__)

# Sentinel distinguishing "no input supplied" from an explicit input of None.
_UNSET = object()


class ActiveSpanContext(TypedDict):
    trace_id: str
    span_id: str


class _SpanInfo(TypedDict, total=False):
    id: str
    span_id: str
    trace_id: str
    parent_id: str | None
    started_at: str
    ended_at: str | None
    name: str
    type: str
    input: Any
    output: Any
    error: str | None
    contexts: list[dict[str, Any]]
    # Type names of input/output values that could only be captured as
    # placeholders (serialized at capture time to snapshot a mutable value).
    # Carried to the send boundary so finalize_span_payload can mark the span.
    dropped: list[str]


def _now_iso() -> str:
    return now_iso_timestamp()


def _safe_serialize(value: Any) -> Any:
    """Serialize a value to something JSON-safe.

    Delegates to the shared ``to_json_safe`` so the recurse-the-dump logic lives
    in exactly one place (see bitfab/serialize.py)."""
    return to_json_safe(value)


def _extract_content_blocks(content: Any) -> list[dict[str, Any]]:
    """Extract content blocks from an AssistantMessage's content list."""
    if not content:
        return []
    blocks = []
    for block in content:
        blocks.append(_safe_serialize(block))
    return blocks


def _as_token_count(value: Any) -> int | float | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return value
    return None


def _extract_usage(message: Any) -> dict[str, Any]:
    """Extract token usage from an AssistantMessage.

    Anthropic reports ``input_tokens`` as the NON-cached prompt tokens, with
    cache reads and cache writes counted separately. Bitfab's ``inputTokens``
    is the full prompt size (matching the LangGraph integration), so fold the
    cache buckets in. ``cacheReadTokens`` stays the cached subset, which the
    read side uses to back out the uncached portion (``tokenType=uncached``).
    """
    usage_info: dict[str, Any] = {}
    usage = getattr(message, "usage", None)
    if not usage:
        return usage_info

    if isinstance(usage, dict):
        raw = usage
    elif hasattr(usage, "__dict__"):
        raw = usage.__dict__
    else:
        return usage_info

    base_input = _as_token_count(raw.get("input_tokens"))
    cache_read = _as_token_count(raw.get("cache_read_input_tokens"))
    cache_creation = _as_token_count(raw.get("cache_creation_input_tokens"))
    if base_input is not None or cache_read is not None or cache_creation is not None:
        usage_info["inputTokens"] = (
            (base_input or 0) + (cache_read or 0) + (cache_creation or 0)
        )

    output = _as_token_count(raw.get("output_tokens"))
    if output is not None:
        usage_info["outputTokens"] = output
    if cache_read is not None:
        usage_info["cacheReadTokens"] = cache_read
    if cache_creation is not None:
        usage_info["cacheCreationTokens"] = cache_creation

    return usage_info


class BitfabClaudeAgentHandler:
    """Claude Agent SDK handler that sends traces to Bitfab.

    Captures LLM turns, tool invocations, and subagent execution as
    Bitfab spans with proper parent-child hierarchy.

    Usage::

        from bitfab import Bitfab
        from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions

        bitfab = Bitfab(api_key="your-api-key")
        handler = bitfab.get_claude_agent_handler("my-agent")

        options = handler.instrument_options(
            ClaudeAgentOptions(model="claude-sonnet-4-5-...")
        )

        async with ClaudeSDKClient(options=options) as client:
            await client.query("Do something")
            async for message in handler.wrap_response(client.receive_response()):
                ...  # process messages normally

    Args:
        api_key: Bitfab API key for authentication
        trace_function_key: Groups traces under this key in Bitfab
        service_url: Base URL for the Bitfab service
        get_active_span_context: Optional callback that returns the active
            withSpan context for linking Claude Agent traces into an existing
            Bitfab trace tree.
    """

    def __init__(
        self,
        api_key: str,
        trace_function_key: str,
        service_url: str | None = None,
        get_active_span_context: Callable[[], ActiveSpanContext | None] | None = None,
        *,
        _http_client: HttpClient | None = None,
        _should_record: Callable[[], bool] | None = None,
    ):
        self._owns_http_client = _http_client is None
        self._http_client = _http_client or HttpClient(
            api_key=api_key, service_url=service_url or DEFAULT_SERVICE_URL
        )
        self._trace_function_key = trace_function_key
        self._get_active_span_context = get_active_span_context
        self._should_record = _should_record or (
            lambda: (self._http_client._resolve_api_key() or "").strip() != ""
        )

        self._run_to_span: dict[str, _SpanInfo] = {}
        self._trace_id: str | None = None
        self._root_span_id: str | None = None
        self._active_context: ActiveSpanContext | None = None
        self._trace_started_at: str | None = None

        # LLM turn tracking
        self._conversation_history: list[dict[str, Any]] = []
        self._pending_messages: list[dict[str, Any]] = []
        self._current_llm_span_id: str | None = None
        self._current_llm_message_id: str | None = None
        self._current_llm_content: list[dict[str, Any]] = []
        self._current_llm_model: str | None = None
        self._current_llm_usage: dict[str, Any] = {}
        self._current_llm_started_at: str | None = None
        self._current_llm_history_snapshot: list[dict[str, Any]] = []

        # Subagent tracking
        self._active_subagent_spans: dict[str, str] = {}

        # Synthetic root span (handler-only replay). When an ``input`` is passed
        # to wrap_query/wrap_response, the handler emits a root ``agent`` span
        # carrying that input, so a handler-instrumented run is replayable
        # WITHOUT an enclosing ``@bitfab.span`` - matching the LangGraph handler,
        # which records the graph input as its root. The prompt is not present
        # anywhere in the message stream, so it must be passed in explicitly.
        self._has_root_input = False
        self._root_input: Any = None
        self._root_output: Any = None

    # ── trace lifecycle ──────────────────────────────────────────

    def close(self, timeout: float = 30.0) -> bool:
        """Flush this handler and close resources it created."""
        if self._owns_http_client:
            return self._http_client.close(timeout)
        return self._http_client.wait_for_pending_requests(timeout)

    def __enter__(self) -> BitfabClaudeAgentHandler:
        return self

    def __exit__(self, _exc_type: Any, _exc: Any, _traceback: Any) -> None:
        self.close()

    def _ensure_trace(self) -> str:
        """Initialize the trace if not yet started. Returns trace_id."""
        if self._trace_id is not None:
            return self._trace_id

        self._active_context = (
            self._get_active_span_context()
            if self._get_active_span_context is not None
            else None
        )

        if self._active_context is not None:
            self._trace_id = self._active_context["trace_id"]
        else:
            self._trace_id = str(uuid.uuid4())

        self._trace_started_at = _now_iso()
        return self._trace_id

    def _get_parent_id(self, agent_id: str | None = None) -> str | None:
        """Determine the parent span ID for a new span."""
        if agent_id and agent_id in self._active_subagent_spans:
            return self._active_subagent_spans[agent_id]
        # Prefer the synthetic root (handler-only mode) so every span nests
        # under it; fall back to the enclosing withSpan context. The two are
        # never both set - the synthetic root is only created when there is no
        # active context.
        if self._root_span_id is not None:
            return self._root_span_id
        if self._active_context is not None:
            return self._active_context["span_id"]
        return None

    def _maybe_start_root_span(self) -> None:
        """Emit the synthetic root ``agent`` span once, before any child spans.

        No-op unless an ``input`` was supplied AND there is no enclosing
        ``@bitfab.span`` (in which case that outer span is already the
        replayable root).
        """
        if not self._has_root_input or self._root_span_id is not None:
            return
        self._ensure_trace()
        if self._active_context is not None:
            return
        span_id = str(uuid.uuid4())
        self._start_span(
            span_id=span_id,
            name=self._trace_function_key,
            span_type="agent",
            input_data=self._root_input,
            parent_id=None,
        )
        self._root_span_id = span_id

    def _complete_root_span(self) -> None:
        if self._root_span_id is None:
            return
        span_id = self._root_span_id
        self._root_span_id = None
        self._complete_span(span_id, output=self._root_output)

    # ── span helpers (same pattern as langgraph.py) ──────────────

    def _start_span(
        self,
        span_id: str,
        name: str,
        span_type: str,
        input_data: Any = None,
        parent_id: str | None = None,
    ) -> _SpanInfo:
        trace_id = self._ensure_trace()

        # Serialize input now to snapshot it (tool input can mutate between
        # PreToolUse and PostToolUse), but keep the report so a lossy input is
        # still marked non-replayable at the send boundary.
        safe_input, input_dropped = to_json_safe_report(input_data)

        span_info: _SpanInfo = {
            "id": str(uuid.uuid4()),
            "span_id": span_id,
            "trace_id": trace_id,
            "parent_id": parent_id,
            "started_at": _now_iso(),
            "name": name,
            "type": span_type,
            "input": safe_input,
            "contexts": [],
        }
        if input_dropped:
            span_info["dropped"] = list(input_dropped)
        self._run_to_span[span_id] = span_info
        self._http_client.trace_completion.start(
            span_info["trace_id"], span_info["span_id"]
        )
        return span_info

    def _complete_span(
        self,
        span_id: str,
        output: Any = None,
        error: str | None = None,
        extra_contexts: dict[str, Any] | None = None,
    ) -> None:
        span_info = self._run_to_span.pop(span_id, None)
        if span_info is None:
            return

        span_info["ended_at"] = _now_iso()
        safe_output, output_dropped = to_json_safe_report(output)
        span_info["output"] = safe_output
        if output_dropped:
            span_info["dropped"] = [*span_info.get("dropped", []), *output_dropped]
        if error is not None:
            span_info["error"] = error

        if extra_contexts:
            span_info.setdefault("contexts", []).append(extra_contexts)

        self._send_span(span_info)

        self._http_client.trace_completion.end(
            span_info["trace_id"], span_info["span_id"]
        )

    def _send_span(self, span_info: _SpanInfo) -> None:
        if not self._should_record():
            return
        span_data: dict[str, Any] = {
            "name": span_info.get("name", ""),
            "type": span_info.get("type", "custom"),
        }
        if span_info.get("input") is not None:
            span_data["input"] = span_info["input"]
        if span_info.get("output") is not None:
            span_data["output"] = span_info["output"]
        if span_info.get("error") is not None:
            span_data["error"] = span_info["error"]
        if span_info.get("contexts"):
            span_data["contexts"] = span_info["contexts"]

        raw_span: dict[str, Any] = {
            "id": span_info["span_id"],
            "trace_id": span_info["trace_id"],
            "started_at": span_info["started_at"],
            "ended_at": span_info.get("ended_at", _now_iso()),
            "span_data": span_data,
            "span_origin": make_span_origin("claude-agent-sdk"),
        }
        if span_info.get("parent_id") is not None:
            raw_span["parent_id"] = span_info["parent_id"]

        payload: dict[str, Any] = {
            "id": span_info.get("id") or str(uuid.uuid4()),
            "traceId": span_info["trace_id"],
            "type": "sdk-function",
            "source": "python-sdk-claude-agent-sdk",
            "traceFunctionKey": self._trace_function_key,
            "sourceTraceId": span_info["trace_id"],
            "rawSpan": raw_span,
        }

        # Sanitize the whole span (a non-serializable value in any field is
        # dumped/stubbed, a lossy capture is marked) instead of a bare json.dumps
        # that drops the span on the first stray value. extra_dropped carries
        # losses from the capture-time input/output snapshot above.
        payload = finalize_span_payload(payload, extra_dropped=span_info.get("dropped"))

        try:
            self._http_client.send_external_span(payload)
        except Exception as e:
            logger.error(
                "Bitfab: Failed to send Claude Agent span: %s", e, exc_info=True
            )

    def _send_trace_completion(
        self,
        ended_at: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        if not self._should_record():
            return
        if self._trace_id is None:
            return

        completed = self._active_context is None
        trace_id = self._trace_id

        # Mark as sent so the finally block doesn't re-send
        self._trace_id = None

        trace_data: dict[str, Any] = {
            "id": trace_id,
            "type": "sdk-function",
            "source": "python-sdk-claude-agent-sdk",
            "traceFunctionKey": self._trace_function_key,
            "externalTrace": {
                "id": trace_id,
                "started_at": self._trace_started_at or _now_iso(),
                "ended_at": ended_at or _now_iso(),
            },
            "completed": completed,
        }

        if metadata:
            trace_data["externalTrace"]["metadata"] = metadata

        # Sanitize the whole trace (warning when the capture was lossy) instead
        # of a bare json.dumps that drops the trace on the first stray value.
        trace_data = finalize_trace_payload(trace_data, logger)

        try:
            self._http_client.send_external_trace(trace_data)
        except Exception as e:
            logger.error(
                "Bitfab: Failed to send Claude Agent trace: %s", e, exc_info=True
            )

    # ── hook callbacks ───────────────────────────────────────────

    async def _pre_tool_use_hook(
        self,
        input_data: dict[str, Any],
        tool_use_id: str | None,
        context: Any,
    ) -> dict[str, Any]:
        try:
            sid = input_data.get("tool_use_id", tool_use_id or str(uuid.uuid4()))
            tool_name = input_data.get("tool_name", "tool")
            tool_input = input_data.get("tool_input", {})
            agent_id = input_data.get("agent_id")
            parent_id = self._get_parent_id(agent_id)

            self._start_span(
                span_id=sid,
                name=tool_name,
                span_type="function",
                input_data=tool_input,
                parent_id=parent_id,
            )
        except Exception:
            logger.debug("Bitfab: Error in _pre_tool_use_hook", exc_info=True)
        return {}

    async def _post_tool_use_hook(
        self,
        input_data: dict[str, Any],
        tool_use_id: str | None,
        context: Any,
    ) -> dict[str, Any]:
        try:
            sid = input_data.get("tool_use_id", tool_use_id or "")
            tool_response = input_data.get("tool_response")
            self._complete_span(sid, output=tool_response)
        except Exception:
            logger.debug("Bitfab: Error in _post_tool_use_hook", exc_info=True)
        return {}

    async def _post_tool_use_failure_hook(
        self,
        input_data: dict[str, Any],
        tool_use_id: str | None,
        context: Any,
    ) -> dict[str, Any]:
        try:
            sid = input_data.get("tool_use_id", tool_use_id or "")
            error = input_data.get("error", "Unknown error")
            self._complete_span(sid, error=str(error))
        except Exception:
            logger.debug("Bitfab: Error in _post_tool_use_failure_hook", exc_info=True)
        return {}

    async def _subagent_start_hook(
        self,
        input_data: dict[str, Any],
        tool_use_id: str | None,
        context: Any,
    ) -> dict[str, Any]:
        try:
            agent_id = input_data.get("agent_id", str(uuid.uuid4()))
            agent_type = input_data.get("agent_type", "subagent")
            parent_id = self._get_parent_id()

            span_id = str(uuid.uuid4())
            self._active_subagent_spans[agent_id] = span_id

            self._start_span(
                span_id=span_id,
                name=f"Agent: {agent_type}",
                span_type="agent",
                parent_id=parent_id,
            )
        except Exception:
            logger.debug("Bitfab: Error in _subagent_start_hook", exc_info=True)
        return {}

    async def _subagent_stop_hook(
        self,
        input_data: dict[str, Any],
        tool_use_id: str | None,
        context: Any,
    ) -> dict[str, Any]:
        try:
            agent_id = input_data.get("agent_id", "")
            span_id = self._active_subagent_spans.pop(agent_id, None)
            if span_id:
                self._complete_span(span_id)
        except Exception:
            logger.debug("Bitfab: Error in _subagent_stop_hook", exc_info=True)
        return {}

    # ── public API ───────────────────────────────────────────────

    def instrument_options(self, options: Any) -> Any:
        """Inject Bitfab tracing hooks into ClaudeAgentOptions.

        Modifies the options in-place and returns them for convenience.

        Args:
            options: A ClaudeAgentOptions instance (or any object with a
                ``hooks`` attribute that is a dict of hook event lists).

        Returns:
            The modified options object with Bitfab hooks injected.
        """
        try:
            from claude_agent_sdk import HookMatcher
        except ImportError as e:
            raise ImportError(
                "claude-agent-sdk is required for Claude Agent SDK tracing. "
                "Install it with: pip install 'bitfab-py[claude-agent-sdk]'"
            ) from e

        hooks = getattr(options, "hooks", None)
        if hooks is None:
            hooks = {}
            options.hooks = hooks

        hook_config = [
            ("PreToolUse", self._pre_tool_use_hook),
            ("PostToolUse", self._post_tool_use_hook),
            ("PostToolUseFailure", self._post_tool_use_failure_hook),
            ("SubagentStart", self._subagent_start_hook),
            ("SubagentStop", self._subagent_stop_hook),
        ]

        for event, callback in hook_config:
            if event not in hooks:
                hooks[event] = []
            hooks[event].append(HookMatcher(matcher=None, hooks=[callback]))

        return options

    async def wrap_response(
        self, stream: AsyncIterator[Any], input: Any = _UNSET
    ) -> AsyncIterator[Any]:
        """Wrap a ClaudeSDKClient.receive_response() stream to capture LLM turns.

        Yields every message unchanged while capturing AssistantMessage
        content as LLM turn spans.

        Args:
            stream: The async iterator from ``client.receive_response()``
            input: The prompt (or the serializable args that produced it).
                Pass it to record a replayable root span - see :meth:`wrap_query`.

        Yields:
            Each message from the stream, unmodified.
        """
        self._set_root_input(input)
        async for message in self._process_stream(stream):
            yield message

    async def wrap_query(
        self, stream: AsyncIterator[Any], input: Any = _UNSET
    ) -> AsyncIterator[Any]:
        """Wrap a ``query()`` async iterator to capture LLM turns.

        Tool and subagent spans are captured separately via the hooks injected
        by :meth:`instrument_options`.

        Args:
            stream: The async iterator from ``query(...)``
            input: The prompt (or the serializable args that produced it). Pass
                it to make a handler-only run replayable: the handler records a
                root ``agent`` span with that input, so ``replay(key, fn)`` can
                re-feed it. Omit it only when an enclosing ``@bitfab.span``
                already supplies the replayable root.

        Yields:
            Each message from the stream, unmodified.
        """
        self._set_root_input(input)
        async for message in self._process_stream(stream):
            yield message

    def _set_root_input(self, value: Any) -> None:
        # Set deterministically on every wrap call so a prior call's input can
        # never leak into a later input-less run on a reused handler (e.g. if
        # the earlier stream's iterator was abandoned mid-iteration, so
        # _reset_state never ran).
        if value is not _UNSET:
            self._has_root_input = True
            self._root_input = value
        else:
            self._has_root_input = False
            self._root_input = None
        self._root_output = None

    # ── stream processing ────────────────────────────────────────

    async def _process_stream(self, stream: AsyncIterator[Any]) -> AsyncIterator[Any]:
        """Core stream processing logic shared by wrap_response and wrap_query."""
        try:
            # Guarded: a failure starting the root span must never abort
            # consumption of the user's stream. Tracing is a side-channel.
            try:
                self._maybe_start_root_span()
            except Exception:
                logger.debug("Bitfab: Error starting root span", exc_info=True)
            async for message in stream:
                try:
                    self._process_message(message)
                except Exception:
                    logger.debug("Bitfab: Error processing message", exc_info=True)
                yield message
        finally:
            try:
                self._flush_llm_turn()
                self._complete_root_span()
                self._send_trace_completion()
            except Exception:
                logger.debug("Bitfab: Error in stream cleanup", exc_info=True)
            self._reset_state()

    def _process_message(self, message: Any) -> None:
        """Route a message to the appropriate handler based on its type."""
        type_name = type(message).__name__

        if type_name == "AssistantMessage":
            self._handle_assistant_message(message)
        elif type_name == "UserMessage":
            self._handle_user_message(message)
        elif type_name == "ResultMessage":
            self._handle_result_message(message)

    def _handle_assistant_message(self, message: Any) -> None:
        """Buffer assistant message content for LLM turn span creation."""
        self._ensure_trace()

        message_id = getattr(message, "message_id", None)

        if message_id != self._current_llm_message_id:
            self._flush_llm_turn()

            # Drain pending user/tool messages into history before snapshot
            self._conversation_history.extend(self._pending_messages)
            self._pending_messages.clear()

            self._current_llm_span_id = str(uuid.uuid4())
            self._current_llm_message_id = message_id
            self._current_llm_content = []
            self._current_llm_model = getattr(message, "model", None)
            self._current_llm_usage = {}
            self._current_llm_started_at = _now_iso()
            self._current_llm_history_snapshot = list(self._conversation_history)

        content = getattr(message, "content", None)
        if content:
            self._current_llm_content.extend(_extract_content_blocks(content))

        usage = _extract_usage(message)
        if usage:
            self._current_llm_usage.update(usage)

        model = getattr(message, "model", None)
        if model:
            self._current_llm_model = model

    def _handle_user_message(self, message: Any) -> None:
        """Buffer user message for later insertion into conversation history."""
        content = getattr(message, "content", None)
        tool_use_result = getattr(message, "tool_use_result", None)

        if tool_use_result is not None:
            self._pending_messages.append(
                {
                    "role": "tool",
                    "content": _safe_serialize(content),
                    "tool_result": _safe_serialize(tool_use_result),
                }
            )
        else:
            self._pending_messages.append(
                {
                    "role": "user",
                    "content": _safe_serialize(content),
                }
            )

    def _handle_result_message(self, message: Any) -> None:
        """Flush final LLM turn and send trace completion."""
        self._flush_llm_turn()

        # The final result text is the synthetic root span's output.
        result_text = getattr(message, "result", None)
        if result_text is not None:
            self._root_output = result_text
        self._complete_root_span()

        metadata: dict[str, Any] = {}
        for attr in (
            "num_turns",
            "total_cost_usd",
            "duration_ms",
            "duration_api_ms",
            "session_id",
        ):
            val = getattr(message, attr, None)
            if val is not None:
                metadata[attr] = val

        result_usage = getattr(message, "usage", None)
        if result_usage:
            if isinstance(result_usage, dict):
                metadata["usage"] = result_usage
            elif hasattr(result_usage, "__dict__"):
                metadata["usage"] = {
                    k: v
                    for k, v in result_usage.__dict__.items()
                    if not k.startswith("_")
                }

        self._send_trace_completion(metadata=metadata if metadata else None)

    def _flush_llm_turn(self) -> None:
        """Flush the buffered LLM turn as a span."""
        if self._current_llm_span_id is None:
            return

        span_id = self._current_llm_span_id
        trace_id = self._ensure_trace()
        parent_id = self._get_parent_id()

        llm_context: dict[str, Any] = {}
        if self._current_llm_model:
            llm_context["model"] = self._current_llm_model
        llm_context.update(self._current_llm_usage)

        span_info: _SpanInfo = {
            "id": str(uuid.uuid4()),
            "span_id": span_id,
            "trace_id": trace_id,
            "parent_id": parent_id,
            "started_at": self._current_llm_started_at or _now_iso(),
            "ended_at": _now_iso(),
            "name": self._current_llm_model or "llm",
            "type": "llm",
            "input": self._current_llm_history_snapshot,
            "output": self._current_llm_content,
            "contexts": [llm_context] if llm_context else [],
        }

        self._send_span(span_info)

        self._conversation_history.append(
            {
                "role": "assistant",
                "content": self._current_llm_content,
            }
        )

        self._current_llm_span_id = None
        self._current_llm_message_id = None
        self._current_llm_content = []
        self._current_llm_model = None
        self._current_llm_usage = {}
        self._current_llm_started_at = None
        self._current_llm_history_snapshot = []

    def _reset_state(self) -> None:
        """Reset all state after a conversation completes."""
        self._run_to_span.clear()
        self._trace_id = None
        self._root_span_id = None
        self._has_root_input = False
        self._root_input = None
        self._root_output = None
        self._active_context = None
        self._trace_started_at = None
        self._conversation_history.clear()
        self._pending_messages.clear()
        self._current_llm_span_id = None
        self._current_llm_message_id = None
        self._current_llm_content = []
        self._current_llm_model = None
        self._current_llm_usage = {}
        self._current_llm_started_at = None
        self._current_llm_history_snapshot = []
        self._active_subagent_spans.clear()
