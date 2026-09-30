"""Auto-generated stub for module: footfall."""
from typing import Any, Dict, List, Optional, Set

from ..Trackers import ConfigDrivenTracker, TrackerProfile
from ..core.base import BaseProcessor, ConfigProtocol, ProcessingContext, ProcessingResult
from ..core.config import AlertConfig, BaseConfig, LineConfig, ZoneConfig
from ..utils import BBoxSmoothingConfig, BBoxSmoothingTracker, apply_category_mapping, bbox_smoothing, calculate_iou, match_results_structure
from ..utils.counting_utils import PolygonCounter, VectorABLineCounter, parse_line_config, polygon_offset_inward
from ..utils.geometry_utils import get_bbox_bottom25_center, point_in_polygon
from ..utils.post_processing_config_client import PostProcessingConfigClient

# Classes
class FootFallConfig:
    # Configuration for Footfall use case (same schema as people tracking).

    def validate(self: Any) -> List[str]:
        """
        Validate people tracking configuration.
        
                Geometry (line_a, line_b, outer_polygon, inner_polygon) may be empty at load time
                when it will be resolved from API via stream_info + config_client in process().
                At use time (_get_or_create_counter), missing geometry raises if not resolved.
        """
        ...

class FootFallUseCase:
    # Footfall use case with polygon/abline counting, zone analysis and alerting (same logic as people tracking).

    def __init__(self: Any) -> None:
        """
        Initialize footfall use case.
        """
        ...

    def clear_current_frame_tracking(self: Any) -> int:
        """
        MANUAL USE ONLY: Clear only current frame tracking data while preserving cumulative totals.
        
         This method is NOT called automatically anywhere in the code.
        
        This is the SAFE method to use for manual clearing of stale/expired current frame data.
        The cumulative total (self._total_count) is always preserved.
        
        In streaming scenarios, you typically don't need to call this at all.
        
        Returns:
            Number of current frame tracks cleared
        """
        ...

    def clear_expired_tracks(self: Any, max_age_seconds: float = 300.0) -> int: ...

    def create_default_config(self: Any, **overrides: Any) -> Any: ...

    def get_all_zone_counts(self: Any) -> Dict[str, Dict[str, int]]: ...

    def get_config_schema(self: Any) -> Dict[str, Any]: ...

    def get_current_frame_count(self: Any) -> int:
        """
        Get the count of people in the current frame.
        """
        ...

    def get_frame_info(self: Any) -> Dict[str, Any]:
        """
        Get detailed information about frame processing and global frame offset.
        """
        ...

    def get_global_frame_id(self: Any, local_frame_id: str) -> str:
        """
        Convert local frame ID to global frame ID.
        """
        ...

    def get_global_frame_offset(self: Any) -> int:
        """
        Get the current global frame offset.
        """
        ...

    def get_total_count(self: Any) -> int:
        """
        Get the total count of unique people tracked across all calls.
        """
        ...

    def get_total_frames_processed(self: Any) -> int:
        """
        Get the total number of frames processed across all calls.
        """
        ...

    def get_track_ids_info(self: Any) -> Dict[str, Any]:
        """
        Get detailed information about track IDs.
        """
        ...

    def get_tracking_debug_info(self: Any) -> Dict[str, Any]:
        """
        Get detailed debugging information about tracking state.
        """
        ...

    def get_zone_current_count(self: Any, zone_name: str) -> int: ...

    def get_zone_total_count(self: Any, zone_name: str) -> int: ...

    def get_zone_tracking_info(self: Any) -> Dict[str, Dict[str, Any]]: ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any:
        """
        Process a single frame of detections and return agg_summary with in/out counts.
                Args:
                    data: Raw model output (detection or tracking format)
                    config: People counting configuration
                    context: Processing context
                    stream_info: Stream information containing frame details (optional)
        
                Returns:
                    ProcessingResult: Processing result with standardized agg_summary structure
        """
        ...

    def reset_frame_counter(self: Any) -> None: ...

    def reset_tracking_state(self: Any) -> None:
        """
        WARNING: This completely resets ALL tracking data including cumulative totals!
        
        This should ONLY be used when:
        - Starting a completely new tracking session
        - Switching to a different video/stream
        - Manual reset requested by user
        
        For clearing expired/stale tracks, use clear_current_frame_tracking() instead.
        """
        ...

    def set_config_client(self: Any, client: Optional[Any]) -> None:
        """
        Set the PostProcessingConfigClient used to resolve lines/zones from API (by_app_deployment, camera_id).
        """
        ...

    def set_global_frame_offset(self: Any, offset: int) -> None:
        """
        Set the global frame offset for video chunk processing.
        """
        ...

    def update_global_frame_offset(self: Any, frames_in_chunk: int) -> None:
        """
        Update global frame offset after processing a chunk.
        """
        ...

