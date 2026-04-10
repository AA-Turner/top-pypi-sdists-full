"""Tool 2: create_campaign — Create a LinkedIn outreach campaign from a natural language description.

Takes a target description like "Find me fintech CTOs" and:
1. Generates an ICP (Ideal Customer Profile) via LLM
2. Searches LinkedIn for matching prospects
3. Scores and ranks prospects by fit
4. Creates a campaign with queued contacts
5. Shows a preview for confirmation
"""

from __future__ import annotations

import json
import logging
from typing import Any

from ..ai.icp_schemas import IcpResult, icp_result_from_dict
from .. import config as config_mod
from ..config import get_tier, is_scheduler_enabled, load_config, set_scheduler_enabled
from ..constants import (
    DEFAULT_NOISE_TYPE,
    DEFAULT_VOICE_HUMANIZE,
    FREE_MAX_CAMPAIGNS,
    FREE_MAX_CONTACTS_ANALYZED,
    STATUS_ACTIVE,
    STATUS_DRAFT,
    TIER_PRO,
    VALID_VOICE_MODES,
    VOICE_MODE_MIXED,
)
from ..db.queries import (
    assign_variant,
    create_campaign,
    create_outreach,
    get_icp,
    get_monthly_usage,
    get_setting,
    increment_usage,
    list_ab_tests,
    list_campaigns,
    save_contact,
    save_setting,
    update_campaign,
)
from ..formatter import stars, table
from ..linkedin import (
    UnipileAuthError,
    UnipileError,
    get_account_id,
    get_linkedin_client,
)
from ..db.async_bridge import run_db

logger = logging.getLogger(__name__)


def _score_prospect(prospect: dict, icp_segment: dict) -> float:
    """Score a prospect (0.0 - 1.0) against an ICP segment."""
    score = 0.0
    max_score = 0.0

    # Title match (highest weight)
    max_score += 3.0
    target_titles = [t.lower() for t in icp_segment.get("titles", [])]
    prospect_title = prospect.get("title", "").lower()
    if any(t in prospect_title for t in target_titles):
        score += 3.0
    elif any(word in prospect_title for t in target_titles for word in t.split()):
        score += 1.5

    # Keyword match in headline
    max_score += 2.0
    keywords = icp_segment.get("keywords", "").lower().split(",")
    headline = prospect.get("headline", "").lower()
    keyword_matches = sum(1 for kw in keywords if kw.strip() and kw.strip() in headline)
    if keywords:
        score += min(2.0, (keyword_matches / max(len(keywords), 1)) * 2.0)

    # Has company info
    max_score += 1.0
    if prospect.get("company"):
        score += 1.0

    # Has location info
    max_score += 0.5
    if prospect.get("location"):
        score += 0.5

    # Has public_id (can be reached)
    max_score += 0.5
    if prospect.get("public_id"):
        score += 0.5

    return score / max_score if max_score > 0 else 0.0


async def run_create_campaign(
    target_description: str,
    campaign_name: str = "",
    icp_id: str = "",
    company_context: str = "",
    mode: str = "autopilot",
    company_url: str = "",
    voice_mode: str = VOICE_MODE_MIXED,
    connections_only: str = "",
    _internal_source: str = "",
) -> str:
    """Create a new outreach campaign.

    Args:
        target_description: Who to target (e.g. "CTOs at fintech startups").
        campaign_name: Optional name for the campaign.
        icp_id: Optional saved ICP ID to reuse.
        company_context: Optional website URL or company description.
        mode: "autopilot" (sends automatically) or "copilot" (review each message).
        company_url: Optional LinkedIn company URL for account-based targeting.
            When provided, searches for employees at that specific company matching
            the ICP title filters. Example: "https://www.linkedin.com/company/google"
        voice_mode: Voice memo mode for follow-ups/replies. "mixed" (default,
            alternates text and voice), "text_only", "voice_only", or "ab_test".

    Flow:
    1. Check setup is complete + free tier limits
    2. On first campaign: ask for company context if missing (guide for best results)
    3. Load saved ICP (if icp_id provided) or generate new one (with company_context if given)
    4. Search LinkedIn for matching prospects
    5. Score and rank by fit
    6. Create campaign + queued contacts in DB
    7. Auto-enable scheduler if autopilot
    8. Return launch confirmation
    """

    # Always autopilot (copilot mode removed)
    mode = "autopilot"

    # Validate voice_mode
    if voice_mode and voice_mode not in VALID_VOICE_MODES:
        return f"❌ Invalid voice_mode '{voice_mode}'. Must be one of: {', '.join(sorted(VALID_VOICE_MODES))}."
    if not voice_mode:
        voice_mode = VOICE_MODE_MIXED

    # ── Step 0: Check setup ──
    setup_done = await run_db(get_setting, "setup_complete", False)
    if not setup_done:
        return (
            "❌ Setup required before creating campaigns.\n\n"
            "Please run setup_profile first — it connects your LinkedIn account and "
            "analyzes your writing style so messages sound like you.\n\n"
            "If you haven't started setup yet, say 'set up my profile' and I'll walk "
            "you through it step by step (takes about 2 minutes)."
        )

    # ── Step 1: Free tier limits ──
    tier = get_tier()
    existing = await run_db(list_campaigns)
    if tier != TIER_PRO:
        active_campaigns = [c for c in existing if c["status"] in (STATUS_ACTIVE, STATUS_DRAFT)]
        if len(active_campaigns) >= FREE_MAX_CAMPAIGNS:
            return (
                f"⚠️ Free tier limit: {FREE_MAX_CAMPAIGNS} active campaign(s).\n\n"
                "You already have an active campaign. Options:\n"
                "├── Complete or pause your current campaign first\n"
                "└── Upgrade to Pro ($29/mo) for unlimited campaigns\n\n"
                "Tip: Say 'show_status' to see your current campaign."
            )

    # ── Step 1b: First campaign — ask for company context and guide for best results ──
    is_first_campaign = len(existing) == 0
    if is_first_campaign and not icp_id and not (company_context or "").strip():
        return (
            "👋 **First campaign — let's set you up for the best results**\n\n"
            "**Share your company context** so we can:\n"
            "├── Build a sharper ICP (who’s a great fit for *you*)\n"
            "├── Match LinkedIn prospects more precisely\n"
            "└── Generate messages that feel relevant to your product\n\n"
            "**How to provide it:**\n"
            "• **Option A:** Create the campaign with context in one go:\n"
            "  `create_campaign(target_description=\"…\", company_context=\"Your website URL or 1–2 sentences about your product/company\")`\n\n"
            "• **Option B:** Generate an ICP first (with context), then create the campaign:\n"
            "  1. `generate_icp(target_description=\"…\", company_context=\"…\")`\n"
            "  2. `create_campaign(icp_id=\"<id from step 1>\")`\n\n"
            "**Examples of company_context:**\n"
            "• Your homepage URL (e.g. https://yourproduct.com)\n"
            "• A short blurb: \"We help SMBs automate payroll. Series A, 20 people.\"\n\n"
            "Once you have your context ready, call create_campaign again with `company_context` (or use an ICP from generate_icp)."
        )

    # ── Step 2: Get Unipile account ──
    account_id = get_account_id()
    if not account_id:
        return (
            "❌ No LinkedIn account connected.\n\n"
            "Run setup_profile first to connect your LinkedIn account."
        )

    try:
        client = get_linkedin_client()
    except UnipileError as e:
        return f"❌ {e}"

    # ── Step 2b: Resolve search account (separate from sending account) ──
    from ..services.search_account_resolver import resolve_search_account

    try:
        search_acct_id, use_sales_nav = await resolve_search_account(
            client=client,
            sending_account_id=account_id,
        )
    except Exception as e:
        logger.warning("Search account resolution failed, using own account: %s", e)
        search_acct_id = account_id
        use_sales_nav = False

    if search_acct_id != account_id:
        logger.info(
            "Using premium account %s for search (sending via %s)",
            search_acct_id[:8], account_id[:8],
        )

    # Pass search_account_id to backend if using a different account
    _search_account_override = search_acct_id if search_acct_id != account_id else None

    # ── Step 3: Load saved ICP or generate new one ──
    saved_icp_result: IcpResult | None = None

    if icp_id:
        # Try full ID first, then prefix match
        icp_record = await run_db(get_icp, icp_id)
        if not icp_record:
            # Try prefix match (user may pass truncated ID like "a1b2c3d4...")
            from ..db.queries import list_icps
            all_icps = await run_db(list_icps)
            for r in all_icps:
                if r["id"].startswith(icp_id.rstrip(".")):
                    icp_record = r
                    break

        if not icp_record:
            return (
                f"ICP not found: `{icp_id}`\n\n"
                "Use show_status() to see saved ICPs, or generate a new one with generate_icp()."
            )

        try:
            icp_data = json.loads(icp_record["icp_json"])
            saved_icp_result = icp_result_from_dict(icp_data)
            logger.info(f"Loaded saved ICP: {icp_record['name']} ({len(saved_icp_result.icps)} personas)")
        except Exception as e:
            logger.warning(f"Failed to parse saved ICP: {e}")
            saved_icp_result = None

    if saved_icp_result and saved_icp_result.icps:
        # Use saved ICP — build segments from enriched data
        icp = _icp_result_to_legacy(saved_icp_result, target_description)
    else:
        # Generate new ICP inline (with company_context when provided)
        profile = await run_db(get_setting, "profile", {})
        expertise = await run_db(get_setting, "expertise_map", {})
        user_context = {**profile, **expertise}

        try:
            from ..tools.generate_icp import generate_icp_result_for_campaign
        except ImportError as e:
            logger.error(f"ICP module import failed: {e}", exc_info=True)
            return (
                f"❌ Could not load ICP generator: {e}\n\n"
                "This may be a missing dependency. Try: pip install heylead[icp]"
            )

        try:
            result = await generate_icp_result_for_campaign(
                target_description=target_description,
                company_context=company_context or "",
                focus_query="",
                user_context=user_context,
            )
            if not result.icps:
                return (
                    "❌ Could not generate an ICP for this description.\n\n"
                    "Try a different or broader target description."
                )
            icp = _icp_result_to_legacy(result, target_description)
        except Exception as e:
            logger.error(f"ICP generation failed: {e}", exc_info=True)
            return (
                f"❌ Failed to generate ICP: {e}\n\n"
                "Check your LLM API key in ~/.heylead/config.json"
            )

    # ── Step 4: Sales Navigator status (resolved in Step 2b) ──
    if use_sales_nav:
        logger.info("Sales Navigator available — using enhanced search")

    # ── Step 4b: ABM — enrich with company info if company_url provided ──
    abm_company_name = ""
    if company_url:
        try:
            # Extract company identifier from URL (e.g., "google" from linkedin.com/company/google)
            import re
            match = re.search(r"linkedin\.com/company/([^/?#]+)", company_url)
            identifier = match.group(1) if match else company_url.strip()
            company_data = await client.get_company_profile(account_id, identifier)
            if isinstance(company_data, dict):
                abm_company_name = company_data.get("name") or company_data.get("company_name") or ""
                logger.info("ABM mode: targeting employees at '%s'", abm_company_name)
        except Exception as e:
            logger.warning("Company profile fetch failed: %s", e)
            # Fall back to using the URL/identifier as company name
            if not abm_company_name:
                match = re.search(r"linkedin\.com/company/([^/?#]+)", company_url)
                abm_company_name = match.group(1).replace("-", " ").title() if match else ""

    # ── Step 4c: Auto-create company watchlist for ABM signal monitoring ──
    if abm_company_name and company_url:
        try:
            from ..db.signal_queries import list_watchlists, save_watchlist
            import re as _re
            _match = _re.search(r"linkedin\.com/company/([^/?#]+)", company_url)
            company_identifier = _match.group(1) if _match else ""
            if isinstance(company_data, dict):
                company_identifier = company_data.get("provider_id") or company_identifier
            if company_identifier:
                existing_company_wl = [
                    w for w in await run_db(list_watchlists, is_active=True)
                    if w.get("watch_type") == "company"
                    and company_identifier in (w.get("keywords_list") or [])
                ]
                if not existing_company_wl:
                    await run_db(save_watchlist, name=abm_company_name or company_identifier,
                        watch_type="company",
                        keywords=[company_identifier],
                        campaign_id=campaign_id,)
                    logger.info("Auto-created company watchlist for ABM target: %s", abm_company_name)
        except Exception as e:
            logger.debug("ABM company watchlist creation failed (non-fatal): %s", e)

    # ── Step 5: Find prospects ──
    all_prospects: list[dict] = []
    segments = icp.get("segments", [])

    # Track which segment each prospect came from (for per-segment scoring)
    segment_index_map: dict[str, int] = {}  # prospect key → segment index

    if connections_only == "on":
        # ── CONNECTIONS-ONLY: source from local connections table ──
        # No LinkedIn search needed — we already have all 1st-degree connections.
        from ..services.connection_sync import ensure_synced, get_all_connections
        from ..db.global_contact_queries import get_global_contacts_by_identifiers

        await ensure_synced(client, account_id)
        raw_connections = await run_db(get_all_connections, account_id)
        logger.info("Connections-only: %d 1st-degree connections found", len(raw_connections))

        # Batch lookup existing global_contacts for enrichment data
        all_identifiers = []
        for c in raw_connections:
            if c.get("provider_id"):
                all_identifiers.append(c["provider_id"])
            if c.get("public_id"):
                all_identifiers.append(c["public_id"])
        gc_map = await run_db(get_global_contacts_by_identifiers, all_identifiers)

        # Convert connections to prospect dicts, merging any existing enrichment
        for conn in raw_connections:
            pid = conn.get("provider_id", "")
            pub = conn.get("public_id", "")
            # Find matching global_contact (try provider_id first, then public_id)
            gc = gc_map.get(pid.lower().strip()) or gc_map.get(pub.lower().strip()) or {}
            # Merge enriched data if available
            profile_json = gc.get("profile_json", "")
            title = gc.get("title") or conn.get("headline", "")
            company = gc.get("company", "")
            location = gc.get("location", "")
            if profile_json and not company:
                try:
                    pj = json.loads(profile_json) if isinstance(profile_json, str) else profile_json
                    company = pj.get("company", "") or company
                    location = pj.get("location", "") or location
                    if not title:
                        title = pj.get("headline", "") or pj.get("title", "")
                except (json.JSONDecodeError, TypeError):
                    pass

            prospect = {
                "name": conn.get("name", ""),
                "title": title,
                "headline": conn.get("headline", ""),
                "company": company,
                "location": location,
                "linkedin_id": pid or pub,
                "provider_id": pid,
                "public_id": pub,
                "linkedin_url": f"https://www.linkedin.com/in/{pub}" if pub else "",
                "profile_json": profile_json,
                "_source_tag": "connection",
            }
            if pid or pub:
                all_prospects.append(prospect)
    else:
        # ── STANDARD: Search LinkedIn via Unipile with structured filters ──

        # Pagination config
        MAX_PAGES = 15 if not use_sales_nav else 10
        RESULTS_PER_PAGE = 50 if not use_sales_nav else 100

        for seg_idx, segment in enumerate(segments):
            keywords = segment.get("keywords", "")
            titles = segment.get("titles", [])
            has_structured = segment.get("has_structured", False)

            # Build search keywords as fallback
            search_keywords = keywords
            if not has_structured and titles and titles[0].lower() not in keywords.lower():
                search_keywords = f"{titles[0]} {keywords}"

            # ABM: prepend company name to keywords for company-targeted search
            if abm_company_name:
                title_part = titles[0] if titles else ""
                search_keywords = f"{title_part} {abm_company_name}".strip()

            # Extract structured filters (enriched LinkedIn codes)
            search_filters: dict = {}
            if has_structured or segment.get("industry_codes"):
                if segment.get("industry_codes"):
                    search_filters["industry_codes"] = segment["industry_codes"]
                if segment.get("location_codes"):
                    search_filters["location_codes"] = segment["location_codes"]

                if use_sales_nav:
                    if segment.get("title_codes"):
                        search_filters["role_codes"] = segment["title_codes"]
                    if segment.get("seniority"):
                        search_filters["seniority"] = segment["seniority"]
                    if segment.get("company_headcount"):
                        search_filters["company_headcount"] = segment["company_headcount"]
                    if segment.get("company_types"):
                        search_filters["company_types"] = segment["company_types"]
                    if segment.get("department_codes"):
                        search_filters["department_codes"] = segment["department_codes"]
                    if segment.get("tenure"):
                        search_filters["tenure"] = segment["tenure"]
                    if segment.get("spotlight"):
                        search_filters["spotlight"] = segment["spotlight"]
                    if segment.get("annual_revenue"):
                        search_filters["annual_revenue"] = segment["annual_revenue"]
                    if segment.get("company_headcount_growth"):
                        search_filters["company_headcount_growth"] = segment["company_headcount_growth"]
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

                logger.info(
                    "Searching with %d structured filters for '%s'",
                    len(search_filters), segment.get("name"),
                )

            # ── Paginated search loop ──
            cursor = None
            segment_prospects: list[dict] = []

            for page in range(MAX_PAGES):
                try:
                    prospects, next_cursor = await client.search_people(
                        account_id=search_acct_id,
                        keywords=search_keywords,
                        count=RESULTS_PER_PAGE,
                        use_sales_navigator=use_sales_nav,
                        cursor=cursor,
                        search_account_id=_search_account_override,
                        **search_filters,
                    )
                    prospects = [
                        p for p in prospects
                        if p.get("public_id") or p.get("linkedin_url")
                    ]
                    segment_prospects.extend(prospects)

                    if not next_cursor or len(segment_prospects) >= 200:
                        break
                    cursor = next_cursor
                    logger.info(
                        "Page %d: got %d prospects, paginating...",
                        page + 1, len(prospects),
                    )
                except UnipileAuthError:
                    if _search_account_override:
                        from ..services.search_account_resolver import invalidate_search_account_cache
                        invalidate_search_account_cache()
                        logger.warning(
                            "Premium search account auth failed, falling back to sending account"
                        )
                        search_acct_id = account_id
                        _search_account_override = None
                        use_sales_nav = False
                        break
                    await client.close()
                    return (
                        "🔑 LinkedIn account disconnected.\n\n"
                        "Run setup_profile() again to reconnect."
                    )
                except UnipileError:
                    await client.close()
                    raise
                except Exception as e:
                    logger.warning(f"Search failed for segment '{segment.get('name')}' page {page}: {e}")
                    break

            # Fallback: if structured search yielded too few results, retry with
            # relaxed filters (drop company_headcount, add title keywords)
            if len(segment_prospects) < 5 and has_structured and not use_sales_nav:
                relaxed_filters = {k: v for k, v in search_filters.items()}
                relaxed_filters.pop("company_headcount", None)
                relaxed_filters.pop("tenure", None)
                title_kw = " OR ".join(titles[:3]) if titles else ""
                logger.info(
                    "Segment '%s': only %d prospects with full filters, "
                    "retrying with relaxed filters + title keywords '%s'",
                    segment.get("name"), len(segment_prospects), title_kw[:60],
                )
                try:
                    retry_prospects, _ = await client.search_people(
                        account_id=search_acct_id,
                        keywords=title_kw,
                        count=RESULTS_PER_PAGE,
                        use_sales_navigator=False,
                        search_account_id=_search_account_override,
                        **relaxed_filters,
                    )
                    retry_prospects = [
                        p for p in retry_prospects
                        if p.get("public_id") or p.get("linkedin_url")
                    ]
                    existing_ids = {
                        p.get("public_id") or p.get("linkedin_url")
                        for p in segment_prospects
                    }
                    for p in retry_prospects:
                        pid = p.get("public_id") or p.get("linkedin_url")
                        if pid and pid not in existing_ids:
                            segment_prospects.append(p)
                            existing_ids.add(pid)
                    logger.info(
                        "Relaxed retry added %d new prospects (total: %d)",
                        len(retry_prospects), len(segment_prospects),
                    )
                except Exception as e:
                    logger.warning(f"Relaxed search fallback failed: {e}")

            if segment_prospects:
                logger.info(
                    "Segment '%s': %d prospects across %d pages%s",
                    segment.get("name"), len(segment_prospects),
                    min(page + 1, MAX_PAGES),
                    " (Sales Nav)" if use_sales_nav else "",
                )

            # Tag each prospect with its source segment index (first segment wins)
            for p in segment_prospects:
                key = p.get("public_id") or p.get("linkedin_url") or p.get("name")
                if key and key not in segment_index_map:
                    segment_index_map[key] = seg_idx

            all_prospects.extend(segment_prospects)

    if not all_prospects:
        if connections_only == "on":
            return (
                f"❌ No 1st-degree connections found in your network.\n\n"
                "Your connections may not be synced yet. Try:\n"
                "1. Run setup_profile() to re-sync your LinkedIn account\n"
                "2. Drop connections_only to run standard cold outreach with invitations"
            )
        return (
            "😕 No prospects found on LinkedIn for this description.\n\n"
            f"Searched for: \"{target_description}\"\n\n"
            "Try:\n"
            "├── Use broader keywords (e.g., 'startup founders' instead of 'fintech CTO Series A')\n"
            "├── Check your LinkedIn connection (run setup_profile)\n"
            "├── In backend mode: check heylead-api logs and Unipile account/API limits\n"
            "└── Try a different target description"
        )

    # Deduplicate by public_id or linkedin_url
    seen = set()
    unique_prospects = []
    for p in all_prospects:
        key = p.get("public_id") or p.get("linkedin_url") or p.get("name")
        if key and key not in seen:
            seen.add(key)
            unique_prospects.append(p)

    # ── Step 5a: Dedup — filter existing connections + cross-campaign contacts ──
    dedup_summary = ""
    try:
        from ..services.dedup_service import (
            dedup_prospects,
            fetch_connection_ids,
            filter_to_connections_only,
            format_dedup_summary,
            get_all_known_linkedin_ids,
            get_excluded_linkedin_ids,
        )
        known_ids = await run_db(get_all_known_linkedin_ids)
        connection_ids = await fetch_connection_ids(client, account_id)
        excluded_ids = await run_db(get_excluded_linkedin_ids)

        # Filter out contacts excluded from automation (do-not-automate tag / do_not_contact)
        if excluded_ids:
            pre_excluded = len(unique_prospects)
            unique_prospects = [
                p for p in unique_prospects
                if not ({
                    (p.get("public_id") or "").lower().strip(),
                    (p.get("provider_id") or "").lower().strip(),
                    (p.get("linkedin_url") or "").lower().strip(),
                } - {""}) & excluded_ids
            ]
            excluded_count = pre_excluded - len(unique_prospects)
            if excluded_count > 0:
                logger.info("Excluded %d contacts from automation (do-not-automate)", excluded_count)
                dedup_summary += f"\n{excluded_count} excluded from automation (do-not-automate)"

        if connections_only == "on":
            # Connections-only: prospects come from local connections table
            # (already verified 1st-degree). Only remove cross-campaign dupes.
            pre_count = len(unique_prospects)
            unique_prospects = [
                p for p in unique_prospects
                if not ({
                    (p.get("public_id") or "").lower().strip(),
                    (p.get("provider_id") or "").lower().strip(),
                    (p.get("linkedin_url") or "").lower().strip(),
                } - {""}) & known_ids
            ]
            dupes = pre_count - len(unique_prospects)
            if dupes > 0:
                dedup_summary += f"\nConnections filter: {pre_count} connections, {dupes} cross-campaign duplicates removed"
                logger.info("Connections-only: %s", dedup_summary)
        else:
            # Standard: filter OUT existing connections + duplicates
            unique_prospects, dedup_stats = dedup_prospects(
                unique_prospects, known_ids, connection_ids,
            )
            dedup_summary = format_dedup_summary(dedup_stats)
            if dedup_summary:
                logger.info("Dedup: %s", dedup_summary)
    except Exception as e:
        logger.warning("Dedup check failed (non-critical): %s", e)

    # ── Known-contacts detection (connections-only) ──
    known_contacts_warning = ""
    if connections_only == "on" and unique_prospects:
        try:
            known_contacts = await run_db(
                _detect_known_contacts, unique_prospects,
            )
            if known_contacts:
                known_contacts_warning = (
                    f"\n⚠️ {len(known_contacts)} contacts with existing conversations detected:\n"
                    + "\n".join(
                        f"  - {kc['name']} ({kc['message_count']} messages exchanged)"
                        for kc in known_contacts[:5]
                    )
                )
                if len(known_contacts) > 5:
                    known_contacts_warning += f"\n  ... and {len(known_contacts) - 5} more"
                known_contacts_warning += (
                    "\n\nTag contacts with 'do-not-automate' to exclude them: "
                    "contacts(action='tag', contact_id='...', tag='do-not-automate')"
                )
                logger.info("Known-contacts warning: %d contacts with prior conversations",
                            len(known_contacts))
        except Exception as e:
            logger.warning("Known-contacts detection failed (non-critical): %s", e)

    if not unique_prospects:
        if connections_only == "on":
            return (
                f"❌ No existing connections found matching \"{target_description}\".\n\n"
                f"All {len(all_prospects)} connections are already in other campaigns.\n\n"
                "Options:\n"
                "1. Drop connections_only to run standard cold outreach with invitations\n"
                "2. Use a broader target description to match more of your network\n"
                "3. Connect with target people first, then create a connections-only campaign"
            )
        return (
            "All found prospects are already in your campaigns or connections.\n\n"
            f"Searched for: \"{target_description}\"\n\n"
            "Try a different or broader target description to find new prospects."
        )

    # ── Step 5b (pre): Post-search filtering for Classic LinkedIn ──
    # Classic search drops seniority, company_headcount, etc.
    # Apply soft filtering here to remove obvious mismatches.
    if not use_sales_nav and segments:
        pre_count = len(unique_prospects)
        unique_prospects = _post_filter_classic_prospects(
            unique_prospects, segments, segment_index_map,
        )
        filtered_out = pre_count - len(unique_prospects)
        if filtered_out > 0:
            logger.info(
                "Post-search filter: removed %d/%d prospects (Classic LinkedIn)",
                filtered_out, pre_count,
            )

    if not unique_prospects:
        return (
            "All prospects were filtered out by ICP seniority/title matching.\n\n"
            f"Searched for: \"{target_description}\"\n\n"
            "Try broader targeting or adjust your ICP criteria."
        )

    # ── Step 5b: Score each prospect against campaign ICP ──
    from ..services.icp_match_scorer import compute_icp_match
    icp_json_for_scoring = icp  # Parsed dict with "segments" key

    # Connections-only: preliminary score → enrich top 50 → full score
    if connections_only == "on":
        # Preliminary score using headline-only data
        for prospect in unique_prospects:
            result = compute_icp_match(prospect, icp_json_for_scoring)
            prospect["_preliminary_score"] = result["icp_match_score"]
        unique_prospects.sort(key=lambda p: p.get("_preliminary_score", 0), reverse=True)

        # Enrich top 50 with full LinkedIn profiles for better scoring
        try:
            from ..services.connection_sync import enrich_prospects
            enriched_count = await enrich_prospects(
                client, account_id, unique_prospects[:50], max_enrich=50,
            )
            if enriched_count > 0:
                logger.info("Enriched %d connections with full profiles before scoring", enriched_count)
        except Exception as e:
            logger.warning("Connection enrichment failed (non-critical): %s", e)

    # Full ICP score (with enriched data for connections-only top candidates)
    for prospect in unique_prospects:
        result = compute_icp_match(prospect, icp_json_for_scoring)
        prospect["fit_score"] = result["icp_match_score"]

    # Sort by score, highest first
    unique_prospects.sort(key=lambda p: p.get("fit_score", 0), reverse=True)

    # Filter out prospects below minimum fit score threshold
    from ..constants import MIN_FIT_SCORE_THRESHOLD
    pre_filter_count = len(unique_prospects)
    unique_prospects = [p for p in unique_prospects if p.get("fit_score", 0) >= MIN_FIT_SCORE_THRESHOLD]
    low_score_filtered = pre_filter_count - len(unique_prospects)
    if low_score_filtered > 0:
        logger.info("Filtered %d prospects below fit_score threshold %.2f", low_score_filtered, MIN_FIT_SCORE_THRESHOLD)

    # Free tier: cap contacts
    max_contacts = FREE_MAX_CONTACTS_ANALYZED if tier != TIER_PRO else 1000
    prospects_to_save = unique_prospects[:max_contacts]

    # ── Step 6: Create campaign in DB ──
    final_name = campaign_name or icp.get("campaign_name", target_description[:40])

    # Build config — connections-only disables invitations + all warm-up
    is_connections_only = connections_only == "on"
    config = {
        "target_description": target_description,
        "prospect_count": len(prospects_to_save),
        "booking_link": "",
        "voice_mode": voice_mode,
        "voice_noise_type": DEFAULT_NOISE_TYPE,
        "voice_humanize": DEFAULT_VOICE_HUMANIZE,
        # Warm-up sequence toggles
        "enable_profile_views": not is_connections_only,
        "enable_follows": not is_connections_only,
        "enable_endorsements": not is_connections_only,
        "enable_engagements": not is_connections_only,
        "enable_followups": True,
        # Invitation toggle
        "enable_invitations": not is_connections_only,
        # Connections-only flag
        "connections_only": is_connections_only,
        # Engagement settings
        "engagement_mode": "auto",
        # Follow-up settings
        "max_followups": 5,
        "followup_delay_days": [1, 7, 14, 21, 28],
        # Invite settings
        "withdraw_stale_invites": True,
        "stale_invite_days": 21,
        "active_days": [0, 1, 2, 3, 4, 5, 6],
        # Search account routing
        "search_account_id": search_acct_id if search_acct_id != account_id else "",
    }

    # Build context_json — persist company_context so it flows to message prompts
    context = {}
    if company_context:
        context["offerings"] = company_context
        context["company_context_raw"] = company_context
    context_json = json.dumps(context) if context else ""

    campaign_id = await run_db(create_campaign, name=final_name,
        icp_json=json.dumps(icp),
        status=STATUS_ACTIVE,
        mode=mode,
        config_json=json.dumps(config),
        context_json=context_json,)

    # Save contacts + create outreach records
    _source = _internal_source or "linkedin_search"
    _source_detail = f"ICP: {target_description[:100]}"
    if _internal_source == "strategy_spawn":
        _source_detail = f"Auto-spawned: {target_description[:100]}"
    has_ab_test = bool( await run_db(list_ab_tests, campaign_id, status="running"))
    for prospect in prospects_to_save:
        contact_id = await run_db(save_contact, campaign_id=campaign_id,
            name=prospect.get("name", ""),
            title=prospect.get("title", ""),
            company=prospect.get("company", ""),
            linkedin_url=prospect.get("linkedin_url", ""),
            linkedin_id=prospect.get("public_id", ""),
            profile_json=json.dumps(prospect),
            fit_score=prospect.get("fit_score", 0.0),
            source=_source,
            source_detail=_source_detail,)
        variant = await run_db(assign_variant, campaign_id) if has_ab_test else None
        await run_db(create_outreach, campaign_id=campaign_id,
            contact_id=contact_id,
            status="pending",
            variant=variant,)

    # ── Step 6a-extra: Auto-create company watchlists from top prospect companies ──
    try:
        from collections import Counter as _Counter
        from ..db.signal_queries import list_watchlists as _list_wl, save_watchlist as _save_wl

        company_counts = _Counter(
            p.get("company", "").strip()
            for p in prospects_to_save
            if p.get("company", "").strip()
        )
        # Take top 5 companies (any count ≥1) — diverse campaigns often have 1 per company
        existing_wl = await run_db(_list_wl, is_active=True)
        existing_company_wls = [w for w in existing_wl if w.get("watch_type") == "company"]
        existing_company_kw = {
            kw.lower()
            for w in existing_company_wls
            for kw in (w.get("keywords_list") or [])
        }
        existing_company_names = {
            w.get("name", "").lower()
            for w in existing_company_wls
        }
        company_wl_created = 0
        for comp_name, count in company_counts.most_common(10):
            if company_wl_created >= 5:
                break
            comp_lower = comp_name.lower()
            # Dedup against both keywords and watchlist names
            if comp_lower in existing_company_kw or comp_lower in existing_company_names:
                continue
            _save_wl(
                name=comp_name,
                watch_type="company",
                keywords=[comp_name],
                campaign_id=campaign_id,
            )
            company_wl_created += 1
        if company_wl_created:
            logger.info("Auto-created %d company watchlists from prospect companies", company_wl_created)
    except Exception as e:
        logger.debug("Company watchlist auto-creation from contacts failed (non-fatal): %s", e)

    # ── Step 6b: Signal intelligence — watchlists + retroactive matching ──
    signal_summary_lines: list[str] = []
    try:
        from ..services.signal_linker import analyze_signal_coverage, scan_signal_pool_for_campaign
        from ..services.signal_service import create_watchlists_from_icp

        # Analyze what's already being monitored
        coverage = analyze_signal_coverage(icp)

        # Auto-create campaign-specific watchlists for missing topics
        wl_ids = create_watchlists_from_icp(
            icp_json=icp,
            campaign_id=campaign_id,
            icp_name=final_name,
        )

        if wl_ids or coverage["already_covered"] > 0:
            parts = []
            if coverage["already_covered"] > 0:
                parts.append(f"{coverage['already_covered']} topics already monitored")
            if wl_ids:
                parts.append(f"{len(wl_ids)} new watchlists created")
            signal_summary_lines.append(f"📡 Signal monitoring: {', '.join(parts)}")

        # Scan existing signal pool for hot leads matching this ICP
        match_result = scan_signal_pool_for_campaign(campaign_id, icp)
        if match_result["hot_leads_found"] > 0:
            signal_summary_lines.append(
                f"🔥 {match_result['hot_leads_found']} hot leads found from existing signals!"
            )
    except Exception as e:
        logger.debug("Signal intelligence setup failed (non-fatal): %s", e)

    # Track usage
    await run_db(increment_usage, "campaigns_created")

    # Auto-enable scheduler for autopilot campaigns
    scheduler_was_off = False
    cloud_was_off = False
    if mode == "autopilot" and not is_scheduler_enabled():
        set_scheduler_enabled(
            True,
            caller="auto_campaign",
            reason="Auto-enabled for new autopilot campaign",
        )
        scheduler_was_off = True
        logger.info("Auto-enabled scheduler for new autopilot campaign")

    # Auto-enable cloud scheduler for autopilot campaigns in backend mode
    if mode == "autopilot" and config_mod.is_backend_mode():
        try:
            from ..services.cloud_sync import toggle_cloud_scheduler
            result = await toggle_cloud_scheduler(enabled=True)
            if "enabled" in result.lower():
                cloud_was_off = True
                logger.info("Auto-enabled cloud scheduler for new autopilot campaign")
        except Exception as e:
            logger.warning(f"Cloud scheduler auto-enable failed (non-fatal): {e}")

    # ── Step 7: Format launch confirmation ──
    header = "🚀 Campaign Launched" if mode == "autopilot" else "✅ Campaign Created"
    output_lines = [
        f"{header}: **{final_name}**",
        f"📋 Campaign ID: `{campaign_id[:8]}...`",
        "",
    ]

    # ICP summary
    summary = icp.get("summary", target_description)
    if summary:
        output_lines.append(summary)
    if icp.get("relevance_hook"):
        output_lines.append(f"Hook: {icp['relevance_hook']}")
    if search_acct_id != account_id:
        output_lines.append("Searched via premium account (Sales Navigator)")
    elif use_sales_nav:
        output_lines.append("Searched with Sales Navigator")
    output_lines.append(f"{len(prospects_to_save)} prospects queued")
    if dedup_summary:
        output_lines.append(f"🔍 {dedup_summary}")
    if known_contacts_warning:
        output_lines.append(known_contacts_warning)
    if signal_summary_lines:
        for line in signal_summary_lines:
            output_lines.append(line)
    output_lines.append("")

    # Show top 5 prospects
    output_lines.append(f"Top prospects (of {len(prospects_to_save)}):")
    for i, p in enumerate(prospects_to_save[:5]):
        is_last = i == min(4, len(prospects_to_save) - 1)
        prefix = "└──" if is_last else "├──"
        name = p.get("name", "Unknown")
        title = p.get("title", "")
        company = p.get("company", "")
        score = p.get("fit_score", 0)
        star_rating = stars(score)

        role = f"{title}" if title else ""
        if company:
            role += f" at {company}" if role else company

        output_lines.append(f"{prefix} {i+1}. {name} — {role} (fit: {star_rating})")

    if len(prospects_to_save) > 5:
        output_lines.append(f"    ... and {len(prospects_to_save) - 5} more")

    # Mode-specific section
    if mode == "autopilot":
        output_lines.extend([
            "",
            "🤖 **Mode: Autopilot** — outreach runs automatically",
            "",
            "What happens next:",
            "├── 💬 Warm-up — engaging with prospect posts (25-40 min intervals)",
            "├── 🤝 Invitations — personalized connection requests after warm-up (20-40 min)",
            "├── 📩 Follow-ups — automatic DMs on days 1, 7, 14, 21, 28",
            "└── 📬 Reply detection — checked every 5 min, hot leads surfaced",
            "",
            "All messages pass a 5-stage validation pipeline and respect LinkedIn rate limits.",
        ])

        if scheduler_was_off:
            output_lines.append("⚡ Scheduler has been automatically enabled.")
        if cloud_was_off:
            output_lines.append("☁️ Cloud scheduler enabled — outreach runs 24/7, even when your laptop is off.")

        output_lines.extend([
            "",
            "Monitor anytime:",
            "├── show_status() — campaign dashboard",
            "├── check_replies() — see who responded",
            "├── campaign_report() — detailed analytics",
            "├── pause_campaign() — pause if needed",
            "└── edit_campaign(mode='copilot') — switch to manual review",
        ])
    else:
        # Copilot mode
        output_lines.extend([
            "",
            "📌 **Mode: Copilot** — you review each message before sending",
            "",
            "Ready to start? Say:",
            "├── \"send messages\" → generate_and_send",
            "├── \"show status\" → show_status",
            "└── edit_campaign(mode='autopilot') → switch to autonomous mode",
        ])

    # Voice mode info
    if voice_mode != "text_only":
        voice_label = {"mixed": "Mixed (alternating text & voice)", "voice_only": "Voice only", "ab_test": "A/B testing text vs voice"}.get(voice_mode, voice_mode)
        output_lines.extend(["", f"🎤 **Voice memos: {voice_label}** — edit_campaign(voice_mode='text_only') to disable"])

    # Nudge to add campaign context if missing (critical for message quality)
    if not company_context:
        output_lines.extend([
            "",
            "⚠️ **No company context set** — your messages will be generic without it.",
            "   Add these now for much better outreach quality:",
            "   → `edit_campaign(offerings='What you sell and the value you provide')`",
            "   → `edit_campaign(case_studies='Brief success story with numbers')`",
            "   → `edit_campaign(booking_link='https://cal.com/you/15min')`",
        ])

    if is_first_campaign:
        output_lines.extend([
            "",
            "🔍 **Prospects will check your profile before accepting** — run a quick brand audit",
            "   to make sure your LinkedIn profile converts visitors into connections:",
            "   → `brand_strategy(action='analyze')` — scores your headline, summary, and content",
            "",
            "💡 For your next campaign, keep using company_context for sharper ICPs and more relevant outreach.",
        ])

    if tier != TIER_PRO and len(unique_prospects) > max_contacts:
        output_lines.extend([
            "",
            f"💡 Found {len(unique_prospects)} total matches but free tier caps at {max_contacts}.",
            "   Upgrade to Pro ($29/mo) for unlimited contacts.",
        ])

    # ── Flag brand re-analysis with new ICP context ──
    try:
        from ..services.brand_service import load_brand_analysis
        if await run_db(load_brand_analysis):
            await run_db(save_setting, "brand_reanalyze_needed", True)
            logger.info("Flagged brand for ICP-driven re-analysis after campaign creation")
    except Exception as e:
        logger.debug("Brand re-analysis flag failed (non-fatal): %s", e)

    return "\n".join(output_lines)


def _icp_result_to_legacy(result: IcpResult, target_description: str) -> dict:
    """Convert an IcpResult to structured search segments preserving enriched codes.

    Each segment carries both human-readable fields AND enriched LinkedIn codes
    so the search can use structured Unipile filters instead of keyword-only.
    """
    segments = []
    for icp in result.icps:
        titles = icp.job_titles.include if icp.job_titles else []
        industries = icp.industries.include if icp.industries else []
        locations = icp.locations.include if icp.locations else []
        keywords_list = icp.keywords or []

        # Fallback keyword string (used when no enriched codes)
        keyword_parts = []
        if titles:
            keyword_parts.extend(titles[:2])
        if industries:
            keyword_parts.extend(industries[:2])
        if keywords_list:
            keyword_parts.extend(keywords_list[:3])

        # ── Extract enriched LinkedIn codes (from Phase 6 enrichment) ──
        enriched = icp.linkedin_enriched_params
        industry_codes: list[str] = []
        location_codes: list[str] = []
        title_codes: list[str] = []
        department_codes: list[str] = []

        if enriched:
            if enriched.industries and enriched.industries.include:
                industry_codes = [p.code for p in enriched.industries.include if p.code]
            if enriched.locations and enriched.locations.include:
                location_codes = [p.code for p in enriched.locations.include if p.code]
            if enriched.job_titles and enriched.job_titles.include:
                title_codes = [p.code for p in enriched.job_titles.include if p.code]
            if enriched.departments and enriched.departments.include:
                department_codes = [p.code for p in enriched.departments.include if p.code]

        # ── Structured parameters ──
        seniority_list = icp.seniority.include if icp.seniority else []

        headcount: dict[str, int] | None = None
        if icp.company_headcount and (icp.company_headcount.min or icp.company_headcount.max):
            headcount = {}
            if icp.company_headcount.min:
                headcount["min"] = icp.company_headcount.min
            if icp.company_headcount.max:
                headcount["max"] = icp.company_headcount.max

        tenure_param: dict[str, int] | None = None
        if icp.tenure and (icp.tenure.min or icp.tenure.max):
            tenure_param = {}
            if icp.tenure.min:
                tenure_param["min"] = icp.tenure.min
            if icp.tenure.max:
                tenure_param["max"] = icp.tenure.max

        company_types_list = icp.company_types or []
        has_structured = bool(industry_codes or location_codes or title_codes)

        if has_structured:
            logger.info(
                "Segment '%s': %d industry, %d location, %d title codes; seniority=%s",
                icp.name, len(industry_codes), len(location_codes),
                len(title_codes), seniority_list[:2] or "any",
            )

        segments.append({
            "name": icp.name or "Segment",
            "titles": titles,
            "keywords": ", ".join(keyword_parts) if keyword_parts else target_description,
            "industries": industries,
            "locations": locations,
            # Enriched LinkedIn codes for structured search
            "industry_codes": industry_codes,
            "location_codes": location_codes,
            "title_codes": title_codes,
            "department_codes": department_codes,
            # Structured parameters
            "seniority": seniority_list,
            "company_headcount": headcount,
            "company_types": company_types_list,
            "tenure": tenure_param,
            # Sales Navigator advanced filters
            "spotlight": icp.spotlight_filters,
            "boolean_keywords": icp.boolean_keywords or "",
            "annual_revenue": icp.annual_revenue,
            "company_headcount_growth": icp.company_headcount_growth or "",
            "has_structured": has_structured,
        })

    return {
        "segments": segments,
        "summary": result.summary or target_description,
        "campaign_name": result.campaign_name or target_description[:40],
        "relevance_hook": result.relevance_hook or "",
    }


def _detect_known_contacts(prospects: list[dict]) -> list[dict]:
    """Detect prospects with existing conversation history (>5 messages).

    Returns a list of dicts with name and message_count for prospects
    that have significant prior conversations.
    """
    from ..db.schema import get_db
    db = get_db()
    known = []
    for p in prospects:
        linkedin_id = (p.get("provider_id") or p.get("public_id") or "").strip()
        if not linkedin_id:
            continue
        row = db.execute(
            """SELECT gc.name, COUNT(m.id) as msg_count
               FROM global_contacts gc
               JOIN contacts c ON c.global_contact_id = gc.id
               JOIN outreaches o ON o.contact_id = c.id
               JOIN messages m ON m.outreach_id = o.id
               WHERE gc.linkedin_id = ?
               GROUP BY gc.id
               HAVING msg_count > 5""",
            (linkedin_id,),
        ).fetchone()
        if row:
            known.append({"name": row["name"], "message_count": row["msg_count"]})
    db.close()
    return known


def _post_filter_classic_prospects(
    prospects: list[dict],
    segments: list[dict],
    segment_map: dict[str, int],
) -> list[dict]:
    """Apply ICP criteria that Classic LinkedIn doesn't support as search filters.

    Classic search only uses industry + location as structured filters, dropping
    seniority, company_headcount, etc. This function applies soft title-based
    filtering to remove obvious mismatches (e.g., PhD students, interns when
    targeting VP-level sales leaders).
    """
    from ..constants import SENIORITY_KEYWORDS

    filtered = []
    for p in prospects:
        key = p.get("public_id") or p.get("linkedin_url") or p.get("name")
        seg_idx = segment_map.get(key, 0) if key else 0
        segment = segments[seg_idx] if seg_idx < len(segments) else {}

        # Seniority check: if ICP specifies seniority, check prospect title
        target_seniority = segment.get("seniority", [])
        if target_seniority:
            title = (p.get("title") or "").lower()
            if title and not _title_matches_seniority(title, target_seniority, SENIORITY_KEYWORDS):
                continue

        filtered.append(p)
    return filtered


def _title_matches_seniority(
    title: str,
    target_levels: list[str],
    seniority_keywords: dict[str, list[str]],
) -> bool:
    """Check if a prospect's title matches any of the target seniority levels."""
    for level in target_levels:
        level_lower = level.lower()
        keywords = seniority_keywords.get(level_lower, [])
        if any(kw in title for kw in keywords):
            return True
    return False
