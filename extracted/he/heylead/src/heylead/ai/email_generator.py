"""Email message generation — subject lines + body for cold email outreach.

Uses the same voice signature and prospect analysis as LinkedIn messages,
but adapts format for email: subject line, HTML body, clear CTA.
"""

from __future__ import annotations

import logging
from typing import Any

from .llm_router import call_llm

logger = logging.getLogger(__name__)

# Email constraints
SUBJECT_MAX_CHARS = 60
BODY_MAX_CHARS = 800


async def generate_email(
    prospect: dict[str, Any],
    sender_profile: dict[str, Any],
    voice_signature: dict[str, Any],
    campaign_context: dict[str, Any] | None = None,
    prospect_analysis: dict[str, Any] | None = None,
    intelligence_text: str = "",
    max_body_chars: int = BODY_MAX_CHARS,
) -> dict[str, Any]:
    """Generate a personalized cold email with subject line and body.

    Returns:
        {"subject": str, "body": str, "reasoning": dict}
    """
    prospect_name = prospect.get("name", "there")
    prospect_first = prospect_name.split()[0] if prospect_name else "there"
    prospect_title = prospect.get("title") or prospect.get("headline") or ""
    prospect_company = prospect.get("company") or ""

    sender_name = sender_profile.get("name") or sender_profile.get("full_name") or ""
    sender_title = sender_profile.get("headline") or sender_profile.get("title") or ""

    # Voice constraints
    style = voice_signature.get("style", "professional")
    tone = voice_signature.get("tone", "conversational")
    vocab_avoid = voice_signature.get("vocabulary", {}).get("avoid", [])

    # Campaign context
    target_desc = ""
    offerings = ""
    relevance_hook = ""
    if campaign_context:
        target_desc = campaign_context.get("target_description", "")
        offerings = campaign_context.get("offerings", "")
        relevance_hook = campaign_context.get("relevance_hook", "")

    # Prospect intelligence
    fit_reason = ""
    pain_points = ""
    if prospect_analysis:
        fit_reason = prospect_analysis.get("fit_reason", "")
        pain_points = ", ".join(prospect_analysis.get("pain_points", [])[:3])

    prompt = f"""Generate a personalized cold email for B2B outreach.

SENDER: {sender_name} — {sender_title}
PROSPECT: {prospect_first} ({prospect_title} at {prospect_company})

VOICE SIGNATURE:
- Style: {style}
- Tone: {tone}
- Words to AVOID: {', '.join(vocab_avoid[:10]) if vocab_avoid else 'none'}

CAMPAIGN CONTEXT:
- Target audience: {target_desc}
- Offerings: {offerings}
- Relevance hook: {relevance_hook}

PROSPECT INTELLIGENCE:
- Fit reason: {fit_reason}
- Pain points: {pain_points}
- Extra context: {intelligence_text[:300] if intelligence_text else 'none'}

RULES:
1. Subject line: {SUBJECT_MAX_CHARS} chars max. No clickbait. Personalized.
2. Body: {max_body_chars} chars max. Plain text (no HTML tags).
3. First line: personal hook referencing something specific about them
4. Middle: 1-2 sentences connecting their situation to what you offer
5. End: soft CTA (question, not demand). No "book a call" — ask if it resonates.
6. NO generic opener like "I hope this email finds you well"
7. NO "I noticed you" or "I came across your profile" — too salesy
8. Sound like {sender_name}, not a sales bot
9. Keep it under 5 sentences total
10. Use their first name only

Return JSON:
{{"subject": "...", "body": "...", "reasoning": {{"hook": "...", "angle": "..."}}}}"""

    try:
        raw = await call_llm(prompt, max_tokens=600, json_mode=True)
        import json
        result = json.loads(raw)
        # Enforce limits
        subject = (result.get("subject") or "")[:SUBJECT_MAX_CHARS]
        body = (result.get("body") or "")[:max_body_chars]
        return {
            "subject": subject,
            "body": body,
            "reasoning": result.get("reasoning", {}),
        }
    except Exception as e:
        logger.error(f"Email generation failed: {e}")
        raise


async def generate_email_followup(
    prospect: dict[str, Any],
    sender_profile: dict[str, Any],
    voice_signature: dict[str, Any],
    previous_subject: str = "",
    previous_body: str = "",
    followup_count: int = 1,
) -> dict[str, Any]:
    """Generate a follow-up email (reply to previous thread).

    Returns:
        {"subject": str, "body": str}
    """
    prospect_first = (prospect.get("name") or "there").split()[0]
    sender_name = sender_profile.get("name") or ""
    style = voice_signature.get("style", "professional")
    tone = voice_signature.get("tone", "conversational")

    prompt = f"""Generate a follow-up email for B2B outreach.

This is follow-up #{followup_count} to a cold email that got no reply.

SENDER: {sender_name}
PROSPECT: {prospect_first}
PREVIOUS SUBJECT: {previous_subject}
PREVIOUS EMAIL: {previous_body[:300]}

VOICE: {style}, {tone}

RULES:
1. Subject: "Re: {previous_subject}" (keep the thread)
2. Body: 2-3 sentences max
3. Don't repeat the original pitch
4. Add new value (insight, stat, case study reference)
5. Lighter CTA than before
6. Follow-up #{followup_count}: {'gentle bump' if followup_count == 1 else 'final reach-out with graceful close' if followup_count >= 3 else 'add new angle'}

Return JSON: {{"subject": "...", "body": "..."}}"""

    try:
        raw = await call_llm(prompt, max_tokens=300, json_mode=True)
        import json
        result = json.loads(raw)
        return {
            "subject": result.get("subject", f"Re: {previous_subject}"),
            "body": (result.get("body") or "")[:BODY_MAX_CHARS],
        }
    except Exception as e:
        logger.error(f"Email follow-up generation failed: {e}")
        raise
