"""The owner's close barrier: before it releases the run, wait, bounded by `PROBE_SAMPLES_CLOSE_WAIT`
(default 120 s), until capture shows every declared producer's last seal received (RL plan §3.4)."""

from __future__ import annotations

import os
import time
from collections.abc import Callable, Mapping
from typing import Any

#: Seconds the owner waits for producers' last seals before it releases the run anyway.
CLOSE_WAIT_ENV = "PROBE_SAMPLES_CLOSE_WAIT"
DEFAULT_CLOSE_WAIT_SECONDS = 120.0
POLL_SECONDS = 2.0


def get_close_wait(env: Mapping[str, str] | None = None) -> float:
    """`PROBE_SAMPLES_CLOSE_WAIT` in seconds; unreadable or negative is the default."""
    raw = (env if env is not None else os.environ).get(CLOSE_WAIT_ENV, "")
    try:
        value = float(raw)
    except ValueError:
        return DEFAULT_CLOSE_WAIT_SECONDS
    return value if value >= 0 else DEFAULT_CLOSE_WAIT_SECONDS


#: Capture reasons (`CaptureReasonCode`) a producer's late delivery can still clear: the barrier
#: waits while one is shown. Others (in progress, no manifest, a gone producer, a refused batch)
#: no wait fixes.
WAITED_REASONS = frozenset(
    {"missing_samples", "unsealed_step", "producer_open", "producer_silent", "bundle_missing"}
)


def has_every_last_seal(capture: Mapping[str, Any]) -> bool:
    """Whether a capture answer (`Capture`) shows every declared producer's last seal received:
    complete, or no reason left that a late delivery could clear (a cut list is not trusted)."""
    if capture.get("is_complete"):
        return True
    reasons = capture.get("reasons")
    if not isinstance(reasons, list) or capture.get("is_truncated"):
        return False
    return not any(
        not isinstance(reason, Mapping) or reason.get("code") in WAITED_REASONS for reason in reasons
    )


def _is_lasting(exc: Exception) -> bool:
    """A read failure no retry clears: a refusal or a missing route, not a busy server."""
    from ...delivery.ops.classify import classify

    return classify(exc) in ("permanent", "auth")


def wait_for_last_seals(
    fetch_capture: Callable[[], Mapping[str, Any]],
    *,
    timeout: float | None = None,
    clock: Callable[[], float] = time.monotonic,
    sleep: Callable[[float], None] = time.sleep,
) -> bool:
    """Poll capture until every producer's last seal is in, or ``timeout`` (default: the env knob)
    runs out. True when they all arrived; a producer still silent never holds the run (its samples
    land later and flip capture to yes). A busy or unreachable server counts as not yet; a refusal
    (no such route on an older server, no access) ends the wait at once."""
    budget = get_close_wait() if timeout is None else max(0.0, timeout)
    deadline = clock() + budget
    while True:
        try:
            if has_every_last_seal(fetch_capture()):
                return True
        except Exception as exc:  # noqa: BLE001 -- never a raise at close
            if _is_lasting(exc):
                return False  # no route (an older server), no access: no wait answers it
        left = deadline - clock()
        if left <= 0:
            return False
        sleep(min(POLL_SECONDS, left))
