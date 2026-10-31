"""The in-page clip surgery, run in a REAL headless Chromium against saved HTML.

No DOM double: container choice, sibling removal, junk removal, section scope
and the placeholder sweep all depend on real layout (``innerText``, rendered
size), which only a real browser computes. Each test loads one fixture with
``set_content`` and calls the same ``window.__pressClip`` functions the renderer
calls on a live page.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from matrx_scraper.press_clip.renderer import CLIP_PAGE_JS

FIXTURES = Path(__file__).with_name("fixtures")


@pytest.fixture(scope="module")
async def browser():
    from playwright.async_api import async_playwright

    pw = await async_playwright().start()
    b = await pw.chromium.launch(headless=True)
    try:
        yield b
    finally:
        await b.close()
        await pw.stop()


async def _load(browser, fixture: str):
    page = await browser.new_page(viewport={"width": 1180, "height": 1600})
    # Every subresource is answered locally; the fixture never touches a network.
    await page.route("**/*", lambda route: route.fulfill(status=204, body=""))
    await page.set_content((FIXTURES / fixture).read_text(), wait_until="domcontentloaded")
    await page.evaluate(CLIP_PAGE_JS)
    return page


async def _clip(page, **opts):
    base = {
        "brandName": "",
        "sectionHeading": "",
        "keep": [],
        "drop": [],
        "root": "",
        "logoSrc": "",
        "logoSvg": "",
    }
    base.update(opts)
    return await page.evaluate("(o) => window.__pressClip.clip(o)", base)


async def test_container_is_tightest_candidate_holding_h1_and_most_text(browser):
    page = await _load(browser, "news_article.html")
    picked = await page.evaluate(
        "() => window.__pressClip.describe(window.__pressClip.pickContainer(''))"
    )
    # Not .article-body (no h1), not the footer .post-content recirc card (inside <footer>).
    assert picked == "article#story.story"


async def test_candidates_inside_site_chrome_never_win(browser):
    page = await _load(browser, "news_article.html")
    inside = await page.evaluate(
        "() => window.__pressClip.candidates().some(el => el.closest('header, nav, footer, aside'))"
    )
    assert inside is False


async def test_root_override_wins(browser):
    page = await _load(browser, "news_article.html")
    picked = await page.evaluate(
        "() => window.__pressClip.describe(window.__pressClip.pickContainer('.article-body'))"
    )
    assert picked == "div.article-body"


async def test_siblings_of_ancestor_chain_are_removed_and_story_kept(browser):
    page = await _load(browser, "news_article.html")
    report = await _clip(page)
    assert report["root_selector_used"] == "article#story.story"
    for gone in ("#site-header", ".sidebar", "footer", ".comments"):
        assert await page.locator(gone).count() == 0, gone
    body = await page.inner_text("article")
    assert "room-by-room renovation plan" in body and "primary bathroom" in body
    assert await page.locator("figure.lead-photo img").count() == 1


async def test_hard_junk_and_caller_drop_removed_but_keep_survives(browser):
    page = await _load(browser, "news_article.html")
    await _clip(page, drop=[".sponsored-rail"], keep=[".keep-me"])
    assert await page.locator("[data-ad]").count() == 0
    assert await page.locator("iframe").count() == 0
    assert await page.locator(".newsletter-box").count() == 0
    assert await page.locator(".sponsored-rail:not(.keep-me)").count() == 0
    assert await page.locator(".keep-me").count() == 1


async def test_placeholder_sweep_logs_every_removal_and_keeps_media(browser):
    page = await _load(browser, "news_article.html")
    report = await _clip(page)
    swept = report["removed_placeholders"]
    assert any(s.startswith("div.empty-slot [300×250]") for s in swept), swept
    assert any(s.startswith("aside.inline-promo [300×120]") for s in swept), swept
    assert await page.locator(".empty-slot").count() == 0
    # The photo figure has media and a caption — it is content, never swept.
    assert await page.locator("figure.lead-photo").count() == 1
    assert not any("lead-photo" in s for s in swept)


async def test_section_scope_keeps_lead_and_brand_section_only(browser):
    page = await _load(browser, "roundup_article.html")
    report = await _clip(page, brandName="Recycle Coach", sectionHeading="Recycle Coach")
    assert report["section_applied"] is True
    for kept in ("#lead", "#rc1", "#rc2"):
        assert await page.locator(kept).count() == 1, kept
    for gone in ("#kanopy", "#retrac"):
        assert await page.locator(gone).count() == 0, gone


async def test_section_scope_needs_heading_that_starts_with_the_name(browser):
    page = await _load(browser, "roundup_article.html")
    # "Re-TRAC" is not how any heading starts with "Recycle Coach Inc"; a loose
    # 8-letter prefix ("recycle ") would wrongly match — the full name must lead.
    report = await _clip(page, brandName="Recycle Coach Inc", sectionHeading="Recycle Coach Inc")
    assert report["section_applied"] is False
    for kept in ("#lead", "#kanopy", "#rc1", "#retrac"):
        assert await page.locator(kept).count() == 1, kept


async def test_brand_found_in_text_is_a_plain_search(browser):
    page = await _load(browser, "news_article.html")
    assert (await _clip(page, brandName="Birchwood Avenue Renovation"))["brand_found_in_text"] is True
    page = await _load(browser, "news_article.html")
    assert (await _clip(page, brandName="Harbor Dental Group"))[
        "brand_found_in_text"
    ] is False


async def test_read_meta_reads_the_page(browser):
    page = await _load(browser, "news_article.html")
    meta = await page.evaluate("() => window.__pressClip.readMeta()")
    assert meta == {
        "outlet_name": "Home Project Journal",
        "headline": "Birchwood Avenue Renovation completes its kitchen",
        "byline": "Priya Raman",
        "published_at": "2026-09-20T08:30:00Z",
    }


async def test_read_meta_leaves_absent_fields_null(browser):
    page = await _load(browser, "bare_page.html")
    meta = await page.evaluate("() => window.__pressClip.readMeta()")
    assert meta["headline"] is None
    assert meta["byline"] is None
    assert meta["published_at"] is None


async def test_masthead_logo_is_the_home_linking_image(browser):
    page = await _load(browser, "news_article.html")
    found = await page.evaluate("() => window.__pressClip.detectMastheadLogo()")
    assert found["logoSrc"].endswith("/static/logo-home-project-journal.png")


async def test_masthead_svg_is_found_and_stamped_dark(browser):
    page = await _load(browser, "roundup_article.html")
    found = await page.evaluate("() => window.__pressClip.detectMastheadLogo()")
    assert found["logoSvg"].startswith("<svg")
    await _clip(page, logoSvg=found["logoSvg"])
    stamped = await page.inner_html(".pc-logo")
    assert 'fill="#111"' in stamped and "#ffffff" not in stamped.lower()


async def test_logo_is_stamped_large_at_the_top(browser):
    page = await _load(browser, "news_article.html")
    await _clip(page, logoSrc="https://cdn.example/logo.png")
    first = await page.evaluate("() => document.body.firstElementChild.className")
    assert first == "pc-header"
    height = await page.evaluate("() => document.querySelector('.pc-header img').style.height")
    assert height == "64px"


async def test_text_wordmark_only_when_no_logo(browser):
    page = await _load(browser, "news_article.html")
    await _clip(page)
    assert await page.inner_text(".pc-header") == "Home Project Journal"


async def test_headline_element_is_found_by_its_text_not_by_being_the_first_h1(browser):
    page = await _load(browser, "headline_not_h1.html")
    report = await _clip(page, brandName="ERI")
    # No article/main/entry-content holds the headline; the tightest ancestor of the
    # real headline that holds a body's worth of text is the container.
    assert report["root_selector_used"] == "div.col-inner"
    assert report["brand_found_in_text"] is True
    assert await page.locator(".col-side").count() == 0
    assert "joint venture called ERI India" in await page.inner_text("body")


async def test_visible_byline_and_date_are_read_when_meta_is_absent(browser):
    page = await _load(browser, "headline_not_h1.html")
    meta = await page.evaluate("() => window.__pressClip.readMeta()")
    assert meta["headline"] == "ERI and Ecoreco join forces to launch ERI India"
    assert meta["byline"] == "CD Bureau"
    assert meta["published_at"] == "September 02, 2026"


async def test_author_meta_that_is_the_outlet_name_is_not_a_byline(browser):
    page = await _load(browser, "infinite_scroll.html")
    meta = await page.evaluate("() => window.__pressClip.readMeta()")
    assert meta["byline"] == "ERIN MCCORMICK"
    assert meta["headline"] == "Datacenter rush will create a tsunami of discarded electronics"
    assert meta["published_at"] == "Sep 16, 2026"


async def test_container_marked_before_infinite_scroll_appends_more_stories(browser):
    page = await _load(browser, "infinite_scroll.html")
    await page.evaluate("() => window.__pressClip.markContainer('')")
    # Scrolling appends the next stories into <main>, each with its own h1.
    await page.evaluate(
        """() => { for (let i = 0; i < 5; i++) { const a = document.createElement('article');
             a.innerHTML = '<h1>Next story ' + i + '</h1><p>' + 'Unrelated text. '.repeat(120) + '</p>';
             document.querySelector('main').appendChild(a); } }"""
    )
    report = await _clip(page)
    assert report["root_selector_used"] == "article#first"
    assert "Next story" not in await page.inner_text("body")


async def test_blank_line_spacers_are_typography_not_placeholders(browser):
    page = await _load(browser, "news_article.html")
    report = await _clip(page)
    assert await page.locator(".blank-line").count() == 1
    assert not any("blank-line" in s for s in report["removed_placeholders"])


async def test_final_sweep_removes_late_overlays_and_fixed_bars_but_not_the_story(browser):
    page = await _load(browser, "news_article.html")
    await page.evaluate("() => window.__pressClip.markContainer('')")
    await _clip(page, logoSrc="https://cdn.example/logo.png", keep=[".keep-me"])
    # A consent manager injects its window AFTER the surgery; a share bar is fixed.
    await page.evaluate(
        """() => {
          const c = document.createElement('div'); c.className = 'consent-window';
          c.innerHTML = '<div role="dialog" style="position:fixed;bottom:0;height:120px">We use cookies</div>';
          document.body.appendChild(c);
          const bar = document.createElement('div'); bar.className = 'share-bar';
          bar.style.cssText = 'position:fixed;top:0;height:40px;width:100%'; bar.textContent = 'Share';
          document.querySelector('article').appendChild(bar);
          const k = document.querySelector('.keep-me'); k.style.position = 'fixed';
        }"""
    )
    removed = await page.evaluate("(k) => window.__pressClip.finalSweep(k)", [".keep-me"])
    assert await page.locator(".consent-window").count() == 0
    assert await page.locator(".share-bar").count() == 0
    assert await page.locator(".keep-me").count() == 1
    assert await page.locator(".pc-header").count() == 1
    assert "room-by-room renovation plan" in await page.inner_text("article")
    assert any(r.startswith("div.consent-window") for r in removed), removed
    assert any(r.startswith("div.share-bar") for r in removed), removed


async def test_overlays_reinjected_after_the_final_sweep_stay_hidden(browser):
    page = await _load(browser, "news_article.html")
    await page.evaluate("() => window.__pressClip.markContainer('')")
    await _clip(page, logoSrc="https://cdn.example/logo.png")
    await page.evaluate("(k) => window.__pressClip.finalSweep(k)", [])
    # A consent manager that notices its window was removed puts it straight back.
    await page.evaluate(
        """() => { const c = document.createElement('div'); c.className = 'consent-again';
             c.textContent = 'We use cookies'; document.body.appendChild(c); }"""
    )
    shown = await page.evaluate(
        "() => getComputedStyle(document.querySelector('.consent-again')).display"
    )
    assert shown == "none"
    assert await page.is_visible("article")
    assert await page.is_visible(".pc-header")


async def test_photos_set_as_css_backgrounds_survive_the_placeholder_sweep(browser):
    page = await _load(browser, "background_photo.html")
    report = await _clip(page)
    swept = report["removed_placeholders"]
    # A box whose only content is a background image is a photo, not an empty slot.
    for kept in (".hero-photo", ".inline-figure", ".photo-bg", ".inline-bg"):
        assert await page.locator(kept).count() == 1, (kept, swept)
    # The truly empty slot is still swept.
    assert any(s.startswith("div.empty-slot [300×250]") for s in swept), swept
    assert await page.locator(".empty-slot").count() == 0


async def test_brand_found_in_text_matches_whole_words_only(browser):
    # "Coach" is not the word "Coaching"; "Lakeside" inside "Lakeside Coaching" is a whole word.
    for name, found in (("Coach", False), ("Lake", False), ("Lakeside", True),
                        ("lakeside coaching", True), ("Studio", True), ("Train", False)):
        page = await _load(browser, "background_photo.html")
        assert (await _clip(page, brandName=name))["brand_found_in_text"] is found, name


async def test_blank_ad_slots_are_swept_whatever_placeholder_they_carry(browser):
    """Break: any background-image counted as a photo, so 300×250, 300×600 and 728×90 ad slots
    holding a skeleton gradient, a spinner or a 1×1 inline image survived into the clip."""
    page = await _load(browser, "blank_ad_slots.html")
    report = await _clip(page)
    swept = report["removed_placeholders"]
    for slot in (".slot-skeleton", ".slot-spinner", ".slot-pixel", ".slot-svg-loader", ".slot-img-pixel"):
        assert await page.locator(slot).count() == 0, (slot, swept)
    assert any(s.startswith("div.slot-pixel [728×90]") for s in swept), swept
    # Real pictures stay, an ad-sized one included. (Their classes avoid the word "ad": since review 4 an
    # ad class or id overrides the media inside it.)
    for kept in (".hero-photo", ".photo-in-iab-size", ".figure-in-iab-size"):
        assert await page.locator(kept).count() == 1, (kept, swept)


async def test_the_photo_rules_are_the_hosts(browser):
    """The size threshold, spinner patterns and ad sizes come from the caller (the press.clip
    photo_rules knob); with no ad sizes and no spinner patterns, a spinner is a picture again."""
    page = await _load(browser, "blank_ad_slots.html")
    await _clip(page, photo={"spinnerPatterns": [], "adSlotSizes": []})
    assert await page.locator(".slot-spinner").count() == 1
    assert await page.locator(".slot-skeleton").count() == 0  # a gradient is never a picture


async def test_the_page_defaults_are_the_python_seeds(browser):
    """clip_page.js's PHOTO_DEFAULTS and renderer.PHOTO_RULE_SEEDS are one list (the knob's seed)."""
    from matrx_scraper.press_clip.renderer import photo_rules_for_page

    page = await _load(browser, "bare_page.html")
    assert await page.evaluate("() => window.__pressClip.PHOTO_DEFAULTS") == photo_rules_for_page(None)


async def test_a_box_holding_real_media_is_never_swept(browser):
    """Break (third adversarial review): a real <img> under a "/1x1/" ratio-crop path, a lazy image
    whose picture waits in data-src / data-lazy-src, background photos at Cloudinary ar_1x1 or in a
    /placeholders-replaced/ folder, a <picture> with a srcset, and a 300×250 YouTube embed were all
    swept as ad slots. Only a box with no real media AND an ad-slot signature is swept."""
    page = await _load(browser, "media_is_never_an_ad_slot.html")
    report = await _clip(page)
    swept = report["removed_placeholders"]
    for kept in (".img-ratio", ".lazy-headshot", ".lazy-placeholder", ".bg-ratio", ".bg-placeholder-path",
                 ".picture-only", ".iframe-video"):
        assert await page.locator(kept).count() == 1, (kept, swept)
    assert await page.locator(".iframe-video iframe").count() == 1, "the video embed itself stays"
    # Real ad slots still go: an ad class with a spinner (not an IAB size), and an ad iframe at 300×250.
    assert await page.locator(".ad-wrapper").count() == 0, swept
    assert await page.locator(".story-promo-frame").count() == 0, swept
    assert any(s.startswith("div.ad-wrapper [410×130]") for s in swept), swept


ROUND4_KEPT = (".k-video-source", ".k-video-lazy-source", ".k-video-bare-source", ".k-svg-chart", ".k-figure-svg",
               ".k-canvas-chart", ".k-datawrapper", ".k-flourish", ".k-infogram", ".k-spotify", ".k-soundcloud",
               ".k-twitter", ".k-instagram", ".k-mixed-chart")
ROUND4_SWEPT = (".a-gpt-img", ".a-native-card", ".sponsored-tile", ".a-outbrain-tile", ".a-labelled-tile",
                ".a-outstream", ".a-jw", ".a-mixed-ad")
# Since review 5 a box holding real media needs TWO ad signals: an id word alone ("ad-slot-chart") around a
# Datawrapper chart is one signal, so the chart stays (its iframe is an editorial embed with no ad mark).
ROUND4_ONE_SIGNAL_KEPT = (".a-chart-in-ad",)


async def test_body_media_is_kept_charts_embeds_and_lazy_video_included(browser):
    """Break (fourth adversarial review): inline SVG and canvas charts, Datawrapper / Flourish / Infogram
    charts, Spotify / SoundCloud / Twitter / Instagram embeds and a <video> whose only source is a child
    <source> (lazy, or with no src at all) were swept from the article body."""
    page = await _load(browser, "body_media_and_real_ads.html")
    report = await _clip(page)
    swept = report["removed_placeholders"]
    for kept in ROUND4_KEPT:
        assert await page.locator(kept).count() == 1, (kept, swept)
    for embed in (".k-datawrapper iframe", ".k-flourish iframe", ".k-spotify iframe", ".k-instagram iframe"):
        assert await page.locator(embed).count() == 1, embed


async def test_strong_ad_signals_override_the_media_an_ad_carries(browser):
    """Break: an ad-network creative in an ad box, image-only Taboola / Outbrain / sponsor tiles, an
    outstream <video> ad and a jwplayer frame in an ad container were kept because they held media."""
    page = await _load(browser, "body_media_and_real_ads.html")
    report = await _clip(page)
    swept = report["removed_placeholders"]
    for ad in ROUND4_SWEPT:
        assert await page.locator(ad).count() == 0, (ad, swept)
    for kept in ROUND4_ONE_SIGNAL_KEPT:
        assert await page.locator(kept).count() == 1, (kept, swept)
    assert any(s.startswith("div.a-gpt-img [300×250]") for s in swept), swept
    # The story text is untouched.
    assert "grant the owners plan" in await page.locator("article").inner_text()


async def test_the_editorial_embed_and_ad_network_lists_are_the_hosts(browser):
    """The lists come from the press.clip.photo_rules knob: with no editorial hosts a chart frame is junk
    again, and with no ad-network hosts or ad words an image tile linking to one is a picture again."""
    page = await _load(browser, "body_media_and_real_ads.html")
    await _clip(page, photo={"editorialEmbedHosts": [], "adNetworkHosts": [], "adMarkerWords": []})
    assert await page.locator(".k-flourish iframe").count() == 0
    assert await page.locator(".a-outbrain-tile").count() == 1


REVIEW5_KEPT = (".k0", ".k13", ".k1", ".k2", ".k3", ".k4", ".k5", ".k6", ".k7", ".k8", ".k9", ".k10", ".k11", ".k12",
                ".m3", ".k-no-ads-hero", ".k-tiktok", ".k-tweet", ".k-youtube")
REVIEW5_SWEPT = (".a1", ".a2", ".a3", ".a4", ".m1", ".m2", ".m4", ".m5")


async def test_one_ad_signal_never_sweeps_a_body_photo(browser):
    """Break (fifth adversarial review): all 12 captionless body photos were swept on one weak signal —
    ad-hoc-gallery, "lead ad", leaderboard, hero-billboard, gpt-illustration, sponsor-logos, adv-column-photo,
    promoted-story-image, id ad-free-hero, data-ad-free, an ads-media. sub-domain, utm_medium=display."""
    page = await _load(browser, "ad_rule_needs_two_signals.html")
    report = await _clip(page)
    swept = report["removed_placeholders"]
    for kept in REVIEW5_KEPT:
        assert await page.locator(kept).count() == 1, (kept, swept)
    for embed in (".k-tiktok iframe", ".k-tweet iframe", ".k-youtube iframe"):
        assert await page.locator(embed).count() == 1, embed


async def test_two_ad_signals_or_an_ad_embed_url_sweep_the_box(browser):
    """Break: an ad server path containing "tiktok.com/embed" passed as a TikTok embed; a promoted-tweet
    frame and a "sponsored" maps pin passed as editorial embeds. Two signals (token + ad-network link,
    token + ad size with no caption, a data-ad-slot at an ad size) sweep a box holding a picture."""
    page = await _load(browser, "ad_rule_needs_two_signals.html")
    report = await _clip(page)
    swept = report["removed_placeholders"]
    for ad in REVIEW5_SWEPT:
        assert await page.locator(ad).count() == 0, (ad, swept)
    assert "grant the owners plan" in await page.locator("article").inner_text()


REVIEW6_KEPT = (".k0", ".k1", ".k2", ".k3", ".k4")
REVIEW6_SWEPT = (".a1", ".a2", ".a3", ".a4", ".a5", ".a6", ".a7")


async def test_strong_ad_marks_sweep_alone_and_layout_compounds_never_mark(browser):
    """Break (sixth adversarial review): a responsive house ad with the class "ad" and a data-sponsor box
    stayed, "advertorial" was never caught, and a 300×250 editorial photo with the camelCase class "headAd"
    (plus data-ad-exclude, data-ad-position and ads-disabled photos) was swept. An exact "ad"/"ads" class,
    advertorial and known ad attributes are strong alone; "ad" glued to a layout word is not an ad."""
    page = await _load(browser, "ad_tokens_strong_and_compound.html")
    report = await _clip(page)
    swept = report["removed_placeholders"]
    for kept in REVIEW6_KEPT:
        assert await page.locator(kept).count() == 1, (kept, swept)
    for ad in REVIEW6_SWEPT:
        assert await page.locator(ad).count() == 0, (ad, swept)
    assert "grant the owners plan" in await page.locator("article").inner_text()


REVIEW7_KEPT = tuple(f".e{i}" for i in range(1, 11))
REVIEW7_SWEPT = tuple(f".m{i}" for i in range(1, 8))


async def test_only_known_ad_attributes_are_strong_and_editorial_ad_attributes_never_mark(browser):
    """Break (seventh adversarial review): any data-ad-* outside a short negation list, and any data-sponsor-*,
    was a strong mark alone, so editorial figures with data-ad-avoid, data-ad-skip, data-ad-break-after,
    data-ad-ignore, data-ad-insertion="none" and data-sponsor-credit were swept, while a Google slot marked only
    by data-google-query-id stayed. Now only known ad-server attributes (data-ad-slot, data-ad-client,
    data-google-query-id...) and a truthy data-sponsor / data-sponsored are strong; an attribute saying avoid,
    skip, ignore, none, break, insertion, credit or exclude is editorial; any other data-ad-* is weak."""
    page = await _load(browser, "ad_attributes_editorial_and_known.html")
    report = await _clip(page)
    swept = report["removed_placeholders"]
    for kept in REVIEW7_KEPT:
        assert await page.locator(kept).count() == 1, (kept, swept)
    for ad in REVIEW7_SWEPT:
        assert await page.locator(ad).count() == 0, (ad, swept)
    assert "MRI scans" in await page.locator("article").inner_text()


async def _count(page, selector: str) -> int:
    return await page.evaluate("(s) => document.querySelectorAll(s).length", selector)


async def test_root_selector_used_matches_exactly_one_element_on_the_unclipped_page(browser):
    # Four sibling div.col-md-12 hold the menu, the story and two teasers: `div.col-md-12` (the old record)
    # matches all four, so a reviewer opening the page by it lands on the menu.
    page = await _load(browser, "duplicate_root_class.html")
    assert await _count(page, "div.col-md-12") == 4
    picked = await page.evaluate("() => { const e = window.__pressClip.pickContainer(''); e.setAttribute('data-pc-root','1'); return window.__pressClip.describe(e); }")
    assert picked == "div.col-md-12"
    report = await _clip(page)
    selector = report["root_selector_used"]
    assert selector != "div.col-md-12"
    # The record is checked on a fresh, unclipped copy of the same page: it must find the story and only the story.
    fresh = await _load(browser, "duplicate_root_class.html")
    assert await _count(fresh, selector) == 1, selector
    assert "Story-top-sec" in await fresh.evaluate(
        "(s) => document.querySelector(s).innerHTML", selector
    )


async def test_unique_selector_keeps_the_readable_form_when_it_is_already_unique(browser):
    page = await _load(browser, "news_article.html")
    report = await _clip(page)
    assert report["root_selector_used"] == "article#story.story"


async def test_unique_selector_agrees_with_the_server_root_finder(browser):
    # One rule, two implementations (clip_page.js and aidream root_candidates.stable_selector): on the same page
    # both selectors must point at the same single element.
    pytest.importorskip("lxml")
    try:
        from aidream.services.press_clip.root_candidates import root_candidates_from_html
    except ImportError:
        pytest.skip("aidream is not importable from the scraper package's environment")
    html = (FIXTURES / "duplicate_root_class.html").read_text()
    server = root_candidates_from_html(html, headline="Recycler opens new certified e-waste processing line")
    page = await _load(browser, "duplicate_root_class.html")
    js_sel = await page.evaluate(
        "() => window.__pressClip.uniqueSelector(window.__pressClip.pickContainer(''))"
    )
    assert await _count(page, server["suggested_root"]) == 1
    same = await page.evaluate(
        "([a, b]) => document.querySelector(a) === document.querySelector(b)",
        [js_sel, server["suggested_root"]],
    )
    assert same, (js_sel, server["suggested_root"])
