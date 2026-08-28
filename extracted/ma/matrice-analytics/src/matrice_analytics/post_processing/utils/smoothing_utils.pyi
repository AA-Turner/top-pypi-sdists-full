"""Auto-generated stub for module: smoothing_utils."""
from typing import Any, Dict, List, Optional, Union

# Constants
logger: Any

# Functions
def bbox_smoothing(detections: Union[List[Dict], Dict[str, List[Dict]]], config: Any, tracker: Optional[Any] = None) -> Union[List[Dict], Dict[str, List[Dict]]]:
    """
    Apply smoothing algorithm to bbox detections.
    
    Args:
        detections: Either:
                   - List of detection dictionaries (detection format)
                   - Dict with frame keys containing lists of detections (tracking format)
        config: Smoothing configuration
        tracker: Optional tracker instance for persistent state across frames
    
    Returns:
        Same format as input: List[Dict] or Dict[str, List[Dict]]
    """
    ...
def create_bbox_smoothing_tracker(config: Any) -> Any:
    """
    Create a new bbox smoothing tracker instance.
    
    Args:
        config: Smoothing configuration
    
    Returns:
        BBoxSmoothingTracker: New tracker instance
    """
    ...
def create_default_smoothing_config(**overrides: Any) -> Any:
    """
    Create default smoothing configuration with optional overrides.
    
    Args:
        **overrides: Configuration overrides
    
    Returns:
        BBoxSmoothingConfig: Configuration instance
    """
    ...

# Classes
class BBoxSmoothingConfig:
    # Configuration for bbox smoothing algorithms.

    ...
class BBoxSmoothingTracker:
    # Tracks individual objects for smoothing across frames.

    def __init__(self: Any, config: Any) -> None: ...

    def get_stats(self: Any) -> Dict[str, Any]:
        """
        Get tracker statistics.
        """
        ...

    def reset(self: Any) -> Any:
        """
        Reset tracker state.
        """
        ...

