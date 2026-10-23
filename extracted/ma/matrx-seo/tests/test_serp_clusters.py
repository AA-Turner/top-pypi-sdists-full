"""Keyword clusters by search-result overlap (matrx_seo.serp_clusters) — behavior.

Each test states the rule it holds; each one fails if the rule is broken.
"""

from __future__ import annotations

import pytest

from matrx_seo.serp_clusters import (
    NO_ORGANIC_RESULTS,
    NO_STORED_RESULTS,
    ClusterSettings,
    KeywordSerp,
    cluster_id_for,
    cluster_keywords,
    normalize_url,
    pairwise_overlaps,
    top_urls,
)


def _urls(*names: str) -> list[str]:
    return [f"https://{n}.com/page" for n in names]


def _kw(kid: str, urls: list[str] | None, volume: int | None = None) -> KeywordSerp:
    return KeywordSerp(keyword_id=kid, phrase=f"phrase {kid}", urls=urls, search_volume=volume)


def _status(result, kid: str):
    return result.by_keyword()[kid]


# ── URL normalization ──────────────────────────────────────────────────────


@pytest.mark.parametrize(
    ("a", "b"),
    [
        ("https://www.example.com/a/", "http://example.com/a"),
        ("https://Example.COM/a?utm_source=x&utm_medium=y", "example.com/a"),
        ("https://example.com/a?gclid=1&b=2&a=1", "https://example.com/a?a=1&b=2"),
        ("https://example.com/a#section", "https://example.com/a"),
        ("https://example.com:443/a", "https://example.com/a"),
        ("https://example.com/?srsltid=AfmBOo", "https://example.com"),
    ],
)
def test_url_variants_of_one_page_normalize_to_the_same_key(a: str, b: str) -> None:
    assert normalize_url(a) == normalize_url(b)


# Shapes copied from stored seo.serp_result rows (census 2026-10-22).
def test_stored_srsltid_variants_of_one_page_are_one_page() -> None:
    stored = [
        "https://www.office.fedex.com/default/shredding-services?srsltid=AfmBOopk6Dtm-u9gFSzfykG2aq",
        "https://www.office.fedex.com/default/shredding-services?srsltid=AfmBOoqHa5_dNy4SmfPPdG3e0d",
        "https://www.office.fedex.com/default/shredding-services?srsltid=AfmBOoqMm6i1QqHzJekGzx1OKd",
    ]
    assert len({normalize_url(u) for u in stored}) == 1


def test_stored_query_identified_pages_stay_different() -> None:
    # The page IS the query: two YouTube videos, two Yelp searches. Stripping the query
    # (what a naive split on '?' does) would fake overlap between unrelated keywords.
    assert normalize_url("https://www.youtube.com/watch?v=0u99UQVqLCI") != normalize_url(
        "https://www.youtube.com/watch?v=5tzE2Je3Y10"
    )
    assert normalize_url("https://www.yelp.com/search?cflt=bubbletea&find_loc=Dothan%2C+AL") != normalize_url(
        "https://www.yelp.com/search?cflt=gardening&find_loc=Peoria%2C+IL"
    )
    a = cluster_keywords(
        [_kw("a", [f"https://www.youtube.com/watch?v=a{i}" for i in range(5)]),
         _kw("b", [f"https://www.youtube.com/watch?v=b{i}" for i in range(5)])]
    )
    assert a.clusters == []


@pytest.mark.parametrize(
    "wrapped",
    [
        "https://www.google.com/url?q=https://www.example.com/a/%3Futm_source%3Dx&sa=U&ved=2ahUKE&usg=AOvVaw",
        "https://www.google.com/url?sa=t&url=https%3A%2F%2Fexample.com%2Fa&ved=0CAE&usg=AOvVaw",
        "https://google.co.uk/url?q=http://example.com/a",
    ],
)
def test_google_click_wrappers_unwrap_to_their_target(wrapped: str) -> None:
    assert normalize_url(wrapped) == "example.com/a"


def test_a_google_search_link_is_not_a_wrapper() -> None:
    # Stored on image-pack rows: q= is search words, not a URL.
    link = "https://www.google.com/search?sca_esv=f05da100&hl=en&gl=US&q=JY+Tea&udm=2&source=univ"
    assert normalize_url(link).startswith("google.com/search?")


@pytest.mark.parametrize(
    "variant",
    [
        "https://youtu.be/9t8y-LXuYF8",
        "https://youtu.be/9t8y-LXuYF8?t=42",
        "https://m.youtube.com/watch?v=9t8y-LXuYF8&feature=share",
        "https://www.youtube.com/watch?v=9t8y-LXuYF8&t=1m30s&si=AbC",
    ],
)
def test_youtube_hosts_and_positions_are_one_video(variant: str) -> None:
    assert normalize_url(variant) == normalize_url("https://www.youtube.com/watch?v=9t8y-LXuYF8") == "youtube.com/watch?v=9t8y-LXuYF8"


def test_t_names_a_page_outside_youtube() -> None:
    assert normalize_url("https://forum.example.com/view?t=1") != normalize_url("https://forum.example.com/view?t=2")


@pytest.mark.parametrize(
    ("a", "b"),
    [
        ("https://example.com/caf%C3%A9", "https://example.com/café"),
        ("https://example.com/a%7Eb", "https://example.com/a~b"),
        ("https://example.com/docs/index.html", "https://example.com/docs/"),
        ("https://example.com/Index.HTM", "https://example.com/"),
    ],
)
def test_percent_encoding_and_index_pages_normalize(a: str, b: str) -> None:
    assert normalize_url(a) == normalize_url(b)


def test_an_encoded_slash_is_not_a_path_separator() -> None:
    assert normalize_url("https://example.com/a%2Fb") != normalize_url("https://example.com/a/b")


def test_different_pages_stay_different() -> None:
    assert normalize_url("https://example.com/a") != normalize_url("https://example.com/b")
    assert normalize_url("https://example.com/A") != normalize_url("https://example.com/a")  # paths are case sensitive
    assert normalize_url("https://example.com/a?id=1") != normalize_url("https://example.com/a?id=2")
    assert normalize_url("https://example.com:8080/a") != normalize_url("https://example.com/a")


def test_a_url_without_a_host_is_not_a_url() -> None:
    assert normalize_url("") is None
    assert normalize_url(None) is None
    assert normalize_url("   ") is None


def test_normalized_duplicates_count_once_and_top_n_is_respected() -> None:
    urls = ["https://www.a.com/x/", "http://a.com/x", "https://b.com", "https://c.com", "https://d.com"]
    assert top_urls(urls, 3) == ("a.com/x", "b.com", "c.com")


def test_tracking_variants_link_two_keywords_that_raw_urls_would_not() -> None:
    a = ["https://www.x.com/p/?utm_source=g", "https://y.com/q#top", "https://z.com/"]
    b = ["http://x.com/p", "https://y.com/q", "https://z.com?gclid=9"]
    result = cluster_keywords([_kw("a", a), _kw("b", b)], ClusterSettings(min_shared=3))
    assert _status(result, "a").status == "clustered"
    assert _status(result, "a").shared_count == 3


# ── identical and disjoint SERPs ──────────────────────────────────────────


def test_identical_serps_form_one_cluster_with_every_url_as_justification() -> None:
    same = _urls(*"abcdefghij")
    result = cluster_keywords([_kw("k1", same, 100), _kw("k2", same, 900)])
    assert len(result.clusters) == 1
    c1, c2 = _status(result, "k1"), _status(result, "k2")
    assert c1.cluster_id == c2.cluster_id == cluster_id_for(["k1", "k2"])
    assert c1.head_keyword_id == "k2"  # highest volume is the head
    assert c1.shared_count == 10 and c1.jaccard == 1.0
    assert list(c1.shared_urls) == [normalize_url(u) for u in same]
    assert c1.linked_to == "k2" and c2.linked_to == "k1"


def test_disjoint_serps_never_cluster() -> None:
    result = cluster_keywords([_kw("k1", _urls(*"abcdefghij")), _kw("k2", _urls(*"klmnopqrst"))])
    assert result.clusters == []
    assert {k.status for k in result.keywords} == {"alone"}
    assert pairwise_overlaps({"k1": top_urls(_urls(*"abc"), 10), "k2": top_urls(_urls(*"def"), 10)}) == []


# ── single link ───────────────────────────────────────────────────────────


def test_a_chain_joins_ends_that_share_nothing() -> None:
    # A–B share a,b,c; B–C share x,y,z; A and C share nothing.
    a = _urls("a", "b", "c", "a1", "a2")
    b = _urls("a", "b", "c", "x", "y", "z")
    c = _urls("x", "y", "z", "c1", "c2")
    result = cluster_keywords([_kw("A", a), _kw("B", b), _kw("C", c)])
    ids = {k.keyword_id: k.cluster_id for k in result.keywords}
    assert ids["A"] == ids["B"] == ids["C"] is not None
    assert result.clusters[0]["size"] == 3
    # A's justification is its link to B, never a fabricated link to C.
    assert _status(result, "A").linked_to == "B"
    assert _status(result, "C").linked_to == "B"


# ── the threshold knob ────────────────────────────────────────────────────


def test_count_threshold_decides_whether_two_shared_urls_link() -> None:
    a, b = _urls("s1", "s2", "a1", "a2"), _urls("s1", "s2", "b1", "b2")
    assert cluster_keywords([_kw("a", a), _kw("b", b)], ClusterSettings(min_shared=3)).clusters == []
    assert len(cluster_keywords([_kw("a", a), _kw("b", b)], ClusterSettings(min_shared=2)).clusters) == 1


def test_jaccard_mode_uses_the_jaccard_threshold_not_the_count() -> None:
    # 2 shared out of 6 distinct URLs → jaccard 0.3333.
    a, b = _urls("s1", "s2", "a1", "a2"), _urls("s1", "s2", "b1", "b2")
    low = ClusterSettings(mode="jaccard", min_jaccard=0.3, min_shared=99)
    high = ClusterSettings(mode="jaccard", min_jaccard=0.34, min_shared=1)
    linked = cluster_keywords([_kw("a", a), _kw("b", b)], low)
    assert len(linked.clusters) == 1
    assert _status(linked, "a").overlap_score == pytest.approx(0.3333, abs=1e-4)
    assert cluster_keywords([_kw("a", a), _kw("b", b)], high).clusters == []


def test_top_n_limits_which_urls_count() -> None:
    a = _urls("a1", "a2", "a3", "s1", "s2", "s3")
    b = _urls("b1", "b2", "b3", "s1", "s2", "s3")
    assert cluster_keywords([_kw("a", a), _kw("b", b)], ClusterSettings(top_n=3)).clusters == []
    assert len(cluster_keywords([_kw("a", a), _kw("b", b)], ClusterSettings(top_n=6)).clusters) == 1


# ── missing snapshots ─────────────────────────────────────────────────────


def test_a_keyword_without_a_stored_snapshot_is_reported_never_guessed() -> None:
    same = _urls(*"abcdef")
    result = cluster_keywords([_kw("k1", same), _kw("k2", same), _kw("none", None), _kw("empty", [])])
    none, empty = _status(result, "none"), _status(result, "empty")
    assert none.status == "not_clustered" and none.reason == NO_STORED_RESULTS and none.cluster_id is None
    assert empty.status == "not_clustered" and empty.reason == NO_ORGANIC_RESULTS
    assert result.clusters[0]["size"] == 2
    assert [k.keyword_id for k in result.keywords][-2:] in (["none", "empty"], ["empty", "none"])


# ── the max-size guard ────────────────────────────────────────────────────


def test_max_cluster_size_refuses_a_merge_and_says_so() -> None:
    same = _urls(*"abcdef")
    serps = [_kw(f"k{i}", same, volume=10 - i) for i in range(5)]
    result = cluster_keywords(serps, ClusterSettings(max_cluster_size=3))
    assert max(c["size"] for c in result.clusters) <= 3
    assert result.refused_links > 0
    assert any("largest-cluster setting" in n for n in result.notices)
    refused = [k for k in result.keywords if k.refused_links]
    assert refused, "a refused link is reported on the keywords it touched"
    alone = [k for k in result.keywords if k.status == "alone"]
    assert all(k.reason == "linking it would pass the largest cluster size" for k in alone)


def test_same_inputs_give_the_same_clusters_in_any_order() -> None:
    a = _urls("a", "b", "c", "d")
    b = _urls("a", "b", "c", "e")
    c = _urls("x", "y", "z", "w")
    d = _urls("x", "y", "z", "v")
    first = cluster_keywords([_kw("A", a), _kw("B", b), _kw("C", c), _kw("D", d)])
    second = cluster_keywords([_kw("D", d), _kw("C", c), _kw("B", b), _kw("A", a)])
    assert [k.as_dict() for k in first.keywords] == [k.as_dict() for k in second.keywords]
    assert first.clusters == second.clusters


def test_settings_are_validated() -> None:
    with pytest.raises(ValueError):
        cluster_keywords([], ClusterSettings(max_cluster_size=1))
