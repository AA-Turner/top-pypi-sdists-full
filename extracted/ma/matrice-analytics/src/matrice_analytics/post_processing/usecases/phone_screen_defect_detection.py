"""
Phone Screen Defect Detection Use Case

Detects defects on phone screens (scratches, cracks, dead pixels, discoloration, etc.)
using object detection with bbox merging, ByteTrack tracking, analytics,
alert generation and standardized agg_summary output.
"""

import time
from typing import Any, Dict, List, Optional

import numpy as np

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

try:
    from ultralytics.trackers.byte_tracker import BYTETracker
except ImportError:
    BYTETracker = None
from types import SimpleNamespace


class PhoneScreenDefectDetectionConfig(BaseConfig):
    def __init__(
        self,
        usecase: str = "phone_screen_defect_detection",
        category: str = "industrial",
        confidence_threshold: float = 0.4,
        target_categories: Optional[List[str]] = None,
        enable_bbox_merge: bool = True,
        merge_iou_threshold: float = 0.4,
        containment_threshold: float = 0.7,
        enable_tracking: bool = True,
        alert_config: Optional[AlertConfig] = None,
        index_to_category: Optional[Dict[int, str]] = None,
        **kwargs,
    ):
        super().__init__(usecase=usecase, category=category, **kwargs)

        self.confidence_threshold = confidence_threshold
        self.target_categories = target_categories or ["Scratched"]

        self.enable_bbox_merge = enable_bbox_merge
        self.merge_iou_threshold = merge_iou_threshold
        self.containment_threshold = containment_threshold

        self.enable_tracking = enable_tracking
        self.alert_config = alert_config
        self.index_to_category = index_to_category if index_to_category is not None else {0: "Scratched"}

    def validate(self):
        errors = super().validate()

        if not 0 <= self.confidence_threshold <= 1:
            errors.append("confidence_threshold must be between 0 and 1")

        if self.merge_iou_threshold < 0:
            errors.append("merge_iou_threshold must be >= 0")

        if self.containment_threshold < 0:
            errors.append("containment_threshold must be >= 0")

        if self.alert_config:
            errors.extend(self.alert_config.validate() or [])

        return errors


class PhoneScreenDefectDetectionUseCase(BaseProcessor):
    def __init__(self):
        super().__init__("phone_screen_defect_detection")

        self.CASE_TYPE = "phone_screen_defect_detection"
        self.CASE_VERSION = "1.0"

        self.category = "industrial"

        self._total_frames = 0
        self._total_defects = 0

        self._unique_tracks = set()

        self._tracker = None

        self._img_size = (1080, 1920)

        self._last_alert_time = 0

        self.start_timer = None
        self._tracking_start_time = None

    # ============================================================
    # Main Process
    # ============================================================

    def process(
        self,
        data: Any,
        config: ConfigProtocol,
        context: Optional[ProcessingContext] = None,
        stream_info: Optional[Any] = None,
    ) -> ProcessingResult:
        start_time = time.time()

        if not isinstance(config, PhoneScreenDefectDetectionConfig):
            self._debug_elapsed_since(start_time)
            return self.create_error_result(
                "Invalid configuration type",
                usecase=self.name,
                category=self.category,
                context=context,
            )

        if context is None:
            context = ProcessingContext()

        input_format = match_results_structure(data)
        context.input_format = input_format
        context.confidence_threshold = config.confidence_threshold

        errors = config.validate()
        if errors:
            context.mark_completed()
            self._debug_elapsed_since(start_time)
            return self.create_error_result(
                f"Configuration validation failed: {errors}",
                usecase=self.name,
                category=self.category,
                context=context,
            )

        is_multi_frame = self.detect_frame_structure(data)
        frames = data if is_multi_frame else {"current_frame": data}

        if stream_info:
            settings = stream_info.get("input_settings", {})
            self._img_size = settings.get("frame_size", (1080, 1920))
        else:
            self._img_size = (1080, 1920)

        agg_summary = {}

        for frame_key, frame_data in frames.items():
            frame_number = None
            if stream_info:
                input_settings = stream_info.get("input_settings", {})
                frame_number = input_settings.get("start_frame")
            frame_id = str(frame_number) if frame_number is not None else str(frame_key)

            (
                incidents,
                tracking_stats,
                business_analytics,
                alerts,
                summary,
            ) = self._process_frame(frame_data, config, frame_id, stream_info)

            agg_summary[frame_id] = {
                "incidents": incidents if isinstance(incidents, dict) else (incidents[0] if incidents else {}),
                "tracking_stats": (
                    tracking_stats
                    if isinstance(tracking_stats, dict)
                    else (tracking_stats[0] if tracking_stats else {})
                ),
                "business_analytics": (
                    business_analytics
                    if isinstance(business_analytics, dict)
                    else (business_analytics[0] if business_analytics else {})
                ),
                "alerts": alerts,
                "zone_analysis": {},
                "human_text": summary,
            }

        context.mark_completed()

        result = self.create_result(
            data={"agg_summary": agg_summary},
            usecase=self.name,
            category=self.category,
            context=context,
        )

        latency = (time.time() - start_time) * 1000

        self.logger.info(f"[PERF] F{self._total_frames} | latency={latency:.1f}ms")

        self._debug_elapsed_since(start_time)
        return result

    # ============================================================
    # Frame Processing
    # ============================================================

    def _process_frame(self, frame_data, config, _frame_id, stream_info):
        _ = (_frame_id,)
        if isinstance(frame_data, list):
            detections = frame_data
        elif isinstance(frame_data, dict) and "predictions" in frame_data:
            detections = frame_data["predictions"]
        else:
            detections = []

        detections = filter_by_confidence(
            detections,
            config.confidence_threshold,
        )

        if config.index_to_category:
            detections = apply_category_mapping(
                detections,
                config.index_to_category,
            )

        detections = filter_by_categories(
            detections,
            config.target_categories,
        )

        if config.enable_bbox_merge:
            detections = self._merge_detections(detections, config)

        current_count = len(detections)

        self._total_frames += 1
        self._total_defects += current_count

        alerts = self._generate_alerts(config, current_count)
        incidents = self._generate_incidents(alerts, stream_info)

        tracking_stats = self._generate_tracking_stats(
            detections,
            alerts,
            stream_info,
        )

        business_analytics = self._generate_business_analytics(
            detections,
            alerts,
            stream_info,
        )

        summary = self._generate_summary(current_count)

        return incidents, tracking_stats, business_analytics, alerts, summary

    # ============================================================
    # Spatial Merge
    # ============================================================

    def _merge_detections(self, detections, config):
        merged = []
        used = set()

        for i, det1 in enumerate(detections):
            if i in used:
                continue

            box1 = det1["bounding_box"]

            cluster = [box1]
            confs = [det1["confidence"]]

            used.add(i)

            for j, det2 in enumerate(detections[i + 1 :], start=i + 1):
                if j in used:
                    continue

                box2 = det2["bounding_box"]

                if (
                    self._compute_iou(box1, box2) >= config.merge_iou_threshold
                    or self._compute_containment(box1, box2) >= config.containment_threshold
                ):
                    cluster.append(box2)
                    confs.append(det2["confidence"])
                    used.add(j)

            merged_box = self._merge_cluster_boxes(cluster)

            merged.append(
                {
                    "category": det1.get("category", "Scratched"),
                    "confidence": max(confs),
                    "bounding_box": merged_box,
                }
            )

        return merged

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
    # Tracking
    # ============================================================

    def _get_tracker(self):
        """Lazily initialise BYTETracker on first use."""
        if self._tracker is None:
            if BYTETracker is None:
                raise ImportError("BYTETracker not available. Install ultralytics: pip install ultralytics")
            tracker_args = SimpleNamespace(
                track_thresh=0.25,
                track_high_thresh=0.5,
                track_buffer=30,
                match_thresh=0.8,
                frame_rate=30,
            )
            self._tracker = BYTETracker(tracker_args)
        return self._tracker

    def _run_tracking(self, detections):
        if not detections:
            return []

        tracks_input = []

        for det in detections:
            bbox = det["bounding_box"]

            x1 = bbox["x_min"]
            y1 = bbox["y_min"]
            x2 = bbox["x_max"]
            y2 = bbox["y_max"]

            score = det.get("confidence", 1.0)

            tracks_input.append([x1, y1, x2, y2, score])

        tracks_input = np.array(tracks_input)

        tracker = self._get_tracker()
        tracks = tracker.update(tracks_input)

        tracked = []

        for t in tracks:
            x1, y1, x2, y2 = t.tlbr
            track_id = int(t.track_id)

            tracked.append(
                {
                    "category": "Scratched",
                    "confidence": float(t.score),
                    "track_id": track_id,
                    "bounding_box": {
                        "x_min": float(x1),
                        "y_min": float(y1),
                        "x_max": float(x2),
                        "y_max": float(y2),
                    },
                }
            )

            self._unique_tracks.add(track_id)

        return tracked

    # ============================================================
    # Alerts
    # ============================================================

    def _generate_alerts(self, config, count):
        if not config.alert_config:
            return []

        threshold = config.alert_config.count_thresholds.get("Scratched", None)

        if threshold is None:
            return []

        if count < threshold:
            return []

        if time.time() - self._last_alert_time < config.alert_config.alert_cooldown:
            return []

        alert = self.create_alert_object(
            alert_type="defect_threshold",
            alert_id=f"phone_screen_defect_{self._total_frames}",
            incident_category=self.name,
            threshold_value=threshold,
            ascending=True,
            settings={"threshold": threshold},
        )

        self._last_alert_time = time.time()

        return [alert]

    # ============================================================
    # Incidents
    # ============================================================

    def _generate_incidents(self, alerts, stream_info):
        if not alerts:
            return []

        camera_info = self.get_camera_info_from_stream(stream_info)

        incident = self.create_incident(
            incident_id=alerts[0]["alert_id"],
            incident_type=self.name,
            severity_level="critical",
            human_text="Phone screen defect detected",
            camera_info=camera_info,
            alerts=alerts,
        )

        return incident

    # ============================================================
    # Tracking Stats
    # ============================================================

    def _generate_tracking_stats(self, detections, alerts, stream_info):
        camera_info = self.get_camera_info_from_stream(stream_info)

        detection_objs = []
        for d in detections:
            bbox = d["bounding_box"]
            bbox_canonical = {
                "xmin": bbox["x_min"],
                "ymin": bbox["y_min"],
                "xmax": bbox["x_max"],
                "ymax": bbox["y_max"],
            }
            detection_objs.append(self.create_detection_object(d.get("category", "Scratched"), bbox_canonical))

        total_counts = [{"category": "Scratched", "count": self._total_defects}]
        current_counts = [{"category": "Scratched", "count": len(detections)}]

        stat = self.create_tracking_stats(
            total_counts=total_counts,
            current_counts=current_counts,
            detections=detection_objs,
            human_text=f"Current defects: {len(detections)}",
            camera_info=camera_info,
            alerts=alerts,
        )

        return stat

    # ============================================================
    # Business Analytics
    # ============================================================

    def _generate_business_analytics(self, _detections, alerts, stream_info):
        _ = (_detections,)
        camera_info = self.get_camera_info_from_stream(stream_info)

        analytics = {
            "total_frames": self._total_frames,
            "total_defects": self._total_defects,
            "unique_defect_tracks": len(self._unique_tracks),
        }

        analytics_obj = self.create_business_analytics(
            analysis_name="phone_screen_defect_analytics",
            statistics=analytics,
            human_text=f"Total defects detected: {self._total_defects}",
            camera_info=camera_info,
            alerts=alerts,
        )

        return analytics_obj

    # ============================================================
    # Summary
    # ============================================================

    def _generate_summary(self, current_count):
        lines = []

        lines.append("Application Name: " + self.CASE_TYPE)
        lines.append("Application Version: " + self.CASE_VERSION)

        lines.append(f"Current defects: {current_count}")
        lines.append(f"Total defects: {self._total_defects}")
        lines.append(f"Total frames: {self._total_frames}")

        return "\n".join(lines)
