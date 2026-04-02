"""Voice signature analyzer — the #1 killer feature.

Analyzes the user's LinkedIn profile and posts to generate a voice signature
(tone, vocabulary, patterns) and expertise map. This is what makes every
outreach message sound like the user, not a bot.

From customer discovery: 7 of 12 interested users had their strongest
positive reaction to voice matching.
"""

from __future__ import annotations

import logging
from typing import Any

from .json_repair import parse_json
from .llm import LLMClient
from .prompt_loader import get_prompt_temperature, has_prompt, render_prompt

logger = logging.getLogger(__name__)

# ──────────────────────────────────────────────
# Voice Analysis Prompt
# ──────────────────────────────────────────────

VOICE_ANALYSIS_SYSTEM = """You are an expert communication analyst specializing in LinkedIn professional communication styles. You analyze how people write and communicate to create a "voice signature" that can be used to generate messages that sound authentically like them.

You are precise, analytical, and output structured JSON only."""

VOICE_ANALYSIS_PROMPT = """Analyze this LinkedIn profile and their recent posts to create a detailed voice signature and expertise map.

## PROFILE DATA
Name: {name}
Headline: {headline}
Title: {title} at {company}
Location: {location}
Industry: {industry}
Summary: {summary}

## EXPERIENCE
{experience}

## SKILLS
{skills}

## RECENT POSTS ({post_count} posts)
{posts}

---

## TASK
Create two things:

### 1. VOICE SIGNATURE
Analyze their writing style from posts, headline, and summary. If they have no posts, infer from their headline, summary, and professional context.

Extract:
- **tone**: One-line description (e.g., "Direct, technical, slightly informal")
- **sentence_length**: Their typical pattern (e.g., "Short (avg 8 words)" or "Medium, uses compound sentences")
- **signature_pattern**: How they typically open and close communications (e.g., "Opens with first name, closes with question")
- **vocabulary_preferences**: Words/phrases they gravitate toward
- **no_go**: Things they would NEVER write (e.g., "Won't use emojis, won't say 'synergy'")
- **formality_level**: 1-10 scale (1=very casual, 10=very formal)
- **communication_style**: Specific recommendations for matching their voice

### 2. EXPERTISE MAP
From their profile, experience, and posts:
- **core**: Their primary expertise areas (comma-separated)
- **credible_topics**: Topics they can credibly discuss in outreach
- **off_limits**: Topics outside their domain they should NOT comment on
- **industry_context**: Brief description of their industry positioning

## RESPONSE FORMAT
Return ONLY valid JSON (no markdown, no explanation):
{{
    "voice": {{
        "tone": "...",
        "sentence_length": "...",
        "signature_pattern": "...",
        "vocabulary_preferences": ["...", "..."],
        "no_go": "...",
        "formality_level": 7,
        "communication_style": ["...", "..."]
    }},
    "expertise": {{
        "core": "...",
        "credible_topics": "...",
        "off_limits": "...",
        "industry_context": "..."
    }}
}}"""


def _format_experience(experience: list[dict]) -> str:
    if not experience:
        return "No experience data available"
    lines = []
    for exp in experience:
        title = exp.get("title", "Unknown")
        company = exp.get("company", "Unknown")
        desc = exp.get("description", "")
        line = f"- {title} at {company}"
        if desc:
            line += f": {desc[:200]}"
        lines.append(line)
    return "\n".join(lines)


def _format_posts(posts: list[dict]) -> str:
    if not posts:
        return "No recent posts available — infer voice from profile data."
    lines = []
    for i, post in enumerate(posts, 1):
        text = post.get("text", "").strip()
        if text:
            lines.append(f"Post {i}:\n{text[:500]}\n")
    return "\n".join(lines) if lines else "No posts with text content found."


async def analyze_voice(profile: dict[str, Any]) -> dict[str, Any]:
    """Analyze a LinkedIn profile and return voice signature + expertise map.

    Args:
        profile: Dict from linkedin.profile.fetch_own_profile()

    Returns:
        Dict with 'voice' and 'expertise' keys containing the analysis.
    """
    # Route through backend if in backend mode and no local LLM key
    from ..config import has_local_llm_key, is_backend_mode
    if is_backend_mode() and not has_local_llm_key():
        from ..linkedin import get_linkedin_client
        client = get_linkedin_client()
        try:
            return await client.analyze_voice(profile, profile.get("posts", []))
        finally:
            await client.close()

    # Build template variables
    tpl_vars = {
        "name": profile.get("name", "Unknown"),
        "headline": profile.get("headline", ""),
        "title": profile.get("title", ""),
        "company": profile.get("company", ""),
        "location": profile.get("location", ""),
        "industry": profile.get("industry", ""),
        "summary": profile.get("summary", ""),
        "experience": _format_experience(profile.get("experience", [])),
        "skills": ", ".join(profile.get("skills", [])[:15]),
        "post_count": str(len(profile.get("posts", []))),
        "posts": _format_posts(profile.get("posts", [])),
    }

    # v63 path: use JSON prompt template
    if has_prompt("voice_analysis"):
        logger.debug("Using v63 voice_analysis prompt")
        prompt = render_prompt("voice_analysis", tpl_vars)
        temperature = get_prompt_temperature("voice_analysis")
    else:
        # Legacy fallback
        logger.debug("Using legacy voice_analysis prompt")
        prompt = VOICE_ANALYSIS_PROMPT.format(**tpl_vars)
        temperature = 0.5

    client = LLMClient()
    raw = await client.generate(prompt, system=VOICE_ANALYSIS_SYSTEM, temperature=temperature)

    # Parse JSON from response with 2-tier repair
    default_result = {
        "voice": {
            "tone": "Could not analyze — check your LLM API key",
            "sentence_length": "Unknown",
            "signature_pattern": "Unknown",
            "vocabulary_preferences": [],
            "no_go": "Unknown",
            "formality_level": 5,
            "communication_style": [],
        },
        "expertise": {
            "core": profile.get("headline", ""),
            "credible_topics": "",
            "off_limits": "",
            "industry_context": profile.get("industry", ""),
        },
    }

    return parse_json(raw, fallback=default_result)
