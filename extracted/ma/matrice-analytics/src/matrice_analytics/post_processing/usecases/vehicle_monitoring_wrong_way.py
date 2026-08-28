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
from ..utils.geometry_utils import get_bbox_bottom25_center, point_in_polygon
from ..utils.incident_manager_utils import INCIDENT_MANAGER, IncidentManagerFactory
from ..utils.wrong_way_tracker import WrongWayDetectionTracker

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


def _max_wrong_way_confidence_pct(detections: List[Dict]) -> float:
    """Map max wrong-way trajectory confidence to 0-100 (incident_quant for INCIDENT_MANAGER)."""
    if not detections:
        return 0.0
    max_conf = max(float(d.get("wrong_way_confidence", 0.0) or 0.0) for d in detections)
    return min(100.0, max_conf * 100.0)


@dataclass
class VehicleMonitoringWrongWayConfig(BaseConfig):
    """Configuration for wrong-way vehicle detection use case."""

    enable_smoothing: bool = True
    smoothing_algorithm: str = "observability"
    smoothing_window_size: int = 20
    smoothing_cooldown_frames: int = 5
    smoothing_confidence_range_factor: float = 0.5
    confidence_threshold: float = 0.6

    # Class Aggregation: Configuration parameters
    enable_class_aggregation: bool = True
    class_aggregation_window_size: int = 30  # 30 frames ≈ 1 second at 30 FPS

    # Wrong-Way Detection Settings (Trajectory-Based)
    enable_wrong_way_detection: bool = True

    wrong_way_confidence_suspect: float = 0.3  # Threshold to enter SUSPECT state
    wrong_way_confidence_confirm: float = 0.7  # Threshold to confirm WRONG_WAY
    wrong_way_min_velocity: float = 2.0  # Min velocity (pixels/frame) to consider motion
    auto_ref_min_tracks: int = 5  # Min tracks needed for auto-estimation
    stale_track_frames: int = 30

    # No zone analytics in this use case's default deployment shape — the
    # wrong-way reference direction is auto-learned from observed traffic
    # (see WrongWayDetectionTracker). zone_config is only for deployments that
    # explicitly want a USER_ZONE reference (_setup_reference_from_zone reads
    # it unconditionally, regardless of enable_wrong_way_detection/has_zones),
    # so it must default to None rather than a hardcoded test polygon.
    zone_config: Optional[Dict[str, Any]] = None

    usecase_categories: List[str] = field(
        default_factory=lambda: ["bicycle", "motorcycle", "car", "van", "bus", "truck"]
    )

    target_categories: List[str] = field(
        default_factory=lambda: ["bicycle", "motorcycle", "car", "van", "bus", "truck"]
    )
    alert_config: Optional[AlertConfig] = None
    index_to_category: Optional[Dict[int, str]] = field(
        default_factory=lambda: {
            0: "bicycle",
            1: "motorcycle",
            2: "car",
            3: "van",
            4: "bus",
            5: "truck",
        }
    )

    # Incident-manager wiring.
    session: Optional[Any] = None
    server_id: Optional[str] = None


class VehicleMonitoringWrongWayUseCase(BaseProcessor):
    CATEGORY_DISPLAY = {
        "bicycle": "Bicycle",
        "motorcycle": "Motorcycle",
        "car": "Car",
        "van": "Van",
        "bus": "Bus",
        "truck": "Truck",
    }
    _INCIDENT_LOG = "[INCIDENT_MANAGER]"

    def __init__(self):
        super().__init__("vehicle_monitoring_wrong_way")
        self.category = "traffic"
        self.CASE_TYPE: Optional[str] = "vehicle_monitoring_wrong_way"
        self.CASE_VERSION: Optional[str] = "1.0"
        self.target_categories = ["bicycle", "motorcycle", "car", "van", "bus", "truck"]
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

        # Incident manager.
        self._incident_manager_factory: Optional[IncidentManagerFactory] = None
        self._incident_manager: Optional[INCIDENT_MANAGER] = None
        self._incident_manager_initialized: bool = False
        self._legacy_redis_publisher: Any = None

        # Wrong-way detection tracker (NEW)
        self.wrong_way_tracker = None
        # Reference direction tracking (for zone-based reference)
        self._reference_zone_name: Optional[str] = None
        self._reference_zone_polygon: Optional[List[List[float]]] = None

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

    def _get_legacy_redis_publisher(self) -> Any:
        if self._legacy_redis_publisher is None:
            from ...analytics.redis_publisher import AnalyticsRedisPublisher

            self._legacy_redis_publisher = AnalyticsRedisPublisher()
        return self._legacy_redis_publisher

    # ---- Incident manager lifecycle ---------------------------------------

    def _initialize_incident_manager_once(self, config: VehicleMonitoringWrongWayConfig) -> None:
        if self._incident_manager_initialized:
            return
        try:
            self.logger.info(f"{self._INCIDENT_LOG} Initializing incident manager for wrong-way detection...")
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
        if not incident:
            if context is not None:
                context.metadata["incident_published_via_manager"] = False
            return False

        published = False
        camera_id = _resolve_manager_camera_id(stream_info)
        if self._incident_manager:
            try:
                published = bool(
                    self._incident_manager.process_incident(
                        camera_id=camera_id,
                        incident_data=incident,
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
        elif not published:
            try:
                from ..utils.legacy_analytics_bridge import get_legacy_session

                stream_key = str((stream_info or {}).get("stream_key") or "default_stream")
                session = get_legacy_session(stream_key)
                published = session.maybe_publish_incident(
                    incident,
                    stream_info,
                    usecase=self.name,
                    app_name=None,
                    publisher=self._get_legacy_redis_publisher(),
                    camera_id=camera_id,
                )
                if published:
                    self.logger.info(
                        f"{self._INCIDENT_LOG} Incident published via legacy Redis bridge for camera: {camera_id}"
                    )
            except Exception as e:
                self.logger.error(
                    f"{self._INCIDENT_LOG} Legacy Redis incident publish failed: {e}",
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

        # Config validation
        is_valid_config = isinstance(config, VehicleMonitoringWrongWayConfig) or (
            hasattr(config, "usecase") and hasattr(config, "category")
        )
        if not is_valid_config:
            self.logger.error(
                f"Config validation failed in vehicle_monitoring_wrong_way. "
                f"Got type={type(config).__name__}, module={type(config).__module__}, "
                f"usecase={getattr(config, 'usecase', 'N/A')}, category={getattr(config, 'category', 'N/A')}"
            )
            return self.create_error_result(
                f"Invalid config type: expected VehicleMonitoringWrongWayConfig or config with usecase='vehicle_monitoring_wrong_way', "
                f"got {type(config).__name__} with usecase={getattr(config, 'usecase', 'N/A')}",
                usecase=self.name,
                category=self.category,
                context=context,
            )

        if not self._incident_manager_initialized:
            self._initialize_incident_manager_once(config)

        if context is None:
            context = ProcessingContext()

        # Determine if zones are configured
        has_zones = (
            bool(config.zone_config and config.zone_config.get("zones")) and not config.enable_wrong_way_detection
        )

        # Normalize YOLO outputs to internal schema
        data = self._normalize_yolo_results(data, getattr(config, "index_to_category", None))

        input_format = match_results_structure(data)
        context.input_format = input_format
        context.confidence_threshold = config.confidence_threshold
        config.confidence_threshold = 0.25
        # TODO: param to be updated

        if config.confidence_threshold is not None:
            processed_data = filter_by_confidence(data, config.confidence_threshold)
            self.logger.debug(f"Applied confidence filtering with threshold {config.confidence_threshold}")
        else:
            processed_data = data

        if config.index_to_category:
            processed_data = apply_category_mapping(processed_data, config.index_to_category)
            self.logger.debug("Applied category mapping")

        processed_data = [d for d in processed_data if d.get("category") in self.target_categories]
        self.logger.debug("Applied category filtering")

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
                # derive_from_confidence=False: this config's confidence_threshold
                # defaults to 0.6 (non-None), and the ORIGINAL code never applied
                # confidence-derived thresholds here (only class-aggregation
                # passthrough) -- letting the seam's default derive_from_confidence
                # apply would silently retune track_high/low/new_thresh.
                self.tracker = self._tracker_seam.get_shared_tracker(
                    config,
                    stream_info,
                    profile=TrackerProfile.DEFAULT,
                    derive_from_confidence=False,
                    enable_class_aggregation=config.enable_class_aggregation,
                    class_aggregation_window_size=config.class_aggregation_window_size,
                )
            processed_data = self.tracker.update(processed_data)
        except Exception as e:
            self.logger.warning(f"AdvancedTracker failed: {e}")

        # WRONG-WAY DETECTION
        wrong_way_analytics = None
        if config.enable_wrong_way_detection and processed_data:
            if self.wrong_way_tracker is None:
                self.wrong_way_tracker = WrongWayDetectionTracker(
                    v_min=config.wrong_way_min_velocity,
                    c_suspect=config.wrong_way_confidence_suspect,
                    c_confirm=config.wrong_way_confidence_confirm,
                    stale_track_frames=config.stale_track_frames,
                    auto_ref_min_tracks=config.auto_ref_min_tracks,
                )
                self.logger.info(
                    f"Initialized WrongWayDetectionTracker v2: "
                    f"v_min={config.wrong_way_min_velocity}, "
                    f"c_suspect={config.wrong_way_confidence_suspect}, "
                    f"c_confirm={config.wrong_way_confidence_confirm}"
                )

                self._setup_reference_from_zone(config)

            wrong_way_analytics = self.wrong_way_tracker.update(
                detections=processed_data, current_frame=self._total_frame_counter
            )

            ww_count = wrong_way_analytics.get("current_wrong_way_count", 0)
            suspect_count = wrong_way_analytics.get("current_suspect_count", 0)
            ref_status = wrong_way_analytics.get("reference_status", "NONE")

            if ww_count > 0 or suspect_count > 0:
                self.logger.info(
                    f"[Frame {self._total_frame_counter}] Wrong-Way: "
                    f"ref={ref_status}, wrong_way={ww_count}, suspect={suspect_count}, "
                    f"total={wrong_way_analytics.get('total_wrong_way_count', 0)}"
                )

        # Update tracking state
        self._update_tracking_state(processed_data, has_zones=has_zones)
        self._total_frame_counter += 1

        # Extract frame number
        frame_number = None
        if stream_info:
            input_settings = stream_info.get("input_settings", {})
            start_frame = input_settings.get("start_frame")
            end_frame = input_settings.get("end_frame")
            if start_frame is not None and end_frame is not None and start_frame == end_frame:
                frame_number = start_frame

        # Calculate summaries
        counting_summary = self._count_categories(processed_data, config)
        total_counts = self.get_total_counts()
        counting_summary["total_counts"] = total_counts
        counting_summary["categories"] = {}
        for detection in processed_data:
            category = detection.get("category", "unknown")
            counting_summary["categories"][category] = counting_summary["categories"].get(category, 0) + 1

        # Zone analysis (if configured)
        zone_analysis = {}
        if has_zones:
            frame_data = processed_data
            zone_analysis = count_objects_in_zones(frame_data, config.zone_config["zones"], stream_info)
            if zone_analysis:
                enhanced_zone_analysis = self._update_zone_tracking(zone_analysis, processed_data, config)
                for zone_name, enhanced_data in enhanced_zone_analysis.items():
                    zone_analysis[zone_name] = enhanced_data
                per_category_count = {
                    cat: len(self._current_frame_track_ids.get(cat, set())) for cat in self.target_categories
                }
                counting_summary["per_category_count"] = {k: v for k, v in per_category_count.items() if v > 0}
                counting_summary["total_count"] = sum(per_category_count.values())

        # Generate outputs
        alerts = self._check_alerts(counting_summary, zone_analysis, frame_number, config)
        self._extract_predictions(processed_data)
        incidents_list = self._generate_incidents(
            counting_summary,
            zone_analysis,
            alerts,
            config,
            frame_number,
            stream_info,
            wrong_way_analytics,
        )

        tracking_stats_list = self._generate_tracking_stats(
            counting_summary,
            zone_analysis,
            alerts,
            config,
            frame_number,
            stream_info,
            wrong_way_analytics,
        )

        business_analytics_list = self._generate_business_analytics(
            counting_summary, zone_analysis, alerts, config, stream_info, wrong_way_analytics, is_empty=False
        )

        summary_list = self._generate_summary(
            counting_summary,
            zone_analysis,
            incidents_list,
            tracking_stats_list,
            business_analytics_list,
            alerts,
        )

        # Assemble output
        incidents = incidents_list[0] if incidents_list else {}
        self._send_incident_to_manager(incidents, stream_info, context=context)
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

        # Log performance
        proc_time = time.time() - processing_start
        processing_latency_ms = proc_time * 1000.0
        processing_fps = (1.0 / proc_time) if proc_time > 0 else None
        print(
            f"latency in ms: {processing_latency_ms} | Throughput fps: {processing_fps} | Frame_Number: {self._total_frame_counter}"
        )

        return result

    def _generate_incidents(
        self,
        _counting_summary: Dict,
        _zone_analysis: Dict,
        alerts: List,
        config: VehicleMonitoringWrongWayConfig,
        frame_number: Optional[int] = None,
        stream_info: Optional[Dict[str, Any]] = None,
        wrong_way_analytics: Optional[Dict] = None,
    ) -> List[Dict]:
        """Generate an incident event when a vehicle is confirmed (or suspected) wrong-way."""
        _ = (_counting_summary, _zone_analysis)
        incidents: List[Dict] = []
        current_wrong_way = (wrong_way_analytics or {}).get("current_wrong_way_count", 0)
        current_suspect = (wrong_way_analytics or {}).get("current_suspect_count", 0)
        wrong_way_detections = (wrong_way_analytics or {}).get("current_wrong_way_detections", [])
        suspect_detections = (wrong_way_analytics or {}).get("current_suspect_detections", [])

        if current_wrong_way <= 0 and current_suspect <= 0:
            self._ascending_alert_list.append(0)
            incidents.append({})
            return incidents

        self._ascending_alert_list = (
            self._ascending_alert_list[-900:] if len(self._ascending_alert_list) > 900 else self._ascending_alert_list
        )

        current_timestamp = self._get_current_timestamp_str(stream_info)
        start_timestamp = self._get_start_timestamp_str(stream_info)
        camera_info = self.get_camera_info_from_stream(stream_info)

        # A confirmed wrong-way vehicle is a significant safety event on its own;
        # a suspect (trajectory not yet confirmed) is a lower-confidence leading
        # indicator. incident_quant (below) lets a per-camera ThresholdConfig
        # dynamically override this fallback level.
        if current_wrong_way > 0:
            level = "significant"
            self._ascending_alert_list.append(2)
        else:
            level = "low"
            self._ascending_alert_list.append(1)

        human_text_lines = [f"WRONG-WAY DRIVING DETECTED @ {current_timestamp}:"]
        human_text_lines.append(f"\tSeverity Level: {level}")
        human_text_lines.append(f"\tCurrent Wrong-Way Vehicles: {current_wrong_way}")
        human_text_lines.append(f"\tCurrent Suspects: {current_suspect}")
        for det in wrong_way_detections:
            human_text_lines.append(
                f"\t\t- [WRONG-WAY] {det.get('category')} (ID:{det.get('track_id')}, "
                f"conf:{det.get('wrong_way_confidence', 0):.2f})"
            )
        for det in suspect_detections:
            human_text_lines.append(
                f"\t\t- [SUSPECT] {det.get('category')} (ID:{det.get('track_id')}, "
                f"conf:{det.get('wrong_way_confidence', 0):.2f})"
            )
        human_text = "\n".join(human_text_lines)

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
        # Real trajectory-confidence-based quant so a per-camera ThresholdConfig
        # can dynamically override the level fallback above - mirrors
        # drone_detection.py's _max_drone_confidence_pct pattern.
        event["incident_quant"] = _max_wrong_way_confidence_pct(wrong_way_detections or suspect_detections)
        incidents.append(event)
        return incidents

    def _generate_tracking_stats(
        self,
        counting_summary: Dict,
        zone_analysis: Dict,
        alerts: List,
        config: VehicleMonitoringWrongWayConfig,
        _frame_number: Optional[int] = None,
        stream_info: Optional[Dict[str, Any]] = None,
        wrong_way_analytics: Optional[Dict] = None,
    ) -> List[Dict]:
        """Generate tracking statistics including wrong-way analytics."""
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
        current_counts = [{"category": cat, "count": count} for cat, count in per_category_count.items() if count > 0]

        # Build detections list
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
            else:
                detection_obj = self.create_detection_object(category, bbox)
            detections.append(detection_obj)

        # Alert settings
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

        # === BUILD HUMAN TEXT ===
        human_text_lines = []
        human_text_lines.append(f"CURRENT FRAME @ {current_timestamp}:")

        # Display current counts
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
            human_text_lines.append(f"\t- Vehicles Detected: {total_detections}")
            if per_category_count:
                for cat, count in per_category_count.items():
                    if count > 0:
                        human_text_lines.append(f"\t\t- {cat}: {count}")

        # === WRONG-WAY ANALYTICS IN HUMAN TEXT ===
        if wrong_way_analytics:
            ref_source = wrong_way_analytics.get("reference_source", "NONE")
            ref_status = wrong_way_analytics.get("reference_status", "NONE")
            current_wrong_way = wrong_way_analytics.get("current_wrong_way_count", 0)
            total_wrong_way = wrong_way_analytics.get("total_wrong_way_count", 0)
            current_suspect = wrong_way_analytics.get("current_suspect_count", 0)

            human_text_lines.append("")
            human_text_lines.append("WRONG-WAY DETECTION:")
            human_text_lines.append(f"\t- Reference: {ref_source} ({ref_status})")

            if ref_status == "LEARNING":
                human_text_lines.append("\t- Status: Learning traffic pattern...")
            else:
                human_text_lines.append(f"\t- Current Wrong-Way: {current_wrong_way}")
                human_text_lines.append(f"\t- Total Wrong-Way Events: {total_wrong_way}")
                human_text_lines.append(f"\t- Current Suspects: {current_suspect}")

                # List wrong-way vehicles with confidence
                for det in wrong_way_analytics.get("current_wrong_way_detections", []):
                    human_text_lines.append(
                        f"\t\t- [WRONG-WAY] {det['category']} (ID:{det['track_id']}, "
                        f"conf:{det.get('wrong_way_confidence', 0):.2f})"
                    )

                # List suspect vehicles
                for det in wrong_way_analytics.get("current_suspect_detections", []):
                    human_text_lines.append(
                        f"\t\t- [SUSPECT] {det['category']} (ID:{det['track_id']}, "
                        f"conf:{det.get('wrong_way_confidence', 0):.2f})"
                    )

        human_text_lines.append("")
        human_text = "\n".join(human_text_lines)

        # Build tracking stat
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

        # NOTE : Add wrong-way analytics to tracking stats
        if wrong_way_analytics:
            tracking_stat["wrong_way_analytics"] = {
                "reference_source": wrong_way_analytics.get("reference_source", "NONE"),
                "reference_status": wrong_way_analytics.get("reference_status", "NONE"),
                "current_wrong_way_count": wrong_way_analytics.get("current_wrong_way_count", 0),
                "total_wrong_way_count": wrong_way_analytics.get("total_wrong_way_count", 0),
                "current_wrong_way_detections": wrong_way_analytics.get("current_wrong_way_detections", []),
                "current_suspect_count": wrong_way_analytics.get("current_suspect_count", 0),
                "current_suspect_detections": wrong_way_analytics.get("current_suspect_detections", []),
            }
            self.logger.debug(
                f"Wrong-way analytics: ref={wrong_way_analytics.get('reference_status')}, "
                f"wrong_way={wrong_way_analytics.get('current_wrong_way_count', 0)}, "
                f"suspect={wrong_way_analytics.get('current_suspect_count', 0)}"
            )

        tracking_stats.append(tracking_stat)
        return tracking_stats

    def _setup_reference_from_zone(self, config: VehicleMonitoringWrongWayConfig) -> None:
        """Extract reference direction from zone_config (first point → last point)."""

        if not config.zone_config or not config.zone_config.get("zones"):
            self.logger.info("No zone_config provided — using auto-reference estimation")
            return

        zones = config.zone_config["zones"]

        # Use the first zone as reference direction source
        for zone_name, zone_polygon in zones.items():
            if zone_polygon and len(zone_polygon) >= 2:
                self._reference_zone_name = zone_name
                self._reference_zone_polygon = zone_polygon

                success = self.wrong_way_tracker.set_reference_from_zone(zone_polygon)

                if success:
                    self.logger.info(
                        f"Reference direction set from zone '{zone_name}': "
                        f"first={zone_polygon[0]} → last={zone_polygon[-1]}"
                    )
                else:
                    self.logger.warning(f"Failed to set reference from zone '{zone_name}'")

                break

    def _update_zone_tracking(
        self,
        zone_analysis: Dict[str, Dict[str, int]],
        detections: List[Dict],
        config: VehicleMonitoringWrongWayConfig,
    ) -> Dict[str, Dict[str, Any]]:
        """Update zone tracking with current frame data."""
        if not zone_analysis or not config.zone_config or not config.zone_config["zones"]:
            return {}

        enhanced_zone_analysis = {}
        zones = config.zone_config["zones"]

        track_to_cat = {
            det.get("track_id"): det.get("category") for det in detections if det.get("track_id") is not None
        }
        current_frame_zone_tracks = {}

        for zone_name in zones.keys():
            current_frame_zone_tracks[zone_name] = set()
            if zone_name not in self._zone_current_track_ids:
                self._zone_current_track_ids[zone_name] = set()
            if zone_name not in self._zone_total_track_ids:
                self._zone_total_track_ids[zone_name] = set()

        for detection in detections:
            track_id = detection.get("track_id")
            if track_id is None:
                continue

            bbox = detection.get("bounding_box", detection.get("bbox"))
            if not bbox:
                continue

            center_point = get_bbox_bottom25_center(bbox)
            in_any_zone = False

            for zone_name, zone_polygon in zones.items():
                polygon_points = [(point[0], point[1]) for point in zone_polygon]
                if point_in_polygon(center_point, polygon_points):
                    current_frame_zone_tracks[zone_name].add(track_id)
                    in_any_zone = True
                    if track_id not in self._total_count_list:
                        self._total_count_list.append(track_id)

            if in_any_zone:
                cat = track_to_cat.get(track_id)
                if cat:
                    self._current_frame_track_ids.setdefault(cat, set()).add(track_id)
                    if track_id not in self._tracked_in_zones:
                        self._tracked_in_zones.add(track_id)
                        self._per_category_total_track_ids.setdefault(cat, set()).add(track_id)

        for zone_name, zone_counts in zone_analysis.items():
            current_tracks = current_frame_zone_tracks.get(zone_name, set())
            self._zone_current_track_ids[zone_name] = current_tracks
            self._zone_total_track_ids[zone_name].update(current_tracks)
            self._zone_current_counts[zone_name] = len(current_tracks)
            self._zone_total_counts[zone_name] = len(self._zone_total_track_ids[zone_name])

            enhanced_zone_analysis[zone_name] = {
                "current_count": self._zone_current_counts[zone_name],
                "total_count": self._zone_total_counts[zone_name],
                "current_track_ids": list(current_tracks),
                "total_track_ids": list(self._zone_total_track_ids[zone_name]),
                "original_counts": zone_counts,
            }

        return enhanced_zone_analysis

    def _normalize_yolo_results(self, data: Any, index_to_category: Optional[Dict[int, str]] = None) -> Any:
        """Normalize YOLO-style outputs to internal detection schema."""

        def to_bbox_dict(d: Dict[str, Any]) -> Dict[str, Any]:
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
            if "xywh" in d and isinstance(d["xywh"], (list, tuple)) and len(d["xywh"]) >= 4:
                cx, cy, w, h = d["xywh"][:4]
                return {
                    "x1": cx - w / 2,
                    "y1": cy - h / 2,
                    "x2": cx + w / 2,
                    "y2": cy + h / 2,
                }
            return {}

        def resolve_category(d: Dict[str, Any]) -> Tuple[str, Optional[int]]:
            raw_cls = d.get("category", d.get("category_id", d.get("class", d.get("cls"))))
            label_name = d.get("name")
            if isinstance(raw_cls, int):
                if index_to_category and raw_cls in index_to_category:
                    return index_to_category[raw_cls], raw_cls
                return str(raw_cls), raw_cls
            if isinstance(raw_cls, str):
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
            for key in ("track_id", "frame_id", "masks", "segmentation"):
                if key in det:
                    normalized[key] = det[key]
            return normalized

        if isinstance(data, list):
            return [normalize_det(d) if isinstance(d, dict) else d for d in data]
        if isinstance(data, dict):
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
        config: VehicleMonitoringWrongWayConfig,
    ) -> List[Dict]:
        """Check for alert conditions."""
        _ = (_zone_analysis,)
        alerts = []
        if not config.alert_config:
            return alerts

        total_detections = summary.get("total_count", 0)
        per_category_count = summary.get("per_category_count", {})
        frame_key = str(frame_number) if frame_number is not None else "current_frame"

        if hasattr(config.alert_config, "count_thresholds") and config.alert_config.count_thresholds:
            for category, threshold in config.alert_config.count_thresholds.items():
                if category == "all" and total_detections > threshold:
                    alerts.append(
                        {
                            "alert_type": getattr(config.alert_config, "alert_type", ["Default"]),
                            "alert_id": f"alert_{category}_{frame_key}",
                            "incident_category": self.CASE_TYPE,
                            "threshold_level": threshold,
                            "settings": {},
                        }
                    )
                elif category in per_category_count and per_category_count[category] > threshold:
                    alerts.append(
                        {
                            "alert_type": getattr(config.alert_config, "alert_type", ["Default"]),
                            "alert_id": f"alert_{category}_{frame_key}",
                            "incident_category": self.CASE_TYPE,
                            "threshold_level": threshold,
                            "settings": {},
                        }
                    )
        return alerts

    def _generate_business_analytics(
        self,
        _counting_summary: Dict,
        _zone_analysis: Dict,
        _alerts: Any,
        _config: VehicleMonitoringWrongWayConfig,
        _stream_info: Optional[Dict[str, Any]] = None,
        wrong_way_analytics: Optional[Dict] = None,
        is_empty=False,
    ) -> List[Dict]:
        """Generate business analytics: frame vehicle composition + wrong-way counts.

        Sourced from the same counting_summary / wrong_way_analytics the frame
        already computed for tracking_stats/incidents — this is the slice the
        app-store demo pipeline (migration.py / aggregate_frames.py) reads as
        per-frame numeric KPIs, distinct from the legacy bridge's results-agg
        path which reads tracking_stats directly.
        """
        _ = (_alerts, _config, _zone_analysis)
        if is_empty:
            return []

        wrong_way_analytics = wrong_way_analytics or {}
        per_category_count = _counting_summary.get("per_category_count", {})

        return [
            {
                "analysis_name": self.CASE_TYPE,
                "vehicle_count": _counting_summary.get("total_count", 0),
                "current_wrong_way_count": wrong_way_analytics.get("current_wrong_way_count", 0),
                "total_wrong_way_events": wrong_way_analytics.get("total_wrong_way_count", 0),
                "current_suspect_count": wrong_way_analytics.get("current_suspect_count", 0),
                "car_count": per_category_count.get("car", 0),
                "truck_count": per_category_count.get("truck", 0),
                "bus_count": per_category_count.get("bus", 0),
                "van_count": per_category_count.get("van", 0),
                "motorcycle_count": per_category_count.get("motorcycle", 0),
                "bicycle_count": per_category_count.get("bicycle", 0),
            }
        ]

    def _generate_summary(
        self,
        _summary: dict,
        _zone_analysis: Dict,
        incidents: List,
        tracking_stats: List,
        business_analytics: List,
        _alerts: List,
    ) -> List[str]:
        """Generate human-readable summary."""
        _ = (_alerts, _summary, _zone_analysis)
        lines = []
        lines.append(f"Application Name: {self.CASE_TYPE}")
        lines.append(f"Application Version: {self.CASE_VERSION}")
        if len(incidents) > 0:
            lines.append(f"Incidents: \n\t{incidents[0].get('human_text', 'No incidents detected')}")
        if len(tracking_stats) > 0:
            lines.append(
                f"Tracking Statistics: \t{tracking_stats[0].get('human_text', 'No tracking statistics detected')}"
            )
        if len(business_analytics) > 0:
            lines.append(
                f"Business Analytics: \t{business_analytics[0].get('human_text', 'No business analytics detected')}"
            )
        if len(incidents) == 0 and len(tracking_stats) == 0 and len(business_analytics) == 0:
            lines.append("Summary: No Summary Data")
        return ["\n".join(lines)]

    def _get_track_ids_info(self, detections: list) -> Dict[str, Any]:
        """Get track ID information."""
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
        """Update tracking state with canonical ID merging."""
        if not hasattr(self, "_per_category_total_track_ids"):
            self._per_category_total_track_ids = {cat: set() for cat in self.target_categories}
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
            self._current_frame_track_ids.setdefault(cat, set()).add(canonical_id)

    def get_total_counts(self):
        """Get total counts per category."""
        return {cat: len(ids) for cat, ids in getattr(self, "_per_category_total_track_ids", {}).items()}

    def _count_categories(self, detections: list, _config: VehicleMonitoringWrongWayConfig) -> dict:
        """Count detections per category."""
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
        """Extract predictions from detections."""
        return [
            {
                "category": det.get("category", "unknown"),
                "confidence": det.get("confidence", 0.0),
                "bounding_box": det.get("bounding_box", {}),
            }
            for det in detections
        ]

    def _format_timestamp_for_stream(self, timestamp: float) -> str:
        """Format timestamp for stream output."""
        dt = datetime.fromtimestamp(timestamp, tz=timezone.utc)
        return dt.strftime("%Y:%m:%d %H:%M:%S")

    def _format_timestamp_for_video(self, timestamp: float) -> str:
        """Format timestamp for video output."""
        hours = int(timestamp // 3600)
        minutes = int((timestamp % 3600) // 60)
        seconds = round(float(timestamp % 60), 2)
        return f"{hours:02d}:{minutes:02d}:{seconds:.1f}"

    def _format_timestamp(self, timestamp: Any) -> str:
        """Format timestamp to standard format."""
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
            # Non-fatal: exception ignored here; execution continues per surrounding logic.
            pass
        return timestamp_clean

    def _get_current_timestamp_str(
        self,
        stream_info: Optional[Dict[str, Any]],
        precision=False,
        _frame_id: Optional[str] = None,
    ) -> str:
        """Get formatted current timestamp based on stream type."""
        _ = (_frame_id,)
        if not stream_info:
            return "00:00:00.00"

        if precision:
            if stream_info.get("input_settings", {}).get("start_frame", "na") != "na":
                return self._format_timestamp(stream_info.get("input_settings", {}).get("stream_time", "NA"))
            else:
                return datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")

        if stream_info.get("input_settings", {}).get("start_frame", "na") != "na":
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
