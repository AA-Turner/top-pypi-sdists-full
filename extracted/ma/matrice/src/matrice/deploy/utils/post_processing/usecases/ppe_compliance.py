from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
import time
from collections import deque
from datetime import datetime, timezone

from ..core.base import BaseProcessor, ProcessingContext, ProcessingResult, ConfigProtocol
from ..core.config import BaseConfig, AlertConfig
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
class PPEComplianceConfig(BaseConfig):
    # Smoothing configuration
    enable_smoothing: bool = True
    smoothing_algorithm: str = "observability"  # "window" or "observability"
    smoothing_window_size: int = 20
    smoothing_cooldown_frames: int = 5
    smoothing_confidence_range_factor: float = 0.5
    
    # Violation thresholds
    no_hardhat_threshold: float = 0.91
    no_mask_threshold: float = 0.4
    no_safety_vest_threshold: float = 0.4
    
    violation_categories: List[str] = field(default_factory=lambda: [
        "NO-Hardhat", "NO-Mask", "NO-Safety Vest"
    ])
    alert_config: Optional[AlertConfig] = None
    index_to_category: Optional[Dict[int, str]] = field(default_factory=lambda: {
        -1: 'Hardhat', 0: 'Mask', 1: 'NO-Hardhat', 2: 'NO-Mask', 3: 'NO-Safety Vest',
        4: 'Person', 5: 'Safety Cone', 6: 'Safety Vest', 7: 'machinery', 8: 'vehicle'
    })

class PPEComplianceUseCase(BaseProcessor):
    def _get_track_ids_info(self, detections: list) -> Dict[str, Any]:
        """
        Get detailed information about track IDs for PPE violations (per frame).
        """
        # Collect all track_ids in this frame
        frame_track_ids = set()
        for det in detections:
            tid = det.get('track_id')
            if tid is not None:
                frame_track_ids.add(tid)
        # Use persistent total set for unique counting
        total_track_ids = set()
        for s in getattr(self, '_violation_total_track_ids', {}).values():
            total_track_ids.update(s)
        return {
            "total_count": len(total_track_ids),
            "current_frame_count": len(frame_track_ids),
            "total_unique_track_ids": len(total_track_ids),
            "current_frame_track_ids": list(frame_track_ids),
            "last_update_time": time.time(),
            "total_frames_processed": getattr(self, '_total_frame_counter', 0)
        }

    @staticmethod
    def _iou(bbox1, bbox2):
        """Compute IoU between two bboxes (dicts with xmin/ymin/xmax/ymax)."""
        x1 = max(bbox1["xmin"], bbox2["xmin"])
        y1 = max(bbox1["ymin"], bbox2["ymin"])
        x2 = min(bbox1["xmax"], bbox2["xmax"])
        y2 = min(bbox1["ymax"], bbox2["ymax"])
        inter_w = max(0, x2 - x1)
        inter_h = max(0, y2 - y1)
        inter_area = inter_w * inter_h
        area1 = (bbox1["xmax"] - bbox1["xmin"]) * (bbox1["ymax"] - bbox1["ymin"])
        area2 = (bbox2["xmax"] - bbox2["xmin"]) * (bbox2["ymax"] - bbox2["ymin"])
        union = area1 + area2 - inter_area
        if union == 0:
            return 0.0
        return inter_area / union

    @staticmethod
    def _deduplicate_violations(detections, iou_thresh=0.7):
        """Suppress duplicate/overlapping violations with same label and high IoU."""
        filtered = []
        used = [False] * len(detections)
        for i, det in enumerate(detections):
            if used[i]:
                continue
            group = [i]
            for j in range(i+1, len(detections)):
                if used[j]:
                    continue
                if det.get("category") == detections[j].get("category"):
                    bbox1 = det.get("bounding_box")
                    bbox2 = detections[j].get("bounding_box")
                    if bbox1 and bbox2:
                        iou = PPEComplianceUseCase._iou(bbox1, bbox2)
                        if iou > iou_thresh:
                            used[j] = True
                            group.append(j)
            # Keep the highest confidence detection in the group
            best_idx = max(group, key=lambda idx: detections[idx].get("confidence", 0))
            filtered.append(detections[best_idx])
            used[best_idx] = True
        return filtered
    def _update_violation_tracking_state(self, detections: list):
        """
        Track unique violation track_ids per category for total count after tracking.
        """
        self._violation_total_track_ids = getattr(self, '_violation_total_track_ids', {cat: set() for cat in self.violation_categories})
        self._violation_current_frame_track_ids = {cat: set() for cat in self.violation_categories}
        for det in detections:
            cat = det.get('category')
            track_id = det.get('track_id')
            if cat in self.violation_categories and track_id is not None:
                self._violation_total_track_ids[cat].add(track_id)
                self._violation_current_frame_track_ids[cat].add(track_id)

    def get_total_violation_counts(self):
        """
        Return total unique track_id count for each violation category.
        """
        return {cat: len(ids) for cat, ids in getattr(self, '_violation_total_track_ids', {}).items()}
    """PPE compliance detection use case with violation smoothing and alerting."""

    def __init__(self):
        super().__init__("ppe_compliance_detection")
        self.category = "ppe"
        # List of violation categories to track
        self.violation_categories = ["NO-Hardhat", "NO-Mask", "NO-Safety Vest"]
        # Initialize smoothing tracker
        self.smoothing_tracker = None
        # Initialize advanced tracker (will be created on first use)
        self.tracker = None
        # Initialize tracking state variables
        self._total_frame_counter = 0
        self._global_frame_offset = 0
        # Set of current frame track_ids (updated per frame)
        self._current_frame_track_ids = set()
        # Track start time for "TOTAL SINCE" calculation
        self._tracking_start_time = None
    def _format_timestamp_for_video(self, timestamp: float) -> str:
        """Format timestamp for video chunks (HH:MM:SS.ms format)."""
        hours = int(timestamp // 3600)
        minutes = int((timestamp % 3600) // 60)
        seconds = timestamp % 60
        return f"{hours:02d}:{minutes:02d}:{seconds:06.2f}"

    def _format_timestamp_for_stream(self, timestamp: float) -> str:
        """Format timestamp for streams (YYYY:MM:DD HH:MM:SS format)."""
        dt = datetime.fromtimestamp(timestamp, tz=timezone.utc)
        return dt.strftime('%Y:%m:%d %H:%M:%S')

    def _get_current_timestamp_str(self, stream_info: Optional[Dict[str, Any]]) -> str:
        """Get formatted current timestamp based on stream type."""
        if not stream_info:
            return "00:00:00.00"
        is_video_chunk = stream_info.get("input_settings", {}).get("is_video_chunk", False)
        # if is_video_chunk:
        #     video_timestamp = stream_info.get("video_timestamp", 0.0)
        #     return self._format_timestamp_for_video(video_timestamp)
        if stream_info.get("input_settings", {}).get("stream_type", "video_file") == "video_file":
            # If video format, return video timestamp
            stream_time_str = stream_info.get("video_timestamp", "")
            return stream_time_str[:8]
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
        """Get formatted start timestamp for 'TOTAL SINCE' based on stream type."""
        if not stream_info:
            return "00:00:00"
        is_video_chunk = stream_info.get("input_settings", {}).get("is_video_chunk", False)
        if is_video_chunk:
            return "00:00:00"
        elif stream_info.get("input_settings", {}).get("stream_type", "video_file") == "video_file":
            # If video format, start from 00:00:00
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

    def process(self, data: Any, config: ConfigProtocol, context: Optional[ProcessingContext] = None, stream_info: Optional[Dict[str, Any]] = None) -> ProcessingResult:
        """
        Main entry point for PPE compliance detection post-processing.
        Applies category mapping, violation smoothing, counting, alerting, and summary generation.
        Returns a ProcessingResult with all relevant outputs.
        """
        start_time = time.time()
        # Ensure config is correct type
        if not isinstance(config, PPEComplianceConfig):
            return self.create_error_result("Invalid config type", usecase=self.name, category=self.category, context=context)
        if context is None:
            context = ProcessingContext()

        # Detect input format and store in context
        input_format = match_results_structure(data)
        context.input_format = input_format
        context.no_hardhat_threshold = config.no_hardhat_threshold



        # Map detection indices to category names robustly (PPE only)
        processed_data = self._robust_apply_category_mapping(data, config.index_to_category)
        # Only keep violation categories (remove 'Person', etc.)
        processed_data = [d for d in processed_data if d.get('category') in self.violation_categories]

        # Apply bbox smoothing if enabled
        if config.enable_smoothing:
            if self.smoothing_tracker is None:
                smoothing_config = BBoxSmoothingConfig(
                    smoothing_algorithm=config.smoothing_algorithm,
                    window_size=config.smoothing_window_size,
                    cooldown_frames=config.smoothing_cooldown_frames,
                    confidence_threshold=config.no_mask_threshold,  # Use mask threshold as default
                    confidence_range_factor=config.smoothing_confidence_range_factor,
                    enable_smoothing=True
                )
                self.smoothing_tracker = BBoxSmoothingTracker(smoothing_config)
            smoothed_violations = bbox_smoothing(processed_data, self.smoothing_tracker.config, self.smoothing_tracker)
            processed_data = smoothed_violations

        # Advanced tracking (BYTETracker-like)
        try:
            from ..advanced_tracker import AdvancedTracker
            from ..advanced_tracker.config import TrackerConfig
            
            # Create tracker instance if it doesn't exist (preserves state across frames)
            if self.tracker is None:
                tracker_config = TrackerConfig()
                self.tracker = AdvancedTracker(tracker_config)
                self.logger.info("Initialized AdvancedTracker for PPE compliance tracking")
            
            # The tracker expects the data in the same format as input
            # It will add track_id and frame_id to each detection
            processed_data = self.tracker.update(processed_data)
            
        except Exception as e:
            # If advanced tracker fails, fallback to unsmoothed detections
            self.logger.warning(f"AdvancedTracker failed: {e}")

        # Deduplicate overlapping violations (same label, high IoU)
        # processed_data = self._deduplicate_violations(processed_data, iou_thresh=0.92)

        # Update violation tracking state for total count per label
        self._update_violation_tracking_state(processed_data)
        
        # Update frame counter
        self._total_frame_counter += 1

        # Extract frame information from stream_info
        frame_number = None
        if stream_info:
            input_settings = stream_info.get("input_settings", {})
            start_frame = input_settings.get("start_frame")
            end_frame = input_settings.get("end_frame")
            # If start and end frame are the same, it's a single frame
            if start_frame is not None and end_frame is not None and start_frame == end_frame:
                frame_number = start_frame

        # Compute summaries and alerts
        general_counting_summary = calculate_counting_summary(data)
        counting_summary = self._count_categories(processed_data, config)
        # Add total unique violation counts after tracking using only local state
        total_violation_counts = self.get_total_violation_counts()
        counting_summary['total_violation_counts'] = total_violation_counts
        insights = self._generate_insights(counting_summary, config)
        alerts = self._check_alerts(counting_summary, config)
        predictions = self._extract_predictions(processed_data)
        summary = self._generate_summary(counting_summary, alerts)

        # Step: Generate structured events and tracking stats with frame-based keys
        events_list = self._generate_events(counting_summary, alerts, config, frame_number, stream_info)
        tracking_stats_list = self._generate_tracking_stats(counting_summary, insights, summary, config, frame_number, stream_info)

        # Extract frame-based dictionaries from the lists
        events = events_list[0] if events_list else {}
        tracking_stats = tracking_stats_list[0] if tracking_stats_list else {}

        context.mark_completed()

        # Build result object
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
        
        This should be called when:
        - Starting a completely new tracking session
        - Switching to a different video/stream
        - Manual reset requested by user
        """
        if self.tracker is not None:
            self.tracker.reset()
            self.logger.info("AdvancedTracker reset for new tracking session")
    
    def reset_violation_tracking(self) -> None:
        """
        Reset violation tracking state (total counts, track IDs, etc.).
        
        This should be called when:
        - Starting a completely new tracking session
        - Switching to a different video/stream
        - Manual reset requested by user
        """
        self._violation_total_track_ids = {cat: set() for cat in self.violation_categories}
        self._total_frame_counter = 0
        self._global_frame_offset = 0
        self._tracking_start_time = None
        self.logger.info("PPE violation tracking state reset")
    
    def reset_all_tracking(self) -> None:
        """
        Reset both advanced tracker and violation tracking state.
        """
        self.reset_tracker()
        self.reset_violation_tracking()
        self.logger.info("All PPE tracking state reset")
        
    def _generate_events(self, counting_summary: Dict, alerts: List, config: PPEComplianceConfig, frame_number: Optional[int] = None, stream_info: Optional[Dict[str, Any]] = None) -> List[Dict]:
        """Generate structured events for the output format with frame-based keys."""
        # Use frame number as key, fallback to 'current_frame' if not available
        frame_key = str(frame_number) if frame_number is not None else "current_frame"
        events = [{frame_key: []}]
        frame_events = events[0][frame_key]
        total_violations = counting_summary.get("total_count", 0)

        # Generate human text in new format
        human_text_lines = ["EVENTS DETECTED:"]
        if total_violations > 0:
            human_text_lines.append(f"    - {total_violations} PPE violation(s) detected [INFO]")
        else:
            human_text_lines.append("    - No PPE violations detected")
        human_text = "\n".join(human_text_lines)

        if total_violations > 0:
            event = {
                "type": "ppe_violation",
                "severity": "info",
                "category": "ppe",
                "count": total_violations,
                "timestamp": datetime.now(timezone.utc).strftime('%Y-%m-%d-%H:%M:%S UTC'),
                "location_info": None,
                "human_text": human_text
            }
            frame_events.append(event)
        # Add alert events
        for alert in alerts:
            alert_event = {
                "type": alert.get("type", "alert"),
                "severity": alert.get("severity", "warning"),
                "category": alert.get("category", "ppe"),
                "count": alert.get("current_count", 0),
                "timestamp": datetime.now(timezone.utc).strftime('%Y-%m-%d-%H:%M:%S UTC'),
                "location_info": alert.get("zone"),
                "human_text": alert.get("human_text", "PPE alert triggered")
            }
            frame_events.append(alert_event)
        return events

    def _generate_tracking_stats(
            self,
            counting_summary: Dict,
            insights: List[str],
            summary: str,
            config: PPEComplianceConfig,
            frame_number: Optional[int] = None,
            stream_info: Optional[Dict[str, Any]] = None
    ) -> List[Dict]:
        """Generate structured tracking stats for the output format with frame-based keys, including track_ids_info."""


        frame_key = str(frame_number) if frame_number is not None else "current_frame"
        tracking_stats = [{frame_key: []}]
        frame_tracking_stats = tracking_stats[0][frame_key]

        total_violations = counting_summary.get("total_count", 0)
        per_cat = counting_summary.get("per_category_count", {})
        cumulative = counting_summary.get("total_violation_counts", {})
        cumulative_total = sum(cumulative.values()) if cumulative else 0

        track_ids_info = self._get_track_ids_info(counting_summary.get("detections", []))

        current_timestamp = self._get_current_timestamp_str(stream_info)
        start_timestamp = self._get_start_timestamp_str(stream_info)

        human_text_lines = []

        # CURRENT FRAME section
        human_text_lines.append(f"CURRENT FRAME @ {current_timestamp}:")
        if total_violations > 0:
            human_text_lines.append(f"\t- PPE Violations Detected: {total_violations}")
            for cat in ["NO-Hardhat", "NO-Mask", "NO-Safety Vest"]:
                count = per_cat.get(cat, 0)
                if count > 0:
                    label = self.CATEGORY_DISPLAY.get(cat, cat).replace(" Violations", "")
                    human_text_lines.append(f"\t\t- {label}: {count}")
        else:
            human_text_lines.append("\t- No PPE violations detected")

        human_text_lines.append("")  # spacing

        # TOTAL SINCE section
        human_text_lines.append(f"TOTAL SINCE {start_timestamp}:")
        human_text_lines.append(f"\t- Total PPE Violations Detected: {cumulative_total}")
        for cat in ["NO-Hardhat", "NO-Mask", "NO-Safety Vest"]:
            count = cumulative.get(cat, 0)
            if count > 0:
                label = self.CATEGORY_DISPLAY.get(cat, cat).replace(" Violations", "")
                human_text_lines.append(f"\t\t- {label}: {count}")

        human_text = "\n".join(human_text_lines)

        tracking_stat = {
            "type": "ppe_tracking",
            "category": "ppe",
            "count": total_violations,
            "insights": insights,
            "summary": summary,
            "timestamp": datetime.now(timezone.utc).strftime('%Y-%m-%d-%H:%M:%S UTC'),
            "human_text": human_text,
            "track_ids_info": track_ids_info,
            "global_frame_offset": getattr(self, '_global_frame_offset', 0),
            "local_frame_id": frame_key
        }

        frame_tracking_stats.append(tracking_stat)
        return tracking_stats

    def _count_categories(self, detections: list, config: PPEComplianceConfig) -> dict:
        """
        Count the number of detections per category and return a summary dict.
        The detections list is expected to have 'track_id' (from tracker), 'category', 'bounding_box', etc.
        Output structure will include 'track_id' for each detection as per AdvancedTracker output.
        """
        counts = {}
        for det in detections:
            cat = det.get('category', 'unknown')
            if cat in self.violation_categories:
                counts[cat] = counts.get(cat, 0) + 1
        # Each detection dict will now include 'track_id' (and possibly 'frame_id')
        filtered_detections = [
            {
                "bounding_box": det.get("bounding_box"),
                "category": det.get("category"),
                "confidence": det.get("confidence"),
                "track_id": det.get("track_id"),
                "frame_id": det.get("frame_id")
            }
            for det in detections if det.get('category') in self.violation_categories
        ]
        return {
            "total_count": sum(counts.values()),
            "per_category_count": counts,
            "detections": filtered_detections
        }

    # Human-friendly display names for violation categories
    CATEGORY_DISPLAY = {
        "NO-Hardhat": "No Hardhat Violations",
        "NO-Mask": "No Mask Violations",
        "NO-Safety Vest": "No Safety Vest Violations"
    }

    def _generate_insights(self, summary: dict, config: PPEComplianceConfig) -> List[str]:
        """
        Generate human-readable insights for each violation category.
        """
        insights = []
        per_cat = summary.get("per_category_count", {})
        for cat, count in per_cat.items():
            display = self.CATEGORY_DISPLAY.get(cat, cat)
            insights.append(f"{display}:{count}")
        return insights

    def _check_alerts(self, summary: dict, config: PPEComplianceConfig) -> List[Dict]:
        """
        Check if any alert thresholds are exceeded and return alert dicts.
        """
        alerts = []
        if not config.alert_config:
            return alerts
        total = summary.get("total_count", 0)
        if config.alert_config.count_thresholds:
            for category, threshold in config.alert_config.count_thresholds.items():
                if category == "all" and total >= threshold:
                    timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%d-%H:%M:%S UTC')
                    alert_description = f"PPE violation count ({total}) exceeds threshold ({threshold})"
                    alerts.append({
                        "type": "count_threshold",
                        "severity": "warning",
                        "message": alert_description,
                        "category": category,
                        "current_count": total,
                        "threshold": threshold,
                        "human_text": f"Time: {timestamp}\n{alert_description}"
                    })
        return alerts

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
        Generate a human_text string for the result, including per-category insights if available.
        Adds a tab before each violation label for better formatting.
        Also always includes the cumulative violation count so far.
        """
        total = summary.get("total_count", 0)
        per_cat = summary.get("per_category_count", {})
        cumulative = summary.get("total_violation_counts", {})
        cumulative_total = sum(cumulative.values()) if cumulative else 0
        lines = []
        if total > 0:
            lines.append(f"{total} PPE violation(s) detected")
            if per_cat:
                lines.append("violations:")
                for cat, count in per_cat.items():
                    display = self.CATEGORY_DISPLAY.get(cat, cat)
                    label = display.replace(" Violations", "").replace("No ", "No ").replace("Safety Vest", "safety vest").replace("Mask", "mask").replace("Hardhat", "hardhat")
                    if count == 1:
                        lines.append(f"\t{label}")
                    else:
                        lines.append(f"\t{label}:{count}")
        else:
            lines.append("No PPE violation detected")
        lines.append(f"Total PPE violations detected: {cumulative_total}")
        if alerts:
            lines.append(f"{len(alerts)} alert(s)")
        return "\n".join(lines)

    def _robust_apply_category_mapping(self, data, index_to_category):
        """
        Map detection indices to category names, robustly handling int or numeric string indices.
        Only for PPE use case to avoid affecting other use cases.
        Handles both int and str keys in index_to_category.
        """
        mapped = []
        for det in data:
            mapped_det = det.copy()
            cat = det.get("category")
            # Convert string numbers to int if possible
            if isinstance(cat, str) and cat.isdigit():
                cat_int = int(cat)
            else:
                cat_int = cat
            mapped_label = None
            if cat_int in index_to_category:
                mapped_label = index_to_category[cat_int]
            elif isinstance(cat_int, int) and str(cat_int) in index_to_category:
                mapped_label = index_to_category[str(cat_int)]
            if mapped_label is not None:
                mapped_det["category"] = mapped_label
            mapped.append(mapped_det)
        return mapped
