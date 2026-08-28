"""The runtime: manifest + stream + detections -> validated payloads.

``_contracts/09-tobe-engine-architecture.md`` §§1-4, ``clauding/STAGE_BC_PLAN.md`` §3.

Three modules, one job each:

* :mod:`~matrice_analytics.engine.runtime.stream_info` -- typed parsing of the untyped
  ``stream_info`` dict (surface **S4**), with every fallback logged so drift is visible.
* :mod:`~matrice_analytics.engine.runtime.session` -- per-camera execution:
  ``detections -> entity remap -> zone partition (once) -> pipeline per zone``.
* :mod:`~matrice_analytics.engine.runtime.window` -- the 60-second aggregation boundary, on the
  injectable frame clock (**PY-13**), and the ``results-agg`` message it publishes.

The whole chain, from an app reference to a wire payload::

    from matrice_analytics.engine.manifest.loader import load_app_bundle
    from matrice_analytics.engine.runtime import Session
    from matrice_analytics.engine.publish import RedisStreamPublisher

    app = load_app_bundle("people_counting@1.6")
    session = Session.from_loaded_app(app, stream_info, publisher=RedisStreamPublisher())
    for frame in frames:
        outcome = session.process_frame(frame.detections, frame_ts=frame.ts)
        # outcome.payload() is the per-frame return value; results-agg and incident_res
        # have already gone to the publisher.

Nothing here imports ``post_processing`` or ``analytics`` (**PY-20**).
"""

from __future__ import annotations

from matrice_analytics.engine.runtime.session import (
    DEFAULT_THRESHOLD_SEVERITY,
    FrameOutcome,
    Session,
    SessionError,
)
from matrice_analytics.engine.runtime.stream_info import (
    FieldSource,
    StreamInfoError,
    StreamInfoParse,
    parse_stream_info,
    resolve_stream_info,
)
from matrice_analytics.engine.runtime.window import (
    AggregationWindow,
    MetricPlan,
    ZoneCounters,
    collapse,
    human_text_for,
    metric_plan,
    stage_key_map,
)

__all__ = [
    # session
    "DEFAULT_THRESHOLD_SEVERITY",
    "FrameOutcome",
    "Session",
    "SessionError",
    # stream_info (S4)
    "FieldSource",
    "StreamInfoError",
    "StreamInfoParse",
    "parse_stream_info",
    "resolve_stream_info",
    # window
    "AggregationWindow",
    "MetricPlan",
    "ZoneCounters",
    "collapse",
    "human_text_for",
    "metric_plan",
    "stage_key_map",
]
