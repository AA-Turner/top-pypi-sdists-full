"""Auto-generated stub for module: factory."""
from typing import Any, Optional

from .advanced_tracker import AdvancedTrackerAdapter
from .base import BaseObjectTracker
from .bytetrack import ByteTrackAdapter
from .config import SUPPORTED_TRACKING_METHODS, MatriceTrackerConfig
from .deep_oc_sort import DeepOCSortAdapter
from .sort import SORTTrackerAdapter

# Constants
logger: Any

# Functions
def create_tracker(method: str, config: Optional[Any] = None, namespace: Optional[str] = None) -> Any:
    """
    Factory for post-processing trackers.
    
    Args:
        method: ``advanced`` | ``sort`` | ``bytetrack`` | ``deep_oc_sort``. ``oc_sort`` /
            ``deepsort`` / ``botsort`` are accepted (see ``SUPPORTED_TRACKING_METHODS``)
            but normalize to ``advanced`` -- their adapters were deleted (F10b step S3).
        config: Unified tracker configuration
        namespace: Optional stream namespace for ID isolation (advanced tracker)
    
    Returns:
        BaseObjectTracker instance
    """
    ...
def normalize_tracking_method(method: str) -> str: ...
