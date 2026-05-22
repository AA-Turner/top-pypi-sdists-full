"""Auto-generated stub for module: advanced_helper_utils."""
from typing import Any, Dict, List, Optional, Tuple

# Functions
def bytes_to_image(image_bytes: Any, return_format: str = 'pil') -> Optional[Any]:
    """
    Convert image bytes to PIL Image or numpy array.
    """
    ...
def bytes_to_video_frame(video_bytes: Any, frame_number: int = 0, return_format: str = 'cv2') -> Optional[Any]:
    """
    Extract a specific frame from video bytes.
    """
    ...
def calculate_bbox_fingerprint(bbox: Dict[str, float], category: str = 'unknown') -> str:
    """
    Generate a fingerprint for bbox deduplication.
    """
    ...
def clean_expired_tracks(track_timestamps: Dict, track_last_seen: Dict, current_timestamp: float, expiry_time: float) -> None:
    """
    Clean expired tracks from tracking dictionaries.
    """
    ...
def convert_detection_to_tracking_format(detections: List[Dict], frame_id: str = '0') -> Dict:
    """
    Convert detection format to tracking format.
    """
    ...
def convert_tracking_to_detection_format(tracking_results: Dict) -> List[Dict]:
    """
    Convert tracking format to detection format.
    """
    ...
def generate_summary_statistics(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate comprehensive summary statistics from tracking data.
    """
    ...
def get_image_dimensions(image_bytes: Any) -> Optional[Tuple[int, int]]:
    """
    Get image dimensions (width, height) from image bytes.
    """
    ...
def get_image_format(image_bytes: Any) -> Optional[str]:
    """
    Detect image format from bytes.
    """
    ...
def is_valid_image_bytes(image_bytes: Any) -> bool:
    """
    Check if bytes represent a valid image.
    """
    ...
def line_segments_intersect(p1: Tuple[float, float], p2: Tuple[float, float], p3: Tuple[float, float], p4: Tuple[float, float]) -> bool:
    """
    Check if two line segments intersect.
    """
    ...
