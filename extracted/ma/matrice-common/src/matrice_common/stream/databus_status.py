"""NodeStatus — Per-node SHM health files for DataBus pipeline monitoring.

Each pipeline node owns exactly one status file at:
    /dev/shm/databus_status__{node_id}

No concurrent-writer contention (single owner per file).
Readers can check health of any node via NodeStatus.read(node_id).

File format: [4 bytes: length (uint32 LE)][JSON bytes (orjson)]

Usage:
    # Node writes its own status
    status = NodeStatus("yolo_gpu0")
    status.write(status="alive", model_loaded=True,
                 buffer_addresses=["/dev/shm/databus__cam1__yolo__detection0"])

    # Periodic heartbeat (fast-path: update only timestamp)
    status.heartbeat()

    # Reader checks node health
    info = NodeStatus.read("yolo_gpu0")
    if info and NodeStatus.is_stale(info):
        print("Node yolo_gpu0 appears dead")

    # Cleanup on graceful shutdown
    status.remove()
"""

import logging
import os
import struct
import time
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

# /dev/shm is the canonical POSIX shared memory path; override via env var if needed.
SHM_BASE_PATH = os.getenv("MATRICE_SHM_PATH", "/dev/shm")  # nosec B108
STATUS_PREFIX = "databus_status__"
STALE_THRESHOLD_NS = 30_000_000_000  # 30 seconds

# ─── JSON serialization with orjson fallback ─────────────────────────────────
try:
    import orjson

    def _dumps(obj: Any) -> bytes:
        return orjson.dumps(obj)

    def _loads(data: bytes) -> Any:
        return orjson.loads(data)
except ImportError:
    import json

    def _dumps(obj: Any) -> bytes:
        return json.dumps(obj).encode("utf-8")

    def _loads(data: bytes) -> Any:
        return json.loads(data if isinstance(data, str) else data.decode("utf-8"))


class NodeStatus:
    """Per-node SHM status file.

    Each node owns exactly one file — no write contention.
    """

    def __init__(self, node_id: str):
        self.node_id = node_id
        self.path = os.path.join(SHM_BASE_PATH, f"{STATUS_PREFIX}{node_id}")

    def write(
        self, status: str = "alive", model_loaded: bool = False, buffer_addresses: Optional[List[str]] = None, **extra
    ) -> None:
        """Write full status. Creates file if needed."""
        payload = {
            "node_id": self.node_id,
            "status": status,
            "model_loaded": model_loaded,
            "buffer_addresses": buffer_addresses or [],
            "last_heartbeat_ns": time.time_ns(),
            **extra,
        }
        data = _dumps(payload)
        # Atomic write: length-prefix + data
        with open(self.path, "wb") as f:
            f.write(struct.pack("<I", len(data)))
            f.write(data)

    def heartbeat(self) -> None:
        """Fast-path: update only last_heartbeat_ns in existing status."""
        existing = self._read_local()
        if existing:
            existing["last_heartbeat_ns"] = time.time_ns()
            data = _dumps(existing)
            with open(self.path, "wb") as f:
                f.write(struct.pack("<I", len(data)))
                f.write(data)
        else:
            # No existing status — write a minimal one
            self.write()

    def remove(self) -> None:
        """Delete status file on graceful shutdown."""
        try:
            os.unlink(self.path)
        except FileNotFoundError:
            pass
        except OSError as e:
            logger.warning(f"Failed to remove status file {self.path}: {e}")

    def _read_local(self) -> Optional[Dict]:
        """Read this node's own status file."""
        return NodeStatus.read(self.node_id)

    @staticmethod
    def read(node_id: str) -> Optional[Dict]:
        """Read one node's status by ID.

        Returns:
            Status dict or None if not found/corrupt.
        """
        path = os.path.join(SHM_BASE_PATH, f"{STATUS_PREFIX}{node_id}")
        try:
            with open(path, "rb") as f:
                length_bytes = f.read(4)
                if len(length_bytes) < 4:
                    return None
                length = struct.unpack("<I", length_bytes)[0]
                data = f.read(length)
                if len(data) < length:
                    return None
                return _loads(data)
        except FileNotFoundError:
            return None
        except Exception as e:
            logger.debug(f"Failed to read status for {node_id}: {e}")
            return None

    @staticmethod
    def read_all() -> List[Dict]:
        """Read all node status files.

        Returns:
            List of status dicts for all active nodes.
        """
        results = []
        try:
            for entry in os.listdir(SHM_BASE_PATH):
                if entry.startswith(STATUS_PREFIX):
                    node_id = entry[len(STATUS_PREFIX) :]
                    status = NodeStatus.read(node_id)
                    if status:
                        results.append(status)
        except OSError as e:
            logger.warning(f"Failed to list status files: {e}")
        return results

    @staticmethod
    def is_stale(status_dict: Dict, threshold_ns: int = STALE_THRESHOLD_NS) -> bool:
        """Check if a node's status is stale (no heartbeat within threshold).

        Args:
            status_dict: Status dict from read() or read_all()
            threshold_ns: Stale threshold in nanoseconds (default 30s)

        Returns:
            True if last heartbeat is older than threshold.
        """
        hb = status_dict.get("last_heartbeat_ns", 0)
        if hb == 0:
            return True
        return (time.time_ns() - hb) > threshold_ns

    def __repr__(self):
        return f"NodeStatus(node_id={self.node_id!r}, path={self.path!r})"
