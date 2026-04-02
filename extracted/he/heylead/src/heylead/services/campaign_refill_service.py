"""Campaign prospect enrichment — continuously discover new prospects from all sources.

Proactively feeds active campaigns from 13 sources:

LinkedIn search (API), global contacts, below-threshold signals, job changers,
signal accounts, profile viewers, post authors, competitor commenters,
company page engagers, 1st-degree connections, post commenters on your content,
low-confidence inbound leads, and news event company resolution.

All sources produce a uniform prospect dict that flows through a single pipeline:
collect → dedup → score via compute_icp_match() → sort by fit_score → save.

The communication strategist then picks highest-scored prospects first for
engagement (ORDER BY fit_score DESC).

Runs every hour via the scheduler as JOB_CAMPAIGN_REFILL.
"""

from __future__ import annotations

import json
import logging
import time
from typing import Any

from ..db import aio as db
from ..db.async_bridge import run_db

logger = logging.getLogger(__name__)


# ──────────────────────────────────────────────
# Main entry point
# ──────────────────────────────────────────────


async def refill_campaigns() -> str:
    """Proactively enrich all active campaigns with new prospects from all sources.

    Returns summary string.
    """
    from ..constants import (
        CAMPAIGN_REFILL_BATCH_SIZE,
        CAMPAIGN_REFILL_COOLDOWN_HOURS,
        CAMPAIGN_REFILL_MAX_PAGES,
        STATUS_ACTIVE,
    )

    campaigns = await db.list_campaigns(status=STATUS_ACTIVE)
    if not campaigns:
        return "No active campaigns"

    enriched = 0
    skipped = 0
    total_added = 0
    now = int(time.time())

    for campaign in campaigns:
        campaign_id = campaign["id"]
        campaign_name = campaign.get("name", campaign_id[:8])

        try:
            config = json.loads(campaign.get("config_json") or "{}")
        except (json.JSONDecodeError, TypeError):
            config = {}

        # Cooldown — avoid hammering sources
        last_refill = config.get("last_refill_at", 0)
        if now - last_refill < CAMPAIGN_REFILL_COOLDOWN_HOURS * 3600:
            skipped += 1
            continue

        # Parse ICP
        try:
            icp = json.loads(campaign.get("icp_json") or "{}")
        except (json.JSONDecodeError, TypeError):
            skipped += 1
            continue

        if not icp.get("segments"):
            skipped += 1
            continue

        try:
            added = await _enrich_campaign(
                campaign_id=campaign_id,
                campaign_name=campaign_name,
                icp=icp,
                config=config,
                max_pages=CAMPAIGN_REFILL_MAX_PAGES,
                batch_size=CAMPAIGN_REFILL_BATCH_SIZE,
            )
        except Exception as e:
            logger.warning("Enrichment failed for campaign %s: %s", campaign_name, e)
            continue

        config["last_refill_at"] = now
        await db.update_campaign(campaign_id, config_json=json.dumps(config))

        if added > 0:
            enriched += 1
            total_added += added
            logger.info("Campaign %s: added %d prospects via enrichment", campaign_name, added)

    parts = []
    if enriched:
        parts.append(f"{enriched} campaigns enriched ({total_added} new prospects)")
    if skipped:
        parts.append(f"{skipped} skipped (cooldown/no ICP)")
    return "; ".join(parts) or "No campaigns to enrich"


# ──────────────────────────────────────────────
# Core enrichment pipeline
# ──────────────────────────────────────────────


async def _enrich_campaign(
    campaign_id: str,
    campaign_name: str,
    icp: dict[str, Any],
    config: dict[str, Any],
    max_pages: int,
    batch_size: int,
) -> int:
    """Collect prospects from all sources, dedup, score, and save the best ones.

    Returns the number of prospects added.
    """
    from ..linkedin import get_account_id, get_linkedin_client
    from ..services.dedup_service import (
        dedup_prospects,
        fetch_connection_ids,
        get_all_known_linkedin_ids,
    )
    from ..services.icp_match_scorer import compute_icp_match

    client = get_linkedin_client()
    account_id = get_account_id()
    if not account_id:
        return 0

    is_connections_only = config.get("connections_only", False)

    # ── Collect from all sources ──
    all_prospects: list[dict] = []

    # Tier A: Person-level data, ready to score
    for collector in [
        lambda: _collect_from_global_contacts(campaign_id),
        lambda: _collect_from_below_threshold_signals(),
        lambda: _collect_from_job_changers(),
        lambda: _collect_from_signal_accounts(),
    ]:
        try:
            all_prospects += await collector()
        except Exception as e:
            logger.debug("Collector failed (non-critical): %s", e)

    # Tier B: Partial data, headline as title proxy
    for collector in [
        lambda: _collect_from_profile_viewers(),
        lambda: _collect_from_post_authors(),
        lambda: _collect_from_competitor_commenters(),
        lambda: _collect_from_company_engagers(),
        lambda: _collect_from_connections(account_id),
        lambda: _collect_from_post_commenters(),
        lambda: _collect_from_low_confidence_inbound(),
    ]:
        try:
            all_prospects += await collector()
        except Exception as e:
            logger.debug("Collector failed (non-critical): %s", e)

    # Tier C: Company-level, needs LinkedIn search
    try:
        all_prospects += await _collect_from_news_events(client, account_id, icp)
    except Exception as e:
        logger.debug("News event collector failed (non-critical): %s", e)

    # LinkedIn search (existing source) — skip for connections-only campaigns
    # since they source prospects from the connections table, not search.
    if not config.get("refill_exhausted") and not is_connections_only:
        try:
            search_prospects = await _search_linkedin(
                client, account_id, icp, config, max_pages, is_connections_only,
            )
            all_prospects += search_prospects
        except Exception as e:
            logger.debug("LinkedIn search failed (non-critical): %s", e)

    if not all_prospects:
        return 0

    # ── Unified pipeline: dedup → score → save ──

    # Dedup within batch by linkedin_id / public_id
    seen: set[str] = set()
    unique: list[dict] = []
    for p in all_prospects:
        key = (
            p.get("linkedin_id") or p.get("public_id")
            or p.get("linkedin_url") or ""
        ).lower().strip()
        if key and key not in seen:
            # Filter company page IDs (pure numeric = company, not person)
            raw_lid = (p.get("linkedin_id") or p.get("public_id") or "").strip()
            if raw_lid and raw_lid.isdigit():
                continue
            seen.add(key)
            unique.append(p)

    # Dedup against known contacts + connections
    try:
        known_ids = await run_db(get_all_known_linkedin_ids)
        connection_ids = await fetch_connection_ids(client, account_id)
        if is_connections_only:
            unique = [
                p for p in unique
                if not ({
                    (p.get("public_id") or "").lower().strip(),
                    (p.get("linkedin_id") or "").lower().strip(),
                    (p.get("provider_id") or "").lower().strip(),
                    (p.get("linkedin_url") or "").lower().strip(),
                } - {""}) & known_ids
            ]
        else:
            unique, _ = dedup_prospects(unique, known_ids, connection_ids)
    except Exception as e:
        logger.warning("Dedup failed (non-critical): %s", e)

    if not unique:
        return 0

    # Score against campaign ICP
    for prospect in unique:
        result = compute_icp_match(prospect, icp)
        prospect["fit_score"] = result["icp_match_score"]

    # Sort by score — communication strategist picks highest first
    unique.sort(key=lambda p: p.get("fit_score", 0), reverse=True)
    to_save = unique[:batch_size]

    # Save contacts + create pending outreaches
    added = 0
    for prospect in to_save:
        source_tag = prospect.pop("_source_tag", "enrichment")
        # Ensure provider_id from search results is persisted in profile_json
        # so DM send can use the correct ACoAAA-format ID.
        profile_json_str = prospect.get("profile_json", "")
        prov_id = prospect.get("provider_id", "")
        if prov_id and not profile_json_str:
            profile_json_str = json.dumps({"provider_id": prov_id})
        elif prov_id and profile_json_str:
            try:
                pj = json.loads(profile_json_str)
                if not pj.get("provider_id"):
                    pj["provider_id"] = prov_id
                    profile_json_str = json.dumps(pj)
            except (json.JSONDecodeError, TypeError):
                pass
        contact_id = await db.save_contact(
            campaign_id=campaign_id,
            name=prospect.get("name", ""),
            title=prospect.get("title", ""),
            company=prospect.get("company", ""),
            linkedin_url=prospect.get("linkedin_url", ""),
            linkedin_id=prospect.get("linkedin_id") or prospect.get("public_id", ""),
            profile_json=profile_json_str,
            fit_score=prospect.get("fit_score", 0.0),
            source="auto_enrichment",
            source_detail=source_tag,
        )
        if contact_id:
            await db.create_outreach(campaign_id=campaign_id, contact_id=contact_id, status="pending")
            added += 1

    return added


# ──────────────────────────────────────────────
# Tier A: Person-level, full data
# ──────────────────────────────────────────────


async def _collect_from_global_contacts(campaign_id: str) -> list[dict]:
    """Prospects already in global DB but not in this campaign."""
    # Get existing linkedin_ids in this campaign
    existing = await db.get_contacts_for_campaign(campaign_id)
    existing_ids = {
        (c.get("linkedin_id") or "").lower().strip()
        for c in existing
    } - {""}

    contacts = await db.search_global_contacts(
        lifecycle_stage="prospect", min_fit_score=0.1, limit=200,
    )
    results = []
    for c in contacts:
        lid = (c.get("linkedin_id") or "").lower().strip()
        if lid and lid not in existing_ids and not lid.isdigit():
            results.append({
                "name": c.get("name", ""),
                "title": c.get("title", ""),
                "company": c.get("company", ""),
                "linkedin_id": c.get("linkedin_id", ""),
                "linkedin_url": c.get("linkedin_url", ""),
                "location": c.get("location", ""),
                "profile_json": c.get("profile_json", ""),
                "_source_tag": "global_contacts",
            })
    return results


async def _collect_from_below_threshold_signals() -> list[dict]:
    """Signals that scored too low for one campaign may match another."""
    signals = await db.list_signals(status="actioned", limit=200)
    results = []
    for sig in signals:
        if sig.get("action_taken") != "below_threshold":
            continue
        lid = sig.get("linkedin_id", "")
        if not lid:
            continue
        meta = _parse_meta(sig)
        results.append({
            "name": sig.get("prospect_name", ""),
            "title": sig.get("prospect_title", ""),
            "company": meta.get("company", ""),
            "linkedin_id": lid,
            "linkedin_url": "",
            "_source_tag": "signal_reeval",
        })
    return results


async def _collect_from_job_changers() -> list[dict]:
    """People who recently changed jobs — new role, new budget."""
    from ..constants import SIGNAL_JOB_CHANGE

    signals = await db.list_signals(signal_type=SIGNAL_JOB_CHANGE, limit=100)
    results = []
    for sig in signals:
        lid = sig.get("linkedin_id", "")
        if not lid:
            continue
        meta = _parse_meta(sig)
        # Use new role data for scoring
        results.append({
            "name": sig.get("prospect_name", ""),
            "title": meta.get("new_title") or sig.get("prospect_title", ""),
            "company": meta.get("new_company") or meta.get("company", ""),
            "linkedin_id": lid,
            "linkedin_url": "",
            "_source_tag": "job_change",
        })
    return results


async def _collect_from_signal_accounts() -> list[dict]:
    """Aggregated multi-signal prospects with composite scores."""
    accounts = await db.list_signal_accounts(min_score=0.3, limit=200)
    results = []
    for acct in accounts:
        lid = acct.get("linkedin_id", "")
        if not lid:
            continue
        results.append({
            "name": acct.get("prospect_name", ""),
            "title": "",
            "company": acct.get("company", ""),
            "linkedin_id": lid,
            "linkedin_url": "",
            "_source_tag": "signal_account",
        })
    return results


# ──────────────────────────────────────────────
# Tier B: Partial data, headline as title proxy
# ──────────────────────────────────────────────


async def _collect_from_profile_viewers() -> list[dict]:
    """People who viewed your profile and match ICP."""
    from ..constants import SIGNAL_PROFILE_VIEW

    signals = await db.list_signals(signal_type=SIGNAL_PROFILE_VIEW, limit=100)
    results = []
    for sig in signals:
        lid = sig.get("linkedin_id", "")
        if not lid:
            continue
        meta = _parse_meta(sig)
        # Only include ICP-matched viewers
        if not meta.get("is_icp_match"):
            continue
        results.append({
            "name": sig.get("prospect_name", ""),
            "title": sig.get("prospect_title") or meta.get("viewer_title", ""),
            "company": meta.get("viewer_company", ""),
            "linkedin_id": lid,
            "linkedin_url": "",
            "_source_tag": "profile_viewer",
        })
    return results


async def _collect_from_post_authors() -> list[dict]:
    """Active LinkedIn authors posting about relevant topics."""
    authors = await db.list_post_authors(limit=200)
    results = []
    for author in authors:
        lid = author.get("linkedin_id", "")
        if not lid:
            continue
        # Only active authors (2+ posts seen)
        if (author.get("posts_seen") or 0) < 2:
            continue
        results.append({
            "name": author.get("name", ""),
            "title": author.get("headline", ""),  # headline as title proxy
            "company": author.get("company", ""),
            "linkedin_id": lid,
            "linkedin_url": "",
            "_source_tag": "post_author",
        })
    return results


async def _collect_from_competitor_commenters() -> list[dict]:
    """People commenting on competitor posts — potential buyers."""
    from ..constants import SIGNAL_COMPETITOR_POST_COMMENTER

    signals = await db.list_signals(signal_type=SIGNAL_COMPETITOR_POST_COMMENTER, limit=100)
    results = []
    for sig in signals:
        lid = sig.get("linkedin_id", "")
        if not lid:
            continue
        meta = _parse_meta(sig)
        results.append({
            "name": sig.get("prospect_name", ""),
            "title": sig.get("prospect_title") or meta.get("author_headline", ""),
            "company": meta.get("author_company", ""),
            "linkedin_id": lid,
            "linkedin_url": "",
            "_source_tag": "competitor_commenter",
        })
    return results


async def _collect_from_company_engagers() -> list[dict]:
    """People who engaged with your company's LinkedIn page."""
    from ..constants import (
        SIGNAL_COMPANY_FOLLOWER,
        SIGNAL_COMPANY_POST_COMMENT,
        SIGNAL_COMPANY_POST_REACTION,
    )

    results = []
    for signal_type in (
        SIGNAL_COMPANY_POST_COMMENT,
        SIGNAL_COMPANY_POST_REACTION,
        SIGNAL_COMPANY_FOLLOWER,
    ):
        signals = await db.list_signals(signal_type=signal_type, limit=50)
        for sig in signals:
            lid = sig.get("linkedin_id", "")
            if not lid:
                continue
            meta = _parse_meta(sig)
            results.append({
                "name": sig.get("prospect_name", ""),
                "title": sig.get("prospect_title") or meta.get("author_headline", ""),
                "company": meta.get("author_company", ""),
                "linkedin_id": lid,
                "linkedin_url": "",
                "_source_tag": "company_engager",
            })
    return results


async def _collect_from_connections(account_id: str) -> list[dict]:
    """1st-degree connections — warm leads, skip invitation step."""
    def _query_connections(acct_id: str) -> list[dict]:
        from ..db.schema import get_db
        conn = get_db()
        rows = conn.execute(
            "SELECT name, headline, provider_id, public_id FROM connections WHERE account_id = ?",
            (acct_id,),
        ).fetchall()
        conn.close()
        return [dict(r) for r in rows]

    rows = await run_db(_query_connections, account_id)

    results = []
    for r in rows:
        lid = r.get("provider_id") or r.get("public_id") or ""
        if not lid:
            continue
        results.append({
            "name": r.get("name", ""),
            "title": r.get("headline", ""),  # headline as title proxy
            "company": "",
            "linkedin_id": lid,
            "public_id": r.get("public_id", ""),
            "linkedin_url": "",
            "_source_tag": "connection",
        })
    return results


async def _collect_from_post_commenters() -> list[dict]:
    """People who commented on your published posts."""
    signals = await db.list_inbound_signals(signal_type="comment", limit=100)
    results = []
    for sig in signals:
        sid = sig.get("sender_id", "")
        if not sid:
            continue
        results.append({
            "name": sig.get("sender_name", ""),
            "title": sig.get("sender_headline", ""),
            "company": sig.get("sender_company", ""),
            "linkedin_id": sid,
            "linkedin_url": sig.get("sender_url", ""),
            "profile_json": sig.get("profile_json", ""),
            "_source_tag": "post_commenter",
        })
    return results


async def _collect_from_low_confidence_inbound() -> list[dict]:
    """Inbound leads that scored low but aren't spam — worth re-evaluating."""
    signals = await db.list_inbound_signals(status="qualified", limit=100)
    results = []
    for sig in signals:
        # Skip spam and high-confidence (already processed)
        if sig.get("intent") == "spam":
            continue
        conf = sig.get("confidence") or 0
        if conf >= 0.5:
            continue
        sid = sig.get("sender_id", "")
        if not sid:
            continue
        results.append({
            "name": sig.get("sender_name", ""),
            "title": sig.get("sender_headline", ""),
            "company": sig.get("sender_company", ""),
            "linkedin_id": sid,
            "linkedin_url": sig.get("sender_url", ""),
            "profile_json": sig.get("profile_json", ""),
            "_source_tag": "inbound_low_conf",
        })
    return results


# ──────────────────────────────────────────────
# Tier C: Company-level, needs LinkedIn search
# ──────────────────────────────────────────────


async def _collect_from_news_events(
    client: Any, account_id: str, icp: dict[str, Any],
) -> list[dict]:
    """Companies from news events (funding, acquisition, etc.) — resolve to people."""
    from ..constants import (
        SIGNAL_NEWS_ACQUISITION,
        SIGNAL_NEWS_EXEC_HIRE,
        SIGNAL_NEWS_EXPANSION,
        SIGNAL_NEWS_FUNDING,
        SIGNAL_NEWS_PRODUCT_LAUNCH,
    )

    # Collect unique company names from recent news signals
    companies: dict[str, str] = {}  # company_name → signal_type
    for sig_type in (
        SIGNAL_NEWS_FUNDING, SIGNAL_NEWS_ACQUISITION, SIGNAL_NEWS_EXEC_HIRE,
        SIGNAL_NEWS_EXPANSION, SIGNAL_NEWS_PRODUCT_LAUNCH,
    ):
        signals = await db.list_signals(signal_type=sig_type, limit=20)
        for sig in signals:
            meta = _parse_meta(sig)
            company = meta.get("company_name") or meta.get("company", "")
            if company and company not in companies:
                companies[company] = sig_type

    if not companies:
        return []

    # Extract target title from ICP for search
    segments = icp.get("segments", [])
    target_title = ""
    if segments:
        titles = segments[0].get("titles", [])
        target_title = titles[0] if titles else segments[0].get("keywords", "")

    # Search for people at each company (cap: 5 companies × 10 people)
    results = []
    for company_name in list(companies.keys())[:5]:
        try:
            prospects, _ = await client.search_people(
                account_id=account_id,
                keywords=f"{target_title} {company_name}".strip(),
                count=10,
            )
            for p in prospects:
                if not (p.get("public_id") or p.get("linkedin_url")):
                    continue
                p["_source_tag"] = f"news_{companies[company_name]}"
                results.append(p)
        except Exception as e:
            logger.debug("News company search failed for %s: %s", company_name, e)
            continue

    return results


# ──────────────────────────────────────────────
# LinkedIn search (existing source)
# ──────────────────────────────────────────────


async def _search_linkedin(
    client: Any,
    account_id: str,
    icp: dict[str, Any],
    config: dict[str, Any],
    max_pages: int,
    is_connections_only: bool,
) -> list[dict]:
    """Search LinkedIn for new prospects using campaign ICP with cursor resumption."""
    from ..linkedin.unipile import UnipileAuthError
    from ..services.search_account_resolver import resolve_search_account

    search_acct_id = config.get("search_account_id") or account_id
    try:
        resolved_id, use_sales_nav = await resolve_search_account(client, account_id)
        if not config.get("search_account_id"):
            search_acct_id = resolved_id
    except Exception:
        use_sales_nav = False

    segments = icp.get("segments", [])
    cursors = config.get("search_cursors", {})
    results_per_page = 100 if use_sales_nav else 50
    all_prospects: list[dict] = []

    for seg_idx, segment in enumerate(segments):
        seg_key = str(seg_idx)
        if cursors.get(seg_key) == "__exhausted__":
            continue

        cursor = cursors.get(seg_key)
        keywords, search_filters = _build_search_filters(
            segment, use_sales_nav, is_connections_only,
        )

        segment_prospects: list[dict] = []
        for page in range(max_pages):
            try:
                prospects, next_cursor = await client.search_people(
                    account_id=search_acct_id,
                    keywords=keywords,
                    count=results_per_page,
                    use_sales_navigator=use_sales_nav,
                    cursor=cursor,
                    **search_filters,
                )
                prospects = [
                    p for p in prospects
                    if p.get("public_id") or p.get("linkedin_url")
                ]
                segment_prospects.extend(prospects)

                if not next_cursor or len(segment_prospects) >= 200:
                    cursors[seg_key] = "__exhausted__" if not next_cursor else next_cursor
                    break
                cursor = next_cursor
            except UnipileAuthError:
                logger.warning("Auth error during LinkedIn search")
                break
            except Exception as e:
                logger.warning("Search failed segment %d page %d: %s", seg_idx, page, e)
                break
        else:
            if cursor:
                cursors[seg_key] = cursor

        for p in segment_prospects:
            p["_source_tag"] = "linkedin_search"
        all_prospects.extend(segment_prospects)

    config["search_cursors"] = cursors

    # Mark exhausted if all segments done
    if all(cursors.get(str(i)) == "__exhausted__" for i in range(len(segments))):
        config["refill_exhausted"] = True

    return all_prospects


# ──────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────


def _parse_meta(sig: dict[str, Any]) -> dict[str, Any]:
    """Parse metadata_json from a signal row."""
    raw = sig.get("metadata_json", "")
    if not raw:
        return {}
    try:
        return json.loads(raw) if isinstance(raw, str) else raw
    except (json.JSONDecodeError, TypeError):
        return {}


def _build_search_filters(
    segment: dict[str, Any],
    use_sales_nav: bool,
    connections_only: bool,
) -> tuple[str, dict[str, Any]]:
    """Build search keywords and filters from an ICP segment."""
    keywords = segment.get("keywords", "")
    titles = segment.get("titles", [])
    has_structured = segment.get("has_structured", False)

    search_keywords = keywords
    if not has_structured and titles and titles[0].lower() not in keywords.lower():
        search_keywords = f"{titles[0]} {keywords}"

    search_filters: dict[str, Any] = {}
    if has_structured or segment.get("industry_codes"):
        if segment.get("industry_codes"):
            search_filters["industry_codes"] = segment["industry_codes"]
        if segment.get("location_codes"):
            search_filters["location_codes"] = segment["location_codes"]

        if use_sales_nav:
            for key, param in [
                ("title_codes", "role_codes"), ("seniority", "seniority"),
                ("company_headcount", "company_headcount"), ("company_types", "company_types"),
                ("department_codes", "department_codes"), ("tenure", "tenure"),
                ("spotlight", "spotlight"), ("annual_revenue", "annual_revenue"),
                ("company_headcount_growth", "company_headcount_growth"),
            ]:
                if segment.get(key):
                    search_filters[param] = segment[key]
            if segment.get("boolean_keywords"):
                search_keywords = segment["boolean_keywords"]
            elif search_filters.get("role_codes"):
                search_keywords = ""
        else:
            title_kw = " OR ".join(titles[:3]) if titles else ""
            if title_kw:
                search_keywords = title_kw
            elif search_filters.get("industry_codes"):
                search_keywords = ""

    if connections_only:
        search_filters["network_distance"] = [1]

    return search_keywords, search_filters


# ──────────────────────────────────────────────
# Profile enrichment for contacts with empty profile_json
# ──────────────────────────────────────────────

ENRICH_BATCH_SIZE = 50
ENRICH_DELAY_SECONDS = 2.5


async def backfill_empty_profiles() -> str:
    """Periodic backfill: enrich global contacts with empty profile_json.

    Scheduled every 15 min via JOB_BACKFILL_PROFILES. Skips company page IDs.
    Rate-limited to ENRICH_BATCH_SIZE per run with delays between calls.
    Prioritizes 1st-degree connections (network_degree=1) so synced
    connections get enriched first.
    """
    import asyncio

    from ..db.async_bridge import run_db
    from ..db.global_contact_queries import upsert_global_contact
    from ..linkedin import get_account_id, get_linkedin_client

    client = get_linkedin_client()
    account_id = get_account_id()
    if not account_id:
        return "No account connected"

    def _find_unenriched() -> list[dict]:
        from ..db.schema import get_db

        conn = get_db()
        rows = conn.execute(
            """SELECT id, linkedin_id, name, title, company, linkedin_url, fit_score
               FROM global_contacts
               WHERE (profile_json IS NULL OR profile_json = '' OR profile_json = '{}')
                 AND linkedin_id IS NOT NULL AND linkedin_id != ''
               ORDER BY network_degree DESC NULLS LAST, created_at DESC
               LIMIT ?""",
            (ENRICH_BATCH_SIZE,),
        ).fetchall()
        conn.close()
        return [dict(r) for r in rows]

    rows = await run_db(_find_unenriched)
    if not rows:
        return "No contacts need profile backfill"

    enriched = 0
    skipped_company = 0
    failed = 0
    for row in rows:
        lid = row["linkedin_id"]
        if lid.strip().isdigit():
            skipped_company += 1
            continue
        try:
            profile = await client.get_profile(account_id, lid)
            if not profile:
                failed += 1
                continue
            profile_str = json.dumps(profile) if isinstance(profile, dict) else str(profile)

            title = row.get("title") or ""
            company = row.get("company") or ""
            if isinstance(profile, dict):
                title = profile.get("title") or title
                company = profile.get("company") or company

            await run_db(
                upsert_global_contact,
                linkedin_id=lid,
                name=row.get("name", ""),
                title=title,
                company=company,
                linkedin_url=row.get("linkedin_url", ""),
                profile_json=profile_str,
                fit_score=row.get("fit_score", 0.0),
                source="profile_backfill",
            )
            enriched += 1
        except Exception as e:
            logger.debug("Backfill failed for %s: %s", lid[:20], e)
            failed += 1
        await asyncio.sleep(ENRICH_DELAY_SECONDS)

    parts = []
    if enriched:
        parts.append(f"{enriched} profiles enriched")
    if skipped_company:
        parts.append(f"{skipped_company} company pages skipped")
    if failed:
        parts.append(f"{failed} failed")
    return "; ".join(parts) or "No profiles enriched"
