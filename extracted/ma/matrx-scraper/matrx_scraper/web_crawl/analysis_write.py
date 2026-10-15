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
  REOPENS, pass resolves, `n_a` CLOSES AS UNVERIFIED (resolved, with the
  check's own reason stored in ``metadata.unverified``), `error` leaves it
  untouched. An unanswerable check never resolves a finding silently — but it
  never keeps one open either: on 2026-10-14, 113 "page has no title" findings
  stood open on pages whose titles were fine, because the page later became
  un-judgeable and nothing could ever close them. A later warn/fail reopens
  the same row.
- Suppression is user-owned state and is NEVER written here.
- A finding row is the DURABLE identity of `(site, subject, item)`. A condition
  that comes back reopens THAT row (`status='reopened'`), never a fresh one —
  see `reconcile_findings` for why user state makes this load-bearing.
"""

from __future__ import annotations

from collections import defaultdict

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


SEVERITY_ORDER = ("info", "low", "med", "high", "critical")


def _step(severity: str, by: int) -> str:
    index = SEVERITY_ORDER.index(severity) if severity in SEVERITY_ORDER else 0
    return SEVERITY_ORDER[max(0, min(len(SEVERITY_ORDER) - 1, index + by))]


def _cap(severity: str, ceiling: str) -> str:
    if severity not in SEVERITY_ORDER:
        return ceiling
    return severity if SEVERITY_ORDER.index(severity) <= SEVERITY_ORDER.index(ceiling) else ceiling


def band_severity(item: WebAnalysisItem, score: int | None) -> str:
    """The catalogue row's own band for a score. A scoreless outcome
    (`n_a`/`error`) is `info`: it carries no judgement about the page."""
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


def severity_for(item: WebAnalysisItem, score: int | None, *, on_homepage: bool = False) -> str:
    """Severity = the check's band, shaped by its TIER (Arman's 2026-10-05
    check-tier rulings, ``web.analysis_item.tier``) and where it failed.

    * A (blocks being found): one step up, never below ``high`` once failing.
    * B (hurts rankings): the band, capped at ``high``.
    * C (polish): the band, capped at ``low``.
    * D (AI opinion): always ``info`` — an opinion never escalates.
    * A failure on the homepage moves up one more step (except tier D).
    A passing or scoreless result stays ``info`` whatever the tier.
    Plan: common-docs/systems/marketing/seo/projects/fact-before-opinion/REGISTER.md R-04.
    """
    base = band_severity(item, score)
    if base == "info":
        return "info"
    tier = getattr(item, "tier", None)
    if tier == "D":
        return "info"
    if tier == "A":
        severity = _step(base, 1)
        if SEVERITY_ORDER.index(severity) < SEVERITY_ORDER.index("high"):
            severity = "high"
    elif tier == "B":
        severity = _cap(base, "high")
    elif tier == "C":
        severity = _cap(base, "low")
    else:
        severity = base
    if on_homepage:
        severity = _step(severity, 1)
        if tier == "C":
            severity = _cap(severity, "med")
    return severity


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
    site_scoped_item_ids: frozenset[str] | set[str] = frozenset(),
    rolled_up: dict[tuple[str, str], str] | None = None,
    rollup_item_ids: frozenset[str] | set[str] = frozenset(),
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

    ``rolled_up`` maps ``(page subject id, item id)`` to the site result that
    names the shared cause (``web_crawl/rollup.py``): such a page row opens no
    page finding, and an open one closes with ``metadata.rolled_up`` pointing
    at the site result. ``rollup_item_ids`` are the checks that MAY roll up;
    an open SITE finding for one of them that got no site row this run closes,
    because the shared cause is gone (or no longer shared).
    """
    rolled_up = rolled_up or {}

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

    # A check that moved from one-row-per-page to one-row-per-site leaves its old
    # page-subject findings behind; nothing will ever pass or fail them again, so
    # they are resolved here (history kept — the rows stay, status `resolved`).
    # Only an item that produced a non-error SITE row in this run is retired, so a
    # crashed check never erases a finding.
    answered_site_items = {
        str(row["item_id"])
        for row, _created in results
        if row["subject_type"] == "site"
        and row["status"] != "error"
        and str(row["item_id"]) in site_scoped_item_ids
    }
    retired: list[dict] = [
        {
            "id": str(f.id),
            "status": "resolved",
            "resolved_at": computed_at,
        }
        for f in findings
        if f.subject_type == "page"
        and f.status != "resolved"
        and str(f.item_id) in answered_site_items
    ]

    creates: list[dict] = []
    refreshes: list[dict] = []
    reopens: list[dict] = []
    resolves: list[dict] = []
    unverified: list[dict] = []
    covered: list[dict] = []
    for row, created in results:
        key = (str(row["subject_id"]), str(row["item_id"]))
        existing = open_by_key.get(key)
        if key in rolled_up and row["status"] in ("warn", "fail"):
            if existing is not None:
                covered.append(
                    {
                        "id": str(existing.id),
                        "status": "resolved",
                        "resolved_at": computed_at,
                        "last_result_id": str(created.id),
                        "metadata": {
                            **(getattr(existing, "metadata", None) or {}),
                            "rolled_up": {"site_result_id": rolled_up[key]},
                        },
                    }
                )
            continue
        if row["status"] in ("warn", "fail"):
            if existing is None and key in resolved_by_key:
                # It came back. Same row, same history, same suppression.
                prior = resolved_by_key.pop(key)
                reopens.append(
                    {
                        "id": str(prior.id),
                        "metadata": {
                            k: v
                            for k, v in (getattr(prior, "metadata", None) or {}).items()
                            if k not in ("unverified", "rolled_up")
                        },
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
        elif row["status"] == "n_a" and existing is not None:
            reason = (row.get("metadata") or {}).get("reasoning")
            unverified.append(
                {
                    "id": str(existing.id),
                    "status": "resolved",
                    "resolved_at": computed_at,
                    "last_result_id": str(created.id),
                    "metadata": {
                        **(getattr(existing, "metadata", None) or {}),
                        "unverified": {"at": computed_at.isoformat(), "reason": reason},
                    },
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

    # A roll-up site finding whose shared cause is gone: no site row this run.
    answered_rollups = {
        str(row["item_id"])
        for row, _created in results
        if row["subject_type"] == "site" and str(row["item_id"]) in rollup_item_ids
    }
    # "The shared cause is gone" needs most pages actually re-judged: when most
    # came back n_a (stale lab data, blocked fetches) the close is UNVERIFIED,
    # with the reason, never a silent "fixed".
    gone_rollups: list[dict] = []
    judged: dict[str, int] = defaultdict(int)
    page_rows: dict[str, int] = defaultdict(int)
    for row, _created in results:
        if row["subject_type"] != "page":
            continue
        page_rows[str(row["item_id"])] += 1
        if row["status"] in ("pass", "warn", "fail"):
            judged[str(row["item_id"])] += 1
    for f in findings:
        item = str(f.item_id)
        if (
            f.subject_type != "site"
            or f.status == "resolved"
            or item not in rollup_item_ids
            or item in answered_rollups
            or judged[item] == 0
        ):
            continue
        mostly_judged = judged[item] * 2 >= page_rows[item]
        gone_rollups.append(
            {
                "id": str(f.id),
                "status": "resolved",
                "resolved_at": computed_at,
                "metadata": {
                    **(getattr(f, "metadata", None) or {}),
                    **(
                        {"cause_gone": {"at": computed_at.isoformat()}}
                        if mostly_judged
                        else {
                            "unverified": {
                                "at": computed_at.isoformat(),
                                "reason": (
                                    f"Only {judged[item]} of {page_rows[item]} pages could be "
                                    "rechecked, so we can't confirm the shared cause is fixed."
                                ),
                            }
                        }
                    ),
                },
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
                    "metadata": "jsonb",
                },
            )
        summary.findings_reopened += len(reopens)
    if retired:
        async with transaction(WEB_DB_NAME):
            await bulk_update_by_pk(
                WebFinding,
                retired,
                casts={"id": "uuid", "status": "text", "resolved_at": "timestamptz"},
            )
        summary.findings_resolved += len(retired)
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
    if unverified:
        async with transaction(WEB_DB_NAME):
            await bulk_update_by_pk(
                WebFinding,
                unverified,
                casts={
                    "id": "uuid",
                    "status": "text",
                    "resolved_at": "timestamptz",
                    "last_result_id": "uuid",
                    "metadata": "jsonb",
                },
            )
        summary.findings_resolved += len(unverified)
    if gone_rollups:
        async with transaction(WEB_DB_NAME):
            await bulk_update_by_pk(
                WebFinding,
                gone_rollups,
                casts={"id": "uuid", "status": "text", "resolved_at": "timestamptz", "metadata": "jsonb"},
            )
        summary.findings_resolved += len(gone_rollups)
    if covered:
        async with transaction(WEB_DB_NAME):
            await bulk_update_by_pk(
                WebFinding,
                covered,
                casts={
                    "id": "uuid",
                    "status": "text",
                    "resolved_at": "timestamptz",
                    "last_result_id": "uuid",
                    "metadata": "jsonb",
                },
            )
        summary.findings_resolved += len(covered)


__all__ = ["insert_results", "reconcile_findings", "severity_for"]
