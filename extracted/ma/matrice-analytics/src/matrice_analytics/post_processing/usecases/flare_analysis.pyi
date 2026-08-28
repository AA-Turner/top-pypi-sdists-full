"""Auto-generated stub for module: flare_analysis."""
from typing import Any, Dict, List, Optional

from ..Trackers import ConfigDrivenTracker, TrackerProfile
from ..core.base import BaseProcessor, ConfigProtocol, ProcessingContext, ProcessingResult
from ..core.config import AlertConfig, BaseConfig
from ..utils import BBoxSmoothingConfig, BBoxSmoothingTracker, apply_category_mapping, bbox_smoothing, filter_by_categories, filter_by_confidence, match_results_structure

# Classes
class FlareAnalysisConfig:
    # Configuration for flare analysis use case.

    def validate(self: Any) -> List[str]: ...

class FlareAnalysisUseCase:
    # Flare analysis processor. The model classifies each detection directly as
    #     GoodFlare (clean combustion) or BadFlare (smoke present, incomplete
    #     combustion); this usecase counts, tracks, and grades incident severity from
    #     those categories -- it does not do any of its own image analysis.

    def __init__(self: Any) -> None: ...

    CATEGORY_DISPLAY: Dict[Any, Any]

    def create_default_config(self: Any, **overrides: Any) -> Any: ...

    def get_config_schema(self: Any) -> Dict[str, Any]: ...

    def get_new_counts_this_frame(self: Any) -> Dict[str, int]:
        """
        Return count of NEW track_ids per category this frame.
        """
        ...

    def get_total_counts(self: Any) -> Any: ...

    def process(self: Any, data: Any, config: Any, input_bytes: Optional[Any] = None, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any: ...

    def reset_all_tracking(self: Any) -> None: ...

    def reset_flare_tracking(self: Any) -> None: ...

    def reset_tracker(self: Any) -> None: ...

