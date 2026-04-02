"""Tool: engage_prospect — Comment on, react to, or follow a prospect on LinkedIn.

Core engagement loop:
1. Find next outreach candidate for engagement
2. For follow action: follow the prospect's profile (no post needed)
3. For comment/react: fetch prospect's recent LinkedIn posts via get_user_posts()
4. Pick the best post (most recent with substantial text)
5. Generate voice-matched comment or react with LIKE
6. In Copilot mode: show post + proposed action for review
7. In Autopilot: send immediately
8. Log engagement to DB
"""

from __future__ import annotations

import json
import logging
import random
import time
from typing import Any

from ..ai.comment_generator import generate_comment, COMMENT_MAX_CHARS
from ..ai.message_fixer import fix_message
from ..ai.message_improver import improve_message
from ..ai.message_validator import validate_comment
from ..ai.prospect_analyzer import analyze_prospect
from ..config import get_tier
from ..constants import (
    AUTO_REACT_PROBABILITY,
    COMMENT_MAX_CHARS as COMMENT_LIMIT,
    FREE_MAX_ENGAGEMENTS,
    TIER_PRO,
)
from ..db import aio as db
from ..db.async_bridge import run_db
from ..formatter import stars
from ..linkedin import (
    UnipileAuthError,
    UnipileError,
    get_account_id,
    get_linkedin_client,
)

logger = logging.getLogger(__name__)

MAX_ENGAGEMENTS_PER_OUTREACH = 3  # Don't over-engage with a single prospect

# Time-limited cooldowns (seconds) — match scheduler_store.py constants
COOLDOWN_NO_POSTS = 48 * 3600       # 48h: prospect has no posts at all
COOLDOWN_422_ERROR = 48 * 3600      # 48h: Unipile returned 422 for get_user_posts


async def _should_react_auto(outreach_id: str, post_text: str, engagement_mode: str = "auto") -> bool:
    """Decide whether auto mode should react (like) or comment.

    engagement_mode controls behavior:
    - "auto": Short posts (<50 chars) -> react. Budget-aware: if one type's
              budget is exhausted, force the other. Otherwise 50/50 probability.
    - "comment_only": Always comment (never react).
    - "react_only": Always react (never comment).
    """
    if engagement_mode == "comment_only":
        return False
    if engagement_mode == "react_only":
        return True

    # Default "auto" behavior
    if len(post_text) < 50:
        return True

    # Budget-aware decision: if one type is exhausted, force the other
    from ..linkedin.rate_limiter import check_engagement_budget
    react_ok, _, _ = await check_engagement_budget(engagement_type="react")
    comment_ok, _, _ = await check_engagement_budget(engagement_type="comment")

    if react_ok and not comment_ok:
        return True   # Comment budget full → react
    if comment_ok and not react_ok:
        return False  # React budget full → comment

    return random.random() < AUTO_REACT_PROBABILITY


async def run_engage_prospect(
    campaign_id: str = "",
    outreach_id: str = "",
    action: str = "auto",
    mode: str = "autopilot",
) -> str:
    """Engage with a prospect's LinkedIn post (comment or react).

    Flow:
    1. Pre-checks: setup_complete, account_id, client
    2. Normalize action, find campaign + candidate
    3. Fetch prospect's recent posts
    4. Pick best post, generate comment or react
    5. Copilot: show for review. Autopilot: send immediately.
    6. Log engagement to DB
    """

    # ── Step 0: Pre-checks ──
    setup_done = await db.get_setting("setup_complete", False)
    if not setup_done:
        return (
            "Setup required before engaging.\n\n"
            "Please run setup_profile first."
        )

    account_id = get_account_id()
    if not account_id:
        return "No LinkedIn account connected. Run setup_profile first."

    try:
        client = get_linkedin_client()
    except UnipileError as e:
        return f"{e}"

    # Normalize action
    action = action.lower().strip()
    if action == "like":
        action = "react"
    if action not in ("auto", "comment", "react", "follow", "endorse", "reply_comment", "view"):
        await client.close()
        return f"Invalid action: '{action}'. Use 'auto', 'comment', 'react', 'follow', 'endorse', 'reply_comment', or 'like'."

    # ── Step 1: Find campaign + engagement candidate ──
    if outreach_id:
        outreach = await db.get_outreach(outreach_id)
        if not outreach:
            await client.close()
            return f"Outreach not found: {outreach_id}"
        campaign = await db.get_campaign(outreach["campaign_id"])
        if not campaign:
            await client.close()
            return "Campaign not found for this outreach."
        campaign_id = campaign["id"]
        candidate = await db.get_outreach_with_contact(outreach_id)
        if not candidate:
            await client.close()
            return "Could not load contact data for this outreach."

        # Exclusion gate
        from ..db.global_contact_queries import is_excluded_by_contact_id
        if await run_db(is_excluded_by_contact_id, candidate.get("contact_id", "")):
            await client.close()
            return (
                f"Skipped {candidate.get('name', 'Unknown')} — excluded from automation.\n\n"
                "This contact has the 'do-not-automate' tag or 'do_not_contact' lifecycle."
            )
    else:
        campaign, err = await db.find_active_campaign(campaign_id)
        if not campaign:
            await client.close()
            return err
        campaign_id = campaign["id"]

        # Block engagement when campaign is paused
        if campaign.get("status") == "paused":
            await client.close()
            return (
                f"Campaign '{campaign['name']}' is paused.\n\n"
                "No engagement will be sent while the campaign is paused.\n"
                "Use resume_campaign() to resume."
            )

        candidates = await db.get_engagement_candidates(campaign_id, MAX_ENGAGEMENTS_PER_OUTREACH)

        # Filter out excluded contacts
        if candidates:
            from ..db.global_contact_queries import is_excluded_by_contact_id
            filtered = []
            for c in candidates:
                if not await run_db(is_excluded_by_contact_id, c.get("contact_id", "")):
                    filtered.append(c)
            candidates = filtered

        if not candidates:
            await client.close()
            return (
                f"No prospects available for engagement in '{campaign['name']}'.\n\n"
                "Prospects need to be in the campaign first.\n"
                "Use generate_and_send() to reach new prospects."
            )
        # Will iterate through candidates below to find one with posts
        candidate = None
        outreach_id = ""

    # ── Step 2: Check monthly limits ──
    tier = get_tier()
    if tier != TIER_PRO:
        usage = await db.get_monthly_usage()
        monthly_engagements = usage.get("engagements_sent", 0)
        if monthly_engagements >= FREE_MAX_ENGAGEMENTS:
            await client.close()
            return (
                f"Free tier limit reached: {FREE_MAX_ENGAGEMENTS} engagements/month.\n\n"
                "Upgrade to Pro ($29/mo) for more engagements."
            )

    # ── Step 2a: Handle view action (lightest warm-up, no posts needed) ──
    if action == "view":
        if candidate is None:
            candidate = candidates[0] if candidates else None
            if candidate:
                outreach_id = candidate.get("outreach_id", "")

        if candidate is None:
            await client.close()
            return (
                "No prospects available for profile view.\n\n"
                "Prospects need to be in the campaign first.\n"
                "Use generate_and_send() to reach new prospects."
            )

        return await _handle_view(
            client, account_id, outreach_id, candidate, mode,
            campaign_id=campaign_id,
        )

    # ── Step 2b: Handle follow action (no posts needed) ──
    if action == "follow":
        # For follow, we just need a candidate — no need to fetch posts
        if candidate is None:
            # Pick the first candidate from the list
            candidate = candidates[0] if candidates else None
            if candidate:
                outreach_id = candidate.get("outreach_id", "")

        if candidate is None:
            await client.close()
            return (
                "No prospects available for follow.\n\n"
                "Prospects need to be in the campaign first.\n"
                "Use generate_and_send() to reach new prospects."
            )

        return await _handle_follow(
            client, account_id, outreach_id, candidate, mode,
            campaign_id=campaign_id,
        )

    # ── Step 2c: Handle endorse action (no posts needed) ──
    if action == "endorse":
        if candidate is None:
            candidate = candidates[0] if candidates else None
            if candidate:
                outreach_id = candidate.get("outreach_id", "")

        if candidate is None:
            await client.close()
            return (
                "No prospects available for endorsement.\n\n"
                "Prospects need to be in the campaign first.\n"
                "Use generate_and_send() to reach new prospects."
            )

        return await _handle_endorse(
            client, account_id, outreach_id, candidate, mode,
            campaign_id=campaign_id,
        )

    # ── Step 2d: Handle reply_comment action ──
    if action == "reply_comment":
        if candidate is None:
            candidate = candidates[0] if candidates else None
            if candidate:
                outreach_id = candidate.get("outreach_id", "")

        if candidate is None:
            await client.close()
            return (
                "No prospects available for comment replies.\n\n"
                "Use engage_prospect(action='comment') first to start conversations."
            )

        return await _handle_reply_comment(
            client, account_id, outreach_id, candidate, mode,
            campaign_id=campaign_id,
        )

    # ── Step 3: Fetch prospect's recent posts ──
    # If candidate was set by outreach_id, use single-candidate list
    if candidate is not None:
        candidates_to_try = [candidate]
    # else candidates list was populated above

    skipped_names: list[str] = []
    posts: list[dict[str, Any]] = []

    for cand in (candidates_to_try if candidate is not None else candidates):
        # Use provider_id from profile_json — Unipile requires the internal
        # provider ID (starts with ACo...), NOT the public LinkedIn slug.
        profile_data = {}
        if cand.get("profile_json"):
            try:
                profile_data = json.loads(cand["profile_json"])
            except (json.JSONDecodeError, TypeError):
                pass

        prospect_identifier = profile_data.get("provider_id", "")
        if not prospect_identifier:
            # Fallback: try linkedin_id or extract from URL
            prospect_identifier = cand.get("linkedin_id", "")
        if not prospect_identifier:
            url = cand.get("linkedin_url", "")
            if "/in/" in url:
                prospect_identifier = url.split("/in/")[-1].strip("/")

        if not prospect_identifier:
            skipped_names.append(cand.get("name", "Unknown"))
            continue

        got_422 = False
        try:
            posts = await client.get_user_posts(account_id, prospect_identifier, limit=5)
        except Exception as e:
            logger.error(f"Failed to fetch posts for {cand.get('name')}: {e}")
            posts = []

        # Detect _status_code sentinel (e.g. 422 from Unipile)
        if posts and isinstance(posts[0], dict) and "_status_code" in posts[0]:
            got_422 = True
            posts = []

        # Fallback: search_posts by prospect name when get_user_posts fails
        if not posts and got_422:
            prospect_name_for_search = cand.get("name", "")
            if prospect_name_for_search:
                try:
                    search_results, _ = await client.search_posts(
                        account_id, prospect_name_for_search, limit=10,
                    )
                    # Filter to posts authored by this prospect
                    for sr in search_results:
                        if _is_post_by_prospect(sr, cand):
                            posts.append({
                                "id": sr.get("post_id", ""),
                                "text": sr.get("text", ""),
                                "date": sr.get("timestamp", ""),
                                "metrics": {},
                            })
                    if posts:
                        logger.info(
                            f"search_posts fallback found {len(posts)} posts "
                            f"for {prospect_name_for_search}"
                        )
                except Exception as e:
                    logger.warning(f"search_posts fallback failed for {prospect_name_for_search}: {e}")

        if posts:
            # Persist discovered posts + author
            for p in posts:
                p_id = p.get("id", "")
                p_text = p.get("text", "")
                if p_id and p_text:
                    await db.upsert_post(
                        p_id,
                        author_linkedin_id=cand.get("linkedin_id", ""),
                        author_name=cand.get("name", ""),
                        text=p_text[:2000],
                        metrics_json=json.dumps(p.get("metrics", {})) if p.get("metrics") else "",
                        source="search",
                    )
            candidate = cand
            outreach_id = cand.get("outreach_id", outreach_id)
            break
        else:
            skipped_names.append(cand.get("name", "Unknown"))
            # Time-limited cooldown so prospect becomes eligible again later
            cand_outreach_id = cand.get("outreach_id", "")
            if cand_outreach_id:
                # Shorter cooldowns when invite-blocked — re-check prospects faster
                from ..linkedin.rate_limiter import can_send_now, BLOCK_DAILY, BLOCK_WEEKLY
                _, _, block_type = await can_send_now()
                invite_blocked = block_type in (BLOCK_DAILY, BLOCK_WEEKLY)
                if invite_blocked:
                    # Shorter cooldowns when invite-blocked (24h vs 48h)
                    cooldown = 24 * 3600 if got_422 else 24 * 3600
                else:
                    cooldown = COOLDOWN_422_ERROR if got_422 else COOLDOWN_NO_POSTS
                cooldown_until = int(time.time()) + cooldown
                await db.update_outreach(
                    cand_outreach_id,
                    next_action=json.dumps({"skip_engagement_until": cooldown_until}),
                )
                await db.log_action(
                    "engagement_skipped",
                    outreach_id=cand_outreach_id,
                    result="no_posts_cooldown",
                    details={
                        "prospect": cand.get("name", "Unknown"),
                        "got_422": got_422,
                        "cooldown_hours": cooldown // 3600,
                    },
                )

    prospect_name = candidate.get("name", "Unknown") if candidate else "Unknown"
    prospect_title = candidate.get("title", "") if candidate else ""
    prospect_company = candidate.get("company", "") if candidate else ""
    role_str = prospect_title
    if prospect_company:
        role_str += f" at {prospect_company}" if role_str else prospect_company

    # ── Step 4: Handle no posts ──
    if not posts or candidate is None:
        await client.close()
        if skipped_names:
            names_str = ", ".join(skipped_names)
            return (
                f"No recent posts found for any candidate ({names_str}).\n\n"
                "None of the available prospects have posted recently.\n"
                "Try send_followup() for a DM instead, or wait for new content."
            )
        return (
            f"No recent posts found for {prospect_name} ({role_str}).\n\n"
            "This prospect hasn't posted recently, so engagement isn't possible right now.\n"
            "Try send_followup() for a DM instead, or engage_prospect() with a different prospect."
        )

    # ── Step 4b: Filter already-engaged posts (account-wide dedup) ──
    # Level 1: Per-outreach dedup (same prospect's posts)
    per_outreach_ids = await db.get_engaged_post_ids(outreach_id)
    # Level 2: Account-wide dedup — prevent same LinkedIn account from
    # commenting on the same post via different outreaches
    account_engaged_ids = await db.get_account_engaged_post_ids(account_id)
    engaged_ids = per_outreach_ids | account_engaged_ids

    if engaged_ids:
        posts = [p for p in posts if p.get("id", "") not in engaged_ids]
        if not posts:
            was_global = bool(account_engaged_ids - per_outreach_ids)
            await client.close()
            if was_global:
                return (
                    f"All recent posts by {prospect_name} were already engaged "
                    "by another outreach from this account.\n\n"
                    "This prevents duplicate comments on the same post.\n"
                    "Wait for new content, or try a different prospect."
                )
            return (
                f"All recent posts by {prospect_name} have already been engaged.\n\n"
                "Wait for new content, or try a different prospect.\n"
                "Use engage_prospect() again to auto-pick the next candidate."
            )

    # ── Step 5: Pick best post + decide action ──
    # Simple heuristic: pick most recent post with substantial text (>50 chars)
    target_post = posts[0]  # Default to most recent
    for post in posts:
        text = post.get("text", "")
        if len(text) > 50:
            target_post = post
            break

    if action == "react":
        return await _handle_reaction(
            client, account_id, outreach_id, candidate, target_post, mode,
            campaign_id=campaign_id,
        )

    # Read engagement_mode from campaign config
    campaign_config = json.loads(campaign.get("config_json") or "{}")
    engagement_mode = campaign_config.get("engagement_mode", "auto")

    # For "auto": mixed strategy — respects engagement_mode config
    post_text = target_post.get("text", "")
    if action == "auto" and await _should_react_auto(outreach_id, post_text, engagement_mode):
        return await _handle_reaction(
            client, account_id, outreach_id, candidate, target_post, mode,
            campaign_id=campaign_id,
        )

    # ── Step 6: Generate comment ──
    sender_profile = await db.get_setting("profile", {})
    voice_signature = await db.get_setting("voice_signature", {})

    prospect_data = json.loads(candidate.get("profile_json", "{}")) if candidate.get("profile_json") else {
        "name": prospect_name,
        "title": prospect_title,
        "company": prospect_company,
        "headline": f"{prospect_title} at {prospect_company}" if prospect_company else prospect_title,
    }

    # ── Prospect Intelligence: load cached or generate ──
    prospect_analysis = None
    contact_db_id = candidate.get("contact_id") or candidate.get("contact_db_id", "")
    if contact_db_id:
        prospect_analysis = await db.get_contact_analysis(contact_db_id)
    if not prospect_analysis:
        campaign_config = json.loads(campaign.get("config_json") or "{}")
        icp_data = json.loads(campaign.get("icp_json") or "{}")
        campaign_context = {
            "target_description": campaign_config.get("target_description", ""),
            "relevance_hook": icp_data.get("relevance_hook", ""),
        }
        try:
            prospect_analysis = await analyze_prospect(
                prospect=prospect_data,
                campaign_context=campaign_context,
                icp_data=icp_data,
            )
            if contact_db_id:
                await db.save_contact_analysis(contact_db_id, prospect_analysis)
        except Exception as e:
            logger.warning(f"Prospect analysis failed, proceeding without: {e}")

    # ── Generate → Improve → Validate → Fix pipeline ──
    comment_text = ""
    style = ""
    reasoning = {}
    validation = None

    # Attempt 1: Generate + Improve + Validate (+ Fix if needed)
    try:
        result = await generate_comment(
            prospect=prospect_data,
            sender_profile=sender_profile,
            voice_signature=voice_signature,
            post_data=target_post,
            max_chars=COMMENT_MAX_CHARS,
            prospect_analysis=prospect_analysis,
        )
        comment_text = result.get("comment", "")
        style = result.get("style", "")
        reasoning = result.get("reasoning", {})
    except Exception as e:
        logger.error(f"Comment generation failed: {e}")
        await client.close()
        return f"Failed to generate comment: {e}"

    # Improve stage — polish for naturalness
    try:
        comment_text = await improve_message(
            draft=comment_text,
            voice_signature=voice_signature,
            message_type="comment",
            max_chars=COMMENT_MAX_CHARS,
        )
    except Exception as e:
        logger.warning(f"Improve stage failed, using raw comment: {e}")

    # Validate
    validation = validate_comment(comment_text, voice_signature, max_chars=COMMENT_MAX_CHARS)

    # Fix stage — if validation failed, surgically fix issues
    if not validation.is_valid:
        logger.info(f"Comment validation failed, attempting fix: {validation.issues}")
        try:
            comment_text = await fix_message(
                message=comment_text,
                issues=validation.issues,
                voice_signature=voice_signature,
                message_type="comment",
                max_chars=COMMENT_MAX_CHARS,
            )
            validation = validate_comment(comment_text, voice_signature, max_chars=COMMENT_MAX_CHARS)
        except Exception as e:
            logger.warning(f"Fix stage failed: {e}")

    # Last resort: regenerate from scratch if still invalid
    if not validation.is_valid:
        logger.info(f"Fix failed, regenerating comment from scratch: {validation.issues}")
        try:
            result = await generate_comment(
                prospect=prospect_data,
                sender_profile=sender_profile,
                voice_signature=voice_signature,
                post_data=target_post,
                max_chars=COMMENT_MAX_CHARS,
                prospect_analysis=prospect_analysis,
            )
            comment_text = result.get("comment", "")
            style = result.get("style", "")
            reasoning = result.get("reasoning", {})
            comment_text = await improve_message(
                draft=comment_text,
                voice_signature=voice_signature,
                message_type="comment",
                max_chars=COMMENT_MAX_CHARS,
            )
            validation = validate_comment(comment_text, voice_signature, max_chars=COMMENT_MAX_CHARS)
        except Exception as e:
            logger.error(f"Regeneration failed: {e}")

    if not validation or not validation.is_valid:
        issues_text = "\n".join(f"  ⚠️ {issue}" for issue in (validation.issues if validation else []))
        if mode == "autopilot":
            logger.warning(f"Autopilot blocked invalid comment: {issues_text}")
            await db.log_action("validation_blocked", outreach_id=outreach_id, result="blocked",
                       details={"issues": validation.issues if validation else [], "type": "comment"})
            await client.close()
            return (
                f"⚠️ Comment for {prospect_name} failed validation "
                f"after Generate → Improve → Fix pipeline.\n\n"
                f"Issues:\n{issues_text}\n\n"
                "The comment was NOT posted to protect your account.\n"
                "Try: engage_prospect(mode='copilot') to review and edit manually."
            )
        else:
            logger.warning(f"Copilot comment has validation warnings: {issues_text}")

    # ── Step 7: Copilot vs Autopilot ──
    post_preview = post_text[:150]
    if len(post_text) > 150:
        post_preview += "..."

    fit_score = candidate.get("fit_score", 0)

    if False:  # copilot mode removed
        # Store proposed action for later approval
        await db.update_outreach(outreach_id, next_action=json.dumps({
            "type": "comment",
            "post_id": target_post.get("id", ""),
            "comment": comment_text,
            "post_text": post_text[:500],
        }))

        output = [
            f"Comment for **{prospect_name}** ({role_str}):",
            f"   Fit: {stars(fit_score)}",
            "",
            f"   Post: \"{post_preview}\"",
            "",
            f'   Comment: "{comment_text}"',
            f"   ({len(comment_text)}/{COMMENT_MAX_CHARS} chars)",
            "",
        ]

        if style:
            output.append(f"   Style: {style}")
        if reasoning:
            hook = reasoning.get("post_hook", "")
            angle = reasoning.get("angle", "")
            if hook:
                output.append(f"   Hook: {hook}")
            if angle:
                output.append(f"   Angle: {angle}")
            output.append("")

        if validation and validation.warnings:
            for w in validation.warnings:
                output.append(f"   {w}")
            output.append("")

        output.extend([
            "Post this? Reply with:",
            "  'yes' / 'send' to post this comment",
            "  'react' to just like the post instead",
            "  'skip' to skip this prospect",
            "  'edit: [your text]' to post a custom comment instead",
            "  'stop' to pause the campaign",
        ])

        await client.close()
        return "\n".join(line for line in output if line is not None)

    else:
        # Autopilot — send immediately
        return await _send_comment(
            client, account_id, outreach_id, candidate, target_post,
            comment_text, style, reasoning,
            campaign_id=campaign_id,
        )


def _is_post_by_prospect(search_result: dict, candidate: dict) -> bool:
    """Check if a search_posts result was authored by the given prospect."""
    author_name = (search_result.get("author_name") or "").lower().strip()
    prospect_name = (candidate.get("name") or "").lower().strip()
    if not author_name or not prospect_name:
        return False
    # Exact match or one name contains the other
    if author_name == prospect_name:
        return True
    # Check if all parts of the prospect name appear in the author name
    parts = prospect_name.split()
    if len(parts) >= 2 and all(p in author_name for p in parts):
        return True
    # Check author_id matches provider_id
    author_id = search_result.get("author_id", "")
    if author_id:
        profile_data = {}
        if candidate.get("profile_json"):
            try:
                profile_data = json.loads(candidate["profile_json"])
            except (json.JSONDecodeError, TypeError):
                pass
        provider_id = profile_data.get("provider_id", "")
        if provider_id and author_id == provider_id:
            return True
    return False


async def _handle_reaction(
    client: Any,
    account_id: str,
    outreach_id: str,
    candidate: dict,
    target_post: dict,
    mode: str,
    campaign_id: str = "",
) -> str:
    """Handle a reaction (LIKE) on a post."""
    prospect_name = candidate.get("name", "Unknown")
    post_preview = target_post.get("text", "")[:100]
    if len(target_post.get("text", "")) > 100:
        post_preview += "..."
    post_id = target_post.get("id", "")

    if False:  # copilot mode removed
        await db.update_outreach(outreach_id, next_action=json.dumps({
            "type": "react",
            "post_id": post_id,
        }))

        output = [
            f"React to **{prospect_name}**'s post:",
            f"   Post: \"{post_preview}\"",
            "",
            "   Action: Like this post",
            "",
            "Send this? Reply with:",
            "  'yes' / 'send' to like the post",
            "  'comment' to write a comment instead",
            "  'skip' to skip this prospect",
        ]
        await client.close()
        return "\n".join(output)

    # Autopilot — reserve DB slot BEFORE calling LinkedIn API
    engagement_id = await db.reserve_engagement(
        outreach_id=outreach_id,
        action_type="react",
        post_id=post_id,
        account_id=account_id,
        campaign_id=campaign_id,
    )
    if not engagement_id:
        await client.close()
        return (
            f"Post by {prospect_name} was already engaged by another outreach. "
            "Skipping to avoid duplicate."
        )

    try:
        result = await client.send_post_reaction(
            account_id, post_id, "LIKE",
            outreach_id=outreach_id,
            post_text=target_post.get("text", "")[:500],
        )
    except UnipileAuthError:
        await db.delete_engagement(engagement_id)
        await client.close()
        return "LinkedIn account disconnected. Run setup_profile() again."
    except Exception as e:
        await db.delete_engagement(engagement_id)
        await client.close()
        return f"Failed to react: {e}"
    finally:
        await client.close()

    if result.get("success"):
        await db.finalize_engagement(
            engagement_id=engagement_id,
            post_text=target_post.get("text", "")[:500],
            reaction_type="LIKE",
        )
        await db.increment_usage("engagements_sent")
        await db.log_action(
            "engagement_react",
            outreach_id=outreach_id,
            result="success",
            details={"prospect": prospect_name, "post_id": post_id},
        )
        # Verify reaction via get_post_reactions() (real double-confirmation)
        try:
            from ..services.engagement_verifier import verify_reaction_immediate
            await verify_reaction_immediate(client, account_id, engagement_id, post_id)
        except Exception:
            pass
        # Real-time anomaly check (fire-and-forget)
        try:
            from ..services.anomaly_detector import check_post_engagement_anomaly, log_anomalies
            anomaly = check_post_engagement_anomaly(post_id, account_id)
            if anomaly:
                log_anomalies([anomaly])
        except Exception:
            pass  # Never block engagement flow
        return f"Liked {prospect_name}'s post: \"{post_preview}\""
    else:
        error = result.get("error", "Unknown error")
        await db.delete_engagement(engagement_id)
        await db.log_action(
            "engagement_react_failed",
            outreach_id=outreach_id,
            result="error",
            details={"error": error},
        )
        return f"Reaction failed for {prospect_name}: {error}"


async def _send_comment(
    client: Any,
    account_id: str,
    outreach_id: str,
    candidate: dict,
    target_post: dict,
    comment_text: str,
    style: str,
    reasoning: dict,
    campaign_id: str = "",
) -> str:
    """Send a comment on a post and record it."""
    prospect_name = candidate.get("name", "Unknown")
    post_id = target_post.get("id", "")

    # Reserve DB slot BEFORE calling LinkedIn API to prevent race conditions.
    # The UNIQUE constraint on (post_id, account_id) ensures only one job wins.
    engagement_id = await db.reserve_engagement(
        outreach_id=outreach_id,
        action_type="comment",
        post_id=post_id,
        account_id=account_id,
        campaign_id=campaign_id,
    )
    if not engagement_id:
        await client.close()
        return (
            f"Post by {prospect_name} was already engaged by another outreach. "
            "Skipping to avoid duplicate."
        )

    try:
        result = await client.send_post_comment(
            account_id, post_id, comment_text,
            outreach_id=outreach_id,
            post_text=target_post.get("text", "")[:500],
        )
    except UnipileAuthError:
        await db.delete_engagement(engagement_id)
        await client.close()
        return "LinkedIn account disconnected. Run setup_profile() again."
    except Exception as e:
        await db.delete_engagement(engagement_id)
        await client.close()
        return f"Failed to send comment: {e}"
    finally:
        await client.close()

    if result.get("success"):
        await db.finalize_engagement(
            engagement_id=engagement_id,
            post_text=target_post.get("text", "")[:500],
            text=comment_text,
            reasoning=json.dumps({"style": style, **reasoning}),
        )
        await db.increment_usage("engagements_sent")
        await db.log_action(
            "engagement_comment",
            outreach_id=outreach_id,
            result="success",
            details={
                "prospect": prospect_name,
                "post_id": post_id,
                "comment_length": len(comment_text),
                "style": style,
                "reasoning": reasoning,
            },
        )

        # Immediate comment verification — confirm it actually appeared
        try:
            from ..services.engagement_verifier import verify_comment_immediate
            await verify_comment_immediate(
                client, account_id, engagement_id, post_id, comment_text,
            )
        except Exception:
            pass  # Never block engagement flow

        # Real-time anomaly check (fire-and-forget)
        try:
            from ..services.anomaly_detector import check_post_engagement_anomaly, log_anomalies
            anomaly = check_post_engagement_anomaly(post_id, account_id)
            if anomaly:
                log_anomalies([anomaly])
        except Exception:
            pass  # Never block engagement flow

        output = f"Commented on {prospect_name}'s post:\n"
        output += f'   "{comment_text}"'
        if style:
            output += f"\n\n   Style: {style}"
        return output
    else:
        error = result.get("error", "Unknown error")
        await db.delete_engagement(engagement_id)
        await db.log_action(
            "engagement_comment_failed",
            outreach_id=outreach_id,
            result="error",
            details={"error": error},
        )

        # Fallback: try a reaction (LIKE) instead of giving up
        logger.info(f"Comment failed for {prospect_name}, falling back to reaction: {error}")
        try:
            react_result = await client.send_post_reaction(account_id, post_id, "LIKE")
            if react_result.get("success"):
                fallback_eid = await db.save_engagement(
                    outreach_id=outreach_id,
                    action_type="react",
                    post_id=post_id,
                    post_text=target_post.get("text", "")[:500],
                    reaction_type="LIKE",
                    status="sent",
                    campaign_id=campaign_id,
                    account_id=account_id,
                )
                # Verify fallback reaction via get_post_reactions()
                try:
                    from ..services.engagement_verifier import verify_reaction_immediate
                    await verify_reaction_immediate(client, account_id, fallback_eid, post_id)
                except Exception:
                    pass
                await db.increment_usage("engagements_sent")
                await db.log_action(
                    "engagement_react_fallback",
                    outreach_id=outreach_id,
                    result="success",
                    details={"prospect": prospect_name, "post_id": post_id, "original_error": error},
                )
                return (
                    f"Comment failed for {prospect_name} ({error}), "
                    f"but liked their post instead."
                )
        except Exception as react_err:
            logger.warning(f"Reaction fallback also failed: {react_err}")

        return f"Comment failed for {prospect_name}: {error}"


async def _handle_view(
    client: Any,
    account_id: str,
    outreach_id: str,
    candidate: dict,
    mode: str,
    campaign_id: str = "",
) -> str:
    """Handle a profile view action (lightest warm-up before any other interaction)."""
    prospect_name = candidate.get("name", "Unknown")
    prospect_title = candidate.get("title", "")
    prospect_company = candidate.get("company", "")
    role_str = prospect_title
    if prospect_company:
        role_str += f" at {prospect_company}" if role_str else prospect_company
    fit_score = candidate.get("fit_score", 0)

    # Extract provider_id from profile_json
    profile_data = {}
    if candidate.get("profile_json"):
        try:
            profile_data = json.loads(candidate["profile_json"])
        except (json.JSONDecodeError, TypeError):
            pass

    provider_id = profile_data.get("provider_id", "")
    if not provider_id:
        provider_id = candidate.get("linkedin_id") or ""
    if not provider_id:
        url = candidate.get("linkedin_url") or ""
        if "/in/" in url:
            provider_id = url.split("/in/")[-1].strip("/")

    if not provider_id:
        await client.close()
        return f"Cannot view {prospect_name}: no LinkedIn identifier found."

    if False:  # copilot mode removed
        await db.update_outreach(outreach_id, next_action=json.dumps({
            "type": "view",
            "provider_id": provider_id,
        }))

        output = [
            f"View **{prospect_name}**'s profile ({role_str})?",
            f"   Fit: {stars(fit_score)}",
            "",
            "   Action: View their LinkedIn profile",
            '   (Triggers a notification: "X viewed your profile")',
            "",
            "Send this? Reply with:",
            "  'yes' / 'send' to view their profile",
            "  'skip' to skip this prospect",
            "  'stop' to pause the campaign",
        ]
        await client.close()
        return "\n".join(output)

    # Autopilot — view immediately
    try:
        result = await client.view_profile(account_id, provider_id)
    except UnipileAuthError:
        await client.close()
        return "LinkedIn account disconnected. Run setup_profile() again."
    except Exception as e:
        await client.close()
        return f"Failed to view profile: {e}"
    finally:
        await client.close()

    if result.get("success"):
        engagement_id = await db.save_engagement(
            outreach_id=outreach_id,
            action_type="profile_view",
            post_id="",
            post_text="",
            text=f"Viewed {prospect_name}'s profile",
            status="sent",
            campaign_id=campaign_id,
            account_id=account_id,
        )
        await db.increment_usage("engagements_sent")
        await db.log_action(
            "engagement_profile_view",
            outreach_id=outreach_id,
            result="success",
            details={"prospect": prospect_name, "provider_id": provider_id},
        )
        # Mark trust_api — no verification API for profile views
        try:
            from ..services.engagement_verifier import mark_trust_api
            await mark_trust_api(engagement_id)
        except Exception:
            pass
        return (
            f"Viewed **{prospect_name}**'s profile ({role_str})\n\n"
            'They\'ll get a notification: "X viewed your profile".\n'
            "This is the subtlest warm-up signal before following."
        )
    else:
        error = result.get("error", "Unknown error")
        await db.log_action(
            "engagement_profile_view_failed",
            outreach_id=outreach_id,
            result="error",
            details={"error": error, "prospect": prospect_name},
        )
        return f"Profile view failed for {prospect_name}: {error}"


async def _handle_follow(
    client: Any,
    account_id: str,
    outreach_id: str,
    candidate: dict,
    mode: str,
    campaign_id: str = "",
) -> str:
    """Handle a profile follow action (warm-up before connecting)."""
    prospect_name = candidate.get("name", "Unknown")
    prospect_title = candidate.get("title", "")
    prospect_company = candidate.get("company", "")
    role_str = prospect_title
    if prospect_company:
        role_str += f" at {prospect_company}" if role_str else prospect_company
    fit_score = candidate.get("fit_score", 0)

    # Extract provider_id from profile_json
    profile_data = {}
    if candidate.get("profile_json"):
        try:
            profile_data = json.loads(candidate["profile_json"])
        except (json.JSONDecodeError, TypeError):
            pass

    provider_id = profile_data.get("provider_id", "")
    if not provider_id:
        provider_id = candidate.get("linkedin_id") or ""
    if not provider_id:
        url = candidate.get("linkedin_url") or ""
        if "/in/" in url:
            provider_id = url.split("/in/")[-1].strip("/")

    if not provider_id:
        await client.close()
        return f"Cannot follow {prospect_name}: no LinkedIn identifier found."

    # Pre-flight dedup: check if already followed (race condition guard)
    try:
        def _check_follow_dedup(oid: str) -> bool:
            from ..db.schema import get_db as _get_db
            _conn = _get_db()
            row = _conn.execute(
                "SELECT 1 FROM engagements WHERE outreach_id = ? AND action_type = 'follow' LIMIT 1",
                (oid,),
            ).fetchone()
            _conn.close()
            return row is not None

        has_follow = await run_db(_check_follow_dedup, outreach_id)
        if has_follow:
            await client.close()
            return f"Already followed {prospect_name} — skipping duplicate."
    except Exception:
        pass  # Proceed if dedup check fails

    if False:  # copilot mode removed
        # Store proposed action for later approval
        await db.update_outreach(outreach_id, next_action=json.dumps({
            "type": "follow",
            "provider_id": provider_id,
        }))

        output = [
            f"Follow **{prospect_name}** ({role_str})?",
            f"   Fit: {stars(fit_score)}",
            "",
            "   Action: Follow their profile on LinkedIn",
            "   (Triggers a notification: \"X started following you\")",
            "",
            "Send this? Reply with:",
            "  'yes' / 'send' to follow their profile",
            "  'skip' to skip this prospect",
            "  'stop' to pause the campaign",
        ]
        await client.close()
        return "\n".join(output)

    # Autopilot — follow immediately
    try:
        result = await client.follow_profile(account_id, provider_id)
    except UnipileAuthError:
        await client.close()
        return "LinkedIn account disconnected. Run setup_profile() again."
    except Exception as e:
        await client.close()
        return f"Failed to follow: {e}"
    finally:
        await client.close()

    if result.get("success"):
        engagement_id = await db.save_engagement(
            outreach_id=outreach_id,
            action_type="follow",
            post_id="",
            post_text="",
            text=f"Followed {prospect_name}",
            status="sent",
            campaign_id=campaign_id,
            account_id=account_id,
        )
        await db.increment_usage("engagements_sent")
        await db.log_action(
            "engagement_follow",
            outreach_id=outreach_id,
            result="success",
            details={"prospect": prospect_name, "provider_id": provider_id},
        )
        # Verify follow via check_follow_status() (real double-confirmation)
        try:
            from ..services.engagement_verifier import verify_follow_immediate
            await verify_follow_immediate(client, account_id, provider_id, engagement_id)
        except Exception:
            pass
        return (
            f"Followed **{prospect_name}** ({role_str})\n\n"
            "They'll get a notification: \"X started following you\".\n"
            "This warms them up for a future connection request."
        )
    else:
        error = result.get("error", "Unknown error")
        await db.log_action(
            "engagement_follow_failed",
            outreach_id=outreach_id,
            result="error",
            details={"error": error, "prospect": prospect_name},
        )
        return f"Follow failed for {prospect_name}: {error}"


async def _handle_endorse(
    client: Any,
    account_id: str,
    outreach_id: str,
    candidate: dict,
    mode: str,
    campaign_id: str = "",
) -> str:
    """Handle a skill endorsement action (high-visibility warm-up)."""
    from ..constants import ENDORSEMENT_ENABLED
    if not ENDORSEMENT_ENABLED:
        await client.close()
        return (
            "Endorsement is temporarily disabled (Unipile endpoint unreliable). "
            "Skipping to next warm-up action."
        )
    prospect_name = candidate.get("name", "Unknown")
    prospect_title = candidate.get("title", "")
    prospect_company = candidate.get("company", "")
    role_str = prospect_title
    if prospect_company:
        role_str += f" at {prospect_company}" if role_str else prospect_company
    fit_score = candidate.get("fit_score", 0)

    # Extract provider_id from profile_json
    profile_data = {}
    if candidate.get("profile_json"):
        try:
            profile_data = json.loads(candidate["profile_json"])
        except (json.JSONDecodeError, TypeError):
            pass

    provider_id = profile_data.get("provider_id", "")
    if not provider_id:
        provider_id = candidate.get("linkedin_id") or ""
    if not provider_id:
        url = candidate.get("linkedin_url") or ""
        if "/in/" in url:
            provider_id = url.split("/in/")[-1].strip("/")

    if not provider_id:
        await client.close()
        return f"Cannot endorse {prospect_name}: no LinkedIn identifier found."

    if False:  # copilot mode removed
        # Store proposed action for later approval
        await db.update_outreach(outreach_id, next_action=json.dumps({
            "type": "endorse",
            "provider_id": provider_id,
        }))

        output = [
            f"Endorse **{prospect_name}**'s skills ({role_str})?",
            f"   Fit: {stars(fit_score)}",
            "",
            "   Action: Endorse their skills on LinkedIn",
            "   (Triggers a high-visibility notification: \"X endorsed your skills\")",
            "",
            "Send this? Reply with:",
            "  'yes' / 'send' to endorse their skills",
            "  'skip' to skip this prospect",
            "  'stop' to pause the campaign",
        ]
        await client.close()
        return "\n".join(output)

    # Autopilot — endorse immediately
    try:
        result = await client.endorse_skill(account_id, provider_id)
    except UnipileAuthError:
        await client.close()
        return "LinkedIn account disconnected. Run setup_profile() again."
    except Exception as e:
        await client.close()
        return f"Failed to endorse: {e}"
    finally:
        await client.close()

    if result.get("success"):
        engagement_id = await db.save_engagement(
            outreach_id=outreach_id,
            action_type="endorse",
            post_id="",
            post_text="",
            text=f"Endorsed {prospect_name}'s skills",
            status="sent",
            campaign_id=campaign_id,
            account_id=account_id,
        )
        await db.increment_usage("engagements_sent")
        await db.log_action(
            "engagement_endorse",
            outreach_id=outreach_id,
            result="success",
            details={"prospect": prospect_name, "provider_id": provider_id},
        )
        # Mark trust_api — no verification API for endorsements
        try:
            from ..services.engagement_verifier import mark_trust_api
            await mark_trust_api(engagement_id)
        except Exception:
            pass
        return (
            f"Endorsed **{prospect_name}**'s skills ({role_str})\n\n"
            "They'll get a notification: \"X endorsed your skills\".\n"
            "This is a high-visibility warm-up before connecting."
        )
    else:
        error = result.get("error", "Unknown error")
        await db.log_action(
            "engagement_endorse_failed",
            outreach_id=outreach_id,
            result="error",
            details={"error": error, "prospect": prospect_name},
        )
        return f"Endorsement failed for {prospect_name}: {error}"


async def _handle_reply_comment(
    client: Any,
    account_id: str,
    outreach_id: str,
    candidate: dict[str, Any],
    mode: str,
    campaign_id: str = "",
) -> str:
    """Monitor and reply to prospect's responses on our comments.

    Checks posts we've previously commented on, finds prospect replies,
    and generates a contextual reply to continue the thread.
    """
    prospect_name = candidate.get("name", "Unknown")
    title = candidate.get("title", "")
    company = candidate.get("company", "")
    role_str = f"{title} at {company}" if title and company else (title or company)

    # Find our previous engagements (comments) on this outreach
    def _fetch_comment_engagements(oid: str) -> list:
        from ..db.schema import get_db as _get_db
        _conn = _get_db()
        rows = _conn.execute(
            """SELECT post_id, text, action_type FROM engagements
               WHERE outreach_id = ? AND action_type = 'comment'
               ORDER BY created_at DESC LIMIT 5""",
            (oid,),
        ).fetchall()
        _conn.close()
        return rows

    engagements = await run_db(_fetch_comment_engagements, outreach_id)

    if not engagements:
        await client.close()
        return (
            f"No previous comments on {prospect_name}'s posts.\n\n"
            "Use engage_prospect(action='comment') first to start a conversation."
        )

    # Check each commented post for new replies
    for eng in engagements:
        e = dict(eng)
        post_id = e.get("post_id", "")
        our_comment = e.get("text", "")
        if not post_id:
            continue

        try:
            comments = await client.get_post_comments(account_id, post_id, limit=30)
        except Exception:
            continue

        if not comments:
            continue

        # Find replies from the prospect (by checking author name or ID)
        prospect_replies = []
        for c in comments:
            author = c.get("author_name", "")
            # Simple name match — not perfect but practical
            if author and prospect_name.split()[0].lower() in author.lower():
                prospect_replies.append(c)

        if not prospect_replies:
            continue

        # Found a reply — generate a response
        latest_reply = prospect_replies[-1]
        reply_text = latest_reply.get("text", "")
        reply_comment_id = latest_reply.get("comment_id", "")

        if not reply_text or not reply_comment_id:
            continue

        # Generate reply using LLM
        try:
            voice = await db.get_setting("voice_signature", {})
            from ..ai.llm_router import call_llm

            prompt = f"""Generate a brief reply to this LinkedIn comment thread.

Your original comment: "{our_comment}"
{prospect_name}'s reply: "{reply_text}"

Write a natural, voice-matched reply (2-3 sentences max).
Voice style: {voice.get('style', 'professional')}
Tone: {voice.get('tone', 'conversational')}

Keep it short and conversational. If they asked a question, answer it.
If they agreed, build on the point. Aim to advance the relationship.

Return ONLY the reply text."""

            reply_content = await call_llm(prompt, max_tokens=200)
        except Exception as e:
            await client.close()
            return f"Failed to generate reply: {e}"

        if not reply_content:
            continue

        # Copilot mode: show for review
        if False:  # copilot mode removed
            await db.update_outreach(outreach_id, next_action=json.dumps({
                "type": "reply_comment",
                "post_id": post_id,
                "comment_id": reply_comment_id,
                "text": reply_content,
            }))

            output = [
                f"Comment reply for **{prospect_name}** ({role_str}):",
                "",
                f'   Their reply: "{reply_text[:120]}"',
                f'   Your reply:  "{reply_content}"',
                "",
                "Send this? Reply with:",
                "  'yes' / 'send' to reply",
                "  'skip' to skip",
                "  'edit: [your text]' to send custom reply",
            ]
            await client.close()
            return "\n".join(output)

        # Autopilot: send reply
        try:
            result = await client.reply_to_comment(
                account_id, post_id, reply_comment_id, reply_content,
            )
        except Exception as e:
            await client.close()
            return f"Failed to reply: {e}"
        finally:
            await client.close()

        if result.get("success"):
            reply_eid = await db.save_engagement(
                outreach_id=outreach_id,
                action_type="reply_comment",
                post_id=post_id,
                post_text=reply_text[:500],
                text=reply_content,
                status="sent",
                campaign_id=campaign_id,
                account_id=account_id,
            )
            # Immediate verification — confirm reply comment appeared
            try:
                from ..services.engagement_verifier import verify_comment_immediate
                await verify_comment_immediate(
                    client, account_id, reply_eid, post_id, reply_content,
                )
            except Exception:
                pass
            await db.increment_usage("engagements_sent")
            await db.log_action(
                "engagement_reply_comment",
                outreach_id=outreach_id,
                result="success",
                details={
                    "prospect": prospect_name,
                    "their_reply": reply_text[:200],
                    "our_reply": reply_content[:200],
                },
            )
            return (
                f"Replied to **{prospect_name}**'s comment ({role_str})\n\n"
                f'   Their comment: "{reply_text[:80]}..."\n'
                f'   Your reply: "{reply_content[:80]}..."\n\n'
                "Thread engagement builds stronger relationships before connecting."
            )
        else:
            return f"Comment reply failed: {result.get('error', 'Unknown error')}"

    await client.close()
    return (
        f"No new replies from {prospect_name} on your comments.\n\n"
        "They haven't responded to your comments yet. Try engaging with a new post."
    )
