"""Auto-generated stub for module: drop_caches."""
from typing import Any

# Constants
DEFAULT_ENV_GATE: str
logger: Any

# Functions
def drop_caches(level: int = 3) -> bool:
    """
    Write ``level`` to ``/proc/sys/vm/drop_caches`` if gates allow.
    
        Returns ``True`` if the write succeeded, ``False`` otherwise. Never raises.
    
        level:
            1 = pagecache, 2 = dentries+inodes, 3 = both (default).
        require_env:
            Name of the env var that must be set to a truthy value. Pass ``None``
            to skip the env gate (only do this from tests or explicit ops tools).
    """
    ...
