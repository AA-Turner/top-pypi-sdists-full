"""LangChain FrameworkEventClassifier.

Unlike LangGraph there's no Pregel/Channel plumbing to strip; the only
framework-internal noise is anything tagged ``langsmith:hidden``.

Plain LCEL has no intrinsic notion of a sub-agent — a nested chain is
indistinguishable from any other chain — so a caller marks one explicitly by
setting its ``run_name`` to (or prefixing it with) ``aigie:subagent``::

    inner = (prompt | llm | parser).with_config(run_name="aigie:subagent:research")

``run_name`` is deliberately the marker rather than a tag/metadata key: those
inherit down to every child run in LangChain, which would mis-mark the
sub-agent's own internal steps as further sub-agents. ``run_name`` applies only
to the runnable it's set on, so exactly one boundary span is promoted.
"""

from __future__ import annotations

from aigie.tracing.event_classifier import (
    EventKind,
    FrameworkEvent,
    FrameworkEventClassifier,
)

_HIDDEN_TAG = "langsmith:hidden"
_SUBAGENT_MARKER = "aigie:subagent"


class LangChainEventClassifier(FrameworkEventClassifier):
    def classify_chain_event(self, event: FrameworkEvent) -> EventKind:
        if _HIDDEN_TAG in event.tags:
            return EventKind.DROP
        if event.parent_run_id is not None and event.name.startswith(_SUBAGENT_MARKER):
            return EventKind.SUBGRAPH_WORKFLOW
        return EventKind.CHAIN

    def classify_llm_event(self, event: FrameworkEvent) -> EventKind:
        return EventKind.LLM

    def classify_tool_event(self, event: FrameworkEvent) -> EventKind:
        return EventKind.TOOL
