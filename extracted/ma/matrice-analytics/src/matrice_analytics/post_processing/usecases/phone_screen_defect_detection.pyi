"""Auto-generated stub for module: phone_screen_defect_detection."""
from typing import Any, Dict, List, Optional

from ..core.base import BaseProcessor, ConfigProtocol, ProcessingContext, ProcessingResult
from ..core.config import AlertConfig, BaseConfig
from ..utils import apply_category_mapping, filter_by_categories, filter_by_confidence, match_results_structure

# Classes
class PhoneScreenDefectDetectionConfig:
    def __init__(self: Any, usecase: str = 'phone_screen_defect_detection', category: str = 'industrial', confidence_threshold: float = 0.4, target_categories: Optional[List[str]] = None, enable_bbox_merge: bool = True, merge_iou_threshold: float = 0.4, containment_threshold: float = 0.7, enable_tracking: bool = True, alert_config: Optional[Any] = None, index_to_category: Optional[Dict[int, str]] = None, **kwargs: Any) -> None: ...

    def validate(self: Any) -> Any: ...

class PhoneScreenDefectDetectionUseCase:
    def __init__(self: Any) -> None: ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Any] = None) -> Any: ...

