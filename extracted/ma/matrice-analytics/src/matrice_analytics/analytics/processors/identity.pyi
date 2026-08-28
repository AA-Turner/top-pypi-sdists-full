"""Auto-generated stub for module: identity."""
from typing import Any, Optional

from ..base_processor import BaseMetricProcessor, MetricEntry
from ..schemas import ProcessorAggregationOutput

# Constants
logger: Any

# Classes
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

