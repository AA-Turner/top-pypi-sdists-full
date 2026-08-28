"""Stub file for post_processing.Trackers directory."""
from typing import Any, Dict, List, Optional, Set, Tuple

from ..advanced_tracker import AdvancedTracker
from ..advanced_tracker.config import TrackerConfig
from ..utils.bytetrack_utils import bbox_to_xyxy, iou_xyxy
from .advanced_tracker import AdvancedTrackerAdapter
from .base import BaseObjectTracker
from .base import BaseObjectTracker, DetectionDict
from .bytetrack import ByteTrackAdapter
from .config import MatriceTrackerConfig
from .config import SUPPORTED_TRACKING_METHODS, MatriceTrackerConfig
from .deep_oc_sort import DeepOCSortAdapter
from .factory import create_tracker, normalize_tracking_method
from .sort import SORTTrackerAdapter

# Constants
DetectionDict: Any = ...  # From base
SUPPORTED_TRACKING_METHODS: Any = ...  # From config
logger: Any = ...  # From factory
MATRICE_LEGACY_SORT_ENV: str = ...  # From integration
logger: Any = ...  # From integration

# Functions
# From base
def ensure_track_id(detections: List[Any]) -> List[Any]:
    """
    Set ``track_id`` to -1 when missing (SORT/ByteTrack convention).
    """
    ...

# From det_utils
def assign_track_ids_by_iou(detections: List[Dict[str, Any]], track_boxes: List[Tuple[Any.Any, int]], min_iou: float = 0.1) -> List[Dict[str, Any]]:
    """
    Map tracker output boxes onto input detections via IoU.
    
        F10b S12 (consolidation-plan.md Step 12): this package's own in-package copy of
        the IoU remap, kept for ``deep_oc_sort`` (its only caller, `Trackers/deep_oc_sort/
        adapter.py`) rather than unified away -- ``py_inference`` is the only place the
        plan designates a canonical shared implementation for. ``min_iou=0.10`` is
        **inclusive** (``>=``, not ``>``): a detection/track pair at exactly the boundary
        IoU counts as a match. This differs from two of the plan's other five IoU-remap
        sites, which gate on strict ``>`` -- picking ``>=`` here is a deliberate, called-out
        semantics choice (consolidation-plan.md §1.12), not an oversight.
    """
    ...

# From det_utils
def frame_from_stream(stream_info: Optional[Dict[str, Any]]) -> Any:
    """
    Return a BGR frame array from ``stream_info`` when present.
    """
    ...

# From det_utils
def stream_resolution(stream_info: Optional[Dict[str, Any]]) -> Tuple[int, int]:
    """
    Return ``(height, width)`` from stream_info; default ``(480, 640)``.
    """
    ...

# From factory
def create_tracker(method: str, config: Optional[Any] = None, namespace: Optional[str] = None) -> Any:
    """
    Factory for post-processing trackers.
    
    Args:
        method: ``advanced`` | ``sort`` | ``bytetrack`` | ``deep_oc_sort``. ``oc_sort`` /
            ``deepsort`` / ``botsort`` are accepted (see ``SUPPORTED_TRACKING_METHODS``)
            but normalize to ``advanced`` -- their adapters were deleted (F10b step S3).
        config: Unified tracker configuration
        namespace: Optional stream namespace for ID isolation (advanced tracker)
    
    Returns:
        BaseObjectTracker instance
    """
    ...

# From factory
def normalize_tracking_method(method: str) -> str: ...

# From integration
def build_tracker_config(profile: Any = TrackerProfile.DEFAULT, config: Any = None, stream_info: Optional[Dict[str, Any]] = None, **overrides: Any) -> Any:
    """
    Resolve a `TrackerConfig` for a use-case call site: profile baseline,
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
    ...

# From integration
def get_effective_tracking_method(config: Any) -> Optional[str]:
    """
    Resolve which Matrice tracker to run from a use-case config.
    
    Priority:
    1. Explicit ``tracking_method`` on config (``"none"`` disables tracking)
    2. Legacy ``enable_advanced_tracker=True`` → ``"advanced"`` (other use cases)
    3. Otherwise no Matrice tracker
    """
    ...

# From integration
def legacy_sort_enabled() -> bool:
    """
    True when the S9 kill-switch is set, keeping the pre-migration
        SORTTracker/ByteTrackWrapper path alive for one release.
    """
    ...

# From integration
def legacy_sort_tracker_overrides(config: Any, method: str) -> Dict[str, Any]:
    """
    Best-effort kwarg mapping from the legacy SORTTracker/ByteTrackWrapper's
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
    ...

# From integration
def tracker_namespace(stream_info: Optional[Dict[str, Any]]) -> Optional[str]:
    """
    Derive a per-stream namespace for track ID isolation.
    """
    ...

# Classes
# From base
class BaseObjectTracker:
    # Matrice-facing tracker API: List[Dict] in, same list + track_id out.

    def reset(self: Any) -> None:
        """
        Reset internal tracker state.
        """
        ...

    def restore_state(self: Any) -> None:
        """
        Restore persisted state if supported.
        """
        ...

    def save_state(self: Any) -> None:
        """
        Persist tracker state if supported.
        """
        ...

    def update(self: Any, detections: List[Any], stream_info: Optional[Dict[str, Any]] = None) -> List[Any]:
        """
        Attach ``track_id`` to each detection dict.
        """
        ...


# From config
class MatriceTrackerConfig:
    # Unified config passed from use cases into tracker adapters.

    def from_config(cls: Any, config: Any, stream_info: Optional[Dict[str, Any]] = None) -> Any:
        """
        Build tracker config from a use-case config object.
        """
        ...


# From integration
class ConfigDrivenTracker:
    # Lazy-init tracker selected by ``config.tracking_method``.

    def __init__(self: Any) -> None: ...

    def apply(self: Any, detections: List[Any], config: Any, stream_info: Optional[Dict[str, Any]] = None) -> List[Any]:
        """
        Run tracking when enabled on ``config``; otherwise return detections unchanged.
        """
        ...

    def get_shared_tracker(self: Any, config: Any = None, stream_info: Optional[Dict[str, Any]] = None, **overrides: Any) -> Optional[Any]:
        """
        Lazily construct (or return the cached) `AdvancedTracker` for this
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
        ...

    def is_initialized(self: Any) -> bool: ...

    def reset(self: Any) -> None: ...


# From integration
class TrackerProfile:
    # Named `TrackerConfig` baselines measured across the 136 literal
    #     `TrackerConfig(...)` call sites in usecases/ (consolidation plan §1.8).
    #     An enum + `**overrides` on `build_tracker_config`, not a 136-row config
    #     table — the drift is 4 real profiles plus 4 bespoke outliers, and a
    #     table keyed by use-case name would need to be kept in sync with the file
    #     list forever.

    DEFAULT: str
    FACE: str
    LEGACY_40: str
    NEW_FLOW: str


from . import base, config, det_utils, factory, integration