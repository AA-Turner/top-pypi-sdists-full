"""Shared HTTP client for the Slack Web API.

Single place that owns the base URL, the ``Bearer`` auth header, the request
timeout, the ``ok`` / ``error`` parsing (enriched via
:func:`pysae_ai_tools.slack.common.describe_slack_error`) and the uniform
handling of ``ratelimited`` (honour ``Retry-After`` and retry). Every
``slack`` subcommand goes through :func:`slack_get`, :func:`slack_post` or
:func:`slack_paginate` instead of re-implementing the urllib boilerplate, so a
cross-cutting change (retry, timeout, auth) happens here once.

All three helpers raise :class:`SlackApiError` on any failure — a Slack-level
``ok: false`` (``.code`` carries the raw Slack error code) or a transport error
(``.code`` empty). Callers catch the one exception and render ``str(err)``,
which is already the human-enriched message.
"""

import json
import time
import urllib.error
import urllib.parse
import urllib.request
from collections.abc import Iterator

from .common import describe_slack_error

SLACK_API_BASE = "https://slack.com/api"

DEFAULT_TIMEOUT = 10

# Slack answers a throttled call with HTTP 429 + a ``Retry-After`` header (and,
# rarely, a 200 body with ``error: ratelimited``). We wait the advertised delay
# and retry, transparently for callers, up to this many times.
MAX_RATELIMIT_RETRIES = 3
_DEFAULT_RETRY_AFTER = 1


class SlackApiError(RuntimeError):
    """A Slack Web API call failed.

    ``code`` is the raw Slack error code for an ``ok: false`` response (e.g.
    ``not_in_channel``), empty for a transport-level failure. The exception
    message is the human-enriched form, so callers can surface ``str(err)``
    directly and branch on ``err.code`` when they need the machine code.
    """

    def __init__(self, message: str, *, code: str = "") -> None:
        self.code = code
        super().__init__(message)


def _retry_after_seconds(headers: object) -> int:
    value = headers.get("Retry-After") if hasattr(headers, "get") else None
    try:
        return max(int(str(value)), _DEFAULT_RETRY_AFTER)
    except (TypeError, ValueError):
        return _DEFAULT_RETRY_AFTER


def _request(req: urllib.request.Request, timeout: int) -> dict[str, object]:
    """Send ``req``, parse the JSON body, retrying on rate-limit; raise on failure."""
    for attempt in range(MAX_RATELIMIT_RETRIES + 1):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                raw = resp.read()
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < MAX_RATELIMIT_RETRIES:
                time.sleep(_retry_after_seconds(e.headers))
                continue
            raise SlackApiError(f"HTTP {e.code} from Slack: {e.reason}") from None
        except urllib.error.URLError as e:
            raise SlackApiError(f"network error reaching Slack: {e.reason}") from None

        try:
            parsed: dict[str, object] = json.loads(raw)
        except json.JSONDecodeError as e:
            raise SlackApiError(f"invalid JSON from Slack: {e}") from None

        if parsed.get("ok"):
            return parsed
        code = str(parsed.get("error", "unknown"))
        if code == "ratelimited" and attempt < MAX_RATELIMIT_RETRIES:
            time.sleep(_DEFAULT_RETRY_AFTER)
            continue
        raise SlackApiError(describe_slack_error(code), code=code)
    raise SlackApiError(describe_slack_error("ratelimited"), code="ratelimited")


def slack_get(token: str, method: str, params: dict[str, str], *, timeout: int = DEFAULT_TIMEOUT) -> dict[str, object]:
    """GET a Slack Web API ``method`` with ``params``; return the parsed ``ok`` body."""
    qs = urllib.parse.urlencode(params)
    req = urllib.request.Request(
        f"{SLACK_API_BASE}/{method}?{qs}",
        headers={"Authorization": f"Bearer {token}"},
        method="GET",
    )
    return _request(req, timeout)


def slack_post(
    token: str, method: str, payload: dict[str, object], *, timeout: int = DEFAULT_TIMEOUT
) -> dict[str, object]:
    """POST ``payload`` as JSON to a Slack Web API ``method``; return the parsed ``ok`` body."""
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        f"{SLACK_API_BASE}/{method}",
        data=data,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json; charset=utf-8",
        },
        method="POST",
    )
    return _request(req, timeout)


def slack_paginate(
    token: str,
    method: str,
    params: dict[str, str],
    *,
    items_key: str,
    timeout: int = DEFAULT_TIMEOUT,
) -> Iterator[dict[str, object]]:
    """Yield each ``dict`` item of ``items_key`` across every cursor page of ``method``.

    Follows ``response_metadata.next_cursor`` until it is empty. ``params`` is the
    per-call query (channel, oldest, limit, …); the cursor is injected on each page.
    Lazy: a caller that returns early stops the paging.
    """
    cursor: str | None = None
    while True:
        page = dict(params)
        if cursor:
            page["cursor"] = cursor
        data = slack_get(token, method, page, timeout=timeout)
        items = data.get(items_key)
        if isinstance(items, list):
            for item in items:
                if isinstance(item, dict):
                    yield item
        meta = data.get("response_metadata")
        cursor = meta.get("next_cursor") if isinstance(meta, dict) else None
        if not cursor:
            break
