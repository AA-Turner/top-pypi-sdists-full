"""Auto-generated stub for module: schemas."""
from typing import Any

# Classes
class AggregationResult:
    # Output of :meth:`AnalyticsEngine.aggregate` — matches analytics_publisher format.
    #
    #     Built by the engine from :class:`StreamInfo` plus merged
    #     :class:`ProcessorAggregationOutput` chunks. Top-level fields mirror
    #     ``AnalyticsPublisher._build_analytics_message`` so that consumers see
    #     identical JSON whether the message came from the
    #     publisher (production) or from the analytics engine directly.
    #
    #     Field names use the exact keys that analytics_publisher emits
    #     (mixed snake_case / camelCase) to avoid alias/serialization complexity.

    ...
class BoundingBox:
    # Bounding box coordinates.

    ...
class DetectionEntry:
    # Single detection within tracking_stats.

    ...
class FrameResult:
    # Output of a single process_frame() call.
    #
    #     Serializes to::
    #
    #         {
    #             "result": {
    #                 "value": {
    #                     "input_streams": [...],
    #                     "agg_summary": {"0": {"tracking_stats": {...}, "business_analytics": {...}, "alerts": []}},
    #                 }
    #             }
    #         }

    ...
class FrameSummaryEntry:
    # Single entry within agg_summary (keyed by frame index).

    ...
class IncidentDetail:
    # Single incident entry within an :class:`IncidentMessage`.

    ...
class IncidentEvent:
    # Event emitted by ``IncidentProcessor`` when an incident state changes.
    #
    #     Produced by the lifecycle state machine and drained via
    #     ``drain_incident_events()``.

    ...
class IncidentFrameResult:
    # Return type for ``IncidentProcessor.process_frame()``.
    #
    #     Carries the per-frame incident state snapshot.  No metrics — incidents
    #     are event-driven, not aggregated.

    ...
class IncidentLifecycleState:
    # Per-camera mutable state managed by :class:`IncidentLifecycle`.
    #
    #     ``validate_assignment=True`` ensures Pydantic validates every field
    #     mutation, keeping the state machine honest.

    model_config: Any

class IncidentMessage:
    # Redis ``incident_res`` message matching Go tracker ``CameraEventIncoming``.
    #
    #     Use :meth:`from_event` to construct from an :class:`IncidentEvent` and
    #     :class:`StreamInfo` context.

    def from_event(cls: Any, event: Any, stream_info: Any | None = None, frame_id: str = '', stream_time: str = '', location_name: str = '') -> Any:
        """
        Build an ``IncidentMessage`` from an event and stream context.
        
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
        ...

class IncidentProcessorConfig:
    # Parsed and validated incident section from the YAML manifest.
    #
    #     Single source of truth for how the ``IncidentProcessor`` behaves.

    ...
class IncidentThreshold:
    # Single threshold level for incident severity calculation.

    ...
class IncidentTypeConfig:
    # Configuration for one incident type from the YAML manifest.

    ...
class InputStreamEntry:
    # Wrapper for input stream info.

    ...
class InputStreamInfo:
    # Metadata for an input stream.

    ...
class LifecycleConfig:
    # Configurable thresholds for the consecutive-frame validation.
    #
    #     Used by :class:`IncidentLifecycle`.

    ...
class MetricEntry:
    # Single metric in the standardized metrics[] output format.

    ...
class ProcessorAggregationOutput:
    # Per-category contribution to a 1-minute aggregation window.
    #
    #     Parallels :class:`ProcessorFrameOutput` on the frame path: each metric
    #     processor returns only its piece (aggregated ``metrics[]`` and, for VOLUME,
    #     ``tracking_stats``). :meth:`~matrice_analytics.analytics.engine.AnalyticsEngine.aggregate`
    #     merges all chunks with :class:`StreamInfo` into the full
    #     :class:`AggregationResult` message.

    ...
class ProcessorFrameOutput:
    # Raw per-frame output from a single category processor.
    #
    #     Carries the processor's computed metrics and display-ready fields
    #     without the nested result envelope.  The engine combines outputs
    #     from all processors into the final :class:`FrameResult`.

    ...
class QuantStrategyConfig:
    # Selects how ``incident_quant`` is computed from raw detections.

    ...
class ResultValue:
    # The value payload containing streams and analytics summary.

    ...
class ResultWrapper:
    # Top-level result wrapper.

    ...
class SeverityLevel:
    # Severity levels for the incident lifecycle state machine.

    critical: str
    info: str
    low: str
    medium: str
    none: str
    significant: str

class StreamInfo:
    # Per-stream context: camera, application, and geometry for analytics.
    #
    #     Combines fields present in aggregation summaries (camera/app identity),
    #     frame-level input stream metadata (e.g. ``original_fps`` from
    #     ``input_streams[].input_stream``), and optional ``zone_config`` (lines and
    #     zones only; counting options come from the manifest ``volume.counter``).

    model_config: Any

class TrackingStats:
    # Frame-level tracking statistics.
    #
    #     Lightweight structure embedded in each ``FrameSummaryEntry`` within
    #     ``agg_summary``.  Contains only the human-readable text and the
    #     per-frame detection list.

    ...
class ZoneConfig:
    # Normalized geometry for volume / footfall (lines and zones only).
    #
    #     Coordinates are typically normalized to ``0.0``-``1.0``. ``lines`` values
    #     may be a single ``[x, y]`` pair or segment endpoints ``[[x1, y1], [x2, y2]]``
    #     per named line.
    #
    #     Counting parameters (``method``, ``in_direction``, ``use_foot_center``)
    #     live under the manifest ``volume.counter`` section; frame size is
    #     :attr:`StreamInfo.resolution`.

    model_config: Any

