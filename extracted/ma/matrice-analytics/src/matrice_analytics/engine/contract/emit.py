"""The single build + validate + publish path for every outbound payload.

Objective **O1**.  There are currently three independent ``results-agg``
builders -- ``analytics/engine.py:257-300``,
``utils/legacy_analytics_bridge.py:2989-3044`` and
``analytics/analytics_publisher.py:911-925`` -- with divergent field sets;
the third adds ``inferencePipelineId`` and ``deployment_instance_id`` and
**omits ``metrics`` entirely** (defect PY-3).  This module replaces all
three.

Two rules make that stick:

1. :func:`to_payload` is the **only** function in the codebase that turns a
   contract model into a wire dict.  Nothing else calls ``model_dump``.
2. Every ``build_*`` function validates through
   :mod:`matrice_analytics.engine.contract.conformance` before returning, so
   a non-conforming payload cannot leave the engine (contract Section 1 rule
   3: the backend validates almost nothing).

Transport is deliberately absent.  :class:`Publisher` is a two-line
:class:`~typing.Protocol`; the Redis implementation is a later workstream.
That keeps the contract module importable, testable and dependency-free.
"""

from __future__ import annotations

import logging
from collections.abc import Mapping, Sequence
from datetime import datetime
from typing import Any, Final, Protocol, runtime_checkable

from matrice_analytics.engine.contract.conformance import Surface, assert_conforms
from matrice_analytics.engine.contract.schemas import (
    AggregationResult,
    Category,
    FrameResult,
    FrameSummaryEntry,
    Incident,
    IncidentMessage,
    InputStreamEntry,
    InputStreamInfo,
    MetricEntry,
    ResultValue,
    ResultWrapper,
    StreamInfo,
    TrackingStats,
    to_rfc3339z,
    to_stream_time,
)

logger = logging.getLogger(__name__)

__all__ = [
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
]


STREAM_RESULTS_AGG: Final[str] = "results-agg"
"""S1 Redis stream name. ``XADD results-agg {"data": <json>}``, one message
per 60-second window per camera."""

STREAM_INCIDENT_RES: Final[str] = "incident_res"
"""S2 Redis stream name. ``XADD incident_res {"data": <json>}``, emitted on a
severity transition, never per frame."""

PAYLOAD_FIELD: Final[str] = "data"
"""The Redis stream field the JSON payload is written under.

Every consumer hedges on this name -- be-media-server tries ``data`` then any
valid-JSON field, be-analytics tries ``data`` then ``result`` then ``value``
-- which is evidence it has changed at least once.  py_analytics' own writer
has always used ``data``; keep it.
"""


@runtime_checkable
class Publisher(Protocol):
    """Anything that can put a payload on a named stream.

    Intentionally minimal.  **No Redis here** -- transport, connection
    management, retry and the ``_message_key`` partitioning hint belong to a
    separate workstream.  The contract module's job ends when a validated
    dict has been handed over.

    Implementations must not mutate ``payload``.
    """

    def publish(self, stream: str, payload: dict[str, Any]) -> None:
        """Publish ``payload`` to ``stream``.

        Args:
            stream: :data:`STREAM_RESULTS_AGG` or :data:`STREAM_INCIDENT_RES`.
            payload: A conforming wire dict from :func:`to_payload`.
        """
        ...


# ---------------------------------------------------------------------------
# Serialisation -- the one place a payload dict is constructed
# ---------------------------------------------------------------------------


def to_payload(
    model: AggregationResult | IncidentMessage | FrameResult,
) -> dict[str, Any]:
    """Serialise a contract model to its wire dict.

    ``by_alias=True`` is what emits the frozen camelCase names -- ``locationId``
    (FROZEN-1) and ``imageUrl`` (FROZEN-3).  Dumping without it silently
    produces ``location_id``/``image_url``, which breaks ingestion with no
    error anywhere: the row simply arrives with ``_idLocation = ""``.  That is
    the reason this lives in exactly one function.

    ``mode="json"`` renders enums as their string values and keeps every
    number JSON-native.  ``exclude_none=True`` guarantees rule 7 -- no
    ``None`` ever reaches the wire (every declared string already defaults to
    ``""``; the only nullable field in the contract is ``detections[].track_id``,
    which is omitted rather than sent as ``null``).

    Args:
        model: A validated contract model.

    Returns:
        A plain JSON-serialisable dict.
    """
    return model.model_dump(mode="json", by_alias=True, exclude_none=True)


# ---------------------------------------------------------------------------
# S1 -- results-agg
# ---------------------------------------------------------------------------


def build_aggregation(
    stream_info: StreamInfo,
    *,
    input_timestamp: datetime | int | float | str,
    tracking_stats: Mapping[str, TrackingStats] | None = None,
    metrics: Sequence[MetricEntry] | None = None,
) -> AggregationResult:
    """Build and validate one ``results-agg`` message (S1).

    Args:
        stream_info: The typed per-stream context (S4).  Supplies every
            envelope identity field, including ``location_id``, which is
            emitted as ``locationId`` (FROZEN-1).
        input_timestamp: The window's event time.  Set **unconditionally** --
            without a root ``input_timestamp`` the backend falls back to "the
            first zone's timestamp", where "first" is Go map iteration order
            and therefore nondeterministic (BE-5).  Accepts anything
            :func:`~...schemas.to_rfc3339z` accepts.
        tracking_stats: Zone id -> :class:`~...schemas.TrackingStats`
            (FROZEN-2: keyed by zone, never flat).  Single-bucket apps use the
            literal key ``"global"``.
        metrics: The window's ``metrics[]`` entries.

    Returns:
        A conforming :class:`~...schemas.AggregationResult`.

    Raises:
        pydantic.ValidationError: A field is structurally wrong (illegal enum,
            numeric string, bad timestamp).
        ConformanceViolation: The assembled payload fails one of the six
            checks -- most commonly "at least one of tracking_stats / metrics
            must be non-empty", which the backend answers by dropping the
            whole message.
    """
    result = AggregationResult(
        camera_id=stream_info.camera_id,
        camera_name=stream_info.camera_name,
        app_deployment_id=stream_info.app_deployment_id,
        app_id=stream_info.app_id,
        camera_group=stream_info.camera_group,
        location_id=stream_info.location_id,
        location=stream_info.location,
        application_name=stream_info.application_name,
        application_key_name=stream_info.application_key_name,
        application_version=stream_info.application_version,
        input_timestamp=to_rfc3339z(input_timestamp),
        rtp_number=stream_info.rtp_number,
        tracking_stats=dict(tracking_stats or {}),
        metrics=list(metrics or []),
    )
    assert_conforms(to_payload(result), Surface.results_agg)
    return result


def publish_aggregation(publisher: Publisher, result: AggregationResult) -> None:
    """Serialise and publish an ``results-agg`` message.

    Re-validates on the way out: :func:`build_aggregation` validated at build
    time, but a model is mutable and this is the last point at which a
    non-conforming payload can be stopped.

    Args:
        publisher: The transport.
        result: The message to send.

    Raises:
        ConformanceViolation: The payload no longer conforms.
    """
    payload = to_payload(result)
    assert_conforms(payload, Surface.results_agg)
    logger.debug(
        "publishing %s for camera=%s zones=%d metrics=%d",
        STREAM_RESULTS_AGG,
        result.camera_id,
        len(result.tracking_stats),
        len(result.metrics),
    )
    publisher.publish(STREAM_RESULTS_AGG, payload)


# ---------------------------------------------------------------------------
# S2 -- incident_res
# ---------------------------------------------------------------------------


def build_incident(
    stream_info: StreamInfo,
    *,
    incidents: Sequence[Incident],
    category: Category | str = "",
    frame_id: str | None = None,
    stream_time: datetime | int | float | str | None = None,
    rtp_number: str | None = None,
) -> IncidentMessage:
    """Build and validate one ``incident_res`` message (S2).

    Emit on a severity **transition** only.  The backend does find-or-create
    with up-only escalation: re-sending the same severity is a no-op,
    de-escalation is not representable, and only a non-empty ``end_time``
    closes an incident (contract Section 3.4).

    Note the deliberate naming divergence from S1: this surface carries
    ``application_id`` (not ``app_id``) and ``location_name`` (not
    ``location``).  Both are frozen -- they match a different Go DTO.

    Args:
        stream_info: The typed per-stream context (S4).
        incidents: One or more :class:`~...schemas.Incident` entries.
        category: ``SAFETY`` / ``QUALITY`` / ``VOLUME`` or ``""`` (untagged).
        frame_id: Legacy Redis frame key; falls back to
            ``stream_info.frame_id``.
        stream_time: Media anchor in the §3.3 format.  A datetime or epoch is
            formatted by :func:`~...schemas.to_stream_time`; a string is
            passed through and validated.  Falls back to
            ``stream_info.stream_time``.
        rtp_number: The frame's RTP timestamp -- the anchor the backend
            resolves the alert thumbnail and the looked-up wall-clock time
            from.  Falls back to ``stream_info.rtp_number``.  Present for the
            same reason ``frame_id`` is: all three are per-frame, and a
            builder that overrode only two invited callers to publish a
            current frame's id beside a stale image anchor.

    Returns:
        A conforming :class:`~...schemas.IncidentMessage`.  ``camera_name`` is
        blanked when it equals ``camera_id`` (FROZEN-8).

    Raises:
        pydantic.ValidationError: A field is structurally wrong (e.g. a
            severity that is not one of the five lowercase wire values).
        ConformanceViolation: The assembled payload fails one of the six
            checks.
    """
    if stream_time is None:
        resolved_stream_time = stream_info.stream_time
    elif isinstance(stream_time, str):
        resolved_stream_time = stream_time
    else:
        resolved_stream_time = to_stream_time(stream_time)

    message = IncidentMessage(
        camera_id=stream_info.camera_id,
        camera_name=stream_info.camera_name,
        app_deployment_id=stream_info.app_deployment_id,
        application_id=stream_info.app_id,
        application_name=stream_info.application_name,
        location_name=stream_info.location,
        frame_id=stream_info.frame_id if frame_id is None else frame_id,
        rtp_number=stream_info.rtp_number if rtp_number is None else rtp_number,
        stream_time=resolved_stream_time,
        category=category,
        incidents=list(incidents),
    )
    assert_conforms(to_payload(message), Surface.incident_res)
    return message


def publish_incident(publisher: Publisher, message: IncidentMessage) -> None:
    """Serialise and publish an ``incident_res`` message.

    Args:
        publisher: The transport.
        message: The message to send.

    Raises:
        ConformanceViolation: The payload no longer conforms.
    """
    payload = to_payload(message)
    assert_conforms(payload, Surface.incident_res)
    logger.debug(
        "publishing %s for camera=%s incidents=%d",
        STREAM_INCIDENT_RES,
        message.camera_id,
        len(message.incidents),
    )
    publisher.publish(STREAM_INCIDENT_RES, payload)


# ---------------------------------------------------------------------------
# S3 -- the per-frame return value
# ---------------------------------------------------------------------------


def build_frame_result(
    *,
    agg_summary: Mapping[str, FrameSummaryEntry],
    original_fps: float,
) -> FrameResult:
    """Build and validate the per-frame return value (S3).

    py_analytics does not publish this -- it returns a dict and an inference
    worker outside this workspace XADDs it to
    ``<cameraId>_<appDeploymentId>_output_topic``.  We own ``agg_summary`` and
    the detections inside it; the worker stamps everything else.

    Three properties are guaranteed here:

    * ``agg_summary`` is **keyed by zone** (PY-5).  Today the key is
      ``"<int>"``, ``"None"``, ``"current_frame"`` or a zone name depending
      on the file.  This is a visible behaviour change for three consumers
      and must be announced, not slipped in.
    * Each zone's ``tracking_stats`` carries **all four count lists** (PY-2),
      guaranteed by :class:`~...schemas.FrameTrackingStats` inheriting from
      :class:`~...schemas.TrackingStats`.  Without them be-analytics'
      ``hasTrackingStats`` fails on all seven probe paths and every instant
      metric evaluates against zero.
    * Detections appear **once**, inside the zone that owns them.  There is
      no top-level ``detections`` echo: the duplicate copies are why
      fe-streaming dedupes by bbox string key, a dedupe that silently
      collapses two genuine objects at identical coordinates.

    ``agg_summary`` is emitted twice -- nested under ``result.value`` and
    hoisted to the top level -- because consumers probe both paths.  The two
    are the same data by construction.

    Args:
        agg_summary: Zone id -> :class:`~...schemas.FrameSummaryEntry`.
        original_fps: Source frame rate, echoed in
            ``result.value.input_streams``.

    Returns:
        A conforming :class:`~...schemas.FrameResult`.

    Raises:
        pydantic.ValidationError: A field is structurally wrong (e.g. a
            bounding box outside 0-1).
        ConformanceViolation: The assembled payload fails one of the six
            checks.
    """
    zones = dict(agg_summary)
    frame = FrameResult(
        result=ResultWrapper(
            value=ResultValue(
                input_streams=[
                    InputStreamEntry(
                        input_stream=InputStreamInfo(original_fps=original_fps)
                    )
                ],
                agg_summary=zones,
            )
        ),
        agg_summary=zones,
    )
    assert_conforms(to_payload(frame), Surface.frame_result)
    return frame
