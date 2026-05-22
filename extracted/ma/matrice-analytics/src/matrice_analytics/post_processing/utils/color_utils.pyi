"""Auto-generated stub for module: color_utils."""
from typing import Any, Dict, List, Optional, Tuple

# Constants
CANONICAL_COLOR_LAB: Any
CANONICAL_COLOR_NAMES: List[Any]
CANONICAL_COLOR_RGB: Dict[Any, Any]
XKCD_COLORS: Any
logger: Any

# Functions
def extract_major_colors(image: Any.Any, k: int = 3) -> List[Tuple[str, str, float]]:
    """
    Extract the major colors from an image using K-means clustering.
    
    Args:
        image: Input image as numpy array (RGB format)
        k: Number of dominant colors to extract
    
    Returns:
        List of tuples containing (color_name, hex_color, percentage)
    """
    ...
def process_video_with_color_detection(video_bytes: Any, predictions: Dict[str, List[Dict]], output_dir: str = './output', top_k_colors: int = 3, min_confidence: float = 0.5, fps: Optional[float] = None) -> Tuple[str, str]:
    """
    Convenience function to process video with color detection.
    
    Args:
        video_bytes: Raw video file bytes
        predictions: Dict with frame_id -> list of detection dicts
        output_dir: Directory to save output files
        top_k_colors: Number of top colors to extract per detection
        min_confidence: Minimum confidence threshold for detections
        fps: Video FPS (will be auto-detected if not provided)
    
    Returns:
        Tuple of (detailed_results_path, summary_results_path)
    """
    ...

# Classes
class VideoColorClassifier:
    # A comprehensive system for processing video frames with model predictions
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
        Main function to process video with model predictions and extract colors.
        
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
        Reset the classifier state.
        """
        ...

