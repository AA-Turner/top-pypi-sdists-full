"""Auto-generated stub for module: agnostic_nms."""
from typing import Any, Dict, List, Optional

# Functions
def apply_nms(detections: List[Dict[str, Any]], iou_threshold: float = 0.45, class_agnostic: bool = True, min_box_size: float = 2.0, use_vectorized: bool = True) -> List[Dict[str, Any]]:
    """
    Convenience function for one-time NMS application.
    
    Args:
        detections: List of detection dicts
        iou_threshold: IoU threshold for suppression
        class_agnostic: If True, suppress across all classes
        min_box_size: Minimum box dimension in pixels
        use_vectorized: Use PyTorch implementation if available
    
    Returns:
        Filtered list of detections
    
    Example:
        >>> detections = [
        ...     {"category": "car", "confidence": 0.9,
        ...      "bounding_box": {"x1": 100, "y1": 100, "x2": 200, "y2": 200}},
        ...     {"category": "car", "confidence": 0.85,
        ...      "bounding_box": {"x1": 105, "y1": 105, "x2": 205, "y2": 205}}
        ... ]
        >>> filtered = apply_nms(detections, iou_threshold=0.5, class_agnostic=True)
        >>> len(filtered)
        1
    """
    ...

# Classes
class AgnosticNMS:
    # Production-grade NMS implementation with YOLO-matching behavior.
    #
    # Features:
    # - Class-specific and class-agnostic modes
    # - Vectorized (PyTorch) and iterative fallback
    # - Numerical stability enhancements
    # - Box validation and filtering
    # - Schema preservation
    # - Zero side effects
    # - Supports both x1/y1/x2/y2 and xmin/ymin/xmax/ymax bbox formats
    #
    # Attributes:
    #     iou_threshold: IoU threshold for suppression (default: 0.45)
    #     min_box_size: Minimum box width/height in pixels (default: 2.0)
    #     use_vectorized: Use torchvision.ops.nms if available (default: True)
    #     eps: Epsilon for numerical stability (default: 1e-7)

    def __init__(self: Any, iou_threshold: float = 0.45, min_box_size: float = 2.0, use_vectorized: bool = True, eps: float = 1e-07) -> None:
        """
        Initialize NMS module.
        
        Args:
            iou_threshold: IoU threshold for suppression (0.0 to 1.0)
            min_box_size: Minimum box dimension in pixels
            use_vectorized: Use PyTorch implementation if available
            eps: Epsilon for numerical stability in IoU computation
        """
        ...

    def apply(self: Any, detections: List[Dict[str, Any]], class_agnostic: bool = True, target_categories: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """
        Apply NMS to detections.
        
        Args:
            detections: List of detection dicts with schema:
                {
                    "category": str,
                    "confidence": float,
                    "bounding_box": {"x1": float, "y1": float, "x2": float, "y2": float}
                                 or {"xmin": float, "ymin": float, "xmax": float, "ymax": float},
                    ... (other fields preserved)
                }
            class_agnostic: If True, suppress across all classes
            target_categories: Optional list of categories to process (others ignored)
        
        Returns:
            Filtered list of detections with identical schema
        """
        ...

    def get_stats(self: Any) -> Dict[str, Any]:
        """
        Get NMS usage statistics.
        
        Returns:
            Dictionary with statistics:
            - total_calls: Number of times apply() was called
            - vectorized_calls: Number of vectorized NMS calls
            - iterative_calls: Number of iterative NMS calls
            - total_input: Total input detections
            - total_output: Total output detections
            - total_suppressed: Total suppressed detections
            - suppression_rate: Percentage of detections suppressed
        """
        ...

    def is_vectorized_available() -> bool:
        """
        Check if vectorized implementation is available.
        """
        ...

    def reset_stats(self: Any) -> Any:
        """
        Reset usage statistics.
        """
        ...

