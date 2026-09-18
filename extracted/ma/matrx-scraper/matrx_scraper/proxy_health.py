"""Proxy-pool health — the telemetry that would have told us.

On 2026-09-17 a 60-URL block hunt found 11 targets failing with an identical
`proxy_error` / `curl: (7) CONNECT tunnel failed, response 403`: IRS.gov,
SEC EDGAR, OSHA, FDA, eCFR, the Federal Register, PubMed, California's
legislature and courts, `docs.stripe.com` and `youtube.com`. None of those
sites blocked us — **our own proxy vendor refused to open the tunnel**, which
is what a 403 on the CONNECT (rather than on the page) means. Nothing in the
system could tell the two apart, so an infrastructure outage read as "the web
is hostile" for an unknown length of time.

This module is deliberately tiny and in-process: counters plus a short-lived
per-host memory of which destinations the pool refuses, exposed on
`/health/ready` as `proxy_pool`. It is evidence, never a gate — no request is
ever blocked by what is recorded here.
"""

from __future__ import annotations

import time
from collections import Counter
from threading import Lock
from urllib.parse import urlparse

#: How long a host stays on the "the pool refuses this destination" list. Long
#: enough to spare the next request three doomed proxy attempts, short enough
#: that a vendor fixing their ACL is picked up without a deploy.
REFUSAL_MEMORY_SECONDS = 900.0

#: Cap the refusal map so a pool-wide outage cannot grow it without bound.
REFUSAL_MEMORY_MAX_HOSTS = 500

_lock = Lock()
_counters: Counter[str] = Counter()
_refused_hosts: dict[str, float] = {}
_last_proxy_error: str | None = None
_last_proxy_error_at: float | None = None


def host_of(url: str) -> str:
    try:
        return (urlparse(url).hostname or "").lower()
    except Exception:
        return ""


def record_attempt(*, proxied: bool) -> None:
    with _lock:
        _counters["attempts"] += 1
        _counters["proxied_attempts" if proxied else "direct_attempts"] += 1


def record_proxy_refusal(url: str, reason: str | None) -> None:
    """The pool itself refused to carry this request (CONNECT failed / 407)."""
    global _last_proxy_error, _last_proxy_error_at
    host = host_of(url)
    now = time.monotonic()
    with _lock:
        _counters["proxy_refusals"] += 1
        _last_proxy_error = (reason or "")[:300] or None
        _last_proxy_error_at = time.time()
        if host:
            if len(_refused_hosts) >= REFUSAL_MEMORY_MAX_HOSTS and host not in _refused_hosts:
                # Drop the oldest rather than refusing to learn.
                oldest = min(_refused_hosts, key=_refused_hosts.__getitem__)
                _refused_hosts.pop(oldest, None)
            _refused_hosts[host] = now


def record_proxy_success(url: str) -> None:
    """A proxy carried this host fine — forget any refusal we remembered."""
    host = host_of(url)
    with _lock:
        _counters["proxy_successes"] += 1
        _refused_hosts.pop(host, None)


def pool_refuses(url: str) -> bool:
    """Did the pool refuse this host recently? Used to go direct FIRST."""
    host = host_of(url)
    if not host:
        return False
    now = time.monotonic()
    with _lock:
        seen = _refused_hosts.get(host)
        if seen is None:
            return False
        if now - seen > REFUSAL_MEMORY_SECONDS:
            _refused_hosts.pop(host, None)
            return False
        return True


def record_direct_fallback(*, rescued: bool) -> None:
    """A proxy-refused request was retried without the proxy."""
    with _lock:
        _counters["direct_fallbacks"] += 1
        if rescued:
            _counters["direct_fallback_rescues"] += 1


def proxy_health_snapshot() -> dict[str, object]:
    """What `/health/ready` publishes. Hostnames only — never a proxy URL,
    which carries the vendor username and password."""
    now = time.monotonic()
    with _lock:
        live = sorted(
            host
            for host, seen in _refused_hosts.items()
            if now - seen <= REFUSAL_MEMORY_SECONDS
        )
        counters = dict(_counters)
        last_error = _last_proxy_error
        last_error_at = _last_proxy_error_at
    attempts = counters.get("proxied_attempts", 0)
    refusals = counters.get("proxy_refusals", 0)
    return {
        **counters,
        "refusal_rate": round(refusals / attempts, 4) if attempts else 0.0,
        "refused_hosts": live,
        "refused_host_count": len(live),
        "last_proxy_error": last_error,
        "last_proxy_error_at": last_error_at,
    }


def reset_for_tests() -> None:
    global _last_proxy_error, _last_proxy_error_at
    with _lock:
        _counters.clear()
        _refused_hosts.clear()
        _last_proxy_error = None
        _last_proxy_error_at = None
