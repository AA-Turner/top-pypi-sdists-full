"""The deterministic competitor-classification layer.

These pin the rules that Arman's 2026-08-14 ruling turned into a schema, using
the REAL domains our production data returned as "competitors" for
datadestruction.com — the live evidence that a single flat competitor list is
wrong (common-docs/systems/marketing/competitor-classification/FEATURE.md §2).
"""

from __future__ import annotations

import pytest

from matrx_seo.competitor_classification import (
    DomainRule,
    DomainRuleset,
    classify_entity_role,
    default_posture,
    default_use_for_link_gap,
    derive_label,
    search_overlap_band,
)


#: A miniature stand-in for ``platform.domain_classification``. The real ruleset
#: is 166 live rows and growing; these are the exact patterns whose behaviour the
#: matching logic must guarantee, written in the registry's own two shapes.
REGISTRY = DomainRuleset(
    [
        DomainRule("wikipedia.org", "domain", "reference", "Encyclopedic."),
        DomainRule("ieee.org", "domain", "reference", "Standards body."),
        DomainRule("theconversation.com", "domain", "publisher", "Editorial."),
        DomainRule("lifewire.com", "domain", "publisher", "Editorial."),
        DomainRule("realself.com", "domain", "marketplace", "Sells your customers back to you."),
        DomainRule("yelp.com", "domain", "marketplace", "Directory."),
        DomainRule("forbes.com", "domain", "publisher", "Editorial."),
        DomainRule("reddit.com", "domain", "community", "User-generated."),
        DomainRule("carrier.com", "domain", "manufacturer", "OEM."),
        DomainRule(".gov", "suffix", "reference", "Government."),
        DomainRule(".edu", "suffix", "reference", "Academic."),
        DomainRule(".ac.uk", "suffix", "reference", "Academic."),
    ]
)


class TestDeterministicRole:
    @pytest.mark.parametrize(
        ("domain", "expected"),
        [
            # Every one of these was returned as a "competitor" for
            # datadestruction.com by /backlinks/competitors in production.
            ("ieee.org", "reference"),
            ("nist.gov", "reference"),
            ("theconversation.com", "publisher"),
            ("lifewire.com", "publisher"),
            # Arman's medspa example.
            ("realself.com", "marketplace"),
            ("reddit.com", "community"),
            ("en.wikipedia.org", "reference"),
            ("www.yelp.com", "marketplace"),
            ("https://forbes.com/some/article", "publisher"),
            ("epa.gov", "reference"),
            ("mit.edu", "reference"),
            ("cam.ac.uk", "reference"),
            # A role the original 8-value taxonomy had no name for (§3a Finding 4).
            ("carrier.com", "manufacturer"),
        ],
    )
    def test_known_non_competitors_are_settled_without_ai(self, domain, expected):
        verdict = classify_entity_role(domain, REGISTRY)
        assert verdict is not None, f"{domain} should not have needed an AI call"
        assert verdict.entity_role == expected
        # A proposal a human cannot evaluate is one they will rubber-stamp.
        assert verdict.reason.strip()
        assert verdict.rule.strip()

    @pytest.mark.parametrize(
        "domain",
        [
            # Real businesses — the deterministic layer must DECLINE, not guess.
            "shredit.com",
            "shrednations.com",
            "securis.com",
            "blancco.com",
            "allgreenrecycling.com",
            "some-local-medspa.com",
        ],
    )
    def test_real_companies_are_handed_to_the_ai_layer(self, domain):
        assert classify_entity_role(domain, REGISTRY) is None

    def test_blank_input_declines_rather_than_raising(self):
        assert classify_entity_role("", REGISTRY) is None
        assert classify_entity_role("   ", REGISTRY) is None

    def test_an_empty_registry_declines_everything(self):
        """The safe failure. No rules loaded means every candidate reaches the AI
        layer — the pre-registry behaviour, never a wrong label."""
        assert classify_entity_role("wikipedia.org", DomainRuleset([])) is None

    def test_an_org_row_overrides_the_system_row(self):
        """FEATURE.md §3 Axis 4: entity_role is a property of the RELATIONSHIP.
        Lennox competes with Carrier; the platform default calls Carrier a
        manufacturer, and Lennox's own row must win."""
        ruleset = DomainRuleset(
            [
                DomainRule("carrier.com", "domain", "manufacturer", "OEM.", source="system"),
                DomainRule(
                    "carrier.com",
                    "domain",
                    "business",
                    "They are our head-to-head rival.",
                    source="org",
                    is_org_override=True,
                ),
            ]
        )
        verdict = classify_entity_role("carrier.com", ruleset)
        assert verdict is not None
        assert verdict.entity_role == "business"
        assert "your organization" in verdict.reason

    def test_the_org_row_wins_regardless_of_load_order(self):
        ruleset = DomainRuleset(
            [
                DomainRule(
                    "carrier.com",
                    "domain",
                    "business",
                    "Ours.",
                    is_org_override=True,
                ),
                DomainRule("carrier.com", "domain", "manufacturer", "OEM."),
            ]
        )
        verdict = classify_entity_role("carrier.com", ruleset)
        assert verdict is not None and verdict.entity_role == "business"

    def test_the_longer_suffix_wins(self):
        ruleset = DomainRuleset(
            [
                DomainRule(".uk", "suffix", "irrelevant", "Country code."),
                DomainRule(".ac.uk", "suffix", "reference", "Academic."),
            ]
        )
        verdict = classify_entity_role("cam.ac.uk", ruleset)
        assert verdict is not None and verdict.entity_role == "reference"

    def test_an_exact_domain_beats_a_suffix(self):
        """A .gov that is genuinely a business to someone stays classifiable."""
        ruleset = DomainRuleset(
            [
                DomainRule(".gov", "suffix", "reference", "Government."),
                DomainRule("recycling.gov", "domain", "business", "They sell what we sell."),
            ]
        )
        verdict = classify_entity_role("recycling.gov", ruleset)
        assert verdict is not None and verdict.entity_role == "business"

    def test_a_lookalike_domain_does_not_match(self):
        """``notwikipedia.org`` is not a subdomain of ``wikipedia.org``."""
        assert classify_entity_role("notwikipedia.org", REGISTRY) is None


class TestDerivedLabel:
    def test_the_forty_five_minute_medspa_is_not_a_direct_competitor(self):
        """Arman's case: same business, out of reach. The whole reason business
        overlap and market overlap are separate axes."""
        assert (
            derive_label(
                business_overlap="direct",
                market_overlap="different_market",
                entity_role="business",
            )
            == "Out-of-market peer"
        )

    def test_the_same_business_in_range_is_a_direct_competitor(self):
        assert (
            derive_label(
                business_overlap="direct",
                market_overlap="same_market",
                entity_role="business",
            )
            == "Direct competitor"
        )

    def test_the_plastic_surgeon_is_adjacent_not_direct(self):
        """Different industry, same reach — takes revenue, sells something else."""
        assert (
            derive_label(
                business_overlap="adjacent",
                market_overlap="same_market",
                entity_role="business",
            )
            == "Adjacent competitor"
        )

    def test_realself_is_a_marketplace_whatever_its_search_overlap(self):
        assert (
            derive_label(
                business_overlap="none",
                market_overlap="market_agnostic",
                entity_role="marketplace",
                search_overlap_band="dominant",
            )
            == "Marketplace / lead broker"
        )

    def test_a_business_that_only_takes_the_serp_is_labelled_as_such(self):
        assert (
            derive_label(
                business_overlap="none",
                market_overlap="market_agnostic",
                entity_role="business",
                search_overlap_band="strong",
            )
            == "Search-only competitor"
        )

    def test_unset_axes_do_not_produce_a_confident_wrong_label(self):
        assert (
            derive_label(business_overlap=None, market_overlap=None, entity_role=None)
            == "Unclassified"
        )


class TestLinkGapSeeding:
    def test_out_of_market_peers_are_the_best_seed_in_the_system(self):
        """The non-obvious result the geography axis unlocks: same industry, same
        linkers, zero competitive risk. FEATURE.md §5."""
        assert default_use_for_link_gap(business_overlap="direct", entity_role="business")

    def test_chasing_wikipedias_linkers_is_worthless(self):
        for role in ("reference", "community", "marketplace", "publisher"):
            assert not default_use_for_link_gap(business_overlap="direct", entity_role=role), (
                f"{role} must never seed a paid gap run"
            )

    def test_a_pure_search_competitor_does_not_seed(self):
        assert not default_use_for_link_gap(business_overlap="none", entity_role="business")

    def test_an_unclassified_competitor_never_seeds_by_default(self):
        """Nothing spends money until something has actually been decided."""
        assert not default_use_for_link_gap(business_overlap=None, entity_role=None)
        assert not default_use_for_link_gap(business_overlap="direct", entity_role=None)


class TestPosture:
    def test_out_of_market_peers_default_to_copy_not_compete(self):
        assert (
            default_posture(
                business_overlap="direct",
                market_overlap="different_market",
                entity_role="business",
            )
            == "copy"
        )

    def test_in_market_rivals_default_to_compete(self):
        assert (
            default_posture(
                business_overlap="direct",
                market_overlap="same_market",
                entity_role="business",
            )
            == "compete"
        )

    def test_publishers_default_to_outreach(self):
        assert (
            default_posture(business_overlap="none", market_overlap=None, entity_role="publisher")
            == "outreach"
        )


class TestSearchOverlapBand:
    def test_a_small_site_losing_most_of_its_keywords_reads_as_dominant(self):
        assert (
            search_overlap_band(keyword_intersections=400, own_organic_keywords=500) == "dominant"
        )

    def test_a_large_absolute_overlap_is_never_reported_as_none(self):
        """400 shared keywords is 1% of a 40k-keyword site — but it is not zero,
        and a ratio-only rule would hide a real competitor behind the denominator."""
        assert (
            search_overlap_band(keyword_intersections=400, own_organic_keywords=40_000) == "strong"
        )

    def test_a_tiny_overlap_on_a_huge_site_stays_weak(self):
        assert (
            search_overlap_band(keyword_intersections=12, own_organic_keywords=40_000) == "slight"
        )

    def test_absolute_signal_used_when_our_own_count_is_unknown(self):
        assert search_overlap_band(keyword_intersections=400) == "strong"

    def test_nothing_to_measure_returns_none_not_a_fabricated_band(self):
        assert search_overlap_band(keyword_intersections=None) is None
        assert search_overlap_band(keyword_intersections=None, own_organic_keywords=100) is None

    def test_zero_intersections_is_a_measurement_not_a_missing_value(self):
        assert search_overlap_band(keyword_intersections=0) == "none"
