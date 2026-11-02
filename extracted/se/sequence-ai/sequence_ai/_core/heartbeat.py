"""
The robot's SDK heard from by its worker: every EVERY_S - a fifth of WINDOW_S, 2 s, the figures Viam's sessions keep -
a Policy that holds a worker says on its stream, in a message that is no request, how its arm stands (stale.py): "acting"
while it asks ahead, "waiting" while it asks for none ahead, "stale" while the answer it plays ran out with no next one
in hand - why, and for how long - and its stretches so far. The worker says it on its GET /robots, the platform on GET /v1/robots/{name}
and `seq robot status`: a robot alive and acting, alive with its loop stuck, or not heard from for its window - its
process gone, hung whole, or its link down. A stretch the worker hears under way is two lines of the policy's log,
`seq policy logs`: heard begun, and heard ended.
Best effort, on a thread of its own, from the first observe() or act() until close(): with no stream open it is one not
heard, and the robot's code hears nothing of it. It counts for nothing more than this: while it is heard from, its
worker keeps the robot's place on its copy between two episodes, however long the reset
 - no act, no seat on the platform, and nothing the worker's idle time goes by.


"""
from __future__ import annotations

import threading
import weakref
from datetime import datetime, timezone
from typing import Any, Optional

WINDOW_S = 2.0
EVERY_S = WINDOW_S / 5


def said(state: Any, now: Optional[datetime] = None) -> dict:
    """A heartbeat's body from a Policy's `stale` (stale.StaleState): its window, its state, and its stale stretch - the
    one under way, else the last - with how many there were, how long the ended ones lasted together, and the act it
    waited on ("late": its request id, which the worker's log lines of the stretch carry, so `--rid` finds them)."""
    under = state.now
    body: dict = {"window_s": WINDOW_S,
                  "state": "stale" if under is not None else "acting" if state.ahead else "waiting"}
    one = under or state.last
    if one is not None:
        stale = {"reason": one.reason, "events": state.events, "stale_s": state.stale_s}
        if one.request_id:
            stale["request_id"] = one.request_id
        if under is not None:
            at = now or datetime.now(timezone.utc)
            stale["for_s"] = round(max(0.0, (at - under.at).total_seconds()), 3)
        body["stale"] = stale
    return body


class Heartbeat:
    """The thread that sends them for `owner`, a Policy: every `every_s` its transport's heartbeat() - which sends none
    before it holds a worker - with its `stale` said (said), until close(), or until the Policy is closed or gone. The
    Policy is held by a weak reference alone, never while the thread waits or sends: one dropped without close() is
    still collected, its seat given back (policy._OPEN), and its heartbeats end with it."""

    def __init__(self, owner: Any, every_s: Optional[float] = None) -> None:
        self._owner = weakref.ref(owner)
        self._every = EVERY_S if every_s is None else every_s
        self._stop = threading.Event()
        self._thread = threading.Thread(target=self._run, daemon=True, name="seq-heartbeat")
        self._thread.start()

    def _run(self) -> None:
        while not self._stop.wait(self._every):
            owner = self._owner()
            if owner is None or getattr(owner, "_closed", False):
                return
            send, state = getattr(owner._t, "heartbeat", None), owner._stale.state
            del owner
            try:
                send(said(state))
            except Exception:
                pass

    def close(self) -> None:
        """No more heartbeats: the thread ends at once, or as the one on its way is answered."""
        self._stop.set()
        self._thread.join(0.1)
