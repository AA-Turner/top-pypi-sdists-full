"""Auto-generated stub for module: circuit_breaker."""
from typing import Any, Optional

from __future__ import annotations
from enum import Enum
import threading
import time

# Classes
class CircuitBreaker:
    """
    Thread-safe circuit breaker with CLOSED/OPEN/HALF_OPEN transitions.
    
        Args:
            failure_threshold: consecutive failures before opening.
            cooldown_sec: seconds to stay open before moving to half-open.
            clock: callable returning current time in seconds (injectable for tests).
    """

    def __init__(self: Any, failure_threshold: int = 3, cooldown_sec: float = 60.0, clock: Optional[Callable[[], float]] = None) -> None: ...

    def current_cooldown_sec(self: Any) -> float: ...

    def failure_count(self: Any) -> int: ...

    def failure_threshold(self: Any) -> int: ...

    def is_open(self: Any) -> bool: ...

    def open_with_cooldown(self: Any, cooldown_sec: float) -> None: ...
        """
        Force OPEN state with a new cooldown; used for exponential backoff on re-open.
        """

    def record_failure(self: Any) -> None: ...

    def record_success(self: Any) -> None: ...

    def reset(self: Any) -> None: ...

    def seconds_since_open(self: Any) -> float: ...
        """
        Seconds elapsed since the breaker last entered OPEN state (0 if not open).
        """

    def state(self: Any) -> str: ...

