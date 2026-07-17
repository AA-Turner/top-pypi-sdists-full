"""LangGraph-native callback handler (L3 framework binding).

Thin subclass of the shared ``LangChainCallbackBase`` — the generic
``BaseCallbackHandler`` span-emission logic lives there. This file supplies
only the LangGraph-specific seams: node/step/path metadata extraction, the
``langgraph`` wire framing, and subgraph-workflow handling. The bridge
(``LangGraphLifecycle``) drives the per-invocation trace lifecycle, so the
``_note_start`` / ``_note_end`` hooks stay at their no-op defaults.

Wire shape is constrained by the committed baselines under
``tests/unit/integrations/langgraph/baseline/``.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import UUID

from aigie.integrations.langgraph._metadata import extract_langgraph_metadata, passthrough_metadata
from aigie.integrations.langgraph.control_flow import is_control_flow_signal
from aigie.integrations.langgraph.event_classifier import LangGraphEventClassifier
from aigie.tracing.event_classifier import FrameworkEventClassifier
from aigie.tracing.lc_callback_base import LangChainCallbackBase
from aigie.tracing.trace_state import current_trace_id

_LG_INPUT_KEYS = ("langgraph_node", "langgraph_step", "langgraph_path")


class LangGraphNativeCallback(LangChainCallbackBase):
    """LangChainCallbackBase bound to LangGraph's node/step/path metadata."""

    framework_name = "langgraph"

    def _default_classifier(self) -> FrameworkEventClassifier:
        return LangGraphEventClassifier()

    def _fw_metadata(
        self, metadata: dict[str, Any] | None, tags: list[Any] | None
    ) -> dict[str, Any]:
        return extract_langgraph_metadata(metadata=metadata, tags=tags)

    def _chain_metadata(
        self, user_metadata: dict[str, Any] | None, fw_meta: dict[str, Any]
    ) -> dict[str, Any]:
        return passthrough_metadata(user_metadata, fw_meta)

    def _chain_span_name(self, resolved_name: str, fw_meta: dict[str, Any]) -> str:
        return resolved_name or fw_meta.get("langgraph_node") or "chain"

    def _llm_span_name(self, model_display: str, fw_meta: dict[str, Any]) -> str:
        return fw_meta.get("langgraph_node") or f"LLM: {model_display}"

    def _augment_llm_input(self, llm_input: dict[str, Any], fw_meta: dict[str, Any]) -> None:
        for k in _LG_INPUT_KEYS:
            if k in fw_meta:
                llm_input[k] = fw_meta[k]

    def on_chain_error(
        self,
        error: BaseException,
        *,
        run_id: UUID,
        parent_run_id: UUID | None = None,
        **kwargs: Any,
    ) -> None:
        if not is_control_flow_signal(error):
            super().on_chain_error(error, run_id=run_id, parent_run_id=parent_run_id, **kwargs)
            return
        self._pause_control_flow_span(run_id)

    def on_llm_error(self, error: BaseException, *, run_id: UUID, **kwargs: Any) -> None:
        if not is_control_flow_signal(error):
            super().on_llm_error(error, run_id=run_id, **kwargs)
            return
        self._pause_control_flow_span(run_id)

    def on_tool_error(self, error: BaseException, *, run_id: UUID, **kwargs: Any) -> None:
        if not is_control_flow_signal(error):
            super().on_tool_error(error, run_id=run_id, **kwargs)
            return
        self._pause_control_flow_span(run_id)

    def _pause_control_flow_span(self, run_id: UUID) -> None:
        state = self.spans.get_state(str(run_id))
        name = state["name"] if state else "chain"
        self._execution.end_span(name=name, status="paused", at=datetime.now(timezone.utc))
        self.spans.pause_span(run_id=str(run_id))
        self._note_end(run_id, error=None)

    def _on_node_span_opened(self, run_id: str, fw_meta: dict[str, Any]) -> None:
        hook = getattr(self, "_aigie_rewind", None)
        if hook is None or not fw_meta.get("langgraph_node"):
            return
        trace_id = current_trace_id()
        if trace_id is None:
            return
        # Key the handle by the emitted span id (what the backend/orchestrator
        # sees), not the framework run_id. open_span generates a fresh uuid and
        # maps run_id -> state["id"]; a late verdict references that id.
        state = self.spans.get_state(run_id)
        span_id = state["id"] if state else run_id
        handle = hook.capability.build_handle(span_id, trace_id, hook.app, hook.config)
        if handle is not None:
            hook.coordinator.record(trace_id, span_id, handle)
