"""A scripted agent-theater run for the keyless Studio demo.

The live agent theater needs an LLM key + a scanned workspace. So that
anyone can *see* the theater (and to give the cold-open its second beat),
this generates a realistic, deterministic sequence of the same typed
events a real gap run emits — batches of KSIs being classified, verdicts
landing — with plausible verdicts derived from each KSI's structural
category. It is clearly a DEMO (the app labels it as such); it is NOT a
real classification of anyone's system.

This is distinct from the Phase-2 honest replay (a recording of a real
run); this is synthetic sample data for first-touch.
"""

from __future__ import annotations

import random

from efterlev.events.schema import (
    AgentFinished,
    AgentStarted,
    BatchStarted,
    KsiClassified,
    StudioEvent,
)

_BATCH = 5

# Per structural category, the plausible verdict mix for a sample run.
_VERDICT_WEIGHTS: dict[str, list[tuple[str, float]]] = {
    "scanner": [("implemented", 0.6), ("partial", 0.25), ("not_implemented", 0.15)],
    "hybrid": [("implemented", 0.4), ("partial", 0.45), ("not_implemented", 0.15)],
    "procedural": [
        ("not_implemented", 0.5),
        ("evidence_layer_inapplicable", 0.3),
        ("partial", 0.2),
    ],
    "uncovered": [("not_implemented", 0.7), ("not_applicable", 0.3)],
}


def _pick(rng: random.Random, category: str) -> str:
    weights = _VERDICT_WEIGHTS.get(category, _VERDICT_WEIGHTS["uncovered"])
    r = rng.random()
    cum = 0.0
    for status, w in weights:
        cum += w
        if r <= cum:
            return status
    return weights[-1][0]


def demo_events(categories: dict[str, str], *, seed: int = 23) -> list[StudioEvent]:
    """Build a deterministic sample agent-run event sequence.

    `categories` maps each KSI to its structural category (from the
    catalog). Returns the event list in emission order, batched like a
    real run (5 KSIs per batch).
    """
    rng = random.Random(seed)
    ksis = sorted(categories)
    events: list[StudioEvent] = [AgentStarted(agent="gap (demo)", total_ksis=len(ksis))]
    batches = [ksis[i : i + _BATCH] for i in range(0, len(ksis), _BATCH)]
    total = len(batches)
    counts: dict[str, int] = {}
    for idx, batch in enumerate(batches, start=1):
        events.append(BatchStarted(index=idx, total=total, ksis=list(batch)))
        for ksi in batch:
            status = _pick(rng, categories.get(ksi, "uncovered"))
            counts[status] = counts.get(status, 0) + 1
            ev_count = rng.randint(1, 4) if status in ("implemented", "partial") else 0
            events.append(KsiClassified(ksi=ksi, status=status, evidence_count=ev_count))
    events.append(AgentFinished(counts=counts))
    return events
