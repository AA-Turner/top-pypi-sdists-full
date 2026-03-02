"""
Liquid Leak Detection Use Case

Canonical Matrice-compliant industrial liquid leak detection.

This usecase performs:
1. Detection filtering (confidence + category)
2. Optional spatial merging of overlapping detections
3. Temporal validation (activation + deactivation logic)
4. Alert generation with cooldown control
5. Incident creation
6. Tracking statistics generation
7. Business analytics generation
8. Standardized frame-wise agg_summary output

All visualization logic must be handled outside this file.
This module is purely post-processing logic.
"""

from typing import Any, Dict, List, Optional
from datetime import datetime, timezone
import time

# Core framework abstractions
from ..core.base import (
    BaseProcessor,         # Base class providing standardized result structure
    ProcessingContext,     # Context object for performance + metadata tracking
    ProcessingResult,      # Standard result container returned by process()
    ConfigProtocol,        # Config typing interface
)

# Core configuration base classes
from ..core.config import BaseConfig, AlertConfig

# Utility functions for detection filtering & format handling
from ..utils import (
    filter_by_confidence,      # Removes detections below threshold
    filter_by_categories,      # Keeps only target categories
    apply_category_mapping,    # Optional class-index to label mapping
    match_results_structure,   # Detects input structure (single frame / multi frame)
)


# ============================================================
# Configuration
# ============================================================

class LiquidLeakDetectionConfig(BaseConfig):
    """
    Configuration class for Liquid Leak Detection.

    Extends BaseConfig and adds:
    - Spatial merging parameters
    - Temporal validation parameters
    - Cooldown control
    - Analytics toggles
    """

    def __init__(
        self,
        usecase: str = "liquid_leak_detection",
        category: str = "industrial",

        # Confidence filtering threshold
        confidence_threshold: float = 0.25,

        # Target object classes to monitor
        target_categories: Optional[List[str]] = None,

        # Enable/disable business analytics output
        enable_analytics: bool = True,

        # Enable/disable spatial merging of overlapping detections
        enable_spatial_merge: bool = True,
        iou_merge_threshold: float = 0.5,
        containment_threshold: float = 0.6,

        # Temporal validation settings
        activation_frames: int = 3,
        deactivation_frames: int = 40,

        # Alert emission cooldown (seconds)
        alert_cooldown_seconds: int = 30,

        # Optional mapping from model index → category name
        index_to_category: Optional[Dict[int, str]] = None,

        # AlertConfig controls alert formatting & channels
        alert_config: Optional[AlertConfig] = None,

        **kwargs
    ):
        # Initialize BaseConfig fields (usecase + category + common fields)
        super().__init__(usecase=usecase, category=category, **kwargs)

        # Store configuration values
        self.confidence_threshold = confidence_threshold
        self.target_categories = target_categories or ["liquid_leak"]
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
        """
        Validates configuration parameters before processing.
        Ensures no invalid thresholds or misconfiguration.
        """
        errors = super().validate()

        # Confidence must be normalized
        if not 0.0 <= self.confidence_threshold <= 1.0:
            errors.append("confidence_threshold must be between 0.0 and 1.0")

        # Temporal logic must have positive activation window
        if self.activation_frames < 1:
            errors.append("activation_frames must be >= 1")

        if self.deactivation_frames < 1:
            errors.append("deactivation_frames must be >= 1")

        # Validate nested AlertConfig if provided
        if self.alert_config:
            errors.extend(self.alert_config.validate())

        # Cooldown must not be negative
        if self.alert_cooldown_seconds < 0:
            errors.append("alert_cooldown_seconds must be >= 0")

        return errors


# ============================================================
# Use Case
# ============================================================

class LiquidLeakDetectionUseCase(BaseProcessor):
    """
    Industrial liquid leak detection usecase.

    Responsibilities:
    - Process frame detections
    - Apply filtering and merging
    - Maintain temporal state
    - Generate alerts and incidents
    - Produce standardized agg_summary output
    """

    def __init__(self):
        # Initialize BaseProcessor with usecase name
        super().__init__("liquid_leak_detection")

        # Metadata
        self.CASE_TYPE = "liquid_leak_detection"
        self.CASE_VERSION = "1.0"
        self.category = "industrial"

        # Target detection class
        self.target_categories = ["liquid_leak"]

        # -------------------------
        # Temporal State Variables
        # -------------------------

        # Counts consecutive frames where leak detected
        self._active_counter = 0

        # Counts consecutive frames where leak absent
        self._inactive_counter = 0

        # Whether alert is currently active
        self._alert_active = False

        # Number of alerts triggered since start
        self._total_alerts_triggered = 0

        # -------------------------
        # Analytics State Variables
        # -------------------------

        # Total processed frames
        self._total_frames = 0

        # Total detections across frames
        self._total_detections = 0

        # Frames containing at least one detection
        self._active_frames = 0

        # -------------------------
        # Alert Runtime State
        # -------------------------

        self._alert_id = None
        self._alert_start_frame = None
        self._last_alert_time = 0  # For cooldown tracking

        # Timestamp helpers
        self.start_timer = None
        self._tracking_start_time = None

    # ============================================================
    # Default Config Factory
    # ============================================================

    def create_default_config(self, **overrides) -> LiquidLeakDetectionConfig:
        """
        Creates a default configuration instance.

        Allows override of any field via kwargs.
        Used for testing and quick experimentation.
        """
        config = LiquidLeakDetectionConfig(
            confidence_threshold=overrides.get("confidence_threshold", 0.25),
            target_categories=overrides.get("target_categories", ["liquid_leak"]),
            enable_analytics=overrides.get("enable_analytics", True),
            enable_spatial_merge=overrides.get("enable_spatial_merge", True),
            iou_merge_threshold=overrides.get("iou_merge_threshold", 0.5),
            containment_threshold=overrides.get("containment_threshold", 0.6),
            activation_frames=overrides.get("activation_frames", 3),
            deactivation_frames=overrides.get("deactivation_frames", 40),
            alert_cooldown_seconds=overrides.get("alert_cooldown_seconds", 10),
            alert_config=overrides.get("alert_config", AlertConfig())
        )
        return config

    # ============================================================
    # Main Processing
    # ============================================================

    def process(
        self,
        data: Any,
        config: ConfigProtocol,
        context: Optional[ProcessingContext] = None,
        stream_info: Optional[Any] = None,
    ) -> ProcessingResult:
        """
        Main entry point for processing detection results.

        This function:
        - Validates configuration
        - Detects input format
        - Processes each frame independently
        - Builds standardized frame-wise agg_summary
        - Returns ProcessingResult
        """

        processing_start = time.time()

        # Ensure correct config type
        if not isinstance(config, LiquidLeakDetectionConfig):
            return self.create_error_result(
                "Invalid configuration type",
                usecase=self.name,
                category=self.category,
                context=context,
            )

        # Initialize context if missing
        if context is None:
            context = ProcessingContext()

        # Identify input format (list / dict / multi-frame)
        input_format = match_results_structure(data)
        context.input_format = input_format
        context.confidence_threshold = config.confidence_threshold

        # Validate configuration
        errors = config.validate()
        if errors:
            context.mark_completed()
            return self.create_error_result(
                f"Configuration validation failed: {errors}",
                usecase=self.name,
                category=self.category,
                context=context,
            )

        # Detect whether input contains multiple frames
        is_multi_frame = self.detect_frame_structure(data)
        frames = data if is_multi_frame else {"current_frame": data}

        # Dictionaries keyed by frame_id
        frame_incidents = {}
        frame_tracking_stats = {}
        frame_business_analytics = {}
        frame_alerts = {}
        frame_human_text = {}

        # Process each frame independently
        for frame_key, frame_data in frames.items():
            frame_id = str(frame_key)

            (
                incidents,
                tracking_stats,
                business_analytics,
                alerts,
                summary_text,
            ) = self._process_frame(frame_data, config, frame_id, stream_info)

            frame_incidents[frame_id] = incidents
            frame_tracking_stats[frame_id] = tracking_stats
            frame_business_analytics[frame_id] = business_analytics
            frame_alerts[frame_id] = alerts
            frame_human_text[frame_id] = summary_text

        # Construct standardized frame-wise agg_summary structure
        agg_summary = self.create_frame_wise_agg_summary(
            frame_incidents,
            frame_tracking_stats,
            frame_business_analytics,
            frame_alerts,
            frame_human_text,
        )

        context.mark_completed()

        # Wrap into ProcessingResult
        result = self.create_result(
            data={"agg_summary": agg_summary},
            usecase=self.name,
            category=self.category,
            context=context,
        )

        # Performance logging
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

        if isinstance(frame_data, list):
            detections = frame_data
        elif isinstance(frame_data, dict) and "predictions" in frame_data:
            detections = frame_data["predictions"]
        else:
            detections = []

        detections = filter_by_confidence(detections, config.confidence_threshold)

        if config.index_to_category:
            detections = apply_category_mapping(detections, config.index_to_category)

        detections = filter_by_categories(detections, config.target_categories)

        if config.enable_spatial_merge:
            detections = self._merge_detections(detections, config)

        current_count = len(detections)

        self._total_frames += 1
        self._total_detections += current_count

        if current_count > 0:
            self._active_frames += 1

        self._update_temporal_state(current_count, config)

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
    # Spatial Merge (Same as Gas)
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
                "category": "liquid_leak",
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
    # Temporal Logic (Same Pattern)
    # ============================================================

    def _update_temporal_state(self, current_count, config):

        if current_count > 0:
            self._active_counter += 1
            self._inactive_counter = 0

            if not self._alert_active and self._active_counter >= config.activation_frames:
                self._alert_active = True
                self._total_alerts_triggered += 1
                self._alert_id = f"liquid_leak_{self._total_frames}"
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
    # Alerts / Incidents / Stats / Analytics / Summary
    # ============================================================

    def _generate_alerts(self, config: LiquidLeakDetectionConfig, stream_info):

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

        # cooldown = getattr(config.alert_config, "alert_cooldown", 0)
        cooldown = config.alert_cooldown_seconds

        emit_allowed = True
        if cooldown > 0:
            if time.time() - self._last_alert_time < cooldown:
                emit_allowed = False

        alert["emit"] = emit_allowed

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
            human_text="Liquid leak confirmed and alert active",
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
            {"category": "liquid_leak", "count": self._total_detections}
        ]
        current_counts = [
            {"category": "liquid_leak", "count": len(detections)}
        ]

        detection_objs = [
            self.create_detection_object("liquid_leak", d["bounding_box"])
            for d in detections
        ]

        human_text = (
            f"Current liquid detections: {len(detections)}, "
            f"Total detections: {self._total_detections}"
        )

        high_precision_start_timestamp = self._get_start_timestamp_str(stream_info, precision=True)

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
            reset_time=None,
        )

        return [stat]


    def _generate_business_analytics(self, detections, alerts, stream_info):

        camera_info = self.get_camera_info_from_stream(stream_info)

        analytics_stats = {
            "total_frames": self._total_frames,
            "total_alerts_triggered": self._total_alerts_triggered,
            "active_frames": self._active_frames,
            "liquid_presence_ratio": self._active_frames / max(1, self._total_frames),
            "current_detections": len(detections),
        }

        text = f"Liquid presence ratio: {analytics_stats['liquid_presence_ratio']:.2f}"

        analytics = self.create_business_analytics(
            analysis_name="liquid_leak_analytics",
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

        lines.append("Tracking Statistics:")
        lines.append(f"- Current liquid detections: {current_count}")
        lines.append(f"- Total detections: {self._total_detections}")

        lines.append("Business Analytics:")
        lines.append(f"- Total frames processed: {self._total_frames}")
        lines.append(f"- Total alerts triggered: {self._total_alerts_triggered}")
        lines.append(f"- Liquid presence ratio: {self._active_frames / max(1, self._total_frames):.2f}")

        if self._alert_active:
            lines.append("Status: LIQUID LEAK CONFIRMED (CRITICAL)")
        elif current_count > 0:
            lines.append(f"Status: Leak detected ({self._active_counter} validation frames)")
        else:
            lines.append("Status: No liquid leak detected")

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