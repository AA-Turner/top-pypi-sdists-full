"""Collector: prospect_post_collector — Scan campaign contacts' recent posts for signals.

Iterates active campaigns, fetches contacts' recent posts via get_user_posts(),
and saves them as SIGNAL_PROSPECT_POST signals for classification.
"""

from __future__ import annotations

import json
import logging
import time
from typing import Any

from ..constants import (
    SIGNAL_PROSPECT_POST,
    SIGNAL_PROSPECT_SCAN_BATCH,
    SIGNAL_PROSPECT_POST_LOOKBACK_DAYS,
    SIGNAL_TTL_PROSPECT_POST,
)
from ..db.async_bridge import run_db
from ..db.queries import get_contacts_for_campaign, list_campaigns
from ..db.post_queries import upsert_post
from ..db.signal_queries import (
    save_signal,
    signal_exists,
    upsert_signal_account,
)

logger = logging.getLogger(__name__)


async def collect_prospect_posts() -> str:
    """Scan campaign contacts' recent posts and save as signals.

    Flow:
    1. Get all active campaigns
    2. For each campaign, get contacts with linkedin_id
    3. Skip contacts scanned recently (< SIGNAL_PROSPECT_SCAN_SECONDS ago)
    4. Fetch recent posts via get_user_posts()
    5. Deduplicate by post_id
    6. Save as SIGNAL_PROSPECT_POST signals (status='new', for later classification)
    7. Update contact's last_scanned_at

    Returns:
        Summary string of results.
    """
    from ..linkedin import get_account_id, get_linkedin_client

    account_id = get_account_id()
    if not account_id:
        return "No LinkedIn account connected — skipping prospect post scan."

    # Get active campaigns
    campaigns = await run_db(list_campaigns, status="active")
    if not campaigns:
        return "No active campaigns — skipping prospect post scan."

    client = get_linkedin_client()
    total_signals = 0
    total_contacts_scanned = 0
    errors = 0

    try:
        now = int(time.time())
        lookback_cutoff = now - (SIGNAL_PROSPECT_POST_LOOKBACK_DAYS * 86400)
        # Scan interval — re-scan contacts every 4 hours
        rescan_seconds = 4 * 3600
        scan_cutoff = now - rescan_seconds

        for campaign in campaigns:
            campaign_id = campaign.get("id", "")
            if not campaign_id:
                continue

            # Get contacts with linkedin_id
            contacts = await run_db(get_contacts_for_campaign, campaign_id)
            scannable = [
                c for c in contacts
                if c.get("linkedin_id")
                and (not c.get("last_scanned_at") or c["last_scanned_at"] < scan_cutoff)
            ]

            if not scannable:
                continue

            # Limit batch size
            batch = scannable[:SIGNAL_PROSPECT_SCAN_BATCH]

            for contact in batch:
                if total_contacts_scanned >= SIGNAL_PROSPECT_SCAN_BATCH:
                    break

                linkedin_id = contact["linkedin_id"]
                contact_id = contact.get("id", "")
                contact_name = contact.get("name", "Unknown")
                contact_title = contact.get("title", "")

                try:
                    posts = await client.get_user_posts(
                        account_id, linkedin_id, limit=5,
                    )

                    # Detect 422 sentinel
                    if posts and isinstance(posts[0], dict) and "_status_code" in posts[0]:
                        logger.info(
                            "get_user_posts returned %s for %s — skipping",
                            posts[0].get("_status_code"), contact_name,
                        )
                        await run_db(_update_last_scanned, contact_id, now)
                        total_contacts_scanned += 1
                        continue

                    if not posts:
                        await run_db(_update_last_scanned, contact_id, now)
                        total_contacts_scanned += 1
                        continue

                    for post in posts:
                        post_id = post.get("id", "")
                        post_text = post.get("text", "")
                        post_date = post.get("date", "")

                        if not post_text or not post_id:
                            continue

                        # Skip posts older than lookback window
                        post_ts = _parse_post_date(post_date)
                        if post_ts and post_ts < lookback_cutoff:
                            continue

                        # Deduplicate
                        if await run_db(signal_exists, SIGNAL_PROSPECT_POST, post_id=post_id):
                            continue

                        # Extract expanded fields from post
                        metrics = post.get("metrics", {})
                        impressions = int(
                            metrics.get("impressions_count", 0)
                            or metrics.get("impressions_counter", 0)
                            or 0
                        )
                        reposts = int(
                            metrics.get("reposts_count", 0)
                            or metrics.get("repost_counter", 0)
                            or 0
                        )
                        is_repost = 1 if post.get("is_repost") else 0
                        visibility = post.get("visibility", "")
                        media_type = post.get("media_type", "")

                        # Persist post + author to posts/post_authors tables
                        await run_db(
                            upsert_post,
                            post_id,
                            author_linkedin_id=linkedin_id,
                            author_name=contact_name,
                            text=post_text[:2000],
                            metrics_json=json.dumps(metrics),
                            source="prospect_scan",
                            impressions_count=impressions,
                            reposts_count=reposts,
                            is_repost=is_repost,
                            visibility=visibility,
                            media_type=media_type,
                        )

                        # Save signal (always created with status='new' for later LLM classification)
                        expires_at = now + SIGNAL_TTL_PROSPECT_POST
                        await run_db(
                            save_signal,
                            signal_type=SIGNAL_PROSPECT_POST,
                            source="prospect_scan",
                            prospect_id=contact_id,
                            prospect_name=contact_name,
                            prospect_title=contact_title,
                            linkedin_id=linkedin_id,
                            campaign_id=campaign_id,
                            content=post_text[:2000],
                            post_id=post_id,
                            metadata_json=json.dumps({
                                "post_date": post_date,
                                "metrics": metrics,
                                "contact_company": contact.get("company", ""),
                                "impressions_count": impressions,
                                "reposts_count": reposts,
                                "is_repost": bool(is_repost),
                                "visibility": visibility,
                                "media_type": media_type,
                            }),
                            expires_at=expires_at,
                        )
                        total_signals += 1

                        # Update signal account aggregation
                        await run_db(
                            upsert_signal_account,
                            linkedin_id=linkedin_id,
                            prospect_name=contact_name,
                            company=contact.get("company", ""),
                        )

                    await run_db(_update_last_scanned, contact_id, now)
                    total_contacts_scanned += 1

                except Exception as e:
                    logger.warning(
                        "Error scanning posts for %s: %s", contact_name, e,
                    )
                    errors += 1

    finally:
        await client.close()

    summary = (
        f"Prospect post scan complete: {total_contacts_scanned} contacts scanned, "
        f"{total_signals} new signals found"
    )
    if errors:
        summary += f", {errors} errors"
    logger.info(summary)
    return summary


def _update_last_scanned(contact_id: str, timestamp: int) -> None:
    """Update the contact's last_scanned_at timestamp."""
    from ..db.queries import get_db

    if not contact_id:
        return
    db = get_db()
    try:
        db.execute(
            "UPDATE contacts SET last_scanned_at = ? WHERE id = ?",
            (timestamp, contact_id),
        )
        db.commit()
    except Exception as e:
        logger.warning("Failed to update last_scanned_at for %s: %s", contact_id, e)
    finally:
        db.close()


def _parse_post_date(date_str: str) -> int | None:
    """Try to parse a post date string to a Unix timestamp.

    Handles ISO format, Unix timestamp strings, and common date formats.
    Returns None if parsing fails.
    """
    if not date_str:
        return None

    # Already a Unix timestamp?
    try:
        ts = int(date_str)
        if ts > 1_000_000_000:  # Reasonable Unix timestamp
            return ts
    except (ValueError, TypeError):
        pass

    # Try ISO format
    import datetime

    for fmt in (
        "%Y-%m-%dT%H:%M:%S.%fZ",
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%dT%H:%M:%S%z",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d",
    ):
        try:
            dt = datetime.datetime.strptime(date_str, fmt)
            return int(dt.timestamp())
        except ValueError:
            continue

    return None
