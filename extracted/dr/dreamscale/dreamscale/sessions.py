"""Session orchestration: cold-start polling with progress, session cleanup, and
the 20s heartbeat task."""

from __future__ import annotations

import asyncio
import time
from collections.abc import Awaitable, Callable
from contextlib import suppress
from typing import Any

import httpx

from dreamscale import errors
from dreamscale.constants import (
    HEARTBEAT_S,
    POLL_INTERVAL_S,
    RESUME_POLL_INITIAL_S,
    START_TIMEOUT_S,
)
from dreamscale.control import Session
from dreamscale.policy.connection import rate_limited_delay_s

# How a region reads in progress lines; other region ids print as they are.
_REGION_LABELS = {"us-west-2": "us-west", "us-east-1": "us-east"}


def region_label(region: str | None) -> str | None:
    """``us-west`` for us-west-2 and ``us-east`` for us-east-1."""
    return _REGION_LABELS.get(region, region) if region else region


async def wait_until_ready(
    control: Any,
    session: Session,
    *,
    on_progress: Callable[[str], None],
    poll_interval_s: float = POLL_INTERVAL_S,
    progress_interval_s: float = 30.0,
    timeout_s: float | None = None,
    sleep: Callable[..., Any] = asyncio.sleep,
    clock: Callable[[], float] = time.monotonic,
    on_status: Callable[[Session], None] | None = None,
    restart_session: Callable[[], Awaitable[Session]] | None = None,
) -> Session:
    """Poll GET /v1/sessions/{id} until ready/active. Each poll refreshes the lease.

    ``on_status`` sees every session the poll observes (queued, starting, ready...), so a
    caller can follow the queue without parsing progress lines."""
    from dreamscale.terminal import compute_progress

    with compute_progress(on_progress, clock=clock) as progress:
        # A keep-warm reclaim keeps the parked session's original created_at, so its
        # age measures earlier tasks, not this start. Only a fresh launch spends it.
        reclaimed = session.selection_reason == "keep_warm_reuse"
        started_at = clock()
        cap = started_at + timeout_s if timeout_s is not None else float("inf")

        def deadline_of(s: Session) -> float:
            """When this start gives up, on ``clock()``: the server's ``startup_timeout_s``
            from the session's creation (a reclaim's from now), within the caller's own
            ``timeout_s``. Read on every poll: the server raises it while a training run
            makes room for this robot (DSL-310), and lowers it back after."""
            budget = s.startup_timeout_s or START_TIMEOUT_S
            if s.startup_timeout_s and s.created_at is not None and not reclaimed:
                return min(cap, clock() + max(0.0, budget - max(0.0, time.time() - s.created_at)))
            return min(cap, started_at + budget)

        deadline = deadline_of(session)
        current = session
        announced = False
        queue_announced = False
        last_progress_at = 0.0
        last_retry_progress_at = float("-inf")
        last_eta_s: int | None = None
        last_phase: str | None = None
        resume_poll_s = RESUME_POLL_INITIAL_S
        fallback: str | None = None  # the next-closest region a server started in
        noted = False  # a note with no region (a training run making room) is said once
        restarted = False
        while True:
            now = clock()
            if on_status is not None:
                on_status(current)
            if current.starting_note and current.starting_region:
                if current.starting_region != fallback:
                    # Its region is full: a server starts in the next-closest one.
                    fallback = current.starting_region
                    progress(current.starting_note)
            elif current.starting_note and not noted:
                noted = True
                progress(current.starting_note)
            if current.status in ("ready", "active"):
                if not fallback and current.region_notice and current.region_fallback:
                    # The fallback can become ready between polls, without the client ever
                    # observing its loading note. The ready response still records the move.
                    fallback = current.region
                if fallback and region_label(current.region) == region_label(fallback):
                    progress(
                        f"Running in {region_label(current.region) or current.region}, the "
                        "next-closest region: each request takes a little longer."
                    )
                elif fallback and current.region:
                    # Its own region's server came free before the next-closest one.
                    progress(f"A server in {region_label(current.region)} came free first; "
                             "running there.")
                if current.region_probe_status == "failed":
                    progress(
                        "Region latency check was unavailable; "
                        f"used deterministic fallback {region_label(current.region) or 'routing'}."
                    )
                elif current.region_probe_status == "degraded":
                    progress(
                        "Region latency check was partial; "
                        f"selected {region_label(current.region) or 'the best measured region'}."
                    )
                if current.region_notice:
                    progress(
                        f"Using {region_label(current.routed_region)} for faster compute "
                        "availability."
                    )
                if current.low_balance:
                    progress(
                        f"Low balance. {errors.CREDITS_FIX} before the session is interrupted."
                    )
                return current
            restart_needed = (
                current.status in ("closed", "expired") and current.reason == "deployment_restarted"
            ) or (
                restarted and current.status == "failed"
                and (current.error or {}).get("code") == "deployment_requalifying"
            )
            if restart_needed and restart_session is not None:
                remaining_s = deadline - clock()
                if remaining_s <= 0:
                    raise errors.catalog("start_failed")
                progress(
                    "The deployment restarted while starting; connecting to its new server…"
                )
                try:
                    async with asyncio.timeout(remaining_s):
                        while True:
                            try:
                                current = await restart_session()
                                break
                            except errors.DreamscaleError as error:
                                if error.code != "deployment_requalifying":
                                    raise
                                remaining_s = deadline - clock()
                                if remaining_s <= poll_interval_s:
                                    raise errors.catalog("start_failed") from None
                                await sleep(poll_interval_s)
                except TimeoutError:
                    raise errors.catalog("start_failed") from None
                # A new session's creation time must not grant a new startup budget.
                restarted = True
                announced = queue_announced = False
                continue
            if current.status == "failed":
                raise errors.from_payload({"error": current.error or {}})
            if current.status in ("closed", "expired"):
                if current.reason == "quota_exhausted":
                    raise errors.catalog("insufficient_credits")
                if current.reason == "idle_timeout":
                    raise errors.catalog("idle_timeout")
                raise errors.catalog("session_expired")
            if current.status == "queued":
                # No capacity yet — keep polling like `starting`, but with a queue notice.
                # The overall deadline still applies (a queue that never clears times out).
                place = ""
                if current.queue_position is not None:
                    place = f", position {current.queue_position} in the queue"
                    # A training run making room (a note with no region) gives its own time.
                    pausing = bool(current.starting_note) and not current.starting_region
                    if current.queue_eta_s and not pausing:
                        place += f" (about {current.queue_eta_s}s)"
                if not queue_announced:
                    progress(f"Waiting for your compute to become available: 0s elapsed{place}")
                    queue_announced = True
                    last_progress_at = now
                elif now - last_progress_at >= progress_interval_s:
                    elapsed = int(max(0.0, now - started_at))
                    progress(
                        f"Waiting for your compute to become available: {elapsed}s elapsed{place}"
                    )
                    last_progress_at = now
            elif current.startup_phase and current.startup_phase.startswith("restoring"):
                if (
                    last_phase != current.startup_phase
                    or now - last_progress_at >= progress_interval_s
                ):
                    progress(
                        "Restoring archived model storage: "
                        f"{int(max(0, now - started_at))}s elapsed"
                    )
                    last_progress_at = now
                    last_phase = current.startup_phase
                    announced = False
            elif current.status == "resuming":
                # A warm worker confirms a reclaim within milliseconds; poll on a short
                # backoff instead of a full cold-start interval.
                pass
            else:
                # status == "starting"
                eta = (
                    f" (estimate {current.eta_s}s; model load can take longer)"
                    if current.eta_s else ""
                )
                if not announced:
                    progress(f"Starting your compute: 0s elapsed{eta}")
                    announced = True
                    last_progress_at = now
                    last_eta_s = current.eta_s
                elif (
                    current.eta_s != last_eta_s or now - last_progress_at >= progress_interval_s
                ):
                    elapsed = int(max(0.0, now - started_at))
                    progress(f"Starting your compute: {elapsed}s elapsed{eta}")
                    last_progress_at = now
                    last_eta_s = current.eta_s
            if now >= deadline:
                raise errors.catalog("start_failed")
            interval = poll_interval_s
            if current.status == "resuming":
                interval = min(poll_interval_s, resume_poll_s)
                resume_poll_s = min(poll_interval_s, resume_poll_s * 2)
            await sleep(min(interval, deadline - now))
            remaining_s = deadline - clock()
            if remaining_s <= 0:
                raise errors.catalog("start_failed")
            try:
                async with asyncio.timeout(remaining_s):
                    current = await control.get_session(current.session_id)
                refreshed_deadline = deadline_of(current)
                deadline = min(deadline, refreshed_deadline) if restarted else refreshed_deadline
            except TimeoutError:
                raise errors.catalog("start_failed") from None
            except (
                httpx.TimeoutException, httpx.NetworkError, httpx.RemoteProtocolError,
                errors.ServerError,
            ):
                # GET is safe to repeat for this lease (a 5xx is a control-plane redeploy,
                # not a verdict on the session). Keep the original startup deadline; never
                # replay session creation or a model prediction.
                if clock() - last_retry_progress_at >= progress_interval_s:
                    progress("Connection interrupted while compute starts; retrying this session…")
                    last_retry_progress_at = clock()


async def stop_session(control: Any, session_id: str) -> None:
    with suppress(Exception):
        await control.delete_session(session_id)


class Heartbeat:
    """POST heartbeat every HEARTBEAT_S; sets `expired` when the session is gone."""

    def __init__(
        self,
        control: Any,
        session_id: str,
        *,
        interval_s: float = HEARTBEAT_S,
        sleep: Callable[..., Any] = asyncio.sleep,
    ) -> None:
        self._control = control
        self._session_id = session_id
        self._interval_s = interval_s
        self._sleep = sleep
        self._task: asyncio.Task | None = None
        self.expired = asyncio.Event()
        # The session as the last heartbeat answered it (None until one has).
        self.latest: dict[str, Any] | None = None

    def start(self) -> None:
        self._task = asyncio.create_task(self._run())

    async def _run(self) -> None:
        delay_s = self._interval_s
        while True:
            await self._sleep(delay_s)
            delay_s = self._interval_s
            try:
                answer = await self._control.heartbeat(self._session_id)
                if isinstance(answer, dict):
                    self.latest = answer
            except errors.ServerError:
                # A control-plane redeploy answers 502/503 for a while; the session on the
                # worker is untouched. Keep heartbeating, like any transient network error.
                continue
            except errors.DreamscaleError as exc:
                if exc.code == "rate_limited":
                    # A 429 (a WAF rule, a busy NAT) says wait, not that the session is gone:
                    # the next beat waits as Retry-After says, jittered, never sooner than usual.
                    retry_after_s = getattr(exc, "retry_after_s", None)
                    delay_s = max(self._interval_s, rate_limited_delay_s(retry_after_s))
                    continue
                self.expired.set()
                return
            except httpx.HTTPError:
                continue  # transient; GET polls / data-plane activity also refresh the lease

    async def wait_expired(self, timeout: float) -> None:  # noqa: ASYNC109 (bounded test helper)
        try:
            await asyncio.wait_for(self.expired.wait(), timeout=timeout)
        except TimeoutError:
            pass

    async def stop(self) -> None:
        if self._task is not None:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
