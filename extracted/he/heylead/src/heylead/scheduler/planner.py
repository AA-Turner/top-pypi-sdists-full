"""Work planner — determines WHAT to schedule and WHEN.

Analyzes active autopilot campaigns and creates scheduler jobs for:
1. Follows: warm-up follows on prospect profiles (new in Sprint 28)
2. Invitations: pending outreaches that need to be sent
3. Follow-ups: connected outreaches that are due based on schedule
4. Engagements: warm-up comments/reactions before inviting

All decisions respect:
- Follow-up schedule (PRO_FOLLOWUP_SCHEDULE_DAYS: 1, 7, 14, 21, 28 days)
- Per-campaign config toggles (enable_follows, enable_engagements, etc.)
- Deduplication (no duplicate pending jobs for same outreach)
- Randomized delays (10-25 min follows, 20-40 min invites, etc.)
- Unipile/LinkedIn as the authority on rate limits (no proactive caps)
"""

from __future__ import annotations

import json
import logging
import random
import time
from typing import Any

from ..config import get_tier
from ..db.async_bridge import run_db
from ..constants import (
    ENDORSE_DELAY_MAX,
    ENDORSE_DELAY_MIN,
    ENGAGEMENT_DELAY_MAX,
    ENGAGEMENT_DELAY_MIN,
    FOLLOW_DELAY_MAX,
    FOLLOW_DELAY_MIN,
    PROFILE_VIEW_DELAY_MAX,
    PROFILE_VIEW_DELAY_MIN,
    FOLLOWUP_DELAY_MAX,
    FOLLOWUP_DELAY_MIN,
    FREE_MAX_FOLLOWUPS,
    DM_DELAY_MAX,
    DM_DELAY_MIN,
    INVITE_DELAY_MAX,
    INVITE_DELAY_MIN,
    JOB_ACCEPT_INBOUND,
    JOB_CHECK_POST_COMMENTS,
    JOB_ENDORSE,
    JOB_ENGAGE,
    JOB_FOLLOW,
    JOB_PROCESS_INBOUND,
    JOB_PROFILE_VIEW,
    JOB_FOLLOWUP,
    JOB_INVITE,
    JOB_QUALIFY_INBOUND,
    JOB_SEND_DM,
    JOB_WITHDRAW_INVITE,
    PRO_FOLLOWUP_SCHEDULE_DAYS,
    PRO_MAX_FOLLOWUPS,
    STALE_INVITE_DAYS,
    TIER_PRO,
)
from ..db.queries import (
    create_scheduler_job,
    get_campaign,
    get_engagement_candidates,
    get_follow_candidates,
    get_followup_candidates,
    get_profile_view_candidates,
    get_messages_for_outreach,
    get_outreach,
    get_pending_job_count,
    get_pending_outreach_job,
    list_campaigns,
)

logger = logging.getLogger(__name__)


async def _log_skip(
    campaign_id: str | None,
    action: str,
    reason: str,
    details: dict[str, Any] | None = None,
) -> None:
    """Log a scheduler skip decision to actions_log. Fire-and-forget."""
    try:
        from ..db.queries import log_action
        await run_db(
            log_action,
            action_type=f"skip_{action}",
            result="skipped",
            campaign_id=campaign_id or "",
            details={"reason": reason, **(details or {})},
        )
    except Exception:
        pass  # Never block the planner


def _has_daily_plan(outreach_id: str) -> bool:
    """Check if this outreach has a daily strategy plan for today.

    If a daily plan exists, the communication strategist owns scheduling
    for this prospect — individual plan_*() functions should skip it.
    Fails open: returns False on any error so hardcoded logic takes over.
    """
    try:
        from ..db.strategist_queries import has_daily_plan
        return has_daily_plan(outreach_id)
    except Exception:
        return False


def _has_recent_completed_job(outreach_id: str, job_type: str) -> bool:
    """Check if a job of this type completed recently for this outreach (within 1 hour).

    Prevents duplicate scheduling when the engagement record hasn't been
    written yet but the job already completed.
    """
    try:
        from ..db.schema import get_db
        db = get_db()
        row = db.execute(
            """SELECT 1 FROM scheduler_jobs
               WHERE outreach_id = ? AND job_type = ?
                 AND status = 'completed'
                 AND completed_at > ?
               LIMIT 1""",
            (outreach_id, job_type, int(time.time()) - 3600),
        ).fetchone()
        db.close()
        return row is not None
    except Exception:
        return False


async def _is_invite_blocked() -> bool:
    """Check if LinkedIn invitations are currently blocked (daily or weekly limit).

    Stubbed — no proactive rate limit checks; Unipile/LinkedIn is the authority.
    """
    return False


def _get_campaign_config(campaign_id: str) -> dict[str, Any]:
    """Load and parse config_json for a campaign. Returns empty dict on failure."""
    campaign = get_campaign(campaign_id)
    if not campaign:
        return {}
    try:
        return json.loads(campaign.get("config_json") or "{}")
    except (json.JSONDecodeError, TypeError):
        return {}


async def plan_campaign_work(campaign_id: str) -> None:
    """Analyze an autopilot campaign and schedule invite + follow-up jobs.

    Called by the scheduler engine every tick for each active autopilot campaign.
    Creates jobs in the scheduler_jobs table with randomized future scheduled_at times.
    """
    now = int(time.time())
    tier = get_tier()

    # ── 1. Invitations or DMs ──
    config = await run_db(_get_campaign_config, campaign_id)
    if not config.get("enable_invitations", True):
        await _plan_dms(campaign_id, now)
    else:
        await _plan_invitations(campaign_id, now, config=config)
        # Schedule initial DMs only for prospects who already accepted an
        # invitation (status='connected').  only_connected=True prevents
        # racing a DM against a pending invite (which fails with 403).
        await _plan_dms(campaign_id, now, only_connected=True)

    # ── 2. Follow-ups ──
    await _plan_followups(campaign_id, now, tier)

    # ── 3. Orphan rescue ──
    # Safety net: find connected prospects with no pending jobs that fell
    # through the cracks (failed jobs, scheduler gaps, etc.) and re-schedule.
    await _rescue_orphans(campaign_id, now, tier)


async def _rescue_orphans(campaign_id: str, now: int, tier: str) -> None:
    """Re-schedule jobs for connected prospects that have no pending work.

    This is a safety net that catches prospects missed by _plan_dms() and
    _plan_followups() — e.g. due to prior failed jobs, scheduler gaps, or
    status transitions that happened outside the normal flow.
    """
    from ..db.queries import find_orphaned_outreaches

    max_followups = PRO_MAX_FOLLOWUPS if tier == TIER_PRO else 2
    orphans = await run_db(find_orphaned_outreaches, campaign_id, max_followups)
    if not orphans:
        return

    rescued = 0
    for orphan in orphans:
        outreach_id = orphan["outreach_id"]
        followup_count = orphan.get("followup_count", 0)

        if followup_count == 0:
            # Needs initial DM — _plan_dms should handle, but if it didn't
            # (e.g. slots were full), schedule directly
            job_type = JOB_SEND_DM
        else:
            job_type = JOB_FOLLOWUP

        delay = random.randint(DM_DELAY_MIN, DM_DELAY_MAX) + (rescued * random.randint(300, 600))
        await run_db(
            create_scheduler_job,
            campaign_id=campaign_id,
            job_type=job_type,
            scheduled_at=now + delay,
            outreach_id=outreach_id,
        )
        logger.info(
            "Rescued orphan outreach %s (followup_count=%d) → %s job in %d min",
            outreach_id, followup_count, job_type, delay // 60,
        )
        rescued += 1

    if rescued:
        await _log_skip(campaign_id, "rescue", "orphans_found", {"rescued": rescued})


async def plan_profile_views(campaign_id: str) -> None:
    """Schedule profile view jobs for pending outreaches that haven't been viewed yet.

    Called every 10 min by the scheduler engine. Profile views warm up
    prospects by triggering a "X viewed your profile" notification —
    the lightest possible warm-up signal before following.
    Skipped if enable_profile_views is off in campaign config.
    """
    # Check per-campaign toggle
    config = await run_db(_get_campaign_config, campaign_id)
    if not config.get("enable_profile_views", True):
        logger.debug("Profile views disabled for campaign %s", campaign_id)
        await _log_skip(campaign_id, "profile_view", "feature_disabled")
        return
    if not config.get("enable_invitations", True):
        await _log_skip(campaign_id, "profile_view", "dm_only_campaign")
        return

    now = int(time.time())

    # Check for existing pending profile view jobs for this campaign (dedup)
    pending_count = await run_db(get_pending_job_count, campaign_id, JOB_PROFILE_VIEW)
    if pending_count >= 5:
        logger.debug("Already %d pending profile view jobs for campaign %s", pending_count, campaign_id)
        await _log_skip(campaign_id, "profile_view", "pending_jobs_full", {"pending": pending_count})
        return

    # Find pending outreaches that haven't been viewed yet
    candidates = await run_db(get_profile_view_candidates, campaign_id)
    if not candidates:
        await _log_skip(campaign_id, "profile_view", "no_candidates")
        return

    # Schedule up to 5 profile view jobs with staggered delays
    scheduled = 0
    for candidate in candidates[:8]:
        outreach_id = candidate["outreach_id"]

        # Skip if this outreach already has a pending profile view job
        if await run_db(get_pending_outreach_job, outreach_id, JOB_PROFILE_VIEW):
            continue

        # Skip if communication strategist owns this prospect's schedule today
        if await run_db(_has_daily_plan, outreach_id):
            continue

        delay = random.randint(PROFILE_VIEW_DELAY_MIN, PROFILE_VIEW_DELAY_MAX)
        scheduled_at = now + delay + (scheduled * random.randint(180, 420))

        await run_db(
            create_scheduler_job,
            campaign_id=campaign_id,
            job_type=JOB_PROFILE_VIEW,
            scheduled_at=scheduled_at,
            outreach_id=outreach_id,
        )
        logger.debug(
            "Scheduled profile view for outreach %s in %d min",
            outreach_id, (scheduled_at - now) // 60,
        )
        scheduled += 1
        if scheduled >= 5:
            break


async def plan_follows(campaign_id: str) -> None:
    """Schedule follow jobs for pending outreaches that haven't been followed yet.

    Called every 15 min by the scheduler engine. Follows warm up prospects
    by triggering a "X started following you" notification before connecting.
    Skipped if enable_follows is off in campaign config.
    """
    # Check per-campaign toggle
    config = await run_db(_get_campaign_config, campaign_id)
    if not config.get("enable_follows", True):
        logger.debug("Follows disabled for campaign %s", campaign_id)
        await _log_skip(campaign_id, "follow", "feature_disabled")
        return
    if not config.get("enable_invitations", True):
        await _log_skip(campaign_id, "follow", "dm_only_campaign")
        return

    now = int(time.time())

    # Check for existing pending follow jobs for this campaign (dedup)
    pending_count = await run_db(get_pending_job_count, campaign_id, JOB_FOLLOW)
    if pending_count >= 4:
        logger.debug("Already %d pending follow jobs for campaign %s", pending_count, campaign_id)
        await _log_skip(campaign_id, "follow", "pending_jobs_full", {"pending": pending_count})
        return

    # Find pending outreaches that haven't been followed yet
    candidates = await run_db(get_follow_candidates, campaign_id)
    if not candidates:
        await _log_skip(campaign_id, "follow", "no_candidates")
        return

    # Schedule up to 4 follow jobs with staggered delays
    scheduled = 0
    for candidate in candidates[:6]:
        outreach_id = candidate["outreach_id"]

        # Skip if this outreach already has a pending follow job
        if await run_db(get_pending_outreach_job, outreach_id, JOB_FOLLOW):
            continue

        # Skip if a follow job completed recently (race condition guard)
        if await run_db(_has_recent_completed_job, outreach_id, JOB_FOLLOW):
            continue

        # Skip if communication strategist owns this prospect's schedule today
        if await run_db(_has_daily_plan, outreach_id):
            continue

        delay = random.randint(FOLLOW_DELAY_MIN, FOLLOW_DELAY_MAX)
        scheduled_at = now + delay + (scheduled * random.randint(300, 600))

        await run_db(
            create_scheduler_job,
            campaign_id=campaign_id,
            job_type=JOB_FOLLOW,
            scheduled_at=scheduled_at,
            outreach_id=outreach_id,
        )
        logger.debug(
            "Scheduled follow for outreach %s in %d min",
            outreach_id, (scheduled_at - now) // 60,
        )
        scheduled += 1
        if scheduled >= 4:
            break


async def plan_engagements(campaign_id: str) -> None:
    """Schedule engagement warm-up jobs for an autopilot campaign.

    Called less frequently (every 30 min) since engagements are lower priority.
    Skipped if enable_engagements is off in campaign config.
    """
    # Check per-campaign toggle
    config = await run_db(_get_campaign_config, campaign_id)
    if not config.get("enable_engagements", True):
        logger.debug("Engagements disabled for campaign %s", campaign_id)
        await _log_skip(campaign_id, "engage", "feature_disabled")
        return
    if not config.get("enable_invitations", True):
        await _log_skip(campaign_id, "engage", "dm_only_campaign")
        return

    now = int(time.time())
    max_per_outreach = 3

    # Check for existing pending engagement jobs for this campaign
    pending_count = await run_db(get_pending_job_count, campaign_id, JOB_ENGAGE)
    if pending_count >= 4:
        logger.debug("Already %d pending engagement jobs for campaign %s", pending_count, campaign_id)
        await _log_skip(campaign_id, "engage", "pending_jobs_full", {"pending": pending_count})
        return

    # Find engagement candidates
    candidates = await run_db(get_engagement_candidates, campaign_id, max_per_outreach=max_per_outreach)
    if not candidates:
        await _log_skip(campaign_id, "engage", "no_candidates")
        return

    # Schedule up to 4 engagement jobs with staggered delays
    scheduled = 0
    for candidate in candidates[:6]:
        outreach_id = candidate["outreach_id"]

        # Skip if this outreach already has a pending engagement job
        if await run_db(get_pending_outreach_job, outreach_id, JOB_ENGAGE):
            continue

        # Skip if communication strategist owns this prospect's schedule today
        if await run_db(_has_daily_plan, outreach_id):
            continue

        delay = random.randint(ENGAGEMENT_DELAY_MIN, ENGAGEMENT_DELAY_MAX)
        scheduled_at = now + delay + (scheduled * random.randint(300, 600))

        await run_db(
            create_scheduler_job,
            campaign_id=campaign_id,
            job_type=JOB_ENGAGE,
            scheduled_at=scheduled_at,
            outreach_id=outreach_id,
        )
        logger.debug(
            "Scheduled engagement for outreach %s in %d min",
            outreach_id, (scheduled_at - now) // 60,
        )
        scheduled += 1
        if scheduled >= 4:
            break


async def _plan_dms(
    campaign_id: str, now: int, *, only_connected: bool = False,
) -> None:
    """Schedule DM jobs for prospects needing their first message.

    When *only_connected* is False (DM-only campaigns): targets 'pending' or
    'connected' prospects — 'pending' ones are existing connections detected
    via silent-sync.

    When *only_connected* is True (invitation-based campaigns): targets only
    'connected' prospects — those who already accepted an invitation.  This
    prevents racing a DM against a pending invite, which would fail with
    403 subscription_required.

    Schedules up to 5 DM jobs per tick to avoid throughput bottlenecks.
    """
    pending_dms = await run_db(get_pending_job_count, campaign_id, JOB_SEND_DM)
    if pending_dms >= 5:
        await _log_skip(campaign_id, "dm", "pending_jobs_full", {"pending": pending_dms})
        return

    from ..db.queries import get_next_dm_candidate

    slots = 5 - pending_dms
    scheduled = 0
    for _ in range(slots):
        outreach = await run_db(
            get_next_dm_candidate, campaign_id, JOB_SEND_DM,
            only_connected=only_connected,
        )
        if not outreach:
            break

        delay = random.randint(DM_DELAY_MIN, DM_DELAY_MAX) + (scheduled * random.randint(300, 600))
        await run_db(
            create_scheduler_job,
            campaign_id=campaign_id,
            job_type=JOB_SEND_DM,
            scheduled_at=now + delay,
            outreach_id=outreach["id"],
        )
        logger.debug(
            "Scheduled DM for outreach %s in campaign %s in %d min",
            outreach["id"], campaign_id, delay // 60,
        )
        scheduled += 1

    if scheduled == 0:
        await _log_skip(campaign_id, "dm", "no_candidates")


async def _plan_invitations(
    campaign_id: str, now: int, *, config: dict[str, Any] | None = None,
) -> None:
    """Schedule invitation jobs for pending outreaches.

    LinkedIn first; falls back to email when LinkedIn limits are hit.
    """
    # Check LinkedIn pending invitation count — if at limit, auto-withdraw oldest
    try:
        from ..linkedin import get_account_id, get_linkedin_client
        from ..linkedin.rate_limiter import check_pending_limit, withdraw_oldest_to_free_spot
        _acct = get_account_id()
        if _acct:
            _client = get_linkedin_client()
            can_send_pending, pending_reason, _ = await check_pending_limit(_client, _acct)
            if not can_send_pending:
                logger.info("Pending limit hit — auto-withdrawing oldest invite to free spot")
                wd_result = await withdraw_oldest_to_free_spot(_client, _acct)
                if wd_result.get("success"):
                    logger.info(
                        "Auto-withdrew invite for %s (%d days old) to free spot",
                        wd_result.get("name", "unknown"), wd_result.get("days_old", 0),
                    )
                else:
                    logger.warning("Auto-withdraw failed: %s — skipping invitations", wd_result.get("error"))
                    await _log_skip(campaign_id, "invite", "pending_limit", {"reason": pending_reason})
                    return
    except Exception as e:
        logger.warning("Pending limit check failed in planner (non-blocking): %s", e)

    # Check for existing pending invite jobs (dedup)
    pending_invites = await run_db(get_pending_job_count, campaign_id, JOB_INVITE)
    if pending_invites >= 5:
        logger.debug("Already %d pending invite jobs for campaign %s", pending_invites, campaign_id)
        await _log_skip(campaign_id, "invite", "pending_jobs_full", {"pending": pending_invites})
        return

    # Pick a specific outreach to bind the job to (prevents duplicate sends).
    # exclude_job_type filters out outreaches that already have a pending/running
    # invite job, so the planner doesn't get stuck on the same top-ranked prospect.
    from ..db.queries import get_next_pending_outreach
    outreach = await run_db(get_next_pending_outreach, campaign_id, JOB_INVITE)
    if not outreach:
        await _log_skip(campaign_id, "invite", "no_candidates")
        return

    # Schedule one invitation with randomized delay
    delay = random.randint(INVITE_DELAY_MIN, INVITE_DELAY_MAX)
    scheduled_at = now + delay

    await run_db(
        create_scheduler_job,
        campaign_id=campaign_id,
        job_type=JOB_INVITE,
        scheduled_at=scheduled_at,
        outreach_id=outreach["id"],
    )
    logger.debug(
        "Scheduled invitation for outreach %s in campaign %s in %d min",
        outreach["id"], campaign_id, delay // 60,
    )


async def _plan_email_overflow(campaign_id: str, now: int) -> None:
    """Schedule email invitation jobs when LinkedIn limits are hit.

    Only targets prospects who:
    - Have status = 'pending' (not yet contacted on any channel)
    - Have an email address available
    - Email account is connected
    - Email rate limits are not exhausted
    """
    from ..constants import (
        EMAIL_INVITE_DELAY_MIN,
        EMAIL_INVITE_DELAY_MAX,
        JOB_EMAIL_INVITE,
    )
    from ..services.channel_selector import has_email_channel
    from ..linkedin.rate_limiter import can_send_email_now

    # Guard: email channel must be available
    if not await run_db(has_email_channel):
        logger.debug("Email overflow: no email channel configured")
        await _log_skip(campaign_id, "email", "no_email_channel")
        return

    # Guard: check email rate limits
    can_email, email_reason = await can_send_email_now()
    if not can_email:
        logger.debug("Email overflow: %s", email_reason)
        await _log_skip(campaign_id, "email", "rate_limited", {"reason": email_reason})
        return

    # Guard: dedup — don't pile up email jobs
    pending_email_jobs = await run_db(get_pending_job_count, campaign_id, JOB_EMAIL_INVITE)
    if pending_email_jobs >= 2:
        logger.debug(
            "Already %d pending email invite jobs for campaign %s",
            pending_email_jobs, campaign_id,
        )
        await _log_skip(campaign_id, "email", "pending_jobs_full", {"pending": pending_email_jobs})
        return

    # Find pending prospects with email addresses
    from ..db.queries import get_email_eligible_pending_outreaches
    candidates = await run_db(get_email_eligible_pending_outreaches, campaign_id, 5)

    if not candidates:
        logger.debug("Email overflow: no email-eligible prospects in campaign %s", campaign_id)
        await _log_skip(campaign_id, "email", "no_candidates")
        return

    # Schedule one email invite job (highest fit_score first)
    best = candidates[0]
    delay = random.randint(EMAIL_INVITE_DELAY_MIN, EMAIL_INVITE_DELAY_MAX)
    scheduled_at = now + delay

    await run_db(
        create_scheduler_job,
        campaign_id=campaign_id,
        job_type=JOB_EMAIL_INVITE,
        scheduled_at=scheduled_at,
        outreach_id=best["outreach_id"],
    )
    logger.info(
        "Email overflow: scheduled email invite for %s (campaign %s) in %d min",
        best.get("name", "unknown"), campaign_id, delay // 60,
    )


async def _plan_followups(campaign_id: str, now: int, tier: str) -> None:
    """Schedule follow-up jobs for connected outreaches that are due."""
    # Check per-campaign toggle
    config = await run_db(_get_campaign_config, campaign_id)
    if not config.get("enable_followups", True):
        logger.debug("Follow-ups disabled for campaign %s", campaign_id)
        await _log_skip(campaign_id, "followup", "feature_disabled")
        return

    # Use per-campaign max_followups if set, else tier default
    config_max = config.get("max_followups")
    if config_max and isinstance(config_max, int) and 1 <= config_max <= 5:
        max_followups = config_max
    else:
        max_followups = PRO_MAX_FOLLOWUPS if tier == TIER_PRO else FREE_MAX_FOLLOWUPS

    # Check for existing pending followup jobs (dedup)
    pending_followups = await run_db(get_pending_job_count, campaign_id, JOB_FOLLOWUP)
    if pending_followups >= 3:
        logger.debug("Already %d pending followup jobs for campaign %s", pending_followups, campaign_id)
        await _log_skip(campaign_id, "followup", "pending_jobs_full", {"pending": pending_followups})
        return

    # Find connected outreaches ready for follow-up
    candidates = await run_db(get_followup_candidates, campaign_id, max_followups)
    if not candidates:
        await _log_skip(campaign_id, "followup", "no_candidates")
        return

    scheduled = 0
    for candidate in candidates:
        outreach_id = candidate["outreach_id"]

        # Skip prospects that haven't been messaged yet (followup_count=0).
        # Their initial DM is handled by _plan_dms(), not follow-ups.
        if candidate.get("followup_count", 0) == 0:
            continue

        # Skip if this outreach already has a pending followup job
        if await run_db(get_pending_outreach_job, outreach_id, JOB_FOLLOWUP):
            continue

        # Skip if communication strategist owns this prospect's schedule today
        if await run_db(_has_daily_plan, outreach_id):
            continue

        # Check if follow-up is due based on schedule (per-campaign or global)
        custom_schedule = config.get("followup_delay_days")
        if custom_schedule and not isinstance(custom_schedule, list):
            custom_schedule = None
        if not _is_followup_due(candidate, tier, custom_schedule=custom_schedule):
            continue

        # Schedule with randomized delay + stagger
        delay = random.randint(FOLLOWUP_DELAY_MIN, FOLLOWUP_DELAY_MAX)
        scheduled_at = now + delay + (scheduled * random.randint(300, 600))

        await run_db(
            create_scheduler_job,
            campaign_id=campaign_id,
            job_type=JOB_FOLLOWUP,
            scheduled_at=scheduled_at,
            outreach_id=outreach_id,
        )
        logger.debug(
            "Scheduled follow-up #%d for outreach %s in %d min",
            candidate.get("followup_count", 0) + 1,
            outreach_id,
            (scheduled_at - now) // 60,
        )
        scheduled += 1
        if scheduled >= 2:
            break


async def plan_auto_replies(campaign_id: str) -> None:
    """Schedule auto-reply jobs for outreaches that received prospect messages.

    Called every 5 min by the scheduler engine. Creates JOB_AUTO_REPLY jobs
    with randomized delays (5-15 min) after the prospect's message was received.
    Skipped if enable_auto_replies is off in campaign config.

    For autopilot campaigns: auto-sends replies after validation.
    For copilot campaigns: queues replies for user review.
    """
    from ..constants import (
        AUTO_REPLY_DELAY_MAX,
        AUTO_REPLY_DELAY_MIN,
        JOB_AUTO_REPLY,
    )
    from ..db.queries import (
        get_auto_reply_candidates,
    )

    # Check per-campaign toggle
    config = await run_db(_get_campaign_config, campaign_id)
    if not config.get("enable_auto_replies", True):
        logger.debug("Auto-replies disabled for campaign %s", campaign_id)
        await _log_skip(campaign_id, "auto_reply", "feature_disabled")
        return

    # Check for existing pending auto-reply jobs (dedup)
    pending = await run_db(get_pending_job_count, campaign_id, JOB_AUTO_REPLY)
    if pending >= 5:
        logger.debug("Already %d pending auto-reply jobs for campaign %s", pending, campaign_id)
        await _log_skip(campaign_id, "auto_reply", "pending_jobs_full", {"pending": pending})
        return

    # Find candidates with minimum age filter (ensures delay has elapsed)
    candidates = await run_db(get_auto_reply_candidates, campaign_id, AUTO_REPLY_DELAY_MIN)
    if not candidates:
        await _log_skip(campaign_id, "auto_reply", "no_candidates")
        return

    now = int(time.time())
    scheduled = 0

    for candidate in candidates:
        outreach_id = candidate["outreach_id"]

        # Skip if this outreach already has a pending auto-reply job
        if await run_db(get_pending_outreach_job, outreach_id, JOB_AUTO_REPLY):
            continue

        # NOTE: Do NOT check _has_daily_plan here. The strategist creates
        # "skip_today" plans for replied/messaged outreaches, which would
        # block auto-replies entirely. Auto-replies are reactive (responding
        # to prospect messages) and must always take priority.

        # Calculate delay: random between now and remaining max delay
        last_msg_ts = candidate.get("last_message_ts", now)
        elapsed = now - last_msg_ts
        remaining_max = max(0, AUTO_REPLY_DELAY_MAX - elapsed)
        delay = random.randint(0, remaining_max) + (scheduled * random.randint(120, 300))
        scheduled_at = now + delay

        await run_db(
            create_scheduler_job,
            campaign_id=campaign_id,
            job_type=JOB_AUTO_REPLY,
            scheduled_at=scheduled_at,
            outreach_id=outreach_id,
        )
        logger.info(
            "Scheduled auto-reply for outreach %s in %d min (sentiment=%s)",
            outreach_id[:8],
            delay // 60,
            candidate.get("last_sentiment", "unknown"),
        )
        scheduled += 1
        if scheduled >= 3:  # Max 3 per planning cycle (pacing)
            break


async def plan_inbound_auto_replies() -> None:
    """Schedule auto-reply jobs for inbound outreaches (no campaign).

    Handles organic LinkedIn messages that aren't part of any campaign.
    Uses the same delay and dedup logic as campaign auto-replies.
    """
    from ..constants import (
        AUTO_REPLY_DELAY_MAX,
        AUTO_REPLY_DELAY_MIN,
        JOB_AUTO_REPLY,
    )
    from ..db.queries import (
        get_inbound_auto_reply_candidates,
    )

    # Check for existing pending inbound auto-reply jobs
    pending = await run_db(get_pending_job_count, "", JOB_AUTO_REPLY)
    if pending >= 5:
        logger.debug("Already %d pending inbound auto-reply jobs", pending)
        return

    candidates = await run_db(get_inbound_auto_reply_candidates, AUTO_REPLY_DELAY_MIN)
    if not candidates:
        return

    now = int(time.time())
    scheduled = 0

    for candidate in candidates:
        outreach_id = candidate["outreach_id"]

        # Skip if this outreach already has a pending auto-reply job
        if await run_db(get_pending_outreach_job, outreach_id, JOB_AUTO_REPLY):
            continue

        # Calculate delay: random between now and remaining max delay
        last_msg_ts = candidate.get("last_message_ts", now)
        elapsed = now - last_msg_ts
        remaining_max = max(0, AUTO_REPLY_DELAY_MAX - elapsed)
        delay = random.randint(0, remaining_max) + (scheduled * random.randint(120, 300))
        scheduled_at = now + delay

        await run_db(
            create_scheduler_job,
            campaign_id="",
            job_type=JOB_AUTO_REPLY,
            scheduled_at=scheduled_at,
            outreach_id=outreach_id,
        )
        logger.info(
            "Scheduled inbound auto-reply for outreach %s in %d min (sentiment=%s)",
            outreach_id[:8],
            delay // 60,
            candidate.get("last_sentiment", "unknown"),
        )
        scheduled += 1
        if scheduled >= 3:  # Max 3 per planning cycle (pacing)
            break


async def plan_endorsements(campaign_id: str) -> None:
    """Schedule endorsement jobs for prospects that haven't been endorsed yet.

    Called every 15 min. Endorses prospects' skills as a high-visibility
    warm-up touch (triggers "X endorsed your skills" notification).
    Sequence: Follow → Endorse → Engage → Invite → Follow-up DM.
    Skipped if enable_endorsements is off in campaign config or globally disabled.
    """
    from ..constants import ENDORSEMENT_ENABLED
    if not ENDORSEMENT_ENABLED:
        await _log_skip(campaign_id, "endorse", "globally_disabled")
        return

    # Check per-campaign toggle
    config = await run_db(_get_campaign_config, campaign_id)
    if not config.get("enable_endorsements", True):
        logger.debug("Endorsements disabled for campaign %s", campaign_id)
        await _log_skip(campaign_id, "endorse", "feature_disabled")
        return
    if not config.get("enable_invitations", True):
        await _log_skip(campaign_id, "endorse", "dm_only_campaign")
        return

    now = int(time.time())

    # Dedup: check for existing pending endorse jobs
    pending_count = await run_db(get_pending_job_count, campaign_id, JOB_ENDORSE)
    if pending_count >= 3:
        logger.debug("Already %d pending endorse jobs for campaign %s", pending_count, campaign_id)
        await _log_skip(campaign_id, "endorse", "pending_jobs_full", {"pending": pending_count})
        return

    # Find candidates: pending or followed outreaches without an endorsement engagement
    # Respects both permanent skip_engagement and time-limited JSON cooldowns
    def _query_endorse_candidates(cid: str) -> list:
        from ..db.schema import get_db
        _now = int(time.time())
        db = get_db()
        rows = db.execute(
            """SELECT o.id as outreach_id
               FROM outreaches o
               JOIN contacts c ON o.contact_id = c.id
               WHERE o.campaign_id = ?
                 AND o.status IN ('pending', 'invited')
                 AND COALESCE(o.next_action, '') != 'skip_engagement'
                 AND (
                   o.next_action IS NULL
                   OR o.next_action = ''
                   OR json_valid(o.next_action) = 0
                   OR json_extract(o.next_action, '$.skip_engagement_until') IS NULL
                   OR json_extract(o.next_action, '$.skip_engagement_until') < ?
                 )
                 AND NOT EXISTS (
                     SELECT 1 FROM engagements e
                     WHERE e.outreach_id = o.id AND e.action_type = 'endorse'
                 )
               ORDER BY c.fit_score DESC
               LIMIT 6""",
            (cid, _now),
        ).fetchall()
        db.close()
        return rows

    candidates = await run_db(_query_endorse_candidates, campaign_id)

    if not candidates:
        await _log_skip(campaign_id, "endorse", "no_candidates")
        return

    scheduled = 0
    for cand in candidates:
        outreach_id = cand["outreach_id"]

        if await run_db(get_pending_outreach_job, outreach_id, JOB_ENDORSE):
            continue

        # Skip if communication strategist owns this prospect's schedule today
        if await run_db(_has_daily_plan, outreach_id):
            continue

        delay = random.randint(ENDORSE_DELAY_MIN, ENDORSE_DELAY_MAX)
        scheduled_at = now + delay + (scheduled * random.randint(300, 600))

        await run_db(
            create_scheduler_job,
            campaign_id=campaign_id,
            job_type=JOB_ENDORSE,
            scheduled_at=scheduled_at,
            outreach_id=outreach_id,
        )
        logger.debug(
            "Scheduled endorsement for outreach %s in %d min",
            outreach_id, (scheduled_at - now) // 60,
        )
        scheduled += 1
        if scheduled >= 3:
            break


async def plan_stale_invite_withdrawals() -> None:
    """Schedule a single job to check and withdraw stale sent invitations.

    Called every hour. Finds sent invitations older than STALE_INVITE_DAYS
    and schedules withdrawal to free up invite quota.
    """
    now = int(time.time())

    # Only schedule if no withdraw job is already pending
    pending_count = await run_db(get_pending_job_count, None, JOB_WITHDRAW_INVITE)
    if pending_count > 0:
        logger.debug("Already %d pending withdraw jobs", pending_count)
        return

    await run_db(
        create_scheduler_job,
        campaign_id=None,
        job_type=JOB_WITHDRAW_INVITE,
        scheduled_at=now,
    )
    logger.debug("Scheduled stale invite withdrawal check")


async def plan_process_inbound() -> None:
    """Schedule unified classify-first inbound pipeline.

    Called every 15 min by the scheduler engine. Creates one JOB_PROCESS_INBOUND
    job that detects, classifies, and acts on all inbound signals in a single pass.

    Replaces the old plan_inbound_accepts() + plan_qualify_inbound().
    """
    now = int(time.time())

    pending_count = await run_db(get_pending_job_count, None, JOB_PROCESS_INBOUND)
    if pending_count > 0:
        logger.debug("Already %d pending process_inbound jobs", pending_count)
        return

    await run_db(
        create_scheduler_job,
        campaign_id=None,
        job_type=JOB_PROCESS_INBOUND,
        scheduled_at=now,
    )
    logger.debug("Scheduled unified inbound pipeline")


# DEPRECATED: kept for backward compatibility with in-flight jobs
async def plan_inbound_accepts() -> None:
    """DEPRECATED: Use plan_process_inbound() instead."""
    await plan_process_inbound()


async def plan_qualify_inbound() -> None:
    """DEPRECATED: Use plan_process_inbound() instead."""
    await plan_process_inbound()


async def plan_check_post_comments() -> None:
    """Schedule a job to check comments on recently published posts.

    Called every 30 min by the scheduler engine.
    """
    now = int(time.time())

    pending_count = await run_db(get_pending_job_count, None, JOB_CHECK_POST_COMMENTS)
    if pending_count > 0:
        logger.debug("Already %d pending check_post_comments jobs", pending_count)
        return

    await run_db(
        create_scheduler_job,
        campaign_id=None,
        job_type=JOB_CHECK_POST_COMMENTS,
        scheduled_at=now,
    )
    logger.debug("Scheduled post comment check")


# ──────────────────────────────────────────────
# Signal collection planners (v1.0)
# ──────────────────────────────────────────────


async def plan_keyword_signal_collection() -> None:
    """Schedule a job to collect keyword signals from LinkedIn post searches.

    Called every 30 min by the scheduler engine. Creates one
    JOB_COLLECT_KEYWORD_SIGNALS job that iterates all active watchlists.
    """
    from ..constants import JOB_COLLECT_KEYWORD_SIGNALS

    now = int(time.time())

    pending_count = await run_db(get_pending_job_count, None, JOB_COLLECT_KEYWORD_SIGNALS)
    if pending_count > 0:
        logger.debug("Already %d pending keyword signal collection jobs", pending_count)
        return

    # Only schedule if there are active watchlists
    from ..db.signal_queries import list_watchlists
    watchlists = await run_db(list_watchlists, is_active=True)
    if not watchlists:
        return

    await run_db(
        create_scheduler_job,
        campaign_id=None,
        job_type=JOB_COLLECT_KEYWORD_SIGNALS,
        scheduled_at=now,
    )
    logger.debug("Scheduled keyword signal collection (%d active watchlists)", len(watchlists))


async def plan_prospect_post_scan() -> None:
    """Schedule a job to scan campaign contacts' recent posts for signals.

    Called every 1 hour by the scheduler engine. Creates one
    JOB_SCAN_PROSPECT_POSTS job that iterates active campaign contacts.
    """
    from ..constants import JOB_SCAN_PROSPECT_POSTS

    now = int(time.time())

    pending_count = await run_db(get_pending_job_count, None, JOB_SCAN_PROSPECT_POSTS)
    if pending_count > 0:
        logger.debug("Already %d pending prospect post scan jobs", pending_count)
        return

    # Only schedule if there are active campaigns with contacts
    active = await run_db(list_campaigns, status="active")
    if not active:
        return

    await run_db(
        create_scheduler_job,
        campaign_id=None,
        job_type=JOB_SCAN_PROSPECT_POSTS,
        scheduled_at=now,
    )
    logger.debug("Scheduled prospect post scan (%d active campaigns)", len(active))


async def plan_signal_classification() -> None:
    """Schedule a job to classify pending signals with LLM.

    Called every 15 min by the scheduler engine. Creates one
    JOB_CLASSIFY_SIGNALS job that processes signals with status='new'.
    """
    from ..constants import JOB_CLASSIFY_SIGNALS

    now = int(time.time())

    pending_count = await run_db(get_pending_job_count, None, JOB_CLASSIFY_SIGNALS)
    if pending_count > 0:
        logger.debug("Already %d pending signal classification jobs", pending_count)
        return

    # Only schedule if there are unclassified signals
    from ..db.signal_queries import list_signals
    from ..constants import SIGNAL_STATUS_NEW

    unclassified = await run_db(list_signals, status=SIGNAL_STATUS_NEW, limit=1)
    if not unclassified:
        return

    await run_db(
        create_scheduler_job,
        campaign_id=None,
        job_type=JOB_CLASSIFY_SIGNALS,
        scheduled_at=now,
    )
    logger.debug("Scheduled signal classification")


async def plan_profile_view_collection() -> None:
    """Schedule a job to collect LinkedIn profile viewers.

    Called every 1 hour by the scheduler engine. Creates one
    JOB_COLLECT_PROFILE_VIEWS job. Requires LinkedIn Premium.
    """
    from ..constants import JOB_COLLECT_PROFILE_VIEWS

    now = int(time.time())

    pending_count = await run_db(get_pending_job_count, None, JOB_COLLECT_PROFILE_VIEWS)
    if pending_count > 0:
        logger.debug("Already %d pending profile view collection jobs", pending_count)
        return

    await run_db(
        create_scheduler_job,
        campaign_id=None,
        job_type=JOB_COLLECT_PROFILE_VIEWS,
        scheduled_at=now,
    )
    logger.debug("Scheduled profile view collection")


async def plan_job_change_detection() -> None:
    """Schedule a job to detect job title/company changes for campaign contacts.

    Called every 4 hours by the scheduler engine. Creates one
    JOB_DETECT_JOB_CHANGES job that scans contacts not recently scanned.
    """
    from ..constants import JOB_DETECT_JOB_CHANGES

    now = int(time.time())

    pending_count = await run_db(get_pending_job_count, None, JOB_DETECT_JOB_CHANGES)
    if pending_count > 0:
        logger.debug("Already %d pending job change detection jobs", pending_count)
        return

    # Only schedule if there are active campaigns with contacts
    active = await run_db(list_campaigns, status="active")
    if not active:
        return

    await run_db(
        create_scheduler_job,
        campaign_id=None,
        job_type=JOB_DETECT_JOB_CHANGES,
        scheduled_at=now,
    )
    logger.debug("Scheduled job change detection (%d active campaigns)", len(active))


async def plan_competitor_signal_collection() -> None:
    """Schedule a job to collect competitor mention signals from LinkedIn posts.

    Called every 30 min by the scheduler engine. Creates one
    JOB_COLLECT_COMPETITOR_SIGNALS job that searches for competitor names.
    """
    from ..constants import JOB_COLLECT_COMPETITOR_SIGNALS

    now = int(time.time())

    pending_count = await run_db(get_pending_job_count, None, JOB_COLLECT_COMPETITOR_SIGNALS)
    if pending_count > 0:
        logger.debug("Already %d pending competitor signal collection jobs", pending_count)
        return

    # Only schedule if there are active competitor watchlists
    from ..db.signal_queries import list_watchlists

    comp_watchlists = await run_db(list_watchlists, is_active=True, watch_type="competitor")
    if not comp_watchlists:
        return

    await run_db(
        create_scheduler_job,
        campaign_id=None,
        job_type=JOB_COLLECT_COMPETITOR_SIGNALS,
        scheduled_at=now,
    )
    logger.debug(
        "Scheduled competitor signal collection (%d competitor watchlists)",
        len(comp_watchlists),
    )


async def plan_signal_activation() -> None:
    """Schedule signal activation — convert classified signals to outreach.

    Called every 15 min by the scheduler engine. Creates one
    JOB_ACTIVATE_SIGNALS job if classified signals exist.
    """
    from ..constants import JOB_ACTIVATE_SIGNALS, SIGNAL_STATUS_CLASSIFIED

    now = int(time.time())

    pending_count = await run_db(get_pending_job_count, None, JOB_ACTIVATE_SIGNALS)
    if pending_count > 0:
        logger.debug("Already %d pending signal activation jobs", pending_count)
        return

    # Only schedule if there are classified signals to process
    from ..db.signal_queries import list_signals

    classified = await run_db(list_signals, status=SIGNAL_STATUS_CLASSIFIED, limit=1)
    if not classified:
        return

    await run_db(
        create_scheduler_job,
        campaign_id=None,
        job_type=JOB_ACTIVATE_SIGNALS,
        scheduled_at=now,
    )
    logger.debug("Scheduled signal activation")


async def plan_hiring_signal_collection() -> None:
    """Schedule hiring surge detection from LinkedIn job searches.

    Called every 4 hours by the scheduler engine. Creates one
    JOB_COLLECT_HIRING_SIGNALS job if no pending job exists.
    """
    from ..constants import JOB_COLLECT_HIRING_SIGNALS

    now = int(time.time())

    pending_count = await run_db(get_pending_job_count, None, JOB_COLLECT_HIRING_SIGNALS)
    if pending_count > 0:
        return

    await run_db(
        create_scheduler_job,
        campaign_id=None,
        job_type=JOB_COLLECT_HIRING_SIGNALS,
        scheduled_at=now,
    )
    logger.debug("Scheduled hiring signal collection")


async def plan_news_signal_collection() -> None:
    """Schedule news/funding signal collection from SERPER API.

    Called every 4 hours by the scheduler engine. Creates one
    JOB_COLLECT_NEWS_SIGNALS job if no pending job exists.
    """
    from ..constants import JOB_COLLECT_NEWS_SIGNALS

    now = int(time.time())

    pending_count = await run_db(get_pending_job_count, None, JOB_COLLECT_NEWS_SIGNALS)
    if pending_count > 0:
        return

    await run_db(
        create_scheduler_job,
        campaign_id=None,
        job_type=JOB_COLLECT_NEWS_SIGNALS,
        scheduled_at=now,
    )
    logger.debug("Scheduled news signal collection")


async def plan_company_page_collection() -> None:
    """Schedule company page engagement signal collection.

    Called every 1 hour by the scheduler engine. Creates one
    JOB_COLLECT_COMPANY_PAGE job if no pending job exists.
    """
    from ..constants import JOB_COLLECT_COMPANY_PAGE

    now = int(time.time())

    pending_count = await run_db(get_pending_job_count, None, JOB_COLLECT_COMPANY_PAGE)
    if pending_count > 0:
        return

    await run_db(
        create_scheduler_job,
        campaign_id=None,
        job_type=JOB_COLLECT_COMPANY_PAGE,
        scheduled_at=now,
    )
    logger.debug("Scheduled company page engagement collection")


async def plan_company_follower_collection() -> None:
    """Schedule company follower signal collection.

    Called every 4 hours by the scheduler engine. Creates one
    JOB_COLLECT_COMPANY_FOLLOWERS job if no pending job exists.
    """
    from ..constants import JOB_COLLECT_COMPANY_FOLLOWERS

    now = int(time.time())

    pending_count = await run_db(get_pending_job_count, None, JOB_COLLECT_COMPANY_FOLLOWERS)
    if pending_count > 0:
        return

    await run_db(
        create_scheduler_job,
        campaign_id=None,
        job_type=JOB_COLLECT_COMPANY_FOLLOWERS,
        scheduled_at=now,
    )
    logger.debug("Scheduled company follower collection")


async def plan_post_intent_classification() -> None:
    """Schedule post content intent classification (Phase 5).

    Called every 30 minutes. Classifies prospect posts for granular
    buyer intent signals (pain_point, tech_evaluation, budget, seeking_recs).
    """
    from ..constants import JOB_CLASSIFY_POST_INTENT

    now = int(time.time())

    pending_count = await run_db(get_pending_job_count, None, JOB_CLASSIFY_POST_INTENT)
    if pending_count > 0:
        return

    await run_db(
        create_scheduler_job,
        campaign_id=None,
        job_type=JOB_CLASSIFY_POST_INTENT,
        scheduled_at=now,
    )
    logger.debug("Scheduled post intent classification")


async def plan_comment_mining() -> None:
    """Schedule comment mining from competitor/industry posts (Phase 5).

    Called every 2 hours. Mines comments from high-engagement posts
    to discover new leads matching campaign ICPs.
    """
    from ..constants import JOB_MINE_COMMENTS

    now = int(time.time())

    pending_count = await run_db(get_pending_job_count, None, JOB_MINE_COMMENTS)
    if pending_count > 0:
        return

    await run_db(
        create_scheduler_job,
        campaign_id=None,
        job_type=JOB_MINE_COMMENTS,
        scheduled_at=now,
    )
    logger.debug("Scheduled comment mining")


async def plan_compound_intent_detection() -> None:
    """Schedule compound intent detection — stack weak signals into strong events.

    Called every 30 minutes by the scheduler engine. Creates one
    JOB_DETECT_COMPOUND_INTENT job if no pending job exists.
    """
    from ..constants import JOB_DETECT_COMPOUND_INTENT

    now = int(time.time())

    pending_count = await run_db(get_pending_job_count, None, JOB_DETECT_COMPOUND_INTENT)
    if pending_count > 0:
        return

    await run_db(
        create_scheduler_job,
        campaign_id=None,
        job_type=JOB_DETECT_COMPOUND_INTENT,
        scheduled_at=now,
    )
    logger.debug("Scheduled compound intent detection")


async def plan_decay_cycle() -> None:
    """Schedule signal decay cycle — expire old signals and recompute scores.

    Called every 6 hours by the scheduler engine. Creates one
    JOB_SIGNAL_DECAY_CYCLE job if no pending job exists.
    """
    from ..constants import JOB_SIGNAL_DECAY_CYCLE

    now = int(time.time())

    pending_count = await run_db(get_pending_job_count, None, JOB_SIGNAL_DECAY_CYCLE)
    if pending_count > 0:
        return

    await run_db(
        create_scheduler_job,
        campaign_id=None,
        job_type=JOB_SIGNAL_DECAY_CYCLE,
        scheduled_at=now,
    )
    logger.debug("Scheduled signal decay cycle")


async def plan_signal_rematch() -> None:
    """Schedule periodic re-matching of homeless signals to campaigns.

    Called every 1 hour. Re-evaluates signals that previously had no
    matching campaign — they may now match a newly created campaign.
    """
    from ..constants import JOB_REMATCH_SIGNALS

    now = int(time.time())

    pending_count = await run_db(get_pending_job_count, None, JOB_REMATCH_SIGNALS)
    if pending_count > 0:
        return

    await run_db(
        create_scheduler_job,
        campaign_id=None,
        job_type=JOB_REMATCH_SIGNALS,
        scheduled_at=now,
    )
    logger.debug("Scheduled signal rematch cycle")


async def plan_orphan_signal_backfill() -> None:
    """Schedule periodic backfill of orphan signals to known contacts.

    Called every 2 hours. Links signals (prospect_id IS NULL) whose
    linkedin_id now matches a contact in the contacts table.
    """
    from ..constants import JOB_BACKFILL_ORPHAN_SIGNALS

    now = int(time.time())

    pending_count = await run_db(get_pending_job_count, None, JOB_BACKFILL_ORPHAN_SIGNALS)
    if pending_count > 0:
        return

    await run_db(
        create_scheduler_job,
        campaign_id=None,
        job_type=JOB_BACKFILL_ORPHAN_SIGNALS,
        scheduled_at=now,
    )
    logger.debug("Scheduled orphan signal backfill")


# ──────────────────────────────────────────────
# Brand strategy planners (account-level)
# ──────────────────────────────────────────────


async def plan_brand_post() -> None:
    """Schedule a brand post job if the plan has a pending post action.

    Called every hour. Checks:
    1. Brand plan exists with pending post actions
    2. No pending brand_post job already (dedup)
    3. Daily brand post limit not reached
    """
    from ..constants import (
        BRAND_POST_DELAY_MAX,
        BRAND_POST_DELAY_MIN,
        JOB_BRAND_POST,
    )
    from ..services.brand_service import (
        get_next_pending_action_by_type,
        load_brand_plan,
    )

    plan = await run_db(load_brand_plan)
    if not plan:
        return

    # Check for pending post actions
    next_post = get_next_pending_action_by_type(plan, "post")
    if not next_post:
        return

    # Dedup: no pending brand_post jobs
    pending = await run_db(get_pending_job_count, None, JOB_BRAND_POST)
    if pending > 0:
        logger.debug("Already %d pending brand_post jobs", pending)
        return

    now = int(time.time())
    delay = random.randint(BRAND_POST_DELAY_MIN, BRAND_POST_DELAY_MAX)
    scheduled_at = now + delay

    await run_db(
        create_scheduler_job,
        campaign_id=None,
        job_type=JOB_BRAND_POST,
        scheduled_at=scheduled_at,
    )
    logger.debug("Scheduled brand post in %d min", delay // 60)


async def plan_brand_engagement() -> None:
    """Schedule a brand engagement job if the plan has a pending engagement action.

    Called every 4 hours. Checks:
    1. Brand plan exists with pending engagement actions
    2. No pending brand_engage job already (dedup)
    3. Combined daily engagement limit not exceeded
    """
    from ..constants import (
        BRAND_ENGAGE_DELAY_MAX,
        BRAND_ENGAGE_DELAY_MIN,
        JOB_BRAND_ENGAGE,
    )
    from ..services.brand_service import (
        get_next_pending_action_by_type,
        load_brand_plan,
    )

    plan = await run_db(load_brand_plan)
    if not plan:
        return

    next_engage = get_next_pending_action_by_type(plan, "engagement")
    if not next_engage:
        return

    # Dedup
    pending = await run_db(get_pending_job_count, None, JOB_BRAND_ENGAGE)
    if pending > 0:
        logger.debug("Already %d pending brand_engage jobs", pending)
        return

    now = int(time.time())
    delay = random.randint(BRAND_ENGAGE_DELAY_MIN, BRAND_ENGAGE_DELAY_MAX)
    scheduled_at = now + delay

    await run_db(
        create_scheduler_job,
        campaign_id=None,
        job_type=JOB_BRAND_ENGAGE,
        scheduled_at=scheduled_at,
    )
    logger.debug("Scheduled brand engagement in %d min", delay // 60)


async def plan_brand_lifecycle() -> None:
    """Manage brand strategy lifecycle: auto-analyze, auto-plan, re-analyze.

    Called every hour. Handles:
    1. No analysis → schedule brand_analyze (first-time auto-analyze)
    2. Analysis exists but no plan → schedule brand_analyze (will auto-plan)
    3. Plan complete + age >= 28 days → schedule brand_analyze (re-analyze cycle)
    """
    from ..constants import BRAND_REANALYZE_DAYS, JOB_BRAND_ANALYZE
    from ..db.queries import get_setting
    from ..services.brand_service import (
        get_brand_age_days,
        is_plan_complete,
        load_brand_analysis,
        load_brand_plan,
    )

    # Dedup
    pending = await run_db(get_pending_job_count, None, JOB_BRAND_ANALYZE)
    if pending > 0:
        return

    analysis = await run_db(load_brand_analysis)
    plan = await run_db(load_brand_plan)
    now = int(time.time())

    should_analyze = False

    # Check if campaign creation flagged a re-analysis (ICP changed)
    reanalyze_needed = await run_db(get_setting, "brand_reanalyze_needed", False)
    if reanalyze_needed:
        should_analyze = True
        logger.debug("Brand: ICP-driven re-analysis flagged by campaign creation")
    elif not analysis:
        # First-time: auto-analyze
        should_analyze = True
        logger.debug("Brand: no analysis found, scheduling auto-analyze")
    elif not plan:
        # Analysis exists but no plan — will auto-plan after analyzing
        should_analyze = True
        logger.debug("Brand: analysis exists but no plan, scheduling auto-plan")
    elif plan and is_plan_complete(plan):
        # Plan completed — check if 28 days have passed for re-analyze
        age_days = await run_db(get_brand_age_days)
        if age_days >= BRAND_REANALYZE_DAYS:
            should_analyze = True
            logger.debug("Brand: plan complete + %d days old, scheduling re-analyze", age_days)

    if should_analyze:
        await run_db(
            create_scheduler_job,
            campaign_id=None,
            job_type=JOB_BRAND_ANALYZE,
            scheduled_at=now + random.randint(300, 900),  # 5-15 min delay
        )


def _is_followup_due(
    candidate: dict[str, Any],
    tier: str,
    custom_schedule: list[int] | None = None,
) -> bool:
    """Check if a follow-up is due based on the schedule.

    Uses custom_schedule if provided (from per-campaign config),
    otherwise PRO_FOLLOWUP_SCHEDULE_DAYS for Pro tier: [1, 7, 14, 21, 28].
    Free tier: simpler check (just needs to have been connected for >= 1 day).

    Args:
        candidate: Outreach candidate from get_followup_candidates()
        tier: User's tier ('free' or 'pro')
        custom_schedule: Optional per-campaign follow-up schedule in days.

    Returns:
        True if the follow-up is due now.
    """
    followup_count = candidate.get("followup_count", 0)
    # Use accepted_at (set once on connection) instead of updated_at
    # (which resets on every warm-up action, preventing follow-ups from firing)
    outreach_updated = candidate.get("accepted_at") or candidate.get("outreach_updated_at", 0)

    if not outreach_updated:
        return False

    now = int(time.time())
    days_since = (now - outreach_updated) // 86400

    schedule = custom_schedule or (PRO_FOLLOWUP_SCHEDULE_DAYS if tier == TIER_PRO else None)

    if schedule and followup_count > 0:
        schedule_idx = min(followup_count, len(schedule) - 1)
        required_days = schedule[schedule_idx]
        return days_since >= required_days
    else:
        # First follow-up (any tier) or free tier without custom schedule
        return days_since >= 1


# ──────────────────────────────────────────────
# Communication Strategist: plan from daily strategy
# ──────────────────────────────────────────────

async def plan_from_daily_strategy(campaign_id: str) -> None:
    """Execute today's daily strategy plans for a campaign.

    Called every 15 min by the scheduler engine. Reads prospect_daily_plans
    for today, finds unexecuted actions whose timing is right, and creates
    scheduler_jobs for them.

    This is the "output side" of the Communication Strategist — it converts
    AI-generated plans into concrete scheduler jobs.
    """
    from ..services.communication_strategist import execute_planned_actions

    jobs_created = await execute_planned_actions(campaign_id)
    if jobs_created > 0:
        logger.info(
            "Strategy plans: scheduled %d jobs for campaign %s",
            jobs_created,
            campaign_id,
        )


# ──────────────────────────────────────────────
# Campaign auto-refill: top up prospects via LinkedIn search
# ──────────────────────────────────────────────

async def plan_campaign_refill() -> None:
    """Schedule campaign refill — search for more prospects when campaigns run low.

    Called every hour by the scheduler engine. Creates one
    JOB_CAMPAIGN_REFILL job if none pending.
    """
    from ..constants import JOB_CAMPAIGN_REFILL

    now = int(time.time())

    pending_count = await run_db(get_pending_job_count, None, JOB_CAMPAIGN_REFILL)
    if pending_count > 0:
        logger.debug("Already %d pending campaign refill jobs", pending_count)
        return

    await run_db(
        create_scheduler_job,
        campaign_id=None,
        job_type=JOB_CAMPAIGN_REFILL,
        scheduled_at=now,
    )
    logger.debug("Scheduled campaign refill")


async def plan_backfill_profiles() -> None:
    """Schedule profile backfill if none pending.

    Called every 2 hours by the scheduler engine. Creates one
    JOB_BACKFILL_PROFILES job if none pending.
    """
    from ..constants import JOB_BACKFILL_PROFILES

    now = int(time.time())

    pending_count = await run_db(get_pending_job_count, None, JOB_BACKFILL_PROFILES)
    if pending_count > 0:
        logger.debug("Already %d pending profile backfill jobs", pending_count)
        return

    await run_db(
        create_scheduler_job,
        campaign_id=None,
        job_type=JOB_BACKFILL_PROFILES,
        scheduled_at=now,
    )
    logger.debug("Scheduled profile backfill")
