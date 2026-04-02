"""Hiring surge signal collector — detects companies posting many related jobs.

Uses `search_jobs()` with ICP-derived role keywords to find active hiring.
Groups results by company and flags "surges" when a company has 3+ related
job postings — a strong budget/growth signal indicating buying intent.

Runs every 4 hours via the scheduler.
"""

from __future__ import annotations

import json
import logging
import time
from collections import defaultdict
from typing import Any

logger = logging.getLogger(__name__)


async def collect_hiring_signals() -> str:
    """Collect hiring surge signals from LinkedIn job searches.

    For each active campaign with an ICP:
    1. Extract role-related keywords from ICP job_titles + keywords
    2. Search LinkedIn jobs using those keywords
    3. Group results by company
    4. Flag companies with 3+ related postings as hiring surges
    5. Cross-reference against campaign contacts

    Returns summary string.
    """
    from ..constants import (
        SIGNAL_DAILY_KEYWORD_SEARCHES,
        SIGNAL_HIRING_SURGE,
        SIGNAL_TTL_HIRING_SURGE,
        STATUS_ACTIVE,
    )
    from ..db.async_bridge import run_db
    from ..db.queries import list_campaigns
    from ..db.signal_queries import (
        get_contact_by_linkedin_id,
        get_daily_signal_search_count,
        save_signal,
        signal_exists,
        upsert_signal_account,
    )
    from ..linkedin import UnipileError, get_account_id, get_linkedin_client

    account_id = get_account_id()
    if not account_id:
        return "No LinkedIn account connected."

    # Hiring searches share the daily budget with keyword searches
    daily_count = await run_db(get_daily_signal_search_count, "keyword")
    remaining = SIGNAL_DAILY_KEYWORD_SEARCHES - daily_count
    if remaining <= 0:
        return f"Daily search limit reached ({daily_count}/{SIGNAL_DAILY_KEYWORD_SEARCHES})."

    # Max 20 job searches per run (subset of shared budget)
    max_searches = min(remaining, 20)

    # Get active campaigns with ICPs
    campaigns = await run_db(list_campaigns, status=STATUS_ACTIVE)
    if not campaigns:
        return "No active campaigns."

    # Extract search keywords from campaign ICPs
    search_keywords = _extract_hiring_keywords(campaigns)
    if not search_keywords:
        return "No ICP keywords available for hiring search."

    try:
        client = get_linkedin_client()
    except UnipileError as e:
        return f"LinkedIn client error: {e}"

    total_searched = 0
    total_new = 0
    errors = 0
    now = int(time.time())
    surge_threshold = 3  # 3+ related postings = hiring surge

    # Aggregate jobs by company across all keyword searches
    company_jobs: dict[str, list[dict[str, Any]]] = defaultdict(list)
    company_campaigns: dict[str, str] = {}  # company_id → campaign_id

    try:
        for keyword, campaign_id in search_keywords:
            if total_searched >= max_searches:
                break

            try:
                jobs, _ = await client.search_jobs(
                    account_id, keyword, limit=25
                )
                total_searched += 1

                for job in jobs:
                    company_id = job.get("company_id", "")
                    company_name = job.get("company_name", "")
                    if not company_id or not company_name:
                        continue

                    company_jobs[company_id].append(job)
                    if campaign_id and company_id not in company_campaigns:
                        company_campaigns[company_id] = campaign_id

            except Exception as e:
                logger.warning(
                    "Job search failed for '%s': %s", keyword, e
                )
                errors += 1

        # Detect surges: companies with 3+ job postings
        for company_id, jobs in company_jobs.items():
            if len(jobs) < surge_threshold:
                continue

            company_name = jobs[0].get("company_name", "")

            # Dedup: skip if we already have a recent hiring surge for this company
            if await run_db(
                signal_exists,
                SIGNAL_HIRING_SURGE,
                linkedin_id=company_id,
                lookback_seconds=7 * 86400,  # 1 week cooldown
            ):
                continue

            # Build job summary
            job_titles = [j.get("title", "") for j in jobs[:10]]
            locations = list({j.get("location", "") for j in jobs if j.get("location")})
            campaign_id = company_campaigns.get(company_id)

            metadata = {
                "company_id": company_id,
                "company_name": company_name,
                "company_url": jobs[0].get("company_url", ""),
                "job_count": len(jobs),
                "job_titles": job_titles,
                "locations": locations[:5],
                "surge_threshold": surge_threshold,
                "search_keywords": [
                    kw for kw, _ in search_keywords[:5]
                ],
            }

            # Build descriptive content
            content = (
                f"{company_name} is hiring for {len(jobs)} roles: "
                f"{', '.join(job_titles[:5])}"
            )
            if len(job_titles) > 5:
                content += f" and {len(job_titles) - 5} more"

            await run_db(
                save_signal,
                signal_type=SIGNAL_HIRING_SURGE,
                source="job_search",
                prospect_name=company_name,
                linkedin_id=company_id,
                campaign_id=campaign_id,
                content=content[:1000],
                metadata_json=json.dumps(metadata),
                expires_at=now + SIGNAL_TTL_HIRING_SURGE,
            )
            total_new += 1

            # Update signal account for company
            await run_db(
                upsert_signal_account,
                linkedin_id=company_id,
                prospect_name=company_name,
                company=company_name,
            )

    finally:
        await client.close()

    summary = (
        f"Searched {total_searched} job keywords, "
        f"found {total_new} hiring surges "
        f"({len(company_jobs)} companies analyzed)"
    )
    if errors:
        summary += f", {errors} errors"
    return summary


def _extract_hiring_keywords(
    campaigns: list[dict[str, Any]],
) -> list[tuple[str, str]]:
    """Extract job-search keywords from campaign ICPs.

    Pulls from ICP job_titles and keywords fields.
    Returns list of (keyword, campaign_id) tuples.
    """
    import json as _json

    results: list[tuple[str, str]] = []
    seen: set[str] = set()

    for campaign in campaigns:
        campaign_id = campaign.get("id", "")
        icp_json = campaign.get("icp_json", "")
        if not icp_json:
            continue

        try:
            icp_data = _json.loads(icp_json)
        except (ValueError, TypeError):
            continue

        # Handle both direct ICP and IcpResult wrapper
        icps = icp_data.get("icps", [icp_data])

        for icp in icps:
            if not isinstance(icp, dict):
                continue

            # Extract from job_titles — handle dict, list, and str formats
            job_titles = icp.get("job_titles", {})
            titles_list: list[str] = []
            if isinstance(job_titles, dict):
                titles_list = job_titles.get("include", [])
            elif isinstance(job_titles, list):
                titles_list = job_titles
            elif isinstance(job_titles, str) and job_titles.strip():
                titles_list = [job_titles]

            for title in titles_list:
                if not isinstance(title, str):
                    continue
                title_clean = title.strip().lower()
                if title_clean and title_clean not in seen:
                    seen.add(title_clean)
                    results.append((title, campaign_id))

            # Extract from keywords — handle dict, list, and str formats
            keywords = icp.get("keywords", [])
            keywords_list: list[str] = []
            if isinstance(keywords, dict):
                keywords_list = keywords.get("include", [])
            elif isinstance(keywords, list):
                keywords_list = keywords
            elif isinstance(keywords, str) and keywords.strip():
                keywords_list = [keywords]

            for kw in keywords_list[:5]:
                if not isinstance(kw, str):
                    continue
                kw_clean = kw.strip().lower()
                if kw_clean and kw_clean not in seen:
                    seen.add(kw_clean)
                    results.append((kw, campaign_id))

    return results
