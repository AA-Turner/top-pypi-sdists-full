from typing import Any, Dict, List, Optional
from dataclasses import asdict
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
from dataclasses import dataclass, field
from ..core.config import BaseConfig, AlertConfig, ZoneConfig

@dataclass
class AbandonedObjectConfig(BaseConfig):
    """Configuration for abandoned object detection use case."""
    enable_smoothing: bool = True
    smoothing_algorithm: str = "observability"
    smoothing_window_size: int = 20
    smoothing_cooldown_frames: int = 5
    smoothing_confidence_range_factor: float = 0.5
    confidence_threshold: float = 0.4
    usecase_categories: List[str] = field(
        default_factory=lambda: ['backpack', 'handbag', 'suitcase']
    )
    target_categories: List[str] = field(
        default_factory=lambda: ['backpack', 'handbag', 'suitcase']
    )
    alert_config: Optional[AlertConfig] = None
    index_to_category: Optional[Dict[int, str]] = field(
        default_factory=lambda: {
            24: "backpack",
            26: "handbag",
            28: "suitcase"
        }
    )
    stationary_threshold_frames: int = 60  # Frames to consider object abandoned
    person_category: str = "person"
    person_index: int = 0

class AbandonedObjectDetectionUseCase(BaseProcessor):
    CATEGORY_DISPLAY = {
        "backpack": "backpack",
        "handbag": "handbag",
        "suitcase": "suitcase"
    }
    
    def __init__(self):
        super().__init__("abandoned_object_detection")
        self.category = "security"
        self.CASE_TYPE: Optional[str] = 'abandoned_object_detection'
        self.CASE_VERSION: Optional[str] = '1.0'
        self.target_categories = ['backpack', 'handbag', 'suitcase']
        self.smoothing_tracker = None
        self.tracker = None
        self._total_frame_counter = 0
        self._global_frame_offset = 0
        self._tracking_start_time = None
        self._track_aliases: Dict[Any, Any] = {}
        self._canonical_tracks: Dict[Any, Dict[str, Any]] = {}
        self._track_merge_iou_threshold: float = 0.05
        self._track_merge_time_window: float = 7.0
        self._ascending_alert_list: List[int] = []
        self.current_incident_end_timestamp: str = "N/A"
        self._stationary_tracks: Dict[Any, Dict[str, Any]] = {}  # Track stationary objects
        self._person_bboxes: List[Dict] = []  # Store person bboxes for overlap check

    def process(self, data: Any, config: ConfigProtocol, context: Optional[ProcessingContext] = None,
                stream_info: Optional[Dict[str, Any]] = None) -> ProcessingResult:
        start_time = time.time()
        if not isinstance(config, AbandonedObjectConfig):
            return self.create_error_result("Invalid config type", usecase=self.name, category=self.category, context=context)
        if context is None:
            context = ProcessingContext()

        input_format = match_results_structure(data)
        context.input_format = input_format
        context.confidence_threshold = config.confidence_threshold

        processed_data = filter_by_confidence(data, config.confidence_threshold)
        if config.index_to_category:
            processed_data = apply_category_mapping(processed_data, config.index_to_category)
        processed_data = [d for d in processed_data if d.get('category') in self.target_categories or d.get('category') == config.person_category]

        # Store person bboxes for overlap check
        self._person_bboxes = [d.get('bounding_box') for d in processed_data if d.get('category') == config.person_category]

        # Apply bbox smoothing
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
            processed_data = bbox_smoothing(processed_data, self.smoothing_tracker.config, self.smoothing_tracker)

        # Advanced tracking
        try:
            from ..advanced_tracker import AdvancedTracker
            from ..advanced_tracker.config import TrackerConfig
            if self.tracker is None:
                tracker_config = TrackerConfig()
                self.tracker = AdvancedTracker(tracker_config)
            processed_data = self.tracker.update(processed_data)
        except Exception as e:
            self.logger.warning(f"AdvancedTracker failed: {e}")

        # Check for stationary objects
        abandoned_data = self._check_stationary_objects(processed_data, config)

        self._update_tracking_state(abandoned_data)
        self._total_frame_counter += 1

        frame_number = None
        if stream_info:
            input_settings = stream_info.get("input_settings", {})
            start_frame = input_settings.get("start_frame")
            end_frame = input_settings.get("end_frame")
            if start_frame is not None and end_frame is not None and start_frame == end_frame:
                frame_number = start_frame

        counting_summary = self._count_categories(abandoned_data, config)
        total_counts = self.get_total_counts()
        counting_summary['total_counts'] = total_counts
        alerts = self._check_alerts(counting_summary, frame_number, config)
        predictions = self._extract_predictions(abandoned_data)

        incidents_list = self._generate_incidents(counting_summary, alerts, config, frame_number, stream_info)
        tracking_stats_list = self._generate_tracking_stats(counting_summary, alerts, config, frame_number, stream_info)
        business_analytics_list = self._generate_business_analytics(counting_summary, alerts, config, stream_info, is_empty=True)
        summary_list = self._generate_summary(counting_summary, incidents_list, tracking_stats_list, business_analytics_list, alerts)

        incidents = incidents_list[0] if incidents_list else {}
        tracking_stats = tracking_stats_list[0] if tracking_stats_list else {}
        business_analytics = business_analytics_list[0] if business_analytics_list else {}
        summary = summary_list[0] if summary_list else {}
        agg_summary = {str(frame_number): {
            "incidents": incidents,
            "tracking_stats": tracking_stats,
            "business_analytics": business_analytics,
            "alerts": alerts,
            "human_text": summary}
        }

        context.mark_completed()
        result = self.create_result(
            data={"agg_summary": agg_summary},
            usecase=self.name,
            category=self.category,
            context=context
        )
        return result

    def _check_stationary_objects(self, data: List[Dict], config: AbandonedObjectConfig) -> List[Dict]:
        """Check if objects are stationary and not overlapping with persons."""
        abandoned_data = []
        current_time = time.time()

        for det in data:
            if det.get('category') not in self.target_categories:
                continue
            track_id = det.get('track_id')
            bbox = det.get('bounding_box')
            if not track_id or not bbox:
                continue

            # Calculate centroid
            centroid = self._calculate_centroid(bbox)
            if track_id not in self._stationary_tracks:
                self._stationary_tracks[track_id] = {
                    'centroid': centroid,
                    'frame_count': 1,
                    'start_time': current_time,
                    'bbox': bbox
                }
            else:
                track_info = self._stationary_tracks[track_id]
                prev_centroid = track_info['centroid']
                track_info['frame_count'] += 1
                track_info['bbox'] = bbox

                # Check if centroid has moved significantly
                if self._is_centroid_stationary(centroid, prev_centroid):
                    if track_info['frame_count'] >= config.stationary_threshold_frames:
                        # Check for overlap with person
                        if not self._overlaps_with_person(bbox):
                            det['category'] = 'abandoned_object'
                            abandoned_data.append(det)
                    track_info['centroid'] = centroid
                else:
                    # Reset if centroid moves
                    track_info['centroid'] = centroid
                    track_info['frame_count'] = 1
                    track_info['start_time'] = current_time

        return abandoned_data

    def _calculate_centroid(self, bbox: Dict) -> tuple:
        """Calculate centroid of a bounding box."""
        if 'xmin' in bbox:
            x = (bbox['xmin'] + bbox['xmax']) / 2
            y = (bbox['ymin'] + bbox['ymax']) / 2
        elif 'x1' in bbox:
            x = (bbox['x1'] + bbox['x2']) / 2
            y = (bbox['y1'] + bbox['y2']) / 2
        else:
            return (0, 0)
        return (x, y)

    def _is_centroid_stationary(self, centroid: tuple, prev_centroid: tuple, threshold: float = 5.0) -> bool:
        """Check if centroid movement is within threshold."""
        x1, y1 = centroid
        x2, y2 = prev_centroid
        distance = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
        return distance < threshold

    def _overlaps_with_person(self, bbox: Dict) -> bool:
        """Check if bbox overlaps with any person bbox."""
        for person_bbox in self._person_bboxes:
            if person_bbox and self._compute_iou(bbox, person_bbox) > 0.1:
                return True
        return False

    def _check_alerts(self, summary: dict, frame_number: Any, config: AbandonedObjectConfig) -> List[Dict]:
        def get_trend(data, lookback=900, threshold=0.6):
            window = data[-lookback:] if len(data) >= lookback else data
            if len(window) < 2:
                return True
            increasing = sum(1 for i in range(1, len(window)) if window[i] >= window[i - 1])
            ratio = increasing / (len(window) - 1)
            return ratio >= threshold

        frame_key = str(frame_number) if frame_number is not None else "current_frame"
        alerts = []
        total_detections = summary.get("total_count", 0)
        total_counts_dict = summary.get("total_counts", {})
        per_category_count = summary.get("per_category_count", {})

        if not config.alert_config:
            return alerts

        if hasattr(config.alert_config, 'count_thresholds') and config.alert_config.count_thresholds:
            for category, threshold in config.alert_config.count_thresholds.items():
                if category == "all" and total_detections > threshold:
                    alerts.append({
                        "alert_type": getattr(config.alert_config, 'alert_type', ['Default']),
                        "alert_id": f"alert_{category}_{frame_key}",
                        "incident_category": self.CASE_TYPE,
                        "threshold_level": threshold,
                        "ascending": get_trend(self._ascending_alert_list, lookback=900, threshold=0.8),
                        "settings": {t: v for t, v in zip(getattr(config.alert_config, 'alert_type', ['Default']),
                                                         getattr(config.alert_config, 'alert_value', ['JSON']))}
                    })
                elif category == "abandoned_object" and per_category_count.get(category, 0) > threshold:
                    alerts.append({
                        "alert_type": getattr(config.alert_config, 'alert_type', ['Default']),
                        "alert_id": f"alert_{category}_{frame_key}",
                        "incident_category": self.CASE_TYPE,
                        "threshold_level": threshold,
                        "ascending": get_trend(self._ascending_alert_list, lookback=900, threshold=0.8),
                        "settings": {t: v for t, v in zip(getattr(config.alert_config, 'alert_type', ['Default']),
                                                         getattr(config.alert_config, 'alert_value', ['JSON']))}
                    })
        return alerts

    def _generate_incidents(self, counting_summary: Dict, alerts: List, config: AbandonedObjectConfig,
                           frame_number: Optional[int] = None, stream_info: Optional[Dict[str, Any]] = None) -> List[Dict]:
        incidents = []
        total_detections = counting_summary.get("total_count", 0)
        current_timestamp = self._get_current_timestamp_str(stream_info)
        camera_info = self.get_camera_info_from_stream(stream_info)
        
        self._ascending_alert_list = self._ascending_alert_list[-900:] if len(self._ascending_alert_list) > 900 else self._ascending_alert_list
        
        if total_detections > 0:
            level = "low"
            intensity = 5.0
            start_timestamp = self._get_start_timestamp_str(stream_info)
            if start_timestamp and self.current_incident_end_timestamp == 'N/A':
                self.current_incident_end_timestamp = 'Incident still active'
            elif start_timestamp and self.current_incident_end_timestamp == 'Incident still active':
                if len(self._ascending_alert_list) >= 15 and sum(self._ascending_alert_list[-15:]) / 15 < 1.5:
                    self.current_incident_end_timestamp = current_timestamp
            elif self.current_incident_end_timestamp != 'Incident still active' and self.current_incident_end_timestamp != 'N/A':
                self.current_incident_end_timestamp = 'N/A'

            if config.alert_config and config.alert_config.count_thresholds:
                threshold = config.alert_config.count_thresholds.get("all", 15)
                intensity = min(10.0, (total_detections / threshold) * 10)
                if intensity >= 9:
                    level = "critical"
                    self._ascending_alert_list.append(3)
                elif intensity >= 7:
                    level = "significant"
                    self._ascending_alert_list.append(2)
                elif intensity >= 5:
                    level = "medium"
                    self._ascending_alert_list.append(1)
                else:
                    level = "low"
                    self._ascending_alert_list.append(0)
            else:
                if total_detections > 30:
                    level = "critical"
                    intensity = 10.0
                    self._ascending_alert_list.append(3)
                elif total_detections > 25:
                    level = "significant"
                    intensity = 9.0
                    self._ascending_alert_list.append(2)
                elif total_detections > 15:
                    level = "medium"
                    intensity = 7.0
                    self._ascending_alert_list.append(1)
                else:
                    level = "low"
                    intensity = min(10.0, total_detections / 3.0)
                    self._ascending_alert_list.append(0)

            human_text_lines = [f"ABANDONED OBJECT DETECTED @ {current_timestamp}:"]
            human_text_lines.append(f"\tSeverity Level: {(self.CASE_TYPE, level)}")
            human_text = "\n".join(human_text_lines)

            alert_settings = []
            if config.alert_config and hasattr(config.alert_config, 'alert_type'):
                alert_settings.append({
                    "alert_type": getattr(config.alert_config, 'alert_type', ['Default']),
                    "incident_category": self.CASE_TYPE,
                    "threshold_level": config.alert_config.count_thresholds if hasattr(config.alert_config, 'count_thresholds') else {},
                    "ascending": True,
                    "settings": {t: v for t, v in zip(getattr(config.alert_config, 'alert_type', ['Default']),
                                                     getattr(config.alert_config, 'alert_value', ['JSON']))}
                })

            event = self.create_incident(
                incident_id=self.CASE_TYPE + '_' + str(frame_number),
                incident_type=self.CASE_TYPE,
                severity_level=level,
                human_text=human_text,
                camera_info=camera_info,
                alerts=alerts,
                alert_settings=alert_settings,
                start_time=start_timestamp,
                end_time=self.current_incident_end_timestamp,
                level_settings={"low": 1, "medium": 3, "significant": 4, "critical": 7}
            )
            incidents.append(event)
        else:
            self._ascending_alert_list.append(0)
            incidents.append({})

        return incidents

    def _generate_tracking_stats(self, counting_summary: Dict, alerts: List, config: AbandonedObjectConfig,
                                frame_number: Optional[int] = None, stream_info: Optional[Dict[str, Any]] = None) -> List[Dict]:
        camera_info = self.get_camera_info_from_stream(stream_info)
        tracking_stats = []
        total_detections = counting_summary.get("total_count", 0)
        total_counts_dict = counting_summary.get("total_counts", {})
        per_category_count = counting_summary.get("per_category_count", {})
        current_timestamp = self._get_current_timestamp_str(stream_info, precision=False)
        start_timestamp = self._get_start_timestamp_str(stream_info, precision=False)
        high_precision_start_timestamp = self._get_current_timestamp_str(stream_info, precision=True)
        high_precision_reset_timestamp = self._get_start_timestamp_str(stream_info, precision=True)

        total_counts = [{"category": cat, "count": count} for cat, count in total_counts_dict.items() if count > 0]
        current_counts = [{"category": cat, "count": count} for cat, count in per_category_count.items() if count > 0 or total_detections > 0]

        detections = []
        for detection in counting_summary.get("detections", []):
            bbox = detection.get("bounding_box", {})
            category = detection.get("category", "abandoned_object")
            detection_obj = self.create_detection_object(category, bbox)
            detections.append(detection_obj)

        alert_settings = []
        if config.alert_config and hasattr(config.alert_config, 'alert_type'):
            alert_settings.append({
                "alert_type": getattr(config.alert_config, 'alert_type', ['Default']),
                "incident_category": self.CASE_TYPE,
                "threshold_level": config.alert_config.count_thresholds if hasattr(config.alert_config, 'count_thresholds') else {},
                "ascending": True,
                "settings": {t: v for t, v in zip(getattr(config.alert_config, 'alert_type', ['Default']),
                                                 getattr(config.alert_config, 'alert_value', ['JSON']))}
            })

        human_text_lines = [f"Tracking Statistics:"]
        human_text_lines.append(f"CURRENT FRAME @ {current_timestamp}")
        for cat, count in per_category_count.items():
            human_text_lines.append(f"\t{cat}: {count}")
        human_text_lines.append(f"TOTAL SINCE {start_timestamp}")
        for cat, count in total_counts_dict.items():
            if count > 0:
                human_text_lines.append(f"\t{cat}: {count}")
        human_text_lines.append(f"Alerts: {alerts[0].get('settings', {}) if alerts else 'None'} sent @ {current_timestamp}")
        human_text = "\n".join(human_text_lines)

        reset_settings = [{"interval_type": "daily", "reset_time": {"value": 9, "time_unit": "hour"}}]

        tracking_stat = self.create_tracking_stats(
            total_counts=total_counts,
            current_counts=current_counts,
            detections=detections,
            human_text=human_text,
            camera_info=camera_info,
            alerts=alerts,
            alert_settings=alert_settings,
            reset_settings=reset_settings,
            start_time=high_precision_start_timestamp,
            reset_time=high_precision_reset_timestamp
        )
        tracking_stats.append(tracking_stat)
        return tracking_stats

    def _generate_business_analytics(self, counting_summary: Dict, alerts: Any, config: AbandonedObjectConfig,
                                    stream_info: Optional[Dict[str, Any]] = None, is_empty=False) -> List[Dict]:
        if is_empty:
            return []
        return []

    def _generate_summary(self, summary: dict, incidents: List, tracking_stats: List, business_analytics: List, alerts: List) -> List[str]:
        lines = {}
        lines["Application Name"] = self.CASE_TYPE
        lines["Application Version"] = self.CASE_VERSION
        if len(incidents) > 0:
            lines["Incidents:"] = f"\n\t{incidents[0].get('human_text', 'No incidents detected')}\n"
        if len(tracking_stats) > 0:
            lines["Tracking Statistics:"] = f"\t{tracking_stats[0].get('human_text', 'No tracking statistics detected')}\n"
        if len(business_analytics) > 0:
            lines["Business Analytics:"] = f"\t{business_analytics[0].get('human_text', 'No business analytics detected')}\n"
        if len(incidents) == 0 and len(tracking_stats) == 0 and len(business_analytics) == 0:
            lines["Summary"] = "No Summary Data"
        return [lines]

    def _get_track_ids_info(self, detections: list) -> Dict[str, Any]:
        frame_track_ids = {det.get('track_id') for det in detections if det.get('track_id') is not None}
        total_track_ids = set()
        for s in getattr(self, '_per_category_total_track_ids', {}).values():
            total_track_ids.update(s)
        return {
            "total_count": len(total_track_ids),
            "current_frame_count": len(frame_track_ids),
            "total_unique_track_ids": len(total_track_ids),
            "current_frame_track_ids": list(frame_track_ids),
            "last_update_time": time.time(),
            "total_frames_processed": getattr(self, '_total_frame_counter', 0)
        }

    def _update_tracking_state(self, detections: list):
        if not hasattr(self, "_per_category_total_track_ids"):
            self._per_category_total_track_ids = {cat: set() for cat in self.target_categories + ['abandoned_object']}
        self._current_frame_track_ids = {cat: set() for cat in self.target_categories + ['abandoned_object']}

        for det in detections:
            cat = det.get("category")
            raw_track_id = det.get("track_id")
            if cat not in self.target_categories + ['abandoned_object'] or raw_track_id is None:
                continue
            bbox = det.get("bounding_box", det.get("bbox"))
            canonical_id = self._merge_or_register_track(raw_track_id, bbox)
            det["track_id"] = canonical_id
            self._per_category_total_track_ids.setdefault(cat, set()).add(canonical_id)
            self._current_frame_track_ids[cat].add(canonical_id)

    def get_total_counts(self):
        return {cat: len(ids) for cat, ids in getattr(self, '_per_category_total_track_ids', {}).items()}

    def _format_timestamp_for_stream(self, timestamp: float) -> str:
        dt = datetime.fromtimestamp(timestamp, tz=timezone.utc)
        return dt.strftime('%Y:%m:%d %H:%M:%S')

    def _format_timestamp_for_video(self, timestamp: float) -> str:
        hours = int(timestamp // 3600)
        minutes = int((timestamp % 3600) // 60)
        seconds = round(float(timestamp % 60), 2)
        return f"{hours:02d}:{minutes:02d}:{seconds:.1f}"

    def _get_current_timestamp_str(self, stream_info: Optional[Dict[str, Any]], precision=False, frame_id: Optional[str] = None) -> str:
        if not stream_info:
            return "00:00:00.00" if precision else "00:00:00"
        if precision:
            if stream_info.get("input_settings", {}).get("start_frame", "na") != "na":
                start_time = (int(frame_id) if frame_id else stream_info.get("input_settings", {}).get("start_frame", 30)) / stream_info.get("input_settings", {}).get("original_fps", 30)
                return self._format_timestamp_for_video(start_time)
            return datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")
        if stream_info.get("input_settings", {}).get("start_frame", "na") != "na":
            start_time = (int(frame_id) if frame_id else stream_info.get("input_settings", {}).get("start_frame", 30)) / stream_info.get("input_settings", {}).get("original_fps", 30)
            return self._format_timestamp_for_video(start_time)
        stream_time_str = stream_info.get("input_settings", {}).get("stream_info", {}).get("stream_time", "")
        if stream_time_str:
            try:
                timestamp_str = stream_time_str.replace(" UTC", "")
                dt = datetime.strptime(timestamp_str, "%Y-%m-%d-%H:%M:%S.%f")
                timestamp = dt.replace(tzinfo=timezone.utc).timestamp()
                return self._format_timestamp_for_stream(timestamp)
            except:
                return self._format_timestamp_for_stream(time.time())
        return self._format_timestamp_for_stream(time.time())

    def _get_start_timestamp_str(self, stream_info: Optional[Dict[str, Any]], precision=False) -> str:
        if not stream_info:
            return "00:00:00"
        if precision:
            if stream_info.get("input_settings", {}).get("start_frame", "na") != "na":
                return "00:00:00"
            return datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")
        if stream_info.get("input_settings", {}).get("start_frame", "na") != "na":
            return "00:00:00"
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

    def _count_categories(self, detections: list, config: AbandonedObjectConfig) -> dict:
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

    def _extract_predictions(self, detections: list) -> List[Dict[str, Any]]:
        return [
            {
                "category": det.get("category", "unknown"),
                "confidence": det.get("confidence", 0.0),
                "bounding_box": det.get("bounding_box", {})
            }
            for det in detections
        ]

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