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

from typing import Any

from aigie.integrations.langgraph._metadata import extract_langgraph_metadata, passthrough_metadata
from aigie.integrations.langgraph.event_classifier import LangGraphEventClassifier
from aigie.tracing.event_classifier import FrameworkEventClassifier
from aigie.tracing.lc_callback_base import LangChainCallbackBase

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
