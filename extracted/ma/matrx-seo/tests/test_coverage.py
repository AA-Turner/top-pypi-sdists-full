"""Coverage pure logic — the doctrines pinned, not the happy path."""

from __future__ import annotations

from datetime import UTC, datetime

import pytest
from matrx_scraper.canonical import story_url_key

from matrx_seo.coverage import (
    CompetitorTerm,
    TrackerSpec,
    VoiceRow,
    classify_candidate,
    detect_medium,
    hit_score,
    mention_dedupe_key,
    share_of_voice,
)
from matrx_seo.providers.gdelt import build_query, parse_articles

NOW = datetime(2026, 8, 16, 12, 0, tzinfo=UTC)


def spec(**overrides) -> TrackerSpec:
    base = dict(
        tracker_id="t1",
        brand_key="ai-matrx",
        brand_terms=["AI Matrx", "aimatrx"],
        exclude_terms=[],
        competitors=[CompetitorTerm(key="zapier", terms=["Zapier"])],
        ignore_domains=["aimatrx.com"],
    )
    base.update(overrides)
    return TrackerSpec(**base)


# ── URL identity ─────────────────────────────────────────────────────────────


def test_story_url_key_strips_tracking_and_www_so_one_story_files_once():
    a = story_url_key("https://www.Example.com/story/?utm_source=x&id=7")
    b = story_url_key("http://example.com/story?id=7")
    assert a == b == "https://example.com/story?id=7"


def test_story_url_key_refuses_a_hostless_string_rather_than_inventing_one():
    with pytest.raises(ValueError):
        story_url_key("   ")


def test_a_mention_is_keyed_on_the_platforms_one_article_key():
    """The mention's normalized_url IS the story key a news sighting carries, so a coverage
    mention and a news sighting of the same article always agree (NEWS-ENGINE-SPEC §4.1)."""
    raw = "https://www.Example.com/story/?utm_source=x&id=7&fbclid=q"
    candidate = classify_candidate(
        spec(), url=raw, title="AI Matrx ships", source="gdelt", discovered_at=NOW
    )
    assert candidate is not None
    assert candidate.normalized_url == story_url_key(raw)
    assert candidate.domain == "example.com"


def test_dedupe_key_is_per_tracker_so_two_trackers_may_both_hold_one_article():
    url = story_url_key("https://example.com/story")
    assert mention_dedupe_key("t1", url) != mention_dedupe_key("t2", url)
    assert mention_dedupe_key("t1", url) == mention_dedupe_key("t1", url)


# ── Classification ───────────────────────────────────────────────────────────


def test_a_brand_hit_is_ours_even_when_a_competitor_is_also_named():
    candidate = classify_candidate(
        spec(),
        url="https://news.example.com/roundup",
        title="Zapier and AI Matrx both shipped this week",
        source="gdelt",
        discovered_at=NOW,
    )
    assert candidate is not None
    assert candidate.is_competitor is False
    assert candidate.competitor_key is None


def test_a_competitor_only_hit_lands_on_the_competitor_side():
    candidate = classify_candidate(
        spec(),
        url="https://news.example.com/zapier-raises",
        title="Zapier raises a round",
        source="gdelt",
        discovered_at=NOW,
    )
    assert candidate is not None and candidate.is_competitor
    assert candidate.competitor_key == "zapier"


def test_no_matching_term_is_silence_not_a_low_confidence_row():
    assert (
        classify_candidate(
            spec(),
            url="https://news.example.com/weather",
            title="It rained today",
            source="gdelt",
            discovered_at=NOW,
        )
        is None
    )


def test_a_term_matches_whole_words_only_so_arman_never_matches_armani():
    """Live 2026-09-29: a founder-name term turned Giorgio Armani stories into brand coverage."""
    armani = dict(
        url="https://tribune.com.pk/story/armani-unveils-shimmering-collection",
        title="Armani unveils shimmering collection in pursuit of 'evolution'",
        source="gdelt",
        discovered_at=NOW,
    )
    assert classify_candidate(spec(brand_terms=["Arman"], competitors=[]), **armani) is None
    assert classify_candidate(spec(brand_terms=["Green"], competitors=[]),
                              url="https://x.example/a", title="Greenpeace sues", source="gdelt",
                              discovered_at=NOW) is None
    hit = classify_candidate(spec(brand_terms=["arman sadeghi"], competitors=[]),
                             url="https://x.example/b", title="Arman  Sadeghi, founder, speaks",
                             source="gdelt", discovered_at=NOW)
    assert hit is not None and hit.matched_terms == ["arman sadeghi"]


def test_share_of_voice_counts_only_real_mentions():
    rows = [
        VoiceRow(is_competitor=False, verdict="passing_mention", hit_score=27),
        VoiceRow(is_competitor=False, verdict="wrong_entity", hit_score=27),  # Giorgio Armani
        VoiceRow(is_competitor=False, verdict="junk"),  # "Access Denied"
        VoiceRow(is_competitor=False, verdict="uncertain"),  # could not read the page
        VoiceRow(is_competitor=True, competitor_key="rival"),
    ]
    result = share_of_voice(rows, brand_key="b")
    assert result.total_mentions == 2
    assert result.brand_share_pct == 50.0
    assert next(e for e in result.entries if e.is_brand).mentions == 1


def test_the_brands_own_domain_is_never_coverage():
    assert (
        classify_candidate(
            spec(),
            url="https://www.aimatrx.com/blog/we-are-great",
            title="AI Matrx announces something",
            source="gdelt",
            discovered_at=NOW,
        )
        is None
    )


def test_an_exclude_term_declines_the_whole_candidate():
    assert (
        classify_candidate(
            spec(exclude_terms=["job posting"]),
            url="https://jobs.example.com/x",
            title="AI Matrx job posting: engineer",
            source="gdelt",
            discovered_at=NOW,
        )
        is None
    )


def test_podcasts_and_newsletters_are_detected_from_url_and_title_only():
    assert detect_medium("https://podcasts.apple.com/us/podcast/x/id1") == "podcast"
    assert detect_medium("https://someone.substack.com/p/issue-12") == "newsletter"
    assert detect_medium("https://news.example.com/story") == "news"


# ── Hit score ────────────────────────────────────────────────────────────────


def test_unmeasured_inputs_score_zero_points_and_never_a_midpoint_guess():
    unread = hit_score(prominence=None, sentiment=None, links_to_site=False)
    assert unread.score == 0
    assert "not read the page yet" in unread.reason


def test_headline_positive_and_linked_outscores_a_buried_neutral_mention():
    strong = hit_score(prominence="headline", sentiment="positive", links_to_site=True)
    weak = hit_score(prominence="passing", sentiment="neutral", links_to_site=False)
    assert strong.score > weak.score
    assert strong.components["links_to_site"] == 20


def test_hit_score_is_bounded_and_explains_itself():
    top = hit_score(prominence="headline", sentiment="positive", links_to_site=True, authority=100)
    assert top.score == 100
    assert top.reason.startswith("Scored 100 of 100 because")


# ── Share of voice ───────────────────────────────────────────────────────────


def test_share_of_voice_splits_brand_and_competitors_over_one_window():
    rows = [
        VoiceRow(is_competitor=False, links_to_site=True, hit_score=80),
        VoiceRow(is_competitor=False, hit_score=40),
        VoiceRow(is_competitor=True, competitor_key="zapier", hit_score=50),
        VoiceRow(is_competitor=True, competitor_key="n8n"),
    ]
    result = share_of_voice(rows, brand_key="ai-matrx")
    assert result.total_mentions == 4
    assert result.brand_share_pct == 50.0
    brand = result.entries[0]
    assert brand.is_brand and brand.mentions == 2 and brand.linked_mentions == 1
    assert brand.avg_hit_score == 60


def test_share_of_voice_with_no_mentions_is_zero_not_a_crash():
    result = share_of_voice([], brand_key="ai-matrx")
    assert result.total_mentions == 0 and result.brand_share_pct == 0.0


# ── GDELT query + parsing ────────────────────────────────────────────────────


def test_multi_word_terms_are_quoted_so_a_brand_search_does_not_widen():
    query = build_query(terms=["AI Matrx", "aimatrx"], exclude_terms=["job posting"])
    assert '"AI Matrx"' in query and "aimatrx" in query and " OR " in query
    assert '-"job posting"' in query


def test_a_query_with_no_terms_is_refused():
    with pytest.raises(ValueError):
        build_query(terms=[])


def test_parse_articles_ignores_junk_entries_instead_of_raising():
    parsed = parse_articles(
        {
            "articles": [
                {
                    "url": "https://example.com/a",
                    "title": "A",
                    "domain": "example.com",
                    "seendate": "20260816T031500Z",
                },
                {"title": "no url"},
                "not-a-dict",
            ]
        }
    )
    assert len(parsed) == 1
    assert parsed[0].seen_at == datetime(2026, 8, 16, 3, 15, tzinfo=UTC)


def test_parse_articles_on_a_shapeless_payload_is_empty_not_an_exception():
    assert parse_articles({"error": "bad query"}) == []
    assert parse_articles(None) == []


# ── The double-filter defect (found on the first live pass) ──────────────────


def test_a_source_matched_article_is_kept_even_when_the_headline_omits_the_term():
    """GDELT matches the FULL article; re-demanding the term in the headline
    discarded ten real stories on the first live run."""
    from matrx_seo.coverage import SourceMatch

    candidate = classify_candidate(
        spec(),
        url="https://news.example.com/enterprise-roundup",
        title="Six platforms worth watching this year",  # brand named in paragraph 3
        source="gdelt",
        discovered_at=NOW,
        source_matched=SourceMatch(terms=["AI Matrx", "aimatrx"]),
    )
    assert candidate is not None
    assert candidate.is_competitor is False
    assert candidate.matched_terms == ["AI Matrx", "aimatrx"]


def test_a_source_matched_competitor_query_lands_on_the_competitor_side():
    from matrx_seo.coverage import SourceMatch

    candidate = classify_candidate(
        spec(),
        url="https://news.example.com/automation-roundup",
        title="Automation tools worth watching",
        source="gdelt",
        discovered_at=NOW,
        source_matched=SourceMatch(terms=["Zapier"], competitor_key="zapier"),
    )
    assert candidate is not None and candidate.is_competitor
    assert candidate.competitor_key == "zapier"


def test_a_local_headline_hit_still_wins_over_the_source_side():
    """An article the rival's query returned, whose headline names US, is ours."""
    from matrx_seo.coverage import SourceMatch

    candidate = classify_candidate(
        spec(),
        url="https://news.example.com/x",
        title="AI Matrx takes on Zapier",
        source="gdelt",
        discovered_at=NOW,
        source_matched=SourceMatch(terms=["Zapier"], competitor_key="zapier"),
    )
    assert candidate is not None and candidate.is_competitor is False


def test_exclusions_and_the_ignore_list_still_win_over_a_source_match():
    from matrx_seo.coverage import SourceMatch

    assert (
        classify_candidate(
            spec(exclude_terms=["job posting"]),
            url="https://jobs.example.com/x",
            title="Engineer — job posting",
            source="gdelt",
            discovered_at=NOW,
            source_matched=SourceMatch(terms=["AI Matrx"]),
        )
        is None
    )
    assert (
        classify_candidate(
            spec(),
            url="https://aimatrx.com/blog/post",
            title="Anything",
            source="gdelt",
            discovered_at=NOW,
            source_matched=SourceMatch(terms=["AI Matrx"]),
        )
        is None
    )


def test_without_a_source_match_the_strict_local_rule_still_applies():
    """A pasted URL has been filtered by nothing, so nothing is assumed."""
    assert (
        classify_candidate(
            spec(),
            url="https://news.example.com/unrelated",
            title="Something else entirely",
            source="manual",
            discovered_at=NOW,
        )
        is None
    )
