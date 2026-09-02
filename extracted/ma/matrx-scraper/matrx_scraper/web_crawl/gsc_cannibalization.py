"""Canonical query×page evidence for the site-level GSC cannibalization check."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, timedelta
from decimal import Decimal, ROUND_HALF_UP
from functools import reduce

from matrx_orm import Q, Sum

from matrx_scraper.db.models_seo_host import SeoSearchPerformanceDaily
from matrx_scraper.seo_audit import CheckOutcome, SYNC_GSC, clamp_score

GSC_CANNIBAL_PERIOD_DAYS = 28
GSC_CANNIBAL_MIN_IMPRESSIONS = 200
GSC_CANNIBAL_MIN_PAGE_SHARE = 0.20
# How many significant query names one page-split aggregate covers. Bounds the
# IN-list size, nothing else — the totals pass is a single grouped query now.
GSC_CANNIBAL_PAGE_SPLIT_BATCH_SIZE = 500
GSC_CANNIBAL_EVIDENCE_LIMIT = 20


@dataclass(frozen=True)
class CannibalPage:
    page_id: str
    impressions: int
    impression_share: float


@dataclass(frozen=True)
class CannibalQuery:
    query: str
    impressions: int
    competing_pages: tuple[CannibalPage, ...]


@dataclass
class GscCannibalizationEvidence:
    available: bool = False
    latest_date: date | None = None
    significant_queries: int = 0
    cannibalized_queries: int = 0
    samples: list[CannibalQuery] = field(default_factory=list)


def check_gsc_keyword_cannibalization(
    evidence: GscCannibalizationEvidence,
) -> CheckOutcome:
    if not evidence.available or evidence.latest_date is None:
        return CheckOutcome(
            "n_a",
            None,
            "No query-by-page Search Console evidence has been collected for this "
            "site. Pull Search Console query and page data before judging whether "
            "multiple pages compete for the same search.",
            remediation=SYNC_GSC,
        )

    significant = evidence.significant_queries
    cannibalized = evidence.cannibalized_queries
    ratio = cannibalized / significant if significant else 0.0
    score = clamp_score(
        int(
            (Decimal(100) * (Decimal(1) - Decimal(str(ratio)))).quantize(
                Decimal("1"), rounding=ROUND_HALF_UP
            )
        )
    )
    window_start = evidence.latest_date - timedelta(days=GSC_CANNIBAL_PERIOD_DAYS - 1)
    stored_evidence = {
        "window": {
            "from": window_start.isoformat(),
            "to": evidence.latest_date.isoformat(),
            "days": GSC_CANNIBAL_PERIOD_DAYS,
        },
        "significant_query_impression_floor": GSC_CANNIBAL_MIN_IMPRESSIONS,
        "competing_page_share_floor": GSC_CANNIBAL_MIN_PAGE_SHARE,
        "significant_queries": significant,
        "cannibalized_queries": cannibalized,
        "cannibalized_share": round(ratio, 4),
        "samples": [
            {
                "query": sample.query,
                "impressions": sample.impressions,
                "pages": [
                    {
                        "page_id": page.page_id,
                        "impressions": page.impressions,
                        "impression_share": round(page.impression_share, 4),
                    }
                    for page in sample.competing_pages
                ],
            }
            for sample in evidence.samples
        ],
    }
    if cannibalized == 0:
        detail = (
            "No query reached 200 impressions in this period, so there was no "
            "meaningful search demand to split across pages."
            if significant == 0
            else f"None of the {significant:,} queries with at least "
            f"{GSC_CANNIBAL_MIN_IMPRESSIONS} impressions was split across two "
            "pages holding 20% or more each."
        )
        return CheckOutcome("pass", 100, detail, evidence=stored_evidence)

    status = "warn" if score >= 50 else "fail"
    return CheckOutcome(
        status,
        score,
        f"{cannibalized:,} of {significant:,} significant Google queries "
        f"({ratio:.0%}) split their impressions across at least two pages with "
        "20% or more each. Those pages are competing with one another for the "
        "same search instead of giving Google one clear answer to rank.",
        issue_count=cannibalized,
        evidence=stored_evidence,
    )


async def load_gsc_keyword_cannibalization(
    site_id: str,
) -> GscCannibalizationEvidence:
    """Load a complete 28-day census in a BOUNDED number of grouped queries.

    The canonical SEO writer can re-collect the same date. Exactly as the live
    GSC insight RPC does, the newest run for each date wins.

    🚨 Never page the query universe through repeated aggregates. The previous
    shape read query names 100 at a time, re-running TWO grouped aggregates
    over the whole window per batch — ~1.8s each on a 991k-row site (measured
    live 2026-08-12), so a 19k-query site spent 20+ minutes in this loader
    alone and the analysis run was reaped before it could write anything. One
    query's total is one small tuple: the whole distinct-query census of even a
    large site is a few MB, far cheaper than hundreds of table-wide scans.
    """

    base_filters = {
        "site_id": site_id,
        "provider": "gsc",
        "dimension_profile": "query_page",
        "query__isnull": False,
        "page_id__isnull": False,
    }
    # Read one row from the canonical GSC scope index instead of aggregating
    # every qualifying row. GROUP BY + MAX prevented Postgres from using the
    # ordered `(site_id, dimension_profile, date)` partial index as a bounded
    # watermark lookup on large sites.
    span = await (
        SeoSearchPerformanceDaily.filter(**base_filters)
        .order_by("-date")
        .limit(1)
        .values("date")
    )
    if not span or span[0]["date"] is None:
        return GscCannibalizationEvidence()

    latest: date = span[0]["date"]
    start = latest - timedelta(days=GSC_CANNIBAL_PERIOD_DAYS - 1)
    winners = await (
        SeoSearchPerformanceDaily.filter(**base_filters, date__gte=start, date__lte=latest)
        .distinct("date")
        .order_by("date", "-created_at", "-run_id")
        .values("date", "run_id")
    )
    if not winners:
        return GscCannibalizationEvidence()
    winner_pairs = reduce(
        lambda left, right: left | right,
        (Q(date=row["date"], run_id=row["run_id"]) for row in winners),
    )
    evidence = GscCannibalizationEvidence(available=True, latest_date=latest)

    # ONE grouped pass over the window for per-query totals; the significance
    # floor is applied in Python because a total is one tiny tuple.
    total_rows = await (
        SeoSearchPerformanceDaily.filter(winner_pairs, **base_filters)
        .group_by("query")
        .annotate(total_impressions=Sum("impressions"))
        .values("query", "total_impressions")
    )
    query_totals = {
        str(row["query"]): int(row["total_impressions"] or 0)
        for row in total_rows
        if int(row["total_impressions"] or 0) >= GSC_CANNIBAL_MIN_IMPRESSIONS
    }
    evidence.significant_queries = len(query_totals)
    if not query_totals:
        return evidence

    # Page splits for the significant queries only, IN-list bounded per batch.
    pages_by_query: dict[str, list[CannibalPage]] = {}
    names = sorted(query_totals)
    for start in range(0, len(names), GSC_CANNIBAL_PAGE_SPLIT_BATCH_SIZE):
        chunk = names[start : start + GSC_CANNIBAL_PAGE_SPLIT_BATCH_SIZE]
        page_rows = await (
            SeoSearchPerformanceDaily.filter(
                winner_pairs,
                **base_filters,
                query__in=chunk,
            )
            .group_by("query", "page_id")
            .annotate(page_impressions=Sum("impressions"))
            .values("query", "page_id", "page_impressions")
        )
        for row in page_rows:
            query = str(row["query"])
            impressions = int(row["page_impressions"] or 0)
            share = impressions / query_totals[query]
            if share >= GSC_CANNIBAL_MIN_PAGE_SHARE:
                pages_by_query.setdefault(query, []).append(
                    CannibalPage(str(row["page_id"]), impressions, share)
                )

    cannibalized = [(query, pages) for query, pages in pages_by_query.items() if len(pages) >= 2]
    evidence.cannibalized_queries = len(cannibalized)
    cannibalized.sort(key=lambda pair: (-query_totals[pair[0]], pair[0]))
    evidence.samples = [
        CannibalQuery(
            query=query,
            impressions=query_totals[query],
            competing_pages=tuple(
                sorted(pages, key=lambda page: (-page.impressions, page.page_id))
            ),
        )
        for query, pages in cannibalized[:GSC_CANNIBAL_EVIDENCE_LIMIT]
    ]
    return evidence


__all__ = [
    "CannibalPage",
    "CannibalQuery",
    "GSC_CANNIBAL_MIN_IMPRESSIONS",
    "GSC_CANNIBAL_MIN_PAGE_SHARE",
    "GSC_CANNIBAL_PAGE_SPLIT_BATCH_SIZE",
    "GscCannibalizationEvidence",
    "check_gsc_keyword_cannibalization",
    "load_gsc_keyword_cannibalization",
]
