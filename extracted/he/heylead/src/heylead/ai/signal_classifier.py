"""AI: signal_classifier — 3-stage signal intent classification.

Mirrors the inbound_qualifier.py pattern:
1. Fast rules: keyword matching for obvious signals
2. ICP keyword overlap: match signal content against ICP pain points/keywords
3. LLM classification: full semantic analysis with engagement hook extraction

Classifies signals from prospect posts, keyword mentions, and other sources.
"""

from __future__ import annotations

import json
import logging
import re
from dataclasses import dataclass
from typing import Any

from ..db.async_bridge import run_db
from ..constants import (
    SIGNAL_CLASSIFY_BATCH,
    SIGNAL_COMPANY_CHANGE,
    SIGNAL_HEADLINE_CHANGE,
    SIGNAL_HEADLINE_INTENT,
    SIGNAL_INTENT_BUYING,
    SIGNAL_INTENT_COMPETITOR_EVAL,
    SIGNAL_INTENT_JOB_SEEKING,
    SIGNAL_INTENT_PAIN_POINT,
    SIGNAL_INTENT_THOUGHT_LEADERSHIP,
    SIGNAL_INTENT_UNKNOWN,
    SIGNAL_PROMOTION,
    SIGNAL_STATUS_CLASSIFIED,
    SIGNAL_STATUS_NEW,
)

logger = logging.getLogger(__name__)

# ──────────────────────────────────────────────
# Output schema
# ──────────────────────────────────────────────


@dataclass
class SignalClassification:
    """Result of classifying a signal's intent."""

    intent: str  # buying_signal, pain_point, competitor_eval, thought_leadership, job_seeking, unknown
    confidence: float  # 0.0 - 1.0
    pain_points_detected: list[str]
    keywords_matched: list[str]
    engagement_hook: str  # Suggested angle for outreach referencing this signal
    reasoning: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "intent": self.intent,
            "confidence": self.confidence,
            "pain_points_detected": self.pain_points_detected,
            "keywords_matched": self.keywords_matched,
            "engagement_hook": self.engagement_hook,
            "reasoning": self.reasoning,
        }


# ──────────────────────────────────────────────
# Stage 1: Fast rule-based classification
# ──────────────────────────────────────────────

# Buying signal keywords — someone is actively looking for a solution
_BUYING_KEYWORDS = [
    "looking for a tool",
    "looking for a solution",
    "need a better way",
    "anyone recommend",
    "any recommendations",
    "can anyone suggest",
    "what tool do you use",
    "which platform",
    "evaluating options",
    "in the market for",
    "ready to switch",
    "demo request",
    "free trial",
    "pricing",
    "compared to",
    "switching from",
    "moving away from",
    "replacing our",
    "need help with",
    "struggling with",
    "frustrated with",
    "tired of",
]

# Pain point keywords — expressing a problem that our product solves
_PAIN_POINT_KEYWORDS = [
    "biggest challenge",
    "main struggle",
    "pain point",
    "bottleneck",
    "time-consuming",
    "manual process",
    "not scalable",
    "low response rate",
    "low reply rate",
    "cold outreach",
    "outbound is dead",
    "outreach fatigue",
    "personalization at scale",
    "hard to reach",
    "getting ghosted",
]

# Competitor evaluation — mentioning competitor names or comparing tools
_COMPETITOR_KEYWORDS = [
    "outreach.io",
    "salesloft",
    "apollo",
    "lemlist",
    "instantly",
    "woodpecker",
    "mailshake",
    "reply.io",
    "smartlead",
    "clay.com",
    "trigify",
    "unify",
    "common room",
    "usergems",
    "warmly",
    "linkedin automation",
    "sales engagement",
]

# Job seeking signals
_JOB_SEEKING_KEYWORDS = [
    "open to work",
    "looking for opportunities",
    "available for hire",
    "seeking new role",
    "recently laid off",
    "exploring opportunities",
    "#opentowork",
    "just got laid off",
    "let go from",
    "looking for my next",
]


def _detect_mention_context(content: str) -> str:
    """Detect mention context for competitor signals.

    Returns one of: "switching_from", "evaluating", "complaint", "general".
    Used by the activator's hot signal fast-track.
    """
    lower = content.lower()
    for kw in ("switching from", "moving away", "replacing", "looking for alternative",
                "leaving", "ditching", "dropping", "migrating from"):
        if kw in lower:
            return "switching_from"
    for kw in ("evaluating", "comparing", "vs ", " or ", "which is better",
                "considering", "looking at", "exploring options"):
        if kw in lower:
            return "evaluating"
    for kw in ("frustrated", "terrible", "worst", "overpriced", "pricing is crazy",
                "too expensive", "broken", "doesn't work", "hate", "sucks"):
        if kw in lower:
            return "complaint"
    return "general"


def _classify_fast(content: str) -> SignalClassification | None:
    """Stage 1: Fast rule-based classification.

    Returns a classification if strong signal detected, None otherwise.
    """
    content_lower = content.lower()

    # Check buying signals
    matched_buying = [kw for kw in _BUYING_KEYWORDS if kw in content_lower]
    if len(matched_buying) >= 2:
        return SignalClassification(
            intent=SIGNAL_INTENT_BUYING,
            confidence=0.85,
            pain_points_detected=[],
            keywords_matched=matched_buying,
            engagement_hook=f"They're actively searching — mentioned: {', '.join(matched_buying[:3])}",
            reasoning=f"Multiple buying signal keywords detected: {', '.join(matched_buying[:3])}",
        )

    # Check pain points
    matched_pain = [kw for kw in _PAIN_POINT_KEYWORDS if kw in content_lower]
    if len(matched_pain) >= 2:
        return SignalClassification(
            intent=SIGNAL_INTENT_PAIN_POINT,
            confidence=0.75,
            pain_points_detected=matched_pain,
            keywords_matched=matched_pain,
            engagement_hook=f"They're experiencing pain — mentioned: {', '.join(matched_pain[:3])}",
            reasoning=f"Multiple pain point keywords detected: {', '.join(matched_pain[:3])}",
        )

    # Check competitor mentions
    matched_comp = [kw for kw in _COMPETITOR_KEYWORDS if kw in content_lower]
    if matched_comp:
        return SignalClassification(
            intent=SIGNAL_INTENT_COMPETITOR_EVAL,
            confidence=0.80,
            pain_points_detected=[],
            keywords_matched=matched_comp,
            engagement_hook=f"Mentioned competitor(s): {', '.join(matched_comp[:3])} — opportunity for displacement",
            reasoning=f"Competitor mention detected: {', '.join(matched_comp[:3])}",
        )

    # Check job seeking
    matched_job = [kw for kw in _JOB_SEEKING_KEYWORDS if kw in content_lower]
    if matched_job:
        return SignalClassification(
            intent=SIGNAL_INTENT_JOB_SEEKING,
            confidence=0.80,
            pain_points_detected=[],
            keywords_matched=matched_job,
            engagement_hook="",
            reasoning=f"Job seeking language detected: {', '.join(matched_job[:2])}",
        )

    # Single strong buying keyword
    if matched_buying:
        return SignalClassification(
            intent=SIGNAL_INTENT_BUYING,
            confidence=0.60,
            pain_points_detected=[],
            keywords_matched=matched_buying,
            engagement_hook=f"Possible buying intent — mentioned: {matched_buying[0]}",
            reasoning=f"Single buying signal keyword: {matched_buying[0]}",
        )

    return None


# ──────────────────────────────────────────────
# Stage 2: ICP keyword overlap
# ──────────────────────────────────────────────


def _compute_icp_overlap(
    content: str,
    icp_data: dict[str, Any],
) -> tuple[float, list[str], list[str]]:
    """Compute overlap between signal content and ICP keywords/pain points.

    Returns:
        (overlap_score, matched_keywords, matched_pain_points)
    """
    content_lower = content.lower()
    matched_keywords: list[str] = []
    matched_pain_points: list[str] = []

    # Extract keywords from ICP
    icp_keywords: list[str] = []

    # Direct keywords
    kws = icp_data.get("keywords", [])
    if isinstance(kws, list):
        icp_keywords.extend(str(k).lower() for k in kws if k)

    # Pain points
    pps = icp_data.get("pain_points", [])
    if isinstance(pps, list):
        for pp in pps:
            pp_str = str(pp).lower()
            # Extract key phrases (2+ word chunks)
            words = pp_str.split()
            if len(words) <= 4:
                icp_keywords.append(pp_str)
            else:
                # Use sliding window for long pain points
                for i in range(len(words) - 1):
                    icp_keywords.append(f"{words[i]} {words[i + 1]}")

    # Job titles (include list)
    jt = icp_data.get("job_titles", {})
    if isinstance(jt, dict):
        for title in (jt.get("include") or []):
            icp_keywords.append(str(title).lower())
    elif isinstance(jt, list):
        for title in jt:
            icp_keywords.append(str(title).lower())

    # Industries (include list)
    ind = icp_data.get("industries", {})
    if isinstance(ind, dict):
        for industry in (ind.get("include") or []):
            icp_keywords.append(str(industry).lower())
    elif isinstance(ind, list):
        for industry in ind:
            icp_keywords.append(str(industry).lower())

    if not icp_keywords:
        return 0.0, [], []

    # Deduplicate
    icp_keywords = list(set(icp_keywords))

    # Match
    for kw in icp_keywords:
        if not kw or len(kw) < 3:
            continue
        if kw in content_lower:
            matched_keywords.append(kw)
            # Track if it came from pain points
            for pp in pps:
                if kw in str(pp).lower():
                    matched_pain_points.append(str(pp))
                    break

    if not icp_keywords:
        return 0.0, matched_keywords, matched_pain_points

    overlap = len(matched_keywords) / len(icp_keywords)
    return min(overlap * 3, 1.0), matched_keywords, list(set(matched_pain_points))  # Boost: 3x multiplier


# ──────────────────────────────────────────────
# Stage 3: LLM classification
# ──────────────────────────────────────────────

_CLASSIFY_SYSTEM = """You are an expert B2B sales signal analyst. Given a LinkedIn post by a prospect, \
analyze it for buying signals relevant to the company's ICPs (Ideal Customer Profiles).

You are looking for:
- Buying intent: actively seeking solutions, evaluating tools, requesting recommendations
- Pain points: expressing frustration, challenges, bottlenecks that the company's product could solve
- Competitor evaluation: mentioning or comparing competitor products
- Thought leadership: sharing expertise relevant to the ICP's domain (good for engagement, lower priority)
- Job seeking: career transition signals

Output ONLY a JSON object with these fields:
- intent: "buying_signal" | "pain_point" | "competitor_eval" | "thought_leadership" | "job_seeking" | "unknown"
- confidence: 0.0-1.0
- pain_points_detected: [list of pain points expressed in the post]
- keywords_matched: [list of ICP-relevant keywords found]
- engagement_hook: "1-2 sentence suggested angle for outreach referencing this post naturally"
- reasoning: "1-2 sentence explanation of classification"
"""

_CLASSIFY_PROMPT = """Analyze this LinkedIn post for buying signals:

Post author: {name} ({headline}, {company})
Post text:
---
{post_text}
---

Active ICPs:
{icp_section}

Classify the post's intent and extract actionable insights."""


def _build_icp_section(active_icps: list[dict[str, Any]]) -> str:
    """Build a compact ICP summary for the LLM prompt."""
    if not active_icps:
        return "No ICPs defined."

    parts: list[str] = []
    for icp_row in active_icps[:3]:  # Max 3 ICPs to keep prompt short
        icp_json_str = icp_row.get("icp_json", "{}")
        try:
            parsed = json.loads(icp_json_str) if isinstance(icp_json_str, str) else icp_json_str
        except (json.JSONDecodeError, TypeError):
            continue

        icp_name = icp_row.get("name", "Unknown")
        # Get sub-ICPs
        sub_icps = parsed.get("icps", [parsed]) if parsed else []
        for sub in sub_icps[:2]:  # Max 2 sub-ICPs per ICP
            desc = str(sub.get("description", ""))[:150]
            pps = sub.get("pain_points", [])[:3]
            kws = sub.get("keywords", [])[:5]
            pain_str = ", ".join(str(p) for p in pps) if pps else "none"
            kw_str = ", ".join(str(k) for k in kws) if kws else "none"
            parts.append(
                f"ICP '{icp_name}': {desc}\n"
                f"  Pain points: {pain_str}\n"
                f"  Keywords: {kw_str}"
            )

    return "\n\n".join(parts) if parts else "No ICP details available."


def _parse_classification_response(
    raw: str,
) -> SignalClassification:
    """Parse LLM JSON response into SignalClassification."""
    # Strip markdown fences
    text = raw.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*\n?", "", text)
        text = re.sub(r"\n?```\s*$", "", text)

    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        # Try to extract JSON from surrounding text
        match = re.search(r"\{[\s\S]*\}", text)
        if match:
            try:
                data = json.loads(match.group())
            except json.JSONDecodeError:
                return _fallback_classification("Could not parse LLM response as JSON")
        else:
            return _fallback_classification("No JSON found in LLM response")

    # Validate intent
    valid_intents = {
        SIGNAL_INTENT_BUYING, SIGNAL_INTENT_PAIN_POINT,
        SIGNAL_INTENT_COMPETITOR_EVAL, SIGNAL_INTENT_THOUGHT_LEADERSHIP,
        SIGNAL_INTENT_JOB_SEEKING, SIGNAL_INTENT_UNKNOWN,
    }
    intent = data.get("intent", SIGNAL_INTENT_UNKNOWN)
    if intent not in valid_intents:
        intent = SIGNAL_INTENT_UNKNOWN

    # Validate confidence
    confidence = data.get("confidence", 0.3)
    try:
        confidence = float(confidence)
    except (ValueError, TypeError):
        confidence = 0.3
    confidence = max(0.0, min(1.0, confidence))

    return SignalClassification(
        intent=intent,
        confidence=confidence,
        pain_points_detected=data.get("pain_points_detected", []) or [],
        keywords_matched=data.get("keywords_matched", []) or [],
        engagement_hook=str(data.get("engagement_hook", "")),
        reasoning=str(data.get("reasoning", "")),
    )


def _fallback_classification(reason: str) -> SignalClassification:
    """Return a low-confidence unknown classification."""
    return SignalClassification(
        intent=SIGNAL_INTENT_UNKNOWN,
        confidence=0.2,
        pain_points_detected=[],
        keywords_matched=[],
        engagement_hook="",
        reasoning=reason,
    )


# ──────────────────────────────────────────────
# Main classification function
# ──────────────────────────────────────────────


async def classify_signal(
    content: str,
    author_name: str = "",
    author_headline: str = "",
    author_company: str = "",
    active_icps: list[dict[str, Any]] | None = None,
) -> SignalClassification:
    """Classify a signal's intent using the 3-stage pipeline.

    Args:
        content: The signal text (post text, keyword mention, etc.)
        author_name: Name of the person who created the content.
        author_headline: Their LinkedIn headline.
        author_company: Their company name.
        active_icps: List of ICP dicts from list_icps(status='active').

    Returns:
        SignalClassification with intent, confidence, and engagement hook.
    """
    if not content or not content.strip():
        return _fallback_classification("Empty signal content")

    icps = active_icps or []

    # ── Stage 1: Fast rules ──
    fast_result = _classify_fast(content)
    if fast_result and fast_result.confidence >= 0.75:
        logger.info(
            "Signal classified (fast): %s → %s (%.0f%%)",
            author_name or "unknown", fast_result.intent, fast_result.confidence * 100,
        )
        return fast_result

    # ── Stage 2: ICP keyword overlap ──
    best_overlap = 0.0
    best_keywords: list[str] = []
    best_pain_points: list[str] = []

    for icp_row in icps:
        icp_json_str = icp_row.get("icp_json", "{}")
        try:
            parsed = json.loads(icp_json_str) if isinstance(icp_json_str, str) else icp_json_str
        except (json.JSONDecodeError, TypeError):
            continue

        for single_icp in (parsed.get("icps", [parsed]) if parsed else []):
            overlap, matched_kws, matched_pps = _compute_icp_overlap(content, single_icp)
            if overlap > best_overlap:
                best_overlap = overlap
                best_keywords = matched_kws
                best_pain_points = matched_pps

    # Merge fast result with ICP overlap for boosted confidence
    if fast_result and best_overlap > 0:
        # Boost fast result confidence with ICP overlap
        boosted_confidence = min(fast_result.confidence + (best_overlap * 0.2), 1.0)
        fast_result.confidence = boosted_confidence
        fast_result.keywords_matched = list(set(fast_result.keywords_matched + best_keywords))
        fast_result.pain_points_detected = list(set(fast_result.pain_points_detected + best_pain_points))
        logger.info(
            "Signal classified (fast+ICP boost): %s → %s (%.0f%%)",
            author_name or "unknown", fast_result.intent, fast_result.confidence * 100,
        )
        return fast_result

    # ── Stage 3: LLM classification ──
    from ..config import has_local_llm_key, is_backend_mode

    # Try backend route first
    if is_backend_mode() and not has_local_llm_key():
        from ..linkedin import get_linkedin_client

        backend_client = get_linkedin_client()
        try:
            result = await backend_client.classify_signal(
                content=content,
                author_name=author_name,
                author_headline=author_headline,
                author_company=author_company,
                icp_summaries=[
                    {
                        "id": icp.get("id"),
                        "name": icp.get("name"),
                        "icp_json": icp.get("icp_json", "{}"),
                    }
                    for icp in icps
                ],
            )
            logger.info(
                "Signal classified (backend): %s → %s (%.0f%%)",
                author_name or "unknown", result.intent, result.confidence * 100,
            )
            return result
        except Exception as e:
            logger.warning("Backend classify_signal failed: %s, trying local LLM", e)
        finally:
            await backend_client.close()

    # Try local LLM
    try:
        from .llm import LLMClient

        client = LLMClient()
        icp_section = _build_icp_section(icps)

        prompt = _CLASSIFY_PROMPT.format(
            name=author_name or "Unknown",
            headline=author_headline or "Unknown",
            company=author_company or "Unknown",
            post_text=content[:1500],  # Limit content length
            icp_section=icp_section,
        )

        raw = await client.generate(prompt, system=_CLASSIFY_SYSTEM, temperature=0.2, max_tokens=500)
        result = _parse_classification_response(raw)
        logger.info(
            "Signal classified (LLM): %s → %s (%.0f%%)",
            author_name or "unknown", result.intent, result.confidence * 100,
        )
        return result

    except Exception as e:
        logger.warning("LLM classify_signal failed: %s, using keyword overlap", e)

    # ── Fallback: keyword overlap only ──
    if best_overlap >= 0.2:
        intent = SIGNAL_INTENT_PAIN_POINT if best_pain_points else SIGNAL_INTENT_UNKNOWN
        return SignalClassification(
            intent=intent,
            confidence=best_overlap,
            pain_points_detected=best_pain_points,
            keywords_matched=best_keywords,
            engagement_hook=f"ICP keyword overlap ({best_overlap:.0%}) — matches: {', '.join(best_keywords[:3])}" if best_keywords else "",
            reasoning=f"ICP keyword overlap: {best_overlap:.0%}",
        )

    # If fast result exists with lower confidence, return it
    if fast_result:
        return fast_result

    return _fallback_classification("No strong signals detected in content.")


# ──────────────────────────────────────────────
# Batch classification for scheduler
# ──────────────────────────────────────────────


async def classify_pending_signals() -> str:
    """Classify all signals with status='new'.

    Called by the scheduler every SIGNAL_CLASSIFY_SECONDS.

    Flow:
    1. Fetch signals with status='new' (limited by SIGNAL_CLASSIFY_BATCH)
    2. Load active ICPs for context
    3. Classify each signal
    4. Update signal with intent, confidence, reasoning, engagement_hook
    5. Set status to 'classified'

    Returns:
        Summary string of results.
    """
    from ..db.queries import list_icps
    from ..db.signal_queries import list_signals, update_signal

    # Get unclassified signals
    signals = await run_db(list_signals, status=SIGNAL_STATUS_NEW, limit=SIGNAL_CLASSIFY_BATCH)
    if not signals:
        return "No signals pending classification."

    # Load active ICPs for context
    active_icps = await run_db(list_icps, status="active")

    classified = 0
    errors = 0

    for signal in signals:
        signal_id = signal.get("id", "")
        content = signal.get("content", "")
        prospect_name = signal.get("prospect_name", "")
        prospect_title = signal.get("prospect_title", "")

        # Extract company from metadata
        metadata = {}
        meta_str = signal.get("metadata_json", "")
        if meta_str:
            try:
                metadata = json.loads(meta_str)
            except (json.JSONDecodeError, TypeError):
                pass
        company = metadata.get("contact_company", "") or metadata.get("company", "")

        # ── Fast-path: profile change signals (already validated by collector) ──
        signal_type = signal.get("signal_type", "")
        if signal_type in (SIGNAL_COMPANY_CHANGE, SIGNAL_PROMOTION):
            import time
            await run_db(
                update_signal,
                signal_id=signal_id,
                intent=SIGNAL_INTENT_BUYING,
                confidence=0.70,
                reasoning=f"Profile change ({signal_type}) indicates potential buying opportunity",
                status=SIGNAL_STATUS_CLASSIFIED,
                classified_at=int(time.time()),
            )
            classified += 1
            continue

        if signal_type == SIGNAL_HEADLINE_INTENT:
            import time
            intent_cats = metadata.get("intent_categories", [])
            if any(c in ("hiring", "evaluating") for c in intent_cats):
                hi_intent = SIGNAL_INTENT_BUYING
                hi_conf = 0.75
            elif "building" in intent_cats:
                hi_intent = SIGNAL_INTENT_BUYING
                hi_conf = 0.60
            elif "open_to_opportunities" in intent_cats:
                hi_intent = SIGNAL_INTENT_JOB_SEEKING
                hi_conf = 0.80
            else:
                hi_intent = SIGNAL_INTENT_UNKNOWN
                hi_conf = 0.40
            await run_db(
                update_signal,
                signal_id=signal_id,
                intent=hi_intent,
                confidence=hi_conf,
                reasoning=f"Headline intent categories: {', '.join(intent_cats)}",
                status=SIGNAL_STATUS_CLASSIFIED,
                classified_at=int(time.time()),
            )
            classified += 1
            continue

        if signal_type == SIGNAL_HEADLINE_CHANGE:
            import time
            await run_db(
                update_signal,
                signal_id=signal_id,
                intent=SIGNAL_INTENT_UNKNOWN,
                confidence=0.30,
                reasoning="Generic headline change, no strong intent signal",
                status=SIGNAL_STATUS_CLASSIFIED,
                classified_at=int(time.time()),
            )
            classified += 1
            continue

        try:
            result = await classify_signal(
                content=content,
                author_name=prospect_name,
                author_headline=prospect_title,
                author_company=company,
                active_icps=active_icps,
            )

            # Author pattern boost: repeated topic → higher confidence
            linkedin_id = signal.get("linkedin_id", "")
            confidence = result.confidence
            pattern_note = ""
            if linkedin_id and result.intent != SIGNAL_INTENT_UNKNOWN:
                try:
                    from ..constants import (
                        AUTHOR_PATTERN_CONFIDENCE_BOOST,
                        AUTHOR_PATTERN_MIN_POSTS,
                        AUTHOR_PATTERN_WINDOW_DAYS,
                    )
                    from ..db.post_queries import get_recent_topics_by_author

                    topics = await run_db(
                        get_recent_topics_by_author,
                        linkedin_id, days=AUTHOR_PATTERN_WINDOW_DAYS,
                    )
                    # Check if any topic appears enough times for a pattern
                    repeated = {t: c for t, c in topics.items() if c >= AUTHOR_PATTERN_MIN_POSTS}
                    if repeated:
                        confidence = min(1.0, confidence + AUTHOR_PATTERN_CONFIDENCE_BOOST)
                        top_topic = max(repeated, key=repeated.get)
                        pattern_note = (
                            f" [Author pattern: posted about '{top_topic}' "
                            f"{repeated[top_topic]}x in {AUTHOR_PATTERN_WINDOW_DAYS}d]"
                        )
                except Exception:
                    pass  # Pattern detection failure doesn't block classification

            # Update signal with classification results
            import time

            # Merge classification metadata into existing metadata
            classification_meta = {
                **metadata,
                "pain_points_detected": result.pain_points_detected,
                "keywords_matched": result.keywords_matched,
                "engagement_hook": result.engagement_hook,
            }
            if pattern_note:
                classification_meta["author_pattern"] = pattern_note.strip(" []")

            # Detect mention_context for competitor signals (used by fast-track)
            if signal.get("signal_type") == "competitor_mention" and content:
                mention_context = _detect_mention_context(content)
                classification_meta["mention_context"] = mention_context

            await run_db(
                update_signal,
                signal_id=signal_id,
                intent=result.intent,
                confidence=confidence,
                reasoning=result.reasoning + pattern_note,
                status=SIGNAL_STATUS_CLASSIFIED,
                classified_at=int(time.time()),
                metadata_json=json.dumps(classification_meta),
            )
            classified += 1

        except Exception as e:
            logger.warning("Failed to classify signal %s: %s", signal_id[:8], e)
            errors += 1

    summary = f"Signal classification complete: {classified}/{len(signals)} classified"
    if errors:
        summary += f", {errors} errors"
    logger.info(summary)
    return summary
