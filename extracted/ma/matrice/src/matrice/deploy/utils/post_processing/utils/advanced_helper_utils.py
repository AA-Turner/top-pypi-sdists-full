"""
Advanced helper utilities for specialized post-processing operations.
These functions provide advanced image/video processing and tracking utilities
not available in the basic refactored system.
"""

import time
import math
import io
import numpy as np
from typing import List, Dict, Any, Tuple, Optional, Set
from collections import defaultdict

# Try to import optional dependencies
try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

try:
    import cv2
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False


def line_segments_intersect(p1: Tuple[float, float], p2: Tuple[float, float], 
                           p3: Tuple[float, float], p4: Tuple[float, float]) -> bool:
    """Check if two line segments intersect."""
    def ccw(A, B, C):
        return (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])
    
    return ccw(p1, p3, p4) != ccw(p2, p3, p4) and ccw(p1, p2, p3) != ccw(p1, p2, p4)


def calculate_bbox_fingerprint(bbox: Dict[str, float], category: str = "unknown") -> str:
    """Generate a fingerprint for bbox deduplication."""
    if not bbox:
        return f"{category}_empty"
    
    # Normalize bbox format
    if "xmin" in bbox:
        x1, y1, x2, y2 = bbox["xmin"], bbox["ymin"], bbox["xmax"], bbox["ymax"]
    elif "x1" in bbox:
        x1, y1, x2, y2 = bbox["x1"], bbox["y1"], bbox["x2"], bbox["y2"]
    else:
        values = list(bbox.values())
        x1, y1, x2, y2 = values[0], values[1], values[2], values[3]
    
    # Round to reduce minor variations
    x1, y1, x2, y2 = round(x1, 1), round(y1, 1), round(x2, 1), round(y2, 1)
    
    return f"{category}_{x1}_{y1}_{x2}_{y2}"


def clean_expired_tracks(track_timestamps: Dict, track_last_seen: Dict, 
                        current_timestamp: float, expiry_time: float) -> None:
    """Clean expired tracks from tracking dictionaries."""
    expired_tracks = []
    
    for track_id, last_seen in track_last_seen.items():
        if current_timestamp - last_seen > expiry_time:
            expired_tracks.append(track_id)
    
    for track_id in expired_tracks:
        track_timestamps.pop(track_id, None)
        track_last_seen.pop(track_id, None)


def generate_summary_statistics(data: Dict[str, Any]) -> Dict[str, Any]:
    """Generate comprehensive summary statistics from tracking data."""
    summary = {
        "total_objects": 0,
        "objects_by_category": defaultdict(int),
        "unique_tracks": set(),
        "tracks_by_category": defaultdict(set),
        "frame_count": 0,
        "time_range": {"start": None, "end": None},
        "activity_periods": []
    }
    
    if isinstance(data, dict):
        for frame_id, detections in data.items():
            if isinstance(detections, list):
                summary["frame_count"] += 1
                frame_time = None
                
                try:
                    frame_time = float(frame_id)
                    if summary["time_range"]["start"] is None or frame_time < summary["time_range"]["start"]:
                        summary["time_range"]["start"] = frame_time
                    if summary["time_range"]["end"] is None or frame_time > summary["time_range"]["end"]:
                        summary["time_range"]["end"] = frame_time
                except:
                    pass
                
                for detection in detections:
                    summary["total_objects"] += 1
                    category = detection.get("category", "unknown")
                    summary["objects_by_category"][category] += 1
                    
                    if "track_id" in detection:
                        track_id = detection["track_id"]
                        summary["unique_tracks"].add(track_id)
                        summary["tracks_by_category"][category].add(track_id)
    
    # Convert sets to counts for JSON serialization
    summary["unique_tracks"] = len(summary["unique_tracks"])
    summary["tracks_by_category"] = {k: len(v) for k, v in summary["tracks_by_category"].items()}
    summary["objects_by_category"] = dict(summary["objects_by_category"])
    
    return summary


def bytes_to_image(image_bytes: bytes, return_format: str = "pil") -> Optional[Any]:
    """Convert image bytes to PIL Image or numpy array."""
    if not image_bytes:
        return None
    
    try:
        if return_format.lower() == "pil":
            if not PIL_AVAILABLE:
                raise ImportError("PIL is required for PIL format. Install with: pip install Pillow")
            return Image.open(io.BytesIO(image_bytes))
        
        elif return_format.lower() == "cv2":
            if not CV2_AVAILABLE:
                raise ImportError("OpenCV is required for CV2 format. Install with: pip install opencv-python")
            
            # Convert bytes to numpy array
            nparr = np.frombuffer(image_bytes, np.uint8)
            # Decode image
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            return img
        
        elif return_format.lower() == "numpy":
            if PIL_AVAILABLE:
                pil_img = Image.open(io.BytesIO(image_bytes))
                return np.array(pil_img)
            else:
                raise ImportError("PIL is required for numpy conversion. Install with: pip install Pillow")
        
        else:
            raise ValueError(f"Unsupported return format: {return_format}. Use 'pil', 'cv2', or 'numpy'")
    
    except Exception as e:
        print(f"Error converting image bytes: {e}")
        return None


def bytes_to_video_frame(video_bytes: bytes, frame_number: int = 0, return_format: str = "cv2") -> Optional[Any]:
    """Extract a specific frame from video bytes."""
    if not video_bytes or not CV2_AVAILABLE:
        if not CV2_AVAILABLE:
            raise ImportError("OpenCV is required for video processing. Install with: pip install opencv-python")
        return None
    
    try:
        # Create temporary file in memory
        import tempfile
        import os
        
        with tempfile.NamedTemporaryFile(suffix='.mp4', delete=False) as temp_file:
            temp_file.write(video_bytes)
            temp_path = temp_file.name
        
        try:
            # Open video
            cap = cv2.VideoCapture(temp_path)
            
            # Set frame position
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
            
            # Read frame
            ret, frame = cap.read()
            cap.release()
            
            if not ret:
                return None
            
            if return_format.lower() == "cv2":
                return frame
            elif return_format.lower() == "pil":
                if not PIL_AVAILABLE:
                    raise ImportError("PIL is required for PIL format. Install with: pip install Pillow")
                # Convert BGR to RGB for PIL
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                return Image.fromarray(rgb_frame)
            elif return_format.lower() == "numpy":
                return frame
            else:
                raise ValueError(f"Unsupported return format: {return_format}")
        
        finally:
            # Clean up temporary file
            if os.path.exists(temp_path):
                os.unlink(temp_path)
    
    except Exception as e:
        print(f"Error extracting video frame: {e}")
        return None


def get_image_dimensions(image_bytes: bytes) -> Optional[Tuple[int, int]]:
    """Get image dimensions (width, height) from image bytes."""
    if not image_bytes:
        return None
    
    try:
        if PIL_AVAILABLE:
            img = Image.open(io.BytesIO(image_bytes))
            return img.size  # PIL returns (width, height)
        elif CV2_AVAILABLE:
            nparr = np.frombuffer(image_bytes, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            if img is not None:
                height, width = img.shape[:2]
                return (width, height)
        else:
            raise ImportError("Either PIL or OpenCV is required. Install with: pip install Pillow opencv-python")
        
    except Exception as e:
        print(f"Error getting image dimensions: {e}")
    
    return None


def is_valid_image_bytes(image_bytes: bytes) -> bool:
    """Check if bytes represent a valid image."""
    if not image_bytes:
        return False
    
    try:
        if PIL_AVAILABLE:
            Image.open(io.BytesIO(image_bytes))
            return True
        elif CV2_AVAILABLE:
            nparr = np.frombuffer(image_bytes, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            return img is not None
        else:
            # Basic check for common image headers
            if image_bytes.startswith(b'\xff\xd8\xff'):  # JPEG
                return True
            elif image_bytes.startswith(b'\x89PNG\r\n\x1a\n'):  # PNG
                return True
            elif image_bytes.startswith(b'GIF87a') or image_bytes.startswith(b'GIF89a'):  # GIF
                return True
            elif image_bytes.startswith(b'BM'):  # BMP
                return True
            return False
        
    except Exception:
        return False


def get_image_format(image_bytes: bytes) -> Optional[str]:
    """Detect image format from bytes."""
    if not image_bytes:
        return None
    
    try:
        if PIL_AVAILABLE:
            img = Image.open(io.BytesIO(image_bytes))
            return img.format.lower() if img.format else None
        else:
            # Basic format detection
            if image_bytes.startswith(b'\xff\xd8\xff'):
                return 'jpeg'
            elif image_bytes.startswith(b'\x89PNG\r\n\x1a\n'):
                return 'png'
            elif image_bytes.startswith(b'GIF87a') or image_bytes.startswith(b'GIF89a'):
                return 'gif'
            elif image_bytes.startswith(b'BM'):
                return 'bmp'
            elif image_bytes.startswith(b'RIFF') and b'WEBP' in image_bytes[:12]:
                return 'webp'
            return None
        
    except Exception:
        return None


def convert_detection_to_tracking_format(detections: List[Dict], frame_id: str = "0") -> Dict:
    """Convert detection format to tracking format."""
    tracking_results = {frame_id: []}
    
    for detection in detections:
        tracking_detection = {
            "track_id": detection.get("track_id", 0),
            "category": detection.get("category", "unknown"),
            "confidence": detection.get("confidence", 0.0),
            "bounding_box": detection.get("bounding_box", detection.get("bbox", {}))
        }
        tracking_results[frame_id].append(tracking_detection)
    
    return tracking_results


def convert_tracking_to_detection_format(tracking_results: Dict) -> List[Dict]:
    """Convert tracking format to detection format."""
    detections = []
    
    for frame_id, frame_detections in tracking_results.items():
        if isinstance(frame_detections, list):
            for detection in frame_detections:
                detection_item = {
                    "category": detection.get("category", "unknown"),
                    "confidence": detection.get("confidence", 0.0),
                    "bounding_box": detection.get("bounding_box", detection.get("bbox", {}))
                }
                if "track_id" in detection:
                    detection_item["track_id"] = detection["track_id"]
                detections.append(detection_item)
    
    return detections 