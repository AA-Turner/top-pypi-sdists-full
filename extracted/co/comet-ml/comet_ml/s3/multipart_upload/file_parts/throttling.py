# -*- coding: utf-8 -*-
# *******************************************************
#   ____                     _               _
#  / ___|___  _ __ ___   ___| |_   _ __ ___ | |
# | |   / _ \| '_ ` _ \ / _ \ __| | '_ ` _ \| |
# | |__| (_) | | | | | |  __/ |_ _| | | | | | |
#  \____\___/|_| |_| |_|\___|\__(_)_| |_| |_|_|
#
#  Sign up for free at https://www.comet.com
#  Copyright (C) 2015-2025 Comet ML INC
#  This source code is licensed under the MIT license.
# *******************************************************
import logging
import random
import threading
import time
from typing import Optional

LOGGER = logging.getLogger(__name__)

# How long the brake holds the first time, and the ceiling it grows to. A part that
# was told to slow down will wait at least the first value before trying again, and
# consecutive throttles double it. The ceiling is well inside the presigned URL
# lifetime so that waiting never outlives the URL being waited on.
INITIAL_HOLD_SECONDS = 0.5
MAX_HOLD_SECONDS = 30.0

# Once this many consecutive sends succeed, the hold is back to its initial value.
# Recovering on a count rather than a clock means the brake releases as fast as the
# endpoint actually allows, without polling anything.
SUCCESSES_TO_RECOVER = 10


class ThrottleGate(object):
    """A brake shared by every part upload, so one throttled part slows them all.

    Retrying a throttled request on its own is not enough to respect a rate limit.
    The limit applies to the whole process, so the other parts in flight are the
    reason the limit was hit, and letting them carry on at full rate while one of
    them backs off just moves which request gets rejected. This closes for everyone
    when any part is throttled.

    Holds grow while throttling continues and shrink once it stops, which keeps a
    brief burst cheap and a sustained limit survivable. Nothing here runs on a timer
    or a background thread: waiters block on an Event with a deadline, and the state
    only changes when a request reports its outcome.
    """

    def __init__(
        self,
        initial_hold: float = INITIAL_HOLD_SECONDS,
        max_hold: float = MAX_HOLD_SECONDS,
        successes_to_recover: int = SUCCESSES_TO_RECOVER,
    ):
        self._initial_hold = initial_hold
        self._max_hold = max_hold
        self._successes_to_recover = successes_to_recover

        self._lock = threading.Lock()
        # Set means open. Everything waits when it is cleared.
        self._open = threading.Event()
        self._open.set()
        self._hold = initial_hold
        self._open_at = 0.0
        self._successes = 0
        self._throttles = 0

    @property
    def throttle_count(self) -> int:
        """How many times the brake has been applied. For logging and tests."""
        with self._lock:
            return self._throttles

    @property
    def current_hold(self) -> float:
        with self._lock:
            return self._hold

    def wait_until_open(self, timeout: Optional[float] = None) -> bool:
        """Blocks while the brake is on. True if it is open, False if timeout hit.

        Called before every attempt, including the first, so a part that starts
        while the endpoint is complaining waits its turn instead of adding to the
        pile.
        """
        deadline = None if timeout is None else time.monotonic() + timeout

        while True:
            with self._lock:
                remaining = self._open_at - time.monotonic()
                if remaining <= 0:
                    # The hold has expired. Reopen so the next caller goes straight
                    # through, and let this one proceed.
                    self._open.set()
                    return True

            wait_for = remaining
            if deadline is not None:
                left = deadline - time.monotonic()
                if left <= 0:
                    return False
                wait_for = min(wait_for, left)

            # Waits for the hold to elapse, or wakes early if it is lifted.
            self._open.wait(timeout=wait_for)

    def report_throttled(
        self,
        retry_after: Optional[float] = None,
        max_hold: Optional[float] = None,
    ) -> float:
        """Applies the brake. Returns how long it will hold, in seconds.

        retry_after is the server's own instruction when it sent one, and it wins
        over the computed hold: a server that says how long to wait knows better
        than a doubling heuristic.

        max_hold caps this particular hold. The caller passes what remains of its own
        retry budget, so a server asking for an hour cannot park every upload in the
        process for an hour when nothing here would still be allowed to retry by
        then.

        Reports arriving while the brake is already on belong to the same episode and
        do not escalate it again. Every part in flight is throttled at more or less
        the same instant, so counting each one would treat a single "slow down" as
        eight of them: with eight parts and a 0.5s floor, the first burst alone drove
        the hold to its 30s ceiling. The doubling is meant to escalate across rounds
        of throttling, not across the parts within one round.
        """
        with self._lock:
            self._throttles += 1
            self._successes = 0
            now = time.monotonic()

            if self._open_at > now:
                # Same episode, reported by another part. Hold as it stands, unless
                # this response carries a longer instruction than the one in force.
                if retry_after is not None:
                    self._open_at = max(
                        self._open_at, now + self._capped(retry_after, max_hold)
                    )

                remaining = self._open_at - now
                LOGGER.debug(
                    "Upload rate limited again while already holding, %.2fs left "
                    "(throttle #%d)",
                    remaining,
                    self._throttles,
                )
                return remaining

            hold = self._hold
            self._hold = min(self._hold * 2, self._max_hold)

            if retry_after is not None:
                hold = max(hold, retry_after)
            # Spread the reopening slightly, so parts released by one hold do not
            # all arrive in the same instant and re-trigger it.
            hold *= 1.0 + 0.25 * random.random()
            hold = self._capped(hold, max_hold)

            self._open_at = now + hold
            self._open.clear()

            LOGGER.debug(
                "Upload rate limited, holding all part uploads for %.2fs "
                "(throttle #%d, retry_after=%s)",
                hold,
                self._throttles,
                retry_after,
            )
            return hold

    @staticmethod
    def _capped(hold: float, max_hold: Optional[float]) -> float:
        if max_hold is None:
            return hold

        return max(0.0, min(hold, max_hold))

    def report_success(self) -> None:
        """A send got through. Enough of these and the hold returns to its floor."""
        with self._lock:
            if self._hold == self._initial_hold:
                return

            self._successes += 1
            if self._successes >= self._successes_to_recover:
                self._hold = self._initial_hold
                self._successes = 0
                LOGGER.debug("Upload rate limit appears to have cleared.")


_default_gate = ThrottleGate()


def default_gate() -> ThrottleGate:
    """The process-wide brake.

    A rate limit belongs to the account and endpoint rather than to any one upload,
    so every part in the process shares one, whichever experiment or pool it came
    from. Injectable everywhere it is used, which is how the tests get an isolated
    one.
    """
    return _default_gate
