import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

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
from ..utils.agnostic_nms import AgnosticNMS
from ..utils.geometry_utils import get_bbox_bottom25_center, point_in_polygon


@dataclass
class VehicleMonitoringDroneViewConfig(BaseConfig):
    """Configuration for drone view vehicle monitoring use case."""

    enable_smoothing: bool = True
    smoothing_algorithm: str = "observability"
    smoothing_window_size: int = 20
    smoothing_cooldown_frames: int = 5
    smoothing_confidence_range_factor: float = 0.5
    confidence_threshold: float = 0.6

    # Agnostic-NMS: Configuration parameters
    enable_nms: bool = True
    nms_iou_threshold: float = 0.45
    nms_class_agnostic: bool = True
    nms_min_box_size: float = 2.0
    nms_use_vectorized: bool = True

    # Class Aggregation: Configuration parameters
    enable_class_aggregation: bool = True
    class_aggregation_window_size: int = 30  # 30 frames ≈ 1 second at 30 FPS

    # JBK_720_GATE POLYGON = [[86, 328], [844, 317], [1277, 520], [1273, 707], [125, 713]]
    zone_config: Optional[Dict[str, List[List[float]]]] = None  # field(
    #     default_factory=lambda: {
    #         "zones": {
    #             "Interest_Region": [[86, 328], [844, 317], [1277, 520], [1273, 707], [125, 713]],
    #         }
    #     }
    # )
    usecase_categories: List[str] = field(default_factory=lambda: ["car", "van", "bus", "truck"])
    target_categories: List[str] = field(default_factory=lambda: ["car", "van", "bus", "truck"])
    alert_config: Optional[AlertConfig] = None
    index_to_category: Optional[Dict[int, str]] = field(
        default_factory=lambda: {0: "car", 1: "van", 2: "bus", 3: "truck"}
    )


class VehicleMonitoringDroneViewUseCase(BaseProcessor):
    CATEGORY_DISPLAY = {
        "car": "Car",
        "van": "Van",
        "bus": "Bus",
        "truck": "Truck",
    }

    def __init__(self):
        super().__init__("vehicle_monitoring_drone_view")
        self.category = "traffic"
        self.CASE_TYPE: Optional[str] = "vehicle_monitoring_drone_view"
        self.CASE_VERSION: Optional[str] = "1.0"
        self.target_categories = ["car", "van", "bus", "truck"]
        self.smoothing_tracker = None
        self.tracker = None
        self._tracker_seam = ConfigDrivenTracker()
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

        # Agnostic-NMS: Initialize reusable NMS module
        self._nms_module = None

    def process(
        self,
        data: Any,
        config: ConfigProtocol,
        context: Optional[ProcessingContext] = None,
        stream_info: Optional[Dict[str, Any]] = None,
    ) -> ProcessingResult:
        processing_start = time.time()
        if not isinstance(config, VehicleMonitoringDroneViewConfig):
            return self.create_error_result(
                "Invalid config type",
                usecase=self.name,
                category=self.category,
                context=context,
            )
        if context is None:
            context = ProcessingContext()

        # Determine if zones are configured
        has_zones = bool(config.zone_config and config.zone_config.get("zones"))

        # ===== DEBUG POINT 1: RAW INPUT =====
        self._log_detection_stats(data, "01_RAW_INPUT", show_samples=True)

        # Normalize typical YOLO outputs (COCO pretrained) to internal schema
        data = self._normalize_yolo_results(data, getattr(config, "index_to_category", None))

        # ===== DEBUG POINT 2: AFTER NORMALIZATION =====
        self._log_detection_stats(data, "02_AFTER_NORMALIZATION", show_samples=True)

        input_format = match_results_structure(data)
        context.input_format = input_format
        context.confidence_threshold = config.confidence_threshold
        # NOTE : Confidence Threshold overwrite disabled for now
        # config.confidence_threshold = 0.25

        # param to be updated

        if config.confidence_threshold is not None:
            processed_data = filter_by_confidence(data, config.confidence_threshold)
            self.logger.debug(f"Applied confidence filtering with threshold {config.confidence_threshold}")
            # ===== DEBUG POINT 3: AFTER CONFIDENCE FILTER =====
            self._log_detection_stats(processed_data, "03_AFTER_CONFIDENCE_FILTER")
        else:
            processed_data = data
            self.logger.debug("Did not apply confidence filtering since no threshold provided")

        if config.index_to_category:
            processed_data = apply_category_mapping(processed_data, config.index_to_category)
            self.logger.debug("Applied category mapping")
            # ===== DEBUG POINT 4: AFTER CATEGORY MAPPING =====
            self._log_detection_stats(processed_data, "04_AFTER_CATEGORY_MAPPING")

        # Agnostic-NMS: Apply NMS using reusable module with safety
        if getattr(config, "enable_nms", False):
            pre_nms_count = len(processed_data)

            # ===== DEBUG POINT 5: BEFORE NMS =====
            self._log_detection_stats(processed_data, "05_BEFORE_NMS", show_samples=True)

            # Safety: Log pre-NMS state for debugging
            if pre_nms_count > 0:
                sample_det = processed_data[0]
                self.logger.debug(
                    f"Pre-NMS sample detection keys: {list(sample_det.keys())}, "
                    f"category type: {type(sample_det.get('category')).__name__}, "
                    f"confidence type: {type(sample_det.get('confidence')).__name__}"
                )

            try:
                # Initialize NMS module if needed
                if self._nms_module is None:
                    self._nms_module = AgnosticNMS(
                        iou_threshold=getattr(config, "nms_iou_threshold", 0.45),
                        min_box_size=getattr(config, "nms_min_box_size", 2.0),
                        use_vectorized=getattr(config, "nms_use_vectorized", True),
                    )
                    self.logger.info("AgnosticNMS module initialized")

                # Apply NMS
                processed_data = self._nms_module.apply(
                    processed_data,
                    class_agnostic=getattr(config, "nms_class_agnostic", True),
                    target_categories=self.target_categories,
                )

                post_nms_count = len(processed_data)
                suppressed_count = pre_nms_count - post_nms_count

                # ===== DEBUG POINT 6: AFTER NMS =====
                self._log_detection_stats(processed_data, "06_AFTER_NMS")

                self.logger.info(
                    f"NMS applied successfully: {pre_nms_count} -> {post_nms_count} detections "
                    f"({suppressed_count} suppressed, {100 * suppressed_count / max(pre_nms_count, 1):.1f}%)"
                )

            except ValueError as ve:
                # Schema validation error - log detailed diagnostics
                self.logger.error(f"NMS schema validation failed: {ve}")
                self.logger.error("Continuing without NMS. Check logs above for detailed diagnostics.")

            except Exception as e:
                # Unexpected error - log full details
                import traceback

                self.logger.error(f"NMS failed with unexpected error: {e}")
                self.logger.error(f"Traceback: {traceback.format_exc()}")
                self.logger.error("Continuing without NMS.")

        processed_data = [d for d in processed_data if d.get("category") in self.target_categories]
        if config.target_categories:
            processed_data = [d for d in processed_data if d.get("category") in self.target_categories]
            self.logger.debug("Applied category filtering")

            # ===== DEBUG POINT 7: AFTER TARGET CATEGORY FILTER =====
            self._log_detection_stats(processed_data, "07_AFTER_TARGET_FILTER")

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

            # ===== DEBUG POINT 8: AFTER SMOOTHING =====
            self._log_detection_stats(processed_data, "08_AFTER_SMOOTHING")

        try:
            if self.tracker is None:
                self.tracker = self._tracker_seam.get_shared_tracker(
                    profile=TrackerProfile.DEFAULT,
                    enable_class_aggregation=config.enable_class_aggregation,
                    class_aggregation_window_size=config.class_aggregation_window_size,
                )
                self.logger.info("Initialized AdvancedTracker for Vehicle Monitoring Drone View Use Case")

                if config.enable_class_aggregation:
                    self.logger.info(
                        f"AdvancedTracker initialized with class aggregation "
                        f"(window_size={config.class_aggregation_window_size})"
                    )
                else:
                    self.logger.info("AdvancedTracker initialized without class aggregation")

            processed_data = self.tracker.update(processed_data)

            # ===== DEBUG POINT 9: AFTER TRACKING =====
            self._log_detection_stats(processed_data, "09_AFTER_TRACKING")

        except Exception as e:
            self.logger.warning(f"AdvancedTracker failed: {e}")

        self._update_tracking_state(processed_data, has_zones=has_zones)
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
        config: VehicleMonitoringDroneViewConfig,
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

                    # Update global cumulative if first time in any zone
                    if track_id not in self._tracked_in_zones:
                        self._tracked_in_zones.add(track_id)
                        self._per_category_total_track_ids.setdefault(cat, set()).add(track_id)

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
        config: VehicleMonitoringDroneViewConfig,
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
        config: VehicleMonitoringDroneViewConfig,
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

            human_text_lines = [f"VEHICLE INCIDENTS DETECTED @ {current_timestamp}:"]
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
        config: VehicleMonitoringDroneViewConfig,
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

        # Get new track IDs count (vehicles that appeared for FIRST TIME - requires tracker to be enabled)
        new_counts_dict = self.get_new_counts_this_frame()

        # DIRECT COUNT from detections list - most reliable source of truth
        raw_detections = counting_summary.get("detections", [])
        detection_count_by_category = {}
        for det in raw_detections:
            cat = det.get("category", "vehicle")
            detection_count_by_category[cat] = detection_count_by_category.get(cat, 0) + 1

        total_counts = [{"category": cat, "count": count} for cat, count in total_counts_dict.items() if count > 0]
        # current_counts: ALL vehicles currently detected in frame - computed directly from detections
        current_counts = [{"category": cat, "count": count} for cat, count in detection_count_by_category.items()]
        # Fallback: if detection_count_by_category is empty but we have total_detections, use per_category_count
        if not current_counts and total_detections > 0:
            current_counts = [{"category": cat, "count": count} for cat, count in per_category_count.items()]
        # current_new_counts: Only NEW vehicles who appeared for the first time (requires tracker enabled)
        current_new_counts = [{"category": cat, "count": count} for cat, count in new_counts_dict.items()]

        detections = []
        for detection in counting_summary.get("detections", []):
            bbox = detection.get("bounding_box", {})
            category = detection.get("category", "vehicle")
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

        # Generate human text similar to people_counting format
        human_text_lines = []
        human_text_lines.append(f"CURRENT FRAME @ {current_timestamp}:")

        # Display current counts - zone-wise or category-wise
        if zone_analysis:
            human_text_lines.append("\t- Vehicles Detected by Zone:")
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
                human_text_lines.append(f"\t- Total Vehicles in Frame ({cat}): {count}")
                human_text_lines.append(f"\t- New Vehicles (just entered) ({cat}): {new_count}")

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
        _config: VehicleMonitoringDroneViewConfig,
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

    def _update_tracking_state(self, detections: list, has_zones: bool = False):
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
            if not has_zones:
                self._per_category_total_track_ids.setdefault(cat, set()).add(canonical_id)
            # For current frame, add unconditionally here; will be overridden/adjusted if has_zones in _update_zone_tracking
            self._current_frame_track_ids.setdefault(cat, set()).add(canonical_id)

        # NEW track IDs = present in current frame but NOT in previous frame
        self._new_track_ids_this_frame = {
            cat: (self._current_frame_track_ids.get(cat, set()) - self._previous_frame_track_ids.get(cat, set()))
            for cat in self.target_categories
        }

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

    def _count_categories(self, detections: list, _config: VehicleMonitoringDroneViewConfig) -> dict:
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

    def _log_detection_stats(self, data: Any, stage_name: str, show_samples: bool = False) -> None:
        """
        Log detailed detection statistics at any pipeline stage with frame identification.

        Args:
            data: Detection data (list or dict format)
            stage_name: Name of the pipeline stage for identification
            show_samples: If True, show sample detection structure
        """
        if not getattr(self, "_debug_detection_flow", True):
            return

        # Use existing frame counter
        frame_id = self._total_frame_counter
        timestamp_str = datetime.now(timezone.utc).strftime("%H:%M:%S.%f")[:-3]

        # Create unique log identifier for grep
        log_id = f"FRAME_{frame_id:06d}"

        separator = "=" * 80
        print(f"\n{separator}")
        print(f"[DETECTION_STATS] {log_id} | Time: {timestamp_str} | Stage: {stage_name}")
        print(separator)

        # Handle different data formats
        detections = []
        if isinstance(data, list):
            detections = data
        elif isinstance(data, dict):
            # Frame-based format
            for fid, frame_dets in data.items():
                if isinstance(frame_dets, list):
                    detections.extend(frame_dets)

        if not detections:
            print(f"  Frame: #{frame_id} | Total Detections: 0")
            print(separator)
            return

        # Calculate statistics
        total_count = len(detections)

        # Count by category
        category_counts = {}
        confidence_sum = {}
        confidence_min = {}
        confidence_max = {}
        bbox_format_count = {"x1/y1/x2/y2": 0, "xmin/ymin/xmax/ymax": 0, "other": 0}
        has_track_id = 0

        for det in detections:
            if not isinstance(det, dict):
                continue

            # Category counting
            cat = det.get("category", "UNKNOWN")
            category_counts[cat] = category_counts.get(cat, 0) + 1

            # Confidence stats
            conf = det.get("confidence", 0.0)
            if cat not in confidence_sum:
                confidence_sum[cat] = 0.0
                confidence_min[cat] = conf
                confidence_max[cat] = conf
            confidence_sum[cat] += conf
            confidence_min[cat] = min(confidence_min[cat], conf)
            confidence_max[cat] = max(confidence_max[cat], conf)

            # BBox format detection
            bbox = det.get("bounding_box", det.get("bbox", {}))
            if isinstance(bbox, dict):
                if "x1" in bbox and "y1" in bbox:
                    bbox_format_count["x1/y1/x2/y2"] += 1
                elif "xmin" in bbox and "ymin" in bbox:
                    bbox_format_count["xmin/ymin/xmax/ymax"] += 1
                else:
                    bbox_format_count["other"] += 1

            # Track ID presence
            if det.get("track_id") is not None:
                has_track_id += 1

        # Print summary
        print(f"  Frame: #{frame_id} | Total Detections: {total_count}")

        if has_track_id > 0:
            print(f"  Detections with Track ID: {has_track_id} ({100 * has_track_id / total_count:.1f}%)")

        print("\n  Category Distribution:")

        # Sort categories by count (descending)
        sorted_cats = sorted(category_counts.items(), key=lambda x: x[1], reverse=True)

        for cat, count in sorted_cats:
            percentage = (count / total_count) * 100
            avg_conf = confidence_sum[cat] / count
            min_conf = confidence_min[cat]
            max_conf = confidence_max[cat]

            print(
                f"    [{cat:20s}] Count: {count:4d} ({percentage:5.1f}%) | "
                f"Conf: avg={avg_conf:.3f}, min={min_conf:.3f}, max={max_conf:.3f}"
            )

        # Print bbox format distribution
        print("\n  BBox Format Distribution:")
        for fmt, count in bbox_format_count.items():
            if count > 0:
                percentage = (count / total_count) * 100
                print(f"    {fmt:25s}: {count:4d} ({percentage:5.1f}%)")

        # Show sample detection structure if requested
        if show_samples and detections:
            print("\n  Sample Detection Structure:")
            sample = detections[0]
            print(f"    Keys: {list(sample.keys())}")
            print(f"    Category: {sample.get('category')} (type: {type(sample.get('category')).__name__})")
            print(f"    Confidence: {sample.get('confidence')} (type: {type(sample.get('confidence')).__name__})")

            if sample.get("track_id") is not None:
                print(f"    Track ID: {sample.get('track_id')} (type: {type(sample.get('track_id')).__name__})")

            bbox = sample.get("bounding_box", sample.get("bbox", {}))
            if isinstance(bbox, dict):
                print(f"    BBox Keys: {list(bbox.keys())}")
                if bbox:
                    first_key = list(bbox.keys())[0]
                    print(f"    BBox Coord Type: {type(bbox[first_key]).__name__}")

        print(separator)
