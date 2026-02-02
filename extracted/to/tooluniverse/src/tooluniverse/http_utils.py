"""
Shared HTTP utilities for ToolUniverse tools.

Goal: provide a small, dependency-light helper for retrying transient HTTP failures
without changing individual tool return formats.
"""

from __future__ import annotations

from typing import Any, Mapping, Optional, Sequence, Tuple, Union
import time

import requests


RetryStatuses = Sequence[int]


def request_with_retry(
    session: Union[requests.Session, Any],
    method: str,
    url: str,
    *,
    params: Optional[Mapping[str, Any]] = None,
    headers: Optional[Mapping[str, str]] = None,
    json: Any = None,
    data: Any = None,
    timeout: Optional[float] = None,
    retry_statuses: RetryStatuses = (502, 503, 504),
    max_attempts: int = 3,
    backoff_seconds: float = 0.5,
) -> requests.Response:
    """
    Make an HTTP request with small exponential backoff on transient failures.

    Retries:
    - timeouts / connection errors
    - HTTP status codes in retry_statuses

    Notes:
    - Does NOT call raise_for_status(); callers can decide how to handle non-2xx.
    - Keeps behavior conservative (defaults: 3 attempts, 0.5s backoff).
    """
    m = (method or "GET").upper()
    attempts = max(1, int(max_attempts))
    last_exc: Optional[BaseException] = None

    for attempt in range(attempts):
        try:
            resp = session.request(
                m,
                url,
                params=params,
                headers=headers,
                json=json,
                data=data,
                timeout=timeout,
            )

            if resp.status_code in set(retry_statuses) and attempt < attempts - 1:
                sleep_s = backoff_seconds * (2**attempt)
                time.sleep(sleep_s)
                continue

            return resp

        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
            last_exc = e
            if attempt < attempts - 1:
                sleep_s = backoff_seconds * (2**attempt)
                time.sleep(sleep_s)
                continue
            raise

        except requests.exceptions.RequestException as e:
            # Retry only when it looks like a transient network failure
            last_exc = e
            if attempt < attempts - 1:
                sleep_s = backoff_seconds * (2**attempt)
                time.sleep(sleep_s)
                continue
            raise

    # Should be unreachable, but keep a clear failure mode.
    if last_exc:
        raise last_exc
    raise RuntimeError("request_with_retry failed unexpectedly without an exception")
