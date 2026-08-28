"""Stub file for analytics.processors directory."""
from typing import Any, Dict, List, Optional, Set

from ..base_processor import BaseMetricProcessor
from ..base_processor import BaseMetricProcessor, MetricEntry
from ..geometry import create_counter_from_zone_config, denormalize_zone_config
from ..incident_lifecycle import IncidentLifecycle
from ..quant_strategies import compute_quant
from ..schemas import MetricEntry, ProcessorAggregationOutput
from ..schemas import ProcessorAggregationOutput
from ..schemas import SEVERITY_ORDER, IncidentEvent, IncidentFrameResult, IncidentLifecycleState, IncidentProcessorConfig, IncidentThreshold, IncidentTypeConfig, LifecycleConfig, QuantStrategyConfig, SeverityLevel

# Constants
logger: Any = ...  # From identity
logger: Any = ...  # From incident
logger: Any = ...  # From quality
logger: Any = ...  # From safety
logger: Any = ...  # From volume

# Functions
# From incident
def calculate_severity(incident_quant: float, thresholds: list[dict[str, Any]], order: str = 'ascending') -> Any:
    """
    Determine severity from *incident_quant* using *thresholds*.
    
        For ascending order (higher quant = more severe): returns the highest
        level whose ``percentage`` is <= *incident_quant*.
    
        Args:
            incident_quant: Quantitative incident measurement (0-100).
            thresholds: List of ``{"level": str, "percentage": float}`` dicts.
            order: ``"ascending"`` or ``"descending"``.
    
        Returns:
            Resolved :class:`SeverityLevel`.
    """
    ...

# Classes
# From identity
class IdentityProcessor:
    # IDENTITY category processor for LPR / FR analytics.

    def __init__(self: Any, category: str, manifest_config: dict[str, Any], zone_id: str = '') -> None:
        """
        Initialise IdentityProcessor.
        
                Args:
                    category: Passed by the engine; always overridden to ``"IDENTITY"``.
                    manifest_config: Full parsed manifest dict from the YAML config.
                    zone_id: Optional zone name when running per-zone analytics.
                        Empty string means global (no zone).
        """
        ...

    def aggregate_1min(self: Any) -> Any:
        """
        Aggregate buffered frames into window-level IDENTITY metrics.
        
                Emits window-unique counts based on confirmed track IDs rather
                than summed frame counts, so the same plate visible for 100
                frames counts as 1 identification.
        """
        ...

    def reset(self: Any) -> None: ...


# From incident
class IncidentProcessor:
    # Standalone INCIDENT category processor.
    #
    #     No metrics, no aggregation, no inheritance from ``BaseMetricProcessor``.
    #     Delegates quant computation to :func:`compute_quant` and lifecycle
    #     management to :class:`IncidentLifecycle`.  Configured from a YAML
    #     manifest via :class:`IncidentProcessorConfig`.
    #
    #     Args:
    #         manifest_config: Full parsed manifest dict (same structure loaded
    #             from ``fire_detection.yaml``, ``weapon_detection.yaml``, etc.).

    def __init__(self: Any, manifest_config: dict[str, Any]) -> None:
        """
        Initialize from a parsed YAML manifest dict.
        """
        ...

    def drain_events(self: Any) -> list[Any]:
        """
        Return and clear all pending incident events (Pydantic models).
        """
        ...

    def get_lifecycle_state(self: Any, camera_id: str) -> Any | None:
        """
        Return a copy of the lifecycle state for *camera_id*.
        """
        ...

    def process_frame(self: Any, detections: list[dict[str, Any]], frame_ts: float, frame_id: str = '') -> Any:
        """
        Process one frame of detections through the incident pipeline.
        
                1. Filter detections by entity mapping.
                2. Compute ``incident_quant`` via the configured quant strategy.
                3. Resolve severity from thresholds.
                4. Run the lifecycle state machine (consecutive-frame validation).
                5. Return an :class:`IncidentFrameResult` snapshot.
        
                Emitted :class:`IncidentEvent` objects are buffered internally and
                retrieved via :meth:`drain_events`.
        """
        ...

    def reset(self: Any) -> None:
        """
        Full reset — clears lifecycle state, pending events, and overrides.
        """
        ...

    def update_thresholds(self: Any, camera_id: str, thresholds: list[dict[str, Any]], incident_type: str = '') -> None:
        """
        Set runtime threshold overrides for a camera.
        
                Maps backend ``"high"`` to internal ``"significant"`` on input.
        """
        ...


# From quality
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


# From safety
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


# From volume
class VolumeProcessor:
    # VOLUME category processor for counting-based analytics.
    #
    #     Computes per-frame metrics (entry_count, exit_count, current_occupancy)
    #     and aggregation-time metrics (peak_count, unique_count, turnover_rate).
    #
    #     When geometry (zone_config) is set via ``set_zone_config()``, entry/exit
    #     counts are derived from line-crossing or polygon-based counters. Otherwise,
    #     falls back to simple track-ID counting.
    #
    #     Window-level aggregation mirrors ``AnalyticsPublisher`` semantics:
    #
    #     - **current_counts** = SUM of per-frame ``current_new_counts``
    #       (new arrivals in the 1-min window).
    #     - **total_current_counts** = previous window's last-frame occupancy
    #       + accumulated new arrivals (0 carry on first window).
    #     - **total_counts** = cumulative unique since last full reset.

    def __init__(self: Any, category: str, manifest_config: dict[str, Any], zone_id: str = '') -> None:
        """
        Initialize VolumeProcessor, ignoring ``category`` in favour of "VOLUME".
        
                Args:
                    category: Passed by the engine; always overridden to ``"VOLUME"``.
                    manifest_config: Full parsed manifest dict from the YAML config file.
                    zone_id: Optional zone name when running per-zone analytics.
                        Empty string means global (no zone).
        """
        ...

    def has_geometry(self: Any) -> bool:
        """
        Whether a geometry counter is active.
        """
        ...

    def remove_zone_config(self: Any) -> None:
        """
        Remove geometry config and revert to simple track-ID counting.
        """
        ...

    def reset(self: Any) -> None:
        """
        Full reset including VOLUME-specific state.
        """
        ...

    def set_zone_config(self: Any, zone_config: dict[str, Any], width: int, height: int, method: str = 'abline', in_direction: str = 'A_to_B', use_foot_center: bool = False) -> None:
        """
        Set geometry and create a counting counter for entry/exit analytics.
        
                After calling this, ``_compute_frame_metrics`` will use the geometry
                counter instead of simple track-ID counting.
        
                Args:
                    zone_config: Dict with ``"lines"`` and/or ``"zones"`` in normalized
                        (0-1) coordinates, matching the Matrice post-processing API format.
                    width: Frame width in pixels (for denormalization).
                    height: Frame height in pixels (for denormalization).
                    method: ``"abline"`` (two-line trap zone) or ``"polygon"``
                        (double-polygon hysteresis).
                    in_direction: For abline method -- ``"A_to_B"`` or ``"B_to_A"``.
                    use_foot_center: Use bottom-center of bbox instead of center.
        """
        ...


from . import identity, incident, quality, safety, volume