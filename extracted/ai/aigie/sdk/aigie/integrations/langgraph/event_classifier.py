"""LangGraph implementation of FrameworkEventClassifier.

ONE classifier handles chain + llm + tool events for LangGraph. Filter
rules are pure functions of the raw event so they're table-testable.
"""

from __future__ import annotations

from aigie.tracing.event_classifier import (
    EventKind,
    FrameworkEvent,
    FrameworkEventClassifier,
)

_LANGGRAPH_GRAPH_NAMES = frozenset(
    {"LangGraph", "Pregel", "CompiledStateGraph", "CompiledGraph"}
)
_DROP_NAME_PREFIXES = ("ChannelWrite", "ChannelRead")
_DROP_NAMES = frozenset({"__start__", "__end__"})


class LangGraphEventClassifier(FrameworkEventClassifier):
    def classify_chain_event(self, event: FrameworkEvent) -> EventKind:
        node = event.framework_metadata.get("langgraph_node")
        if isinstance(node, str) and node.startswith("__"):
            return EventKind.DROP
        if event.name in _DROP_NAMES or event.name.startswith(_DROP_NAME_PREFIXES):
            return EventKind.DROP
        if "langsmith:hidden" in event.tags:
            return EventKind.DROP
        if (
            not node
            and event.parent_run_id is None
            and event.name in _LANGGRAPH_GRAPH_NAMES
        ):
            return EventKind.DROP
        if event.name in _LANGGRAPH_GRAPH_NAMES and event.parent_run_id is not None:
            return EventKind.SUBGRAPH_WORKFLOW
        return EventKind.CHAIN

    def classify_llm_event(self, event: FrameworkEvent) -> EventKind:
        return EventKind.LLM

    def classify_tool_event(self, event: FrameworkEvent) -> EventKind:
        return EventKind.TOOL
