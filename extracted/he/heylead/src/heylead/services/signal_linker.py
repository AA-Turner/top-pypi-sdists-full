"""Signal linker — retroactive matching of signals to campaigns and contacts.

Bridges two gaps in the signal pipeline:
1. When a new campaign is created, scan the existing signal pool for
   hot leads that match the campaign's ICP (signals that previously
   had no matching campaign).
2. Periodically re-evaluate "homeless" signals (action_taken =
   'no_matching_campaign') against all active campaigns — giving them
   a second chance when new campaigns appear.
3. Backfill orphan signals (prospect_id IS NULL) to contacts that
   now exist in the contacts table.

Entry points:
- scan_signal_pool_for_campaign()  — on campaign creation
- match_signals_to_campaigns()     — periodic scheduler job (hourly)
- backfill_orphan_signals()        — periodic scheduler job (every 2h)
"""

from __future__ import annotations

import json
import logging
import time
from typing import Any

logger = logging.getLogger(__name__)

# Maximum hot leads added per campaign creation (avoid flooding)
MAX_RETROACTIVE_LEADS = 20

# Maximum signals re-matched per periodic run
MAX_REMATCH_PER_RUN = 30

# Maximum orphan signals linked per backfill run
MAX_BACKFILL_PER_RUN = 200


# ──────────────────────────────────────────────
# 1. Scan signal pool on campaign creation
# ──────────────────────────────────────────────

def scan_signal_pool_for_campaign(
    campaign_id: str,
    icp_json: str | dict,
) -> dict[str, Any]:
    """Scan existing signals for hot leads matching a new campaign's ICP.

    Called during ``create_campaign`` after contacts are saved.
    Finds signals that were previously "homeless" (no matching campaign)
    or still awaiting activation, and whose content matches the ICP.

    Returns:
        {"hot_leads_found": int, "signals_matched": int, "details": list}
    """
    from ..db.queries import save_contact, create_outreach, get_contact_analysis, save_contact_analysis
    from ..db.signal_queries import (
        find_signals_matching_icp_text,
        get_contact_by_linkedin_id,
        update_signal,
        upsert_signal_account,
    )

    # Extract ICP keywords (reuse activator's logic)
    icp_keywords = _extract_icp_keywords_from_json(icp_json)
    if not icp_keywords:
        return {"hot_leads_found": 0, "signals_matched": 0, "details": []}

    # Find matching signals from the pool
    matching_signals = find_signals_matching_icp_text(
        icp_keywords,
        exclude_campaign_id=campaign_id,
        limit=MAX_RETROACTIVE_LEADS * 3,  # Fetch more, dedup below
    )

    if not matching_signals:
        return {"hot_leads_found": 0, "signals_matched": 0, "details": []}

    now = int(time.time())
    hot_leads_found = 0
    signals_matched = 0
    seen_linkedin_ids: set[str] = set()
    details: list[dict[str, str]] = []

    for sig in matching_signals:
        if hot_leads_found >= MAX_RETROACTIVE_LEADS:
            break

        linkedin_id = sig.get("linkedin_id") or ""
        if not linkedin_id:
            continue

        # Dedup: skip if we've already processed this person in this batch
        if linkedin_id in seen_linkedin_ids:
            continue
        seen_linkedin_ids.add(linkedin_id)

        # Dedup: skip if already a contact in THIS campaign
        existing = get_contact_by_linkedin_id(linkedin_id)
        if existing and existing.get("campaign_id") == campaign_id:
            continue

        # Build signal context for personalized messaging
        signal_context = _build_signal_context_safe(sig)

        # Create contact as a hot lead
        try:
            _sig_detail = f"{sig.get('signal_type', '?')}: {(sig.get('content') or '')[:60]}"
            contact_id = save_contact(
                campaign_id=campaign_id,
                name=sig.get("prospect_name") or "Unknown",
                title=sig.get("prospect_title") or "",
                company=_extract_company(sig),
                linkedin_url=f"https://www.linkedin.com/in/{linkedin_id}",
                linkedin_id=linkedin_id,
                fit_score=min((sig.get("signal_score") or 0.3) * 10, 10.0),
                source="signal_discovery",
                source_detail=_sig_detail,
            )

            # Inject signal context into analysis_json
            save_contact_analysis(contact_id, {
                "signal_context": signal_context,
                "summary": signal_context.get("engagement_hook", ""),
                "pain_points": signal_context.get("pain_points", []),
                "retroactive_match": True,
            })

            # Create outreach with signal reference
            signal_id = sig.get("id", "")
            create_outreach(
                campaign_id=campaign_id,
                contact_id=contact_id,
                status="pending",
                signal_id=signal_id,
            )

            # Update signal status
            update_signal(
                signal_id,
                status="actioned",
                action_taken="retroactive_campaign_match",
                campaign_id=campaign_id,
                prospect_id=contact_id,
                actioned_at=now,
            )

            # Update signal account aggregation
            upsert_signal_account(
                linkedin_id=linkedin_id,
                prospect_name=sig.get("prospect_name"),
                company=_extract_company(sig),
            )

            hot_leads_found += 1
            signals_matched += 1
            details.append({
                "name": sig.get("prospect_name") or "Unknown",
                "signal_type": sig.get("signal_type", ""),
                "intent": sig.get("intent", ""),
            })

            logger.info(
                "Retroactive signal match: %s (%s) → campaign %s",
                sig.get("prospect_name", "Unknown"),
                sig.get("signal_type", ""),
                campaign_id[:8],
            )

        except Exception as e:
            logger.debug("Failed to create retroactive hot lead: %s", e)
            continue

    if hot_leads_found > 0:
        logger.info(
            "Signal pool scan: found %d hot leads from %d signals for campaign %s",
            hot_leads_found, signals_matched, campaign_id[:8],
        )

    return {
        "hot_leads_found": hot_leads_found,
        "signals_matched": signals_matched,
        "details": details,
    }


# ──────────────────────────────────────────────
# 2. Periodic: re-match homeless signals to campaigns
# ──────────────────────────────────────────────

def match_signals_to_campaigns() -> str:
    """Re-evaluate homeless signals against all active campaigns.

    Runs periodically (every 1 hour) as a scheduler job.
    Picks up signals with action_taken='no_matching_campaign' that
    may now have a matching campaign (created after the signal was
    first processed).

    Returns summary string.
    """
    from ..db.queries import list_campaigns, save_contact, create_outreach, save_contact_analysis
    from ..db.signal_queries import (
        find_homeless_signals,
        get_contact_by_linkedin_id,
        update_signal,
        upsert_signal_account,
    )

    active_campaigns = list_campaigns(status="active")
    if not active_campaigns:
        return "No active campaigns."

    homeless = find_homeless_signals(limit=MAX_REMATCH_PER_RUN * 2)
    if not homeless:
        return "No homeless signals to re-match."

    now = int(time.time())
    matched = 0
    skipped = 0

    for sig in homeless:
        if matched >= MAX_REMATCH_PER_RUN:
            break

        linkedin_id = sig.get("linkedin_id") or ""
        if not linkedin_id:
            skipped += 1
            continue

        # Check if already a contact somewhere
        existing = get_contact_by_linkedin_id(linkedin_id)
        if existing:
            # Already in a campaign — just link the signal
            update_signal(
                sig["id"],
                action_taken="retroactive_linked_existing",
                prospect_id=existing["id"],
                campaign_id=existing.get("campaign_id"),
                actioned_at=now,
            )
            skipped += 1
            continue

        # Try to match to a campaign via ICP overlap
        campaign_id = _match_best_campaign(sig, active_campaigns)
        if not campaign_id:
            continue  # Still no match — leave as-is for next cycle

        # Build signal context
        signal_context = _build_signal_context_safe(sig)

        try:
            _sig_detail = f"{sig.get('signal_type', '?')}: {(sig.get('content') or '')[:60]}"
            contact_id = save_contact(
                campaign_id=campaign_id,
                name=sig.get("prospect_name") or "Unknown",
                title=sig.get("prospect_title") or "",
                company=_extract_company(sig),
                linkedin_url=f"https://www.linkedin.com/in/{linkedin_id}",
                linkedin_id=linkedin_id,
                fit_score=min((sig.get("signal_score") or 0.3) * 10, 10.0),
                source="signal_discovery",
                source_detail=_sig_detail,
            )

            # Inject signal context
            save_contact_analysis(contact_id, {
                "signal_context": signal_context,
                "summary": signal_context.get("engagement_hook", ""),
                "pain_points": signal_context.get("pain_points", []),
                "retroactive_match": True,
            })

            create_outreach(
                campaign_id=campaign_id,
                contact_id=contact_id,
                status="pending",
                signal_id=sig["id"],
            )

            update_signal(
                sig["id"],
                status="actioned",
                action_taken="retroactive_campaign_match",
                campaign_id=campaign_id,
                prospect_id=contact_id,
                actioned_at=now,
            )

            upsert_signal_account(
                linkedin_id=linkedin_id,
                prospect_name=sig.get("prospect_name"),
                company=_extract_company(sig),
            )

            matched += 1
            logger.info(
                "Signal rematch: %s (%s) → campaign %s",
                sig.get("prospect_name", "Unknown"),
                sig.get("signal_type", ""),
                campaign_id[:8],
            )

        except Exception as e:
            logger.debug("Signal rematch failed: %s", e)
            continue

    summary = f"Signal rematch: {matched} matched, {skipped} skipped"
    if matched > 0:
        logger.info(summary)
    return summary


# ──────────────────────────────────────────────
# 3. Periodic: backfill orphan signals to contacts
# ──────────────────────────────────────────────

def backfill_orphan_signals() -> str:
    """Link orphan signals (prospect_id IS NULL) to now-known contacts.

    Catches signals detected before the contact existed. Links them
    and boosts the contact's fit_score with signal intelligence.

    Returns summary string.
    """
    from ..db.signal_queries import (
        find_orphan_signals_with_contacts,
        bulk_link_signals_to_contact,
        get_signal,
        upsert_signal_account,
    )

    matches = find_orphan_signals_with_contacts(limit=MAX_BACKFILL_PER_RUN)
    if not matches:
        return "No orphan signals to backfill."

    # Group by contact for efficient processing
    by_contact: dict[str, list[dict]] = {}
    for m in matches:
        cid = m["contact_id"]
        by_contact.setdefault(cid, []).append(m)

    total_linked = 0
    contacts_boosted = 0

    for contact_id, signal_matches in by_contact.items():
        campaign_id = signal_matches[0]["contact_campaign_id"]
        signal_ids = [s["signal_id"] for s in signal_matches]

        count = bulk_link_signals_to_contact(signal_ids, contact_id, campaign_id)
        total_linked += count

        if count > 0:
            # Boost contact with signal intelligence
            try:
                full_signals = []
                for sid in signal_ids[:5]:  # Cap to avoid over-fetching
                    sig = get_signal(sid)
                    if sig:
                        full_signals.append(sig)

                if full_signals:
                    _boost_contact_with_signals(contact_id, full_signals)
                    contacts_boosted += 1

                # Update signal account aggregation
                linkedin_id = signal_matches[0].get("linkedin_id", "")
                if linkedin_id:
                    upsert_signal_account(linkedin_id=linkedin_id)
            except Exception as e:
                logger.debug("Backfill boost failed for contact %s: %s", contact_id[:8], e)

    summary = f"Backfill: linked {total_linked} orphan signals to {contacts_boosted} contacts"
    if total_linked > 0:
        logger.info(summary)
    return summary


# ──────────────────────────────────────────────
# 4. Analyze watchlist coverage for campaign ICP
# ──────────────────────────────────────────────

def analyze_signal_coverage(icp_json: str | dict) -> dict[str, Any]:
    """Analyze how well existing watchlists cover a campaign's ICP topics.

    Returns:
        {
            "already_covered": int,  # ICP keywords already in active watchlists
            "new_topics": int,       # ICP keywords NOT yet tracked
            "total_icp_keywords": int,
            "coverage_pct": float,
            "watchlists_relevant": int,  # existing watchlists with overlap
        }
    """
    from ..db.signal_queries import list_watchlists

    icp_keywords = _extract_icp_keywords_from_json(icp_json)
    if not icp_keywords:
        return {
            "already_covered": 0,
            "new_topics": 0,
            "total_icp_keywords": 0,
            "coverage_pct": 0.0,
            "watchlists_relevant": 0,
        }

    # Gather all existing watchlist keywords
    existing_keywords: set[str] = set()
    watchlists = list_watchlists(is_active=True)
    relevant_count = 0
    for wl in watchlists:
        wl_keywords = {k.lower().strip() for k in wl.get("keywords_list", [])}
        overlap = icp_keywords & wl_keywords
        if overlap:
            relevant_count += 1
        existing_keywords |= wl_keywords

    covered = icp_keywords & existing_keywords
    new = icp_keywords - existing_keywords

    return {
        "already_covered": len(covered),
        "new_topics": len(new),
        "total_icp_keywords": len(icp_keywords),
        "coverage_pct": len(covered) / len(icp_keywords) if icp_keywords else 0.0,
        "watchlists_relevant": relevant_count,
    }


# ──────────────────────────────────────────────
# Helpers (shared utilities)
# ──────────────────────────────────────────────

def _extract_icp_keywords_from_json(icp_json: str | dict) -> set[str]:
    """Extract searchable keywords from ICP JSON (reuses activator's logic)."""
    if isinstance(icp_json, str):
        try:
            parsed = json.loads(icp_json)
        except (json.JSONDecodeError, TypeError):
            return set()
    else:
        parsed = icp_json

    keywords: set[str] = set()

    # Handle nested ICP structure
    if isinstance(parsed, dict):
        icps_list = parsed.get("icps", [parsed])
    elif isinstance(parsed, list):
        icps_list = parsed
    else:
        return set()

    for icp in icps_list:
        if not isinstance(icp, dict):
            continue
        _extract_icp_keywords(icp, keywords)

    return keywords


def _extract_icp_keywords(icp_data: dict[str, Any], keywords: set[str]) -> None:
    """Extract searchable keywords from an ICP persona dict.

    Mirrors ``_extract_icp_keywords`` from ``signal_activator.py``.
    """
    # Pain points
    for pp in icp_data.get("pain_points", []):
        if isinstance(pp, str):
            keywords.add(pp.lower())
        elif isinstance(pp, dict):
            keywords.add((pp.get("pain", "") or pp.get("description", "")).lower())

    # Keywords
    for kw in icp_data.get("keywords", []):
        if isinstance(kw, str):
            keywords.add(kw.lower())

    # Industries (handle both list[str] and LinkedinSearchParam dict)
    industries = icp_data.get("industries", [])
    if isinstance(industries, dict):
        industries = industries.get("include", [])
    for ind in industries:
        if isinstance(ind, str):
            keywords.add(ind.lower())

    # Job titles (handle both list[str] and LinkedinSearchParam dict)
    job_titles = icp_data.get("job_titles", [])
    if isinstance(job_titles, dict):
        job_titles = job_titles.get("include", [])
    for jt in job_titles:
        if isinstance(jt, str):
            keywords.add(jt.lower())

    # Target description
    target = icp_data.get("target_description", "") or icp_data.get("name", "")
    if target:
        for word in target.lower().split():
            if len(word) > 4:  # Skip short words
                keywords.add(word)

    # Remove empty strings
    keywords.discard("")


def _match_best_campaign(
    signal: dict[str, Any],
    campaigns: list[dict[str, Any]],
) -> str | None:
    """Find the best-matching campaign via ICP overlap.

    Mirrors ``_match_best_campaign`` from ``signal_activator.py``
    to avoid circular imports.
    """
    from ..constants import SIGNAL_ICP_MIN_OVERLAP

    if not campaigns:
        return None

    content = (signal.get("content") or "").lower()
    prospect_title = (signal.get("prospect_title") or "").lower()
    meta_raw = signal.get("metadata_json") or ""
    try:
        meta = json.loads(meta_raw) if meta_raw else {}
    except (json.JSONDecodeError, TypeError):
        meta = {}
    keyword = (meta.get("keyword") or "").lower()
    match_text = f"{content} {prospect_title} {keyword}"

    best_campaign_id = None
    best_overlap = 0.0

    for camp in campaigns:
        icp_raw = camp.get("icp_json", "")
        if not icp_raw:
            continue

        try:
            icp_data = json.loads(icp_raw) if isinstance(icp_raw, str) else icp_raw
        except (json.JSONDecodeError, TypeError):
            continue

        icp_keywords: set[str] = set()
        if isinstance(icp_data, dict):
            icps_list = icp_data.get("icps", [icp_data])
        elif isinstance(icp_data, list):
            icps_list = icp_data
        else:
            continue

        for persona in icps_list:
            if isinstance(persona, dict):
                _extract_icp_keywords(persona, icp_keywords)

        if not icp_keywords:
            continue

        matched = sum(1 for kw in icp_keywords if kw in match_text)
        overlap = matched / len(icp_keywords) if icp_keywords else 0

        if overlap > best_overlap:
            best_overlap = overlap
            best_campaign_id = camp["id"]

    if best_campaign_id and best_overlap >= SIGNAL_ICP_MIN_OVERLAP:
        return best_campaign_id

    return None


def _build_signal_context_safe(signal: dict[str, Any]) -> dict[str, Any]:
    """Build signal context dict for message personalization.

    Tries to use the activator's ``_build_signal_context`` but
    falls back to a simple dict if that fails (avoids circular imports).
    """
    try:
        from ..services.signal_activator import _build_signal_context
        return _build_signal_context(signal)
    except Exception:
        return {
            "signal_type": signal.get("signal_type", "unknown"),
            "intent": signal.get("intent", "unknown"),
            "confidence": signal.get("confidence", 0.0),
            "engagement_hook": "",
            "pain_points": [],
            "keywords_matched": [],
        }


def _boost_contact_with_signals(
    contact_id: str,
    signals: list[dict[str, Any]],
) -> None:
    """Boost a contact's fit_score and inject signal context.

    Mirrors ``_boost_existing_contact`` from ``signal_activator.py``.
    """
    from ..db.queries import get_contact_analysis, save_contact_analysis, update_contact
    from ..services.signal_scorer import compute_signal_score

    if not signals:
        return

    now = int(time.time())

    # Compute best signal score
    best_score = max(compute_signal_score(s, now) for s in signals)

    # Boost fit_score
    try:
        from ..db.schema import get_db
        db = get_db()
        row = db.execute("SELECT fit_score FROM contacts WHERE id = ?", (contact_id,)).fetchone()
        db.close()
        current_fit = (row["fit_score"] if row else 0) or 0
        boosted = min(current_fit + best_score * 2, 10.0)
        if boosted > current_fit:
            update_contact(contact_id, fit_score=boosted)
    except Exception as e:
        logger.debug("Fit score boost failed: %s", e)

    # Inject signal context into analysis_json
    try:
        best_signal = max(signals, key=lambda s: compute_signal_score(s, now))
        signal_context = _build_signal_context_safe(best_signal)

        existing_analysis = get_contact_analysis(contact_id) or {}
        existing_analysis["signal_context"] = signal_context
        existing_analysis["retroactive_match"] = True
        existing_analysis["matched_signals_count"] = len(signals)

        # Merge pain points
        new_pains = signal_context.get("pain_points", [])
        if new_pains:
            existing_pains = existing_analysis.get("pain_points", [])
            merged = list(set(existing_pains) | set(new_pains))
            existing_analysis["pain_points"] = merged[:5]

        save_contact_analysis(contact_id, existing_analysis)
    except Exception as e:
        logger.debug("Signal context injection failed: %s", e)


def _extract_company(signal: dict[str, Any]) -> str:
    """Extract company name from signal metadata or content."""
    meta_raw = signal.get("metadata_json") or ""
    try:
        meta = json.loads(meta_raw) if meta_raw else {}
    except (json.JSONDecodeError, TypeError):
        meta = {}

    company = meta.get("new_company") or meta.get("company") or ""
    if not company:
        title = signal.get("prospect_title") or ""
        if " at " in title:
            company = title.rsplit(" at ", 1)[1]
    return company
