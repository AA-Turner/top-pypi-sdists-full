"""Compute phases (rollout, train, weight sync, eval) per rank as `phase` spans, one spans POST per
step (RL plan §3.3c, T5). Only `rollout` spans become trials, so phases cost no title or index."""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

#: The span type phases are stored as.
PHASE_SPAN_TYPE = "phase"
#: Spans per POST: the server's cap (`MAX_SPANS_PER_REQUEST`).
SPANS_MAX = 10_000


@dataclass(frozen=True)
class Phase:
    """What one rank (or engine) did over one interval of a step."""

    name: str  # rollout | train | weight_sync | eval | ... (the framework's word)
    started_at: datetime | str
    ended_at: datetime | str
    role: str | None = None  # trainer | rollout | engine | ...
    rank: int | None = None
    node: str | None = None
    gpus: tuple[int, ...] = ()
    attributes: Mapping[str, Any] = field(default_factory=dict)

    @classmethod
    def from_value(cls, value: Phase | Mapping[str, Any]) -> Phase:
        if isinstance(value, Phase):
            return value
        known = {name: value[name] for name in cls.__dataclass_fields__ if name in value}
        if "gpus" in known:
            known["gpus"] = tuple(int(gpu) for gpu in known["gpus"] or ())
        return cls(**known)


def _to_iso(value: datetime | str) -> str:
    return value.isoformat() if isinstance(value, datetime) else str(value)


def build_phase_spans(
    step: int, phases: Iterable[Phase | Mapping[str, Any]], *, epoch: int, make_id
) -> list[dict]:
    """The step's phases as span bodies. ``make_id(external_key)`` gives each a stable id, so a
    retried step addresses the same rows; the key carries the epoch, so a resume never collides."""
    spans = []
    for index, raw in enumerate(phases):
        phase = Phase.from_value(raw)
        key = f"phase:{epoch}:{step}:{phase.role or ''}:{phase.rank if phase.rank is not None else ''}:{phase.name}:{index}"
        attributes = {
            **dict(phase.attributes),
            "phase": phase.name,
            "role": phase.role,
            "rank": phase.rank,
            "node": phase.node,
            "gpus": list(phase.gpus),
        }
        spans.append(
            {
                "id": make_id(key),
                "span_type": PHASE_SPAN_TYPE,
                "name": phase.name,
                "step_index": step,
                "external_key": key,
                "status": "completed",
                "started_at": _to_iso(phase.started_at),
                "ended_at": _to_iso(phase.ended_at),
                "attributes": {name: value for name, value in attributes.items() if value is not None},
                "summary_metrics": {},
                "coords": {},
            }
        )
    return spans
