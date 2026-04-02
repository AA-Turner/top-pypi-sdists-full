"""Deduplication service — prevent outreach to existing connections and cross-campaign duplicates.

Before adding prospects to a campaign, checks against:
1. Company/business profiles (LinkedIn Pages masquerading as people)
2. Existing 1st-degree LinkedIn connections (via Unipile relations API)
3. All contacts across all campaigns in the local DB
4. Optional exclusion list (LinkedIn URLs / public_ids)

This solves the #2 complaint across all AI SDRs: "AI contacted our existing clients."
"""

from __future__ import annotations

import logging
import re
from typing import Any

from ..db.schema import get_db

logger = logging.getLogger(__name__)


# ── Company / Business Profile Detection ──

# Common business suffixes and keywords (case-insensitive)
_COMPANY_SUFFIXES = re.compile(
    r"\b(?:Inc|LLC|Ltd|GmbH|Corp|Co|AG|SA|SRL|BV|PLC|LP|LLP|"
    r"Pty|Pvt|OÜ|SAS|SARL|KG|AB|AS|ApS|Oy|NV|SE)\b\.?$",
    re.IGNORECASE,
)

_COMPANY_KEYWORDS = re.compile(
    r"\b(?:Solutions|Technologies|Consulting|Services|Agency|Studios?|"
    r"Labs?|Digital|Media|Group|Partners|Ventures|Capital|Holdings|"
    r"Enterprises|Systems|Networks|Software|Platform|Innovations|"
    r"Analytics|Dynamics|Automations?|Intelligence)\b",
    re.IGNORECASE,
)

# Broader patterns for names that are clearly not personal names.
# Two+ word names ending in a company keyword (e.g., "Prodigy AI Solutions")
_COMPANY_NAME_ENDING = re.compile(
    r"(?:Solutions|Technologies|Consulting|Services|Agency|Studios?|"
    r"Labs?|Digital|Media|Group|Partners|Ventures|Capital|Holdings|"
    r"Enterprises|Systems|Networks|Software|Platform|Innovations|"
    r"Analytics|Dynamics|Automations?|Intelligence)$",
    re.IGNORECASE,
)

# Numeric-only public_id is a strong signal for company pages
_NUMERIC_ONLY = re.compile(r"^\d+$")


def is_company_profile(prospect: dict) -> bool:
    """Detect if a prospect dict looks like a company/business page, not a person.

    Uses multiple heuristics:
    1. LinkedIn URL contains /company/ instead of /in/
    2. Name ends with a business suffix (Inc, LLC, Ltd, etc.)
    3. Name ends with a business keyword (Solutions, Technologies, etc.)
    4. Numeric-only public_id combined with a non-personal-looking name

    Returns True if this is likely a company profile that should be skipped.
    """
    name = (prospect.get("name") or "").strip()
    if not name:
        return False

    # Signal 1: URL path contains /company/
    url = (prospect.get("linkedin_url") or prospect.get("profile_url") or "").lower()
    if "/company/" in url:
        return True

    # Signal 2: Name ends with a business suffix (Inc, LLC, Ltd, etc.)
    if _COMPANY_SUFFIXES.search(name):
        logger.debug("Company profile detected (suffix): %s", name)
        return True

    # Signal 3: Name ends with a business keyword (Solutions, Consulting, Agency, etc.)
    # This catches "Prodigy AI Solutions", "Growth Agency", "Apex Consulting"
    # False positive risk is near-zero — real people don't have last names like "Solutions"
    words = name.split()
    if len(words) >= 2 and _COMPANY_NAME_ENDING.search(words[-1]):
        logger.debug("Company profile detected (name ends with business keyword): %s", name)
        return True

    # Signal 4: Single-word name that's a common business term
    if len(words) == 1 and _COMPANY_KEYWORDS.search(name):
        logger.debug("Company profile detected (single business word): %s", name)
        return True

    # Signal 5: Numeric-only public_id + name doesn't look like a person
    # Real people have slug IDs like "john-doe-123"; company pages often have numeric-only IDs
    pub_id = (prospect.get("public_id") or "").strip()
    if pub_id and _NUMERIC_ONLY.match(pub_id):
        # Numeric ID alone isn't enough (some real people have them)
        # But combined with a name that has no lowercase words (suggesting business name)
        # or contains any company keyword anywhere, flag it
        if _COMPANY_KEYWORDS.search(name):
            logger.debug("Company profile detected (numeric ID + keyword): %s", name)
            return True

    return False


def get_all_known_linkedin_ids() -> set[str]:
    """Collect all linkedin_id and public_id values from the global contact base.

    Queries global_contacts (one row per person) for faster dedup than scanning
    all campaign contacts. Falls back to the contacts table if global_contacts
    doesn't exist yet (pre-migration).

    Returns a set of lowercase identifiers (public_ids + linkedin_ids + urls)
    that we have already contacted across all campaigns.
    """
    db = get_db()

    # Try global_contacts first (fast path — one row per person)
    try:
        rows = db.execute(
            """SELECT linkedin_id FROM global_contacts
               WHERE linkedin_id IS NOT NULL AND linkedin_id != ''
               UNION
               SELECT linkedin_url FROM global_contacts
               WHERE linkedin_url IS NOT NULL AND linkedin_url != ''
               UNION
               SELECT json_extract(profile_json, '$.provider_id') FROM global_contacts
               WHERE profile_json IS NOT NULL AND profile_json != ''
                 AND json_valid(profile_json)
                 AND json_extract(profile_json, '$.provider_id') IS NOT NULL
                 AND json_extract(profile_json, '$.provider_id') != ''"""
        ).fetchall()
    except Exception:
        # Fallback: old behavior (pre-migration, global_contacts doesn't exist)
        rows = db.execute(
            """SELECT DISTINCT linkedin_id FROM contacts
               WHERE linkedin_id IS NOT NULL AND linkedin_id != ''
               UNION
               SELECT DISTINCT linkedin_url FROM contacts
               WHERE linkedin_url IS NOT NULL AND linkedin_url != ''
               UNION
               SELECT DISTINCT json_extract(profile_json, '$.provider_id') FROM contacts
               WHERE profile_json IS NOT NULL AND profile_json != ''
                 AND json_valid(profile_json)
                 AND json_extract(profile_json, '$.provider_id') IS NOT NULL
                 AND json_extract(profile_json, '$.provider_id') != ''"""
        ).fetchall()

    db.close()

    ids: set[str] = set()
    for row in rows:
        val = row[0]
        if val:
            ids.add(val.lower().strip())
    return ids


async def fetch_connection_ids(
    client: Any,
    account_id: str,
    max_pages: int = 20,
) -> set[str]:
    """Fetch 1st-degree connection identifiers, using local cache when possible.

    Uses the local connections table (auto-syncs if stale >1h).
    Falls back to the Unipile relations API if local DB is empty.
    Returns a set of provider_id and public_id values (lowercased).
    """
    try:
        from .connection_sync import ensure_synced
        return await ensure_synced(client, account_id)
    except Exception as e:
        logger.warning("Local connection sync failed, falling back to API: %s", e)

    # Fallback: direct API call (old behavior)
    all_ids: set[str] = set()
    try:
        relations = await client.get_relations(account_id, limit=100)
        for rel in relations:
            pid = rel.get("provider_id", "")
            pub = rel.get("public_id", "")
            if pid:
                all_ids.add(pid.lower().strip())
            if pub:
                all_ids.add(pub.lower().strip())
                all_ids.add(f"https://www.linkedin.com/in/{pub.lower().strip()}")
    except Exception as e:
        logger.warning("Failed to fetch connections for dedup: %s", e)

    return all_ids


def get_excluded_linkedin_ids() -> set[str]:
    """Get LinkedIn identifiers for contacts excluded from automation.

    Returns identifiers for contacts with 'do-not-automate' tag or
    'do_not_contact' lifecycle stage.
    """
    db = get_db()
    ids: set[str] = set()
    try:
        rows = db.execute(
            """SELECT linkedin_id, linkedin_url
               FROM global_contacts
               WHERE lifecycle_stage = 'do_not_contact'
                  OR tags_json LIKE '%"do-not-automate"%'""",
        ).fetchall()
        for row in rows:
            lid = (row["linkedin_id"] or "").lower().strip()
            url = (row["linkedin_url"] or "").lower().strip()
            if lid:
                ids.add(lid)
            if url:
                ids.add(url)
    except Exception as e:
        logger.warning("Failed to fetch excluded IDs: %s", e)
    finally:
        db.close()
    return ids


def dedup_prospects(
    prospects: list[dict],
    known_ids: set[str],
    connection_ids: set[str],
    exclusion_ids: set[str] | None = None,
) -> tuple[list[dict], dict[str, int]]:
    """Filter out duplicate and already-known prospects.

    Args:
        prospects: List of prospect dicts from LinkedIn search.
        known_ids: Identifiers already in our contacts DB.
        connection_ids: 1st-degree LinkedIn connection identifiers.
        exclusion_ids: Optional set of manually excluded identifiers.

    Returns:
        (filtered_prospects, stats) where stats has counts for each filter reason.
    """
    exclusion = exclusion_ids or set()
    stats = {
        "total_before": len(prospects),
        "company_profile": 0,
        "existing_connection": 0,
        "cross_campaign_duplicate": 0,
        "exclusion_list": 0,
        "passed": 0,
    }

    filtered: list[dict] = []

    for prospect in prospects:
        # Check 0: company/business profile (not a real person)
        if is_company_profile(prospect):
            stats["company_profile"] += 1
            continue

        pub_id = (prospect.get("public_id") or "").lower().strip()
        prov_id = (prospect.get("provider_id") or "").lower().strip()
        url = (prospect.get("linkedin_url") or "").lower().strip()

        identifiers = {x for x in (pub_id, prov_id, url) if x}
        if pub_id:
            identifiers.add(f"https://www.linkedin.com/in/{pub_id}")

        # Check 1: existing connection
        if identifiers & connection_ids:
            stats["existing_connection"] += 1
            continue

        # Check 2: cross-campaign duplicate
        if identifiers & known_ids:
            stats["cross_campaign_duplicate"] += 1
            continue

        # Check 3: exclusion list
        if identifiers & exclusion:
            stats["exclusion_list"] += 1
            continue

        stats["passed"] += 1
        filtered.append(prospect)

    return filtered, stats


def filter_to_connections_only(
    prospects: list[dict],
    connection_ids: set[str],
    known_ids: set[str] | None = None,
) -> tuple[list[dict], dict[str, int]]:
    """Keep ONLY existing connections (inverse of dedup_prospects).

    For DM-only / connections-only campaigns: include only 1st-degree
    connections. Optionally removes cross-campaign duplicates via *known_ids*.

    Returns:
        (filtered_prospects, stats) with counts.
    """
    known = known_ids or set()
    stats = {
        "total_before": len(prospects),
        "company_profile": 0,
        "connected": 0,
        "not_connected": 0,
        "cross_campaign_duplicate": 0,
    }

    filtered: list[dict] = []

    for prospect in prospects:
        # Skip company/business profiles
        if is_company_profile(prospect):
            stats["company_profile"] += 1
            continue

        pub_id = (prospect.get("public_id") or "").lower().strip()
        prov_id = (prospect.get("provider_id") or "").lower().strip()
        url = (prospect.get("linkedin_url") or "").lower().strip()

        identifiers = {x for x in (pub_id, prov_id, url) if x}
        if pub_id:
            identifiers.add(f"https://www.linkedin.com/in/{pub_id}")

        # Must be an existing connection
        if not (identifiers & connection_ids):
            stats["not_connected"] += 1
            continue

        # Skip cross-campaign duplicates
        if identifiers & known:
            stats["cross_campaign_duplicate"] += 1
            continue

        stats["connected"] += 1
        filtered.append(prospect)

    return filtered, stats


def format_dedup_summary(stats: dict[str, int]) -> str:
    """Format deduplication stats into a human-readable summary line."""
    removed = stats["total_before"] - stats["passed"]
    if removed == 0:
        return ""

    parts: list[str] = []
    if stats.get("company_profile", 0) > 0:
        parts.append(f"{stats['company_profile']} company pages")
    if stats["existing_connection"] > 0:
        parts.append(f"{stats['existing_connection']} existing connections")
    if stats["cross_campaign_duplicate"] > 0:
        parts.append(f"{stats['cross_campaign_duplicate']} cross-campaign duplicates")
    if stats["exclusion_list"] > 0:
        parts.append(f"{stats['exclusion_list']} excluded")

    return f"Filtered {removed} prospects: {', '.join(parts)}"
