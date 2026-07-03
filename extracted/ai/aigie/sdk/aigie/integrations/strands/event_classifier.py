"""Pure event-classification rules for the Strands integration."""

from __future__ import annotations

from aigie.tracing.event_classifier import EventKind, FrameworkEvent, FrameworkEventClassifier


class StrandsEventClassifier(FrameworkEventClassifier):
    def classify_chain_event(self, event: FrameworkEvent) -> EventKind:
        if event.framework_metadata.get("kind") == "node":
            return EventKind.SUBGRAPH_WORKFLOW
        return EventKind.CHAIN

    def classify_llm_event(self, event: FrameworkEvent) -> EventKind:
        return EventKind.LLM

    def classify_tool_event(self, event: FrameworkEvent) -> EventKind:
        return EventKind.TOOL
