"""Retry timing and confirmed rate-limit policy shared by dispatcher lookups."""

from __future__ import annotations

import json
import os
import re
import sys
import time
from collections.abc import Callable, Mapping
from datetime import datetime
from email.utils import parsedate_to_datetime
from math import isfinite

from agentic_devtools.cli.shared.retry import ProviderRateLimitError, calculate_rate_limit_delay

MAX_RETRY_WINDOW_SECONDS = 21_000
_RATE_LIMIT_EVIDENCE = re.compile(r"API rate limit exceeded|secondary rate limit|rate limit", re.IGNORECASE)


def _retry_after_seconds(value: str | None, current: float) -> float | None:
    """Parse numeric or HTTP-date Retry-After timing."""
    if not value:
        return None
    if value.isascii() and value.isdigit():
        try:
            return float(int(value))
        except OverflowError:
            return MAX_RETRY_WINDOW_SECONDS + 1
    try:
        retry_epoch = parsedate_to_datetime(value).timestamp()
    except TypeError, ValueError, OverflowError:
        return None
    return max(0.0, retry_epoch - current)


def _primary_reset(headers: Mapping[str, str]) -> float | None:
    """Use the primary reset only when remaining quota explicitly equals zero."""
    remaining = headers.get("x-ratelimit-remaining")
    try:
        exhausted = remaining is not None and int(remaining) == 0
    except ValueError:
        return None
    if not exhausted:
        return None
    reset = headers.get("x-ratelimit-reset")
    if reset is None:
        return None
    try:
        return float(reset)
    except ValueError:
        return None


def calculate_dispatch_retry_delay(headers: Mapping[str, str], *, now: float | None = None) -> float:
    """Select a provider delay without using a primary reset for secondary limits."""
    current = time.time() if now is None else now
    normalized = {
        key.lower(): value.strip() for key, value in headers.items() if isinstance(key, str) and isinstance(value, str)
    }
    delay = calculate_rate_limit_delay(
        retry_after_seconds=_retry_after_seconds(normalized.get("retry-after"), current),
        reset_timestamp=_primary_reset(normalized),
        now=current,
        fallback_delay=60,
        safety_margin=0,
        max_delay=sys.float_info.max,
    )
    if delay.source == "x-ratelimit-reset":
        return delay.delay_seconds + 1
    return delay.delay_seconds


def _notify_rate_limit(
    error: ProviderRateLimitError, callback: Callable[[ProviderRateLimitError], None] | None
) -> None:
    """Notify the durable producer only when the failure confirms a rate limit."""
    if error.is_rate_limit and callback is not None:
        callback(error)


def _validate_retry_settings(max_attempts: int, retry_window_seconds: float) -> None:
    """Reject retry bounds that could create unbounded or invalid lookup behavior."""
    if isinstance(max_attempts, bool) or not isinstance(max_attempts, int) or max_attempts <= 0:
        raise ValueError("max_attempts must be a positive integer")
    if (
        isinstance(retry_window_seconds, bool)
        or not isinstance(retry_window_seconds, (int, float))
        or retry_window_seconds < 0
        or retry_window_seconds > sys.float_info.max
        or not isfinite(retry_window_seconds)
    ):
        raise ValueError("retry_window_seconds must be finite and non-negative")


def _rate_limit_error(headers: dict[str, str], delay: float) -> ProviderRateLimitError:
    """Preserve provider timing in a typed error, refusing invalid supplied deadlines."""
    from agentic_devtools.cli.ci.github_provider import _parse_rate_limit_headers

    retry_after, reset, remaining = _parse_rate_limit_headers(headers)
    raw_retry_after = headers.get("retry-after")
    if raw_retry_after and retry_after is None:
        try:
            parsedate_to_datetime(raw_retry_after).timestamp()
        except (TypeError, ValueError, OverflowError) as exc:
            raise ValueError("Invalid provider rate-limit timing") from exc
    if headers.get("x-ratelimit-reset") and reset is None:
        raise ValueError("Invalid provider rate-limit timing")
    return ProviderRateLimitError(
        retry_after_seconds=delay,
        reset_timestamp=reset,
        remaining=remaining,
        provider="github",
        credential_identity=os.environ.get("AI_PR_LOOP_CREDENTIAL_IDENTITY", "DEFAULT_CLASSIC_REPO_WORKFLOW_PAT"),
        source="dispatcher-throttle",
    )


def _is_rate_limit(status: int | None, headers: Mapping[str, str], diagnostics: str) -> bool:
    """Distinguish confirmed limits from permission-denied 403 responses."""
    remaining = headers.get("x-ratelimit-remaining")
    try:
        exhausted = remaining is not None and int(remaining) == 0
    except ValueError:
        exhausted = False
    return status == 429 or (
        status == 403
        and (bool(_RATE_LIMIT_EVIDENCE.search(diagnostics)) or exhausted or bool(headers.get("retry-after")))
    )


def _parse_workflow_run(body: bytes) -> dict[str, object]:
    """Validate a complete lookup response before exposing a throttle decision."""
    try:
        response = json.loads(body)
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise RuntimeError(
            "Throttle lookup succeeded without a JSON response; "
            "throttle state is unknown and the scheduler wake-up was not handled."
        ) from exc
    if not isinstance(response, dict):
        raise RuntimeError(
            "Throttle lookup returned an invalid JSON response; "
            "throttle state is unknown and the scheduler wake-up was not handled."
        )
    if "workflow_runs" not in response:
        raise RuntimeError(
            "Throttle lookup response is missing workflow_runs; "
            "throttle state is unknown and the scheduler wake-up was not handled."
        )
    workflow_runs = response["workflow_runs"]
    if not isinstance(workflow_runs, list):
        raise RuntimeError(
            "Throttle lookup returned an invalid workflow_runs response; "
            "throttle state is unknown and the scheduler wake-up was not handled."
        )
    if not workflow_runs:
        return {}
    last_run = workflow_runs[0]
    if not isinstance(last_run, dict):
        raise RuntimeError(
            "Throttle lookup returned an invalid workflow run; "
            "throttle state is unknown and the scheduler wake-up was not handled."
        )
    updated_at = last_run.get("updated_at")
    if not isinstance(updated_at, str) or not updated_at.strip():
        raise RuntimeError(
            "Throttle lookup returned an invalid updated_at value; "
            "throttle state is unknown and the scheduler wake-up was not handled."
        )
    try:
        datetime.fromisoformat(updated_at.replace("Z", "+00:00"))
    except ValueError as exc:
        raise RuntimeError(
            "Throttle lookup returned an invalid updated_at timestamp; "
            "throttle state is unknown and the scheduler wake-up was not handled."
        ) from exc
    return last_run
