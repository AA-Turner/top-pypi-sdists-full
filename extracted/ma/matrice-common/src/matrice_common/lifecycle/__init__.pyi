"""Stub file for lifecycle directory."""
from typing import Any, Callable, List, Optional, Tuple

# Constants
logger: Any = ...  # From cuda_finalize
DEFAULT_ENV_GATE: str = ...  # From drop_caches
logger: Any = ...  # From drop_caches
logger: Any = ...  # From process_lifecycle
DEFAULT_PREFIXES: Tuple[Any, ...] = ...  # From shm_cleanup
logger: Any = ...  # From shm_cleanup

# Functions
# From cuda_finalize
def finalize_cuda() -> None:
    """
    Run the canonical CUDA teardown sequence; never raises.
    """
    ...

# From drop_caches
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

# From process_lifecycle
def register_shutdown(callback: Callable[[], None]) -> None:
    """
    Register ``callback`` to run on process shutdown.
    
        Args:
            callback: Zero-arg callable. Exceptions are caught and logged.
            weight: Lower runs first; ties broken by registration order.
            name: Optional label used in logs; defaults to ``callback.__qualname__``.
    """
    ...

# From process_lifecycle
def run_shutdown_now() -> None:
    """
    Run all registered callbacks immediately and clear the registry.
    
        Idempotent: subsequent calls are no-ops. Useful in tests and for callers
        that want to drive shutdown explicitly without waiting for atexit.
    """
    ...

# From shm_cleanup
def cleanup_owned_shm(prefixes: Any[str] = DEFAULT_PREFIXES) -> List[str]:
    """
    Unlink ``{shm_dir}/{prefix}*`` files owned by the current uid.
    
        Returns the list of files actually unlinked. Never raises; logs at debug
        level on per-file failures.
    """
    ...

# From shm_cleanup
def safe_unlink_if_owner(path: str) -> bool:
    """
    Unlink ``path`` only if it's owned by the current uid. Returns True on success.
    """
    ...

from . import cuda_finalize, drop_caches, process_lifecycle, shm_cleanup