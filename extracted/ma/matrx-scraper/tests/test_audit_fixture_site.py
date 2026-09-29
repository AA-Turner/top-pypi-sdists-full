"""The SEO audit, forced against a site we control — OPENSEO-TOOLS-SPEC §8.2 / T11.

Learned from OpenSEO's badseo.dev: every fixture page declares EXACTLY the
checks it must raise (``tests/fixtures/audit_site/<site>/site.json``,
``expected_checks``; empty = must be clean), the real crawler and the real
checks run over it (``audit_fixture_harness``), and each page is compared as an
exact set — a missing verdict and an extra one both fail it.

Three sets partition the 83 builtin catalogue rows and are printed on every run:

* ``NOT_IMPLEMENTED`` — builtin rows no check function computes (recounted from
  code: ``analysis.PAGE_CHECKS`` + ``analysis.SITE_CHECKS``).
* ``EXTERNAL_ONLY`` — implemented checks that need evidence no crawl produces
  (Search Console, PageSpeed lab data).
* everything else must be raised by at least one fixture — the coverage gate.

``KNOWN_DEFECTS`` names each page where our pipeline is known to disagree with
the truth its manifest declares: the page is asserted against what it raises
TODAY (so a fix fails the test and forces the entry out), and every entry is
printed loudly on every run. A defect is never hidden by editing a manifest.

Runs offline: loopback servers only, with a socket guard (see the harness).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import pytest

from audit_fixture_harness import (
    FixtureSite,
    audit_fixture_site,
    fixture_site_names,
    route_page_key,
)
from matrx_scraper.web_crawl import analysis

#: Every builtin, non-deleted `web.analysis_item` key — read from the live
#: catalogue on 2026-09-28 (83 rows). `scripts/check_seo_catalogue_coverage.py`
#: owns catalogue ⟷ code drift against the live DB; this snapshot lets the gate
#: run offline. A row added to the catalogue is added here in the same change.
BUILTIN_CATALOGUE: frozenset[str] = frozenset(
    """
    a11y_lab_basics anchor_text_descriptiveness asset_delivery broken_external_links
    broken_images broken_internal_links broken_page_4xx caching_policy canonical_conflicts
    canonical_presence content_depth content_freshness content_quality_eeat crawl_depth
    cwv_cls cwv_inp_tbt cwv_lcp duplicate_content_exact excessive_outlinks grammar_spelling
    gsc_ctr_opportunity gsc_index_coverage gsc_keyword_cannibalization gsc_performance_decay
    h1_presence heading_hierarchy host_protocol_consistency hreflang_reciprocity
    hreflang_validity hsts_policy html_lang_validity https_enforcement image_alt_presence
    image_alt_quality image_dimension_attrs image_lazy_loading image_modern_format
    image_oversized internal_inlink_coverage internal_link_equity internal_redirect_links
    intrusive_interstitials keyword_topical_coverage local_business_markup
    meta_description_duplication meta_description_length meta_description_presence
    meta_refresh_redirect meta_robots_conflicts mixed_content mobile_render_quality
    mobile_usability_lab near_duplicate_content nofollow_internal_links og_image_validity
    orphan_pages page_weight pagination_markup readability redirect_chain redirect_loop
    robots_txt_health search_intent_alignment security_headers serp_snippet_quality
    server_error_5xx sitemap_coverage sitemap_health social_meta_completeness
    soft_404_detection structured_data_coverage structured_data_validity
    temporary_redirect_usage text_html_ratio thin_content title_duplication
    title_keyword_alignment title_length title_presence tls_certificate
    ttfb_server_response url_design_quality viewport_meta
    """.split()
)

#: Builtin rows with NO check function (15 of 83 on 2026-09-28, recounted from
#: code — the "68 of 83" figure checked out). Each reason says what is missing.
NOT_IMPLEMENTED: dict[str, str] = {
    "a11y_lab_basics": "needs a rendered-browser accessibility pass; nothing computes it",
    "content_freshness": "no dated-content evidence is scored yet",
    "content_quality_eeat": "AI judgement row; no model pass is wired to the sweep",
    "grammar_spelling": "AI judgement row; no model pass is wired to the sweep",
    "gsc_index_coverage": "needs Search Console index-coverage data; no check reads it",
    "image_alt_quality": "AI judgement row (alt text quality, not presence)",
    "intrusive_interstitials": "AI vision row; needs a rendered screenshot pass",
    "keyword_topical_coverage": "AI judgement row; no model pass is wired to the sweep",
    "mobile_render_quality": "AI vision row; needs a rendered screenshot pass",
    "mobile_usability_lab": "needs a mobile lab render; nothing computes it",
    "readability": "Flesch is captured per page but no check scores it",
    "search_intent_alignment": "AI judgement row; no model pass is wired to the sweep",
    "serp_snippet_quality": "AI judgement row; no model pass is wired to the sweep",
    "structured_data_coverage": "AI judgement row (which markup a page should carry)",
    "title_keyword_alignment": "needs a target keyword per page; no check reads one",
}

#: Implemented checks whose evidence no crawl can produce. A fixture cannot
#: raise them; their unit tests own them.
EXTERNAL_ONLY: dict[str, str] = {
    "cwv_lcp": "PageSpeed lab data (seo.page_performance), never a crawl",
    "cwv_inp_tbt": "PageSpeed lab data (seo.page_performance), never a crawl",
    "cwv_cls": "PageSpeed lab data (seo.page_performance), never a crawl",
    "asset_delivery": "PageSpeed lab delivery breakdown, never a crawl",
    "caching_policy": "PageSpeed lab cache breakdown, never a crawl",
    "gsc_ctr_opportunity": "Search Console page statistics (web.gsc_page_stat)",
    "gsc_performance_decay": "Search Console page statistics across three windows",
    "gsc_keyword_cannibalization": "Search Console query x page performance",
}


@dataclass(frozen=True)
class KnownDefect:
    raised_today: tuple[str, ...]
    defect: str
    owner: str


#: (site, route) -> what the page raises TODAY instead of its declared truth.
KNOWN_DEFECTS: dict[tuple[str, str], KnownDefect] = {}

SITES = fixture_site_names()
_RUNS: dict[str, Any] = {}


# ---------------------------------------------------------------------------
# Pure gate logic — the forcing-function tests below run it on altered inputs.


def implemented_checks() -> frozenset[str]:
    return frozenset(analysis.PAGE_CHECKS) | frozenset(analysis.SITE_CHECKS)


def partition_errors(
    implemented: frozenset[str],
    not_implemented: dict[str, str],
    external_only: dict[str, str],
    catalogue: frozenset[str] = BUILTIN_CATALOGUE,
) -> list[str]:
    """Every way the three sets can disagree with the code and the catalogue."""

    errors = []
    for key in sorted(implemented & set(not_implemented)):
        errors.append(f"{key} is implemented now — remove it from NOT_IMPLEMENTED")
    for key in sorted(catalogue - implemented - set(not_implemented)):
        errors.append(f"{key} has no check function — add it to NOT_IMPLEMENTED with a reason")
    for key in sorted(set(external_only) - implemented):
        errors.append(f"{key} is EXTERNAL_ONLY but not implemented")
    for key in sorted(implemented - catalogue):
        errors.append(f"{key} is implemented but has no builtin catalogue row")
    for key in sorted(set(not_implemented) - catalogue):
        errors.append(f"{key} is in NOT_IMPLEMENTED but not in the catalogue")
    for mapping_name, mapping in (
        ("NOT_IMPLEMENTED", not_implemented),
        ("EXTERNAL_ONLY", external_only),
    ):
        for key, reason in mapping.items():
            if not reason.strip():
                errors.append(f"{mapping_name}[{key}] has no reason")
    return errors


def declared_truth(sites: dict[str, FixtureSite]) -> dict[str, set[str]]:
    """check key -> the fixtures ('site:route' or 'site:<site>') declaring it."""

    covered: dict[str, set[str]] = {}
    for name, site in sites.items():
        for path, route in site.routes.items():
            for key in route.expected_checks or []:
                covered.setdefault(key, set()).add(f"{name}:{path}")
        for key in site.site_expected_checks:
            covered.setdefault(key, set()).add(f"{name}:<site>")
    return covered


def coverage_gaps(
    implemented: frozenset[str], external_only: dict[str, str], covered: dict[str, set[str]]
) -> list[str]:
    return sorted(implemented - set(external_only) - set(covered))


def manifest_errors(sites: dict[str, FixtureSite]) -> list[str]:
    """Every declared key must be a real, crawlable check of the right subject."""

    page_keys, site_keys = set(analysis.PAGE_CHECKS), set(analysis.SITE_CHECKS)
    errors = []
    for name, site in sites.items():
        for path, route in site.routes.items():
            for key in route.expected_checks or []:
                if key not in page_keys:
                    errors.append(f"{name}:{path} expects {key}, not a per-page check")
                if key in EXTERNAL_ONLY or key in NOT_IMPLEMENTED:
                    errors.append(f"{name}:{path} expects {key}, which no crawl can raise")
            if route.no_verdict and route.expected_checks:
                errors.append(f"{name}:{path} is no_verdict but declares expected_checks")
        for key in site.site_expected_checks:
            if key not in site_keys:
                errors.append(f"{name} site expects {key}, not a site check")
    for (name, path), _defect in KNOWN_DEFECTS.items():
        if name not in sites or (path != "<site>" and path not in sites[name].routes):
            errors.append(f"KNOWN_DEFECTS names {name}:{path}, which is not a fixture route")
    return errors


def page_diff(expected: set[str], raised: set[str]) -> str | None:
    missing, unexpected = sorted(expected - raised), sorted(raised - expected)
    if not missing and not unexpected:
        return None
    parts = []
    if missing:
        parts.append(f"missing: {missing}")
    if unexpected:
        parts.append(f"unexpected: {unexpected}")
    return "; ".join(parts)


def _load_sites() -> dict[str, FixtureSite]:
    return {name: FixtureSite.load(name) for name in SITES}


# ---------------------------------------------------------------------------
# Static gates (no crawl).


def test_catalogue_partition_matches_the_code() -> None:
    errors = partition_errors(implemented_checks(), NOT_IMPLEMENTED, EXTERNAL_ONLY)
    assert not errors, "\n".join(errors)


def test_fixture_manifests_name_real_checks() -> None:
    errors = manifest_errors(_load_sites())
    assert not errors, "\n".join(errors)


def test_coverage_gate_every_implemented_check_has_a_fixture() -> None:
    gaps = coverage_gaps(implemented_checks(), EXTERNAL_ONLY, declared_truth(_load_sites()))
    assert not gaps, (
        "implemented checks with no fixture page that must raise them "
        f"(add one under tests/fixtures/audit_site/): {gaps}"
    )


# The gate's own forcing functions: each alters ONE input the way a careless
# edit would and proves the gate notices.


def test_gate_fails_when_a_fixture_is_removed() -> None:
    sites = _load_sites()
    covered = declared_truth(sites)
    assert "heading_hierarchy" in covered
    covered.pop("heading_hierarchy")
    assert coverage_gaps(implemented_checks(), EXTERNAL_ONLY, covered) == ["heading_hierarchy"]


def test_gate_fails_when_a_set_is_edited_silently() -> None:
    implemented = implemented_checks()
    trimmed = dict(NOT_IMPLEMENTED)
    trimmed.pop("readability")
    assert any("readability" in e for e in partition_errors(implemented, trimmed, EXTERNAL_ONLY))
    stale = {**NOT_IMPLEMENTED, "title_presence": "pretend it is not built"}
    assert any("title_presence" in e for e in partition_errors(implemented, stale, EXTERNAL_ONLY))
    moved = {k: v for k, v in EXTERNAL_ONLY.items() if k != "cwv_lcp"}
    assert coverage_gaps(implemented, moved, declared_truth(_load_sites())) == ["cwv_lcp"]


def test_page_comparison_fails_on_an_extra_or_a_missing_issue() -> None:
    assert page_diff({"title_presence"}, {"title_presence"}) is None
    assert page_diff({"title_presence"}, {"title_presence", "h1_presence"}) == (
        "unexpected: ['h1_presence']"
    )
    assert page_diff({"title_presence", "h1_presence"}, {"h1_presence"}) == (
        "missing: ['title_presence']"
    )
    assert page_diff(set(), {"thin_content"}) == "unexpected: ['thin_content']"


# ---------------------------------------------------------------------------
# The real crawl + checks, one run per fixture site.


def _crawl_expectation_errors(site: FixtureSite, run: Any) -> list[str]:
    from matrx_scraper.events import CrawlWarningEvent

    errors: list[str] = []
    manifest = site.expected_crawl
    completed = run.crawl_completed
    status = getattr(completed, "status", None)
    want_status = manifest.get("status", "completed")
    if status != want_status:
        errors.append(f"crawl ended {status!r}, expected {want_status!r}")
    if (
        "stop_reason" in manifest
        and getattr(completed, "stop_reason", None) != manifest["stop_reason"]
    ):
        errors.append(
            f"crawl stop_reason {getattr(completed, 'stop_reason', None)!r}, "
            f"expected {manifest['stop_reason']!r}"
        )
    sources = {
        (e.context or {}).get("pause_source")
        for e in run.events
        if isinstance(e, CrawlWarningEvent)
    } - {None}
    for source in manifest.get("pause_sources", []):
        if source not in sources:
            errors.append(
                f"no crawl-wide pause with pause_source={source!r} (saw {sorted(sources)})"
            )
    # Link-first: a sitemap-only URL waits until the link-discovered frontier is
    # drained. Measured against the nav (every page the homepage links), which
    # is queued before any sitemap-only URL may be taken; a deep chain still in
    # flight can legitimately interleave (the frontier is empty between hops).
    first_seen = {}
    for index, path in enumerate(run.requests):
        first_seen.setdefault(path, index)
    linked = [first_seen[p] for p, _label in site.nav if p in first_seen]
    for path in site.fetched_after_links:
        if path not in first_seen:
            errors.append(f"{path} was never fetched")
        elif linked and first_seen[path] < max(linked):
            errors.append(f"{path} (sitemap-only) was fetched before link discovery finished")
    return errors


@pytest.mark.parametrize("site_name", SITES)
async def test_fixture_site_raises_exactly_what_it_declares(
    site_name: str, monkeypatch: pytest.MonkeyPatch, tmp_path: Any
) -> None:
    run = await audit_fixture_site(site_name, monkeypatch, tmp_path)
    _RUNS[site_name] = run
    site = run.site
    failures: list[str] = []

    declared: dict[str, tuple[str, Any]] = {}
    for path, route in site.routes.items():
        if route.no_verdict:
            continue
        declared[route_page_key(path)] = (path, route)
    for key in sorted(run.raised_by_page):
        if key.startswith("plain:"):
            failures.append(f"{key}: a plain-http page got a verdict of its own")
        elif key not in declared:
            failures.append(
                f"{key}: got a verdict but no route declares it — raised {sorted(run.raised_by_page[key])}"
            )
    for key, (path, route) in sorted(declared.items()):
        if key not in run.raised_by_page:
            failures.append(f"{path}: declared, but the audit produced no verdict for it")
            continue
        raised = run.raised_by_page[key]
        defect = KNOWN_DEFECTS.get((site_name, path))
        if defect is not None:
            print(f"\n  KNOWN DEFECT {site_name}:{path} — {defect.defect} [owner: {defect.owner}]")
            diff = page_diff(set(defect.raised_today), raised)
            if diff:
                failures.append(
                    f"{path}: KNOWN_DEFECTS no longer matches ({diff}) — if the defect is "
                    f"fixed, delete its entry; the manifest already holds the truth "
                    f"{sorted(route.expected_checks or [])}"
                )
            continue
        diff = page_diff(set(route.expected_checks or []), raised)
        if diff:
            failures.append(f"{path}: {diff}")
        if route.expect_blocked_link_targets:
            evidence = getattr(
                run.outcomes_by_page[key].get("broken_internal_links"), "evidence", None
            )
            if not (evidence or {}).get("blocked_targets"):
                failures.append(f"{path}: the walled targets were not reported as blocked_targets")

    site_defect = KNOWN_DEFECTS.get((site_name, "<site>"))
    if site_defect is not None:
        print(
            f"\n  KNOWN DEFECT {site_name}:<site> — {site_defect.defect} [owner: {site_defect.owner}]"
        )
        site_diff = page_diff(set(site_defect.raised_today), run.site_raised)
        if site_diff:
            failures.append(
                f"<site>: KNOWN_DEFECTS no longer matches ({site_diff}) — if fixed, delete the "
                f"entry; the manifest holds the truth {sorted(site.site_expected_checks)}"
            )
    else:
        site_diff = page_diff(set(site.site_expected_checks), run.site_raised)
        if site_diff:
            failures.append(f"<site>: {site_diff}")
    failures.extend(_crawl_expectation_errors(site, run))
    assert not failures, f"fixture site {site_name!r}:\n  " + "\n  ".join(failures)


def test_coverage_summary_is_printed() -> None:
    """exercised / implemented / not implemented / external-only, of the catalogue."""

    implemented = implemented_checks()
    covered = declared_truth(_load_sites())
    defect_only = {
        key
        for key, where in covered.items()
        if all(
            (loc.split(":", 1)[0], loc.split(":", 1)[1]) in KNOWN_DEFECTS
            for loc in where
            if not loc.endswith("<site>")
        )
        and not any(loc.endswith("<site>") for loc in where)
    }
    exercised = sorted((set(covered) & implemented) - defect_only)
    if _RUNS:
        actually = set()
        for run in _RUNS.values():
            actually |= set().union(*run.raised_by_page.values()) if run.raised_by_page else set()
            actually |= run.site_raised
        exercised = sorted(set(exercised) & actually)
    line = (
        f"exercised {len(exercised)} / implemented {len(implemented)} / "
        f"not implemented {len(NOT_IMPLEMENTED)} / external-only {len(EXTERNAL_ONLY)} "
        f"of {len(BUILTIN_CATALOGUE)}"
    )
    print(f"\n[AUDIT FIXTURES] {line}")
    if defect_only:
        print(f"[AUDIT FIXTURES] declared but blocked by a known defect: {sorted(defect_only)}")
    for (site_name, path), defect in sorted(KNOWN_DEFECTS.items()):
        print(f"[AUDIT FIXTURES] KNOWN DEFECT {site_name}:{path} — {defect.owner}")
    assert len(implemented) + len(NOT_IMPLEMENTED) == len(BUILTIN_CATALOGUE)
