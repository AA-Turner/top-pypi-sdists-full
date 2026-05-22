"""Auto-generated stub for module: loitering_detection."""
from typing import Any, Dict, List, Optional

from ..core.base import BaseProcessor, ConfigProtocol, ProcessingContext, ProcessingResult
from ..core.config import AlertConfig, BaseConfig
from ..utils import BBoxSmoothingTracker, ByteTrackWrapper, SORTTracker, apply_category_mapping, bbox_centroid, bbox_feet_point, bbox_iou, dist, filter_by_confidence, match_results_structure, smooth_point

# Classes
class LoiteringConfig:
    def validate(self: Any) -> List[str]: ...

class LoiteringUseCase:
    def __init__(self: Any) -> None: ...

    GLOBAL_ZONE_NAME: str

    def get_total_counts(self: Any) -> Dict[str, int]:
        """
        Return total unique track_id counts per category.
        """
        ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any: ...

