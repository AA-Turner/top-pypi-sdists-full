"""
Gas Leak Detection Use Case

Canonical Matrice-compliant industrial gas leak detection.
Includes spatial merging, temporal validation, analytics, alert generation,
and standardized agg_summary output.
"""

from typing import Any, Dict, List, Optional
from datetime import datetime, timezone
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
    filter_by_categories,
    apply_category_mapping,
    match_results_structure,
)


# ============================================================
# Configuration
# ============================================================

class PipeGasLeakDetectionConfig(BaseConfig):

    def __init__(
        self,
        usecase: str = "gas_leak_detection",
        category: str = "industrial",
        confidence_threshold: float = 0.25,
        target_categories: Optional[List[str]] = None,
        enable_analytics: bool = True,
        enable_spatial_merge: bool = True,
        iou_merge_threshold: float = 0.3,
        containment_threshold: float = 0.5,
        activation_frames: int = 4,
        deactivation_frames: int = 30,
        alert_cooldown_seconds: int = 30,
        index_to_category: Optional[Dict[int, str]] = None,
        alert_config: Optional[AlertConfig] = None,
        **kwargs
    ):
        super().__init__(usecase=usecase, category=category, **kwargs)

        self.confidence_threshold = confidence_threshold
        self.target_categories = target_categories or ["gas_leak"]
        self.enable_analytics = enable_analytics

        self.enable_spatial_merge = enable_spatial_merge
        self.iou_merge_threshold = iou_merge_threshold
        self.containment_threshold = containment_threshold

        self.activation_frames = activation_frames
        self.deactivation_frames = deactivation_frames
        self.alert_cooldown_seconds = alert_cooldown_seconds
        self.index_to_category = index_to_category
        self.alert_config = alert_config

    def validate(self) -> List[str]:
        errors = super().validate()

        if not 0.0 <= self.confidence_threshold <= 1.0:
            errors.append("confidence_threshold must be between 0.0 and 1.0")

        if self.activation_frames < 1:
            errors.append("activation_frames must be >= 1")

        if self.deactivation_frames < 1:
            errors.append("deactivation_frames must be >= 1")

        if self.alert_config:
            errors.extend(self.alert_config.validate())


        return errors


# ============================================================
# Use Case
# ============================================================

class PipeGasLeakDetectionUseCase(BaseProcessor):

    def __init__(self):
        super().__init__("pipe_gas_leak_detection")
        self.CASE_TYPE = "pipe_gas_leak_detection"
        self.CASE_VERSION = "1.0"
        self.category = "industrial"

        self.target_categories = ["gas_leak"]

        # Temporal state
        self._active_counter = 0
        self._inactive_counter = 0
        self._alert_active = False
        self._total_alerts_triggered = 0

        # Analytics state
        self._total_frames = 0
        self._total_detections = 0
        self._active_frames = 0

        # Persistent alert state
        self._alert_id = None
        self._alert_start_frame = None
        self._last_alert_time = 0

        self.start_timer = None
        self._tracking_start_time = None



    # ============================================================
    # Main Processing (Canonical)
    # ============================================================

    def process(
        self,
        data: Any,
        config: ConfigProtocol,
        context: Optional[ProcessingContext] = None,
        stream_info: Optional[Any] = None,
    ) -> ProcessingResult:
        
        print("Inside usecase module:", __name__)

        processing_start = time.time()

        if not isinstance(config, PipeGasLeakDetectionConfig):
            return self.create_error_result(
                "Invalid configuration type",
                usecase=self.name,
                category=self.category,
                context=context,
            )

        if context is None:
            context = ProcessingContext()

        # Canonical input format detection
        input_format = match_results_structure(data)
        context.input_format = input_format
        context.confidence_threshold = config.confidence_threshold

        errors = config.validate()
        if errors:
            context.mark_completed()
            return self.create_error_result(
                f"Configuration validation failed: {errors}",
                usecase=self.name,
                category=self.category,
                context=context,
            )
        
        # errors = config.validate()
        # print("VALIDATION ERRORS:", errors)

        # if errors:
        #     context.mark_completed()
        #     return self.create_error_result(
        #         f"Configuration validation failed: {errors}",
        #         usecase=self.name,
        #         category=self.category,
        #         context=context,
        #     )


        # Handle single or multi-frame uniformly
        is_multi_frame = self.detect_frame_structure(data)
        frames = data if is_multi_frame else {"current_frame": data}

        agg_summary = {}

        for frame_key, frame_data in frames.items():
            frame_id = str(frame_key)

            (
                incidents,
                tracking_stats,
                business_analytics,
                alerts,
                summary_text,
            ) = self._process_frame(frame_data, config, frame_id, stream_info)

            agg_summary[frame_id] = {
                "incidents": incidents,
                "tracking_stats": tracking_stats,
                "business_analytics": business_analytics,
                "alerts": alerts,
                "human_text": summary_text,
            }

        context.mark_completed()

        result = self.create_result(
            data={"agg_summary": agg_summary},
            usecase=self.name,
            category=self.category,
            context=context,
        )

        # Canonical performance logging
        proc_time = time.time() - processing_start
        latency_ms = proc_time * 1000.0
        fps = (1.0 / proc_time) if proc_time > 0 else None

        print(
            f"[PERF] F{self._total_frames} | "
            f"latency={latency_ms:.1f}ms "
            + (f"fps={fps:.1f}" if fps else "")
        )

        return result

    # ============================================================
    # Frame Processing
    # ============================================================

    def _process_frame(self, frame_data, config, frame_id, stream_info):

        # Normalize input structure
        if isinstance(frame_data, list):
            detections = frame_data
        elif isinstance(frame_data, dict) and "predictions" in frame_data:
            detections = frame_data["predictions"]
        else:
            detections = []

        # Filtering
        detections = filter_by_confidence(detections, config.confidence_threshold)

        if config.index_to_category:
            detections = apply_category_mapping(detections, config.index_to_category)

        detections = filter_by_categories(detections, config.target_categories)

        if config.enable_spatial_merge:
            detections = self._merge_detections(detections, config)

        current_count = len(detections)

        # Update analytics counters
        self._total_frames += 1
        self._total_detections += current_count

        if current_count > 0:
            self._active_frames += 1

        # state_changed = self._update_temporal_state(current_count, config)
        self._update_temporal_state(current_count, config)

        # Generate standardized components
        alerts = self._generate_alerts(config, stream_info)
        incidents = self._generate_incidents(alerts, stream_info)
        tracking_stats = self._generate_tracking_stats(detections, alerts, stream_info)
        business_analytics = (
            self._generate_business_analytics(detections, alerts, stream_info)
            if config.enable_analytics else []
        )
        summary = self._generate_summary(current_count)

        return incidents, tracking_stats, business_analytics, alerts, summary

    # ============================================================
    # Spatial Merge (Unchanged Logic)
    # ============================================================

    def _merge_detections(self, detections, config):

        boxes = [d.get("bounding_box") for d in detections]
        confs = [d.get("confidence") for d in detections]

        merged = []
        used = set()

        for i in range(len(boxes)):
            if i in used:
                continue

            base = boxes[i]
            cluster = [base]
            cluster_confs = [confs[i]]
            used.add(i)

            for j in range(i + 1, len(boxes)):
                if j in used:
                    continue
                if self._should_merge(base, boxes[j], config):
                    cluster.append(boxes[j])
                    cluster_confs.append(confs[j])
                    used.add(j)

            merged_box = self._merge_cluster_boxes(cluster)
            merged_conf = max(cluster_confs)

            merged.append({
                "category": "gas_leak",
                "confidence": merged_conf,
                "bounding_box": merged_box,
            })

        return merged

    def _should_merge(self, b1, b2, config):
        return (
            self._compute_iou(b1, b2) >= config.iou_merge_threshold
            or self._compute_containment(b1, b2) >= config.containment_threshold
        )

    def _compute_iou(self, b1, b2):
        x1 = max(b1["x_min"], b2["x_min"])
        y1 = max(b1["y_min"], b2["y_min"])
        x2 = min(b1["x_max"], b2["x_max"])
        y2 = min(b1["y_max"], b2["y_max"])

        inter = max(0, x2 - x1) * max(0, y2 - y1)
        area1 = (b1["x_max"] - b1["x_min"]) * (b1["y_max"] - b1["y_min"])
        area2 = (b2["x_max"] - b2["x_min"]) * (b2["y_max"] - b2["y_min"])

        union = area1 + area2 - inter
        return inter / union if union > 0 else 0

    def _compute_containment(self, b1, b2):
        x1 = max(b1["x_min"], b2["x_min"])
        y1 = max(b1["y_min"], b2["y_min"])
        x2 = min(b1["x_max"], b2["x_max"])
        y2 = min(b1["y_max"], b2["y_max"])

        inter = max(0, x2 - x1) * max(0, y2 - y1)
        area1 = (b1["x_max"] - b1["x_min"]) * (b1["y_max"] - b1["y_min"])
        area2 = (b2["x_max"] - b2["x_min"]) * (b2["y_max"] - b2["y_min"])

        min_area = min(area1, area2)
        return inter / min_area if min_area > 0 else 0

    def _merge_cluster_boxes(self, cluster):
        return {
            "x_min": min(b["x_min"] for b in cluster),
            "y_min": min(b["y_min"] for b in cluster),
            "x_max": max(b["x_max"] for b in cluster),
            "y_max": max(b["y_max"] for b in cluster),
        }

    # ============================================================
    # Temporal Logic (Unchanged)
    # ============================================================

    def _update_temporal_state(self, current_count, config):

        if current_count > 0:
            self._active_counter += 1
            self._inactive_counter = 0

            if not self._alert_active and self._active_counter >= config.activation_frames:
                self._alert_active = True
                self._total_alerts_triggered += 1
                self._alert_id = f"gas_leak_{self._total_frames}"
                self._alert_start_frame = self._total_frames

        else:
            self._inactive_counter += 1
            self._active_counter = 0

            if self._alert_active and self._inactive_counter >= config.deactivation_frames:
                self._alert_active = False
                self.start_timer = None
                self._tracking_start_time = None
                self._alert_id = None
                self._alert_start_frame = None

        return self._alert_active

    # ============================================================
    # Canonical Generators
    # ============================================================

    # def _generate_alerts(self, config: PipeGasLeakDetectionConfig, stream_info):

    #     if not self._alert_active:
    #         return []

    #     if not config.alert_config:
    #         return []

    #     # Respect cooldown
    #     cooldown = getattr(config.alert_config, "alert_cooldown", 0)
    #     if cooldown and hasattr(self, "_last_alert_time"):
    #         if time.time() - self._last_alert_time < cooldown:
    #             return []

    #     alert_types = getattr(config.alert_config, "alert_type", ["Default"])
    #     alert_values = getattr(config.alert_config, "alert_value", ["JSON"])

    #     settings_map = {
    #         t: v for t, v in zip(alert_types, alert_values)
    #     }

    #     alert = self.create_alert_object(
    #         alert_type=alert_types[0],
    #         alert_id=self._alert_id,
    #         incident_category=self.name,
    #         threshold_value=config.activation_frames,
    #         ascending=True,
    #         settings=settings_map,
    #     )

    #     alert["status"] = "active"
    #     alert["start_frame"] = self._alert_start_frame
    #     alert["current_frame"] = self._total_frames
    #     alert["duration_frames"] = self._total_frames - self._alert_start_frame

    #     self._last_alert_time = time.time()

    #     return [alert]

    def _generate_alerts(self, config: PipeGasLeakDetectionConfig, stream_info):

        if not self._alert_active:
            return []

        if not config.alert_config:
            return []

        alert_types = getattr(config.alert_config, "alert_type", ["Default"])
        alert_values = getattr(config.alert_config, "alert_value", ["JSON"])

        settings_map = {
            t: v for t, v in zip(alert_types, alert_values)
        }

        alert = self.create_alert_object(
            alert_type=alert_types[0],
            alert_id=self._alert_id,
            incident_category=self.name,
            threshold_value=config.activation_frames,
            ascending=True,
            settings=settings_map,
        )

        alert["status"] = "active"
        alert["start_frame"] = self._alert_start_frame
        alert["current_frame"] = self._total_frames
        alert["duration_frames"] = self._total_frames - self._alert_start_frame

        # ---------------------------------------------------
        # NEW: Separate emission logic
        # ---------------------------------------------------
        cooldown = getattr(config.alert_config, "alert_cooldown", 0)

        emit_allowed = True
        if cooldown > 0:
            if time.time() - self._last_alert_time < cooldown:
                emit_allowed = False

        alert["emit"] = emit_allowed   # <-- NEW FIELD

        if emit_allowed:
            self._last_alert_time = time.time()

        return [alert]


    def _generate_incidents(self, alerts, stream_info):

        if not alerts:
            return []

        camera_info = self.get_camera_info_from_stream(stream_info)

        alert_settings = []

        if alerts:
            alert_obj = alerts[0]
            alert_settings.append({
                "alert_type": alert_obj.get("alert_type"),
                "incident_category": self.name,
                "threshold_value": alert_obj.get("threshold_value"),
                "ascending": True,
                "settings": alert_obj.get("settings", {}),
            })

        start_timestamp = self._get_start_timestamp_str(stream_info)
        current_timestamp = self._get_current_timestamp_str(stream_info)

        incident = self.create_incident(
            incident_id=self._alert_id,
            incident_type=self.name,
            severity_level="critical",
            human_text="Gas leak confirmed and alert active",
            camera_info=camera_info,
            alerts=alerts,
            alert_settings=alert_settings,
            start_time=start_timestamp,
            end_time="active" if self._alert_active else current_timestamp,
            level_settings={"critical": 5},
        )

        return [incident]



    def _generate_tracking_stats(self, detections, alerts, stream_info):

        camera_info = self.get_camera_info_from_stream(stream_info)

        total_counts = [
            {"category": "gas_leak", "count": self._total_detections}
        ]
        current_counts = [
            {"category": "gas_leak", "count": len(detections)}
        ]

        detection_objs = [
            self.create_detection_object("gas_leak", d["bounding_box"])
            for d in detections
        ]

        human_text = (
            f"Current gas detections: {len(detections)}, "
            f"Total detections: {self._total_detections}"
        )

        current_timestamp = self._get_current_timestamp_str(stream_info, precision=False)
        # high_precision_start_timestamp = self._get_current_timestamp_str(stream_info, precision=True)
        # high_precision_reset_timestamp = self._get_start_timestamp_str(stream_info, precision=True)

        high_precision_start_timestamp = self._get_start_timestamp_str(stream_info, precision=True)
        high_precision_reset_timestamp = None



        stat = self.create_tracking_stats(
            total_counts=total_counts,
            current_counts=current_counts,
            detections=detection_objs,
            human_text=human_text,
            camera_info=camera_info,
            alerts=alerts,
            alert_settings=[],
            reset_settings=[],
            start_time=high_precision_start_timestamp,
            reset_time=high_precision_reset_timestamp,
            # current_time=current_timestamp,
        )

        return [stat]

    def _generate_business_analytics(self, detections, alerts, stream_info):

        camera_info = self.get_camera_info_from_stream(stream_info)

        analytics_stats = {
            "total_frames": self._total_frames,
            "total_alerts_triggered": self._total_alerts_triggered,
            "active_frames": self._active_frames,
            "gas_presence_ratio": self._active_frames / max(1, self._total_frames),
            "current_detections": len(detections),
        }

        text = f"Gas presence ratio: {analytics_stats['gas_presence_ratio']:.2f}"

        analytics = self.create_business_analytics(
            analysis_name="gas_leak_analytics",
            statistics=analytics_stats,
            human_text=text,
            camera_info=camera_info,
            alerts=alerts,
        )

        return [analytics]

 
    def _generate_summary(self, current_count):

        lines = []
        lines.append("Application Name: " + self.CASE_TYPE)
        lines.append("Application Version: " + self.CASE_VERSION)

        # Tracking statistics
        lines.append("Tracking Statistics:")
        lines.append(f"- Current gas detections: {current_count}")
        lines.append(f"- Total detections: {self._total_detections}")

        # Business analytics
        lines.append("Business Analytics:")
        lines.append(f"- Total frames processed: {self._total_frames}")
        lines.append(f"- Total alerts triggered: {self._total_alerts_triggered}")
        lines.append(f"- Gas presence ratio: {self._active_frames / max(1, self._total_frames):.2f}")

        if self._alert_active:
            lines.append("Status: GAS LEAK CONFIRMED (CRITICAL)")
        elif current_count > 0:
            lines.append(f"Status: Gas detected ({self._active_counter} validation frames)")
        else:
            lines.append("Status: No gas leak detected")

        return "\n".join(lines)


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