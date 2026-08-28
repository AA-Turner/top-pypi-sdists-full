"""``unique_count`` -- "how many distinct ones have I seen", deduplicated by track id.

Normative sources: ``_contracts/08-tobe-primitive-catalogue.md`` §1 (the primitive),
``_contracts/09-tobe-engine-architecture.md`` §4 (state and the two clears),
``_contracts/12-defect-register.md`` **FROZEN-4** (what ``total`` means).

**This is the most-duplicated block in the repository.**  Roughly 120 lines of
"track-id set, per-category set, new-this-frame set, promote, snapshot" are copy-pasted
across ~75 use cases -- ``usecases/people_counting.py:1142-1229`` is the reference copy,
and every copy re-decides the same three questions slightly differently.  Implemented once
here (objective **O2**), the answers are:

**The two lifetimes are the whole primitive.**  ``09`` §4 rule 2 exists because getting
this backwards is the single most common bug in custom code:

``new``
    :attr:`~matrice_analytics.engine.state.store.Lifetime.WINDOW`.  How many ids were seen
    for the first time *ever* during this aggregation window.
    :meth:`~matrice_analytics.engine.state.store.StateStore.end_window` clears it, so the
    next window starts at zero.  Carrying it over double-counts.

``total``
    :attr:`~matrice_analytics.engine.state.store.Lifetime.PERSISTENT`.  Distinct ids since
    the process last restarted -- **not** since the beginning of time, and deliberately so
    (**FROZEN-4**).  The backend's ClickHouse rollup formula is written against exactly
    that meaning; making it absolute here would silently change every historical series.
    A window boundary must never touch it.

The invariant that ties them together is ``total_after = total_before + new``, which is why
``new`` counts *first-ever* sightings rather than "ids seen this window that were not seen
last window".  The two readings differ for an object that leaves and comes back, and only
the first one sums.

**This stage is what puts an app on a volume dashboard (BE-16).**  ``results-agg``'s
``current_counts`` is the window's *arrival delta* -- it lands in ``raw_analytics.count``,
which the backend's five-minute rollup sums -- and an arrival is a first sighting of a
*distinct* object, which nothing but this primitive can decide.
:class:`~matrice_analytics.engine.runtime.window.ZoneCounters` reads it from the
``per_category.<entity>`` values below, differencing them across the window boundary.  An
app with no ``unique_count`` stage publishes zero arrivals and is flat on every volume
chart; :meth:`AggregationWindow.build
<matrice_analytics.engine.runtime.window.AggregationWindow.build>` warns about exactly that
once.  The alternative -- substituting the per-frame level -- is the defect **BE-16**
records, and it inflates the published footfall by roughly the number of windows in the
bucket.

**No wall clock** (**PY-13**).  Nothing here reads a clock at all: the window boundary
arrives as a :meth:`UniqueCount.reset` call, not as an elapsed-seconds test.

**No private state** (``09`` §4 rule 1, **D6**).  The seen-id sets live in the
:class:`~matrice_analytics.engine.state.store.StateStore` as plain nested dicts, not in the
``self._per_category_total_track_ids`` the legacy copies use.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any, ClassVar

from matrice_analytics.engine.manifest.models import UniqueCountConfig
from matrice_analytics.engine.primitives.base import (
    FrameContext,
    PrimitiveOutput,
    Scalar,
    TrackState,
    WindowOutput,
    register,
)
from matrice_analytics.engine.state import Lifetime, StateStore

__all__ = ["UniqueCount"]


#: PERSISTENT (**FROZEN-4**): ``{entity: {track_id_as_str: 1}}``.  A dict rather than a set
#: because ``09`` §4 wants stored values plain enough for a durable backing to serialise,
#: and because membership has to be O(1) on the hot path.
_SEEN_KEY = "seen_ids"

#: WINDOW: ids first seen during the current aggregation window.
_NEW_KEY = "new_in_window"

#: PERSISTENT diagnostic: detections of a configured entity that carried no track id and so
#: could not be deduplicated.  Not published -- ``UniqueCountConfig.output_names()`` does
#: not declare it, and a stage must not invent wire-visible keys a manifest cannot resolve
#: (``09`` §3).  It is in the store so that "the unique count is too low" has an answer
#: other than "the tracker is fine, look again".
_UNTRACKED_KEY = "untracked_detections"


def _tracks_from_previous(
    previous: Mapping[str, PrimitiveOutput],
    entities: frozenset[str],
    zone: str,
) -> dict[str, set[int]] | None:
    """Collect this frame's track ids from the upstream stages' :class:`TrackState`s.

    :attr:`PrimitiveOutput.tracks` is the documented channel for "a later stage reads
    tracking without re-implementing it" (``base.TrackState``), and it is strictly better
    evidence than a detection's ``track_id``: a :class:`TrackState` states its own entity
    and zone, so nothing has to be inferred.

    Args:
        previous: :attr:`FrameContext.previous` -- earlier stages keyed by *stage* name.  A
            manifest may run ``track`` under a custom ``name:``, so every stage is scanned
            rather than the literal key ``"track"`` looked up.
        entities: The configured categories.
        zone: This frame's zone, to drop any track a stage published for another one.

    Returns:
        ``{entity: {track_id}}``, or ``None`` when no upstream stage published tracks at
        all -- which is the signal to fall back to the detections.  ``None`` and "an empty
        frame" are different answers and must not collapse into one.
    """
    found: dict[str, set[int]] = {}
    any_tracker = False
    for output in previous.values():
        if not output.tracks:
            continue
        any_tracker = True
        state: TrackState
        for state in output.tracks.values():
            if state.entity not in entities or state.zone != zone:
                continue
            found.setdefault(state.entity, set()).add(int(state.track_id))
    return found if any_tracker else None


@register(name="unique_count")
class UniqueCount:
    """Distinct-object counting for one zone, deduplicated by tracker id.

    Publishes, into :attr:`PrimitiveOutput.values`:

    ``new``
        Ids seen for the first time *on this frame*.  A per-frame sample, so
        ``metrics[].agg_type: sum`` over a window reproduces the window figure exactly --
        the per-frame values are disjoint by construction.

    ``new_in_window``
        The running count of first-ever-seen ids **so far this window** -- the same
        WINDOW-lifetime counter :meth:`window` reads at the boundary, read one frame
        earlier.  A metric wanting a live arrivals-so-far total sources this with
        ``agg_type: last``, rather than summing ``new`` per frame and getting the right
        answer only once the window has actually closed.

    ``total``
        Distinct ids since process start (**FROZEN-4**).  A level, not an event: aggregate
        it with ``max`` or ``last``, never ``sum``.

    ``per_category.<entity>``
        The same cumulative total, split by entity, one key per
        :attr:`UniqueCountConfig.categories` entry.  These sum to ``total``, because the
        dedup key is ``(entity, track_id)`` and not the bare id -- a tracker is free to
        reuse an id across classes, and a per-category breakdown that does not add up is
        worse than none.

        These are also the **only** input to ``results-agg``'s ``current_counts``,
        ``current_new_counts`` and ``total_counts``
        (:class:`~matrice_analytics.engine.runtime.window.ZoneCounters` differences them
        across the window boundary to get arrivals), so an entity missing from
        :attr:`UniqueCountConfig.categories` is an entity with no volume series -- even if
        ``detect`` counts it every frame.

    Requires a ``track`` stage earlier in the pipeline
    (:attr:`UniqueCountConfig.REQUIRES`); it reads that stage's
    :attr:`PrimitiveOutput.tracks`.

    Example:
        >>> from matrice_analytics.engine.state import InMemoryStateStore
        >>> state = InMemoryStateStore().for_primitive("cam-1", "footfall", "global", "unique_count")
        >>> stage = UniqueCount(UniqueCountConfig(categories=["person"]), state)
        >>> stage.process(ctx).values["total"]              # doctest: +SKIP
        1
    """

    name: ClassVar[str] = "unique_count"
    Config: ClassVar[type[UniqueCountConfig]] = UniqueCountConfig

    __slots__ = ("_categories", "_config", "_entities", "_state")

    def __init__(self, config: UniqueCountConfig, state: StateStore) -> None:
        """Bind a validated config and an already-scoped state store.

        Args:
            config: The stage's validated :class:`UniqueCountConfig`.
            state: A store scoped to ``<camera_id>/<app_id>/<zone>/<primitive>``
                (``09`` §4).  The seen-id sets live here and nowhere else (**D6**); a
                ``self._seen`` set would be invisible to the state layer, to
                :meth:`StateStore.end_window` and to any future durable backing.

        Note:
            ``config.by`` is ``Literal["track_id"]`` -- one strategy, checked at manifest
            load.  It is read rather than ignored so that adding a second strategy later is
            a change here and not a silent no-op.
        """
        if config.by != "track_id":
            raise ValueError(
                f"unique_count.by={config.by!r} is not implemented. UniqueCountConfig "
                "accepts only 'track_id'; a strategy the manifest allows but the runtime "
                "silently ignores would publish a plausible-looking wrong number."
            )
        self._config = config
        self._state = state
        self._categories: tuple[str, ...] = tuple(config.categories)
        self._entities: frozenset[str] = frozenset(config.categories)

    # -- per frame ----------------------------------------------------------

    def process(self, ctx: FrameContext) -> PrimitiveOutput:
        """Fold this frame's track ids into the cumulative sets.

        Args:
            ctx: One frame in one zone.  Track ids come from an upstream ``track`` stage's
                :attr:`PrimitiveOutput.tracks` when there is one, and from
                ``detection.track_id`` otherwise -- never both, because a tracker that
                renumbered the ids would otherwise have every object counted twice.

        Returns:
            ``new`` for this frame, plus the cumulative ``total`` and per-category
            breakdown.
        """
        current = self._current_ids(ctx)
        seen: dict[str, dict[str, int]] = {
            entity: dict(ids) for entity, ids in (self._state.get(_SEEN_KEY, {}) or {}).items()
        }

        new_this_frame = 0
        for entity, ids in current.items():
            bucket = seen.setdefault(entity, {})
            for track_id in sorted(ids):  # sorted: deterministic, which O5 asserts on
                key = str(track_id)
                if key not in bucket:
                    bucket[key] = 1
                    new_this_frame += 1

        # PERSISTENT: a cumulative total survives the window boundary (FROZEN-4). Writing
        # this with Lifetime.WINDOW is the bug 09 §4 rule 2 is written to prevent.
        self._state.set(_SEEN_KEY, seen, lifetime=Lifetime.PERSISTENT)
        # WINDOW: a measurement *of* this window, cleared by end_window().
        if new_this_frame:
            self._state.incr(_NEW_KEY, new_this_frame, lifetime=Lifetime.WINDOW)
        elif self._state.get(_NEW_KEY) is None:
            self._state.set(_NEW_KEY, 0.0, lifetime=Lifetime.WINDOW)

        values: dict[str, Scalar] = {
            "new": new_this_frame,
            # Live, so-far-this-window running total -- the same `_NEW_KEY` counter
            # `.window()` reads at the boundary, read one frame earlier. `new` stays exactly
            # "first seen this frame" (agg_type: sum over it at window close depends on that,
            # per this stage's own contract above); a metric wanting the running arrivals
            # total mid-window sources this key instead, with agg_type: last.
            "new_in_window": int(self._state.get(_NEW_KEY, 0) or 0),
            "total": self._total(seen),
        }
        for entity in self._categories:
            values[f"per_category.{entity}"] = len(seen.get(entity, {}))
        return PrimitiveOutput(values=values)

    def _current_ids(self, ctx: FrameContext) -> dict[str, set[int]]:
        """This frame's ``{entity: {track_id}}``, from the best available source."""
        from_tracker = _tracks_from_previous(ctx.previous, self._entities, ctx.zone)
        if from_tracker is not None:
            return from_tracker

        found: dict[str, set[int]] = {}
        untracked = 0
        for detection in ctx.of_entity(*self._categories):
            if detection.track_id is None:
                untracked += 1
                continue
            found.setdefault(detection.entity, set()).add(int(detection.track_id))
        if untracked:
            # Loud in the state, not silent: an unmeasured drop is how "the count is too
            # low" becomes unanswerable (PY-10's argument, applied to tracking).
            self._state.incr(_UNTRACKED_KEY, untracked, lifetime=Lifetime.PERSISTENT)
        return found

    @staticmethod
    def _total(seen: Mapping[str, Mapping[str, Any]]) -> int:
        """Distinct ``(entity, track_id)`` pairs across every bucket."""
        return sum(len(bucket) for bucket in seen.values())

    # -- per window ---------------------------------------------------------

    def window(self, frames: Sequence[PrimitiveOutput]) -> WindowOutput:
        """Publish the window's ``new`` and the running ``total``.

        ``new`` is read from the WINDOW-lifetime counter rather than summed from ``frames``.
        The two are equal -- each frame's ``new`` counts ids nothing had seen before, so the
        per-frame values are disjoint -- but the counter is the one that is still correct
        when the runtime does not retain 1,500 per-frame outputs, and it is the value
        :meth:`reset` is about to clear.

        Args:
            frames: This stage's per-frame outputs, in frame order.  Accepted for the
                protocol; the store is authoritative.

        Returns:
            ``new`` for the closing window and the cumulative ``total`` (**FROZEN-4**).
        """
        _ = frames
        seen: Mapping[str, Mapping[str, Any]] = self._state.get(_SEEN_KEY, {}) or {}
        values: dict[str, Scalar] = {
            "new": int(self._state.get(_NEW_KEY, 0) or 0),
            # Same counter as "new" here (the window has closed, so "so far" and "final" are
            # the same reading) -- published under its own name so a metric sourced from
            # `unique_count.new_in_window` resolves from this WindowOutput directly rather
            # than falling back to collapsing retained per-frame samples, which is subject to
            # the retention cap `observe()` warns about on a long or high-fps window.
            "new_in_window": int(self._state.get(_NEW_KEY, 0) or 0),
            "total": self._total(seen),
        }
        for entity in self._categories:
            values[f"per_category.{entity}"] = len(seen.get(entity, {}))
        return WindowOutput(values=values)

    def reset(self) -> None:
        """Clear ``new`` at the aggregation boundary; keep ``total`` (**FROZEN-4**).

        One call does both, because the lifetime was declared at write time:
        :meth:`StateStore.end_window` drops ``new_in_window`` and cannot touch the seen-id
        sets.  That is the point of the enum -- ``09`` §4 rule 2 notes that today the
        distinction is implicit in *which method clears which field*
        (``base_processor.py:126-131,182``), and that getting it backwards is the most
        common bug in custom code.  Here getting it backwards is not expressible.

        Clearing the totals here would reset the cumulative series to zero every 60
        seconds, and the backend's rollup would read each reset as a genuine restart.
        """
        self._state.end_window()
