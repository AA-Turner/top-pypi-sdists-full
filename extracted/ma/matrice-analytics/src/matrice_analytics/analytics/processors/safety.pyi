"""Auto-generated stub for module: safety."""
from typing import Any, Optional

from ..base_processor import BaseMetricProcessor
from ..schemas import MetricEntry, ProcessorAggregationOutput

# Constants
logger: Any

# Classes
class SafetyProcessor:
    # SAFETY category processor for PPE compliance analytics.
    #
    #     Per-frame metrics (``_compute_frame_metrics``):
    #
    #     - **total_persons**: number of person detections in this frame.
    #     - **compliant_count**: persons wearing all ``required_ppe`` items.
    #     - **violation_count**: persons missing any required PPE (or with
    #       a direct violation-class detection).
    #     - **compliance_pct**: ``compliant_count / total_persons * 100`` for
    #       the current frame (0.0 when no persons).
    #     - **<item>_count**: one entry per configured PPE item (e.g.
    #       ``hardhat_count``, ``vest_count``).
    #
    #     1-minute aggregation (``aggregate_1min`` override):
    #
    #     - ``total_persons``      = unique person track IDs confirmed in window.
    #     - ``violation_count``    = unique violator track IDs in window.
    #     - ``compliance_pct``     = mean of per-frame compliance_pct values.
    #     - ``<item>_count``       = unique track IDs per PPE item in window.
    #
    #     YAML manifest (``safety:`` section) drives:
    #
    #     - ``person_classes``:     entity names counted as persons.
    #     - ``ppe_classes``:        entity names recognised as PPE items.
    #     - ``required_ppe``:       subset of ``ppe_classes`` that MUST be worn.
    #     - ``violation_classes``:  entity names that directly indicate a
    #                               violation (model-emitted ``NO-*`` labels).
    #     - ``metrics``:            which metric keys to emit (same shape as
    #                               other processors).

    def __init__(self: Any, category: str, manifest_config: dict[str, Any], zone_id: str = '') -> None:
        """
        Initialise SafetyProcessor.
        
                Args:
                    category: Passed by the engine; always overridden to ``"SAFETY"``.
                    manifest_config: Full parsed manifest dict.
                    zone_id: Optional zone name when running per-zone analytics.
                        Empty string means global (no zone).
        """
        ...

    def aggregate_1min(self: Any) -> Any:
        """
        Aggregate buffered frames into window-level SAFETY metrics.
        
                Window semantics (design doc §3.7):
                  - ``compliance_pct``  — mean of per-frame values.
                  - ``total_persons``   — unique confirmed person track IDs.
                  - ``violation_count`` — unique confirmed violator track IDs.
                  - ``<item>_count``    — unique confirmed track IDs per PPE item.
                  - ``compliant_count`` — ``total_persons - violation_count``
                                          (conservative window-level derivation).
        
                SAFETY does not emit ``tracking_stats`` (only VOLUME does).
        """
        ...

    def reset(self: Any) -> None:
        """
        Full reset including SAFETY-specific state.
        """
        ...

