import time
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime, timezone
from collections import deque

# Core SDK imports
from ..core.base import BaseProcessor, ProcessingContext, ProcessingResult, ConfigProtocol
from ..core.config import BaseConfig, AlertConfig

# Utility functions
from ..utils import (
    filter_by_confidence,
    calculate_counting_summary,
    match_results_structure,
    apply_category_mapping,
    bbox_smoothing,
    BBoxSmoothingConfig,
    BBoxSmoothingTracker
)


@dataclass
class LicensePlateConfig(BaseConfig):
    # Smoothing configuration
    enable_smoothing: bool = True
    smoothing_algorithm: str = "observability"  # "window" or "observability"
    smoothing_window_size: int = 20
    smoothing_cooldown_frames: int = 5
    smoothing_confidence_range_factor: float = 0.5

    relevant_categories: List[str] = field(default_factory=lambda: ["License_Plate"])

    # Placeholder alert config for structural compatibility
    alert_config: Optional[AlertConfig] = None

    confidence_threshold: float = 0.4

    # Only relevant classes: License Plate is index 0
    index_to_category: Optional[Dict[int, str]] = field(default_factory=lambda: {
        0: "License_Plate",
        1: "cars",
        2: "motorcycle",
        3: "truck"
    })

class LicensePlateUseCase(BaseProcessor):
    """
    License Plate Detection Use Case — structured similarly to PPEComplianceUseCase.
    Tracks per-frame counts and total unique license plates using track_ids.
    """

    def __init__(self):
        super().__init__("license_plate_detection")
        self.category = "license_plate"

        # List of categories to track (same as config; retained for local use)
        self.relevant_categories = ["License_Plate"]

        # Smoothing tracker (created on-demand if enabled)
        self.smoothing_tracker = None

        # Advanced tracker (will be created on first use)
        self.tracker = None

        # Internal tracking state variables
        self._total_frame_counter = 0
        self._global_frame_offset = 0

        # Set of all unique track_ids seen so far
        self._total_license_plate_track_ids = set()

        # Set of current frame track_ids (updated per frame)
        self._current_frame_track_ids = set()

    def _update_tracking_state(self, detections: List[Dict[str, Any]]) -> None:
        """
        Track unique license plate track_ids for cumulative and per-frame counts.
        """
        self._current_frame_track_ids = set()
        for det in detections:
            track_id = det.get("track_id")
            if track_id is not None:
                self._total_license_plate_track_ids.add(track_id)
                self._current_frame_track_ids.add(track_id)

    def get_total_license_plate_count(self) -> int:
        """
        Return the total number of unique license plates detected so far
        (based on unique track_ids).
        """
        return len(self._total_license_plate_track_ids)

    def _get_track_ids_info(self, detections: list) -> dict:
        frame_track_ids = set()
        for det in detections:
            tid = det.get("track_id")
            if tid is not None:
                frame_track_ids.add(tid)

        # Update total unique track ids set
        self._total_license_plate_track_ids.update(frame_track_ids)

        return {
            "frame_track_ids": list(frame_track_ids),  # ✅ JSON-serializable
            "total_unique_track_ids": list(self._total_license_plate_track_ids),  # ✅ JSON-serializable
            "frame_track_ids_count": len(frame_track_ids),
            "total_unique_count": len(self._total_license_plate_track_ids),
        }

    def process(
            self,
            data: Any,
            config: ConfigProtocol,
            context: Optional[ProcessingContext] = None,
            stream_info: Optional[Dict[str, Any]] = None
    ) -> ProcessingResult:
        """
        Main entry point for License Plate Detection post-processing.
        Applies category mapping, smoothing, tracking, counting, and summary generation.
        """
        start_time = time.time()

        if not isinstance(config, LicensePlateConfig):
            return self.create_error_result("Invalid config type", usecase=self.name, category=self.category,
                                            context=context)

        if context is None:
            context = ProcessingContext()

        # Detect input format and store in context
        input_format = match_results_structure(data)
        context.input_format = input_format

        # Map detection indices to category names if needed
        processed_data = apply_category_mapping(data, config.index_to_category)

        # Filter only relevant category (License_Plate)
        processed_data = [
            d for d in processed_data
            if d.get("category") in self.relevant_categories
        ]

        # Apply bbox smoothing if enabled
        if config.enable_smoothing:
            if self.smoothing_tracker is None:
                smoothing_config = BBoxSmoothingConfig(
                    smoothing_algorithm=config.smoothing_algorithm,
                    window_size=config.smoothing_window_size,
                    cooldown_frames=config.smoothing_cooldown_frames,
                    confidence_threshold=0.5,  # Reasonable default
                    confidence_range_factor=config.smoothing_confidence_range_factor,
                    enable_smoothing=True
                )
                self.smoothing_tracker = BBoxSmoothingTracker(smoothing_config)

            processed_data = bbox_smoothing(
                processed_data,
                self.smoothing_tracker.config,
                self.smoothing_tracker
            )

        # Apply advanced tracking
        try:
            from ..advanced_tracker import AdvancedTracker
            from ..advanced_tracker.config import TrackerConfig

            if self.tracker is None:
                tracker_config = TrackerConfig()
                self.tracker = AdvancedTracker(tracker_config)
                self.logger.info("Initialized AdvancedTracker for License Plate tracking")

            processed_data = self.tracker.update(processed_data)

        except Exception as e:
            self.logger.warning(f"AdvancedTracker failed: {e}")

        # Update tracking state
        self._update_tracking_state(processed_data)

        # Update frame counter
        self._total_frame_counter += 1

        # Extract frame number from stream_info
        frame_number = None
        if stream_info:
            input_settings = stream_info.get("input_settings", {})
            start_frame = input_settings.get("start_frame")
            end_frame = input_settings.get("end_frame")
            if start_frame is not None and end_frame is not None and start_frame == end_frame:
                frame_number = start_frame

        # Compute summaries
        general_counting_summary = calculate_counting_summary(data)
        counting_summary = self._count_categories(processed_data, config)
        total_unique = self.get_total_license_plate_count()
        counting_summary["total_license_plate_count"] = total_unique

        insights = self._generate_insights(counting_summary, config)
        alerts = []  # No alerts for license plate
        predictions = self._extract_predictions(processed_data)
        summary = self._generate_summary(counting_summary, alerts)

        events_list = self._generate_events(counting_summary, alerts, config, frame_number)
        tracking_stats_list = self._generate_tracking_stats(counting_summary, insights, summary, config, frame_number)

        events = events_list[0] if events_list else {}
        tracking_stats = tracking_stats_list[0] if tracking_stats_list else {}

        context.mark_completed()

        result = self.create_result(
            data={
                "counting_summary": counting_summary,
                "general_counting_summary": general_counting_summary,
                "alerts": alerts,
                "total_violations": counting_summary.get("total_count", 0),
                "events": events,
                "tracking_stats": tracking_stats,
            },
            usecase=self.name,
            category=self.category,
            context=context
        )
        result.summary = summary
        result.insights = insights
        result.predictions = predictions
        return result

    def reset_tracker(self) -> None:
        """
        Reset the advanced tracker instance.
        """
        if self.tracker is not None:
            self.tracker.reset()
            self.logger.info("AdvancedTracker reset for new license plate session")

    def reset_tracking_state(self) -> None:
        """
        Reset license plate tracking state (total counts, track IDs, etc.).
        """
        self._total_license_plate_track_ids = set()
        self._total_frame_counter = 0
        self._global_frame_offset = 0
        self.logger.info("License plate tracking state reset")

    def reset_all_tracking(self) -> None:
        """
        Reset both advanced tracker and tracking state.
        """
        self.reset_tracker()
        self.reset_tracking_state()
        self.logger.info("All license plate tracking state reset")

    def _generate_events(
            self,
            counting_summary: Dict,
            alerts: List,
            config: LicensePlateConfig,
            frame_number: Optional[int] = None
    ) -> List[Dict]:
        """Generate structured events for the output format with frame-based keys (no alerts for license plates)."""
        from datetime import datetime, timezone

        # Use frame number as key, fallback to 'current_frame' if not available
        frame_key = str(frame_number) if frame_number is not None else "current_frame"
        events = [{frame_key: []}]
        frame_events = events[0][frame_key]
        total_count = counting_summary.get("total_count", 0)

        if total_count > 0:
            event = {
                "type": "license_plate_detection",
                "severity": "info",
                "category": "license_plate",
                "count": total_count,
                "timestamp": datetime.now(timezone.utc).strftime('%Y-%m-%d-%H:%M:%S UTC'),
                "location_info": None,
                "human_text": f"{total_count} license plate(s) detected"
            }
            frame_events.append(event)

        return events

    def _generate_tracking_stats(
            self,
            counting_summary: Dict,
            insights: List[str],
            summary: str,
            config: LicensePlateConfig,
            frame_number: Optional[int] = None
    ) -> List[Dict]:
        """Generate structured tracking stats with frame-based keys, including per-frame and cumulative counts."""
        from datetime import datetime, timezone

        frame_key = str(frame_number) if frame_number is not None else "current_frame"
        tracking_stats = [{frame_key: []}]
        frame_tracking_stats = tracking_stats[0][frame_key]

        per_frame_count = counting_summary.get("total_count", 0)
        total_unique = counting_summary.get("total_license_plate_count", 0)

        if per_frame_count > 0:
            # Get detailed track_ids info
            track_ids_info = self._get_track_ids_info(counting_summary.get("detections", []))

            tracking_stat = {
                "type": "license_plate_tracking",
                "category": "license_plate",
                "count": per_frame_count,
                "insights": insights,
                "summary": summary,
                "timestamp": datetime.now(timezone.utc).strftime('%Y-%m-%d-%H:%M:%S UTC'),
                "human_text": (
                    f"Tracking Start Time: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M')}\n"
                    f"License Plates Detected: {per_frame_count}\n"
                    f"Total Unique Plates: {total_unique}"
                ),
                "track_ids_info": track_ids_info,
                "global_frame_offset": getattr(self, "_global_frame_offset", 0),
                "local_frame_id": frame_key
            }
            frame_tracking_stats.append(tracking_stat)

        return tracking_stats

    def _count_categories(self, detections: list, config: LicensePlateConfig) -> dict:
        """
        Count the number of license plate detections and return a summary dict.
        Expected to include track_id and category from the AdvancedTracker output.
        """
        counts = {}
        for det in detections:
            cat = det.get('category', 'unknown')
            counts[cat] = counts.get(cat, 0) + 1

        return {
            "total_count": sum(counts.values()),
            "per_category_count": counts,
            "detections": [
                {
                    "bounding_box": det.get("bounding_box"),
                    "category": det.get("category"),
                    "confidence": det.get("confidence"),
                    "track_id": det.get("track_id"),
                    "frame_id": det.get("frame_id")
                }
                for det in detections
            ]
        }

    def _generate_insights(self, summary: dict, config: LicensePlateConfig) -> List[str]:
        """
        Generate simple human-readable insights for license plate detection.
        """
        insights = []
        per_cat = summary.get("per_category_count", {})
        for cat, count in per_cat.items():
            insights.append(f"{cat}: {count} detected")
        return insights

    def _check_alerts(self, summary: dict, config: LicensePlateConfig) -> List[Dict]:
        """
        No alerts are applicable for License Plate Detection.
        This method is retained for architectural consistency.
        """
        return []

    def _extract_predictions(self, detections: list) -> List[Dict[str, Any]]:
        """
        Extract prediction details for output (category, confidence, bounding box).
        """
        return [
            {
                "category": det.get("category", "unknown"),
                "confidence": det.get("confidence", 0.0),
                "bounding_box": det.get("bounding_box", {})
            }
            for det in detections
        ]

    def _generate_summary(self, summary: dict, alerts: List) -> str:
        """
        Generate a human_text string for license plate detection.
        Includes per-frame count and cumulative unique count so far.
        """
        total = summary.get("total_count", 0)
        per_cat = summary.get("per_category_count", {})
        cumulative_total = summary.get("total_license_plate_count", 0)

        lines = []

        if total > 0:
            lines.append(f"{total} license plate(s) detected in this frame")
            if per_cat:
                lines.append("detections:")
                for cat, count in per_cat.items():
                    label = "License Plate"
                    lines.append(f"\t{label}:{count}")
        else:
            lines.append("No license plates detected in this frame")

        lines.append(f"Total unique license plates detected: {cumulative_total}")

        return "\n".join(lines)

