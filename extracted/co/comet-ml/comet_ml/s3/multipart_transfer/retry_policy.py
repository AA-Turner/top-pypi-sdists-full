# -*- coding: utf-8 -*-
# *******************************************************
#   ____                     _               _
#  / ___|___  _ __ ___   ___| |_   _ __ ___ | |
# | |   / _ \| '_ ` _ \ / _ \ __| | '_ ` _ \| |
# | |__| (_) | | | | | |  __/ |_ _| | | | | | |
#  \____\___/|_| |_| |_|\___|\__(_)_| |_| |_|_|
#
#  Sign up for free at https://www.comet.com
#  Copyright (C) 2015-2026 Comet ML INC
#  This source code is licensed under the MIT license.
# *******************************************************
"""The retry policy every S3 part transfer follows, whichever way its bytes go.

Which statuses mean "retry", how long a rate limit may be waited out, how backoff
is spread, and how a server's Retry-After is read. The loops that apply it live
with their transfers - uploads in multipart_upload.retry_strategy, ranged GETs in
multipart_download.range_requests - because what a retry must redo differs.
"""
import datetime
import email.utils
import logging
import math
import random
from typing import Optional

from requests import Response

from ...connection.connection_helpers import calculate_backoff_time

LOGGER = logging.getLogger(__name__)

# Something broke at the far end, or at a gateway in front of it. Retryable, but with
# no promise that retrying will help, so these keep the modest attempt count.
SERVER_ERROR_STATUS_CODES = [500, 502, 504]

# The statuses that mean "you are going too fast" rather than "something broke". The
# distinction matters for how hard we try: a throttled request is one the server has
# promised to accept later, so giving up on it early is throwing away an upload that
# was going to succeed. 429 is here for completeness; S3 itself uses 503 SlowDown.
THROTTLING_STATUS_CODES = [429, 503]

# Throttling gets its own budget, and it is a budget of *time*, not of attempts. Four
# attempts is right for an error that is probably not going to clear; it is the wrong
# shape entirely for a rate limit, where the whole point is to wait the endpoint out.
#
# Time has to be the binding constraint because attempts are consumed at a rate we do
# not control: while some parts are getting through, the shared brake keeps releasing,
# so a heavily throttled part can burn attempts quickly without much time passing. A
# 64 MiB asset against an endpoint rejecting 94% of requests exhausted a 24-attempt
# budget in 55 seconds of a 600 second allowance, and failed while nearly the whole
# allowance was unspent.
MAX_THROTTLE_RETRY_SECONDS = 600.0

# A loose backstop against a pathological endpoint that rejects instantly and forever,
# where the time budget alone would mean a very large number of requests. Deliberately
# high enough that the time budget is what normally decides.
MAX_THROTTLE_ATTEMPTS = 100

# Parts of one asset are sent to or fetched from S3 together, so they also get throttled together,
# and an unjittered backoff would march them all back in step - a thundering herd
# aimed at an endpoint that just asked for less traffic. Each sleep is spread over
# the interval it would otherwise be, up to half again as long, which decorrelates
# the attempts without ever retrying sooner than the configured backoff: when the
# server has asked for a slower request rate, erring short is the wrong direction.
# Only the part path needs this; the single-request operations around it have
# nothing to collide with.
PART_RETRY_JITTER = 0.5


def backoff_with_jitter(backoff_factor: float, attempt: int, jitter: float) -> float:
    backoff_time = calculate_backoff_time(
        backoff_factor=backoff_factor, retry_attempt=attempt
    )
    if jitter > 0:
        backoff_time *= 1.0 + jitter * random.random()

    return backoff_time


def retry_after_seconds(response: Optional[Response]) -> Optional[float]:
    """The server's own instruction on how long to wait, when it sent one.

    A server that says how long to back off knows better than any doubling
    heuristic, so this wins wherever it is present. Both forms the header permits
    are accepted, and anything unparseable is ignored rather than trusted.
    """
    if response is None:
        return None

    raw = response.headers.get("Retry-After")
    if raw is None:
        return None

    try:
        return finite_seconds(float(raw))
    except (TypeError, ValueError):
        pass

    try:
        retry_at = email.utils.parsedate_to_datetime(raw)
    except (TypeError, ValueError):
        LOGGER.debug("Could not parse Retry-After header %r", raw)
        return None

    now = datetime.datetime.now(tz=retry_at.tzinfo)

    return finite_seconds((retry_at - now).total_seconds())


def finite_seconds(value: float) -> Optional[float]:
    """A delay we are willing to act on, or None.

    "Retry-After: inf" parses as a float perfectly well, and on the path with no
    shared gate to bound it that reached time.sleep() directly - a worker thread
    parked forever on a header. Anything not finite is treated as absent rather than
    trusted; the caller then falls back to its own backoff.
    """
    if not math.isfinite(value):
        LOGGER.debug("Ignoring a non-finite Retry-After value: %r", value)
        return None

    return max(0.0, value)
