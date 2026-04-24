"""Tool: create_post — Generate and publish voice-matched posts.

Creates posts on LinkedIn, X/Twitter, or both using the user's voice signature.
Supports social selling by building authority and driving inbound connections.
"""

from __future__ import annotations

import logging

from ..db.queries import get_setting, log_action, save_published_post
from ..linkedin import get_account_id, get_linkedin_client, UnipileError
from ..db.async_bridge import run_db

logger = logging.getLogger(__name__)


async def run_create_post(
    topic: str = "",
    tone: str = "professional",
    mode: str = "autopilot",
    platforms: str = "linkedin",
) -> str:
    """Generate and publish a voice-matched post.

    Args:
        topic: What to post about.
        tone: Post tone: "professional", "casual", "thought-leader", "storytelling".
        mode: "autopilot" (publishes immediately).
        platforms: Comma-separated platforms: "linkedin", "x", or "linkedin,x".
    """

    # ── Pre-checks ──
    setup_done = await run_db(get_setting, "setup_complete", False)
    if not setup_done:
        return (
            "Setup required before creating posts.\n\n"
            "Please run setup_profile first."
        )

    if not topic:
        return (
            "Please provide a topic for the post.\n\n"
            "Examples:\n"
            '  create_post(topic="share a tip about cold outreach")\n'
            '  create_post(topic="comment on AI in sales")\n'
            '  create_post(topic="share a lesson learned this week")'
        )

    platform_list = [p.strip().lower() for p in platforms.split(",")]

    # Check at least one platform has credentials
    account_id = get_account_id()
    has_linkedin = "linkedin" in platform_list and bool(account_id)
    has_x = ("x" in platform_list or "twitter" in platform_list)

    if not has_linkedin and not has_x:
        return "No accounts connected. Run setup_profile first."

    # ── Load profile + voice ──
    profile = await run_db(get_setting, "profile", {})
    voice = await run_db(get_setting, "voice_signature", {})

    from ..ai.llm_router import call_llm

    name = profile.get("name", "")
    title = profile.get("title", "")
    company = profile.get("company", "")
    industry = profile.get("industry", "")
    voice_style = voice.get("style", "professional")
    voice_tone = voice.get("tone", "")
    voice_patterns = voice.get("patterns", [])
    patterns_str = ", ".join(voice_patterns[:5]) if voice_patterns else ""

    output_parts: list[str] = []

    # ── LinkedIn ──
    if has_linkedin:
        result = await _publish_linkedin(
            call_llm, account_id, topic, tone,
            name, title, company, industry, voice_style, voice_tone, patterns_str,
        )
        output_parts.append(result)

    # ── X/Twitter ──
    if has_x:
        result = await _publish_x(
            call_llm, topic, tone,
            name, title, company, industry, voice_style, voice_tone, patterns_str,
        )
        output_parts.append(result)

    return "\n\n---\n\n".join(output_parts)


async def _publish_linkedin(
    call_llm, account_id, topic, tone,
    name, title, company, industry, voice_style, voice_tone, patterns_str,
) -> str:
    """Generate and publish a LinkedIn post."""
    try:
        prompt = f"""Write a LinkedIn post for {name} ({title} at {company}).
Industry: {industry}
Writing style: {voice_style}
Tone: {voice_tone or tone}
Patterns: {patterns_str}

Topic: {topic}
Tone requested: {tone}

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

        post_text = await call_llm(prompt, max_tokens=800)
        if not post_text or len(post_text) < 30:
            return "LinkedIn: Failed to generate post content."
    except Exception as e:
        return f"LinkedIn: Failed to generate post: {e}"

    try:
        client = get_linkedin_client()
        result = await client.create_post(account_id, post_text)
        await client.close()

        if result.get("success"):
            post_id = result.get("post_id", "")
            await run_db(log_action, "post_created", details={
                "topic": topic, "tone": tone, "chars": len(post_text),
                "post_id": post_id, "platform": "linkedin",
            })
            if post_id:
                try:
                    await run_db(save_published_post, post_id=post_id, text=post_text[:500], topic=topic)
                except Exception:
                    pass
            return (
                f"LinkedIn post published!\n\n"
                f'   "{post_text[:200]}{"..." if len(post_text) > 200 else ""}"\n'
                f"   ({len(post_text)} chars)"
            )
        else:
            return f"LinkedIn: {result.get('error', 'Unknown error')}"
    except (UnipileError, Exception) as e:
        return f"LinkedIn publish failed: {e}"


async def _publish_x(
    call_llm, topic, tone,
    name, title, company, industry, voice_style, voice_tone, patterns_str,
) -> str:
    """Generate and publish an X/Twitter post via backend proxy."""
    try:
        prompt = f"""Write a tweet for {name} ({title} at {company}).
Industry: {industry}
Writing style: {voice_style}
Tone: {voice_tone or tone}
Patterns: {patterns_str}

Topic: {topic}
Tone requested: {tone}

Requirements:
- Write in first person, using {name}'s voice
- MUST be under 280 characters (strict Twitter limit)
- Hook immediately — no padding or filler
- Be provocative, insightful, or actionable
- Do NOT use hashtags unless the user's style includes them
- No emojis unless the user naturally uses them
- End with a punchy statement or question

Return ONLY the tweet text, nothing else."""

        tweet_text = await call_llm(prompt, max_tokens=400)
        if not tweet_text or len(tweet_text) < 10:
            return "X: Failed to generate tweet content."
        tweet_text = tweet_text.strip()
        if len(tweet_text) > 280:
            tweet_text = tweet_text[:277] + "..."
    except Exception as e:
        return f"X: Failed to generate tweet: {e}"

    # Post via backend proxy (which handles X OAuth tokens)
    try:
        from .. import config as cfg
        if cfg.is_backend_mode():
            client = get_linkedin_client()
            # Use the multi-platform proxy endpoint
            import httpx
            url = f"{client.base_url}/api/v1/posts"
            resp = await client._client.post(
                url,
                json={"text": tweet_text, "platforms": ["x"]},
                headers=client._headers(),
            )
            data = resp.json() if resp.status_code in (200, 201) else {}
            results = data.get("results", {})
            x_result = results.get("x", data)
            if x_result.get("success"):
                await run_db(log_action, "post_created", details={
                    "topic": topic, "tone": tone, "chars": len(tweet_text),
                    "post_id": x_result.get("post_id", ""), "platform": "x",
                })
                return (
                    f"X tweet published!\n\n"
                    f'   "{tweet_text}"\n'
                    f"   ({len(tweet_text)} chars)"
                )
            else:
                return f"X: {x_result.get('error', 'Unknown error')}"
        else:
            return "X posting requires backend mode. Set up backend connection first."
    except Exception as e:
        logger.error("X publish failed: %s", e)
        return f"X publish failed: {e}"
