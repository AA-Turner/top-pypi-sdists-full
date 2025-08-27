from typing import Any, Dict, List, Optional, Tuple
from dataclasses import asdict
import time
from datetime import datetime, timezone

from ..core.base import BaseProcessor, ProcessingContext, ProcessingResult, ConfigProtocol
from ..utils import (
    filter_by_confidence,
    apply_category_mapping,
    count_objects_by_category,
    count_objects_in_zones,
    calculate_counting_summary,
    match_results_structure,
    bbox_smoothing,
    BBoxSmoothingConfig,
    BBoxSmoothingTracker,
    get_bbox_center,
    point_in_polygon
)
from dataclasses import dataclass, field
from ..core.config import BaseConfig, AlertConfig

@dataclass
class DwellConfig(BaseConfig):
    """Configuration for dwell detection use case."""
    enable_smoothing: bool = True
    centroid_threshold: float = 10.0
    smoothing_algorithm: str = "observability"
    smoothing_window_size: int = 20
    smoothing_cooldown_frames: int = 5
    smoothing_confidence_range_factor: float = 0.5
    confidence_threshold: float = 0.6
    dwell_threshold: int = 300  # Frames to consider a person as dwelling
    usecase_categories: List[str] = field(default_factory=lambda: ['person'])
    target_categories: List[str] = field(default_factory=lambda: ['person'])
    alert_config: Optional[AlertConfig] = None
    zone_config: Optional[Dict[str, Dict[str, List[List[float]]]]] = None
    index_to_category: Optional[Dict[int, str]] = field(
        default_factory=lambda: {0: "person"}
    )
    person_index: int = 0

class DwellUseCase(BaseProcessor):
    CATEGORY_DISPLAY = {"person": "Person"}

    def __init__(self):
        super().__init__("dwell")
        self.category = "general"
        self.CASE_TYPE: Optional[str] = 'dwell'
        self.CASE_VERSION: Optional[str] = '1.0'
        self.target_categories = ['person']
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
        self._stationary_tracks: Dict[Any, Dict[str, Any]] = {}
        self._zone_current_track_ids: Dict[str, set] = {}
        self._zone_total_track_ids: Dict[str, set] = {}
        self._zone_current_counts: Dict[str, int] = {}
        self._zone_total_counts: Dict[str, int] = {}
        self.start_timer = None

    def process(self, data: Any, config: ConfigProtocol, context: Optional[ProcessingContext] = None,
                stream_info: Optional[Dict[str, Any]] = None) -> ProcessingResult:
        start_time = time.time()
        if not isinstance(config, DwellConfig):
            return self.create_error_result("Invalid config type", usecase=self.name, category=self.category, context=context)
        if context is None:
            context = ProcessingContext()

        input_format = match_results_structure(data)
        context.input_format = input_format
        context.confidence_threshold = config.confidence_threshold

        processed_data = filter_by_confidence(data, config.confidence_threshold)
        if config.index_to_category:
            processed_data = apply_category_mapping(processed_data, config.index_to_category)
        processed_data = [d for d in processed_data if d.get('category') in self.target_categories]

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

        try:
            from ..advanced_tracker import AdvancedTracker
            from ..advanced_tracker.config import TrackerConfig
            if self.tracker is None:
                tracker_config = TrackerConfig()
                self.tracker = AdvancedTracker(tracker_config)
            processed_data = self.tracker.update(processed_data)
        except Exception as e:
            self.logger.warning(f"AdvancedTracker failed: {e}")

        dwell_data = self._check_dwell_objects(processed_data, config)
        self._update_tracking_state(dwell_data)
        self._total_frame_counter += 1

        frame_number = None
        if stream_info:
            input_settings = stream_info.get("input_settings", {})
            start_frame = input_settings.get("start_frame")
            end_frame = input_settings.get("end_frame")
            if start_frame is not None and end_frame is not None and start_frame == end_frame:
                frame_number = start_frame

        counting_summary = self._count_categories(dwell_data, config)
        total_counts = self.get_total_counts()
        counting_summary['total_counts'] = total_counts

        zone_analysis = {}
        if config.zone_config and config.zone_config['zones']:
            frame_data = processed_data
            zone_analysis = count_objects_in_zones(frame_data, config.zone_config['zones'])
            if zone_analysis:
                zone_analysis = self._update_zone_tracking(zone_analysis, dwell_data, config)

        alerts = self._check_alerts(counting_summary, zone_analysis, frame_number, config)
        predictions = self._extract_predictions(dwell_data)

        incidents_list = self._generate_incidents(counting_summary, zone_analysis, alerts, config, frame_number, stream_info)
        tracking_stats_list = self._generate_tracking_stats(counting_summary, zone_analysis, alerts, config, frame_number, stream_info)
        business_analytics_list = self._generate_business_analytics(counting_summary, zone_analysis, alerts, config, stream_info, is_empty=True)
        summary_list = self._generate_summary(counting_summary, zone_analysis, incidents_list, tracking_stats_list, business_analytics_list, alerts)

        incidents = incidents_list[0] if incidents_list else {}
        tracking_stats = tracking_stats_list[0] if tracking_stats_list else {}
        business_analytics = business_analytics_list[0] if business_analytics_list else {}
        summary = summary_list[0] if summary_list else {}
        agg_summary = {str(frame_number): {
            "incidents": incidents,
            "tracking_stats": tracking_stats,
            "business_analytics": business_analytics,
            "alerts": alerts,
            "zone_analysis": zone_analysis,
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

    def _check_dwell_objects(self, data: List[Dict], config: DwellConfig) -> List[Dict]:
        dwell_data = []
        current_time = time.time()

        for det in data:
            if det.get('category') not in self.target_categories:
                continue
            track_id = det.get('track_id')
            bbox = det.get('bounding_box')
            if not track_id or not bbox:
                continue

            centroid = self._calculate_centroid(bbox)
            in_zone = self._is_in_zone(bbox, config.zone_config['zones'] if config.zone_config else None)

            if track_id not in self._stationary_tracks:
                self._stationary_tracks[track_id] = {
                    'centroid': centroid,
                    'frame_count': 1,
                    'start_time': current_time,
                    'bbox': bbox,
                    'in_zone': in_zone
                }
                track_info = self._stationary_tracks[track_id]
                if track_info['frame_count'] >= config.dwell_threshold and in_zone:
                    det['category'] = 'dwell_person'
                    dwell_data.append(det)
            else:
                track_info = self._stationary_tracks[track_id]
                prev_centroid = track_info['centroid']
                track_info['frame_count'] += 1
                track_info['bbox'] = bbox
                track_info['in_zone'] = in_zone

                if self._is_centroid_stationary(centroid, prev_centroid, config.centroid_threshold):
                    if track_info['frame_count'] >= config.dwell_threshold and in_zone:
                        det['category'] = 'dwell_person'
                        dwell_data.append(det)
                else:
                    track_info['frame_count'] = max(1, track_info['frame_count'] - 5)
                    track_info['centroid'] = centroid
                    track_info['start_time'] = current_time

        return dwell_data

    def _calculate_centroid(self, bbox: Dict) -> tuple:
        if 'xmin' in bbox:
            x = (bbox['xmin'] + bbox['xmax']) / 2
            y = (bbox['ymin'] + bbox['ymax']) / 2
        elif 'x1' in bbox:
            x = (bbox['x1'] + bbox['x2']) / 2
            y = (bbox['y1'] + bbox['y2']) / 2
        else:
            return (0, 0)
        return (x, y)

    def _is_centroid_stationary(self, centroid: tuple, prev_centroid: tuple, threshold: float) -> bool:
        x1, y1 = centroid
        x2, y2 = prev_centroid
        distance = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
        return distance < threshold

    def _is_in_zone(self, bbox: Dict, zones: Optional[Dict[str, List[List[float]]]]) -> bool:
        if not zones:
            return True
        center = get_bbox_center(bbox)
        for zone_name, zone_polygon in zones.items():
            polygon_points = [(point[0], point[1]) for point in zone_polygon]
            if point_in_polygon(center, polygon_points):
                return True
        return False

    def _update_zone_tracking(self, zone_analysis: Dict[str, Dict[str, int]], detections: List[Dict], config: DwellConfig) -> Dict[str, Dict[str, Any]]:
        if not zone_analysis or not config.zone_config or not config.zone_config['zones']:
            return {}

        enhanced_zone_analysis = {}
        zones = config.zone_config['zones']
        current_frame_zone_tracks = {}

        for zone_name in zones.keys():
            current_frame_zone_tracks[zone_name] = set()
            if zone_name not in self._zone_current_track_ids:
                self._zone_current_track_ids[zone_name] = set()
            if zone_name not in self._zone_total_track_ids:
                self._zone_total_track_ids[zone_name] = set()

        for detection in detections:
            track_id = detection.get("track_id")
            if track_id is None:
                continue
            bbox = detection.get("bounding_box")
            if not bbox:
                continue
            center_point = get_bbox_center(bbox)
            for zone_name, zone_polygon in zones.items():
                polygon_points = [(point[0], point[1]) for point in zone_polygon]
                if point_in_polygon(center_point, polygon_points):
                    current_frame_zone_tracks[zone_name].add(track_id)

        for zone_name, zone_counts in zone_analysis.items():
            current_tracks = current_frame_zone_tracks.get(zone_name, set())
            self._zone_current_track_ids[zone_name] = current_tracks
            self._zone_total_track_ids[zone_name].update(current_tracks)
            self._zone_current_counts[zone_name] = len(current_tracks)
            self._zone_total_counts[zone_name] = len(self._zone_total_track_ids[zone_name])
            enhanced_zone_analysis[zone_name] = {
                "current_count": self._zone_current_counts[zone_name],
                "total_count": self._zone_total_counts[zone_name],
                "current_track_ids": list(current_tracks),
                "total_track_ids": list(self._zone_total_track_ids[zone_name]),
                "original_counts": zone_counts
            }

        return enhanced_zone_analysis

    def _check_alerts(self, summary: dict, zone_analysis: Dict, frame_number: Any, config: DwellConfig) -> List[Dict]:
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
                elif category == "dwell_person" and per_category_count.get(category, 0) > threshold:
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

    def _generate_incidents(self, counting_summary: Dict, zone_analysis: Dict, alerts: List, config: DwellConfig,
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

            human_text_lines = [f"DWELL DETECTED @ {current_timestamp}:"]
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

    def _generate_tracking_stats(self, counting_summary: Dict, zone_analysis: Dict, alerts: List, config: DwellConfig,
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
            category = detection.get("category", "dwell_person")
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

        # human_text_lines = [f"Tracking Statistics:"]
        # human_text_lines.append(f"CURRENT FRAME @ {current_timestamp}")
        # if zone_analysis:
        #     human_text_lines.append("\tZones (current):")
        #     for zone_name, zone_data in zone_analysis.items():
        #         current_count = zone_data.get("current_count", 0)
        #         human_text_lines.append(f"\t{zone_name}: {int(current_count)}")
        # else:
        #     for cat, count in per_category_count.items():
        #         human_text_lines.append(f"\t{cat}: {count}")
        # human_text_lines.append(f"TOTAL SINCE {start_timestamp}")
        # if zone_analysis:
        #     human_text_lines.append("\tZones (total):")
        #     for zone_name, zone_data in zone_analysis.items():
        #         total_count = zone_data.get("total_count", 0)
        #         human_text_lines.append(f"\t{zone_name}: {int(total_count)}")
        # else:
        #     for cat, count in total_counts_dict.items():
        #         if count > 0:
        #             human_text_lines.append(f"\t{cat}: {count}")
        # human_text_lines.append(f"Alerts: {alerts[0].get('settings', {}) if alerts else 'None'} sent @ {current_timestamp}")
        # human_text = "\n".join(human_text_lines)

        human_text_lines = [f"Tracking Statistics:"]
        human_text_lines.append(f"CURRENT FRAME @ {current_timestamp}")
        # Append zone-wise current counts if available
        if zone_analysis:
            human_text_lines.append("\tZones (current):")
            for zone_name, zone_data in zone_analysis.items():
                current_count = 0
                if isinstance(zone_data, dict):
                    if "current_count" in zone_data:
                        current_count = zone_data.get("current_count", 0)
                    else:
                        counts_dict = zone_data.get("original_counts") if isinstance(zone_data.get("original_counts"), dict) else zone_data
                        current_count = counts_dict.get(
                            "total",
                            sum(v for v in counts_dict.values() if isinstance(v, (int, float)))
                        )
                human_text_lines.append(f"\t{zone_name}: {int(current_count)}")
        else:
            if any(count > 0 for count in per_category_count.values()):

                for cat, count in per_category_count.items():
                    if count > 0:
                        human_text_lines.append(f"\t- {count} {cat.capitalize()} detected")
                    else:
                        human_text_lines.append(f"\t- No detections")
        human_text_lines.append(f"TOTAL SINCE {start_timestamp}")
        # Append zone-wise total counts if available
        if zone_analysis:
            human_text_lines.append("\tZones (total):")
            for zone_name, zone_data in zone_analysis.items():
                total_count = 0
                if isinstance(zone_data, dict):
                    # Prefer the numeric cumulative total if available
                    if "total_count" in zone_data and isinstance(zone_data.get("total_count"), (int, float)):
                        total_count = zone_data.get("total_count", 0)
                    # Fallback: compute from list of total_track_ids if present
                    elif "total_track_ids" in zone_data and isinstance(zone_data.get("total_track_ids"), list):
                        total_count = len(zone_data.get("total_track_ids", []))
                    else:
                        # Last resort: try to sum numeric values present
                        counts_dict = zone_data if isinstance(zone_data, dict) else {}
                        total_count = sum(v for v in counts_dict.values() if isinstance(v, (int, float)))
                human_text_lines.append(f"\t{zone_name}: {int(total_count)}")
        else:
            for cat, count in total_counts_dict.items():
                if count > 0:
                    human_text_lines.append(f"\t{cat}: {count}")
        if alerts:
            for alert in alerts:
                human_text_lines.append(f"Alerts: {alert.get('settings', {})} sent @ {current_timestamp}")
        else:
            human_text_lines.append("Alerts: None")
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

    def _generate_business_analytics(self, counting_summary: Dict, zone_analysis: Dict, alerts: Any, config: DwellConfig,
                                    stream_info: Optional[Dict[str, Any]] = None, is_empty=False) -> List[Dict]:
        if is_empty:
            return []
        return []

    def _generate_summary(self, summary: dict, zone_analysis: Dict, incidents: List, tracking_stats: List, business_analytics: List, alerts: List) -> List[str]:
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
        return ["\n".join(f"{k}: {v}" for k, v in lines.items())]

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
            self._per_category_total_track_ids = {cat: set() for cat in self.target_categories + ['dwell_person']}
        self._current_frame_track_ids = {cat: set() for cat in self.target_categories + ['dwell_person']}

        for det in detections:
            cat = det.get("category")
            raw_track_id = det.get("track_id")
            if cat not in self.target_categories + ['dwell_person'] or raw_track_id is None:
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

    def _get_current_timestamp_str(self, stream_info: Optional[Dict[str, Any]], precision=False, frame_id: Optional[str]=None) -> str:
        """Get formatted current timestamp based on stream type."""
        
        if not stream_info:
            return "00:00:00.00"
        if precision:
            if stream_info.get("input_settings", {}).get("start_frame", "na") != "na":
                if frame_id:
                    start_time = int(frame_id)/stream_info.get("input_settings", {}).get("original_fps", 30)
                else:
                    start_time = stream_info.get("input_settings", {}).get("start_frame", 30)/stream_info.get("input_settings", {}).get("original_fps", 30)
                stream_time_str = self._format_timestamp_for_video(start_time)
                
                return self._format_timestamp(stream_info.get("input_settings", {}).get("stream_time", "NA"))
            else:
                return datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")

        if stream_info.get("input_settings", {}).get("start_frame", "na") != "na":
            if frame_id:
                start_time = int(frame_id)/stream_info.get("input_settings", {}).get("original_fps", 30)
            else:
                start_time = stream_info.get("input_settings", {}).get("start_frame", 30)/stream_info.get("input_settings", {}).get("original_fps", 30)

            stream_time_str = self._format_timestamp_for_video(start_time)
           

            return self._format_timestamp(stream_info.get("input_settings", {}).get("stream_time", "NA"))
        else:
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
            if self.start_timer is None:
                self.start_timer = stream_info.get("input_settings", {}).get("stream_time", "NA")
                return self._format_timestamp(self.start_timer)
            elif stream_info.get("input_settings", {}).get("start_frame", "na") == 1:
                self.start_timer = stream_info.get("input_settings", {}).get("stream_time", "NA")
                return self._format_timestamp(self.start_timer)
            else:
                return self._format_timestamp(self.start_timer)

        if self.start_timer is None:
            self.start_timer = stream_info.get("input_settings", {}).get("stream_time", "NA")
            return self._format_timestamp(self.start_timer)
        elif stream_info.get("input_settings", {}).get("start_frame", "na") == 1:
            self.start_timer = stream_info.get("input_settings", {}).get("stream_time", "NA")
            return self._format_timestamp(self.start_timer)
        
        else:
            if self.start_timer is not None:
                return self._format_timestamp(self.start_timer)

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

    def _count_categories(self, detections: list, config: DwellConfig) -> dict:
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

    def _format_timestamp(self, timestamp: Any) -> str:
        """Format a timestamp so that exactly two digits follow the decimal point (milliseconds).

        The input can be either:
        1. A numeric Unix timestamp (``float`` / ``int``) – it will first be converted to a
           string in the format ``YYYY-MM-DD-HH:MM:SS.ffffff UTC``.
        2. A string already following the same layout.

        The returned value preserves the overall format of the input but truncates or pads
        the fractional seconds portion to **exactly two digits**.

        Example
        -------
        >>> self._format_timestamp("2025-08-19-04:22:47.187574 UTC")
        '2025-08-19-04:22:47.18 UTC'
        """

        # Convert numeric timestamps to the expected string representation first
        if isinstance(timestamp, (int, float)):
            timestamp = datetime.fromtimestamp(timestamp, timezone.utc).strftime(
                '%Y-%m-%d-%H:%M:%S.%f UTC'
            )

        # Ensure we are working with a string from here on
        if not isinstance(timestamp, str):
            return str(timestamp)

        # If there is no fractional component, simply return the original string
        if '.' not in timestamp:
            return timestamp

        # Split out the main portion (up to the decimal point)
        main_part, fractional_and_suffix = timestamp.split('.', 1)

        # Separate fractional digits from the suffix (typically ' UTC')
        if ' ' in fractional_and_suffix:
            fractional_part, suffix = fractional_and_suffix.split(' ', 1)
            suffix = ' ' + suffix  # Re-attach the space removed by split
        else:
            fractional_part, suffix = fractional_and_suffix, ''

        # Guarantee exactly two digits for the fractional part
        fractional_part = (fractional_part + '00')[:2]

        return f"{main_part}.{fractional_part}{suffix}"

    def _get_tracking_start_time(self) -> str:
        if self._tracking_start_time is None:
            return "N/A"
        return self._format_timestamp(self._tracking_start_time)

    def _set_tracking_start_time(self) -> None:
        self._tracking_start_time = time.time()