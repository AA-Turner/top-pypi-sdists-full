from datetime import UTC, datetime, timedelta
from decimal import Decimal

import pytest

from matrx_seo.change_anomaly import ChangeVolumeInput, assess_change_volume
from matrx_seo.pagespeed_coverage import (
    CoveragePage,
    importance_score,
    plan_pagespeed_coverage,
)

NOW = datetime(2026, 8, 9, tzinfo=UTC)


def page(
    pid: str,
    *,
    site: str = "site-a",
    homepage: bool = False,
    depth: int = 1,
    clicks: int = 0,
    impressions: int = 0,
    link_score: str | None = None,
    measured_days_ago: int | None = None,
    changed_days_ago: int | None = None,
) -> CoveragePage:
    return CoveragePage(
        page_id=pid,
        site_id=site,
        url=f"https://{site}.com/{pid}",
        is_homepage=homepage,
        depth=depth,
        clicks=clicks,
        impressions=impressions,
        link_score=Decimal(link_score) if link_score is not None else None,
        last_measured_at=(
            NOW - timedelta(days=measured_days_ago) if measured_days_ago is not None else None
        ),
        last_changed_at=(
            NOW - timedelta(days=changed_days_ago) if changed_days_ago is not None else None
        ),
    )


# ── importance ─────────────────────────────────────────────────────────────


def test_traffic_outranks_structure_and_homepage_outranks_a_dead_page() -> None:
    trafficked = page("p1", clicks=500, impressions=20_000)
    linked = page("p2", link_score="0.02")
    dead = page("p3", depth=4)
    home = page("p0", homepage=True, depth=0)
    assert importance_score(trafficked) > importance_score(linked) > importance_score(dead)
    assert importance_score(home) > importance_score(dead)


def test_scoring_degrades_gracefully_with_no_signals_at_all() -> None:
    """Most sites have no GSC binding and no PageRank yet — ordering must still
    be deterministic and shallow-first, not arbitrary."""
    shallow = page("a", depth=1)
    deep = page("b", depth=6)
    assert importance_score(shallow) > importance_score(deep)
    assert importance_score(deep) >= 0.0


def test_log_scaling_stops_one_huge_page_from_flattening_everything() -> None:
    huge = importance_score(page("a", impressions=1_000_000))
    normal = importance_score(page("b", impressions=1_000))
    assert huge > normal
    # Sub-linear: a 1000x traffic difference must not be a 1000x score gap.
    assert huge < normal * 3


def test_queue_orders_real_clicks_and_impressions_before_internal_importance() -> None:
    """The UI promises GSC demand first; PageRank may only break traffic ties."""
    pages = [
        page("internally-linked", clicks=2, impressions=585, link_score="1"),
        page("search-winner", clicks=48, impressions=6_545),
        page("impression-runner-up", clicks=2, impressions=1_500),
    ]
    plan = plan_pagespeed_coverage({"site-a": pages}, now=NOW, request_budget=3)
    assert [selection.page_id for selection in plan.selections] == [
        "search-winner",
        "impression-runner-up",
        "internally-linked",
    ]


# ── coverage-first ordering ────────────────────────────────────────────────


def test_never_measured_pages_beat_refreshes_of_more_important_pages() -> None:
    """The whole point of 'every page gets at least one test': a high-traffic
    homepage due for refresh must NOT crowd out an unmeasured page."""
    pages = [
        page("home", homepage=True, depth=0, clicks=9_999, measured_days_ago=400),
        page("never", depth=3),
    ]
    plan = plan_pagespeed_coverage({"site-a": pages}, now=NOW, request_budget=1)
    assert [s.page_id for s in plan.selections] == ["never"]
    assert plan.selections[0].reason == "never_measured"


def test_changed_content_beats_a_routine_refresh() -> None:
    pages = [
        page("stale", clicks=100, measured_days_ago=200),
        page("edited", measured_days_ago=10, changed_days_ago=1),
    ]
    plan = plan_pagespeed_coverage({"site-a": pages}, now=NOW, request_budget=2)
    assert plan.selections[0].page_id == "edited"
    assert plan.selections[0].reason == "content_changed"


def test_recently_measured_unchanged_page_is_not_selected() -> None:
    pages = [page("fresh", clicks=100, measured_days_ago=1)]
    plan = plan_pagespeed_coverage({"site-a": pages}, now=NOW)
    assert plan.selections == []
    assert plan.requests_planned == 0


def test_refresh_cadence_is_tier_sensitive() -> None:
    """A low-value page measured 60 days ago is not yet due; a homepage is."""
    home = page("home", homepage=True, depth=0, clicks=5_000, measured_days_ago=60)
    junk = page("junk", depth=7, measured_days_ago=60)
    plan = plan_pagespeed_coverage({"s": [home, junk]}, now=NOW)
    picked = {s.page_id for s in plan.selections}
    assert "home" in picked
    assert "junk" not in picked


# ── strategies ─────────────────────────────────────────────────────────────


def test_first_coverage_is_mobile_only_for_every_page() -> None:
    pages = [page("home", homepage=True, depth=0)] + [page(f"p{i}", depth=5) for i in range(40)]
    plan = plan_pagespeed_coverage({"s": pages}, now=NOW, request_budget=500)
    by_id = {s.page_id: s for s in plan.selections}
    assert by_id["home"].strategies == ["mobile"]
    assert by_id["p39"].strategies == ["mobile"]
    assert sum(s.requests for s in plan.selections) == len(plan.selections)


def test_important_pages_get_desktop_on_a_due_refresh() -> None:
    pages = [page("home", homepage=True, depth=0, measured_days_ago=8)]
    plan = plan_pagespeed_coverage({"s": pages}, now=NOW, request_budget=2)
    assert plan.selections[0].strategies == ["mobile", "desktop"]


# ── budget + fairness (the real reason this exists) ────────────────────────


def test_one_huge_site_cannot_starve_the_others() -> None:
    """allgreenrecycling (4,425 pages) must not consume the whole cycle."""
    big = {f"big-{i}": page(f"big-{i}", site="big", depth=3) for i in range(4_425)}
    small = {f"small-{i}": page(f"small-{i}", site="small", depth=1) for i in range(50)}
    plan = plan_pagespeed_coverage(
        {"big": list(big.values()), "small": list(small.values())},
        now=NOW,
        request_budget=1_500,
        per_site_request_cap=100,
    )
    per_site = {a.site_id: a for a in plan.per_site}
    assert per_site["big"].requests <= 100
    assert per_site["big"].capped is True
    # The small site still got served in the same cycle — that is fairness.
    assert per_site["small"].requests > 0
    assert per_site["small"].selected_pages == 50


def test_global_budget_is_never_exceeded_and_exhaustion_is_reported() -> None:
    sites = {
        f"s{n}": [page(f"s{n}-p{i}", site=f"s{n}", depth=2) for i in range(200)] for n in range(12)
    }
    plan = plan_pagespeed_coverage(sites, now=NOW, request_budget=300, per_site_request_cap=100)
    assert plan.requests_planned <= 300
    assert sum(s.requests for s in plan.selections) == plan.requests_planned
    assert plan.budget_exhausted is True


def test_a_page_is_never_half_measured_when_budget_runs_out() -> None:
    """A 2-request page with 1 request left must be deferred whole, or it would
    be recorded as covered on a partial pass."""
    plan = plan_pagespeed_coverage(
        {"s": [page("home", homepage=True, depth=0, measured_days_ago=8)]},
        now=NOW,
        request_budget=1,
    )
    assert plan.selections == []
    assert plan.budget_exhausted is True


def test_rotation_advances_across_cycles_without_a_cursor() -> None:
    """Measuring stamps last_measured_at, which is what moves the batch forward."""
    pages = [page(f"p{i}", depth=2) for i in range(250)]
    first = plan_pagespeed_coverage(
        {"s": pages}, now=NOW, request_budget=100, per_site_request_cap=100
    )
    done = {s.page_id for s in first.selections}
    assert len(done) == 100

    later = NOW + timedelta(days=1)
    advanced = [
        p.model_copy(update={"last_measured_at": NOW}) if p.page_id in done else p for p in pages
    ]
    second = plan_pagespeed_coverage(
        {"s": advanced}, now=later, request_budget=100, per_site_request_cap=100
    )
    picked = {s.page_id for s in second.selections}
    assert picked.isdisjoint(done), "cycle 2 must not re-measure cycle 1's pages"
    assert len(picked) == 100


def test_short_cycles_rotate_between_sites_without_a_cursor() -> None:
    sites = {
        f"s{index}": [page(f"p{page_index}", site=f"s{index}") for page_index in range(10)]
        for index in range(4)
    }
    first = plan_pagespeed_coverage(sites, now=NOW, request_budget=2, per_site_request_cap=2)
    first_sites = {selection.site_id for selection in first.selections}
    assert len(first_sites) == 2

    measured = {selection.page_id for selection in first.selections}
    advanced = {
        site_id: [
            candidate.model_copy(update={"last_measured_at": NOW})
            if candidate.page_id in measured and candidate.site_id in first_sites
            else candidate
            for candidate in pages
        ]
        for site_id, pages in sites.items()
    }
    second = plan_pagespeed_coverage(
        advanced,
        now=NOW + timedelta(minutes=10),
        request_budget=2,
        per_site_request_cap=2,
    )
    assert {selection.site_id for selection in second.selections}.isdisjoint(first_sites)


def test_coverage_backlog_is_reported_per_site() -> None:
    pages = [page(f"p{i}", depth=2) for i in range(250)]
    plan = plan_pagespeed_coverage(
        {"s": pages}, now=NOW, request_budget=100, per_site_request_cap=100
    )
    allocation = plan.per_site[0]
    assert allocation.never_measured == 250
    assert allocation.remaining_never_measured == 150


def test_full_coverage_is_reached_by_repeated_cycles() -> None:
    """The end-to-end promise: keep running and every page gets measured."""
    pages = [page(f"p{i}", depth=2) for i in range(220)]
    measured: dict[str, datetime] = {}
    for cycle in range(10):
        now = NOW + timedelta(days=cycle)
        current = [
            p.model_copy(update={"last_measured_at": measured.get(p.page_id)}) for p in pages
        ]
        plan = plan_pagespeed_coverage(
            {"s": current}, now=now, request_budget=100, per_site_request_cap=100
        )
        if not plan.selections:
            break
        for selection in plan.selections:
            measured[selection.page_id] = now
    assert len(measured) == 220


def test_zero_budget_plans_nothing_and_does_not_crash() -> None:
    plan = plan_pagespeed_coverage({"s": [page("a")]}, now=NOW, request_budget=0)
    assert plan.selections == []
    assert plan.requests_planned == 0


def test_invalid_budget_arguments_raise() -> None:
    with pytest.raises(ValueError):
        plan_pagespeed_coverage({}, now=NOW, request_budget=-1)
    with pytest.raises(ValueError):
        plan_pagespeed_coverage({}, now=NOW, per_site_request_cap=0)


# ── change-volume anomaly guard ────────────────────────────────────────────


def test_fifteen_of_five_hundred_changed_is_believable() -> None:
    result = assess_change_volume(
        ChangeVolumeInput(site_id="s", session_id="x", compared_pages=500, changed_pages=15)
    )
    assert result.verdict == "normal"
    assert result.fan_out_allowed is True


def test_all_five_hundred_changed_stops_and_flags() -> None:
    result = assess_change_volume(
        ChangeVolumeInput(site_id="s", session_id="x", compared_pages=500, changed_pages=500)
    )
    assert result.verdict == "anomalous"
    assert result.fan_out_allowed is False
    assert result.likely_causes, "an anomaly must explain what usually causes it"
    # Written for a non-technical site owner.
    assert "ratio" not in result.detail.lower()
    assert "hash" not in result.detail.lower()


def test_four_hundred_of_five_hundred_also_stops() -> None:
    result = assess_change_volume(
        ChangeVolumeInput(site_id="s", session_id="x", compared_pages=500, changed_pages=400)
    )
    assert result.verdict == "anomalous"
    assert result.fan_out_allowed is False


def test_small_site_changing_completely_is_not_an_anomaly() -> None:
    """3 of 4 pages is 75% and entirely normal — ratio alone would be wrong."""
    result = assess_change_volume(
        ChangeVolumeInput(site_id="s", session_id="x", compared_pages=4, changed_pages=3)
    )
    assert result.verdict == "normal"
    assert result.fan_out_allowed is True


def test_added_and_removed_pages_do_not_inflate_the_changed_ratio() -> None:
    result = assess_change_volume(
        ChangeVolumeInput(
            site_id="s",
            session_id="x",
            compared_pages=200,
            changed_pages=5,
            added_pages=300,
            removed_pages=100,
        )
    )
    assert result.verdict == "normal"
    assert result.changed_ratio == pytest.approx(5 / 200)


def test_midrange_change_is_suspicious_and_still_blocks_fan_out() -> None:
    result = assess_change_volume(
        ChangeVolumeInput(site_id="s", session_id="x", compared_pages=200, changed_pages=100)
    )
    assert result.verdict == "suspicious"
    assert result.fan_out_allowed is False


def test_truncated_diff_is_carried_through_so_callers_know_it_is_a_sample() -> None:
    result = assess_change_volume(
        ChangeVolumeInput(
            site_id="s", session_id="x", compared_pages=500, changed_pages=5, truncated=True
        )
    )
    assert result.truncated is True


# ── asset filtering (8% of the real budget was going to images) ────────────


@pytest.mark.parametrize(
    "url",
    [
        "https://x.com/wp-content/uploads/2015/09/Bottom-.jpeg",
        "https://x.com/img/a.JPG",
        "https://x.com/sitemap_index.xml",
        "https://x.com/style.css",
        "https://x.com/app.min.js",
        "https://x.com/brochure.pdf",
        "https://x.com/font.woff2",
        "https://x.com/video.mp4",
        # Extension-LESS machine endpoints. A suffix-only test measured these
        # as pages: every WordPress site on the platform spent PSI budget on
        # its own REST API, and content_type_last is NULL for most such rows so
        # it could not reject them either.
        "https://x.com/wp-json/wp/v2/compliance/21086",
        "https://x.com/wp-json/oembed/1.0/embed?url=https%3A%2F%2Fx.com%2Fa%2F",
        "https://x.com/wp-json",
        "https://x.com/blog/feed",
        "https://x.com/?rest_route=/wp/v2/posts",
    ],
)
def test_assets_are_not_measurable(url: str) -> None:
    from matrx_seo.pagespeed_coverage import is_measurable_page

    assert is_measurable_page(url) is False


@pytest.mark.parametrize(
    "url",
    [
        "https://x.com/",
        "https://x.com",
        "https://x.com/blog/prevent-chapped-lips",
        "https://x.com/treatment-areas/face/brows",
        "https://x.com/page.html",
        "https://x.com/products/gold-chain-bag",
        # A dot in a path segment that is not a known asset suffix is a page.
        "https://x.com/v1.2/release-notes",
        "https://x.com/e-waste-recycling?ref=nav",
        # "feed" as a content word is not the feed endpoint.
        "https://x.com/blog/feeding-your-dog",
    ],
)
def test_real_pages_stay_measurable(url: str) -> None:
    from matrx_seo.pagespeed_coverage import is_measurable_page

    assert is_measurable_page(url) is True


def test_content_type_can_reject_a_suffixless_asset_url() -> None:
    from matrx_seo.pagespeed_coverage import is_measurable_page

    assert is_measurable_page("https://x.com/cdn/image", "image/png") is False
    assert is_measurable_page("https://x.com/cdn/thing", "image") is False
    assert is_measurable_page("https://x.com/cdn/thing", "text/html") is True
    # NULL content_type (9,411 of 11,505 real rows) must not reject anything.
    assert is_measurable_page("https://x.com/cdn/thing", None) is True


# ---------------------------------------------------------------------------
# Failure classification — the poison-pill gate. Every message below is a
# VERBATIM error string taken from `scheduler.sch_run` on 2026-08-13, when
# three pages produced 156 of the sweep's failures.
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "message",
    [
        "113f3fe4[mobile]: ProviderResponseError: PSI HTTP 400: Lighthouse returned "
        "error: NO_FCP. The page did not paint any content.",
        "0e557001[mobile]: ProviderResponseError: PSI HTTP 400: Lighthouse returned "
        "error: FAILED_DOCUMENT_REQUEST. Lighthouse was unable to reliably load the "
        "page you requested. (Details: net::ERR_TIMED_OUT)",
        "x[mobile]: ProviderResponseError: PSI HTTP 400: Lighthouse returned error: "
        "ERRORED_DOCUMENT_REQUEST. Status code: 500",
        "x[mobile]: PSI HTTP 400: Lighthouse returned error: DNS_FAILURE",
    ],
)
def test_page_level_lighthouse_verdicts_are_terminal(message: str) -> None:
    from matrx_seo.pagespeed_coverage import classify_psi_failure

    assert classify_psi_failure(message).kind == "terminal"


@pytest.mark.parametrize(
    ("message", "code"),
    [
        ("x[mobile]: ProviderResponseError: PSI HTTP 500: internal error", "provider_5xx"),
        ("x[mobile]: PSI HTTP 503: backend unavailable", "provider_5xx"),
        ("x[mobile]: TimeoutError: ", "timeout"),
        ("x[mobile]: ReadTimeout: timed out reading from PSI", "timeout"),
        ("x[mobile]: ProviderResponseError: PSI HTTP 429: quota exceeded", "rate_limited"),
        (
            "x[mobile]: ProviderResponseError: RemoteProtocolError: Server disconnected",
            "unknown",
        ),
    ],
)
def test_provider_side_failures_keep_retrying(message: str, code: str) -> None:
    from matrx_seo.pagespeed_coverage import classify_psi_failure

    verdict = classify_psi_failure(message)
    assert verdict.kind == "transient"
    assert verdict.code == code


def test_unrecognized_failures_default_to_retrying() -> None:
    """Fails OPEN, deliberately — the OPPOSITE direction from is_measurable_page.

    A wrongly retried page costs one request per cycle and is visible in the
    run history. A wrongly quarantined page silently stops being covered, which
    is the single outcome the health ledger exists to prevent.
    """
    from matrx_seo.pagespeed_coverage import classify_psi_failure

    verdict = classify_psi_failure("something nobody has seen before")
    assert verdict.kind == "transient"
    assert verdict.code == "unknown"


def test_a_terminal_code_wins_over_an_incidental_timeout_mention() -> None:
    """FAILED_DOCUMENT_REQUEST always carries `net::ERR_TIMED_OUT` details.

    Reading that as "timeout ⇒ transient" would leave the exact live poison
    pill in the sweep forever, so the terminal codes are matched FIRST.
    """
    from matrx_seo.pagespeed_coverage import classify_psi_failure

    verdict = classify_psi_failure(
        "PSI HTTP 400: Lighthouse returned error: FAILED_DOCUMENT_REQUEST. "
        "(Details: net::ERR_TIMED_OUT) TimeoutError"
    )
    assert verdict.kind == "terminal"
    assert verdict.code == "FAILED_DOCUMENT_REQUEST"
