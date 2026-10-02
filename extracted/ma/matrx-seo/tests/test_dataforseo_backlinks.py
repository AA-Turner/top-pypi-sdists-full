from __future__ import annotations

import json
from datetime import UTC, datetime
from decimal import Decimal
from pathlib import Path

import pytest

from matrx_seo.providers.dataforseo.backlinks import normalize_backlink_payload

_FIXTURE_PATH = Path(__file__).parent / "fixtures/dataforseo/backlinks/representative.json"
_RESULTS: dict[str, list[dict[str, object]]] = json.loads(_FIXTURE_PATH.read_text())
_FETCHED_AT = datetime(2026, 7, 22, 12, tzinfo=UTC)


def _raw(endpoint: str) -> dict[str, object]:
    return {
        "version": "0.1.20260722",
        "status_code": 20000,
        "status_message": "Ok.",
        "provider_envelope_extra": "retained",
        "tasks": [
            {
                "id": "task-1",
                "status_code": 20000,
                "status_message": "Ok.",
                "cost": 0.024,
                "provider_task_extra": "retained",
                "result": _RESULTS[endpoint],
            }
        ],
    }


@pytest.mark.parametrize(
    ("endpoint", "dataset", "backlinks", "dimensions"),
    [
        ("/v3/backlinks/summary/live", "summary", 0, 0),
        ("/v3/backlinks/backlinks/live", "backlinks", 1, 0),
        ("/v3/backlinks/referring_domains/live", "referring_domains", 0, 1),
        ("/v3/backlinks/anchors/live", "anchors", 0, 1),
        ("/v3/backlinks/history/live", "history", 0, 0),
        ("/v3/backlinks/domain_pages/live", "domain_pages", 0, 1),
        ("/v3/backlinks/domain_pages_summary/live", "domain_pages_summary", 0, 1),
        ("/v3/backlinks/timeseries_summary/live", "timeseries_summary", 0, 0),
        (
            "/v3/backlinks/timeseries_new_lost_summary/live",
            "timeseries_new_lost_summary",
            0,
            0,
        ),
        ("/v3/backlinks/competitors/live", "competitors", 0, 1),
    ],
)
def test_all_supported_endpoints_dispatch(
    endpoint: str,
    dataset: str,
    backlinks: int,
    dimensions: int,
) -> None:
    observations = normalize_backlink_payload(
        endpoint=endpoint,
        raw=_raw(endpoint),
        site_id="site-1",
        page_id="page-1",
        target="example.com",
        fetched_at=_FETCHED_AT,
    )
    assert len(observations) == 1
    observation = observations[0]
    assert observation.dataset == dataset
    assert observation.site_id == "site-1"
    assert observation.page_id == "page-1"
    assert observation.target == "example.com"
    assert len(observation.backlinks) == backlinks
    assert len(observation.dimensions) == dimensions
    assert observation.extras["provider_envelope"]["provider_envelope_extra"] == "retained"
    assert observation.extras["provider_task"]["provider_task_extra"] == "retained"


def test_summary_maps_metrics_and_preserves_unmodeled_info() -> None:
    observation = normalize_backlink_payload(
        endpoint="/v3/backlinks/summary/live",
        raw=_raw("/v3/backlinks/summary/live"),
        site_id="site-1",
        page_id=None,
        target="fallback.example",
        fetched_at=_FETCHED_AT,
    )[0]
    assert observation.total_backlinks == 12
    assert observation.nofollow_backlinks == 2
    assert observation.dofollow_backlinks == 10
    assert observation.referring_domains == 5
    assert observation.referring_ips == 4
    assert observation.referring_subnets == 3
    assert observation.broken_backlinks == 1
    assert observation.rank_score == Decimal("321")
    assert observation.spam_score == Decimal("7")
    assert observation.extras["provider_result"]["info"] == {"country": "US"}


def test_summary_maps_nofollow_from_referring_links_attributes() -> None:
    raw = _raw("/v3/backlinks/summary/live")
    raw["tasks"][0]["result"] = [
        {
            "target": "example.com",
            "rank": 258,
            "backlinks": 1610,
            "referring_domains": 451,
            "referring_links_attributes": {"nofollow": 185, "ugc": 76},
            "referring_pages_nofollow": 185,
        }
    ]
    observation = normalize_backlink_payload(
        endpoint="/v3/backlinks/summary/live",
        raw=raw,
        site_id="site-1",
        page_id=None,
        target="example.com",
        fetched_at=_FETCHED_AT,
    )[0]
    assert observation.total_backlinks == 1610
    assert observation.nofollow_backlinks == 185
    assert observation.dofollow_backlinks == 1425


def test_empty_collection_accepts_provider_null_items_with_zero_counts() -> None:
    raw = _raw("/v3/backlinks/domain_pages/live")
    raw["tasks"][0]["result"] = [
        {
            "target": "example.com",
            "items": None,
            "items_count": 0,
            "total_count": 0,
        }
    ]

    observation = normalize_backlink_payload(
        endpoint="/v3/backlinks/domain_pages/live",
        raw=raw,
        site_id="site-1",
        page_id=None,
        target="example.com",
        fetched_at=_FETCHED_AT,
    )[0]

    assert observation.dimensions == []


def test_backlink_rows_map_identity_state_ranks_and_extras() -> None:
    snapshot = normalize_backlink_payload(
        endpoint="/v3/backlinks/backlinks/live",
        raw=_raw("/v3/backlinks/backlinks/live"),
        site_id="site-1",
        page_id="page-1",
        target="example.com",
        fetched_at=_FETCHED_AT,
    )[0]
    assert snapshot.total_backlinks == 1
    item = snapshot.backlinks[0]
    assert item.source_url == "https://source.example/post"
    assert item.source_domain == "source.example"
    assert item.target_url == "https://example.com/page"
    assert item.anchor_text == "Example"
    assert item.is_dofollow is True
    assert item.state == "new"
    assert item.source_rank == Decimal("101")
    assert item.domain_rank == Decimal("202")
    assert item.extras["tld_from"] == "example"
    assert snapshot.extras["provider_result"]["search_after_token"] == "next"


def test_dimension_endpoints_map_their_distinct_identity_shapes() -> None:
    referring = normalize_backlink_payload(
        endpoint="/v3/backlinks/referring_domains/live",
        raw=_raw("/v3/backlinks/referring_domains/live"),
        site_id="site-1",
        page_id=None,
        target="example.com",
        fetched_at=_FETCHED_AT,
    )[0].dimensions[0]
    assert referring.dimension_kind == "referring_domain"
    assert referring.dimension_key == "source.example"
    assert referring.backlinks == 8
    assert referring.extras["referring_links_tld"] == {"com": 8}

    anchor = normalize_backlink_payload(
        endpoint="/v3/backlinks/anchors/live",
        raw=_raw("/v3/backlinks/anchors/live"),
        site_id="site-1",
        page_id=None,
        target="example.com",
        fetched_at=_FETCHED_AT,
    )[0].dimensions[0]
    assert anchor.dimension_kind == "anchor"
    assert anchor.dimension_key == "Example"
    assert anchor.extras["referring_links_attributes"] == {"nofollow": 1}

    competitor = normalize_backlink_payload(
        endpoint="/v3/backlinks/competitors/live",
        raw=_raw("/v3/backlinks/competitors/live"),
        site_id="site-1",
        page_id=None,
        target="example.com",
        fetched_at=_FETCHED_AT,
    )[0].dimensions[0]
    assert competitor.dimension_kind == "competitor_domain"
    assert competitor.dimension_key == "competitor.example"
    assert competitor.rank_score == Decimal("199")
    assert competitor.extras["intersections"] == 42


def test_domain_page_variants_map_nested_and_flat_summaries() -> None:
    nested = normalize_backlink_payload(
        endpoint="/v3/backlinks/domain_pages/live",
        raw=_raw("/v3/backlinks/domain_pages/live"),
        site_id="site-1",
        page_id=None,
        target="example.com",
        fetched_at=_FETCHED_AT,
    )[0].dimensions[0]
    assert nested.dimension_key == "https://example.com/page"
    assert nested.label == "Example Page"
    assert nested.backlinks == 9
    assert nested.referring_domains == 5
    assert nested.extras["meta"]["words_count"] == 500
    assert nested.extras["page_summary"]["broken_backlinks"] == 2

    flat = normalize_backlink_payload(
        endpoint="/v3/backlinks/domain_pages_summary/live",
        raw=_raw("/v3/backlinks/domain_pages_summary/live"),
        site_id="site-1",
        page_id=None,
        target="example.com",
        fetched_at=_FETCHED_AT,
    )[0].dimensions[0]
    assert flat.dimension_key == "https://example.com/summary"
    assert flat.backlinks == 7
    assert flat.extras["referring_links_countries"] == {"US": 7}


def test_history_and_timeseries_use_provider_bucket_time() -> None:
    history = normalize_backlink_payload(
        endpoint="/v3/backlinks/history/live",
        raw=_raw("/v3/backlinks/history/live"),
        site_id="site-1",
        page_id=None,
        target="example.com",
        fetched_at=_FETCHED_AT,
    )[0]
    assert history.observed_at == datetime(2026, 6, 30, tzinfo=UTC)
    assert history.new_backlinks == 3
    assert history.lost_backlinks == 1
    assert history.extras["provider_item"]["new_referring_domains"] == 2

    summary = normalize_backlink_payload(
        endpoint="/v3/backlinks/timeseries_summary/live",
        raw=_raw("/v3/backlinks/timeseries_summary/live"),
        site_id="site-1",
        page_id=None,
        target="example.com",
        fetched_at=_FETCHED_AT,
    )[0]
    assert summary.total_backlinks == 15
    assert summary.nofollow_backlinks == 4
    assert summary.dofollow_backlinks == 11
    assert summary.extras["provider_item"]["referring_pages"] == 14

    new_lost = normalize_backlink_payload(
        endpoint="/v3/backlinks/timeseries_new_lost_summary/live",
        raw=_raw("/v3/backlinks/timeseries_new_lost_summary/live"),
        site_id="site-1",
        page_id=None,
        target="example.com",
        fetched_at=_FETCHED_AT,
    )[0]
    assert new_lost.new_backlinks == 5
    assert new_lost.lost_backlinks == 2
    assert new_lost.extras["provider_item"]["lost_referring_domains"] == 1


@pytest.mark.parametrize(
    ("endpoint", "raw", "message"),
    [
        ("/v3/backlinks/not_real/live", {"tasks": []}, "unsupported"),
        ("/v3/backlinks/summary/live", {}, "tasks must be a non-empty list"),
        (
            "/v3/backlinks/summary/live",
            {"tasks": [{"result": {}}]},
            "task.result must be a list",
        ),
        (
            "/v3/backlinks/backlinks/live",
            {"tasks": [{"result": [{"target": "example.com", "items": {}}]}]},
            "result.items must be a list",
        ),
    ],
)
def test_unknown_endpoint_and_malformed_shapes_fail_loudly(
    endpoint: str,
    raw: dict[str, object],
    message: str,
) -> None:
    with pytest.raises(ValueError, match=message):
        normalize_backlink_payload(
            endpoint=endpoint,
            raw=raw,
            site_id="site-1",
            page_id=None,
            target="example.com",
            fetched_at=_FETCHED_AT,
        )
