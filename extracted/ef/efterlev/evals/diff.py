"""Delta-vs-prior reporter for the eval harness.

After each `python -m evals run`, the harness writes a metrics.json
under `evals/results/<fixture_id>/<timestamp>/metrics.json`. The diff
module reads the prior run (if any) for the same fixture and produces
a per-metric delta report.

Phase 1 ships the diff as a print-to-stdout block at the end of the
`run` summary. Phase 3 (when the eval harness becomes a required CI
check) reuses the same diff to produce PR-comment annotations.

Per the DECISIONS entry, Phase 1 is yellow-flag-not-hard-block: a
metric drop > 5% (the noise-floor estimate) gets a warning emoji
but doesn't fail the run. Phase 3 hard-blocks once the noise floor
is calibrated against ≥ 4 weeks of trend data.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

# Per the DECISIONS entry: ±5% per-metric noise floor at Phase 1.
# Drops greater than this threshold warrant a yellow flag in the
# delta output. Phase 3 will calibrate a real floor from trend data
# and convert the yellow flag into a hard block.
NOISE_FLOOR = 0.05


@dataclass(frozen=True)
class MetricDelta:
    """Per-metric delta vs the prior run on the same fixture."""

    name: str
    prior_score: float | None
    current_score: float
    delta: float | None  # current - prior; None if no prior

    @property
    def is_yellow_flag(self) -> bool:
        """True when the delta represents a regression worth surfacing.
        Per the DECISIONS entry's yellow-flag-not-hard-block discipline:
        any drop > NOISE_FLOOR earns the flag. Improvements never flag.
        """
        return self.delta is not None and self.delta < -NOISE_FLOOR


def _find_prior_metrics(
    results_root: Path,
    current_timestamp: str,
) -> Path | None:
    """Find the most-recent metrics.json under `results_root` that is
    NOT the current run's. Returns None if no prior run exists yet
    (the typical state on the first eval run for a new fixture).

    Layout assumption: `results_root/<timestamp>/metrics.json`.
    Sort lexically by timestamp (which is YYYYMMDDTHHMMSSZ -- sortable).
    """
    if not results_root.is_dir():
        return None
    candidates = sorted(
        p for p in results_root.glob("*/metrics.json") if p.parent.name != current_timestamp
    )
    return candidates[-1] if candidates else None


def compute_deltas(
    current_metrics_path: Path,
    results_root: Path,
) -> list[MetricDelta]:
    """Return per-metric MetricDeltas comparing the current run vs the
    most recent prior run on the same fixture. Empty list if there's
    no prior run (every run is a baseline-of-one until the second).

    Robust to schema additions: a metric present in current but absent
    in prior reports `prior_score=None`; a metric in prior but absent
    in current is dropped (PR gamma adding M5 means the first post-gamma run's
    delta omits M5 from the prior side, surfacing as `prior=None`).
    """
    current_data = json.loads(current_metrics_path.read_text(encoding="utf-8"))
    current_by_name = {m["name"]: m["score"] for m in current_data.get("metrics", [])}

    prior_path = _find_prior_metrics(results_root, current_data.get("timestamp", ""))
    if prior_path is None:
        return [
            MetricDelta(name=name, prior_score=None, current_score=score, delta=None)
            for name, score in current_by_name.items()
        ]

    prior_data = json.loads(prior_path.read_text(encoding="utf-8"))
    prior_by_name = {m["name"]: m["score"] for m in prior_data.get("metrics", [])}

    deltas: list[MetricDelta] = []
    for name, current_score in current_by_name.items():
        prior_score = prior_by_name.get(name)
        delta = (current_score - prior_score) if prior_score is not None else None
        deltas.append(
            MetricDelta(
                name=name,
                prior_score=prior_score,
                current_score=current_score,
                delta=delta,
            )
        )
    return deltas


def format_delta_block(deltas: list[MetricDelta]) -> str:
    """Format the deltas as a multi-line text block for the run
    summary. Yellow-flag rows get a leading `!` indicator; first-run
    rows get a `*`; unchanged rows are unmarked.
    """
    if not deltas:
        return "(no prior run; this is the baseline)"

    has_prior = any(d.prior_score is not None for d in deltas)
    if not has_prior:
        return "(no prior run on this fixture; this is the baseline)"

    lines = ["delta vs prior run:"]
    for d in deltas:
        if d.delta is None:
            marker = "*"  # new metric (no prior baseline)
            change = "  (new metric)"
        elif d.is_yellow_flag:
            marker = "!"
            change = f"  {d.delta:+.3f}  (regression > noise floor {NOISE_FLOOR})"
        else:
            marker = " "
            change = f"  {d.delta:+.3f}"
        lines.append(f"  {marker} {d.name:24s} {d.current_score:.3f}{change}")
    return "\n".join(lines)
