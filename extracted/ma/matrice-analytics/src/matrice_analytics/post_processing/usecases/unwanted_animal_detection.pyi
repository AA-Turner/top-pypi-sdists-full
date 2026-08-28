"""Auto-generated stub for module: unwanted_animal_detection."""
from typing import Any, Dict, List, Optional

from ..core.base import BaseProcessor, ConfigProtocol, ProcessingContext, ProcessingResult
from ..core.config import AlertConfig, BaseConfig
from ..utils import apply_category_mapping, filter_by_confidence, match_results_structure
from ..utils.incident_manager_utils import INCIDENT_MANAGER, IncidentManagerFactory

# Classes
class UnwantedAnimalDetectionConfig:
    # Configuration for the unwanted animal detection use case.

    def validate(self: Any) -> List[str]: ...

class UnwantedAnimalDetectionUseCase:
    def __init__(self: Any) -> None: ...

    CATEGORY_DISPLAY: Dict[Any, Any]

    def create_default_config(self: Any, **overrides: Any) -> Any: ...

    def get_config_schema(self: Any) -> Dict[str, Any]: ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any: ...

