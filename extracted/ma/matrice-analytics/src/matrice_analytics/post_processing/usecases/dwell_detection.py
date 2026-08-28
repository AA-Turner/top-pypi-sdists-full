import threading
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
from ..Trackers import ConfigDrivenTracker, TrackerProfile  # noqa: E402
from ..utils import (
    BBoxSmoothingConfig,
    BBoxSmoothingTracker,
    apply_category_mapping,
    bbox_smoothing,
    count_objects_in_zones,
    filter_by_confidence,
    get_bbox_bottom_center,
    match_results_structure,
    point_in_polygon,
)
from ..utils.incident_manager_utils import INCIDENT_MANAGER, IncidentManagerFactory
from ..utils.post_processing_config_client import (
    GEOMETRY_RETRY_INTERVAL as _GEOMETRY_RETRY_INTERVAL,
)
from ..utils.post_processing_config_client import (
    PostProcessingConfigClient,
)

_DEFAULT_CAMERA_ID = "camera"
_INCIDENT_LOG = "[INCIDENT_MANAGER]"


def _resolve_manager_camera_id(stream_info: Optional[Dict[str, Any]]) -> str:
    """Resolve the camera key used by IncidentManager state tracking.

    Uses the real camera id from ``stream_info`` (never a hardcoded value) so
    per-camera incident lifecycle stays correct in multi-camera deployments.
    """
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


@dataclass
class DwellConfig(BaseConfig):
    """Configuration for dwell detection use case.

    All time-sensitive thresholds are expressed in **wall-clock seconds** so
    they are independent of the inference frame-rate.  The system is called
    once per inferred frame (which may be every 1st, 3rd, 10th, or any Nth
    video frame), so frame-count-based thresholds are inherently unreliable.

    Key thresholds
    --------------
    dwell_threshold
        Continuous stationary wall-clock **seconds** before a person is
        labelled ``Dweller``.  Default 5.0 s catches genuine dwell events
        while ignoring people who pause briefly while walking.
    loitering_time_threshold_seconds
        Wall-clock seconds of continuous dwelling after which a per-person
        dwell alert is fired exactly once per track per session.  Defaults to
        60 s (1 minute).
    centroid_threshold
        Maximum Euclidean **pixel** displacement between successive process()
        calls for a person to be considered stationary.  Frame-rate agnostic
        because it measures spatial distance, not temporal distance.
    stale_track_frames
        Wall-clock **seconds** of continuous absence before a track is evicted
        from the stationary-tracks registry.  (Name kept for API compatibility;
        the value is now in seconds.)  Default 3 s survives brief occlusions
        and zone-boundary jitter.
    movement_penalty
        Wall-clock **seconds** subtracted from a track's accumulated stationary
        time when movement is detected.  (Name kept for API compatibility;
        the value is now in seconds.)  Gentle enough to survive natural weight
        shifts without resetting dwell progress entirely.
    zone_params
        Optional per-zone overrides for any threshold above.  When a key is
        absent for a given zone the global ``DwellConfig`` value is used as
        the default.  Populated automatically when resolving zones from the
        Matrice UI/API.
        Example::

            {
              "shelf":    {"dwell_threshold": 8.0,
                           "loitering_time_threshold_seconds": 90.0},
              "checkout": {"stale_track_frames": 5.0,
                           "movement_penalty": 1.0}
            }
    """

    enable_smoothing: bool = True
    # Pixel distance a person's centroid may shift between consecutive
    # process() calls and still be considered stationary.  12 px absorbs
    # natural body sway and YOLO bbox jitter without masking a real step.
    centroid_threshold: float = 15.0
    smoothing_algorithm: str = "observability"
    smoothing_window_size: int = 20
    smoothing_cooldown_frames: int = 5
    smoothing_confidence_range_factor: float = 0.5
    confidence_threshold: float = 0.25
    # Continuous stationary seconds required to label someone a Dweller.
    dwell_threshold: float = 2.0
    # Alert after 60 s of continuous dwelling.
    loitering_time_threshold_seconds: float = 10.0
    # Seconds of absence before a track is evicted from the stationary registry.
    stale_track_frames: float = 3.0
    # Seconds subtracted from accumulated stationary time on movement detection.
    movement_penalty: float = 0.5
    # Minimum wall-clock seconds between published incidents for the SAME ongoing
    # dwell episode. Brief detection dropouts shorter than this are treated as the
    # same incident (no new incident emitted); once dwell stops for longer than
    # this the episode closes, so the next dwell is a NEW incident and the cooldown
    # resets. Default 60 s → at most one incident per minute per unique dwell.
    incident_cooldown_seconds: float = 60.0
    usecase_categories: List[str] = field(default_factory=lambda: ["person"])
    target_categories: List[str] = field(default_factory=lambda: ["person"])
    alert_config: Optional[AlertConfig] = None
    zone_config: Optional[Dict[str, Dict[str, List[List[float]]]]] = None
    # Per-zone parameter overrides (all time-based, seconds).
    zone_params: Optional[Dict[str, Dict[str, Any]]] = None
    index_to_category: Optional[Dict[int, str]] = field(default_factory=lambda: {0: "person"})
    person_index: int = 0


class DwellUseCase(BaseProcessor):
    """Per-frame dwell / loitering detector.

    Tracks how long each detected person remains stationary inside configured
    zones and emits structured analytics with:

    * Per-person dwell duration in seconds.
    * Per-zone unique-dweller counts and average dwell times.
    * Per-person dwell alerts when a person exceeds the zone-specific (or
      global) ``loitering_time_threshold_seconds``.
    * Zone geometry resolved from the Matrice UI/API (same pattern as
      ``HazardZoneEntryUseCase``) so operators can draw zones without
      re-deploying config files.
    """

    CATEGORY_DISPLAY = {"person": "Person"}

    def __init__(self):
        super().__init__("dwell")
        self.category = "general"
        self.CASE_TYPE: Optional[str] = "dwell"
        self.CASE_VERSION: Optional[str] = "1.1"
        self.target_categories = ["person"]
        self.smoothing_tracker = None
        self.tracker = None
        self._tracker_seam = ConfigDrivenTracker()
        self._total_frame_counter = 0
        self._global_frame_offset = 0
        self._tracking_start_time = None
        self._track_aliases: Dict[Any, Any] = {}
        self._canonical_tracks: Dict[Any, Dict[str, Any]] = {}
        # IoU threshold for merging a new raw_id into an existing canonical track.
        # 0.05 was far too low — any slight bbox overlap (different persons standing
        # near each other) would incorrectly merge them into one canonical ID.
        # 0.20 matches the people_counting baseline; combined with the center-
        # distance + size-ratio fallback below, it gives robust re-association.
        self._track_merge_iou_threshold: float = 0.20
        # How long (wall-clock seconds) to keep a canonical track alive after
        # last seeing it.  7 s gives dwell continuity across brief occlusions.
        self._track_merge_time_window: float = 7.0
        # Each entry is (wall_clock_timestamp, severity_value: 0-3).
        # Stored as tuples so trend queries use time windows instead of
        # frame-count windows — making the logic FPS-independent.
        self._ascending_alert_entries: List[Tuple[float, int]] = []
        self.current_incident_end_timestamp: str = "N/A"

        # ------------------------------------------------------------------ #
        # Incident manager wiring (legacy INCIDENT flow, same as             #
        # loitering_detection). Publishes the dwell incident to the          #
        # ``incident_res`` stream via IncidentManager, which owns the        #
        # open/close lifecycle and re-derives severity from incident_quant.  #
        # ------------------------------------------------------------------ #
        self._incident_manager_factory: Optional[IncidentManagerFactory] = None
        self._incident_manager: Optional[INCIDENT_MANAGER] = None
        self._incident_manager_initialized: bool = False

        # ------------------------------------------------------------------ #
        # Persistent single-incident lifecycle (same idea as                 #
        # loitering_detection). One stable incident per dwell episode instead #
        # of a brand-new incident every frame, plus a wall-clock cooldown so  #
        # the same ongoing incident is not re-published more than once per    #
        # ``incident_cooldown_seconds``. A new episode resets the cooldown.   #
        # ------------------------------------------------------------------ #
        self._dwell_incident_active: bool = False
        # Monotonic episode counter → stable incident_id "dwell_<n>" per episode.
        self._dwell_episode_id: int = 0
        # Wall-clock time of the most recent frame with an active dwell incident.
        self._dwell_last_active_wall: float = 0.0
        # start_time held stable for the duration of the episode.
        self._dwell_episode_start_ts: str = ""
        # Highest severity rank seen this episode (kept non-decreasing so the
        # published severity never flaps down frame-to-frame).
        self._dwell_episode_max_rank: int = -1
        # Highest incident_quant seen this episode. The IncidentManager derives
        # severity from incident_quant, so holding it non-decreasing stops the
        # manager from re-publishing a level change every time the count wobbles.
        self._dwell_episode_max_quant: float = 0.0
        # Snapshot of the last active incident so it can be re-emitted during
        # brief dropouts and closed (with a real end_time) when the episode ends.
        self._dwell_last_incident: Optional[Dict[str, Any]] = None

        # ------------------------------------------------------------------ #
        # VOLUME analytics state                                             #
        # ------------------------------------------------------------------ #
        # Unique in-zone persons (footfall) seen on the most recent frame —
        # drives the ``visitors_in_zone`` VOLUME metric. Set in
        # _check_dwell_objects every frame.
        self._last_visitors_in_zone: int = 0
        # track ids appearing for the first time this frame, per category —
        # drives ``current_new_counts`` in tracking_stats.
        self._new_track_ids_this_frame: Dict[str, set] = {}

        # Stationary-track registry — keyed by canonical track_id.
        # Each entry: {centroid, start_wall_time, dwell_start_wall_time,
        #              last_seen_time, bbox, zone_name}
        self._stationary_tracks: Dict[Any, Dict[str, Any]] = {}

        # Zone occupancy counters
        self._zone_current_track_ids: Dict[str, set] = {}
        self._zone_total_track_ids: Dict[str, set] = {}
        self._zone_current_counts: Dict[str, int] = {}
        self._zone_total_counts: Dict[str, int] = {}

        self.start_timer = None

        # ------------------------------------------------------------------ #
        # Dwell-duration and dwell-alert state                               #
        # ------------------------------------------------------------------ #

        # Track IDs that have already received a dwell alert this session.
        self._loitering_alerted_tracks: Set[Any] = set()

        # zone_name -> set of track_ids ever confirmed as Dweller in that zone
        self._zone_unique_dwellers: Dict[str, Set[Any]] = {}

        # track_id -> latest known dwell_seconds (updated every dwell frame)
        self._track_dwell_seconds: Dict[Any, float] = {}

        # ------------------------------------------------------------------ #
        # API-based zone geometry resolution (same as hazard_zone_entry)      #
        # ------------------------------------------------------------------ #
        self._config_client: Optional[PostProcessingConfigClient] = None
        self._resolved_geometry_cache: Optional["DwellConfig"] = None
        self._geometry_thread: Optional[threading.Thread] = None
        self._zone_resolution_attempted: bool = False
        # Guards writes from the background resolver thread vs reads in process()
        self._geometry_lock = threading.Lock()

    # ------------------------------------------------------------------ #
    # Public API — zone geometry injection                                #
    # ------------------------------------------------------------------ #

    def set_config_client(self, client: Optional[PostProcessingConfigClient]) -> None:
        """Inject a ``PostProcessingConfigClient`` for API-based zone resolution.

        Must be called before the first ``process()`` invocation.  When a
        client is provided the use case resolves zone polygons drawn in the
        Matrice UI, falling back to ``zone_config`` in ``DwellConfig`` if the
        API is unavailable.
        """
        self._config_client = client

    # ------------------------------------------------------------------ #
    # Zone-param resolver                                                 #
    # ------------------------------------------------------------------ #

    def _get_zone_param(self, zone_name: str, param_name: str, config: "DwellConfig") -> Any:
        """Return the value of ``param_name`` for a specific zone.

        Lookup order:
        1. ``config.zone_params[zone_name][param_name]`` — zone-specific override.
        2. ``getattr(config, param_name)`` — global ``DwellConfig`` default.

        This lets operators configure e.g. a shorter dwell threshold for a
        busy checkout zone without changing the global config.
        """
        if config.zone_params:
            zone_overrides = config.zone_params.get(zone_name, {})
            if param_name in zone_overrides:
                return zone_overrides[param_name]
        return getattr(config, param_name, None)

    # ------------------------------------------------------------------ #
    # Background zone-geometry resolver                                   #
    # ------------------------------------------------------------------ #

    def _start_geometry_resolver(self, config: "DwellConfig", stream_info: Dict[str, Any]) -> None:
        """Spawn a daemon thread that retries API zone resolution until it succeeds."""
        if self._geometry_thread is not None:
            return  # already running

        def _resolver() -> None:
            while True:
                try:
                    result = self._resolve_geometry_from_api(config, stream_info)
                    if result is not None:
                        with self._geometry_lock:
                            self._resolved_geometry_cache = result
                        self.logger.info("DwellUseCase: zone geometry resolved from API (background thread)")
                        return
                    self.logger.info(
                        "DwellUseCase: API returned no zone config, retrying in %ds",
                        _GEOMETRY_RETRY_INTERVAL,
                    )
                except Exception as exc:
                    self.logger.warning("DwellUseCase: background geometry resolve error: %s", exc)
                time.sleep(_GEOMETRY_RETRY_INTERVAL)

        t = threading.Thread(target=_resolver, daemon=True, name="dwell-zone-geometry-resolver")
        self._geometry_thread = t
        t.start()
        self.logger.info("DwellUseCase: started background zone geometry resolver thread")

    def _resolve_geometry_from_api(
        self,
        config: "DwellConfig",
        stream_info: Optional[Dict[str, Any]],
    ) -> Optional["DwellConfig"]:
        """Resolve zone polygons from the Matrice post-processing config API.

        Resolution order for the API client:
        1. Client injected via ``set_config_client()``.
        2. ``stream_info["config_client"]`` if present.
        3. Lazy creation from env vars:
           ``MATRICE_ACCESS_KEY_ID`` / ``MATRICE_SECRET_ACCESS_KEY`` /
           ``MATRICE_ACCOUNT_NUMBER``.

        Returns a new ``DwellConfig`` with ``zone_config`` populated, or
        ``None`` when zones cannot be resolved.
        """
        client = self._config_client or (stream_info.get("config_client") if stream_info else None)
        if not client and stream_info:
            try:
                client = PostProcessingConfigClient(logger=self.logger)
                if getattr(client, "_session", None) is None:
                    self.logger.info(
                        "DwellUseCase: _resolve_geometry_from_api skipped — no session. "
                        "Set MATRICE_ACCESS_KEY_ID / MATRICE_SECRET_ACCESS_KEY / MATRICE_ACCOUNT_NUMBER "
                        "or call set_config_client() to enable API zone resolution."
                    )
                    return None
                self._config_client = client
            except Exception as exc:
                self.logger.warning("DwellUseCase: cannot create PostProcessingConfigClient: %s", exc)
                return None

        if not stream_info or not client:
            return None

        ids = client.get_stream_identifiers(stream_info)
        app_deployment_id = ids.get("app_deployment_id") or ""
        camera_id = ids.get("camera_id") or ""
        self.logger.info(
            "DwellUseCase: _resolve_geometry_from_api app_deployment_id=%s camera_id=%s",
            app_deployment_id or "(empty)",
            camera_id or "(empty)",
        )

        if not app_deployment_id or not camera_id:
            self.logger.info("DwellUseCase: _resolve_geometry_from_api skipped — missing identifiers")
            return None

        configs, err, _ = client.get_post_processing_configs_by_app_deployment(app_deployment_id)
        if err or not configs:
            self.logger.info(
                "DwellUseCase: _resolve_geometry_from_api — fetch failed (err=%r, count=%s)",
                err,
                len(configs) if configs else 0,
            )
            return None

        filtered = client.filter_configs_by_camera_id(configs, camera_id)
        if not filtered:
            self.logger.info("DwellUseCase: _resolve_geometry_from_api — no config for camera_id=%s", camera_id)
            return None

        doc = filtered[0]
        width, height = client.get_resolution(camera_id)
        if width is None or height is None:
            self.logger.info("DwellUseCase: _resolve_geometry_from_api — no resolution for camera_id=%s", camera_id)
            return None

        doc_px = client.denormalize_config(doc, width, height)
        post = doc_px.get("postProcessing") or {}
        cam_cfg = post.get(camera_id) or {}
        zone_config_raw = cam_cfg.get("zone_config") or {}
        zones_px = zone_config_raw.get("zones") or {}

        if not isinstance(zones_px, dict) or not zones_px:
            self.logger.info("DwellUseCase: _resolve_geometry_from_api — no zones for camera_id=%s", camera_id)
            return None

        zones_dict = {name: [list(pt) for pt in points] for name, points in zones_px.items()}
        self.logger.info("DwellUseCase: resolved %d zone(s) from API: %s", len(zones_dict), list(zones_dict.keys()))

        # Extract per-zone parameter overrides.
        #
        # API response shape (confirmed from real config format):
        #
        #   postProcessing:
        #     {camera_id}:              ← cam_cfg
        #       zone_config:            ← zone_config_raw
        #         zones:     { ... }    ← pixel-coord polygons
        #         zone_params: { ... }  ← thresholds live HERE, inside zone_config
        #
        # zone_params is NOT at cam_cfg level — it is a sibling of "zones"
        # inside "zone_config".  Reading cam_cfg.get("zone_params") would always
        # return empty, silently dropping all per-zone threshold overrides.
        zone_params_raw: Dict[str, Any] = zone_config_raw.get("zone_params") or {}
        zone_params: Optional[Dict[str, Dict[str, Any]]] = (
            {zn: dict(zp) for zn, zp in zone_params_raw.items() if isinstance(zp, dict)} if zone_params_raw else None
        )
        if zone_params:
            self.logger.info("DwellUseCase: resolved zone_params for zones: %s", list(zone_params.keys()))
        else:
            self.logger.info("DwellUseCase: no zone_params found in zone_config (using global DwellConfig defaults)")

        # Return a new DwellConfig preserving all existing settings but with
        # zone_config and zone_params replaced by API-resolved values.
        from dataclasses import replace as _replace  # local import to avoid top-level clash

        return _replace(
            config,
            zone_config={"zones": zones_dict},
            zone_params=zone_params if zone_params else config.zone_params,
        )

    # ------------------------------------------------------------------ #
    # Incident manager (fire-style: process every frame, incident or {})  #
    # ------------------------------------------------------------------ #

    def _initialize_incident_manager_once(self, config: "DwellConfig") -> None:
        """Initialize the incident manager exactly once (first ``process()``)."""
        if self._incident_manager_initialized:
            return
        try:
            self.logger.info("%s Starting incident manager initialization for dwell detection...", _INCIDENT_LOG)
            if self._incident_manager_factory is None:
                self._incident_manager_factory = IncidentManagerFactory(logger=self.logger)
            self._incident_manager = self._incident_manager_factory.initialize(config)
            if self._incident_manager:
                self.logger.info("%s Incident manager initialized successfully for dwell detection", _INCIDENT_LOG)
            else:
                self.logger.warning("%s Incident manager not available; incidents won't be published", _INCIDENT_LOG)
        except Exception as e:
            self.logger.error("%s Incident manager initialization failed: %s", _INCIDENT_LOG, e, exc_info=True)
        finally:
            self._incident_manager_initialized = True

    def _send_incident_to_manager(
        self,
        incident: Dict,
        stream_info: Optional[Dict[str, Any]] = None,
        context: Optional[ProcessingContext] = None,
    ) -> bool:
        """Feed the dwell incident (or ``{}``) to the IncidentManager every frame.

        Fire-style: always call ``process_incident`` so idle frames can close the
        incident cycle. Sets ``incident_published_via_manager`` so
        ``post_processor`` does not double-publish the same incident via the
        legacy bridge. Never publishes to Redis directly from the use case.
        """
        camera_id = _resolve_manager_camera_id(stream_info)
        published = False

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
                    self.logger.info("%s Incident published for camera: %s", _INCIDENT_LOG, camera_id)
            except Exception as e:
                self.logger.error("%s Error publishing incident: %s", _INCIDENT_LOG, e, exc_info=True)

        if context is not None:
            context.metadata["incident_published_via_manager"] = bool(self._incident_manager)
        return published

    # ------------------------------------------------------------------ #
    # Main entry point                                                    #
    # ------------------------------------------------------------------ #

    def process(
        self,
        data: Any,
        config: ConfigProtocol,
        context: Optional[ProcessingContext] = None,
        stream_info: Optional[Dict[str, Any]] = None,
    ) -> ProcessingResult:
        """Process one frame of detections and return ``agg_summary``.

        ``agg_summary`` structure (keyed by frame_number)::

            {
              "<frame>": {
                "incidents":        { ... severity + dwell_person_zones ... },
                "tracking_stats":   { ... dwell_durations, zone_dwell_summary,
                                        dwell_alerts ... },
                "business_analytics": {},
                "alerts":           [ ... count-threshold alerts ... ],
                "zone_analysis":    { ... per-zone track counts ... },
                "human_text":       "..."
              }
            }
        """
        start_time = time.time()
        if not isinstance(config, DwellConfig):
            self._debug_elapsed_since(start_time)
            return self.create_error_result(
                "Invalid config type",
                usecase=self.name,
                category=self.category,
                context=context,
            )
        if context is None:
            context = ProcessingContext()

        # ------------------------------------------------------------------ #
        # Zone geometry resolution from UI/API — first frame only (blocking). #
        # On failure a background retry thread is started.                    #
        # ------------------------------------------------------------------ #
        if not self._zone_resolution_attempted:
            self._zone_resolution_attempted = True
            if stream_info:
                self.logger.info("DwellUseCase: attempting zone geometry resolution from API (first frame)")
                try:
                    resolved = self._resolve_geometry_from_api(config, stream_info)
                    if resolved is not None:
                        with self._geometry_lock:
                            self._resolved_geometry_cache = resolved
                        self.logger.info("DwellUseCase: zone geometry resolved and cached")
                    else:
                        self.logger.warning(
                            "DwellUseCase: API returned no zones on first frame; "
                            "starting background retry (every %ds). "
                            "Using zone_config from DwellConfig until resolved.",
                            _GEOMETRY_RETRY_INTERVAL,
                        )
                        self._start_geometry_resolver(config, stream_info)
                except Exception as exc:
                    self.logger.warning(
                        "DwellUseCase: zone geometry resolution raised on first frame (%s); starting background retry.",
                        exc,
                    )
                    self._start_geometry_resolver(config, stream_info)
            else:
                self.logger.info("DwellUseCase: no stream_info on first frame; using DwellConfig zone_config")

        # Use API-resolved geometry when available (thread-safe read).
        with self._geometry_lock:
            cached = self._resolved_geometry_cache
        if cached is not None:
            config = cached

        # Initialize the incident manager once, after zone resolution so the
        # config matches API-resolved zones when present.
        self._initialize_incident_manager_once(config)

        # ------------------------------------------------------------------ #
        # Detection pipeline                                                   #
        # ------------------------------------------------------------------ #
        input_format = match_results_structure(data)
        context.input_format = input_format
        context.confidence_threshold = config.confidence_threshold

        processed_data = filter_by_confidence(data, config.confidence_threshold)
        if config.index_to_category:
            processed_data = apply_category_mapping(processed_data, config.index_to_category)
        processed_data = [d for d in processed_data if d.get("category") in self.target_categories]

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
                    config, stream_info, profile=TrackerProfile.DEFAULT
                )
            processed_data = self.tracker.update(processed_data)
        except Exception as exc:
            self.logger.warning("AdvancedTracker failed: %s", exc)

        # Resolve canonical IDs BEFORE dwell checking so that _stationary_tracks
        # always keys on stable canonical IDs, not raw AdvancedTracker IDs that
        # can change across brief occlusions or tracker re-initialisations.
        processed_data = self._apply_canonical_ids(processed_data)

        dwell_data, dwell_alerts, presence_data = self._check_dwell_objects(processed_data, config, stream_info)
        # Track "person" (non-dwelling) and "Dweller" (dwelling) separately —
        # presence_data + dwell_data is a disjoint partition of processed_data
        # (same canonical track_ids/bboxes, just re-labelled by dwell state),
        # so this buckets current/total/new counts per category correctly.
        self._update_tracking_state(presence_data + dwell_data)
        self._total_frame_counter += 1

        frame_number = None
        if stream_info:
            input_settings = stream_info.get("input_settings", {})
            start_frame = input_settings.get("start_frame")
            end_frame = input_settings.get("end_frame")
            if start_frame is not None and end_frame is not None and start_frame == end_frame:
                frame_number = start_frame

        counting_summary = self._count_categories(dwell_data, config)
        total_counts = self.get_total_counts()
        counting_summary["total_counts"] = total_counts

        # Surface plain "person" (non-dwelling) bboxes alongside "Dweller"
        # in the detections list, so every in-zone person carries a bbox in
        # agg_summary. Appended after total_count/per_category_count are
        # already computed above (dwell-only), so incident/alert thresholds
        # — which key off those dwell-only totals — are unaffected.
        if presence_data:
            counting_summary["detections"] = counting_summary.get("detections", []) + [
                {
                    "bounding_box": det.get("bounding_box"),
                    "category": det.get("category"),
                    "confidence": det.get("confidence"),
                    "track_id": det.get("track_id"),
                    "frame_id": det.get("frame_id"),
                    "zone_name": det.get("zone_name"),
                    "dwell_seconds": det.get("dwell_seconds"),
                }
                for det in presence_data
            ]

        zone_analysis: Dict[str, Any] = {}
        if config.zone_config and config.zone_config.get("zones"):
            frame_data = processed_data
            zone_analysis = count_objects_in_zones(frame_data, config.zone_config["zones"])
            if zone_analysis:
                zone_analysis = self._update_zone_tracking(zone_analysis, dwell_data, config)

        alerts = self._check_alerts(counting_summary, zone_analysis, frame_number, config)
        self._extract_predictions(dwell_data)
        incidents_list = self._generate_incidents(
            counting_summary, zone_analysis, alerts, config, frame_number, stream_info
        )
        tracking_stats_list = self._generate_tracking_stats(
            counting_summary,
            zone_analysis,
            alerts,
            config,
            frame_number,
            stream_info,
            dwell_alerts,
            dwell_data,
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

        # Publish this frame's incident (or {}) to the IncidentManager so it can
        # own the open/close lifecycle. Pass context so the legacy bridge skips
        # duplicate incident_res publishing for this frame.
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
        self._debug_elapsed_since(start_time)
        return result

    # ------------------------------------------------------------------ #
    # Helpers — time / fps                                                #
    # ------------------------------------------------------------------ #

    def _get_fps(self, stream_info: Optional[Dict[str, Any]]) -> float:
        """Return frames-per-second from ``stream_info``, defaulting to 30.0."""
        if stream_info:
            fps = stream_info.get("input_settings", {}).get("original_fps")
            if fps and float(fps) > 0:
                return float(fps)
        return 30.0

    def _get_wall_time_from_stream(self, stream_info: Optional[Dict[str, Any]]) -> Optional[float]:
        """Parse the current frame wall-clock time from ``stream_info``.

        Checks ``stream_time`` at the root level first, then
        ``input_settings.stream_time``.  Returns a UTC float timestamp, or
        ``None`` if unparseable.
        """
        if not stream_info:
            return None
        raw = stream_info.get("stream_time") or stream_info.get("input_settings", {}).get("stream_time")
        if not raw:
            return None
        try:
            ts = str(raw).replace(" UTC", "")
            dt = datetime.strptime(ts, "%Y-%m-%d-%H:%M:%S.%f")
            return dt.replace(tzinfo=timezone.utc).timestamp()
        except Exception:
            return None

    # ------------------------------------------------------------------ #
    # Core dwell logic                                                    #
    # ------------------------------------------------------------------ #

    def _get_zone_for_bbox(
        self,
        bbox: Dict,
        zones: Optional[Dict[str, List[List[float]]]],
    ) -> Optional[str]:
        """Return the zone name whose polygon contains the person's foot center.

        Zone membership is determined by the **bottom-center** of the bounding
        box (the foot / floor contact point), which is more accurate than the
        geometric center for people standing on a floor plane.

        Returns
        -------
        str
            Name of the matching zone.
        ``"__global__"``
            When ``zones`` is ``None`` or empty (no zones configured) —
            the whole frame is treated as one zone so that dwell tracking
            still works without zone setup.
        ``None``
            When zones are configured but the foot center falls outside all
            defined polygons.  The caller must skip this detection entirely.
        """
        if not zones:
            return "__global__"
        foot_center = get_bbox_bottom_center(bbox)
        for zone_name, zone_polygon in zones.items():
            polygon_points = [(pt[0], pt[1]) for pt in zone_polygon]
            if point_in_polygon(foot_center, polygon_points):
                return zone_name
        return None

    def _check_dwell_objects(
        self,
        data: List[Dict],
        config: DwellConfig,
        stream_info: Optional[Dict[str, Any]],
    ) -> Tuple[List[Dict], List[Dict], List[Dict]]:
        """Classify detections as ``Dweller`` and emit per-person dwell alerts.

        Zone membership is determined by the person's **foot center** (bottom-
        center of the bounding box).  Detections whose foot center falls
        outside every configured zone are ignored entirely — no state is
        stored and no counting is done for them.

        All thresholds (``dwell_threshold``, ``loitering_time_threshold_seconds``,
        ``centroid_threshold``, ``movement_penalty``, ``stale_track_frames``)
        are resolved per-zone via ``_get_zone_param``, falling back to the
        global ``DwellConfig`` value when a zone-specific override is absent.

        All time-based decisions use wall-clock seconds derived from
        ``stream_info.stream_time`` so that the logic is completely independent
        of inference frame-rate.

        Returns
        -------
        dwell_data
            Subset of ``data`` whose tracks have been continuously stationary
            for at least ``dwell_threshold`` seconds.  Each entry gains two
            extra fields: ``zone_name`` (str) and ``dwell_seconds`` (float).
        dwell_alerts
            List of alert dicts for tracks whose ``dwell_seconds`` exceeded
            ``loitering_time_threshold_seconds`` for the first time this session.
        presence_data
            Every in-zone track that has **not yet** crossed ``dwell_threshold``,
            still labelled ``"person"``, each carrying ``bounding_box``,
            ``zone_name`` and its current (sub-threshold) ``dwell_seconds``.
            Kept separate from ``dwell_data`` so dwell-only aggregates
            (``dwell_durations``, ``zone_dwell_summary``, incident/alert
            thresholds) are unaffected — this list exists purely so callers can
            surface a bbox for every in-zone person, not just confirmed dwellers.
        """
        dwell_data: List[Dict] = []
        dwell_alerts: List[Dict] = []
        presence_data: List[Dict] = []
        current_wall_time = self._get_wall_time_from_stream(stream_info) or time.time()
        zones = config.zone_config.get("zones") if config.zone_config else None

        # Unique in-zone persons this frame (dwelling or not) — footfall/presence
        # count that drives the ``visitors_in_zone`` VOLUME metric.
        visitors_in_zone: Set[Any] = set()

        for det in data:
            if det.get("category") not in self.target_categories:
                continue
            track_id = det.get("track_id")
            bbox = det.get("bounding_box")
            if not track_id or not bbox:
                continue

            # Resolve zone using foot center (bottom-center of bbox).
            zone_name = self._get_zone_for_bbox(bbox, zones)

            # Person is outside all defined zones — no operations at all.
            if zone_name is None:
                continue

            # Count every in-zone person (present in the monitored area now).
            visitors_in_zone.add(track_id)

            # Resolve per-zone thresholds — all expressed in seconds.
            z_centroid_threshold: float = self._get_zone_param(zone_name, "centroid_threshold", config)
            z_dwell_threshold: float = self._get_zone_param(zone_name, "dwell_threshold", config)
            z_movement_penalty: float = self._get_zone_param(zone_name, "movement_penalty", config)
            z_loitering_threshold: float = self._get_zone_param(zone_name, "loitering_time_threshold_seconds", config)

            centroid = self._calculate_centroid(bbox)

            if track_id not in self._stationary_tracks:
                # First time seeing this track — initialise wall-clock state.
                self._stationary_tracks[track_id] = {
                    "centroid": centroid,
                    "start_wall_time": current_wall_time,  # reset on movement
                    "dwell_start_wall_time": None,
                    "last_seen_time": current_wall_time,  # updated every call
                    "bbox": bbox,
                    "zone_name": zone_name,
                }
            else:
                track_info = self._stationary_tracks[track_id]
                prev_centroid = track_info["centroid"]
                track_info["last_seen_time"] = current_wall_time
                track_info["bbox"] = bbox
                track_info["zone_name"] = zone_name

                if self._is_centroid_stationary(centroid, prev_centroid, z_centroid_threshold):
                    # Person is stationary — nothing to reset.
                    pass
                else:
                    # Movement detected: penalise accumulated stationary time
                    # by subtracting movement_penalty (seconds) from start_wall_time.
                    # Clamped so start_wall_time never goes ahead of current time.
                    elapsed = current_wall_time - track_info["start_wall_time"]
                    remaining = max(0.0, elapsed - z_movement_penalty)
                    track_info["start_wall_time"] = current_wall_time - remaining
                    track_info["dwell_start_wall_time"] = None

                track_info["centroid"] = centroid

            track_info = self._stationary_tracks[track_id]

            # Stationary time = wall-clock seconds since start_wall_time was last reset.
            stationary_seconds = current_wall_time - track_info["start_wall_time"]

            if stationary_seconds >= z_dwell_threshold:
                if track_info["dwell_start_wall_time"] is None:
                    track_info["dwell_start_wall_time"] = current_wall_time

                dwell_secs = round(stationary_seconds, 2)

                self._track_dwell_seconds[track_id] = dwell_secs
                self._zone_unique_dwellers.setdefault(zone_name, set()).add(track_id)

                det = dict(det)  # shallow copy — do not mutate upstream data
                det["category"] = "Dweller"
                det["zone_name"] = zone_name
                det["dwell_seconds"] = dwell_secs
                dwell_data.append(det)

                # Per-person dwell alert — fires exactly once per track per session.
                if dwell_secs >= z_loitering_threshold and track_id not in self._loitering_alerted_tracks:
                    self._loitering_alerted_tracks.add(track_id)
                    dwell_alerts.append(
                        {
                            "alert_type": "dwell",
                            "track_id": track_id,
                            "zone_name": zone_name,
                            "dwell_seconds": dwell_secs,
                            "threshold_seconds": z_loitering_threshold,
                            "timestamp": self._format_timestamp(current_wall_time),
                        }
                    )
                    self.logger.warning(
                        "DwellUseCase: dwell alert — track_id=%s zone=%s dwell_seconds=%.1f threshold=%.1f",
                        track_id,
                        zone_name,
                        dwell_secs,
                        z_loitering_threshold,
                    )
            else:
                # Not yet dwelling — still emit a plain "person" detection (with
                # bbox) so agg_summary/detections can carry a box for every
                # in-zone person, not just those who have crossed the dwell
                # threshold. Routed separately from ``dwell_data`` so
                # dwell-only aggregates (dwell_durations, zone_dwell_summary,
                # incident/alert count thresholds) are unaffected.
                det = dict(det)  # shallow copy — do not mutate upstream data
                det["zone_name"] = zone_name
                det["dwell_seconds"] = round(stationary_seconds, 2)
                presence_data.append(det)

        # Snapshot the footfall count for this frame (read by _generate_tracking_stats).
        self._last_visitors_in_zone = len(visitors_in_zone)

        # ------------------------------------------------------------------ #
        # Evict stale tracks using wall-clock time (zone-specific seconds)    #
        # ------------------------------------------------------------------ #
        stale_ids = [
            tid
            for tid, info in self._stationary_tracks.items()
            if current_wall_time - info.get("last_seen_time", current_wall_time)
            > self._get_zone_param(info.get("zone_name", "__global__"), "stale_track_frames", config)
        ]
        for tid in stale_ids:
            del self._stationary_tracks[tid]
        if stale_ids:
            self.logger.debug("DwellUseCase: evicted %d stale track(s): %s", len(stale_ids), stale_ids)

        return dwell_data, dwell_alerts, presence_data

    def _calculate_centroid(self, bbox: Dict) -> tuple:
        """Return (cx, cy) for an axis-aligned bounding box dict."""
        if "xmin" in bbox:
            x = (bbox["xmin"] + bbox["xmax"]) / 2
            y = (bbox["ymin"] + bbox["ymax"]) / 2
        elif "x1" in bbox:
            x = (bbox["x1"] + bbox["x2"]) / 2
            y = (bbox["y1"] + bbox["y2"]) / 2
        else:
            return (0, 0)
        return (x, y)

    def _is_centroid_stationary(self, centroid: tuple, prev_centroid: tuple, threshold: float) -> bool:
        """Return True when Euclidean distance between centroids is below ``threshold`` pixels."""
        x1, y1 = centroid
        x2, y2 = prev_centroid
        distance = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
        return distance < threshold

    def _is_in_zone(self, bbox: Dict, zones: Optional[Dict[str, List[List[float]]]]) -> bool:
        """Legacy helper — returns True if the foot center is inside any zone (or zones is None)."""
        return self._get_zone_for_bbox(bbox, zones) is not None

    # ------------------------------------------------------------------ #
    # Zone tracking                                                       #
    # ------------------------------------------------------------------ #

    def _update_zone_tracking(
        self,
        zone_analysis: Dict[str, Dict[str, int]],
        detections: List[Dict],
        config: DwellConfig,
    ) -> Dict[str, Dict[str, Any]]:
        """Enrich ``zone_analysis`` with cumulative track-ID sets and dwell metrics."""
        zones = config.zone_config.get("zones") if config.zone_config else {}
        if not zone_analysis or not zones:
            return {}

        enhanced: Dict[str, Any] = {}
        current_frame_zone_tracks: Dict[str, set] = {zn: set() for zn in zones}

        for zn in zones:
            self._zone_current_track_ids.setdefault(zn, set())
            self._zone_total_track_ids.setdefault(zn, set())

        for det in detections:
            track_id = det.get("track_id")
            if track_id is None:
                continue
            bbox = det.get("bounding_box")
            if not bbox:
                continue
            zone_name = det.get("zone_name") or self._get_zone_for_bbox(bbox, zones)
            if zone_name and zone_name != "__global__" and zone_name in current_frame_zone_tracks:
                current_frame_zone_tracks[zone_name].add(track_id)

        for zone_name, zone_counts in zone_analysis.items():
            current_tracks = current_frame_zone_tracks.get(zone_name, set())
            self._zone_current_track_ids[zone_name] = current_tracks
            self._zone_total_track_ids[zone_name].update(current_tracks)
            self._zone_current_counts[zone_name] = len(current_tracks)
            self._zone_total_counts[zone_name] = len(self._zone_total_track_ids[zone_name])
            enhanced[zone_name] = {
                "current_count": self._zone_current_counts[zone_name],
                "total_count": self._zone_total_counts[zone_name],
                "current_track_ids": list(current_tracks),
                "total_track_ids": list(self._zone_total_track_ids[zone_name]),
                "original_counts": zone_counts,
            }

        return enhanced

    # ------------------------------------------------------------------ #
    # Dwell metrics computation                                           #
    # ------------------------------------------------------------------ #

    def _compute_zone_dwell_summary(self, dwell_data: List[Dict]) -> Dict[str, Dict[str, Any]]:
        """Build per-zone dwell statistics from current-frame dwell detections.

        Returns
        -------
        dict mapping zone_name to::

            {
              "unique_dwellers":   int,   # cumulative unique dwellers in zone
              "current_dwell_count": int, # dwellers this frame
              "avg_dwell_seconds": float, # mean over all known dwell durations
            }
        """
        summary: Dict[str, Dict[str, Any]] = {}

        # Compute per-zone current count
        zone_current: Dict[str, int] = {}
        for det in dwell_data:
            zn = det.get("zone_name", "__global__")
            zone_current[zn] = zone_current.get(zn, 0) + 1

        # Aggregate over all zones that have ever seen a dweller
        all_zones = set(self._zone_unique_dwellers.keys()) | set(zone_current.keys())
        for zn in all_zones:
            unique_ids = self._zone_unique_dwellers.get(zn, set())
            dwell_times = [self._track_dwell_seconds[tid] for tid in unique_ids if tid in self._track_dwell_seconds]
            avg = round(sum(dwell_times) / len(dwell_times), 2) if dwell_times else 0.0
            summary[zn] = {
                "unique_dwellers": len(unique_ids),
                "current_dwell_count": zone_current.get(zn, 0),
                "avg_dwell_seconds": avg,
            }

        return summary

    # ------------------------------------------------------------------ #
    # Alert checking                                                      #
    # ------------------------------------------------------------------ #

    def _check_alerts(
        self,
        summary: dict,
        _zone_analysis: Dict,
        frame_number: Any,
        config: DwellConfig,
    ) -> List[Dict]:
        _ = (_zone_analysis,)

        def get_trend(entries: List[Tuple[float, int]], window_seconds: float = 30.0, threshold: float = 0.6) -> bool:
            """Return True when severity values have been predominantly increasing
            over the last ``window_seconds`` of elapsed time.  FPS-independent.

            monotonic(), matching how ``_ascending_alert_entries`` is stamped in
            _generate_incidents: this is an elapsed-time window, so a wall-clock
            step must not change which observations fall inside it.
            """
            cutoff = time.monotonic() - window_seconds
            window = [v for t, v in entries if t >= cutoff]
            if len(window) < 2:
                return True
            increasing = sum(1 for i in range(1, len(window)) if window[i] >= window[i - 1])
            return (increasing / (len(window) - 1)) >= threshold

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
                            "ascending": get_trend(self._ascending_alert_entries),
                            "settings": {
                                t: v
                                for t, v in zip(
                                    getattr(config.alert_config, "alert_type", ["Default"]),
                                    getattr(config.alert_config, "alert_value", ["JSON"]),
                                )
                            },
                        }
                    )
                elif category == "Dweller" and per_category_count.get(category, 0) > threshold:
                    alerts.append(
                        {
                            "alert_type": getattr(config.alert_config, "alert_type", ["Default"]),
                            "alert_id": f"alert_{category}_{frame_key}",
                            "incident_category": self.CASE_TYPE,
                            "threshold_level": threshold,
                            "ascending": get_trend(self._ascending_alert_entries),
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
    # Incident generation                                                 #
    # ------------------------------------------------------------------ #

    def _generate_incidents(
        self,
        counting_summary: Dict,
        _zone_analysis: Dict,
        alerts: List,
        config: DwellConfig,
        frame_number: Optional[int] = None,
        stream_info: Optional[Dict[str, Any]] = None,
    ) -> List[Dict]:
        _ = (_zone_analysis,)
        incidents = []
        # Incidents fire on Dweller presence specifically, not on every visitor
        # in the zone — a plain "person" who never dwells long enough to be
        # promoted to "Dweller" should not trigger an incident.
        per_category_count = counting_summary.get("per_category_count", {})
        total_detections = per_category_count.get("Dweller", 0)
        current_timestamp = self._get_current_timestamp_str(stream_info)
        camera_info = self.get_camera_info_from_stream(stream_info)

        # monotonic(): this stamps _ascending_alert_entries and drives the trim
        # window below, both pure elapsed-time measurements read back by
        # get_trend(). Wall-clock timestamps for display come from
        # _get_wall_time_from_stream()/now_wall, which are deliberately separate.
        now = time.monotonic()
        # Trim entries older than 5 minutes to bound memory usage regardless of
        # how long the stream has been running.
        _5min_ago = now - 300.0
        self._ascending_alert_entries = [(t, v) for t, v in self._ascending_alert_entries if t >= _5min_ago]

        # Build per-zone Dweller breakdown from current detections
        dwell_person_zones: Dict[str, int] = {}
        for det in counting_summary.get("detections", []):
            if det.get("category") == "Dweller":
                zn = det.get("zone_name", "__global__")
                dwell_person_zones[zn] = dwell_person_zones.get(zn, 0) + 1

        # Wall-clock time + cooldown drive episode segmentation (FPS-independent).
        now_wall = self._get_wall_time_from_stream(stream_info) or time.time()
        cooldown = float(getattr(config, "incident_cooldown_seconds", 60.0) or 0.0)
        rank_to_level = {0: "low", 1: "medium", 2: "significant", 3: "critical"}
        level_to_rank = {"low": 0, "medium": 1, "significant": 2, "critical": 3}

        if total_detections > 0:
            start_timestamp = self._get_start_timestamp_str(stream_info)
            self._debug_stream_timing("start_timestamp", start_timestamp)

            # ---- Episode segmentation (cooldown) ---------------------------- #
            # A NEW incident begins only when no episode is active, or when dwell
            # had stopped for longer than the cooldown (the previous episode is
            # considered closed). Otherwise this frame continues the SAME incident,
            # so we do not spawn a new incident every frame.
            gap = now_wall - self._dwell_last_active_wall
            is_new_incident = (not self._dwell_incident_active) or (
                self._dwell_last_active_wall > 0.0 and gap > cooldown
            )
            if is_new_incident:
                self._dwell_episode_id += 1
                self._dwell_incident_active = True
                self._dwell_episode_start_ts = start_timestamp or current_timestamp
                self._dwell_episode_max_rank = -1
                self._dwell_episode_max_quant = 0.0
            self._dwell_last_active_wall = now_wall

            # ---- Current-frame severity ------------------------------------- #
            if config.alert_config and config.alert_config.count_thresholds:
                threshold = config.alert_config.count_thresholds.get("all", 15)
                intensity = min(10.0, (total_detections / threshold) * 10)
                if intensity >= 9:
                    level = "critical"
                elif intensity >= 7:
                    level = "significant"
                elif intensity >= 5:
                    level = "medium"
                else:
                    level = "low"
            else:
                if total_detections > 30:
                    level = "critical"
                elif total_detections > 25:
                    level = "significant"
                elif total_detections > 15:
                    level = "medium"
                else:
                    level = "low"

            # Keep severity non-decreasing across the episode so the published
            # level never flaps down frame-to-frame (avoids republish churn).
            self._dwell_episode_max_rank = max(self._dwell_episode_max_rank, level_to_rank[level])
            level = rank_to_level[self._dwell_episode_max_rank]
            self._ascending_alert_entries.append((now, self._dwell_episode_max_rank))

            zone_lines = "\n".join(f"\t  {zn}: {cnt} Dweller(s)" for zn, cnt in dwell_person_zones.items())
            human_text_lines = [f"DWELL DETECTED @ {current_timestamp}:"]
            human_text_lines.append(f"\tSeverity Level: {(self.CASE_TYPE, level)}")
            if zone_lines:
                human_text_lines.append(f"\tZone Breakdown:\n{zone_lines}")
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

            # incident_quant = (Dweller_count / count_threshold) * 100, matching
            # the count_ratio strategy in dwell-detection.yaml. IncidentManager
            # re-derives severity from this value using deployment thresholds.
            if config.alert_config and config.alert_config.count_thresholds:
                count_threshold = config.alert_config.count_thresholds.get("all", 1) or 1
            else:
                count_threshold = 1
            incident_quant = min(100.0, (total_detections / count_threshold) * 100.0) if count_threshold else 0.0
            # Hold non-decreasing across the episode so the manager-derived severity
            # (and thus republishing) is stable while the same incident is ongoing.
            self._dwell_episode_max_quant = max(self._dwell_episode_max_quant, incident_quant)
            incident_quant = self._dwell_episode_max_quant

            self.current_incident_end_timestamp = "Incident still active"
            event = self.create_incident(
                # Stable incident_id for the whole episode (not per-frame), so the
                # ongoing dwell reads as one unique incident.
                incident_id=f"{self.CASE_TYPE}_{self._dwell_episode_id}",
                incident_type=self.CASE_TYPE,
                severity_level=level,
                human_text=human_text,
                camera_info=camera_info,
                alerts=alerts,
                alert_settings=alert_settings,
                start_time=self._dwell_episode_start_ts,
                end_time=self.current_incident_end_timestamp,
                level_settings={"low": 1, "medium": 3, "significant": 4, "critical": 7},
            )
            # Attach zone breakdown directly on the incident dict
            event["dwell_person_zones"] = dwell_person_zones
            # incident_quant drives IncidentManager severity (count_ratio strategy).
            event["incident_quant"] = round(incident_quant, 2)
            # Snapshot so the episode can be held across brief dropouts and closed
            # (with a real end_time) once dwell stops for longer than the cooldown.
            self._dwell_last_incident = dict(event)
            incidents.append(event)
        else:
            self._ascending_alert_entries.append((now, 0))
            if self._dwell_incident_active and self._dwell_last_incident is not None:
                gap = now_wall - self._dwell_last_active_wall
                if gap <= cooldown:
                    # Brief detection dropout within the cooldown — keep the SAME
                    # incident alive (re-emit last snapshot) so a momentary miss
                    # does not split one dwell into several incidents.
                    incidents.append(dict(self._dwell_last_incident))
                else:
                    # Dwell has stopped for longer than the cooldown — close the
                    # episode once (real end_time), then reset so the next dwell is
                    # a brand-new incident and the cooldown starts over.
                    closing = dict(self._dwell_last_incident)
                    closing["severity_level"] = "info"
                    closing["end_time"] = current_timestamp
                    self.current_incident_end_timestamp = current_timestamp
                    self._dwell_incident_active = False
                    self._dwell_last_incident = None
                    self._dwell_episode_max_rank = -1
                    incidents.append(closing)
            else:
                self.current_incident_end_timestamp = "N/A"
                incidents.append({})

        return incidents

    # ------------------------------------------------------------------ #
    # Tracking stats generation                                           #
    # ------------------------------------------------------------------ #

    def _generate_tracking_stats(
        self,
        counting_summary: Dict,
        zone_analysis: Dict,
        alerts: List,
        config: DwellConfig,
        _frame_number: Optional[int] = None,
        stream_info: Optional[Dict[str, Any]] = None,
        dwell_alerts: Optional[List[Dict]] = None,
        dwell_data: Optional[List[Dict]] = None,
    ) -> List[Dict]:
        """Generate tracking statistics including dwell durations and zone dwell summary."""
        _ = (_frame_number,)
        camera_info = self.get_camera_info_from_stream(stream_info)
        tracking_stats = []
        total_counts_dict = counting_summary.get("total_counts", {})
        per_category_count = counting_summary.get("per_category_count", {})
        current_timestamp = self._get_current_timestamp_str(stream_info, precision=False)
        start_timestamp = self._get_start_timestamp_str(stream_info, precision=False)
        self._debug_stream_timing("start_timestamp", start_timestamp)
        high_precision_start_timestamp = self._get_current_timestamp_str(stream_info, precision=True)
        high_precision_reset_timestamp = self._get_start_timestamp_str(stream_info, precision=True)

        # Always emit both "person" and "Dweller" — even at 0 — so consumers
        # never have to guess whether a category was simply absent this frame.
        current_frame_ids = getattr(self, "_current_frame_track_ids", {})
        total_counts = [{"category": cat, "count": total_counts_dict.get(cat, 0)} for cat in ("person", "Dweller")]
        current_counts = [
            {"category": cat, "count": len(current_frame_ids.get(cat, set()))} for cat in ("person", "Dweller")
        ]

        # ---- Detection objects with zone_name ----
        detections = []
        for detection in counting_summary.get("detections", []):
            bbox = detection.get("bounding_box", {})
            category = detection.get("category", "Dweller")
            zone_name = detection.get("zone_name", None)
            detection_obj = self.create_detection_object(category, bbox, track_id=detection.get("track_id"))
            if zone_name:
                detection_obj["zone_name"] = zone_name
            detections.append(detection_obj)

        # ---- Per-person dwell durations ----
        dwell_durations = []
        for det in dwell_data or []:
            tid = det.get("track_id")
            dwell_durations.append(
                {
                    "track_id": tid,
                    "dwell_seconds": det.get("dwell_seconds", 0.0),
                    "zone_name": det.get("zone_name", "__global__"),
                }
            )

        # ---- Zone dwell summary ----
        zone_dwell_summary = self._compute_zone_dwell_summary(dwell_data or [])

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

        # ---- Human-readable text ----
        human_text_lines = ["Tracking Statistics:"]
        human_text_lines.append(f"CURRENT FRAME @ {current_timestamp}")
        if zone_analysis:
            human_text_lines.append("\tZones (current dwell):")
            for zone_name, zone_data in zone_dwell_summary.items():
                human_text_lines.append(
                    f"\t  {zone_name}: {zone_data['current_dwell_count']} dwelling "
                    f"(avg {zone_data['avg_dwell_seconds']:.1f}s, "
                    f"{zone_data['unique_dwellers']} unique)"
                )
        else:
            for entry in current_counts:
                cat, count = entry["category"], entry["count"]
                if count > 0:
                    human_text_lines.append(f"\t- {count} {cat.replace('_', ' ')} detected")
                else:
                    human_text_lines.append(f"\t- No {cat.replace('_', ' ')} detections")
        human_text_lines.append(f"TOTAL SINCE {start_timestamp}")
        if zone_analysis:
            human_text_lines.append("\tZones (total unique dwellers):")
            for zone_name, zone_data in zone_dwell_summary.items():
                human_text_lines.append(f"\t  {zone_name}: {zone_data['unique_dwellers']}")
        else:
            for cat, count in total_counts_dict.items():
                if count > 0:
                    human_text_lines.append(f"\t{cat}: {count}")
        if dwell_alerts:
            for da in dwell_alerts:
                human_text_lines.append(
                    f"DWELL ALERT: track_id={da['track_id']} zone={da['zone_name']} "
                    f"dwell={da['dwell_seconds']}s > {da['threshold_seconds']}s @ {da['timestamp']}"
                )
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
        # Attach new dwell-specific metrics
        tracking_stat["dwell_durations"] = dwell_durations
        tracking_stat["zone_dwell_summary"] = zone_dwell_summary
        tracking_stat["dwell_alerts"] = dwell_alerts or []

        # ------------------------------------------------------------------ #
        # VOLUME analytics fields (consumed by legacy_analytics_bridge)       #
        # ------------------------------------------------------------------ #
        # current_new_counts (even zeros) prevents ANALYTICS_WARN spam and lets
        # the bridge derive footfall/entry counts; total_current_counts mirrors
        # current_counts as the in-frame snapshot.
        new_counts = self.get_new_counts_this_frame()
        tracking_stat["current_new_counts"] = [
            {"category": cat, "count": int(new_counts.get(cat, 0))} for cat in ("person", "Dweller")
        ]
        tracking_stat["total_current_counts"] = current_counts

        # Compact dwell metric block read directly by the bridge (same pattern as
        # parking_analytics). All five keys match dwell-analytics-metrics.json.
        all_dwell_secs = list(self._track_dwell_seconds.values())
        tracking_stat["dwell_analytics"] = {
            "visitors_in_zone": int(self._last_visitors_in_zone),
            "active_dwellers": int(per_category_count.get("Dweller", 0)),
            "unique_dwellers": int(self.get_total_counts().get("Dweller", 0)),
            "avg_dwell_time_seconds": (round(sum(all_dwell_secs) / len(all_dwell_secs), 2) if all_dwell_secs else 0.0),
            "max_dwell_time_seconds": round(max(all_dwell_secs), 2) if all_dwell_secs else 0.0,
        }

        tracking_stats.append(tracking_stat)
        return tracking_stats

    # ------------------------------------------------------------------ #
    # Business analytics + summary (unchanged)                           #
    # ------------------------------------------------------------------ #

    def _generate_business_analytics(
        self,
        _counting_summary: Dict,
        _zone_analysis: Dict,
        _alerts: Any,
        _config: DwellConfig,
        _stream_info: Optional[Dict[str, Any]] = None,
        is_empty=False,
    ) -> List[Dict]:
        _ = (_alerts, _config, _counting_summary, _stream_info, _zone_analysis)
        if is_empty:
            return []
        return []

    def _generate_summary(
        self,
        _summary: dict,
        _zone_analysis: Dict,
        incidents: List,
        tracking_stats: List,
        business_analytics: List,
        _alerts: List,
    ) -> List[str]:
        _ = (_alerts, _summary, _zone_analysis)
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
        if not incidents and not tracking_stats and not business_analytics:
            lines["Summary"] = "No Summary Data"
        return ["\n".join(f"{k}: {v}" for k, v in lines.items())]

    # ------------------------------------------------------------------ #
    # Track management helpers                                           #
    # ------------------------------------------------------------------ #

    def _get_track_ids_info(self, detections: list) -> Dict[str, Any]:
        current_track_ids = {det.get("track_id") for det in detections if det.get("track_id") is not None}
        total_track_ids: set = set()
        for s in getattr(self, "_per_category_total_track_ids", {}).values():
            total_track_ids.update(s)
        return {
            "total_count": len(total_track_ids),
            "current_detection_count": len(current_track_ids),
            "total_unique_track_ids": len(total_track_ids),
            "current_detection_track_ids": list(current_track_ids),
            "last_update_time": time.time(),
            "total_inferences_processed": getattr(self, "_total_frame_counter", 0),
        }

    def _update_tracking_state(self, detections: list) -> None:
        categories = self.target_categories + ["Dweller"]
        if not hasattr(self, "_per_category_total_track_ids"):
            self._per_category_total_track_ids = {cat: set() for cat in categories}
        self._current_frame_track_ids = {cat: set() for cat in categories}
        # Track ids appearing for the FIRST time this frame (drives current_new_counts).
        self._new_track_ids_this_frame = {cat: set() for cat in categories}

        for det in detections:
            cat = det.get("category")
            raw_track_id = det.get("track_id")
            if cat not in categories or raw_track_id is None:
                continue
            bbox = det.get("bounding_box", det.get("bbox"))
            canonical_id = self._merge_or_register_track(raw_track_id, bbox)
            det["track_id"] = canonical_id
            total_set = self._per_category_total_track_ids.setdefault(cat, set())
            if canonical_id not in total_set:
                # First time this category has ever seen this track id.
                self._new_track_ids_this_frame.setdefault(cat, set()).add(canonical_id)
            total_set.add(canonical_id)
            self._current_frame_track_ids[cat].add(canonical_id)

    def get_new_counts_this_frame(self) -> Dict[str, int]:
        """Count of track ids reported for the FIRST time this frame, per category."""
        return {cat: len(ids) for cat, ids in getattr(self, "_new_track_ids_this_frame", {}).items()}

    def get_total_counts(self) -> Dict[str, int]:
        """Return cumulative unique counts for both ``"person"`` and ``"Dweller"``.

        ``"person"`` — every unique in-zone track ever seen while NOT yet
        dwelling, sourced from ``_per_category_total_track_ids["person"]``
        (populated by ``_update_tracking_state`` from ``presence_data``).
        ``"Dweller"`` — unique tracks ever promoted past the dwell threshold,
        sourced from ``_zone_unique_dwellers`` (populated by
        ``_check_dwell_objects()`` whenever a track crosses the threshold).

        Both keys are always present, defaulting to 0, so callers never need
        to guess whether a category was tracked yet.
        """
        all_dwell_ids: set = set()
        for ids in self._zone_unique_dwellers.values():
            all_dwell_ids.update(ids)
        person_ids = getattr(self, "_per_category_total_track_ids", {}).get("person", set())
        return {"person": len(person_ids), "Dweller": len(all_dwell_ids)}

    # ------------------------------------------------------------------ #
    # Timestamp helpers                                                   #
    # ------------------------------------------------------------------ #

    def _format_timestamp_for_stream(self, timestamp: float) -> str:
        dt = datetime.fromtimestamp(timestamp, tz=timezone.utc)
        return dt.strftime("%Y:%m:%d %H:%M:%S")

    def _format_timestamp_for_video(self, timestamp: float) -> str:
        hours = int(timestamp // 3600)
        minutes = int((timestamp % 3600) // 60)
        seconds = round(float(timestamp % 60), 2)
        return f"{hours:02d}:{minutes:02d}:{seconds:.1f}"

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
                self.start_timer = stream_info.get("input_settings", {}).get("stream_time", "NA")
                return self._format_timestamp(self.start_timer)
            elif stream_info.get("input_settings", {}).get("start_frame", "na") == 1:
                self.start_timer = stream_info.get("input_settings", {}).get("stream_time", "NA")
                return self._format_timestamp(self.start_timer)
            else:
                return self._format_timestamp(self.start_timer)

        if self.start_timer is None:
            self.start_timer = stream_info.get("input_settings", {}).get("stream_time", "NA")
            return self._format_timestamp(self.start_timer)
        elif stream_info.get("input_settings", {}).get("start_frame", "na") == 1:
            self.start_timer = stream_info.get("input_settings", {}).get("stream_time", "NA")
            return self._format_timestamp(self.start_timer)
        else:
            if self.start_timer is not None:
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

    # ------------------------------------------------------------------ #
    # Count / prediction helpers                                         #
    # ------------------------------------------------------------------ #

    def _count_categories(self, detections: list, _config: DwellConfig) -> dict:
        _ = (_config,)
        counts: Dict[str, int] = {}
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
                    "zone_name": det.get("zone_name"),
                    "dwell_seconds": det.get("dwell_seconds"),
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

    # ------------------------------------------------------------------ #
    # Track alias / IoU merging                                          #
    # ------------------------------------------------------------------ #

    def _apply_canonical_ids(self, detections: List[Dict]) -> List[Dict]:
        """Replace each detection's raw tracker ID with a stable canonical ID.

        Called on the full ``processed_data`` list before ``_check_dwell_objects``
        so that ``_stationary_tracks`` always keys on canonical IDs.  Without this
        pre-pass, a tracker re-assignment (occlusion, brief exit) would create a
        new entry in ``_stationary_tracks`` and reset the accumulated stationary
        time for a person who was already mid-dwell.
        """
        result: List[Dict] = []
        for det in detections:
            raw_id = det.get("track_id")
            bbox = det.get("bounding_box")
            if raw_id is not None and bbox is not None:
                canonical_id = self._merge_or_register_track(raw_id, bbox)
                if canonical_id != raw_id:
                    det = dict(det)  # shallow copy — never mutate upstream data
                    det["track_id"] = canonical_id
            result.append(det)
        return result

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
        """Return a stable canonical track ID for ``raw_id``.

        Re-associates a new raw tracker ID with an existing canonical track when
        the bounding boxes are close enough, preserving dwell history across
        brief tracker re-assignments (occlusions, detector jitter).

        Match criteria (either is sufficient):
          * IoU  ≥ ``_track_merge_iou_threshold`` (0.20)
          * centre-distance < 35 px  AND  size-ratio > 0.60
        """
        if raw_id is None or bbox is None:
            return raw_id
        # monotonic(): "last_update" is written and compared only inside this
        # method, purely to age entries out of _canonical_tracks after
        # _track_merge_time_window elapsed seconds. A wall-clock step backwards
        # would otherwise strand aliases indefinitely (the pool never expires),
        # and a step forwards would flush them all and break re-identification.
        now = time.monotonic()

        # Fast path — already aliased.
        if raw_id in self._track_aliases:
            canonical_id = self._track_aliases[raw_id]
            track_info = self._canonical_tracks.get(canonical_id)
            if track_info is not None:
                track_info["last_bbox"] = bbox
                track_info["last_update"] = now
                track_info["raw_ids"].add(raw_id)
            return canonical_id

        # Evict stale canonical tracks before searching for a merge partner.
        # Without this, dead entries accumulate indefinitely and can incorrectly
        # absorb new detections whose bboxes happen to overlap the old position.
        stale = [
            cid
            for cid, info in self._canonical_tracks.items()
            if now - info["last_update"] > self._track_merge_time_window
        ]
        for cid in stale:
            del self._canonical_tracks[cid]

        # Normalise bbox to dict with xmin/ymin/xmax/ymax for helper functions.
        def _as_dict(b: Any) -> Optional[Dict[str, float]]:
            if isinstance(b, dict):
                if "xmin" in b:
                    return b
                if "x1" in b:
                    return {"xmin": b["x1"], "ymin": b["y1"], "xmax": b["x2"], "ymax": b["y2"]}
            if isinstance(b, (list, tuple)) and len(b) >= 4:
                return {"xmin": b[0], "ymin": b[1], "xmax": b[2], "ymax": b[3]}
            return None

        bbox_d = _as_dict(bbox)

        # Search active canonical tracks for a merge partner.
        for canonical_id, info in self._canonical_tracks.items():
            prev = _as_dict(info["last_bbox"])
            if prev is None or bbox_d is None:
                continue

            iou = self._compute_iou(bbox_d, prev)

            # Centre-distance
            cx1 = (prev["xmin"] + prev["xmax"]) / 2
            cy1 = (prev["ymin"] + prev["ymax"]) / 2
            cx2 = (bbox_d["xmin"] + bbox_d["xmax"]) / 2
            cy2 = (bbox_d["ymin"] + bbox_d["ymax"]) / 2
            centre_dist = ((cx1 - cx2) ** 2 + (cy1 - cy2) ** 2) ** 0.5

            # Size-ratio (how similar the bbox areas are)
            area1 = (prev["xmax"] - prev["xmin"]) * (prev["ymax"] - prev["ymin"])
            area2 = (bbox_d["xmax"] - bbox_d["xmin"]) * (bbox_d["ymax"] - bbox_d["ymin"])
            size_ratio = (min(area1, area2) / max(area1, area2)) if max(area1, area2) > 0 else 0.0

            if iou >= self._track_merge_iou_threshold or (centre_dist < 35 and size_ratio > 0.6):
                self._track_aliases[raw_id] = canonical_id
                info["last_bbox"] = bbox
                info["last_update"] = now
                info["raw_ids"].add(raw_id)
                return canonical_id

        # No match — register a new canonical track.
        canonical_id = raw_id
        self._track_aliases[raw_id] = canonical_id
        self._canonical_tracks[canonical_id] = {
            "last_bbox": bbox,
            "last_update": now,
            "raw_ids": {raw_id},
        }
        return canonical_id

    # ------------------------------------------------------------------ #
    # Timestamp formatting                                                #
    # ------------------------------------------------------------------ #

    def _format_timestamp(self, timestamp: Any) -> str:
        """Format a timestamp to exactly two fractional-second digits.

        Accepts a numeric Unix timestamp or a string in the format
        ``YYYY-MM-DD-HH:MM:SS.ffffff UTC``.

        Example::

            >>> self._format_timestamp("2025-08-19-04:22:47.187574 UTC")
            '2025-08-19-04:22:47.18 UTC'
        """
        if isinstance(timestamp, (int, float)):
            timestamp = datetime.fromtimestamp(timestamp, timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")
        if not isinstance(timestamp, str):
            return str(timestamp)
        if "." not in timestamp:
            return timestamp
        main_part, fractional_and_suffix = timestamp.split(".", 1)
        if " " in fractional_and_suffix:
            fractional_part, suffix = fractional_and_suffix.split(" ", 1)
            suffix = " " + suffix
        else:
            fractional_part, suffix = fractional_and_suffix, ""
        fractional_part = (fractional_part + "00")[:2]
        return f"{main_part}.{fractional_part}{suffix}"

    def _get_tracking_start_time(self) -> str:
        if self._tracking_start_time is None:
            return "N/A"
        return self._format_timestamp(self._tracking_start_time)

    def _set_tracking_start_time(self) -> None:
        self._tracking_start_time = time.time()
