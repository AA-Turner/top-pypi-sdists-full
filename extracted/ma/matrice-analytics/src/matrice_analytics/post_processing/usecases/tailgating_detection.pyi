"""Auto-generated stub for module: tailgating_detection."""
from typing import Any, Dict, List, Optional, Set, Tuple

from ..Trackers import ConfigDrivenTracker, TrackerProfile, legacy_sort_tracker_overrides
from ..core.base import BaseProcessor, ConfigProtocol, ProcessingContext, ProcessingResult
from ..core.config import AlertConfig, BaseConfig, ZoneConfig
from ..utils import ByteTrackWrapper, SORTTracker, filter_by_confidence, get_bbox_bottom25_center, match_results_structure
from ..utils.geometry_utils import calculate_iou, get_bbox_bottom_center, point_in_polygon
from ..utils.incident_manager_utils import INCIDENT_MANAGER, IncidentManagerFactory
from ..utils.tailgating_utils import AccessEventManager, AccessPointState, CrossingRecord, analyze_passage, build_side_zone_map, detect_crossing
from .hazard_zone_entry import PostProcessingConfigClient
from .hazard_zone_entry import PostProcessingConfigClient

# Constants
TAILGATING_OUTPUT_CLASS_IDS: Dict[Any, Any]
TAILGATING_SEVERITY: str
logger: Any

# Functions
def lift_ai_camera_zones_into_post_processing(doc: Dict[str, Any]) -> Dict[str, Any]:
    """
    Fold AI-style payloads into ``postProcessing`` (same contract as overcrowding).
    
        Matrice UI / exports may place ``zone_config`` under a top-level camera id key;
        this merges those into ``postProcessing`` without overwriting existing keys.
    """
    ...

# Classes
class TailgatingConfig:
    # Tailgating post-processing configuration (door-agnostic, bidirectional).
    #
    #     **Geometry** is **two shared zones** plus **one or more access lines**:
    #
    #     - ``zones``: exactly **two** polygons (e.g. ``{"zone_1": [...], "zone_2": [...]}``).
    #       They are shared by every access line. For any single passage the
    #       *destination* zone is treated as the secured zone and the *origin* zone as
    #       the access/buffer zone — the roles flip with direction.
    #     - ``access_lines``: a mapping ``{access_line_id: [p1, p2]}`` with at least one
    #       entry. Each access line is an independent access point (door / turnstile)
    #       with its own per-direction tailgating state.
    #
    #     Both may also be supplied via ``extra_params`` (``extra_params["zones"]`` /
    #     ``extra_params["access_lines"]``); top-level values win on duplicate keys.
    #
    #     **Bidirectional detection**: a crossing is detected in either direction. The
    #     detector anchors on the last *clear* side of a line and fires when the foot
    #     reaches the opposite clear side, so an arbitrary gap between the zone polygons
    #     and the line (where the foot is momentarily inside neither zone) does not break
    #     detection. Tailgating windows are keyed by ``(access_line_id, direction)`` so
    #     opposite-direction passages never interfere.
    #
    #     **Matrice UI / API geometry**: When ``stream_info`` is present and
    #     ``PostProcessingConfigClient`` can reach the deployment post-processing config,
    #     geometry is merged on the first frame. The camera ``zone_config`` (after
    #     denormalization) must contain ``zones`` (two polygons) and ``lines`` (one or
    #     more two-point lines). For local / bench runs set
    #     ``stream_info["skip_tailgating_api_zones"]`` to true to skip API resolution.
    #
    #     **Output labeling**: ``tracking_stats.detections`` use
    #     ``category: "tailgating_person"`` (``class_id: 1``) for any detection whose
    #     ``track_id`` is a suspect from an active incident still present in live
    #     detections; others remain ``"person"`` (``class_id: 0``).
    #
    #     **Incidents / alerts**: keyed by ``(access_line_id, direction)``. An incident
    #     opens immediately on the crossing frame whose passage analysis flags
    #     suspect(s) and persists while any suspect ``track_id`` remains visible. Alerts
    #     fire on the crossing frame for new suspects (per-line alert cooldown).
    #
    #     **Internal tracking** (same contract as ``loitering_detection``): when
    #     ``enable_tracking`` is True, a per-stream SORT (default) or ByteTrack wrapper
    #     assigns stable integer ``track_id`` values before crossing logic runs.
    #
    #     **Per-line tuning** via ``zone_params`` (``{access_line_id: {...overrides}}``):
    #     ``allowed_persons_per_event``, ``access_window_sec``, ``silence_timeout_sec``,
    #     ``cooldown_sec``, ``max_follow_time_delta_sec``. Absent keys fall back to the
    #     global defaults.

    def __init__(self: Any, usecase: str = 'tailgating_detection', category: str = 'security', confidence_threshold: float = 0.5, target_categories: Optional[List[str]] = None, zones: Optional[Dict[str, List[List[float]]]] = None, access_lines: Optional[Dict[str, List[List[float]]]] = None, zone_config: Optional[Dict[str, Any]] = None, zone_params: Optional[Dict[str, Dict[str, Any]]] = None, access_window_sec: float = 5.0, silence_timeout_sec: float = 2.0, cooldown_sec: float = 4.0, allowed_persons_per_event: int = 1, max_follow_time_delta_sec: float = 3.0, min_motion_magnitude: float = 2.0, side_margin: float = 5.0, line_endpoint_padding: float = 0.0, cross_memory_frames: int = 0, tracking_method: str = 'sort', tracking_max_age: int = 30, tracking_min_hits: int = 2, tracking_iou_threshold: float = 0.25, bytetrack_track_thresh: float = 0.25, bytetrack_match_thresh: float = 0.8, alert_config: Optional[Any] = None, **kwargs: Any) -> None: ...

    EXTRA_PARAM_KEYS: Any

    def normalize_access_lines(raw: Any) -> Dict[str, List[List[float]]]:
        """
        Coerce access lines to ``{access_line_id: [p1, p2]}``.
        """
        ...

    def normalize_zone_polygons(raw: Any) -> Dict[str, List[List[float]]]:
        """
        Coerce shared zones to ``{name: polygon}`` from a dict or a ``ZoneConfig``.
        """
        ...

    def validate(self: Any) -> Any: ...

    def zones_lines_from_zone_config(zone_config: Any) -> Tuple[Dict[str, List[List[float]]], Dict[str, List[List[float]]]]:
        """
        Split a Matrice/UI ``zone_config`` into ``(zones, access_lines)``.
        
                Expected shape: ``{"zones": {zone_name: polygon, ...},
                "lines": {line_name: [p1, p2], ...}}`` (pixel coordinates).
        """
        ...

class TailgatingDetectionUseCase:
    def __init__(self: Any) -> None: ...

    def create_default_config(self: Any, **overrides: Any) -> Any: ...

    def draw_config_zones_on_frame(self: Any, frame: Any, config: Any) -> None:
        """
        Draw the two shared zones and every access line on *frame* in place.
        
                *frame* is BGR; geometry points may be pixel or normalized (auto-detected).
                Requires ``opencv-python`` and ``numpy``.
        """
        ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Any] = None) -> Any: ...

    def set_config_client(self: Any, client: Optional[Any]) -> None:
        """
        Set client used to resolve zone/line geometry from deployment post-processing config.
        """
        ...

