"""Ticket dependency graph for the parallel batch scheduler.

Reads the hard GitLab issue links (``blocks`` / ``is_blocked_by``; ``relates_to`` is
ignored) among the batch candidates and turns them into a schedulable DAG. A ticket
may only start its phase-1 implementation once every hard dependency is **merged**, so
the graph classifies each candidate as:

- **ready** — no in-batch blocker (start immediately);
- **edges** — in-batch ordering constraints ``blocker → blocked``;
- **deferred** — blocked by an external ticket not merged this run (or, transitively, by a
  deferred one) → not processed this run;
- **cycles** — cannot be topologically ordered (in a dependency cycle or downstream of one)
  → escalate.

Pure logic: the GitLab fetchers (``fetch_links`` / ``is_satisfied``) are injected so the
graph is unit-testable without network. Refs are canonical ``project_path#iid`` strings.
"""

from collections import deque
from collections.abc import Callable
from dataclasses import dataclass

from pydantic import BaseModel

HARD_LINK_TYPES = frozenset({"blocks", "is_blocked_by"})


def ref(project_path: str, iid: int) -> str:
    """Canonical, cross-project ticket key."""
    return f"{project_path}#{iid}"


@dataclass
class LinkedIssue:
    """One GitLab issue link off a candidate: the linked issue and how it relates."""

    ref: str  # the linked issue, as project_path#iid
    link_type: str  # blocks | is_blocked_by | relates_to
    state: str  # opened | closed


class Edge(BaseModel):
    blocker: str  # must merge before `blocked`
    blocked: str


class DeferredTicket(BaseModel):
    ticket: str
    blocked_by: list[str]  # unmet blockers (external, or transitively deferred)


class DepGraph(BaseModel):
    ready: list[str]  # non-deferred, non-cycle, zero in-batch blockers
    edges: list[Edge]  # in-batch ordering constraints among schedulable tickets
    deferred: list[DeferredTicket]
    cycles: list[str]  # tickets that cannot be ordered (cycle or downstream of one)


def build_graph(
    candidates: list[str],
    fetch_links: Callable[[str], list[LinkedIssue]],
    is_satisfied: Callable[[str, str], bool],
) -> DepGraph:
    """Build the schedulable dependency graph over ``candidates`` (canonical refs).

    ``fetch_links(ref)`` returns the issue links of one candidate; ``is_satisfied(ref, state)``
    tells whether an **external** blocker is already merged (closed or merged-MR).
    """
    cand = set(candidates)
    edges: set[tuple[str, str]] = set()
    external_unmet: dict[str, set[str]] = {}

    for x in candidates:
        for link in fetch_links(x):
            if link.link_type not in HARD_LINK_TYPES:
                continue
            blocker, blocked = (link.ref, x) if link.link_type == "is_blocked_by" else (x, link.ref)
            if blocked not in cand:
                continue  # we only schedule candidates
            if blocker in cand:
                edges.add((blocker, blocked))
            elif not is_satisfied(blocker, link.state):
                external_unmet.setdefault(blocked, set()).add(blocker)

    deferred_reasons = _propagate_deferred(external_unmet, edges)
    schedulable = [c for c in candidates if c not in deferred_reasons]
    live_edges = {(b, x) for (b, x) in edges if b in schedulable and x in schedulable}
    ready, cycles = _kahn(schedulable, live_edges)

    return DepGraph(
        ready=sorted(ready),
        edges=[Edge(blocker=b, blocked=x) for b, x in sorted(live_edges)],
        deferred=[
            DeferredTicket(ticket=t, blocked_by=sorted(reasons)) for t, reasons in sorted(deferred_reasons.items())
        ],
        cycles=sorted(cycles),
    )


def _propagate_deferred(external_unmet: dict[str, set[str]], edges: set[tuple[str, str]]) -> dict[str, set[str]]:
    """Seed deferred from external unmet deps, then propagate along edges (blocker deferred → blocked deferred)."""
    reasons: dict[str, set[str]] = {t: set(b) for t, b in external_unmet.items()}
    out: dict[str, list[str]] = {}
    for b, x in edges:
        out.setdefault(b, []).append(x)
    queue = deque(reasons)
    while queue:
        blocker = queue.popleft()
        for blocked in out.get(blocker, []):
            if blocker not in reasons.get(blocked, set()):
                if blocked not in reasons:
                    queue.append(blocked)
                reasons.setdefault(blocked, set()).add(blocker)
    return reasons


def _kahn(nodes: list[str], edges: set[tuple[str, str]]) -> tuple[list[str], list[str]]:
    """Topological peel. Returns (initial ready set = in-degree 0, unorderable nodes = cycles)."""
    indeg = dict.fromkeys(nodes, 0)
    succ: dict[str, list[str]] = {n: [] for n in nodes}
    for blocker, blocked in edges:
        indeg[blocked] += 1
        succ[blocker].append(blocked)
    ready = [n for n in nodes if indeg[n] == 0]
    queue = deque(ready)
    removed: set[str] = set()
    while queue:
        n = queue.popleft()
        removed.add(n)
        for m in succ[n]:
            indeg[m] -= 1
            if indeg[m] == 0:
                queue.append(m)
    cycles = [n for n in nodes if n not in removed]
    return ready, cycles
