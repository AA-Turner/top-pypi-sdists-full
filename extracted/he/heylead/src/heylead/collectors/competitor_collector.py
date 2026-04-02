"""Competitor mention signal collector — monitors LinkedIn posts mentioning competitors.

Polls `search_posts()` for each competitor name in watchlists where
`watch_type='competitor'`. Cross-references post authors against campaign
contacts and ICPs. Signals competitor mentions that indicate evaluation
or switching intent — a high-value buying signal.

Runs every 30 minutes via the scheduler (shares budget with keyword collector).
"""

from __future__ import annotations

import json
import logging
import time
from typing import Any

logger = logging.getLogger(__name__)


async def collect_competitor_signals() -> str:
    """Collect signals from LinkedIn posts mentioning competitors.

    Iterates competitor watchlists and searches for each competitor name.
    Deduplicates against existing signals. Cross-references authors against
    campaign contacts for higher-value signals.

    Returns summary string.
    """
    from ..constants import (
        SIGNAL_COMPETITOR_MENTION,
        SIGNAL_DAILY_KEYWORD_SEARCHES,
        SIGNAL_TTL_COMPETITOR_MENTION,
    )
    from ..db.async_bridge import run_db
    from ..db.signal_queries import (
        get_contact_by_linkedin_id,
        get_daily_signal_search_count,
        list_watchlists,
        save_signal,
        signal_exists,
        update_watchlist,
        upsert_signal_account,
    )
    from ..linkedin import UnipileError, get_account_id, get_linkedin_client

    account_id = get_account_id()
    if not account_id:
        return "No LinkedIn account connected."

    # Check daily rate limit (shared budget with keyword collector)
    daily_count = await run_db(get_daily_signal_search_count, "keyword")
    if daily_count >= SIGNAL_DAILY_KEYWORD_SEARCHES:
        return f"Daily search limit reached ({daily_count}/{SIGNAL_DAILY_KEYWORD_SEARCHES})."

    # Get competitor watchlists only
    watchlists = await run_db(list_watchlists, is_active=True, watch_type="competitor")
    if not watchlists:
        return "No active competitor watchlists."

    try:
        client = get_linkedin_client()
    except UnipileError as e:
        return f"LinkedIn client error: {e}"

    total_new = 0
    total_searched = 0
    errors = 0
    now = int(time.time())

    try:
        for wl in watchlists:
            if daily_count + total_searched >= SIGNAL_DAILY_KEYWORD_SEARCHES:
                break

            wl_id = wl["id"]
            keywords_list = wl.get("keywords_list", [])
            campaign_id = wl.get("campaign_id")
            wl_name = wl.get("name", "")

            for competitor_name in keywords_list:
                if daily_count + total_searched >= SIGNAL_DAILY_KEYWORD_SEARCHES:
                    break

                if not competitor_name or not competitor_name.strip():
                    continue

                try:
                    posts, _ = await client.search_posts(
                        account_id, competitor_name.strip(), limit=25
                    )
                    total_searched += 1

                    for post in posts:
                        post_id = post.get("post_id", "")
                        post_text = post.get("text", "")
                        author_id = post.get("author_id", "")
                        author_name = post.get("author_name", "")
                        author_headline = post.get("author_headline", "")

                        if not post_id or not post_text:
                            continue

                        # Dedup
                        if await run_db(
                            signal_exists,
                            SIGNAL_COMPETITOR_MENTION, post_id=post_id
                        ):
                            continue

                        # Analyze mention context
                        mention_context = _analyze_competitor_mention(
                            post_text, competitor_name
                        )

                        # Cross-reference author against contacts
                        linked_prospect_id = None
                        linked_campaign_id = campaign_id
                        is_known_contact = False
                        if author_id:
                            contact = await run_db(get_contact_by_linkedin_id, author_id)
                            if contact:
                                linked_prospect_id = contact["id"]
                                linked_campaign_id = (
                                    linked_campaign_id
                                    or contact.get("campaign_id")
                                )
                                is_known_contact = True

                        # Build metadata
                        metadata = {
                            "competitor_name": competitor_name,
                            "watchlist_id": wl_id,
                            "watchlist_name": wl_name,
                            "mention_context": mention_context,
                            "is_known_contact": is_known_contact,
                            "author_headline": author_headline,
                            "author_url": post.get("author_url", ""),
                            "reactions_count": post.get("reactions_count", 0),
                            "comments_count": post.get("comments_count", 0),
                            "timestamp": post.get("timestamp", ""),
                        }

                        await run_db(
                            save_signal,
                            signal_type=SIGNAL_COMPETITOR_MENTION,
                            source="competitor_search",
                            prospect_name=author_name or None,
                            prospect_title=author_headline or None,
                            linkedin_id=author_id or None,
                            prospect_id=linked_prospect_id,
                            campaign_id=linked_campaign_id,
                            content=post_text[:1000],
                            post_id=post_id,
                            metadata_json=json.dumps(metadata),
                            expires_at=now + SIGNAL_TTL_COMPETITOR_MENTION,
                        )
                        total_new += 1

                        # Update signal account
                        if author_id:
                            await run_db(
                                upsert_signal_account,
                                linkedin_id=author_id,
                                prospect_name=author_name or None,
                            )

                except Exception as e:
                    logger.warning(
                        "Competitor search failed for '%s': %s",
                        competitor_name,
                        e,
                    )
                    errors += 1

            # Update last polled timestamp
            await run_db(update_watchlist, wl_id, last_polled_at=now)

    finally:
        await client.close()

    summary = (
        f"Searched {total_searched} competitor terms, "
        f"found {total_new} new signals"
    )
    if errors:
        summary += f", {errors} errors"
    return summary


def _analyze_competitor_mention(post_text: str, competitor_name: str) -> str:
    """Analyze the context of a competitor mention in a post.

    Returns a brief context classification:
    - 'switching_from': Post mentions leaving/replacing the competitor
    - 'evaluating': Post mentions comparing/evaluating competitors
    - 'complaint': Post contains negative sentiment about competitor
    - 'recommendation': Post recommends the competitor (less valuable)
    - 'general': Neutral mention
    """
    text_lower = post_text.lower()
    comp_lower = competitor_name.lower()

    # Switching signals
    switching_phrases = [
        f"switching from {comp_lower}",
        f"replacing {comp_lower}",
        f"moving away from {comp_lower}",
        f"left {comp_lower}",
        f"leaving {comp_lower}",
        f"migrating from {comp_lower}",
        f"ditching {comp_lower}",
        f"dropped {comp_lower}",
        f"cancelled {comp_lower}",
        f"canceled {comp_lower}",
        "looking for alternatives",
        "looking for an alternative",
        "need a replacement",
    ]
    if any(phrase in text_lower for phrase in switching_phrases):
        return "switching_from"

    # Evaluation signals
    eval_phrases = [
        f"{comp_lower} vs",
        f"vs {comp_lower}",
        f"compared to {comp_lower}",
        f"alternative to {comp_lower}",
        f"alternatives to {comp_lower}",
        f"better than {comp_lower}",
        f"instead of {comp_lower}",
        "which tool",
        "which platform",
        "evaluating",
        "comparing",
        "shopping for",
    ]
    if any(phrase in text_lower for phrase in eval_phrases):
        return "evaluating"

    # Complaint signals
    complaint_phrases = [
        f"frustrated with {comp_lower}",
        f"disappointed with {comp_lower}",
        f"hate {comp_lower}",
        f"problem with {comp_lower}",
        f"issues with {comp_lower}",
        f"broken {comp_lower}",
        f"{comp_lower} is terrible",
        f"{comp_lower} sucks",
        f"{comp_lower} doesn't work",
        f"{comp_lower} is too expensive",
        f"{comp_lower} pricing",
    ]
    if any(phrase in text_lower for phrase in complaint_phrases):
        return "complaint"

    # Recommendation (less valuable — they like the competitor)
    rec_phrases = [
        f"love {comp_lower}",
        f"recommend {comp_lower}",
        f"{comp_lower} is amazing",
        f"{comp_lower} is great",
        f"use {comp_lower}",
        f"switched to {comp_lower}",
    ]
    if any(phrase in text_lower for phrase in rec_phrases):
        return "recommendation"

    return "general"
