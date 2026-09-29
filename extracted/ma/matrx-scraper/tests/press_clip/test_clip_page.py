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
        "clientName": "",
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


async def test_section_scope_keeps_lead_and_client_section_only(browser):
    page = await _load(browser, "roundup_article.html")
    report = await _clip(page, clientName="Recycle Coach", sectionHeading="Recycle Coach")
    assert report["section_applied"] is True
    for kept in ("#lead", "#rc1", "#rc2"):
        assert await page.locator(kept).count() == 1, kept
    for gone in ("#kanopy", "#retrac"):
        assert await page.locator(gone).count() == 0, gone


async def test_section_scope_needs_heading_that_starts_with_the_name(browser):
    page = await _load(browser, "roundup_article.html")
    # "Re-TRAC" is not how any heading starts with "Recycle Coach Inc"; a loose
    # 8-letter prefix ("recycle ") would wrongly match — the full name must lead.
    report = await _clip(page, clientName="Recycle Coach Inc", sectionHeading="Recycle Coach Inc")
    assert report["section_applied"] is False
    for kept in ("#lead", "#kanopy", "#rc1", "#retrac"):
        assert await page.locator(kept).count() == 1, kept


async def test_client_found_in_text_is_a_plain_search(browser):
    page = await _load(browser, "news_article.html")
    assert (await _clip(page, clientName="Birchwood Avenue Renovation"))["client_found_in_text"] is True
    page = await _load(browser, "news_article.html")
    assert (await _clip(page, clientName="Harbor Dental Group"))[
        "client_found_in_text"
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
    report = await _clip(page, clientName="ERI")
    # No article/main/entry-content holds the headline; the tightest ancestor of the
    # real headline that holds a body's worth of text is the container.
    assert report["root_selector_used"] == "div.col-inner"
    assert report["client_found_in_text"] is True
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
