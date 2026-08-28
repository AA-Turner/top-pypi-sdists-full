import threading
import time
from dataclasses import dataclass, field, replace
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from ..core.base import (
    BaseProcessor,
    ConfigProtocol,
    ProcessingContext,
    ProcessingResult,
)
from ..core.config import AlertConfig, BaseConfig, ZoneConfig
from ..Trackers import ConfigDrivenTracker, TrackerProfile
from ..utils import (
    BBoxSmoothingConfig,
    BBoxSmoothingTracker,
    apply_category_mapping,
    bbox_smoothing,
    filter_by_confidence,
    match_results_structure,
)
from ..utils.geometry_utils import get_bbox_bottom25_center, point_in_polygon
from ..utils.post_processing_config_client import PostProcessingConfigClient


@dataclass
class PedestrianDetectionConfig(BaseConfig):
    """Configuration for pedestrian detection use case in pedestrian monitoring."""

    # Smoothing configuration
    enable_smoothing: bool = True
    smoothing_algorithm: str = "observability"  # "window" or "observability"
    smoothing_window_size: int = 20
    smoothing_cooldown_frames: int = 5
    smoothing_confidence_range_factor: float = 0.5

    # confidence thresholds
    confidence_threshold: float = 0.6

    usecase_categories: List[str] = field(default_factory=lambda: ["ped"])

    target_categories: List[str] = field(default_factory=lambda: ["ped"])

    alert_config: Optional[AlertConfig] = None
    zone_config: Optional[ZoneConfig] = None

    index_to_category: Optional[Dict[int, str]] = field(
        default_factory=lambda: {
            0: "person",
        }
    )


class PedestrianDetectionUseCase(BaseProcessor):
    # Human-friendly display names for categories
    CATEGORY_DISPLAY = {
        "person": "Pedestrian",
    }

    def __init__(self):
        super().__init__("pedestrian_detection")
        self.category = "pedestrian"

        self.CASE_TYPE: Optional[str] = "pedestrian_detection"
        self.CASE_VERSION: Optional[str] = "1.3"

        # List of  categories to track
        self.target_categories = ["person"]

        # Initialize smoothing tracker
        self.smoothing_tracker = None

        # Initialize advanced tracker (will be created on first use)
        self.tracker = None
        self._tracker_seam = ConfigDrivenTracker()

        # Initialize tracking state variables
        self._total_frame_counter = 0
        self._global_frame_offset = 0

        # Track start time for "TOTAL SINCE" calculation
        self._tracking_start_time = None
        self.start_timer = None

        self._track_aliases: Dict[Any, Any] = {}
        self._canonical_tracks: Dict[Any, Dict[str, Any]] = {}
        self._track_merge_iou_threshold: float = 0.2
        self._track_merge_time_window: float = 4.0

        self._consecutive_track_frames: Dict[str, Dict[Any, int]] = {}
        self._min_confirm_frames: int = 3

        self._ascending_alert_list: List[int] = []
        self.current_incident_end_timestamp: str = "N/A"

        # Zone-based tracking storage
        self._zone_current_track_ids: Dict[str, set] = {}
        self._zone_total_track_ids: Dict[str, set] = {}
        self._zone_current_counts: Dict[str, int] = {}
        self._zone_total_counts: Dict[str, int] = {}
        self._zone_new_counts: Dict[str, int] = {}

        # API-resolved geometry config client state
        self._config_client: Optional[PostProcessingConfigClient] = None
        self._resolved_geometry_cache: Optional[PedestrianDetectionConfig] = None
        self._geometry_thread: Optional[threading.Thread] = None

    def set_config_client(self, client: Optional[PostProcessingConfigClient]) -> None:
        """Set the PostProcessingConfigClient used to resolve zones from API (by_app_deployment, camera_id)."""
        self._config_client = client

    def _start_geometry_resolver(self, config: PedestrianDetectionConfig, stream_info: Dict[str, Any]) -> None:
        """Spawn a daemon thread that resolves geometry from the API.

        On success the cache is updated and the thread exits.
        On failure it retries every 30 seconds.
        Never blocks the calling (frame-processing) thread.
        """
        if self._geometry_thread is not None:
            return  # already running

        def _resolver():
            while True:
                try:
                    result = self._resolve_geometry_from_api(config, stream_info)
                    if result is not None:
                        self._resolved_geometry_cache = result
                        self.logger.info("Pedestrian Detection: geometry resolved from API (background thread)")
                        return  # done
                    self.logger.info("Pedestrian Detection: API geometry returned None, retrying in 30s")
                except Exception as exc:  # noqa: BLE001 - background retry loop must not die on any error
                    self.logger.warning("Pedestrian Detection: background geometry resolve error: %s", exc)
                time.sleep(30)

        t = threading.Thread(target=_resolver, daemon=True, name="pedestrian-geometry-resolver")
        self._geometry_thread = t
        t.start()
        self.logger.info("Pedestrian Detection: started background geometry resolver thread")

    def _resolve_geometry_from_api(
        self,
        config: PedestrianDetectionConfig,
        stream_info: Optional[Dict[str, Any]],
    ) -> Optional[PedestrianDetectionConfig]:
        """Resolve zone_config from PostProcessingConfigClient flow."""
        client = self._config_client or (stream_info.get("config_client") if stream_info else None)
        if not client and stream_info:
            try:
                client = PostProcessingConfigClient(logger=self.logger)
                if getattr(client, "_session", None) is None:
                    self.logger.info(
                        "Pedestrian Detection: _resolve_geometry_from_api skipped (no config_client; set "
                        "MATRICE_ACCESS_KEY_ID, MATRICE_SECRET_ACCESS_KEY, MATRICE_ACCOUNT_NUMBER "
                        "or call set_config_client() for API geometry resolution)"
                    )
                    return None
                self._config_client = client
            except Exception as e:  # noqa: BLE001 - config client creation is best-effort; must not crash processing
                self.logger.warning(
                    "Pedestrian Detection: _resolve_geometry_from_api could not create config client from env: %s",
                    e,
                )
                return None
        if not stream_info:
            self.logger.info("Pedestrian Detection: _resolve_geometry_from_api skipped (no stream_info)")
            return None
        if not client:
            self.logger.info("Pedestrian Detection: _resolve_geometry_from_api skipped (no config_client)")
            return None
        ids = client.get_stream_identifiers(stream_info)
        app_deployment_id = ids.get("app_deployment_id") or ""
        camera_id = ids.get("camera_id") or ""
        self.logger.info(
            "Pedestrian Detection: _resolve_geometry_from_api app_deployment_id=%s camera_id=%s",
            app_deployment_id or "(empty)",
            camera_id or "(empty)",
        )
        if not app_deployment_id or not camera_id:
            return None
        configs, err, _ = client.get_post_processing_configs_by_app_deployment(app_deployment_id)
        if err or not configs:
            return None
        filtered = client.filter_configs_by_camera_id(configs, camera_id)
        if not filtered:
            return None
        doc = filtered[0]
        width, height = client.get_resolution(camera_id)
        if width is None or height is None:
            return None
        doc_px = client.denormalize_config(doc, width, height)
        post = doc_px.get("postProcessing") or {}
        cam_cfg = post.get(camera_id) or {}
        zone_config_raw = cam_cfg.get("zone_config") or {}
        zones_px = zone_config_raw.get("zones") or {}
        if not isinstance(zones_px, dict):
            zones_px = {}

        new_zone_config = ZoneConfig(zones=zones_px)
        return replace(
            config,
            zone_config=new_zone_config,
        )

    def process(
        self,
        data: Any,
        config: ConfigProtocol,
        context: Optional[ProcessingContext] = None,
        stream_info: Optional[Dict[str, Any]] = None,
    ) -> ProcessingResult:
        """
        Main entry point for  post-processing.
        Applies category mapping, smoothing, counting, alerting, and summary generation.
        Returns a ProcessingResult with all relevant outputs.
        """
        start_time = time.time()
        # Resolve geometry from API on the first frame.
        # This uses PostProcessingConfigClient to fetch and denormalize zones
        # against the camera's DB resolution, overriding any normalized config.
        if stream_info and self._resolved_geometry_cache is None and self._geometry_thread is None:
            try:
                resolved = self._resolve_geometry_from_api(config, stream_info)
                if resolved is not None:
                    self._resolved_geometry_cache = resolved
                else:
                    self._start_geometry_resolver(config, stream_info)
            except Exception as exc:  # noqa: BLE001 - first-frame geometry resolve is best-effort
                self.logger.warning("Pedestrian Detection: First frame geometry resolve failed: %s", exc)
                self._start_geometry_resolver(config, stream_info)

        # Override config with API-resolved configuration (zones) if available
        if self._resolved_geometry_cache is not None:
            config = self._resolved_geometry_cache

        # Ensure config is correct type
        if not isinstance(config, PedestrianDetectionConfig):
            self._debug_elapsed_since(start_time)
            return self.create_error_result(
                "Invalid config type",
                usecase=self.name,
                category=self.category,
                context=context,
            )
        if context is None:
            context = ProcessingContext()

        # Detect input format and store in context
        input_format = match_results_structure(data)
        context.input_format = input_format
        context.confidence_threshold = config.confidence_threshold

        if config.confidence_threshold is not None:
            processed_data = filter_by_confidence(data, config.confidence_threshold)
            self.logger.debug(f"Applied confidence filtering with threshold {config.confidence_threshold}")
        else:
            processed_data = data

            self.logger.debug("Did not apply confidence filtering with threshold since nothing was provided")

        # Step 2: Apply category mapping if provided
        if config.index_to_category:
            processed_data = apply_category_mapping(processed_data, config.index_to_category)
            self.logger.debug("Applied category mapping")

        if config.target_categories:
            processed_data = [d for d in processed_data if d.get("category") in self.target_categories]
            self.logger.debug("Applied  category filtering")

        # Apply bbox smoothing if enabled
        if config.enable_smoothing:
            if self.smoothing_tracker is None:
                smoothing_config = BBoxSmoothingConfig(
                    smoothing_algorithm=config.smoothing_algorithm,
                    window_size=config.smoothing_window_size,
                    cooldown_frames=config.smoothing_cooldown_frames,
                    confidence_threshold=config.confidence_threshold,  # Use mask threshold as default
                    confidence_range_factor=config.smoothing_confidence_range_factor,
                    enable_smoothing=True,
                )
                self.smoothing_tracker = BBoxSmoothingTracker(smoothing_config)
            processed_data = bbox_smoothing(processed_data, self.smoothing_tracker.config, self.smoothing_tracker)

        # Advanced tracking (BYTETracker-like)
        try:
            # Create tracker instance if it doesn't exist (preserves state across frames)
            if self.tracker is None:
                self.tracker = self._tracker_seam.get_shared_tracker(
                    profile=TrackerProfile.LEGACY_40,
                    max_time_lost=1200,
                )

            # The tracker expects the data in the same format as input
            # It will add track_id and frame_id to each detection
            processed_data = self.tracker.update(processed_data)

        except Exception as e:  # noqa: BLE001 - tracker failure falls back to unsmoothed detections
            # If advanced tracker fails, fallback to unsmoothed detections
            self.logger.warning(f"AdvancedTracker failed: {e}")

        # Update tracking state for total count per label
        self._update_tracking_state(processed_data)
        self._total_frame_counter += 1

        # Update zone-based tracking
        self._update_zone_tracking(processed_data, config)

        # Compute current_new_counts (in/out delta vs previous frame)
        current_all: set = set()
        for ids in getattr(self, "_current_frame_track_ids", {}).values():
            current_all.update(ids)
        prev_all: set = set()
        for ids in getattr(self, "_previous_frame_track_ids", {}).values():
            prev_all.update(ids)
        self._current_new_counts = {
            "in": len(current_all - prev_all),
            "out": len(prev_all - current_all),
        }

        # Extract frame information from stream_info
        frame_number = None
        if stream_info:
            input_settings = stream_info.get("input_settings", {})
            start_frame = input_settings.get("start_frame")
            end_frame = input_settings.get("end_frame")
            # If start and end frame are the same, it's a single frame
            if start_frame is not None and end_frame is not None and start_frame == end_frame:
                frame_number = start_frame

        # Compute summaries and alerts
        counting_summary = self._count_categories(processed_data, config)
        # Add total unique  counts after tracking using only local state
        total_counts = {self._display_category(cat): count for cat, count in self.get_total_counts().items()}
        counting_summary["total_counts"] = total_counts

        alerts = self._check_alerts(counting_summary, frame_number, config)
        self._extract_predictions(processed_data)
        incidents_list = self._generate_incidents(counting_summary, alerts, config, frame_number, stream_info)
        tracking_stats_list = self._generate_tracking_stats(counting_summary, alerts, config, frame_number, stream_info)
        # business_analytics_list = self._generate_business_analytics(counting_summary, alerts, config, frame_number, stream_info, is_empty=True)
        business_analytics_list = []
        summary_list = self._generate_summary(
            counting_summary,
            incidents_list,
            tracking_stats_list,
            business_analytics_list,
            alerts,
        )

        # Extract frame-based dictionaries from the lists
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

        # Build result object following the new pattern

        result = self.create_result(
            data={"agg_summary": agg_summary},
            usecase=self.name,
            category=self.category,
            context=context,
        )

        self._debug_elapsed_since(start_time)
        return result

    def _check_alerts(self, summary: dict, frame_number: Any, config: PedestrianDetectionConfig) -> List[Dict]:
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
        if total >= 5:
            alerts.append(
                {
                    "alert_type": (
                        getattr(config.alert_config, "alert_type", ["Default"])
                        if hasattr(config, "alert_config") and hasattr(config.alert_config, "alert_type")
                        else ["Default"]
                    ),
                    "alert_id": "alert_all_" + frame_key,
                    "incident_category": self.CASE_TYPE,
                    "threshold_level": 5,
                    "ascending": get_trend(self._ascending_alert_list, lookback=900, threshold=0.8),
                    "settings": {
                        t: v
                        for t, v in zip(
                            (
                                getattr(config.alert_config, "alert_type", ["Default"])
                                if hasattr(config.alert_config, "alert_type")
                                else ["Default"]
                            ),
                            (
                                getattr(config.alert_config, "alert_value", ["JSON"])
                                if hasattr(config.alert_config, "alert_value")
                                else ["JSON"]
                            ),
                            strict=False,
                        )
                    },
                }
            )

        return alerts

    def _generate_incidents(
        self,
        counting_summary: Dict,
        alerts: List,
        config: PedestrianDetectionConfig,
        frame_number: Optional[int] = None,
        stream_info: Optional[Dict[str, Any]] = None,
    ) -> List[Dict]:
        """Generate structured incidents for the output format with frame-based keys."""

        incidents = []
        total_detections = counting_summary.get("total_count", 0)
        current_timestamp = self._get_current_timestamp_str(stream_info)
        camera_info = self.get_camera_info_from_stream(stream_info)

        self._ascending_alert_list = (
            self._ascending_alert_list[-900:] if len(self._ascending_alert_list) > 900 else self._ascending_alert_list
        )

        if total_detections > 0:
            # Determine event level based on thresholds
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
                threshold = 5  # Force threshold to 5 as requested
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

            # Generate human text in new format
            human_text_lines = [f"INCIDENTS DETECTED @ {current_timestamp}:"]
            human_text_lines.append(f"\tSeverity Level: {(self.CASE_TYPE, level)}")
            human_text = "\n".join(human_text_lines)

            alert_settings = []
            if config.alert_config and hasattr(config.alert_config, "alert_type"):
                alert_settings.append(
                    {
                        "alert_type": (
                            getattr(config.alert_config, "alert_type", ["Default"])
                            if hasattr(config.alert_config, "alert_type")
                            else ["Default"]
                        ),
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
                                (
                                    getattr(config.alert_config, "alert_type", ["Default"])
                                    if hasattr(config.alert_config, "alert_type")
                                    else ["Default"]
                                ),
                                (
                                    getattr(config.alert_config, "alert_value", ["JSON"])
                                    if hasattr(config.alert_config, "alert_value")
                                    else ["JSON"]
                                ),
                                strict=False,
                            )
                        },
                    }
                )

            event = self.create_incident(
                incident_id=self.CASE_TYPE + "_" + str(frame_number),
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
        config: PedestrianDetectionConfig,
        _frame_number: Optional[int] = None,
        stream_info: Optional[Dict[str, Any]] = None,
    ) -> List[Dict]:
        """Generate structured tracking stats matching eg.json format."""
        _ = (_frame_number,)
        camera_info = self.get_camera_info_from_stream(stream_info)

        tracking_stats = []

        total_detections = counting_summary.get("total_count", 0)  # CURRENT total count of all classes
        total_counts_dict = counting_summary.get("total_counts", {})  # TOTAL cumulative counts per class
        per_category_count = counting_summary.get("per_category_count", {})  # CURRENT count per class

        current_timestamp = self._get_current_timestamp_str(stream_info, precision=False)
        start_timestamp = self._get_start_timestamp_str(stream_info, precision=False)
        self._debug_stream_timing("start_timestamp", start_timestamp)

        # Create high precision timestamps for input_timestamp and reset_timestamp
        high_precision_start_timestamp = self._get_current_timestamp_str(stream_info, precision=True)
        high_precision_reset_timestamp = self._get_start_timestamp_str(stream_info, precision=True)

        # Build total_counts array in expected format
        total_counts = []
        for cat, count in total_counts_dict.items():
            if count > 0:
                total_counts.append({"category": cat, "count": count})

        # Build current_counts array in expected format
        current_counts = []
        for cat, count in per_category_count.items():
            if count > 0 or total_detections > 0:  # Include even if 0 when there are detections
                current_counts.append({"category": cat, "count": count})

        # Prepare detections without confidence scores (as per eg.json)
        detections = []
        for detection in counting_summary.get("detections", []):
            bbox = detection.get("bounding_box", {})
            category = detection.get("category", "person")
            # Include segmentation if available (like in eg.json)
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

            if "track_id" in detection:
                detection_obj["track_id"] = detection["track_id"]

            detections.append(detection_obj)

        # Build alert_settings array in expected format
        alert_settings = []
        if config.alert_config and hasattr(config.alert_config, "alert_type"):
            alert_settings.append(
                {
                    "alert_type": (
                        getattr(config.alert_config, "alert_type", ["Default"])
                        if hasattr(config.alert_config, "alert_type")
                        else ["Default"]
                    ),
                    "incident_category": self.CASE_TYPE,
                    "threshold_level": (
                        config.alert_config.count_thresholds if hasattr(config.alert_config, "count_thresholds") else {}
                    ),
                    "ascending": True,
                    "settings": {
                        t: v
                        for t, v in zip(
                            (
                                getattr(config.alert_config, "alert_type", ["Default"])
                                if hasattr(config.alert_config, "alert_type")
                                else ["Default"]
                            ),
                            (
                                getattr(config.alert_config, "alert_value", ["JSON"])
                                if hasattr(config.alert_config, "alert_value")
                                else ["JSON"]
                            ),
                            strict=False,
                        )
                    },
                }
            )

        # Generate human_text in expected format
        human_text_lines = ["Tracking Statistics:"]
        human_text_lines.append(f"CURRENT FRAME @ {current_timestamp}")

        for cat, count in per_category_count.items():
            human_text_lines.append(f"\t{cat}: {count}")

        # Zone-wise breakdown
        zone_cc = counting_summary.get("zone_current_counts", {})
        zone_tc = counting_summary.get("zone_total_counts", {})
        zone_nc = counting_summary.get("zone_new_counts", {})
        if zone_cc:
            human_text_lines.append("ZONE-WISE CURRENT:")
            for zn, cnt in zone_cc.items():
                human_text_lines.append(f"\t{zn}: {cnt} (total: {zone_tc.get(zn, 0)}, new: {zone_nc.get(zn, 0)})")

        # In / Out delta
        current_new = counting_summary.get("current_new_counts", {"in": 0, "out": 0})
        human_text_lines.append(f"NEW IN: {current_new.get('in', 0)}  |  NEW OUT: {current_new.get('out', 0)}")

        human_text_lines.append(f"TOTAL SINCE {start_timestamp}")
        for cat, count in total_counts_dict.items():
            if count > 0:
                human_text_lines.append(f"\t{cat}: {count}")

        if alerts:
            for alert in alerts:
                human_text_lines.append(f"Alerts: {alert.get('settings', {})} sent @ {current_timestamp}")
        else:
            human_text_lines.append("Alerts: None")

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

        # ── Append zone-wise and new counts ────────────────────────────────
        zone_current_counts = counting_summary.get("zone_current_counts", {})
        zone_total_counts = counting_summary.get("zone_total_counts", {})
        zone_new_counts = counting_summary.get("zone_new_counts", {})
        current_new = counting_summary.get("current_new_counts", {"in": 0, "out": 0})

        tracking_stat["zone_current_counts"] = [{"category": k, "count": v} for k, v in zone_current_counts.items()]
        tracking_stat["zone_total_counts"] = [{"category": k, "count": v} for k, v in zone_total_counts.items()]
        tracking_stat["zone_new_counts"] = [{"category": k, "count": v} for k, v in zone_new_counts.items()]
        new_counts_dict = self.get_new_counts_this_frame()
        tracking_stat["current_new_counts"] = [
            {"category": self._display_category(cat), "count": count} for cat, count in new_counts_dict.items()
        ]

        tracking_stats.append(tracking_stat)
        return tracking_stats

    def _generate_business_analytics(
        self,
        _counting_summary: Dict,
        _zone_analysis: Dict,
        _config: PedestrianDetectionConfig,
        _stream_info: Optional[Dict[str, Any]] = None,
        is_empty=False,
    ) -> List[Dict]:
        """Generate standardized business analytics for the agg_summary structure."""
        _ = (_config, _counting_summary, _stream_info, _zone_analysis)
        if is_empty:
            return []

        # -----IF YOUR USECASE NEEDS BUSINESS ANALYTICS, YOU CAN USE THIS FUNCTION------#

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
        lines = {}
        lines["Application Name"] = self.CASE_TYPE
        lines["Application Version"] = self.CASE_VERSION
        if len(incidents) > 0:
            lines["Incidents:"] = f"\n\t{incidents[0].get('human_text', 'No incidents detected')}\n"
        if len(tracking_stats) > 0:
            lines["Tracking Statistics:"] = (
                f"\t{tracking_stats[0].get('human_text', 'No tracking statistics detected')}\n"
            )
        if len(business_analytics) > 0:
            lines["Business Analytics:"] = (
                f"\t{business_analytics[0].get('human_text', 'No business analytics detected')}\n"
            )

        if len(incidents) == 0 and len(tracking_stats) == 0 and len(business_analytics) == 0:
            lines["Summary"] = "No Summary Data"

        return [lines]

    def _get_track_ids_info(self, detections: list) -> Dict[str, Any]:
        """
        Get detailed information about track IDs (per frame).
        """
        # Collect all track_ids in this frame
        frame_track_ids = set()
        for det in detections:
            tid = det.get("track_id")
            if tid is not None:
                frame_track_ids.add(tid)
        # Use persistent total set for unique counting
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
        """
        Track unique categories track_ids per category for total count after tracking.
        Applies canonical ID merging (time-based, stale-track pruning) and a
        consecutive-frames confirmation gate before a track is counted as new/total.
        Mirrors people_counting logic.
        """
        if not hasattr(self, "_per_category_total_track_ids"):
            self._per_category_total_track_ids = {cat: set() for cat in self.target_categories}
        if not hasattr(self, "_previous_frame_track_ids"):
            self._previous_frame_track_ids = {cat: set() for cat in self.target_categories}
        if not hasattr(self, "_consecutive_track_frames"):
            self._consecutive_track_frames = {cat: {} for cat in self.target_categories}
        if not hasattr(self, "_min_confirm_frames"):
            self._min_confirm_frames = 3

        min_hits = max(1, int(getattr(self, "_min_confirm_frames", 3)))

        self._current_frame_track_ids = {cat: set() for cat in self.target_categories}

        for det in detections:
            cat = det.get("category")
            raw_track_id = det.get("track_id")
            if cat not in self.target_categories or raw_track_id is None:
                continue
            bbox = det.get("bounding_box", det.get("bbox"))
            canonical_id = self._merge_or_register_track(raw_track_id, bbox)
            # Propagate canonical ID back so downstream zone/counting logic uses it
            det["track_id"] = canonical_id
            self._current_frame_track_ids[cat].add(canonical_id)

        self._new_track_ids_this_frame = {cat: set() for cat in self.target_categories}

        for cat in self.target_categories:
            current_ids = self._current_frame_track_ids.get(cat, set())
            prev_counts = self._consecutive_track_frames.get(cat, {})
            next_counts: Dict[Any, int] = {}

            for tid in current_ids:
                next_counts[tid] = min(min_hits, prev_counts.get(tid, 0) + 1)

            # Soft decay: IDs not seen this frame lose one count instead of resetting
            for tid, prev in prev_counts.items():
                if tid in current_ids:
                    continue
                decayed = max(0, prev - 1)
                if decayed > 0:
                    next_counts[tid] = decayed

            self._consecutive_track_frames[cat] = next_counts

            confirmed_total = self._per_category_total_track_ids.setdefault(cat, set())
            for tid, consec in next_counts.items():
                if consec >= min_hits and tid not in confirmed_total:
                    confirmed_total.add(tid)
                    self._new_track_ids_this_frame[cat].add(tid)

        self._previous_frame_track_ids = {cat: set(ids) for cat, ids in self._current_frame_track_ids.items()}

    def _update_zone_tracking(self, detections: list, config: PedestrianDetectionConfig) -> None:
        """Update zone-based tracking: current, total, and new counts per zone.

        Uses ``get_bbox_bottom25_center`` + ``point_in_polygon`` for zone membership.
        """
        zone_cfg = getattr(config, "zone_config", None)
        if zone_cfg is None or not getattr(zone_cfg, "zones", None):
            # No zones configured — reset zone state
            self._zone_current_counts = {}
            self._zone_total_counts = {}
            self._zone_new_counts = {}
            return

        zones = zone_cfg.zones  # Dict[str, List[List[float]]]

        # Initialise storage for any new zones
        for zone_name in zones:
            if zone_name not in self._zone_total_track_ids:
                self._zone_total_track_ids[zone_name] = set()

        # Build per-zone current-frame track-id sets
        prev_zone_track_ids: Dict[str, set] = {zn: set(self._zone_current_track_ids.get(zn, set())) for zn in zones}
        zone_current: Dict[str, set] = {zn: set() for zn in zones}

        for det in detections:
            bbox = det.get("bounding_box") or det.get("bbox")
            track_id = det.get("track_id")
            if bbox is None:
                continue

            foot_point = get_bbox_bottom25_center(bbox)
            if foot_point == (0, 0):
                continue

            for zone_name, polygon in zones.items():
                poly_tuples = [(pt[0], pt[1]) for pt in polygon]
                if point_in_polygon(foot_point, poly_tuples):
                    if track_id is not None:
                        zone_current[zone_name].add(track_id)
                        self._zone_total_track_ids[zone_name].add(track_id)

        # Compute counts
        self._zone_current_track_ids = zone_current
        self._zone_current_counts = {zn: len(ids) for zn, ids in zone_current.items()}
        self._zone_total_counts = {zn: len(self._zone_total_track_ids.get(zn, set())) for zn in zones}
        self._zone_new_counts = {zn: len(zone_current[zn] - prev_zone_track_ids.get(zn, set())) for zn in zones}

    def get_total_counts(self):
        """Return total unique confirmed track_id count for each category."""
        return {cat: len(ids) for cat, ids in getattr(self, "_per_category_total_track_ids", {}).items()}

    def get_new_counts_this_frame(self) -> Dict[str, int]:
        """Return count of track IDs confirmed as new for the first time this frame.

        A track is counted as new only after appearing for at least
        ``_min_confirm_frames`` consecutive frames, matching people_counting behaviour.
        Each ID is reported exactly once across all frames.
        """
        return {cat: len(ids) for cat, ids in getattr(self, "_new_track_ids_this_frame", {}).items()}

    def _format_timestamp_for_video(self, timestamp: float) -> str:
        """Format timestamp for video chunks (HH:MM:SS.ms format)."""
        hours = int(timestamp // 3600)
        minutes = int((timestamp % 3600) // 60)
        seconds = round(float(timestamp % 60), 2)
        return f"{hours:02d}:{minutes:02d}:{seconds:.1f}"

    def _format_timestamp_for_stream(self, timestamp: float) -> str:
        """Format timestamp for streams (YYYY:MM:DD HH:MM:SS format)."""
        dt = datetime.fromtimestamp(timestamp, tz=timezone.utc)
        return dt.strftime("%Y:%m:%d %H:%M:%S")

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
                except Exception:  # noqa: BLE001 - malformed stream_time string, fall back to wall clock
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
                    except Exception:  # noqa: BLE001 - malformed stream_time string, fall back to wall clock
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
                    except Exception:  # noqa: BLE001 - malformed stream_time string, fall back to wall clock
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
                    except Exception:  # noqa: BLE001 - malformed stream_time string, fall back to wall clock
                        self._tracking_start_time = time.time()
                else:
                    self._tracking_start_time = time.time()

            dt = datetime.fromtimestamp(self._tracking_start_time, tz=timezone.utc)
            dt = dt.replace(minute=0, second=0, microsecond=0)
            return dt.strftime("%Y:%m:%d %H:%M:%S")

    def _display_category(self, cat: Optional[str]) -> Optional[str]:
        """Map an internal tracking category to its wire/display name.

        Internal matching (target_categories, tracker state) stays on the raw
        model category ("person"); only output-facing fields are relabeled,
        matching ml-applications' pedestrian_detection-v1.4 wire relabel.
        """
        return self.CATEGORY_DISPLAY.get(cat, cat)

    def _count_categories(self, detections: list, _config: PedestrianDetectionConfig) -> dict:
        """
        Count the number of detections per category and return a summary dict.
        The detections list is expected to have 'track_id' (from tracker), 'category', 'bounding_box', etc.
        Output structure will include 'track_id' for each detection as per AdvancedTracker output.
        Also includes zone-wise counts computed by _update_zone_tracking.
        """
        _ = (_config,)
        counts = {}
        for det in detections:
            cat = self._display_category(det.get("category", "unknown"))
            counts[cat] = counts.get(cat, 0) + 1
        # Each detection dict will now include 'track_id' (and possibly 'frame_id')
        result = {
            "total_count": sum(counts.values()),
            "per_category_count": counts,
            "detections": [
                {
                    "bounding_box": det.get("bounding_box"),
                    "category": self._display_category(det.get("category")),
                    "confidence": det.get("confidence"),
                    "track_id": det.get("track_id"),
                    "frame_id": det.get("frame_id"),
                }
                for det in detections
            ],
            # Zone-wise counts (populated by _update_zone_tracking)
            "zone_current_counts": dict(self._zone_current_counts),
            "zone_total_counts": dict(self._zone_total_counts),
            "zone_new_counts": dict(self._zone_new_counts),
            "zone_polygons": getattr(getattr(_config, "zone_config", None), "zones", {}),
            # In/out delta (populated in process())
            "current_new_counts": getattr(self, "_current_new_counts", {"in": 0, "out": 0}),
        }
        return result

    def _extract_predictions(self, detections: list) -> List[Dict[str, Any]]:
        """
        Extract prediction details for output (category, confidence, bounding box).
        """
        return [
            {
                "category": det.get("category", "unknown"),
                "confidence": det.get("confidence", 0.0),
                "bounding_box": det.get("bounding_box", {}),
            }
            for det in detections
        ]

    # ------------------------------------------------------------------ #
    # Canonical ID helpers                                               #
    # ------------------------------------------------------------------ #
    def _compute_iou(self, box1: Any, box2: Any) -> float:
        """Compute IoU between two bounding boxes which may be dicts or lists.
        Falls back to 0 when insufficient data is available."""

        # Helper to convert bbox (dict or list) to [x1, y1, x2, y2]
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
                # Fallback: first four numeric values
                values = [v for v in bbox.values() if isinstance(v, (int, float))]
                return values[:4] if len(values) >= 4 else []
            return []

        l1 = _bbox_to_list(box1)
        l2 = _bbox_to_list(box2)
        if len(l1) < 4 or len(l2) < 4:
            return 0.0
        x1_min, y1_min, x1_max, y1_max = l1
        x2_min, y2_min, x2_max, y2_max = l2

        # Ensure correct order
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
        """Return a stable canonical ID for a raw tracker ID.

        Uses wall-clock time for staleness (mirrors people_counting logic).
        Stale canonical tracks are pruned so reused tracker IDs are never
        incorrectly aliased to an old entity.
        """
        if raw_id is None or bbox is None:
            return raw_id

        now = time.time()

        # Fast path – raw_id already mapped
        if raw_id in self._track_aliases:
            canonical_id = self._track_aliases[raw_id]
            track_info = self._canonical_tracks.get(canonical_id)
            if track_info is not None:
                track_info["last_bbox"] = bbox
                track_info["last_update"] = now
                track_info["raw_ids"].add(raw_id)
            return canonical_id

        # Prune stale canonical tracks so reused raw IDs get a fresh entry.
        to_delete = [
            cid
            for cid, info in self._canonical_tracks.items()
            if now - info["last_update"] > self._track_merge_time_window
        ]
        for cid in to_delete:
            del self._canonical_tracks[cid]

        # Attempt to merge with a still-active canonical track
        for canonical_id, info in self._canonical_tracks.items():
            if now - info["last_update"] > self._track_merge_time_window:
                continue
            prev_bbox = info["last_bbox"]
            if prev_bbox is None:
                continue
            iou = self._compute_iou(bbox, prev_bbox)

            try:
                cx1 = (prev_bbox["xmin"] + prev_bbox["xmax"]) / 2
                cy1 = (prev_bbox["ymin"] + prev_bbox["ymax"]) / 2
                cx2 = (bbox["xmin"] + bbox["xmax"]) / 2
                cy2 = (bbox["ymin"] + bbox["ymax"]) / 2
                center_dist = ((cx1 - cx2) ** 2 + (cy1 - cy2) ** 2) ** 0.5
                area1 = (prev_bbox["xmax"] - prev_bbox["xmin"]) * (prev_bbox["ymax"] - prev_bbox["ymin"])
                area2 = (bbox["xmax"] - bbox["xmin"]) * (bbox["ymax"] - bbox["ymin"])
                size_ratio = min(area1, area2) / max(area1, area2) if max(area1, area2) > 0 else 0
            except (TypeError, KeyError):
                center_dist = float("inf")
                size_ratio = 0

            if iou >= 0.28 or (center_dist < 35 and size_ratio > 0.6):
                self._track_aliases[raw_id] = canonical_id
                info["last_bbox"] = bbox
                info["last_update"] = now
                info["raw_ids"].add(raw_id)
                return canonical_id

        # No match – register as a new canonical track
        canonical_id = raw_id
        self._track_aliases[raw_id] = canonical_id
        self._canonical_tracks[canonical_id] = {
            "last_bbox": bbox,
            "last_update": now,
            "raw_ids": {raw_id},
        }
        return canonical_id

    def _format_timestamp(self, timestamp: Any) -> str:
        """Format a timestamp to match the current timestamp format: YYYY:MM:DD HH:MM:SS.

        Accepts either a numeric Unix timestamp (float/int) or a string in the format
        ``YYYY-MM-DD-HH:MM:SS.ffffff UTC``. Returns ``YYYY:MM:DD HH:MM:SS``.
        """
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
        except Exception as exc:  # noqa: BLE001 - malformed timestamp string, fall back to the raw value
            self.logger.debug("Pedestrian Detection: _format_timestamp fallback parse failed: %s", exc)

        return timestamp_clean

    def _get_tracking_start_time(self) -> str:
        """Get the tracking start time, formatted as a string."""
        if self._tracking_start_time is None:
            return "N/A"
        return self._format_timestamp(self._tracking_start_time)

    def _set_tracking_start_time(self) -> None:
        """Set the tracking start time to the current time."""
        self._tracking_start_time = time.time()
