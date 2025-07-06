"""
Color processing utilities for extracting colors from detected objects in video frames.
"""

import cv2
import numpy as np
import json
import tempfile
import os
from typing import List, Dict, Any, Tuple, Optional
from collections import defaultdict
from datetime import datetime, timedelta
import logging
from sklearn.cluster import KMeans
from skimage import color
from matplotlib import colors as mcolors
import numpy as np
logger = logging.getLogger(__name__)

# Try to import sklearn at module level with fallback
try:
    from sklearn.cluster import KMeans
    SKLEARN_AVAILABLE = True
    logger.debug("sklearn successfully imported for color clustering")
except ImportError:
    SKLEARN_AVAILABLE = False
    logger.warning("sklearn not available, using fallback color extraction method")
except RuntimeError as e:
    # Handle the specific "can't register atexit after shutdown" error
    if "atexit" in str(e):
        SKLEARN_AVAILABLE = False
        logger.warning(f"sklearn import failed due to shutdown race condition: {e}. Using fallback method.")
    else:
        raise

# Color extraction functions
def extract_major_colors(image: np.ndarray, k: int = 3) -> List[Tuple[str, str, float]]:
    """
    Extract the major colors from an image using K-means clustering.
    
    Args:
        image: Input image as numpy array (RGB format)
        k: Number of dominant colors to extract
        
    Returns:
        List of tuples containing (color_name, hex_color, percentage)
    """
    if not SKLEARN_AVAILABLE:
        logger.debug("Using OpenCV fallback method for color extraction")
        return _extract_major_colors_opencv_fallback(image, k)
    
    try:
        # Use sklearn method
        return _extract_major_colors_sklearn(image, k)
    except Exception as e:
        logger.warning(f"sklearn color extraction failed: {e}. Using OpenCV fallback.")
        return _extract_major_colors_opencv_fallback(image, k)


def _extract_major_colors_sklearn(image: np.ndarray, k: int = 3) -> List[Tuple[str, str, float]]:
    """Extract major colors using sklearn KMeans clustering."""
    # Reshape image to be a list of pixels
    data = image.reshape((-1, 3))
    data = np.float32(data)
    
    # Apply sklearn K-means clustering
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(data)
    
    # Get cluster centers and labels
    centers = np.uint8(kmeans.cluster_centers_)
    labels = kmeans.labels_
    
    # Calculate percentages
    unique_labels, counts = np.unique(labels, return_counts=True)
    percentages = counts / len(labels)
    
    # Convert to color names and hex
    colors = []
    for i, (center, percentage) in enumerate(zip(centers, percentages)):
        hex_color = "#{:02x}{:02x}{:02x}".format(center[0], center[1], center[2])
        color_name = _rgb_to_color_name(center)
        colors.append((color_name, hex_color, float(percentage)))
    
    # Sort by percentage (descending)
    colors.sort(key=lambda x: x[2], reverse=True)
    
    return colors


def _extract_major_colors_opencv_fallback(image: np.ndarray, k: int = 3) -> List[Tuple[str, str, float]]:
    """Extract major colors using OpenCV's K-means clustering as fallback."""
    try:
        # Reshape image to be a list of pixels
        data = image.reshape((-1, 3))
        data = np.float32(data)
        
        # Apply OpenCV K-means clustering
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        _, labels, centers = cv2.kmeans(data, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
        
        # Convert centers to uint8
        centers = np.uint8(centers)
        
        # Calculate percentages
        unique_labels, counts = np.unique(labels, return_counts=True)
        percentages = counts / len(labels)
        
        # Convert to color names and hex
        colors = []
        for i, (center, percentage) in enumerate(zip(centers, percentages)):
            hex_color = "#{:02x}{:02x}{:02x}".format(center[0], center[1], center[2])
            color_name = _rgb_to_color_name(center)
            colors.append((color_name, hex_color, float(percentage)))
        
        # Sort by percentage (descending)
        colors.sort(key=lambda x: x[2], reverse=True)
        
        return colors
        
    except Exception as e:
        logger.error(f"OpenCV color extraction failed: {e}. Using basic color analysis.")
        return _extract_colors_basic_fallback(image, k)


def _extract_colors_basic_fallback(image: np.ndarray, k: int = 3) -> List[Tuple[str, str, float]]:
    """Basic color extraction fallback using color channel analysis."""
    try:
        if image.size == 0:
            return []
            
        # Calculate average color
        mean_color = np.mean(image.reshape(-1, 3), axis=0).astype(np.uint8)
        hex_color = "#{:02x}{:02x}{:02x}".format(mean_color[0], mean_color[1], mean_color[2])
        color_name = _rgb_to_color_name(mean_color)
        
        # For simplicity, return the average color as the dominant color
        return [(color_name, hex_color, 1.0)]
        
    except Exception as e:
        logger.error(f"Basic color extraction failed: {e}. Returning default.")
        return [("unknown", "#808080", 1.0)]  # Gray as default


# def _rgb_to_color_name(rgb: np.ndarray) -> str:
#     """
#     Convert RGB values to approximate color name.
    
#     Args:
#         rgb: RGB values as numpy array
        
#     Returns:
#         Color name as string
#     """
#     r, g, b = rgb
    
#     # Simple color mapping based on dominant channel
#     if r > g and r > b:
#         if r > 200:
#             return "red" if g < 100 and b < 100 else "pink"
#         else:
#             return "brown" if g > 100 or b > 100 else "dark_red"
#     elif g > r and g > b:
#         if g > 200:
#             return "green" if r < 100 and b < 100 else "light_green"
#         else:
#             return "dark_green"
#     elif b > r and b > g:
#         if b > 200:
#             return "blue" if r < 100 and g < 100 else "light_blue"
#         else:
#             return "dark_blue"
#     else:
#         # Similar values - grayscale or mixed
#         avg = (r + g + b) / 3
#         if avg > 200:
#             return "white"
#         elif avg < 50:
#             return "black"
#         else:
#             return "gray"

XKCD_COLORS = {
    name.replace("xkcd:", ""): mcolors.to_rgb(hex)
    for name, hex in mcolors.XKCD_COLORS.items()
}

# Canonical colors you want to allow
CANONICAL_COLOR_NAMES = [
    "brown", "red", "orange", "yellow", "green", "lime", "cyan",
    "blue", "purple", "pink", "white", "grey", "black"
]

# Canonical RGB values (you can adjust these if needed)
CANONICAL_COLOR_RGB = {
    "brown":   (150, 75, 0),
    "red":     (255, 0, 0),
    "orange":  (255, 165, 0),
    "yellow":  (255, 255, 0),
    "green":   (0, 128, 0),
    "lime":    (191, 255, 0),
    "cyan":    (0, 255, 255),
    "blue":    (0, 0, 255),
    "purple":  (128, 0, 128),
    "pink":    (255, 192, 203),
    "white":   (255, 255, 255),
    "grey":    (128, 128, 128),
    "black":   (0, 0, 0)
}

# Pre-convert to LAB for speed
CANONICAL_COLOR_LAB = {
    name: color.rgb2lab([[np.array(rgb) / 255.0]])[0][0]
    for name, rgb in CANONICAL_COLOR_RGB.items()
}

def _rgb_to_color_name(rgb: np.ndarray) -> str:
    """
    Convert an RGB color to the closest color in a fixed canonical set.
    
    Args:
        rgb: RGB triplet as np.ndarray or list (0–255)
        
    Returns:
        Closest canonical color name as string
    """
    rgb = np.array(rgb)
    rgb_normalized = rgb / 255.0
    input_lab = color.rgb2lab([[rgb_normalized]])[0][0]

    min_dist = float('inf')
    closest_name = "unknown"

    for name, ref_lab in CANONICAL_COLOR_LAB.items():
        dist = np.linalg.norm(input_lab - ref_lab)
        if dist < min_dist:
            min_dist = dist
            closest_name = name

    return closest_name




class VideoColorClassifier:
    """
    A comprehensive system for processing video frames with model predictions
    and extracting color information from detected objects.
    """
    
    def __init__(self, top_k_colors: int = 3, min_confidence: float = 0.5):
        """
        Initialize the video color classifier.
        
        Args:
            top_k_colors: Number of top colors to extract per detection
            min_confidence: Minimum confidence threshold for detections
        """
        self.top_k_colors = top_k_colors
        self.min_confidence = min_confidence
        self.detailed_results = []
        self.summary_results = defaultdict(lambda: defaultdict(list))
        
    def process_video_with_predictions(
        self,
        video_bytes: bytes,
        predictions: Dict[str, List[Dict]],
        output_dir: str = "./output",
        fps: Optional[float] = None
    ) -> Tuple[str, str]:
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
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Create temporary video file
        with tempfile.NamedTemporaryFile(suffix='.mp4', delete=False) as temp_video:
            temp_video.write(video_bytes)
            temp_video_path = temp_video.name
        
        try:
            # Process video frame by frame
            self._process_video_frames(temp_video_path, predictions, fps)
            
            # Save detailed results
            detailed_path = os.path.join(output_dir, "detailed_color_results.json")
            self._save_detailed_results(detailed_path)
            
            # Generate and save summary results
            summary_path = os.path.join(output_dir, "color_summary_report.json")
            self._generate_summary_report(summary_path, fps)
            
            logger.info(f"Processing complete. Results saved to {output_dir}")
            return detailed_path, summary_path
            
        finally:
            # Clean up temporary video file
            if os.path.exists(temp_video_path):
                os.unlink(temp_video_path)
    
    def _process_video_frames(
        self,
        video_path: str,
        predictions: Dict[str, List[Dict]],
        fps: Optional[float] = None
    ):
        """
        Process video frame by frame and extract colors from detections.
        """
        cap = cv2.VideoCapture(video_path)
        
        if not cap.isOpened():
            raise ValueError(f"Could not open video file: {video_path}")
        
        # Get video properties
        if fps is None:
            fps = cap.get(cv2.CAP_PROP_FPS)
        
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        logger.info(f"Processing video: {total_frames} frames at {fps} FPS")
        
        frame_count = 0
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            frame_id = str(frame_count)
            timestamp = frame_count / fps
            
            # Convert BGR to RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Process detections for this frame
            if frame_id in predictions:
                frame_detections = predictions[frame_id]
                self._process_frame_detections(
                    rgb_frame, frame_detections, frame_id, timestamp
                )
            
            frame_count += 1
            
            # Log progress
            if frame_count % 100 == 0:
                logger.info(f"Processed {frame_count}/{total_frames} frames")
        
        cap.release()
        logger.info(f"Completed processing {frame_count} frames")
    
    def _process_frame_detections(
        self,
        frame: np.ndarray,
        detections: List[Dict],
        frame_id: str,
        timestamp: float
    ):
        """
        Process all detections in a single frame.
        """
        for detection in detections:
            # Skip low confidence detections
            if detection.get('confidence', 1.0) < self.min_confidence:
                continue
            
            # Extract detection information
            bbox = detection.get('bounding_box', detection.get('bbox'))
            category = detection.get('category', detection.get('class', 'unknown'))
            track_id = detection.get('track_id', detection.get('id'))
            confidence = detection.get('confidence', 1.0)
            
            if bbox is None:
                continue
            
            # Crop object from frame
            cropped_obj = self._crop_bbox(frame, bbox)
            
            if cropped_obj.size == 0:
                logger.warning(f"Empty crop for bbox: {bbox} in frame {frame_id}")
                continue
            
            # Extract colors
            major_colors = extract_major_colors(cropped_obj, k=self.top_k_colors)
            main_color = major_colors[0][0] if major_colors else "unknown"
            
            # Create detailed result entry
            detailed_entry = {
                "frame_id": frame_id,
                "timestamp": round(timestamp, 2),
                "timestamp_formatted": self._format_timestamp(timestamp),
                "track_id": track_id,
                "category": category,
                "confidence": round(confidence, 3),
                "bbox": bbox,
                "major_colors": major_colors,
                "main_color": main_color,
                "color_confidence": major_colors[0][2] if major_colors else 0.0
            }
            
            self.detailed_results.append(detailed_entry)
            
            # Update summary data
            self._update_summary_data(detailed_entry)
    
    def _crop_bbox(self, image: np.ndarray, bbox: Dict[str, int]) -> np.ndarray:
        """
        Crop image using bbox coordinates with bounds checking.
        """
        h, w = image.shape[:2]
        
        # Handle different bbox formats
        if 'xmin' in bbox:
            xmin = max(0, int(bbox["xmin"]))
            ymin = max(0, int(bbox["ymin"]))
            xmax = min(w, int(bbox["xmax"]))
            ymax = min(h, int(bbox["ymax"]))
        elif 'x1' in bbox:
            xmin = max(0, int(bbox["x1"]))
            ymin = max(0, int(bbox["y1"]))
            xmax = min(w, int(bbox["x2"]))
            ymax = min(h, int(bbox["y2"]))
        else:
            # Assume [x1, y1, x2, y2] format
            values = list(bbox.values()) if isinstance(bbox, dict) else bbox
            xmin = max(0, int(values[0]))
            ymin = max(0, int(values[1]))
            xmax = min(w, int(values[2]))
            ymax = min(h, int(values[3]))
        
        # Ensure valid crop region
        if xmax <= xmin or ymax <= ymin:
            return np.array([])
        
        return image[ymin:ymax, xmin:xmax]
    
    def _update_summary_data(self, detection_entry: Dict):
        """
        Update summary data with detection entry.
        """
        category = detection_entry["category"]
        main_color = detection_entry["main_color"]
        timestamp = detection_entry["timestamp"]
        
        self.summary_results[category][main_color].append({
            "timestamp": timestamp,
            "confidence": detection_entry["confidence"],
            "track_id": detection_entry["track_id"]
        })
    
    def _generate_summary_report(self, output_path: str, fps: float):
        """
        Generate and save summary report.
        """
        summary_report = {
            "processing_info": {
                "total_detections": len(self.detailed_results),
                "fps": fps,
                "processing_timestamp": datetime.now().isoformat()
            },
            "category_color_analysis": {},
            "color_distribution": defaultdict(int),
            "insights": []
        }
        
        # Analyze each category
        for category, color_data in self.summary_results.items():
            category_analysis = {
                "total_detections": sum(len(detections) for detections in color_data.values()),
                "color_breakdown": {},
                "dominant_color": None,
                "color_diversity": len(color_data)
            }
            
            # Calculate color breakdown
            for color, detections in color_data.items():
                category_analysis["color_breakdown"][color] = len(detections)
                summary_report["color_distribution"][color] += len(detections)
            
            # Find dominant color
            if category_analysis["color_breakdown"]:
                dominant_color = max(category_analysis["color_breakdown"].items(), key=lambda x: x[1])
                category_analysis["dominant_color"] = {
                    "color": dominant_color[0],
                    "count": dominant_color[1],
                    "percentage": round(dominant_color[1] / category_analysis["total_detections"] * 100, 2)
                }
            
            summary_report["category_color_analysis"][category] = category_analysis
        
        # Generate insights
        summary_report["insights"] = self._generate_insights(summary_report)
        
        # Save to file
        with open(output_path, 'w') as f:
            json.dump(summary_report, f, indent=2, default=str)
        
        logger.info(f"Summary report saved to {output_path}")
    
    def _generate_insights(self, summary_report: Dict) -> List[str]:
        """
        Generate insights from the summary report.
        """
        insights = []
        
        total_detections = summary_report["processing_info"]["total_detections"]
        insights.append(f"Processed {total_detections} total detections")
        
        # Most common color overall
        color_dist = summary_report["color_distribution"]
        if color_dist:
            most_common_color = max(color_dist.items(), key=lambda x: x[1])
            insights.append(f"Most common color across all categories: {most_common_color[0]} ({most_common_color[1]} detections)")
        
        # Category-specific insights
        for category, analysis in summary_report["category_color_analysis"].items():
            if analysis["dominant_color"]:
                dominant = analysis["dominant_color"]
                insights.append(f"{category.title()}: predominantly {dominant['color']} ({dominant['percentage']}%)")
            
            if analysis["color_diversity"] > 5:
                insights.append(f"{category.title()}: high color diversity ({analysis['color_diversity']} different colors)")
        
        return insights
    
    def _save_detailed_results(self, output_path: str):
        """
        Save detailed results to JSON file.
        """
        detailed_data = {
            "processing_info": {
                "total_detections": len(self.detailed_results),
                "processing_timestamp": datetime.now().isoformat()
            },
            "detections": self.detailed_results
        }
        
        with open(output_path, 'w') as f:
            json.dump(detailed_data, f, indent=2, default=str)
        
        logger.info(f"Detailed results saved to {output_path}")
    
    def _format_timestamp(self, seconds: float) -> str:
        """
        Format timestamp in MM:SS format.
        """
        minutes = int(seconds // 60)
        seconds = int(seconds % 60)
        return f"{minutes:02d}:{seconds:02d}"
    
    def reset(self):
        """
        Reset the classifier state.
        """
        self.detailed_results = []
        self.summary_results = defaultdict(lambda: defaultdict(list))


def process_video_with_color_detection(
    video_bytes: bytes,
    predictions: Dict[str, List[Dict]],
    output_dir: str = "./output",
    top_k_colors: int = 3,
    min_confidence: float = 0.5,
    fps: Optional[float] = None
) -> Tuple[str, str]:
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
    classifier = VideoColorClassifier(top_k_colors=top_k_colors, min_confidence=min_confidence)
    return classifier.process_video_with_predictions(video_bytes, predictions, output_dir, fps) 