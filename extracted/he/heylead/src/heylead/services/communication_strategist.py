"""Communication Strategist — AI-planned daily action plans per prospect.

Replaces the hardcoded warm-up sequence with dynamic, LLM-generated daily plans.
Runs once per day (~6 AM user time) via JOB_DAILY_STRATEGY, with plan execution
checked every 15 min via JOB_EXECUTE_STRATEGY_PLANS.

Integration flow:
  Daily:
    run_daily_strategy() →
      _evaluate_yesterday_plans()     # feedback loop
      for each active campaign:
        _collect_prospect_context()   # gather data
        _batch_plan_actions()         # LLM call per batch of 50
        _store_daily_plans()          # persist to DB

  Every 15 min:
    execute_planned_actions(campaign_id) →
      read today's plans
      find next unexecuted action with right timing
      create scheduler_job → existing executor handles it
"""

from __future__ import annotations

import json
import logging
import random
import time
from datetime import datetime, timezone
from typing import Any

from ..constants import (
    STRATEGIST_AVAILABLE_ACTIONS,
    STRATEGIST_BATCH_SIZE,
    STRATEGIST_FEEDBACK_LOOKBACK_DAYS,
    STRATEGIST_FEEDBACK_TOP_N,
    STRATEGIST_MAX_ACTIONS_PER_DAY,
    STRATEGIST_MAX_PROSPECTS,
    JOB_ENGAGE,
    JOB_ENDORSE,
    JOB_FOLLOW,
    JOB_FOLLOWUP,
    JOB_INVITE,
    JOB_PROFILE_VIEW,
    JOB_SEND_DM,
)
from ..db.async_bridge import run_db

logger = logging.getLogger(__name__)


# ──────────────────────────────────────────────
# Main Entry Point (daily)
# ──────────────────────────────────────────────

async def run_daily_strategy() -> dict[str, Any]:
    """Main entry point. Runs once per day. Generates daily plans for all active campaigns."""
    summary: dict[str, Any] = {
        "plans_created": 0,
        "plans_evaluated": 0,
        "campaigns_processed": 0,
        "llm_calls": 0,
        "fallback_used": 0,
        "errors": [],
    }

    # Phase 1: Evaluate yesterday's plans (feedback loop)
    try:
        evaluated = await _evaluate_yesterday_plans()
        summary["plans_evaluated"] = evaluated
    except Exception as e:
        logger.error("Plan evaluation failed: %s", e)
        summary["errors"].append(f"evaluation: {e}")

    # Phase 2: Generate today's plans for all active autopilot campaigns
    from ..db.queries import list_campaigns

    campaigns = await run_db(list_campaigns, status="active")
    for campaign in campaigns:
        if campaign.get("mode") != "autopilot":
            continue

        campaign_id = campaign["id"]
        try:
            created = await _plan_campaign_prospects(campaign, summary)
            summary["plans_created"] += created
            summary["campaigns_processed"] += 1
        except Exception as e:
            logger.error("Strategy planning failed for campaign %s: %s", campaign_id, e)
            summary["errors"].append(f"campaign {campaign_id[:8]}: {e}")

    logger.info(
        "Daily strategy complete: %d plans, %d evaluated, %d campaigns, %d LLM calls",
        summary["plans_created"],
        summary["plans_evaluated"],
        summary["campaigns_processed"],
        summary["llm_calls"],
    )
    return summary


# ──────────────────────────────────────────────
# Campaign-Level Planning
# ──────────────────────────────────────────────

async def _plan_campaign_prospects(campaign: dict, summary: dict) -> int:
    """Generate daily plans for all prospects in a single campaign."""
    from ..db.strategist_queries import (
        get_feedback_data,
        get_prospects_needing_plans,
        save_daily_plan,
    )

    campaign_id = campaign["id"]
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    # Get prospects that need plans
    prospects = await run_db(get_prospects_needing_plans, campaign_id)
    if not prospects:
        return 0

    # Cap at STRATEGIST_MAX_PROSPECTS
    prospects = prospects[:STRATEGIST_MAX_PROSPECTS]

    # Get feedback from recent plans
    feedback = await run_db(
        get_feedback_data, STRATEGIST_FEEDBACK_LOOKBACK_DAYS, STRATEGIST_FEEDBACK_TOP_N
    )

    # Prepare campaign context (ICP, voice) — once per campaign
    campaign_context = _build_campaign_context(campaign)

    # Detect DM-only campaign (connections-only, no invitations)
    try:
        config = json.loads(campaign.get("config_json") or "{}")
    except (json.JSONDecodeError, TypeError):
        config = {}
    dm_only = not config.get("enable_invitations", True)

    # Batch processing
    created = 0
    for i in range(0, len(prospects), STRATEGIST_BATCH_SIZE):
        batch = prospects[i : i + STRATEGIST_BATCH_SIZE]
        try:
            plans = await _batch_plan_actions(batch, campaign_context, feedback, dm_only=dm_only)
            summary["llm_calls"] += 1

            for plan in plans:
                outreach_id = plan.get("outreach_id")
                if not outreach_id:
                    continue

                actions = plan.get("actions", [])

                # Validate: cap at STRATEGIST_MAX_ACTIONS_PER_DAY
                actions = actions[:STRATEGIST_MAX_ACTIONS_PER_DAY]

                # Validate action types
                actions = [
                    a for a in actions if a.get("action_type") in STRATEGIST_AVAILABLE_ACTIONS
                ]

                # For DM-only campaigns, rewrite any "invite" actions the LLM
                # may have generated into "send_dm" — belt-and-suspenders guard.
                if dm_only:
                    for a in actions:
                        if a.get("action_type") == "invite":
                            a["action_type"] = "send_dm"
                            a["rationale"] = (a.get("rationale", "") + " [rewritten: dm_only campaign]").strip()
                else:
                    # Regular campaigns must NOT use send_dm — the prospect may
                    # not be a 1st-degree connection yet.  Rewrite to "invite".
                    for a in actions:
                        if a.get("action_type") == "send_dm":
                            a["action_type"] = "invite"
                            a["rationale"] = (a.get("rationale", "") + " [rewritten: not dm_only campaign]").strip()

                if not actions:
                    actions = [
                        {
                            "action_type": "skip_today",
                            "priority": 1,
                            "timing_preference": "anytime",
                            "params": {},
                            "rationale": "LLM returned no valid actions",
                        }
                    ]

                await run_db(save_daily_plan, outreach_id, campaign_id, today, actions, "llm")
                created += 1

        except Exception as e:
            logger.warning("LLM batch planning failed, falling back to heuristic: %s", e)
            # FALLBACK: Generate heuristic plans for this batch
            for prospect in batch:
                fallback_actions = _generate_fallback_plan(prospect, dm_only=dm_only)
                await run_db(
                    save_daily_plan,
                    prospect["outreach_id"],
                    campaign_id,
                    today,
                    fallback_actions,
                    "fallback",
                )
                created += 1
                summary["fallback_used"] += 1

    return created


# ──────────────────────────────────────────────
# LLM Batch Call
# ──────────────────────────────────────────────

async def _batch_plan_actions(
    prospects: list[dict],
    campaign_context: dict,
    feedback: dict,
    *,
    dm_only: bool = False,
) -> list[dict]:
    """Call LLM to generate daily plans for a batch of ~50 prospects."""
    from ..ai.strategist_prompts import (
        STRATEGIST_SYSTEM,
        STRATEGIST_BATCH_PROMPT,
        format_feedback_section,
        format_prospect_for_llm,
    )

    # Build the prompt
    prospects_section = "\n".join(format_prospect_for_llm(p) for p in prospects)
    feedback_section = format_feedback_section(feedback)

    # Add DM-only campaign context so the LLM plans send_dm instead of invite
    dm_only_section = ""
    if dm_only:
        dm_only_section = (
            "\n\n## IMPORTANT: DM-Only Campaign\n"
            "This is a connections-only campaign. All prospects are existing 1st-degree connections.\n"
            "- Use 'send_dm' instead of 'invite' for all pending/connected prospects\n"
            "- Do NOT plan 'invite' actions — they are already connected\n"
            "- Skip warm-up actions (profile_view, follow, endorse) — not needed for existing connections\n"
            "- Focus on send_dm and followup actions only"
        )

    prompt = STRATEGIST_BATCH_PROMPT.format(
        campaign_name=campaign_context.get("name", ""),
        icp_summary=campaign_context.get("icp_summary", ""),
        voice_summary=campaign_context.get("voice_summary", ""),
        feedback_section=feedback_section,
        prospect_count=len(prospects),
        prospects_section=prospects_section,
    ) + dm_only_section

    # Try backend LLM proxy
    from ..config import is_backend_mode, has_local_llm_key

    if is_backend_mode() and not has_local_llm_key():
        from ..linkedin.factory import get_linkedin_client

        client = get_linkedin_client()
        try:
            result = await client.plan_daily_actions(prompt)
        finally:
            await client.close()
        return result.get("plans", [])

    # Fallback: local BYOK
    if has_local_llm_key():
        from ..ai.llm import call_llm

        raw = await run_db(call_llm, prompt, system=STRATEGIST_SYSTEM, temperature=0.3)
        return _parse_plans_json(raw)

    # No LLM available — will be caught by caller and fall back to heuristic
    raise RuntimeError("No LLM available (no backend mode and no local API key)")


def _parse_plans_json(raw: str) -> list[dict]:
    """Parse LLM JSON response, with repair for markdown fences."""
    import re

    # Try direct parse
    try:
        parsed = json.loads(raw)
        return parsed.get("plans", [])
    except (json.JSONDecodeError, AttributeError):
        pass

    # Try extracting from markdown code blocks
    match = re.search(r"```(?:json)?\s*([\s\S]*?)```", raw)
    if match:
        try:
            parsed = json.loads(match.group(1))
            return parsed.get("plans", [])
        except (json.JSONDecodeError, AttributeError):
            pass

    logger.warning("Failed to parse strategist LLM output")
    return []


# ──────────────────────────────────────────────
# Heuristic Fallback
# ──────────────────────────────────────────────

def _generate_fallback_plan(prospect: dict, *, dm_only: bool = False) -> list[dict]:
    """Generate a heuristic plan when LLM is unavailable.

    Mirrors the existing hardcoded sequence logic but returns it as a plan.
    When *dm_only* is True (connections-only campaigns), plans send_dm instead
    of invite and skips warm-up — prospects are already connected.
    """
    status = prospect.get("status", "pending")
    engagement_count = prospect.get("engagement_count", 0)
    engagement_types = (prospect.get("engagement_types") or "").split(",")
    engagement_types = [t.strip() for t in engagement_types if t.strip()]

    actions: list[dict] = []

    if status in ("pending", "connected") and dm_only:
        # DM-only campaign: send DM directly, no warm-up needed
        actions.append({
            "action_type": "send_dm",
            "priority": 1,
            "timing_preference": "morning",
            "params": {},
            "rationale": "Core outreach: send DM to existing connection",
        })

    elif status == "pending":
        has_profile_view = "profile_view" in engagement_types or "view" in engagement_types
        has_follow = "follow" in engagement_types
        has_endorse = "endorse" in engagement_types
        has_engagement = any(t in engagement_types for t in ("comment", "react"))

        # Core action: always present — warm-up must never delay outreach.
        # timing_preference="anytime" ensures the invite is never deferred
        # to the next day when a warm-up action consumes the morning window.
        actions.append({
            "action_type": "invite",
            "priority": 2,
            "timing_preference": "anytime",
            "params": {},
            "rationale": "Core outreach: send invitation",
        })

        # Optional warm-up: one action alongside (not before) core outreach
        warmup = None
        if not has_profile_view:
            warmup = {"action_type": "profile_view", "rationale": "Warm-up: profile view notification", "timing_preference": "morning"}
        elif not has_follow:
            warmup = {"action_type": "follow", "rationale": "Warm-up: follow notification", "timing_preference": "morning"}
        elif not has_endorse:
            warmup = {"action_type": "endorse", "rationale": "Warm-up: endorse skills", "timing_preference": "afternoon"}
        elif not has_engagement:
            warmup = {"action_type": "engage_comment", "rationale": "Warm-up: engage with post", "timing_preference": "afternoon"}

        if warmup:
            warmup.update({"priority": 1, "params": {}})
            actions.insert(0, warmup)

    elif status == "connected":
        actions.append({
            "action_type": "followup",
            "priority": 1,
            "timing_preference": "morning",
            "params": {},
            "rationale": "Connected prospect: follow-up DM",
        })

    elif status in ("replied", "messaged"):
        actions.append({
            "action_type": "skip_today",
            "priority": 1,
            "timing_preference": "anytime",
            "params": {},
            "rationale": "Active conversation: let human manage",
        })

    elif status == "invited":
        if engagement_count < 3:
            actions.append({
                "action_type": "engage_react",
                "priority": 1,
                "timing_preference": "afternoon",
                "params": {},
                "rationale": "Keep warm while waiting for invite acceptance",
            })
        else:
            actions.append({
                "action_type": "skip_today",
                "priority": 1,
                "timing_preference": "anytime",
                "params": {},
                "rationale": "Enough engagement, waiting for acceptance",
            })

    if not actions:
        actions.append({
            "action_type": "skip_today",
            "priority": 1,
            "timing_preference": "anytime",
            "params": {},
            "rationale": "No action needed in current state",
        })

    return actions


# ──────────────────────────────────────────────
# Plan Execution (every 15 min)
# ──────────────────────────────────────────────

async def execute_planned_actions(campaign_id: str) -> int:
    """Read today's plans and create scheduler_jobs for unexecuted actions.

    Called every 15 min by the engine. Returns count of jobs created.
    """
    from ..db.queries import create_scheduler_job, get_pending_job_count, get_pending_outreach_job
    from ..db.strategist_queries import get_campaign_daily_plans, mark_action_skipped

    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    plans = await run_db(get_campaign_daily_plans, campaign_id, today)

    now = int(time.time())
    current_hour = datetime.now(timezone.utc).hour
    jobs_created = 0

    for plan in plans:
        outreach_id = plan["outreach_id"]
        planned = plan["planned_actions"]
        executed = plan["executed_actions"]
        executed_types = {e["action_type"] for e in executed}

        for action in planned:
            action_type = action.get("action_type")
            if action_type in executed_types:
                continue  # Already done or skipped — no re-logging
            if action_type == "skip_today":
                continue  # Intentional — no logging needed

            # Check timing preference
            timing = action.get("timing_preference", "anytime")
            if not _is_right_timing(timing, current_hour):
                continue  # Will be retried in the right window — don't log as skip

            # Map strategy action_type to job_type
            job_type = _map_action_to_job_type(action_type)
            if not job_type:
                await run_db(mark_action_skipped, outreach_id, today, action_type,
                             f"unmapped_action_type: {action_type}")
                continue

            # Dedup: skip if this specific outreach already has a pending/running job
            if await run_db(get_pending_outreach_job, outreach_id, job_type):
                await run_db(mark_action_skipped, outreach_id, today, action_type,
                             f"duplicate_job: pending {job_type} already exists")
                continue

            # Dedup: don't flood the campaign queue
            pending = await run_db(get_pending_job_count, campaign_id, job_type)
            if pending > 2:
                await run_db(mark_action_skipped, outreach_id, today, action_type,
                             f"queue_full: {pending} pending {job_type} jobs")
                continue

            # Create scheduler job with randomized delay (5-20 min)
            delay = random.randint(300, 1200)
            await run_db(
                create_scheduler_job,
                campaign_id=campaign_id,
                job_type=job_type,
                scheduled_at=now + delay + (jobs_created * random.randint(180, 420)),
                outreach_id=outreach_id,
            )
            jobs_created += 1

            # Core outreach (invite, send_dm, followup, etc.) is never gated
            # behind warm-up — keep iterating so both warm-up AND core get
            # scheduled in the same cycle.  Warm-up actions still pace at
            # one-per-cycle per prospect.
            _CORE_JOB_TYPES = {"invite", "send_dm", "followup", "auto_reply", "discover"}
            if job_type not in _CORE_JOB_TYPES:
                break  # One warm-up action at a time per prospect

    return jobs_created


# ──────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────

def _map_action_to_job_type(action_type: str) -> str | None:
    """Map strategy action type to existing scheduler job type."""
    mapping = {
        "profile_view": JOB_PROFILE_VIEW,
        "follow": JOB_FOLLOW,
        "endorse": JOB_ENDORSE,
        "engage_comment": JOB_ENGAGE,
        "engage_react": JOB_ENGAGE,
        "invite": JOB_INVITE,
        "send_dm": JOB_SEND_DM,
        "followup": JOB_FOLLOWUP,
        "voice_memo": JOB_FOLLOWUP,
    }
    return mapping.get(action_type)


def _is_right_timing(timing: str, current_utc_hour: int) -> bool:
    """Check if the current time matches the timing preference.

    NOTE: Simplified to UTC. Production should use prospect's local timezone.
    """
    if timing == "anytime":
        return True
    if timing == "morning" and 8 <= current_utc_hour < 12:
        return True
    if timing == "afternoon" and 12 <= current_utc_hour < 16:
        return True
    if timing == "evening" and 16 <= current_utc_hour < 19:
        return True
    return False


async def _evaluate_yesterday_plans() -> int:
    """Score yesterday's plans based on outcomes. Returns count scored."""
    from ..db.strategist_queries import score_yesterday_plans

    return await run_db(score_yesterday_plans)


def _build_campaign_context(campaign: dict) -> dict:
    """Build concise campaign context for the LLM prompt."""
    icp_summary = ""
    try:
        icp = json.loads(campaign.get("icp_json") or "{}")
        if isinstance(icp, dict):
            personas = icp.get("personas", [])
            if personas:
                icp_summary = "; ".join(
                    f"{p.get('title', '')} at {p.get('company_type', '')}" for p in personas[:3]
                )
    except Exception:
        pass

    from ..db.queries import get_setting

    voice = get_setting("voice_signature", {})
    voice_summary = ""
    if isinstance(voice, dict):
        voice_summary = voice.get("tone", "professional") + ", " + voice.get("style", "")

    return {
        "name": campaign.get("name", ""),
        "icp_summary": icp_summary[:200],
        "voice_summary": voice_summary[:100],
    }
