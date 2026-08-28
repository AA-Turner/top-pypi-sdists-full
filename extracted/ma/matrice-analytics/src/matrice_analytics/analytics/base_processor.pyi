"""Auto-generated stub for module: base_processor."""
from typing import Any

from .schemas import BoundingBox, DetectionEntry, MetricEntry, ProcessorAggregationOutput, ProcessorFrameOutput

# Constants
logger: Any

# Classes
class BaseMetricProcessor:
    # Abstract base for all category processors.
    #
    #     Subclasses must implement ``_compute_frame_metrics()`` and optionally
    #     override ``_compute_category_metrics()`` for aggregation-time extras.

    def __init__(self: Any, category: str, manifest_config: dict[str, Any]) -> None:
        """
        Initialize the processor with a category name and manifest config.
        
                Args:
                    category: The analytics category string (e.g. "VOLUME", "INCIDENT").
                    manifest_config: Full parsed manifest dict from the YAML config file.
        """
        ...

    def aggregate_1min(self: Any) -> Any:
        """
        Aggregate buffered frames into metrics and optional VOLUME ``tracking_stats``.
        
                Returns a processor chunk; ``AnalyticsEngine.aggregate`` merges chunks
                into the full publisher-shaped ``AggregationResult``.
        """
        ...

    def process_frame(self: Any, detections: list[dict[str, Any]], frame_ts: float, frame_id: str = '') -> Any:
        """
        Process a single frame of detections.
        
                Template method:
                  1. ``_pre_process``  — filter to target categories
                  2. ``_update_track_counts`` — update track-ID sets
                  3. ``_compute_frame_metrics`` — subclass hook (returns metrics)
                  4. Build ``ProcessorFrameOutput`` with business_analytics, human_text, etc.
        
                The engine is responsible for assembling the final ``FrameResult``
                envelope from outputs of all processors.
        """
        ...

    def reset(self: Any) -> None:
        """
        Full reset — clears all state including cumulative track IDs.
        """
        ...

