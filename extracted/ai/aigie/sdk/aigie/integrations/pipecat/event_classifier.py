"""Pure event-classification rules for the Pipecat integration."""

from __future__ import annotations

from aigie.tracing.event_classifier import EventKind, FrameworkEvent, FrameworkEventClassifier


class PipecatEventClassifier(FrameworkEventClassifier):
    # Pipecat's filtering is frame-level (see _frames.is_rejected); by the time an
    # event reaches a span there is nothing left to drop or reclassify.
    def classify_chain_event(self, event: FrameworkEvent) -> EventKind:
        return EventKind.CHAIN

    def classify_llm_event(self, event: FrameworkEvent) -> EventKind:
        return EventKind.LLM

    def classify_tool_event(self, event: FrameworkEvent) -> EventKind:
        return EventKind.TOOL
