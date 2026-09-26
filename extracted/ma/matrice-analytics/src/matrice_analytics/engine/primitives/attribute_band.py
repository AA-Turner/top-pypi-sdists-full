"""``attribute_band`` -- a numeric per-detection attribute, averaged per track and banded.

Normative source: ``classification-primitives.md`` §5.4. Replaces
``age_detection.AgeSmoother`` (a 20-frame running mean per track,
``usecases/age_detection.py:176-193``) plus ``_get_age_category`` (the Child/Adult/Senior
cut points -- ``age <= 19``, ``age <= 60``, else Senior, ``:242-249``), which are two halves
of one operation split across two places in legacy, with the cut points hard-coded in a
method body where no manifest can reach them.

Legacy's smoothing rule, reproduced exactly (``:308-323``): a detection **with** a track id
runs through the per-track running mean; one **without** a track id is banded on its own raw
value, unsmoothed -- there is no history to average over. Legacy's ``final_age = 0`` /
"leave the detection unclassified" fallback for a missing observation is replaced by the
same honest absence-counting ``attribute_count`` already established: a subject with no
usable measurement is ``unknown_count``, never a fabricated ``0`` sitting in a real band.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import ClassVar

from matrice_analytics.engine.manifest.models import AttributeBandConfig
from matrice_analytics.engine.primitives.base import (
    FrameContext,
    PrimitiveOutput,
    Scalar,
    WindowOutput,
    register,
)
from matrice_analytics.engine.state import Lifetime, StateStore

__all__ = ["AttributeBand"]


def _as_number(text: str) -> float | None:
    """A decoded attribute's label as a float, or ``None`` if it is not one.

    :class:`~matrice_analytics.engine.intake.attributes.AttributeSpec.numeric` already keeps
    a numeric attribute's label as a number's string form at intake; this is a second,
    defensive check rather than a trust that the producer honoured that contract.
    """
    try:
        return float(text)
    except ValueError:
        return None


@register(name="attribute_band")
class AttributeBand:
    """Per-track running mean of a numeric attribute, banded into named buckets.

    Outputs, each resolvable as ``<stage>.<name>``:

    ``<band>.count``
        Subjects this frame whose (smoothed, where a track id exists) value falls in
        ``<band>``.
    ``measured_count``
        Subjects successfully banded. Sum of the per-band counts.
    ``unknown_count``
        Subjects carrying no usable numeric value for ``attribute`` this frame.
    ``instance_count``
        All subjects in this zone this frame, banded or not. The denominator.
    ``mean_value``
        This frame's average of the (smoothed) measured values; a health diagnostic, not a
        metric.

    Per-track running-mean history is ``Lifetime.PERSISTENT`` -- a track's smoothed value
    must not re-ramp from empty at every window boundary -- and is pruned the same way
    ``attribute_vote`` prunes its per-track vote history: against the upstream ``track``
    stage's currently-active track ids, never against this stage's own per-frame subset.
    """

    name: ClassVar[str] = "attribute_band"
    Config: ClassVar[type[AttributeBandConfig]] = AttributeBandConfig

    __slots__ = ("_attribute", "_bands", "_config", "_smooth_frames", "_state", "_subject")

    def __init__(self, config: AttributeBandConfig, state: StateStore) -> None:
        self._config = config
        self._state = state
        self._attribute = config.attribute
        self._subject: tuple[str, ...] = tuple(config.subject)
        self._bands = tuple(config.bands)
        self._smooth_frames = int(config.smooth_frames)

    def process(self, ctx: FrameContext) -> PrimitiveOutput:
        """Band this zone's subjects by the (smoothed) value of one numeric attribute."""
        per_band = dict.fromkeys((band.name for band in self._bands), 0)
        unknown = 0
        total = 0.0
        measured = 0
        instances = 0
        active_ids: set[int] = set()

        for det in ctx.of_entity(*self._subject):
            instances += 1
            ref = det.attributes.get(self._attribute)
            raw = _as_number(ref.label) if ref is not None else None
            if raw is None:
                unknown += 1
                continue
            if det.track_id is not None:
                track_id = int(det.track_id)
                active_ids.add(track_id)
                value = self._smoothed(track_id, raw)
            else:
                value = raw
            per_band[self._band_for(value)] += 1
            measured += 1
            total += value

        self._prune(ctx, active_ids)
        mean_value = total / measured if measured else 0.0
        self._accumulate(per_band, measured, unknown, instances, mean_value)

        values: dict[str, Scalar] = {f"{name}.count": count for name, count in per_band.items()}
        values.update(
            measured_count=measured,
            unknown_count=unknown,
            instance_count=instances,
            mean_value=mean_value,
        )
        return PrimitiveOutput(values=values)

    def _smoothed(self, track_id: int, raw: float) -> float:
        """This track's running mean over its last ``smooth_frames`` observations
        (``AgeSmoother.update``, unbounded-within-window arithmetic mean, not an EMA)."""
        history: list[float] = list(self._state.get(f"values.{track_id}") or ())
        history.append(raw)
        trimmed = history[-self._smooth_frames :]
        self._state.set(f"values.{track_id}", trimmed, lifetime=Lifetime.PERSISTENT)
        return sum(trimmed) / len(trimmed)

    def _band_for(self, value: float) -> str:
        """The first band (ascending) whose ``upper`` is not exceeded, or the last band --
        config validation already guarantees the last band's ``upper`` is either the
        greatest bound or ``None`` ('and above'), so this always resolves."""
        for band in self._bands:
            if band.upper is None or value <= band.upper:
                return band.name
        return self._bands[-1].name

    def _prune(self, ctx: FrameContext, current_ids: set[int]) -> None:
        """Drop running-mean history for tracks the tracker itself has retired.

        Mirrors ``attribute_vote._prune`` exactly: "active" is read from the upstream
        ``track`` stage's published state, never from this frame's own subject-filtered
        subset, or a track that goes unmeasured for one frame would be wrongly pruned.
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
            if not key.startswith("values."):
                continue
            try:
                track_id = int(key[len("values.") :])
            except ValueError:
                continue
            if track_id not in active:
                self._state.delete(key)

    def _accumulate(
        self,
        per_band: Mapping[str, int],
        measured: int,
        unknown: int,
        instances: int,
        mean_value: float,
    ) -> None:
        """Fold this frame into the window, in the state store. ``Lifetime.WINDOW``
        throughout -- every one of these is a measurement *of* the window."""
        for name, count in per_band.items():
            self._state.set(f"last.{name}", count, lifetime=Lifetime.WINDOW)
        self._state.set("last.measured", measured, lifetime=Lifetime.WINDOW)
        self._state.set("last.unknown", unknown, lifetime=Lifetime.WINDOW)
        self._state.set("last.instances", instances, lifetime=Lifetime.WINDOW)
        self._state.set("last.mean", mean_value, lifetime=Lifetime.WINDOW)
        self._state.incr("frames", 1, lifetime=Lifetime.WINDOW)

    def window(self, frames: Sequence[PrimitiveOutput]) -> WindowOutput:
        """Republish the last frame's readings -- no separate peak variant (unlike
        ``attribute_count``): a band count is not tracked as a high-water mark here.

        Args:
            frames: Unused -- the state store is authoritative, for the same reason
                ``attribute_count.window`` ignores it.
        """
        del frames
        if not float(self._state.get("frames") or 0.0):
            return WindowOutput()
        values: dict[str, Scalar] = {
            f"{band.name}.count": int(self._state.get(f"last.{band.name}") or 0)
            for band in self._bands
        }
        values.update(
            measured_count=int(self._state.get("last.measured") or 0),
            unknown_count=int(self._state.get("last.unknown") or 0),
            instance_count=int(self._state.get("last.instances") or 0),
            mean_value=float(self._state.get("last.mean") or 0.0),
        )
        return WindowOutput(values=values)

    def reset(self) -> None:
        """``end_window()``, not ``clear()`` -- per-track running-mean history is
        PERSISTENT and must survive the window boundary, or a track's smoothed value
        re-ramps from empty once per interval."""
        self._state.end_window()
