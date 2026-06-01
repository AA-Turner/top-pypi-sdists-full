"""LangGraph-native callback handler (L3 framework binding).

Implements langchain_core.callbacks.BaseCallbackHandler directly — does
NOT inherit from AigieCallbackHandler. Composes Phase-1 shared helpers
(llm_metadata, execution_state, trace_finalization) for cross-framework
concerns. LangGraph-specific bits (langgraph_node/_step/_path extraction,
GraphInterrupt detection) live in this file.

Wire shape is constrained by:
- SpanComplete contract (sdk/aigie/tracing/types.py)
- Committed baselines under tests/unit/integrations/langgraph/baseline/

This callback MUST NOT emit any of the legacy metadata keys
(error_classification, error_detection, error_severity,
error_is_transient, status_message) and MUST NOT embed an error envelope
in span.output. Both are enforced by SpanEventHandler.
"""

from __future__ import annotations

import contextlib
from datetime import datetime, timezone
from typing import Any
from uuid import UUID

from langchain_core.callbacks import BaseCallbackHandler

from aigie.cost_tracking import UsageMetadata, calculate_cost
from aigie.integrations.langgraph.event_classifier import LangGraphEventClassifier
from aigie.tracing.event_classifier import EventKind, FrameworkEvent
from aigie.tracing.execution_state import ExecutionState
from aigie.tracing.llm_metadata import (
    extract_llm_params,
    extract_model_info,
    extract_prompt_content,
)
from aigie.tracing.span_event_handler import SpanEventHandler
from aigie.tracing.trace_finalization import finalize_trace
from aigie.tracing.trace_state import current_trace_id

# Keys that ``_extract_langgraph_metadata`` consumes (and that we therefore
# don't want passing through twice into the chain-span metadata).
_LG_META_KEYS = frozenset(
    {"langgraph_node", "langgraph_step", "langgraph_path", "node", "step", "graph_node", "path"}
)


def _extract_langgraph_metadata(  # noqa: C901, PLR0915 — multi-source (metadata + 3 tag patterns)
    *,
    metadata: dict[str, Any] | None,
    tags: list[Any] | None,
) -> dict[str, Any]:
    """Pull langgraph_node/langgraph_step/langgraph_path from metadata and tags.

    Matches the extraction in AigieCallbackHandler.on_llm_start L843-874.
    """
    out: dict[str, Any] = {}

    if metadata and isinstance(metadata, dict):
        node = metadata.get("langgraph_node") or metadata.get("node") or metadata.get("graph_node")
        step = metadata.get("langgraph_step") or metadata.get("step")
        path = metadata.get("langgraph_path") or metadata.get("path")
        if node:
            out["langgraph_node"] = node
        if step is not None:
            out["langgraph_step"] = step
        if path:
            out["langgraph_path"] = path

    if tags and isinstance(tags, list):
        for tag in tags:
            if not isinstance(tag, str):
                continue
            if tag.startswith(("graph:", "langgraph:")):
                parts = tag.split(":")
                if len(parts) >= 3 and parts[1] == "step":
                    out.setdefault("langgraph_node", parts[2])
            elif tag.startswith("seq:step:"):
                with contextlib.suppress(ValueError, IndexError):
                    out.setdefault("langgraph_step", int(tag.split(":")[2]))
            elif tag.startswith("node:"):
                out.setdefault("langgraph_node", tag.split(":", 1)[1])

    return out


def _passthrough_metadata(
    user_metadata: dict[str, Any] | None,
    lg_meta: dict[str, Any],
) -> dict[str, Any]:
    """Keep non-langgraph user metadata keys alongside our langgraph_* fields."""
    if not user_metadata:
        return lg_meta
    out = dict(lg_meta)
    for k, v in user_metadata.items():
        if k not in _LG_META_KEYS and k not in out:
            out[k] = v
    return out


def _normalize_usage(raw: Any) -> dict[str, int] | None:
    if raw is None:
        return None
    if isinstance(raw, dict):
        d = raw
    elif hasattr(raw, "prompt_tokens") or hasattr(raw, "input_tokens"):
        d = {
            "prompt_tokens": getattr(raw, "prompt_tokens", 0) or getattr(raw, "input_tokens", 0),
            "completion_tokens": (
                getattr(raw, "completion_tokens", 0) or getattr(raw, "output_tokens", 0)
            ),
            "total_tokens": getattr(raw, "total_tokens", 0),
        }
    else:
        return None
    prompt = d.get("prompt_tokens") or d.get("input_tokens") or 0
    completion = d.get("completion_tokens") or d.get("output_tokens") or 0
    total = d.get("total_tokens") or (prompt + completion)
    if prompt == 0 and completion == 0 and total == 0:
        return None
    return {
        "prompt_tokens": int(prompt),
        "completion_tokens": int(completion),
        "total_tokens": int(total),
    }


def _iter_usage_sources(response: Any):
    """Yield candidate usage payloads from every known LangChain location."""
    llm_output = getattr(response, "llm_output", None)
    if isinstance(llm_output, dict):
        yield llm_output.get("token_usage")
        yield llm_output.get("usage")
        rmeta = llm_output.get("response_metadata")
        if isinstance(rmeta, dict):
            yield rmeta.get("token_usage")
            yield rmeta.get("usage")
    try:
        gen = response.generations[0][0]
    except Exception:  # noqa: BLE001
        return
    gen_info = getattr(gen, "generation_info", None)
    if isinstance(gen_info, dict):
        yield gen_info.get("usage_metadata")
        yield gen_info.get("token_usage")
        yield gen_info.get("usage")
    msg = getattr(gen, "message", None)
    if msg is not None:
        yield getattr(msg, "usage_metadata", None)


def _extract_langchain_usage(response: Any) -> dict[str, int] | None:
    """Walk LangChain's LLMResult shape to find token usage.

    Token usage lands in many places depending on provider — `llm_output`
    (OpenAI/Anthropic via langchain_aws), nested `response_metadata`,
    `generation_info["usage_metadata"]` (modern LangChain), or
    `message.usage_metadata` (chat models with AIMessage).
    """
    for raw in _iter_usage_sources(response):
        found = _normalize_usage(raw)
        if found:
            return found
    return None


class LangGraphNativeCallback(BaseCallbackHandler):
    """BaseCallbackHandler that emits Kytte spans via a held SpanEventHandler."""

    # Class-level marker recognized by LangGraphLifecycle._already_tracing
    # when scanning config["callbacks"] for an existing handler. Beats
    # comparing __name__ strings (survives renames + identity stays correct
    # across reloads).
    _is_aigie_handler = True

    _WORKFLOW_RUN_ID = "__workflow__"

    def __init__(
        self,
        emitter: Any,
        workflow_name: str,
        classifier: Any = None,
        *,
        config: Any = None,
    ) -> None:
        BaseCallbackHandler.__init__(self)
        self.spans = SpanEventHandler(emitter=emitter, config=config)
        self._workflow_name = workflow_name
        self._execution = ExecutionState()
        self._classifier = classifier if classifier is not None else LangGraphEventClassifier()

    def _resolve_parent(self, parent_run_id: UUID | None) -> str | None:
        """Resolve a framework parent_run_id to a run_id we have open.

        LangGraph fires node-level on_chain_start with parent_run_id pointing
        at the outer Pregel wrapper — which we deliberately *filter* (so it
        never enters self.spans._open). Without redirection those children land as
        orphan root spans. When the framework parent can't be found but the
        workflow span is open, fall back to that so nodes attach to the run's
        root visually.
        """
        if parent_run_id is None:
            return None
        sid = str(parent_run_id)
        if self.spans.is_open(sid):
            return sid
        if self.spans.is_open(self._WORKFLOW_RUN_ID):
            return self._WORKFLOW_RUN_ID
        return None

    # ------------------------------------------------------------------
    # Chain events
    # ------------------------------------------------------------------

    def on_chain_start(
        self,
        serialized: dict[str, Any] | None,
        inputs: Any,
        *,
        run_id: UUID,
        parent_run_id: UUID | None = None,
        tags: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        # Modern LangChain passes serialized=None for most chains; the real
        # class/runnable name lives in kwargs["name"]. Fall back through
        # serialized fields for older versions where serialized was populated.
        kw_name = kwargs.get("name")
        ser_name = (serialized or {}).get("name") if serialized else None
        serialized_id = (serialized or {}).get("id")
        class_name = (
            serialized_id[-1] if isinstance(serialized_id, list) and serialized_id else None
        )
        resolved_name = kw_name or ser_name or class_name or ""

        kind = self._classifier.classify_chain_event(
            FrameworkEvent(
                name=resolved_name,
                parent_run_id=str(parent_run_id) if parent_run_id else None,
                framework_metadata=metadata or {},
                tags=tuple(tags or ()),
            )
        )
        if kind is EventKind.DROP:
            return
        lg_meta = _extract_langgraph_metadata(metadata=metadata, tags=tags)
        if kind is EventKind.SUBGRAPH_WORKFLOW:
            self._open_subgraph_workflow_span(run_id, parent_run_id, inputs, metadata, lg_meta)
            return
        name = resolved_name or lg_meta.get("langgraph_node") or "chain"
        self._open_chain_span(run_id, parent_run_id, name, inputs, metadata, lg_meta)

    def _open_chain_span(self, run_id, parent_run_id, name, inputs, metadata, lg_meta):
        merged = {"chain_type": "chain", **_passthrough_metadata(metadata, lg_meta)}
        self.spans.open_span(
            run_id=str(run_id),
            parent_run_id=self._resolve_parent(parent_run_id),
            name=name,
            span_type="chain",
            input=inputs,
            metadata=merged,
        )
        self._execution.start_span(name=name, span_type="chain", at=datetime.now(timezone.utc))

    def _open_subgraph_workflow_span(self, run_id, parent_run_id, inputs, metadata, lg_meta):
        sub_merged = {"chain_type": "workflow", **_passthrough_metadata(metadata, lg_meta)}
        self.spans.open_span(
            run_id=str(run_id),
            parent_run_id=self._resolve_parent(parent_run_id),
            name="top_workflow",
            span_type="workflow",
            input=inputs,
            metadata=sub_merged,
        )
        self._execution.start_span(
            name="top_workflow", span_type="workflow", at=datetime.now(timezone.utc)
        )

    def on_chain_end(
        self,
        outputs: Any,
        *,
        run_id: UUID,
        parent_run_id: UUID | None = None,
        **kwargs: Any,
    ) -> None:
        state = self.spans.get_state(str(run_id))
        name = state["name"] if state else "chain"
        self._execution.end_span(name=name, status="success", at=datetime.now(timezone.utc))
        self.spans.close_span(run_id=str(run_id), output=outputs)

    def on_chain_error(
        self,
        error: BaseException,
        *,
        run_id: UUID,
        parent_run_id: UUID | None = None,
        **kwargs: Any,
    ) -> None:
        state = self.spans.get_state(str(run_id))
        name = state["name"] if state else "chain"
        self._execution.end_span(
            name=name, status="error", at=datetime.now(timezone.utc), error_message=str(error)
        )
        self.spans.fail_span(run_id=str(run_id), error=error)

    # ------------------------------------------------------------------
    # LLM events
    # ------------------------------------------------------------------

    def on_llm_start(  # noqa: PLR0915 — composes 3 helpers + builds span input dict
        self,
        serialized: dict[str, Any] | None,
        prompts: list,
        *,
        run_id: UUID,
        parent_run_id: UUID | None = None,
        tags: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        invocation_params = kwargs.get("invocation_params") or {}
        model_info = extract_model_info(
            serialized=serialized,
            invocation_params=invocation_params,
            metadata=metadata,
        )
        system_prompt, message_dicts = extract_prompt_content(prompts)
        llm_params = extract_llm_params(invocation_params=invocation_params, kwargs=kwargs)
        lg_meta = _extract_langgraph_metadata(metadata=metadata, tags=tags)

        llm_input: dict[str, Any] = {
            "model": model_info.display_name,
            "prompts": message_dicts or prompts,
            "prompt_count": len(prompts) if prompts else 0,
        }
        if model_info.model_id:
            llm_input["model_id"] = model_info.model_id
        if system_prompt:
            llm_input["system_prompt"] = system_prompt
        if llm_params:
            llm_input["parameters"] = llm_params
        for k in ("langgraph_node", "langgraph_step", "langgraph_path"):
            if k in lg_meta:
                llm_input[k] = lg_meta[k]

        span_name = lg_meta.get("langgraph_node") or f"LLM: {model_info.display_name}"
        # Backend extracts `model`/`model_name`/`model_id` from metadata into
        # the spans table columns (see spans.model in agent_monitor schema).
        merged_metadata: dict[str, Any] = {
            **lg_meta,
            "model": model_info.display_name,
            "model_name": model_info.display_name,
        }
        if model_info.model_id:
            merged_metadata["model_id"] = model_info.model_id

        # Backend reads spans.model from the top-level wire field, not metadata.
        extras: dict[str, Any] = {"model": model_info.display_name}
        if model_info.model_id:
            extras["internal_model"] = model_info.display_name
            extras["internal_model_id"] = model_info.model_id
        self.spans.open_span(
            run_id=str(run_id),
            parent_run_id=self._resolve_parent(parent_run_id),
            name=span_name,
            span_type="llm",
            input=llm_input,
            metadata=merged_metadata,
            extras=extras,
        )
        self._execution.increment_turn()
        self._execution.start_span(name=span_name, span_type="llm", at=datetime.now(timezone.utc))

    def on_chat_model_start(
        self,
        serialized: dict[str, Any] | None,
        messages: list[list[Any]],
        *,
        run_id: UUID,
        parent_run_id: UUID | None = None,
        tags: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        flat_prompts = messages[0] if messages else []
        self.on_llm_start(
            serialized=serialized,
            prompts=flat_prompts,
            run_id=run_id,
            parent_run_id=parent_run_id,
            tags=tags,
            metadata=metadata,
            **kwargs,
        )

    def on_llm_end(
        self,
        response: Any,
        *,
        run_id: UUID,
        **kwargs: Any,
    ) -> None:
        sid = str(run_id)
        output = self._extract_response_text(response)
        state = self.spans.get_state(sid)
        if state is None:
            self.spans.close_span(run_id=sid, output=output)
            return
        extras, metadata_updates = self._build_llm_end_payload(response, state)
        self._execution.end_span(
            name=state["name"], status="success", at=datetime.now(timezone.utc)
        )
        self.spans.close_span(
            run_id=sid,
            output=output,
            extras=extras or None,
            metadata_updates=metadata_updates or None,
        )

    @staticmethod
    def _extract_response_text(response: Any) -> Any:
        try:
            return response.generations[0][0].text
        except Exception:  # noqa: BLE001
            return str(response)

    def _build_llm_end_payload(
        self, response: Any, state: dict[str, Any]
    ) -> tuple[dict[str, Any], dict[str, Any]]:
        md = state["metadata"]
        # LangChain wraps the LLM response as LLMResult; usage hides in
        # llm_output / generation_info / message.usage_metadata depending on
        # the provider. _extract_langchain_usage walks all known paths.
        usage = _extract_langchain_usage(response)
        cost = self._calculate_cost(usage, md.get("model_id") or md.get("model"))

        # Backend extracts spans.model from top-level wire fields; re-stamp
        # so the span_update payload carries the same values as span_create.
        extras: dict[str, Any] = {}
        if md.get("model"):
            extras["model"] = md["model"]
        if md.get("model_id"):
            extras["internal_model_id"] = md["model_id"]

        metadata_updates: dict[str, Any] = {}
        if usage is not None:
            metadata_updates.update(self._usage_to_metadata(usage, cost))
            if cost is not None:
                metadata_updates.update(cost)
            extras["prompt_tokens"] = usage["prompt_tokens"]
            extras["completion_tokens"] = usage["completion_tokens"]
            extras["total_tokens"] = usage["total_tokens"]
        return extras, metadata_updates

    @staticmethod
    def _usage_to_metadata(usage: dict[str, int], cost: dict[str, float] | None) -> dict[str, Any]:
        token_usage: dict[str, int | float] = {
            "prompt_tokens": usage["prompt_tokens"],
            "input_tokens": usage["prompt_tokens"],
            "completion_tokens": usage["completion_tokens"],
            "output_tokens": usage["completion_tokens"],
            "total_tokens": usage["total_tokens"],
        }
        if cost is not None:
            token_usage["input_cost"] = cost["input_cost"]
            token_usage["output_cost"] = cost["output_cost"]
            token_usage["estimated_cost"] = cost["total_cost"]
        return {
            "prompt_tokens": usage["prompt_tokens"],
            "completion_tokens": usage["completion_tokens"],
            "total_tokens": usage["total_tokens"],
            "token_usage": token_usage,
        }

    @staticmethod
    def _calculate_cost(
        usage: dict[str, int] | None, model_id: str | None
    ) -> dict[str, float] | None:
        """Compute input/output/total cost from token usage. Best-effort: returns
        None on failure (unknown model, computation error)."""
        if not usage or not model_id:
            return None
        try:
            breakdown = calculate_cost(
                UsageMetadata(
                    input_tokens=usage["prompt_tokens"],
                    output_tokens=usage["completion_tokens"],
                    total_tokens=usage["total_tokens"],
                ),
                model_override=model_id,
            )
        except Exception:  # noqa: BLE001
            return None
        if breakdown is None:
            return None
        return {
            "input_cost": float(getattr(breakdown, "input_cost", 0.0) or 0.0),
            "output_cost": float(getattr(breakdown, "output_cost", 0.0) or 0.0),
            "total_cost": float(getattr(breakdown, "total_cost", 0.0) or 0.0),
        }

    def on_llm_error(
        self,
        error: BaseException,
        *,
        run_id: UUID,
        **kwargs: Any,
    ) -> None:
        state = self.spans.get_state(str(run_id))
        if state:
            self._execution.end_span(
                name=state["name"],
                status="error",
                at=datetime.now(timezone.utc),
                error_message=str(error),
            )
        self.spans.fail_span(run_id=str(run_id), error=error)

    # ------------------------------------------------------------------
    # Tool events
    # ------------------------------------------------------------------

    def on_tool_start(
        self,
        serialized: dict[str, Any] | None,
        input_str: str,
        *,
        run_id: UUID,
        parent_run_id: UUID | None = None,
        tags: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        lg_meta = _extract_langgraph_metadata(metadata=metadata, tags=tags)
        name = (serialized or {}).get("name") or "tool"
        self.spans.open_span(
            run_id=str(run_id),
            parent_run_id=self._resolve_parent(parent_run_id),
            name=name,
            span_type="tool",
            input=input_str,
            metadata=lg_meta,
        )
        self._execution.start_span(name=name, span_type="tool", at=datetime.now(timezone.utc))

    def on_tool_end(
        self,
        output: Any,
        *,
        run_id: UUID,
        **kwargs: Any,
    ) -> None:
        self._execution.increment_tool_calls()
        state = self.spans.get_state(str(run_id))
        if state:
            self._execution.end_span(
                name=state["name"], status="success", at=datetime.now(timezone.utc)
            )
        self.spans.close_span(run_id=str(run_id), output=output)

    def on_tool_error(
        self,
        error: BaseException,
        *,
        run_id: UUID,
        **kwargs: Any,
    ) -> None:
        state = self.spans.get_state(str(run_id))
        if state:
            self._execution.end_span(
                name=state["name"],
                status="error",
                at=datetime.now(timezone.utc),
                error_message=str(error),
            )
        self.spans.fail_span(run_id=str(run_id), error=error)

    # ------------------------------------------------------------------
    # Workflow lifecycle (called by LangGraphLifecycle, not LangChain)
    # ------------------------------------------------------------------

    def open_workflow_span(self, *, input: Any) -> None:
        self.spans.open_span(
            run_id=self._WORKFLOW_RUN_ID,
            parent_run_id=None,
            name=self._workflow_name,
            span_type="workflow",
            input=input,
            metadata={"chain_type": "workflow"},
        )
        self._execution.start_span(
            name=self._workflow_name, span_type="workflow", at=datetime.now(timezone.utc)
        )

    def close_workflow_span(
        self, *, output: Any = None, error: BaseException | None = None
    ) -> None:
        now = datetime.now(timezone.utc)
        if error is not None:
            self._execution.end_span(
                name=self._workflow_name, status="error", at=now, error_message=str(error)
            )
            self.spans.fail_span(run_id=self._WORKFLOW_RUN_ID, error=error)
        else:
            self._execution.end_span(name=self._workflow_name, status="success", at=now)
            self.spans.close_span(run_id=self._WORKFLOW_RUN_ID, output=output)

    def finalize(self, *, error: BaseException | None) -> None:
        """Emit the trace_update marking the run complete."""
        trace_id = current_trace_id()
        if trace_id is None:
            return
        finalize_trace(
            emitter=self.spans.emitter,
            trace_id=trace_id,
            agent_name=self._workflow_name,
            execution_state=self._execution,
            trace_metadata={"framework": "langgraph", "type": "langgraph"},
            error=error,
        )
