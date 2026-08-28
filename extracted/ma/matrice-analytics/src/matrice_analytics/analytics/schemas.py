"""Pydantic models for the category-processor analytics pipeline."""

from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any

from pydantic import AliasChoices, BaseModel, ConfigDict, Field


class MetricEntry(BaseModel):
    """Single metric in the standardized metrics[] output format."""

    key: str  # e.g. "entry_count", "current_occupancy"
    data: float  # numeric value
    agg_type: str  # "sum" | "max" | "avg" | "last"
    category: str  # "VOLUME" | "QUALITY" | "SAFETY" | "IDENTITY" | ...
    zone: str = "global"  # zone name; "global" when zone is not predictable


# ---------------------------------------------------------------------------
# Incident schemas — config
# ---------------------------------------------------------------------------


class IncidentThreshold(BaseModel):
    """Single threshold level for incident severity calculation."""

    level: str  # "low", "medium", "significant", "critical"
    percentage: float  # quant value that triggers this level


class IncidentTypeConfig(BaseModel):
    """Configuration for one incident type from the YAML manifest."""

    key: str  # e.g. "fire_detection"
    name: str = ""
    thresholds: list[IncidentThreshold] = Field(default_factory=list)
    order: str = "ascending"  # "ascending" | "descending"


# ---------------------------------------------------------------------------
# Incident schemas — severity, lifecycle, and processor config
# ---------------------------------------------------------------------------


class SeverityLevel(str, Enum):
    """Severity levels for the incident lifecycle state machine."""

    none = "none"
    info = "info"
    low = "low"
    medium = "medium"
    significant = "significant"
    critical = "critical"


SEVERITY_ORDER: list[str] = ["none", "low", "medium", "significant", "critical"]
"""Ordered severity levels (ascending).  ``"info"`` is excluded because it is
a control signal, not a true severity rank."""


class LifecycleConfig(BaseModel):
    """Configurable thresholds for the consecutive-frame validation.

    Used by :class:`IncidentLifecycle`.
    """

    consecutive_frames_default: int = Field(
        default=5,
        description="Frames required to confirm medium / significant / critical.",
    )
    consecutive_frames_low: int = Field(
        default=10,
        description="Frames required to confirm low (stricter to avoid false positives).",
    )
    consecutive_frames_empty: int = Field(
        default=101,
        description="Consecutive empty frames before emitting an end-of-incident signal.",
    )


class QuantStrategyConfig(BaseModel):
    """Selects how ``incident_quant`` is computed from raw detections."""

    strategy: str = Field(
        default="max_confidence",
        description="One of: area_ratio, max_confidence, count_based.",
    )
    threshold_area: float = Field(
        default=250200.0,
        description="Reference area in px² (used by area_ratio strategy).",
    )
    count_threshold: int = Field(
        default=10,
        description="Reference detection count (used by count_based strategy).",
    )


class IncidentProcessorConfig(BaseModel):
    """Parsed and validated incident section from the YAML manifest.

    Single source of truth for how the ``IncidentProcessor`` behaves.
    """

    incident_types: list[IncidentTypeConfig] = Field(default_factory=list)
    quant: QuantStrategyConfig = Field(default_factory=QuantStrategyConfig)
    lifecycle: LifecycleConfig = Field(default_factory=LifecycleConfig)


class IncidentLifecycleState(BaseModel):
    """Per-camera mutable state managed by :class:`IncidentLifecycle`.

    ``validate_assignment=True`` ensures Pydantic validates every field
    mutation, keeping the state machine honest.
    """

    model_config = ConfigDict(validate_assignment=True)

    current_level: SeverityLevel = SeverityLevel.none
    pending_level: SeverityLevel = SeverityLevel.none
    consecutive_count: int = 0
    last_published_level: SeverityLevel = SeverityLevel.none
    incident_cycle_id: int = 1
    empty_frames_count: int = 0
    incident_active: bool = False
    current_incident_id: str = ""
    start_time: str = ""
    event_detected_count: int = 0


class IncidentFrameResult(BaseModel):
    """Return type for ``IncidentProcessor.process_frame()``.

    Carries the per-frame incident state snapshot.  No metrics — incidents
    are event-driven, not aggregated.
    """

    camera_id: str = ""
    incident_type: str = ""
    severity_level: SeverityLevel = SeverityLevel.none
    incident_quant: float = 0.0
    event_confidence: float = 0.0
    incident_active: bool = False
    event_detected_count: int = 0
    events_emitted: int = 0


# ---------------------------------------------------------------------------
# Incident schemas — event and Redis message
# ---------------------------------------------------------------------------


class IncidentEvent(BaseModel):
    """Event emitted by ``IncidentProcessor`` when an incident state changes.

    Produced by the lifecycle state machine and drained via
    ``drain_incident_events()``.
    """

    incident_id: str = ""
    incident_type: str = ""
    severity_level: str = ""
    human_text: str = ""
    start_time: str = ""
    end_time: str = ""
    camera_id: str = ""
    cycle_id: int = 0
    is_escalation: bool = False
    is_end_signal: bool = False
    incident_quant: float = 0.0
    event_confidence: float = 0.0
    frame_id: str = ""


class IncidentDetail(BaseModel):
    """Single incident entry within an :class:`IncidentMessage`."""

    incident_id: str = ""
    incident_type: str = ""
    severity_level: str = ""
    human_text: str = ""
    start_time: str = ""
    end_time: str = ""



class IncidentMessage(BaseModel):
    """Redis ``incident_res`` message matching Go tracker ``CameraEventIncoming``.

    Use :meth:`from_event` to construct from an :class:`IncidentEvent` and
    :class:`StreamInfo` context.
    """

    camera_id: str = ""
    app_deployment_id: str = ""
    application_id: str = ""
    application_name: str = ""
    camera_name: str = ""
    frame_id: str = ""
    rtp_number: str = ""
    location_name: str = ""
    stream_time: str = ""
    incidents: list[IncidentDetail] = Field(default_factory=list)

    @classmethod
    def from_event(
        cls,
        event: IncidentEvent,
        stream_info: StreamInfo | None = None,
        frame_id: str = "",
        stream_time: str = "",
        location_name: str = "",
    ) -> IncidentMessage:
        """Build an ``IncidentMessage`` from an event and stream context.

        Args:
            event: Incident event from ``IncidentProcessor.drain_incident_events()``.
            stream_info: Camera/application context (accepts ``None``).
            frame_id: Frame identifier string.
            stream_time: Formatted stream timestamp; overrides ``stream_info.stream_time``
                when non-empty.
            location_name: Human-readable location name.

        Returns:
            Fully populated ``IncidentMessage`` ready for serialization.
        """
        if stream_info is None:
            stream_info = StreamInfo()

        camera_id = event.camera_id or stream_info.camera_id or "default_camera"
        resolved_frame_id = frame_id or event.frame_id
        resolved_stream_time = (
            stream_time
            or stream_info.stream_time
            or datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")
        )
        resolved_rtp_number = stream_info.rtp_number or ""

        return cls(
            camera_id=camera_id,
            app_deployment_id=stream_info.app_deployment_id,
            application_id=stream_info.app_id,
            application_name=stream_info.application_name,
            camera_name=stream_info.camera_name,
            frame_id=resolved_frame_id,
            rtp_number=resolved_rtp_number,
            location_name=location_name or stream_info.location or "",
            stream_time=resolved_stream_time,
            incidents=[
                IncidentDetail(
                    incident_id=event.incident_id,
                    incident_type=event.incident_type,
                    severity_level=event.severity_level,
                    human_text=event.human_text,
                    start_time=event.start_time,
                    end_time=event.end_time,
                )
            ],
        )


class BoundingBox(BaseModel):
    """Bounding box coordinates."""

    xmin: float = 0.0
    ymin: float = 0.0
    xmax: float = 0.0
    ymax: float = 0.0


class DetectionEntry(BaseModel):
    """Single detection within tracking_stats."""

    category: str = ""
    bounding_box: BoundingBox = Field(default_factory=BoundingBox)


class TrackingStats(BaseModel):
    """Frame-level tracking statistics.

    Lightweight structure embedded in each ``FrameSummaryEntry`` within
    ``agg_summary``.  Contains only the human-readable text and the
    per-frame detection list.
    """

    human_text: str = ""
    detections: list[DetectionEntry] = Field(default_factory=list)


class ProcessorFrameOutput(BaseModel):
    """Raw per-frame output from a single category processor.

    Carries the processor's computed metrics and display-ready fields
    without the nested result envelope.  The engine combines outputs
    from all processors into the final :class:`FrameResult`.
    """

    metrics: list[MetricEntry] = Field(default_factory=list)
    business_analytics: dict[str, Any] = Field(default_factory=dict)
    human_text: str = ""
    detections: list[DetectionEntry] = Field(default_factory=list)
    alerts: list[dict[str, Any]] = Field(default_factory=list)
    frame_ts: float = 0.0
    frame_id: str = ""


class ProcessorAggregationOutput(BaseModel):
    """Per-category contribution to a 1-minute aggregation window.

    Parallels :class:`ProcessorFrameOutput` on the frame path: each metric
    processor returns only its piece (aggregated ``metrics[]`` and, for VOLUME,
    ``tracking_stats``). :meth:`~matrice_analytics.analytics.engine.AnalyticsEngine.aggregate`
    merges all chunks with :class:`StreamInfo` into the full
    :class:`AggregationResult` message.
    """

    metrics: list[dict[str, Any]] = Field(default_factory=list)
    tracking_stats: dict[str, Any] = Field(default_factory=dict)


class FrameSummaryEntry(BaseModel):
    """Single entry within agg_summary (keyed by frame index)."""

    tracking_stats: TrackingStats = Field(default_factory=TrackingStats)
    business_analytics: dict[str, Any] = Field(default_factory=dict)
    alerts: list[dict[str, Any]] = Field(default_factory=list)


class InputStreamInfo(BaseModel):
    """Metadata for an input stream."""

    original_fps: float = 0.0


class InputStreamEntry(BaseModel):
    """Wrapper for input stream info."""

    input_stream: InputStreamInfo = Field(default_factory=InputStreamInfo)


class ResultValue(BaseModel):
    """The value payload containing streams and analytics summary."""

    input_streams: list[InputStreamEntry] = Field(default_factory=list)
    agg_summary: dict[str, FrameSummaryEntry] = Field(default_factory=dict)


class ResultWrapper(BaseModel):
    """Top-level result wrapper."""

    value: ResultValue = Field(default_factory=ResultValue)


class FrameResult(BaseModel):
    """Output of a single process_frame() call.

    Serializes to::

        {
            "result": {
                "value": {
                    "input_streams": [...],
                    "agg_summary": {"0": {"tracking_stats": {...}, "business_analytics": {...}, "alerts": []}},
                }
            }
        }
    """

    result: ResultWrapper = Field(default_factory=ResultWrapper)

    # Internal fields for the aggregation pipeline (excluded from serialization)
    metrics: list[MetricEntry] = Field(default_factory=list, exclude=True)
    frame_ts: float = Field(default=0.0, exclude=True)
    frame_id: str = Field(default="", exclude=True)


class AggregationResult(BaseModel):
    """Output of :meth:`AnalyticsEngine.aggregate` — matches analytics_publisher format.

    Built by the engine from :class:`StreamInfo` plus merged
    :class:`ProcessorAggregationOutput` chunks. Top-level fields mirror
    ``AnalyticsPublisher._build_analytics_message`` so that consumers see
    identical JSON whether the message came from the
    publisher (production) or from the analytics engine directly.

    Field names use the exact keys that analytics_publisher emits
    (mixed snake_case / camelCase) to avoid alias/serialization complexity.
    """

    camera_id: str = ""
    camera_name: str = ""
    app_deployment_id: str = ""
    app_id: str = ""
    camera_group: str = ""
    locationId: str = ""  # noqa: N815
    location: str = ""
    application_name: str = ""
    application_key_name: str = ""
    application_version: str = ""

    # Aggregated tracking statistics
    tracking_stats: dict[str, Any] = Field(default_factory=dict)

    # Standardized metrics list
    metrics: list[dict[str, Any]] = Field(default_factory=list)


class ZoneConfig(BaseModel):
    """Normalized geometry for volume / footfall (lines and zones only).

    Coordinates are typically normalized to ``0.0``-``1.0``. ``lines`` values
    may be a single ``[x, y]`` pair or segment endpoints ``[[x1, y1], [x2, y2]]``
    per named line.

    Counting parameters (``method``, ``in_direction``, ``use_foot_center``)
    live under the manifest ``volume.counter`` section; frame size is
    :attr:`StreamInfo.resolution`.
    """

    model_config = ConfigDict(extra="ignore")

    lines: dict[str, list[float] | list[list[float]]] = Field(
        default_factory=dict,
        description="Named lines: map line name to [x, y] or [[x,y],[x,y]] segment endpoints.",
    )
    zones: dict[str, list[list[float]]] = Field(
        default_factory=dict,
        description="Named polygons as lists of [x, y] vertices.",
    )


class StreamInfo(BaseModel):
    """Per-stream context: camera, application, and geometry for analytics.

    Combines fields present in aggregation summaries (camera/app identity),
    frame-level input stream metadata (e.g. ``original_fps`` from
    ``input_streams[].input_stream``), and optional ``zone_config`` (lines and
    zones only; counting options come from the manifest ``volume.counter``).
    """

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    # --- Camera (identity, location, stream) ---
    camera_id: str = ""
    camera_name: str = ""
    camera_group: str = ""
    location_id: str = Field(
        default="",
        validation_alias=AliasChoices("location_id", "locationId"),
        serialization_alias="locationId",
        description="Location identifier (aggregation JSON key is locationId).",
    )
    location: str = ""
    original_fps: float = Field(
        default=0.0,
        description="Source frame rate from input_streams[].input_stream.original_fps.",
    )
    rtp_number: str = Field(
        default="",
        description="RTP sequence number for media server frame retrieval.",
    )
    stream_time: str = Field(
        default="",
        description="Stream timestamp string from the pipeline (e.g. YYYY-MM-DD-HH:MM:SS.ffffff UTC).",
    )

    resolution: list[int] = Field(
        default_factory=lambda: [0, 0],
        description="Frame size in pixels as [width, height].",
    )

    # --- Application (deployment and catalog identity) ---
    app_deployment_id: str = ""
    app_id: str = ""
    application_name: str = ""
    application_key_name: str = ""
    application_version: str = ""

    # --- Geometry (volume / footfall) ---
    zone_config: ZoneConfig | None = Field(
        default=None,
        description="Named lines and polygons (normalized coordinates).",
    )
