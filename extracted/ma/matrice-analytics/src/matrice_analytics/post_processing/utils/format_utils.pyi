"""Auto-generated stub for module: format_utils."""
from typing import Any, Dict, List

from ..core.base import ResultFormat

# Functions
def convert_detection_to_tracking_format(detections: List[Dict], frame_id: str = '0') -> Dict:
    """
    Convert detection format to tracking format.
    
    Args:
        detections: List of detection dictionaries
        frame_id: Frame identifier
    
    Returns:
        Dict: Results in tracking format
    """
    ...
def convert_to_coco_format(results: Any) -> List[Dict]:
    """
    Convert results to COCO format.
    
    Args:
        results: Input results in any supported format
    
    Returns:
        List[Dict]: Results in COCO format
    """
    ...
def convert_to_tracking_format(detections: List[Dict], frame_id: str = '0') -> Dict:
    """
    Convert detection format to tracking format.
    
    Args:
        detections: List of detection dictionaries
        frame_id: Frame identifier
    
    Returns:
        Dict: Results in tracking format
    """
    ...
def convert_to_yolo_format(results: Any) -> List[List[float]]:
    """
    Convert results to YOLO format (normalized coordinates).
    
    Args:
        results: Input results in any supported format
    
    Returns:
        List[List[float]]: Results in YOLO format [class_id, x_center, y_center, width, height, confidence]
    """
    ...
def convert_tracking_to_detection_format(tracking_results: Dict) -> List[Dict]:
    """
    Convert tracking format to detection format.
    
    Args:
        tracking_results: Tracking results dictionary
    
    Returns:
        List[Dict]: Results in detection format
    """
    ...
def match_results_structure(results: Any) -> Any:
    """
    Match the results structure to the expected structure based on actual output formats.
    
    Based on eg_output.json:
    - Classification: {"category": str, "confidence": float}
    - Detection: [{"bounding_box": {...}, "category": str, "confidence": float}, ...]
    - Instance Segmentation: Same as detection but with "masks" field
    - Object Tracking: {"frame_id": [{"track_id": int, "category": str, "confidence": float, "bounding_box": {...}}, ...]}
    - Activity Recognition: {"frame_id": [{"category": str, "confidence": float, "bounding_box": {...}}, ...]} (no track_id)
    
    Args:
        results: Raw model output to analyze
    
    Returns:
        ResultFormat: Detected format type
    """
    ...
