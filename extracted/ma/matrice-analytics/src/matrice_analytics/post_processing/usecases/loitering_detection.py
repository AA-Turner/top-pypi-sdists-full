from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple
from collections import deque
import time
import numpy as np
from datetime import datetime, timezone

from ..core.base import BaseProcessor, ProcessingContext, ProcessingResult, ConfigProtocol
from ..core.config import BaseConfig, AlertConfig

from ..utils import (
    filter_by_confidence,
    apply_category_mapping,
    match_results_structure,
    bbox_smoothing,
    BBoxSmoothingConfig,
    BBoxSmoothingTracker,
    SORTTracker,
    ByteTrackWrapper,
    bbox_centroid,
    bbox_feet_point,
    dist,
    smooth_point,
    bbox_iou,
)


# =============================================================================
# Config
# =============================================================================
@dataclass
class LoiteringConfig(BaseConfig):

    confidence_threshold: float = 0.6
    target_categories: List[str] = field(default_factory=lambda: ["person"])

    loiter_threshold_seconds: float = 10.0
    velocity_threshold_px_per_sec: float = 18.0
    stationary_ratio_threshold: float = 0.70
    min_presence_seconds: float = 2.0

    behavior_window_seconds: float = 8.0
    min_behavior_window_seconds: float = 4.0

    track_timeout_seconds: float = 12.0

    max_centroid_jump_px: float = 80.0
    centroid_ema_alpha: float = 0.25

    speed_window_size: int = 15
    slow_flags_window_size: int = 15

    enable_smoothing: bool = True
    smoothing_algorithm: str = "observability"
    smoothing_window_size: int = 20
    smoothing_cooldown_frames: int = 5
    smoothing_confidence_range_factor: float = 0.5

    index_to_category: Optional[Dict[int, str]] = field(default_factory=lambda: {0: "person"})

    alert_cooldown_seconds: float = 4.0
    alert_config: Optional[AlertConfig] = None

    enable_tracking: bool = True
    tracking_method: str = "sort"

    tracking_max_age: int = 30
    tracking_min_hits: int = 2
    tracking_iou_threshold: float = 0.25

    def validate(self) -> List[str]:
        errors: List[str] = super().validate()

        if self.loiter_threshold_seconds < 0:
            errors.append("loiter_threshold_seconds must be non-negative")
        if self.velocity_threshold_px_per_sec < 0:
            errors.append("velocity_threshold_px_per_sec must be non-negative")
        if not 0.0 <= self.stationary_ratio_threshold <= 1.0:
            errors.append("stationary_ratio_threshold must be between 0 and 1")
        if self.speed_window_size < 3:
            errors.append("speed_window_size must be >= 3")
        if self.slow_flags_window_size < 3:
            errors.append("slow_flags_window_size must be >= 3")

        if self.alert_config:
            errors.extend(self.alert_config.validate())

        return errors


# =============================================================================
# Use Case
# =============================================================================
class LoiteringUseCase(BaseProcessor):

    GLOBAL_ZONE_NAME = "global"

    def __init__(self):
        super().__init__("loitering")

        self.category = "general"
        self.CASE_TYPE = "loitering"
        self.CASE_VERSION = "4.1"

        self.target_categories = ["person"]

        self.smoothing_tracker: Optional[BBoxSmoothingTracker] = None
        self.tracker: Optional[Any] = None

        self._total_frame_counter = 0
        self._loiter_tracks: Dict[int, Dict[str, Any]] = {}

        self._per_category_total_track_ids: Dict[str, set] = {}
        self._current_frame_track_ids: Dict[str, set] = {}
        self.start_timer = None
        self._tracking_start_time = None


    # =========================================================================
    # Canonical Process
    # =========================================================================
    def process(
        self,
        data: Any,
        config: ConfigProtocol,
        context: Optional[ProcessingContext] = None,
        stream_info: Optional[Dict[str, Any]] = None,
    ) -> ProcessingResult:

        processing_start = time.time()

        if not isinstance(config, LoiteringConfig):
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

        is_multi_frame = self.detect_frame_structure(data)
        frames = data if is_multi_frame else {"current_frame": data}

        frame_incidents = {}
        frame_tracking_stats = {}
        frame_business_analytics = {}
        frame_alerts = {}
        frame_human_text = {}

        enriched_detections: List[Dict[str, Any]] = []

        for frame_key, frame_data in frames.items():

            (
                incidents,
                tracking_stats,
                business_analytics,
                alerts,
                summary_text,
                detections_out,
            ) = self._process_frame(frame_data, config, str(frame_key), stream_info)

            frame_incidents[str(frame_key)] = incidents
            frame_tracking_stats[str(frame_key)] = tracking_stats
            frame_business_analytics[str(frame_key)] = business_analytics
            frame_alerts[str(frame_key)] = alerts
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
        fps = (1.0 / proc_time) if proc_time > 0 else None

        print(
            f"[PERF] F{self._total_frame_counter} | "
            f"latency={latency_ms:.1f}ms "
            + (f"fps={fps:.1f}" if fps else "")
        )

        return result
    # =========================================================================

    def _init_track_state(
        self,
        bbox: Dict[str, Any],
        centroid: Tuple[float, float],
        feet: Tuple[float, float],
        config: LoiteringConfig,
    ) -> Dict[str, Any]:
        """
        Create a new per-track state dict.

        The two sliding windows:
          - speed_window: instantaneous feet speed per frame (px/sec)
          - slow_flags_window: 1.0 if stationary else 0.0 (same length as speed_window)
        """
        win = max(3, int(config.speed_window_size))
        return {
            "presence_seconds": 0.0,
            "missing_for_seconds": 0.0,
            "last_bbox": bbox,
            "last_centroid": centroid,
            "smoothed_centroid": centroid,
            "last_feet": feet,
            "smoothed_feet": feet,
            "speed_window": deque(maxlen=win),
            "slow_flags_window": deque(maxlen=max(3, int(config.slow_flags_window_size))),
            "last_inst_speed_feet": 0.0,
            "last_inst_speed_centroid": 0.0,
            "is_loitering": False,
            "last_alert_video_time": None,
            "resurrection_hits": 0,
        }


    def _is_stationary(self, inst_speed_feet: float, inst_speed_centroid: float, config: LoiteringConfig) -> bool:
        """
        Determine if a track is stationary for this frame.
        Feet speed is treated more strictly, centroid speed is allowed more tolerance.
        """
        vth = float(config.velocity_threshold_px_per_sec)
        return (inst_speed_feet <= vth * 0.80) and (inst_speed_centroid <= vth * 1.20)
    

    def _process_frame(
        self,
        frame_data: Any,
        config: LoiteringConfig,
        frame_key: str,
        stream_info: Optional[Dict[str, Any]],
    ):
        """
        Canonical per-frame processing aligned with Matrice template.

        Returns:
            incidents: List[Dict]
            tracking_stats: List[Dict]
            business_analytics: List[Dict]
            alerts: List[Dict]
            summary_text: str
            enriched_detections: List[Dict]
        """

        # -------------------------------------------------
        # Frame counter (canonical)
        # -------------------------------------------------
        self._total_frame_counter += 1

        # -------------------------------------------------
        # Normalize detections
        # -------------------------------------------------
        if isinstance(frame_data, list):
            detections = frame_data
        elif isinstance(frame_data, dict) and "predictions" in frame_data:
            detections = frame_data["predictions"]
        else:
            detections = []

        # -------------------------------------------------
        # Confidence filtering
        # -------------------------------------------------
        detections = filter_by_confidence(detections, config.confidence_threshold)

        # -------------------------------------------------
        # Category mapping (if needed)
        # -------------------------------------------------
        if config.index_to_category:
            detections = apply_category_mapping(detections, config.index_to_category)

        # -------------------------------------------------
        # Keep only target categories
        # -------------------------------------------------
        detections = [
            d for d in detections
            if d.get("category") in config.target_categories
        ]
        # print(f"[FRAME {frame_key}] Person detections after filtering: {len(detections)}")

        # -------------------------------------------------
        # Compute dt_video + video_time_seconds
        # -------------------------------------------------
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

        # -------------------------------------------------
        # Tracking (if enabled)
        # -------------------------------------------------
        if config.enable_tracking:
            self._init_tracker(config, stream_info)

            if self.tracker:
                try:
                    if isinstance(self.tracker, ByteTrackWrapper):
                        detections = self.tracker.update(detections, stream_info=stream_info)
                    else:
                        detections = self.tracker.update(detections)
                except Exception as e:
                    print(f"[TRACKER-ERROR] {e}")

            active_tracks = sum(1 for d in detections if int(d.get("track_id", -1)) >= 0)
            # print(f"[FRAME {frame_key}] Active tracked detections: {active_tracks}")


        # -------------------------------------------------
        # Update loiter state machine
        # -------------------------------------------------
        self._update_loiter_states(
            detections=detections,
            config=config,
            dt_video=dt_video,
            video_time_seconds=video_time_seconds,
        )
        active_loiter_states = sum(1 for st in self._loiter_tracks.values() if st.get("is_loitering"))
        # print(f"[FRAME {frame_key}] Loiter state-machine active tracks: {active_loiter_states}")

        # -------------------------------------------------
        # Enrich detections with loiter flag
        # -------------------------------------------------
        enriched_detections: List[Dict[str, Any]] = []

        for det in detections:
            tid = det.get("track_id")
            is_loitering = False

            if tid is not None and int(tid) >= 0:
                st = self._loiter_tracks.get(int(tid))
                if st:
                    is_loitering = bool(st.get("is_loitering", False))

            det_out = dict(det)
            det_out["frame_id"] = frame_key
            det_out["is_loitering"] = is_loitering

            # Optional category transformation
            if is_loitering:
                det_out["category"] = "loitering_person"

            enriched_detections.append(det_out)

        loiter_frame_count = sum(1 for d in enriched_detections if d.get("is_loitering"))
        # print(f"[FRAME {frame_key}] Loiter detections in frame: {loiter_frame_count}")

        # -------------------------------------------------
        # Update unique tracking counts
        # -------------------------------------------------
        self._update_tracking_state(enriched_detections)

        # -------------------------------------------------
        # Counting summary (canonical)
        # -------------------------------------------------
        counting_summary = self._count_categories(enriched_detections)

        # -------------------------------------------------
        # Alerts
        # -------------------------------------------------
        alerts = self._check_alerts(
            detections=enriched_detections,
            frame_key=frame_key,
            config=config,
            video_time_seconds=video_time_seconds,
        )
        # print(f"[FRAME {frame_key}] Alerts emitted this frame: {len(alerts)}")

        # -------------------------------------------------
        # Tracking stats
        # -------------------------------------------------
        tracking_stats = self._generate_tracking_stats(
            counting_summary=counting_summary,
            alerts=alerts,
            config=config,
            frame_number=int(frame_key) if frame_key.isdigit() else None,
            stream_info=stream_info,
        )

        # -------------------------------------------------
        # Incidents
        # -------------------------------------------------
        incidents = self._generate_incidents(
            counting_summary=counting_summary,
            alerts=alerts,
            config=config,
            frame_number=int(frame_key) if frame_key.isdigit() else None,
            stream_info=stream_info,
            video_time_seconds=video_time_seconds,
        )

        # -------------------------------------------------
        # Business analytics (minimal canonical)
        # -------------------------------------------------
        business_analytics: List[Dict[str, Any]] = []

        # -------------------------------------------------
        # Human summary
        # -------------------------------------------------
        summary_text = self._generate_summary(
            incidents=incidents,
            tracking_stats=tracking_stats,
            business_analytics=business_analytics,
        )

        return (
            incidents,
            tracking_stats,
            business_analytics,
            alerts,
            summary_text,
            enriched_detections,
        )



    def _init_tracker(self, config: LoiteringConfig, stream_info: Optional[Dict[str, Any]]) -> None:
        """
        Initialize an internal tracker if enabled by config.

        Supported:
          - SORTTracker (Kalman + Hungarian)
          - ByteTrackWrapper (YOLOX BYTETracker wrapper)

        NOTE:
        - If you are already running YOLO.track(persist=True), you typically set
          enable_tracking=False so this is skipped.
        """
        if self.tracker is not None:
            return

        method = str(getattr(config, "tracking_method", "sort")).lower().strip()

        if method == "sort":
            self.tracker = SORTTracker(
                iou_threshold=float(getattr(config, "tracking_iou_threshold", 0.25)),
                max_age=int(getattr(config, "tracking_max_age", 30)),
                min_hits=int(getattr(config, "tracking_min_hits", 2)),
            )
            return

        if method == "bytetrack":
            # ByteTrackWrapper needs fps mostly for track management / time scaling
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

        # Unknown method => no tracking
        self.tracker = None

    def _update_loiter_states(
        self,
        detections: List[Dict[str, Any]],
        config: LoiteringConfig,
        dt_video: float,
        video_time_seconds: float,
    ) -> None:
        """
        Update the canonical per-track loiter state in `self._loiter_tracks`.

        This method is the "state machine heart" of the usecase.

        What it does:
        - Iterates detections for the configured target_categories ("person" by default)
        - For each detection with a valid track_id:
            * Initialize per-track state if this is a new track
            * Accumulate presence time using dt_video (fps-based)
            * Smooth centroid + feet point to reduce jitter (EMA)
            * Clamp large centroid jumps (prevents spikes in speed)
            * Compute instantaneous speed (px/sec) for centroid and feet
            * Push speed + stationary flags into sliding windows
            * Decide loitering based on:
                - presence >= loiter_threshold_seconds
                - slow_ratio >= stationary_ratio_threshold
                - avg_speed <= velocity_threshold_px_per_sec
        - Tracks missing detections and expires old tracks after track_timeout_seconds

        Notes:
        - `video_time_seconds` is currently used for alert cooldown outside this method,
          but it is kept in signature to support future time-based extensions.
        - This method does NOT modify detection objects directly. It only updates track state.
        """
        # Track IDs that appear in this frame (used to handle "missing" tracks later)
        present_ids: set[int] = set()

        # Helper: safely extract bbox dict from a detection
        def _get_bbox(det: Dict[str, Any]) -> Optional[Dict[str, float]]:
            bbox = det.get("bounding_box") or det.get("bbox")
            return bbox if isinstance(bbox, dict) else None

        # Helper: attempt to "heal" / merge an old track into a newly seen track_id
        # if the tracker re-assigns IDs briefly (common in occlusion / ID switches).
        def _try_heal_track_id(
            new_tid: int,
            new_bbox: Dict[str, float],
            new_feet: Tuple[float, float],
        ) -> Optional[int]:
            best_old_tid: Optional[int] = None
            best_score: float = -1.0

            # Only consider tracks missing for <= track_timeout_seconds
            max_missing = float(config.track_timeout_seconds)

            # Healing thresholds (soft-configurable via getattr)
            iou_thr = float(getattr(config, "id_heal_iou_threshold", 0.30))
            feet_dist_thr = float(getattr(config, "id_heal_feet_distance_px", 60.0))

            for old_tid, st in self._loiter_tracks.items():
                if old_tid == new_tid:
                    continue

                # Only consider "recently missing" tracks
                missing_for = float(st.get("missing_for_seconds", 0.0))
                if missing_for <= 0.0 or missing_for > max_missing:
                    continue

                old_bbox = st.get("last_bbox")
                if not isinstance(old_bbox, dict):
                    continue

                # Primary match signal = bbox IoU
                iou = float(bbox_iou(old_bbox, new_bbox))
                if iou >= iou_thr:
                    score = iou
                else:
                    # Fallback match signal = feet-point proximity
                    old_feet = st.get("smoothed_feet") or st.get("last_feet")
                    if not old_feet:
                        continue

                    feet_dist = float(dist(old_feet, new_feet))
                    if feet_dist <= feet_dist_thr:
                        score = 1.0 - min(1.0, feet_dist / max(1.0, feet_dist_thr))
                    else:
                        continue

                if score > best_score:
                    best_score = score
                    best_old_tid = old_tid

            if best_old_tid is None:
                return None

            # Merge old state into new track ID
            old_state = self._loiter_tracks.get(best_old_tid)
            if not old_state:
                return None

            self._loiter_tracks[new_tid] = old_state
            self._loiter_tracks.pop(best_old_tid, None)

            if getattr(config, "enable_id_healing_debug", True):
                self.logger.info(
                    f"[LOITER-ID-HEAL] merged old_tid={best_old_tid} -> new_tid={new_tid} score={best_score:.2f}"
                )

            return best_old_tid

        # ---------------------------------------------------------------------
        # Per-detection update (present tracks)
        # ---------------------------------------------------------------------
        for det in detections:
            # Ignore unrelated categories
            if det.get("category") not in self.target_categories:
                continue

            # Must have track_id for temporal analysis
            tid = det.get("track_id")
            if tid is None:
                continue

            try:
                tid_int = int(tid)
            except Exception:
                continue

            if tid_int < 0:
                continue

            bbox = _get_bbox(det)
            if not bbox:
                continue

            # Feature points derived from bbox
            centroid = bbox_centroid(bbox)
            feet = bbox_feet_point(bbox)

            # If track_id is new, attempt to heal by merging a recently-missing track
            if tid_int not in self._loiter_tracks and self._loiter_tracks:
                _try_heal_track_id(tid_int, bbox, feet)

            present_ids.add(tid_int)

            # If still new after healing attempt: initialize state and move on
            if tid_int not in self._loiter_tracks:
                self._loiter_tracks[tid_int] = self._init_track_state(bbox, centroid, feet, config)
                continue

            st = self._loiter_tracks[tid_int]

            # Presence accumulates in video-time (dt_video)
            st["presence_seconds"] = float(st.get("presence_seconds", 0.0) + dt_video)

            # Reset missing time since we saw it this frame
            st["missing_for_seconds"] = 0.0

            # Use smoothed points as speed reference (reduces jitter spikes)
            prev_centroid = st.get("smoothed_centroid", centroid)
            prev_feet = st.get("smoothed_feet", feet)

            # Exponential moving average smoothing for centroid
            centroid_alpha = float(config.centroid_ema_alpha)
            new_centroid = smooth_point(prev_centroid, centroid, centroid_alpha)

            # Feet point gets a slightly stronger smoothing by default
            feet_alpha = min(0.40, centroid_alpha + 0.10)
            new_feet = smooth_point(prev_feet, feet, float(feet_alpha))

            # Clamp sudden centroid jumps to keep speed stable
            max_jump = float(config.max_centroid_jump_px)
            if dist(prev_centroid, new_centroid) > max_jump:
                dx = new_centroid[0] - prev_centroid[0]
                dy = new_centroid[1] - prev_centroid[1]
                norm = max(1e-6, (dx * dx + dy * dy) ** 0.5)
                scale = max_jump / norm
                new_centroid = (prev_centroid[0] + dx * scale, prev_centroid[1] + dy * scale)

            # Instantaneous speeds (px/sec)
            dt_safe = max(1e-6, dt_video)
            inst_speed_centroid = dist(new_centroid, prev_centroid) / dt_safe
            inst_speed_feet = dist(new_feet, prev_feet) / dt_safe

            st["last_inst_speed_centroid"] = float(inst_speed_centroid)
            st["last_inst_speed_feet"] = float(inst_speed_feet)

            # Convert speeds into a stationary flag (1.0 or 0.0)
            stationary = self._is_stationary(inst_speed_feet, inst_speed_centroid, config)
            slow_flag = 1.0 if stationary else 0.0

            # Update sliding windows
            st["speed_window"].append(float(inst_speed_feet))
            st["slow_flags_window"].append(float(slow_flag))

            # Update last + smoothed anchors
            st["last_bbox"] = bbox
            st["last_centroid"] = centroid
            st["smoothed_centroid"] = new_centroid
            st["last_feet"] = feet
            st["smoothed_feet"] = new_feet

            presence = float(st.get("presence_seconds", 0.0))

            # Do not allow loitering decisions too early (warm-up)
            if presence < float(config.min_presence_seconds):
                st["is_loitering"] = False
                self._loiter_tracks[tid_int] = st
                continue

            # A minimal window is required for stable behavior stats
            enough_window = (
                len(st["speed_window"]) >= 3
                and len(st["slow_flags_window"]) >= 3
                and min(presence, float(config.behavior_window_seconds)) >= float(config.min_behavior_window_seconds)
            )

            # Compute behavior-window statistics
            win_avg_speed = float(np.mean(list(st["speed_window"]))) if st["speed_window"] else 0.0
            win_slow_ratio = float(np.mean(list(st["slow_flags_window"]))) if st["slow_flags_window"] else 0.0

            # Final loiter decision
            is_loitering = False
            if enough_window:
                is_loitering = (
                    presence >= float(config.loiter_threshold_seconds)
                    and win_slow_ratio >= float(config.stationary_ratio_threshold)
                    and win_avg_speed <= float(config.velocity_threshold_px_per_sec)
                )

            # Periodic debug (only after threshold time)
            if presence >= float(config.loiter_threshold_seconds) and (self._total_frame_counter % 50 == 0):
                self.logger.info(
                    f"[LOITER-DEBUG] tid={tid_int} presence={presence:.2f}s "
                    f"avg_speed={win_avg_speed:.2f} slow_ratio={win_slow_ratio:.2f} loiter={is_loitering}"
                )

            st["is_loitering"] = bool(is_loitering)
            self._loiter_tracks[tid_int] = st

        # ---------------------------------------------------------------------
        # Missing track handling (tracks not observed this frame)
        # ---------------------------------------------------------------------
        for tid, st in list(self._loiter_tracks.items()):
            if tid in present_ids:
                continue

            # Accumulate missing time in video-time
            st["missing_for_seconds"] = float(st.get("missing_for_seconds", 0.0) + dt_video)

            # Drop tracks that have been missing too long
            if float(st["missing_for_seconds"]) > float(config.track_timeout_seconds):
                self._loiter_tracks.pop(tid, None)
            else:
                self._loiter_tracks[tid] = st

    def _check_alerts(
        self,
        detections: List[Dict[str, Any]],
        frame_key: str,
        config: LoiteringConfig,
        video_time_seconds: float,
    ) -> List[Dict[str, Any]]:
        """
        Generate loitering alerts (cooldown-enforced per track_id).

        Alerts are only emitted when:
          - a track is currently loitering
          - cooldown time has passed since last alert for the same track
        """
        alerts: List[Dict[str, Any]] = []

        # Default alert output format
        alert_type = ["Default"]
        alert_value = ["JSON"]
        settings_map = {"Default": "JSON"}

        # If alert_config exists, build type->value mapping
        if config.alert_config:
            alert_type = getattr(config.alert_config, "alert_type", ["Default"])
            alert_value = getattr(config.alert_config, "alert_value", ["JSON"])
            settings_map = {t: v for t, v in zip(alert_type, alert_value)}

        for det in detections:
            tid = det.get("track_id")
            if tid is None or int(tid) < 0:
                if getattr(config, "enable_alerts_debug", False):
                    self.logger.info(f"[LOITER-ALERTS] skipping det without valid track_id: {tid}")
                continue

            tid = int(tid)
            st = self._loiter_tracks.get(tid)
            if not st:
                if getattr(config, "enable_alerts_debug", False):
                    self.logger.info(f"[LOITER-ALERTS] no state for tid={tid}")
                continue

            # Only alert on loitering tracks
            if not bool(st.get("is_loitering", False)):
                if getattr(config, "enable_alerts_debug", False):
                    self.logger.info(f"[LOITER-ALERTS] tid={tid} not loitering (state.is_loitering=False)")
                continue

            # Cooldown check (video-time based)
            last_alert = st.get("last_alert_video_time", None)
            if last_alert is not None and (video_time_seconds - float(last_alert)) < float(config.alert_cooldown_seconds):
                if getattr(config, "enable_alerts_debug", False):
                    self.logger.info(
                        f"[LOITER-ALERTS] tid={tid} cooldown active: now={video_time_seconds} last={last_alert} cooldown={config.alert_cooldown_seconds}"
                    )
                continue

            # Mark alert time
            st["last_alert_video_time"] = float(video_time_seconds)
            self._loiter_tracks[tid] = st

            bbox = det.get("bounding_box") or det.get("bbox")

            speed_window = list(st.get("speed_window", []))
            slow_flags = list(st.get("slow_flags_window", []))
            win_avg_speed = float(np.mean(speed_window)) if speed_window else 0.0
            win_slow_ratio = float(np.mean(slow_flags)) if slow_flags else 0.0

            alerts.append(
                {
                    "alert_type": alert_type,
                    "alert_id": f"loitering_alert_{tid}_{frame_key}",
                    "incident_category": self.CASE_TYPE,
                    "track_id": tid,
                    "zone_name": self.GLOBAL_ZONE_NAME,
                    "bounding_box": bbox,
                    "confidence": float(det.get("confidence", 0.0)),
                    "category": det.get("category"),
                    "dwell_seconds": round(float(st.get("presence_seconds", 0.0)), 2),
                    "window_slow_ratio": round(float(win_slow_ratio), 3),
                    "avg_speed_px_per_sec": round(float(win_avg_speed), 3),
                    "threshold_seconds": float(config.loiter_threshold_seconds),
                    "settings": settings_map,
                }
            )
            self.logger.info(f"[LOITER-ALERTS] emitted alert track_id={tid} frame_key={frame_key}")

        return alerts


    def _update_tracking_state(self, detections: List[Dict[str, Any]]) -> None:
        """
        Update unique-counting state used in tracking_stats output.

        We maintain:
          - _per_category_total_track_ids: unique ids seen over time
          - _current_frame_track_ids: ids seen in this frame
        """
        categories = self.target_categories + ["loitering_person"]
        if not self._per_category_total_track_ids:
            self._per_category_total_track_ids = {cat: set() for cat in categories}

        self._current_frame_track_ids = {cat: set() for cat in categories}

        for det in detections:
            cat = det.get("category")
            tid = det.get("track_id")
            if cat not in categories or tid is None or int(tid) < 0:
                continue

            tid = int(tid)
            self._per_category_total_track_ids.setdefault(cat, set()).add(tid)
            self._current_frame_track_ids[cat].add(tid)


    def _count_categories(self, detections: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Frame-level raw detection count (not unique-tracks).

        This supports the Matrice agg_summary schema:
          - total_count
          - per_category_count
          - list of detections (minimal schema)
        """
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
                    "is_loitering": bool(det.get("is_loitering", False)),
                }
                for det in detections
            ],
        }


    def _generate_tracking_stats(
        self,
        counting_summary: Dict[str, Any],
        alerts: List[Dict[str, Any]],
        config: LoiteringConfig,
        frame_number: Optional[int] = None,
        stream_info: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        camera_info = self.get_camera_info_from_stream(stream_info)
        total_counts = [{"category": k, "count": int(v)} for k, v in self.get_total_counts().items()]
        current_counts = [{"category": k, "count": int(v)} for k, v in counting_summary.get("per_category_count", {}).items()]

        detections_objs = []
        for det in counting_summary.get("detections", []):
            bbox = det.get("bounding_box", {}) or {}
            category = det.get("category", "unknown") or "unknown"
            detections_objs.append(self.create_detection_object(category, bbox))

        human_text = (
            f"LOITERING @ {self._get_current_timestamp_str(stream_info)}\n"
            f"Loiterers in frame: {int(counting_summary.get('per_category_count', {}).get('loitering_person', 0))}\n"
            f"Threshold: {float(config.loiter_threshold_seconds):.1f}s | "
            f"v_th: {float(config.velocity_threshold_px_per_sec):.1f}px/s | "
            f"ratio_th: {float(config.stationary_ratio_threshold):.2f}"
        )

        alert_settings = []
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

        tracking_stats = self.create_tracking_stats(
            total_counts=total_counts,
            current_counts=current_counts,
            detections=detections_objs,
            human_text=human_text,
            camera_info=camera_info,
            alerts=alerts,
            alert_settings=alert_settings,
            reset_settings=[{"interval_type": "daily", "reset_time": {"value": 9, "time_unit": "hour"}}],
            start_time=self._get_current_timestamp_str(stream_info),
            reset_time=self._get_current_timestamp_str(stream_info),
        )
        tracking_stats["target_categories"] = self.target_categories
        return [tracking_stats]


    def _generate_incidents(
        self,
        counting_summary: Dict[str, Any],
        alerts: List[Dict[str, Any]],
        config: LoiteringConfig,
        frame_number: Optional[int] = None,
        stream_info: Optional[Dict[str, Any]] = None,
        video_time_seconds: Optional[float] = None,
    ) -> List[Dict[str, Any]]:
        loiterers = int(counting_summary.get("per_category_count", {}).get("loitering_person", 0))
        if loiterers <= 0:
            return []
        human_text = (
            f"LOITERING @ {self._get_current_timestamp_str(stream_info)}\n"
            f"Loiterers in frame: {loiterers}"
        )
        camera_info = self.get_camera_info_from_stream(stream_info)

        # If there are LOITERING tracks but no alerts were generated (possibly due to missing alert_config
        # or suppressed logic), create a conservative fallback alert per loitering detection to ensure VMS
        # receives at least one alert payload per loiter event.
        fallback_alerts: List[Dict[str, Any]] = []
        if loiterers > 0 and (not alerts):
            warn_msg = "No alerts generated for loiterers; creating fallback alerts for compatibility with VMS"
            self.logger.info(f"[LOITER-FALLBACK] {warn_msg}")

            # build settings_map similar to _check_alerts default
            alert_type = ["Default"]
            alert_value = ["JSON"]
            settings_map = {"Default": "JSON"}

            # Iterate detections in counting_summary to find loitering_person entries
            for det in counting_summary.get("detections", []):
                try:
                    tid = det.get("track_id")
                    if tid is None or int(tid) < 0:
                        continue
                    tid = int(tid)
                except Exception:
                    continue

                if not bool(det.get("is_loitering", False)):
                    continue

                st = self._loiter_tracks.get(tid, {})
                speed_window = list(st.get("speed_window", [])) if st else []
                slow_flags = list(st.get("slow_flags_window", [])) if st else []
                win_avg_speed = float(np.mean(speed_window)) if speed_window else 0.0
                win_slow_ratio = float(np.mean(slow_flags)) if slow_flags else 0.0

                bbox = det.get("bounding_box") or det.get("bbox")

                # if a video_time_seconds is provided, set per-track last_alert_video_time to avoid duplicate alerts
                if video_time_seconds is not None and isinstance(st, dict):
                    try:
                        st["last_alert_video_time"] = float(video_time_seconds)
                        self._loiter_tracks[tid] = st
                    except Exception:
                        pass

                fallback_alerts.append(
                    {
                        "alert_type": alert_type,
                        "alert_id": f"loitering_alert_{tid}_{frame_number}",
                        "incident_category": self.CASE_TYPE,
                        "track_id": tid,
                        "zone_name": self.GLOBAL_ZONE_NAME,
                        "bounding_box": bbox,
                        "confidence": float(det.get("confidence", 0.0)),
                        "category": det.get("category"),
                        "dwell_seconds": round(float(st.get("presence_seconds", 0.0)), 2) if st else 0.0,
                        "window_slow_ratio": round(float(win_slow_ratio), 3),
                        "avg_speed_px_per_sec": round(float(win_avg_speed), 3),
                        "threshold_seconds": float(config.loiter_threshold_seconds),
                        "settings": settings_map,
                    }
                )

            # use fallback alerts as the alerts list passed into create_incident
            if fallback_alerts:
                alerts_to_use = fallback_alerts
            else:
                alerts_to_use = alerts
        else:
            alerts_to_use = alerts

        incident = self.create_incident(
            incident_id=f"{self.CASE_TYPE}_{frame_number or 'current_frame'}",
            incident_type=self.CASE_TYPE,
            severity_level="medium",
            human_text=human_text,
            camera_info=camera_info,
            alerts=alerts_to_use,
            alert_settings=[],
            start_time=self._get_current_timestamp_str(stream_info),
            end_time="Incident still active",
            level_settings={"low": 1, "medium": 3, "significant": 5, "critical": 8},
        )
        if not incident:
            return []
        return [incident]


    def _generate_summary(
        self,
        incidents: List[Dict[str, Any]],
        tracking_stats: List[Dict[str, Any]],
        business_analytics: List[Dict[str, Any]],
    ) -> str:

        lines: List[str] = []
        lines.append(f"Application Name: {self.CASE_TYPE}")
        lines.append(f"Application Version: {self.CASE_VERSION}")
        if tracking_stats:
            lines.append(f"Tracking Statistics:\t{tracking_stats[0].get('human_text', '')}")
        if incidents:
            lines.append(f"Incidents:\t{incidents[0].get('human_text', '')}")
        if business_analytics:
            lines.append(f"Business Analytics:\t{business_analytics[0].get('human_text', '')}")
        return "\n".join(lines)


    def get_total_counts(self) -> Dict[str, int]:
        """Return total unique track_id counts per category."""
        return {cat: len(ids) for cat, ids in self._per_category_total_track_ids.items()}


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