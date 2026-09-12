"""Facts — the append-only durable truth of a run.

A fact is immutable and per-run sequenced. Facts are the durable state *and* the
audit trail: the same object, not one derived from the other. A ``WorkflowEvent``
emitted by a step is recorded as an ``event_emitted`` fact, which is what makes
the authoring surface and the storage model the same idea at two altitudes.

``seq`` is assigned by the **executing host** — the only party that knows
execution order. The platform accepts appends idempotently on ``(run, seq)`` and
folds only a gap-free prefix, so a run page is always *behind*, never *wrong*.

Nothing in this module does I/O or reads a clock. ``occurred_at`` is supplied by
the caller so the fold stays pure and exhaustively testable.
"""

import re
import typing as t
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

__all__ = [
    "Fact",
    "FactKind",
    "UnitKey",
    "parse_unit",
    "unit_key",
]

FactKind = t.Literal[
    "run_started",
    "node_ready",
    "node_started",
    "event_emitted",
    "node_output",
    "node_failed",
    "node_skipped",
    "node_log",
    "fan_out_materialized",
    "agent_session_started",
    "approval_requested",
    "approval_decided",
    "run_cancelled",
    "run_completed",
    "run_failed",
]


class UnitKey(t.NamedTuple):
    """Identity of one node *instance*.

    ``iteration`` is always 0 in v1 and is carried here as the loop reservation —
    the projection's unique key includes it from the first migration precisely so
    bounded loops are additive rather than a migration on the largest table.
    """

    node_key: str
    ordinal: int = 0
    iteration: int = 0

    def __str__(self) -> str:
        return f"{self.node_key}:{self.ordinal}:{self.iteration}"


def unit_key(node_key: str, ordinal: int = 0, iteration: int = 0) -> UnitKey:
    return UnitKey(node_key, ordinal, iteration)


def parse_unit(raw: str) -> UnitKey:
    if len(raw) > 255 or not re.fullmatch(r"[a-z][a-z0-9_]*:[0-9]+:[0-9]+", raw):
        raise ValueError("unit key must be node_key:ordinal:iteration with nonnegative indices")
    node_key, ordinal, iteration = raw.rsplit(":", 2)
    parsed = UnitKey(node_key, int(ordinal), int(iteration))
    if max(parsed.ordinal, parsed.iteration) > 2**31 - 1:
        raise ValueError("unit key indices exceed the supported integer range")
    return parsed


class Fact(BaseModel):
    """One immutable record in a run's log.

    Payload shapes by kind:

    ``run_started``            ``{"input": {...}}``
    ``node_ready``             ``{"input": {...}}``
    ``node_started``           ``{}``
    ``event_emitted``          ``{"event_type": str, "data": {...}, "index": int}``
    ``node_output``            ``{"event_type": str, "data": {...}}``
    ``node_failed``            ``{"failure_class": str, "error": str}``
    ``node_skipped``           ``{"reason": str}``
    ``node_log``               ``{"message": str, "fields": {...}}``
    ``fan_out_materialized``   ``{"count": int, "event_type": str}``
    ``agent_session_started``  ``{"session_id": str}``
    ``approval_requested``     ``{"summary": str, "payload": {...}}``
    ``approval_decided``       ``{"outcome": str, "decided_by": str | None}``
    ``run_cancelled``          ``{"reason": str}``
    ``run_completed``          ``{"result": Any}``
    ``run_failed``             ``{"error": str}``
    """

    model_config = ConfigDict(extra="forbid")

    seq: int
    kind: str
    """Deliberately ``str``, not ``FactKind``.

    Adding a fact kind is a *compatibility event*: an older reader must be able
    to load a newer log and ignore what it does not recognise. A strict Literal
    would reject such a fact at construction, which turns a forward-compatible
    addition into a hard break. Producers should use :data:`FactKind`; readers
    must tolerate anything.
    """
    unit_key: str | None = None
    """The raw ``node_key:ordinal:iteration`` string, matching the
    ``workflow_facts.unit_key`` column. :attr:`unit` is the parsed form."""
    attempt: int = 1
    payload: dict[str, t.Any] = Field(default_factory=dict)
    occurred_at: datetime | None = None
    idempotency_key: str | None = None

    @property
    def unit(self) -> UnitKey | None:
        """The parsed identity, or ``None`` for run-level facts."""
        return parse_unit(self.unit_key) if self.unit_key else None
