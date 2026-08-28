"""Auto-generated stub for module: engine."""
from typing import Any, Dict, List, Set

from .base_processor import BaseMetricProcessor
from .geometry import assign_detections_to_zones, build_zone_polygons_px
from .processors.incident import IncidentProcessor
from .processors.volume import VolumeProcessor
from .schemas import AggregationResult, FrameResult, FrameSummaryEntry, IncidentEvent, IncidentMessage, InputStreamEntry, InputStreamInfo, ResultValue, ResultWrapper, StreamInfo, TrackingStats

# Constants
logger: Any

# Classes
class AnalyticsEngine:
    # Orchestrator that reads a YAML manifest and dispatches frames to processors.
    #
    #     Zone analytics is always active for every metric-based category.  When
    #     ``StreamInfo.zone_config.zones`` contains named polygons, one processor
    #     of each loaded metric category (VOLUME, QUALITY, SAFETY, ...) is created
    #     **per zone** and detections are assigned via point-in-polygon containment
    #     before reaching any processor.  Otherwise a single ``"global"`` zone
    #     receives all detections.
    #
    #     Internal layout:
    #
    #     - ``_zone_metric_processors``: ``{zone_name: {category: processor}}``
    #       — all zone-aware processors, nested by zone then category.
    #     - ``_incident_processor``: the standalone INCIDENT processor (no zones).

    def __init__(self: Any, manifest_path_or_name: str, stream_info: Any | dict[str, Any] | None = None) -> None:
        """
        Load a YAML manifest and instantiate category processors.
        
                Args:
                    manifest_path_or_name: Absolute path or bare name (resolved under
                        ``config/``) of the YAML analytics manifest.
                    stream_info: Camera, application, and geometry context
                        (:class:`~matrice_analytics.analytics.schemas.StreamInfo`),
                        or a dict accepted by ``StreamInfo.model_validate``. Values
                        populate aggregation output; ``zone_config`` and ``resolution``
                        are merged with manifest ``volume.counter`` for geometry.
        """
        ...

    def aggregate(self: Any) -> Any:
        """
        Trigger 1-minute aggregation across all processors.
        
                For each zone, aggregates every loaded metric processor
                (VOLUME, QUALITY, SAFETY, ...).  Metrics are tagged with the
                zone name.  Only VOLUME processors contribute ``tracking_stats``
                (keyed per zone); QUALITY and SAFETY deliberately do not emit
                tracking_stats at aggregation time.
        """
        ...

    def app_id(self: Any) -> str:
        """
        Application ID from the manifest.
        """
        ...

    def app_name(self: Any) -> str:
        """
        Application name from the manifest.
        """
        ...

    def categories(self: Any) -> list[str]:
        """
        List of active category names (e.g. ``["VOLUME", "QUALITY", "INCIDENT"]``).
        
                Derived from the actual per-zone processor set so that any
                auto-created VOLUME fallback (for apps that don't declare VOLUME
                in their manifest) is still surfaced.
        """
        ...

    def drain_incident_events(self: Any) -> list[dict[str, Any]]:
        """
        Return and clear pending incident events as serialized ``IncidentMessage`` dicts.
        
                Each event is wrapped with :class:`IncidentMessage.from_event` using
                the engine's :attr:`stream_info`, producing dicts ready for Redis
                publishing.  Returns an empty list if no INCIDENT processor is loaded.
        """
        ...

    def get_incident_state(self: Any, camera_id: str) -> Any:
        """
        Debug access to per-camera incident lifecycle state.
        
                Returns an :class:`IncidentLifecycleState` copy or ``None``.
        """
        ...

    def incident_processor(self: Any) -> Any:
        """
        The standalone incident processor, or ``None`` if not loaded.
        """
        ...

    def process_frame(self: Any, detections: list[dict[str, Any]], frame_ts: float, frame_id: str = '') -> dict[str, Any]:
        """
        Process a single frame through all category processors.
        
                Assigns detections to zones (or the default ``"global"`` zone),
                runs every loaded metric processor (VOLUME, QUALITY, SAFETY, ...)
                per zone against the zone-filtered detections, then runs the
                standalone INCIDENT processor on all detections.
        
                Only the VOLUME processor in each zone contributes
                ``tracking_stats`` (``human_text`` + ``detections``) to the frame
                summary.  QUALITY/SAFETY contributions merge into the same zone's
                ``business_analytics`` and ``alerts``.
        
                Args:
                    detections: List of detection dicts with track_id pre-assigned.
                    frame_ts: Frame timestamp (seconds).
                    frame_id: Frame identifier string.
        
                Returns:
                    Combined FrameResult dict with zone-keyed ``agg_summary``.
        """
        ...

    def processors(self: Any) -> dict[str, Any]:
        """
        Flat mapping of category name → processor instance for the ``"global"`` zone.
        
                Provided for backwards compatibility with callers that expect a
                per-category view.  When named zones are active, this returns the
                processors of the first zone (typically still representative of
                per-category wiring).  Prefer :attr:`zone_metric_processors` for
                the full nested view.
        """
        ...

    def reset(self: Any) -> None:
        """
        Full reset of all processors and engine state.
        """
        ...

    def set_zone_config(self: Any, zone_config: dict[str, Any], width: int, height: int, method: str | None = None, in_direction: str = 'A_to_B', use_foot_center: bool = False) -> None:
        """
        Set geometry on the global VOLUME processor for entry/exit counting.
        
                Named-zone polygons are already configured at construction time via
                ``StreamInfo.zone_config.zones``; this helper is for apps that use
                line/polygon counters in the default ``"global"`` zone (footfall,
                people_counting, etc.).
        
                Args:
                    zone_config: Dict with ``"lines"`` and/or ``"zones"`` in normalized
                        (0-1) coordinates.
                    width: Frame width in pixels.
                    height: Frame height in pixels.
                    method: ``"abline"`` or ``"polygon"``.
                    in_direction: For abline -- ``"A_to_B"`` or ``"B_to_A"``.
                    use_foot_center: Use bottom-center of bbox instead of center.
        """
        ...

    def should_aggregate(self: Any, frame_ts: float) -> bool:
        """
        Check if enough time has elapsed to trigger 1-minute aggregation.
        """
        ...

    def stream_info(self: Any) -> Any:
        """
        Resolved stream metadata and geometry context.
        """
        ...

    def update_incident_thresholds(self: Any, camera_id: str, thresholds: list[dict[str, Any]], incident_type: str = '') -> None:
        """
        Update incident thresholds for a camera at runtime.
        
                Convenience method that delegates to the INCIDENT processor.
                Called by the config-polling caller when new thresholds arrive.
        """
        ...

    def zone_metric_processors(self: Any) -> dict[str, dict[str, Any]]:
        """
        Nested mapping of zone name → category → processor instance.
        
                This is the canonical runtime layout: every zone has one processor
                per loaded metric category.  INCIDENT is not included here (it is
                standalone and zone-agnostic — see :attr:`incident_processor`).
        """
        ...

    def zone_processors(self: Any) -> dict[str, Any]:
        """
        Mapping of zone name to that zone's ``VolumeProcessor`` instance.
        
                Kept for backwards compatibility with tests and debug tooling that
                expect a flat ``{zone: VolumeProcessor}`` view.  Use
                :attr:`zone_metric_processors` for the full nested
                ``{zone: {category: processor}}`` view.
        """
        ...

    def zones_active(self: Any) -> bool:
        """
        Whether named zone analytics is active (not just the default global).
        """
        ...

