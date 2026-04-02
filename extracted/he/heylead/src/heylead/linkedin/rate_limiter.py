"""Proactive rate limiting — enforces daily caps to prevent LinkedIn bans.

Each action type has a hard daily cap defined in constants.py.
The scheduler checks caps BEFORE executing any action.
A total daily budget limits cumulative visible LinkedIn actions.

Also provides:
- Pacing helpers (delay between sends)
- Pending invitation cache + withdrawal utility
- Ban risk monitoring with graduated warnings
"""

from __future__ import annotations

import logging
import random
import time
from datetime import datetime, timedelta
from typing import Any

from .. import constants
from ..db import aio as db
from ..db.async_bridge import run_db

logger = logging.getLogger(__name__)

# Block type constants
BLOCK_NONE = ""
BLOCK_TIME = "time"
BLOCK_DAILY = "daily"
BLOCK_WEEKLY = "weekly"
BLOCK_PENDING = "pending"
BLOCK_TOTAL = "total_daily"

# Map action types to their daily cap constant and action_log patterns
_ACTION_CAP_MAP: dict[str, tuple[int, list[str]]] = {
    "invite": (
        constants.DAILY_CAP_INVITATIONS,
        ["engagement_invite", "outreach_status_change"],
    ),
    "follow": (
        constants.DAILY_CAP_FOLLOWS,
        ["engagement_follow"],
    ),
    "profile_view": (
        constants.DAILY_CAP_PROFILE_VIEWS,
        ["engagement_profile_view"],
    ),
    "comment": (
        constants.DAILY_CAP_COMMENTS,
        ["engagement_comment"],
    ),
    "react": (
        constants.DAILY_CAP_REACTIONS,
        ["engagement_react", "engagement_react_fallback"],
    ),
    "engage": (
        # engage = comment + react combined
        constants.DAILY_CAP_COMMENTS + constants.DAILY_CAP_REACTIONS,
        ["engagement_comment", "engagement_react", "engagement_react_fallback"],
    ),
    "dm": (
        constants.DAILY_CAP_DMS,
        ["dm_sent", "reply_sent"],
    ),
    "auto_reply": (
        constants.DAILY_CAP_AUTO_REPLIES,
        ["auto_reply_sent"],
    ),
    "followup": (
        constants.DAILY_CAP_DMS,
        ["dm_sent", "reply_sent"],
    ),
    "withdraw": (
        constants.DAILY_CAP_WITHDRAWALS,
        ["stale_invite_withdrawn", "invite_withdrawn_to_free_spot"],
    ),
}

# Cache for today's action counts (refreshed every 60 seconds)
_daily_counts_cache: dict[str, Any] = {}
_CACHE_TTL = 60  # seconds


def _today_start_ts() -> int:
    """Unix timestamp for start of today (midnight local)."""
    import datetime as dt
    today = dt.date.today()
    return int(time.mktime(today.timetuple()))


async def _get_daily_action_counts() -> dict[str, int]:
    """Get today's action counts from actions_log, with 60s cache."""
    now = time.time()
    if (
        _daily_counts_cache.get("data") is not None
        and (now - _daily_counts_cache.get("fetched_at", 0)) < _CACHE_TTL
    ):
        return _daily_counts_cache["data"]

    from ..db.queries import get_actions_taken
    actions = await run_db(get_actions_taken, 24)

    # Flatten to {action_type: success_count}
    counts: dict[str, int] = {}
    for action_type, breakdown in actions.items():
        # Count only successful actions
        success = breakdown.get("success", 0)
        counts[action_type] = success

    # Also get engagement counts from engagements table (more accurate)
    from ..db.queries import get_daily_engagement_counts_all
    eng_counts = await run_db(get_daily_engagement_counts_all)
    for action_type, count in eng_counts.items():
        key = f"engagement_{action_type}"
        counts[key] = max(counts.get(key, 0), count)

    # Get pending engagement counts too
    from ..db.queries import get_daily_engagement_counts_pending
    pend_counts = await run_db(get_daily_engagement_counts_pending)
    for action_type, count in pend_counts.items():
        key = f"engagement_{action_type}"
        counts[key] = counts.get(key, 0) + count

    _daily_counts_cache["data"] = counts
    _daily_counts_cache["fetched_at"] = now
    return counts


def _count_for_action(counts: dict[str, int], patterns: list[str]) -> int:
    """Sum counts matching any of the given action_type patterns."""
    total = 0
    for pattern in patterns:
        total += counts.get(pattern, 0)
    return total


def _total_visible_actions(counts: dict[str, int]) -> int:
    """Sum all visible LinkedIn actions for today."""
    visible_patterns = [
        "engagement_follow", "engagement_profile_view",
        "engagement_comment", "engagement_react", "engagement_react_fallback",
        "dm_sent", "reply_sent", "auto_reply_sent",
        "stale_invite_withdrawn", "invite_withdrawn_to_free_spot",
    ]
    total = _count_for_action(counts, visible_patterns)
    # Add invitations (tracked differently via outreach_status_change)
    # Count from engagements table for invite type if available
    total += counts.get("engagement_invite", 0)
    # Also count from rate_limits table
    from ..db.queries import get_rate_limit_today
    try:
        rl = get_rate_limit_today()
        total += rl.get("sent", 0) if isinstance(rl, dict) else 0
    except Exception:
        pass
    return total


async def check_daily_cap(action_type: str) -> tuple[bool, int, int, str]:
    """Check if an action type is within its daily cap.

    Args:
        action_type: One of "invite", "follow", "profile_view", "comment",
                     "react", "engage", "dm", "auto_reply", "followup", "withdraw"

    Returns:
        (can_proceed, current_count, cap, block_reason)
    """
    cap_info = _ACTION_CAP_MAP.get(action_type)
    if not cap_info:
        # Unknown action type — allow but log
        logger.debug("No daily cap defined for action type: %s", action_type)
        return True, 0, 999, BLOCK_NONE

    cap, patterns = cap_info
    counts = await _get_daily_action_counts()
    current = _count_for_action(counts, patterns)

    # Check action-specific cap
    if current >= cap:
        logger.warning(
            "Daily cap reached for %s: %d/%d — blocking action",
            action_type, current, cap,
        )
        return False, current, cap, BLOCK_DAILY

    # Check total daily budget
    total = _total_visible_actions(counts)
    if total >= constants.DAILY_CAP_TOTAL_ACTIONS:
        logger.warning(
            "Total daily action budget exhausted: %d/%d — blocking %s",
            total, constants.DAILY_CAP_TOTAL_ACTIONS, action_type,
        )
        return False, total, constants.DAILY_CAP_TOTAL_ACTIONS, BLOCK_TOTAL

    # Ban risk warnings
    pct = current / cap if cap > 0 else 0
    if pct >= constants.BAN_RISK_CRITICAL_PCT:
        logger.warning(
            "BAN RISK CRITICAL: %s at %.0f%% of daily cap (%d/%d)",
            action_type, pct * 100, current, cap,
        )
    elif pct >= constants.BAN_RISK_WARNING_PCT:
        logger.info(
            "Ban risk warning: %s at %.0f%% of daily cap (%d/%d)",
            action_type, pct * 100, current, cap,
        )

    total_pct = total / constants.DAILY_CAP_TOTAL_ACTIONS if constants.DAILY_CAP_TOTAL_ACTIONS > 0 else 0
    if total_pct >= constants.BAN_RISK_CRITICAL_PCT:
        logger.warning(
            "BAN RISK CRITICAL: total actions at %.0f%% (%d/%d)",
            total_pct * 100, total, constants.DAILY_CAP_TOTAL_ACTIONS,
        )
    elif total_pct >= constants.BAN_RISK_WARNING_PCT:
        logger.info(
            "Ban risk warning: total actions at %.0f%% (%d/%d)",
            total_pct * 100, total, constants.DAILY_CAP_TOTAL_ACTIONS,
        )

    return True, current, cap, BLOCK_NONE


async def get_daily_cap_summary() -> dict[str, dict[str, int]]:
    """Get a summary of all daily caps and current usage.

    Returns: {action_type: {"current": N, "cap": N, "remaining": N, "pct": N}}
    """
    counts = await _get_daily_action_counts()
    summary: dict[str, dict[str, int]] = {}

    for action_type, (cap, patterns) in _ACTION_CAP_MAP.items():
        if action_type == "engage":
            continue  # Skip composite — show comment/react separately
        current = _count_for_action(counts, patterns)
        summary[action_type] = {
            "current": current,
            "cap": cap,
            "remaining": max(0, cap - current),
            "pct": int((current / cap * 100) if cap > 0 else 0),
        }

    total = _total_visible_actions(counts)
    summary["_total"] = {
        "current": total,
        "cap": constants.DAILY_CAP_TOTAL_ACTIONS,
        "remaining": max(0, constants.DAILY_CAP_TOTAL_ACTIONS - total),
        "pct": int((total / constants.DAILY_CAP_TOTAL_ACTIONS * 100)
                    if constants.DAILY_CAP_TOTAL_ACTIONS > 0 else 0),
    }
    return summary


def invalidate_daily_cache() -> None:
    """Force refresh of daily counts on next check (call after action succeeds)."""
    _daily_counts_cache.clear()


# ──────────────────────────────────────────────
# Backwards-compatible API (used by existing callers)
# ──────────────────────────────────────────────

async def can_send_now(
    *, skip_time_check: bool = False
) -> tuple[bool, str, str]:
    """Check if we can send an invitation now (respects daily cap)."""
    can, current, cap, block = await check_daily_cap("invite")
    if not can:
        return False, f"Daily invitation cap reached ({current}/{cap})", block
    return True, "", BLOCK_NONE


async def can_send_email_now() -> tuple[bool, str]:
    """Always returns True — no proactive email limits."""
    return True, ""


async def increment_email_sent() -> None:
    """Track an email send in the email rate limits table."""
    from ..db.queries import increment_email_sent as _inc
    await run_db(_inc)


def get_next_delay() -> int:
    """Get randomized delay in seconds for the next send."""
    min_secs = constants.MIN_DELAY_MINUTES * 60
    max_secs = constants.MAX_DELAY_MINUTES * 60
    return random.randint(min_secs, max_secs)


async def update_limits_after_send(blocked: bool = False) -> int:
    """Invalidate cache after a send. Returns 0."""
    invalidate_daily_cache()
    return 0


async def check_engagement_budget(
    engagement_type: str = "",
) -> tuple[bool, int, int]:
    """Check engagement budget using daily caps.

    Maps engagement_type to the appropriate cap check.
    Returns (has_budget, current, limit).
    """
    # Map engagement_type to our cap action types
    type_map = {
        "comment": "comment",
        "react": "react",
        "follow": "follow",
        "profile_view": "profile_view",
        "view": "profile_view",
        "endorse": "follow",  # shares follow cap
        "engage": "engage",
        "": "engage",  # default
    }
    action = type_map.get(engagement_type, "engage")
    can, current, cap, _ = await check_daily_cap(action)
    return can, current, cap


async def check_pending_limit(
    client: Any, account_id: str
) -> tuple[bool, str, str]:
    """Always returns can_send=True — no proactive pending limit."""
    return True, "", BLOCK_NONE


async def estimate_weekly_limit_reset() -> tuple[bool, int, str]:
    """Always returns not-at-limit — no weekly cap."""
    return False, 0, ""


async def _get_effective_caps() -> tuple[int, int]:
    """Return (weekly_cap, daily_max) for health score calculation."""
    return 200, 30


# ──────────────────────────────────────────────
# Pending invitation cache + withdrawal (utility, not rate limiting)
# ──────────────────────────────────────────────

_pending_cache: dict[str, Any] = {}


async def get_cached_pending_invitations(
    client: Any, account_id: str
) -> tuple[int, list[dict]]:
    """Return (count, invitation_list) with a 5-minute TTL cache."""
    now = time.time()
    fetched_at = _pending_cache.get("fetched_at", 0)
    if (
        _pending_cache.get("invitations") is not None
        and (now - fetched_at) < constants.PENDING_CACHE_TTL_SECONDS
    ):
        invitations = _pending_cache["invitations"]
        return len(invitations), invitations

    try:
        invitations = await client.get_pending_invitations(account_id)
    except Exception as e:
        logger.warning("Failed to fetch pending invitations: %s", e)
        if _pending_cache.get("invitations") is not None:
            invitations = _pending_cache["invitations"]
            return len(invitations), invitations
        return 0, []

    _pending_cache["invitations"] = invitations
    _pending_cache["fetched_at"] = now
    return len(invitations), invitations


def invalidate_pending_cache() -> None:
    """Clear the pending invitation cache. Call after send or withdrawal."""
    _pending_cache.clear()


async def withdraw_oldest_to_free_spot(
    client: Any, account_id: str
) -> dict[str, Any]:
    """Withdraw the oldest pending invitation to free a spot."""
    # Check withdrawal daily cap first
    can, current, cap, _ = await check_daily_cap("withdraw")
    if not can:
        logger.warning("Daily withdrawal cap reached (%d/%d), skipping", current, cap)
        return {"success": False, "error": f"Daily withdrawal cap reached ({current}/{cap})"}

    count, invitations = await get_cached_pending_invitations(
        client, account_id
    )
    if not invitations:
        return {"success": False, "error": "No pending invitations to withdraw"}

    # Parse timestamps and sort oldest-first
    now_ts = int(time.time())
    candidates = []
    for inv in invitations:
        inv_time = (
            inv.get("parsed_datetime")
            or inv.get("timestamp")
            or inv.get("created_at")
            or 0
        )
        if isinstance(inv_time, str):
            try:
                inv_time = int(
                    datetime.fromisoformat(
                        inv_time.replace("Z", "+00:00")
                    ).timestamp()
                )
            except (ValueError, TypeError):
                inv_time = 0
        inv_id = inv.get("id") or inv.get("invitation_id") or ""
        if inv_id and inv_time:
            candidates.append((inv_time, inv_id, inv))

    if not candidates:
        return {"success": False, "error": "No valid invitation candidates"}

    candidates.sort(key=lambda x: x[0])  # oldest first
    oldest_time, oldest_id, oldest_inv = candidates[0]
    days_old = (now_ts - oldest_time) // 86400
    name = oldest_inv.get("invited_user") or oldest_inv.get("name") or ""

    try:
        result = await client.withdraw_invitation(account_id, oldest_id)
    except Exception as e:
        logger.warning("Failed to withdraw invitation %s: %s", oldest_id, e)
        return {"success": False, "error": str(e)}

    if result.get("success"):
        invalidate_pending_cache()
        invalidate_daily_cache()
        await db.log_action(
            "invite_withdrawn_to_free_spot",
            result="success",
            details={
                "invitation_id": oldest_id,
                "days_old": days_old,
                "name": name,
                "pending_count_before": count,
            },
        )
        logger.info(
            "Withdrew oldest invitation %s (%d days old, %s) to free spot",
            oldest_id,
            days_old,
            name,
        )
        return {
            "success": True,
            "invitation_id": oldest_id,
            "days_old": days_old,
            "name": name,
        }

    error = result.get("error", "Unknown error")
    logger.warning("Failed to withdraw invitation %s: %s", oldest_id, error)
    return {"success": False, "error": error}
