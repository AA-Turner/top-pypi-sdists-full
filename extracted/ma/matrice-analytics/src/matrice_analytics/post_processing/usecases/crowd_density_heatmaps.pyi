"""Auto-generated stub for module: crowd_density_heatmaps."""
from typing import Any, Dict, Optional

from ..advanced_tracker import AdvancedTracker
from ..advanced_tracker.config import TrackerConfig
from ..core.base import BaseProcessor, ConfigProtocol, ProcessingContext, ProcessingResult
from ..core.config import AlertConfig, BaseConfig, ZoneConfig
from ..utils import apply_category_mapping, filter_by_confidence, match_results_structure
from ..utils.geometry_utils import point_in_polygon

# Classes
class CrowdDensityHeatMapsConfig:
    # Configuration for heatmaps use case.

    ...
class CrowdDensityHeatMapsUseCase:
    def __init__(self: Any) -> None: ...

    def get_total_counts(self: Any) -> Any: ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any: ...

