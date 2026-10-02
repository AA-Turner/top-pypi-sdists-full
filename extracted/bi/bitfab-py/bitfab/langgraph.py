"""LangGraph/LangChain callback handler for Bitfab tracing.

Hooks into LangGraph's callback system to capture graph node execution,
LLM calls, and tool invocations as Bitfab spans, without requiring users
to decorate their functions with @span (which fails on non-serializable args).
"""

from __future__ import annotations

import logging
import uuid
from typing import TYPE_CHECKING, Any, Callable, TypedDict

from bitfab.constants import DEFAULT_SERVICE_URL
from bitfab.http import HttpClient
from bitfab.processor_payload import finalize_span_payload, finalize_trace_payload
from bitfab.serialize import to_json_safe_report
from bitfab.span_origin import make_span_origin
from bitfab.timestamp import now_iso_timestamp

if TYPE_CHECKING:
    from langchain_core.callbacks import BaseCallbackHandler
    from langchain_core.outputs import LLMResult
else:
    try:
        from langchain_core.callbacks import BaseCallbackHandler
    except ImportError:
        BaseCallbackHandler = object

logger = logging.getLogger(__name__)

_LANGGRAPH_METADATA_KEYS = (
    "langgraph_step",
    "langgraph_node",
    "langgraph_triggers",
    "langgraph_path",
    "langgraph_checkpoint_ns",
)

_LANGSMITH_HIDDEN_TAG = "langsmith:hidden"


class ActiveSpanContext(TypedDict):
    trace_id: str
    span_id: str


class _SpanInfo(TypedDict, total=False):
    id: str
    span_id: str
    trace_id: str
    root_run_id: str
    parent_id: str | None
    started_at: str
    ended_at: str | None
    name: str
    type: str
    input: Any
    output: Any
    error: str | None
    contexts: list[dict[str, Any]]
    model: str | None
    hidden: bool
    # Type names of input/output values that could only be captured as
    # placeholders (serialized at capture time to snapshot a mutable value).
    # Carried to the send boundary so finalize_span_payload can mark the span.
    dropped: list[str]


class _InvocationState(TypedDict):
    trace_id: str
    active_context: ActiveSpanContext | None
    root_run_id: str


def _now_iso() -> str:
    return now_iso_timestamp()


def _convert_message(message: Any) -> dict[str, Any]:
    """Convert a LangChain BaseMessage (or dict) to a role/content dict."""
    if isinstance(message, dict):
        return message

    if hasattr(message, "model_dump"):
        return message.model_dump()

    role_map = {
        "HumanMessage": "user",
        "AIMessage": "assistant",
        "SystemMessage": "system",
        "ToolMessage": "tool",
        "FunctionMessage": "function",
        "ChatMessage": None,
    }

    cls_name = type(message).__name__
    role = role_map.get(cls_name)
    if role is None:
        role = getattr(message, "role", "unknown")

    result: dict[str, Any] = {
        "role": role,
        "content": getattr(message, "content", str(message)),
    }

    tool_calls = getattr(message, "tool_calls", None)
    if tool_calls:
        result["tool_calls"] = tool_calls

    tool_call_id = getattr(message, "tool_call_id", None)
    if tool_call_id:
        result["tool_call_id"] = tool_call_id

    name = getattr(message, "name", None)
    if name:
        result["name"] = name

    return result


def _extract_model_name(
    serialized: dict[str, Any] | None,
    metadata: dict[str, Any] | None,
) -> str | None:
    """Extract model name from serialized dict or metadata."""
    if serialized:
        kwargs = serialized.get("kwargs", {})
        model = (
            kwargs.get("model_name") or kwargs.get("model") or kwargs.get("model_id")
        )
        if model:
            return str(model)

    if metadata:
        ls_model = metadata.get("ls_model_name")
        if ls_model:
            return str(ls_model)

    return None


_USAGE_KEYS = ("inputTokens", "outputTokens", "totalTokens", "cachedInputTokens")


def _as_token_count(value: Any) -> int | float | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return value
    return None


def _normalize_token_usage(raw: Any) -> dict[str, int | float | None] | None:
    """Normalize a provider-reported token-usage dict into Bitfab span fields.

    Handles, in priority order:
    - Anthropic native (``input_tokens`` EXCLUDES cache reads/creation, so
      they are added back to get the true prompt size)
    - OpenAI native (``prompt_tokens`` / ``completion_tokens``)
    - Google Gemini / Vertex native (``prompt_token_count`` /
      ``candidates_token_count``)
    - LangChain normalized ``usage_metadata`` (``input_tokens`` /
      ``output_tokens`` / ``total_tokens`` with
      ``input_token_details.cache_read``)

    Returns None when the value carries no recognizable token counts. Never
    estimates: only provider-reported numbers are returned.
    """
    if not isinstance(raw, dict) or not raw:
        return None

    # Anthropic native: input_tokens excludes cached reads and cache writes.
    if "cache_read_input_tokens" in raw or "cache_creation_input_tokens" in raw:
        cache_read = _as_token_count(raw.get("cache_read_input_tokens"))
        cache_creation = _as_token_count(raw.get("cache_creation_input_tokens"))
        base_input = _as_token_count(raw.get("input_tokens"))
        output_tokens = _as_token_count(raw.get("output_tokens"))
        if (
            cache_read is None
            and cache_creation is None
            and base_input is None
            and output_tokens is None
        ):
            return None
        input_tokens = (base_input or 0) + (cache_read or 0) + (cache_creation or 0)
        return {
            "inputTokens": input_tokens,
            "outputTokens": output_tokens,
            "totalTokens": input_tokens + (output_tokens or 0),
            "cachedInputTokens": cache_read,
        }

    # OpenAI native.
    if "prompt_tokens" in raw or "completion_tokens" in raw:
        prompt_details = raw.get("prompt_tokens_details") or {}
        cached = (
            _as_token_count(prompt_details.get("cached_tokens"))
            if isinstance(prompt_details, dict)
            else None
        )
        return _with_any_token_count(
            {
                "inputTokens": _as_token_count(raw.get("prompt_tokens")),
                "outputTokens": _as_token_count(raw.get("completion_tokens")),
                "totalTokens": _as_token_count(raw.get("total_tokens")),
                "cachedInputTokens": cached,
            }
        )

    # Google Gemini / Vertex native.
    if "prompt_token_count" in raw or "candidates_token_count" in raw:
        return _with_any_token_count(
            {
                "inputTokens": _as_token_count(raw.get("prompt_token_count")),
                "outputTokens": _as_token_count(raw.get("candidates_token_count")),
                "totalTokens": _as_token_count(raw.get("total_token_count")),
                "cachedInputTokens": _as_token_count(
                    raw.get("cached_content_token_count")
                ),
            }
        )

    # LangChain normalized usage_metadata (also plain Anthropic without cache
    # keys).
    if "input_tokens" in raw or "output_tokens" in raw:
        input_details = raw.get("input_token_details") or {}
        cached = (
            _as_token_count(input_details.get("cache_read"))
            if isinstance(input_details, dict)
            else None
        )
        input_tokens = _as_token_count(raw.get("input_tokens"))
        output_tokens = _as_token_count(raw.get("output_tokens"))
        total_tokens = _as_token_count(raw.get("total_tokens"))
        if (
            total_tokens is None
            and input_tokens is not None
            and output_tokens is not None
        ):
            total_tokens = input_tokens + output_tokens
        return _with_any_token_count(
            {
                "inputTokens": input_tokens,
                "outputTokens": output_tokens,
                "totalTokens": total_tokens,
                "cachedInputTokens": cached,
            }
        )

    return None


def _with_any_token_count(
    usage: dict[str, int | float | None],
) -> dict[str, int | float | None] | None:
    """Treat a recognizable usage shape with no numeric values as no usage.

    Returning None lets extraction fall through to the next source
    (response_metadata, then legacy llm_output) instead of blocking it.
    """
    if any(usage[key] is not None for key in _USAGE_KEYS):
        return usage
    return None


def _get_field(obj: Any, name: str) -> Any:
    if isinstance(obj, dict):
        return obj.get(name)
    return getattr(obj, name, None)


def _usage_from_generations(generations: Any) -> dict[str, int | float | None] | None:
    """Extract usage from each generation's message.

    Prefers the standardized ``usage_metadata`` (set by modern LangChain chat
    models, including the final aggregated chunk of streaming runs), falling
    back to provider-native ``response_metadata``. Sums across generations
    when a result has several.
    """
    if not generations:
        return None

    totals: dict[str, int | float | None] = {key: None for key in _USAGE_KEYS}
    found = False
    for batch in generations:
        if not isinstance(batch, (list, tuple)):
            continue
        for gen in batch:
            message = _get_field(gen, "message")
            if message is None:
                continue
            usage = _normalize_token_usage(_get_field(message, "usage_metadata"))
            if usage is None:
                response_metadata = _get_field(message, "response_metadata")
                if isinstance(response_metadata, dict):
                    usage = _normalize_token_usage(
                        response_metadata.get("token_usage")
                    ) or _normalize_token_usage(response_metadata.get("usage"))
            if usage is None:
                continue
            found = True
            for key in _USAGE_KEYS:
                value = usage.get(key)
                if value is not None:
                    totals[key] = (totals[key] or 0) + value

    return totals if found else None


def _extract_usage(response: Any) -> dict[str, Any]:
    """Extract token usage from an LLMResult.

    Resolution order: per-generation ``message.usage_metadata`` (normalized,
    provider-agnostic), then ``message.response_metadata`` token usage, then
    the legacy ``llm_output.token_usage`` / ``usage`` location. Fields with no
    provider-reported value are omitted; nothing is ever estimated.
    """
    normalized = _usage_from_generations(getattr(response, "generations", None))

    if normalized is None:
        llm_output = getattr(response, "llm_output", None)
        if isinstance(llm_output, dict):
            normalized = _normalize_token_usage(
                llm_output.get("token_usage")
            ) or _normalize_token_usage(llm_output.get("usage"))

    usage: dict[str, Any] = {}
    if not normalized:
        return usage
    for key in _USAGE_KEYS:
        if normalized.get(key) is not None:
            usage[key] = normalized[key]

    return usage


def _extract_langgraph_metadata(metadata: dict[str, Any] | None) -> dict[str, Any]:
    """Extract LangGraph-specific metadata keys."""
    if not metadata:
        return {}
    return {k: metadata[k] for k in _LANGGRAPH_METADATA_KEYS if k in metadata}


class BitfabLangGraphCallbackHandler(BaseCallbackHandler):
    """LangChain/LangGraph callback handler that sends traces to Bitfab.

    Captures graph node execution, LLM calls, and tool invocations as
    Bitfab spans with proper parent-child hierarchy.

    Usage::

        from bitfab import Bitfab

        bitfab = Bitfab(api_key="your-api-key")
        handler = bitfab.get_langgraph_callback_handler("my-agent")

        result = agent.invoke(
            {"messages": [...]},
            config={"callbacks": [handler]},
        )

    Args:
        api_key: Bitfab API key for authentication
        trace_function_key: Groups traces under this key in Bitfab
        service_url: Base URL for the Bitfab service
        get_active_span_context: Optional callback that returns the active
            withSpan context for linking LangGraph traces into an existing
            Bitfab trace tree.
    """

    ignore_retry = True
    # Retriever callbacks ARE captured (retriever queries -> function spans).
    ignore_retriever = False
    ignore_custom_event = True

    def __init__(
        self,
        api_key: str,
        trace_function_key: str,
        service_url: str | None = None,
        get_active_span_context: Callable[[], ActiveSpanContext | None] | None = None,
        capture_tools: bool = True,
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
        self._capture_tools = capture_tools
        self._should_record = _should_record or (
            lambda: (self._http_client._resolve_api_key() or "").strip() != ""
        )

        self._run_to_span: dict[str, _SpanInfo] = {}
        self._invocations: dict[str, _InvocationState] = {}

    # ── lifecycle helpers ──────────────────────────────────────────

    def close(self, timeout: float = 30.0) -> bool:
        """Flush this handler and close resources it created."""
        if self._owns_http_client:
            return self._http_client.close(timeout)
        return self._http_client.wait_for_pending_requests(timeout)

    def __enter__(self) -> BitfabLangGraphCallbackHandler:
        return self

    def __exit__(self, _exc_type: Any, _exc: Any, _traceback: Any) -> None:
        self.close()

    def _get_active_context(self) -> ActiveSpanContext | None:
        if self._get_active_span_context is None:
            return None
        return self._get_active_span_context()

    def _create_root_invocation(self, run_id: str) -> _InvocationState:
        active_context = self._get_active_context()
        invocation = {
            "trace_id": active_context["trace_id"]
            if active_context is not None
            else str(uuid.uuid4()),
            "active_context": active_context,
            "root_run_id": run_id,
        }
        self._invocations[run_id] = invocation
        return invocation

    def _get_or_create_parent_invocation(
        self, parent_span: _SpanInfo
    ) -> _InvocationState:
        root_run_id = parent_span["root_run_id"]
        invocation = self._invocations.get(root_run_id)
        if invocation is not None:
            return invocation

        invocation = {
            "trace_id": parent_span["trace_id"],
            "active_context": None,
            "root_run_id": root_run_id,
        }
        self._invocations[root_run_id] = invocation
        return invocation

    def _resolve_visible_parent_span(self, parent_span: _SpanInfo) -> _SpanInfo | None:
        resolved: _SpanInfo | None = parent_span
        while resolved is not None and resolved.get("hidden") is True:
            parent_id = resolved.get("parent_id")
            resolved = self._run_to_span.get(parent_id) if parent_id else None
        return resolved

    def _get_active_parent_id(self, invocation: _InvocationState) -> str | None:
        active_context = invocation.get("active_context")
        if active_context is None:
            return None
        return active_context["span_id"]

    def _resolve_parent_id(
        self,
        parent_span: _SpanInfo | None,
        parent_run_id: str | None,
        invocation: _InvocationState,
        will_hide: bool,
    ) -> str | None:
        if parent_span is None:
            return self._get_active_parent_id(invocation)

        if will_hide:
            return parent_run_id

        # Hidden callbacks stay local for parent resolution. Walk visible spans
        # to the nearest submitted ancestor so the stored tree has no orphan.
        resolved_parent = self._resolve_visible_parent_span(parent_span)
        if resolved_parent is not None:
            return resolved_parent["span_id"]

        return self._get_active_parent_id(invocation)

    def _build_span_info(
        self,
        run_id: str,
        invocation: _InvocationState,
        parent_id: str | None,
        name: str,
        span_type: str,
        input_data: Any,
        metadata: dict[str, Any] | None,
        will_hide: bool,
    ) -> _SpanInfo:
        lg_metadata = _extract_langgraph_metadata(metadata)
        contexts: list[dict[str, Any]] = [lg_metadata] if lg_metadata else []

        # Serialize input now to snapshot it (the input dict can mutate between
        # span start and send), but keep the report so a lossy input is still
        # marked non-replayable at the send boundary.
        safe_input, input_dropped = to_json_safe_report(input_data)

        span_info: _SpanInfo = {
            "id": str(uuid.uuid4()),
            "span_id": run_id,
            "trace_id": invocation["trace_id"],
            "root_run_id": invocation["root_run_id"],
            "parent_id": parent_id,
            "started_at": _now_iso(),
            "name": name,
            "type": span_type,
            "input": safe_input,
            "contexts": contexts,
        }
        if input_dropped:
            span_info["dropped"] = list(input_dropped)
        if will_hide:
            span_info["hidden"] = True
        return span_info

    def _build_trace_payload(
        self,
        root_span: _SpanInfo,
        *,
        completed: bool,
    ) -> dict[str, Any]:
        external_trace: dict[str, Any] = {
            "id": root_span["trace_id"],
            "started_at": root_span["started_at"],
        }
        if completed:
            external_trace["ended_at"] = root_span.get("ended_at", _now_iso())

        return {
            "id": root_span["trace_id"],
            "type": "sdk-function",
            "source": "python-sdk-langgraph",
            "traceFunctionKey": self._trace_function_key,
            "externalTrace": external_trace,
            "completed": completed,
        }

    def _start_span(
        self,
        run_id: str,
        parent_run_id: str | None,
        name: str,
        span_type: str,
        input_data: Any = None,
        metadata: dict[str, Any] | None = None,
        tags: list[str] | None = None,
    ) -> _SpanInfo:
        """Register a new span and return its info dict.

        State is scoped per-invocation (keyed by root run_id) so one handler
        instance can safely be reused across concurrent ``.invoke()`` calls,
        which is the documented LangGraph pattern. Any event whose parent we
        don't already track is treated as the root of a new invocation; this
        handles both top-level roots and LangGraph's Pregel-internal root
        scheduler (which doesn't emit a callback of its own).
        """
        parent_span = self._run_to_span.get(parent_run_id) if parent_run_id else None
        will_hide = tags is not None and _LANGSMITH_HIDDEN_TAG in tags
        is_root_invocation = parent_span is None
        invocation = (
            self._create_root_invocation(run_id)
            if is_root_invocation
            else self._get_or_create_parent_invocation(parent_span)
        )
        effective_parent_id = self._resolve_parent_id(
            parent_span=parent_span,
            parent_run_id=parent_run_id,
            invocation=invocation,
            will_hide=will_hide,
        )
        span_info = self._build_span_info(
            run_id=run_id,
            invocation=invocation,
            parent_id=effective_parent_id,
            name=name,
            span_type=span_type,
            input_data=input_data,
            metadata=metadata,
            will_hide=will_hide,
        )
        self._run_to_span[run_id] = span_info
        if span_info.get("hidden") is not True:
            self._http_client.trace_completion.start(
                span_info["trace_id"], span_info["span_id"]
            )

        if is_root_invocation:
            self._send_trace_start(span_info)

        return span_info

    def _complete_span(
        self,
        run_id: str,
        output: Any = None,
        error: str | None = None,
        extra_contexts: dict[str, Any] | None = None,
    ) -> None:
        """Finalize and send a span."""
        span_info = self._run_to_span.pop(run_id, None)
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

        if span_info.get("hidden") is not True:
            self._send_span(span_info)

        if run_id == span_info.get("root_run_id"):
            invocation = self._invocations.pop(run_id, None)
            active_context = (
                invocation["active_context"] if invocation is not None else None
            )
            self._send_trace_completion(span_info, active_context)

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
            "span_origin": make_span_origin("langgraph"),
        }
        if span_info.get("parent_id") is not None:
            raw_span["parent_id"] = span_info["parent_id"]

        payload: dict[str, Any] = {
            "id": span_info.get("id") or str(uuid.uuid4()),
            "traceId": span_info["trace_id"],
            "type": "sdk-function",
            "source": "python-sdk-langgraph",
            "traceFunctionKey": self._trace_function_key,
            "sourceTraceId": span_info["trace_id"],
            "rawSpan": raw_span,
        }

        payload = finalize_span_payload(payload, extra_dropped=span_info.get("dropped"))

        try:
            self._http_client.send_external_span(payload)
        except Exception as e:
            logger.error("Bitfab: Failed to send LangGraph span: %s", e, exc_info=True)

    def _send_trace_completion(
        self,
        root_span: _SpanInfo,
        active_context: ActiveSpanContext | None,
    ) -> None:
        """Send trace completion signal to Bitfab."""
        if not self._should_record():
            return
        trace_data = self._build_trace_payload(
            root_span,
            completed=active_context is None,
        )
        trace_data = finalize_trace_payload(trace_data, logger)

        try:
            self._http_client.send_external_trace(trace_data)
        except Exception as e:
            logger.error("Bitfab: Failed to send LangGraph trace: %s", e, exc_info=True)

    def _send_trace_start(self, root_span: _SpanInfo) -> None:
        """Register a LangGraph invocation as soon as its root is known."""
        if not self._should_record():
            return
        trace_data = self._build_trace_payload(root_span, completed=False)
        trace_data = finalize_trace_payload(trace_data, logger)

        try:
            self._http_client.send_external_trace(trace_data)
        except Exception as e:
            logger.error(
                "Bitfab: Failed to send LangGraph trace start: %s",
                e,
                exc_info=True,
            )

    # ── chain callbacks (graph nodes) ─────────────────────────────

    def on_chain_start(
        self,
        serialized: dict[str, Any],
        inputs: dict[str, Any],
        *,
        run_id: uuid.UUID,
        parent_run_id: uuid.UUID | None = None,
        tags: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        try:
            serialized = serialized or {}
            name = (
                kwargs.get("run_name")
                or kwargs.get("name")
                or serialized.get("name")
                or serialized.get("id", ["chain"])[-1]
            )
            self._start_span(
                run_id=str(run_id),
                parent_run_id=str(parent_run_id) if parent_run_id else None,
                name=str(name),
                span_type="agent",
                input_data=inputs,
                metadata=metadata,
                tags=tags,
            )
        except Exception:
            logger.debug("Bitfab: Error in on_chain_start", exc_info=True)

    def on_chain_end(
        self,
        outputs: dict[str, Any],
        *,
        run_id: uuid.UUID,
        parent_run_id: uuid.UUID | None = None,
        **kwargs: Any,
    ) -> None:
        try:
            self._complete_span(str(run_id), output=outputs)
        except Exception:
            logger.debug("Bitfab: Error in on_chain_end", exc_info=True)

    def on_chain_error(
        self,
        error: BaseException,
        *,
        run_id: uuid.UUID,
        parent_run_id: uuid.UUID | None = None,
        **kwargs: Any,
    ) -> None:
        try:
            if type(error).__name__ == "GraphBubbleUp":
                self._complete_span(str(run_id), output=None, error=None)
                return
            self._complete_span(str(run_id), output=None, error=repr(error))
        except Exception:
            logger.debug("Bitfab: Error in on_chain_error", exc_info=True)

    # ── LLM callbacks ─────────────────────────────────────────────

    def on_chat_model_start(
        self,
        serialized: dict[str, Any],
        messages: list[list[Any]],
        *,
        run_id: uuid.UUID,
        parent_run_id: uuid.UUID | None = None,
        tags: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        try:
            serialized = serialized or {}
            model = _extract_model_name(serialized, metadata)
            name = (
                kwargs.get("run_name")
                or kwargs.get("name")
                or model
                or serialized.get("id", ["llm"])[-1]
            )
            converted = [[_convert_message(m) for m in batch] for batch in messages]

            span_info = self._start_span(
                run_id=str(run_id),
                parent_run_id=str(parent_run_id) if parent_run_id else None,
                name=str(name),
                span_type="llm",
                input_data=converted,
                metadata=metadata,
                tags=tags,
            )
            span_info["model"] = model
        except Exception:
            logger.debug("Bitfab: Error in on_chat_model_start", exc_info=True)

    def on_llm_start(
        self,
        serialized: dict[str, Any],
        prompts: list[str],
        *,
        run_id: uuid.UUID,
        parent_run_id: uuid.UUID | None = None,
        tags: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        try:
            serialized = serialized or {}
            model = _extract_model_name(serialized, metadata)
            name = (
                kwargs.get("run_name")
                or kwargs.get("name")
                or model
                or serialized.get("id", ["llm"])[-1]
            )

            span_info = self._start_span(
                run_id=str(run_id),
                parent_run_id=str(parent_run_id) if parent_run_id else None,
                name=str(name),
                span_type="llm",
                input_data=prompts,
                metadata=metadata,
                tags=tags,
            )
            span_info["model"] = model
        except Exception:
            logger.debug("Bitfab: Error in on_llm_start", exc_info=True)

    def on_llm_end(
        self,
        response: LLMResult,
        *,
        run_id: uuid.UUID,
        parent_run_id: uuid.UUID | None = None,
        **kwargs: Any,
    ) -> None:
        try:
            output: Any = None
            generations = getattr(response, "generations", None)
            if generations and len(generations) > 0 and len(generations[-1]) > 0:
                gen = generations[-1][-1]
                msg = getattr(gen, "message", None)
                if msg is not None:
                    output = _convert_message(msg)
                else:
                    output = getattr(gen, "text", str(gen))

            usage = _extract_usage(response)
            span_info = self._run_to_span.get(str(run_id))
            model = span_info.get("model") if span_info else None

            llm_context: dict[str, Any] = {}
            if model:
                llm_context["model"] = model
            llm_context.update(usage)

            self._complete_span(
                str(run_id),
                output=output,
                extra_contexts=llm_context if llm_context else None,
            )
        except Exception:
            logger.debug("Bitfab: Error in on_llm_end", exc_info=True)

    def on_llm_error(
        self,
        error: BaseException,
        *,
        run_id: uuid.UUID,
        parent_run_id: uuid.UUID | None = None,
        **kwargs: Any,
    ) -> None:
        try:
            self._complete_span(str(run_id), output=None, error=repr(error))
        except Exception:
            logger.debug("Bitfab: Error in on_llm_error", exc_info=True)

    def on_llm_new_token(self, token: str, **kwargs: Any) -> None:
        pass

    # ── tool callbacks ────────────────────────────────────────────

    def on_tool_start(
        self,
        serialized: dict[str, Any],
        input_str: str,
        *,
        run_id: uuid.UUID,
        parent_run_id: uuid.UUID | None = None,
        tags: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
        inputs: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        if not self._capture_tools:
            return
        try:
            serialized = serialized or {}
            name = (
                kwargs.get("run_name")
                or kwargs.get("name")
                or serialized.get("name")
                or "tool"
            )
            self._start_span(
                run_id=str(run_id),
                parent_run_id=str(parent_run_id) if parent_run_id else None,
                name=str(name),
                span_type="function",
                input_data=inputs if inputs is not None else input_str,
                metadata=metadata,
                tags=tags,
            )
        except Exception:
            logger.debug("Bitfab: Error in on_tool_start", exc_info=True)

    def on_tool_end(
        self,
        output: Any,
        *,
        run_id: uuid.UUID,
        parent_run_id: uuid.UUID | None = None,
        **kwargs: Any,
    ) -> None:
        if not self._capture_tools:
            return
        try:
            self._complete_span(str(run_id), output=output)
        except Exception:
            logger.debug("Bitfab: Error in on_tool_end", exc_info=True)

    def on_tool_error(
        self,
        error: BaseException,
        *,
        run_id: uuid.UUID,
        parent_run_id: uuid.UUID | None = None,
        **kwargs: Any,
    ) -> None:
        if not self._capture_tools:
            return
        try:
            self._complete_span(str(run_id), output=None, error=repr(error))
        except Exception:
            logger.debug("Bitfab: Error in on_tool_error", exc_info=True)

    # ── retriever callbacks ───────────────────────────────────────

    def on_retriever_start(
        self,
        serialized: dict[str, Any],
        query: str,
        *,
        run_id: uuid.UUID,
        parent_run_id: uuid.UUID | None = None,
        tags: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        try:
            serialized = serialized or {}
            name = (
                kwargs.get("run_name")
                or kwargs.get("name")
                or serialized.get("name")
                or "retriever"
            )
            self._start_span(
                run_id=str(run_id),
                parent_run_id=str(parent_run_id) if parent_run_id else None,
                name=str(name),
                span_type="function",
                input_data=query,
                metadata=metadata,
                tags=tags,
            )
        except Exception:
            logger.debug("Bitfab: Error in on_retriever_start", exc_info=True)

    def on_retriever_end(
        self,
        documents: Any,
        *,
        run_id: uuid.UUID,
        parent_run_id: uuid.UUID | None = None,
        **kwargs: Any,
    ) -> None:
        try:
            self._complete_span(str(run_id), output=documents)
        except Exception:
            logger.debug("Bitfab: Error in on_retriever_end", exc_info=True)

    def on_retriever_error(
        self,
        error: BaseException,
        *,
        run_id: uuid.UUID,
        parent_run_id: uuid.UUID | None = None,
        **kwargs: Any,
    ) -> None:
        try:
            self._complete_span(str(run_id), output=None, error=repr(error))
        except Exception:
            logger.debug("Bitfab: Error in on_retriever_error", exc_info=True)


# LangChain chains and LangGraph graphs share the same callback system, so one
# handler serves both. Exported under both names.
BitfabLangChainCallbackHandler = BitfabLangGraphCallbackHandler
