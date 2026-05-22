"""Auto-generated stub for module: suspicious_activity_detection."""
from typing import Any, Dict, Optional

from ..advanced_tracker import AdvancedTracker
from ..advanced_tracker.config import TrackerConfig
from ..core.base import BaseProcessor, ConfigProtocol, ProcessingContext, ProcessingResult
from ..core.config import AlertConfig, BaseConfig
from ..utils import BBoxSmoothingConfig, BBoxSmoothingTracker, bbox_smoothing, filter_by_confidence, match_results_structure

# Functions
def apply_category_mapping(results: Any, index_to_category: Dict[str, str]) -> Any:
    """
    Apply category index to name mapping.
    
    Args:
        results: Detection or tracking results
        index_to_category: Mapping from category index to category name
    
    Returns:
        Results with mapped category names
    """
    ...
def load_model_from_checkpoint(checkpoint_path: Any, local_path: Any) -> Any:
    """
    Load a model from checkpoint URL
    """
    ...

# Classes
class SusActivityConfig:
    # Configuration for PCB Defect Detection use case.

    ...
class SusActivityUseCase:
    def __init__(self: Any) -> None: ...

    def get_total_counts(self: Any) -> Any:
        """
        Return total unique track_id count for each category.
        """
        ...

    def helper(self: Any, data: Any, config: Any) -> Any: ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any:
        """
        Main entry point for  post-processing.
        Applies category mapping, smoothing, counting, alerting, and summary generation.
        Returns a ProcessingResult with all relevant outputs.
        """
        ...

