"""Tool: create_post — Generate and publish a voice-matched LinkedIn post.

Creates LinkedIn posts using the user's voice signature and ICP pain points.
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
    mode: str = "copilot",
) -> str:
    """Generate and publish a voice-matched LinkedIn post.

    Args:
        topic: What to post about (e.g., "share a tip about cold outreach",
            "comment on AI in sales", "share a success story").
        tone: Post tone: "professional", "casual", "thought-leader", "storytelling".
        mode: "autopilot" (publishes immediately) or "copilot" (shows for review).
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
            "  create_post(topic=\"share a tip about cold outreach\")\n"
            "  create_post(topic=\"comment on AI in sales\")\n"
            "  create_post(topic=\"share a lesson learned this week\")"
        )

    account_id = get_account_id()
    if not account_id:
        return "No LinkedIn account connected. Run setup_profile first."

    # ── Generate post content using LLM ──
    profile = await run_db(get_setting, "profile", {})
    voice = await run_db(get_setting, "voice_signature", {})

    try:
        from ..ai.llm_router import call_llm

        name = profile.get("name", "")
        title = profile.get("title", "")
        company = profile.get("company", "")
        industry = profile.get("industry", "")

        # Voice characteristics
        voice_style = voice.get("style", "professional")
        voice_tone = voice.get("tone", "")
        voice_patterns = voice.get("patterns", [])
        patterns_str = ", ".join(voice_patterns[:5]) if voice_patterns else ""

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
            return "Failed to generate post content. Try a different topic."

    except Exception as e:
        logger.error("Post generation failed: %s", e)
        return f"Failed to generate post: {e}"

    # ── Copilot mode: show for review ──
    if False:  # copilot mode removed
        # Store the draft for later publishing
        from ..db.queries import save_setting
        await run_db(save_setting, "pending_post", {
            "text": post_text,
            "topic": topic,
            "tone": tone,
        })

        output = [
            "LinkedIn Post Draft:",
            "",
            f'   "{post_text}"',
            f"   ({len(post_text)} chars)",
            "",
            "Publish this post? Reply with:",
            "  'yes' / 'send' — publish now",
            "  'edit: [your text]' — publish custom text instead",
            "  'skip' — discard this draft",
        ]
        return "\n".join(output)

    # ── Autopilot mode: publish immediately ──
    try:
        client = get_linkedin_client()
        result = await client.create_post(account_id, post_text)
        await client.close()

        if result.get("success"):
            post_id = result.get("post_id", "")
            await run_db(log_action, "post_created", details={
                "topic": topic,
                "tone": tone,
                "chars": len(post_text),
                "post_id": post_id,
            })
            # Save for inbound comment monitoring
            if post_id:
                try:
                    await run_db(save_published_post, post_id=post_id, text=post_text[:500], topic=topic)
                except Exception as e:
                    logger.debug("Failed to save published post for monitoring: %s", e)
            return (
                f"LinkedIn post published!\n\n"
                f'   "{post_text[:200]}{"..." if len(post_text) > 200 else ""}"\n'
                f"   ({len(post_text)} chars)\n\n"
                "Tip: Posts get the most engagement in the first 2 hours. "
                "Reply to comments quickly to boost reach."
            )
        else:
            error = result.get("error", "Unknown error")
            return f"Post publish failed: {error}\n\nDraft saved — try again later."
    except UnipileError as e:
        return f"Post publish failed: {e}"
    except Exception as e:
        logger.error("Post publish failed: %s", e)
        return f"Post publish failed: {e}"
