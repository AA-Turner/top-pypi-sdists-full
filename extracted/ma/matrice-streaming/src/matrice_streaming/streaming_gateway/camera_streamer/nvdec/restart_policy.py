"""Cooldown-aware, give-up-capable restart supervisor for decode workers.

Pure logic (no GStreamer/GPU imports) extracted from ``nvdec.py`` so the
restart / back-off / give-up policy can be unit-tested in isolation — the
``nvdec.py`` decode loop is GPU-only and excluded from the coverage denominator.

Why this exists: a permanently-unreachable source (e.g. an RTSP URL returning
"Not found") must not retry its demuxer forever at ERROR level. The old path
had a fixed cooldown but no give-up state, so a dead camera re-emitted a full
``logger.exception`` traceback every cooldown window until the gateway was
restarted.

Behaviour: :meth:`StreamSupervisor.on_error` / :meth:`on_eof` gate restart
attempts to at most one per ``cooldown_sec``. After ``max_restarts`` accepted
restarts within ``window_sec`` the supervisor enters a **sticky** "given up"
state: :meth:`should_give_up` returns True, the effective cooldown stretches to
``giveup_cooldown_sec`` (slow-probe), and the ``on_give_up`` callback fires
exactly once (the caller uses these to demote logging and keep probing quietly).
*Proven* recovery — frames flowing again, not merely a demuxer that reopened —
calls :meth:`StreamSupervisor.reset` to leave the state and re-arm the normal
cadence, so a camera whose source comes back recovers automatically.
``reset(..., keep_anchor=True)`` keeps the cooldown anchor while clearing the
history, so recovery never zeroes the minimum spacing between restarts (see
:meth:`StreamSupervisor.reset`).

:func:`resolve_restart_policy` is the single reader of the operator knobs. It
also resolves the two *stall-detection* values (``MATRICE_SG_STALL_SEC``,
``MATRICE_SG_BOOTSTRAP_SEC``): they are not restart-cadence knobs, but they are
read by the same decode loop, and keeping all six in one dependency-free module
is what stops a future refactor from dropping one silently.
"""

from __future__ import annotations

import logging
import os
import threading
import time
from dataclasses import dataclass
from typing import Callable, Dict, List, Mapping, Optional

log = logging.getLogger(__name__)

# Defaults for the env knobs resolved by resolve_restart_policy below
# (MATRICE_SG_RESTART_COOLDOWN, MATRICE_SG_GIVEUP_COOLDOWN, MATRICE_SG_MAX_RESTARTS,
# MATRICE_SG_RESTART_WINDOW, MATRICE_SG_STALL_SEC, MATRICE_SG_BOOTSTRAP_SEC).
# The cooldown/window/max_restarts three carry a reachability invariant — see
# RestartPolicy, which owns it and warns when an override breaks it.
_DEFAULT_COOLDOWN_SEC = 30.0
_DEFAULT_EOF_COOLDOWN_SEC = 2.0
_DEFAULT_GIVEUP_COOLDOWN_SEC = 300.0
_DEFAULT_MAX_RESTARTS = 3
_DEFAULT_WINDOW_SEC = 300.0
# Stall detection, not restart cadence: how long a stream may produce no frames
# before the decode loop calls it stalled, and the grace period after a (re)open
# before that detection arms (a cold RTSP open legitimately yields nothing for
# several seconds). Resolved here so all six operator knobs live together.
_DEFAULT_STALL_SEC = 10.0
_DEFAULT_BOOTSTRAP_SEC = 30.0

_ENV_RESTART_COOLDOWN_SEC = "MATRICE_SG_RESTART_COOLDOWN"
_ENV_GIVEUP_COOLDOWN_SEC = "MATRICE_SG_GIVEUP_COOLDOWN"
_ENV_MAX_RESTARTS = "MATRICE_SG_MAX_RESTARTS"
_ENV_RESTART_WINDOW_SEC = "MATRICE_SG_RESTART_WINDOW"
_ENV_STALL_SEC = "MATRICE_SG_STALL_SEC"
_ENV_BOOTSTRAP_SEC = "MATRICE_SG_BOOTSTRAP_SEC"


@dataclass(frozen=True)
class RestartPolicy:
    """Resolved restart / stall tunables for the decode loop.

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

    cooldown_sec: float = _DEFAULT_COOLDOWN_SEC
    giveup_cooldown_sec: float = _DEFAULT_GIVEUP_COOLDOWN_SEC
    max_restarts: int = _DEFAULT_MAX_RESTARTS
    window_sec: float = _DEFAULT_WINDOW_SEC
    stall_sec: float = _DEFAULT_STALL_SEC
    bootstrap_sec: float = _DEFAULT_BOOTSTRAP_SEC

    @property
    def restart_budget_per_window(self) -> float:
        """How many restarts the cooldown lets into one window (``inf`` if 0)."""
        if self.cooldown_sec <= 0 or self.window_sec <= 0:
            return float("inf")
        return self.window_sec / self.cooldown_sec

    @property
    def giveup_reachable(self) -> bool:
        """True if the give-up threshold can actually be crossed.

        See the invariant on the class: give-up needs *more* than
        ``max_restarts`` accepted restarts inside the window, and the cooldown
        caps how many can fit.
        """
        return self.restart_budget_per_window > self.max_restarts


def _env_int(env: Mapping[str, str], key: str, default: int, floor: int) -> int:
    """Read ``key`` as an int, clamped to ``floor``. Never raises."""
    raw = env.get(key)
    if raw is None or str(raw).strip() == "":
        return default
    try:
        value = int(str(raw).strip())
    except (TypeError, ValueError):
        log.warning("%s=%r is not an integer; using default %s", key, raw, default)
        return default
    if value < floor:
        log.warning("%s=%r is below the minimum %s; clamping", key, raw, floor)
        return floor
    return value


def _env_float(env: Mapping[str, str], key: str, default: float, floor: float) -> float:
    """Read ``key`` as a float, clamped to ``floor``. Never raises."""
    raw = env.get(key)
    if raw is None or str(raw).strip() == "":
        return default
    try:
        value = float(str(raw).strip())
    except (TypeError, ValueError):
        log.warning("%s=%r is not a number; using default %s", key, raw, default)
        return default
    if value < floor:
        log.warning("%s=%r is below the minimum %s; clamping", key, raw, floor)
        return floor
    return value


def resolve_restart_policy(env: Optional[Mapping[str, str]] = None) -> RestartPolicy:
    """Build a :class:`RestartPolicy` from the environment.

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
    source = os.environ if env is None else env

    policy = RestartPolicy(
        cooldown_sec=_env_float(source, _ENV_RESTART_COOLDOWN_SEC, _DEFAULT_COOLDOWN_SEC, floor=0.0),
        giveup_cooldown_sec=_env_float(source, _ENV_GIVEUP_COOLDOWN_SEC, _DEFAULT_GIVEUP_COOLDOWN_SEC, floor=0.0),
        max_restarts=_env_int(source, _ENV_MAX_RESTARTS, _DEFAULT_MAX_RESTARTS, floor=1),
        window_sec=_env_float(source, _ENV_RESTART_WINDOW_SEC, _DEFAULT_WINDOW_SEC, floor=0.0),
        stall_sec=_env_float(source, _ENV_STALL_SEC, _DEFAULT_STALL_SEC, floor=0.0),
        bootstrap_sec=_env_float(source, _ENV_BOOTSTRAP_SEC, _DEFAULT_BOOTSTRAP_SEC, floor=0.0),
    )

    if not policy.giveup_reachable:
        # Not fatal — the supervisor still throttles restarts, which is most of
        # the value — but give-up (and with it the quiet slow-probe cadence) can
        # never trip under this configuration, so a dead camera logs forever.
        log.warning(
            "%s=%s and %s=%s admit at most %.1f restarts per window, which is not above %s=%s; "
            "give-up can never trip and a permanently-dead source will keep retrying at full volume",
            _ENV_RESTART_COOLDOWN_SEC,
            policy.cooldown_sec,
            _ENV_RESTART_WINDOW_SEC,
            policy.window_sec,
            policy.restart_budget_per_window,
            _ENV_MAX_RESTARTS,
            policy.max_restarts,
        )
    return policy


class _CameraState:
    """Per-camera restart bookkeeping."""

    __slots__ = ("restarts", "last_attempt", "given_up")

    def __init__(self) -> None:
        self.restarts: List[float] = []  # accepted-restart timestamps within the window
        self.last_attempt: float = float("-inf")  # clock() of the last accepted restart
        self.given_up: bool = False  # sticky; cleared only by reset()


class StreamSupervisor:
    """Cooldown-aware restart supervisor for a single decode worker.

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

    def __init__(
        self,
        cooldown_sec: float = _DEFAULT_COOLDOWN_SEC,
        eof_cooldown_sec: float = _DEFAULT_EOF_COOLDOWN_SEC,
        max_restarts: int = _DEFAULT_MAX_RESTARTS,
        window_sec: float = _DEFAULT_WINDOW_SEC,
        clock: Optional[Callable[[], float]] = None,
        on_give_up: Optional[Callable[[str], None]] = None,
        giveup_cooldown_sec: float = _DEFAULT_GIVEUP_COOLDOWN_SEC,
    ) -> None:
        self.cooldown_sec = max(0.0, float(cooldown_sec))
        self.eof_cooldown_sec = max(0.0, float(eof_cooldown_sec))
        self.giveup_cooldown_sec = max(self.cooldown_sec, float(giveup_cooldown_sec))
        self.max_restarts = max(1, int(max_restarts))
        self.window_sec = max(0.0, float(window_sec))
        self._clock = clock or time.monotonic
        self._on_give_up = on_give_up
        self._by_cam: Dict[str, _CameraState] = {}
        # Decoders run one thread per pool; cameras are partitioned across them,
        # but the supervisor instance is shared, so guard the dict.
        self._lock = threading.Lock()

    @classmethod
    def from_policy(
        cls,
        policy: RestartPolicy,
        clock: Optional[Callable[[], float]] = None,
        on_give_up: Optional[Callable[[str], None]] = None,
        eof_cooldown_sec: float = _DEFAULT_EOF_COOLDOWN_SEC,
    ) -> "StreamSupervisor":
        """Build a supervisor from a resolved :class:`RestartPolicy`.

        The policy's stall knobs are deliberately not consumed here: stall
        detection is the decode loop's job, not the supervisor's.
        """
        return cls(
            cooldown_sec=policy.cooldown_sec,
            eof_cooldown_sec=eof_cooldown_sec,
            max_restarts=policy.max_restarts,
            window_sec=policy.window_sec,
            clock=clock,
            on_give_up=on_give_up,
            giveup_cooldown_sec=policy.giveup_cooldown_sec,
        )

    def _state(self, camera_id: str) -> _CameraState:
        st = self._by_cam.get(camera_id)
        if st is None:
            st = _CameraState()
            self._by_cam[camera_id] = st
        return st

    def _prune(self, st: _CameraState, now: float) -> None:
        """Drop restart timestamps older than the rolling window."""
        if self.window_sec <= 0:
            return
        cutoff = now - self.window_sec
        if st.restarts and st.restarts[0] < cutoff:
            st.restarts = [t for t in st.restarts if t >= cutoff]

    def _accept(self, camera_id: str, cooldown: float) -> bool:
        """Record a restart request; return True if it should proceed now.

        Returns False while inside the (possibly slow-probe) cooldown window.
        The give-up flag is sticky and only fires its callback once.
        """
        with self._lock:
            st = self._state(camera_id)
            now = self._clock()
            effective = self.giveup_cooldown_sec if st.given_up else cooldown
            if now - st.last_attempt < effective:
                return False
            st.last_attempt = now
            st.restarts.append(now)
            self._prune(st, now)
            fire_give_up = not st.given_up and len(st.restarts) > self.max_restarts
            if fire_give_up:
                st.given_up = True
            callback = self._on_give_up if fire_give_up else None
        # Fire the callback outside the lock — it may log or touch stream state.
        if callback is not None:
            try:
                callback(camera_id)
            except Exception:  # pragma: no cover - a callback must never break restart
                log.debug("on_give_up callback raised for %s", camera_id, exc_info=True)
        return True

    def on_eof(self, camera_id: str) -> bool:
        """Record an EOF; return True if a restart should proceed now."""
        return self._accept(camera_id, self.eof_cooldown_sec)

    def on_error(self, camera_id: str, exc: Optional[Exception] = None) -> bool:
        """Record an error; return True if a restart should proceed now.

        Returns False if inside the cooldown window (caller should skip restart).
        """
        return self._accept(camera_id, self.cooldown_sec)

    def reset(self, camera_id: str, keep_anchor: bool = False) -> None:
        """Clear restart history for a camera (call on *proven* recovery).

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
        with self._lock:
            if not keep_anchor:
                self._by_cam.pop(camera_id, None)
                return
            st = self._by_cam.get(camera_id)
            if st is None:
                # Never restarted: there is no anchor to keep and no history to
                # clear. Do NOT create state here — a camera that has only ever
                # streamed must stay absent from the dict.
                return
            st.restarts = []
            st.given_up = False

    def should_give_up(self, camera_id: str) -> bool:
        """Return True if max_restarts within window_sec has been exceeded.

        Sticky: once set it stays until :meth:`reset` is called on recovery, so
        the slow-probe cadence does not oscillate as old timestamps age out.
        """
        with self._lock:
            st = self._by_cam.get(camera_id)
            return bool(st and st.given_up)
