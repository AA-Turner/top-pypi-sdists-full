"""Auto-generated stub for module: databus_batch_consumer."""
from typing import Any, Dict, List, Union

from .databus import DataBus, DataBusConsumer, DataFormat, _parse_format

# Constants
BatchItem: Any
logger: Any

# Classes
class BatchConsumer:
    # Multi-channel batched consumer with dynamic batching and timeout.
    #
    #     Collects from multiple DataBus channels using round-robin with adaptive
    #     polling. Returns partial batches on timeout (never blocks forever).

    def __init__(self: Any, addresses: List[str], consumer_key: str, format: Union[str, Any]) -> None: ...

    def ack_batch(self: Any, items: List[Any]) -> None:
        """
        Acknowledge all items in a batch.
        
                Args:
                    items: List of (data, metadata, address) tuples from collect_batch()
        """
        ...

    def add_channel(self: Any, address: str) -> bool:
        """
        Dynamically add a channel.
        
                Args:
                    address: Full DataBus address (e.g., /dev/shm/databus__cam__node__port)
        
                Returns:
                    True if connection succeeded
        """
        ...

    def addresses(self: Any) -> List[str]:
        """
        List of all registered addresses (connected or not).
        """
        ...

    def channel_count(self: Any) -> int:
        """
        Number of connected channels.
        """
        ...

    def close(self: Any) -> None:
        """
        Close all consumer connections and cleanup.
        """
        ...

    def collect_batch(self: Any, max_batch: int = 64, timeout_ms: float = 10.0) -> List[Any]:
        """
        Collect up to max_batch items across all channels.
        
                Implements dynamic batching:
                - Collects items until max_batch reached OR timeout expires
                - Returns early if full batch collected
                - Returns whatever items are available on timeout (even 1 item)
                - Round-robin across channels for fair scheduling
        
                Args:
                    max_batch: Maximum items to collect
                    timeout_ms: Maximum wait time in milliseconds (0 = no timeout)
        
                Returns:
                    List of (data, metadata, address) tuples
        """
        ...

    def connect(self: Any) -> bool:
        """
        Connect to all channels.
        
                Returns:
                    True if at least one channel connected successfully.
        """
        ...

    def connected(self: Any) -> bool:
        """
        True if at least one channel is connected.
        """
        ...

    def get_lag(self: Any) -> Dict[str, int]:
        """
        Get per-channel consumer lag (frames behind).
        
                Only works for CUDA IPC consumers that expose get_frames_behind().
                Returns 0 for POSIX SHM consumers (no native lag tracking).
        """
        ...

    def remove_channel(self: Any, address: str) -> None:
        """
        Dynamically remove a channel.
        
                Args:
                    address: Full DataBus address to remove
        """
        ...

