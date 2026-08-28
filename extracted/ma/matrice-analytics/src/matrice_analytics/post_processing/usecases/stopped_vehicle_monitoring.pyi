"""Auto-generated stub for module: stopped_vehicle_monitoring."""
from typing import Any, Dict, Optional

from ..Trackers import ConfigDrivenTracker, TrackerProfile
from ..core.base import BaseProcessor, ConfigProtocol, ProcessingContext, ProcessingResult
from ..core.config import AlertConfig, BaseConfig
from ..utils import BBoxSmoothingConfig, BBoxSmoothingTracker, apply_category_mapping, bbox_smoothing, count_objects_in_zones, filter_by_confidence, match_results_structure
from ..utils.geometry_utils import get_bbox_bottom25_center, get_bbox_center, point_in_polygon

# Classes
class StoppedVehicleMonitoringConfig:
    # Minimal configuration - only essential tunable parameters

    ...
class StoppedVehicleMonitoringUseCase:
    # Stopped vehicle detection use case.
    # Detects vehicles that have stopped for configurable duration.

    def __init__(self: Any) -> None: ...

    def get_total_counts(self: Any) -> Any:
        """
        Get total unique counts per category
        """
        ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any: ...

class StoppedVehicleTracker:
    # Per-track state for stopped vehicle detection.
    # Uses hybrid approach: displacement buffer for jitter + EWMA for drift.

    def __init__(self: Any, track_id: int, initial_bbox: Dict, timestamp: float, zone_name: Optional[str] = None) -> None: ...

    def get_stationary_duration(self: Any, current_time: float) -> float:
        """
        Get time since vehicle became stationary (seconds)
        """
        ...

    def update(self: Any, bbox: Dict, timestamp: float, zone_name: Optional[str] = None) -> bool:
        """
        Update track state and return True if vehicle is confirmed stopped.
        
        Algorithm:
        1. Update position buffer
        2. Update EWMA centroid
        3. Check short-term jitter (buffer analysis)
        4. Check long-term drift (EWMA analysis)
        5. Confirm stopped state if both conditions met
        """
        ...

