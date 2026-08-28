"""Auto-generated stub for module: pipe_corrosion_detection."""
from typing import Any, Dict, List, Optional

from ..Trackers import ConfigDrivenTracker, TrackerProfile
from ..core.base import BaseProcessor, ConfigProtocol, ProcessingContext, ProcessingResult
from ..core.config import AlertConfig, BaseConfig
from ..utils import apply_category_mapping, filter_by_categories, filter_by_confidence, match_results_structure
from ..utils.incident_manager_utils import INCIDENT_MANAGER, IncidentManagerFactory

# Constants
logger: Any

# Classes
class PipeCorrosionDetectionConfig:
    # Configuration for Pipe Corrosion Detection Use Case.
    #
    # Includes:
    # - Confidence filtering
    # - Spatial merge thresholds
    # - Temporal validation parameters
    # - Alert cooldown settings

    def __init__(self: Any, usecase: str = 'pipe_corrosion_detection', category: str = 'industrial', confidence_threshold: float = 0.25, target_categories: Optional[List[str]] = None, enable_spatial_merge: bool = True, iou_merge_threshold: float = 0.3, containment_threshold: float = 0.5, activation_frames: int = 10, deactivation_frames: int = 10, alert_cooldown_seconds: int = 30, enable_analytics: bool = True, index_to_category: Optional[Dict[int, str]] = None, alert_config: Optional[Any] = None, **kwargs: Any) -> None: ...

    def validate(self: Any) -> List[str]: ...

class PipeCorrosionDetectionUseCase:
    def __init__(self: Any) -> None: ...

    def get_total_counts(self: Any) -> Dict[str, int]: ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Any] = None) -> Any: ...

    def reset_state(self: Any) -> Any: ...

