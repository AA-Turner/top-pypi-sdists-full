"""Collector: profile_view_collector — Detect who viewed your LinkedIn profile.

Polls get_profile_viewers() (requires LinkedIn Premium or Sales Navigator),
cross-references viewers against campaign contacts, and saves as
SIGNAL_PROFILE_VIEW signals.

Phase 4 enhancements:
- ICP matching for viewers (checks title/company against active ICPs)
- Higher confidence scores for ICP-matching viewers
- Enriched metadata (is_icp_match, fit_score, viewer_seniority)
"""

from __future__ import annotations

import json
import logging
import time
from typing import Any

from ..constants import (
    SIGNAL_PROFILE_VIEW,
    SIGNAL_TTL_PROFILE_VIEW,
)
from ..db.async_bridge import run_db
from ..db.queries import get_setting
from ..db.signal_queries import (
    get_contact_by_linkedin_id,
    save_signal,
    signal_exists,
    upsert_signal_account,
)

logger = logging.getLogger(__name__)


async def collect_profile_views() -> str:
    """Collect profile view signals from LinkedIn.

    Flow:
    1. Call get_profile_viewers() to get recent viewers
    2. For each viewer, extract name/title/company/url
    3. Try to resolve linkedin_id from URL
    4. Cross-reference against campaign contacts
    5. Save as SIGNAL_PROFILE_VIEW signals
    6. Update signal_accounts aggregation

    Returns:
        Summary string of results.
    """
    from ..linkedin import get_account_id, get_linkedin_client

    account_id = get_account_id()
    if not account_id:
        return "No LinkedIn account connected — skipping profile view collection."

    client = get_linkedin_client()
    total_signals = 0
    icp_matches = 0
    errors = 0

    try:
        viewers = await client.get_profile_viewers(account_id)

        if not viewers:
            # Check if Voyager is broken vs no viewers
            try:
                from ..linkedin.backend_client import BackendClient

                if isinstance(client, BackendClient) and hasattr(client, "is_voyager_available"):
                    voyager_ok = await client.is_voyager_available()
                    if not voyager_ok:
                        return (
                            "Profile viewer tracking unavailable — LinkedIn Voyager API "
                            "returning errors (may need account reconnection via Unipile)."
                        )
            except Exception:
                pass
            return "No profile viewers found (requires LinkedIn Premium)."

        now = int(time.time())

        for viewer in viewers:
            viewer_name = viewer.get("name", "")
            viewer_title = viewer.get("title", "")
            viewer_company = viewer.get("company", "")
            viewer_url = viewer.get("url", "")

            if not viewer_name:
                continue

            # Try to extract linkedin_id from URL or other fields
            linkedin_id = _extract_linkedin_id(viewer_url, viewer)

            # Deduplicate: check if we already have a profile_view signal
            # for this person within the TTL window
            if linkedin_id:
                if await run_db(
                    signal_exists,
                    SIGNAL_PROFILE_VIEW,
                    linkedin_id=linkedin_id,
                    lookback_seconds=SIGNAL_TTL_PROFILE_VIEW,
                ):
                    continue
            elif viewer_name:
                # Fallback dedup by name (less reliable)
                if await run_db(
                    signal_exists,
                    SIGNAL_PROFILE_VIEW,
                    linkedin_id=viewer_name,  # Use name as pseudo-ID
                    lookback_seconds=SIGNAL_TTL_PROFILE_VIEW,
                ):
                    continue

            # Cross-reference against campaign contacts
            contact = None
            campaign_id = None
            prospect_id = None

            if linkedin_id:
                contact = await run_db(get_contact_by_linkedin_id, linkedin_id)
                if contact:
                    campaign_id = contact.get("campaign_id")
                    prospect_id = contact.get("id")

            # Phase 4: ICP matching — check viewer against active campaign ICPs
            icp_result = await run_db(_check_icp_match, viewer_title, viewer_company)
            is_icp_match = icp_result.get("is_match", False)
            fit_score = icp_result.get("fit_score", 0.0)
            viewer_seniority = _infer_seniority(viewer_title)

            # Higher confidence for ICP-matching viewers
            confidence = 0.7 if is_icp_match else (0.5 if contact else 0.3)

            try:
                expires_at = now + SIGNAL_TTL_PROFILE_VIEW

                # Resolve campaign_id — use None (not empty string) for FK safety
                resolved_campaign_id = (
                    campaign_id
                    or icp_result.get("campaign_id")
                    or None
                )

                await run_db(
                    save_signal,
                    signal_type=SIGNAL_PROFILE_VIEW,
                    source="profile_viewers",
                    prospect_id=prospect_id or None,
                    prospect_name=viewer_name,
                    prospect_title=viewer_title,
                    linkedin_id=linkedin_id or viewer_name,
                    campaign_id=resolved_campaign_id,
                    content="Viewed your LinkedIn profile",
                    confidence=confidence,
                    metadata_json=json.dumps({
                        "viewer_company": viewer_company,
                        "viewer_url": viewer_url,
                        "is_campaign_contact": contact is not None,
                        "relation": viewer.get("relation", ""),
                        "is_icp_match": is_icp_match,
                        "fit_score": fit_score,
                        "viewer_seniority": viewer_seniority,
                        "matched_icp_campaign": icp_result.get("campaign_id", ""),
                    }),
                    expires_at=expires_at,
                )
                total_signals += 1
                if is_icp_match:
                    icp_matches += 1

                # Update signal account aggregation
                if linkedin_id:
                    await run_db(
                        upsert_signal_account,
                        linkedin_id=linkedin_id,
                        prospect_name=viewer_name,
                        company=viewer_company,
                    )

                if contact:
                    logger.info(
                        "Profile viewer cross-reference: %s is campaign contact (campaign=%s)",
                        viewer_name, campaign_id[:8] if campaign_id else "?",
                    )
                if is_icp_match:
                    logger.info(
                        "Profile viewer ICP match: %s (%s at %s) — fit=%.2f",
                        viewer_name, viewer_title, viewer_company, fit_score,
                    )

            except Exception as e:
                logger.warning("Error saving profile view signal for %s: %s", viewer_name, e)
                errors += 1

    except Exception as e:
        logger.warning("Profile view collection failed: %s", e)
        return f"Profile view collection failed: {e}"
    finally:
        await client.close()

    summary = f"Profile view collection: {total_signals} new signals from {len(viewers)} viewers"
    if icp_matches:
        summary += f", {icp_matches} ICP matches"
    if errors:
        summary += f", {errors} errors"
    logger.info(summary)
    return summary


def _extract_linkedin_id(url: str, viewer: dict[str, Any]) -> str:
    """Try to extract a LinkedIn provider_id or public_id from a viewer.

    Args:
        url: The viewer's LinkedIn profile URL.
        viewer: Full viewer dict from get_profile_viewers().

    Returns:
        LinkedIn ID string, or empty string if not extractable.
    """
    # Check for direct provider_id field
    provider_id = viewer.get("provider_id", "") or viewer.get("linkedin_id", "")
    if provider_id:
        return str(provider_id)

    # Try to extract from URL
    if not url:
        return ""

    # URLs like https://www.linkedin.com/in/johndoe or /in/johndoe/
    import re

    match = re.search(r"linkedin\.com/in/([^/?#]+)", url)
    if match:
        return match.group(1).strip("/")

    # URLs with member ID: /profile/view?id=12345
    match = re.search(r"[?&]id=(\d+)", url)
    if match:
        return match.group(1)

    return ""


def _check_icp_match(title: str, company: str) -> dict[str, Any]:
    """Check if a viewer matches any active campaign ICP.

    Performs a lightweight keyword overlap check against ICP data
    stored in active campaigns. No LLM call — pure heuristic.

    Returns:
        Dict with is_match, fit_score, campaign_id.
    """
    from ..db.queries import list_campaigns

    result: dict[str, Any] = {"is_match": False, "fit_score": 0.0, "campaign_id": ""}

    if not title and not company:
        return result

    title_lower = (title or "").lower()
    company_lower = (company or "").lower()

    try:
        campaigns = list_campaigns(status="active")
    except Exception:
        return result

    best_score = 0.0
    best_campaign_id = ""

    for campaign in campaigns:
        icp_json = campaign.get("icp_json") or campaign.get("icp_data") or ""
        if not icp_json:
            continue

        try:
            if isinstance(icp_json, str):
                icp = json.loads(icp_json)
            else:
                icp = icp_json
        except (json.JSONDecodeError, TypeError):
            continue

        # Extract ICP keywords: titles, industries, company attributes
        icp_titles = _extract_icp_keywords(icp, "titles")
        icp_industries = _extract_icp_keywords(icp, "industries")
        icp_companies = _extract_icp_keywords(icp, "companies")

        score = 0.0

        # Title match (strongest signal)
        for kw in icp_titles:
            if kw in title_lower:
                score += 0.4
                break

        # Industry/company match
        for kw in icp_industries:
            if kw in title_lower or kw in company_lower:
                score += 0.2
                break

        for kw in icp_companies:
            if kw in company_lower:
                score += 0.3
                break

        # Seniority bonus
        seniority = _infer_seniority(title)
        if seniority in ("c_level", "vp"):
            score += 0.1

        score = min(score, 1.0)

        if score > best_score:
            best_score = score
            best_campaign_id = campaign.get("id", "")

    if best_score >= 0.3:
        result["is_match"] = True
        result["fit_score"] = round(best_score, 2)
        result["campaign_id"] = best_campaign_id

    return result


def _extract_icp_keywords(icp: dict | list, category: str) -> list[str]:
    """Extract keyword list from ICP data for matching.

    Handles various ICP formats (flat dict, personas list, etc.).
    """
    keywords: list[str] = []

    # ICP may be a list of personas or a single dict
    if isinstance(icp, list):
        for persona in icp:
            keywords.extend(_extract_icp_keywords(persona, category))
        return list(set(keywords))

    if not isinstance(icp, dict):
        return keywords

    if category == "titles":
        # Look for job title fields
        for key in ("target_titles", "job_titles", "titles", "seniority_levels", "roles"):
            val = icp.get(key, [])
            if isinstance(val, list):
                keywords.extend(str(v).lower() for v in val)
            elif isinstance(val, str):
                keywords.append(val.lower())

    elif category == "industries":
        for key in ("industries", "industry", "verticals", "sectors"):
            val = icp.get(key, [])
            if isinstance(val, list):
                keywords.extend(str(v).lower() for v in val)
            elif isinstance(val, str):
                keywords.append(val.lower())

    elif category == "companies":
        for key in ("companies", "company_names", "target_companies"):
            val = icp.get(key, [])
            if isinstance(val, list):
                keywords.extend(str(v).lower() for v in val)
            elif isinstance(val, str):
                keywords.append(val.lower())

    # Also check nested "personas" key
    personas = icp.get("personas", [])
    if isinstance(personas, list):
        for p in personas:
            keywords.extend(_extract_icp_keywords(p, category))

    return list(set(keywords))


def _infer_seniority(title: str) -> str:
    """Infer seniority level from a job title.

    Returns one of: c_level, vp, director, manager, individual, unknown.
    Uses word-boundary matching to avoid false positives (e.g. "director" ≠ "cto").
    """
    import re

    if not title:
        return "unknown"
    lower = title.lower()

    # Order matters: check most senior first
    # Use word boundaries (\b) to avoid substring false positives
    if re.search(r"\b(ceo|cto|cfo|coo|cmo|cio|cpo|chief)\b", lower):
        return "c_level"
    if re.search(r"\b(vp|vice president|svp|evp)\b", lower):
        return "vp"
    if re.search(r"\b(director|head of)\b", lower):
        return "director"
    if re.search(r"\b(manager|team lead)\b", lower) or lower.endswith(" lead"):
        return "manager"
    if re.search(r"\b(engineer|developer|analyst|specialist|associate|consultant)\b", lower):
        return "individual"

    return "unknown"
