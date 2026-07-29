"""Auto-generated stub for module: process_lifecycle."""
from typing import Any, Callable, Optional

# Constants
logger: Any

# Functions
def register_shutdown(callback: Callable[[], None]) -> None:
    """
    Register ``callback`` to run on process shutdown.
    
        Args:
            callback: Zero-arg callable. Exceptions are caught and logged.
            weight: Lower runs first; ties broken by registration order.
            name: Optional label used in logs; defaults to ``callback.__qualname__``.
    """
    ...
def run_shutdown_now() -> None:
    """
    Run all registered callbacks immediately and clear the registry.
    
        Idempotent: subsequent calls are no-ops. Useful in tests and for callers
        that want to drive shutdown explicitly without waiting for atexit.
    """
    ...
