from __future__ import annotations

from datetime import date

import pytest

from matrx_scraper.db.models_seo_host import SeoSearchPerformanceDaily
from matrx_scraper.web_crawl.analysis import SITE_CHECKS, SiteFacts
from matrx_scraper.web_crawl.gsc_cannibalization import (
    CannibalPage,
    CannibalQuery,
    GscCannibalizationEvidence,
    check_gsc_keyword_cannibalization,
    load_gsc_keyword_cannibalization,
)


def evidence(*, significant: int, cannibalized: int) -> GscCannibalizationEvidence:
    return GscCannibalizationEvidence(
        available=True,
        latest_date=date(2026, 8, 8),
        significant_queries=significant,
        cannibalized_queries=cannibalized,
        samples=[
            CannibalQuery(
                query="shared answer",
                impressions=1_000,
                competing_pages=(
                    CannibalPage("page-a", 550, 0.55),
                    CannibalPage("page-b", 450, 0.45),
                ),
            )
        ]
        if cannibalized
        else [],
    )


@pytest.mark.parametrize(
    ("significant", "cannibalized", "score", "status"),
    [
        (0, 0, 100, "pass"),
        (10, 0, 100, "pass"),
        (10, 1, 90, "warn"),
        (10, 5, 50, "warn"),
        (10, 7, 30, "fail"),
    ],
)
def test_live_formula_bands(significant, cannibalized, score, status):
    outcome = check_gsc_keyword_cannibalization(
        evidence(significant=significant, cannibalized=cannibalized)
    )
    assert outcome.score == score
    assert outcome.status == status
    assert outcome.issue_count == cannibalized


def test_half_score_rounds_like_postgres_not_python_bankers_rounding():
    outcome = check_gsc_keyword_cannibalization(evidence(significant=8, cannibalized=1))
    assert outcome.score == 88


def test_missing_query_page_collection_is_na_not_a_clean_pass():
    outcome = check_gsc_keyword_cannibalization(GscCannibalizationEvidence())
    assert outcome.status == "n_a"
    assert outcome.score is None
    assert outcome.remediation is not None


def test_evidence_names_every_competing_page_identity():
    outcome = check_gsc_keyword_cannibalization(evidence(significant=10, cannibalized=1))
    pages = outcome.evidence["samples"][0]["pages"]
    assert [page["page_id"] for page in pages] == ["page-a", "page-b"]
    assert outcome.evidence["significant_query_impression_floor"] == 200
    assert outcome.evidence["competing_page_share_floor"] == 0.2


def test_site_registry_persists_the_catalogue_check():
    assert "gsc_keyword_cannibalization" in SITE_CHECKS
    outcome = SITE_CHECKS["gsc_keyword_cannibalization"](
        SiteFacts(site_id="site", gsc_cannibalization=evidence(significant=4, cannibalized=1))
    )
    assert outcome.score == 75


def test_host_mirror_is_narrow_and_read_only():
    assert SeoSearchPerformanceDaily._meta.db_schema == "seo"
    assert SeoSearchPerformanceDaily._meta.table_name == "search_performance_daily"
    assert SeoSearchPerformanceDaily._read_only is True
    assert "clicks" not in SeoSearchPerformanceDaily._meta.fields


@pytest.mark.asyncio
async def test_loader_uses_latest_run_per_date_and_batched_aggregates(monkeypatch):
    responses = [
        [{"date": date(2026, 8, 8)}],
        [
            {"date": date(2026, 8, 7), "run_id": "run-new"},
            {"date": date(2026, 8, 8), "run_id": "run-new"},
        ],
        [
            {"query": "one owner", "total_impressions": 500},
            {"query": "split answer", "total_impressions": 1_000},
        ],
        [
            {"query": "one owner", "page_id": "page-a", "page_impressions": 500},
            {"query": "split answer", "page_id": "page-b", "page_impressions": 600},
            {"query": "split answer", "page_id": "page-c", "page_impressions": 400},
        ],
    ]
    filter_calls: list[tuple[tuple, dict]] = []
    operations: list[tuple[str, tuple]] = []

    class Query:
        def group_by(self, *args):
            operations.append(("group_by", args))
            return self

        def annotate(self, **_kwargs):
            return self

        def distinct(self, *_args):
            return self

        def order_by(self, *args):
            operations.append(("order_by", args))
            return self

        def limit(self, limit):
            operations.append(("limit", (limit,)))
            return self

        def filter(self, *args, **kwargs):
            filter_calls.append((args, kwargs))
            return self

        async def values(self, *_args):
            return responses.pop(0)

    def fake_filter(*args, **kwargs):
        filter_calls.append((args, kwargs))
        return Query()

    monkeypatch.setattr(SeoSearchPerformanceDaily, "filter", fake_filter)
    result = await load_gsc_keyword_cannibalization("site-1")

    assert result.significant_queries == 2
    assert result.cannibalized_queries == 1
    assert [page.page_id for page in result.samples[0].competing_pages] == ["page-b", "page-c"]
    assert any(call[1].get("dimension_profile") == "query_page" for call in filter_calls)
    assert any(call[0] for call in filter_calls), "winner date/run Q must constrain aggregates"
    assert operations[:2] == [("order_by", ("-date",)), ("limit", (1,))]
    assert ("group_by", ("site_id",)) not in operations
