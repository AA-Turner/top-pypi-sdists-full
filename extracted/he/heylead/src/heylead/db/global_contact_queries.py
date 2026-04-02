"""SQLite CRUD helpers for the global contact base (master record per person)."""

from __future__ import annotations

import json
import logging
import time
import uuid
from typing import Any, Optional

from .schema import get_db

logger = logging.getLogger(__name__)

# Lifecycle stage ordering — only promote forward, never demote.
# Higher number = more advanced stage.
_LIFECYCLE_ORDER: dict[str, int] = {
    "prospect": 0,
    "contacted": 1,
    "connected": 2,
    "engaged": 3,
    "lost": 3,  # same level as engaged (can go engaged→lost, not customer→lost)
    "customer": 4,
    "churned": 5,
    "do_not_contact": 6,
}

# Map outreach status → global contact lifecycle stage
_OUTREACH_TO_LIFECYCLE: dict[str, str] = {
    "invited": "contacted",
    "connected": "connected",
    "messaged": "connected",
    "replied": "engaged",
    "hot_lead": "engaged",
    "closed_happy": "customer",
    "closed_unhappy": "lost",
}


# ──────────────────────────────────────────────
# Core CRUD
# ──────────────────────────────────────────────

def upsert_global_contact(
    linkedin_id: str,
    name: str,
    title: str = "",
    company: str = "",
    linkedin_url: str = "",
    email: str = "",
    location: str = "",
    profile_json: str = "",
    analysis_json: str = "",
    fit_score: float = 0.0,
    estimated_revenue: float = 0.0,
    source: str = "search",
    source_detail: str = "",
    campaign_id: str = "",
) -> str:
    """Create or update a global contact. Returns global_contact_id.

    If linkedin_id matches an existing record, updates fields using
    "best wins" logic (newer non-empty values win, MAX for scores).
    """
    now = int(time.time())
    db = get_db()

    existing = None
    if linkedin_id:
        existing = db.execute(
            "SELECT * FROM global_contacts WHERE linkedin_id = ? LIMIT 1",
            (linkedin_id,),
        ).fetchone()

    # Fallback: match by provider_id inside profile_json
    if not existing and profile_json:
        try:
            pj = json.loads(profile_json) if isinstance(profile_json, str) else profile_json
            incoming_pid = (pj.get("provider_id") or "").strip()
            if incoming_pid:
                existing = db.execute(
                    """SELECT * FROM global_contacts
                       WHERE profile_json IS NOT NULL AND profile_json != ''
                         AND json_valid(profile_json)
                         AND json_extract(profile_json, '$.provider_id') = ?
                       LIMIT 1""",
                    (incoming_pid,),
                ).fetchone()
                if existing:
                    logger.info(
                        "Matched global contact by provider_id %s (linkedin_id mismatch: %s vs %s)",
                        incoming_pid, linkedin_id, dict(existing).get("linkedin_id"),
                    )
        except (json.JSONDecodeError, TypeError, AttributeError):
            pass

    if existing:
        existing = dict(existing)
        gid = existing["id"]
        # Update with best available data (non-empty wins, MAX for scores)
        updates: dict[str, Any] = {"updated_at": now}
        # Backfill linkedin_id if existing record was matched by provider_id only
        if linkedin_id and not existing.get("linkedin_id"):
            updates["linkedin_id"] = linkedin_id
        if name and not existing.get("name"):
            updates["name"] = name
        if title and not existing.get("title"):
            updates["title"] = title
        if company and not existing.get("company"):
            updates["company"] = company
        if linkedin_url and not existing.get("linkedin_url"):
            updates["linkedin_url"] = linkedin_url
        if email and not existing.get("email"):
            updates["email"] = email
        if location and not existing.get("location"):
            updates["location"] = location
        if profile_json and (
            not existing.get("profile_json")
            or len(profile_json) > len(existing.get("profile_json") or "")
        ):
            updates["profile_json"] = profile_json
        if analysis_json and not existing.get("analysis_json"):
            updates["analysis_json"] = analysis_json
        if fit_score > (existing.get("fit_score") or 0):
            updates["fit_score"] = fit_score
        if estimated_revenue > (existing.get("estimated_revenue") or 0):
            updates["estimated_revenue"] = estimated_revenue
        # Promote source if new value is more specific than generic 'search'
        if source and source != "search" and existing.get("source") in ("search", "", None):
            updates["source"] = source
        if source_detail and not existing.get("source_detail"):
            updates["source_detail"] = source_detail
        updates["total_campaigns"] = (existing.get("total_campaigns") or 0) + 1

        set_clause = ", ".join(f"{k} = ?" for k in updates)
        values = list(updates.values()) + [gid]
        db.execute(f"UPDATE global_contacts SET {set_clause} WHERE id = ?", values)
        db.commit()
        db.close()
        return gid

    # Create new
    gid = str(uuid.uuid4())
    db.execute(
        """INSERT INTO global_contacts
           (id, linkedin_id, linkedin_url, name, title, company, email, location,
            profile_json, analysis_json, fit_score, estimated_revenue,
            lifecycle_stage, source, source_detail, first_campaign_id, total_campaigns,
            created_at, updated_at)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'prospect', ?, ?, ?, 1, ?, ?)""",
        (
            gid, linkedin_id or None, linkedin_url, name, title, company,
            email, location, profile_json, analysis_json, fit_score,
            estimated_revenue, source, source_detail, campaign_id or None, now, now,
        ),
    )
    db.commit()
    db.close()
    return gid


def get_global_contact(global_contact_id: str) -> Optional[dict]:
    """Get a global contact by ID."""
    db = get_db()
    row = db.execute(
        "SELECT * FROM global_contacts WHERE id = ?", (global_contact_id,)
    ).fetchone()
    db.close()
    return dict(row) if row else None


def get_global_contacts_by_identifiers(identifiers: list[str]) -> dict[str, dict]:
    """Batch lookup global_contacts by linkedin_id or provider_id (in profile_json).

    Returns mapping of lowercase identifier -> global_contact row.
    Matches on linkedin_id column first, then provider_id inside profile_json.
    Used to merge existing enrichment data into connection-based prospects.
    """
    if not identifiers:
        return {}
    db = get_db()
    result: dict[str, dict] = {}
    # SQLite has a 999-parameter limit — batch in chunks
    chunk_size = 900
    try:
        for i in range(0, len(identifiers), chunk_size):
            chunk = identifiers[i : i + chunk_size]
            placeholders = ",".join("?" for _ in chunk)
            # Match by linkedin_id
            rows = db.execute(
                f"SELECT * FROM global_contacts WHERE linkedin_id IN ({placeholders})",
                chunk,
            ).fetchall()
            for row in rows:
                r = dict(row)
                lid = (r.get("linkedin_id") or "").lower().strip()
                if lid:
                    result[lid] = r
            # Also match by provider_id inside profile_json for identifiers not yet found
            remaining = [ident for ident in chunk if ident.lower().strip() not in result]
            if remaining:
                for ident in remaining:
                    row = db.execute(
                        """SELECT * FROM global_contacts
                           WHERE profile_json IS NOT NULL AND profile_json != ''
                             AND json_valid(profile_json)
                             AND json_extract(profile_json, '$.provider_id') = ?
                           LIMIT 1""",
                        (ident,),
                    ).fetchone()
                    if row:
                        result[ident.lower().strip()] = dict(row)
    except Exception as e:
        logger.warning("Batch global contacts lookup failed: %s", e)
    finally:
        db.close()
    return result


def get_global_contact_by_linkedin_id(linkedin_id: str) -> Optional[dict]:
    """Get a global contact by linkedin_id."""
    if not linkedin_id:
        return None
    db = get_db()
    row = db.execute(
        "SELECT * FROM global_contacts WHERE linkedin_id = ? LIMIT 1",
        (linkedin_id,),
    ).fetchone()
    db.close()
    return dict(row) if row else None


# ──────────────────────────────────────────────
# Search & List
# ──────────────────────────────────────────────

def search_global_contacts(
    query: str = "",
    lifecycle_stage: str = "",
    tag: str = "",
    min_fit_score: float = 0.0,
    limit: int = 50,
    offset: int = 0,
    order_by: str = "updated_at DESC",
) -> list[dict]:
    """Search global contacts with text search, lifecycle filter, tag filter."""
    conditions: list[str] = []
    params: list[Any] = []

    if query:
        conditions.append(
            "(name LIKE ? OR title LIKE ? OR company LIKE ? OR email LIKE ? OR location LIKE ?)"
        )
        q = f"%{query}%"
        params.extend([q, q, q, q, q])

    if lifecycle_stage:
        conditions.append("lifecycle_stage = ?")
        params.append(lifecycle_stage)

    if tag:
        conditions.append("tags_json LIKE ?")
        params.append(f'%"{tag}"%')

    if min_fit_score > 0:
        conditions.append("fit_score >= ?")
        params.append(min_fit_score)

    where = f"WHERE {' AND '.join(conditions)}" if conditions else ""

    # Validate order_by to prevent SQL injection
    allowed_orders = {
        "updated_at DESC", "updated_at ASC",
        "created_at DESC", "created_at ASC",
        "fit_score DESC", "fit_score ASC",
        "name ASC", "name DESC",
        "last_interaction_at DESC",
    }
    if order_by not in allowed_orders:
        order_by = "updated_at DESC"

    db = get_db()
    rows = db.execute(
        f"SELECT * FROM global_contacts {where} ORDER BY {order_by} LIMIT ? OFFSET ?",
        params + [limit, offset],
    ).fetchall()
    db.close()
    return [dict(r) for r in rows]


def get_all_global_linkedin_ids() -> set[str]:
    """Fast set of all linkedin_ids in global_contacts (for dedup)."""
    db = get_db()
    rows = db.execute(
        """SELECT linkedin_id FROM global_contacts
           WHERE linkedin_id IS NOT NULL AND linkedin_id != ''
           UNION
           SELECT linkedin_url FROM global_contacts
           WHERE linkedin_url IS NOT NULL AND linkedin_url != ''"""
    ).fetchall()
    db.close()

    ids: set[str] = set()
    for row in rows:
        val = row[0]
        if val:
            ids.add(val.lower().strip())
    return ids


# ──────────────────────────────────────────────
# Lifecycle
# ──────────────────────────────────────────────

def update_global_contact_lifecycle(
    global_contact_id: str, new_stage: str
) -> None:
    """Update lifecycle stage (only promotes forward, never demotes).

    Uses _LIFECYCLE_ORDER to determine if the new stage is higher.
    """
    if new_stage not in _LIFECYCLE_ORDER:
        return

    db = get_db()
    row = db.execute(
        "SELECT lifecycle_stage FROM global_contacts WHERE id = ?",
        (global_contact_id,),
    ).fetchone()
    if not row:
        db.close()
        return

    current = row["lifecycle_stage"] or "prospect"
    current_order = _LIFECYCLE_ORDER.get(current, 0)
    new_order = _LIFECYCLE_ORDER.get(new_stage, 0)

    if new_order > current_order:
        now = int(time.time())
        db.execute(
            "UPDATE global_contacts SET lifecycle_stage = ?, updated_at = ? WHERE id = ?",
            (new_stage, now, global_contact_id),
        )
        db.commit()
    db.close()


def promote_lifecycle_from_outreach(
    outreach_id: str, outreach_status: str
) -> None:
    """Promote global contact lifecycle based on outreach status change.

    Called from update_outreach(). Non-critical — failures are logged, not raised.
    """
    target = _OUTREACH_TO_LIFECYCLE.get(outreach_status)
    if not target:
        return

    try:
        db = get_db()
        row = db.execute(
            """SELECT c.global_contact_id
               FROM outreaches o
               JOIN contacts c ON o.contact_id = c.id
               WHERE o.id = ?""",
            (outreach_id,),
        ).fetchone()
        db.close()

        if row and row["global_contact_id"]:
            update_global_contact_lifecycle(row["global_contact_id"], target)

            # Update last_interaction_at
            now = int(time.time())
            db2 = get_db()
            db2.execute(
                "UPDATE global_contacts SET last_interaction_at = ?, updated_at = ? WHERE id = ?",
                (now, now, row["global_contact_id"]),
            )
            db2.commit()
            db2.close()

            # If contacted for the first time, set first_contacted_at
            if target == "contacted":
                db3 = get_db()
                db3.execute(
                    """UPDATE global_contacts
                       SET first_contacted_at = ?
                       WHERE id = ? AND first_contacted_at IS NULL""",
                    (now, row["global_contact_id"]),
                )
                db3.commit()
                db3.close()
    except Exception as exc:
        logger.warning("Failed to promote global contact lifecycle: %s", exc)


# ──────────────────────────────────────────────
# Tags & Notes
# ──────────────────────────────────────────────

def add_global_contact_tag(global_contact_id: str, tag: str) -> None:
    """Add a tag to a global contact's tags_json."""
    tag = tag.strip().lower()
    if not tag:
        return
    db = get_db()
    row = db.execute(
        "SELECT tags_json FROM global_contacts WHERE id = ?",
        (global_contact_id,),
    ).fetchone()
    if not row:
        db.close()
        return

    tags = json.loads(row["tags_json"] or "[]")
    if tag not in tags:
        tags.append(tag)
        db.execute(
            "UPDATE global_contacts SET tags_json = ?, updated_at = ? WHERE id = ?",
            (json.dumps(tags), int(time.time()), global_contact_id),
        )
        db.commit()
    db.close()


def remove_global_contact_tag(global_contact_id: str, tag: str) -> None:
    """Remove a tag from a global contact's tags_json."""
    tag = tag.strip().lower()
    if not tag:
        return
    db = get_db()
    row = db.execute(
        "SELECT tags_json FROM global_contacts WHERE id = ?",
        (global_contact_id,),
    ).fetchone()
    if not row:
        db.close()
        return

    tags = json.loads(row["tags_json"] or "[]")
    if tag in tags:
        tags.remove(tag)
        db.execute(
            "UPDATE global_contacts SET tags_json = ?, updated_at = ? WHERE id = ?",
            (json.dumps(tags), int(time.time()), global_contact_id),
        )
        db.commit()
    db.close()


def is_excluded_from_automation(global_contact_id: str) -> bool:
    """Check if a global contact should be excluded from all automation.

    Returns True if the contact has the 'do-not-automate' tag or
    lifecycle_stage == 'do_not_contact'.
    """
    if not global_contact_id:
        return False
    db = get_db()
    row = db.execute(
        "SELECT tags_json, lifecycle_stage FROM global_contacts WHERE id = ?",
        (global_contact_id,),
    ).fetchone()
    db.close()
    if not row:
        return False
    if row["lifecycle_stage"] == "do_not_contact":
        return True
    tags = json.loads(row["tags_json"] or "[]")
    return "do-not-automate" in tags


def is_excluded_by_contact_id(contact_id: str) -> bool:
    """Check exclusion using a campaign-level contact_id (resolves to global)."""
    if not contact_id:
        return False
    db = get_db()
    row = db.execute(
        "SELECT global_contact_id FROM contacts WHERE id = ?",
        (contact_id,),
    ).fetchone()
    db.close()
    if not row or not row["global_contact_id"]:
        return False
    return is_excluded_from_automation(row["global_contact_id"])


def add_global_contact_note(global_contact_id: str, text: str) -> None:
    """Append a note to a global contact's notes_json."""
    text = text.strip()
    if not text:
        return
    db = get_db()
    row = db.execute(
        "SELECT notes_json FROM global_contacts WHERE id = ?",
        (global_contact_id,),
    ).fetchone()
    if not row:
        db.close()
        return

    notes = json.loads(row["notes_json"] or "[]")
    notes.append({"text": text, "created_at": int(time.time())})
    db.execute(
        "UPDATE global_contacts SET notes_json = ?, updated_at = ? WHERE id = ?",
        (json.dumps(notes), int(time.time()), global_contact_id),
    )
    db.commit()
    db.close()


# ──────────────────────────────────────────────
# Cross-Campaign History
# ──────────────────────────────────────────────

def get_cross_campaign_history(global_contact_id: str) -> Optional[dict]:
    """Get full cross-campaign interaction history for a global contact.

    Returns:
        {
            "global_contact": {...},
            "campaigns": [
                {
                    "campaign_id": "...",
                    "campaign_name": "...",
                    "contact_id": "...",
                    "fit_score": 0.85,
                    "outreach": {...},
                    "messages": [...],
                    "engagements": [...],
                }
            ],
            "signals": [...],
        }
    """
    gc = get_global_contact(global_contact_id)
    if not gc:
        return None

    db = get_db()

    # Get all campaign contacts linked to this global contact
    contacts = db.execute(
        """SELECT c.*, camp.name as campaign_name, camp.status as campaign_status
           FROM contacts c
           LEFT JOIN campaigns camp ON c.campaign_id = camp.id
           WHERE c.global_contact_id = ?
           ORDER BY c.created_at DESC""",
        (global_contact_id,),
    ).fetchall()

    campaigns: list[dict] = []
    for contact in contacts:
        c = dict(contact)
        contact_id = c["id"]
        campaign_id = c["campaign_id"]

        # Get outreach for this contact
        outreach_row = db.execute(
            "SELECT * FROM outreaches WHERE contact_id = ? AND campaign_id = ? LIMIT 1",
            (contact_id, campaign_id),
        ).fetchone()
        outreach = dict(outreach_row) if outreach_row else None

        # Get messages
        messages: list[dict] = []
        if outreach:
            msg_rows = db.execute(
                "SELECT * FROM messages WHERE outreach_id = ? ORDER BY timestamp ASC",
                (outreach["id"],),
            ).fetchall()
            messages = [dict(m) for m in msg_rows]

        # Get engagements
        engagements: list[dict] = []
        if outreach:
            eng_rows = db.execute(
                "SELECT * FROM engagements WHERE outreach_id = ? ORDER BY created_at ASC",
                (outreach["id"],),
            ).fetchall()
            engagements = [dict(e) for e in eng_rows]

        campaigns.append({
            "campaign_id": campaign_id,
            "campaign_name": c.get("campaign_name") or "Unknown",
            "campaign_status": c.get("campaign_status") or "unknown",
            "contact_id": contact_id,
            "fit_score": c.get("fit_score") or 0.0,
            "outreach": outreach,
            "messages": messages,
            "engagements": engagements,
        })

    # Get signals linked to this person's linkedin_id
    signals: list[dict] = []
    linkedin_id = gc.get("linkedin_id")
    if linkedin_id:
        sig_rows = db.execute(
            """SELECT * FROM signals WHERE linkedin_id = ?
               ORDER BY detected_at DESC LIMIT 20""",
            (linkedin_id,),
        ).fetchall()
        signals = [dict(s) for s in sig_rows]

    db.close()

    return {
        "global_contact": gc,
        "campaigns": campaigns,
        "signals": signals,
    }


# ──────────────────────────────────────────────
# Stats
# ──────────────────────────────────────────────

def get_global_contact_stats() -> dict:
    """Dashboard stats: total contacts, by lifecycle, by source, top tags."""
    db = get_db()

    total = db.execute("SELECT COUNT(*) as cnt FROM global_contacts").fetchone()["cnt"]

    # By lifecycle
    lc_rows = db.execute(
        """SELECT lifecycle_stage, COUNT(*) as cnt
           FROM global_contacts GROUP BY lifecycle_stage ORDER BY cnt DESC"""
    ).fetchall()
    by_lifecycle = {r["lifecycle_stage"]: r["cnt"] for r in lc_rows}

    # By source
    src_rows = db.execute(
        """SELECT source, COUNT(*) as cnt
           FROM global_contacts GROUP BY source ORDER BY cnt DESC"""
    ).fetchall()
    by_source = {r["source"]: r["cnt"] for r in src_rows}

    # Top tags (flatten tags_json across all contacts)
    tag_rows = db.execute(
        "SELECT tags_json FROM global_contacts WHERE tags_json != '[]'"
    ).fetchall()
    tag_counts: dict[str, int] = {}
    for row in tag_rows:
        try:
            tags = json.loads(row["tags_json"] or "[]")
            for t in tags:
                tag_counts[t] = tag_counts.get(t, 0) + 1
        except (json.JSONDecodeError, TypeError):
            pass
    top_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)[:10]

    db.close()

    return {
        "total": total,
        "by_lifecycle": by_lifecycle,
        "by_source": by_source,
        "top_tags": top_tags,
    }


# ──────────────────────────────────────────────
# Duplicate detection & merging
# ──────────────────────────────────────────────

def find_duplicate_global_contacts() -> list[dict]:
    """Find global contacts that share the same provider_id but have different IDs.

    Returns list of dicts with keys: keep_id, merge_id, provider_id, keep_name, merge_name.
    """
    db = get_db()
    try:
        # Strategy 1: Match by provider_id in profile_json
        rows = db.execute(
            """WITH pids AS (
                 SELECT id, name, total_campaigns, fit_score,
                        json_extract(profile_json, '$.provider_id') AS pid
                 FROM global_contacts
                 WHERE profile_json IS NOT NULL AND profile_json != ''
                   AND json_valid(profile_json)
                   AND json_extract(profile_json, '$.provider_id') IS NOT NULL
                   AND json_extract(profile_json, '$.provider_id') != ''
               )
               SELECT p1.id AS id1, p2.id AS id2, p1.pid AS pid,
                      p1.name AS name1, p2.name AS name2,
                      p1.total_campaigns AS tc1, p2.total_campaigns AS tc2,
                      p1.fit_score AS fs1, p2.fit_score AS fs2
               FROM pids p1
               JOIN pids p2 ON p1.pid = p2.pid AND p1.id < p2.id"""
        ).fetchall()

        # Strategy 2: Match where one record has provider_id (ACoAA) as linkedin_id
        # and another has the public_id slug — same name indicates same person.
        # Check both orderings since gc1.id < gc2.id may place either format first.
        rows2 = db.execute(
            """SELECT gc1.id AS id1, gc2.id AS id2,
                      CASE WHEN gc1.linkedin_id LIKE 'ACoAA%' THEN gc1.linkedin_id
                           ELSE gc2.linkedin_id END AS pid,
                      gc1.name AS name1, gc2.name AS name2,
                      gc1.total_campaigns AS tc1, gc2.total_campaigns AS tc2,
                      gc1.fit_score AS fs1, gc2.fit_score AS fs2
               FROM global_contacts gc1
               JOIN global_contacts gc2
                 ON LOWER(TRIM(gc1.name)) = LOWER(TRIM(gc2.name))
                AND gc1.id < gc2.id
               WHERE gc1.name IS NOT NULL AND gc1.name != ''
                 AND gc1.linkedin_id IS NOT NULL AND gc1.linkedin_id != ''
                 AND gc2.linkedin_id IS NOT NULL AND gc2.linkedin_id != ''
                 AND (
                   (gc1.linkedin_id LIKE 'ACoAA%' AND gc2.linkedin_id NOT LIKE 'ACoAA%')
                   OR
                   (gc2.linkedin_id LIKE 'ACoAA%' AND gc1.linkedin_id NOT LIKE 'ACoAA%')
                 )"""
        ).fetchall()
        rows = list(rows) + list(rows2)
    except Exception as e:
        logger.warning("find_duplicate_global_contacts failed: %s", e)
        db.close()
        return []

    db.close()

    duplicates = []
    seen_pairs: set[tuple[str, str]] = set()
    for row in rows:
        row = dict(row)
        # Deduplicate pairs (same pair may appear from multiple strategies)
        pair_key = tuple(sorted((row["id1"], row["id2"])))
        if pair_key in seen_pairs:
            continue
        seen_pairs.add(pair_key)

        # Keep the record with more campaigns (or higher fit_score as tiebreaker)
        tc1, tc2 = row["tc1"] or 0, row["tc2"] or 0
        fs1, fs2 = row["fs1"] or 0, row["fs2"] or 0
        if tc1 > tc2 or (tc1 == tc2 and fs1 >= fs2):
            keep_id, merge_id = row["id1"], row["id2"]
            keep_name, merge_name = row["name1"], row["name2"]
        else:
            keep_id, merge_id = row["id2"], row["id1"]
            keep_name, merge_name = row["name2"], row["name1"]

        duplicates.append({
            "keep_id": keep_id,
            "merge_id": merge_id,
            "provider_id": row["pid"],
            "keep_name": keep_name,
            "merge_name": merge_name,
        })

    return duplicates


def merge_global_contacts(keep_id: str, merge_id: str) -> bool:
    """Merge two global contact records. Keeps keep_id, deletes merge_id.

    - Applies "best wins" field merging
    - Reassigns all contacts.global_contact_id FKs from merge_id to keep_id
    - Combines tags and notes
    - Sums total_campaigns
    """
    db = get_db()
    try:
        keep_row = db.execute(
            "SELECT * FROM global_contacts WHERE id = ?", (keep_id,)
        ).fetchone()
        merge_row = db.execute(
            "SELECT * FROM global_contacts WHERE id = ?", (merge_id,)
        ).fetchone()

        if not keep_row or not merge_row:
            logger.warning("merge_global_contacts: one or both records not found")
            db.close()
            return False

        keep = dict(keep_row)
        merge = dict(merge_row)
        now = int(time.time())

        # Best-wins merge
        updates: dict[str, Any] = {"updated_at": now}

        # Fill empty fields from merge record
        for field in ("name", "title", "company", "linkedin_id", "linkedin_url",
                      "email", "location", "source_detail"):
            if not keep.get(field) and merge.get(field):
                updates[field] = merge[field]

        # MAX for scores
        if (merge.get("fit_score") or 0) > (keep.get("fit_score") or 0):
            updates["fit_score"] = merge["fit_score"]
        if (merge.get("estimated_revenue") or 0) > (keep.get("estimated_revenue") or 0):
            updates["estimated_revenue"] = merge["estimated_revenue"]

        # Longer profile_json wins
        if merge.get("profile_json") and len(merge["profile_json"]) > len(keep.get("profile_json") or ""):
            updates["profile_json"] = merge["profile_json"]
        if merge.get("analysis_json") and not keep.get("analysis_json"):
            updates["analysis_json"] = merge["analysis_json"]

        # Combine tags
        keep_tags = set()
        merge_tags = set()
        try:
            keep_tags = set(json.loads(keep.get("tags_json") or "[]"))
        except (json.JSONDecodeError, TypeError):
            pass
        try:
            merge_tags = set(json.loads(merge.get("tags_json") or "[]"))
        except (json.JSONDecodeError, TypeError):
            pass
        combined_tags = sorted(keep_tags | merge_tags)
        if combined_tags:
            updates["tags_json"] = json.dumps(combined_tags)

        # Combine notes
        keep_notes = []
        merge_notes = []
        try:
            keep_notes = json.loads(keep.get("notes_json") or "[]")
        except (json.JSONDecodeError, TypeError):
            pass
        try:
            merge_notes = json.loads(merge.get("notes_json") or "[]")
        except (json.JSONDecodeError, TypeError):
            pass
        combined_notes = keep_notes + merge_notes
        if combined_notes:
            updates["notes_json"] = json.dumps(combined_notes)

        # Sum campaigns
        updates["total_campaigns"] = (keep.get("total_campaigns") or 0) + (merge.get("total_campaigns") or 0)

        # Promote lifecycle stage (keep higher)
        keep_stage = keep.get("lifecycle_stage") or "prospect"
        merge_stage = merge.get("lifecycle_stage") or "prospect"
        if _LIFECYCLE_ORDER.get(merge_stage, 0) > _LIFECYCLE_ORDER.get(keep_stage, 0):
            updates["lifecycle_stage"] = merge_stage

        # Apply updates to keep record
        if updates:
            set_clause = ", ".join(f"{k} = ?" for k in updates)
            values = list(updates.values()) + [keep_id]
            db.execute(f"UPDATE global_contacts SET {set_clause} WHERE id = ?", values)

        # Reassign campaign contacts FK
        db.execute(
            "UPDATE contacts SET global_contact_id = ? WHERE global_contact_id = ?",
            (keep_id, merge_id),
        )

        # Delete merged record
        db.execute("DELETE FROM global_contacts WHERE id = ?", (merge_id,))

        db.commit()
        logger.info("Merged global contact %s into %s", merge_id, keep_id)
        db.close()
        return True

    except Exception as e:
        logger.error("merge_global_contacts failed: %s", e)
        db.close()
        return False
