"""Inbound lead qualification engine.

Qualifies inbound LinkedIn signals (connection requests, unsolicited DMs,
post comments) against the user's active ICPs to determine lead potential.
"""

from __future__ import annotations

import json
import logging
import re
from dataclasses import asdict, dataclass
from typing import Any

from .llm import LLMClient

logger = logging.getLogger(__name__)


@dataclass
class InboundQualification:
    """Result of qualifying an inbound signal."""

    intent: str  # 'buying_signal', 'networking', 'job_seeking', 'spam', 'vendor_pitch', 'partnership', 'unknown'
    matched_icp_id: str | None
    confidence: float  # 0.0-1.0
    recommended_action: str  # 'engage_immediately', 'ask_purpose', 'accept_and_monitor', 'ignore'
    reasoning: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


# ──────────────────────────────────────────────
# Fast path: rule-based spam/recruiter detection
# ──────────────────────────────────────────────

_SPAM_HEADLINE_KEYWORDS = [
    "recruiter", "talent acquisition", "staffing", "headhunter",
    "recruiting", "hiring manager",
]

_JOB_SEEKING_KEYWORDS = [
    "looking for opportunities", "open to work", "seeking new role",
    "job seeker", "actively looking", "#opentowork",
]

_SPAM_MESSAGE_PATTERNS = [
    r"we have.*?opportunity",
    r"perfect candidate",
    r"immediate opening",
    r"your resume",
    r"job (opening|position|vacancy)",
    r"apply now",
    r"we are hiring",
]

_VENDOR_HEADLINE_KEYWORDS = [
    "account executive", "business development representative",
    "sales representative", "sales manager", "sales director",
    "sales executive", "partnership manager", "channel partner",
    "growth consultant", "growth advisor",
    "lead generation", "demand generation",
    "talent operations", "outsourcing", "managed services",
]

_VENDOR_MESSAGE_PATTERNS = [
    r"(?:our|the)\s+(?:platform|solution|tool|product|service|marketplace|candidates)",
    r"(?:browse|check out|explore)\s+(?:our|the)\s+\w+",
    r"(?:book|schedule)\s+(?:a\s+)?(?:call|demo|meeting|time|chat)",
    r"meetings\.hubspot\.com",
    r"calendly\.com/",
    r"cal\.com/",
    r"(?:get|schedule)\s+(?:interviews|demos?)\s+on\s+your\s+calendar",
    r"hire\s+(?:fast|faster|quickly|remote)",
    r"skip\s+(?:filtering|screening|sourcing)",
    r"if\s+(?:this|now)\s+is\s+not\s+the\s+right\s+time",
    r"know\s+(?:someone|anyone)\s+who",
    r"this\s+might\s+be\s+useful",
    r"(?:our|we)\s+(?:can|could)\s+(?:help|get|save|reduce|increase)",
    r"(?:save|reduce)\s+(?:you|your\s+team)\s+(?:time|hours|money)",
    r"we\s+(?:help|work\s+with|specialize)",
    r"interested\s+in\s+(?:a\s+)?(?:demo|trial|pilot|free)",
]


def _classify_fast(
    headline: str,
    content: str,
) -> InboundQualification | None:
    """Rule-based fast classification for obvious cases."""
    headline_lower = (headline or "").lower()
    content_lower = (content or "").lower()

    # Check recruiter/staffing headline
    for kw in _SPAM_HEADLINE_KEYWORDS:
        if kw in headline_lower:
            logger.info(
                "Fast classify: recruiter headline match — keyword='%s' headline='%s'",
                kw, headline[:80],
            )
            return InboundQualification(
                intent="job_seeking",
                matched_icp_id=None,
                confidence=0.85,
                recommended_action="ignore",
                reasoning=f"Headline contains recruiter keyword: '{kw}'",
            )

    # Check job-seeking signals
    for kw in _JOB_SEEKING_KEYWORDS:
        if kw in headline_lower or kw in content_lower:
            logger.info(
                "Fast classify: job-seeking match — keyword='%s' in=%s",
                kw, "headline" if kw in headline_lower else "content",
            )
            return InboundQualification(
                intent="job_seeking",
                matched_icp_id=None,
                confidence=0.8,
                recommended_action="ignore",
                reasoning=f"Job-seeking signal detected: '{kw}'",
            )

    # Check spam message patterns
    for pattern in _SPAM_MESSAGE_PATTERNS:
        if content_lower and re.search(pattern, content_lower):
            logger.info(
                "Fast classify: spam pattern match — pattern='%s' content='%s'",
                pattern, content[:80],
            )
            return InboundQualification(
                intent="spam",
                matched_icp_id=None,
                confidence=0.8,
                recommended_action="ignore",
                reasoning=f"Spam pattern detected in message",
            )

    # Check vendor/sales pitch headline keywords
    for kw in _VENDOR_HEADLINE_KEYWORDS:
        if kw in headline_lower:
            logger.info(
                "Fast classify: vendor headline match — keyword='%s' headline='%s'",
                kw, headline[:80],
            )
            return InboundQualification(
                intent="vendor_pitch",
                matched_icp_id=None,
                confidence=0.85,
                recommended_action="ignore",
                reasoning=f"Vendor/sales headline keyword: '{kw}'",
            )

    # Check vendor pitch message patterns (require 2+ matches to avoid false positives)
    if content_lower:
        matched_patterns = [p for p in _VENDOR_MESSAGE_PATTERNS if re.search(p, content_lower)]
        vendor_match_count = len(matched_patterns)
        if vendor_match_count >= 2:
            logger.info(
                "Fast classify: vendor message patterns — %d matches: %s content='%s'",
                vendor_match_count, matched_patterns[:4], content[:80],
            )
            return InboundQualification(
                intent="vendor_pitch",
                matched_icp_id=None,
                confidence=0.80,
                recommended_action="ignore",
                reasoning=f"Vendor pitch: {vendor_match_count} sales patterns detected in message",
            )
        elif vendor_match_count == 1:
            logger.debug(
                "Fast classify: vendor message — only 1 pattern match (%s), below threshold",
                matched_patterns[0],
            )

    logger.debug("Fast classify: no match — headline='%s' content='%s'", headline[:60], content[:60])
    return None


# ──────────────────────────────────────────────
# Structured ICP keyword matching
# ──────────────────────────────────────────────

def _compute_keyword_overlap(
    profile: dict[str, Any],
    icp: dict[str, Any],
) -> float:
    """Compute weighted keyword overlap between a profile and an ICP.

    Returns 0.0-1.0 score with weighted matching:
    - Title matches weighted 3x (strongest buying signal)
    - Industry matches weighted 2x
    - Seniority matches weighted 1.5x
    - Generic keywords weighted 1x
    - Exclude-list matches penalize -0.3 each
    """
    # Build the profile text to search
    profile_text = " ".join([
        (profile.get("headline") or ""),
        (profile.get("title") or ""),
        (profile.get("company") or ""),
        (profile.get("name") or ""),
    ]).lower()

    if not profile_text.strip():
        return 0.0

    # Collect weighted match terms: (term, weight)
    weighted_terms: list[tuple[str, float]] = []

    # Keywords from ICP (weight: 1.0)
    keywords = icp.get("keywords") or []
    for kw in keywords:
        if kw:
            weighted_terms.append((str(kw).lower(), 1.0))

    # Job titles (weight: 3.0 — strongest buying signal)
    job_titles = icp.get("job_titles") or {}
    for title in (job_titles.get("include") or []):
        term = title.get("name", "") if isinstance(title, dict) else str(title)
        if term:
            weighted_terms.append((term.lower(), 3.0))

    # Industries (weight: 2.0)
    industries = icp.get("industries") or {}
    for ind in (industries.get("include") or []):
        term = ind.get("name", "") if isinstance(ind, dict) else str(ind)
        if term:
            weighted_terms.append((term.lower(), 2.0))

    # Seniority (weight: 1.5)
    seniority = icp.get("seniority") or {}
    for sen in (seniority.get("include") or []):
        term = sen.get("name", "") if isinstance(sen, dict) else str(sen)
        if term:
            weighted_terms.append((term.lower(), 1.5))

    if not weighted_terms:
        return 0.0

    # Compute weighted score
    total_weight = sum(w for _, w in weighted_terms)
    matched_weight = sum(w for term, w in weighted_terms if term in profile_text)

    # Check exclude lists — penalize matches
    penalty = 0.0
    for field_name in ("job_titles", "industries", "seniority"):
        field_data = icp.get(field_name) or {}
        for exc in (field_data.get("exclude") or []):
            term = exc.get("name", "") if isinstance(exc, dict) else str(exc)
            if term and term.lower() in profile_text:
                penalty += 0.3

    raw_score = matched_weight / max(total_weight, 1)
    return max(0.0, min(1.0, raw_score - penalty))


# ──────────────────────────────────────────────
# LLM qualification
# ──────────────────────────────────────────────

_QUALIFY_SYSTEM = """You are an expert B2B sales analyst. Given an inbound LinkedIn signal (connection request, DM, or post comment), determine if the sender could be a potential customer/lead.

You must output a valid JSON object with these exact fields:
- "intent": one of "buying_signal", "networking", "job_seeking", "spam", "vendor_pitch", "partnership", "unknown"
- "matched_icp_id": the ID of the best-matching ICP, or null if no match
- "confidence": float between 0.0 and 1.0
- "recommended_action": one of "engage_immediately", "ask_purpose", "accept_and_monitor", "ignore"
- "reasoning": brief explanation (1-2 sentences)

Intent definitions:
- buying_signal: Shows signs of being a potential buyer (title matches ICP, mentions pain points, asks about product/service)
- networking: General professional networking (industry peer, mutual connections, no buying intent)
- job_seeking: Looking for a job or is a recruiter
- spam: Irrelevant, mass messaging, or promotional
- vendor_pitch: Sender is selling a product or service (mentions their platform/tool/solution, includes booking links, pitches demos, or offers their services)
- partnership: Interested in collaboration, not buying
- unknown: Can't determine intent from available info

Recommended action logic:
- engage_immediately: High-confidence buying signal (confidence >= 0.7)
- ask_purpose: Looks promising but unclear intent (confidence 0.4-0.7)
- accept_and_monitor: Low confidence match, worth keeping in network
- ignore: Spam, recruiters, vendor pitches, or clearly irrelevant

No markdown. No code fences. Output ONLY the JSON object."""

_QUALIFY_PROMPT = """Qualify this inbound LinkedIn signal:

Signal type: {signal_type}

Sender profile:
- Name: {name}
- Headline: {headline}
- Company: {company}

{content_section}

Active ICPs (Ideal Customer Profiles) to match against:
{icp_section}

Classify intent, match to an ICP if relevant, and recommend an action."""


def _build_icp_section(icps: list[dict[str, Any]]) -> str:
    """Build a concise ICP summary for the LLM prompt."""
    if not icps:
        return "No active ICPs defined. Qualify based on general B2B sales signals."

    sections = []
    for icp_data in icps:
        icp_json_str = icp_data.get("icp_json", "{}")
        try:
            parsed = json.loads(icp_json_str) if isinstance(icp_json_str, str) else icp_json_str
        except (json.JSONDecodeError, TypeError):
            parsed = {}

        # Extract individual ICPs from the result
        icps_list = parsed.get("icps", [parsed]) if parsed else [{}]
        for single_icp in icps_list[:2]:  # Max 2 per result to keep prompt short
            icp_id = icp_data.get("id", "")
            name = single_icp.get("name", icp_data.get("name", "Unknown"))
            desc = single_icp.get("description", "")[:150]
            pain_points = ", ".join((single_icp.get("pain_points") or [])[:3])
            keywords = ", ".join((single_icp.get("keywords") or [])[:5])

            section = f"  ICP '{name}' (id={icp_id}):"
            if desc:
                section += f"\n    Description: {desc}"
            if pain_points:
                section += f"\n    Pain points: {pain_points}"
            if keywords:
                section += f"\n    Keywords: {keywords}"
            sections.append(section)

    return "\n".join(sections) if sections else "No ICP details available."


def _parse_qualification_response(raw: str, icps: list[dict]) -> InboundQualification:
    """Parse the LLM JSON response into an InboundQualification."""
    # Strip markdown fences if present
    text = raw.strip()
    if text.startswith("```"):
        text = re.sub(r"^```\w*\n?", "", text)
        text = re.sub(r"\n?```$", "", text)

    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        # Try to extract JSON from response
        match = re.search(r'\{[^{}]*"intent"[^{}]*\}', text, re.DOTALL)
        if match:
            try:
                data = json.loads(match.group())
            except json.JSONDecodeError:
                return InboundQualification(
                    intent="unknown",
                    matched_icp_id=None,
                    confidence=0.3,
                    recommended_action="ask_purpose",
                    reasoning="Could not parse qualification response",
                )
        else:
            return InboundQualification(
                intent="unknown",
                matched_icp_id=None,
                confidence=0.3,
                recommended_action="ask_purpose",
                reasoning="Could not parse qualification response",
            )

    valid_intents = {"buying_signal", "networking", "job_seeking", "spam", "vendor_pitch", "partnership", "unknown"}
    valid_actions = {"engage_immediately", "ask_purpose", "accept_and_monitor", "ignore"}

    intent = data.get("intent", "unknown")
    if intent not in valid_intents:
        intent = "unknown"

    action = data.get("recommended_action", "ask_purpose")
    if action not in valid_actions:
        action = "ask_purpose"

    confidence = float(data.get("confidence", 0.3))
    confidence = max(0.0, min(1.0, confidence))

    matched_icp_id = data.get("matched_icp_id")
    # Validate that matched ICP actually exists
    if matched_icp_id:
        icp_ids = {icp.get("id") for icp in icps}
        if matched_icp_id not in icp_ids:
            matched_icp_id = None

    return InboundQualification(
        intent=intent,
        matched_icp_id=matched_icp_id,
        confidence=confidence,
        recommended_action=action,
        reasoning=data.get("reasoning", ""),
    )


async def qualify_inbound(
    profile: dict[str, Any],
    content: str | None,
    signal_type: str,
    active_icps: list[dict[str, Any]],
) -> InboundQualification:
    """Qualify an inbound signal against ICPs.

    Tries fast rule-based classification first, then structured keyword
    matching, and falls back to LLM for ambiguous cases.

    Args:
        profile: Sender info with name, headline, company, title.
        content: Their message, comment text, or invite note (may be empty).
        signal_type: 'invitation', 'message', or 'comment'.
        active_icps: List of ICP dicts from list_icps(status='active').

    Returns:
        InboundQualification with intent, ICP match, confidence, and action.
    """
    headline = profile.get("headline", "") or profile.get("title", "")
    content_str = content or ""

    # 1. Fast path: rule-based spam/recruiter detection
    fast_result = _classify_fast(headline, content_str)
    if fast_result:
        logger.info("Inbound qualified (fast): %s → %s", profile.get("name"), fast_result.intent)
        return fast_result

    # 2. Structured keyword matching (boost for LLM or standalone)
    best_overlap = 0.0
    best_icp_id = None
    for icp in active_icps:
        icp_json_str = icp.get("icp_json", "{}")
        try:
            parsed = json.loads(icp_json_str) if isinstance(icp_json_str, str) else icp_json_str
        except (json.JSONDecodeError, TypeError):
            continue
        for single_icp in (parsed.get("icps", [parsed]) if parsed else []):
            overlap = _compute_keyword_overlap(profile, single_icp)
            if overlap > 0:
                logger.debug(
                    "Keyword overlap: %s vs ICP '%s' = %.2f",
                    profile.get("name"), single_icp.get("name", icp.get("id", "?")), overlap,
                )
            if overlap > best_overlap:
                best_overlap = overlap
                best_icp_id = icp.get("id")

    logger.info(
        "Keyword overlap result: %s — best_score=%.2f best_icp=%s",
        profile.get("name"), best_overlap, best_icp_id or "none",
    )

    # 3. LLM qualification
    # Route through backend if in backend mode
    from ..config import has_local_llm_key, is_backend_mode
    if is_backend_mode() and not has_local_llm_key():
        from ..linkedin import get_linkedin_client
        backend_client = get_linkedin_client()
        try:
            return await backend_client.qualify_inbound(
                profile=profile,
                content=content_str,
                signal_type=signal_type,
                icp_summaries=[
                    {
                        "id": icp.get("id"),
                        "name": icp.get("name"),
                        "icp_json": icp.get("icp_json", "{}"),
                    }
                    for icp in active_icps
                ],
            )
        except Exception as e:
            logger.warning("Backend qualify_inbound failed: %s, using keyword match", e)
            # Fall through to keyword-only result
        finally:
            await backend_client.close()

    # Try local LLM
    try:
        client = LLMClient()
        content_section = f'Message/Comment: "{content_str[:500]}"' if content_str else "No message content (silent connection request)."
        icp_section = _build_icp_section(active_icps)

        prompt = _QUALIFY_PROMPT.format(
            signal_type=signal_type,
            name=profile.get("name", "Unknown"),
            headline=headline,
            company=profile.get("company", "Unknown"),
            content_section=content_section,
            icp_section=icp_section,
        )

        raw = await client.generate(prompt, system=_QUALIFY_SYSTEM, temperature=0.2, max_tokens=500)
        result = _parse_qualification_response(raw, active_icps)
        logger.info("Inbound qualified (LLM): %s → %s (%.0f%%)", profile.get("name"), result.intent, result.confidence * 100)
        return result

    except Exception as e:
        logger.warning("LLM qualify_inbound failed: %s, using keyword overlap", e)

    # 4. Fallback: keyword overlap only
    if best_overlap >= 0.3:
        return InboundQualification(
            intent="unknown",
            matched_icp_id=best_icp_id,
            confidence=best_overlap,
            recommended_action="ask_purpose" if best_overlap >= 0.4 else "accept_and_monitor",
            reasoning=f"Keyword overlap with ICP: {best_overlap:.0%}",
        )

    return InboundQualification(
        intent="unknown",
        matched_icp_id=None,
        confidence=0.2,
        recommended_action="accept_and_monitor",
        reasoning="No strong signals detected — worth monitoring.",
    )


# ──────────────────────────────────────────────
# Discovery DM Generation
# ──────────────────────────────────────────────

_DISCOVERY_SYSTEM = """You are a skilled SDR writing LinkedIn DMs. You read what people actually say and respond like a real human would — acknowledging their specific situation before moving the conversation forward.

Rules:
- Sound human and conversational, never scripted or robotic
- Match the sender's voice and tone
- ALWAYS reference what they specifically said — their question, challenge, news, or project
- If they asked a question: acknowledge it, relate to it briefly, then suggest a call or deeper chat — do NOT try to fully answer complex questions in a DM
- If they shared a challenge: show you understand, share a brief relevant insight, then open the door to help
- If they said "not interested" or "not now": respect it gracefully, leave the door open, don't push
- Only ask a generic "what brought you here?" question for silent connections with no message
- Keep it under 400 characters
- Never use salesy language, emojis, or exclamation marks
- Never hard-pitch — be genuinely helpful and curious

Output a JSON object with "message" and "reasoning" fields. No markdown or code fences."""

_DISCOVERY_PROMPT = """Generate a contextual LinkedIn reply.

My voice: {voice_desc}
{sender_context}

Signal type: {signal_type}
Their name: {name}
Their headline: {headline}
{content_section}
{qualification_section}

Reply naturally to what they said. Reference their specific words or situation. If they asked something, acknowledge it and suggest connecting for a proper conversation — don't try to give a full answer in a DM."""


# ──────────────────────────────────────────────
# Counter-Pitch Generation (for vendor_pitch intent)
# ──────────────────────────────────────────────

_COUNTER_PITCH_SYSTEM = """You are a skilled SDR writing a LinkedIn DM reply to someone who just pitched YOU their product/service. Your goal: flip the conversation — acknowledge their outreach briefly, then pivot to YOUR product naturally.

Rules:
- Sound human and conversational, never scripted or robotic
- Do NOT be dismissive or rude about their pitch — be warm and professional
- Briefly acknowledge what they do (1 short sentence max)
- Pivot naturally: mention something about what YOU do that could be relevant to THEM
- End with a soft question about their own pain point that your product solves
- Keep it under 400 characters
- Never use salesy language, emojis, or exclamation marks
- Never hard-pitch — be genuinely curious about their situation
- The tone should feel like a peer-to-peer exchange, not a rejection or counter-attack

Output a JSON object with "message" and "reasoning" fields. No markdown or code fences."""

_COUNTER_PITCH_PROMPT = """Generate a counter-pitch LinkedIn reply to a vendor who pitched me.

My voice: {voice_desc}
{sender_context}

My product/company: {my_offering}

Their name: {name}
Their headline: {headline}
Their pitch message:
\"\"\"
{content}
\"\"\"

Reply warmly, briefly acknowledge their service, then pivot to what I do. Ask about a pain point my product could solve for them or their clients."""


async def generate_counter_pitch(
    sender_profile: dict[str, Any],
    content: str,
    voice: dict[str, Any],
    campaign_context: dict[str, Any] | None = None,
) -> dict[str, str]:
    """Generate a counter-pitch reply to a vendor who pitched us.

    Returns dict with 'message' and 'reasoning' keys.
    """
    logger.info(
        "Generating counter-pitch for %s (headline='%s') — content='%s'",
        sender_profile.get("name", "?"),
        sender_profile.get("headline", "")[:60],
        (content or "")[:80],
    )
    voice_desc = f"Tone: {voice.get('tone', 'professional')}, style: {voice.get('sentence_length', 'concise')}"

    # Build our offering description from campaign context
    my_offering = ""
    if campaign_context:
        parts = []
        if campaign_context.get("relevance_hook"):
            parts.append(campaign_context["relevance_hook"])
        if campaign_context.get("target_description"):
            parts.append(f"Target audience: {campaign_context['target_description']}")
        my_offering = ". ".join(parts)
    if not my_offering:
        my_offering = "Not specified — keep the pivot generic and curiosity-driven."

    # Build sender context from stored profile
    sender_context = ""
    try:
        from ..db.queries import get_setting
        from ..db.engine import run as run_db
        my_profile = await run_db(get_setting, "profile", {})
        if my_profile:
            my_headline = my_profile.get("headline", "")
            if my_headline:
                sender_context = f"About me: {my_headline}"
    except Exception:
        pass

    prompt = _COUNTER_PITCH_PROMPT.format(
        voice_desc=voice_desc,
        sender_context=sender_context,
        my_offering=my_offering,
        name=sender_profile.get("name", "there"),
        headline=sender_profile.get("headline", ""),
        content=(content or "")[:800],
    )

    # Route through backend if in backend mode
    from ..config import has_local_llm_key, is_backend_mode
    if is_backend_mode() and not has_local_llm_key():
        from ..linkedin import get_linkedin_client
        backend_client = get_linkedin_client()
        try:
            my_headline = ""
            try:
                my_profile = await run_db(get_setting, "profile", {})
                my_headline = my_profile.get("headline", "") if my_profile else ""
            except Exception:
                pass
            return await backend_client.generate_counter_pitch(
                profile=sender_profile,
                content=content or "",
                voice=voice,
                campaign_context=campaign_context or {},
                sender_headline=my_headline,
            )
        except Exception as e:
            logger.warning("Backend generate_counter_pitch failed: %s", e)
        finally:
            await backend_client.close()

    # Local LLM
    try:
        client = LLMClient()
        raw = await client.generate(prompt, system=_COUNTER_PITCH_SYSTEM, temperature=0.7, max_tokens=500)
        text = raw.strip()
        if text.startswith("```"):
            text = re.sub(r"^```\w*\n?", "", text)
            text = re.sub(r"\n?```$", "", text)
        try:
            data = json.loads(text)
            return {
                "message": data.get("message", text),
                "reasoning": data.get("reasoning", ""),
            }
        except json.JSONDecodeError:
            return {"message": text[:400], "reasoning": ""}
    except Exception as e:
        logger.warning("Counter-pitch generation failed: %s", e)
        name = sender_profile.get("name", "").split()[0] if sender_profile.get("name") else "there"
        return {
            "message": f"Hey {name}, appreciate the outreach. Curious — how are you handling your own outbound prospecting?",
            "reasoning": "Fallback generic counter-pitch",
        }


async def generate_discovery_question(
    sender_profile: dict[str, Any],
    signal_type: str,
    content: str | None,
    voice: dict[str, Any],
    qualification: InboundQualification | None = None,
) -> dict[str, str]:
    """Generate a warm discovery DM to ask about the sender's purpose.

    Returns dict with 'message' and 'reasoning' keys.
    """
    logger.info(
        "Generating discovery DM for %s (headline='%s', signal=%s) — intent=%s confidence=%.2f content='%s'",
        sender_profile.get("name", "?"),
        sender_profile.get("headline", "")[:60],
        signal_type,
        qualification.intent if qualification else "?",
        qualification.confidence if qualification else 0,
        (content or "")[:80],
    )
    voice_desc = f"Tone: {voice.get('tone', 'professional')}, style: {voice.get('sentence_length', 'concise')}"

    content_section = f'Their message(s):\n"""\n{(content or "")[:800]}\n"""' if content else "No message — silent connection."

    qual_section = ""
    if qualification:
        qual_section = f"Qualification: {qualification.intent} ({qualification.confidence:.0%} confidence)"
        if qualification.reasoning:
            qual_section += f"\nContext: {qualification.reasoning}"

    # Build sender context from stored profile
    sender_context = ""
    try:
        from ..db.queries import get_setting
        from ..db.engine import run as run_db
        my_profile = await run_db(get_setting, "profile", {})
        if my_profile:
            my_headline = my_profile.get("headline", "")
            if my_headline:
                sender_context = f"About me: {my_headline}"
    except Exception:
        pass

    prompt = _DISCOVERY_PROMPT.format(
        voice_desc=voice_desc,
        sender_context=sender_context,
        signal_type=signal_type,
        name=sender_profile.get("name", "there"),
        headline=sender_profile.get("headline", ""),
        content_section=content_section,
        qualification_section=qual_section,
    )

    # Route through backend if in backend mode
    from ..config import has_local_llm_key, is_backend_mode
    if is_backend_mode() and not has_local_llm_key():
        from ..linkedin import get_linkedin_client
        backend_client = get_linkedin_client()
        try:
            # Get our headline for context
            my_headline = ""
            try:
                my_profile = await run_db(get_setting, "profile", {})
                my_headline = my_profile.get("headline", "") if my_profile else ""
            except Exception:
                pass
            return await backend_client.generate_discovery_dm(
                profile=sender_profile,
                signal_type=signal_type,
                content=content or "",
                voice=voice,
                qualification=qualification.to_dict() if qualification else {},
                sender_headline=my_headline,
            )
        except Exception as e:
            logger.warning("Backend generate_discovery_dm failed: %s", e)
        finally:
            await backend_client.close()

    # Local LLM
    try:
        client = LLMClient()
        raw = await client.generate(prompt, system=_DISCOVERY_SYSTEM, temperature=0.7, max_tokens=500)
        text = raw.strip()
        if text.startswith("```"):
            text = re.sub(r"^```\w*\n?", "", text)
            text = re.sub(r"\n?```$", "", text)
        try:
            data = json.loads(text)
            return {
                "message": data.get("message", text),
                "reasoning": data.get("reasoning", ""),
            }
        except json.JSONDecodeError:
            return {"message": text[:400], "reasoning": ""}
    except Exception as e:
        logger.warning("Discovery DM generation failed: %s", e)
        name = sender_profile.get("name", "").split()[0] if sender_profile.get("name") else "there"
        return {
            "message": f"Hey {name}, thanks for connecting! What prompted you to reach out?",
            "reasoning": "Fallback generic discovery question",
        }
