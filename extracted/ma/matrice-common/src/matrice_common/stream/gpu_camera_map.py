"""Shared memory GPU-Camera mapping for CUDA IPC coordination.

This module provides a shared memory-based key-value store for coordinating
camera-to-GPU assignments between the Streaming Gateway (producer) and
Inference Engine (consumer).

The producer writes the mapping when creating ring buffers, and the consumer
reads to connect to the correct ring buffers on the correct GPU.

Architecture:
=============

    STREAMING GATEWAY                    INFERENCE ENGINE
    (Producer Process)                   (Consumer Process)
          |                                    |
          v                                    v
    +----------------+                  +----------------+
    | GpuCameraMap   |   /dev/shm/      | GpuCameraMap   |
    | (is_producer)  |<--------------->| (is_consumer)  |
    +----------------+  gpu_camera_map  +----------------+
          |                                    |
    camera_id -> gpu_id              gpu_id <- camera_id
          |                                    |
    Create ring                         Connect to ring
    buffers on GPU                      buffers on GPU

Usage:
======

    # Producer (Streaming Gateway):
    gpu_map = GpuCameraMap(is_producer=True)
    gpu_map.initialize()
    gpu_map.set_mapping("cam_0001", gpu_id=0)
    gpu_map.set_mapping("cam_0002", gpu_id=1)
    # ...
    gpu_map.close()  # Cleanup when done

    # Consumer (Inference Engine):
    gpu_map = GpuCameraMap(is_producer=False)
    if gpu_map.connect():
        gpu_id = gpu_map.get_gpu_id("cam_0001")  # Returns 0
        # Connect to ring buffer on correct GPU
"""

import fcntl
import json
import logging
import mmap
import os
import struct
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

# Environment variable for SHM base path (for Docker/custom environments)
# /dev/shm is the canonical POSIX shared memory path; override via env var if needed.
SHM_BASE_PATH = os.getenv("MATRICE_SHM_PATH", "/dev/shm")  # nosec B108

# Cross-platform mmap flags (fallbacks for Windows)
MAP_SHARED = getattr(mmap, "MAP_SHARED", 1)
PROT_READ = getattr(mmap, "PROT_READ", 1)
PROT_WRITE = getattr(mmap, "PROT_WRITE", 2)


class GpuCameraMap:
    """Shared memory store for camera_id -> gpu_id mapping.

    Uses a simple JSON format stored in shared memory with a size header.
    Thread-safe via file locking for writes.

    Format in shared memory:
    - 4 bytes: uint32 size of JSON data
    - N bytes: JSON string {"camera_id": gpu_id, ...}
    """

    SHM_PATH = f"{SHM_BASE_PATH}/gpu_camera_map"
    MAX_SIZE = 1024 * 1024  # 1MB for ~10k cameras

    def __init__(self, is_producer: bool = True) -> None:
        """Initialize the GPU camera map.

        Args:
            is_producer: True if this process creates/writes the mapping,
                        False if this process only reads.
        """
        self.is_producer = is_producer
        self._fd: Optional[int] = None
        self._mmap: Optional[mmap.mmap] = None
        self._initialized = False

    def initialize(self) -> bool:
        """Initialize as producer - create shared memory.

        Creates the shared memory file and initializes with empty mapping.
        Should be called by the streaming gateway before creating ring buffers.

        Returns:
            True if successful, False otherwise.
        """
        if not self.is_producer:
            logger.error("initialize() should only be called by producer")
            return False

        try:
            # Open or create — do NOT unlink, as consumers may have it mmap'd.
            # Unlinking creates a new inode; existing mmaps keep reading the
            # deleted old inode and never see new writes.
            self._fd = os.open(self.SHM_PATH, os.O_CREAT | os.O_RDWR, 0o666)
            os.ftruncate(self._fd, self.MAX_SIZE)

            # Memory map it
            self._mmap = mmap.mmap(self._fd, self.MAX_SIZE, MAP_SHARED, PROT_READ | PROT_WRITE)  # type: ignore[arg-type]

            # Write empty mapping
            self._write_mapping({})
            self._initialized = True

            logger.info(f"GpuCameraMap initialized at {self.SHM_PATH}")
            return True

        except Exception as e:
            logger.error(f"Failed to initialize GpuCameraMap: {e}")
            return False

    def connect(self) -> bool:
        """Connect to existing shared memory.

        For producers: opens with read-write access to allow writing mappings.
        For consumers: opens with read-only access.

        Returns:
            True if successful, False otherwise.
        """
        try:
            if not os.path.exists(self.SHM_PATH):
                logger.warning(f"GpuCameraMap not found at {self.SHM_PATH} - producer not started yet")
                return False

            if self.is_producer:
                # Producer needs read-write access to write mappings
                self._fd = os.open(self.SHM_PATH, os.O_RDWR)
                self._mmap = mmap.mmap(self._fd, self.MAX_SIZE, MAP_SHARED, PROT_READ | PROT_WRITE)  # type: ignore[arg-type]
            else:
                # Consumer only needs read access
                self._fd = os.open(self.SHM_PATH, os.O_RDONLY)
                self._mmap = mmap.mmap(self._fd, self.MAX_SIZE, MAP_SHARED, PROT_READ)  # type: ignore[arg-type]
            self._initialized = True

            logger.info(f"GpuCameraMap connected at {self.SHM_PATH} (mode={'rw' if self.is_producer else 'ro'})")
            return True

        except FileNotFoundError:
            logger.warning(f"GpuCameraMap not found at {self.SHM_PATH}")
            return False
        except Exception as e:
            logger.error(f"Failed to connect to GpuCameraMap: {e}")
            return False

    def set_mapping(self, camera_id: str, gpu_id: int) -> None:
        """Set GPU assignment for a camera (producer only).

        Thread-safe via file locking.

        Args:
            camera_id: Camera identifier
            gpu_id: GPU ID to assign this camera to
        """
        if not self.is_producer:
            logger.error("set_mapping() should only be called by producer")
            return

        if not self._initialized:
            logger.error("GpuCameraMap not initialized")
            return

        # Read current mapping, update, write back (with lock)
        mapping = self.get_all_mappings()
        mapping[camera_id] = gpu_id
        self._write_mapping(mapping)

    def set_bulk_mapping(self, mappings: Dict[str, int]) -> None:
        """Set multiple GPU assignments at once (producer only).

        More efficient than multiple set_mapping() calls.
        Uses exclusive lock around the entire read-modify-write cycle
        to prevent race conditions when multiple processes write concurrently.

        Args:
            mappings: Dict of camera_id -> gpu_id
        """
        if not self.is_producer:
            logger.error("set_bulk_mapping() should only be called by producer")
            return

        if not self._initialized or self._mmap is None:
            logger.error("GpuCameraMap not initialized")
            return

        try:
            # Lock around entire read-modify-write to prevent race conditions
            fcntl.flock(self._fd, fcntl.LOCK_EX)  # type: ignore[arg-type]
            try:
                # Read current mappings inside lock
                self._mmap.seek(0)
                size_bytes = self._mmap.read(4)
                current = {}
                if len(size_bytes) >= 4:
                    size = struct.unpack("<I", size_bytes)[0]
                    if 0 < size <= self.MAX_SIZE - 4:
                        try:
                            data = self._mmap.read(size).decode("utf-8")
                            current = json.loads(data)
                        except (json.JSONDecodeError, UnicodeDecodeError):
                            pass

                # Update with new mappings
                current.update(mappings)

                # Write back inside lock
                data = json.dumps(current).encode("utf-8")
                if len(data) + 4 > self.MAX_SIZE:
                    logger.error(f"GpuCameraMap: Mapping too large ({len(data)} bytes)")
                    return

                self._mmap.seek(0)
                self._mmap.write(struct.pack("<I", len(data)))
                self._mmap.write(data)
                self._mmap.flush()
            finally:
                fcntl.flock(self._fd, fcntl.LOCK_UN)  # type: ignore[arg-type]

            logger.info(f"GpuCameraMap: Set {len(mappings)} camera-GPU mappings (total: {len(current)})")
        except Exception as e:
            logger.error(f"GpuCameraMap: Failed to set bulk mapping: {e}")

    def replace_all_mappings(self, mappings: Dict[str, int]) -> None:
        """Replace the entire map with the given mappings (producer only).

        Unlike set_bulk_mapping() which merges, this does a full atomic replace.
        Removed cameras will no longer appear in the map.

        Args:
            mappings: Complete dict of camera_id -> gpu_id
        """
        if not self.is_producer:
            logger.error("replace_all_mappings() should only be called by producer")
            return

        if not self._initialized:
            logger.error("GpuCameraMap not initialized")
            return

        self._write_mapping(mappings)

    def remove_mapping(self, camera_id: str) -> None:
        """Remove a single camera from the map (producer only).

        Thread-safe via file locking.

        Args:
            camera_id: Camera identifier to remove
        """
        if not self.is_producer:
            logger.error("remove_mapping() should only be called by producer")
            return

        if not self._initialized:
            logger.error("GpuCameraMap not initialized")
            return

        mapping = self.get_all_mappings()
        if camera_id in mapping:
            del mapping[camera_id]
            self._write_mapping(mapping)

    def check_file_recreated(self) -> bool:
        """Return True if the SHM file's on-disk inode no longer matches our open fd.

        When the SHM file is unlinked + recreated (SG restart with external cleanup,
        operator `rm -f /dev/shm/gpu_camera_map`, or `docker rm` on the SG container),
        the open fd keeps pointing at the deleted inode while a new inode appears at
        the same path. Comparing os.fstat(fd).st_ino vs os.stat(path).st_ino detects
        this. Mirrors CudaShmRingBuffer.check_file_recreated().

        Returns:
            True if file was recreated (stale) or missing, False if still the same file.
        """
        if self._fd is None:
            return False
        try:
            our_inode = os.fstat(self._fd).st_ino
            disk_inode = os.stat(self.SHM_PATH).st_ino
            return our_inode != disk_inode
        except FileNotFoundError:
            return True
        except Exception:
            return False

    def reconnect(self) -> bool:
        """Close the stale mmap+fd and re-open the current SHM file by path.

        Idempotent: safe to call even when not connected. Returns True on success,
        False when the file is missing (caller should retry later).
        """
        self.close()
        return self.connect()

    def _ensure_fresh(self) -> None:
        """Read-path hook: reconnect transparently if the file was recreated.

        Consumer-only. Producers own the file's lifecycle and should not be
        silently re-attached to a stranger's inode. Cheap (~1 stat syscall);
        called by get_all_mappings() so consumers self-heal on the next read
        after an SG restart, without needing external watchdog intervention.

        Two recovery paths:
          - we have an open fd but the inode changed -> close + reopen
          - we have no fd (initial connect failed, or a prior reconnect lost it
            because the file was momentarily missing) and the file now exists
            -> connect()
        """
        if self.is_producer:
            return
        if self._fd is not None:
            if self.check_file_recreated():
                logger.warning(f"GpuCameraMap: SHM file recreated at {self.SHM_PATH}, reconnecting")
                self.reconnect()
        elif os.path.exists(self.SHM_PATH):
            logger.info(f"GpuCameraMap: SHM file now available at {self.SHM_PATH}, connecting")
            self.connect()

    def get_gpu_id(self, camera_id: str) -> Optional[int]:
        """Get GPU ID for a camera (consumer).

        Args:
            camera_id: Camera identifier

        Returns:
            GPU ID if found, None otherwise.
        """
        mapping = self.get_all_mappings()
        return mapping.get(camera_id)

    def get_all_mappings(self) -> Dict[str, int]:
        """Get all camera-to-GPU mappings.

        Returns:
            Dict of camera_id -> gpu_id
        """
        self._ensure_fresh()
        if not self._initialized or self._mmap is None:
            return {}

        try:
            self._mmap.seek(0)
            size_bytes = self._mmap.read(4)
            if len(size_bytes) < 4:
                return {}

            size = struct.unpack("<I", size_bytes)[0]
            if size == 0 or size > self.MAX_SIZE - 4:
                return {}

            data = self._mmap.read(size).decode("utf-8")
            return json.loads(data)

        except json.JSONDecodeError as e:
            logger.warning(f"GpuCameraMap: Invalid JSON data: {e}")
            return {}
        except Exception as e:
            logger.debug(f"GpuCameraMap: Failed to read mappings: {e}")
            return {}

    def get_cameras_for_gpu(self, gpu_id: int) -> List[str]:
        """Get all camera IDs assigned to a specific GPU.

        Args:
            gpu_id: GPU ID to filter by

        Returns:
            List of camera IDs assigned to this GPU
        """
        mapping = self.get_all_mappings()
        return [cam_id for cam_id, gid in mapping.items() if gid == gpu_id]

    def _write_mapping(self, mapping: Dict[str, int]) -> None:
        """Write mapping to shared memory (producer only).

        Thread-safe via file locking.
        """
        if self._mmap is None:
            return

        try:
            data = json.dumps(mapping).encode("utf-8")

            if len(data) + 4 > self.MAX_SIZE:
                logger.error(f"GpuCameraMap: Mapping too large ({len(data)} bytes)")
                return

            # Lock for writing
            fcntl.flock(self._fd, fcntl.LOCK_EX)  # type: ignore[attr-defined]
            try:
                self._mmap.seek(0)
                self._mmap.write(struct.pack("<I", len(data)))
                self._mmap.write(data)
                self._mmap.flush()
            finally:
                fcntl.flock(self._fd, fcntl.LOCK_UN)  # type: ignore[attr-defined]

        except Exception as e:
            logger.error(f"GpuCameraMap: Failed to write mapping: {e}")

    def close(self) -> None:
        """Close the shared memory mapping.

        Producer should call this during cleanup.
        """
        try:
            if self._mmap:
                self._mmap.close()
                self._mmap = None

            if self._fd:
                os.close(self._fd)
                self._fd = None

            # Do NOT unlink the SHM file on close — consumers may still have
            # it mmap'd. The file persists in /dev/shm and gets reused on next
            # initialize() call. It's cleaned up automatically on reboot.

            self._initialized = False

        except Exception as e:
            logger.warning(f"GpuCameraMap: Error during close: {e}")

    def __enter__(self):
        """Context manager entry."""
        if self.is_producer:
            self.initialize()
        else:
            self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
        return False


# Singleton instance for global access
_gpu_camera_map: Optional[GpuCameraMap] = None


def get_gpu_camera_map(is_producer: bool = False) -> GpuCameraMap:
    """Get or create the global GpuCameraMap instance.

    Args:
        is_producer: True if this is the producer process

    Returns:
        GpuCameraMap instance (may not be initialized)
    """
    global _gpu_camera_map
    if _gpu_camera_map is None:
        _gpu_camera_map = GpuCameraMap(is_producer=is_producer)
    return _gpu_camera_map
