"""Config-driven tracker wiring for post-processing use cases."""

from __future__ import annotations

import logging
import os
from enum import Enum
from typing import Any, Dict, List, Optional

from ..advanced_tracker import AdvancedTracker
from ..advanced_tracker.config import TrackerConfig
from .base import BaseObjectTracker, DetectionDict
from .config import MatriceTrackerConfig
from .factory import create_tracker, normalize_tracking_method

logger = logging.getLogger(__name__)


def tracker_namespace(stream_info: Optional[Dict[str, Any]]) -> Optional[str]:
    """Derive a per-stream namespace for track ID isolation."""
    if stream_info and stream_info.get("stream_key"):
        return str(hash(stream_info["stream_key"]) % 1000000)
    return None


def get_effective_tracking_method(config: Any) -> Optional[str]:
    """
    Resolve which Matrice tracker to run from a use-case config.

    Priority:
    1. Explicit ``tracking_method`` on config (``"none"`` disables tracking)
    2. Legacy ``enable_advanced_tracker=True`` → ``"advanced"`` (other use cases)
    3. Otherwise no Matrice tracker
    """
    raw = getattr(config, "tracking_method", None)
    if raw is not None and str(raw).strip():
        method = normalize_tracking_method(str(raw))
        if method == "none":
            return None
        return method

    if getattr(config, "enable_advanced_tracker", False):
        return "advanced"

    return None


# =============================================================================
# The shared seam (F10b step S5) — for the 110 bare `AdvancedTracker(...)`
# construction sites in usecases/*.py, NOT for the method-name-dispatch path
# `ConfigDrivenTracker.apply()` already serves (deep_oc_sort.py,
# violence_detection_testing.py). Deliberately bypasses
# `MatriceTrackerConfig.from_config` (Trackers/config.py:107-150) entirely,
# whose defaults are 0.4/0.05/0.3/0.8 — routing the 73 bare-default sites
# through it would silently retune all of them (see consolidation plan §1.8).
# =============================================================================


class TrackerProfile(str, Enum):
    """Named `TrackerConfig` baselines measured across the 136 literal
    `TrackerConfig(...)` call sites in usecases/ (consolidation plan §1.8).
    An enum + `**overrides` on `build_tracker_config`, not a 136-row config
    table — the drift is 4 real profiles plus 4 bespoke outliers, and a
    table keyed by use-case name would need to be kept in sync with the file
    list forever."""

    #: 73 bare `TrackerConfig()` sites — literally `TrackerConfig`'s own
    #: dataclass defaults (0.5/0.1/0.5/0.5, buffer 600, max_time_lost 1800).
    #: No override needed; kept as a named profile for call-site clarity.
    DEFAULT = "default"

    #: 21 sites — 0.4/0.05/0.3/0.8, buffer 600, max_time_lost 1800. Also
    #: `MatriceTrackerConfig.from_config`'s defaults (the `Trackers/`-factory
    #: path) — same threshold family, different buffer/mtl combination below.
    LEGACY_40 = "legacy_40"

    #: `analytics/engine_session.py:490-498` (the F18 new-flow tracker) —
    #: LEGACY_40's thresholds with max_time_lost=1200, frame_rate=25.
    #: `namespace=True` here is load-bearing (F18 flow) and must stay
    #: `str(hash(stream_key) % 1000000)` verbatim (matches `tracker_namespace`).
    NEW_FLOW = "new_flow"

    #: `face_reg/face_recognition.py:2312-2321` — 0.5/0.05/0.5/0.8,
    #: `enable_gmc=False`, `frame_rate=20`. Buffer/max_time_lost come from
    #: the use-case's own `tracker_buffer`/`tracker_max_time_lost` config
    #: fields (default 600/300) — passed as overrides, not baked into the
    #: profile, since they are themselves configurable there.
    FACE = "face"


_PROFILE_BASE_KWARGS: Dict["TrackerProfile", Dict[str, Any]] = {
    TrackerProfile.DEFAULT: {},
    TrackerProfile.LEGACY_40: {
        "track_high_thresh": 0.4,
        "track_low_thresh": 0.05,
        "new_track_thresh": 0.3,
        "match_thresh": 0.8,
        "track_buffer": 600,
        "max_time_lost": 1800,
    },
    TrackerProfile.NEW_FLOW: {
        "track_high_thresh": 0.4,
        "track_low_thresh": 0.05,
        "new_track_thresh": 0.3,
        "match_thresh": 0.8,
        "track_buffer": 600,
        "max_time_lost": 1200,
        "frame_rate": 25,
    },
    TrackerProfile.FACE: {
        "track_high_thresh": 0.5,
        "track_low_thresh": 0.05,
        "new_track_thresh": 0.5,
        "match_thresh": 0.8,
        "fuse_score": True,
        "enable_gmc": False,
        "frame_rate": 20,
    },
}


def build_tracker_config(
    profile: TrackerProfile = TrackerProfile.DEFAULT,
    config: Any = None,
    stream_info: Optional[Dict[str, Any]] = None,
    *,
    derive_from_confidence: bool = True,
    **overrides: Any,
) -> TrackerConfig:
    """Resolve a `TrackerConfig` for a use-case call site: profile baseline,
    then explicit ``**overrides`` (the 4 bespoke sites — `hazard_zone_entry.py`
    14 fields, `pedestrian_detection.py` max_time_lost=1200,
    `vehicle_color_detection.py` 0.6/0.1/0.7/0.6, `illegal_parking_detection.py`
    — pass these), then (if enabled and ``config.confidence_threshold`` is
    set) the confidence-derived override — reproducing
    `Trackers/advanced_tracker/adapter.py:67-70` /
    `usecases/age_detection.py:188-193` byte-for-byte: ``track_high_thresh``
    and ``new_track_thresh`` become the confidence threshold,
    ``track_low_thresh`` becomes ``max(0.05, confidence_threshold / 2)`` —
    `match_thresh`/buffer/mtl are untouched by this step, matching every real
    site that does it.

    ``config``/``stream_info`` are accepted (not just ``**overrides``) so
    call sites can pass the use-case config object directly, matching the
    shape of the existing `MatriceTrackerConfig.from_config(config,
    stream_info)` call convention — `stream_info` is unused today (no current
    reference site derives a `TrackerConfig` field from it) and is accepted
    for forward compatibility with a future fps-from-stream resolver.
    """
    _ = stream_info
    kwargs: Dict[str, Any] = dict(_PROFILE_BASE_KWARGS.get(profile, {}))
    kwargs.update(overrides)
    tracker_config = TrackerConfig(**kwargs)

    if derive_from_confidence and config is not None:
        conf = getattr(config, "confidence_threshold", None)
        if conf is not None:
            tracker_config.track_high_thresh = float(conf)
            tracker_config.track_low_thresh = max(0.05, float(conf) / 2)
            tracker_config.new_track_thresh = float(conf)

    return tracker_config


# =============================================================================
# F10b step S9 (consolidation plan §9.3 Step 9): the 7 use-cases whose default
# ``tracking_method`` is "sort" (abandoned_object_detection, area_utilization,
# flood_detection, landslide_detection, loitering_detection,
# overcrowding_detection, tailgating_detection) route onto this same seam
# instead of the legacy SORTTracker/ByteTrackWrapper (utils/bytetrack_utils.py).
# ``MATRICE_LEGACY_SORT=1`` is the kill-switch that keeps the old path alive
# for one release, per the plan's own rollback requirement (§7).
# =============================================================================

MATRICE_LEGACY_SORT_ENV = "MATRICE_LEGACY_SORT"


def legacy_sort_enabled() -> bool:
    """True when the S9 kill-switch is set, keeping the pre-migration
    SORTTracker/ByteTrackWrapper path alive for one release."""
    return os.environ.get(MATRICE_LEGACY_SORT_ENV) == "1"


def legacy_sort_tracker_overrides(config: Any, method: str) -> Dict[str, Any]:
    """Best-effort kwarg mapping from the legacy SORTTracker/ByteTrackWrapper's
    config knobs onto `AdvancedTracker`'s ByteTrack-style two-stage thresholds,
    for the S9 use-cases above.

    This is deliberately **not** a byte-identical parity mapping:
    ``SORTTracker``'s single-stage IoU assignment and ``ByteTrackWrapper``'s
    IoU-only re-match (`bytetrack_utils.py`) have no exact equivalent in
    `AdvancedTracker`'s two-stage cascade -- the consolidation plan itself
    calls this "a behaviour change by construction" (§1.3). The actual
    verification is the shadow-diff gate (>=95% per-frame `tracking_stats`
    count parity), not this function.

    ``method == "bytetrack"``: `ByteTrackWrapper` wraps YOLOX's `BYTETracker`,
    which is itself the algorithm `AdvancedTracker` is modeled on, so
    ``bytetrack_track_thresh``/``bytetrack_match_thresh`` map directly onto
    `track_high_thresh`/`match_thresh` -- both are already score/cost-max
    thresholds in the same units.

    Every other resolved method (including the "sort" default): `SORTTracker`
    has **no** confidence gate at all -- every input detection is matched
    regardless of score -- so `track_high_thresh`/`track_low_thresh`/
    `new_track_thresh` are set to 0.0 (nothing pre-filtered, matching SORT).
    Its own `tracking_iou_threshold` is a MINIMUM-IoU-to-accept, the inverse
    of `match_thresh` (a MAXIMUM ``1 - IoU`` cost) -- inverted here
    accordingly, not passed through as-is (empirically confirmed via a
    synthetic shadow-diff: passing it through directly made `match_thresh`
    far stricter than intended and silently dropped re-matched tracks).

    ``tracking_max_age`` maps to both ``track_buffer`` and ``max_time_lost``
    (SORT/ByteTrack use one knob for "how long to keep a lost track").
    """
    max_age = int(getattr(config, "tracking_max_age", 30))
    if method == "bytetrack":
        track_thresh = float(getattr(config, "bytetrack_track_thresh", 0.25))
        match_thresh = float(getattr(config, "bytetrack_match_thresh", 0.80))
        return {
            "track_high_thresh": track_thresh,
            "track_low_thresh": max(0.05, track_thresh / 2),
            "new_track_thresh": track_thresh,
            "match_thresh": match_thresh,
            "track_buffer": max_age,
            "max_time_lost": max_age,
        }

    iou_floor = float(getattr(config, "tracking_iou_threshold", 0.25))
    return {
        "track_high_thresh": 0.0,
        "track_low_thresh": 0.0,
        "new_track_thresh": 0.0,
        "match_thresh": max(0.01, 1.0 - iou_floor),
        "track_buffer": max_age,
        "max_time_lost": max_age,
    }


class ConfigDrivenTracker:
    """Lazy-init tracker selected by ``config.tracking_method``."""

    def __init__(self) -> None:
        self._tracker: Optional[BaseObjectTracker] = None
        self._method: Optional[str] = None
        # Separate cache slot for get_shared_tracker() (below) -- a distinct
        # seam from apply()'s method-name dispatch above, so the two never
        # collide if a future caller somehow used both on one instance.
        self._shared_tracker: Optional[AdvancedTracker] = None

    @property
    def is_initialized(self) -> bool:
        return self._tracker is not None

    def reset(self) -> None:
        if self._tracker is not None:
            try:
                self._tracker.reset()
            except Exception:
                pass
        self._tracker = None
        self._method = None
        if self._shared_tracker is not None:
            try:
                self._shared_tracker.reset()
            except Exception:
                pass
        self._shared_tracker = None

    def apply(
        self,
        detections: List[DetectionDict],
        config: Any,
        stream_info: Optional[Dict[str, Any]] = None,
        *,
        log: Optional[logging.Logger] = None,
    ) -> List[DetectionDict]:
        """Run tracking when enabled on ``config``; otherwise return detections unchanged."""
        method = get_effective_tracking_method(config)
        if not method:
            return detections

        log = log or logger
        namespace = tracker_namespace(stream_info)

        if self._tracker is None or self._method != method:
            tracker_cfg = MatriceTrackerConfig.from_config(config, stream_info)
            self._tracker = create_tracker(method, tracker_cfg, namespace=namespace)
            self._method = method
            if hasattr(self._tracker, "restore_state"):
                try:
                    self._tracker.restore_state()
                except Exception:
                    pass
            log.info("Initialized %s tracker (namespace=%s)", method, namespace)

        return self._tracker.update(detections, stream_info=stream_info)

    def get_shared_tracker(
        self,
        config: Any = None,
        stream_info: Optional[Dict[str, Any]] = None,
        *,
        profile: TrackerProfile = TrackerProfile.DEFAULT,
        namespace: bool = False,
        restore: bool = False,
        gate_attr: Optional[str] = None,
        derive_from_confidence: bool = True,
        log: Optional[logging.Logger] = None,
        **overrides: Any,
    ) -> Optional[AdvancedTracker]:
        """Lazily construct (or return the cached) `AdvancedTracker` for this
        instance, resolved via `build_tracker_config` -- the seam for the 110
        bare-`AdvancedTracker(...)` use-case call sites (consolidation plan
        §3), not the method-name-dispatch `.apply()` above (which stays the
        seam for `deep_oc_sort`/`legacy_analytics`-style method selection).

        Args:
            config: optional -- some sites factor tracker construction into a
                helper method (e.g. `_apply_advanced_tracking(self,
                processed_data)`) that never received the use-case config
                object at all (its original `TrackerConfig()` was always
                bare). `None` is safe: `derive_from_confidence` and
                `gate_attr` both no-op on a `None` config.
            profile: which `TrackerProfile` baseline to resolve.
            namespace: **default False** -- 90 of the 110 call sites have no
                namespace today (consolidation plan §1.7); defaulting this on
                would flip `track_id` numbering across those 90 use-cases,
                moving `tracking_stats` (the F18-gated field). Only the F18
                new-flow site (`engine_session.py`) and a handful of others
                pass `True`.
            restore: **default False** -- only 17 of 113 files call
                `restore_state()` today; defaulting this on would restore
                persisted cumulative counts across 90 use-cases that never
                did before, also moving `tracking_stats`.
            gate_attr: e.g. `"enable_advanced_tracker"` for the 12 files that
                gate construction on a legacy boolean config field. When set
                and falsy on `config`, returns None without constructing
                anything (tracking stays off for this instance).
            **overrides: passed straight through to `build_tracker_config`
                for the 4 bespoke call sites.
        """
        if gate_attr is not None and not getattr(config, gate_attr, False):
            return None

        if self._shared_tracker is not None:
            return self._shared_tracker

        log = log or logger
        tracker_config = build_tracker_config(
            profile,
            config,
            stream_info,
            derive_from_confidence=derive_from_confidence,
            **overrides,
        )
        ns = tracker_namespace(stream_info) if namespace else None
        self._shared_tracker = AdvancedTracker(tracker_config, namespace=ns)

        if restore and hasattr(self._shared_tracker, "restore_state"):
            try:
                self._shared_tracker.restore_state()
            except Exception:
                pass

        log.info(
            "Initialized shared AdvancedTracker (profile=%s, namespace=%s, restore=%s)",
            profile.value if isinstance(profile, TrackerProfile) else profile,
            ns,
            restore,
        )
        return self._shared_tracker
