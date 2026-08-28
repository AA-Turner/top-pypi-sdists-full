"""Auto-generated stub for module: config."""
from typing import Any, Dict, Optional

# Constants
SUPPORTED_TRACKING_METHODS: Any

# Classes
class MatriceTrackerConfig:
    # Unified config passed from use cases into tracker adapters.

    def from_config(cls: Any, config: Any, stream_info: Optional[Dict[str, Any]] = None) -> Any:
        """
        Build tracker config from a use-case config object.
        """
        ...

