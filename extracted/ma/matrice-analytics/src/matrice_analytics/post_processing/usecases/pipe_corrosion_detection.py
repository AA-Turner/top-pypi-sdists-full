"""
Pipe Corrosion Detection Use Case

Canonical Matrice-compliant industrial pipe corrosion detection.
Includes:
- Confidence filtering
- Category filtering (ignores "mask")
- Spatial merging (IoU + containment + full-inside logic)
- Temporal validation (activation/deactivation frames)
- Alert generation with cooldown
- Incident creation
- Tracking statistics (detection-based only, no tracking)
- Business analytics
- Standardized agg_summary output

Severity is always set to "high".
"""

from typing import Any, Dict, List, Optional
from datetime import datetime, timezone
import time
import uuid

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

class PipeCorrosionDetectionConfig(BaseConfig):
    """
    Configuration for Pipe Corrosion Detection Use Case.

    Includes:
    - Confidence filtering
    - Spatial merge thresholds
    - Temporal validation parameters
    - Alert cooldown settings
    """

    def __init__(
        self,
        usecase: str = "pipe_corrosion_detection",
        category: str = "industrial",
        confidence_threshold: float = 0.25,
        target_categories: Optional[List[str]] = None,
        enable_spatial_merge: bool = True,
        iou_merge_threshold: float = 0.3,
        containment_threshold: float = 0.5,
        activation_frames: int = 10,
        deactivation_frames: int = 10,
        alert_cooldown_seconds: int = 30,
        enable_analytics: bool = True,
        index_to_category: Optional[Dict[int, str]] = None,
        alert_config: Optional[AlertConfig] = None,
        **kwargs
    ):
        super().__init__(usecase=usecase, category=category, **kwargs)

        self.confidence_threshold = confidence_threshold
        self.target_categories = target_categories or ["corrosion"]

        self.enable_spatial_merge = enable_spatial_merge
        self.iou_merge_threshold = iou_merge_threshold
        self.containment_threshold = containment_threshold

        self.activation_frames = activation_frames
        self.deactivation_frames = deactivation_frames
        self.alert_cooldown_seconds = alert_cooldown_seconds

        self.enable_analytics = enable_analytics
        self.index_to_category = index_to_category
        self.alert_config = alert_config

    def validate(self) -> List[str]:
        errors = super().validate()

        if not 0.0 <= self.confidence_threshold <= 1.0:
            errors.append("confidence_threshold must be between 0 and 1")

        if self.activation_frames < 1:
            errors.append("activation_frames must be >= 1")

        if self.deactivation_frames < 1:
            errors.append("deactivation_frames must be >= 1")

        if self.alert_config:
            errors.extend(self.alert_config.validate())

        if self.alert_cooldown_seconds < 0:
            errors.append("alert_cooldown must be >= 0")

        return errors


# ============================================================
# Use Case
# ============================================================

class PipeCorrosionDetectionUseCase(BaseProcessor):

    def __init__(self):
        super().__init__("pipe_corrosion_detection")

        self.CASE_TYPE = "pipe_corrosion_detection"
        self.CASE_VERSION = "1.0"
        self.category = "industrial"

        # -----------------------------
        # Temporal State Variables
        # -----------------------------
        self._active_counter = 0
        self._inactive_counter = 0
        self._alert_active = False
        self._total_alerts_triggered = 0

        self._alert_id = None
        self._alert_start_frame = None
        self._last_alert_time = 0

        # -----------------------------
        # Analytics Counters
        # -----------------------------
        self._total_frames = 0
        self._total_detections = 0
        self._active_frames = 0

        self.start_timer = None


    # ============================================================
    # Main Processing Entry
    # ============================================================

    def process(
        self,
        data: Any,
        config: ConfigProtocol,
        context: Optional[ProcessingContext] = None,
        stream_info: Optional[Any] = None,
    ) -> ProcessingResult:

        # print("Inside pipe_corrosion module:", __name__)

        processing_start = time.time()

        # Validate configuration type
        if not isinstance(config, PipeCorrosionDetectionConfig):
            return self.create_error_result(
                "Invalid configuration type",
                usecase=self.name,
                category=self.category,
                context=context,
            )

        if context is None:
            context = ProcessingContext()

        # Detect input structure (single frame or multi-frame)
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

        # Canonical multi-frame handling
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

        # Performance logging
        proc_time = time.time() - processing_start
        latency_ms = proc_time * 1000.0
        fps = (1.0 / proc_time) if proc_time > 0 else None

        print(
            f"[PERF] F{self._total_frames} | "
            f"latency={latency_ms:.1f}ms "
            + (f"fps={fps:.1f}" if fps else "")
        )

        # print(agg_summary)
        return result


    # ============================================================
    # Frame Processing Logic
    # ============================================================

    def _process_frame(self, frame_data, config, frame_id, stream_info):

        # print(f"\n[FRAME {frame_id}] Processing started")

        # Normalize detections
        if isinstance(frame_data, list):
            detections = frame_data
        elif isinstance(frame_data, dict) and "predictions" in frame_data:
            detections = frame_data["predictions"]
        else:
            detections = []

        # print(f"[FRAME {frame_id}] Raw detections: {len(detections)}")

        # Step 1 — Confidence filtering
        detections = filter_by_confidence(detections, config.confidence_threshold)

        # Step 2 — Category mapping if model uses index
        if config.index_to_category:
            detections = apply_category_mapping(detections, config.index_to_category)

        # Step 3 — Keep ONLY corrosion detections
        detections = filter_by_categories(detections, config.target_categories)

        # print(f"[FRAME {frame_id}] After filtering corrosion only: {len(detections)}")

        # Step 4 — Spatial merge
        if config.enable_spatial_merge:
            detections = self._merge_detections(detections, config)

        # print(f"[FRAME {frame_id}] After merging: {len(detections)}")

        # Print bounding boxes
        for d in detections:
            bbox = d["bounding_box"]
            conf = d.get("confidence", 0.0)

            # print(
            #     f"[FRAME {frame_id}] CORROSION BOX: {bbox} "
            #     f"| Confidence: {conf:.4f}"
            # )

        current_count = len(detections)

        # Update analytics
        self._total_frames += 1
        self._total_detections += current_count

        if current_count > 0:
            self._active_frames += 1

        # Update temporal validation state
        self._update_temporal_state(current_count, config)

        print(
            f"[STATE] ActiveCounter={self._active_counter} "
            f"InactiveCounter={self._inactive_counter} "
            f"AlertActive={self._alert_active}"
        )

        # Generate standardized outputs
        alerts = self._generate_alerts(config, stream_info)
        incidents = self._generate_incidents(alerts, stream_info)
        tracking_stats = self._generate_tracking_stats(detections, alerts, stream_info)
        business_analytics = (
            self._generate_business_analytics(detections, alerts, stream_info)
            if config.enable_analytics else []
        )
        summary = self._generate_summary(current_count, config)

        return incidents, tracking_stats, business_analytics, alerts, summary


    # ============================================================
    # Spatial Merge Logic
    # ============================================================

    def _merge_detections(self, detections, config):
        """
        Merge:
        - Intersecting boxes (IoU)
        - Contained boxes
        - Fully inside boxes
        """

        boxes = [d["bounding_box"] for d in detections]
        confs = [d["confidence"] for d in detections]

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
                "category": "corrosion",
                "confidence": merged_conf,
                "bounding_box": merged_box,
            })
        
            # print(f"[MERGE] Cluster size: {len(cluster)} | Max confidence: {merged_conf:.4f}")

        return merged


    def _should_merge(self, b1, b2, config):

        # IoU condition
        if self._compute_iou(b1, b2) >= config.iou_merge_threshold:
            return True

        # Containment condition
        if self._compute_containment(b1, b2) >= config.containment_threshold:
            return True

        # Full inside condition
        if self._is_fully_inside(b1, b2):
            return True

        return False


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


    def _is_fully_inside(self, b1, b2):
        return (
            b1["x_min"] >= b2["x_min"] and
            b1["y_min"] >= b2["y_min"] and
            b1["x_max"] <= b2["x_max"] and
            b1["y_max"] <= b2["y_max"]
        ) or (
            b2["x_min"] >= b1["x_min"] and
            b2["y_min"] >= b1["y_min"] and
            b2["x_max"] <= b1["x_max"] and
            b2["y_max"] <= b1["y_max"]
        )


    def _merge_cluster_boxes(self, cluster):
        return {
            "x_min": min(b["x_min"] for b in cluster),
            "y_min": min(b["y_min"] for b in cluster),
            "x_max": max(b["x_max"] for b in cluster),
            "y_max": max(b["y_max"] for b in cluster),
        }


    # ============================================================
    # Temporal State Update
    # ============================================================

    def _update_temporal_state(self, current_count, config):

        if current_count > 0:
            self._active_counter += 1
            self._inactive_counter = 0

            if not self._alert_active and self._active_counter >= config.activation_frames:
                self._alert_active = True
                self._total_alerts_triggered += 1
                # Generate globally unique alert ID
                self._alert_id = f"corrosion_{uuid.uuid4().hex[:8]}"

                self._alert_start_frame = self._total_frames

        else:
            self._inactive_counter += 1
            self._active_counter = 0

            if self._alert_active and self._inactive_counter >= config.deactivation_frames:
                self._alert_active = False
                self._alert_id = None
                self._alert_start_frame = None


    # ============================================================
    # Alert, Incident, Analytics, Summary
    # ============================================================

    def _generate_alerts(self, config, stream_info):

        if not self._alert_active or not config.alert_config:
            return []

        alert_types = getattr(config.alert_config, "alert_type", ["Default"])
        alert_values = getattr(config.alert_config, "alert_value", ["JSON"])

        settings_map = {t: v for t, v in zip(alert_types, alert_values)}

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

        incident = self.create_incident(
            incident_id=self._alert_id,
            incident_type=self.name,
            severity_level="high",
            human_text="Pipe corrosion confirmed and alert active",
            camera_info=camera_info,
            alerts=alerts,
            alert_settings=[],
            start_time=self._get_current_timestamp_str(stream_info),
            end_time="active",
            level_settings={"high": 3},
        )

        return [incident]


    def _generate_tracking_stats(self, detections, alerts, stream_info):

        camera_info = self.get_camera_info_from_stream(stream_info)

        total_counts = [{"category": "corrosion", "count": self._total_detections}]
        current_counts = [{"category": "corrosion", "count": len(detections)}]

        detection_objs = []
        for d in detections:
            obj = self.create_detection_object(
                "corrosion",
                d["bounding_box"]
            )

            # Inject confidence manually
            obj["confidence"] = d.get("confidence", 0.0)

            detection_objs.append(obj)


        human_text = (
            f"Current corrosion detections: {len(detections)}, "
            f"Total detections: {self._total_detections}"
        )

        stat = self.create_tracking_stats(
            total_counts=total_counts,
            current_counts=current_counts,
            detections=detection_objs,
            human_text=human_text,
            camera_info=camera_info,
            alerts=alerts,
            alert_settings=[],
            reset_settings=[],
            start_time=self._get_current_timestamp_str(stream_info),
            reset_time=None,
        )

        return [stat]


    def _generate_business_analytics(self, detections, alerts, stream_info):

        camera_info = self.get_camera_info_from_stream(stream_info)

        analytics_stats = {
            "total_frames": self._total_frames,
            "total_alerts_triggered": self._total_alerts_triggered,
            "active_frames": self._active_frames,
            "corrosion_presence_ratio": self._active_frames / max(1, self._total_frames),
            "current_detections": len(detections),
        }

        analytics = self.create_business_analytics(
            analysis_name="corrosion_analytics",
            statistics=analytics_stats,
            human_text=f"Corrosion presence ratio: {analytics_stats['corrosion_presence_ratio']:.2f}",
            camera_info=camera_info,
            alerts=alerts,
        )

        return [analytics]


    def _generate_summary(self, current_count, config):

        lines = []
        lines.append("Application Name: " + self.CASE_TYPE)
        lines.append("Application Version: " + self.CASE_VERSION)

        lines.append("Tracking Statistics:")
        lines.append(f"- Current corrosion detections: {current_count}")
        lines.append(f"- Total detections: {self._total_detections}")

        lines.append("Business Analytics:")
        lines.append(f"- Total frames processed: {self._total_frames}")
        lines.append(f"- Total alerts triggered: {self._total_alerts_triggered}")
        lines.append(f"- Corrosion presence ratio: {self._active_frames / max(1, self._total_frames):.2f}")

        if self._alert_active:
            lines.append("Status: CORROSION CONFIRMED (HIGH)")
        elif current_count > 0:
            lines.append(
                f"Status: Corrosion detected "
                f"({self._active_counter}/{config.activation_frames} validation frames)"
            )
        else:
            lines.append("Status: No corrosion detected")

        return "\n".join(lines)

    # ----------------------------
    # Timestamp helpers 
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
