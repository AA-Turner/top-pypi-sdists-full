"""Auto-generated stub for module: anti_spoofing_detection."""
from typing import Any, Dict, Optional

from ..advanced_tracker import AdvancedTracker
from ..advanced_tracker.config import TrackerConfig
from ..core.base import BaseProcessor, ConfigProtocol, ProcessingContext, ProcessingResult
from ..core.config import AlertConfig, BaseConfig
from ..utils import BBoxSmoothingConfig, BBoxSmoothingTracker, apply_category_mapping, bbox_smoothing, filter_by_confidence, match_results_structure

# Classes
class AntiSpoofingDetectionConfig:
    # Configuration for anti-spoofing detection use case.

    ...
class AntiSpoofingDetectionUseCase:
    def __init__(self: Any) -> None: ...

    CATEGORY_DISPLAY: Any

    def get_total_counts(self: Any) -> Any:
        """
        Return total unique track_id count for each category.
        """
        ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any: ...

