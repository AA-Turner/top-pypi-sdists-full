"""Stub file for analytics directory."""
from typing import Any, Callable, Dict, List, Optional, Set, Union

from ..post_processing.Trackers.integration import ConfigDrivenTracker, TrackerProfile
from ..post_processing.utils.counting_utils import ABLineCounter, PolygonCounter, parse_line_config, polygon_offset_inward
from ..post_processing.utils.post_processing_config_client import is_null_object_id, normalize_location_id
from .base_processor import BaseMetricProcessor
from .engine import AnalyticsEngine
from .engine_session import normalize_index_to_category
from .geometry import assign_detections_to_zones, build_zone_polygons_px
from .processors.incident import IncidentProcessor
from .processors.volume import VolumeProcessor
from .schemas import AggregationResult, FrameResult, FrameSummaryEntry, IncidentEvent, IncidentMessage, InputStreamEntry, InputStreamInfo, ResultValue, ResultWrapper, StreamInfo, TrackingStats
from .schemas import BoundingBox, DetectionEntry, MetricEntry, ProcessorAggregationOutput, ProcessorFrameOutput
from .schemas import QuantStrategyConfig
from .schemas import SEVERITY_ORDER, IncidentEvent, IncidentLifecycleState, LifecycleConfig, SeverityLevel

# Constants
logger: Any = ...  # From base_processor
logger: Any = ...  # From engine
logger: Any = ...  # From engine_session
ALLOWED_CATEGORIES: Set[Any] = ...  # From flow
FLOW_ENV_VAR: str = ...  # From flow
NEW_FLOW_DENYLIST: Set[Any] = ...  # From flow
NEW_FLOW_HARNESS_DENYLIST: Set[Any] = ...  # From flow
logger: Any = ...  # From flow
logger: Any = ...  # From geometry
logger: Any = ...  # From incident_lifecycle
QuantFn: Any = ...  # From quant_strategies
logger: Any = ...  # From quant_strategies
AGG_STREAM: str = ...  # From redis_publisher
INCIDENT_STREAM: str = ...  # From redis_publisher
logger: Any = ...  # From redis_publisher

# Functions
# From engine_session
def build_coco_harness_mislabel_lookup(model_index_to_category: Dict[int, str]) -> Dict[str, int]:
    """
    Map wrong COCO string labels back to custom-model class ids.
    
        The inference harness labels PPE model outputs with COCO names at the same
        numeric index (e.g. class 0 → ``person`` instead of ``Hardhat``,
        class 5 → ``bus`` instead of ``Person``). When ``class_id`` is stripped
        and only the wrong string remains, reverse via the default COCO name at
        each model index.
    """
    ...

# From engine_session
def detection_class_id_from_detection(det: Dict[str, Any]) -> Optional[int]:
    """
    Best-effort numeric class id from common inference field names.
    
        Prefer ``category_id`` / ``cls`` / ``class`` before ``class_id`` — the
        harness often sticks ``class_id`` at 0 while ``category_id`` still carries
        the true model class.
    """
    ...

# From engine_session
def looks_like_coco_index_to_category(mapping: Optional[Dict[int, str]]) -> bool:
    """
    Heuristic: deployment UI often ships a generic COCO map for custom models.
    """
    ...

# From engine_session
def looks_like_wrong_ppe_index_to_category(mapping: Optional[Dict[int, str]]) -> bool:
    """
    Detect incomplete or mis-typed PPE maps (e.g. ``{0: 'Person'}`` from the UI).
    """
    ...

# From engine_session
def map_detection_categories(detections: List[Dict[str, Any]], index_to_category: Optional[Dict[Any, Any]]) -> List[Dict[str, Any]]:
    """
    Map detections to labels from ``index_to_category`` config.
    
        Shared by new-flow AnalyticsEngineSession and legacy ``ppe_compliance``.
    
        PPE harness reality (``ppe_coco_fixup=True``):
          - ``class_id`` is often stuck at 0 for every box — do not trust it alone.
          - Category string is the COCO name at the PPE model index:
            person→Hardhat, bicycle→Mask, …, bus→Person, truck→Safety Vest, …
          Priority:
            1. COCO harness strings (primary path)
            2. Keep known PPE labels already on the detection
            3. ``category_id`` / ``cls`` / ``class`` when present and not stuck-only
               via ``class_id`` (prefer those keys over ``class_id``)
            4. Numeric category field
    """
    ...

# From engine_session
def normalize_index_to_category(mapping: Optional[Dict[Any, Any]]) -> Dict[int, str]:
    """
    Coerce ``index_to_category`` keys to ``int`` (JSON uploads use string keys).
    
        Values are stripped: this is the other ingestion boundary for the deployment's
        ``class_index_map``, and a single trailing space in it (``"gun "``) once made a
        weapon app detect nothing at all, silently, because an unmapped class is ignored
        rather than rejected. See ``post_processing.utils.filter_utils`` for the same guard
        on the other path -- the two must agree or the bug just moves.
    """
    ...

# From engine_session
def resolve_camera_fields_from_stream_info(stream_info: Optional[Dict[str, Any]]) -> Dict[str, str]:
    """
    Resolve camera identity fields from the per-frame ``stream_info`` dict.
    
        Mirrors legacy ``AnalyticsPublisher`` / ``INCIDENT_MANAGER`` lookup paths
        so ``results-agg`` gets the human-readable ``camera_name``, not a duplicate
        of ``camera_id`` when the name lives under ``stream_config`` or nested
        ``input_streams``.
    """
    ...

# From engine_session
def resolve_location_for_publish(stream_info: Optional[Dict[str, Any]]) -> Dict[str, str]:
    """
    Resolve ``locationId`` and display ``location`` for Redis / results-agg envelopes.
    
        Mirrors the field lookup paths used for incidents (``camera_info``, ``stream_config``,
        enriched top-level ``stream_info``). Null Mongo ObjectIds are blanked; missing names
        fall back to ``Unknown Location``.
    """
    ...

# From flow
def load_manifest_index_to_category(manifest_name: str) -> Optional[Dict[int, str]]:
    """
    Return ``index_to_category`` from a bundled manifest, if present.
    """
    ...

# From flow
def resolve_manifest_for_app(app_name: Optional[str]) -> Optional[str]:
    """
    Return the new-flow manifest name for ``app_name``, or None for legacy.
    
        A non-None return is a bare manifest name guaranteed to exist under
        ``analytics/config/`` and loadable by ``AnalyticsEngine(manifest_name)``.
    """
    ...

# From geometry
def assign_detections_to_zones(detections: list[dict[str, Any]], zones_px: dict[str, Any.Any], use_foot_center: bool = False) -> dict[str, list[dict[str, Any]]]:
    """
    Partition detections into named zones by point-in-polygon containment.
    
        Each detection is assigned to the **first** zone whose polygon contains
        the detection's reference point.  Detections that fall in no zone are
        discarded.
    
        Args:
            detections: Raw detection dicts (with ``bounding_box`` / ``bbox``).
            zones_px: Mapping of zone name to polygon vertices as a numpy array
                of shape ``(N, 2)`` in **pixel** coordinates (``int32``).
            use_foot_center: Use bottom-center of bbox instead of center.
    
        Returns:
            Dict mapping ``zone_name`` to the list of detections whose reference
            point falls inside that zone.
    """
    ...

# From geometry
def build_zone_polygons_px(zones_normalized: dict[str, list[list[float]]], width: int, height: int) -> dict[str, Any.Any]:
    """
    Denormalize zone polygons and convert to numpy arrays for OpenCV.
    
        Args:
            zones_normalized: Zone name to list of ``[x_norm, y_norm]`` vertices.
            width: Frame width in pixels.
            height: Frame height in pixels.
    
        Returns:
            Dict mapping zone name to ``np.ndarray`` of shape ``(N, 1, 2)``
            with ``int32`` dtype (format expected by ``cv2.pointPolygonTest``).
    """
    ...

# From geometry
def create_counter_from_zone_config(zone_config_px: dict[str, Any], method: str = 'abline', in_direction: str = 'A_to_B', use_foot_center: bool = False, inner_polygon_offset: int = _DEFAULT_INNER_POLYGON_OFFSET) -> Union[Any, Any]:
    """
    Create a counting counter from a pixel-space zone_config.
    
        The ``method`` parameter selects which counter to build:
    
        * ``"abline"``: requires >= 2 lines in ``zone_config_px["lines"]``.
          The first two lines become ``line_a`` and ``line_b`` for ``ABLineCounter``.
        * ``"polygon"``: requires >= 1 zone in ``zone_config_px["zones"]``.
          First zone is ``outer_polygon``; second (if present) is ``inner_polygon``.
          When only one zone is provided, ``inner_polygon`` is auto-computed via
          ``polygon_offset_inward``.
    
        Args:
            zone_config_px: Dict with ``"lines"`` and/or ``"zones"`` in pixel coords.
            method: ``"abline"`` or ``"polygon"``.
            in_direction: For abline -- ``"A_to_B"`` or ``"B_to_A"``.
            use_foot_center: Use bottom-center of bbox instead of center.
            inner_polygon_offset: Pixel inset for auto-computed inner polygon.
    
        Returns:
            An ``ABLineCounter`` or ``PolygonCounter`` instance.
    
        Raises:
            ValueError: If required geometry is missing for the chosen method.
    """
    ...

# From geometry
def denormalize_zone_config(zone_config: dict[str, Any], width: int, height: int) -> dict[str, Any]:
    """
    Convert a zone_config from normalized (0-1) coords to integer pixel coords.
    
        Args:
            zone_config: Dict with ``"lines"`` and/or ``"zones"`` in normalized coords.
            width: Frame width in pixels.
            height: Frame height in pixels.
    
        Returns:
            Deep copy of zone_config with all coordinates converted to pixels.
    """
    ...

# From geometry
def get_detection_reference_point(detection: dict[str, Any], use_foot_center: bool = False) -> tuple[float, float] | None:
    """
    Extract the reference point (center or foot-center) from a detection.
    
        Args:
            detection: Dict with ``bounding_box`` or ``bbox`` key.
            use_foot_center: If ``True``, return the bottom-center of the bbox
                instead of the geometric center.
    
        Returns:
            ``(x, y)`` in the same coordinate space as the bounding box, or
            ``None`` if the bbox is missing / invalid.
    """
    ...

# From geometry
def point_in_polygon(point: tuple[float, float], polygon: Any.Any) -> bool:
    """
    Test whether *point* lies inside *polygon* using OpenCV.
    
        Args:
            point: ``(x, y)`` in pixel coordinates.
            polygon: Numpy array of shape ``(N, 2)`` with integer pixel vertices.
    
        Returns:
            ``True`` if the point is inside or on the edge of the polygon.
    """
    ...

# From quant_strategies
def compute_quant(detections: list[dict[str, Any]], config: Any) -> tuple[float, float]:
    """
    Compute ``(incident_quant, event_confidence)`` using the configured strategy.
    
        Falls back to ``max_confidence`` if the strategy name is not recognised.
    
        Args:
            detections: Filtered detection dicts for this frame.
            config: Strategy selection and parameters from the YAML manifest.
    
        Returns:
            ``(incident_quant, event_confidence)`` tuple.
    """
    ...

# Classes
# From analytics_publisher
class AnalyticsPublisher:
    # Publishes aggregated analytics to Redis (localhost) and Kafka internal streams.
    #
    # Monitors output queue and aggregates tracking statistics over 5-minute windows.
    # Publishes to 'results-agg' topic on both Redis and Kafka.
    #
    # Output structure (zone-keyed: tracking_stats maps zone_id -> stats; the old
    # non-zone-aware flow uses the single "global" zone):
    #     tracking_stats: {
    #         "global": {
    #             "input_timestamp": "2026-06-14T06:30:00Z",                  # RFC3339 UTC event time
    #             "current_counts": [{"category": "person", "count": 2}],         # NEW people in this publish window (delta)
    #             "total_current_counts": [{"category": "person", "count": 7}],   # ALL people in frame right now
    #             "total_counts": [{"category": "person", "count": 15}]           # Cumulative unique since reset
    #         }
    #     }

    def __init__(self: Any, camera_configs: Dict[str, Any], aggregation_interval: int = DEFAULT_AGGREGATION_INTERVAL, publish_interval: int = DEFAULT_PUBLISH_INTERVAL, app_deployment_id: Optional[str] = None, inference_pipeline_id: Optional[str] = None, deployment_instance_id: Optional[str] = None, app_id: Optional[str] = None, app_name: Optional[str] = None, app_version: Optional[str] = None, redis_host: str = 'localhost', redis_port: int = 6379, redis_password: Optional[str] = None, redis_username: Optional[str] = None, redis_db: int = 0, sentinel_hosts: Optional[List] = None, master_name: Optional[str] = None, kafka_bootstrap_servers: Optional[str] = None, enable_kafka: bool = False) -> None: ...

    ANALYTICS_TOPIC: str
    ANALYTICS_ZONE_GLOBAL: str
    DEFAULT_AGGREGATION_INTERVAL: int
    DEFAULT_PUBLISH_INTERVAL: int

    def enqueue_analytics_data(self: Any, task_data: Dict[str, Any]) -> None:
        """
        Enqueue analytics data from producer for processing.
        Called by ProducerWorker after sending messages.
        
        Args:
            task_data: Task data from output queue containing analytics info
        """
        ...

    def get_metrics(self: Any) -> Dict[str, Any]:
        """
        Get analytics publisher metrics.
        """
        ...

    def set_redis_config_provider(self: Any, provider: Callable[[], Optional[Dict[str, Any]]]) -> None:
        """
        Set a callback that provides fresh Redis connection config for retries.
        
                The provider should return a dict with keys:
                host, port, password, username, sentinel_hosts, master_name
        """
        ...

    def start(self: Any) -> Any.Any:
        """
        Start the analytics publisher in a separate thread.
        """
        ...

    def stop(self: Any) -> Any:
        """
        Stop the analytics publisher.
        """
        ...

    def update_camera_configs(self: Any, camera_configs: Dict[str, Any]) -> None:
        """
        Update camera configurations thread-safely.
        """
        ...


# From base_processor
class BaseMetricProcessor:
    # Abstract base for all category processors.
    #
    #     Subclasses must implement ``_compute_frame_metrics()`` and optionally
    #     override ``_compute_category_metrics()`` for aggregation-time extras.

    def __init__(self: Any, category: str, manifest_config: dict[str, Any]) -> None:
        """
        Initialize the processor with a category name and manifest config.
        
                Args:
                    category: The analytics category string (e.g. "VOLUME", "INCIDENT").
                    manifest_config: Full parsed manifest dict from the YAML config file.
        """
        ...

    def aggregate_1min(self: Any) -> Any:
        """
        Aggregate buffered frames into metrics and optional VOLUME ``tracking_stats``.
        
                Returns a processor chunk; ``AnalyticsEngine.aggregate`` merges chunks
                into the full publisher-shaped ``AggregationResult``.
        """
        ...

    def process_frame(self: Any, detections: list[dict[str, Any]], frame_ts: float, frame_id: str = '') -> Any:
        """
        Process a single frame of detections.
        
                Template method:
                  1. ``_pre_process``  — filter to target categories
                  2. ``_update_track_counts`` — update track-ID sets
                  3. ``_compute_frame_metrics`` — subclass hook (returns metrics)
                  4. Build ``ProcessorFrameOutput`` with business_analytics, human_text, etc.
        
                The engine is responsible for assembling the final ``FrameResult``
                envelope from outputs of all processors.
        """
        ...

    def reset(self: Any) -> None:
        """
        Full reset — clears all state including cumulative track IDs.
        """
        ...


# From engine
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


# From engine_session
class AnalyticsEngineSession:
    # One camera's AnalyticsEngine + tracker + publishing wiring.

    def __init__(self: Any, manifest_name: str, app_name: Optional[str], index_to_category: Optional[Dict[int, str]], publisher: Any, logger_: Optional[Any.Any] = None) -> None: ...

    def process(self: Any, detections: List[Dict[str, Any]], stream_info: Optional[Dict[str, Any]], stream_key: str = '') -> Dict[str, Any]:
        """
        Run one frame; return the per-frame zone-keyed agg_summary (or {}).
        """
        ...


# From incident_lifecycle
class IncidentLifecycle:
    # Per-camera incident lifecycle state machine.
    #
    #     Pure computation: no I/O.  Given a severity level for each frame it
    #     maintains per-camera state and emits :class:`IncidentEvent` instances
    #     when the confirmed severity level changes or an incident ends.
    #
    #     Args:
    #         config: Tunable consecutive-frame thresholds.

    def __init__(self: Any, config: Any | None = None) -> None:
        """
        Initialize with optional lifecycle configuration (defaults applied).
        """
        ...

    def get_all_states(self: Any) -> dict[str, Any]:
        """
        Return copies of all per-camera lifecycle states.
        """
        ...

    def get_state(self: Any, camera_id: str) -> Any | None:
        """
        Return a copy of the lifecycle state for a camera, or ``None``.
        """
        ...

    def process_frame(self: Any, camera_id: str, severity_level: Any, incident_quant: float, event_confidence: float, frame_ts: float, frame_id: str, incident_type: str) -> list[Any]:
        """
        Run one frame through the lifecycle for *camera_id*.
        
                Args:
                    camera_id: Unique camera identifier.
                    severity_level: Computed severity for this frame.
                    incident_quant: Quantitative incident measurement (0-100).
                    event_confidence: Maximum detection confidence (0-1).
                    frame_ts: Frame timestamp in seconds.
                    frame_id: Frame identifier string.
                    incident_type: Incident type key from the manifest.
        
                Returns:
                    List of ``IncidentEvent`` models emitted this frame (usually 0 or 1).
        """
        ...

    def reset(self: Any) -> None:
        """
        Clear all per-camera state.
        """
        ...

    def reset_camera(self: Any, camera_id: str) -> None:
        """
        Clear state for a single camera.
        """
        ...


# From redis_publisher
class AnalyticsRedisPublisher:
    # Lazy, per-process Redis publisher for incident_res + results-agg.

    def __init__(self: Any, config: Optional[Dict[str, Any]] = None) -> None: ...

    def publish_aggregation(self: Any, camera_id: str, payload: Dict[str, Any]) -> bool: ...

    def publish_incident(self: Any, camera_id: str, payload: Dict[str, Any]) -> bool: ...


# From schemas
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

# From schemas
class BoundingBox:
    # Bounding box coordinates.

    ...

# From schemas
class DetectionEntry:
    # Single detection within tracking_stats.

    ...

# From schemas
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

# From schemas
class FrameSummaryEntry:
    # Single entry within agg_summary (keyed by frame index).

    ...

# From schemas
class IncidentDetail:
    # Single incident entry within an :class:`IncidentMessage`.

    ...

# From schemas
class IncidentEvent:
    # Event emitted by ``IncidentProcessor`` when an incident state changes.
    #
    #     Produced by the lifecycle state machine and drained via
    #     ``drain_incident_events()``.

    ...

# From schemas
class IncidentFrameResult:
    # Return type for ``IncidentProcessor.process_frame()``.
    #
    #     Carries the per-frame incident state snapshot.  No metrics — incidents
    #     are event-driven, not aggregated.

    ...

# From schemas
class IncidentLifecycleState:
    # Per-camera mutable state managed by :class:`IncidentLifecycle`.
    #
    #     ``validate_assignment=True`` ensures Pydantic validates every field
    #     mutation, keeping the state machine honest.

    model_config: Any


# From schemas
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


# From schemas
class IncidentProcessorConfig:
    # Parsed and validated incident section from the YAML manifest.
    #
    #     Single source of truth for how the ``IncidentProcessor`` behaves.

    ...

# From schemas
class IncidentThreshold:
    # Single threshold level for incident severity calculation.

    ...

# From schemas
class IncidentTypeConfig:
    # Configuration for one incident type from the YAML manifest.

    ...

# From schemas
class InputStreamEntry:
    # Wrapper for input stream info.

    ...

# From schemas
class InputStreamInfo:
    # Metadata for an input stream.

    ...

# From schemas
class LifecycleConfig:
    # Configurable thresholds for the consecutive-frame validation.
    #
    #     Used by :class:`IncidentLifecycle`.

    ...

# From schemas
class MetricEntry:
    # Single metric in the standardized metrics[] output format.

    ...

# From schemas
class ProcessorAggregationOutput:
    # Per-category contribution to a 1-minute aggregation window.
    #
    #     Parallels :class:`ProcessorFrameOutput` on the frame path: each metric
    #     processor returns only its piece (aggregated ``metrics[]`` and, for VOLUME,
    #     ``tracking_stats``). :meth:`~matrice_analytics.analytics.engine.AnalyticsEngine.aggregate`
    #     merges all chunks with :class:`StreamInfo` into the full
    #     :class:`AggregationResult` message.

    ...

# From schemas
class ProcessorFrameOutput:
    # Raw per-frame output from a single category processor.
    #
    #     Carries the processor's computed metrics and display-ready fields
    #     without the nested result envelope.  The engine combines outputs
    #     from all processors into the final :class:`FrameResult`.

    ...

# From schemas
class QuantStrategyConfig:
    # Selects how ``incident_quant`` is computed from raw detections.

    ...

# From schemas
class ResultValue:
    # The value payload containing streams and analytics summary.

    ...

# From schemas
class ResultWrapper:
    # Top-level result wrapper.

    ...

# From schemas
class SeverityLevel:
    # Severity levels for the incident lifecycle state machine.

    critical: str
    info: str
    low: str
    medium: str
    none: str
    significant: str


# From schemas
class StreamInfo:
    # Per-stream context: camera, application, and geometry for analytics.
    #
    #     Combines fields present in aggregation summaries (camera/app identity),
    #     frame-level input stream metadata (e.g. ``original_fps`` from
    #     ``input_streams[].input_stream``), and optional ``zone_config`` (lines and
    #     zones only; counting options come from the manifest ``volume.counter``).

    model_config: Any


# From schemas
class TrackingStats:
    # Frame-level tracking statistics.
    #
    #     Lightweight structure embedded in each ``FrameSummaryEntry`` within
    #     ``agg_summary``.  Contains only the human-readable text and the
    #     per-frame detection list.

    ...

# From schemas
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


from . import analytics_publisher, base_processor, engine, engine_session, flow, geometry, incident_lifecycle, quant_strategies, redis_publisher, schemas