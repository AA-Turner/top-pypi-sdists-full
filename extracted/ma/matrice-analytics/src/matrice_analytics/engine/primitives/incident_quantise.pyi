"""Auto-generated stub for module: incident_quantise."""
from typing import Any

# Functions
def level_rank(level: str) -> int:
    """
    Severity as a comparable integer: ``none`` 0, ``info`` 1 ... ``critical`` 5.
    
        Ranked against the **wire vocabulary**
        (:data:`~matrice_analytics.engine.manifest.models.SEVERITY_LEVELS`), never against the
        position of a rung in ``levels:``.  A config may declare any subset of the ladder in
        either ``order``, so a list-position rank would make ``critical`` outrank ``high`` in
        one app and not in another -- the rank has to mean "how bad", not "how far down the
        YAML".
    
        Args:
            level: A severity name, or :data:`NO_LEVEL`.
    
        Returns:
            ``0`` for :data:`NO_LEVEL` or an unknown name, otherwise ``1``-based position in
            ``info, low, medium, high, critical``.
    """
    ...

# Classes
class IncidentQuantise:
    # ``incident_quantise`` -- magnitude in, severity out.
    #
    #     Outputs (:attr:`PrimitiveOutput.values`):
    #
    #     ``level``
    #         The severity name this frame's magnitude reaches, or :data:`NO_LEVEL`.
    #     ``level_rank``
    #         :func:`level_rank` of it -- ``0`` for none, ``5`` for critical.  Publish this, not
    #         ``level``, to a numeric metric: ``metrics[].data`` is a number and a numeric
    #         *string* is rejected outright (contract Section 1 rule 6).
    #     ``area``
    #         Summed bounding-box area of the quantised detections, as a **fraction of the
    #         frame** (boxes are normalized 0-1, contract Section 4) -- unless
    #         :attr:`~matrice_analytics.engine.manifest.models.IncidentQuantiseConfig.area_source` is
    #         set, in which case this is that stage's ``area_ratio`` (true mask coverage) instead.
    #     ``confidence``
    #         Highest detection confidence, ``0-1``.
    #
    #     Raises one :class:`~matrice_analytics.engine.primitives.base.PrimitiveEvent` per frame
    #     while the magnitude reaches a rung, and none at :data:`NO_LEVEL`.  An empty frame is
    #     never an incident: with no detections the strategies would all quantise to ``0``, and a
    #     ladder with a ``percentage: 0`` rung would then report that rung forever on a camera
    #     watching an empty room.
    #
    #     Note:
    #         The event's ``kind`` is this **stage's name**, not an ``incidents.types[].key``.
    #         :class:`~matrice_analytics.engine.manifest.models.IncidentQuantiseConfig` carries no
    #         incident key -- the manifest joins the two the other way round, with
    #         ``incidents.types[].severity_from: <stage name>`` (``models.py:1891-1903``) -- so
    #         the stage name is the only identifier this primitive has, and the runtime resolves
    #         the incident type from it.

    def __init__(self: Any, config: Any, state: Any) -> None:
        """
        Construct from a validated config and an already-scoped state store.
        
                Args:
                    config: The stage's config, validated by the manifest loader.
                    state: A store scoped to ``<camera_id>/<app_id>/<zone>/<stage>`` (``09`` §4).
        
                Raises:
                    ValueError: ``strategy: area_ratio`` with a ``threshold_area`` above ``1.0``.
                        See :meth:`_quant_area_ratio` -- a pixel² threshold against normalized
                        boxes quantises every frame to the bottom of the ladder, and a fire app
                        that reports ``low`` during a fire is worse than one that refuses to start.
        """
        ...

    def process(self: Any, ctx: Any) -> Any:
        """
        Quantise this zone's detections for one frame.
        
                Args:
                    ctx: The frame's detections, already entity-remapped and zone-assigned.
        
                Returns:
                    The level, its rank, the measured area and the peak confidence, plus one event
                    when a rung was reached.
        
                Note:
                    Every detection in the zone is quantised.
                    :class:`~matrice_analytics.engine.manifest.models.IncidentQuantiseConfig` has no
                    ``classes:`` field, so the narrowing is the *model's* -- recipe E's
                    ``detect: {classes: [fire, smoke]}`` documents the intent but does not filter
                    what this stage sees.  On a multi-class model that matters; see the workstream
                    report.
        """
        ...

    def reset(self: Any) -> None:
        """
        Clear the window peak at the aggregation boundary.
        
                :meth:`~matrice_analytics.engine.state.store.StateStore.end_window`, never
                ``clear()`` -- the distinction is the whole point of
                :class:`~matrice_analytics.engine.state.Lifetime` (``09`` §4 rule 2,
                **FROZEN-4**).
        """
        ...

    def window(self: Any, frames: Any[Any]) -> Any:
        """
        Collapse the window to its worst frame.
        
                The **peak**, not the mean.  Severity is ordinal: the average of ``critical`` and
                ``none`` is not ``medium``, and publishing a ratio-shaped aggregate of an ordinal
                is the same class of mistake as summing a percentage (**PY-1**).  ``area`` and
                ``confidence`` are the maxima over the window for the same reason -- they are the
                evidence for the peak level.
        
                No events.  Every candidate was already raised by :meth:`process` at the frame it
                happened on; repeating them here would give the runtime's find-or-create two
                arrivals for one occurrence.
        
                Args:
                    frames: This stage's per-frame outputs for the window, in frame order.
        """
        ...

