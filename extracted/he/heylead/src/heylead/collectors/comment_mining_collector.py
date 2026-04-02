"""Collector: comment_mining_collector — Mine comments from competitor & industry posts.

Extracts leads from:
1. Competitor company post commenters (competitor_post_commenter)
2. High-engagement industry posts (industry_thread_participant)
3. Known prospects commenting on competitor posts (prospect_comments_on_competitor)

These are Tier 3 signals — higher effort but massive lead gen potential.
Each commenter is cross-referenced against campaign ICPs for relevance.

Runs every 2 hours via the scheduler (SIGNAL_COMMENT_MINING_SECONDS).
"""

from __future__ import annotations

import json
import logging
import time
from typing import Any

logger = logging.getLogger(__name__)


async def mine_post_comments() -> str:
    """Mine comments from competitor/industry posts for lead signals.

    Flow:
    1. Get competitor watchlists → fetch their recent posts
    2. For high-engagement posts (20+ comments), extract all commenters
    3. Cross-reference commenters against active ICPs
    4. Create signals for ICP-matching commenters
    5. Also check if known prospects are commenting on competitor posts

    Returns summary string.
    """
    from ..constants import (
        COMMENT_MINING_MAX_COMMENTERS_PER_POST,
        COMMENT_MINING_MAX_POSTS,
        COMMENT_MINING_MIN_COMMENTS,
        SIGNAL_COMPETITOR_POST_COMMENTER,
        SIGNAL_INDUSTRY_THREAD_PARTICIPANT,
        SIGNAL_PROSPECT_COMMENTS_ON_COMPETITOR,
        SIGNAL_TTL_COMPETITOR_POST_COMMENTER,
        SIGNAL_TTL_INDUSTRY_THREAD_PARTICIPANT,
        SIGNAL_TTL_PROSPECT_COMMENTS_ON_COMPETITOR,
    )
    from ..db.async_bridge import run_db
    from ..db.signal_queries import (
        get_contact_by_linkedin_id,
        list_watchlists,
        save_signal,
        signal_exists,
        upsert_signal_account,
    )
    from ..linkedin import get_account_id, get_linkedin_client

    account_id = get_account_id()
    if not account_id:
        return "No LinkedIn account connected — skipping comment mining."

    client = get_linkedin_client()
    now = int(time.time())

    # Get competitor and keyword watchlists
    watchlists = await run_db(list_watchlists, is_active=True)
    competitor_wls = [w for w in watchlists if w.get("watch_type") == "competitor"]
    keyword_wls = [w for w in watchlists if w.get("watch_type") == "keyword"]

    if not competitor_wls and not keyword_wls:
        return "No watchlists configured for comment mining."

    # Load ICP titles/industries for matching
    icp_matcher = await run_db(_load_icp_matcher)

    total_new = 0
    posts_mined = 0
    errors = 0

    try:
        # ── Phase 1: Mine competitor post comments ──
        for wl in competitor_wls[:5]:  # Max 5 competitor watchlists
            keywords_list = wl.get("keywords_list", [])
            campaign_id = wl.get("campaign_id")
            wl_name = wl.get("name", "")

            for keyword in keywords_list[:3]:  # Max 3 keywords per watchlist
                try:
                    results, _ = await client.search_posts(
                        account_id, keyword, limit=10,
                    )
                except Exception as e:
                    logger.debug("Competitor post search failed for '%s': %s", keyword, e)
                    errors += 1
                    continue

                # Filter to high-engagement posts
                viral_posts = [
                    p for p in results
                    if int(p.get("comments_count", 0) or 0) >= COMMENT_MINING_MIN_COMMENTS
                ]

                for post in viral_posts[:COMMENT_MINING_MAX_POSTS]:
                    post_id = post.get("post_id", "")
                    post_text = (post.get("text") or "")[:300]
                    comments_count = int(post.get("comments_count", 0) or 0)

                    if not post_id:
                        continue

                    # Skip if already mined (dedup by post_id + source)
                    mine_key = f"mine:{post_id}"
                    if await run_db(signal_exists, SIGNAL_COMPETITOR_POST_COMMENTER, post_id=mine_key):
                        continue

                    try:
                        comments = await client.get_post_comments(
                            account_id, post_id,
                            limit=COMMENT_MINING_MAX_COMMENTERS_PER_POST,
                        )
                    except Exception as e:
                        logger.debug("get_post_comments failed for %s: %s", post_id, e)
                        errors += 1
                        continue

                    posts_mined += 1

                    for comment in comments:
                        author_id = comment.get("author_id", "")
                        author_name = comment.get("author_name", "")
                        author_headline = comment.get("author_headline", "")
                        comment_text = comment.get("text", "")

                        if not author_id or author_id == "N/A":
                            continue

                        # Check if this is a known prospect
                        known_contact = await run_db(get_contact_by_linkedin_id, author_id)

                        if known_contact:
                            # Known prospect commenting on competitor → high-value signal
                            dedup_key = f"pcoc:{post_id}:{author_id}"
                            if not await run_db(
                                signal_exists,
                                SIGNAL_PROSPECT_COMMENTS_ON_COMPETITOR,
                                post_id=dedup_key,
                            ):
                                metadata = {
                                    "competitor_keyword": keyword,
                                    "post_text": post_text,
                                    "comment_text": comment_text[:200],
                                    "comments_on_post": comments_count,
                                    "contact_name": known_contact.get("name", ""),
                                    "contact_campaign_id": known_contact.get("campaign_id", ""),
                                }
                                await run_db(
                                    save_signal,
                                    signal_type=SIGNAL_PROSPECT_COMMENTS_ON_COMPETITOR,
                                    source="comment_mining",
                                    prospect_id=known_contact.get("id"),
                                    prospect_name=author_name,
                                    prospect_title=author_headline or known_contact.get("title"),
                                    linkedin_id=author_id,
                                    campaign_id=known_contact.get("campaign_id") or campaign_id,
                                    content=f"Commented on competitor post about '{keyword}': {comment_text[:200]}",
                                    post_id=dedup_key,
                                    metadata_json=json.dumps(metadata),
                                    expires_at=now + SIGNAL_TTL_PROSPECT_COMMENTS_ON_COMPETITOR,
                                )
                                await run_db(
                                    upsert_signal_account,
                                    linkedin_id=author_id,
                                    prospect_name=author_name,
                                )
                                total_new += 1
                        else:
                            # Unknown person — check ICP match
                            if not _matches_icp(author_headline, icp_matcher):
                                continue

                            dedup_key = f"cpc_mine:{post_id}:{author_id}"
                            if not await run_db(
                                signal_exists,
                                SIGNAL_COMPETITOR_POST_COMMENTER,
                                post_id=dedup_key,
                            ):
                                is_question = comment_text.strip().endswith("?")
                                metadata = {
                                    "competitor_keyword": keyword,
                                    "post_text": post_text,
                                    "comment_text": comment_text[:200],
                                    "author_headline": author_headline,
                                    "is_question": is_question,
                                    "comments_on_post": comments_count,
                                }
                                # Boost confidence for questions (stronger intent)
                                confidence = 0.60 if is_question else 0.45

                                await run_db(
                                    save_signal,
                                    signal_type=SIGNAL_COMPETITOR_POST_COMMENTER,
                                    source="comment_mining",
                                    prospect_name=author_name,
                                    prospect_title=author_headline,
                                    linkedin_id=author_id,
                                    campaign_id=campaign_id,
                                    content=f"Commented on competitor post: {comment_text[:300]}",
                                    post_id=dedup_key,
                                    metadata_json=json.dumps(metadata),
                                    expires_at=now + SIGNAL_TTL_COMPETITOR_POST_COMMENTER,
                                    confidence=confidence,
                                )
                                await run_db(
                                    upsert_signal_account,
                                    linkedin_id=author_id,
                                    prospect_name=author_name,
                                )
                                total_new += 1

                    # Mark this post as mined
                    await run_db(
                        save_signal,
                        signal_type=SIGNAL_COMPETITOR_POST_COMMENTER,
                        source="comment_mining_marker",
                        content=f"Post mined: {post_text[:100]}",
                        post_id=mine_key,
                        metadata_json=json.dumps({"mined_at": now, "comments_extracted": len(comments)}),
                        expires_at=now + (7 * 86400),  # Re-mine after 7 days
                    )

        # ── Phase 2: Mine industry keyword post comments ──
        for wl in keyword_wls[:3]:  # Max 3 keyword watchlists
            keywords_list = wl.get("keywords_list", [])
            campaign_id = wl.get("campaign_id")

            for keyword in keywords_list[:2]:  # Max 2 keywords per watchlist
                try:
                    results, _ = await client.search_posts(
                        account_id, keyword, limit=10,
                    )
                except Exception as e:
                    logger.debug("Industry post search failed for '%s': %s", keyword, e)
                    errors += 1
                    continue

                # Only mine very high-engagement posts for industry threads
                viral_posts = [
                    p for p in results
                    if int(p.get("comments_count", 0) or 0) >= COMMENT_MINING_MIN_COMMENTS * 2
                ]

                for post in viral_posts[:3]:  # Max 3 viral posts per keyword
                    post_id = post.get("post_id", "")
                    post_text = (post.get("text") or "")[:300]

                    if not post_id:
                        continue

                    mine_key = f"mine_ind:{post_id}"
                    if await run_db(signal_exists, SIGNAL_INDUSTRY_THREAD_PARTICIPANT, post_id=mine_key):
                        continue

                    try:
                        comments = await client.get_post_comments(
                            account_id, post_id,
                            limit=COMMENT_MINING_MAX_COMMENTERS_PER_POST,
                        )
                    except Exception as e:
                        logger.debug("get_post_comments failed for industry post %s: %s", post_id, e)
                        errors += 1
                        continue

                    posts_mined += 1

                    for comment in comments:
                        author_id = comment.get("author_id", "")
                        author_name = comment.get("author_name", "")
                        author_headline = comment.get("author_headline", "")
                        comment_text = comment.get("text", "")

                        if not author_id or author_id == "N/A":
                            continue

                        # Check ICP match
                        if not _matches_icp(author_headline, icp_matcher):
                            continue

                        dedup_key = f"itp:{post_id}:{author_id}"
                        if await run_db(signal_exists, SIGNAL_INDUSTRY_THREAD_PARTICIPANT, post_id=dedup_key):
                            continue

                        is_question = comment_text.strip().endswith("?")
                        metadata = {
                            "industry_keyword": keyword,
                            "post_text": post_text,
                            "comment_text": comment_text[:200],
                            "author_headline": author_headline,
                            "is_question": is_question,
                        }

                        confidence = 0.55 if is_question else 0.40

                        await run_db(
                            save_signal,
                            signal_type=SIGNAL_INDUSTRY_THREAD_PARTICIPANT,
                            source="comment_mining",
                            prospect_name=author_name,
                            prospect_title=author_headline,
                            linkedin_id=author_id,
                            campaign_id=campaign_id,
                            content=f"Active in industry thread about '{keyword}': {comment_text[:300]}",
                            post_id=dedup_key,
                            metadata_json=json.dumps(metadata),
                            expires_at=now + SIGNAL_TTL_INDUSTRY_THREAD_PARTICIPANT,
                            confidence=confidence,
                        )
                        await run_db(
                            upsert_signal_account,
                            linkedin_id=author_id,
                            prospect_name=author_name,
                        )
                        total_new += 1

                    # Mark as mined
                    await run_db(
                        save_signal,
                        signal_type=SIGNAL_INDUSTRY_THREAD_PARTICIPANT,
                        source="comment_mining_marker",
                        content=f"Industry post mined: {post_text[:100]}",
                        post_id=mine_key,
                        metadata_json=json.dumps({"mined_at": now}),
                        expires_at=now + (7 * 86400),
                    )

    finally:
        await client.close()

    summary = (
        f"Comment mining: {posts_mined} posts mined, "
        f"{total_new} new signals created"
    )
    if errors:
        summary += f", {errors} errors"
    logger.info(summary)
    return summary


def _load_icp_matcher() -> dict[str, Any]:
    """Load ICP data for lightweight headline matching."""
    from ..db.queries import list_icps

    matcher: dict[str, Any] = {
        "titles": set(),
        "industries": set(),
        "seniority_keywords": {
            "vp", "vice president", "director", "head of", "chief",
            "cto", "cmo", "cro", "coo", "cfo", "ceo", "founder",
            "co-founder", "partner", "lead", "manager", "senior",
            "principal", "svp", "evp",
        },
    }

    for icp_row in list_icps(status="active"):
        icp_json_str = icp_row.get("icp_json", "{}")
        try:
            parsed = json.loads(icp_json_str) if isinstance(icp_json_str, str) else icp_json_str
        except (json.JSONDecodeError, TypeError):
            continue

        for sub_icp in (parsed.get("icps", [parsed]) if parsed else []):
            # Extract job titles
            jt = sub_icp.get("job_titles", {})
            titles = jt.get("include", []) if isinstance(jt, dict) else (jt if isinstance(jt, list) else [])
            for title in titles:
                matcher["titles"].add(str(title).lower())

            # Extract industries
            ind = sub_icp.get("industries", {})
            industries = ind.get("include", []) if isinstance(ind, dict) else (ind if isinstance(ind, list) else [])
            for industry in industries:
                matcher["industries"].add(str(industry).lower())

    return matcher


def _matches_icp(headline: str, matcher: dict[str, Any]) -> bool:
    """Lightweight ICP match: check if headline contains ICP job titles or seniority keywords."""
    if not headline:
        return False

    headline_lower = headline.lower()

    # Check seniority keywords (fast filter — must have some seniority indicator)
    has_seniority = any(kw in headline_lower for kw in matcher.get("seniority_keywords", set()))
    if not has_seniority:
        return False

    # Check ICP title match (at least partial)
    titles = matcher.get("titles", set())
    if titles:
        for title in titles:
            if title in headline_lower:
                return True

    # If no specific titles to match but has seniority, accept
    if not titles:
        return True

    return False
