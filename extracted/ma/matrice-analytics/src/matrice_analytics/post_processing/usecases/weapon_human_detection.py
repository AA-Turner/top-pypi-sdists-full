"""
Weapon Human Detection Use Case for Post-Processing.

Model classes:
- 0: weapon
- 1: human

Incidents, alerts, and weapon counts use weapon detections only.
Human boxes can be included in tracking output for visualization via ``include_humans_in_output``.
"""

import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Set, Tuple

from ..core.base import (
    BaseProcessor,
    ConfigProtocol,
    ProcessingContext,
    ProcessingResult,
)
from ..core.config import AlertConfig, BaseConfig
from ..Trackers import ConfigDrivenTracker, TrackerProfile
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
from ..utils.weapon_human_filter import apply_weapon_human_frame_filter


@dataclass
class WeaponHumanDetectionConfig(BaseConfig):
    """Configuration for weapon + human detection post-processing (best (2).pt)."""

    enable_smoothing: bool = True
    smoothing_algorithm: str = "observability"
    smoothing_window_size: int = 20
    smoothing_cooldown_frames: int = 5
    smoothing_confidence_range_factor: float = 0.5

    confidence_threshold: float = 0.28
    enable_class_aggregation: bool = False
    class_aggregation_window_size: int = 30

    zone_config: Optional[Dict[str, List[List[float]]]] = None

    enable_weapon_human_filter: bool = True
    human_category_names: List[str] = field(default_factory=lambda: ["human", "person"])
    weapon_categories: List[str] = field(default_factory=lambda: ["weapon"])
    max_weapon_to_human_area_ratio: float = 0.40

    usecase_categories: List[str] = field(default_factory=lambda: ["weapon", "human"])
    # Incidents/alerts/counts use weapon only; humans are optional in bbox output.
    target_categories: List[str] = field(default_factory=lambda: ["weapon"])
    include_humans_in_output: bool = True

    alert_config: Optional[AlertConfig] = field(default_factory=lambda: AlertConfig(count_thresholds={"weapon": 0}))

    index_to_category: Optional[Dict[int, str]] = field(
        default_factory=lambda: {
            0: "weapon",
            1: "human",
        }
    )


class WeaponHumanDetectionUseCase(BaseProcessor):
    CATEGORY_DISPLAY = {"weapon": "Weapon", "human": "Human"}

    def __init__(self):
        super().__init__("weapon_human_detection")
        self.category = "security"
        self.CASE_TYPE: Optional[str] = "weapon_human_detection"
        self.CASE_VERSION: Optional[str] = "1.0"

        # Weapon-only for incidents, alerts, and cumulative tracking counts.
        self.target_categories = ["weapon"]
        self._human_display_detections: List[Dict[str, Any]] = []

        self.smoothing_tracker = None
        self.tracker = None
        self._tracker_seam = ConfigDrivenTracker()
        self._total_frame_counter = 0
        self._global_frame_offset = 0
        self._tracking_start_time = None
        self._track_aliases: Dict[Any, Any] = {}
        self._canonical_tracks: Dict[Any, Dict[str, Any]] = {}
        self._track_merge_iou_threshold: float = 0.8
        self._track_merge_time_window: float = 7.0
        self._ascending_alert_list: List[int] = []
        self.current_incident_end_timestamp: str = "N/A"
        self.start_timer = None

        # Track ID storage for total count calculation
        self._per_category_total_track_ids = {cat: set() for cat in self.target_categories}
        self._current_frame_track_ids = {cat: set() for cat in self.target_categories}
        self._tracked_in_zones = set()  # New: Unique track IDs that have entered any zone
        self._total_count = 0  # Cached total count
        self._last_update_time = time.time()  # Track when last updated
        self._total_count_list = []

        # Zone-based tracking storage
        self._zone_current_track_ids = {}  # zone_name -> set of current track IDs in zone
        self._zone_total_track_ids = {}  # zone_name -> set of all track IDs that have been in zone
        self._zone_current_counts = {}  # zone_name -> current count in zone
        self._zone_total_counts = {}  # zone_name -> total count that have been in zone

    def process(
        self,
        data: Any,
        config: ConfigProtocol,
        context: Optional[ProcessingContext] = None,
        stream_info: Optional[Dict[str, Any]] = None,
    ) -> ProcessingResult:
        processing_start = time.time()
        is_valid_config = isinstance(config, WeaponHumanDetectionConfig) or (
            hasattr(config, "usecase")
            and config.usecase == "weapon_human_detection"
            and hasattr(config, "category")
            and config.category == "security"
        )
        if not is_valid_config:
            self.logger.error(
                f"Config validation failed in weapon_human_detection. "
                f"Got type={type(config).__name__}, module={type(config).__module__}, "
                f"usecase={getattr(config, 'usecase', 'N/A')}, category={getattr(config, 'category', 'N/A')}"
            )
            return self.create_error_result(
                f"Invalid config type: expected WeaponHumanDetectionConfig or config with usecase='weapon_human_detection' "
                f"got {type(config).__name__} with usecase={getattr(config, 'usecase', 'N/A')}",
                usecase=self.name,
                category=self.category,
                context=context,
            )
        if context is None:
            context = ProcessingContext()
        has_zones = bool(config.zone_config and config.zone_config.get("zones"))
        # Normalize common YOLO payloads (cls/conf/xyxy/xywh) to internal schema.
        data = self._normalize_yolo_results(data, getattr(config, "index_to_category", None))
        self.logger.debug(f"[weapon_human_detection] normalized_input={data}")
        input_format = match_results_structure(data)
        context.input_format = input_format
        context.confidence_threshold = config.confidence_threshold

        if config.confidence_threshold is not None:
            processed_data = filter_by_confidence(data, config.confidence_threshold)
            self.logger.debug(f"Applied confidence filtering with threshold {config.confidence_threshold}")
        else:
            processed_data = data
            self.logger.debug("Did not apply confidence filtering since no threshold provided")

        # Map model indices to category names.
        if config.index_to_category:
            processed_data = apply_category_mapping(processed_data, config.index_to_category)

        processed_data = self._canonicalize_categories(processed_data)

        if getattr(config, "enable_weapon_human_filter", True) and isinstance(processed_data, list):
            weapon_set: Set[str] = {str(c).lower() for c in getattr(config, "weapon_categories", ["weapon"])}
            human_set: Set[str] = {str(c).lower() for c in getattr(config, "human_category_names", ["human", "person"])}
            ratio = float(getattr(config, "max_weapon_to_human_area_ratio", 0.40))
            processed_data = apply_weapon_human_frame_filter(
                processed_data,
                weapon_categories=weapon_set,
                human_categories=human_set,
                max_weapon_to_human_area_ratio=ratio,
            )

        self._human_display_detections = []
        if getattr(config, "include_humans_in_output", True) and isinstance(processed_data, list):
            human_set = {str(c).lower() for c in getattr(config, "human_category_names", ["human", "person"])}
            self._human_display_detections = [
                det for det in processed_data if str(det.get("category", "")).lower() in human_set
            ]

        # Keep only weapon for incidents, alerts, tracking counts, and weapon pipeline.
        if config.target_categories:
            processed_data = [d for d in processed_data if d.get("category") in config.target_categories]
            self.logger.debug("Applied category mapping")

        processed_data = [d for d in processed_data if d.get("category") in self.target_categories]
        if config.target_categories:
            processed_data = [d for d in processed_data if d.get("category") in self.target_categories]
            self.logger.debug("Applied category filtering")

        for det in processed_data:
            if not isinstance(det, dict):
                continue
            if det.get("track_id") is not None:
                continue
            for key in (
                "tracker_id",
                "tracking_id",
                "trackId",
                "trackID",
                "id",
                "object_id",
            ):
                candidate = det.get(key)
                if candidate is not None:
                    det["track_id"] = candidate
                    break
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

        # Track detections for stable IDs and cumulative unique counting.
        try:
            if self.tracker is None:
                self.tracker = self._tracker_seam.get_shared_tracker(
                    stream_info=stream_info,
                    profile=TrackerProfile.LEGACY_40,
                    namespace=True,
                    restore=True,
                    max_time_lost=int(1200),
                    frame_rate=25,
                    enable_class_aggregation=config.enable_class_aggregation,
                    class_aggregation_window_size=config.class_aggregation_window_size,
                )
            processed_data = self.tracker.update(processed_data)
        except Exception as exc:
            self.logger.warning(f"AdvancedTracker failed: {exc}")

        self._update_tracking_state(processed_data, _has_zones=has_zones)
        self._total_frame_counter += 1

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
        counting_summary["categories"] = {}
        for detection in processed_data:
            category = detection.get("category", "unknown")
            counting_summary["categories"][category] = counting_summary["categories"].get(category, 0) + 1

        zone_analysis = {}
        if has_zones:
            # Convert single frame to format expected by count_objects_in_zones
            frame_data = processed_data  # [frame_detections]
            zone_analysis = count_objects_in_zones(frame_data, config.zone_config["zones"], stream_info)

            if zone_analysis:
                enhanced_zone_analysis = self._update_zone_tracking(zone_analysis, processed_data, config)
                # Merge enhanced zone analysis with original zone analysis
                for zone_name, enhanced_data in enhanced_zone_analysis.items():
                    zone_analysis[zone_name] = enhanced_data

                # Adjust counting_summary for zones (current counts based on union across zones)
                per_category_count = {
                    cat: len(self._current_frame_track_ids.get(cat, set())) for cat in self.target_categories
                }
                counting_summary["per_category_count"] = {k: v for k, v in per_category_count.items() if v > 0}
                counting_summary["total_count"] = sum(per_category_count.values())

        alerts = self._check_alerts(counting_summary, zone_analysis, frame_number, config)
        self._extract_predictions(processed_data)
        _ = self._generate_incidents(counting_summary, zone_analysis, alerts, config, frame_number, stream_info)
        incidents_list = []
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
        processing_latency_ms = proc_time * 1000.0
        processing_fps = (1.0 / proc_time) if proc_time > 0 else None
        # Log the performance metrics using the module-level logger
        print(
            "latency in ms:",
            processing_latency_ms,
            "| Throughput fps:",
            processing_fps,
            "| Frame_Number:",
            self._total_frame_counter,
        )
        return result

    def _update_zone_tracking(
        self,
        zone_analysis: Dict[str, Dict[str, int]],
        detections: List[Dict],
        config: WeaponHumanDetectionConfig,
    ) -> Dict[str, Dict[str, Any]]:
        """
        Update zone tracking with current frame data.

        Args:
            zone_analysis: Current zone analysis results
            detections: List of detections with track IDs

        Returns:
            Enhanced zone analysis with tracking information
        """
        if not zone_analysis or not config.zone_config or not config.zone_config["zones"]:
            return {}

        enhanced_zone_analysis = {}
        zones = config.zone_config["zones"]

        # Get track to category mapping
        track_to_cat = {
            det.get("track_id"): det.get("category") for det in detections if det.get("track_id") is not None
        }

        # Get current frame track IDs in each zone
        current_frame_zone_tracks = {}

        # Initialize zone tracking for all zones
        for zone_name in zones.keys():
            current_frame_zone_tracks[zone_name] = set()
            if zone_name not in self._zone_current_track_ids:
                self._zone_current_track_ids[zone_name] = set()
            if zone_name not in self._zone_total_track_ids:
                self._zone_total_track_ids[zone_name] = set()

        # Check each detection against each zone
        for detection in detections:
            track_id = detection.get("track_id")
            if track_id is None:
                continue

            # Get detection bbox
            bbox = detection.get("bounding_box", detection.get("bbox"))
            if not bbox:
                continue

            # Get detection center point
            center_point = get_bbox_bottom25_center(bbox)  # get_bbox_center(bbox)

            # Flag to check if this track is in any zone this frame
            in_any_zone = False

            # Check which zone this detection is in using actual zone polygons
            for zone_name, zone_polygon in zones.items():
                # Convert polygon points to tuples for point_in_polygon function
                # zone_polygon format: [[x1, y1], [x2, y2], [x3, y3], ...]
                polygon_points = [(point[0], point[1]) for point in zone_polygon]

                # Check if detection center is inside the zone polygon using ray casting algorithm
                if point_in_polygon(center_point, polygon_points):
                    current_frame_zone_tracks[zone_name].add(track_id)
                    in_any_zone = True
                    if track_id not in self._total_count_list:
                        self._total_count_list.append(track_id)

            # If in any zone, update global current and total (cumulative only if new)
            if in_any_zone:
                cat = track_to_cat.get(track_id)
                if cat:
                    # Update current frame global (union across zones)
                    self._current_frame_track_ids.setdefault(cat, set()).add(track_id)

                    # Track if this is the first time in any zone (zone-entry tracking only)
                    # NOTE: Global _per_category_total_track_ids is updated in _update_tracking_state()
                    # to avoid double-updates and ensure consistent timing of new vs total computation
                    if track_id not in self._tracked_in_zones:
                        self._tracked_in_zones.add(track_id)

        # Update zone tracking for each zone
        for zone_name, zone_counts in zone_analysis.items():
            # Get current frame tracks for this zone
            current_tracks = current_frame_zone_tracks.get(zone_name, set())

            # Update current zone tracks
            self._zone_current_track_ids[zone_name] = current_tracks

            # Update total zone tracks (accumulate all track IDs that have been in zone)
            self._zone_total_track_ids[zone_name].update(current_tracks)

            # Update counts
            self._zone_current_counts[zone_name] = len(current_tracks)
            self._zone_total_counts[zone_name] = len(self._zone_total_track_ids[zone_name])

            # Create enhanced zone analysis
            enhanced_zone_analysis[zone_name] = {
                "current_count": self._zone_current_counts[zone_name],
                "total_count": self._zone_total_counts[zone_name],
                "current_track_ids": list(current_tracks),
                "total_track_ids": list(self._zone_total_track_ids[zone_name]),
                "original_counts": zone_counts,  # Preserve original zone counts
            }

        return enhanced_zone_analysis

    @staticmethod
    def _canonicalize_categories(data: Any) -> Any:
        """Map Roboflow / YOLO label variants to canonical human | weapon."""

        def canon(name: Any) -> str:
            key = str(name).strip().lower().replace(" ", "").replace("-", "").replace("_", "")
            if key == "weapon":
                return "weapon"
            if key in {"human", "person"}:
                return "human"
            return str(name).strip().lower()

        if isinstance(data, list):
            for det in data:
                if isinstance(det, dict) and det.get("category") is not None:
                    det["category"] = canon(det["category"])
            return data
        if isinstance(data, dict):
            for _frame, dets in data.items():
                if isinstance(dets, list):
                    for det in dets:
                        if isinstance(det, dict) and det.get("category") is not None:
                            det["category"] = canon(det["category"])
            return data
        return data

    def _normalize_yolo_results(self, data: Any, index_to_category: Optional[Dict[int, str]] = None) -> Any:
        """
        Normalize YOLO-style outputs to internal detection schema:
        - category/category_id: prefer string label using COCO mapping if available
        - confidence: map from 'conf'/'score' to 'confidence'
        - bounding_box: ensure dict with keys (x1,y1,x2,y2) or (xmin,ymin,xmax,ymax)
        - supports list of detections and frame_id -> detections dict
        """

        def to_bbox_dict(d: Dict[str, Any]) -> Dict[str, Any]:
            if "bounding_box" in d and isinstance(d["bounding_box"], dict):
                return d["bounding_box"]
            if "bbox" in d:
                bbox = d["bbox"]
                if isinstance(bbox, dict):
                    return bbox
                if isinstance(bbox, (list, tuple)) and len(bbox) >= 4:
                    x1, y1, x2, y2 = bbox[0], bbox[1], bbox[2], bbox[3]
                    return {"x1": x1, "y1": y1, "x2": x2, "y2": y2}
            if "xyxy" in d and isinstance(d["xyxy"], (list, tuple)) and len(d["xyxy"]) >= 4:
                x1, y1, x2, y2 = d["xyxy"][0], d["xyxy"][1], d["xyxy"][2], d["xyxy"][3]
                return {"x1": x1, "y1": y1, "x2": x2, "y2": y2}
            if "xywh" in d and isinstance(d["xywh"], (list, tuple)) and len(d["xywh"]) >= 4:
                cx, cy, w, h = d["xywh"][0], d["xywh"][1], d["xywh"][2], d["xywh"][3]
                x1, y1, x2, y2 = cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2
                return {"x1": x1, "y1": y1, "x2": x2, "y2": y2}
            return {}

        def resolve_category(d: Dict[str, Any]) -> Tuple[str, Optional[int]]:
            raw_cls = d.get("category", d.get("category_id", d.get("class", d.get("cls"))))
            label_name = d.get("name")
            if isinstance(raw_cls, int):
                if index_to_category and raw_cls in index_to_category:
                    return index_to_category[raw_cls], raw_cls
                return str(raw_cls), raw_cls
            if isinstance(raw_cls, str):
                # Some YOLO exports provide string labels directly
                return raw_cls, None
            if label_name:
                return str(label_name), None
            return "unknown", None

        def normalize_det(det: Dict[str, Any]) -> Dict[str, Any]:
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
            # Preserve optional fields
            for key in ("track_id", "frame_id", "masks", "segmentation"):
                if key in det:
                    normalized[key] = det[key]
            return normalized

        if isinstance(data, list):
            return [normalize_det(d) if isinstance(d, dict) else d for d in data]
        if isinstance(data, dict):
            # Detect tracking style dict: frame_id -> list of detections
            normalized_dict: Dict[str, Any] = {}
            for k, v in data.items():
                if isinstance(v, list):
                    normalized_dict[k] = [normalize_det(d) if isinstance(d, dict) else d for d in v]
                elif isinstance(v, dict):
                    normalized_dict[k] = normalize_det(v)
                else:
                    normalized_dict[k] = v
            return normalized_dict
        return data

    def _check_alerts(
        self,
        summary: dict,
        _zone_analysis: Dict,
        frame_number: Any,
        config: WeaponHumanDetectionConfig,
    ) -> List[Dict]:
        _ = (_zone_analysis,)

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
        _zone_analysis: Dict,
        alerts: List,
        config: WeaponHumanDetectionConfig,
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

            human_text_lines = [f"WEAPON INCIDENTS DETECTED @ {current_timestamp}:"]
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
        zone_analysis: Dict,
        alerts: List,
        config: WeaponHumanDetectionConfig,
        frame_number: Optional[int] = None,
        stream_info: Optional[Dict[str, Any]] = None,
    ) -> List[Dict]:
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

        # Get new track IDs count (weapon events that appeared for FIRST TIME - requires tracker to be enabled)
        new_counts_dict = self.get_new_counts_this_frame()

        # DIRECT COUNT from detections list - most reliable source of truth
        raw_detections = counting_summary.get("detections", [])
        detection_count_by_category = {}
        for det in raw_detections:
            cat = det.get("category", "weapon")
            detection_count_by_category[cat] = detection_count_by_category.get(cat, 0) + 1

        total_counts = [{"category": cat, "count": count} for cat, count in total_counts_dict.items() if count > 0]
        # current_counts: ALL weapon detections in frame - computed directly from detections
        current_counts = [{"category": cat, "count": count} for cat, count in detection_count_by_category.items()]
        # Fallback: if detection_count_by_category is empty but we have total_detections, use per_category_count
        if not current_counts and total_detections > 0:
            current_counts = [{"category": cat, "count": count} for cat, count in per_category_count.items()]
        # current_new_counts: Only NEW weapon events (first time seen; requires tracker enabled)
        current_new_counts = [{"category": cat, "count": count} for cat, count in new_counts_dict.items()]

        # ONE concise stats summary line
        curr_total = sum(c.get("count", 0) for c in current_counts)
        new_total = sum(c.get("count", 0) for c in current_new_counts)
        total_total = sum(c.get("count", 0) for c in total_counts)
        print(f"[STATS] F{frame_number} | current={curr_total} new={new_total} total={total_total}")

        detections = []
        for detection in counting_summary.get("detections", []):
            bbox = detection.get("bounding_box", {})
            category = detection.get("category", "weapon")
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

        if getattr(config, "include_humans_in_output", True):
            for detection in self._human_display_detections:
                bbox = detection.get("bounding_box", {})
                category = detection.get("category", "human")
                detections.append(self.create_detection_object(category, bbox))

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

        # Generate human text similar to people_counting format
        human_text_lines = []
        human_text_lines.append(f"CURRENT FRAME @ {current_timestamp}:")

        # Display current counts - zone-wise or category-wise
        if zone_analysis:
            human_text_lines.append("\t- Weapon Detected by Zone:")
            for zone_name, zone_data in zone_analysis.items():
                current_count = 0
                if isinstance(zone_data, dict):
                    if "current_count" in zone_data:
                        current_count = zone_data.get("current_count", 0)
                    else:
                        counts_dict = (
                            zone_data.get("original_counts")
                            if isinstance(zone_data.get("original_counts"), dict)
                            else zone_data
                        )
                        current_count = counts_dict.get(
                            "total",
                            sum(v for v in counts_dict.values() if isinstance(v, (int, float))),
                        )
                human_text_lines.append(f"\t\t- {zone_name}: {int(current_count)}")
        else:
            for cat, count in detection_count_by_category.items():
                new_count = new_counts_dict.get(cat, 0)
                human_text_lines.append(f"\t- Total Weapons in Frame ({cat}): {count}")
                human_text_lines.append(f"\t- New Weapons (just entered) ({cat}): {new_count}")

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
        tracking_stat["target_categories"] = self.target_categories
        # current_new_counts: NEW track IDs that appeared for first time in this frame/aggregation
        tracking_stat["current_new_counts"] = current_new_counts
        tracking_stats.append(tracking_stat)
        return tracking_stats

    def _generate_business_analytics(
        self,
        _counting_summary: Dict,
        _zone_analysis: Dict,
        _alerts: Any,
        _config: WeaponHumanDetectionConfig,
        _stream_info: Optional[Dict[str, Any]] = None,
        is_empty=False,
    ) -> List[Dict]:
        _ = (_alerts, _config, _counting_summary, _stream_info, _zone_analysis)
        if is_empty:
            return []

        return None

    def _generate_summary(
        self,
        _summary: dict,
        _zone_analysis: Dict,
        incidents: List,
        tracking_stats: List,
        business_analytics: List,
        _alerts: List,
    ) -> List[str]:
        """
        Generate a human_text string for the tracking_stat, incident, business analytics and alerts.
        """
        _ = (_alerts, _summary, _zone_analysis)
        lines = []
        lines.append("Application Name: " + self.CASE_TYPE)
        lines.append("Application Version: " + self.CASE_VERSION)
        if len(incidents) > 0:
            lines.append("Incidents: " + f"\n\t{incidents[0].get('human_text', 'No incidents detected')}")
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

    def _update_tracking_state(self, detections: list, _has_zones: bool = False):
        _ = (_has_zones,)
        if not hasattr(self, "_per_category_total_track_ids"):
            self._per_category_total_track_ids = {cat: set() for cat in self.target_categories}
        if not hasattr(self, "_previous_frame_track_ids"):
            self._previous_frame_track_ids = {cat: set() for cat in self.target_categories}

        # Step 1: Build current frame track IDs (DON'T update total yet!)
        self._current_frame_track_ids = {cat: set() for cat in self.target_categories}

        for det in detections:
            cat = det.get("category")
            raw_track_id = det.get("track_id")
            if cat not in self.target_categories or raw_track_id is None:
                continue
            bbox = det.get("bounding_box", det.get("bbox"))
            canonical_id = self._merge_or_register_track(raw_track_id, bbox)
            det["track_id"] = canonical_id
            # DON'T update total here - must compute "new" first!
            self._current_frame_track_ids.setdefault(cat, set()).add(canonical_id)

        # Step 2: Compute NEW = current - total (BEFORE updating total!)
        # This ensures re-entries are NOT counted as "new" again
        self._new_track_ids_this_frame = {
            cat: (self._current_frame_track_ids.get(cat, set()) - self._per_category_total_track_ids.get(cat, set()))
            for cat in self.target_categories
        }

        # ONE concise log line per frame (using first target category for display)
        first_cat = self.target_categories[0] if self.target_categories else "weapon"
        current_ids = sorted(list(self._current_frame_track_ids.get(first_cat, set())))
        new_ids = sorted(list(self._new_track_ids_this_frame.get(first_cat, set())))
        total_seen = len(self._per_category_total_track_ids.get(first_cat, set()))
        print(
            f"[TRACK] F{self._total_frame_counter} | det={len(detections)} ids={current_ids[:10]}{'...' if len(current_ids) > 10 else ''} new={new_ids} total_seen={total_seen}"
        )

        # Only log when NEW track IDs created (helpful for debugging)
        if any(len(ids) > 0 for ids in self._new_track_ids_this_frame.values()):
            print(
                f"[NEW_TRACK] F{self._total_frame_counter} | new_ids={new_ids} total_unique={total_seen + len(new_ids)}"
            )

        # Step 3: NOW update total with current IDs (ALWAYS, regardless of zones!)
        # Zone-specific tracking is handled separately in _update_zone_tracking
        for cat, ids in self._current_frame_track_ids.items():
            self._per_category_total_track_ids.setdefault(cat, set()).update(ids)

        # DIAGNOSTIC: Warn if total_seen grows too large relative to detections
        total_seen_after = len(self._per_category_total_track_ids.get(first_cat, set()))
        if total_seen_after > 100 and len(detections) > 0:
            ratio = total_seen_after / max(len(detections), 1)
            if ratio > 20:
                print(
                    f"[WARN] F{self._total_frame_counter} | total_seen={total_seen_after} vs det={len(detections)} "
                    f"(ratio={ratio:.1f}x) - possible tracker instability or use case recreation"
                )

        # Snapshot current -> previous for next call
        self._previous_frame_track_ids = {cat: set(ids) for cat, ids in self._current_frame_track_ids.items()}

    def get_total_counts(self):
        return {cat: len(ids) for cat, ids in getattr(self, "_per_category_total_track_ids", {}).items()}

    def get_new_counts_this_frame(self) -> Dict[str, int]:
        """Get count of NEW track IDs that appeared in this frame/aggregation vs the previous one."""
        return {cat: len(ids) for cat, ids in getattr(self, "_new_track_ids_this_frame", {}).items()}

    def get_current_frame_counts(self) -> Dict[str, int]:
        """Get count of ALL track IDs currently in this frame (existing + new)."""
        return {cat: len(ids) for cat, ids in getattr(self, "_current_frame_track_ids", {}).items()}

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
        timestamp_human = timestamp.replace(" UTC", "").strip()

        # Remove milliseconds if present (everything after the last dot)
        if "." in timestamp_human:
            timestamp_human = timestamp_human.split(".")[0]

        # Parse the timestamp string and convert to desired format
        try:
            # Handle format: YYYY-MM-DD-HH:MM:SS
            if timestamp_human.count("-") >= 2:
                # Replace first two dashes with colons for date part, third with space
                parts = timestamp_human.split("-")
                if len(parts) >= 4:
                    # parts = ['2025', '10', '27', '19:31:20']
                    formatted = f"{parts[0]}:{parts[1]}:{parts[2]} {'-'.join(parts[3:])}"
                    return formatted
        except Exception:
            # Non-fatal: exception ignored here; execution continues per surrounding logic.
            pass

        # If parsing fails, return the humaned string as-is
        return timestamp_human

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

    def _count_categories(self, detections: list, _config: WeaponHumanDetectionConfig) -> dict:
        _ = (_config,)
        counts = {}
        for det in detections:
            cat = det.get("category", "unknown")
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
