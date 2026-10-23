"""The JS app-shell guard, the dead-end page check, and duplicate-group candidacy.

Realistic HTML, through the REAL `audit_html` -> `evidence_from_audit` -> checks
path, and through the sweep's `index_page_facts` aggregation. Headless: no
network, no browser.
"""

from __future__ import annotations

from dataclasses import fields

import pytest

from matrx_scraper import read_judge
from matrx_scraper.app_shell import SHELL_HTML_MARKERS, SHELL_TEXT_MARKERS
from matrx_scraper.parser import knobs as parser_knobs
from matrx_scraper.seo_audit import (
    JS_SHELL_NOT_APPLICABLE_REASON,
    PAGE_CHECKS,
    PageEvidence,
    audit_html,
    evidence_from_audit,
    page_is_js_shell,
    run_page_checks,
)
from matrx_scraper.web_crawl import analysis
from matrx_scraper.web_crawl.analysis import PageFacts, SiteAggregates, index_page_facts
from matrx_scraper.web_crawl.rollup import ROLLUP_RULES

NEXT_SHELL = """<!DOCTYPE html><html lang="en"><head><meta charSet="utf-8"/>
<meta name="viewport" content="width=device-width"/><title>Acme Dashboard</title>
<meta name="description" content="Acme's customer dashboard."/>
<script src="/_next/static/chunks/webpack-1a2b.js" defer=""></script>
<script src="/_next/static/chunks/main-3c4d.js" defer=""></script></head>
<body><div id="__next"></div>
<script id="__NEXT_DATA__" type="application/json">{"props":{"pageProps":{"intro":"Welcome to the Acme dashboard where you can manage invoices, customers, reports, exports and every setting your team needs, from billing contacts to audit logs and saved filters"}},"page":"/","query":{},"buildId":"k2P9"}</script>
</body></html>"""

CRA_SHELL = """<!doctype html><html lang="en"><head><meta charset="utf-8"/>
<link rel="icon" href="/favicon.ico"/><meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>React App</title><script defer="defer" src="/static/js/main.8f3a1c.js"></script>
<link href="/static/css/main.2b7e.css" rel="stylesheet"></head>
<body><noscript>You need to enable JavaScript to run this app.</noscript><div id="root"></div></body></html>"""

SSR_PAGE = """<!DOCTYPE html><html lang="en"><head><title>Blue Running Shoes | Acme</title>
<meta name="description" content="Lightweight blue running shoes for daily training."/>
<script src="/_next/static/chunks/main-3c4d.js" defer=""></script></head>
<body><div id="__next"><header><nav><a href="/">Home</a> <a href="/shoes">Shoes</a></nav></header>
<main><h1>Blue Running Shoes</h1><p>Our lightest daily trainer, built for long easy miles and
quick tempo days alike. The knit upper breathes, the foam returns energy, and the outsole lasts.</p>
<h2>Fit</h2><p>True to size with a roomy toe box.</p><img src="/shoe.jpg" alt="Blue running shoe"/>
<p><a href="/shoes/blue/reviews">Read the reviews</a></p></main></div>
<script id="__NEXT_DATA__" type="application/json">{"page":"/shoes/blue"}</script></body></html>"""

# Few words, but a real page: it has links (and a heading), so it is never a shell.
SMALL_REAL_PAGE = """<!doctype html><html lang="en"><head><title>Contact us</title>
<script src="/assets/app.js" type="module"></script></head>
<body><div id="app"><h1>Contact</h1><p>Call us any day.</p>
<a href="/">Home</a> <a href="/about">About</a></div></body></html>"""

DEAD_END_PAGE = """<!doctype html><html lang="en"><head><title>Our 2026 product recall notice</title>
<meta name="description" content="Details of the 2026 recall."/></head>
<body><main><h1>Product recall notice</h1>
<p>We are recalling the 2026 model of the trail kettle because the lid latch can loosen after
repeated heating. If you own one, stop using it and keep the receipt. Refunds are issued in
full and replacement units ship within two weeks. Thank you for your patience while we fix this.</p>
</main></body></html>"""

CONTENT_CHECKS = (
    "h1_presence",
    "heading_hierarchy",
    "thin_content",
    "content_depth",
    "text_html_ratio",
    "image_alt_presence",
    "soft_404_detection",
)


@pytest.fixture(autouse=True)
def _standalone_knobs():
    parser_knobs.configure_parser_knobs(None)
    yield
    parser_knobs.configure_parser_knobs(None)


def _evidence(html: str, url: str, *, status: int = 200) -> PageEvidence:
    audit = audit_html(html, url)
    return evidence_from_audit(audit, http_status=status, response_bytes=len(html.encode()))


def _facts(page_id: str, ev: PageEvidence, **overrides) -> PageFacts:
    values = {f.name: getattr(ev, f.name) for f in fields(PageEvidence)}
    values.update(overrides)
    return PageFacts(page_id=page_id, **values)


# --- is_js_shell -------------------------------------------------------------


@pytest.mark.parametrize(
    ("html", "url", "expected"),
    [
        (NEXT_SHELL, "https://acme.example/dashboard", True),
        (CRA_SHELL, "https://acme.example/app", True),
        (SSR_PAGE, "https://acme.example/shoes/blue", False),
        (SMALL_REAL_PAGE, "https://acme.example/contact", False),
        (DEAD_END_PAGE, "https://acme.example/recall", False),
    ],
)
def test_is_js_shell_fact(html: str, url: str, expected: bool) -> None:
    assert page_is_js_shell(_evidence(html, url)) is expected


def test_next_shell_json_payload_is_not_read_as_visible_words() -> None:
    audit = audit_html(NEXT_SHELL, "https://acme.example/dashboard")
    # Script text (the __NEXT_DATA__ JSON) is never counted as words — not by the
    # page's word count, and not by the shell test.
    assert audit.word_count == 0
    assert audit.app_shell_words == 0


def test_word_count_excludes_script_style_and_template_text() -> None:
    html = (
        "<html><body><p>Four real visible words</p>"
        "<script>var a = 'one two three four five six';</script>"
        "<style>p { color: red; } .x { margin: 0 }</style>"
        "<template><p>hidden template words here</p></template>"
        "<noscript>Enable JavaScript</noscript></body></html>"
    )
    audit = audit_html(html, "https://acme.example/words")
    assert audit.word_count == 6  # 4 visible + the 2-word noscript line a crawler sees


def test_unknown_when_the_snapshot_never_captured_shell_markup() -> None:
    ev = _evidence(CRA_SHELL, "https://acme.example/app")
    ev.app_root = None
    ev.executable_script = None
    assert page_is_js_shell(ev) is None
    outcome = PAGE_CHECKS["content_needs_rendering"](ev)
    assert outcome.status == "n_a" and outcome.remediation is not None
    # Unknown never silences the content checks: thin content still judges.
    assert PAGE_CHECKS["thin_content"](ev).status == "fail"


def test_word_limit_is_a_knob() -> None:
    ev = _evidence(CRA_SHELL, "https://acme.example/app")
    assert page_is_js_shell(ev) is True
    # The noscript line is 9 words: a limit at or below that makes it a page.
    parser_knobs.configure_parser_knobs(lambda key: {"audit.js_shell_word_limit": 5}[key])
    assert page_is_js_shell(ev) is False


# --- the guard ---------------------------------------------------------------


@pytest.mark.parametrize("html", [NEXT_SHELL, CRA_SHELL])
def test_shell_content_checks_are_not_applicable(html: str) -> None:
    results = run_page_checks(_evidence(html, "https://acme.example/app"))
    for key in CONTENT_CHECKS:
        assert results[key].status == "n_a", key
        assert results[key].reasoning == JS_SHELL_NOT_APPLICABLE_REASON
        assert results[key].issue_count == 0
    rendering = results["content_needs_rendering"]
    assert rendering.status == "fail" and rendering.issue_count == 1
    assert "Render mode" in rendering.reasoning and "Browser always" in rendering.reasoning
    assert results["dead_end_page"].status == "n_a"


def test_same_shell_without_the_guard_raised_false_findings() -> None:
    """The defect the guard fixes: the unguarded checks fail a shell."""
    ev = _evidence(CRA_SHELL, "https://acme.example/app")
    assert PAGE_CHECKS["thin_content"].__wrapped__(ev).status == "fail"
    assert PAGE_CHECKS["h1_presence"].__wrapped__(ev).status == "fail"


@pytest.mark.parametrize(
    ("html", "url"),
    [(SSR_PAGE, "https://acme.example/shoes/blue"), (SMALL_REAL_PAGE, "https://acme.example/contact")],
)
def test_real_pages_keep_their_content_verdicts(html: str, url: str) -> None:
    results = run_page_checks(_evidence(html, url))
    assert results["content_needs_rendering"].status == "pass"
    assert results["h1_presence"].status == "pass"
    assert results["thin_content"].reasoning != JS_SHELL_NOT_APPLICABLE_REASON


# --- dead_end_page -----------------------------------------------------------


def test_dead_end_page_raises_a_finding() -> None:
    outcome = PAGE_CHECKS["dead_end_page"](_evidence(DEAD_END_PAGE, "https://acme.example/recall"))
    assert outcome.status == "warn" and outcome.issue_count == 1


def test_linked_page_is_not_a_dead_end() -> None:
    outcome = PAGE_CHECKS["dead_end_page"](_evidence(SSR_PAGE, "https://acme.example/shoes/blue"))
    assert outcome.status == "pass"


def test_noindexed_or_non_2xx_dead_end_is_not_judged() -> None:
    noindexed = DEAD_END_PAGE.replace("</title>", '</title><meta name="robots" content="noindex"/>')
    assert PAGE_CHECKS["dead_end_page"](_evidence(noindexed, "https://acme.example/recall")).status == "n_a"
    gone = _evidence(DEAD_END_PAGE, "https://acme.example/recall", status=404)
    assert PAGE_CHECKS["dead_end_page"](gone).status == "n_a"


def test_new_checks_roll_up_site_wide() -> None:
    assert ROLLUP_RULES["content_needs_rendering"].tokens is None
    assert ROLLUP_RULES["dead_end_page"].tokens is None
    assert {"content_needs_rendering", "dead_end_page"} <= set(analysis.CATALOGUED_PAGE_CHECKS)


# --- duplicate grouping ------------------------------------------------------


def _dup_site(*pages: PageFacts) -> SiteAggregates:
    site = SiteAggregates()
    index_page_facts(list(pages), site)
    return site


def test_duplicate_groups_exclude_noindex_and_canonicalized_pages() -> None:
    base = _evidence(DEAD_END_PAGE, "https://acme.example/recall")
    a = _facts("a", base, url="https://acme.example/recall", exact_sha256="x", fingerprint_version=1)
    noindexed = _facts("b", base, url="https://acme.example/recall?print=1", noindex=True,
                       exact_sha256="x", fingerprint_version=1)
    canonicalized = _facts("c", base, url="https://acme.example/recall?ref=mail", canonical_matches=False,
                           exact_sha256="x", fingerprint_version=1)
    site = _dup_site(a, noindexed, canonicalized)
    for check in (
        analysis._check_title_duplication,
        analysis._check_meta_description_duplication,
        analysis._check_duplicate_content_exact,
    ):
        assert check(a, site).status == "pass", check.__name__
        assert check(noindexed, site).status == "n_a", check.__name__
        assert check(canonicalized, site).status == "n_a", check.__name__


def test_two_indexable_twins_still_duplicate() -> None:
    base = _evidence(DEAD_END_PAGE, "https://acme.example/recall")
    a = _facts("a", base, url="https://acme.example/recall", exact_sha256="x", fingerprint_version=1)
    b = _facts("b", base, url="https://acme.example/recall-copy", exact_sha256="x", fingerprint_version=1)
    site = _dup_site(a, b)
    assert analysis._check_title_duplication(a, site).status == "warn"
    assert analysis._check_duplicate_content_exact(a, site).status == "fail"


def test_app_shell_routes_are_not_duplicates_of_each_other() -> None:
    shell = _evidence(CRA_SHELL, "https://acme.example/app")
    a = _facts("a", shell, url="https://acme.example/app/one", exact_sha256="s", fingerprint_version=1)
    b = _facts("b", shell, url="https://acme.example/app/two", exact_sha256="s", fingerprint_version=1)
    site = _dup_site(a, b)
    assert not site.pages_by_title and not site.pages_by_sha
    outcome = analysis._check_title_duplication(a, site)
    assert outcome.status == "n_a" and outcome.reasoning == JS_SHELL_NOT_APPLICABLE_REASON
    assert analysis._near_duplicate_indexable(a) is False
    facts = analysis._build_site_facts("site", [a, b])
    near = analysis.SITE_CHECKS["near_duplicate_content"](facts)
    assert near.status == "n_a" and "JavaScript" in near.reasoning


# --- one marker list ---------------------------------------------------------


def test_read_judge_uses_the_shared_markers() -> None:
    assert read_judge._SHELL_HTML_MARKERS is SHELL_HTML_MARKERS
    assert read_judge._SHELL_TEXT_MARKERS is SHELL_TEXT_MARKERS
    verdict = read_judge.judge_read(status=200, text="", html=CRA_SHELL)
    assert verdict.failed


# --- the crawler keeps shells, never empty pages -----------------------------


def test_crawler_keeps_only_real_shells_through_the_sanity_gate() -> None:
    from matrx_scraper.seo_audit import SHELL_KEEP_FAILURE_REASONS
    from matrx_scraper.seo_audit import html_is_js_shell

    assert SHELL_KEEP_FAILURE_REASONS == {"empty_content", "low_text_content", "js_shell"}
    assert html_is_js_shell(CRA_SHELL, "https://acme.example/app")
    assert html_is_js_shell(NEXT_SHELL, "https://acme.example/dashboard")
    # Empty, broken, or merely short pages are not shells: they still fail.
    assert not html_is_js_shell("", "https://acme.example/empty")
    assert not html_is_js_shell("<html><body></body></html>", "https://acme.example/blank")
    assert not html_is_js_shell("<html><body><div id='root'></div></body></html>", "https://acme.example/noscript")
    assert not html_is_js_shell(SMALL_REAL_PAGE, "https://acme.example/contact")


# --- every shell signal is load-bearing --------------------------------------

_SCRIPT = '<script src="/static/js/main.js"></script>'


def _shell(body: str, head: str = "") -> bool | None:
    html = f"<html><head><title>App</title>{head}</head><body>{body}</body></html>"
    return page_is_js_shell(_evidence(html, "https://acme.example/app"))


def test_each_shell_signal_is_required() -> None:
    assert _shell(f'<div id="root"></div>{_SCRIPT}') is True
    assert _shell('<div id="root"></div>') is False  # no executable script
    assert _shell(f"<div></div>{_SCRIPT}") is False  # no app root
    assert _shell(f'<div id="root"><h2>Hi</h2></div>{_SCRIPT}') is False  # a heading
    assert _shell(f'<div id="root"></div><a href="/x">x</a>{_SCRIPT}') is False  # a link
    assert _shell(f'<div id="root"></div><img src="/a.png" alt="a">{_SCRIPT}') is False  # an image
    twenty = " ".join(["word"] * 20)
    assert _shell(f'<div id="root"></div><noscript>{twenty}</noscript>{_SCRIPT}') is False  # 20 words


@pytest.mark.parametrize(
    "body",
    [
        f'<div id="q-app"></div>{_SCRIPT}',
        f'<div id="___gatsby"></div>{_SCRIPT}',
        '<div style="display: contents"><script>{__sveltekit_x = {}; import("/app.js")}</script></div>',
        '<script src="flutter_bootstrap.js" async></script>',
        '<div id="root"></div><script type="text/babel">render()</script>',
        '<div id="root"></div><script type="text/ecmascript" src="/a.js"></script>',
        f'<div id="root"><div class="spin">Loading...</div></div>{_SCRIPT}',
        f'<div id="root"><p>Please enable JavaScript to use this site.</p></div>{_SCRIPT}',
    ],
)
def test_more_frameworks_are_shells(body: str) -> None:
    assert _shell(body) is True


def test_body_mounted_frameworks_are_shells() -> None:
    sveltekit = (
        '<html><body data-sveltekit-preload-data="hover"><div style="display: contents">'
        '<script>{__sveltekit_x = {}; import("/app.js")}</script></div></body></html>'
    )
    ember = '<html><body class="ember-application"><script src="/assets/vendor.js"></script></body></html>'
    for html in (sveltekit, ember):
        assert page_is_js_shell(_evidence(html, "https://acme.example/")) is True


def test_server_rendered_text_inside_the_root_is_not_a_shell() -> None:
    ssr = (
        '<html><body><div id="__next"><p>We moved. Call us today.</p></div>'
        '<script id="__NEXT_DATA__" type="application/json">{"props":{}}</script>'
        f"{_SCRIPT}</body></html>"
    )
    assert page_is_js_shell(_evidence(ssr, "https://acme.example/moved")) is False


def test_root_text_limit_is_an_org_knob() -> None:
    from matrx_scraper.seo_audit import reset_js_shell_knobs, use_js_shell_knobs

    ssr = f'<html><body><div id="root"><p>We moved. Call us today.</p></div>{_SCRIPT}</body></html>'
    ev = _evidence(ssr, "https://acme.example/moved")
    assert page_is_js_shell(ev) is False
    token = use_js_shell_knobs({"audit.js_shell_root_text_words": 10, "audit.js_shell_word_limit": 20})
    try:
        assert page_is_js_shell(ev) is True
    finally:
        reset_js_shell_knobs(token)


async def test_shell_knobs_resolve_for_the_organization() -> None:
    from matrx_scraper.parser.knobs import KnobScope
    from matrx_scraper.seo_audit import resolve_js_shell_knobs

    seen: list[KnobScope] = []

    async def scoped(keys, scope):
        seen.append(scope)
        return {"audit.js_shell_word_limit": 7} if scope.organization_id == "org-a" else {}

    parser_knobs.configure_parser_knobs(lambda key: {"audit.js_shell_word_limit": 20, "audit.js_shell_root_text_words": 3}[key], scoped_reader=scoped)
    values = await resolve_js_shell_knobs(KnobScope(organization_id="org-a"))
    assert values["audit.js_shell_word_limit"] == 7 and values["audit.js_shell_root_text_words"] == 3
    assert seen and seen[0].organization_id == "org-a"


# --- the crawler keeps shells and soft 404s, never walls ---------------------


def test_keepable_failed_reads() -> None:
    from matrx_scraper.seo_audit import KEPT_JS_SHELL, KEPT_SOFT_404, keepable_failed_read

    url = "https://acme.example/app"
    visible_js = f'<html><body><div id="root"><p>Please enable JavaScript to use this site.</p></div>{_SCRIPT}</body></html>'
    assert keepable_failed_read(failure_reason="js_shell", status=200, html=visible_js, url=url) == KEPT_JS_SHELL
    assert keepable_failed_read(failure_reason="empty_content", status=200, html=CRA_SHELL, url=url) == KEPT_JS_SHELL
    assert keepable_failed_read(failure_reason="not_found", status=200, html=DEAD_END_PAGE, url=url) == KEPT_SOFT_404
    # Never a non-2xx answer, an empty body, or a page that is not a shell.
    assert keepable_failed_read(failure_reason="empty_content", status=404, html=CRA_SHELL, url=url) is None
    assert keepable_failed_read(failure_reason="empty_content", status=200, html="", url=url) is None
    assert keepable_failed_read(failure_reason="empty_content", status=200, html="<html><body></body></html>", url=url) is None
    # A bot wall inside an app root is still a wall.
    wall = f'<html><head><title>Just a moment...</title></head><body><div id="root"></div>{_SCRIPT}</body></html>'
    assert keepable_failed_read(failure_reason="empty_content", status=200, html=wall, url=url, title="Just a moment...") is None


def test_kept_reads_are_not_announced_as_blocks() -> None:
    from types import SimpleNamespace

    from matrx_scraper.orchestrator import is_a_wall

    def result(html: str, reason: str = "empty_content", status: int = 200):
        return SimpleNamespace(url="https://acme.example/app", response_url=None, status_code=status,
                               raw_html=html, title="React App", failure_reason=reason)

    # The crawler keeps a shell: no block row.
    assert is_a_wall(result(CRA_SHELL), keeps_failed_reads=True) is False
    assert is_a_wall(result(DEAD_END_PAGE, "not_found"), keeps_failed_reads=True) is False
    # Any other caller, or a page the crawler does not keep, is still announced.
    assert is_a_wall(result(CRA_SHELL), keeps_failed_reads=False) is True
    assert is_a_wall(result("<html><body></body></html>"), keeps_failed_reads=True) is True
    assert is_a_wall(result(CRA_SHELL, status=503), keeps_failed_reads=True) is True


# --- canonicals are resolved against the page --------------------------------


@pytest.mark.parametrize(
    ("canonical", "page_url", "expected"),
    [
        ("/shoes/blue", "https://acme.example/shoes/blue", True),
        ("//acme.example/shoes/blue", "https://acme.example/shoes/blue", True),
        ("https://acme.example/shoes/blue/", "https://acme.example/shoes/blue", True),
        ("/shoes/red", "https://acme.example/shoes/blue", False),
        ("https://other.example/shoes/blue", "https://acme.example/shoes/blue", False),
        ("//other.example/shoes/blue", "https://acme.example/shoes/blue", False),
    ],
)
def test_canonicals_resolve_against_the_page(canonical: str, page_url: str, expected: bool) -> None:
    from matrx_scraper.audit_metrics import canonical_is_self, evaluate_indexability

    assert canonical_is_self(canonical, page_url) is expected
    verdict = evaluate_indexability(200, None, canonical, [], page_url, page_url)
    assert verdict["canonical_matches"] is expected
    html = f'<html><head><link rel="canonical" href="{canonical}"></head><body><p>x</p></body></html>'
    assert _evidence(html, page_url).canonical_matches is expected


def test_relative_self_canonical_stays_in_duplicate_groups() -> None:
    base = _evidence(DEAD_END_PAGE, "https://acme.example/recall")
    a = _facts("a", base, url="https://acme.example/recall", canonical_url="/recall", canonical_matches=True,
               exact_sha256="x", fingerprint_version=2)
    b = _facts("b", base, url="https://acme.example/recall-copy", canonical_url="/recall-copy",
               canonical_matches=True, exact_sha256="x", fingerprint_version=2)
    site = _dup_site(a, b)
    assert analysis._check_duplicate_content_exact(a, site).status == "fail"


# --- dead ends: same site, real onward links ---------------------------------


def test_www_and_apex_links_are_internal_and_self_links_are_not() -> None:
    page = "https://acme.example/recall"
    www = DEAD_END_PAGE.replace("</main>", '<p><a href="https://www.acme.example/shop">Shop</a></p></main>')
    assert PAGE_CHECKS["dead_end_page"](_evidence(www, page)).status == "pass"
    self_only = DEAD_END_PAGE.replace(
        "</main>", '<p><a href="#top">Top</a> <a href="/recall">This page</a> <a href="https://acme.example/recall#faq">FAQ</a></p></main>'
    )
    assert PAGE_CHECKS["dead_end_page"](_evidence(self_only, page)).status == "warn"


def test_fingerprint_version_moved_with_the_counting_method() -> None:
    from matrx_scraper.parser.hashing import FINGERPRINT_VERSION

    assert FINGERPRINT_VERSION == 2


# --- bot walls in app-shell markup are blocked reads, never shells -----------

_WALLS = {
    "px_captcha": (
        '<html><head><title>Access to this page has been denied</title></head><body>'
        f'<div id="px-captcha"></div><div id="root"></div>{_SCRIPT}</body></html>'
    ),
    "datadome": (
        '<html><head><title>example.com</title></head><body><div id="root"></div>'
        '<script>var dd={"cid":"x"}</script><script src="https://ct.captcha-delivery.com/c.js"></script>'
        "</body></html>"
    ),
    "cloudflare_just_a_moment": (
        f'<html><head><title>Just a moment...</title></head><body><div id="root"></div>{_SCRIPT}</body></html>'
    ),
}


@pytest.mark.parametrize("name", sorted(_WALLS))
def test_bot_walls_are_never_shells(name: str) -> None:
    from matrx_scraper.seo_audit import is_bot_wall

    html = _WALLS[name]
    url = "https://acme.example/p"
    title = html.split("<title>", 1)[1].split("</title>", 1)[0]
    assert is_bot_wall(html=html, title=title) is True
    ev = _evidence(html, url)
    assert ev.bot_wall is True
    assert page_is_js_shell(ev) is False
    assert html_is_js_shell_for(html, url) is False
    rendering = PAGE_CHECKS["content_needs_rendering"](ev)
    assert rendering.status == "n_a" and rendering.reasoning.startswith("Blocked — could not assess")
    # Content checks get the blocked answer, never a thin-content or missing-H1 finding.
    for key in ("thin_content", "h1_presence", "dead_end_page"):
        outcome = PAGE_CHECKS[key](ev)
        assert outcome.status == "n_a" and outcome.reasoning.startswith("Blocked"), key


def html_is_js_shell_for(html: str, url: str) -> bool:
    from matrx_scraper.seo_audit import html_is_js_shell

    return html_is_js_shell(html, url)


def test_a_stored_wall_snapshot_reads_as_blocked() -> None:
    ev = _evidence(_WALLS["datadome"], "https://acme.example/p")
    facts = _facts("w", ev, bot_wall=True, fetch_blocked_reason="cloudflare_block")
    assert PAGE_CHECKS["thin_content"](facts).reasoning.startswith("Blocked")
    assert analysis._check_title_duplication(facts, SiteAggregates()).reasoning.startswith("Blocked")


def test_a_503_maintenance_frame_is_a_page_not_a_shell() -> None:
    maintenance = (
        '<html><head><title>Under maintenance</title></head><body>'
        f'<div id="root"></div>{_SCRIPT}</body></html>'
    )
    assert page_is_js_shell(_evidence(maintenance, "https://acme.example/", status=503)) is False
    # A 200 maintenance frame has no reliable marker (documented gap): still a shell.
    assert page_is_js_shell(_evidence(maintenance, "https://acme.example/")) is True


# --- round 2: real pages are never walls; kept soft 404s; canonicals --------

_LONG_BODY = " ".join(["Cloudflare Workers let you run code at the edge."] * 80)


@pytest.mark.parametrize(
    "title", ["Cloudflare Workers tutorial: deploy in five minutes", "Security check-up for small business"]
)
def test_a_full_page_with_a_wall_word_in_its_title_is_not_a_wall(title: str) -> None:
    html = (
        f'<html><head><title>{title}</title><script src="/_next/static/main.js"></script></head>'
        f'<body><div id="__next"><header><a href="/">Home</a><a href="/blog">Blog</a></header>'
        f'<main><h1>{title}</h1><p>{_LONG_BODY}</p><img src="/a.png" alt="x"></main></div>'
        '<script id="__NEXT_DATA__" type="application/json">{}</script></body></html>'
    )
    ev = _evidence(html, "https://example.com/blog/x")
    assert ev.bot_wall is False
    assert PAGE_CHECKS["h1_presence"](ev).status == "pass"
    assert PAGE_CHECKS["content_needs_rendering"](ev).status == "pass"


def test_a_soft_404_that_is_a_wall_is_never_kept() -> None:
    from matrx_scraper.seo_audit import keepable_failed_read

    wall = _WALLS["cloudflare_just_a_moment"]
    assert keepable_failed_read(
        failure_reason="not_found", status=200, html=wall, url="https://acme.example/p", title="Just a moment..."
    ) is None


def test_stored_relative_self_canonical_is_rejudged_on_load() -> None:
    from types import SimpleNamespace

    snap = SimpleNamespace(
        id="s1",
        head_tags={"title": "Recall", "canonical_url": "/recall"},
        seo_metrics={},
        audit_metrics={"indexability": {"canonical_matches": False, "noindex": False, "nofollow": False}},
        headings={"h1_count": 1, "all": [{"level": 1, "text": "Recall"}]},
        images={"count": 0, "missing_alt": 0, "items": []},
        extracted={},
        structured_data={},
        perf={},
        links_summary={"internal": 3, "total": 3},
        word_count=300,
        http_status=200,
        captured_at=None,
    )
    page = SimpleNamespace(id="p1", url="https://acme.example/recall", link_score=None, target_keyword=None)
    assert analysis._extract_page_facts(page, snap).canonical_matches is True
    snap.head_tags = {"title": "Recall", "canonical_url": "/elsewhere"}
    assert analysis._extract_page_facts(page, snap).canonical_matches is False


_CHAIN3 = [
    {"url": "https://acme.example/old", "status": 301},
    {"url": "https://acme.example/middle", "status": 301},
    {"url": "https://acme.example/new", "status": 200},
]
_CHAIN2 = [
    {"url": "http://acme.example/new", "status": 301},
    {"url": "https://acme.example/new", "status": 200},
]


@pytest.mark.parametrize(
    ("canonical", "chain", "requested", "is_self"),
    [
        ("http://acme.example/new", _CHAIN2, "http://acme.example/new", False),  # 2 hops, canonical = start
        ("https://acme.example/old", _CHAIN3, "https://acme.example/old", False),  # 3 hops, start
        ("/middle", _CHAIN3, "https://acme.example/old", False),  # 3 hops, middle
        ("https://acme.example/new", _CHAIN3, "https://acme.example/old", True),  # the final URL
        ("https://acme.example/old-page", [], "https://acme.example/old-page", True),  # no redirect
    ],
)
def test_a_canonical_naming_any_redirecting_url_points_to_a_redirect(canonical, chain, requested, is_self) -> None:
    from matrx_scraper.audit_metrics import evaluate_indexability

    verdict = evaluate_indexability(200, None, canonical, chain, "https://acme.example/new", requested)
    assert verdict["canonical_matches"] is is_self
    ev = PageEvidence(url="https://acme.example/new", canonical_url=canonical, canonical_matches=is_self,
                      redirect_chain=chain, http_status=200, noindex=False)
    outcome = PAGE_CHECKS["canonical_conflicts"](ev)
    if is_self:
        assert outcome.status == "pass" or outcome.status == "n_a"
    else:
        assert outcome.status == "fail" and outcome.score == 30 and "redirect" in outcome.reasoning


def test_a_kept_soft_404_gets_only_its_soft_404_finding() -> None:
    from matrx_scraper.seo_audit import KEPT_SOFT_404_REASON

    soft = DEAD_END_PAGE.replace("Our 2026 product recall notice", "Page not found").replace(
        "<p>We are recalling", "<p>Sorry. We are recalling"
    )
    ev = _evidence(soft, "https://acme.example/gone")
    ev.kept_soft_404 = True
    ev.word_count = 12
    results = run_page_checks(ev)
    assert results["soft_404_detection"].status in ("warn", "fail")
    others = {k: o for k, o in results.items() if k != "soft_404_detection"}
    assert all(o.status == "n_a" and o.reasoning == KEPT_SOFT_404_REASON for o in others.values())
    facts = _facts("g", ev)
    assert analysis.PAGE_CHECKS["title_duplication"](facts, SiteAggregates()).reasoning == KEPT_SOFT_404_REASON


def test_the_wall_census_imports_light() -> None:
    import subprocess
    import sys

    code = (
        "import sys, matrx_scraper.challenge_census as c; "
        "heavy=[m for m in ('curl_cffi','readability','orjson','httpx','dotenv','matrx_scraper.scraper') if m in sys.modules]; "
        "print(heavy)"
    )
    out = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, timeout=60)
    assert out.stdout.strip() == "[]", out.stdout + out.stderr
    from matrx_scraper import scraper
    from matrx_scraper.challenge_census import FailureReason, detect_challenge_reasons

    assert scraper.FailureReason is FailureReason and scraper.detect_challenge_reasons is detect_challenge_reasons


def test_kept_soft_404s_are_not_duplicate_candidates() -> None:
    base = _evidence(DEAD_END_PAGE, "https://acme.example/gone")
    a = _facts("a", base, url="https://acme.example/gone-a", exact_sha256="x", fingerprint_version=2, kept_soft_404=True)
    b = _facts("b", base, url="https://acme.example/gone-b", exact_sha256="x", fingerprint_version=2, kept_soft_404=True)
    site = _dup_site(a, b)
    assert not site.pages_by_title and not site.pages_by_sha
    assert analysis._near_duplicate_indexable(a) is False


@pytest.mark.parametrize(
    "title",
    [
        "Cloudflare Workers pricing",
        "Security check-up for small business",
        "One more step to finish your order",
        "Access Denied - The Band",
    ],
)
def test_short_real_pages_with_wall_words_in_the_title_are_not_walls(title: str) -> None:
    from matrx_scraper.seo_audit import is_bot_wall

    html = (
        f"<html><head><title>{title}</title></head><body><div id=\"root\"><main><p>"
        "Plans start at five dollars a month. Compare tiers and pick what fits your team."
        f"</p></main></div>{_SCRIPT}</body></html>"
    )
    assert is_bot_wall(html=html, title=title) is False
    assert _evidence(html, "https://acme.example/p").bot_wall is False
