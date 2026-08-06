"""Auto-generated stub for module: health_monitor."""
from typing import Any, Optional

from __future__ import annotations
from matrice_streaming.support.circuit_breaker import CircuitBreaker
import logging
import threading
import time

# Constants
log: Any

# Classes
class HealthMonitor:
    """
    Periodic health-check loop for a streaming action.
    
        The loop runs inside a daemon thread (caller's responsibility). It owns:
        - the action-ID validation cadence (separate, longer interval)
        - the health-check / restart decision policy
        - CircuitBreaker state for health outcomes (visible to callers after run() returns)
    
        All side effects are expressed as callbacks so the class is unit-testable
        without a live StreamingAction instance.
    
        Args:
            circuit_breaker: records health-check outcomes.
            stop_event: shared with the owning StreamingAction; loop exits when set.
            monitoring_interval: seconds between health checks.
            action_id_check_interval: seconds between action-ID validation probes.
            max_restart_attempts: consecutive unhealthy ticks allowed before giving up.
            auto_restart: whether to attempt a restart on unhealthy ticks.
    """

    def __init__(self: Any, circuit_breaker: Any, stop_event: Any, monitoring_interval: float = 30.0, action_id_check_interval: float = 300.0, max_restart_attempts: int = 3, auto_restart: bool = True) -> None: ...

    def run(self: Any, is_running: Any, is_healthy: Any, check_action_id: Any, on_healthy: Any, on_unhealthy: Any, on_action_id_mismatch: Any, on_restart: Any, on_fatal: Any, on_error: Optional[Callable[[str], None]] = None) -> None: ...
        """
        Run the health-check loop (blocking; call from a daemon thread).
        
                Args:
                    is_running: returns True while the action is active.
                    is_healthy: returns True when the gateway is healthy.
                    check_action_id: returns False if the action ID has been superseded.
                    on_healthy: called on each healthy tick — reset restart counter,
                        send heartbeat, collect metrics.
                    on_unhealthy: called on each unhealthy tick — update failure stats.
                    on_action_id_mismatch: called with error message when ID mismatch
                        is detected; caller should stop the action.
                    on_restart: called with (attempt, max) when a restart should be
                        triggered; caller spawns the restart thread and this run() exits.
                    on_fatal: called with error message when max restarts are exceeded.
                    on_error: optional; called with the message when an iteration of the
                        loop raises, so the owner can record it in its own stats.
        """

