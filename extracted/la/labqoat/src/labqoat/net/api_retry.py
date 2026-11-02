"""When a management API request is sent again after a refusal the server said was temporary."""

from __future__ import annotations

import json
import time
from collections.abc import Iterator
from typing import ClassVar


class ApiRetry:
    """Ride out short refusals: contention, rate limits, a restarting service.

    A request the server refused because of contention or a rate limit was never applied, so any request is
    sent again. A gateway failure or a lost connection may have reached the server, so only a request that
    does the same when sent twice is repeated: reads, deletions, puts and anything with an idempotency key.
    A streamed body cannot be sent twice and is never retried. The wait follows ``Retry-After`` when the
    server gives one, doubling from half a second otherwise, within six attempts and a fixed overall time.
    """

    SECONDS: ClassVar[float] = 30.0
    ATTEMPTS: ClassVar[int] = 6
    FIRST_PAUSE: ClassVar[float] = 0.5
    LONGEST_PAUSE: ClassVar[float] = 8.0
    TEMPORARY_CODES: ClassVar[frozenset[str]] = frozenset({"retryable_contention"})
    GATEWAY: ClassVar[frozenset[int]] = frozenset({502, 503, 504})
    IDEMPOTENT: ClassVar[frozenset[str]] = frozenset({"GET", "HEAD", "PUT", "DELETE", "OPTIONS"})

    def __init__(self, method: str, content: bytes | Iterator[bytes] | None, idempotency_key: str | None) -> None:
        """Start the clock for one request."""
        self._replayable = content is None or isinstance(content, bytes)
        self._repeatable = method.upper() in self.IDEMPOTENT or idempotency_key is not None
        self._deadline = time.monotonic() + self.SECONDS
        self._pause = self.FIRST_PAUSE
        self._retries = 0

    def refused(self, status: int, body: bytes, retry_after: str | None) -> bool:
        """Whether a refusal may be followed by the same request; waits first when it may."""
        if not self._replayable:
            return False
        temporary = status == 429 or (status == 503 and self.problem_code(body) in self.TEMPORARY_CODES)
        if not temporary and not (status in self.GATEWAY and self._repeatable):
            return False
        return self._wait(self.hinted(retry_after))

    def lost(self) -> bool:
        """Whether a request whose answer never came may be sent again; waits first when it may."""
        return self._replayable and self._repeatable and self._wait(None)

    def _wait(self, hint: float | None) -> bool:
        """Sleep before the next attempt unless that would pass the deadline."""
        pause = min(hint if hint is not None else self._pause, self.LONGEST_PAUSE)
        if self._retries + 1 >= self.ATTEMPTS or time.monotonic() + pause >= self._deadline:
            return False
        time.sleep(pause)
        self._retries += 1
        self._pause = min(self._pause * 2, self.LONGEST_PAUSE)
        return True

    @staticmethod
    def hinted(retry_after: str | None) -> float | None:
        """Seconds named by a numeric ``Retry-After``; dates and junk give no hint."""
        try:
            return max(float(retry_after), 0.0) if retry_after is not None else None
        except ValueError:
            return None

    @staticmethod
    def problem_code(body: bytes) -> str | None:
        """The ``code`` of a Problem Details body, if the body is one."""
        try:
            document = json.loads(body or b"{}")
        except ValueError:
            return None
        code = document.get("code") if isinstance(document, dict) else None
        return code if isinstance(code, str) else None
