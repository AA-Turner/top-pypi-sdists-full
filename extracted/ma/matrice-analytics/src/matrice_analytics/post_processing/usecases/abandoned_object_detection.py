"""
Abandoned Object Detection Use Case
=====================================


Key design decisions:
- Time-based thresholds (seconds) not frame-based — works across any FPS camera
- Velocity-based stationary check with sliding window (robust to brief jitter)
- Per-track state machine with track timeout cleanup
- No person proximity check (V3 model has no person class — can be added later)
- Alert cooldown per track to avoid spam

Classes:
    - baby_stroller (0), wheelchair (1), shopping_cart (2), umbrella (3),
      helmet (4), bicycle (5), laptop (6), vehicle (7),
      carry_bag (8), scooter (9), cardboard_box (10)

Author: Dhiyanesh G
"""

from __future__ import annotations

import os
import time
from collections import deque
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Tuple

import numpy as np

from ..core.base import (
    BaseProcessor,
    ConfigProtocol,
    ProcessingContext,
    ProcessingResult,
)
from ..core.config import AlertConfig, BaseConfig
from ..Trackers import ConfigDrivenTracker, TrackerProfile, legacy_sort_tracker_overrides
from ..utils import (
    BBoxSmoothingConfig,
    BBoxSmoothingTracker,
    ByteTrackWrapper,
    SORTTracker,
    apply_category_mapping,
    bbox_centroid,
    bbox_iou,
    bbox_smoothing,
    dist,
    filter_by_confidence,
    match_results_structure,
    smooth_point,
)
from ..utils.incident_manager_utils import INCIDENT_MANAGER, IncidentManagerFactory

_DEFAULT_CAMERA_ID = "camera"

# Synthetic class index for a confirmed-abandoned object. Never produced by the
# model itself (which only ever outputs 0-10) -- assigned here in post-processing
# once a track crosses the abandonment threshold, so that any downstream consumer
# rendering a label off class_id (via index_to_category) rather than the
# `category` string sees "abandoned_object" too, not the original object class.
ABANDONED_CLASS_ID = 11


def _resolve_manager_camera_id(stream_info: Dict[str, Any] | None) -> str:
    """Resolve the camera key used by IncidentManager state tracking.

    Uses the real camera id from ``stream_info`` (never a hardcoded value) so
    per-camera incident lifecycle stays correct in multi-camera deployments.
    """
    if not stream_info:
        return _DEFAULT_CAMERA_ID
    inp = stream_info.get("input_settings")
    if not isinstance(inp, dict):
        inp = {}
    camera_info = stream_info.get("camera_info")
    if not isinstance(camera_info, dict):
        camera_info = {}
    camera_id = (
        stream_info.get("camera_id")
        or inp.get("camera_id")
        or camera_info.get("camera_id")
        or stream_info.get("stream_key")
    )
    return str(camera_id) if camera_id else _DEFAULT_CAMERA_ID


# =============================================================================
# Config
# =============================================================================


@dataclass
class AbandonedObjectConfig(BaseConfig):
    """Configuration for abandoned object detection."""

    # Detection
    confidence_threshold: float = 0.30
    target_categories: List[str] = field(
        default_factory=lambda: [
            "baby_stroller",
            "wheelchair",
            "shopping_cart",
            "umbrella",
            "helmet",
            "bicycle",
            "laptop",
            "vehicle",
            "carry_bag",
            "scooter",
            "cardboard_box",
        ]
    )
    index_to_category: Dict[int, str] | None = field(
        default_factory=lambda: {
            0: "baby_stroller",
            1: "wheelchair",
            2: "shopping_cart",
            3: "umbrella",
            4: "helmet",
            5: "bicycle",
            6: "laptop",
            7: "vehicle",
            8: "carry_bag",
            9: "scooter",
            10: "cardboard_box",
            ABANDONED_CLASS_ID: "abandoned_object",
        }
    )

    # Abandonment thresholds
    abandonment_threshold_seconds: float = 30.0  # object must be stationary for this long
    min_presence_seconds: float = 2.0  # warmup — ignore objects seen for < 2s
    velocity_threshold_px_per_sec: float = 15.0  # below this = stationary
    stationary_ratio_threshold: float = 0.75  # 75% of window must be stationary
    behavior_window_seconds: float = 8.0  # sliding window size in seconds
    min_behavior_window_seconds: float = 3.0  # min window before making decision

    # Detection confirmation — a track must be continuously present for this
    # long before it's treated as a real detection (bbox shown, abandonment
    # timer started). Filters out single-/few-frame flicker false positives.
    # Lower for short benchmark clips; production should keep this at 5s.
    track_confirmation_seconds: float = 5.0

    # Oversized-bbox rejection — width/height beyond this many px is almost
    # always a false detection (e.g. a misclassified background region), so
    # it's dropped before tracking rather than fed into the state machine.
    max_bbox_dimension_px: float = 250.0

    # Track management
    track_timeout_seconds: float = 15.0  # drop track if missing for this long
    max_centroid_jump_px: float = 60.0  # clamp sudden bbox jumps
    centroid_ema_alpha: float = 0.25  # EMA smoothing for centroid
    speed_window_size: int = 15
    slow_flags_window_size: int = 15

    # ID healing (re-associates tracks after brief occlusion)
    id_heal_iou_threshold: float = 0.30
    id_heal_feet_distance_px: float = 60.0

    # Alerts
    alert_cooldown_seconds: float = 30.0  # re-alert interval per track
    alert_config: AlertConfig | None = None

    # Smoothing
    enable_smoothing: bool = True
    smoothing_algorithm: str = "observability"
    smoothing_window_size: int = 20
    smoothing_cooldown_frames: int = 5
    smoothing_confidence_range_factor: float = 0.5

    # Tracking
    enable_tracking: bool = True
    tracking_method: str = "sort"
    tracking_max_age: int = 30
    tracking_min_hits: int = 2
    tracking_iou_threshold: float = 0.25

    def validate(self) -> List[str]:
        errors: List[str] = super().validate()
        if self.abandonment_threshold_seconds < 0:
            errors.append("abandonment_threshold_seconds must be non-negative")
        if self.velocity_threshold_px_per_sec < 0:
            errors.append("velocity_threshold_px_per_sec must be non-negative")
        if not 0.0 <= self.stationary_ratio_threshold <= 1.0:
            errors.append("stationary_ratio_threshold must be between 0 and 1")
        if self.speed_window_size < 3:
            errors.append("speed_window_size must be >= 3")
        if self.track_confirmation_seconds < 0:
            errors.append("track_confirmation_seconds must be non-negative")
        if self.max_bbox_dimension_px <= 0:
            errors.append("max_bbox_dimension_px must be positive")
        if self.alert_config:
            errors.extend(self.alert_config.validate())
        return errors


# =============================================================================
# Use Case
# =============================================================================


class AbandonedObjectDetectionUseCase(BaseProcessor):
    """
    Detects abandoned objects using a velocity-based stationary state machine.

    Flow per frame:
        1. Filter by confidence
        2. Apply category mapping (index -> name)
        3. Smooth bboxes (optional)
        4. Track objects (SORT / ByteTrack)
        5. Update per-track abandonment state machine
        6. Enrich detections with is_abandoned flag
        7. Generate alerts (cooldown-enforced per track)
        8. Return agg_summary
    """

    GLOBAL_ZONE_NAME = "global"

    def __init__(self):
        super().__init__("abandoned_object_detection")
        self.category = "security"
        self.CASE_TYPE = "abandoned_object_detection"
        self.CASE_VERSION = "1.0"

        self.target_categories: List[str] = []
        self.smoothing_tracker: BBoxSmoothingTracker | None = None
        self.tracker: Any | None = None

        self._total_frame_counter: int = 0
        self._abandoned_tracks: Dict[int, Dict[str, Any]] = {}
        self._per_category_total_track_ids: Dict[str, set] = {}
        self._current_frame_track_ids: Dict[str, set] = {}
        self._new_track_ids_this_frame: Dict[str, set] = {}
        self.start_timer = None
        self._tracking_start_time = None

        # Incident manager — registers this usecase with the platform's
        # Incident/Volume Analytics discovery (see _send_incident_to_manager).
        self._incident_manager_factory: IncidentManagerFactory | None = None
        self._incident_manager: INCIDENT_MANAGER | None = None
        self._incident_manager_initialized: bool = False
        self._abandon_incident_id: str = self.CASE_TYPE
        self._abandon_incident_active: bool = False
        self._abandon_incident_start_ts: str | None = None
        self._abandon_last_incident: Dict[str, Any] | None = None

    # =========================================================================
    # Helpers
    # =========================================================================

    @staticmethod
    def _parse_track_id(tid: Any) -> int | None:
        if tid is None:
            return None
        try:
            return int(tid)
        except (TypeError, ValueError):
            return None

    def _init_track_state(
        self,
        bbox: Dict[str, Any],
        centroid: Tuple[float, float],
        config: AbandonedObjectConfig,
    ) -> Dict[str, Any]:
        win = max(3, int(config.speed_window_size))
        return {
            "presence_seconds": 0.0,
            "missing_for_seconds": 0.0,
            "last_bbox": bbox,
            "last_centroid": centroid,
            "smoothed_centroid": centroid,
            "speed_window": deque(maxlen=win),
            "slow_flags_window": deque(maxlen=max(3, int(config.slow_flags_window_size))),
            "last_inst_speed": 0.0,
            "is_abandoned": False,
            "last_alert_video_time": None,
            "confirmed": False,
            "abandonment_timer_seconds": 0.0,
        }

    def _is_stationary(
        self,
        inst_speed: float,
        config: AbandonedObjectConfig,
    ) -> bool:
        return inst_speed <= float(config.velocity_threshold_px_per_sec)

    @staticmethod
    def _filter_oversized_bboxes(
        detections: List[Dict[str, Any]],
        config: AbandonedObjectConfig,
    ) -> List[Dict[str, Any]]:
        """Drop detections whose bbox width or height exceeds max_bbox_dimension_px.

        Oversized boxes are almost always a misclassified background region
        rather than a real object, so they're rejected before tracking to
        avoid polluting track states / ID-healing candidates.
        """
        max_dim = float(config.max_bbox_dimension_px)
        kept: List[Dict[str, Any]] = []
        for det in detections:
            bbox = det.get("bounding_box") or det.get("bbox")
            if not isinstance(bbox, dict):
                kept.append(det)
                continue
            width = float(bbox.get("x2", 0.0)) - float(bbox.get("x1", 0.0))
            height = float(bbox.get("y2", 0.0)) - float(bbox.get("y1", 0.0))
            if width > max_dim or height > max_dim:
                continue
            kept.append(det)
        return kept

    # =========================================================================
    # Tracker init
    # =========================================================================

    def _init_tracker(
        self,
        config: AbandonedObjectConfig,
        stream_info: Dict[str, Any] | None,
    ) -> None:
        if self.tracker is not None:
            return

        method = str(getattr(config, "tracking_method", "sort")).lower().strip()

        # F10b S9 (consolidation-plan.md Step 9): route the legacy SORT/ByteTrack
        # default onto the AdvancedTracker seam. MATRICE_LEGACY_SORT=1 keeps the
        # pre-migration path alive for one release (kill-switch, plan §7).
        if method in ("sort", "bytetrack") and os.environ.get("MATRICE_LEGACY_SORT") != "1":
            self.tracker = ConfigDrivenTracker().get_shared_tracker(
                profile=TrackerProfile.DEFAULT,
                **legacy_sort_tracker_overrides(config, method),
            )
            return

        if method == "sort":
            self.tracker = SORTTracker(
                iou_threshold=float(getattr(config, "tracking_iou_threshold", 0.25)),
                max_age=int(getattr(config, "tracking_max_age", 30)),
                min_hits=int(getattr(config, "tracking_min_hits", 2)),
            )
            return

        if method == "bytetrack":
            fps = 30.0
            try:
                if stream_info:
                    fps_val = stream_info.get("input_settings", {}).get("original_fps")
                    if fps_val and float(fps_val) > 1e-6:
                        fps = float(fps_val)
            except Exception:
                fps = 30.0
            self.tracker = ByteTrackWrapper(
                fps=float(fps),
                track_thresh=float(getattr(config, "bytetrack_track_thresh", 0.25)),
                match_thresh=float(getattr(config, "bytetrack_match_thresh", 0.80)),
                track_buffer=int(getattr(config, "tracking_max_age", 30)),
            )
            return

        self.tracker = None

    # =========================================================================
    # State machine
    # =========================================================================

    def _update_abandoned_states(
        self,
        detections: List[Dict[str, Any]],
        config: AbandonedObjectConfig,
        dt_video: float,
        video_time_seconds: float,
    ) -> None:
        """
        Core state machine — updates per-track abandonment state.

        For each tracked object:
          - Accumulate presence time using dt_video (fps-aware, not frame-based)
          - Smooth centroid with EMA to reduce jitter
          - Clamp large centroid jumps
          - Compute instantaneous speed (px/sec)
          - Push into sliding window
          - Decide abandoned if:
              presence >= abandonment_threshold_seconds
              AND slow_ratio >= stationary_ratio_threshold
              AND avg_speed <= velocity_threshold_px_per_sec
          - Expire tracks missing > track_timeout_seconds
        """
        present_ids: set = set()

        def _get_bbox(det: Dict[str, Any]) -> Dict[str, float] | None:
            bbox = det.get("bounding_box") or det.get("bbox")
            return bbox if isinstance(bbox, dict) else None

        def _try_heal_track_id(
            new_tid: int,
            new_bbox: Dict[str, float],
            new_centroid: Tuple[float, float],
        ) -> int | None:
            """Merge a recently-missing track into new_tid if bbox/centroid match."""
            best_old_tid: int | None = None
            best_score: float = -1.0
            max_missing = float(config.track_timeout_seconds)
            iou_thr = float(config.id_heal_iou_threshold)
            dist_thr = float(config.id_heal_feet_distance_px)

            for old_tid, st in self._abandoned_tracks.items():
                if old_tid == new_tid:
                    continue
                missing_for = float(st.get("missing_for_seconds", 0.0))
                if missing_for <= 0.0 or missing_for > max_missing:
                    continue
                old_bbox = st.get("last_bbox")
                if not isinstance(old_bbox, dict):
                    continue
                iou = float(bbox_iou(old_bbox, new_bbox))
                if iou >= iou_thr:
                    score = iou
                else:
                    old_centroid = st.get("smoothed_centroid") or st.get("last_centroid")
                    if not old_centroid:
                        continue
                    d = float(dist(old_centroid, new_centroid))
                    if d <= dist_thr:
                        score = 1.0 - min(1.0, d / max(1.0, dist_thr))
                    else:
                        continue
                if score > best_score:
                    best_score = score
                    best_old_tid = old_tid

            if best_old_tid is None:
                return None

            old_state = self._abandoned_tracks.get(best_old_tid)
            if not old_state:
                return None

            self._abandoned_tracks[new_tid] = old_state
            self._abandoned_tracks.pop(best_old_tid, None)
            self.logger.info(
                f"[ABANDON-ID-HEAL] merged old_tid={best_old_tid} -> new_tid={new_tid} score={best_score:.2f}"
            )
            return best_old_tid

        # ------------------------------------------------------------------
        # Per-detection update
        # ------------------------------------------------------------------
        for det in detections:
            if det.get("category") not in self.target_categories:
                continue

            tid = det.get("track_id")
            tid_int = self._parse_track_id(tid)
            if tid_int is None or tid_int < 0:
                continue

            bbox = _get_bbox(det)
            if not bbox:
                continue

            centroid = bbox_centroid(bbox)

            # Attempt ID healing for new track_ids
            if tid_int not in self._abandoned_tracks and self._abandoned_tracks:
                _try_heal_track_id(tid_int, bbox, centroid)

            present_ids.add(tid_int)

            # Initialize new track
            if tid_int not in self._abandoned_tracks:
                self._abandoned_tracks[tid_int] = self._init_track_state(bbox, centroid, config)
                continue

            st = self._abandoned_tracks[tid_int]

            # Accumulate presence in video-time seconds (fps-aware)
            st["presence_seconds"] = float(st.get("presence_seconds", 0.0) + dt_video)
            st["missing_for_seconds"] = 0.0

            # EMA smoothing on centroid
            prev_centroid = st.get("smoothed_centroid", centroid)
            alpha = float(config.centroid_ema_alpha)
            new_centroid = smooth_point(prev_centroid, centroid, alpha)

            # Clamp sudden jumps
            max_jump = float(config.max_centroid_jump_px)
            if dist(prev_centroid, new_centroid) > max_jump:
                dx = new_centroid[0] - prev_centroid[0]
                dy = new_centroid[1] - prev_centroid[1]
                norm = max(1e-6, (dx * dx + dy * dy) ** 0.5)
                scale = max_jump / norm
                new_centroid = (
                    prev_centroid[0] + dx * scale,
                    prev_centroid[1] + dy * scale,
                )

            # Instantaneous speed (px/sec)
            dt_safe = max(1e-6, dt_video)
            inst_speed = dist(new_centroid, prev_centroid) / dt_safe
            st["last_inst_speed"] = float(inst_speed)

            # Push into sliding windows
            stationary = self._is_stationary(inst_speed, config)
            st["speed_window"].append(float(inst_speed))
            st["slow_flags_window"].append(1.0 if stationary else 0.0)

            # Update anchors
            st["last_bbox"] = bbox
            st["last_centroid"] = centroid
            st["smoothed_centroid"] = new_centroid

            presence = float(st.get("presence_seconds", 0.0))

            # Confirmation gate — a track isn't treated as a real detection
            # until it's been continuously present for track_confirmation_seconds.
            # Before that: no bbox is shown (see _process_frame) and the
            # abandonment timer hasn't started yet.
            if not st.get("confirmed", False):
                if presence >= float(config.track_confirmation_seconds):
                    st["confirmed"] = True
                else:
                    st["is_abandoned"] = False
                    self._abandoned_tracks[tid_int] = st
                    continue

            # Abandonment timer starts counting from the moment of confirmation,
            # not from the track's raw first appearance.
            st["abandonment_timer_seconds"] = float(st.get("abandonment_timer_seconds", 0.0) + dt_video)
            timer = float(st["abandonment_timer_seconds"])

            # Warmup — no decision before min_presence_seconds (post-confirmation)
            if timer < float(config.min_presence_seconds):
                st["is_abandoned"] = False
                self._abandoned_tracks[tid_int] = st
                continue

            # Need enough window data before deciding
            enough_window = (
                len(st["speed_window"]) >= 3
                and len(st["slow_flags_window"]) >= 3
                and min(timer, float(config.behavior_window_seconds)) >= float(config.min_behavior_window_seconds)
            )

            win_avg_speed = float(np.mean(list(st["speed_window"]))) if st["speed_window"] else 0.0
            win_slow_ratio = float(np.mean(list(st["slow_flags_window"]))) if st["slow_flags_window"] else 0.0

            is_abandoned = False
            if enough_window:
                is_abandoned = (
                    timer >= float(config.abandonment_threshold_seconds)
                    and win_slow_ratio >= float(config.stationary_ratio_threshold)
                    and win_avg_speed <= float(config.velocity_threshold_px_per_sec)
                )

            if timer >= float(config.abandonment_threshold_seconds) and (self._total_frame_counter % 50 == 0):
                self.logger.info(
                    f"[ABANDON-DEBUG] tid={tid_int} timer={timer:.2f}s "
                    f"avg_speed={win_avg_speed:.2f} slow_ratio={win_slow_ratio:.2f} abandoned={is_abandoned}"
                )

            st["is_abandoned"] = bool(is_abandoned)
            self._abandoned_tracks[tid_int] = st

        # ------------------------------------------------------------------
        # Expire missing tracks
        # ------------------------------------------------------------------
        for tid, st in list(self._abandoned_tracks.items()):
            if tid in present_ids:
                continue
            st["missing_for_seconds"] = float(st.get("missing_for_seconds", 0.0) + dt_video)
            if float(st["missing_for_seconds"]) > float(config.track_timeout_seconds):
                self._abandoned_tracks.pop(tid, None)
                self.logger.info(f"[ABANDON-EXPIRE] dropped track tid={tid}")
            else:
                self._abandoned_tracks[tid] = st

    # =========================================================================
    # Alerts
    # =========================================================================

    def _check_alerts(
        self,
        detections: List[Dict[str, Any]],
        frame_key: str,
        config: AbandonedObjectConfig,
        video_time_seconds: float,
    ) -> List[Dict[str, Any]]:
        """
        Emit alerts for abandoned objects — one per track per cooldown window.
        """
        alerts: List[Dict[str, Any]] = []

        if config.alert_config:
            alert_type = getattr(config.alert_config, "alert_type", ["Default"])
            alert_value = getattr(config.alert_config, "alert_value", ["JSON"])
            settings_map = {t: v for t, v in zip(alert_type, alert_value)}
        else:
            alert_type = ["Default"]
            alert_value = ["JSON"]
            settings_map = {"Default": "JSON"}

        for det in detections:
            tid = det.get("track_id")
            tid_int = self._parse_track_id(tid)
            if tid_int is None or tid_int < 0:
                continue

            st = self._abandoned_tracks.get(tid_int)
            if not st:
                continue

            if not bool(st.get("is_abandoned", False)):
                continue

            # Cooldown check
            last_alert = st.get("last_alert_video_time", None)
            if last_alert is not None and (video_time_seconds - float(last_alert)) < float(
                config.alert_cooldown_seconds
            ):
                continue

            st["last_alert_video_time"] = float(video_time_seconds)
            self._abandoned_tracks[tid_int] = st

            bbox = det.get("bounding_box") or det.get("bbox")
            speed_window = list(st.get("speed_window", []))
            slow_flags = list(st.get("slow_flags_window", []))
            win_avg_speed = float(np.mean(speed_window)) if speed_window else 0.0
            win_slow_ratio = float(np.mean(slow_flags)) if slow_flags else 0.0

            alerts.append(
                {
                    "alert_type": alert_type,
                    "alert_id": f"abandoned_alert_{tid_int}_{frame_key}",
                    "incident_category": self.CASE_TYPE,
                    "track_id": tid_int,
                    "zone_name": self.GLOBAL_ZONE_NAME,
                    "bounding_box": bbox,
                    "confidence": float(det.get("confidence", 0.0)),
                    "category": det.get("category"),
                    "abandoned_for_seconds": round(float(st.get("abandonment_timer_seconds", 0.0)), 2),
                    "window_slow_ratio": round(float(win_slow_ratio), 3),
                    "avg_speed_px_per_sec": round(float(win_avg_speed), 3),
                    "threshold_seconds": float(config.abandonment_threshold_seconds),
                    "settings": settings_map,
                }
            )
            self.logger.info(
                f"[ABANDON-ALERT] emitted alert track_id={tid_int} frame={frame_key} "
                f"timer={st.get('abandonment_timer_seconds', 0.0):.1f}s"
            )

        return alerts

    # =========================================================================
    # Tracking state
    # =========================================================================

    def _update_tracking_state(self, detections: List[Dict[str, Any]]) -> None:
        categories = self.target_categories + ["abandoned_object"]
        if not self._per_category_total_track_ids:
            self._per_category_total_track_ids = {cat: set() for cat in categories}

        self._current_frame_track_ids = {cat: set() for cat in categories}

        for det in detections:
            cat = det.get("category")
            tid = det.get("track_id")
            tid_int = self._parse_track_id(tid)
            if cat not in categories or tid_int is None or tid_int < 0:
                continue
            self._current_frame_track_ids.setdefault(cat, set()).add(tid_int)

        # NEW = current - total, computed BEFORE updating total so a track_id
        # that already accumulated under e.g. "carry_bag" still correctly
        # counts as new the first time it appears under "abandoned_object"
        # (each category has its own independent cumulative set).
        self._new_track_ids_this_frame = {
            cat: (self._current_frame_track_ids.get(cat, set()) - self._per_category_total_track_ids.get(cat, set()))
            for cat in categories
        }

        for cat, ids in self._current_frame_track_ids.items():
            self._per_category_total_track_ids.setdefault(cat, set()).update(ids)

    def get_total_counts(self) -> Dict[str, int]:
        """Return total unique track_id counts per category."""
        return {cat: len(ids) for cat, ids in self._per_category_total_track_ids.items()}

    def get_new_counts_this_frame(self) -> Dict[str, int]:
        """Return count of NEW track_ids per category (first appearance under that category)."""
        return {cat: len(ids) for cat, ids in getattr(self, "_new_track_ids_this_frame", {}).items()}

    def _get_current_timestamp_str(
        self,
        stream_info: Dict[str, Any] | None,
        _precision: bool = False,
        _frame_id: str | None = None,
    ) -> str:
        """Canonical UTC timestamp generator — YYYY:MM:DD HH:MM:SS."""
        _ = (_frame_id, _precision)
        try:
            if stream_info:
                raw = stream_info.get("input_settings", {}).get("stream_time")
                if raw and isinstance(raw, str):
                    raw = raw.replace(" UTC", "").strip()
                    if "." in raw:
                        raw = raw.split(".")[0]
                    parts = raw.split("-")
                    if len(parts) >= 6:
                        return f"{parts[0]}:{parts[1]}:{parts[2]} {parts[3]}:{parts[4]}:{parts[5]}"
        except Exception as exc:
            self.logger.debug(
                "Failed to parse stream_time from stream_info in _get_timestamp_str: %r",
                exc,
            )
        return datetime.now(timezone.utc).strftime("%Y:%m:%d %H:%M:%S")

    def _count_categories(self, detections: List[Dict[str, Any]]) -> Dict[str, Any]:
        counts: Dict[str, int] = {}
        for det in detections:
            cat = det.get("category", "unknown")
            counts[cat] = counts.get(cat, 0) + 1

        return {
            "total_count": int(sum(counts.values())),
            "per_category_count": counts,
            "detections": [
                {
                    "bounding_box": det.get("bounding_box"),
                    "category": det.get("category"),
                    "confidence": det.get("confidence"),
                    "track_id": det.get("track_id"),
                    "frame_id": det.get("frame_id"),
                    "is_abandoned": bool(det.get("is_abandoned", False)),
                    "abandoned_for_seconds": det.get("abandoned_for_seconds", 0.0),
                }
                for det in detections
            ],
        }

    # =========================================================================
    # Incident manager (Incident/Volume Analytics registration)
    # =========================================================================

    def _initialize_incident_manager_once(self, config: AbandonedObjectConfig) -> None:
        """Initialize the incident manager exactly once (first ``process()`` call)."""
        if self._incident_manager_initialized:
            return
        try:
            self.logger.info(
                "[INCIDENT_MANAGER] Starting incident manager initialization for abandoned object detection..."
            )
            if self._incident_manager_factory is None:
                self._incident_manager_factory = IncidentManagerFactory(logger=self.logger)
            self._incident_manager = self._incident_manager_factory.initialize(config)
            if self._incident_manager:
                self.logger.info(
                    "[INCIDENT_MANAGER] Incident manager initialized successfully for abandoned object detection"
                )
            else:
                self.logger.warning("[INCIDENT_MANAGER] Incident manager not available; incidents won't be published")
        except Exception as e:
            self.logger.error(f"[INCIDENT_MANAGER] Incident manager initialization failed: {e}", exc_info=True)
        finally:
            self._incident_manager_initialized = True

    def _send_incident_to_manager(
        self,
        incident: Dict[str, Any],
        stream_info: Dict[str, Any] | None = None,
        context: ProcessingContext | None = None,
    ) -> bool:
        """Feed the abandoned-object incident (or ``{}``) to the IncidentManager every frame.

        Fire-style: always call ``process_incident`` so idle frames can close
        the incident cycle, matching the pattern used by intrusion_detection
        and dwell_detection.
        """
        camera_id = _resolve_manager_camera_id(stream_info)
        published = False

        if self._incident_manager:
            try:
                published = bool(
                    self._incident_manager.process_incident(
                        camera_id=camera_id,
                        incident_data=incident or {},
                        stream_info=stream_info,
                    )
                )
                if published:
                    self.logger.info(f"[INCIDENT_MANAGER] Incident published for camera: {camera_id}")
            except Exception as e:
                self.logger.error(f"[INCIDENT_MANAGER] Error publishing incident: {e}", exc_info=True)

        if context is not None:
            context.metadata["incident_published_via_manager"] = bool(self._incident_manager)
        return published

    def _build_manager_incident(
        self,
        incidents: Dict[str, Any],
        config: AbandonedObjectConfig,
        stream_info: Dict[str, Any] | None,
    ) -> Dict[str, Any]:
        """Build the lifecycle-aware incident object for IncidentManagerFactory.

        Kept separate from the ``incidents`` dict stored in agg_summary (which
        always carries frame_number/camera_info housekeeping and would never
        look "empty" to the manager) — the manager's own idle-detection checks
        for a literal ``{}``, so this returns exactly that when nothing is
        abandoned and there's no open episode to close.
        """
        abandoned_count = int(incidents.get("abandoned_count", 0))
        current_ts = self._get_current_timestamp_str(stream_info)
        camera_info = incidents.get("camera_info") or self.get_camera_info_from_stream(stream_info)

        if config.alert_config and getattr(config.alert_config, "count_thresholds", None):
            count_threshold = config.alert_config.count_thresholds.get("all", 1) or 1
        else:
            count_threshold = 1
        incident_quant = min(100.0, (abandoned_count / count_threshold) * 100.0) if count_threshold else 0.0

        if abandoned_count > 0:
            if not self._abandon_incident_active:
                self._abandon_incident_start_ts = current_ts
                self._abandon_incident_active = True
            event = self.create_incident(
                incident_id=self._abandon_incident_id,
                incident_type=self.CASE_TYPE,
                severity_level="critical",
                human_text=f"ABANDONED OBJECT @ {current_ts}: {abandoned_count} object(s) currently abandoned",
                camera_info=camera_info,
                alerts=incidents.get("alerts", []),
                start_time=self._abandon_incident_start_ts,
                end_time="",
                level_settings={"low": 1, "medium": 3, "significant": 4, "critical": 7},
            )
            event["incident_quant"] = round(incident_quant, 2)
            self._abandon_last_incident = dict(event)
            return event

        if self._abandon_incident_active and self._abandon_last_incident is not None:
            # Object no longer abandoned this frame — emit one closing
            # snapshot with a real end_time, then reset for the next episode.
            closing = dict(self._abandon_last_incident)
            closing["end_time"] = current_ts
            self._abandon_last_incident = None
            self._abandon_incident_active = False
            return closing

        return {}

    # =========================================================================
    # Per-frame processing
    # =========================================================================

    def _process_frame(
        self,
        frame_data: Any,
        config: AbandonedObjectConfig,
        frame_key: str,
        stream_info: Dict[str, Any] | None,
        context: ProcessingContext | None = None,
    ):
        self._total_frame_counter = int(frame_key)

        # Normalize detections
        if isinstance(frame_data, list):
            detections = frame_data
        elif isinstance(frame_data, dict) and "predictions" in frame_data:
            detections = frame_data["predictions"]
        else:
            detections = []

        # Confidence filter
        detections = filter_by_confidence(detections, config.confidence_threshold)

        # Category mapping
        if config.index_to_category:
            detections = apply_category_mapping(detections, config.index_to_category)

        # Keep only target categories
        detections = [d for d in detections if d.get("category") in self.target_categories]

        # Drop oversized bboxes — likely false detections, never fed into the tracker
        detections = self._filter_oversized_bboxes(detections, config)

        # FPS-aware dt
        fps = 30.0
        if stream_info:
            try:
                fps_val = stream_info.get("input_settings", {}).get("original_fps")
                if fps_val and float(fps_val) > 1e-6:
                    fps = float(fps_val)
            except Exception:
                fps = 30.0

        dt_video = 1.0 / max(1e-6, fps)
        video_time_seconds = self._total_frame_counter * dt_video

        # Tracking
        if config.enable_tracking:
            self._init_tracker(config, stream_info)
            if self.tracker:
                try:
                    if isinstance(self.tracker, ByteTrackWrapper):
                        detections = self.tracker.update(detections, stream_info=stream_info)
                    else:
                        detections = self.tracker.update(detections)
                except Exception:
                    self.logger.exception("[TRACKER-ERROR] tracker update failed")

        # Update state machine
        self._update_abandoned_states(detections, config, dt_video, video_time_seconds)

        # Enrich detections with abandonment flag.
        # Tracks that haven't hit track_confirmation_seconds yet are dropped
        # entirely here — no bbox is shown until a detection is confirmed.
        enriched_detections: List[Dict[str, Any]] = []
        for det in detections:
            tid = det.get("track_id")
            tid_int = self._parse_track_id(tid)
            is_abandoned = False
            abandoned_for_seconds = 0.0
            confirmed = True

            if tid_int is not None and tid_int >= 0:
                st = self._abandoned_tracks.get(tid_int)
                if st:
                    confirmed = bool(st.get("confirmed", False))
                    is_abandoned = bool(st.get("is_abandoned", False))
                    abandoned_for_seconds = round(float(st.get("abandonment_timer_seconds", 0.0)), 2)

            if not confirmed:
                continue

            det_out = dict(det)
            det_out["frame_id"] = frame_key
            det_out["is_abandoned"] = is_abandoned
            det_out["abandoned_for_seconds"] = abandoned_for_seconds

            if is_abandoned:
                det_out["category"] = "abandoned_object"
                det_out["class_id"] = ABANDONED_CLASS_ID

            enriched_detections.append(det_out)

        # Update unique tracking counts
        self._update_tracking_state(enriched_detections)

        # Counting summary
        counting_summary = self._count_categories(enriched_detections)

        # Alerts
        new_alerts = self._check_alerts(
            detections=enriched_detections,
            frame_key=frame_key,
            config=config,
            video_time_seconds=video_time_seconds,
        )

        # Active alerts (state-based)
        active_alerts = [
            {
                "alert_type": ["Default"],
                "alert_id": f"abandoned_active_{tid}_{frame_key}",
                "incident_category": self.CASE_TYPE,
                "track_id": tid,
                "zone_name": self.GLOBAL_ZONE_NAME,
                "status": "active",
                "abandoned_for_seconds": round(float(st.get("abandonment_timer_seconds", 0.0)), 2),
            }
            for tid, st in self._abandoned_tracks.items()
            if st.get("is_abandoned")
        ]

        # Tracking stats — cooldown-gated new_alerts, not active_alerts (which
        # would repeat every frame an object stays abandoned and defeat the
        # per-track alert cooldown entirely).
        tracking_stats = self._generate_tracking_stats(
            counting_summary,
            new_alerts,
            config,
            int(frame_key) if str(frame_key).isdigit() else None,
            stream_info,
        )

        # Incidents
        incidents = self._generate_incidents(
            counting_summary=counting_summary,
            alerts=new_alerts,
            config=config,
            frame_number=int(frame_key) if str(frame_key).isdigit() else None,
            stream_info=stream_info,
            video_time_seconds=video_time_seconds,
        )

        # Register with IncidentManager (Incident/Volume Analytics discovery) —
        # separate object from `incidents` above, see _build_manager_incident.
        manager_incident = self._build_manager_incident(incidents, config, stream_info)
        self._send_incident_to_manager(manager_incident, stream_info, context=context)

        business_analytics: Dict[str, Any] = {}

        summary_text = self._generate_summary(
            incidents=incidents,
            tracking_stats=tracking_stats,
            business_analytics=business_analytics,
        )

        return (
            incidents,
            tracking_stats,
            business_analytics,
            new_alerts,
            active_alerts,
            summary_text,
            enriched_detections,
        )

    # =========================================================================
    # Canonical process entry point
    # =========================================================================

    def process(
        self,
        data: Any,
        config: ConfigProtocol,
        context: ProcessingContext | None = None,
        stream_info: Dict[str, Any] | None = None,
    ) -> ProcessingResult:
        processing_start = time.time()

        if not isinstance(config, AbandonedObjectConfig):
            return self.create_error_result(
                "Invalid configuration type",
                usecase=self.name,
                category=self.category,
                context=context,
            )

        if context is None:
            context = ProcessingContext()

        context.input_format = match_results_structure(data)
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

        # Sync target_categories from config
        self.target_categories = list(config.target_categories)

        self._initialize_incident_manager_once(config)

        # Bbox smoothing (optional)
        if config.enable_smoothing:
            if self.smoothing_tracker is None:
                smoothing_config = BBoxSmoothingConfig(
                    smoothing_algorithm=config.smoothing_algorithm,
                    window_size=config.smoothing_window_size,
                    cooldown_frames=config.smoothing_cooldown_frames,
                    confidence_threshold=config.confidence_threshold,
                    confidence_range_factor=config.smoothing_confidence_range_factor,
                    enable_smoothing=True,
                )
                self.smoothing_tracker = BBoxSmoothingTracker(smoothing_config)
            data = bbox_smoothing(data, self.smoothing_tracker.config, self.smoothing_tracker)

        # Frame ID
        is_multi_frame = self.detect_frame_structure(data)
        if stream_info and "input_settings" in stream_info:
            frame_id = stream_info["input_settings"].get("start_frame")
        else:
            frame_id = None

        if frame_id is None or not isinstance(frame_id, (int, float)):
            frame_id = self._total_frame_counter + 1
        frame_id = int(frame_id)

        frames = data if is_multi_frame else {str(frame_id): data}

        frame_incidents: Dict[str, Any] = {}
        frame_tracking_stats: Dict[str, Any] = {}
        frame_business_analytics: Dict[str, Any] = {}
        frame_alerts: Dict[str, Any] = {}
        frame_human_text: Dict[str, Any] = {}
        enriched_detections: List[Dict[str, Any]] = []

        for frame_key, frame_data in frames.items():
            (
                incidents,
                tracking_stats,
                business_analytics,
                new_alerts,
                _active_alerts,
                summary_text,
                detections_out,
            ) = self._process_frame(frame_data, config, str(frame_key), stream_info, context=context)

            frame_incidents[str(frame_key)] = incidents
            frame_tracking_stats[str(frame_key)] = tracking_stats
            frame_business_analytics[str(frame_key)] = business_analytics
            frame_alerts[str(frame_key)] = new_alerts
            frame_human_text[str(frame_key)] = summary_text
            enriched_detections = detections_out

        agg_summary = self.create_frame_wise_agg_summary(
            frame_incidents,
            frame_tracking_stats,
            frame_business_analytics,
            frame_alerts,
            frame_human_text,
        )

        context.mark_completed()

        result = self.create_result(
            data={
                "agg_summary": agg_summary,
                "detections": enriched_detections,
            },
            usecase=self.name,
            category=self.category,
            context=context,
        )

        proc_time = time.time() - processing_start
        latency_ms = proc_time * 1000.0
        fps_out = (1.0 / proc_time) if proc_time > 0 else None
        perf_suffix = f"fps={fps_out:.1f}" if fps_out else ""
        self.logger.debug(
            "[PERF] F%s | latency=%.1fms %s",
            self._total_frame_counter,
            latency_ms,
            perf_suffix,
        )

        return result

    # =========================================================================
    # Output generators
    # =========================================================================

    def _generate_tracking_stats(
        self,
        counting_summary: Dict[str, Any],
        alerts: List[Dict[str, Any]],
        config: AbandonedObjectConfig,
        frame_number: int | None = None,
        stream_info: Dict[str, Any] | None = None,
    ) -> Dict[str, Any]:
        camera_info = self.get_camera_info_from_stream(stream_info)
        total_counts = [{"category": k, "count": int(v)} for k, v in self.get_total_counts().items()]
        current_counts = [
            {"category": k, "count": int(v)} for k, v in counting_summary.get("per_category_count", {}).items()
        ]
        abandoned_count = int(counting_summary.get("per_category_count", {}).get("abandoned_object", 0))

        human_text = (
            f"ABANDONED OBJECT @ {self._get_current_timestamp_str(stream_info)}\n"
            f"Abandoned objects in frame: {abandoned_count}\n"
            f"Threshold: {float(config.abandonment_threshold_seconds):.1f}s | "
            f"v_th: {float(config.velocity_threshold_px_per_sec):.1f}px/s | "
            f"ratio_th: {float(config.stationary_ratio_threshold):.2f}"
        )

        alert_settings = [
            {
                "alert_type": ["Default"],
                "incident_category": self.CASE_TYPE,
                "threshold_level": {"abandoned_object": config.abandonment_threshold_seconds},
                "ascending": True,
                "settings": {"Default": "JSON"},
            }
        ]

        if config.alert_config and hasattr(config.alert_config, "alert_type"):
            alert_settings.append(
                {
                    "alert_type": getattr(config.alert_config, "alert_type", ["Default"]),
                    "incident_category": self.CASE_TYPE,
                    "threshold_level": getattr(config.alert_config, "count_thresholds", {}) or {},
                    "ascending": True,
                    "settings": {
                        t: v
                        for t, v in zip(
                            getattr(config.alert_config, "alert_type", ["Default"]),
                            getattr(config.alert_config, "alert_value", ["JSON"]),
                        )
                    },
                }
            )

        current_new_counts = [{"category": k, "count": int(v)} for k, v in self.get_new_counts_this_frame().items()]

        return {
            "frame_number": frame_number,
            "camera_info": camera_info,
            "total_counts": total_counts,
            "current_counts": current_counts,
            "current_new_counts": current_new_counts,
            "abandoned_count": abandoned_count,
            "active_track_count": len(self._abandoned_tracks),
            "alerts": alerts,
            "alert_settings": alert_settings,
            "human_text": human_text,
        }

    def _generate_incidents(
        self,
        counting_summary: Dict[str, Any],
        alerts: List[Dict[str, Any]],
        config: AbandonedObjectConfig,
        frame_number: int | None = None,
        stream_info: Dict[str, Any] | None = None,
        video_time_seconds: float = 0.0,
    ) -> Dict[str, Any]:
        abandoned_count = int(counting_summary.get("per_category_count", {}).get("abandoned_object", 0))
        camera_info = self.get_camera_info_from_stream(stream_info)

        return {
            "frame_number": frame_number,
            "camera_info": camera_info,
            "incident_category": self.CASE_TYPE,
            "abandoned_count": abandoned_count,
            "alerts": alerts,
            "video_time_seconds": round(video_time_seconds, 2),
            "active_tracks": [
                {
                    "track_id": tid,
                    "presence_seconds": round(float(st.get("presence_seconds", 0.0)), 2),
                    "is_abandoned": bool(st.get("is_abandoned", False)),
                    "avg_speed": round(float(np.mean(list(st["speed_window"]))) if st.get("speed_window") else 0.0, 3),
                }
                for tid, st in self._abandoned_tracks.items()
            ],
        }

    def _generate_summary(
        self,
        incidents: Dict[str, Any],
        tracking_stats: Dict[str, Any],
        business_analytics: Dict[str, Any],
    ) -> str:
        abandoned_count = incidents.get("abandoned_count", 0)
        active_tracks = len(self._abandoned_tracks)
        if abandoned_count > 0:
            return f"ALERT: {abandoned_count} abandoned object(s) detected. Tracking {active_tracks} object(s) total."
        return f"Monitoring {active_tracks} object(s). No abandoned objects detected."
