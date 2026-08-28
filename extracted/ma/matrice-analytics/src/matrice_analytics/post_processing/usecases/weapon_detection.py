"""
Weapon Detection use case (single-camera).

Transforms raw detections into severity-graded incidents, alerts, and tracking
stats. Structured after the fire_detection active pattern:
  - state machines lifted into IncidentIdTracker
  - deduplicated alert-dict / severity-level logic extracted to helpers
  - single-camera assumption collapses camera_id resolution to a constant
  - adds min_confirmation_frames: N consecutive frames of sustained detection
    required before an incident is emitted (default 5; set to 1 to disable)
  - severity from max weapon-detection confidence (not bbox area or count):
      critical >= 70%, medium >= 40%, low >= 27%

Model emits: {0: "knife", 1: "gun", 2: "hands_without_gun", 3: "phone", 4: "pen",
5: "stick"}. Only knife/gun are treated as weapons (bounding boxes, tracking,
incidents, alerts); the remaining hard-negative training classes are mapped
for completeness but filtered out below.

Zone geometry (same API path as footfall):
  postProcessing.<camera_id>.zone_config.zones — normalized (0–1) polygon points
  from the UI, denormalized to pixels via camera resolution. When zones are
  configured, incidents are emitted only for weapons inside a polygon.
"""

import re
import threading
import time
from collections import Counter
from dataclasses import dataclass, field, replace
from datetime import datetime, timedelta, timezone
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
    bbox_smoothing,
    count_objects_in_zones,
    filter_by_confidence,
    match_results_structure,
)
from ..utils.geometry_utils import get_bbox_bottom25_center, point_in_polygon
from ..utils.incident_manager_utils import INCIDENT_MANAGER, IncidentManagerFactory
from ..utils.post_processing_config_client import PostProcessingConfigClient

# ============================================================================
# Constants
# ============================================================================

# Severity cutoffs on max weapon confidence % (ordered high→low; first match wins).
_SEVERITY_CUTOFFS: Tuple[Tuple[str, float], ...] = (
    ("critical", 70.0),
    ("medium", 40.0),
    ("low", 27.0),
)
_LEVEL_SETTINGS = {"low": 27, "medium": 40, "critical": 70}
_RESET_SETTINGS = [{"interval_type": "daily", "reset_time": {"value": 9, "time_unit": "hour"}}]

# Trend window used by both _check_alerts and _generate_incidents.
_TREND_LOOKBACK = 23
_TREND_PRIOR = 14

# IncidentIdTracker state-machine thresholds.
_HIT_CONFIRM_FRAMES = 7
_EMPTY_RESET_FRAMES = 130

# Rolling-buffer caps.
_ALERT_HISTORY_CAP = 5000

# Single-camera fallback when stream_info has no camera_id.
_DEFAULT_CAMERA_ID = "camera"
_GEOMETRY_RETRY_INTERVAL = 30  # Seconds between background retry attempts when API fails (footfall pattern)


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


# Default alert channel used when alert_config is missing.
_DEFAULT_ALERT_CONFIG_KWARGS = dict(
    count_thresholds={"knife": 0, "gun": 0},
    alert_type=["email"],
    alert_value=["hemanth.reddy@matrice.ai"],
    alert_incident_category=["WEAPON-ALERT"],
)


# ============================================================================
# Config
# ============================================================================


@dataclass
class WeaponDetectionConfig(BaseConfig):
    confidence_threshold: float = 0.28

    weapon_categories: List[str] = field(default_factory=lambda: ["knife", "gun"])
    target_categories: List[str] = field(default_factory=lambda: ["knife", "gun"])

    alert_config: Optional[AlertConfig] = field(default_factory=lambda: AlertConfig(**_DEFAULT_ALERT_CONFIG_KWARGS))

    index_to_category: Optional[Dict[int, str]] = field(
        default_factory=lambda: {
            0: "knife",
            1: "gun",
            2: "hands_without_gun",
            3: "phone",
            4: "pen",
            5: "stick",
        }
    )

    # BBox smoothing.
    enable_smoothing: bool = True
    smoothing_algorithm: str = "observability"
    smoothing_window_size: int = 20
    smoothing_cooldown_frames: int = 5
    smoothing_confidence_range_factor: float = 0.5

    # Consecutive frames of sustained detection required before emitting an
    # incident. Set to 1 to disable confirmation gating.
    min_confirmation_frames: int = 5

    # Incident-manager wiring.
    session: Optional[Any] = None
    server_id: Optional[str] = None

    # Optional polygon zones; incidents fire only for weapons inside when set.
    zone_config: Optional[ZoneConfig] = None

    def __post_init__(self):
        if not (0.0 <= self.confidence_threshold <= 1.0):
            raise ValueError("confidence_threshold must be between 0.0 and 1.0")
        self.weapon_categories = [c.lower() for c in self.weapon_categories]
        if self.index_to_category:
            self.index_to_category = {k: v.lower() for k, v in self.index_to_category.items()}
        if self.target_categories:
            self.target_categories = [c.lower() for c in self.target_categories]

    def validate(self) -> List[str]:
        """Validate weapon detection configuration.

        zone_config may be empty at load time when geometry will be resolved from
        API via stream_info + config_client in process().
        """
        errors = super().validate()
        if self.zone_config:
            errors.extend(self.zone_config.validate())
        return errors


# ============================================================================
# Pure helpers
# ============================================================================


def _level_from_confidence_pct(confidence_pct: float) -> str:
    for level, cutoff in _SEVERITY_CUTOFFS:
        if confidence_pct >= cutoff:
            return level
    return "low"


def _max_weapon_confidence_pct(detections: List[Dict]) -> float:
    """Map max weapon confidence to 0–100 (incident_quant for INCIDENT_MANAGER)."""
    if not detections:
        return 0.0
    max_conf = max(float(d.get("confidence", 0.0) or 0.0) for d in detections)
    return min(100.0, max_conf * 100.0)


def _trend_windows(history: List[str]) -> Optional[Tuple[str, str]]:
    """
    Return (older_dominant, newer_dominant) over the lookback window, or None
    if the history is too short.
    """
    if len(history) < _TREND_LOOKBACK:
        return None
    post = _TREND_LOOKBACK - _TREND_PRIOR - 1
    older = history[-_TREND_LOOKBACK:][:-_TREND_PRIOR]
    newer = history[-post:]
    older_dom = Counter(older).most_common(1)[0][0]
    newer_dom = Counter(newer).most_common(1)[0][0]
    return older_dom, newer_dom


def _is_trend_ascending(history: List[str]) -> bool:
    pair = _trend_windows(history)
    if pair is None:
        return True
    ring = ["low", "medium", "critical", "low"]
    older_dom, newer_dom = pair
    return ring.index(older_dom) <= ring.index(newer_dom)


def _alert_settings_dict(alert_config: Optional[AlertConfig]) -> Dict[str, str]:
    if not alert_config:
        return {}
    types = alert_config.alert_type or ["Default"]
    values = alert_config.alert_value or ["JSON"]
    return {t: v for t, v in zip(types, values)}


def _zones_from_config(config: WeaponDetectionConfig) -> Dict[str, List[List[float]]]:
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


def _zone_for_detection(bbox: Dict, zones: Dict[str, List[List[float]]]) -> Optional[str]:
    if not zones or not bbox:
        return None
    foot = get_bbox_bottom25_center(bbox)
    for zone_name, polygon in zones.items():
        pts = [(float(p[0]), float(p[1])) for p in polygon]
        if point_in_polygon(foot, pts):
            return zone_name
    return None


# ============================================================================
# Incident-id state machine
# ============================================================================


class IncidentIdTracker:
    """
    Tracks severity-level progression across frames to produce monotonically
    increasing incident/alert IDs (7 frames to advance a level; 130 empty
    frames to close an incident).
    """

    _HIT_CYCLE = ["low", "medium", "critical", "low"]

    def __init__(self):
        self.id_hit_list: List[str] = list(self._HIT_CYCLE)
        self.id_hit_counter: int = 0
        self.latest_stack: Optional[str] = None
        self.id_timing_list: List[str] = []
        self.return_id_counter: int = 1

    def advance(self, sev_level: str, current_ts: str) -> Tuple[int, int]:
        """
        Feed a severity level ("" if no detection). Returns (rank_id, alert_id).
        """
        if sev_level != "":
            if sev_level == self.id_hit_list[0] and len(self.id_hit_list) >= 2:
                self.id_hit_counter += 1
                if self.id_hit_counter > _HIT_CONFIRM_FRAMES:
                    self.latest_stack = self.id_hit_list[0]
                    self.id_hit_list.pop(0)
                    self.id_hit_counter = 0
                    self.id_timing_list.append(current_ts)
                    return (5 - len(self.id_hit_list), self.return_id_counter)
            elif self.id_hit_counter > 0:
                self.id_hit_counter -= 1
            elif self.id_hit_counter < 0:
                self.id_hit_counter = 0

            if len(self.id_hit_list) > 1:
                if sev_level == self.latest_stack:
                    return (5 - len(self.id_hit_list), self.return_id_counter)
                return (0, 0)
        else:
            if len(self.id_hit_list) == 1:
                self.id_hit_counter += 1
                if self.id_hit_counter > _EMPTY_RESET_FRAMES:
                    self.id_hit_list = list(self._HIT_CYCLE)
                    pre_return_id = self.return_id_counter
                    self.return_id_counter += 1
                    self.id_hit_counter = 0
                    self.latest_stack = None
                    self.id_timing_list.append(current_ts)
                    return (5, pre_return_id)
                if sev_level == self.latest_stack:
                    return (5 - len(self.id_hit_list), self.return_id_counter)
                return (0, 0)
            elif self.id_hit_counter > 0:
                self.id_hit_counter -= 1
            elif self.id_hit_counter < 0:
                self.id_hit_counter = 0

        return (1, 1)


# ============================================================================
# Use case
# ============================================================================


class WeaponDetectionUseCase(BaseProcessor):
    CASE_TYPE: Optional[str] = "weapon_detection"
    CASE_VERSION: Optional[str] = "1.3"
    _INCIDENT_LOG = "[INCIDENT_MANAGER]"

    def __init__(self):
        super().__init__("weapon_detection")
        self.category = "security"

        self.target_categories: List[str] = ["knife", "gun"]

        # Rolling state.
        self.smoothing_tracker: Optional[BBoxSmoothingTracker] = None
        self.tracker: Any = None
        self._tracker_seam = ConfigDrivenTracker()
        self._ascending_alert_list: List[str] = []
        self._consecutive_weapon_frames: int = 0
        self._total_weapons_detected_session: Dict[str, int] = {}
        self._prev_weapon_count: Dict[str, int] = {}
        self._weapon_uses_track_ids: bool = False
        self.current_incident_end_timestamp: str = "N/A"
        self.start_timer = None
        self._tracking_start_time = None

        # Incident-id state machine.
        self._id_tracker = IncidentIdTracker()

        # Incident manager.
        self._incident_manager_factory: Optional[IncidentManagerFactory] = None
        self._incident_manager: Optional[INCIDENT_MANAGER] = None
        self._incident_manager_initialized: bool = False
        self._legacy_redis_publisher: Any = None

        # Geometry resolution from API (footfall pattern).
        self._config_client: Optional[PostProcessingConfigClient] = None
        self._resolved_geometry_cache: Optional[WeaponDetectionConfig] = None
        self._geometry_thread: Optional[threading.Thread] = None
        self._zones_resolution_source: Optional[str] = None
        self._zones_diag_logged: bool = False

        # Zone-based tracking storage (footfall pattern).
        self._zone_current_track_ids: Dict[str, set] = {}
        self._zone_total_track_ids: Dict[str, set] = {}
        self._zone_current_counts: Dict[str, int] = {}
        self._zone_total_counts: Dict[str, int] = {}

    def _zones_payload(self, zones: Dict[str, List[List[float]]]) -> Dict[str, List[List[float]]]:
        """Serialize zone polygons for agg_summary / logs."""
        return {name: [[float(p[0]), float(p[1])] for p in polygon if len(p) >= 2] for name, polygon in zones.items()}

    def _log_zone_diagnostics_once(
        self,
        zones: Dict[str, List[List[float]]],
    ) -> None:
        if self._zones_diag_logged:
            return
        self._zones_diag_logged = True
        payload = self._zones_payload(zones)
        self.logger.info(
            "Weapon detection zone diagnostics: source=%s zones_configured=%s zone_polygons_pixels=%s",
            self._zones_resolution_source or "none",
            bool(zones),
            payload,
        )

    def set_config_client(self, client: Optional[PostProcessingConfigClient]) -> None:
        """Set PostProcessingConfigClient for API zone polygons (by_app_deployment + camera_id)."""
        self._config_client = client

    def _start_geometry_resolver(self, config: WeaponDetectionConfig, stream_info: Dict[str, Any]) -> None:
        """Spawn a daemon thread that resolves geometry from the API (footfall pattern)."""
        if self._geometry_thread is not None:
            return

        def _resolver() -> None:
            while True:
                try:
                    result = self._resolve_geometry_from_api(config, stream_info)
                    if result is not None:
                        self._resolved_geometry_cache = result
                        self.logger.info("Weapon detection: geometry resolved from API (background thread)")
                        return
                    self.logger.info(
                        "Weapon detection: API geometry returned None, retrying in %ds",
                        _GEOMETRY_RETRY_INTERVAL,
                    )
                except Exception as exc:
                    self.logger.warning(
                        "Weapon detection: background geometry resolve error: %s",
                        exc,
                    )
                time.sleep(_GEOMETRY_RETRY_INTERVAL)

        self._geometry_thread = threading.Thread(
            target=_resolver,
            daemon=True,
            name="weapon-detection-geometry-resolver",
        )
        self._geometry_thread.start()
        self.logger.info("Weapon detection: started background geometry resolver thread")

    def _resolve_geometry_from_api(
        self,
        config: WeaponDetectionConfig,
        stream_info: Optional[Dict[str, Any]],
    ) -> Optional[WeaponDetectionConfig]:
        """Resolve zone polygons from PostProcessingConfigClient (footfall API flow).

        Uses: get_stream_identifiers -> get_post_processing_configs_by_app_deployment ->
        filter_configs_by_camera_id -> get_resolution -> denormalize_config -> zone_config.zones.
        Returns a new config with zone_config populated, or None if unavailable.
        """
        client = self._config_client or (stream_info.get("config_client") if stream_info else None)
        if not client and stream_info:
            try:
                client = PostProcessingConfigClient(logger=self.logger)
                if getattr(client, "_session", None) is None:
                    self.logger.info(
                        "Weapon detection: _resolve_geometry_from_api skipped (no config_client; set "
                        "MATRICE_ACCESS_KEY_ID, MATRICE_SECRET_ACCESS_KEY, MATRICE_ACCOUNT_NUMBER "
                        "or call set_config_client() for API geometry resolution)"
                    )
                    return None
                self._config_client = client
            except Exception as exc:
                self.logger.warning(
                    "Weapon detection: _resolve_geometry_from_api could not create config client: %s",
                    exc,
                )
                return None
        if not stream_info:
            self.logger.info("Weapon detection: _resolve_geometry_from_api skipped (no stream_info)")
            return None
        if not client:
            self.logger.info(
                "Weapon detection: _resolve_geometry_from_api skipped (no config_client; set "
                "MATRICE_* env or call set_config_client() for API geometry resolution)"
            )
            return None

        ids = client.get_stream_identifiers(stream_info)
        app_deployment_id = ids.get("app_deployment_id") or ""
        camera_id = ids.get("camera_id") or ""
        self.logger.info(
            "Weapon detection: _resolve_geometry_from_api app_deployment_id=%s camera_id=%s",
            app_deployment_id or "(empty)",
            camera_id or "(empty)",
        )
        if not app_deployment_id or not camera_id:
            self.logger.info(
                "Weapon detection: _resolve_geometry_from_api returning None (missing app_deployment_id or camera_id)"
            )
            return None

        configs, err, _ = client.get_post_processing_configs_by_app_deployment(app_deployment_id)
        if err or not configs:
            self.logger.info(
                "Weapon detection: _resolve_geometry_from_api returning None "
                "(get_post_processing_configs_by_app_deployment: err=%r, configs count=%s)",
                err,
                len(configs) if configs else 0,
            )
            return None

        filtered = client.filter_configs_by_camera_id(configs, camera_id)
        if not filtered:
            self.logger.info(
                "Weapon detection: _resolve_geometry_from_api returning None "
                "(filter_configs_by_camera_id: no config for camera_id=%s)",
                camera_id,
            )
            return None

        width, height = client.get_resolution(camera_id)
        if width is None or height is None:
            self.logger.info(
                "Weapon detection: _resolve_geometry_from_api returning None "
                "(get_resolution: width=%r, height=%r for camera_id=%s)",
                width,
                height,
                camera_id,
            )
            return None

        self.logger.info(
            "Weapon detection: _resolve_geometry_from_api width=%r, height=%r",
            width,
            height,
        )
        doc_px = client.denormalize_config(filtered[0], width, height)
        post = doc_px.get("postProcessing") or {}
        cam_cfg = post.get(camera_id) or {}
        zone_config_raw = cam_cfg.get("zone_config") or {}
        zones_px = zone_config_raw.get("zones") or {}
        if not isinstance(zones_px, dict):
            zones_px = {}
        self.logger.info(
            "Weapon detection: _resolve_geometry_from_api zones_px=%r",
            zones_px,
        )
        if not zones_px:
            return None

        zones_dict: Dict[str, List[List[float]]] = {}
        for name, points in zones_px.items():
            if not isinstance(points, list) or len(points) < 3:
                self.logger.warning(
                    "Weapon detection: skipping zone '%s' (need >= 3 points, got %s)",
                    name,
                    len(points) if isinstance(points, list) else 0,
                )
                continue
            zones_dict[name] = [[float(p[0]), float(p[1])] for p in points if len(p) >= 2]

        if not zones_dict:
            return None

        self.logger.info(
            "Weapon detection: resolved %d zone polygon(s) from API: %s; pixels=%s",
            len(zones_dict),
            list(zones_dict.keys()),
            self._zones_payload(zones_dict),
        )
        self._zones_resolution_source = "api"
        return replace(config, zone_config=ZoneConfig(zones=zones_dict))

    def _apply_zone_filter(
        self,
        detections: List[Dict],
        zones: Dict[str, List[List[float]]],
        config: WeaponDetectionConfig,
    ) -> List[Dict]:
        """Keep non-weapon detections; weapons must fall inside a configured polygon."""
        weapon_cats = {c.lower() for c in config.weapon_categories}
        filtered: List[Dict] = []
        for det in detections:
            cat = str(det.get("category", "")).lower()
            if cat not in weapon_cats:
                filtered.append(det)
                continue
            bbox = det.get("bounding_box", det.get("bbox"))
            zone_name = _zone_for_detection(bbox, zones) if bbox else None
            if zone_name:
                out = dict(det)
                out["zone_id"] = zone_name
                filtered.append(out)
        return filtered

    def _update_zone_tracking(
        self,
        zone_analysis: Dict[str, Dict[str, int]],
        detections: List[Dict],
        config: WeaponDetectionConfig,
    ) -> Dict[str, Dict[str, Any]]:
        """Update per-zone weapon tracking (footfall pattern)."""
        if not zone_analysis or not config.zone_config or not config.zone_config.zones:
            return {}

        enhanced_zone_analysis: Dict[str, Dict[str, Any]] = {}
        zones = config.zone_config.zones
        weapon_cats = {c.lower() for c in config.weapon_categories}
        current_frame_zone_tracks: Dict[str, set] = {}

        for zone_name in zones.keys():
            current_frame_zone_tracks[zone_name] = set()
            if zone_name not in self._zone_current_track_ids:
                self._zone_current_track_ids[zone_name] = set()
            if zone_name not in self._zone_total_track_ids:
                self._zone_total_track_ids[zone_name] = set()

        for detection in detections:
            if str(detection.get("category", "")).lower() not in weapon_cats:
                continue
            track_id = detection.get("track_id")
            bbox = detection.get("bounding_box", detection.get("bbox"))
            if not bbox:
                continue
            center_point = get_bbox_bottom25_center(bbox)
            for zone_name, zone_polygon in zones.items():
                polygon_points = [(point[0], point[1]) for point in zone_polygon]
                if point_in_polygon(center_point, polygon_points):
                    if track_id is not None:
                        current_frame_zone_tracks[zone_name].add(track_id)

        for zone_name, zone_counts in zone_analysis.items():
            current_tracks = current_frame_zone_tracks.get(zone_name, set())
            original_weapon_count = 0
            if isinstance(zone_counts, dict):
                original_weapon_count = sum(int(v) for cat, v in zone_counts.items() if str(cat).lower() in weapon_cats)
            current_count = len(current_tracks) if current_tracks else original_weapon_count
            self._zone_current_track_ids[zone_name] = current_tracks
            self._zone_total_track_ids[zone_name].update(current_tracks)
            self._zone_current_counts[zone_name] = current_count
            if current_tracks:
                self._zone_total_counts[zone_name] = len(self._zone_total_track_ids[zone_name])
            else:
                self._zone_total_counts[zone_name] = max(
                    self._zone_total_counts.get(zone_name, 0),
                    original_weapon_count,
                )
            polygon = zones.get(zone_name, [])
            enhanced_zone_analysis[zone_name] = {
                "current_count": current_count,
                "total_count": self._zone_total_counts[zone_name],
                "active_weapons": current_count,
                "current_track_ids": list(current_tracks),
                "total_track_ids": list(self._zone_total_track_ids[zone_name]),
                "original_counts": zone_counts,
                "polygon_points": len(polygon),
                "polygon_pixels": [[float(p[0]), float(p[1])] for p in polygon],
            }
        return enhanced_zone_analysis

    def _get_legacy_redis_publisher(self) -> Any:
        if self._legacy_redis_publisher is None:
            from ...analytics.redis_publisher import AnalyticsRedisPublisher

            self._legacy_redis_publisher = AnalyticsRedisPublisher()
        return self._legacy_redis_publisher

    # ---- Incident manager lifecycle ---------------------------------------

    def _initialize_incident_manager_once(self, config: WeaponDetectionConfig) -> None:
        if self._incident_manager_initialized:
            return
        try:
            self.logger.info(f"{self._INCIDENT_LOG} Initializing incident manager for weapon detection...")
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

    # ---- Main pipeline ----------------------------------------------------

    def process(
        self,
        data: Any,
        config: ConfigProtocol,
        context: Optional[ProcessingContext] = None,
        stream_info: Optional[Dict[str, Any]] = None,
    ) -> ProcessingResult:
        start_time = time.time()
        try:
            if not isinstance(config, WeaponDetectionConfig):
                self._debug_elapsed_since(start_time)
                return self.create_error_result(
                    "Invalid configuration type for weapon detection",
                    usecase=self.name,
                    category=self.category,
                    context=context,
                )

            if not self._incident_manager_initialized:
                self._initialize_incident_manager_once(config)

            if context is None:
                context = ProcessingContext()
            context.input_format = match_results_structure(data)
            context.confidence_threshold = config.confidence_threshold
            self.logger.info(
                f"Processing weapon detection with format: "
                f"{context.input_format.value} "
                f"with threshold: {config.confidence_threshold}"
            )

            if config.alert_config is None:
                config.alert_config = AlertConfig(**_DEFAULT_ALERT_CONFIG_KWARGS)

            self.target_categories = [c.lower() for c in config.target_categories]

            # Resolve geometry from API exactly once (first frame only; footfall pattern).
            if stream_info and self._resolved_geometry_cache is None and self._geometry_thread is None:
                self.logger.info("Weapon detection: resolving geometry from API (first frame, blocking)")
                try:
                    resolved = self._resolve_geometry_from_api(config, stream_info)
                    if resolved is not None:
                        self._resolved_geometry_cache = resolved
                        self.logger.info("Weapon detection: geometry resolved and cached on first frame")
                    else:
                        self.logger.warning(
                            "Weapon detection: API returned None on first frame; "
                            "starting background retry thread (will not block future frames)"
                        )
                        self._start_geometry_resolver(config, stream_info)
                except Exception as exc:
                    self.logger.warning(
                        "Weapon detection: geometry resolution raised on first frame: %s; "
                        "starting background retry thread",
                        exc,
                    )
                    self._start_geometry_resolver(config, stream_info)

            # Use resolved geometry if available, else fallback to inline config.
            if self._resolved_geometry_cache is not None:
                config = self._resolved_geometry_cache
                self.logger.debug("Weapon detection: _resolved_geometry_cache assigned to config")

            inline_zones = _zones_from_config(config)
            if inline_zones and self._resolved_geometry_cache is None:
                self._zones_resolution_source = "inline_config"
                self.logger.info(
                    "Weapon detection: using zone_config from deployment config; pixels=%s",
                    self._zones_payload(inline_zones),
                )

            zones = _zones_from_config(config)
            zones_configured = bool(zones)
            if zones_configured and self._zones_resolution_source is None:
                self._zones_resolution_source = "inline_config"
            elif not zones_configured and self._zones_resolution_source is None:
                self._zones_resolution_source = "none"
            self._log_zone_diagnostics_once(zones)
            zone_polygons_payload = self._zones_payload(zones)

            processed = self._filter_and_map(data, config)
            processed = self._smooth_bboxes(processed, config)
            self._normalize_track_ids(processed)
            processed = self._run_tracker(processed, stream_info)
            if zones_configured:
                processed = self._apply_zone_filter(processed, zones, config)
            self._update_tracking_state(processed)
            summary = self._calculate_weapon_summary(processed, config)
            frame_number = self._extract_frame_number(stream_info)

            zone_analysis: Dict[str, Dict[str, Any]] = {}
            if zones_configured:
                weapon_dets = summary.get("detections", [])
                zone_analysis = count_objects_in_zones(weapon_dets, zones, stream_info)
                if zone_analysis:
                    enhanced_zone_analysis = self._update_zone_tracking(zone_analysis, weapon_dets, config)
                    for zone_name, enhanced_data in enhanced_zone_analysis.items():
                        zone_analysis[zone_name] = enhanced_data

            alerts = self._check_alerts(summary, config, stream_info)
            incidents_list = self._generate_incidents(summary, alerts, config, stream_info)
            tracking_stats_list = self._generate_tracking_stats(
                summary,
                alerts,
                config,
                frame_number=frame_number,
                stream_info=stream_info,
                zones=zones,
                zones_configured=zones_configured,
                zones_source=self._zones_resolution_source,
                zone_analysis=zone_analysis,
            )
            business_analytics_list = (
                self._generate_business_analytics(summary, alerts, config, stream_info, is_empty=True) or []
            )

            incident = incidents_list[0] if incidents_list else {}
            self._send_incident_to_manager(incident, stream_info, context=context)

            summary_list = self._generate_summary(incidents_list, tracking_stats_list, business_analytics_list)

            context.processing_time = time.time() - start_time
            tracking_stat = tracking_stats_list[0] if tracking_stats_list else {}

            if len(tracking_stats_list) > 1:
                alerts = tracking_stats_list[1]
                incident = tracking_stats_list[2]

            agg_summary = {
                str(frame_number): {
                    "incidents": incident,
                    "tracking_stats": tracking_stat,
                    "business_analytics": business_analytics_list,
                    "alerts": alerts,
                    "zone_analysis": zone_analysis,
                    "weapon_detection_analytics": {
                        "active_weapons": summary.get("total_objects", 0),
                        "zones_configured": zones_configured,
                        "zone_names": list(zones.keys()) if zones_configured else [],
                        "zones_source": self._zones_resolution_source or "none",
                        "zone_polygons_pixels": zone_polygons_payload,
                    },
                    "human_text": summary_list[0] if summary_list else {},
                }
            }
            context.mark_completed()
            result = self.create_result(
                data={"agg_summary": agg_summary},
                usecase=self.name,
                category=self.category,
                context=context,
            )
            self._debug_elapsed_since(start_time)
            return result

        except Exception as e:
            self.logger.error(f"Error in weapon detection processing: {e}", exc_info=True)
            self._debug_elapsed_since(start_time)
            return self.create_error_result(
                f"Weapon detection processing failed: {e}",
                error_type="WeaponDetectionProcessingError",
                usecase=self.name,
                category=self.category,
                context=context,
            )

    # ---- Pipeline stages --------------------------------------------------

    @staticmethod
    def _normalize_track_ids(processed: List[Dict]) -> None:
        """Normalize alternate tracker id fields to track_id (footfall pattern)."""
        for det in processed:
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

    def _run_tracker(self, processed: List[Dict], stream_info: Optional[Dict[str, Any]]) -> List[Dict]:
        """Assign track_id via AdvancedTracker (ByteTrack-style) when upstream
        detections don't already carry one (people_counting / weapon_human_detection
        pattern). Runs on the full detection set before zone filtering so a
        weapon keeps its track_id as it moves in/out of a drawn zone.

        On any failure, returns detections unchanged: _resolve_weapon_volume_counts
        then falls back to raw per-frame count deltas (fine as a safety net, but
        that fallback is what motivated giving every detection a real track_id
        here in the first place).
        """
        try:
            if self.tracker is None:
                self.tracker = self._tracker_seam.get_shared_tracker(
                    stream_info=stream_info,
                    profile=TrackerProfile.LEGACY_40,
                    namespace=True,
                    restore=True,
                    max_time_lost=int(1200),
                    frame_rate=25,
                )
            return self.tracker.update(processed)
        except Exception as exc:
            self.logger.warning(f"AdvancedTracker failed: {exc}")
            return processed

    def _filter_and_map(self, data: Any, config: WeaponDetectionConfig) -> List[Dict]:
        processed = data
        if config.confidence_threshold is not None:
            processed = filter_by_confidence(processed, config.confidence_threshold)
        if config.index_to_category:
            processed = apply_category_mapping(processed, config.index_to_category)
        if self.target_categories:
            processed = [d for d in processed if d.get("category", "").lower() in self.target_categories]
        return processed

    def _smooth_bboxes(self, processed: List[Dict], config: WeaponDetectionConfig) -> List[Dict]:
        if not config.enable_smoothing:
            return processed
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

        smoothable = set(self.target_categories)
        to_smooth = [d for d in processed if d.get("category", "").lower() in smoothable]
        others = [d for d in processed if d.get("category", "").lower() not in smoothable]
        smoothed = bbox_smoothing(to_smooth, self.smoothing_tracker.config, self.smoothing_tracker)
        return others + smoothed

    @staticmethod
    def _extract_frame_number(
        stream_info: Optional[Dict[str, Any]],
    ) -> Optional[int]:
        if not stream_info:
            return None
        input_settings = stream_info.get("input_settings", {})
        start = input_settings.get("start_frame")
        end = input_settings.get("end_frame")
        if start is not None and end is not None and start == end:
            return start
        return start

    def _calculate_weapon_summary(self, data: Any, config: WeaponDetectionConfig) -> Dict[str, Any]:
        if not isinstance(data, list):
            return {
                "total_objects": 0,
                "by_category": {},
                "detections": [],
                "by_category_tracking": {},
            }

        tracking_cats = [c.lower() for c in config.target_categories]
        by_category_tracking: Dict[str, int] = {c: 0 for c in tracking_cats}
        for d in data:
            if not isinstance(d, dict):
                continue
            c = d.get("category", "").lower()
            if c in by_category_tracking:
                by_category_tracking[c] = by_category_tracking.get(c, 0) + 1

        valid = [c.lower() for c in config.weapon_categories]
        detections = [d for d in data if isinstance(d, dict) and d.get("category", "").lower() in valid]
        per_cat: Dict[str, int] = {}
        for d in detections:
            c = d.get("category", "unknown").lower()
            per_cat[c] = per_cat.get(c, 0) + 1

        by_cat = {
            cat: sum(1 for d in detections if d.get("category", "").lower() == cat.lower())
            for cat in config.weapon_categories
        }
        return {
            "total_objects": len(detections),
            "by_category": by_cat,
            "detections": detections,
            "per_category_count": per_cat,
            "by_category_tracking": by_category_tracking,
        }

    # ---- Alerts -----------------------------------------------------------

    def _check_alerts(
        self,
        summary: Dict,
        config: WeaponDetectionConfig,
        stream_info: Optional[Dict[str, Any]] = None,
    ) -> List[Dict]:
        total = summary.get("total_objects", 0)
        if total == 0 or not config.alert_config:
            return []
        thresholds = getattr(config.alert_config, "count_thresholds", None) or {}
        if not thresholds:
            return []

        last_level = self._ascending_alert_list[-1] if self._ascending_alert_list else "low"
        current_ts = self._get_current_timestamp_str(stream_info)
        rank_ids, alert_id = self._id_tracker.advance(last_level, current_ts)
        if rank_ids not in (1, 2, 3, 4, 5):
            alert_id = 1

        trend = _is_trend_ascending(self._ascending_alert_list)
        per_cat = summary.get("per_category_count", {})
        alerts: List[Dict] = []
        for category, threshold in thresholds.items():
            if isinstance(threshold, str):
                threshold = int(threshold)
            if category == "all":
                if total > threshold:
                    alerts.append(self._build_alert(category, alert_id, threshold, trend, config))
            elif category in per_cat and per_cat[category] > threshold:
                alerts.append(self._build_alert(category, alert_id, threshold, trend, config))
        return alerts

    def _build_alert(
        self,
        category: str,
        alert_id: int,
        threshold: int,
        ascending: bool,
        config: WeaponDetectionConfig,
    ) -> Dict:
        ac = config.alert_config
        alert_type = (ac.alert_type if ac else ["Default"]) or ["Default"]
        return {
            "alert_type": alert_type,
            "alert_id": f"alert_{category}_{alert_type[0]}_{alert_id}",
            "incident_category": self.CASE_TYPE,
            "threshold_level": threshold,
            "ascending": ascending,
            "settings": _alert_settings_dict(ac),
        }

    # ---- Incidents --------------------------------------------------------

    def _generate_incidents(
        self,
        summary: Dict,
        alerts: List[Dict],
        config: WeaponDetectionConfig,
        stream_info: Optional[Dict[str, Any]] = None,
    ) -> List[Dict]:
        total = summary.get("total_objects", 0)
        current_ts = self._get_current_timestamp_str(stream_info)
        camera_info = self.get_camera_info_from_stream(stream_info)

        if len(self._ascending_alert_list) > _ALERT_HISTORY_CAP:
            self._ascending_alert_list = self._ascending_alert_list[-_ALERT_HISTORY_CAP:]

        if total == 0:
            self._consecutive_weapon_frames = 0
            return [{}]

        self._consecutive_weapon_frames += 1
        if self._consecutive_weapon_frames < config.min_confirmation_frames:
            self.logger.debug(
                f"Weapon detected but awaiting confirmation: "
                f"{self._consecutive_weapon_frames}/{config.min_confirmation_frames} frames"
            )
            return [{}]

        thresholds = getattr(config.alert_config, "count_thresholds", None) or {}
        per_cat = summary.get("per_category_count", {})
        if not thresholds and per_cat:
            thresholds = {cat: 0 for cat in per_cat.keys()}
            self.logger.debug(f"[INCIDENT] count_thresholds was empty, using detected categories: {thresholds}")

        detections = summary.get("detections", [])
        incidents: List[Dict] = []
        for category in thresholds:
            if category == "all" or category in per_cat:
                incidents.append(
                    self._build_incident(
                        detections,
                        config,
                        alerts,
                        camera_info,
                        current_ts,
                        stream_info,
                        is_fallback=False,
                    )
                )
                break

        if not incidents:
            self.logger.warning(
                f"[INCIDENT] No incident generated despite {total} detections. Generating fallback incident."
            )
            incidents.append(
                self._build_incident(
                    detections,
                    config,
                    alerts,
                    camera_info,
                    current_ts,
                    stream_info,
                    is_fallback=True,
                )
            )
        return incidents

    def _build_incident(
        self,
        detections: List[Dict],
        config: WeaponDetectionConfig,
        alerts: List[Dict],
        camera_info: Dict,
        current_ts: str,
        stream_info: Optional[Dict[str, Any]],
        is_fallback: bool,
    ) -> Dict:
        start_ts = self._get_start_timestamp_str(stream_info)
        self._debug_stream_timing("start_timestamp", start_ts)

        if not is_fallback:
            self._update_incident_end_timestamp(start_ts)
        else:
            self.current_incident_end_timestamp = "Incident still active"

        confidence_pct = _max_weapon_confidence_pct(detections)
        level = _level_from_confidence_pct(confidence_pct)
        self._ascending_alert_list.append(level)

        rank_ids, incident_id = self._id_tracker.advance(level, current_ts)
        if rank_ids not in (1, 2, 3, 4, 5):
            incident_id = 1
        timing = self._id_tracker.id_timing_list
        if timing:
            if len(timing) == rank_ids:
                start_ts = timing[-1]
            if len(timing) > 3 and level == "critical":
                start_ts = timing[-1]

        human_text = f"INCIDENT DETECTED: {self.CASE_TYPE} severity={level}"
        zone_ids = sorted({str(d.get("zone_id")) for d in detections if d.get("zone_id")})
        if zone_ids:
            human_text += f" zone={','.join(zone_ids)}"

        alert_settings = self._alert_settings_block(config) if not is_fallback else []
        end_time = self.current_incident_end_timestamp if not is_fallback else "Incident still active"
        incident_suffix = "fallback" if is_fallback else str(incident_id)

        event = self.create_incident(
            incident_id=f"incident_{self.CASE_TYPE}_{incident_suffix}",
            incident_type=self.CASE_TYPE,
            severity_level=level,
            human_text=human_text,
            camera_info=camera_info,
            alerts=alerts,
            alert_settings=alert_settings,
            start_time=start_ts,
            end_time=end_time,
            level_settings=_LEVEL_SETTINGS,
        )
        if not is_fallback:
            event["duration"] = self.get_duration_seconds(start_ts, self.current_incident_end_timestamp)
        event["incident_quant"] = confidence_pct
        if zone_ids:
            event["zone_id"] = zone_ids[0] if len(zone_ids) == 1 else zone_ids
        return event

    def _update_incident_end_timestamp(self, start_ts: str) -> None:
        """
        State machine:
          "N/A"                   -> "Incident still active"  (on start)
          "Incident still active" -> "Incident active"        (on dominant-level flip)
          anything else           -> "N/A"                    (reset)
        """
        if start_ts and self.current_incident_end_timestamp == "N/A":
            self.current_incident_end_timestamp = "Incident still active"
        elif start_ts and self.current_incident_end_timestamp == "Incident still active":
            pair = _trend_windows(self._ascending_alert_list)
            if pair is not None and pair[0] != pair[1]:
                self.current_incident_end_timestamp = "Incident active"
        elif self.current_incident_end_timestamp not in (
            "Incident still active",
            "N/A",
        ):
            self.current_incident_end_timestamp = "N/A"

    def _alert_settings_block(self, config: WeaponDetectionConfig) -> List[Dict]:
        ac = config.alert_config
        if not ac:
            return []
        return [
            {
                "alert_type": ac.alert_type or ["Default"],
                "incident_category": self.CASE_TYPE,
                "threshold_level": ac.count_thresholds or {},
                "ascending": True,
                "settings": _alert_settings_dict(ac),
            }
        ]

    # ---- Tracking stats ---------------------------------------------------

    def _resolve_weapon_volume_counts(
        self,
        summary: Dict,
        config: WeaponDetectionConfig,
    ) -> Tuple[Dict[str, int], Dict[str, int]]:
        """Return (new_by_category, total_by_category) using track IDs when available.

        Per-category (knife/gun) rather than a single merged bucket, so
        business analytics can tell knife incidents from gun incidents.
        """
        weapon_cats = [c.lower() for c in config.weapon_categories]
        by_cat = summary.get("by_category", {})
        weapon_dets = [d for d in summary.get("detections", []) if str(d.get("category", "")).lower() in weapon_cats]
        if any(d.get("track_id") is not None for d in weapon_dets):
            self._weapon_uses_track_ids = True

        if self._weapon_uses_track_ids:
            new_counts_dict = self.get_new_counts_this_frame()
            total_counts_dict = self.get_total_counts()
            new_by_cat = {cat: int(new_counts_dict.get(cat, 0)) for cat in weapon_cats}
            total_by_cat = {cat: int(total_counts_dict.get(cat, 0)) for cat in weapon_cats}
            return new_by_cat, total_by_cat

        # No track_id from upstream: add only net new boxes vs previous frame, per category.
        new_by_cat = {}
        for cat in weapon_cats:
            count = int(by_cat.get(cat, 0))
            new_by_cat[cat] = max(0, count - self._prev_weapon_count.get(cat, 0))
            self._total_weapons_detected_session[cat] = (
                self._total_weapons_detected_session.get(cat, 0) + new_by_cat[cat]
            )
            self._prev_weapon_count[cat] = count
        total_by_cat = {cat: self._total_weapons_detected_session.get(cat, 0) for cat in weapon_cats}
        return new_by_cat, total_by_cat

    def _generate_tracking_stats(
        self,
        summary: Dict,
        alerts: List,
        config: WeaponDetectionConfig,
        frame_number: Optional[int] = None,
        stream_info: Optional[Dict[str, Any]] = None,
        zones: Optional[Dict[str, List[List[float]]]] = None,
        zones_configured: bool = False,
        zones_source: Optional[str] = None,
        zone_analysis: Optional[Dict[str, Dict[str, Any]]] = None,
    ) -> List:
        _ = frame_number
        camera_info = self.get_camera_info_from_stream(stream_info)
        weapon_cats = [c.lower() for c in config.weapon_categories]
        by_cat = summary.get("by_category", {})
        by_cat_track = summary.get("by_category_tracking") or {}
        count_by_cat = {cat: int(by_cat_track.get(cat, by_cat.get(cat, 0))) for cat in weapon_cats}
        weapon_count = sum(count_by_cat.values())

        new_by_cat, total_by_cat = self._resolve_weapon_volume_counts(summary, config)
        weapon_new = sum(new_by_cat.values())

        current_ts = self._get_current_timestamp_str(stream_info)
        start_ts = self._get_start_timestamp_str(stream_info)
        self._debug_stream_timing("start_timestamp", start_ts)
        high_precision_start = self._get_current_timestamp_str(stream_info, precision=True)
        high_precision_reset = self._get_start_timestamp_str(stream_info, precision=True)

        current_counts = [{"category": cat, "count": count_by_cat[cat]} for cat in weapon_cats]
        current_new_counts = [{"category": cat, "count": new_by_cat.get(cat, 0)} for cat in weapon_cats]
        total_counts = [{"category": cat, "count": total_by_cat.get(cat, 0)} for cat in weapon_cats]
        total_current_counts = [{"category": cat, "count": count_by_cat[cat]} for cat in weapon_cats]

        lines = [
            f"CURRENT FRAME @ {current_ts}:",
            f"\t- Weapons in Frame: {weapon_count}",
            f"\t- New Weapons (just entered): {weapon_new}",
        ]
        for cat in weapon_cats:
            lines.append(f"\t\t- {cat}: {count_by_cat[cat]} (new: {new_by_cat.get(cat, 0)})")
        if zones_configured:
            lines.append(f"\t- Zones configured: yes (source={zones_source or 'none'})")
            if zone_analysis:
                lines.append("\t- Zone counts:")
                for zone_name, zone_data in zone_analysis.items():
                    if isinstance(zone_data, dict):
                        current_count = zone_data.get(
                            "active_weapons",
                            zone_data.get("current_count", 0),
                        )
                    else:
                        current_count = zone_data
                    lines.append(f"\t\t- {zone_name}: {int(current_count)}")
            elif zones:
                for zone_name, polygon in zones.items():
                    pts = "; ".join(f"({int(p[0])},{int(p[1])})" for p in polygon if len(p) >= 2)
                    lines.append(f"\t  zone {zone_name}: {pts}")
        human_text = "\n".join(lines)

        detections: List[Dict] = []
        weapon_cats = {c.lower() for c in config.weapon_categories}
        for det in summary.get("detections", []):
            if str(det.get("category", "")).lower() not in weapon_cats:
                continue
            bbox = det.get("bounding_box", {})
            category = det.get("category", "Weapon")
            seg = det.get("masks") or det.get("segmentation") or det.get("mask")
            if seg is not None:
                obj = self.create_detection_object(category, bbox, segmentation=seg)
            else:
                obj = self.create_detection_object(category, bbox)
            if det.get("zone_id"):
                obj["zone_id"] = det["zone_id"]
            detections.append(obj)

        alert_settings = self._alert_settings_block(config)
        tracking_stat = self.create_tracking_stats(
            total_counts=total_counts,
            current_counts=current_counts,
            detections=detections,
            human_text=human_text,
            camera_info=camera_info,
            alerts=alerts,
            alert_settings=alert_settings,
            reset_settings=_RESET_SETTINGS,
            start_time=high_precision_start,
            reset_time=high_precision_reset,
        )
        tracking_stat["target_categories"] = list(config.weapon_categories)
        tracking_stat["current_new_counts"] = current_new_counts
        tracking_stat["total_current_counts"] = total_current_counts
        tracking_stats: List = [tracking_stat]
        return tracking_stats

    # ---- Business analytics / summary / schema ---------------------------

    def _generate_business_analytics(
        self,
        _summary: Dict,
        _alerts: Any,
        _config: WeaponDetectionConfig,
        _stream_info: Optional[Dict[str, Any]] = None,
        is_empty: bool = False,
    ) -> Optional[List[Dict]]:
        if is_empty:
            return []
        return None

    def _generate_summary(
        self,
        incidents: List[Dict],
        tracking_stats: List,
        business_analytics: List,
    ) -> List[str]:
        lines = [
            f"Application Name: {self.CASE_TYPE}",
            f"Application Version: {self.CASE_VERSION}",
        ]
        if incidents:
            first = incidents[0] if isinstance(incidents[0], dict) else {}
            lines.append("Incidents: " + f"\n\t{first.get('human_text', 'No incidents detected')}")
        if tracking_stats:
            first = tracking_stats[0] if isinstance(tracking_stats[0], dict) else {}
            lines.append("Tracking Statistics: " + f"\t{first.get('human_text', 'No tracking statistics detected')}")
        if business_analytics:
            first = business_analytics[0] if isinstance(business_analytics[0], dict) else {}
            lines.append("Business Analytics: " + f"\t{first.get('human_text', 'No business analytics detected')}")
        if not incidents and not tracking_stats and not business_analytics:
            lines.append("Summary: No Summary Data")
        return ["\n".join(lines)]

    def get_config_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "confidence_threshold": {
                    "type": "number",
                    "minimum": 0.0,
                    "maximum": 1.0,
                    "default": 0.28,
                    "description": "Minimum confidence threshold for detections",
                },
                "weapon_categories": {
                    "type": "array",
                    "items": {"type": "string"},
                    "default": ["knife", "gun"],
                    "description": "Category names counted as weapons for incidents and alert totals",
                },
                "min_confirmation_frames": {
                    "type": "integer",
                    "minimum": 1,
                    "default": 5,
                    "description": "Consecutive frames of sustained detection required before an incident is emitted",
                },
                "zone_config": {
                    "type": "object",
                    "description": "Optional polygon zones; incidents fire only for weapons inside when configured",
                    "properties": {
                        "zones": {
                            "type": "object",
                            "additionalProperties": {
                                "type": "array",
                                "items": {
                                    "type": "array",
                                    "items": {"type": "number"},
                                    "minItems": 2,
                                    "maxItems": 2,
                                },
                                "minItems": 3,
                            },
                        }
                    },
                },
                "index_to_category": {
                    "type": "object",
                    "additionalProperties": {"type": "string"},
                    "description": "Mapping from category indices to names",
                },
                "alert_config": {
                    "type": "object",
                    "properties": {
                        "count_thresholds": {
                            "type": "object",
                            "additionalProperties": {
                                "type": "integer",
                                "minimum": 1,
                            },
                            "description": "Count thresholds for alerts",
                        }
                    },
                },
            },
            "required": ["confidence_threshold"],
            "additionalProperties": False,
        }

    def create_default_config(self, **overrides) -> WeaponDetectionConfig:
        defaults = {
            "category": self.category,
            "usecase": self.name,
            "confidence_threshold": 0.28,
            "weapon_categories": ["knife", "gun"],
        }
        defaults.update(overrides)
        return WeaponDetectionConfig(**defaults)

    # ---- Tracking stubs (API compatibility) ------------------------------

    def _update_tracking_state(self, detections: list) -> None:
        """Update per-category track-id sets used for current_new/total_counts."""
        if not hasattr(self, "_per_category_total_track_ids"):
            self._per_category_total_track_ids = {cat: set() for cat in self.target_categories}
        if not hasattr(self, "_previous_frame_track_ids"):
            self._previous_frame_track_ids = {cat: set() for cat in self.target_categories}
        self._current_frame_track_ids = {cat: set() for cat in self.target_categories}
        for det in detections:
            cat = str(det.get("category", "")).lower()
            track_id = det.get("track_id")
            if cat not in self.target_categories or track_id is None:
                continue
            self._per_category_total_track_ids.setdefault(cat, set()).add(track_id)
            self._current_frame_track_ids[cat].add(track_id)
        self._new_track_ids_this_frame = {
            cat: (self._current_frame_track_ids.get(cat, set()) - self._previous_frame_track_ids.get(cat, set()))
            for cat in self.target_categories
        }
        self._previous_frame_track_ids = {cat: set(ids) for cat, ids in self._current_frame_track_ids.items()}

    def get_total_counts(self) -> Dict[str, int]:
        return {cat: len(ids) for cat, ids in getattr(self, "_per_category_total_track_ids", {}).items()}

    def get_new_counts_this_frame(self) -> Dict[str, int]:
        return {cat: len(ids) for cat, ids in getattr(self, "_new_track_ids_this_frame", {}).items()}

    def get_current_frame_counts(self) -> Dict[str, int]:
        return {cat: len(ids) for cat, ids in getattr(self, "_current_frame_track_ids", {}).items()}

    # ---- Timestamp plumbing (preserved from prior version) ---------------

    def _format_timestamp_for_stream(self, timestamp: float) -> str:
        dt = datetime.fromtimestamp(timestamp, tz=timezone.utc)
        if dt.year < 2000:
            dt = datetime.now(timezone.utc)
        return dt.strftime("%Y:%m:%d %H:%M:%S")

    def _format_timestamp_for_video(self, timestamp: float) -> str:
        hours = int(timestamp // 3600)
        minutes = int((timestamp % 3600) // 60)
        seconds = round(float(timestamp % 60), 2)
        return f"{hours:02d}:{minutes:02d}:{seconds:.1f}"

    def _format_timestamp(self, timestamp: Any) -> str:
        """Format a timestamp to YYYY:MM:DD HH:MM:SS."""
        if isinstance(timestamp, (int, float)):
            dt = datetime.fromtimestamp(timestamp, timezone.utc)
            if dt.year < 2000:
                dt = datetime.now(timezone.utc)
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
                    try:
                        if int(parts[0]) < 2000:
                            return datetime.now(timezone.utc).strftime("%Y:%m:%d %H:%M:%S")
                    except ValueError:
                        pass
                    return f"{parts[0]}:{parts[1]}:{parts[2]} {'-'.join(parts[3:])}"
        except Exception:
            pass

        return timestamp_clean

    def _get_current_timestamp_str(
        self,
        stream_info: Optional[Dict[str, Any]],
        precision: bool = False,
        frame_id: Optional[str] = None,
    ) -> str:
        if not stream_info:
            return "00:00:00.00"
        input_settings = stream_info.get("input_settings", {}) or {}
        start_frame = input_settings.get("start_frame", "na")

        if precision:
            if start_frame != "na":
                if frame_id:
                    start_time = int(frame_id) / input_settings.get("original_fps", 30)
                else:
                    start_time = input_settings.get("start_frame", 30) / input_settings.get("original_fps", 30)
                self._debug_stream_timing("stream_time_str", self._format_timestamp_for_video(start_time))
                return self._format_timestamp(input_settings.get("stream_time", "NA"))
            return datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")

        if start_frame != "na":
            if frame_id:
                start_time = int(frame_id) / input_settings.get("original_fps", 30)
            else:
                start_time = input_settings.get("start_frame", 30) / input_settings.get("original_fps", 30)
            self._debug_stream_timing("stream_time_str", self._format_timestamp_for_video(start_time))
            return self._format_timestamp(input_settings.get("stream_time", "NA"))

        stream_time_str = input_settings.get("stream_info", {}).get("stream_time", "")
        if stream_time_str:
            try:
                dt = datetime.strptime(stream_time_str.replace(" UTC", ""), "%Y-%m-%d-%H:%M:%S.%f")
                ts = dt.replace(tzinfo=timezone.utc).timestamp()
                return self._format_timestamp_for_stream(ts)
            except Exception:
                return self._format_timestamp_for_stream(time.time())
        return self._format_timestamp_for_stream(time.time())

    def _get_start_timestamp_str(self, stream_info: Optional[Dict[str, Any]], precision: bool = False) -> str:
        if not stream_info:
            return "00:00:00"
        input_settings = stream_info.get("input_settings", {}) or {}

        def _candidate_from_stream_time(now_fallback: bool = True) -> str:
            candidate = input_settings.get("stream_time")
            if not candidate or candidate == "NA":
                nested = input_settings.get("stream_info", {}).get("stream_time", "")
                if nested:
                    try:
                        dt = datetime.strptime(nested.replace(" UTC", ""), "%Y-%m-%d-%H:%M:%S.%f")
                        self._tracking_start_time = dt.replace(tzinfo=timezone.utc).timestamp()
                        candidate = datetime.fromtimestamp(self._tracking_start_time, timezone.utc).strftime(
                            "%Y-%m-%d-%H:%M:%S.%f UTC"
                        )
                    except Exception:
                        candidate = (
                            datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC") if now_fallback else None
                        )
                else:
                    candidate = (
                        datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC") if now_fallback else None
                    )
            return candidate

        if precision:
            if self.start_timer is None:
                candidate = input_settings.get("stream_time")
                if not candidate or candidate == "NA":
                    candidate = datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")
                self.start_timer = candidate
                return self._format_timestamp(self.start_timer)
            if input_settings.get("start_frame", "na") == 1:
                candidate = input_settings.get("stream_time")
                if not candidate or candidate == "NA":
                    candidate = datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")
                self.start_timer = candidate
                return self._format_timestamp(self.start_timer)
            return self._format_timestamp(self.start_timer)

        if self.start_timer is None:
            self.start_timer = _candidate_from_stream_time()
            return self._format_timestamp(self.start_timer)

        if input_settings.get("start_frame", "na") == 1:
            candidate = input_settings.get("stream_time")
            if not candidate or candidate == "NA":
                nested = input_settings.get("stream_info", {}).get("stream_time", "")
                if nested:
                    try:
                        dt = datetime.strptime(nested.replace(" UTC", ""), "%Y-%m-%d-%H:%M:%S.%f")
                        ts = dt.replace(tzinfo=timezone.utc).timestamp()
                        candidate = datetime.fromtimestamp(ts, timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")
                    except Exception:
                        candidate = datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")
                else:
                    candidate = datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")
            self.start_timer = candidate
            return self._format_timestamp(self.start_timer)

        if self.start_timer is not None and self.start_timer != "NA":
            return self._format_timestamp(self.start_timer)

        if self._tracking_start_time is None:
            nested = input_settings.get("stream_info", {}).get("stream_time", "")
            if nested:
                try:
                    dt = datetime.strptime(nested.replace(" UTC", ""), "%Y-%m-%d-%H:%M:%S.%f")
                    self._tracking_start_time = dt.replace(tzinfo=timezone.utc).timestamp()
                except Exception:
                    self._tracking_start_time = time.time()
            else:
                self._tracking_start_time = time.time()

        dt = datetime.fromtimestamp(self._tracking_start_time, tz=timezone.utc)
        if dt.year < 2000:
            dt = datetime.now(timezone.utc)
        dt = dt.replace(minute=0, second=0, microsecond=0)
        return dt.strftime("%Y:%m:%d %H:%M:%S")

    def get_duration_seconds(self, start_time, end_time):
        def parse_relative_time(t):
            try:
                parts = t.strip().split(":")
                if len(parts) != 3:
                    return None
                return timedelta(hours=int(parts[0]), minutes=int(parts[1]), seconds=float(parts[2]))
            except Exception:
                return None

        def parse_time(t):
            if re.match(r"^\d{1,2}:\d{2}:\d{1,2}(\.\d+)?$", t):
                return parse_relative_time(t)
            if "UTC" in t:
                try:
                    return datetime.strptime(t, "%Y-%m-%d-%H:%M:%S.%f UTC")
                except ValueError:
                    return None
            return None

        start_dt = parse_time(start_time)
        end_dt = parse_time(end_time)

        if start_dt is None or end_dt is None:
            return "N/A"
        if isinstance(start_dt, timedelta) and isinstance(end_dt, timedelta):
            return (end_dt - start_dt).total_seconds()
        if isinstance(start_dt, datetime) and isinstance(end_dt, datetime):
            return (end_dt - start_dt).total_seconds()
        return None
