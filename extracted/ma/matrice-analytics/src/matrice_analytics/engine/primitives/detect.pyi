"""Auto-generated stub for module: detect."""
from typing import Any

# Classes
class Detect:
    # Thresholded class presence and counts for one zone, one frame.
    #
    #     Publishes, into :attr:`PrimitiveOutput.values`:
    #
    #     ``<entity>.count``
    #         Admitted detections of that entity this frame, one key per
    #         :attr:`DetectConfig.classes` entry.  Always present, ``0`` when the entity is
    #         absent -- an omitted key would make ``metrics[].source`` unresolvable and turn a
    #         quiet camera into a manifest load error (``09`` §3).
    #
    #     ``total``
    #         The sum of the per-entity counts.
    #
    #     ``max_confidence``
    #         The highest admitted confidence, ``0.0`` when nothing was admitted.
    #
    #     :meth:`window` publishes the same three names **plus** ``<entity>.count_peak`` and
    #     ``total_peak``.  The un-suffixed names carry the window's *last-frame* value and the
    #     suffixed ones its *peak*, because a window output is published as-is and therefore has to
    #     say which reading it is -- ``agg_type`` cannot choose between them.  See :meth:`window`.
    #
    #     Example:
    #         >>> from matrice_analytics.engine.state import InMemoryStateStore
    #         >>> config = DetectConfig(classes=["person"])
    #         >>> stage = Detect(config, InMemoryStateStore().for_primitive("c1", "a1", "global", "detect"))
    #         >>> out = stage.process(ctx)                       # doctest: +SKIP
    #         >>> out.values["person.count"]                     # doctest: +SKIP
    #         3

    def __init__(self: Any, config: Any, state: Any) -> None:
        """
        Bind a validated config and an already-scoped state store.
        
                Args:
                    config: The stage's validated :class:`DetectConfig`.
                    state: A store scoped to ``<camera_id>/<app_id>/<zone>/<primitive>``
                        (``09`` §4).  Every mutable value this primitive owns lives here; there is
                        deliberately no ``self._counts`` (**D6**).
        
                Note:
                    ``min_confidence`` defaults to ``0.0`` rather than to a guessed model
                    threshold.  ``DetectConfig.min_confidence`` documents itself as an *override*
                    of ``model.confidence_threshold``, and a primitive cannot see the model block
                    (``09`` §1) -- so with no override the pipeline's own thresholding stands and
                    this stage adds none of its own.  Inventing a default here would silently drop
                    detections the app asked to keep.
        """
        ...

    def process(self: Any, ctx: Any) -> Any:
        """
        Count this frame's admitted detections, per entity and in total.
        
                Args:
                    ctx: One frame in one zone.  Detections are already entity-remapped and
                        zone-assigned, so this reads :attr:`PipelineDetection.entity` and never the
                        model's ``category`` (``09`` §3).
        
                Returns:
                    The per-entity counts, the total and the peak confidence.
        """
        ...

    def reset(self: Any) -> None:
        """
        Clear the window peaks at the aggregation boundary -- and nothing else.
        
                ``09`` §4 rule 2 in one line: :meth:`StateStore.end_window` drops every
                :attr:`Lifetime.WINDOW` key and leaves the
                :attr:`Lifetime.PERSISTENT` smoothing windows alone.  Clearing those would make
                every object in frame re-ramp its confidence window once a minute, which reads
                downstream as a count that dips at :00 -- a wrong number that looks like flaky
                analytics rather than like a bug.
        """
        ...

    def window(self: Any, frames: Any[Any]) -> Any:
        """
        Publish **both** readings of the window, under two names each -- never a sum.
        
                A count is a level, not an event: summing 1,500 per-frame "3 people" samples
                publishes 4,500 people.  Conflating the two is exactly **PY-1**, which is why
                :class:`WindowOutput` is a separate type from :class:`PrimitiveOutput` in the first
                place.
        
                The peak is not the *only* honest collapse of a level, though, and pretending it was
                is a defect of its own.  A :class:`WindowOutput` is published verbatim -- the runtime
                does not re-apply ``metrics[].agg_type`` to a registered primitive, deliberately -- so
                while this method published one number per name, a manifest asking for
                ``current_occupancy`` (``agg_type: last``) and ``peak_occupancy`` (``agg_type: max``)
                off the same source got the *peak* twice and ``current_occupancy`` was simply wrong.
                The rule is: **a stage's window value is what it is; if you need two readings, publish
                two names.**  So:
        
                ``<entity>.count`` / ``total``
                    The value on the window's **last** frame -- "how many are in view now", which is
                    what ``agg_type: last`` means.
                ``<entity>.count_peak`` / ``total_peak``
                    The window's **high-water mark** -- "how many at the busiest moment", which is what
                    ``agg_type: max`` means.
                ``max_confidence``
                    The window maximum.  One name, one reading: it is already declared as a maximum, and
                    the confidence on an arbitrary last frame answers no question.
        
                Args:
                    frames: This stage's per-frame outputs for the window, in frame order.  Folded into
                        the *peaks* so those are right whether or not the runtime retained them; the
                        last readings come from the store only, because retention is capped and
                        ``frames[-1]`` is therefore not reliably the window's last frame.
        
                Returns:
                    The last and peak per-entity counts, the last and peak totals, and the peak
                    confidence.
        """
        ...

