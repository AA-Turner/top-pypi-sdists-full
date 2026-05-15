"""Auto-generated stub for module: databus_status."""
from typing import Any, Dict, List, Optional

# Constants
SHM_BASE_PATH: Any
STALE_THRESHOLD_NS: int
STATUS_PREFIX: str
logger: Any

# Classes
class NodeStatus:
    # Per-node SHM status file.
    #
    #     Each node owns exactly one file — no write contention.

    def __init__(self: Any, node_id: str) -> None: ...

    def heartbeat(self: Any) -> None:
        """
        Fast-path: update only last_heartbeat_ns in existing status.
        """
        ...

    def is_stale(status_dict: Dict, threshold_ns: int = STALE_THRESHOLD_NS) -> bool:
        """
        Check if a node's status is stale (no heartbeat within threshold).
        
                Args:
                    status_dict: Status dict from read() or read_all()
                    threshold_ns: Stale threshold in nanoseconds (default 30s)
        
                Returns:
                    True if last heartbeat is older than threshold.
        """
        ...

    def read(node_id: str) -> Optional[Dict]:
        """
        Read one node's status by ID.
        
                Returns:
                    Status dict or None if not found/corrupt.
        """
        ...

    def read_all() -> List[Dict]:
        """
        Read all node status files.
        
                Returns:
                    List of status dicts for all active nodes.
        """
        ...

    def remove(self: Any) -> None:
        """
        Delete status file on graceful shutdown.
        """
        ...

    def write(self: Any, status: str = 'alive', model_loaded: bool = False, buffer_addresses: Optional[List[str]] = None, **extra: Any) -> None:
        """
        Write full status. Creates file if needed.
        """
        ...

