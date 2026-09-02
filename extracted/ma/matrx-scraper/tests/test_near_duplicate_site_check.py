from matrx_scraper.web_crawl.near_duplicate import (
    NEAR_DUPLICATE_MAX_DISTANCE,
    NearDuplicatePage,
    build_near_duplicate_report,
)
from matrx_scraper.web_crawl.analysis import SITE_CHECKS, PageFacts, _build_site_facts


def page(
    page_id: str,
    simhash: str | None,
    *,
    version: int | None = 1,
    canonical_url: str | None = None,
    indexable: bool | None = True,
) -> NearDuplicatePage:
    return NearDuplicatePage(
        page_id=page_id,
        url=f"https://example.com/{page_id}",
        fingerprint_version=version,
        simhash64=simhash,
        canonical_url=canonical_url,
        indexable=indexable,
    )


def test_contract_threshold_and_site_score_are_exact():
    assert NEAR_DUPLICATE_MAX_DISTANCE == 6
    report = build_near_duplicate_report(
        [
            page("a", "0000000000000000"),
            page("b", "000000000000003f"),  # six changed bits = 90.625%
            page("c", "ffffffffffffffff"),
            page("noindex", "0000000000000000", indexable=False),
        ]
    )
    assert report.indexable_pages == 3
    assert report.near_duplicate_pages == 2
    assert report.score == 33
    assert [[item.page_id for item in cluster.pages] for cluster in report.clusters] == [["a", "b"]]


def test_seven_bit_distance_is_below_the_published_threshold():
    report = build_near_duplicate_report(
        [page("a", "0000000000000000"), page("b", "000000000000007f")]
    )
    assert report.near_duplicate_pages == 0
    assert report.score == 100


def test_versions_never_compare_and_missing_fingerprints_make_score_unknown():
    report = build_near_duplicate_report(
        [
            page("old", "0000000000000000", version=1),
            page("new", "0000000000000000", version=2),
            page("missing", None, version=None),
        ]
    )
    assert report.near_duplicate_pages == 0
    assert report.pages_without_fingerprint == 1
    assert report.score is None


def test_unknown_indexability_makes_the_site_score_unknown():
    report = build_near_duplicate_report(
        [page("known", "0000000000000000"), page("unknown", "ffffffffffffffff", indexable=None)]
    )
    assert report.indexable_pages == 1
    assert report.pages_without_indexability == 1
    assert report.score is None


def test_canonical_consolidated_pairs_are_excluded():
    canonical = "https://example.com/a"
    report = build_near_duplicate_report(
        [
            page("a", "0000000000000000", canonical_url=canonical),
            page("variant", "0000000000000001", canonical_url=canonical),
        ]
    )
    assert report.canonical_pairs_excluded == 1
    assert report.near_duplicate_pages == 0
    assert report.score == 100


def test_evidence_names_every_pair_and_page_deterministically():
    report = build_near_duplicate_report(
        [
            page("c", "0000000000000003"),
            page("a", "0000000000000000"),
            page("b", "0000000000000001"),
        ]
    )
    evidence = report.evidence()
    cluster = evidence["clusters"][0]
    assert cluster["pages"] == [
        "https://example.com/a",
        "https://example.com/b",
        "https://example.com/c",
    ]
    assert cluster["matching_pairs"][0] == {
        "left_page_id": "a",
        "left_url": "https://example.com/a",
        "right_page_id": "b",
        "right_url": "https://example.com/b",
        "hamming_distance": 1,
        "similarity_percent": 98.44,
    }


def test_site_registry_scores_one_aggregate_result_with_cluster_evidence():
    facts = _build_site_facts(
        "site-1",
        [
            PageFacts(
                page_id="a",
                url="https://example.com/a",
                noindex=False,
                fingerprint_version=1,
                simhash64="0000000000000000",
            ),
            PageFacts(
                page_id="b",
                url="https://example.com/b",
                noindex=False,
                fingerprint_version=1,
                simhash64="0000000000000001",
            ),
        ],
    )
    outcome = SITE_CHECKS["near_duplicate_content"](facts)
    assert outcome.status == "fail"
    assert outcome.score == 0
    assert outcome.issue_count == 2
    assert outcome.evidence["clusters"][0]["pages"] == [
        "https://example.com/a",
        "https://example.com/b",
    ]
