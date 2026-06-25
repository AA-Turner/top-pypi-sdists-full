"""Shared ``BaseCallbackHandler`` base for langchain_core-callback integrations.

LangGraph and LangChain both dispatch events through langchain_core's callback
contract; the span-emission logic is identical, so this base owns it and
subclasses override only small seams (``framework_name``, ``_fw_metadata``,
``_chain_metadata``, ``_chain_span_name``, ``_llm_span_name``,
``_augment_llm_input``). Setting ``callback_driven = True`` opts into the
base-owned trace boundary documented below.

Wire shape is constrained by the committed baselines under
``tests/unit/integrations/langgraph/baseline/``.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import UUID

from langchain_core.callbacks import BaseCallbackHandler

from aigie.tracing.event_classifier import EventKind, FrameworkEvent, FrameworkEventClassifier
from aigie.tracing.execution_state import ExecutionState
from aigie.tracing.lc_trace_boundary import LangChainTraceBoundary
from aigie.tracing.lc_usage import usage_payload
from aigie.tracing.llm_metadata import (
    extract_llm_params,
    extract_model_info,
    extract_prompt_content,
)
from aigie.tracing.span_event_handler import SpanEventHandler


class LangChainCallbackBase(LangChainTraceBoundary, BaseCallbackHandler):
    """BaseCallbackHandler that emits Kytte spans via a held SpanEventHandler.

    Framework-agnostic. Subclass and override the seams documented in the
    module docstring to bind a concrete framework.
    """

    # Recognized when scanning ``config["callbacks"]`` for an existing Aigie
    # handler — beats comparing ``__name__`` strings.
    _is_aigie_handler = True

    _WORKFLOW_RUN_ID = "__workflow__"

    framework_name: str = "langchain"

    def __init__(
        self,
        emitter: Any,
        workflow_name: str,
        classifier: FrameworkEventClassifier | None = None,
        *,
        config: Any = None,
    ) -> None:
        BaseCallbackHandler.__init__(self)
        self.spans = SpanEventHandler(emitter=emitter, config=config)
        self._workflow_name = workflow_name
        self._execution = ExecutionState()
        self._classifier = classifier if classifier is not None else self._default_classifier()
        # Callback-driven trace-boundary state (used only when callback_driven).
        self._root_run_id: str | None = None
        self._trace_id: str | None = None
        self._ambient_token: Any = None
        self._suppressed = False

    # ------------------------------------------------------------------
    # Framework seams (override in subclasses)
    # ------------------------------------------------------------------

    def _default_classifier(self) -> FrameworkEventClassifier:
        raise NotImplementedError(
            "subclass must supply a classifier or override _default_classifier"
        )

    def _fw_metadata(
        self, metadata: dict[str, Any] | None, tags: list[Any] | None
    ) -> dict[str, Any]:
        return {}

    def _chain_metadata(
        self, user_metadata: dict[str, Any] | None, fw_meta: dict[str, Any]
    ) -> dict[str, Any]:
        if not user_metadata:
            return dict(fw_meta)
        out = dict(fw_meta)
        for k, v in user_metadata.items():
            out.setdefault(k, v)
        return out

    def _chain_span_name(self, resolved_name: str, fw_meta: dict[str, Any]) -> str:
        return resolved_name or "chain"

    def _llm_span_name(self, model_display: str, fw_meta: dict[str, Any]) -> str:
        return f"LLM: {model_display}"

    def _augment_llm_input(self, llm_input: dict[str, Any], fw_meta: dict[str, Any]) -> None:
        return

    # Trace-root span + callback-driven boundary (_note_start / _note_end /
    # open_workflow_span / …) live in LangChainTraceBoundary.

    def _resolve_parent(self, parent_run_id: UUID | None) -> str | None:
        if parent_run_id is None:
            # Callback-driven: root-level events nest under the workflow span.
            if self.callback_driven and self.spans.is_open(self._WORKFLOW_RUN_ID):
                return self._WORKFLOW_RUN_ID
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
        fw_meta = self._fw_metadata(metadata, tags)
        name = self._chain_span_name(resolved_name, fw_meta)
        if self._note_start(run_id, parent_run_id, name, inputs):
            return
        if kind is EventKind.SUBGRAPH_WORKFLOW:
            self._open_subgraph_workflow_span(run_id, parent_run_id, inputs, metadata, fw_meta)
            return
        self._open_chain_span(run_id, parent_run_id, name, inputs, metadata, fw_meta)

    def _open_chain_span(self, run_id, parent_run_id, name, inputs, metadata, fw_meta):
        merged = {"chain_type": "chain", **self._chain_metadata(metadata, fw_meta)}
        self.spans.open_span(
            run_id=str(run_id),
            parent_run_id=self._resolve_parent(parent_run_id),
            name=name,
            span_type="chain",
            input=inputs,
            metadata=merged,
        )
        self._execution.start_span(name=name, span_type="chain", at=datetime.now(timezone.utc))

    def _open_subgraph_workflow_span(self, run_id, parent_run_id, inputs, metadata, fw_meta):
        sub_merged = {"chain_type": "workflow", **self._chain_metadata(metadata, fw_meta)}
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
        self._note_end(run_id, output=outputs)

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
        self._note_end(run_id, error=error)

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
        fw_meta = self._fw_metadata(metadata, tags)

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
        self._augment_llm_input(llm_input, fw_meta)

        span_name = self._llm_span_name(model_info.display_name, fw_meta)
        if self._note_start(run_id, parent_run_id, span_name, llm_input):
            return
        # Backend extracts `model`/`model_name`/`model_id` from metadata into
        # the spans table columns (see spans.model in agent_monitor schema).
        merged_metadata: dict[str, Any] = {
            **fw_meta,
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
            self._note_end(run_id, output=output)
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
        self._note_end(run_id, output=output)

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
        # Token/cost extraction + wire placement is owned by lc_usage.usage_payload
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
        self._note_end(run_id, error=error)

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
        fw_meta = self._fw_metadata(metadata, tags)
        name = (serialized or {}).get("name") or "tool"
        if self._note_start(run_id, parent_run_id, name, input_str):
            return
        self.spans.open_span(
            run_id=str(run_id),
            parent_run_id=self._resolve_parent(parent_run_id),
            name=name,
            span_type="tool",
            input=input_str,
            metadata=fw_meta,
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
        self._note_end(run_id, output=output)

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
        self._note_end(run_id, error=error)
