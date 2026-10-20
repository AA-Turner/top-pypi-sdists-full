"""The coverage map, the honest failure judge, the advanced-fallback knob and the agent hint line.

Examples are real reads from scrape history (``scraper.scrape_parsed_page``, 2026-10-16): a
Cloudflare "Just a moment..." toasttab order page, an Instagram caption of 26 characters (a REAL
read), example.com's 127-character page (real), a paywall teaser, a sign-in page.
"""

from __future__ import annotations

from typing import Any

import pytest

from matrx_scraper import _ext
from matrx_scraper import coverage as cov
from matrx_scraper.features import read_page as rp
from matrx_scraper.read_judge import (
    CHALLENGE,
    EMPTY,
    FETCH_ERROR,
    HTTP_ERROR,
    JS_SHELL,
    SIGN_IN_WALL,
    judge_read,
)

_KEYS = (cov.EXT_PRICE, cov.EXT_SPEED, cov.EXT_SOCIAL_DETECT, cov.EXT_MODE, cov.EXT_READER, cov.EXT_CLIENT, cov.EXT_RUN_SLOT)


@pytest.fixture(autouse=True)
def _clean_ext():
    saved = {k: _ext._registry[k] for k in _KEYS if k in _ext._registry}
    for k in _KEYS:
        _ext._registry.pop(k, None)
    yield
    for k in _KEYS:
        _ext._registry.pop(k, None)
    _ext._registry.update(saved)


# ── judge_read: strong signals only ──────────────────────────────────────


@pytest.mark.parametrize(
    ("kwargs", "reason"),
    [
        # toasttab order page, 262 chars, title "Just a moment..." (Cloudflare)
        ({"title": "Just a moment...", "text": "www.toasttab.com Verifying you are human. This may take a few seconds."},
         CHALLENGE),
        ({"text": "Verifying you are not a robot. Please wait while we check your browser."}, CHALLENGE),
        ({"title": "Robot or human?", "text": "Activate and hold the button to confirm that you're human."}, CHALLENGE),
        ({"title": "Access Denied", "text": "You don't have permission to access this page on this server."}, CHALLENGE),
        ({"text": "Are you human? Press & Hold to confirm you are a human (and not a bot)."}, CHALLENGE),
        ({"status": 403, "text": "Forbidden"}, HTTP_ERROR),
        ({"status": 404, "text": "Page not found"}, HTTP_ERROR),
        ({"status": 200, "text": ""}, EMPTY),
        ({"text": "", "fetch_failure": "request_error"}, FETCH_ERROR),
        ({"text": "", "fetch_failure": "cloudflare_block"}, CHALLENGE),
        ({"text": "You need to enable JavaScript to run this app."}, JS_SHELL),
        ({"text": "Loading", "html": '<html><body><div id="root"></div><script src="/app.js"></script></body></html>'},
         JS_SHELL),
        ({"title": "Log in • Instagram", "text": "Log in to see photos and videos from friends."}, SIGN_IN_WALL),
        ({"title": "Sign in to your account", "text": "Email, phone, or Skype. Can't access your account?"},
         SIGN_IN_WALL),
        ({"text": "Join LinkedIn. Sign in to view the full profile of this member."}, SIGN_IN_WALL),
    ],
)
def test_strong_signals_fail(kwargs: dict[str, Any], reason: str):
    v = judge_read(**kwargs)
    assert v.failed and v.reason == reason, v
    assert v.detail  # plain words, always


@pytest.mark.parametrize(
    "kwargs",
    [
        # Instagram reel: the caption IS the content (26 chars) — a short page is not a failure
        {"status": 200, "title": "“I need to apologize Alex”", "text": "“I need to apologize Alex”"},
        # example.com, 127 chars
        {"status": 200, "title": "Example Domain",
         "text": "This domain is for use in illustrative examples in documents. You may use this domain in "
                 "literature without prior coordination."},
        # nltimes paywall-ish teaser, ~280 chars of related links
        {"status": 200, "title": "Most data centers refusing to say how much water, electricity they use",
         "text": "More like this: Dutch emissions increased in 2025; Climate goals further out of reach. "
                 "Construction permit granted for massive data center in Amsterdam Zuidoost."},
        # a long article that mentions "access denied" is an article
        {"status": 200, "title": "Why 'Access Denied' errors happen", "text": "word " * 600 + "access denied"},
        # a long page with a JS reminder in the footer is not a shell
        {"status": 200, "text": "real content " * 40 + " Please enable JavaScript for comments."},
    ],
)
def test_short_or_odd_but_real_pages_pass(kwargs: dict[str, Any]):
    v = judge_read(**kwargs)
    assert not v.failed, v


# Real examples (scrape history 2026-10-16, exact stored text) the first judge let through.
_LINKEDIN_WALL = (
    "# Sign in\nor\n[Forgot password?](https://www.linkedin.com/checkpoint/rp/request-password-reset?session_redirect="
    "%2Fsearch%2Fresults%2Fpeople%2F%3FfirstName%3D%2522Ellie%2522%26lastName%3D%2522Sadeghi%2522)\n"
    "## We\u2019ve emailed a one-time link to your primary email address\nClick on the link to sign in instantly to "
    "your LinkedIn account.\nIf you don\u2019t see the email in your inbox, check your spam folder.\nNew to LinkedIn? "
    "[Join now](https://www.linkedin.com/signup/cold-join?session_redirect=%2Fsearch%2Fresults%2Fpeople%2F)\n"
    "Agree & Join LinkedIn\nBy clicking Continue, you agree to LinkedIn\u2019s [User Agreement]"
    "(https://www.linkedin.com/legal/user-agreement) , [Privacy Policy](https://www.linkedin.com/legal/privacy-policy) , "
    "and [Cookie Policy](https://www.linkedin.com/legal/cookie-policy) ."
)


@pytest.mark.parametrize(
    ("kwargs", "reason"),
    [
        ({"status": 200, "title": "LinkedIn Login, Sign in | LinkedIn", "text": _LINKEDIN_WALL}, SIGN_IN_WALL),
        ({"status": 200, "text": _LINKEDIN_WALL}, SIGN_IN_WALL),
        ({"status": 200, "title": "Please Wait",
          "text": "# Please wait\nWe are optimizing your request for the best experience.\n\nPlease Wait"}, CHALLENGE),
        ({"status": 200, "title": "TikTok - Make Your Day",
          "text": "\n[Watch Unknown Video](https://lf16-tiktok-web.tiktokcdn-us.com/obj/tiktok-web-tx/tiktok/webapp/main/"
                  "webapp-desktop/playback1.mp4)"}, JS_SHELL),
    ],
)
def test_real_walls_and_shells_the_first_judge_missed_now_fail(kwargs: dict[str, Any], reason: str):
    v = judge_read(**kwargs)
    assert v.failed and v.reason == reason and v.coverable, v


def test_a_real_404_with_a_whole_article_is_failed_but_carries_no_coverage():
    wiki = ("Readwise is not a page on Wikipedia. Wikipedia does not have an article with this exact name. "
            "Search for this page title in Wikipedia to check for alternative titles or spellings. " * 12)
    v = judge_read(status=404, title="Readwise - Wikipedia", text=wiki)
    assert v.failed and v.reason == HTTP_ERROR and v.coverable is False
    assert judge_read(status=410, text="Gone").coverable is False
    for status in (401, 403, 429, 500, 503):
        assert judge_read(status=status, text="Forbidden").coverable is True


async def test_a_404_page_is_not_offered_coverage_or_a_paid_retry(monkeypatch):
    calls: list[Any] = []

    async def reader(urls, allow):
        calls.append(urls)
        return [{"url": urls[0], "ok": True, "text": "paid"}]

    async def missing(u: str):
        return ({"status": "success", "text": "Wikipedia does not have an article with this exact name. " * 40},
                judge_read(status=404, text="Wikipedia does not have an article with this exact name. " * 40))

    _ext.configure_ext(brightdata_client=_Unlocking(), coverage_price=_price, advanced_fallback_mode=_mode("fast"),
                       advanced_reader=reader)
    monkeypatch.setattr(rp, "_read_page_http_judged", missing)
    out = await rp.read_page_mcp_quick(url="https://en.wikipedia.org/wiki/Readwise")
    assert calls == [] and out["status"] == "error" and out["coverage"] == []
    assert out["verdict"]["reason"] == HTTP_ERROR


# ── coverage map ─────────────────────────────────────────────────────────


class _Unlocking:
    async def unlock(self, url: str):  # pragma: no cover - shape only
        raise AssertionError


async def _price(service: str, source_key: str | None, org: str | None):
    return {"unlocker": (0.0015, 30), "social": (0.002, 40), "structured": (0.0015, 30)}[service]


def _social(url: str):
    return "instagram" if "instagram.com" in url else None


async def test_coverage_is_empty_without_any_reader_and_for_non_web():
    assert await cov.coverage_for("https://example.com/x") == []
    _ext.configure_ext(brightdata_client=_Unlocking())
    assert await cov.coverage_for("mailto:someone@example.com") == []


async def test_any_page_is_covered_by_the_fast_unlocker_with_its_price():
    _ext.configure_ext(brightdata_client=_Unlocking(), coverage_price=_price)
    out = await cov.coverage_for("https://www.toasttab.com/local/order/bard-coffee-185-middle-st")
    assert [c.service for c in out] == ["unlocker"]
    c = out[0]
    assert c.speed == "fast" and c.points_per_unit == 30 and c.label == "advanced reader" and c.unit == "page"


async def test_a_social_profile_puts_the_social_reader_first():
    _ext.configure_ext(brightdata_client=_Unlocking(), coverage_price=_price, social_platform_detector=_social)
    out = await cov.coverage_for("https://www.instagram.com/nasa/")
    assert [c.service for c in out][:2] == ["social", "unlocker"]
    assert out[0].platform == "instagram" and out[0].label == "social reader"


async def test_a_catalog_url_lists_structured_data_last_as_slow():
    _ext.configure_ext(brightdata_client=_Unlocking(), coverage_price=_price)
    out = await cov.coverage_for("https://www.trustpilot.com/review/example.com")
    services = [c.service for c in out]
    assert services[0] == "unlocker" and "structured" in services
    structured = [c for c in out if c.service == "structured"]
    assert all(c.speed in ("research", "batch") and c.source_key for c in structured)


async def test_measured_speed_from_the_host_sets_the_class():
    async def speed(service: str, key: str | None):
        return 45.0 if service == "structured" else None

    _ext.configure_ext(brightdata_client=_Unlocking(), coverage_speed=speed)
    out = await cov.coverage_for("https://www.trustpilot.com/review/example.com")
    s = next(c for c in out if c.service == "structured")
    assert s.typical_seconds == 45.0 and s.speed == "research"


def test_speed_class_never_calls_structured_fast():
    assert cov.speed_class(5, "structured") == "research"
    assert cov.speed_class(None, "structured") == "batch"
    assert cov.speed_class(7, "unlocker") == "fast"


# ── the agent hint line ──────────────────────────────────────────────────


def test_hint_line_is_one_short_line_only_when_failed_pages_are_covered():
    assert cov.hint_line([]) is None
    assert cov.hint_line([("https://a.example", [])]) is None
    unl = {"service": "unlocker", "speed": "fast", "typical_seconds": 7.0, "points_per_unit": 30}
    soc = {"service": "social", "speed": "fast", "typical_seconds": 9.0, "points_per_unit": 40}
    line = cov.hint_line([("https://a", [unl]), ("https://b", [unl]), ("https://ig", [soc, unl])])
    assert line is not None and "\n" not in line
    assert line.startswith("3 pages failed") and "1 via the social reader" in line
    assert "advanced_read" in line and "only if you have no better source" in line
    for vendor in ("bright", "scrapecreators", "unlocker zone"):
        assert vendor not in line.lower()


def test_hint_line_never_points_an_agent_at_a_slow_reader():
    slow = {"service": "structured", "speed": "batch", "typical_seconds": 600.0, "points_per_unit": 5}
    unl = {"service": "unlocker", "speed": "fast", "typical_seconds": 7.0, "points_per_unit": 30}
    assert cov.hint_line([("https://a", [slow])]) is None  # only slow coverage: say nothing
    line = cov.hint_line([("https://a", [slow]), ("https://b", [unl])])
    assert line is not None and line.startswith("1 page failed")  # the slow-only page is not counted
    for text in (line,):
        assert "allow" not in text and "slow" not in text and "all'" not in text


# ── the knob: off | fast | all ───────────────────────────────────────────


def _wall(url: str):
    async def fake(u: str):
        return ({"status": "success", "text": "Just a moment...", "result": "x", "page": {"text_data": "x"}},
                judge_read(title="Just a moment...", text="Verifying you are human."))
    return fake


def _mode(value: str):
    async def mode() -> str:
        return value
    return mode


async def test_knob_off_carries_coverage_and_runs_nothing(monkeypatch):
    calls: list[Any] = []

    async def reader(urls, allow):
        calls.append((urls, allow))
        return [{"url": urls[0], "ok": True, "text": "paid"}]

    _ext.configure_ext(brightdata_client=_Unlocking(), coverage_price=_price, advanced_fallback_mode=_mode("off"),
                       advanced_reader=reader)
    monkeypatch.setattr(rp, "_read_page_http_judged", _wall("u"))
    out = await rp.read_page_mcp_quick(url="https://www.toasttab.com/x")
    assert calls == [] and out["status"] == "error" and out["text"] == ""
    assert out["verdict"]["reason"] == CHALLENGE and "page" not in out
    assert out["coverage"][0]["service"] == "unlocker" and out["coverage"][0]["points_per_unit"] == 30


async def test_no_host_mode_means_off(monkeypatch):
    calls: list[Any] = []

    async def reader(urls, allow):
        calls.append(urls)
        return []

    _ext.configure_ext(brightdata_client=_Unlocking(), advanced_reader=reader)
    monkeypatch.setattr(rp, "_read_page_http_judged", _wall("u"))
    out = await rp.read_page_mcp_quick(url="https://www.toasttab.com/x")
    assert calls == [] and out["coverage"]


async def test_knob_fast_retries_through_the_door_and_says_which_reader(monkeypatch):
    calls: list[Any] = []

    async def reader(urls, allow):
        calls.append((urls, allow))
        return [{"url": urls[0], "ok": True, "service": "unlocker", "reader": "advanced reader", "seconds": 6.2,
                 "points": 30, "text": "the real menu", "message": "Read by the advanced reader in 6.2 s (30 points)."}]

    _ext.configure_ext(brightdata_client=_Unlocking(), advanced_fallback_mode=_mode("fast"), advanced_reader=reader)
    monkeypatch.setattr(rp, "_read_page_http_judged", _wall("u"))
    out = await rp.read_page_mcp_quick(url="https://www.toasttab.com/x")
    assert calls == [(["https://www.toasttab.com/x"], "fast")]
    assert out["status"] == "success" and out["text"] == "the real menu" and out["engine"] == "advanced_read"
    assert out["advanced_read"]["points"] == 30 and "text" not in out["advanced_read"]


async def test_fast_retries_stop_at_the_per_run_ceiling_and_keep_the_coverage_note(monkeypatch):
    calls: list[Any] = []
    left = [2]

    async def reader(urls, allow):
        calls.append(urls[0])
        return [{"url": urls[0], "ok": True, "text": "paid", "points": 30}]

    async def slot() -> bool:
        if left[0] <= 0:
            return False
        left[0] -= 1
        return True

    _ext.configure_ext(brightdata_client=_Unlocking(), coverage_price=_price, advanced_fallback_mode=_mode("fast"),
                       advanced_reader=reader, advanced_fallback_run_slot=slot)
    monkeypatch.setattr(rp, "_read_page_http_judged", _wall("u"))
    outs = [await rp.read_page_mcp_quick(url=f"https://www.toasttab.com/{i}") for i in range(4)]
    assert calls == ["https://www.toasttab.com/0", "https://www.toasttab.com/1"]
    assert [o["status"] for o in outs] == ["success", "success", "error", "error"]
    assert outs[3]["coverage"][0]["service"] == "unlocker" and "advanced_read" not in outs[3]


async def test_a_failing_run_slot_hook_spends_nothing(monkeypatch):
    calls: list[Any] = []

    async def reader(urls, allow):
        calls.append(urls)
        return []

    async def broken() -> bool:
        raise RuntimeError("knob unreadable")

    _ext.configure_ext(brightdata_client=_Unlocking(), advanced_fallback_mode=_mode("fast"), advanced_reader=reader,
                       advanced_fallback_run_slot=broken)
    monkeypatch.setattr(rp, "_read_page_http_judged", _wall("u"))
    out = await rp.read_page_mcp_quick(url="https://www.toasttab.com/x")
    assert calls == [] and out["coverage"]


async def test_knob_fast_never_runs_when_only_slow_structured_data_covers(monkeypatch):
    calls: list[Any] = []

    async def reader(urls, allow):
        calls.append(urls)
        return []

    async def only_structured(url, organization_id=None):
        return [cov.Coverage(service="structured", label="structured data", speed="batch", typical_seconds=300,
                             unit="record", points_per_unit=30, returns="records", source_key="k")]

    _ext.configure_ext(advanced_fallback_mode=_mode("fast"), advanced_reader=reader)
    monkeypatch.setattr(cov, "coverage_for", only_structured)
    monkeypatch.setattr(rp, "_read_page_http_judged", _wall("u"))
    out = await rp.read_page_mcp_quick(url="https://www.toasttab.com/x")
    assert calls == [] and out["coverage"][0]["service"] == "structured"


async def test_knob_all_allows_structured(monkeypatch):
    calls: list[Any] = []

    async def reader(urls, allow):
        calls.append(allow)
        return [{"url": urls[0], "ok": False, "message": "No reader could open this page.", "points": 0}]

    async def only_structured(url, organization_id=None):
        return [cov.Coverage(service="structured", label="structured data", speed="batch", typical_seconds=300,
                             unit="record", points_per_unit=30, returns="records", source_key="k")]

    _ext.configure_ext(advanced_fallback_mode=_mode("all"), advanced_reader=reader)
    monkeypatch.setattr(cov, "coverage_for", only_structured)
    monkeypatch.setattr(rp, "_read_page_http_judged", _wall("u"))
    out = await rp.read_page_mcp_quick(url="https://www.toasttab.com/x")
    assert calls == ["all"] and out["status"] == "error" and out["advanced_read"]["ok"] is False


async def test_a_good_read_is_untouched(monkeypatch):
    async def fine(u: str):
        return {"status": "success", "text": "hello " * 100}, judge_read(status=200, text="hello " * 100)

    _ext.configure_ext(brightdata_client=_Unlocking(), advanced_fallback_mode=_mode("all"))
    monkeypatch.setattr(rp, "_read_page_http_judged", fine)
    out = await rp.read_page_mcp_quick(url="https://example.com/")
    assert out["status"] == "success" and "coverage" not in out and "verdict" not in out


# ── research: judged failures are collected with their coverage ──────────


async def test_research_scrape_collects_a_walled_page_with_its_coverage(monkeypatch):
    from types import SimpleNamespace

    from matrx_scraper.features import mcp_tool_helpers as helpers
    from matrx_scraper.scraper import FailureReason

    async def walled(url: str):
        return SimpleNamespace(failed=True, content="", content_bytes=None, status_code=403, title="Just a moment...",
                               failed_primary_reason=FailureReason.CLOUDFLARE_BLOCK)

    _ext.configure_ext(brightdata_client=_Unlocking(), coverage_price=_price)
    monkeypatch.setattr(helpers, "fetch_normally_with_proxy", walled)
    failures: list[dict[str, Any]] = []
    page = await helpers.scrape_url_core("https://www.toasttab.com/x", failures=failures)
    assert page is None and len(failures) == 1
    f = failures[0]
    assert f["verdict"]["reason"] == CHALLENGE and f["coverage"][0]["service"] == "unlocker"
    assert "cloudflare" not in f["verdict"]["detail"].lower()
    assert cov.hint_line([(f["url"], f["coverage"])]).startswith("1 page failed")
