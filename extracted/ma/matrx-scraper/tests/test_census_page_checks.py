"""Live-census regressions for the per-page checks (2026-10-14).

Each test pins one false/noisy finding the census found open on real sites. The
rule behind all of them: a finding must be TRUE, worth a person's time, and name
its cause - never claim what was not measured.
"""

from __future__ import annotations

from matrx_scraper import seo_audit
from matrx_scraper.seo_audit import (
    CheckOutcome,
    PageEvidence,
    audit_html,
    check_broken_images,
    check_canonical_presence,
    check_content_depth,
    check_h1_presence,
    check_image_alt_presence,
    check_image_dimension_attrs,
    check_image_lazy_loading,
    check_meta_description_length,
    check_og_image_validity,
    check_social_meta_completeness,
    check_soft_404_detection,
    check_structured_data_validity,
    check_text_html_ratio,
    check_thin_content,
    check_title_length,
    check_url_design_quality,
)

OG = {
    "og:title": "T",
    "og:description": "D",
    "og:image": "https://example.com/i.jpg",
    "og:url": "https://example.com/a",
    "og:type": "website",
}


def ev(**kw) -> PageEvidence:
    base = dict(url="https://example.com/a", head_captured=True, og=dict(OG), twitter={})
    base.update(kw)
    return PageEvidence(**base)


def valid(o: CheckOutcome) -> None:
    assert o.status in ("pass", "warn", "fail", "n_a")
    if o.status == "n_a":
        assert o.score is None
    else:
        assert o.score is not None and 1 <= o.score <= 100
    assert o.reasoning


def img(**kw) -> dict:
    item = {"src": "https://example.com/p.jpg", "alt": "x", "width": 10, "height": 10}
    item.update(kw)
    return item


# 1. title / description length: contract bands, not stale pixel flags --------


def test_title_60_chars_is_optimal_even_when_a_stale_mobile_flag_says_otherwise():
    title = "T" * 60
    stale = {"ok": False, "mobile_ok": False, "desktop_ok": True, "issues": ["mobile limit 500px"]}
    o = check_title_length(ev(title=title, title_metrics=stale))
    valid(o)
    assert o.status == "pass" and o.score == 100
    assert "500px" not in o.reasoning


def test_title_bands_follow_the_contract():
    assert check_title_length(ev(title="x" * 65)).score == 75  # 61-70, not a finding
    assert check_title_length(ev(title="x" * 65)).status == "pass"
    over = check_title_length(ev(title="x" * 71))
    assert over.status == "warn" and over.score == 55
    short = check_title_length(ev(title="x" * 14))
    assert short.status == "warn" and short.score == 50


def test_description_bands_follow_the_contract():
    stale = {"ok": False, "desktop_ok": False, "issues": ["too wide at 920px"]}
    ok = check_meta_description_length(ev(description="d" * 155, description_metrics=stale))
    assert ok.status == "pass" and ok.score == 100
    assert check_meta_description_length(ev(description="d" * 160)).status == "pass"
    assert check_meta_description_length(ev(description="d" * 166)).score == 65
    assert check_meta_description_length(ev(description="d" * 49)).score == 60


# 2. title comes from <head> only ----------------------------------------------


def test_inline_svg_title_is_not_the_page_title():
    html = (
        "<html><head><meta charset=utf-8></head><body>"
        "<svg><title>icon-X</title></svg><p>hello</p></body></html>"
    )
    assert audit_html(html, "https://example.com/").title == ""
    real = (
        "<html><head><title>Real  Title\n here</title></head><body>"
        "<svg><title>icon-X</title></svg></body></html>"
    )
    assert audit_html(real, "https://example.com/").title == "Real Title here"


def test_parser_core_title_ignores_svg_title():
    from matrx_scraper.parser.core import ParserOrchestrator

    def title_of(html: str) -> str:
        parser = ParserOrchestrator(soup=html, url="https://example.com/")
        parser._init_url_meta()
        return parser.page_title

    assert title_of("<html><body><svg><title>icon-X</title></svg></body></html>") == ""
    assert (
        title_of(
            "<html><head><title>Real</title></head><body><svg><title>icon-X</title></svg></body></html>"
        )
        == "Real"
    )


# 3. h1 -------------------------------------------------------------------------


def test_h1_scores_per_contract():
    assert check_h1_presence(ev(h1_count=0)).score == 30
    multi = check_h1_presence(ev(h1_count=2))
    assert multi.score == 55 and multi.status == "warn"


# 4. url design -----------------------------------------------------------------


def test_url_length_alone_never_fails_and_sentences_are_grammatical():
    long_url = "https://example.com/" + "a" * 130
    o = check_url_design_quality(ev(url=long_url))
    valid(o)
    assert o.status == "pass" and o.score == 85
    assert "This URL longer" not in o.reasoning
    mixed = check_url_design_quality(ev(url=long_url + "?a=1&b=2&c=3"))
    assert mixed.status == "warn"
    assert "This URL is longer than 115 characters" in mixed.reasoning


# 5. content checks -------------------------------------------------------------


def test_content_depth_ignores_contact_pages_noindex_and_non_articles():
    og = {"og:type": "article"}
    contact = ev(url="https://example.com/contact-us", og=og, word_count=300)
    assert check_content_depth(contact).status == "n_a"
    thank = ev(url="https://example.com/thank-you", og=og, schema_types=["Article"], word_count=40)
    assert check_content_depth(thank).status == "n_a"
    noindex = ev(url="https://example.com/blog/x", og=og, word_count=100, noindex=True)
    assert check_content_depth(noindex).status == "n_a"
    real = ev(url="https://example.com/blog/x", og=og, word_count=100)
    assert check_content_depth(real).score == 55


def test_thin_content_and_ratio_do_not_judge_noindex_or_utility_pages():
    assert check_thin_content(ev(word_count=30, noindex=True)).status == "n_a"
    assert (
        check_thin_content(ev(url="https://example.com/thank-you", word_count=30)).status == "n_a"
    )
    assert check_thin_content(ev(word_count=30)).status in ("warn", "fail")
    thin = ev(word_count=40, text_bytes=600, response_bytes=150_000)
    assert check_text_html_ratio(thin).status == "n_a"
    fat = ev(word_count=900, text_bytes=600, response_bytes=150_000)
    assert check_text_html_ratio(fat).status == "warn"
    assert (
        check_text_html_ratio(
            ev(word_count=900, noindex=True, text_bytes=1, response_bytes=9_000)
        ).status
        == "n_a"
    )


def test_soft_404_needs_an_error_signal_not_word_count_alone():
    page = ev(
        http_status=200,
        title="About us",
        word_count=38,
        headings=[{"level": 1, "text": "About"}],
        h1_count=1,
    )
    assert check_soft_404_detection(page).status == "pass"
    err = ev(http_status=200, title="Page Not Found", word_count=38)
    assert check_soft_404_detection(err).status == "fail"


# 6. images ---------------------------------------------------------------------

PLACEHOLDER = {"src": None, "alt": "logo", "width": None, "height": None}
PIXEL = img(src="https://www.facebook.com/tr?id=1&noscript=1", width=None, height=None, alt=None)
ONE = img(src="https://example.com/t.gif", width=1, height=1, alt=None)


def test_dimension_check_skips_placeholders_pixels_and_trackers():
    items = [img(), PLACEHOLDER, PIXEL, ONE]
    o = check_image_dimension_attrs(ev(image_count=4, image_items=items))
    assert o.status == "pass" and o.score == 100
    only = check_image_dimension_attrs(ev(image_count=2, image_items=[PLACEHOLDER, PIXEL]))
    assert only.status == "n_a"


def test_alt_check_is_n_a_without_an_inventory_and_exempts_decorative_and_pixels():
    legacy = ev(image_count=20, images_missing_alt=6, image_items=[])
    assert check_image_alt_presence(legacy).status == "n_a"
    items = [img(alt="x"), img(alt=""), img(alt=""), ONE, PIXEL, PLACEHOLDER]
    o = check_image_alt_presence(ev(image_count=6, image_items=items))
    assert o.status == "pass"
    bad = check_image_alt_presence(ev(image_count=2, image_items=[img(alt=None), img(alt="y")]))
    assert bad.issue_count == 1


def test_broken_images_ignores_noscript_tracking_pixel():
    pixel = dict(PIXEL, http_status=404, content_type="text/html")
    o = check_broken_images(ev(image_count=1, image_items=[pixel]))
    assert o.status == "n_a"
    html = (
        "<html><head><title>x</title></head><body>"
        '<noscript><img src="https://www.facebook.com/tr?id=1&noscript=1"></noscript>'
        '<img src="/a.jpg" alt="a" width="5" height="5"></body></html>'
    )
    result = audit_html(html, "https://example.com/")
    assert result.images_total == 1


def test_lazy_loading_uses_regions_and_src_only_featured_match():
    # Header logos/badges no longer use up the "first 3" slots, so the 4th picture
    # (a lazy below-fold image) is judged below the fold, not as a lazy hero.
    header = [img(src=f"https://example.com/badge{i}.png", region="header") for i in range(2)]
    content = [img(src=f"https://example.com/c{i}.jpg", loading="eager") for i in range(3)]
    below = img(src="https://example.com/below.jpg", loading="lazy")
    footer = img(src="https://example.com/twitter-logo.png", region="footer")
    o = check_image_lazy_loading(ev(image_count=7, image_items=[*header, *content, below, footer]))
    assert o.status == "pass", o.reasoning
    # A footer icon that loads eagerly is never reported.
    assert "twitter-logo" not in str(o.evidence)
    # The featured URL inside another copy's srcset does NOT make that copy the hero.
    html = (
        '<html><head><title>t</title><meta property="og:image" content="https://example.com/hero.jpg">'
        "</head><body>"
        + "".join(f'<img src="/e{i}.jpg" alt="a" width="9" height="9">' for i in range(3))
        + '<img src="/copy.jpg" srcset="https://example.com/hero.jpg 1024w" loading="lazy" alt="a" width="9" height="9">'
        "</body></html>"
    )
    items = audit_html(html, "https://example.com/").image_inventory
    assert not any(i.get("featured") for i in items if i["src"].endswith("copy.jpg"))


# 7. social / og ----------------------------------------------------------------


def test_missing_og_image_is_reported_once_and_truthfully():
    og = {k: v for k, v in OG.items() if k != "og:image"}
    social = check_social_meta_completeness(ev(og=og, twitter={"twitter:card": "summary"}))
    assert social.status == "pass"
    assert "og:image" not in (social.evidence or {}).get("missing_og_tags", [])
    o = check_og_image_validity(ev(og=og, twitter={"twitter:image": "https://example.com/t.jpg"}))
    assert o.status == "fail"
    assert "grey" not in o.reasoning and "everywhere" not in o.reasoning
    assert "may share without a picture" in o.reasoning


# 8. mixed content --------------------------------------------------------------


def test_profile_link_is_not_mixed_content():
    html = (
        "<html><head><title>t</title>"
        '<link rel="profile" href="http://gmpg.org/xfn/11">'
        '<link rel="stylesheet" href="http://cdn.example.com/a.css">'
        "</head><body><noscript><img src='http://t.example.com/p.gif'></noscript></body></html>"
    )
    result = audit_html(html, "https://example.com/")
    assert result.mixed_content == ["http://cdn.example.com/a.css"]


# 9. structured data ------------------------------------------------------------


def sd(*blocks) -> dict:
    return {"blocks": list(blocks), "parse_errors": []}


def test_structured_data_no_invented_requirements():
    org = {"source": "json-ld", "types": ["Organization"], "data": {"url": "https://e.com"}}
    assert "Organization" not in seo_audit.RICH_RESULT_REQUIRED_PROPERTIES
    o = check_structured_data_validity(ev(structured_data=sd(org)))
    assert o.status != "fail"  # no "requires name" - Google lists no required properties

    video = {
        "source": "json-ld",
        "types": ["VideoObject"],
        "data": {
            "name": "n",
            "thumbnailUrl": "t",
            "uploadDate": "d",
            "description": "x",
            "duration": "PT1M",
            "embedUrl": "https://e.com/embed",
        },
    }
    assert check_structured_data_validity(ev(structured_data=sd(video))).status == "pass"

    empty_scope = {
        "source": "microdata",
        "types": ["Organization"],
        "data": {"type": "Organization", "value": "Menu Home"},
    }
    o = check_structured_data_validity(ev(structured_data=sd(empty_scope)))
    assert o.status == "pass"


# 10. canonical -----------------------------------------------------------------


def test_missing_canonical_on_noindex_is_n_a_and_on_indexable_is_65():
    assert check_canonical_presence(ev(noindex=True)).status == "n_a"
    o = check_canonical_presence(ev(noindex=False))
    assert o.status == "warn" and o.score == 65
