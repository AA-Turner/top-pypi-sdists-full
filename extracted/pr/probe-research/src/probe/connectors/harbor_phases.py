"""Harbor trial-phase -> span synthesis, and the coverage report over a trial.

DELIBERATELY NOT IN ``atif.py``. That module's contract is that expansion is a
pure function of the stored ``trajectory.json`` bytes, which is what makes
``probe trial expand`` re-runnable years later. Phase timings come from
``result.json``, a different artifact. Folding them into the trajectory parser
would mean a re-expansion silently produced different spans depending on which
files happened to still be around.

WHAT A TRIAL'S WALL CLOCK IS MADE OF
------------------------------------

Harbor records four phase intervals and the trial's own start/end. It does NOT
record what happens between the phases, and it does not record the tail after
verification -- but both are measured, because they are the complement of
intervals it did record::

    trial              [==================================================]
      environment_setup [==]
      agent_setup           [========]
                                     ><  gap  (orchestration)
      agent_execution           [==================]
                                                   ><   gap  (log download)
      verifier                                       [=====]
                                                            [=========]  gap
                                                                (teardown)

The gap spans are named ``unattributed_gap``, never named for the cause. Reading
Harbor's control flow shows what CAN run in an interval; it cannot show that
nothing else did. The likely cause rides as an ATTRIBUTE with its provenance
attached, so a reader can weigh it and a future Harbor reorder makes an
attribute stale rather than making a span name a lie.

COVERAGE IS A UNION, NOT A SUM
------------------------------

``sum(child durations) == parent duration`` is the wrong check: it double-counts
any overlap and it hard-fails on a cancelled or partially captured trial. What
this module reports instead is the UNION of the direct-child intervals against
the trial extent, plus the overlaps it found. A trial that does not add up is
described, not repaired.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from .atif import PlannedSpan, _aware, _elapsed_ms

#: Span types this module emits. Open vocabulary on the wire; the dashboard's
#: ``SpanType`` mirrors these.
SPAN_TYPE_PHASE = "phase"
SPAN_TYPE_GAP = "unattributed_gap"

#: The phases Harbor records, in the order it runs them. Order here is
#: documentation and the basis of the ``likely_cause`` lookup -- the spans
#: themselves are ordered by what was MEASURED, never by this tuple.
PHASE_ORDER = ("environment_setup", "agent_setup", "agent_execution", "verifier")

#: Provenance for a phase span: Harbor measured the extent AND named it.
PHASE_SOURCE_HARBOR = "harbor_result"

#: Provenance for a gap: the extent is measured (it is the complement of two
#: recorded intervals) but nothing names it.
GAP_SOURCE_MEASURED = "measured_complement"

#: Provenance for the ``likely_cause`` attribute specifically -- read out of
#: Harbor's control flow at the pinned version, NOT reported by Harbor.
CAUSE_SOURCE_CONTROL_FLOW = "inferred_harbor_control_flow"

#: The Harbor range whose control flow the ``likely_cause`` table was read from.
#: ``tests/test_harbor_phases.py`` asserts this still matches the pin in
#: ``agent/pyproject.toml`` -- widen one and the guard fails loudly rather than
#: letting a reorder turn the causes into confident fiction.
CAUSE_HARBOR_RANGE = ">=0.20,<0.22"

#: What runs in each gap, by the phases that bracket it. Read from Harbor
#: 0.21.0: ``trial.py:408`` ``_prepare()`` then ``:456`` ``AGENT_START``;
#: ``single_step.py:87`` finally -> ``trial.py:721`` ``_sync_agent_output`` ->
#: ``_download_agent_logs``; ``trial.py:417`` ``_finalize()`` runs
#: ``_stop_agent_environment()`` and only then stamps ``finished_at``.
_LIKELY_CAUSE: dict[tuple[str | None, str | None], str] = {
    (None, "environment_setup"): "trial start before environment setup",
    ("environment_setup", "agent_setup"): "environment healthcheck and skill upload",
    ("agent_setup", "agent_execution"): "trial orchestration between setup and agent start",
    ("agent_execution", "verifier"): "agent log download from the sandbox",
    ("verifier", None): "environment teardown before the trial is stamped finished",
}

#: Harbor records four phases. A manifest carrying hundreds is a malformed or
#: hostile producer, and `_overlaps` is O(n^2) over whatever it is handed, so
#: the pair scan gets a ceiling rather than the producer's word for it.
MAX_PHASES = 32

#: Gaps shorter than this are clock noise, not work. The real
#: ``marshmallow-code__apispec`` trial has a 39-microsecond seam between
#: ``environment_setup`` and ``agent_setup``; a span for that is a row of
#: nothing in every timeline forever.
MIN_GAP_MS = 1


#: Sort floor for a plan with no parseable start. Never rendered; it only keeps
#: the key total so one unparseable stamp cannot raise TypeError mid-sort.
_EPOCH = datetime.min.replace(tzinfo=timezone.utc)


def _parse(value: Any) -> datetime | None:
    """A tz-aware datetime, or ``None`` for anything we will not order on."""
    text = _aware(value)
    if text is None:
        return None
    try:
        return datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError:
        return None


class _Interval:
    """One measured [start, end] with the label it was recorded under."""

    __slots__ = ("name", "start", "end", "start_text", "end_text")

    def __init__(self, name: str, start: datetime, end: datetime, start_text: str, end_text: str):
        self.name = name
        self.start = start
        self.end = end
        self.start_text = start_text
        self.end_text = end_text


def _clip(
    intervals: list[_Interval], start: datetime | None, end: datetime | None
) -> list[_Interval]:
    """Drop phases that fall outside the trial they claim to belong to.

    A phase ending before the trial began, or starting after it ended, is a
    producer error. Emitting it anyway stretches the timeline's whole window to
    fit a span that cannot have happened, which rescales every other bar in the
    run to nothing.
    """
    if start is None and end is None:
        return intervals
    kept = []
    for iv in intervals:
        if end is not None and iv.start > end:
            continue
        if start is not None and iv.end < start:
            continue
        kept.append(iv)
    return kept


def _phase_intervals(phases: Any) -> list[_Interval]:
    """Closed, non-negative phase intervals in MEASURED order.

    A phase missing either side is dropped, not guessed at: Harbor leaves
    ``finished_at`` unset on a phase that was still running when the trial died,
    and an open interval has no extent to draw. A phase whose clock ran backwards
    is dropped for the same reason ``_elapsed_ms`` refuses a negative delta --
    that is corrupt input, not a short phase.
    """
    if not isinstance(phases, dict):
        return []
    out: list[_Interval] = []
    for name, timing in phases.items():
        if not isinstance(timing, dict):
            continue
        start_text = _aware(timing.get("started_at"))
        end_text = _aware(timing.get("finished_at"))
        start, end = _parse(start_text), _parse(end_text)
        if start is None or end is None or end < start:
            continue
        out.append(_Interval(str(name), start, end, start_text, end_text))
    out.sort(key=lambda i: (i.start, i.end))
    return out[:MAX_PHASES]


def _merge(intervals: list[_Interval]) -> list[tuple[datetime, datetime]]:
    """Union of the intervals, as disjoint spans in ascending order."""
    merged: list[tuple[datetime, datetime]] = []
    for iv in intervals:
        if merged and iv.start <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(merged[-1][1], iv.end))
        else:
            merged.append((iv.start, iv.end))
    return merged


def _overlaps(intervals: list[_Interval]) -> list[dict[str, Any]]:
    """Pairs of phases that claim the same wall clock. Reported, never repaired."""
    found: list[dict[str, Any]] = []
    for index, iv in enumerate(intervals):
        for other in intervals[index + 1 :]:
            if other.start >= iv.end:
                break
            overlap_ms = _elapsed_ms(other.start_text, min(iv.end, other.end).isoformat())
            found.append(
                {"phases": [iv.name, other.name], "overlap_ms": overlap_ms or 0}
            )
    return found


def _iso(value: datetime) -> str:
    return value.isoformat().replace("+00:00", "Z")


def plan_phase_spans(
    phases: Any,
    *,
    trial_started_at: str | None,
    trial_ended_at: str | None,
) -> tuple[list[PlannedSpan], dict[str, Any]]:
    """Phase and gap spans for one trial, plus the coverage report over them.

    Returns ``([], report)`` when there is nothing measurable -- a synthetic
    fixture with no ``phases`` block, or a trial whose own extent was never
    stamped. That is the honest empty answer: with no phases recorded, a single
    gap covering the whole trial would assert that we know nothing happened,
    which is a different claim from not knowing.

    Every span is closed (both ends measured) and carries no ``elapsed_ms``:
    these are the only spans in the tree whose duration is a subtraction of two
    recorded stamps rather than an inference, and mixing them into the inferred
    vocabulary would erase exactly the distinction that makes them useful.
    """
    trial_start = _parse(trial_started_at)
    trial_end = _parse(trial_ended_at)
    intervals = _clip(_phase_intervals(phases), trial_start, trial_end)

    report: dict[str, Any] = {
        "phases": len(intervals),
        "gaps": 0,
        "overlaps": _overlaps(intervals),
        "covered_ms": 0,
        "trial_ms": None,
        "state": "no_phases" if not intervals else "complete",
    }
    if not intervals:
        return [], report

    plans: list[PlannedSpan] = []
    for iv in intervals:
        plans.append(
            PlannedSpan(
                path=f"phase/{iv.name}",
                span_type=SPAN_TYPE_PHASE,
                name=iv.name,
                parent_path=None,
                started_at=iv.start_text,
                ended_at=iv.end_text,
                attributes={
                    "phase": iv.name,
                    "timing_source": PHASE_SOURCE_HARBOR,
                },
            )
        )

    gap_count = 0
    merged = _merge(intervals)
    report["covered_ms"] = sum(
        _elapsed_ms(_iso(start), _iso(end)) or 0 for start, end in merged
    )

    # Gaps are the complement of the union inside the trial's own extent. With
    # no trial extent we can still describe the seams BETWEEN phases; we just
    # cannot know about a lead-in or a tail, so we do not invent them.
    edges: list[tuple[datetime | None, datetime | None]] = []
    if trial_start is not None and trial_start < merged[0][0]:
        edges.append((trial_start, merged[0][0]))
    for index in range(len(merged) - 1):
        edges.append((merged[index][1], merged[index + 1][0]))
    if trial_end is not None and trial_end > merged[-1][1]:
        edges.append((merged[-1][1], trial_end))

    for start, end in edges:
        if start is None or end is None or end <= start:
            continue
        start_text, end_text = _iso(start), _iso(end)
        extent = _elapsed_ms(start_text, end_text)
        if extent is None or extent < MIN_GAP_MS:
            continue
        before = next((iv.name for iv in reversed(intervals) if iv.end <= start), None)
        after = next((iv.name for iv in intervals if iv.start >= end), None)
        # Identity comes from the phases the gap sits BETWEEN, not from a
        # counter. `gap/0` silently means a different interval the moment an
        # earlier phase appears or disappears, and nothing deletes the row it
        # used to name -- so a re-capture would leave a stale span behind
        # wearing an id that now belongs to different wall clock.
        path = f"gap/{before or 'start'}~{after or 'end'}"
        attributes: dict[str, Any] = {
            "timing_source": GAP_SOURCE_MEASURED,
            "after_phase": before,
            "before_phase": after,
        }
        cause = _LIKELY_CAUSE.get((before, after))
        if cause:
            attributes["likely_cause"] = cause
            attributes["cause_source"] = CAUSE_SOURCE_CONTROL_FLOW
            attributes["cause_harbor_range"] = CAUSE_HARBOR_RANGE
        plans.append(
            PlannedSpan(
                path=path,
                span_type=SPAN_TYPE_GAP,
                name="unattributed",
                parent_path=None,
                started_at=start_text,
                ended_at=end_text,
                attributes={k: v for k, v in attributes.items() if v is not None},
            )
        )
        gap_count += 1

    report["gaps"] = gap_count
    if trial_start is not None and trial_end is not None and trial_end >= trial_start:
        report["trial_ms"] = _elapsed_ms(_iso(trial_start), _iso(trial_end))
    if report["overlaps"]:
        report["state"] = "overlapping"
    elif report["trial_ms"] is None:
        report["state"] = "unbounded_trial"

    # Sorting on the ISO STRING would order "…T10:00+02:00" before
    # "…T09:00Z" even though the second instant is later. Same trap the
    # interval scan already avoids by comparing parsed datetimes.
    plans.sort(key=lambda p: (_parse(p.started_at) or _EPOCH, p.path))
    return plans, report


def agent_execution_path(plans: list[PlannedSpan]) -> str | None:
    """The plan path of the ``agent_execution`` phase, if it was measured.

    This is what the trajectory expansion reparents turns onto. ``None`` means
    the phase was never closed -- a crashed trial -- and turns stay directly
    under the rollout rather than being hung off a phase that has no extent.
    """
    for plan in plans:
        if plan.span_type == SPAN_TYPE_PHASE and plan.name == "agent_execution":
            return plan.path
    return None


def agent_execution_bounds(plans: list[PlannedSpan]) -> tuple[str | None, str | None]:
    """``(started_at, ended_at)`` of the agent_execution phase, or ``(None, None)``.

    The end is what bounds the LAST ATIF turn, which otherwise has no next
    sibling to infer an extent from and renders as a point forever.
    """
    for plan in plans:
        if plan.span_type == SPAN_TYPE_PHASE and plan.name == "agent_execution":
            return plan.started_at, plan.ended_at
    return None, None
