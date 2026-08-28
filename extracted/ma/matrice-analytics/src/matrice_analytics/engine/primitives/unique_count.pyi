"""Auto-generated stub for module: unique_count."""
from typing import Any

# Classes
class UniqueCount:
    # Distinct-object counting for one zone, deduplicated by tracker id.
    #
    #     Publishes, into :attr:`PrimitiveOutput.values`:
    #
    #     ``new``
    #         Ids seen for the first time *on this frame*.  A per-frame sample, so
    #         ``metrics[].agg_type: sum`` over a window reproduces the window figure exactly --
    #         the per-frame values are disjoint by construction.
    #
    #     ``new_in_window``
    #         The running count of first-ever-seen ids **so far this window** -- the same
    #         WINDOW-lifetime counter :meth:`window` reads at the boundary, read one frame
    #         earlier.  A metric wanting a live arrivals-so-far total sources this with
    #         ``agg_type: last``, rather than summing ``new`` per frame and getting the right
    #         answer only once the window has actually closed.
    #
    #     ``total``
    #         Distinct ids since process start (**FROZEN-4**).  A level, not an event: aggregate
    #         it with ``max`` or ``last``, never ``sum``.
    #
    #     ``per_category.<entity>``
    #         The same cumulative total, split by entity, one key per
    #         :attr:`UniqueCountConfig.categories` entry.  These sum to ``total``, because the
    #         dedup key is ``(entity, track_id)`` and not the bare id -- a tracker is free to
    #         reuse an id across classes, and a per-category breakdown that does not add up is
    #         worse than none.
    #
    #         These are also the **only** input to ``results-agg``'s ``current_counts``,
    #         ``current_new_counts`` and ``total_counts``
    #         (:class:`~matrice_analytics.engine.runtime.window.ZoneCounters` differences them
    #         across the window boundary to get arrivals), so an entity missing from
    #         :attr:`UniqueCountConfig.categories` is an entity with no volume series -- even if
    #         ``detect`` counts it every frame.
    #
    #     Requires a ``track`` stage earlier in the pipeline
    #     (:attr:`UniqueCountConfig.REQUIRES`); it reads that stage's
    #     :attr:`PrimitiveOutput.tracks`.
    #
    #     Example:
    #         >>> from matrice_analytics.engine.state import InMemoryStateStore
    #         >>> state = InMemoryStateStore().for_primitive("cam-1", "footfall", "global", "unique_count")
    #         >>> stage = UniqueCount(UniqueCountConfig(categories=["person"]), state)
    #         >>> stage.process(ctx).values["total"]              # doctest: +SKIP
    #         1

    def __init__(self: Any, config: Any, state: Any) -> None:
        """
        Bind a validated config and an already-scoped state store.
        
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
        ...

    def process(self: Any, ctx: Any) -> Any:
        """
        Fold this frame's track ids into the cumulative sets.
        
                Args:
                    ctx: One frame in one zone.  Track ids come from an upstream ``track`` stage's
                        :attr:`PrimitiveOutput.tracks` when there is one, and from
                        ``detection.track_id`` otherwise -- never both, because a tracker that
                        renumbered the ids would otherwise have every object counted twice.
        
                Returns:
                    ``new`` for this frame, plus the cumulative ``total`` and per-category
                    breakdown.
        """
        ...

    def reset(self: Any) -> None:
        """
        Clear ``new`` at the aggregation boundary; keep ``total`` (**FROZEN-4**).
        
                One call does both, because the lifetime was declared at write time:
                :meth:`StateStore.end_window` drops ``new_in_window`` and cannot touch the seen-id
                sets.  That is the point of the enum -- ``09`` §4 rule 2 notes that today the
                distinction is implicit in *which method clears which field*
                (``base_processor.py:126-131,182``), and that getting it backwards is the most
                common bug in custom code.  Here getting it backwards is not expressible.
        
                Clearing the totals here would reset the cumulative series to zero every 60
                seconds, and the backend's rollup would read each reset as a genuine restart.
        """
        ...

    def window(self: Any, frames: Any[Any]) -> Any:
        """
        Publish the window's ``new`` and the running ``total``.
        
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
        ...

