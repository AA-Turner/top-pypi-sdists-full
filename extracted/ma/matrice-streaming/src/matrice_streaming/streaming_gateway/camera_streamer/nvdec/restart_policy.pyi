"""Auto-generated stub for module: restart_policy."""
from typing import Any, Dict, List, Optional

from __future__ import annotations
from dataclasses import dataclass
import logging
import os
import threading
import time

# Constants
log: Any

# Functions
def resolve_restart_policy(env: Optional[Mapping[str, str]] = None) -> Any: ...
    """
    Build a :class:`RestartPolicy` from the environment.
    
        Reads all six operator-facing knobs the decode loop honours:
        ``MATRICE_SG_RESTART_COOLDOWN``, ``MATRICE_SG_GIVEUP_COOLDOWN``,
        ``MATRICE_SG_MAX_RESTARTS``, ``MATRICE_SG_RESTART_WINDOW``,
        ``MATRICE_SG_STALL_SEC`` and ``MATRICE_SG_BOOTSTRAP_SEC``.
    
        Malformed values fall back to the documented default with a warning; this
        function never raises, because a typo in a deployment env var must not stop
        the gateway from starting.
    
        Args:
            env: mapping to read from. Defaults to ``os.environ``; injectable so
                callers (and tests) need no process-global mutation.
    
        Returns:
            The resolved policy.
    """

# Classes
class RestartPolicy:
    """
    Resolved restart / stall tunables for the decode loop.
    
        Frozen: the policy is resolved once at construction and shared across decode
        threads, so it must not be mutable state anybody can drift.
    
        INVARIANT — ``window_sec / cooldown_sec >= max_restarts``. Only one restart
        is *accepted* per ``cooldown_sec``, so at most ``window_sec / cooldown_sec``
        of them can ever sit inside the rolling window at once. If that ratio drops
        below ``max_restarts`` the count can never exceed the threshold and give-up
        becomes unreachable: a dead camera retries at full volume forever, which is
        the exact failure this module exists to end. With the defaults the budget is
        ``300 / 30 = 10`` against a threshold of ``3``, so a dead source gives up
        after ~4 accepted failures (~120s). :func:`resolve_restart_policy` warns when
        an override breaks the invariant; see :attr:`giveup_reachable`.
    
        Attributes:
            cooldown_sec: minimum seconds between error-triggered restarts.
            giveup_cooldown_sec: slow-probe cooldown once given up.
            max_restarts: accepted restarts within ``window_sec`` before give-up.
            window_sec: rolling window for the restart count (0 disables pruning).
            stall_sec: seconds of no frames before the stream counts as stalled.
            bootstrap_sec: grace period before stall detection arms.
    """

    def giveup_reachable(self: Any) -> bool: ...
        """
        True if the give-up threshold can actually be crossed.
        
                See the invariant on the class: give-up needs *more* than
                ``max_restarts`` accepted restarts inside the window, and the cooldown
                caps how many can fit.
        """

    def restart_budget_per_window(self: Any) -> float: ...
        """
        How many restarts the cooldown lets into one window (``inf`` if 0).
        """

class StreamSupervisor:
    """
    Cooldown-aware restart supervisor for a single decode worker.
    
        Args:
            cooldown_sec: minimum seconds between error-triggered restarts.
            eof_cooldown_sec: minimum seconds between EOF-triggered restarts.
            max_restarts: max restarts within *window_sec* before give-up.
            window_sec: rolling window for the max_restarts count.
            clock: injectable time function (seconds); defaults to time.monotonic.
            on_give_up: optional callback invoked once when the give-up threshold
                is first reached (receives the camera_id).
            giveup_cooldown_sec: slow-probe cooldown applied once given up; floored
                at cooldown_sec so it is never shorter than the normal cadence.
    """

    def __init__(self: Any, cooldown_sec: float = _DEFAULT_COOLDOWN_SEC, eof_cooldown_sec: float = _DEFAULT_EOF_COOLDOWN_SEC, max_restarts: int = _DEFAULT_MAX_RESTARTS, window_sec: float = _DEFAULT_WINDOW_SEC, clock: Optional[Callable[[], float]] = None, on_give_up: Optional[Callable[[str], None]] = None, giveup_cooldown_sec: float = _DEFAULT_GIVEUP_COOLDOWN_SEC) -> None: ...

    def from_policy(cls: Any, policy: Any, clock: Optional[Callable[[], float]] = None, on_give_up: Optional[Callable[[str], None]] = None, eof_cooldown_sec: float = _DEFAULT_EOF_COOLDOWN_SEC) -> Any: ...
        """
        Build a supervisor from a resolved :class:`RestartPolicy`.
        
                The policy's stall knobs are deliberately not consumed here: stall
                detection is the decode loop's job, not the supervisor's.
        """

    def on_eof(self: Any, camera_id: str) -> bool: ...
        """
        Record an EOF; return True if a restart should proceed now.
        """

    def on_error(self: Any, camera_id: str, exc: Optional[Exception] = None) -> bool: ...
        """
        Record an error; return True if a restart should proceed now.
        
                Returns False if inside the cooldown window (caller should skip restart).
        """

    def reset(self: Any, camera_id: str, keep_anchor: bool = False) -> None: ...
        """
        Clear restart history for a camera (call on *proven* recovery).
        
                This is the only thing that clears the sticky give-up flag, so a source
                that comes back returns to the normal cadence immediately.
        
                Args:
                    camera_id: the camera whose history to clear.
                    keep_anchor: keep ``last_attempt`` — the cooldown anchor — instead of
                        dropping the whole state. Recovery must not shorten the minimum
                        spacing between restarts: dropping the anchor let a camera that
                        *reopens* fine but immediately re-stalls restart once per stall
                        detection (10s) instead of once per ``cooldown_sec`` (30s), which
                        is the 15-30 restarts/min flapping this class exists to prevent.
                        Keeping the anchor costs a genuinely-recovered camera nothing —
                        by the time it errors again the anchor is older than the cooldown,
                        so the next restart is accepted immediately.
        """

    def should_give_up(self: Any, camera_id: str) -> bool: ...
        """
        Return True if max_restarts within window_sec has been exceeded.
        
                Sticky: once set it stays until :meth:`reset` is called on recovery, so
                the slow-probe cadence does not oscillate as old timestamps age out.
        """

