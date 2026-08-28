"""Auto-generated stub for module: accident_detection."""
from typing import Any, Dict, Optional

from ..core.base import BaseProcessor, ConfigProtocol, ProcessingContext, ProcessingResult, ResultFormat
from ..core.config import AlertConfig, BaseConfig
from ..utils import apply_category_mapping, filter_by_confidence

# Classes
class AccidentDetectionConfig:
    # Configuration for accident detection post-processing (X3D classifier).

    ...
class AccidentDetectionUseCase:
    # Post-processor for X3D accident-classification model outputs.

    def __init__(self: Any) -> None: ...

    def get_current_frame_counts(self: Any) -> Dict[str, int]:
        """
        Return 1 for categories with a currently-confirmed episode.
        """
        ...

    def get_new_counts_this_frame(self: Any) -> Dict[str, int]:
        """
        Return 1 for categories whose episode was newly confirmed this frame.
        """
        ...

    def get_total_counts(self: Any) -> Dict[str, int]:
        """
        Return cumulative confirmed-episode counts per category.
        """
        ...

    def process(self: Any, data: Any = None, config: Any = None, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any:
        """
        Run the accident-classification post-processing pipeline for one frame.
        
                Args:
                    data: Raw X3D classification output for this frame (see module
                        docstring for shape).
                    config: Must be an :class:`AccidentDetectionConfig` instance.
                    context: Optional processing context carrying metadata.
                    stream_info: Stream/video metadata used for timestamps and the
                        debounce clock (``stream_time`` / ``original_fps``).
        
                Returns:
                    :class:`ProcessingResult` containing the ``agg_summary`` payload.
        """
        ...

