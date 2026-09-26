"""``attribute_count`` -- counts by the value of a decoded second-stage attribute.

Normative source: ``classification-primitives.md`` §5.2. The counting half of every
chained-classifier app: ``vehicle_type_classification``'s ``vehicle_type_counts``
(``:1007-1014``), ``age_gender_detection``'s per-gender counts, ``face_emotion``'s
per-emotion counts. Reads :attr:`~matrice_analytics.engine.primitives.base.
PipelineDetection.attributes`, which :mod:`matrice_analytics.engine.intake.attributes`
decoded at intake; this primitive never looks at a pixel and never runs a model, because the
classifier is chained upstream (``classification-primitives.md`` P0).

**Counting absence is the feature.** ``unknown_count`` / ``other_count`` are what turn a dead
classifier chain from "every value bucket reads zero forever" into a number an operator can
alarm on. Legacy writes the string ``"unknown"`` into the same keyspace as the real labels
(``vehicle_type_classification.py:955``, ``:1009``) and cannot tell "no ambulances today" from
"the classifier has been dead since Tuesday" apart.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import ClassVar

from matrice_analytics.engine.manifest.models import AttributeCountConfig
from matrice_analytics.engine.primitives.base import (
    FrameContext,
    PipelineDetection,
    PrimitiveOutput,
    Scalar,
    WindowOutput,
    register,
)
from matrice_analytics.engine.state import Lifetime, StateStore

__all__ = ["AttributeCount"]


@register(name="attribute_count")
class AttributeCount:
    """Per-value counts of one decoded attribute, for one zone, one frame.

    Outputs (:attr:`~matrice_analytics.engine.primitives.base.PrimitiveOutput.values`), each
    resolvable as ``<stage>.<name>``:

    ``<value>.count``
        Detections of ``subject`` in this zone counted as ``<value>``. For a tracked
        subject, this is a same-attribute ``attribute_vote`` stage's stabilised decision
        when one ran earlier in the pipeline (see :meth:`_resolve`); otherwise the raw
        intake-decoded attribute, gated by ``min_confidence``.
    ``<value>.new``
        Tracks resolved to ``<value>`` for the **first time ever** during this window --
        a WINDOW-lifetime event count, disjoint per frame, so ``metrics[].agg_type: sum``
        over it reproduces the window figure exactly. Mirrors ``unique_count``'s own
        ``new``/``total`` split and its explicit philosophy: once a track's first-ever
        decision for this attribute is counted, it is never counted again -- not on a
        later frame with the same value, and not if the value later switches (an
        ``attribute_vote`` ``switch_count``). Retroactively moving a track's ``.new``
        event to a different value after a switch would un-sum an already-reported
        window, which is exactly the invariant ``unique_count``'s own docstring refuses
        to break for the same reason. Untracked detections (no ``track_id``) cannot be
        deduplicated and never contribute here, same as ``unique_count``.
    ``other_new``
        The ``.new`` counterpart to ``other_count`` -- first-ever decisions whose label
        is real but not in ``values``.
    ``labelled_count``
        How many carried *any* declared value. Sum of the per-value counts.
    ``unknown_count``
        Subjects carrying **no** attribute, or one below ``min_confidence``.
    ``other_count``
        Subjects whose label is real but not in ``values`` -- the vocabulary-drift signal.
    ``instance_count``
        All subjects in this zone this frame, labelled or not. The denominator.
    ``max_confidence``
        The highest attribute confidence this frame; a health diagnostic, not a metric.

    **``unknown_count == instance_count`` is the classifier-outage signal.**  A dead
    classifier chain and a frame full of unclassifiable crops look identical in per-value
    counts alone, so this primitive counts absence explicitly rather than letting every
    bucket read ``0``.

    Not here, on purpose: temporal stabilisation (``attribute_vote``), banding a numeric
    attribute (``attribute_band``), uniqueness over time (``unique_count``, which dedupes on
    ``(entity, track_id)`` and is unchanged by any of this), and severity
    (``incident_quantise``).
    """

    name: ClassVar[str] = "attribute_count"
    Config: ClassVar[type[AttributeCountConfig]] = AttributeCountConfig

    __slots__ = ("_attribute", "_config", "_min_confidence", "_state", "_subject", "_values")

    def __init__(self, config: AttributeCountConfig, state: StateStore) -> None:
        self._config = config
        self._state = state
        self._attribute = config.attribute
        self._subject: tuple[str, ...] = tuple(config.subject)
        self._values: tuple[str, ...] = tuple(config.values)
        self._min_confidence = float(config.min_confidence)

    def process(self, ctx: FrameContext) -> PrimitiveOutput:
        """Count this zone's subjects by attribute value for one frame.

        No clock call, no ``require_resolution`` -- but not "reads only ``ctx.detections``"
        any more: see :meth:`_resolve`.
        """
        detections = ctx.of_entity(*self._subject)
        per_value = dict.fromkeys(self._values, 0)
        new_per_value = dict.fromkeys(self._values, 0)
        unknown = other = other_new = 0
        best_confidence = 0.0
        active_ids: set[int] = set()

        for det in detections:
            label, confidence = self._resolve(ctx, det)
            if label is None:
                unknown += 1
                continue
            best_confidence = max(best_confidence, confidence)
            if label in per_value:
                per_value[label] += 1
            else:
                other += 1

            if det.track_id is None:
                continue  # can't be deduplicated -- never contributes to .new
            track_id = int(det.track_id)
            active_ids.add(track_id)
            if self._first_sighting(track_id):
                if label in new_per_value:
                    new_per_value[label] += 1
                else:
                    other_new += 1

        self._prune(ctx, active_ids)
        labelled = sum(per_value.values())
        self._accumulate(
            per_value,
            new_per_value,
            labelled,
            unknown,
            other,
            other_new,
            len(detections),
            best_confidence,
        )

        values: dict[str, Scalar] = {f"{value}.count": count for value, count in per_value.items()}
        values.update({f"{value}.new": count for value, count in new_per_value.items()})
        values.update(
            labelled_count=labelled,
            unknown_count=unknown,
            other_count=other,
            other_new=other_new,
            instance_count=len(detections),
            max_confidence=best_confidence,
        )
        return PrimitiveOutput(values=values)

    def _first_sighting(self, track_id: int) -> bool:
        """Whether this track's *first-ever* resolved decision for this attribute is
        happening right now.

        PERSISTENT: a track counted once must never be counted again, across window
        boundaries, regardless of a later ``attribute_vote`` switch -- the same
        first-ever-sighting philosophy ``unique_count``'s ``_SEEN_KEY`` uses, and for the
        same reason (retroactively moving an already-reported window's count would break
        ``agg_type: sum``'s invariant that per-window figures stay summable).
        """
        key = f"counted.{track_id}"
        if self._state.get(key):
            return False
        self._state.set(key, True, lifetime=Lifetime.PERSISTENT)
        return True

    def _prune(self, ctx: FrameContext, current_ids: set[int]) -> None:
        """Drop ``.new`` dedup state for tracks the tracker itself has retired.

        Mirrors ``attribute_vote._prune``/``attribute_band._prune`` exactly: "active" is
        read from the upstream ``track`` stage's published state, never from this frame's
        own subject-filtered subset, or a track that goes unresolved for one frame would
        be wrongly pruned and could fire a second ``.new`` event on its return.
        """
        active: set[int] | None = None
        for output in ctx.previous.values():
            if not output.tracks:
                continue
            if active is None:
                active = set()
            active.update(output.tracks)
        if active is None:
            return
        active.update(current_ids)
        for key in list(self._state.keys(lifetime=Lifetime.PERSISTENT)):
            if not key.startswith("counted."):
                continue
            try:
                track_id = int(key[len("counted.") :])
            except ValueError:
                continue
            if track_id not in active:
                self._state.delete(key)

    def _resolve(self, ctx: FrameContext, det: PipelineDetection) -> tuple[str | None, float]:
        """The value to count for one detection, and its confidence.

        A same-attribute ``attribute_vote`` stage earlier in this pipeline publishes its
        stabilised per-track decision on ``TrackState.attributes[attribute]`` --
        ``attribute_vote`` never mutates ``ctx.detections`` itself (documented there as
        "a primitive that could change the frame the next stage sees would be action at a
        distance"), so pipeline *order* alone does not make this primitive see that
        decision. ``ctx.previous`` is keyed by stage name and holds only earlier stages'
        outputs (``base.py`` ``FrameContext.previous``), which is what
        ``AppManifest._check_attribute_order`` is actually a precondition for: read it
        explicitly here, rather than assume ordering is self-enforcing.

        Once a track has a stabilised decision, it is counted unconditionally --
        ``attribute_vote``'s own ``min_votes``/``method`` already is the reliability gate
        for a stabilised value, and this primitive's ``min_confidence`` measures a single
        raw frame's confidence, the wrong dimension to re-gate a categorical vote outcome
        by. ``min_confidence`` still gates the raw fallback path exactly as before.

        Falls back to the raw intake-decoded attribute when: no track id, no upstream
        stage in this pipeline publishes a decision for this attribute at all, or this
        track has none yet this frame (undecided -- ``attribute_vote`` does not include an
        undecided track in ``PrimitiveOutput.tracks``, ``attribute_vote.py`` ``process()``).
        If more than one earlier stage publishes this attribute for the same track
        (two ``attribute_vote`` stages on one attribute -- unusual, not forbidden), the
        first one found, in pipeline order, wins.
        """
        if det.track_id is not None:
            track_id = int(det.track_id)
            for output in ctx.previous.values():
                state = output.tracks.get(track_id) if output.tracks else None
                if state is None:
                    continue
                decided = state.attributes.get(self._attribute)
                if decided is not None:
                    confidence = state.attributes.get(f"{self._attribute}_confidence")
                    return (
                        str(decided),
                        float(confidence) if isinstance(confidence, int | float) else 1.0,
                    )

        ref = det.attributes.get(self._attribute)
        if ref is None or ref.confidence < self._min_confidence:
            return None, 0.0
        return ref.label, ref.confidence

    def _accumulate(
        self,
        per_value: Mapping[str, int],
        new_per_value: Mapping[str, int],
        labelled: int,
        unknown: int,
        other: int,
        other_new: int,
        instances: int,
        best_confidence: float,
    ) -> None:
        """Fold this frame into the window, in the state store.

        ``Lifetime.WINDOW`` throughout: every one of these is a measurement *of* the window,
        and carrying a peak across the boundary reports the last interval's busiest moment as
        this one's (``09`` §4 rule 2). ``new.<value>``/``new.other`` are incremented, not set
        -- disjoint per-frame counts folding into a running window total, the same shape
        ``unique_count``'s ``_NEW_KEY`` uses (as opposed to ``last.<value>``'s overwrite,
        which is a level reading, not an event tally).
        """
        for value, count in per_value.items():
            self._state.set(f"last.{value}", count, lifetime=Lifetime.WINDOW)
            self._state.set(
                f"peak.{value}",
                max(int(self._state.get(f"peak.{value}") or 0), count),
                lifetime=Lifetime.WINDOW,
            )
        for value, count in new_per_value.items():
            if count:
                self._state.incr(f"new.{value}", count, lifetime=Lifetime.WINDOW)
            elif self._state.get(f"new.{value}") is None:
                self._state.set(f"new.{value}", 0.0, lifetime=Lifetime.WINDOW)
        if other_new:
            self._state.incr("new.other", other_new, lifetime=Lifetime.WINDOW)
        elif self._state.get("new.other") is None:
            self._state.set("new.other", 0.0, lifetime=Lifetime.WINDOW)
        self._state.set("last.labelled", labelled, lifetime=Lifetime.WINDOW)
        self._state.set(
            "peak.labelled",
            max(int(self._state.get("peak.labelled") or 0), labelled),
            lifetime=Lifetime.WINDOW,
        )
        self._state.set("last.unknown", unknown, lifetime=Lifetime.WINDOW)
        self._state.set("last.other", other, lifetime=Lifetime.WINDOW)
        self._state.set("last.instances", instances, lifetime=Lifetime.WINDOW)
        self._state.set(
            "peak.confidence",
            max(float(self._state.get("peak.confidence") or 0.0), best_confidence),
            lifetime=Lifetime.WINDOW,
        )
        self._state.incr("frames", 1, lifetime=Lifetime.WINDOW)

    def window(self, frames: Sequence[PrimitiveOutput]) -> WindowOutput:
        """Collapse the window. Every count is a level, so each gets **two** names (**PY-1**).

        Args:
            frames: Unused -- the accumulators hold the same data already folded, and they
                survive a window whose retained frames were capped by
                ``runtime/window.py``'s ``max_frames`` truncation, which would silently
                lower a peak recomputed from this list.
        """
        del frames
        if not float(self._state.get("frames") or 0.0):
            return WindowOutput()
        values: dict[str, Scalar] = {}
        for value in self._values:
            values[f"{value}.count"] = int(self._state.get(f"last.{value}") or 0)
            values[f"{value}.count_peak"] = int(self._state.get(f"peak.{value}") or 0)
            values[f"{value}.new"] = int(self._state.get(f"new.{value}") or 0)
        values.update(
            labelled_count=int(self._state.get("last.labelled") or 0),
            labelled_count_peak=int(self._state.get("peak.labelled") or 0),
            unknown_count=int(self._state.get("last.unknown") or 0),
            other_count=int(self._state.get("last.other") or 0),
            other_new=int(self._state.get("new.other") or 0),
            instance_count=int(self._state.get("last.instances") or 0),
            max_confidence=float(self._state.get("peak.confidence") or 0.0),
        )
        return WindowOutput(values=values)

    def reset(self) -> None:
        """``end_window()``, not ``clear()`` -- this stage keeps no cumulative total, and
        reaching for the full reset is the habit that erases one somewhere else
        (``09`` §4 rule 2, **FROZEN-4**)."""
        self._state.end_window()
