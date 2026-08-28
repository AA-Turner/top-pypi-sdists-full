"""Auto-generated stub for module: quality."""
from typing import Any, Optional

from ..base_processor import BaseMetricProcessor, MetricEntry
from ..schemas import ProcessorAggregationOutput

# Constants
logger: Any

# Classes
class QualityProcessor:
    # QUALITY category processor for defect-detection analytics.
    #
    #     Per-frame metrics (from ``_compute_frame_metrics``):
    #
    #     - **defect_count**: number of defect-class detections in this frame.
    #     - **total_inspected**: number of inspection-class detections in this
    #       frame (e.g. bottles currently visible).
    #     - **defect_rate**: ``defect_count / total_inspected`` for this frame.
    #
    #     1-minute aggregation (from ``aggregate_1min``, overridden):
    #
    #     - **defect_count**: unique defect track IDs confirmed in the 60s window.
    #     - **total_inspected**: unique inspection-class track IDs confirmed in
    #       the 60s window.
    #     - **defect_rate**: ``unique_defects / unique_inspected`` (window-level).
    #
    #     The YAML manifest's ``quality.metrics`` section controls which keys
    #     are emitted.  ``quality.inspection_classes`` and
    #     ``quality.defect_classes`` configure which entity names count as
    #     inspected items vs defects.

    def __init__(self: Any, category: str, manifest_config: dict[str, Any], zone_id: str = '') -> None:
        """
        Initialise QualityProcessor.
        
                Args:
                    category: Passed by the engine; always overridden to ``"QUALITY"``.
                    manifest_config: Full parsed manifest dict from the YAML config.
                    zone_id: Optional zone name when running per-zone analytics.
                        Empty string means global (no zone).
        """
        ...

    def aggregate_1min(self: Any) -> Any:
        """
        Aggregate buffered frames into window-level QUALITY metrics.
        
                Overrides the base class's default averaging behaviour because
                ``defect_rate`` must be computed on window-level uniques, not as
                a mean of per-frame rates.
        
                Emits:
                    - ``defect_count``    = unique defect track IDs confirmed in window.
                    - ``total_inspected`` = unique inspection-class track IDs confirmed in window.
                    - ``defect_rate``     = unique_defects / unique_inspected.
        
                QUALITY processors do not emit ``tracking_stats``; only VOLUME does.
        """
        ...

    def reset(self: Any) -> None:
        """
        Full reset including QUALITY-specific state.
        """
        ...

