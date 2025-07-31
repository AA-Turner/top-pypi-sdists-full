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
        0: 'Hardhat', 1: 'Mask', 2: 'NO-Hardhat', 3: 'NO-Mask', 4: 'NO-Safety Vest',
        5: 'Person', 6: 'Safety Cone', 7: 'Safety Vest', 8: 'machinery', 9: 'vehicle'
    })

class PPEComplianceUseCase(BaseProcessor):
    def get_camera_info_from_stream(self, stream_info: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Extract camera information from stream_info dict, matching mask_detection's approach.
        """
        if not stream_info:
            return {"camera_name": None, "camera_group": None, "location": None}
        input_settings = stream_info.get("input_settings", {})
        camera_name = input_settings.get("camera_name")
        camera_group = input_settings.get("camera_group")
        location = input_settings.get("location")
        return {
            "camera_name": camera_name,
            "camera_group": camera_group,
            "location": location
        }
    def _merge_or_register_track(self, raw_id: Any, bbox: Any) -> Any:
        """Return a stable canonical ID for a raw tracker ID, merging fragmented tracks when IoU and temporal constraints indicate they represent the same physical object."""
        if not hasattr(self, '_track_aliases'):
            self._track_aliases = {}
            self._canonical_tracks = {}
            self._canonical_id_counter = 0
        if raw_id is None or bbox is None:
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
        # Attempt to merge with an existing canonical track (IoU + time window)
        best_iou = 0.0
        best_canonical = None
        for cid, info in self._canonical_tracks.items():
            last_bbox = info.get("last_bbox")
            last_update = info.get("last_update", 0)
            if last_bbox is not None and now - last_update < 2.0:
                iou = self._iou(bbox, last_bbox)
                if iou > 0.7 and iou > best_iou:
                    best_iou = iou
                    best_canonical = cid
        if best_canonical is not None:
            self._track_aliases[raw_id] = best_canonical
            info = self._canonical_tracks[best_canonical]
            info["last_bbox"] = bbox
            info["last_update"] = now
            info["raw_ids"].add(raw_id)
            return best_canonical
        # New canonical track
        canonical_id = f"ppe_{self._canonical_id_counter}"
        self._canonical_id_counter += 1
        self._track_aliases[raw_id] = canonical_id
        self._canonical_tracks[canonical_id] = {
            "last_bbox": bbox,
            "last_update": now,
            "raw_ids": {raw_id},
        }
        return canonical_id
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
        Uses canonical ID merging to avoid duplicate counting when the tracker loses and reassigns IDs.
        """
        if not hasattr(self, '_violation_total_track_ids'):
            self._violation_total_track_ids = {cat: set() for cat in self.violation_categories}
        self._violation_current_frame_track_ids = {cat: set() for cat in self.violation_categories}
        for det in detections:
            cat = det.get('category')
            raw_track_id = det.get('track_id')
            if cat not in self.violation_categories or raw_track_id is None:
                continue
            bbox = det.get("bounding_box", det.get("bbox"))
            canonical_id = self._merge_or_register_track(raw_track_id, bbox)
            det["track_id"] = canonical_id  # propagate canonical ID
            self._violation_total_track_ids.setdefault(cat, set()).add(canonical_id)
            self._violation_current_frame_track_ids[cat].add(canonical_id)

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
        """Format timestamp for video chunks (HH:MM:SS.s format)."""
        hours = int(timestamp // 3600)
        minutes = int((timestamp % 3600) // 60)
        seconds = round(float(timestamp % 60), 1)
        return f"{hours:02d}:{minutes:02d}:{seconds:.1f}"

    def _format_timestamp_for_stream(self, timestamp: float) -> str:
        """Format timestamp for streams (YYYY:MM:DD HH:MM:SS format)."""
        dt = datetime.fromtimestamp(timestamp, tz=timezone.utc)
        return dt.strftime('%Y:%m:%d %H:%M:%S')

    def _get_current_timestamp_str(self, stream_info: Optional[Dict[str, Any]], precision=False, frame_id: Optional[str]=None) -> str:
        """Get formatted current timestamp based on stream type."""
        if not stream_info:
            return "00:00:00.00"
        # If precision is requested, use frame-based time for video files
        if precision:
            if stream_info.get("feed_type", "live") == "disk":
                start_time = stream_info.get("start_frame", 30)/stream_info.get("original_fps", 30)
            if stream_info.get("input_settings", {}).get("start_frame", "na") != "na":
                if frame_id:
                    start_time = int(frame_id)/stream_info.get("input_settings", {}).get("original_fps", 30)
                else:
                    start_time = stream_info.get("input_settings", {}).get("start_frame", 30)/stream_info.get("input_settings", {}).get("original_fps", 30)
                stream_time_str = self._format_timestamp_for_video(start_time)
                return stream_time_str
            else:
                return datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")

        if stream_info.get("feed_type", "live") == "disk":
            start_time = stream_info.get("start_frame", 30)/stream_info.get("original_fps", 30)
        if stream_info.get("input_settings", {}).get("start_frame", "na") != "na":
            if frame_id:
                start_time = int(frame_id)/stream_info.get("input_settings", {}).get("original_fps", 30)
            else:
                start_time = stream_info.get("input_settings", {}).get("start_frame", 30)/stream_info.get("input_settings", {}).get("original_fps", 30)
            stream_time_str = self._format_timestamp_for_video(start_time)
            return stream_time_str
        else:
            # For streams, use stream_time from stream_info
            stream_time_str = stream_info.get("input_settings", {}).get("stream_info", {}).get("stream_time", "")
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

    def _get_start_timestamp_str(self, stream_info: Optional[Dict[str, Any]], precision=False) -> str:
        """Get formatted start timestamp for 'TOTAL SINCE' based on stream type."""
        if not stream_info:
            return "00:00:00"
        if precision:
            if stream_info.get("input_settings", {}).get("start_frame", "na") != "na":
                return "00:00:00"
            else:
                return datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")

        if stream_info.get("input_settings", {}).get("start_frame", "na") != "na":
            return "00:00:00"
        else:
            if self._tracking_start_time is None:
                stream_time_str = stream_info.get("input_settings", {}).get("stream_info", {}).get("stream_time", "")
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
        Returns a ProcessingResult with all relevant outputs in the new agg_summary format
        """
        start_time = time.time()
        if not isinstance(config, PPEComplianceConfig):
            return self.create_error_result("Invalid config type", usecase=self.name, category=self.category, context=context)
        if context is None:
            context = ProcessingContext()

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
            processed_data = bbox_smoothing(processed_data, self.smoothing_tracker.config, self.smoothing_tracker)

        # Advanced tracking (BYTETracker-like)
        try:
            from ..advanced_tracker import AdvancedTracker
            from ..advanced_tracker.config import TrackerConfig
            if self.tracker is None:
                tracker_config = TrackerConfig()
                self.tracker = AdvancedTracker(tracker_config)
                self.logger.info("Initialized AdvancedTracker for PPE compliance tracking")
            processed_data = self.tracker.update(processed_data)
        except Exception as e:
            self.logger.warning(f"AdvancedTracker failed: {e}")

        self._update_violation_tracking_state(processed_data)
        self._total_frame_counter += 1

        # Frame number logic (not chunkwise, just per call)
        frame_number = self._total_frame_counter

        # Compute summaries and alerts
        general_counting_summary = calculate_counting_summary(data)
        counting_summary = self._count_categories(processed_data, config)
        total_violation_counts = self.get_total_violation_counts()
        counting_summary['total_violation_counts'] = total_violation_counts
        insights = self._generate_insights(counting_summary, config)
        alerts = self._check_alerts(counting_summary, config)
        predictions = self._extract_predictions(processed_data)
        summary = self._generate_summary(counting_summary, alerts)

        # Generate new-format output (agg_summary)
        incidents = self._generate_events(counting_summary, alerts, config, frame_number, stream_info)
        tracking_stats = self._generate_tracking_stats(counting_summary, insights, summary, config, frame_number, stream_info)
        business_analytics = {}
        app_name = "ppe_compliance"
        app_version = "1.2"
        agg_human_text = {
            "Application Name": app_name,
            "Application Version": app_version,
            "Incidents:": incidents.get("human_text", ""),
            "Tracking Statistics:": tracking_stats.get("human_text", "")
        }
        agg_summary = {str(frame_number): {
            "incidents": incidents,
            "tracking_stats": tracking_stats,
            "business_analytics": business_analytics,
            "alerts": alerts,
            "human_text": agg_human_text
        }}

        context.mark_completed()
        result = self.create_result(
            data={"agg_summary": agg_summary},
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
        # Also reset canonical track merging state
        self._track_aliases = {}
        self._canonical_tracks = {}
        self._canonical_id_counter = 0
        self.logger.info("PPE violation tracking state reset")
    
    def reset_all_tracking(self) -> None:
        """
        Reset both advanced tracker and violation tracking state.
        """
        self.reset_tracker()
        self.reset_violation_tracking()
        self.logger.info("All PPE tracking state reset")
        
    def _generate_events(self, counting_summary: Dict, alerts: List, config: PPEComplianceConfig, frame_number: Optional[int] = None, stream_info: Optional[Dict[str, Any]] = None) -> Dict:
        total_violations = counting_summary.get("total_count", 0)
        severity = "info" if total_violations > 0 else "none"
        human_text = f"INCIDENTS DETECTED @ :\n\tSeverity Level: ('ppe_compliance', '{severity}')"
        incident = {
            "incident_id": f"ppe_compliance_{frame_number}",
            "incident_type": "ppe_compliance",
            "severity_level": severity,
            "human_text": human_text,
            "start_time": "00:00:00",
            "end_time": "00:00:00",
            "camera_info": self.get_camera_info_from_stream(stream_info),
            "level_settings": {
                "low": 1,
                "medium": 3,
                "significant": 4,
                "critical": 7
            },
            "alerts": alerts,
            "alert_settings": [],
        }
        return incident

    def _generate_tracking_stats(
            self,
            counting_summary: Dict,
            insights: List[str],
            summary: str,
            config: PPEComplianceConfig,
            frame_number: Optional[int] = None,
            stream_info: Optional[Dict[str, Any]] = None
    ) -> Dict:
        total_violations = counting_summary.get("total_count", 0)
        per_cat = counting_summary.get("per_category_count", {})
        cumulative = counting_summary.get("total_violation_counts", {})
        cumulative_total = sum(cumulative.values()) if cumulative else 0
        track_ids_info = self._get_track_ids_info(counting_summary.get("detections", []))
        current_timestamp = self._get_current_timestamp_str(stream_info)
        start_timestamp = self._get_start_timestamp_str(stream_info)
        human_text_lines = []
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
        human_text_lines.append("")
        human_text_lines.append(f"TOTAL SINCE {start_timestamp}:")
        human_text_lines.append(f"\t- Total PPE Violations Detected: {cumulative_total}")
        for cat in ["NO-Hardhat", "NO-Mask", "NO-Safety Vest"]:
            count = cumulative.get(cat, 0)
            if count > 0:
                label = self.CATEGORY_DISPLAY.get(cat, cat).replace(" Violations", "")
                human_text_lines.append(f"\t\t- {label}: {count}")
        human_text = "\n".join(human_text_lines)
        tracking_stat = {
            "input_timestamp": datetime.now(timezone.utc).strftime('%Y-%m-%d-%H:%M:%S.%f UTC'),
            "reset_timestamp": "00:00:00",
            "camera_info": self.get_camera_info_from_stream(stream_info),
            "total_counts": [
                {"category": cat, "count": cumulative.get(cat, 0)} for cat in ["NO-Hardhat", "NO-Mask", "NO-Safety Vest"]
            ],
            "current_counts": [
                {"category": cat, "count": per_cat.get(cat, 0)} for cat in ["NO-Hardhat", "NO-Mask", "NO-Safety Vest"] if per_cat.get(cat, 0) > 0
            ],
            "detections": counting_summary.get("detections", []),
            "alerts": [],
            "alert_settings": [],
            "reset_settings": [
                {
                    "interval_type": "daily",
                    "reset_time": {"value": 9, "time_unit": "hour"}
                }
            ],
            "human_text": human_text
        }
        return tracking_stat

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
