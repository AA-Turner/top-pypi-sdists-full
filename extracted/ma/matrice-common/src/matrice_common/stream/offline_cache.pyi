"""Auto-generated stub for module: offline_cache."""
from typing import Any, Callable, Dict, List, Optional

# Constants
DEFAULT_CHECK_INTERVAL: Any
DEFAULT_FLUSH_BATCH_SIZE: Any
DEFAULT_MAX_SIZE: Any
DEFAULT_TTL_SECONDS: Any
logger: Any

# Classes
class DeviceInfo:
    # Tracked state for a single device.

    ...
class DeviceState:
    OFFLINE: str
    ONLINE: str
    UNKNOWN: str

class OfflineRequestCache:
    # Store-and-forward cache that queues requests for offline devices.
    #
    #     When a device goes offline (detected via health_check_fn or send failure),
    #     subsequent requests are queued in memory. When the device comes back online,
    #     queued requests are flushed in order.
    #
    #     Args:
    #         send_fn: Callable(device_id, payload) -> bool. Returns True on success.
    #         health_check_fn: Optional callable(device_id) -> bool. Returns True if online.
    #             If not provided, online/offline is inferred from send_fn success/failure.
    #         max_size: Maximum total queued requests across all devices.
    #         ttl_seconds: Per-request TTL. Expired requests are discarded.
    #         flush_batch_size: Max requests to flush per cycle per device.
    #         check_interval: Seconds between health check cycles.

    def __init__(self: Any, send_fn: Callable[[str, Any], bool], health_check_fn: Optional[Callable[[str], bool]] = None, max_size: int = DEFAULT_MAX_SIZE, ttl_seconds: float = DEFAULT_TTL_SECONDS, flush_batch_size: int = DEFAULT_FLUSH_BATCH_SIZE, check_interval: float = DEFAULT_CHECK_INTERVAL) -> None: ...

    def device_status(self: Any, device_id: str) -> str:
        """
        Get current status of a device.
        """
        ...

    def get_stats(self: Any) -> Dict[str, Any]:
        """
        Get cache statistics.
        """
        ...

    def get_warnings(self: Any, clear: bool = True) -> List[Dict[str, Any]]:
        """
        Get and optionally clear accumulated warnings.
        """
        ...

    def start(self: Any) -> None:
        """
        Start the background health-check and flush thread.
        """
        ...

    def stop(self: Any, flush_timeout: float = 5.0) -> None:
        """
        Stop monitoring and attempt final flush of queued requests.
        """
        ...

    def submit(self: Any, device_id: str, payload: Any) -> bool:
        """
        Submit a request for a device.
        
                If the device is online, sends immediately. If offline or send fails,
                queues the request for later delivery.
        
                Returns:
                    True if sent immediately, False if queued.
        """
        ...

class QueuedRequest:
    # A request waiting to be sent when the target comes back online.

    def is_expired(self: Any, ttl: float) -> bool: ...

