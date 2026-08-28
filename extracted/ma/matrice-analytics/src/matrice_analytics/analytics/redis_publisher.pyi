"""Auto-generated stub for module: redis_publisher."""
from typing import Any, Dict, Optional

# Constants
AGG_STREAM: str
INCIDENT_STREAM: str
logger: Any

# Classes
class AnalyticsRedisPublisher:
    # Lazy, per-process Redis publisher for incident_res + results-agg.

    def __init__(self: Any, config: Optional[Dict[str, Any]] = None) -> None: ...

    def publish_aggregation(self: Any, camera_id: str, payload: Dict[str, Any]) -> bool: ...

    def publish_incident(self: Any, camera_id: str, payload: Dict[str, Any]) -> bool: ...

