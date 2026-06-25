"""LangChain FrameworkEventClassifier.

Unlike LangGraph there's no Pregel/Channel plumbing to strip; the only
framework-internal noise is anything tagged ``langsmith:hidden``.
"""

from __future__ import annotations

from aigie.tracing.event_classifier import (
    EventKind,
    FrameworkEvent,
    FrameworkEventClassifier,
)

_HIDDEN_TAG = "langsmith:hidden"


class LangChainEventClassifier(FrameworkEventClassifier):
    def classify_chain_event(self, event: FrameworkEvent) -> EventKind:
        if _HIDDEN_TAG in event.tags:
            return EventKind.DROP
        return EventKind.CHAIN

    def classify_llm_event(self, event: FrameworkEvent) -> EventKind:
        return EventKind.LLM

    def classify_tool_event(self, event: FrameworkEvent) -> EventKind:
        return EventKind.TOOL
