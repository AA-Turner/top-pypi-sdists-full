"""Turn a ranked candidate pool + dependency graph into an execution plan.

Pure logic shared by both in-session batch paths:

- the sequential path (concurrency=1) processes ``ordered`` top to bottom — each ticket merges
  before the next starts, so a topological order is enough for correctness;
- the parallel Workflow (concurrency>1) uses ``ordered`` + the graph edges to fill its worker
  pool, respecting the same dependency constraints.

``ordered`` is a topological order of the schedulable tickets (dependencies before dependents),
breaking ties by the pool's ranking order. Deferred and cycle tickets are excluded from
``ordered`` and surfaced separately so the caller can record them (deferred / escalated).
"""

import heapq

from pydantic import BaseModel

from .dep_graph import DeferredTicket, DepGraph


class BatchPlan(BaseModel):
    ordered: list[str]  # schedulable refs, dependencies first, ties by ranking order
    deferred: list[DeferredTicket]  # unmet hard dependency → not processed this run
    cycles: list[str]  # unorderable (dependency cycle / downstream) → escalate


def topological_order(refs: list[str], edges: list[tuple[str, str]]) -> list[str]:
    """Kahn topological sort of ``refs`` under ``edges`` (blocker → blocked).

    Ties (independent tickets, or several unblocked at once) break by position in ``refs`` —
    the ranking order — so the highest-scored ready ticket goes first. ``refs`` must exclude
    cycle nodes (the caller drops them); every ref then appears exactly once in the result.
    """
    rank = {r: i for i, r in enumerate(refs)}
    present = set(refs)
    succ: dict[str, list[str]] = {r: [] for r in refs}
    indeg = dict.fromkeys(refs, 0)
    for blocker, blocked in edges:
        if blocker in present and blocked in present:
            succ[blocker].append(blocked)
            indeg[blocked] += 1
    heap = [(rank[r], r) for r in refs if indeg[r] == 0]
    heapq.heapify(heap)
    out: list[str] = []
    while heap:
        _, node = heapq.heappop(heap)
        out.append(node)
        for m in succ[node]:
            indeg[m] -= 1
            if indeg[m] == 0:
                heapq.heappush(heap, (rank[m], m))
    return out


def plan_batch(pool_refs: list[str], graph: DepGraph) -> BatchPlan:
    """Execution plan for ``pool_refs`` (ranking order) under ``graph``.

    Drops deferred + cycle tickets from the schedulable set and topologically orders the rest.
    """
    excluded = {d.ticket for d in graph.deferred} | set(graph.cycles)
    schedulable = [r for r in pool_refs if r not in excluded]
    edges = [(e.blocker, e.blocked) for e in graph.edges]
    return BatchPlan(
        ordered=topological_order(schedulable, edges),
        deferred=graph.deferred,
        cycles=graph.cycles,
    )
