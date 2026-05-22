"""Auto-generated stub for module: tailgating_detection."""
from typing import Any, Dict, List, Optional, Set

from ..core.base import BaseProcessor, ConfigProtocol, ProcessingContext, ProcessingResult
from ..core.config import AlertConfig, BaseConfig, ZoneConfig
from ..utils import filter_by_confidence, get_bbox_bottom25_center, match_results_structure
from ..utils.tailgating_utils import AccessEventManager, CrossingRecord, DoorRuntime, analyze_passage, compute_entry_normal, detect_crossing, signed_distance
from .hazard_zone_entry import PostProcessingConfigClient
from .hazard_zone_entry import PostProcessingConfigClient

# Constants
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
    # Tailgating post-processing configuration.
    #
    #     **Zones** are **required**: supply ``zones`` at the top level and/or under
    #     ``extra_params["zones"]`` (same shape). Top-level ``zones`` overrides
    #     ``extra_params`` on duplicate door ids.
    #
    #     **Matrice UI / API geometry**: When ``stream_info`` is present and
    #     ``PostProcessingConfigClient`` can reach the deployment post-processing
    #     config (env credentials or ``stream_info["config_client"]`` or
    #     ``TailgatingDetectionUseCase.set_config_client``), door geometry for one
    #     door is merged on the first frame. Expected keys in the camera
    #     ``zone_config`` (after denormalization) are ``lines["access_line"]`` or
    #     ``zones["access_line"]`` (two points), ``zones["secured_zone"]`` (polygon),
    #     and optionally ``zones["access_buffer_zone"]``. Use
    #     ``stream_info["tailgating_door_id"]`` to choose which door id to update when
    #     several doors exist; if exactly one door is configured, that id is used.
    #     For local file / bench runs without deployment context, set
    #     ``stream_info["skip_tailgating_api_zones"]`` to true to skip Matrice API
    #     resolution entirely (avoids opening a session when credentials exist).
    #
    #     **Output labeling**: In each frame, ``tracking_stats.detections`` may use
    #     ``category: "tailgating_person"`` for any detection whose ``track_id`` is
    #     listed in that frame’s tailgating analysis ``suspected_tailgaters``; others
    #     remain ``"person"``. Counts in ``total_counts`` / ``current_counts`` match
    #     those categories.
    #
    #     **Timing and geometry tuning** in ``extra_params`` (``access_window_sec``,
    #     ``silence_timeout_sec``, ``cooldown_sec``, ``allowed_persons_per_event``,
    #     ``max_follow_time_delta_sec``, ``min_motion_magnitude``,
    #     ``line_intersection_tolerance``, ``enable_direction_validation``,
    #     ``cross_memory_frames``) are merged onto this config and removed from
    #     ``extra_params`` so they take effect in production payloads that nest them.

    def __init__(self: Any, usecase: str = 'tailgating_detection', category: str = 'security', confidence_threshold: float = 0.5, target_categories: Optional[List[str]] = None, zones: Optional[Dict[str, Any]] = None, access_window_sec: float = 5.0, silence_timeout_sec: float = 2.0, cooldown_sec: float = 4.0, allowed_persons_per_event: int = 1, max_follow_time_delta_sec: float = 3.0, min_motion_magnitude: float = 0.002, line_intersection_tolerance: float = 0.02, enable_direction_validation: bool = False, cross_memory_frames: int = 0, alert_config: Optional[Any] = None, **kwargs: Any) -> None: ...

    EXTRA_PARAM_KEYS: Any

    def merge_zones_sources(top_level: Optional[Dict[str, Any]], from_extra: Any) -> Dict[str, Any]:
        """
        Merge zone maps; top-level ``zones`` wins on duplicate door ids.
        """
        ...

    def normalize_zones_mapping(raw: Any) -> Dict[str, Any]:
        """
        Coerce door_id -> ZoneConfig from ZoneConfig instances or nested dicts.
        """
        ...

    def validate(self: Any) -> Any: ...

    def validate_door_geometry(door_id: str, zone_cfg: Any) -> None: ...

    def validate_zone_point(label: str, pt: Any, door_id: str) -> None: ...

class TailgatingDetectionUseCase:
    def __init__(self: Any) -> None: ...

    def create_default_config(self: Any, **overrides: Any) -> Any: ...

    def draw_config_zones_on_frame(self: Any, frame: Any, config: Any) -> None:
        """
        Draw all doors in *config* onto *frame*.
        """
        ...

    def draw_zones_on_frame(self: Any, frame: Any, zone_cfg: Any) -> None:
        """
        Draw secured zone, optional access buffer zone, and access (intersection) line on
        *frame* in place. *frame* is BGR; zone points are normalized [0, 1].
        
        Requires ``opencv-python`` and ``numpy``.
        """
        ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Any] = None) -> Any: ...

    def set_config_client(self: Any, client: Optional[Any]) -> None:
        """
        Set client used to resolve door geometry from deployment post-processing config.
        """
        ...

