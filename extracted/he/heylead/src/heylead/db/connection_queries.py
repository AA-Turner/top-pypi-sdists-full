"""Query helpers for the local connections table.

Used by the ``my_connections`` contacts action to search 1st-degree
LinkedIn connections that have been synced locally via connection_sync.
All functions are **synchronous** and must be called via ``run_db()``.
"""

from __future__ import annotations

import time
from typing import Any

from .schema import get_db


def search_my_connections(
    query: str,
    account_id: str,
    limit: int = 25,
) -> list[dict[str, Any]]:
    """Full-text LIKE search across name, headline, company, location.

    Splits query into keywords and matches connections containing ANY keyword.
    Results are ranked by number of keyword hits and field weight:
    name match (4) > headline (3) > company (2) > location (1).
    """
    db = get_db()
    try:
        keywords = [kw.strip() for kw in query.split() if kw.strip()]
        if not keywords:
            return []

        # Build per-keyword match clauses
        where_parts: list[str] = []
        score_parts: list[str] = []
        params: list[str] = []

        for _kw in keywords:
            pat = f"%{_kw}%"
            where_parts.append(
                "(LOWER(name) LIKE LOWER(?) OR LOWER(headline) LIKE LOWER(?)"
                " OR LOWER(company) LIKE LOWER(?) OR LOWER(location) LIKE LOWER(?))"
            )
            params.extend([pat, pat, pat, pat])
            score_parts.append(
                "(CASE WHEN LOWER(name) LIKE LOWER(?) THEN 4 ELSE 0 END"
                " + CASE WHEN LOWER(headline) LIKE LOWER(?) THEN 3 ELSE 0 END"
                " + CASE WHEN LOWER(company) LIKE LOWER(?) THEN 2 ELSE 0 END"
                " + CASE WHEN LOWER(location) LIKE LOWER(?) THEN 1 ELSE 0 END)"
            )
            params.extend([pat, pat, pat, pat])

        where_clause = " OR ".join(where_parts)
        score_expr = " + ".join(score_parts)
        # Params order: where_params (account_id inserted), then score_params via subquery
        where_params = params[: len(keywords) * 4]
        score_params = params[len(keywords) * 4 :]

        sql = f"""SELECT provider_id, public_id, name, headline,
                         company, location, profile_url, synced_at,
                         ({score_expr}) AS relevance
                  FROM connections
                  WHERE account_id = ? AND ({where_clause})
                  ORDER BY relevance DESC, name ASC
                  LIMIT ?"""
        all_params = score_params + [account_id] + where_params + [limit]

        rows = db.execute(sql, all_params).fetchall()
        return [dict(r) for r in rows]
    finally:
        db.close()


def list_all_connections(
    account_id: str,
    limit: int = 50,
    offset: int = 0,
) -> list[dict[str, Any]]:
    """List all locally-synced connections ordered by name."""
    db = get_db()
    try:
        rows = db.execute(
            """SELECT provider_id, public_id, name, headline,
                      company, location, profile_url, synced_at
               FROM connections
               WHERE account_id = ?
               ORDER BY name ASC
               LIMIT ? OFFSET ?""",
            (account_id, limit, offset),
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        db.close()


def get_connection_sync_status(account_id: str) -> dict[str, Any]:
    """Return sync status: count, last_synced timestamp, and age in seconds."""
    db = get_db()
    try:
        row = db.execute(
            "SELECT COUNT(*) AS cnt, MAX(synced_at) AS last_synced FROM connections WHERE account_id = ?",
            (account_id,),
        ).fetchone()
        count = row["cnt"] if row else 0
        last_synced = row["last_synced"] if row else None
        age = int(time.time()) - last_synced if last_synced else None
        return {
            "count": count,
            "last_synced": last_synced,
            "age_seconds": age,
            "synced": count > 0,
        }
    finally:
        db.close()
