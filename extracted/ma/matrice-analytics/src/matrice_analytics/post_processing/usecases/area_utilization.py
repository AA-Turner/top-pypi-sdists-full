"""
Area Utilization (People Counting + Utilization Analytics) post-processing usecase.

This file is a "modified clone" of people_counting.py with area_utilization logic layered on top.

Key behavior:
- Counts people (like PeopleCountingUseCase)
- Computes zone-wise capacity utilization (like area_utilization.py)
- Policy-correct zones:
    - If user provides zones -> compute zone-wise metrics
    - If user does NOT provide zones -> treat full camera frame as ONE zone named "global"
- Primary metric:
    occupancy_percent = (people_count / capacity) * 100
- Rolling window (seconds) metrics:
    time_occupied_percent = % of frames in window with count>0
    avg_occupancy_percent = avg(count) / capacity * 100
- Membership rule:
    - Uses bbox CENTER point for zone membership

Output schema: Matrice Analytics agg_summary (frame-wise)
- incidents
- tracking_stats
- business_analytics (NOW populated with utilization metrics)
- alerts (count-based + optional occupancy-based if configured)
- human_text
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, field
import time
from datetime import datetime, timezone

from ..core.base import BaseProcessor, ProcessingContext, ProcessingResult, ConfigProtocol, ProcessingStatus, ResultFormat
from ..core.config import BaseConfig, ZoneConfig, AlertConfig

from ..utils import (
    filter_by_confidence,
    apply_category_mapping,
    match_results_structure,
    filter_by_categories,
    count_objects_by_category,
    count_objects_in_zones,
    calculate_counting_summary,
    bbox_smoothing,
    BBoxSmoothingConfig,
    BBoxSmoothingTracker,
    point_in_polygon,
)

# from ..utils.geometry_utils import point_in_polygon


TARGET_CATEGORY = "person"

WARN_NO_ZONES = "no_zones_configured_full_frame_used"
WARN_ZONE_TOO_BIG = "zone_exceeds_stream_resolution"
WARN_MISSING_STREAM_RESOLUTION = "missing_stream_resolution"

DEFAULT_CAPACITY = 10
DEFAULT_WINDOW_SECONDS = 300  # 5 minutes


def _bbox_center(bbox: Any) -> Tuple[float, float]:
    """
    bbox formats supported:
    - dict xmin,ymin,xmax,ymax
    - dict x1,y1,x2,y2
    - list [x1,y1,x2,y2]
    """
    if not bbox:
        return (0.0, 0.0)

    if isinstance(bbox, (list, tuple)) and len(bbox) >= 4:
        x1, y1, x2, y2 = bbox[0], bbox[1], bbox[2], bbox[3]
        return ((float(x1) + float(x2)) / 2.0, (float(y1) + float(y2)) / 2.0)

    if isinstance(bbox, dict):
        if "xmin" in bbox:
            return (
                (float(bbox.get("xmin", 0)) + float(bbox.get("xmax", 0))) / 2.0,
                (float(bbox.get("ymin", 0)) + float(bbox.get("ymax", 0))) / 2.0,
            )
        if "x1" in bbox:
            return (
                (float(bbox.get("x1", 0)) + float(bbox.get("x2", 0))) / 2.0,
                (float(bbox.get("y1", 0)) + float(bbox.get("y2", 0))) / 2.0,
            )

    return (0.0, 0.0)


def _normalize_detection_bbox(det: Dict[str, Any]) -> Dict[str, Any]:
    """
    Ensure bbox exists under det['bounding_box'] if only det['bbox'] exists.
    """
    d = det.copy()
    if "bounding_box" not in d and "bbox" in d:
        d["bounding_box"] = d["bbox"]
    return d


def _zone_exceeds_stream_resolution(zone_poly: List[List[float]], stream_res: Dict[str, Any]) -> bool:
    w = stream_res.get("width", 0) or 0
    h = stream_res.get("height", 0) or 0
    if not w or not h:
        return False

    for p in zone_poly:
        if len(p) >= 2 and (p[0] > w or p[1] > h):
            return True
    return False


def _occupancy_state(percent: float) -> str:
    """
    State buckets policy:
    - vacant: 0
    - low: (0, 30]
    - moderate: (30, 70]
    - high: (70, 100]
    - overcrowded: >100
    """
    if percent <= 0:
        return "vacant"
    if percent <= 30:
        return "low"
    if percent <= 70:
        return "moderate"
    if percent <= 100:
        return "high"
    return "overcrowded"


# ----------------------------
# Config
# ----------------------------
@dataclass
class AreaUtilizationConfig(BaseConfig):
    """
    Configuration for area utilization use case.

    This config intentionally mirrors PeopleCountingConfig so that:
    - client payloads stay consistent
    - PostProcessor/config_manager behavior remains predictable
    - we can safely clone people_counting.py behavior

    Utilization-specific parameters live in:
      extra_params = {
        "zone_capacities": {"global": 10, "meeting_room": 6},
        "window_seconds": 300,
      }
    """

    # -----------------------------
    # Smoothing configuration (kept for parity)
    # -----------------------------
    enable_smoothing: bool = True
    smoothing_algorithm: str = "observability"  # "window" or "observability"
    smoothing_window_size: int = 20
    smoothing_cooldown_frames: int = 5
    smoothing_confidence_range_factor: float = 0.5

    # -----------------------------
    # PERFORMANCE: Tracker selection
    # -----------------------------
    enable_advanced_tracker: bool = False  # Heavy O(n³) tracker - enable only when tracking quality is critical
    enable_simple_tracker: bool = False    # Lightweight O(n) tracker - fast but no cross-frame persistence

    # -----------------------------
    # Zone configuration
    # -----------------------------
    zone_config: Optional[ZoneConfig] = None

    # -----------------------------
    # Counting parameters
    # -----------------------------
    enable_unique_counting: bool = True
    time_window_minutes: int = 60  # kept for parity (even if window_seconds is used for utilization)

    # -----------------------------
    # Category mapping
    # -----------------------------
    person_categories: List[str] = field(default_factory=lambda: ["person", "people"])
    index_to_category: Optional[Dict[int, str]] = None

    # -----------------------------
    # Alerts
    # -----------------------------
    alert_config: Optional[AlertConfig] = None

    # Keep same broad target list (even if we filter down to person internally)
    target_categories: List[str] = field(
        default_factory=lambda: [
            "person", "people", "human", "man", "woman", "male", "female"
        ]
    )

    # -----------------------------
    # Utilization-specific behavior
    # -----------------------------
    use_center_membership: bool = True  # zone membership uses bbox center

    def validate(self) -> List[str]:
        """Validate area utilization configuration (PeopleCountingConfig-compatible)."""
        errors = super().validate()

        if self.time_window_minutes <= 0:
            errors.append("time_window_minutes must be positive")

        if not self.person_categories:
            errors.append("person_categories cannot be empty")

        # Validate nested configs
        if self.zone_config:
            errors.extend(self.zone_config.validate())

        if self.alert_config:
            errors.extend(self.alert_config.validate())

        return errors


# ----------------------------
# UseCase
# ----------------------------
class AreaUtilizationUseCase(BaseProcessor):
    """
    Area Utilization = People Counting + Capacity Analytics.

    Keeps PeopleCounting behavior:
    - incidents
    - tracking_stats
    - alerts (count-based + optional occupancy-based)
    - human_text summary

    Adds:
    - business_analytics with zone-wise utilization metrics
    """

    def __init__(self):
        super().__init__("area_utilization")
        self.category = "general"
        self.CASE_TYPE: Optional[str] = "area_utilization"
        self.CASE_VERSION: Optional[str] = "1.0"

        # Keep people-only focus (like people_counting)
        self.target_categories = ["person"]

        # tracker state (same pattern)
        self.tracker = None
        self._total_frame_counter = 0
        self._tracking_start_time = None

        # alert trend state
        self._ascending_alert_list: List[int] = []
        self.current_incident_end_timestamp: str = "N/A"
        self.start_timer = None

        # persistent rolling history per zone: [(timestamp, count), ...]
        self._history: Dict[str, List[Tuple[float, int]]] = {}

    # ----------------------------
    # Lightweight tracker option (same as people_counting)
    # ----------------------------
    def _simple_tracker_update(self, detections: list) -> list:
        """
        PERFORMANCE: Lightweight tracker alternative
        Simple tracker using frame-local indexing (O(n)).
        Does not persist track IDs across frames.
        Enable via config.enable_simple_tracker = True
        """
        for i, det in enumerate(detections):
            if det.get("track_id") is None:
                det["track_id"] = f"simple_{self._total_frame_counter}_{i}"
        return detections

    # ----------------------------
    # Main process
    # ----------------------------
    def process(
        self,
        data: Any,
        config: ConfigProtocol,
        context: Optional[ProcessingContext] = None,
        stream_info: Optional[Dict[str, Any]] = None,
    ) -> ProcessingResult:
        processing_start = time.time()

        if not isinstance(config, AreaUtilizationConfig):
            return self.create_error_result(
                "Invalid config type",
                usecase=self.name,
                category=self.category,
                context=context,
            )

        if context is None:
            context = ProcessingContext()

        # Validate config
        errors = config.validate()
        if errors:
            context.mark_completed()
            return self.create_error_result(
                "Invalid configuration",
                usecase=self.name,
                category=self.category,
                context=context,
            )

        # Detect input format (for metadata parity)
        input_format = match_results_structure(data)
        context.input_format = input_format
        context.confidence_threshold = config.confidence_threshold

        # Confidence filtering
        if config.confidence_threshold is not None:
            processed_data = filter_by_confidence(data, config.confidence_threshold)
        else:
            processed_data = data

        # Category mapping
        if config.index_to_category:
            processed_data = apply_category_mapping(processed_data, config.index_to_category)

        # Category filtering (people-only)
        target_cats = config.target_categories or self.target_categories
        processed_data = self._filter_target_categories(processed_data, target_cats)

        # Normalize bbox field names
        processed_data = [_normalize_detection_bbox(d) for d in processed_data] if isinstance(processed_data, list) else []

        # Tracker selection (optional)
        if getattr(config, "enable_advanced_tracker", False):
            try:
                from ..advanced_tracker import AdvancedTracker
                from ..advanced_tracker.config import TrackerConfig

                if self.tracker is None:
                    tracker_config = TrackerConfig(
                        track_high_thresh=0.4,
                        track_low_thresh=0.05,
                        new_track_thresh=0.3,
                        match_thresh=0.8,
                    )
                    self.tracker = AdvancedTracker(tracker_config)
                processed_data = self.tracker.update(processed_data)
            except Exception as e:
                self.logger.warning(f"AdvancedTracker failed: {e}")
        elif getattr(config, "enable_simple_tracker", False):
            processed_data = self._simple_tracker_update(processed_data)

        # Update counting state
        self._update_tracking_state(processed_data)
        self._total_frame_counter += 1

        # Determine frame_number (keep people_counting behavior)
        frame_number = None
        if stream_info:
            input_settings = stream_info.get("input_settings", {})
            start_frame = input_settings.get("start_frame")
            end_frame = input_settings.get("end_frame")
            if start_frame is not None and end_frame is not None and start_frame == end_frame:
                frame_number = start_frame
        frame_key = str(frame_number) if frame_number is not None else "current_frame"

        # Build counting summary
        counting_summary = self._count_people(processed_data)
        total_counts = self.get_total_counts()
        counting_summary["total_counts"] = total_counts

        # Compute area utilization stats (zones + capacity + rolling window)
        warnings: List[str] = []
        zone_stats = self._compute_area_utilization(
            detections=processed_data,
            config=config,
            context=context,
            stream_info=stream_info,
            warnings=warnings,
        )

        # Alerts (count-based + optional occupancy-based)
        alerts = self._check_alerts(counting_summary, zone_stats, frame_key, config)

        # Incidents / Tracking stats (kept same schema style)
        incidents_list = self._generate_incidents(counting_summary, alerts, config, frame_number, stream_info)
        tracking_stats_list = self._generate_tracking_stats(counting_summary, alerts, zone_stats, config, frame_number, stream_info)

        # Business analytics (new)
        business_analytics_list = self._generate_business_analytics(zone_stats, alerts, stream_info)

        # Summary (human_text)
        summary_list = self._generate_summary(
            incidents_list,
            tracking_stats_list,
            business_analytics_list,
        )

        incidents = incidents_list[0] if incidents_list else {}
        tracking_stats = tracking_stats_list[0] if tracking_stats_list else {}
        business_analytics = business_analytics_list[0] if business_analytics_list else {}
        summary = summary_list[0] if summary_list else ""

        agg_summary = {
            frame_key: {
                "incidents": incidents,
                "tracking_stats": tracking_stats,
                "business_analytics": business_analytics,
                "alerts": alerts,
                "human_text": summary,
            }
        }

        context.mark_completed()

        result = self.create_result(
            data={"agg_summary": agg_summary},
            usecase=self.name,
            category=self.category,
            context=context,
        )

        # Performance logs (same as people_counting)
        proc_time = time.time() - processing_start
        processing_latency_ms = proc_time * 1000.0
        processing_fps = (1.0 / proc_time) if proc_time > 0 else None
        print(
            "latency in ms:",
            processing_latency_ms,
            "| Throughput fps:",
            processing_fps,
            "| Frame_Number:",
            self._total_frame_counter,
        )
        if warnings:
            result.warnings = list(dict.fromkeys(warnings))
        return result

    # ----------------------------
    # Filtering helpers
    # ----------------------------
    def _filter_target_categories(self, data: Any, targets: List[str]) -> List[Dict[str, Any]]:
        if isinstance(data, list):
            return [d for d in data if d.get("category") in targets]
        return []

    # ----------------------------
    # Utilization computation
    # ----------------------------
    def _compute_area_utilization(
        self,
        detections: List[Dict[str, Any]],
        config: AreaUtilizationConfig,
        context: ProcessingContext,
        stream_info: Optional[Dict[str, Any]],
        warnings: List[str],
    ) -> Dict[str, Any]:
        """
        Returns zone_stats dict:
        {
          zone_name: {
            "count": int,
            "capacity": int,
            "occupancy_percent": float,
            "state": str,
            "time_occupied_percent": float,
            "avg_occupancy_percent": float
          }
        }
        """
        # Determine zones
        zones: Dict[str, Any] = {}
        if config.zone_config and getattr(config.zone_config, "zones", None):
            zones = config.zone_config.zones
        else:
            zones = {"global": None}
            warnings.append(WARN_NO_ZONES)

        # Stream resolution (optional warnings)
        # area_utilization.py uses context.metadata["stream_info"]["stream_resolution"]
        # but people_counting uses stream_info arg. We'll support both.
        meta_stream_info = (context.metadata or {}).get("stream_info", {}) if context else {}
        si = stream_info or meta_stream_info or {}
        res = {}
        if isinstance(si, dict):
            res = si.get("stream_resolution", {}) or si.get("input_settings", {}).get("stream_resolution", {}) or {}
        frame_w = int(res.get("width", 0) or 0)
        frame_h = int(res.get("height", 0) or 0)
        if frame_w <= 0 or frame_h <= 0:
            warnings.append(WARN_MISSING_STREAM_RESOLUTION)

        # Zone scale warning
        if zones and "global" not in zones and frame_w > 0 and frame_h > 0:
            for _zname, poly in zones.items():
                if poly and _zone_exceeds_stream_resolution(poly, {"width": frame_w, "height": frame_h}):
                    warnings.append(WARN_ZONE_TOO_BIG)
                    break

        # Params from extra_params
        extra = config.extra_params or {}
        capacities = extra.get("zone_capacities", {}) or {}
        window_seconds = int(extra.get("window_seconds", DEFAULT_WINDOW_SECONDS) or DEFAULT_WINDOW_SECONDS)

        now_ts = time.time()

        zone_stats: Dict[str, Any] = {}
        for zone_name, poly in zones.items():
            # Determine in-zone detections
            if poly is None:
                in_zone = detections[:]
            else:
                in_zone = []
                if not poly or len(poly) < 3:
                    in_zone = []
                else:
                    poly_points = [(p[0], p[1]) for p in poly]
                    for det in detections:
                        bbox = det.get("bounding_box") or det.get("bbox")
                        if not bbox:
                            continue
                        cx, cy = _bbox_center(bbox)
                        if point_in_polygon((cx, cy), poly_points):
                            in_zone.append(det)

            count = len(in_zone)
            capacity = int(capacities.get(zone_name, capacities.get("global", DEFAULT_CAPACITY)) or DEFAULT_CAPACITY)

            occ_percent = 0.0
            if capacity > 0:
                occ_percent = (count / capacity) * 100.0
            occ_percent = round(occ_percent, 3)
            state = _occupancy_state(occ_percent)

            # Update rolling history
            if zone_name not in self._history:
                self._history[zone_name] = []
            self._history[zone_name].append((now_ts, count))

            cutoff = now_ts - float(window_seconds)
            self._history[zone_name] = [(t, c) for (t, c) in self._history[zone_name] if t >= cutoff]

            # Time occupied percent (frame occupancy ratio)
            hist = self._history[zone_name]
            if hist:
                occupied_frames = sum(1 for (_, c) in hist if c > 0)
                time_occ_percent = (occupied_frames / len(hist)) * 100.0
                avg_occ = sum(c for (_, c) in hist) / len(hist)
                avg_occ_percent = (avg_occ / capacity) * 100.0 if capacity > 0 else 0.0
            else:
                time_occ_percent = 0.0
                avg_occ_percent = 0.0

            zone_stats[zone_name] = {
                "count": count,
                "capacity": capacity,
                "occupancy_percent": round(occ_percent, 3),
                "state": state,
                "time_occupied_percent": round(time_occ_percent, 3),
                "avg_occupancy_percent": round(avg_occ_percent, 3),
            }

        return zone_stats

    # ----------------------------
    # Alerts (count-based + optional occupancy-based)
    # ----------------------------
    def _check_alerts(
        self,
        counting_summary: Dict[str, Any],
        zone_stats: Dict[str, Any],
        frame_key: str,
        config: AreaUtilizationConfig,
    ) -> List[Dict[str, Any]]:
        def get_trend(data, lookback=900, threshold=0.6):
            window = data[-lookback:] if len(data) >= lookback else data
            if len(window) < 2:
                return True
            increasing = 0
            total = 0
            for i in range(1, len(window)):
                if window[i] >= window[i - 1]:
                    increasing += 1
                total += 1
            ratio = increasing / total
            return ratio >= threshold

        alerts: List[Dict[str, Any]] = []

        if not config.alert_config:
            return alerts

        # 1) Count-based alerts (keep people_counting behavior)
        total_detections = counting_summary.get("total_count", 0)
        per_category_count = counting_summary.get("per_category_count", {})

        if getattr(config.alert_config, "count_thresholds", None):
            alert_type_cfg = getattr(config.alert_config, "alert_type", ["Default"])
            alert_value_cfg = getattr(config.alert_config, "alert_value", ["JSON"])
            alert_type_str = alert_type_cfg[0] if isinstance(alert_type_cfg, (list, tuple)) and len(alert_type_cfg) > 0 else alert_type_cfg
            settings_map = {t: v for t, v in zip(alert_type_cfg, alert_value_cfg)}
            for category, threshold in config.alert_config.count_thresholds.items():
                if category == "all" and total_detections > threshold:
                    alert = self.create_alert_object(
                        alert_type_str,
                        f"alert_count_{category}_{frame_key}",
                        self.CASE_TYPE,
                        threshold,
                        ascending=get_trend(self._ascending_alert_list, lookback=900, threshold=0.8),
                        settings=settings_map,
                    )
                    alert["current_value"] = total_detections
                    alerts.append(alert)
                elif category in per_category_count and per_category_count[category] > threshold:
                    current = per_category_count[category]
                    alert = self.create_alert_object(
                        alert_type_str,
                        f"alert_count_{category}_{frame_key}",
                        self.CASE_TYPE,
                        threshold,
                        ascending=get_trend(self._ascending_alert_list, lookback=900, threshold=0.8),
                        settings=settings_map,
                    )
                    alert["current_value"] = current
                    alert["category"] = category
                    alerts.append(alert)

        # 2) Optional occupancy-based alerts (if configured)
        occupancy_thresholds = getattr(config.alert_config, "occupancy_thresholds", None)
        if occupancy_thresholds:
            alert_type_cfg = getattr(config.alert_config, "alert_type", ["Default"])
            alert_value_cfg = getattr(config.alert_config, "alert_value", ["JSON"])
            alert_type_str = alert_type_cfg[0] if isinstance(alert_type_cfg, (list, tuple)) and len(alert_type_cfg) > 0 else alert_type_cfg
            settings_map = {t: v for t, v in zip(alert_type_cfg, alert_value_cfg)}
            for zone_name, stats in zone_stats.items():
                threshold = occupancy_thresholds.get(zone_name, occupancy_thresholds.get("all"))
                if threshold is None:
                    continue
                occ_percent = float(stats.get("occupancy_percent", 0.0))
                if occ_percent > float(threshold):
                    # derive recent counts for trend (use history if available)
                    zone_hist = self._history.get(zone_name, [])
                    zone_counts = [c for (_, c) in zone_hist] if zone_hist else []
                    ascending = get_trend(zone_counts, lookback=900, threshold=0.8) if len(zone_counts) >= 2 else True
                    alert = self.create_alert_object(
                        alert_type_str,
                        f"alert_occ_{zone_name}_{frame_key}",
                        self.CASE_TYPE,
                        threshold,
                        ascending=ascending,
                        settings=settings_map,
                    )
                    alert["current_value"] = occ_percent
                    alert["zone"] = zone_name
                    alerts.append(alert)

        if alerts:
            try:
                self.logger.info(f"area_utilization: generated alerts: {alerts}")
            except Exception:
                pass

        return alerts

    # ----------------------------
    # Incident generation (kept people_counting style)
    # ----------------------------
    def _generate_incidents(
        self,
        counting_summary: Dict[str, Any],
        alerts: List[Dict[str, Any]],
        config: AreaUtilizationConfig,
        frame_number: Optional[int] = None,
        stream_info: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        incidents: List[Dict[str, Any]] = []
        total_detections = counting_summary.get("total_count", 0)

        current_timestamp = self._get_current_timestamp_str(stream_info)
        camera_info = self.get_camera_info_from_stream(stream_info)

        # keep trend window limited
        self._ascending_alert_list = (
            self._ascending_alert_list[-900:] if len(self._ascending_alert_list) > 900 else self._ascending_alert_list
        )

        if total_detections > 0:
            level = "low"
            intensity = 5.0
            start_timestamp = self._get_start_timestamp_str(stream_info)

            if start_timestamp and self.current_incident_end_timestamp == "N/A":
                self.current_incident_end_timestamp = "Incident still active"
            elif start_timestamp and self.current_incident_end_timestamp == "Incident still active":
                if len(self._ascending_alert_list) >= 15 and sum(self._ascending_alert_list[-15:]) / 15 < 1.5:
                    self.current_incident_end_timestamp = current_timestamp
            elif (
                self.current_incident_end_timestamp != "Incident still active"
                and self.current_incident_end_timestamp != "N/A"
            ):
                self.current_incident_end_timestamp = "N/A"

            # severity logic based on count thresholds (same style)
            if config.alert_config and getattr(config.alert_config, "count_thresholds", None):
                threshold = config.alert_config.count_thresholds.get("all", 15)
                intensity = min(10.0, (total_detections / threshold) * 10) if threshold else 10.0
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

            human_text_lines = [f"AREA UTILIZATION INCIDENTS DETECTED @ {current_timestamp}:"]
            human_text_lines.append(f"\tSeverity Level: {(self.CASE_TYPE, level)}")
            human_text = "\n".join(human_text_lines)

            alert_settings = []
            if config.alert_config and hasattr(config.alert_config, "alert_type"):
                alert_type_cfg = getattr(config.alert_config, "alert_type", ["Default"])
                alert_value_cfg = getattr(config.alert_config, "alert_value", ["JSON"])
                alert_type_str = alert_type_cfg[0] if isinstance(alert_type_cfg, (list, tuple)) and len(alert_type_cfg) > 0 else alert_type_cfg
                settings_map = {t: v for t, v in zip(alert_type_cfg, alert_value_cfg)}
                alert_settings.append(
                    {
                        "alert_type": alert_type_str,
                        "incident_category": self.CASE_TYPE,
                        "threshold_value": getattr(config.alert_config, "count_thresholds", {}) or {},
                        "ascending": True,
                        "settings": settings_map,
                    }
                )

            event = self.create_incident(
                incident_id=f"{self.CASE_TYPE}_{frame_number}",
                incident_type=self.CASE_TYPE,
                severity_level=level,
                human_text=human_text,
                camera_info=camera_info,
                alerts=alerts,
                alert_settings=alert_settings,
                start_time=start_timestamp,
                end_time=self.current_incident_end_timestamp,
                level_settings={"low": 1, "medium": 3, "significant": 4, "critical": 7},
            )
            incidents.append(event)
        else:
            self._ascending_alert_list.append(0)
            incidents.append({})

        return incidents

    # ----------------------------
    # Tracking stats (kept people_counting style)
    # ----------------------------
    def _generate_tracking_stats(
        self,
        counting_summary: Dict[str, Any],
        alerts: List[Dict[str, Any]],
        zone_stats: Dict[str, Any],
        config: AreaUtilizationConfig,
        frame_number: Optional[int] = None,
        stream_info: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        camera_info = self.get_camera_info_from_stream(stream_info)

        total_detections = counting_summary.get("total_count", 0)
        total_counts_dict = counting_summary.get("total_counts", {})
        per_category_count = counting_summary.get("per_category_count", {})

        current_timestamp = self._get_current_timestamp_str(stream_info, precision=False)
        start_timestamp = self._get_start_timestamp_str(stream_info, precision=False)
        high_precision_start_timestamp = self._get_current_timestamp_str(stream_info, precision=True)
        high_precision_reset_timestamp = self._get_start_timestamp_str(stream_info, precision=True)

        total_counts = [{"category": cat, "count": count} for cat, count in total_counts_dict.items() if count > 0]
        current_counts = [
            {"category": cat, "count": count} for cat, count in per_category_count.items() if count > 0 or total_detections > 0
        ]

        detections_objs = []
        for detection in counting_summary.get("detections", []):
            bbox = detection.get("bounding_box", {})
            category = detection.get("category", "person")
            detection_obj = self.create_detection_object(category, bbox)
            # preserve optional fields for downstream consumers
            if detection.get("track_id") is not None:
                detection_obj["track_id"] = detection.get("track_id")
            if detection.get("confidence") is not None:
                detection_obj["confidence"] = detection.get("confidence")
            detections_objs.append(detection_obj)

        alert_settings = []
        if config.alert_config and hasattr(config.alert_config, "alert_type"):
            alert_type_cfg = getattr(config.alert_config, "alert_type", ["Default"])
            alert_value_cfg = getattr(config.alert_config, "alert_value", ["JSON"])
            alert_type_str = alert_type_cfg[0] if isinstance(alert_type_cfg, (list, tuple)) and len(alert_type_cfg) > 0 else alert_type_cfg
            settings_map = {t: v for t, v in zip(alert_type_cfg, alert_value_cfg)}
            alert_settings.append(
                {
                    "alert_type": alert_type_str,
                    "incident_category": self.CASE_TYPE,
                    "threshold_value": getattr(config.alert_config, "count_thresholds", {}) or {},
                    "ascending": True,
                    "settings": settings_map,
                }
            )

        human_text_lines: List[str] = []
        human_text_lines.append(f"CURRENT FRAME @ {current_timestamp}:")
        for _cat, count in per_category_count.items():
            human_text_lines.append(f"\t- People Detected: {count}")

        # Add per-zone counts and occupancy metrics to human text
        if zone_stats:
            human_text_lines.append("")
            human_text_lines.append("Zone Utilization:")
            for zname, zst in zone_stats.items():
                human_text_lines.append(
                    f"\t- {zname}: {zst.get('count', 0)}/{zst.get('capacity', 0)} "
                    f"occ={zst.get('occupancy_percent', 0):.1f}% "
                    f"time={zst.get('time_occupied_percent', 0):.1f}% "
                    f"avg={zst.get('avg_occupancy_percent', 0):.1f}%"
                )

        human_text_lines.append("")
        human_text = "\n".join(human_text_lines)

        reset_settings = [{"interval_type": "daily", "reset_time": {"value": 9, "time_unit": "hour"}}]
        tracking_stat = self.create_tracking_stats(
            total_counts=total_counts,
            current_counts=current_counts,
            detections=detections_objs,
            human_text=human_text,
            camera_info=camera_info,
            alerts=alerts,
            alert_settings=alert_settings,
            reset_settings=reset_settings,
            start_time=high_precision_start_timestamp,
            reset_time=high_precision_reset_timestamp,
        )
        tracking_stat["target_categories"] = self.target_categories
        # include zone-level statistics for easy access in tracking_stats
        tracking_stat["zone_statistics"] = zone_stats or {}
        return [tracking_stat]

    # ----------------------------
    # Business analytics (NEW)
    # ----------------------------
    def _generate_business_analytics(
        self,
        zone_stats: Dict[str, Any],
        alerts: Optional[List[Dict[str, Any]]],
        stream_info: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        camera_info = self.get_camera_info_from_stream(stream_info)
        human_text = self._build_utilization_human_text(zone_stats)

        analytics_obj = self.create_business_analytics(
            analysis_name="area_utilization",
            statistics=zone_stats,
            human_text=human_text,
            camera_info=camera_info if camera_info else self.get_default_camera_info(),
            alerts=alerts or [],
        )
        return [analytics_obj]

    def _build_utilization_human_text(self, zone_stats: Dict[str, Any]) -> str:
        lines = ["Area Utilization (Capacity-based):"]
        for z, s in zone_stats.items():
            lines.append(
                f"\t{z}: {s.get('occupancy_percent', 0.0)}% "
                f"({s.get('count', 0)}/{s.get('capacity', 0)}) "
                f"state={s.get('state', 'unknown')} | "
                f"time_occupied={s.get('time_occupied_percent', 0.0)}% "
                f"avg_occ={s.get('avg_occupancy_percent', 0.0)}%"
            )
        return "\n".join(lines)

    # ----------------------------
    # Human summary generator (kept style)
    # ----------------------------
    def _generate_summary(
        self,
        incidents: List[Dict[str, Any]],
        tracking_stats: List[Dict[str, Any]],
        business_analytics: List[Dict[str, Any]],
    ) -> List[str]:
        lines: List[str] = []
        lines.append("Application Name: " + self.CASE_TYPE)
        lines.append("Application Version: " + self.CASE_VERSION)

        if len(tracking_stats) > 0:
            lines.append("Tracking Statistics: " + f"\t{tracking_stats[0].get('human_text', '')}")
        if len(business_analytics) > 0:
            lines.append("Business Analytics: " + f"\t{business_analytics[0].get('human_text', '')}")

        if len(incidents) == 0 and len(tracking_stats) == 0 and len(business_analytics) == 0:
            lines.append("Summary: " + "No Summary Data")

        return ["\n".join(lines)]

    # ----------------------------
    # Counting + tracking state helpers
    # ----------------------------
    def _count_people(self, detections: List[Dict[str, Any]]) -> Dict[str, Any]:
        counts: Dict[str, int] = {}
        for det in detections:
            cat = det.get("category", "unknown")
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
                    "frame_id": det.get("frame_id"),
                }
                for det in detections
            ],
        }

    def _update_tracking_state(self, detections: List[Dict[str, Any]]):
        if not hasattr(self, "_per_category_total_track_ids"):
            self._per_category_total_track_ids = {cat: set() for cat in self.target_categories}
        self._current_frame_track_ids = {cat: set() for cat in self.target_categories}

        for det in detections:
            cat = det.get("category")
            track_id = det.get("track_id")
            if cat not in self.target_categories:
                continue
            if track_id is not None:
                self._per_category_total_track_ids.setdefault(cat, set()).add(track_id)
                self._current_frame_track_ids[cat].add(track_id)

    def get_total_counts(self) -> Dict[str, int]:
        return {cat: len(ids) for cat, ids in getattr(self, "_per_category_total_track_ids", {}).items()}

    # ----------------------------
    # Timestamp helpers (copied style from people_counting)
    # ----------------------------
    def _format_timestamp_for_stream(self, timestamp: float) -> str:
        dt = datetime.fromtimestamp(timestamp, tz=timezone.utc)
        return dt.strftime("%Y:%m:%d %H:%M:%S")

    def _format_timestamp_for_video(self, timestamp: float) -> str:
        hours = int(timestamp // 3600)
        minutes = int((timestamp % 3600) // 60)
        seconds = round(float(timestamp % 60), 2)
        return f"{hours:02d}:{minutes:02d}:{seconds:.1f}"

    def _format_timestamp(self, timestamp: Any) -> str:
        if isinstance(timestamp, (int, float)):
            dt = datetime.fromtimestamp(timestamp, timezone.utc)
            return dt.strftime("%Y:%m:%d %H:%M:%S")

        if not isinstance(timestamp, str):
            return str(timestamp)

        timestamp_clean = timestamp.replace(" UTC", "").strip()
        if "." in timestamp_clean:
            timestamp_clean = timestamp_clean.split(".")[0]

        try:
            if timestamp_clean.count("-") >= 2:
                parts = timestamp_clean.split("-")
                if len(parts) >= 4:
                    formatted = f"{parts[0]}:{parts[1]}:{parts[2]} {'-'.join(parts[3:])}"
                    return formatted
        except Exception:
            pass

        return timestamp_clean

    def _get_current_timestamp_str(self, stream_info: Optional[Dict[str, Any]], precision=False, frame_id: Optional[str] = None) -> str:
        if not stream_info:
            return "00:00:00.00"
        if precision:
            if stream_info.get("input_settings", {}).get("start_frame", "na") != "na":
                if frame_id:
                    start_time = int(frame_id) / stream_info.get("input_settings", {}).get("original_fps", 30)
                else:
                    start_time = stream_info.get("input_settings", {}).get("start_frame", 30) / stream_info.get("input_settings", {}).get("original_fps", 30)
                _ = self._format_timestamp_for_video(start_time)
                return self._format_timestamp(stream_info.get("input_settings", {}).get("stream_time", "NA"))
            else:
                return datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")

        if stream_info.get("input_settings", {}).get("start_frame", "na") != "na":
            if frame_id:
                start_time = int(frame_id) / stream_info.get("input_settings", {}).get("original_fps", 30)
            else:
                start_time = stream_info.get("input_settings", {}).get("start_frame", 30) / stream_info.get("input_settings", {}).get("original_fps", 30)
            _ = self._format_timestamp_for_video(start_time)
            return self._format_timestamp(stream_info.get("input_settings", {}).get("stream_time", "NA"))
        else:
            stream_time_str = stream_info.get("input_settings", {}).get("stream_info", {}).get("stream_time", "")
            if stream_time_str:
                try:
                    timestamp_str = stream_time_str.replace(" UTC", "")
                    dt = datetime.strptime(timestamp_str, "%Y-%m-%d-%H:%M:%S.%f")
                    timestamp = dt.replace(tzinfo=timezone.utc).timestamp()
                    return self._format_timestamp_for_stream(timestamp)
                except Exception:
                    return self._format_timestamp_for_stream(time.time())
            else:
                return self._format_timestamp_for_stream(time.time())

    def _get_start_timestamp_str(self, stream_info: Optional[Dict[str, Any]], precision=False) -> str:
        if not stream_info:
            return "00:00:00"

        if precision:
            if self.start_timer is None:
                candidate = stream_info.get("input_settings", {}).get("stream_time")
                if not candidate or candidate == "NA":
                    candidate = datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")
                self.start_timer = candidate
                return self._format_timestamp(self.start_timer)
            elif stream_info.get("input_settings", {}).get("start_frame", "na") == 1:
                candidate = stream_info.get("input_settings", {}).get("stream_time")
                if not candidate or candidate == "NA":
                    candidate = datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")
                self.start_timer = candidate
                return self._format_timestamp(self.start_timer)
            else:
                return self._format_timestamp(self.start_timer)

        if self.start_timer is None:
            candidate = stream_info.get("input_settings", {}).get("stream_time")
            if not candidate or candidate == "NA":
                stream_time_str = stream_info.get("input_settings", {}).get("stream_info", {}).get("stream_time", "")
                if stream_time_str:
                    try:
                        timestamp_str = stream_time_str.replace(" UTC", "")
                        dt = datetime.strptime(timestamp_str, "%Y-%m-%d-%H:%M:%S.%f")
                        self._tracking_start_time = dt.replace(tzinfo=timezone.utc).timestamp()
                        candidate = datetime.fromtimestamp(self._tracking_start_time, timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")
                    except Exception:
                        candidate = datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")
                else:
                    candidate = datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")
            self.start_timer = candidate
            return self._format_timestamp(self.start_timer)
        elif stream_info.get("input_settings", {}).get("start_frame", "na") == 1:
            candidate = stream_info.get("input_settings", {}).get("stream_time")
            if not candidate or candidate == "NA":
                stream_time_str = stream_info.get("input_settings", {}).get("stream_info", {}).get("stream_time", "")
                if stream_time_str:
                    try:
                        timestamp_str = stream_time_str.replace(" UTC", "")
                        dt = datetime.strptime(timestamp_str, "%Y-%m-%d-%H:%M:%S.%f")
                        ts = dt.replace(tzinfo=timezone.utc).timestamp()
                        candidate = datetime.fromtimestamp(ts, timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")
                    except Exception:
                        candidate = datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")
                else:
                    candidate = datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")
            self.start_timer = candidate
            return self._format_timestamp(self.start_timer)
        else:
            if self.start_timer is not None and self.start_timer != "NA":
                return self._format_timestamp(self.start_timer)

            if self._tracking_start_time is None:
                stream_time_str = stream_info.get("input_settings", {}).get("stream_info", {}).get("stream_time", "")
                if stream_time_str:
                    try:
                        timestamp_str = stream_time_str.replace(" UTC", "")
                        dt = datetime.strptime(timestamp_str, "%Y-%m-%d-%H:%M:%S.%f")
                        self._tracking_start_time = dt.replace(tzinfo=timezone.utc).timestamp()
                    except Exception:
                        self._tracking_start_time = time.time()
                else:
                    self._tracking_start_time = time.time()

            dt = datetime.fromtimestamp(self._tracking_start_time, tz=timezone.utc)
            dt = dt.replace(minute=0, second=0, microsecond=0)
            return dt.strftime("%Y:%m:%d %H:%M:%S")