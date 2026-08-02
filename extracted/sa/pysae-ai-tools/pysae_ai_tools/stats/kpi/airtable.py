"""Airtable collector: P1/P2 incident counts from the Customer Service base.

Mapping criticité → priorité (see ``support-vocabulary.md``): 4–5 → P1, 3 → P2.
Date filtering happens client-side (small volume, avoids Airtable formula
date-parsing pitfalls).
"""

from typing import Any

import httpx

from ...env.resolve import try_auto_resolve

BASE_ID = "app79vpJ07qFIOEm1"  # Customer Service
TICKETS_TABLE_ID = "tblHjCvyOcdq0Kw0z"  # Tickets support
CRITICITY_FIELD = "Criticité"
DECLARED_AT_FIELD = "Date déclaration"


def fetch_critical_tickets() -> list[dict[str, Any]]:
    """All tickets with Criticité >= 3, fields limited to criticity + declaration date."""
    api_key = try_auto_resolve("AIRTABLE_API_KEY")
    if not api_key:
        raise RuntimeError("AIRTABLE_API_KEY not resolved — run `pysae-ai-tools env resolve AIRTABLE_API_KEY`")

    records: list[dict[str, Any]] = []
    offset: str | None = None
    with httpx.Client(
        base_url=f"https://api.airtable.com/v0/{BASE_ID}",
        headers={"Authorization": f"Bearer {api_key}"},
        timeout=30,
    ) as airtable:
        while True:
            params = httpx.QueryParams(
                [
                    ("filterByFormula", f"{{{CRITICITY_FIELD}}} >= 3"),
                    ("pageSize", "100"),
                    ("fields[]", CRITICITY_FIELD),
                    ("fields[]", DECLARED_AT_FIELD),
                ]
            )
            if offset:
                params = params.set("offset", offset)
            resp = airtable.get(f"/{TICKETS_TABLE_ID}", params=params)
            resp.raise_for_status()
            payload = resp.json()
            records.extend(payload.get("records", []))
            offset = payload.get("offset")
            if not offset:
                return records


def count_p1_p2(records: list[dict[str, Any]], since: str, until: str) -> tuple[int, int]:
    """(P1, P2) counts among tickets declared in ``[since, until)`` (YYYY-MM-DD bounds)."""
    p1 = p2 = 0
    for record in records:
        fields = record.get("fields", {})
        declared_at = (fields.get(DECLARED_AT_FIELD) or "")[:10]
        criticity = fields.get(CRITICITY_FIELD)
        if not declared_at or criticity is None or not since <= declared_at < until:
            continue
        if criticity >= 4:
            p1 += 1
        elif criticity == 3:
            p2 += 1
    return p1, p2
