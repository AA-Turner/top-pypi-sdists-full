"""
Area Utilization (People Counting + Utilization Analytics) post-processing usecase.

This file is a "modified clone" of people_counting.py with area_utilization logic layered on top.

Key behavior:
- Counts people (like PeopleCountingUseCase)
- Computes zone-wise capacity utilization (like area_utilization.py)
- Zone geometry from the Matrice UI (same path as ``overcrowding_detection``):
  when ``stream_info`` and API credentials (or ``set_config_client``) are available,
  zone polygons can be resolved from the post-processing config API into pixel
  coordinates; otherwise ``zone_config`` from the deployment payload is used.
- Policy-correct zones:
    - If user provides zones -> compute zone-wise metrics
    - If user does NOT provide zones -> treat full camera frame as ONE zone named "global"
- Primary metric:
    occupancy_percent = (people_count / capacity) * 100
- Rolling window (seconds) metrics:
    time_occupied_percent = % of frames in window with count>0
    avg_occupancy_percent = avg(count) / capacity * 100
- Membership rule:
    - Configurable via ``use_center_membership``: bbox CENTER point (default)
      or bbox BOTTOM-CENTER ("feet") point for zone membership

Output schema: Matrice Analytics agg_summary (frame-wise), built via
``BaseProcessor.create_frame_wise_agg_summary`` (same as overcrowding_detection):
- incidents: list of incident dicts per frame
- tracking_stats: list of tracking-stat dicts per frame
- business_analytics: list (utilization metrics in ``statistics``)
- alerts: per-zone over-capacity alerts. Single source of truth is
  ``zone_config.zone_params[<zone>]["capacity"]`` — the same capacity drives the
  utilization math and the alert (a zone alerts when its in-zone count exceeds
  its capacity). There is no separate count/occupancy threshold knob.
- human_text
"""

from __future__ import annotations

import os
import threading
import time
from dataclasses import dataclass, field, replace
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

# Seconds between background retries when API zone fetch fails (parity with overcrowding_detection).
_GEOMETRY_RETRY_INTERVAL_SEC = 30

from ..core.base import (
    BaseProcessor,
    ConfigProtocol,
    ProcessingContext,
    ProcessingResult,
)
from ..core.config import AlertConfig, BaseConfig, ZoneConfig
from ..Trackers import ConfigDrivenTracker, TrackerProfile, legacy_sort_tracker_overrides
from ..utils import (
    ByteTrackWrapper,
    SORTTracker,
    apply_category_mapping,
    filter_by_confidence,
    match_results_structure,
    point_in_polygon,
)

# from ..utils.geometry_utils import point_in_polygon


TARGET_CATEGORY = "person"

WARN_NO_ZONES = "no_zones_configured_full_frame_used"
WARN_ZONE_TOO_BIG = "zone_exceeds_stream_resolution"
WARN_MISSING_STREAM_RESOLUTION = "missing_stream_resolution"

DEFAULT_CAPACITY = 10
DEFAULT_WINDOW_SECONDS = 300  # 5 minutes

# ---------------------------------------------------------------------------
# Over-capacity incident / alert policy (single source of truth = zone capacity)
# ---------------------------------------------------------------------------
# A zone is "over capacity" when its occupancy reaches 100% (count >= capacity).
# Severity escalates to critical at 120%.
OCCUPANCY_ENTER_PERCENT = 100.0     # raise incident + alert at/above this occupancy
OCCUPANCY_CRITICAL_PERCENT = 120.0  # severity -> "critical" at/above this occupancy
# Anti-flicker hysteresis: once an episode is active it only clears after occupancy
# stays *below* OCCUPANCY_EXIT_PERCENT for OCCUPANCY_EXIT_FRAMES consecutive frames.
OCCUPANCY_EXIT_PERCENT = 90.0
OCCUPANCY_EXIT_FRAMES = 5

SEVERITY_HIGH = "high"
SEVERITY_CRITICAL = "critical"


def _severity_for_occupancy(occupancy_percent: float) -> str:
    """Map an occupancy percentage to an over-capacity severity level.

    Only meaningful at/above 100% (where an episode exists): >=120% -> critical,
    otherwise high.
    """
    return SEVERITY_CRITICAL if occupancy_percent >= OCCUPANCY_CRITICAL_PERCENT else SEVERITY_HIGH


def _as_dict(value: Any) -> Dict[str, Any]:
    """Return value only when it is a dict; otherwise empty dict."""
    return value if isinstance(value, dict) else {}


def _bbox_center(bbox: Any) -> Tuple[float, float]:
    """
    bbox formats supported:
    - dict xmin,ymin,xmax,ymax
    - dict x1,y1,x2,y2
    - list [x1,y1,x2,y2]
    """
    if not bbox:
        return (0.0, 0.0)

    if isinstance(bbox, (list, tuple)) and len(bbox) >= 4:
        x1, y1, x2, y2 = bbox[0], bbox[1], bbox[2], bbox[3]
        return ((float(x1) + float(x2)) / 2.0, (float(y1) + float(y2)) / 2.0)

    if isinstance(bbox, dict):
        if "xmin" in bbox:
            return (
                (float(bbox.get("xmin", 0)) + float(bbox.get("xmax", 0))) / 2.0,
                (float(bbox.get("ymin", 0)) + float(bbox.get("ymax", 0))) / 2.0,
            )
        if "x1" in bbox:
            return (
                (float(bbox.get("x1", 0)) + float(bbox.get("x2", 0))) / 2.0,
                (float(bbox.get("y1", 0)) + float(bbox.get("y2", 0))) / 2.0,
            )

    return (0.0, 0.0)


def _bbox_bottom_center(bbox: Any) -> Tuple[float, float]:
    """
    Bottom-center ("feet") point of a bbox: horizontal midpoint, bottom edge.

    Image coordinates increase downward, so the bottom edge is the larger y
    (ymax / y2). This represents where a person stands on the ground plane and is
    generally more accurate than the geometric center for ground-region zone
    membership on angled/elevated cameras.

    bbox formats supported (same as ``_bbox_center``):
    - dict xmin,ymin,xmax,ymax
    - dict x1,y1,x2,y2
    - list [x1,y1,x2,y2]
    """
    if not bbox:
        return (0.0, 0.0)

    if isinstance(bbox, (list, tuple)) and len(bbox) >= 4:
        x1, y1, x2, y2 = bbox[0], bbox[1], bbox[2], bbox[3]
        return ((float(x1) + float(x2)) / 2.0, max(float(y1), float(y2)))

    if isinstance(bbox, dict):
        if "xmin" in bbox:
            return (
                (float(bbox.get("xmin", 0)) + float(bbox.get("xmax", 0))) / 2.0,
                max(float(bbox.get("ymin", 0)), float(bbox.get("ymax", 0))),
            )
        if "x1" in bbox:
            return (
                (float(bbox.get("x1", 0)) + float(bbox.get("x2", 0))) / 2.0,
                max(float(bbox.get("y1", 0)), float(bbox.get("y2", 0))),
            )

    return (0.0, 0.0)


def _normalize_detection_bbox(det: Dict[str, Any]) -> Dict[str, Any]:
    """
    Ensure bbox exists under det['bounding_box'] if only det['bbox'] exists.
    """
    if not isinstance(det, dict):
        return {}
    d = det.copy()
    if "bounding_box" not in d and "bbox" in d:
        d["bounding_box"] = d["bbox"]
    return d


def _zone_exceeds_stream_resolution(zone_poly: List[List[float]], stream_res: Dict[str, Any]) -> bool:
    w = stream_res.get("width", 0) or 0
    h = stream_res.get("height", 0) or 0
    if not w or not h:
        return False

    for p in zone_poly:
        if len(p) >= 2 and (p[0] > w or p[1] > h):
            return True
    return False


def _occupancy_state(percent: float) -> str:
    """
    State buckets policy:
    - vacant: 0
    - low: (0, 30]
    - moderate: (30, 70]
    - near_capacity: (70, 100) -- approaching capacity, no incident/alert yet
    - high: [100, 120) -- matches OCCUPANCY_ENTER_PERCENT, incident-active range
    - critical: >=120 -- matches OCCUPANCY_CRITICAL_PERCENT

    Aligned with the over-capacity incident/alert policy above so this displayed
    state can never read "high"/"critical" without an incident actually being
    open (previously "high" covered (70, 100], which sat entirely below
    OCCUPANCY_ENTER_PERCENT=100 and so never corresponded to a real incident).
    """
    if percent <= 0:
        return "vacant"
    if percent <= 30:
        return "low"
    if percent <= 70:
        return "moderate"
    if percent < OCCUPANCY_ENTER_PERCENT:
        return "near_capacity"
    if percent < OCCUPANCY_CRITICAL_PERCENT:
        return "high"
    return "critical"


# ----------------------------
# Config
# ----------------------------
@dataclass
class AreaUtilizationConfig(BaseConfig):
    """
    Configuration for area utilization use case.

    This config intentionally mirrors PeopleCountingConfig so that:
    - client payloads stay consistent
    - PostProcessor/config_manager behavior remains predictable
    - we can safely clone people_counting.py behavior

    Per-zone capacity is the single source of truth and lives inside the zone
    geometry payload::

      zone_config.zone_params = {"meeting_room": {"capacity": 6}, ...}

    That capacity drives BOTH the utilization math (``occupancy_percent``) AND the
    alerting: a zone alerts when its in-zone people count exceeds its capacity.
    ``extra_params.zone_capacities`` is still read as a legacy fallback, and
    ``window_seconds`` (rolling-window length) still lives in ``extra_params``.
    """

    # -----------------------------
    # Smoothing configuration (kept for parity)
    # -----------------------------
    enable_smoothing: bool = True
    smoothing_algorithm: str = "observability"  # "window" or "observability"
    smoothing_window_size: int = 20
    smoothing_cooldown_frames: int = 5
    smoothing_confidence_range_factor: float = 0.5

    # -----------------------------
    # Tracking (assigns stable cross-frame track_ids)
    # -----------------------------
    # Primary tracker (same pattern as loitering_detection): a lightweight
    # SORT / ByteTrack tracker that stamps a persistent integer ``track_id`` on
    # each detection so per-zone unique counts and track-id lists can be built.
    enable_tracking: bool = True
    tracking_method: str = "sort"  # "sort" (Kalman + Hungarian) or "bytetrack"
    tracking_max_age: int = 30
    tracking_min_hits: int = 2
    tracking_iou_threshold: float = 0.25

    # -----------------------------
    # PERFORMANCE: Legacy tracker selection (fallbacks when enable_tracking=False)
    # -----------------------------
    enable_advanced_tracker: bool = False  # Heavy O(n³) tracker - enable only when tracking quality is critical
    enable_simple_tracker: bool = False  # Lightweight O(n) tracker - fast but no cross-frame persistence

    # -----------------------------
    # Zone configuration
    # -----------------------------
    zone_config: Optional[ZoneConfig] = None

    # Per-zone parameters (name -> {param: value}), e.g. {"road": {"capacity": 30}}.
    # In the UI/API/JSON payload these live *inside* ``zone_config`` (sibling of
    # ``zones``); ``__post_init__`` lifts them out to this field so the shared
    # ``ZoneConfig`` in core/config.py does not need to know about them. ``capacity``
    # here is the single source of truth for the utilization math AND the alerts.
    zone_params: Dict[str, Dict[str, Any]] = field(default_factory=dict)

    # -----------------------------
    # Counting parameters
    # -----------------------------
    enable_unique_counting: bool = True
    time_window_minutes: int = 60  # kept for parity (even if window_seconds is used for utilization)

    # -----------------------------
    # Category mapping
    # -----------------------------
    person_categories: List[str] = field(default_factory=lambda: ["person", "people"])
    index_to_category: Optional[Dict[int, str]] = None

    # -----------------------------
    # Alerts
    # -----------------------------
    alert_config: Optional[AlertConfig] = None

    # Keep same broad target list (even if we filter down to person internally)
    target_categories: List[str] = field(
        default_factory=lambda: [
            "person",
            "people",
            "human",
            "man",
            "woman",
            "male",
            "female",
        ]
    )

    # -----------------------------
    # Utilization-specific behavior
    # -----------------------------
    # Zone membership point: True -> bbox geometric center; False -> bbox
    # bottom-center ("feet"), which better reflects ground-plane standing position.
    use_center_membership: bool = True

    def __post_init__(self) -> None:
        """Accept ``zone_config`` as a plain dict (UI/API/JSON payload shape).

        The Matrice UI and the post-processing JSON configs emit ``zone_config``
        as a dict with ``zones`` (pixel polygons) and ``zone_params`` (per-zone
        capacity, etc.) nested inside it, plus an unused ``lines`` key. Lift
        ``zones`` into a proper :class:`ZoneConfig` (which intentionally has no
        knowledge of ``zone_params``) and hoist ``zone_params`` onto this config's
        own ``zone_params`` field, so behavior is identical whether the config was
        built in Python or loaded from JSON — without touching core/config.py.
        """
        zc = self.zone_config
        if isinstance(zc, dict):
            # Hoist nested zone_params (unless explicitly provided on the config).
            if not self.zone_params:
                nested = zc.get("zone_params", {})
                if isinstance(nested, dict):
                    self.zone_params = {
                        str(zn): dict(zp) for zn, zp in nested.items() if isinstance(zp, dict)
                    }
            self.zone_config = ZoneConfig(
                zones=zc.get("zones", {}) or {},
                zone_confidence_thresholds=zc.get("zone_confidence_thresholds", {}) or {},
                zone_categories=zc.get("zone_categories", {}) or {},
            )

    def validate(self) -> List[str]:
        """Validate area utilization configuration (PeopleCountingConfig-compatible)."""
        errors = super().validate()

        if self.time_window_minutes <= 0:
            errors.append("time_window_minutes must be positive")

        if not self.person_categories:
            errors.append("person_categories cannot be empty")

        # Validate nested configs
        if self.zone_config:
            errors.extend(self.zone_config.validate())

        if self.alert_config:
            errors.extend(self.alert_config.validate())

        return errors


# ----------------------------
# UseCase
# ----------------------------
class AreaUtilizationUseCase(BaseProcessor):
    """
    Area Utilization = People Counting + Capacity Analytics.

    Keeps PeopleCounting behavior:
    - incidents
    - tracking_stats
    - alerts (per-zone over-capacity, threshold = zone_params capacity)
    - human_text summary

    Adds:
    - business_analytics (list per frame) with zone-wise utilization metrics
    """

    def __init__(self):
        super().__init__("area_utilization")
        self.category = "general"
        self.CASE_TYPE: Optional[str] = "area_utilization"
        self.CASE_VERSION: Optional[str] = "1.0"

        # Keep people-only focus (like people_counting)
        self.target_categories = ["person"]

        # tracker state (same pattern)
        self.tracker = None
        self._total_frame_counter = 0
        self._tracking_start_time = None

        # alert trend state
        self._ascending_alert_list: List[int] = []
        self.start_timer = None
        # Incident lifecycle: a single, *persistent* over-capacity incident.
        # While ≥1 zone is over capacity the same incident (stable id + start_time)
        # is re-emitted each frame with end_time=""; a closing snapshot (with a real
        # end_time) is emitted on the frame the over-capacity condition clears.
        self._au_incident_active: bool = False
        self._au_last_incident: Optional[Dict[str, Any]] = None
        self._au_incident_id: Optional[str] = None
        self._au_incident_start_time: Optional[str] = None

        # Per-zone over-capacity state machine (drives both alerts and the
        # incident). Per zone: {"active": bool, "below_frames": int, "alerted": bool}
        #   active       -> currently inside an over-capacity episode (with hysteresis)
        #   below_frames -> consecutive frames under OCCUPANCY_EXIT_PERCENT while active
        #   alerted      -> the one-shot alert for this episode has been emitted
        self._zone_oc_state: Dict[str, Dict[str, Any]] = {}

        # persistent rolling history per zone: [(timestamp, count), ...]
        self._history: Dict[str, List[Tuple[float, int]]] = {}

        # pixel polygons of the zones used on the current frame, keyed by zone
        # name (``None`` for the synthetic full-frame "global" zone). Populated in
        # _compute_area_utilization and surfaced as "zone_coords" in zone_analysis.
        self._current_zone_polys: Dict[str, Any] = {}

        # per-zone track-id state (populated when tracking is enabled)
        #   _zone_current_track_ids: zone_name -> set of track_ids seen in the zone this frame
        #   _zone_total_track_ids:   zone_name -> set of all track_ids ever seen in the zone
        self._zone_current_track_ids: Dict[str, set] = {}
        self._zone_total_track_ids: Dict[str, set] = {}

        # Matrice UI zones via post-processing config API (same pattern as overcrowding_detection)
        self._config_client: Any = None  # PostProcessingConfigClient (lazy-imported)
        self._resolved_geometry_cache: Optional[AreaUtilizationConfig] = None
        self._geometry_thread: Optional[threading.Thread] = None
        self._zone_resolution_attempted = False
        self._last_zone_signature: Optional[Tuple[str, ...]] = None

    # ----------------------------
    # API geometry resolution (Matrice post-processing config → pixel zones)
    # ----------------------------

    def set_config_client(self, client: Any) -> None:
        """Set client used to resolve zones from deployment/camera post-processing config."""
        self._config_client = client

    @staticmethod
    def _zone_signature(cfg: AreaUtilizationConfig) -> Tuple[str, ...]:
        if cfg.zone_config and getattr(cfg.zone_config, "zones", None):
            return tuple(sorted(cfg.zone_config.zones.keys()))
        return ("global",)

    def _start_geometry_resolver(
        self,
        config: AreaUtilizationConfig,
        stream_info: Dict[str, Any],
    ) -> None:
        if self._geometry_thread is not None:
            return

        def _resolver() -> None:
            while True:
                try:
                    result = self._resolve_geometry_from_api(config, stream_info)
                    if result is not None:
                        self._resolved_geometry_cache = result
                        self.logger.info(
                            "AreaUtilization: zone geometry resolved from API "
                            "(background thread)"
                        )
                        return
                    self.logger.info(
                        "AreaUtilization: API geometry returned None, retrying in %ds",
                        _GEOMETRY_RETRY_INTERVAL_SEC,
                    )
                except Exception as exc:
                    self.logger.warning(
                        "AreaUtilization: background geometry resolve error: %s",
                        exc,
                    )
                time.sleep(_GEOMETRY_RETRY_INTERVAL_SEC)

        t = threading.Thread(
            target=_resolver,
            daemon=True,
            name="area-utilization-zone-geometry-resolver",
        )
        self._geometry_thread = t
        t.start()
        self.logger.info(
            "AreaUtilization: started background zone geometry resolver thread"
        )

    def _resolve_geometry_from_api(
        self,
        config: AreaUtilizationConfig,
        stream_info: Optional[Dict[str, Any]],
    ) -> Optional[AreaUtilizationConfig]:
        """Resolve ``zone_config`` from PostProcessingConfigClient (UI zones → pixel coords)."""
        from .overcrowding_detection import (
            PostProcessingConfigClient,
            lift_ai_camera_zones_into_post_processing,
        )

        client = self._config_client or (
            stream_info.get("config_client") if stream_info else None
        )
        if not client and stream_info:
            try:
                client = PostProcessingConfigClient(logger=self.logger)
                if getattr(client, "_session", None) is None:
                    self.logger.info(
                        "AreaUtilization: _resolve_geometry_from_api skipped "
                        "(no config_client; set MATRICE_ACCESS_KEY_ID, "
                        "MATRICE_SECRET_ACCESS_KEY, MATRICE_ACCOUNT_NUMBER "
                        "or call set_config_client() for API zone resolution)"
                    )
                    return None
                self._config_client = client
            except Exception as e:
                self.logger.warning(
                    "AreaUtilization: could not create config client from env: %s",
                    e,
                )
                return None

        if not stream_info:
            self.logger.info(
                "AreaUtilization: _resolve_geometry_from_api skipped (no stream_info)"
            )
            return None
        if not client:
            self.logger.info(
                "AreaUtilization: _resolve_geometry_from_api skipped (no config_client)"
            )
            return None

        ids = client.get_stream_identifiers(stream_info)
        app_deployment_id = ids.get("app_deployment_id") or ""
        camera_id = ids.get("camera_id") or ""
        self.logger.info(
            "AreaUtilization: _resolve_geometry_from_api app_deployment_id=%s camera_id=%s",
            app_deployment_id or "(empty)",
            camera_id or "(empty)",
        )

        if not app_deployment_id or not camera_id:
            self.logger.info(
                "_resolve_geometry_from_api: returning None (missing app_deployment_id or camera_id)"
            )
            return None

        configs, err, _ = client.get_post_processing_configs_by_app_deployment(
            app_deployment_id
        )
        if err or not configs:
            self.logger.info(
                "_resolve_geometry_from_api: returning None "
                "(get_post_processing_configs_by_app_deployment: err=%r, configs count=%s)",
                err,
                len(configs) if configs else 0,
            )
            return None

        filtered = client.filter_configs_by_camera_id(configs, camera_id)
        if not filtered:
            self.logger.info(
                "_resolve_geometry_from_api: returning None "
                "(filter_configs_by_camera_id: no config for camera_id=%s)",
                camera_id,
            )
            return None

        doc = filtered[0]
        doc = lift_ai_camera_zones_into_post_processing(doc)
        width, height = client.get_resolution(camera_id)
        if width is None or height is None:
            self.logger.info(
                "_resolve_geometry_from_api: returning None "
                "(get_resolution: width=%r, height=%r for camera_id=%s)",
                width,
                height,
                camera_id,
            )
            return None

        doc_px = client.denormalize_config(doc, width, height)
        post = doc_px.get("postProcessing") or {}
        cam_cfg = post.get(camera_id) or {}
        zone_config_raw = cam_cfg.get("zone_config") or {}
        zones_px = zone_config_raw.get("zones") or {}

        if not isinstance(zones_px, dict) or not zones_px:
            self.logger.info(
                "_resolve_geometry_from_api: returning None "
                "(no zones found in zone_config for camera_id=%s)",
                camera_id,
            )
            return None

        zones_dict: Dict[str, List[List[float]]] = {}
        for name, points in zones_px.items():
            if not isinstance(points, list) or len(points) < 3:
                self.logger.warning(
                    "AreaUtilization: skipping zone %r (need list of >= 3 points)",
                    name,
                )
                continue
            row: List[List[float]] = []
            for pt in points:
                if isinstance(pt, (list, tuple)) and len(pt) >= 2:
                    row.append([float(pt[0]), float(pt[1])])
                else:
                    row = []
                    break
            if len(row) >= 3:
                zones_dict[str(name)] = row
            else:
                self.logger.warning(
                    "AreaUtilization: skipping zone %r (invalid point list)", name
                )

        # Per-zone params (capacity, etc.) live as a sibling of "zones" inside
        # "zone_config" — same shape as dwell_detection. Reading it here keeps
        # capacity travelling with the geometry resolved from the UI/API. We keep
        # zone_params on the AreaUtilizationConfig (not on ZoneConfig) so the shared
        # core/config.py ZoneConfig stays untouched.
        zone_params_raw = zone_config_raw.get("zone_params") or {}
        zone_params_dict: Dict[str, Dict[str, Any]] = {
            str(zn): dict(zp)
            for zn, zp in zone_params_raw.items()
            if isinstance(zp, dict)
        }
        new_zone_config = ZoneConfig(zones=zones_dict)

        self.logger.info(
            "AreaUtilization: resolved %d zone(s) from API: %s (zone_params: %s)",
            len(zones_dict),
            list(zones_dict.keys()),
            list(zone_params_dict.keys()),
        )
        return replace(
            config,
            zone_config=new_zone_config,
            zone_params=zone_params_dict or config.zone_params,
        )

    # ----------------------------
    # Tracking helpers (same pattern as loitering_detection)
    # ----------------------------
    @staticmethod
    def _parse_track_id(tid: Any) -> Optional[int]:
        """Return int track_id, or None if missing / not coercible (skip, no crash)."""
        if tid is None:
            return None
        try:
            return int(tid)
        except (TypeError, ValueError):
            return None

    def _init_tracker(self, config: AreaUtilizationConfig, stream_info: Optional[Dict[str, Any]]) -> None:
        """
        Initialize an internal tracker if ``enable_tracking`` is set.

        Supported (same as loitering_detection):
          - SORTTracker (Kalman + Hungarian)
          - ByteTrackWrapper (YOLOX BYTETracker wrapper)

        The tracker stamps a persistent integer ``track_id`` on each detection so
        downstream per-zone unique counts and track-id lists can be built.
        """
        if self.tracker is not None:
            return

        method = str(getattr(config, "tracking_method", "sort")).lower().strip()

        # F10b S9 (consolidation-plan.md Step 9): route the legacy SORT/ByteTrack
        # default onto the AdvancedTracker seam. MATRICE_LEGACY_SORT=1 keeps the
        # pre-migration path alive for one release (kill-switch, plan §7).
        if method in ("sort", "bytetrack") and os.environ.get("MATRICE_LEGACY_SORT") != "1":
            self.tracker = ConfigDrivenTracker().get_shared_tracker(
                profile=TrackerProfile.DEFAULT,
                **legacy_sort_tracker_overrides(config, method),
            )
            self.logger.info("AreaUtilization: initialized AdvancedTracker (seam) for legacy %s method", method)
            return

        if method == "sort":
            self.tracker = SORTTracker(
                iou_threshold=float(getattr(config, "tracking_iou_threshold", 0.25)),
                max_age=int(getattr(config, "tracking_max_age", 30)),
                min_hits=int(getattr(config, "tracking_min_hits", 2)),
            )
            self.logger.info("AreaUtilization: initialized SORTTracker")
            return

        if method == "bytetrack":
            fps = 30.0
            try:
                if stream_info:
                    fps_val = stream_info.get("input_settings", {}).get("original_fps")
                    if fps_val and float(fps_val) > 1e-6:
                        fps = float(fps_val)
            except Exception:
                fps = 30.0

            self.tracker = ByteTrackWrapper(
                fps=float(fps),
                track_thresh=float(getattr(config, "bytetrack_track_thresh", 0.25)),
                match_thresh=float(getattr(config, "bytetrack_match_thresh", 0.80)),
                track_buffer=int(getattr(config, "tracking_max_age", 30)),
            )
            self.logger.info("AreaUtilization: initialized ByteTrackWrapper (fps=%s)", fps)
            return

        # Unknown method => no tracking
        self.tracker = None

    # ----------------------------
    # Lightweight tracker option (same as people_counting)
    # ----------------------------
    def _simple_tracker_update(self, detections: list) -> list:
        """
        PERFORMANCE: Lightweight tracker alternative
        Simple tracker using frame-local indexing (O(n)).
        Does not persist track IDs across frames.
        Enable via config.enable_simple_tracker = True
        """
        for i, det in enumerate(detections):
            if not isinstance(det, dict):
                continue
            if det.get("track_id") is None:
                det["track_id"] = f"simple_{self._total_frame_counter}_{i}"
        return detections

    # ----------------------------
    # Main process
    # ----------------------------
    def process(
        self,
        data: Any,
        config: ConfigProtocol,
        context: Optional[ProcessingContext] = None,
        stream_info: Optional[Dict[str, Any]] = None,
    ) -> ProcessingResult:
        processing_start = time.time()

        if not isinstance(config, AreaUtilizationConfig):
            return self.create_error_result(
                "Invalid config type",
                usecase=self.name,
                category=self.category,
                context=context,
            )

        if context is None:
            context = ProcessingContext()

        # Validate config
        errors = config.validate()
        if errors:
            context.mark_completed()
            return self.create_error_result(
                "Invalid configuration",
                usecase=self.name,
                category=self.category,
                context=context,
            )

        if not self._zone_resolution_attempted:
            self._zone_resolution_attempted = True
            if stream_info:
                self.logger.info(
                    "AreaUtilization: attempting zone geometry resolution from API "
                    "(first frame, blocking)"
                )
                try:
                    resolved = self._resolve_geometry_from_api(config, stream_info)
                    if resolved is not None:
                        self._resolved_geometry_cache = resolved
                        self.logger.info(
                            "AreaUtilization: zone geometry resolved from API and cached"
                        )
                    else:
                        self.logger.warning(
                            "AreaUtilization: API returned no zone config on first "
                            "attempt; starting background retry thread (every %ds). "
                            "Using zone_config from user config until resolved.",
                            _GEOMETRY_RETRY_INTERVAL_SEC,
                        )
                        self._start_geometry_resolver(config, stream_info)
                except Exception as exc:
                    self.logger.warning(
                        "AreaUtilization: zone geometry resolution raised on first "
                        "attempt (%s); starting background retry thread (every %ds). "
                        "Using zone_config from user config until resolved.",
                        exc,
                        _GEOMETRY_RETRY_INTERVAL_SEC,
                    )
                    self._start_geometry_resolver(config, stream_info)
            else:
                self.logger.info(
                    "AreaUtilization: no stream_info on first frame; "
                    "using zone_config from user config"
                )

        effective_config = config
        if self._resolved_geometry_cache is not None:
            effective_config = self._resolved_geometry_cache
            self.logger.debug("AreaUtilization: using API-resolved zone geometry")

        sig = self._zone_signature(effective_config)
        if self._last_zone_signature is not None and sig != self._last_zone_signature:
            self._history.clear()
            self._zone_current_track_ids.clear()
            self._zone_total_track_ids.clear()
            # Zone set changed -> over-capacity state no longer applies; reset the
            # state machine and any active incident so we don't carry stale episodes.
            self._zone_oc_state.clear()
            self._au_incident_active = False
            self._au_last_incident = None
            self._au_incident_id = None
            self._au_incident_start_time = None
        self._last_zone_signature = sig

        # Detect input format (for metadata parity)
        input_format = match_results_structure(data)
        context.input_format = input_format
        context.confidence_threshold = effective_config.confidence_threshold

        # Confidence filtering
        if effective_config.confidence_threshold is not None:
            processed_data = filter_by_confidence(
                data, effective_config.confidence_threshold
            )
        else:
            processed_data = data

        # Category mapping
        if effective_config.index_to_category:
            processed_data = apply_category_mapping(
                processed_data, effective_config.index_to_category
            )

        # Category filtering (people-only)
        target_cats = effective_config.target_categories or self.target_categories
        processed_data = self._filter_target_categories(processed_data, target_cats)

        # Normalize bbox field names
        processed_data = (
            [_normalize_detection_bbox(d) for d in processed_data if isinstance(d, dict)]
            if isinstance(processed_data, list)
            else []
        )

        # Tracking: assign stable cross-frame track_ids (same pattern as loitering_detection).
        # Primary path is SORT / ByteTrack via enable_tracking; the advanced/simple
        # trackers remain as explicit fallbacks for backward compatibility.
        if getattr(effective_config, "enable_tracking", True):
            self._init_tracker(effective_config, stream_info)
            if self.tracker is not None:
                try:
                    if isinstance(self.tracker, ByteTrackWrapper):
                        processed_data = self.tracker.update(processed_data, stream_info=stream_info)
                    else:
                        processed_data = self.tracker.update(processed_data)
                except Exception as e:
                    self.logger.warning(f"AreaUtilization tracker update failed: {e}")
        elif getattr(effective_config, "enable_advanced_tracker", False):
            try:
                if self.tracker is None:
                    # F10b S6/S7 gap closure: LEGACY_40's own base kwargs (0.4/0.05/0.3/0.8)
                    # are this site's literal config -- no overrides needed. Already gated
                    # on enable_advanced_tracker by the enclosing elif, so no gate_attr here.
                    self.tracker = ConfigDrivenTracker().get_shared_tracker(profile=TrackerProfile.LEGACY_40)
                processed_data = self.tracker.update(processed_data)
            except Exception as e:
                self.logger.warning(f"AdvancedTracker failed: {e}")
        elif getattr(effective_config, "enable_simple_tracker", False):
            processed_data = self._simple_tracker_update(processed_data)

        # Update counting state
        self._update_tracking_state(processed_data)
        self._total_frame_counter += 1

        # Determine frame_number (keep people_counting behavior)
        frame_number = None
        if stream_info:
            input_settings = stream_info.get("input_settings", {})
            start_frame = input_settings.get("start_frame")
            end_frame = input_settings.get("end_frame")
            if start_frame is not None and end_frame is not None and start_frame == end_frame:
                frame_number = start_frame
        frame_key = str(frame_number) if frame_number is not None else "current_frame"

        # Build counting summary
        counting_summary = self._count_people(processed_data)
        total_counts = self.get_total_counts()
        counting_summary["total_counts"] = total_counts

        # Compute area utilization stats (zones + capacity + rolling window)
        warnings: List[str] = []
        zone_stats = self._compute_area_utilization(
            detections=processed_data,
            config=effective_config,
            context=context,
            stream_info=stream_info,
            warnings=warnings,
        )

        # Over-capacity evaluation: per-zone state machine that drives both the
        # one-shot alerts and the persistent incident. Single source of truth is
        # each zone's capacity (from zone_params) -> occupancy_percent.
        over_capacity = self._evaluate_over_capacity(zone_stats, frame_key, effective_config)
        alerts = over_capacity["alerts"]

        # Incidents / Tracking stats (kept same schema style)
        incidents_list = self._generate_incidents(
            over_capacity,
            zone_stats,
            effective_config,
            frame_number,
            stream_info,
        )
        tracking_stats_list = self._generate_tracking_stats(
            counting_summary,
            alerts,
            zone_stats,
            effective_config,
            frame_number,
            stream_info,
        )

        # Business analytics (new)
        business_analytics_list = self._generate_business_analytics(zone_stats, alerts, stream_info)

        # Summary (human_text)
        summary_list = self._generate_summary(
            incidents_list,
            tracking_stats_list,
            business_analytics_list,
        )

        human_text_str = summary_list[0] if summary_list else ""

        zone_analysis = self._build_zone_analysis(zone_stats)

        incidents_item     = incidents_list[0]          if incidents_list          else {}
        tracking_item      = tracking_stats_list[0]     if tracking_stats_list     else {}
        business_item      = business_analytics_list[0] if business_analytics_list else {}
        summary_str        = summary_list[0]            if summary_list            else ""

        agg_summary: Dict[str, Any] = {
            frame_key: {
                "incidents":          incidents_item,
                "tracking_stats":     tracking_item,
                "business_analytics": business_item,
                "alerts":             alerts,
                "human_text":         summary_str,
            }
        }
        if zone_analysis:
            agg_summary[frame_key]["zone_analysis"] = zone_analysis

        context.mark_completed()

        result = self.create_result(
            data={"agg_summary": agg_summary},
            usecase=self.name,
            category=self.category,
            context=context,
        )

        # Performance (was stdout in people_counting; use logger for library use)
        proc_time = time.time() - processing_start
        processing_latency_ms = proc_time * 1000.0
        processing_fps = (1.0 / proc_time) if proc_time > 0 else None
        self.logger.info(
            "area_utilization performance: latency_ms=%s throughput_fps=%s frame_counter=%s",
            processing_latency_ms,
            processing_fps,
            self._total_frame_counter,
        )
        if warnings:
            result.warnings = list(dict.fromkeys(warnings))
        return result

    # ----------------------------
    # Filtering helpers
    # ----------------------------
    def _filter_target_categories(self, data: Any, targets: List[str]) -> List[Dict[str, Any]]:
        if isinstance(data, list):
            return [d for d in data if isinstance(d, dict) and d.get("category") in targets]
        return []

    # ----------------------------
    # Utilization computation
    # ----------------------------
    def _compute_area_utilization(
        self,
        detections: List[Dict[str, Any]],
        config: AreaUtilizationConfig,
        context: ProcessingContext,
        stream_info: Optional[Dict[str, Any]],
        warnings: List[str],
    ) -> Dict[str, Any]:
        """
        Returns zone_stats dict:
        {
          zone_name: {
            "count": int,
            "capacity": int,
            "occupancy_percent": float,
            "state": str,
            "time_occupied_percent": float,
            "avg_occupancy_percent": float
          }
        }
        """
        # Determine zones
        zones: Dict[str, Any] = {}
        if config.zone_config and getattr(config.zone_config, "zones", None):
            zones = config.zone_config.zones
        else:
            zones = {"global": None}
            warnings.append(WARN_NO_ZONES)

        # Stream resolution (optional warnings)
        # area_utilization.py uses context.metadata["stream_info"]["stream_resolution"]
        # but people_counting uses stream_info arg. We'll support both.
        meta_stream_info = (context.metadata or {}).get("stream_info", {}) if context else {}
        si = stream_info or meta_stream_info or {}
        res = {}
        if isinstance(si, dict):
            stream_resolution = _as_dict(si.get("stream_resolution"))
            input_settings = _as_dict(si.get("input_settings"))
            res = stream_resolution or _as_dict(input_settings.get("stream_resolution"))
        frame_w = int(res.get("width", 0) or 0)
        frame_h = int(res.get("height", 0) or 0)
        if frame_w <= 0 or frame_h <= 0:
            warnings.append(WARN_MISSING_STREAM_RESOLUTION)

        # Zone scale warning
        if zones and "global" not in zones and frame_w > 0 and frame_h > 0:
            for _zname, poly in zones.items():
                if poly and _zone_exceeds_stream_resolution(poly, {"width": frame_w, "height": frame_h}):
                    warnings.append(WARN_ZONE_TOO_BIG)
                    break

        # Capacity source of truth is ``config.zone_params[zone]["capacity"]``
        # (hoisted from the nested zone_config payload in __post_init__).
        # ``extra_params.zone_capacities`` is still honored as a legacy fallback so
        # older configs keep working.
        zone_params = _as_dict(getattr(config, "zone_params", None))
        extra = _as_dict(config.extra_params)
        legacy_capacities = _as_dict(extra.get("zone_capacities"))
        window_seconds = int(extra.get("window_seconds", DEFAULT_WINDOW_SECONDS) or DEFAULT_WINDOW_SECONDS)

        # Remember the polygons used this frame so _build_zone_analysis can emit
        # them under "zone_coords".
        self._current_zone_polys = dict(zones)

        now_ts = time.time()

        zone_stats: Dict[str, Any] = {}
        for zone_name, poly in zones.items():
            # Determine in-zone detections
            if poly is None:
                in_zone = detections[:]
            else:
                in_zone = []
                if not poly or len(poly) < 3:
                    in_zone = []
                else:
                    poly_points = [(p[0], p[1]) for p in poly]
                    # Membership point: geometric center vs bottom-center ("feet").
                    # Bottom-center is the ground-plane standing position and is
                    # generally more accurate for ground-region zones on angled cameras.
                    point_fn = _bbox_center if getattr(config, "use_center_membership", True) else _bbox_bottom_center
                    for det in detections:
                        if not isinstance(det, dict):
                            continue
                        bbox = det.get("bounding_box") or det.get("bbox")
                        if not bbox:
                            continue
                        cx, cy = point_fn(bbox)
                        if point_in_polygon((cx, cy), poly_points):
                            in_zone.append(det)

            count = len(in_zone)

            # Collect track_ids for this zone (when tracking assigned them).
            current_ids: set = set()
            for det in in_zone:
                tid = self._parse_track_id(det.get("track_id"))
                if tid is not None and tid >= 0:
                    current_ids.add(tid)
            self._zone_current_track_ids[zone_name] = current_ids
            if zone_name not in self._zone_total_track_ids:
                self._zone_total_track_ids[zone_name] = set()
            self._zone_total_track_ids[zone_name].update(current_ids)

            capacity = self._resolve_zone_capacity(zone_name, zone_params, legacy_capacities)

            occ_percent = 0.0
            if capacity > 0:
                occ_percent = (count / capacity) * 100.0
            occ_percent = round(occ_percent, 3)
            state = _occupancy_state(occ_percent)

            # Update rolling history
            if zone_name not in self._history:
                self._history[zone_name] = []
            self._history[zone_name].append((now_ts, count))

            cutoff = now_ts - float(window_seconds)
            self._history[zone_name] = [(t, c) for (t, c) in self._history[zone_name] if t >= cutoff]

            # Time occupied percent (frame occupancy ratio)
            hist = self._history[zone_name]
            if hist:
                occupied_frames = sum(1 for (_, c) in hist if c > 0)
                time_occ_percent = (occupied_frames / len(hist)) * 100.0
                avg_occ = sum(c for (_, c) in hist) / len(hist)
                avg_occ_percent = (avg_occ / capacity) * 100.0 if capacity > 0 else 0.0
            else:
                time_occ_percent = 0.0
                avg_occ_percent = 0.0

            zone_stats[zone_name] = {
                "count": count,
                "capacity": capacity,
                "occupancy_percent": round(occ_percent, 3),
                "state": state,
                "time_occupied_percent": round(time_occ_percent, 3),
                "avg_occupancy_percent": round(avg_occ_percent, 3),
            }

        return zone_stats

    @staticmethod
    def _resolve_zone_capacity(
        zone_name: str,
        zone_params: Dict[str, Any],
        legacy_capacities: Dict[str, Any],
    ) -> int:
        """Resolve a zone's capacity.

        Lookup order:
        1. ``zone_config.zone_params[zone_name]["capacity"]`` — primary source.
        2. ``extra_params.zone_capacities[zone_name]`` (or ``"global"``) — legacy
           fallback so pre-existing configs keep working.
        3. ``DEFAULT_CAPACITY``.
        """
        def _coerce_pos_int(value: Any) -> Optional[int]:
            try:
                ivalue = int(value)
            except (TypeError, ValueError):
                return None
            return ivalue if ivalue > 0 else None

        params = zone_params.get(zone_name)
        if isinstance(params, dict) and "capacity" in params:
            cap = _coerce_pos_int(params.get("capacity"))
            if cap is not None:
                return cap

        legacy = legacy_capacities.get(zone_name, legacy_capacities.get("global"))
        cap = _coerce_pos_int(legacy)
        if cap is not None:
            return cap

        return DEFAULT_CAPACITY

    def _zone_track_ids(self, zone_name: str) -> Tuple[List[Any], int]:
        """
        Return ``(current_track_ids, total_count)`` for a zone.

        - ``current_track_ids``: ids present in the zone this frame, deterministically
          ordered. Bounded by live occupancy, so it is safe to emit every frame.
        - ``total_count``: cumulative unique track count for the zone. Returned as an
          **integer only** — the full id list (``total_track_ids``) is intentionally
          not exposed, because on long-running / crowded streams that list would grow
          without bound and bloat every frame's output.
        """
        current = sorted(self._zone_current_track_ids.get(zone_name, set()), key=lambda x: str(x))
        total_count = len(self._zone_total_track_ids.get(zone_name, set()))
        return current, total_count

    def _build_zone_analysis(self, zone_stats: Dict[str, Any]) -> Dict[str, Any]:
        """Convert zone_stats to zone_analysis matching hazard_zone_entry structure."""
        zone_analysis: Dict[str, Any] = {}
        for zone_name, st in (zone_stats or {}).items():
            if not isinstance(st, dict):
                continue
            current_ids, total_count = self._zone_track_ids(zone_name)
            # Pixel polygon of the zone (None for the synthetic full-frame
            # "global" zone -> emit an empty list).
            poly = self._current_zone_polys.get(zone_name)
            zone_coords = poly if isinstance(poly, list) else []
            zone_analysis[zone_name] = {
                "current_count":         st.get("count", 0),
                "total_count":           total_count,
                "current_track_ids":     current_ids,
                "original_counts":       {},
                "capacity":              st.get("capacity", 0),
                "occupancy_percent":     st.get("occupancy_percent", 0.0),
                "state":                 st.get("state", "vacant"),
                "time_occupied_percent": st.get("time_occupied_percent", 0.0),
                "avg_occupancy_percent": st.get("avg_occupancy_percent", 0.0),
                "zone_coords":           zone_coords,
            }
        return zone_analysis

    # ----------------------------
    # Over-capacity evaluation (per-zone state machine -> alerts + incident)
    # ----------------------------
    def _evaluate_over_capacity(
        self,
        zone_stats: Dict[str, Any],
        frame_key: str,
        config: AreaUtilizationConfig,
    ) -> Dict[str, Any]:
        """Run the per-zone over-capacity state machine for this frame.

        Single source of truth: ``zone_config.zone_params[<zone>]["capacity"]``,
        which drives ``occupancy_percent``. Policy:

        * **Enter** an over-capacity episode when occupancy reaches
          ``OCCUPANCY_ENTER_PERCENT`` (100%, i.e. count >= capacity).
        * **Severity**: ``high`` at >=100%, escalating to ``critical`` at
          >=``OCCUPANCY_CRITICAL_PERCENT`` (120%).
        * **Alert once per episode**: a single alert is emitted on the frame the
          episode begins; it is *not* re-emitted while the episode stays active.
        * **Exit (hysteresis / anti-flicker)**: an active episode only clears
          after occupancy stays **below** ``OCCUPANCY_EXIT_PERCENT`` (90%) for
          ``OCCUPANCY_EXIT_FRAMES`` (5) consecutive frames. Between 90% and 100%
          the episode is held active (no flicker on small dips).

        Returns
        -------
        dict with:
          - ``alerts``: new one-shot alerts emitted this frame (``list``)
          - ``active_zones``: ``{zone_name: occupancy_percent}`` for zones whose
            episode is currently active (drives the persistent incident)
          - ``max_active_occupancy``: max occupancy among active zones (or 0.0)
        """
        alerts: List[Dict[str, Any]] = []
        active_zones: Dict[str, float] = {}

        alert_cfg = config.alert_config
        alert_type_cfg = getattr(alert_cfg, "alert_type", ["Default"]) if alert_cfg else ["Default"]
        alert_value_cfg = getattr(alert_cfg, "alert_value", ["JSON"]) if alert_cfg else ["JSON"]
        alert_type_str = (
            alert_type_cfg[0]
            if isinstance(alert_type_cfg, (list, tuple)) and len(alert_type_cfg) > 0
            else alert_type_cfg
        )
        settings_map = {t: v for t, v in zip(alert_type_cfg, alert_value_cfg)}

        for zone_name, stats in zone_stats.items():
            stats = _as_dict(stats)
            capacity = int(stats.get("capacity", 0) or 0)
            count = int(stats.get("count", 0) or 0)
            occ = float(stats.get("occupancy_percent", 0.0) or 0.0)

            state = self._zone_oc_state.setdefault(
                zone_name, {"active": False, "below_frames": 0, "alerted": False}
            )

            # Capacity must be valid to evaluate over-capacity for this zone.
            if capacity <= 0:
                state["active"] = False
                state["below_frames"] = 0
                state["alerted"] = False
                continue

            if not state["active"]:
                # Enter a new episode at/above 100% occupancy.
                if occ >= OCCUPANCY_ENTER_PERCENT:
                    state["active"] = True
                    state["below_frames"] = 0
                    state["alerted"] = False
            else:
                # Active: apply exit hysteresis. Reset the counter on any frame at
                # or above the exit threshold; only clear after a sustained dip.
                if occ >= OCCUPANCY_EXIT_PERCENT:
                    state["below_frames"] = 0
                else:
                    state["below_frames"] += 1
                    if state["below_frames"] >= OCCUPANCY_EXIT_FRAMES:
                        state["active"] = False
                        state["alerted"] = False
                        state["below_frames"] = 0

            if state["active"]:
                active_zones[zone_name] = occ
                # One-shot alert at episode start (not re-emitted while active).
                if not state["alerted"] and alert_cfg is not None:
                    severity = _severity_for_occupancy(occ)
                    alert = self.create_alert_object(
                        alert_type_str,
                        f"alert_occ_{zone_name}_{frame_key}",
                        self.CASE_TYPE,
                        capacity,
                        ascending=True,
                        settings=settings_map,
                    )
                    alert["current_value"] = count
                    alert["zone"] = zone_name
                    alert["capacity"] = capacity
                    alert["occupancy_percent"] = occ
                    alert["severity"] = severity
                    alerts.append(alert)
                    state["alerted"] = True

        max_active_occ = max(active_zones.values()) if active_zones else 0.0

        if alerts:
            try:
                self.logger.info(f"area_utilization: generated over-capacity alerts: {alerts}")
            except Exception:
                # Non-fatal: exception ignored here; execution continues per surrounding logic.
                pass

        return {
            "alerts": alerts,
            "active_zones": active_zones,
            "max_active_occupancy": max_active_occ,
        }

    # ----------------------------
    # Incident generation (persistent over-capacity incident)
    # ----------------------------
    def _build_incident_alert_settings(self, alert_config, zone_stats: Dict[str, Any]) -> list:
        """Build alert_settings list. Thresholds are the per-zone capacities
        (from ``zone_params``) — the same values that drive the math and alerts."""
        if not (alert_config and hasattr(alert_config, "alert_type")):
            return []
        alert_type_cfg = getattr(alert_config, "alert_type", ["Default"])
        alert_value_cfg = getattr(alert_config, "alert_value", ["JSON"])
        zone_capacities = {
            zn: _as_dict(st).get("capacity", 0)
            for zn, st in (zone_stats or {}).items()
        }
        return [
            {
                "alert_type": alert_type_cfg,
                "incident_category": self.CASE_TYPE,
                "threshold_value": zone_capacities,
                "ascending": True,
                "settings": dict(zip(alert_type_cfg, alert_value_cfg)),
            }
        ]

    def _generate_incidents(
        self,
        over_capacity: Dict[str, Any],
        zone_stats: Dict[str, Any],
        config: AreaUtilizationConfig,
        frame_number: Optional[int] = None,
        stream_info: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        """Emit a single, persistent over-capacity incident.

        An incident exists only while at least one zone is in an active
        over-capacity episode (see :meth:`_evaluate_over_capacity`). The same
        incident (stable ``incident_id`` + ``start_time``) is re-emitted every
        frame with ``end_time=""`` while active, and a closing snapshot (with a
        real ``end_time``) is emitted on the frame the condition clears.

        Severity tracks the most-occupied active zone: ``high`` at >=100%,
        ``critical`` at >=120%. It may escalate (or de-escalate back to ``high``)
        across frames while the incident persists.
        """
        incidents: List[Dict[str, Any]] = []
        active_zones: Dict[str, float] = over_capacity.get("active_zones", {})
        alerts: List[Dict[str, Any]] = over_capacity.get("alerts", [])
        current_timestamp = self._get_current_timestamp_str(stream_info)
        camera_info = self.get_camera_info_from_stream(stream_info)

        self._ascending_alert_list = self._ascending_alert_list[-900:]

        # No zone over capacity -> no active incident.
        if not active_zones:
            self._ascending_alert_list.append(0)
            if self._au_incident_active and self._au_last_incident is not None:
                # Episode just ended this frame: re-emit it with a real end_time.
                closing = dict(self._au_last_incident)
                closing["end_time"] = current_timestamp
                incidents.append(closing)
            else:
                incidents.append({})
            self._au_incident_active = False
            self._au_last_incident = None
            self._au_incident_id = None
            self._au_incident_start_time = None
            return incidents

        # At least one zone is over capacity -> incident is active.
        max_occ = over_capacity.get("max_active_occupancy", 0.0) or 0.0
        level = _severity_for_occupancy(max_occ)
        self._ascending_alert_list.append(3 if level == SEVERITY_CRITICAL else 2)

        if not self._au_incident_active:
            # New episode: fix a stable id and start time for the whole episode.
            self._au_incident_active = True
            self._au_incident_id = f"{self.CASE_TYPE}_{frame_number}"
            self._au_incident_start_time = current_timestamp
        start_timestamp = self._au_incident_start_time or current_timestamp
        self._debug_stream_timing("start_timestamp", start_timestamp)

        zones_desc = ", ".join(
            f"{zn} ({active_zones[zn]:.1f}%)" for zn in sorted(active_zones)
        )
        human_text = "\n".join(
            [
                f"AREA UTILIZATION OVER-CAPACITY @ {current_timestamp}:",
                f"\tSeverity Level: {level}",
                f"\tOver-capacity zones: {zones_desc}",
            ]
        )
        alert_settings = self._build_incident_alert_settings(config.alert_config, zone_stats)

        event = self.create_incident(
            incident_id=self._au_incident_id,
            incident_type=self.CASE_TYPE,
            severity_level=level,
            human_text=human_text,
            camera_info=camera_info,
            alerts=alerts,
            alert_settings=alert_settings,
            start_time=start_timestamp,
            end_time="",
            level_settings={"high": 4, "critical": 7},
        )
        # create_incident does `end_time or timestamp`, which would swallow an empty
        # string; force "" so consumers see the incident as still active.
        event["end_time"] = ""
        # Surface which zones are over capacity directly on the incident.
        event["over_capacity_zones"] = dict(active_zones)
        incidents.append(event)
        # Remember the active incident so we can emit a closing snapshot when it ends.
        self._au_last_incident = dict(event)
        return incidents

    # ----------------------------
    # Tracking stats (kept people_counting style)
    # ----------------------------
    def _generate_tracking_stats(
        self,
        counting_summary: Dict[str, Any],
        alerts: List[Dict[str, Any]],
        zone_stats: Dict[str, Any],
        config: AreaUtilizationConfig,
        _frame_number: Optional[int] = None,
        stream_info: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        _ = (_frame_number,)
        camera_info = self.get_camera_info_from_stream(stream_info)

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

        detections_objs = []
        for detection in counting_summary.get("detections", []):
            bbox = detection.get("bounding_box", {})
            category = detection.get("category", "person")
            detection_obj = self.create_detection_object(category, bbox)
            # preserve optional fields for downstream consumers
            if detection.get("track_id") is not None:
                detection_obj["track_id"] = detection.get("track_id")
            if detection.get("confidence") is not None:
                detection_obj["confidence"] = detection.get("confidence")
            detections_objs.append(detection_obj)

        alert_settings = []
        if config.alert_config and hasattr(config.alert_config, "alert_type"):
            alert_type_cfg = getattr(config.alert_config, "alert_type", ["Default"])
            alert_value_cfg = getattr(config.alert_config, "alert_value", ["JSON"])
            settings_map = {t: v for t, v in zip(alert_type_cfg, alert_value_cfg)}
            # Thresholds are the per-zone capacities (from zone_params) — the same
            # single source of truth that drives the math and the alerts.
            zone_capacities = {
                zn: _as_dict(st).get("capacity", 0)
                for zn, st in (zone_stats or {}).items()
            }
            alert_settings.append(
                {
                    "alert_type": alert_type_cfg,
                    "incident_category": self.CASE_TYPE,
                    "threshold_value": zone_capacities,
                    "ascending": True,
                    "settings": settings_map,
                }
            )

        human_text_lines: List[str] = []
        human_text_lines.append(f"CURRENT FRAME @ {current_timestamp}:")
        for _cat, count in per_category_count.items():
            human_text_lines.append(f"\t- People Detected: {count}")

        # Add per-zone counts and occupancy metrics to human text
        if zone_stats:
            human_text_lines.append("")
            human_text_lines.append("Zone Utilization:")
            for zname, zst in zone_stats.items():
                human_text_lines.append(
                    f"\t- {zname}: {zst.get('count', 0)}/{zst.get('capacity', 0)} "
                    f"occ={zst.get('occupancy_percent', 0):.1f}% "
                    f"time={zst.get('time_occupied_percent', 0):.1f}% "
                    f"avg={zst.get('avg_occupancy_percent', 0):.1f}%"
                )

        human_text_lines.append("")
        human_text = "\n".join(human_text_lines)

        reset_settings = [{"interval_type": "daily", "reset_time": {"value": 9, "time_unit": "hour"}}]
        tracking_stat = self.create_tracking_stats(
            total_counts=total_counts,
            current_counts=current_counts,
            detections=detections_objs,
            human_text=human_text,
            camera_info=camera_info,
            alerts=alerts,
            alert_settings=alert_settings,
            reset_settings=reset_settings,
            start_time=high_precision_start_timestamp,
            reset_time=high_precision_reset_timestamp,
        )
        tracking_stat["target_categories"] = self.target_categories
        # Per-zone metrics are surfaced once, in the frame-level ``zone_analysis``
        # block (see _build_zone_analysis). It is a superset of the legacy
        # ``zone_statistics`` (raw zone_stats dict) and ``zone_stats`` (per-zone
        # track-id list) that used to be duplicated here, so those keys were
        # removed to avoid carrying the same data three times.
        new_counts = self.get_new_counts_this_frame()
        tracking_stat["current_new_counts"] = [
            {"category": cat, "count": new_counts.get(cat, 0)} for cat in self.target_categories
        ]
        tracking_stat["total_current_counts"] = current_counts
        return [tracking_stat]

    # ----------------------------
    # Business analytics (NEW)
    # ----------------------------
    def _generate_business_analytics(
        self,
        zone_stats: Dict[str, Any],
        alerts: Optional[List[Dict[str, Any]]],
        stream_info: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        camera_info = self.get_camera_info_from_stream(stream_info)
        human_text = self._build_utilization_human_text(zone_stats)

        analytics_obj = self.create_business_analytics(
            analysis_name="area_utilization",
            statistics=zone_stats,
            human_text=human_text,
            camera_info=camera_info if camera_info else self.get_default_camera_info(),
            alerts=alerts or [],
        )
        return [analytics_obj]

    def _build_utilization_human_text(self, zone_stats: Dict[str, Any]) -> str:
        lines = ["Area Utilization (Capacity-based):"]
        for z, s in zone_stats.items():
            lines.append(
                f"\t{z}: {s.get('occupancy_percent', 0.0)}% "
                f"({s.get('count', 0)}/{s.get('capacity', 0)}) "
                f"state={s.get('state', 'unknown')} | "
                f"time_occupied={s.get('time_occupied_percent', 0.0)}% "
                f"avg_occ={s.get('avg_occupancy_percent', 0.0)}%"
            )
        return "\n".join(lines)

    # ----------------------------
    # Human summary generator (kept style)
    # ----------------------------
    def _generate_summary(
        self,
        incidents: List[Dict[str, Any]],
        tracking_stats: List[Dict[str, Any]],
        business_analytics: List[Dict[str, Any]],
    ) -> List[str]:
        lines: List[str] = []
        lines.append("Application Name: " + self.CASE_TYPE)
        lines.append("Application Version: " + self.CASE_VERSION)

        if len(tracking_stats) > 0:
            lines.append("Tracking Statistics: " + f"\t{tracking_stats[0].get('human_text', '')}")
        if len(business_analytics) > 0:
            lines.append("Business Analytics: " + f"\t{business_analytics[0].get('human_text', '')}")

        if len(incidents) == 0 and len(tracking_stats) == 0 and len(business_analytics) == 0:
            lines.append("Summary: " + "No Summary Data")

        return ["\n".join(lines)]

    # ----------------------------
    # Counting + tracking state helpers
    # ----------------------------
    def _count_people(self, detections: List[Dict[str, Any]]) -> Dict[str, Any]:
        counts: Dict[str, int] = {}
        for det in detections:
            if not isinstance(det, dict):
                continue
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
                if isinstance(det, dict)
            ],
        }

    def _update_tracking_state(self, detections: List[Dict[str, Any]]):
        if not hasattr(self, "_per_category_total_track_ids"):
            self._per_category_total_track_ids = {cat: set() for cat in self.target_categories}
        self._current_frame_track_ids = {cat: set() for cat in self.target_categories}
        # Track ids appearing for the FIRST time this frame (drives current_new_counts).
        self._new_track_ids_this_frame = {cat: set() for cat in self.target_categories}

        for det in detections:
            if not isinstance(det, dict):
                continue
            cat = det.get("category")
            track_id = det.get("track_id")
            if cat not in self.target_categories:
                continue
            if track_id is not None:
                total_set = self._per_category_total_track_ids.setdefault(cat, set())
                if track_id not in total_set:
                    # First time we have ever seen this track id for this category.
                    self._new_track_ids_this_frame.setdefault(cat, set()).add(track_id)
                    total_set.add(track_id)
                self._current_frame_track_ids[cat].add(track_id)

    def get_total_counts(self) -> Dict[str, int]:
        return {cat: len(ids) for cat, ids in getattr(self, "_per_category_total_track_ids", {}).items()}

    def get_new_counts_this_frame(self) -> Dict[str, int]:
        """Count of track ids reported for the FIRST time this frame, per category."""
        return {cat: len(ids) for cat, ids in getattr(self, "_new_track_ids_this_frame", {}).items()}

    # ----------------------------
    # Timestamp helpers (copied style from people_counting)
    # ----------------------------
    def _format_timestamp_for_stream(self, timestamp: float) -> str:
        dt = datetime.fromtimestamp(timestamp, tz=timezone.utc)
        return dt.strftime("%Y:%m:%d %H:%M:%S")

    def _format_timestamp_for_video(self, timestamp: float) -> str:
        hours = int(timestamp // 3600)
        minutes = int((timestamp % 3600) // 60)
        seconds = round(float(timestamp % 60), 2)
        return f"{hours:02d}:{minutes:02d}:{seconds:.1f}"

    def _format_timestamp(self, timestamp: Any) -> str:
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
                    formatted = f"{parts[0]}:{parts[1]}:{parts[2]} {'-'.join(parts[3:])}"
                    return formatted
        except Exception:
            # Non-fatal: exception ignored here; execution continues per surrounding logic.
            pass

        return timestamp_clean

    def _get_current_timestamp_str(
        self,
        stream_info: Optional[Dict[str, Any]],
        precision=False,
        frame_id: Optional[str] = None,
    ) -> str:
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
                _ = self._format_timestamp_for_video(start_time)
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
            _ = self._format_timestamp_for_video(start_time)
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
