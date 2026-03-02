"""
Overcrowding Detection Usecase
--------------------------------

Definition:
    Overcrowding occurs when the number of detected persons in a zone
    exceeds a configured threshold for a configured number of frames.

Features:
- Zone-based or global detection
- Stateful detection (persistence + recovery)
- Alert cooldown support (AlertConfig)
- Incident lifecycle tracking (start/end)
- Multi-frame compatible
- Canonical agg_summary using BaseProcessor helpers

No density logic.
No rolling analytics.
Pure threshold-based safety detection.
"""

from __future__ import annotations

from typing import Any, Dict, List, Tuple, Optional
from dataclasses import dataclass, field
import time
from datetime import datetime, timezone

from ..core.base import (
    BaseProcessor,
    ProcessingContext,
    ProcessingResult,
    ConfigProtocol,
)
from ..core.config import BaseConfig, ZoneConfig, AlertConfig
from ..utils import (
    filter_by_confidence,
    apply_category_mapping,
    match_results_structure,
    point_in_polygon,
)

# ------------------------------------------------------------------------------
# Configuration
# ------------------------------------------------------------------------------

@dataclass
class OvercrowdingDetectionConfig(BaseConfig):
    zone_config: Optional[ZoneConfig] = None

    # Required thresholds
    count_thresholds: Dict[str, int] = field(default_factory=lambda: {"global": 10})

    # Stability controls
    persistence_frames: int = 3
    recovery_frames: int = 3

    # Severity controls
    warning_ratio: float = 0.8
    recovery_ratio: float = 0.9  # hysteresis exit ratio

    # Category mapping
    index_to_category: Optional[Dict[int, str]] = None
    target_categories: List[str] = field(default_factory=lambda: ["person"])

    alert_config: Optional[AlertConfig] = None

    # ADD this inside OvercrowdingDetectionConfig
    zone_settings: Dict[str, Dict[str, Any]] = field(default_factory=dict)

    def validate(self) -> List[str]:
        errors = super().validate()

        if not self.count_thresholds:
            errors.append("count_thresholds must be provided.")

        for z, t in self.count_thresholds.items():
            if t <= 0:
                errors.append(f"Threshold for zone '{z}' must be positive.")

        if self.persistence_frames <= 0:
            errors.append("persistence_frames must be positive.")

        if self.recovery_frames <= 0:
            errors.append("recovery_frames must be positive.")

        if not (0 < self.warning_ratio <= 1.0):
            errors.append("warning_ratio must be between 0 and 1.")

        if not (0 < self.recovery_ratio <= 1.0):
            errors.append("recovery_ratio must be between 0 and 1.")

        if self.zone_config:
            errors.extend(self.zone_config.validate())

        if self.alert_config:
            errors.extend(self.alert_config.validate())

        return errors


# ------------------------------------------------------------------------------
# Processor
# ------------------------------------------------------------------------------

class OvercrowdingDetectionUseCase(BaseProcessor):

    def __init__(self):
        super().__init__("overcrowding_detection")
        self.category = "safety"
        self.CASE_TYPE = "overcrowding_detection"
        self.CASE_VERSION = "1.0"

        self._zone_states: Dict[str, Dict[str, Any]] = {}
        self._zone_alert_timestamps: Dict[str, float] = {}
        self._frame_counter = 0

    # --------------------------------------------------------------------------
    # Main Entry
    # --------------------------------------------------------------------------

    def process(
        self,
        data: Any,
        config: ConfigProtocol,
        context: Optional[ProcessingContext] = None,
        stream_info: Optional[Dict[str, Any]] = None,
    ) -> ProcessingResult:

        if not isinstance(config, OvercrowdingDetectionConfig):
            return self.create_error_result(
                "Invalid config type",
                usecase=self.name,
                category=self.category,
                context=context,
            )

        if context is None:
            context = ProcessingContext()

        errors = config.validate()
        if errors:
            context.mark_completed()
            return self.create_error_result(
                "Invalid configuration",
                usecase=self.name,
                category=self.category,
                context=context,
            )

        is_multi_frame = isinstance(data, dict)

        frame_incidents = {}
        frame_tracking_stats = {}
        frame_business_analytics = {}
        frame_human_text = {}
        frame_alerts = {}

        if is_multi_frame:
            iterable = data.items()
        else:
            frame_key = "0"
            if stream_info:
                frame_key = str(
                    stream_info.get("input_settings", {}).get("start_frame", 0)
                )
            iterable = [(frame_key, data)]

        for frame_id, frame_data in iterable:

            output = self._process_single_frame(
                frame_data, config, context, stream_info
            )

            frame_incidents[frame_id] = output["incidents"]
            frame_tracking_stats[frame_id] = output["tracking_stats"]
            frame_business_analytics[frame_id] = output["business_analytics"]
            frame_alerts[frame_id] = output["alerts"]
            frame_human_text[frame_id] = output["human_text"]

        agg_summary = self.create_frame_wise_agg_summary(
            frame_incidents,
            frame_tracking_stats,
            frame_business_analytics,
            frame_alerts,
            frame_human_text,
        )

        context.mark_completed()

        return self.create_result(
            data={"agg_summary": agg_summary},
            usecase=self.name,
            category=self.category,
            context=context,
        )

    # --------------------------------------------------------------------------
    # Single Frame
    # --------------------------------------------------------------------------

    def _process_single_frame(
        self,
        data: Any,
        config: OvercrowdingDetectionConfig,
        context: ProcessingContext,
        stream_info: Optional[Dict[str, Any]],
    ) -> Dict[str, Any]:

        detections = self._prepare_detections(data, config)
        zone_counts = self._count_per_zone(detections, config)

        self._cleanup_stale_zones(zone_counts)

        zone_results = self._evaluate_overcrowding(zone_counts, config)
        alerts = self._generate_alerts(zone_results, config)
        incidents = self._generate_incidents(zone_results, alerts, stream_info)
        tracking_stats = self._generate_tracking_stats(
            detections, zone_results, alerts, stream_info
        )
        business_analytics = self._generate_business_analytics(
            zone_results, alerts, stream_info
        )

        human_text = self._build_human_text(zone_results)

        self._frame_counter += 1
        # frame_id = str(self._frame_counter)
        frame_id = str(
            stream_info.get("input_settings", {}).get("start_frame", self._frame_counter)
        )

        return {
            "incidents": incidents,
            "tracking_stats": tracking_stats,
            "business_analytics": business_analytics,
            "alerts": alerts,
            "human_text": human_text,
        }

    # --------------------------------------------------------------------------
    # Detection Preparation
    # --------------------------------------------------------------------------

    def _prepare_detections(self, data, config):

        detections = data

        if config.confidence_threshold is not None:
            detections = filter_by_confidence(
                detections, config.confidence_threshold
            )

        if config.index_to_category:
            detections = apply_category_mapping(
                detections, config.index_to_category
            )

        detections = [
            d for d in detections
            if d.get("category") in config.target_categories
        ]

        return detections

    # --------------------------------------------------------------------------
    # Zone Counting
    # --------------------------------------------------------------------------

    def _count_per_zone(self, detections, config):

        if config.zone_config and config.zone_config.zones:
            zones = config.zone_config.zones
        else:
            zones = {"global": None}

        counts = {}

        for zone_name, polygon in zones.items():

            if polygon is None:
                counts[zone_name] = len(detections)
                continue

            poly_points = [(p[0], p[1]) for p in polygon]
            count = 0

            for det in detections:
                bbox = det.get("bounding_box") or det.get("bbox")
                if not bbox:
                    continue

                cx, cy = self._bbox_center(bbox)

                if point_in_polygon((cx, cy), poly_points):
                    count += 1

            counts[zone_name] = count

        return counts

    # --------------------------------------------------------------------------
    # Stateful Evaluation
    # --------------------------------------------------------------------------

    def _compute_severity(
        self,
        zone: str,
        ratio: float,
        is_active: bool,
        warning_ratio: float,
        config
    ):

        # AlertConfig severity override
        if config.alert_config and hasattr(config.alert_config, "severity_mapping"):
            mapping = getattr(config.alert_config, "severity_mapping", {})

            # Expect mapping like {"warning": 0.8, "critical": 1.0}
            chosen = "normal"
            for level, threshold in sorted(mapping.items(), key=lambda x: x[1]):
                if ratio >= threshold:
                    chosen = level
            return chosen

        # Default fallback
        if is_active:
            return "critical"
        elif ratio >= warning_ratio:
            return "warning"
        else:
            return "normal"



    def _evaluate_overcrowding(self, zone_counts, config):

        results = {}
        for zone, count in zone_counts.items():
            # --- Per-zone overrides ---
            zone_cfg = config.zone_settings.get(zone, {})
            threshold = zone_cfg.get(
                "threshold",
                config.count_thresholds.get(zone, config.count_thresholds.get("global"))
            )

            warning_ratio = zone_cfg.get("warning_ratio", config.warning_ratio)
            recovery_ratio = zone_cfg.get("recovery_ratio", config.recovery_ratio)

            exit_threshold = threshold * recovery_ratio
            ratio = count / threshold if threshold else 0.0

            if zone not in self._zone_states:
                self._zone_states[zone] = {
                    "violation_streak": 0,
                    "recovery_streak": 0,
                    "is_active": False,
                    "start_timestamp": None,
                }

            state = self._zone_states[zone]

            # ENTER
            if count > threshold:
                state["violation_streak"] += 1
                state["recovery_streak"] = 0

                if (
                    state["violation_streak"] >= config.persistence_frames
                    and not state["is_active"]
                ):
                    state["is_active"] = True
                    state["start_timestamp"] = time.time()

            # EXIT (Hysteresis)
            elif count <= exit_threshold:
                state["recovery_streak"] += 1
                state["violation_streak"] = 0

                if (
                    state["recovery_streak"] >= config.recovery_frames
                    and state["is_active"]
                ):
                    state["is_active"] = False

            severity = self._compute_severity(
                zone,
                ratio,
                state["is_active"],
                warning_ratio,
                config
            )

            results[zone] = {
                "count": count,
                "threshold": threshold,
                "ratio": round(ratio, 3),
                "severity": severity,
                "is_overcrowded": state["is_active"],
            }
        return results

    # --------------------------------------------------------------------------
    # Alert Generation with Cooldown
    # --------------------------------------------------------------------------

    def _generate_alerts(self, zone_results, config):

        alerts = []

        if not config.alert_config:
            return alerts

        alert_type_cfg = getattr(config.alert_config, "alert_type", ["Default"])
        alert_value_cfg = getattr(config.alert_config, "alert_value", ["JSON"])
        alert_type = alert_type_cfg[0]
        settings_map = {t: v for t, v in zip(alert_type_cfg, alert_value_cfg)}

        global_cooldown = config.alert_config.alert_cooldown or 0
        now_ts = time.time()

        for zone, stats in zone_results.items():

            if stats["severity"] != "critical":
                continue

            zone_cfg = config.zone_settings.get(zone, {})
            zone_cooldown = zone_cfg.get("cooldown", global_cooldown)

            if not self._should_trigger_alert(zone, zone_cooldown, now_ts):
                continue

            alert = self.create_alert_object(
                alert_type,
                f"alert_overcrowding_{zone}_{self._frame_counter}",
                self.CASE_TYPE,
                stats["threshold"],
                ascending=True,
                settings=settings_map,
            )

            alert["current_value"] = stats["count"]
            alert["zone"] = zone
            alert["severity"] = stats["severity"]

            alerts.append(alert)

            self._zone_alert_timestamps[zone] = now_ts

        return alerts


    def _should_trigger_alert(self, zone, cooldown, now_ts):
        last_ts = self._zone_alert_timestamps.get(zone)
        if last_ts is None:
            return True
        return (now_ts - last_ts) >= cooldown

    # --------------------------------------------------------------------------
    # Incident Generation
    # --------------------------------------------------------------------------

    def _generate_incidents(self, zone_results, alerts, stream_info):

        camera_info = self.get_camera_info_from_stream(stream_info)
        incidents = []

        for zone, stats in zone_results.items():

            if not stats["is_overcrowded"]:
                continue

            state = self._zone_states.get(zone, {})
            start_time = state.get("start_timestamp")

            human_text = (
                f"Overcrowding detected in zone '{zone}' | "
                f"Count: {stats['count']} | "
                f"Threshold: {stats['threshold']} | "
                f"Severity: {stats['severity']}"
            )
            zone_alerts = [
                a for a in alerts
                if a.get("zone") == zone
            ]

            incident = self.create_incident(
                incident_id=f"{self.CASE_TYPE}_{zone}_{self._frame_counter}",
                incident_type=self.CASE_TYPE,
                severity_level=stats["severity"],
                human_text=human_text,
                camera_info=camera_info,
                alerts=zone_alerts,
                alert_settings=[],
                start_time=start_time,
                end_time=None,
            )

            incidents.append(incident)

        return incidents




    # --------------------------------------------------------------------------
    # Tracking Stats
    # --------------------------------------------------------------------------

    def _generate_tracking_stats(self, detections, zone_results, alerts, stream_info):

        camera_info = self.get_camera_info_from_stream(stream_info)
        total_count = len(detections)

        tracking_stat = self.create_tracking_stats(
            total_counts=[{"category": "person", "count": total_count}],
            current_counts=[{"category": "person", "count": total_count}],
            detections=[
                self.create_detection_object(
                    "person",
                    d.get("bounding_box") or d.get("bbox")
                )
                for d in detections
            ],
            human_text=self._build_human_text(zone_results),
            camera_info=camera_info,
            alerts=alerts,
            alert_settings=[],
            reset_settings=[],
        )

        tracking_stat["zone_statistics"] = zone_results

        return [tracking_stat]

    # --------------------------------------------------------------------------
    # Business Analytics
    # --------------------------------------------------------------------------

    def _generate_business_analytics(self, zone_results, alerts, stream_info):

        camera_info = self.get_camera_info_from_stream(stream_info)

        analytics = self.create_business_analytics(
            analysis_name="overcrowding",
            statistics=zone_results,
            human_text=self._build_human_text(zone_results),
            camera_info=camera_info,
            alerts=alerts,
        )

        return [analytics]

    # --------------------------------------------------------------------------
    # Human Text
    # --------------------------------------------------------------------------

    def _build_human_text(self, zone_results):

        lines = ["Overcrowding Status:"]
        for zone, stats in zone_results.items():
            lines.append(
                f"{zone}: {stats['count']}/{stats['threshold']} "
                f"(ratio={stats['ratio']}) "
                f"severity={stats['severity']}"
            )
        return "\n".join(lines)

    # --------------------------------------------------------------------------
    # Cleanup
    # --------------------------------------------------------------------------

    def _cleanup_stale_zones(self, zone_counts):

        active_zones = set(zone_counts.keys())

        for z in list(self._zone_states.keys()):
            if z not in active_zones:
                del self._zone_states[z]

        for z in list(self._zone_alert_timestamps.keys()):
            if z not in active_zones:
                del self._zone_alert_timestamps[z]

    
    def _bbox_center(self, bbox: Any) -> Tuple[float, float]:
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