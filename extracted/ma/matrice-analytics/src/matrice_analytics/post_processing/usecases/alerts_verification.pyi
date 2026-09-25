"""Auto-generated stub for module: alerts_verification."""
from typing import Any, Dict, Optional

from ..core.base import BaseProcessor, ConfigProtocol, ProcessingContext, ProcessingResult
from ..core.config import AlertConfig, BaseConfig
from ..utils import apply_category_mapping, filter_by_confidence, match_results_structure
from ..utils.incident_manager_utils import INCIDENT_MANAGER, IncidentManagerFactory

# Classes
class AlertsVerificationConfig:
    # Configuration for Alerts Verification.

    ...
class AlertsVerificationUseCase:
    # Raise a fire alert from a single detection, ready for remote verification.

    def __init__(self: Any) -> None: ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any:
        """
        Alert on this frame's fire, if any.
        """
        ...

