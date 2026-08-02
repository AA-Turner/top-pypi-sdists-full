"""Auto-generated stub for module: secure_cache."""
from typing import Any

from pathlib import Path
import os
import stat
import tempfile

# Functions
def is_safe_cached_file(path: Any) -> bool: ...
    """
    True if ``path`` is a regular file owned by the current uid.
    
        Rejects symlinks and files owned by other users so a pre-seeded cache entry
        is never trusted for reuse.
    """
def secure_cache_dir(name: str) -> Any: ...
    """
    Return a per-user cache dir under the temp root, created mode 0700.
    
        The directory name is suffixed with the current uid so distinct users never
        share a cache path. Raises RuntimeError if an existing path at that location
        is a symlink, not a directory, or owned by another user (hijack attempt).
    """
