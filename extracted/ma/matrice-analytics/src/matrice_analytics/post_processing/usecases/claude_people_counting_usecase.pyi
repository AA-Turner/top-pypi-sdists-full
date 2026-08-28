"""Auto-generated stub for module: claude_people_counting_usecase."""
from typing import Any, Dict, List, Optional

from ..core.base import BaseProcessor, ConfigProtocol, ProcessingContext, ProcessingResult
from ..core.config import AlertConfig, BaseConfig
from ..utils import apply_category_mapping, filter_by_confidence

# Classes
class ClaudePeopleCountingUsecaseConfig:
    def __init__(self: Any, usecase: str = 'claude_people_counting_usecase', category: str = 'general', confidence_threshold: float = 0.4, target_categories: Optional[List[str]] = None, enable_analytics: bool = True, enable_tracking: bool = True, enable_unique_counting: bool = True, index_to_category: Optional[Dict[int, str]] = None, alert_config: Optional[Any] = None, **kwargs: Any) -> None: ...

    def validate(self: Any) -> List[str]: ...

class ClaudePeopleCountingUsecaseUseCase:
    def __init__(self: Any) -> None: ...

    def create_default_config(self: Any, **overrides: Any) -> 'Any': ...

    def get_config_schema(self: Any) -> Dict[str, Any]: ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any: ...

