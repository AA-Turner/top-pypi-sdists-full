"""SERP prospecting — the query builder, the tag contract, and the normalizer.

Pins the three things a future agent would otherwise get wrong:

* the tag IS the contract — variant/seed/exclude ride inside the provider
  payload, so a resumed run normalizes identically with no side-channel;
* our own domain never becomes an opportunity;
* an untagged organic SERP payload REFUSES normalization loudly — rank
  tracking on DataForSEO has no canonical normalizer and must not silently
  become prospecting.
"""

from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal

import pytest

from matrx_seo.providers.dataforseo.serp_prospect import (
    decode_prospect_tag,
    encode_prospect_tag,
    is_prospect_payload,
    normalize_serp_prospect_payload,
)
from matrx_seo.serp_prospecting import (
    HOT_OFF_PRESS_SEARCH_PARAM,
    MAX_PROSPECT_QUERIES,
    QueryVariant,
    build_prospect_queries,
)

FETCHED_AT = datetime(2026, 8, 16, 12, 0, tzinfo=UTC)


def _tag(variant: str = "keyword", seed: str = "dental implants") -> str:
    return encode_prospect_tag(variant=variant, seed_keyword=seed, exclude_domain="mysite.com")


def _payload(items_by_task: list[tuple[str, str, list[dict]]]) -> dict:
    """items_by_task: (query, tag, items)."""
    return {
        "version": "3",
        "status_code": 20000,
        "tasks": [
            {
                "id": f"task-{index}",
                "status_code": 20000,
                "data": {"keyword": query, "tag": tag},
                "result": [{"items": items}],
            }
            for index, (query, tag, items) in enumerate(items_by_task)
        ],
    }


def _item(domain: str, rank: int, *, type_: str = "organic") -> dict:
    return {
        "type": type_,
        "rank_absolute": rank,
        "rank_group": rank,
        "url": f"https://{domain}/page-{rank}",
        "domain": domain,
        "title": f"{domain} page",
        "description": "snippet",
    }


class TestTagContract:
    def test_round_trip(self):
        tag = encode_prospect_tag(
            variant="resource_page",
            seed_keyword="emergency dentist",
            exclude_domain="Example.COM",
        )
        assert decode_prospect_tag(tag) == (
            "resource_page",
            "emergency dentist",
            "example.com",
        )

    def test_foreign_tag_is_not_ours(self):
        assert decode_prospect_tag("someone-elses-tag") is None
        assert decode_prospect_tag(None) is None

    def test_pipe_stripped_not_smuggled(self):
        tag = encode_prospect_tag(variant="keyword", seed_keyword="a|b", exclude_domain="x.com")
        assert decode_prospect_tag(tag) == ("keyword", "a b", "x.com")


class TestQueryBuilder:
    def test_variants_expand_and_dedupe(self):
        queries, dropped = build_prospect_queries(
            ["dental implants", " dental   implants "],
            [QueryVariant.KEYWORD, QueryVariant.RESOURCE_PAGE],
        )
        texts = [q.query for q in queries]
        assert texts[0] == "dental implants"
        assert "dental implants intitle:resources" in texts
        assert len(texts) == len(set(t.lower() for t in texts))
        assert not dropped

    def test_cap_names_what_was_dropped(self):
        keywords = [f"keyword {n}" for n in range(20)]
        queries, dropped = build_prospect_queries(
            keywords,
            [
                QueryVariant.KEYWORD,
                QueryVariant.ADVANCED_OPERATOR,
                QueryVariant.RESOURCE_PAGE,
                QueryVariant.LISTICLE,
            ],
        )
        assert len(queries) == MAX_PROSPECT_QUERIES
        assert dropped  # 20 seeds × 7 templates = 140 candidates

    def test_blank_keywords_refuse(self):
        with pytest.raises(ValueError, match="no usable"):
            build_prospect_queries(["   "], [QueryVariant.KEYWORD])

    def test_hot_off_press_param_is_last_24h(self):
        assert HOT_OFF_PRESS_SEARCH_PARAM == "tbs=qdr:d"

    def test_hot_off_press_survives_keyword_dedupe(self):
        # Same query TEXT as the keyword variant, but a different paid request
        # (tbs=qdr:d) — the first live preview silently dropped the variant.
        queries, _ = build_prospect_queries(
            ["dental implants"], [QueryVariant.KEYWORD, QueryVariant.HOT_OFF_PRESS]
        )
        variants = [q.variant for q in queries]
        assert QueryVariant.KEYWORD in variants
        assert QueryVariant.HOT_OFF_PRESS in variants


class TestNormalizer:
    def test_aggregates_across_queries_by_domain(self):
        payload = _payload(
            [
                ("dental implants", _tag(), [_item("blog-a.com", 3), _item("news-b.com", 7)]),
                (
                    '"dental implants" "write for us"',
                    _tag("advanced_operator"),
                    [_item("blog-a.com", 1)],
                ),
            ]
        )
        assert is_prospect_payload(payload)
        observations = normalize_serp_prospect_payload(
            raw=payload, site_id="site-1", fetched_at=FETCHED_AT
        )
        assert len(observations) == 1
        obs = observations[0]
        by_domain = {d.normalized_domain: d for d in obs.domains}
        assert by_domain["blog-a.com"].mention_count == 2
        assert by_domain["blog-a.com"].best_rank == 1
        assert sorted(by_domain["blog-a.com"].variants) == [
            "advanced_operator",
            "keyword",
        ]
        assert by_domain["news-b.com"].mention_count == 1
        # Most-mentioned domain leads.
        assert obs.domains[0].normalized_domain == "blog-a.com"

    def test_own_domain_never_becomes_an_opportunity(self):
        payload = _payload(
            [("dental implants", _tag(), [_item("mysite.com", 1), _item("other.com", 2)])]
        )
        obs = normalize_serp_prospect_payload(raw=payload, site_id="site-1", fetched_at=FETCHED_AT)[
            0
        ]
        assert [d.normalized_domain for d in obs.domains] == ["other.com"]
        assert obs.excluded_domains == ["mysite.com"]

    def test_non_prospect_result_types_skipped(self):
        payload = _payload(
            [
                (
                    "dental implants",
                    _tag(),
                    [_item("ads.com", 1, type_="paid"), _item("real.com", 2)],
                )
            ]
        )
        obs = normalize_serp_prospect_payload(raw=payload, site_id="site-1", fetched_at=FETCHED_AT)[
            0
        ]
        assert [d.normalized_domain for d in obs.domains] == ["real.com"]

    def test_untagged_payload_refuses_loudly(self):
        payload = {
            "tasks": [
                {
                    "status_code": 20000,
                    "data": {"keyword": "dental implants"},
                    "result": [{"items": [_item("a.com", 1)]}],
                }
            ]
        }
        assert not is_prospect_payload(payload)
        with pytest.raises(NotImplementedError, match="rank"):
            normalize_serp_prospect_payload(raw=payload, site_id="site-1", fetched_at=FETCHED_AT)

    def test_no_search_results_is_an_empty_answer_not_a_failure(self):
        # DataForSEO 40102 "No Search Results." — the search ran and nobody
        # ranks (hot-off-press on a niche topic). Measured live 2026-08-16:
        # this failed a whole 16-task run before the fix.
        empty_task = {
            "id": "task-e",
            "status_code": 40102,
            "status_message": "No Search Results.",
            "data": {"keyword": "ai workflow automation", "tag": _tag("hot_off_press")},
            "result": None,
        }
        payload = _payload([("dental implants", _tag(), [_item("a.com", 1)])])
        payload["tasks"].append(empty_task)
        obs = normalize_serp_prospect_payload(raw=payload, site_id="site-1", fetched_at=FETCHED_AT)[
            0
        ]
        assert obs.extras.get("empty_queries") == ["ai workflow automation"]
        assert "failed_tasks" not in obs.extras

        # All-empty is a correct outcome too — zero domains, no raise.
        all_empty = {"tasks": [empty_task]}
        obs = normalize_serp_prospect_payload(
            raw=all_empty, site_id="site-1", fetched_at=FETCHED_AT
        )[0]
        assert obs.domains == []

    def test_client_batch_error_ignores_no_search_results(self):
        from matrx_seo.providers.dataforseo.client import _OK_TASK_STATUS_CODES

        assert 40102 in _OK_TASK_STATUS_CODES
        assert 20000 in _OK_TASK_STATUS_CODES

    def test_partial_task_failure_survives_total_failure_raises(self):
        ok = ("dental implants", _tag(), [_item("a.com", 1)])
        failed_task = {
            "id": "task-x",
            "status_code": 40501,
            "status_message": "invalid keyword",
            "data": {"keyword": "bad query", "tag": _tag("listicle")},
            "result": None,
        }
        payload = _payload([ok])
        payload["tasks"].append(failed_task)
        obs = normalize_serp_prospect_payload(raw=payload, site_id="site-1", fetched_at=FETCHED_AT)[
            0
        ]
        assert obs.extras["failed_tasks"][0]["query"] == "bad query"
        assert [d.normalized_domain for d in obs.domains] == ["a.com"]

        all_failed = {"tasks": [failed_task]}
        with pytest.raises(ValueError, match="every prospect SERP task failed"):
            normalize_serp_prospect_payload(raw=all_failed, site_id="site-1", fetched_at=FETCHED_AT)


class TestAuthorityFold:
    def test_bulk_payload_folds_by_field(self):
        from matrx_seo.authority_enrichment import (
            AuthorityEnrichmentService,
            DomainAuthorityMetrics,
        )

        metrics = {"a.com": DomainAuthorityMetrics(domain="a.com")}
        AuthorityEnrichmentService._fold_payload(
            {"tasks": [{"result": [{"items": [{"target": "www.A.com.", "rank": 312}]}]}]},
            "rank",
            metrics,
        )
        assert metrics["a.com"].domain_rank == Decimal("312")
