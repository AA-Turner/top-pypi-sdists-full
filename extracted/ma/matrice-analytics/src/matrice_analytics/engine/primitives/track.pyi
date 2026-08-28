"""Auto-generated stub for module: track."""
from typing import Any

# Constants
Box: Any

# Functions
def assign(cost: list[list[float]], threshold: float) -> tuple[list[tuple[int, int]], list[int], list[int]]:
    """
    Optimal assignment, then drop every pair costing more than ``threshold``.
    
        The order matters and is the legacy behaviour
        (``advanced_tracker/matching.linear_assignment``): solving first and gating second
        keeps the assignment globally optimal, where gating first would let a cheap-but-wrong
        pair win because the right one was pruned.
    
        Args:
            cost: An ``n x m`` cost matrix.
            threshold: The maximum acceptable cost.  **This is a cost, not an IoU** --
                ``TrackConfig.match_thresh`` of ``0.8`` accepts an IoU as low as ``0.2``.  The
                legacy field name reads like a similarity and is not one; the semantics are
                preserved here rather than quietly inverted, because inverting them would
                change the behaviour of every migrated app.
    
        Returns:
            ``(pairs, unmatched_rows, unmatched_columns)``.
    """
    ...
def hungarian(cost: list[list[float]]) -> list[tuple[int, int]]:
    """
    Optimal one-to-one assignment minimising total cost (Jonker-Volgenant).
    
        The shortest-augmenting-path form of the Hungarian algorithm, ``O(n^2 m)``.  It is here
        rather than ``scipy.optimize.linear_sum_assignment`` because a primitive may not import
        scipy (**PY-20**); it returns the same optimum, and at the frame sizes this runs at
        (tens of boxes) the pure-Python cost is irrelevant next to being able to import the
        engine at all.
    
        Greedy nearest-neighbour matching was the alternative and is rejected on purpose: it
        swaps the ids of two objects that cross, and an id swap is invisible in the counts
        while corrupting every downstream dwell and unique count.
    
        Args:
            cost: An ``n x m`` cost matrix.  Rows and columns may differ in length.
    
        Returns:
            ``(row, column)`` pairs, at most ``min(n, m)`` of them, sorted by row.  Every cost
            is assigned -- the caller drops the pairs it considers too expensive.
    """
    ...
def iou(a: Any, b: Any) -> float:
    """
    Intersection over union of two boxes.
    
        Args:
            a: First box, ``(xmin, ymin, xmax, ymax)``.
            b: Second box.
    
        Returns:
            ``0.0`` for disjoint or degenerate boxes, up to ``1.0`` for identical ones.
    """
    ...
def observations_from(detections: Any[Any]) -> list[Any]:
    """
    Build tracker observations from detections -- exposed for tests.
    
        Lets a test drive :class:`_Tracker` directly with the same conversion
        :meth:`Track.process` uses, rather than re-deriving it and drifting.
    """
    ...

# Classes
class Track:
    # ID association for one zone, with the method chosen by the manifest.
    #
    #     Publishes ``active_tracks`` into :attr:`PrimitiveOutput.values` and one
    #     :class:`TrackState` per emitted track into :attr:`PrimitiveOutput.tracks`.  The
    #     ``tracks`` mapping is the contract with downstream stages: ``unique_count``, ``dwell``
    #     and ``velocity_state`` read it rather than re-implementing tracking, which is the
    #     duplication this primitive exists to end.
    #
    #     Each :class:`TrackState` carries ``score`` and ``det_index`` in
    #     :attr:`TrackState.attributes`.  ``det_index`` indexes
    #     :attr:`FrameContext.detections`, so a later stage can reach the detection's box without
    #     this primitive mutating the frame's detection tuple -- primitives do not write to what
    #     the next stage is about to read (``base.FrameContext``).
    #
    #     Example:
    #         >>> from matrice_analytics.engine.state import InMemoryStateStore
    #         >>> state = InMemoryStateStore().for_primitive("cam-1", "footfall", "global", "track")
    #         >>> stage = Track(TrackConfig(method="bytetrack"), state)
    #         >>> out = stage.process(ctx)                       # doctest: +SKIP
    #         >>> sorted(out.tracks)                             # doctest: +SKIP
    #         [1, 2]

    def __init__(self: Any, config: Any, state: Any) -> None:
        """
        Bind a validated config and an already-scoped state store.
        
                Args:
                    config: The stage's validated :class:`TrackConfig`.  Unlike
                        ``engine_session.py:483``, every knob here came from a manifest.
                    state: A store scoped to ``<camera_id>/<app_id>/<zone>/<primitive>``.
        
                Note:
                    The track-id namespace is
                    :func:`~matrice_analytics.engine.state.store.stable_namespace` over
                    :attr:`~matrice_analytics.engine.state.store.StateStore.prefix` -- the store's own
                    scope, and **never** ``hash()`` (**PY-9**).  The prefix already encodes camera,
                    app, zone and stage, so two cameras cannot collide and the same camera gets the
                    same namespace in every process, forever.  It is read off the protocol rather
                    than through a ``getattr``: scope identity is part of the ``StateStore``
                    contract, so a store that cannot answer is a broken store, not a fallback case.
                    An unscoped root store answers ``""``, which is no identity at all; the stage
                    name stands in there, and is stable for the same reason.
        """
        ...

    def process(self: Any, ctx: Any) -> Any:
        """
        Associate this frame's detections with the running tracks.
        
                Args:
                    ctx: One frame in one zone.  Boxes are read in the contract's normalized 0-1
                        space and never converted to pixels, so this stage needs no resolution and
                        cannot make the 1920x mistake (**PY-7**).
        
                Returns:
                    ``active_tracks`` and the per-track :class:`TrackState` mapping.
        """
        ...

    def reset(self: Any) -> None:
        """
        Clear the window peak -- and emphatically **not** the tracker.
        
                ``09`` §4 rule 2.  :meth:`StateStore.end_window` drops the
                :attr:`Lifetime.WINDOW` peak and leaves the
                :attr:`Lifetime.PERSISTENT` tracker blob untouched.  Clearing the tracker here
                would hand every object in frame a brand-new id once a minute; ``unique_count``
                would then count the same person 60 times an hour and the footfall graph would show
                a spike on every window boundary.  That is the single most expensive way to get
                ``reset()`` wrong, and it is why the lifetime is declared at write time rather than
                inferred from which method is clearing what.
        """
        ...

    def window(self: Any, frames: Any[Any]) -> Any:
        """
        Report the window's simultaneous track count, **both** readings, under two names.
        
                A sum would publish "1,500 tracks" for one person standing still for a minute
                (**PY-1**); the *distinct* count over the window is ``unique_count``'s job, not this
                one's.  What is left is a level, and a level has two honest window readings:
        
                ``active_tracks``
                    How many were being tracked on the window's **last** frame -- ``agg_type: last``.
                ``active_tracks_peak``
                    How many at once at the **busiest** moment -- ``agg_type: max``.
        
                Both are published because a :class:`WindowOutput` is published verbatim: the runtime
                does not re-apply ``agg_type`` to a registered primitive, so one name could only ever
                carry one of the two numbers, and a manifest asking for the other got this one silently.
        
                Args:
                    frames: This stage's per-frame outputs, in frame order.  Folded into the peak so it
                        is right either way; the last reading comes from the store, because the
                        runtime caps retention and ``frames[-1]`` is then not the window's last frame.
        """
        ...

