"""OfflineRequestCache — Store-and-forward cache for offline device resilience.

Queues outbound requests (analytics results, API calls) when a target device
or service is unreachable, and replays them automatically on reconnection.

Integrates with NodeStatus heartbeat monitoring to detect online/offline
transitions and AppWarningManager for user-facing notifications.

Environment variables:
    MATRICE_OFFLINE_CACHE_MAX_SIZE: Max queued requests (default: 10000)
    MATRICE_OFFLINE_CACHE_TTL: Per-request TTL in seconds (default: 300)
    MATRICE_OFFLINE_CACHE_FLUSH_BATCH: Requests per flush batch (default: 100)
    MATRICE_OFFLINE_CACHE_CHECK_INTERVAL: Health check interval secs (default: 10)

Usage:
    cache = OfflineRequestCache(send_fn=my_api_call)
    cache.start()

    # Submit requests — queued if offline, sent immediately if online
    cache.submit("device_123", {"type": "analytics", "data": {...}})

    # Check device status
    print(cache.device_status("device_123"))  # "online" / "offline" / "unknown"

    # Graceful shutdown — flushes remaining requests
    cache.stop()
"""

import logging
import os
import threading
import time
from collections import defaultdict, deque
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Deque, Dict, List, Optional

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
DEFAULT_MAX_SIZE = int(os.environ.get("MATRICE_OFFLINE_CACHE_MAX_SIZE", "10000"))
DEFAULT_TTL_SECONDS = float(os.environ.get("MATRICE_OFFLINE_CACHE_TTL", "300"))
DEFAULT_FLUSH_BATCH_SIZE = int(os.environ.get("MATRICE_OFFLINE_CACHE_FLUSH_BATCH", "100"))
DEFAULT_CHECK_INTERVAL = float(os.environ.get("MATRICE_OFFLINE_CACHE_CHECK_INTERVAL", "10"))


class DeviceState(Enum):
    ONLINE = "online"
    OFFLINE = "offline"
    UNKNOWN = "unknown"


@dataclass
class QueuedRequest:
    """A request waiting to be sent when the target comes back online."""

    device_id: str
    payload: Any
    created_at: float = field(default_factory=time.time)
    attempts: int = 0

    def is_expired(self, ttl: float) -> bool:
        return (time.time() - self.created_at) > ttl


@dataclass
class DeviceInfo:
    """Tracked state for a single device."""

    state: DeviceState = DeviceState.UNKNOWN
    last_seen: float = 0.0
    last_offline: float = 0.0
    offline_count: int = 0
    queued: int = 0
    flushed: int = 0
    expired: int = 0


class OfflineRequestCache:
    """Store-and-forward cache that queues requests for offline devices.

    When a device goes offline (detected via health_check_fn or send failure),
    subsequent requests are queued in memory. When the device comes back online,
    queued requests are flushed in order.

    Args:
        send_fn: Callable(device_id, payload) -> bool. Returns True on success.
        health_check_fn: Optional callable(device_id) -> bool. Returns True if online.
            If not provided, online/offline is inferred from send_fn success/failure.
        max_size: Maximum total queued requests across all devices.
        ttl_seconds: Per-request TTL. Expired requests are discarded.
        flush_batch_size: Max requests to flush per cycle per device.
        check_interval: Seconds between health check cycles.
    """

    def __init__(
        self,
        send_fn: Callable[[str, Any], bool],
        health_check_fn: Optional[Callable[[str], bool]] = None,
        max_size: int = DEFAULT_MAX_SIZE,
        ttl_seconds: float = DEFAULT_TTL_SECONDS,
        flush_batch_size: int = DEFAULT_FLUSH_BATCH_SIZE,
        check_interval: float = DEFAULT_CHECK_INTERVAL,
    ):
        self._send_fn = send_fn
        self._health_check_fn = health_check_fn
        self._max_size = max_size
        self._ttl = ttl_seconds
        self._flush_batch_size = flush_batch_size
        self._check_interval = check_interval

        self._queues: Dict[str, Deque[QueuedRequest]] = defaultdict(deque)
        self._devices: Dict[str, DeviceInfo] = defaultdict(DeviceInfo)
        self._total_queued = 0
        self._lock = threading.Lock()
        self._stop_event = threading.Event()
        self._thread: Optional[threading.Thread] = None
        self._warnings: List[Dict[str, Any]] = []

    def start(self) -> None:
        """Start the background health-check and flush thread."""
        if self._thread and self._thread.is_alive():
            return
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._monitor_loop, name="OfflineCacheMonitor", daemon=True)
        self._thread.start()
        logger.info(
            f"OfflineRequestCache started: max_size={self._max_size}, "
            f"ttl={self._ttl}s, check_interval={self._check_interval}s"
        )

    def stop(self, flush_timeout: float = 5.0) -> None:
        """Stop monitoring and attempt final flush of queued requests."""
        self._stop_event.set()
        if self._thread:
            self._thread.join(timeout=flush_timeout)
        # Final flush attempt for all online devices
        with self._lock:
            for device_id in list(self._queues.keys()):
                self._flush_device(device_id)
        logger.info("OfflineRequestCache stopped")

    def submit(self, device_id: str, payload: Any) -> bool:
        """Submit a request for a device.

        If the device is online, sends immediately. If offline or send fails,
        queues the request for later delivery.

        Returns:
            True if sent immediately, False if queued.
        """
        with self._lock:
            device = self._devices[device_id]

            # If device is known online, try sending directly
            if device.state == DeviceState.ONLINE:
                try:
                    if self._send_fn(device_id, payload):
                        return True
                except Exception as e:
                    logger.debug(f"Send to {device_id} failed, queueing: {e}")
                # Send failed — mark offline and queue
                self._mark_offline(device_id)

            # Queue the request
            return self._enqueue(device_id, payload)

    def device_status(self, device_id: str) -> str:
        """Get current status of a device."""
        with self._lock:
            return self._devices[device_id].state.value

    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        with self._lock:
            return {
                "total_queued": self._total_queued,
                "devices_tracked": len(self._devices),
                "devices_offline": sum(1 for d in self._devices.values() if d.state == DeviceState.OFFLINE),
                "per_device": {
                    did: {
                        "state": info.state.value,
                        "queued": info.queued,
                        "flushed": info.flushed,
                        "expired": info.expired,
                    }
                    for did, info in self._devices.items()
                },
            }

    def get_warnings(self, clear: bool = True) -> List[Dict[str, Any]]:
        """Get and optionally clear accumulated warnings."""
        with self._lock:
            warnings = list(self._warnings)
            if clear:
                self._warnings.clear()
            return warnings

    # ── Internal ──────────────────────────────────────────────────────────

    def _enqueue(self, device_id: str, payload: Any) -> bool:
        """Queue a request. Returns False (indicating it was queued, not sent)."""
        if self._total_queued >= self._max_size:
            # Evict oldest expired request across all devices
            self._evict_expired()
            if self._total_queued >= self._max_size:
                self._emit_warning(device_id, "QUEUE_FULL", f"Cache full ({self._max_size}), dropping request")
                return False

        req = QueuedRequest(device_id=device_id, payload=payload)
        self._queues[device_id].append(req)
        self._total_queued += 1
        self._devices[device_id].queued += 1
        return False

    def _mark_offline(self, device_id: str) -> None:
        """Transition a device to offline state."""
        device = self._devices[device_id]
        if device.state != DeviceState.OFFLINE:
            device.state = DeviceState.OFFLINE
            device.last_offline = time.time()
            device.offline_count += 1
            self._emit_warning(
                device_id, "DEVICE_OFFLINE", f"Device {device_id} went offline (count: {device.offline_count})"
            )
            logger.warning(f"Device {device_id} marked OFFLINE")

    def _mark_online(self, device_id: str) -> None:
        """Transition a device to online state and flush queue."""
        device = self._devices[device_id]
        if device.state != DeviceState.ONLINE:
            was_offline = device.state == DeviceState.OFFLINE
            device.state = DeviceState.ONLINE
            device.last_seen = time.time()
            if was_offline:
                self._emit_warning(device_id, "DEVICE_ONLINE", f"Device {device_id} back online, flushing queue")
                logger.info(f"Device {device_id} back ONLINE, flushing queued requests")
            self._flush_device(device_id)

    def _flush_device(self, device_id: str) -> int:
        """Flush queued requests for a device. Returns number flushed."""
        queue = self._queues.get(device_id)
        if not queue:
            return 0

        flushed = 0
        for _ in range(min(self._flush_batch_size, len(queue))):
            if not queue:
                break
            req = queue[0]

            # Skip expired
            if req.is_expired(self._ttl):
                queue.popleft()
                self._total_queued -= 1
                self._devices[device_id].expired += 1
                continue

            # Attempt send
            req.attempts += 1
            try:
                if self._send_fn(device_id, req.payload):
                    queue.popleft()
                    self._total_queued -= 1
                    self._devices[device_id].flushed += 1
                    flushed += 1
                else:
                    # Send failed — stop flushing, device might be offline again
                    self._mark_offline(device_id)
                    break
            except Exception:
                self._mark_offline(device_id)
                break

        return flushed

    def _evict_expired(self) -> int:
        """Remove expired requests across all queues."""
        evicted = 0
        for device_id, queue in list(self._queues.items()):
            while queue and queue[0].is_expired(self._ttl):
                queue.popleft()
                self._total_queued -= 1
                self._devices[device_id].expired += 1
                evicted += 1
            if not queue:
                del self._queues[device_id]
        return evicted

    def _emit_warning(self, device_id: str, warning_type: str, message: str) -> None:
        """Add a warning to the warnings list."""
        self._warnings.append(
            {
                "timestamp": time.time(),
                "device_id": device_id,
                "type": warning_type,
                "message": message,
            }
        )
        # Keep warnings bounded
        if len(self._warnings) > 1000:
            self._warnings = self._warnings[-500:]

    def _monitor_loop(self) -> None:
        """Background thread: check device health and flush queues."""
        while not self._stop_event.wait(timeout=self._check_interval):
            with self._lock:
                # Evict expired requests
                self._evict_expired()

                # Check health of all tracked devices
                for device_id in list(self._devices.keys()):
                    if self._health_check_fn:
                        try:
                            is_online = self._health_check_fn(device_id)
                        except Exception:
                            is_online = False

                        if is_online:
                            self._mark_online(device_id)
                        else:
                            self._mark_offline(device_id)
                    elif self._devices[device_id].state == DeviceState.ONLINE:
                        # No health check fn — flush online devices
                        self._flush_device(device_id)
