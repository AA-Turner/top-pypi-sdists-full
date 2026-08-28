"""The canonical output contract for py_analytics.

Three modules, one job each:

* :mod:`~matrice_analytics.engine.contract.schemas` -- THE wire format,
  declared once (objective **O1**).
* :mod:`~matrice_analytics.engine.contract.emit` -- the single
  build + validate + publish path.  The only place a payload dict is
  constructed.
* :mod:`~matrice_analytics.engine.contract.conformance` -- the six checks
  from contract Section 7, reused verbatim by the auto-generated per-app test
  suites (objective **O5**).

Normative spec: ``_contracts/07-tobe-canonical-contract.md``.  The frozen
quirks it preserves are catalogued in ``_contracts/12-defect-register.md``
Section FROZEN and cited by id in every docstring that implements one.

This package has no dependency on ``matrice_analytics.post_processing`` or
``matrice_analytics.analytics``.
"""

from __future__ import annotations

from matrice_analytics.engine.contract.conformance import (
    COUNT_LIST_FIELDS,
    ConformanceError,
    ConformanceViolation,
    Surface,
    assert_conforms,
    check_enum_values,
    check_no_stray_camelcase,
    check_payload_not_empty,
    check_required_fields,
    check_timestamps,
    check_tracking_stats_shape,
    conformance_errors,
    conforms,
)
from matrice_analytics.engine.contract.emit import (
    PAYLOAD_FIELD,
    STREAM_INCIDENT_RES,
    STREAM_RESULTS_AGG,
    Publisher,
    build_aggregation,
    build_frame_result,
    build_incident,
    publish_aggregation,
    publish_incident,
    to_payload,
)
from matrice_analytics.engine.contract.schemas import (
    ALLOWED_CAMELCASE_FIELDS,
    GLOBAL_ZONE,
    INTERNAL_SEVERITY_ALIASES,
    SEVERITY_RANK,
    AggregationResult,
    AggType,
    BoundingBox,
    Category,
    Detection,
    FrameResult,
    FrameSummaryEntry,
    FrameTrackingStats,
    Incident,
    IncidentMessage,
    IncidentStatus,
    InputStreamEntry,
    InputStreamInfo,
    MetricEntry,
    ResultValue,
    ResultWrapper,
    Severity,
    StreamInfo,
    StreamInfoError,
    TrackingCount,
    TrackingStats,
    ZoneConfig,
    derive_incident_status,
    is_rfc3339z,
    is_stream_time,
    now_rfc3339z,
    parse_agg_type,
    parse_category,
    parse_incident_category,
    parse_rfc3339z,
    parse_severity,
    parse_stream_time,
    to_rfc3339z,
    to_stream_time,
)

__all__ = [
    # schemas -- enums and vocabulary
    "AggType",
    "Category",
    "IncidentStatus",
    "Severity",
    "ALLOWED_CAMELCASE_FIELDS",
    "GLOBAL_ZONE",
    "INTERNAL_SEVERITY_ALIASES",
    "SEVERITY_RANK",
    "parse_agg_type",
    "parse_category",
    "parse_incident_category",
    "parse_severity",
    "derive_incident_status",
    # schemas -- timestamps
    "is_rfc3339z",
    "is_stream_time",
    "now_rfc3339z",
    "parse_rfc3339z",
    "parse_stream_time",
    "to_rfc3339z",
    "to_stream_time",
    # schemas -- S1
    "AggregationResult",
    "MetricEntry",
    "TrackingCount",
    "TrackingStats",
    # schemas -- S2
    "Incident",
    "IncidentMessage",
    # schemas -- S3
    "BoundingBox",
    "Detection",
    "FrameResult",
    "FrameSummaryEntry",
    "FrameTrackingStats",
    "InputStreamEntry",
    "InputStreamInfo",
    "ResultValue",
    "ResultWrapper",
    # schemas -- S4
    "StreamInfo",
    "StreamInfoError",
    "ZoneConfig",
    # emit
    "PAYLOAD_FIELD",
    "Publisher",
    "STREAM_INCIDENT_RES",
    "STREAM_RESULTS_AGG",
    "build_aggregation",
    "build_frame_result",
    "build_incident",
    "publish_aggregation",
    "publish_incident",
    "to_payload",
    # conformance
    "COUNT_LIST_FIELDS",
    "ConformanceError",
    "ConformanceViolation",
    "Surface",
    "assert_conforms",
    "check_enum_values",
    "check_no_stray_camelcase",
    "check_payload_not_empty",
    "check_required_fields",
    "check_timestamps",
    "check_tracking_stats_shape",
    "conformance_errors",
    "conforms",
]
