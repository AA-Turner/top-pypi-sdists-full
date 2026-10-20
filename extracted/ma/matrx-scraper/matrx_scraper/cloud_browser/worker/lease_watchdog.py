"""THE LEASE WATCHDOG'S QUESTION: is the control plane gone, or only unreachable?

A worker whose lease nobody renews used to end itself 150 s after the last
renewal (60 s lease + 90 s grace). That is right when the control plane has
truly let the run go, and wrong whenever the renewer is merely failing or the
server cannot be reached: on 2026-10-17 a suspended renewer ended every Cloud
Computer, and a database blip or a deploy gap would do the same. Arman: a
machine never fails on its own.

So once the grace has passed the worker ASKS (``POST /browser-worker/lease-check``
on the server its bootstrap named) and acts only on a definite answer:

- ``ended`` — the server says this run (this activation) is over: stop, as before.
- ``live`` — the run is still wanted and only the renewals stopped: keep running.
- anything else (timeout, refused, 5xx, a database error answered as 503) is
  ``unknown``: keep running, for at most ``unreachable_max_seconds`` (0 = for
  ever). The server sends that value and the probe interval with every answer
  (knobs ``cloud_browser.worker_watchdog.*``); the worker keeps the last ones.
  Until the first answer it asks on every watchdog tick and has no limit: a
  worker that has never heard the server's limit never ends on silence.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Literal
from urllib.parse import urlsplit

import httpx

logger = logging.getLogger(__name__)

LEASE_CHECK_PATH = "/browser-worker/lease-check"

Verdict = Literal["live", "ended", "unknown"]


@dataclass(frozen=True)
class LeaseCheck:
    verdict: Verdict
    probe_interval_seconds: int | None = None
    unreachable_max_seconds: int | None = None
    detail: str = ""


def lease_check_url(callback_url: str | None) -> str | None:
    """The lease-check door on the server that bootstrapped this run."""
    if not callback_url:
        return None
    parts = urlsplit(callback_url)
    if parts.scheme not in {"http", "https"} or not parts.netloc:
        return None
    return f"{parts.scheme}://{parts.netloc}{LEASE_CHECK_PATH}"


async def probe_control_plane(
    url: str | None,
    *,
    run_id: str,
    activation_key: str,
    worker_id: str,
    timeout_seconds: float,
    client: httpx.AsyncClient | None = None,
) -> LeaseCheck:
    """Ask the server about this run. Never raises; no answer is ``unknown``."""
    if not url:
        return LeaseCheck("unknown", detail="no control-plane address")
    body = {"run_id": run_id, "activation_key": activation_key, "worker_id": worker_id}
    try:
        if client is None:
            async with httpx.AsyncClient(timeout=timeout_seconds) as owned:
                response = await owned.post(url, json=body)
        else:
            response = await client.post(url, json=body, timeout=timeout_seconds)
    except Exception as exc:  # noqa: BLE001 — unreachable is an answer, not a crash
        return LeaseCheck("unknown", detail=f"{type(exc).__name__}: {exc}"[:300])
    if response.status_code != 200:
        return LeaseCheck("unknown", detail=f"HTTP {response.status_code}")
    try:
        data = response.json()
        verdict = data.get("verdict")
        if verdict not in {"live", "ended"}:
            return LeaseCheck("unknown", detail=f"unrecognised verdict {verdict!r}")
        return LeaseCheck(
            verdict,
            probe_interval_seconds=_positive_int(data.get("probe_interval_seconds")),
            unreachable_max_seconds=_non_negative_int(data.get("unreachable_max_seconds")),
        )
    except Exception as exc:  # noqa: BLE001
        return LeaseCheck("unknown", detail=f"unreadable answer: {exc}"[:300])


def _positive_int(value: object) -> int | None:
    try:
        n = int(value)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return None
    return n if n > 0 else None


def _non_negative_int(value: object) -> int | None:
    try:
        n = int(value)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return None
    return n if n >= 0 else None


class WatchdogState:
    """What the watchdog remembers between ticks once a lease has lapsed."""

    def __init__(self) -> None:
        #: None until the server's first answer: ask on every tick, never give up.
        self.probe_interval_seconds: int | None = None
        self.unreachable_max_seconds: int | None = None
        self.last_probe_at: datetime | None = None
        self.unreachable_since: datetime | None = None

    def reset(self) -> None:
        """A renewal arrived (or there is no run): nothing is lapsed any more."""
        self.last_probe_at = None
        self.unreachable_since = None

    def probe_due(self, now: datetime) -> bool:
        if self.last_probe_at is None or self.probe_interval_seconds is None:
            return True
        return now - self.last_probe_at >= timedelta(seconds=self.probe_interval_seconds)

    def decide(self, check: LeaseCheck, now: datetime) -> Literal["stay", "end"]:
        self.last_probe_at = now
        if check.probe_interval_seconds is not None:
            self.probe_interval_seconds = check.probe_interval_seconds
        if check.unreachable_max_seconds is not None:
            self.unreachable_max_seconds = check.unreachable_max_seconds
        if check.verdict == "ended":
            return "end"
        if check.verdict == "live":
            self.unreachable_since = None
            return "stay"
        if self.unreachable_since is None:
            self.unreachable_since = now
        limit = self.unreachable_max_seconds
        if limit and now - self.unreachable_since >= timedelta(seconds=limit):
            return "end"
        return "stay"
