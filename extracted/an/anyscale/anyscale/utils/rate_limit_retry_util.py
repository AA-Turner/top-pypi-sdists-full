"""Client-side handling for control-plane rate-limit (HTTP 429) responses.

The control plane answers an over-limit request with ``429`` plus a
``Retry-After`` header (``backend/server/common/rate_limiting/``). urllib3's
default policy already honors that header, so this module does not add the
retrying -- it makes it bounded, visible and escapable:

- Each wait is capped at ``MAX_RETRY_AFTER_SECONDS``.
- Each wait is announced on stderr, for every status this policy waits on
  (413/429/503), so a pause never looks like a hang.
- ``ANYSCALE_DISABLE_RATE_LIMIT_RETRIES=1`` refuses 429 waits outright.

Retries stay tied to ``Retry-After``: a 429 without that header is surfaced
rather than retried, since our limiter always sends it and a header-less 429
comes from something else whose backoff semantics we should not guess at. Only
idempotent methods are retried, so a rate-limited job submit is never
resubmitted here. Exhausting the budget raises ``ApiException(429)``, matching
the released client.
"""

import os
from typing import Any, Optional

from urllib3.exceptions import InvalidHeader
from urllib3.util.retry import Retry

from anyscale.cli_logger import BlockLogger


# Compared against "1" like image_sdk.py:22 and anyscale_client.py:192, rather
# than tested for truthiness, which would make `...=0` disable retries.
DISABLE_ENV_VAR = "ANYSCALE_DISABLE_RATE_LIMIT_RETRIES"

RATE_LIMIT_STATUS = 429

# urllib3's historical default budget, which is what the released client used.
TOTAL_RETRIES = 3

# Cap on a single wait. Sized at 2 * window_seconds, the ceiling of
# compute_retry_after(); every policy currently uses window_seconds=60. Raise it
# alongside any longer window, or we retry before the server's window closes.
MAX_RETRY_AFTER_SECONDS = 120.0

# The opt-out hint is guidance, not per-event data, so it rides along with the
# first announcement only. A dict rather than a bool so updating it is a
# mutation, not a rebinding needing `global` (ruff PLW0603).
_hint_state = {"shown": False}


def _reset_hint_for_testing() -> None:
    """Clear the once-per-process hint latch. For tests only."""
    _hint_state["shown"] = False


class RateLimitRetry(Retry):
    """urllib3 ``Retry`` that caps Retry-After waits and announces them."""

    def __init__(self, *args: Any, logger: Optional[BlockLogger] = None, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self._logger = logger or BlockLogger()

    def new(self, **kw: Any) -> "RateLimitRetry":
        # urllib3 rebuilds from a fixed parameter list, dropping the logger.
        kw.setdefault("logger", self._logger)
        return super().new(**kw)  # type: ignore[return-value]

    def get_retry_after(self, response) -> Optional[float]:
        try:
            retry_after = super().get_retry_after(response)
        except InvalidHeader:
            # urllib3 accepts only a bare integer or HTTP-date. urlopen does not
            # wrap retries.sleep(), so a proxy sending "1.5" would escape as a
            # traceback.
            return None
        if retry_after is None:
            return None
        return min(retry_after, MAX_RETRY_AFTER_SECONDS)

    def _announce(self, status: int, wait: float) -> None:
        if status != RATE_LIMIT_STATUS:
            # The opt-out refuses 429 only, so the hint would be false advice
            # here, and consuming the latch would rob a later real rate limit.
            message = f"Anyscale API returned {status}; retrying in {wait:.0f}s."
        else:
            message = f"Rate limited by the Anyscale API; retrying in {wait:.0f}s."
            if not _hint_state["shown"]:
                message += f" Set {DISABLE_ENV_VAR}=1 to fail fast instead."
                _hint_state["shown"] = True
        self._logger.warning(message)

    def sleep(self, response=None) -> None:
        status = getattr(response, "status", None) if response is not None else None
        # 413 and 503 are retried by this policy too, and a silent 503 wait
        # during a deploy is indistinguishable from a hang. The header gate
        # mirrors Retry.sleep, which only honors it when respect_* is set.
        if status in self.RETRY_AFTER_STATUS_CODES and self.respect_retry_after_header:
            wait = self.get_retry_after(response)
            if wait:
                self._announce(status, wait)
        super().sleep(response)


class RateLimitOptOutRetry(Retry):
    """Opt-out policy: never waits on a 429, otherwise urllib3's default.

    ``respect_retry_after_header=False`` would be shorter but disables
    ``Retry-After`` for every code in ``RETRY_AFTER_STATUS_CODES``, so opting out
    of rate-limit waits would also drop 413/503 resilience.
    """

    def is_retry(self, method, status_code, has_retry_after: bool = False) -> bool:
        if status_code == RATE_LIMIT_STATUS:
            return False
        # urllib3's is_retry can return 0 rather than False: its final
        # expression short-circuits on self.total, an int.
        return bool(super().is_retry(method, status_code, has_retry_after))


def build_rate_limit_retry(logger: Optional[BlockLogger] = None) -> Retry:
    """Retry policy honoring 429 + Retry-After.

    Args:
        logger: Optional ``BlockLogger``. Announcements route through it, so a
            caller passing ``log_output=False`` stays silent.

    Returning ``None`` instead of a policy would disable nothing: it leaves the
    pool on urllib3's default, which honors Retry-After on 429s by itself.
    """
    if os.environ.get(DISABLE_ENV_VAR, "0") == "1":
        return RateLimitOptOutRetry(TOTAL_RETRIES)
    return RateLimitRetry(TOTAL_RETRIES, respect_retry_after_header=True, logger=logger)
