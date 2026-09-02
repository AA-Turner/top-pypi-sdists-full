"""
Async HTTP fetch helpers for the Census API.

Provides:
- ``fetch_json``: GET with retry-on-status loop (429 / 502 / 503 / 504),
  honouring ``Retry-After``, with exponential backoff fallback.
- ``fan_out``: Parallel per-state requests under an ``asyncio.Semaphore``
  with fail-fast semantics.
- ``STATE_CODES``: Tuple of 52 FIPS codes (50 states + DC + PR).

The retry loop shape is copied from
``flowtask/components/OpenStreetMap.py:188-236``.
"""

from __future__ import annotations

import asyncio
import logging
import random
from typing import Any, Callable

import aiohttp

from flowtask.components._census.resolver import scrub_url
from flowtask.exceptions import ComponentError

# ---------------------------------------------------------------------------
# FIPS codes — 50 states + DC + PR (52 total)
# Source: Census Bureau FIPS Publication 6-4
# ---------------------------------------------------------------------------

STATE_CODES: tuple[str, ...] = (
    "01",  # Alabama
    "02",  # Alaska
    "04",  # Arizona
    "05",  # Arkansas
    "06",  # California
    "08",  # Colorado
    "09",  # Connecticut
    "10",  # Delaware
    "11",  # District of Columbia
    "12",  # Florida
    "13",  # Georgia
    "15",  # Hawaii
    "16",  # Idaho
    "17",  # Illinois
    "18",  # Indiana
    "19",  # Iowa
    "20",  # Kansas
    "21",  # Kentucky
    "22",  # Louisiana
    "23",  # Maine
    "24",  # Maryland
    "25",  # Massachusetts
    "26",  # Michigan
    "27",  # Minnesota
    "28",  # Mississippi
    "29",  # Missouri
    "30",  # Montana
    "31",  # Nebraska
    "32",  # Nevada
    "33",  # New Hampshire
    "34",  # New Jersey
    "35",  # New Mexico
    "36",  # New York
    "37",  # North Carolina
    "38",  # North Dakota
    "39",  # Ohio
    "40",  # Oklahoma
    "41",  # Oregon
    "42",  # Pennsylvania
    "44",  # Rhode Island
    "45",  # South Carolina
    "46",  # South Dakota
    "47",  # Tennessee
    "48",  # Texas
    "49",  # Utah
    "50",  # Vermont
    "51",  # Virginia
    "53",  # Washington
    "54",  # West Virginia
    "55",  # Wisconsin
    "56",  # Wyoming
    "72",  # Puerto Rico
)

# Sanity check — fail at import time if the list is wrong.
if len(STATE_CODES) != 52:
    raise ValueError(f"STATE_CODES must have 52 entries, got {len(STATE_CODES)}")

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

_RETRIABLE_STATUSES: frozenset[int] = frozenset({429, 502, 503, 504})
_IMMEDIATE_ERROR_STATUSES: frozenset[int] = frozenset({400, 404})
_MAX_RETRY_AFTER_SECS: float = 60.0


# ---------------------------------------------------------------------------
# fetch_json
# ---------------------------------------------------------------------------


async def fetch_json(
    session: aiohttp.ClientSession,
    url: str,
    logger: logging.Logger,
    *,
    max_retries: int = 5,
    base_backoff: float = 1.0,
) -> list[Any] | dict[str, Any]:
    """GET a URL and return the parsed JSON payload with retry-on-status logic.

    Retry policy (mirrors ``OpenStreetMap._post_overpass``):
    - 200: parse JSON and return.
    - 429: honour ``Retry-After`` header; else exponential back-off.
    - 502 / 503 / 504: exponential back-off (no ``Retry-After`` lookup).
    - 400 / 404: read body and raise ``ComponentError`` immediately.
    - Other 4xx: raise ``ComponentError`` immediately.
    - Network errors (``aiohttp.ClientError``, ``asyncio.TimeoutError``):
      treated as retriable; raise ``ComponentError`` on exhaustion.
    - All attempts exhausted: raise ``ComponentError`` naming the last status.

    The session is caller-owned — this function does NOT create or close it.
    Every URL surfaced in error messages passes through ``scrub_url()`` to
    avoid leaking the API key.

    Args:
        session: A caller-owned ``aiohttp.ClientSession``.
        url: The URL to GET.
        logger: A logger for warning / error messages.
        max_retries: Maximum number of retry attempts (default 5).
        base_backoff: Base seconds for exponential back-off (default 1.0).

    Returns:
        The parsed JSON as a ``list`` or ``dict``.

    Raises:
        ComponentError: On non-retriable errors or after all retries are
            exhausted.
    """
    safe_url = scrub_url(url)
    attempt = 0
    last_status: int | None = None

    while True:
        retry_after: str | None = None
        try:
            async with session.get(url) as response:
                last_status = response.status
                if last_status == 200:
                    return await response.json(content_type=None)

                if last_status in _IMMEDIATE_ERROR_STATUSES:
                    body = await response.text()
                    raise ComponentError(
                        f"Census API returned {last_status} for {safe_url!r}: "
                        f"{body[:300]}",
                        status=last_status,
                    )

                if last_status in _RETRIABLE_STATUSES:
                    retry_after = response.headers.get("Retry-After")
                    logger.warning(
                        "Census API %d (attempt %d / %d): %s",
                        last_status,
                        attempt + 1,
                        max_retries,
                        safe_url,
                    )
                else:
                    # Non-retriable 4xx or 5xx we don't know about.
                    body = await response.text()
                    raise ComponentError(
                        f"Census API returned unexpected status {last_status} "
                        f"for {safe_url!r}: {body[:300]}",
                        status=last_status,
                    )

        except ComponentError:
            raise
        except (aiohttp.ClientError, asyncio.TimeoutError) as exc:
            logger.warning(
                "Census API network error (attempt %d / %d): %s — %s",
                attempt + 1,
                max_retries,
                safe_url,
                exc,
            )

        attempt += 1
        if attempt >= max_retries:
            raise ComponentError(
                f"Census API request to {safe_url!r} failed after "
                f"{max_retries} attempts (last status: {last_status}).",
                status=last_status or 503,
            )

        # Compute back-off delay.
        delay = base_backoff * (2 ** attempt)
        if retry_after is not None:
            try:
                delay = max(delay, min(float(retry_after), _MAX_RETRY_AFTER_SECS))
            except (TypeError, ValueError):
                pass
        delay += random.uniform(0, 1.0)  # jitter to avoid retry herds
        logger.warning(
            "Retrying in %.1f s (attempt %d / %d): %s",
            delay,
            attempt,
            max_retries,
            safe_url,
        )
        await asyncio.sleep(delay)


# ---------------------------------------------------------------------------
# fan_out
# ---------------------------------------------------------------------------


async def fan_out(
    session: aiohttp.ClientSession,
    url_for_state: Callable[[str], str],
    states: list[str],
    semaphore: asyncio.Semaphore,
    logger: logging.Logger,
) -> list[list[Any] | dict[str, Any]]:
    """Issue parallel per-state requests under a semaphore with fail-fast.

    Each state call acquires the semaphore before calling ``fetch_json``, so
    at most ``semaphore._value`` requests are in-flight concurrently.

    Uses ``asyncio.gather(..., return_exceptions=False)`` — the first failing
    state cancels the rest and re-raises the ``ComponentError`` with the state
    code included in the message.

    Args:
        session: A caller-owned ``aiohttp.ClientSession``.
        url_for_state: Callable that maps a FIPS code to the Census API URL
            for that state.
        states: List of FIPS codes to fetch (e.g. ``STATE_CODES``).
        semaphore: An ``asyncio.Semaphore`` limiting concurrency.
        logger: A logger for error messages.

    Returns:
        A list of per-state raw JSON payloads (in the same order as ``states``).
        Each payload is a ``list`` (Census API format: first row = headers).

    Raises:
        ComponentError: If any state request fails after retries.  The failing
            state code is included in the message.
    """

    async def _fetch_one_state(state: str) -> list[Any] | dict[str, Any]:
        async with semaphore:
            try:
                return await fetch_json(session, url_for_state(state), logger)
            except ComponentError as exc:
                logger.error(
                    "Census fan-out: state %s failed — %s", state, exc
                )
                raise ComponentError(
                    f"Census fan-out: state {state!r} failed — {exc}",
                    status=exc.status if hasattr(exc, "status") else 503,
                ) from exc

    tasks = [_fetch_one_state(state) for state in states]
    # return_exceptions=False is the default; first failure propagates.
    results = await asyncio.gather(*tasks, return_exceptions=False)
    return list(results)
