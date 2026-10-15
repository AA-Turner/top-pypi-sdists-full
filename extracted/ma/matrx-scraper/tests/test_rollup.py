"""One shared cause is one finding (2026-10-14 census: one footer logo sat in
298 image findings, one jQuery file in 208 caching findings)."""

from __future__ import annotations

from matrx_scraper.web_crawl.rollup import ROLLUP_MIN_PAGES, plan_rollups

LOGO = "https://site.example/wp-content/themes/t/twitter-logo.png"


def _row(i, item_key, status="warn", score=60, evidence=None, item_id="item-1", metadata_reason=None):
    meta = {"evidence": evidence or {}}
    if metadata_reason:
        meta["reasoning"] = metadata_reason
    return {
        "subject_type": "page",
        "subject_id": f"p{i}",
        "item_id": item_id,
        "item_key": item_key,
        "status": status,
        "score": score,
        "metadata": meta,
    }


URLS = {f"p{i}": f"https://site.example/page-{i}" for i in range(400)}


def test_a_shared_image_becomes_one_site_plan():
    rows = [_row(i, "image_dimension_attrs", evidence={"missing_dimensions": [LOGO]}) for i in range(298)]
    rows.append(_row(999, "image_dimension_attrs", evidence={"missing_dimensions": [LOGO, "https://x/own.jpg"]}))
    [plan] = plan_rollups(rows, URLS)
    assert plan.outcome.evidence["shared_causes"][0]["cause"] == LOGO
    assert plan.outcome.evidence["shared_causes"][0]["pages"] == 299
    assert len(plan.covered) == 298  # the page with its own extra image keeps its own finding
    assert "p999" not in plan.covered
    assert "fixing it once clears every page" in plan.outcome.reasoning


def test_fewer_than_the_minimum_stays_per_page():
    rows = [_row(i, "image_dimension_attrs", evidence={"missing_dimensions": [LOGO]}) for i in range(ROLLUP_MIN_PAGES - 1)]
    assert plan_rollups(rows, URLS) == []


def test_unique_causes_never_roll_up():
    rows = [_row(i, "image_dimension_attrs", evidence={"missing_dimensions": [f"https://x/{i}.jpg"]}) for i in range(50)]
    assert plan_rollups(rows, URLS) == []


def test_sitewide_speed_rolls_up_when_most_pages_fail():
    rows = [_row(i, "cwv_lcp", evidence={"lcp_ms": 4000 + i}) for i in range(60)]
    rows += [_row(100 + i, "cwv_lcp", status="pass", score=95) for i in range(20)]
    [plan] = plan_rollups(rows, URLS)
    assert plan.outcome.evidence["pages_affected"] == 60
    assert plan.outcome.evidence["pages_checked"] == 80
    assert "60 of the 80 pages" in plan.outcome.reasoning


def test_speed_stays_per_page_when_most_pages_pass():
    rows = [_row(i, "cwv_lcp", evidence={"lcp_ms": 5000}) for i in range(10)]
    rows += [_row(100 + i, "cwv_lcp", status="pass", score=95) for i in range(40)]
    assert plan_rollups(rows, URLS) == []


def test_per_page_checks_are_never_rolled_up():
    rows = [_row(i, "title_length") for i in range(100)]
    assert plan_rollups(rows, URLS) == []


def test_plans_are_db_valid():
    rows = [_row(i, "caching_policy", evidence={"short_ttl_urls": [f"https://site.example/wp-includes/js/jquery.min.js"]}) for i in range(10)]
    [plan] = plan_rollups(rows, URLS)
    assert plan.outcome.status in ("warn", "fail") and 1 <= plan.outcome.score <= 100


def test_a_page_with_more_problems_than_its_sample_keeps_its_finding():
    # Evidence lists are capped at 5; a page with 12 problem images whose first
    # 5 are the shared logo must not be covered — images 6-12 are its own.
    shared = [f"https://site.example/theme/logo-{k}.png" for k in range(5)]
    rows = [_row(i, "image_dimension_attrs", evidence={"missing_dimensions": shared}) for i in range(10)]
    for r in rows:
        r["issue_count"] = 5
    rows[0]["issue_count"] = 12
    [plan] = plan_rollups(rows, URLS)
    assert "p0" not in plan.covered and len(plan.covered) == 9


def test_a_far_worse_page_is_not_hidden_by_a_sitewide_rollup():
    rows = [_row(i, "cwv_lcp", evidence={"lcp_ms": 3100}) for i in range(20)]
    rows.append(_row(99, "cwv_lcp", evidence={"lcp_ms": 12000}))
    [plan] = plan_rollups(rows, URLS)
    assert "p99" not in plan.covered


def test_distinct_canonical_problems_never_merge():
    missing = [_row(i, "canonical_presence", metadata_reason="No rel=canonical — variants compete") for i in range(6)]
    relative = [_row(10 + i, "canonical_presence", metadata_reason="Canonical is relative — resolve it") for i in range(2)]
    [plan] = plan_rollups(missing + relative, URLS)
    assert plan.covered == {f"p{i}" for i in range(6)}
