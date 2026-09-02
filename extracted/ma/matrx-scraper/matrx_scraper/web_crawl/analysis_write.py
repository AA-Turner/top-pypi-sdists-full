"""The ONE write path for `web.analysis_result` + `web.finding` — shared by
every analysis provider.

Extracted from `analysis.py` (2026-08-09) when the `matrx_ai_premium` /
`matrx_ai_vision` providers arrived: a second provider writing its own inserts
and its own finding reconciliation would have been a second lifecycle, and the
finding register (`at most ONE open finding per (site, subject, item)`) only
holds if every producer reconciles through the same code.

**Provider-agnostic by construction.** Nothing here knows whether a row came
from deterministic rules, a model, or Lighthouse — a provider computes outcomes
and hands them over; these functions own the DB contract:

- `web.analysis_result` is IMMUTABLE (insert-only). `status` pass|warn|fail
  requires `score` 1–100; `n_a`/`error` require NULL — DB CHECK
  `analysis_result_status_score_valid`.
- `severity` comes from the catalogue row's own `severity_map` bands, never
  from a provider's opinion.
- `web.finding` is the mutable register: warn/fail opens-or-refreshes-or-
  REOPENS, pass resolves, everything else (`n_a`/`error`) leaves the register
  untouched — an unanswerable check must never silently resolve a real open
  finding.
- Suppression is user-owned state and is NEVER written here.
- A finding row is the DURABLE identity of `(site, subject, item)`. A condition
  that comes back reopens THAT row (`status='reopened'`), never a fresh one —
  see `reconcile_findings` for why user state makes this load-bearing.
"""

from __future__ import annotations

from datetime import UTC, datetime

from matrx_orm import transaction
from matrx_orm.operations.bulk_update_values import bulk_update_by_pk

from matrx_scraper.db.models_web import (
    AnalysisItem as WebAnalysisItem,
    AnalysisResult as WebAnalysisResult,
    Finding as WebFinding,
)
from matrx_scraper.db.web import WEB_DB_NAME
from matrx_scraper.web_crawl.contracts import AnalysisSummary

_RESULT_INSERT_BATCH = 500
_EPOCH = datetime.min.replace(tzinfo=UTC)


def severity_for(item: WebAnalysisItem, score: int | None) -> str:
    """Map a score onto the catalogue row's own severity bands.

    The item row owns the bands — a provider never invents severity. A scoreless
    outcome (`n_a`/`error`) is `info`: it carries no judgement about the page.
    """
    if score is None:
        return "info"
    bands = ((item.severity_map or {}).get("bands")) or []
    for band in bands:
        try:
            if score <= int(band["max"]):
                return str(band["severity"])
        except (KeyError, TypeError, ValueError):
            continue
    return "info"


async def insert_results(rows: list[dict]) -> list[WebAnalysisResult]:
    """Insert immutable result rows in batches, refusing to under-report."""
    created: list[WebAnalysisResult] = []
    for start in range(0, len(rows), _RESULT_INSERT_BATCH):
        chunk = rows[start : start + _RESULT_INSERT_BATCH]
        async with transaction(WEB_DB_NAME):
            created.extend(await WebAnalysisResult.bulk_create(chunk))
    if len(created) != len(rows):
        raise RuntimeError(
            f"analysis wrote {len(created)} of {len(rows)} results — refusing to "
            "under-report silently"
        )
    return created


async def reconcile_findings(
    *,
    site_id: str,
    organization_id: str,
    computed_at: datetime,
    results: list[tuple[dict, WebAnalysisResult]],
    summary: AnalysisSummary,
) -> None:
    """Open/refresh/reopen a finding per warn/fail result; resolve on pass.

    One live finding per (site, subject, item) — DB-enforced by
    ``finding_open_uniq``. A finding ROW is that triple's durable identity:
    when a resolved condition is detected again, the SAME row comes back as
    ``reopened`` (``resolved_at`` cleared, ``first_detected_at`` preserved),
    never a fresh row.

    Why the row, not a new one: `web.finding` carries USER state — a
    suppression with the reason the user wrote, and a "resolved" they clicked
    to mean "I fixed this". Opening a new row for a recurrence silently threw
    all of it away: the suppression the user recorded stopped applying, the
    noise they cleared came back with a new id, and the register lied about
    how long the condition had really been wrong. Reopening is also the only
    writer of the ``reopened`` status the schema has always allowed and the UI
    has always rendered.

    Suppression itself is user state and is never modified here.
    """

    findings = await WebFinding.filter(site_id=site_id, deleted_at__isnull=True).all()
    open_by_key: dict[tuple[str, str], WebFinding] = {}
    # Latest resolved row per key — the one a recurrence reopens. Older
    # resolved rows for the same key stay as history, untouched.
    resolved_by_key: dict[tuple[str, str], WebFinding] = {}
    for f in findings:
        key = (str(f.subject_id), str(f.item_id))
        if f.status == "resolved":
            prior = resolved_by_key.get(key)
            # `finding_resolution_valid` guarantees resolved_at is set; the
            # fallback is aware because the column is timestamptz and a naive
            # sentinel would raise on comparison rather than sort last.
            if prior is None or (f.resolved_at or _EPOCH) > (prior.resolved_at or _EPOCH):
                resolved_by_key[key] = f
        else:
            # `finding_open_uniq` guarantees at most one non-resolved row here.
            open_by_key[key] = f

    creates: list[dict] = []
    refreshes: list[dict] = []
    reopens: list[dict] = []
    resolves: list[dict] = []
    for row, created in results:
        key = (str(row["subject_id"]), str(row["item_id"]))
        existing = open_by_key.get(key)
        if row["status"] in ("warn", "fail"):
            if existing is None and key in resolved_by_key:
                # It came back. Same row, same history, same suppression.
                reopens.append(
                    {
                        "id": str(resolved_by_key.pop(key).id),
                        "status": "reopened",
                        "resolved_at": None,
                        "severity": row["severity"],
                        "last_result_id": str(created.id),
                        "last_detected_at": computed_at,
                    }
                )
            elif existing is None:
                creates.append(
                    {
                        "organization_id": organization_id,
                        "site_id": site_id,
                        "subject_type": row["subject_type"],
                        "subject_id": row["subject_id"],
                        "page_id": row["page_id"],
                        "item_id": row["item_id"],
                        "item_key": row["item_key"],
                        "category": row["category"],
                        "subcategory": row["subcategory"],
                        "severity": row["severity"],
                        "status": "open",
                        "first_result_id": str(created.id),
                        "last_result_id": str(created.id),
                        "first_detected_at": computed_at,
                        "last_detected_at": computed_at,
                    }
                )
            else:
                refreshes.append(
                    {
                        "id": str(existing.id),
                        "severity": row["severity"],
                        "last_result_id": str(created.id),
                        "last_detected_at": computed_at,
                    }
                )
        elif row["status"] == "pass" and existing is not None:
            resolves.append(
                {
                    "id": str(existing.id),
                    "status": "resolved",
                    "resolved_at": computed_at,
                    "last_result_id": str(created.id),
                }
            )

    if creates:
        async with transaction(WEB_DB_NAME):
            await WebFinding.bulk_create(creates)
        summary.findings_opened += len(creates)
    if refreshes:
        async with transaction(WEB_DB_NAME):
            await bulk_update_by_pk(
                WebFinding,
                refreshes,
                casts={
                    "id": "uuid",
                    "severity": "text",
                    "last_result_id": "uuid",
                    "last_detected_at": "timestamptz",
                },
            )
        summary.findings_refreshed += len(refreshes)
    if reopens:
        async with transaction(WEB_DB_NAME):
            await bulk_update_by_pk(
                WebFinding,
                reopens,
                casts={
                    "id": "uuid",
                    "status": "text",
                    # All-NULL column — asyncpg cannot infer the type without
                    # the hint, and clearing it is what makes the row live
                    # again under `finding_resolution_valid`.
                    "resolved_at": "timestamptz",
                    "severity": "text",
                    "last_result_id": "uuid",
                    "last_detected_at": "timestamptz",
                },
            )
        summary.findings_reopened += len(reopens)
    if resolves:
        async with transaction(WEB_DB_NAME):
            await bulk_update_by_pk(
                WebFinding,
                resolves,
                casts={
                    "id": "uuid",
                    "status": "text",
                    "resolved_at": "timestamptz",
                    "last_result_id": "uuid",
                },
            )
        summary.findings_resolved += len(resolves)


__all__ = ["insert_results", "reconcile_findings", "severity_for"]
