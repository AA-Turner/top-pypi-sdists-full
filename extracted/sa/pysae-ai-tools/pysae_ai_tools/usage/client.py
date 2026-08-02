"""Read the Claude subscription usage (5-hour session + weekly windows).

Queries the OAuth usage endpoint with the Claude Code OAuth token stored in
``~/.claude/.credentials.json`` and caches the result on disk so the PreToolUse
hook never hits the network more than once per ``cache_ttl`` seconds, however
many tool calls fire in between.

The endpoint rate-limits aggressively. To avoid feeding the limit, a disk lock
shared across every invocation throttles live fetches (``MIN_FETCH_INTERVAL``)
and, on a 429, backs off until the server's ``Retry-After`` elapses. While a
backoff is active the last cached snapshot is served, flagged ``stale`` so
callers can surface that the data could not be refreshed.
"""

import json
import re
import subprocess
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path

import httpx

from . import account

CREDENTIALS_PATH = Path.home() / ".claude" / ".credentials.json"
CACHE_PATH = account.active_state_dir() / "usage-cache.json"
LOCK_PATH = account.active_state_dir() / "usage-lock.json"
USAGE_URL = "https://api.anthropic.com/api/oauth/usage"
OAUTH_BETA = "oauth-2025-04-20"
# The endpoint rate-limits per User-Agent bucket: a plain client lands in a more
# aggressively throttled pool, so we always present a real ``claude-code/<version>``.
# Used when ``claude --version`` is unavailable; keep in step with a recent release.
FALLBACK_CLAUDE_VERSION = "2.1.202"

# At most one live fetch per interval, across every session/hook invocation.
MIN_FETCH_INTERVAL = 30.0
# Fallback backoff when a 429 (or 5xx) carries no usable Retry-After header.
DEFAULT_RATE_LIMIT_BACKOFF = 300.0
# How long a statusline-sourced cache entry is trusted without falling back to the API.
# The statusline rewrites the cache on every render, so a fresh entry means a Claude Code
# session is live (and thus the only thing consuming the plan). Generous on purpose: outside
# a session the plan usage barely moves, and a long window keeps the (aggressively
# rate-limited) usage endpoint untouched during normal work. See ``get_usage``.
STATUSLINE_FRESH_TTL = 600.0

# Cache provenance: a live API fetch, or a Claude Code statusline render feeding us its
# ``rate_limits`` payload for free.
CACHE_SOURCE_API = "api"
CACHE_SOURCE_STATUSLINE = "statusline"

# Maps the canonical `limits[].kind` to the window it backs, for severity lookup.
_FIVE_HOUR_KINDS = {"session"}
_SEVEN_DAY_KINDS = {"weekly_all"}


@dataclass
class Window:
    """A single rate-limit window: the 5-hour session or the rolling week."""

    label: str
    percent: float
    resets_at: datetime | None
    severity: str


@dataclass
class ExtraUsage:
    """Billed extra usage that accrues once a plan window is exhausted. ``amount`` and
    ``limit`` are the monthly figures the API reports: spend so far this month and the
    monthly cap (``limit`` is None when the API omits it)."""

    amount: float
    currency: str
    enabled: bool
    limit: float | None = None


@dataclass
class UsageSnapshot:
    """Parsed usage for both plan windows, plus when it was fetched.

    ``from_cache`` is True whenever the data was served from the on-disk cache
    rather than a live fetch. When it is, three independent hold-off epochs say why a
    fetch was withheld (each None when not in effect): ``rate_limited_until`` is a
    server 429 backoff, ``unavailable_until`` is a server-side error/overload backoff
    (5xx, incl. 529 Overloaded) with the offending code in ``unavailable_status``,
    ``throttled_until`` is our own minimum interval between fetches. All three None on a
    cache serve means the API was simply unreachable.

    ``fetched_now`` is True whenever this call actually hit the network, regardless of the
    outcome: a live success (``from_cache`` False), but also a failed attempt that fell
    back to cache (a 429/5xx/transport error — then ``from_cache`` is True yet the request
    was still sent). It is False only when no request left the process (cache within TTL,
    an honoured hold-off, or a missing token).

    ``source`` records where the data came from: ``CACHE_SOURCE_API`` (a live/cached API
    fetch) or ``CACHE_SOURCE_STATUSLINE`` (fed by a Claude Code status line render).
    """

    five_hour: Window
    seven_day: Window
    extra: ExtraUsage
    fetched_at: float
    from_cache: bool = False
    rate_limited_until: float | None = None
    unavailable_until: float | None = None
    unavailable_status: int | None = None
    throttled_until: float | None = None
    fetched_now: bool = False
    source: str = CACHE_SOURCE_API

    @property
    def max_percent(self) -> float:
        return max(self.five_hour.percent, self.seven_day.percent)


def _read_token() -> str | None:
    """Return the Claude.ai OAuth access token, or None if unavailable/expired."""
    try:
        data = json.loads(CREDENTIALS_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    oauth = data.get("claudeAiOauth")
    if not isinstance(oauth, dict):
        return None
    token = oauth.get("accessToken")
    expires_at = oauth.get("expiresAt")
    if isinstance(expires_at, (int, float)) and expires_at / 1000 <= time.time():
        return None
    return token if isinstance(token, str) and token else None


@dataclass
class _FetchSuccess:
    raw: dict[str, object]


@dataclass
class _FetchRateLimited:
    retry_after: float


@dataclass
class _FetchError:
    """A failed fetch. ``status`` is the HTTP status when the server responded with a
    non-200/non-429 code (e.g. 529 Overloaded, 503), or None on a transport error/timeout
    where the API could not be reached at all."""

    status: int | None = None


_FetchResult = _FetchSuccess | _FetchRateLimited | _FetchError


def parse_retry_after(value: str | None, now: float) -> float | None:
    """Parse an HTTP ``Retry-After`` header to seconds-from-now.

    Accepts both forms allowed by RFC 9110: an integer delta in seconds, or an
    HTTP-date. Returns None when absent, unparseable, or already in the past.
    """
    if not value:
        return None
    trimmed = value.strip()
    if trimmed.isdigit():
        seconds = int(trimmed)
        return float(seconds) if seconds > 0 else None
    try:
        retry_at = parsedate_to_datetime(trimmed)
    except (TypeError, ValueError):
        return None
    if retry_at is None:
        return None
    if retry_at.tzinfo is None:
        retry_at = retry_at.replace(tzinfo=timezone.utc)
    delta = retry_at.timestamp() - now
    return delta if delta > 0 else None


_user_agent_cache: str | None = None


def _user_agent() -> str:
    """``claude-code/<version>`` from ``claude --version``, cached for the process.

    The usage endpoint rate-limits per User-Agent; a ``claude-code/*`` string
    lands in a less aggressive bucket. Falls back to ``FALLBACK_CLAUDE_VERSION``
    when the ``claude`` binary is absent or its output unparseable, so a real
    version is always presented."""
    global _user_agent_cache
    if _user_agent_cache is not None:
        return _user_agent_cache
    version = FALLBACK_CLAUDE_VERSION
    try:
        result = subprocess.run(
            ["claude", "--version"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=5.0,
        )
        match = re.search(r"\d+\.\d+\.\d+", result.stdout or "")
        if match:
            version = match.group(0)
    except (FileNotFoundError, subprocess.SubprocessError, OSError):
        pass
    _user_agent_cache = f"claude-code/{version}"
    return _user_agent_cache


def _fetch(token: str, now: float) -> _FetchResult:
    """Query the OAuth usage endpoint, distinguishing a 429 from other failures."""
    try:
        resp = httpx.get(
            USAGE_URL,
            headers={
                "Authorization": f"Bearer {token}",
                "anthropic-beta": OAUTH_BETA,
                "User-Agent": _user_agent(),
            },
            timeout=8.0,
        )
    except httpx.HTTPError:
        return _FetchError()
    if resp.status_code == 429:
        retry_after = parse_retry_after(resp.headers.get("retry-after"), now) or DEFAULT_RATE_LIMIT_BACKOFF
        return _FetchRateLimited(retry_after)
    if resp.status_code != 200:
        return _FetchError(status=resp.status_code)
    try:
        payload = resp.json()
    except (json.JSONDecodeError, ValueError):
        return _FetchError()
    return _FetchSuccess(payload) if isinstance(payload, dict) else _FetchError()


def _parse_resets_at(raw: object) -> datetime | None:
    if not isinstance(raw, str) or not raw:
        return None
    try:
        return datetime.fromisoformat(raw)
    except ValueError:
        return None


def _as_utc(dt: datetime) -> datetime:
    """Attach UTC to a naive datetime so two instants compare unambiguously."""
    return dt if dt.tzinfo is not None else dt.replace(tzinfo=timezone.utc)


def _window_regressed(incoming: datetime | None, known: datetime | None) -> bool:
    """True when ``incoming`` identifies an older window than the one already ``known``.

    A window's ``resets_at`` is its identity and moves strictly forward as windows roll
    over. Claude Code's status line occasionally replays an already-reset window (its old
    ``resets_at`` with a stale 100% utilization); such a payload regresses the id and must be
    ignored so it never overwrites the current window. Comparing two window ids (never the
    wall clock) makes this robust to clock drift and to the reset boundary itself.
    """
    return incoming is not None and known is not None and _as_utc(incoming) < _as_utc(known)


def _severity_for(raw: dict[str, object], kinds: set[str]) -> str:
    """Pull the severity of the matching limit from the canonical `limits` array."""
    limits = raw.get("limits")
    if not isinstance(limits, list):
        return "normal"
    for item in limits:
        if isinstance(item, dict) and item.get("kind") in kinds:
            sev = item.get("severity")
            if isinstance(sev, str) and sev:
                return sev
    return "normal"


def _window(raw: dict[str, object], key: str, label: str, kinds: set[str]) -> Window:
    block = raw.get(key)
    block = block if isinstance(block, dict) else {}
    percent = block.get("utilization")
    return Window(
        label=label,
        percent=float(percent) if isinstance(percent, (int, float)) else 0.0,
        resets_at=_parse_resets_at(block.get("resets_at")),
        severity=_severity_for(raw, kinds),
    )


def _money_minor(block: object) -> float | None:
    """Convert a ``{amount_minor, exponent}`` money block to a float, or None if malformed."""
    if isinstance(block, dict):
        minor = block.get("amount_minor")
        exponent = block.get("exponent", 0)
        if isinstance(minor, (int, float)) and isinstance(exponent, int):
            return float(minor) / (10.0**exponent)
    return None


def _parse_extra(raw: dict[str, object]) -> ExtraUsage:
    """Parse the billed extra-usage spend + monthly cap from `spend` (or `extra_usage`)."""
    spend = raw.get("spend")
    if isinstance(spend, dict):
        used = spend.get("used")
        amount = _money_minor(used)
        if amount is not None and isinstance(used, dict):
            return ExtraUsage(
                amount=amount,
                currency=str(used.get("currency", "")),
                enabled=bool(spend.get("enabled")),
                limit=_money_minor(spend.get("limit")),
            )
    extra = raw.get("extra_usage")
    if isinstance(extra, dict):
        credits = extra.get("used_credits")
        places = extra.get("decimal_places", 0)
        if isinstance(credits, (int, float)) and isinstance(places, int):
            monthly = extra.get("monthly_limit")
            limit = float(monthly) / (10**places) if isinstance(monthly, (int, float)) else None
            return ExtraUsage(
                amount=float(credits) / (10**places),
                currency=str(extra.get("currency", "")),
                enabled=bool(extra.get("is_enabled")),
                limit=limit,
            )
    return ExtraUsage(amount=0.0, currency="", enabled=False)


def _parse(
    raw: dict[str, object],
    fetched_at: float,
    from_cache: bool = False,
    rate_limited_until: float | None = None,
    unavailable_until: float | None = None,
    unavailable_status: int | None = None,
    throttled_until: float | None = None,
    fetched_now: bool = False,
    source: str = CACHE_SOURCE_API,
) -> UsageSnapshot:
    return UsageSnapshot(
        five_hour=_window(raw, "five_hour", "Fenêtre 5H", _FIVE_HOUR_KINDS),
        seven_day=_window(raw, "seven_day", "Semaine", _SEVEN_DAY_KINDS),
        extra=_parse_extra(raw),
        fetched_at=fetched_at,
        from_cache=from_cache,
        rate_limited_until=rate_limited_until,
        unavailable_until=unavailable_until,
        unavailable_status=unavailable_status,
        throttled_until=throttled_until,
        fetched_now=fetched_now,
        source=source,
    )


def _read_cache() -> tuple[dict[str, object], float, str] | None:
    """Return ``(raw, fetched_at, source)`` of the on-disk cache, or None when absent/corrupt.

    ``source`` is ``CACHE_SOURCE_API`` or ``CACHE_SOURCE_STATUSLINE``; a legacy entry with no
    ``source`` field is treated as API-sourced (its historical meaning)."""
    try:
        data = json.loads(CACHE_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    raw = data.get("raw")
    fetched_at = data.get("fetched_at")
    source = data.get("source")
    if isinstance(raw, dict) and isinstance(fetched_at, (int, float)):
        return raw, float(fetched_at), source if isinstance(source, str) else CACHE_SOURCE_API
    return None


def read_cached_usage(target: account.Account) -> UsageSnapshot | None:
    """Read-only snapshot of ``target``'s on-disk cache, for consulting a non-active account.

    No fetch, no lock, no write: a non-active account has no usable token, so ``show``/``history``
    can only replay whatever its last active session cached. None when that account has no cache."""
    try:
        data = json.loads((account.state_dir(target) / "usage-cache.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    raw = data.get("raw")
    fetched_at = data.get("fetched_at")
    source = data.get("source")
    if not isinstance(raw, dict) or not isinstance(fetched_at, (int, float)):
        return None
    return _parse(
        raw,
        float(fetched_at),
        from_cache=True,
        source=source if isinstance(source, str) else CACHE_SOURCE_API,
    )


def _write_cache(raw: dict[str, object], fetched_at: float, source: str = CACHE_SOURCE_API) -> None:
    CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    CACHE_PATH.write_text(
        json.dumps({"fetched_at": fetched_at, "source": source, "raw": raw}, ensure_ascii=False),
        encoding="utf-8",
    )


def _epoch_to_iso(epoch: float | None) -> str | None:
    """UTC ISO-8601 string for a Unix-*seconds* epoch, or None when absent or unusable.

    Guards the conversion: a NaN, an overflow, or a milliseconds value (which lands past
    year 9999) raises ``ValueError``/``OverflowError`` — we return None rather than let it
    crash the status line, whose whole point is to never fail."""
    if epoch is None:
        return None
    try:
        return datetime.fromtimestamp(epoch, timezone.utc).isoformat()
    except (ValueError, OverflowError, OSError):
        return None


def record_statusline_usage(
    five_hour_pct: float | None,
    five_hour_resets_at: float | None,
    seven_day_pct: float | None,
    seven_day_resets_at: float | None,
    now: float,
) -> None:
    """Persist the plan usage a Claude Code statusline render just handed us into the shared
    cache, so every other consumer (hook, ``show``, ``prime``) reads it instead of calling the
    rate-limited API. Percentages/reset epochs come from the statusline ``rate_limits`` payload.

    The statusline never carries the billed extra-usage ``spend`` block, so the last one seen
    from an API fetch is preserved — ``show`` keeps reporting the last known overage (with its
    age) rather than dropping it. Absent windows keep whatever the previous cache held."""
    prev = _read_cache()
    raw: dict[str, object] = dict(prev[0]) if prev is not None else {}

    def _window(key: str, pct: float | None, resets_epoch: float | None) -> None:
        if pct is None:
            return
        raw_prev = raw.get(key)
        prev_block = raw_prev if isinstance(raw_prev, dict) else None
        prev_resets = _parse_resets_at(prev_block.get("resets_at")) if prev_block else None
        prev_pct = prev_block.get("utilization") if prev_block else None
        block: dict[str, object] = {"utilization": float(pct)}
        iso = _epoch_to_iso(resets_epoch)
        if iso is not None:
            incoming_resets = _parse_resets_at(iso)
            # The status line sometimes replays an already-reset window (its old resets_at with a
            # stale 100%). A window id only moves forward, so an incoming id older than the one we
            # already hold is that replay: drop it and keep the current window untouched.
            if _window_regressed(incoming_resets, prev_resets):
                return
            # Same window (identical id): utilization only climbs until the reset, so a lower
            # incoming value is a stale render — typically an idle parallel Claude Code session
            # replaying an older rate_limits payload into the shared cache. Keep the higher known
            # value so the reading doesn't flap between sessions (e.g. 71% ⇄ 41%).
            if (
                incoming_resets is not None
                and prev_resets is not None
                and _as_utc(incoming_resets) == _as_utc(prev_resets)
                and isinstance(prev_pct, (int, float))
                and float(pct) < float(prev_pct)
            ):
                return
            block["resets_at"] = iso
        elif prev_block and "resets_at" in prev_block:
            # Unusable/absent reset epoch: keep a reset time already known (e.g. from a prior
            # API fetch) rather than silently dropping it.
            block["resets_at"] = prev_block["resets_at"]
        raw[key] = block

    _window("five_hour", five_hour_pct, five_hour_resets_at)
    _window("seven_day", seven_day_pct, seven_day_resets_at)
    _write_cache(raw, now, source=CACHE_SOURCE_STATUSLINE)


def _read_lock(now: float) -> tuple[float, str, int | None] | None:
    """Return (blocked_until, reason, status) if a fetch backoff is currently active, else None.

    ``reason`` is ``"rate_limited"`` (a server 429), ``"unavailable"`` (a server 5xx, with
    the HTTP code in ``status``) or ``"throttle"`` (our own minimum interval between fetches).
    """
    try:
        data = json.loads(LOCK_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    blocked_until = data.get("blocked_until")
    reason = data.get("reason", "throttle")
    status = data.get("status")
    if isinstance(blocked_until, (int, float)) and isinstance(reason, str) and blocked_until > now:
        return float(blocked_until), reason, status if isinstance(status, int) else None
    return None


def _write_lock(blocked_until: float, reason: str, status: int | None = None) -> None:
    try:
        LOCK_PATH.parent.mkdir(parents=True, exist_ok=True)
        payload: dict[str, object] = {"blocked_until": blocked_until, "reason": reason}
        if status is not None:
            payload["status"] = status
        LOCK_PATH.write_text(json.dumps(payload), encoding="utf-8")
    except OSError:
        pass


def _clear_lock() -> None:
    try:
        LOCK_PATH.unlink()
    except OSError:
        pass


def get_usage(
    cache_ttl: float = 60.0,
    bypass_throttle: bool = False,
    bypass_rate_limit: bool = False,
    min_fetch_interval: float = MIN_FETCH_INTERVAL,
    statusline_ttl: float = STATUSLINE_FRESH_TTL,
) -> UsageSnapshot | None:
    """Return the current usage snapshot, preferring the disk cache over a live fetch.

    Never raises: returns None when credentials are missing/expired and no usable
    cache exists. A stale cache is preferred over None when a live fetch is skipped
    or fails.

    Source order, cheapest first:
      1. A **statusline**-sourced cache entry younger than ``statusline_ttl`` — fed for free by
         a live Claude Code session, so the (rate-limited) API is never touched while working.
      2. Any cache entry younger than ``cache_ttl``.
      3. A live API fetch, rate-limit aware (see below).

    ``usage show --fresh`` sets both ``cache_ttl`` and ``statusline_ttl`` to 0 to force the
    live fetch. Fetches honour a server 429/5xx backoff (cached snapshot served, flagged stale)
    and our own inter-fetch throttle (``min_fetch_interval``); ``bypass_throttle`` (``--fresh``)
    skips only the throttle, never a server backoff. ``bypass_rate_limit`` (``usage show
    --force``) additionally overrides the server backoff and hits the endpoint regardless — the
    deliberate escape hatch when the caller accepts hammering a limited/overloaded API.
    """
    now = time.time()
    cached = _read_cache()
    if cached is not None:
        raw, fetched_at, source = cached
        if source == CACHE_SOURCE_STATUSLINE and statusline_ttl > 0 and now - fetched_at < statusline_ttl:
            return _parse(raw, fetched_at, from_cache=True, source=source)
        if now - fetched_at < cache_ttl:
            return _parse(raw, fetched_at, from_cache=True, source=source)

    lock = _read_lock(now)
    if lock is not None and not bypass_rate_limit:
        blocked_until, reason, status = lock
        # A server-side hold-off (429 or 5xx) is honoured even by --fresh — hammering a
        # limited/overloaded API can only make it worse. Only our own throttle yields to --fresh.
        # --force (bypass_rate_limit) skips this block entirely and fetches regardless.
        if reason in ("rate_limited", "unavailable") or not bypass_throttle:
            if cached is not None:
                if reason == "rate_limited":
                    return _parse(cached[0], cached[1], from_cache=True, rate_limited_until=blocked_until)
                if reason == "unavailable":
                    return _parse(
                        cached[0],
                        cached[1],
                        from_cache=True,
                        unavailable_until=blocked_until,
                        unavailable_status=status,
                    )
                return _parse(cached[0], cached[1], from_cache=True, throttled_until=blocked_until)
            return None

    token = _read_token()
    if token is None:
        return _parse(cached[0], cached[1], from_cache=True) if cached is not None else None

    _write_lock(now + min_fetch_interval, "throttle")
    result = _fetch(token, now)
    if isinstance(result, _FetchSuccess):
        _write_cache(result.raw, now)
        _clear_lock()
        return _parse(result.raw, now, fetched_now=True)
    if isinstance(result, _FetchRateLimited):
        blocked_until = now + result.retry_after
        _write_lock(blocked_until, "rate_limited")
        if cached is not None:
            return _parse(cached[0], cached[1], from_cache=True, rate_limited_until=blocked_until, fetched_now=True)
        return None

    if isinstance(result, _FetchError) and result.status is not None and result.status >= 500:
        # Server reachable but erroring/overloaded (5xx, incl. 529 Overloaded): back off and
        # serve the cached snapshot, flagged so the source note says "unavailable", not "unreachable".
        blocked_until = now + DEFAULT_RATE_LIMIT_BACKOFF
        _write_lock(blocked_until, "unavailable", status=result.status)
        if cached is not None:
            return _parse(
                cached[0],
                cached[1],
                from_cache=True,
                unavailable_until=blocked_until,
                unavailable_status=result.status,
                fetched_now=True,
            )
        return None

    # Transport error/timeout (or other non-200): keep the throttle lock so we don't hammer,
    # serve cache if any.
    return _parse(cached[0], cached[1], from_cache=True, fetched_now=True) if cached is not None else None
