"""Tool 5: show_status — Dashboard in the chat.

Shows campaign stats, acceptance rate, reply rate, hot leads,
account health, and free tier usage.

The chat IS the dashboard. Forever.
"""

from __future__ import annotations

import json
import logging
from typing import Any

from .. import config
from ..config import get_tier
from ..constants import (
    FREE_MAX_CAMPAIGNS,
    FREE_MAX_ENGAGEMENTS,
    FREE_MAX_FOLLOWUPS,
    FREE_MONTHLY_INVITATIONS,
    FREE_MONTHLY_MESSAGES,
    PRO_MAX_FOLLOWUPS,
    TIER_PRO,
)
from ..db import aio as db
from ..db.async_bridge import run_db
from ..constants import SOURCE_LABELS
from ..formatter import conversion_rate_display, format_duration, progress_bar, prospect_link, stars
from ..services.health_score import compute_health_score, format_health_score

logger = logging.getLogger(__name__)


async def run_show_status(campaign_id: str = "") -> str:
    """Show outreach dashboard.

    If campaign_id is provided: show detailed stats for that campaign.
    If empty: show overview of all campaigns + account health.

    In backend mode: tries live stats from backend first, falls back to
    synced local DB, then raw local DB.
    """

    setup_done = await db.get_setting("setup_complete", False)
    if not setup_done:
        return (
            "👋 Welcome to HeyLead — your AI LinkedIn SDR!\n\n"
            "You haven't set up your profile yet. Let's fix that!\n\n"
            "Say 'set up my profile' or run setup_profile, and I'll walk you through "
            "connecting your LinkedIn account and configuring AI in about 2 minutes.\n\n"
            "After setup, you can:\n"
            "  → create_campaign('find me fintech CTOs') — find prospects\n"
            "  → generate_and_send() — craft personalized messages\n"
            "  → check_replies() — see who responded\n"
            "  → show_status() — your outreach dashboard"
        )

    # ── Backend mode: try live stats first, then sync ──
    backend_offline = False

    if config.is_backend_mode() and not campaign_id:
        try:
            from ..services.cloud_sync import BackendAuthError, fetch_live_stats
            live = await fetch_live_stats()
            if live and live.get("campaigns"):
                return await _show_overview_from_backend(live)
            elif live is not None:
                # Backend reachable but returned no campaigns — try syncing local state up
                try:
                    from ..services.cloud_sync import sync_to_cloud
                    await sync_to_cloud()
                except Exception:
                    pass
        except BackendAuthError:
            return _auth_error_message()
        except Exception as e:
            backend_offline = True
            logger.debug("Live stats failed, falling back to sync: %s", e)

        # Fallback: pull changes to update local DB before reading
        try:
            from ..services.cloud_sync import BackendAuthError, ensure_synced
            await ensure_synced()
        except BackendAuthError:
            return _auth_error_message()
        except Exception as e:
            backend_offline = True
            logger.debug("ensure_synced failed: %s", e)

    elif config.is_backend_mode() and campaign_id:
        # For campaign detail, just ensure synced before reading local
        try:
            from ..services.cloud_sync import BackendAuthError, ensure_synced
            await ensure_synced()
        except BackendAuthError:
            return _auth_error_message()
        except Exception as e:
            backend_offline = True
            logger.debug("ensure_synced failed: %s", e)

    # ── Specific campaign view ──
    if campaign_id:
        return await _show_campaign_detail(campaign_id)

    # ── Overview ──
    return await _show_overview(offline=backend_offline)


def _auth_error_message() -> str:
    """Return a user-facing message when the backend JWT is expired or invalid."""
    from ..constants import DEFAULT_BACKEND_URL, LOGIN_URL_PATH

    login_url = f"{DEFAULT_BACKEND_URL}{LOGIN_URL_PATH}"
    return (
        "⚠️ **Authentication expired**\n\n"
        "Your HeyLead session token has expired or is invalid.\n"
        "Your campaigns are still safe on the server — you just need to re-authenticate.\n\n"
        "**To fix:**\n"
        f"1. Open: {login_url}\n"
        "2. Sign in and copy your new token\n"
        "3. Run: setup_profile(backend_jwt='YOUR_NEW_TOKEN')\n\n"
        "After that, show_status() will work again."
    )


async def _show_overview(offline: bool = False) -> str:
    """Show overview of all campaigns + account health."""

    campaigns = await db.list_campaigns()
    tier = get_tier()
    rate_data = await db.get_rate_limit_today()
    usage = await db.get_monthly_usage()

    if offline and config.is_backend_mode():
        import time as _ts
        _last_pull = await db.get_setting("last_pull_timestamp", 0)
        if not isinstance(_last_pull, (int, float)):
            _last_pull = 0
        _age_s = int(_ts.time()) - int(_last_pull) if _last_pull else 0
        if _age_s > 300:
            output = [f"📊 **HeyLead Dashboard** (offline — last sync {_age_s // 60}m ago)\n"]
            output.append(f"⚠️ Data may be stale — backend unreachable, showing cached data\n")
        else:
            output = [f"📊 **HeyLead Dashboard** (cached — {_age_s}s old)\n"]
    else:
        output = ["📊 **HeyLead Dashboard**\n"]

    # ── Account Health ──
    # Use verified invitation count for display, keep attempted for rate limiting
    _outreach_chg = await db.get_outreach_changes(hours=24)
    sent_verified = _outreach_chg.get("invited", 0)
    sent_pending = _outreach_chg.get("invited_pending", 0)
    sent = sent_verified + sent_pending  # total sent today (verified + pending verification)
    sent_attempted = rate_data.get("sent", 0)  # for rate limit comparison
    # Use accepted_at-based count (same timeframe as sent) instead of
    # rate_limits counter which can drift out of sync.
    accepted = _outreach_chg.get("accepted", 0)
    daily_limit = rate_data.get("daily_limit", 15)
    acceptance_rate = min(1.0, accepted / sent) if sent > 0 else 0.0

    weekly_sent = await db.get_weekly_invitation_sum()

    # Try to fetch InMail balance + SSI score + pending invitations (non-blocking)
    inmail_credits = -1
    ssi_data: dict = {}
    linkedin_pending_count: int | None = None
    try:
        from ..linkedin import get_account_id, get_linkedin_client, UnipileError
        account_id = get_account_id()
        if account_id:
            client = get_linkedin_client()
            try:
                inmail_data = await client.get_inmail_balance(account_id)
                inmail_credits = inmail_data.get("credits", -1)
            except Exception:
                pass
            try:
                ssi_data = await client.get_ssi_score(account_id)
            except Exception:
                pass
            try:
                from ..linkedin.rate_limiter import get_cached_pending_invitations
                linkedin_pending_count, _ = await get_cached_pending_invitations(client, account_id)
            except Exception:
                pass
            finally:
                await client.close()
    except Exception:
        pass

    # Compute LinkedIn Health Score
    ssi_score = ssi_data.get("score", 0)
    sending_days = await db.get_sending_days_7d()
    total_sent_lifetime = 0
    try:
        def _query_total_sent():
            from ..db.schema import get_db as _get_db
            _db = _get_db()
            row_total = _db.execute("SELECT COALESCE(SUM(sent), 0) as total FROM rate_limits").fetchone()
            _db.close()
            return row_total["total"] if row_total else 0
        total_sent_lifetime = await run_db(_query_total_sent)
    except Exception:
        pass

    from ..linkedin.rate_limiter import _get_effective_caps, estimate_weekly_limit_reset
    _eff_weekly_cap, _ = await _get_effective_caps()
    hs = compute_health_score(
        ssi_score=ssi_score,
        acceptance_rate=acceptance_rate,
        total_sent=total_sent_lifetime,
        daily_sent=sent,
        daily_limit=daily_limit,
        weekly_sent=weekly_sent,
        weekly_limit=_eff_weekly_cap,
        sending_days_7d=sending_days,
    )

    output.append(format_health_score(hs))
    output.append("")

    # DM and follow-up counts from local DB
    import time as _time_mod
    _today_start = int(_time_mod.time()) - (int(_time_mod.time()) % 86400)
    try:
        def _query_activity_counts():
            from ..db.schema import get_db as _get_db
            _db_act = _get_db()
            _dm_row = _db_act.execute(
                "SELECT COUNT(*) as cnt FROM outreaches WHERE status = 'messaged' AND updated_at >= ?",
                (_today_start,),
            ).fetchone()
            _dms = (_dm_row["cnt"] if _dm_row else 0) or 0
            _fu_row = _db_act.execute(
                "SELECT COUNT(*) as cnt FROM messages WHERE role = 'sdr' AND created_at >= ?",
                (_today_start,),
            ).fetchone()
            _fus = (_fu_row["cnt"] if _fu_row else 0) or 0
            _db_act.close()
            return _dms, _fus
        dms_today, followups_today = await run_db(_query_activity_counts)
    except Exception:
        dms_today = 0
        followups_today = 0

    output.append("Activity:")
    output.append(f"├── Invitations: {sent}/{daily_limit} today")
    if dms_today > 0:
        output.append(f"├── DMs sent: {dms_today} today")
    if followups_today > 0:
        output.append(f"├── Follow-ups: {followups_today} today")
    if dms_today > 0 and sent > 0:
        total_outreach_today = sent + dms_today
        output.append(f"├── Total outreach: {total_outreach_today} today")
    output.append(f"├── Weekly: {weekly_sent}/{_eff_weekly_cap} invitations")
    if linkedin_pending_count is not None:
        output.append(f"├── LinkedIn pending: {linkedin_pending_count} sent invitations")
    if weekly_sent >= _eff_weekly_cap:
        _, _, _eta_msg = await estimate_weekly_limit_reset()
        output.append(f"├── ⚠️ Weekly limit reached — invitations resume in {_eta_msg}")
        output.append("│   Email overflow + engagements continue normally")
    # Email overflow stats
    from ..services.channel_selector import has_email_channel
    if await run_db(has_email_channel):
        email_rate = await db.get_email_rate_limit_today()
        email_sent = email_rate.get("sent", 0)
        if email_sent > 0 or sent >= daily_limit or weekly_sent >= _eff_weekly_cap:
            output.append(f"├── 📧 Email overflow: {email_sent} today")
    if inmail_credits >= 0:
        output.append(f"├── InMail credits: {inmail_credits}")
    has_sales_nav = await db.get_setting("has_sales_navigator", False)
    if has_sales_nav:
        output.append("├── License: Sales Navigator ✓ (80/day limit)")
    hubspot_key = await db.get_setting("hubspot_api_key", "")
    if hubspot_key:
        output.append("├── HubSpot: Connected ✓ — crm_sync() to push deals")
    if ssi_score:
        ssi_pillars = ssi_data.get("pillars", [])
        pillar_str = ", ".join(f"{p['name']}: {p['score']}" for p in ssi_pillars if p.get("name")) if ssi_pillars else ""
        ssi_line = f"├── SSI Score: {ssi_score}/100"
        if pillar_str:
            ssi_line += f" ({pillar_str})"
        output.append(ssi_line)
    output.append(f"└── Acceptance rate: {acceptance_rate:.0%}" if sent > 0 else "└── Acceptance rate: No data yet")
    output.append("")

    # ── Free tier usage ──
    if tier != TIER_PRO:
        inv_used = usage.get("invitations_sent", 0)
        msg_used = usage.get("messages_sent", 0)

        output.append("Free Tier Usage (this month):")
        output.append(f"├── Invitations: {inv_used}/{FREE_MONTHLY_INVITATIONS} {progress_bar(inv_used, FREE_MONTHLY_INVITATIONS, 15)}")
        output.append(f"├── Messages: {msg_used}/{FREE_MONTHLY_MESSAGES} {progress_bar(msg_used, FREE_MONTHLY_MESSAGES, 15)}")
        output.append(f"└── Campaigns: {len([c for c in campaigns if c['status'] in ('active', 'draft')])}/{FREE_MAX_CAMPAIGNS}")
        output.append("")

    # ── Campaigns ──
    if not campaigns:
        if offline and config.is_backend_mode():
            output.append("⚠️ Backend unreachable — your campaigns may still exist on the server.")
            output.append("Try again in a moment, or re-authenticate with setup_profile(backend_jwt='...').")
        else:
            output.append("No campaigns yet.")
            output.append("Create one: create_campaign(\"your target description\")")
    else:
        output.append(f"Campaigns ({len(campaigns)}):")
        for i, camp in enumerate(campaigns):
            is_last = i == len(campaigns) - 1
            prefix = "└──" if is_last else "├──"

            stats = await db.get_campaign_stats(camp["id"])
            status_icon = {
                "active": "🟢",
                "paused": "⏸️",
                "completed": "✅",
                "draft": "📝",
            }.get(camp["status"], "⚪")

            hot = stats.get("hot_leads", 0)
            hot_str = f" 🔥{hot}" if hot > 0 else ""

            # Context-aware label: "DMed" for connections-only, "sent" for invitations
            _camp_cfg = json.loads(camp.get("config_json") or "{}")
            _is_dm_only = (
                _camp_cfg.get("connections_only") in (True, "on")
                or not _camp_cfg.get("enable_invitations", True)
            )
            _action_label = "DMed" if _is_dm_only else "sent"

            output.append(
                f"{prefix} {status_icon} {camp['name']} — "
                f"{stats['invited']} {_action_label}, "
                f"{stats['connected']} connected, "
                f"{stats['replied']} replied{hot_str}"
            )

    output.append("")

    # ── Saved ICPs ──
    icps = await db.list_icps(status="active")
    if icps:
        output.append(f"Saved ICPs ({len(icps)}):")
        for i, icp in enumerate(icps[:5]):
            is_last = i == min(4, len(icps) - 1)
            prefix = "└──" if is_last else "├──"
            confidence = icp.get("confidence", 0.5)
            output.append(
                f"{prefix} `{icp['id'][:8]}...` {icp['name']} "
                f"({stars(confidence)} {confidence:.0%})"
            )
        if len(icps) > 5:
            output.append(f"    ... and {len(icps) - 5} more")
        output.append("    Tip: create_campaign(icp_id=\"<id>\") to use a saved ICP")
        output.append("")

    # ── Hot leads summary ──
    def _query_hot_leads():
        from ..db.schema import get_db as _get_db
        _db = _get_db()
        rows = _db.execute(
            """SELECT c.name, c.title, c.company, c.linkedin_url, c.source,
                      MAX(o.updated_at) as last_update
               FROM outreaches o
               JOIN contacts c ON o.contact_id = c.id
               WHERE o.status = 'hot_lead'
               GROUP BY c.id
               ORDER BY last_update DESC
               LIMIT 5"""
        ).fetchall()
        _db.close()
        return rows
    hot_leads = await run_db(_query_hot_leads)

    if hot_leads:
        output.append(f"🔥 Hot Leads ({len(hot_leads)}):")
        for i, lead in enumerate(hot_leads):
            l = dict(lead)
            is_last = i == len(hot_leads) - 1
            prefix = "└──" if is_last else "├──"
            role = l.get("title", "")
            if l.get("company"):
                role += f" at {l['company']}" if role else l["company"]
            src = l.get("source", "search")
            src_label = SOURCE_LABELS.get(src, "")
            src_tag = f" [{src_label}]" if src_label and src not in ("search", "linkedin_search") else ""
            output.append(f"{prefix} {prospect_link(l['name'], l.get('linkedin_url', ''))} — {role}{src_tag}")
        output.append("")

    # ── Engagement stats ──
    eng_stats = await db.get_engagement_stats()
    eng_comments = eng_stats.get("comments", 0)
    eng_reactions = eng_stats.get("reactions", 0)
    eng_total = eng_comments + eng_reactions
    if eng_total > 0:
        output.append(f"💬 Engagements ({eng_total}):")
        output.append(f"├── Comments: {eng_comments}")
        output.append(f"└── Reactions: {eng_reactions}")
        output.append("")
    elif tier != TIER_PRO:
        eng_used = usage.get("engagements_sent", 0)
        if eng_used > 0:
            output.append(f"💬 Engagements: {eng_used}/{FREE_MAX_ENGAGEMENTS} this month")
            output.append("")

    # ── Engagement verification stats ──
    try:
        v_stats = await db.get_engagement_verification_stats()
        v_total = sum(v_stats.values())
        if v_total > 0:
            parts = []
            if v_stats["verified"]:
                parts.append(f"{v_stats['verified']} verified")
            if v_stats["unverified"]:
                parts.append(f"{v_stats['unverified']} unverified")
            if v_stats["trust_api"]:
                parts.append(f"{v_stats['trust_api']} trust_api")
            if v_stats["pending"]:
                parts.append(f"{v_stats['pending']} pending")
            output.append(f"Verification: {' | '.join(parts)}")
            output.append("")
    except Exception as e:
        logger.warning("Verification stats failed: %s", e)

    # ── Follow-up ready hint ──
    max_followups = PRO_MAX_FOLLOWUPS if tier == TIER_PRO else FREE_MAX_FOLLOWUPS
    total_followup_ready = 0
    for camp in campaigns:
        if camp.get("status") in ("active", "draft"):
            total_followup_ready += await db.count_followup_ready(camp["id"], max_followups)
    if total_followup_ready > 0:
        output.append(
            f"💬 {total_followup_ready} prospect{'s' if total_followup_ready != 1 else ''} "
            "ready for follow-up — use send_followup()"
        )
        output.append("")

    # ── Paused campaigns hint (with pause reason) ──
    paused_campaigns = [c for c in campaigns if c.get("status") == "paused"]
    if paused_campaigns:
        import json as _pj
        from ..linkedin.rate_limiter import estimate_weekly_limit_reset as _ewlr_p
        output.append(f"⏸️ {len(paused_campaigns)} paused campaign(s):")
        for pc in paused_campaigns[:3]:
            _pc_cfg = _pj.loads(pc.get("config_json") or "{}")
            _pr = _pc_cfg.get("pause_reason", "user")
            if _pr == "weekly_limit":
                _, _, _p_eta = await _ewlr_p()
                if pc.get("mode") == "autopilot":
                    output.append(f"   └── {pc['name']} — auto-paused (weekly limit) — auto-resumes in {_p_eta}")
                else:
                    output.append(f"   └── {pc['name']} — paused (weekly limit) — resume_campaign(\"{pc['id'][:8]}...\")")
            elif _pr == "emergency_stop":
                output.append(f"   └── {pc['name']} — emergency stopped — resume_campaign(\"{pc['id'][:8]}...\")")
            else:
                output.append(f"   └── {pc['name']} — resume_campaign(\"{pc['id'][:8]}...\")")
        output.append("")

    # ── Archived campaigns hint ──
    completed_campaigns = [c for c in campaigns if c.get("status") == "completed"]
    if completed_campaigns:
        output.append(f"📦 {len(completed_campaigns)} archived campaign(s)")
        output.append("")

    # ── Brand strategy progress ──
    _brand_plan = await db.get_setting("brand_strategy")
    if _brand_plan and isinstance(_brand_plan, dict) and _brand_plan.get("weeks"):
        import time as _t
        from ..config import is_scheduler_enabled
        _bp_total = sum(len(w.get("actions", [])) for w in _brand_plan.get("weeks", []))
        _bp_done = sum(
            1 for w in _brand_plan.get("weeks", [])
            for a in w.get("actions", []) if a.get("status") == "completed"
        )
        output.append(f"🎯 Brand Strategy: {_bp_done}/{_bp_total} actions")
        output.append(f"   {progress_bar(_bp_done, _bp_total, 15)}")
        _created = _brand_plan.get("created_at", 0)
        if _created:
            _week_idx = min((_t.time() - _created) // 604800, len(_brand_plan["weeks"]) - 1)
            _week_idx = max(0, int(_week_idx))
            _theme = _brand_plan["weeks"][_week_idx].get("theme", "")
            if _theme:
                output.append(f"   Week {_week_idx + 1}: {_theme}")
        # Show automation status when scheduler is active
        if is_scheduler_enabled():
            output.append("   Automation: Active (posts + engagement run automatically)")
            if _bp_done >= _bp_total:
                output.append('   Re-analysis scheduled at 28-day mark')
            else:
                output.append('   Progress: brand_strategy(action="progress")')
        else:
            if _bp_done < _bp_total:
                output.append('   Next: brand_strategy(action="execute")')
            else:
                output.append('   All done! Run brand_strategy(action="progress") for results.')
        output.append("")

    # ── Strategy Engine ──
    try:
        strat = await db.get_strategy_summary()
        if strat.get("active_patterns", 0) > 0 or strat.get("total_actions", 0) > 0:
            top = strat.get("top_pattern")
            top_str = f" | Top: {top['pattern_key']}" if top else ""
            output.append(
                f"\U0001f9e0 Strategy Engine: {strat['active_patterns']} patterns, "
                f"{strat['total_actions']} actions "
                f"({strat.get('validated_actions', 0)} validated)"
                f"{top_str}"
            )
            if strat.get("spawned_campaigns", 0) > 0:
                output.append(f"   Auto-spawned campaigns: {strat['spawned_campaigns']}")
            output.append('   Details: show_strategy()')
            output.append("")
    except Exception:
        pass

    # ── Inbound Pipeline ──
    try:
        funnel = await db.get_inbound_funnel_stats()
        total_inbound = sum(funnel.get("by_status", {}).values())
        if total_inbound > 0:
            by_status = funnel.get("by_status", {})
            by_intent = funnel.get("by_intent", {})
            new_count = by_status.get("new", 0)
            qualified_count = by_status.get("qualified", 0)
            engaged_count = by_status.get("engaged", 0)
            converted_count = by_status.get("converted", 0)

            output.append(f"Inbound Pipeline ({total_inbound} signals):")

            # Status breakdown
            status_parts = []
            if new_count:
                status_parts.append(f"{new_count} new")
            if qualified_count:
                status_parts.append(f"{qualified_count} qualified")
            if engaged_count:
                status_parts.append(f"{engaged_count} engaged")
            if converted_count:
                status_parts.append(f"{converted_count} converted")
            if status_parts:
                output.append(f"   {' | '.join(status_parts)}")

            # Intent breakdown for qualified leads
            buying = by_intent.get("buying_signal", 0)
            networking = by_intent.get("networking", 0)
            partnership = by_intent.get("partnership", 0)
            vendor = by_intent.get("vendor_pitch", 0)
            intent_parts = []
            if buying:
                intent_parts.append(f"{buying} buying signal")
            if networking:
                intent_parts.append(f"{networking} networking")
            if partnership:
                intent_parts.append(f"{partnership} partnership")
            if vendor:
                intent_parts.append(f"{vendor} vendor pitch")
            if intent_parts:
                output.append(f"   Intents: {', '.join(intent_parts)}")

            # Top match
            top_leads = await db.list_inbound_signals(status="qualified", limit=1)
            if top_leads:
                top = top_leads[0]
                top_name = top.get("sender_name", "Unknown")
                top_headline = top.get("sender_headline", "")
                top_conf = top.get("confidence", 0) or 0
                badge = "🟢" if top_conf >= 0.7 else "🟡" if top_conf >= 0.4 else "🔴"
                top_line = f"   Top: {badge} {top_name}"
                if top_headline:
                    top_line += f" — {top_headline}"
                top_line += f" ({top_conf:.0%})"
                output.append(top_line)

            output.append("")
    except Exception as e:
        logger.debug("Inbound pipeline stats failed: %s", e)

    # ── Signal Intelligence ──
    try:
        from ..services.signal_service import format_signal_dashboard
        signal_section = await run_db(format_signal_dashboard, days=7)
        if signal_section:
            output.append(signal_section)
    except Exception as e:
        logger.debug("Signal dashboard failed: %s", e)

    # ── Global contact base ──
    try:
        gc_stats = await db.get_global_contact_stats()
        if gc_stats["total"] > 0:
            output.append("")
            output.append("Contact Base")
            parts = [f"{gc_stats['total']} people"]
            for stage, count in gc_stats["by_lifecycle"].items():
                if count > 0:
                    parts.append(f"{count} {stage}")
            output.append("  " + "  |  ".join(parts))
            output.append("  Run contacts(action='stats') for full breakdown")
    except Exception:
        pass  # Non-critical

    # ── Post Intelligence ──
    try:
        pstats = await db.get_post_collection_stats(days=1)
        total_posts = pstats.get("total_posts", 0)
        if total_posts > 0:
            output.append(f"Post Intelligence ({total_posts} total posts):")
            output.append(f"├── Today: {pstats.get('posts_collected_today', 0)} collected, {pstats.get('posts_analyzed_today', 0)} analyzed")
            output.append(f"├── Authors scanned today: {pstats.get('authors_scanned_today', 0)}")
            coverage = pstats.get("analysis_coverage", 0)
            output.append(f"├── Analysis coverage: {coverage}%")
            try:
                def _query_research_counts():
                    from ..db.schema import get_db as _get_db
                    _db = _get_db()
                    _tc = _db.execute(
                        "SELECT COUNT(*) as cnt FROM contacts WHERE linkedin_id IS NOT NULL"
                    ).fetchone()
                    _rc = _db.execute(
                        "SELECT COUNT(*) as cnt FROM contacts WHERE research_status = 'complete'"
                    ).fetchone()
                    _pc = _db.execute(
                        "SELECT COUNT(*) as cnt FROM contacts WHERE research_status IS NULL OR research_status = 'pending'"
                    ).fetchone()
                    _db.close()
                    return (
                        _tc["cnt"] if _tc else 0,
                        _rc["cnt"] if _rc else 0,
                        _pc["cnt"] if _pc else 0,
                    )
                tc, rc, pc = await run_db(_query_research_counts)
                if tc > 0:
                    output.append(f"├── Research: {rc}/{tc} contacts researched ({pc} pending)")
            except Exception:
                pass
            output.append(f"└── Total analyzed: {pstats.get('total_analyzed', 0)}/{total_posts}")
            output.append("")
    except Exception:
        pass  # Non-critical

    # ── Cross-validation: outreach statuses vs usage counters ──
    try:
        _total_reached = 0
        for c in campaigns:
            if c["status"] in ("active", "paused"):
                _cs = await db.get_campaign_stats(c["id"])
                _total_reached += _cs.get("invited", 0)
        _total_usage = usage.get("invitations_sent", 0) + usage.get("messages_sent", 0)
        if _total_reached > 0 and _total_usage > 0:
            _drift = abs(_total_reached - _total_usage)
            if _drift > max(5, _total_reached * 0.1):
                output.append(
                    f"⚠️ Stats drift: {_total_reached} outreaches reached vs "
                    f"{_total_usage} in usage counters — numbers may be inaccurate"
                )
                output.append("")
    except Exception:
        pass

    # ── ICP Prospect Enrichment ──
    try:
        import time as _time_mod2
        _day_ago = int(_time_mod2.time()) - 86400
        def _query_enrichment_stats():
            from ..db.schema import get_db as _get_db
            _edb = _get_db()
            _s24h = _edb.execute(
                """SELECT source_detail, COUNT(*) as cnt
                   FROM contacts WHERE source = 'auto_enrichment' AND created_at >= ?
                   GROUP BY source_detail ORDER BY cnt DESC""",
                (_day_ago,),
            ).fetchall()
            _sall = _edb.execute(
                """SELECT source_detail, COUNT(*) as cnt
                   FROM contacts WHERE source = 'auto_enrichment'
                   GROUP BY source_detail ORDER BY cnt DESC""",
            ).fetchall()
            _edb.close()
            return _s24h, _sall
        _src_24h, _src_all = await run_db(_query_enrichment_stats)

        if _src_24h or _src_all:
            _labels = {
                "linkedin_search": "LinkedIn Search", "global_contacts": "Global Contacts",
                "signal_reeval": "Re-evaluated Signals", "job_change": "Job Changers",
                "signal_account": "Signal Accounts", "profile_viewer": "Profile Viewers",
                "post_author": "Post Authors", "competitor_commenter": "Competitor Commenters",
                "company_engager": "Company Engagers", "connection": "1st-Degree Connections",
                "post_commenter": "Post Commenters", "inbound_low_conf": "Inbound (Low Conf)",
            }
            _t24 = sum(r["cnt"] for r in _src_24h)
            _tall = sum(r["cnt"] for r in _src_all)
            output.append(f"Prospect Enrichment ({_t24} last 24h, {_tall} total):")
            _c24 = {r["source_detail"]: r["cnt"] for r in _src_24h}
            for row in _src_all:
                tag = row["source_detail"] or "unknown"
                label = _labels.get(tag, tag.replace("_", " ").title())
                c24 = _c24.get(tag, 0)
                output.append(f"  {label}: {c24} (24h) / {row['cnt']} (total)")
            output.append("")
    except Exception:
        pass

    # ── Pipeline Health ──
    try:
        def _query_pipeline_health():
            from ..db.schema import get_db as _get_db
            _hdb = _get_db()
            _health_items = []

            _orphaned = _hdb.execute(
                """SELECT COUNT(*) as cnt FROM outreaches o
                   WHERE o.status = 'connected' AND o.followup_count = 0
                   AND o.id NOT IN (
                       SELECT sj.outreach_id FROM scheduler_jobs sj
                       WHERE sj.outreach_id IS NOT NULL
                         AND sj.job_type IN ('send_dm', 'followup')
                         AND sj.status IN ('pending', 'running')
                   )"""
            ).fetchone()["cnt"]
            if _orphaned > 0:
                _health_items.append(f"  {_orphaned} orphaned prospects (connected, no pending jobs)")

            _unverified = _hdb.execute(
                "SELECT COUNT(*) as cnt FROM engagements WHERE verified_status = 'unverified'"
            ).fetchone()["cnt"]
            if _unverified > 0:
                _health_items.append(f"  {_unverified} unverified engagements")

            _pending_jobs = _hdb.execute(
                """SELECT job_type, COUNT(*) as cnt FROM scheduler_jobs
                   WHERE status = 'pending' GROUP BY job_type ORDER BY cnt DESC LIMIT 5"""
            ).fetchall()
            if _pending_jobs:
                _job_parts = [f"{r['job_type']}={r['cnt']}" for r in _pending_jobs]
                _health_items.append(f"  Pending jobs: {', '.join(_job_parts)}")

            _hdb.close()
            return _health_items

        _health_items = await run_db(_query_pipeline_health)
        if _health_items:
            output.append("Pipeline Health:")
            for item in _health_items:
                output.append(item)
            output.append("")
    except Exception:
        pass

    # ── Quick actions ──
    has_active = any(c.get("status") == "active" for c in campaigns)
    has_paused = len(paused_campaigns) > 0
    has_copilot = any(
        c.get("status") == "active" and c.get("mode") == "copilot"
        for c in campaigns
    )

    output.append("Quick actions:")
    output.append("├── \"any replies?\" → check_replies")
    output.append("├── \"what's next?\" → suggest_next_action")
    output.append("├── \"detailed report\" → campaign_report")
    if has_copilot:
        output.append("├── \"send messages\" → generate_and_send")
    if total_followup_ready > 0:
        output.append("├── \"send follow-up\" → send_followup")
    output.append("├── \"engage posts\" → engage_prospect")
    if has_active:
        output.append("├── \"pause outreach\" → pause_campaign")
    if has_paused:
        output.append("├── \"resume outreach\" → resume_campaign")
    output.append("├── \"export results\" → export_campaign")
    output.append("├── \"compare campaigns\" → compare_campaigns")
    output.append("├── \"edit campaign\" → edit_campaign")
    output.append("├── \"view conversation\" → show_conversation")
    output.append("├── \"retry errors\" → retry_failed")
    output.append("├── \"skip prospect\" → skip_prospect")
    output.append("├── \"stop everything\" → emergency_stop")
    output.append("├── \"brand audit\" → brand_strategy")
    output.append("├── \"sync to CRM\" → crm_sync")
    output.append("├── \"signal feed\" → show_signals")
    output.append("├── \"manage keywords\" → manage_watchlist")
    output.append("├── \"browse contacts\" → contacts")
    output.append("└── \"create campaign\" → create_campaign")

    return "\n".join(output)


async def _show_overview_from_backend(data: dict) -> str:
    """Format dashboard from live backend stats.

    Uses the same visual style as _show_overview() but with data
    from the backend's GET /api/v1/stats response.
    """
    from ..services.health_score import compute_health_score, format_health_score

    tier = get_tier()
    campaigns = data.get("campaigns", [])
    rl = data.get("rate_limits", {})
    usage = data.get("usage", {})
    eng = data.get("engagements", {})
    hot_leads = data.get("hot_leads", [])

    output = ["📊 **HeyLead Dashboard** (live)\n"]

    # ── Account Connectivity Warning ──
    acct_status = data.get("account_status", "connected")
    acct_message = data.get("account_status_message", "")
    if acct_status == "disconnected":
        output.append("⚠️ **LinkedIn Account Disconnected**\n")
        output.append("Your LinkedIn session has expired. All outreach is paused.")
        output.append("Go to https://heylead.dev/auth/login-url to reconnect,")
        output.append("then run setup_profile(backend_jwt='YOUR_TOKEN').\n")
    elif acct_status == "degraded":
        output.append(f"⚠️ **Account Warning**: {acct_message}\n")

    # ── Account Health ──
    sent = rl.get("sent_today", 0)
    accepted = rl.get("accepted_today", 0)
    daily_limit = rl.get("daily_limit", 15)
    weekly_sent = rl.get("weekly_sent", 0)
    acceptance_rate = min(1.0, accepted / sent) if sent > 0 else 0.0

    # Compute health score (SSI not available from backend, use 0)
    total_sent_lifetime = weekly_sent  # Approximate with weekly
    sending_days = min(7, weekly_sent) if weekly_sent > 0 else 0  # Approximate
    from ..linkedin.rate_limiter import _get_effective_caps as _gec2, estimate_weekly_limit_reset as _ewlr2
    _eff_wc2, _ = await _gec2()
    hs = compute_health_score(
        ssi_score=0,
        acceptance_rate=acceptance_rate,
        total_sent=total_sent_lifetime,
        daily_sent=sent,
        daily_limit=daily_limit,
        weekly_sent=weekly_sent,
        weekly_limit=_eff_wc2,
        sending_days_7d=sending_days,
    )

    output.append(format_health_score(hs))
    output.append("")
    dms_today = rl.get("dms_sent_today", 0)
    followups_today = rl.get("followups_today", 0)
    total_outreach_today = sent + dms_today

    output.append("Activity:")
    output.append(f"├── Invitations: {sent}/{daily_limit} today")
    if dms_today > 0:
        output.append(f"├── DMs sent: {dms_today} today")
    if followups_today > 0:
        output.append(f"├── Follow-ups: {followups_today} today")
    if dms_today > 0 and sent > 0:
        output.append(f"├── Total outreach: {total_outreach_today} today")
    output.append(f"├── Weekly: {weekly_sent}/{_eff_wc2} invitations")
    if weekly_sent >= _eff_wc2:
        _, _, _eta2 = await _ewlr2()
        output.append(f"├── ⚠️ Weekly limit reached — invitations resume in {_eta2}")
        output.append("│   Email overflow + engagements continue normally")
    # Email overflow stats (cloud scheduler path)
    from ..services.channel_selector import has_email_channel as _has_email
    if await run_db(_has_email):
        _erl = await db.get_email_rate_limit_today()
        _es = _erl.get("sent", 0)
        if _es > 0 or sent >= daily_limit or weekly_sent >= _eff_wc2:
            output.append(f"├── 📧 Email overflow: {_es} today")
    output.append(f"└── Acceptance rate: {acceptance_rate:.0%}" if sent > 0 else "└── Acceptance rate: No data yet")
    output.append("")

    # ── Free tier usage ──
    if tier != TIER_PRO:
        inv_used = usage.get("invitations_sent", 0)
        msg_used = usage.get("messages_sent", 0)

        output.append("Free Tier Usage (this month):")
        output.append(f"├── Invitations: {inv_used}/{FREE_MONTHLY_INVITATIONS} {progress_bar(inv_used, FREE_MONTHLY_INVITATIONS, 15)}")
        output.append(f"├── Messages: {msg_used}/{FREE_MONTHLY_MESSAGES} {progress_bar(msg_used, FREE_MONTHLY_MESSAGES, 15)}")
        active_count = len([c for c in campaigns if c.get("status") in ("active", "draft")])
        output.append(f"└── Campaigns: {active_count}/{FREE_MAX_CAMPAIGNS}")
        output.append("")

    # ── Campaigns ──
    if not campaigns:
        output.append("No campaigns yet.")
        output.append("Create one: create_campaign(\"your target description\")")
    else:
        output.append(f"Campaigns ({len(campaigns)}):")
        for i, camp in enumerate(campaigns):
            is_last = i == len(campaigns) - 1
            prefix = "└──" if is_last else "├──"

            status_icon = {
                "active": "🟢",
                "paused": "⏸️",
                "completed": "✅",
                "draft": "📝",
            }.get(camp.get("status", ""), "⚪")

            hot = camp.get("hot_leads", 0)
            hot_str = f" 🔥{hot}" if hot > 0 else ""

            # Context-aware label: "DMed" for connections-only, "sent" for invitations
            _action_label = "DMed" if camp.get("connections_only", False) else "sent"

            output.append(
                f"{prefix} {status_icon} {camp['name']} — "
                f"{camp.get('invited', 0)} {_action_label}, "
                f"{camp.get('connected', 0)} connected, "
                f"{camp.get('replied', 0)} replied{hot_str}"
            )

    output.append("")

    # ── Hot leads ──
    if hot_leads:
        output.append(f"🔥 Hot Leads ({len(hot_leads)}):")
        for i, lead in enumerate(hot_leads):
            is_last = i == len(hot_leads) - 1
            prefix = "└──" if is_last else "├──"
            role = lead.get("title", "")
            if lead.get("company"):
                role += f" at {lead['company']}" if role else lead["company"]
            output.append(f"{prefix} {lead.get('name', 'Unknown')} — {role}")
        output.append("")

    # ── Engagement stats ──
    eng_comments = eng.get("comments", 0)
    eng_reactions = eng.get("reactions", 0)
    eng_total = eng_comments + eng_reactions
    if eng_total > 0:
        output.append(f"💬 Engagements ({eng_total}):")
        output.append(f"├── Comments: {eng_comments}")
        output.append(f"└── Reactions: {eng_reactions}")
        output.append("")

    # ── Local-only sections (ICPs, signals, brand, strategy — still from local DB) ──
    try:
        icps = await db.list_icps(status="active")
        if icps:
            output.append(f"Saved ICPs ({len(icps)}):")
            for i, icp in enumerate(icps[:5]):
                is_last = i == min(4, len(icps) - 1)
                prefix = "└──" if is_last else "├──"
                confidence = icp.get("confidence", 0.5)
                output.append(
                    f"{prefix} `{icp['id'][:8]}...` {icp['name']} "
                    f"({stars(confidence)} {confidence:.0%})"
                )
            if len(icps) > 5:
                output.append(f"    ... and {len(icps) - 5} more")
            output.append("    Tip: create_campaign(icp_id=\"<id>\") to use a saved ICP")
            output.append("")
    except Exception:
        pass

    # ── Signal Intelligence ──
    try:
        from ..services.signal_service import format_signal_dashboard
        signal_section = await run_db(format_signal_dashboard, days=7)
        if signal_section:
            output.append(signal_section)
    except Exception:
        pass

    # ── Contact Base ──
    try:
        gc_stats = await db.get_global_contact_stats()
        if gc_stats["total"] > 0:
            output.append("")
            output.append("Contact Base")
            parts = [f"{gc_stats['total']} people"]
            for stage, count in gc_stats["by_lifecycle"].items():
                if count > 0:
                    parts.append(f"{count} {stage}")
            output.append("  " + "  |  ".join(parts))
            output.append("  Run contacts(action='stats') for full breakdown")
    except Exception:
        pass  # Non-critical

    # ── Post Intelligence ──
    try:
        pstats = await db.get_post_collection_stats(days=1)
        total_posts = pstats.get("total_posts", 0)
        if total_posts > 0:
            output.append(f"Post Intelligence ({total_posts} total posts):")
            output.append(f"├── Today: {pstats.get('posts_collected_today', 0)} collected, {pstats.get('posts_analyzed_today', 0)} analyzed")
            output.append(f"├── Authors scanned today: {pstats.get('authors_scanned_today', 0)}")
            coverage = pstats.get("analysis_coverage", 0)
            output.append(f"├── Analysis coverage: {coverage}%")
            try:
                def _query_research_counts_backend():
                    from ..db.schema import get_db as _get_db
                    _rdb = _get_db()
                    _tc = _rdb.execute(
                        "SELECT COUNT(*) as cnt FROM contacts WHERE linkedin_id IS NOT NULL"
                    ).fetchone()
                    _rc = _rdb.execute(
                        "SELECT COUNT(*) as cnt FROM contacts WHERE research_status = 'complete'"
                    ).fetchone()
                    _pc = _rdb.execute(
                        "SELECT COUNT(*) as cnt FROM contacts WHERE research_status IS NULL OR research_status = 'pending'"
                    ).fetchone()
                    _rdb.close()
                    return (
                        _tc["cnt"] if _tc else 0,
                        _rc["cnt"] if _rc else 0,
                        _pc["cnt"] if _pc else 0,
                    )
                tc, rc, pc = await run_db(_query_research_counts_backend)
                if tc > 0:
                    output.append(f"├── Research: {rc}/{tc} contacts researched ({pc} pending)")
            except Exception:
                pass
            output.append(f"└── Total analyzed: {pstats.get('total_analyzed', 0)}/{total_posts}")
            output.append("")
    except Exception:
        pass  # Non-critical

    # ── Cross-validation: outreach statuses vs usage counters ──
    try:
        _total_reached = sum(
            c.get("invited", 0)
            for c in campaigns if c.get("status") in ("active", "paused")
        )
        _total_usage = usage.get("invitations_sent", 0) + usage.get("messages_sent", 0)
        if _total_reached > 0 and _total_usage > 0:
            _drift = abs(_total_reached - _total_usage)
            if _drift > max(5, _total_reached * 0.1):
                output.append(
                    f"⚠️ Stats drift: {_total_reached} outreaches reached vs "
                    f"{_total_usage} in usage counters — numbers may be inaccurate"
                )
                output.append("")
    except Exception:
        pass

    # ── Quick actions ──
    has_active = any(c.get("status") == "active" for c in campaigns)
    has_copilot = any(
        c.get("status") == "active" and c.get("mode") == "copilot"
        for c in campaigns
    )

    output.append("Quick actions:")
    output.append("├── \"any replies?\" → check_replies")
    output.append("├── \"what's next?\" → suggest_next_action")
    output.append("├── \"detailed report\" → campaign_report")
    if has_copilot:
        output.append("├── \"send messages\" → generate_and_send")
    output.append("├── \"engage posts\" → engage_prospect")
    if has_active:
        output.append("├── \"pause outreach\" → pause_campaign")
    output.append("├── \"export results\" → export_campaign")
    output.append("├── \"compare campaigns\" → compare_campaigns")
    output.append("├── \"edit campaign\" → edit_campaign")
    output.append("├── \"view conversation\" → show_conversation")
    output.append("├── \"retry errors\" → retry_failed")
    output.append("├── \"skip prospect\" → skip_prospect")
    output.append("├── \"stop everything\" → emergency_stop")
    output.append("├── \"brand audit\" → brand_strategy")
    output.append("├── \"sync to CRM\" → crm_sync")
    output.append("├── \"signal feed\" → show_signals")
    output.append("├── \"manage keywords\" → manage_watchlist")
    output.append("└── \"create campaign\" → create_campaign")

    return "\n".join(output)


async def _show_campaign_detail(campaign_id: str) -> str:
    """Show detailed stats for a specific campaign."""

    campaign = await db.get_campaign(campaign_id)
    if not campaign:
        return f"❌ Campaign not found: {campaign_id}"

    stats = await db.get_campaign_stats(campaign_id)
    config = json.loads(campaign.get("config_json") or "{}")
    icp = json.loads(campaign.get("icp_json") or "{}")

    # Calculate days since creation
    import time
    created = campaign.get("created_at", 0)
    days = (int(time.time()) - created) // 86400 if created else 0

    output = [
        f"📊 Campaign: **{campaign['name']}** (Day {days})",
        f"   Mode: {'🤖 Autopilot' if campaign.get('mode') == 'autopilot' else '👤 Copilot'}",
        f"   Target: {config.get('target_description', 'N/A')}",
        "",
    ]

    # Settings summary (only show non-default values)
    settings_lines: list[str] = []

    # Voice mode
    vm = config.get("voice_mode", "text_only")
    if vm != "text_only":
        settings_lines.append(f"🎤 Voice: {vm}")

    # Warm-up toggles — show disabled ones
    toggles = {
        "enable_profile_views": ("Profile Views", True),
        "enable_follows": ("Follows", True),
        "enable_endorsements": ("Endorsements", True),
        "enable_engagements": ("Engagements", True),
        "enable_followups": ("Follow-ups", True),
    }
    disabled = [label for key, (label, default) in toggles.items() if not config.get(key, default)]
    if disabled:
        settings_lines.append(f"⏸️ Disabled: {', '.join(disabled)}")

    # Engagement mode
    em = config.get("engagement_mode", "auto")
    if em != "auto":
        settings_lines.append(f"💬 Engagement: {em.replace('_', ' ')}")

    # Follow-up schedule
    fdd = config.get("followup_delay_days")
    mf = config.get("max_followups")
    if fdd and fdd != [1, 7, 14, 21, 28]:
        settings_lines.append(f"📅 Follow-up schedule: day {','.join(map(str, fdd))}")
    elif mf and mf != 5:
        settings_lines.append(f"📅 Max follow-ups: {mf}")

    # Business hours
    if config.get("send_in_business_hours") in (True, "on"):
        settings_lines.append("🕐 Business hours: on")

    # Active days
    ad = config.get("active_days")
    if ad and ad != [0, 1, 2, 3, 4]:
        day_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        settings_lines.append(f"📆 Active days: {','.join(day_names[d] for d in ad if d < 7)}")

    if settings_lines:
        output.append("Settings:")
        for i, line in enumerate(settings_lines):
            prefix = "└──" if i == len(settings_lines) - 1 else "├──"
            output.append(f"{prefix} {line}")
        output.append("")

    # Stats tree
    total = stats.get("total_prospects", 0)
    invited = stats.get("invited", 0)
    connected = stats.get("connected", 0)
    replied = stats.get("replied", 0)
    hot = stats.get("hot_leads", 0)
    skipped = stats.get("skipped", 0)
    pending = total - invited - skipped

    _is_dm_only_detail = (
        config.get("connections_only") in (True, "on")
        or not config.get("enable_invitations", True)
    )
    output.append("Progress:")
    output.append(f"├── DMs sent: {invited}" if _is_dm_only_detail else f"├── Invitations sent: {invited}")
    acc_str = f"{stats['acceptance_rate']:.0%}"
    raw = stats.get('raw_acceptance_rate', 0)
    if raw > 0 and abs(raw - stats['acceptance_rate']) > 0.01:
        acc_str += f" (raw: {raw:.0%})"
    output.append(f"├── Accepted: {connected} ({acc_str})" if invited > 0 else f"├── Accepted: {connected}")
    output.append(f"├── Replies: {replied} ({stats['reply_rate']:.0%})" if connected > 0 else f"├── Replies: {replied}")
    output.append(f"├── Hot leads: {hot} 🔥" if hot > 0 else f"├── Hot leads: {hot}")
    if skipped > 0:
        output.append(f"├── Skipped: {skipped}")
    output.append(f"└── Remaining: {pending} prospects queued")
    output.append("")

    # Funnel visualization
    if invited > 0:
        output.append("Funnel:")
        output.append(f"├── Queued:    {progress_bar(total, total, 20)} {total}")
        output.append(f"├── Sent:      {progress_bar(invited, total, 20)} {invited}")
        output.append(f"├── Connected: {progress_bar(connected, total, 20)} {connected}")
        output.append(f"├── Replied:   {progress_bar(replied, total, 20)} {replied}")
        output.append(f"└── Hot leads: {progress_bar(hot, total, 20)} {hot}")
        output.append("")

    # Velocity metrics
    velocity = await db.get_campaign_velocity(campaign_id)
    cnt_accept = velocity.get("count_accepted", 0)
    if cnt_accept > 0:
        avg_tta = velocity.get("avg_time_to_accept")
        avg_ttr = velocity.get("avg_time_to_reply")
        output.append("Velocity:")
        output.append(f"\u251c\u2500\u2500 Avg time to accept: {format_duration(avg_tta)}")
        if avg_ttr is not None:
            output.append(f"\u2514\u2500\u2500 Avg time to reply: {format_duration(avg_ttr)}")
        else:
            output.append(f"\u2514\u2500\u2500 Avg time to reply: No replies yet")
        output.append("")

    # Outcomes section
    outcomes = await db.get_campaign_outcomes(campaign_id)
    if outcomes["total_closed"] > 0:
        output.append("Outcomes:")
        output.append(f"\u251c\u2500\u2500 \U0001f3c6 Won: {outcomes['closed_happy']}")
        output.append(f"\u251c\u2500\u2500 \U0001f4c9 Lost: {outcomes['closed_unhappy']}")
        if outcomes["opted_out"] > 0:
            output.append(f"\u251c\u2500\u2500 \U0001f6ab Opted out: {outcomes['opted_out']}")
        output.append(f"\u2514\u2500\u2500 Conversion: {conversion_rate_display(outcomes['closed_happy'], outcomes['closed_unhappy'])}")
        output.append("")

    # Engagement stats for this campaign
    camp_eng = await db.get_engagement_stats(campaign_id)
    camp_comments = camp_eng.get("comments", 0)
    camp_reactions = camp_eng.get("reactions", 0)
    camp_eng_total = camp_comments + camp_reactions
    if camp_eng_total > 0:
        output.append("Engagements:")
        output.append(f"├── Comments: {camp_comments}")
        output.append(f"└── Reactions: {camp_reactions}")
        # Per-campaign verification stats
        try:
            cv = await db.get_engagement_verification_stats(campaign_id)
            cv_total = sum(cv.values())
            if cv_total > 0:
                parts = []
                if cv["verified"]:
                    parts.append(f"{cv['verified']} verified")
                if cv["unverified"]:
                    parts.append(f"{cv['unverified']} unverified")
                if cv["trust_api"]:
                    parts.append(f"{cv['trust_api']} trust_api")
                if cv["pending"]:
                    parts.append(f"{cv['pending']} pending")
                output.append(f"    Verification: {' | '.join(parts)}")
        except Exception:
            pass
        output.append("")

    # Voice memo stats
    voice_stats = await db.get_voice_memo_stats(campaign_id)
    voice_sent = voice_stats.get("voice_sent", 0)
    if voice_sent > 0:
        voice_rr = voice_stats.get("voice_reply_rate", 0)
        text_rr = voice_stats.get("text_reply_rate", 0)
        text_sent = voice_stats.get("text_sent", 0)
        output.append(f"🎤 Voice memos: {voice_sent} sent (text: {text_sent})")
        if voice_stats.get("voice_total_outreaches", 0) > 0:
            output.append(f"   Reply rate: voice {voice_rr:.0%} vs text {text_rr:.0%}")
        output.append("")

    # Stale leads warning
    stale = await db.get_stale_outreaches(campaign_id, stale_days=14)
    if stale:
        output.append(f"⚠️ {len(stale)} stale lead{'s' if len(stale) != 1 else ''} (no activity 14+ days)")
        output.append(f"   → Run campaign_report for details")
        output.append("")

    # Top prospects with status
    def _query_top_contacts():
        from ..db.schema import get_db as _get_db
        _db = _get_db()
        rows = _db.execute(
            """SELECT c.name, c.title, c.company, c.fit_score, o.status
               FROM contacts c
               JOIN outreaches o ON o.contact_id = c.id
               WHERE c.campaign_id = ?
               ORDER BY c.fit_score DESC
               LIMIT 5""",
            (campaign_id,),
        ).fetchall()
        _db.close()
        return rows
    top_contacts = await run_db(_query_top_contacts)

    if top_contacts:
        output.append("Top Prospects:")
        status_icons = {
            "pending": "⏳",
            "invited": "📤",
            "connected": "🤝",
            "messaged": "💬",
            "replied": "📩",
            "hot_lead": "🔥",
            "review_pending": "👀",
            "skipped": "⏭️",
            "opted_out": "🚫",
            "closed_happy": "✅",
            "closed_unhappy": "❌",
            "error": "⚠️",
        }
        for i, contact in enumerate(top_contacts):
            c = dict(contact)
            is_last = i == len(top_contacts) - 1
            prefix = "└──" if is_last else "├──"
            icon = status_icons.get(c.get("status", ""), "⚪")
            role = c.get("title", "")
            if c.get("company"):
                role += f" at {c['company']}" if role else c["company"]
            output.append(f"{prefix} {icon} {c['name']} — {role} ({stars(c.get('fit_score', 0))})")
        output.append("")

    return "\n".join(output)
