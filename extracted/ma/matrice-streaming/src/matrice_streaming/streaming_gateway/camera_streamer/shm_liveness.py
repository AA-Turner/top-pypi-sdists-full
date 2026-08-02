"""Detect whether a /dev/shm segment is still held open by a live process.

Used to make SHM cleanup safe: a segment some process still has open is NOT
stale, and unlinking it strands that producer's consumers with ENOENT while
frames are still flowing.

Deliberately dependency-free (no ``fcntl``, no ``gi``, nothing from
``matrice_common``) so it imports and unit-tests on any platform. The worker
managers that call it cannot even be imported on Windows — ``nvdec_worker_manager``
pulls in ``matrice_common.stream.gpu_camera_map``, which imports the POSIX-only
``fcntl`` — so keeping this logic separate is what makes it verifiable.

Everything here FAILS OPEN: if the scan cannot be completed (no ``/proc``,
permissions, a racing process), the answer is "assume live", because wrongly
keeping a stale file costs one leaked inode while wrongly deleting a live one
breaks a running camera.

Requires ``--pid=host`` to see other containers' processes, which the SG always
runs with. Without it the scan still sees this container's own processes, so the
common case (the SG's own worker sub-process holding the segment) is covered
regardless.
"""

from __future__ import annotations

import glob
import logging
import os
from typing import Optional, Set

logger = logging.getLogger(__name__)

SHM_DIR = "/dev/shm"  # nosec B108 - the POSIX shared-memory mount, not a temp file


def held_shm_paths() -> Optional[Set[str]]:
    """Return every ``/dev/shm`` path currently held open by any live process.

    Returns ``None`` when the scan could not be performed, which callers must
    treat as "unknown — assume everything is live" (fail open). An empty set is a
    positive result meaning "scanned successfully, nothing is held".
    """
    if not os.path.isdir("/proc"):
        # Not Linux, or /proc not mounted: we cannot know. Fail open.
        return None

    held: Set[str] = set()
    try:
        for fd_path in glob.iglob("/proc/[0-9]*/fd/*"):
            try:
                target = os.readlink(fd_path)
            except OSError:
                # Process or fd vanished mid-scan; normal, keep going.
                continue
            if target.startswith(SHM_DIR):
                # A deleted-but-still-open file reads as "<path> (deleted)"; such a
                # segment is already unlinked, so it is not something we can or
                # need to remove.
                if not target.endswith(" (deleted)"):
                    held.add(target)
    except Exception as e:
        logger.warning(f"SHM liveness scan failed ({e}); treating all segments as live")
        return None
    return held


def is_shm_path_live(path: str, held: Optional[Set[str]] = None) -> bool:
    """True if ``path`` is held open by a live process, or if that is unknown.

    Pass ``held`` from a single :func:`held_shm_paths` call when checking many
    paths, so the ``/proc`` walk happens once instead of per path.
    """
    if held is None:
        held = held_shm_paths()
    if held is None:
        return True  # fail open
    return path in held


def camera_shm_prefixes(camera_id: str) -> tuple:
    """The ``/dev/shm`` name prefixes owned by ``camera_id``.

    Mirrors the patterns the worker managers clean:
    ``databus__<cam>__*`` (ring buffers, e.g. ``__sg__frames``) and
    ``databus_status__<cam>`` (the status segment, which has no trailing ``__``).
    """
    return (
        f"{SHM_DIR}/databus__{camera_id}__",
        f"{SHM_DIR}/databus_status__{camera_id}",
    )


def camera_has_live_shm(camera_id: str, held: Optional[Set[str]] = None) -> bool:
    """True if any live process holds a databus segment for ``camera_id`` open.

    Fails open (returns True) when the scan is unavailable, so an unreadable
    ``/proc`` can never license deleting a segment a producer is writing.
    """
    if not camera_id:
        return False
    if held is None:
        held = held_shm_paths()
    if held is None:
        return True  # fail open
    prefixes = camera_shm_prefixes(camera_id)
    return any(p.startswith(prefixes) for p in held)
