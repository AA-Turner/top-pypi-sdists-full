"""LangGraph-native callback handler (L3 framework binding).

Implements langchain_core.callbacks.BaseCallbackHandler directly — does
NOT inherit from AigieCallbackHandler. Composes Phase-1 shared helpers
(llm_metadata, execution_state) for cross-framework
concerns. LangGraph-specific bits (langgraph_node/_step/_path extraction,
GraphInterrupt detection) live in this file.

Wire shape is constrained by:
- Span contract (sdk/aigie/tracing/types.py)
- Committed baselines under tests/unit/integrations/langgraph/baseline/

This callback MUST NOT emit any of the legacy metadata keys
(error_classification, error_detection, error_severity,
error_is_transient, status_message) and MUST NOT embed an error envelope
in span.output. Both are enforced by SpanEventHandler.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import UUID

from langchain_core.callbacks import BaseCallbackHandler

from aigie.integrations.langgraph.event_classifier import LangGraphEventClassifier
from aigie.tracing.event_classifier import EventKind, FrameworkEvent
from aigie.tracing.execution_state import ExecutionState
from aigie.tracing.llm_metadata import (
    extract_llm_params,
    extract_model_info,
    extract_prompt_content,
)
from aigie.tracing.span_event_handler import SpanEventHandler
from aigie.tracing.trace_state import current_trace_id

from aigie.integrations.langgraph._metadata import extract_langgraph_metadata, passthrough_metadata
from aigie.integrations.langgraph._usage import usage_payload


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
        lg_meta = extract_langgraph_metadata(metadata=metadata, tags=tags)
        if kind is EventKind.SUBGRAPH_WORKFLOW:
            self._open_subgraph_workflow_span(run_id, parent_run_id, inputs, metadata, lg_meta)
            return
        name = resolved_name or lg_meta.get("langgraph_node") or "chain"
        self._open_chain_span(run_id, parent_run_id, name, inputs, metadata, lg_meta)

    def _open_chain_span(self, run_id, parent_run_id, name, inputs, metadata, lg_meta):
        merged = {"chain_type": "chain", **passthrough_metadata(metadata, lg_meta)}
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
        sub_merged = {"chain_type": "workflow", **passthrough_metadata(metadata, lg_meta)}
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
        lg_meta = extract_langgraph_metadata(metadata=metadata, tags=tags)

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
        # Token/cost extraction + wire placement is owned by _usage.usage_payload
        # (which funnels through the shared Usage object). LangChain hides usage
        # in many provider-specific locations; that helper walks them all.
        extras, metadata_updates = usage_payload(response, md.get("model_id") or md.get("model"))

        # Backend extracts spans.model from top-level wire fields; re-stamp
        # so the span_update payload carries the same values as span_create.
        if md.get("model"):
            extras["model"] = md["model"]
        if md.get("model_id"):
            extras["internal_model_id"] = md["model_id"]
        return extras, metadata_updates

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
        lg_meta = extract_langgraph_metadata(metadata=metadata, tags=tags)
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
        # The workflow span IS the trace root: pin span_id == trace_id so the
        # finalized root carries trace identity (no separate trace event). Fold
        # ambient tracing_context() tags/metadata onto it — with root == trace
        # the root must carry what the removed trace_create used to (mirrors the
        # claude_agent_sdk path).
        from aigie.context_manager import merge_metadata, merge_tags

        metadata = merge_metadata(
            {"chain_type": "workflow", "framework": "langgraph", "type": "langgraph"}
        )
        tags = merge_tags()
        self.spans.open_span(
            run_id=self._WORKFLOW_RUN_ID,
            parent_run_id=None,
            name=self._workflow_name,
            span_type="workflow",
            input=input,
            metadata=metadata,
            extras={"tags": tags} if tags else None,
            span_id=current_trace_id(),
        )
        self._execution.start_span(
            name=self._workflow_name, span_type="workflow", at=datetime.now(timezone.utc)
        )

    def close_workflow_span(
        self, *, output: Any = None, error: BaseException | None = None
    ) -> None:
        now = datetime.now(timezone.utc)
        status = "error" if error is not None else "success"
        # Fold the old trace_update's run-level data onto the root span — there
        # is no separate trace event anymore.
        metadata_updates = self._root_metadata_updates(status)
        if error is not None:
            self._execution.end_span(
                name=self._workflow_name, status="error", at=now, error_message=str(error)
            )
            self.spans.fail_span(
                run_id=self._WORKFLOW_RUN_ID, error=error, metadata_updates=metadata_updates
            )
        else:
            self._execution.end_span(name=self._workflow_name, status="success", at=now)
            self.spans.close_span(
                run_id=self._WORKFLOW_RUN_ID, output=output, metadata_updates=metadata_updates
            )

    def _root_metadata_updates(self, status: str) -> dict[str, Any]:
        """Run-level execution data that the legacy trace_update carried, now
        folded onto the finalized root span."""
        metadata: dict[str, Any] = {
            "framework": "langgraph",
            "type": "langgraph",
            "execution_plan": self._execution.to_execution_plan(
                agent_name=self._workflow_name, status=status
            ),
            "turn_count": self._execution.turn_count,
        }
        execution_data = self._execution.to_execution_data()
        if execution_data["execution_path"]:
            metadata["execution_data"] = execution_data
        return metadata
