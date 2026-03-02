import cv2
import numpy as np
import json
import tempfile
import os
from typing import List, Dict, Any, Tuple, Optional
from collections import defaultdict
from datetime import datetime, timedelta
import logging

# Import your existing color extraction functions
#from color_map_utils import extract_major_colors

# Configure logging
logger = logging.getLogger(__name__)

class VideoColorClassifier:
    """
    A comprehensive system for processing video frames with YOLO predictions
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
        Main function to process video with YOLO predictions and extract colors.
        
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
            major_colors = [()] #extract_major_colors(cropped_obj, k=self.top_k_colors)
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
        elif 'x' in bbox:  # Alternative format
            x, y, width, height = bbox['x'], bbox['y'], bbox['width'], bbox['height']
            xmin = max(0, int(x))
            ymin = max(0, int(y))
            xmax = min(w, int(x + width))
            ymax = min(h, int(y + height))
        else:
            raise ValueError(f"Unsupported bbox format: {bbox}")
        
        return image[ymin:ymax, xmin:xmax]
    
    def _update_summary_data(self, detection_entry: Dict):
        """
        Update summary data structures with detection information.
        """
        category = detection_entry['category']
        main_color = detection_entry['main_color']
        timestamp = detection_entry['timestamp']
        
        # Store color occurrences with timestamps
        self.summary_results[category][main_color].append({
            'timestamp': timestamp,
            'timestamp_formatted': detection_entry['timestamp_formatted'],
            'track_id': detection_entry['track_id'],
            'confidence': detection_entry['confidence'],
            'color_confidence': detection_entry['color_confidence']
        })
    
    def _generate_summary_report(self, output_path: str, fps: float):
        """
        Generate human-readable summary report.
        """
        summary_report = {
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "total_detections": len(self.detailed_results),
                "video_fps": fps,
                "categories_detected": list(self.summary_results.keys())
            },
            "category_color_analysis": {},
            "time_intervals": {},
            "color_distribution": {}
        }
        
        # Generate category-wise color analysis
        for category, color_data in self.summary_results.items():
            category_analysis = {
                "total_detections": sum(len(occurrences) for occurrences in color_data.values()),
                "colors_found": {},
                "dominant_color": None,
                "time_range": {"start": None, "end": None}
            }
            
            # Analyze each color for this category
            max_count = 0
            all_timestamps = []
            
            for color, occurrences in color_data.items():
                count = len(occurrences)
                timestamps = [occ['timestamp'] for occ in occurrences]
                all_timestamps.extend(timestamps)
                
                if count > max_count:
                    max_count = count
                    category_analysis["dominant_color"] = color
                
                # Calculate time intervals for this color
                time_intervals = self._calculate_time_intervals(timestamps)
                
                category_analysis["colors_found"][color] = {
                    "count": count,
                    "percentage": round((count / category_analysis["total_detections"]) * 100, 2),
                    "first_seen": self._format_timestamp(min(timestamps)),
                    "last_seen": self._format_timestamp(max(timestamps)),
                    "time_intervals": time_intervals,
                    "average_confidence": round(
                        np.mean([occ['color_confidence'] for occ in occurrences]), 3
                    )
                }
            
            # Set overall time range for category
            if all_timestamps:
                category_analysis["time_range"] = {
                    "start": self._format_timestamp(min(all_timestamps)),
                    "end": self._format_timestamp(max(all_timestamps)),
                    "duration_seconds": round(max(all_timestamps) - min(all_timestamps), 2)
                }
            
            summary_report["category_color_analysis"][category] = category_analysis
        
        # Generate overall color distribution
        color_counts = defaultdict(int)
        for category_data in self.summary_results.values():
            for color, occurrences in category_data.items():
                color_counts[color] += len(occurrences)
        
        total_detections = sum(color_counts.values())
        summary_report["color_distribution"] = {
            color: {
                "count": count,
                "percentage": round((count / total_detections) * 100, 2)
            }
            for color, count in sorted(color_counts.items(), key=lambda x: x[1], reverse=True)
        }
        
        # Generate readable insights
        summary_report["insights"] = self._generate_insights(summary_report)
        
        # Save summary report
        with open(output_path, 'w') as f:
            json.dump(summary_report, f, indent=2)
        
        logger.info(f"Summary report saved to {output_path}")
    
    def _calculate_time_intervals(self, timestamps: List[float]) -> List[Dict]:
        """
        Calculate continuous time intervals from timestamps.
        """
        if not timestamps:
            return []
        
        timestamps = sorted(timestamps)
        intervals = []
        start = timestamps[0]
        end = timestamps[0]
        
        for i in range(1, len(timestamps)):
            # If gap is more than 2 seconds, start new interval
            if timestamps[i] - end > 2.0:
                intervals.append({
                    "start": self._format_timestamp(start),
                    "end": self._format_timestamp(end),
                    "duration": round(end - start, 2)
                })
                start = timestamps[i]
            end = timestamps[i]
        
        # Add final interval
        intervals.append({
            "start": self._format_timestamp(start),
            "end": self._format_timestamp(end),
            "duration": round(end - start, 2)
        })
        
        return intervals
    
    def _generate_insights(self, summary_report: Dict) -> List[str]:
        """
        Generate human-readable insights from the analysis.
        """
        insights = []
        
        # Most common category
        category_counts = {
            cat: data["total_detections"] 
            for cat, data in summary_report["category_color_analysis"].items()
        }
        
        if category_counts:
            most_common_category = max(category_counts, key=category_counts.get)
            insights.append(
                f"Most frequently detected object: {most_common_category} "
                f"({category_counts[most_common_category]} detections)"
            )
        
        # Most common color overall
        color_dist = summary_report["color_distribution"]
        if color_dist:
            most_common_color = max(color_dist, key=lambda x: color_dist[x]["count"])
            insights.append(
                f"Most common color across all objects: {most_common_color} "
                f"({color_dist[most_common_color]['percentage']}%)"
            )
        
        # Category-specific insights
        for category, data in summary_report["category_color_analysis"].items():
            if data["dominant_color"]:
                dominant_color = data["dominant_color"]
                color_data = data["colors_found"][dominant_color]
                insights.append(
                    f"{category.title()} objects are predominantly {dominant_color} "
                    f"({color_data['percentage']}% of {category} detections)"
                )
        
        return insights
    
    def _save_detailed_results(self, output_path: str):
        """
        Save detailed frame-by-frame results.
        """
        detailed_output = {
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "total_frames_processed": len(set(r["frame_id"] for r in self.detailed_results)),
                "total_detections": len(self.detailed_results),
                "detection_categories": list(set(r["category"] for r in self.detailed_results))
            },
            "detections": self.detailed_results
        }
        
        with open(output_path, 'w') as f:
            json.dump(detailed_output, f, indent=2)
        
        logger.info(f"Detailed results saved to {output_path}")
    
    def _format_timestamp(self, seconds: float) -> str:
        """
        Format timestamp in MM:SS format.
        """
        minutes = int(seconds // 60)
        secs = seconds % 60
        return f"{minutes:02d}:{secs:05.2f}"
    
    def reset(self):
        """
        Reset the classifier for processing a new video.
        """
        self.detailed_results = []
        self.summary_results = defaultdict(lambda: defaultdict(list))


# Convenience function for direct usage
def process_video_with_color_detection(
    video_bytes: bytes,
    yolo_predictions: Dict[str, List[Dict]],
    output_dir: str = "./output",
    top_k_colors: int = 3,
    min_confidence: float = 0.5,
    fps: Optional[float] = None
) -> Tuple[str, str]:
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
    classifier = VideoColorClassifier(top_k_colors, min_confidence)
    return classifier.process_video_with_predictions(
        video_bytes, yolo_predictions, output_dir, fps
    )