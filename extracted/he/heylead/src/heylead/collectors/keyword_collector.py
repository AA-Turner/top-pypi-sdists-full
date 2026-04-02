"""Keyword signal collector — monitors LinkedIn posts for watchlist keywords.

Distributes searches across all pool accounts for maximum throughput
(50 searches/account/day = 500/day with 10 accounts). Supports cursor-based
pagination to fetch up to 3 pages per keyword search (75 results vs 25).

Runs every 30 minutes via the scheduler.
"""

from __future__ import annotations

import json
import logging
import time
from typing import Any

logger = logging.getLogger(__name__)


async def collect_keyword_signals() -> str:
    """Collect signals from LinkedIn post searches for all active watchlists.

    Distributes keyword searches across pool accounts (round-robin).
    Each account has its own daily budget of DISTRIBUTED_SEARCH_PER_ACCOUNT_DAILY.
    Fetches up to KEYWORD_SEARCH_MAX_PAGES pages per keyword for deeper results.

    For each active watchlist:
    1. Search LinkedIn posts using watchlist keywords (multi-account, paginated)
    2. Deduplicate against existing signals (same post_id + signal_type)
    3. Store posts in posts table for analysis
    4. Cross-reference post authors against campaign contacts
    5. Save new signals with watchlist_id tracking

    Returns summary string.
    """
    from ..constants import (
        DISTRIBUTED_SEARCH_PER_ACCOUNT_DAILY,
        KEYWORD_SEARCH_MAX_PAGES,
        SIGNAL_COMPETITOR_MENTION,
        SIGNAL_DAILY_KEYWORD_SEARCHES,
        SIGNAL_KEYWORD_MENTION,
        SIGNAL_TTL_COMPETITOR_MENTION,
        SIGNAL_TTL_KEYWORD_MENTION,
    )
    from ..db.async_bridge import run_db
    from ..db.post_queries import upsert_post
    from ..db.signal_queries import (
        batch_get_contacts_by_linkedin_ids,
        batch_signal_exists,
        get_daily_signal_search_count,
        list_watchlists,
        save_signal,
        update_watchlist,
        upsert_signal_account,
    )
    from ..linkedin import UnipileError, get_account_id, get_linkedin_client

    account_id = get_account_id()
    if not account_id:
        return "No LinkedIn account connected."

    # Get active watchlists
    watchlists = await run_db(list_watchlists, is_active=True)
    if not watchlists:
        return "No active watchlists configured."

    try:
        client = get_linkedin_client()
    except UnipileError as e:
        return f"LinkedIn client error: {e}"

    # Get pool accounts for distributed searching
    accounts = await _get_pool_accounts(client, account_id)
    num_accounts = len(accounts)

    # Total daily budget = per-account limit × number of accounts
    total_daily_budget = DISTRIBUTED_SEARCH_PER_ACCOUNT_DAILY * num_accounts

    # Check how many searches we've already done today (rough global check)
    daily_count = await run_db(get_daily_signal_search_count, "keyword")
    if daily_count >= total_daily_budget:
        await client.close()
        return (
            f"Daily keyword search limit reached "
            f"({daily_count}/{total_daily_budget} across {num_accounts} accounts)."
        )

    # Build flat list of (keyword, watchlist) pairs, filtering disabled keywords
    search_queue: list[tuple[str, dict]] = []
    for wl in watchlists:
        keywords_list = wl.get("keywords_list", [])
        disabled = set()
        try:
            disabled = set(json.loads(wl.get("disabled_keywords", "[]") or "[]"))
        except (json.JSONDecodeError, TypeError):
            pass
        for kw in keywords_list:
            if kw not in disabled:
                search_queue.append((kw, wl))

    if not search_queue:
        await client.close()
        return "No keywords to search (all disabled or no watchlists)."

    total_new = 0
    total_searched = 0
    total_posts_stored = 0
    errors = 0
    now = int(time.time())
    remaining = total_daily_budget - daily_count

    # Track per-account search counts for this run
    account_searches: dict[str, int] = {aid: 0 for aid in accounts}

    for i, (keyword, wl) in enumerate(search_queue):
        if total_searched >= remaining:
            break

        # Round-robin assign to account
        acct_id = accounts[i % num_accounts]
        if account_searches[acct_id] >= DISTRIBUTED_SEARCH_PER_ACCOUNT_DAILY:
            # This account is exhausted, try next available
            acct_id = _next_available_account(
                accounts, account_searches, DISTRIBUTED_SEARCH_PER_ACCOUNT_DAILY,
            )
            if not acct_id:
                break  # All accounts exhausted

        wl_id = wl["id"]
        watch_type = wl.get("watch_type", "keyword")
        campaign_id = wl.get("campaign_id")

        signal_type = (
            SIGNAL_COMPETITOR_MENTION if watch_type == "competitor"
            else SIGNAL_KEYWORD_MENTION
        )
        ttl = (
            SIGNAL_TTL_COMPETITOR_MENTION if watch_type == "competitor"
            else SIGNAL_TTL_KEYWORD_MENTION
        )

        try:
            # Paginated search — fetch up to KEYWORD_SEARCH_MAX_PAGES pages
            all_posts = await _search_keyword_paginated(
                client, acct_id, keyword, max_pages=KEYWORD_SEARCH_MAX_PAGES,
            )
            account_searches[acct_id] += 1
            total_searched += 1

            # Batch dedup: pre-fetch existing signals and contacts
            valid_posts = [p for p in all_posts if p.get("post_id") and p.get("text")]
            all_post_ids = [p["post_id"] for p in valid_posts]
            existing_signals = await run_db(batch_signal_exists, signal_type, post_ids=all_post_ids)
            all_author_ids = [p.get("author_id", "") for p in valid_posts if p.get("author_id")]
            contacts_by_lid = await run_db(batch_get_contacts_by_linkedin_ids, all_author_ids) if all_author_ids else {}

            for post in valid_posts:
                post_id = post.get("post_id", "")
                post_text = post.get("text", "")
                author_id = post.get("author_id", "")
                author_name = post.get("author_name", "")
                author_headline = post.get("author_headline", "")

                # Store post in posts table for analysis (with expanded fields)
                impressions = int(post.get("impressions_count") or 0)
                reposts = int(post.get("reposts_count") or 0)
                await run_db(
                    upsert_post,
                    post_id,
                    author_linkedin_id=author_id,
                    author_name=author_name,
                    text=post_text[:2000],
                    metrics_json=json.dumps({
                        "reactions_count": post.get("reactions_count", 0),
                        "comments_count": post.get("comments_count", 0),
                        "impressions_count": impressions,
                        "reposts_count": reposts,
                    }),
                    source="keyword_search",
                    visibility=post.get("visibility", ""),
                    media_type=post.get("media_type", ""),
                    is_repost=1 if post.get("is_repost") else 0,
                    impressions_count=impressions,
                    reposts_count=reposts,
                )
                total_posts_stored += 1

                # Dedup: skip signal if we already have one for this post
                if post_id in existing_signals:
                    continue

                # Cross-reference: check if author is a campaign contact
                linked_prospect_id = None
                linked_campaign_id = campaign_id
                if author_id:
                    contact = contacts_by_lid.get(author_id)
                    if contact:
                        linked_prospect_id = contact["id"]
                        linked_campaign_id = (
                            linked_campaign_id or contact.get("campaign_id")
                        )

                # Build metadata (with expanded fields)
                metadata = {
                    "keyword": keyword,
                    "watchlist_id": wl_id,
                    "watchlist_name": wl.get("name", ""),
                    "watch_type": watch_type,
                    "author_headline": author_headline,
                    "author_url": post.get("author_url", ""),
                    "reactions_count": post.get("reactions_count", 0),
                    "comments_count": post.get("comments_count", 0),
                    "impressions_count": impressions,
                    "reposts_count": reposts,
                    "timestamp": post.get("timestamp", ""),
                    "account_id": acct_id[:8],
                    "media_type": post.get("media_type", "text"),
                    "is_repost": bool(post.get("is_repost")),
                    "share_url": post.get("share_url", ""),
                }
                if linked_prospect_id:
                    metadata["matched_contact"] = True

                await run_db(
                    save_signal,
                    signal_type=signal_type,
                    source="keyword_search",
                    prospect_name=author_name or None,
                    prospect_title=author_headline or None,
                    linkedin_id=author_id or None,
                    prospect_id=linked_prospect_id,
                    campaign_id=linked_campaign_id,
                    content=post_text[:1000],
                    post_id=post_id,
                    metadata_json=json.dumps(metadata),
                    expires_at=now + ttl,
                    watchlist_id=wl_id,
                )
                total_new += 1

                if author_id:
                    await run_db(
                        upsert_signal_account,
                        linkedin_id=author_id,
                        prospect_name=author_name or None,
                    )

        except Exception as e:
            logger.warning(
                "Keyword search failed for '%s' via account %s: %s",
                keyword, acct_id[:8], e,
            )
            errors += 1

        # Update last polled timestamp
        await run_db(update_watchlist, wl_id, last_polled_at=now)

    await client.close()

    summary = (
        f"Searched {total_searched} keywords across {num_accounts} accounts, "
        f"found {total_new} new signals, stored {total_posts_stored} posts"
    )
    if errors:
        summary += f", {errors} errors"
    return summary


# ──────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────


async def _get_pool_accounts(client: Any, fallback_account_id: str) -> list[str]:
    """Get list of account IDs to use for searching."""
    try:
        status = await client.network_pool_status()
        if status and "accounts" in status:
            healthy = [
                a["account_id"] for a in status["accounts"]
                if a.get("health_status") == "healthy" and a.get("account_id")
            ]
            if healthy:
                return healthy
    except Exception:
        pass
    return [fallback_account_id]


async def _search_keyword_paginated(
    client: Any,
    account_id: str,
    keyword: str,
    max_pages: int = 3,
) -> list[dict]:
    """Search posts with cursor-based pagination for deeper results."""
    all_posts: list[dict] = []
    cursor = None

    for page in range(max_pages):
        try:
            results, next_cursor = await client.search_posts(
                account_id, keyword, limit=25, cursor=cursor,
            )
            all_posts.extend(results)

            if not next_cursor or not results:
                break
            cursor = next_cursor
        except Exception as e:
            if page == 0:
                raise  # First page failure is fatal
            logger.debug("Pagination stopped at page %d for '%s': %s", page, keyword, e)
            break

    return all_posts


def _next_available_account(
    accounts: list[str],
    account_searches: dict[str, int],
    per_account_limit: int,
) -> str | None:
    """Find the next account that hasn't hit its daily limit."""
    for aid in accounts:
        if account_searches.get(aid, 0) < per_account_limit:
            return aid
    return None
