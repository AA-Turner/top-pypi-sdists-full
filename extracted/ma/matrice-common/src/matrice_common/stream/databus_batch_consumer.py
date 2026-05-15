"""BatchConsumer — Multi-channel batched consumer for DataBus.

Collects data from multiple DataBus channels with dynamic batching and timeout.
Replicates the FramePointerCollector.collect_batch_dynamic() pattern from
yolo_code_base/inference/frame_collector.py.

Usage:
    # Create consumers for multiple cameras
    addresses = [
        DataBus.compute_address(f"cam_{i}", "yolo", "detection0")
        for i in range(10)
    ]
    bc = BatchConsumer(addresses, consumer_key="analytics", format="json")
    bc.connect()

    # Collect batch with timeout
    batch = bc.collect_batch(max_batch=64, timeout_ms=10.0)
    for data, metadata, address in batch:
        process(data)
    bc.ack_batch(batch)

    # Dynamic add/remove
    bc.add_channel(DataBus.compute_address("cam_new", "yolo", "detection0"))
    bc.remove_channel(DataBus.compute_address("cam_old", "yolo", "detection0"))

    bc.close()
"""

import logging
import os
import time
from typing import Any, Dict, List, Optional, Tuple, Union

from .databus import DataBus, DataBusConsumer, DataFormat, _parse_format

logger = logging.getLogger(__name__)

# Type alias: (data, metadata, address)
BatchItem = Tuple[Any, Dict, str]


def _parse_address(address: str) -> Optional[Tuple[str, str, str]]:
    """Parse DataBus address into (camera_id, node_id, port_name).

    Args:
        address: Full path like /dev/shm/databus__{cam}__{node}__{port}

    Returns:
        (camera_id, node_id, port_name) or None if not a valid DataBus address
    """
    base = os.path.basename(address)
    if not base.startswith("databus__"):
        return None
    parts = base.split("__")
    if len(parts) != 4:  # "databus", camera_id, node_id, port_name
        return None
    return (parts[1], parts[2], parts[3])


class BatchConsumer:
    """Multi-channel batched consumer with dynamic batching and timeout.

    Collects from multiple DataBus channels using round-robin with adaptive
    polling. Returns partial batches on timeout (never blocks forever).
    """

    def __init__(
        self,
        addresses: List[str],
        consumer_key: str,
        format: Union[str, DataFormat],
        *,
        gpu_id: int = 0,
    ):
        self._addresses = list(addresses)
        self._consumer_key = consumer_key
        self._format = _parse_format(format)
        self._gpu_id = gpu_id
        self._consumers: Dict[str, DataBusConsumer] = {}
        self._connected = False

    def connect(self) -> bool:
        """Connect to all channels.

        Returns:
            True if at least one channel connected successfully.
        """
        for addr in self._addresses:
            self._try_connect(addr)
        self._connected = len(self._consumers) > 0
        if self._connected:
            logger.info(f"BatchConsumer connected: {len(self._consumers)}/{len(self._addresses)} channels")
        else:
            logger.warning("BatchConsumer: no channels connected")
        return self._connected

    def _try_connect(self, address: str) -> bool:
        """Try to connect a single channel. Returns True on success."""
        if address in self._consumers:
            return True

        parts = _parse_address(address)
        if parts is None:
            logger.warning(f"BatchConsumer: invalid address {address}")
            return False

        camera_id, node_id, port_name = parts
        try:
            consumer = DataBus.consumer(
                camera_id=camera_id,
                node_id=node_id,
                port_name=port_name,
                format=self._format,
                consumer_key=self._consumer_key,
                gpu_id=self._gpu_id,
            )
            self._consumers[address] = consumer
            return True
        except Exception as e:
            logger.debug(f"BatchConsumer: failed to connect {address}: {e}")
            return False

    def collect_batch(
        self,
        max_batch: int = 64,
        timeout_ms: float = 10.0,
    ) -> List[BatchItem]:
        """Collect up to max_batch items across all channels.

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
        results: List[BatchItem] = []
        start_time = time.perf_counter()
        deadline = start_time + (timeout_ms / 1000.0) if timeout_ms > 0 else float("inf")

        # Adaptive polling: start aggressive, back off if no items
        poll_interval = 0.0001  # 100 microseconds initial
        max_poll_interval = 0.001  # 1ms max

        while len(results) < max_batch:
            if time.perf_counter() >= deadline:
                break

            got_any = False

            for addr, consumer in list(self._consumers.items()):
                if len(results) >= max_batch:
                    break

                try:
                    data, metadata = consumer.consume()
                    if data is not None:
                        results.append((data, metadata, addr))
                        got_any = True
                except Exception as e:
                    logger.debug(f"BatchConsumer: error reading {addr}: {e}")

            if len(results) >= max_batch:
                break

            if not got_any:
                time.sleep(poll_interval)
                poll_interval = min(poll_interval * 1.5, max_poll_interval)
            else:
                poll_interval = 0.0001  # Reset to aggressive

        return results

    def ack_batch(self, items: List[BatchItem]) -> None:
        """Acknowledge all items in a batch.

        Args:
            items: List of (data, metadata, address) tuples from collect_batch()
        """
        for _data, metadata, addr in items:
            consumer = self._consumers.get(addr)
            if consumer and metadata and "frame_idx" in metadata:
                try:
                    consumer.ack(metadata["frame_idx"])
                except Exception as e:
                    logger.debug(f"BatchConsumer: ack failed for {addr}: {e}")

    def add_channel(self, address: str) -> bool:
        """Dynamically add a channel.

        Args:
            address: Full DataBus address (e.g., /dev/shm/databus__cam__node__port)

        Returns:
            True if connection succeeded
        """
        if address not in self._addresses:
            self._addresses.append(address)
        success = self._try_connect(address)
        if success:
            self._connected = True
        return success

    def remove_channel(self, address: str) -> None:
        """Dynamically remove a channel.

        Args:
            address: Full DataBus address to remove
        """
        consumer = self._consumers.pop(address, None)
        if consumer:
            consumer.close()
        if address in self._addresses:
            self._addresses.remove(address)
        self._connected = len(self._consumers) > 0

    @property
    def connected(self) -> bool:
        """True if at least one channel is connected."""
        return self._connected

    @property
    def channel_count(self) -> int:
        """Number of connected channels."""
        return len(self._consumers)

    @property
    def addresses(self) -> List[str]:
        """List of all registered addresses (connected or not)."""
        return list(self._addresses)

    def get_lag(self) -> Dict[str, int]:
        """Get per-channel consumer lag (frames behind).

        Only works for CUDA IPC consumers that expose get_frames_behind().
        Returns 0 for POSIX SHM consumers (no native lag tracking).
        """
        lag = {}
        for addr, consumer in self._consumers.items():
            try:
                if hasattr(consumer._rb, "get_frames_behind"):
                    lag[addr] = consumer._rb.get_frames_behind()
                else:
                    lag[addr] = 0
            except Exception:
                lag[addr] = -1
        return lag

    def close(self) -> None:
        """Close all consumer connections and cleanup."""
        for consumer in self._consumers.values():
            try:
                consumer.close()
            except Exception:
                pass
        self._consumers.clear()
        self._connected = False

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def __repr__(self):
        return (
            f"BatchConsumer(channels={len(self._consumers)}/{len(self._addresses)}, "
            f"format={self._format.value}, key={self._consumer_key!r})"
        )
