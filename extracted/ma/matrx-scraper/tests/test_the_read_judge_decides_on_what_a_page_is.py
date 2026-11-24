"""The read judge decides on what a login page or an interstitial IS, never on length plus a keyword (fix round 3).

Round 2's "hollow page" rule failed real pages (a short article with a login form in its header, a blog with a
comment login, an article quoting "verify you are human") and passed shells. The judge now measures the page:
vendor wall markup or a vendor title, a redirect onto a sign-in address, a password form with no content beside
it. Where it cannot settle a read it keeps the page and says so ("possibly an interstitial"), never silently.

Fixtures: ``fixtures/read_judge`` holds real responses captured from this Mac on 2026-11-17 with an ordinary
request (scripts cut to 200 characters, styles and most attributes stripped), plus real-derived pages for the
reviewer's examples; ``manifest.json`` names each source URL, final URL, status, headers and what was changed.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from matrx_scraper import read_judge
from matrx_scraper.read_judge import judge_read, set_read_judge_knobs_source
from selectolax.lexbor import LexborHTMLParser

FIXTURES = Path(__file__).parent / "fixtures" / "read_judge"
MANIFEST = json.loads((FIXTURES / "manifest.json").read_text())


def _judge(entry: dict, **extra):
    html = (FIXTURES / entry["file"]).read_text()
    tree = LexborHTMLParser(html)
    title = entry.get("title") or (tree.css_first("title").text().strip() if tree.css_first("title") else "")
    for node in tree.css("script, style, noscript, template, svg"):
        node.decompose()
    text = tree.body.text(separator=" ") if tree.body else ""
    args = dict(status=entry["status"], text=text, html=html, title=title, headers=entry["headers"],
                final_url=entry["final_url"], requested_url=entry["source"])
    return judge_read(**{**args, **extra})


def _outcome(verdict) -> str:
    return verdict.reason if verdict.failed else ("unsure" if verdict.unsure else "read")


@pytest.mark.parametrize("entry", MANIFEST, ids=[m["file"] for m in MANIFEST])
def test_every_captured_page_is_judged_for_what_it_is(entry: dict) -> None:
    assert _outcome(_judge(entry)) == entry["expect"], entry.get("note", "")


def test_the_reviewers_examples_are_all_in_the_set() -> None:
    names = {m["file"] for m in MANIFEST}
    assert {"article_2500_header_login.html", "blog_2800_comment_login.html", "article_1000_verify_human.html",
            "interstitial_2000_padded.html", "login_landing_3500.html"} <= names
    assert sum(m["kind"] == "real" for m in MANIFEST) >= 15


ART = ("The bakery industry has seen rising costs this year. " * 60)


@pytest.mark.parametrize("text", [
    "Checking your browser before accessing example.com. " + ART[:1900],
    "How captchas work: when a site asks you to verify you are human, it checks signals. " + ART[:900],
])
def test_a_challenge_phrase_with_no_html_is_read_and_marked_never_silent(text: str) -> None:
    verdict = judge_read(status=200, text=text, html=None)
    assert not verdict.failed
    assert verdict.unsure.startswith("possibly an interstitial")


def test_a_sign_in_redirect_fails_and_the_same_address_alone_is_only_unsure() -> None:
    entry = next(m for m in MANIFEST if m["file"] == "reddit_old.html")
    assert _judge(entry).reason == "sign_in_wall"
    alone = judge_read(status=200, text="Welcome", final_url=entry["final_url"])
    assert not alone.failed and alone.unsure.startswith("possibly a sign-in page")


def test_the_thresholds_are_knobs(monkeypatch: pytest.MonkeyPatch) -> None:
    entry = next(m for m in MANIFEST if m["file"] == "so_login.html")
    plain = {**entry, "final_url": None, "source": None, "title": "Stack Overflow"}
    assert _judge(plain).reason == "sign_in_wall"  # a password form with 1 content block beside it
    set_read_judge_knobs_source(lambda: {"login_max_blocks": 0})
    try:
        verdict = _judge(plain)
        assert not verdict.failed and verdict.unsure.startswith("possibly a sign-in page")
    finally:
        set_read_judge_knobs_source(None)


def test_a_broken_knob_reader_is_announced_and_the_defaults_hold(capsys: pytest.CaptureFixture[str]) -> None:
    def broken() -> dict[str, int]:
        raise RuntimeError("knob table unreachable")

    set_read_judge_knobs_source(broken)
    try:
        assert read_judge.judge_knobs() == read_judge.JudgeKnobs()
    finally:
        set_read_judge_knobs_source(None)
    assert "knob table unreachable" in capsys.readouterr().err


def test_an_unsure_read_is_named_to_the_writer_in_the_record_and_in_the_sources_block() -> None:
    from matrx_scraper.features.research_budget import Budgets, plan_groups, sources_block

    words = "possibly an interstitial (verify you are human; no HTML to check its structure, 9 sentences)"
    raw = [{"url": "https://a.example/p", "title": "t", "content": "Body text. " * 50, "query": "q", "unsure": words}]
    groups, plans = plan_groups(queries=["q"], instructions="", listings=[], pages=raw, budgets=Budgets())
    page = next(p for p in plans if p.url == "https://a.example/p")
    assert page.record()["unsure"] == words
    assert f"UNSURE READ, {words}: https://a.example/p" in groups[0].run_facts()
    block = sources_block([(page.url, False, page.unsure)], [])
    assert f"- https://a.example/p ({words})" in block


# ── closing pass (2026-11-17): a sign-in phrase on a short page never fails it; two label slips ──────────────────

@pytest.mark.parametrize("footer", ["Forgot password?", "Sign in to your account", "Please sign in"])
def test_a_short_page_with_a_sign_in_phrase_and_no_password_form_is_read(footer: str) -> None:
    html = f"<html><head><title>Notes</title></head><body><main><p>{ART[:600]}</p></main><footer>{footer}</footer></body></html>"
    text = ART[:600] + " " + footer
    verdict = judge_read(status=200, text=text, html=html, title="Notes")
    assert not verdict.failed, verdict.reason
    verdict = judge_read(status=200, text=text, html=None, title="Notes")  # no-HTML path: phrase alone never fails either
    assert not verdict.failed, verdict.reason


def test_a_javascript_only_login_shell_is_a_script_shell_not_empty() -> None:
    html = '<html><head><title>Log in</title></head><body><div id="root"></div><script src="/app.js"></script></body></html>'
    verdict = judge_read(status=200, text="", html=html, title="Log in")
    assert verdict.failed and verdict.reason == "js_shell" and "script-only shell" in verdict.detail
    assert judge_read(status=200, text="", html="<html><body></body></html>", title="").reason == "empty"


def test_a_403_with_no_wall_markup_is_http_error_because_the_status_is_all_the_evidence() -> None:
    plain = judge_read(status=403, text="Forbidden", html="<html><body>Forbidden</body></html>", title="403")
    assert plain.reason == "http_error" and plain.detail.endswith("(HTTP 403)")
    wall = judge_read(status=403, text="Just a moment", html="<html><head><title>Just a moment...</title></head><body></body></html>",
                      title="Just a moment...")
    assert wall.reason == "challenge"
