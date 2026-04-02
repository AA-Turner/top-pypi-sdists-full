"""ICP match scoring and composite lead scoring for campaign prioritization.

Replaces the old data-completeness heuristic with actual ICP attribute
matching across 6 dimensions: title, industry, seniority, company size,
location, and keyword overlap.

Also provides a unified composite lead score that combines ICP match,
revenue estimate, signal score, engagement history, and historical
segment performance into a single 0-1 priority score.

No LLM calls — all heuristic-based for speed and consistency.
"""

from __future__ import annotations

import json
import logging
import time
from typing import Any

from ..db.async_bridge import run_db
from ..constants import SENIORITY_KEYWORDS
from .revenue_estimator import (
    extract_headcount,
    extract_industry,
    infer_seniority,
    parse_json_field,
)

logger = logging.getLogger(__name__)

# ──────────────────────────────────────────────
# ICP Match Score Weights
# ──────────────────────────────────────────────

ICP_WEIGHT_TITLE = 0.30
ICP_WEIGHT_INDUSTRY = 0.20
ICP_WEIGHT_SENIORITY = 0.15
ICP_WEIGHT_COMPANY_SIZE = 0.15
ICP_WEIGHT_LOCATION = 0.10
ICP_WEIGHT_KEYWORDS = 0.10

# Neutral scores for unknown/missing data (don't penalize, don't reward)
UNKNOWN_SCORE = 0.3
LOCATION_UNKNOWN_SCORE = 0.5

# ──────────────────────────────────────────────
# Composite Lead Score Weights
# ──────────────────────────────────────────────

COMPOSITE_WEIGHT_ICP_MATCH = 0.30
COMPOSITE_WEIGHT_REVENUE = 0.25
COMPOSITE_WEIGHT_SIGNAL = 0.20
COMPOSITE_WEIGHT_ENGAGEMENT = 0.15
COMPOSITE_WEIGHT_SEGMENT = 0.10

# Revenue normalization cap ($100K ACV = 1.0)
REVENUE_NORM_CAP = 100_000


# ──────────────────────────────────────────────
# ICP Match Scoring
# ──────────────────────────────────────────────

def compute_icp_match(
    contact: dict[str, Any],
    campaign_icp_json: str | dict | None = None,
) -> dict[str, Any]:
    """Score a contact against the campaign ICP (0.0-1.0).

    Args:
        contact: Contact dict with title, company, location, profile_json, analysis_json.
        campaign_icp_json: Campaign ICP as JSON string or parsed dict.

    Returns:
        {"icp_match_score": float, "breakdown": {dimension: score}}.
    """
    icp = _parse_first_icp(campaign_icp_json)
    if not icp:
        # No ICP data — return neutral score
        return {"icp_match_score": UNKNOWN_SCORE, "breakdown": {}}

    title_score = _score_title_match(contact.get("title", ""), icp)
    industry_score = _score_industry_match(contact, icp, campaign_icp_json)
    seniority_score = _score_seniority_match(contact.get("title", ""), icp)
    size_score = _score_company_size(contact, icp, campaign_icp_json)
    location_score = _score_location_match(contact, icp)
    keyword_score = _score_keyword_overlap(contact, icp)

    breakdown = {
        "title": title_score,
        "industry": industry_score,
        "seniority": seniority_score,
        "company_size": size_score,
        "location": location_score,
        "keywords": keyword_score,
    }

    raw = (
        ICP_WEIGHT_TITLE * title_score
        + ICP_WEIGHT_INDUSTRY * industry_score
        + ICP_WEIGHT_SENIORITY * seniority_score
        + ICP_WEIGHT_COMPANY_SIZE * size_score
        + ICP_WEIGHT_LOCATION * location_score
        + ICP_WEIGHT_KEYWORDS * keyword_score
    )

    icp_match = round(max(0.0, min(1.0, raw)), 4)
    return {"icp_match_score": icp_match, "breakdown": breakdown}


# ──────────────────────────────────────────────
# Composite Lead Score
# ──────────────────────────────────────────────

def compute_composite_lead_score(
    contact: dict[str, Any],
    campaign_icp_json: str | dict | None = None,
    patterns: list[dict[str, Any]] | None = None,
) -> float:
    """Unified 0-1 composite score combining all available signals.

    Components (weights sum to 1.0):
    - ICP Match (0.30): How well prospect matches campaign ICP
    - Revenue Estimate (0.25): Normalized estimated_revenue
    - Signal Score (0.20): From signal_accounts composite_score
    - Engagement Score (0.15): Behavioral engagement history
    - Segment Performance (0.10): Historical conversion for matching segment

    Args:
        contact: Contact dict (must include id, title, company, linkedin_id, etc.)
        campaign_icp_json: Campaign ICP JSON.
        patterns: Strategy patterns for segment performance lookup.

    Returns:
        Composite score 0.0-1.0.
    """
    # 1. ICP Match
    icp_result = compute_icp_match(contact, campaign_icp_json)
    icp_score = icp_result["icp_match_score"]

    # 2. Revenue (normalized to 0-1)
    revenue_raw = contact.get("estimated_revenue", 0) or 0
    revenue_score = min(revenue_raw / REVENUE_NORM_CAP, 1.0) if revenue_raw > 0 else 0.0

    # 3. Signal Score
    signal_score = _get_signal_score(contact.get("linkedin_id", ""))

    # 4. Engagement Score
    engagement_score = _compute_engagement_score(
        contact.get("id", ""),
        contact.get("linkedin_id", ""),
    )

    # 5. Segment Performance
    segment_score = _get_segment_performance_score(contact, patterns)

    composite = (
        COMPOSITE_WEIGHT_ICP_MATCH * icp_score
        + COMPOSITE_WEIGHT_REVENUE * revenue_score
        + COMPOSITE_WEIGHT_SIGNAL * signal_score
        + COMPOSITE_WEIGHT_ENGAGEMENT * engagement_score
        + COMPOSITE_WEIGHT_SEGMENT * segment_score
    )

    return round(max(0.0, min(1.0, composite)), 4)


# ──────────────────────────────────────────────
# Backfill
# ──────────────────────────────────────────────

async def backfill_icp_match_scores(limit: int = 500) -> int:
    """Re-score contacts with ICP match instead of data completeness.

    Targets contacts whose fit_score was set by the old heuristic
    (typically rounded to 2 decimal places from the data-completeness formula).

    Returns:
        Number of contacts updated.
    """
    def _do_backfill():
        from ..db.schema import get_db

        db = get_db()
        rows = db.execute("""
            SELECT c.id, c.title, c.company, c.linkedin_id,
                   c.profile_json, c.analysis_json, c.fit_score,
                   c.estimated_revenue, camp.icp_json
            FROM contacts c
            LEFT JOIN campaigns camp ON c.campaign_id = camp.id
            WHERE camp.icp_json IS NOT NULL AND camp.icp_json != ''
            ORDER BY c.created_at DESC
            LIMIT ?
        """, (limit,)).fetchall()
        db.close()

        if not rows:
            return 0

        updated = 0
        db = get_db()
        for row in rows:
            contact = dict(row)
            icp_json = contact.get("icp_json")
            if not icp_json:
                continue

            result = compute_icp_match(contact, icp_json)
            new_score = result["icp_match_score"]
            old_score = contact.get("fit_score", 0) or 0

            if abs(new_score - old_score) > 0.01:
                db.execute(
                    "UPDATE contacts SET fit_score = ? WHERE id = ?",
                    (new_score, contact["id"]),
                )
                updated += 1

        if updated:
            db.commit()
            logger.info("ICP match scorer: backfilled %d contacts", updated)
        db.close()
        return updated

    return await run_db(_do_backfill)


# ──────────────────────────────────────────────
# ICP Match — Dimension Scorers
# ──────────────────────────────────────────────

def _parse_first_icp(campaign_icp_json: str | dict | None) -> dict[str, Any] | None:
    """Parse the first ICP from campaign ICP JSON.

    Handles two formats:
    - Modern: {"icps": [{"job_titles": {"include": [...]}, ...}]}
    - Legacy: {"segments": [{"titles": [...], "keywords": "...", ...}]}
    """
    if not campaign_icp_json:
        return None

    if isinstance(campaign_icp_json, str):
        try:
            data = json.loads(campaign_icp_json)
        except (json.JSONDecodeError, TypeError):
            return None
    else:
        data = campaign_icp_json

    if isinstance(data, dict):
        # Modern format: icps[]
        icps = data.get("icps", [])
        if isinstance(icps, list) and icps:
            first = icps[0]
            return first if isinstance(first, dict) else None

        # Legacy format: segments[] — convert to ICP dict
        segments = data.get("segments", [])
        if isinstance(segments, list) and segments:
            seg = segments[0]
            if isinstance(seg, dict):
                return _segment_to_icp(seg)

    return None


def _segment_to_icp(seg: dict[str, Any]) -> dict[str, Any]:
    """Convert a legacy segment dict to ICP dict format.

    Segment format: {"titles": [...], "industries": [...], "seniority": [...],
                     "locations": [...], "keywords": "comma,separated",
                     "company_headcount": {"min": N, "max": N}}
    ICP format: {"job_titles": {"include": [...]}, "industries": {"include": [...]}, ...}
    """
    titles = seg.get("titles", [])
    industries = seg.get("industries", [])
    locations = seg.get("locations", [])
    seniority = seg.get("seniority", [])

    # Keywords: segment stores as comma-separated string, ICP as list
    keywords_raw = seg.get("keywords", "")
    if isinstance(keywords_raw, str):
        keywords = [k.strip() for k in keywords_raw.split(",") if k.strip()]
    elif isinstance(keywords_raw, list):
        keywords = keywords_raw
    else:
        keywords = []

    return {
        "job_titles": {"include": titles, "exclude": []},
        "industries": {"include": industries, "exclude": []},
        "seniority": {"include": seniority, "exclude": []},
        "locations": {"include": locations, "exclude": []},
        "company_headcount": seg.get("company_headcount") or {},
        "keywords": keywords,
    }


def _get_include_exclude(icp: dict, field: str) -> tuple[list[str], list[str]]:
    """Extract include/exclude lists from an ICP field (LinkedinSearchParam format)."""
    val = icp.get(field)
    if isinstance(val, dict):
        include = [s.lower().strip() for s in val.get("include", []) if s]
        exclude = [s.lower().strip() for s in val.get("exclude", []) if s]
        return include, exclude
    if isinstance(val, list):
        return [s.lower().strip() for s in val if s], []
    return [], []


def _score_title_match(title: str, icp: dict) -> float:
    """Score title match against ICP job_titles (0.0-1.0)."""
    if not title:
        return UNKNOWN_SCORE

    title_lower = title.lower().strip()
    include, exclude = _get_include_exclude(icp, "job_titles")

    # Exclude check first — disqualify immediately
    for term in exclude:
        if term in title_lower:
            return 0.0

    if not include:
        return UNKNOWN_SCORE

    # Exact match (full title contains a full include term)
    for term in include:
        if term in title_lower:
            return 1.0

    # Partial word overlap: check individual words from include terms
    title_words = set(title_lower.split())
    best_overlap = 0.0
    for term in include:
        term_words = set(term.split())
        if not term_words:
            continue
        overlap = len(title_words & term_words) / len(term_words)
        best_overlap = max(best_overlap, overlap)

    if best_overlap >= 0.5:
        return 0.3 + (best_overlap * 0.4)  # 0.5 overlap → 0.5, 1.0 overlap → 0.7

    return 0.1  # Title exists but no match


def _score_industry_match(
    contact: dict[str, Any],
    icp: dict,
    campaign_icp_json: str | dict | None = None,
) -> float:
    """Score industry match against ICP industries (0.0-1.0)."""
    parsed_icp = None
    if isinstance(campaign_icp_json, str):
        try:
            parsed_icp = json.loads(campaign_icp_json)
        except (json.JSONDecodeError, TypeError):
            pass
    elif isinstance(campaign_icp_json, dict):
        parsed_icp = campaign_icp_json

    industry = extract_industry(contact, parsed_icp)
    if not industry:
        return UNKNOWN_SCORE

    include, exclude = _get_include_exclude(icp, "industries")

    # Exclude check
    for term in exclude:
        if term in industry or industry in term:
            return 0.0

    if not include:
        return UNKNOWN_SCORE

    # Exact match
    for term in include:
        if term == industry or term in industry or industry in term:
            return 1.0

    # No match
    return 0.1


def _score_seniority_match(title: str, icp: dict) -> float:
    """Score seniority match against ICP seniority (0.0-1.0)."""
    if not title:
        return UNKNOWN_SCORE

    seniority = infer_seniority(title)
    include, exclude = _get_include_exclude(icp, "seniority")

    # Exclude check
    if seniority in exclude:
        return 0.0
    for term in exclude:
        # Also check keyword-level (e.g., exclude "entry" matches "analyst")
        kws = SENIORITY_KEYWORDS.get(term, [])
        if any(kw in title.lower() for kw in kws):
            return 0.0

    if not include:
        return UNKNOWN_SCORE

    # Exact seniority level match
    if seniority in include:
        return 1.0

    # Adjacent match (e.g., ICP wants "director", prospect is "vp" → close)
    seniority_order = ["entry", "senior", "manager", "director", "vp", "cxo", "owner"]
    try:
        prospect_idx = seniority_order.index(seniority)
        best_distance = min(
            abs(prospect_idx - seniority_order.index(inc))
            for inc in include
            if inc in seniority_order
        )
        if best_distance == 1:
            return 0.7  # One level away
        if best_distance == 2:
            return 0.4  # Two levels away
    except ValueError:
        pass

    return 0.2


def _score_company_size(
    contact: dict[str, Any],
    icp: dict,
    campaign_icp_json: str | dict | None = None,
) -> float:
    """Score company size match against ICP headcount range (0.0-1.0)."""
    parsed_icp = None
    if isinstance(campaign_icp_json, str):
        try:
            parsed_icp = json.loads(campaign_icp_json)
        except (json.JSONDecodeError, TypeError):
            pass
    elif isinstance(campaign_icp_json, dict):
        parsed_icp = campaign_icp_json

    # Don't use ICP fallback for headcount — we're scoring against ICP, not filling gaps
    headcount = extract_headcount(contact, None)

    hc_range = icp.get("company_headcount", {})
    if not isinstance(hc_range, dict):
        return UNKNOWN_SCORE

    icp_min = hc_range.get("min") or 0
    icp_max = hc_range.get("max") or 0

    if not icp_min and not icp_max:
        return UNKNOWN_SCORE  # ICP doesn't specify headcount

    if headcount is None:
        return UNKNOWN_SCORE  # Can't determine headcount

    # Within range → perfect match
    effective_max = icp_max or (icp_min * 10)  # No max means open-ended
    if icp_min <= headcount <= effective_max:
        return 1.0

    # Within 2x range → partial match
    extended_min = max(1, icp_min // 2)
    extended_max = effective_max * 2
    if extended_min <= headcount <= extended_max:
        return 0.5

    # Way out of range
    return 0.1


def _score_location_match(contact: dict[str, Any], icp: dict) -> float:
    """Score location match against ICP locations (0.0-1.0)."""
    location = (contact.get("location") or "").lower().strip()
    if not location:
        # Try profile_json
        profile = parse_json_field(contact.get("profile_json"))
        if profile:
            location = (profile.get("location", "") or "").lower().strip()

    include, exclude = _get_include_exclude(icp, "locations")

    if not location:
        return LOCATION_UNKNOWN_SCORE

    # Exclude check
    for term in exclude:
        if term in location or location in term:
            return 0.0

    if not include:
        return LOCATION_UNKNOWN_SCORE

    # Match
    for term in include:
        if term in location or location in term:
            return 1.0

    return 0.2  # Has location but doesn't match


def _score_keyword_overlap(contact: dict[str, Any], icp: dict) -> float:
    """Score keyword overlap between contact text and ICP keywords (0.0-1.0)."""
    keywords = icp.get("keywords", [])
    if not keywords or not isinstance(keywords, list):
        return UNKNOWN_SCORE

    # Build searchable text from contact
    parts = [
        contact.get("title", ""),
        contact.get("company", ""),
        contact.get("headline", ""),  # Direct headline from search results
    ]
    profile = parse_json_field(contact.get("profile_json"))
    if profile:
        parts.append(profile.get("headline", "") or "")
        parts.append(profile.get("summary", "") or "")

    text = " ".join(p for p in parts if p).lower()
    if not text:
        return UNKNOWN_SCORE

    matches = sum(1 for kw in keywords if kw.lower() in text)
    if not matches:
        return 0.0

    return min(1.0, matches / max(len(keywords), 1))


# ──────────────────────────────────────────────
# Composite Score — Sub-Components
# ──────────────────────────────────────────────

def _get_signal_score(linkedin_id: str) -> float:
    """Look up composite signal score for a prospect."""
    if not linkedin_id:
        return 0.0

    try:
        from ..db.signal_queries import get_signal_account
        account = get_signal_account(linkedin_id)
        if account:
            return account.get("composite_score", 0.0) or 0.0
    except Exception:
        logger.debug("Could not look up signal score for %s", linkedin_id)
    return 0.0


def _compute_engagement_score(contact_id: str, linkedin_id: str) -> float:
    """Compute engagement score from behavioral history (0.0-1.0).

    Considers:
    - Profile views from prospect (from signals table)
    - Comments on our posts (from signals table)
    - Post reactions on our content (from signals table)
    - Our engagement with their content (from engagements table)

    Uses freshness decay and best-signal-as-baseline pattern.
    """
    if not contact_id and not linkedin_id:
        return 0.0

    now = int(time.time())
    scored_types: dict[str, float] = {}

    # Check signals table for prospect-initiated engagement
    if linkedin_id:
        try:
            from ..db.signal_queries import list_signals
            signals = list_signals(linkedin_id=linkedin_id, limit=20)
            for sig in signals:
                sig_type = sig.get("signal_type", "")
                detected_at = sig.get("detected_at", 0) or sig.get("created_at", 0) or 0

                # Apply freshness decay
                decay = _simple_freshness_decay(detected_at, now)

                # Score by signal type
                type_score = 0.0
                if sig_type == "profile_view":
                    type_score = 0.30 * decay
                elif sig_type == "commenter_match":
                    type_score = 0.30 * decay
                elif sig_type == "post_engagement":
                    type_score = 0.20 * decay

                if type_score > scored_types.get(sig_type, 0):
                    scored_types[sig_type] = type_score
        except Exception:
            logger.debug("Could not fetch signals for engagement score")

    # Check engagements table for our engagement with their content
    if contact_id:
        try:
            from ..db.schema import get_db
            db = get_db()
            rows = db.execute("""
                SELECT e.action_type, e.created_at
                FROM engagements e
                JOIN outreaches o ON e.outreach_id = o.id
                WHERE o.contact_id = ? AND e.status = 'sent'
                ORDER BY e.created_at DESC
                LIMIT 10
            """, (contact_id,)).fetchall()
            db.close()

            if rows:
                # Our engagement counts for a smaller amount (reciprocity signal)
                best_our_engagement = 0.0
                for row in rows:
                    detected_at = row["created_at"] or 0
                    decay = _simple_freshness_decay(detected_at, now)
                    best_our_engagement = max(best_our_engagement, 0.10 * decay)
                if best_our_engagement > scored_types.get("our_engagement", 0):
                    scored_types["our_engagement"] = best_our_engagement
        except Exception:
            logger.debug("Could not fetch engagements for engagement score")

    if not scored_types:
        return 0.0

    # Best-signal-as-baseline with diminishing stacking (same pattern as signal_scorer)
    sorted_scores = sorted(scored_types.values(), reverse=True)
    baseline = sorted_scores[0] / 0.30 * 0.80  # Normalize baseline to ~0.80
    baseline = min(baseline, 0.80)

    additional = sum(s * 0.5 for s in sorted_scores[1:])
    return min(1.0, round(baseline + additional, 4))


def _get_segment_performance_score(
    contact: dict[str, Any],
    patterns: list[dict[str, Any]] | None,
) -> float:
    """Score based on historical segment performance (0.0-1.0).

    Looks up matching patterns by title+company against strategy_patterns
    to find historical acceptance/conversion rates for similar prospects.
    """
    if not patterns:
        return 0.5  # Neutral on cold start

    title = (contact.get("title", "") or "").lower()
    company = (contact.get("company", "") or "").lower()

    if not title and not company:
        return 0.5

    best_score = 0.0
    for pattern in patterns:
        pattern_key = (pattern.get("pattern_key", "") or "").lower()
        if not pattern_key:
            continue

        # Check if contact matches pattern key (title+company format)
        parts = pattern_key.split("+")
        matched = any(
            (part.strip() in title or part.strip() in company)
            for part in parts
            if part.strip()
        )
        if not matched:
            continue

        # Score = acceptance_rate × confidence × sample_size_factor
        confidence = pattern.get("confidence", 0.5) or 0.5
        sample_size = pattern.get("sample_size", 0) or 0
        sample_factor = min(1.0, sample_size / 50)

        # Try to extract acceptance rate from details
        details = pattern.get("details_json")
        if isinstance(details, str):
            try:
                details = json.loads(details)
            except (json.JSONDecodeError, TypeError):
                details = {}
        elif not isinstance(details, dict):
            details = {}

        acceptance = details.get("acceptance_rate", 0) or 0
        if isinstance(acceptance, str):
            try:
                acceptance = float(acceptance.rstrip("%")) / 100
            except (ValueError, TypeError):
                acceptance = 0

        score = acceptance * confidence * sample_factor
        best_score = max(best_score, score)

    return best_score if best_score > 0 else 0.5


def _simple_freshness_decay(detected_at: int, now: int) -> float:
    """Simple freshness decay matching signal_scorer's curve."""
    if not detected_at:
        return 0.1

    age_days = max(0, (now - detected_at) / 86400)

    decay_curve = [
        (1, 1.0),
        (3, 0.85),
        (7, 0.65),
        (14, 0.40),
        (30, 0.20),
    ]

    for threshold_days, multiplier in decay_curve:
        if age_days <= threshold_days:
            return multiplier

    return 0.1
