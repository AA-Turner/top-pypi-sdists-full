"""Auto-generated stub for module: age_gender_detection."""
from typing import Any, Dict, List, Optional

# Constants
AVG_AGE: int
MAX_AGE: int
MIN_AGE: int

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

# Classes
class AgeGenderConfig:
    # Configuration for age and gender detection use case in age and gender detection.

    def validate(self: Any) -> List[str]:
        """
        Validate configuration parameters.
        """
        ...

class AgeGenderUseCase:
    def __init__(self: Any) -> None: ...

    def get_total_counts(self: Any) -> Any:
        """
        Return total unique age-gender encountered so far.
        """
        ...

    def process(self: Any, data: Any, config: Any, input_bytes: Optional[Any] = None, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any: ...

    def reset_all_tracking(self: Any) -> None:
        """
        Reset both advanced tracker and plate tracking state.
        """
        ...

    def reset_plate_tracking(self: Any) -> None:
        """
        Reset plate tracking state.
        """
        ...

    def reset_tracker(self: Any) -> None:
        """
        Reset the advanced tracker instance.
        """
        ...

