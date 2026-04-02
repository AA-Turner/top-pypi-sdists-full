"""Tool: brand_strategy — Analyze and improve your LinkedIn personal brand.

Audits your profile, generates a 4-week strategy, executes actions
(auto-publish posts, auto-comment/react/follow, profile suggestions),
and tracks progress.

Fully automated execution:
  - Posts: generated with voice matching and published immediately
  - Engagement: finds trending posts in your niche, comments/reacts/follows
  - Profile edits: auto-applied via Unipile PATCH /api/v1/users/me/edit
"""

from __future__ import annotations

import logging
import time as _time
from typing import Any

from ..db.queries import (
    get_campaign_stats,
    get_rate_limit_today,
    get_sending_days_7d,
    get_setting,
    get_weekly_invitation_sum,
    list_campaigns,
    log_action,
    save_engagement,
)
from ..formatter import progress_bar, stars, table, tree
from ..linkedin import get_account_id, get_linkedin_client, UnipileError
from ..services.brand_service import (
    capture_baseline,
    compute_progress,
    count_plan_progress,
    get_next_pending_action,
    load_brand_analysis,
    load_brand_baseline,
    load_brand_plan,
    mark_action_completed,
    save_brand_analysis,
    save_brand_baseline,
    save_brand_plan,
)
from ..services.health_score import compute_health_score
from ..db.async_bridge import run_db

logger = logging.getLogger(__name__)


async def run_brand_strategy(
    action: str = "analyze",
    focus: str = "",
    photo: str = "",
) -> str:
    """Main handler for brand_strategy tool."""

    # ── Pre-checks ──
    setup_done = await run_db(get_setting, "setup_complete", False)
    if not setup_done:
        return (
            "Setup required before analyzing your brand.\n\n"
            "Please run setup_profile first."
        )

    account_id = get_account_id()
    if not account_id:
        return "No LinkedIn account connected. Run setup_profile first."

    if action == "analyze":
        return await _handle_analyze(account_id, focus)
    elif action == "plan":
        return await _handle_plan(account_id, focus)
    elif action == "execute":
        return await _handle_execute(account_id)
    elif action == "progress":
        return await _handle_progress(account_id)
    elif action == "upload_photo":
        return await _handle_upload_photo(account_id, photo)
    elif action == "upload_cover":
        return await _handle_upload_cover(account_id, photo)
    elif action == "set_link":
        return await _handle_set_link(account_id, focus)
    elif action == "makeover":
        return await _handle_makeover(account_id)
    elif action == "photo_enhance":
        return await _handle_photo_enhance(account_id)
    elif action == "test_headline":
        return _handle_test_headline(focus)
    else:
        return (
            "Unknown action. Available actions:\n\n"
            '  brand_strategy(action="analyze")       — Full profile audit\n'
            '  brand_strategy(action="plan")          — Generate 4-week strategy\n'
            '  brand_strategy(action="execute")       — Execute next action\n'
            '  brand_strategy(action="progress")      — Track before/after metrics\n'
            '  brand_strategy(action="upload_photo")  — Upload profile photo\n'
            '  brand_strategy(action="upload_cover")  — Upload cover photo\n'
            '  brand_strategy(action="set_link", focus="https://...")  — Set custom CTA link\n'
            '  brand_strategy(action="makeover")      — One-click full profile optimization\n'
            '  brand_strategy(action="photo_enhance") — Auto-enhance profile photo settings\n'
            '  brand_strategy(action="test_headline", focus="Variant A | Variant B")  — Start headline A/B test'
        )


# ──────────────────────────────────────────────
# Action: analyze
# ──────────────────────────────────────────────


async def _handle_analyze(account_id: str, focus: str) -> str:
    """Full profile audit with scored areas."""

    from ..ai.brand_strategist import analyze_brand_profile
    from ..services.brand_service import get_active_icp_context

    # ── Gather data ──
    profile = await run_db(get_setting, "profile", {})
    voice = await run_db(get_setting, "voice_signature", {})
    expertise = await run_db(get_setting, "expertise_map", {})
    icp_context = get_active_icp_context()

    # Fetch SSI and posts
    ssi_data: dict[str, Any] = {}
    posts: list[dict] = []
    try:
        client = get_linkedin_client()
        try:
            ssi_data = await client.get_ssi_score(account_id)
        except Exception as e:
            logger.warning("SSI fetch failed: %s", e)

        provider_id = profile.get("provider_id", "")
        if provider_id:
            try:
                posts = await client.get_posts(account_id, provider_id)
            except Exception as e:
                logger.warning("Posts fetch failed: %s", e)
        await client.close()
    except Exception as e:
        logger.warning("Client init failed: %s", e)

    # Aggregate campaign stats
    campaign_stats = await _aggregate_campaign_stats()

    # ── Run LLM analysis ──
    analysis = await analyze_brand_profile(
        profile, posts, ssi_data, campaign_stats, voice, expertise,
        icp_context=icp_context,
    )

    # ── Save ──
    save_brand_analysis(analysis)

    # ── Format output ──
    return _format_analysis(analysis, focus)


async def _aggregate_campaign_stats() -> dict[str, Any]:
    """Aggregate acceptance and reply rates across all campaigns."""
    campaigns = await run_db(list_campaigns)
    total_invited = 0
    total_connected = 0
    total_replied = 0

    for c in campaigns:
        if c.get("status") in ("draft", "archived"):
            continue
        stats = await run_db(get_campaign_stats, c["id"])
        total_invited += stats.get("invited", 0)
        total_connected += stats.get("connected", 0)
        total_replied += stats.get("replied", 0)

    acceptance_rate = total_connected / total_invited if total_invited > 0 else 0
    reply_rate = total_replied / total_connected if total_connected > 0 else 0

    return {
        "acceptance_rate": acceptance_rate,
        "reply_rate": reply_rate,
        "total_invited": total_invited,
        "total_connected": total_connected,
        "total_replied": total_replied,
    }


def _format_analysis(analysis: dict[str, Any], focus: str) -> str:
    """Format brand analysis for chat display."""
    overall = analysis.get("overall_score", 0)
    areas = analysis.get("areas", {})
    top_actions = analysis.get("top_3_actions", [])

    # Overall score with rating
    if overall >= 80:
        rating = "Excellent"
    elif overall >= 60:
        rating = "Good"
    elif overall >= 40:
        rating = "Needs Work"
    else:
        rating = "Critical"

    lines = [
        f"Brand Profile Audit (Score: {overall}/100 — {rating})",
        "",
    ]

    # ── Each area ──
    area_order = ["headline", "summary", "content", "profile_completeness", "ssi_breakdown", "engagement"]
    area_labels = {
        "headline": "Headline",
        "summary": "Summary/About",
        "content": "Content Strategy",
        "profile_completeness": "Profile Completeness",
        "ssi_breakdown": "SSI Score",
        "engagement": "Engagement",
    }

    for key in area_order:
        area = areas.get(key, {})
        if not area:
            continue

        if focus and focus != "all" and focus != key:
            continue

        label = area_labels.get(key, key)
        score = area.get("score", 0)
        lines.append(f"{label}: {score}/10 {stars(score, 10)}")

        # Area-specific details
        if key == "headline":
            current = area.get("current", "")
            if current:
                lines.append(f"  Current: \"{current}\"")
            suggestion = area.get("suggestion", "")
            if suggestion:
                lines.append(f"  Suggested: \"{suggestion}\"")

        issues = area.get("issues", [])
        if issues:
            for issue in issues[:3]:
                lines.append(f"  - {issue}")

        if key == "profile_completeness":
            missing = area.get("missing", [])
            if missing:
                lines.append(f"  Missing: {', '.join(missing)}")

        if key == "ssi_breakdown":
            improvements = area.get("improvements", [])
            for imp in improvements[:3]:
                lines.append(f"  - {imp}")

        lines.append("")

    # ── Top 3 actions ──
    if top_actions:
        lines.append("Top 3 Actions:")
        for i, action in enumerate(top_actions, 1):
            lines.append(f"  {i}. {action}")
        lines.append("")

    lines.append('Next: Run brand_strategy(action="plan") to generate a 4-week improvement plan.')

    return "\n".join(lines)


# ──────────────────────────────────────────────
# Action: plan
# ──────────────────────────────────────────────


async def _handle_plan(account_id: str, focus: str) -> str:
    """Generate a 4-week brand strategy plan."""

    from ..ai.brand_strategist import generate_brand_plan
    from ..services.brand_service import get_active_icp_context

    # Require existing analysis
    analysis = load_brand_analysis()
    if not analysis:
        return (
            "No brand analysis found.\n\n"
            'Run brand_strategy(action="analyze") first to audit your profile.'
        )

    profile = await run_db(get_setting, "profile", {})
    voice = await run_db(get_setting, "voice_signature", {})
    expertise = await run_db(get_setting, "expertise_map", {})
    icp_context = get_active_icp_context()

    # ── Generate plan via LLM ──
    plan = await generate_brand_plan(
        analysis, profile, voice, expertise, focus or "all",
        icp_context=icp_context,
    )

    if not plan.get("weeks"):
        return "Failed to generate brand plan. Please try again."

    plan["focus"] = focus or "all"

    # ── Capture baseline ──
    ssi_data: dict[str, Any] = {}
    try:
        client = get_linkedin_client()
        ssi_data = await client.get_ssi_score(account_id)
        await client.close()
    except Exception:
        pass

    campaign_stats = await _aggregate_campaign_stats()
    hs = _compute_current_health(ssi_data, campaign_stats)

    baseline = capture_baseline(profile, ssi_data, hs.total, campaign_stats.get("acceptance_rate", 0))
    save_brand_baseline(baseline)

    # ── Save plan ──
    save_brand_plan(plan)

    # ── Format output ──
    return _format_plan(plan)


def _format_plan(plan: dict[str, Any]) -> str:
    """Format brand strategy plan for chat display."""
    lines = [
        "4-Week Brand Strategy",
        "",
    ]

    for week in plan.get("weeks", []):
        week_num = week.get("week", "?")
        theme = week.get("theme", "")
        lines.append(f"Week {week_num}: {theme}")

        actions = week.get("actions", [])
        for i, action in enumerate(actions):
            is_last = i == len(actions) - 1
            prefix = "└──" if is_last else "├──"
            desc = action.get("description", "")
            action_type = action.get("type", "")
            icon = {"profile_optimize": "✏️", "post": "📝", "engagement": "💬", "photo_enhance": "📸"}.get(action_type, "📌")
            lines.append(f"  {prefix} {icon} {desc}")

        lines.append("")

    # Content calendar
    calendar = plan.get("content_calendar", [])
    if calendar:
        lines.append("Content Calendar:")
        for entry in calendar:
            day = entry.get("day", "")
            ctype = entry.get("type", "")
            topic = entry.get("example_topic", "")
            lines.append(f"  {day}: {ctype} — {topic}")
        lines.append("")

    # Engagement targets
    targets = plan.get("engagement_targets", {})
    if targets:
        lines.append("Weekly Targets:")
        lines.append(f"  Posts: {targets.get('weekly_posts', 2)}/week")
        lines.append(f"  Comments: {targets.get('daily_comments', 5)}/day")
        lines.append(f"  Reactions: {targets.get('daily_reactions', 10)}/day")
        lines.append("")

    completed, total = count_plan_progress(plan)
    lines.append(f"Progress: {completed}/{total} actions")
    lines.append(f"  {progress_bar(completed, total, 20)}")
    lines.append("")
    lines.append('Next: Run brand_strategy(action="execute") to start working on your plan.')

    return "\n".join(lines)


# ──────────────────────────────────────────────
# Action: execute
# ──────────────────────────────────────────────


async def _handle_execute(account_id: str) -> str:
    """Execute the next pending action from the plan."""

    plan = load_brand_plan()
    if not plan:
        return (
            "No brand strategy plan found.\n\n"
            'Run brand_strategy(action="plan") first to generate a plan.'
        )

    action = get_next_pending_action(plan)
    if not action:
        return (
            "All brand strategy actions completed!\n\n"
            'Run brand_strategy(action="progress") to see your results.'
        )

    action_type = action.get("type", "")
    action_id = action.get("id", "")

    if action_type == "post":
        return await _execute_post_action(action, action_id, account_id)
    elif action_type == "profile_optimize":
        return await _execute_profile_action(action, action_id)
    elif action_type == "photo_enhance":
        return await _handle_photo_enhance(account_id, action_id=action_id)
    elif action_type == "engagement":
        return await _execute_engagement_action(action, action_id, account_id)
    else:
        mark_action_completed(action_id, "Skipped — unknown type")
        return f"Skipped unknown action type: {action_type}. Moving to next."


async def _execute_post_action(action: dict[str, Any], action_id: str, account_id: str) -> str:
    """Generate and auto-publish a LinkedIn post."""
    topic = action.get("topic", action.get("description", ""))
    tone = action.get("tone", "thought-leader")

    profile = await run_db(get_setting, "profile", {})
    voice = await run_db(get_setting, "voice_signature", {})

    name = profile.get("name", "")
    title = profile.get("title", "")
    company = profile.get("company", "")
    industry = profile.get("industry", "")
    voice_tone = voice.get("tone", "")
    voice_patterns = ", ".join(voice.get("communication_style", [])[:5])

    prompt = f"""Write a LinkedIn post for {name} ({title} at {company}).
Industry: {industry}
Writing style: {voice_tone}
Tone: {tone}
Patterns: {voice_patterns}

Topic: {topic}

Requirements:
- Write in first person, using {name}'s voice and style
- Keep it between 150-1200 characters (optimal LinkedIn engagement)
- Include a hook in the first line to stop scrolling
- Use short paragraphs (1-3 sentences each)
- End with a question or call-to-action to drive engagement
- Do NOT use hashtags unless the user's style includes them
- Do NOT use emojis unless the user's style includes them
- Be authentic and conversational, not corporate
- Share a genuine insight, story, or perspective

Return ONLY the post text, nothing else."""

    try:
        from ..config import has_local_llm_key, is_backend_mode

        if is_backend_mode() and not has_local_llm_key():
            # Route through backend — use generate_message endpoint with post context
            client = get_linkedin_client()
            resp = await client.generate_message(
                {"name": name, "title": title, "company": company, "industry": industry},
                {"name": "audience", "title": "LinkedIn audience"},
                voice,
                {
                    "target": f"LinkedIn post about: {topic}",
                    "type": "post",
                    "max_chars": "1200",
                    "instructions": prompt,
                },
            )
            post_text = resp.get("message", "")
            await client.close()
        else:
            from ..ai.llm import LLMClient

            llm = LLMClient()
            post_text = await llm.generate(prompt, max_tokens=800)
    except Exception as e:
        logger.error("Brand post generation failed: %s", e)
        mark_action_completed(action_id, f"Failed: {e}")
        return f"Failed to generate post: {e}"

    if not post_text or len(post_text) < 30:
        mark_action_completed(action_id, "Failed: empty post")
        return "Failed to generate post content. Try again."

    # ── Auto-publish ──
    try:
        client = get_linkedin_client()
        result = await client.create_post(account_id, post_text)
        await client.close()

        if result.get("success"):
            await run_db(log_action, "brand_post_published", details={
                "topic": topic, "tone": tone, "chars": len(post_text),
                "post_id": result.get("post_id", ""),
            })
            mark_action_completed(action_id, f"Published: {topic[:50]}")

            plan = load_brand_plan()
            completed, total = count_plan_progress(plan) if plan else (0, 0)

            return (
                f"Brand Strategy: Post Published!\n\n"
                f'   "{post_text[:300]}{"..." if len(post_text) > 300 else ""}"\n'
                f"   ({len(post_text)} chars)\n\n"
                f"Tip: Reply to comments in the first 2 hours to boost reach.\n\n"
                f"Progress: {completed}/{total} actions completed"
            )
        else:
            error = result.get("error", "Unknown error")
            mark_action_completed(action_id, f"Publish failed: {error}")
            return f"Post generated but publish failed: {error}\n\nDraft:\n{post_text}"
    except Exception as e:
        mark_action_completed(action_id, f"Publish failed: {e}")
        return f"Post generated but publish failed: {e}\n\nDraft:\n{post_text}"


async def _execute_profile_action(action: dict[str, Any], action_id: str) -> str:
    """Generate profile optimization and auto-apply via Unipile PATCH endpoint."""
    from ..ai.brand_strategist import generate_brand_action
    from ..services.brand_service import get_active_icp_context

    profile = await run_db(get_setting, "profile", {})
    voice = await run_db(get_setting, "voice_signature", {})
    analysis = load_brand_analysis() or {}
    subtype = action.get("subtype", "headline")
    icp_context = get_active_icp_context()

    # For education/open_to_work — use action description directly (no LLM generation needed)
    if subtype in ("education", "open_to_work"):
        return await _execute_direct_profile_action(action, action_id, subtype)

    result = await generate_brand_action(
        action, profile, voice, analysis, icp_context=icp_context,
    )

    if result.get("error"):
        return f"Failed to generate suggestion: {result['error']}"

    # ── Auto-apply via profile editor (with change tracking) ──
    from .profile_editor import apply_profile_change

    provider_id = profile.get("provider_id", "")
    account_id = get_account_id()
    auto_applied = False

    if provider_id and account_id:
        try:
            client = get_linkedin_client()
            if subtype == "headline" and result.get("options"):
                best = result["options"][0]["text"]
                apply_result = await apply_profile_change(
                    client, account_id, provider_id, "headline", best,
                    source="brand_strategy",
                )
                if apply_result.get("success"):
                    auto_applied = True
                    logger.info("Auto-applied headline: %s", best[:50])
                else:
                    logger.warning(
                        "Auto-apply headline failed: %s",
                        apply_result.get("error", "unknown error"),
                    )
            elif subtype == "summary" and result.get("summary"):
                apply_result = await apply_profile_change(
                    client, account_id, provider_id, "summary", result["summary"],
                    source="brand_strategy",
                )
                if apply_result.get("success"):
                    auto_applied = True
                    logger.info("Auto-applied summary update")
                else:
                    logger.warning(
                        "Auto-apply summary failed: %s",
                        apply_result.get("error", "unknown error"),
                    )
            await client.close()
        except Exception as e:
            logger.warning("Auto-apply %s failed (falling back to suggestions): %s", subtype, e)

    completion_note = f"Auto-applied {subtype}" if auto_applied else f"Generated {subtype} suggestions"
    mark_action_completed(action_id, completion_note)

    plan = load_brand_plan()
    completed, total = count_plan_progress(plan) if plan else (0, 0)

    if auto_applied:
        # Profile was updated automatically
        if subtype == "headline":
            best = result["options"][0]["text"]
            lines = [
                f"Brand Strategy: Headline Updated Automatically!",
                "",
                f'  New headline: "{best}"',
                f"  Rationale: {result['options'][0].get('rationale', '')}",
                "",
            ]
        else:
            lines = [
                f"Brand Strategy: Summary Updated Automatically!",
                "",
                f"  {result['summary'][:300]}{'...' if len(result.get('summary', '')) > 300 else ''}",
                "",
            ]
        lines.append(f"Progress: {completed}/{total} actions completed")
        return "\n".join(lines)

    # Fallback: show suggestions for manual application
    lines = [
        f"Brand Strategy: Optimize {subtype.title()}",
        "(Auto-apply was not possible — please apply manually)",
        "",
    ]

    if subtype == "headline":
        options = result.get("options", [])
        if options:
            for i, opt in enumerate(options, 1):
                text = opt.get("text", "")
                rationale = opt.get("rationale", "")
                lines.append(f"Option {i}: \"{text}\"")
                if rationale:
                    lines.append(f"  Why: {rationale}")
                lines.append("")
            lines.append("Copy your preferred headline and update it on LinkedIn.")
        else:
            lines.append("Could not generate headline options.")

    elif subtype == "summary":
        summary = result.get("summary", "")
        hook = result.get("hook", "")
        if summary:
            lines.append("Suggested About Section:")
            lines.append("")
            lines.append(f"  {summary}")
            lines.append("")
            if hook:
                lines.append(f"Hook (first 2 lines): \"{hook}\"")
                lines.append("")
            lines.append("Copy this to your LinkedIn About section and customize as needed.")
        else:
            lines.append("Could not generate summary.")

    lines.append("")
    lines.append(f"Progress: {completed}/{total} actions completed")

    return "\n".join(lines)


async def _execute_engagement_action(
    action: dict[str, Any], action_id: str, account_id: str,
) -> str:
    """Auto-execute engagement: find trending posts, comment/react/follow."""
    desc = action.get("description", "")
    target = action.get("target_count", 5)
    engagement_type = action.get("engagement_type", "comment")  # comment, react, follow

    profile = await run_db(get_setting, "profile", {})
    voice = await run_db(get_setting, "voice_signature", {})
    expertise = await run_db(get_setting, "expertise_map", {})

    # Derive search keywords from user's expertise and industry
    keywords = expertise.get("credible_topics", expertise.get("core", ""))
    if not keywords:
        keywords = profile.get("industry", profile.get("title", ""))

    results: list[str] = []
    errors: list[str] = []
    count = 0

    try:
        client = get_linkedin_client()

        # ── Step 1: Discover trending posts in the user's niche ──
        posts: list[dict] = []
        try:
            search_results, _ = await client.search_posts(
                account_id, keywords, limit=min(target * 2, 20),
            )
            for sr in search_results:
                post_id = sr.get("post_id", sr.get("id", ""))
                text = sr.get("text", "")
                author = sr.get("author_name", "")
                if post_id and text and len(text) > 30:
                    author_lid = sr.get("author_provider_id", sr.get("provider_id", ""))
                    posts.append({
                        "post_id": post_id,
                        "text": text,
                        "author": author,
                        "provider_id": author_lid,
                    })
                    # Persist post + author
                    from ..db.post_queries import upsert_post
                    await run_db(upsert_post, post_id,
                        author_linkedin_id=author_lid,
                        author_name=author,
                        text=text[:2000],
                        source="brand_strategy",)
        except Exception as e:
            logger.warning("Post search failed: %s", e)
            errors.append(f"Post search failed: {e}")

        # ── Step 2: Execute engagements ──
        for post in posts[:target]:
            post_id = post["post_id"]

            if engagement_type == "follow" and post.get("provider_id"):
                # Follow the post author
                try:
                    follow_result = await client.follow_profile(account_id, post["provider_id"])
                    if follow_result.get("success"):
                        await run_db(save_engagement, outreach_id="",
                            action_type="follow",
                            post_id=post_id,
                            post_text="",
                            text=f"Followed {post['author']}",
                            status="sent",
                            reasoning="brand_strategy",)
                        results.append(f"Followed {post['author']}")
                        count += 1
                    else:
                        err = follow_result.get("error", "unknown error")
                        logger.warning("Follow failed for %s: %s", post["author"], err)
                        errors.append(f"Follow failed ({post['author']}): {err}")
                except Exception as e:
                    errors.append(f"Follow failed ({post['author']}): {e}")
                continue

            if engagement_type == "react" or engagement_type == "like":
                # React to the post
                try:
                    react_result = await client.send_post_reaction(account_id, post_id, "LIKE")
                    if react_result.get("success"):
                        await run_db(save_engagement, outreach_id="",
                            action_type="react",
                            post_id=post_id,
                            post_text=post["text"][:500],
                            reaction_type="LIKE",
                            status="sent",
                            reasoning="brand_strategy",)
                        results.append(f"Liked post by {post['author']}")
                        count += 1
                    else:
                        err = react_result.get("error", "unknown error")
                        logger.warning("React failed for %s: %s", post["author"], err)
                        errors.append(f"React failed ({post['author']}): {err}")
                except Exception as e:
                    errors.append(f"React failed ({post['author']}): {e}")
                continue

            # Default: comment
            try:
                voice_tone = voice.get("tone", "professional")
                comment_prompt = f"""Write a brief, authentic LinkedIn comment on this post.

Post by {post['author']}:
"{post['text'][:500]}"

You are {profile.get('name', '')} ({profile.get('title', '')}).
Your voice: {voice_tone}

Rules:
- 50-200 characters max
- Be genuine, add value (insight, question, agreement with nuance)
- Match the user's voice tone
- No generic "Great post!" or "Thanks for sharing!"
- Do NOT use emojis unless the user's style includes them

Return ONLY the comment text."""

                from ..config import has_local_llm_key, is_backend_mode

                if is_backend_mode() and not has_local_llm_key():
                    resp = await client.generate_comment(
                        {"name": profile.get("name", ""), "title": profile.get("title", "")},
                        {"name": post["author"]},
                        voice,
                        {"text": post["text"][:500], "post_id": post["post_id"]},
                    )
                    comment_text = resp.get("comment", "")
                else:
                    from ..ai.llm import LLMClient

                    llm = LLMClient()
                    comment_text = await llm.generate(comment_prompt, max_tokens=200)
                if comment_text and len(comment_text) >= 10:
                    comment_result = await client.send_post_comment(account_id, post_id, comment_text)
                    if comment_result.get("success"):
                        await run_db(save_engagement, outreach_id="",
                            action_type="comment",
                            post_id=post_id,
                            post_text=post["text"][:500],
                            text=comment_text,
                            status="sent",
                            reasoning="brand_strategy",)
                        results.append(
                            f"Commented on {post['author']}'s post: "
                            f'"{comment_text[:60]}{"..." if len(comment_text) > 60 else ""}"'
                        )
                        count += 1
                    else:
                        err = comment_result.get("error", "unknown error")
                        logger.warning("Comment failed for %s: %s", post["author"], err)
                        errors.append(f"Comment failed ({post['author']}): {err}")
                else:
                    # Fallback to reaction if comment generation fails
                    fallback_result = await client.send_post_reaction(account_id, post_id, "LIKE")
                    if fallback_result.get("success"):
                        await run_db(save_engagement, outreach_id="",
                            action_type="react",
                            post_id=post_id,
                            post_text=post["text"][:500],
                            reaction_type="LIKE",
                            status="sent",
                            reasoning="brand_strategy",)
                        results.append(f"Liked post by {post['author']} (comment gen failed)")
                        count += 1
                    else:
                        err = fallback_result.get("error", "unknown error")
                        errors.append(f"React fallback failed ({post['author']}): {err}")
            except Exception as e:
                # Fallback to reaction on any error
                try:
                    fallback_result = await client.send_post_reaction(account_id, post_id, "LIKE")
                    if fallback_result.get("success"):
                        await run_db(save_engagement, outreach_id="",
                            action_type="react",
                            post_id=post_id,
                            post_text=post["text"][:500],
                            reaction_type="LIKE",
                            status="sent",
                            reasoning="brand_strategy",)
                        results.append(f"Liked post by {post['author']} (comment failed)")
                        count += 1
                    else:
                        err = fallback_result.get("error", "unknown error")
                        errors.append(f"Engage failed ({post['author']}): {err}")
                except Exception as fallback_err:
                    errors.append(f"Engage failed ({post['author']}): {e}; fallback also failed: {fallback_err}")

        await client.close()
    except Exception as e:
        logger.error("Engagement execution failed: %s", e)
        errors.append(f"Client error: {e}")

    await run_db(log_action, "brand_engagement", details={
        "type": engagement_type, "target": target,
        "completed": count, "keywords": keywords[:100],
    })

    mark_action_completed(action_id, f"{engagement_type}: {count}/{target}")

    plan = load_brand_plan()
    completed, total = count_plan_progress(plan) if plan else (0, 0)

    # ── Format output ──
    lines = [
        f"Brand Strategy: Engagement ({engagement_type.title()})",
        f"Target: {desc}",
        f"Completed: {count}/{target}",
        "",
    ]

    if results:
        lines.append("Actions taken:")
        for r in results:
            lines.append(f"  ✅ {r}")
        lines.append("")

    if errors:
        lines.append("Issues:")
        for e in errors[:3]:
            lines.append(f"  ⚠️ {e}")
        lines.append("")

    lines.append(f"Progress: {completed}/{total} actions completed")

    return "\n".join(lines)


# ──────────────────────────────────────────────
# Action: progress
# ──────────────────────────────────────────────


async def _handle_progress(account_id: str) -> str:
    """Show before/after metrics and action progress."""

    baseline = load_brand_baseline()
    plan = load_brand_plan()

    if not baseline or not plan:
        return (
            "No brand strategy in progress.\n\n"
            'Run brand_strategy(action="analyze") first, then brand_strategy(action="plan").'
        )

    # Fetch current metrics
    ssi_data: dict[str, Any] = {}
    try:
        client = get_linkedin_client()
        ssi_data = await client.get_ssi_score(account_id)
        await client.close()
    except Exception:
        pass

    campaign_stats = await _aggregate_campaign_stats()
    hs = _compute_current_health(ssi_data, campaign_stats)

    progress = compute_progress(
        baseline,
        ssi_data,
        campaign_stats.get("acceptance_rate", 0),
        hs.total,
        plan,
    )

    return _format_progress(progress, plan)


def _format_progress(progress: dict[str, Any], plan: dict[str, Any]) -> str:
    """Format progress report."""

    def _change_str(change: float | int, is_pct: bool = False) -> str:
        if change > 0:
            return f"+{change:.0%}" if is_pct else f"+{change}"
        elif change < 0:
            return f"{change:.0%}" if is_pct else f"{change}"
        return "—"

    lines = [
        f"Brand Strategy Progress (Day {progress['days_since_start']})",
        "",
    ]

    # Metrics comparison table
    headers = ["Metric", "Before", "Now", "Change"]
    rows = [
        [
            "SSI Score",
            str(progress["ssi_before"]),
            str(progress["ssi_now"]),
            _change_str(progress["ssi_change"]),
        ],
        [
            "Acceptance Rate",
            f"{progress['acceptance_before']:.0%}",
            f"{progress['acceptance_now']:.0%}",
            _change_str(progress["acceptance_change"], is_pct=True),
        ],
        [
            "Health Score",
            str(progress["health_before"]),
            str(progress["health_now"]),
            _change_str(progress["health_change"]),
        ],
    ]

    lines.append(table(headers, rows))
    lines.append("")

    # Action progress
    completed = progress["actions_completed"]
    total = progress["actions_total"]
    lines.append(f"Actions: {completed}/{total} completed")
    lines.append(f"  {progress_bar(completed, total, 20)}")
    lines.append("")

    # Per-week breakdown
    for week in plan.get("weeks", []):
        week_num = week.get("week", "?")
        theme = week.get("theme", "")
        actions = week.get("actions", [])
        week_done = sum(1 for a in actions if a.get("status") == "completed")
        week_total = len(actions)
        status_icon = "✅" if week_done == week_total else "⏳"
        lines.append(f"  {status_icon} Week {week_num}: {theme} ({week_done}/{week_total})")

    lines.append("")

    if completed < total:
        lines.append(f'{progress["actions_remaining"]} actions remaining.')
        lines.append('Run brand_strategy(action="execute") to continue.')
    else:
        lines.append("All actions completed! Great work on your personal brand.")
        lines.append('Run brand_strategy(action="analyze") for a fresh audit to measure improvement.')

    return "\n".join(lines)


# ──────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────


async def _handle_upload_photo(account_id: str, photo_input: str) -> str:
    """Handle profile photo upload via file path or base64 data."""
    if not photo_input:
        return (
            "Please provide your photo:\n\n"
            '  brand_strategy(action="upload_photo", photo="/path/to/your/photo.jpg")\n\n'
            "Or provide base64-encoded image data:\n"
            '  brand_strategy(action="upload_photo", photo="data:image/jpeg;base64,...")\n\n'
            "Supported formats: JPEG, PNG (recommended: 400x400px, under 8MB)"
        )

    import base64
    from pathlib import Path

    image_bytes: bytes | None = None
    content_type = "image/jpeg"

    # Option 1: Base64 data URI
    if photo_input.startswith("data:"):
        try:
            header, data = photo_input.split(",", 1)
            content_type = header.split(";")[0].replace("data:", "")
            image_bytes = base64.b64decode(data)
        except Exception as e:
            return f"Invalid base64 data URI: {e}"

    # Option 2: Raw base64 string (long string, not a file path)
    elif len(photo_input) > 500 and not photo_input.startswith("/"):
        try:
            image_bytes = base64.b64decode(photo_input)
        except Exception as e:
            return f"Invalid base64 data: {e}"

    # Option 3: File path
    else:
        path = Path(photo_input).expanduser()
        if not path.exists():
            return f"File not found: {photo_input}"
        if path.stat().st_size > 8 * 1024 * 1024:
            return "Photo must be under 8MB."
        image_bytes = path.read_bytes()
        suffix = path.suffix.lower().lstrip(".")
        content_type = {
            "jpg": "image/jpeg", "jpeg": "image/jpeg", "png": "image/png",
        }.get(suffix, "image/jpeg")

    if not image_bytes:
        return "Could not read the photo. Please provide a valid file path or base64 data."

    # Attempt upload (with change tracking)
    from .profile_editor import apply_profile_change

    profile = await run_db(get_setting, "profile", {})
    provider_id = profile.get("provider_id", "")

    try:
        client = get_linkedin_client()
        result = await apply_profile_change(
            client, account_id, provider_id, "photo", "<photo uploaded>",
            source="brand_strategy",
            image_bytes=image_bytes, content_type=content_type,
        )
        await client.close()

        if result.get("success"):
            await run_db(log_action, "brand_photo_uploaded", details={"size": len(image_bytes)})
            return (
                "Profile photo uploaded successfully!\n\n"
                "LinkedIn may take a few minutes to process and display your new photo.\n"
                "A professional headshot significantly improves connection acceptance rates."
            )
        else:
            error = result.get("error", "Unknown error")
            logger.warning("Photo upload via API failed: %s", error)
            return (
                f"Photo upload via API failed: {error}\n\n"
                "LinkedIn's API may not support direct photo uploads at this time.\n"
                "Please upload your photo manually:\n"
                "  1. Go to linkedin.com/in/me\n"
                "  2. Click the camera icon on your profile photo\n"
                "  3. Upload your photo\n\n"
                "A professional headshot increases profile views by 14x."
            )
    except Exception as e:
        return f"Photo upload failed: {e}\n\nPlease upload manually at linkedin.com/in/me"


async def _handle_upload_cover(account_id: str, photo_input: str) -> str:
    """Handle cover photo upload via file path or base64 data."""
    if not photo_input:
        return (
            "Please provide your cover photo:\n\n"
            '  brand_strategy(action="upload_cover", photo="/path/to/cover.jpg")\n\n'
            "Or provide base64-encoded image data:\n"
            '  brand_strategy(action="upload_cover", photo="data:image/jpeg;base64,...")\n\n'
            "Recommended: 1584x396px, under 8MB (JPEG or PNG)"
        )

    import base64
    from pathlib import Path

    image_bytes: bytes | None = None
    content_type = "image/jpeg"

    if photo_input.startswith("data:"):
        try:
            header, data = photo_input.split(",", 1)
            content_type = header.split(";")[0].replace("data:", "")
            image_bytes = base64.b64decode(data)
        except Exception as e:
            return f"Invalid base64 data URI: {e}"
    elif len(photo_input) > 500 and not photo_input.startswith("/"):
        try:
            image_bytes = base64.b64decode(photo_input)
        except Exception as e:
            return f"Invalid base64 data: {e}"
    else:
        path = Path(photo_input).expanduser()
        if not path.exists():
            return f"File not found: {photo_input}"
        if path.stat().st_size > 8 * 1024 * 1024:
            return "Cover photo must be under 8MB."
        image_bytes = path.read_bytes()
        suffix = path.suffix.lower().lstrip(".")
        content_type = {
            "jpg": "image/jpeg", "jpeg": "image/jpeg", "png": "image/png",
        }.get(suffix, "image/jpeg")

    if not image_bytes:
        return "Could not read the cover photo. Please provide a valid file path or base64 data."

    from .profile_editor import apply_profile_change

    profile = await run_db(get_setting, "profile", {})
    provider_id = profile.get("provider_id", "")

    try:
        client = get_linkedin_client()
        result = await apply_profile_change(
            client, account_id, provider_id, "cover_photo", "<cover photo uploaded>",
            source="brand_strategy",
            image_bytes=image_bytes, content_type=content_type,
        )
        await client.close()

        if result.get("success"):
            await run_db(log_action, "brand_cover_uploaded", details={"size": len(image_bytes)})
            return (
                "Cover photo uploaded successfully!\n\n"
                "LinkedIn may take a few minutes to process and display your new cover photo.\n"
                "A branded cover image reinforces your value proposition at a glance."
            )
        else:
            error = result.get("error", "Unknown error")
            return (
                f"Cover photo upload failed: {error}\n\n"
                "Please upload manually: linkedin.com/in/me → Edit intro → pencil on cover image."
            )
    except Exception as e:
        return f"Cover photo upload failed: {e}\n\nPlease upload manually at linkedin.com/in/me"


async def _handle_set_link(account_id: str, url: str) -> str:
    """Set the custom CTA link on the profile (e.g. Calendly, website)."""
    if not url:
        return (
            "Please provide the URL for your custom link:\n\n"
            '  brand_strategy(action="set_link", focus="https://cal.com/your-link")\n\n'
            "This sets the clickable CTA button on your LinkedIn profile.\n"
            "Common choices: Calendly, website, portfolio, lead magnet."
        )

    import json

    category = "WEBSITE"
    link_data = json.dumps({"category": category, "url": url})

    from .profile_editor import apply_profile_change

    profile = await run_db(get_setting, "profile", {})
    provider_id = profile.get("provider_id", "")

    try:
        client = get_linkedin_client()
        result = await apply_profile_change(
            client, account_id, provider_id, "custom_link", link_data,
            source="brand_strategy",
        )
        await client.close()

        if result.get("success"):
            await run_db(log_action, "brand_link_set", details={"url": url, "category": category})
            return (
                f"Custom link set successfully!\n\n"
                f"  Category: {category}\n"
                f"  URL: {url}\n\n"
                "Visitors to your profile will now see a clickable link button.\n"
                "This is one of the highest-conversion profile elements for outreach."
            )
        else:
            error = result.get("error", "Unknown error")
            return f"Failed to set custom link: {error}"
    except Exception as e:
        return f"Failed to set custom link: {e}"


def _compute_current_health(ssi_data: dict[str, Any], campaign_stats: dict[str, Any]):
    """Compute current health score from available data."""
    daily_record = await run_db(get_rate_limit_today)
    weekly = await run_db(get_weekly_invitation_sum)
    sending_days = await run_db(get_sending_days_7d)

    return compute_health_score(
        ssi_score=ssi_data.get("score", 0),
        acceptance_rate=campaign_stats.get("acceptance_rate", 0),
        total_sent=campaign_stats.get("total_invited", 0),
        daily_sent=daily_record.get("sent", 0) if isinstance(daily_record, dict) else daily_record,
        daily_limit=daily_record.get("daily_limit", 15) if isinstance(daily_record, dict) else 15,
        weekly_sent=weekly,
        sending_days_7d=sending_days,
    )


# ──────────────────────────────────────────────
# Action: photo_enhance
# ──────────────────────────────────────────────


async def _handle_photo_enhance(account_id: str, *, action_id: str = "") -> str:
    """Auto-enhance profile photo with Unipile's STUDIO filter."""
    import json

    from .profile_editor import apply_profile_change

    profile = await run_db(get_setting, "profile", {})
    provider_id = profile.get("provider_id", "")

    settings = {"filter": "STUDIO"}

    try:
        client = get_linkedin_client()
        result = await apply_profile_change(
            client, account_id, provider_id, "picture_settings",
            json.dumps(settings), source="brand_strategy",
        )
        await client.close()

        if action_id:
            mark_action_completed(action_id, "Applied STUDIO filter")

        if result.get("success"):
            await run_db(log_action, "brand_photo_enhanced", details=settings)
            return (
                "Profile photo enhanced!\n\n"
                "  Applied: STUDIO filter (professional look)\n\n"
                "LinkedIn's STUDIO filter optimizes contrast and lighting\n"
                "for a professional headshot appearance."
            )
        else:
            error = result.get("error", "Unknown error")
            return f"Photo enhancement failed: {error}"
    except Exception as e:
        if action_id:
            mark_action_completed(action_id, f"Failed: {e}")
        return f"Photo enhancement failed: {e}"


# ──────────────────────────────────────────────
# Action: makeover (one-click full profile optimization)
# ──────────────────────────────────────────────


async def _handle_makeover(account_id: str) -> str:
    """One-click full profile optimization using all available fields."""
    import json

    from ..ai.brand_strategist import generate_brand_action
    from ..services.brand_service import get_active_icp_context

    from .profile_editor import apply_profile_change

    profile = await run_db(get_setting, "profile", {})
    voice = await run_db(get_setting, "voice_signature", {})
    provider_id = profile.get("provider_id", "")
    analysis = load_brand_analysis()
    icp_context = get_active_icp_context()

    if not analysis:
        return (
            "No brand analysis found.\n\n"
            'Run brand_strategy(action="analyze") first to audit your profile.'
        )

    applied: list[str] = []
    failed: list[str] = []
    change_ids: list[str] = []

    client = get_linkedin_client()

    try:
        # ── 1. Headline ──
        headline_result = await generate_brand_action(
            {"subtype": "headline"}, profile, voice, analysis, icp_context=icp_context,
        )
        if headline_result.get("options"):
            best = headline_result["options"][0]["text"]
            r = await apply_profile_change(
                client, account_id, provider_id, "headline", best,
                source="makeover",
            )
            if r.get("success"):
                applied.append(f'Headline: "{best}"')
                if r.get("change_id"):
                    change_ids.append(r["change_id"])
            else:
                failed.append(f"Headline: {r.get('error', 'unknown')}")

        # ── 2. Summary ──
        summary_result = await generate_brand_action(
            {"subtype": "summary"}, profile, voice, analysis, icp_context=icp_context,
        )
        if summary_result.get("summary"):
            r = await apply_profile_change(
                client, account_id, provider_id, "summary", summary_result["summary"],
                source="makeover",
            )
            if r.get("success"):
                applied.append(f"Summary: updated ({len(summary_result['summary'])} chars)")
                if r.get("change_id"):
                    change_ids.append(r["change_id"])
            else:
                failed.append(f"Summary: {r.get('error', 'unknown')}")

        # ── 3. Photo enhancement ──
        r = await apply_profile_change(
            client, account_id, provider_id, "picture_settings",
            json.dumps({"filter": "STUDIO"}), source="makeover",
        )
        if r.get("success"):
            applied.append("Photo: STUDIO filter applied")
            if r.get("change_id"):
                change_ids.append(r["change_id"])
        else:
            failed.append(f"Photo settings: {r.get('error', 'unknown')}")

        # ── 4. Skills from brand audit ──
        areas = analysis.get("areas", {})
        missing = areas.get("profile_completeness", {}).get("missing", [])

        # Suggest skills based on expertise
        expertise = await run_db(get_setting, "expertise_map", {})
        core_skills = expertise.get("core", [])
        if isinstance(core_skills, str):
            core_skills = [s.strip() for s in core_skills.split(",") if s.strip()]
        current_skills = profile.get("skills", [])
        new_skills = [s for s in core_skills if s not in current_skills][:5]
        if new_skills:
            r = await apply_profile_change(
                client, account_id, provider_id, "skills",
                json.dumps(new_skills), source="makeover",
            )
            if r.get("success"):
                applied.append(f"Skills: added {', '.join(new_skills)}")
                if r.get("change_id"):
                    change_ids.append(r["change_id"])
            else:
                failed.append(f"Skills: {r.get('error', 'unknown')}")

        await client.close()
    except Exception as e:
        logger.error("Makeover failed: %s", e)
        failed.append(f"Error: {e}")
        try:
            await client.close()
        except Exception:
            pass

    await run_db(log_action, "brand_makeover", details={
        "applied": len(applied), "failed": len(failed),
    })

    lines = ["Profile Makeover Complete!", ""]

    if applied:
        lines.append("Applied:")
        for item in applied:
            lines.append(f"  {item}")
        lines.append("")

    if failed:
        lines.append("Could not apply:")
        for item in failed:
            lines.append(f"  {item}")
        lines.append("")

    if change_ids:
        lines.append(f"Change IDs (for rollback): {', '.join(change_ids)}")
        lines.append('Use profile_history(action="restore", change_id="...") to undo any change.')
        lines.append("")

    lines.append(f"Total: {len(applied)} applied, {len(failed)} skipped")

    return "\n".join(lines)


# ──────────────────────────────────────────────
# Direct profile actions (education, open_to_work)
# ──────────────────────────────────────────────


async def _execute_direct_profile_action(
    action: dict[str, Any], action_id: str, subtype: str,
) -> str:
    """Execute education/open_to_work profile actions from the brand plan."""
    import json

    from .profile_editor import apply_profile_change

    profile = await run_db(get_setting, "profile", {})
    provider_id = profile.get("provider_id", "")
    account_id = get_account_id()
    desc = action.get("description", "")

    if not account_id or not provider_id:
        mark_action_completed(action_id, "Skipped — no account")
        return f"Cannot auto-apply {subtype}: no LinkedIn account connected."

    # Extract structured data from action if available, otherwise skip
    data = action.get("data")
    if not data:
        mark_action_completed(action_id, f"Suggestion: {desc}")
        plan = load_brand_plan()
        completed, total = count_plan_progress(plan) if plan else (0, 0)
        return (
            f"Brand Strategy: {subtype.replace('_', ' ').title()} Suggestion\n\n"
            f"  {desc}\n\n"
            f"This action requires manual data input. Use the profile editor:\n"
            f'  Apply via: profile_editor(field="{subtype}", value=\'{{...}}\')\n\n'
            f"Progress: {completed}/{total} actions completed"
        )

    try:
        client = get_linkedin_client()
        result = await apply_profile_change(
            client, account_id, provider_id, subtype,
            json.dumps(data) if isinstance(data, dict) else data,
            source="brand_strategy",
        )
        await client.close()

        if result.get("success"):
            mark_action_completed(action_id, f"Auto-applied {subtype}")
            plan = load_brand_plan()
            completed, total = count_plan_progress(plan) if plan else (0, 0)
            return (
                f"Brand Strategy: {subtype.replace('_', ' ').title()} Updated!\n\n"
                f"  {desc}\n\n"
                f"Progress: {completed}/{total} actions completed"
            )
        else:
            error = result.get("error", "unknown")
            mark_action_completed(action_id, f"Failed: {error}")
            return f"Failed to apply {subtype}: {error}"
    except Exception as e:
        mark_action_completed(action_id, f"Failed: {e}")
        return f"Failed to apply {subtype}: {e}"


# ──────────────────────────────────────────────
# Action: test_headline (headline A/B testing)
# ──────────────────────────────────────────────


def _handle_test_headline(focus: str) -> str:
    """Start a headline A/B test.

    ``focus`` should be "Variant A headline | Variant B headline".
    Uses the first active campaign for tracking.
    """
    if not focus or "|" not in focus:
        return (
            "Start a headline A/B test:\n\n"
            '  brand_strategy(action="test_headline",\n'
            '    focus="AI-Powered Sales Leader | Building the Future of Outbound")\n\n'
            "Separate the two headline variants with a pipe (|).\n"
            "The test will alternate headlines across invite batches\n"
            "and measure acceptance/reply rate per variant.\n\n"
            "Auto-evaluates after 14 days or when 15+ prospects per variant."
        )

    parts = [p.strip() for p in focus.split("|", 1)]
    variant_a = parts[0]
    variant_b = parts[1]

    if len(variant_a) > 220 or len(variant_b) > 220:
        return "Headlines must be 220 characters or less."

    # Use the first active campaign
    campaigns = await run_db(list_campaigns, status="active")
    if not campaigns:
        campaigns = await run_db(list_campaigns)
    if not campaigns:
        return "No campaigns found. Create a campaign first to run a headline test."

    campaign_id = campaigns[0]["id"]
    campaign_name = campaigns[0].get("name", campaign_id[:8])

    from ..db.queries import create_ab_test, list_ab_tests

    # Check for existing running headline tests
    running = await run_db(list_ab_tests, campaign_id=campaign_id, status="running")
    headline_running = [t for t in running if t.get("test_type") == "headline"]
    if headline_running:
        existing = headline_running[0]
        return (
            f"A headline test is already running for campaign '{campaign_name}':\n\n"
            f'  A: "{existing["variant_a"]}"\n'
            f'  B: "{existing["variant_b"]}"\n\n'
            f"Wait for it to complete or cancel it first."
        )

    test_id = create_ab_test(
        campaign_id=campaign_id,
        name=f"Headline: {variant_a[:30]}... vs {variant_b[:30]}...",
        variant_a=variant_a,
        variant_b=variant_b,
        hypothesis="Which headline drives higher acceptance and reply rates?",
        test_type="headline",
    )

    return (
        f"Headline A/B Test Started!\n\n"
        f"  Campaign: {campaign_name}\n"
        f'  Variant A: "{variant_a}"\n'
        f'  Variant B: "{variant_b}"\n'
        f"  Test ID: {test_id[:8]}...\n\n"
        f"How it works:\n"
        f"  - Headlines alternate across invite batches\n"
        f"  - Each prospect tracks which headline was active\n"
        f"  - Acceptance rate and reply rate compared per variant\n"
        f"  - Auto-evaluates after 14 days or 15+ prospects per variant\n\n"
        f'Check progress: brand_strategy(action="progress")'
    )
