"""Generation context enrichment helpers for the kernel lifecycle."""

from __future__ import annotations

from typing import Any

from packages.contracts.runtime import ContextBundle


def build_context_for_generation(
    *,
    dependencies: Any,
    request: Any,
    profile: Any,
    session: Any,
    intent: Any,
    goals: tuple[Any, ...],
    memories: tuple[Any, ...],
    context: ContextBundle,
    decision: Any,
    plan: Any,
    continuity: Any,
    clock: Any,
    augment_clock: Any,
) -> ContextBundle:
    if request.tool_name is not None:
        return context
    enriched_context = context
    augment = getattr(dependencies.context, "augment_for_generation", None)
    if callable(augment):
        enriched = augment(
            session=session,
            goals=goals,
            memories=memories,
            context=context,
            intent=intent,
            decision=decision,
            plan=plan,
            continuity=continuity,
        )
        if isinstance(enriched, ContextBundle):
            enriched_context = enriched
    if clock is None:
        return enriched_context
    return augment_clock(enriched_context, clock=clock)


__all__ = ["build_context_for_generation"]
