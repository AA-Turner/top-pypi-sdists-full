"""The fold — facts in, state out.

``fold(facts)`` reduces the append-only log into the current state of a run. It
is the same shape as the ``workflow_run_nodes`` projection, and the projection is
maintained incrementally from the same logic, which is why
``rebuild-projection`` must be a no-op diff (acceptance gate 2).

**Recovery is a fold, not a replay.** On restart we re-read facts and rebuild
state; we never re-execute a step body to get back to where we were. Because no
user code runs during recovery there is no determinism contract on author code —
the requirement that rules out DBOS, Temporal, and Dapr does not apply to us.

Pure: no I/O, no clock, no randomness.
"""

import typing as t
from dataclasses import dataclass, field
from datetime import datetime

from dreadnode_workflow_core.events import FailureClass
from dreadnode_workflow_core.facts import Fact, UnitKey, parse_unit

__all__ = [
    "EmittedEvent",
    "NodeState",
    "RunState",
    "fold",
    "fold_incremental",
]

NodeStatus = t.Literal[
    "pending",
    "ready",
    "running",
    "awaiting_approval",
    "completed",
    "failed",
    "skipped",
    "cancelled",
]
RunStatus = t.Literal["pending", "running", "suspended", "completed", "failed", "cancelled", "lost"]

TERMINAL_NODE_STATUSES: frozenset[str] = frozenset({"completed", "failed", "skipped", "cancelled"})
"""A node instance is *settled* when it reaches one of these — which is what a
join waits for, rather than waiting for success. Partial failure is a first-class
case, not an edge case."""


@dataclass
class NodeState:
    """One node instance, folded."""

    unit: UnitKey
    status: NodeStatus = "pending"
    input: dict[str, t.Any] | None = None
    output: dict[str, t.Any] | None = None
    output_event_type: str | None = None
    session_id: str | None = None
    agent: str | None = None
    """Which agent this instance actually ran.

    A step that calls ``ctx.agent(ev.agent, ...)`` has no statically knowable
    agent — the topology can only say ``agents_dynamic``. The *run* knows
    exactly, because the name reached the runtime, so record it here rather than
    leaving a fan-out of five specialists rendered as five identical rows."""
    agent_sessions: list[dict[str, t.Any]] = field(default_factory=list)
    """Every agent session this instance opened, in order.

    A step may call ``ctx.agent()`` more than once, and each call opens its own
    session. ``session_id`` and ``agent`` hold the *most recent* — which is what
    the transcript pane shows — but they used to be the only record, so earlier
    calls were silently unreachable from the projection even though the fact log
    kept them. This is the full list.
    """
    attempts: int = 0
    failure_class: FailureClass | None = None
    error: str | None = None
    skipped_reason: str | None = None
    last_fact_seq: int = 0
    started_at: datetime | None = None
    finished_at: datetime | None = None

    @property
    def settled(self) -> bool:
        return self.status in TERMINAL_NODE_STATUSES

    @property
    def succeeded(self) -> bool:
        return self.status == "completed"


@dataclass
class EmittedEvent:
    """One event a step emitted, and where it came from.

    ``index`` is the position within a fan-out (0 for everything else), and is
    what gives a downstream instance its ordinal.
    """

    seq: int
    source: UnitKey
    event_type: str
    data: dict[str, t.Any]
    index: int = 0


@dataclass
class RunState:
    """Everything the scheduler needs, and nothing it does not."""

    status: RunStatus = "pending"
    input: dict[str, t.Any] = field(default_factory=dict)
    nodes: dict[UnitKey, NodeState] = field(default_factory=dict)
    emitted: list[EmittedEvent] = field(default_factory=list)
    fan_out_counts: dict[str, int] = field(default_factory=dict)
    """``node_key`` → how many instances a fan-out materialized."""
    approvals: dict[UnitKey, str] = field(default_factory=dict)
    """Gate unit → outcome, once decided."""
    pending_approvals: set[UnitKey] = field(default_factory=set)
    result: t.Any = None
    error: str | None = None
    last_seq: int = 0

    # ── Queries the scheduler leans on ───────────────────────────────────

    def node(self, unit: UnitKey) -> NodeState | None:
        return self.nodes.get(unit)

    def instances_of(self, node_key: str) -> list[NodeState]:
        return [n for n in self.nodes.values() if n.unit.node_key == node_key]

    def running_count(self, node_key: str) -> int:
        return sum(
            1
            for n in self.nodes.values()
            if n.unit.node_key == node_key and n.status in ("running", "ready")
        )

    def events_from(self, node_key: str, event_type: str) -> list[EmittedEvent]:
        return [
            e for e in self.emitted if e.source.node_key == node_key and e.event_type == event_type
        ]

    def is_terminal(self) -> bool:
        return self.status in ("completed", "failed", "cancelled", "lost")


def fold(facts: t.Iterable[Fact]) -> RunState:
    """Reduce a fact sequence into current state.

    Facts must arrive in ``seq`` order and gap-free; the caller is responsible for
    applying only a contiguous prefix. Unknown fact kinds are *tolerated and
    ignored* so an older fold can read a newer log — adding a kind is a
    compatibility event, not a break.
    """
    return fold_incremental(RunState(), facts)


def fold_incremental(state: RunState, facts: t.Iterable[Fact]) -> RunState:
    """Apply more facts to an existing state, in place.

    This is the same code path the projection maintainer uses, which is what
    makes ``rebuild-projection`` a diff rather than a second implementation.
    """
    for fact in facts:
        if fact.seq <= state.last_seq:
            continue  # idempotent: a redelivered fact is a no-op
        _apply(state, fact)
        state.last_seq = fact.seq
    return state


def _apply(state: RunState, fact: Fact) -> None:
    kind = fact.kind
    unit = parse_unit(fact.unit_key) if fact.unit_key else None

    if kind == "run_started":
        state.status = "running"
        state.input = dict(fact.payload.get("input") or {})
        return

    if kind == "run_cancelled":
        state.status = "cancelled"
        state.error = fact.payload.get("reason")
        for node in state.nodes.values():
            if not node.settled:
                node.status = "cancelled"
        return

    if kind == "run_completed":
        state.status = "completed"
        state.result = fact.payload.get("result")
        return

    if kind == "run_failed":
        state.status = "failed"
        state.error = fact.payload.get("error")
        return

    if kind == "fan_out_materialized":
        node_key = fact.payload.get("node_key") or (unit.node_key if unit else "")
        state.fan_out_counts[node_key] = int(fact.payload.get("count", 0))
        return

    if kind == "approval_decided":
        if unit is not None:
            state.approvals[unit] = str(fact.payload.get("outcome"))
            state.pending_approvals.discard(unit)
            node = state.nodes.get(unit)
            if node is not None and node.status == "awaiting_approval":
                node.status = "completed"
        if state.status == "suspended":
            state.status = "running"
        return

    if unit is None:
        return

    node = state.nodes.get(unit)
    if node is None:
        node = NodeState(unit=unit)
        state.nodes[unit] = node
    node.last_fact_seq = fact.seq

    if kind == "node_ready":
        node.status = "ready"
        node.input = fact.payload.get("input")
    elif kind == "node_started":
        node.status = "running"
        node.attempts = max(node.attempts, fact.attempt)
        node.started_at = node.started_at or fact.occurred_at
    elif kind == "agent_session_started":
        # Recorded at agent *start*, so a node that fails or times out mid-agent
        # still links to its partial transcript.
        session_id = fact.payload.get("session_id")
        agent = fact.payload.get("agent")
        # Last wins for the primary pair; every call is kept in the list.
        node.session_id = session_id
        node.agent = agent
        node.agent_sessions.append({"session_id": session_id, "agent": agent})
    elif kind == "event_emitted":
        state.emitted.append(
            EmittedEvent(
                seq=fact.seq,
                source=unit,
                event_type=str(fact.payload.get("event_type")),
                data=dict(fact.payload.get("data") or {}),
                index=int(fact.payload.get("index", 0)),
            )
        )
    elif kind == "node_output":
        node.status = "completed"
        node.output = fact.payload.get("data")
        node.output_event_type = fact.payload.get("event_type")
        node.finished_at = fact.occurred_at
    elif kind == "node_failed":
        node.status = "failed"
        node.failure_class = fact.payload.get("failure_class") or "error"
        node.error = fact.payload.get("error")
        node.finished_at = fact.occurred_at
    elif kind == "node_skipped":
        node.status = "skipped"
        node.skipped_reason = fact.payload.get("reason")
        node.finished_at = fact.occurred_at
    elif kind == "approval_requested":
        node.status = "awaiting_approval"
        state.pending_approvals.add(unit)
        state.status = "suspended"
    # Unknown kinds fall through untouched, on purpose.
