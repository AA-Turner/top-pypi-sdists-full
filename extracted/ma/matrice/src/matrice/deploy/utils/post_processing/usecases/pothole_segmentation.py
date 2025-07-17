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
        self.categories = ["pothole"]
        self.relevant_categories = ["pothole"]

        # Optional smoothing tracker
        self.smoothing_tracker = None

        # Optional upstream tracker placeholder (unused here)
        self.tracker = None

        # --- Tracking counters ---
        self._total_frame_counter = 0
        self._global_frame_offset = 0

        # --- Canonical pothole tracking ---
        self._total_pothole_track_ids = set()  # All unique canonical pothole track IDs
        self._current_frame_track_ids = set()  # Current frame's canonical IDs

        # --- Tracking start time (for SINCE reporting) ---
        self._tracking_start_time = None

        # --- Canonical aliasing to avoid duplicate pothole counts ---
        self._track_aliases: Dict[Any, Any] = {}
        self._canonical_tracks: Dict[Any, Dict[str, Any]] = {}

        # Merge logic thresholds
        self._track_merge_iou_threshold: float = 0.05  # IoU ≥ 0.05 = same pothole
        self._track_merge_time_window: float = 7.0  # Merge if within 7 seconds

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

    def _update_tracking_state(self, detections: List[Dict[str, Any]]) -> None:
        """
        Track unique pothole track_ids for cumulative and per-frame counts.
        Applies canonical ID merging to avoid duplicate counting when the tracker
        temporarily loses an object and assigns a new ID.
        """
        self._current_frame_track_ids = set()

        for det in detections:
            cat = det.get("category", "").lower()
            raw_track_id = det.get("track_id")
            if cat not in self.categories or raw_track_id is None:
                continue

            bbox = det.get("bounding_box", det.get("bbox"))
            canonical_id = self._merge_or_register_track(raw_track_id, bbox)
            det["track_id"] = canonical_id  # Propagate canonical ID downstream

            self._total_pothole_track_ids.add(canonical_id)
            self._current_frame_track_ids.add(canonical_id)

    def get_total_pothole_count(self) -> int:
        """
        Return the total number of unique potholes detected so far
        (based on unique track_ids).
        """
        return len(self._total_pothole_track_ids)

    def _get_track_ids_info(self, detections: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Extract per-frame and cumulative track ID stats for potholes.
        Mirrors the license plate implementation exactly.
        """
        frame_track_ids = set()
        for det in detections:
            tid = det.get("track_id")
            if tid is not None:
                frame_track_ids.add(tid)

        # Update total unique pothole track IDs
        self._total_pothole_track_ids.update(frame_track_ids)

        return {
            "frame_track_ids": list(frame_track_ids),  #  JSON-serializable
            "total_unique_track_ids": list(self._total_pothole_track_ids),
            "frame_track_ids_count": len(frame_track_ids),
            "total_unique_count": len(self._total_pothole_track_ids),
        }

    def _format_timestamp_for_stream(self, timestamp: float) -> str:
        """Format timestamp for streams (YYYY:MM:DD HH:MM:SS format)."""
        dt = datetime.fromtimestamp(timestamp, tz=timezone.utc)
        return dt.strftime('%Y:%m:%d %H:%M:%S')

    def _extract_frame_number(self, stream_info: Optional[Dict[str, Any]]) -> Optional[int]:
        """
        Extract frame number from stream_info if available.
        Tries both modern 'frame_number' and fallback to input_settings → start_frame.
        """
        if not stream_info:
            return None

        # First try direct frame_number (preferred)
        if "frame_number" in stream_info:
            return stream_info["frame_number"]

        # Fallback: use start_frame if start == end (used in some input sources)
        input_settings = stream_info.get("input_settings", {})
        start_frame = input_settings.get("start_frame")
        end_frame = input_settings.get("end_frame")

        if start_frame is not None and end_frame is not None and start_frame == end_frame:
            return start_frame

        return None

    def process(
            self,
            data: Any,
            config: ConfigProtocol,
            context: Optional[ProcessingContext] = None,
            stream_info: Optional[Dict[str, Any]] = None
    ) -> ProcessingResult:
        """
        Process pothole segmentation use case with tracking, smoothing, summary generation,
        insights, and human-readable reporting.
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

            # Normalize category strings (e.g., "0" → "pothole")
            for det in processed_data:
                cat = det.get("category")
                if isinstance(cat, str) and cat.isdigit():
                    det["category"] = config.index_to_category.get(int(cat), cat)

            # Step 3: Filter to pothole category only
            processed_data = [
                d for d in processed_data
                if d.get("category", "").lower() in self.categories
            ]

            # Step 4: BBox smoothing (optional)
            if config.enable_smoothing:
                processed_data = self._apply_bbox_smoothing(processed_data, config)

            # Step 5: Apply advanced tracker if available
            try:
                from ..advanced_tracker import AdvancedTracker
                from ..advanced_tracker.config import TrackerConfig

                if self.tracker is None:
                    tracker_config = TrackerConfig()
                    self.tracker = AdvancedTracker(tracker_config)
                    self.logger.info("Initialized AdvancedTracker for pothole tracking")

                processed_data = self.tracker.update(processed_data)

            except Exception as e:
                self.logger.warning(f"AdvancedTracker failed: {e}")

            # Step 6: Internal tracking state update
            self._update_tracking_state(processed_data)

            # Step 7: Frame tracking and counters
            frame_number = self._extract_frame_number(stream_info)

            if frame_number is None:
                frame_number = self._total_frame_counter
                self._total_frame_counter += 1

            # Step 8: Summary and counts
            pothole_summary = self._calculate_pothole_summary(processed_data, config)
            general_summary = calculate_counting_summary(processed_data)
            pothole_summary["total_pothole_count"] = self.get_total_pothole_count()

            # Step 9: Insights and alerts
            insights = self._generate_insights(pothole_summary, config)
            alerts = self._check_alerts(pothole_summary, config)
            metrics = self._calculate_metrics(pothole_summary, config, context)
            model_metadata = self._generate_model_metadata(config)
            stream_info.get("input_settings", {})["model_metadata"] = model_metadata
            
            predictions = self._extract_predictions(processed_data, config)
            summary_text = self._generate_summary(pothole_summary, general_summary, alerts)

            # Step 10: Events and tracking stats
            events_dict = self._generate_events(pothole_summary, alerts, config, frame_number)
            tracking_stats_dict = self._generate_tracking_stats(
                pothole_summary, insights, summary_text, config, frame_number, stream_info
            )

            # Final result
            context.processing_time = time.time() - start_time
            context.mark_completed()

            result = self.create_result(
                data={
                    "pothole_summary": pothole_summary,
                    "general_counting_summary": general_summary,
                    "alerts": alerts,
                    "total_pothole_detections": pothole_summary.get("total_objects", 0),
                    "events": events_dict,
                    "tracking_stats": tracking_stats_dict,
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

    def _generate_model_metadata(self, config) -> dict:
        """
        Generate model metadata to be included in the processing result.

        Returns:
            A list of key-value pairs representing model metadata, such as:
            - index_to_category mapping from config
            - categories/classes used for detection
        """
        model_metadata = {"index_to_category":config.index_to_category,"target_classes": self.relevant_categories }
        return model_metadata

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

    def reset_tracker(self) -> None:
        """
        Reset the advanced tracker instance.
        """
        if self.tracker is not None:
            self.tracker.reset()
            self.logger.info("AdvancedTracker reset for new pothole session")

    def reset_tracking_state(self) -> None:
        """
        Reset pothole tracking state (total counts, track IDs, etc.).
        """
        self._total_pothole_track_ids = set()
        self._total_frame_counter = 0
        self._global_frame_offset = 0
        self._tracking_start_time = None
        self._track_aliases.clear()
        self._canonical_tracks.clear()
        self.logger.info("Pothole tracking state reset")

    def reset_all_tracking(self) -> None:
        """
        Reset both advanced tracker and internal tracking state.
        """
        self.reset_tracker()
        self.reset_tracking_state()
        self.logger.info("All pothole tracking state reset")

    def _calculate_pothole_summary(self, data: List[Dict[str, Any]], config: PotholeConfig) -> Dict[str, Any]:
        """
        Calculate summary statistics for pothole detections, including per-category
        counts, total objects, and unique pothole count using internal tracking.
        """
        summary = {
            "total_objects": 0,
            "by_category": {},
            "detections": [],
            "total_pothole_count": 0,
        }

        if not isinstance(data, list):
            return summary

        valid_category = "pothole"
        detections = [
            det for det in data
            if det.get("category", "").lower() == valid_category
        ]

        summary["total_objects"] = len(detections)
        summary["by_category"] = {valid_category: len(detections)}
        summary["detections"] = detections
        summary["total_pothole_count"] = self.get_total_pothole_count()

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
        Generate human-readable summary for pothole detection,
        including total unique pothole count tracked so far.
        """
        total = summary.get("total_objects", 0)
        unique_total = summary.get("total_pothole_count", 0)

        if unique_total == 0:
            return "No pothole alert raised so far"

        summary_parts = []

        if total > 0:
            summary_parts.append(
                f"{total} pothole{'s' if total != 1 else ''} detected in current frame"
            )

        summary_parts.append(
            f"Total unique pothole{'s' if unique_total != 1 else ''} detected so far: {unique_total}"
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
    ) -> List[Dict[str, List[Dict[str, Any]]]]:
        """
        Generate structured events for pothole detection output with frame-aware keys,
        including unique pothole count via tracking.
        """
        from datetime import datetime, timezone

        frame_key = str(frame_number) if frame_number is not None else "current_frame"
        events = {frame_key: []}
        frame_events = events[frame_key]

        total = summary.get("total_objects", 0)
        unique_total = summary.get("total_pothole_count", 0)
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

            human_lines = [
                f"    - {total} pothole{'s' if total != 1 else ''} detected in current frame",
                f"    - Total unique potholes detected so far: {unique_total}",
                f"    - Intensity level: {intensity:.1f} ({level})"
            ]

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

        # Add alerts (if any)
        for alert in alerts:
            alert_lines = [
                "    - pothole detected",
                f"    - Total unique potholes detected so far: {unique_total}",
                f"    - Alert type: {alert.get('type', 'pothole_alert')}"
            ]

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
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        Generate structured tracking stats with frame-based keys, mirroring the license plate use case.
        Includes per-frame and cumulative unique pothole counts.
        """
        from datetime import datetime, timezone

        frame_key = str(frame_number) if frame_number is not None else "current_frame"
        tracking_stats = {frame_key: []}
        frame_tracking_stats = tracking_stats[frame_key]

        detections = summary.get("detections", [])

        # Extract track IDs for current frame
        track_ids = [d.get("track_id") for d in detections if d.get("track_id") is not None]
        unique_ids_this_frame = set(track_ids)

        # Initialize and update global unique pothole ID tracker
        if not hasattr(self, "_unique_ids_seen"):
            self._unique_ids_seen = set()
        self._unique_ids_seen.update(unique_ids_this_frame)

        per_frame_count = len(unique_ids_this_frame)
        total_unique = len(self._unique_ids_seen)

        # Track ID details
        track_ids_info = {
            "frame_track_ids": list(unique_ids_this_frame),
            "total_unique_track_ids": list(self._unique_ids_seen),
            "frame_track_ids_count": per_frame_count,
            "total_unique_count": total_unique,
        }

        # Get formatted timestamps
        current_timestamp = self._get_current_timestamp_str(stream_info)
        start_timestamp = self._get_start_timestamp_str(stream_info)

        # Build human-readable summary
        human_text_lines = []

        human_text_lines.append(f"CURRENT FRAME @ {current_timestamp}:")
        if per_frame_count > 0:
            human_text_lines.append(f"\t- Potholes Detected: {per_frame_count}")
        else:
            human_text_lines.append("\t- No potholes detected")

        human_text_lines.append("")  # spacing

        human_text_lines.append(f"TOTAL SINCE {start_timestamp}:")
        if total_unique > 0:
            human_text_lines.append(f"\t- Total Unique Potholes Detected: {total_unique}")
        else:
            human_text_lines.append(f"\t- No pothole alert raised so far")

        human_text = "\n".join(human_text_lines)

        tracking_stat = {
            "type": "pothole_tracking",
            "category": "infrastructure",
            "count": per_frame_count,
            "insights": insights,
            "summary": summary_text,
            "timestamp": datetime.now(timezone.utc).strftime('%Y-%m-%d-%H:%M:%S UTC'),
            "human_text": human_text,
            "track_ids_info": track_ids_info,
            "global_frame_offset": getattr(self, "_global_frame_offset", 0),
            "local_frame_id": frame_key,
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




    # ------------------------------------------------------------------ #
        # Canonical ID helpers                                               #
        # ------------------------------------------------------------------ #

    def _compute_iou(self, box1: Any, box2: Any) -> float:
        """Compute IoU between two bounding boxes which may be dicts or lists.
        Falls back to 0 when insufficient data is available."""

        # Helper to convert bbox (dict or list) to [x1, y1, x2, y2]
        def _bbox_to_list(bbox):
            if bbox is None:
                return []
            if isinstance(bbox, list):
                return bbox[:4] if len(bbox) >= 4 else []
            if isinstance(bbox, dict):
                if "xmin" in bbox:
                    return [bbox["xmin"], bbox["ymin"], bbox["xmax"], bbox["ymax"]]
                if "x1" in bbox:
                    return [bbox["x1"], bbox["y1"], bbox["x2"], bbox["y2"]]
                # Fallback: first four numeric values
                values = [v for v in bbox.values() if isinstance(v, (int, float))]
                return values[:4] if len(values) >= 4 else []
            return []

        l1 = _bbox_to_list(box1)
        l2 = _bbox_to_list(box2)
        if len(l1) < 4 or len(l2) < 4:
            return 0.0
        x1_min, y1_min, x1_max, y1_max = l1
        x2_min, y2_min, x2_max, y2_max = l2

        # Ensure correct order
        x1_min, x1_max = min(x1_min, x1_max), max(x1_min, x1_max)
        y1_min, y1_max = min(y1_min, y1_max), max(y1_min, y1_max)
        x2_min, x2_max = min(x2_min, x2_max), max(x2_min, x2_max)
        y2_min, y2_max = min(y2_min, y2_max), max(y2_min, y2_max)

        inter_x_min = max(x1_min, x2_min)
        inter_y_min = max(y1_min, y2_min)
        inter_x_max = min(x1_max, x2_max)
        inter_y_max = min(y1_max, y2_max)

        inter_w = max(0.0, inter_x_max - inter_x_min)
        inter_h = max(0.0, inter_y_max - inter_y_min)
        inter_area = inter_w * inter_h

        area1 = (x1_max - x1_min) * (y1_max - y1_min)
        area2 = (x2_max - x2_min) * (y2_max - y2_min)
        union_area = area1 + area2 - inter_area

        return (inter_area / union_area) if union_area > 0 else 0.0

    def _merge_or_register_track(self, raw_id: Any, bbox: Any) -> Any:
        """Return a stable canonical ID for a raw tracker ID, merging fragmented
        tracks when IoU and temporal constraints indicate they represent the
        same physical vehicle."""
        if raw_id is None or bbox is None:
            # Nothing to merge
            return raw_id

        now = time.time()

        # Fast path – raw_id already mapped
        if raw_id in self._track_aliases:
            canonical_id = self._track_aliases[raw_id]
            track_info = self._canonical_tracks.get(canonical_id)
            if track_info is not None:
                track_info["last_bbox"] = bbox
                track_info["last_update"] = now
                track_info["raw_ids"].add(raw_id)
            return canonical_id

        # Attempt to merge with an existing canonical track
        for canonical_id, info in self._canonical_tracks.items():
            # Only consider recently updated tracks
            if now - info["last_update"] > self._track_merge_time_window:
                continue
            iou = self._compute_iou(bbox, info["last_bbox"])
            if iou >= self._track_merge_iou_threshold:
                # Merge
                self._track_aliases[raw_id] = canonical_id
                info["last_bbox"] = bbox
                info["last_update"] = now
                info["raw_ids"].add(raw_id)
                return canonical_id

        # No match – register new canonical track
        canonical_id = raw_id
        self._track_aliases[raw_id] = canonical_id
        self._canonical_tracks[canonical_id] = {
            "last_bbox": bbox,
            "last_update": now,
            "raw_ids": {raw_id},
        }
        return canonical_id

    def _format_timestamp(self, timestamp: float) -> str:
        """Format a timestamp for human-readable output."""
        return datetime.fromtimestamp(timestamp, timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')

    def _get_tracking_start_time(self) -> str:
        """Get the tracking start time, formatted as a string."""
        if self._tracking_start_time is None:
            return "N/A"
        return self._format_timestamp(self._tracking_start_time)

    def _set_tracking_start_time(self) -> None:
        """Set the tracking start time to the current time."""
        self._tracking_start_time = time.time()

