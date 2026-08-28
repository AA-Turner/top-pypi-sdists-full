"""Auto-generated stub for module: quant_strategies."""
from typing import Any

from .schemas import QuantStrategyConfig

# Constants
QuantFn: Any
logger: Any

# Functions
def compute_quant(detections: list[dict[str, Any]], config: Any) -> tuple[float, float]:
    """
    Compute ``(incident_quant, event_confidence)`` using the configured strategy.
    
        Falls back to ``max_confidence`` if the strategy name is not recognised.
    
        Args:
            detections: Filtered detection dicts for this frame.
            config: Strategy selection and parameters from the YAML manifest.
    
        Returns:
            ``(incident_quant, event_confidence)`` tuple.
    """
    ...
