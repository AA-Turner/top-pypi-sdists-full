"""
Pothole Segmentation use case implementation.

This module provides a structured implementation for pothole segmentation
with mask and bounding box-based analysis, insights, alerts, and tracking.
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
import time

from ..core.base import (
    BaseProcessor,
    ProcessingContext,
    ProcessingResult,
    ConfigProtocol,
)
from ..core.config import BaseConfig, AlertConfig
from ..utils import (
    filter_by_confidence,
    apply_category_mapping,
    calculate_counting_summary,
    match_results_structure,
    bbox_smoothing,
    BBoxSmoothingConfig,
    BBoxSmoothingTracker
)


@dataclass
class PotholeConfig(BaseConfig):
    confidence_threshold: float = 0.5
    pothole_categories: List[str] = field(default_factory=lambda: ["pothole"])
    alert_config: Optional[AlertConfig] = None
    time_window_minutes: int = 60
    enable_unique_counting: bool = True

    index_to_category: Optional[Dict[int, str]] = field(
        default_factory=lambda: {0: "pothole"}
    )

    # BBox smoothing (optional)
    enable_smoothing: bool = False
    smoothing_algorithm: str = "linear"
    smoothing_window_size: int = 5
    smoothing_cooldown_frames: int = 10
    smoothing_confidence_range_factor: float = 0.2

    # New: mask-based area analysis toggle
    enable_mask_analysis: bool = True

    def __post_init__(self):
        if not (0.0 <= self.confidence_threshold <= 1.0):
            raise ValueError("confidence_threshold must be between 0.0 and 1.0")

        self.pothole_categories = [cat.lower() for cat in self.pothole_categories]
        if self.index_to_category:
            self.index_to_category = {k: v.lower() for k, v in self.index_to_category.items()}


class PotholeSegmentationUseCase(BaseProcessor):
    def __init__(self):
        super().__init__("pothole_segmentation")
        self.category = "infrastructure"
        self.smoothing_tracker = None
        self._pothole_recent_history = []

    def get_config_schema(self) -> Dict[str, Any]:
        """Get configuration schema for pothole segmentation."""
        return {
            "type": "object",
            "properties": {
                "confidence_threshold": {
                    "type": "number",
                    "minimum": 0.0,
                    "maximum": 1.0,
                    "default": 0.5,
                    "description": "Minimum confidence threshold for detections",
                },
                "pothole_categories": {
                    "type": "array",
                    "items": {"type": "string"},
                    "default": ["pothole"],
                    "description": "Category names that represent potholes",
                },
                "index_to_category": {
                    "type": "object",
                    "additionalProperties": {"type": "string"},
                    "description": "Mapping from category indices to names",
                },
                "alert_config": {
                    "type": "object",
                    "properties": {
                        "count_thresholds": {
                            "type": "object",
                            "additionalProperties": {"type": "integer", "minimum": 1},
                            "description": "Count thresholds for alerts",
                        }
                    },
                },
            },
            "required": ["confidence_threshold"],
            "additionalProperties": False,
        }

    def create_default_config(self, **overrides) -> PotholeConfig:
        """Create default configuration with optional overrides."""
        defaults = {
            "category": self.category,
            "usecase": self.name,
            "confidence_threshold": 0.5,
            "pothole_categories": ["pothole"],
        }
        defaults.update(overrides)
        return PotholeConfig(**defaults)

    def process(
            self,
            data: Any,
            config: ConfigProtocol,
            context: Optional[ProcessingContext] = None,
            stream_info: Optional[Dict[str, Any]] = None
    ) -> ProcessingResult:
        """
        Process pothole segmentation use case.
        """
        start_time = time.time()

        try:
            # Step 0: Validate config
            if not isinstance(config, PotholeConfig):
                return self.create_error_result(
                    "Invalid configuration type for pothole segmentation",
                    usecase=self.name,
                    category=self.category,
                    context=context,
                )

            # Step 1: Init context
            if context is None:
                context = ProcessingContext()
            input_format = match_results_structure(data)
            context.input_format = input_format
            context.confidence_threshold = config.confidence_threshold
            self.logger.info(f"Processing pothole segmentation with format: {input_format.value}")

            # Step 2: Preprocessing
            processed_data = self._preprocess_data(data, config)

            # Step 3: BBox smoothing (optional)
            if config.enable_smoothing:
                processed_data = self._apply_bbox_smoothing(processed_data, config)

            # Step 4: Summary generation
            pothole_summary = self._calculate_pothole_summary(processed_data, config)
            general_summary = calculate_counting_summary(processed_data)

            # Step 5: Insights and alerts
            insights = self._generate_insights(pothole_summary, config)
            alerts = self._check_alerts(pothole_summary, config)

            # Step 6: Metrics
            metrics = self._calculate_metrics(pothole_summary, config, context)

            # Step 7: Predictions
            predictions = self._extract_predictions(processed_data, config)

            # Step 8: Human-readable summary
            summary_text = self._generate_summary(pothole_summary, general_summary, alerts)

            # Step 9: Frame number
            frame_number = self._extract_frame_number(stream_info)

            # Step 10: Events and tracking
            events = self._generate_events(pothole_summary, alerts, config, frame_number)
            tracking_stats = self._generate_tracking_stats(
                pothole_summary, insights, summary_text, config, frame_number, stream_info
            )

            # Finalize and return result
            context.processing_time = time.time() - start_time
            context.mark_completed()

            result = self.create_result(
                data={
                    "pothole_summary": pothole_summary,
                    "general_counting_summary": general_summary,
                    "alerts": alerts,
                    "total_pothole_detections": pothole_summary.get("total_objects", 0),
                    "events": events,
                    "tracking_stats": tracking_stats,
                },
                usecase=self.name,
                category=self.category,
                context=context,
            )

            result.summary = summary_text
            result.insights = insights
            result.predictions = predictions
            result.metrics = metrics
            return result

        except Exception as e:
            self.logger.error(f"Error in pothole segmentation processing: {str(e)}")
            return self.create_error_result(
                f"Pothole segmentation processing failed: {str(e)}",
                error_type="PotholeProcessingError",
                usecase=self.name,
                category=self.category,
                context=context,
            )

    def _preprocess_data(self, data: Any, config: PotholeConfig) -> List[Dict[str, Any]]:
        """
        Apply confidence filtering and category mapping to raw detections.
        """
        processed_data = data

        if config.confidence_threshold is not None:
            processed_data = filter_by_confidence(processed_data, config.confidence_threshold)
            self.logger.debug(f"Applied confidence filtering: threshold = {config.confidence_threshold}")

        if config.index_to_category:
            processed_data = apply_category_mapping(processed_data, config.index_to_category)
            self.logger.debug("Applied index-to-category mapping")

        return processed_data

    def _apply_bbox_smoothing(self, data: List[Dict[str, Any]], config: PotholeConfig) -> List[Dict[str, Any]]:
        """
        Apply bounding box smoothing to pothole detections.
        """
        if self.smoothing_tracker is None:
            smoothing_config = BBoxSmoothingConfig(
                smoothing_algorithm=config.smoothing_algorithm,
                window_size=config.smoothing_window_size,
                cooldown_frames=config.smoothing_cooldown_frames,
                confidence_threshold=config.confidence_threshold,
                confidence_range_factor=config.smoothing_confidence_range_factor,
                enable_smoothing=True
            )
            self.smoothing_tracker = BBoxSmoothingTracker(smoothing_config)

        pothole_detections = [d for d in data if d.get("category", "").lower() == "pothole"]
        non_pothole_detections = [d for d in data if d.get("category", "").lower() != "pothole"]

        smoothed_detections = bbox_smoothing(
            pothole_detections,
            self.smoothing_tracker.config,
            self.smoothing_tracker
        )

        self.logger.debug("Applied bbox smoothing to pothole detections")
        return non_pothole_detections + smoothed_detections

    def _calculate_pothole_summary(self, data: List[Dict[str, Any]], config: PotholeConfig) -> Dict[str, Any]:
        """
        Calculate summary statistics for pothole detections.
        """
        if not isinstance(data, list):
            return {"total_objects": 0, "by_category": {}, "detections": []}

        valid_category = "pothole"

        detections = [
            det for det in data
            if det.get("category", "").lower() == valid_category
        ]

        summary = {
            "total_objects": len(detections),
            "by_category": {
                valid_category: len(detections)
            },
            "detections": detections,
        }

        return summary

    def _generate_insights(self, summary: Dict[str, Any], config: PotholeConfig) -> List[str]:
        """
        Generate high-level insights for pothole detection.
        """
        insights = []

        total = summary.get("total_objects", 0)
        detections = summary.get("detections", [])

        if total == 0:
            insights.append("EVENT: No potholes detected in the scene")
        else:
            insights.append(f"EVENT: {total} pothole{'s' if total != 1 else ''} detected")

            # Calculate area covered using bounding boxes
            total_area = 0.0
            for det in detections:
                bbox = det.get("bounding_box") or det.get("bbox")
                if bbox:
                    xmin = bbox.get("xmin")
                    ymin = bbox.get("ymin")
                    xmax = bbox.get("xmax")
                    ymax = bbox.get("ymax")
                    if None not in (xmin, ymin, xmax, ymax):
                        width = xmax - xmin
                        height = ymax - ymin
                        if width > 0 and height > 0:
                            total_area += width * height

            threshold_area = 10000.0  # Same base threshold as fire/smoke
            intensity_pct = min(100.0, (total_area / threshold_area) * 100)

            if intensity_pct < 20:
                insights.append(f"SEVERITY: Low pothole spread ({intensity_pct:.1f}% area)")
            elif intensity_pct <= 50:
                insights.append(f"SEVERITY: Moderate pothole spread ({intensity_pct:.1f}% area)")
            elif intensity_pct <= 80:
                insights.append(f"SEVERITY: High pothole spread ({intensity_pct:.1f}% area)")
            else:
                insights.append(f"SEVERITY: Severe pothole damage — critical zone ({intensity_pct:.1f}% area)")

        return insights

    def _check_alerts(self, summary: Dict[str, Any], config: PotholeConfig) -> List[Dict[str, Any]]:
        """
        Raise alerts if potholes detected with severity based on area spread.
        """
        alerts = []

        total = summary.get("total_objects", 0)
        detections = summary.get("detections", [])

        if total == 0:
            return []

        # Calculate total bbox area
        total_area = 0.0
        for det in detections:
            bbox = det.get("bounding_box") or det.get("bbox")
            if bbox:
                xmin = bbox.get("xmin")
                ymin = bbox.get("ymin")
                xmax = bbox.get("xmax")
                ymax = bbox.get("ymax")
                if None not in (xmin, ymin, xmax, ymax):
                    width = xmax - xmin
                    height = ymax - ymin
                    if width > 0 and height > 0:
                        total_area += width * height

        threshold_area = 10000.0
        intensity_pct = min(100.0, (total_area / threshold_area) * 100)

        # Severity levels (same as fire/smoke)
        if intensity_pct > 80:
            severity = "critical"
        elif intensity_pct > 50:
            severity = "warning"
        else:
            severity = "info"

        alert = {
            "type": "pothole_alert",
            "message": f"{total} pothole detection{'s' if total != 1 else ''} with area coverage {intensity_pct:.1f}%",
            "severity": severity,
            "detected_potholes": total,
        }

        alerts.append(alert)
        return alerts

    def _calculate_metrics(
            self,
            summary: Dict[str, Any],
            config: PotholeConfig,
            context: ProcessingContext
    ) -> Dict[str, Any]:
        """
        Calculate detailed metrics for pothole detection analytics.
        """
        total = summary.get("total_objects", 0)
        detections = summary.get("detections", [])

        metrics = {
            "total_detections": total,
            "processing_time": context.processing_time or 0.0,
            "confidence_threshold": config.confidence_threshold,
            "intensity_percentage": 0.0,
            "damage_level": "unknown",
        }

        # Total area calculation (using bbox)
        total_area = 0.0
        for det in detections:
            bbox = det.get("bounding_box") or det.get("bbox")
            if bbox:
                xmin = bbox.get("xmin")
                ymin = bbox.get("ymin")
                xmax = bbox.get("xmax")
                ymax = bbox.get("ymax")
                if None not in (xmin, ymin, xmax, ymax):
                    width = xmax - xmin
                    height = ymax - ymin
                    if width > 0 and height > 0:
                        total_area += width * height

        threshold_area = 10000.0
        intensity_pct = min(100.0, (total_area / threshold_area) * 100)
        metrics["intensity_percentage"] = intensity_pct

        # Label based on thresholds
        if intensity_pct < 20:
            metrics["damage_level"] = "low"
        elif intensity_pct < 50:
            metrics["damage_level"] = "moderate"
        elif intensity_pct < 80:
            metrics["damage_level"] = "high"
        else:
            metrics["damage_level"] = "critical"

        return metrics

    def _extract_predictions(self, data: Any, config: PotholeConfig) -> List[Dict[str, Any]]:
        """
        Extract predictions from processed data including masks for segmentation.
        """
        predictions = []

        try:
            if isinstance(data, list):
                for item in data:
                    if isinstance(item, dict):
                        prediction = {
                            "category": item.get("category", item.get("class", "unknown")),
                            "confidence": item.get("confidence", item.get("score", 0.0)),
                            "bounding_box": item.get("bounding_box", item.get("bbox", {})),
                            "mask": item.get("mask", item.get("masks", None))  # Accept either key
                        }
                        predictions.append(prediction)
        except Exception as e:
            self.logger.warning(f"Failed to extract predictions: {str(e)}")

        return predictions

    def _generate_summary(
            self, summary: Dict, general_summary: Dict, alerts: List
    ) -> str:
        """
        Generate human-readable summary for pothole detection.
        """
        total = summary.get("total_objects", 0)

        if total == 0:
            return "No potholes detected"

        summary_parts = []

        summary_parts.append(
            f"{total} pothole{'s' if total != 1 else ''} detected"
        )

        if alerts:
            alert_count = len(alerts)
            summary_parts.append(
                f"{alert_count} alert{'s' if alert_count != 1 else ''}"
            )

        return ", ".join(summary_parts)

    def _generate_events(
            self,
            summary: Dict,
            alerts: List[Dict],
            config: PotholeConfig,
            frame_number: Optional[int] = None
    ) -> Dict:
        """
        Generate structured events for pothole detection output with frame-aware keys.
        """
        from datetime import datetime, timezone

        frame_key = str(frame_number) if frame_number is not None else "current_frame"
        events = {frame_key: []}
        frame_events = events[frame_key]

        total = summary.get("total_objects", 0)
        detections = summary.get("detections", [])

        if total > 0:
            # Total area via bbox
            total_area = 0.0
            for det in detections:
                bbox = det.get("bounding_box") or det.get("bbox")
                if bbox:
                    xmin = bbox.get("xmin")
                    ymin = bbox.get("ymin")
                    xmax = bbox.get("xmax")
                    ymax = bbox.get("ymax")
                    if None not in (xmin, ymin, xmax, ymax):
                        width = xmax - xmin
                        height = ymax - ymin
                        if width > 0 and height > 0:
                            total_area += width * height

            threshold_area = 10000.0
            intensity = min(10.0, (total_area / threshold_area) * 10)

            if intensity >= 7:
                level = "critical"
            elif intensity >= 5:
                level = "warning"
            else:
                level = "info"

            # Event: pothole_detection
            human_lines = ["    - pothole detected"]
            pothole_event = {
                "type": "pothole_detection",
                "stream_time": datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S UTC"),
                "level": level,
                "intensity": round(intensity, 1),
                "config": {
                    "min_value": 0,
                    "max_value": 10,
                    "level_settings": {"info": 2, "warning": 5, "critical": 7},
                },
                "application_name": "Pothole Detection System",
                "application_version": "1.0",
                "location_info": None,
                "human_text": "\n".join(human_lines),
            }
            frame_events.append(pothole_event)

        # Event: pothole_alert(s)
        for alert in alerts:
            alert_lines = ["    - pothole detected"]

            alert_event = {
                "type": alert.get("type", "pothole_alert"),
                "stream_time": datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S UTC"),
                "level": alert.get("severity", "warning"),
                "intensity": 8.0,
                "config": {
                    "min_value": 0,
                    "max_value": 10,
                    "level_settings": {"info": 2, "warning": 5, "critical": 7},
                },
                "application_name": "Pothole Alert System",
                "application_version": "1.0",
                "location_info": None,
                "human_text": "\n".join(alert_lines),
            }
            frame_events.append(alert_event)

        return events

    def _generate_tracking_stats(
            self,
            summary: Dict,
            insights: List[str],
            summary_text: str,
            config: PotholeConfig,
            frame_number: Optional[int] = None,
            stream_info: Optional[Dict[str, Any]] = None
    ) -> Dict:
        """
        Generate structured tracking stats for pothole detection with frame-based keys.
        """

        frame_key = str(frame_number) if frame_number is not None else "current_frame"
        tracking_stats = {frame_key: []}
        frame_tracking_stats = tracking_stats[frame_key]

        total = summary.get("total_objects", 0)
        detections = summary.get("detections", [])

        # Update rolling history
        if frame_number is not None:
            self._pothole_recent_history.append({
                "frame": frame_number,
                "potholes": total,
            })
            if len(self._pothole_recent_history) > 150:
                self._pothole_recent_history.pop(0)

        # Compute intensity from area
        total_area = 0.0
        for det in detections:
            bbox = det.get("bounding_box") or det.get("bbox")
            if bbox:
                xmin = bbox.get("xmin")
                ymin = bbox.get("ymin")
                xmax = bbox.get("xmax")
                ymax = bbox.get("ymax")
                if None not in (xmin, ymin, xmax, ymax):
                    width = xmax - xmin
                    height = ymax - ymin
                    if width > 0 and height > 0:
                        total_area += width * height

        threshold_area = 10000.0
        intensity_pct = min(100.0, (total_area / threshold_area) * 100)

        # Human-readable text
        current_timestamp = self._get_current_timestamp_str(stream_info)
        start_timestamp = self._get_start_timestamp_str(stream_info)

        human_lines = [f"CURRENT FRAME @ {current_timestamp}:"]
        if total > 0:
            human_lines.append(f"\t- Potholes detected: {total}")
        else:
            human_lines.append(f"\t- No potholes detected")

        human_lines.append("")  # spacing
        human_lines.append(f"ALERTS SINCE @ {start_timestamp}:")

        recent_alerts = any(entry.get("potholes", 0) > 0 for entry in self._pothole_recent_history)

        if recent_alerts:
            human_lines.append(f"\t- Pothole alerts raised")
        else:
            human_lines.append(f"\t- No pothole alerts raised")

        human_text = "\n".join(human_lines)

        tracking_stat = {
            "all_results_for_tracking": {
                "total_detections": total,
                "intensity_percentage": intensity_pct,
                "pothole_summary": summary,
                "unique_count": self._count_unique_tracks(summary),
            },
            "human_text": human_text
        }

        frame_tracking_stats.append(tracking_stat)
        return tracking_stats

    def _count_unique_tracks(self, summary: Dict) -> Optional[int]:
        """Count unique track IDs from detections, if tracking info exists."""
        detections = summary.get("detections", [])
        if not detections:
            return None

        unique_tracks = set()
        for detection in detections:
            track_id = detection.get("track_id")
            if track_id is not None:
                unique_tracks.add(track_id)

        return len(unique_tracks) if unique_tracks else None

    def _get_current_timestamp_str(self, stream_info: Optional[Dict[str, Any]]) -> str:
        """Get formatted current timestamp based on stream type."""
        if not stream_info:
            return "00:00:00.00"

        if stream_info.get("input_settings", {}).get("stream_type", "video_file") == "video_file":
            return stream_info.get("video_timestamp", "")[:8]
        else:
            stream_time_str = stream_info.get("stream_time", "")
            if stream_time_str:
                try:
                    timestamp_str = stream_time_str.replace(" UTC", "")
                    dt = datetime.strptime(timestamp_str, "%Y-%m-%d-%H:%M:%S.%f")
                    timestamp = dt.replace(tzinfo=timezone.utc).timestamp()
                    return self._format_timestamp_for_stream(timestamp)
                except:
                    return self._format_timestamp_for_stream(time.time())
            else:
                return self._format_timestamp_for_stream(time.time())

    def _get_start_timestamp_str(self, stream_info: Optional[Dict[str, Any]]) -> str:
        """Get formatted start timestamp for 'SINCE' block."""
        if not stream_info:
            return "00:00:00"

        if stream_info.get("input_settings", {}).get("stream_type", "video_file") == "video_file":
            return "00:00:00"

        if self._tracking_start_time is None:
            stream_time_str = stream_info.get("stream_time", "")
            if stream_time_str:
                try:
                    timestamp_str = stream_time_str.replace(" UTC", "")
                    dt = datetime.strptime(timestamp_str, "%Y-%m-%d-%H:%M:%S.%f")
                    self._tracking_start_time = dt.replace(tzinfo=timezone.utc).timestamp()
                except:
                    self._tracking_start_time = time.time()
            else:
                self._tracking_start_time = time.time()

        dt = datetime.fromtimestamp(self._tracking_start_time, tz=timezone.utc)
        dt = dt.replace(minute=0, second=0, microsecond=0)
        return dt.strftime('%Y:%m:%d %H:%M:%S')

    def _extract_frame_number(self, stream_info: Optional[Dict[str, Any]]) -> Optional[int]:
        """Extract frame number from stream_info if available."""
        if not stream_info:
            return None
        return stream_info.get("frame_number")

