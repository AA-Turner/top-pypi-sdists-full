"""Auto-generated stub for module: phone_screen_defect_detection."""
from typing import Any, Dict, List, Optional, Tuple

from ..Trackers import ConfigDrivenTracker, TrackerProfile
from ..core.base import BaseProcessor, ConfigProtocol, ProcessingContext, ProcessingResult
from ..core.config import AlertConfig, BaseConfig
from ..utils import apply_category_mapping, filter_by_categories, filter_by_confidence, match_results_structure
from ..utils.incident_manager_utils import INCIDENT_MANAGER, IncidentManagerFactory

# Constants
logger: Any

# Classes
class PhoneScreenDefectDetectionConfig:
    # Configuration for the Phone Screen Defect Detection use case.

    def __init__(self: Any, usecase: str = 'phone_screen_defect_detection', category: str = 'industrial', confidence_threshold: float = 0.4, target_categories: Optional[List[str]] = None, enable_bbox_merge: bool = True, merge_iou_threshold: float = 0.4, containment_threshold: float = 0.7, enable_tracking: bool = True, enable_analytics: bool = True, alert_cooldown_seconds: int = 60, alert_config: Optional[Any] = None, index_to_category: Optional[Dict[int, str]] = None, **kwargs: Any) -> None: ...

    def validate(self: Any) -> Any: ...

class PhoneScreenDefectDetectionUseCase:
    # Screen inspection: defective units per window, plus defect presence time.

    def __init__(self: Any) -> None: ...

    CATEGORY_DISPLAY: Dict[Any, Any]
    CATEGORY_NORMALIZE: Dict[Any, Any]
    DEFECT_CATEGORIES: Tuple[Any, ...]
    INSPECTION_CATEGORIES: Tuple[Any, ...]

    def get_new_counts_this_frame(self: Any) -> Dict[str, int]:
        """
        Track_ids seen for the FIRST time this frame, per category.
        """
        ...

    def get_total_counts(self: Any) -> Dict[str, int]:
        """
        Cumulative UNIQUE track_id count per category.
        """
        ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Any] = None) -> Any: ...

    def reset_state(self: Any) -> Any: ...

