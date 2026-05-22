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

import logging
import time
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from ..core.base import (
    BaseProcessor,
    ConfigProtocol,
    ProcessingContext,
    ProcessingResult,
)
from ..core.config import AlertConfig, BaseConfig
from ..utils import (
    apply_category_mapping,
    filter_by_categories,
    filter_by_confidence,
    match_results_structure,
)

logger = logging.getLogger(__name__)

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
        **kwargs,
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
        self._tracking_start_time: Optional[float] = None

    def reset_state(self):
        self.__init__()

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
        if is_multi_frame:
            frames = data
        else:
            # Extract frame_id from stream_info
            frame_id = "0"
            if stream_info:
                frame_id = str(stream_info.get("input_settings", {}).get("start_frame", 0))
            frames = {frame_id: data}

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
                "incidents": incidents if incidents else {},
                "tracking_stats": tracking_stats if tracking_stats else {},
                "business_analytics": business_analytics if business_analytics else {},
                "alerts": alerts,
                "zone_analysis": {},
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

        logger.debug(
            "[PERF] F%s | latency=%.1fms%s",
            self._total_frames,
            latency_ms,
            f" fps={fps:.1f}" if fps else "",
        )

        # print(agg_summary)
        return result

    # ============================================================
    # Detection / bbox normalization (prod may send x1/y1, xmin, xyxy, etc.)
    # ============================================================

    def _raw_bbox_from_detection(self, det: Dict[str, Any]) -> Any:
        if not isinstance(det, dict):
            return None
        if "bounding_box" in det:
            bb = det["bounding_box"]
            if isinstance(bb, dict):
                return bb
            if isinstance(bb, (list, tuple)) and len(bb) >= 4:
                return bb
        if "bbox" in det:
            return det["bbox"]
        if "xyxy" in det:
            xy = det["xyxy"]
            if isinstance(xy, (list, tuple)) and len(xy) >= 4:
                return xy
        if "xywh" in det:
            xyw = det["xywh"]
            if isinstance(xyw, (list, tuple)) and len(xyw) >= 4:
                cx, cy, w, h = (
                    float(xyw[0]),
                    float(xyw[1]),
                    float(xyw[2]),
                    float(xyw[3]),
                )
                return [cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2]
        if all(k in det for k in ("x1", "y1", "x2", "y2")):
            return [det["x1"], det["y1"], det["x2"], det["y2"]]
        if all(k in det for k in ("xmin", "ymin", "xmax", "ymax")):
            return [det["xmin"], det["ymin"], det["xmax"], det["ymax"]]
        if all(k in det for k in ("x_min", "y_min", "x_max", "y_max")):
            return [det["x_min"], det["y_min"], det["x_max"], det["y_max"]]
        return None

    def _canonical_bounding_box(self, det: Dict[str, Any]) -> Optional[Dict[str, float]]:
        raw = self._raw_bbox_from_detection(det)
        if raw is None:
            return None

        x1: Optional[float] = None
        y1: Optional[float] = None
        x2: Optional[float] = None
        y2: Optional[float] = None

        if isinstance(raw, (list, tuple)) and len(raw) >= 4:
            x1, y1, x2, y2 = (float(raw[0]), float(raw[1]), float(raw[2]), float(raw[3]))
        elif isinstance(raw, dict):
            if all(k in raw for k in ("x_min", "y_min", "x_max", "y_max")):
                x1, y1, x2, y2 = (
                    float(raw["x_min"]),
                    float(raw["y_min"]),
                    float(raw["x_max"]),
                    float(raw["y_max"]),
                )
            elif all(k in raw for k in ("xmin", "ymin", "xmax", "ymax")):
                x1, y1, x2, y2 = (
                    float(raw["xmin"]),
                    float(raw["ymin"]),
                    float(raw["xmax"]),
                    float(raw["ymax"]),
                )
            elif all(k in raw for k in ("x1", "y1", "x2", "y2")):
                x1, y1, x2, y2 = (
                    float(raw["x1"]),
                    float(raw["y1"]),
                    float(raw["x2"]),
                    float(raw["y2"]),
                )
            elif all(k in raw for k in ("left", "top", "right", "bottom")):
                x1, y1, x2, y2 = (
                    float(raw["left"]),
                    float(raw["top"]),
                    float(raw["right"]),
                    float(raw["bottom"]),
                )
            elif all(k in raw for k in ("x", "y", "width", "height")):
                x1 = float(raw["x"])
                y1 = float(raw["y"])
                x2 = x1 + float(raw["width"])
                y2 = y1 + float(raw["height"])
            else:
                return None
        else:
            return None

        if x2 < x1:
            x1, x2 = x2, x1
        if y2 < y1:
            y1, y2 = y2, y1

        return {"xmin": x1, "ymin": y1, "xmax": x2, "ymax": y2}

    def _normalize_detection(self, det: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        if not isinstance(det, dict):
            return None
        bbox = self._canonical_bounding_box(det)
        if bbox is None:
            return None
        conf = float(det.get("confidence", det.get("conf", det.get("score", 0.0))))
        out = {
            "category": det.get("category", "corrosion"),
            "confidence": conf,
            "bounding_box": bbox,
        }
        for key in ("track_id", "frame_id", "category_id"):
            if key in det:
                out[key] = det[key]
        return out

    def _normalize_detections(self, detections: Any) -> List[Dict[str, Any]]:
        if not isinstance(detections, list):
            return []
        out: List[Dict[str, Any]] = []
        for d in detections:
            nd = self._normalize_detection(d) if isinstance(d, dict) else None
            if nd is not None:
                out.append(nd)
        return out

    # ============================================================
    # Frame Processing Logic
    # ============================================================

    def _process_frame(self, frame_data, config, _frame_id, stream_info):
        # print(f"\n[FRAME {frame_id}] Processing started")

        # Normalize detections
        _ = (_frame_id,)
        if isinstance(frame_data, list):
            detections = frame_data
        elif isinstance(frame_data, dict) and "predictions" in frame_data:
            detections = frame_data["predictions"]
        else:
            detections = []

        # print(f"[FRAME {frame_id}] Raw detections: {len(detections)}")

        detections = self._normalize_detections(detections)

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

        # Print bounding boxes (debug; bbox/conf were only for commented print)
        # for d in detections:
        #     bbox = ...
        #     print(f"[FRAME {frame_id}] CORROSION BOX: {bbox} ...")

        current_count = len(detections)

        # Update analytics
        self._total_frames += 1
        self._total_detections += current_count

        if current_count > 0:
            self._active_frames += 1

        # Update temporal validation state
        self._update_temporal_state(current_count, config)

        logger.debug(
            "[STATE] ActiveCounter=%s InactiveCounter=%s AlertActive=%s",
            self._active_counter,
            self._inactive_counter,
            self._alert_active,
        )

        # Generate standardized outputs
        alerts = self._generate_alerts(config, stream_info)
        incidents = self._generate_incidents(alerts, stream_info, config)
        tracking_stats = self._generate_tracking_stats(detections, alerts, stream_info, config)
        business_analytics = (
            self._generate_business_analytics(detections, alerts, stream_info) if config.enable_analytics else {}
        )
        summary = self._generate_summary(current_count, config, stream_info)

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

            merged.append(
                {
                    "category": "corrosion",
                    "confidence": merged_conf,
                    "bounding_box": merged_box,
                }
            )

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
        x1 = max(b1["xmin"], b2["xmin"])
        y1 = max(b1["ymin"], b2["ymin"])
        x2 = min(b1["xmax"], b2["xmax"])
        y2 = min(b1["ymax"], b2["ymax"])

        inter = max(0, x2 - x1) * max(0, y2 - y1)

        area1 = (b1["xmax"] - b1["xmin"]) * (b1["ymax"] - b1["ymin"])
        area2 = (b2["xmax"] - b2["xmin"]) * (b2["ymax"] - b2["ymin"])

        union = area1 + area2 - inter
        return inter / union if union > 0 else 0

    def _compute_containment(self, b1, b2):
        x1 = max(b1["xmin"], b2["xmin"])
        y1 = max(b1["ymin"], b2["ymin"])
        x2 = min(b1["xmax"], b2["xmax"])
        y2 = min(b1["ymax"], b2["ymax"])

        inter = max(0, x2 - x1) * max(0, y2 - y1)

        area1 = (b1["xmax"] - b1["xmin"]) * (b1["ymax"] - b1["ymin"])
        area2 = (b2["xmax"] - b2["xmin"]) * (b2["ymax"] - b2["ymin"])

        min_area = min(area1, area2)
        return inter / min_area if min_area > 0 else 0

    def _is_fully_inside(self, b1, b2):
        return (
            b1["xmin"] >= b2["xmin"]
            and b1["ymin"] >= b2["ymin"]
            and b1["xmax"] <= b2["xmax"]
            and b1["ymax"] <= b2["ymax"]
        ) or (
            b2["xmin"] >= b1["xmin"]
            and b2["ymin"] >= b1["ymin"]
            and b2["xmax"] <= b1["xmax"]
            and b2["ymax"] <= b1["ymax"]
        )

    def _merge_cluster_boxes(self, cluster):
        return {
            "xmin": min(b["xmin"] for b in cluster),
            "ymin": min(b["ymin"] for b in cluster),
            "xmax": max(b["xmax"] for b in cluster),
            "ymax": max(b["ymax"] for b in cluster),
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

    def _generate_alerts(self, config, _stream_info):
        _ = (_stream_info,)
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

    def _generate_incidents(self, alerts, stream_info, config):
        if not alerts:
            return {}

        camera_info = self.get_camera_info_from_stream(stream_info)

        alert_types = config.alert_config.alert_type if config.alert_config else ["Default"]
        alert_values = config.alert_config.alert_value if config.alert_config else ["JSON"]

        settings_map = {t: v for t, v in zip(alert_types, alert_values)}

        incident = self.create_incident(
            incident_id=self._alert_id,
            incident_type=self.name,
            severity_level="high",
            human_text="Pipe corrosion confirmed and alert active",
            camera_info=camera_info,
            alerts=alerts,
            alert_settings=[
                {
                    "alert_type": alert_types,
                    "incident_category": self.name,
                    "threshold_level": {"corrosion": config.activation_frames},
                    "ascending": True,
                    "settings": settings_map,
                }
            ],
            start_time=self._get_current_timestamp_str(stream_info),
            end_time="Incident still active",
            level_settings={"high": 3},
        )

        return incident

    def _generate_tracking_stats(self, detections, alerts, stream_info, config):
        camera_info = self.get_camera_info_from_stream(stream_info)

        total_counts = [{"category": "corrosion", "count": self._total_detections}]
        current_counts = [{"category": "corrosion", "count": len(detections)}]

        detection_objs = []
        for d in detections:
            obj = self.create_detection_object("corrosion", d["bounding_box"])

            # Inject confidence manually
            # obj["confidence"] = d.get("confidence", 0.0)

            detection_objs.append(obj)

        human_text = f"Current corrosion detections: {len(detections)}, Total detections: {self._total_detections}"

        input_ts = self._get_current_timestamp_str(stream_info)
        reset_ts = self._get_start_timestamp_str(stream_info)

        # ----------------------------
        # Alert Settings (canonical)
        # ----------------------------
        if config.alert_config:
            alert_types = config.alert_config.alert_type
            alert_values = config.alert_config.alert_value

            settings_map = {t: v for t, v in zip(alert_types, alert_values)}
            alert_settings = [
                {
                    "alert_type": alert_types,
                    "incident_category": self.name,
                    "threshold_level": {"corrosion": config.activation_frames},
                    "ascending": True,
                    "settings": settings_map,
                }
            ]
        else:
            alert_settings = []

        stat = self.create_tracking_stats(
            total_counts=total_counts,
            current_counts=current_counts,
            detections=detection_objs,
            human_text=human_text,
            camera_info=camera_info,
            alerts=alerts,
            alert_settings=alert_settings,
            reset_settings=[],
            start_time=input_ts,
            reset_time=reset_ts,
        )

        return stat

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

        return analytics

    def _generate_summary(self, current_count, _config, stream_info=None):
        _ = (_config,)
        current_ts = self._get_current_timestamp_str(stream_info)
        start_ts = self._get_start_timestamp_str(stream_info)

        lines = []
        lines.append(f"Application: {self.CASE_TYPE} v{self.CASE_VERSION}")

        lines.append(f"CURRENT FRAME @ {current_ts}:")
        lines.append(f"\t- Corrosion Detected: {current_count}")

        lines.append(f"TOTAL SINCE {start_ts}:")
        lines.append(f"\t- Total Corrosion Detections: {self._total_detections}")

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
            # Non-fatal: exception ignored here; execution continues per surrounding logic.
            pass

        return timestamp_clean

    def _get_current_timestamp_str(
        self,
        stream_info: Optional[Dict[str, Any]],
        precision=False,
        frame_id: Optional[str] = None,
    ) -> str:
        if not stream_info:
            return "00:00:00.00"
        if precision:
            if stream_info.get("input_settings", {}).get("start_frame", "na") != "na":
                if frame_id:
                    start_time = int(frame_id) / stream_info.get("input_settings", {}).get("original_fps", 30)
                else:
                    start_time = stream_info.get("input_settings", {}).get("start_frame", 30) / stream_info.get(
                        "input_settings", {}
                    ).get("original_fps", 30)
                _ = self._format_timestamp_for_video(start_time)
                return self._format_timestamp(stream_info.get("input_settings", {}).get("stream_time", "NA"))
            else:
                return datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")

        if stream_info.get("input_settings", {}).get("start_frame", "na") != "na":
            if frame_id:
                start_time = int(frame_id) / stream_info.get("input_settings", {}).get("original_fps", 30)
            else:
                start_time = stream_info.get("input_settings", {}).get("start_frame", 30) / stream_info.get(
                    "input_settings", {}
                ).get("original_fps", 30)
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
                        candidate = datetime.fromtimestamp(self._tracking_start_time, timezone.utc).strftime(
                            "%Y-%m-%d-%H:%M:%S.%f UTC"
                        )
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
