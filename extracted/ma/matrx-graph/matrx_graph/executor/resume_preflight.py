"""Resume pre-flight: can this checkpoint EVER finish on this graph?

A checkpoint may be resumed against a compiled graph that is not the one the
run started on (a draft edited mid-run). When the new graph adds a REQUIRED
inbound edge whose source can never run again, the target's join never
completes: the run does all the remaining work, then parks ERRORED with "Join
deadlock". This answers it up front from the checkpoint, so such a resume is
refused before any step runs — and every other resume proceeds.

🚨 It refuses only on PROVEN impossibility. Any uncertainty passes.

"Can still run" follows EVERY way the engine launches a node (census,
2026-10-01 — review of f053f5b83d, whose edge-only reachability refused
unchanged graphs):

* an edge (any kind, back-edges included) out of a node that can still run;
* a dispatcher (``validation.DISPATCHER_NODE_TYPES`` — map / send / loop /
  work_queue) launches ``config.target_node_id``, and may relaunch itself;
* a node whose spec declares ``launches_nodes`` may ``ctx.send`` ANY node —
  if one can still run, nothing is provable and the check passes;
* a kind-subscription node (``trigger_kind``) fires on data any running node
  emits — it can run whenever anything can;
* an unknown node type (no spec to read) is treated as a launcher: pass.

Not judged at all: nodes on a cycle (their firings are opened by back-edges,
§9), nodes a dispatcher launches (a Send skips the join), ``join_policy='any'``
nodes (they fire per delivery) and subscription nodes (they never join).
"""

from __future__ import annotations

from typing import Any

from matrx_graph.types.compiled import CompiledGraph
from matrx_graph.types.primitives import EdgeKind

#: THE joinable edge kinds — the scheduler's join accumulator imports this.
JOINABLE_KINDS = (EdgeKind.DATA, EdgeKind.CONDITIONAL, EdgeKind.CONTROL, EdgeKind.ERROR)


def required_edge_ids(graph: CompiledGraph, node_id: str) -> set[str]:
    """The required inbound set (§3.2): all joinable inbound edges, minus cycle
    back-edges (F13 — requiring one would deadlock every feedback loop) and
    fan-out ``each`` edges (dispatchers, like back-edges, open firings rather
    than resolving a join). ``Scheduler._required_edge_ids`` is this."""
    return {
        eid
        for eid in graph.nodes[node_id].incoming_edge_ids
        if graph.edges[eid].kind in JOINABLE_KINDS
        and not graph.edges[eid].is_back_edge
        and graph.edges[eid].fan_out != "each"
    }


class _AnythingMayRun(Exception):
    """A node that can still run may launch any node."""


def _dispatch_target(graph: CompiledGraph, node_id: str) -> str | None:
    from matrx_graph.validation import DISPATCHER_NODE_TYPES

    node = graph.nodes[node_id]
    if node.spec_type not in DISPATCHER_NODE_TYPES:
        return None
    target = getattr(node.config, "target_node_id", None)
    return target if isinstance(target, str) else None


def launch_is_declared(graph: CompiledGraph, registry: Any, source: str, target: str) -> bool:
    """Whether a ``ctx.send`` from ``source`` to ``target`` is one the graph
    DECLARES — a dispatcher's config target (or itself), or a spec with
    ``launches_nodes``. The scheduler checks every Send against this, so the
    pre-flight's model of "who can launch what" cannot silently go stale."""
    if source not in graph.nodes:
        return False
    dispatch_target = _dispatch_target(graph, source)
    if dispatch_target is not None and target in {dispatch_target, source}:
        return True
    try:
        spec = registry.get(graph.nodes[source].spec_type).spec
    except Exception:  # noqa: BLE001
        return False
    return bool(getattr(spec, "launches_nodes", False))


#: Spec types seen sending WITHOUT declaring it — the alarm's once-per-process
#: memory ONLY. The pre-flight's launch picture never reads it: it comes from
#: the static declarations alone, so it cannot differ by process age.
_OBSERVED_LAUNCHERS: set[str] = set()

#: ``MATRX_GRAPH_STRICT_LAUNCHES=1`` turns an undeclared launch into a refusal
#: (the package's own tests run strict). Production logs it as an ERROR and
#: allows the run: the run itself is correct, only the declaration is missing,
#: and refusing a working run over metadata would be the worse failure. The fix
#: is the declaration; the static census in the host's tests catches it first.
STRICT_LAUNCHES_ENV = "MATRX_GRAPH_STRICT_LAUNCHES"


def record_undeclared_launch(spec_type: str, source: str, target: str) -> None:
    """Announce a ``ctx.send`` the graph never declared; raise when strict."""
    import logging
    import os

    first = spec_type not in _OBSERVED_LAUNCHERS
    _OBSERVED_LAUNCHERS.add(spec_type)
    message = (
        f"step '{source}' ({spec_type}) launched '{target}' with ctx.send but its spec "
        "does not declare launches_nodes=True and it is not a dispatcher sending to "
        "its config target — declare it on the node's spec"
    )
    if os.environ.get(STRICT_LAUNCHES_ENV, "").lower() in {"1", "true", "yes"}:
        from matrx_graph.errors import ExecutionError

        raise ExecutionError(message)
    if first:
        logging.getLogger(__name__).error("[matrx_graph] UNDECLARED LAUNCH: %s", message)


def _launched_by(
    graph: CompiledGraph, node_id: str, registry: Any, *, back_edges: bool = True
) -> set[str]:
    from matrx_graph.validation import DISPATCHER_NODE_TYPES

    node = graph.nodes[node_id]
    try:
        spec = registry.get(node.spec_type).spec
    except Exception as exc:  # noqa: BLE001 — no spec to read = cannot prove anything
        raise _AnythingMayRun from exc
    if getattr(spec, "launches_nodes", False):
        raise _AnythingMayRun
    targets = {
        graph.edges[eid].target_node_id
        for eid in node.outgoing_edge_ids
        if back_edges or not graph.edges[eid].is_back_edge
    }
    if node.spec_type in DISPATCHER_NODE_TYPES:
        target = _dispatch_target(graph, node_id)
        if target is None or target not in graph.nodes:
            raise _AnythingMayRun
        targets |= {target, node_id}
    return targets


def can_still_run(
    graph: CompiledGraph, frontier: set[str], registry: Any, *, back_edges: bool = True
) -> set[str] | None:
    """Every node the engine could still launch from ``frontier`` (the
    frontier included); ``None`` when that cannot be bounded (a live launcher
    may send anywhere). ``back_edges=False`` follows one pass forward only —
    what a fork uses to ask which branches MEET, so a loop never pulls an
    unrelated sibling in."""
    subscribers = {nid for nid, node in graph.nodes.items() if node.trigger_kind}
    seen = {n for n in frontier if n in graph.nodes}
    stack = list(seen)
    try:
        while stack:
            if subscribers - seen:
                fresh = subscribers - seen
                seen |= fresh
                stack.extend(fresh)
            node_id = stack.pop()
            for target in _launched_by(graph, node_id, registry, back_edges=back_edges):
                if target not in seen:
                    seen.add(target)
                    stack.append(target)
    except _AnythingMayRun:
        return None
    return seen


def _cyclic_nodes(graph: CompiledGraph) -> set[str]:
    """Nodes on a cycle — Tarjan's SCC, iterative, linear in nodes + edges
    (adjacency built once)."""
    adjacency: dict[str, list[str]] = {
        nid: [
            graph.edges[eid].target_node_id
            for eid in node.outgoing_edge_ids
            if graph.edges[eid].target_node_id in graph.nodes
        ]
        for nid, node in graph.nodes.items()
    }
    index: dict[str, int] = {}
    low: dict[str, int] = {}
    on_stack: set[str] = set()
    stack: list[str] = []
    cyclic: set[str] = set()
    counter = 0
    for root in graph.nodes:
        if root in index:
            continue
        work: list[tuple[str, int]] = [(root, 0)]
        while work:
            nid, child = work[-1]
            succ = adjacency[nid]
            if child == 0:
                index[nid] = low[nid] = counter
                counter += 1
                stack.append(nid)
                on_stack.add(nid)
            if child < len(succ):
                work[-1] = (nid, child + 1)
                nxt = succ[child]
                if nxt not in index:
                    work.append((nxt, 0))
                elif nxt in on_stack:
                    low[nid] = min(low[nid], index[nxt])
                continue
            work.pop()
            if work:
                parent = work[-1][0]
                low[parent] = min(low[parent], low[nid])
            if low[nid] == index[nid]:
                component: list[str] = []
                while True:
                    member = stack.pop()
                    on_stack.discard(member)
                    component.append(member)
                    if member == nid:
                        break
                if len(component) > 1 or nid in succ:
                    cyclic.update(component)
    return cyclic


def resume_preflight_problems(
    graph: CompiledGraph, checkpoint: Any, registry: Any = None
) -> list[str]:
    """Plain-English reasons this checkpoint can NEVER finish on ``graph``;
    empty when it can, or when that cannot be proven."""
    if registry is None:
        from matrx_graph.executor.registry import default_registry

        registry = default_registry()
    problems: list[str] = []
    frontier = {ni.node_id for ni in checkpoint.next_invocations}
    missing = sorted(n for n in frontier if n not in graph.nodes)
    if missing:
        problems.append(
            "the run was about to execute step(s) this version of the workflow no "
            f"longer has: {', '.join(missing)}"
        )
    for node_id, binding in checkpoint.pending_bindings.items():
        if node_id not in graph.nodes:
            problems.append(
                f"step '{node_id}' was waiting on its inputs but this version of the "
                "workflow no longer has it"
            )
            continue
        gone = sorted(
            {key.split("@@", 1)[0] for key in binding.edges}
            - set(graph.edges)
        )
        if gone:
            problems.append(
                f"step '{node_id}' holds inputs from connection(s) this version of the "
                f"workflow no longer has: {', '.join(gone)}"
            )
    if problems:
        return problems

    live = can_still_run(graph, frontier, registry)
    if live is None:
        return []
    cyclic = _cyclic_nodes(graph)
    # A step a dispatcher launches is fired by a Send, which SKIPS the join —
    # its edge inputs are never waited on (review of 6bac24af48: a loop body
    # with a static input from 'setup' was refused on an unchanged graph).
    send_launched = {
        target for nid in graph.nodes if (target := _dispatch_target(graph, nid)) is not None
    }
    unjudged = frontier | cyclic | send_launched
    for node_id in sorted((live | set(checkpoint.pending_bindings)) - unjudged):
        node = graph.nodes[node_id]
        if node.join_policy != "all" or node.trigger_kind:
            continue
        binding = checkpoint.pending_bindings.get(node_id)
        resolved = {key.split("@@", 1)[0] for key in (binding.edges if binding else {})}
        for eid in sorted(required_edge_ids(graph, node_id)):
            source = graph.edges[eid].source_node_id
            if eid in resolved or source in live:
                continue
            problems.append(
                f"step '{node_id}' needs input from '{source}', which will not run again "
                f"in this run — rerun from '{source}' or start a fresh run"
            )
    return problems


__all__ = [
    "JOINABLE_KINDS",
    "can_still_run",
    "launch_is_declared",
    "record_undeclared_launch",
    "required_edge_ids",
    "resume_preflight_problems",
]
