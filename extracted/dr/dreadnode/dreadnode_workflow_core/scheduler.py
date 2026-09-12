"""The scheduler — ``next_actions(topology, state) -> [Action]``.

A pure function. No I/O, no clock, no randomness. Given the static graph and the
folded state, it decides what should happen next and returns it as data; the host
is a thin loop that executes those actions and appends the resulting facts.

Purity is the point:

* Crash and interleaving behaviour is exhaustively testable without a database —
  truncate a fact sequence at any prefix and assert recovery.
* **Both hosts call the same function**, so the in-process runtime host and the
  (deferred) durable platform host cannot disagree on control flow. That is
  risk 3 dissolved by construction rather than by a parity test.
"""

import typing as t
from dataclasses import dataclass, field

from dreadnode_workflow_core.facts import UnitKey, unit_key
from dreadnode_workflow_core.state import EmittedEvent, RunState
from dreadnode_workflow_core.topology import Topology, TopologyEdge

__all__ = [
    "Action",
    "CompleteRun",
    "FailRun",
    "MaterializeFanOut",
    "ReadyNode",
    "RequestApproval",
    "SkipNode",
    "next_actions",
]

APPROVAL_REQUEST = "ApprovalRequest"
APPROVAL_DECISION = "ApprovalDecision"


# ── Actions ──────────────────────────────────────────────────────────────


@dataclass(frozen=True)
class ReadyNode:
    """Run one node instance with this input."""

    unit: UnitKey
    input: dict[str, t.Any]
    source_events: tuple[int, ...] = ()
    """``seq`` of every event consumed, so the host can mark them routed."""


@dataclass(frozen=True)
class SkipNode:
    """Record an untaken path, so the run page shows *why* it was empty."""

    unit: UnitKey
    reason: str


@dataclass(frozen=True)
class MaterializeFanOut:
    """Declare how wide a fan-out is, before its instances are readied."""

    node_key: str
    count: int


@dataclass(frozen=True)
class RequestApproval:
    """Suspend on a human decision."""

    unit: UnitKey
    summary: str
    payload: dict[str, t.Any] = field(default_factory=dict)


@dataclass(frozen=True)
class CompleteRun:
    result: t.Any = None


@dataclass(frozen=True)
class FailRun:
    error: str


Action = ReadyNode | SkipNode | MaterializeFanOut | RequestApproval | CompleteRun | FailRun


# ── The scheduler ────────────────────────────────────────────────────────


def next_actions(topology: Topology, state: RunState) -> list[Action]:
    """Decide what happens next. Deterministic for a given (topology, state)."""
    if state.is_terminal():
        return []

    # The entry node has no incoming edges, so readiness cannot be derived from
    # predecessors. Key on "no instance yet" rather than on run status — the run
    # is already `running` by the time `run_started` has been folded.
    entry = unit_key(topology.entry)
    if topology.entry and state.node(entry) is None:
        return [ReadyNode(unit=entry, input={"input": state.input})]

    actions: list[Action] = []

    # 1. A materialization cap breach fails the run before anything is spawned.
    for point in topology.fan_out_points:
        emitted = [e for e in state.emitted if e.source.node_key == point.node]
        events = [e for e in emitted if _is_fan_out_event(topology, point.node, e)]
        if len(events) > point.cap:
            return [
                FailRun(
                    error=(
                        f"fan-out at {point.node!r} produced {len(events)} items, "
                        f"over the materialization cap of {point.cap}"
                    )
                )
            ]

    # 2. Declare fan-out widths that have not been recorded yet.
    actions.extend(_materializations(topology, state))

    # 3. Approvals: a gate that emitted ApprovalRequest suspends the run.
    actions.extend(_approval_requests(state))

    # 4. Ready whatever became runnable.
    actions.extend(_ready_nodes(topology, state))

    # 5. Skip paths that can no longer be taken.
    actions.extend(_skips(topology, state))

    if actions:
        return actions

    # 6. Nothing to do — decide whether the run is over.
    return _finalize(topology, state)


# ── Step 2: fan-out width ────────────────────────────────────────────────


def _is_fan_out_event(topology: Topology, node_key: str, event: EmittedEvent) -> bool:
    return any(
        e.kind == "fan_out" and e.event == event.event_type for e in topology.successors(node_key)
    )


def _materializations(topology: Topology, state: RunState) -> list[Action]:
    out: list[Action] = []
    for point in topology.fan_out_points:
        if point.node in state.fan_out_counts:
            continue
        source = state.node(unit_key(point.node))
        if source is None or source.status != "completed":
            # `settled` is not enough: a fan-out source that failed or was
            # skipped never produced items, and materializing a zero-width
            # fan-out would let a downstream join fire on nothing.
            continue
        count = len(
            [
                e
                for e in state.emitted
                if e.source.node_key == point.node and _is_fan_out_event(topology, point.node, e)
            ]
        )
        out.append(MaterializeFanOut(node_key=point.node, count=count))
    return out


# ── Step 3: approvals ────────────────────────────────────────────────────


def _approval_requests(state: RunState) -> list[Action]:
    out: list[Action] = []
    for event in state.emitted:
        if event.event_type != APPROVAL_REQUEST:
            continue
        if event.source in state.pending_approvals or event.source in state.approvals:
            continue
        node = state.node(event.source)
        if node is not None and node.status == "awaiting_approval":
            continue
        out.append(
            RequestApproval(
                unit=event.source,
                summary=str(event.data.get("summary", "")),
                payload=dict(event.data.get("payload") or {}),
            )
        )
    return out


# ── Step 4: readiness ────────────────────────────────────────────────────


def _ready_nodes(topology: Topology, state: RunState) -> list[Action]:
    out: list[Action] = []
    planned: set[UnitKey] = set()

    for node in topology.nodes:
        incoming = topology.predecessors(node.key)
        if not incoming:
            continue

        if node.consumes.collect:
            action = _ready_join(topology, state, node.key)
            if action is not None and action.unit not in planned:
                out.append(action)
                planned.add(action.unit)
            continue

        for unit, payload, seqs in _ready_simple(state, incoming):
            if unit in planned:
                continue
            if not _within_concurrency(topology, state, node.key, out):
                break
            out.append(ReadyNode(unit=unit, input=payload, source_events=seqs))
            planned.add(unit)

    return out


def _ready_simple(
    state: RunState,
    incoming: list[TopologyEdge],
) -> t.Iterator[tuple[UnitKey, dict[str, t.Any], tuple[int, ...]]]:
    """One instance per matching event that has not been consumed yet."""
    for edge in incoming:
        for event in state.emitted:
            if event.source.node_key != edge.from_ or event.event_type != edge.event:
                continue
            if edge.event == APPROVAL_DECISION and event.source not in state.approvals:
                continue
            unit = _target_unit(edge, event)
            existing = state.node(unit)
            if existing is not None and existing.status != "pending":
                continue
            yield unit, {"event": event.data, "event_type": event.event_type}, (event.seq,)


def _target_unit(edge: TopologyEdge, event: EmittedEvent) -> UnitKey:
    """Ordinal assignment — where fan-out width propagates.

    A fan-out edge gives the target the event's index. Any other edge inherits
    the source's ordinal, so a chain downstream of a fan-out stays one lane per
    element rather than collapsing.
    """
    if edge.kind == "fan_out":
        return unit_key(edge.to, event.index)
    return unit_key(edge.to, event.source.ordinal)


def _within_concurrency(
    topology: Topology, state: RunState, node_key: str, planned: list[Action]
) -> bool:
    cap = topology.node(node_key).config.max_concurrency
    if cap is None:
        return True
    already = state.running_count(node_key)
    queued = sum(1 for a in planned if isinstance(a, ReadyNode) and a.unit.node_key == node_key)
    return already + queued < cap


def _ready_join(topology: Topology, state: RunState, node_key: str) -> ReadyNode | None:
    """A join fires when every declared input has *settled*, not succeeded."""
    unit = unit_key(node_key)
    existing = state.node(unit)
    if existing is not None and existing.status != "pending":
        return None

    node = topology.node(node_key)
    join = next((j for j in topology.join_points if j.node == node_key), None)
    if join is None:
        return None

    collected: list[dict[str, t.Any]] = []
    failures: list[dict[str, t.Any]] = []
    seqs: list[int] = []

    for event_type in join.collects:
        producers = [e.from_ for e in topology.predecessors(node_key) if e.event == event_type]
        for producer in producers:
            expected = _expected_instances(topology, state, producer)
            if expected is None:
                return None  # width not yet known
            for ordinal in expected:
                instance = state.node(unit_key(producer, ordinal))
                if instance is None or not instance.settled:
                    return None  # still in flight
                if instance.status == "completed":
                    match = next(
                        (
                            e
                            for e in state.emitted
                            if e.source == instance.unit and e.event_type == event_type
                        ),
                        None,
                    )
                    if match is not None:
                        collected.append(
                            {
                                "event_type": match.event_type,
                                "data": match.data,
                            }
                        )
                        seqs.append(match.seq)
                elif instance.status in ("failed", "cancelled"):
                    failures.append(
                        {
                            "node": producer,
                            "ordinal": ordinal,
                            "failure_class": instance.failure_class or "error",
                            "error": instance.error,
                        }
                    )

    if node.consumes.events == [APPROVAL_DECISION] and not collected:
        return None

    return ReadyNode(
        unit=unit,
        input={"collected": collected, "failed": failures},
        source_events=tuple(seqs),
    )


def _expected_instances(topology: Topology, state: RunState, producer: str) -> list[int] | None:
    """Which ordinals of ``producer`` a join must wait for.

    ``None`` means "not yet knowable" — a fan-out whose width has not been
    materialized, which is precisely when a join must not fire.
    """
    is_fan_out_target = any(f.target == producer for f in topology.fan_out_points)
    if not is_fan_out_target:
        incoming = topology.predecessors(producer)
        if not incoming or topology.node(producer).consumes.collect:
            return [0]
        # Sequential/fork/branch edges retain the source ordinal. Carry the
        # full expected width through every step until a Collect collapses it.
        ordinals: set[int] = set()
        for edge in incoming:
            upstream = _expected_instances(topology, state, edge.from_)
            if upstream is None:
                return None
            ordinals.update(upstream)
        return sorted(ordinals)

    source = next(f.node for f in topology.fan_out_points if f.target == producer)
    if source not in state.fan_out_counts:
        return None
    return list(range(state.fan_out_counts[source]))


# ── Step 5: skips ────────────────────────────────────────────────────────


def _skips(topology: Topology, state: RunState) -> list[Action]:
    """Record a path that can no longer be taken.

    A node is skipped only when *every* incoming edge is dead — which is what
    keeps a convergence point (two branch arms meeting) alive while either arm
    is still live.
    """
    out: list[Action] = []
    for node in topology.nodes:
        incoming = topology.predecessors(node.key)
        if not incoming:
            continue
        for instance in _skip_candidates(topology, state, node.key):
            existing = state.node(instance)
            if existing is not None and existing.status != "pending":
                continue
            ordinal = None if node.consumes.collect else instance.ordinal
            if all(_edge_is_dead(topology, state, edge, ordinal) for edge in incoming):
                out.append(
                    SkipNode(
                        unit=instance,
                        reason="no incoming path was taken",
                    )
                )
    return out


def _skip_candidates(topology: Topology, state: RunState, node_key: str) -> list[UnitKey]:
    return [unit_key(node_key, i) for i in (_expected_instances(topology, state, node_key) or [])]


def _edge_is_dead(
    topology: Topology, state: RunState, edge: TopologyEdge, ordinal: int | None = None
) -> bool:
    """An edge is dead when its event can never arrive.

    Every instance of the source counts, not just ordinal 0. A fan-out source
    has many, and under a concurrency cap some may not exist yet — so a single
    failed sibling must not declare the edge dead and skip the join that exists
    precisely to handle partial failure.
    """
    expected = _expected_instances(topology, state, edge.from_)
    if expected is None:
        return False  # fan-out width unknown; nothing can be ruled out yet
    if not expected:
        return _dead(topology, state, edge.from_)

    if ordinal is not None and edge.kind != "fan_out":
        expected = [i for i in expected if i == ordinal]

    for source_ordinal in expected:
        instance = state.node(unit_key(edge.from_, source_ordinal))
        # Missing means "not started yet" under a concurrency cap, not "gone".
        if instance is None or not instance.settled:
            return False

    # Every instance settled. The edge is dead only if none of them emitted this
    # event — which is exactly what an untaken branch arm looks like.
    return not any(
        e.source.node_key == edge.from_
        and e.event_type == edge.event
        and (ordinal is None or _target_unit(edge, e).ordinal == ordinal)
        for e in state.emitted
    )


def _dead(topology: Topology, state: RunState, node_key: str) -> bool:
    """A node with no instance is dead only if everything upstream is dead."""
    incoming = topology.predecessors(node_key)
    if not incoming:
        return False
    return all(_edge_is_dead(topology, state, edge) for edge in incoming)


# ── Step 6: finalization ─────────────────────────────────────────────────


def _finalize(topology: Topology, state: RunState) -> list[Action]:
    if state.pending_approvals:
        return []  # suspended on a human, not finished

    if any(n.status in ("ready", "running") for n in state.nodes.values()):
        return []

    for terminal in topology.terminals:
        instance = state.node(unit_key(terminal))
        if instance is not None and instance.status == "completed":
            return [CompleteRun(result=(instance.output or {}).get("result"))]

    failed = [n for n in state.nodes.values() if n.status == "failed"]
    if failed:
        first = failed[0]
        return [
            FailRun(
                error=(
                    f"node {first.unit.node_key!r} failed ({first.failure_class}): {first.error}"
                )
            )
        ]

    if not state.nodes:
        return []

    if all(n.settled for n in state.nodes.values()):
        return [FailRun(error="run stalled: no terminal node completed and no work remains")]
    return []


# ── Join policy ──────────────────────────────────────────────────────────


def check_min_success(topology: Topology, node_key: str, collected: int, failed: int) -> str | None:
    """Return an error when a join's declared minimum is not met.

    The author's code decides what a degraded result *means*; this is the
    declarative guard that stops a one-specialist report shipping by accident.
    """
    join = next((j for j in topology.join_points if j.node == node_key), None)
    if join is None or join.min_success is None:
        return None
    total = collected + failed
    if join.min_success == "all":
        if collected < total:
            return f"join {node_key!r} requires all {total} inputs, got {collected}"
        return None
    if collected < join.min_success:
        return (
            f"join {node_key!r} requires min_success={join.min_success}, got {collected} of {total}"
        )
    return None
