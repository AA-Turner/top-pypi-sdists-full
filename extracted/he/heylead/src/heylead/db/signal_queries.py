"""SQLite CRUD helpers for proactive signal-based selling."""

from __future__ import annotations

import json
import time
import uuid
from typing import Any, Optional

from .schema import get_db


# ──────────────────────────────────────────────
# Signals
# ──────────────────────────────────────────────

def save_signal(
    signal_type: str,
    source: str,
    *,
    prospect_id: str | None = None,
    prospect_name: str | None = None,
    prospect_title: str | None = None,
    linkedin_id: str | None = None,
    campaign_id: str | None = None,
    content: str | None = None,
    post_id: str | None = None,
    metadata_json: str | None = None,
    expires_at: int | None = None,
    watchlist_id: str | None = None,
    confidence: float | None = None,
) -> str:
    """Save a new signal. Returns the signal ID."""
    signal_id = uuid.uuid4().hex[:12]
    now = int(time.time())

    # Sanitize FK fields: empty strings violate FOREIGN KEY constraints
    # (PRAGMA foreign_keys=ON). Convert "" → None so SQLite treats as NULL.
    if not prospect_id:
        prospect_id = None
    if not campaign_id:
        campaign_id = None

    # Default expiry if not provided
    if expires_at is None:
        from ..constants import SIGNAL_TTL_DEFAULT
        expires_at = now + SIGNAL_TTL_DEFAULT

    db = get_db()
    if confidence is not None:
        db.execute(
            """INSERT INTO signals
               (id, signal_type, source, prospect_id, prospect_name, prospect_title,
                linkedin_id, campaign_id, content, post_id, metadata_json,
                status, confidence, expires_at, detected_at, watchlist_id)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'new', ?, ?, ?, ?)""",
            (
                signal_id, signal_type, source,
                prospect_id, prospect_name, prospect_title,
                linkedin_id, campaign_id,
                content, post_id, metadata_json,
                confidence, expires_at, now, watchlist_id,
            ),
        )
    else:
        db.execute(
            """INSERT INTO signals
               (id, signal_type, source, prospect_id, prospect_name, prospect_title,
                linkedin_id, campaign_id, content, post_id, metadata_json,
                status, expires_at, detected_at, watchlist_id)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'new', ?, ?, ?)""",
            (
                signal_id, signal_type, source,
                prospect_id, prospect_name, prospect_title,
                linkedin_id, campaign_id,
                content, post_id, metadata_json,
                expires_at, now, watchlist_id,
            ),
        )
    db.commit()
    db.close()
    return signal_id


def get_signal(signal_id: str) -> dict[str, Any] | None:
    """Get a signal by ID."""
    db = get_db()
    row = db.execute("SELECT * FROM signals WHERE id = ?", (signal_id,)).fetchone()
    db.close()
    return dict(row) if row else None


def list_signals(
    *,
    status: str | None = None,
    signal_type: str | None = None,
    linkedin_id: str | None = None,
    campaign_id: str | None = None,
    post_id: str | None = None,
    limit: int = 50,
    offset: int = 0,
    order_by: str = "detected_at DESC",
) -> list[dict[str, Any]]:
    """List signals with optional filters."""
    conditions: list[str] = []
    params: list[Any] = []

    if status:
        conditions.append("status = ?")
        params.append(status)
    if signal_type:
        conditions.append("signal_type = ?")
        params.append(signal_type)
    if linkedin_id:
        conditions.append("linkedin_id = ?")
        params.append(linkedin_id)
    if campaign_id:
        conditions.append("campaign_id = ?")
        params.append(campaign_id)
    if post_id:
        conditions.append("post_id = ?")
        params.append(post_id)

    where = " AND ".join(conditions) if conditions else "1=1"
    # Whitelist order_by to prevent injection
    allowed_orders = {
        "detected_at DESC", "detected_at ASC",
        "signal_score DESC", "signal_score ASC",
        "confidence DESC", "confidence ASC",
    }
    if order_by not in allowed_orders:
        order_by = "detected_at DESC"

    query = f"SELECT * FROM signals WHERE {where} ORDER BY {order_by} LIMIT ? OFFSET ?"
    params.extend([limit, offset])

    db = get_db()
    rows = db.execute(query, params).fetchall()
    db.close()
    return [dict(r) for r in rows]


def list_signals_for_sync(since_ts: int, limit: int = 200) -> list[dict[str, Any]]:
    """List signals detected after *since_ts* for cloud sync.

    Returns up to *limit* signals ordered oldest-first so the backend
    receives them in chronological order.
    """
    db = get_db()
    rows = db.execute(
        "SELECT * FROM signals WHERE detected_at > ? "
        "ORDER BY detected_at ASC LIMIT ?",
        (since_ts, limit),
    ).fetchall()
    db.close()
    return [dict(r) for r in rows]


def update_signal(signal_id: str, **kwargs: Any) -> None:
    """Update signal fields."""
    if not kwargs:
        return
    sets = ", ".join(f"{k} = ?" for k in kwargs)
    vals = list(kwargs.values())
    vals.append(signal_id)

    db = get_db()
    db.execute(f"UPDATE signals SET {sets} WHERE id = ?", vals)
    db.commit()
    db.close()


def batch_signal_exists(
    signal_type: str,
    post_ids: list[str] | None = None,
    linkedin_ids: list[str] | None = None,
    *,
    lookback_seconds: int | None = None,
) -> set[str]:
    """Check which IDs already have signals (batch dedup).

    Returns a set of post_ids or linkedin_ids that already exist.
    Chunks at 400 to stay under SQLite's 999 variable limit.
    """
    ids = post_ids or linkedin_ids
    if not ids:
        return set()

    id_column = "post_id" if post_ids else "linkedin_id"
    existing: set[str] = set()
    db = get_db()

    for i in range(0, len(ids), 400):
        chunk = ids[i : i + 400]
        placeholders = ",".join("?" for _ in chunk)
        conditions = [f"signal_type = ?", f"{id_column} IN ({placeholders})"]
        params: list[Any] = [signal_type] + chunk

        if lookback_seconds:
            cutoff = int(time.time()) - lookback_seconds
            conditions.append("detected_at >= ?")
            params.append(cutoff)

        where = " AND ".join(conditions)
        rows = db.execute(
            f"SELECT {id_column} FROM signals WHERE {where}", params
        ).fetchall()
        existing.update(r[0] for r in rows if r[0])

    db.close()
    return existing


def signal_exists(
    signal_type: str,
    linkedin_id: str | None = None,
    post_id: str | None = None,
    *,
    lookback_seconds: int | None = None,
) -> bool:
    """Check if a signal already exists (for dedup).

    Matches on signal_type + (linkedin_id or post_id).
    Optionally limits check to recent signals within lookback_seconds.
    """
    conditions = ["signal_type = ?"]
    params: list[Any] = [signal_type]

    if linkedin_id:
        conditions.append("linkedin_id = ?")
        params.append(linkedin_id)
    if post_id:
        conditions.append("post_id = ?")
        params.append(post_id)

    if lookback_seconds:
        cutoff = int(time.time()) - lookback_seconds
        conditions.append("detected_at >= ?")
        params.append(cutoff)

    where = " AND ".join(conditions)
    db = get_db()
    row = db.execute(f"SELECT 1 FROM signals WHERE {where} LIMIT 1", params).fetchone()
    db.close()
    return row is not None


def count_signals_by_type(
    *,
    days: int = 7,
    campaign_id: str | None = None,
) -> dict[str, int]:
    """Count signals by type within the given time window."""
    cutoff = int(time.time()) - (days * 86400)
    conditions = ["detected_at >= ?"]
    params: list[Any] = [cutoff]

    if campaign_id:
        conditions.append("campaign_id = ?")
        params.append(campaign_id)

    where = " AND ".join(conditions)
    db = get_db()
    rows = db.execute(
        f"SELECT signal_type, COUNT(*) as cnt FROM signals WHERE {where} GROUP BY signal_type",
        params,
    ).fetchall()
    db.close()
    return {row["signal_type"]: row["cnt"] for row in rows}


def get_signal_funnel_stats(days: int = 7) -> dict[str, Any]:
    """Get signal funnel stats for dashboard."""
    cutoff = int(time.time()) - (days * 86400)

    db = get_db()

    # By status
    status_rows = db.execute(
        "SELECT status, COUNT(*) as cnt FROM signals WHERE detected_at >= ? GROUP BY status",
        (cutoff,),
    ).fetchall()
    by_status = {r["status"]: r["cnt"] for r in status_rows}

    # By type
    type_rows = db.execute(
        "SELECT signal_type, COUNT(*) as cnt FROM signals WHERE detected_at >= ? GROUP BY signal_type",
        (cutoff,),
    ).fetchall()
    by_type = {r["signal_type"]: r["cnt"] for r in type_rows}

    # Top prospects by signal count
    top_rows = db.execute(
        """SELECT linkedin_id, prospect_name, prospect_title, COUNT(*) as cnt,
                  MAX(signal_score) as max_score
           FROM signals
           WHERE detected_at >= ? AND linkedin_id IS NOT NULL
           GROUP BY linkedin_id
           ORDER BY cnt DESC, max_score DESC
           LIMIT 10""",
        (cutoff,),
    ).fetchall()
    top_prospects = [dict(r) for r in top_rows]

    db.close()
    return {
        "by_status": by_status,
        "by_type": by_type,
        "top_prospects": top_prospects,
        "total": sum(by_status.values()),
    }


def expire_old_signals() -> int:
    """Move expired signals to 'expired' status. Returns count expired."""
    now = int(time.time())
    db = get_db()
    cursor = db.execute(
        "UPDATE signals SET status = 'expired' WHERE expires_at <= ? AND status NOT IN ('expired', 'actioned', 'dismissed')",
        (now,),
    )
    count = cursor.rowcount
    db.commit()
    db.close()
    return count


# ──────────────────────────────────────────────
# Signal Watchlists
# ──────────────────────────────────────────────

def save_watchlist(
    name: str,
    watch_type: str,
    keywords: list[str],
    *,
    campaign_id: str | None = None,
) -> str:
    """Create a new watchlist. Returns watchlist ID."""
    wl_id = uuid.uuid4().hex[:12]
    db = get_db()
    db.execute(
        """INSERT INTO signal_watchlists
           (id, name, watch_type, keywords, campaign_id, is_active, created_at)
           VALUES (?, ?, ?, ?, ?, 1, ?)""",
        (wl_id, name, watch_type, json.dumps(keywords), campaign_id, int(time.time())),
    )
    db.commit()
    db.close()
    return wl_id


def list_watchlists(
    *,
    is_active: bool | None = True,
    watch_type: str | None = None,
    campaign_id: str | None = None,
) -> list[dict[str, Any]]:
    """List watchlists with optional filters."""
    conditions: list[str] = []
    params: list[Any] = []

    if is_active is not None:
        conditions.append("is_active = ?")
        params.append(1 if is_active else 0)
    if watch_type:
        conditions.append("watch_type = ?")
        params.append(watch_type)
    if campaign_id:
        conditions.append("campaign_id = ?")
        params.append(campaign_id)

    where = " AND ".join(conditions) if conditions else "1=1"
    db = get_db()
    rows = db.execute(
        f"SELECT * FROM signal_watchlists WHERE {where} ORDER BY created_at DESC",
        params,
    ).fetchall()
    db.close()

    result = []
    for r in rows:
        d = dict(r)
        # Parse keywords JSON
        try:
            d["keywords_list"] = json.loads(d.get("keywords", "[]"))
        except (json.JSONDecodeError, TypeError):
            d["keywords_list"] = []
        result.append(d)
    return result


def get_watchlist(watchlist_id: str) -> dict[str, Any] | None:
    """Get a watchlist by ID."""
    db = get_db()
    row = db.execute("SELECT * FROM signal_watchlists WHERE id = ?", (watchlist_id,)).fetchone()
    db.close()
    if not row:
        return None
    d = dict(row)
    try:
        d["keywords_list"] = json.loads(d.get("keywords", "[]"))
    except (json.JSONDecodeError, TypeError):
        d["keywords_list"] = []
    return d


def update_watchlist(watchlist_id: str, **kwargs: Any) -> None:
    """Update watchlist fields. Handles keywords → JSON serialization."""
    if not kwargs:
        return
    # Serialize keywords list to JSON if provided
    if "keywords" in kwargs and isinstance(kwargs["keywords"], list):
        kwargs["keywords"] = json.dumps(kwargs["keywords"])

    sets = ", ".join(f"{k} = ?" for k in kwargs)
    vals = list(kwargs.values())
    vals.append(watchlist_id)

    db = get_db()
    db.execute(f"UPDATE signal_watchlists SET {sets} WHERE id = ?", vals)
    db.commit()
    db.close()


def delete_watchlist(watchlist_id: str) -> None:
    """Delete a watchlist."""
    db = get_db()
    db.execute("DELETE FROM signal_watchlists WHERE id = ?", (watchlist_id,))
    db.commit()
    db.close()


# ──────────────────────────────────────────────
# Company Posts Tracked (Phase 2 intent expansion)
# ──────────────────────────────────────────────

def save_company_post_tracked(
    watchlist_id: str,
    post_id: str,
    post_text: str | None = None,
) -> str:
    """Save a company page post for engagement tracking."""
    row_id = str(uuid.uuid4())
    now = int(time.time())
    db = get_db()
    db.execute(
        """INSERT OR IGNORE INTO company_posts_tracked
           (id, watchlist_id, post_id, post_text, created_at)
           VALUES (?, ?, ?, ?, ?)""",
        (row_id, watchlist_id, post_id, (post_text or "")[:1000], now),
    )
    db.commit()
    db.close()
    return row_id


def get_tracked_posts_for_watchlist(watchlist_id: str) -> list[dict[str, Any]]:
    """Get all tracked posts for a company watchlist."""
    db = get_db()
    rows = db.execute(
        """SELECT * FROM company_posts_tracked
           WHERE watchlist_id = ?
           ORDER BY created_at DESC""",
        (watchlist_id,),
    ).fetchall()
    db.close()
    return [dict(r) for r in rows]


def update_company_post_tracked(
    post_id: str,
    *,
    known_commenters: list[str] | None = None,
    known_reactors: list[str] | None = None,
) -> None:
    """Update known commenters/reactors for a tracked post."""
    now = int(time.time())
    db = get_db()
    sets = ["last_checked_at = ?"]
    params: list[Any] = [now]
    if known_commenters is not None:
        sets.append("known_commenters = ?")
        params.append(json.dumps(known_commenters))
    if known_reactors is not None:
        sets.append("known_reactors = ?")
        params.append(json.dumps(known_reactors))
    params.append(post_id)
    db.execute(
        f"UPDATE company_posts_tracked SET {', '.join(sets)} WHERE post_id = ?",
        params,
    )
    db.commit()
    db.close()


def get_company_post_by_post_id(post_id: str) -> dict[str, Any] | None:
    """Get a tracked post by its LinkedIn post_id."""
    db = get_db()
    row = db.execute(
        "SELECT * FROM company_posts_tracked WHERE post_id = ?",
        (post_id,),
    ).fetchone()
    db.close()
    return dict(row) if row else None


# ──────────────────────────────────────────────
# Signal Accounts (aggregated scores)
# ──────────────────────────────────────────────

def upsert_signal_account(
    linkedin_id: str,
    prospect_name: str | None = None,
    company: str | None = None,
) -> None:
    """Update or create signal account aggregation."""
    now = int(time.time())
    db = get_db()

    # Count signals and compute top signal type
    stats = db.execute(
        """SELECT COUNT(*) as total, signal_type, MAX(signal_score) as max_score
           FROM signals
           WHERE linkedin_id = ? AND status NOT IN ('expired', 'dismissed')
           GROUP BY signal_type
           ORDER BY max_score DESC""",
        (linkedin_id,),
    ).fetchall()

    total = sum(r["total"] for r in stats)
    top_type = stats[0]["signal_type"] if stats else None
    max_score = max((r["max_score"] for r in stats), default=0.0)

    # Get last signal timestamp
    last_row = db.execute(
        "SELECT MAX(detected_at) as last_at FROM signals WHERE linkedin_id = ?",
        (linkedin_id,),
    ).fetchone()
    last_at = last_row["last_at"] if last_row else None

    db.execute(
        """INSERT INTO signal_accounts
               (linkedin_id, prospect_name, company, total_signals, composite_score,
                top_signal_type, last_signal_at, updated_at)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?)
           ON CONFLICT(linkedin_id) DO UPDATE SET
               prospect_name = COALESCE(excluded.prospect_name, signal_accounts.prospect_name),
               company = COALESCE(excluded.company, signal_accounts.company),
               total_signals = excluded.total_signals,
               composite_score = excluded.composite_score,
               top_signal_type = excluded.top_signal_type,
               last_signal_at = excluded.last_signal_at,
               updated_at = excluded.updated_at""",
        (linkedin_id, prospect_name, company, total, max_score, top_type, last_at, now),
    )
    db.commit()
    db.close()


def list_signal_accounts(
    *,
    min_score: float = 0.0,
    limit: int = 20,
) -> list[dict[str, Any]]:
    """List signal accounts ordered by composite score."""
    db = get_db()
    rows = db.execute(
        """SELECT * FROM signal_accounts
           WHERE composite_score >= ?
           ORDER BY composite_score DESC, total_signals DESC
           LIMIT ?""",
        (min_score, limit),
    ).fetchall()
    db.close()
    return [dict(r) for r in rows]


def get_signal_account(linkedin_id: str) -> dict[str, Any] | None:
    """Get signal account by linkedin_id."""
    db = get_db()
    row = db.execute(
        "SELECT * FROM signal_accounts WHERE linkedin_id = ?",
        (linkedin_id,),
    ).fetchone()
    db.close()
    return dict(row) if row else None


def _update_signal_account_score(
    linkedin_id: str,
    composite_score: float,
    total_signals: int,
    top_signal_type: str,
) -> None:
    """Update signal account with computed composite score.

    Called by signal_scorer.recompute_all_signal_accounts() after
    computing weighted scores with freshness decay.
    """
    now = int(time.time())
    db = get_db()
    db.execute(
        """UPDATE signal_accounts
           SET composite_score = ?, total_signals = ?,
               top_signal_type = ?, updated_at = ?
           WHERE linkedin_id = ?""",
        (composite_score, total_signals, top_signal_type, now, linkedin_id),
    )
    db.commit()
    db.close()


# ──────────────────────────────────────────────
# Contact cross-reference helpers
# ──────────────────────────────────────────────

def get_contact_by_linkedin_id(linkedin_id: str) -> dict[str, Any] | None:
    """Find a contact by LinkedIn provider ID across all campaigns."""
    db = get_db()
    row = db.execute(
        "SELECT * FROM contacts WHERE linkedin_id = ? LIMIT 1",
        (linkedin_id,),
    ).fetchone()
    db.close()
    return dict(row) if row else None


def get_contact_by_provider_id(provider_id: str) -> dict[str, Any] | None:
    """Find a contact by LinkedIn provider_id stored in profile_json.

    contacts.linkedin_id stores public_id (slug format like 'john-doe-123')
    but Unipile messages return provider_id (ACoAAA format). This function
    searches the profile_json blob for the provider_id to bridge the gap.
    """
    if not provider_id:
        return None
    db = get_db()
    row = db.execute(
        "SELECT * FROM contacts WHERE json_extract(profile_json, '$.provider_id') = ? LIMIT 1",
        (provider_id,),
    ).fetchone()
    db.close()
    return dict(row) if row else None


def batch_get_contacts_by_linkedin_ids(
    linkedin_ids: list[str],
) -> dict[str, dict[str, Any]]:
    """Find contacts by LinkedIn IDs in a single query (batch version).

    Returns a dict mapping linkedin_id → contact row.
    """
    if not linkedin_ids:
        return {}

    result: dict[str, dict[str, Any]] = {}
    db = get_db()

    for i in range(0, len(linkedin_ids), 400):
        chunk = linkedin_ids[i : i + 400]
        placeholders = ",".join("?" for _ in chunk)
        rows = db.execute(
            f"SELECT * FROM contacts WHERE linkedin_id IN ({placeholders})",
            chunk,
        ).fetchall()
        for row in rows:
            r = dict(row)
            lid = r.get("linkedin_id", "")
            if lid and lid not in result:
                result[lid] = r

    db.close()
    return result


def get_contact_by_name_company(name: str, company: str) -> dict[str, Any] | None:
    """Find a contact by case-insensitive name + company match.

    Falls back dedup for inbound signals when linkedin_id doesn't match.
    Returns the most recent match, or None.
    """
    if not name or not company:
        return None
    db = get_db()
    row = db.execute(
        """SELECT * FROM contacts
           WHERE LOWER(name) = LOWER(?) AND LOWER(company) = LOWER(?)
           ORDER BY created_at DESC LIMIT 1""",
        (name.strip(), company.strip()),
    ).fetchone()
    db.close()
    return dict(row) if row else None


def get_signal_performance(campaign_id: str = "") -> dict[str, Any]:
    """Get signal-triggered outreach performance vs cold outreach.

    Compares outreaches with signal_id (signal-triggered) against those
    without (cold). Returns acceptance rates, reply rates, and conversion.

    Args:
        campaign_id: Optional campaign filter. Analyzes all if empty.

    Returns:
        {
            "signal": {"total", "invited", "connected", "replied", "won", "acceptance_rate", "reply_rate"},
            "cold": {"total", "invited", "connected", "replied", "won", "acceptance_rate", "reply_rate"},
            "signal_lift": {"acceptance", "reply"},  # % improvement
            "by_signal_type": {type: {"total", "connected", "replied"}, ...},
        }
    """
    db = get_db()

    # Build WHERE clause
    where = ""
    params: list[Any] = []
    if campaign_id:
        where = " AND o.campaign_id = ?"
        params.append(campaign_id)

    # Signal-triggered outreaches
    signal_row = db.execute(
        f"""SELECT
            COUNT(*) as total,
            SUM(CASE WHEN o.status NOT IN ('pending', 'review_pending') THEN 1 ELSE 0 END) as invited,
            SUM(CASE WHEN o.status IN ('connected', 'messaged', 'replied', 'hot_lead', 'closed_happy', 'closed_unhappy', 'reverse_pitch', 'opted_out') THEN 1 ELSE 0 END) as connected,
            SUM(CASE WHEN o.status IN ('replied', 'hot_lead', 'closed_happy', 'closed_unhappy', 'reverse_pitch', 'opted_out') THEN 1 ELSE 0 END) as replied,
            SUM(CASE WHEN o.status = 'closed_happy' THEN 1 ELSE 0 END) as won
        FROM outreaches o
        WHERE o.signal_id IS NOT NULL{where}""",
        params,
    ).fetchone()

    # Cold outreaches
    cold_row = db.execute(
        f"""SELECT
            COUNT(*) as total,
            SUM(CASE WHEN o.status NOT IN ('pending', 'review_pending') THEN 1 ELSE 0 END) as invited,
            SUM(CASE WHEN o.status IN ('connected', 'messaged', 'replied', 'hot_lead', 'closed_happy', 'closed_unhappy', 'reverse_pitch', 'opted_out') THEN 1 ELSE 0 END) as connected,
            SUM(CASE WHEN o.status IN ('replied', 'hot_lead', 'closed_happy', 'closed_unhappy', 'reverse_pitch', 'opted_out') THEN 1 ELSE 0 END) as replied,
            SUM(CASE WHEN o.status = 'closed_happy' THEN 1 ELSE 0 END) as won
        FROM outreaches o
        WHERE o.signal_id IS NULL{where}""",
        params,
    ).fetchone()

    def _build_stats(row: Any) -> dict[str, Any]:
        total = row["total"] or 0
        invited = row["invited"] or 0
        connected = row["connected"] or 0
        replied = row["replied"] or 0
        won = row["won"] or 0
        return {
            "total": total,
            "invited": invited,
            "connected": connected,
            "replied": replied,
            "won": won,
            "acceptance_rate": connected / invited if invited > 0 else 0,
            "reply_rate": replied / connected if connected > 0 else 0,
        }

    signal_stats = _build_stats(signal_row)
    cold_stats = _build_stats(cold_row)

    # Calculate signal lift
    lift: dict[str, float] = {}
    if cold_stats["acceptance_rate"] > 0:
        lift["acceptance"] = (
            (signal_stats["acceptance_rate"] - cold_stats["acceptance_rate"])
            / cold_stats["acceptance_rate"]
        )
    if cold_stats["reply_rate"] > 0:
        lift["reply"] = (
            (signal_stats["reply_rate"] - cold_stats["reply_rate"])
            / cold_stats["reply_rate"]
        )

    # Breakdown by signal type
    by_type_rows = db.execute(
        f"""SELECT
            s.signal_type,
            COUNT(*) as total,
            SUM(CASE WHEN o.status IN ('connected', 'messaged', 'replied', 'hot_lead', 'closed_happy', 'closed_unhappy', 'reverse_pitch', 'opted_out') THEN 1 ELSE 0 END) as connected,
            SUM(CASE WHEN o.status IN ('replied', 'hot_lead', 'closed_happy', 'closed_unhappy', 'reverse_pitch', 'opted_out') THEN 1 ELSE 0 END) as replied,
            SUM(CASE WHEN o.status = 'closed_happy' THEN 1 ELSE 0 END) as won
        FROM outreaches o
        JOIN signals s ON o.signal_id = s.id
        WHERE o.signal_id IS NOT NULL{where}
        GROUP BY s.signal_type
        ORDER BY total DESC""",
        params,
    ).fetchall()

    by_type = {}
    for row in by_type_rows:
        by_type[row["signal_type"]] = {
            "total": row["total"] or 0,
            "connected": row["connected"] or 0,
            "replied": row["replied"] or 0,
            "won": row["won"] or 0,
        }

    db.close()

    return {
        "signal": signal_stats,
        "cold": cold_stats,
        "signal_lift": lift,
        "by_signal_type": by_type,
    }


def get_signal_to_conversion_funnel(
    days: int = 30,
    campaign_id: str = "",
) -> dict[str, Any]:
    """Get full signal-to-conversion funnel with per-signal-type breakdown.

    Tracks the journey: signal detected → classified → actioned →
    outreach created → invited → connected → replied → won.

    Returns:
        {
            "total_signals": int,
            "classified": int,
            "actioned": int,
            "outreaches_created": int,
            "funnel": {  # overall outreach funnel for signal-triggered
                "invited": int, "connected": int, "replied": int,
                "hot_leads": int, "won": int, "lost": int,
            },
            "by_type": {  # per signal type
                "keyword_mention": {
                    "signals": int, "actioned": int, "outreaches": int,
                    "connected": int, "replied": int, "won": int,
                    "activation_rate": float, "conversion_rate": float,
                },
                ...
            },
            "by_action": {  # count of each action_taken
                "outreach_created": int, "campaign_added": int,
                "priority_boosted": int, "below_threshold": int,
            },
            "avg_signal_to_outreach_hours": float | None,
        }
    """
    db = get_db()
    cutoff = int(time.time()) - (days * 86400)

    # Build WHERE
    sig_where = "s.detected_at >= ?"
    sig_params: list[Any] = [cutoff]
    out_where = "o.signal_id IS NOT NULL"
    out_params: list[Any] = []

    if campaign_id:
        sig_where += " AND s.campaign_id = ?"
        sig_params.append(campaign_id)
        out_where += " AND o.campaign_id = ?"
        out_params.append(campaign_id)

    # Signal pipeline stats
    pipeline_row = db.execute(
        f"""SELECT
            COUNT(*) as total,
            SUM(CASE WHEN status IN ('classified', 'actioned') THEN 1 ELSE 0 END) as classified,
            SUM(CASE WHEN status = 'actioned' THEN 1 ELSE 0 END) as actioned
        FROM signals s
        WHERE {sig_where}""",
        sig_params,
    ).fetchone()

    total_signals = (pipeline_row["total"] or 0) if pipeline_row else 0
    classified = (pipeline_row["classified"] or 0) if pipeline_row else 0
    actioned = (pipeline_row["actioned"] or 0) if pipeline_row else 0

    # Action breakdown
    action_rows = db.execute(
        f"""SELECT action_taken, COUNT(*) as cnt
        FROM signals s
        WHERE {sig_where} AND action_taken IS NOT NULL
        GROUP BY action_taken""",
        sig_params,
    ).fetchall()
    by_action = {r["action_taken"]: r["cnt"] for r in action_rows}

    # Outreach funnel for signal-triggered outreaches
    funnel_row = db.execute(
        f"""SELECT
            COUNT(*) as total,
            SUM(CASE WHEN o.status NOT IN ('pending', 'review_pending') THEN 1 ELSE 0 END) as invited,
            SUM(CASE WHEN o.status IN ('connected', 'messaged', 'replied', 'hot_lead', 'closed_happy', 'closed_unhappy', 'reverse_pitch', 'opted_out') THEN 1 ELSE 0 END) as connected,
            SUM(CASE WHEN o.status IN ('replied', 'hot_lead', 'closed_happy', 'closed_unhappy', 'reverse_pitch', 'opted_out') THEN 1 ELSE 0 END) as replied,
            SUM(CASE WHEN o.status = 'hot_lead' THEN 1 ELSE 0 END) as hot_leads,
            SUM(CASE WHEN o.status = 'closed_happy' THEN 1 ELSE 0 END) as won,
            SUM(CASE WHEN o.status = 'closed_unhappy' THEN 1 ELSE 0 END) as lost
        FROM outreaches o
        WHERE {out_where}""",
        out_params,
    ).fetchone()

    funnel = {
        "invited": (funnel_row["invited"] or 0) if funnel_row else 0,
        "connected": (funnel_row["connected"] or 0) if funnel_row else 0,
        "replied": (funnel_row["replied"] or 0) if funnel_row else 0,
        "hot_leads": (funnel_row["hot_leads"] or 0) if funnel_row else 0,
        "won": (funnel_row["won"] or 0) if funnel_row else 0,
        "lost": (funnel_row["lost"] or 0) if funnel_row else 0,
    }
    outreaches_total = (funnel_row["total"] or 0) if funnel_row else 0

    # Per-signal-type funnel (join signals → outreaches)
    type_rows = db.execute(
        f"""SELECT
            s.signal_type,
            COUNT(DISTINCT s.id) as signals,
            SUM(CASE WHEN s.status = 'actioned' THEN 1 ELSE 0 END) as actioned_signals,
            COUNT(DISTINCT o.id) as outreaches,
            SUM(CASE WHEN o.status IN ('connected', 'messaged', 'replied', 'hot_lead', 'closed_happy', 'closed_unhappy', 'reverse_pitch', 'opted_out') THEN 1 ELSE 0 END) as connected,
            SUM(CASE WHEN o.status IN ('replied', 'hot_lead', 'closed_happy', 'closed_unhappy', 'reverse_pitch', 'opted_out') THEN 1 ELSE 0 END) as replied,
            SUM(CASE WHEN o.status = 'closed_happy' THEN 1 ELSE 0 END) as won
        FROM signals s
        LEFT JOIN outreaches o ON o.signal_id = s.id
        WHERE {sig_where}
        GROUP BY s.signal_type
        ORDER BY signals DESC""",
        sig_params,
    ).fetchall()

    by_type: dict[str, dict[str, Any]] = {}
    for row in type_rows:
        sig_type = row["signal_type"]
        signals_count = row["signals"] or 0
        outreaches_count = row["outreaches"] or 0
        connected_count = row["connected"] or 0
        replied_count = row["replied"] or 0
        won_count = row["won"] or 0

        by_type[sig_type] = {
            "signals": signals_count,
            "actioned": row["actioned_signals"] or 0,
            "outreaches": outreaches_count,
            "connected": connected_count,
            "replied": replied_count,
            "won": won_count,
            "activation_rate": outreaches_count / signals_count if signals_count > 0 else 0,
            "conversion_rate": won_count / outreaches_count if outreaches_count > 0 else 0,
        }

    # Average time from signal detection to outreach creation
    avg_time_row = db.execute(
        f"""SELECT AVG(o.created_at - s.detected_at) as avg_seconds
        FROM outreaches o
        JOIN signals s ON o.signal_id = s.id
        WHERE {out_where} AND o.created_at > s.detected_at""",
        out_params,
    ).fetchone()

    avg_hours = None
    if avg_time_row and avg_time_row["avg_seconds"]:
        avg_hours = avg_time_row["avg_seconds"] / 3600

    db.close()

    return {
        "total_signals": total_signals,
        "classified": classified,
        "actioned": actioned,
        "outreaches_created": outreaches_total,
        "funnel": funnel,
        "by_type": by_type,
        "by_action": by_action,
        "avg_signal_to_outreach_hours": avg_hours,
    }


# ──────────────────────────────────────────────
# Intent Events (compound intent from stacked signals)
# ──────────────────────────────────────────────

def save_intent_event(
    linkedin_id: str,
    event_type: str,
    signal_ids: list[str],
    signal_types: list[str],
    composite_score: float,
    *,
    company: str | None = None,
    expires_at: int | None = None,
) -> str:
    """Save a compound intent event. Returns event ID."""
    event_id = uuid.uuid4().hex[:12]
    now = int(time.time())

    if expires_at is None:
        expires_at = now + 14 * 86400  # Default 14-day expiry

    db = get_db()
    db.execute(
        """INSERT INTO intent_events
           (id, linkedin_id, company, event_type, signal_ids, signal_types,
            composite_score, detected_at, expires_at)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            event_id, linkedin_id, company, event_type,
            json.dumps(signal_ids), json.dumps(signal_types),
            composite_score, now, expires_at,
        ),
    )
    db.commit()
    db.close()
    return event_id


def list_intent_events(
    *,
    linkedin_id: str | None = None,
    event_type: str | None = None,
    active_only: bool = True,
    limit: int = 50,
) -> list[dict[str, Any]]:
    """List intent events with optional filters."""
    conditions: list[str] = []
    params: list[Any] = []
    now = int(time.time())

    if linkedin_id:
        conditions.append("linkedin_id = ?")
        params.append(linkedin_id)
    if event_type:
        conditions.append("event_type = ?")
        params.append(event_type)
    if active_only:
        conditions.append("expires_at > ?")
        params.append(now)

    where = " AND ".join(conditions) if conditions else "1=1"
    db = get_db()
    rows = db.execute(
        f"""SELECT * FROM intent_events
            WHERE {where}
            ORDER BY composite_score DESC, detected_at DESC
            LIMIT ?""",
        params + [limit],
    ).fetchall()
    db.close()

    result = []
    for r in rows:
        d = dict(r)
        try:
            d["signal_ids_list"] = json.loads(d.get("signal_ids", "[]"))
        except (json.JSONDecodeError, TypeError):
            d["signal_ids_list"] = []
        try:
            d["signal_types_list"] = json.loads(d.get("signal_types", "[]"))
        except (json.JSONDecodeError, TypeError):
            d["signal_types_list"] = []
        result.append(d)
    return result


def intent_event_exists(
    linkedin_id: str,
    event_type: str,
    *,
    lookback_seconds: int = 14 * 86400,
) -> bool:
    """Check if a compound intent event already exists (for dedup)."""
    cutoff = int(time.time()) - lookback_seconds
    db = get_db()
    row = db.execute(
        """SELECT 1 FROM intent_events
           WHERE linkedin_id = ? AND event_type = ? AND detected_at >= ?
           LIMIT 1""",
        (linkedin_id, event_type, cutoff),
    ).fetchone()
    db.close()
    return row is not None


def get_intent_event_stats(days: int = 30) -> dict[str, Any]:
    """Get intent event stats for dashboard."""
    cutoff = int(time.time()) - (days * 86400)
    db = get_db()

    # By type
    type_rows = db.execute(
        """SELECT event_type, COUNT(*) as cnt, AVG(composite_score) as avg_score
           FROM intent_events
           WHERE detected_at >= ?
           GROUP BY event_type
           ORDER BY cnt DESC""",
        (cutoff,),
    ).fetchall()

    by_type = {}
    total = 0
    for r in type_rows:
        by_type[r["event_type"]] = {
            "count": r["cnt"],
            "avg_score": r["avg_score"] or 0,
        }
        total += r["cnt"]

    # By action
    action_rows = db.execute(
        """SELECT action_taken, COUNT(*) as cnt
           FROM intent_events
           WHERE detected_at >= ? AND action_taken IS NOT NULL
           GROUP BY action_taken""",
        (cutoff,),
    ).fetchall()
    by_action = {r["action_taken"]: r["cnt"] for r in action_rows}

    db.close()
    return {
        "total": total,
        "by_type": by_type,
        "by_action": by_action,
    }


def update_intent_event(event_id: str, **kwargs: Any) -> None:
    """Update intent event fields."""
    if not kwargs:
        return
    sets = ", ".join(f"{k} = ?" for k in kwargs)
    vals = list(kwargs.values())
    vals.append(event_id)
    db = get_db()
    db.execute(f"UPDATE intent_events SET {sets} WHERE id = ?", vals)
    db.commit()
    db.close()


# ──────────────────────────────────────────────
# Signal linker queries (retroactive matching)
# ──────────────────────────────────────────────

def find_homeless_signals(limit: int = 200) -> list[dict[str, Any]]:
    """Find non-expired signals that had no matching campaign.

    These are signals that were classified and activated, but
    ``_match_best_campaign()`` returned no suitable campaign at the time.
    They deserve a second chance whenever a new campaign is created.

    Returns list of full signal dicts, ordered by signal_score DESC.
    """
    now = int(time.time())
    db = get_db()
    rows = db.execute(
        """SELECT * FROM signals
           WHERE status = 'actioned'
             AND action_taken IN ('no_matching_campaign', 'below_threshold')
             AND expires_at > ?
           ORDER BY signal_score DESC, detected_at DESC
           LIMIT ?""",
        (now, limit),
    ).fetchall()
    db.close()
    return [dict(r) for r in rows]


def find_orphan_signals_with_contacts(limit: int = 200) -> list[dict[str, Any]]:
    """Find orphan signals (prospect_id IS NULL) whose linkedin_id matches a contact.

    Used by the periodic backfill job to link signals that were
    detected before the contact was added to any campaign.

    Returns list of dicts with signal and contact info.
    """
    now = int(time.time())
    db = get_db()
    rows = db.execute(
        """SELECT s.id as signal_id, s.linkedin_id, s.status as signal_status,
                  s.signal_score, s.signal_type, s.content, s.intent,
                  s.confidence, s.metadata_json,
                  c.id as contact_id, c.campaign_id as contact_campaign_id
           FROM signals s
           JOIN contacts c ON s.linkedin_id = c.linkedin_id
           WHERE s.prospect_id IS NULL
             AND s.status NOT IN ('expired', 'dismissed')
             AND s.expires_at > ?
           LIMIT ?""",
        (now, limit),
    ).fetchall()
    db.close()
    return [dict(r) for r in rows]


def bulk_link_signals_to_contact(
    signal_ids: list[str],
    contact_id: str,
    campaign_id: str,
) -> int:
    """Link multiple orphan signals to a contact. Returns count updated."""
    if not signal_ids:
        return 0
    placeholders = ",".join("?" for _ in signal_ids)
    db = get_db()
    cursor = db.execute(
        f"""UPDATE signals
            SET prospect_id = ?, campaign_id = COALESCE(campaign_id, ?)
            WHERE id IN ({placeholders})
              AND prospect_id IS NULL""",
        [contact_id, campaign_id] + signal_ids,
    )
    count = cursor.rowcount
    db.commit()
    db.close()
    return count


def find_signals_matching_icp_text(
    icp_keywords: set[str],
    *,
    exclude_campaign_id: str = "",
    limit: int = 200,
) -> list[dict[str, Any]]:
    """Find non-expired signals whose content matches ICP keywords.

    Used during campaign creation to retroactively scan the signal pool
    for hot leads that match the new campaign's ICP.

    Args:
        icp_keywords: Set of lowercase keywords from the ICP.
        exclude_campaign_id: Skip signals already linked to this campaign.
        limit: Max signals to return.

    Returns:
        List of signal dicts, ordered by signal_score DESC.
    """
    now = int(time.time())
    db = get_db()

    # Get candidate signals: classified or homeless, non-expired
    conditions = [
        "expires_at > ?",
        "(status = 'classified' OR (status = 'actioned' AND action_taken IN ('no_matching_campaign', 'below_threshold')))",
    ]
    params: list[Any] = [now]

    if exclude_campaign_id:
        conditions.append("(campaign_id IS NULL OR campaign_id != ?)")
        params.append(exclude_campaign_id)

    where = " AND ".join(conditions)
    rows = db.execute(
        f"""SELECT * FROM signals
            WHERE {where}
            ORDER BY signal_score DESC, detected_at DESC
            LIMIT ?""",
        params + [limit],
    ).fetchall()
    db.close()

    # Filter in Python for ICP keyword overlap (flexible text matching)
    matched: list[dict[str, Any]] = []
    for row in rows:
        d = dict(row)
        content = (d.get("content") or "").lower()
        title = (d.get("prospect_title") or "").lower()
        meta_raw = d.get("metadata_json") or ""
        try:
            meta = json.loads(meta_raw) if meta_raw else {}
        except (json.JSONDecodeError, TypeError):
            meta = {}
        keyword = (meta.get("keyword") or "").lower()
        match_text = f"{content} {title} {keyword}"

        hits = sum(1 for kw in icp_keywords if len(kw) >= 3 and kw in match_text)
        if icp_keywords and hits / len(icp_keywords) >= 0.2:
            d["_icp_overlap"] = hits / len(icp_keywords)
            matched.append(d)

    # Sort by overlap * signal_score
    matched.sort(
        key=lambda s: (s.get("_icp_overlap", 0) * (s.get("signal_score") or 0.1)),
        reverse=True,
    )
    return matched


# ──────────────────────────────────────────────
# Signal Optimization CRUD
# ──────────────────────────────────────────────

def get_weight_overrides() -> dict[str, float]:
    """Return all active weight overrides as {signal_type: weight}."""
    db = get_db()
    rows = db.execute("SELECT signal_type, weight FROM signal_weight_overrides").fetchall()
    db.close()
    return {r["signal_type"]: r["weight"] for r in rows}


def upsert_weight_override(
    signal_type: str, weight: float, previous_weight: float,
    source: str = "auto", applied_by: str = "optimizer",
) -> None:
    now = int(time.time())
    db = get_db()
    db.execute(
        """INSERT INTO signal_weight_overrides
           (signal_type, weight, previous_weight, source, applied_at, applied_by)
           VALUES (?, ?, ?, ?, ?, ?)
           ON CONFLICT(signal_type) DO UPDATE SET
             previous_weight = excluded.previous_weight,
             weight = excluded.weight, source = excluded.source,
             applied_at = excluded.applied_at, applied_by = excluded.applied_by""",
        (signal_type, weight, previous_weight, source, now, applied_by),
    )
    db.commit()
    db.close()


def delete_weight_override(signal_type: str) -> bool:
    db = get_db()
    cur = db.execute("DELETE FROM signal_weight_overrides WHERE signal_type = ?", (signal_type,))
    db.commit()
    db.close()
    return cur.rowcount > 0


def get_threshold_overrides() -> dict[str, float]:
    """Return all active threshold overrides as {threshold_name: value}."""
    db = get_db()
    rows = db.execute("SELECT threshold_name, value FROM signal_threshold_overrides").fetchall()
    db.close()
    return {r["threshold_name"]: r["value"] for r in rows}


def upsert_threshold_override(
    threshold_name: str, value: float, previous_value: float,
    source: str = "auto", applied_by: str = "optimizer",
) -> None:
    now = int(time.time())
    db = get_db()
    db.execute(
        """INSERT INTO signal_threshold_overrides
           (threshold_name, value, previous_value, source, applied_at, applied_by)
           VALUES (?, ?, ?, ?, ?, ?)
           ON CONFLICT(threshold_name) DO UPDATE SET
             previous_value = excluded.previous_value,
             value = excluded.value, source = excluded.source,
             applied_at = excluded.applied_at, applied_by = excluded.applied_by""",
        (threshold_name, value, previous_value, source, now, applied_by),
    )
    db.commit()
    db.close()


def delete_threshold_override(threshold_name: str) -> bool:
    db = get_db()
    cur = db.execute("DELETE FROM signal_threshold_overrides WHERE threshold_name = ?", (threshold_name,))
    db.commit()
    db.close()
    return cur.rowcount > 0


def save_optimization_history(
    optimization_type: str, target: str, before_value: str, after_value: str,
    reason: str = "", data_points: int = 0, confidence: float = 0.0,
    status: str = "applied",
) -> str:
    entry_id = uuid.uuid4().hex[:12]
    now = int(time.time())
    db = get_db()
    db.execute(
        """INSERT INTO optimization_history
           (id, optimization_type, target, before_value, after_value,
            reason, data_points, confidence, status, applied_at)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (entry_id, optimization_type, target, before_value, after_value,
         reason, data_points, confidence, status, now),
    )
    db.commit()
    db.close()
    return entry_id


def list_optimization_history(
    optimization_type: str = "", limit: int = 30,
) -> list[dict[str, Any]]:
    db = get_db()
    if optimization_type:
        rows = db.execute(
            "SELECT * FROM optimization_history WHERE optimization_type = ? ORDER BY applied_at DESC LIMIT ?",
            (optimization_type, limit),
        ).fetchall()
    else:
        rows = db.execute(
            "SELECT * FROM optimization_history ORDER BY applied_at DESC LIMIT ?",
            (limit,),
        ).fetchall()
    db.close()
    return [dict(r) for r in rows]


def rollback_optimization(entry_id: str, rolled_back_by: str = "user") -> dict[str, Any] | None:
    """Mark an optimization entry as rolled back. Returns the entry or None."""
    now = int(time.time())
    db = get_db()
    row = db.execute("SELECT * FROM optimization_history WHERE id = ?", (entry_id,)).fetchone()
    if not row:
        db.close()
        return None
    db.execute(
        "UPDATE optimization_history SET status = 'rolled_back', rolled_back_at = ?, rolled_back_by = ? WHERE id = ?",
        (now, rolled_back_by, entry_id),
    )
    db.commit()
    db.close()
    return dict(row)


def get_daily_signal_search_count(search_type: str = "keyword") -> int:
    """Count how many signal searches we've done today (for rate limiting)."""
    today_start = int(time.time()) - (int(time.time()) % 86400)  # Midnight UTC
    db = get_db()
    row = db.execute(
        """SELECT COUNT(*) as cnt FROM signals
           WHERE source = ? AND detected_at >= ?""",
        (f"{search_type}_search", today_start),
    ).fetchone()
    db.close()
    return row["cnt"] if row else 0
