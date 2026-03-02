"""CronScheduler — asyncio-based scheduler for automation jobs."""

from __future__ import annotations

import asyncio
import json
import logging
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from .models import AutomationJob, ExecutionMode, ScheduleType
from .storage import AutomationStorage

log = logging.getLogger(__name__)

# Interval pattern: digits followed by m/h/d/w
_INTERVAL_RE = re.compile(r"^(\d+)\s*([mhdw])$", re.IGNORECASE)

_INTERVAL_MULTIPLIERS = {
    "m": timedelta(minutes=1),
    "h": timedelta(hours=1),
    "d": timedelta(days=1),
    "w": timedelta(weeks=1),
}

HEARTBEAT_JOB_ID = "__heartbeat__"

# Exponential backoff tiers: 30s → 1m → 5m → 15m → 60m
_BACKOFF_TIERS = [
    timedelta(seconds=30),
    timedelta(minutes=1),
    timedelta(minutes=5),
    timedelta(minutes=15),
    timedelta(minutes=60),
]


def _parse_interval(value: str) -> timedelta:
    """Parse "30m", "2h", "1d", "1w" into a timedelta."""
    m = _INTERVAL_RE.match(value.strip())
    if not m:
        raise ValueError(f"Invalid interval format: {value!r}  (expected e.g. '30m', '2h', '1d')")
    count = int(m.group(1))
    unit = m.group(2).lower()
    return count * _INTERVAL_MULTIPLIERS[unit]


def _compute_next_run(job: AutomationJob, now: datetime) -> str | None:
    """Compute the next run time for a job and return as ISO string."""
    if job.schedule_type == ScheduleType.AT or job.schedule_type == "at":
        target = datetime.fromisoformat(job.schedule_value)
        if target.tzinfo is None:
            target = target.replace(tzinfo=timezone.utc)
        return target.isoformat() if target > now else None

    if job.schedule_type == ScheduleType.EVERY or job.schedule_type == "every":
        delta = _parse_interval(job.schedule_value)
        if job.last_run_at:
            base = datetime.fromisoformat(job.last_run_at)
            if base.tzinfo is None:
                base = base.replace(tzinfo=timezone.utc)
            nxt = base + delta
        else:
            nxt = now + delta
        return nxt.isoformat()

    if job.schedule_type == ScheduleType.CRON or job.schedule_type == "cron":
        try:
            from croniter import croniter
            cron = croniter(job.schedule_value, now)
            return cron.get_next(datetime).replace(tzinfo=timezone.utc).isoformat()
        except Exception:
            log.warning("Failed to parse cron expression %r", job.schedule_value)
            return None

    return None


class CronScheduler:
    """Asyncio scheduler that ticks every 30 s and dispatches due jobs."""

    def __init__(self, storage: AutomationStorage, emdash_dir: Path) -> None:
        self._storage = storage
        self._emdash_dir = emdash_dir
        self._server_url: str = ""
        self._task: asyncio.Task | None = None
        self._jobs: list[AutomationJob] = []
        self._running_count = 0
        self._stop_event = asyncio.Event()

    # -- Lifecycle -----------------------------------------------------------

    async def start(self, server_url: str) -> None:
        self._server_url = server_url
        self._jobs = self._storage.load_jobs()
        self._ensure_heartbeat()
        self._stop_event.clear()
        self._task = asyncio.create_task(self._scheduler_loop(), name="automation-scheduler")
        log.info("Automation scheduler started (%d jobs)", len(self._jobs))
        print(f"Automation scheduler started ({len(self._jobs)} jobs, cron_enabled={self._storage.load_config().cron_enabled})", flush=True)

        # Catch-up: dispatch jobs that were missed while server was down
        asyncio.create_task(self._run_missed_jobs())

    async def _run_missed_jobs(self) -> None:
        """Dispatch jobs that should have fired while the server was down."""
        config = self._storage.load_config()
        if not config.cron_enabled:
            return

        now = datetime.now(timezone.utc)
        missed = []

        for job in self._jobs:
            if not job.enabled or job.one_shot:
                continue
            if job.id == HEARTBEAT_JOB_ID:
                continue  # don't catch up heartbeats
            if not job.next_run_at:
                continue
            nxt = datetime.fromisoformat(job.next_run_at)
            if nxt.tzinfo is None:
                nxt = nxt.replace(tzinfo=timezone.utc)
            if nxt < now:
                missed.append(job)

        if not missed:
            return

        print(f"[Scheduler] Catching up {len(missed)} missed job(s)", flush=True)
        for job in missed:
            try:
                print(f"[Scheduler] Catch-up: {job.id} ({job.name})", flush=True)
                await self._dispatch_job(job, now)
            except Exception as exc:
                print(f"[Scheduler] Catch-up failed for {job.id}: {exc}", flush=True)
                log.exception("Catch-up dispatch failed for job %s", job.id)

    async def stop(self) -> None:
        self._stop_event.set()
        if self._task and not self._task.done():
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        log.info("Automation scheduler stopped")

    # -- Main loop -----------------------------------------------------------

    async def _scheduler_loop(self) -> None:
        while not self._stop_event.is_set():
            try:
                await self._tick()
            except Exception as exc:
                print(f"[Scheduler] Tick error: {exc}", flush=True)
                log.exception("Scheduler tick error")
            try:
                await asyncio.wait_for(self._stop_event.wait(), timeout=30)
                break  # stop_event was set
            except asyncio.TimeoutError:
                pass  # normal 30s tick

    async def _tick(self) -> None:
        config = self._storage.load_config()
        if not config.cron_enabled:
            return

        now = datetime.now(timezone.utc)
        enabled_jobs = [j for j in self._jobs if j.enabled]
        print(f"[Scheduler] Tick at {now.isoformat()} — {len(enabled_jobs)} enabled jobs", flush=True)
        to_delete: list[str] = []

        for job in list(self._jobs):
            if not job.enabled:
                continue
            if self._running_count >= config.max_concurrent_runs:
                break
            if not self._is_due(job, now, config):
                continue

            print(f"[Scheduler] Dispatching job {job.id} ({job.name})", flush=True)

            # Disable one-shot jobs BEFORE dispatch so they never re-fire
            if job.one_shot:
                job.enabled = False
                to_delete.append(job.id)

            try:
                await self._dispatch_job(job, now)
            except Exception as exc:
                print(f"[Scheduler] Dispatch failed for {job.id}: {exc}", flush=True)
                log.exception("Dispatch failed for job %s", job.id)

        # Remove one-shot jobs from disk regardless of dispatch outcome
        if to_delete:
            self._jobs = [j for j in self._jobs if j.id not in to_delete]
            self._storage.save_jobs(self._jobs)

    @staticmethod
    def _backoff_delay(consecutive_errors: int) -> timedelta:
        """Return the backoff delay for the given error count (0 = no backoff)."""
        if consecutive_errors <= 0:
            return timedelta(0)
        idx = min(consecutive_errors - 1, len(_BACKOFF_TIERS) - 1)
        return _BACKOFF_TIERS[idx]

    def _is_in_backoff(self, job: AutomationJob, now: datetime) -> bool:
        """Return True if a recurring job is still in exponential backoff."""
        if job.consecutive_errors <= 0 or not job.last_run_at:
            return False
        last = datetime.fromisoformat(job.last_run_at)
        if last.tzinfo is None:
            last = last.replace(tzinfo=timezone.utc)
        delay = self._backoff_delay(job.consecutive_errors)
        return now < last + delay

    def _is_due(self, job: AutomationJob, now: datetime, config: Any) -> bool:
        # Skip jobs in exponential backoff (only recurring, not one-shot)
        if not job.one_shot and self._is_in_backoff(job, now):
            return False

        # Heartbeat: check active hours
        if job.id == HEARTBEAT_JOB_ID:
            hb = config.heartbeat
            if not hb.enabled:
                return False
            local_hour = now.astimezone().hour
            if not (hb.active_hours[0] <= local_hour < hb.active_hours[1]):
                return False

        if job.schedule_type in (ScheduleType.AT, "at"):
            target = datetime.fromisoformat(job.schedule_value)
            if target.tzinfo is None:
                target = target.replace(tzinfo=timezone.utc)
            return now >= target

        if job.schedule_type in (ScheduleType.EVERY, "every"):
            delta = _parse_interval(job.schedule_value)
            if job.last_run_at:
                base = datetime.fromisoformat(job.last_run_at)
                if base.tzinfo is None:
                    base = base.replace(tzinfo=timezone.utc)
                return now >= base + delta
            # Never run before — due immediately
            return True

        if job.schedule_type in (ScheduleType.CRON, "cron"):
            try:
                from croniter import croniter
                if job.last_run_at:
                    base = datetime.fromisoformat(job.last_run_at)
                    if base.tzinfo is None:
                        base = base.replace(tzinfo=timezone.utc)
                else:
                    base = now - timedelta(minutes=1)
                cron = croniter(job.schedule_value, base)
                nxt = cron.get_next(datetime)
                if nxt.tzinfo is None:
                    nxt = nxt.replace(tzinfo=timezone.utc)
                return now >= nxt
            except Exception:
                return False

        return False

    # -- Dispatch ------------------------------------------------------------

    async def _dispatch_job(self, job: AutomationJob, now: datetime) -> None:
        job.last_run_at = now.isoformat()
        job.run_count += 1
        job.next_run_at = _compute_next_run(job, now)
        self._storage.save_jobs(self._jobs)

        try:
            # Both modes trigger the LLM — the agent is proactive, not a
            # static message relay.  ``main_session`` re-uses the ongoing
            # conversation context while ``isolated`` starts a fresh session.
            self._running_count += 1
            if job.mode in (ExecutionMode.MAIN_SESSION, "main_session"):
                asyncio.create_task(self._run_main_session_wrapper(job))
            else:
                asyncio.create_task(self._run_isolated_wrapper(job))
            # Success — reset backoff
            job.consecutive_errors = 0
            job.last_status = "ok"
            job.last_error = None
        except Exception as exc:
            job.consecutive_errors += 1
            job.last_status = "error"
            job.last_error = str(exc)[:200]
            backoff = self._backoff_delay(job.consecutive_errors)
            print(
                f"[Scheduler] Job {job.id} failed ({job.consecutive_errors} consecutive), "
                f"backoff {backoff.total_seconds()}s: {exc}",
                flush=True,
            )
            raise
        finally:
            self._storage.save_jobs(self._jobs)

    # -- Main-session LLM dispatch -------------------------------------------

    async def _run_main_session_wrapper(self, job: AutomationJob) -> None:
        """Background wrapper for main-session LLM invocation."""
        try:
            await self._run_main_session(job)
        except Exception:
            log.exception("Main-session run failed for job %s", job.id)
        finally:
            self._running_count -= 1

    async def _run_main_session(self, job: AutomationJob) -> None:
        """Trigger the LLM agent for a main-session job and deliver the response.

        Instead of injecting a static reminder text, this invokes the agent so
        it can reason about the payload, access tools, take context into
        consideration, and produce a proactive response.
        """
        import httpx

        url = f"{self._server_url}/api/agent/chat"
        payload = {
            "message": (
                f"[Scheduled — {job.name}] {job.payload}\n\n"
                "You are being triggered proactively by a scheduled job. "
                "Act on the above task: analyse the situation, use your tools "
                "if needed, and provide a useful, actionable response."
            ),
            "options": {"agent_type": "open"},
        }

        response_text = ""
        try:
            async with httpx.AsyncClient(timeout=180) as client:
                async with client.stream("POST", url, json=payload) as resp:
                    resp.raise_for_status()
                    response_text = await self._read_agent_response_from_sse(resp)
        except Exception:
            log.exception("HTTP call failed for main-session job %s", job.id)
            return

        if response_text:
            try:
                from ..channels.router import get_channel_router
                from ..channels.base import ChannelEvent

                router = get_channel_router()
                if router:
                    event = ChannelEvent(
                        type="text",
                        content=response_text,
                        metadata={
                            "source": "automation",
                            "job_id": job.id,
                            "job_name": job.name,
                        },
                    )
                    sender_id = self._resolve_sender_id(router)
                    print(
                        f"[Scheduler] Delivering main-session LLM response "
                        f"for job {job.id} to sender_id={sender_id}",
                        flush=True,
                    )
                    result = await router.deliver(event, sender_id=sender_id)
                    print(
                        f"[Scheduler] Delivery result: channel={result.channel}, "
                        f"success={result.success}, error={result.error}",
                        flush=True,
                    )
            except Exception:
                log.exception(
                    "Failed to deliver main-session result for job %s", job.id
                )

        log.info(
            "Main-session job %s completed (%d chars response)",
            job.id,
            len(response_text),
        )

    @staticmethod
    def _resolve_sender_id(router) -> str:
        """Get a usable sender_id for outbound delivery on the active channel.

        Uses the last known sender from the router's *primary* channel
        (tracked when the user sends a message).  Falls back to the primary
        channel's ``authorized_chats`` config (e.g. Telegram), then
        ``'default'`` for StoredChannel.
        """
        # Prefer the last sender who interacted on the active channel
        last = router.last_sender_id
        if last:
            return last

        # Fallback: check the primary (active) channel for a default sender
        primary = router.primary
        if primary:
            try:
                if (
                    hasattr(primary, "_config")
                    and hasattr(primary._config, "authorized_chats")
                    and primary._config.authorized_chats
                ):
                    chat_id = str(primary._config.authorized_chats[0])
                    log.info(
                        "No last_sender_id on %s; using authorized_chat %s",
                        primary.name,
                        chat_id,
                    )
                    return chat_id
            except Exception:
                pass

        log.warning(
            "No last_sender_id and no authorized_chats on active channel — "
            "CRON delivery will fall back to StoredChannel (pending.json). "
            "Send a message on the active channel or configure authorized_chats "
            "to enable direct delivery."
        )
        return "default"

    async def _run_isolated_wrapper(self, job: AutomationJob) -> None:
        try:
            await self._run_isolated(job)
        except Exception:
            log.exception("Isolated run failed for job %s", job.id)
        finally:
            self._running_count -= 1

    async def _run_isolated(self, job: AutomationJob) -> None:
        """POST to the local agent/chat endpoint and deliver the result."""
        import httpx

        url = f"{self._server_url}/api/agent/chat"
        payload = {
            "message": f"[Automation: {job.name}] {job.payload}",
            "options": {"agent_type": "open"},
        }

        response_text = ""
        try:
            async with httpx.AsyncClient(timeout=120) as client:
                async with client.stream("POST", url, json=payload) as resp:
                    resp.raise_for_status()
                    response_text = await self._read_agent_response_from_sse(resp)
        except Exception:
            log.exception("HTTP call failed for isolated job %s", job.id)
            return

        if response_text:
            try:
                from ..channels.router import get_channel_router
                from ..channels.base import ChannelEvent

                router = get_channel_router()
                if router:
                    event = ChannelEvent(
                        type="text",
                        content=response_text,
                        metadata={"source": "automation", "job_id": job.id},
                    )
                    sender_id = self._resolve_sender_id(router)
                    print(
                        f"[Scheduler] Delivering isolated LLM response "
                        f"for job {job.id} to sender_id={sender_id}",
                        flush=True,
                    )
                    result = await router.deliver(event, sender_id=sender_id)
                    print(
                        f"[Scheduler] Isolated delivery result: channel={result.channel}, "
                        f"success={result.success}, error={result.error}",
                        flush=True,
                    )
            except Exception:
                log.exception("Failed to deliver isolated result for job %s", job.id)

        log.info("Isolated job %s completed (%d chars)", job.id, len(response_text))

    @staticmethod
    async def _read_agent_response_from_sse(resp: Any) -> str:
        """Read SSE stream from /api/agent/chat and extract assistant text.

        Supports both canonical event framing (`event: response`) and legacy
        payload-style typing (`data: {"type": "content", ...}`).
        """
        current_event: str | None = None
        chunks: list[str] = []
        final_response = ""

        async for raw_line in resp.aiter_lines():
            line = raw_line.strip()
            if not line:
                continue

            if line.startswith("event: "):
                current_event = line[7:].strip()
                continue

            if not line.startswith("data: "):
                continue

            try:
                data = json.loads(line[6:])
            except (json.JSONDecodeError, TypeError):
                continue

            event_type = current_event or str(data.get("type", "")).strip()
            if not event_type:
                continue

            if event_type in ("message_complete", "session_end"):
                break

            if event_type == "error":
                message = data.get("message")
                if message:
                    log.warning("Automation SSE stream reported error: %s", message)
                continue

            content = data.get("content")
            if not content:
                continue

            text = str(content)
            if event_type == "response":
                final_response = text
                chunks.clear()
                continue

            if event_type in {"partial_response", "assistant_text", "content"} and not final_response:
                chunks.append(text)

        return final_response or "".join(chunks)

    # -- Heartbeat management ------------------------------------------------

    def _ensure_heartbeat(self) -> None:
        """Ensure the synthetic heartbeat job exists.

        Only persists to disk when there are real user jobs or the heartbeat
        is enabled.  This avoids eagerly creating the .emdash/automation/
        folder for agent types that don't use automation (e.g. coding agent).
        """
        config = self._storage.load_config()
        hb = config.heartbeat
        existing = next((j for j in self._jobs if j.id == HEARTBEAT_JOB_ID), None)

        if existing:
            # Sync config into the existing synthetic job
            existing.schedule_value = f"{hb.interval_minutes}m"
            existing.payload = hb.payload
            existing.enabled = hb.enabled
        else:
            self._jobs.append(AutomationJob(
                id=HEARTBEAT_JOB_ID,
                name="Heartbeat",
                schedule_type="every",
                schedule_value=f"{hb.interval_minutes}m",
                payload=hb.payload,
                mode="main_session",
                enabled=hb.enabled,
            ))

        # Only persist when there's something meaningful to save.
        # This prevents creating .emdash/automation/ for non-open agents.
        has_user_jobs = any(j.id != HEARTBEAT_JOB_ID for j in self._jobs)
        if has_user_jobs or hb.enabled:
            self._storage.save_jobs(self._jobs)

    # -- CRUD (sync, called from tool / API) ---------------------------------

    def add_job(self, job: AutomationJob) -> AutomationJob:
        now = datetime.now(timezone.utc)
        if not job.created_at:
            job.created_at = now.isoformat()
        job.next_run_at = _compute_next_run(job, now)
        if job.schedule_type in (ScheduleType.AT, "at"):
            job.one_shot = True
        self._jobs.append(job)
        self._storage.save_jobs(self._jobs)
        return job

    def remove_job(self, job_id: str) -> bool:
        before = len(self._jobs)
        self._jobs = [j for j in self._jobs if j.id != job_id]
        if len(self._jobs) < before:
            self._storage.save_jobs(self._jobs)
            return True
        return False

    def list_jobs(self) -> list[AutomationJob]:
        return [j for j in self._jobs if j.id != HEARTBEAT_JOB_ID]

    def update_job(self, job_id: str, **updates: Any) -> AutomationJob | None:
        for job in self._jobs:
            if job.id == job_id:
                for key, value in updates.items():
                    if hasattr(job, key):
                        setattr(job, key, value)
                now = datetime.now(timezone.utc)
                job.next_run_at = _compute_next_run(job, now)
                self._storage.save_jobs(self._jobs)
                return job
        return None
