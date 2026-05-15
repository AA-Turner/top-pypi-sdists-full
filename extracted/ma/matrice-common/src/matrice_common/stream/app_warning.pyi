"""Auto-generated stub for module: app_warning."""
from typing import Any, Callable, Dict, List

from .databus_status import STALE_THRESHOLD_NS, NodeStatus

# Constants
DEFAULT_CHECK_INTERVAL: Any
DEFAULT_STALE_THRESHOLD_SEC: Any
logger: Any

# Classes
class AppWarningManager:
    # Monitors DataBus pipeline nodes and emits warnings on state changes.
    #
    #     Uses NodeStatus SHM heartbeat files for zero-overhead health checking.
    #     Warning callbacks are invoked on the monitor thread — keep handlers fast.
    #
    #     Args:
    #         check_interval: Seconds between health check sweeps.
    #         stale_threshold_sec: Seconds without heartbeat before a node is stale.

    def __init__(self: Any, check_interval: float = DEFAULT_CHECK_INTERVAL, stale_threshold_sec: float = DEFAULT_STALE_THRESHOLD_SEC) -> None: ...

    def get_node_states(self: Any) -> Dict[str, Dict[str, Any]]:
        """
        Get current state of all monitored nodes.
        """
        ...

    def get_warnings(self: Any, clear: bool = True) -> List[Dict[str, Any]]:
        """
        Get accumulated warnings, optionally clearing the buffer.
        """
        ...

    def is_node_online(self: Any, node_id: str) -> bool:
        """
        Check if a specific node is online.
        """
        ...

    def on_warning(self: Any, callback: Callable[[Dict[str, Any]], None]) -> None:
        """
        Register a callback for warning events.
        
                Callback receives a dict with keys: timestamp, node_id, type, message, details.
                Warning types: DEVICE_OFFLINE, DEVICE_ONLINE, DEVICE_STALE, NODE_DISCOVERED.
        """
        ...

    def start(self: Any) -> None:
        """
        Start the background monitoring thread.
        """
        ...

    def stop(self: Any) -> None:
        """
        Stop the monitoring thread.
        """
        ...

class NodeState:
    # Internal tracking state for a monitored node.

    ...
