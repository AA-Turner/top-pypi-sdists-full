"""
Pipe Corrosion Detection Use Case

Canonical Matrice-compliant industrial pipe corrosion detection.
Includes:
- Confidence filtering
- Category filtering (ignores "mask")
- Spatial merging (containment-only: merge solely when one box is fully inside another)
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
from ..Trackers import ConfigDrivenTracker, TrackerProfile  # noqa: E402
from ..utils import (
    apply_category_mapping,
    filter_by_categories,
    filter_by_confidence,
    match_results_structure,
)
from ..utils.incident_manager_utils import INCIDENT_MANAGER, IncidentManagerFactory

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

        # Target detection class
        self.target_categories = ["corrosion"]

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

        # Lifecycle transition flags (set per frame by _update_temporal_state)
        self._just_activated = False
        self._just_closed = False
        self._closing_alert_id = None
        self._closing_start_frame = None

        # -----------------------------
        # Analytics Counters
        # -----------------------------
        self._total_frames = 0
        self._total_detections = 0
        self._active_frames = 0
        # Longest unbroken run of corrosion-present frames this session, in
        # frames — converted to seconds for max_continuous_corrosion_seconds.
        self._max_active_streak = 0

        # Tracking State (AdvancedTracker)
        self.tracker = None
        self._tracker_seam = ConfigDrivenTracker()
        self._per_category_total_track_ids = {cat: set() for cat in self.target_categories}
        self._current_frame_track_ids = {cat: set() for cat in self.target_categories}
        self._new_track_ids_this_frame = {cat: set() for cat in self.target_categories}

        self.start_timer = None
        self._tracking_start_time: Optional[float] = None

        # -----------------------------
        # Incident Manager wiring (same pattern as loitering_detection)
        # -----------------------------
        self._incident_manager_factory: Optional[IncidentManagerFactory] = None
        self._incident_manager: Optional[INCIDENT_MANAGER] = None
        self._incident_manager_initialized: bool = False
        # Cameras for which count-based severity thresholds were already registered.
        self._thresholds_registered: set = set()
        # Current-frame detection count, used to derive count-based severity in
        # _generate_incidents (set each frame by _process_frame).
        self._current_count: int = 0

    def reset_state(self):
        self.__init__()

    # ============================================================
    # Incident Manager (same wiring as loitering_detection)
    # ============================================================

    @staticmethod
    def _severity_for_count(count: int) -> str:
        """Count-based incident severity: 1-2 -> 'high', >=3 -> 'critical'."""
        return "critical" if int(count) >= 3 else "high"

    def _initialize_incident_manager_once(self, config: ConfigProtocol) -> None:
        """Initialize the incident manager ONCE (on first process() invocation)."""
        if self._incident_manager_initialized:
            return
        try:
            logger.info("[INCIDENT_MANAGER] Initializing for pipe corrosion detection...")
            if self._incident_manager_factory is None:
                self._incident_manager_factory = IncidentManagerFactory(logger=logger)
            self._incident_manager = self._incident_manager_factory.initialize(config)
            if self._incident_manager:
                logger.info("[INCIDENT_MANAGER] Initialized for pipe corrosion detection")
            else:
                logger.warning("[INCIDENT_MANAGER] Not available; incidents won't be published")
        except Exception as e:  # pragma: no cover - defensive
            logger.error("[INCIDENT_MANAGER] Initialization failed: %s", e, exc_info=True)
        finally:
            self._incident_manager_initialized = True

    @staticmethod
    def _resolve_camera_id(stream_info: Optional[Dict[str, Any]]) -> str:
        """Resolve camera_id from stream_info (camera_info -> top-level -> topic)."""
        camera_id = ""
        if stream_info:
            camera_info = stream_info.get("camera_info", {}) or {}
            camera_id = camera_info.get("camera_id", "") or camera_info.get("cameraId", "")
            if not camera_id:
                camera_id = stream_info.get("camera_id", "") or stream_info.get("cameraId", "")
            if not camera_id:
                topic = stream_info.get("topic", "")
                if topic:
                    for suffix in ("_input_topic", "_input-topic"):
                        if suffix in topic:
                            camera_id = topic.split(suffix)[0]
                            break
        return camera_id or "default_camera"

    def _register_incident_thresholds(self, camera_id: str) -> None:
        """Register count-based severity thresholds for a camera (1-2 high, >=3 critical).

        Registered once per camera. Backend config polling (if any) overrides these.
        """
        if camera_id in self._thresholds_registered:
            return
        self._thresholds_registered.add(camera_id)
        if not self._incident_manager:
            return
        try:
            self._incident_manager.set_thresholds_for_camera(
                camera_id=camera_id,
                thresholds=[
                    {"level": "high", "percentage": 1},
                    {"level": "critical", "percentage": 3},
                ],
                incident_type=self.name,
            )
        except Exception as e:  # pragma: no cover - defensive
            logger.warning("[INCIDENT_MANAGER] threshold registration failed: %s", e)

    def _send_incident_to_manager(
        self,
        incident: Dict[str, Any],
        stream_info: Optional[Dict[str, Any]],
        context: Optional[ProcessingContext] = None,
    ) -> None:
        """Send this frame's incident (or {} when idle) to the incident manager.

        ``incident or {}`` is passed on EVERY frame — including idle ones — so the
        manager can count empty frames and publish the close event
        (``severity_level: "info"`` + ``end_time``).

        Sets ``context.metadata["incident_published_via_manager"]`` so
        ``post_processor._publish_legacy_frame_analytics`` skips the
        legacy-bridge ``incident_res`` fallback. Without this flag the bridge
        profile (``publish_incidents=True``) republishes the same incident under
        a different ``incident_id``, producing a double open that never closes.
        """
        if context is not None:
            context.metadata["incident_published_via_manager"] = bool(self._incident_manager)
        if not self._incident_manager:
            return
        camera_id = self._resolve_camera_id(stream_info)
        self._register_incident_thresholds(camera_id)
        try:
            self._incident_manager.process_incident(
                camera_id=camera_id, incident_data=incident or {}, stream_info=stream_info
            )
        except Exception as e:  # pragma: no cover - defensive
            logger.error("[INCIDENT_MANAGER] Error sending incident: %s", e, exc_info=True)

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

        # Initialize the incident manager once (after config validation).
        self._initialize_incident_manager_once(config)

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

            # Publish this frame's incident status to the incident manager for
            # level tracking / publishing (empty {} is tracked for close).
            self._send_incident_to_manager(incidents, stream_info, context=context)

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

        # Step 5 — Tracker: attach stable track_ids (drives current_new_counts)
        detections = self._apply_tracker(detections)
        self._update_tracking_state(detections)

        current_count = len(detections)
        # Expose to _generate_incidents for count-based severity.
        self._current_count = current_count

        # Update analytics
        self._total_frames += 1
        self._total_detections += current_count

        if current_count > 0:
            self._active_frames += 1

        # Update temporal validation state
        self._update_temporal_state(current_count, config)

        # Longest unbroken run of corrosion-present frames seen this session.
        # _update_temporal_state has just set _active_counter to the length of the
        # current run (0 on an idle frame), so tracking its max here gives
        # max_continuous_corrosion_seconds without a second counter.
        self._max_active_streak = max(self._max_active_streak, self._active_counter)

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

        # The closing incident (emitted on the deactivation frame) needed the
        # original start timestamp, so reset the timers only after generation.
        if self._just_closed:
            self.start_timer = None
            self._tracking_start_time = None

        return incidents, tracking_stats, business_analytics, alerts, summary

    # ============================================================
    # Tracking (AdvancedTracker) + current_new_counts support
    # ============================================================

    def _apply_tracker(self, detections: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Attach stable track_ids via AdvancedTracker; pass through on failure."""
        try:
            if self.tracker is None:
                self.tracker = self._tracker_seam.get_shared_tracker(profile=TrackerProfile.DEFAULT)
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
        return {cat: len(ids) for cat, ids in self._per_category_total_track_ids.items()}

    # ============================================================
    # Spatial Merge Logic
    # ============================================================

    def _merge_detections(self, detections, config):
        """
        Containment-only merge: two boxes merge ONLY when one is fully inside
        the other. Partial overlaps (any IoU) and partial containment do NOT
        merge, so distinct corrosion regions remain separate.
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

    def _should_merge(self, b1, b2, _config):
        # Merge ONLY when one box is geometrically, fully contained inside the
        # other. No IoU or partial-containment merging: overlapping-but-not-
        # contained corrosion regions stay distinct.
        _ = (_config,)
        return self._is_fully_inside(b1, b2)

    def _is_fully_inside(self, b1, b2):
        """True if b1 is entirely within b2, or b2 entirely within b1."""
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
    # Temporal State Update
    # ============================================================

    def _update_temporal_state(self, current_count, config):
        # Reset per-frame transition flags.
        self._just_activated = False
        self._just_closed = False

        if current_count > 0:
            self._active_counter += 1
            self._inactive_counter = 0

            if not self._alert_active and self._active_counter >= config.activation_frames:
                self._alert_active = True
                self._total_alerts_triggered += 1
                # Generate globally unique alert ID
                self._alert_id = f"corrosion_{uuid.uuid4().hex[:8]}"

                self._alert_start_frame = self._total_frames
                self._just_activated = True

        else:
            self._inactive_counter += 1
            self._active_counter = 0

            if self._alert_active and self._inactive_counter >= config.deactivation_frames:
                # Capture identity before clearing so the closing incident (this
                # frame) can reference it. Timer reset is deferred to the caller.
                self._just_closed = True
                self._closing_alert_id = self._alert_id
                self._closing_start_frame = self._alert_start_frame
                self._alert_active = False
                self._alert_id = None
                self._alert_start_frame = None

    # ============================================================
    # Alert, Incident, Analytics, Summary
    # ============================================================

    def _generate_alerts(self, config, _stream_info):
        _ = (_stream_info,)
        # One-time emission: alert fires only on the frame the incident opens.
        if not self._just_activated or not config.alert_config:
            return []

        alert_types = getattr(config.alert_config, "alert_type", ["Default"]) or ["Default"]
        alert_values = getattr(config.alert_config, "alert_value", ["JSON"]) or ["JSON"]

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
        alert["duration_frames"] = 0
        alert["emit"] = True
        self._last_alert_time = time.time()

        return [alert]

    def _generate_incidents(self, alerts, stream_info, config):
        # Incidents are persistent: emitted every frame while active, plus one
        # final closing frame carrying the real end timestamp.
        if not self._alert_active and not self._just_closed:
            return {}

        camera_info = self.get_camera_info_from_stream(stream_info)
        incident_id = self._alert_id if self._alert_active else self._closing_alert_id

        current_timestamp = self._get_current_timestamp_str(stream_info)
        start_timestamp = self._get_start_timestamp_str(stream_info)

        # Count-based severity: 1-2 corrosion detections -> high, >=3 -> critical.
        count = int(getattr(self, "_current_count", 0))
        severity = self._severity_for_count(count)

        incident = self.create_incident(
            incident_id=incident_id,
            incident_type=self.name,
            severity_level=severity,
            human_text=f"Pipe corrosion confirmed and alert active (detections={count}, severity={severity})",
            camera_info=camera_info,
            alerts=alerts,
            alert_settings=self._build_alert_settings(config, alerts),
            start_time=start_timestamp,
            end_time=current_timestamp,  # placeholder; overridden below
            level_settings={"high": 1, "critical": 3},
        )

        # incident_quant (detection count) lets the incident manager map severity
        # via its thresholds (1 -> high, 3 -> critical).
        incident["incident_quant"] = float(count)

        if self._alert_active:
            # Active incidents have an empty end_time (set explicitly because
            # create_incident coerces falsy end_time back to start_time).
            incident["end_time"] = ""
        else:
            incident["end_time"] = current_timestamp
            incident["human_text"] = "Pipe corrosion incident closed"

        return incident

    def _build_alert_settings(self, config, alerts: List) -> List[Dict[str, Any]]:
        """Canonical ``alert_settings`` entries.

        Mirrors solar_panel / intrusion_detection / hazard_zone_entry: prefer the
        real alert objects when present (so published settings match what actually
        fired), else fall back to the deployment AlertConfig.

        Uses ``threshold_value`` — the key ``BaseProcessor.create_alert_object``
        emits — and mirrors its SCALAR value. Renaming the key alone was not
        enough: this app previously published ``{"corrosion": N}`` under the same
        name that alerts[] uses for a plain ``N``, so a consumer reading one key
        across both payloads got a dict in one place and an int in the other.
        """
        if alerts:
            return [
                {
                    "alert_type": a.get("alert_type"),
                    "incident_category": self.CASE_TYPE,
                    "threshold_value": a.get("threshold_value"),
                    "ascending": a.get("ascending", True),
                    "settings": a.get("settings", {}),
                }
                for a in alerts
                if isinstance(a, dict)
            ]
        ac = config.alert_config
        if ac and hasattr(ac, "alert_type"):
            alert_types = getattr(ac, "alert_type", ["Default"]) or ["Default"]
            alert_values = getattr(ac, "alert_value", ["JSON"]) or ["JSON"]
            return [
                {
                    "alert_type": alert_types,
                    "incident_category": self.CASE_TYPE,
                    # activation_frames is this family's threshold (consecutive
                    # frames required to confirm), not AlertConfig.count_thresholds
                    # — the pipe apps never populate count_thresholds.
                    "threshold_value": config.activation_frames,
                    "ascending": True,
                    "settings": {t: v for t, v in zip(alert_types, alert_values)},
                }
            ]
        return []

    # ============================================================
    # QUALITY analytics block (results-agg via legacy_analytics_bridge)
    # ============================================================

    @staticmethod
    def _get_fps(stream_info: Optional[Dict[str, Any]]) -> float:
        """Stream FPS for frame→seconds conversion; 30.0 when unavailable."""
        if stream_info:
            try:
                fps = (stream_info.get("input_settings", {}) or {}).get("original_fps")
                if fps and float(fps) > 1e-6:
                    return float(fps)
            except (TypeError, ValueError, AttributeError):
                pass
        return 30.0

    def _compute_corrosion_analytics(
        self, detections: List[Dict[str, Any]], stream_info: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Per-frame QUALITY block consumed by ``_ingest_pipe_corrosion_quality``.

        Stored at ``tracking_stats["corrosion_analytics"]`` every frame. The bridge
        derives the published 60s-window metrics from these fields:

          current_corrosion_count → current_count            (agg last)
          new_corrosion_count     → union of frame_new_ids    (agg sum)
          total_corrosion_count   → total_unique_count        (agg last)
          peak_corrosion_count    → max of current_count      (agg max)
          corrosion_presence      → active frames / frames in window * 100 (agg avg)

        ``frame_new_ids`` (not a raw count) is what makes new_corrosion_count
        deduplicated: a region persisting across the window contributes its
        track_id on one frame only, so the union counts it once.

        ``frame_seconds`` / ``max_continuous_seconds`` are emitted even though the
        current corrosion metric set does not publish them — they let a duration
        metric be added in the manifest without touching this use case, and they
        match the gas/liquid blocks so the three apps stay interchangeable.
        """
        current_count = len(detections)
        fps = self._get_fps(stream_info)
        frame_seconds = 1.0 / fps

        return {
            "current_count": current_count,
            "total_unique_count": self.get_total_counts().get("corrosion", 0),
            "frame_new_ids": sorted(self._new_track_ids_this_frame.get("corrosion", set())),
            "is_active": current_count > 0,
            "frame_seconds": round(frame_seconds, 6),
            "max_continuous_seconds": round(self._max_active_streak * frame_seconds, 3),
            # Session-cumulative reference values (parity with business_analytics).
            "active_frames": self._active_frames,
            "total_frames": self._total_frames,
            "presence_ratio": self._active_frames / max(1, self._total_frames),
        }

    def _generate_tracking_stats(self, detections, alerts, stream_info, config):
        camera_info = self.get_camera_info_from_stream(stream_info)

        # Cumulative UNIQUE corrosion regions (track_id set), NOT the raw
        # per-frame detection sum. A single patch that persists across the clip
        # must count once — _total_detections counts it once per frame (observed
        # 106 vs 4 real regions on assets/frames/.../pipe-corrosion-10), which
        # would inflate every "last"-agg total metric the bridge resolves from
        # total_counts, and break the window-delta used for new_corrosion_count.
        total_unique = self.get_total_counts().get("corrosion", 0)
        total_counts = [{"category": "corrosion", "count": total_unique}]
        current_counts = [{"category": "corrosion", "count": len(detections)}]
        current_new_counts = [
            {"category": cat, "count": len(ids)} for cat, ids in self._new_track_ids_this_frame.items()
        ]

        detection_objs = []
        for d in detections:
            obj = self.create_detection_object("corrosion", d["bounding_box"], track_id=d.get("track_id"))
            detection_objs.append(obj)

        new_total = sum(c["count"] for c in current_new_counts)
        human_text = (
            f"Current corrosion detections: {len(detections)}, "
            f"New this frame: {new_total}, Total unique regions: {total_unique}"
        )

        input_ts = self._get_current_timestamp_str(stream_info)
        reset_ts = self._get_start_timestamp_str(stream_info)

        # Alert settings — same canonical builder the incident payload uses, so
        # tracking_stats and incidents can never drift in key name or value type.
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

        stat["current_new_counts"] = current_new_counts
        # Side-channel QUALITY block for legacy_analytics_bridge (results-agg).
        # Emitted every frame — the bridge needs idle frames too, or
        # corrosion_presence would read 100% whenever corrosion is intermittent.
        stat["corrosion_analytics"] = self._compute_corrosion_analytics(detections, stream_info)

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
