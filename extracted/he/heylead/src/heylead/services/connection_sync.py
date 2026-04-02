"""Connection sync service — persist 1st-degree LinkedIn connections locally.

Fetches connections from Unipile's relations API and stores them in the local
SQLite `connections` table so we can do fast set-based dedup without hitting
the API every time. Also provides helpers to check/mark individual connections.

Key functions:
- sync_connections(): Full sync from Unipile → local DB
- get_local_connection_ids(): Fast set of provider_id + public_id from local DB
- is_first_degree(): Quick single-row check
- mark_connected(): Record a newly connected prospect
- get_sync_age(): Seconds since last sync
- audit_campaign_connections(): Batch audit for existing campaigns
"""

from __future__ import annotations

import logging
import time
import uuid
from typing import Any

from ..db.async_bridge import run_db
from ..db.schema import get_db

logger = logging.getLogger(__name__)

# Re-sync if local data is older than this (1 hour) — used by ensure_synced() for dedup
SYNC_STALE_SECONDS = 3600
# Full sync stale threshold (24 hours) — used for my_connections search
FULL_SYNC_STALE_SECONDS = 86400


async def sync_connections(
    client: Any,
    account_id: str,
    max_relations: int = 20000,
    force: bool = False,
) -> int:
    """Fetch 1st-degree connections from Unipile and upsert into local DB.

    Tries the relations API first; if it fails/returns empty, falls back to
    extracting connections from inbox chats (each chat attendee = 1st degree).

    Args:
        client: LinkedIn client (BackendClient or UnipileClient).
        account_id: Unipile account ID.
        max_relations: Max relations to fetch (paginated).
        force: If True, bypass the stale check and always re-sync.

    Returns:
        Number of connections synced.
    """
    # Skip if recently synced (unless forced)
    if not force:
        age = await run_db(get_sync_age, account_id)
        if age is not None and age < FULL_SYNC_STALE_SECONDS:
            count = await run_db(get_connection_count, account_id)
            if count > 0:
                logger.info("Connection sync fresh (age=%ds, count=%d), skipping", age, count)
                return count

    relations: list[dict[str, Any]] = []

    # Strategy 1: Relations API (full data with names)
    try:
        relations = await client.get_relations(account_id, limit=max_relations)
    except Exception as e:
        logger.warning("Relations API failed, will try inbox fallback: %s", e)

    # Strategy 2: Inbox chats fallback (provider_ids only, no names)
    if not relations:
        logger.info("Falling back to inbox chats for connection sync")
        relations = await _sync_from_inbox(client, account_id, max_chats=max_relations)

    if not relations:
        logger.debug("No connections found for account %s", account_id)
        return 0

    def _upsert_connections():
        db = get_db()
        now_ = int(time.time())
        synced_ = 0

        try:
            for rel in relations:
                provider_id = (rel.get("provider_id") or "").strip()
                if not provider_id:
                    continue

                public_id = (rel.get("public_id") or "").strip()
                name = (rel.get("name") or "").strip()
                headline = (rel.get("headline") or "").strip()
                company = (rel.get("company") or "").strip()
                location = (rel.get("location") or "").strip()
                profile_url = (rel.get("profile_url") or "").strip()
                if not profile_url and public_id:
                    profile_url = f"https://www.linkedin.com/in/{public_id}"

                # Upsert: INSERT OR REPLACE on the UNIQUE(account_id, provider_id) constraint
                db.execute(
                    """INSERT INTO connections
                       (id, account_id, provider_id, public_id, name, headline,
                        company, location, profile_url, synced_at)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                       ON CONFLICT(account_id, provider_id) DO UPDATE SET
                           public_id = excluded.public_id,
                           name = excluded.name,
                           headline = excluded.headline,
                           company = COALESCE(NULLIF(excluded.company, ''), connections.company),
                           location = COALESCE(NULLIF(excluded.location, ''), connections.location),
                           profile_url = COALESCE(NULLIF(excluded.profile_url, ''), connections.profile_url),
                           synced_at = excluded.synced_at""",
                    (str(uuid.uuid4()), account_id, provider_id, public_id,
                     name, headline, company, location, profile_url, now_),
                )
                synced_ += 1

            # Prune stale connections: remove entries not in the fresh API response.
            # This handles people who disconnected since the last sync.
            fresh_pids = {(rel.get("provider_id") or "").strip() for rel in relations}
            fresh_pids.discard("")
            if fresh_pids and synced_ > 0:
                # Only prune if the API returned a meaningful set (> 10) to avoid
                # accidentally wiping everything on a partial/failed API response.
                if len(fresh_pids) > 10:
                    placeholders = ",".join("?" for _ in fresh_pids)
                    deleted = db.execute(
                        f"DELETE FROM connections WHERE account_id = ? AND provider_id NOT IN ({placeholders})",
                        (account_id, *fresh_pids),
                    ).rowcount
                    if deleted:
                        logger.info("Connection sync: pruned %d stale connections for account %s", deleted, account_id)

            db.commit()
            logger.info("Connection sync: %d connections synced for account %s", synced_, account_id)
        except Exception as e:
            logger.warning("Connection sync failed (DB): %s", e)
        finally:
            db.close()
        return synced_

    synced = await run_db(_upsert_connections)

    # Update global_contacts.network_degree for synced connections
    await run_db(_update_global_contacts_degree, relations)

    return synced


async def _sync_from_inbox(
    client: Any,
    account_id: str,
    max_chats: int = 500,
) -> list[dict[str, Any]]:
    """Extract 1st-degree connections from inbox chats as a fallback.

    Each LinkedIn chat has an attendee_provider_id which is a 1st-degree connection.
    This works when the relations API times out (common for accounts with many connections).
    Fetches raw chat data directly from the backend/Unipile chats endpoint.
    """
    relations: list[dict[str, Any]] = []
    seen_pids: set[str] = set()

    try:
        # Use raw chats endpoint to get attendee_provider_id
        # (the normalized get_chats() loses this field)
        all_chats: list[dict[str, Any]] = []
        cursor: str | None = None
        page_size = min(max_chats, 50)
        pages = 0
        max_pages = (max_chats // page_size) + 1

        while pages < max_pages:
            chats_page, next_cursor = await _fetch_raw_chats(
                client, page_size, cursor,
            )
            if not chats_page:
                break
            all_chats.extend(chats_page)
            cursor = next_cursor
            pages += 1
            if not cursor or len(all_chats) >= max_chats:
                break

        for chat in all_chats:
            if not isinstance(chat, dict):
                continue

            # Extract attendee provider_id
            att_pid = chat.get("attendee_provider_id", "")
            if not att_pid or att_pid in seen_pids:
                continue
            seen_pids.add(att_pid)

            relations.append({
                "provider_id": str(att_pid),
                "name": "",
                "headline": "",
                "public_id": "",
            })

        logger.info(
            "Inbox fallback: found %d unique connections from %d chats",
            len(relations), len(all_chats),
        )
    except Exception as e:
        logger.warning("Inbox fallback failed: %s", e)

    return relations


async def _fetch_raw_chats(
    client: Any,
    limit: int = 50,
    cursor: str | None = None,
) -> tuple[list[dict[str, Any]], str | None]:
    """Fetch raw chat objects from the backend/Unipile chats endpoint.

    Returns (items, next_cursor). Items have attendee_provider_id for connections.
    Uses backend config directly for reliability (avoids client internal access issues).
    """
    import httpx

    try:
        # Get backend config directly — more reliable than accessing client internals
        from ..config import get_backend_config
        base_url, jwt_token = get_backend_config()
        if not base_url or not jwt_token:
            # Try client internals as fallback
            base_url = getattr(client, "base_url", "")
            jwt_token = getattr(client, "jwt_token", "")
            if not base_url or not jwt_token:
                logger.debug("No backend config or client credentials for raw chats fetch")
                return [], None

        url = f"{base_url.rstrip('/')}/api/v1/chats?limit={limit}"
        if cursor:
            url += f"&cursor={cursor}"

        headers = {
            "Authorization": f"Bearer {jwt_token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        async with httpx.AsyncClient(timeout=httpx.Timeout(30.0)) as http:
            resp = await http.get(url, headers=headers)

        if resp.status_code != 200:
            logger.warning("Raw chats fetch returned %d: %s", resp.status_code, resp.text[:200])
            return [], None

        data = resp.json()
        items = data.get("items", []) if isinstance(data, dict) else []
        next_cursor = data.get("cursor") if isinstance(data, dict) else None

        return items, next_cursor
    except Exception as e:
        logger.warning("Raw chats fetch failed: %s", e)
        return [], None


def _update_global_contacts_degree(relations: list[dict[str, Any]]) -> None:
    """Upsert 1st-degree connections into global_contacts.

    For existing contacts: sets network_degree=1.
    For new contacts: creates a global_contacts record from connection data
    so all 1st-degree connections are available across campaigns/accounts.
    """
    db = get_db()
    try:
        updated = 0
        inserted = 0
        now_ = int(time.time())

        for rel in relations:
            provider_id = (rel.get("provider_id") or "").strip()
            public_id = (rel.get("public_id") or "").strip()
            name = (rel.get("name") or "").strip()
            if not provider_id and not public_id:
                continue

            # Try updating existing contact first (by provider_id or public_id)
            matched = False
            for identifier in [public_id, provider_id]:
                if not identifier:
                    continue
                cursor = db.execute(
                    """UPDATE global_contacts SET network_degree = 1, updated_at = ?
                       WHERE (linkedin_id = ? OR linkedin_id = ?) AND (network_degree IS NULL OR network_degree != 1)""",
                    (now_, identifier, identifier.lower()),
                )
                if cursor.rowcount > 0:
                    updated += cursor.rowcount
                    matched = True
                    break
                # Check if it exists but already marked 1st-degree
                exists = db.execute(
                    "SELECT 1 FROM global_contacts WHERE linkedin_id = ? OR linkedin_id = ? LIMIT 1",
                    (identifier, identifier.lower()),
                ).fetchone()
                if exists:
                    matched = True
                    break

            # Insert new contact if not found anywhere
            if not matched and name:
                headline = (rel.get("headline") or "").strip()
                company = (rel.get("company") or "").strip()
                location = (rel.get("location") or "").strip()
                profile_url = (rel.get("profile_url") or "").strip()
                linkedin_id = public_id or provider_id

                try:
                    db.execute(
                        """INSERT INTO global_contacts
                           (id, linkedin_id, linkedin_url, name, title, company,
                            location, network_degree, source, lifecycle_stage,
                            created_at, updated_at)
                           VALUES (?, ?, ?, ?, ?, ?, ?, 1, 'connection_sync', 'prospect', ?, ?)""",
                        (str(uuid.uuid4()), linkedin_id, profile_url, name,
                         headline, company, location, now_, now_),
                    )
                    inserted += 1
                except Exception:
                    pass  # UNIQUE constraint — skip duplicates

        if updated or inserted:
            db.commit()
            if updated:
                logger.info("Updated network_degree=1 for %d global contacts", updated)
            if inserted:
                logger.info("Inserted %d new global contacts from connections", inserted)
    except Exception as e:
        logger.debug("Global contacts degree update skipped: %s", e)
    finally:
        db.close()


def get_all_connections(account_id: str) -> list[dict[str, str]]:
    """Return all locally stored 1st-degree connections with full data fields.

    Returns list of dicts with: provider_id, public_id, name, headline.
    Used by connections-only campaigns to source prospects directly from
    the connections table instead of LinkedIn search.
    """
    db = get_db()
    try:
        rows = db.execute(
            "SELECT provider_id, public_id, name, headline FROM connections WHERE account_id = ?",
            (account_id,),
        ).fetchall()
    except Exception:
        return []
    finally:
        db.close()

    results = []
    for row in rows:
        r = dict(row) if hasattr(row, "keys") else {
            "provider_id": row[0] or "",
            "public_id": row[1] or "",
            "name": row[2] or "",
            "headline": row[3] or "",
        }
        if not (r.get("provider_id") or r.get("public_id")):
            continue
        results.append({
            "provider_id": (r.get("provider_id") or "").strip(),
            "public_id": (r.get("public_id") or "").strip(),
            "name": (r.get("name") or "").strip(),
            "headline": (r.get("headline") or "").strip(),
        })
    return results


def get_local_connection_ids(account_id: str) -> set[str]:
    """Fast set-based lookup of all locally stored 1st-degree connection identifiers.

    Returns a set of lowercase provider_ids + public_ids + linkedin URLs.
    """
    db = get_db()
    try:
        rows = db.execute(
            """SELECT provider_id, public_id FROM connections WHERE account_id = ?""",
            (account_id,),
        ).fetchall()
    except Exception:
        return set()
    finally:
        db.close()

    ids: set[str] = set()
    for row in rows:
        pid = row[0] or ""
        pub = row[1] or ""
        if pid:
            ids.add(pid.lower().strip())
        if pub:
            ids.add(pub.lower().strip())
            ids.add(f"https://www.linkedin.com/in/{pub.lower().strip()}")
    return ids


def is_first_degree(account_id: str, provider_id: str) -> bool:
    """Quick check if a specific prospect is a 1st-degree connection in local DB."""
    if not provider_id:
        return False
    db = get_db()
    try:
        row = db.execute(
            "SELECT 1 FROM connections WHERE account_id = ? AND provider_id = ? LIMIT 1",
            (account_id, provider_id.strip()),
        ).fetchone()
        return row is not None
    except Exception:
        return False
    finally:
        db.close()


def is_first_degree_by_public_id(account_id: str, public_id: str) -> bool:
    """Quick check if a specific prospect is a 1st-degree connection by public_id."""
    if not public_id:
        return False
    db = get_db()
    try:
        row = db.execute(
            "SELECT 1 FROM connections WHERE account_id = ? AND LOWER(public_id) = LOWER(?) LIMIT 1",
            (account_id, public_id.strip()),
        ).fetchone()
        return row is not None
    except Exception:
        return False
    finally:
        db.close()


def mark_connected(
    account_id: str,
    provider_id: str,
    name: str = "",
    public_id: str = "",
    headline: str = "",
) -> None:
    """Record a newly connected prospect in local connections table.

    Called when we discover a prospect is already connected (via profile check or 409).
    """
    if not provider_id:
        return
    db = get_db()
    try:
        db.execute(
            """INSERT INTO connections (id, account_id, provider_id, public_id, name, headline, synced_at)
               VALUES (?, ?, ?, ?, ?, ?, ?)
               ON CONFLICT(account_id, provider_id) DO UPDATE SET
                   name = COALESCE(NULLIF(excluded.name, ''), connections.name),
                   public_id = COALESCE(NULLIF(excluded.public_id, ''), connections.public_id),
                   headline = COALESCE(NULLIF(excluded.headline, ''), connections.headline),
                   synced_at = excluded.synced_at""",
            (str(uuid.uuid4()), account_id, provider_id.strip(), public_id, name, headline, int(time.time())),
        )
        db.commit()
    except Exception as e:
        logger.debug("mark_connected failed: %s", e)
    finally:
        db.close()


def get_sync_age(account_id: str) -> int | None:
    """Return seconds since last connection sync, or None if never synced."""
    db = get_db()
    try:
        row = db.execute(
            "SELECT MAX(synced_at) FROM connections WHERE account_id = ?",
            (account_id,),
        ).fetchone()
        if row and row[0]:
            return int(time.time()) - int(row[0])
        return None
    except Exception:
        return None
    finally:
        db.close()


async def ensure_synced(client: Any, account_id: str) -> set[str]:
    """Ensure connections are synced (auto-sync if stale), then return local IDs.

    This is the main entry point for dedup: checks sync age and refreshes if needed,
    then returns the fast local set.
    """
    age = await run_db(get_sync_age, account_id)
    if age is None or age > SYNC_STALE_SECONDS:
        logger.info("Connection sync stale (age=%s) — re-syncing for account %s", age, account_id)
        await sync_connections(client, account_id)
    return await run_db(get_local_connection_ids, account_id)


async def enrich_prospects(
    client: Any,
    account_id: str,
    prospects: list[dict],
    max_enrich: int = 50,
    delay: float = 1.0,
) -> int:
    """Enrich prospects missing profile_json with full LinkedIn profiles.

    Calls get_profile() per prospect that lacks profile_json, then upserts
    the enriched data to global_contacts and updates the prospect dict in-place.
    Also fetches recent posts for enriched prospects.

    Args:
        client: LinkedIn client (UnipileClient or BackendClient).
        account_id: Unipile account ID.
        prospects: List of prospect dicts to enrich (modified in-place).
        max_enrich: Maximum number of profiles to enrich (rate limit safety).
        delay: Seconds to wait between API calls.

    Returns:
        Number of profiles successfully enriched.
    """
    import asyncio
    import json as _json

    from ..db.global_contact_queries import upsert_global_contact

    # Filter to prospects that need enrichment
    to_enrich = [
        p for p in prospects
        if not p.get("profile_json")
        and (p.get("provider_id") or p.get("public_id") or p.get("linkedin_id"))
    ][:max_enrich]

    if not to_enrich:
        return 0

    enriched = 0
    for i, prospect in enumerate(to_enrich):
        lid = (
            prospect.get("provider_id")
            or prospect.get("public_id")
            or prospect.get("linkedin_id", "")
        )
        if not lid:
            continue

        try:
            profile = await client.get_profile(account_id, lid)
            if not profile or not isinstance(profile, dict):
                continue

            profile_json = _json.dumps(profile)
            # Update prospect dict in-place with enriched data
            prospect["profile_json"] = profile_json
            if profile.get("title") and not prospect.get("title"):
                prospect["title"] = profile["title"]
            if profile.get("headline"):
                prospect["title"] = prospect.get("title") or profile["headline"]
            if profile.get("company") and not prospect.get("company"):
                prospect["company"] = profile["company"]
            if profile.get("location") and not prospect.get("location"):
                prospect["location"] = profile["location"]
            if profile.get("provider_id") and not prospect.get("provider_id"):
                prospect["provider_id"] = profile["provider_id"]

            # Upsert to global_contacts
            try:
                await run_db(upsert_global_contact,
                    linkedin_id=lid,
                    name=prospect.get("name", ""),
                    title=prospect.get("title", ""),
                    company=prospect.get("company", ""),
                    linkedin_url=prospect.get("linkedin_url", ""),
                    location=prospect.get("location", ""),
                    profile_json=profile_json,
                    source="connection_enrichment",
                )
            except Exception as e:
                logger.debug("Global contact upsert failed for %s: %s", lid, e)

            # Fetch recent posts
            try:
                from ..db.post_queries import upsert_post
                posts = await client.get_user_posts(account_id, lid, limit=10)
                if posts and isinstance(posts, list):
                    for post in posts:
                        pid = post.get("id", "")
                        txt = post.get("text", "")
                        if pid and txt:
                            await run_db(upsert_post,
                                pid,
                                author_linkedin_id=lid,
                                author_name=prospect.get("name", ""),
                                text=txt[:2000],
                                metrics_json=_json.dumps(post.get("metrics", {})),
                                source="enrichment",
                            )
            except Exception:
                pass  # Post fetch is non-critical

            enriched += 1
            logger.debug("Enriched %s (%d/%d)", prospect.get("name", lid), enriched, len(to_enrich))

        except Exception as e:
            logger.debug("Enrich failed for %s: %s", lid, e)

        # Rate limit delay (skip after last item)
        if i < len(to_enrich) - 1:
            await asyncio.sleep(delay)

    logger.info("Enriched %d/%d prospects with full profiles", enriched, len(to_enrich))
    return enriched


async def audit_campaign_connections(
    client: Any,
    account_id: str,
    campaign_id: str,
) -> dict[str, Any]:
    """Audit a campaign's pending outreaches against current 1st-degree connections.

    1. Ensure connections are synced
    2. Get all pending outreaches for the campaign
    3. Cross-reference against local connections
    4. For matches: update outreach to 'connected'
    5. Return audit report

    Returns:
        {"total_pending": int, "already_connected": int, "updated": list[str]}
    """
    from ..db.schema import get_db as _get_db

    # Step 1: Ensure fresh connections
    await ensure_synced(client, account_id)
    connection_ids = await run_db(get_local_connection_ids, account_id)

    # Step 2: Get pending outreaches
    def _get_pending_outreaches(cid):
        db = _get_db()
        try:
            return db.execute(
                """SELECT o.id, o.contact_id, c.linkedin_id, c.name, c.linkedin_url,
                          c.profile_json
                   FROM outreaches o
                   JOIN contacts c ON o.contact_id = c.id
                   WHERE o.campaign_id = ? AND o.status = 'pending'""",
                (cid,),
            ).fetchall()
        finally:
            db.close()

    rows = await run_db(_get_pending_outreaches, campaign_id)

    report = {
        "total_pending": len(rows),
        "already_connected": 0,
        "updated": [],
    }

    if not rows:
        return report

    # Step 3 & 4: Cross-reference and update
    import json

    for row in rows:
        outreach_id = row[0]
        linkedin_id = (row[2] or "").lower().strip()
        name = row[3] or ""
        linkedin_url = (row[4] or "").lower().strip()
        profile_json_str = row[5] or "{}"

        # Extract provider_id from profile_json
        provider_id = ""
        try:
            profile = json.loads(profile_json_str)
            provider_id = (profile.get("provider_id") or "").lower().strip()
        except Exception:
            pass

        # Build identifier set for this prospect
        identifiers = {x for x in (linkedin_id, provider_id, linkedin_url) if x}
        if linkedin_id:
            identifiers.add(f"https://www.linkedin.com/in/{linkedin_id}")

        # Check against local connections
        if identifiers & connection_ids:
            def _mark_connected(oid):
                db = _get_db()
                try:
                    db.execute(
                        "UPDATE outreaches SET status = 'connected' WHERE id = ?",
                        (oid,),
                    )
                    db.commit()
                finally:
                    db.close()

            await run_db(_mark_connected, outreach_id)

            report["already_connected"] += 1
            report["updated"].append(name or outreach_id)
            logger.info("Audit: %s is already 1st-degree connected — marked as 'connected'", name)

    return report


def get_connection_count(account_id: str) -> int:
    """Return the number of locally stored connections for an account."""
    db = get_db()
    try:
        row = db.execute(
            "SELECT COUNT(*) FROM connections WHERE account_id = ?",
            (account_id,),
        ).fetchone()
        return row[0] if row else 0
    except Exception:
        return 0
    finally:
        db.close()
