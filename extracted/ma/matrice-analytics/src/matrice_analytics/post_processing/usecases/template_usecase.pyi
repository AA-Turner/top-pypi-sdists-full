"""Auto-generated stub for module: template_usecase."""
from typing import Any, Dict, List, Optional

from ..core.base import BaseProcessor, ConfigProtocol, ProcessingContext, ProcessingResult
from ..core.config import BaseConfig
from ..utils import apply_category_mapping

# Classes
class TemplateUseCase:
    # Template use case showing how to implement standardized agg_summary structure.

    def __init__(self: Any) -> None:
        """
        Initialize template use case.
        """
        ...

    def create_default_config(self: Any, **overrides: Any) -> Any:
        """
        Create default configuration with optional overrides.
        """
        ...

    def get_config_schema(self: Any) -> Dict[str, Any]:
        """
        Get configuration schema for template use case.
        """
        ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Any] = None) -> Any:
        """
        Process data using template use case - automatically detects single or multi-frame structure.
        
        Args:
            data: Raw model output (detection or tracking format)
            config: Template use case configuration
            context: Processing context
            stream_info: Stream information (optional)
        
        Returns:
            ProcessingResult: Processing result with standardized agg_summary structure
        """
        ...

class TemplateUseCaseConfig:
    # Configuration for Template Use Case.

    def __init__(self: Any, usecase: str = 'template_usecase', category: str = 'general', confidence_threshold: float = 0.5, target_categories: List[str] = None, enable_analytics: bool = True, alert_threshold: int = 5, **kwargs: Any) -> None: ...

    def validate(self: Any) -> List[str]:
        """
        Validate configuration.
        """
        ...

