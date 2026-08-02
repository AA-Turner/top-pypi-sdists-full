"""Auto-generated stub for module: _mp_patch."""

import multiprocessing.resource_tracker as _rt

# Functions
def install_resource_tracker_patch() -> None: ...
    """
    Install the semaphore-unlink no-op patch on this interpreter.
    
        Must run BEFORE any ``mp.Queue``/``mp.Lock`` is created. Safe to call
        repeatedly and from any process.
    """
