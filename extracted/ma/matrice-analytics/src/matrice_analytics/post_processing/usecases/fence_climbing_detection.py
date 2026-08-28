"""
Fence Climbing Detection use case implementation.

Detects persons climbing or attempting to climb fences within user-defined zones.
Zone geometry can be resolved from the Matrice API at runtime or configured via a
local config file.  When the API is unavailable the default zone covers the top half
of a 1920x1080 frame.

Architecture closely mirrors HazardZoneEntryUseCase:
  * Per-track consecutive-frame confirmation before triggering an alert.
  * Background thread retries API zone geometry every 30 s on first-frame failure.
  * Incident manager integration for downstream alerting pipelines.
"""

import threading
import time
from collections import defaultdict
from dataclasses import dataclass, replace
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Set

from ..core.base import (
    BaseProcessor,
    ConfigProtocol,
    ProcessingContext,
    ProcessingResult,
)
from ..core.config import AlertConfig, PeopleCountingConfig, ZoneConfig
from ..Trackers import ConfigDrivenTracker, TrackerProfile
from ..utils import (
    apply_category_mapping,
    match_results_structure,
)
from ..utils.geometry_utils import (
    get_bbox_bottom25_center,
    get_bbox_center,
    point_in_polygon,
)

_GEOMETRY_RETRY_INTERVAL = 30  # seconds between background API retries
_DEFAULT_1080P_TOP_HALF_ZONE: Dict[str, List[List[float]]] = {
    "fence_zone": [
        [0.0, 0.0],
        [1920.0, 0.0],
        [1920.0, 540.0],
        [0.0, 540.0],
    ]
}


@dataclass
class FenceClimbingDetectionConfig(PeopleCountingConfig):
    """Configuration for Fence Climbing Detection use case."""

    zone_config: Optional[ZoneConfig] = None

    min_climbing_frames: int = 3
    exit_grace_frames: int = 3
    climbing_confidence_threshold: float = 0.6
    min_vertical_displacement: float = 20.0

    def __post_init__(self) -> None:
        if isinstance(self.zone_config, dict):
            self.zone_config = ZoneConfig(**self.zone_config)
        if isinstance(self.alert_config, dict):
            self.alert_config = AlertConfig(**self.alert_config)

    def validate(self) -> List[str]:
        errors = super().validate()
        if self.min_climbing_frames < 1:
            errors.append("min_climbing_frames must be >= 1")
        if self.exit_grace_frames < 0:
            errors.append("exit_grace_frames must be >= 0")
        if not 0.0 <= self.climbing_confidence_threshold <= 1.0:
            errors.append("climbing_confidence_threshold must be between 0.0 and 1.0")
        if self.min_vertical_displacement < 0:
            errors.append("min_vertical_displacement must be >= 0")
        if self.zone_config:
            errors.extend(self.zone_config.validate())
        if self.alert_config:
            errors.extend(self.alert_config.validate())
        return errors


class FenceClimbingDetectionUseCase(BaseProcessor):
    """Fence Climbing Detection with zone analysis, per-track state, and incident manager."""

    def __init__(self):
        super().__init__("fence_climbing_detection")
        self.category = "general"
        self.CASE_TYPE: Optional[str] = "fence_climbing_detection"
        self.CASE_VERSION: Optional[str] = "1.0"
        self.target_categories = ["person"]
        self.tracker = None
        self._tracker_seam = None

        self._total_frame_counter = 0
        self._global_frame_offset = 0
        self._tracking_start_time: Optional[float] = None
        self._ascending_alert_list: List[int] = []
        self.current_incident_end_timestamp: str = "N/A"

        # Per-track state inside each zone
        self._zone_inside_frames: Dict[str, Dict[Any, int]] = {}
        self._zone_outside_frames: Dict[str, Dict[Any, int]] = {}
        self._zone_alerted_tracks: Dict[str, set] = defaultdict(set)
        self._zone_current_track_ids: Dict[str, set] = {}
        self._zone_total_track_ids: Dict[str, set] = {}
        self._zone_current_counts: Dict[str, int] = {}
        self._zone_total_counts: Dict[str, int] = {}

        # Vertical displacement tracking: stores bbox center Y when a track
        # first enters a zone. Compared against current Y at confirmation time.
        self._zone_track_initial_y: Dict[str, Dict[Any, float]] = {}

        # Track confirmation
        self._consecutive_track_frames: Dict[Any, int] = {}
        self._min_confirm_frames: int = 3

        # API zone geometry resolution
        self._zone_resolution_attempted: bool = False
        self._resolved_geometry_cache: Optional[FenceClimbingDetectionConfig] = None
        self._config_client: Optional[Any] = None
        self._geometry_thread: Optional[threading.Thread] = None

        # Incident manager
        self._incident_manager_factory: Optional[Any] = None
        self._incident_manager: Optional[Any] = None
        self._incident_manager_initialized: bool = False

    # ------------------------------------------------------------------ #
    # Public helpers
    # ------------------------------------------------------------------ #

    def set_config_client(self, client: Any) -> None:
        self._config_client = client

    def get_config_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "confidence_threshold": {
                    "type": "number",
                    "minimum": 0.0,
                    "maximum": 1.0,
                    "default": 0.5,
                },
                "climbing_confidence_threshold": {
                    "type": "number",
                    "minimum": 0.0,
                    "maximum": 1.0,
                    "default": 0.6,
                },
                "min_climbing_frames": {
                    "type": "integer",
                    "minimum": 1,
                    "default": 3,
                },
                "exit_grace_frames": {
                    "type": "integer",
                    "minimum": 0,
                    "default": 3,
                },
                "min_vertical_displacement": {
                    "type": "number",
                    "minimum": 0,
                    "default": 20.0,
                    "description": "Minimum cumulative vertical displacement (pixels) required to confirm climbing",
                },
                "target_categories": {
                    "type": "array",
                    "items": {"type": "string"},
                    "default": ["person"],
                },
            },
            "required": ["confidence_threshold"],
            "additionalProperties": False,
        }

    def create_default_config(self, **overrides) -> FenceClimbingDetectionConfig:
        defaults = {
            "category": self.category,
            "usecase": self.name,
            "confidence_threshold": 0.5,
            "climbing_confidence_threshold": 0.6,
            "min_climbing_frames": 3,
            "exit_grace_frames": 3,
            "min_vertical_displacement": 20.0,
            "target_categories": ["person"],
            "zone_config": ZoneConfig(zones=_DEFAULT_1080P_TOP_HALF_ZONE),
        }
        defaults.update(overrides)
        return FenceClimbingDetectionConfig(**defaults)

    # ------------------------------------------------------------------ #
    # API zone geometry resolution
    # ------------------------------------------------------------------ #

    def _start_geometry_resolver(
        self,
        config: FenceClimbingDetectionConfig,
        stream_info: Optional[Dict[str, Any]],
    ) -> None:
        if self._geometry_thread and self._geometry_thread.is_alive():
            return

        def _resolver():
            while True:
                try:
                    result = self._resolve_geometry_from_api(config, stream_info)
                    if result is not None:
                        self._resolved_geometry_cache = result
                        self.logger.info("FenceClimbingDetection: zone geometry resolved from API (background thread)")
                        return
                    self.logger.info(
                        "FenceClimbingDetection: API geometry returned None, retrying in %ds",
                        _GEOMETRY_RETRY_INTERVAL,
                    )
                except Exception as exc:
                    self.logger.warning(
                        "FenceClimbingDetection: background geometry resolve error: %s",
                        exc,
                    )
                time.sleep(_GEOMETRY_RETRY_INTERVAL)

        t = threading.Thread(
            target=_resolver,
            daemon=True,
            name="fence-climbing-geometry-resolver",
        )
        self._geometry_thread = t
        t.start()
        self.logger.info("FenceClimbingDetection: started background zone geometry resolver thread")

    def _resolve_geometry_from_api(
        self,
        config: FenceClimbingDetectionConfig,
        stream_info: Optional[Dict[str, Any]],
    ) -> Optional[FenceClimbingDetectionConfig]:
        """Resolve zone_config from PostProcessingConfigClient flow.

        Uses: get_stream_identifiers -> get_post_processing_configs_by_app_deployment ->
        filter_configs_by_camera_id -> get_resolution -> denormalize_config -> extract zones.
        Returns a new config with zone_config filled, or None if unavailable.
        """
        from .hazard_zone_entry import PostProcessingConfigClient

        client = self._config_client or (stream_info.get("config_client") if stream_info else None)
        if not client and stream_info:
            try:
                client = PostProcessingConfigClient(logger=self.logger)
                if getattr(client, "_session", None) is None:
                    self.logger.info("FenceClimbingDetection: _resolve_geometry_from_api skipped (no config_client)")
                    return None
                self._config_client = client
            except Exception as e:
                self.logger.warning(
                    "FenceClimbingDetection: could not create config client from env: %s",
                    e,
                )
                return None

        if not stream_info or not client:
            return None

        ids = client.get_stream_identifiers(stream_info)
        app_deployment_id = ids.get("app_deployment_id") or ""
        camera_id = ids.get("camera_id") or ""

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

        if not isinstance(zones_px, dict) or not zones_px:
            return None

        zones_dict = {name: [list(pt) for pt in points] for name, points in zones_px.items()}
        new_zone_config = ZoneConfig(zones=zones_dict)

        self.logger.info(
            "FenceClimbingDetection: resolved %d zone(s) from API: %s",
            len(zones_dict),
            list(zones_dict.keys()),
        )
        return replace(config, zone_config=new_zone_config)

    # ------------------------------------------------------------------ #
    # Incident manager
    # ------------------------------------------------------------------ #

    def _initialize_incident_manager_once(self, config: FenceClimbingDetectionConfig) -> None:
        if self._incident_manager_initialized:
            return
        try:
            from ..utils.incident_manager_utils import IncidentManagerFactory

            if self._incident_manager_factory is None:
                self._incident_manager_factory = IncidentManagerFactory(logger=self.logger)
            self._incident_manager = self._incident_manager_factory.initialize(config)
            if self._incident_manager:
                self.logger.info("FenceClimbingDetection: incident manager initialized")
        except Exception as exc:
            self.logger.warning("FenceClimbingDetection: incident manager init failed: %s", exc)
        finally:
            self._incident_manager_initialized = True

    # ------------------------------------------------------------------ #
    # Main processing
    # ------------------------------------------------------------------ #

    def process(
        self,
        data: Any,
        config: ConfigProtocol,
        context: Optional[ProcessingContext] = None,
        stream_info: Optional[Dict[str, Any]] = None,
    ) -> ProcessingResult:
        processing_start = time.time()

        try:
            if not isinstance(config, FenceClimbingDetectionConfig):
                return self.create_error_result(
                    "Invalid configuration type for fence climbing detection",
                    usecase=self.name,
                    category=self.category,
                    context=context,
                )

            if context is None:
                context = ProcessingContext()

            # Initialize incident manager on first call
            self._initialize_incident_manager_once(config)

            # ----------------------------------------------------------
            # Resolve zone geometry from API exactly once (first frame).
            # Fallback: default top-half 1080p zone.
            # ----------------------------------------------------------
            if not self._zone_resolution_attempted:
                self._zone_resolution_attempted = True
                if stream_info:
                    try:
                        resolved = self._resolve_geometry_from_api(config, stream_info)
                        if resolved is not None:
                            self._resolved_geometry_cache = resolved
                            self.logger.info("FenceClimbingDetection: zone geometry resolved from API and cached")
                        else:
                            self.logger.warning(
                                "FenceClimbingDetection: API returned no zone config; "
                                "starting background retry (every %ds). Using fallback zone.",
                                _GEOMETRY_RETRY_INTERVAL,
                            )
                            self._start_geometry_resolver(config, stream_info)
                    except Exception as exc:
                        self.logger.warning(
                            "FenceClimbingDetection: zone resolution raised (%s); "
                            "starting background retry. Using fallback zone.",
                            exc,
                        )
                        self._start_geometry_resolver(config, stream_info)
                else:
                    self.logger.info("FenceClimbingDetection: no stream_info on first frame; using config zone")

            if self._resolved_geometry_cache is not None:
                config = self._resolved_geometry_cache

            # Apply default zone if none configured
            if not config.zone_config or not config.zone_config.zones:
                config = replace(
                    config,
                    zone_config=ZoneConfig(zones=_DEFAULT_1080P_TOP_HALF_ZONE),
                )
                self.logger.debug("FenceClimbingDetection: applied default top-half 1080p zone")

            context.input_format = match_results_structure(data)
            context.confidence_threshold = config.confidence_threshold

            # Normalize data to flat detection list
            if isinstance(data, list):
                processed_data = data
            elif isinstance(data, dict):
                processed_data = []
                for _key, value in data.items():
                    if isinstance(value, list):
                        processed_data = value
                        break
            else:
                processed_data = []

            self._total_frame_counter += 1

            # Determine frame number
            frame_number: Any = None
            if stream_info:
                input_settings = stream_info.get("input_settings", {}) or {}
                start_frame = input_settings.get("start_frame")
                end_frame = input_settings.get("end_frame")
                if start_frame is not None and end_frame is not None and start_frame == end_frame:
                    frame_number = start_frame
            if frame_number is None:
                frame_number = self._total_frame_counter

            (
                alerts,
                incidents_list,
                tracking_stats_list,
                business_analytics_list,
                summary_list,
            ) = self._process_frame_detections(processed_data, config, str(frame_number), stream_info)

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

            proc_ms = (time.time() - processing_start) * 1000.0
            self.logger.debug(
                "FenceClimbingDetection: frame %s processed in %.1f ms",
                frame_number,
                proc_ms,
            )

            return self.create_result(
                data={"agg_summary": agg_summary},
                usecase=self.name,
                category=self.category,
                context=context,
            )

        except Exception as e:
            self.logger.error("FenceClimbingDetection.process failed: %s", e, exc_info=True)
            if context:
                context.mark_completed()
            return self.create_error_result(
                str(e),
                type(e).__name__,
                usecase=self.name,
                category=self.category,
                context=context,
            )

    # ------------------------------------------------------------------ #
    # Frame-level processing
    # ------------------------------------------------------------------ #

    def _process_frame_detections(
        self,
        frame_data: Any,
        config: FenceClimbingDetectionConfig,
        frame_id: str,
        stream_info: Optional[Dict[str, Any]] = None,
    ) -> tuple:
        if isinstance(frame_data, list):
            frame_detections = frame_data
        else:
            frame_detections = []

        # Confidence filter
        if config.confidence_threshold is not None:
            frame_detections = [d for d in frame_detections if d.get("confidence", 0) >= config.confidence_threshold]

        # Category mapping
        if config.index_to_category:
            frame_detections = apply_category_mapping(frame_detections, config.index_to_category)

        # Category filter
        target_cats = config.target_categories or self.target_categories
        frame_detections = [d for d in frame_detections if d.get("category") in target_cats]

        # Tracker integration
        needs_tracking = bool(config.enable_tracking)
        if self.tracker is None and needs_tracking:
            try:
                fps = 30
                try:
                    if stream_info:
                        fps = int(stream_info.get("input_settings", {}).get("original_fps", 30))
                        if fps <= 0:
                            fps = 30
                except Exception:
                    fps = 30

                # F10b S6/S7 gap closure: LEGACY_40's base kwargs (0.4/0.05/0.3/0.8) are this
                # site's literals; track_buffer/max_time_lost/frame_rate are fps-derived overrides.
                if self._tracker_seam is None:
                    self._tracker_seam = ConfigDrivenTracker()
                self.tracker = self._tracker_seam.get_shared_tracker(
                    profile=TrackerProfile.LEGACY_40,
                    track_buffer=int(3 * fps),
                    max_time_lost=int(3 * fps),
                    frame_rate=fps,
                )
                self.logger.info("Initialized AdvancedTracker for FenceClimbingDetection")
            except Exception as e:
                self.logger.warning("AdvancedTracker init failed, using raw detections: %s", e)

        tracked_detections = frame_detections
        if self.tracker is not None and needs_tracking:
            try:
                tracked_detections = self.tracker.update(frame_detections)
            except Exception as e:
                self.logger.warning("AdvancedTracker update failed, using raw detections: %s", e)
                tracked_detections = frame_detections

        counting_summary = {
            "total_objects": len(tracked_detections),
            "detections": tracked_detections,
            "categories": {},
        }
        for det in tracked_detections:
            cat = det.get("category", "unknown")
            counting_summary["categories"][cat] = counting_summary["categories"].get(cat, 0) + 1

        # Update tracking state
        self._update_tracking_state(counting_summary)

        # Zone analysis
        resolved_zones: Dict[str, Any] = (
            config.zone_config.zones if config.zone_config and config.zone_config.zones else {}
        )

        zone_analysis: Dict[str, Any] = {zn: {} for zn in resolved_zones}
        if resolved_zones:
            enhanced = self._update_zone_tracking(zone_analysis, counting_summary["detections"], config)
            for zn, edata in enhanced.items():
                zone_analysis[zn] = edata

        alerts = self._check_alerts(counting_summary, zone_analysis, config, frame_id)
        incidents = self._generate_incidents(counting_summary, zone_analysis, alerts, config, frame_id, stream_info)
        tracking_stats = self._generate_tracking_stats(
            counting_summary, zone_analysis, config, frame_id, alerts, stream_info
        )
        business_analytics = self._generate_business_analytics(
            counting_summary, zone_analysis, config, frame_id, stream_info
        )
        summary = self._generate_summary(counting_summary, incidents, tracking_stats, business_analytics, alerts)

        return alerts, incidents, tracking_stats, business_analytics, summary

    # ------------------------------------------------------------------ #
    # Zone tracking (per-track consecutive-frame confirmation)
    # ------------------------------------------------------------------ #

    def _update_zone_tracking(
        self,
        zone_analysis: Dict[str, Dict[str, int]],
        detections: List[Dict],
        config: FenceClimbingDetectionConfig,
    ) -> Dict[str, Dict[str, Any]]:
        if config.zone_config and config.zone_config.zones:
            zones = config.zone_config.zones
        else:
            return {}

        enhanced_zone_analysis = {}
        current_frame_zone_tracks: Dict[str, set] = {}

        for zone_name in zones:
            current_frame_zone_tracks[zone_name] = set()
            if zone_name not in self._zone_total_track_ids:
                self._zone_total_track_ids[zone_name] = set()
            if zone_name not in self._zone_alerted_tracks:
                self._zone_alerted_tracks[zone_name] = set()
            if zone_name not in self._zone_inside_frames:
                self._zone_inside_frames[zone_name] = {}
            if zone_name not in self._zone_outside_frames:
                self._zone_outside_frames[zone_name] = {}
            if zone_name not in self._zone_track_initial_y:
                self._zone_track_initial_y[zone_name] = {}

        min_vert = config.min_vertical_displacement

        for detection in detections:
            track_id = detection.get("track_id")
            if track_id is None:
                continue

            bbox = detection.get("bounding_box", detection.get("bbox"))
            if not bbox:
                continue

            center_point = get_bbox_bottom25_center(bbox)
            _, current_center_y = get_bbox_center(bbox)

            for zone_name, zone_polygon in zones.items():
                polygon_points = [(pt[0], pt[1]) for pt in zone_polygon]

                if point_in_polygon(center_point, polygon_points):
                    current_frame_zone_tracks[zone_name].add(track_id)

                    prev = self._zone_inside_frames[zone_name].get(track_id, 0)
                    self._zone_inside_frames[zone_name][track_id] = prev + 1
                    self._zone_outside_frames[zone_name].pop(track_id, None)

                    if track_id not in self._zone_track_initial_y[zone_name]:
                        self._zone_track_initial_y[zone_name][track_id] = current_center_y

                    inside_count = self._zone_inside_frames[zone_name][track_id]

                    if (
                        inside_count >= config.min_climbing_frames
                        and track_id not in self._zone_alerted_tracks[zone_name]
                    ):
                        initial_y = self._zone_track_initial_y[zone_name].get(track_id, current_center_y)
                        vertical_displacement = abs(current_center_y - initial_y)

                        if vertical_displacement >= min_vert:
                            detection["_fence_climbing_event"] = {
                                "zone_name": zone_name,
                                "track_id": track_id,
                                "vertical_displacement": round(vertical_displacement, 1),
                            }
                else:
                    outside = self._zone_outside_frames[zone_name].get(track_id, 0) + 1
                    self._zone_outside_frames[zone_name][track_id] = outside

                    if outside >= config.exit_grace_frames and track_id not in current_frame_zone_tracks[zone_name]:
                        self._zone_inside_frames[zone_name].pop(track_id, None)
                        self._zone_outside_frames[zone_name].pop(track_id, None)
                        self._zone_alerted_tracks[zone_name].discard(track_id)
                        self._zone_track_initial_y[zone_name].pop(track_id, None)

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

    # ------------------------------------------------------------------ #
    # Tracking state helpers (mirrored from HazardZoneEntry)
    # ------------------------------------------------------------------ #

    def _update_tracking_state(self, counting_summary: Dict) -> None:
        detections = counting_summary.get("detections", [])
        current_frame_tracks: Set[Any] = set()

        if not detections:
            for tid in list(self._consecutive_track_frames.keys()):
                self._consecutive_track_frames[tid] = max(0, self._consecutive_track_frames[tid] - 1)
            self._current_frame_track_ids: Set[Any] = set()
            return

        for detection in detections:
            track_id = detection.get("track_id")
            if track_id is not None:
                current_frame_tracks.add(track_id)

        updated: Dict[Any, int] = {}
        for tid in current_frame_tracks:
            prev = self._consecutive_track_frames.get(tid, 0)
            updated[tid] = min(self._min_confirm_frames, prev + 1)
        for tid, prev in self._consecutive_track_frames.items():
            if tid not in updated:
                updated[tid] = max(0, prev - 1)
        self._consecutive_track_frames = updated

        if not hasattr(self, "_total_track_ids"):
            self._total_track_ids: Set[Any] = set()

        for tid, count in self._consecutive_track_frames.items():
            if count >= self._min_confirm_frames and tid not in self._total_track_ids:
                self._total_track_ids.add(tid)

        self._current_frame_track_ids = current_frame_tracks
        self._total_count = len(self._total_track_ids)

    def get_total_count(self) -> int:
        return getattr(self, "_total_count", 0)

    def get_current_frame_count(self) -> int:
        return len(getattr(self, "_current_frame_track_ids", set()))

    # ------------------------------------------------------------------ #
    # Alerts
    # ------------------------------------------------------------------ #

    def _check_alerts(
        self,
        counting_summary: Dict,
        _zone_analysis: Dict,
        config: FenceClimbingDetectionConfig,
        frame_id: str,
    ) -> List[Dict]:
        _ = (_zone_analysis,)
        alerts: List[Dict] = []

        if not config.alert_config:
            # Still generate alerts for climbing events even without alert_config
            for det in counting_summary.get("detections", []):
                evt = det.get("_fence_climbing_event")
                if not evt:
                    continue
                alerts.append(
                    {
                        "alert_type": ["Default"],
                        "alert_id": f"fence_climb_{evt['zone_name']}_{evt['track_id']}_{frame_id}",
                        "incident_category": self.CASE_TYPE,
                        "threshold_level": "climbing_confirmed",
                        "ascending": True,
                        "settings": {},
                    }
                )
                self._zone_alerted_tracks[evt["zone_name"]].add(evt["track_id"])
                det.pop("_fence_climbing_event", None)
            return alerts

        # Climbing-event alerts
        for det in counting_summary.get("detections", []):
            evt = det.get("_fence_climbing_event")
            if not evt:
                continue
            alerts.append(
                {
                    "alert_type": getattr(config.alert_config, "alert_type", ["Default"]),
                    "alert_id": f"fence_climb_{evt['zone_name']}_{evt['track_id']}_{frame_id}",
                    "incident_category": self.CASE_TYPE,
                    "threshold_level": "climbing_confirmed",
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
            self._zone_alerted_tracks[evt["zone_name"]].add(evt["track_id"])
            det.pop("_fence_climbing_event", None)

        # Count-threshold alerts
        total_people = counting_summary.get("total_objects", 0)
        if hasattr(config.alert_config, "count_thresholds") and config.alert_config.count_thresholds:
            for category, threshold in config.alert_config.count_thresholds.items():
                if category == "all" and total_people >= threshold:
                    alerts.append(
                        {
                            "alert_type": getattr(config.alert_config, "alert_type", ["Default"]),
                            "alert_id": f"alert_{category}_{frame_id}",
                            "incident_category": self.CASE_TYPE,
                            "threshold_level": threshold,
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

        return alerts

    # ------------------------------------------------------------------ #
    # Incidents
    # ------------------------------------------------------------------ #

    def _generate_incidents(
        self,
        counting_summary: Dict,
        _zone_analysis: Dict,
        alerts: List,
        config: FenceClimbingDetectionConfig,
        frame_id: str,
        stream_info: Optional[Dict[str, Any]] = None,
    ) -> List[Dict]:
        _ = (_zone_analysis,)
        camera_info = self.get_camera_info_from_stream(stream_info)
        incidents = []
        total_people = counting_summary.get("total_objects", 0)
        current_timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

        self._ascending_alert_list = (
            self._ascending_alert_list[-900:] if len(self._ascending_alert_list) > 900 else self._ascending_alert_list
        )

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

        if total_people > 0:
            if total_people > 10:
                level = "critical"
                self._ascending_alert_list.append(3)
            elif total_people > 5:
                level = "significant"
                self._ascending_alert_list.append(2)
            elif total_people > 2:
                level = "medium"
                self._ascending_alert_list.append(1)
            else:
                level = "low"
                self._ascending_alert_list.append(0)

            human_text = (
                f"FENCE CLIMBING INCIDENTS @ {current_timestamp}:\n"
                f"\tSeverity Level: {level}\n"
                f"\tPersons in fence zone: {total_people}"
            )

            event = self.create_incident(
                incident_id=f"{self.CASE_TYPE}_{frame_id}_{int(time.time())}",
                incident_type=self.CASE_TYPE,
                severity_level=level,
                human_text=human_text,
                camera_info=camera_info,
                alerts=alerts,
                alert_settings=alert_settings,
            )
            incidents.append(event)
        else:
            self._ascending_alert_list.append(0)
            incidents.append({})

        return incidents

    # ------------------------------------------------------------------ #
    # Tracking stats
    # ------------------------------------------------------------------ #

    def _generate_tracking_stats(
        self,
        counting_summary: Dict,
        zone_analysis: Dict,
        config: FenceClimbingDetectionConfig,
        frame_id: str,
        alerts: Any = None,
        stream_info: Optional[Dict[str, Any]] = None,
    ) -> List[Dict]:
        if alerts is None:
            alerts = []

        total_people = counting_summary.get("total_objects", 0)
        total_unique_count = self.get_total_count()
        camera_info = self.get_camera_info_from_stream(stream_info)

        total_counts = []
        current_counts = []
        for category in config.person_categories or ["person"]:
            if total_unique_count > 0:
                total_counts.append(self.create_count_object(category, total_unique_count))
            current_frame_count = self.get_current_frame_count()
            if current_frame_count > 0 or total_people > 0:
                current_counts.append(self.create_count_object(category, current_frame_count))

        detections = []
        for det in counting_summary.get("detections", []):
            bbox = det.get("bounding_box", {})
            category = det.get("category", "person")
            detections.append(self.create_detection_object(category, bbox))

        current_timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

        human_text_lines = [f"FENCE CLIMBING STATUS @ {current_timestamp}:"]
        human_text_lines.append(f"\t- Persons detected: {total_people}")

        if zone_analysis:
            for zone_name, zone_data in zone_analysis.items():
                zone_current = zone_data.get("current_count", 0)
                zone_total = zone_data.get("total_count", 0)
                human_text_lines.append(f"\t- {zone_name}: {zone_current} current, {zone_total} total")

        human_text_lines.append(f"\t- Total unique tracked: {total_unique_count}")
        if not alerts:
            human_text_lines.append("Alerts: None")
        human_text = "\n".join(human_text_lines)

        tracking_stat = self.create_tracking_stats(
            total_counts,
            current_counts,
            detections,
            human_text,
            camera_info,
            alerts,
        )

        if zone_analysis:
            tracking_stat["zone_stats"] = [
                {
                    "zone_name": zn,
                    "current_count": zd.get("current_count", 0),
                    "total_count": zd.get("total_count", 0),
                    "current_track_ids": zd.get("current_track_ids", []),
                    "total_track_ids": zd.get("total_track_ids", []),
                }
                for zn, zd in zone_analysis.items()
            ]

        return [tracking_stat]

    # ------------------------------------------------------------------ #
    # Business analytics
    # ------------------------------------------------------------------ #

    def _generate_business_analytics(
        self,
        counting_summary: Dict,
        zone_analysis: Dict,
        config: FenceClimbingDetectionConfig,
        frame_id: str,
        stream_info: Optional[Dict[str, Any]] = None,
    ) -> List[Dict]:
        camera_info = self.get_camera_info_from_stream(stream_info)
        total_people = counting_summary.get("total_objects", 0)

        if total_people == 0 and not config.enable_analytics:
            return []

        analytics_stats = {
            "fence_zone_person_count": total_people,
            "unique_persons_tracked": self.get_total_count(),
            "current_frame_count": self.get_current_frame_count(),
        }

        if zone_analysis:
            for zone_name, zone_data in zone_analysis.items():
                analytics_stats[f"{zone_name}_occupancy"] = zone_data.get("current_count", 0)

        current_timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
        analytics_human_text = self.generate_analytics_human_text(
            "fence_climbing_analytics",
            analytics_stats,
            current_timestamp,
            current_timestamp,
        )

        analytics = self.create_business_analytics(
            "fence_climbing_analytics",
            analytics_stats,
            analytics_human_text,
            camera_info,
        )
        return [analytics]

    # ------------------------------------------------------------------ #
    # Summary
    # ------------------------------------------------------------------ #

    def _generate_summary(
        self,
        _summary: dict,
        incidents: List,
        tracking_stats: List,
        business_analytics: List,
        _alerts: List,
    ) -> List[str]:
        _ = (_alerts, _summary)
        lines = [
            f"Application Name: {self.CASE_TYPE}",
            f"Application Version: {self.CASE_VERSION}",
        ]
        if incidents:
            lines.append("Incidents: " + f"\n\t{incidents[0].get('human_text', 'No incidents detected')}")
        if tracking_stats:
            lines.append("Tracking Statistics: " + f"\t{tracking_stats[0].get('human_text', 'No tracking stats')}")
        if business_analytics:
            lines.append("Business Analytics: " + f"\t{business_analytics[0].get('human_text', 'No analytics')}")
        if not incidents and not tracking_stats and not business_analytics:
            lines.append("Summary: No Summary Data")

        return ["\n".join(lines)]
