"""
Advanced customer service use case implementation.

This module provides comprehensive customer service analytics with advanced tracking,
journey analysis, queue management, and detailed business intelligence metrics.
"""

import re
import threading
import time
import uuid
from collections import defaultdict
from dataclasses import replace
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

from ..core.base import (
    BaseProcessor,
    ConfigProtocol,
    ProcessingContext,
    ProcessingResult,
)
from ..core.config import CustomerServiceConfig, ZoneConfig
from ..Trackers import ConfigDrivenTracker, TrackerProfile
from ..utils import (
    BBoxSmoothingConfig,
    BBoxSmoothingTracker,
    apply_category_mapping,
    bbox_smoothing,
    filter_by_confidence,
    get_bbox_center,
    match_results_structure,
    point_in_polygon,
)
from ..utils.geometry_utils import to_zone_test_point
from ..utils.post_processing_config_client import (
    GEOMETRY_RETRY_INTERVAL,
    PostProcessingConfigClient,
)

# Counter zones arrive as one flat ``zone_config.zones`` dict and are split by
# name prefix into paired staff/customer polygons: ``staff_1`` pairs with
# ``customer_1``, ``staff_2`` with ``customer_2``, and so on. One counter == one
# pair, so the suffix is the counter id.
_ZONE_NAME_RE = re.compile(r"^(staff|customer)_(\d+)$")
_STAFF_ROLE = "staff"
_CUSTOMER_ROLE = "customer"
# A person who is in frame but not yet confirmed in any zone. Committing a role
# on the first frame a track appears is what made staff read as customers: a
# track only earns the staff label after min_inside_frames inside a staff zone,
# so for those first frames it fell through to "customer" and was added to
# global_customer_ids -- a permanent set, so the miscount survived the later
# promotion to staff. Pending tracks are drawn, but counted as neither, and this
# category is outside the profile's tracking categories so it never reaches the
# published count lists.
_PENDING_ROLE = "pending"


def assign_person_by_area(detections, _customer_areas, staff_areas):
    """Assign 'person' detections to 'staff' or 'customer' by area polygon.

    .. deprecated::
        No longer used by :class:`AdvancedCustomerServiceUseCase`, which assigns
        roles from paired counter zones via ``_update_zone_membership`` -- with
        entry/exit hysteresis, bbox-centre membership, and a bounded sticky-staff
        latch, none of which this function has. Retained because it is a public
        module-level symbol (declared in the ``.pyi`` stub) and removing it would
        be a breaking change for any out-of-tree caller. Near-identical copies live
        in ``customer_service.py`` and ``car_service.py``, which still use theirs.

    Modifies the detection list in-place.

    Args:
        detections: List of detection dicts.
        _customer_areas: Unused; kept for signature compatibility.
        staff_areas: Dict of area_name -> polygon (list of [x, y]).
    """
    # Only process detections with category 'person' for staff/customer assignment
    _ = (_customer_areas,)
    staff_track_ids = set()
    # First pass: assign staff and remember their track_ids
    for det in detections:
        if det.get("category") != "person" and det.get("category") != "staff":
            # Skip non-person, non-staff objects (e.g., chair, tie, etc.)
            continue
        if det.get("category") == "person":
            bbox = det.get("bbox", det.get("bounding_box", None))
            if bbox and len(bbox) == 4:
                center = get_bbox_center(bbox)
                for polygon in staff_areas.values():
                    if point_in_polygon(center, polygon):
                        det["category"] = "staff"
                        if "track_id" in det:
                            staff_track_ids.add(det["track_id"])
                        break
        elif det.get("category") == "staff" and "track_id" in det:
            staff_track_ids.add(det["track_id"])
    # Second pass: assign customer only if not a known staff track_id
    for det in detections:
        if det.get("category") != "person":
            continue
        if det.get("track_id") not in staff_track_ids:
            det["category"] = "customer"
        elif det.get("track_id") in staff_track_ids:
            det["category"] = "staff"


class AdvancedCustomerServiceUseCase(BaseProcessor):
    def __init__(self):
        """Initialize advanced customer service use case."""
        super().__init__("advanced_customer_service")
        self.category = "sales"
        self.CASE_TYPE: Optional[str] = "advanced_customer_service"
        # 2.0: counter-zone model, renamed/removed payload keys, 24 VOLUME metrics.
        self.CASE_VERSION: Optional[str] = "2.0"

        # Customer journey lifecycle (R6). The only survivor of the original
        # "advanced tracking structures" block: the other nine were assigned here
        # and in _initialize_areas and then read by nothing at all -- some since
        # before this rework, the rest orphaned when Phase 4 deleted the proximity
        # service model. Removed rather than left as plausible-looking state that
        # a later reader would try to use.
        self.customer_journey = {}

        # Persistent unique id sets
        self.global_staff_ids = set()
        self.global_customer_ids = set()
        # Sticky staff identity across frames (R1): once a track is confirmed in a
        # staff zone it stays staff, evicted only by presence_grace_frames.
        self.persistent_staff_ids = set()
        # Sticky customer identity, the mirror of the above: a track confirmed in
        # a customer zone keeps the customer label while it is in frame, so
        # stepping out of the zone for a few frames does not flip it back to
        # pending. Evicted by presence_grace_frames, and revoked outright if the
        # track is later confirmed as staff.
        self.persistent_customer_ids = set()

        # Journey states
        self.JOURNEY_STATES = {
            "ENTERING": "entering",
            "QUEUING": "queuing",
            "BEING_SERVED": "being_served",
            "COMPLETED": "completed",
            "LEFT": "left",
        }

        # Tracker initialization (for YOLOv8 frame-wise predictions)
        self.tracker = None
        self._tracker_seam = ConfigDrivenTracker()
        self.smoothing_tracker = None
        self._total_frame_counter = 0

        # Track merging and aliasing (like people_counting)
        self._track_aliases: Dict[Any, Any] = {}
        self._canonical_tracks: Dict[Any, Dict[str, Any]] = {}
        self._track_merge_iou_threshold: float = 0.05
        self._track_merge_time_window: float = 7.0

        # Per-category track ID tracking
        self._per_category_total_track_ids: Dict[str, set] = {}
        self._current_frame_track_ids: Dict[str, set] = {}

        self.start_timer = None
        # Read by _get_start_timestamp_str's fallback branch; initialized here so that
        # branch cannot raise AttributeError when start_timer is present but == "NA".
        self._tracking_start_time: Optional[float] = None

        # Single analytics clock for the frame currently being processed. Every
        # duration metric reads this rather than calling time.time() directly, so
        # they all share one time base. See _resolve_analytics_now.
        self._now: Optional[float] = None

        # Bounded rolling history for the time-weighted avg_staff_count. Unbounded
        # growth here leaked memory on long-running streams (one sample per frame).
        self._staff_presence_history: List[Tuple[float, int]] = []
        self._max_staff_presence_samples: int = 1000
        # Only positions[-1] is ever read; cap the trail so per-customer journeys
        # cannot grow without bound over a long session.
        self._max_journey_positions: int = 50

        # The business-metrics-manager (5-minute Redis/Kafka aggregate publish)
        # integration was removed here (INC pending). It never initialized in
        # this deployment shape: BusinessMetricsManagerFactory._discover_action_id
        # only scans cwd / /usr/src for a directory NAMED like an action id, but
        # this container's action id only ever arrives via the ACTION_RECORD_ID
        # env var -- so the manager was permanently None and every frame paid the
        # init attempt and logging for nothing. The per-frame business_metrics
        # values still reach consumers unconditionally via
        # business_analytics.business_metrics in agg_summary (_calculate_analytics);
        # this only removed the separate, never-working 5-min-aggregate publish
        # path. customer_service.py / license_plate_monitoring.py keep their own
        # integration with the still-live business_metrics_manager_utils module.

        # ---- Counter zone geometry (R1/R2/R9, D-03) ----
        # Zones arrive as one flat zone_config.zones dict and are split by name
        # prefix; the dict key here is the COUNTER ID (the "1" of "customer_1"),
        # so staff and customer polygons for one counter share a key.
        self._staff_zones: Dict[str, List[List[float]]] = {}
        self._customer_zones: Dict[str, List[List[float]]] = {}
        self._counter_ids: List[str] = []
        self._zone_params: Dict[str, Dict[str, Any]] = {}
        self._config_client: Optional[PostProcessingConfigClient] = None
        self._geometry_thread: Optional[threading.Thread] = None
        self._resolved_geometry_cache: Optional[CustomerServiceConfig] = None
        self._zone_resolution_attempted: bool = False
        # Zones are compulsory (D-04), so a violation fails the frame. Logged once
        # per stream rather than per frame -- at 30fps a per-frame error log for a
        # camera whose zones were never drawn is a flood, not a signal.
        self._zone_violation_logged: bool = False

        self._init_zone_membership_state()

        # ---- Per-counter serving state (D-01/D-06) ----
        # At most one customer is served per counter at any instant, and only when
        # that counter's staff zone is occupied.
        self._counter_served_track: Dict[str, Any] = {}
        # Which counter each customer is currently a member of, for exit detection.
        self._customer_counter: Dict[Any, str] = {}

        # ---- Session cumulative counters ----
        # MONOTONIC by construction: the analytics bridge derives per-window
        # "*_in_interval" metrics as (value now - value at window start), which is
        # only valid if these never decrease.
        self._total_customers_served: int = 0
        self._total_abandoned: int = 0

        # Bounded rings of completed durations. Unbounded lists here were how
        # service_times grew for the life of the process.
        self._wait_durations: List[float] = []
        self._service_durations: List[float] = []
        self._max_wait_seconds: float = 0.0
        self._max_service_seconds: float = 0.0
        self._max_duration_samples: int = 500

        # Per-frame id sets published on the side channel.
        self._frame_new_customer_ids: List[Any] = []
        self._frame_served_ids: List[Any] = []
        self._frame_abandoned_ids: List[Any] = []
        # Snapshot of per-counter state for the frame in flight.
        self._counter_status: Dict[str, Dict[str, Any]] = {}

        # Incident episode lifecycle (ACS-04). One episode spans a continuous run
        # of alerting frames: the id is minted when it opens and held until it
        # closes, and _last_incident is the snapshot re-emitted with a real
        # end_time on the frame the condition clears -- the only thing that ever
        # closes an episode.
        self._incident_active: bool = False
        self._incident_id: Optional[str] = None
        self._incident_start_timestamp: str = ""
        self._last_incident: Optional[Dict[str, Any]] = None

    def _init_zone_membership_state(self) -> None:
        """Zone membership with hysteresis (R3).

        All keyed counter_id -> track_id -> value. A track is CONFIRMED inside a
        zone only after min_inside_frames consecutive frames, and only leaves
        after exit_grace_frames consecutive frames outside. Crowded queues
        occlude constantly; without this a single dropped frame would evict a
        customer, restart their entry clock and hand "being served" to someone
        else (see _pick_served_track).

        Split out of __init__ so that method stays under the org complexity cap;
        it is one cohesive block of state and has no other caller.
        """
        self._cz_inside_frames: Dict[str, Dict[Any, int]] = {}
        self._cz_outside_frames: Dict[str, Dict[Any, int]] = {}
        self._sz_inside_frames: Dict[str, Dict[Any, int]] = {}
        self._sz_outside_frames: Dict[str, Dict[Any, int]] = {}
        # First confirmed entry into a customer zone, on the analytics clock. This
        # is what the FIFO serving rule orders on, so it must survive a brief
        # occlusion -- hence presence_grace_frames rather than exit_grace_frames.
        self._cz_entry_time: Dict[str, Dict[Any, float]] = {}
        # CONFIRMED and seen-inside-this-frame. Diagnostics only -- not used to
        # derive counts (see _cz_members below). Note this is NOT the raw
        # geometric membership: the add() only fires once min_inside_frames has
        # been met, so an entrant still inside its confirmation window is in
        # neither this nor _cz_members.
        self._cz_current_tracks: Dict[str, set] = {}
        self._sz_current_tracks: Dict[str, set] = {}
        # RAW geometric membership this frame, pre-hysteresis and pre-role: every
        # track whose zone-test point fell inside the polygon, whatever role it
        # ends up with. This is what zone_analysis[...].original_counts reports,
        # so that it means the same thing as intrusion_detection's own
        # original_counts (which comes from count_objects_in_zones, i.e. before
        # that app's debounce). Per-frame, cleared by
        # _prepare_zone_membership_frame.
        self._cz_raw_tracks: Dict[str, set] = {}
        self._sz_raw_tracks: Dict[str, set] = {}
        # RETAINED membership: confirmed and not yet released. This -- not
        # _cz_current_tracks -- is what counts are derived from, so a customer
        # occluded for a frame does not make the queue momentarily shorter. That
        # robustness is the whole point of the hysteresis (R3).
        self._cz_members: Dict[str, set] = {}
        self._sz_members: Dict[str, set] = {}
        # Lifetime-unique confirmed track ids per RAW zone name (customer_<id> /
        # staff_<id>), for zone_analysis[...].total_count -- the ACS analogue of
        # intrusion_detection's own _zone_total_track_ids. Grows for the life of
        # the session by design (same tradeoff intrusion_detection accepts): only
        # its length is ever emitted, never the set itself.
        self._zone_total_track_ids: Dict[str, set] = {}
        # Consecutive frames a track has been absent from the frame entirely.
        self._track_absent_frames: Dict[Any, int] = {}

    def process(
        self,
        data: Any,
        config: ConfigProtocol,
        context: Optional[ProcessingContext] = None,
        stream_info: Optional[dict] = None,
    ) -> ProcessingResult:
        """
        Process advanced customer service analytics.
        """
        start_time = time.time()
        # Was three bare print()s plus three logger.info lines dumping the whole
        # stream_info -- per frame, so ~30x/second per camera, to stdout where no
        # log level can turn it off. Debug level, one line.
        self.logger.debug("stream_info: %s", stream_info)

        try:
            if not isinstance(config, CustomerServiceConfig):
                self._debug_elapsed_since(start_time)
                return self.create_error_result(
                    "Invalid configuration type for advanced customer service",
                    usecase=self.name,
                    category=self.category,
                    context=context,
                )

            # NOTE: this used to also do `context.stream_info = stream_info` here.
            # Removed (INC pending): nothing downstream ever reads
            # result.to_dict()["context"]["stream_info"] back off the result, and
            # stream_info can carry a live `config_client` object (see
            # _resolve_geometry_from_api's `stream_info.get("config_client")`) --
            # ProcessingResult.to_dict()'s blind `context.__dict__` dump then tries
            # to serialize that object's internals, which is what was producing
            # "Dict key must be str" in the result producer on every frame.
            if context is None:
                context = ProcessingContext()

            # Reject payloads that are neither a detection list nor a frame-keyed dict.
            # _extract_detections is deliberately lenient and returns [] for anything
            # else, which would otherwise surface as a successful frame reporting zero
            # customers -- indistinguishable from a genuinely empty scene, and a silent
            # mask over an upstream format change.
            if not isinstance(data, (list, dict)):
                self._debug_elapsed_since(start_time)
                return self.create_error_result(
                    "Invalid data format: expected a list of detections or a frame-keyed "
                    f"dict, got {type(data).__name__}",
                    usecase=self.name,
                    category=self.category,
                    context=context,
                )

            # Track aliasing bounds are configurable now rather than hardcoded at
            # 0.05 / 7.0s. 0.05 IoU is loose enough to fold a passer-by onto a
            # neighbour's canonical ID in a crowded queue.
            self._track_merge_iou_threshold = config.track_merge_iou_threshold
            self._track_merge_time_window = config.track_merge_time_window_seconds

            # Counter zones are COMPULSORY and must be paired (staff_<i> with
            # customer_<i>). Publishing zeros for a camera whose zones were never
            # drawn would be indistinguishable from a genuinely quiet store, which
            # is the same silent-mask failure the data-format guard above exists to
            # prevent -- so a violation fails the frame with a message naming it.
            zone_violations = self._prepare_counter_zones(config, stream_info)
            if zone_violations:
                if not self._zone_violation_logged:
                    self._zone_violation_logged = True
                    self.logger.error(
                        "AdvancedCustomerService: unusable counter zones for camera=%s: %s",
                        (self.get_camera_info_from_stream(stream_info) or {}).get(
                            "camera_name", "unknown"
                        ),
                        "; ".join(zone_violations),
                    )
                self._debug_elapsed_since(start_time)
                return self.create_error_result(
                    "advanced_customer_service requires paired counter zones "
                    "(staff_1 + customer_1, staff_2 + customer_2, ...): "
                    + "; ".join(zone_violations),
                    usecase=self.name,
                    category=self.category,
                    context=context,
                )
            self._zone_violation_logged = False

            # Establish this frame's analytics clock before anything that records a
            # timestamp (track aliasing, journey state, presence history) runs, so a
            # single frame never mixes stream time with wall time.
            self._now = self._resolve_analytics_now(stream_info)

            input_format = match_results_structure(data)
            context.input_format = input_format
            context.confidence_threshold = config.confidence_threshold
            context.enable_tracking = config.enable_tracking

            self.logger.info(
                f"Processing advanced customer service with format: {input_format.value}"
            )

            processed_data = data
            if config.confidence_threshold is not None:
                processed_data = filter_by_confidence(processed_data, config.confidence_threshold)
                self.logger.debug(
                    f"Applied confidence filtering with threshold {config.confidence_threshold}"
                )

            if hasattr(config, "index_to_category") and config.index_to_category:
                processed_data = apply_category_mapping(processed_data, config.index_to_category)
                self.logger.debug("Applied category mapping")

            # --- Smoothing logic ---
            if getattr(config, "enable_smoothing", False):
                if not hasattr(self, "smoothing_tracker") or self.smoothing_tracker is None:
                    smoothing_config = BBoxSmoothingConfig(
                        smoothing_algorithm=getattr(config, "smoothing_algorithm", "observability"),
                        window_size=getattr(config, "smoothing_window_size", 20),
                        cooldown_frames=getattr(config, "smoothing_cooldown_frames", 5),
                        confidence_threshold=getattr(config, "confidence_threshold", 0.5),
                        confidence_range_factor=getattr(
                            config, "smoothing_confidence_range_factor", 0.5
                        ),
                        enable_smoothing=True,
                    )
                    self.smoothing_tracker = BBoxSmoothingTracker(smoothing_config)
                processed_data = bbox_smoothing(
                    processed_data,
                    self.smoothing_tracker.config,
                    self.smoothing_tracker,
                )

            # Extract detections from processed data
            detections = self._extract_detections(processed_data)

            # --- Apply AdvancedTracker for YOLOv8 frame-wise predictions (like people_counting) ---
            try:
                if self.tracker is None:
                    # NOTE: the original inline construction used a truthy check
                    # (`if config.confidence_threshold else 0.4`), which treats
                    # confidence_threshold == 0.0 as "unset" and falls back to
                    # LEGACY_40's 0.4. The seam's derive_from_confidence checks
                    # `is not None`, so confidence_threshold == 0.0 (a degenerate,
                    # not realistically-configured value) would be honored as
                    # 0.0 instead of falling back to 0.4. Documented, not silently
                    # assumed identical.
                    self.tracker = self._tracker_seam.get_shared_tracker(
                        config, stream_info, profile=TrackerProfile.LEGACY_40
                    )
                # Apply tracker to get track_ids
                detections_before_tracking = len(detections)
                detections = self.tracker.update(detections)
                self.logger.debug(
                    f"Applied AdvancedTracker, {len(detections)} detections with track_ids"
                )
                if detections_before_tracking and not detections:
                    # The tracker does not raise on an unusable payload, it just
                    # returns nothing -- so this would otherwise present as a silently
                    # empty analytics frame. The usual cause is bbox geometry supplied
                    # as a bare [x1, y1, x2, y2] list; the tracker requires
                    # `bounding_box` as an {xmin, ymin, xmax, ymax} dict.
                    self.logger.warning(
                        "AdvancedTracker consumed %d detections and returned none - all analytics "
                        "for this frame will read zero. Check that detections carry `bounding_box` "
                        "as an {xmin,ymin,xmax,ymax} dict rather than a bare bbox list.",
                        detections_before_tracking,
                    )
            except Exception as e:  # noqa: BLE001 - third-party tracker, frame boundary
                # Deliberately blind: AdvancedTracker is third-party code called
                # once per frame, and no tracker failure is worth taking the
                # whole analytics frame down. Degrades to untracked detections.
                self.logger.warning(f"AdvancedTracker failed: {e}, continuing without tracking")

            # Update tracking state (track merging, canonical IDs)
            self._update_tracking_state(detections)
            self._total_frame_counter += 1

            # Relabel staff/customer from counter-zone geometry and refresh
            # per-counter membership. Replaces assign_person_by_area +
            # _categorize_detections: role now comes from which zone a track is
            # confirmed in, not from the model's class name, so staff_categories /
            # customer_categories are no longer consulted.
            staff_detections, customer_detections = self._update_zone_membership(
                detections, config, stream_info
            )
            self.logger.debug(
                f"Extracted {len(staff_detections)} staff and {len(customer_detections)} customer detections"
            )

            # Extract frame number from stream_info (like people_counting)
            frame_number = None
            if stream_info:
                input_settings = stream_info.get("input_settings", {})
                start_frame = input_settings.get("start_frame")
                end_frame = input_settings.get("end_frame")
                if start_frame is not None and end_frame is not None and start_frame == end_frame:
                    frame_number = start_frame

            current_time = self._current_clock()
            analytics_results = self._process_comprehensive_analytics(
                staff_detections, customer_detections, config, current_time
            )

            # --- FIX: Ensure agg_summary is top-level and events/tracking_stats are dicts ---
            # Reconstruct processed_data dict with frame_number as key for per-frame analytics
            if frame_number is not None:
                processed_data_for_summary = {str(frame_number): detections}
            elif isinstance(processed_data, dict):
                processed_data_for_summary = processed_data
            else:
                processed_data_for_summary = {"0": detections}

            agg_summary = self._generate_per_frame_agg_summary(
                processed_data_for_summary,
                analytics_results,
                config,
                context,
                stream_info,
            )

            insights = self._generate_insights(analytics_results, config)
            alerts = self._check_alerts(analytics_results, config)
            summary = self._generate_summary(analytics_results, alerts)
            predictions = self._extract_predictions(processed_data)
            context.mark_completed()

            # Compose result data with harmonized agg_summary structure
            result = self.create_result(
                data={"agg_summary": agg_summary},
                usecase=self.name,
                category=self.category,
                context=context,
            )

            result.summary = summary
            result.insights = insights
            result.predictions = predictions
            result.metrics = analytics_results.get("business_metrics", {})

            # The old "no customer or staff areas defined" and "high service
            # proximity threshold" warnings are gone. Both described the retired
            # area/proximity model: geometry now comes from paired counter zones
            # that are validated before any analytics run (a missing pair is a hard
            # error, not a warning), and serving identity no longer uses a distance
            # threshold. Left in place they fired on every valid frame -- because
            # customer_areas/staff_areas are legitimately empty now -- which
            # downgraded every successful result to WARNING.

            self.logger.info(
                f"Advanced customer service analysis completed successfully in {result.processing_time:.2f}s"
            )
            self._debug_elapsed_since(start_time)
            return result

        except Exception as e:
            self.logger.error(f"Advanced customer service analysis failed: {str(e)}", exc_info=True)

            if context:
                context.mark_completed()

            self._debug_elapsed_since(start_time)
            return self.create_error_result(
                str(e),
                type(e).__name__,
                usecase=self.name,
                category=self.category,
                context=context,
            )

    def _generate_per_frame_agg_summary(
        self, processed_data, analytics_results, config, _context, stream_info=None
    ):
        """
        Generate agg_summary dict with per-frame incidents, tracking_stats, business_analytics, alerts, human_text.
        processed_data: dict of frame_id -> detections (list)
        analytics_results: output of _compile_analytics_results
        """
        _ = (_context,)
        agg_summary = {}

        # Try to get FPS from stream_info or config
        fps = None
        if stream_info:
            fps = stream_info.get("fps") or stream_info.get("frame_rate")
        if not fps:
            fps = getattr(config, "fps", None) or getattr(config, "frame_rate", None)
        try:
            fps = float(fps)
            if fps <= 0:
                fps = None
        except (TypeError, ValueError):
            fps = None

        # If frame_ids are not sorted, sort them numerically if possible
        try:
            frame_ids = sorted(processed_data.keys(), key=int)
        except (TypeError, ValueError):
            frame_ids = list(processed_data.keys())

        # For real-time fallback, record wall-clock start time
        wallclock_start_time = None
        if not fps:
            wallclock_start_time = time.time()
        self._debug_stream_timing("wallclock_start_time", wallclock_start_time)

        # Computed once per process() call, like intrusion_detection's own
        # zone_analysis -- the same state feeds every frame_id in the loop below.
        zone_analysis = self._get_zone_analysis()

        for frame_id in frame_ids:
            detections = processed_data[frame_id]

            queue_analytics = analytics_results.get("customer_queue_analytics", {})
            staff_analytics = analytics_results.get("staff_management_analytics", {})
            counter_analytics = analytics_results.get("counter_analytics", {})
            journey_analytics = analytics_results.get("customer_journey_analytics", {})
            business_metrics = analytics_results.get("business_metrics", {})

            current_timestamp = self._get_current_timestamp_str(stream_info)
            start_timestamp = self._get_start_timestamp_str(stream_info)
            self._debug_stream_timing("start_timestamp", start_timestamp)

            alerts, alert_settings = self._build_alerts(config, queue_analytics, counter_analytics)

            human_text = self._build_human_text(
                current_timestamp, queue_analytics, staff_analytics, counter_analytics
            )

            event = self._build_incident(
                config,
                counter_analytics,
                alerts,
                alert_settings,
                human_text,
                current_timestamp=current_timestamp,
                start_timestamp=start_timestamp,
                stream_info=stream_info,
            )

            # One naming convention across every count list and
            # target_categories: lowercase "staff" / "customer". These previously
            # disagreed four ways ("Active Customers", "Staff", "person"), so any
            # dashboard joining counts on category name missed.
            total_counts, current_counts, current_new_counts = self._build_count_lists(
                staff_analytics, journey_analytics, queue_analytics
            )

            detection_objs = [
                {
                    "category": d.get("category"),
                    "bounding_box": d.get("bounding_box", d.get("bbox", {})),
                    "track_id": d.get("track_id"),
                }
                for d in detections
                # Pending tracks are included. They are counted nowhere -- not in
                # any count list, not in target_categories -- but they are real
                # people the model saw, and people_in_frame counts them, so
                # dropping them here would leave the detections list disagreeing
                # with that number and give an overlay no box to draw for someone
                # plainly standing in the shot.
                if isinstance(d, dict)
                and d.get("category") in (_STAFF_ROLE, _CUSTOMER_ROLE, _PENDING_ROLE)
            ]

            reset_settings = self._build_reset_settings(config)

            tracking_stat = {
                "input_timestamp": current_timestamp,
                "reset_timestamp": start_timestamp,
                "camera_info": self.get_camera_info_from_stream(stream_info),
                "total_counts": total_counts,
                "current_counts": current_counts,
                "current_new_counts": current_new_counts,
                "detections": detection_objs,
                "alerts": alerts,
                "alert_settings": alert_settings,
                "reset_settings": reset_settings,
                "human_text": human_text,
                "target_categories": [_STAFF_ROLE, _CUSTOMER_ROLE],
                # Side channel consumed by legacy_analytics_bridge. Emitted on
                # EVERY frame including idle ones: idle frames are the denominator
                # for every windowed mean, and omitting them would bias each one.
                "customer_service_analytics": self._build_side_channel(
                    queue_analytics,
                    staff_analytics,
                    counter_analytics,
                    journey_analytics,
                    people_in_frame=len(detection_objs),
                ),
            }

            business_analytics = {
                "business_metrics": business_metrics,
                "customer_queue_analytics": queue_analytics,
                "staff_management_analytics": staff_analytics,
                "counter_analytics": counter_analytics,
                "customer_journey_analytics": journey_analytics,
                "alerts": alerts,
                "alert_settings": alert_settings,
            }
            agg_summary[str(frame_id)] = {
                "incidents": event,
                "tracking_stats": tracking_stat,
                "business_analytics": business_analytics,
                "alerts": alerts,
                "human_text": human_text,
            }
            # Mirrors intrusion_detection: only attached when there are
            # configured zones to report, same as `if zone_analysis:` there.
            if zone_analysis:
                agg_summary[str(frame_id)]["zone_analysis"] = zone_analysis
        return agg_summary

    def _build_count_lists(
        self,
        staff_analytics: Dict[str, Any],
        journey_analytics: Dict[str, Any],
        queue_analytics: Dict[str, Any],
    ) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]]]:
        """The three ``tracking_stats`` count lists, in the shared contract order.

        Returns ``(total_counts, current_counts, current_new_counts)``. Only
        ``staff``/``customer`` appear: ``pending`` is deliberately absent from
        every count list (see the ``detection_objs`` note in the caller).
        """
        total_counts = [
            {"category": _STAFF_ROLE, "count": staff_analytics.get("total_staff", 0)},
            {"category": _CUSTOMER_ROLE, "count": journey_analytics.get("unique_customers", 0)},
        ]
        current_counts = [
            {"category": _STAFF_ROLE, "count": staff_analytics.get("active_staff", 0)},
            {"category": _CUSTOMER_ROLE, "count": queue_analytics.get("active_customers", 0)},
        ]
        new_counts = self.get_new_counts_this_frame()
        current_new_counts = [
            {"category": role, "count": new_counts.get(role, 0)}
            for role in (_STAFF_ROLE, _CUSTOMER_ROLE)
        ]
        return total_counts, current_counts, current_new_counts

    @staticmethod
    def _build_reset_settings(config: CustomerServiceConfig) -> List[Dict[str, Any]]:
        """The ``tracking_stats.reset_settings`` block: a pure view of config."""
        return [
            {
                "interval_type": config.reset_interval_type,
                "reset_time": {
                    "value": config.reset_time_value,
                    "time_unit": config.reset_time_unit,
                },
            }
        ]

    def _build_side_channel(
        self,
        queue: Dict[str, Any],
        staff: Dict[str, Any],
        counters: Dict[str, Any],
        journey: Dict[str, Any],
        *,
        people_in_frame: int,
    ) -> Dict[str, Any]:
        """Per-frame block the analytics bridge resolves every VOLUME metric from.

        ``unique_customers`` / ``total_customers_served`` / ``total_abandoned`` are
        MONOTONIC by construction. The bridge derives each ``*_in_interval`` metric
        as (value now - value at window start), which is only valid while that
        holds -- so nothing here may ever decrease.

        Three separate headcounts, deliberately named for what they actually
        measure. Zones are compulsory (R2) but the frame is bigger than the
        zones, so somebody standing in the shop floor is real and countable yet
        belongs to no counter:

        * ``people_in_frame`` -- every person detected, zone or no zone. The only
          one of the three comparable to other apps' ``people_in_frame``.
        * ``customers_at_counters`` -- customers assigned to some counter.
        * ``staff_on_counters`` -- staff currently inside a staff zone.

        The last two were originally called ``customers_in_frame`` /
        ``staff_in_frame``, which promised footfall and delivered zone
        occupancy - and ``customers_at_counters`` was a second key carrying the
        identical number. Renamed before Phase 6 put them on the wire.
        """
        customers_now = queue.get("active_customers", 0)
        staff_now = staff.get("active_staff", 0)
        return {
            "people_in_frame": people_in_frame,
            "customers_at_counters": customers_now,
            "staff_on_counters": staff_now,
            "total_counters": counters.get("total_counters", 0),
            "active_counters": counters.get("active_counters", 0),
            "staffed_counters": counters.get("staffed_counters", 0),
            "serving_counters": counters.get("serving_counters", 0),
            "counter_utilization": counters.get("counter_utilization", 0.0),
            "staff_coverage": staff.get("staff_coverage", 0.0),
            "total_queue_length": counters.get("total_queue_length", 0),
            "max_queue_length": counters.get("max_queue_length", 0),
            # monotonic cumulative counters
            "unique_customers": journey.get("unique_customers", 0),
            "total_customers_served": self._total_customers_served,
            "total_abandoned": self._total_abandoned,
            # duration snapshots
            "avg_wait_seconds": queue.get("avg_wait_seconds", 0.0),
            "max_wait_seconds": queue.get("max_wait_seconds", 0.0),
            "avg_service_seconds": queue.get("avg_service_seconds", 0.0),
            "max_service_seconds": queue.get("max_service_seconds", 0.0),
            "abandonment_rate": (self._calculate_abandonment_rate()),
            "customer_to_staff_ratio": round(customers_now / max(staff_now, 1), 2),
            # per-frame id sets
            "frame_new_customer_ids": list(self._frame_new_customer_ids),
            "frame_served_ids": list(self._frame_served_ids),
            "frame_abandoned_ids": list(self._frame_abandoned_ids),
            # per-counter detail (NOT a VOLUME metric -- a dict cannot be published
            # as one; kept here for per-counter dashboards and debugging)
            "counters": counters.get("counters", {}),
        }

    def _build_incident(
        self,
        config: CustomerServiceConfig,
        counters: Dict[str, Any],
        alerts: List[Dict],
        alert_settings: List[Dict],
        human_text: str,
        *,
        current_timestamp: str,
        start_timestamp: str,
        stream_info: Optional[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """One incident episode per continuous run of alerting frames (ACS-04).

        Reference implementation is ``intrusion_detection._generate_incidents``;
        the three rules that make an episode legible downstream are:

        * **active frame** -> ``end_time = ""``. Anything else reads as CLOSED, so
          a "still active" *sentence* (which is what this use case used to emit)
          closes the incident on its very first frame.
        * **the frame the condition clears** -> re-emit the last active incident
          once with a real ``end_time``. That re-emission is the ONLY thing that
          ever closes an episode; without it an incident stays open forever.
        * **idle frame** -> ``{}``. Not an incident with zero counts: an empty dict
          is how the wire says "nothing happening".

        ``incident_id`` is a uuid minted when the episode opens and held for its
        whole duration. The old ``f"AdvancedCustomerService_{frame_id}"`` changed
        every frame, so every frame looked like a brand-new incident and none of
        them could ever be closed.

        The gate is ``bool(alerts)`` -- the same condition the alerts themselves
        use, so the two can never disagree about whether something is wrong. It is
        also self-clearing, which matters: ``assembly_line_detection`` gated on a
        permanently-present object and its incident could never close.
        """
        level_settings = {"low": 1, "medium": 3, "significant": 4, "critical": 7}
        camera_info = stream_info.get("camera_info", {}) if stream_info else {}

        if not alerts:
            if self._incident_active and self._last_incident is not None:
                closing = dict(self._last_incident)
                closing["end_time"] = current_timestamp
                self._incident_active = False
                self._incident_id = None
                self._last_incident = None
                return closing
            self._incident_active = False
            self._incident_id = None
            self._last_incident = None
            return {}

        if not self._incident_active:
            self._incident_active = True
            self._incident_id = str(uuid.uuid4())
            # The episode's own start, not the stream's: a queue that builds two
            # hours in did not start when the camera did.
            self._incident_start_timestamp = start_timestamp or current_timestamp

        severity_level = self._compute_severity_level(
            counters.get("max_queue_length", 0), level_settings
        )
        event = self.create_incident(
            incident_id=self._incident_id,
            incident_type=self.CASE_TYPE,
            severity_level=severity_level,
            human_text=human_text,
            camera_info=camera_info,
            alerts=alerts,
            alert_settings=alert_settings,
            start_time=self._incident_start_timestamp,
            end_time="",
            level_settings=level_settings,
        )
        # create_incident computes `end_time or timestamp`, which silently turns
        # "" into a real timestamp -- i.e. into a CLOSED incident. Re-assign.
        event["end_time"] = ""
        self._last_incident = dict(event)
        _ = (config,)
        return event

    def _calculate_abandonment_rate(self) -> float:
        resolved = self._total_customers_served + self._total_abandoned
        return round(self._total_abandoned / resolved * 100.0, 2) if resolved else 0.0

    def _build_alerts(
        self,
        config: CustomerServiceConfig,
        queue: Dict[str, Any],
        counters: Dict[str, Any],
    ) -> Tuple[List[Dict], List[Dict]]:
        """Alerts for the agg_summary payload.

        Single source of truth: ``_check_alerts`` now delegates here, so the
        summary and the payload cannot disagree about whether an alert fired.
        Previously the two paths had different gating (one bailed out when
        ``alert_config`` was None, the other ignored it) and different rules.
        """
        alerts: List[Dict] = []
        alert_settings: List[Dict] = []
        email = config.email_address or ""

        # Queue length is PER COUNTER: a site-wide sum would trip on many short
        # queues, which is not the condition anyone wants to be paged about.
        worst_queue = counters.get("max_queue_length", 0)
        if worst_queue > config.queue_length_threshold:
            alert_settings.append(
                {
                    "alert_type": "email",
                    "incident_category": "customer_queue",
                    "threshold_level": config.queue_length_threshold,
                    "ascending": True,
                    "settings": {"email_address": email},
                }
            )
            alerts.append(
                {
                    "alert_type": "email",
                    "alert_id": "email_1",
                    "incident_category": "customer_queue",
                    "threshold_value": worst_queue,
                    "ascending": True,
                    "settings": {"email_address": email},
                }
            )

        # An occupied but unstaffed counter -- customers waiting at a desk nobody
        # is working. Replaces the old service_efficiency alert, which fired off an
        # all-time ratio that decayed toward zero and so latched on permanently.
        unstaffed_busy = [
            counter_id
            for counter_id, status in (counters.get("counters") or {}).items()
            if status.get("is_active") and not status.get("is_staffed")
        ]
        if unstaffed_busy:
            alert_settings.append(
                {
                    "alert_type": "email",
                    "incident_category": "unstaffed_counter",
                    "threshold_level": 0,
                    "ascending": True,
                    "settings": {"email_address": email},
                }
            )
            alerts.append(
                {
                    "alert_type": "email",
                    "alert_id": "email_2",
                    "incident_category": "unstaffed_counter",
                    "threshold_value": len(unstaffed_busy),
                    "ascending": True,
                    "settings": {"email_address": email},
                    "counters": sorted(
                        unstaffed_busy, key=lambda c: int(c) if str(c).isdigit() else 0
                    ),
                }
            )

        _ = (queue,)
        return alerts, alert_settings

    # ------------------------------------------------------------------ #
    # Counter zone geometry (R1/R2/R9, D-03)                             #
    # ------------------------------------------------------------------ #

    def set_config_client(self, client: Optional[PostProcessingConfigClient]) -> None:
        """Set the client used to resolve zones from the post-processing API."""
        self._config_client = client

    def _start_geometry_resolver(
        self, config: CustomerServiceConfig, stream_info: Dict[str, Any]
    ) -> None:
        """Spawn a daemon thread that keeps retrying API geometry resolution."""
        if self._geometry_thread is not None:
            return

        def _resolver():
            while True:
                try:
                    result = self._resolve_geometry_from_api(config, stream_info)
                    if result is not None:
                        self._resolved_geometry_cache = result
                        self.logger.info(
                            "AdvancedCustomerService: zone geometry resolved from API (background)"
                        )
                        return
                    self.logger.info(
                        "AdvancedCustomerService: API geometry returned None, retrying in %ds",
                        GEOMETRY_RETRY_INTERVAL,
                    )
                except Exception as exc:  # noqa: BLE001 - background thread must never die
                    # Deliberately blind: this is the retry loop of a daemon
                    # thread. Any escaping exception kills the thread, and with
                    # it every future retry, so geometry would never resolve.
                    self.logger.warning(
                        "AdvancedCustomerService: background geometry resolve error: %s", exc
                    )
                time.sleep(GEOMETRY_RETRY_INTERVAL)

        t = threading.Thread(target=_resolver, daemon=True, name="acs-zone-geometry-resolver")
        self._geometry_thread = t
        t.start()
        self.logger.info(
            "AdvancedCustomerService: started background zone geometry resolver thread"
        )

    def _resolve_geometry_from_api(
        self,
        config: CustomerServiceConfig,
        stream_info: Optional[Dict[str, Any]],
    ) -> Optional[CustomerServiceConfig]:
        """Resolve ``zone_config`` from the post-processing API.

        Mirrors ``intrusion_detection._resolve_geometry_from_api``. The zones it
        returns are always PIXEL space -- that is what ``denormalize_config``
        means -- so a normalized detection point must be scaled up before it is
        tested against them (see ``to_zone_test_point``).
        """
        client = self._config_client or (stream_info.get("config_client") if stream_info else None)
        if not client and stream_info:
            try:
                client = PostProcessingConfigClient(logger=self.logger)
                if getattr(client, "_session", None) is None:
                    self.logger.info(
                        "AdvancedCustomerService: geometry resolution skipped (no config_client; set "
                        "MATRICE_ACCESS_KEY_ID, MATRICE_SECRET_ACCESS_KEY, MATRICE_ACCOUNT_NUMBER "
                        "or call set_config_client())"
                    )
                    return None
                self._config_client = client
            except Exception as e:  # noqa: BLE001 - external SDK/credential boundary
                # Deliberately blind: constructing the client reaches into the
                # matrice SDK and the environment (credentials, network). Every
                # failure mode here is optional-feature degradation, not a
                # reason to fail the frame.
                self.logger.warning(
                    "AdvancedCustomerService: could not create config client from env: %s",
                    e,
                )
                return None

        if not stream_info or not client:
            return None

        ids = client.get_stream_identifiers(stream_info)
        app_deployment_id = ids.get("app_deployment_id") or ""
        camera_id = ids.get("camera_id") or ""
        if not app_deployment_id or not camera_id:
            self.logger.info(
                "AdvancedCustomerService: geometry resolution skipped (missing app_deployment_id=%r or camera_id=%r)",
                app_deployment_id,
                camera_id,
            )
            return None

        configs, err, _ = client.get_post_processing_configs_by_app_deployment(app_deployment_id)
        if err or not configs:
            self.logger.info(
                "AdvancedCustomerService: geometry resolution returning None (err=%r, configs=%s)",
                err,
                len(configs) if configs else 0,
            )
            return None

        filtered = client.filter_configs_by_camera_id(configs, camera_id)
        if not filtered:
            self.logger.info(
                "AdvancedCustomerService: no post-processing config for camera_id=%s",
                camera_id,
            )
            return None

        width, height = client.get_resolution(camera_id)
        if width is None or height is None:
            self.logger.info(
                "AdvancedCustomerService: no resolution for camera_id=%s (width=%r height=%r)",
                camera_id,
                width,
                height,
            )
            return None

        doc_px = client.denormalize_config(filtered[0], width, height)
        cam_cfg = (doc_px.get("postProcessing") or {}).get(camera_id) or {}
        zone_config_raw = cam_cfg.get("zone_config") or {}
        zones_px = zone_config_raw.get("zones") or {}
        if not isinstance(zones_px, dict) or not zones_px:
            self.logger.info(
                "AdvancedCustomerService: no zones in zone_config for camera_id=%s",
                camera_id,
            )
            return None

        zones_dict = {str(name): [list(pt) for pt in points] for name, points in zones_px.items()}

        zone_params_raw = zone_config_raw.get("zone_params") or {}
        if isinstance(zone_params_raw, dict) and zone_params_raw:
            self._zone_params = {
                str(zn): dict(zp) for zn, zp in zone_params_raw.items() if isinstance(zp, dict)
            }

        self.logger.info(
            "AdvancedCustomerService: resolved %d zone(s) from API: %s",
            len(zones_dict),
            sorted(zones_dict.keys()),
        )
        return replace(config, zone_config=ZoneConfig(zones=zones_dict))

    def _normalize_zone_config_and_params(self, config: CustomerServiceConfig) -> None:
        """Accept ``zone_config`` as a raw dict and hoist nested ``zone_params``.

        The UI/API/JSON shape nests per-zone tuning parameters as a sibling of
        ``zones`` inside ``zone_config``. ``CustomerServiceConfig`` has no
        ``zone_params`` field (and must not grow one -- it is shared with the
        ``customer_service`` use case), so they are stored on the use case.
        No-op once already normalized.
        """
        zc = getattr(config, "zone_config", None)
        if isinstance(zc, dict):
            zones = zc.get("zones") or {}
            zone_params = zc.get("zone_params") or {}
            if isinstance(zone_params, dict) and zone_params:
                self._zone_params = {
                    str(zn): dict(zp) for zn, zp in zone_params.items() if isinstance(zp, dict)
                }
            config.zone_config = ZoneConfig(
                zones={str(name): [list(pt) for pt in pts] for name, pts in zones.items()}
                if isinstance(zones, dict)
                else {}
            )

    def _zone_param(self, zone_name: str, key: str, default: Any) -> Any:
        """Per-zone override from ``zone_params``, falling back to a global."""
        params = self._zone_params.get(zone_name) or {}
        value = params.get(key)
        return default if value is None else value

    def _split_zones_by_role(
        self, zones: Dict[str, List[List[float]]]
    ) -> Tuple[Dict[str, List[List[float]]], Dict[str, List[List[float]]], List[str]]:
        """Split a flat zones dict into staff/customer polygons keyed by counter id.

        Returns ``(staff_zones, customer_zones, unrecognised_names)``. A name that
        matches neither ``staff_<int>`` nor ``customer_<int>`` is collected and
        reported rather than silently dropped -- a typo'd zone name would
        otherwise remove a whole counter from the analytics with no signal.
        """
        staff_zones: Dict[str, List[List[float]]] = {}
        customer_zones: Dict[str, List[List[float]]] = {}
        unrecognised: List[str] = []

        for name, polygon in (zones or {}).items():
            match = _ZONE_NAME_RE.match(str(name).strip().lower())
            if not match:
                unrecognised.append(str(name))
                continue
            role, counter_id = match.group(1), str(int(match.group(2)))
            if role == _STAFF_ROLE:
                staff_zones[counter_id] = polygon
            else:
                customer_zones[counter_id] = polygon

        return staff_zones, customer_zones, sorted(unrecognised)

    def _validate_counter_zones(
        self,
        staff_zones: Dict[str, List[List[float]]],
        customer_zones: Dict[str, List[List[float]]],
        unrecognised: List[str],
    ) -> List[str]:
        """Return every reason this zone configuration is unusable.

        Zones are compulsory and must be paired. Odd/even arity is NOT checked
        directly: "must come in pairs" is exactly equivalent to "every staff_<k>
        has a customer_<k> and vice versa", and pairing yields an error message
        that names the missing zone instead of just a count.
        """
        violations: List[str] = []

        if not staff_zones and not customer_zones:
            violations.append(
                "no counter zones configured - advanced_customer_service requires at least one "
                "staff_1 / customer_1 polygon pair in zone_config.zones"
            )

        for counter_id in sorted(set(customer_zones) - set(staff_zones), key=int):
            violations.append(f"customer_{counter_id} has no matching staff_{counter_id}")
        for counter_id in sorted(set(staff_zones) - set(customer_zones), key=int):
            violations.append(f"staff_{counter_id} has no matching customer_{counter_id}")

        if unrecognised:
            violations.append(
                "zone name(s) match neither staff_<n> nor customer_<n>: " + ", ".join(unrecognised)
            )

        for role, zone_map in ((_STAFF_ROLE, staff_zones), (_CUSTOMER_ROLE, customer_zones)):
            for counter_id, polygon in sorted(zone_map.items(), key=lambda kv: int(kv[0])):
                if not isinstance(polygon, (list, tuple)) or len(polygon) < 3:
                    violations.append(f"{role}_{counter_id} must have at least 3 points")
                    continue
                for i, point in enumerate(polygon):
                    if not isinstance(point, (list, tuple)) or len(point) != 2:
                        violations.append(
                            f"{role}_{counter_id} point {i} must have exactly 2 coordinates"
                        )

        return violations

    def _prepare_counter_zones(
        self,
        config: CustomerServiceConfig,
        stream_info: Optional[Dict[str, Any]],
    ) -> List[str]:
        """Resolve, split and validate counter zones. Returns violations (empty == OK)."""
        self._normalize_zone_config_and_params(config)

        # First frame: try a blocking resolve so a deployment whose zones live
        # only in the API is not failed before they arrive, then hand off to the
        # background thread. Ordering matters -- validating first would reject a
        # perfectly good camera on frame 1.
        if not self._zone_resolution_attempted:
            self._zone_resolution_attempted = True
            if stream_info:
                try:
                    resolved = self._resolve_geometry_from_api(config, stream_info)
                    if resolved is not None and resolved.zone_config is not None:
                        config.zone_config = resolved.zone_config
                    else:
                        self._start_geometry_resolver(config, stream_info)
                except Exception as exc:  # noqa: BLE001 - network/API boundary on the hot path
                    # Deliberately blind: an API round-trip on the first frame
                    # must never be able to fail the frame; the supplied
                    # zone_config is a complete fallback.
                    self.logger.warning(
                        "AdvancedCustomerService: first-frame geometry resolve raised (%s); "
                        "using zone_config from the supplied config",
                        exc,
                    )
                    self._start_geometry_resolver(config, stream_info)
            else:
                self.logger.info(
                    "AdvancedCustomerService: no stream_info on first frame; using zone_config from config"
                )
        elif (
            self._resolved_geometry_cache is not None
            and self._resolved_geometry_cache.zone_config is not None
        ):
            config.zone_config = self._resolved_geometry_cache.zone_config

        zones = {}
        if config.zone_config is not None and getattr(config.zone_config, "zones", None):
            zones = config.zone_config.zones

        staff_zones, customer_zones, unrecognised = self._split_zones_by_role(zones)
        violations = self._validate_counter_zones(staff_zones, customer_zones, unrecognised)
        if violations:
            return violations

        self._staff_zones = staff_zones
        self._customer_zones = customer_zones
        self._counter_ids = sorted(customer_zones.keys(), key=int)
        return []

    def _zone_test_point(self, detection: Dict[str, Any], stream_info: Optional[Dict[str, Any]]):
        """Point used for zone membership: the bbox CENTRE, scaled if normalized.

        Deliberately the centre, not the bottom-centre that intrusion_detection
        uses. A partially occluded person in a crowded queue often has no visible
        feet, so a foot point is extrapolated and unstable; the centre degrades
        far more gracefully. ``to_zone_test_point`` is still required because zone
        polygons are pixel space while detections may be normalized 0-1, and an
        unscaled normalized point reads as permanently outside every zone.

        Returns ``None`` when the bbox is missing or unusable. ``get_bbox_center``
        returns ``(0, 0)`` for an unrecognised bbox, and ``(0, 0)`` is a truthy
        tuple, so a plain ``if not centre`` guard silently treats such a detection
        as standing at the frame origin.
        """
        bbox = detection.get("bounding_box", detection.get("bbox"))
        if not bbox:
            return None
        if isinstance(bbox, dict):
            keys = set(bbox)
            if not ({"xmin", "ymin", "xmax", "ymax"} <= keys or {"x1", "y1", "x2", "y2"} <= keys):
                return None
        elif isinstance(bbox, (list, tuple)):
            if len(bbox) < 4:
                return None
        else:
            return None
        centre = get_bbox_center(bbox)
        return to_zone_test_point(centre, bbox, stream_info)

    # ------------------------------------------------------------------ #
    # Relabel + zone membership (R1/R3/R4)                               #
    # ------------------------------------------------------------------ #

    def _prepare_zone_membership_frame(
        self,
    ) -> Tuple[Dict[str, List[Tuple[float, float]]], Dict[str, List[Tuple[float, float]]]]:
        """Per-frame setup for ``_update_zone_membership``.

        Ensures a state bucket exists for every counter, clears the
        seen-this-frame sets (which are per-frame by definition, unlike
        ``_cz_members`` / ``_sz_members``, which are retained across frames by
        the hysteresis), and returns the staff/customer polygons as coordinate
        pairs. Split out to keep the caller under the org complexity cap.
        """
        for counter_id in self._counter_ids:
            self._cz_inside_frames.setdefault(counter_id, {})
            self._cz_outside_frames.setdefault(counter_id, {})
            self._cz_entry_time.setdefault(counter_id, {})
            self._sz_inside_frames.setdefault(counter_id, {})
            self._sz_outside_frames.setdefault(counter_id, {})
            self._cz_members.setdefault(counter_id, set())
            self._sz_members.setdefault(counter_id, set())
        self._cz_current_tracks = {counter_id: set() for counter_id in self._counter_ids}
        self._sz_current_tracks = {counter_id: set() for counter_id in self._counter_ids}
        self._cz_raw_tracks = {counter_id: set() for counter_id in self._counter_ids}
        self._sz_raw_tracks = {counter_id: set() for counter_id in self._counter_ids}

        staff_polys = {
            counter_id: [(p[0], p[1]) for p in polygon]
            for counter_id, polygon in self._staff_zones.items()
        }
        customer_polys = {
            counter_id: [(p[0], p[1]) for p in polygon]
            for counter_id, polygon in self._customer_zones.items()
        }
        return staff_polys, customer_polys

    def _geometry_pass(
        self,
        detections: List[Dict[str, Any]],
        staff_polys: Dict[str, List[Tuple[float, float]]],
        customer_polys: Dict[str, List[Tuple[float, float]]],
        stream_info: Optional[Dict[str, Any]],
    ) -> List[Tuple[Dict[str, Any], Any, set, set]]:
        """Test every detection against every zone polygon, once.

        Returns ``[(detection, track_id, staff_hits, customer_hits), ...]`` for
        the detections that can be placed at all -- a detection with no track id
        or no derivable zone-test point is skipped, since neither hysteresis nor
        membership can be attributed without those.

        Also records the RAW geometric occupancy of each polygon this frame, in
        ``_sz_raw_tracks`` / ``_cz_raw_tracks``. This is the only point in the
        pipeline where that reading exists (everything downstream is debounced
        and role-filtered), and it is what ``zone_analysis[...].original_counts``
        publishes.

        Split out of ``_update_zone_membership`` so that method stays within the
        org complexity cap; behaviour is unchanged and it has no other caller.
        """
        usable: List[Tuple[Dict[str, Any], Any, set, set]] = []
        for detection in detections:
            track_id = detection.get("track_id")
            if track_id is None:
                continue
            centre = self._zone_test_point(detection, stream_info)
            if centre is None:
                continue
            staff_hits = {
                cid for cid, poly in staff_polys.items() if point_in_polygon(centre, poly)
            }
            customer_hits = {
                cid for cid, poly in customer_polys.items() if point_in_polygon(centre, poly)
            }
            for cid in staff_hits:
                self._sz_raw_tracks.setdefault(cid, set()).add(track_id)
            for cid in customer_hits:
                self._cz_raw_tracks.setdefault(cid, set()).add(track_id)
            usable.append((detection, track_id, staff_hits, customer_hits))
        return usable

    def _update_zone_membership(
        self,
        detections: List[Dict[str, Any]],
        config: CustomerServiceConfig,
        stream_info: Optional[Dict[str, Any]],
    ) -> Tuple[List[Dict], List[Dict]]:
        """Relabel every detection staff/customer and refresh counter membership.

        Replaces ``assign_person_by_area`` + ``_categorize_detections``. Returns
        ``(staff_detections, customer_detections)``.

        Label order is load-bearing. A counter zone spans the desk, so a staff
        member standing behind it is geometrically inside ``customer_<i>``. Staff
        must therefore be identified and excluded BEFORE customer membership is
        counted, or every staffed counter reports a phantom customer and reads
        permanently active.
        """
        min_inside_default = max(1, int(config.min_inside_frames))
        exit_grace_default = max(1, int(config.exit_grace_frames))
        now = self._current_clock()

        def _mi(zone_name: str) -> int:
            return max(1, int(self._zone_param(zone_name, "min_inside_frames", min_inside_default)))

        def _eg(zone_name: str) -> int:
            return max(1, int(self._zone_param(zone_name, "exit_grace_frames", exit_grace_default)))

        staff_polys, customer_polys = self._prepare_zone_membership_frame()

        usable = self._geometry_pass(detections, staff_polys, customer_polys, stream_info)

        # --- staff zone hysteresis, then the sticky staff label ---
        for _detection, track_id, staff_hits, _customer_hits in usable:
            for counter_id in self._counter_ids:
                zone_name = f"staff_{counter_id}"
                if counter_id in staff_hits:
                    self._sz_inside_frames[counter_id][track_id] = (
                        self._sz_inside_frames[counter_id].get(track_id, 0) + 1
                    )
                    self._sz_outside_frames[counter_id].pop(track_id, None)
                    if self._sz_inside_frames[counter_id][track_id] >= _mi(zone_name):
                        self._sz_current_tracks[counter_id].add(track_id)
                        self._sz_members[counter_id].add(track_id)
                        # Sticky (R1): once seen working a counter, this track stays
                        # staff even when it walks through a customer zone. Evicted
                        # only after presence_grace_frames away from frame.
                        self.persistent_staff_ids.add(track_id)
                        self.global_staff_ids.add(track_id)
                        # Revoke any customer identity earned earlier. A track that
                        # stood in the customer zone before stepping behind the desk
                        # was a staff member the whole time; leaving it in
                        # global_customer_ids inflates unique_customers permanently.
                        # unique_customers can therefore step DOWN on a promotion --
                        # the bridge's window delta clamps at 0, so a correction
                        # costs at most an undercount in the window it lands in,
                        # never a negative reading.
                        self.persistent_customer_ids.discard(track_id)
                        self.global_customer_ids.discard(track_id)
                else:
                    outside = self._sz_outside_frames[counter_id].get(track_id, 0) + 1
                    self._sz_outside_frames[counter_id][track_id] = outside
                    if outside >= _eg(zone_name):
                        self._sz_inside_frames[counter_id].pop(track_id, None)
                        self._sz_outside_frames[counter_id].pop(track_id, None)
                        self._sz_members[counter_id].discard(track_id)

        # --- customer zone hysteresis, non-staff only ---
        # Runs BEFORE the labelling pass, which is the fix for the staff-counted-
        # as-customer miscount. It used to run after, gated on the customer label,
        # which meant the label had to be committed first -- and the only way to
        # commit it before the zone had confirmed anything was to default every
        # unconfirmed track to "customer". Same set of tracks is processed here
        # (non-staff == what used to be labelled customer), so membership itself is
        # unchanged; only the moment a role is committed moves.
        for _detection, track_id, _staff_hits, customer_hits in usable:
            if track_id in self.persistent_staff_ids:
                # A confirmed staff member inside a customer zone must not hold
                # membership there. Drop any residual counters so a promoted track
                # cannot keep occupying a counter as a phantom customer.
                for counter_id in self._counter_ids:
                    self._cz_inside_frames[counter_id].pop(track_id, None)
                    self._cz_outside_frames[counter_id].pop(track_id, None)
                    self._cz_entry_time[counter_id].pop(track_id, None)
                    self._cz_members[counter_id].discard(track_id)
                continue
            for counter_id in self._counter_ids:
                zone_name = f"customer_{counter_id}"
                if counter_id in customer_hits:
                    self._cz_inside_frames[counter_id][track_id] = (
                        self._cz_inside_frames[counter_id].get(track_id, 0) + 1
                    )
                    self._cz_outside_frames[counter_id].pop(track_id, None)
                    if self._cz_inside_frames[counter_id][track_id] >= _mi(zone_name):
                        self._cz_current_tracks[counter_id].add(track_id)
                        self._cz_members[counter_id].add(track_id)
                        # setdefault, never overwrite: the entry time is what FIFO
                        # serving orders on, so re-stamping it every frame would
                        # make everyone permanently equal-oldest.
                        self._cz_entry_time[counter_id].setdefault(track_id, now)
                else:
                    outside = self._cz_outside_frames[counter_id].get(track_id, 0) + 1
                    self._cz_outside_frames[counter_id][track_id] = outside
                    if outside >= _eg(zone_name):
                        self._cz_inside_frames[counter_id].pop(track_id, None)
                        self._cz_outside_frames[counter_id].pop(track_id, None)
                        self._cz_entry_time[counter_id].pop(track_id, None)
                        self._cz_members[counter_id].discard(track_id)

        # --- labelling pass: commit a role only once a zone has confirmed one ---
        # Three outcomes, not two. A track that has been in frame for fewer than
        # min_inside_frames -- or that has simply never held a zone long enough --
        # is PENDING: drawn, but counted as neither staff nor customer. Anything
        # else guesses, and the cheapest guess ("not staff yet, so customer") is
        # exactly the miscount this replaces.
        staff_detections: List[Dict] = []
        customer_detections: List[Dict] = []
        for detection, track_id, _staff_hits, _customer_hits in usable:
            if track_id in self.persistent_staff_ids:
                detection["category"] = _STAFF_ROLE
                staff_detections.append(detection)
                continue
            if any(track_id in members for members in self._cz_members.values()):
                self.persistent_customer_ids.add(track_id)
            if track_id in self.persistent_customer_ids:
                detection["category"] = _CUSTOMER_ROLE
                customer_detections.append(detection)
                self.global_customer_ids.add(track_id)
            else:
                detection["category"] = _PENDING_ROLE

        self._evict_absent_tracks(detections, config)
        return staff_detections, customer_detections

    def _evict_absent_tracks(
        self, detections: List[Dict[str, Any]], config: CustomerServiceConfig
    ) -> None:
        """Purge tracks that have been gone from frame for presence_grace_frames.

        Absence from the frame is different from being outside a zone: a track lost
        to occlusion should keep its zone membership and its entry timestamp for a
        while, because it is the same person. Without an eviction bound, though,
        every dict here grows for the life of the process, and ``persistent_staff_ids``
        would mark a track staff forever (ACS-03 / ACS-07).
        """
        presence_grace = max(0, int(config.presence_grace_frames))
        present = {
            d.get("track_id")
            for d in detections
            if isinstance(d, dict) and d.get("track_id") is not None
        }

        for track_id in present:
            self._track_absent_frames.pop(track_id, None)

        known = set(self._track_absent_frames)
        for counter_id in self._counter_ids:
            known |= set(self._cz_inside_frames.get(counter_id, {}))
            known |= set(self._sz_inside_frames.get(counter_id, {}))
            known |= set(self._cz_entry_time.get(counter_id, {}))
        known |= set(self.persistent_staff_ids)
        known |= set(self.persistent_customer_ids)

        for track_id in known - present:
            absent = self._track_absent_frames.get(track_id, 0) + 1
            self._track_absent_frames[track_id] = absent
            if absent < presence_grace:
                continue
            for counter_id in self._counter_ids:
                self._cz_inside_frames.get(counter_id, {}).pop(track_id, None)
                self._cz_outside_frames.get(counter_id, {}).pop(track_id, None)
                self._cz_entry_time.get(counter_id, {}).pop(track_id, None)
                self._sz_inside_frames.get(counter_id, {}).pop(track_id, None)
                self._sz_outside_frames.get(counter_id, {}).pop(track_id, None)
                self._cz_members.get(counter_id, set()).discard(track_id)
                self._sz_members.get(counter_id, set()).discard(track_id)
            self.persistent_staff_ids.discard(track_id)
            # The sticky customer label is dropped on the same schedule as the
            # sticky staff one. global_customer_ids is NOT touched -- that is the
            # session's unique-customer tally and a customer who leaves has still
            # been a customer.
            self.persistent_customer_ids.discard(track_id)
            self._track_absent_frames.pop(track_id, None)

    # ------------------------------------------------------------------ #
    # Counter state machine + journey lifecycle (R6, D-01, D-06)         #
    # ------------------------------------------------------------------ #

    def _pick_served_track(self, counter_id: str, members: set) -> Optional[Any]:
        """The customer being served at this counter: the longest present (FIFO).

        D-06. A queue is FIFO, and presence duration is far more robust in a
        crowded, occluded scene than any geometric "closest to the desk" test.
        Ties (identical entry timestamps, possible when several tracks confirm on
        the same frame) break on track id so the choice is deterministic rather
        than dependent on set iteration order.
        """
        entries = self._cz_entry_time.get(counter_id, {})
        candidates = [
            (entries.get(track_id), track_id) for track_id in members if track_id in entries
        ]
        if not candidates:
            return None
        return min(candidates, key=lambda pair: (pair[0], str(pair[1])))[1]

    def _update_counter_state(self, current_time: float) -> None:
        """Refresh per-counter occupancy/serving and drive journey transitions."""
        self._frame_new_customer_ids = []
        self._frame_served_ids = []
        self._frame_abandoned_ids = []
        self._counter_status = {}

        previous_membership = dict(self._customer_counter)
        new_membership: Dict[Any, str] = {}

        for counter_id in self._counter_ids:
            # RETAINED membership, so an occluded customer does not momentarily
            # shorten the queue.
            customer_members = set(self._cz_members.get(counter_id, set()))
            staff_members = set(self._sz_members.get(counter_id, set()))
            is_staffed = bool(staff_members)

            # Service requires staff presence: an unstaffed counter has everyone
            # queuing and nobody served. That is what makes serving_counters a real
            # measurement rather than a restatement of active_counters.
            served_track = (
                self._pick_served_track(counter_id, customer_members) if is_staffed else None
            )
            self._counter_served_track[counter_id] = served_track

            occupancy = len(customer_members)
            queue_depth = occupancy - 1 if served_track is not None else occupancy

            for track_id in customer_members:
                new_membership[track_id] = counter_id

            self._counter_status[counter_id] = {
                "customers": occupancy,
                "queue_depth": max(0, queue_depth),
                "is_active": occupancy > 0,
                "is_staffed": is_staffed,
                "staff_count": len(staff_members),
                "served_track_id": served_track,
            }
            if served_track is not None:
                self._frame_served_ids.append(served_track)

        # --- journeys for customers currently at a counter ---
        for track_id, counter_id in new_membership.items():
            journey = self.customer_journey.get(track_id)
            if journey is None:
                journey = self._new_journey(track_id, counter_id, current_time)
                self._frame_new_customer_ids.append(track_id)
            journey["counter_id"] = counter_id
            journey["last_seen"] = current_time
            journey["areas_visited"].add(f"customer_{counter_id}")

            if self._counter_served_track.get(counter_id) == track_id:
                if journey["first_served_at"] is None:
                    # Stamped ONCE. Staff stepping away and returning must not
                    # restart the clock or re-count the service.
                    journey["first_served_at"] = current_time
                journey["state"] = self.JOURNEY_STATES["BEING_SERVED"]
            else:
                journey["state"] = self.JOURNEY_STATES["QUEUING"]

        # --- exits: R6, split by whether they were ever served ---
        for track_id in previous_membership:
            if track_id in new_membership:
                continue
            journey = self.customer_journey.pop(track_id, None)
            if journey is None:
                continue
            entry_time = journey.get("entry_time", current_time)
            first_served_at = journey.get("first_served_at")
            if first_served_at is not None:
                # Served, then left -> a completed service.
                self._total_customers_served += 1
                self._record_duration(
                    self._wait_durations, max(0.0, first_served_at - entry_time), "wait"
                )
                self._record_duration(
                    self._service_durations, max(0.0, current_time - first_served_at), "service"
                )
            else:
                # Left while still queuing -> balked. This split is the whole
                # difference between "served and departed" and "gave up", and it is
                # what makes an abandonment rate possible at all.
                self._total_abandoned += 1
                self._frame_abandoned_ids.append(track_id)

        self._customer_counter = new_membership

    def _new_journey(self, track_id: Any, counter_id: str, current_time: float) -> Dict[str, Any]:
        """Create a journey record. Evicted on exit, so this stays bounded."""
        journey = {
            "state": self.JOURNEY_STATES["ENTERING"],
            "counter_id": counter_id,
            "entry_time": current_time,
            "last_seen": current_time,
            "first_served_at": None,
            "areas_visited": set(),
        }
        self.customer_journey[track_id] = journey
        return journey

    def _record_duration(self, ring: List[float], value: float, kind: str) -> None:
        """Append to a bounded ring and update the running maximum.

        The maximum is tracked separately because it must survive the ring
        discarding old samples -- a session maximum that silently drops when the
        ring rolls over would be wrong, not merely stale.
        """
        ring.append(value)
        if len(ring) > self._max_duration_samples:
            del ring[: -self._max_duration_samples]
        if kind == "wait":
            self._max_wait_seconds = max(self._max_wait_seconds, value)
        else:
            self._max_service_seconds = max(self._max_service_seconds, value)

    def _resolve_analytics_now(self, stream_info: Optional[Dict[str, Any]]) -> float:
        """Resolve the clock that every duration metric is measured against.

        Wait, service and journey durations must advance with the *stream*, not
        with wall-clock processing time. An offline video processed faster than
        realtime otherwise reports service times of a few milliseconds for an
        interaction lasting hundreds of frames, and a backlogged live stream
        reports inflated ones. Derived as ``start_frame / original_fps`` when the
        stream exposes both; falls back to wall clock otherwise, which keeps
        realtime behaviour unchanged for callers that pass no frame information.
        """
        if stream_info:
            input_settings = stream_info.get("input_settings", {}) or {}
            frame = input_settings.get("start_frame")
            fps = input_settings.get("original_fps") or stream_info.get("fps")
            if frame is not None and frame != "na" and fps:
                try:
                    fps_value = float(fps)
                    if fps_value > 0:
                        return float(frame) / fps_value
                except (TypeError, ValueError):
                    pass
        return time.time()

    def _current_clock(self) -> float:
        """Clock for the frame in flight, falling back to wall time off-cycle."""
        return self._now if self._now is not None else time.time()

    def _extract_detections(self, data: Any) -> List[Dict[str, Any]]:
        """Extract detections from processed data."""
        detections = []

        try:
            if isinstance(data, list):
                # Direct detection list
                detections = [d for d in data if isinstance(d, dict)]
            elif isinstance(data, dict):
                # Frame-based or structured data
                for value in data.values():
                    if isinstance(value, list):
                        detections.extend([d for d in value if isinstance(d, dict)])
                    elif isinstance(value, dict) and any(
                        k in value for k in ["bbox", "bounding_box", "category"]
                    ):
                        detections.append(value)
        except (AttributeError, TypeError, ValueError, KeyError) as e:
            self.logger.warning(f"Failed to extract detections: {str(e)}")

        return detections

    # _categorize_detections was removed here. Role no longer comes from the
    # model's class name matched against staff_categories / customer_categories --
    # it comes from which counter zone a track is confirmed in
    # (_update_zone_membership), so the category lists are not consulted at all.
    # Its sticky-staff bookkeeping moved there too, where it is now bounded by
    # presence_grace_frames instead of growing for the life of the process.

    def _process_comprehensive_analytics(
        self,
        staff_detections: List[Dict],
        customer_detections: List[Dict],
        _config: CustomerServiceConfig,
        current_time: float,
    ) -> Dict[str, Any]:
        """Process comprehensive customer service analytics.

        Zone membership and role assignment already happened in
        ``_update_zone_membership``; this drives the per-counter state machine and
        the customer journey lifecycle off that membership, then compiles results.
        The old area-occupancy passes are gone -- occupancy is now per counter zone
        and computed once, rather than per role and then filtered, which is what
        made a service area depend on being contained by another zone.
        """
        _ = (_config, staff_detections, customer_detections)
        self._update_counter_state(current_time)
        return self._compile_analytics_results(current_time)

    # The area-occupancy pipeline was removed here:
    #   _process_staff_detections, _process_customer_detections,
    #   _initialize_customer_journey, _update_customer_journey_state,
    #   _is_customer_being_served, _find_nearest_staff,
    #   _update_service_interactions
    #
    # All seven implemented the retired customer_areas / staff_areas /
    # service_areas model. Occupancy is now computed ONCE per counter zone in
    # _update_zone_membership and read from the retained member sets, rather than
    # being accumulated per role and then re-tested against a third set of
    # polygons -- which is what silently required each service area to be
    # geometrically contained by both a customer area and a staff area.
    # Serving identity no longer uses staff proximity, so there is no
    # nearest-staff search and no pixel distance threshold.

    def _compile_analytics_results(self, current_time: float) -> Dict[str, Any]:
        """Compile analytics from per-counter state."""
        queue = self._get_customer_queue_results()
        staff = self._get_staff_management_results()
        counters = self._get_counter_results()
        journey = self._get_customer_journey_results()
        return {
            "customer_queue_analytics": queue,
            "staff_management_analytics": staff,
            "counter_analytics": counters,
            "customer_journey_analytics": journey,
            "business_metrics": self._calculate_analytics(queue, staff, counters),
            "processing_timestamp": current_time,
        }

    def _counter_totals(self) -> Dict[str, int]:
        """Site-level roll-up of the per-counter snapshot."""
        statuses = self._counter_status.values()
        queue_depths = [s["queue_depth"] for s in statuses]
        return {
            "total_counters": len(self._counter_ids),
            "active_counters": sum(1 for s in statuses if s["is_active"]),
            "staffed_counters": sum(1 for s in statuses if s["is_staffed"]),
            "serving_counters": sum(1 for s in statuses if s["served_track_id"] is not None),
            "customers_at_counters": sum(s["customers"] for s in statuses),
            "total_queue_length": sum(queue_depths),
            "max_queue_length": max(queue_depths) if queue_depths else 0,
        }

    def _get_customer_queue_results(self) -> Dict[str, Any]:
        """Queue analytics.

        ``queue_lengths_by_area`` is deliberately gone: it was a dict, and a VOLUME
        metric carries one scalar, so it could never be published. The per-counter
        breakdown lives in ``counter_analytics.counters`` and the publishable
        aggregates are the scalars below.
        """
        totals = self._counter_totals()
        waits = self._wait_durations
        services = self._service_durations
        return {
            "active_customers": len(self._customer_counter),
            "customers_queuing": totals["total_queue_length"],
            "customers_at_counters": totals["customers_at_counters"],
            "total_queue_length": totals["total_queue_length"],
            "max_queue_length": totals["max_queue_length"],
            "total_customers_served": self._total_customers_served,
            "total_abandoned": self._total_abandoned,
            "avg_wait_seconds": round(sum(waits) / len(waits), 2) if waits else 0.0,
            "max_wait_seconds": round(self._max_wait_seconds, 2),
            "avg_service_seconds": round(sum(services) / len(services), 2) if services else 0.0,
            "max_service_seconds": round(self._max_service_seconds, 2),
        }

    def _get_staff_management_results(self) -> Dict[str, Any]:
        """Staff analytics, derived from staff-zone membership."""
        totals = self._counter_totals()
        staff_now = {tid for members in self._sz_members.values() for tid in members}
        total_counters = max(1, totals["total_counters"])
        return {
            "active_staff": len(staff_now),
            "total_staff": len(self.global_staff_ids),
            "staffed_counters": totals["staffed_counters"],
            "staff_coverage": round(totals["staffed_counters"] / total_counters * 100.0, 2),
            "staff_distribution": {
                "staff_{}".format(cid): len(self._sz_members.get(cid, set()))
                for cid in self._counter_ids
            },
        }

    def _get_counter_results(self) -> Dict[str, Any]:
        """Per-counter detail plus its site-level roll-up.

        Replaces ``service_area_analytics``. Because occupancy is read straight
        from each zone own member set, a counter reports correctly whether or not
        any other polygon happens to overlap it.
        """
        totals = self._counter_totals()
        total_counters = max(1, totals["total_counters"])
        return {
            **totals,
            "counter_utilization": round(totals["active_counters"] / total_counters * 100.0, 2),
            "counters": {cid: dict(status) for cid, status in self._counter_status.items()},
        }

    def _get_zone_analysis(self) -> Dict[str, Dict[str, Any]]:
        """Per-raw-zone detail, keyed by the drawn zone name (``customer_<id>`` /
        ``staff_<id>``) -- the ``zone_analysis`` side channel intrusion_detection
        also emits, in the same per-zone shape (``current_count``, ``total_count``,
        ``current_track_ids``, ``original_counts``, ``zone_coords``).

        Unlike intrusion_detection (single flat ``zones`` dict, geometry retested
        here via ``count_objects_in_zones`` + ``_update_zone_tracking``), ACS
        already computes both readings per counter zone in
        ``_update_zone_membership`` -- ``_cz_members`` / ``_sz_members`` (retained,
        debounced) and ``_cz_raw_tracks`` / ``_sz_raw_tracks`` (raw geometric
        membership this frame). This reuses that state rather than re-testing
        geometry a second time.

        ``current_count``/``current_track_ids`` come from the retained (debounced)
        member sets, matching intrusion_detection's post-``_update_zone_tracking``
        semantics. ``original_counts`` is the ACS analogue of intrusion_detection's
        pre-debounce ``count_objects_in_zones`` output: raw geometric occupancy of
        the polygon this frame, one scalar keyed by the zone's role. It is
        deliberately NOT taken from ``_cz_current_tracks`` -- that set is only
        populated once hysteresis has confirmed, so it would read 0 for an entrant
        still inside its confirmation window and could never exceed
        ``current_count``, which is the entire point of publishing a pre-debounce
        number beside a debounced one.

        The two therefore differ in both directions, and that is the signal:
        ``original_counts`` above ``current_count`` means someone is inside the
        polygon but not yet confirmed (or is staff standing in a customer zone);
        below it means a confirmed member is currently occluded and being held by
        ``exit_grace_frames``.

        ``total_count`` is a lifetime-unique count per raw zone name -- tracked in
        ``_zone_total_track_ids``, the same bounded-only-by-session-length pattern
        intrusion_detection's own ``_zone_total_track_ids`` uses.
        """
        zone_analysis: Dict[str, Dict[str, Any]] = {}
        for counter_id in self._counter_ids:
            customer_zone_name = f"customer_{counter_id}"
            confirmed_customers = self._cz_members.get(counter_id, set())
            self._zone_total_track_ids.setdefault(customer_zone_name, set()).update(
                confirmed_customers
            )
            zone_analysis[customer_zone_name] = {
                "current_count": len(confirmed_customers),
                "total_count": len(self._zone_total_track_ids[customer_zone_name]),
                "current_track_ids": list(confirmed_customers),
                "original_counts": {
                    _CUSTOMER_ROLE: len(self._cz_raw_tracks.get(counter_id, set()))
                },
                "zone_coords": list(self._customer_zones.get(counter_id, [])),
            }

            staff_zone_name = f"staff_{counter_id}"
            confirmed_staff = self._sz_members.get(counter_id, set())
            self._zone_total_track_ids.setdefault(staff_zone_name, set()).update(confirmed_staff)
            zone_analysis[staff_zone_name] = {
                "current_count": len(confirmed_staff),
                "total_count": len(self._zone_total_track_ids[staff_zone_name]),
                "current_track_ids": list(confirmed_staff),
                "original_counts": {_STAFF_ROLE: len(self._sz_raw_tracks.get(counter_id, set()))},
                "zone_coords": list(self._staff_zones.get(counter_id, [])),
            }
        return zone_analysis

    def _get_customer_journey_results(self) -> Dict[str, Any]:
        """Journey analytics over the live (non-evicted) journeys."""
        journey_states = {state: 0 for state in self.JOURNEY_STATES.values()}
        for journey in self.customer_journey.values():
            state = journey.get("state")
            if state in journey_states:
                journey_states[state] += 1
        # Terminal states are evicted on exit, so their live count is always 0;
        # the cumulative session totals carry that information instead.
        journey_states[self.JOURNEY_STATES["COMPLETED"]] = self._total_customers_served
        journey_states[self.JOURNEY_STATES["LEFT"]] = self._total_abandoned

        popular: Dict[str, int] = defaultdict(int)
        for journey in self.customer_journey.values():
            for area in journey.get("areas_visited", set()):
                popular[area] += 1

        return {
            "total_journeys": len(self.customer_journey),
            "unique_customers": len(self.global_customer_ids),
            "journey_states": journey_states,
            "popular_areas": dict(sorted(popular.items(), key=lambda kv: -kv[1])),
        }

    def _calculate_analytics(
        self,
        queue: Dict[str, Any],
        staff: Dict[str, Any],
        counters: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Business metrics.

        ``service_efficiency`` / ``staff_utilization`` / ``overall_performance``
        are gone from this dict. Each divided a windowed numerator by an all-time
        denominator, so over a long stream they drifted regardless of real
        performance and latched their alerts on permanently. What replaces them is
        windowed by construction: an abandonment rate over resolved outcomes, and
        utilisation over the fixed counter count.
        """
        resolved = self._total_customers_served + self._total_abandoned
        return {
            "customer_to_staff_ratio": round(
                queue["active_customers"] / max(staff["active_staff"], 1), 2
            ),
            "counter_utilization": counters["counter_utilization"],
            "staff_coverage": staff["staff_coverage"],
            "abandonment_rate": round(self._total_abandoned / resolved * 100.0, 2)
            if resolved
            else 0.0,
            "avg_queue_length": round(
                queue["total_queue_length"] / max(1, counters["total_counters"]), 2
            ),
        }

    def _compute_severity_level(self, queue_depth: int, level_settings: Dict[str, int]) -> str:
        """Map the worst single counter queue depth onto a severity band.

        Per counter, not the site-wide sum: many short queues are not the same
        condition as one long one, and only the latter is worth escalating.

        Bands are read from ``level_settings`` (the same dict published on the
        incident) and evaluated highest-first, so the thresholds and the
        rendered severity can never disagree. Returns "info" below the lowest
        band, matching the previous default.
        """
        severity = "info"
        for level in ("low", "medium", "significant", "critical"):
            threshold = level_settings.get(level)
            if threshold is not None and queue_depth >= threshold:
                severity = level
        return severity

    def _check_alerts(self, analytics_results: Dict, config: CustomerServiceConfig) -> List[Dict]:
        """Alerts for ``result.summary``.

        Delegates to the same ``_build_alerts`` the agg_summary payload uses, so
        the two surfaces cannot disagree. They previously had different gating
        (this one bailed out entirely when ``alert_config`` was None, the payload
        path ignored it) and a different rule set, so the summary could report an
        alert the payload did not and vice versa.
        """
        alerts, _settings = self._build_alerts(
            config,
            analytics_results.get("customer_queue_analytics", {}),
            analytics_results.get("counter_analytics", {}),
        )
        return alerts

    def _build_human_text(
        self,
        current_timestamp: str,
        queue: Dict[str, Any],
        staff: Dict[str, Any],
        counters: Dict[str, Any],
    ) -> str:
        """Operator-facing per-frame summary."""
        lines = [f"CURRENT FRAME @ {current_timestamp}:"]
        lines.append(f"\t- Customers: {queue.get('active_customers', 0)}")
        lines.append(f"\t\t- Waiting: {counters.get('total_queue_length', 0)}")
        lines.append(f"\t\t- Being served: {counters.get('serving_counters', 0)}")
        lines.append(f"\t- Staff on counters: {staff.get('active_staff', 0)}")
        lines.append(
            f"\t- Counters: {counters.get('active_counters', 0)} active / "
            f"{counters.get('staffed_counters', 0)} staffed / {counters.get('total_counters', 0)} total"
        )
        for counter_id, status in sorted(
            (counters.get("counters") or {}).items(),
            key=lambda kv: int(kv[0]) if str(kv[0]).isdigit() else 0,
        ):
            state = "serving" if status.get("served_track_id") is not None else "idle"
            if status.get("is_active") and not status.get("is_staffed"):
                state = "UNSTAFFED"
            lines.append(
                f"\t\t- counter {counter_id}: {state}, "
                f"{status.get('customers', 0)} present, {status.get('queue_depth', 0)} waiting"
            )
        lines.append("")
        return "\n".join(lines)

    def _generate_insights(
        self, analytics_results: Dict, _config: CustomerServiceConfig
    ) -> List[str]:
        """Actionable insights from the counter model."""
        _ = (_config,)
        insights: List[str] = []
        queue = analytics_results.get("customer_queue_analytics", {})
        staff = analytics_results.get("staff_management_analytics", {})
        counters = analytics_results.get("counter_analytics", {})
        metrics = analytics_results.get("business_metrics", {})

        total_counters = counters.get("total_counters", 0)
        active = counters.get("active_counters", 0)
        staffed = counters.get("staffed_counters", 0)
        serving = counters.get("serving_counters", 0)

        if queue.get("active_customers", 0) == 0:
            insights.append("No customers at any counter")
            return insights

        insights.append(
            f"{queue.get('active_customers', 0)} customer(s) at {active}/{total_counters} counters"
        )
        if serving:
            insights.append(f"🔄 {serving} counter(s) actively serving")

        waiting = counters.get("total_queue_length", 0)
        if waiting:
            insights.append(
                f"📊 {waiting} customer(s) waiting, worst counter {counters.get('max_queue_length', 0)}"
            )

        # The condition that actually costs money: someone waiting at a desk
        # nobody is working.
        unstaffed_busy = [
            cid
            for cid, s in (counters.get("counters") or {}).items()
            if s.get("is_active") and not s.get("is_staffed")
        ]
        if unstaffed_busy:
            insights.append(
                "⚠️ Customers waiting at unstaffed counter(s): "
                + ", ".join(sorted(unstaffed_busy, key=lambda c: int(c) if str(c).isdigit() else 0))
            )

        if total_counters and staffed < total_counters:
            insights.append(
                f"{total_counters - staffed} counter(s) unstaffed ({staff.get('staff_coverage', 0.0)}% covered)"
            )

        avg_wait = queue.get("avg_wait_seconds", 0.0)
        if avg_wait > 300:
            insights.append(f"⚠️ Long average wait: {avg_wait / 60:.1f} min")
        elif avg_wait > 0:
            insights.append(f"⏱️ Average wait: {avg_wait / 60:.1f} min")

        avg_service = queue.get("avg_service_seconds", 0.0)
        if avg_service > 0:
            insights.append(f"Average service time: {avg_service / 60:.1f} min")

        abandon = metrics.get("abandonment_rate", 0.0)
        if abandon >= 20.0:
            insights.append(
                f"⚠️ High abandonment: {abandon}% of customers left without being served"
            )
        elif abandon > 0:
            insights.append(f"Abandonment rate: {abandon}%")

        return insights

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
        except (ValueError, TypeError, IndexError) as exc:
            # Non-fatal, and narrow on purpose: the block above only does string
            # splitting and formatting on a value already known to be a str, so
            # there is no failure mode here worth swallowing blindly. Falls
            # through to returning the cleaned string unchanged.
            self.logger.debug("AdvancedCustomerService: timestamp reformat failed (%s)", exc)

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
                # ACS-13: frame_id / original_fps was computed here, formatted as a
                # video offset into stream_time_str, logged, and then thrown away --
                # the return value below is the wall-clock stream_time either way.
                # Removed along with the arithmetic that fed it.
                return self._format_timestamp(
                    stream_info.get("input_settings", {}).get("stream_time", "NA")
                )
            else:
                return datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")

        if stream_info.get("input_settings", {}).get("start_frame", "na") != "na":
            # Same discarded computation as the precision branch above (ACS-13).
            return self._format_timestamp(
                stream_info.get("input_settings", {}).get("stream_time", "NA")
            )
        else:
            stream_time_str = (
                stream_info.get("input_settings", {}).get("stream_info", {}).get("stream_time", "")
            )
            if stream_time_str:
                try:
                    timestamp_str = stream_time_str.replace(" UTC", "")
                    dt = datetime.strptime(timestamp_str, "%Y-%m-%d-%H:%M:%S.%f")
                    timestamp = dt.replace(tzinfo=timezone.utc).timestamp()
                    return self._format_timestamp_for_stream(timestamp)
                except (ValueError, TypeError, AttributeError):
                    return self._format_timestamp_for_stream(time.time())
            else:
                return self._format_timestamp_for_stream(time.time())

    def _get_start_timestamp_str(
        self, stream_info: Optional[Dict[str, Any]], precision=False
    ) -> str:
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
                stream_time_str = (
                    stream_info.get("input_settings", {})
                    .get("stream_info", {})
                    .get("stream_time", "")
                )
                if stream_time_str:
                    try:
                        timestamp_str = stream_time_str.replace(" UTC", "")
                        dt = datetime.strptime(timestamp_str, "%Y-%m-%d-%H:%M:%S.%f")
                        self._tracking_start_time = dt.replace(tzinfo=timezone.utc).timestamp()
                        candidate = datetime.fromtimestamp(
                            self._tracking_start_time, timezone.utc
                        ).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")
                    except (ValueError, TypeError, AttributeError):
                        candidate = datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")
                else:
                    candidate = datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")
            self.start_timer = candidate
            return self._format_timestamp(self.start_timer)
        elif stream_info.get("input_settings", {}).get("start_frame", "na") == 1:
            candidate = stream_info.get("input_settings", {}).get("stream_time")
            if not candidate or candidate == "NA":
                stream_time_str = (
                    stream_info.get("input_settings", {})
                    .get("stream_info", {})
                    .get("stream_time", "")
                )
                if stream_time_str:
                    try:
                        timestamp_str = stream_time_str.replace(" UTC", "")
                        dt = datetime.strptime(timestamp_str, "%Y-%m-%d-%H:%M:%S.%f")
                        ts = dt.replace(tzinfo=timezone.utc).timestamp()
                        candidate = datetime.fromtimestamp(ts, timezone.utc).strftime(
                            "%Y-%m-%d-%H:%M:%S.%f UTC"
                        )
                    except (ValueError, TypeError, AttributeError):
                        candidate = datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")
                else:
                    candidate = datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")
            self.start_timer = candidate
            return self._format_timestamp(self.start_timer)

        else:
            if self.start_timer is not None and self.start_timer != "NA":
                return self._format_timestamp(self.start_timer)

            if self._tracking_start_time is None:
                stream_time_str = (
                    stream_info.get("input_settings", {})
                    .get("stream_info", {})
                    .get("stream_time", "")
                )
                if stream_time_str:
                    try:
                        timestamp_str = stream_time_str.replace(" UTC", "")
                        dt = datetime.strptime(timestamp_str, "%Y-%m-%d-%H:%M:%S.%f")
                        self._tracking_start_time = dt.replace(tzinfo=timezone.utc).timestamp()
                    except (ValueError, TypeError, AttributeError):
                        self._tracking_start_time = time.time()
                else:
                    self._tracking_start_time = time.time()

            dt = datetime.fromtimestamp(self._tracking_start_time, tz=timezone.utc)
            dt = dt.replace(minute=0, second=0, microsecond=0)
            return dt.strftime("%Y:%m:%d %H:%M:%S")

    # _format_timestamp_for_video was removed with ACS-13: its only two callers
    # formatted a value they then discarded.

    def _format_timestamp_for_stream(self, timestamp: float) -> str:
        dt = datetime.fromtimestamp(timestamp, tz=timezone.utc)
        return dt.strftime("%Y:%m:%d %H:%M:%S")

    def get_camera_info_from_stream(self, stream_info):
        """Extract camera_info from stream_info, matching people_counting pattern."""
        if not stream_info:
            return {}
        # Try to get camera_info directly
        camera_info = stream_info.get("camera_info")
        if camera_info:
            return camera_info
        # Fallback: try to extract from nested input_settings
        input_settings = stream_info.get("input_settings", {})
        for key in ["camera_info", "camera_id", "location", "site_id"]:
            if key in input_settings:
                return {key: input_settings[key]}
        return {}

    def _compute_iou(self, box1: Any, box2: Any) -> float:
        """Compute IoU between two bounding boxes."""

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
        """Return a stable canonical ID for a raw tracker ID."""
        if raw_id is None or bbox is None:
            return raw_id
        # Stream clock, so _track_merge_time_window is a window of stream seconds
        # and track aliasing replays deterministically for a given video.
        now = self._current_clock()
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

    def _update_tracking_state(self, detections: List[Dict]):
        """Track unique track_ids per category (staff/customer).
        Computes which track IDs are NEW (appeared for first time this frame).
        """
        target_categories = ["staff", "customer", "person"]
        if (
            not hasattr(self, "_per_category_total_track_ids")
            or self._per_category_total_track_ids is None
        ):
            self._per_category_total_track_ids = {cat: set() for cat in target_categories}
        if not hasattr(self, "_previous_frame_track_ids"):
            self._previous_frame_track_ids = {cat: set() for cat in target_categories}
        self._current_frame_track_ids = {cat: set() for cat in target_categories}

        for det in detections:
            cat = det.get("category")
            raw_track_id = det.get("track_id")
            if cat not in target_categories or raw_track_id is None:
                continue
            bbox = det.get("bounding_box", det.get("bbox"))
            canonical_id = self._merge_or_register_track(raw_track_id, bbox)
            det["track_id"] = canonical_id
            self._per_category_total_track_ids.setdefault(cat, set()).add(canonical_id)
            self._current_frame_track_ids[cat].add(canonical_id)

        # NEW track IDs = present in current frame but NOT in previous frame
        self._new_track_ids_this_frame = {
            cat: (
                self._current_frame_track_ids.get(cat, set())
                - self._previous_frame_track_ids.get(cat, set())
            )
            for cat in target_categories
        }

        # Snapshot current -> previous for next call
        self._previous_frame_track_ids = {
            cat: set(ids) for cat, ids in self._current_frame_track_ids.items()
        }

    def get_total_counts(self) -> Dict[str, int]:
        """Return total unique track counts per category."""
        return {
            cat: len(ids) for cat, ids in getattr(self, "_per_category_total_track_ids", {}).items()
        }

    def get_new_counts_this_frame(self) -> Dict[str, int]:
        """Get count of NEW track IDs that appeared in this frame vs the previous one."""
        return {
            cat: len(ids) for cat, ids in getattr(self, "_new_track_ids_this_frame", {}).items()
        }

    def get_current_frame_counts(self) -> Dict[str, int]:
        """Get count of ALL track IDs currently in this frame (existing + new)."""
        return {cat: len(ids) for cat, ids in getattr(self, "_current_frame_track_ids", {}).items()}

    def _get_track_ids_info(self, detections: List[Dict]) -> Dict[str, Any]:
        """Get detailed information about track IDs."""
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

    def _generate_summary(self, analytics_results: Dict, alerts: List) -> str:
        """Generate human-readable summary."""
        # Beautiful, tabbed, non-technical summary for all major analytics sections
        queue_analytics = analytics_results.get("customer_queue_analytics", {})
        staff_analytics = analytics_results.get("staff_management_analytics", {})
        counter_analytics = analytics_results.get("counter_analytics", {})
        journey_analytics = analytics_results.get("customer_journey_analytics", {})
        business_metrics = analytics_results.get("business_metrics", {})

        def tabbed_section(title, dct, omit_keys=None):
            if not dct:
                return f"{title}: None"
            omit_keys = omit_keys or set()
            lines = [f"{title}:"]
            for k, v in dct.items():
                if k in omit_keys:
                    continue
                if isinstance(v, dict):
                    lines.append(f"\t{k}:")
                    for sk, sv in v.items():
                        lines.append(f"\t\t{sk}: {sv}")
                elif isinstance(v, list):
                    lines.append(f"\t{k}: [{len(v)} items]")
                else:
                    lines.append(f"\t{k}: {v}")
            return "\n".join(lines)

        summary = []
        summary.append("Application Name: " + self.CASE_TYPE)
        summary.append("Application Version: " + self.CASE_VERSION)
        summary.append(
            tabbed_section(
                "customer_queue_analytics",
                queue_analytics,
                omit_keys={"wait_times_completed", "wait_times_ongoing"},
            )
        )
        summary.append(tabbed_section("staff_management_analytics", staff_analytics))
        # "counters" is nested per-counter detail; the roll-up scalars beside it
        # already carry the headline numbers, so rendering both is just noise.
        summary.append(
            tabbed_section("counter_analytics", counter_analytics, omit_keys={"counters"})
        )
        summary.append(tabbed_section("customer_journey_analytics", journey_analytics))
        summary.append(tabbed_section("business_metrics", business_metrics))

        if alerts:
            critical_alerts = sum(1 for alert in alerts if alert.get("severity") == "critical")
            if critical_alerts > 0:
                summary.append(f"ALERTS: {critical_alerts} critical alert(s)")
            else:
                summary.append(f"ALERTS: {len(alerts)} alert(s)")

        return "\n".join(summary)

    def get_config_schema(self) -> Dict[str, Any]:
        """Get configuration schema for advanced customer service."""
        return {
            "type": "object",
            "properties": {
                "confidence_threshold": {
                    "type": "number",
                    "minimum": 0.0,
                    "maximum": 1.0,
                    "default": 0.5,
                    "description": "Minimum confidence threshold for detections",
                },
                "customer_areas": {
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
                    "description": "Customer area definitions as polygons",
                },
                "staff_areas": {
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
                    "description": "Staff area definitions as polygons",
                },
                "service_areas": {
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
                    "description": "Service area definitions as polygons",
                },
                # Eight keys were removed from this schema in Phase 7, all of them
                # advertised knobs this use case no longer reads: staff_categories /
                # customer_categories (role now comes from which counter zone a track
                # is in, never from the model class name -- R1),
                # service_proximity_threshold / max_service_time / buffer_time (the
                # proximity service model was deleted in Phase 4),
                # enable_journey_analysis / enable_queue_analytics (never read at all),
                # and tracking_config (the tracker is built by ConfigDrivenTracker from
                # TrackerProfile.LEGACY_40). An advertised knob that changes nothing is
                # worse than an absent one: someone tunes it and trusts the result. The
                # CustomerServiceConfig fields stay -- that class is shared with the
                # customer_service use case, and removing fields there is not additive.
                "enable_tracking": {
                    "type": "boolean",
                    "default": True,
                    "description": "Enable advanced tracking for analytics",
                },
                "enable_smoothing": {
                    "type": "boolean",
                    # False, not True. This key was advertised for a long time
                    # without a matching CustomerServiceConfig field, so
                    # filter_config_kwargs dropped whatever was configured and
                    # getattr(config, "enable_smoothing", False) always won --
                    # smoothing has never actually run. The field exists now, so
                    # advertising True here would silently switch smoothing on for
                    # every existing deployment. Enabling it is a separate,
                    # deliberately measured change.
                    "default": False,
                    "description": "Enable bounding box smoothing for detections",
                },
                "smoothing_algorithm": {
                    "type": "string",
                    "enum": ["observability", "kalman"],
                    "default": "observability",
                },
                "smoothing_window_size": {
                    "type": "integer",
                    "minimum": 1,
                    "default": 20,
                },
                "smoothing_cooldown_frames": {
                    "type": "integer",
                    "minimum": 0,
                    "default": 5,
                },
                # smoothing_confidence_threshold removed: it never had a backing
                # field, and the smoothing config reads plain confidence_threshold.
                # Advertising it meant a configured value was silently dropped --
                # ACS-01's exact failure mode, left behind as the last instance of it.
                "smoothing_confidence_range_factor": {
                    "type": "number",
                    "minimum": 0.0,
                    "default": 0.5,
                },
                "reset_interval_type": {
                    "type": "string",
                    "default": "daily",
                    "description": "Interval type for resetting analytics (e.g., daily, weekly)",
                },
                "reset_time_value": {
                    "type": "integer",
                    "default": 9,
                    "description": "Time value for reset (e.g., hour of day)",
                },
                "reset_time_unit": {
                    "type": "string",
                    "default": "hour",
                    "description": "Time unit for reset (e.g., hour, minute)",
                },
                "alert_config": {
                    "type": "object",
                    "description": "Custom alert configuration settings",
                },
                "queue_length_threshold": {
                    "type": "integer",
                    "default": 10,
                    "description": "Threshold for queue length alerts",
                },
                # service_efficiency_threshold / staff_utilization_threshold were added
                # to this schema in Phase 1 (ACS-01) and their alerts deleted in Phase 5
                # -- service_efficiency fired off an all-time ratio that decayed toward
                # zero and so latched on permanently. Un-advertised here rather than
                # left as tunables with no effect.
                "email_address": {
                    "type": "string",
                    "default": "",
                    "description": "Email address for alert notifications",
                },
                "zone_config": {
                    "type": "object",
                    "description": (
                        "Counter zone geometry. 'zones' maps zone name -> polygon and must "
                        "contain paired staff_<i> / customer_<i> entries (staff_1 + customer_1, "
                        "staff_2 + customer_2, ...). Resolved from the post-processing API in "
                        "pixel space."
                    ),
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
                        },
                        "zone_params": {"type": "object"},
                    },
                },
                "min_inside_frames": {
                    "type": "integer",
                    "minimum": 1,
                    "default": 2,
                    "description": "Consecutive frames inside a zone before membership is confirmed",
                },
                "exit_grace_frames": {
                    "type": "integer",
                    "minimum": 1,
                    "default": 3,
                    "description": "Consecutive frames outside a zone before membership is dropped",
                },
                "presence_grace_frames": {
                    "type": "integer",
                    "minimum": 0,
                    "default": 15,
                    "description": (
                        "Frames a confirmed track may be absent from frame before its zone-entry "
                        "timestamp is discarded (occlusion tolerance for the serving rule)"
                    ),
                },
                "track_merge_iou_threshold": {
                    "type": "number",
                    "minimum": 0.0,
                    "maximum": 1.0,
                    "default": 0.15,
                    "description": "IoU above which a re-issued tracker ID is folded onto a canonical ID",
                },
                "track_merge_time_window_seconds": {
                    "type": "number",
                    "minimum": 0.0,
                    "default": 8.0,
                    "description": "How long a canonical track stays eligible for ID merging",
                },
            },
            "required": ["confidence_threshold"],
            "additionalProperties": False,
        }

    def create_default_config(self, **overrides) -> CustomerServiceConfig:
        """Create default configuration with optional overrides."""
        defaults = {
            "category": self.category,
            "usecase": self.name,
            "confidence_threshold": 0.5,
            "enable_tracking": True,
            "enable_analytics": True,
            # The six category/proximity/service-time keys that used to be set here
            # are gone with the schema entries above: nothing reads them, and passing
            # them made the default config look like it configured behaviour it did
            # not. The dataclass defaults still cover them for the shared config class.
            # NOTE: no "stream_info" key here. CustomerServiceConfig has no such
            # field, so passing it made this method raise TypeError on every call.
            # Stream metadata reaches the use case through process(stream_info=...).
        }
        defaults.update(overrides)
        return CustomerServiceConfig(**defaults)

    def _extract_predictions(self, data: Any) -> Dict[str, List[Dict[str, Any]]]:
        """Extract predictions from processed data for API compatibility, grouped by frame number if available."""
        predictions = {}
        try:
            if isinstance(data, dict):
                # Frame-based or tracking format
                for frame_id, items in data.items():
                    if not isinstance(items, list):
                        continue
                    frame_preds = []
                    for item in items:
                        if isinstance(item, dict):
                            pred = {
                                "category": item.get("category", item.get("class", "unknown")),
                                "confidence": item.get("confidence", item.get("score", 0.0)),
                                "bounding_box": item.get("bounding_box", item.get("bbox", {})),
                                "track_id": item.get("track_id"),
                            }
                            frame_preds.append(pred)
                    if frame_preds:
                        predictions[str(frame_id)] = frame_preds
            elif isinstance(data, list):
                # If not frame-based, put all predictions under a generic key
                predictions["0"] = []
                for item in data:
                    if isinstance(item, dict):
                        pred = {
                            "category": item.get("category", item.get("class", "unknown")),
                            "confidence": item.get("confidence", item.get("score", 0.0)),
                            "bounding_box": item.get("bounding_box", item.get("bbox", {})),
                            "track_id": item.get("track_id"),
                        }
                        predictions["0"].append(pred)
        except (AttributeError, TypeError, ValueError, KeyError) as e:
            self.logger.warning(f"Failed to extract predictions: {str(e)}")
        return predictions
