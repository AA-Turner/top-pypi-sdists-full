import math
import time
from collections import defaultdict, deque
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Sequence, Tuple

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
from ..utils.incident_manager_utils import INCIDENT_MANAGER, IncidentManagerFactory

# COCO 17 keypoint indices (Ultralytics / OpenPose-compatible ordering).
_KP_LEFT_SHOULDER, _KP_RIGHT_SHOULDER = 5, 6
_KP_LEFT_HIP, _KP_RIGHT_HIP = 11, 12

# Fallback camera key when stream_info carries no camera identifier.
_DEFAULT_CAMERA_ID = "camera"


def _resolve_manager_camera_id(stream_info: Optional[Dict[str, Any]]) -> str:
    """Resolve the camera key used by IncidentManager state tracking."""
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


def _extract_coco17_keypoints(detection: Dict[str, Any]) -> Optional[List[Tuple[float, float, float]]]:
    """
    Return 17 tuples (x, y, confidence), or None if keypoints cannot be parsed.

    Supported shapes on ``detection["keypoints"]``:
      * Flat list of length 51: [x0,y0,c0, x1,y1,c1, ...]
      * Length 34: xy only, confidence assumed 1.0
      * Length 17: each element is [x,y] or [x,y,c]
      * Dict with "xy"/"data"/"coords" (+ optional "conf"/"visibility")
    """
    raw = detection.get("keypoints")
    if raw is None:
        return None

    if isinstance(raw, dict):
        xy = raw.get("xy") or raw.get("data") or raw.get("coords")
        conf = raw.get("conf") or raw.get("visibility")
        if xy is None:
            return None
        try:
            flat_xy: List[float] = []
            if xy and isinstance(xy[0], (list, tuple)) and len(xy[0]) >= 2:
                for row in xy[:17]:
                    flat_xy.extend([float(row[0]), float(row[1])])
            elif len(xy) >= 34:
                flat_xy = [float(x) for x in xy[:34]]
            else:
                return None

            if conf is not None and len(conf) >= 17:
                cfs = [float(conf[i]) for i in range(17)]
            else:
                cfs = [1.0] * 17

            return [(flat_xy[i * 2], flat_xy[i * 2 + 1], cfs[i]) for i in range(17)]
        except (TypeError, ValueError, IndexError):
            return None

    if not isinstance(raw, (list, tuple)):
        return None

    if len(raw) == 51:
        try:
            return [(float(raw[i * 3]), float(raw[i * 3 + 1]), float(raw[i * 3 + 2])) for i in range(17)]
        except (TypeError, ValueError, IndexError):
            return None

    if len(raw) == 34:
        try:
            return [(float(raw[i * 2]), float(raw[i * 2 + 1]), 1.0) for i in range(17)]
        except (TypeError, ValueError, IndexError):
            return None

    if len(raw) == 17:
        try:
            out: List[Tuple[float, float, float]] = []
            for triple in raw:
                seq: Sequence[float] = triple  # type: ignore[assignment]
                cf = float(seq[2]) if len(seq) > 2 else 1.0
                out.append((float(seq[0]), float(seq[1]), cf))
            return out
        except (TypeError, ValueError, IndexError):
            return None

    return None


@dataclass
class FallDetectionConfig(BaseConfig):
    """Configuration for fall detection in people analytics usecase."""

    enable_smoothing: bool = True
    smoothing_algorithm: str = "observability"
    smoothing_window_size: int = 20
    smoothing_cooldown_frames: int = 5
    smoothing_confidence_range_factor: float = 0.5
    confidence_threshold: float = 0.6

    # Pose-based fall detection: a strict 3-step sequence (all required, in order)
    # derived from the person box and COCO-17 keypoints, not a fall/non_fall model:
    #   Step 1 - sudden fast drop: body center drops > pose_drop_ratio_thresh of the
    #            frame height within the short pose_drop_window_seconds (slow = sitting).
    #   Step 2 - now flat: bbox wider-than-tall OR torso angle past pose_angle_thresh_deg.
    #   Step 3 - stayed down: remains horizontal pose_stay_down_seconds without getting up.
    enable_fall_detection: bool = True
    pose_angle_thresh_deg: float = 45.0  # torso "horizontal" when angle from vertical exceeds this
    pose_aspect_ratio_thresh: float = 1.0  # box width/height above this means wider-than-tall
    pose_drop_window_seconds: float = 0.6  # short window in which a "sudden" drop must occur
    pose_drop_ratio_thresh: float = 0.15  # fraction of frame height the center must drop in-window
    pose_drop_to_down_grace: float = 1.5  # max wait from drop to becoming horizontal before reset
    pose_stay_down_seconds: float = 3.0  # must stay down (not get up) this long to confirm a fall
    pose_kpt_conf_thresh: float = 0.3  # ignore keypoints below this confidence
    pose_track_eviction_frames: int = 60  # drop per-track state after this many frames of absence

    # Class Aggregation: Configuration parameters
    enable_class_aggregation: bool = False
    class_aggregation_window_size: int = 30  # 30 frames ≈ 1 second at 30 FPS

    zone_config: Optional[Dict[str, List[List[float]]]] = None  # field(
    usecase_categories: List[str] = field(default_factory=lambda: ["person", "fall", "non_fall"])
    target_categories: List[str] = field(default_factory=lambda: ["fall"])
    alert_config: AlertConfig = field(default_factory=lambda: AlertConfig(count_thresholds={"fall": 1}))
    index_to_category: Optional[Dict[int, str]] = field(default_factory=lambda: {0: "person"})

    # Incident-manager wiring (third flow).
    session: Optional[Any] = None
    server_id: Optional[str] = None


class FallDetectionUseCase(BaseProcessor):
    CATEGORY_DISPLAY = {"fall": "Fall", "non_fall": "Non-Fall"}

    def __init__(self):
        super().__init__("fall_detection")
        self.category = "general"
        self.CASE_TYPE: Optional[str] = "fall_detection"
        self.CASE_VERSION: Optional[str] = "1.0"
        self.target_categories = ["fall"]
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

        self.fall_detector = None  # Pose-based detector, initialized lazily in process()

        # Incident manager (third flow): owns the incident open/close lifecycle
        # and incident_res publishing.
        self._INCIDENT_LOG = "[INCIDENT_MANAGER]"
        self._incident_manager_factory: Optional[IncidentManagerFactory] = None
        self._incident_manager: Optional[INCIDENT_MANAGER] = None
        self._incident_manager_initialized: bool = False

    # ---- Incident manager lifecycle ---------------------------------------

    def _initialize_incident_manager_once(self, config: "FallDetectionConfig") -> None:
        if self._incident_manager_initialized:
            return
        try:
            self.logger.info(f"{self._INCIDENT_LOG} Initializing incident manager for fall detection...")
            if self._incident_manager_factory is None:
                self._incident_manager_factory = IncidentManagerFactory(logger=self.logger)
            self._incident_manager = self._incident_manager_factory.initialize(config)
            if self._incident_manager:
                self.logger.info(f"{self._INCIDENT_LOG} Incident manager ready")
            else:
                self.logger.warning(
                    f"{self._INCIDENT_LOG} Incident manager unavailable; incidents will not be published"
                )
        except Exception as e:
            self.logger.error(
                f"{self._INCIDENT_LOG} Incident manager init failed: {e}",
                exc_info=True,
            )
        finally:
            self._incident_manager_initialized = True

    def _send_incident_to_manager(
        self,
        incident: Dict,
        stream_info: Optional[Dict[str, Any]] = None,
        context: Optional[ProcessingContext] = None,
    ) -> bool:
        """Feed the fall incident to the manager and report whether its state changed.

        Fire-style: the manager is called every frame with ``incident or {}`` (no
        early return on an empty dict) so it can count idle frames and publish the
        closing ``info`` transition once the person is back up. Returns True only
        when the manager published a state change (open / severity change / close).
        """
        published = False
        camera_id = _resolve_manager_camera_id(stream_info)
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
                    self.logger.info(f"{self._INCIDENT_LOG} Incident published for camera: {camera_id}")
            except Exception as e:
                self.logger.error(
                    f"{self._INCIDENT_LOG} Error publishing incident: {e}",
                    exc_info=True,
                )

        if context is not None:
            # When IncidentManager is active it owns the full open/close lifecycle.
            # Skip duplicate legacy incident_res publishes from PostProcessor.
            context.metadata["incident_published_via_manager"] = bool(self._incident_manager)
        return published

    def process(
        self,
        data: Any,
        config: ConfigProtocol,
        context: Optional[ProcessingContext] = None,
        stream_info: Optional[Dict[str, Any]] = None,
    ) -> ProcessingResult:
        processing_start = time.time()
        # Relaxed check: Accept FallDetectionConfig OR any config with matching usecase/category
        # This handles multiprocessing module path mismatches while maintaining type safety
        is_valid_config = isinstance(config, FallDetectionConfig) or (
            hasattr(config, "usecase")
            and config.usecase == "fall_detection"
            and hasattr(config, "category")
            and config.category == "general"
        )
        if not is_valid_config:
            self.logger.error(
                f"Config validation failed in fall_detection. "
                f"Got type={type(config).__name__}, module={type(config).__module__}, "
                f"usecase={getattr(config, 'usecase', 'N/A')}, category={getattr(config, 'category', 'N/A')}"
            )
            return self.create_error_result(
                f"Invalid config type: expected FallDetectionConfig or config with usecase='fall_detection', "
                f"got {type(config).__name__} with usecase={getattr(config, 'usecase', 'N/A')}",
                usecase=self.name,
                category=self.category,
                context=context,
            )
        if context is None:
            context = ProcessingContext()

        if not self._incident_manager_initialized:
            self._initialize_incident_manager_once(config)

        # Determine if zones are configured
        has_zones = bool(config.zone_config and config.zone_config.get("zones"))

        data = self._normalize_yolo_results(data, getattr(config, "index_to_category", None))

        input_format = match_results_structure(data)
        context.input_format = input_format
        context.confidence_threshold = config.confidence_threshold
        config.confidence_threshold = 0.5
        # NOTE : param to be updated

        if config.confidence_threshold is not None:
            processed_data = filter_by_confidence(data, config.confidence_threshold)
            self.logger.debug(f"Applied confidence filtering with threshold {config.confidence_threshold}")
        else:
            processed_data = data
            self.logger.debug("Did not apply confidence filtering since no threshold provided")

        if config.index_to_category:
            processed_data = apply_category_mapping(processed_data, config.index_to_category)
            self.logger.debug("Applied category mapping")

        if config.usecase_categories:
            processed_data = [d for d in processed_data if d.get("category") in config.usecase_categories]
            self.logger.debug("Applied usecase category filtering (fall + non_fall)")

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

        try:
            if self.tracker is None:
                self.tracker = self._tracker_seam.get_shared_tracker(
                    stream_info=stream_info,
                    profile=TrackerProfile.DEFAULT,
                    namespace=True,
                    restore=True,
                    enable_class_aggregation=config.enable_class_aggregation,
                    class_aggregation_window_size=config.class_aggregation_window_size,
                )
            processed_data = self.tracker.update(processed_data)
        except Exception as e:
            self.logger.warning(f"AdvancedTracker failed: {e}")

        if config.enable_fall_detection:
            if self.fall_detector is None:
                detector_config = PoseFallConfig(
                    angle_thresh_deg=config.pose_angle_thresh_deg,
                    aspect_ratio_thresh=config.pose_aspect_ratio_thresh,
                    drop_window_seconds=config.pose_drop_window_seconds,
                    drop_ratio_thresh=config.pose_drop_ratio_thresh,
                    drop_to_down_grace=config.pose_drop_to_down_grace,
                    stay_down_seconds=config.pose_stay_down_seconds,
                    kpt_conf_thresh=config.pose_kpt_conf_thresh,
                    track_eviction_frames=config.pose_track_eviction_frames,
                    fall_class="fall",
                    enabled=True,
                )
                self.fall_detector = PoseFallDetector(detector_config)
                self.logger.info(
                    f"Initialized PoseFallDetector "
                    f"(drop>{config.pose_drop_ratio_thresh} in {config.pose_drop_window_seconds}s, "
                    f"angle>{config.pose_angle_thresh_deg}deg, "
                    f"stay_down={config.pose_stay_down_seconds}s)"
                )
            frame_h = self._get_frame_height(stream_info)
            processed_data = self.fall_detector.update(processed_data, frame_h)

            if self._total_frame_counter % 1000 == 0 and self._total_frame_counter > 0:
                stats = self.fall_detector.get_stats()
                self.logger.info(
                    f"[PoseFall] F{self._total_frame_counter} | "
                    f"confirmed_falls={stats['confirmed_falls']} "
                    f"active_tracks={stats['active_tracks']}"
                )

        if config.target_categories:
            processed_data = [d for d in processed_data if d.get("category") in config.target_categories]

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

        # Alert for every confirmed fall: _check_alerts fires whenever a fall is
        # present (count_thresholds default {"fall": 1}). This is intentionally
        # NOT gated on incident-state transitions, so each confirmed fall alerts.
        alerts = self._check_alerts(counting_summary, frame_number, config)

        self._extract_predictions(processed_data)
        incidents_list = self._generate_incidents(
            counting_summary, zone_analysis, alerts, config, frame_number, stream_info
        )

        # Third flow: hand the fall incident to the IncidentManager, which owns the
        # open/close lifecycle and publishes to incident_res. Sets the
        # incident_published_via_manager flag so the PostProcessor legacy bridge
        # does not double-publish. Fed every frame ({} when no fall) for idle close.
        incident = incidents_list[0] if incidents_list else {}
        self._send_incident_to_manager(incident, stream_info, context=context)

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
        config: FallDetectionConfig,
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
            # Preserve optional fields (keypoints are required by the pose-based detector;
            # skeleton_type is surfaced alongside keypoints into agg_summary tracking_stats).
            for key in ("track_id", "frame_id", "masks", "segmentation", "keypoints", "skeleton_type"):
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

    def _check_alerts(self, summary: dict, frame_number: Any, config: FallDetectionConfig) -> List[Dict]:
        """
        Check if any alert thresholds are exceeded and return alert dicts.
        """

        def get_trend(data, lookback=900, threshold=0.6):
            """
            Determine if the trend is ascending or descending based on actual value progression.
            Now works with values 0,1,2,3 (not just binary).
            """
            window = data[-lookback:] if len(data) >= lookback else data
            if len(window) < 2:
                return True  # not enough data to determine trend
            increasing = 0
            total = 0
            for i in range(1, len(window)):
                if window[i] >= window[i - 1]:
                    increasing += 1
                total += 1
            ratio = increasing / total
            if ratio >= threshold:
                return True
            elif ratio <= (1 - threshold):
                return False
            return None

        frame_key = str(frame_number) if frame_number is not None else "current_frame"
        alerts = []

        if not config.alert_config:
            return alerts

        total = summary.get("total_count", 0)
        # self._ascending_alert_list
        if hasattr(config.alert_config, "count_thresholds") and config.alert_config.count_thresholds:
            for category, threshold in config.alert_config.count_thresholds.items():
                if category == "all" and total > threshold:
                    alerts.append(
                        {
                            "alert_type": (
                                getattr(config.alert_config, "alert_type", ["Default"])
                                if hasattr(config.alert_config, "alert_type")
                                else ["Default"]
                            ),
                            "alert_id": "alert_" + category + "_" + frame_key,
                            "incident_category": self.CASE_TYPE,
                            "threshold_level": threshold,
                            "ascending": get_trend(self._ascending_alert_list, lookback=900, threshold=0.8),
                            "settings": {
                                t: v
                                for t, v in zip(
                                    (
                                        getattr(
                                            config.alert_config,
                                            "alert_type",
                                            ["Default"],
                                        )
                                        if hasattr(config.alert_config, "alert_type")
                                        else ["Default"]
                                    ),
                                    (
                                        getattr(config.alert_config, "alert_value", ["JSON"])
                                        if hasattr(config.alert_config, "alert_value")
                                        else ["JSON"]
                                    ),
                                )
                            },
                        }
                    )
                elif category in summary.get("per_category_count", {}):
                    count = summary.get("per_category_count", {})[category]
                    if (
                        count >= threshold
                    ):  # Fixed update to use >= for threshold comparison, as validation fails for zero thresholds
                        alerts.append(
                            {
                                "alert_type": (
                                    getattr(config.alert_config, "alert_type", ["Default"])
                                    if hasattr(config.alert_config, "alert_type")
                                    else ["Default"]
                                ),
                                "alert_id": "alert_" + category + "_" + frame_key,
                                "incident_category": self.CASE_TYPE,
                                "threshold_level": threshold,
                                "ascending": get_trend(
                                    self._ascending_alert_list,
                                    lookback=900,
                                    threshold=0.8,
                                ),
                                "settings": {
                                    t: v
                                    for t, v in zip(
                                        (
                                            getattr(
                                                config.alert_config,
                                                "alert_type",
                                                ["Default"],
                                            )
                                            if hasattr(config.alert_config, "alert_type")
                                            else ["Default"]
                                        ),
                                        (
                                            getattr(
                                                config.alert_config,
                                                "alert_value",
                                                ["JSON"],
                                            )
                                            if hasattr(config.alert_config, "alert_value")
                                            else ["JSON"]
                                        ),
                                    )
                                },
                            }
                        )
        else:
            pass
        return alerts

    def _generate_incidents(
        self,
        counting_summary: Dict,
        _zone_analysis: Dict,
        alerts: List,
        config: FallDetectionConfig,
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
                # Calibrate for falls: a single confirmed fall is a critical event.
                # Fall back to the "fall" threshold (default 1), not a crowd-counting "all" of 15.
                threshold = config.alert_config.count_thresholds.get(
                    "all", config.alert_config.count_thresholds.get("fall", 1)
                )
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

            human_text_lines = [f"FALL INCIDENTS DETECTED @ {current_timestamp}:"]
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

            # incident_quant drives severity in the IncidentManager (third flow).
            # A confirmed fall is a critical event, so scale the fall count against
            # its threshold to a 0-100 quant; a single fall saturates to 100 and
            # maps to "critical" under the manager's default thresholds.
            fall_threshold = 1
            if (
                config.alert_config
                and hasattr(config.alert_config, "count_thresholds")
                and config.alert_config.count_thresholds
            ):
                fall_threshold = (
                    config.alert_config.count_thresholds.get("all", config.alert_config.count_thresholds.get("fall", 1))
                    or 1
                )
            incident_quant = min(100.0, (total_detections / fall_threshold) * 100.0)

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
            event["incident_quant"] = incident_quant
            incidents.append(event)
        else:
            # No falls this frame: close any active incident so the end timestamp resolves
            # for the common "fall ended / person got up" case (would otherwise stay active).
            if self.current_incident_end_timestamp == "Incident still active":
                self.current_incident_end_timestamp = current_timestamp
            self._ascending_alert_list.append(0)
            incidents.append({})
        return incidents

    def _generate_tracking_stats(
        self,
        counting_summary: Dict,
        zone_analysis: Dict,
        alerts: List,
        config: FallDetectionConfig,
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

        # Get new track IDs count (persons that appeared for FIRST TIME - requires tracker to be enabled)
        new_counts_dict = self.get_new_counts_this_frame()

        # DIRECT COUNT from detections list - most reliable source of truth
        raw_detections = counting_summary.get("detections", [])
        detection_count_by_category = {}
        for det in raw_detections:
            cat = det.get("category", "person")
            detection_count_by_category[cat] = detection_count_by_category.get(cat, 0) + 1

        total_counts = [{"category": cat, "count": count} for cat, count in total_counts_dict.items() if count > 0]
        # current_counts: ALL persons currently detected in frame - computed directly from detections
        current_counts = [{"category": cat, "count": count} for cat, count in detection_count_by_category.items()]
        # Fallback: if detection_count_by_category is empty but we have total_detections, use per_category_count
        if not current_counts and total_detections > 0:
            current_counts = [{"category": cat, "count": count} for cat, count in per_category_count.items()]
        # current_new_counts: Only NEW persons who appeared for the first time (requires tracker enabled)
        current_new_counts = [{"category": cat, "count": count} for cat, count in new_counts_dict.items()]

        # ONE concise stats summary line
        curr_total = sum(c.get("count", 0) for c in current_counts)
        new_total = sum(c.get("count", 0) for c in current_new_counts)
        total_total = sum(c.get("count", 0) for c in total_counts)
        print(f"[STATS] F{frame_number} | current={curr_total} new={new_total} total={total_total}")

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
            # Surface pose keypoints (and skeleton_type/track_id/confidence) onto the
            # tracked detection so agg_summary.<frame>.tracking_stats.detections[]
            # carries them, matching the top-level prediction detections[] shape.
            # create_detection_object() has no keypoints slot, so attach directly.
            keypoints = detection.get("keypoints")
            if keypoints is not None:
                detection_obj["keypoints"] = keypoints
                skeleton_type = detection.get("skeleton_type")
                if skeleton_type is not None:
                    detection_obj["skeleton_type"] = skeleton_type
            track_id = detection.get("track_id")
            if track_id is not None and "track_id" not in detection_obj:
                detection_obj["track_id"] = track_id
            confidence = detection.get("confidence")
            if confidence is not None:
                detection_obj["confidence"] = confidence
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
            human_text_lines.append("\t- People Detected by Zone:")
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
                human_text_lines.append(f"\t- Total People in Frame ({cat}): {count}")
                human_text_lines.append(f"\t- New People (just entered) ({cat}): {new_count}")

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
        _config: FallDetectionConfig,
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
        first_cat = self.target_categories[0] if self.target_categories else "vehicle"
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

    def _count_categories(self, detections: list, _config: FallDetectionConfig) -> dict:
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
                    # Pose fields carried through so tracking_stats.detections[]
                    # can surface them (matches top-level prediction detections[]).
                    "keypoints": det.get("keypoints"),
                    "skeleton_type": det.get("skeleton_type"),
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

    @staticmethod
    def _get_frame_height(stream_info: Optional[Dict[str, Any]]) -> Optional[int]:
        """Resolve the stream frame height (pixels) for the vertical-drop signal.

        Looks in ``stream_resolution`` at the top level and under ``input_settings``;
        returns None when unavailable (the drop signal is then skipped).
        """
        if not isinstance(stream_info, dict):
            return None
        res = stream_info.get("stream_resolution")
        if not isinstance(res, dict):
            input_settings = stream_info.get("input_settings", {})
            res = input_settings.get("stream_resolution") if isinstance(input_settings, dict) else None
        if not isinstance(res, dict):
            return None
        height = res.get("height", 0) or 0
        try:
            height = int(height)
        except (TypeError, ValueError):
            return None
        return height if height > 0 else None


"""
Pose-Based Fall Detection
=========================
Post-tracker geometric fall detection (mirrors the standalone YOLO-pose
``fall_detection.py``). Instead of trusting a fall/non_fall classifier, it
confirms a fall only when a strict 3-step sequence happens IN ORDER per person:

  Step 1 - Sudden fast drop: the body center drops more than ``drop_ratio_thresh``
           of the frame height within the short ``drop_window_seconds`` window. A
           slow descent (sitting/lying down) never accumulates enough drop that
           fast, so it is ignored.
  Step 2 - Now flat: posture becomes horizontal (bbox wider-than-tall OR torso
           angle past ``angle_thresh_deg`` from vertical).
  Step 3 - Stayed down: remains horizontal for at least ``stay_down_seconds``
           and does NOT get back up.

Implemented as a per-track state machine: NORMAL -> DROP_SEEN -> DOWN -> FALLEN.
Confirmed falls are relabeled to ``fall_class`` so the downstream
target_categories filter and counting/incident logic pick them up.

Integration:
  In FallDetectionUseCase.process(), after tracker update and before
  _update_tracking_state():
    processed_data = self.fall_detector.update(processed_data, frame_h)
"""


@dataclass
class PoseFallConfig:
    """Configuration for the pose-based (3-step) fall detector."""

    # Torso considered "horizontal" when its angle from vertical exceeds this.
    angle_thresh_deg: float = 45.0
    # box width/height above this means wider-than-tall -> lying.
    aspect_ratio_thresh: float = 1.0
    # Step 1: short window in which a "sudden" drop must occur (long = slow sit, ignored).
    drop_window_seconds: float = 0.6
    # Step 1: fraction of frame height the center must drop within the window.
    drop_ratio_thresh: float = 0.15
    # Step 2: max time to wait after a drop for the body to become horizontal before reset.
    drop_to_down_grace: float = 1.5
    # Step 3: how long they must stay down (not get up) before a fall is confirmed.
    stay_down_seconds: float = 3.0
    # Ignore keypoints the model isn't confident about.
    kpt_conf_thresh: float = 0.3
    # Remove per-track state after this many frames of absence.
    track_eviction_frames: int = 60
    # Category label assigned to a confirmed fall.
    fall_class: str = "fall"
    # Enable/disable the detector entirely.
    enabled: bool = True


class PoseFallDetector:
    """
    Per-track 3-step fall detection (drop -> flat -> stayed down).

    For each tracked person, runs a state machine that requires a sudden fast
    drop, followed by a horizontal posture, followed by staying down for a few
    seconds without getting up. Only then is the detection relabeled to
    ``fall_class``; everything else passes through unchanged.
    """

    def __init__(self, config: Optional[PoseFallConfig] = None):
        self.config = config or PoseFallConfig()

        # Per-person rolling history of (timestamp, center_y_norm) for the drop signal.
        self._history: Dict[Any, deque] = defaultdict(lambda: deque(maxlen=256))
        # Per-person state machine: "NORMAL" | "DROP_SEEN" | "DOWN" | "FALLEN".
        self._phase: Dict[Any, str] = defaultdict(lambda: "NORMAL")
        # Timestamps anchoring the steps.
        self._drop_time: Dict[Any, float] = {}
        self._down_since: Dict[Any, float] = {}
        # Track last-seen frame for eviction.
        self._track_last_seen: Dict[Any, int] = {}
        self._frame_count: int = 0
        self._stats = {"confirmed_falls": 0}

    @staticmethod
    def _box_to_xyxy(bbox: Any) -> Optional[Tuple[float, float, float, float]]:
        """Normalize a bounding box (dict or list) to (x1, y1, x2, y2)."""
        if isinstance(bbox, dict):
            if "x1" in bbox:
                return (bbox["x1"], bbox["y1"], bbox["x2"], bbox["y2"])
            if "xmin" in bbox:
                return (bbox["xmin"], bbox["ymin"], bbox["xmax"], bbox["ymax"])
            vals = [v for v in bbox.values() if isinstance(v, (int, float))]
            return tuple(vals[:4]) if len(vals) >= 4 else None  # type: ignore[return-value]
        if isinstance(bbox, (list, tuple)) and len(bbox) >= 4:
            return (bbox[0], bbox[1], bbox[2], bbox[3])
        return None

    def _torso_angle_from_vertical(self, kps: Optional[List[Tuple[float, float, float]]]) -> Optional[float]:
        """Angle (degrees) of the torso line away from vertical. None if unknown."""
        if kps is None:
            return None
        thresh = self.config.kpt_conf_thresh

        def midpoint(a: int, b: int) -> Optional[Tuple[float, float]]:
            if kps[a][2] < thresh or kps[b][2] < thresh:
                return None
            return ((kps[a][0] + kps[b][0]) / 2.0, (kps[a][1] + kps[b][1]) / 2.0)

        shoulder = midpoint(_KP_LEFT_SHOULDER, _KP_RIGHT_SHOULDER)
        hip = midpoint(_KP_LEFT_HIP, _KP_RIGHT_HIP)
        if shoulder is None or hip is None:
            return None

        # Vector from hips up toward shoulders; 0 deg = perfectly upright.
        dx = shoulder[0] - hip[0]
        dy = shoulder[1] - hip[1]
        return float(math.degrees(math.atan2(abs(dx), abs(dy))))

    def update(self, detections: List[Dict], frame_h: Optional[int] = None) -> List[Dict]:
        """
        Process tracked detections and apply the 3-step fall detection.

        Args:
            detections: detection dicts from the tracker. Each should have
                'track_id', 'bounding_box', and ideally 'keypoints'.
            frame_h: stream frame height in pixels, used to normalize the
                vertical-drop signal (Step 1). Required for the drop step; when
                absent, the drop can't be measured so no fall is confirmed.

        Returns:
            The detections list with confirmed falls relabeled to ``fall_class``.
            Untracked detections pass through unchanged.
        """
        if not self.config.enabled:
            return detections

        self._frame_count += 1
        now = time.time()
        output = []

        for det in detections:
            track_id = det.get("track_id")
            if track_id is None:
                # Cannot run the per-track state machine without a stable id.
                # Keypoints are intentionally preserved on the detection so
                # agg_summary tracking_stats.detections[] can surface them.
                output.append(det)
                continue

            self._track_last_seen[track_id] = self._frame_count

            box = self._box_to_xyxy(det.get("bounding_box", det.get("bbox")))
            if box is None:
                # Keypoints preserved for agg_summary surfacing (see below).
                output.append(det)
                continue
            x1, y1, x2, y2 = box
            width = max(1.0, x2 - x1)
            height = max(1.0, y2 - y1)
            aspect_ratio = width / height

            kps = _extract_coco17_keypoints(det)
            angle = self._torso_angle_from_vertical(kps)
            # Keypoints drive the fall classification here AND are intentionally
            # preserved on the detection dict so they propagate to
            # agg_summary.<frame>.tracking_stats.detections[] (via
            # _count_categories -> _generate_tracking_stats), matching the
            # top-level prediction detections[] shape.

            # Step 2 signal: is the current posture horizontal / flat?
            horizontal_by_box = aspect_ratio > self.config.aspect_ratio_thresh
            horizontal_by_angle = angle is not None and angle > self.config.angle_thresh_deg
            is_horizontal = horizontal_by_box or horizontal_by_angle

            # --- Step 1 (sudden fast drop) TEMPORARILY DISABLED ---------------
            # The model frequently loses the track while a person is mid-fall, so
            # the sudden drop is often never observed -> false negatives. For now
            # we skip the drop gate and confirm on "flat + stayed down" alone.
            # To restore the original 3-step behaviour, uncomment the drop signal
            # and the NORMAL/DROP_SEEN branches below (and remove the bypass).
            sudden_drop = False
            # if frame_h and frame_h > 0:
            #     center_y_norm = ((y1 + y2) / 2.0) / frame_h
            #     hist = self._history[track_id]
            #     hist.append((now, center_y_norm))
            #     window = [y for (t, y) in hist if now - t <= self.config.drop_window_seconds]
            #     if len(window) >= 2:
            #         sudden_drop = (center_y_norm - min(window)) > self.config.drop_ratio_thresh

            # State machine (drop step bypassed): NORMAL -> DOWN -> FALLEN.
            phase = self._phase[track_id]
            # if phase == "NORMAL":
            #     if sudden_drop:
            #         phase = "DROP_SEEN"
            #         self._drop_time[track_id] = now
            # elif phase == "DROP_SEEN":
            #     if is_horizontal:
            #         phase = "DOWN"
            #         self._down_since[track_id] = now
            #     elif now - self._drop_time.get(track_id, now) > self.config.drop_to_down_grace:
            #         phase = "NORMAL"  # dropped but never went flat -> not a fall
            if phase in ("NORMAL", "DROP_SEEN"):
                # No drop required: as soon as the posture is flat, start the timer.
                if is_horizontal:
                    phase = "DOWN"
                    self._down_since[track_id] = now
            elif phase == "DOWN":
                if not is_horizontal:
                    phase = "NORMAL"  # got back up -> no fall
                elif now - self._down_since.get(track_id, now) >= self.config.stay_down_seconds:
                    phase = "FALLEN"
            elif phase == "FALLEN":
                if not is_horizontal:
                    phase = "NORMAL"  # recovered / stood back up
            self._phase[track_id] = phase
            confirmed_fall = phase == "FALLEN"

            # Telemetry for downstream consumers / debugging.
            det["aspect_ratio"] = round(aspect_ratio, 2)
            det["torso_angle"] = None if angle is None else round(angle, 1)
            det["sudden_drop"] = sudden_drop
            det["fall_phase"] = phase

            if confirmed_fall:
                det["category"] = self.config.fall_class
                det["_fall_confirmed"] = True
                self._stats["confirmed_falls"] += 1

            output.append(det)

        # Periodic eviction of stale tracks.
        if self._frame_count % 30 == 0:
            self._evict_stale_tracks()

        return output

    def _evict_stale_tracks(self):
        """Remove state for tracks not seen recently."""
        eviction_threshold = self._frame_count - self.config.track_eviction_frames
        stale_ids = [tid for tid, last_seen in self._track_last_seen.items() if last_seen < eviction_threshold]
        for tid in stale_ids:
            self._history.pop(tid, None)
            self._phase.pop(tid, None)
            self._drop_time.pop(tid, None)
            self._down_since.pop(tid, None)
            self._track_last_seen.pop(tid, None)

    def get_stats(self) -> Dict[str, Any]:
        """Return detector statistics."""
        return {
            "confirmed_falls": self._stats["confirmed_falls"],
            "active_tracks": len(self._track_last_seen),
            "frame_count": self._frame_count,
        }

    def reset(self):
        """Reset all state. Call when switching streams or restarting."""
        self._history.clear()
        self._phase.clear()
        self._drop_time.clear()
        self._down_since.clear()
        self._track_last_seen.clear()
        self._frame_count = 0
        self._stats = {"confirmed_falls": 0}
