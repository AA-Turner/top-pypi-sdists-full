"""Auto-generated stub for module: crowdflow."""
from typing import Any, Dict, List, Optional

from ..Trackers import ConfigDrivenTracker, TrackerProfile
from ..core.base import BaseProcessor, ConfigProtocol, ProcessingContext, ProcessingResult
from ..core.config import AlertConfig, BaseConfig, ZoneConfig
from ..utils import apply_category_mapping, filter_by_confidence, match_results_structure
from ..utils.geometry_utils import point_in_polygon

# Classes
class CrowdflowConfig:
    # Configuration for footfall use case.

    def validate(self: Any) -> List[str]:
        """
        Validate people counting configuration.
        """
        ...

class CrowdflowUseCase:
    def __init__(self: Any) -> None: ...

    def get_total_counts(self: Any) -> Any: ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any: ...

class TrajectoryCorrector:
    # Handles Velocity-Fusion logic to correct model orientation errors.
    # Stores history of track centers and applies EMA smoothing.

    def __init__(self: Any) -> None: ...

    def get_direction_label(self: Any, angle: Any) -> Any:
        """
        Your custom logic for Front/Back/Left/Right
        """
        ...

    def update_and_get_label(self: Any, track_id: Any, center: Any, raw_angle_deg: Any) -> Any:
        """
        1. Fixes Angle (+90)
        2. Calculates Velocity
        3. Applies EMA Smoothing
        4. Returns (Smooth_Angle, Label_String)
        """
        ...

