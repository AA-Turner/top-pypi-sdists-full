"""Severity shaped by Arman's check tiers (fact-before-opinion R-04).

Real catalog bands (web.analysis_item, 2026-10-05). The 2026-10-05 incident:
a homepage with no canonical scored in canonical_presence's `low` band, so the
one fact that mattered sat at `low` among 15,536 findings.
"""

from types import SimpleNamespace

from matrx_scraper.web_crawl.analysis_write import band_severity, severity_for

FOUR_BANDS = {"bands": [{"max": 20, "severity": "high"}, {"max": 45, "severity": "med"},
                        {"max": 75, "severity": "low"}, {"max": 100, "severity": "info"}],
              "scale": "1-100"}
THREE_BANDS = {"bands": [{"max": 30, "severity": "med"}, {"max": 60, "severity": "low"},
                         {"max": 100, "severity": "info"}], "scale": "1-100"}


def item(tier, bands=FOUR_BANDS):
    return SimpleNamespace(tier=tier, severity_map=bands)


def test_the_incident_a_missing_homepage_canonical_is_critical() -> None:
    canonical_presence = item("A")
    assert band_severity(canonical_presence, 60) == "low"  # what it used to be
    assert severity_for(canonical_presence, 60) == "high"
    assert severity_for(canonical_presence, 60, on_homepage=True) == "critical"


def test_polish_never_outranks_a_blocker() -> None:
    meta_description_length = item("C", THREE_BANDS)
    assert severity_for(meta_description_length, 10) == "low"
    assert severity_for(meta_description_length, 10, on_homepage=True) == "med"
    assert severity_for(item("A"), 70) == "high"


def test_ranking_checks_keep_their_band_capped_at_high() -> None:
    assert severity_for(item("B"), 10) == "high"
    assert severity_for(item("B"), 40) == "med"


def test_an_opinion_never_escalates() -> None:
    gsc_ctr_opportunity = item("D", THREE_BANDS)
    assert severity_for(gsc_ctr_opportunity, 1, on_homepage=True) == "info"


def test_planted_breaks_passing_unknown_and_unruled() -> None:
    # Passing and scoreless results carry no judgment, whatever the tier.
    assert severity_for(item("A"), 95, on_homepage=True) == "info"
    assert severity_for(item("A"), None, on_homepage=True) == "info"
    # A check nobody has ruled on keeps its band exactly.
    assert severity_for(item(None), 60) == "low"
