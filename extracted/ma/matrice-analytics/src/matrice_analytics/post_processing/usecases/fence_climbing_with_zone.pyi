"""Auto-generated stub for module: fence_climbing_with_zone."""
from typing import Any, Dict, List, Optional

from ..core.base import BaseProcessor, ConfigProtocol, ProcessingContext, ProcessingResult
from ..core.config import AlertConfig, BaseConfig
from ..utils import apply_category_mapping
from ..utils.geometry_utils import point_in_polygon

# Classes
class FenceClimbingWithZoneConfig:
    # Configuration for `fence_climbing_with_zone`.
    #
    #     Attributes:
    #         zone_polygon: Polygon vertices in image pixel coordinates as a list
    #             of [x, y] pairs. Format matches `point_in_polygon`. Must have
    #             at least 3 vertices.
    #         confidence_threshold: Minimum YOLO detection score to consider.
    #         target_categories: Keep only detections whose `category` is in this
    #             list (lower-cased). Defaults to ``["person"]``.
    #         index_to_category: Optional class-index -> name map (YOLO classes).
    #         alert_config: Optional alert channel/threshold configuration.

    def validate(self: Any) -> List[str]: ...

class FenceClimbingWithZoneUseCase:
    # Per-detection in-zone check.
    #
    #     For each YOLO detection that survives the confidence + category filters,
    #     test whether the bbox's bottom-center sits inside ``config.zone_polygon``.
    #     Every match emits one alert and one incident.

    def __init__(self: Any) -> None: ...

    def create_default_config(self: Any, **overrides: Any) -> Any: ...

    def get_config_schema(self: Any) -> Dict[str, Any]: ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any: ...

