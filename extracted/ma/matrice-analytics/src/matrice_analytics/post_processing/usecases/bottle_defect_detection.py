"""
Bottle Defect Detection Use Case

Canonical Matrice-compliant bottle inspection use case. Structure mirrors
``pipe_corrosion_detection.py`` so the QUALITY family stays interchangeable:
- Detection / bbox normalization (accepts x1y1x2y2, xyxy, xywh, xmin, x_min, ...)
- Confidence filtering
- Category mapping + filtering
- Spatial merging (IoU or containment)
- AdvancedTracker for stable track_ids (drives current_new_counts)
- Alert generation with cooldown
- Incident creation
- Tracking statistics with all four canonical count fields
- ``quality_analytics`` side-channel block for legacy_analytics_bridge
- Business analytics
- Standardized agg_summary output
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
from ..Trackers import ConfigDrivenTracker, TrackerProfile
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


class BottleDefectDetectionConfig(BaseConfig):
    """Configuration for the Bottle Defect Detection use case."""

    def __init__(
        self,
        usecase: str = "bottle_defect_detection",
        category: str = "industrial",
        confidence_threshold: float = 0.4,
        target_categories: Optional[List[str]] = None,
        enable_bbox_merge: bool = True,
        merge_iou_threshold: float = 0.4,
        containment_threshold: float = 0.7,
        enable_tracking: bool = True,
        enable_analytics: bool = True,
        alert_cooldown_seconds: int = 60,
        alert_config: Optional[AlertConfig] = None,
        index_to_category: Optional[Dict[int, str]] = None,
        **kwargs,
    ):
        super().__init__(usecase=usecase, category=category, **kwargs)

        self.confidence_threshold = confidence_threshold
        self.target_categories = target_categories or ["defect"]

        self.enable_bbox_merge = enable_bbox_merge
        self.merge_iou_threshold = merge_iou_threshold
        self.containment_threshold = containment_threshold

        self.enable_tracking = enable_tracking
        self.enable_analytics = enable_analytics
        # Declared explicitly because the shipped deployment config
        # (assets/config_files/bottle-defect/bottle-defect-detection.json) sets
        # extra_params.alert_cooldown_seconds. Without this parameter the value
        # falls through **kwargs into BaseConfig.__init__ and raises TypeError,
        # so the real config could not be loaded at all. Same field name as
        # PipeCorrosionDetectionConfig.
        self.alert_cooldown_seconds = alert_cooldown_seconds
        self.alert_config = alert_config
        self.index_to_category = index_to_category

    def validate(self):
        errors = super().validate()

        if not 0 <= self.confidence_threshold <= 1:
            errors.append("confidence_threshold must be between 0 and 1")

        if self.merge_iou_threshold < 0:
            errors.append("merge_iou_threshold must be >= 0")

        if self.containment_threshold < 0:
            errors.append("containment_threshold must be >= 0")

        if self.alert_cooldown_seconds < 0:
            errors.append("alert_cooldown_seconds must be >= 0")

        if self.alert_config:
            errors.extend(self.alert_config.validate() or [])

        return errors


# ============================================================
# Use Case
# ============================================================


class BottleDefectDetectionUseCase(BaseProcessor):
    """Bottle inspection: defective units per window, plus defect presence time."""

    # Single-class model (deployment config maps index 0 -> "defect"). Upstream
    # casing varies by training run, so normalize before any membership check --
    # skipping this silently zeroes quality_analytics while results-agg keeps
    # publishing on schedule.
    CATEGORY_NORMALIZE = {
        "defect": "defect",
        "Defect": "defect",
        "DEFECT": "defect",
        "bottle_defect": "defect",
        "Bottle-Defect": "defect",
        "bottle-defect": "defect",
    }

    CATEGORY_DISPLAY = {"defect": "Defect"}

    # Two-tier QUALITY split. Defect-only model: every inspected object IS a
    # defect, so the two tuples are identical and defect_rate is pinned at 1.0
    # (which is why the manifest publishes defect_presence instead). Kept
    # explicit so the shape matches solar_panel, where they genuinely differ.
    INSPECTION_CATEGORIES = ("defect",)
    DEFECT_CATEGORIES = ("defect",)

    def __init__(self):
        super().__init__("bottle_defect_detection")

        self.CASE_TYPE = "bottle_defect_detection"
        self.CASE_VERSION = "1.1"
        self.category = "industrial"

        self.target_categories = ["defect"]

        # -----------------------------
        # Analytics counters
        # -----------------------------
        self._total_frames = 0
        # Raw per-frame detection sum. NOT a unique count -- used only for the
        # peak/average style figures in business_analytics and the human_text.
        self._total_defects = 0
        self._active_frames = 0
        # Longest unbroken run of defect-present frames this session, in frames;
        # converted to seconds for max_continuous_seconds.
        self._active_streak = 0
        self._max_active_streak = 0

        # -----------------------------
        # Tracking state (AdvancedTracker)
        # -----------------------------
        self.tracker = None
        self._tracker_seam = ConfigDrivenTracker()
        self._per_category_total_track_ids = {cat: set() for cat in self.target_categories}
        self._current_frame_track_ids = {cat: set() for cat in self.target_categories}
        self._new_track_ids_this_frame = {cat: set() for cat in self.target_categories}

        # Alert cooldown anchor. Stamped with time.monotonic() so a wall-clock step
        # backwards (NTP correction, VM restore) cannot suppress alerts past the
        # cooldown. None means "never emitted", so the first alert always fires --
        # a 0 sentinel is unsafe here because monotonic() may start near zero.
        self._last_alert_monotonic: Optional[float] = None
        self._total_alerts_triggered = 0

        # -----------------------------
        # Incident lifecycle (see _generate_incidents)
        # -----------------------------
        self._incident_active = False
        # Stable for the whole episode -- an id that changes per frame is read
        # downstream as a brand-new incident every frame, so nothing ever closes.
        self._incident_id: Optional[str] = None
        # Last active incident, re-emitted once with a real end_time on the frame
        # the episode ends. Without this the close is never published.
        self._last_incident_snapshot: Optional[Dict[str, Any]] = None
        self.current_incident_end_timestamp: str = "N/A"

        self.start_timer = None
        self._tracking_start_time: Optional[float] = None

    def reset_state(self):
        self.__init__()

    @staticmethod
    def _severity_for_count(count: int) -> str:
        """Count-based severity: 1-2 defects -> 'high', >=3 -> 'critical'.

        Same shape as PipeCorrosionDetectionUseCase._severity_for_count, and it
        matches the level_settings registered on the incident below.
        """
        return "critical" if int(count) >= 3 else "high"

    # ============================================================
    # Category normalization
    # ============================================================

    @classmethod
    def _normalize_category(cls, category: Any) -> str:
        """Canonical snake_case label for filtering and QUALITY metrics."""
        if category is None:
            return ""
        raw = str(category).strip()
        if raw in cls.CATEGORY_NORMALIZE:
            return cls.CATEGORY_NORMALIZE[raw]
        for canonical, display in cls.CATEGORY_DISPLAY.items():
            if raw == display or raw.lower() == display.lower():
                return canonical
        return raw.lower().replace(" ", "_").replace("-", "_")

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
        processing_start = time.time()

        if not isinstance(config, BottleDefectDetectionConfig):
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
            return self.create_error_result(
                f"Configuration validation failed: {errors}",
                usecase=self.name,
                category=self.category,
                context=context,
            )

        # Canonical multi-frame handling (same as pipe_corrosion_detection).
        is_multi_frame = self.detect_frame_structure(data)
        if is_multi_frame:
            frames = data
        else:
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

        proc_time = time.time() - processing_start
        logger.debug("[PERF] F%s | latency=%.1fms", self._total_frames, proc_time * 1000.0)

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
                cx, cy, w, h = (float(xyw[0]), float(xyw[1]), float(xyw[2]), float(xyw[3]))
                return [cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2]
        if all(k in det for k in ("x1", "y1", "x2", "y2")):
            return [det["x1"], det["y1"], det["x2"], det["y2"]]
        if all(k in det for k in ("xmin", "ymin", "xmax", "ymax")):
            return [det["xmin"], det["ymin"], det["xmax"], det["ymax"]]
        if all(k in det for k in ("x_min", "y_min", "x_max", "y_max")):
            return [det["x_min"], det["y_min"], det["x_max"], det["y_max"]]
        return None

    def _canonical_bounding_box(self, det: Dict[str, Any]) -> Optional[Dict[str, float]]:
        """Return the bbox as ``{xmin, ymin, xmax, ymax}``.

        ``xmin`` (no underscore) is the form AdvancedTracker and
        ``create_detection_object`` expect -- an ``x_min`` bbox is silently
        dropped by the tracker's bbox parser.
        """
        raw = self._raw_bbox_from_detection(det)
        if raw is None:
            return None

        x1 = y1 = x2 = y2 = None

        if isinstance(raw, (list, tuple)) and len(raw) >= 4:
            x1, y1, x2, y2 = (float(raw[0]), float(raw[1]), float(raw[2]), float(raw[3]))
        elif isinstance(raw, dict):
            for keys in (
                ("x_min", "y_min", "x_max", "y_max"),
                ("xmin", "ymin", "xmax", "ymax"),
                ("x1", "y1", "x2", "y2"),
                ("left", "top", "right", "bottom"),
            ):
                if all(k in raw for k in keys):
                    x1, y1, x2, y2 = (
                        float(raw[keys[0]]),
                        float(raw[keys[1]]),
                        float(raw[keys[2]]),
                        float(raw[keys[3]]),
                    )
                    break
            else:
                if all(k in raw for k in ("x", "y", "width", "height")):
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
            "category": det.get("category", "defect"),
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
        _ = (_frame_id,)
        if isinstance(frame_data, list):
            detections = frame_data
        elif isinstance(frame_data, dict) and "predictions" in frame_data:
            detections = frame_data["predictions"]
        else:
            detections = []

        detections = self._normalize_detections(detections)

        # Step 1 -- Confidence filtering
        detections = filter_by_confidence(detections, config.confidence_threshold)

        # Step 2 -- Category mapping if the model emits indices
        if config.index_to_category:
            detections = apply_category_mapping(detections, config.index_to_category)

        # Step 3 -- Canonicalize labels, then keep only target categories.
        # BOTH sides are normalized so a deployment JSON carrying "Defect"
        # matches the canonical "defect" detections.
        for det in detections:
            det["category"] = self._normalize_category(det.get("category"))
        normalized_targets = [self._normalize_category(c) for c in (config.target_categories or [])]
        detections = filter_by_categories(detections, normalized_targets)

        # Step 4 -- Spatial merge (several flaws on one bottle -> one detection)
        if config.enable_bbox_merge:
            detections = self._merge_detections(detections, config)

        # Step 5 -- Tracker: attach stable track_ids (drives current_new_counts)
        if config.enable_tracking:
            detections = self._apply_tracker(detections)
        self._update_tracking_state(detections)

        current_count = len(detections)

        self._total_frames += 1
        self._total_defects += current_count

        if current_count > 0:
            self._active_frames += 1
            self._active_streak += 1
            self._max_active_streak = max(self._max_active_streak, self._active_streak)
        else:
            self._active_streak = 0

        alerts = self._generate_alerts(config, current_count)
        incidents = self._generate_incidents(alerts, stream_info, current_count, config)
        tracking_stats = self._generate_tracking_stats(detections, alerts, stream_info, config)
        business_analytics = (
            self._generate_business_analytics(detections, alerts, stream_info) if config.enable_analytics else {}
        )
        summary = self._generate_summary(current_count, stream_info)

        return incidents, tracking_stats, business_analytics, alerts, summary

    # ============================================================
    # Tracking (AdvancedTracker) + current_new_counts support
    # ============================================================

    def _apply_tracker(self, detections: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Attach stable track_ids via AdvancedTracker; pass through on failure."""
        try:
            if self.tracker is None:
                self.tracker = self._tracker_seam.get_shared_tracker(profile=TrackerProfile.DEFAULT)
                logger.info("Initialized AdvancedTracker for Bottle Defect Detection")
            return self.tracker.update(detections)
        except Exception as e:  # pragma: no cover - defensive
            logger.warning("AdvancedTracker failed: %s", e)
            return detections

    def _update_tracking_state(self, detections: List[Dict[str, Any]]) -> None:
        """Maintain per-category total / current / newly-seen track id sets."""
        self._current_frame_track_ids = {cat: set() for cat in self.target_categories}
        new_ids = {cat: set() for cat in self.target_categories}
        for det in detections:
            cat = det.get("category")
            track_id = det.get("track_id")
            if cat not in self.target_categories or track_id is None:
                continue
            seen = self._per_category_total_track_ids.setdefault(cat, set())
            if track_id not in seen:
                new_ids[cat].add(track_id)
            seen.add(track_id)
            self._current_frame_track_ids[cat].add(track_id)
        self._new_track_ids_this_frame = new_ids

    def get_total_counts(self) -> Dict[str, int]:
        """Cumulative UNIQUE track_id count per category."""
        return {cat: len(ids) for cat, ids in self._per_category_total_track_ids.items()}

    def get_new_counts_this_frame(self) -> Dict[str, int]:
        """Track_ids seen for the FIRST time this frame, per category."""
        return {cat: len(ids) for cat, ids in self._new_track_ids_this_frame.items()}

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
            confs = [det1.get("confidence", 0.0)]
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
                    confs.append(det2.get("confidence", 0.0))
                    used.add(j)

            merged.append(
                {
                    "category": det1.get("category", "defect"),
                    "confidence": max(confs) if confs else 0.0,
                    "bounding_box": self._merge_cluster_boxes(cluster),
                }
            )

        return merged

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

    def _merge_cluster_boxes(self, cluster):
        return {
            "xmin": min(b["xmin"] for b in cluster),
            "ymin": min(b["ymin"] for b in cluster),
            "xmax": max(b["xmax"] for b in cluster),
            "ymax": max(b["ymax"] for b in cluster),
        }

    # ============================================================
    # Alerts / Incidents
    # ============================================================

    def _generate_alerts(self, config, count):
        if not config.alert_config:
            return []

        thresholds = getattr(config.alert_config, "count_thresholds", None) or {}
        threshold = thresholds.get("defect", thresholds.get("all"))

        if threshold is None or count < threshold:
            return []

        # AlertConfig.alert_cooldown wins when set; otherwise fall back to the
        # deployment's alert_cooldown_seconds.
        cooldown = getattr(config.alert_config, "alert_cooldown", 0) or config.alert_cooldown_seconds or 0
        now = time.monotonic()
        if self._last_alert_monotonic is not None and now - self._last_alert_monotonic < cooldown:
            return []

        alert_types = getattr(config.alert_config, "alert_type", ["Default"]) or ["Default"]
        alert_values = getattr(config.alert_config, "alert_value", ["JSON"]) or ["JSON"]

        alert = self.create_alert_object(
            alert_type=alert_types[0],
            alert_id=f"defect_{self._total_frames}",
            incident_category=self.name,
            threshold_value=threshold,
            ascending=True,
            settings={t: v for t, v in zip(alert_types, alert_values)},
        )

        self._last_alert_monotonic = now
        self._total_alerts_triggered += 1

        return [alert]

    def _build_alert_settings(self, config, alerts) -> List[Dict[str, Any]]:
        """Canonical ``alert_settings`` entries.

        Mirrors intrusion_detection: prefer the real alert objects when present
        (so the published settings match what actually fired), else fall back to
        the deployment's AlertConfig. Uses ``threshold_value`` -- the key
        ``BaseProcessor.create_alert_object`` emits -- so alerts[] and
        alert_settings[] agree on one spelling.
        """
        if alerts:
            return [
                {
                    "alert_type": a.get("alert_type"),
                    "incident_category": self.name,
                    "threshold_value": a.get("threshold_value"),
                    "ascending": a.get("ascending", True),
                    "settings": a.get("settings", {}),
                }
                for a in alerts
                if isinstance(a, dict)
            ]
        if config.alert_config and hasattr(config.alert_config, "alert_type"):
            alert_types = getattr(config.alert_config, "alert_type", ["Default"]) or ["Default"]
            alert_values = getattr(config.alert_config, "alert_value", ["JSON"]) or ["JSON"]
            return [
                {
                    "alert_type": alert_types,
                    "incident_category": self.name,
                    "threshold_value": getattr(config.alert_config, "count_thresholds", None),
                    "ascending": True,
                    "settings": {t: v for t, v in zip(alert_types, alert_values)},
                }
            ]
        return []

    def _generate_incidents(self, alerts, stream_info, count, config):
        """Incident lifecycle with an explicit closing frame.

        Three states, and the closing frame is the one that is easy to miss:

        1. ACTIVE  -> emit the incident with ``end_time = ""``. The empty string
           is a lifecycle placeholder (``incident_res_format``
           ``_INCIDENT_END_TIME_PLACEHOLDERS``); any real timestamp here would be
           read downstream as "this incident has closed".
        2. JUST ENDED -> re-emit the LAST active incident once, with a real
           ``end_time``. This extra frame is the only thing that ever publishes a
           closing timestamp -- previously the episode simply stopped appearing
           in agg_summary and the incident stayed open forever.
        3. IDLE -> ``{}``.

        ``create_incident`` computes ``end_time or timestamp``, which silently
        turns ``""`` back into ``start_time`` -- a real timestamp, i.e. every
        active frame would look like a close. The explicit re-assignment after
        the call is required, not defensive (same guard as
        intrusion_detection.py).

        Activity here is DEFECT PRESENCE, not ``bool(alerts)``: alerts are
        threshold-gated and need an AlertConfig, so keying the incident off them
        meant a deployment without count_thresholds produced no incidents at all.
        """
        camera_info = self.get_camera_info_from_stream(stream_info)
        current_timestamp = self._get_current_timestamp_str(stream_info)
        incident_active = count > 0

        if incident_active:
            if not self._incident_active:
                self._incident_active = True
                self._incident_id = f"{self.CASE_TYPE}_{uuid.uuid4().hex[:8]}"
            # Held at "" for the whole active episode.
            self.current_incident_end_timestamp = ""

            severity = self._severity_for_count(count)
            incident = self.create_incident(
                incident_id=self._incident_id,
                incident_type=self.name,
                severity_level=severity,
                human_text=f"Bottle defect detected (defects={count}, severity={severity})",
                camera_info=camera_info,
                alerts=alerts,
                alert_settings=self._build_alert_settings(config, alerts),
                start_time=self._get_start_timestamp_str(stream_info),
                end_time=self.current_incident_end_timestamp,
                level_settings={"high": 1, "critical": 3},
            )
            # See docstring: create_incident coerces a falsy end_time to start_time.
            incident["end_time"] = self.current_incident_end_timestamp
            incident["incident_quant"] = float(count)
            self._last_incident_snapshot = dict(incident)
            return incident

        if self._incident_active and self._last_incident_snapshot is not None:
            closing = dict(self._last_incident_snapshot)
            closing["end_time"] = current_timestamp
            closing["human_text"] = "Bottle defect incident closed"
            self._last_incident_snapshot = None
            self._incident_active = False
            self.current_incident_end_timestamp = "N/A"
            return closing

        self._incident_active = False
        self.current_incident_end_timestamp = "N/A"
        return {}

    # ============================================================
    # QUALITY analytics block (results-agg via legacy_analytics_bridge)
    # ============================================================

    @staticmethod
    def _get_fps(stream_info: Optional[Dict[str, Any]]) -> float:
        """Stream FPS for frame->seconds conversion; 30.0 when unavailable."""
        if stream_info:
            try:
                fps = (stream_info.get("input_settings", {}) or {}).get("original_fps")
                if fps and float(fps) > 1e-6:
                    return float(fps)
            except (TypeError, ValueError, AttributeError):
                pass
        return 30.0

    def _compute_quality_analytics(
        self, detections: List[Dict[str, Any]], stream_info: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Per-frame QUALITY block stored at ``tracking_stats["quality_analytics"]``.

        Emitted on EVERY frame, including idle ones -- ``total_frames`` is the
        presence denominator, so skipping idle frames would make
        ``defect_presence`` read 100% for any intermittent defect.

        The field set is deliberately a SUPERSET of the two existing bridge
        contracts so one hook can serve this app either way:

          * pipe family (``_ingest_pipe_defect_analytics``) reads
            ``current_count`` / ``total_unique_count`` / ``frame_new_ids`` /
            ``is_active`` / ``frame_seconds`` / ``max_continuous_seconds``.
          * car damage (``_ingest_car_damage_quality``) reads ``defect_count`` /
            ``total_inspected`` / ``frame_defect_ids`` / ``frame_inspected_ids``.

        Mapping to the manifest metrics (bottle-defect.yaml):
          defect_count       <- union of frame_defect_ids over the window (agg sum)
          total_defect_count <- total_unique_count                       (agg last)
          defect_presence    <- active frames / frames in window * 100    (agg avg)

        ``frame_new_ids`` vs ``frame_defect_ids`` is a real distinction, not a
        duplicate: ``frame_new_ids`` holds only track_ids seen for the FIRST time
        (union = defects that ARRIVED this window), while ``frame_defect_ids``
        holds every defect id in frame (union = defects OBSERVED this window,
        including ones carried over from the previous window). Both are emitted
        so the bridge can pick the semantics the metric needs.

        ``frame_seconds`` / ``max_continuous_seconds`` are emitted even though
        this app's metric set does not publish a duration -- they let a duration
        metric be added in the manifest without touching this use case, and they
        keep the block interchangeable with the pipe apps.
        """
        inspected_ids: set = set()
        defect_ids: set = set()
        total_inspected = 0
        defect_count = 0

        for det in detections:
            cat = self._normalize_category(det.get("category", ""))
            if cat not in self.INSPECTION_CATEGORIES:
                continue
            total_inspected += 1
            tid = det.get("track_id")
            if tid is not None:
                inspected_ids.add(tid)
            if cat in self.DEFECT_CATEGORIES:
                defect_count += 1
                if tid is not None:
                    defect_ids.add(tid)

        current_count = len(detections)
        fps = self._get_fps(stream_info)
        frame_seconds = 1.0 / fps
        total_unique = self.get_total_counts().get("defect", 0)

        return {
            # ---- pipe-family parity fields ----
            "current_count": current_count,
            "total_unique_count": total_unique,
            "frame_new_ids": sorted(self._new_track_ids_this_frame.get("defect", set())),
            "is_active": current_count > 0,
            "frame_seconds": round(frame_seconds, 6),
            "max_continuous_seconds": round(self._max_active_streak * frame_seconds, 3),
            # ---- car-damage / QUALITY-doc parity fields ----
            # Defect-only model: total_inspected == defect_count and defect_rate
            # is pinned at 1.0. Carried for contract parity only; the manifest
            # publishes defect_presence as the real denominator instead.
            "defect_count": defect_count,
            "total_inspected": total_inspected,
            "defect_rate": (defect_count / total_inspected) if total_inspected > 0 else 0.0,
            "frame_defect_ids": sorted(defect_ids),
            "frame_inspected_ids": sorted(inspected_ids),
            # ---- session-cumulative reference values ----
            "active_frames": self._active_frames,
            "total_frames": self._total_frames,
            "presence_ratio": self._active_frames / max(1, self._total_frames),
        }

    # ============================================================
    # Tracking Stats
    # ============================================================

    def _generate_tracking_stats(self, detections, alerts, stream_info, config):
        camera_info = self.get_camera_info_from_stream(stream_info)

        # Cumulative UNIQUE defect track_ids, NOT the raw per-frame sum. One
        # bottle held across 40 frames must count once; _total_defects counts it
        # 40 times, which would inflate every "last"-agg total the bridge
        # resolves from total_counts.
        total_unique = self.get_total_counts().get("defect", 0)

        total_counts = [{"category": "defect", "count": total_unique}]
        current_counts = [{"category": "defect", "count": len(detections)}]
        current_new_counts = [
            {"category": cat, "count": len(ids)} for cat, ids in self._new_track_ids_this_frame.items()
        ]

        detection_objs = [
            self.create_detection_object("defect", d["bounding_box"], track_id=d.get("track_id")) for d in detections
        ]

        new_total = sum(c["count"] for c in current_new_counts)
        human_text = (
            f"Current defects: {len(detections)}, "
            f"New this frame: {new_total}, Total unique defective bottles: {total_unique}"
        )

        input_ts = self._get_current_timestamp_str(stream_info)
        reset_ts = self._get_start_timestamp_str(stream_info)

        # Same builder the incident uses, so alerts[] / alert_settings[] carry one
        # spelling of the threshold key across both payloads.
        alert_settings = self._build_alert_settings(config, alerts)

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

        stat["target_categories"] = self.target_categories
        # current_new_counts: track_ids seen for the first time this frame.
        stat["current_new_counts"] = current_new_counts
        # total_current_counts: alias of current_counts, kept because the bridge
        # reads it as an occupancy fallback (legacy_analytics_bridge line ~1197).
        stat["total_current_counts"] = current_counts
        # Side-channel QUALITY block for legacy_analytics_bridge (results-agg).
        stat["quality_analytics"] = self._compute_quality_analytics(detections, stream_info)

        return stat

    # ============================================================
    # Business Analytics
    # ============================================================

    def _generate_business_analytics(self, detections, alerts, stream_info):
        camera_info = self.get_camera_info_from_stream(stream_info)

        analytics_stats = {
            "total_frames": self._total_frames,
            "total_alerts_triggered": self._total_alerts_triggered,
            "active_frames": self._active_frames,
            "defect_presence_ratio": self._active_frames / max(1, self._total_frames),
            "current_detections": len(detections),
            "total_detections": self._total_defects,
            "unique_defect_tracks": self.get_total_counts().get("defect", 0),
        }

        return self.create_business_analytics(
            analysis_name="bottle_defect_analytics",
            statistics=analytics_stats,
            human_text=(
                f"Unique defective bottles: {analytics_stats['unique_defect_tracks']}, "
                f"defect presence ratio: {analytics_stats['defect_presence_ratio']:.2f}"
            ),
            camera_info=camera_info,
            alerts=alerts,
        )

    # ============================================================
    # Summary
    # ============================================================

    def _generate_summary(self, current_count, stream_info=None):
        current_ts = self._get_current_timestamp_str(stream_info)
        start_ts = self._get_start_timestamp_str(stream_info)

        lines = []
        lines.append(f"Application: {self.CASE_TYPE} v{self.CASE_VERSION}")
        lines.append(f"CURRENT FRAME @ {current_ts}:")
        lines.append(f"\t- Defects Detected: {current_count}")
        lines.append(f"TOTAL SINCE {start_ts}:")
        lines.append(f"\t- Unique Defective Bottles: {self.get_total_counts().get('defect', 0)}")
        lines.append(f"\t- Total Frames: {self._total_frames}")

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
                    return f"{parts[0]}:{parts[1]}:{parts[2]} {'-'.join(parts[3:])}"
        except Exception:
            pass

        return timestamp_clean

    def _get_current_timestamp_str(
        self,
        stream_info: Optional[Dict[str, Any]],
        precision=False,
        frame_id: Optional[str] = None,
    ) -> str:
        _ = (precision, frame_id)
        if not stream_info:
            return "00:00:00.00"

        input_settings = stream_info.get("input_settings", {}) or {}
        if input_settings.get("start_frame", "na") != "na":
            return self._format_timestamp(input_settings.get("stream_time", "NA"))

        stream_time_str = (input_settings.get("stream_info", {}) or {}).get("stream_time", "")
        if stream_time_str:
            try:
                dt = datetime.strptime(stream_time_str.replace(" UTC", ""), "%Y-%m-%d-%H:%M:%S.%f")
                return self._format_timestamp_for_stream(dt.replace(tzinfo=timezone.utc).timestamp())
            except Exception:
                return self._format_timestamp_for_stream(time.time())
        return self._format_timestamp_for_stream(time.time())

    def _get_start_timestamp_str(self, stream_info: Optional[Dict[str, Any]], precision=False) -> str:
        _ = (precision,)
        if not stream_info:
            return "00:00:00"

        input_settings = stream_info.get("input_settings", {}) or {}

        if self.start_timer is None or input_settings.get("start_frame", "na") == 1:
            candidate = input_settings.get("stream_time")
            if not candidate or candidate == "NA":
                candidate = datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")
            self.start_timer = candidate

        if self.start_timer is not None and self.start_timer != "NA":
            return self._format_timestamp(self.start_timer)

        if self._tracking_start_time is None:
            self._tracking_start_time = time.time()
        dt = datetime.fromtimestamp(self._tracking_start_time, tz=timezone.utc)
        return dt.replace(minute=0, second=0, microsecond=0).strftime("%Y:%m:%d %H:%M:%S")
