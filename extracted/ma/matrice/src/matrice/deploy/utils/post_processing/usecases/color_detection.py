"""
Color Detection Use Case for Post-Processing Framework

This module provides color detection capabilities for objects in video streams.
It analyzes the dominant colors of detected objects and provides insights about
color distribution patterns.
"""

from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
import tempfile
import os
import cv2
import numpy as np
from collections import defaultdict
import time
from ..core.base import BaseProcessor, ProcessingContext, ProcessingResult, ConfigProtocol
from ..core.config import BaseConfig, AlertConfig
from ..utils import (
    filter_by_confidence, 
    filter_by_categories, 
    apply_category_mapping, 
    match_results_structure,
    extract_major_colors
)


@dataclass
class ColorDetectionConfig(BaseConfig):
    """Configuration for color detection use case."""
    
    # Detection settings
    confidence_threshold: float = 0.5
    
    # Color analysis settings
    top_k_colors: int = 3
    frame_skip: int = 1
    
    # Category settings
    target_categories: Optional[List[str]] = field(default_factory=lambda: [
        "person", "people", "car", "cars", "truck", "trucks", "motorcycle", "motorcycles", "vehicle", "vehicles", "bus", "bicycle"
    ])
    
    # Video processing settings
    fps: Optional[float] = None
    bbox_format: str = "auto"
    
    # Category mapping
    index_to_category: Optional[Dict[int, str]] = None
    
    # Alert configuration
    alert_config: Optional[AlertConfig] = None
    
    # Time window configuration
    time_window_minutes: int = 60
    enable_unique_counting: bool = True

    def validate(self) -> List[str]:
        """Validate configuration parameters."""
        errors = super().validate()
        
        if self.confidence_threshold < 0 or self.confidence_threshold > 1:
            errors.append("confidence_threshold must be between 0 and 1")
            
        if self.top_k_colors <= 0:
            errors.append("top_k_colors must be positive")
            
        if self.frame_skip <= 0:
            errors.append("frame_skip must be positive")
            
        if self.bbox_format not in ["auto", "xmin_ymin_xmax_ymax", "x_y_width_height"]:
            errors.append("bbox_format must be one of: auto, xmin_ymin_xmax_ymax, x_y_width_height")
            
        return errors


class ColorDetectionUseCase(BaseProcessor):
    """Color detection processor for analyzing object colors in video streams."""
    
    def __init__(self):
        super().__init__("color_detection")
        self.category = "visual_appearance"
        
    def get_config_schema(self) -> Dict[str, Any]:
        """Get JSON schema for configuration validation."""
        return {
            "type": "object",
            "properties": {
                "confidence_threshold": {"type": "number", "minimum": 0.0, "maximum": 1.0, "default": 0.5},
                "top_k_colors": {"type": "integer", "minimum": 1, "default": 3},
                "frame_skip": {"type": "integer", "minimum": 1, "default": 1},
                "target_categories": {"type": ["array", "null"], "items": {"type": "string"}, "default": [
                    "person", "people", "car", "cars", "truck", "trucks", "motorcycle", "motorcycles", "vehicle", "vehicles", "bus", "bicycle"
                ]},
                "fps": {"type": ["number", "null"], "minimum": 1.0, "default": None},
                "bbox_format": {"type": "string", "enum": ["auto", "xmin_ymin_xmax_ymax", "x_y_width_height"], "default": "auto"},
                "index_to_category": {"type": ["object", "null"], "default": None},
                "alert_config": {"type": ["object", "null"], "default": None}
            },
            "required": ["confidence_threshold", "top_k_colors"],
            "additionalProperties": False
        }
        
    def create_default_config(self, **overrides) -> ColorDetectionConfig:
        """Create default configuration with optional overrides."""
        defaults = {
            "category": self.category,
            "usecase": self.name,
            "confidence_threshold": 0.5,
            "top_k_colors": 3,
            "frame_skip": 1,
            "target_categories": [
                "person", "people", "car", "cars", "truck", "trucks", 
                "motorcycle", "motorcycles", "vehicle", "vehicles", "bus", "bicycle"
            ],
            "fps": None,
            "bbox_format": "auto",
            "index_to_category": None,
            "alert_config": None
        }
        defaults.update(overrides)
        return ColorDetectionConfig(**defaults)
        
    def process(
        self,
        data: Any, 
        config: ConfigProtocol,
        input_bytes: Optional[bytes] = None,
        context: Optional[ProcessingContext] = None
    ) -> ProcessingResult:
        """
        Process color detection use case.
        
        Args:
            data: Raw model output (detection or tracking format)
            config: Color detection configuration
            input_bytes: Video or image bytes for color analysis
            context: Processing context
            
        Returns:
            ProcessingResult: Processing result with color detection analytics
        """
        start_time = time.time()
        
        try:
            # Ensure we have the right config type
            if not isinstance(config, ColorDetectionConfig):
                return self.create_error_result(
                    "Invalid configuration type for color detection",
                    usecase=self.name,
                    category=self.category,
                    context=context
                )
            
            # Initialize processing context if not provided
            if context is None:
                context = ProcessingContext()
            
            # Validate required inputs
            if not input_bytes:
                return self.create_error_result(
                    "input_bytes (video/image) is required for color detection",
                    usecase=self.name,
                    category=self.category,
                    context=context
                )
            
            if not data:
                return self.create_error_result(
                    "Detection data is required for color detection",
                    usecase=self.name,
                    category=self.category,
                    context=context
                )
            
            # Detect input format
            input_format = match_results_structure(data)
            context.input_format = input_format
            context.confidence_threshold = config.confidence_threshold
            
            self.logger.info(f"Processing color detection with format: {input_format.value}")
            
            # Step 1: Apply confidence filtering
            processed_data = data
            if config.confidence_threshold is not None:
                processed_data = filter_by_confidence(processed_data, config.confidence_threshold)
                self.logger.debug(f"Applied confidence filtering with threshold {config.confidence_threshold}")
            
            # Step 2: Apply category mapping if provided
            if config.index_to_category:
                processed_data = apply_category_mapping(processed_data, config.index_to_category)
                self.logger.debug("Applied category mapping")
            
            # Step 2.5: Filter to only include target categories
            color_processed_data = processed_data
            if config.target_categories:
                color_processed_data = filter_by_categories(processed_data.copy(), config.target_categories)
                self.logger.debug(f"Applied target category filtering for: {config.target_categories}")
            
            # Step 3: Analyze colors in media (video or image)
            color_analysis = self._analyze_colors_in_media(
                color_processed_data, 
                input_bytes, 
                config
            )
            
            # Step 4: Calculate comprehensive summaries
            color_summary = self._calculate_color_summary(color_analysis, config)
            general_summary = self._calculate_general_summary(processed_data, config)
            
            # Step 5: Generate insights and alerts
            insights = self._generate_insights(color_summary, config)
            alerts = self._check_alerts(color_summary, config)
            
            # Step 6: Calculate detailed metrics
            metrics = self._calculate_metrics(color_analysis, color_summary, config, context)
            
            # Step 7: Extract predictions for API compatibility
            predictions = self._extract_predictions(color_analysis, config)
            
            # Step 8: Generate human-readable summary
            summary = self._generate_summary(color_summary, general_summary, alerts)
            
            # Step 9: Generate structured events and tracking stats
            events = self._generate_events(color_summary, alerts, config)
            tracking_stats = self._generate_tracking_stats(color_summary, insights, summary, config)
            
            # Mark processing as completed
            context.mark_completed()
            
            # Create successful result
            result = self.create_result(
                data={
                    "color_analysis": color_analysis,
                    "color_summary": color_summary,
                    "general_summary": general_summary,
                    "alerts": alerts,
                    "total_detections": len(color_analysis),
                    "unique_colors": len(color_summary.get("color_distribution", {})),
                    "events": events,
                    "tracking_stats": tracking_stats
                },
                usecase=self.name,
                category=self.category,
                context=context
            )
            
            # Add human-readable information
            result.summary = summary
            result.insights = insights
            result.predictions = predictions
            result.metrics = metrics
            
            # Add warnings for low confidence detections
            if config.confidence_threshold and config.confidence_threshold < 0.3:
                result.add_warning(f"Low confidence threshold ({config.confidence_threshold}) may result in false positives")
            
            processing_time = context.processing_time or time.time() - start_time
            self.logger.info(f"Color detection completed successfully in {processing_time:.2f}s")
            return result
            
        except Exception as e:
            self.logger.error(f"Color detection failed: {str(e)}", exc_info=True)
            
            if context:
                context.mark_completed()
            
            return self.create_error_result(
                str(e), 
                type(e).__name__,
                usecase=self.name,
                category=self.category,
                context=context
            )
            
    def _analyze_colors_in_media(
        self, 
        data: Any, 
        media_bytes: bytes, 
        config: ColorDetectionConfig
    ) -> List[Dict[str, Any]]:
        """Analyze colors of detected objects in video frames or images."""
        
        # Determine if input is video or image
        is_video = self._is_video_bytes(media_bytes)
        
        if is_video:
            return self._analyze_colors_in_video(data, media_bytes, config)
        else:
            return self._analyze_colors_in_image(data, media_bytes, config)
    
    def _is_video_bytes(self, media_bytes: bytes) -> bool:
        """Determine if bytes represent a video file."""
        # Check common video file signatures
        video_signatures = [
            b'\x00\x00\x00\x20ftypmp4',  # MP4
            b'\x00\x00\x00\x18ftypmp4',  # MP4 variant
            b'RIFF',  # AVI
            b'\x1aE\xdf\xa3',  # MKV/WebM
            b'ftyp',  # General MP4 family
        ]
        
        for signature in video_signatures:
            if media_bytes.startswith(signature) or signature in media_bytes[:50]:
                return True
        return False
    
    def _analyze_colors_in_video(
        self, 
        data: Any, 
        video_bytes: bytes, 
        config: ColorDetectionConfig
    ) -> List[Dict[str, Any]]:
        """Analyze colors of detected objects in video frames."""

        # Save video to temporary file
        with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as temp_video:
            temp_video.write(video_bytes)
            video_path = temp_video.name

        try:
            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                raise RuntimeError("Failed to open video file")

            fps = config.fps or cap.get(cv2.CAP_PROP_FPS)
            color_analysis = []
            frame_id = 0
            seen_track_ids = set()

            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                # Skip frames based on frame_skip setting
                if frame_id % config.frame_skip != 0:
                    frame_id += 1
                    continue

                frame_key = str(frame_id)
                timestamp = frame_id / fps

                # Get detections for this frame
                frame_detections = self._get_frame_detections(data, frame_key)
                if not frame_detections:
                    frame_id += 1
                    continue

                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # Analyze colors for each detection
                for detection in frame_detections:
                    if detection.get("confidence", 1.0) < config.confidence_threshold:
                        continue

                    bbox = detection.get("bounding_box", detection.get("bbox"))
                    if not bbox:
                        continue

                    track_id = detection.get("track_id")
                    if config.enable_unique_counting and track_id is not None:
                        if track_id in seen_track_ids:
                            continue  # Skip if already counted
                        seen_track_ids.add(track_id)

                    # Crop the bounding box region
                    crop = self._crop_bbox(rgb_frame, bbox, config.bbox_format)
                    if crop.size == 0:
                        continue

                    # Extract major colors
                    major_colors = extract_major_colors(crop, k=config.top_k_colors)
                    main_color = major_colors[0][0] if major_colors else "unknown"

                    color_record = {
                        "frame_id": frame_key,
                        "timestamp": round(timestamp, 2),
                        "category": detection.get("category", "unknown"),
                        "confidence": round(detection.get("confidence", 0.0), 3),
                        "main_color": main_color,
                        "major_colors": major_colors,
                        "bbox": bbox,
                        "detection_id": detection.get("id", f"det_{len(color_analysis)}"),
                        "track_id": track_id
                    }
                    color_analysis.append(color_record)

                frame_id += 1

            cap.release()
            return color_analysis

        finally:
            if os.path.exists(video_path):
                os.unlink(video_path)
    
    def _analyze_colors_in_image(
        self, 
        data: Any, 
        image_bytes: bytes, 
        config: ColorDetectionConfig
    ) -> List[Dict[str, Any]]:
        """Analyze colors of detected objects in a single image."""
        
        # Decode image from bytes
        image_array = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
        
        if image is None:
            raise RuntimeError("Failed to decode image from bytes")
        
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        color_analysis = []
        
        # Get detections from data
        detections = self._get_frame_detections(data, "0")  # Use "0" as frame ID for single image
        
        seen_track_ids = set()
        
        for detection in detections:
            if detection.get("confidence", 1.0) < config.confidence_threshold:
                continue

            bbox = detection.get("bounding_box", detection.get("bbox"))
            if not bbox:
                continue

            track_id = detection.get("track_id")
            if config.enable_unique_counting and track_id is not None:
                if track_id in seen_track_ids:
                    continue  # Skip if already counted
                seen_track_ids.add(track_id)

            # Crop the bounding box region
            crop = self._crop_bbox(rgb_image, bbox, config.bbox_format)
            if crop.size == 0:
                continue

            # Extract major colors
            major_colors = extract_major_colors(crop, k=config.top_k_colors)
            main_color = major_colors[0][0] if major_colors else "unknown"

            color_record = {
                "frame_id": "0",
                "timestamp": 0.0,
                "category": detection.get("category", "unknown"),
                "confidence": round(detection.get("confidence", 0.0), 3),
                "main_color": main_color,
                "major_colors": major_colors,
                "bbox": bbox,
                "detection_id": detection.get("id", f"det_{len(color_analysis)}"),
                "track_id": track_id
            }
            color_analysis.append(color_record)
        
        return color_analysis
    
    def _get_frame_detections(self, data: Any, frame_key: str) -> List[Dict[str, Any]]:
        """Extract detections for a specific frame from data."""
        if isinstance(data, dict):
            # Frame-based format
            return data.get(frame_key, [])
        elif isinstance(data, list):
            # List format (single frame or all detections)
            return data
        else:
            return []


                
    def _crop_bbox(self, image: np.ndarray, bbox: Dict[str, Any], bbox_format: str) -> np.ndarray:
        """Crop bounding box region from image."""
        h, w = image.shape[:2]
        
        # Auto-detect bbox format
        if bbox_format == "auto":
            if "xmin" in bbox:
                bbox_format = "xmin_ymin_xmax_ymax"
            elif "x" in bbox:
                bbox_format = "x_y_width_height"
            else:
                return np.zeros((0, 0, 3), dtype=np.uint8)
                
        # Extract coordinates based on format
        if bbox_format == "xmin_ymin_xmax_ymax":
            xmin = max(0, int(bbox["xmin"]))
            ymin = max(0, int(bbox["ymin"]))
            xmax = min(w, int(bbox["xmax"]))
            ymax = min(h, int(bbox["ymax"]))
        elif bbox_format == "x_y_width_height":
            xmin = max(0, int(bbox["x"]))
            ymin = max(0, int(bbox["y"]))
            xmax = min(w, int(bbox["x"] + bbox["width"]))
            ymax = min(h, int(bbox["y"] + bbox["height"]))
        else:
            return np.zeros((0, 0, 3), dtype=np.uint8)
            
        return image[ymin:ymax, xmin:xmax]
        
    def _calculate_color_summary(self, color_analysis: List[Dict], config: ColorDetectionConfig) -> Dict[str, Any]:
        """Calculate color distribution summary."""
        
        # Group by category and color
        category_colors = defaultdict(lambda: defaultdict(int))
        total_detections = len(color_analysis)
        
        for record in color_analysis:
            category = record["category"]
            main_color = record["main_color"]
            category_colors[category][main_color] += 1
            
        # Calculate summary statistics
        summary = {
            "total_detections": total_detections,
            "categories": dict(category_colors),
            "color_distribution": {},
            "dominant_colors": {}
        }
        
        # Calculate overall color distribution
        all_colors = defaultdict(int)
        for category_data in category_colors.values():
            for color, count in category_data.items():
                all_colors[color] += count
                
        summary["color_distribution"] = dict(all_colors)
        
        # Find dominant color per category
        for category, colors in category_colors.items():
            if colors:
                dominant_color = max(colors.items(), key=lambda x: x[1])
                summary["dominant_colors"][category] = {
                    "color": dominant_color[0],
                    "count": dominant_color[1],
                    "percentage": round((dominant_color[1] / sum(colors.values())) * 100, 1)
                }
                
        return summary
        
    def _calculate_general_summary(self, processed_data: Any, config: ColorDetectionConfig) -> Dict[str, Any]:
        """Calculate general detection summary."""
        
        # Count objects by category
        category_counts = defaultdict(int)
        total_objects = 0
        
        if isinstance(processed_data, dict):
            # Frame-based format
            for frame_data in processed_data.values():
                if isinstance(frame_data, list):
                    for detection in frame_data:
                        if detection.get("confidence", 1.0) >= config.confidence_threshold:
                            category = detection.get("category", "unknown")
                            category_counts[category] += 1
                            total_objects += 1
        elif isinstance(processed_data, list):
            # List format
            for detection in processed_data:
                if detection.get("confidence", 1.0) >= config.confidence_threshold:
                    category = detection.get("category", "unknown")
                    category_counts[category] += 1
                    total_objects += 1
                        
        return {
            "total_objects": total_objects,
            "category_counts": dict(category_counts),
            "categories_detected": list(category_counts.keys())
        }
        
    def _generate_insights(self, color_summary: Dict, config: ColorDetectionConfig) -> List[str]:
        """Generate insights from color analysis."""
        insights = []

        total_detections = color_summary.get("total_detections", 0)
        if total_detections == 0:
            insights.append("No objects detected for color analysis.")
            return insights

        categories = color_summary.get("categories", {})
        dominant_colors = color_summary.get("dominant_colors", {})
        color_distribution = color_summary.get("color_distribution", {})

        # Per-category color insights
        for category, colors in categories.items():
            total = sum(colors.values())
            color_details = ", ".join([f"{color}: {count}" for color, count in colors.items()])
            insights.append(f"{category.capitalize()} colors: {color_details} (Total: {total})")

        # Dominant color summary per category
        for category, info in dominant_colors.items():
            insights.append(
                f"{category.capitalize()} is mostly {info['color']} "
                f"({info['count']} detections, {info['percentage']}%)"
            )

        # Color diversity insights
        unique_colors = len(color_distribution)
        if unique_colors > 1:
            insights.append(f"Detected {unique_colors} unique colors across all categories.")

        # Most common color overall
        if color_distribution:
            most_common_color = max(color_distribution.items(), key=lambda x: x[1])
            insights.append(
                f"Most common color overall: {most_common_color[0]} ({most_common_color[1]} detections)"
            )

        return insights

        
    def _check_alerts(self, color_summary: Dict, config: ColorDetectionConfig) -> List[Dict]:
        """Check for alert conditions."""
        alerts = []
        
        if not config.alert_config:
            return alerts
            
        total_detections = color_summary.get("total_detections", 0)
        
        # Count threshold alerts
        if config.alert_config.count_thresholds:
            for category, threshold in config.alert_config.count_thresholds.items():
                if category == "all" and total_detections >= threshold:
                    alerts.append({
                        "type": "count_threshold",
                        "severity": "warning",
                        "message": f"Total detections ({total_detections}) exceeds threshold ({threshold})",
                        "category": category,
                        "current_count": total_detections,
                        "threshold": threshold,
                        "timestamp": datetime.now().isoformat()
                    })
                elif category in color_summary.get("categories", {}):
                    category_total = sum(color_summary["categories"][category].values())
                    if category_total >= threshold:
                        alerts.append({
                            "type": "count_threshold",
                            "severity": "warning", 
                            "message": f"{category} detections ({category_total}) exceeds threshold ({threshold})",
                            "category": category,
                            "current_count": category_total,
                            "threshold": threshold,
                            "timestamp": datetime.now().isoformat()
                        })
                        
        return alerts
        
    def _calculate_metrics(self, color_analysis: List[Dict], color_summary: Dict, config: ColorDetectionConfig, context: ProcessingContext) -> Dict[str, Any]:
        """Calculate detailed metrics for analytics."""
        total_detections = len(color_analysis)
        unique_colors = len(color_summary.get("color_distribution", {}))
        
        metrics = {
            "total_detections": total_detections,
            "unique_colors": unique_colors,
            "categories_analyzed": len(color_summary.get("categories", {})),
            "processing_time": context.processing_time or 0.0,
            "input_format": context.input_format.value,
            "confidence_threshold": config.confidence_threshold,
            "color_diversity": 0.0,
            "detection_rate": 0.0,
            "average_colors_per_detection": config.top_k_colors
        }
        
        # Calculate color diversity
        if total_detections > 0:
            metrics["color_diversity"] = (unique_colors / total_detections) * 100
        
        # Calculate detection rate
        if config.time_window_minutes and config.time_window_minutes > 0:
            metrics["detection_rate"] = (total_detections / config.time_window_minutes) * 60
        
        # Per-category metrics
        if color_summary.get("categories"):
            category_metrics = {}
            for category, colors in color_summary["categories"].items():
                category_total = sum(colors.values())
                category_metrics[category] = {
                    "count": category_total,
                    "unique_colors": len(colors),
                    "color_diversity": (len(colors) / category_total) * 100 if category_total > 0 else 0
                }
            metrics["category_metrics"] = category_metrics
        
        # Processing settings
        metrics["processing_settings"] = {
            "confidence_threshold": config.confidence_threshold,
            "top_k_colors": config.top_k_colors,
            "frame_skip": config.frame_skip,
            "target_categories": config.target_categories,
            "enable_unique_counting": config.enable_unique_counting
        }
        
        return metrics
        
    def _extract_predictions(self, color_analysis: List[Dict], config: ColorDetectionConfig) -> List[Dict]:
        """Extract predictions in standard format."""
        
        predictions = []
        for record in color_analysis:
            prediction = {
                "category": record["category"],
                "confidence": record["confidence"],
                "bbox": record["bbox"],
                "frame_id": record["frame_id"],
                "timestamp": record["timestamp"],
                "main_color": record["main_color"],
                "major_colors": record["major_colors"]
            }
            if "detection_id" in record:
                prediction["id"] = record["detection_id"]
            predictions.append(prediction)
            
        return predictions
    
    def _generate_summary(self, color_summary: Dict, general_summary: Dict, alerts: List) -> str:
        """Generate human-readable summary."""
        total_detections = color_summary.get("total_detections", 0)
        unique_colors = len(color_summary.get("color_distribution", {}))
        
        if total_detections == 0:
            return "No objects detected for color analysis"
        
        summary_parts = [f"{total_detections} objects analyzed for colors"]
        
        if unique_colors > 0:
            summary_parts.append(f"{unique_colors} unique colors detected")
        
        categories = color_summary.get("categories", {})
        if len(categories) > 1:
            summary_parts.append(f"across {len(categories)} categories")
        
        if alerts:
            alert_count = len(alerts)
            summary_parts.append(f"with {alert_count} alert{'s' if alert_count != 1 else ''}")
        
        return ", ".join(summary_parts)
    
    def _generate_events(self, color_summary: Dict, alerts: List, config: ColorDetectionConfig) -> List[Dict]:
        """Generate structured events for the output format."""
        from datetime import datetime, timezone
        
        events = []
        total_detections = color_summary.get("total_detections", 0)
        unique_colors = len(color_summary.get("color_distribution", {}))
        
        if total_detections > 0:
            # Determine event level based on thresholds
            level = "info"
            intensity = 5.0
            
            if config.alert_config and config.alert_config.count_thresholds:
                threshold = config.alert_config.count_thresholds.get("all", 20)
                intensity = min(10.0, (total_detections / threshold) * 10)
                
                if intensity >= 7:
                    level = "critical"
                elif intensity >= 5:
                    level = "warning"
                else:
                    level = "info"
            else:
                if total_detections > 50:
                    level = "critical"
                    intensity = 9.0
                elif total_detections > 25:
                    level = "warning" 
                    intensity = 7.0
                else:
                    level = "info"
                    intensity = min(10.0, total_detections / 5.0)
            
            # Main color detection event
            event = {
                "type": "color_detection",
                "stream_time": datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S UTC"),
                "level": level,
                "intensity": round(intensity, 1),
                "config": {
                    "min_value": 0,
                    "max_value": 10,
                    "level_settings": {"info": 2, "warning": 5, "critical": 7}
                },
                "application_name": "Color Detection System",
                "application_version": "1.2",
                "location_info": None,
                # "human_text": f"Event: Color Detection\nLevel: {level.title()}\nTime: {datetime.now(timezone.utc).strftime('%Y-%m-%d-%H:%M:%S UTC')}\nDetections: {total_detections} objects analyzed\nColors: {unique_colors} unique colors detected\nIntensity: {intensity:.1f}/10"
            }
            if level == "critical":  
                event["human_text"] = (
                    f"Event: Color Detection\nLevel: {level.title()}\nTime: {datetime.now(timezone.utc).strftime('%Y-%m-%d-%H:%M:%S UTC')}\nDetections: {total_detections} objects analyzed\nColors: {unique_colors} unique colors detected\nIntensity: {intensity:.1f}/10"
                )
            else:
                event["human_text"] = (
                    f""
                )
            events.append(event)
        
        # Add category-specific events if multiple categories
        categories = color_summary.get("categories", {})
        if len(categories) > 1:
            for category, colors in categories.items():
                category_total = sum(colors.values())
                if category_total > 0:
                    category_intensity = min(10.0, category_total / 10.0)
                    category_level = "info"
                    if category_intensity >= 7:
                        category_level = "warning"
                    elif category_intensity >= 5:
                        category_level = "info"
                    
                    # Find dominant color for this category
                    dominant_color = max(colors.items(), key=lambda x: x[1])[0] if colors else "unknown"
                    
                    category_event = {
                        "type": "color_category_analysis",
                        "stream_time": datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S UTC"),
                        "level": category_level,
                        "intensity": round(category_intensity, 1),
                        "config": {
                            "min_value": 0,
                            "max_value": 10,
                            "level_settings": {"info": 2, "warning": 5, "critical": 7}
                        },
                        "application_name": "Color Category Analysis System",
                        "application_version": "1.2",
                        "location_info": category,
                        "human_text": f"Category: {category}\nCount: {category_total} objects\n color: {dominant_color}",
                    }
                    events.append(category_event)
        
        # Add alert events
        for alert in alerts:
            alert_event = {
                "type": alert.get("type", "color_alert"),
                "stream_time": datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S UTC"),
                "level": alert.get("severity", "warning"),
                "intensity": 8.0,
                "config": {
                    "min_value": 0,
                    "max_value": 10,
                    "level_settings": {"info": 2, "warning": 5, "critical": 7}
                },
                "application_name": "Color Detection Alert System",
                "application_version": "1.2",
                "location_info": None,
                "human_text": f"Event: {alert.get('type', 'Color Alert').title()}\nMessage: {alert.get('message', 'Color detection alert triggered')}"
            }
            events.append(alert_event)
        
        return events
    
    def _generate_tracking_stats(self, color_summary: Dict, insights: List[str], summary: str, config: ColorDetectionConfig) -> List[Dict]:
        """Generate structured tracking stats for the output format."""
        from datetime import datetime, timezone
        
        tracking_stats = []
        total_detections = color_summary.get("total_detections", 0)
        
        if total_detections > 0:
            # Create main tracking stats entry
            tracking_stat = {
                "tracking_start_time": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
                "all_results_for_tracking": {
                    "total_detections": total_detections,
                    "color_summary": color_summary,
                    "detection_rate": (total_detections / config.time_window_minutes * 60) if config.time_window_minutes else 0,
                    "unique_colors": len(color_summary.get("color_distribution", {})),
                    "categories_analyzed": len(color_summary.get("categories", {})),
                    "dominant_colors": color_summary.get("dominant_colors", {}),
                    "color_diversity": len(color_summary.get("color_distribution", {})) / total_detections * 100 if total_detections > 0 else 0
                },
                "human_text": self._generate_human_text_for_tracking(total_detections, color_summary, insights, summary, config)
            }
            tracking_stats.append(tracking_stat)
        
        return tracking_stats
    
    def _generate_human_text_for_tracking(self, total_detections: int, color_summary: Dict, insights: List[str], summary: str, config: ColorDetectionConfig) -> str:
        """Generate human-readable text for tracking stats."""
        from datetime import datetime, timezone
        
        text_parts = [
            #f"Tracking Start Time: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M')}",
            #f"Objects Analyzed: {total_detections}"
        ]
        
        if config.time_window_minutes:
            detection_rate_per_hour = (total_detections / config.time_window_minutes) * 60
            #text_parts.append(f"Detection Rate: {detection_rate_per_hour:.1f} objects per hour")
        
        # Add color statistics
        unique_colors = len(color_summary.get("color_distribution", {}))
        #text_parts.append(f"Unique Colors Detected: {unique_colors}")
        
        if total_detections > 0:
            color_diversity = (unique_colors / total_detections) * 100
            #text_parts.append(f"Color Diversity: {color_diversity:.1f}%")
        
        # Add category breakdown
        categories = color_summary.get("categories", {})
        if categories:
            #text_parts.append(f"Categories Analyzed: {len(categories)}")
            for category, colors in categories.items():
                category_total = sum(colors.values())
                if category_total > 0:
                    dominant_color = max(colors.items(), key=lambda x: x[1])[0] if colors else "unknown"
                    text_parts.append(f"  {category_total} {category.title()} detected, Color: {dominant_color}")
        
        # Add color distribution summary
        color_distribution = color_summary.get("color_distribution", {})
        if color_distribution:
            top_colors = sorted(color_distribution.items(), key=lambda x: x[1], reverse=True)[:3]
            #text_parts.append("Top Colors:")
            for color, count in top_colors:
                percentage = (count / total_detections) * 100
                #text_parts.append(f"  {color.title()}: {count} objects ({percentage:.1f}%)")
        
        # Add key insights
        # if insights:
        #     text_parts.append("Key Color Insights:")
        #     for insight in insights[:3]:  # Limit to first 3 insights
        #         text_parts.append(f"  - {insight}")
        
        return "\n".join(text_parts)
