import math
import time
from collections import defaultdict, deque
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

import numpy as np

from ..core.base import (
    BaseProcessor,
    ConfigProtocol,
    ProcessingContext,
    ProcessingResult,
)
from ..core.config import AlertConfig, BaseConfig, ZoneConfig
from ..utils import (
    apply_category_mapping,
    filter_by_confidence,
    match_results_structure,
)
from ..utils.geometry_utils import point_in_polygon


class TrajectoryCorrector:
    """
    Handles Velocity-Fusion logic to correct model orientation errors.
    Stores history of track centers and applies EMA smoothing.
    """

    def __init__(self):
        # track_id -> { "centers": deque, "smooth_angle": float }
        self.history = defaultdict(
            lambda: {
                "centers": deque(maxlen=10),
                "angles": deque(maxlen=5),
                "smooth_angle": None,
            }
        )

    def get_direction_label(self, angle):
        """
        Your custom logic for Front/Back/Left/Right
        """
        if angle is None:
            return "unknown"
        angle = angle % 360
        if 45 <= angle < 135:
            return "back"
        elif 135 <= angle < 225:
            return "left"
        elif 225 <= angle < 315:
            return "front"
        else:
            return "right"

    def update_and_get_label(self, track_id, center, raw_angle_deg):
        """
        1. Fixes Angle (+90)
        2. Calculates Velocity
        3. Applies EMA Smoothing
        4. Returns (Smooth_Angle, Label_String)
        """
        state = self.history[track_id]
        state["centers"].append(center)

        # --- FIX 1: ROTATE MODEL ANGLE ---
        if raw_angle_deg is None:
            raw_angle_deg = 0.0
        fixed_raw_angle = (raw_angle_deg + 90) % 360
        state["angles"].append(fixed_raw_angle)

        # --- FIX 2: CALCULATE VELOCITY ---
        motion_angle = self._compute_motion_angle(state["centers"])

        # Decide Target Angle
        if motion_angle is not None:
            target_angle = motion_angle
        else:
            target_angle = fixed_raw_angle

        # --- FIX 3: EMA SMOOTHING ---
        alpha = 0.2

        if state["smooth_angle"] is None:
            state["smooth_angle"] = target_angle
        else:
            prev_rad = math.radians(state["smooth_angle"])
            curr_rad = math.radians(target_angle)

            new_sin = (1 - alpha) * math.sin(prev_rad) + alpha * math.sin(curr_rad)
            new_cos = (1 - alpha) * math.cos(prev_rad) + alpha * math.cos(curr_rad)

            state["smooth_angle"] = math.degrees(math.atan2(new_sin, new_cos)) % 360

        final_angle = state["smooth_angle"]
        label = self.get_direction_label(final_angle)

        return final_angle, label

    def _compute_motion_angle(self, centers):
        if len(centers) < 2:
            return None

        # Look back 5 frames for stability
        lookback = min(len(centers), 5)
        x_past, y_past = centers[-lookback]
        x_now, y_now = centers[-1]

        dx = x_now - x_past
        dy = y_now - y_past

        # THRESHOLD: 2.5 pixels
        if math.hypot(dx, dy) < 0.5:
            return None

        return math.degrees(math.atan2(-dy, dx)) % 360


@dataclass
class CrowdflowConfig(BaseConfig):
    """Configuration for footfall use case."""

    # Smoothing configuration
    enable_smoothing: bool = False
    smoothing_algorithm: str = "observability"  # "window" or "observability"
    smoothing_window_size: int = 20
    smoothing_cooldown_frames: int = 5
    smoothing_confidence_range_factor: float = 0.5

    # Zone configuration
    zone_config: Optional[ZoneConfig] = None

    # Counting parameters
    enable_unique_counting: bool = True
    time_window_minutes: int = 60

    # Category mapping
    person_categories: List[str] = field(default_factory=lambda: ["person"])
    index_to_category: Optional[Dict[int, str]] = None

    # Alert configuration
    alert_config: Optional[AlertConfig] = None

    target_categories: List[str] = field(default_factory=lambda: ["person"])

    def validate(self) -> List[str]:
        """Validate people counting configuration."""
        errors = super().validate()

        if self.time_window_minutes <= 0:
            errors.append("time_window_minutes must be positive")

        if not self.person_categories:
            errors.append("person_categories cannot be empty")

        # Validate nested configurations
        if self.zone_config:
            errors.extend(self.zone_config.validate())

        if self.alert_config:
            errors.extend(self.alert_config.validate())

        return errors


class CrowdflowUseCase(BaseProcessor):
    # CATEGORY_DISPLAY = {
    #     "person": "Person"
    # }

    def __init__(self):
        super().__init__("crowdflow")
        self.category = "retail"
        self.CASE_TYPE: Optional[str] = "crowdflow"
        self.CASE_VERSION: Optional[str] = "1.1"
        self.target_categories = ["person", "front", "back", "left", "right"]
        self.smoothing_tracker = None
        self.tracker = None

        # -------------------------------
        # ZONE-based Crowd Flow
        # -------------------------------
        self.MIN_TRACKS_PER_GRID = 1
        self._track_trajectories = defaultdict(lambda: deque(maxlen=30))
        self._zone_trajectories = defaultdict(lambda: defaultdict(lambda: deque(maxlen=30)))

        self._zone_flow = defaultdict(
            lambda: {
                "sum_sin": 0.0,
                "sum_cos": 0.0,
                "count": 0,
                "frame_tracks": {
                    "front": set(),
                    "back": set(),
                    "left": set(),
                    "right": set(),
                },
                "window_tracks": {
                    "front": set(),
                    "back": set(),
                    "left": set(),
                    "right": set(),
                },
            }
        )

        # Initialize the Velocity Logic
        self.trajectory_corrector = TrajectoryCorrector()
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

    def _compute_avg_displacement(self, trajectories, min_len=6):
        starts, ends = [], []

        for t in trajectories:
            if len(t) >= min_len:
                starts.append(t[0])
                ends.append(t[-1])

        if not starts:
            return None

        sx = int(sum(p[0] for p in starts) / len(starts))
        sy = int(sum(p[1] for p in starts) / len(starts))
        ex = int(sum(p[0] for p in ends) / len(ends))
        ey = int(sum(p[1] for p in ends) / len(ends))

        dx, dy = ex - sx, ey - sy
        angle = math.degrees(math.atan2(-dy, dx)) % 360

        return {
            "start": (sx, sy),
            "end": (ex, ey),
            "angle": angle,
            "track_count": len(starts),
        }

    def process(
        self,
        data: Any,
        config: ConfigProtocol,
        context: Optional[ProcessingContext] = None,
        stream_info: Optional[Dict[str, Any]] = None,
    ) -> ProcessingResult:
        processing_start = time.time()
        if not isinstance(config, CrowdflowConfig):
            return self.create_error_result(
                "Invalid config type",
                usecase=self.name,
                category=self.category,
                context=context,
            )
        if context is None:
            context = ProcessingContext()

        fps = 25
        if stream_info:
            fps = stream_info.get("input_settings", {}).get("original_fps", 25)

        decay_interval = int(2 * fps)

        # -------------------------------
        # Resolve Zones
        # -------------------------------
        zones = {}

        if config.zone_config and config.zone_config.zones:
            zones = config.zone_config.zones
        else:
            # Fallback: full frame as single zone
            zones = {"__full_frame__": None}

        # Temporal decay of window tracks (~2 sec behavior)
        if self._total_frame_counter % decay_interval == 0:
            for cell in self._zone_flow.values():
                for d in cell["window_tracks"]:
                    cell["window_tracks"][d] = {tid for tid in cell["window_tracks"][d] if np.random.rand() < 0.90}

        # Reset per-frame snapshot FIRST
        for cell in self._zone_flow.values():
            for d in cell["frame_tracks"]:
                cell["frame_tracks"][d].clear()

        # Then apply temporal decay
        for cell in self._zone_flow.values():
            cell["sum_sin"] *= 0.92
            cell["sum_cos"] *= 0.92
            cell["count"] *= 0.92

        input_format = match_results_structure(data)
        context.input_format = input_format
        context.confidence_threshold = config.confidence_threshold

        # ... [Keep your standard filtering logic here: confidence, mapping, categories] ...
        if config.confidence_threshold is not None:
            processed_data = filter_by_confidence(data, config.confidence_threshold)
        else:
            processed_data = data

        if config.index_to_category:
            processed_data = apply_category_mapping(processed_data, config.index_to_category)

        if config.target_categories:
            processed_data = [d for d in processed_data if d.get("category") in self.target_categories]

        try:
            from ..advanced_tracker import AdvancedTracker
            from ..advanced_tracker.config import TrackerConfig

            if self.tracker is None:
                tracker_config = TrackerConfig(
                    track_high_thresh=0.4,
                    track_low_thresh=0.05,
                    new_track_thresh=0.3,
                    match_thresh=0.8,
                )
                self.tracker = AdvancedTracker(tracker_config)
                self.logger.info("Initialized AdvancedTracker for People Counting")

            # 1. Run Standard Tracker (Assigns IDs)
            processed_data = self.tracker.update(processed_data)

            # =========================================================
            # NEW: INJECT VELOCITY FUSION LOGIC (CORRECTED)
            # =========================================================
            for det in processed_data:
                track_id = det.get("track_id")

                # STREAM-SAFE bbox normalization
                bbox = det.get("bbox") or det.get("bounding_box")

                if isinstance(bbox, dict):
                    bbox = [
                        bbox.get("xmin"),
                        bbox.get("ymin"),
                        bbox.get("xmax"),
                        bbox.get("ymax"),
                    ]

                # Hard safety guard
                if not bbox or len(bbox) < 4:
                    continue

                # Check for 'raw_angle' (from predict.py) or 'orientation'
                raw_angle = det.get("angle", det.get("raw_angle", det.get("orientation", 0.0)))

                if track_id is not None and bbox:
                    # Calculate Center (cx, cy)
                    cx = int((bbox[0] + bbox[2]) / 2)
                    cy = int((bbox[1] + bbox[3]) / 2)

                    # Run Correction (Velocity + EMA + 90 Fix)
                    # FIX: Unpack both values (Angle AND Label)
                    final_angle, direction_label = self.trajectory_corrector.update_and_get_label(
                        track_id, (cx, cy), raw_angle
                    )

                    # OVERWRITE the detection angle
                    det["orientation"] = final_angle  # For UI
                    det["angle"] = final_angle  # For Analytics

                    # FIX: SAVE THE DIRECTION LABEL
                    det["category"] = direction_label
                    det["direction"] = direction_label  # "front", "back", etc.

                    # -------------------------------
                    # Assign detection to zone
                    # -------------------------------
                    assigned_zone = None

                    if "__full_frame__" in zones:
                        assigned_zone = "__full_frame__"
                    else:
                        for zone_name, polygon in zones.items():
                            polygon_points = [(p[0], p[1]) for p in polygon]
                            if point_in_polygon((cx, cy), polygon_points):
                                assigned_zone = zone_name
                                break

                    if assigned_zone is None:
                        continue  # outside all zones

                    self._zone_trajectories[assigned_zone][track_id].append((cx, cy))
                    cell = self._zone_flow[assigned_zone]

                    rad = math.radians(final_angle)
                    cell["sum_cos"] += math.cos(rad)
                    cell["sum_sin"] += math.sin(rad)
                    cell["count"] += 1

                    cell["frame_tracks"][direction_label].add(track_id)
                    cell["window_tracks"][direction_label].add(track_id)

            # =========================================================

        except Exception as e:
            self.logger.warning(f"AdvancedTracker/Velocity failed: {e}")

        # ... [The rest of your process method remains exactly the same] ...
        # CLEAN DEAD TRACKS (CRITICAL – prevents memory leak)
        # ---------------------------------------------------------

        # Zone clean up
        alive_ids = {d.get("track_id") for d in processed_data if d.get("track_id") is not None}

        for zone in list(self._zone_trajectories.keys()):
            for tid in list(self._zone_trajectories[zone].keys()):
                if tid not in alive_ids:
                    del self._zone_trajectories[zone][tid]

        # Clean global trajectory memory
        for tid in list(self._track_trajectories.keys()):
            if tid not in alive_ids:
                self._track_trajectories.pop(tid, None)

        self._update_tracking_state(processed_data)

        frame_number = None
        if stream_info:
            input_settings = stream_info.get("input_settings", {})
            start_frame = input_settings.get("start_frame")
            end_frame = input_settings.get("end_frame")
            if start_frame is not None and end_frame is not None and start_frame == end_frame:
                frame_number = start_frame

        counting_summary = self._count_categories(processed_data, config)
        total_counts = self.get_total_counts()
        counting_summary["total_counts"] = total_counts

        alerts = self._check_alerts(counting_summary, frame_number, config)
        self._extract_predictions(processed_data)
        incidents_list = self._generate_incidents(counting_summary, alerts, config, frame_number, stream_info)
        tracking_stats_list = self._generate_tracking_stats(counting_summary, alerts, config, frame_number, stream_info)
        business_analytics_list = self._generate_business_analytics(
            counting_summary, alerts, config, stream_info, is_empty=True
        )
        summary_list = self._generate_summary(
            counting_summary,
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
        processing_latency_ms = proc_time * 1000.0
        processing_fps = (1.0 / proc_time) if proc_time > 0 else None
        # Log the performance metrics using the module-level logger
        self._total_frame_counter += 1
        print(
            "latency in ms:",
            processing_latency_ms,
            "| Throughput fps:",
            processing_fps,
            "| Frame_Number:",
            self._total_frame_counter,
        )
        return result

    def _check_alerts(self, summary: dict, frame_number: Any, config: CrowdflowConfig) -> List[Dict]:
        def get_trend(data, lookback=900, threshold=0.6):
            window = data[-lookback:] if len(data) >= lookback else data
            if len(window) < 2:
                return True
            increasing = 0
            total = 0
            for i in range(1, len(window)):
                if window[i] >= window[i - 1]:
                    increasing += 1
                total += 1
            ratio = increasing / total
            return ratio >= threshold

        frame_key = str(frame_number) if frame_number is not None else "current_frame"
        alerts = []
        total_detections = summary.get("total_count", 0)
        per_category_count = summary.get("per_category_count", {})

        if not config.alert_config:
            return alerts

        if hasattr(config.alert_config, "count_thresholds") and config.alert_config.count_thresholds:
            for category, threshold in config.alert_config.count_thresholds.items():
                if category == "all" and total_detections > threshold:
                    alerts.append(
                        {
                            "alert_type": getattr(config.alert_config, "alert_type", ["Default"]),
                            "alert_id": f"alert_{category}_{frame_key}",
                            "incident_category": self.CASE_TYPE,
                            "threshold_level": threshold,
                            "ascending": get_trend(self._ascending_alert_list, lookback=900, threshold=0.8),
                            "settings": {
                                t: v
                                for t, v in zip(
                                    getattr(config.alert_config, "alert_type", ["Default"]),
                                    getattr(config.alert_config, "alert_value", ["JSON"]),
                                )
                            },
                        }
                    )
                elif category in per_category_count and per_category_count[category] > threshold:
                    alerts.append(
                        {
                            "alert_type": getattr(config.alert_config, "alert_type", ["Default"]),
                            "alert_id": f"alert_{category}_{frame_key}",
                            "incident_category": self.CASE_TYPE,
                            "threshold_level": threshold,
                            "ascending": get_trend(self._ascending_alert_list, lookback=900, threshold=0.8),
                            "settings": {
                                t: v
                                for t, v in zip(
                                    getattr(config.alert_config, "alert_type", ["Default"]),
                                    getattr(config.alert_config, "alert_value", ["JSON"]),
                                )
                            },
                        }
                    )
        return alerts

    def _generate_incidents(
        self,
        counting_summary: Dict,
        alerts: List,
        config: CrowdflowConfig,
        frame_number: Optional[int] = None,
        stream_info: Optional[Dict[str, Any]] = None,
    ) -> List[Dict]:
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

            if config.alert_config and config.alert_config.count_thresholds:
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

            human_text_lines = [f"COUNTING INCIDENTS DETECTED @ {current_timestamp}:"]
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
        counting_summary: Dict,
        alerts: List,
        config: CrowdflowConfig,
        _frame_number: Optional[int] = None,
        stream_info: Optional[Dict[str, Any]] = None,
    ) -> List[Dict]:
        _ = (_frame_number,)
        camera_info = self.get_camera_info_from_stream(stream_info)
        tracking_stats = []
        total_detections = counting_summary.get("total_count", 0)
        total_counts_dict = counting_summary.get("total_counts", {})
        per_category_count = counting_summary.get("per_category_count", {})
        current_timestamp = self._get_current_timestamp_str(stream_info, precision=False)
        start_timestamp = self._get_start_timestamp_str(stream_info, precision=False)
        self._debug_stream_timing("start_timestamp", start_timestamp)
        high_precision_start_timestamp = self._get_current_timestamp_str(stream_info, precision=True)
        high_precision_reset_timestamp = self._get_start_timestamp_str(stream_info, precision=True)

        total_counts = [{"category": cat, "count": count} for cat, count in total_counts_dict.items() if count > 0]
        current_counts = [
            {"category": cat, "count": count}
            for cat, count in per_category_count.items()
            if count > 0 or total_detections > 0
        ]

        detections = []
        for detection in counting_summary.get("detections", []):
            bbox = detection.get("bounding_box", {})
            category = detection.get("category", "person")
            if detection.get("masks"):
                segmentation = detection.get("masks", [])
                detection_obj = self.create_detection_object(category, bbox, segmentation=segmentation)
            elif detection.get("segmentation"):
                segmentation = detection.get("segmentation")
                detection_obj = self.create_detection_object(category, bbox, segmentation=segmentation)
            elif detection.get("mask"):
                segmentation = detection.get("mask")
                detection_obj = self.create_detection_object(category, bbox, segmentation=segmentation)
            else:
                detection_obj = self.create_detection_object(category, bbox)
            detections.append(detection_obj)

        alert_settings = []
        if config.alert_config and hasattr(config.alert_config, "alert_type"):
            alert_settings.append(
                {
                    "alert_type": getattr(config.alert_config, "alert_type", ["Default"]),
                    "incident_category": self.CASE_TYPE,
                    "threshold_level": (
                        config.alert_config.count_thresholds if hasattr(config.alert_config, "count_thresholds") else {}
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

        human_text_lines = []
        human_text_lines.append(f"CURRENT FRAME @ {current_timestamp}:")
        for cat, count in per_category_count.items():
            human_text_lines.append(f"\t- People Detected: {count}")
        human_text_lines.append("")
        human_text = "\n".join(human_text_lines)

        reset_settings = [{"interval_type": "daily", "reset_time": {"value": 9, "time_unit": "hour"}}]
        tracking_stat = self.create_tracking_stats(
            total_counts=total_counts,
            current_counts=current_counts,
            detections=detections,
            human_text=human_text,
            camera_info=camera_info,
            alerts=alerts,
            alert_settings=alert_settings,
            reset_settings=reset_settings,
            start_time=high_precision_start_timestamp,
            reset_time=high_precision_reset_timestamp,
        )
        # -------------------------------
        # Crowd Flow Aggregation ## Zones
        # -------------------------------

        crowd_flow = []

        for zone_name, tracks in self._zone_trajectories.items():
            avg = self._compute_avg_displacement(tracks.values())
            if not avg or avg["track_count"] < self.MIN_TRACKS_PER_GRID:
                continue

            cell = self._zone_flow[zone_name]

            front = len(cell["window_tracks"]["front"])
            back = len(cell["window_tracks"]["back"])
            left = len(cell["window_tracks"]["left"])
            right = len(cell["window_tracks"]["right"])

            conflict = (front >= self.MIN_TRACKS_PER_GRID and back >= self.MIN_TRACKS_PER_GRID) or (
                left >= self.MIN_TRACKS_PER_GRID and right >= self.MIN_TRACKS_PER_GRID
            )

            avg_direction_angle = None
            if cell["count"] >= self.MIN_TRACKS_PER_GRID:
                avg_direction_angle = math.degrees(math.atan2(cell["sum_sin"], cell["sum_cos"])) % 360

            crowd_flow.append(
                {
                    "zone": zone_name,
                    "conflict": conflict,
                    "avg_displacement": {
                        "start": avg["start"],
                        "end": avg["end"],
                        "angle": avg["angle"],
                        "track_count": avg["track_count"],
                    },
                    "direction_flow": {
                        "avg_angle": avg_direction_angle,
                        "counts": {
                            "front": len(cell["frame_tracks"]["front"]),
                            "back": len(cell["frame_tracks"]["back"]),
                            "left": len(cell["frame_tracks"]["left"]),
                            "right": len(cell["frame_tracks"]["right"]),
                        },
                    },
                }
            )

        tracking_stat["crowd_flow"] = crowd_flow

        tracking_stat["target_categories"] = self.target_categories
        tracking_stats.append(tracking_stat)
        return tracking_stats

    def _generate_business_analytics(
        self,
        _counting_summary: Dict,
        _alerts: Any,
        _config: CrowdflowConfig,
        _stream_info: Optional[Dict[str, Any]] = None,
        is_empty=False,
    ) -> List[Dict]:
        _ = (_alerts, _config, _counting_summary, _stream_info)
        if is_empty:
            return []

        return None

    def _generate_summary(
        self,
        _summary: dict,
        incidents: List,
        tracking_stats: List,
        business_analytics: List,
        _alerts: List,
    ) -> List[str]:
        """
        Generate a human_text string for the tracking_stat, incident, business analytics and alerts.
        """
        _ = (_alerts, _summary)
        lines = []
        lines.append("Application Name: " + self.CASE_TYPE)
        lines.append("Application Version: " + self.CASE_VERSION)
        if len(tracking_stats) > 0:
            lines.append(
                "Tracking Statistics: " + f"\t{tracking_stats[0].get('human_text', 'No tracking statistics detected')}"
            )
        if len(business_analytics) > 0:
            lines.append(
                "Business Analytics: "
                + f"\t{business_analytics[0].get('human_text', 'No business analytics detected')}"
            )

        if len(incidents) == 0 and len(tracking_stats) == 0 and len(business_analytics) == 0:
            lines.append("Summary: " + "No Summary Data")

        return ["\n".join(lines)]

    def _get_track_ids_info(self, detections: list) -> Dict[str, Any]:
        frame_track_ids = set()
        for det in detections:
            tid = det.get("track_id")
            if tid is not None:
                frame_track_ids.add(tid)
        total_track_ids = set()
        for s in getattr(self, "_per_category_total_track_ids", {}).values():
            total_track_ids.update(s)
        return {
            "total_count": len(total_track_ids),
            "current_frame_count": len(frame_track_ids),
            "total_unique_track_ids": len(total_track_ids),
            "current_frame_track_ids": list(frame_track_ids),
            "last_update_time": time.time(),
            "total_frames_processed": getattr(self, "_total_frame_counter", 0),
        }

    def _update_tracking_state(self, detections: list):
        if not hasattr(self, "_per_category_total_track_ids"):
            self._per_category_total_track_ids = {cat: set() for cat in self.target_categories}
        self._current_frame_track_ids = {cat: set() for cat in self.target_categories}

        for det in detections:
            cat = det.get("category")
            raw_track_id = det.get("track_id")
            if cat not in self.target_categories or raw_track_id is None:
                continue
            bbox = det.get("bbox") or det.get("bounding_box")

            if isinstance(bbox, dict):
                bbox = [
                    bbox.get("xmin"),
                    bbox.get("ymin"),
                    bbox.get("xmax"),
                    bbox.get("ymax"),
                ]

            if not bbox or len(bbox) < 4:
                continue

            canonical_id = self._merge_or_register_track(raw_track_id, bbox)

            det["track_id"] = canonical_id
            self._per_category_total_track_ids.setdefault(cat, set()).add(canonical_id)
            self._current_frame_track_ids[cat].add(canonical_id)

    def get_total_counts(self):
        return {cat: len(ids) for cat, ids in getattr(self, "_per_category_total_track_ids", {}).items()}

    def _format_timestamp_for_stream(self, timestamp: float) -> str:
        dt = datetime.fromtimestamp(timestamp, tz=timezone.utc)
        return dt.strftime("%Y:%m:%d %H:%M:%S")

    def _format_timestamp_for_video(self, timestamp: float) -> str:
        hours = int(timestamp // 3600)
        minutes = int((timestamp % 3600) // 60)
        seconds = round(float(timestamp % 60), 2)
        return f"{hours:02d}:{minutes:02d}:{seconds:.1f}"

    def _format_timestamp(self, timestamp: Any) -> str:
        """Format a timestamp to match the current timestamp format: YYYY:MM:DD HH:MM:SS.

        The input can be either:
        1. A numeric Unix timestamp (``float`` / ``int``) – it will be converted to datetime.
        2. A string in the format ``YYYY-MM-DD-HH:MM:SS.ffffff UTC``.

        The returned value will be in the format: YYYY:MM:DD HH:MM:SS (no milliseconds, no UTC suffix).

        Example
        -------
        >>> self._format_timestamp("2025-10-27-19:31:20.187574 UTC")
        '2025:10:27 19:31:20'
        """

        # Convert numeric timestamps to datetime first
        if isinstance(timestamp, (int, float)):
            dt = datetime.fromtimestamp(timestamp, timezone.utc)
            return dt.strftime("%Y:%m:%d %H:%M:%S")

        # Ensure we are working with a string from here on
        if not isinstance(timestamp, str):
            return str(timestamp)

        # Remove ' UTC' suffix if present
        timestamp_clean = timestamp.replace(" UTC", "").strip()

        # Remove milliseconds if present (everything after the last dot)
        if "." in timestamp_clean:
            timestamp_clean = timestamp_clean.split(".")[0]

        # Parse the timestamp string and convert to desired format
        try:
            # Handle format: YYYY-MM-DD-HH:MM:SS
            if timestamp_clean.count("-") >= 2:
                # Replace first two dashes with colons for date part, third with space
                parts = timestamp_clean.split("-")
                if len(parts) >= 4:
                    # parts = ['2025', '10', '27', '19:31:20']
                    formatted = f"{parts[0]}:{parts[1]}:{parts[2]} {'-'.join(parts[3:])}"
                    return formatted
        except Exception:
            # Non-fatal: exception ignored here; execution continues per surrounding logic.
            pass

        # If parsing fails, return the cleaned string as-is
        return timestamp_clean

    def _get_current_timestamp_str(
        self,
        stream_info: Optional[Dict[str, Any]],
        precision=False,
        frame_id: Optional[str] = None,
    ) -> str:
        """Get formatted current timestamp based on stream type."""

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
                stream_time_str = self._format_timestamp_for_video(start_time)
                self._debug_stream_timing("stream_time_str", stream_time_str)
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

            stream_time_str = self._format_timestamp_for_video(start_time)

            self._debug_stream_timing("stream_time_str", stream_time_str)
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
        """Get formatted start timestamp for 'TOTAL SINCE' based on stream type."""
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
            # Prefer direct input_settings.stream_time if available and not NA
            candidate = stream_info.get("input_settings", {}).get("stream_time")
            if not candidate or candidate == "NA":
                # Fallback to nested stream_info.stream_time used by current timestamp path
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

    def _count_categories(self, detections: list, _config: CrowdflowConfig) -> dict:
        _ = (_config,)
        counts = {}
        for det in detections:
            cat = det.get("direction") or "unknown"
            counts[cat] = counts.get(cat, 0) + 1
        return {
            "total_count": sum(counts.values()),
            "per_category_count": counts,
            "detections": [
                {
                    "bounding_box": det.get("bounding_box"),
                    "category": det.get("category"),
                    "direction": det.get("direction"),
                    "confidence": det.get("confidence"),
                    "track_id": det.get("track_id"),
                    "frame_id": det.get("frame_id"),
                    "angle": det.get("angle"),
                    "orientation": det.get("orientation"),  # for UI arrows
                }
                for det in detections
            ],
        }

    def _extract_predictions(self, detections: list) -> List[Dict[str, Any]]:
        return [
            {
                "category": det.get("category", "unknown"),
                "confidence": det.get("confidence", 0.0),
                "bounding_box": det.get("bounding_box", {}),
            }
            for det in detections
        ]

    def _compute_iou(self, box1: Any, box2: Any) -> float:
        def _bbox_to_list(bbox):
            if bbox is None:
                return []
            if isinstance(bbox, list):
                return bbox[:4] if len(bbox) >= 4 else []
            if isinstance(bbox, dict):
                if "xmin" in bbox:
                    return [bbox["xmin"], bbox["ymin"], bbox["xmax"], bbox["ymax"]]
                if "x1" in bbox:
                    return [bbox["x1"], bbox["y1"], bbox["x2"], bbox["y2"]]
                values = [v for v in bbox.values() if isinstance(v, (int, float))]
                return values[:4] if len(values) >= 4 else []
            return []

        l1 = _bbox_to_list(box1)
        l2 = _bbox_to_list(box2)
        if len(l1) < 4 or len(l2) < 4:
            return 0.0
        x1_min, y1_min, x1_max, y1_max = l1
        x2_min, y2_min, x2_max, y2_max = l2
        x1_min, x1_max = min(x1_min, x1_max), max(x1_min, x1_max)
        y1_min, y1_max = min(y1_min, y1_max), max(y1_min, y1_max)
        x2_min, x2_max = min(x2_min, x2_max), max(x2_min, x2_max)
        y2_min, y2_max = min(y2_min, y2_max), max(y2_min, y2_max)
        inter_x_min = max(x1_min, x2_min)
        inter_y_min = max(y1_min, y2_min)
        inter_x_max = min(x1_max, x2_max)
        inter_y_max = min(y1_max, y2_max)
        inter_w = max(0.0, inter_x_max - inter_x_min)
        inter_h = max(0.0, inter_y_max - inter_y_min)
        inter_area = inter_w * inter_h
        area1 = (x1_max - x1_min) * (y1_max - y1_min)
        area2 = (x2_max - x2_min) * (y2_max - y2_min)
        union_area = area1 + area2 - inter_area
        return (inter_area / union_area) if union_area > 0 else 0.0

    def _merge_or_register_track(self, raw_id: Any, bbox: Any) -> Any:
        if raw_id is None or bbox is None:
            return raw_id
        now = time.time()
        if raw_id in self._track_aliases:
            canonical_id = self._track_aliases[raw_id]
            track_info = self._canonical_tracks.get(canonical_id)
            if track_info is not None:
                track_info["last_bbox"] = bbox
                track_info["last_update"] = now
                track_info["raw_ids"].add(raw_id)
            return canonical_id
        for canonical_id, info in self._canonical_tracks.items():
            if now - info["last_update"] > self._track_merge_time_window:
                continue
            iou = self._compute_iou(bbox, info["last_bbox"])
            if iou >= self._track_merge_iou_threshold:
                self._track_aliases[raw_id] = canonical_id
                info["last_bbox"] = bbox
                info["last_update"] = now
                info["raw_ids"].add(raw_id)
                return canonical_id
        canonical_id = raw_id
        self._track_aliases[raw_id] = canonical_id
        self._canonical_tracks[canonical_id] = {
            "last_bbox": bbox,
            "last_update": now,
            "raw_ids": {raw_id},
        }
        return canonical_id

    def _get_tracking_start_time(self) -> str:
        if self._tracking_start_time is None:
            return "N/A"
        return self._format_timestamp(self._tracking_start_time)

    def _set_tracking_start_time(self) -> None:
        self._tracking_start_time = time.time()
