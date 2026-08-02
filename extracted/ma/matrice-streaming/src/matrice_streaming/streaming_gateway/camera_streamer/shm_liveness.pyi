"""Auto-generated stub for module: shm_liveness."""
from typing import Any, Optional, Set

from __future__ import annotations
import glob
import logging
import os

# Constants
SHM_DIR: str
logger: Any

# Functions
def camera_has_live_shm(camera_id: str, held: Optional[Set[str]] = None) -> bool: ...
    """
    True if any live process holds a databus segment for ``camera_id`` open.
    
        Fails open (returns True) when the scan is unavailable, so an unreadable
        ``/proc`` can never license deleting a segment a producer is writing.
    """
def camera_shm_prefixes(camera_id: str) -> tuple: ...
    """
    The ``/dev/shm`` name prefixes owned by ``camera_id``.
    
        Mirrors the patterns the worker managers clean:
        ``databus__<cam>__*`` (ring buffers, e.g. ``__sg__frames``) and
        ``databus_status__<cam>`` (the status segment, which has no trailing ``__``).
    """
def held_shm_paths() -> Optional[Set[str]]: ...
    """
    Return every ``/dev/shm`` path currently held open by any live process.
    
        Returns ``None`` when the scan could not be performed, which callers must
        treat as "unknown — assume everything is live" (fail open). An empty set is a
        positive result meaning "scanned successfully, nothing is held".
    """
def is_shm_path_live(path: str, held: Optional[Set[str]] = None) -> bool: ...
    """
    True if ``path`` is held open by a live process, or if that is unknown.
    
        Pass ``held`` from a single :func:`held_shm_paths` call when checking many
        paths, so the ``/proc`` walk happens once instead of per path.
    """
