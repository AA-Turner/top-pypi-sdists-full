"""
Illegal parking detection — vehicles that remain stationary in place (optionally inside
configured zones) for at least ``min_dwell_time_sec``.

Unlike stopped-vehicle monitoring, downstream consumers only receive detections once the
dwell threshold is met; moving or briefly stopped vehicles are withheld from the output.

Zone geometry (same API path as footfall):
  postProcessing.<camera_id>.zone_config.zones — normalized (0–1) polygon points from the UI,
  denormalized to pixels via camera resolution. Each zone is a list of [x, y] vertices
  (minimum 3 points; 4 points for a typical rectangle). Lines in zone_config are ignored.
"""

from __future__ import annotations

import threading
import time
from collections import deque
from dataclasses import dataclass, field, replace
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

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
    bbox_iou,
    bbox_smoothing,
    filter_by_confidence,
    match_results_structure,
)
from ..utils.geometry_utils import get_bbox_bottom10_center, get_bbox_bottom25_center, point_in_polygon
from ..utils.post_processing_config_client import PostProcessingConfigClient

DEFAULT_VEHICLE_CATEGORIES = ["bicycle", "motorcycle", "car", "van", "bus", "truck"]
_GEOMETRY_RETRY_INTERVAL = 30  # seconds between background API zone retries (footfall pattern)


DEFAULT_INDEX_TO_CATEGORY = {
    0: "bicycle",
    1: "motorcycle",
    2: "car",
    3: "van",
    4: "bus",
    5: "truck",
}


@dataclass
class IllegalParkingConfig(BaseConfig):
    """Configuration for illegal parking detection."""

    min_dwell_time_sec: float = 3.0
    short_term_displacement_threshold_px: float = 10.0
    long_term_drift_threshold_px: float = 12.0
    # Frames in the motion buffer before short-term stationary can be evaluated.
    stationary_min_observations: int = 10
    # When False, short-term stability alone can mark a track stationary (more sensitive).
    require_anchor_pair: bool = True
    # Max drift from fixed 1st/2nd anchor centers (stricter than short/long window).
    anchor_drift_threshold_px: float = 8.0
    # Max distance allowed between the 1st and 2nd anchor centers when locking stationary.
    anchor_pair_max_distance_px: float = 6.0
    anchor_pair_max_scale_fraction: float = 0.10
    anchor_drift_max_scale_fraction: float = 0.10
    # Only drop track state after this long without any detection (not a dwell reset timer).
    track_cleanup_sec: float = 120.0
    # Brief grace after bbox jitter / slight motion before clearing an active violation.
    violation_clear_sec: float = 1.0
    # Clear violation if the track is not seen in any detection this long (removes ghost boxes).
    off_screen_clear_sec: float = 2.0
    # Higher IoU required to merge a new tracker ID onto an existing vehicle (reduces wrong-object merge).
    track_merge_iou_threshold: float = 0.45
    track_merge_time_window_sec: float = 20.0
    # AdvancedTracker matching (higher = stricter, fewer ID swaps to nearby objects).
    tracker_match_thresh: float = 0.65
    tracker_unconfirmed_match_thresh: float = 0.75
    alert_cooldown_sec: float = 60.0

    zone_config: Optional[ZoneConfig] = None

    enable_smoothing: bool = True
    smoothing_algorithm: str = "observability"
    smoothing_window_size: int = 20
    smoothing_cooldown_frames: int = 5
    smoothing_confidence_range_factor: float = 0.5
    confidence_threshold: float = 0.2

    enable_class_aggregation: bool = True
    class_aggregation_window_size: int = 30

    usecase_categories: List[str] = field(default_factory=lambda: list(DEFAULT_VEHICLE_CATEGORIES))
    target_categories: List[str] = field(default_factory=lambda: list(DEFAULT_VEHICLE_CATEGORIES))
    alert_config: Optional[AlertConfig] = None
    index_to_category: Optional[Dict[int, str]] = field(default_factory=lambda: dict(DEFAULT_INDEX_TO_CATEGORY))

    def validate(self) -> List[str]:
        errors = super().validate()
        if self.min_dwell_time_sec <= 0:
            errors.append("min_dwell_time_sec must be positive")
        if self.short_term_displacement_threshold_px <= 0:
            errors.append("short_term_displacement_threshold_px must be positive")
        if self.long_term_drift_threshold_px <= 0:
            errors.append("long_term_drift_threshold_px must be positive")
        if self.violation_clear_sec <= 0:
            errors.append("violation_clear_sec must be positive")
        if self.anchor_drift_threshold_px <= 0:
            errors.append("anchor_drift_threshold_px must be positive")
        if self.anchor_pair_max_distance_px <= 0:
            errors.append("anchor_pair_max_distance_px must be positive")
        if self.stationary_min_observations < 2:
            errors.append("stationary_min_observations must be at least 2")
        if self.zone_config:
            errors.extend(self.zone_config.validate())
        if self.alert_config:
            errors.extend(self.alert_config.validate())
        return errors


def _zones_from_config(config: IllegalParkingConfig) -> Dict[str, List[List[float]]]:
    """Named polygon zones: {zone_name: [[x, y], ...], ...}."""
    zone_cfg = config.zone_config
    if zone_cfg is None:
        return {}
    if isinstance(zone_cfg, ZoneConfig):
        return dict(zone_cfg.zones or {})
    if isinstance(zone_cfg, dict):
        zones = zone_cfg.get("zones")
        return zones if isinstance(zones, dict) else {}
    return {}


def _bbox_to_position(bbox: Dict) -> Tuple[float, float, float, float]:
    if "xmin" in bbox:
        x = (bbox["xmin"] + bbox["xmax"]) / 2
        y = (bbox["ymin"] + bbox["ymax"]) / 2
        w = bbox["xmax"] - bbox["xmin"]
        h = bbox["ymax"] - bbox["ymin"]
    else:
        x = (bbox["x1"] + bbox["x2"]) / 2
        y = (bbox["y1"] + bbox["y2"]) / 2
        w = bbox["x2"] - bbox["x1"]
        h = bbox["y2"] - bbox["y1"]
    return (x, y, w, h)


def _motion_reference_point(bbox: Dict) -> Tuple[float, float, float]:
    """Bottom-10% reference point + scale (tighter than bottom-25% for center drift)."""
    ref_x, ref_y = get_bbox_bottom10_center(bbox)
    _, _, w, h = _bbox_to_position(bbox)
    scale = max(float(w), float(h), 1.0)
    return (float(ref_x), float(ref_y), scale)


def _zone_for_detection(bbox: Dict, zones: Dict[str, List[List[float]]]) -> Optional[str]:
    if not zones or not bbox:
        return None
    foot = get_bbox_bottom25_center(bbox)
    for zone_name, polygon in zones.items():
        pts = [(float(p[0]), float(p[1])) for p in polygon]
        if point_in_polygon(foot, pts):
            return zone_name
    return None


class _IllegalParkingTrackState:
    """Per-track stationary dwell state."""

    def __init__(
        self,
        track_id: int,
        bbox: Dict,
        timestamp: float,
        zone_name: Optional[str],
        config: IllegalParkingConfig,
    ):
        self.track_id = track_id
        self.config = config
        self.position_buffer: deque = deque(maxlen=30)
        self.position_buffer.append(_motion_reference_point(bbox))
        ref = _motion_reference_point(bbox)
        self.ewma_centroid = (ref[0], ref[1])
        self.ewma_alpha = 0.3
        self.first_seen = timestamp
        self.last_seen = timestamp
        self.stationary_start_time = timestamp
        self.is_stationary = False
        self.violation_confirmed = False
        self.current_zone = zone_name
        self.zone_entry_time = timestamp if zone_name else None
        self.last_alert_time: Optional[float] = None
        self.moving_since: Optional[float] = None
        self.anchor_primary: Optional[Tuple[float, float]] = None
        self.anchor_secondary: Optional[Tuple[float, float]] = None
        self.violation_confirmed_at: Optional[float] = None
        self.confirmed_dwell_sec: float = 0.0
        self.category: Optional[str] = None
        self.last_bbox = bbox

    def update(
        self,
        bbox: Dict,
        category: str,
        timestamp: float,
        zone_name: Optional[str],
        zones_configured: bool,
    ) -> bool:
        """Update state; return True if violation is active this frame."""
        self.category = category
        self.last_bbox = bbox
        self.last_seen = timestamp
        pos = _motion_reference_point(bbox)
        self.position_buffer.append(pos)
        centroid = (pos[0], pos[1])
        self.ewma_centroid = (
            self.ewma_alpha * centroid[0] + (1 - self.ewma_alpha) * self.ewma_centroid[0],
            self.ewma_alpha * centroid[1] + (1 - self.ewma_alpha) * self.ewma_centroid[1],
        )

        if zone_name != self.current_zone:
            self.current_zone = zone_name
            self.zone_entry_time = timestamp if zone_name else None
            if self.violation_confirmed and not zone_name and zones_configured:
                self._clear_violation()
                self.is_stationary = False

        short_ok = self._short_term_stationary()
        if short_ok:
            if self.anchor_primary is None:
                self.anchor_primary = (pos[0], pos[1])
            elif self.anchor_secondary is None:
                self.anchor_secondary = (pos[0], pos[1])
        if self.config.require_anchor_pair:
            actually_stationary = short_ok and self.anchor_secondary is not None and self._anchor_drift_ok(pos)
        else:
            actually_stationary = short_ok
        stationary_now = actually_stationary
        clear_after = float(self.config.violation_clear_sec)

        if not stationary_now:
            if self.moving_since is None:
                self.moving_since = timestamp
            elif self.violation_confirmed and (timestamp - self.moving_since) < clear_after:
                stationary_now = True

        if stationary_now:
            if actually_stationary:
                self.moving_since = None
            if not self.is_stationary:
                self.stationary_start_time = timestamp
            self.is_stationary = True
        else:
            self.is_stationary = False
            self.stationary_start_time = timestamp
            if not short_ok:
                self.anchor_primary = None
                self.anchor_secondary = None
            elif (
                self.anchor_primary is not None
                and self.anchor_secondary is not None
                and (not self._anchor_pair_ok(pos[2]) or not self._anchor_drift_ok(pos))
            ):
                self.anchor_primary = None
                self.anchor_secondary = None
            if self.moving_since and (timestamp - self.moving_since) >= clear_after:
                self._clear_violation()
            if not self.violation_confirmed:
                return False

        if zones_configured and self.current_zone is None:
            if self.violation_confirmed:
                self._clear_violation()
            return False

        if self.violation_confirmed:
            return True

        if not self.is_stationary:
            return False

        dwell_sec = timestamp - self.stationary_start_time
        if dwell_sec < self.config.min_dwell_time_sec:
            return False

        self.violation_confirmed = True
        self.violation_confirmed_at = timestamp
        self.confirmed_dwell_sec = dwell_sec
        return True

    def _clear_violation(self) -> None:
        self.violation_confirmed = False
        self.violation_confirmed_at = None
        self.confirmed_dwell_sec = 0.0

    def _motion_limits(self, scale: float) -> Tuple[float, float]:
        short_limit = max(
            self.config.short_term_displacement_threshold_px,
            0.10 * scale,
        )
        long_limit = max(
            self.config.long_term_drift_threshold_px,
            0.10 * scale,
        )
        return short_limit, long_limit

    def _short_term_stationary(self) -> bool:
        min_obs = max(2, int(getattr(self.config, "stationary_min_observations", 4)))
        if len(self.position_buffer) < min_obs:
            return False
        positions = list(self.position_buffer)
        max_displacement = 0.0
        for i in range(len(positions)):
            for j in range(i + 1, len(positions)):
                dx = positions[i][0] - positions[j][0]
                dy = positions[i][1] - positions[j][1]
                max_displacement = max(max_displacement, (dx * dx + dy * dy) ** 0.5)
        sizes = [p[2] for p in positions]
        avg_scale = sum(sizes) / len(sizes) if sizes else 1.0
        short_limit, _ = self._motion_limits(avg_scale)
        return max_displacement < short_limit

    def _anchor_limit(self, scale: float) -> float:
        return max(
            self.config.anchor_drift_threshold_px,
            self.config.anchor_drift_max_scale_fraction * scale,
        )

    def _anchor_pair_ok(self, scale: float) -> bool:
        if self.anchor_primary is None or self.anchor_secondary is None:
            return False
        pair_limit = max(
            self.config.anchor_pair_max_distance_px,
            self.config.anchor_pair_max_scale_fraction * scale,
        )
        dx = self.anchor_secondary[0] - self.anchor_primary[0]
        dy = self.anchor_secondary[1] - self.anchor_primary[1]
        return (dx * dx + dy * dy) ** 0.5 < pair_limit

    def _anchor_drift_ok(self, pos: Tuple[float, float, float]) -> bool:
        if self.anchor_primary is None or self.anchor_secondary is None:
            return False
        if not self._anchor_pair_ok(pos[2]):
            return False
        anchor_limit = self._anchor_limit(pos[2])
        for anchor in (self.anchor_primary, self.anchor_secondary):
            dx = pos[0] - anchor[0]
            dy = pos[1] - anchor[1]
            if (dx * dx + dy * dy) ** 0.5 >= anchor_limit:
                return False
        return True

    def display_dwell_sec(self, current_time: float) -> float:
        """Dwell seconds shown on output (stable during brief violation_clear grace)."""
        if self.violation_confirmed:
            if self.is_stationary:
                return max(self.confirmed_dwell_sec, current_time - self.stationary_start_time)
            return self.confirmed_dwell_sec
        if self.is_stationary:
            return max(0.0, current_time - self.stationary_start_time)
        return 0.0


class IllegalParkingDetectionUseCase(BaseProcessor):
    """Emit vehicle detections only after illegal-parking dwell threshold is met."""

    OUTPUT_CATEGORY = "illegal_parking"

    def __init__(self):
        super().__init__("illegal_parking_detection")
        self.category = "traffic"
        self.CASE_TYPE = "illegal_parking_detection"
        self.CASE_VERSION = "1.0"
        self.target_categories = list(DEFAULT_VEHICLE_CATEGORIES)
        self.smoothing_tracker: Optional[BBoxSmoothingTracker] = None
        self.tracker = None
        self._tracker_seam = ConfigDrivenTracker()
        self._total_frame_counter = 0
        self._track_states: Dict[int, _IllegalParkingTrackState] = {}
        self._total_violation_events = 0
        # Every canonical track ID ever seen, any of the 6 vehicle classes, violating
        # or not -- backs the "total_vehicles_tracked" VOLUME metric (analytics
        # config / legacy bridge), independent of the violation-only output detections.
        self._total_unique_vehicle_ids: set = set()
        self._total_confirmed_dwell_sum: float = 0.0
        # Reset every call to _collect_violation_detections(); read back by process()
        # to populate the per-frame side-channel fields the legacy bridge accumulates
        # over its ~60s publish window (mirrors car_damage_detection's frame_defect_ids
        # / frame_inspected_ids pattern) without changing this method's return value.
        self._last_frame_vehicle_ids: List[int] = []
        self._last_frame_confirmed_dwell_seconds: List[float] = []
        self._track_aliases: Dict[Any, Any] = {}
        self._canonical_tracks: Dict[Any, Dict[str, Any]] = {}
        self._track_merge_iou_threshold: float = 0.45
        self._track_merge_time_window: float = 20.0
        self._config_client: Optional[PostProcessingConfigClient] = None
        self._resolved_zone_config_cache: Optional[IllegalParkingConfig] = None
        self._geometry_thread: Optional[threading.Thread] = None
        self._zones_resolution_source: Optional[str] = None
        self._zones_diag_logged: bool = False

    def _zones_payload(self, zones: Dict[str, List[List[float]]]) -> Dict[str, List[List[float]]]:
        """Serialize zone polygons for agg_summary / logs."""
        return {name: [[float(p[0]), float(p[1])] for p in polygon if len(p) >= 2] for name, polygon in zones.items()}

    def _log_zone_diagnostics_once(
        self,
        zones: Dict[str, List[List[float]]],
        config: IllegalParkingConfig,
    ) -> None:
        if self._zones_diag_logged:
            return
        self._zones_diag_logged = True
        payload = self._zones_payload(zones)
        self.logger.info(
            "Illegal parking zone diagnostics: source=%s zones_configured=%s "
            "min_dwell_time_sec=%s zone_polygons_pixels=%s",
            self._zones_resolution_source or "none",
            bool(zones),
            config.min_dwell_time_sec,
            payload,
        )

    def set_config_client(self, client: PostProcessingConfigClient) -> None:
        """Set PostProcessingConfigClient for API zone polygons (by_app_deployment + camera_id)."""
        self._config_client = client

    def _start_zone_resolver(self, config: IllegalParkingConfig, stream_info: Dict[str, Any]) -> None:
        """Background retry for API zone geometry (same pattern as footfall)."""
        if self._geometry_thread is not None:
            return

        def _resolver() -> None:
            while True:
                try:
                    result = self._resolve_zone_config_from_api(config, stream_info)
                    if result is not None:
                        self._resolved_zone_config_cache = result
                        self.logger.info("Illegal parking: zone polygons resolved from API (background)")
                        return
                    self.logger.info(
                        "Illegal parking: API zones returned None, retrying in %ds",
                        _GEOMETRY_RETRY_INTERVAL,
                    )
                except Exception as exc:
                    self.logger.warning(
                        "Illegal parking: background zone resolve error: %s",
                        exc,
                    )
                time.sleep(_GEOMETRY_RETRY_INTERVAL)

        self._geometry_thread = threading.Thread(
            target=_resolver,
            daemon=True,
            name="illegal-parking-zone-resolver",
        )
        self._geometry_thread.start()
        self.logger.info("Illegal parking: started background zone resolver thread")

    def _resolve_zone_config_from_api(
        self,
        config: IllegalParkingConfig,
        stream_info: Optional[Dict[str, Any]],
    ) -> Optional[IllegalParkingConfig]:
        """Load polygon zones from deployment UI (same API flow as footfall).

        Reads ``zone_config.zones`` only (ignores ``lines``). Each zone value is a polygon:
        at least 3 ``[x, y]`` points in pixel space after denormalize (4 points = rectangle).
        """
        client = self._config_client or (stream_info.get("config_client") if stream_info else None)
        if not client and stream_info:
            try:
                client = PostProcessingConfigClient(logger=self.logger)
                if getattr(client, "_session", None) is None:
                    self.logger.info(
                        "Illegal parking: zone API skipped (no config_client; set MATRICE_* env "
                        "or call set_config_client())"
                    )
                    return None
                self._config_client = client
            except Exception as exc:
                self.logger.warning(
                    "Illegal parking: could not create config client for zone resolution: %s",
                    exc,
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

        width, height = client.get_resolution(camera_id)
        if width is None or height is None:
            return None

        doc_px = client.denormalize_config(filtered[0], width, height)
        post = doc_px.get("postProcessing") or {}
        cam_cfg = post.get(camera_id) or {}
        zone_config_raw = cam_cfg.get("zone_config") or {}
        zones_px = zone_config_raw.get("zones") or {}
        if not isinstance(zones_px, dict) or not zones_px:
            return None

        zones_dict: Dict[str, List[List[float]]] = {}
        for name, points in zones_px.items():
            if not isinstance(points, list) or len(points) < 3:
                self.logger.warning(
                    "Illegal parking: skipping zone '%s' (need >= 3 points, got %s)",
                    name,
                    len(points) if isinstance(points, list) else 0,
                )
                continue
            zones_dict[name] = [[float(p[0]), float(p[1])] for p in points if len(p) >= 2]

        if not zones_dict:
            return None

        self.logger.info(
            "Illegal parking: resolved %d zone polygon(s) from API: %s; pixels=%s",
            len(zones_dict),
            list(zones_dict.keys()),
            self._zones_payload(zones_dict),
        )
        self._zones_resolution_source = "api"
        return replace(config, zone_config=ZoneConfig(zones=zones_dict))

    def _build_zone_analysis(
        self,
        violation_detections: List[Dict],
        zones: Dict[str, List[List[float]]],
        zones_configured: bool,
    ) -> Dict[str, Dict[str, Any]]:
        if not zones_configured:
            return {}
        analysis = {
            name: {
                "active_violations": 0,
                "polygon_points": len(points),
                "polygon_pixels": [[float(p[0]), float(p[1])] for p in points],
            }
            for name, points in zones.items()
        }
        for det in violation_detections:
            zone_id = det.get("zone_id")
            if zone_id in analysis:
                analysis[zone_id]["active_violations"] += 1
        return analysis

    def process(
        self,
        data: Any,
        config: ConfigProtocol,
        context: Optional[ProcessingContext] = None,
        stream_info: Optional[Dict[str, Any]] = None,
    ) -> ProcessingResult:
        if not isinstance(config, IllegalParkingConfig) and not (
            getattr(config, "usecase", None) == "illegal_parking_detection"
            and getattr(config, "category", None) == "traffic"
        ):
            return self.create_error_result(
                "Invalid config type: expected IllegalParkingConfig",
                usecase=self.name,
                category=self.category,
                context=context,
            )

        if not isinstance(config, IllegalParkingConfig):
            zone_cfg = getattr(config, "zone_config", None)
            if zone_cfg and isinstance(zone_cfg, dict):
                zone_cfg = ZoneConfig(**zone_cfg)
            config = IllegalParkingConfig(
                category=getattr(config, "category", "traffic"),
                usecase=getattr(config, "usecase", "illegal_parking_detection"),
                confidence_threshold=getattr(config, "confidence_threshold", 0.4),
                target_categories=list(getattr(config, "target_categories", DEFAULT_VEHICLE_CATEGORIES)),
                usecase_categories=list(getattr(config, "usecase_categories", DEFAULT_VEHICLE_CATEGORIES)),
                index_to_category=dict(getattr(config, "index_to_category", DEFAULT_INDEX_TO_CATEGORY) or {}),
                min_dwell_time_sec=float(getattr(config, "min_dwell_time_sec", 3.0)),
                violation_clear_sec=float(getattr(config, "violation_clear_sec", 1.0)),
                stationary_min_observations=int(getattr(config, "stationary_min_observations", 10)),
                require_anchor_pair=bool(getattr(config, "require_anchor_pair", True)),
                short_term_displacement_threshold_px=float(
                    getattr(config, "short_term_displacement_threshold_px", 10.0)
                ),
                zone_config=zone_cfg,
                alert_config=getattr(config, "alert_config", None),
            )

        if context is None:
            context = ProcessingContext()

        inline_zones = _zones_from_config(config)
        if inline_zones and self._resolved_zone_config_cache is None:
            self._zones_resolution_source = "inline_config"
            self.logger.info(
                "Illegal parking: using zone_config from deployment config; pixels=%s",
                self._zones_payload(inline_zones),
            )

        # Resolve zone polygons from API on first frame (footfall-style); cache for later frames.
        if stream_info and self._resolved_zone_config_cache is None and self._geometry_thread is None:
            self.logger.info("Illegal parking: resolving zone polygons from API (first frame)")
            try:
                resolved = self._resolve_zone_config_from_api(config, stream_info)
                if resolved is not None:
                    self._resolved_zone_config_cache = resolved
                    self.logger.info("Illegal parking: zone polygons cached from API")
                else:
                    self.logger.warning(
                        "Illegal parking: API returned no zones on first frame; "
                        "starting background retry (interval %ds). Using inline zone_config if any.",
                        _GEOMETRY_RETRY_INTERVAL,
                    )
                    self._start_zone_resolver(config, stream_info)
            except Exception as exc:
                self.logger.warning(
                    "Illegal parking: zone resolution failed on first frame: %s; starting background retry",
                    exc,
                )
                self._start_zone_resolver(config, stream_info)

        if self._resolved_zone_config_cache is not None:
            config = self._resolved_zone_config_cache

        zones = _zones_from_config(config)
        zones_configured = bool(zones)
        if zones_configured and self._zones_resolution_source is None:
            self._zones_resolution_source = "inline_config"
        elif not zones_configured and self._zones_resolution_source is None:
            self._zones_resolution_source = "none"
        self._log_zone_diagnostics_once(zones, config)
        zone_polygons_payload = self._zones_payload(zones)

        data = self._normalize_yolo_results(data, config.index_to_category)
        context.input_format = match_results_structure(data)
        context.confidence_threshold = config.confidence_threshold

        processed = filter_by_confidence(data, config.confidence_threshold)
        if config.index_to_category:
            processed = apply_category_mapping(processed, config.index_to_category)
        processed = [d for d in processed if d.get("category") in config.target_categories]

        if config.enable_smoothing:
            if self.smoothing_tracker is None:
                self.smoothing_tracker = BBoxSmoothingTracker(
                    BBoxSmoothingConfig(
                        smoothing_algorithm=config.smoothing_algorithm,
                        window_size=config.smoothing_window_size,
                        cooldown_frames=config.smoothing_cooldown_frames,
                        confidence_threshold=config.confidence_threshold,
                        confidence_range_factor=config.smoothing_confidence_range_factor,
                        enable_smoothing=True,
                    )
                )
            processed = bbox_smoothing(processed, self.smoothing_tracker.config, self.smoothing_tracker)

        try:
            if self.tracker is None:
                self.tracker = self._tracker_seam.get_shared_tracker(
                    profile=TrackerProfile.DEFAULT,
                    enable_class_aggregation=config.enable_class_aggregation,
                    class_aggregation_window_size=config.class_aggregation_window_size,
                    match_thresh=float(getattr(config, "tracker_match_thresh", 0.65)),
                    unconfirmed_match_thresh=float(getattr(config, "tracker_unconfirmed_match_thresh", 0.75)),
                )
            processed = self.tracker.update(processed)
            self._track_merge_iou_threshold = float(
                getattr(config, "track_merge_iou_threshold", self._track_merge_iou_threshold)
            )
            self._track_merge_time_window = float(
                getattr(config, "track_merge_time_window_sec", self._track_merge_time_window)
            )
        except Exception as exc:
            self.logger.warning("AdvancedTracker failed for illegal parking: %s", exc)

        current_time = time.time()
        violation_detections = self._collect_violation_detections(
            processed, config, current_time, zones, zones_configured
        )
        self._total_frame_counter += 1

        frame_number = None
        if stream_info:
            inp = stream_info.get("input_settings", {})
            sf, ef = inp.get("start_frame"), inp.get("end_frame")
            if sf is not None and ef is not None and sf == ef:
                frame_number = sf
        frame_key = str(frame_number) if frame_number is not None else "current_frame"

        alerts = self._build_alerts(violation_detections, config, frame_key, current_time)
        counting_summary = self._count_categories(violation_detections)

        human_text = self._build_human_text(
            violation_detections,
            config,
            stream_info,
            zones,
            self._zones_resolution_source,
        )
        tracking_stats = self._build_tracking_stats(
            violation_detections, counting_summary, alerts, config, stream_info, human_text
        )

        zone_analysis = self._build_zone_analysis(violation_detections, zones, zones_configured)

        total_vehicles_tracked = len(self._total_unique_vehicle_ids)
        violation_rate = (
            round(self._total_violation_events / total_vehicles_tracked * 100.0, 2) if total_vehicles_tracked else 0.0
        )
        avg_dwell_time_sec = (
            round(self._total_confirmed_dwell_sum / self._total_violation_events, 2)
            if self._total_violation_events
            else 0.0
        )
        frame_violation_ids = [d["track_id"] for d in violation_detections if d.get("track_id") is not None]

        illegal_parking_analytics = {
            "active_violations": len(violation_detections),
            "total_violation_events": self._total_violation_events,
            # Session-cumulative VOLUME metrics matching
            # illegal-parking-detection-analytics-metrics.json (total_violations
            # maps to total_violation_events above; these three are the metrics
            # without an existing field). The legacy bridge re-derives its own
            # ~60s windowed versions from the frame_* lists below rather than
            # reading these cumulative snapshots directly.
            "total_vehicles_tracked": total_vehicles_tracked,
            "violation_rate": violation_rate,
            "avg_dwell_time_sec": avg_dwell_time_sec,
            "min_dwell_time_sec": config.min_dwell_time_sec,
            "zones_configured": zones_configured,
            "zone_names": list(zones.keys()) if zones_configured else [],
            "zones_source": self._zones_resolution_source or "none",
            "zone_polygons_pixels": zone_polygons_payload,
            # Per-frame ids/values for windowed rollups (legacy_analytics_bridge
            # accumulates these into unique sets / sums over its publish window,
            # same pattern as car_damage_detection's frame_defect_ids /
            # frame_inspected_ids).
            "frame_vehicle_ids": list(self._last_frame_vehicle_ids),
            "frame_violation_ids": frame_violation_ids,
            "frame_confirmed_dwell_seconds": list(self._last_frame_confirmed_dwell_seconds),
        }
        # Mirrored inside tracking_stats (not just top-level) so legacy_analytics_bridge
        # picks it up -- it only reads frame_data["tracking_stats"], same convention as
        # quality_analytics / wrong_way_analytics / hazard_analytics for other use cases.
        tracking_stats["illegal_parking_analytics"] = illegal_parking_analytics

        agg_summary = {
            frame_key: {
                "incidents": {},
                "tracking_stats": tracking_stats,
                "business_analytics": {},
                "alerts": alerts,
                "zone_analysis": zone_analysis,
                "illegal_parking_analytics": illegal_parking_analytics,
                "human_text": human_text,
            }
        }

        context.mark_completed()
        return self.create_result(
            data={"agg_summary": agg_summary},
            usecase=self.name,
            category=self.category,
            context=context,
        )

    def _collect_violation_detections(
        self,
        detections: List[Dict],
        config: IllegalParkingConfig,
        current_time: float,
        zones: Dict[str, List[List[float]]],
        zones_configured: bool,
    ) -> List[Dict]:
        self._track_merge_iou_threshold = float(
            getattr(config, "track_merge_iou_threshold", self._track_merge_iou_threshold)
        )
        self._track_merge_time_window = float(
            getattr(config, "track_merge_time_window_sec", self._track_merge_time_window)
        )
        current_ids = set()
        outputs: List[Dict] = []
        confirmed_dwell_this_frame: List[float] = []

        for det in detections:
            track_id = det.get("track_id")
            if track_id is None:
                continue
            bbox = det.get("bounding_box", det.get("bbox"))
            if not bbox:
                continue

            canonical_id = self._merge_or_register_track(track_id, bbox)
            try:
                raw_tid = int(track_id)
                tid = int(canonical_id)
            except (TypeError, ValueError):
                continue

            self._reconcile_track_state(raw_tid, tid)
            det["track_id"] = tid
            current_ids.add(tid)
            self._total_unique_vehicle_ids.add(tid)

            category = det.get("category", "vehicle")
            zone_name = _zone_for_detection(bbox, zones) if zones_configured else None

            if tid not in self._track_states:
                self._track_states[tid] = _IllegalParkingTrackState(tid, bbox, current_time, zone_name, config)

            state = self._track_states[tid]
            was_confirmed = state.violation_confirmed
            is_violation = state.update(
                bbox,
                category,
                current_time,
                zone_name,
                zones_configured,
            )
            if is_violation and not was_confirmed:
                self._total_violation_events += 1
                self._total_confirmed_dwell_sum += state.confirmed_dwell_sec
                confirmed_dwell_this_frame.append(state.confirmed_dwell_sec)

            if is_violation and tid in current_ids:
                out = dict(det)
                out["original_category"] = category
                out["category"] = self.OUTPUT_CATEGORY
                out["is_illegal_parking"] = True
                out["stationary_duration_sec"] = round(state.display_dwell_sec(current_time), 2)
                out["zone_id"] = state.current_zone
                out["min_dwell_time_sec"] = config.min_dwell_time_sec
                outputs.append(out)

        off_screen = float(getattr(config, "off_screen_clear_sec", 2.0))
        for tid, st in list(self._track_states.items()):
            if tid not in current_ids and st.violation_confirmed:
                if (current_time - st.last_seen) > off_screen:
                    st._clear_violation()

        self._cleanup_trackers(current_ids, current_time, config.track_cleanup_sec)
        self._last_frame_vehicle_ids = sorted(current_ids)
        self._last_frame_confirmed_dwell_seconds = confirmed_dwell_this_frame
        return outputs

    def _merge_or_register_track(self, raw_id: Any, bbox: Dict) -> Any:
        """Map flickering tracker IDs to one canonical ID when boxes overlap in time."""
        if raw_id is None or not bbox:
            return raw_id
        now = time.time()
        if raw_id in self._track_aliases:
            canonical_id = self._track_aliases[raw_id]
            info = self._canonical_tracks.get(canonical_id)
            if info is not None:
                info["last_bbox"] = bbox
                info["last_update"] = now
                info["raw_ids"].add(raw_id)
            return canonical_id

        for canonical_id, info in self._canonical_tracks.items():
            if now - info["last_update"] > self._track_merge_time_window:
                continue
            if bbox_iou(bbox, info["last_bbox"]) >= self._track_merge_iou_threshold:
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

    def _reconcile_track_state(self, raw_tid: int, canonical_tid: int) -> None:
        """Keep dwell state when the tracker assigns a new ID to the same vehicle."""
        if raw_tid == canonical_tid:
            return
        raw_state = self._track_states.pop(raw_tid, None)
        if raw_state is None:
            return
        if canonical_tid not in self._track_states:
            raw_state.track_id = canonical_tid
            self._track_states[canonical_tid] = raw_state
            return

        canon = self._track_states[canonical_tid]
        if raw_state.violation_confirmed:
            canon.violation_confirmed = True
        if raw_state.is_stationary:
            if not canon.is_stationary or raw_state.stationary_start_time < canon.stationary_start_time:
                canon.is_stationary = True
                canon.stationary_start_time = raw_state.stationary_start_time
        if raw_state.current_zone and (
            canon.current_zone is None
            or (
                raw_state.zone_entry_time is not None
                and (canon.zone_entry_time is None or raw_state.zone_entry_time < canon.zone_entry_time)
            )
        ):
            canon.current_zone = raw_state.current_zone
            canon.zone_entry_time = raw_state.zone_entry_time
        canon.position_buffer.extend(raw_state.position_buffer)
        canon.last_seen = max(canon.last_seen, raw_state.last_seen)
        if raw_state.category:
            canon.category = raw_state.category
        canon.last_bbox = raw_state.last_bbox

    def _cleanup_trackers(self, current_ids: set, current_time: float, max_age_sec: float) -> None:
        stale = []
        for tid, st in self._track_states.items():
            if tid in current_ids:
                continue
            grace = max_age_sec * 2 if st.violation_confirmed else max_age_sec
            if (current_time - st.last_seen) > grace:
                stale.append(tid)
        for tid in stale:
            del self._track_states[tid]

    def _build_alerts(
        self,
        violation_detections: List[Dict],
        config: IllegalParkingConfig,
        frame_key: str,
        current_time: float,
    ) -> List[Dict]:
        alerts: List[Dict] = []
        for det in violation_detections:
            tid = det.get("track_id")
            if tid is None:
                continue
            try:
                tid_int = int(tid)
            except (TypeError, ValueError):
                continue
            state = self._track_states.get(tid_int)
            if state is None:
                continue
            if state.last_alert_time is not None and (current_time - state.last_alert_time) < config.alert_cooldown_sec:
                continue
            state.last_alert_time = current_time
            alerts.append(
                {
                    "alert_type": getattr(config.alert_config, "alert_type", ["Default"])
                    if config.alert_config
                    else ["Default"],
                    "alert_id": f"illegal_parking_{tid_int}_{frame_key}",
                    "incident_category": self.CASE_TYPE,
                    "track_id": tid_int,
                    "zone_id": det.get("zone_id"),
                    "stationary_duration_sec": det.get("stationary_duration_sec"),
                    "vehicle_category": det.get("original_category"),
                    "threshold_sec": config.min_dwell_time_sec,
                }
            )
        return alerts

    def _build_human_text(
        self,
        violation_detections: List[Dict],
        config: IllegalParkingConfig,
        stream_info: Optional[Dict[str, Any]],
        zones: Dict[str, List[List[float]]],
        zones_source: Optional[str],
    ) -> str:
        ts = self._get_current_timestamp_str(stream_info)
        lines = [
            f"ILLEGAL PARKING @ {ts}",
            f"Active violations: {len(violation_detections)}",
            f"Dwell threshold: {config.min_dwell_time_sec:.1f}s",
            f"Zones configured: {bool(zones)} (source={zones_source or 'none'})",
        ]
        if zones:
            for zone_name, polygon in zones.items():
                pts = "; ".join(f"({int(p[0])},{int(p[1])})" for p in polygon if len(p) >= 2)
                lines.append(f"  zone {zone_name}: {pts}")
        else:
            lines.append("  zone polygons: (none loaded)")
        for det in violation_detections[:5]:
            lines.append(
                f"  - track {det.get('track_id')} ({det.get('original_category')}) "
                f"{det.get('stationary_duration_sec', 0):.1f}s"
                + (f" zone={det.get('zone_id')}" if det.get("zone_id") else "")
            )
        return "\n".join(lines)

    def _build_tracking_stats(
        self,
        violation_detections: List[Dict],
        counting_summary: Dict,
        alerts: List[Dict],
        config: IllegalParkingConfig,
        stream_info: Optional[Dict[str, Any]],
        human_text: str,
    ) -> Dict[str, Any]:
        camera_info = self.get_camera_info_from_stream(stream_info)
        detection_objs = []
        for det in violation_detections:
            bbox = det.get("bounding_box", det.get("bbox"))
            if not bbox:
                continue
            obj = self.create_detection_object(
                det.get("category", self.OUTPUT_CATEGORY),
                bbox,
                track_id=det.get("track_id"),
            )
            obj["is_illegal_parking"] = True
            obj["stationary_duration_sec"] = det.get("stationary_duration_sec")
            obj["original_category"] = det.get("original_category")
            detection_objs.append(obj)

        per_cat = counting_summary.get("per_category_count", {})
        # create_tracking_stats (and downstream consumers, e.g. legacy_analytics_bridge's
        # _count_list_to_map) expect a list of {"category", "count"} dicts, same
        # convention as weapon_detection / vehicle_monitoring -- not a raw {cat: count} map.
        per_cat_list = [{"category": cat, "count": count} for cat, count in per_cat.items()]
        return self.create_tracking_stats(
            total_counts=per_cat_list,
            current_counts=per_cat_list,
            detections=detection_objs,
            human_text=human_text,
            camera_info=camera_info,
            alerts=alerts,
            alert_settings=[],
            reset_settings=[{"interval_type": "daily", "reset_time": {"value": 9, "time_unit": "hour"}}],
            start_time=stream_info.get("stream_time", "") if stream_info else "",
            reset_time=stream_info.get("reset_time", "") if stream_info else "",
        )

    def _get_current_timestamp_str(self, stream_info: Optional[Dict[str, Any]]) -> str:
        if not stream_info:
            return datetime.now(timezone.utc).strftime("%Y:%m:%d %H:%M:%S")
        stream_time_str = stream_info.get("stream_time", "")
        if stream_time_str:
            return stream_time_str.replace(" UTC", "")[:19]
        return datetime.now(timezone.utc).strftime("%Y:%m:%d %H:%M:%S")

    def _normalize_yolo_results(self, data: Any, index_to_category: Optional[Dict[int, str]] = None) -> Any:
        if not index_to_category:
            return data

        def normalize_det(det: Dict) -> Dict:
            if not isinstance(det, dict):
                return det
            out = dict(det)
            cat = out.get("category")
            if isinstance(cat, int) and cat in index_to_category:
                out["category"] = index_to_category[cat]
            return out

        if isinstance(data, list):
            return [normalize_det(d) if isinstance(d, dict) else d for d in data]
        if isinstance(data, dict):
            return {
                k: [normalize_det(d) if isinstance(d, dict) else d for d in v] if isinstance(v, list) else v
                for k, v in data.items()
            }
        return data

    def _count_categories(self, detections: List[Dict]) -> Dict[str, Any]:
        per_cat: Dict[str, int] = {}
        for det in detections:
            cat = det.get("original_category") or det.get("category", "unknown")
            per_cat[cat] = per_cat.get(cat, 0) + 1
        return {
            "per_category_count": per_cat,
            "total_count": len(detections),
        }

    def create_default_config(self, **overrides) -> IllegalParkingConfig:
        defaults = {
            "category": "traffic",
            "usecase": "illegal_parking_detection",
            "confidence_threshold": 0.4,
            "target_categories": list(DEFAULT_VEHICLE_CATEGORIES),
            "usecase_categories": list(DEFAULT_VEHICLE_CATEGORIES),
            "index_to_category": dict(DEFAULT_INDEX_TO_CATEGORY),
            "min_dwell_time_sec": 3.0,
            "violation_clear_sec": 1.0,
            "stationary_min_observations": 10,
            "require_anchor_pair": True,
        }
        defaults.update(overrides)
        return IllegalParkingConfig(**defaults)
