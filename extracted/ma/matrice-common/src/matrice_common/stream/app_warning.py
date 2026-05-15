"""AppWarningManager — Device health monitoring with warning notifications.

Monitors pipeline nodes via NodeStatus SHM heartbeats and emits structured
warnings when devices go offline/online. Integrates with OfflineRequestCache
for automatic request queuing during outages.

Environment variables:
    MATRICE_WARNING_CHECK_INTERVAL: Health check interval in seconds (default: 10)
    MATRICE_WARNING_STALE_THRESHOLD: Seconds before a node is considered stale (default: 30)

Usage:
    from matrice_common.stream.app_warning import AppWarningManager

    manager = AppWarningManager()
    manager.on_warning(my_callback)  # Register warning handler
    manager.start()

    # Warnings are emitted automatically when nodes go offline/online
    # Or poll manually:
    warnings = manager.get_warnings()
    for w in warnings:
        print(f"[{w['type']}] {w['node_id']}: {w['message']}")

    manager.stop()
"""

import logging
import os
import threading
import time
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional

from .databus_status import STALE_THRESHOLD_NS, NodeStatus

logger = logging.getLogger(__name__)

DEFAULT_CHECK_INTERVAL = float(os.environ.get("MATRICE_WARNING_CHECK_INTERVAL", "10"))
DEFAULT_STALE_THRESHOLD_SEC = float(os.environ.get("MATRICE_WARNING_STALE_THRESHOLD", "30"))


@dataclass
class NodeState:
    """Internal tracking state for a monitored node."""

    node_id: str
    is_online: bool = True
    last_seen_ns: int = 0
    went_offline_at: float = 0.0
    offline_count: int = 0
    last_warning_at: float = 0.0


class AppWarningManager:
    """Monitors DataBus pipeline nodes and emits warnings on state changes.

    Uses NodeStatus SHM heartbeat files for zero-overhead health checking.
    Warning callbacks are invoked on the monitor thread — keep handlers fast.

    Args:
        check_interval: Seconds between health check sweeps.
        stale_threshold_sec: Seconds without heartbeat before a node is stale.
    """

    def __init__(
        self,
        check_interval: float = DEFAULT_CHECK_INTERVAL,
        stale_threshold_sec: float = DEFAULT_STALE_THRESHOLD_SEC,
    ):
        self._check_interval = check_interval
        self._stale_threshold_ns = int(stale_threshold_sec * 1_000_000_000)
        self._nodes: Dict[str, NodeState] = {}
        self._callbacks: List[Callable[[Dict[str, Any]], None]] = []
        self._warnings: List[Dict[str, Any]] = []
        self._lock = threading.Lock()
        self._stop_event = threading.Event()
        self._thread: Optional[threading.Thread] = None

    def start(self) -> None:
        """Start the background monitoring thread."""
        if self._thread and self._thread.is_alive():
            return
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._monitor_loop, name="AppWarningMonitor", daemon=True)
        self._thread.start()
        logger.info(
            f"AppWarningManager started: interval={self._check_interval}s, "
            f"stale_threshold={self._stale_threshold_ns / 1e9:.0f}s"
        )

    def stop(self) -> None:
        """Stop the monitoring thread."""
        self._stop_event.set()
        if self._thread:
            self._thread.join(timeout=5.0)
        logger.info("AppWarningManager stopped")

    def on_warning(self, callback: Callable[[Dict[str, Any]], None]) -> None:
        """Register a callback for warning events.

        Callback receives a dict with keys: timestamp, node_id, type, message, details.
        Warning types: DEVICE_OFFLINE, DEVICE_ONLINE, DEVICE_STALE, NODE_DISCOVERED.
        """
        with self._lock:
            self._callbacks.append(callback)

    def get_warnings(self, clear: bool = True) -> List[Dict[str, Any]]:
        """Get accumulated warnings, optionally clearing the buffer."""
        with self._lock:
            result = list(self._warnings)
            if clear:
                self._warnings.clear()
            return result

    def get_node_states(self) -> Dict[str, Dict[str, Any]]:
        """Get current state of all monitored nodes."""
        with self._lock:
            return {
                nid: {
                    "is_online": ns.is_online,
                    "last_seen_ns": ns.last_seen_ns,
                    "offline_count": ns.offline_count,
                }
                for nid, ns in self._nodes.items()
            }

    def is_node_online(self, node_id: str) -> bool:
        """Check if a specific node is online."""
        with self._lock:
            ns = self._nodes.get(node_id)
            return ns.is_online if ns else False

    # ── Internal ──────────────────────────────────────────────────────────

    def _monitor_loop(self) -> None:
        """Background loop: poll NodeStatus SHM files and emit warnings."""
        while not self._stop_event.wait(timeout=self._check_interval):
            try:
                self._check_all_nodes()
            except Exception as e:
                logger.error(f"AppWarningManager check failed: {e}")

    def _check_all_nodes(self) -> None:
        """Read all NodeStatus files and update state."""
        all_statuses = NodeStatus.read_all()
        seen_ids = set()

        with self._lock:
            for status in all_statuses:
                node_id = status.get("node_id", "")
                if not node_id:
                    continue
                seen_ids.add(node_id)

                is_stale = NodeStatus.is_stale(status, self._stale_threshold_ns)
                hb_ns = status.get("last_heartbeat_ns", 0)

                if node_id not in self._nodes:
                    # New node discovered
                    self._nodes[node_id] = NodeState(
                        node_id=node_id,
                        is_online=not is_stale,
                        last_seen_ns=hb_ns,
                    )
                    self._emit(
                        "NODE_DISCOVERED",
                        node_id,
                        f"Node {node_id} discovered ({'online' if not is_stale else 'stale'})",
                        status=status,
                    )
                    continue

                ns = self._nodes[node_id]
                ns.last_seen_ns = hb_ns

                if is_stale and ns.is_online:
                    # Transition: online -> offline
                    ns.is_online = False
                    ns.went_offline_at = time.time()
                    ns.offline_count += 1
                    self._emit(
                        "DEVICE_OFFLINE",
                        node_id,
                        f"Node {node_id} went offline (no heartbeat for "
                        f"{self._stale_threshold_ns / 1e9:.0f}s, count: {ns.offline_count})",
                        offline_count=ns.offline_count,
                    )

                elif not is_stale and not ns.is_online:
                    # Transition: offline -> online
                    downtime = time.time() - ns.went_offline_at if ns.went_offline_at else 0
                    ns.is_online = True
                    self._emit(
                        "DEVICE_ONLINE",
                        node_id,
                        f"Node {node_id} back online (was offline for {downtime:.1f}s)",
                        downtime_sec=round(downtime, 1),
                    )

            # Check for nodes that disappeared (status file removed)
            for node_id, ns in self._nodes.items():
                if node_id not in seen_ids and ns.is_online:
                    ns.is_online = False
                    ns.went_offline_at = time.time()
                    ns.offline_count += 1
                    self._emit(
                        "DEVICE_OFFLINE",
                        node_id,
                        f"Node {node_id} status file disappeared",
                        offline_count=ns.offline_count,
                    )

    def _emit(self, warning_type: str, node_id: str, message: str, **details) -> None:
        """Emit a warning to callbacks and internal buffer."""
        warning = {
            "timestamp": time.time(),
            "node_id": node_id,
            "type": warning_type,
            "message": message,
            **details,
        }
        self._warnings.append(warning)
        if len(self._warnings) > 1000:
            self._warnings = self._warnings[-500:]

        for cb in self._callbacks:
            try:
                cb(warning)
            except Exception as e:
                logger.error(f"Warning callback error: {e}")

        if warning_type == "DEVICE_OFFLINE":
            logger.warning(message)
        else:
            logger.info(message)
