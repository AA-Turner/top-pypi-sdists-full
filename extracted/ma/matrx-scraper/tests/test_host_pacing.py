"""The crawl-rate ruling, pinned.

Arman, 2026-08-20: detect the platform first, honour robots.txt, otherwise start
LOW and climb until the host pushes back — never open by hammering. Each test
here is one clause of that ruling; a change that breaks one is a change to the
ruling, not to an implementation detail.
"""

from __future__ import annotations

import pytest

from matrx_scraper.host_pacing import (
    DEFAULT_KNOBS,
    HostRamp,
    PacingKnobs,
    RememberedPacing,
    resolve_plan,
)
from matrx_scraper.host_platform import PLATFORM_PROFILES, detect_platform, profile_for
from matrx_scraper.robots_txt import parse_robots_txt


# ---------------------------------------------------------------------------
# Detection — "the first thing we need to do is try to detect the system"
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("headers", "html", "expected"),
    [
        ({"x-shopid": "12345"}, None, "shopify"),
        ({}, '<script src="//cdn.shopify.com/s/x.js">', "shopify"),
        ({"x-pingback": "https://x/xmlrpc.php"}, None, "wordpress"),
        ({}, '<link href="/wp-content/themes/x/style.css">', "wordpress"),
        ({"server": "Pepyaka/1.2"}, None, "wix"),
        ({"x-contextid": "abc"}, None, "squarespace"),
        ({"x-wf-page-id": "1"}, None, "webflow"),
        ({"x-drupal-cache": "HIT"}, None, "drupal"),
        ({"server": "cloudflare", "cf-ray": "abc"}, None, "cloudflare"),
    ],
)
def test_detects_known_platforms(headers, html, expected):
    match = detect_platform(headers=headers, html=html)
    assert match is not None
    assert match.name == expected
    assert match.signals, "a match must carry the evidence that produced it"


def test_unknown_host_is_not_guessed_at():
    """No fingerprint means None — which hands the whole decision to the ramp."""
    assert detect_platform(headers={"server": "nginx"}, html="<p>hello</p>") is None


def test_origin_beats_the_cdn_in_front_of_it():
    """Cloudflare in front of WordPress is WordPress; reporting the CDN loses it."""
    match = detect_platform(
        headers={"cf-ray": "x", "server": "cloudflare", "x-pingback": "y"},
        html='<link href="/wp-includes/x.css">',
    )
    assert match is not None
    assert match.name == "wordpress"
    assert match.fronted_by is not None and match.fronted_by.name == "cloudflare"


def test_a_header_outweighs_one_embedded_asset():
    """A Shopify buy-button embedded on a WordPress page is not a Shopify site."""
    match = detect_platform(
        headers={"x-pingback": "https://x/xmlrpc.php"},
        html='<script src="https://cdn.shopify.com/buy-button.js"></script>',
    )
    assert match is not None and match.name == "wordpress"


def test_every_profile_defends_its_number():
    """A rate with no basis is an invented 'documented limit' — the worst case."""
    for profile in PLATFORM_PROFILES:
        assert profile.basis in {"published", "observed", "conservative"}
        assert profile.rationale.strip(), f"{profile.name} states no rationale"
        if profile.basis == "published":
            assert profile.doc_url, f"{profile.name} claims 'published' with no source"
        if profile.is_fronting:
            assert profile.sustained_rps is None, (
                f"{profile.name} is a CDN; pinning a rate on it would clamp every "
                "origin behind it to the same guess"
            )


# ---------------------------------------------------------------------------
# robots.txt — "honour Crawl-delay as an upper bound where present"
# ---------------------------------------------------------------------------


def test_crawl_delay_is_parsed_and_scoped_to_its_group():
    doc = parse_robots_txt(
        "User-agent: *\nCrawl-delay: 10\nDisallow: /admin\n\n"
        "User-agent: MatrxBot\nRequest-rate: 1/4s\nDisallow:\n"
    )
    assert doc.crawl_delay_for("*") == 10.0
    assert doc.crawl_delay_for("MatrxBot/1.0") == 4.0
    assert not doc.syntax_errors


def test_unparseable_pacing_directive_is_reported_not_swallowed():
    doc = parse_robots_txt("User-agent: *\nCrawl-delay: soon\n")
    assert doc.crawl_delay_for("*") is None
    assert any("Crawl-delay" in err for err in doc.syntax_errors)


def test_crawl_delay_caps_the_ceiling():
    plan = resolve_plan("slow.example", user_max_rps=8.0, crawl_delay_seconds=5.0)
    assert plan.ceiling_rps == pytest.approx(0.2)
    assert plan.source == "robots_crawl_delay"
    assert plan.start_rps <= plan.ceiling_rps


def test_an_absurd_crawl_delay_is_clamped_and_says_so():
    """Honouring 'Crawl-delay: 86400' literally would take a year. Never silent."""
    plan = resolve_plan("hostile.example", crawl_delay_seconds=86_400.0)
    assert plan.ceiling_rps > 1 / 3600
    assert any("86400" in note for note in plan.notes)


# ---------------------------------------------------------------------------
# The plan — order of authority
# ---------------------------------------------------------------------------


def test_published_platform_limit_holds_even_when_the_user_asks_for_more():
    plan = resolve_plan(
        "store.example",
        user_max_rps=10.0,
        platform=detect_platform(headers={"x-shopid": "1"}),
    )
    assert plan.ceiling_rps == pytest.approx(profile_for("shopify").sustained_rps)
    assert plan.user_max_reduced is True
    assert any("2 req/s" in note for note in plan.notes), (
        "a clamped setting the user cannot see is a defect (crawler vision point 8)"
    )


def test_user_maximum_lowers_but_never_raises():
    plan = resolve_plan("anything.example", user_max_rps=1.0)
    assert plan.ceiling_rps == 1.0
    assert plan.source == "user_max"


def test_nothing_known_opens_at_the_floor_not_at_the_old_default():
    """The bug this whole change exists to kill: opening at 4 rps and hoping."""
    plan = resolve_plan("brand-new.example", user_max_rps=4.0)
    assert plan.start_rps == DEFAULT_KNOBS.floor_rps
    assert plan.start_rps < 4.0


def test_a_remembered_ceiling_opens_below_itself():
    plan = resolve_plan(
        "known.example",
        user_max_rps=20.0,
        remembered=RememberedPacing(host="known.example", ceiling_rps=6.0, source="remembered"),
    )
    assert plan.ceiling_rps == pytest.approx(6.0)
    assert plan.start_rps == pytest.approx(6.0 * DEFAULT_KNOBS.remembered_start_fraction)
    assert plan.start_rps < plan.ceiling_rps, "re-opening AT the ceiling is re-hammering"


def test_memory_never_raises_a_published_platform_limit():
    """One lucky run against a Shopify store does not repeal Shopify's 2/s."""
    plan = resolve_plan(
        "store.example",
        platform=detect_platform(headers={"x-shopid": "1"}),
        remembered=RememberedPacing(host="store.example", ceiling_rps=11.0, source="remembered"),
    )
    assert plan.ceiling_rps <= profile_for("shopify").sustained_rps


# ---------------------------------------------------------------------------
# The ramp — "keep pushing up higher until we figure out what the limit is,
# and then back off from it"
# ---------------------------------------------------------------------------


def _feed_clean(ramp: HostRamp, n: int, latency_ms: float | None = 100.0) -> list[float]:
    changes = []
    for _ in range(n):
        new = ramp.observe_success(latency_ms=latency_ms)
        if new is not None:
            changes.append(new)
    return changes


def test_climbs_only_after_sustained_clean_responses():
    ramp = HostRamp(plan=resolve_plan("h.example"))
    opening = ramp.current_rps
    assert _feed_clean(ramp, DEFAULT_KNOBS.ramp_after_clean - 1) == []
    assert ramp.current_rps == opening
    assert _feed_clean(ramp, 1) == [pytest.approx(opening * DEFAULT_KNOBS.ramp_factor)]


def test_climb_stops_at_the_ceiling_and_never_banks_credit():
    ramp = HostRamp(plan=resolve_plan("h.example", user_max_rps=1.0))
    _feed_clean(ramp, 500)
    assert ramp.current_rps == pytest.approx(1.0)


def test_pushback_backs_off_and_records_the_discovered_ceiling():
    ramp = HostRamp(plan=resolve_plan("h.example"))
    _feed_clean(ramp, DEFAULT_KNOBS.ramp_after_clean * 4)
    provoking = ramp.current_rps
    ramp.observe_limit(reason="http_429")
    assert ramp.current_rps == pytest.approx(provoking * DEFAULT_KNOBS.backoff_factor)
    assert ramp.discovered_limit_rps == pytest.approx(provoking * DEFAULT_KNOBS.ceiling_hold)
    assert ramp.ceiling < provoking, "we hold BELOW the discovered limit, never at it"


def test_the_ramp_never_climbs_back_into_a_known_limit():
    ramp = HostRamp(plan=resolve_plan("h.example"))
    _feed_clean(ramp, DEFAULT_KNOBS.ramp_after_clean * 4)
    ramp.observe_limit()
    discovered = ramp.discovered_limit_rps
    _feed_clean(ramp, 500)
    assert ramp.current_rps <= discovered + 1e-9


def test_repeated_limits_settle_rather_than_spiral_to_zero():
    ramp = HostRamp(plan=resolve_plan("h.example"))
    for _ in range(6):
        _feed_clean(ramp, DEFAULT_KNOBS.ramp_after_clean * 3)
        ramp.observe_limit()
    assert ramp.current_rps >= DEFAULT_KNOBS.min_rps


def test_latency_inflection_backs_off_before_a_429_is_ever_sent():
    """A host straining is the host pushing back — it need not say 429 first."""
    ramp = HostRamp(plan=resolve_plan("h.example"))
    _feed_clean(ramp, DEFAULT_KNOBS.ramp_after_clean * 2, latency_ms=300.0)
    climbed = ramp.current_rps
    _feed_clean(ramp, DEFAULT_KNOBS.ramp_after_clean * 2, latency_ms=5_000.0)
    assert ramp.current_rps < climbed
    assert ramp.discovered_limit_rps is not None


def test_fast_pages_do_not_trip_the_latency_check():
    """40 ms going to 100 ms says nothing about load."""
    ramp = HostRamp(plan=resolve_plan("h.example"))
    _feed_clean(ramp, DEFAULT_KNOBS.ramp_after_clean * 2, latency_ms=40.0)
    before = ramp.current_rps
    _feed_clean(ramp, DEFAULT_KNOBS.ramp_after_clean * 2, latency_ms=100.0)
    assert ramp.current_rps > before


def test_a_run_that_learned_nothing_remembers_nothing():
    """A six-page crawl at the floor must not teach the next run '0.5 req/s'."""
    ramp = HostRamp(plan=resolve_plan("h.example"))
    _feed_clean(ramp, 6)
    assert ramp.to_remembered() is None


def test_a_run_that_climbed_cleanly_remembers_what_it_held():
    ramp = HostRamp(plan=resolve_plan("h.example"))
    _feed_clean(ramp, DEFAULT_KNOBS.ramp_after_clean * 3)
    memory = ramp.to_remembered()
    assert memory is not None
    assert memory.ceiling_rps == pytest.approx(ramp.highest_clean_rps)


def test_snapshot_never_claims_a_ceiling_it_did_not_find():
    ramp = HostRamp(plan=resolve_plan("h.example"))
    _feed_clean(ramp, DEFAULT_KNOBS.ramp_after_clean * 3)
    assert ramp.snapshot()["discovered_ceiling_rps"] is None


def test_knobs_are_injectable_per_feature():
    """Every number is a knob the host fills from site settings, not a constant."""
    knobs = PacingKnobs(floor_rps=2.0, max_rps=3.0, ramp_after_clean=1, ramp_factor=4.0)
    ramp = HostRamp(plan=resolve_plan("h.example", knobs=knobs), knobs=knobs)
    assert ramp.current_rps == 2.0
    _feed_clean(ramp, 5)
    assert ramp.current_rps == 3.0
