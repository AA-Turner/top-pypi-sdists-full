"""Auto-generated stub for module: heatmaps."""
from typing import Any, Dict, List, Optional

from ..advanced_tracker import AdvancedTracker
from ..advanced_tracker.config import TrackerConfig
from ..core.base import BaseProcessor, ConfigProtocol, ProcessingContext, ProcessingResult
from ..core.config import AlertConfig, BaseConfig, ZoneConfig
from ..utils import apply_category_mapping, filter_by_confidence, match_results_structure
from ..utils.geometry_utils import point_in_polygon

# Classes
class HeatMapsConfig:
    # Configuration for heatmaps use case.

    def validate(self: Any) -> List[str]: ...

class HeatMapsUseCase:
    def __init__(self: Any) -> None: ...

    INCIDENT_STILL_ACTIVE: str

    def get_total_counts(self: Any) -> Any: ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any: ...

