"""Auto-generated stub for module: dwell_detection."""
from typing import Any, Dict, Optional

from ..Trackers import ConfigDrivenTracker, TrackerProfile
from ..core.base import BaseProcessor, ConfigProtocol, ProcessingContext, ProcessingResult
from ..core.config import AlertConfig, BaseConfig
from ..utils import BBoxSmoothingConfig, BBoxSmoothingTracker, apply_category_mapping, bbox_smoothing, count_objects_in_zones, filter_by_confidence, get_bbox_bottom_center, match_results_structure, point_in_polygon
from ..utils.incident_manager_utils import INCIDENT_MANAGER, IncidentManagerFactory
from ..utils.post_processing_config_client import GEOMETRY_RETRY_INTERVAL
from ..utils.post_processing_config_client import PostProcessingConfigClient

# Classes
class DwellConfig:
    # Configuration for dwell detection use case.
    #
    #     All time-sensitive thresholds are expressed in **wall-clock seconds** so
    #     they are independent of the inference frame-rate.  The system is called
    #     once per inferred frame (which may be every 1st, 3rd, 10th, or any Nth
    #     video frame), so frame-count-based thresholds are inherently unreliable.
    #
    #     Key thresholds
    #     --------------
    #     dwell_threshold
    #         Continuous stationary wall-clock **seconds** before a person is
    #         labelled ``Dweller``.  Default 5.0 s catches genuine dwell events
    #         while ignoring people who pause briefly while walking.
    #     loitering_time_threshold_seconds
    #         Wall-clock seconds of continuous dwelling after which a per-person
    #         dwell alert is fired exactly once per track per session.  Defaults to
    #         60 s (1 minute).
    #     centroid_threshold
    #         Maximum Euclidean **pixel** displacement between successive process()
    #         calls for a person to be considered stationary.  Frame-rate agnostic
    #         because it measures spatial distance, not temporal distance.
    #     stale_track_frames
    #         Wall-clock **seconds** of continuous absence before a track is evicted
    #         from the stationary-tracks registry.  (Name kept for API compatibility;
    #         the value is now in seconds.)  Default 3 s survives brief occlusions
    #         and zone-boundary jitter.
    #     movement_penalty
    #         Wall-clock **seconds** subtracted from a track's accumulated stationary
    #         time when movement is detected.  (Name kept for API compatibility;
    #         the value is now in seconds.)  Gentle enough to survive natural weight
    #         shifts without resetting dwell progress entirely.
    #     zone_params
    #         Optional per-zone overrides for any threshold above.  When a key is
    #         absent for a given zone the global ``DwellConfig`` value is used as
    #         the default.  Populated automatically when resolving zones from the
    #         Matrice UI/API.
    #         Example::
    #
    #             {
    #               "shelf":    {"dwell_threshold": 8.0,
    #                            "loitering_time_threshold_seconds": 90.0},
    #               "checkout": {"stale_track_frames": 5.0,
    #                            "movement_penalty": 1.0}
    #             }

    ...
class DwellUseCase:
    # Per-frame dwell / loitering detector.
    #
    #     Tracks how long each detected person remains stationary inside configured
    #     zones and emits structured analytics with:
    #
    #     * Per-person dwell duration in seconds.
    #     * Per-zone unique-dweller counts and average dwell times.
    #     * Per-person dwell alerts when a person exceeds the zone-specific (or
    #       global) ``loitering_time_threshold_seconds``.
    #     * Zone geometry resolved from the Matrice UI/API (same pattern as
    #       ``HazardZoneEntryUseCase``) so operators can draw zones without
    #       re-deploying config files.

    def __init__(self: Any) -> None: ...

    CATEGORY_DISPLAY: Dict[Any, Any]

    def get_new_counts_this_frame(self: Any) -> Dict[str, int]:
        """
        Count of track ids reported for the FIRST time this frame, per category.
        """
        ...

    def get_total_counts(self: Any) -> Dict[str, int]:
        """
        Return cumulative unique counts for both ``"person"`` and ``"Dweller"``.
        
                ``"person"`` — every unique in-zone track ever seen while NOT yet
                dwelling, sourced from ``_per_category_total_track_ids["person"]``
                (populated by ``_update_tracking_state`` from ``presence_data``).
                ``"Dweller"`` — unique tracks ever promoted past the dwell threshold,
                sourced from ``_zone_unique_dwellers`` (populated by
                ``_check_dwell_objects()`` whenever a track crosses the threshold).
        
                Both keys are always present, defaulting to 0, so callers never need
                to guess whether a category was tracked yet.
        """
        ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any:
        """
        Process one frame of detections and return ``agg_summary``.
        
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
        ...

    def set_config_client(self: Any, client: Optional[Any]) -> None:
        """
        Inject a ``PostProcessingConfigClient`` for API-based zone resolution.
        
                Must be called before the first ``process()`` invocation.  When a
                client is provided the use case resolves zone polygons drawn in the
                Matrice UI, falling back to ``zone_config`` in ``DwellConfig`` if the
                API is unavailable.
        """
        ...

