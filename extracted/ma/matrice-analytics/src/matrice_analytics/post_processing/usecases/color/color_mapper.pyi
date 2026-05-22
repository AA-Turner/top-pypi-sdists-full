"""Auto-generated stub for module: color_mapper."""
from typing import Any, Dict, List, Optional, Tuple

# Constants
logger: Any

# Functions
def process_video_with_color_detection(video_bytes: Any, yolo_predictions: Dict[str, List[Dict]], output_dir: str = './output', top_k_colors: int = 3, min_confidence: float = 0.5, fps: Optional[float] = None) -> Tuple[str, str]:
    """
    Process video with YOLO predictions and extract color information.
    
    Args:
        video_bytes: Raw video file bytes
        yolo_predictions: Dict with frame_id -> list of YOLO detection dicts
        output_dir: Directory to save output files
        top_k_colors: Number of top colors to extract per detection
        min_confidence: Minimum confidence threshold for detections
        fps: Video FPS (auto-detected if not provided)
    
    Returns:
        Tuple of (detailed_results_path, summary_results_path)
    
    Example:
        >>> with open("video.mp4", "rb") as f:
        ...     video_bytes = f.read()
        >>>
        >>> # YOLO predictions format:
        >>> predictions = {
        ...     "0": [
        ...         {
        ...             "category": "car",
        ...             "bounding_box": {"xmin": 100, "ymin": 50, "xmax": 200, "ymax": 150},
        ...             "confidence": 0.95,
        ...             "track_id": "car_001"
        ...         }
        ...     ],
        ...     "1": [...]
        ... }
        >>>
        >>> detailed_path, summary_path = process_video_with_color_detection(
        ...     video_bytes, predictions, "./results"
        ... )
    """
    ...

# Classes
class VideoColorClassifier:
    # A comprehensive system for processing video frames with YOLO predictions
    # and extracting color information from detected objects.

    def __init__(self: Any, top_k_colors: int = 3, min_confidence: float = 0.5) -> None:
        """
        Initialize the video color classifier.
        
        Args:
            top_k_colors: Number of top colors to extract per detection
            min_confidence: Minimum confidence threshold for detections
        """
        ...

    def process_video_with_predictions(self: Any, video_bytes: Any, predictions: Dict[str, List[Dict]], output_dir: str = './output', fps: Optional[float] = None) -> Tuple[str, str]:
        """
        Main function to process video with YOLO predictions and extract colors.
        
        Args:
            video_bytes: Raw video file bytes
            predictions: Dict with frame_id -> list of detection dicts
            output_dir: Directory to save output files
            fps: Video FPS (will be auto-detected if not provided)
        
        Returns:
            Tuple of (detailed_results_path, summary_results_path)
        """
        ...

    def reset(self: Any) -> Any:
        """
        Reset the classifier for processing a new video.
        """
        ...

