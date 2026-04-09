"""SQLite CRUD helpers for HeyLead."""

from __future__ import annotations

import json
import logging
import sqlite3
import time
import uuid
from typing import Any, Optional

from .schema import get_db

logger = logging.getLogger(__name__)


# ──────────────────────────────────────────────
# Settings (key-value store)
# ──────────────────────────────────────────────

def save_setting(key: str, value: Any) -> None:
    """Save a setting (JSON-serialized)."""
    db = get_db()
    db.execute(
        "INSERT OR REPLACE INTO settings (key, value, updated_at) VALUES (?, ?, ?)",
        (key, json.dumps(value), int(time.time())),
    )
    db.commit()
    db.close()


def get_setting(key: str, default: Any = None) -> Any:
    """Load a setting, returning default if not found."""
    db = get_db()
    row = db.execute("SELECT value FROM settings WHERE key = ?", (key,)).fetchone()
    db.close()
    if row is None:
        return default
    try:
        result = json.loads(row["value"])
        # Handle double-serialized JSON (string containing JSON)
        if isinstance(result, str):
            try:
                result = json.loads(result)
            except (json.JSONDecodeError, TypeError, ValueError):
                pass
        return result
    except (json.JSONDecodeError, TypeError):
        return row["value"]


def delete_setting(key: str) -> None:
    db = get_db()
    db.execute("DELETE FROM settings WHERE key = ?", (key,))
    db.commit()
    db.close()


# ──────────────────────────────────────────────
# Campaigns
# ──────────────────────────────────────────────

def create_campaign(
    name: str,
    icp_json: str = "",
    status: str = "draft",
    mode: str = "autopilot",
    config_json: str = "",
    context_json: str = "",
) -> str:
    """Create a new campaign and return its ID."""
    campaign_id = str(uuid.uuid4())
    now = int(time.time())
    db = get_db()
    db.execute(
        """INSERT INTO campaigns (id, name, icp_json, status, mode, config_json, context_json, created_at, updated_at)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (campaign_id, name, icp_json, status, mode, config_json, context_json, now, now),
    )
    db.commit()
    db.close()
    return campaign_id


def get_campaign(campaign_id: str) -> Optional[dict]:
    db = get_db()
    row = db.execute("SELECT * FROM campaigns WHERE id = ?", (campaign_id,)).fetchone()
    db.close()
    return dict(row) if row else None


def get_campaign_context(campaign_id: str) -> dict:
    """Get parsed campaign context (offerings, case_studies, social_proofs, preferences).

    Returns empty dict if campaign not found or context_json is null.
    """
    campaign = get_campaign(campaign_id)
    if not campaign:
        return {}
    context_raw = campaign.get("context_json", "")
    if not context_raw:
        return {}
    try:
        return json.loads(context_raw)
    except (json.JSONDecodeError, TypeError):
        return {}


def list_campaigns(status: Optional[str] = None) -> list[dict]:
    db = get_db()
    if status:
        rows = db.execute(
            "SELECT * FROM campaigns WHERE status = ? ORDER BY created_at DESC", (status,)
        ).fetchall()
    else:
        rows = db.execute("SELECT * FROM campaigns ORDER BY created_at DESC").fetchall()
    db.close()
    return [dict(r) for r in rows]


_VALID_CAMPAIGN_COLS = frozenset({
    "name", "icp_json", "status", "mode", "config_json", "context_json", "updated_at",
})


def update_campaign(campaign_id: str, **kwargs: Any) -> None:
    db = get_db()
    kwargs["updated_at"] = int(time.time())
    bad_keys = set(kwargs) - _VALID_CAMPAIGN_COLS
    if bad_keys:
        raise ValueError(f"Invalid campaign columns: {bad_keys}")
    set_clause = ", ".join(f"{k} = ?" for k in kwargs)
    values = list(kwargs.values()) + [campaign_id]
    db.execute(f"UPDATE campaigns SET {set_clause} WHERE id = ?", values)
    db.commit()
    db.close()


def find_active_campaign(campaign_id: str = "") -> tuple[Optional[dict], str]:
    """Find a campaign by ID or return first active. Returns (campaign, error_msg)."""
    if campaign_id:
        campaign = get_campaign(campaign_id)
        if not campaign:
            return None, f"Campaign not found: {campaign_id}"
        return campaign, ""
    campaigns = list_campaigns(status="active")
    if not campaigns:
        return None, (
            "No active campaigns.\n\n"
            "Create one first: create_campaign(\"your target description\")"
        )
    return campaigns[0], ""


# ──────────────────────────────────────────────
# Contacts
# ──────────────────────────────────────────────

def save_contact(
    campaign_id: str,
    name: str,
    title: str = "",
    company: str = "",
    linkedin_url: str = "",
    linkedin_id: str = "",
    profile_json: str = "",
    fit_score: float = 0.0,
    source: str = "search",
    source_detail: str = "",
) -> str:
    """Save a contact. If duplicate (campaign_id + linkedin_id), return existing ID.

    Also maintains the global_contacts master record.
    """
    now = int(time.time())
    # Check for existing contact with same linkedin_id in this campaign
    if linkedin_id:
        db = get_db()
        row = db.execute(
            "SELECT id FROM contacts WHERE campaign_id = ? AND linkedin_id = ? LIMIT 1",
            (campaign_id, linkedin_id),
        ).fetchone()
        db.close()
        if row:
            return row["id"]

    # Upsert global contact (master record per person)
    global_contact_id = None
    try:
        from .global_contact_queries import upsert_global_contact
        global_contact_id = upsert_global_contact(
            linkedin_id=linkedin_id,
            name=name,
            title=title,
            company=company,
            linkedin_url=linkedin_url,
            profile_json=profile_json,
            fit_score=fit_score,
            source=source,
            source_detail=source_detail,
            campaign_id=campaign_id,
        )
    except Exception:
        pass  # Non-critical — don't break contact creation

    contact_id = str(uuid.uuid4())
    db = get_db()
    try:
        db.execute(
            """INSERT INTO contacts
               (id, campaign_id, global_contact_id, name, title, company,
                linkedin_url, linkedin_id, profile_json, fit_score,
                source, source_detail, created_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (contact_id, campaign_id, global_contact_id, name, title, company,
             linkedin_url, linkedin_id, profile_json, fit_score,
             source, source_detail, now),
        )
        db.commit()
    except sqlite3.IntegrityError:
        # Unique constraint violation — return existing contact
        row = db.execute(
            "SELECT id FROM contacts WHERE campaign_id = ? AND linkedin_id = ? LIMIT 1",
            (campaign_id, linkedin_id),
        ).fetchone()
        db.close()
        if row:
            return row["id"]
    db.close()
    return contact_id


def get_contacts_for_campaign(campaign_id: str, status: Optional[str] = None) -> list[dict]:
    db = get_db()
    if status:
        rows = db.execute(
            "SELECT * FROM contacts WHERE campaign_id = ? AND status = ?",
            (campaign_id, status),
        ).fetchall()
    else:
        rows = db.execute(
            "SELECT * FROM contacts WHERE campaign_id = ?", (campaign_id,)
        ).fetchall()
    db.close()
    return [dict(r) for r in rows]


_VALID_CONTACT_COLS = frozenset({
    "name", "title", "company", "fit_score", "status", "updated_at",
    "analysis_json", "global_contact_id", "source", "source_detail",
    "profile_json",
})


def update_contact(contact_id: str, **kwargs: Any) -> None:
    """Update contact fields (name, title, company, fit_score, status)."""
    db = get_db()
    kwargs["updated_at"] = int(time.time())
    bad_keys = set(kwargs) - _VALID_CONTACT_COLS
    if bad_keys:
        raise ValueError(f"Invalid contact columns: {bad_keys}")
    set_clause = ", ".join(f"{k} = ?" for k in kwargs)
    values = list(kwargs.values()) + [contact_id]
    db.execute(f"UPDATE contacts SET {set_clause} WHERE id = ?", values)
    db.commit()
    db.close()


def save_contact_analysis(contact_id: str, analysis: dict[str, Any]) -> None:
    """Write prospect analysis to contacts.analysis_json."""
    db = get_db()
    db.execute(
        "UPDATE contacts SET analysis_json = ?, updated_at = ? WHERE id = ?",
        (json.dumps(analysis), int(time.time()), contact_id),
    )
    db.commit()
    db.close()


def get_contact_analysis(contact_id: str) -> dict[str, Any] | None:
    """Load cached prospect analysis from contacts.analysis_json.

    Returns parsed dict or None if not cached.
    """
    db = get_db()
    row = db.execute(
        "SELECT analysis_json FROM contacts WHERE id = ?",
        (contact_id,),
    ).fetchone()
    db.close()
    if not row or not row["analysis_json"]:
        return None
    try:
        return json.loads(row["analysis_json"])
    except (json.JSONDecodeError, TypeError):
        return None


# ──────────────────────────────────────────────
# Outreaches
# ──────────────────────────────────────────────

def create_outreach(
    campaign_id: str,
    contact_id: str,
    status: str = "pending",
    variant: str | None = None,
    signal_id: str | None = None,
) -> str:
    outreach_id = str(uuid.uuid4())
    now = int(time.time())
    db = get_db()
    try:
        db.execute(
            """INSERT INTO outreaches (id, campaign_id, contact_id, status, variant, signal_id, created_at, updated_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (outreach_id, campaign_id, contact_id, status, variant, signal_id, now, now),
        )
        db.commit()
    except sqlite3.IntegrityError:
        # Duplicate (campaign_id, contact_id) — return existing outreach ID
        row = db.execute(
            "SELECT id FROM outreaches WHERE campaign_id = ? AND contact_id = ?",
            (campaign_id, contact_id),
        ).fetchone()
        db.close()
        if row:
            logger.debug("Outreach already exists for contact %s in campaign %s", contact_id, campaign_id)
            return row[0]
        raise  # Unexpected IntegrityError — re-raise
    db.close()
    return outreach_id


_VALID_OUTREACH_COLS = frozenset({
    "status", "next_action", "scheduled_at", "followup_count", "updated_at",
    "outcome_json", "memory_json", "variant", "channel", "signal_id",
    "invited_at", "accepted_at", "first_reply_at",
    "invite_attempts", "last_attempt_error",
})

# Status sets that trigger event timestamps
_INVITED_STATUSES = frozenset({"invited"})
_ACCEPTED_STATUSES = frozenset({
    "connected", "messaged", "replied", "hot_lead",
    "closed_happy", "closed_unhappy", "reverse_pitch", "opted_out",
})
_REPLIED_STATUSES = frozenset({
    "replied", "hot_lead", "closed_happy", "closed_unhappy",
    "reverse_pitch", "opted_out",
})


def _auto_set_event_timestamps(
    db: Any,
    outreach_id: str,
    new_status: str,
    now: int,
    kwargs: dict[str, Any],
) -> None:
    """Auto-populate invited_at/accepted_at/first_reply_at on first occurrence.

    Only sets a timestamp if the column is currently NULL (only-first semantics).
    Mutates kwargs in-place so timestamps are included in the same UPDATE.
    """
    needs_invited = new_status in _INVITED_STATUSES
    needs_accepted = new_status in _ACCEPTED_STATUSES
    needs_reply = new_status in _REPLIED_STATUSES

    if not (needs_invited or needs_accepted or needs_reply):
        return

    row = db.execute(
        "SELECT invited_at, accepted_at, first_reply_at FROM outreaches WHERE id = ?",
        (outreach_id,),
    ).fetchone()
    if not row:
        return
    current = dict(row)

    if needs_invited and current.get("invited_at") is None:
        kwargs["invited_at"] = now
    if needs_accepted and current.get("accepted_at") is None:
        kwargs["accepted_at"] = now
    if needs_reply and current.get("first_reply_at") is None:
        kwargs["first_reply_at"] = now


def update_outreach(outreach_id: str, **kwargs: Any) -> None:
    db = get_db()
    now = int(time.time())
    kwargs["updated_at"] = now

    # Auto-populate event timestamps on first status transition
    new_status = kwargs.get("status")

    # Read old status for audit logging (before the update)
    old_status = None
    if new_status:
        row = db.execute(
            "SELECT status FROM outreaches WHERE id = ?", (outreach_id,)
        ).fetchone()
        old_status = row["status"] if row else None
        _auto_set_event_timestamps(db, outreach_id, new_status, now, kwargs)

    bad_keys = set(kwargs) - _VALID_OUTREACH_COLS
    if bad_keys:
        raise ValueError(f"Invalid outreach columns: {bad_keys}")
    set_clause = ", ".join(f"{k} = ?" for k in kwargs)
    values = list(kwargs.values()) + [outreach_id]
    db.execute(f"UPDATE outreaches SET {set_clause} WHERE id = ?", values)

    # When prospect connects/replies, mark SDR messages as read (inferred read receipt)
    if new_status and new_status in _ACCEPTED_STATUSES and new_status != old_status:
        db.execute(
            "UPDATE messages SET read_at = ? WHERE outreach_id = ? AND role = 'sdr' AND read_at IS NULL",
            (now, outreach_id),
        )

    db.commit()
    db.close()

    # Log status transitions for audit trail
    if new_status and new_status != old_status:
        import traceback as _tb
        # Identify the caller for debugging
        caller = ""
        try:
            frame = _tb.extract_stack(limit=3)
            if len(frame) >= 2:
                caller = f"{frame[-2].filename.split('/')[-1]}:{frame[-2].lineno}"
        except Exception:
            pass
        try:
            log_action(
                "outreach_status_change",
                outreach_id=outreach_id,
                result=new_status,
                details={
                    "old_status": old_status,
                    "new_status": new_status,
                    "source": caller,
                    **{k: v for k, v in kwargs.items()
                       if k in ("followup_count", "channel", "last_attempt_error")},
                },
            )
        except Exception:
            pass  # Non-critical — never break outreach updates

    # Promote global contact lifecycle based on outreach status change
    if new_status:
        try:
            from .global_contact_queries import promote_lifecycle_from_outreach
            promote_lifecycle_from_outreach(outreach_id, new_status)
        except Exception:
            pass  # Non-critical — don't break outreach updates


def skip_pending_outreaches(campaign_id: str) -> int:
    """Mark all pending outreaches for a campaign as skipped. Returns count."""
    db = get_db()
    now = int(time.time())
    cursor = db.execute(
        "UPDATE outreaches SET status = 'skipped', updated_at = ? "
        "WHERE campaign_id = ? AND status = 'pending'",
        (now, campaign_id),
    )
    count = cursor.rowcount
    db.commit()
    db.close()
    return count


def find_followup_count_mismatches() -> list[dict]:
    """Find outreaches where followup_count doesn't match actual sdr message count.

    Returns list of dicts with outreach_id, followup_count, actual_msgs, name.
    Used by daily health check to detect and auto-correct data inconsistencies.
    """
    db = get_db()
    rows = db.execute(
        """SELECT o.id as outreach_id, o.followup_count, o.status,
                  c.name,
                  (SELECT COUNT(*) FROM messages m
                   WHERE m.outreach_id = o.id AND m.role = 'sdr') as actual_msgs
           FROM outreaches o
           JOIN contacts c ON o.contact_id = c.id
           WHERE o.status NOT IN ('pending', 'skipped')
             AND o.followup_count != (
                 SELECT COUNT(*) FROM messages m
                 WHERE m.outreach_id = o.id AND m.role = 'sdr'
             )
           ORDER BY c.name
           LIMIT 50"""
    ).fetchall()
    db.close()
    return [dict(r) for r in rows]


def find_orphaned_outreaches(campaign_id: str, max_followups: int = 2) -> list[dict]:
    """Find connected/messaged outreaches with no pending send_dm or followup jobs.

    These are prospects that fell through the cracks — accepted a connection
    but have no scheduled work. Returns outreaches that need rescue.
    Includes 'messaged' status for DM-only campaigns that skip 'connected'.
    """
    db = get_db()
    rows = db.execute(
        """SELECT o.id as outreach_id, o.campaign_id, o.followup_count,
                  o.accepted_at, o.updated_at as outreach_updated_at,
                  c.name, c.fit_score
           FROM outreaches o
           JOIN contacts c ON o.contact_id = c.id
           WHERE o.campaign_id = ?
             AND o.status IN ('connected', 'messaged')
             AND o.followup_count < ?
             AND o.id NOT IN (
                 SELECT sj.outreach_id FROM scheduler_jobs sj
                 WHERE sj.outreach_id IS NOT NULL
                   AND sj.job_type IN ('send_dm', 'followup')
                   AND sj.status IN ('pending', 'running')
             )
           ORDER BY o.accepted_at ASC NULLS LAST
           LIMIT 10""",
        (campaign_id, max_followups),
    ).fetchall()
    db.close()
    return [dict(r) for r in rows]


def count_open_outreaches(campaign_id: str) -> dict[str, int]:
    """Count outreaches by status that still have pending work (connected, invited).

    Returns dict like {"connected": 12, "invited": 5} for statuses with counts > 0.
    Used by archive_campaign to warn about un-messaged prospects.
    """
    db = get_db()
    rows = db.execute(
        """SELECT status, COUNT(*) as cnt FROM outreaches
           WHERE campaign_id = ? AND status IN ('connected', 'invited')
           GROUP BY status""",
        (campaign_id,),
    ).fetchall()
    db.close()
    return {r["status"]: r["cnt"] for r in rows}


def get_outreach(outreach_id: str) -> Optional[dict]:
    """Get a single outreach by ID."""
    db = get_db()
    row = db.execute("SELECT * FROM outreaches WHERE id = ?", (outreach_id,)).fetchone()
    db.close()
    return dict(row) if row else None


def get_outreach_memory(outreach_id: str) -> list[dict]:
    """Get structured conversation memory for an outreach.

    Returns a list of per-followup decision records (cta_used, pain_used,
    greeting, structure, etc.) used for anti-repetition in future follow-ups.
    """
    outreach = get_outreach(outreach_id)
    if not outreach:
        return []
    raw = outreach.get("memory_json", "")
    if not raw:
        return []
    try:
        memory = json.loads(raw)
        return memory if isinstance(memory, list) else []
    except (json.JSONDecodeError, TypeError):
        return []


def save_outreach_memory(outreach_id: str, memory_entry: dict) -> None:
    """Append a follow-up memory entry to the outreach's memory_json.

    Each entry captures what was used in a specific follow-up
    (CTA, pain angle, greeting, structure, etc.) so future
    follow-ups can avoid repeating the same patterns.
    """
    existing = get_outreach_memory(outreach_id)
    existing.append(memory_entry)
    update_outreach(outreach_id, memory_json=json.dumps(existing))


def get_outreach_with_contact(outreach_id: str) -> Optional[dict]:
    """Get outreach data merged with contact info for tool display."""
    db = get_db()
    row = db.execute(
        """SELECT o.id as outreach_id, o.campaign_id, o.contact_id,
                  o.status, o.followup_count, o.next_action, o.updated_at,
                  c.name, c.title, c.company, c.linkedin_url, c.linkedin_id,
                  c.fit_score, c.profile_json, c.analysis_json
           FROM outreaches o
           JOIN contacts c ON o.contact_id = c.id
           WHERE o.id = ?""",
        (outreach_id,),
    ).fetchone()
    db.close()
    return dict(row) if row else None


def count_outreaches_by_status(campaign_id: str, status: str) -> int:
    """Count outreaches with a given status in a campaign."""
    db = get_db()
    row = db.execute(
        "SELECT COUNT(*) as cnt FROM outreaches WHERE campaign_id = ? AND status = ?",
        (campaign_id, status),
    ).fetchone()
    db.close()
    return row["cnt"] if row else 0


def get_next_pending_outreach(campaign_id: str, exclude_job_type: str = "") -> Optional[dict]:
    """Get the next pending outreach for a campaign, ordered by fit_score DESC.

    Used by the planner to bind scheduler jobs to specific outreaches,
    preventing duplicate sends when multiple schedulers are active.

    If *exclude_job_type* is given, outreaches that already have a
    pending/running job of that type are skipped so the planner doesn't
    get stuck on the same top-ranked prospect every tick.
    """
    db = get_db()
    if exclude_job_type:
        row = db.execute(
            """SELECT o.id, o.contact_id, c.fit_score
               FROM outreaches o
               JOIN contacts c ON o.contact_id = c.id
               WHERE o.campaign_id = ? AND o.status = 'pending'
                 AND o.id NOT IN (
                     SELECT sj.outreach_id FROM scheduler_jobs sj
                     WHERE sj.outreach_id IS NOT NULL
                       AND sj.job_type = ?
                       AND sj.status IN ('pending', 'running')
                 )
               ORDER BY c.fit_score DESC
               LIMIT 1""",
            (campaign_id, exclude_job_type),
        ).fetchone()
    else:
        row = db.execute(
            """SELECT o.id, o.contact_id, c.fit_score
               FROM outreaches o
               JOIN contacts c ON o.contact_id = c.id
               WHERE o.campaign_id = ? AND o.status = 'pending'
               ORDER BY c.fit_score DESC
               LIMIT 1""",
            (campaign_id,),
        ).fetchone()
    db.close()
    return dict(row) if row else None


def get_next_dm_candidate(
    campaign_id: str,
    exclude_job_type: str = "",
    only_connected: bool = False,
) -> Optional[dict]:
    """Get next outreach needing a first DM.

    Picks prospects that haven't been messaged yet (followup_count=0, no
    existing SDR messages, no recent send_dm jobs).  Ordered by fit_score DESC.

    When *only_connected* is True, restricts to 'connected' status only — used
    when invitations are enabled so we don't race DMs against pending invites.
    When False (DM-only / connections-only campaigns), includes 'pending' too.
    """
    db = get_db()
    statuses = "('connected')" if only_connected else "('pending', 'connected')"
    # Exclude outreaches that:
    # 1. Have pending/running send_dm jobs (dedup)
    # 2. Have any completed send_dm jobs in last 24h (prevent race-condition re-picks)
    # 3. Already have SDR messages (hard guard against re-messaging)
    row = db.execute(
        f"""SELECT o.id, o.contact_id, c.fit_score
           FROM outreaches o
           JOIN contacts c ON o.contact_id = c.id
           WHERE o.campaign_id = ?
             AND o.status IN {statuses}
             AND o.followup_count = 0
             AND NOT EXISTS (
                 SELECT 1 FROM scheduler_jobs sj
                 WHERE sj.outreach_id = o.id
                   AND sj.job_type = ?
                   AND (sj.status IN ('pending', 'running')
                        OR (sj.status = 'completed' AND sj.completed_at > ?))
             )
             AND NOT EXISTS (
                 SELECT 1 FROM messages m
                 WHERE m.outreach_id = o.id AND m.role = 'sdr'
             )
           ORDER BY c.fit_score DESC
           LIMIT 1""",
        (campaign_id, exclude_job_type or "send_dm", int(time.time()) - 86400),
    ).fetchone()
    db.close()
    return dict(row) if row else None


def get_followup_candidates(
    campaign_id: str,
    max_followups: int = 2,
) -> list[dict]:
    """Find outreaches ready for follow-up.

    Returns outreaches with status 'connected' or 'messaged' and followup_count < max_followups,
    joined with contact data. Ordered by updated_at ASC (oldest first = most overdue).
    'messaged' is included because DM-only campaigns skip 'connected' status entirely.
    """
    db = get_db()
    rows = db.execute(
        """SELECT o.id as outreach_id, o.campaign_id, o.contact_id, o.status,
                  o.followup_count, o.updated_at as outreach_updated_at,
                  o.accepted_at,
                  c.name, c.title, c.company, c.linkedin_url, c.linkedin_id,
                  c.profile_json, c.fit_score
           FROM outreaches o
           JOIN contacts c ON o.contact_id = c.id
           WHERE o.campaign_id = ?
             AND o.status IN ('connected', 'messaged')
             AND o.followup_count < ?
           ORDER BY o.accepted_at ASC NULLS LAST""",
        (campaign_id, max_followups),
    ).fetchall()
    db.close()
    return [dict(r) for r in rows]


def count_followup_ready(campaign_id: str, max_followups: int = 2) -> int:
    """Count outreaches ready for follow-up in a campaign."""
    db = get_db()
    row = db.execute(
        """SELECT COUNT(*) as c FROM outreaches
           WHERE campaign_id = ? AND status IN ('connected', 'messaged') AND followup_count < ?""",
        (campaign_id, max_followups),
    ).fetchone()
    db.close()
    return row["c"] if row else 0


def get_followup_breakdown(campaign_id: str, max_followups: int = 2) -> dict:
    """Detailed breakdown of why follow-up candidates are/aren't eligible.

    Returns counts for: total connected/messaged, eligible (under max),
    maxed out, and per-followup_count distribution.
    """
    db = get_db()
    # Total connected + messaged
    row = db.execute(
        """SELECT COUNT(*) as c FROM outreaches
           WHERE campaign_id = ? AND status IN ('connected', 'messaged')""",
        (campaign_id,),
    ).fetchone()
    total = row["c"] if row else 0

    # Under max followups (eligible pool)
    row = db.execute(
        """SELECT COUNT(*) as c FROM outreaches
           WHERE campaign_id = ? AND status IN ('connected', 'messaged')
             AND followup_count < ?""",
        (campaign_id, max_followups),
    ).fetchone()
    eligible = row["c"] if row else 0

    # Maxed out
    maxed = total - eligible

    # Distribution by followup_count
    rows = db.execute(
        """SELECT followup_count, COUNT(*) as c FROM outreaches
           WHERE campaign_id = ? AND status IN ('connected', 'messaged')
           GROUP BY followup_count ORDER BY followup_count""",
        (campaign_id,),
    ).fetchall()
    distribution = {r["followup_count"]: r["c"] for r in rows}

    # By status
    rows = db.execute(
        """SELECT status, COUNT(*) as c FROM outreaches
           WHERE campaign_id = ? AND status IN ('connected', 'messaged')
           GROUP BY status""",
        (campaign_id,),
    ).fetchall()
    by_status = {r["status"]: r["c"] for r in rows}

    db.close()
    return {
        "total": total,
        "eligible": eligible,
        "maxed_out": maxed,
        "max_followups": max_followups,
        "distribution": distribution,
        "by_status": by_status,
    }


def get_reply_candidates(campaign_id: str | None = None) -> list[dict]:
    """Find outreaches needing a reply, prioritized by sentiment urgency.

    Args:
        campaign_id: Filter to a specific campaign. None or "" = inbound (no campaign).

    Returns outreaches where the last message is from the prospect.
    Ordered by sentiment priority: positive > question > neutral > negative.
    """
    db = get_db()
    if campaign_id:
        where = "o.campaign_id = ?"
        params: tuple = (campaign_id,)
    else:
        where = "(o.campaign_id = '' OR o.campaign_id IS NULL)"
        params = ()
    rows = db.execute(
        f"""SELECT o.id as outreach_id, o.campaign_id, o.contact_id,
                  o.status, o.followup_count, o.updated_at as outreach_updated_at,
                  c.name, c.title, c.company, c.linkedin_url, c.linkedin_id,
                  c.profile_json, c.fit_score,
                  c.id as contact_db_id,
                  m.text as last_reply_text,
                  m.sentiment as last_sentiment
           FROM outreaches o
           JOIN contacts c ON o.contact_id = c.id
           JOIN messages m ON m.outreach_id = o.id
           WHERE {where}
             AND o.status IN ('hot_lead', 'replied', 'connected', 'messaged')
             AND m.role = 'prospect'
             AND m.id = (
                 SELECT m2.id FROM messages m2
                 WHERE m2.outreach_id = o.id
                 ORDER BY m2.timestamp DESC LIMIT 1
             )
             -- Cross-outreach dedup: when the same person is in multiple
             -- campaigns, skip this outreach if any sibling outreach has
             -- already replied (SDR message) after the prospect's latest
             -- message here. Without this, every campaign's auto-reply job
             -- independently fires into the same LinkedIn chat.
             AND NOT EXISTS (
                 SELECT 1
                 FROM outreaches o2
                 JOIN contacts c2 ON o2.contact_id = c2.id
                 JOIN messages m2 ON m2.outreach_id = o2.id
                 WHERE o2.id != o.id
                   AND m2.role = 'sdr'
                   AND m2.timestamp >= m.timestamp
                   AND (
                        (c.global_contact_id IS NOT NULL
                         AND c2.global_contact_id = c.global_contact_id)
                     OR (c.linkedin_id IS NOT NULL AND c.linkedin_id != ''
                         AND c2.linkedin_id = c.linkedin_id)
                   )
             )
           ORDER BY
             CASE m.sentiment
               WHEN 'positive' THEN 1
               WHEN 'engaged' THEN 2
               WHEN 'question' THEN 3
               WHEN 'neutral' THEN 4
               WHEN 'negative' THEN 5
               ELSE 6
             END,
             o.updated_at ASC""",
        params,
    ).fetchall()
    db.close()
    return [dict(r) for r in rows]


# Backward-compatible alias for inbound callers
def get_inbound_reply_candidates() -> list[dict]:
    """Find inbound (campaign-less) outreaches needing a reply."""
    return get_reply_candidates(campaign_id=None)


def get_auto_reply_candidates(campaign_id: str | None = None, min_age_seconds: int = 300) -> list[dict]:
    """Find outreaches needing auto-reply, with minimum age since last prospect message.

    Args:
        campaign_id: Filter to a specific campaign. None or "" = inbound (no campaign).
        min_age_seconds: Minimum age of last prospect message (prevents instant replies).

    Also excludes opt_out/out_of_office/negative sentiments and outreaches with
    pending auto_reply jobs (ignores stale 'running' jobs older than 10 min).
    Additionally excludes outreaches where an SDR message already exists after the
    last prospect message (prevents duplicate replies from concurrent jobs).
    """
    now = int(time.time())
    cutoff = now - min_age_seconds
    stale_cutoff = now - 600  # 10 min TTL for running jobs
    recently_completed = now - 1800  # 30 min cooldown for completed jobs
    db = get_db()
    if campaign_id:
        where = "o.campaign_id = ?"
        params: tuple = (campaign_id, cutoff, stale_cutoff, recently_completed)
    else:
        where = "(o.campaign_id = '' OR o.campaign_id IS NULL)"
        params = (cutoff, stale_cutoff, recently_completed)
    rows = db.execute(
        f"""SELECT o.id as outreach_id, o.campaign_id, o.contact_id,
                  o.status, o.followup_count, o.updated_at as outreach_updated_at,
                  c.name, c.title, c.company, c.linkedin_url, c.linkedin_id,
                  c.profile_json, c.fit_score,
                  c.id as contact_db_id,
                  m.text as last_reply_text,
                  m.sentiment as last_sentiment,
                  m.timestamp as last_message_ts
           FROM outreaches o
           JOIN contacts c ON o.contact_id = c.id
           JOIN messages m ON m.outreach_id = o.id
           WHERE {where}
             AND o.status IN ('hot_lead', 'replied', 'connected', 'messaged')
             AND m.role = 'prospect'
             AND m.sentiment NOT IN ('opt_out', 'out_of_office', 'negative', 'positive', 'calendar')
             AND m.id = (
                 SELECT m2.id FROM messages m2
                 WHERE m2.outreach_id = o.id
                 ORDER BY m2.timestamp DESC LIMIT 1
             )
             AND m.timestamp <= ?
             AND o.id NOT IN (
                 SELECT sj.outreach_id FROM scheduler_jobs sj
                 WHERE sj.outreach_id = o.id
                   AND sj.job_type = 'auto_reply'
                   AND (
                       sj.status = 'pending'
                       OR (sj.status = 'running' AND sj.started_at > ?)
                       OR (sj.status = 'completed' AND sj.completed_at > ?)
                   )
             )
             AND (
                 SELECT COUNT(*) FROM scheduler_jobs sj2
                 WHERE sj2.outreach_id = o.id
                   AND sj2.job_type = 'auto_reply'
                   AND sj2.status = 'failed'
             ) < 3
             AND (
                 SELECT COUNT(*) FROM actions_log al
                 WHERE al.outreach_id = o.id
                   AND al.action_type = 'chat_not_found'
             ) < 3
             AND NOT EXISTS (
                 SELECT 1 FROM messages mx
                 WHERE mx.outreach_id = o.id
                   AND mx.role = 'sdr'
                   AND mx.timestamp >= m.timestamp
             )
           ORDER BY
             CASE m.sentiment
               WHEN 'positive' THEN 1
               WHEN 'engaged' THEN 2
               WHEN 'question' THEN 3
               WHEN 'neutral' THEN 4
               WHEN 'negative' THEN 5
               ELSE 6
             END,
             o.updated_at ASC""",
        params,
    ).fetchall()
    db.close()
    return [dict(r) for r in rows]


# Backward-compatible alias for inbound callers
def get_inbound_auto_reply_candidates(min_age_seconds: int = 300) -> list[dict]:
    """Find inbound (campaign-less) outreaches needing auto-reply."""
    return get_auto_reply_candidates(campaign_id=None, min_age_seconds=min_age_seconds)


def get_daily_auto_reply_count() -> int:
    """Count auto-replies sent today (via actions_log)."""
    today_start = int(time.time()) - (int(time.time()) % 86400)
    db = get_db()
    row = db.execute(
        """SELECT COUNT(*) as cnt FROM actions_log
           WHERE action_type = 'auto_reply_sent'
             AND timestamp >= ?""",
        (today_start,),
    ).fetchone()
    db.close()
    return row["cnt"] if row else 0


def get_pending_approval() -> Optional[dict]:
    """Find the most recently updated outreach with a pending approval.

    Returns the outreach with a non-null next_action field, ordered by
    updated_at DESC (most recent first). Excludes scheduler cooldown
    entries (skip_engagement_until) which are not real pending approvals.
    """
    db = get_db()
    row = db.execute(
        """SELECT * FROM outreaches
           WHERE next_action IS NOT NULL AND next_action != ''
             AND next_action NOT LIKE '%skip_engagement_until%'
           ORDER BY updated_at DESC LIMIT 1"""
    ).fetchone()
    db.close()
    return dict(row) if row else None


# ──────────────────────────────────────────────
# Messages
# ──────────────────────────────────────────────

def save_message(
    outreach_id: str,
    role: str,
    text: str,
    sentiment: str = "",
    format: str = "text",
) -> str:
    db = get_db()
    # Dedup: skip if an identical message (same outreach, role, text) already exists.
    # This prevents duplicate entries from concurrent check_replies runs.
    existing = db.execute(
        "SELECT id FROM messages WHERE outreach_id = ? AND role = ? AND text = ? LIMIT 1",
        (outreach_id, role, text),
    ).fetchone()
    if existing:
        db.close()
        return existing[0] if isinstance(existing, (tuple, list)) else existing["id"]
    msg_id = str(uuid.uuid4())
    db.execute(
        """INSERT INTO messages (id, outreach_id, role, text, sentiment, format, timestamp)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (msg_id, outreach_id, role, text, sentiment, format, int(time.time())),
    )
    db.commit()
    db.close()
    return msg_id


def get_messages_for_outreach(outreach_id: str) -> list[dict]:
    db = get_db()
    rows = db.execute(
        "SELECT * FROM messages WHERE outreach_id = ? ORDER BY timestamp ASC",
        (outreach_id,),
    ).fetchall()
    db.close()
    return [dict(r) for r in rows]


def mark_message_read(message_id: str, read_at: int | None = None) -> None:
    """Mark a message as read by the prospect."""
    db = get_db()
    db.execute(
        "UPDATE messages SET read_at = ? WHERE id = ? AND read_at IS NULL",
        (read_at or int(time.time()), message_id),
    )
    db.commit()
    db.close()


def mark_message_deleted(message_id: str, deleted_at: int | None = None) -> None:
    """Mark a local message as deleted on LinkedIn."""
    db = get_db()
    db.execute(
        "UPDATE messages SET deleted_at = ? WHERE id = ?",
        (deleted_at or int(time.time()), message_id),
    )
    db.commit()
    db.close()


def set_message_external_id(message_id: str, external_message_id: str) -> None:
    """Store the Unipile message ID on a local message record."""
    db = get_db()
    db.execute(
        "UPDATE messages SET external_message_id = ? WHERE id = ?",
        (external_message_id, message_id),
    )
    db.commit()
    db.close()


def get_last_sdr_message(outreach_id: str) -> dict | None:
    """Get the most recent SDR message for an outreach (not deleted)."""
    db = get_db()
    row = db.execute(
        """SELECT * FROM messages
           WHERE outreach_id = ? AND role = 'sdr' AND deleted_at IS NULL
           ORDER BY timestamp DESC LIMIT 1""",
        (outreach_id,),
    ).fetchone()
    db.close()
    return dict(row) if row else None


def get_read_rate(campaign_id: str) -> dict:
    """Calculate read rate for SDR messages in a campaign.

    Returns: {"total_sdr_messages": int, "read_messages": int, "read_rate": float}
    """
    db = get_db()
    row = db.execute(
        """SELECT
               COUNT(*) as total,
               SUM(CASE WHEN m.read_at IS NOT NULL THEN 1 ELSE 0 END) as read_count
           FROM messages m
           JOIN outreaches o ON m.outreach_id = o.id
           WHERE o.campaign_id = ? AND m.role = 'sdr'""",
        (campaign_id,),
    ).fetchone()
    db.close()
    total = row["total"] if row else 0
    read_count = row["read_count"] if row else 0
    return {
        "total_sdr_messages": total,
        "read_messages": read_count,
        "read_rate": read_count / total if total > 0 else 0.0,
    }


# ──────────────────────────────────────────────
# Actions Log
# ──────────────────────────────────────────────

def log_action(
    action_type: str,
    outreach_id: str = "",
    result: str = "",
    details: Any = None,
    campaign_id: str = "",
) -> str:
    action_id = str(uuid.uuid4())
    db = get_db()
    db.execute(
        """INSERT INTO actions_log (id, outreach_id, action_type, result, details_json, timestamp, campaign_id)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (action_id, outreach_id or None, action_type, result,
         json.dumps(details) if details else None, int(time.time()),
         campaign_id or None),
    )
    db.commit()
    db.close()
    return action_id


def get_campaign_status_history(campaign_id: str = "", limit: int = 50) -> list[dict]:
    """Get campaign status change audit log.

    Returns list of dicts with: timestamp, campaign_id, campaign_name,
    old_status, new_status, changed_by, reason.
    """
    db = get_db()
    if campaign_id:
        rows = db.execute(
            """SELECT timestamp, details_json FROM actions_log
               WHERE action_type = 'campaign_status_change'
                 AND details_json LIKE ?
               ORDER BY timestamp DESC LIMIT ?""",
            (f'%"campaign_id": "{campaign_id}"%', limit),
        ).fetchall()
    else:
        rows = db.execute(
            """SELECT timestamp, details_json FROM actions_log
               WHERE action_type = 'campaign_status_change'
               ORDER BY timestamp DESC LIMIT ?""",
            (limit,),
        ).fetchall()
    db.close()
    result = []
    for row in rows:
        details = json.loads(row[1] or "{}")
        details["timestamp"] = row[0]
        result.append(details)
    return result


def get_actions_taken(hours: int = 24, campaign_id: str = "") -> dict[str, dict]:
    """Time-windowed action results from actions_log (excludes skip_ entries).

    Returns: {action_type: {"total": N, "success": N, "error": N, "blocked": N, ...}}
    """
    db = get_db()
    since = int(time.time()) - (hours * 3600)
    sql = """SELECT action_type, result, COUNT(*) as cnt
             FROM actions_log
             WHERE timestamp >= ? AND action_type NOT LIKE 'skip_%'"""
    params: list[Any] = [since]
    if campaign_id:
        sql += " AND campaign_id = ?"
        params.append(campaign_id)
    sql += " GROUP BY action_type, result"
    rows = db.execute(sql, params).fetchall()
    db.close()

    actions: dict[str, dict] = {}
    for r in rows:
        at = r["action_type"]
        res = r["result"] or "unknown"
        cnt = r["cnt"]
        if at not in actions:
            actions[at] = {"total": 0}
        actions[at]["total"] += cnt
        actions[at][res] = actions[at].get(res, 0) + cnt
    return actions


def get_actions_skipped(hours: int = 24, campaign_id: str = "") -> dict[str, int]:
    """Time-windowed skip reasons from actions_log (skip_* entries).

    Returns: {reason: count} e.g. {"daily_limit": 23, "no_candidates": 12}
    """
    db = get_db()
    since = int(time.time()) - (hours * 3600)
    sql = """SELECT json_extract(details_json, '$.reason') as reason, COUNT(*) as cnt
             FROM actions_log
             WHERE timestamp >= ? AND action_type LIKE 'skip_%'"""
    params: list[Any] = [since]
    if campaign_id:
        sql += " AND campaign_id = ?"
        params.append(campaign_id)
    sql += " GROUP BY reason ORDER BY cnt DESC"
    rows = db.execute(sql, params).fetchall()
    db.close()

    return {r["reason"] or "unknown": r["cnt"] for r in rows}


def get_actions_skipped_detailed(hours: int = 24, campaign_id: str = "") -> dict[str, dict[str, int]]:
    """Time-windowed skip reasons grouped by action type.

    Returns: {reason: {action_type_suffix: count}} e.g. {"daily_limit": {"follow": 5, "engage": 3}}
    """
    db = get_db()
    since = int(time.time()) - (hours * 3600)
    sql = """SELECT action_type,
                    json_extract(details_json, '$.reason') as reason,
                    COUNT(*) as cnt
             FROM actions_log
             WHERE timestamp >= ? AND action_type LIKE 'skip_%'"""
    params: list[Any] = [since]
    if campaign_id:
        sql += " AND campaign_id = ?"
        params.append(campaign_id)
    sql += " GROUP BY action_type, reason ORDER BY cnt DESC"
    rows = db.execute(sql, params).fetchall()
    db.close()

    result: dict[str, dict[str, int]] = {}
    for r in rows:
        reason = r["reason"] or "unknown"
        # Extract action suffix: "skip_follow" → "follow"
        action = (r["action_type"] or "").removeprefix("skip_")
        if reason not in result:
            result[reason] = {}
        result[reason][action] = r["cnt"]
    return result


def get_outreach_changes(hours: int = 24, campaign_id: str = "") -> dict[str, Any]:
    """Time-windowed real state changes from outreaches/engagements/messages.

    Returns dict with counts of actual LinkedIn results in the time window.
    """
    db = get_db()
    since = int(time.time()) - (hours * 3600)

    campaign_filter = ""
    params_base: list[Any] = [since]
    if campaign_id:
        campaign_filter = " AND campaign_id = ?"
        params_base = [since, campaign_id]

    # Invitations sent (invited_at in window, verified only)
    row = db.execute(
        f"SELECT COUNT(*) as cnt FROM outreaches WHERE invited_at >= ? AND verified_status = 'confirmed'{campaign_filter}",
        params_base,
    ).fetchone()
    invited = row["cnt"] if row else 0

    # Invitations pending verification
    row = db.execute(
        f"SELECT COUNT(*) as cnt FROM outreaches WHERE invited_at >= ? AND (verified_status IS NULL OR verified_status = ''){campaign_filter}",
        params_base,
    ).fetchone()
    invited_pending = row["cnt"] if row else 0

    # Acceptances (accepted_at in window)
    row = db.execute(
        f"SELECT COUNT(*) as cnt FROM outreaches WHERE accepted_at >= ?{campaign_filter}",
        params_base,
    ).fetchone()
    accepted = row["cnt"] if row else 0

    # Replies (first_reply_at in window)
    row = db.execute(
        f"SELECT COUNT(*) as cnt FROM outreaches WHERE first_reply_at >= ?{campaign_filter}",
        params_base,
    ).fetchone()
    replied = row["cnt"] if row else 0

    # Messages sent (role='sdr' in window)
    if campaign_id:
        msg_sql = """SELECT role, COUNT(*) as cnt FROM messages
                     WHERE timestamp >= ? AND outreach_id IN
                       (SELECT id FROM outreaches WHERE campaign_id = ?)
                     GROUP BY role"""
        msg_params: list[Any] = [since, campaign_id]
    else:
        msg_sql = "SELECT role, COUNT(*) as cnt FROM messages WHERE timestamp >= ? GROUP BY role"
        msg_params = [since]
    msg_rows = db.execute(msg_sql, msg_params).fetchall()
    messages_sent = 0
    messages_received = 0
    for r in msg_rows:
        if r["role"] == "sdr":
            messages_sent = r["cnt"]
        elif r["role"] == "prospect":
            messages_received = r["cnt"]

    # Engagements by type in window (verified only)
    if campaign_id:
        eng_sql = """SELECT action_type, COUNT(*) as cnt FROM engagements
                     WHERE created_at >= ? AND verified_status IN ('verified', 'trust_api')
                       AND outreach_id IN
                       (SELECT id FROM outreaches WHERE campaign_id = ?)
                     GROUP BY action_type"""
        eng_params: list[Any] = [since, campaign_id]
    else:
        eng_sql = """SELECT action_type, COUNT(*) as cnt FROM engagements
                     WHERE created_at >= ? AND verified_status IN ('verified', 'trust_api')
                     GROUP BY action_type"""
        eng_params = [since]
    eng_rows = db.execute(eng_sql, eng_params).fetchall()
    engagements = {r["action_type"]: r["cnt"] for r in eng_rows}

    # Engagements pending verification
    if campaign_id:
        eng_pend_sql = """SELECT action_type, COUNT(*) as cnt FROM engagements
                     WHERE created_at >= ? AND (verified_status IS NULL OR verified_status = '')
                       AND outreach_id IN
                       (SELECT id FROM outreaches WHERE campaign_id = ?)
                     GROUP BY action_type"""
        eng_pend_params: list[Any] = [since, campaign_id]
    else:
        eng_pend_sql = """SELECT action_type, COUNT(*) as cnt FROM engagements
                     WHERE created_at >= ? AND (verified_status IS NULL OR verified_status = '')
                     GROUP BY action_type"""
        eng_pend_params = [since]
    eng_pend_rows = db.execute(eng_pend_sql, eng_pend_params).fetchall()
    engagements_pending = {r["action_type"]: r["cnt"] for r in eng_pend_rows}

    db.close()

    return {
        "invited": invited,
        "invited_pending": invited_pending,
        "accepted": accepted,
        "replied": replied,
        "messages_sent": messages_sent,
        "messages_received": messages_received,
        "engagements": engagements,
        "engagements_pending": engagements_pending,
    }


def get_verification_summary(hours: int = 24) -> dict[str, int]:
    """Summary of post-action verification results.

    Returns: {"confirmed": N, "unconfirmed": N, "pending": N}
    """
    db = get_db()
    since = int(time.time()) - (hours * 3600)

    # Verified outreaches in window
    rows = db.execute(
        """SELECT verified_status, COUNT(*) as cnt FROM outreaches
           WHERE verified_at >= ? AND verified_at IS NOT NULL
           GROUP BY verified_status""",
        (since,),
    ).fetchall()
    result = {r["verified_status"]: r["cnt"] for r in rows if r["verified_status"]}

    # Pending verification (invited recently, not yet verified)
    row = db.execute(
        """SELECT COUNT(*) as cnt FROM outreaches
           WHERE invited_at >= ? AND verified_at IS NULL AND status = 'invited'""",
        (since,),
    ).fetchone()
    result["pending"] = row["cnt"] if row else 0

    db.close()
    return result


# ──────────────────────────────────────────────
# Rate Limits
# ──────────────────────────────────────────────

def get_rate_limit_today() -> dict:
    """Get or create today's rate limit record."""
    from datetime import date, timedelta

    from .. import constants as _c

    today = date.today().isoformat()
    db = get_db()
    row = db.execute("SELECT * FROM rate_limits WHERE date = ?", (today,)).fetchone()
    if row is None:
        rid = str(uuid.uuid4())
        # Carry forward yesterday's adaptive limit
        yesterday = (date.today() - timedelta(days=1)).isoformat()
        prev = db.execute(
            "SELECT daily_limit FROM rate_limits WHERE date = ?", (yesterday,)
        ).fetchone()
        initial = prev["daily_limit"] if prev else 15
        db.execute(
            """INSERT INTO rate_limits (id, date, sent, accepted, daily_limit, blocked, updated_at)
               VALUES (?, ?, 0, 0, ?, 0, ?)""",
            (rid, today, initial, int(time.time())),
        )
        db.commit()
        row = db.execute("SELECT * FROM rate_limits WHERE date = ?", (today,)).fetchone()
    db.close()
    return dict(row)


def increment_sent() -> None:
    from datetime import date
    today = date.today().isoformat()
    db = get_db()
    db.execute(
        "UPDATE rate_limits SET sent = sent + 1, updated_at = ? WHERE date = ?",
        (int(time.time()), today),
    )
    db.commit()
    db.close()


def increment_accepted() -> None:
    from datetime import date
    today = date.today().isoformat()
    db = get_db()
    db.execute(
        "UPDATE rate_limits SET accepted = accepted + 1, updated_at = ? WHERE date = ?",
        (int(time.time()), today),
    )
    db.commit()
    db.close()


def update_daily_limit(new_limit: int) -> None:
    from datetime import date
    today = date.today().isoformat()
    db = get_db()
    db.execute(
        "UPDATE rate_limits SET daily_limit = ?, updated_at = ? WHERE date = ?",
        (new_limit, int(time.time()), today),
    )
    db.commit()
    db.close()


def get_rate_limit_budget() -> dict[str, dict]:
    """Get today's budget remaining per action type.

    Counts completed scheduler_jobs today for warm-up actions, and uses
    rate_limits table for invitations.

    Returns: {action_type: {used_today, limit, remaining, pct_used}}
    """
    from datetime import date

    from .. import constants as _c

    today_start = int(
        __import__("datetime").datetime.combine(
            date.today(), __import__("datetime").time.min
        ).timestamp()
    )

    # Invitation budget from rate_limits table
    rl = get_rate_limit_today()
    inv_sent = rl.get("sent", 0)
    inv_limit = rl.get("daily_limit", 15)

    # Warm-up budgets from scheduler_jobs completed today
    db = get_db()
    rows = db.execute(
        """SELECT job_type, COUNT(*) as cnt
           FROM scheduler_jobs
           WHERE status = 'completed'
             AND completed_at >= ?
           GROUP BY job_type""",
        (today_start,),
    ).fetchall()
    db.close()

    counts: dict[str, int] = {r["job_type"]: r["cnt"] for r in rows}

    limits = {
        "invitations": (15, inv_sent, inv_limit),
        "follows": (None, counts.get("follow", 0), None),
        "engagements": (None, counts.get("engage", 0), None),
        "profile_views": (None, counts.get("profile_view_warmup", 0), None),
        "endorsements": (None, counts.get("endorse", 0), None),
        "followups": (None, counts.get("followup", 0), None),
        "dms": (None, counts.get("send_dm", 0), None),
    }

    budget: dict[str, dict] = {}
    for action, (_default_limit, used, limit) in limits.items():
        if action == "invitations":
            # Use adaptive limit from rate_limits table
            remaining = max(0, inv_limit - inv_sent)
            pct = round(inv_sent / inv_limit * 100, 1) if inv_limit else 0
        elif limit is not None:
            remaining = max(0, limit - used)
            pct = round(used / limit * 100, 1) if limit else 0
        else:
            remaining = None
            pct = None
        budget[action] = {
            "used_today": used,
            "limit": limit,
            "remaining": remaining,
            "pct_used": pct,
        }

    return budget


def get_warmup_effectiveness(campaign_id: str = "") -> dict:
    """Compare acceptance/reply rates for warmed-up vs direct-invite prospects.

    A prospect is "warmed up" if they have engagements created before
    their invitation was sent.

    Returns dict with warmed_up, direct_invite groups and lift metrics.
    """
    db = get_db()
    # Get all outreaches that were invited
    sql = """
        SELECT
            o.id as outreach_id,
            o.invited_at,
            o.accepted_at,
            o.first_reply_at,
            (SELECT COUNT(*) FROM engagements e
             WHERE e.outreach_id = o.id
               AND e.created_at < o.invited_at) as warmup_count
        FROM outreaches o
        WHERE o.invited_at IS NOT NULL
    """
    params: list[Any] = []
    if campaign_id:
        sql += " AND o.campaign_id = ?"
        params.append(campaign_id)

    rows = db.execute(sql, params).fetchall()
    db.close()

    groups: dict[str, dict] = {
        "warmed_up": {"total": 0, "accepted": 0, "replied": 0, "days_sum": 0, "warmup_actions_sum": 0},
        "direct_invite": {"total": 0, "accepted": 0, "replied": 0, "days_sum": 0},
    }

    for r in rows:
        warmup_count = r["warmup_count"] or 0
        group = "warmed_up" if warmup_count > 0 else "direct_invite"
        g = groups[group]
        g["total"] += 1
        if r["accepted_at"]:
            g["accepted"] += 1
            days = (r["accepted_at"] - r["invited_at"]) / 86400
            g["days_sum"] += days
        if r["first_reply_at"]:
            g["replied"] += 1
        if group == "warmed_up":
            g["warmup_actions_sum"] += warmup_count

    result: dict[str, Any] = {}
    for group_name, g in groups.items():
        total = g["total"]
        accepted = g["accepted"]
        replied = g["replied"]
        result[group_name] = {
            "total": total,
            "accepted": accepted,
            "acceptance_rate": round(accepted / total * 100, 1) if total else 0,
            "replied": replied,
            "reply_rate": round(replied / total * 100, 1) if total else 0,
            "avg_days_to_accept": round(g["days_sum"] / accepted, 1) if accepted else None,
        }
        if group_name == "warmed_up":
            result[group_name]["warmup_actions_avg"] = (
                round(g["warmup_actions_sum"] / total, 1) if total else 0
            )

    # Compute lift
    wu = result.get("warmed_up", {})
    di = result.get("direct_invite", {})
    result["lift"] = {
        "acceptance_rate_lift_pp": round(
            wu.get("acceptance_rate", 0) - di.get("acceptance_rate", 0), 1
        ),
        "reply_rate_lift_pp": round(
            wu.get("reply_rate", 0) - di.get("reply_rate", 0), 1
        ),
    }

    return result


def sync_rate_limits_from_outreaches() -> None:
    """Reconcile rate_limits.sent with actual outreach counts.

    Cloud scheduler sends invitations that don't increment the local
    rate_limits.sent counter. This syncs the counter from the outreaches
    table (source of truth) to prevent desync.
    """
    from datetime import date, datetime

    today = date.today().isoformat()
    start_of_day = int(datetime.combine(date.today(), datetime.min.time()).timestamp())

    db = get_db()
    # Count actual invitations sent today from outreaches table
    row = db.execute(
        """SELECT COUNT(*) as cnt FROM outreaches
           WHERE status = 'invited' AND invited_at >= ?""",
        (start_of_day,),
    ).fetchone()
    actual_sent = row["cnt"] if row else 0

    # Update rate_limits if actual count is higher (cloud sent some)
    current = db.execute(
        "SELECT sent FROM rate_limits WHERE date = ?", (today,)
    ).fetchone()
    if current and actual_sent > current["sent"]:
        db.execute(
            "UPDATE rate_limits SET sent = ?, updated_at = ? WHERE date = ?",
            (actual_sent, int(time.time()), today),
        )
        db.commit()
        logger.info(
            "Rate limit sync: sent %d → %d (cloud scheduler catchup)",
            current["sent"], actual_sent,
        )
    db.close()


def get_weekly_invitation_sum() -> int:
    """Sum invitations sent over the last 7 days from rate_limits table."""
    from datetime import date, timedelta
    today = date.today()
    week_ago = (today - timedelta(days=6)).isoformat()
    db = get_db()
    row = db.execute(
        "SELECT COALESCE(SUM(sent), 0) as total FROM rate_limits WHERE date >= ?",
        (week_ago,),
    ).fetchone()
    db.close()
    return row["total"] if row else 0


def get_sending_days_7d() -> int:
    """Count days with at least 1 invitation sent in the last 7 days."""
    from datetime import date, timedelta
    today = date.today()
    week_ago = (today - timedelta(days=6)).isoformat()
    db = get_db()
    row = db.execute(
        "SELECT COUNT(*) as days FROM rate_limits WHERE date >= ? AND sent > 0",
        (week_ago,),
    ).fetchone()
    db.close()
    return row["days"] if row else 0


# ──────────────────────────────────────────────
# Email Rate Limits (overflow channel)
# ──────────────────────────────────────────────


def get_email_rate_limit_today() -> dict:
    """Get or create today's email rate limit record."""
    from datetime import date
    import uuid as _uuid

    today = date.today().isoformat()
    db = get_db()
    row = db.execute(
        "SELECT * FROM email_rate_limits WHERE date = ?", (today,)
    ).fetchone()
    if row is None:
        rid = str(_uuid.uuid4())
        db.execute(
            "INSERT INTO email_rate_limits (id, date, sent, updated_at) VALUES (?, ?, 0, ?)",
            (rid, today, int(time.time())),
        )
        db.commit()
        row = db.execute(
            "SELECT * FROM email_rate_limits WHERE date = ?", (today,)
        ).fetchone()
    db.close()
    return dict(row) if row else {"sent": 0}


def increment_email_sent() -> None:
    """Increment today's email send counter."""
    # Ensure row exists first
    get_email_rate_limit_today()
    from datetime import date

    today = date.today().isoformat()
    db = get_db()
    db.execute(
        "UPDATE email_rate_limits SET sent = sent + 1, updated_at = ? WHERE date = ?",
        (int(time.time()), today),
    )
    db.commit()
    db.close()


def get_weekly_email_sum() -> int:
    """Sum emails sent over the last 7 days."""
    from datetime import date, timedelta

    today = date.today()
    week_ago = (today - timedelta(days=6)).isoformat()
    db = get_db()
    row = db.execute(
        "SELECT COALESCE(SUM(sent), 0) as total FROM email_rate_limits WHERE date >= ?",
        (week_ago,),
    ).fetchone()
    db.close()
    return row["total"] if row else 0


def get_email_eligible_pending_outreaches(campaign_id: str, limit: int = 5) -> list:
    """Get pending outreaches that have email addresses and haven't been contacted.

    Returns prospects who:
    - Have status = 'pending' (not yet contacted on ANY channel)
    - Have an email address in profile_json or linked global_contacts
    - Have NOT been contacted in ANY campaign (cross-campaign anti-double-contact)

    Ordered by fit_score DESC.
    """
    db = get_db()
    rows = db.execute(
        """SELECT o.id as outreach_id, o.contact_id, o.status,
                  c.name, c.title, c.company, c.linkedin_url, c.linkedin_id,
                  c.profile_json, c.fit_score
           FROM outreaches o
           JOIN contacts c ON o.contact_id = c.id
           WHERE o.campaign_id = ?
             AND o.status = 'pending'
             AND c.profile_json LIKE '%"email"%'
             AND NOT EXISTS (
                 SELECT 1 FROM outreaches o2
                 WHERE o2.contact_id = o.contact_id
                   AND o2.id != o.id
                   AND o2.status IN ('invited', 'connected', 'messaged', 'replied')
             )
           ORDER BY c.fit_score DESC
           LIMIT ?""",
        (campaign_id, limit),
    ).fetchall()
    db.close()
    return [dict(r) for r in rows]


def get_daily_signal_outreach_count() -> int:
    """Count signal-triggered outreaches created today (non-null signal_id)."""
    import time
    today_start = int(time.time()) - (int(time.time()) % 86400)
    db = get_db()
    row = db.execute(
        "SELECT COUNT(*) as cnt FROM outreaches WHERE signal_id IS NOT NULL AND created_at >= ?",
        (today_start,),
    ).fetchone()
    db.close()
    return row["cnt"] if row else 0


# ──────────────────────────────────────────────
# Usage Tracking (Free Tier)
# ──────────────────────────────────────────────

def get_monthly_usage() -> dict:
    """Get or create this month's usage record."""
    from datetime import date
    month = date.today().strftime("%Y-%m")
    db = get_db()
    row = db.execute("SELECT * FROM usage WHERE month = ?", (month,)).fetchone()
    if row is None:
        db.execute(
            "INSERT INTO usage (month, updated_at) VALUES (?, ?)",
            (month, int(time.time())),
        )
        db.commit()
        row = db.execute("SELECT * FROM usage WHERE month = ?", (month,)).fetchone()
    db.close()
    return dict(row)


_VALID_USAGE_FIELDS = frozenset({
    "invitations_sent",
    "messages_sent",
    "campaigns_created",
    "icps_generated",
    "engagements_sent",
})


def increment_usage(field: str) -> None:
    """Increment a usage counter (invitations_sent, messages_sent, etc.)."""
    if field not in _VALID_USAGE_FIELDS:
        raise ValueError(f"Invalid usage field: {field}. Must be one of {_VALID_USAGE_FIELDS}")
    from datetime import date
    month = date.today().strftime("%Y-%m")
    db = get_db()
    # Ensure row exists
    get_monthly_usage()
    db.execute(
        f"UPDATE usage SET {field} = {field} + 1, updated_at = ? WHERE month = ?",
        (int(time.time()), month),
    )
    db.commit()
    db.close()


def set_monthly_usage(usage: dict) -> None:
    """Overwrite this month's usage with authoritative backend data."""
    from datetime import date
    month = date.today().strftime("%Y-%m")
    # Ensure row exists
    get_monthly_usage()
    db = get_db()
    updates = []
    values: list[Any] = []
    for field in ("invitations_sent", "messages_sent", "engagements_sent"):
        if field in usage:
            updates.append(f"{field} = ?")
            values.append(usage[field])
    if updates:
        values.extend([int(time.time()), month])
        db.execute(
            f"UPDATE usage SET {', '.join(updates)}, updated_at = ? WHERE month = ?",
            tuple(values),
        )
        db.commit()
    db.close()


# ──────────────────────────────────────────────
# Campaign Stats (for show_status)
# ──────────────────────────────────────────────

def get_campaign_stats(campaign_id: str) -> dict:
    """Calculate aggregate stats for a campaign.

    Rates:
    - acceptance_rate: connected / mature_invited (invitations > 7 days old, excl opted_out)
    - raw_acceptance_rate: connected / all_invited (includes pending, for transparency)
    - reply_rate: replied / connected
    """
    import time as _time
    db = get_db()

    seven_days_ago = int(_time.time()) - (7 * 86400)
    row = db.execute(
        """SELECT
               COUNT(*) as total,
               SUM(CASE WHEN status NOT IN ('pending', 'skipped') THEN 1 ELSE 0 END) as invited,
               SUM(CASE WHEN status NOT IN ('pending', 'skipped', 'opted_out') THEN 1 ELSE 0 END) as invited_excl_optout,
               SUM(CASE WHEN status IN ('connected', 'messaged', 'replied', 'hot_lead', 'closed_happy', 'closed_unhappy', 'reverse_pitch', 'opted_out') THEN 1 ELSE 0 END) as connected,
               SUM(CASE WHEN status IN ('replied', 'hot_lead', 'closed_happy', 'closed_unhappy', 'reverse_pitch', 'opted_out') THEN 1 ELSE 0 END) as replied,
               SUM(CASE WHEN status = 'hot_lead' THEN 1 ELSE 0 END) as hot_leads,
               SUM(CASE WHEN status = 'invited' THEN 1 ELSE 0 END) as pending_invitations,
               SUM(CASE WHEN status = 'skipped' THEN 1 ELSE 0 END) as skipped,
               SUM(CASE WHEN status = 'closed_happy' THEN 1 ELSE 0 END) as closed_happy,
               SUM(CASE WHEN status = 'closed_unhappy' THEN 1 ELSE 0 END) as closed_unhappy,
               SUM(CASE WHEN status = 'opted_out' THEN 1 ELSE 0 END) as opted_out,
               SUM(CASE WHEN status NOT IN ('pending', 'skipped')
                    AND COALESCE(invited_at, updated_at) < ? THEN 1 ELSE 0 END) as mature_invited,
               SUM(CASE WHEN status = 'pending' AND COALESCE(invite_attempts, 0) > 0 THEN 1 ELSE 0 END) as invite_failed
           FROM outreaches
           WHERE campaign_id = ?""",
        (seven_days_ago, campaign_id),
    ).fetchone()

    db.close()

    r = dict(row) if row else {}
    total = r.get("total", 0) or 0
    invited = r.get("invited", 0) or 0
    invited_excl_optout = r.get("invited_excl_optout", 0) or 0
    connected = r.get("connected", 0) or 0
    replied = r.get("replied", 0) or 0
    mature_invited = r.get("mature_invited", 0) or 0

    # Primary rate: only count invitations that have had time to respond (7d+).
    # Falls back to all invitations if no mature invitations yet.
    # Cap at 1.0 — connected can exceed invited when inbound connections are included.
    if mature_invited > 0:
        acceptance_rate = min(1.0, connected / mature_invited)
    elif invited_excl_optout > 0:
        acceptance_rate = min(1.0, connected / invited_excl_optout)
    else:
        acceptance_rate = 0.0

    raw_acceptance_rate = min(1.0, connected / invited) if invited > 0 else 0.0
    reply_rate = replied / connected if connected > 0 else 0.0

    return {
        "total_prospects": total,
        "invited": invited,
        "connected": connected,
        "replied": replied,
        "hot_leads": r.get("hot_leads", 0) or 0,
        "pending_invitations": r.get("pending_invitations", 0) or 0,
        "skipped": r.get("skipped", 0) or 0,
        "closed_happy": r.get("closed_happy", 0) or 0,
        "closed_unhappy": r.get("closed_unhappy", 0) or 0,
        "opted_out": r.get("opted_out", 0) or 0,
        "invite_failed": r.get("invite_failed", 0) or 0,
        "acceptance_rate": acceptance_rate,
        "raw_acceptance_rate": raw_acceptance_rate,
        "reply_rate": reply_rate,
    }


def get_campaign_outcomes(campaign_id: str) -> dict:
    """Get outcome breakdown for a campaign.

    Returns dict with closed_happy, closed_unhappy, opted_out counts,
    total_closed, conversion_rate, and individual outcome details.
    """
    db = get_db()

    closed_happy = db.execute(
        "SELECT COUNT(*) as c FROM outreaches WHERE campaign_id = ? AND status = 'closed_happy'",
        (campaign_id,),
    ).fetchone()["c"]

    closed_unhappy = db.execute(
        "SELECT COUNT(*) as c FROM outreaches WHERE campaign_id = ? AND status = 'closed_unhappy'",
        (campaign_id,),
    ).fetchone()["c"]

    opted_out = db.execute(
        "SELECT COUNT(*) as c FROM outreaches WHERE campaign_id = ? AND status = 'opted_out'",
        (campaign_id,),
    ).fetchone()["c"]

    # Individual outcome details with contact info
    rows = db.execute(
        """SELECT o.id as outreach_id, o.status, o.outcome_json, o.updated_at,
                  c.name, c.title, c.company, c.fit_score
           FROM outreaches o
           JOIN contacts c ON o.contact_id = c.id
           WHERE o.campaign_id = ?
             AND o.status IN ('closed_happy', 'closed_unhappy', 'opted_out')
           ORDER BY o.updated_at DESC""",
        (campaign_id,),
    ).fetchall()
    db.close()

    outcomes = []
    for row in rows:
        r = dict(row)
        outcome_data = {}
        if r.get("outcome_json"):
            try:
                outcome_data = json.loads(r["outcome_json"])
            except (json.JSONDecodeError, TypeError):
                pass
        outcomes.append({
            "outreach_id": r["outreach_id"],
            "status": r["status"],
            "name": r.get("name", "Unknown"),
            "title": r.get("title", ""),
            "company": r.get("company", ""),
            "fit_score": r.get("fit_score", 0),
            "reason": outcome_data.get("reason", ""),
            "meeting_link": outcome_data.get("meeting_link") or outcome_data.get("booking_link", ""),
            "closed_at": outcome_data.get("closed_at", r.get("updated_at", 0)),
        })

    total_closed = closed_happy + closed_unhappy
    conversion_rate = closed_happy / total_closed if total_closed > 0 else 0.0

    return {
        "closed_happy": closed_happy,
        "closed_unhappy": closed_unhappy,
        "opted_out": opted_out,
        "total_closed": total_closed,
        "conversion_rate": conversion_rate,
        "outcomes": outcomes,
    }


def get_stale_outreaches(campaign_id: str, stale_days: int = 14) -> list[dict]:
    """Find outreaches with no activity for N days.

    Returns outreaches in active states (connected, messaged, hot_lead)
    whose updated_at is older than stale_days ago, joined with contact info.
    """
    import time as _time
    cutoff = int(_time.time()) - (stale_days * 86400)
    now = int(_time.time())

    db = get_db()
    rows = db.execute(
        """SELECT o.id as outreach_id, o.status, o.updated_at,
                  c.name, c.title, c.company, c.fit_score, c.source
           FROM outreaches o
           JOIN contacts c ON o.contact_id = c.id
           WHERE o.campaign_id = ?
             AND o.status IN ('connected', 'messaged', 'hot_lead')
             AND o.updated_at < ?
           ORDER BY o.updated_at ASC""",
        (campaign_id, cutoff),
    ).fetchall()
    db.close()

    results = []
    for row in rows:
        r = dict(row)
        days_stale = (now - (r.get("updated_at") or 0)) // 86400
        results.append({
            "outreach_id": r["outreach_id"],
            "status": r["status"],
            "name": r.get("name", "Unknown"),
            "title": r.get("title", ""),
            "company": r.get("company", ""),
            "fit_score": r.get("fit_score", 0),
            "days_stale": days_stale,
            "updated_at": r.get("updated_at", 0),
        })

    return results


def get_campaign_velocity(campaign_id: str) -> dict:
    """Calculate time-based velocity metrics for a campaign.

    Returns avg/min/max time-to-accept, time-to-reply, and per-deal timelines.
    All time values are in seconds. NULL columns are excluded from aggregates.
    """
    db = get_db()

    # Avg/min/max time-to-accept (invited_at → accepted_at)
    accept_row = db.execute(
        """SELECT AVG(accepted_at - invited_at) as avg_tta,
                  MIN(accepted_at - invited_at) as min_tta,
                  MAX(accepted_at - invited_at) as max_tta,
                  COUNT(*) as cnt
           FROM outreaches
           WHERE campaign_id = ?
             AND invited_at IS NOT NULL
             AND accepted_at IS NOT NULL
             AND status IN ('connected', 'messaged', 'replied', 'hot_lead', 'closed_happy', 'closed_unhappy', 'reverse_pitch', 'opted_out')""",
        (campaign_id,),
    ).fetchone()

    # Avg time-to-reply (accepted_at → first_reply_at)
    reply_row = db.execute(
        """SELECT AVG(first_reply_at - accepted_at) as avg_ttr,
                  MIN(first_reply_at - accepted_at) as min_ttr,
                  MAX(first_reply_at - accepted_at) as max_ttr,
                  COUNT(*) as cnt
           FROM outreaches
           WHERE campaign_id = ?
             AND accepted_at IS NOT NULL
             AND first_reply_at IS NOT NULL
             AND status IN ('replied', 'hot_lead', 'closed_happy', 'closed_unhappy', 'reverse_pitch', 'opted_out')""",
        (campaign_id,),
    ).fetchone()

    # Avg invite-to-reply (full funnel)
    full_row = db.execute(
        """SELECT AVG(first_reply_at - invited_at) as avg_full,
                  COUNT(*) as cnt
           FROM outreaches
           WHERE campaign_id = ?
             AND invited_at IS NOT NULL
             AND first_reply_at IS NOT NULL
             AND status IN ('replied', 'hot_lead', 'closed_happy', 'closed_unhappy', 'reverse_pitch', 'opted_out')""",
        (campaign_id,),
    ).fetchone()

    # Per-deal timelines for hot leads and closed deals
    deal_rows = db.execute(
        """SELECT o.invited_at, o.accepted_at, o.first_reply_at,
                  o.status, c.name, c.title, c.company
           FROM outreaches o
           JOIN contacts c ON o.contact_id = c.id
           WHERE o.campaign_id = ?
             AND o.status IN ('closed_happy', 'closed_unhappy', 'hot_lead')
             AND o.invited_at IS NOT NULL
           ORDER BY o.updated_at DESC
           LIMIT 10""",
        (campaign_id,),
    ).fetchall()
    db.close()

    ar = dict(accept_row) if accept_row else {}
    rr = dict(reply_row) if reply_row else {}
    fr = dict(full_row) if full_row else {}

    timelines = []
    for row in deal_rows:
        d = dict(row)
        inv = d.get("invited_at")
        acc = d.get("accepted_at")
        rep = d.get("first_reply_at")
        timelines.append({
            "name": d.get("name", "Unknown"),
            "title": d.get("title", ""),
            "company": d.get("company", ""),
            "status": d.get("status", ""),
            "time_to_accept": (acc - inv) if (inv and acc) else None,
            "time_to_reply": (rep - acc) if (acc and rep) else None,
        })

    return {
        "avg_time_to_accept": ar.get("avg_tta"),
        "avg_time_to_reply": rr.get("avg_ttr"),
        "avg_time_invite_to_reply": fr.get("avg_full"),
        "count_accepted": ar.get("cnt", 0),
        "count_replied": rr.get("cnt", 0),
        "fastest_accept": ar.get("min_tta"),
        "slowest_accept": ar.get("max_tta"),
        "fastest_reply": rr.get("min_ttr"),
        "slowest_reply": rr.get("max_ttr"),
        "per_deal_timelines": timelines,
    }


# ──────────────────────────────────────────────
# ICPs (Ideal Customer Profiles)
# ──────────────────────────────────────────────

def save_icp(
    name: str,
    icp_json: str,
    target_desc: str = "",
    source_url: str = "",
    confidence: float = 0.5,
) -> str:
    """Create a new ICP and return its ID."""
    icp_id = str(uuid.uuid4())
    now = int(time.time())
    db = get_db()
    db.execute(
        """INSERT INTO icps (id, name, icp_json, target_desc, source_url, status, confidence, created_at, updated_at)
           VALUES (?, ?, ?, ?, ?, 'active', ?, ?, ?)""",
        (icp_id, name, icp_json, target_desc, source_url, confidence, now, now),
    )
    db.commit()
    db.close()
    return icp_id


def get_icp(icp_id: str) -> Optional[dict]:
    """Load an ICP by ID."""
    db = get_db()
    row = db.execute("SELECT * FROM icps WHERE id = ?", (icp_id,)).fetchone()
    db.close()
    return dict(row) if row else None


def list_icps(status: Optional[str] = None) -> list[dict]:
    """List all ICPs, optionally filtered by status."""
    db = get_db()
    if status:
        rows = db.execute(
            "SELECT * FROM icps WHERE status = ? ORDER BY created_at DESC",
            (status,),
        ).fetchall()
    else:
        rows = db.execute(
            "SELECT * FROM icps ORDER BY created_at DESC",
        ).fetchall()
    db.close()
    return [dict(r) for r in rows]


_VALID_ICP_COLS = frozenset({
    "name", "icp_json", "target_desc", "source_url", "status",
    "confidence", "updated_at",
})


def update_icp(icp_id: str, **kwargs: Any) -> None:
    """Update an ICP's fields."""
    db = get_db()
    kwargs["updated_at"] = int(time.time())
    bad_keys = set(kwargs) - _VALID_ICP_COLS
    if bad_keys:
        raise ValueError(f"Invalid ICP columns: {bad_keys}")
    set_clause = ", ".join(f"{k} = ?" for k in kwargs)
    values = list(kwargs.values()) + [icp_id]
    db.execute(f"UPDATE icps SET {set_clause} WHERE id = ?", values)
    db.commit()
    db.close()


def delete_icp(icp_id: str) -> None:
    """Delete an ICP and its sources/chunks."""
    db = get_db()
    # Delete chunks for this ICP's sources
    db.execute(
        """DELETE FROM icp_chunks WHERE source_id IN
           (SELECT id FROM icp_sources WHERE icp_id = ?)""",
        (icp_id,),
    )
    db.execute("DELETE FROM icp_sources WHERE icp_id = ?", (icp_id,))
    db.execute("DELETE FROM icps WHERE id = ?", (icp_id,))
    db.commit()
    db.close()


# ──────────────────────────────────────────────
# Engagements
# ──────────────────────────────────────────────

def reserve_engagement(
    outreach_id: str,
    action_type: str,
    post_id: str,
    account_id: str,
    campaign_id: str = "",
) -> str | None:
    """Reserve an engagement slot before calling the LinkedIn API.

    Inserts a row with status='pending' to claim the (post_id, account_id) slot
    via the UNIQUE constraint. Returns engagement ID on success, None if already
    reserved/sent (duplicate).
    """
    if not post_id or not account_id:
        return None
    engagement_id = str(uuid.uuid4())
    db = get_db()
    try:
        db.execute(
            """INSERT INTO engagements
               (id, outreach_id, action_type, post_id, status,
                campaign_id, account_id, created_at)
               VALUES (?, ?, ?, ?, 'pending', ?, ?, ?)""",
            (engagement_id, outreach_id, action_type, post_id,
             campaign_id or None, account_id, int(time.time())),
        )
        db.commit()
    except sqlite3.IntegrityError:
        db.close()
        return None
    db.close()
    return engagement_id


def finalize_engagement(
    engagement_id: str,
    post_text: str = "",
    text: str = "",
    reaction_type: str = "",
    reasoning: str = "",
) -> None:
    """Update a reserved engagement to 'sent' with full details after LinkedIn confirms."""
    db = get_db()
    db.execute(
        """UPDATE engagements
           SET status = 'sent', post_text = ?, text = ?,
               reaction_type = ?, reasoning = ?
           WHERE id = ?""",
        (post_text, text, reaction_type, reasoning, engagement_id),
    )
    db.commit()
    db.close()


def delete_engagement(engagement_id: str) -> None:
    """Remove a reserved engagement that failed to send."""
    db = get_db()
    db.execute("DELETE FROM engagements WHERE id = ? AND status = 'pending'", (engagement_id,))
    db.commit()
    db.close()


def save_engagement(
    outreach_id: str,
    action_type: str,
    post_id: str,
    post_text: str = "",
    text: str = "",
    reaction_type: str = "",
    status: str = "sent",
    reasoning: str = "",
    campaign_id: str = "",
    account_id: str = "",
) -> str | None:
    """Save an engagement action (comment or reaction). Returns engagement ID.

    Returns None if a UNIQUE constraint violation occurs (duplicate post+account),
    which serves as the DB-level safety net against race conditions.
    """
    engagement_id = str(uuid.uuid4())
    db = get_db()
    try:
        db.execute(
            """INSERT INTO engagements
               (id, outreach_id, action_type, post_id, post_text, text,
                reaction_type, status, reasoning, campaign_id, account_id, created_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (engagement_id, outreach_id, action_type, post_id, post_text,
             text, reaction_type, status, reasoning, campaign_id or None,
             account_id or None, int(time.time())),
        )
        db.commit()
    except sqlite3.IntegrityError:
        # UNIQUE constraint on (post_id, account_id) — duplicate engagement
        db.close()
        return None
    db.close()
    return engagement_id


def get_unverified_engagements(since_ts: int, limit: int = 20) -> list[dict]:
    """Fetch engagements with verified_at IS NULL from the last N seconds.

    Joins through outreach → contact to include provider_id for follow verification.
    """
    db = get_db()
    rows = db.execute(
        """SELECT e.id, e.action_type, e.post_id, e.text, e.account_id,
                  e.outreach_id, e.created_at,
                  c.linkedin_id AS contact_linkedin_id,
                  c.profile_json AS contact_profile_json
           FROM engagements e
           LEFT JOIN outreaches o ON e.outreach_id = o.id
           LEFT JOIN contacts c ON o.contact_id = c.id
           WHERE e.created_at >= ?
             AND e.verified_at IS NULL
             AND e.status = 'sent'
           ORDER BY e.created_at DESC
           LIMIT ?""",
        (since_ts, limit),
    ).fetchall()
    db.close()
    return [dict(r) for r in rows]


def update_engagement_verification(
    engagement_id: str,
    verified_status: str,
    external_id: str = "",
) -> None:
    """Update verification status and external_id on an engagement."""
    db = get_db()
    now = int(time.time())
    if external_id:
        db.execute(
            "UPDATE engagements SET verified_at = ?, verified_status = ?, external_id = ? WHERE id = ?",
            (now, verified_status, external_id, engagement_id),
        )
    else:
        db.execute(
            "UPDATE engagements SET verified_at = ?, verified_status = ? WHERE id = ?",
            (now, verified_status, engagement_id),
        )
    db.commit()
    db.close()


def get_engagement_verification_stats(campaign_id: str = "") -> dict:
    """Get engagement verification stats, optionally filtered by campaign."""
    db = get_db()
    where = "WHERE campaign_id = ?" if campaign_id else ""
    params: tuple = (campaign_id,) if campaign_id else ()
    rows = db.execute(
        f"""SELECT
            COALESCE(verified_status, 'pending') as status,
            COUNT(*) as cnt
        FROM engagements
        {where}
        GROUP BY COALESCE(verified_status, 'pending')""",
        params,
    ).fetchall()
    db.close()
    result = {"verified": 0, "unverified": 0, "trust_api": 0, "pending": 0}
    for row in rows:
        key = row["status"] if row["status"] in result else "pending"
        result[key] = row["cnt"]
    return result


def get_engagement_stats(campaign_id: str = "") -> dict:
    """Get engagement stats, optionally filtered by campaign.

    Includes engagements linked via outreach→campaign OR directly via campaign_id.
    Excludes unverified engagements (failed to land on LinkedIn).
    """
    db = get_db()
    unverified_filter = "AND (e.verified_status IS NULL OR e.verified_status != 'unverified')"
    if campaign_id:
        comments = db.execute(
            f"""SELECT COUNT(*) as c FROM engagements e
               LEFT JOIN outreaches o ON e.outreach_id = o.id
               WHERE (o.campaign_id = ? OR e.campaign_id = ?)
               AND e.action_type = 'comment'
               AND e.status = 'sent' {unverified_filter}""",
            (campaign_id, campaign_id),
        ).fetchone()["c"]
        reactions = db.execute(
            f"""SELECT COUNT(*) as c FROM engagements e
               LEFT JOIN outreaches o ON e.outreach_id = o.id
               WHERE (o.campaign_id = ? OR e.campaign_id = ?)
               AND e.action_type = 'react'
               AND e.status = 'sent' {unverified_filter}""",
            (campaign_id, campaign_id),
        ).fetchone()["c"]
    else:
        comments = db.execute(
            "SELECT COUNT(*) as c FROM engagements e WHERE action_type = 'comment' AND status = 'sent' "
            "AND (e.verified_status IS NULL OR e.verified_status != 'unverified')"
        ).fetchone()["c"]
        reactions = db.execute(
            "SELECT COUNT(*) as c FROM engagements e WHERE action_type = 'react' AND status = 'sent' "
            "AND (e.verified_status IS NULL OR e.verified_status != 'unverified')"
        ).fetchone()["c"]
    db.close()
    return {"comments": comments, "reactions": reactions, "total": comments + reactions}


def get_recent_engagements(campaign_id: str = "", limit: int = 10) -> list[dict]:
    """Get recent engagement records with prospect details.

    Returns engagement details including prospect name, post text snippet,
    comment text, action type, and post ID for manual verification.
    """
    db = get_db()
    if campaign_id:
        rows = db.execute(
            """SELECT e.action_type, e.post_id, e.post_text, e.text as comment_text,
                      e.reaction_type, e.status, e.created_at,
                      c.name as prospect_name, c.title as prospect_title
               FROM engagements e
               LEFT JOIN outreaches o ON e.outreach_id = o.id
               LEFT JOIN contacts c ON o.contact_id = c.id
               WHERE (o.campaign_id = ? OR e.campaign_id = ?)
               AND e.action_type IN ('comment', 'react')
               ORDER BY e.created_at DESC
               LIMIT ?""",
            (campaign_id, campaign_id, limit),
        ).fetchall()
    else:
        rows = db.execute(
            """SELECT e.action_type, e.post_id, e.post_text, e.text as comment_text,
                      e.reaction_type, e.status, e.created_at,
                      c.name as prospect_name, c.title as prospect_title
               FROM engagements e
               LEFT JOIN outreaches o ON e.outreach_id = o.id
               LEFT JOIN contacts c ON o.contact_id = c.id
               WHERE e.action_type IN ('comment', 'react')
               ORDER BY e.created_at DESC
               LIMIT ?""",
            (limit,),
        ).fetchall()
    result = [dict(r) for r in rows]
    db.close()
    return result


def get_engagement_candidates(
    campaign_id: str,
    max_per_outreach: int = 3,
) -> list[dict]:
    """Find outreaches ready for post engagement.

    Returns outreaches that haven't exceeded the engagement limit.
    Includes pending/invited/connected/messaged/replied — engaging with
    posts BEFORE connection acceptance is a warm-up tactic.

    Skips outreaches with time-limited cooldowns (next_action JSON with
    ``skip_engagement_until`` timestamp in the future). Expired cooldowns
    are automatically eligible again.
    """
    now = int(time.time())
    db = get_db()
    rows = db.execute(
        """SELECT o.id as outreach_id, o.campaign_id, o.contact_id, o.status,
                  o.followup_count, o.updated_at as outreach_updated_at,
                  o.next_action,
                  c.name, c.title, c.company, c.linkedin_url, c.linkedin_id,
                  c.profile_json, c.fit_score,
                  (SELECT COUNT(*) FROM engagements e WHERE e.outreach_id = o.id) as engagement_count
           FROM outreaches o
           JOIN contacts c ON o.contact_id = c.id
           WHERE o.campaign_id = ?
             AND o.status IN ('pending', 'invited', 'connected', 'messaged', 'replied')
             AND (SELECT COUNT(*) FROM engagements e WHERE e.outreach_id = o.id) < ?
             AND COALESCE(o.next_action, '') != 'skip_engagement'
             AND (
               o.next_action IS NULL
               OR o.next_action = ''
               OR json_valid(o.next_action) = 0
               OR json_extract(o.next_action, '$.skip_engagement_until') IS NULL
               OR json_extract(o.next_action, '$.skip_engagement_until') < ?
             )
           ORDER BY o.updated_at ASC""",
        (campaign_id, max_per_outreach, now),
    ).fetchall()
    db.close()
    return [dict(r) for r in rows]


def get_follow_candidates(campaign_id: str) -> list[dict]:
    """Find pending outreaches that haven't been followed yet.

    Returns outreaches in 'pending' status that have no 'follow'
    engagement yet. Used by the scheduler to auto-follow prospects
    before engaging with their posts.
    Respects both permanent skip_engagement and time-limited JSON cooldowns.
    """
    now = int(time.time())
    db = get_db()
    rows = db.execute(
        """SELECT o.id as outreach_id, o.campaign_id, o.contact_id, o.status,
                  o.followup_count, o.updated_at as outreach_updated_at,
                  c.name, c.title, c.company, c.linkedin_url, c.linkedin_id,
                  c.profile_json, c.fit_score
           FROM outreaches o
           JOIN contacts c ON o.contact_id = c.id
           WHERE o.campaign_id = ?
             AND o.status = 'pending'
             AND COALESCE(o.next_action, '') != 'skip_engagement'
             AND (
               o.next_action IS NULL
               OR o.next_action = ''
               OR json_valid(o.next_action) = 0
               OR json_extract(o.next_action, '$.skip_engagement_until') IS NULL
               OR json_extract(o.next_action, '$.skip_engagement_until') < ?
             )
             AND NOT EXISTS (
                 SELECT 1 FROM engagements e
                 WHERE e.outreach_id = o.id AND e.action_type = 'follow'
             )
           ORDER BY c.fit_score DESC""",
        (campaign_id, now),
    ).fetchall()
    db.close()
    return [dict(r) for r in rows]


def get_profile_view_candidates(campaign_id: str) -> list[dict]:
    """Find pending outreaches that haven't had a profile view yet.

    Returns outreaches in 'pending' status that have no 'profile_view'
    engagement yet. Used by the scheduler to auto-view prospect profiles
    as the lightest warm-up signal before following.
    Respects both permanent skip_engagement and time-limited JSON cooldowns.
    """
    now = int(time.time())
    db = get_db()
    rows = db.execute(
        """SELECT o.id as outreach_id, o.campaign_id, o.contact_id, o.status,
                  o.followup_count, o.updated_at as outreach_updated_at,
                  c.name, c.title, c.company, c.linkedin_url, c.linkedin_id,
                  c.profile_json, c.fit_score
           FROM outreaches o
           JOIN contacts c ON o.contact_id = c.id
           WHERE o.campaign_id = ?
             AND o.status = 'pending'
             AND COALESCE(o.next_action, '') != 'skip_engagement'
             AND (
               o.next_action IS NULL
               OR o.next_action = ''
               OR json_valid(o.next_action) = 0
               OR json_extract(o.next_action, '$.skip_engagement_until') IS NULL
               OR json_extract(o.next_action, '$.skip_engagement_until') < ?
             )
             AND NOT EXISTS (
                 SELECT 1 FROM engagements e
                 WHERE e.outreach_id = o.id AND e.action_type = 'profile_view'
             )
           ORDER BY c.fit_score DESC""",
        (campaign_id, now),
    ).fetchall()
    db.close()
    return [dict(r) for r in rows]


def get_daily_engagement_count() -> int:
    """Count engagements sent today."""
    import datetime
    today = datetime.date.today()
    today_start = int(time.mktime(today.timetuple()))
    db = get_db()
    row = db.execute(
        "SELECT COUNT(*) as c FROM engagements WHERE created_at >= ?",
        (today_start,),
    ).fetchone()
    db.close()
    return row["c"] if row else 0


def get_daily_engagement_count_by_type(action_type: str) -> int:
    """Count engagements of a specific type sent today.

    Enables independent daily limits per action type (comment, react,
    profile_view, follow, endorse).
    """
    import datetime
    today = datetime.date.today()
    today_start = int(time.mktime(today.timetuple()))
    db = get_db()
    row = db.execute(
        "SELECT COUNT(*) as c FROM engagements WHERE action_type = ? AND created_at >= ?",
        (action_type, today_start),
    ).fetchone()
    db.close()
    return row["c"] if row else 0


def get_daily_engagement_counts_all() -> dict:
    """Count verified engagements by action_type for today.

    Returns {action_type: count} dict. Only counts engagements with
    verified_status IN ('verified', 'trust_api') — not NULL (pending)
    or 'unverified' (failed).
    """
    import datetime
    today = datetime.date.today()
    today_start = int(time.mktime(today.timetuple()))
    db = get_db()
    rows = db.execute(
        "SELECT action_type, COUNT(*) as c FROM engagements "
        "WHERE created_at >= ? "
        "AND verified_status IN ('verified', 'trust_api') "
        "GROUP BY action_type",
        (today_start,),
    ).fetchall()
    db.close()
    return {row["action_type"]: row["c"] for row in rows}


def get_daily_engagement_counts_pending() -> dict:
    """Count pending-verification engagements by action_type for today.

    Returns {action_type: count} dict for engagements with NULL verified_status.
    """
    import datetime
    today = datetime.date.today()
    today_start = int(time.mktime(today.timetuple()))
    db = get_db()
    rows = db.execute(
        "SELECT action_type, COUNT(*) as c FROM engagements "
        "WHERE created_at >= ? "
        "AND verified_status IS NULL AND status = 'sent' "
        "GROUP BY action_type",
        (today_start,),
    ).fetchall()
    db.close()
    return {row["action_type"]: row["c"] for row in rows}


def get_daily_brand_post_count() -> int:
    """Count completed brand_post scheduler jobs today."""
    import datetime

    today = datetime.date.today()
    today_start = int(time.mktime(today.timetuple()))
    db = get_db()
    row = db.execute(
        "SELECT COUNT(*) as c FROM scheduler_jobs "
        "WHERE job_type = 'brand_post' AND status = 'completed' AND scheduled_at >= ?",
        (today_start,),
    ).fetchone()
    db.close()
    return row["c"] if row else 0


def get_daily_brand_engage_count() -> int:
    """Count completed brand_engage scheduler jobs today."""
    import datetime

    today = datetime.date.today()
    today_start = int(time.mktime(today.timetuple()))
    db = get_db()
    row = db.execute(
        "SELECT COUNT(*) as c FROM scheduler_jobs "
        "WHERE job_type = 'brand_engage' AND status = 'completed' AND scheduled_at >= ?",
        (today_start,),
    ).fetchone()
    db.close()
    return row["c"] if row else 0


def get_engagement_count_for_outreach(outreach_id: str) -> int:
    """Count engagements for a specific outreach."""
    db = get_db()
    row = db.execute(
        "SELECT COUNT(*) as c FROM engagements WHERE outreach_id = ?",
        (outreach_id,),
    ).fetchone()
    db.close()
    return row["c"] if row else 0


def get_engaged_post_ids(outreach_id: str) -> set[str]:
    """Return post_ids already engaged for this outreach."""
    db = get_db()
    rows = db.execute(
        "SELECT DISTINCT post_id FROM engagements WHERE outreach_id = ?",
        (outreach_id,),
    ).fetchall()
    db.close()
    return {row["post_id"] for row in rows if row["post_id"]}


def get_account_engaged_post_ids(account_id: str) -> set[str]:
    """Return all post_ids already engaged by this account across ALL outreaches.

    This is the global dedup check — prevents the same LinkedIn account from
    commenting on the same post twice, regardless of which outreach triggers it.
    """
    if not account_id:
        return set()
    db = get_db()
    rows = db.execute(
        """SELECT DISTINCT post_id FROM engagements
           WHERE account_id = ? AND post_id IS NOT NULL AND post_id != ''""",
        (account_id,),
    ).fetchall()
    db.close()
    return {row["post_id"] for row in rows}


def is_post_already_engaged(post_id: str, account_id: str = "") -> bool:
    """Check if this post has already been engaged by this account (any outreach).

    Lightweight single-post check used as a pre-send race condition guard.
    """
    if not post_id or not account_id:
        return False
    db = get_db()
    row = db.execute(
        "SELECT 1 FROM engagements WHERE post_id = ? AND account_id = ? LIMIT 1",
        (post_id, account_id),
    ).fetchone()
    db.close()
    return row is not None


# ──────────────────────────────────────────────
# Engagement Anomaly Detection
# ──────────────────────────────────────────────


def get_duplicate_post_engagements(hours: int = 24) -> list[dict]:
    """Find post_ids with multiple engagements by the same account in the last N hours.

    Returns list of dicts with post_id, count, outreach_ids, action_types.
    """
    db = get_db()
    since = int(time.time()) - (hours * 3600)
    rows = db.execute(
        """SELECT post_id, account_id,
                  COUNT(*) as cnt,
                  GROUP_CONCAT(DISTINCT outreach_id) as outreach_ids,
                  GROUP_CONCAT(DISTINCT action_type) as action_types,
                  MIN(created_at) as first_at,
                  MAX(created_at) as last_at
           FROM engagements
           WHERE created_at >= ?
             AND post_id IS NOT NULL AND post_id != ''
             AND account_id IS NOT NULL AND account_id != ''
           GROUP BY post_id, account_id
           HAVING COUNT(*) > 1
           ORDER BY cnt DESC""",
        (since,),
    ).fetchall()
    db.close()
    return [dict(r) for r in rows]


def get_engagement_burst_count(minutes: int = 30) -> int:
    """Count engagements in the last N minutes (burst detection)."""
    db = get_db()
    since = int(time.time()) - (minutes * 60)
    row = db.execute(
        "SELECT COUNT(*) as c FROM engagements WHERE created_at >= ?",
        (since,),
    ).fetchone()
    db.close()
    return row["c"] if row else 0


def get_engagement_burst_count_by_type(minutes: int = 30, action_type: str = "react") -> int:
    """Count engagements of a specific action_type in the last N minutes."""
    db = get_db()
    since = int(time.time()) - (minutes * 60)
    row = db.execute(
        "SELECT COUNT(*) as c FROM engagements WHERE created_at >= ? AND action_type = ?",
        (since, action_type),
    ).fetchone()
    db.close()
    return row["c"] if row else 0


def get_same_company_engagements(hours: int = 24) -> list[dict]:
    """Find cases where many comments were made on posts related to the same company.

    Groups by prospect company to detect same-company-post clustering.
    """
    db = get_db()
    since = int(time.time()) - (hours * 3600)
    rows = db.execute(
        """SELECT c.company, c.name as prospect_name,
                  COUNT(DISTINCT e.post_id) as post_count,
                  COUNT(*) as engagement_count,
                  GROUP_CONCAT(DISTINCT e.post_id) as post_ids
           FROM engagements e
           JOIN outreaches o ON e.outreach_id = o.id
           JOIN contacts c ON o.contact_id = c.id
           WHERE e.created_at >= ?
             AND e.action_type = 'comment'
             AND c.company IS NOT NULL AND c.company != ''
           GROUP BY c.company
           HAVING COUNT(*) > 2
           ORDER BY engagement_count DESC""",
        (since,),
    ).fetchall()
    db.close()
    return [dict(r) for r in rows]


def get_failed_engagement_count(hours: int = 24) -> int:
    """Count failed engagements in the last N hours."""
    db = get_db()
    since = int(time.time()) - (hours * 3600)
    row = db.execute(
        "SELECT COUNT(*) as c FROM engagements WHERE status = 'failed' AND created_at >= ?",
        (since,),
    ).fetchone()
    db.close()
    return row["c"] if row else 0


def get_last_activity_timestamp(outreach_id: str) -> int:
    """Get the most recent activity timestamp for an outreach.

    Checks messages, engagements, and outreach updated_at.
    Returns Unix timestamp (0 if no activity).
    """
    db = get_db()
    # Latest message
    msg = db.execute(
        "SELECT MAX(timestamp) as t FROM messages WHERE outreach_id = ?",
        (outreach_id,),
    ).fetchone()
    # Latest engagement
    eng = db.execute(
        "SELECT MAX(created_at) as t FROM engagements WHERE outreach_id = ?",
        (outreach_id,),
    ).fetchone()
    # Outreach updated_at
    out = db.execute(
        "SELECT updated_at FROM outreaches WHERE id = ?",
        (outreach_id,),
    ).fetchone()
    db.close()

    timestamps = [
        msg["t"] if msg and msg["t"] else 0,
        eng["t"] if eng and eng["t"] else 0,
        out["updated_at"] if out else 0,
    ]
    return max(timestamps)


def get_error_outreaches(campaign_id: str = "") -> list[dict]:
    """Find outreaches with status 'error', optionally filtered by campaign."""
    db = get_db()
    if campaign_id:
        rows = db.execute(
            """SELECT o.id as outreach_id, o.campaign_id, o.contact_id,
                      o.status, o.followup_count, o.updated_at,
                      o.invite_attempts,
                      c.name, c.title, c.company, c.linkedin_url, c.fit_score
               FROM outreaches o
               JOIN contacts c ON o.contact_id = c.id
               WHERE o.campaign_id = ? AND o.status = 'error'
               ORDER BY o.updated_at DESC""",
            (campaign_id,),
        ).fetchall()
    else:
        rows = db.execute(
            """SELECT o.id as outreach_id, o.campaign_id, o.contact_id,
                      o.status, o.followup_count, o.updated_at,
                      o.invite_attempts,
                      c.name, c.title, c.company, c.linkedin_url, c.fit_score
               FROM outreaches o
               JOIN contacts c ON o.contact_id = c.id
               WHERE o.status = 'error'
               ORDER BY o.updated_at DESC"""
        ).fetchall()
    db.close()
    return [dict(r) for r in rows]


# ──────────────────────────────────────────────
# Scheduler Jobs (Sprint 17)
# ──────────────────────────────────────────────

def create_scheduler_job(
    campaign_id: Optional[str],
    job_type: str,
    scheduled_at: int,
    outreach_id: Optional[str] = None,
) -> str:
    """Create a new scheduler job and return its ID."""
    job_id = str(uuid.uuid4())
    db = get_db()
    db.execute(
        """INSERT INTO scheduler_jobs (id, campaign_id, outreach_id, job_type, status, scheduled_at)
           VALUES (?, ?, ?, ?, 'pending', ?)""",
        (job_id, campaign_id, outreach_id, job_type, scheduled_at),
    )
    db.commit()
    db.close()
    return job_id


def get_ready_jobs(limit: int = 10) -> list[dict]:
    """Get jobs that are ready to execute (pending and scheduled_at <= now).

    Core outreach jobs (invite, send_dm, followup, auto_reply) are prioritised
    over warm-up jobs (engage, follow, endorse, profile_view) so that warm-up
    never blocks outreach.
    """
    now = int(time.time())
    db = get_db()
    rows = db.execute(
        """SELECT * FROM scheduler_jobs
           WHERE status = 'pending' AND scheduled_at <= ?
           ORDER BY
               CASE job_type
                   WHEN 'invite' THEN 1
                   WHEN 'send_dm' THEN 1
                   WHEN 'followup' THEN 1
                   WHEN 'auto_reply' THEN 1
                   WHEN 'discover' THEN 2
                   WHEN 'email_fallback' THEN 2
                   WHEN 'engage' THEN 3
                   WHEN 'follow' THEN 4
                   WHEN 'endorse' THEN 4
                   WHEN 'profile_view' THEN 5
                   ELSE 3
               END,
               scheduled_at ASC
           LIMIT ?""",
        (now, limit),
    ).fetchall()
    db.close()
    return [dict(r) for r in rows]


def count_stale_ready_jobs(staleness_seconds: int = 600) -> int:
    """Count pending jobs whose scheduled_at is more than staleness_seconds in the past."""
    now = int(time.time())
    cutoff = now - staleness_seconds
    db = get_db()
    row = db.execute(
        "SELECT COUNT(*) as cnt FROM scheduler_jobs WHERE status = 'pending' AND scheduled_at <= ?",
        (cutoff,),
    ).fetchone()
    db.close()
    return dict(row).get("cnt", 0) if row else 0


def restagger_stale_jobs(staleness_seconds: int = 600, spread_seconds: int = 30) -> int:
    """Re-stagger stale pending jobs, spreading them out from now.

    Jobs are ordered by priority (core outreach first, warm-up last) then by
    original scheduled_at. Each job gets scheduled_at = now + (index * spread_seconds).

    Returns the number of re-staggered jobs.
    """
    now = int(time.time())
    cutoff = now - staleness_seconds
    db = get_db()

    # Fetch stale jobs in priority order (same as get_ready_jobs)
    rows = db.execute(
        """SELECT id FROM scheduler_jobs
           WHERE status = 'pending' AND scheduled_at <= ?
           ORDER BY
               CASE job_type
                   WHEN 'invite' THEN 1
                   WHEN 'send_dm' THEN 1
                   WHEN 'followup' THEN 1
                   WHEN 'auto_reply' THEN 1
                   WHEN 'discover' THEN 2
                   WHEN 'email_fallback' THEN 2
                   WHEN 'engage' THEN 3
                   WHEN 'follow' THEN 4
                   WHEN 'endorse' THEN 4
                   WHEN 'profile_view' THEN 5
                   ELSE 3
               END,
               scheduled_at ASC""",
        (cutoff,),
    ).fetchall()

    if not rows:
        db.close()
        return 0

    for idx, row in enumerate(rows):
        new_time = now + (idx * spread_seconds)
        db.execute(
            "UPDATE scheduler_jobs SET scheduled_at = ? WHERE id = ? AND status = 'pending'",
            (new_time, row["id"]),
        )

    db.commit()
    count = len(rows)
    db.close()
    return count


def claim_job(job_id: str) -> bool:
    """Atomically claim a pending job (set to running). Returns True if claimed."""
    now = int(time.time())
    db = get_db()
    cursor = db.execute(
        """UPDATE scheduler_jobs SET status = 'running', started_at = ?
           WHERE id = ? AND status = 'pending'""",
        (now, job_id),
    )
    db.commit()
    changed = cursor.rowcount > 0
    db.close()
    return changed


def complete_job(
    job_id: str,
    error: Optional[str] = None,
    duration_ms: Optional[int] = None,
) -> None:
    """Mark a job as completed or failed, optionally recording execution duration."""
    now = int(time.time())
    status = "failed" if error else "completed"
    db = get_db()
    if error:
        db.execute(
            """UPDATE scheduler_jobs
               SET status = ?, completed_at = ?, error = ?, retry_count = retry_count + 1,
                   duration_ms = ?
               WHERE id = ?""",
            (status, now, error, duration_ms, job_id),
        )
    else:
        db.execute(
            """UPDATE scheduler_jobs
               SET status = ?, completed_at = ?, duration_ms = ?
               WHERE id = ?""",
            (status, now, duration_ms, job_id),
        )
    db.commit()
    db.close()


def retry_job(job_id: str, new_scheduled_at: int) -> None:
    """Reset a failed job to pending with a new scheduled time."""
    db = get_db()
    db.execute(
        """UPDATE scheduler_jobs SET status = 'pending', scheduled_at = ?,
           started_at = NULL, completed_at = NULL, error = NULL
           WHERE id = ?""",
        (new_scheduled_at, job_id),
    )
    db.commit()
    db.close()


def recover_stuck_jobs(stuck_minutes: int = 30) -> int:
    """Mark stuck jobs as failed so they can be retried.

    Recovers:
    - 'running' jobs with started_at older than *stuck_minutes* (likely crashed)
    - 'pending' jobs with scheduled_at older than *stuck_minutes* (never picked up)

    Returns the number of jobs recovered.
    """
    now = int(time.time())
    cutoff = now - (stuck_minutes * 60)
    db = get_db()

    # Recover stuck running jobs
    c1 = db.execute(
        """UPDATE scheduler_jobs
           SET status = 'failed', error = 'stuck_job_recovered',
               completed_at = ?
           WHERE status = 'running' AND started_at < ?""",
        (now, cutoff),
    )

    # Recover stale pending jobs (scheduled long ago but never claimed)
    c2 = db.execute(
        """UPDATE scheduler_jobs
           SET status = 'failed', error = 'stale_pending_recovered',
               completed_at = ?
           WHERE status = 'pending' AND scheduled_at < ?""",
        (now, cutoff),
    )

    db.commit()
    count = c1.rowcount + c2.rowcount
    db.close()
    return count


# Alias for timezone-aware rescheduling (same mechanics, different semantics)
reschedule_job = retry_job


def get_pending_job_count(campaign_id: Optional[str], job_type: str) -> int:
    """Count pending/running jobs of a given type for a campaign (dedup check).

    Ignores 'running' jobs older than 10 minutes — these are assumed stuck
    (e.g. from a crashed process or stale session). Without this TTL, a single
    stuck job can block all new scheduling for the same job type indefinitely.
    """
    stale_cutoff = int(time.time()) - 600  # 10 min TTL for running jobs
    db = get_db()
    if campaign_id is None:
        row = db.execute(
            """SELECT COUNT(*) as cnt FROM scheduler_jobs
               WHERE campaign_id IS NULL AND job_type = ?
               AND (
                   (status = 'pending')
                   OR (status = 'running' AND started_at > ?)
               )""",
            (job_type, stale_cutoff),
        ).fetchone()
    else:
        row = db.execute(
            """SELECT COUNT(*) as cnt FROM scheduler_jobs
               WHERE campaign_id = ? AND job_type = ?
               AND (
                   (status = 'pending')
                   OR (status = 'running' AND started_at > ?)
               )""",
            (campaign_id, job_type, stale_cutoff),
        ).fetchone()
    db.close()
    return row["cnt"] if row else 0


def get_pending_outreach_job(outreach_id: str, job_type: str) -> Optional[dict]:
    """Check if a specific outreach already has a pending/running job of this type.

    Ignores 'running' jobs older than 10 minutes (assumed stuck).
    """
    stale_cutoff = int(time.time()) - 600  # 10 min TTL for running jobs
    db = get_db()
    row = db.execute(
        """SELECT * FROM scheduler_jobs
           WHERE outreach_id = ? AND job_type = ?
           AND (
               (status = 'pending')
               OR (status = 'running' AND started_at > ?)
           )
           LIMIT 1""",
        (outreach_id, job_type, stale_cutoff),
    ).fetchone()
    db.close()
    return dict(row) if row else None


def cleanup_old_jobs(days: int = 7) -> int:
    """Purge completed/failed jobs older than N days.

    Also purges failed jobs with max retries that are older than 1 day
    (these won't be retried and just waste queue space).
    Returns total count deleted.
    """
    cutoff = int(time.time()) - (days * 86400)
    cutoff_failed = int(time.time()) - 86400  # 1 day for exhausted failures
    db = get_db()
    cursor = db.execute(
        """DELETE FROM scheduler_jobs
           WHERE (status IN ('completed', 'failed') AND created_at < ?)
              OR (status = 'failed' AND retry_count >= 3 AND created_at < ?)""",
        (cutoff, cutoff_failed),
    )
    db.commit()
    deleted = cursor.rowcount
    db.close()
    return deleted


def cleanup_failed_engage_jobs() -> dict[str, int]:
    """Clean up failed engage jobs and set time-limited cooldown on their outreaches.

    Returns dict with 'cleaned' (jobs deleted) and 'marked' (outreaches cooldown-set).
    """
    import json as _json

    db = get_db()
    rows = db.execute(
        """SELECT j.id, j.outreach_id
           FROM scheduler_jobs j
           WHERE j.job_type = 'engage' AND j.status = 'failed'""",
    ).fetchall()
    jobs = [dict(r) for r in rows]

    if not jobs:
        db.close()
        return {"cleaned": 0, "marked": 0}

    cooldown_until = int(time.time()) + 24 * 3600  # 24h cooldown
    cooldown_json = _json.dumps({"skip_engagement_until": cooldown_until})

    marked = 0
    for j in jobs:
        outreach_id = j.get("outreach_id")
        if outreach_id:
            db.execute(
                "UPDATE outreaches SET next_action = ? WHERE id = ?",
                (cooldown_json, outreach_id),
            )
            marked += 1
        db.execute("DELETE FROM scheduler_jobs WHERE id = ?", (j["id"],))

    db.commit()
    db.close()
    return {"cleaned": len(jobs), "marked": marked}


def cleanup_failed_invite_jobs() -> dict[str, int]:
    """Clean up failed invite jobs. Returns dict with 'cleaned' count."""
    db = get_db()
    rows = db.execute(
        """SELECT j.id FROM scheduler_jobs j
           WHERE j.job_type = 'invite' AND j.status = 'failed'""",
    ).fetchall()
    jobs = [dict(r) for r in rows]

    if not jobs:
        db.close()
        return {"cleaned": 0}

    for j in jobs:
        db.execute("DELETE FROM scheduler_jobs WHERE id = ?", (j["id"],))
    db.commit()
    db.close()
    return {"cleaned": len(jobs)}


def recover_stuck_running_jobs(timeout_seconds: int = 600) -> int:
    """Reset jobs stuck in 'running' state for longer than timeout.

    If a job has been 'running' for more than timeout_seconds (default 10 min),
    it's assumed the process crashed. Reset to 'pending' for retry if under
    max retries, or mark 'failed' if retries exhausted.

    Returns total number of recovered/failed jobs.
    """
    cutoff = int(time.time()) - timeout_seconds
    db = get_db()
    # Reset to pending if under retry limit
    cursor = db.execute(
        """UPDATE scheduler_jobs
           SET status = 'pending', started_at = NULL
           WHERE status = 'running' AND started_at < ? AND retry_count < 3""",
        (cutoff,),
    )
    recovered = cursor.rowcount
    # Fail if over retry limit
    cursor2 = db.execute(
        """UPDATE scheduler_jobs
           SET status = 'failed', completed_at = ?, error = 'Stuck running job timed out'
           WHERE status = 'running' AND started_at < ? AND retry_count >= 3""",
        (int(time.time()), cutoff),
    )
    timed_out = cursor2.rowcount
    db.commit()
    db.close()
    return recovered + timed_out


def recover_stuck_sending_outreaches(timeout_seconds: int = 600) -> int:
    """Recover outreaches stuck in 'sending' or 'sending_followup' state.

    If an outreach has been in a transitional send state for longer than
    timeout_seconds (default 10 min), it's assumed the send process crashed.
    Transitions to 'messaged' if a message was actually sent, otherwise
    back to 'connected'.

    Returns total number of recovered outreaches.
    """
    cutoff = int(time.time()) - timeout_seconds
    db = get_db()
    # Find stuck outreaches
    stuck = db.execute(
        """SELECT o.id, o.status
           FROM outreaches o
           WHERE o.status IN ('sending', 'sending_followup')
             AND o.updated_at < ?""",
        (cutoff,),
    ).fetchall()
    if not stuck:
        db.close()
        return 0

    recovered = 0
    now = int(time.time())
    for row in stuck:
        oid = row["id"]
        # Check if a message was actually sent
        has_msg = db.execute(
            "SELECT 1 FROM messages WHERE outreach_id = ? AND role = 'sdr' LIMIT 1",
            (oid,),
        ).fetchone()
        new_status = "messaged" if has_msg else "connected"
        db.execute(
            "UPDATE outreaches SET status = ?, updated_at = ? WHERE id = ?",
            (new_status, now, oid),
        )
        recovered += 1
    db.commit()
    db.close()
    return recovered


def get_scheduler_stats() -> dict:
    """Get scheduler job stats for the dashboard."""
    db = get_db()
    rows = db.execute(
        """SELECT status, job_type, COUNT(*) as cnt
           FROM scheduler_jobs
           GROUP BY status, job_type"""
    ).fetchall()

    # Next scheduled jobs
    next_jobs = db.execute(
        """SELECT job_type, scheduled_at, outreach_id
           FROM scheduler_jobs
           WHERE status = 'pending'
           ORDER BY scheduled_at ASC
           LIMIT 5"""
    ).fetchall()

    # Recent completed/failed
    recent = db.execute(
        """SELECT job_type, status, completed_at, error
           FROM scheduler_jobs
           WHERE status IN ('completed', 'failed')
           ORDER BY completed_at DESC
           LIMIT 10"""
    ).fetchall()

    db.close()
    return {
        "counts": [dict(r) for r in rows],
        "next_jobs": [dict(r) for r in next_jobs],
        "recent": [dict(r) for r in recent],
    }


# ──────────────────────────────────────────────
# Scheduler Events (structured observability log)
# ──────────────────────────────────────────────


def log_scheduler_event(
    event_type: str,
    *,
    campaign_id: Optional[str] = None,
    outreach_id: Optional[str] = None,
    job_id: Optional[str] = None,
    context: Optional[dict] = None,
    duration_ms: Optional[int] = None,
) -> None:
    """Fire-and-forget INSERT into scheduler_events. Never raises."""
    try:
        db = get_db()
        db.execute(
            """INSERT INTO scheduler_events
               (id, event_type, campaign_id, outreach_id, job_id, context, duration_ms, created_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                str(uuid.uuid4()),
                event_type,
                campaign_id,
                outreach_id,
                job_id,
                json.dumps(context or {}),
                duration_ms,
                int(time.time()),
            ),
        )
        db.commit()
        db.close()
    except Exception as e:
        logger.warning("log_scheduler_event FAILED for %s: %s", event_type, e)


def get_recent_scheduler_events(
    hours: int = 24,
    event_type: str = "",
    campaign_id: str = "",
    limit: int = 100,
) -> list[dict]:
    """Query recent scheduler events, newest first."""
    db = get_db()
    since = int(time.time()) - (hours * 3600)
    sql = "SELECT * FROM scheduler_events WHERE created_at >= ?"
    params: list[Any] = [since]

    if event_type:
        sql += " AND event_type = ?"
        params.append(event_type)
    if campaign_id:
        sql += " AND campaign_id = ?"
        params.append(campaign_id)

    sql += " ORDER BY created_at DESC LIMIT ?"
    params.append(min(limit, 500))

    rows = db.execute(sql, params).fetchall()
    db.close()

    events = []
    for r in rows:
        evt = dict(r)
        ctx = evt.get("context", "{}")
        if isinstance(ctx, str):
            try:
                evt["context"] = json.loads(ctx)
            except (json.JSONDecodeError, TypeError):
                pass
        events.append(evt)
    return events


def get_scheduler_event_summary(hours: int = 24) -> dict[str, int]:
    """GROUP BY event_type -> {type: count} for the last N hours."""
    db = get_db()
    since = int(time.time()) - (hours * 3600)
    rows = db.execute(
        """SELECT event_type, COUNT(*) as cnt FROM scheduler_events
           WHERE created_at >= ?
           GROUP BY event_type ORDER BY cnt DESC""",
        (since,),
    ).fetchall()
    db.close()
    return {dict(r)["event_type"]: dict(r)["cnt"] for r in rows}


def get_job_metrics(hours: int = 24) -> dict[str, dict]:
    """Rolling window metrics per job type from scheduler_events.

    Returns {job_type: {total, success, skipped, deferred, permanent_failure,
    failed, success_rate, avg_duration_ms}}.

    Event types:
    - job_completed  → actual success (action was performed)
    - job_skipped    → pre-check blocked it (status changed, not connected, etc.)
    - job_deferred   → budget exhausted / will retry later
    - job_permanent_failure → action failed and won't be retried
    - job_failed     → transient error (exception), may be retried
    """
    db = get_db()
    since = int(time.time()) - (hours * 3600)
    rows = db.execute(
        """SELECT
               json_extract(context, '$.job_type') as jtype,
               event_type,
               COUNT(*) as cnt,
               AVG(duration_ms) as avg_dur
           FROM scheduler_events
           WHERE event_type IN ('job_completed', 'job_failed',
                                'job_skipped', 'job_deferred', 'job_permanent_failure')
             AND created_at >= ?
           GROUP BY jtype, event_type""",
        (since,),
    ).fetchall()
    db.close()

    _EMPTY = {"total": 0, "success": 0, "skipped": 0, "deferred": 0,
              "permanent_failure": 0, "failed": 0, "avg_duration_ms": 0}
    metrics: dict[str, dict] = {}
    for r in rows:
        row = dict(r)
        jtype = row.get("jtype") or "unknown"
        if jtype not in metrics:
            metrics[jtype] = dict(_EMPTY)
        cnt = row["cnt"]
        evt = row["event_type"]
        if evt == "job_completed":
            metrics[jtype]["success"] += cnt
            metrics[jtype]["avg_duration_ms"] = int(row["avg_dur"] or 0)
        elif evt == "job_skipped":
            metrics[jtype]["skipped"] += cnt
        elif evt == "job_deferred":
            metrics[jtype]["deferred"] += cnt
        elif evt == "job_permanent_failure":
            metrics[jtype]["permanent_failure"] += cnt
        else:
            metrics[jtype]["failed"] += cnt
        metrics[jtype]["total"] += cnt

    # Compute success rates (success / total that actually attempted)
    for m in metrics.values():
        attempted = m["total"] - m["skipped"] - m["deferred"]
        if attempted > 0:
            m["success_rate"] = round(m["success"] / attempted * 100, 1)
        else:
            m["success_rate"] = 0.0

    return metrics


def cleanup_scheduler_events(days: int = 7) -> int:
    """Delete events older than retention period. Returns count deleted."""
    db = get_db()
    cutoff = int(time.time()) - (days * 86400)
    cursor = db.execute(
        "DELETE FROM scheduler_events WHERE created_at < ?", (cutoff,),
    )
    db.commit()
    deleted = cursor.rowcount
    db.close()
    return deleted


# ──────────────────────────────────────────────
# Experiments (PM hypothesis tracking)
# ──────────────────────────────────────────────


def save_experiment(
    snapshot: str, result_json: str, campaign_ids: str = "",
) -> str:
    """Save an experiment analysis result. Returns experiment ID."""
    exp_id = str(uuid.uuid4())
    db = get_db()
    db.execute(
        """INSERT INTO experiments (id, snapshot, result_json, campaign_ids, created_at)
           VALUES (?, ?, ?, ?, ?)""",
        (exp_id, snapshot, result_json, campaign_ids, int(time.time())),
    )
    db.commit()
    db.close()
    return exp_id


def list_experiments(limit: int = 5) -> list[dict]:
    """List recent experiments, newest first."""
    db = get_db()
    rows = db.execute(
        "SELECT * FROM experiments ORDER BY created_at DESC LIMIT ?",
        (limit,),
    ).fetchall()
    db.close()
    return [dict(r) for r in rows]


def update_experiment_status(exp_id: str, status: str) -> None:
    """Update experiment status: pending/tested/validated/dismissed."""
    db = get_db()
    db.execute(
        "UPDATE experiments SET status = ? WHERE id = ?",
        (status, exp_id),
    )
    db.commit()
    db.close()


def get_deal_profiles(
    campaign_id: str, status: str, limit: int = 3,
) -> list[dict]:
    """Get contact profiles for won or lost deals.

    Args:
        campaign_id: Campaign to query.
        status: 'closed_happy' or 'closed_unhappy'.
        limit: Max profiles to return.
    """
    db = get_db()
    rows = db.execute(
        """SELECT c.name, c.title, c.company, c.fit_score, o.status
           FROM outreaches o
           JOIN contacts c ON o.contact_id = c.id
           WHERE o.campaign_id = ? AND o.status = ?
           ORDER BY o.updated_at DESC LIMIT ?""",
        (campaign_id, status, limit),
    ).fetchall()
    db.close()
    return [dict(r) for r in rows]


# ──────────────────────────────────────────────
# A/B Tests
# ──────────────────────────────────────────────


def create_ab_test(
    campaign_id: str,
    name: str,
    variant_a: str,
    variant_b: str,
    hypothesis: str = "",
    test_type: str = "message",
) -> str:
    """Create a new A/B test for a campaign. Returns test ID.

    ``test_type`` is ``"message"`` (default) or ``"headline"``.
    """
    test_id = str(uuid.uuid4())
    db = get_db()
    db.execute(
        """INSERT INTO ab_tests (id, campaign_id, name, hypothesis, variant_a, variant_b, test_type)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (test_id, campaign_id, name, hypothesis, variant_a, variant_b, test_type),
    )
    db.commit()
    db.close()
    return test_id


def get_ab_test(test_id: str) -> dict | None:
    """Get an A/B test by ID."""
    db = get_db()
    row = db.execute("SELECT * FROM ab_tests WHERE id = ?", (test_id,)).fetchone()
    db.close()
    return dict(row) if row else None


def list_ab_tests(campaign_id: str = "", status: str = "") -> list[dict]:
    """List A/B tests, optionally filtered by campaign and/or status."""
    db = get_db()
    q = "SELECT * FROM ab_tests"
    params: list = []
    clauses: list[str] = []
    if campaign_id:
        clauses.append("campaign_id = ?")
        params.append(campaign_id)
    if status:
        clauses.append("status = ?")
        params.append(status)
    if clauses:
        q += " WHERE " + " AND ".join(clauses)
    q += " ORDER BY created_at DESC"
    rows = db.execute(q, params).fetchall()
    db.close()
    return [dict(r) for r in rows]


def complete_ab_test(
    test_id: str,
    winner: str,
    result_json: str = "",
) -> None:
    """Mark an A/B test as completed with a winner."""
    db = get_db()
    db.execute(
        """UPDATE ab_tests
           SET status = 'completed', winner = ?, result_json = ?,
               completed_at = strftime('%s', 'now')
           WHERE id = ?""",
        (winner, result_json, test_id),
    )
    db.commit()
    db.close()


def get_variant_stats(campaign_id: str) -> dict:
    """Get per-variant funnel stats for A/B testing.

    Returns {"A": {invited, connected, replied, ...}, "B": {...}, None: {...}}.
    """
    db = get_db()
    rows = db.execute(
        """SELECT variant,
                  COUNT(*) as total,
                  SUM(CASE WHEN status != 'pending' THEN 1 ELSE 0 END) as invited,
                  SUM(CASE WHEN status IN ('connected','messaged','replied','hot_lead',
                       'closed_happy','closed_unhappy') THEN 1 ELSE 0 END) as connected,
                  SUM(CASE WHEN status IN ('replied','hot_lead',
                       'closed_happy','closed_unhappy') THEN 1 ELSE 0 END) as replied,
                  SUM(CASE WHEN status = 'hot_lead' THEN 1 ELSE 0 END) as hot_leads,
                  SUM(CASE WHEN status = 'closed_happy' THEN 1 ELSE 0 END) as won,
                  SUM(CASE WHEN status = 'closed_unhappy' THEN 1 ELSE 0 END) as lost
           FROM outreaches
           WHERE campaign_id = ?
           GROUP BY variant""",
        (campaign_id,),
    ).fetchall()
    db.close()
    result = {}
    for r in rows:
        d = dict(r)
        variant = d.pop("variant")
        invited = d.get("invited", 0)
        connected = d.get("connected", 0)
        d["acceptance_rate"] = round(connected / invited * 100, 1) if invited else 0
        d["reply_rate"] = round(d.get("replied", 0) / connected * 100, 1) if connected else 0
        result[variant] = d
    return result


def assign_variant(campaign_id: str) -> str:
    """Assign the next prospect to variant A or B (round-robin).

    Counts current variant distribution and assigns to the underrepresented one.
    Returns 'A' or 'B'.
    """
    db = get_db()
    rows = db.execute(
        """SELECT variant, COUNT(*) as cnt
           FROM outreaches
           WHERE campaign_id = ? AND variant IS NOT NULL
           GROUP BY variant""",
        (campaign_id,),
    ).fetchall()
    db.close()
    counts = {dict(r)["variant"]: dict(r)["cnt"] for r in rows}
    a_count = counts.get("A", 0)
    b_count = counts.get("B", 0)
    return "A" if a_count <= b_count else "B"


# ──────────────────────────────────────────────
# Cohort Analysis (Feature 4.3)
# ──────────────────────────────────────────────


def get_cohort_analysis(campaign_id: str) -> list[dict]:
    """Group outreaches by invitation week and compute per-cohort funnel stats.

    Returns a list of cohort dicts sorted by week:
    [{"cohort": "2026-W08", "invited": 15, "connected": 8, ...}]
    """
    db = get_db()
    rows = db.execute(
        """SELECT
               CASE
                   WHEN invited_at IS NOT NULL
                   THEN strftime('%%Y-W%%W', invited_at, 'unixepoch')
                   ELSE 'Not invited'
               END as cohort,
               COUNT(*) as total,
               SUM(CASE WHEN status IN ('invited','connected','replied','hot_lead',
                    'messaged','closed_happy','closed_unhappy','opted_out','reverse_pitch')
                    THEN 1 ELSE 0 END) as invited,
               SUM(CASE WHEN status IN ('connected','replied','hot_lead',
                    'messaged','closed_happy','closed_unhappy','reverse_pitch','opted_out')
                    THEN 1 ELSE 0 END) as connected,
               SUM(CASE WHEN status IN ('replied','hot_lead','closed_happy','closed_unhappy','reverse_pitch','opted_out')
                    THEN 1 ELSE 0 END) as replied,
               SUM(CASE WHEN status = 'hot_lead' THEN 1 ELSE 0 END) as hot_lead,
               SUM(CASE WHEN status = 'closed_happy' THEN 1 ELSE 0 END) as won,
               SUM(CASE WHEN status = 'closed_unhappy' THEN 1 ELSE 0 END) as lost
           FROM outreaches
           WHERE campaign_id = ?
           GROUP BY cohort
           ORDER BY cohort""",
        (campaign_id,),
    ).fetchall()
    db.close()

    cohorts = []
    for r in rows:
        d = dict(r)
        invited = d.get("invited", 0)
        connected = d.get("connected", 0)
        d["acceptance_rate"] = round(connected / invited * 100, 1) if invited else 0
        d["reply_rate"] = round(d.get("replied", 0) / connected * 100, 1) if connected else 0
        cohorts.append(d)
    return cohorts


def get_time_series_stats(campaign_id: str) -> list[dict]:
    """Get daily activity counts for a campaign (last 30 days).

    Returns: [{"date": "2026-02-24", "invites": 3, "replies": 1, "connections": 2}]
    """
    db = get_db()
    cutoff = int(time.time()) - (30 * 86400)

    rows = db.execute(
        """SELECT
               date(created_at, 'unixepoch') as date,
               SUM(CASE WHEN status != 'pending' THEN 1 ELSE 0 END) as invites,
               SUM(CASE WHEN status IN ('connected','replied','hot_lead',
                    'messaged','closed_happy','closed_unhappy','reverse_pitch','opted_out')
                    THEN 1 ELSE 0 END) as connections,
               SUM(CASE WHEN status IN ('replied','hot_lead','closed_happy','closed_unhappy','reverse_pitch','opted_out')
                    THEN 1 ELSE 0 END) as replies
           FROM outreaches
           WHERE campaign_id = ? AND created_at > ?
           GROUP BY date
           ORDER BY date""",
        (campaign_id, cutoff),
    ).fetchall()
    db.close()
    return [dict(r) for r in rows]


def get_full_campaign_export(campaign_id: str) -> list[dict]:
    """Get all contacts with outreach data for export.

    Returns a list of dicts with contact + outreach fields for CSV/JSON export.
    """
    db = get_db()
    rows = db.execute(
        """SELECT
               c.name, c.title, c.company, c.linkedin_url, c.linkedin_id,
               c.fit_score,
               o.status, o.channel, o.followup_count, o.variant,
               o.invited_at, o.accepted_at, o.first_reply_at,
               o.outcome_json, o.created_at as outreach_created_at
           FROM outreaches o
           JOIN contacts c ON c.id = o.contact_id
           WHERE o.campaign_id = ?
           ORDER BY o.created_at""",
        (campaign_id,),
    ).fetchall()
    db.close()
    return [dict(r) for r in rows]


# ──────────────────────────────────────────────
# CRM Mappings (Feature 4.4)
# ──────────────────────────────────────────────


def get_crm_mapping(contact_id: str, crm_type: str = "hubspot") -> dict | None:
    """Get an existing CRM mapping for a contact."""
    db = get_db()
    row = db.execute(
        "SELECT * FROM crm_mappings WHERE contact_id = ? AND crm_type = ?",
        (contact_id, crm_type),
    ).fetchone()
    db.close()
    return dict(row) if row else None


def save_crm_mapping(
    contact_id: str,
    crm_type: str = "hubspot",
    crm_contact_id: str = "",
    crm_deal_id: str = "",
) -> str:
    """Create or update a CRM mapping."""
    now = int(time.time())
    existing = get_crm_mapping(contact_id, crm_type)
    db = get_db()
    if existing:
        updates = []
        params: list[Any] = []
        if crm_contact_id:
            updates.append("crm_contact_id = ?")
            params.append(crm_contact_id)
        if crm_deal_id:
            updates.append("crm_deal_id = ?")
            params.append(crm_deal_id)
        updates.append("synced_at = ?")
        params.append(now)
        params.append(existing["id"])
        db.execute(f"UPDATE crm_mappings SET {', '.join(updates)} WHERE id = ?", params)
        db.commit()
        db.close()
        return existing["id"]
    else:
        mapping_id = str(uuid.uuid4())
        db.execute(
            """INSERT INTO crm_mappings (id, contact_id, crm_type, crm_contact_id, crm_deal_id, synced_at, created_at)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (mapping_id, contact_id, crm_type, crm_contact_id, crm_deal_id, now, now),
        )
        db.commit()
        db.close()
        return mapping_id


def get_unsynced_won_outreaches(campaign_id: str) -> list[dict]:
    """Get won outreaches that haven't been synced to CRM yet."""
    db = get_db()
    rows = db.execute(
        """SELECT o.id as outreach_id, o.contact_id, o.outcome_json,
                  c.name, c.title, c.company, c.linkedin_url, c.linkedin_id
           FROM outreaches o
           JOIN contacts c ON c.id = o.contact_id
           LEFT JOIN crm_mappings m ON m.contact_id = c.id AND m.crm_type = 'hubspot'
           WHERE o.campaign_id = ? AND o.status = 'closed_happy'
             AND m.id IS NULL
           ORDER BY o.updated_at DESC""",
        (campaign_id,),
    ).fetchall()
    db.close()
    return [dict(r) for r in rows]


def get_hot_lead_outreaches(campaign_id: str) -> list[dict]:
    """Get hot lead outreaches for CRM sync."""
    db = get_db()
    rows = db.execute(
        """SELECT o.id as outreach_id, o.contact_id, o.outcome_json,
                  c.name, c.title, c.company, c.linkedin_url, c.linkedin_id
           FROM outreaches o
           JOIN contacts c ON c.id = o.contact_id
           WHERE o.campaign_id = ? AND o.status = 'hot_lead'
           ORDER BY o.updated_at DESC""",
        (campaign_id,),
    ).fetchall()
    db.close()
    return [dict(r) for r in rows]


# ──────────────────────────────────────────────
# Inbound Signals (Pipeline)
# ──────────────────────────────────────────────


def save_inbound_signal(
    signal_type: str,
    sender_name: str = "",
    sender_id: str = "",
    sender_headline: str = "",
    sender_company: str = "",
    sender_url: str = "",
    content: str = "",
    post_id: str = "",
    profile_json: str = "",
    invitation_id: str = "",
    message_id: str = "",
) -> str:
    """Save a new inbound signal (invitation, message, or comment). Returns signal ID."""
    signal_id = str(uuid.uuid4())
    db = get_db()
    db.execute(
        """INSERT INTO inbound_signals
           (id, signal_type, sender_name, sender_id, sender_headline,
            sender_company, sender_url, content, post_id, profile_json,
            invitation_id, message_id, created_at)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (signal_id, signal_type, sender_name, sender_id, sender_headline,
         sender_company, sender_url, content, post_id, profile_json,
         invitation_id or None, message_id or None, int(time.time())),
    )
    db.commit()
    db.close()
    return signal_id


def get_inbound_signal(signal_id: str) -> Optional[dict]:
    """Get an inbound signal by ID."""
    db = get_db()
    row = db.execute("SELECT * FROM inbound_signals WHERE id = ?", (signal_id,)).fetchone()
    db.close()
    return dict(row) if row else None


def list_inbound_signals(
    status: str = "",
    signal_type: str = "",
    limit: int = 50,
) -> list[dict]:
    """List inbound signals, optionally filtered by status and/or type."""
    db = get_db()
    q = "SELECT * FROM inbound_signals"
    params: list[Any] = []
    clauses: list[str] = []
    if status:
        clauses.append("status = ?")
        params.append(status)
    if signal_type:
        clauses.append("signal_type = ?")
        params.append(signal_type)
    if clauses:
        q += " WHERE " + " AND ".join(clauses)
    q += " ORDER BY created_at DESC LIMIT ?"
    params.append(limit)
    rows = db.execute(q, params).fetchall()
    db.close()
    return [dict(r) for r in rows]


_VALID_INBOUND_SIGNAL_COLS = frozenset({
    "signal_type", "sender_name", "sender_id", "sender_headline",
    "sender_company", "sender_url", "content", "post_id", "profile_json",
    "intent", "matched_icp_id", "confidence", "recommended_action",
    "reasoning", "status", "campaign_id", "qualified_at", "outreach_id",
    "dm_attempts",
    # Inbound Pipeline v2:
    "invitation_id", "actioned_at", "decline_reason", "message_id",
    "reaction_sent",
})


def update_inbound_signal(signal_id: str, **kwargs: Any) -> None:
    """Update an inbound signal's fields."""
    bad_keys = set(kwargs) - _VALID_INBOUND_SIGNAL_COLS
    if bad_keys:
        raise ValueError(f"Invalid inbound_signal columns: {bad_keys}")
    if not kwargs:
        return
    db = get_db()
    set_clause = ", ".join(f"{k} = ?" for k in kwargs)
    values = list(kwargs.values()) + [signal_id]
    db.execute(f"UPDATE inbound_signals SET {set_clause} WHERE id = ?", values)
    db.commit()
    db.close()


def get_inbound_signal_by_sender(
    sender_id: str,
    signal_type: str = "",
) -> Optional[dict]:
    """Find an existing inbound signal by sender_id (dedup check)."""
    db = get_db()
    if signal_type:
        row = db.execute(
            "SELECT * FROM inbound_signals WHERE sender_id = ? AND signal_type = ? ORDER BY created_at DESC LIMIT 1",
            (sender_id, signal_type),
        ).fetchone()
    else:
        row = db.execute(
            "SELECT * FROM inbound_signals WHERE sender_id = ? ORDER BY created_at DESC LIMIT 1",
            (sender_id,),
        ).fetchone()
    db.close()
    return dict(row) if row else None


def count_inbound_signals(status: str = "", signal_type: str = "") -> int:
    """Count inbound signals, optionally filtered."""
    db = get_db()
    q = "SELECT COUNT(*) as c FROM inbound_signals"
    params: list[Any] = []
    clauses: list[str] = []
    if status:
        clauses.append("status = ?")
        params.append(status)
    if signal_type:
        clauses.append("signal_type = ?")
        params.append(signal_type)
    if clauses:
        q += " WHERE " + " AND ".join(clauses)
    row = db.execute(q, params).fetchone()
    db.close()
    return row["c"] if row else 0


def count_inbound_dms_today() -> int:
    """Count discovery DMs sent today using the actions_log."""
    from datetime import date, datetime, time as dtime

    today_start = int(datetime.combine(date.today(), dtime.min).timestamp())
    db = get_db()
    row = db.execute(
        "SELECT COUNT(*) as c FROM actions_log "
        "WHERE action_type = 'inbound_discovery_dm_sent' AND timestamp >= ?",
        (today_start,),
    ).fetchone()
    db.close()
    return row["c"] if row else 0


def get_inbound_funnel_stats() -> dict:
    """Get inbound pipeline funnel stats grouped by status and intent."""
    db = get_db()
    status_rows = db.execute(
        "SELECT status, COUNT(*) as c FROM inbound_signals GROUP BY status"
    ).fetchall()
    intent_rows = db.execute(
        "SELECT intent, COUNT(*) as c FROM inbound_signals WHERE intent IS NOT NULL GROUP BY intent"
    ).fetchall()
    type_rows = db.execute(
        "SELECT signal_type, COUNT(*) as c FROM inbound_signals GROUP BY signal_type"
    ).fetchall()
    db.close()
    return {
        "by_status": {r["status"]: r["c"] for r in status_rows},
        "by_intent": {r["intent"]: r["c"] for r in intent_rows},
        "by_type": {r["signal_type"]: r["c"] for r in type_rows},
        "total": sum(r["c"] for r in status_rows),
    }


# ──────────────────────────────────────────────
# Published Posts (for inbound comment monitoring)
# ──────────────────────────────────────────────


def save_published_post(
    post_id: str,
    text: str = "",
    topic: str = "",
) -> str:
    """Save a published post for comment monitoring. Returns record ID."""
    record_id = str(uuid.uuid4())
    db = get_db()
    db.execute(
        """INSERT INTO published_posts (id, post_id, text, topic, published_at)
           VALUES (?, ?, ?, ?, ?)""",
        (record_id, post_id, text, topic, int(time.time())),
    )
    db.commit()
    db.close()
    return record_id


def list_published_posts(days: int = 7) -> list[dict]:
    """List recently published posts that need comment monitoring."""
    cutoff = int(time.time()) - (days * 86400)
    db = get_db()
    rows = db.execute(
        "SELECT * FROM published_posts WHERE published_at >= ? ORDER BY published_at DESC",
        (cutoff,),
    ).fetchall()
    db.close()
    return [dict(r) for r in rows]


def get_voice_memo_stats(campaign_id: str = "") -> dict:
    """Get voice memo statistics for analytics.

    Returns: {voice_sent, text_sent, voice_reply_rate, text_reply_rate}
    """
    db = get_db()
    if campaign_id:
        row = db.execute(
            """SELECT
                   SUM(CASE WHEN m.format = 'voice' THEN 1 ELSE 0 END) as voice_sent,
                   SUM(CASE WHEN m.format != 'voice' THEN 1 ELSE 0 END) as text_sent
               FROM messages m
               JOIN outreaches o ON m.outreach_id = o.id
               WHERE o.campaign_id = ? AND m.role = 'sdr'""",
            (campaign_id,),
        ).fetchone()
        # Reply rates per format
        voice_reply_row = db.execute(
            """SELECT COUNT(DISTINCT o.id) as cnt
               FROM outreaches o
               JOIN messages m ON m.outreach_id = o.id
               WHERE o.campaign_id = ?
                 AND o.status IN ('replied', 'hot_lead', 'closed_happy', 'closed_unhappy', 'reverse_pitch', 'opted_out')
                 AND m.format = 'voice' AND m.role = 'sdr'""",
            (campaign_id,),
        ).fetchone()
        text_reply_row = db.execute(
            """SELECT COUNT(DISTINCT o.id) as cnt
               FROM outreaches o
               JOIN messages m ON m.outreach_id = o.id
               WHERE o.campaign_id = ?
                 AND o.status IN ('replied', 'hot_lead', 'closed_happy', 'closed_unhappy', 'reverse_pitch', 'opted_out')
                 AND m.format != 'voice' AND m.role = 'sdr'""",
            (campaign_id,),
        ).fetchone()
        # Total outreaches that received voice vs text
        voice_total_row = db.execute(
            """SELECT COUNT(DISTINCT o.id) as cnt
               FROM outreaches o
               JOIN messages m ON m.outreach_id = o.id
               WHERE o.campaign_id = ? AND m.format = 'voice' AND m.role = 'sdr'""",
            (campaign_id,),
        ).fetchone()
        text_total_row = db.execute(
            """SELECT COUNT(DISTINCT o.id) as cnt
               FROM outreaches o
               JOIN messages m ON m.outreach_id = o.id
               WHERE o.campaign_id = ? AND m.format != 'voice' AND m.role = 'sdr'""",
            (campaign_id,),
        ).fetchone()
    else:
        row = db.execute(
            """SELECT
                   SUM(CASE WHEN format = 'voice' THEN 1 ELSE 0 END) as voice_sent,
                   SUM(CASE WHEN format != 'voice' THEN 1 ELSE 0 END) as text_sent
               FROM messages WHERE role = 'sdr'"""
        ).fetchone()
        voice_reply_row = db.execute(
            """SELECT COUNT(DISTINCT o.id) as cnt
               FROM outreaches o
               JOIN messages m ON m.outreach_id = o.id
               WHERE o.status IN ('replied', 'hot_lead', 'closed_happy', 'closed_unhappy', 'reverse_pitch', 'opted_out')
                 AND m.format = 'voice' AND m.role = 'sdr'"""
        ).fetchone()
        text_reply_row = db.execute(
            """SELECT COUNT(DISTINCT o.id) as cnt
               FROM outreaches o
               JOIN messages m ON m.outreach_id = o.id
               WHERE o.status IN ('replied', 'hot_lead', 'closed_happy', 'closed_unhappy', 'reverse_pitch', 'opted_out')
                 AND m.format != 'voice' AND m.role = 'sdr'"""
        ).fetchone()
        voice_total_row = db.execute(
            """SELECT COUNT(DISTINCT o.id) as cnt
               FROM outreaches o
               JOIN messages m ON m.outreach_id = o.id
               WHERE m.format = 'voice' AND m.role = 'sdr'"""
        ).fetchone()
        text_total_row = db.execute(
            """SELECT COUNT(DISTINCT o.id) as cnt
               FROM outreaches o
               JOIN messages m ON m.outreach_id = o.id
               WHERE m.format != 'voice' AND m.role = 'sdr'"""
        ).fetchone()
    db.close()

    voice_sent = (row["voice_sent"] if row and row["voice_sent"] else 0)
    text_sent = (row["text_sent"] if row and row["text_sent"] else 0)
    voice_replied = voice_reply_row["cnt"] if voice_reply_row else 0
    text_replied = text_reply_row["cnt"] if text_reply_row else 0
    voice_total = voice_total_row["cnt"] if voice_total_row else 0
    text_total = text_total_row["cnt"] if text_total_row else 0

    return {
        "voice_sent": voice_sent,
        "text_sent": text_sent,
        "voice_reply_rate": voice_replied / voice_total if voice_total > 0 else 0.0,
        "text_reply_rate": text_replied / text_total if text_total > 0 else 0.0,
        "voice_replied": voice_replied,
        "text_replied": text_replied,
        "voice_total_outreaches": voice_total,
        "text_total_outreaches": text_total,
    }


def get_daily_voice_memo_count() -> int:
    """Count voice memos sent today for rate limiting."""
    import datetime
    today = datetime.date.today()
    today_start = int(time.mktime(today.timetuple()))
    db = get_db()
    row = db.execute(
        "SELECT COUNT(*) as c FROM messages WHERE format = 'voice' AND timestamp >= ?",
        (today_start,),
    ).fetchone()
    db.close()
    return row["c"] if row else 0


def update_published_post(post_id: str, last_checked: int, comment_count: int) -> None:
    """Update a published post's monitoring state."""
    db = get_db()
    db.execute(
        "UPDATE published_posts SET last_checked = ?, comment_count = ? WHERE post_id = ?",
        (last_checked, comment_count, post_id),
    )
    db.commit()
    db.close()


# ──────────────────────────────────────────────
# Partner Follow-Up Tracking
# ──────────────────────────────────────────────


def create_partner_followup(
    name: str,
    company: str = "",
    email: str = "",
    context: str = "",
    next_followup_ts: int | None = None,
) -> str:
    """Create a new partner follow-up record. Returns the new ID."""
    import uuid

    partner_id = str(uuid.uuid4())[:8]
    now = int(time.time())
    if next_followup_ts is None:
        next_followup_ts = now + 86400  # default: tomorrow
    db = get_db()
    db.execute(
        """INSERT INTO partner_followups
           (id, name, company, email, context, status,
            followup_count, next_followup, last_contacted, notes,
            created_at, updated_at)
           VALUES (?, ?, ?, ?, ?, 'active', 0, ?, ?, '[]', ?, ?)""",
        (partner_id, name, company, email, context,
         next_followup_ts, now, now, now),
    )
    db.commit()
    db.close()
    return partner_id


def get_partner_followups(status: str = "active") -> list[dict]:
    """Return all partner follow-ups with the given status."""
    db = get_db()
    rows = db.execute(
        "SELECT * FROM partner_followups WHERE status = ? ORDER BY next_followup ASC",
        (status,),
    ).fetchall()
    db.close()
    return [dict(r) for r in rows]


def get_partner_followup(partner_id: str) -> dict | None:
    """Return a single partner follow-up by ID."""
    db = get_db()
    row = db.execute(
        "SELECT * FROM partner_followups WHERE id = ?",
        (partner_id,),
    ).fetchone()
    db.close()
    return dict(row) if row else None


def update_partner_followup(partner_id: str, **kwargs: Any) -> None:
    """Update one or more fields on a partner follow-up."""
    _valid = frozenset({
        "name", "company", "email", "context", "status",
        "followup_count", "next_followup", "last_contacted", "notes",
    })
    updates = {k: v for k, v in kwargs.items() if k in _valid}
    if not updates:
        return
    updates["updated_at"] = int(time.time())
    cols = ", ".join(f"{k} = ?" for k in updates)
    vals = list(updates.values()) + [partner_id]
    db = get_db()
    db.execute(f"UPDATE partner_followups SET {cols} WHERE id = ?", vals)
    db.commit()
    db.close()


def get_due_partner_reminders() -> list[dict]:
    """Return all active partner follow-ups whose next_followup <= now."""
    now = int(time.time())
    db = get_db()
    rows = db.execute(
        """SELECT * FROM partner_followups
           WHERE status = 'active' AND next_followup IS NOT NULL AND next_followup <= ?
           ORDER BY next_followup ASC""",
        (now,),
    ).fetchall()
    db.close()
    return [dict(r) for r in rows]


def advance_partner_followup(partner_id: str) -> int | None:
    """Increment followup_count and compute the next follow-up date.

    Uses PARTNER_DEFAULT_SCHEDULE_DAYS for escalating cadence.
    Returns the new next_followup timestamp, or None if max reached.
    """
    from ..constants import PARTNER_DEFAULT_SCHEDULE_DAYS, PARTNER_MAX_AUTO_FOLLOWUPS

    record = get_partner_followup(partner_id)
    if not record:
        return None

    new_count = record["followup_count"] + 1
    now = int(time.time())

    if new_count >= PARTNER_MAX_AUTO_FOLLOWUPS:
        update_partner_followup(
            partner_id,
            followup_count=new_count,
            last_contacted=now,
            status="paused",
        )
        return None

    schedule_idx = min(new_count, len(PARTNER_DEFAULT_SCHEDULE_DAYS) - 1)
    next_days = PARTNER_DEFAULT_SCHEDULE_DAYS[schedule_idx]
    next_ts = now + next_days * 86400

    update_partner_followup(
        partner_id,
        followup_count=new_count,
        last_contacted=now,
        next_followup=next_ts,
    )
    return next_ts


# ──────────────────────────────────────────────
# Profile Change History
# ──────────────────────────────────────────────


def log_profile_change(
    field: str,
    old_value: str | None,
    new_value: str,
    source: str = "manual",
) -> str:
    """Log a LinkedIn profile change. Returns the change ID (8-char uuid)."""
    change_id = str(uuid.uuid4())[:8]
    db = get_db()
    db.execute(
        """INSERT INTO profile_changes (id, field, old_value, new_value, source, status, created_at)
           VALUES (?, ?, ?, ?, ?, 'applied', ?)""",
        (change_id, field, old_value, new_value, source, int(time.time())),
    )
    db.commit()
    db.close()
    return change_id


def get_profile_changes(field: str | None = None, limit: int = 20) -> list[dict]:
    """Return recent profile changes, optionally filtered by field."""
    db = get_db()
    if field:
        rows = db.execute(
            "SELECT * FROM profile_changes WHERE field = ? ORDER BY created_at DESC LIMIT ?",
            (field, limit),
        ).fetchall()
    else:
        rows = db.execute(
            "SELECT * FROM profile_changes ORDER BY created_at DESC LIMIT ?",
            (limit,),
        ).fetchall()
    db.close()
    return [dict(r) for r in rows]


def get_profile_change(change_id: str) -> dict | None:
    """Return a single profile change by ID."""
    db = get_db()
    row = db.execute(
        "SELECT * FROM profile_changes WHERE id = ?",
        (change_id,),
    ).fetchone()
    db.close()
    return dict(row) if row else None


def mark_profile_change_reverted(change_id: str) -> None:
    """Mark a profile change as reverted."""
    db = get_db()
    db.execute(
        "UPDATE profile_changes SET status = 'reverted' WHERE id = ?",
        (change_id,),
    )
    db.commit()
    db.close()


# ──────────────────────────────────────────────
# Prospect Journey Timeline
# ──────────────────────────────────────────────

def get_prospect_timeline(outreach_id: str, days: int = 30) -> list[dict]:
    """Get chronological timeline of all events for an outreach.

    Merges: actions_log, engagements, scheduler_jobs, prospect_daily_plans.
    Returns sorted list of {event_type, action, timestamp, details, source}.
    """
    since = int(time.time()) - (days * 86400)
    db = get_db()

    # 1. Actions log
    actions = db.execute(
        """SELECT action_type, result, details_json, timestamp
           FROM actions_log
           WHERE outreach_id = ? AND timestamp >= ?
           ORDER BY timestamp""",
        (outreach_id, since),
    ).fetchall()

    # 2. Engagements
    engagements = db.execute(
        """SELECT action_type, status, text, post_id, verified_status, created_at
           FROM engagements
           WHERE outreach_id = ? AND created_at >= ?
           ORDER BY created_at""",
        (outreach_id, since),
    ).fetchall()

    # 3. Scheduler jobs
    jobs = db.execute(
        """SELECT job_type, status, scheduled_at, completed_at, duration_ms, error
           FROM scheduler_jobs
           WHERE outreach_id = ? AND scheduled_at >= ?
           ORDER BY scheduled_at""",
        (outreach_id, since),
    ).fetchall()

    # 4. Outreach status history (from outreaches table itself)
    outreach = db.execute(
        """SELECT status, invited_at, accepted_at, first_reply_at, created_at
           FROM outreaches WHERE id = ?""",
        (outreach_id,),
    ).fetchone()

    db.close()

    timeline: list[dict] = []

    # Add actions
    for a in actions:
        details = {}
        if a["details_json"]:
            try:
                details = json.loads(a["details_json"])
            except (json.JSONDecodeError, TypeError):
                pass
        timeline.append({
            "event_type": "action",
            "action": a["action_type"],
            "timestamp": a["timestamp"],
            "details": f"{a['result'] or ''} {details.get('reason', '')}".strip(),
            "source": "actions_log",
        })

    # Add engagements
    for e in engagements:
        detail_parts = [e["action_type"]]
        if e["text"]:
            detail_parts.append(f'"{e["text"][:60]}..."' if len(e["text"] or "") > 60 else f'"{e["text"]}"')
        if e["verified_status"]:
            detail_parts.append(f"[{e['verified_status']}]")
        timeline.append({
            "event_type": "engagement",
            "action": e["action_type"],
            "timestamp": e["created_at"],
            "details": " ".join(detail_parts),
            "source": "engagements",
        })

    # Add jobs
    for j in jobs:
        status = j["status"]
        detail = f"{status}"
        if j["duration_ms"]:
            detail += f" ({j['duration_ms']}ms)"
        if j["error"]:
            detail += f" — {j['error'][:80]}"
        timeline.append({
            "event_type": "job",
            "action": j["job_type"],
            "timestamp": j["completed_at"] or j["scheduled_at"],
            "details": detail,
            "source": "scheduler_jobs",
        })

    # Add outreach milestones
    if outreach:
        o = dict(outreach)
        if o.get("created_at") and o["created_at"] >= since:
            timeline.append({
                "event_type": "milestone",
                "action": "prospect_added",
                "timestamp": o["created_at"],
                "details": f"Status: {o['status']}",
                "source": "outreaches",
            })
        if o.get("invited_at") and o["invited_at"] >= since:
            timeline.append({
                "event_type": "milestone",
                "action": "invited",
                "timestamp": o["invited_at"],
                "details": "Connection invitation sent",
                "source": "outreaches",
            })
        if o.get("accepted_at") and o["accepted_at"] >= since:
            timeline.append({
                "event_type": "milestone",
                "action": "accepted",
                "timestamp": o["accepted_at"],
                "details": "Connection accepted",
                "source": "outreaches",
            })
        if o.get("first_reply_at") and o["first_reply_at"] >= since:
            timeline.append({
                "event_type": "milestone",
                "action": "first_reply",
                "timestamp": o["first_reply_at"],
                "details": "Prospect replied for the first time",
                "source": "outreaches",
            })

    # Sort by timestamp
    timeline.sort(key=lambda x: x["timestamp"] or 0)
    return timeline


# ──────────────────────────────────────────────
# Metric Trend Data (for anomaly detection)
# ──────────────────────────────────────────────

def get_metric_trend_data(days: int = 14) -> dict[str, list[dict]]:
    """Get daily metric values for trend analysis.

    Returns per-day values for: acceptance_rate, reply_rate,
    avg_job_duration_ms, engagement_success_rate.
    """
    from datetime import date, timedelta

    db = get_db()
    result: dict[str, list[dict]] = {
        "acceptance_rate": [],
        "reply_rate": [],
        "avg_job_duration_ms": [],
        "engagement_success_rate": [],
    }

    for offset in range(days):
        d = date.today() - timedelta(days=days - 1 - offset)
        d_str = d.isoformat()
        day_start = int(
            __import__("datetime").datetime.combine(d, __import__("datetime").time.min).timestamp()
        )
        day_end = day_start + 86400

        # Acceptance rate: accepted today / invited in last 7 days
        accepted_today = db.execute(
            "SELECT COUNT(*) as c FROM outreaches WHERE accepted_at >= ? AND accepted_at < ?",
            (day_start, day_end),
        ).fetchone()["c"]
        # Mature invites: sent 7+ days before this day
        mature_cutoff = day_start - (7 * 86400)
        mature_invited = db.execute(
            "SELECT COUNT(*) as c FROM outreaches WHERE invited_at IS NOT NULL AND invited_at < ?",
            (mature_cutoff,),
        ).fetchone()["c"]
        acc_rate = round(accepted_today / mature_invited, 4) if mature_invited else None
        result["acceptance_rate"].append({"date": d_str, "value": acc_rate})

        # Reply rate: first_reply_at set today / connected prospects
        replied_today = db.execute(
            "SELECT COUNT(*) as c FROM outreaches WHERE first_reply_at >= ? AND first_reply_at < ?",
            (day_start, day_end),
        ).fetchone()["c"]
        connected_total = db.execute(
            "SELECT COUNT(*) as c FROM outreaches WHERE accepted_at IS NOT NULL AND accepted_at < ?",
            (day_start,),
        ).fetchone()["c"]
        rep_rate = round(replied_today / connected_total, 4) if connected_total else None
        result["reply_rate"].append({"date": d_str, "value": rep_rate})

        # Avg job duration
        avg_dur = db.execute(
            """SELECT AVG(duration_ms) as avg_ms FROM scheduler_jobs
               WHERE status = 'completed' AND completed_at >= ? AND completed_at < ?
               AND duration_ms IS NOT NULL""",
            (day_start, day_end),
        ).fetchone()["avg_ms"]
        result["avg_job_duration_ms"].append({
            "date": d_str,
            "value": round(avg_dur) if avg_dur else None,
        })

        # Engagement success rate
        total_eng = db.execute(
            "SELECT COUNT(*) as c FROM engagements WHERE created_at >= ? AND created_at < ?",
            (day_start, day_end),
        ).fetchone()["c"]
        verified_eng = db.execute(
            """SELECT COUNT(*) as c FROM engagements
               WHERE created_at >= ? AND created_at < ?
               AND verified_status IN ('verified', 'trust_api')""",
            (day_start, day_end),
        ).fetchone()["c"]
        eng_rate = round(verified_eng / total_eng, 4) if total_eng else None
        result["engagement_success_rate"].append({"date": d_str, "value": eng_rate})

    db.close()
    return result
