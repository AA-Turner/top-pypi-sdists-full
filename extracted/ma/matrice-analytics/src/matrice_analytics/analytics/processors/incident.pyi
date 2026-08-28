"""Auto-generated stub for module: incident."""
from typing import Any, List, Set

from ..incident_lifecycle import IncidentLifecycle
from ..quant_strategies import compute_quant
from ..schemas import SEVERITY_ORDER, IncidentEvent, IncidentFrameResult, IncidentLifecycleState, IncidentProcessorConfig, IncidentThreshold, IncidentTypeConfig, LifecycleConfig, QuantStrategyConfig, SeverityLevel

# Constants
logger: Any

# Functions
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

