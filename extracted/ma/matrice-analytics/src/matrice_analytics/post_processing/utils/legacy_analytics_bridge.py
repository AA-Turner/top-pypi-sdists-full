"""
Legacy use-case bridge → Redis ``incident_res`` + ``results-agg``.

Publishes through :class:`~matrice_analytics.analytics.redis_publisher.AnalyticsRedisPublisher`
using the same envelope shape as the NEW analytics flow, while detection logic
stays in ``post_processing/usecases/*.py``.

Used when ``PostProcessor`` runs the legacy use-case path (no YAML manifest match).
"""

from __future__ import annotations

import logging
import os
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Mapping, Optional, Tuple

from .location_name_cache import LocationNameCache

logger = logging.getLogger(__name__)

AGGREGATION_INTERVAL_SEC = 60.0

# Standalone location-name resolution for results-agg / incident_res-via-bridge.
#
# ``resolve_location_for_publish`` (analytics/engine_session.py) never makes an
# API call — it only accepts a name already sitting in ``stream_info``, else
# falls back to the "Unknown Location" placeholder. The only place that used
# to resolve a location_id -> real name for this bridge was
# ``PostProcessor._enrich_stream_info_camera_metadata``, gated behind an
# unrelated CameraManagement camera_id/camera-metadata lookup — so a missing
# config client or a failed camera lookup silently skipped location too, even
# when ``camera_info.location`` was supplied. Mirrors the independent
# resolution already used by ``incident_manager_utils.py`` (locationId works
# there because it never depended on that gate). Kept self-contained here
# so it cannot affect any other usecase's ``stream_info`` or the new flow.
_location_name_cache = LocationNameCache()
_location_client: Any = None
_location_client_init_attempted = False


def _get_location_client() -> Any:
    global _location_client, _location_client_init_attempted
    if _location_client is not None:
        return _location_client
    if _location_client_init_attempted:
        return None
    _location_client_init_attempted = True
    try:
        from .post_processing_config_client import PostProcessingConfigClient

        client = PostProcessingConfigClient(logger=logger)
        if getattr(client, "_session", None) is None:
            logger.debug(
                "[LEGACY_ANALYTICS] no Matrice session for location lookup "
                "(set MATRICE_ACCESS_KEY_ID / MATRICE_SECRET_ACCESS_KEY)"
            )
            return None
        _location_client = client
        return client
    except Exception:
        logger.warning("[LEGACY_ANALYTICS] could not create location-lookup client", exc_info=True)
        return None


def _fetch_location_name_cached(location_id: str) -> str:
    if not location_id:
        return ""
    cached = _location_name_cache.resolved(location_id)
    if cached is not None:
        return cached
    client = _get_location_client()
    if client is None or not hasattr(client, "fetch_location_name"):
        return ""
    # An empty answer is a FAILURE here, not a resolved name: the client already
    # returns "" for both "no such location" and "the lookup blew up". Storing it as
    # a name pinned "" onto every row for this location for the life of the process
    # (INC-2606); a cool-off keeps the retry cheap without making it permanent.
    if not _location_name_cache.should_fetch(location_id):
        return ""
    name = client.fetch_location_name(location_id) or ""
    if name:
        _location_name_cache.store(location_id, name)
    else:
        _location_name_cache.note_failure(location_id)
    if name:
        logger.info("[LEGACY_ANALYTICS] resolved location=%r for location_id=%s", name, location_id)
    return name


ANALYTICS_ZONE_GLOBAL = "global"

# Env-gated fallback to the OLD caller-wired ``AnalyticsPublisher``.
# When set truthy, the SDK stays OUT of the self-contained publishing path for
# legacy apps: ``legacy_redis_analytics_usecases()`` returns an empty set so
# ``PostProcessor._publish_legacy_frame_analytics`` never fires, and the caller's
# ``AnalyticsPublisher`` remains the sole authority (no double-publish).
LEGACY_PUBLISHER_ENV = "MATRICE_ANALYTICS_LEGACY_PUBLISHER"


def _env_truthy(name: str) -> bool:
    return str(os.environ.get(name, "")).strip().lower() in ("1", "true", "yes", "on")


@dataclass(frozen=True)
class VolumeMetricSpec:
    key: str
    agg_type: str  # sum | last | max | min | avg | mean
    category: str = "VOLUME"


@dataclass(frozen=True)
class LegacyAnalyticsProfile:
    """Per-usecase Redis analytics wiring (incidents + VOLUME results-agg)."""

    application_key_name: str
    default_application_name: str
    volume_metrics: Tuple[VolumeMetricSpec, ...] = ()
    default_tracking_categories: Tuple[str, ...] = ("person",)
    primary_category: str = "person"
    publish_incidents: bool = False
    # weapon/fire: max(weapon+person) over window; people_counting: last-frame occupancy
    occupancy_mode: str = "last_primary"  # last_primary | max_weapon_person
    # window_delta: accumulate current_new over the publish window (footfall / people counting).
    # latest_snapshot: publish the last ingested frame's count lists (weapon / face-style apps).
    rollup_mode: str = "window_delta"


# Pipe inspection family → the tracking_stats side-channel block each use case
# writes every frame. Membership in this map is what routes a profile through
# _ingest_pipe_defect_analytics / the "pipe defect" resolver branch, so adding a
# fourth single-class pipe app is a one-line change here plus a profile above.
_PIPE_DEFECT_BLOCKS: Dict[str, str] = {
    "pipe_corrosion_detection": "corrosion_analytics",
    "pipe_gas_leak_detection": "gas_analytics",
    "liquid_leak_detection": "liquid_analytics",
}

# Per-app metric-key → shared pipe accumulator. The three apps publish
# domain-named keys (new_corrosion_count / new_gas_leak_count / ...) that all
# resolve from the same window state, so the resolver maps key → semantic role
# instead of repeating three near-identical branches.
_PIPE_METRIC_ROLES: Dict[str, str] = {
    # corrosion (QUALITY)
    "new_corrosion_count": "new",
    "total_corrosion_count": "total",
    "peak_corrosion_count": "peak",
    "corrosion_presence": "presence",
    # gas leak (SAFETY)
    "current_gas_leak_count": "current",
    "new_gas_leak_count": "new",
    "total_gas_leak_count": "total",
    "gas_presence": "presence",
    "gas_duration_seconds": "duration",
    "max_continuous_gas_seconds": "max_continuous",
    # liquid leak (SAFETY)
    "current_liquid_leak_count": "current",
    "new_liquid_leak_count": "new",
    "total_liquid_leak_count": "total",
    "liquid_presence": "presence",
    "liquid_duration_seconds": "duration",
    "max_continuous_liquid_seconds": "max_continuous",
}

# Industrial inspection family. All four write the SAME superset side-channel
# block, tracking_stats["quality_analytics"] — a two-tier defect/inspected split
# (frame_defect_ids / frame_inspected_ids, car-damage parity) PLUS the pipe
# family's presence fields (frame_new_ids / is_active / total_unique_count /
# max_continuous_seconds). Membership here routes a profile through
# _ingest_inspection_quality and the inspection resolver branch, so adding a
# fifth inspection app is a one-line change plus a profile.
#
# Deliberately NOT merged with the car_damage_detection branch even though the
# block name is shared: car damage predates the superset contract (no
# frame_new_ids / is_active, so no total_defect_count or defect_presence) and
# publishes defect_rate as a 0-1 RATIO, whereas these four declare
# `unit: percent` and publish 0-100. Folding them together would silently change
# car damage's published defect_rate by 100x.
_INSPECTION_QUALITY_APPS: frozenset = frozenset(
    {
        "bottle_defect_detection",
        "pcb_defect_detection",
        "phone_screen_defect_detection",
        "solar_panel",
    }
)

# parking_lot_analytics: newly-parked vehicle category -> published metric
# bucket. bicycle/motorcycle collapse into the single two_wheeler_count
# metric (parking_lot_analytics-v1.2's custom.newly_parked_two_wheeler);
# every four-wheeler class publishes under its own name.
_PARKING_CLASS_TO_BUCKET: Dict[str, str] = {
    "bicycle": "two_wheeler",
    "motorcycle": "two_wheeler",
    "car": "car",
    "van": "van",
    "bus": "bus",
    "truck": "truck",
}


_LEGACY_PROFILES: Dict[str, LegacyAnalyticsProfile] = {
    "weapon_detection": LegacyAnalyticsProfile(
        application_key_name="weapon_detection",
        default_application_name="Weapon Detection",
        # VOLUME: new knife/gun track IDs summed over the ~60s publish window
        # (agg_type "sum"), split per weapon type -- matches analytics config
        # knives_detected / guns_detected. Model emits knife/gun directly
        # (no more generic "weapon" class, no person class).
        volume_metrics=(
            VolumeMetricSpec("knives_detected", "sum"),
            VolumeMetricSpec("guns_detected", "sum"),
        ),
        default_tracking_categories=("knife", "gun"),
        primary_category="knife",
        publish_incidents=True,
        occupancy_mode="last_primary",
        # window_delta (not latest_snapshot): current_counts = new knife/gun track
        # IDs that first appeared during this window; total_current_counts = the
        # occupancy carried in from before the window started + those new arrivals.
        # This guarantees total_current_counts >= current_counts, which a plain
        # last-frame-vs-window-max comparison (latest_snapshot) could not: a weapon
        # already in frame before the window began has no "new" track ID, so it
        # only shows up in total_current_counts, never in current_counts.
        rollup_mode="window_delta",
    ),
    "violence_detection": LegacyAnalyticsProfile(
        application_key_name="violence_detection",
        default_application_name="Violence Detection",
        volume_metrics=(VolumeMetricSpec("current_occupancy", "last"),),
        default_tracking_categories=("violence",),
        primary_category="violence",
        publish_incidents=True,
        occupancy_mode="last_primary",
        rollup_mode="latest_snapshot",
    ),
    "fire_smoke_detection": LegacyAnalyticsProfile(
        application_key_name="fire_smoke_detection",
        default_application_name="Fire Detection",
        volume_metrics=(VolumeMetricSpec("current_occupancy", "last"),),
        default_tracking_categories=("fire", "smoke"),
        primary_category="fire",
        publish_incidents=True,
        occupancy_mode="last_primary",
    ),
    # X3D accident classifier. Like fire/smoke it has no IncidentManager wiring,
    # so incident_res publish relies on this legacy-bridge fallback: without an
    # explicit profile it fell to _make_default_profile (publish_incidents=False)
    # and every confirmed accident episode was dropped at maybe_publish_incident.
    # accident_detection emits a "critical" incident on episode-open, so
    # publish_incidents=True forwards it to incident_res.
    "accident_detection": LegacyAnalyticsProfile(
        application_key_name="accident_detection",
        default_application_name="Accident Detection",
        # accidents_over_time: unique confirmed-accident episodes this 60s window
        # (agg_type "sum") — resolved generically from current_new_counts, the
        # same window_new_sum pipeline footfall's entry/people_counting's
        # occupancy_in_interval use (no custom ingest needed: accident_detection.py
        # already fires current_new_counts["accident"]=1 exactly once per episode).
        # critical_accidents: of those, how many carried severity_level=="critical"
        # (agg_type "sum") — custom, resolved from the incidents block, since
        # severity isn't part of tracking_stats. Every accident here is currently
        # always "critical" (see accident_detection.py's _generate_incidents), so
        # today critical_accidents == accidents_over_time, but this reads the
        # actual severity rather than assuming it, so it stays correct if a
        # lower-severity tier is ever added.
        volume_metrics=(
            VolumeMetricSpec("accidents_over_time", "sum"),
            VolumeMetricSpec("critical_accidents", "sum"),
        ),
        default_tracking_categories=("accident",),
        primary_category="accident",
        publish_incidents=True,
        occupancy_mode="last_primary",
    ),
    "drone_detection": LegacyAnalyticsProfile(
        application_key_name="drone_detection",
        default_application_name="Drone Detection",
        volume_metrics=(VolumeMetricSpec("current_occupancy", "last"),),
        default_tracking_categories=("drone",),
        primary_category="drone",
        publish_incidents=True,
        occupancy_mode="last_primary",
    ),
    # Without an explicit profile this fell to _make_default_profile
    # (publish_incidents=False, generic "current_occupancy" with no primary
    # category match), so nothing meaningful reached Volume/Incident Analytics
    # regardless of deployment health. current_occupancy here resolves generically
    # off tracking_stats.current_counts["abandoned_object"] (primary_category
    # match), the same category the use case already assigns once an object is
    # confirmed abandoned. publish_incidents=True is the fallback only — the
    # bridge skips it when incident_published_via_manager is set (IncidentManager
    # already handled it), same as loitering_detection.
    # Named metrics (abandoned_count/total_abandoned_count/new_abandoned_count/
    # tracked_object_count) resolved in _resolve_metric_value, mirroring
    # flare_analysis and pothole_detection so the dashboard keys correspond to
    # something the backend actually emits instead of only the generic
    # current_occupancy.
    #
    # rollup_mode is "latest_snapshot", NOT the default "window_delta".
    # Abandonment is a persistent *state*, not an arrival event: a bag left in
    # frame for an hour fires current_new_counts exactly once, so under
    # window_delta (current_counts = window_new_sum) every window after the
    # first published abandoned_object=0 while the bag was still sitting there
    # -- the VOLUME chart reading tracking_stats.current_counts flatlined at 0.
    # latest_snapshot publishes the last frame's in-frame count instead, which
    # stays 1 for as long as the object remains abandoned. Same reasoning as
    # flare_analysis (GoodFlare/BadFlare are states too).
    "abandoned_object_detection": LegacyAnalyticsProfile(
        application_key_name="abandoned_object_detection",
        default_application_name="Abandoned Object Detection",
        volume_metrics=(
            VolumeMetricSpec("current_occupancy", "last"),
            VolumeMetricSpec("abandoned_count", "last"),
            VolumeMetricSpec("total_abandoned_count", "last"),
            VolumeMetricSpec("new_abandoned_count", "sum"),
            VolumeMetricSpec("tracked_object_count", "last"),
        ),
        default_tracking_categories=("abandoned_object",),
        primary_category="abandoned_object",
        publish_incidents=True,
        occupancy_mode="last_primary",
        rollup_mode="latest_snapshot",
    ),
    # Like fire/accident/drone/abandoned_object, flare_analysis has no
    # IncidentManagerFactory wiring of its own -- it builds its own
    # incidents_list via _generate_incidents(), so without an explicit profile
    # this fell to _make_default_profile (publish_incidents=False) and every
    # confirmed bad-flare episode was dropped at maybe_publish_incident.
    # "BadFlare" (not "GoodFlare") is the primary/tracking category since that's
    # the hazard state this usecase exists to alert on.
    "flare_analysis": LegacyAnalyticsProfile(
        application_key_name="flare_analysis",
        default_application_name="Flare Detection",
        # Named per-category metrics (goodflare_count/badflare_count/
        # bad_flare_rate), resolved in _resolve_metric_value -- mirrors
        # mask_detection's mask_count/no_mask_count/mask_violation_rate
        # pattern exactly, so the marketplace metrics.json/widgets.json keys
        # correspond to something the backend actually emits.
        # goodflare_count/badflare_count are per-minute NEW-flare throughput
        # (window_new_sum of current_new_counts across the 60s window), so they
        # carry agg_type "sum" -- matching the marketplace metrics.json. current_occupancy
        # and bad_flare_rate are last-frame / latest snapshots (agg_type "last").
        volume_metrics=(
            VolumeMetricSpec("current_occupancy", "last"),
            VolumeMetricSpec("goodflare_count", "sum"),
            VolumeMetricSpec("badflare_count", "sum"),
            VolumeMetricSpec("bad_flare_rate", "last"),
        ),
        default_tracking_categories=("BadFlare", "GoodFlare"),
        primary_category="BadFlare",
        publish_incidents=True,
        occupancy_mode="last_primary",
        rollup_mode="latest_snapshot",
    ),
    # Same gap as flare_analysis above: pothole_detection generates its own
    # incidents_list with no IncidentManager wiring, so it fell to the generic
    # default profile with publish_incidents=False.
    "pothole_detection": LegacyAnalyticsProfile(
        application_key_name="pothole_detection",
        default_application_name="Pothole Detection",
        # Named metrics (pothole_count/total_pothole_count) resolved in
        # _resolve_metric_value, mirroring mask_detection/flare_analysis's
        # pattern so marketplace metrics.json/widgets.json keys correspond to
        # something the backend actually emits. pothole_severity (largest
        # pothole as % of frame area) is NOT wired here -- it needs bbox-area
        # data this count-based session state doesn't carry; left as a known
        # gap rather than faked.
        volume_metrics=(
            VolumeMetricSpec("current_occupancy", "last"),
            VolumeMetricSpec("pothole_count", "sum"),
            VolumeMetricSpec("total_pothole_count", "last"),
        ),
        default_tracking_categories=("pothole",),
        primary_category="pothole",
        publish_incidents=True,
        occupancy_mode="last_primary",
    ),
    "people_counting": LegacyAnalyticsProfile(
        application_key_name="people_counting",
        default_application_name="People Counting",
        # VOLUME metrics resolved in _resolve_metric_value (app == "people_counting"):
        #   occupancy_in_interval  – sum of current_new_counts["person"]
        #                            across the 60s window (agg_type "sum").
        #   total_occupancy        – latest cumulative total_counts["person"]
        #                            (agg_type "last").
        #   occupancy_percentage   – last-frame occupancy vs capacity (50).
        volume_metrics=(
            VolumeMetricSpec("occupancy_in_interval", "sum"),
            VolumeMetricSpec("total_occupancy", "last"),
            VolumeMetricSpec("occupancy_percentage", "last"),
        ),
        default_tracking_categories=("person",),
        primary_category="person",
        publish_incidents=False,
        occupancy_mode="last_primary",
    ),
    "footfall": LegacyAnalyticsProfile(
        application_key_name="footfall",
        default_application_name="Foot Fall",
        volume_metrics=(
            VolumeMetricSpec("entry", "sum"),
            VolumeMetricSpec("exit", "sum"),
            # Peak concurrent occupancy of the two-line corridor (in+out
            # combined), not a throughput sum -- agg_type "max" so a 5-min/
            # hourly rollup takes the worst pile-up, matching
            # footfall-v1.5's entrance_congestion (4th definition).
            VolumeMetricSpec("entrance_congestion", "max"),
        ),
        default_tracking_categories=("in", "out"),
        primary_category="in",
        publish_incidents=False,
        occupancy_mode="last_primary",
    ),
    "vehicle_monitoring": LegacyAnalyticsProfile(
        application_key_name="vehicle_monitoring",
        default_application_name="Vehicle Monitoring — Highway",
        # Whole-frame vehicle composition. In-frame counts report per-minute
        # THROUGHPUT — the count of new unique vehicles that entered the frame
        # across the 60s window (agg_type "sum"), sourced from current_new_counts
        # so the value reflects traffic flow (how many vehicles passed this
        # minute), not the peak concurrent count in a single frame. Custom
        # per-class keys are resolved in _resolve_metric_value (no
        # current_occupancy here).
        #   <class>_count       → new unique vehicles of that class this window (sum).
        #   total_<class>_count → cumulative unique tracks of that class
        #                         (from the use case's total_counts; agg_type last).
        #   two_wheel_vehicle_count → new (motorcycle + bicycle) this window (sum).
        #   heavy_vehicle_count     → new (bus + truck) this window (sum).
        volume_metrics=(
            VolumeMetricSpec("vehicle_count", "sum"),
            VolumeMetricSpec("car_count", "sum"),
            VolumeMetricSpec("truck_count", "sum"),
            VolumeMetricSpec("bus_count", "sum"),
            VolumeMetricSpec("van_count", "sum"),
            VolumeMetricSpec("motorcycle_count", "sum"),
            VolumeMetricSpec("total_car_count", "last"),
            VolumeMetricSpec("total_truck_count", "last"),
            VolumeMetricSpec("total_bus_count", "last"),
            VolumeMetricSpec("total_van_count", "last"),
            VolumeMetricSpec("total_motorcycle_count", "last"),
            VolumeMetricSpec("two_wheel_vehicle_count", "sum"),
            VolumeMetricSpec("heavy_vehicle_count", "sum"),
        ),
        default_tracking_categories=("car", "truck", "bus", "van", "motorcycle", "bicycle"),
        primary_category="car",
        publish_incidents=False,
        occupancy_mode="last_primary",
    ),
    "stopped_vehicle_monitoring": LegacyAnalyticsProfile(
        application_key_name="stopped_vehicle_monitoring",
        default_application_name="Stopped Vehicle Monitoring",
        # VOLUME metrics resolved in _resolve_metric_value from the use case's
        # side-channel state (not standard current_counts categories):
        #   stopped_vehicle_count      – confirmed stopped vehicles in the last
        #                                frame (snapshot, agg_type "last").
        #   peak_stopped_vehicle_count – max confirmed stopped count across the
        #                                60s window (agg_type "last" of the peak).
        #   total_stopped_events       – cumulative session stop-event total
        #                                (monotonic, agg_type "last").
        volume_metrics=(
            VolumeMetricSpec("stopped_vehicle_count", "last"),
            VolumeMetricSpec("peak_stopped_vehicle_count", "last"),
            VolumeMetricSpec("total_stopped_events", "last"),
        ),
        default_tracking_categories=("car", "truck", "bus", "van", "motorcycle", "bicycle"),
        primary_category="car",
        # Stopped vehicles are genuine roadway incidents (breakdown/illegal
        # stop), and the use case emits a severity-graded incident, so forward
        # it to incident_res. Flip to False if only the VOLUME graph is wanted.
        publish_incidents=True,
        occupancy_mode="last_primary",
        rollup_mode="latest_snapshot",
    ),
    "loitering_detection": LegacyAnalyticsProfile(
        application_key_name="loitering_detection",
        default_application_name="Loitering Detection",
        # VOLUME: latest loiterer count + windowed mean loitering share, plus
        # per-minute NEW unique loiterers and NEW people this window (cumulative
        # total delta over the 60s window, agg_type "sum" — traffic-flow style,
        # not a session cumulative or last-frame snapshot). avg/max_loiter_time_seconds
        # are the latest snapshot of tracking_stats["loitering_analytics"], same
        # shape as intrusion_detection's avg/max_intrusion_time_seconds. All custom
        # keys resolved in _resolve_metric_value. INCIDENT is published by the use
        # case's IncidentManager (publish_incidents=True is the fallback only —
        # the bridge skips it when incident_published_via_manager is set).
        volume_metrics=(
            VolumeMetricSpec("loitering_count", "last"),
            VolumeMetricSpec("loitering_percentage", "mean"),
            VolumeMetricSpec("loitering_unique_count", "sum"),
            VolumeMetricSpec("loitering_count_total", "last"),
            VolumeMetricSpec("people_in_frame", "sum"),
            VolumeMetricSpec("avg_loiter_time_seconds", "last"),
            VolumeMetricSpec("max_loiter_time_seconds", "last"),
        ),
        default_tracking_categories=("person", "loitering_person"),
        primary_category="person",
        publish_incidents=True,
        occupancy_mode="last_primary",
    ),
    # mask_count / no_mask_count: cumulative totals from tracking_stats.total_counts
    # (agg_type "last" — last frame's totals in the 60s window).
    # mask_violation_rate: NO-Mask / (Mask + NO-Mask) * 100 from those totals.
    # All keys prefixed with "mask_" to avoid collision with other usecases.
    #
    # Same gap pothole_detection and flare_analysis both had: mask_detection.py
    # builds its own incidents_list via create_incident()/_generate_incidents()
    # with no IncidentManagerFactory wiring of its own, so publish_incidents=False
    # here means every confirmed mask-violation incident is built correctly and
    # then silently dropped at maybe_publish_incident -- volume metrics still
    # flow (they're a separate path), but nothing ever reaches incident_res.
    # publish_incidents=True is the bridge's own publish path, not a fallback
    # behind an IncidentManager here (there is none) -- mirrors pothole_detection.
    "mask_detection": LegacyAnalyticsProfile(
        application_key_name="mask_detection",
        default_application_name="Mask Detection",
        volume_metrics=(
            VolumeMetricSpec("mask_count", "last"),
            VolumeMetricSpec("no_mask_count", "last"),
            VolumeMetricSpec("mask_violation_rate", "last"),
        ),
        default_tracking_categories=("mask", "no-mask"),
        primary_category="no-mask",
        publish_incidents=True,
        occupancy_mode="last_primary",
        rollup_mode="latest_snapshot",
    ),
    "gender_detection": LegacyAnalyticsProfile(
        application_key_name="gender_detection",
        default_application_name="Gender Detection",
        # VOLUME: last-frame in-frame counts per gender, read from
        # tracking_stats.current_counts (agg_type "last" -- a snapshot, not a
        # cumulative/windowed sum). Category keys are lowercased by
        # _count_list_to_map ("Male" -> "male", "Female" -> "female").
        volume_metrics=(
            VolumeMetricSpec("male_count", "last"),
            VolumeMetricSpec("female_count", "last"),
        ),
        default_tracking_categories=("male", "female"),
        primary_category="male",
        # Demographic classifier (male/female snapshot) -- no incident semantics;
        # keep VOLUME results-agg but suppress incident_res publish.
        publish_incidents=False,
        occupancy_mode="last_primary",
        rollup_mode="latest_snapshot",
    ),
    "age_detection": LegacyAnalyticsProfile(
        application_key_name="age_detection",
        default_application_name="Age Detection",
        # VOLUME: last-frame in-frame counts per age bucket, read from
        # tracking_stats.current_counts (agg_type "last" -- a snapshot, not a
        # cumulative/windowed sum). Category keys are lowercased by
        # _count_list_to_map ("Child" -> "child", "Adult" -> "adult", "Senior"
        # -> "senior").
        volume_metrics=(
            VolumeMetricSpec("child_count", "last"),
            VolumeMetricSpec("adult_count", "last"),
            VolumeMetricSpec("senior_count", "last"),
        ),
        default_tracking_categories=("child", "adult", "senior"),
        primary_category="adult",
        # Demographic classifier (age-bucket snapshot) -- no incident semantics;
        # keep VOLUME results-agg but suppress incident_res publish.
        publish_incidents=False,
        occupancy_mode="last_primary",
        rollup_mode="latest_snapshot",
    ),
    "face_emotion": LegacyAnalyticsProfile(
        application_key_name="face_emotion",
        default_application_name="Face Emotion",
        # VOLUME: last-frame in-frame counts per emotion, read from
        # tracking_stats.current_counts (agg_type "last" -- a snapshot, not a
        # cumulative/windowed sum). These per-emotion counts drive the emotion
        # distribution graph.
        #
        # Casing: face_emotion.py emits title-case categories (EMOTION_LABELS /
        # target_categories: "Surprise".."Neutral"). The categories below are
        # kept LOWERCASE on purpose -- _count_list_to_map lowercases every
        # incoming current_counts category and _filter_count_map lowercases
        # these before matching, so populated frames always resolve lowercase
        # ("Happiness" -> "happiness"). Keeping the tuple lowercase means the
        # zero-fill rows _default_count_list emits on empty frames match that
        # casing too, instead of splitting into title-case-vs-lowercase series.
        volume_metrics=(
            VolumeMetricSpec("surprise_count", "last"),
            VolumeMetricSpec("fear_count", "last"),
            VolumeMetricSpec("disgust_count", "last"),
            VolumeMetricSpec("happiness_count", "last"),
            VolumeMetricSpec("sadness_count", "last"),
            VolumeMetricSpec("anger_count", "last"),
            VolumeMetricSpec("neutral_count", "last"),
        ),
        default_tracking_categories=(
            "surprise",
            "fear",
            "disgust",
            "happiness",
            "sadness",
            "anger",
            "neutral",
        ),
        primary_category="neutral",
        # Emotion classifier (per-emotion snapshot) -- no incident semantics;
        # keep VOLUME results-agg but suppress incident_res publish.
        publish_incidents=False,
        occupancy_mode="last_primary",
        rollup_mode="latest_snapshot",
    ),
    "parking_lot_analytics": LegacyAnalyticsProfile(
        application_key_name="parking_lot_analytics",
        default_application_name="Parking Lot Analytics",
        # Matches parking_lot_analytics-v1.2's `metrics:` block exactly (key,
        # agg_type, and semantics) — all ten keys are custom, resolved in
        # _resolve_metric_value from window_park_entry_sum / _exit_sum /
        # _max_parked_seconds / _newly_parked_sum / _newly_parked_by_category
        # (ingested from the use case's tracking_stats["parking_analytics"]
        # and ["line_counts"] blocks). "park_" prefix on entry/exit avoids
        # clashing with the entry_count/exit_count keys other apps publish.
        #   parked_vehicles_count            – NEWLY parked this window (sum),
        #                                       not a live snapshot.
        #   avg_parking_time_wrt_to_vehicle  – mean dwell over currently-open
        #                                       parked sessions (last).
        #   park_entry_counts / park_exit_counts – per-window corridor
        #                                       crossings (sum), not the
        #                                       cumulative running total.
        #   max_park_seconds                 – per-window peak over
        #                                       currently-open sessions (max).
        #   car/van/bus/truck/two_wheeler_count – per-class NEWLY parked this
        #                                       window (sum), deduped for the
        #                                       life of the process.
        volume_metrics=(
            VolumeMetricSpec("parked_vehicles_count", "sum"),
            VolumeMetricSpec("avg_parking_time_wrt_to_vehicle", "last"),
            VolumeMetricSpec("park_entry_counts", "sum"),
            VolumeMetricSpec("park_exit_counts", "sum"),
            VolumeMetricSpec("max_park_seconds", "max"),
            VolumeMetricSpec("car_count", "sum"),
            VolumeMetricSpec("van_count", "sum"),
            VolumeMetricSpec("bus_count", "sum"),
            VolumeMetricSpec("truck_count", "sum"),
            VolumeMetricSpec("two_wheeler_count", "sum"),
        ),
        default_tracking_categories=("bicycle", "motorcycle", "car", "van", "bus", "truck"),
        primary_category="car",
        publish_incidents=False,
        occupancy_mode="last_primary",
    ),
    "pedestrian_detection": LegacyAnalyticsProfile(
        application_key_name="pedestrian_detection",
        default_application_name="Pedestrian Detection",
        # VOLUME keys and agg_types match pedestrian_detection-v1.4's own
        # occupancy_in_interval/total_occupancy exactly (same shape as
        # people_counting's own pair, requested explicitly since both apps ask
        # the same question for a different entity). Both are custom, resolved
        # in _resolve_metric_value from window_new_sum / latest_totals.
        # default_tracking_categories/primary_category use the wire-visible
        # "Pedestrian" label (matches pedestrian_detection.py's
        # CATEGORY_DISPLAY relabel); _count_list_to_map/_filter_count_map are
        # already case-insensitive, so this still matches the lowercased
        # internal storage.
        volume_metrics=(
            VolumeMetricSpec("occupancy_in_interval", "sum"),
            VolumeMetricSpec("total_occupancy", "last"),
        ),
        default_tracking_categories=("Pedestrian",),
        primary_category="Pedestrian",
        publish_incidents=False,
        occupancy_mode="last_primary",
    ),
    "ppe_compliance": LegacyAnalyticsProfile(
        application_key_name="ppe_compliance",
        default_application_name="PPE Compliance",
        # SAFETY + VOLUME metrics aligned with ppe_compliance use case / SafetyProcessor semantics.
        volume_metrics=(
            VolumeMetricSpec("total_persons", "sum", "SAFETY"),
            VolumeMetricSpec("compliant_count", "sum", "SAFETY"),
            VolumeMetricSpec("violation_count", "sum", "SAFETY"),
            VolumeMetricSpec("compliance_pct", "mean", "SAFETY"),
            VolumeMetricSpec("hardhat_count", "sum", "SAFETY"),
            VolumeMetricSpec("safety_vest_count", "sum", "SAFETY"),
            VolumeMetricSpec("mask_count", "sum", "SAFETY"),
            VolumeMetricSpec("entry_count", "sum", "VOLUME"),
            VolumeMetricSpec("current_occupancy", "last", "VOLUME"),
        ),
        default_tracking_categories=(
            "person",
            "hardhat",
            "mask",
            "safety_vest",
            "no_hardhat",
            "no_mask",
            "no_safety_vest",
        ),
        primary_category="person",
        publish_incidents=False,
        occupancy_mode="last_primary",
    ),
    "dwell": LegacyAnalyticsProfile(
        application_key_name="dwell",
        default_application_name="Dwell Detection",
        # VOLUME: zone footfall + dwell-engagement, matching
        # dwell-analytics-metrics.json. All six keys are custom, resolved in
        # _resolve_metric_value from the use case's tracking_stats["dwell_analytics"]
        # block (same pattern as parking). visitors_in_zone / active_dwellers are
        # per-minute unique-track counts (agg_type "sum", reset every window);
        # unique_dwellers is the session-cumulative total (agg_type "last");
        # dwell_percentage is the windowed mean dweller share (agg_type "mean").
        # INCIDENT is published by the use case's IncidentManager
        # (publish_incidents=True is the fallback only — the bridge skips it when
        # incident_published_via_manager is set on the context).
        volume_metrics=(
            VolumeMetricSpec("active_dwellers", "sum"),
            VolumeMetricSpec("unique_dwellers", "last"),
            VolumeMetricSpec("visitors_in_zone", "sum"),
            VolumeMetricSpec("dwell_percentage", "mean"),
            VolumeMetricSpec("avg_dwell_time", "last"),
            VolumeMetricSpec("max_dwell_time", "last"),
        ),
        default_tracking_categories=("person", "Dweller"),
        primary_category="person",
        publish_incidents=True,
        occupancy_mode="last_primary",
        rollup_mode="latest_snapshot",
    ),
    "hazard_zone_entry": LegacyAnalyticsProfile(
        application_key_name="hazard_zone_entry",
        default_application_name="Hazard Zone Entry",
        # VOLUME: zone footfall + time-in-zone exposure. All keys are custom,
        # resolved in _resolve_metric_value from the use case's
        # tracking_stats["hazard_analytics"] block plus the person total_counts
        # delta. people_in_frame / people_at_risk are per-minute NEW counts (sum)
        # — the growth in cumulative people / zone entrants over the 60s window,
        # not a last-frame snapshot; active_people_at_risk is the instantaneous
        # in-zone count now (last) and unique_zone_entrants is the session
        # cumulative (last). INCIDENT is published by the use case's
        # IncidentManager (publish_incidents=True is the fallback only — the bridge
        # skips it when incident_published_via_manager is set on the context).
        volume_metrics=(
            VolumeMetricSpec("people_in_frame", "sum"),
            VolumeMetricSpec("people_at_risk", "sum"),
            VolumeMetricSpec("active_people_at_risk", "last"),
            VolumeMetricSpec("unique_zone_entrants", "last"),
            VolumeMetricSpec("hazard_entry_percentage", "mean"),
            VolumeMetricSpec("avg_time_in_zone_seconds", "last"),
            VolumeMetricSpec("max_time_in_zone_seconds", "last"),
        ),
        default_tracking_categories=("person", "at_risk"),
        primary_category="person",
        publish_incidents=True,
        occupancy_mode="last_primary",
        rollup_mode="latest_snapshot",
    ),
    "advanced_customer_service": LegacyAnalyticsProfile(
        application_key_name="advanced_customer_service",
        # The platform-facing label from APP_NAME_TO_USECASE (post_processing/
        # config.py), not _humanize()'s "Advanced Customer Service" -- this is what
        # the dashboard shows.
        default_application_name="Customer Activity Analysis",
        # VOLUME: counter throughput + queue health. All keys are custom, resolved
        # from tracking_stats["customer_service_analytics"]. Replaces the
        # synthesized default profile, which published only current_occupancy.
        # publish_incidents=True since ACS-04: the use case now runs a real
        # episode lifecycle (uuid held for the episode, end_time "" while active,
        # a single closing re-emission when the condition clears), so incidents
        # are safe to forward. It was False while the block still hardcoded
        # end_time and rebuilt incident_id every frame -- forwarding that would
        # have published one never-closing incident per frame.
        volume_metrics=(
            # presence
            # Two distinct headcounts, not synonyms: customers attached to a
            # counter, staff on station. The third one the side channel carries,
            # people_in_frame (everyone detected, zone or no zone), is
            # deliberately NOT published -- it is the raw detection count, which
            # for this app includes passers-by who never approach a counter, so
            # it reads as store footfall the counter model cannot back. The resolver
            # still answers the key so re-adding it is a one-line profile
            # change; the block still carries the field for the overlay panel.
            VolumeMetricSpec("customers_at_counters", "last"),
            VolumeMetricSpec("staff_on_counters", "last"),
            # counter occupancy / staffing
            VolumeMetricSpec("total_counters", "last"),
            VolumeMetricSpec("active_counters", "last"),
            VolumeMetricSpec("staffed_counters", "last"),
            VolumeMetricSpec("serving_counters", "last"),
            VolumeMetricSpec("counter_utilization", "mean"),
            VolumeMetricSpec("staff_coverage", "mean"),
            # queue
            VolumeMetricSpec("total_queue_length", "last"),
            VolumeMetricSpec("max_queue_length", "max"),
            VolumeMetricSpec("avg_queue_length", "mean"),
            # throughput (per-window deltas of monotonic cumulative counters)
            VolumeMetricSpec("customers_in_interval", "sum"),
            VolumeMetricSpec("unique_customers", "last"),
            VolumeMetricSpec("customers_served_in_interval", "sum"),
            VolumeMetricSpec("total_customers_served", "last"),
            VolumeMetricSpec("abandoned_in_interval", "sum"),
            VolumeMetricSpec("abandonment_rate", "mean"),
            # durations
            VolumeMetricSpec("avg_wait_seconds", "last"),
            VolumeMetricSpec("max_wait_seconds", "last"),
            VolumeMetricSpec("avg_service_seconds", "last"),
            VolumeMetricSpec("max_service_seconds", "last"),
            # efficiency
            VolumeMetricSpec("customer_to_staff_ratio", "mean"),
            VolumeMetricSpec("staff_productivity", "last"),
        ),
        default_tracking_categories=("customer", "staff"),
        primary_category="customer",
        publish_incidents=True,
        occupancy_mode="last_primary",
        rollup_mode="latest_snapshot",
    ),
    "intrusion_detection": LegacyAnalyticsProfile(
        application_key_name="intrusion_detection",
        default_application_name="Intrusion Detection",
        # VOLUME: secure-zone footfall + time-in-zone snapshot. All six keys are
        # custom, resolved from tracking_stats["intrusion_analytics"]. INCIDENT
        # via IncidentManager (publish_incidents=True is the bridge fallback).
        volume_metrics=(
            VolumeMetricSpec("people_in_frame", "last"),
            VolumeMetricSpec("active_intruders", "last"),
            VolumeMetricSpec("intruders_in_interval", "sum"),
            VolumeMetricSpec("unique_intruders", "last"),
            VolumeMetricSpec("intrusion_percentage", "mean"),
            VolumeMetricSpec("avg_intrusion_time_seconds", "last"),
            VolumeMetricSpec("max_intrusion_time_seconds", "last"),
        ),
        default_tracking_categories=("person", "intruder"),
        primary_category="person",
        publish_incidents=True,
        occupancy_mode="last_primary",
        rollup_mode="latest_snapshot",
    ),
    "tailgating_detection": LegacyAnalyticsProfile(
        application_key_name="tailgating_detection",
        default_application_name="Tailgating Detection",
        # VOLUME: access-control flow snapshot. tailgating_events is summed over
        # the window; the rest are latest / windowed-mean. All keys are custom,
        # resolved from tracking_stats["tailgating_analytics"]. INCIDENT via
        # IncidentManager (publish_incidents=True is the bridge fallback).
        volume_metrics=(
            VolumeMetricSpec("people_in_frame", "last"),
            VolumeMetricSpec("active_tailgaters", "last"),
            VolumeMetricSpec("interval_tailgaters", "sum"),
            VolumeMetricSpec("unique_tailgaters", "last"),
            VolumeMetricSpec("tailgating_percentage", "mean"),
        ),
        default_tracking_categories=("person", "tailgating_person"),
        primary_category="person",
        publish_incidents=True,
        occupancy_mode="last_primary",
        rollup_mode="latest_snapshot",
    ),
    "overcrowding_detection": LegacyAnalyticsProfile(
        application_key_name="overcrowding_detection",
        default_application_name="Overcrowding Detection",
        # VOLUME: occupancy + capacity utilisation. current/peak/avg occupancy
        # (last/max/mean) and mean occupancy_percentage are derived in
        # _resolve_metric_value from the per-frame current_occupancy /
        # occupancy_percentage in tracking_stats["overcrowding_analytics"].
        # INCIDENT via IncidentManager (publish_incidents=True is the fallback).
        volume_metrics=(
            VolumeMetricSpec("live_occupancy", "last"),
            VolumeMetricSpec("current_occupancy", "last"),
            VolumeMetricSpec("peak_occupancy", "max"),
            VolumeMetricSpec("avg_occupancy", "mean"),
            VolumeMetricSpec("occupancy_percentage", "mean"),
            VolumeMetricSpec("unique_visitors", "last"),
        ),
        default_tracking_categories=("person",),
        primary_category="person",
        publish_incidents=True,
        occupancy_mode="last_primary",
        rollup_mode="latest_snapshot",
    ),
    "area_utilization": LegacyAnalyticsProfile(
        application_key_name="area_utilization",
        default_application_name="Area Utilization",
        # VOLUME: same occupancy shape as its sibling overcrowding_detection
        # (zone_occupancy-style headcount), plus time_occupied_percent. No
        # side-channel block -- every key is resolved from generic per-frame
        # state in _resolve_metric_value (see the area_utilization branch).
        volume_metrics=(
            VolumeMetricSpec("live_occupancy", "last"),
            VolumeMetricSpec("current_occupancy", "sum"),
            VolumeMetricSpec("peak_occupancy", "max"),
            VolumeMetricSpec("avg_occupancy", "mean"),
            VolumeMetricSpec("occupancy_percentage", "last"),
            VolumeMetricSpec("time_occupied_percent", "mean"),
            VolumeMetricSpec("unique_visitors", "last"),
        ),
        default_tracking_categories=("person",),
        primary_category="person",
        publish_incidents=True,
        occupancy_mode="last_primary",
        rollup_mode="latest_snapshot",
    ),
    "flood_detection": LegacyAnalyticsProfile(
        application_key_name="flood_detection",
        default_application_name="Flood Detection",
        # VOLUME metrics match flood-analytics-metrics.json:
        #   avg_flood_area_percentage – windowed mean of
        #                               tracking_stats["flood_analytics"]["max_flood_area_pct"]
        #                               across every frame this 60s window,
        #                               including 0%-coverage frames
        #                               (agg_type "mean").
        #   floods_occurred           – sum of current_new_counts["flood"]
        #                               across the window (agg_type "sum").
        #                               flood_detection.py already runs a real
        #                               tracker (SORT/ByteTrack), so this is the
        #                               same generic window_new_sum pipeline
        #                               footfall's entry / accident's
        #                               accidents_over_time use — no custom
        #                               ingest needed.
        # Both keys are resolved in _resolve_metric_value.
        volume_metrics=(
            VolumeMetricSpec("avg_flood_area_percentage", "mean"),
            VolumeMetricSpec("floods_occurred", "sum"),
        ),
        default_tracking_categories=("flood",),
        primary_category="flood",
        publish_incidents=True,
        occupancy_mode="last_primary",
        rollup_mode="latest_snapshot",
    ),
    "landslide_detection": LegacyAnalyticsProfile(
        application_key_name="landslide_detection",
        default_application_name="Landslide Detection",
        # VOLUME metrics match landslide-analytics-metrics.json (same pattern
        # as flood_detection above):
        #   avg_surface_displacement_percentage – windowed mean of
        #       tracking_stats["landslide_analytics"]["max_landslide_area_pct"]
        #       (agg_type "mean").
        #   landslides_occurred – sum of current_new_counts["landslide"]
        #       across the window (agg_type "sum"); landslide_detection.py
        #       also runs a real tracker, so this reads window_new_sum
        #       directly, no custom ingest needed.
        volume_metrics=(
            VolumeMetricSpec("avg_surface_displacement_percentage", "mean"),
            VolumeMetricSpec("landslides_occurred", "sum"),
        ),
        # CATEGORY_DISPLAY maps "landslide" → "Landslide", lowercased to
        # "landslide" by _count_list_to_map.
        default_tracking_categories=("landslide",),
        primary_category="landslide",
        publish_incidents=True,
        occupancy_mode="last_primary",
        rollup_mode="latest_snapshot",
    ),
    "car_damage_detection": LegacyAnalyticsProfile(
        application_key_name="car_damage_detection",
        default_application_name="Car Damage Detection",
        # QUALITY metrics aligned with QualityProcessor / car_damage_detection_new.yaml.
        # Resolved from tracking_stats["quality_analytics"] (unique track IDs over
        # the 60s window, with peak-count fallback when tracks never confirm).
        volume_metrics=(
            VolumeMetricSpec("defect_count", "sum", "QUALITY"),
            VolumeMetricSpec("total_inspected", "sum", "QUALITY"),
            VolumeMetricSpec("defect_rate", "avg", "QUALITY"),
        ),
        default_tracking_categories=(
            "dent",
            "scratch",
            "crack",
            "shattered_glass",
            "broken_lamp",
            "flat_tire",
        ),
        primary_category="dent",
        # results-agg (QUALITY metrics) only — car damage does not publish
        # incident_res via the bridge.
        publish_incidents=False,
        occupancy_mode="last_primary",
        rollup_mode="latest_snapshot",
    ),
    # ── Pipe inspection family ────────────────────────────────────────────
    # pipe_corrosion_detection / pipe_gas_leak_detection / liquid_leak_detection
    # are single-class detectors (corrosion / gas_leak / liquid_leak) with
    # spatial merge enabled, so a large defect reads as ONE region: on the
    # reference clips the max simultaneous count is 1 for the entire clip. Their
    # metric sets are therefore built on unique-track counts plus frame-time
    # presence, not on per-frame tallies.
    #
    # All three resolve from a dedicated side-channel block written every frame
    # by the use case (tracking_stats["<domain>_analytics"]); see the
    # _ingest_*_{quality,safety} hooks. All three run an IncidentManager, so
    # publish_incidents=True is the FALLBACK only — the bridge skips
    # incident_res when incident_published_via_manager is set.
    #
    # rollup_mode="window_delta": total_counts now carries cumulative UNIQUE
    # track IDs (the use cases were fixed to stop summing raw per-frame counts),
    # so window-start/window-end totals are a valid per-minute delta.
    "pipe_corrosion_detection": LegacyAnalyticsProfile(
        application_key_name="pipe_corrosion_detection",
        default_application_name="Pipe Corrosion Detection",
        # QUALITY metrics, resolved from tracking_stats["corrosion_analytics"].
        # Matches app-migrations/quality/pipe-corrosion/
        # pipe-corrosion-analytics-metrics.json exactly.
        volume_metrics=(
            VolumeMetricSpec("new_corrosion_count", "sum", "QUALITY"),
            VolumeMetricSpec("total_corrosion_count", "last", "QUALITY"),
            VolumeMetricSpec("peak_corrosion_count", "max", "QUALITY"),
            VolumeMetricSpec("corrosion_presence", "mean", "QUALITY"),
        ),
        default_tracking_categories=("corrosion",),
        primary_category="corrosion",
        publish_incidents=True,
        occupancy_mode="last_primary",
        rollup_mode="window_delta",
    ),
    "pipe_gas_leak_detection": LegacyAnalyticsProfile(
        application_key_name="pipe_gas_leak_detection",
        default_application_name="Pipe Gas Leak Detection",
        # SAFETY metrics, resolved from tracking_stats["gas_analytics"].
        # Matches app-migrations/quality/pipe-gas-leak/
        # pipe-gas-leak-analytics-metrics.json exactly.
        volume_metrics=(
            VolumeMetricSpec("current_gas_leak_count", "last", "SAFETY"),
            VolumeMetricSpec("new_gas_leak_count", "sum", "SAFETY"),
            VolumeMetricSpec("total_gas_leak_count", "last", "SAFETY"),
            VolumeMetricSpec("gas_presence", "mean", "SAFETY"),
            VolumeMetricSpec("gas_duration_seconds", "sum", "SAFETY"),
            VolumeMetricSpec("max_continuous_gas_seconds", "max", "SAFETY"),
        ),
        default_tracking_categories=("gas_leak",),
        primary_category="gas_leak",
        publish_incidents=True,
        occupancy_mode="last_primary",
        rollup_mode="window_delta",
    ),
    # NOTE the profile key is "liquid_leak_detection", NOT "pipe_liquid_leak" —
    # it must match assets/config_files/pipe-liq-leak/liquid_leak_detection.json
    # ("usecase": "liquid_leak_detection"), which has no "pipe_" prefix even
    # though the app folder does.
    "liquid_leak_detection": LegacyAnalyticsProfile(
        application_key_name="liquid_leak_detection",
        default_application_name="Pipe Liquid Leak Detection",
        # SAFETY metrics, resolved from tracking_stats["liquid_analytics"].
        # Matches app-migrations/quality/pipe-liquid-leak/
        # pipe-liquid-leak-analytics-metrics.json exactly.
        volume_metrics=(
            VolumeMetricSpec("current_liquid_leak_count", "last", "SAFETY"),
            VolumeMetricSpec("new_liquid_leak_count", "sum", "SAFETY"),
            VolumeMetricSpec("total_liquid_leak_count", "last", "SAFETY"),
            VolumeMetricSpec("liquid_presence", "mean", "SAFETY"),
            VolumeMetricSpec("liquid_duration_seconds", "sum", "SAFETY"),
            VolumeMetricSpec("max_continuous_liquid_seconds", "max", "SAFETY"),
        ),
        default_tracking_categories=("liquid_leak",),
        primary_category="liquid_leak",
        publish_incidents=True,
        occupancy_mode="last_primary",
        rollup_mode="window_delta",
    ),
    # ── Industrial inspection family ──────────────────────────────────────
    # bottle_defect_detection / pcb_defect_detection /
    # phone_screen_defect_detection / solar_panel all resolve from the shared
    # superset block tracking_stats["quality_analytics"] via
    # _ingest_inspection_quality (see _INSPECTION_QUALITY_APPS above).
    #
    # Metric keys match app-migrations/quality/<app>/<app>-analytics-metrics.json
    # EXACTLY — those JSON files are the contract; the profile follows them.
    #
    # rollup_mode="window_delta": every one of these use cases puts cumulative
    # UNIQUE track IDs in total_counts (never a raw per-frame sum), so a
    # window-start/window-end delta is valid and current_counts reads as "units
    # that arrived this window" — the throughput number these dashboards want.
    #
    # Three of the four are QUALITY+INCIDENT per their manifests and run an
    # IncidentManager, so publish_incidents=True is the FALLBACK only — the
    # bridge skips incident_res when incident_published_via_manager is set.
    # bottle is QUALITY-only (no INCIDENT module in bottle-defect.yaml), so it
    # keeps publish_incidents=False, the same arrangement as car_damage_detection:
    # the use case still builds an incident dict for agg_summary, but nothing
    # publishes it to incident_res.
    "bottle_defect_detection": LegacyAnalyticsProfile(
        application_key_name="bottle_defect_detection",
        default_application_name="Bottle Defect Detection",
        volume_metrics=(
            VolumeMetricSpec("defect_count", "sum", "QUALITY"),
            VolumeMetricSpec("total_defect_count", "last", "QUALITY"),
            VolumeMetricSpec("defect_presence", "mean", "QUALITY"),
        ),
        default_tracking_categories=("defect",),
        primary_category="defect",
        publish_incidents=False,
        occupancy_mode="last_primary",
        rollup_mode="window_delta",
    ),
    "phone_screen_defect_detection": LegacyAnalyticsProfile(
        application_key_name="phone_screen_defect_detection",
        default_application_name="Phone Screen Defect Detection",
        volume_metrics=(
            VolumeMetricSpec("defect_count", "sum", "QUALITY"),
            VolumeMetricSpec("total_defect_count", "last", "QUALITY"),
            VolumeMetricSpec("defect_presence", "mean", "QUALITY"),
        ),
        # Canonical snake_case: the model emits Title-Case "Scratched", which the
        # use case normalizes to "scratched" before it reaches tracking_stats.
        default_tracking_categories=("scratched",),
        primary_category="scratched",
        publish_incidents=True,
        occupancy_mode="last_primary",
        rollup_mode="window_delta",
    ),
    "pcb_defect_detection": LegacyAnalyticsProfile(
        application_key_name="pcb_defect_detection",
        default_application_name="PCB Defect Detection",
        volume_metrics=(
            VolumeMetricSpec("defect_count", "sum", "QUALITY"),
            VolumeMetricSpec("total_defect_count", "last", "QUALITY"),
            VolumeMetricSpec("defect_presence", "mean", "QUALITY"),
        ),
        # All six classes are defect types (no board/healthy class), which is why
        # the manifest publishes defect_presence rather than defect_rate.
        default_tracking_categories=(
            "Missing_Hole",
            "MouseBite",
            "Open_Circuit",
            "Short_Circuit",
            "Spur",
            "Spurious_Cooper",
        ),
        primary_category="Missing_Hole",
        publish_incidents=True,
        occupancy_mode="last_primary",
        rollup_mode="window_delta",
    ),
    # NOTE the profile key is "solar_panel", NOT "solar_panel_detection" —
    # SolarPanelUseCase registers itself as "solar_panel" (BaseProcessor.__init__
    # + CASE_TYPE), and the profile key must match the deployment "usecase".
    "solar_panel": LegacyAnalyticsProfile(
        application_key_name="solar_panel",
        default_application_name="Solar Panel Detection",
        # The ONLY app in this family with a healthy population (`panel`), so the
        # only one that can publish a real defect_rate instead of a presence %.
        volume_metrics=(
            VolumeMetricSpec("defect_count", "sum", "QUALITY"),
            VolumeMetricSpec("total_inspected", "sum", "QUALITY"),
            VolumeMetricSpec("defect_rate", "mean", "QUALITY"),
            VolumeMetricSpec("total_defect_count", "last", "QUALITY"),
        ),
        default_tracking_categories=("panel", "cracked"),
        primary_category="panel",
        publish_incidents=True,
        occupancy_mode="last_primary",
        rollup_mode="window_delta",
    ),
    # ── Assembly line (VOLUME only) ───────────────────────────────────────
    # Resolves from tracking_stats["assembly_analytics"] via
    # _ingest_assembly_volume. VOLUME-only per
    # app-migrations/volume/assembly-monitoring/assembly-monitoring.yaml:
    # publish_incidents=False because the robot arms are permanently in frame, so
    # a presence-based incident would never close. Revisit only when the trigger
    # is a stall/absence condition.
    #
    # No exit_count metric: without zone geometry the counting path has no exit
    # concept, so declaring it would publish a permanent 0.
    "assembly_line_detection": LegacyAnalyticsProfile(
        application_key_name="assembly_line_detection",
        default_application_name="Automated Assembly Line Monitoring",
        volume_metrics=(
            VolumeMetricSpec("plate_throughput", "sum"),
            VolumeMetricSpec("empty_plate_throughput", "sum"),
            VolumeMetricSpec("line_utilization", "mean"),
            VolumeMetricSpec("entry_count", "sum"),
            VolumeMetricSpec("current_occupancy", "last"),
            VolumeMetricSpec("active_robot_arms", "max"),
        ),
        default_tracking_categories=(
            "metal-plate",
            "metal-plate-empty",
            "robot-arms",
            "robot-arms-2",
            "robot-arms-3",
        ),
        primary_category="metal-plate",
        publish_incidents=False,
        occupancy_mode="last_primary",
        rollup_mode="window_delta",
    ),
    "illegal_parking_detection": LegacyAnalyticsProfile(
        application_key_name="illegal_parking_detection",
        default_application_name="Illegal Parking Detection",
        # VOLUME metrics matching illegal-parking-detection-analytics-metrics.json.
        # total_violations / total_vehicles_tracked are unique canonical-track-id
        # counts accumulated over the ~60s window (same window-unique-id pattern as
        # car_damage_detection's defect_count / total_inspected); violation_rate is
        # the window ratio between them; avg_dwell_time_sec is the mean confirmed
        # dwell duration of violations newly confirmed during the window. All four
        # keys are custom, resolved in _resolve_metric_value from
        # tracking_stats["illegal_parking_analytics"]'s frame_vehicle_ids /
        # frame_violation_ids / frame_confirmed_dwell_seconds.
        volume_metrics=(
            VolumeMetricSpec("total_violations", "sum"),
            VolumeMetricSpec("total_vehicles_tracked", "sum"),
            VolumeMetricSpec("violation_rate", "mean"),
            VolumeMetricSpec("avg_dwell_time_sec", "avg"),
        ),
        default_tracking_categories=("bicycle", "motorcycle", "car", "van", "bus", "truck"),
        primary_category="car",
        # The use case emits no incident_data (no IncidentManager wiring), so this
        # bridge fallback never fires either way; VOLUME results-agg is what backs
        # the appstore config today.
        publish_incidents=False,
        occupancy_mode="last_primary",
        # current_counts (per-class violation-bar widgets) are a point-in-time
        # snapshot of active violations, not a windowed delta -- same rollup as
        # mask_detection / gender_detection / car_damage_detection.
        rollup_mode="latest_snapshot",
    ),
    "vehicle_monitoring_wrong_way": LegacyAnalyticsProfile(
        application_key_name="vehicle_monitoring_wrong_way",
        default_application_name="Vehicle Monitoring — Wrong Way",
        # VOLUME: latest wrong-way / suspect counts + whole-frame vehicle
        # composition. INCIDENT is published by the use case's IncidentManager
        # (publish_incidents=True is the fallback only — the bridge skips it
        # when incident_published_via_manager is set).
        volume_metrics=(
            VolumeMetricSpec("current_wrong_way_count", "last"),
            VolumeMetricSpec("total_wrong_way_events", "last"),
            VolumeMetricSpec("current_suspect_count", "last"),
            VolumeMetricSpec("vehicle_count", "last"),
        ),
        default_tracking_categories=("car", "truck", "bus", "van", "motorcycle", "bicycle"),
        primary_category="car",
        publish_incidents=True,
        occupancy_mode="last_primary",
    ),
    "running_detection": LegacyAnalyticsProfile(
        application_key_name="running_detection",
        default_application_name="Running Detection",
        # VOLUME: latest confirmed-running count + windowed peak/entry sum,
        # all of which resolve from the generic "running" category (this
        # use case's only tracked category — see primary_category below).
        # INCIDENT is published by the use case's IncidentManager
        # (publish_incidents=True is the fallback only — the bridge skips it
        # when incident_published_via_manager is set).
        volume_metrics=(
            VolumeMetricSpec("current_running_count", "last"),
            VolumeMetricSpec("total_running_events", "sum"),
            VolumeMetricSpec("peak_running_count", "last"),
        ),
        default_tracking_categories=("running",),
        primary_category="running",
        publish_incidents=True,
        occupancy_mode="last_primary",
    ),
}

# Use-cases deliberately left OUT of the bridge. These are still-image
# classifiers / segmentation models (medical, pathology, microscopy): they run
# per-image, emit no video ``tracking_stats`` and no streaming incidents, so
# there is nothing to roll up over a 60s window. Publishing an empty results-agg
# for them every minute would be pure noise, and the OLD AnalyticsPublisher also
# skips cameras whose store never fills. Excluded (not bridged):
_EXCLUDED_USECASES = frozenset(
    {
        "histopathological_cancer_detection",
        "bloodcancer_img_detection",
        "skincancer_img_classification",
        "cardiomegaly_classification",
        "plaque_img_segmentation",
        "cell_microscopy_segmentation",
        "wound_segmentation",
        "leaf_det",
        "leaf_disease_detection",
        "flower_segmentation",
    }
)

_sessions: Dict[str, "LegacyAnalyticsSession"] = {}

# Cache of the synthesized default profiles, keyed by usecase.
_default_profiles: Dict[str, LegacyAnalyticsProfile] = {}


def _humanize(usecase: str) -> str:
    return " ".join(part.capitalize() for part in str(usecase).split("_") if part) or "Application"


def _make_default_profile(usecase: str) -> LegacyAnalyticsProfile:
    """Sensible-default profile for any legacy app without an explicit entry.

    Publishes ``incident_res`` whenever the use-case emits an incident, and a
    generic ``current_occupancy`` results-agg metric (``occupancy_mode
    "last_primary"`` sums the latest per-class ``current_counts`` when no primary
    category matches). The zone-keyed ``tracking_stats`` rollup is identical to
    the explicit profiles / the OLD ``AnalyticsPubliser`` (current=sum-of-new,
    total_current=baseline+sum-new, total=latest).
    """
    prof = _default_profiles.get(usecase)
    if prof is None:
        prof = LegacyAnalyticsProfile(
            application_key_name=usecase,
            default_application_name=_humanize(usecase),
            volume_metrics=(VolumeMetricSpec("current_occupancy", "last"),),
            # No hard-coded categories: the tracking_stats rollup is derived
            # purely from whatever categories the app emits (empty until data
            # arrives), so we never inject spurious zero-count classes.
            default_tracking_categories=(),
            primary_category="",  # no match -> occupancy falls back to sum(current)
            # Default OFF: auto-discovered apps publish results-agg counts only.
            # Incidents (incident_res) are opt-IN via an explicit profile with
            # publish_incidents=True (weapon, fire, ...). Prevents classification/
            # detection apps (e.g. mask_detection) from flooding incident_res with
            # per-event "alerts" — especially on shared camera feeds.
            publish_incidents=False,
            occupancy_mode="last_primary",
        )
        _default_profiles[usecase] = prof
    return prof


def _discover_registered_usecases() -> frozenset[str]:
    """All legacy use-case names known to the global processor registry.

    Registration is populated at import of ``matrice_analytics.post_processing``
    and completed when a ``PostProcessor`` is constructed (which always happens
    before any frame is published), so by publish time this reflects the full
    catalog. Failures degrade to an empty set (explicit profiles still work).
    """
    try:
        from ..core.base import registry

        return frozenset(name for names in registry.list_use_cases().values() for name in names)
    except Exception:  # pragma: no cover - registry always importable in practice
        return frozenset()


def legacy_redis_analytics_usecases() -> frozenset[str]:
    """Every legacy app the SDK self-publishes (incident_res + results-agg).

    Full coverage: the explicit profiles PLUS every use-case in the processor
    registry, minus the documented still-image exclusions. Returns an EMPTY set
    when :data:`LEGACY_PUBLISHER_ENV` is truthy, ceding ownership to the caller's
    old ``AnalyticsPublisher`` so there is no double-publish.
    """
    if _env_truthy(LEGACY_PUBLISHER_ENV):
        return frozenset()
    names = set(_LEGACY_PROFILES.keys()) | set(_discover_registered_usecases())
    names -= _EXCLUDED_USECASES
    return frozenset(names)


def get_legacy_profile(usecase: str) -> Optional[LegacyAnalyticsProfile]:
    """Explicit profile if registered, else a synthesized default profile.

    Returns ``None`` only for the documented still-image exclusions, so that a
    caller can distinguish "no analytics wiring" from "default wiring".
    """
    explicit = _LEGACY_PROFILES.get(usecase)
    if explicit is not None:
        return explicit
    if not usecase or usecase in _EXCLUDED_USECASES:
        return None
    return _make_default_profile(usecase)


def get_legacy_session(stream_key: str) -> "LegacyAnalyticsSession":
    key = stream_key or "default_stream"
    if key not in _sessions:
        _sessions[key] = LegacyAnalyticsSession(stream_key=key)
    return _sessions[key]


def reset_legacy_sessions() -> None:
    _sessions.clear()


def _coerce_optional_int(value: Any) -> Optional[int]:
    """``int(value)``, or ``None`` when there is no usable number.

    ``None`` is meaningful for the window-start baselines: it means "no reading
    yet", which the delta resolvers treat as "no growth to report" rather than
    as a baseline of 0 (which would publish the whole session's total).
    """
    if value is None:
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _utc_now_iso_z() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _utc_stream_time() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")


def _count_list_to_map(items: Any) -> Dict[str, int]:
    out: Dict[str, int] = {}
    if not isinstance(items, list):
        return out
    for entry in items:
        if not isinstance(entry, dict):
            continue
        cat = str(entry.get("category", "")).lower()
        if not cat:
            continue
        try:
            out[cat] = int(entry.get("count", 0) or 0)
        except (TypeError, ValueError):
            out[cat] = 0
    return out


def _map_to_count_list(counts: Mapping[str, int]) -> List[Dict[str, Any]]:
    return [{"category": cat, "count": int(count)} for cat, count in sorted(counts.items())]


def _default_count_list(categories: Tuple[str, ...]) -> List[Dict[str, Any]]:
    return [{"category": cat, "count": 0} for cat in categories]


def _filter_count_map(counts: Mapping[str, int], categories: Tuple[str, ...]) -> Dict[str, int]:
    """Keep only profile tracking categories (e.g. knife/gun-only for weapon_detection)."""
    if not categories:
        return dict(counts)
    allowed = frozenset(cat.lower() for cat in categories)
    return {cat: int(count) for cat, count in counts.items() if cat.lower() in allowed}


def _restore_canonical_casing(items: List[Dict[str, Any]], categories: Tuple[str, ...]) -> List[Dict[str, Any]]:
    """Re-key a count list from lowercase back to its real display casing.

    _count_list_to_map/_filter_count_map unconditionally lowercase every
    category for internal storage/matching (a pre-existing, systemic quirk —
    affects any profile with a non-lowercase category, e.g. pedestrian's
    "Pedestrian" or flare_analysis's "BadFlare"/"GoodFlare"). Internal
    lookups must stay on the lowercased key; this only relabels the OUTPUT
    count list back to profile.default_tracking_categories' real casing, so
    published tracking_stats match the wire-visible display name.
    """
    if not categories:
        return items
    canonical = {cat.lower(): cat for cat in categories}
    counts = _count_list_to_map(items)
    restored: Dict[str, int] = {}
    for cat, count in counts.items():
        restored[canonical.get(cat, cat)] = count
    return _map_to_count_list(restored)


def _ensure_total_current_at_least_current(
    current_counts: List[Dict[str, Any]],
    total_current_counts: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """Guarantee total_current_counts[cat] >= current_counts[cat] for every category.

    total_current_counts is "everyone present during the window" (including people
    who were already there before the window started); current_counts is only the
    NEW arrivals during the window, so it can never legitimately exceed the total.
    A mismatch here means an upstream bookkeeping edge case (stale carry, category
    drift, mid-window reset) rather than a real state -- clamp instead of publishing
    a value that breaks the invariant downstream consumers rely on.
    """
    total_map = _count_list_to_map(total_current_counts)
    for cat, cur in _count_list_to_map(current_counts).items():
        if total_map.get(cat, 0) < cur:
            total_map[cat] = cur
    return _map_to_count_list(total_map) if total_map else total_current_counts


def extract_stream_context(
    stream_info: Optional[Dict[str, Any]],
    *,
    usecase: str,
    app_name: Optional[str] = None,
    app_version: str = "1.0",
) -> Dict[str, str]:
    """Resolve camera / deployment identity fields for Redis envelopes."""
    from ...analytics.engine_session import resolve_camera_fields_from_stream_info, resolve_location_for_publish

    si = stream_info or {}
    inp = si.get("input_settings") if isinstance(si.get("input_settings"), dict) else {}
    profile = get_legacy_profile(usecase)
    key_name = profile.application_key_name if profile else usecase
    default_app = profile.default_application_name if profile else (usecase or "Application")
    cam_fields = resolve_camera_fields_from_stream_info(si)

    camera_id = str(
        cam_fields.get("camera_id") or si.get("camera_id") or inp.get("camera_id") or si.get("stream_key") or "camera"
    )
    camera_name = str(cam_fields.get("camera_name") or "")
    loc = resolve_location_for_publish(si)

    if not loc.get("locationId"):
        # resolve_location_for_publish only checks stream_config / top-level
        # camera_info / input_stream-nested camera_info. Some callers instead
        # nest camera_info directly under input_settings (the same shape
        # incident_manager_utils.py already handles for incident_res) — widen
        # the id search here, additively, so results-agg does not miss an id
        # that incident_res already finds via that path.
        from .post_processing_config_client import is_resolvable_location_id, normalize_location_id

        inp_camera_info = inp.get("camera_info") if isinstance(inp.get("camera_info"), dict) else {}
        for candidate in (
            inp.get("location_id"),
            inp.get("locationId"),
            inp_camera_info.get("location_id"),
            inp_camera_info.get("locationId"),
            inp_camera_info.get("location"),
        ):
            text = str(candidate or "").strip()
            if is_resolvable_location_id(text):
                loc = {**loc, "locationId": normalize_location_id(text)}
                break

    if loc.get("locationId") and loc.get("location") in ("", "Unknown Location"):
        resolved_name = _fetch_location_name_cached(loc["locationId"])
        if resolved_name:
            loc = {**loc, "location": resolved_name}
    return {
        "camera_id": camera_id,
        "camera_name": camera_name,
        "app_deployment_id": str(si.get("app_deployment_id") or inp.get("app_deployment_id") or ""),
        "app_id": str(si.get("application_id") or si.get("app_id") or key_name),
        "camera_group": str(si.get("camera_group") or inp.get("camera_group") or "default_group"),
        "locationId": loc["locationId"],
        "location": loc["location"],
        "application_name": str(app_name or si.get("application_name") or default_app),
        "application_key_name": key_name,
        "application_version": str(si.get("application_version") or app_version),
        "frame_id": str(si.get("frame_id") or inp.get("frame_id") or ""),
        "rtp_number": str(si.get("rtp_number") or inp.get("rtp_number") or ""),
        "stream_time": str(si.get("stream_time") or inp.get("stream_time") or _utc_stream_time()),
    }


def build_incident_message(
    incident_data: Dict[str, Any],
    stream_info: Optional[Dict[str, Any]],
    *,
    usecase: str,
    app_name: Optional[str] = None,
    camera_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Build ``incident_res`` payload matching NEW-flow ``IncidentMessage``."""
    if not incident_data:
        return {}
    from .incident_res_format import build_incident_res_message

    ctx = extract_stream_context(stream_info, usecase=usecase, app_name=app_name)
    cid = camera_id or ctx["camera_id"]
    return build_incident_res_message(
        incident_data,
        stream_info,
        camera_id=cid,
        application_name=app_name or ctx.get("application_name"),
        location_name=ctx.get("location"),
        factory_app_deployment_id=ctx.get("app_deployment_id", ""),
        factory_application_id=ctx.get("app_id", ""),
        frame_id=ctx.get("frame_id", ""),
        stream_time=ctx.get("stream_time", ""),
    )


@dataclass
class LegacyAnalyticsSession:
    """Per-stream accumulator for 60s ``results-agg`` publishing."""

    stream_key: str
    last_agg_publish_ts: float = 0.0
    last_incident_level: str = "none"
    # True once a frame with tracking_stats has been ingested. Mirrors the OLD
    # AnalyticsPublisher, which never publishes results-agg for a camera whose
    # store stayed empty (apps that emit no tracking_stats).
    saw_tracking: bool = False
    # weapon/fire occupancy window
    window_weapon_max: int = 0
    window_person_max: int = 0
    # VOLUME window (mirrors VolumeProcessor simple mode)
    window_new_sum: Dict[str, int] = field(default_factory=dict)
    # First-frame-of-window occupancy snapshot (legacy; no longer used for
    # total_current_counts rollup — see prev_window_last_frame_current).
    window_baseline: Dict[str, int] = field(default_factory=dict)
    window_baseline_set: bool = False
    # Carry into the next 60s results-agg tracking_stats block:
    # last-frame in-frame current_counts from the previous published window.
    # Empty / zeros on the first agg after stream start so
    # total_current_counts == current_counts (window new sum) for that publish.
    prev_window_last_frame_current: Dict[str, int] = field(default_factory=dict)
    # Max per-frame total_current_counts seen in the current 60s window
    # (used by latest_snapshot rollup apps; non-snapshot apps use prev-window carry).
    window_total_current_max: Dict[str, int] = field(default_factory=dict)
    window_start_totals: Dict[str, int] = field(default_factory=dict)
    window_start_totals_set: bool = False
    window_entry_total: int = 0
    window_exit_total: int = 0
    # footfall: peak concurrent occupancy of the two-line corridor (in+out)
    # seen this 60s window, for entrance_congestion (agg_type "max").
    window_corridor_occupancy_peak: int = 0
    last_occupancy: int = 0
    # people_counting: highest single-frame occupancy seen in the current window
    window_peak_occupancy: int = 0
    # Windowed mean of loitering share (loiterers / people in frame * 100) for the
    # loitering_percentage "mean" metric — accumulated per frame, averaged on publish.
    window_loiter_pct_sum: float = 0.0
    window_loiter_pct_frames: int = 0
    # avg/max_loiter_time_seconds — latest snapshot of the usecase's own
    # tracking_stats["loitering_analytics"], same pattern as last_intrusion_analytics.
    last_loitering_analytics: Dict[str, Any] = field(default_factory=dict)
    # parking_lot_analytics window. park_entry_counts/park_exit_counts and
    # parked_vehicles_count/per-class counts are per-window SUMS (this
    # minute's corridor crossings / newly-parked events), not cumulative
    # snapshots — see the profile's volume_metrics comment.
    window_park_entry_sum: int = 0
    window_park_exit_sum: int = 0
    last_avg_parking_time: float = 0.0
    # Per-window peak of max-dwell-among-currently-open-sessions (agg_type
    # "max"), NOT an all-time high-water mark — matches
    # ParkingAnalyticsTracker._get_max_parked_time_seconds's own semantics.
    window_max_parked_seconds: float = 0.0
    window_newly_parked_sum: int = 0
    window_newly_parked_by_category: Dict[str, int] = field(default_factory=dict)
    # dwell window — latest snapshot of the use case's dwell_analytics block.
    last_visitors_in_zone: int = 0
    last_active_dwellers: int = 0
    last_unique_dwellers: int = 0
    last_avg_dwell_seconds: float = 0.0
    last_max_dwell_seconds: float = 0.0
    # Windowed mean of the per-frame dweller share, for dwell_percentage.
    window_dwell_pct_sum: float = 0.0
    window_dwell_pct_frames: int = 0
    # ppe_compliance SAFETY window — unique track IDs + per-frame compliance mean.
    window_person_ids: set = field(default_factory=set)
    window_violator_ids: set = field(default_factory=set)
    window_hardhat_ids: set = field(default_factory=set)
    window_safety_vest_ids: set = field(default_factory=set)
    window_mask_ids: set = field(default_factory=set)
    window_compliance_pct_sum: float = 0.0
    window_compliance_pct_frames: int = 0

    # hazard_zone_entry
    last_hazard_analytics: Dict[str, Any] = field(default_factory=dict)
    window_hazard_pct_sum: float = 0.0
    window_hazard_pct_frames: int = 0
    # Cumulative unique_zone_entrants at the window's first frame — the baseline
    # for the per-minute NEW at-risk delta (people_at_risk). None until the first
    # hazard frame of the window is ingested; reset each window.
    hazard_window_start_entrants: Optional[int] = None
    # advanced_customer_service -- counter model side channel.
    last_customer_service_analytics: Dict[str, Any] = field(default_factory=dict)
    window_counter_util_sum: float = 0.0
    window_counter_util_frames: int = 0
    window_staff_cov_sum: float = 0.0
    window_staff_cov_frames: int = 0
    window_queue_len_sum: int = 0
    window_queue_len_frames: int = 0
    window_cs_max_queue: int = 0
    window_cs_ratio_sum: float = 0.0
    window_cs_ratio_frames: int = 0
    # Window-start baselines for the *_in_interval deltas. None only before the
    # very first customer-service frame of the session; from then on _reset_window
    # re-seeds each one from the closing window's final reading, so consecutive
    # windows' deltas partition the session total with no gap at the boundary.
    cs_window_start_customers: Optional[int] = None
    cs_window_start_served: Optional[int] = None
    cs_window_start_abandoned: Optional[int] = None

    # intrusion_detection
    last_intrusion_analytics: Dict[str, Any] = field(default_factory=dict)
    window_intrusion_pct_sum: float = 0.0
    window_intrusion_pct_frames: int = 0
    # Cumulative unique_intruders at the window's first frame — the baseline for
    # the per-minute NEW intruders delta (intruders_in_interval). None until the
    # first intrusion frame of the window is ingested; reset each window.
    intrusion_window_start_intruders: Optional[int] = None
    # tailgating_detection
    last_tailgating_analytics: Dict[str, Any] = field(default_factory=dict)
    window_tailgating_events_sum: int = 0
    window_tailgating_pct_sum: float = 0.0
    window_tailgating_pct_frames: int = 0
    # overcrowding_detection
    last_overcrowding_analytics: Dict[str, Any] = field(default_factory=dict)
    window_occupancy_peak: int = 0
    window_occupancy_sum: int = 0
    window_occupancy_frames: int = 0
    window_occupancy_pct_sum: float = 0.0
    window_occupancy_pct_frames: int = 0
    # area_utilization: no side-channel block (unlike overcrowding_detection),
    # so avg_occupancy / time_occupied_percent accumulate from the generic
    # last_occupancy computed in ingest_agg_summary rather than from a
    # dedicated analytics dict.
    area_util_window_occupancy_sum: int = 0
    area_util_window_occupancy_frames: int = 0
    area_util_window_occupied_frames: int = 0
    # abandoned_object_detection: last frame's active_track_count side-channel
    # (every object the state machine is following, abandoned or not). Not
    # derivable from current_counts, which the profile scopes to the
    # "abandoned_object" category only.
    last_abandoned_active_tracks: int = 0

    # dwell window accumulators — unique track_ids seen across the 60s window.
    # visitors = any in-zone person (person or Dweller category).
    # dwellers = only tracks promoted to Dweller status.
    window_visitor_ids: set = field(default_factory=set)
    window_dweller_ids: set = field(default_factory=set)
    # flood_detection: per-frame snapshot + window accumulators.
    last_flood_detection_count: int = 0
    last_max_flood_area_pct: float = 0.0
    last_total_flood_area_pct: float = 0.0
    # Windowed mean of max_flood_area_pct, for avg_flood_area_percentage.
    # floods_occurred itself needs no dedicated state — it reads window_new_sum
    # (generic current_new_counts→window_new_sum pipeline, since flood_detection.py
    # already runs a real tracker and reports new track IDs per frame).
    window_flood_pct_sum: float = 0.0
    window_flood_pct_frames: int = 0
    # landslide_detection: per-frame snapshot + window accumulators.
    last_landslide_detection_count: int = 0
    last_max_landslide_area_pct: float = 0.0
    last_total_landslide_area_pct: float = 0.0
    # Windowed mean of max_landslide_area_pct, for avg_surface_displacement_percentage.
    # landslides_occurred likewise reads window_new_sum directly (no custom state).
    window_landslide_pct_sum: float = 0.0
    window_landslide_pct_frames: int = 0
    # car_damage_detection QUALITY window — unique track IDs + peak fallback
    # (mirrors QualityProcessor aggregate_1min semantics).
    window_defect_ids: set = field(default_factory=set)
    window_inspected_ids: set = field(default_factory=set)
    window_peak_defect: int = 0
    window_peak_inspected: int = 0
    last_quality_analytics: Dict[str, Any] = field(default_factory=dict)
    # ── Pipe inspection family (corrosion / gas leak / liquid leak) ──────────
    # One shared accumulator set — a session only ever has one profile, so the
    # three apps never contend for these fields. Populated by
    # _ingest_pipe_defect_analytics from the use case's side-channel block.
    #   pipe_window_new_ids   – union of frame_new_ids over the window; len() is
    #                           the deduplicated new_*_count (a region present
    #                           for the whole window contributes exactly once).
    #   pipe_window_peak      – max per-frame region count in the window.
    #   pipe_last_current     – last frame's region count (agg "last" metrics).
    #   pipe_last_total_unique– last cumulative unique-track total.
    #   pipe_window_active/total_frames – true PER-WINDOW presence denominator.
    #     Deliberately NOT the use case's session-cumulative presence_ratio: that
    #     converges and would flatten the "presence % over time" chart.
    #   pipe_window_active_seconds – sum of frame_seconds over ACTIVE frames only.
    #   pipe_max_continuous_seconds – max streak length reported in the window.
    pipe_window_new_ids: set = field(default_factory=set)
    pipe_window_peak: int = 0
    pipe_last_current: int = 0
    pipe_last_total_unique: int = 0
    pipe_window_active_frames: int = 0
    pipe_window_total_frames: int = 0
    pipe_window_active_seconds: float = 0.0
    pipe_max_continuous_seconds: float = 0.0
    # ── Industrial inspection family (bottle / pcb / phone screen / solar) ────
    # The defect/inspected ID sets and peak fallbacks are SHARED with
    # car_damage_detection above (window_defect_ids / window_inspected_ids /
    # window_peak_defect / window_peak_inspected) — identical semantics, and a
    # session only ever has one profile, so the two families never contend.
    # Only the fields car damage has no equivalent for are added here:
    #   insp_window_new_defect_ids  – union of frame_new_ids; first-seen only, so
    #                                 this is "defects that ARRIVED this window"
    #                                 (kept for a future new_* metric; the current
    #                                 defect_count uses the observed-ids union).
    #   insp_last_total_unique      – cumulative unique defect tracks since
    #                                 session start, for total_defect_count
    #                                 (agg "last"). Preserved across window reset.
    #   insp_window_active/total_frames – true PER-WINDOW presence denominator.
    #                                 Deliberately NOT the use case's cumulative
    #                                 presence_ratio, which converges and would
    #                                 flatten the "presence % over time" chart.
    insp_window_new_defect_ids: set = field(default_factory=set)
    insp_last_total_unique: int = 0
    insp_window_active_frames: int = 0
    insp_window_total_frames: int = 0
    insp_max_continuous_seconds: float = 0.0
    # ── assembly_line_detection VOLUME window ────────────────────────────────
    #   asm_window_new_*_ids     – unions of first-seen carrier track IDs, so one
    #                              plate counts once per window however many
    #                              frames it spans (the reason the use case ships
    #                              ID lists rather than per-frame counts).
    #   asm_window_peak_robot_arms – max simultaneous arms; "max" not "last" so a
    #                              single occluded frame doesn't read as a
    #                              stopped station.
    #   asm_last_current_total   – last frame's mapped-object count, for
    #                              current_occupancy. Preserved across reset.
    asm_window_new_loaded_ids: set = field(default_factory=set)
    asm_window_new_empty_ids: set = field(default_factory=set)
    asm_window_peak_robot_arms: int = 0
    asm_last_current_total: int = 0
    # illegal_parking_detection VOLUME window -- unique canonical track IDs seen
    # this window (any of the 6 vehicle classes) and confirmed as violations,
    # plus the confirmed-dwell durations of violations newly confirmed this
    # window (for avg_dwell_time_sec) and peak-cumulative fallbacks for when
    # frame_vehicle_ids / frame_violation_ids are unavailable.
    window_tracked_vehicle_ids: set = field(default_factory=set)
    window_violation_ids: set = field(default_factory=set)
    window_dwell_sum: float = 0.0
    window_dwell_count: int = 0
    window_peak_tracked: int = 0
    window_peak_violations: int = 0
    # vehicle_monitoring_wrong_way: latest snapshot of the side-channel
    # tracking_stats["wrong_way_analytics"] block (not a standard current_counts
    # category, so it's read separately — same pattern as last_hazard_analytics).
    last_wrong_way_analytics: Dict[str, Any] = field(default_factory=dict)

    latest_tracking: Dict[str, Any] = field(default_factory=dict)
    latest_totals: Dict[str, int] = field(default_factory=dict)
    latest_current: Dict[str, int] = field(default_factory=dict)
    latest_frame_current: Dict[str, int] = field(default_factory=dict)
    latest_new: Dict[str, int] = field(default_factory=dict)
    # footfall: raw detection count from tracking_stats.detections (latest frame)
    last_num_detections: int = 0
    # accident_detection: count of confirmed accident episodes this window whose
    # incident carried severity_level == "critical", for critical_accidents.
    window_critical_accidents: int = 0
    # stopped_vehicle_monitoring: latest-frame confirmed stopped-vehicle count
    # (tracking_stats["stopped_vehicle_count"], a snapshot) and the session
    # cumulative stop-event total (stopped_vehicle_analytics["total_events"],
    # monotonic). window_stopped_peak is the max confirmed stopped count seen
    # across the window, for a stable per-minute headline.
    last_stopped_vehicle_count: int = 0
    last_stopped_total_events: int = 0
    window_stopped_peak: int = 0

    def ingest_agg_summary(self, agg_summary: Any, *, profile: LegacyAnalyticsProfile) -> None:
        if not isinstance(agg_summary, dict) or not agg_summary:
            return
        frame_data = next(iter(agg_summary.values()), {})
        if not isinstance(frame_data, dict):
            return
        tracking = frame_data.get("tracking_stats")
        if not isinstance(tracking, dict):
            return

        self.saw_tracking = True
        self.latest_tracking = dict(tracking)
        current = _filter_count_map(
            _count_list_to_map(tracking.get("current_counts")), profile.default_tracking_categories
        )
        totals = _filter_count_map(
            _count_list_to_map(tracking.get("total_counts")), profile.default_tracking_categories
        )
        new = _filter_count_map(
            _count_list_to_map(tracking.get("current_new_counts")), profile.default_tracking_categories
        )

        # accident_detection: current_new_counts["accident"] fires exactly once per
        # debounced episode (episode-confirm frame — see accident_detection.py's
        # _update_presence_state/"new_this_frame"), so gate on that instead of
        # counting every frame the incident stays open. Read severity straight off
        # this same frame's incident block (agg_summary[...]["incidents"]), not
        # tracking_stats, since severity isn't a tracking_stats field.
        if profile.application_key_name == "accident_detection" and new.get("accident", 0) > 0:
            incident_data = frame_data.get("incidents")
            if isinstance(incident_data, dict) and str(incident_data.get("severity_level", "")).lower() == "critical":
                self.window_critical_accidents += 1

        total_current = _filter_count_map(
            _count_list_to_map(tracking.get("total_current_counts")),
            profile.default_tracking_categories,
        )
        dets = tracking.get("detections", [])
        self.last_num_detections = len(dets) if isinstance(dets, list) else 0
        if total_current:
            self.latest_current = total_current
        elif current:
            self.latest_current = current
        self.latest_frame_current = dict(current)

        # vehicle_monitoring per-minute throughput is derived generically from
        # window_new_sum / window_entry_total (accumulated below from
        # current_new_counts), so no vehicle-specific per-frame bookkeeping is
        # needed here — the resolver reads those window accumulators directly.

        if totals:
            if profile.application_key_name == "weapon_detection":
                for cat, count in totals.items():
                    self.latest_totals[cat] = max(self.latest_totals.get(cat, 0), int(count))
            else:
                self.latest_totals = totals
            if not self.window_start_totals_set:
                self.window_start_totals = dict(self.latest_totals)
                self.window_start_totals_set = True
        if new:
            self.latest_new = new

        if not self.window_baseline_set and self.latest_current:
            # Legacy first-frame snapshot (kept for parity with older ingest
            # bookkeeping). results-agg total_current_counts now uses
            # prev_window_last_frame_current for non-snapshot rollups.
            self.window_baseline = dict(self.latest_current)
            self.window_baseline_set = True

        frame_total_current = total_current if total_current else current
        for cat, count in frame_total_current.items():
            self.window_total_current_max[cat] = max(
                self.window_total_current_max.get(cat, 0),
                int(count),
            )

        for cat, count in new.items():
            if count > 0:
                self.window_new_sum[cat] = self.window_new_sum.get(cat, 0) + count
                self.window_entry_total += count

        # Simple-mode exit_count stays 0; footfall-style apps may supply "out" later.
        self.window_exit_total += new.get("out", 0)

        # Windowed mean of the per-frame loitering share (for loitering_percentage).
        # Uses this frame's current_counts; only relevant to loitering profiles.
        if "loitering_person" in profile.default_tracking_categories:
            loiter_now = current.get("loitering_person", 0)
            people_now = loiter_now + current.get("person", 0)
            if people_now > 0:
                self.window_loiter_pct_sum += (loiter_now / people_now) * 100.0
                self.window_loiter_pct_frames += 1

        # footfall: peak concurrent occupancy of the two-line corridor this
        # window (in+out), for entrance_congestion.
        if profile.application_key_name == "footfall":
            try:
                corridor_now = int(tracking.get("corridor_occupancy", 0) or 0)
            except (TypeError, ValueError):
                corridor_now = 0
            self.window_corridor_occupancy_peak = max(self.window_corridor_occupancy_peak, corridor_now)

        # parking_lot_analytics: cumulative line-crossing totals (max across
        # lines, matching the frame-migration derivation) + parking dwell stats.
        # parking_lot_analytics's line_a/line_b entries are the SAME shared
        # corridor accumulator duplicated under both line names (see
        # parking_lot_analytics.py::_update_line_counts's "Expose the single
        # combined corridor count under both line names" comment) — summing
        # both would double-count every crossing, so read exactly one entry.
        line_counts = tracking.get("line_counts")
        if isinstance(line_counts, dict) and line_counts:
            line_entry = line_counts.get("line_a") or next(
                (line for line in line_counts.values() if isinstance(line, dict)), None
            )
            if isinstance(line_entry, dict):
                self.window_park_entry_sum += int(line_entry.get("new_in", 0) or 0)
                self.window_park_exit_sum += int(line_entry.get("new_out", 0) or 0)

        parking = tracking.get("parking_analytics")
        if isinstance(parking, dict):
            try:
                self.last_avg_parking_time = float(parking.get("average_dwell_time_seconds", 0.0) or 0.0)
            except (TypeError, ValueError):
                self.last_avg_parking_time = 0.0
            try:
                frame_max_parked = float(parking.get("max_parked_time_seconds", 0.0) or 0.0)
            except (TypeError, ValueError):
                frame_max_parked = 0.0
            self.window_max_parked_seconds = max(self.window_max_parked_seconds, frame_max_parked)
            try:
                self.window_newly_parked_sum += int(parking.get("newly_parked_total", 0) or 0)
            except (TypeError, ValueError):
                pass
            newly_parked_by_category = parking.get("newly_parked_by_category")
            if isinstance(newly_parked_by_category, dict):
                for cat, count in newly_parked_by_category.items():
                    bucket = _PARKING_CLASS_TO_BUCKET.get(str(cat).lower())
                    if bucket is None:
                        continue
                    try:
                        count_int = int(count or 0)
                    except (TypeError, ValueError):
                        continue
                    self.window_newly_parked_by_category[bucket] = (
                        self.window_newly_parked_by_category.get(bucket, 0) + count_int
                    )

        # dwell_detection: latest snapshot of the five dwell/engagement metrics.
        dwell = tracking.get("dwell_analytics")
        if isinstance(dwell, dict):

            def _as_int(key: str) -> int:
                try:
                    return int(dwell.get(key, 0) or 0)
                except (TypeError, ValueError):
                    return 0

            def _as_float(key: str) -> float:
                try:
                    return float(dwell.get(key, 0.0) or 0.0)
                except (TypeError, ValueError):
                    return 0.0

            self.last_visitors_in_zone = _as_int("visitors_in_zone")
            self.last_active_dwellers = _as_int("active_dwellers")
            self.last_unique_dwellers = _as_int("unique_dwellers")
            self.last_avg_dwell_seconds = _as_float("avg_dwell_time_seconds")
            self.last_max_dwell_seconds = _as_float("max_dwell_time_seconds")
            # Windowed mean of the per-frame dweller share (dwellers / visitors
            # in zone right now * 100) for the dwell_percentage VOLUME metric —
            # same pattern as loitering_percentage / hazard_entry_percentage.
            visitors_now = self.last_visitors_in_zone
            if visitors_now > 0:
                self.window_dwell_pct_sum += (self.last_active_dwellers / visitors_now) * 100.0
                self.window_dwell_pct_frames += 1

        if profile.application_key_name == "ppe_compliance":
            self._ingest_ppe_safety(tracking)
        if profile.application_key_name == "car_damage_detection":
            self._ingest_car_damage_quality(tracking)
        # Pipe inspection family — one hook, per-app side-channel block name.
        _pipe_block = _PIPE_DEFECT_BLOCKS.get(profile.application_key_name)
        if _pipe_block:
            self._ingest_pipe_defect_analytics(tracking, _pipe_block)
        # Industrial inspection family — one hook, one shared block name.
        if profile.application_key_name in _INSPECTION_QUALITY_APPS:
            self._ingest_inspection_quality(tracking)
        if profile.application_key_name == "assembly_line_detection":
            self._ingest_assembly_volume(tracking)
        if profile.application_key_name == "illegal_parking_detection":
            self._ingest_illegal_parking(tracking)
        # hazard_zone_entry: latest snapshot + windowed mean of the entry share.
        hazard = tracking.get("hazard_analytics")
        if isinstance(hazard, dict):
            self.last_hazard_analytics = dict(hazard)
            if self.hazard_window_start_entrants is None:
                try:
                    self.hazard_window_start_entrants = int(hazard.get("unique_zone_entrants", 0) or 0)
                except (TypeError, ValueError):
                    self.hazard_window_start_entrants = 0
            try:
                self.window_hazard_pct_sum += float(hazard.get("hazard_entry_percentage", 0.0) or 0.0)
                self.window_hazard_pct_frames += 1
            except (TypeError, ValueError):
                pass

        # intrusion_detection: latest snapshot + windowed mean of the intrusion share.
        intrusion = tracking.get("intrusion_analytics")
        if isinstance(intrusion, dict):
            self.last_intrusion_analytics = dict(intrusion)
            if self.intrusion_window_start_intruders is None:
                try:
                    self.intrusion_window_start_intruders = int(intrusion.get("unique_intruders", 0) or 0)
                except (TypeError, ValueError):
                    self.intrusion_window_start_intruders = 0
            try:
                self.window_intrusion_pct_sum += float(intrusion.get("intrusion_percentage", 0.0) or 0.0)
                self.window_intrusion_pct_frames += 1
            except (TypeError, ValueError):
                pass

        # advanced_customer_service: counter-model snapshot + windowed means.
        self._ingest_customer_service_volume(tracking)

        # loitering_detection: avg/max_loiter_time_seconds latest snapshot.
        loitering = tracking.get("loitering_analytics")
        if isinstance(loitering, dict):
            self.last_loitering_analytics = dict(loitering)

        # tailgating_detection: latest snapshot + windowed sum of events and
        # windowed mean of the tailgating share.
        tailgating = tracking.get("tailgating_analytics")
        if isinstance(tailgating, dict):
            self.last_tailgating_analytics = dict(tailgating)
            try:
                self.window_tailgating_events_sum += int(tailgating.get("tailgating_events", 0) or 0)
            except (TypeError, ValueError):
                pass
            try:
                self.window_tailgating_pct_sum += float(tailgating.get("tailgating_percentage", 0.0) or 0.0)
                self.window_tailgating_pct_frames += 1
            except (TypeError, ValueError):
                pass

        # overcrowding_detection: latest snapshot + windowed peak / mean of the
        # per-frame occupancy and mean of the occupancy percentage.
        overcrowding = tracking.get("overcrowding_analytics")
        if isinstance(overcrowding, dict):
            self.last_overcrowding_analytics = dict(overcrowding)
            try:
                occ_now = int(overcrowding.get("current_occupancy", 0) or 0)
            except (TypeError, ValueError):
                occ_now = 0
            self.window_occupancy_peak = max(self.window_occupancy_peak, occ_now)
            self.window_occupancy_sum += occ_now
            self.window_occupancy_frames += 1
            try:
                self.window_occupancy_pct_sum += float(overcrowding.get("occupancy_percentage", 0.0) or 0.0)
                self.window_occupancy_pct_frames += 1
            except (TypeError, ValueError):
                pass

        # abandoned_object_detection: tracking_stats["active_track_count"] is a
        # flat int, not a nested analytics block, so it is read straight off the
        # frame. Latest-frame snapshot (matching the profile's rollup_mode); no
        # window accumulator, since "objects currently being tracked" is a
        # point-in-time reading rather than something to sum.
        if profile.application_key_name == "abandoned_object_detection":
            try:
                self.last_abandoned_active_tracks = int(tracking.get("active_track_count", 0) or 0)
            except (TypeError, ValueError):
                self.last_abandoned_active_tracks = 0

        # Accumulate unique track_ids across the window from detections list.
        # Only runs for dwell profile — detections carry track_id + category.
        if profile.application_key_name == "dwell":
            for det in tracking.get("detections", []):
                if not isinstance(det, dict):
                    continue
                track_id = det.get("track_id")
                if not track_id:
                    continue
                category = det.get("category", "")
                if category in ("person", "Dweller"):
                    self.window_visitor_ids.add(track_id)
                if category == "Dweller":
                    self.window_dweller_ids.add(track_id)

        # flood_detection: snapshot of flood_analytics block.
        flood = tracking.get("flood_analytics")
        if isinstance(flood, dict):
            try:
                self.last_flood_detection_count = int(flood.get("flood_detection_count", 0) or 0)
            except (TypeError, ValueError):
                self.last_flood_detection_count = 0
            try:
                frame_pct = float(flood.get("max_flood_area_pct", 0.0) or 0.0)
            except (TypeError, ValueError):
                frame_pct = 0.0
            self.last_max_flood_area_pct = frame_pct
            # avg_flood_area_percentage: windowed mean over every frame
            # (including 0%-coverage frames when no flood is present).
            self.window_flood_pct_sum += frame_pct
            self.window_flood_pct_frames += 1
            try:
                self.last_total_flood_area_pct = float(flood.get("total_flood_area_pct", 0.0) or 0.0)
            except (TypeError, ValueError):
                self.last_total_flood_area_pct = 0.0
            # floods_occurred is resolved directly from window_new_sum["flood"]
            # (see the generic current_new_counts accumulation above) — no
            # extra bookkeeping needed here.

        # landslide_detection: snapshot of landslide_analytics block.
        landslide = tracking.get("landslide_analytics")
        if isinstance(landslide, dict):
            try:
                self.last_landslide_detection_count = int(landslide.get("landslide_detection_count", 0) or 0)
            except (TypeError, ValueError):
                self.last_landslide_detection_count = 0
            try:
                frame_pct = float(landslide.get("max_landslide_area_pct", 0.0) or 0.0)
            except (TypeError, ValueError):
                frame_pct = 0.0
            self.last_max_landslide_area_pct = frame_pct
            # avg_surface_displacement_percentage: windowed mean over every frame.
            self.window_landslide_pct_sum += frame_pct
            self.window_landslide_pct_frames += 1
            try:
                self.last_total_landslide_area_pct = float(landslide.get("total_landslide_area_pct", 0.0) or 0.0)
            except (TypeError, ValueError):
                self.last_total_landslide_area_pct = 0.0
            # landslides_occurred is resolved directly from
            # window_new_sum["landslide"] — no extra bookkeeping needed here.

        # vehicle_monitoring_wrong_way: side-channel snapshot, not a
        # current_counts category — read directly (mirrors hazard/intrusion/
        # tailgating/overcrowding side-channel handling above).
        wrong_way = tracking.get("wrong_way_analytics")
        if isinstance(wrong_way, dict):
            self.last_wrong_way_analytics = dict(wrong_way)

        # stopped_vehicle_monitoring: confirmed stopped-vehicle snapshot lives on
        # tracking_stats["stopped_vehicle_count"]; the monotonic session total is
        # the sibling stopped_vehicle_analytics["total_events"] block.
        if profile.application_key_name == "stopped_vehicle_monitoring":
            try:
                self.last_stopped_vehicle_count = int(tracking.get("stopped_vehicle_count", 0) or 0)
            except (TypeError, ValueError):
                self.last_stopped_vehicle_count = 0
            self.window_stopped_peak = max(self.window_stopped_peak, self.last_stopped_vehicle_count)
            sva = frame_data.get("stopped_vehicle_analytics")
            if isinstance(sva, dict):
                try:
                    self.last_stopped_total_events = int(sva.get("total_events", 0) or 0)
                except (TypeError, ValueError):
                    self.last_stopped_total_events = 0

        primary = profile.primary_category.lower()
        if profile.occupancy_mode == "max_weapon_person":
            self.window_weapon_max = max(self.window_weapon_max, self.latest_current.get("weapon", 0))
            self.window_person_max = max(self.window_person_max, self.latest_current.get("person", 0))
            self.last_occupancy = self.window_weapon_max + self.window_person_max
        else:
            self.last_occupancy = self.latest_current.get(primary, 0)
            if self.last_occupancy == 0 and self.latest_current:
                self.last_occupancy = sum(self.latest_current.values())

        self.window_peak_occupancy = max(self.window_peak_occupancy, self.last_occupancy)

        # area_utilization: mean occupancy and duty cycle (share of frames with
        # anyone present), both from the generic last_occupancy above -- this
        # app has no side-channel block to read a peer figure from.
        if profile.application_key_name == "area_utilization":
            self.area_util_window_occupancy_sum += self.last_occupancy
            self.area_util_window_occupancy_frames += 1
            if self.last_occupancy > 0:
                self.area_util_window_occupied_frames += 1

    def _ingest_customer_service_volume(self, tracking: Mapping[str, Any]) -> None:
        """Snapshot advanced_customer_service's per-frame side channel.

        The block is emitted on every frame including idle ones, which is what
        makes the windowed means below unbiased -- an app that only emitted it when
        busy would report the mean of its busy frames.
        """
        block = tracking.get("customer_service_analytics")
        if not isinstance(block, dict):
            return
        self.last_customer_service_analytics = dict(block)

        def _int(key: str) -> int:
            try:
                return int(block.get(key, 0) or 0)
            except (TypeError, ValueError):
                return 0

        def _float(key: str) -> float:
            try:
                return float(block.get(key, 0.0) or 0.0)
            except (TypeError, ValueError):
                return 0.0

        # First frame of the session only -- every later window gets its baseline
        # from _reset_window, seeded off the closing window's final reading.
        if self.cs_window_start_customers is None:
            self.cs_window_start_customers = _int("unique_customers")
        if self.cs_window_start_served is None:
            self.cs_window_start_served = _int("total_customers_served")
        if self.cs_window_start_abandoned is None:
            self.cs_window_start_abandoned = _int("total_abandoned")

        self.window_counter_util_sum += _float("counter_utilization")
        self.window_counter_util_frames += 1
        self.window_staff_cov_sum += _float("staff_coverage")
        self.window_staff_cov_frames += 1
        self.window_queue_len_sum += _int("total_queue_length")
        self.window_queue_len_frames += 1
        self.window_cs_max_queue = max(self.window_cs_max_queue, _int("max_queue_length"))
        self.window_cs_ratio_sum += _float("customer_to_staff_ratio")
        self.window_cs_ratio_frames += 1
        # The block's own abandonment_rate is deliberately NOT accumulated: it is
        # an all-time ratio, and the resolver recomputes a per-window one from the
        # served/abandoned deltas instead.

    def _ingest_ppe_safety(self, tracking: Mapping[str, Any]) -> None:
        """Accumulate SAFETY window state from ``safety_analytics`` block."""
        safety = tracking.get("safety_analytics")
        if not isinstance(safety, dict):
            return

        try:
            pct = float(safety.get("compliance_pct", 0.0) or 0.0)
        except (TypeError, ValueError):
            pct = 0.0
        self.window_compliance_pct_sum += pct
        self.window_compliance_pct_frames += 1

        for key, target in (
            ("frame_person_ids", self.window_person_ids),
            ("frame_violator_ids", self.window_violator_ids),
            ("frame_hardhat_ids", self.window_hardhat_ids),
            ("frame_safety_vest_ids", self.window_safety_vest_ids),
            ("frame_mask_ids", self.window_mask_ids),
        ):
            ids = safety.get(key)
            if isinstance(ids, list):
                target.update(ids)

    def _ingest_pipe_defect_analytics(self, tracking: Mapping[str, Any], block_name: str) -> None:
        """Accumulate window state for the pipe inspection family.

        ``block_name`` is the use case's side-channel key —
        ``corrosion_analytics`` / ``gas_analytics`` / ``liquid_analytics``. The
        three blocks share one field contract so a single hook serves all of them.

        Called on EVERY frame, including idle ones: ``pipe_window_total_frames``
        is the presence denominator, so skipping idle frames would make
        ``*_presence`` read 100% for any intermittent defect.
        """
        block = tracking.get(block_name)
        if not isinstance(block, dict):
            return

        try:
            current = int(block.get("current_count", 0) or 0)
        except (TypeError, ValueError):
            current = 0
        self.pipe_last_current = current
        self.pipe_window_peak = max(self.pipe_window_peak, current)

        try:
            self.pipe_last_total_unique = int(block.get("total_unique_count", 0) or 0)
        except (TypeError, ValueError):
            pass

        # Deduplicated new-region count: union of per-frame first-seen track IDs.
        new_ids = block.get("frame_new_ids")
        if isinstance(new_ids, list):
            self.pipe_window_new_ids.update(new_ids)

        # Presence denominator + active-time numerator for THIS window.
        # is_active is authoritative when present; fall back to current > 0 so an
        # older use-case build that omits the flag still reports presence.
        raw_active = block.get("is_active")
        is_active = bool(raw_active) if raw_active is not None else current > 0
        self.pipe_window_total_frames += 1
        if is_active:
            self.pipe_window_active_frames += 1
            try:
                self.pipe_window_active_seconds += float(block.get("frame_seconds", 0.0) or 0.0)
            except (TypeError, ValueError):
                pass

        try:
            streak = float(block.get("max_continuous_seconds", 0.0) or 0.0)
            self.pipe_max_continuous_seconds = max(self.pipe_max_continuous_seconds, streak)
        except (TypeError, ValueError):
            pass

    def _ingest_car_damage_quality(self, tracking: Mapping[str, Any]) -> None:
        """Accumulate QUALITY window state from ``quality_analytics`` block."""
        quality = tracking.get("quality_analytics")
        if not isinstance(quality, dict):
            return

        self.last_quality_analytics = dict(quality)

        try:
            frame_defect = int(quality.get("defect_count", 0) or 0)
        except (TypeError, ValueError):
            frame_defect = 0
        try:
            frame_inspected = int(quality.get("total_inspected", 0) or 0)
        except (TypeError, ValueError):
            frame_inspected = 0

        self.window_peak_defect = max(self.window_peak_defect, frame_defect)
        self.window_peak_inspected = max(self.window_peak_inspected, frame_inspected)

        defect_ids = quality.get("frame_defect_ids")
        if isinstance(defect_ids, list):
            self.window_defect_ids.update(defect_ids)
        inspected_ids = quality.get("frame_inspected_ids")
        if isinstance(inspected_ids, list):
            self.window_inspected_ids.update(inspected_ids)

    def _ingest_inspection_quality(self, tracking: Mapping[str, Any]) -> None:
        """Accumulate QUALITY window state for the industrial inspection family.

        Reads the superset ``tracking_stats["quality_analytics"]`` block written
        every frame by bottle / pcb / phone-screen / solar. One hook serves all
        four because they share one field contract.

        Called on EVERY frame, including idle ones: ``insp_window_total_frames``
        is the presence denominator, so skipping idle frames would make
        ``defect_presence`` read 100% for any intermittent defect.

        The defect/inspected unions and peak fallbacks reuse the car-damage
        accumulators (identical semantics); only the presence counters, the
        cumulative total and the first-seen union are inspection-specific.
        """
        quality = tracking.get("quality_analytics")
        if not isinstance(quality, dict):
            return

        self.last_quality_analytics = dict(quality)

        def _as_int(name: str) -> int:
            try:
                return int(quality.get(name, 0) or 0)
            except (TypeError, ValueError):
                return 0

        def _as_float(name: str) -> float:
            try:
                return float(quality.get(name, 0.0) or 0.0)
            except (TypeError, ValueError):
                return 0.0

        frame_defect = _as_int("defect_count")

        # Peak fallbacks for when the tracker never confirms an ID (very
        # short-lived or untracked detections): without these the unique-ID sets
        # stay empty and the metric publishes 0 even though defects were clearly
        # detected.
        self.window_peak_defect = max(self.window_peak_defect, frame_defect)
        self.window_peak_inspected = max(self.window_peak_inspected, _as_int("total_inspected"))

        # Cumulative unique defect tracks since session start. Plain assignment
        # (not max): the use case sources this from its own monotonic track-ID
        # set, and a max() would pin the value permanently if the use case reset.
        self.insp_last_total_unique = _as_int("total_unique_count")

        for src, dst in (
            ("frame_defect_ids", self.window_defect_ids),
            ("frame_inspected_ids", self.window_inspected_ids),
            ("frame_new_ids", self.insp_window_new_defect_ids),
        ):
            ids = quality.get(src)
            if isinstance(ids, list):
                dst.update(ids)

        # is_active is authoritative when present; fall back to the per-frame
        # defect count so an older use-case build still reports presence.
        raw_active = quality.get("is_active")
        is_active = bool(raw_active) if raw_active is not None else frame_defect > 0
        self.insp_window_total_frames += 1
        if is_active:
            self.insp_window_active_frames += 1

        self.insp_max_continuous_seconds = max(self.insp_max_continuous_seconds, _as_float("max_continuous_seconds"))

    def _ingest_assembly_volume(self, tracking: Mapping[str, Any]) -> None:
        """Accumulate VOLUME window state from ``assembly_analytics``.

        The throughput pair arrives as first-seen track-ID LISTS, not counts, so
        the union below counts one physical carrier exactly once per window
        however many frames it stays in view. Summing per-frame counts instead
        would multiply every plate by its dwell time.
        """
        block = tracking.get("assembly_analytics")
        if not isinstance(block, dict):
            return

        for src, dst in (
            ("frame_new_loaded_ids", self.asm_window_new_loaded_ids),
            ("frame_new_empty_ids", self.asm_window_new_empty_ids),
        ):
            ids = block.get(src)
            if isinstance(ids, list):
                dst.update(ids)

        try:
            arms = int(block.get("current_robot_arms", 0) or 0)
            self.asm_window_peak_robot_arms = max(self.asm_window_peak_robot_arms, arms)
        except (TypeError, ValueError):
            pass

        try:
            self.asm_last_current_total = int(block.get("current_total_count", 0) or 0)
        except (TypeError, ValueError):
            pass

    def _ingest_illegal_parking(self, tracking: Mapping[str, Any]) -> None:
        """Accumulate VOLUME window state from ``illegal_parking_analytics`` block."""
        ipa = tracking.get("illegal_parking_analytics")
        if not isinstance(ipa, dict):
            return

        vehicle_ids = ipa.get("frame_vehicle_ids")
        if isinstance(vehicle_ids, list):
            self.window_tracked_vehicle_ids.update(vehicle_ids)
        violation_ids = ipa.get("frame_violation_ids")
        if isinstance(violation_ids, list):
            self.window_violation_ids.update(violation_ids)

        try:
            self.window_peak_tracked = max(self.window_peak_tracked, int(ipa.get("total_vehicles_tracked", 0) or 0))
        except (TypeError, ValueError):
            pass
        try:
            self.window_peak_violations = max(
                self.window_peak_violations, int(ipa.get("total_violation_events", 0) or 0)
            )
        except (TypeError, ValueError):
            pass

        dwell_values = ipa.get("frame_confirmed_dwell_seconds")
        if isinstance(dwell_values, list):
            for value in dwell_values:
                try:
                    self.window_dwell_sum += float(value)
                except (TypeError, ValueError):
                    continue
                self.window_dwell_count += 1

    def _resolve_metric_value(self, key: str, profile: LegacyAnalyticsProfile) -> float:
        # New VOLUME+INCIDENT apps are resolved first, gated by profile, so their
        # keys (e.g. "current_occupancy") never collide with the generic keys
        # handled further down. A given session only ever has one profile.
        app = profile.application_key_name
        if app == "hazard_zone_entry":
            h = self.last_hazard_analytics
            if key == "people_in_frame":
                # NEW people this interval — growth in cumulative person track IDs
                # over the 60s window (agg_type sum). Every entrant first appears
                # as "person" (at_risk is a relabel of the same track), so the
                # person delta counts distinct new people without double counting.
                return float(max(0, self.latest_totals.get("person", 0) - self.window_start_totals.get("person", 0)))
            if key == "people_at_risk":
                # NEW at-risk this interval — growth in cumulative unique zone
                # entrants over the window (agg_type sum). unique_zone_entrants is
                # monotonic, so end − window-start = entrants confirmed this window.
                # No hazard frame landed this window (start still None) -> no
                # growth, not "everyone ever seen is new": fall back to the
                # current cumulative value so the delta comes out 0 instead of
                # fabricating the whole session's count now that last_hazard_analytics
                # carries forward across idle windows.
                current = int(h.get("unique_zone_entrants", 0) or 0)
                start = self.hazard_window_start_entrants if self.hazard_window_start_entrants is not None else current
                return float(max(0, current - start))
            if key == "active_people_at_risk":
                # Instantaneous count of people confirmed in the hazard zone now
                # (last-frame snapshot).
                return float(h.get("people_at_risk", 0) or 0)
            if key == "unique_zone_entrants":
                # Cumulative unique entrants since session start (last).
                return float(h.get("unique_zone_entrants", 0) or 0)
            if key == "hazard_entry_percentage":
                if self.window_hazard_pct_frames > 0:
                    return round(self.window_hazard_pct_sum / self.window_hazard_pct_frames, 2)
                return 0.0
            if key == "avg_time_in_zone_seconds":
                return round(float(h.get("avg_time_in_zone_seconds", 0.0) or 0.0), 2)
            if key == "max_time_in_zone_seconds":
                return round(float(h.get("max_time_in_zone_seconds", 0.0) or 0.0), 2)
            return 0.0
        if app == "advanced_customer_service":
            c = self.last_customer_service_analytics

            def _snap_int(key: str) -> float:
                try:
                    return float(int(c.get(key, 0) or 0))
                except (TypeError, ValueError):
                    return 0.0

            def _snap_float(key: str) -> float:
                try:
                    return round(float(c.get(key, 0.0) or 0.0), 2)
                except (TypeError, ValueError):
                    return 0.0

            def _delta(key: str, baseline: Optional[int]) -> float:
                """Growth in a monotonic cumulative counter over this window.

                Falls back to the current value as the baseline when no frame
                landed this window, so the delta comes out 0 rather than
                fabricating the whole session's total -- the same idle-window
                guard hazard_zone_entry and intrusion_detection use.
                """
                try:
                    current = int(c.get(key, 0) or 0)
                except (TypeError, ValueError):
                    current = 0
                start = baseline if baseline is not None else current
                return float(max(0, current - start))

            # presence / occupancy snapshots. people_in_frame is resolvable but
            # NOT in the profile -- see the note there; keeping the branch means
            # re-adding the metric is a one-line profile change.
            if key in (
                "people_in_frame",
                "customers_at_counters",
                "staff_on_counters",
                "total_counters",
                "active_counters",
                "staffed_counters",
                "serving_counters",
                "total_queue_length",
                "unique_customers",
                "total_customers_served",
            ):
                return _snap_int(key)
            if key in ("avg_wait_seconds", "max_wait_seconds", "avg_service_seconds", "max_service_seconds"):
                return _snap_float(key)

            # windowed means
            if key == "counter_utilization":
                if self.window_counter_util_frames > 0:
                    return round(self.window_counter_util_sum / self.window_counter_util_frames, 2)
                return 0.0
            if key == "staff_coverage":
                if self.window_staff_cov_frames > 0:
                    return round(self.window_staff_cov_sum / self.window_staff_cov_frames, 2)
                return 0.0
            if key == "avg_queue_length":
                if self.window_queue_len_frames > 0:
                    return round(self.window_queue_len_sum / self.window_queue_len_frames, 2)
                return 0.0
            if key == "customer_to_staff_ratio":
                if self.window_cs_ratio_frames > 0:
                    return round(self.window_cs_ratio_sum / self.window_cs_ratio_frames, 2)
                return 0.0

            # window max
            if key == "max_queue_length":
                return float(self.window_cs_max_queue)

            # per-window deltas of monotonic counters
            if key == "customers_in_interval":
                return _delta("unique_customers", self.cs_window_start_customers)
            if key == "customers_served_in_interval":
                return _delta("total_customers_served", self.cs_window_start_served)
            if key == "abandoned_in_interval":
                return _delta("total_abandoned", self.cs_window_start_abandoned)

            if key == "abandonment_rate":
                # Recomputed from THIS window's deltas rather than averaged from
                # the use case's own abandonment_rate field, which is an all-time
                # ratio over every customer since the session opened. An all-time
                # ratio converges: by hour three a bad ten minutes barely moves it,
                # so the trend chart flattens into a straight line and the operator
                # cannot see the bad ten minutes at all. Same reason the pipe
                # defect family computes presence per window here instead of
                # reading the use case's cumulative presence_ratio.
                served = _delta("total_customers_served", self.cs_window_start_served)
                abandoned = _delta("total_abandoned", self.cs_window_start_abandoned)
                resolved = served + abandoned
                if resolved <= 0:
                    # Nobody finished either way this window. 0 is the honest
                    # reading: carrying the previous window's rate forward would
                    # invent abandonment during a window with no customers.
                    return 0.0
                return round(abandoned / resolved * 100.0, 2)

            if key == "staff_productivity":
                # Services completed this window per staff member on the counters.
                served = _delta("total_customers_served", self.cs_window_start_served)
                staff_now = max(1.0, _snap_int("staff_on_counters"))
                return round(served / staff_now, 2)
            return 0.0
        if app == "intrusion_detection":
            i = self.last_intrusion_analytics
            if key == "people_in_frame":
                return float(i.get("people_in_frame", 0) or 0)
            if key == "active_intruders":
                return float(i.get("active_intruders", 0) or 0)
            if key == "unique_intruders":
                return float(i.get("unique_intruders", 0) or 0)
            if key == "intruders_in_interval":
                # NEW confirmed intruders this window — growth in cumulative
                # unique_intruders over the window (agg_type sum), mirroring
                # hazard_zone_entry's people_at_risk delta pattern, including the
                # idle-window fallback: no intrusion frame landed this window
                # (start still None) -> delta 0, not the whole session's count.
                current = int(i.get("unique_intruders", 0) or 0)
                start = (
                    self.intrusion_window_start_intruders
                    if self.intrusion_window_start_intruders is not None
                    else current
                )
                return float(max(0, current - start))
            if key == "intrusion_percentage":
                if self.window_intrusion_pct_frames > 0:
                    return round(self.window_intrusion_pct_sum / self.window_intrusion_pct_frames, 2)
                return 0.0
            if key == "avg_intrusion_time_seconds":
                return round(float(i.get("avg_intrusion_time_seconds", 0.0) or 0.0), 2)
            if key == "max_intrusion_time_seconds":
                return round(float(i.get("max_intrusion_time_seconds", 0.0) or 0.0), 2)
            return 0.0
        if app == "tailgating_detection":
            t = self.last_tailgating_analytics
            if key == "people_in_frame":
                return float(t.get("people_in_frame", 0) or 0)
            if key == "active_tailgaters":
                return float(t.get("active_tailgaters", 0) or 0)
            if key == "tailgating_events":
                return float(self.window_tailgating_events_sum)
            if key == "interval_tailgaters":
                # NEW confirmed tailgaters this window (agg_type sum) -- same
                # accumulator as tailgating_events, the pre-rename key name.
                return float(self.window_tailgating_events_sum)
            if key == "unique_tailgaters":
                return float(t.get("unique_tailgaters", 0) or 0)
            if key == "tailgating_percentage":
                if self.window_tailgating_pct_frames > 0:
                    return round(self.window_tailgating_pct_sum / self.window_tailgating_pct_frames, 2)
                return 0.0
            return 0.0
        if app == "overcrowding_detection":
            o = self.last_overcrowding_analytics
            if key == "live_occupancy":
                # Instantaneous headcount (last-frame snapshot), distinct from
                # current_occupancy below, which is this window's THROUGHPUT.
                return float(self.last_occupancy)
            if key == "current_occupancy":
                return float(o.get("current_occupancy", 0) or 0)
            if key == "peak_occupancy":
                return float(self.window_occupancy_peak)
            if key == "avg_occupancy":
                if self.window_occupancy_frames > 0:
                    return round(self.window_occupancy_sum / self.window_occupancy_frames, 2)
                return 0.0
            if key == "occupancy_percentage":
                if self.window_occupancy_pct_frames > 0:
                    return round(self.window_occupancy_pct_sum / self.window_occupancy_pct_frames, 2)
                return 0.0
            if key == "unique_visitors":
                return float(o.get("unique_visitors", 0) or 0)
            return 0.0
        if app == "area_utilization":
            # No side-channel analytics block for this app (unlike its sibling
            # overcrowding_detection), so every reading comes from the generic
            # per-frame occupancy state in ingest_agg_summary.
            if key == "live_occupancy":
                return float(self.last_occupancy)
            if key == "current_occupancy":
                # NEW people this window (throughput), not the concurrent
                # headcount -- same "misleadingly named" key as overcrowding's.
                return float(self.window_new_sum.get("person", 0))
            if key == "peak_occupancy":
                return float(self.window_peak_occupancy)
            if key == "avg_occupancy":
                if self.area_util_window_occupancy_frames > 0:
                    return round(self.area_util_window_occupancy_sum / self.area_util_window_occupancy_frames, 2)
                return 0.0
            if key == "occupancy_percentage":
                # Capacity is the literal 10 baked into this app version's
                # app.yaml derived expr (zone_occupancy.occupancy / 10 * 100).
                return round(float(self.last_occupancy) / 10.0 * 100.0, 2)
            if key == "time_occupied_percent":
                # Duty cycle: share of this window's frames with anyone present.
                if self.area_util_window_occupancy_frames > 0:
                    return round(
                        (self.area_util_window_occupied_frames / self.area_util_window_occupancy_frames) * 100.0,
                        2,
                    )
                return 0.0
            if key == "unique_visitors":
                return float(self.latest_totals.get("person", 0) or 0)
            return 0.0
        if app == "flood_detection":
            if key == "avg_flood_area_percentage":
                if self.window_flood_pct_frames > 0:
                    return round(self.window_flood_pct_sum / self.window_flood_pct_frames, 4)
                return 0.0
            # floods_occurred: sum of current_new_counts["flood"] across the
            # 60s window (flood_detection.py already runs SORT/ByteTrack, so
            # this is new flood track IDs this window — same window_new_sum
            # pipeline as footfall's entry / accident's accidents_over_time).
            if key == "floods_occurred":
                return float(self.window_new_sum.get("flood", 0))
            return 0.0
        if app == "landslide_detection":
            if key == "avg_surface_displacement_percentage":
                if self.window_landslide_pct_frames > 0:
                    return round(self.window_landslide_pct_sum / self.window_landslide_pct_frames, 4)
                return 0.0
            # landslides_occurred: sum of current_new_counts["landslide"] across
            # the window, same generic window_new_sum pipeline as flood above.
            if key == "landslides_occurred":
                return float(self.window_new_sum.get("landslide", 0))
            return 0.0
        if app == "accident_detection":
            # accidents_over_time: unique confirmed-accident episodes this 60s
            # window (sum) — current_new_counts["accident"] fires exactly once
            # per debounced episode (see accident_detection.py), accumulated
            # generically into window_new_sum by ingest_agg_summary.
            if key == "accidents_over_time":
                return float(self.window_new_sum.get("accident", 0))
            # critical_accidents: of those, how many carried severity_level ==
            # "critical" this window (sum) — accumulated in ingest_agg_summary
            # from the incidents block (severity isn't part of tracking_stats).
            # Every accident is currently always "critical" (see
            # accident_detection.py's _generate_incidents), so today this
            # equals accidents_over_time — reading the actual severity here
            # rather than assuming it keeps this correct if a lower-severity
            # tier is ever added.
            if key == "critical_accidents":
                return float(self.window_critical_accidents)
            return 0.0
        if app == "people_counting":
            if key == "occupancy_in_interval":
                # Sum of current_new_counts["person"] across every frame in the 60s window.
                return float(self.window_new_sum.get("person", 0))
            if key == "total_occupancy":
                # Latest cumulative total_counts["person"] — no window delta or reset.
                return float(self.latest_totals.get("person", 0))
            if key == "occupancy_percentage":
                return round(min(float(self.last_occupancy) / 50.0 * 100.0, 100.0), 2)
            return 0.0
        if app == "footfall":
            # entry / exit: NEW "in"/"out" line-crossings summed over the 60s
            # window (agg_type "sum"), from window_new_sum (accumulated in
            # ingest_agg_summary from tracking_stats["current_new_counts"]).
            if key == "entry":
                return float(self.window_new_sum.get("in", 0))
            if key == "exit":
                return float(self.window_new_sum.get("out", 0))
            if key == "entrance_congestion":
                # Peak concurrent occupancy of the two-line corridor this
                # window (in+out combined), agg_type "max" -- NOT
                # entry+exit throughput (footfall-v1.5's 1st, rejected
                # definition: a smoothly-flowing high-traffic entrance read
                # as "congested" while a genuinely bottlenecked, low-
                # throughput one read as "quiet"). window_corridor_occupancy_peak
                # is cleared every window in _reset_window.
                return float(self.window_corridor_occupancy_peak)
            return 0.0
        if app == "pedestrian_detection":
            # occupancy_in_interval / total_occupancy: same formula shape as
            # people_counting's own pair (pedestrian_detection-v1.4 matches it
            # explicitly). default_tracking_categories is ("Pedestrian",) --
            # the wire-visible relabel -- but window_new_sum/latest_totals key
            # off the lowercased category from _count_list_to_map, hence the
            # lowercase lookup here.
            if key == "occupancy_in_interval":
                return float(self.window_new_sum.get("pedestrian", 0))
            if key == "total_occupancy":
                return float(self.latest_totals.get("pedestrian", 0))
            return 0.0
        if app in _PIPE_DEFECT_BLOCKS:
            # Pipe inspection family (corrosion / gas leak / liquid leak). All keys
            # resolve from the shared pipe_* window state populated by
            # _ingest_pipe_defect_analytics; _PIPE_METRIC_ROLES maps each app's
            # domain-named key to its semantic role.
            role = _PIPE_METRIC_ROLES.get(key)
            if role == "current":
                return float(self.pipe_last_current)
            if role == "new":
                # Deduplicated: one physical region counts once per window no
                # matter how many frames it spans.
                return float(len(self.pipe_window_new_ids))
            if role == "total":
                return float(self.pipe_last_total_unique)
            if role == "peak":
                return float(self.pipe_window_peak)
            if role == "presence":
                # 0–100 over THIS window, not the session — matches unit
                # "percent" in the *-analytics-metrics.json files.
                if self.pipe_window_total_frames > 0:
                    return round(
                        (self.pipe_window_active_frames / self.pipe_window_total_frames) * 100.0,
                        2,
                    )
                return 0.0
            if role == "duration":
                return round(self.pipe_window_active_seconds, 3)
            if role == "max_continuous":
                return round(self.pipe_max_continuous_seconds, 3)
            return 0.0
        if app in _INSPECTION_QUALITY_APPS:
            # Industrial inspection family (bottle / pcb / phone screen / solar).
            # Keys match app-migrations/quality/<app>/<app>-analytics-metrics.json.
            unique_defects = len(self.window_defect_ids)
            unique_inspected = len(self.window_inspected_ids)
            # Peak fallback: tracks may never confirm for very short-lived or
            # untracked detections, in which case the ID sets stay empty and the
            # raw per-frame peak is the honest floor.
            if unique_inspected == 0 and self.window_peak_inspected > 0:
                unique_inspected = self.window_peak_inspected
            if unique_defects == 0 and self.window_peak_defect > 0:
                unique_defects = self.window_peak_defect
            if key == "defect_count":
                # Deduplicated: one defective unit counts once per window no
                # matter how many frames it spans.
                return float(unique_defects)
            if key == "total_inspected":
                # Solar only -- the other three are defect-only models where this
                # would equal defect_count.
                return float(unique_inspected)
            if key == "defect_rate":
                # 0-100, NOT the 0-1 ratio car_damage_detection publishes: these
                # manifests declare `unit: percent`. Computed from the two
                # WINDOW-UNIQUE counts rather than as a mean of per-frame ratios,
                # which would weight a frame holding 1 panel the same as a frame
                # holding 20.
                if unique_inspected > 0:
                    return round((unique_defects / unique_inspected) * 100.0, 2)
                return 0.0
            if key == "total_defect_count":
                # Cumulative unique defect tracks since session start (agg last).
                return float(self.insp_last_total_unique)
            if key == "defect_presence":
                # 0-100 over THIS window, not the session.
                if self.insp_window_total_frames > 0:
                    return round(
                        (self.insp_window_active_frames / self.insp_window_total_frames) * 100.0,
                        2,
                    )
                return 0.0
            return 0.0
        if app == "assembly_line_detection":
            # Deduplicated per-window carrier throughput: one plate counts once
            # however many frames it stays in view.
            loaded = len(self.asm_window_new_loaded_ids)
            empty = len(self.asm_window_new_empty_ids)
            if key == "plate_throughput":
                return float(loaded)
            if key == "empty_plate_throughput":
                return float(empty)
            if key == "line_utilization":
                # Recomputed here from the two window-unique counts rather than
                # averaging the use case's per-frame ratio, which would weight a
                # frame holding one carrier the same as a frame holding six.
                # 0-100 to match `unit: percent`; 0.0 when no carriers were seen.
                carriers = loaded + empty
                if carriers > 0:
                    return round((loaded / carriers) * 100.0, 2)
                return 0.0
            if key == "active_robot_arms":
                return float(self.asm_window_peak_robot_arms)
            if key == "current_occupancy":
                # All mapped objects in the last ingested frame -- resolved from
                # the side-channel block, not last_occupancy, because occupancy
                # here spans every target class rather than primary_category only.
                return float(self.asm_last_current_total)
            if key == "entry_count":
                # Generic window accumulator: sum of positive current_new_counts
                # across all categories. Reads as overall line activity; trust
                # plate_throughput for production counting (see the yaml note on
                # static robot arms inflating this).
                return float(self.window_entry_total)
            return 0.0
        if app == "car_damage_detection":
            unique_defects = len(self.window_defect_ids)
            unique_inspected = len(self.window_inspected_ids)
            if unique_inspected == 0 and self.window_peak_inspected > 0:
                unique_inspected = self.window_peak_inspected
            if unique_defects == 0 and self.window_peak_defect > 0:
                unique_defects = self.window_peak_defect
            if key == "defect_count":
                return float(unique_defects)
            if key == "total_inspected":
                return float(unique_inspected)
            if key == "defect_rate":
                if unique_inspected > 0:
                    return round(unique_defects / unique_inspected, 6)
                return 0.0
            return 0.0
        if app == "illegal_parking_detection":
            unique_tracked = len(self.window_tracked_vehicle_ids)
            unique_violations = len(self.window_violation_ids)
            if unique_tracked == 0 and self.window_peak_tracked > 0:
                unique_tracked = self.window_peak_tracked
            if unique_violations == 0 and self.window_peak_violations > 0:
                unique_violations = self.window_peak_violations
            if key == "total_violations":
                return float(unique_violations)
            if key == "total_vehicles_tracked":
                return float(unique_tracked)
            if key == "violation_rate":
                if unique_tracked > 0:
                    return round(unique_violations / unique_tracked * 100.0, 2)
                return 0.0
            if key == "avg_dwell_time_sec":
                if self.window_dwell_count > 0:
                    return round(self.window_dwell_sum / self.window_dwell_count, 2)
                return 0.0
            return 0.0
        if app == "vehicle_monitoring_wrong_way":
            # current_wrong_way_count / current_suspect_count / total_wrong_way_events
            # are resolved from the side-channel snapshot populated in
            # ingest_agg_summary (tracking_stats["wrong_way_analytics"]), not
            # from latest_current — that dict is never a current_counts category.
            w = self.last_wrong_way_analytics
            if key == "current_wrong_way_count":
                return float(w.get("current_wrong_way_count", 0) or 0)
            if key == "current_suspect_count":
                return float(w.get("current_suspect_count", 0) or 0)
            if key == "total_wrong_way_events":
                return float(w.get("total_wrong_way_count", 0) or 0)
            if key == "vehicle_count":
                return float(sum(self.latest_current.values()))
            return 0.0
        if app == "stopped_vehicle_monitoring":
            # Resolved from the side-channel snapshot populated in
            # ingest_agg_summary (tracking_stats["stopped_vehicle_count"] and the
            # sibling stopped_vehicle_analytics["total_events"]), not from
            # latest_current — stopped counts are not a current_counts category.
            if key == "stopped_vehicle_count":
                return float(self.last_stopped_vehicle_count)
            if key == "peak_stopped_vehicle_count":
                return float(self.window_stopped_peak)
            if key == "total_stopped_events":
                return float(self.last_stopped_total_events)
            return 0.0
        if app == "running_detection":
            # "running" is this app's only tracked category, so current/peak/
            # entry-sum all resolve from the generic latest_current /
            # window_peak_occupancy / window_entry_total state already
            # maintained above (primary_category="running").
            if key == "current_running_count":
                return float(self.latest_current.get("running", 0))
            if key == "peak_running_count":
                return float(self.window_peak_occupancy)
            if key == "total_running_events":
                return float(self.window_entry_total)
            return 0.0
        if app == "vehicle_monitoring":
            # Per-minute THROUGHPUT keys: the number of NEW unique vehicles that
            # entered the frame across the 60s window (window_new_sum, accumulated
            # from current_new_counts in ingest_agg_summary), published with
            # agg_type "sum" — i.e. traffic flow: how many distinct vehicles passed
            # this minute, NOT the peak concurrent count in a single frame. A
            # vehicle is counted in the window it first appears, so there is no
            # cross-window double counting. Composites sum the relevant per-class
            # new arrivals; vehicle_count uses window_entry_total (all positive new
            # arrivals across classes). total_<class>_count are cumulative unique
            # tracks since session start (from the use case's total_counts).
            if key == "vehicle_count":
                return float(self.window_entry_total)
            if key == "heavy_vehicle_count":
                return float(self.window_new_sum.get("bus", 0) + self.window_new_sum.get("truck", 0))
            if key == "car_count":
                return float(self.window_new_sum.get("car", 0))
            if key == "truck_count":
                return float(self.window_new_sum.get("truck", 0))
            if key == "bus_count":
                return float(self.window_new_sum.get("bus", 0))
            if key == "van_count":
                return float(self.window_new_sum.get("van", 0))
            if key == "motorcycle_count":
                return float(self.window_new_sum.get("motorcycle", 0))
            if key == "bicycle_count":
                return float(self.window_new_sum.get("bicycle", 0))
            if key == "two_wheel_vehicle_count":
                return float(self.window_new_sum.get("motorcycle", 0) + self.window_new_sum.get("bicycle", 0))
            # Cumulative unique per-class totals (from the use case's total_counts).
            if key == "total_car_count":
                return float(self.latest_totals.get("car", 0))
            if key == "total_truck_count":
                return float(self.latest_totals.get("truck", 0))
            if key == "total_bus_count":
                return float(self.latest_totals.get("bus", 0))
            if key == "total_van_count":
                return float(self.latest_totals.get("van", 0))
            if key == "total_motorcycle_count":
                return float(self.latest_totals.get("motorcycle", 0))
            return 0.0
        if app == "parking_lot_analytics":
            # Matches parking_lot_analytics-v1.2's metrics block — see the
            # profile's volume_metrics comment. Explicitly app-gated because
            # car_count/van_count/bus_count/truck_count collide by NAME with
            # vehicle_monitoring's own (differently-semantic) keys above.
            if key == "parked_vehicles_count":
                return float(self.window_newly_parked_sum)
            if key == "avg_parking_time_wrt_to_vehicle":
                return float(self.last_avg_parking_time)
            if key == "park_entry_counts":
                return float(self.window_park_entry_sum)
            if key == "park_exit_counts":
                return float(self.window_park_exit_sum)
            if key == "max_park_seconds":
                return float(self.window_max_parked_seconds)
            if key in ("car_count", "van_count", "bus_count", "truck_count"):
                bucket = key[: -len("_count")]
                return float(self.window_newly_parked_by_category.get(bucket, 0))
            if key == "two_wheeler_count":
                return float(self.window_newly_parked_by_category.get("two_wheeler", 0))
            return 0.0
        if app == "loitering_detection":
            # loitering_count / loitering_percentage are per-frame snapshot /
            # windowed mean. loitering_unique_count and people_in_frame are
            # per-minute counts: the growth in cumulative unique track IDs across
            # the 60s window (latest_totals − window-start totals) — i.e. NEW
            # unique loiterers / people that appeared this window (agg_type "sum"),
            # not a session-cumulative or last-frame snapshot. This mirrors the
            # in_footfall / out_footfall delta pattern. Each physical person first
            # appears as "person", so the person delta counts distinct new people
            # without double counting the person→loitering_person relabel.
            if key == "loitering_count":
                return float(self.latest_current.get("loitering_person", 0))
            if key == "loitering_percentage":
                if self.window_loiter_pct_frames > 0:
                    return round(self.window_loiter_pct_sum / self.window_loiter_pct_frames, 2)
                return 0.0
            if key == "loitering_unique_count":
                return float(
                    max(
                        0,
                        self.latest_totals.get("loitering_person", 0)
                        - self.window_start_totals.get("loitering_person", 0),
                    )
                )
            if key == "people_in_frame":
                return float(
                    max(
                        0,
                        self.latest_totals.get("person", 0) - self.window_start_totals.get("person", 0),
                    )
                )
            if key == "loitering_count_total":
                # Running SESSION cumulative unique loiterers (latest
                # "loitering_person" total_count; agg_type last) — not a
                # window delta, unlike loitering_unique_count above.
                return float(self.latest_totals.get("loitering_person", 0) or 0)
            if key == "avg_loiter_time_seconds":
                return round(float(self.last_loitering_analytics.get("avg_loiter_time_seconds", 0.0) or 0.0), 2)
            if key == "max_loiter_time_seconds":
                return round(float(self.last_loitering_analytics.get("max_loiter_time_seconds", 0.0) or 0.0), 2)
            return 0.0
        if key == "entry_count":
            if profile.application_key_name == "ppe_compliance":
                return float(self.window_new_sum.get("person", 0))
            return float(self.window_entry_total)
        if key == "exit_count":
            return float(self.window_exit_total)
        if key == "in_footfall":
            return float(max(0, self.latest_totals.get("in", 0) - self.window_start_totals.get("in", 0)))
        if key == "out_footfall":
            return float(max(0, self.latest_totals.get("out", 0) - self.window_start_totals.get("out", 0)))
        if key == "current_occupancy_footfall":
            delta_in = max(0, self.latest_totals.get("in", 0) - self.window_start_totals.get("in", 0))
            delta_out = max(0, self.latest_totals.get("out", 0) - self.window_start_totals.get("out", 0))
            return float(delta_in + delta_out)
        # --------------------------------------------------------------------------
        if key == "current_occupancy":
            if profile.occupancy_mode == "max_weapon_person":
                return float(self.window_weapon_max + self.window_person_max)
            return float(self.last_occupancy)
        if key == "knives_detected":
            # New knives in the current ~60s aggregation window (sum).
            return float(self.window_new_sum.get("knife", 0))
        if key == "guns_detected":
            # New guns in the current ~60s aggregation window (sum).
            return float(self.window_new_sum.get("gun", 0))
        # VOLUME mask detection keys (mask_detection).
        # Read cumulative totals from tracking_stats.total_counts (stored as
        # latest_totals). Updated every frame; publish uses last frame in window.
        # Category keys are lowercased by _count_list_to_map ("Mask" → "mask").
        # Gated by profile so PPE's SAFETY mask_count (window_mask_ids) is untouched.
        if profile.application_key_name == "mask_detection":
            if key == "mask_count":
                return float(self.window_new_sum.get("mask", 0))
            if key == "no_mask_count":
                return float(self.window_new_sum.get("no-mask", 0))
            if key == "mask_violation_rate":
                mask = float(self.window_new_sum.get("mask", 0))
                no_mask = float(self.window_new_sum.get("no-mask", 0))
                total = mask + no_mask
                return round((no_mask / total * 100.0), 1) if total > 0 else 0.0
        # VOLUME pothole keys (pothole_detection). pothole_count is new
        # potholes this window (sum, traffic-flow style, matches
        # vehicle_monitoring's per-class counts); total_pothole_count is the
        # cumulative unique count on this route (last, matches total_car_count).
        if profile.application_key_name == "pothole_detection":
            if key == "pothole_count":
                return float(self.window_new_sum.get("pothole", 0))
            if key == "total_pothole_count":
                return float(self.latest_totals.get("pothole", 0))
        # VOLUME abandoned-object keys (abandoned_object_detection). Same
        # pattern as pothole_detection above, off the "abandoned_object"
        # category the use case assigns once a track is confirmed abandoned:
        #   abandoned_count       last-frame in-frame count -- how many objects
        #                         are abandoned RIGHT NOW (the headline number;
        #                         same value as current_occupancy, exposed under
        #                         an app-specific name for the dashboard).
        #   total_abandoned_count cumulative unique abandoned tracks (last).
        #   new_abandoned_count   newly-confirmed abandonments this window (sum)
        #                         -- rises once per object, so it reads as an
        #                         event rate rather than a standing level.
        #   tracked_object_count  every object the state machine is following,
        #                         abandoned or not, from the active_track_count
        #                         side-channel ingested above.
        if profile.application_key_name == "abandoned_object_detection":
            if key == "abandoned_count":
                return float(self.latest_frame_current.get("abandoned_object", 0))
            if key == "total_abandoned_count":
                return float(self.latest_totals.get("abandoned_object", 0))
            if key == "new_abandoned_count":
                return float(self.window_new_sum.get("abandoned_object", 0))
            if key == "tracked_object_count":
                return float(self.last_abandoned_active_tracks)
        # VOLUME flare keys (flare_analysis). Same pattern as mask_detection
        # above: windowed new-track sums per category, category keys
        # lowercased by _count_list_to_map ("BadFlare" -> "badflare").
        if profile.application_key_name == "flare_analysis":
            if key == "goodflare_count":
                return float(self.window_new_sum.get("goodflare", 0))
            if key == "badflare_count":
                return float(self.window_new_sum.get("badflare", 0))
            if key == "bad_flare_rate":
                good = float(self.window_new_sum.get("goodflare", 0))
                bad = float(self.window_new_sum.get("badflare", 0))
                total = good + bad
                return round((bad / total * 100.0), 1) if total > 0 else 0.0
        # VOLUME gender keys (gender_detection). Last-frame in-frame counts
        # (from tracking_stats.current_counts, stored as latest_current),
        # agg_type "last" -- not a cumulative/windowed total.
        if profile.application_key_name == "gender_detection":
            if key == "male_count":
                return float(self.latest_current.get("male", 0))
            if key == "female_count":
                return float(self.latest_current.get("female", 0))
        # VOLUME age keys (age_detection). Last-frame in-frame counts per
        # bucket (from tracking_stats.current_counts, stored as latest_current),
        # agg_type "last" -- not a cumulative/windowed total.
        if profile.application_key_name == "age_detection":
            if key == "child_count":
                return float(self.latest_current.get("child", 0))
            if key == "adult_count":
                return float(self.latest_current.get("adult", 0))
            if key == "senior_count":
                return float(self.latest_current.get("senior", 0))
        # VOLUME emotion keys (face_emotion). Last-frame in-frame counts per
        # emotion (from tracking_stats.current_counts, stored as latest_current),
        # agg_type "last" -- not a cumulative/windowed total. Drives the emotion
        # distribution graph.
        if profile.application_key_name == "face_emotion":
            if key == "surprise_count":
                return float(self.latest_current.get("surprise", 0))
            if key == "fear_count":
                return float(self.latest_current.get("fear", 0))
            if key == "disgust_count":
                return float(self.latest_current.get("disgust", 0))
            if key == "happiness_count":
                return float(self.latest_current.get("happiness", 0))
            if key == "sadness_count":
                return float(self.latest_current.get("sadness", 0))
            if key == "anger_count":
                return float(self.latest_current.get("anger", 0))
            if key == "neutral_count":
                return float(self.latest_current.get("neutral", 0))
        # VOLUME dwell keys (dwell_detection).
        # visitors_in_zone / active_dwellers use window-accumulated unique track_ids
        # (all distinct people seen across the full 60s window) rather than the
        # last-frame snapshot, giving a more accurate per-minute headcount.
        if key == "visitors_in_zone":
            return float(len(self.window_visitor_ids)) if self.window_visitor_ids else float(self.last_visitors_in_zone)
        if key == "active_dwellers":
            return float(len(self.window_dweller_ids)) if self.window_dweller_ids else float(self.last_active_dwellers)
        if key == "unique_dwellers":
            return float(self.last_unique_dwellers)
        if key == "dwell_percentage":
            if self.window_dwell_pct_frames > 0:
                return round(self.window_dwell_pct_sum / self.window_dwell_pct_frames, 2)
            return 0.0
        if key == "avg_dwell_time":
            return round(float(self.last_avg_dwell_seconds), 2)
        if key == "max_dwell_time":
            return round(float(self.last_max_dwell_seconds), 2)
        # SAFETY keys (ppe_compliance) — window semantics match SafetyProcessor.
        if key == "total_persons":
            return float(len(self.window_person_ids))
        if key == "violation_count":
            return float(len(self.window_violator_ids))
        if key == "compliant_count":
            unique_persons = len(self.window_person_ids)
            if unique_persons > 0:
                return float(max(0, unique_persons - len(self.window_violator_ids)))
            return 0.0
        if key == "compliance_pct":
            if self.window_compliance_pct_frames > 0:
                return round(self.window_compliance_pct_sum / self.window_compliance_pct_frames, 6)
            return 0.0
        if key == "hardhat_count":
            return float(len(self.window_hardhat_ids))
        if key == "safety_vest_count":
            return float(len(self.window_safety_vest_ids))
        if key == "mask_count":
            return float(len(self.window_mask_ids))
        return 0.0

    def _build_volume_metrics(self, profile: LegacyAnalyticsProfile) -> List[Dict[str, Any]]:
        metrics: List[Dict[str, Any]] = []
        for spec in profile.volume_metrics:
            metrics.append(
                {
                    "key": spec.key,
                    "data": self._resolve_metric_value(spec.key, profile),
                    "agg_type": spec.agg_type,
                    "category": spec.category,
                    "zone": ANALYTICS_ZONE_GLOBAL,
                }
            )
        return metrics

    def _build_tracking_stats_block(
        self,
        profile: LegacyAnalyticsProfile,
        input_ts: str,
    ) -> Dict[str, Any]:
        cats = profile.default_tracking_categories

        if profile.rollup_mode == "latest_snapshot":
            cats = profile.default_tracking_categories
            current_counts = _map_to_count_list(
                _filter_count_map(self.latest_frame_current, cats)
            ) or _default_count_list(cats)
            current_new_counts = _map_to_count_list(_filter_count_map(self.latest_new, cats)) or _default_count_list(
                cats
            )
            total_counts = _map_to_count_list(_filter_count_map(self.latest_totals, cats)) or _default_count_list(cats)
            total_current_counts = (
                _map_to_count_list(_filter_count_map(self.window_total_current_max, cats))
                or _map_to_count_list(_filter_count_map(self.latest_current, cats))
                or list(current_counts)
            )
            total_current_counts = _ensure_total_current_at_least_current(current_counts, total_current_counts)
            return {
                "input_timestamp": input_ts,
                "current_counts": _restore_canonical_casing(current_counts, cats),
                "current_new_counts": _restore_canonical_casing(current_new_counts, cats),
                "total_counts": _restore_canonical_casing(total_counts, cats),
                "total_current_counts": _restore_canonical_casing(total_current_counts, cats),
            }

        # current_counts = sum of new confirmed track IDs over this 60s window.
        current_counts = _map_to_count_list(self.window_new_sum) or _default_count_list(cats)
        current_new_counts = _map_to_count_list(self.latest_new) or _default_count_list(cats)
        total_counts = _map_to_count_list(self.latest_totals) or list(current_counts)

        # total_current_counts = (last-frame current_counts of previous 60s agg)
        #                      + (this window's new-ID sum).
        # First agg after stream start: prev carry is empty → both equal.
        # prev_last/new_arrivals are clamped to >=0 so a negative value leaking in
        # from upstream (bad tracker delta, stale carry) can't push the total below
        # current_counts for that category.
        carry = self.prev_window_last_frame_current
        all_cats = set(cats) | set(carry) | set(self.window_new_sum)
        total_current_counts: List[Dict[str, Any]] = []
        for cat in sorted(all_cats):
            prev_last = max(0, int(carry.get(cat, 0) or 0))
            new_arrivals = max(0, int(self.window_new_sum.get(cat, 0) or 0))
            total_current_counts.append({"category": cat, "count": prev_last + new_arrivals})
        if not total_current_counts:
            total_current_counts = _default_count_list(cats)
        total_current_counts = _ensure_total_current_at_least_current(current_counts, total_current_counts)

        return {
            "input_timestamp": input_ts,
            "current_counts": _restore_canonical_casing(current_counts, cats),
            "current_new_counts": _restore_canonical_casing(current_new_counts, cats),
            "total_counts": _restore_canonical_casing(total_counts, cats),
            "total_current_counts": _restore_canonical_casing(total_current_counts, cats),
        }

    def _reset_window(self) -> None:
        self.window_weapon_max = 0
        self.window_person_max = 0
        self.window_new_sum.clear()
        self.window_baseline.clear()
        self.window_baseline_set = False
        self.window_total_current_max.clear()
        self.window_start_totals.clear()
        self.window_start_totals_set = False
        self.window_entry_total = 0
        self.window_exit_total = 0
        self.window_corridor_occupancy_peak = 0
        self.last_occupancy = 0
        self.window_peak_occupancy = 0
        self.window_loiter_pct_sum = 0.0
        self.window_loiter_pct_frames = 0
        self.last_loitering_analytics = {}
        self.window_park_entry_sum = 0
        self.window_park_exit_sum = 0
        self.last_avg_parking_time = 0.0
        self.window_max_parked_seconds = 0.0
        self.window_newly_parked_sum = 0
        self.window_newly_parked_by_category = {}
        self.last_visitors_in_zone = 0
        self.last_active_dwellers = 0
        self.last_unique_dwellers = 0
        self.last_avg_dwell_seconds = 0.0
        self.last_max_dwell_seconds = 0.0
        self.window_dwell_pct_sum = 0.0
        self.window_dwell_pct_frames = 0
        self.window_person_ids.clear()
        self.window_violator_ids.clear()
        self.window_hardhat_ids.clear()
        self.window_safety_vest_ids.clear()
        self.window_mask_ids.clear()
        self.window_compliance_pct_sum = 0.0
        self.window_compliance_pct_frames = 0
        # last_hazard_analytics / last_intrusion_analytics are NOT cleared here —
        # same "last known value" precedent as pipe_last_current below: both
        # usecases publish their block unconditionally every frame, but a window
        # can still close without one landing (dropped frame, ingest race). A
        # cleared dict would fabricate 0 for unique_zone_entrants/unique_intruders,
        # monotonic counters that must never regress, plus every other hazard/
        # intrusion metric that window. hazard_window_start_entrants /
        # intrusion_window_start_intruders DO reset — they are genuinely
        # per-window baselines for the *_in_interval deltas below.
        self.hazard_window_start_entrants = None
        self.window_hazard_pct_sum = 0.0
        self.window_hazard_pct_frames = 0
        self.intrusion_window_start_intruders = None
        self.window_intrusion_pct_sum = 0.0
        self.window_intrusion_pct_frames = 0
        # last_customer_service_analytics is NOT cleared, same "last known value"
        # precedent as last_hazard_analytics / last_intrusion_analytics: clearing
        # it would fabricate 0 for unique_customers / total_customers_served /
        # total_abandoned, monotonic counters that must never regress.
        #
        # The cs_window_start_* baselines DO carry over, but as the CLOSING
        # window's final reading rather than as None. hazard/intrusion re-seed
        # theirs from the next window's FIRST frame, which loses whatever growth
        # happened between one window's last frame and the next window's first --
        # a real customer served across a window boundary is a count that never
        # gets published anywhere. Seeding from the retained block instead makes
        # the per-window deltas partition the session total exactly. It stays
        # correct for a quiet window too: with no new frame the current value
        # still equals the baseline, so the delta is 0.
        self.cs_window_start_customers = _coerce_optional_int(
            self.last_customer_service_analytics.get("unique_customers")
        )
        self.cs_window_start_served = _coerce_optional_int(
            self.last_customer_service_analytics.get("total_customers_served")
        )
        self.cs_window_start_abandoned = _coerce_optional_int(
            self.last_customer_service_analytics.get("total_abandoned")
        )
        self.window_counter_util_sum = 0.0
        self.window_counter_util_frames = 0
        self.window_staff_cov_sum = 0.0
        self.window_staff_cov_frames = 0
        self.window_queue_len_sum = 0
        self.window_queue_len_frames = 0
        self.window_cs_max_queue = 0
        self.window_cs_ratio_sum = 0.0
        self.window_cs_ratio_frames = 0
        self.last_tailgating_analytics = {}
        self.window_tailgating_events_sum = 0
        self.window_tailgating_pct_sum = 0.0
        self.window_tailgating_pct_frames = 0
        self.last_overcrowding_analytics = {}
        self.window_occupancy_peak = 0
        self.window_occupancy_sum = 0
        self.window_occupancy_frames = 0
        self.window_occupancy_pct_sum = 0.0
        self.window_occupancy_pct_frames = 0
        self.area_util_window_occupancy_sum = 0
        self.area_util_window_occupancy_frames = 0
        self.area_util_window_occupied_frames = 0
        # NOT reset: last_abandoned_active_tracks is a latest-frame snapshot, so
        # zeroing it here would make tracked_object_count read 0 on any window
        # that publishes before the next frame arrives.
        self.window_visitor_ids.clear()
        self.window_dweller_ids.clear()
        self.last_flood_detection_count = 0
        self.last_max_flood_area_pct = 0.0
        self.last_total_flood_area_pct = 0.0
        self.window_flood_pct_sum = 0.0
        self.window_flood_pct_frames = 0
        self.last_landslide_detection_count = 0
        self.last_max_landslide_area_pct = 0.0
        self.last_total_landslide_area_pct = 0.0
        self.window_landslide_pct_sum = 0.0
        self.window_landslide_pct_frames = 0
        self.window_critical_accidents = 0
        self.window_defect_ids.clear()
        self.window_inspected_ids.clear()
        self.window_peak_defect = 0
        self.window_peak_inspected = 0
        self.last_wrong_way_analytics = {}
        self.last_quality_analytics = {}
        # Pipe inspection family: clear the per-window accumulators only.
        # pipe_last_current / pipe_last_total_unique / pipe_max_continuous_seconds
        # are deliberately NOT cleared — they are "last known value" snapshots
        # that every ingested frame overwrites, so preserving them only matters
        # when a window passes with no frames ingested (quiet stream). Zeroing
        # them there would make a cumulative total and a longest-streak metric
        # visibly regress to 0 on the dashboard.
        self.pipe_window_new_ids.clear()
        self.pipe_window_peak = 0
        self.pipe_window_active_frames = 0
        self.pipe_window_total_frames = 0
        self.pipe_window_active_seconds = 0.0
        # Industrial inspection family: per-window accumulators only.
        # insp_last_total_unique / insp_max_continuous_seconds are deliberately
        # NOT cleared — they are "last known value" snapshots that every ingested
        # frame overwrites, so preserving them only matters when a window passes
        # with no frames ingested (quiet stream). Zeroing them there would make a
        # cumulative total visibly regress to 0 on the dashboard.
        # (window_defect_ids / window_inspected_ids / window_peak_* are shared
        # with car damage and already cleared above.)
        self.insp_window_new_defect_ids.clear()
        self.insp_window_active_frames = 0
        self.insp_window_total_frames = 0
        # assembly_line_detection: per-window accumulators only.
        # asm_last_current_total is preserved for the same reason as above.
        self.asm_window_new_loaded_ids.clear()
        self.asm_window_new_empty_ids.clear()
        self.asm_window_peak_robot_arms = 0
        self.window_tracked_vehicle_ids.clear()
        self.window_violation_ids.clear()
        self.window_dwell_sum = 0.0
        self.window_dwell_count = 0
        self.window_peak_tracked = 0
        self.window_peak_violations = 0

    def maybe_publish_incident(
        self,
        incident_data: Dict[str, Any],
        stream_info: Optional[Dict[str, Any]],
        *,
        usecase: str,
        app_name: Optional[str],
        publisher: Any,
        camera_id: Optional[str] = None,
    ) -> bool:
        """Publish to ``incident_res`` on severity transition (deduped)."""
        profile = get_legacy_profile(usecase)
        if not profile or not profile.publish_incidents:
            return False
        if not incident_data or not publisher:
            return False
        from .incident_res_format import is_valid_incident_end_time

        level = str(incident_data.get("severity_level", "none")).lower()
        is_close = level == "info" or is_valid_incident_end_time(incident_data.get("end_time"))
        if level in ("", "none") and not is_close:
            return False
        if not is_close and level == self.last_incident_level:
            return False

        ctx = extract_stream_context(stream_info, usecase=usecase, app_name=app_name)
        cid = camera_id or ctx["camera_id"]
        payload = build_incident_message(incident_data, stream_info, usecase=usecase, app_name=app_name, camera_id=cid)
        ok = bool(publisher.publish_incident(cid, payload))
        if ok:
            wire_level = "info" if is_close else level
            self.last_incident_level = wire_level
            logger.info(
                "[LEGACY_ANALYTICS] incident_res published usecase=%s camera=%s level=%s",
                usecase,
                cid,
                wire_level,
            )
        return ok

    def maybe_publish_results_agg(
        self,
        stream_info: Optional[Dict[str, Any]],
        *,
        usecase: str,
        app_name: Optional[str],
        publisher: Any,
        force: bool = False,
    ) -> bool:
        """Publish ``results-agg`` every ~60s with zone-keyed tracking_stats + metrics."""
        profile = get_legacy_profile(usecase)
        if not profile or not publisher:
            return False
        if not profile.volume_metrics:
            return False
        # Match the OLD AnalyticsPublisher: no tracking data seen -> nothing to
        # roll up, so we do not publish an empty window (avoids stream spam for
        # incident-only apps that emit no tracking_stats).
        if not self.saw_tracking:
            return False
        now = time.time()
        if not force and self.last_agg_publish_ts and (now - self.last_agg_publish_ts) < AGGREGATION_INTERVAL_SEC:
            return False

        input_ts = _utc_now_iso_z()
        ctx = extract_stream_context(stream_info, usecase=usecase, app_name=app_name)
        cid = ctx["camera_id"]

        tracking_block = self._build_tracking_stats_block(profile, input_ts)
        metrics = self._build_volume_metrics(profile)

        payload = {
            **ctx,
            "locationId": ctx["locationId"],
            "input_timestamp": input_ts,
            "tracking_stats": {ANALYTICS_ZONE_GLOBAL: tracking_block},
            "metrics": metrics,
        }

        ok = bool(publisher.publish_aggregation(cid, payload))
        if ok:
            self.last_agg_publish_ts = now
            # Persist last-frame in-frame occupancy for the next window's
            # total_current_counts carry. First publish after start leaves the
            # previous carry empty (zeros); subsequent windows use this snapshot.
            self.prev_window_last_frame_current = {
                cat: int(count) for cat, count in dict(self.latest_frame_current).items()
            }
            self._reset_window()
            logger.info(
                "[LEGACY_ANALYTICS] results-agg published usecase=%s camera=%s metrics=%s",
                usecase,
                cid,
                [m["key"] for m in metrics],
            )
        return ok


def publish_legacy_frame_analytics(
    *,
    usecase: str,
    agg_summary: Any,
    incident_data: Optional[Dict[str, Any]],
    stream_info: Optional[Dict[str, Any]],
    stream_key: str,
    app_name: Optional[str],
    publisher: Any,
    incident_via_manager: bool = False,
) -> None:
    """
    Ingest one legacy frame and publish Redis analytics when due.

    ``incident_via_manager`` is True when ``IncidentManager`` already handled
    the incident for this frame (skip duplicate ``incident_res`` publish).
    """
    profile = get_legacy_profile(usecase)
    if profile is None or publisher is None:
        return

    session = get_legacy_session(stream_key)
    session.ingest_agg_summary(agg_summary, profile=profile)

    if incident_data and not incident_via_manager:
        session.maybe_publish_incident(
            incident_data,
            stream_info,
            usecase=usecase,
            app_name=app_name,
            publisher=publisher,
        )

    session.maybe_publish_results_agg(
        stream_info,
        usecase=usecase,
        app_name=app_name,
        publisher=publisher,
    )
