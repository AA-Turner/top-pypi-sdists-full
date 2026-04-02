"""Prompt loader — loads v63 production prompts from JSON files.

Provides a simple interface for loading prompt templates and rendering them
with HeyLead data structures mapped to v63 variable names.

Usage:
    from .prompt_loader import render_prompt, build_context_block, get_prompt_temperature

    ctx = build_context_block(sender, prospect, campaign, voice, ...)
    prompt = render_prompt("outreach_invitation", ctx)
    temp = get_prompt_temperature("outreach_invitation")
"""

from __future__ import annotations

import json
import logging
import time
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

# Prompt files directory (sibling to ai/)
_PROMPTS_DIR = Path(__file__).parent.parent / "prompts"

# Cache loaded prompts in memory
_prompt_cache: dict[str, dict] = {}


class SafeDict(dict):
    """Dict subclass that returns '{key}' for missing keys in str.format_map().

    This prevents KeyError when a prompt template has variables that aren't
    provided — they're left as-is in the output.
    """

    def __missing__(self, key: str) -> str:
        return "{" + key + "}"


def load_prompt(name: str) -> dict:
    """Load a prompt template from JSON file.

    Args:
        name: Prompt name (e.g., "outreach_invitation", "followup_reasoning")

    Returns:
        Dict with keys: name, description, version, content, variables,
        temperature, response_limit

    Raises:
        FileNotFoundError: If prompt file doesn't exist
    """
    if name in _prompt_cache:
        return _prompt_cache[name]

    path = _PROMPTS_DIR / f"{name}.json"
    if not path.exists():
        raise FileNotFoundError(f"Prompt file not found: {path}")

    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    _prompt_cache[name] = data
    return data


def render_prompt(name: str, variables: dict[str, Any]) -> str:
    """Load a prompt and render it with variables.

    Uses SafeDict so missing variables are left as '{var}' placeholders
    rather than raising KeyError.

    Args:
        name: Prompt name (e.g., "outreach_invitation")
        variables: Dict of variable values to substitute

    Returns:
        Rendered prompt string

    Raises:
        FileNotFoundError: If prompt file doesn't exist
    """
    prompt_data = load_prompt(name)
    content = prompt_data["content"]

    # Use SafeDict for graceful handling of missing variables
    safe_vars = SafeDict(variables)
    rendered = content.format_map(safe_vars)

    return rendered


def get_prompt_temperature(name: str) -> float:
    """Get the recommended temperature for a prompt.

    Args:
        name: Prompt name

    Returns:
        Temperature float (e.g., 0.7, 0.95)
    """
    try:
        data = load_prompt(name)
        return float(data.get("temperature", 0.7))
    except FileNotFoundError:
        return 0.7


def get_prompt_response_limit(name: str) -> int:
    """Get the response symbol limit for a prompt.

    Args:
        name: Prompt name

    Returns:
        Response limit in characters
    """
    try:
        data = load_prompt(name)
        return int(data.get("response_limit", 200))
    except FileNotFoundError:
        return 200


def has_prompt(name: str) -> bool:
    """Check if a prompt file exists.

    Args:
        name: Prompt name

    Returns:
        True if the prompt JSON file exists
    """
    path = _PROMPTS_DIR / f"{name}.json"
    return path.exists()


# ──────────────────────────────────────────────
# Context Builder — maps HeyLead data → v63 variables
# ──────────────────────────────────────────────


def _format_contact_info(prospect: dict[str, Any]) -> str:
    """Format prospect data into v63 {{contact_info}} block."""
    parts = []
    name = prospect.get("name", "")
    if name:
        parts.append(f"Name: {name}")
    title = prospect.get("title", "")
    if title:
        parts.append(f"Title: {title}")
    company = prospect.get("company", "")
    if company:
        parts.append(f"Company: {company}")
    headline = prospect.get("headline", "")
    if headline:
        parts.append(f"Headline: {headline}")
    location = prospect.get("location", "")
    if location:
        parts.append(f"Location: {location}")
    industry = prospect.get("industry", "")
    if industry:
        parts.append(f"Industry: {industry}")
    return "\n".join(parts) if parts else "No contact information available."


def _format_history(messages: list[dict[str, Any]] | None) -> str:
    """Format conversation history for v63 {{history}} variable."""
    if not messages:
        return "No previous messages."
    lines = []
    for msg in messages:
        role = msg.get("role", "unknown")
        text = msg.get("text", "")
        label = "SDR" if role == "sdr" else "PROSPECT"
        lines.append(f"[{label}]: {text}")
    return "\n".join(lines)


def _format_analysis_section(
    analysis: dict[str, Any] | None, section: str
) -> str:
    """Format optional analysis sections for v63 conditional blocks."""
    if not analysis:
        return ""
    data = analysis.get(section, {})
    if not data:
        return ""

    if section == "tone":
        parts = []
        if data.get("recommended_approach"):
            parts.append(f"Recommended approach: {data['recommended_approach']}")
        if data.get("formality_level"):
            parts.append(f"Formality: {data['formality_level']}/10")
        if data.get("industry_jargon"):
            jargon = data["industry_jargon"]
            if isinstance(jargon, list):
                parts.append(f"Jargon: {', '.join(jargon[:5])}")
        return f"Tone Analysis: {'; '.join(parts)}" if parts else ""

    if section == "pain_points":
        if isinstance(data, list):
            return f"Pain Point Analysis: {'; '.join(str(p) for p in data[:3])}"
        return ""

    if section == "signal_context":
        # data is the signal_context dict from contact.analysis_json
        parts = []
        if data.get("signal_type"):
            parts.append(f"Signal: {data['signal_type']}")
        if data.get("signal_angle"):
            parts.append(f"Angle: {data['signal_angle'].replace('_', ' ')}")
        if data.get("engagement_hook"):
            parts.append(f"Hook: {data['engagement_hook']}")
        if data.get("signal_summary"):
            parts.append(f"Context: {data['signal_summary'][:150]}")
        return "; ".join(parts) if parts else ""

    return ""


# ──────────────────────────────────────────────
# Signal Strategy — angle-specific messaging instructions
# ──────────────────────────────────────────────

# Map signal angles → strategy categories
_ANGLE_TO_CATEGORY: dict[str, str] = {
    # Congrats / Milestone
    "congrats_new_company": "congrats",
    "congrats_promotion": "congrats",
    "congrats_funding": "congrats",
    "congrats_acquisition": "congrats",
    "congrats_exec_hire": "congrats",
    "congrats_expansion": "congrats",
    "congrats_product_launch": "congrats",
    "milestone_congrats": "congrats",
    "congrats_reconnect": "congrats",
    # Pain Point / Buying Intent
    "pain_point_alignment": "pain_point",
    "buying_intent_response": "pain_point",
    "solution_alignment": "pain_point",
    # Competitive
    "competitive_displacement": "competitive",
    # Engagement / Shared Context
    "shared_engagement": "engagement",
    "company_page_engagement": "engagement",
    "company_follower_outreach": "engagement",
    "reciprocal_interest": "engagement",
    "icp_profile_viewer": "engagement",
    # Growth / Hiring
    "hiring_partnership": "growth",
    "growth_partnership": "growth",
    "builder_connection": "growth",
    # Empathy / Transition
    "empathy_restructuring": "empathy",
}

_STRATEGY_TEMPLATES: dict[str, str] = {
    "congrats": (
        "SIGNAL STRATEGY — MILESTONE / CONGRATS:\n"
        "This prospect recently hit a milestone (new role, funding, promotion, etc.).\n"
        "Opening: Warm, brief acknowledgment of the change — paraphrase loosely, "
        "never quote their announcement.\n"
        "CTA: Ask how the transition is shaping their day-to-day.\n"
        "Guardrails: Do NOT say 'congrats' or 'congratulations' — it's overused "
        "and sounds templated. Instead, reference the shift naturally "
        '(e.g., "big transitions like that..." or "stepping into something new...").\n'
        "Do NOT mention the company name, job title, or funding amount.\n"
        "Examples:\n"
        '  "Transitions like that tend to surface a lot of things that were on autopilot. '
        'Has the operational side gotten heavier, or were you able to keep it lean?"\n'
        '  "Stepping into something new usually means inheriting a few surprises. '
        'Are you still building the team out, or is the core already in place?"'
    ),
    "pain_point": (
        "SIGNAL STRATEGY — PAIN POINT / BUYING INTENT:\n"
        "This prospect expressed a challenge, asked for recommendations, "
        "or showed buying intent.\n"
        "Opening: Paraphrase their pain loosely as a shared observation — "
        "never quote their words or reference their post directly.\n"
        "CTA: Ask if they've found a way around it, or if it's still taking "
        "up their time.\n"
        "Guardrails: Do NOT pitch a solution. Do NOT mention their post, "
        "comment, or any specific content they shared. Frame it as a common "
        "challenge you've seen, not something you 'noticed' about them.\n"
        "Examples:\n"
        '  "That bottleneck between pipeline and actual conversations seems to '
        'hit every team at some point. Have you found a rhythm that works, '
        'or is it still a time sink?"\n'
        '  "Keeping outreach personal at scale is one of those things that '
        'sounds simple until you try it. Do you still handle that manually, '
        'or did you find a way to automate without losing the human touch?"'
    ),
    "competitive": (
        "SIGNAL STRATEGY — COMPETITIVE DISPLACEMENT:\n"
        "This prospect mentioned frustration with or evaluation of a competitor.\n"
        "Opening: Reference the problem category broadly — never name the "
        "competitor or imply you know they're switching.\n"
        "CTA: Ask what's missing from their current setup.\n"
        "Guardrails: NEVER name the competitor. Do NOT say 'I saw you're "
        "evaluating' or 'looking for alternatives'. Frame it as a general "
        "pattern in their space.\n"
        "Examples:\n"
        '  "Most teams outgrow their first tooling stack once volume picks up. '
        'Is your current setup still keeping pace, or are there gaps showing up?"\n'
        '  "Switching costs keep a lot of teams stuck on tools they\'ve outgrown. '
        'Is that a conversation happening on your end, or is everything still working?"'
    ),
    "engagement": (
        "SIGNAL STRATEGY — SHARED ENGAGEMENT / MUTUAL INTEREST:\n"
        "This prospect engaged with your content, follows your company, "
        "viewed your profile, or appeared in a shared discussion.\n"
        "Opening: Reference the shared space or topic naturally — never "
        'say "I saw you liked our post" or "thanks for following".\n'
        "CTA: Ask about their perspective on the topic.\n"
        "Guardrails: Do NOT reference the specific action (like, follow, "
        "view). Frame it as being in similar circles or working on "
        "similar problems.\n"
        "Examples:\n"
        '  "We seem to be thinking about similar things in this space. '
        'Are you seeing the same shift toward personalization on your end, '
        'or is the focus elsewhere?"\n'
        '  "Looks like we run in similar circles. What\'s taking up most of '
        'your bandwidth right now — is it still the growth side, or has '
        'something else moved up the list?"'
    ),
    "growth": (
        "SIGNAL STRATEGY — GROWTH / HIRING:\n"
        "This prospect is scaling their team, hiring, or building something new.\n"
        "Opening: Reference the growth energy naturally — not the specific "
        "headcount or job posting.\n"
        "CTA: Ask about the scaling challenge — what breaks first when "
        "things speed up.\n"
        "Guardrails: Do NOT reference specific job postings or headcount. "
        'Do NOT say "I see you\'re hiring". Frame it as a growth pattern.\n'
        "Examples:\n"
        '  "Scaling a team fast usually means the process side struggles to '
        'keep up. Has that been smooth so far, or is there a bottleneck '
        'showing up?"\n'
        '  "Building mode is exciting but the operational side tends to lag. '
        'Are you still handling that yourself, or did you bring someone in '
        'for it?"'
    ),
    "empathy": (
        "SIGNAL STRATEGY — EMPATHY / TRANSITION:\n"
        "This prospect's company is going through restructuring or layoffs.\n"
        "Opening: Brief, empathetic acknowledgment — no pity, no "
        "opportunism. Keep it human.\n"
        "CTA: Ask what they're focused on now.\n"
        "Guardrails: Do NOT mention layoffs, restructuring, or any negative "
        "event directly. Do NOT try to sell during a difficult time. "
        "Keep it genuinely human — this is about building a relationship, "
        "not capitalizing on hardship.\n"
        "Examples:\n"
        '  "Periods of change tend to reset a lot of priorities. What\'s '
        'taking up most of your focus right now?"\n'
        '  "Transitions bring a lot of noise, but they also clear space for '
        'what matters. Are you heads-down on something specific, or still '
        'figuring out the next move?"'
    ),
}


def _build_signal_strategy(analysis: dict[str, Any] | None) -> str:
    """Build signal-specific messaging strategy from prospect analysis.

    Extracts signal_context from analysis, maps the signal_angle to a
    strategy category, and returns angle-specific instructions for the LLM.

    Returns empty string if no signal context is present.
    """
    if not analysis:
        return ""
    signal_ctx = analysis.get("signal_context")
    if not signal_ctx or not isinstance(signal_ctx, dict):
        return ""

    angle = signal_ctx.get("signal_angle", "")
    if not angle:
        return ""

    category = _ANGLE_TO_CATEGORY.get(angle, "")
    if not category:
        return ""

    strategy = _STRATEGY_TEMPLATES.get(category, "")
    if not strategy:
        return ""

    # Append signal-specific context for the LLM
    parts = [strategy]
    hook = signal_ctx.get("engagement_hook", "")
    if hook:
        parts.append(f"\nSuggested angle (adapt to your voice, don't copy verbatim): {hook}")
    summary = signal_ctx.get("signal_summary", "")
    if summary:
        parts.append(f"Background context: {summary[:150]}")
    do_not = signal_ctx.get("DO_NOT", "")
    if do_not:
        parts.append(f"IMPORTANT: {do_not}")

    return "\n".join(parts)


def _enrich_trigger_info(
    base_trigger: str,
    analysis: dict[str, Any] | None,
) -> str:
    """Prepend per-prospect signal hook to campaign-level trigger info."""
    if not analysis:
        return base_trigger
    signal_ctx = analysis.get("signal_context")
    if not signal_ctx or not isinstance(signal_ctx, dict):
        return base_trigger
    hook = signal_ctx.get("engagement_hook", "")
    if not hook:
        return base_trigger
    # Combine: signal hook first, then campaign context
    if base_trigger:
        return f"{hook}\n\nCampaign context: {base_trigger}"
    return hook


def _detect_conversation_language(history: list[dict[str, Any]] | None) -> str:
    """Detect language from recent prospect messages and return a language instruction.

    Checks the last 3 prospect messages for non-ASCII characters indicating
    non-English language. Returns an explicit instruction to reply in that language.
    """
    if not history:
        return ""

    # Get last 3 prospect messages (most recent first)
    prospect_msgs = [m.get("text", "") for m in reversed(history) if m.get("role") == "prospect"][:3]
    if not prospect_msgs:
        return ""

    # Check the most recent prospect message for non-Latin characters
    last_msg = prospect_msgs[0]
    if not last_msg:
        return ""

    # Count non-ASCII alphabetic characters (Cyrillic, CJK, Arabic, etc.)
    non_latin = sum(1 for c in last_msg if ord(c) > 127 and c.isalpha())
    total_alpha = sum(1 for c in last_msg if c.isalpha())

    if total_alpha == 0:
        return ""

    # If >30% non-Latin characters, the message is likely in another language
    if non_latin / total_alpha > 0.3:
        return (
            f"CRITICAL LANGUAGE RULE: The prospect's last message is NOT in English. "
            f"You MUST reply in the SAME language the prospect used. "
            f"Match their language exactly. Do NOT switch to English."
        )

    return ""


def _compute_conversation_stage(
    history: list[dict[str, Any]] | None,
    campaign_context: dict[str, Any],
) -> str:
    """Determine conversation stage based on prospect reply count.

    Returns stage-specific instructions for the prompt:
    - early (0-2 prospect replies): keep discovering
    - bridge_ready (3+ replies AND offerings available): time to bridge to product
    """
    if not history:
        return ""
    prospect_replies = sum(1 for m in history if m.get("role") == "prospect")
    has_offerings = (
        campaign_context.get("offerings", "Not specified") != "Not specified"
        and campaign_context.get("offerings", "").strip()
    )

    if prospect_replies >= 3 and has_offerings:
        return (
            "CONVERSATION STAGE: BRIDGE READY\n"
            "The prospect has given 3+ engaged replies. You have enough rapport.\n"
            "It's time to naturally bridge to our value prop.\n"
            "• Use what they shared to connect their situation to our offering.\n"
            "• Pattern: reference what they said → briefly relate it to what we do → "
            "ask if that's relevant for them.\n"
            "• Do NOT keep asking more discovery questions — you have enough context.\n"
            "• The bridge should feel natural, not forced — connect THEIR words to YOUR product.\n"
            "• Keep it to 2-3 sentences. One question max."
        )
    return ""


def build_context_block(
    sender: dict[str, Any],
    prospect: dict[str, Any],
    campaign_config: dict[str, Any],
    voice: dict[str, Any],
    campaign_context: dict[str, Any] | None = None,
    history: list[dict[str, Any]] | None = None,
    analysis: dict[str, Any] | None = None,
    max_chars: int = 200,
    news_context: str | None = None,
    previously_used: str | None = None,
) -> dict[str, str]:
    """Build the complete variable dict mapping HeyLead data → v63 variable names.

    Args:
        sender: User's profile data (name, title, company)
        prospect: Prospect profile data
        campaign_config: Campaign config_json (parsed)
        voice: Voice signature dict
        campaign_context: Optional campaign context_json (offerings, case_studies, etc.)
        history: Optional conversation history (list of {role, text})
        analysis: Optional prospect analysis (from prospect_analyzer)
        max_chars: Character limit for the message
        news_context: Optional formatted news text from SERPER API
        previously_used: Optional formatted memory block for anti-repetition

    Returns:
        Dict ready to pass to render_prompt()
    """
    ctx = campaign_context or {}

    # Core v63 variables
    variables: dict[str, str] = {
        # Prospect info
        "contact_info": _format_contact_info(prospect),
        # Trigger / relevance — enriched with signal hook when available
        "trigger_info": _enrich_trigger_info(
            campaign_config.get("relevance_hook", "")
            or campaign_config.get("target_description", ""),
            analysis,
        ),
        # Campaign context (new fields from context_json)
        "offerings": ctx.get("offerings", "Not specified"),
        "case_studies": ctx.get("case_studies", "Not specified"),
        "social_proofs": ctx.get("social_proofs", "Not specified"),
        "campaign_preferences": ctx.get("campaign_preferences", ""),
        "custom_params": ctx.get("custom_params", ""),
        # Calendar / booking
        "calendar_link": campaign_config.get("booking_link", "Not configured"),
        # Sender
        "company": sender.get("company", "Our company"),
        # Conversation
        "history": _format_history(history),
        # Timestamp
        "current_date_time": time.strftime("%Y-%m-%d %H:%M %Z"),
        # Limits
        "symbols_limit": f"Response symbols limit: {max_chars} characters maximum.",
        # Analysis sections (v63 uses conditional blocks)
        "tone_analysis_section": _format_analysis_section(analysis, "tone")
            if analysis else "",
        "pain_point_section": _format_analysis_section(analysis, "pain_points")
            if analysis else "",
        # Signal-specific messaging strategy
        "signal_strategy": _build_signal_strategy(analysis),
        # News context (from SERPER API, Sprint 15)
        "news_context": news_context or "",
        # Conversation memory (from memory_json, Sprint 16)
        "previously_used": previously_used or "",
        # Language detection — reply in the same language the prospect uses
        "language_rule": _detect_conversation_language(history),
        # Conversation stage — how many prospect replies we've received
        "conversation_stage": _compute_conversation_stage(history, ctx),
    }

    # Voice-related variables (used by HeyLead prompts, not v63 — but included for compatibility)
    voice_vocab = voice.get("vocabulary_preferences", [])
    if isinstance(voice_vocab, list):
        voice_vocab = ", ".join(voice_vocab)

    variables.update({
        "voice_tone": voice.get("tone", "Professional, direct"),
        "voice_sentence": voice.get("sentence_length", "Medium"),
        "voice_vocab": voice_vocab or "None specified",
        "voice_nogo": voice.get("no_go", "Generic sales phrases"),
        # Prospect shorthand
        "prospect_name": prospect.get("name", "").split()[0] if prospect.get("name") else "there",
        "prospect_title": prospect.get("title", ""),
        "prospect_company": prospect.get("company", ""),
        "prospect_headline": prospect.get("headline", ""),
        "prospect_location": prospect.get("location", ""),
        # Sender shorthand
        "sender_name": sender.get("name", ""),
        "sender_title": sender.get("title", ""),
        "sender_company": sender.get("company", ""),
    })

    return variables


def clear_cache() -> None:
    """Clear the prompt cache (useful for testing or hot-reloading)."""
    _prompt_cache.clear()
