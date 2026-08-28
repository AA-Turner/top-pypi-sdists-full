"""Auto-generated stub for module: vehicle_segmentation."""
from typing import Any, Dict, Optional

from ..Trackers import ConfigDrivenTracker, TrackerProfile
from ..core.base import BaseProcessor, ConfigProtocol, ProcessingContext, ProcessingResult
from ..core.config import AlertConfig, BaseConfig
from ..utils import AgnosticNMS, apply_category_mapping, filter_by_confidence, match_results_structure

# Classes
class VehicleSegmentationConfig:
    # Configuration for vehicle segmentation post-processing.

    ...
class VehicleSegmentationUseCase:
    # Post-processor for vehicle segmentation model outputs.

    def __init__(self: Any) -> None: ...

    def get_new_counts_this_frame(self: Any) -> Dict[str, int]:
        """
        Vehicles per category that appeared for the first time in the current frame.
        """
        ...

    def get_total_counts(self: Any) -> Dict[str, int]:
        """
        Cumulative unique vehicle count per category, across all frames seen so far.
        """
        ...

    def process(self: Any, data: Any = None, config: Any = None, context: Any | None = None, stream_info: Dict[str, Any] | None = None) -> Any:
        """
        Run vehicle segmentation post-processing on one frame.
        
                Args:
                    data: Raw model output — either the backend dual-port
                        ``{"detection0": ..., "mask0": ...}`` payload or an
                        already-flat detection list.
                    config: Must be a :class:`VehicleSegmentationConfig` instance.
                    context: Optional processing context carrying metadata.
                    stream_info: Stream/video metadata used for frame numbering.
        
                Returns:
                    :class:`ProcessingResult` containing an ``agg_summary`` payload
                    whose detections carry only encoded segmentation values.
        """
        ...

