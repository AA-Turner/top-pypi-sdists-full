"""Auto-generated stub for module: deep_oc_sort."""
from typing import Any, Dict, List, Optional

from ..Trackers.integration import ConfigDrivenTracker
from ..core.base import BaseProcessor, ConfigProtocol, ProcessingContext, ProcessingResult
from ..core.config import AlertConfig, BaseConfig
from ..utils import apply_category_mapping, filter_by_confidence, match_results_structure

# Classes
class DeepOCSortConfig:
    # Configuration for DeepOCSORT-based people counting.

    def validate(self: Any) -> List[str]: ...

class DeepOCSortUseCase:
    def __init__(self: Any) -> None: ...

    def create_default_config(self: Any, **overrides: Any) -> Any: ...

    def get_config_schema(self: Any) -> Dict[str, Any]: ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any: ...

