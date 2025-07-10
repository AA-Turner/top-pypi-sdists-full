"""
Fire and Smoke Detection use case implementation.

This module provides a structured implementation of fire and smoke detection
with counting, insights generation, alerting, and tracking.
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


# ======================
# 🔧 Config Definition
# ======================



@dataclass
class FireSmokeConfig(BaseConfig):
    confidence_threshold: float = 0.5

    # Only fire and smoke categories included here (exclude normal)
    fire_smoke_categories: List[str] = field(
        default_factory=lambda: ["fire", "smoke"]
    )

    alert_config: Optional[AlertConfig] = None

    time_window_minutes: int = 60
    enable_unique_counting: bool = True

    # Map only fire and smoke; ignore normal (index 1 not included)
    index_to_category: Optional[Dict[int, str]] = field(
        default_factory=lambda: {
            0: "Fire",
            2: "smoke",
        }
    )

    #  BBox smoothing configuration (added)
    enable_smoothing: bool = False
    smoothing_algorithm: str = "linear"
    smoothing_window_size: int = 5
    smoothing_cooldown_frames: int = 10
    smoothing_confidence_range_factor: float = 0.2

    def __post_init__(self):
        if not (0.0 <= self.confidence_threshold <= 1.0):
            raise ValueError("confidence_threshold must be between 0.0 and 1.0")

        # Normalize category names to lowercase for consistent matching
        self.fire_smoke_categories = [cat.lower() for cat in self.fire_smoke_categories]
        if self.index_to_category:
            self.index_to_category = {k: v.lower() for k, v in self.index_to_category.items()}



# ======================

# ======================
class FireSmokeUseCase(BaseProcessor):
    def __init__(self):
        super().__init__("fire_smoke_detection")
        self.category = "hazard"
        self.smoothing_tracker = None  # Required for bbox smoothing


    def get_config_schema(self) -> Dict[str, Any]:
        """Get configuration schema for fire and smoke detection."""
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
                "fire_smoke_categories": {
                    "type": "array",
                    "items": {"type": "string"},
                    "default": ["Fire", "smoke"],
                    "description": "Category names that represent fire and smoke",
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

    def create_default_config(self, **overrides) -> FireSmokeConfig:
        """Create default configuration with optional overrides."""
        defaults = {
            "category": self.category,
            "usecase": self.name,
            "confidence_threshold": 0.5,
            "fire_smoke_categories": ["Fire", "smoke"],
        }
        defaults.update(overrides)
        return FireSmokeConfig(**defaults)

    def process(
            self,
            data: Any,
            config: ConfigProtocol,
            context: Optional[ProcessingContext] = None,
            stream_info: Optional[Dict[str, Any]] = None
    ) -> ProcessingResult:
        """
        Process fire and smoke detection use case.
        """
        start_time = time.time()

        try:
            # Step 0: Validate config
            if not isinstance(config, FireSmokeConfig):
                return self.create_error_result(
                    "Invalid configuration type for fire and smoke detection",
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
            self.logger.info(f"Processing fire and smoke detection with format: {input_format.value}")

            # Step 2: Confidence thresholding
            processed_data = data
            if config.confidence_threshold is not None:
                processed_data = filter_by_confidence(processed_data, config.confidence_threshold)
                self.logger.debug(f"Applied confidence filtering with threshold {config.confidence_threshold}")

            # Step 3: Category mapping
            if config.index_to_category:
                processed_data = apply_category_mapping(processed_data, config.index_to_category)
                self.logger.debug("Applied category mapping")

            # Step 3.5: BBox smoothing for fire/smoke
            if config.enable_smoothing:
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

                smooth_categories = {"fire", "smoke"}
                fire_smoke_detections = [d for d in processed_data if d.get("category") in smooth_categories]
                smoothed_detections = bbox_smoothing(
                    fire_smoke_detections,
                    self.smoothing_tracker.config,
                    self.smoothing_tracker
                )
                non_smoothed_detections = [d for d in processed_data if d.get("category") not in smooth_categories]
                processed_data = non_smoothed_detections + smoothed_detections
                self.logger.debug("Applied bbox smoothing for fire/smoke categories")

            # Step 4: Summarization
            fire_smoke_summary = self._calculate_fire_smoke_summary(processed_data, config)
            general_summary = calculate_counting_summary(processed_data)

            # Step 5: Insights & alerts
            insights = self._generate_insights(fire_smoke_summary, config)
            alerts = self._check_alerts(fire_smoke_summary, config)

            # Step 6: Metrics
            metrics = self._calculate_metrics(fire_smoke_summary, config, context)

            # Step 7: Predictions
            predictions = self._extract_predictions(processed_data, config)

            # Step 8: Human-readable summary
            summary_text = self._generate_summary(fire_smoke_summary, general_summary, alerts)

            # Step 9: Frame number extraction
            frame_number = None
            if stream_info:
                input_settings = stream_info.get("input_settings", {})
                start_frame = input_settings.get("start_frame")
                end_frame = input_settings.get("end_frame")
                if start_frame is not None and end_frame is not None and start_frame == end_frame:
                    frame_number = start_frame
                elif start_frame is not None:
                    frame_number = start_frame

            # Step 10: Events and tracking stats
            events = self._generate_events(fire_smoke_summary, alerts, config, frame_number=frame_number)
            tracking_stats = self._generate_tracking_stats(
                fire_smoke_summary, insights, summary_text, config,
                frame_number=frame_number,
                stream_info=stream_info
            )

            # Finalize context and return result
            context.processing_time = time.time() - start_time
            context.mark_completed()

            result = self.create_result(
                data={
                    "fire_smoke_summary": fire_smoke_summary,
                    "general_counting_summary": general_summary,
                    "alerts": alerts,
                    "total_fire_smoke_detections": fire_smoke_summary.get("total_objects", 0),
                    "total_fire_detections": fire_smoke_summary.get("by_category", {}).get("fire", 0),
                    "total_smoke_detections": fire_smoke_summary.get("by_category", {}).get("smoke", 0),
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
            self.logger.error(f"Error in fire and smoke processing: {str(e)}")
            return self.create_error_result(
                f"Fire and smoke processing failed: {str(e)}",
                error_type="FireSmokeProcessingError",
                usecase=self.name,
                category=self.category,
                context=context,
            )

    # ==== 🔍 Internal Utilities ====
    def _calculate_fire_smoke_summary(
            self, data: Any, config: FireSmokeConfig
    ) -> Dict[str, Any]:
        """Calculate summary for fire and smoke detections."""
        if isinstance(data, list):
            # Normalize the categories to lowercase for matching
            valid_categories = [cat.lower() for cat in config.fire_smoke_categories]

            detections = [
                det for det in data
                if det.get("category", "").lower() in valid_categories
            ]

            summary = {
                "total_objects": len(detections),
                "by_category": {},
                "detections": detections,
            }

            # Count by each category defined in config
            for category in config.fire_smoke_categories:
                count = len([
                    det for det in detections
                    if det.get("category", "").lower() == category.lower()
                ])
                summary["by_category"][category] = count

            return summary

        return {"total_objects": 0, "by_category": {}, "detections": []}

    def _generate_insights(
            self, summary: Dict, config: FireSmokeConfig
    ) -> List[str]:
        """Generate insights using bbox area for intensity."""

        insights = []

        total = summary.get("total_objects", 0)
        by_category = summary.get("by_category", {})
        detections = summary.get("detections", [])

        total_fire = by_category.get("fire", 0)
        total_smoke = by_category.get("smoke", 0)

        if total == 0:
            insights.append("EVENT: No fire or smoke detected in the scene")
        else:
            if total_fire > 0:
                insights.append(f"EVENT: {total_fire} fire region{'s' if total_fire != 1 else ''} detected")
            if total_smoke > 0:
                insights.append(f"EVENT: {total_smoke} smoke cloud{'s' if total_smoke != 1 else ''} detected")

            fire_percent = (total_fire / total) * 100 if total else 0
            smoke_percent = (total_smoke / total) * 100 if total else 0
            insights.append(f"ANALYSIS: {fire_percent:.1f}% fire, {smoke_percent:.1f}% smoke in detected hazards")

            # Calculate total bbox area using xmin, ymin, xmax, ymax format
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

            # Threshold area (configurable if you want)
            threshold_area = 10000.0

            intensity_pct = min(100.0, (total_area / threshold_area) * 100)

            if intensity_pct < 20:
                insights.append(f"INTENSITY: Low fire/smoke activity ({intensity_pct:.1f}% area coverage)")
            elif intensity_pct <= 50:
                insights.append(f"INTENSITY: Moderate fire/smoke activity ({intensity_pct:.1f}%)")
            elif intensity_pct <= 80:
                insights.append(f"INTENSITY: High fire/smoke activity ({intensity_pct:.1f}%)")
            else:
                insights.append(f"INTENSITY: Very high fire/smoke activity — critical hazard ({intensity_pct:.1f}%)")

        return insights

    def _check_alerts(
            self, summary: Dict, config: FireSmokeConfig
    ) -> List[Dict]:
        """Raise alerts if fire or smoke detected with severity based on intensity."""

        alerts = []
        total = summary.get("total_objects", 0)
        by_category = summary.get("by_category", {})
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

        threshold_area = 10000.0  # Same threshold as insights

        intensity_pct = min(100.0, (total_area / threshold_area) * 100)

        # Determine alert severity
        if intensity_pct > 80:
            severity = "critical"
        elif intensity_pct > 50:
            severity = "warning"
        else:
            severity = "info"

        alert = {
            "type": "fire_smoke_alert",
            "message": f"{total} fire/smoke detection{'s' if total != 1 else ''} with intensity {intensity_pct:.1f}%",
            "severity": severity,
            "detected_fire": by_category.get("fire", 0),
            "detected_smoke": by_category.get("smoke", 0),
        }

        alerts.append(alert)
        return alerts

    def _calculate_metrics(
            self,
            summary: Dict,
            config: FireSmokeConfig,
            context: ProcessingContext,
    ) -> Dict[str, Any]:
        """Calculate detailed metrics for fire and smoke analytics."""

        total = summary.get("total_objects", 0)
        by_category = summary.get("by_category", {})
        detections = summary.get("detections", [])

        total_fire = by_category.get("fire", 0)
        total_smoke = by_category.get("smoke", 0)

        metrics = {
            "total_detections": total,
            "total_fire": total_fire,
            "total_smoke": total_smoke,
            "processing_time": context.processing_time or 0.0,
            "confidence_threshold": config.confidence_threshold,
            "intensity_percentage": 0.0,
            "hazard_level": "unknown",
        }

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

        threshold_area = 10000.0  # Same threshold as insights/alerts

        intensity_pct = min(100.0, (total_area / threshold_area) * 100)
        metrics["intensity_percentage"] = intensity_pct

        if intensity_pct < 20:
            metrics["hazard_level"] = "low"
        elif intensity_pct < 50:
            metrics["hazard_level"] = "moderate"
        elif intensity_pct < 80:
            metrics["hazard_level"] = "high"
        else:
            metrics["hazard_level"] = "critical"

        return metrics

    def _extract_predictions(
            self, data: Any, config: FireSmokeConfig
    ) -> List[Dict[str, Any]]:
        """Extract predictions from processed data for API compatibility."""
        predictions = []

        try:
            if isinstance(data, list):
                for item in data:
                    if isinstance(item, dict):
                        prediction = {
                            "category": item.get("category", item.get("class", "unknown")),
                            "confidence": item.get("confidence", item.get("score", 0.0)),
                            "bounding_box": item.get("bounding_box", item.get("bbox", {})),
                        }
                        predictions.append(prediction)

        except Exception as e:
            self.logger.warning(f"Failed to extract predictions: {str(e)}")

        return predictions

    def _generate_summary(
            self, summary: Dict, general_summary: Dict, alerts: List
    ) -> str:
        """Generate human-readable summary for fire and smoke detection."""
        total = summary.get("total_objects", 0)
        total_fire = summary.get("by_category", {}).get("fire", 0)
        total_smoke = summary.get("by_category", {}).get("smoke", 0)

        if total == 0:
            return "No fire or smoke detected"

        summary_parts = []

        if total_fire > 0:
            summary_parts.append(
                f"{total_fire} fire region{'s' if total_fire != 1 else ''} detected"
            )

        if total_smoke > 0:
            summary_parts.append(
                f"{total_smoke} smoke cloud{'s' if total_smoke != 1 else ''} detected"
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
            config: FireSmokeConfig,
            frame_number: Optional[int] = None
    ) -> List[Dict]:
        """Generate structured events for fire and smoke detection output with frame-aware keys."""
        from datetime import datetime, timezone

        frame_key = str(frame_number) if frame_number is not None else "current_frame"
        events = [{frame_key: []}]
        frame_events = events[0][frame_key]

        total = summary.get("total_objects", 0)
        by_category = summary.get("by_category", {})
        detections = summary.get("detections", [])

        total_fire = by_category.get("fire", 0)
        total_smoke = by_category.get("smoke", 0)

        if total > 0:
            # Calculate total detection area
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

            # Use consistent formatting for human_text
            human_lines = []
            if total_fire > 0:
                human_lines.append("    - fire detected")
            if total_smoke > 0:
                human_lines.append("    - smoke detected")
            if total_fire == 0 and total_smoke == 0:
                human_lines.append("    - no fire or smoke detected")

            fire_smoke_event = {
                "type": "fire_smoke_detection",
                "stream_time": datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S UTC"),
                "level": level,
                "intensity": round(intensity, 1),
                "config": {
                    "min_value": 0,
                    "max_value": 10,
                    "level_settings": {"info": 2, "warning": 5, "critical": 7},
                },
                "application_name": "Fire and Smoke Detection System",
                "application_version": "1.0",
                "location_info": None,
                "human_text": "\n".join(human_lines),
            }
            frame_events.append(fire_smoke_event)

        # Add alert events
        for alert in alerts:
            alert_lines = []
            if total_fire > 0:
                alert_lines.append("    - fire detected")
            if total_smoke > 0:
                alert_lines.append("    - smoke detected")
            if total_fire == 0 and total_smoke == 0:
                alert_lines.append("    - no fire or smoke detected")

            alert_text = "\n".join(alert_lines)

            alert_event = {
                "type": alert.get("type", "fire_smoke_alert"),
                "stream_time": datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S UTC"),
                "level": alert.get("severity", "warning"),
                "intensity": 8.0,
                "config": {
                    "min_value": 0,
                    "max_value": 10,
                    "level_settings": {"info": 2, "warning": 5, "critical": 7},
                },
                "application_name": "Fire and Smoke Alert System",
                "application_version": "1.0",
                "location_info": None,
                "human_text": alert_text,
            }
            frame_events.append(alert_event)

        return events

    def _generate_tracking_stats(
            self,
            summary: Dict,
            insights: List[str],
            summary_text: str,
            config: FireSmokeConfig,
            frame_number: Optional[int] = None,
            stream_info: Optional[Dict[str, Any]] = None
    ) -> List[Dict]:
        """Generate structured tracking stats for fire and smoke detection with frame-based keys."""

        # Determine frame key
        frame_key = str(frame_number) if frame_number is not None else "current_frame"

        tracking_stats = [{frame_key: []}]
        frame_tracking_stats = tracking_stats[0][frame_key]

        total = summary.get("total_objects", 0)
        by_category = summary.get("by_category", {})
        detections = summary.get("detections", [])

        total_fire = by_category.get("fire", 0)
        total_smoke = by_category.get("smoke", 0)

        # Compute total bbox area for intensity percentage
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

        # Build human-readable tracking text using timestamp-aware method
        human_text = self._generate_human_text_for_tracking(
            total_fire=total_fire,
            total_smoke=total_smoke,
            intensity_pct=intensity_pct,
            insights=insights,
            summary_text=summary_text,
            frame_number=frame_number,
            stream_info=stream_info  #  Ensure timestamp context is passed
        )

        tracking_stat = {
            "all_results_for_tracking": {
                "total_detections": total,
                "total_fire": total_fire,
                "total_smoke": total_smoke,
                "intensity_percentage": intensity_pct,
                "fire_smoke_summary": summary,
                "unique_count": self._count_unique_tracks(summary)
            },
            "human_text": human_text
        }

        frame_tracking_stats.append(tracking_stat)
        return tracking_stats

        frame_tracking_stats.append(tracking_stat)
        return tracking_stats

    def _generate_human_text_for_tracking(
            self,
            total_fire: int,
            total_smoke: int,
            intensity_pct: float,
            insights: List[str],
            summary_text: str,
            frame_number: Optional[int] = None,
            stream_info: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Generate structured and formatted human_text for tracking stats."""

        # Get formatted timestamps using internal helpers
        current_time_str = self._get_current_timestamp_str(stream_info)
        start_time_str = self._get_start_timestamp_str(stream_info)

        # Current frame status
        current_lines = [f"CURRENT FRAME @ {current_time_str}:"]
        if total_fire > 0:
            current_lines.append("    - fire detected")
        if total_smoke > 0:
            current_lines.append("    - smoke detected")
        if total_fire == 0 and total_smoke == 0:
            current_lines.append("    - no fire or smoke detected")

        # Since beginning (start_time_str) block
        since_lines = [f"\nSINCE {start_time_str}:"]
        if total_fire > 0 and total_smoke > 0:
            since_lines.append("    - alert for fire and smoke")
        elif total_fire > 0:
            since_lines.append("    - alert for fire")
        elif total_smoke > 0:
            since_lines.append("    - alert for smoke")
        else:
            since_lines.append("    - no alert triggered")

        # Final human text
        return "\n".join(current_lines + since_lines)

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

        is_video_chunk = stream_info.get("input_settings", {}).get("is_video_chunk", False)

        if is_video_chunk:
            video_timestamp = stream_info.get("video_timestamp", 0.0)
            return self._format_timestamp_for_video(video_timestamp)
        elif stream_info.get("input_settings", {}).get("stream_type", "video_file") == "video_file":
            return stream_info.get("video_timestamp", "")
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

        is_video_chunk = stream_info.get("input_settings", {}).get("is_video_chunk", False)

        if is_video_chunk or stream_info.get("input_settings", {}).get("stream_type", "video_file") == "video_file":
            return "00:00:00"
        else:
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

    def _format_timestamp_for_video(self, timestamp: float) -> str:
        hours = int(timestamp // 3600)
        minutes = int((timestamp % 3600) // 60)
        seconds = timestamp % 60
        return f"{hours:02d}:{minutes:02d}:{seconds:06.2f}"

    def _format_timestamp_for_stream(self, timestamp: float) -> str:
        dt = datetime.fromtimestamp(timestamp, tz=timezone.utc)
        return dt.strftime('%Y:%m:%d %H:%M:%S')



