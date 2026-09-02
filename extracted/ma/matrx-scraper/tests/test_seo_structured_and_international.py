"""Structured-data and international checks — pure logic, no DB, no network.

These five catalogue items were the rare case where the CAPTURE was already
richer than anything reading it: `web.snapshot.structured_data` has kept every
parsed JSON-LD document, every original script string INCLUDING the malformed
ones, and the parse error each one produced, since the crawler was written.
The tests below are written against that stored payload on purpose —
`test_malformed_json_ld_uses_the_persisted_parse_errors` fails the moment a
check starts re-parsing HTML instead of reading what the capture stored.

Per-page (`seo_audit`): structured_data_validity, hreflang_validity.
Cross-page (`web_crawl.analysis`): local_business_markup, hreflang_reciprocity —
both need the whole site, and reciprocity often needs a site we do not have.
"""

from __future__ import annotations

import json

import pytest

from matrx_scraper.seo_audit import (
    BUSINESS_MISSING_CORE_FAIL_COUNT,
    CheckOutcome,
    audit_html,
    business_entities_in,
    check_hreflang_validity,
    check_structured_data_validity,
    evidence_from_audit,
    is_valid_hreflang_value,
    normalized_url_key,
)
from matrx_scraper.web_crawl.analysis import (
    PageFacts,
    SiteAggregates,
    _check_hreflang_reciprocity,
    _check_local_business_markup,
    index_page_facts,
)


def assert_db_valid(outcome: CheckOutcome) -> None:
    """Mirror of analysis_result_status_score_valid + status_valid."""
    assert outcome.status in ("pass", "warn", "fail", "n_a")
    if outcome.status in ("pass", "warn", "fail"):
        assert outcome.score is not None and 1 <= outcome.score <= 100
    else:
        assert outcome.score is None
    assert outcome.reasoning


def page_with_json_ld(*documents: str, url: str = "https://example.com/a") -> PageFacts:
    """A page whose evidence came through the REAL capture path.

    `audit_html` → `evidence_from_audit` is exactly what a live one-shot audit
    runs, and `structured_data` is the same payload the crawler persists onto
    `web.snapshot.structured_data`.
    """
    scripts = "".join(f'<script type="application/ld+json">{doc}</script>' for doc in documents)
    audit = audit_html(f"<html lang='en'><head>{scripts}</head><body><p>x</p></body></html>", url)
    evidence = evidence_from_audit(audit, http_status=200)
    return PageFacts(
        page_id=url,
        latest_snapshot_id=f"snap:{url}",
        **{
            field: getattr(evidence, field)
            for field in evidence.__dataclass_fields__
            if field != "url"
        },
        url=url,
    )


def facts_with_hreflang(
    url: str, pairs: list[tuple[str, str]], *, canonical: str | None = None
) -> PageFacts:
    return PageFacts(
        page_id=url,
        url=url,
        canonical_url=canonical,
        hreflang=[{"lang": lang, "href": href} for lang, href in pairs],
    )


def aggregates_for(*facts: PageFacts) -> SiteAggregates:
    """Site aggregates built by the PRODUCTION indexer, never by hand."""
    site = SiteAggregates()
    index_page_facts(list(facts), site)
    return site


# ---------------------------------------------------------------------------
# structured_data_validity


VALID_PRODUCT = json.dumps(
    {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": "Merino Runner",
        "image": "https://example.com/shoe.png",
        "description": "A shoe.",
        "brand": {"@type": "Brand", "name": "Example"},
        "sku": "MR-1",
        "aggregateRating": {"@type": "AggregateRating", "ratingValue": "4.5"},
        "offers": {"@type": "Offer", "price": "129.00", "priceCurrency": "USD"},
    }
)

MALFORMED_JSON_LD = '{"@context": "https://schema.org", "@type": "Product", "name": '


def test_malformed_json_ld_uses_the_persisted_parse_errors():
    """The capture already recorded WHY the script failed — use that, don't re-parse."""
    facts = page_with_json_ld(MALFORMED_JSON_LD)

    # The evidence the check reads: the broken script is kept VERBATIM next to
    # the error it produced. This is the payload the crawler persists.
    assert facts.structured_data["parse_errors"], "capture lost the parse error"
    assert facts.structured_data["json_ld_raw"] == [MALFORMED_JSON_LD.strip()]
    assert facts.structured_data["json_ld"] == []

    outcome = check_structured_data_validity(facts)
    assert_db_valid(outcome)
    assert outcome.status == "fail" and outcome.score == 30
    assert outcome.issue_count == 1
    reported = outcome.evidence["parse_errors"][0]
    assert reported["source"] == "json-ld"
    assert "JSONDecodeError" in reported["message"]
    # The user is shown WHICH script broke, quoted from the stored original.
    assert reported["script"].startswith('{"@context"')


def test_a_parse_error_outranks_every_property_problem():
    """One unreadable script voids the page's markup — it is reported first."""
    incomplete_event = json.dumps({"@context": "https://schema.org", "@type": "Event"})
    outcome = check_structured_data_validity(page_with_json_ld(MALFORMED_JSON_LD, incomplete_event))
    assert outcome.status == "fail" and outcome.score == 30


def test_a_complete_rich_result_type_passes():
    outcome = check_structured_data_validity(page_with_json_ld(VALID_PRODUCT))
    assert_db_valid(outcome)
    assert outcome.status == "pass" and outcome.score == 100
    assert "Product" in outcome.reasoning


def test_missing_required_properties_fail_and_missing_recommended_only_warn():
    no_offers = json.dumps(
        {"@context": "https://schema.org", "@type": "Product", "name": "Merino Runner"}
    )
    required = check_structured_data_validity(page_with_json_ld(no_offers))
    assert_db_valid(required)
    assert required.status == "fail" and required.score == 50
    assert required.evidence["missing_required"][0]["type"] == "Product"
    assert "offers" in required.evidence["missing_required"][0]["missing"]

    bare = json.dumps(
        {
            "@context": "https://schema.org",
            "@type": "Product",
            "name": "Merino Runner",
            "offers": {"@type": "Offer", "price": "129.00"},
        }
    )
    recommended = check_structured_data_validity(page_with_json_ld(bare))
    assert_db_valid(recommended)
    assert recommended.status == "warn" and recommended.score == 75
    assert "image" in recommended.evidence["missing_recommended"][0]["missing"]


def test_an_accepted_alias_spelling_is_not_a_missing_property():
    """`aggregateRating` satisfies Product's offer requirement; `phone` is a telephone."""
    with_rating = json.dumps(
        {
            "@context": "https://schema.org",
            "@type": "Product",
            "name": "Merino Runner",
            "image": "https://example.com/s.png",
            "description": "A shoe.",
            "brand": "Example",
            "sku": "MR-1",
            "aggregateRating": {"@type": "AggregateRating", "ratingValue": "4.5"},
        }
    )
    assert check_structured_data_validity(page_with_json_ld(with_rating)).status == "pass"


def test_markup_with_no_rich_result_contract_still_passes_when_it_parses():
    other = json.dumps({"@context": "https://schema.org", "@type": "WebSite", "name": "Example"})
    outcome = check_structured_data_validity(page_with_json_ld(other))
    assert outcome.status == "pass" and outcome.score == 100


def test_absent_markup_is_na_and_absent_capture_offers_a_remediation():
    no_markup = check_structured_data_validity(page_with_json_ld())
    assert_db_valid(no_markup)
    assert no_markup.status == "n_a" and no_markup.remediation is None

    never_captured = check_structured_data_validity(PageFacts(page_id="p", url="https://x.test/a"))
    assert_db_valid(never_captured)
    assert never_captured.status == "n_a"
    assert never_captured.remediation is not None, "missing evidence needs a one-click fix"


# ---------------------------------------------------------------------------
# hreflang_validity


def test_a_valid_hreflang_set_passes():
    facts = facts_with_hreflang(
        "https://example.com/en/",
        [
            ("en", "https://example.com/en/"),
            ("fr", "https://example.com/fr/"),
            ("x-default", "https://example.com/en/"),
        ],
        canonical="https://example.com/en/",
    )
    outcome = check_hreflang_validity(facts)
    assert_db_valid(outcome)
    assert outcome.status == "pass" and outcome.score == 100


@pytest.mark.parametrize(
    ("pairs", "canonical", "status", "score"),
    [
        # invalid language code — breaks the cluster for every page in it
        (
            [("en", "https://example.com/en/"), ("english", "https://example.com/e/")],
            None,
            "fail",
            30,
        ),
        # relative URL
        ([("en", "https://example.com/en/"), ("fr", "/fr/")], None, "fail", 30),
        # no self-reference
        ([("fr", "https://example.com/fr/")], None, "fail", 45),
        # self-reference disagrees with the canonical
        (
            [("en", "https://example.com/en/"), ("fr", "https://example.com/fr/")],
            "https://example.com/en/index.html",
            "fail",
            40,
        ),
        # everything valid, only x-default absent
        (
            [("en", "https://example.com/en/"), ("fr", "https://example.com/fr/")],
            "https://example.com/en/",
            "warn",
            80,
        ),
    ],
)
def test_hreflang_validity_reports_the_catalogue_rules_in_order(pairs, canonical, status, score):
    outcome = check_hreflang_validity(
        facts_with_hreflang("https://example.com/en/", pairs, canonical=canonical)
    )
    assert_db_valid(outcome)
    assert (outcome.status, outcome.score) == (status, score)


def test_no_hreflang_is_na_not_a_pass():
    outcome = check_hreflang_validity(PageFacts(page_id="p", url="https://example.com/a"))
    assert_db_valid(outcome)
    assert outcome.status == "n_a"


def test_x_default_is_the_only_non_language_hreflang_value():
    assert is_valid_hreflang_value("x-default")
    assert is_valid_hreflang_value("zh-Hant-TW")
    assert is_valid_hreflang_value("en-GB")
    assert not is_valid_hreflang_value("x-mine")
    assert not is_valid_hreflang_value("english")
    assert not is_valid_hreflang_value("")


def test_url_matching_ignores_only_the_cosmetic_differences():
    assert normalized_url_key("https://WWW.Example.com/en/") == normalized_url_key(
        "http://example.com/en"
    )
    assert normalized_url_key("https://example.com/en/#top") == normalized_url_key(
        "https://example.com/en/"
    )
    assert normalized_url_key("https://example.com/en/") != normalized_url_key(
        "https://example.com/fr/"
    )


# ---------------------------------------------------------------------------
# hreflang_reciprocity (CROSS-PAGE)


def test_a_reciprocal_pair_on_this_site_passes():
    en = facts_with_hreflang(
        "https://example.com/en/",
        [("en", "https://example.com/en/"), ("fr", "https://example.com/fr/")],
    )
    fr = facts_with_hreflang(
        "https://example.com/fr/",
        [("en", "https://example.com/en/"), ("fr", "https://example.com/fr/")],
    )
    site = aggregates_for(en, fr)
    for facts in (en, fr):
        outcome = _check_hreflang_reciprocity(facts, site)
        assert_db_valid(outcome)
        assert outcome.status == "pass" and outcome.score == 100


def test_a_one_way_annotation_fails_with_the_return_tag_named():
    en = facts_with_hreflang(
        "https://example.com/en/",
        [("en", "https://example.com/en/"), ("fr", "https://example.com/fr/")],
    )
    # The French page was crawled and declares NO hreflang at all — the classic
    # half-built cluster.
    fr = facts_with_hreflang("https://example.com/fr/", [])
    site = aggregates_for(en, fr)

    outcome = _check_hreflang_reciprocity(en, site)
    assert_db_valid(outcome)
    assert outcome.status == "fail" and outcome.score == 1
    assert outcome.issue_count == 1
    assert outcome.evidence["missing_return_tags"] == ["https://example.com/fr/"]

    # …and the page that declares nothing is not blamed for it.
    assert _check_hreflang_reciprocity(fr, site).status == "n_a"


def test_a_partially_reciprocal_set_scores_the_share_that_returns():
    en = facts_with_hreflang(
        "https://example.com/en/",
        [
            ("en", "https://example.com/en/"),
            ("fr", "https://example.com/fr/"),
            ("de", "https://example.com/de/"),
        ],
    )
    fr = facts_with_hreflang("https://example.com/fr/", [("en", "https://example.com/en/")])
    de = facts_with_hreflang("https://example.com/de/", [])
    outcome = _check_hreflang_reciprocity(en, aggregates_for(en, fr, de))
    assert_db_valid(outcome)
    assert outcome.score == 50 and outcome.status == "warn"


def test_a_cross_site_cluster_is_na_never_a_failure():
    """example.de cannot be checked from example.com's crawl — say so."""
    com = facts_with_hreflang(
        "https://example.com/",
        [
            ("en-US", "https://example.com/"),
            ("de-DE", "https://example.de/"),
            ("fr-FR", "https://example.fr/"),
        ],
    )
    outcome = _check_hreflang_reciprocity(com, aggregates_for(com))
    assert_db_valid(outcome)
    assert outcome.status == "n_a" and outcome.score is None
    assert set(outcome.evidence["unverified_targets"]) == {
        "https://example.de/",
        "https://example.fr/",
    }
    assert "other domains" in outcome.reasoning


def test_off_site_targets_never_dilute_the_on_site_verdict():
    en = facts_with_hreflang(
        "https://example.com/en/",
        [
            ("en", "https://example.com/en/"),
            ("fr", "https://example.com/fr/"),
            ("de-DE", "https://example.de/"),
        ],
    )
    fr = facts_with_hreflang(
        "https://example.com/fr/",
        [("en", "https://example.com/en/"), ("fr", "https://example.com/fr/")],
    )
    outcome = _check_hreflang_reciprocity(en, aggregates_for(en, fr))
    assert outcome.status == "pass" and outcome.score == 100
    assert "not cover" in outcome.reasoning


def test_an_uncrawled_same_site_target_is_unverified_not_broken():
    en = facts_with_hreflang(
        "https://example.com/en/",
        [("en", "https://example.com/en/"), ("fr", "https://example.com/fr/")],
    )
    outcome = _check_hreflang_reciprocity(en, aggregates_for(en))
    assert_db_valid(outcome)
    assert outcome.status == "n_a"
    assert outcome.remediation is not None


def test_a_self_reference_only_set_has_nothing_to_return():
    facts = facts_with_hreflang("https://example.com/en/", [("en", "https://example.com/en/")])
    outcome = _check_hreflang_reciprocity(facts, aggregates_for(facts))
    assert outcome.status == "pass" and outcome.score == 100


# ---------------------------------------------------------------------------
# local_business_markup (CROSS-PAGE, site-level)


def _business(**overrides) -> str:
    entity = {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "name": "Example Dental",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "1 Example Way",
            "addressLocality": "Austin",
            "addressRegion": "TX",
            "postalCode": "78701",
        },
        "telephone": "+1-512-555-0100",
        "geo": {"@type": "GeoCoordinates", "latitude": "30.27", "longitude": "-97.74"},
        "openingHours": "Mo-Fr 09:00-17:00",
        "sameAs": ["https://example.com/"],
    }
    entity.update(overrides)
    for key, value in list(entity.items()):
        if value is None:
            del entity[key]
    return json.dumps(entity)


def test_a_complete_consistent_business_entity_passes():
    home = page_with_json_ld(_business(), url="https://example.com/")
    contact = page_with_json_ld(_business(), url="https://example.com/contact")
    site = aggregates_for(home, contact)
    outcome = _check_local_business_markup(home, site)
    assert_db_valid(outcome)
    assert outcome.status == "pass" and outcome.score == 100


def test_no_business_markup_anywhere_on_the_site():
    plain = page_with_json_ld(
        json.dumps({"@context": "https://schema.org", "@type": "WebPage", "name": "Home"}),
        url="https://example.com/",
    )
    outcome = _check_local_business_markup(plain, aggregates_for(plain))
    assert_db_valid(outcome)
    assert outcome.status == "warn" and outcome.score == 50


def test_missing_two_core_nap_properties_is_incomplete_markup():
    stub = page_with_json_ld(_business(address=None, telephone=None), url="https://example.com/")
    outcome = _check_local_business_markup(stub, aggregates_for(stub))
    assert_db_valid(outcome)
    assert outcome.status == "warn" and outcome.score == 65
    assert len(outcome.evidence["missing"]) >= BUSINESS_MISSING_CORE_FAIL_COUNT


def test_the_most_complete_declaration_speaks_for_the_site():
    """A stub entity on one page must not condemn the full one on another."""
    home = page_with_json_ld(_business(), url="https://example.com/")
    stub = page_with_json_ld(
        json.dumps(
            {"@context": "https://schema.org", "@type": "Organization", "name": "Example Dental"}
        ),
        url="https://example.com/blog",
    )
    assert _check_local_business_markup(home, aggregates_for(home, stub)).status == "pass"


def test_conflicting_nap_values_across_pages_are_reported():
    home = page_with_json_ld(_business(), url="https://example.com/")
    contact = page_with_json_ld(
        _business(telephone="+1-512-555-0199"), url="https://example.com/contact"
    )
    outcome = _check_local_business_markup(home, aggregates_for(home, contact))
    assert_db_valid(outcome)
    assert outcome.status == "warn" and outcome.score == 55
    assert "telephone" in outcome.evidence["conflicting_values"]


def test_the_same_phone_written_differently_is_not_a_conflict():
    home = page_with_json_ld(_business(), url="https://example.com/")
    contact = page_with_json_ld(
        _business(telephone="+1-512-555-0100 "), url="https://example.com/contact"
    )
    assert _check_local_business_markup(home, aggregates_for(home, contact)).status == "pass"


def test_no_structured_data_captured_anywhere_is_na():
    blank = PageFacts(page_id="p", url="https://example.com/")
    outcome = _check_local_business_markup(blank, aggregates_for(blank))
    assert_db_valid(outcome)
    assert outcome.status == "n_a"
    assert outcome.remediation is not None


def test_local_business_subtypes_count_as_business_markup():
    entities = business_entities_in(
        page_with_json_ld(_business(**{"@type": "Restaurant"})).structured_data
    )
    assert entities and "Restaurant" in entities[0]["types"]
    assert entities[0]["name"] == "example dental"
