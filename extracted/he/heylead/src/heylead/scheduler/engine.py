"""Scheduler engine — asyncio-based background loop for autonomous outreach.

Runs alongside the MCP server via FastMCP's lifespan hook.
Ticks every 60 seconds, checking for ready work and executing it.

Key responsibilities:
1. Execute ready jobs from the DB-backed job queue
2. Schedule new work (invites, follow-ups) for autopilot campaigns
3. Periodically check for replies (every 5 min)
4. Periodically schedule follow warm-ups (every 15 min)
5. Periodically schedule engagement warm-ups (every 30 min)
6. Retry failed jobs (up to 3 attempts)
7. Cleanup old completed jobs (7 days)
"""

from __future__ import annotations

import asyncio
import logging
import time
import traceback as _tb
from typing import Any

from ..config import is_scheduler_always_on, is_scheduler_enabled, load_config, set_scheduler_enabled
from ..constants import (
    BRAND_ENGAGE_CHECK_SECONDS,
    BRAND_LIFECYCLE_CHECK_SECONDS,
    BRAND_POST_CHECK_SECONDS,
    INBOUND_CHECK_SECONDS,
    INBOUND_PIPELINE_SECONDS,
    INBOUND_QUALIFY_SECONDS,
    POST_COMMENT_CHECK_SECONDS,
    SIGNAL_KEYWORD_POLL_SECONDS,
    SIGNAL_PROSPECT_SCAN_SECONDS,
    SIGNAL_CLASSIFY_SECONDS,
    SIGNAL_PROFILE_VIEW_SECONDS,
    SIGNAL_JOB_CHANGE_SCAN_SECONDS,
    SIGNAL_COMPETITOR_POLL_SECONDS,
    SIGNAL_ACTIVATE_SECONDS,
    SIGNAL_COMPOUND_DETECT_SECONDS,
    SIGNAL_DECAY_CYCLE_SECONDS,
    SIGNAL_REMATCH_SECONDS,
    SIGNAL_BACKFILL_SECONDS,
    SIGNAL_HIRING_SCAN_SECONDS,
    SIGNAL_NEWS_SCAN_SECONDS,
    SIGNAL_COMPANY_PAGE_POLL_SECONDS,
    SIGNAL_COMPANY_FOLLOWER_POLL_SECONDS,
    SIGNAL_COMMENT_MINING_SECONDS,
    POST_INTENT_CLASSIFY_SECONDS,
    JOB_ACCEPT_INBOUND,
    JOB_ACTIVATE_SIGNALS,
    JOB_CHECK_POST_COMMENTS,
    JOB_CHECK_REPLIES,
    JOB_CLASSIFY_POST_INTENT,
    JOB_CLASSIFY_SIGNALS,
    JOB_COMPLETED,
    JOB_ENGAGE,
    JOB_ENDORSE,
    JOB_FAILED,
    JOB_FOLLOW,
    JOB_FOLLOWUP,
    JOB_INVITE,
    JOB_MINE_COMMENTS,
    JOB_PROCESS_INBOUND,
    JOB_PROFILE_VIEW,
    JOB_DAILY_DIGEST,
    JOB_DAILY_STRATEGY,
    JOB_EXECUTE_STRATEGY_PLANS,
    JOB_PARTNER_REMINDER,
    JOB_COLLECT_COMPANY_FOLLOWERS,
    JOB_COLLECT_COMPANY_PAGE,
    JOB_QUALIFY_INBOUND,
    JOB_CAMPAIGN_REFILL,
    JOB_SYNC_CONNECTIONS,
    JOB_WITHDRAW_INVITE,
    SCHEDULER_CLEANUP_DAYS,
    SCHEDULER_DAILY_STRATEGY_SECONDS,
    SCHEDULER_DAILY_DIGEST_SECONDS,
    SCHEDULER_EXECUTE_PLANS_SECONDS,
    SCHEDULER_ENDORSE_SECONDS,
    SCHEDULER_ENGAGEMENT_SECONDS,
    SCHEDULER_FOLLOW_SECONDS,
    SCHEDULER_PROFILE_VIEW_WARMUP_SECONDS,
    SCHEDULER_MAX_RETRIES,
    SCHEDULER_AUTO_REPLY_SECONDS,
    SCHEDULER_AUTO_RESUME_CHECK_SECONDS,
    SCHEDULER_REPLY_CHECK_SECONDS,
    SCHEDULER_RETRY_DELAY,
    SCHEDULER_AB_EVAL_SECONDS,
    SCHEDULER_EXPERIMENT_SECONDS,
    SCHEDULER_PARTNER_REMINDER_SECONDS,
    SCHEDULER_STRATEGY_SECONDS,
    SCHEDULER_BACKFILL_PROFILES_SECONDS,
    SCHEDULER_CAMPAIGN_REFILL_SECONDS,
    SCHEDULER_TICK_SECONDS,
    ANOMALY_SCAN_SECONDS,
    STATUS_ACTIVE,
    STATUS_COMPLETED,
    WITHDRAW_CHECK_SECONDS,
    # Distributed post intelligence
    DISTRIBUTED_SCAN_SECONDS,
    VIRAL_DETECTION_SECONDS,
    WATCHLIST_TUNE_SECONDS,
    JOB_COLLECT_POSTS_DISTRIBUTED,
    JOB_RESEARCH_CONTACTS,
    JOB_BACKFILL_POST_ANALYSIS,
    JOB_DETECT_VIRAL_POSTS,
    JOB_TUNE_WATCHLISTS,
    JOB_OPTIMIZE_SIGNALS,
    SIGNAL_OPTIMIZE_SECONDS,
)
from ..correlation import new_correlation_id, clear_correlation_id, get_correlation_id
from ..tracing import tracer
from ..db.async_bridge import run_db
from ..db.queries import (
    claim_job,
    cleanup_old_jobs,
    cleanup_scheduler_events,
    complete_job,
    count_stale_ready_jobs,
    get_ready_jobs,
    get_setting,
    list_campaigns,
    log_scheduler_event,
    restagger_stale_jobs,
    retry_job,
    save_setting,
)

logger = logging.getLogger(__name__)

# Inbound job types run even when the outbound scheduler is toggled off.
# Job types that run even when the outbound scheduler is toggled off.
# Signal intelligence is passive analysis, not outbound action.
_INBOUND_JOB_TYPES = frozenset({
    JOB_ACCEPT_INBOUND,       # DEPRECATED: kept for in-flight jobs
    JOB_QUALIFY_INBOUND,      # DEPRECATED: kept for in-flight jobs
    JOB_PROCESS_INBOUND,      # Unified classify-first pipeline
    JOB_CHECK_POST_COMMENTS,
    JOB_CLASSIFY_POST_INTENT,
    JOB_CLASSIFY_SIGNALS,
    JOB_ACTIVATE_SIGNALS,
    JOB_COLLECT_COMPANY_PAGE,
    JOB_COLLECT_COMPANY_FOLLOWERS,
    JOB_MINE_COMMENTS,
    JOB_CAMPAIGN_REFILL,
    JOB_PARTNER_REMINDER,
    JOB_DAILY_DIGEST,
    JOB_SYNC_CONNECTIONS,
})


class SchedulerEngine:
    """Asyncio-based scheduler for autonomous outreach execution.

    Runs as a background task in the same event loop as the MCP server.
    All outreach logic is delegated to executors (which reuse existing tool internals).
    """

    # Setting key for persisting timers to SQLite
    _TIMERS_SETTING_KEY = "scheduler_timers"
    # Deprecated timer names to clean up on startup
    _DEPRECATED_TIMERS = {"inbound_check", "qualify_inbound"}

    def __init__(self) -> None:
        self._running = False
        self._task: asyncio.Task[None] | None = None
        # All periodic timers stored in a dict, persisted to SQLite.
        # Loaded on start() to survive MCP server restarts.
        self._timers: dict[str, float] = {}
        self._tick_count: int = 0
        self._errors_in_row: int = 0
        self._started_at: float = 0
        self._reported_stuck_jobs: set[str] = set()  # dedup watchdog events

    def _timer(self, name: str) -> float:
        """Get a timer value (last execution timestamp). Returns 0 if never run."""
        return self._timers.get(name, 0)

    def _set_timer(self, name: str, value: float) -> None:
        """Set a timer value. Persisted to SQLite every 5 ticks."""
        self._timers[name] = value

    async def _send_scheduler_disable_alert(self, toggle_info: dict) -> None:
        """Send immediate email alert when scheduler was disabled while always-on is active."""
        try:
            from ..config import is_backend_mode
            if not is_backend_mode():
                logger.debug("No backend configured, skipping scheduler disable alert")
                return

            import httpx
            from ..services.cloud_sync import _base_url, _headers

            base = _base_url()
            payload = {
                "alert_type": "scheduler_disabled",
                "disabled_by": toggle_info.get("caller", "unknown"),
                "reason": toggle_info.get("reason", ""),
                "disabled_at": toggle_info.get("timestamp", 0),
                "auto_reenabled": True,
            }

            async with httpx.AsyncClient(timeout=15.0) as http:
                resp = await http.post(
                    f"{base}/api/v1/alerts/scheduler-disabled",
                    json=payload,
                    headers=_headers(),
                )
                if resp.status_code == 200:
                    logger.info("Scheduler disable alert sent to backend")
                else:
                    logger.warning(
                        "Scheduler disable alert failed: HTTP %d — %s",
                        resp.status_code, resp.text[:100],
                    )
        except Exception as e:
            logger.warning("Failed to send scheduler disable alert: %s", e)

    @property
    def is_running(self) -> bool:
        return self._running

    @property
    def tick_count(self) -> int:
        return self._tick_count

    async def start(self) -> None:
        """Start the scheduler background loop.

        Loads persisted timer state from SQLite so periodic tasks resume
        where they left off instead of all firing immediately on restart.
        """
        if self._running:
            logger.warning("Scheduler already running")
            return
        # Load persisted timers from DB (survives restarts)
        try:
            saved = await run_db(get_setting, self._TIMERS_SETTING_KEY, {})
            if isinstance(saved, dict):
                self._timers = saved
                logger.info(
                    "Loaded %d persisted scheduler timers", len(self._timers),
                )
                # Clean up deprecated timer keys
                removed = [k for k in self._DEPRECATED_TIMERS if k in self._timers]
                if removed:
                    for k in removed:
                        del self._timers[k]
                    await run_db(save_setting, self._TIMERS_SETTING_KEY, self._timers)
                    logger.info("Cleaned up deprecated timers: %s", removed)
        except Exception as e:
            logger.debug("Failed to load persisted timers: %s", e)

        # Recover jobs stuck in 'running' from a previous crashed session
        try:
            from ..db.queries import recover_stuck_running_jobs, recover_stuck_sending_outreaches
            recovered = await run_db(recover_stuck_running_jobs, 360)
            if recovered > 0:
                logger.warning("Startup: recovered %d stuck running jobs", recovered)
            recovered_out = await run_db(recover_stuck_sending_outreaches, 360)
            if recovered_out > 0:
                logger.warning("Startup: recovered %d stuck sending outreaches", recovered_out)
        except Exception as e:
            logger.debug("Startup stuck-job recovery failed: %s", e)

        # Purge old completed/failed jobs on startup (don't wait for hourly cleanup)
        try:
            from ..db.queries import cleanup_old_jobs
            deleted = await run_db(cleanup_old_jobs, days=SCHEDULER_CLEANUP_DAYS)
            if deleted > 0:
                logger.info("Startup: purged %d old completed/failed jobs", deleted)
        except Exception as e:
            logger.debug("Startup cleanup failed: %s", e)

        self._running = True
        self._started_at = time.time()
        self._task = asyncio.create_task(self._run_loop())
        logger.info("Scheduler engine started")

        # Non-blocking: verify cloud fallback is active
        asyncio.create_task(self._check_cloud_on_startup())

    async def stop(self) -> None:
        """Gracefully stop the scheduler."""
        uptime = time.time() - self._started_at if self._started_at else 0
        logger.warning(
            "Scheduler engine stopping — uptime=%.0fs, ticks=%d, reason=process_shutdown",
            uptime, self._tick_count,
        )
        self._running = False
        if self._task and not self._task.done():
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        self._task = None

        # Check if cloud scheduler is picking up the slack
        await self._verify_cloud_fallback(uptime)

        logger.warning("Scheduler engine stopped")

    async def _verify_cloud_fallback(self, uptime: float) -> None:
        """Check if backend Cloud Scheduler is active. Alert if not."""
        try:
            from .. import config
            if not config.is_backend_mode():
                logger.warning("No backend configured — no cloud fallback available")
                return

            import httpx
            from ..services.cloud_sync import _base_url, _headers

            async with httpx.AsyncClient(timeout=10) as client:
                resp = await client.get(
                    f"{_base_url()}/api/v1/scheduler/health",
                    headers=_headers(),
                )

            if resp.status_code == 200:
                data = resp.json()
                if data.get("status") == "healthy":
                    logger.info(
                        "Cloud scheduler is healthy (last tick %ds ago) — fallback active",
                        data.get("age_seconds", 0),
                    )
                    return
                else:
                    logger.error(
                        "CRITICAL: Cloud scheduler is STALE (last tick %ds ago). "
                        "Both schedulers are down!",
                        data.get("age_seconds", 0),
                    )
            else:
                logger.error(
                    "CRITICAL: Cloud scheduler health check failed (HTTP %d). "
                    "Cannot confirm fallback.",
                    resp.status_code,
                )

            # Cloud is not healthy — trigger alert
            await self._send_both_down_alert(uptime)

        except Exception as e:
            logger.error("Failed to verify cloud fallback: %s", e)
            try:
                await self._send_both_down_alert(uptime)
            except Exception:
                pass

    async def _send_both_down_alert(self, uptime: float) -> None:
        """Tell backend to send a 'both schedulers down' alert email."""
        try:
            from .. import config
            if not config.is_backend_mode():
                return

            import httpx
            from ..services.cloud_sync import _base_url, _headers

            async with httpx.AsyncClient(timeout=10) as client:
                await client.post(
                    f"{_base_url()}/api/v1/scheduler/alert-down",
                    headers=_headers(),
                    json={"local_uptime_seconds": uptime, "local_ticks": self._tick_count},
                )
            logger.info("Both-schedulers-down alert sent via backend")
        except Exception as e:
            logger.warning("Failed to send both-down alert: %s", e)

    async def _outreach_health_watchdog(self, now: float) -> None:
        """Detect stuck jobs and outreach stalls, recover and alert via email.

        Runs every 5 min. Two checks:
        1. Stuck jobs: running for >6 min → recover + alert
        2. Outreach stall: pending outreaches exist but no DM/invite completed
           in last 30 min → alert
        """
        try:
            from ..db.queries import recover_stuck_running_jobs, recover_stuck_sending_outreaches

            # ── Check 1: Stuck jobs ──
            # Use 600s (10 min) threshold — some jobs legitimately take 5+ min
            _STUCK_THRESHOLD = 600

            def _query_stuck(threshold: int) -> list:
                from ..db.schema import get_db
                _db = get_db()
                rows = _db.execute(
                    """SELECT id, job_type, campaign_id, started_at
                       FROM scheduler_jobs
                       WHERE status = 'running' AND started_at < ?""",
                    (int(now) - threshold,),
                ).fetchall()
                _db.close()
                return rows

            stuck_rows = await run_db(_query_stuck, _STUCK_THRESHOLD)

            if stuck_rows:
                recovered = await run_db(recover_stuck_running_jobs, _STUCK_THRESHOLD)
                recovered_out = await run_db(recover_stuck_sending_outreaches, _STUCK_THRESHOLD)
                total_recovered = recovered + recovered_out
                logger.warning(
                    "Watchdog: %d stuck jobs detected, recovered %d jobs + %d outreaches",
                    len(stuck_rows), recovered, recovered_out,
                )

                # Only log event for NEW stuck jobs (dedup across watchdog cycles)
                stuck_ids = {r["id"] for r in stuck_rows}
                new_stuck = stuck_ids - self._reported_stuck_jobs
                self._reported_stuck_jobs = stuck_ids  # update for next cycle

                # Send alert (debounced — max 1 per cooldown period)
                from ..constants import STALL_ALERT_COOLDOWN_SECONDS
                last_stuck_alert = self._timer("last_stuck_alert")
                if now - last_stuck_alert >= STALL_ALERT_COOLDOWN_SECONDS:
                    await self._send_outreach_stall_alert({
                        "stall_type": "stuck_jobs",
                        "minutes_since_last_action": (now - min(r["started_at"] for r in stuck_rows)) / 60,
                        "stuck_jobs": len(stuck_rows),
                        "recovered_jobs": total_recovered,
                        "pending_outreaches": 0,
                        "campaigns": [
                            {"name": r["job_type"], "pending": 1}
                            for r in stuck_rows[:5]
                        ],
                    })
                    self._set_timer("last_stuck_alert", now)

                if new_stuck:
                    await run_db(
                        log_scheduler_event, "watchdog_stuck_jobs",
                        context={
                            "stuck_count": len(stuck_rows),
                            "new_stuck": len(new_stuck),
                            "recovered": total_recovered,
                            "job_types": [r["job_type"] for r in stuck_rows],
                        },
                    )
            else:
                # Clear reported set when no stuck jobs
                self._reported_stuck_jobs.clear()

            # ── Check 2: Outreach stall ──
            # If there are pending outreaches but no DM/invite completed in 30 min
            def _query_stall_info() -> tuple:
                from ..db.schema import get_db
                _db = get_db()
                _pending = _db.execute(
                    """SELECT count(*) FROM outreaches
                       WHERE status IN ('pending', 'connected')
                       AND campaign_id IN (SELECT id FROM campaigns WHERE status = 'active')"""
                ).fetchone()[0]
                _last = None
                _camps = []
                if _pending > 0:
                    _last = _db.execute(
                        """SELECT max(completed_at) FROM scheduler_jobs
                           WHERE job_type IN ('send_dm', 'invite', 'followup')
                           AND status = 'completed'"""
                    ).fetchone()[0]
                    _camps = _db.execute(
                        """SELECT c.name,
                                  (SELECT count(*) FROM outreaches o
                                   WHERE o.campaign_id = c.id
                                   AND o.status IN ('pending', 'connected')) as pending
                           FROM campaigns c
                           WHERE c.status = 'active'"""
                    ).fetchall()
                _db.close()
                return _pending, _last, _camps

            pending_count, last_action, campaign_info = await run_db(_query_stall_info)

            if pending_count > 0:
                minutes_since_action = (now - last_action) / 60 if last_action else 999

                if minutes_since_action >= 30:
                    logger.warning(
                        "Watchdog: outreach stall — %d pending, last action %.0f min ago",
                        pending_count, minutes_since_action,
                    )

                    # Only alert once per stall (use timer to debounce)
                    from ..constants import STALL_ALERT_COOLDOWN_SECONDS
                    last_stall_alert = self._timer("last_stall_alert")
                    if now - last_stall_alert >= STALL_ALERT_COOLDOWN_SECONDS:
                        await self._send_outreach_stall_alert({
                            "stall_type": "outreach_stall",
                            "minutes_since_last_action": minutes_since_action,
                            "stuck_jobs": 0,
                            "pending_outreaches": pending_count,
                            "recovered_jobs": 0,
                            "campaigns": [
                                {"name": r["name"], "pending": r["pending"]}
                                for r in campaign_info[:5]
                            ],
                        })
                        self._set_timer("last_stall_alert", now)

                    await run_db(
                        log_scheduler_event, "watchdog_outreach_stall",
                        context={
                            "pending_outreaches": pending_count,
                            "minutes_since_action": round(minutes_since_action, 1),
                        },
                    )
        except Exception as e:
            logger.warning("Outreach health watchdog failed: %s", e)

    async def _send_outreach_stall_alert(self, details: dict) -> None:
        """Send outreach stall/stuck alert to backend for email delivery."""
        try:
            from ..config import is_backend_mode
            if not is_backend_mode():
                logger.debug("No backend configured, skipping outreach stall alert")
                return

            import httpx
            from ..services.cloud_sync import _base_url, _headers

            async with httpx.AsyncClient(timeout=15.0) as http:
                resp = await http.post(
                    f"{_base_url()}/api/v1/alerts/outreach-stall",
                    json=details,
                    headers=_headers(),
                )
                if resp.status_code == 200:
                    logger.info("Outreach stall alert sent to backend (type: %s)", details.get("stall_type"))
                else:
                    logger.warning(
                        "Outreach stall alert failed: HTTP %d — %s",
                        resp.status_code, resp.text[:100],
                    )
        except Exception as e:
            logger.warning("Failed to send outreach stall alert: %s", e)

    async def _check_cloud_on_startup(self) -> None:
        """Verify cloud scheduler fallback is active on startup (non-blocking)."""
        await asyncio.sleep(10)  # Let MCP server finish initializing
        try:
            from .. import config
            if not config.is_backend_mode():
                logger.info("No backend mode — cloud fallback not available")
                return

            import httpx
            from ..services.cloud_sync import _base_url, _headers

            async with httpx.AsyncClient(timeout=10) as client:
                resp = await client.get(
                    f"{_base_url()}/api/v1/scheduler/health",
                    headers=_headers(),
                )
            if resp.status_code == 200:
                data = resp.json()
                if data.get("status") == "healthy":
                    logger.info(
                        "Cloud scheduler fallback verified (last tick %ds ago)",
                        data.get("age_seconds", 0),
                    )
                else:
                    logger.warning(
                        "Cloud scheduler fallback is STALE — ticks not arriving. "
                        "Check GCP Cloud Scheduler."
                    )
            else:
                logger.warning(
                    "Cloud scheduler health check returned HTTP %d — fallback may not be active",
                    resp.status_code,
                )
        except Exception as e:
            logger.debug("Cloud startup check failed (non-fatal): %s", e)

    async def _run_loop(self) -> None:
        """Main tick loop — runs every SCHEDULER_TICK_SECONDS."""
        # Small initial delay to let the MCP server finish startup
        await asyncio.sleep(5)

        while self._running:
            try:
                await asyncio.wait_for(self._tick(), timeout=55)
                self._errors_in_row = 0
            except asyncio.TimeoutError:
                logger.error("Scheduler tick timed out after 55s — skipping")
                self._errors_in_row += 1
            except asyncio.CancelledError:
                logger.warning("Scheduler run loop cancelled after %d ticks", self._tick_count)
                break
            except Exception as e:
                self._errors_in_row += 1
                logger.error("Scheduler tick error (%d in a row): %s", self._errors_in_row, e)
                # Back off if too many consecutive errors
                if self._errors_in_row >= 5:
                    logger.warning("Too many scheduler errors, backing off for 5 minutes")
                    await asyncio.sleep(300)
                    self._errors_in_row = 0

            await asyncio.sleep(SCHEDULER_TICK_SECONDS)

        # Loop exited normally (not via CancelledError)
        if not self._running:
            logger.warning("Scheduler run loop exited — _running=False after %d ticks", self._tick_count)

    async def _tick(self) -> None:
        """Single scheduler tick — the heart of the autonomous system."""
        self._tick_count += 1

        # Guard: setup must be complete for ANY processing
        if not await run_db(get_setting, "setup_complete", False):
            return

        now = time.time()
        scheduler_on = is_scheduler_enabled()
        tick_processed = 0
        tick_failed = 0
        tick_planned = 0

        # ── ALWAYS-ON GUARD: auto-re-enable if always_on mode is active ──
        if not scheduler_on and is_scheduler_always_on():
            cfg = load_config()
            last_toggle = cfg.get("_last_scheduler_toggle", {})

            set_scheduler_enabled(
                True,
                caller="always_on_guard",
                reason=(
                    f"Auto-re-enabled by always-on guard. "
                    f"Was disabled by '{last_toggle.get('caller', 'unknown')}': "
                    f"{last_toggle.get('reason', 'no reason given')}"
                ),
            )
            scheduler_on = True

            logger.warning(
                "Scheduler was disabled but always_on is active — auto-re-enabled. "
                "Disabled by: %s, reason: %s",
                last_toggle.get("caller", "unknown"),
                last_toggle.get("reason", "unknown"),
            )

            await self._send_scheduler_disable_alert(last_toggle)

            await run_db(
                log_scheduler_event, "scheduler_always_on_reenable",
                context={
                    "disabled_by": last_toggle.get("caller", "unknown"),
                    "disable_reason": last_toggle.get("reason", ""),
                    "disabled_at": last_toggle.get("timestamp", 0),
                    "reenabled_at": int(now),
                },
            )

        # ── ALWAYS-ON: execute ready jobs from the DB queue ──
        # Inbound jobs run regardless of scheduler_enabled.
        # Outbound jobs are skipped when the scheduler is off.
        processed, failed = await self._process_ready_jobs(
            scheduler_on=scheduler_on,
        )
        tick_processed += processed
        tick_failed += failed

        # ── ALWAYS-ON: inbound pipeline (independent of scheduler toggle) ──

        # Unified classify-first inbound pipeline (every 15 min)
        if now - self._timer("inbound_pipeline") >= INBOUND_PIPELINE_SECONDS:
            await self._schedule_process_inbound()
            self._set_timer("inbound_pipeline", now)

        # Check post comments for inbound leads (every 30 min)
        if now - self._timer("post_comment_check") >= POST_COMMENT_CHECK_SECONDS:
            await self._schedule_check_post_comments()
            self._set_timer("post_comment_check", now)

        # ── ALWAYS-ON: signal intelligence pipeline ──
        # Classification and activation are passive analysis, not outbound action.
        # They must run regardless of scheduler toggle so signals don't get stuck.

        # Classify pending signals (every 15 min)
        if now - self._timer("signal_classify") >= SIGNAL_CLASSIFY_SECONDS:
            await self._schedule_signal_classification()
            self._set_timer("signal_classify", now)

        # Activate classified signals (every 15 min)
        if now - self._timer("signal_activate") >= SIGNAL_ACTIVATE_SECONDS:
            await self._schedule_signal_activation()
            self._set_timer("signal_activate", now)

        # Re-match homeless signals to campaigns (every 1 hour)
        if now - self._timer("signal_rematch") >= SIGNAL_REMATCH_SECONDS:
            await self._schedule_signal_rematch()
            self._set_timer("signal_rematch", now)

        # Backfill orphan signals to known contacts (every 2 hours)
        if now - self._timer("orphan_backfill") >= SIGNAL_BACKFILL_SECONDS:
            await self._schedule_orphan_backfill()
            self._set_timer("orphan_backfill", now)

        # Classify post intents for granular buyer signals (every 30 min)
        if now - self._timer("post_intent_classify") >= POST_INTENT_CLASSIFY_SECONDS:
            await self._schedule_post_intent_classification()
            self._set_timer("post_intent_classify", now)

        # Mine competitor/industry post comments for leads (every 2 hours)
        if now - self._timer("comment_mining") >= SIGNAL_COMMENT_MINING_SECONDS:
            await self._schedule_comment_mining()
            self._set_timer("comment_mining", now)

        # Auto-refill campaigns running low on prospects (every 1 hour)
        if now - self._timer("campaign_refill") >= SCHEDULER_CAMPAIGN_REFILL_SECONDS:
            await self._schedule_campaign_refill()
            self._set_timer("campaign_refill", now)

        # Backfill empty profiles (every 2 hours)
        if now - self._timer("backfill_profiles") >= SCHEDULER_BACKFILL_PROFILES_SECONDS:
            await self._schedule_backfill_profiles()
            self._set_timer("backfill_profiles", now)

        # ── OUTBOUND: requires scheduler to be enabled ──
        if not scheduler_on:
            logger.info(
                "tick#%d: processed=%d failed=%d planned=%d scheduler=off",
                self._tick_count, tick_processed, tick_failed, tick_planned,
            )
            return

        # Schedule new work for all active autopilot campaigns
        await self._schedule_new_work()

        # Periodic: auto-resume limit-paused campaigns (every 5 min)
        if now - self._timer("auto_resume_check") >= SCHEDULER_AUTO_RESUME_CHECK_SECONDS:
            await self._check_auto_resume()
            self._set_timer("auto_resume_check", now)

        # Periodic: check replies (every 5 min)
        if now - self._timer("reply_check") >= SCHEDULER_REPLY_CHECK_SECONDS:
            await self._schedule_reply_checks()
            self._set_timer("reply_check", now)

        # Periodic: auto-reply to detected messages (every 5 min)
        if now - self._timer("auto_reply_plan") >= SCHEDULER_AUTO_REPLY_SECONDS:
            await self._schedule_auto_replies()
            self._set_timer("auto_reply_plan", now)

        # Periodic: profile view warm-ups (every 10 min — lightest touch)
        if now - self._timer("profile_view_plan") >= SCHEDULER_PROFILE_VIEW_WARMUP_SECONDS:
            await self._schedule_profile_views()
            self._set_timer("profile_view_plan", now)

        # Periodic: follow warm-ups (every 15 min)
        if now - self._timer("follow_plan") >= SCHEDULER_FOLLOW_SECONDS:
            await self._schedule_follows()
            self._set_timer("follow_plan", now)

        # Periodic: engagement warm-ups (every 30 min)
        if now - self._timer("engagement_plan") >= SCHEDULER_ENGAGEMENT_SECONDS:
            await self._schedule_engagements()
            self._set_timer("engagement_plan", now)

        # 6d. Periodic: collect keyword signals (every 30 min)
        if now - self._timer("keyword_signal_collect") >= SIGNAL_KEYWORD_POLL_SECONDS:
            await self._schedule_keyword_signal_collection()
            self._set_timer("keyword_signal_collect", now)

        # 6e. Periodic: scan prospect posts for signals (every 1 hour)
        if now - self._timer("prospect_post_scan") >= SIGNAL_PROSPECT_SCAN_SECONDS:
            await self._schedule_prospect_post_scan()
            self._set_timer("prospect_post_scan", now)

        # 6g. Periodic: collect profile views (every 1 hour)
        if now - self._timer("profile_view_collect") >= SIGNAL_PROFILE_VIEW_SECONDS:
            await self._schedule_profile_view_collection()
            self._set_timer("profile_view_collect", now)

        # 6h. Periodic: detect job changes (every 4 hours)
        if now - self._timer("job_change_scan") >= SIGNAL_JOB_CHANGE_SCAN_SECONDS:
            await self._schedule_job_change_detection()
            self._set_timer("job_change_scan", now)

        # 6i. Periodic: collect competitor mentions (every 30 min)
        if now - self._timer("competitor_signal_collect") >= SIGNAL_COMPETITOR_POLL_SECONDS:
            await self._schedule_competitor_signal_collection()
            self._set_timer("competitor_signal_collect", now)

        # 6k. Periodic: detect hiring surges (every 4 hours)
        if now - self._timer("hiring_signal_collect") >= SIGNAL_HIRING_SCAN_SECONDS:
            await self._schedule_hiring_signal_collection()
            self._set_timer("hiring_signal_collect", now)

        # 6l. Periodic: collect news/funding signals (every 4 hours)
        if now - self._timer("news_signal_collect") >= SIGNAL_NEWS_SCAN_SECONDS:
            await self._schedule_news_signal_collection()
            self._set_timer("news_signal_collect", now)

        # 6l-2. Periodic: collect company page engagement signals (Phase 2)
        if now - self._timer("company_page_collect") >= SIGNAL_COMPANY_PAGE_POLL_SECONDS:
            await self._schedule_company_page_collection()
            self._set_timer("company_page_collect", now)

        # 6l-3. Periodic: collect company follower signals (Phase 2)
        if now - self._timer("company_follower_collect") >= SIGNAL_COMPANY_FOLLOWER_POLL_SECONDS:
            await self._schedule_company_follower_collection()
            self._set_timer("company_follower_collect", now)

        # 6m. Periodic: detect compound intent events (every 30 min)
        if now - self._timer("compound_intent_detect") >= SIGNAL_COMPOUND_DETECT_SECONDS:
            await self._schedule_compound_intent_detection()
            self._set_timer("compound_intent_detect", now)

        # 6n. Periodic: signal decay cycle (every 6 hours)
        if now - self._timer("decay_cycle") >= SIGNAL_DECAY_CYCLE_SECONDS:
            await self._schedule_decay_cycle()
            self._set_timer("decay_cycle", now)

        # 7. Periodic: skill endorsement warm-ups (every 15 min)
        if now - self._timer("endorse_plan") >= SCHEDULER_ENDORSE_SECONDS:
            await self._schedule_endorsements()
            self._set_timer("endorse_plan", now)

        # 8. Periodic: stale invite withdrawal (every hour)
        if now - self._timer("withdraw_check") >= WITHDRAW_CHECK_SECONDS:
            await self._schedule_stale_withdrawals()
            self._set_timer("withdraw_check", now)

        # 9a. Brand lifecycle (every hour)
        if now - self._timer("brand_lifecycle_check") >= BRAND_LIFECYCLE_CHECK_SECONDS:
            await self._schedule_brand_lifecycle()
            self._set_timer("brand_lifecycle_check", now)

        # 9b. Brand posts (every hour — planner decides if one is due)
        if now - self._timer("brand_post_plan") >= BRAND_POST_CHECK_SECONDS:
            await self._schedule_brand_posts()
            self._set_timer("brand_post_plan", now)

        # 9c. Brand engagement (every 4 hours)
        if now - self._timer("brand_engage_plan") >= BRAND_ENGAGE_CHECK_SECONDS:
            await self._schedule_brand_engagements()
            self._set_timer("brand_engage_plan", now)

        # 10. Cleanup old completed jobs (once per hour)
        if now - self._timer("cleanup") >= 3600:
            try:
                deleted = await run_db(cleanup_old_jobs, days=SCHEDULER_CLEANUP_DAYS)
                if deleted > 0:
                    logger.debug("Cleaned up %d old scheduler jobs", deleted)
            except Exception as e:
                logger.debug("Cleanup failed: %s", e)

            # Auto-cleanup failed engage & invite jobs
            try:
                from ..db.queries import (
                    cleanup_failed_engage_jobs,
                    cleanup_failed_invite_jobs,
                )
                engage_result = await run_db(cleanup_failed_engage_jobs)
                invite_result = await run_db(cleanup_failed_invite_jobs)
                if engage_result["cleaned"] or invite_result["cleaned"]:
                    logger.info(
                        "Auto-cleanup: %d engage + %d invite failed jobs",
                        engage_result["cleaned"], invite_result["cleaned"],
                    )
            except Exception as e:
                logger.debug("Failed job cleanup failed: %s", e)

            # Recover jobs stuck in 'running' state (process crash recovery)
            try:
                from ..db.queries import recover_stuck_running_jobs
                recovered = await run_db(recover_stuck_running_jobs, 360)
                if recovered > 0:
                    logger.warning("Recovered %d stuck running jobs", recovered)
            except Exception as e:
                logger.debug("Stuck job recovery failed: %s", e)

            # Recover outreaches stuck in 'sending'/'sending_followup' state
            try:
                from ..db.queries import recover_stuck_sending_outreaches
                recovered_outreaches = await run_db(recover_stuck_sending_outreaches, 360)
                if recovered_outreaches > 0:
                    logger.warning("Recovered %d stuck sending outreaches", recovered_outreaches)
            except Exception as e:
                logger.debug("Stuck outreach recovery failed: %s", e)

            self._set_timer("cleanup", now)

        # 11. Periodic: A/B test evaluation (every hour)
        if now - self._timer("ab_eval") >= SCHEDULER_AB_EVAL_SECONDS:
            try:
                from ..services.experiment_service import evaluate_ab_tests
                results = await run_db(evaluate_ab_tests)
                for r in results:
                    logger.info("A/B test result: %s", r)
            except Exception as e:
                logger.debug("A/B test evaluation failed: %s", e)
            self._set_timer("ab_eval", now)

        # 12. Periodic: experiment analysis (every 6 hours)
        if now - self._timer("experiment") >= SCHEDULER_EXPERIMENT_SECONDS:
            try:
                from ..services.experiment_service import run_experiment_analysis
                result = await run_experiment_analysis()
                if result:
                    logger.info("Experiment analysis completed: %s", result.get("health_check", "")[:100])
            except Exception as e:
                logger.debug("Experiment analysis failed: %s", e)
            self._set_timer("experiment", now)

        # 13. Periodic: strategy engine cycle (every 4 hours)
        if now - self._timer("strategy_cycle") >= SCHEDULER_STRATEGY_SECONDS:
            try:
                from ..services.strategy_engine import run_strategy_cycle
                result = await run_strategy_cycle()
                if result:
                    logger.info(
                        "Strategy cycle: %d patterns, %d optimizations, %d spawned",
                        result.get("patterns_detected", 0),
                        result.get("optimizations", 0),
                        result.get("campaigns_spawned", 0),
                    )
            except Exception as e:
                logger.debug("Strategy cycle failed: %s", e)
            self._set_timer("strategy_cycle", now)

        # 13b. Periodic: communication strategist — daily planning (once per day)
        if now - self._timer("daily_strategy") >= SCHEDULER_DAILY_STRATEGY_SECONDS:
            try:
                from ..db.queries import create_scheduler_job, get_pending_job_count
                pending = await run_db(get_pending_job_count, None, JOB_DAILY_STRATEGY)
                if pending == 0:
                    await run_db(
                        create_scheduler_job, None, JOB_DAILY_STRATEGY, now
                    )
                    tick_planned += 1
                    logger.info("Scheduled daily strategy planning")
            except Exception as e:
                logger.debug("Daily strategy scheduling failed: %s", e)
            self._set_timer("daily_strategy", now)

        # 13c. Periodic: execute strategy plans (every 15 min)
        if now - self._timer("execute_strategy_plans") >= SCHEDULER_EXECUTE_PLANS_SECONDS:
            try:
                campaigns = await run_db(list_campaigns, status=STATUS_ACTIVE)
                for campaign in campaigns:
                    if campaign.get("mode") != "autopilot":
                        continue
                    campaign_id = campaign["id"]
                    from ..db.queries import create_scheduler_job, get_pending_job_count
                    pending = await run_db(
                        get_pending_job_count, campaign_id, JOB_EXECUTE_STRATEGY_PLANS
                    )
                    if pending == 0:
                        await run_db(
                            create_scheduler_job,
                            campaign_id,
                            JOB_EXECUTE_STRATEGY_PLANS,
                            now,
                        )
                        tick_planned += 1
            except Exception as e:
                logger.debug("Strategy plans execution scheduling failed: %s", e)
            self._set_timer("execute_strategy_plans", now)

        # 14. Periodic: partner follow-up reminders (every hour)
        if now - self._timer("partner_reminder") >= SCHEDULER_PARTNER_REMINDER_SECONDS:
            try:
                from ..db.queries import create_scheduler_job
                await run_db(create_scheduler_job, None, None, JOB_PARTNER_REMINDER)
            except Exception as e:
                logger.debug("Partner reminder scheduling failed: %s", e)
            self._set_timer("partner_reminder", now)

        # 15. Periodic: daily digest (once per day)
        if now - self._timer("daily_digest") >= SCHEDULER_DAILY_DIGEST_SECONDS:
            try:
                from ..db.queries import create_scheduler_job
                await run_db(create_scheduler_job, None, None, JOB_DAILY_DIGEST)
                tick_planned += 1
            except Exception as e:
                logger.debug("Daily digest scheduling failed: %s", e)
            self._set_timer("daily_digest", now)

        # 16a. Periodic: action verification (every 30 min)
        from ..constants import VERIFICATION_CHECK_SECONDS, JOB_VERIFY_ACTIONS
        if now - self._timer("verify_actions") >= VERIFICATION_CHECK_SECONDS:
            try:
                from ..db.queries import create_scheduler_job
                await run_db(create_scheduler_job, None, None, JOB_VERIFY_ACTIONS)
                tick_planned += 1
            except Exception as e:
                logger.debug("Verification scheduling failed: %s", e)
            self._set_timer("verify_actions", now)

        # 16. Periodic: engagement anomaly scan (every hour)
        if now - self._timer("anomaly_scan") >= ANOMALY_SCAN_SECONDS:
            try:
                from ..services.anomaly_detector import run_anomaly_scan

                anomalies = await run_anomaly_scan()
                if anomalies:
                    logger.warning(
                        "Anomaly scan found %d issues: %s",
                        len(anomalies),
                        ", ".join(a.anomaly_type for a in anomalies),
                    )
            except Exception as e:
                logger.debug("Anomaly scan failed: %s", e)
            self._set_timer("anomaly_scan", now)

        # 17. Periodic: connection sync (every 4 hours)
        from ..constants import SCHEDULER_SYNC_CONNECTIONS_SECONDS, JOB_SYNC_CONNECTIONS
        if now - self._timer("sync_connections") >= SCHEDULER_SYNC_CONNECTIONS_SECONDS:
            try:
                from ..db.queries import create_scheduler_job
                await run_db(create_scheduler_job, None, None, JOB_SYNC_CONNECTIONS)
                tick_planned += 1
            except Exception as e:
                logger.debug("Connection sync scheduling failed: %s", e)
            self._set_timer("sync_connections", now)

        # 18. Periodic: distributed post collection (every 30 min)
        if now - self._timer("distributed_post_scan") >= DISTRIBUTED_SCAN_SECONDS:
            try:
                from ..db.queries import create_scheduler_job, get_pending_job_count
                pending = await run_db(get_pending_job_count, None, JOB_COLLECT_POSTS_DISTRIBUTED)
                if pending == 0:
                    await run_db(create_scheduler_job, None, JOB_COLLECT_POSTS_DISTRIBUTED, now)
                    tick_planned += 1
            except Exception as e:
                logger.debug("Distributed post scan scheduling failed: %s", e)
            self._set_timer("distributed_post_scan", now)

        # 19. Periodic: contact research pipeline (every 15 min)
        if now - self._timer("research_contacts") >= 900:
            try:
                from ..db.queries import create_scheduler_job, get_pending_job_count
                pending = await run_db(get_pending_job_count, None, JOB_RESEARCH_CONTACTS)
                if pending == 0:
                    await run_db(create_scheduler_job, None, JOB_RESEARCH_CONTACTS, now)
                    tick_planned += 1
            except Exception as e:
                logger.debug("Contact research scheduling failed: %s", e)
            self._set_timer("research_contacts", now)

        # 20. Periodic: viral post detection (every 1 hour)
        if now - self._timer("viral_detection") >= VIRAL_DETECTION_SECONDS:
            try:
                from ..db.queries import create_scheduler_job, get_pending_job_count
                pending = await run_db(get_pending_job_count, None, JOB_DETECT_VIRAL_POSTS)
                if pending == 0:
                    await run_db(create_scheduler_job, None, JOB_DETECT_VIRAL_POSTS, now)
                    tick_planned += 1
            except Exception as e:
                logger.debug("Viral detection scheduling failed: %s", e)
            self._set_timer("viral_detection", now)

        # 21. Periodic: watchlist auto-tuning (once per day)
        if now - self._timer("watchlist_tune") >= WATCHLIST_TUNE_SECONDS:
            try:
                from ..db.queries import create_scheduler_job, get_pending_job_count
                pending = await run_db(get_pending_job_count, None, JOB_TUNE_WATCHLISTS)
                if pending == 0:
                    await run_db(create_scheduler_job, None, JOB_TUNE_WATCHLISTS, now)
                    tick_planned += 1
            except Exception as e:
                logger.debug("Watchlist tuning scheduling failed: %s", e)
            self._set_timer("watchlist_tune", now)

        # 22. Periodic: signal self-optimization (once per day)
        if now - self._timer("signal_optimize") >= SIGNAL_OPTIMIZE_SECONDS:
            try:
                from ..db.queries import create_scheduler_job, get_pending_job_count
                pending = await run_db(get_pending_job_count, None, JOB_OPTIMIZE_SIGNALS)
                if pending == 0:
                    await run_db(create_scheduler_job, None, JOB_OPTIMIZE_SIGNALS, now)
                    tick_planned += 1
            except Exception as e:
                logger.debug("Signal optimization scheduling failed: %s", e)
            self._set_timer("signal_optimize", now)

        # 23. One-shot: backfill unanalyzed posts (runs once on startup, then every 4 hours)
        if now - self._timer("backfill_analysis") >= 14400:
            try:
                from ..db.queries import create_scheduler_job, get_pending_job_count
                pending = await run_db(get_pending_job_count, None, JOB_BACKFILL_POST_ANALYSIS)
                if pending == 0:
                    await run_db(create_scheduler_job, None, JOB_BACKFILL_POST_ANALYSIS, now)
                    tick_planned += 1
            except Exception as e:
                logger.debug("Backfill analysis scheduling failed: %s", e)
            self._set_timer("backfill_analysis", now)

        # 23. Periodic: outreach health watchdog (every 5 min)
        if now - self._timer("outreach_watchdog") >= 300:
            await self._outreach_health_watchdog(now)
            self._set_timer("outreach_watchdog", now)

        # ── Flush Unipile API metrics every tick ──
        try:
            from ..linkedin.api_metrics import api_metrics
            from ..linkedin.voyager_health import voyager_health

            metrics_summary = api_metrics.summary()
            if metrics_summary:
                await run_db(
                    log_scheduler_event, "api_metrics",
                    context=metrics_summary,
                )
                api_metrics.reset()

            # API health snapshot every 30 min (every 6 ticks)
            if self._tick_count % 6 == 0:
                await run_db(
                    log_scheduler_event, "api_health_snapshot",
                    context={
                        "voyager_health": voyager_health.summary(),
                    },
                )
        except Exception as e:
            logger.debug("API metrics flush failed: %s", e)

        # ── Tick summary + persist timers + event log ──
        logger.info(
            "tick#%d: processed=%d failed=%d planned=%d scheduler=on",
            self._tick_count, tick_processed, tick_failed, tick_planned,
        )
        # Emit tick_summary event (fire-and-forget)
        await run_db(
            log_scheduler_event, "tick_summary",
            context={
                "tick": self._tick_count,
                "processed": tick_processed,
                "failed": tick_failed,
                "planned": tick_planned,
                "scheduler": "on",
            },
        )
        # Persist timers every 5 ticks (~5 min) to survive restarts
        if self._tick_count % 5 == 0:
            try:
                await run_db(save_setting, self._TIMERS_SETTING_KEY, self._timers)
            except Exception as e:
                logger.debug("Timer persistence failed: %s", e)
            # Cleanup old events (7-day retention)
            try:
                await run_db(cleanup_scheduler_events, days=7)
            except Exception as e:
                logger.debug("Event cleanup failed: %s", e)

    async def _process_ready_jobs(
        self, *, scheduler_on: bool = True
    ) -> tuple[int, int]:
        """Find and execute jobs that are ready (scheduled_at <= now).

        When ``scheduler_on`` is False, only inbound job types are executed;
        outbound jobs stay in the queue until the scheduler is re-enabled.

        Jobs are executed concurrently (up to 5 at a time) to avoid slow
        collectors blocking the entire queue.

        Returns:
            (jobs_processed, jobs_failed) counts for tick summary.
        """
        from .executors import execute_job, categorize_error

        # ── Post-outage backlog detection ──
        # If many jobs are stale (scheduled_at > 10 min ago), the scheduler
        # was likely offline. Re-stagger them to avoid a burst that overwhelms
        # the LinkedIn API.
        _STALE_THRESHOLD = 600   # 10 min — jobs older than this are "stale"
        _BACKLOG_MIN = 20        # only act if 20+ stale jobs (normal queue is 0-10)
        _SPREAD_SECONDS = 30     # 1 job every 30s — 100 jobs spread over ~50 min

        stale_count = await run_db(count_stale_ready_jobs, _STALE_THRESHOLD)
        if stale_count >= _BACKLOG_MIN:
            restaggered = await run_db(restagger_stale_jobs, _STALE_THRESHOLD, _SPREAD_SECONDS)
            logger.warning(
                "Post-outage backlog detected: %d stale jobs re-staggered over %d min",
                restaggered, (restaggered * _SPREAD_SECONDS) // 60,
            )
            await run_db(
                log_scheduler_event, "backlog_restaggered",
                context={"stale_count": stale_count, "restaggered": restaggered,
                         "spread_seconds": _SPREAD_SECONDS},
            )

        # Recover stuck jobs (running > 30 min = likely crashed)
        from ..db.queries import recover_stuck_jobs
        stuck_count = await run_db(recover_stuck_jobs, 30)
        if stuck_count:
            logger.warning("Recovered %d stuck jobs (running > 30 min)", stuck_count)

        ready = await run_db(get_ready_jobs, limit=20)

        # Claim jobs sequentially (atomic DB op) before concurrent execution
        claimed: list[dict] = []
        for job in ready:
            job_id = job["id"]
            job_type = job["job_type"]

            # When outbound scheduler is off, only execute inbound jobs
            if not scheduler_on and job_type not in _INBOUND_JOB_TYPES:
                continue

            # Claim the job atomically (prevents double execution)
            if not await run_db(claim_job, job_id):
                logger.debug("Job %s already claimed, skipping", job_id)
                continue

            claimed.append(job)

        if not claimed:
            return 0, 0

        # Track results from concurrent execution
        results: list[bool] = []  # True=success, False=failure
        sem = asyncio.Semaphore(5)

        async def _run_one(job: dict) -> bool:
            async with sem:
                job_id = job["id"]
                job_type = job["job_type"]
                cid = new_correlation_id()
                logger.info("Executing scheduler job: %s (type=%s, cid=%s)", job_id, job_type, cid)

                start_ms = int(time.time() * 1000)
                scheduled_at = job.get("scheduled_at", 0)
                queue_wait_ms = int((time.time() - scheduled_at) * 1000) if scheduled_at else 0
                campaign_id = job.get("campaign_id")
                outreach_id = job.get("outreach_id")
                failed = False
                with tracer.start_as_current_span(f"job:{job_type}") as span:
                    span.set_attribute("job.id", job_id)
                    span.set_attribute("job.type", job_type)
                    span.set_attribute("correlation.id", cid)
                    if campaign_id:
                        span.set_attribute("campaign.id", campaign_id)
                    try:
                        # Long-running collectors get 5 min; everything else 2 min
                        _SLOW_JOBS = {"check_replies", "collect_company_followers",
                                      "collect_posts_distributed", "collect_company_page",
                                      "collect_keyword_signals", "collect_competitor_signals",
                                      "collect_hiring_signals", "collect_news_signals",
                                      "collect_profile_views"}
                        job_timeout = 300 if job_type in _SLOW_JOBS else 120
                        result = await asyncio.wait_for(execute_job(job), timeout=job_timeout)
                        duration_ms = int(time.time() * 1000) - start_ms
                        span.set_attribute("job.duration_ms", duration_ms)

                        # Extract structured outcome from JobResult (if returned)
                        from .executors import JobResult
                        if isinstance(result, JobResult):
                            outcome = result.outcome
                            result_msg = result.message
                        else:
                            outcome = "success"
                            result_msg = str(result) if result else ""

                        await run_db(complete_job, job_id, duration_ms=duration_ms)
                        event_type = f"job_{outcome}" if outcome != "success" else "job_completed"
                        span.set_attribute("job.outcome", outcome)
                        logger.info(
                            "Job %s %s in %dms (type=%s)",
                            job_id, outcome, duration_ms, job_type,
                        )
                        await run_db(
                            log_scheduler_event, event_type,
                            campaign_id=campaign_id, outreach_id=outreach_id,
                            job_id=job_id, duration_ms=duration_ms,
                            context={"job_type": job_type, "outcome": outcome, "correlation_id": cid, "queue_wait_ms": queue_wait_ms},
                        )
                    except Exception as e:
                        failed = True
                        duration_ms = int(time.time() * 1000) - start_ms
                        error_msg = str(e)[:500]
                        error_cat = categorize_error(error_msg)
                        error_tb = _tb.format_exc()[-1500:]
                        span.set_attribute("job.duration_ms", duration_ms)
                        span.set_attribute("error.category", error_cat)
                        span.record_exception(e)
                        await run_db(
                            complete_job, job_id, error=error_msg, duration_ms=duration_ms,
                        )
                        logger.warning(
                            "Job %s failed in %dms [%s]: %s",
                            job_id, duration_ms, error_cat, error_msg,
                            exc_info=True,
                        )
                        await run_db(
                            log_scheduler_event, "job_failed",
                            campaign_id=campaign_id, outreach_id=outreach_id,
                            job_id=job_id, duration_ms=duration_ms,
                            context={
                                "job_type": job_type,
                                "error": error_msg[:200],
                                "error_category": error_cat,
                                "error_traceback": error_tb,
                                "retry_count": job.get("retry_count", 0) + 1,
                                "correlation_id": cid,
                                "queue_wait_ms": queue_wait_ms,
                            },
                        )
                    finally:
                        clear_correlation_id()

                    # Retry failed jobs if under max retries
                    if failed:
                        # Permanent failures (not connected, premium required,
                        # invalid profile) will never resolve — skip ALL retries
                        # to avoid wasting API calls and log noise.
                        if error_cat == "permanent_failure":
                            logger.info(
                                "Job %s permanent failure — no retry (category=%s)",
                                job_id, error_cat,
                            )
                        else:
                            retry_count = job.get("retry_count", 0) + 1
                            if retry_count < SCHEDULER_MAX_RETRIES:
                                new_time = int(time.time()) + SCHEDULER_RETRY_DELAY
                                await run_db(retry_job, job_id, new_time)
                                logger.info("Job %s scheduled for retry #%d", job_id, retry_count)
                            elif job_type in ("send_dm", "followup", "auto_reply", "invite"):
                                # All fast retries exhausted for critical job types.
                                # Create a NEW delayed job with exponential backoff
                                # so the prospect isn't permanently abandoned.
                                _ESCALATION_DELAYS = [3600, 14400, 86400]  # 1h, 4h, 24h
                                escalation_idx = retry_count - SCHEDULER_MAX_RETRIES
                                if escalation_idx < len(_ESCALATION_DELAYS):
                                    delay = _ESCALATION_DELAYS[escalation_idx]
                                    new_time = int(time.time()) + delay
                                    from ..db.queries import create_scheduler_job
                                    await run_db(
                                        create_scheduler_job,
                                        campaign_id=campaign_id,
                                        job_type=job_type,
                                        scheduled_at=new_time,
                                        outreach_id=outreach_id,
                                    )
                                    logger.info(
                                        "Escalated retry for %s job (outreach=%s) in %d min",
                                        job_type, outreach_id, delay // 60,
                                    )

                return not failed

        results = await asyncio.gather(*[_run_one(j) for j in claimed])

        jobs_processed = sum(1 for ok in results if ok)
        jobs_failed = sum(1 for ok in results if not ok)
        return jobs_processed, jobs_failed

    async def _schedule_new_work(self) -> None:
        """Schedule new invite and follow-up jobs for active autopilot campaigns.

        Also schedules follow-ups for completed campaigns — prospects may accept
        invitations days after the campaign finished, and they still need their
        initial DM / follow-up sequence.
        """
        from .planner import plan_campaign_work, _plan_followups

        campaigns = await run_db(list_campaigns, status=STATUS_ACTIVE)
        for campaign in campaigns:
            # Only schedule for autopilot campaigns
            if campaign.get("mode") != "autopilot":
                continue

            try:
                await plan_campaign_work(campaign["id"])
            except Exception as e:
                logger.warning("Planning failed for campaign %s: %s", campaign["id"], e)

        # Completed campaigns: only follow-ups (no new invites/DMs/engagements)
        from ..config import get_tier
        completed = await run_db(list_campaigns, status=STATUS_COMPLETED)
        tier = get_tier()
        for campaign in completed:
            try:
                await _plan_followups(campaign["id"], int(time.time()), tier)
            except Exception as e:
                logger.debug("Follow-up planning failed for completed campaign %s: %s", campaign["id"], e)

    async def _check_auto_resume(self) -> None:
        """Resume autopilot campaigns that were system-paused due to weekly limits.

        Copilot campaigns are not auto-resumed — they get a suggestion
        in suggest_next_action() for the user to resume manually.
        """
        import json as _json
        from ..db.queries import log_action, update_campaign
        from ..linkedin.rate_limiter import can_send_now, BLOCK_DAILY, BLOCK_WEEKLY

        paused = await run_db(list_campaigns, status="paused")
        if not paused:
            return

        # All campaigns share the same LinkedIn account, so check limits once
        can_send, reason, block_type = await can_send_now()
        if block_type in (BLOCK_DAILY, BLOCK_WEEKLY):
            return  # Still limited — nothing to resume

        for campaign in paused:
            cfg = _json.loads(campaign.get("config_json") or "{}")
            pause_reason = cfg.get("pause_reason")

            # Only auto-resume campaigns paused by the system for weekly limits
            if pause_reason != "weekly_limit":
                continue

            # Only auto-resume autopilot campaigns
            if campaign.get("mode") != "autopilot":
                continue

            # Clear pause metadata and resume
            cfg.pop("pause_reason", None)
            cfg.pop("paused_at", None)
            await run_db(
                update_campaign,
                campaign["id"],
                status="active",
                config_json=_json.dumps(cfg),
            )
            await run_db(
                log_action,
                "campaign_status_change",
                result="active",
                details={
                    "campaign_id": campaign["id"],
                    "campaign_name": campaign["name"],
                    "old_status": "paused",
                    "new_status": "active",
                    "changed_by": "scheduler",
                    "reason": "weekly_limit_cleared",
                },
            )
            await run_db(
                log_scheduler_event,
                "campaign_auto_resumed",
                campaign_id=campaign["id"],
                context={
                    "campaign_name": campaign["name"],
                    "reason": "weekly_limit_cleared",
                },
            )

            # Sync to backend
            from ..services.cloud_sync import sync_campaign_status
            try:
                await sync_campaign_status(
                    campaign["id"], "active",
                    caller="scheduler", reason="weekly_limit_cleared",
                )
            except Exception as exc:
                logger.warning("Auto-resume cloud sync failed for %s: %s", campaign["id"], exc)

            logger.info(
                "Auto-resumed campaign %s: %s (weekly limit cleared)",
                campaign["id"], campaign["name"],
            )

    async def _schedule_reply_checks(self) -> None:
        """Schedule reply check jobs for active and completed campaigns.

        Completed campaigns still need reply checks — prospects may reply
        days after the last outreach was sent.
        """
        from ..db.queries import create_scheduler_job, get_pending_job_count

        active = await run_db(list_campaigns, status=STATUS_ACTIVE)
        completed = await run_db(list_campaigns, status=STATUS_COMPLETED)
        campaigns = active + completed
        now = int(time.time())

        for campaign in campaigns:
            campaign_id = campaign["id"]
            # Skip if a reply check is already pending
            if await run_db(get_pending_job_count, campaign_id, JOB_CHECK_REPLIES) > 0:
                continue

            await run_db(
                create_scheduler_job,
                campaign_id=campaign_id,
                job_type=JOB_CHECK_REPLIES,
                scheduled_at=now,  # Execute immediately
            )
            logger.debug("Scheduled reply check for campaign %s", campaign_id)

    async def _schedule_auto_replies(self) -> None:
        """Schedule auto-reply jobs for active and completed campaigns.

        Completed campaigns still need auto-replies — prospects may reply
        days after the last outreach was sent.
        """
        from .planner import plan_auto_replies, plan_inbound_auto_replies

        active = await run_db(list_campaigns, status=STATUS_ACTIVE)
        completed = await run_db(list_campaigns, status=STATUS_COMPLETED)
        campaigns = active + completed
        for campaign in campaigns:
            try:
                await plan_auto_replies(campaign["id"])
            except Exception as e:
                logger.debug(
                    "Auto-reply planning failed for campaign %s: %s",
                    campaign["id"], e,
                )

        # Also plan auto-replies for inbound (campaign-less) outreaches
        try:
            await plan_inbound_auto_replies()
        except Exception as e:
            logger.debug("Inbound auto-reply planning failed: %s", e)

    async def _schedule_profile_views(self) -> None:
        """Schedule profile view warm-up jobs for active autopilot campaigns.

        Profile views are the lightest warm-up touch. The sequence is:
        Profile View → Follow → Endorse → Engage → Invite → Follow-up DM.
        """
        from .planner import plan_profile_views

        campaigns = await run_db(list_campaigns, status=STATUS_ACTIVE)
        for campaign in campaigns:
            if campaign.get("mode") != "autopilot":
                continue

            try:
                await plan_profile_views(campaign["id"])
            except Exception as e:
                logger.debug("Profile view planning failed for campaign %s: %s", campaign["id"], e)

    async def _schedule_follows(self) -> None:
        """Schedule follow warm-up jobs for active autopilot campaigns.

        Follows prospects before engaging with posts to warm them up.
        The sequence is: Follow → Engage → Invite → Follow-up DM.
        """
        from .planner import plan_follows

        campaigns = await run_db(list_campaigns, status=STATUS_ACTIVE)
        for campaign in campaigns:
            if campaign.get("mode") != "autopilot":
                continue

            try:
                await plan_follows(campaign["id"])
            except Exception as e:
                logger.debug("Follow planning failed for campaign %s: %s", campaign["id"], e)

    async def _schedule_process_inbound(self) -> None:
        """Schedule unified classify-first inbound pipeline.

        Account-level (not campaign-specific). Detects invitations + messages,
        classifies all signals via AI, then acts (accept/ignore/DM).
        """
        from .planner import plan_process_inbound

        try:
            await plan_process_inbound()
        except Exception as e:
            logger.debug("Inbound pipeline planning failed: %s", e)

    async def _schedule_check_post_comments(self) -> None:
        """Schedule checking published posts for new comments."""
        from .planner import plan_check_post_comments

        try:
            await plan_check_post_comments()
        except Exception as e:
            logger.debug("Post comment check planning failed: %s", e)

    async def _schedule_keyword_signal_collection(self) -> None:
        """Schedule keyword signal collection from LinkedIn posts."""
        from .planner import plan_keyword_signal_collection

        try:
            await plan_keyword_signal_collection()
        except Exception as e:
            logger.debug("Keyword signal collection planning failed: %s", e)

    async def _schedule_prospect_post_scan(self) -> None:
        """Schedule scanning campaign contacts' posts for signals."""
        from .planner import plan_prospect_post_scan

        try:
            await plan_prospect_post_scan()
        except Exception as e:
            logger.debug("Prospect post scan planning failed: %s", e)

    async def _schedule_signal_classification(self) -> None:
        """Schedule classification of pending signals."""
        from .planner import plan_signal_classification

        try:
            await plan_signal_classification()
        except Exception as e:
            logger.debug("Signal classification planning failed: %s", e)

    async def _schedule_profile_view_collection(self) -> None:
        """Schedule collection of LinkedIn profile viewers."""
        from .planner import plan_profile_view_collection

        try:
            await plan_profile_view_collection()
        except Exception as e:
            logger.debug("Profile view collection planning failed: %s", e)

    async def _schedule_job_change_detection(self) -> None:
        """Schedule job change detection for campaign contacts."""
        from .planner import plan_job_change_detection

        try:
            await plan_job_change_detection()
        except Exception as e:
            logger.debug("Job change detection planning failed: %s", e)

    async def _schedule_competitor_signal_collection(self) -> None:
        """Schedule competitor mention collection from LinkedIn posts."""
        from .planner import plan_competitor_signal_collection

        try:
            await plan_competitor_signal_collection()
        except Exception as e:
            logger.debug("Competitor signal collection planning failed: %s", e)

    async def _schedule_signal_activation(self) -> None:
        """Schedule signal activation — convert high-scoring signals to outreach."""
        from .planner import plan_signal_activation

        try:
            await plan_signal_activation()
        except Exception as e:
            logger.debug("Signal activation planning failed: %s", e)

    async def _schedule_hiring_signal_collection(self) -> None:
        """Schedule hiring surge detection from LinkedIn job searches."""
        from .planner import plan_hiring_signal_collection

        try:
            await plan_hiring_signal_collection()
        except Exception as e:
            logger.debug("Hiring signal collection planning failed: %s", e)

    async def _schedule_news_signal_collection(self) -> None:
        """Schedule news/funding signal collection from SERPER API."""
        from .planner import plan_news_signal_collection

        try:
            await plan_news_signal_collection()
        except Exception as e:
            logger.debug("News signal collection planning failed: %s", e)

    async def _schedule_company_page_collection(self) -> None:
        """Schedule company page engagement signal collection."""
        from .planner import plan_company_page_collection

        try:
            await plan_company_page_collection()
        except Exception as e:
            logger.debug("Company page collection planning failed: %s", e)

    async def _schedule_company_follower_collection(self) -> None:
        """Schedule company follower signal collection."""
        from .planner import plan_company_follower_collection

        try:
            await plan_company_follower_collection()
        except Exception as e:
            logger.debug("Company follower collection planning failed: %s", e)

    async def _schedule_post_intent_classification(self) -> None:
        """Schedule post intent classification for granular buyer signals."""
        from .planner import plan_post_intent_classification

        try:
            await plan_post_intent_classification()
        except Exception as e:
            logger.debug("Post intent classification planning failed: %s", e)

    async def _schedule_comment_mining(self) -> None:
        """Schedule competitor/industry comment mining for lead signals."""
        from .planner import plan_comment_mining

        try:
            await plan_comment_mining()
        except Exception as e:
            logger.debug("Comment mining planning failed: %s", e)

    async def _schedule_compound_intent_detection(self) -> None:
        """Schedule compound intent detection — stack signals into intent events."""
        from .planner import plan_compound_intent_detection

        try:
            await plan_compound_intent_detection()
        except Exception as e:
            logger.debug("Compound intent detection planning failed: %s", e)

    async def _schedule_decay_cycle(self) -> None:
        """Schedule signal decay cycle — expire old signals and recompute scores."""
        from .planner import plan_decay_cycle

        try:
            await plan_decay_cycle()
        except Exception as e:
            logger.debug("Decay cycle planning failed: %s", e)

    async def _schedule_signal_rematch(self) -> None:
        """Schedule re-matching of homeless signals to active campaigns."""
        from .planner import plan_signal_rematch

        try:
            await plan_signal_rematch()
        except Exception as e:
            logger.debug("Signal rematch planning failed: %s", e)

    async def _schedule_orphan_backfill(self) -> None:
        """Schedule backfill of orphan signals to known contacts."""
        from .planner import plan_orphan_signal_backfill

        try:
            await plan_orphan_signal_backfill()
        except Exception as e:
            logger.debug("Orphan signal backfill planning failed: %s", e)

    async def _schedule_endorsements(self) -> None:
        """Schedule skill endorsement warm-up jobs for active autopilot campaigns.

        Endorsements go between follow and engage in the warm-up sequence:
        Follow → Endorse → Engage → Invite → Follow-up DM.
        """
        from .planner import plan_endorsements

        campaigns = await run_db(list_campaigns, status=STATUS_ACTIVE)
        for campaign in campaigns:
            if campaign.get("mode") != "autopilot":
                continue

            try:
                await plan_endorsements(campaign["id"])
            except Exception as e:
                logger.debug("Endorsement planning failed for campaign %s: %s", campaign["id"], e)

    async def _schedule_stale_withdrawals(self) -> None:
        """Schedule stale invitation withdrawal checks.

        Withdraws sent invitations older than STALE_INVITE_DAYS to free up
        LinkedIn invitation quota.
        """
        from .planner import plan_stale_invite_withdrawals

        try:
            await plan_stale_invite_withdrawals()
        except Exception as e:
            logger.debug("Stale invite withdrawal planning failed: %s", e)

    async def _schedule_engagements(self) -> None:
        """Schedule engagement warm-up jobs for active autopilot campaigns."""
        from .planner import plan_engagements

        campaigns = await run_db(list_campaigns, status=STATUS_ACTIVE)
        for campaign in campaigns:
            if campaign.get("mode") != "autopilot":
                continue

            try:
                await plan_engagements(campaign["id"])
            except Exception as e:
                logger.debug("Engagement planning failed for campaign %s: %s", campaign["id"], e)

    # ── Brand strategy scheduling ──

    async def _schedule_brand_lifecycle(self) -> None:
        """Check and manage brand strategy lifecycle (auto-analyze, auto-plan)."""
        from .planner import plan_brand_lifecycle

        try:
            await plan_brand_lifecycle()
        except Exception as e:
            logger.debug("Brand lifecycle planning failed: %s", e)

    async def _schedule_brand_posts(self) -> None:
        """Schedule brand post jobs if plan has pending post actions."""
        from .planner import plan_brand_post

        try:
            await plan_brand_post()
        except Exception as e:
            logger.debug("Brand post planning failed: %s", e)

    async def _schedule_brand_engagements(self) -> None:
        """Schedule brand engagement jobs if plan has pending engagement actions."""
        from .planner import plan_brand_engagement

        try:
            await plan_brand_engagement()
        except Exception as e:
            logger.debug("Brand engagement planning failed: %s", e)

    async def _schedule_campaign_refill(self) -> None:
        """Schedule campaign refill — search for more prospects when running low."""
        from .planner import plan_campaign_refill

        try:
            await plan_campaign_refill()
        except Exception as e:
            logger.debug("Campaign refill planning failed: %s", e)

    async def _schedule_backfill_profiles(self) -> None:
        """Schedule profile backfill for contacts with empty profile_json."""
        from .planner import plan_backfill_profiles

        try:
            await plan_backfill_profiles()
        except Exception as e:
            logger.debug("Profile backfill planning failed: %s", e)
