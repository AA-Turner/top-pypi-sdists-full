"""
Running Detection Use Case
==========================

Detects running individuals in a scene using velocity-based trajectory analysis
on tracked person detections. Outputs confirmed running detections only.

Pipeline
--------
detections → confidence filter → ProxyAdvancedTracker → RunningDetector
    → RunningConfirmationLayer → running-only output payload

Core Components
---------------
RunningDetector
    Computes height-normalised velocity (``height_norm``) per tracked person using
    bottom-25% centroid displacement between consecutive frames. Applies EWMA
    smoothing and classifies against a static threshold.

RunningConfirmationLayer
    Temporal persistence gate. A track is confirmed as running only when it
    exceeds ``min_positives_for_run`` positive classifications within a rolling
    ``confirmation_window_size`` frame window. Suppresses transient false positives.

Key Config Parameters
---------------------
running_detector_config['static_thresholds']['height_norm'] : float
    Primary running threshold. Fraction of body height displaced per frame.
    Default 0.06. Lower = more sensitive; typical range 0.04–0.10.

running_detector_config['ewma_alpha'] : float
    EWMA smoothing factor (0–1). Higher = less smoothing, faster response.
    Default 0.35.

running_detector_config['min_track_age'] : int
    Minimum frames a track must exist before classification is allowed.
    Default 5. Prevents spurious detections on newly appearing tracks.

min_positives_for_run : int
    Minimum positive frames within the confirmation window to confirm running.
    Default 3.

confirmation_window_size : int
    Rolling window size (frames) for the confirmation layer.
    Default 5.

Notes
-----
.. important::
    This is a **heuristic-based algorithm**. All thresholds are tuned for a
    general upright-person, mid-distance camera perspective and designed to be
    robust across common surveillance scenarios. However, **parameters should be
    reviewed and adjusted before deploying to a new client or camera setup**,
    particularly:

    - Camera height and angle (overhead vs. eye-level changes apparent velocity scale)
    - Scene depth and FOV (wide-angle lenses compress displacement)
    - Typical subject size in frame (affects ``height_norm`` calibration)
    - Frame rate (directly scales all velocity values)
    - Expected running vs. walking speed in the target environment

Output
------
Payload is returned under ``agg_summary[frame_number]['tracking_stats']`` with:

- ``current_counts`` — running count for the current frame
- ``total_counts``   — cumulative unique running track count since session start
- ``detections``     — confirmed running detections with category, bbox, velocity
"""

import time
from collections import defaultdict, deque
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

import numpy as np

from ..core.base import (
    BaseProcessor,
    ConfigProtocol,
    ProcessingContext,
    ProcessingResult,
)
from ..core.config import AlertConfig, BaseConfig
from ..utils import (
    BBoxSmoothingConfig,
    BBoxSmoothingTracker,
    apply_category_mapping,
    bbox_smoothing,
    count_objects_in_zones,
    filter_by_confidence,
    match_results_structure,
)
from ..utils.geometry_utils import get_bbox_bottom25_center, point_in_polygon


class RunningDetector:
    """
    Velocity-based running detection from tracked person detections.
    Uses height-normalized velocity for scale-invariant detection.
    """

    DEFAULT_CONFIG = {
        "fps": 30,
        "min_track_age": 5,
        "velocity_units": ["pixel_per_frame", "height_norm"],
        "primary_unit": "height_norm",
        "smoother": "ewma",
        "ewma_alpha": 0.35,
        "ma_window": 5,
        "threshold_method": "static",
        "static_thresholds": {"height_norm": 0.06, "pixel_per_frame": 8.0},
        "trajectory_buffer_size": 60,
    }

    def __init__(self, config: Optional[Dict] = None):
        self.config = {**self.DEFAULT_CONFIG, **(config or {})}
        self.trajectories: Dict[int, deque] = {}
        self.velocity_history: Dict[int, deque] = {}
        self.smoothed_state: Dict[int, Dict[str, float]] = {}
        self.track_ages: Dict[int, int] = {}
        self.frame_count = 0

    def update(self, detections: List[Dict], frame_id: Optional[int] = None) -> List[Dict]:
        """Process detections and add velocity/running info."""
        if frame_id is not None:
            self.frame_count = frame_id
        else:
            self.frame_count += 1

        for det in detections:
            track_id = det.get("track_id")
            bbox = det.get("bounding_box")
            if track_id is None or bbox is None:
                continue

            centroid, height = self._extract_features(bbox)
            self._update_trajectory(track_id, centroid, height)
            velocity = self._compute_velocity(track_id)
            smoothed = self._smooth_velocity(track_id, velocity)
            is_running, details = self._classify_running(track_id, smoothed)

            det["velocity"] = velocity
            det["smoothed_velocity"] = smoothed
            det["is_running"] = is_running
            det["running_details"] = details

        return detections

    def _extract_features(self, bbox: Dict) -> Tuple[Tuple[float, float], float]:
        """Extract bottom-25% centroid and bbox height."""
        if "xmin" in bbox:
            x1, y1, x2, y2 = bbox["xmin"], bbox["ymin"], bbox["xmax"], bbox["ymax"]
        elif "x1" in bbox:
            x1, y1, x2, y2 = bbox["x1"], bbox["y1"], bbox["x2"], bbox["y2"]
        else:
            vals = list(bbox.values())
            if len(vals) >= 4:
                x1, y1, x2, y2 = vals[0], vals[1], vals[2], vals[3]
            else:
                return (0, 0), 1
        height = max(y2 - y1, 1)
        cx = (x1 + x2) / 2
        cy = y2 - 0.25 * height
        return (cx, cy), height

    def _update_trajectory(self, track_id: int, centroid: Tuple[float, float], height: float):
        if track_id not in self.trajectories:
            self.trajectories[track_id] = deque(maxlen=self.config["trajectory_buffer_size"])
            self.track_ages[track_id] = 0
        self.trajectories[track_id].append((centroid, height))
        self.track_ages[track_id] += 1

    def _compute_velocity(self, track_id: int) -> Dict[str, float]:
        traj = self.trajectories.get(track_id)
        if not traj or len(traj) < 2:
            return {}
        (c1, h1), (c2, h2) = traj[-2], traj[-1]
        dx, dy = c2[0] - c1[0], c2[1] - c1[1]
        pixel_disp = np.sqrt(dx * dx + dy * dy)
        height = (h1 + h2) / 2

        velocity = {}
        if "pixel_per_frame" in self.config["velocity_units"]:
            velocity["pixel_per_frame"] = pixel_disp
        if "height_norm" in self.config["velocity_units"]:
            velocity["height_norm"] = pixel_disp / height if height > 0 else 0

        if track_id not in self.velocity_history:
            self.velocity_history[track_id] = deque(maxlen=self.config["trajectory_buffer_size"])
        self.velocity_history[track_id].append(velocity)
        return velocity

    def _smooth_velocity(self, track_id: int, velocity: Dict[str, float]) -> float:
        primary_unit = self.config["primary_unit"]
        if not velocity or primary_unit not in velocity:
            return 0.0
        raw_value = velocity[primary_unit]
        smoother = self.config["smoother"]

        if track_id not in self.smoothed_state:
            self.smoothed_state[track_id] = {}

        if smoother == "none":
            return raw_value
        elif smoother == "ewma":
            alpha = self.config["ewma_alpha"]
            prev = self.smoothed_state[track_id].get(primary_unit, raw_value)
            smoothed = alpha * raw_value + (1 - alpha) * prev
            self.smoothed_state[track_id][primary_unit] = smoothed
            return smoothed
        elif smoother == "ma":
            history = self.velocity_history.get(track_id, deque())
            window = self.config["ma_window"]
            recent = [v.get(primary_unit, 0) for v in list(history)[-window:]]
            return np.mean(recent) if recent else raw_value
        return raw_value

    def _classify_running(self, track_id: int, smoothed_velocity: float) -> Tuple[bool, Dict]:
        details = {
            "smoothed_velocity": smoothed_velocity,
            "track_age": self.track_ages.get(track_id, 0),
        }
        if self.track_ages.get(track_id, 0) < self.config["min_track_age"]:
            details["suppressed"] = True
            return False, details

        primary_unit = self.config["primary_unit"]
        threshold = self.config["static_thresholds"].get(primary_unit, 0.05)
        details["threshold_value"] = threshold
        is_running = smoothed_velocity > threshold
        return is_running, details

    def reset(self):
        self.trajectories.clear()
        self.velocity_history.clear()
        self.smoothed_state.clear()
        self.track_ages.clear()
        self.frame_count = 0

    def cleanup_lost_tracks(self, active_track_ids: List[int]):
        active_set = set(active_track_ids)
        for store in [
            self.trajectories,
            self.velocity_history,
            self.smoothed_state,
            self.track_ages,
        ]:
            dead_ids = [tid for tid in store if tid not in active_set]
            for tid in dead_ids:
                del store[tid]


@dataclass
class RunningConfirmationConfig:
    """Configuration for running detection confirmation layer."""

    window_size: int = 10
    min_positives_for_run: int = 5
    track_eviction_frames: int = 60
    enabled: bool = True


class RunningConfirmationLayer:
    """
    Per-track temporal confirmation for running detection.
    Suppresses flickering FPs by requiring persistent running classification.
    """

    def __init__(self, config: Optional[RunningConfirmationConfig] = None):
        self.config = config or RunningConfirmationConfig()
        self._track_windows: Dict[Any, deque] = defaultdict(lambda: deque(maxlen=self.config.window_size))
        self._track_last_seen: Dict[Any, int] = {}
        self._frame_count: int = 0
        self._stats = {
            "total_running_raw": 0,
            "confirmed_running": 0,
            "suppressed_running": 0,
        }

    def update(self, detections: List[Dict]) -> List[Dict]:
        """
        Apply confirmation logic to running detections.
        Only detections meeting min_positives_for_run threshold are confirmed.
        """
        if not self.config.enabled:
            return detections

        self._frame_count += 1
        output = []

        for det in detections:
            track_id = det.get("track_id")
            is_running_raw = det.get("is_running", False)

            if track_id is None:
                output.append(det)
                continue

            self._track_last_seen[track_id] = self._frame_count
            self._track_windows[track_id].append(is_running_raw)

            if is_running_raw:
                self._stats["total_running_raw"] += 1

            is_confirmed = self._evaluate_track(track_id)

            det_out = det.copy()
            det_out["is_running_confirmed"] = is_confirmed

            if is_running_raw and is_confirmed:
                self._stats["confirmed_running"] += 1
            elif is_running_raw and not is_confirmed:
                self._stats["suppressed_running"] += 1

            output.append(det_out)

        if self._frame_count % 30 == 0:
            self._evict_stale_tracks()

        return output

    def _evaluate_track(self, track_id: Any) -> bool:
        window = self._track_windows.get(track_id)
        if window is None or len(window) == 0:
            return False
        return sum(1 for is_run in window if is_run) >= self.config.min_positives_for_run

    def _evict_stale_tracks(self):
        eviction_threshold = self._frame_count - self.config.track_eviction_frames
        stale_ids = [tid for tid, last_seen in self._track_last_seen.items() if last_seen < eviction_threshold]
        for tid in stale_ids:
            self._track_windows.pop(tid, None)
            self._track_last_seen.pop(tid, None)

    def get_stats(self) -> Dict[str, Any]:
        return {
            **self._stats,
            "active_tracks": len(self._track_windows),
            "frame_count": self._frame_count,
        }

    def reset(self):
        self._track_windows.clear()
        self._track_last_seen.clear()
        self._frame_count = 0
        self._stats = {
            "total_running_raw": 0,
            "confirmed_running": 0,
            "suppressed_running": 0,
        }


@dataclass
class RunningDetectionConfig(BaseConfig):
    """Configuration for running detection use case."""

    enable_smoothing: bool = True
    smoothing_algorithm: str = "observability"
    smoothing_window_size: int = 20
    smoothing_cooldown_frames: int = 5
    smoothing_confidence_range_factor: float = 0.5
    confidence_threshold: float = 0.6

    enable_class_aggregation: bool = False
    class_aggregation_window_size: int = 30

    zone_config: Optional[Dict[str, List[List[float]]]] = None

    usecase_categories: List[str] = field(default_factory=lambda: ["running"])
    target_categories: List[str] = field(default_factory=lambda: ["running"])

    alert_config: AlertConfig = field(default_factory=lambda: AlertConfig(count_thresholds={"running": 1}))

    index_to_category: Optional[Dict[int, str]] = field(default_factory=lambda: {0: "running"})

    running_detector_config: Dict = field(
        default_factory=lambda: {
            "fps": 30,
            "min_track_age": 3,
            "primary_unit": "height_norm",
            "smoother": "ewma",
            "ewma_alpha": 0.35,
            "static_thresholds": {"height_norm": 0.06, "pixel_per_frame": 8.0},
        }
    )

    min_positives_for_run: int = 3
    confirmation_window_size: int = 5


class RunningDetectionUseCase(BaseProcessor):
    CATEGORY_DISPLAY = {"running": "People Running"}

    def __init__(self):
        super().__init__("running_detection")
        self.category = "security"
        self.CASE_TYPE: Optional[str] = "running_detection"
        self.CASE_VERSION: Optional[str] = "1.0"
        self.target_categories = ["running"]

        # Core components
        self.smoothing_tracker = None
        self.tracker = None
        self.running_detector = None
        self.running_confirmator = None

        # Tracking state
        self._total_frame_counter = 0
        self._global_frame_offset = 0
        self._tracking_start_time = None
        self._track_aliases: Dict[Any, Any] = {}
        self._canonical_tracks: Dict[Any, Dict[str, Any]] = {}
        self._track_merge_iou_threshold: float = 0.05
        self._track_merge_time_window: float = 7.0
        self._ascending_alert_list: List[int] = []
        self.current_incident_end_timestamp: str = "N/A"
        self.start_timer = None

        # Count tracking
        self._per_category_total_track_ids = {cat: set() for cat in self.target_categories}
        self._current_frame_track_ids = {cat: set() for cat in self.target_categories}
        self._new_track_ids_this_frame = {cat: set() for cat in self.target_categories}
        self._previous_frame_track_ids = {cat: set() for cat in self.target_categories}
        self._tracked_in_zones = set()
        self._total_count_list = []

        # Zone tracking
        self._zone_current_track_ids = {}
        self._zone_total_track_ids = {}
        self._zone_current_counts = {}
        self._zone_total_counts = {}

    def process(
        self,
        data: Any,
        config: ConfigProtocol,
        context: Optional[ProcessingContext] = None,
        stream_info: Optional[Dict[str, Any]] = None,
    ) -> ProcessingResult:
        processing_start = time.time()

        if not isinstance(config, RunningDetectionConfig):
            return self.create_error_result(
                f"Invalid config type: expected RunningDetectionConfig, got {type(config).__name__}",
                usecase=self.name,
                category=self.category,
                context=context,
            )

        if context is None:
            context = ProcessingContext()

        has_zones = bool(config.zone_config and config.zone_config.get("zones"))

        data = self._normalize_yolo_results(data, config.index_to_category)

        input_format = match_results_structure(data)
        context.input_format = input_format
        context.confidence_threshold = config.confidence_threshold

        processed_data = (
            filter_by_confidence(data, config.confidence_threshold) if config.confidence_threshold else data
        )

        if config.index_to_category:
            processed_data = apply_category_mapping(processed_data, config.index_to_category)

        # Bbox smoothing
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
            processed_data = bbox_smoothing(processed_data, self.smoothing_tracker.config, self.smoothing_tracker)

        # Tracking
        try:
            from ..advanced_tracker.proxy_tracker import ProxyAdvancedTracker

            if self.tracker is None:
                self.tracker = ProxyAdvancedTracker(iou_threshold=0.3, max_misses=30)
                self.logger.info("Initialized ProxyAdvancedTracker for Running Detection")
            processed_data = self.tracker.update(processed_data)
        except Exception as e:
            self.logger.warning(f"ProxyAdvancedTracker failed: {e}")

        for det in processed_data:
            det["category"] = "running"

        # Running Detector
        if self.running_detector is None:
            detector_config = config.running_detector_config.copy()
            if stream_info:
                fps = stream_info.get("input_settings", {}).get("original_fps", 30)
                detector_config["fps"] = fps
            self.running_detector = RunningDetector(detector_config)
            self.logger.info(f"Initialized RunningDetector with config: {detector_config}")

        processed_data = self.running_detector.update(processed_data, self._total_frame_counter)

        # Confirmation layer
        if self.running_confirmator is None:
            confirm_config = RunningConfirmationConfig(
                window_size=config.confirmation_window_size,
                min_positives_for_run=config.min_positives_for_run,
                enabled=True,
            )
            self.running_confirmator = RunningConfirmationLayer(confirm_config)
            self.logger.info(f"Initialized RunningConfirmationLayer (min_positives={config.min_positives_for_run})")

        processed_data = self.running_confirmator.update(processed_data)

        # Only keep confirmed running detections
        running_detections = [det for det in processed_data if det.get("is_running_confirmed", False)]

        if self._total_frame_counter % 100 == 0:
            stats = self.running_confirmator.get_stats()
            self.logger.debug(f"Running confirmation stats: {stats}")

        self._update_tracking_state(running_detections, _has_zones=has_zones)
        self._total_frame_counter += 1

        # Frame number
        frame_number = None
        if stream_info:
            input_settings = stream_info.get("input_settings", {})
            start_frame = input_settings.get("start_frame")
            end_frame = input_settings.get("end_frame")
            if start_frame is not None and end_frame is not None and start_frame == end_frame:
                frame_number = start_frame

        counting_summary = self._count_categories(running_detections, config)
        total_counts = self.get_total_counts()
        counting_summary["total_counts"] = total_counts
        counting_summary["categories"] = {}
        for detection in running_detections:
            category = detection.get("category", "running")
            counting_summary["categories"][category] = counting_summary["categories"].get(category, 0) + 1

        # Zone analysis
        zone_analysis = {}
        if has_zones:
            zone_analysis = count_objects_in_zones(running_detections, config.zone_config["zones"], stream_info)
            if zone_analysis:
                enhanced_zone_analysis = self._update_zone_tracking(zone_analysis, running_detections, config)
                for zone_name, enhanced_data in enhanced_zone_analysis.items():
                    zone_analysis[zone_name] = enhanced_data
                per_category_count = {
                    cat: len(self._current_frame_track_ids.get(cat, set())) for cat in self.target_categories
                }
                counting_summary["per_category_count"] = {k: v for k, v in per_category_count.items() if v > 0}
                counting_summary["total_count"] = sum(per_category_count.values())

        alerts = self._check_alerts(counting_summary, frame_number, config)

        incidents_list = self._generate_incidents(
            counting_summary, zone_analysis, alerts, config, frame_number, stream_info
        )
        tracking_stats_list = self._generate_tracking_stats(
            counting_summary, zone_analysis, alerts, config, frame_number, stream_info
        )
        business_analytics_list = self._generate_business_analytics(
            counting_summary, zone_analysis, alerts, config, stream_info, is_empty=True
        )
        summary_list = self._generate_summary(
            counting_summary,
            zone_analysis,
            incidents_list,
            tracking_stats_list,
            business_analytics_list,
            alerts,
        )

        incidents = incidents_list[0] if incidents_list else {}
        tracking_stats = tracking_stats_list[0] if tracking_stats_list else {}
        business_analytics = business_analytics_list[0] if business_analytics_list else {}
        summary = summary_list[0] if summary_list else {}

        agg_summary = {
            str(frame_number): {
                "incidents": incidents,
                "tracking_stats": tracking_stats,
                "business_analytics": business_analytics,
                "alerts": alerts,
                "zone_analysis": zone_analysis,
                "human_text": summary,
            }
        }

        context.mark_completed()
        result = self.create_result(
            data={"agg_summary": agg_summary},
            usecase=self.name,
            category=self.category,
            context=context,
        )

        proc_time = time.time() - processing_start
        print(
            f"latency_ms: {proc_time * 1000:.1f} | fps: {1 / proc_time:.1f} | frame: {self._total_frame_counter} | running: {len(running_detections)}"
        )

        return result

    def _normalize_yolo_results(self, data: Any, index_to_category: Optional[Dict[int, str]] = None) -> Any:
        """Normalize YOLO outputs to internal schema."""

        def to_bbox_dict(d):
            if "bounding_box" in d and isinstance(d["bounding_box"], dict):
                return d["bounding_box"]
            if "bbox" in d:
                bbox = d["bbox"]
                if isinstance(bbox, dict):
                    return bbox
                if isinstance(bbox, (list, tuple)) and len(bbox) >= 4:
                    return {"x1": bbox[0], "y1": bbox[1], "x2": bbox[2], "y2": bbox[3]}
            if "xyxy" in d and isinstance(d["xyxy"], (list, tuple)) and len(d["xyxy"]) >= 4:
                return {
                    "x1": d["xyxy"][0],
                    "y1": d["xyxy"][1],
                    "x2": d["xyxy"][2],
                    "y2": d["xyxy"][3],
                }
            return {}

        def resolve_category(d):
            raw_cls = d.get("category", d.get("category_id", d.get("class", d.get("cls"))))
            if isinstance(raw_cls, int):
                if index_to_category and raw_cls in index_to_category:
                    return index_to_category[raw_cls], raw_cls
                return str(raw_cls), raw_cls
            if isinstance(raw_cls, str):
                return raw_cls, None
            return "unknown", None

        def normalize_det(det):
            category_name, category_id = resolve_category(det)
            confidence = det.get("confidence", det.get("conf", det.get("score", 0.0)))
            bbox = to_bbox_dict(det)
            normalized = {
                "category": category_name,
                "confidence": confidence,
                "bounding_box": bbox,
            }
            if category_id is not None:
                normalized["category_id"] = category_id
            for key in ("track_id", "frame_id", "masks", "segmentation"):
                if key in det:
                    normalized[key] = det[key]
            return normalized

        if isinstance(data, list):
            return [normalize_det(d) if isinstance(d, dict) else d for d in data]
        if isinstance(data, dict):
            return {k: ([normalize_det(d) for d in v] if isinstance(v, list) else v) for k, v in data.items()}
        return data

    def _update_tracking_state(self, detections: list, _has_zones: bool = False):
        """Update tracking state with confirmed running detections."""
        _ = (_has_zones,)
        if not hasattr(self, "_per_category_total_track_ids"):
            self._per_category_total_track_ids = {cat: set() for cat in self.target_categories}
        if not hasattr(self, "_previous_frame_track_ids"):
            self._previous_frame_track_ids = {cat: set() for cat in self.target_categories}

        self._current_frame_track_ids = {cat: set() for cat in self.target_categories}

        for det in detections:
            cat = det.get("category")
            raw_track_id = det.get("track_id")
            if cat not in self.target_categories or raw_track_id is None:
                continue
            bbox = det.get("bounding_box", det.get("bbox"))
            canonical_id = self._merge_or_register_track(raw_track_id, bbox)
            det["track_id"] = canonical_id
            self._current_frame_track_ids.setdefault(cat, set()).add(canonical_id)

        self._new_track_ids_this_frame = {
            cat: (self._current_frame_track_ids.get(cat, set()) - self._per_category_total_track_ids.get(cat, set()))
            for cat in self.target_categories
        }

        for cat, ids in self._current_frame_track_ids.items():
            self._per_category_total_track_ids.setdefault(cat, set()).update(ids)

        self._previous_frame_track_ids = {cat: set(ids) for cat, ids in self._current_frame_track_ids.items()}

    def _init_zone_tracking_stores(self, zones: Dict) -> None:
        """Ensure zone tracking dicts are initialized for all zones."""
        for zone_name in zones:
            if zone_name not in self._zone_current_track_ids:
                self._zone_current_track_ids[zone_name] = set()
            if zone_name not in self._zone_total_track_ids:
                self._zone_total_track_ids[zone_name] = set()

    def _assign_detections_to_zones(self, detections: List[Dict], zones: Dict, track_to_cat: Dict) -> Dict[str, set]:
        """Assign each detection to zones based on bbox center position."""
        current_frame_zone_tracks: Dict[str, set] = {z: set() for z in zones}
        for det in detections:
            track_id = det.get("track_id")
            bbox = det.get("bounding_box", det.get("bbox"))
            if not track_id or not bbox:
                continue
            center = get_bbox_bottom25_center(bbox)
            for zone_name, polygon in zones.items():
                pts = [(p[0], p[1]) for p in polygon]
                if not point_in_polygon(center, pts):
                    continue
                current_frame_zone_tracks[zone_name].add(track_id)
                cat = track_to_cat.get(track_id)
                if cat:
                    self._current_frame_track_ids.setdefault(cat, set()).add(track_id)
                    self._tracked_in_zones.add(track_id)
        return current_frame_zone_tracks

    def _update_zone_tracking(self, zone_analysis: Dict, detections: List[Dict], config) -> Dict:
        """Update zone tracking with current frame data."""
        if not zone_analysis or not config.zone_config or not config.zone_config.get("zones"):
            return {}

        zones = config.zone_config["zones"]
        self._init_zone_tracking_stores(zones)

        track_to_cat = {det.get("track_id"): det.get("category") for det in detections if det.get("track_id")}
        current_frame_zone_tracks = self._assign_detections_to_zones(detections, zones, track_to_cat)

        enhanced = {}
        for zone_name, counts in zone_analysis.items():
            current = current_frame_zone_tracks.get(zone_name, set())
            self._zone_current_track_ids[zone_name] = current
            self._zone_total_track_ids[zone_name].update(current)
            self._zone_current_counts[zone_name] = len(current)
            self._zone_total_counts[zone_name] = len(self._zone_total_track_ids[zone_name])
            enhanced[zone_name] = {
                "current_count": self._zone_current_counts[zone_name],
                "total_count": self._zone_total_counts[zone_name],
                "current_track_ids": list(current),
                "total_track_ids": list(self._zone_total_track_ids[zone_name]),
                "original_counts": counts,
            }
        return enhanced

    def _count_categories(self, detections: list, _config) -> dict:
        _ = (_config,)
        counts = {}
        for det in detections:
            cat = det.get("category", "running")
            counts[cat] = counts.get(cat, 0) + 1
        return {
            "total_count": sum(counts.values()),
            "per_category_count": counts,
            "detections": [
                {
                    "bounding_box": det.get("bounding_box"),
                    "category": det.get("category"),
                    "confidence": det.get("confidence"),
                    "track_id": det.get("track_id"),
                    "frame_id": det.get("frame_id"),
                    "velocity": det.get("velocity", {}),
                    "smoothed_velocity": det.get("smoothed_velocity", 0),
                }
                for det in detections
            ],
        }

    def get_total_counts(self):
        return {cat: len(self._per_category_total_track_ids.get(cat, set())) for cat in self.target_categories}

    def get_new_counts_this_frame(self) -> Dict[str, int]:
        return {cat: len(ids) for cat, ids in getattr(self, "_new_track_ids_this_frame", {}).items()}

    def _check_alerts(self, summary: dict, frame_number: Any, config) -> List[Dict]:
        frame_key = str(frame_number) if frame_number is not None else "current_frame"
        alerts = []
        total = summary.get("total_count", 0)
        per_cat = summary.get("per_category_count", {})

        if not config.alert_config:
            return alerts

        thresholds = getattr(config.alert_config, "count_thresholds", {})
        for category, threshold in thresholds.items():
            if category == "all" and total >= threshold:
                alerts.append(
                    {
                        "alert_id": f"alert_all_{frame_key}",
                        "category": "all",
                        "count": total,
                        "threshold": threshold,
                    }
                )
            elif category in per_cat and per_cat[category] >= threshold:
                alerts.append(
                    {
                        "alert_id": f"alert_{category}_{frame_key}",
                        "category": category,
                        "count": per_cat[category],
                        "threshold": threshold,
                    }
                )
        return alerts

    def _generate_incidents(
        self,
        counting_summary: Dict,
        _zone_analysis: Dict,
        alerts: List,
        config: RunningDetectionConfig,
        frame_number: Optional[int] = None,
        stream_info: Optional[Dict[str, Any]] = None,
    ) -> List[Dict]:
        _ = (_zone_analysis,)
        incidents = []
        total_detections = counting_summary.get("total_count", 0)
        current_timestamp = self._get_current_timestamp_str(stream_info)
        camera_info = self.get_camera_info_from_stream(stream_info)

        self._ascending_alert_list = (
            self._ascending_alert_list[-900:] if len(self._ascending_alert_list) > 900 else self._ascending_alert_list
        )

        if total_detections > 0:
            start_timestamp = self._get_start_timestamp_str(stream_info)
            self._debug_stream_timing("start_timestamp", start_timestamp)
            if start_timestamp and self.current_incident_end_timestamp == "N/A":
                self.current_incident_end_timestamp = "Incident still active"
            elif start_timestamp and self.current_incident_end_timestamp == "Incident still active":
                if len(self._ascending_alert_list) >= 15 and sum(self._ascending_alert_list[-15:]) / 15 < 1.5:
                    self.current_incident_end_timestamp = current_timestamp
            elif (
                self.current_incident_end_timestamp != "Incident still active"
                and self.current_incident_end_timestamp != "N/A"
            ):
                self.current_incident_end_timestamp = "N/A"

            if (
                config.alert_config
                and hasattr(config.alert_config, "count_thresholds")
                and config.alert_config.count_thresholds
            ):
                threshold = config.alert_config.count_thresholds.get("all", 15)
                intensity = min(10.0, (total_detections / threshold) * 10)
                if intensity >= 9:
                    level = "critical"
                    self._ascending_alert_list.append(3)
                elif intensity >= 7:
                    level = "significant"
                    self._ascending_alert_list.append(2)
                elif intensity >= 5:
                    level = "medium"
                    self._ascending_alert_list.append(1)
                else:
                    level = "low"
                    self._ascending_alert_list.append(0)
            else:
                if total_detections > 30:
                    level = "critical"
                    self._ascending_alert_list.append(3)
                elif total_detections > 25:
                    level = "significant"
                    self._ascending_alert_list.append(2)
                elif total_detections > 15:
                    level = "medium"
                    self._ascending_alert_list.append(1)
                else:
                    level = "low"
                    self._ascending_alert_list.append(0)

            human_text_lines = [f"RUNNING INCIDENTS DETECTED @ {current_timestamp}:"]
            human_text_lines.append(f"\tSeverity Level: {(self.CASE_TYPE, level)}")
            human_text = "\n".join(human_text_lines)

            alert_settings = []
            if config.alert_config and hasattr(config.alert_config, "alert_type"):
                alert_settings.append(
                    {
                        "alert_type": getattr(config.alert_config, "alert_type", ["Default"]),
                        "incident_category": self.CASE_TYPE,
                        "threshold_level": (
                            config.alert_config.count_thresholds
                            if hasattr(config.alert_config, "count_thresholds")
                            else {}
                        ),
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

            event = self.create_incident(
                incident_id=f"{self.CASE_TYPE}_{frame_number}",
                incident_type=self.CASE_TYPE,
                severity_level=level,
                human_text=human_text,
                camera_info=camera_info,
                alerts=alerts,
                alert_settings=alert_settings,
                start_time=start_timestamp,
                end_time=self.current_incident_end_timestamp,
                level_settings={"low": 1, "medium": 3, "significant": 4, "critical": 7},
            )
            incidents.append(event)
        else:
            self._ascending_alert_list.append(0)
            incidents.append({})
        return incidents

    def _generate_tracking_stats(
        self,
        counting_summary,
        _zone_analysis,
        alerts,
        _config,
        _frame_number,
        stream_info,
    ) -> List[Dict]:
        """Generate tracking statistics for confirmed running detections."""
        _ = (_config, _frame_number, _zone_analysis)
        total_counts_dict = counting_summary.get("total_counts", {})
        per_cat = counting_summary.get("per_category_count", {})
        new_counts = self.get_new_counts_this_frame()

        total_counts = [{"category": cat, "count": total_counts_dict.get(cat, 0)} for cat in self.target_categories]
        current_counts = [{"category": cat, "count": per_cat.get(cat, 0)} for cat in self.target_categories]
        current_new_counts = [{"category": cat, "count": new_counts.get(cat, 0)} for cat in self.target_categories]

        detections = []
        for det in counting_summary.get("detections", []):
            bbox = det.get("bounding_box", {})
            category = det.get("category", "running")
            det_obj = self.create_detection_object(category, bbox)
            detections.append(det_obj)

        current_ts = self._get_current_timestamp_str(stream_info, _precision=False)
        start_ts = self._get_start_timestamp_str(stream_info, _precision=False)

        human_lines = [
            f"CURRENT FRAME @ {current_ts}:",
            f"\t- Running Detected: {per_cat.get('running', 0)}",
            f"TOTAL SINCE {start_ts}:",
            f"\t- Total Running Events: {total_counts_dict.get('running', 0)}",
        ]

        tracking_stat = self.create_tracking_stats(
            total_counts=total_counts,
            current_counts=current_counts,
            detections=detections,
            human_text="\n".join(human_lines),
            camera_info=self.get_camera_info_from_stream(stream_info),
            alerts=alerts,
            alert_settings=[],
            reset_settings=[
                {
                    "interval_type": "daily",
                    "reset_time": {"value": 9, "time_unit": "hour"},
                }
            ],
            start_time=self._get_current_timestamp_str(stream_info, _precision=True),
            reset_time=self._get_start_timestamp_str(stream_info, _precision=True),
        )
        tracking_stat["target_categories"] = self.target_categories
        tracking_stat["current_new_counts"] = current_new_counts
        return [tracking_stat]

    def _generate_business_analytics(self, *_args, is_empty=False, **_kwargs) -> List[Dict]:
        _ = (_args, _kwargs, is_empty)
        return []

    def _generate_summary(
        self,
        _summary,
        _zone_analysis,
        _incidents,
        tracking_stats,
        _business_analytics,
        _alerts,
    ) -> List[str]:
        _ = (_alerts, _business_analytics, _incidents, _summary, _zone_analysis)
        lines = [f"Application: {self.CASE_TYPE} v{self.CASE_VERSION}"]
        if tracking_stats:
            lines.append(tracking_stats[0].get("human_text", ""))
        return ["\n".join(lines)]

    def _format_timestamp(self, ts: Any) -> str:
        if isinstance(ts, (int, float)):
            return datetime.fromtimestamp(ts, timezone.utc).strftime("%Y:%m:%d %H:%M:%S")
        if isinstance(ts, str):
            ts = ts.replace(" UTC", "").strip()
            if "." in ts:
                ts = ts.split(".")[0]
            parts = ts.split("-")
            if len(parts) >= 4:
                return f"{parts[0]}:{parts[1]}:{parts[2]} {'-'.join(parts[3:])}"
        return str(ts)

    def _get_current_timestamp_str(self, stream_info, _precision=False, _frame_id=None) -> str:
        _ = (_frame_id, _precision)
        if not stream_info:
            return "00:00:00.00"
        st = stream_info.get("input_settings", {}).get("stream_time", "NA")
        return self._format_timestamp(st) if st != "NA" else datetime.now(timezone.utc).strftime("%Y:%m:%d %H:%M:%S")

    def _get_start_timestamp_str(self, stream_info, _precision=False) -> str:
        _ = (_precision,)
        if self.start_timer:
            return self._format_timestamp(self.start_timer)
        if stream_info:
            st = stream_info.get("input_settings", {}).get("stream_time")
            if st and st != "NA":
                self.start_timer = st
                return self._format_timestamp(st)
        self.start_timer = datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")
        return self._format_timestamp(self.start_timer)

    def _merge_or_register_track(self, raw_id: Any, bbox: Any) -> Any:
        if raw_id is None or bbox is None:
            return raw_id
        now = time.time()
        if raw_id in self._track_aliases:
            cid = self._track_aliases[raw_id]
            if cid in self._canonical_tracks:
                self._canonical_tracks[cid].update({"last_bbox": bbox, "last_update": now})
                self._canonical_tracks[cid]["raw_ids"].add(raw_id)
            return cid
        for cid, info in self._canonical_tracks.items():
            if now - info["last_update"] > self._track_merge_time_window:
                continue
            if self._compute_iou(bbox, info["last_bbox"]) >= self._track_merge_iou_threshold:
                self._track_aliases[raw_id] = cid
                info.update({"last_bbox": bbox, "last_update": now})
                info["raw_ids"].add(raw_id)
                return cid
        self._track_aliases[raw_id] = raw_id
        self._canonical_tracks[raw_id] = {
            "last_bbox": bbox,
            "last_update": now,
            "raw_ids": {raw_id},
        }
        return raw_id

    def _compute_iou(self, b1: Any, b2: Any) -> float:
        def to_list(b):
            if isinstance(b, list):
                return b[:4]
            if isinstance(b, dict):
                if "xmin" in b:
                    return [b["xmin"], b["ymin"], b["xmax"], b["ymax"]]
                if "x1" in b:
                    return [b["x1"], b["y1"], b["x2"], b["y2"]]
            return []

        l1, l2 = to_list(b1), to_list(b2)
        if len(l1) < 4 or len(l2) < 4:
            return 0.0
        xi = max(l1[0], l2[0])
        yi = max(l1[1], l2[1])
        xa = min(l1[2], l2[2])
        ya = min(l1[3], l2[3])
        inter = max(0, xa - xi) * max(0, ya - yi)
        a1 = (l1[2] - l1[0]) * (l1[3] - l1[1])
        a2 = (l2[2] - l2[0]) * (l2[3] - l2[1])
        return inter / (a1 + a2 - inter) if (a1 + a2 - inter) > 0 else 0.0
