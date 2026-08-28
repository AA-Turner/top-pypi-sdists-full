"""Auto-generated stub for module: people_tracking_bkcp."""
from typing import Any, Dict, Optional, Set

from ..core.base import BaseProcessor, ConfigProtocol, ProcessingContext, ProcessingResult, ResultFormat
from ..core.config import LineConfig, PeopleTrackingConfig
from ..utils import BBoxSmoothingConfig, BBoxSmoothingTracker, apply_category_mapping, bbox_smoothing, calculate_iou, count_objects_in_zones, match_results_structure
from ..utils.geometry_utils import get_bbox_bottom25_center, point_in_polygon

# Classes
class PeopleTrackingUseCase:
    # People counting use case with zone analysis and alerting.

    def __init__(self: Any) -> None:
        """
        Initialize people counting use case.
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

    def clear_expired_tracks(self: Any, max_age_seconds: float = 300.0) -> int:
        """
        MANUAL USE ONLY: Clear current frame tracking data if no updates for a while.
        
          This method is NOT called automatically anywhere in the code.
        It's provided as a utility function for manual cleanup if needed.
        
        In streaming scenarios, you typically don't need to call this at all.
        The cumulative total should keep growing as new unique people are detected.
        
        This method only clears current frame tracking data while preserving
        the cumulative total count. The cumulative total should never decrease.
        
        Args:
            max_age_seconds: Maximum age in seconds before clearing current frame tracks
        
        Returns:
            Number of current frame tracks cleared
        """
        ...

    def create_default_config(self: Any, **overrides: Any) -> Any:
        """
        Create default configuration with optional overrides.
        """
        ...

    def get_all_zone_counts(self: Any) -> Dict[str, Dict[str, int]]:
        """
        Get current and total counts for all zones.
        """
        ...

    def get_config_schema(self: Any) -> Dict[str, Any]:
        """
        Get configuration schema for people counting.
        """
        ...

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

    def get_zone_current_count(self: Any, zone_name: str) -> int:
        """
        Get current count of people in a specific zone.
        """
        ...

    def get_zone_total_count(self: Any, zone_name: str) -> int:
        """
        Get total count of people who have been in a specific zone.
        """
        ...

    def get_zone_tracking_info(self: Any) -> Dict[str, Dict[str, Any]]:
        """
        Get detailed zone tracking information.
        """
        ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Any] = None) -> Any:
        """
        Process people counting use case - automatically detects single or multi-frame structure.
        
        Args:
            data: Raw model output (detection or tracking format)
            config: People counting configuration
            context: Processing context
            stream_info: Stream information containing frame details (optional)
        
        Returns:
            ProcessingResult: Processing result with standardized agg_summary structure
        """
        ...

    def reset_frame_counter(self: Any) -> None:
        """
        Reset only the frame counter.
        """
        ...

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

