from typing import Any, Dict, List, Optional
from dataclasses import asdict, dataclass, field
import time
from datetime import datetime, timezone

from ..core.base import BaseProcessor, ProcessingContext, ProcessingResult, ConfigProtocol, ResultFormat
from ..utils import (
    filter_by_confidence,
    filter_by_categories,
    apply_category_mapping,
    count_objects_by_category,
    count_objects_in_zones,
    calculate_counting_summary,
    match_results_structure,
    bbox_smoothing,
    BBoxSmoothingConfig,
    BBoxSmoothingTracker
)
from ..core.config import BaseConfig, AlertConfig, ZoneConfig

@dataclass
class ChickenPoseDetectionConfig(BaseConfig):
    """Configuration for Chicken Pose Detection use case."""
    enable_smoothing: bool = True
    smoothing_algorithm: str = "observability"
    smoothing_window_size: int = 20
    smoothing_cooldown_frames: int = 5
    smoothing_confidence_range_factor: float = 0.5
    confidence_threshold: float = 0.6
    pose_categories: List[str] = field(
        default_factory=lambda: ['moving', 'eat-drink', 'rest']
    )
    target_pose_categories: List[str] = field(
        default_factory=lambda: ['moving', 'eat-drink', 'rest']
    )
    alert_config: Optional[AlertConfig] = None
    index_to_category: Optional[Dict[int, str]] = field(
        default_factory=lambda: {
            0: "moving",
            1: "eat-drink",
            2: "rest"
        }
    )

class ChickenPoseDetectionUseCase(BaseProcessor):
    def _get_track_ids_info(self, detections: list) -> Dict[str, Any]:
        frame_track_ids = set()
        for det in detections:
            tid = det.get('track_id')
            if tid is not None:
                frame_track_ids.add(tid)
        total_track_ids = set()
        for s in getattr(self, '_pose_total_track_ids', {}).values():
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
    def _deduplicate_chickens(detections, iou_thresh=0.7):
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
                        iou = ChickenPoseDetectionUseCase._iou(bbox1, bbox2)
                        if iou > iou_thresh:
                            used[j] = True
                            group.append(j)
            best_idx = max(group, key=lambda idx: detections[idx].get("confidence", 0))
            filtered.append(detections[best_idx])
            used[best_idx] = True
        return filtered

    def _update_pose_tracking_state(self, detections: list):
        if not hasattr(self, "_pose_total_track_ids"):
            self._pose_total_track_ids = {cat: set() for cat in self.pose_categories}
        self._pose_current_frame_track_ids = {cat: set() for cat in self.pose_categories}

        for det in detections:
            cat = det.get("category")
            raw_track_id = det.get("track_id")
            if cat not in self.pose_categories or raw_track_id is None:
                continue
            bbox = det.get("bounding_box", det.get("bbox"))
            canonical_id = self._merge_or_register_track(raw_track_id, bbox)
            det["track_id"] = canonical_id
            self._pose_total_track_ids.setdefault(cat, set()).add(canonical_id)
            self._pose_current_frame_track_ids[cat].add(canonical_id)

    def get_total_pose_counts(self):
        return {cat: len(ids) for cat, ids in getattr(self, '_pose_total_track_ids', {}).items()}

    def _format_timestamp_for_video(self, timestamp: float) -> str:
        hours = int(timestamp // 3600)
        minutes = int((timestamp % 3600) // 60)
        seconds = timestamp % 60
        return f"{hours:02d}:{minutes:02d}:{seconds:06.2f}"

    def _format_timestamp_for_stream(self, timestamp: float) -> str:
        dt = datetime.fromtimestamp(timestamp, tz=timezone.utc)
        return dt.strftime('%Y:%m:%d %H:%M:%S')

    def _get_current_timestamp_str(self, stream_info: Optional[Dict[str, Any]]) -> str:
        if not stream_info:
            return "00:00:00.00"
        if stream_info.get("input_settings", {}).get("stream_type", "video_file") == "video_file":
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

    def __init__(self):
        super().__init__("chicken_pose_detection")
        self.category = "agriculture"
        self.pose_categories = ['moving', 'eat-drink', 'rest']
        self.smoothing_tracker = None
        self.tracker = None
        self._total_frame_counter = 0
        self._global_frame_offset = 0
        self._tracking_start_time = None
        self._track_aliases: Dict[Any, Any] = {}
        self._canonical_tracks: Dict[Any, Dict[str, Any]] = {}
        self._track_merge_iou_threshold: float = 0.05
        self._track_merge_time_window: float = 7.0

    def process(self, data: Any, config: ConfigProtocol, context: Optional[ProcessingContext] = None, stream_info: Optional[Dict[str, Any]] = None) -> ProcessingResult:
        start_time = time.time()
        if not isinstance(config, ChickenPoseDetectionConfig):
            return self.create_error_result("Invalid config type", usecase=self.name, category=self.category, context=context)
        if context is None:
            context = ProcessingContext()

        input_format = match_results_structure(data)
        context.input_format = input_format
        context.confidence_threshold = config.confidence_threshold

        if config.confidence_threshold is not None:
            processed_data = filter_by_confidence(data, config.confidence_threshold)
            self.logger.debug(f"Applied confidence filtering with threshold {config.confidence_threshold}")
        else:
            processed_data = data
            self.logger.debug("Did not apply confidence filtering with threshold since nothing was provided")

        if config.index_to_category:
            processed_data = apply_category_mapping(processed_data, config.index_to_category)
            self.logger.debug("Applied category mapping")

        if config.target_pose_categories:
            processed_data = [d for d in processed_data if d.get('category') in self.pose_categories]
            self.logger.debug("Applied pose category filtering")

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
            smoothed_chickens = bbox_smoothing(processed_data, self.smoothing_tracker.config, self.smoothing_tracker)
            processed_data = smoothed_chickens

        try:
            from ..advanced_tracker import AdvancedTracker
            from ..advanced_tracker.config import TrackerConfig
            if self.tracker is None:
                tracker_config = TrackerConfig()
                self.tracker = AdvancedTracker(tracker_config)
                self.logger.info("Initialized AdvancedTracker for Chicken Pose Detection and tracking")
            processed_data = self.tracker.update(processed_data)
        except Exception as e:
            self.logger.warning(f"AdvancedTracker failed: {e}")

        processed_data = self._deduplicate_chickens(processed_data, iou_thresh=0.95)
        self._update_pose_tracking_state(processed_data)
        self._total_frame_counter += 1

        frame_number = None
        if stream_info:
            input_settings = stream_info.get("input_settings", {})
            start_frame = input_settings.get("start_frame")
            end_frame = input_settings.get("end_frame")
            if start_frame is not None and end_frame is not None and start_frame == end_frame:
                frame_number = start_frame

        general_counting_summary = calculate_counting_summary(data)
        counting_summary = self._count_categories(processed_data, config)
        total_pose_counts = self.get_total_pose_counts()
        counting_summary['total_pose_counts'] = total_pose_counts
        insights = self._generate_insights(counting_summary, config)
        alerts = self._check_alerts(counting_summary, config)
        predictions = self._extract_predictions(processed_data)
        summary = self._generate_summary(counting_summary, alerts)

        events_list = self._generate_events(counting_summary, alerts, config, frame_number, stream_info)
        tracking_stats_list = self._generate_tracking_stats(counting_summary, insights, summary, config, frame_number, stream_info)

        events = events_list[0] if events_list else {}
        tracking_stats = tracking_stats_list[0] if tracking_stats_list else {}

        context.mark_completed()
        result = self.create_result(
            data={
                "counting_summary": counting_summary,
                "general_counting_summary": general_counting_summary,
                "alerts": alerts,
                "total_chickens": counting_summary.get("total_count", 0),
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
        if self.tracker is not None:
            self.tracker.reset()
            self.logger.info("AdvancedTracker reset for new tracking session")

    def reset_pose_tracking(self) -> None:
        self._pose_total_track_ids = {cat: set() for cat in self.pose_categories}
        self._total_frame_counter = 0
        self._global_frame_offset = 0
        self._tracking_start_time = None
        self._track_aliases.clear()
        self._canonical_tracks.clear()
        self.logger.info("Chicken Pose Detection tracking state reset")

    def reset_all_tracking(self) -> None:
        self.reset_tracker()
        self.reset_pose_tracking()
        self.logger.info("All Chickens tracking state reset")

    def _generate_events(self, counting_summary: Dict, alerts: List, config: ChickenPoseDetectionConfig, frame_number: Optional[int] = None, stream_info: Optional[Dict[str, Any]] = None) -> List[Dict]:
        frame_key = str(frame_number) if frame_number is not None else "current_frame"
        events = [{frame_key: []}]
        frame_events = events[0][frame_key]
        total_chickens = counting_summary.get("total_count", 0)

        if total_chickens > 0:
            level = "info"
            intensity = 5.0
            if config.alert_config and config.alert_config.count_thresholds:
                threshold = config.alert_config.count_thresholds.get("all", 15)
                intensity = min(10.0, (total_chickens / threshold) * 10)
                if intensity >= 7:
                    level = "critical"
                elif intensity >= 5:
                    level = "warning"
                else:
                    level = "info"
            else:
                if total_chickens > 25:
                    level = "critical"
                    intensity = 9.0
                elif total_chickens > 15:
                    level = "warning"
                    intensity = 7.0
                else:
                    level = "info"
                    intensity = min(10.0, total_chickens / 3.0)

            human_text_lines = ["EVENTS DETECTED:"]
            human_text_lines.append(f"    - {total_chickens} Chicken(s) detected [INFO]")
            human_text = "\n".join(human_text_lines)

            event = {
                "type": "chicken_pose_detection",
                "stream_time": datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S UTC"),
                "level": level,
                "intensity": round(intensity, 1),
                "config": {
                    "min_value": 0,
                    "max_value": 10,
                    "level_settings": {"info": 2, "warning": 5, "critical": 7}
                },
                "application_name": "Chicken Pose Detection System",
                "application_version": "1.0",
                "location_info": None,
                "human_text": human_text
            }
            frame_events.append(event)

        for alert in alerts:
            total_chickens = counting_summary.get("total_count", 0)
            intensity_message = "ALERT: Low chicken density in the scene"
            if config.alert_config and config.alert_config.count_thresholds:
                threshold = config.alert_config.count_thresholds.get("all", 15)
                percentage = (total_chickens / threshold) * 100 if threshold > 0 else 0
                if percentage < 20:
                    intensity_message = "ALERT: Low chicken density in the scene"
                elif percentage <= 50:
                    intensity_message = "ALERT: Moderate chicken density in the scene"
                elif percentage <= 70:
                    intensity_message = "ALERT: High chicken density in the scene"
                else:
                    intensity_message = "ALERT: Severe chicken density in the scene"
            else:
                if total_chickens > 15:
                    intensity_message = "ALERT: High chicken density in the scene"
                elif total_chickens == 1:
                    intensity_message = "ALERT: Low chicken density in the scene"
                else:
                    intensity_message = "ALERT: Moderate chicken density in the scene"

            alert_event = {
                "type": alert.get("type", "density_alert"),
                "stream_time": datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S UTC"),
                "level": alert.get("severity", "warning"),
                "intensity": 8.0,
                "config": {
                    "min_value": 0,
                    "max_value": 10,
                    "level_settings": {"info": 2, "warning": 5, "critical": 7}
                },
                "application_name": "Chicken Density Alert System",
                "application_version": "1.0",
                "location_info": alert.get("zone"),
                "human_text": f"{datetime.now(timezone.utc).strftime('%Y-%m-%d-%H:%M:%S UTC')} : {intensity_message}"
            }
            frame_events.append(alert_event)

        return events

    def _generate_tracking_stats(
            self,
            counting_summary: Dict,
            insights: List[str],
            summary: str,
            config: ChickenPoseDetectionConfig,
            frame_number: Optional[int] = None,
            stream_info: Optional[Dict[str, Any]] = None
    ) -> List[Dict]:
        frame_key = str(frame_number) if frame_number is not None else "current_frame"
        tracking_stats = [{frame_key: []}]
        frame_tracking_stats = tracking_stats[0][frame_key]

        total_chickens = counting_summary.get("total_count", 0)
        total_pose_counts = counting_summary.get("total_pose_counts", {})
        cumulative_total = sum(total_pose_counts.values()) if total_pose_counts else 0
        per_category_count = counting_summary.get("per_category_count", {})

        track_ids_info = self._get_track_ids_info(counting_summary.get("detections", []))

        current_timestamp = self._get_current_timestamp_str(stream_info)
        start_timestamp = self._get_start_timestamp_str(stream_info)

        human_text_lines = []
        human_text_lines.append(f"CURRENT FRAME @ {current_timestamp}:")
        if total_chickens > 0:
            category_counts = [f"{count} {cat}" for cat, count in per_category_count.items() if count > 0]
            if len(category_counts) == 1:
                chickens_text = category_counts[0] + " detected"
            elif len(category_counts) == 2:
                chickens_text = f"{category_counts[0]} and {category_counts[1]} detected"
            else:
                chickens_text = f"{', '.join(category_counts[:-1])}, and {category_counts[-1]} detected"
            human_text_lines.append(f"\t- {chickens_text}")
        else:
            human_text_lines.append(f"\t- No chickens detected")

        human_text_lines.append("")
        human_text_lines.append(f"TOTAL SINCE {start_timestamp}:")
        human_text_lines.append(f"\t- Total Chickens Detected: {cumulative_total}")
        if total_pose_counts:
            for cat, count in total_pose_counts.items():
                if count > 0:
                    human_text_lines.append(f"\t- {cat}: {count}")

        human_text = "\n".join(human_text_lines)

        tracking_stat = {
            "type": "chicken_pose_tracking",
            "category": "chicken",
            "count": total_chickens,
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

    def _count_categories(self, detections: list, config: ChickenPoseDetectionConfig) -> dict:
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

    CATEGORY_DISPLAY = {
        "Moving": "moving",
        "Eat-Drink": "eat-drink",
        "Rest": "rest"
    }

    def _generate_insights(self, summary: dict, config: ChickenPoseDetectionConfig) -> List[str]:
        insights = []
        per_cat = summary.get("per_category_count", {})
        total_chickens = summary.get("total_count", 0)

        if total_chickens == 0:
            insights.append("No chickens detected in the scene")
            return insights
        insights.append(f"EVENT: Detected {total_chickens} chickens in the scene")
        intensity_threshold = None
        if config.alert_config and config.alert_config.count_thresholds and "all" in config.alert_config.count_thresholds:
            intensity_threshold = config.alert_config.count_thresholds["all"]
        
        if intensity_threshold is not None:
            percentage = (total_chickens / intensity_threshold) * 100
            if percentage < 20:
                insights.append(f"INTENSITY: Low chicken density in the scene ({percentage:.1f}% of capacity)")
            elif percentage <= 50:
                insights.append(f"INTENSITY: Moderate chicken density in the scene ({percentage:.1f}% of capacity)")
            elif percentage <= 70:
                insights.append(f"INTENSITY: High chicken density in the scene ({percentage:.1f}% of capacity)")
            else:
                insights.append(f"INTENSITY: Severe chicken density in the scene ({percentage:.1f}% of capacity)")

        for cat, count in per_cat.items():
            display = self.CATEGORY_DISPLAY.get(cat, cat)
            insights.append(f"{display}: {count}")
        return insights

    def _check_alerts(self, summary: dict, config: ChickenPoseDetectionConfig) -> List[Dict]:
        alerts = []
        if not config.alert_config:
            return alerts
        total = summary.get("total_count", 0)
        if config.alert_config.count_thresholds:
            for category, threshold in config.alert_config.count_thresholds.items():
                if category == "all" and total >= threshold:
                    alerts.append({
                        "type": "count_threshold",
                        "severity": "warning",
                        "message": f"Total chicken count ({total}) exceeds threshold ({threshold})",
                        "category": category,
                        "current_count": total,
                        "threshold": threshold
                    })
                elif category in summary.get("per_category_count", {}):
                    count = summary.get("per_category_count", {})[category]
                    if count >= threshold:
                        alerts.append({
                            "type": "count_threshold",
                            "severity": "warning",
                            "message": f"{category} count ({count}) exceeds threshold ({threshold})",
                            "category": category,
                            "current_count": count,
                            "threshold": threshold
                        })
        return alerts

    def _extract_predictions(self, detections: list) -> List[Dict[str, Any]]:
        return [
            {
                "category": det.get("category", "unknown"),
                "confidence": det.get("confidence", 0.0),
                "bounding_box": det.get("bounding_box", {})
            }
            for det in detections
        ]

    def _generate_summary(self, summary: dict, alerts: List) -> str:
        total = summary.get("total_count", 0)
        per_cat = summary.get("per_category_count", {})
        cumulative = summary.get("total_pose_counts", {})
        cumulative_total = sum(cumulative.values()) if cumulative else 0
        lines = []
        if total > 0:
            lines.append(f"{total} Chicken(s) detected")
            if per_cat:
                lines.append("Chickens:")
                for cat, count in per_cat.items():
                    lines.append(f"\t{cat}: {count}")
        else:
            lines.append("No chickens detected")
        lines.append(f"Total chickens detected: {cumulative_total}")
        if alerts:
            lines.append(f"{len(alerts)} alert(s)")
        return "\n".join(lines)

    def _compute_iou(self, box1: Any, box2: Any) -> float:
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
                values = [v for v in bbox.values() if isinstance(v, (int, float))]
                return values[:4] if len(values) >= 4 else []
            return []

        l1 = _bbox_to_list(box1)
        l2 = _bbox_to_list(box2)
        if len(l1) < 4 or len(l2) < 4:
            return 0.0
        x1_min, y1_min, x1_max, y1_max = l1
        x2_min, y2_min, x2_max, y2_max = l2
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
        if raw_id is None or bbox is None:
            return raw_id
        now = time.time()
        if raw_id in self._track_aliases:
            canonical_id = self._track_aliases[raw_id]
            track_info = self._canonical_tracks.get(canonical_id)
            if track_info is not None:
                track_info["last_bbox"] = bbox
                track_info["last_update"] = now
                track_info["raw_ids"].add(raw_id)
            return canonical_id
        for canonical_id, info in self._canonical_tracks.items():
            if now - info["last_update"] > self._track_merge_time_window:
                continue
            iou = self._compute_iou(bbox, info["last_bbox"])
            if iou >= self._track_merge_iou_threshold:
                self._track_aliases[raw_id] = canonical_id
                info["last_bbox"] = bbox
                info["last_update"] = now
                info["raw_ids"].add(raw_id)
                return canonical_id
        canonical_id = raw_id
        self._track_aliases[raw_id] = canonical_id
        self._canonical_tracks[canonical_id] = {
            "last_bbox": bbox,
            "last_update": now,
            "raw_ids": {raw_id},
        }
        return canonical_id

    def _format_timestamp(self, timestamp: float) -> str:
        return datetime.fromtimestamp(timestamp, timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')

    def _get_tracking_start_time(self) -> str:
        if self._tracking_start_time is None:
            return "N/A"
        return self._format_timestamp(self._tracking_start_time)

    def _set_tracking_start_time(self) -> None:
        self._tracking_start_time = time.time()