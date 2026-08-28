"""Auto-generated stub for module: people_counting."""
from typing import Any, Dict, Optional

from ..Trackers import ConfigDrivenTracker, TrackerProfile
from ..core.base import BaseProcessor, ConfigProtocol, ProcessingContext, ProcessingResult
from ..core.config import PeopleCountingConfig
from ..core.config import ZoneConfig
from ..utils import apply_category_mapping, count_objects_in_zones, filter_by_confidence, get_bbox_bottom_center, match_results_structure, point_in_polygon
from ..utils.post_processing_config_client import GEOMETRY_RETRY_INTERVAL, PostProcessingConfigClient

# Classes
class PeopleCountingUseCase:
    def __init__(self: Any) -> None: ...

    CATEGORY_DISPLAY: Dict[Any, Any]

    def get_current_frame_counts(self: Any) -> Dict[str, int]:
        """
        Get count of ALL track IDs currently in this frame (existing + new).
        """
        ...

    def get_new_counts_this_frame(self: Any) -> Dict[str, int]:
        """
        Get count of CONFIRMED new track IDs reported for the first time this frame.
        
                A track is only counted as "new" when it has been present in the tracker
                output for at least ``min_hits_for_new_track`` consecutive output frames
                (default 3). Short dropouts are tolerated via a soft-decay counter (a
                one-frame miss reduces the counter by 1 instead of resetting to 0).
                This filters out:
                  - Spurious short-lived detections (noise, reflections, shadows)
                  - Brief ID switches caused by tracker matching failures
                  - Flickering detections near the confidence threshold
        
                Each track ID is reported as new **exactly once** across all frames.
                Subsequent frames will return 0 for that track even though it is still
                visible.  This makes downstream aggregation (summing over N seconds)
                produce the correct total of genuinely new people.
        """
        ...

    def get_total_counts(self: Any) -> Any: ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any:
        """
        Process one frame of detections and return ``agg_summary``.
        
                ``agg_summary`` structure (keyed by frame_number)::
        
                    {
                      "<frame>": {
                        "incidents":        { ... severity + zone breakdown ... },
                        "tracking_stats":   {
                          "total_counts":         [{"category": "person", "count": N}],
                          "current_counts":       [...],
                          "current_new_counts":   [...],
                          "detections":           [...],
                          "zone_analysis":        { ... per-zone track counts ... },
                          ...
                        },
                        "business_analytics": {},
                        "alerts":           [...],
                        "zone_analysis":    { ... per-zone track counts ... },
                        "human_text":       "..."
                      }
                    }
        
                Zone behaviour
                --------------
                * When zones are configured (via API or ``PeopleCountingConfig.zone_config``),
                  ``zone_analysis`` contains per-zone current/total track counts.
                * When no zones are configured, ``zone_analysis`` contains a single
                  ``"__global__"`` key covering the entire frame.
                * The existing overall counting logic (total_counts, current_counts,
                  new_counts) is **not modified** — zone_analysis is additive output.
        """
        ...

    def set_config_client(self: Any, client: Optional[Any]) -> None:
        """
        Inject a ``PostProcessingConfigClient`` for API-based zone resolution.
        
                Must be called before the first ``process()`` invocation.  When a
                client is provided the use case resolves zone polygons drawn in the
                Matrice UI, falling back to ``zone_config`` in ``PeopleCountingConfig``
                if the API is unavailable.
        """
        ...

