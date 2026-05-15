"""Auto-generated stub for module: shm_cleanup."""
from typing import Any, List, Tuple

# Constants
DEFAULT_PREFIXES: Tuple[Any, ...]
logger: Any

# Functions
def cleanup_owned_shm(prefixes: Any[str] = DEFAULT_PREFIXES) -> List[str]:
    """
    Unlink ``{shm_dir}/{prefix}*`` files owned by the current uid.
    
        Returns the list of files actually unlinked. Never raises; logs at debug
        level on per-file failures.
    """
    ...
def safe_unlink_if_owner(path: str) -> bool:
    """
    Unlink ``path`` only if it's owned by the current uid. Returns True on success.
    """
    ...
