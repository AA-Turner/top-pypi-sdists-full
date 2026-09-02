"""The two live one-shot surfaces return VERDICTS, not just measurements.

`quick_preview` (the dashboard's New Crawl card) and `scraper_audit_html` (the
agent tool) both used to hand back raw evidence — `title_length: 74` — and made
the consumer know the SEO rules. Our user is a non-technical subject-matter
expert and cannot turn that number into a decision; a model handed the same
number guesses at the threshold and gets it wrong.

These tests pin the fix at both surfaces:

1. a known-bad page comes back with the expected failing check keys, each
   carrying a non-empty plain-English reason;
2. the verdicts are the canonical ones (`seo_audit.PAGE_CHECKS`), not a copy;
3. transport facts the surface genuinely does not have answer `n_a`, never a
   silent pass;
4. the tool result stays bounded — it re-enters the prompt on every loop
   iteration.
"""

from __future__ import annotations

import json
from typing import Any

import pytest

from matrx_scraper.ai_tools.specs import ALL_TOOLS
from matrx_scraper.ai_tools.specs import _scraper_audit_html
from matrx_scraper.seo_audit import (
    PAGE_CHECKS,
    audit_html,
    evidence_from_audit,
    run_page_checks,
)

# A page with a specific, nameable set of defects: a two-character title, no
# meta description, two h1s, a thin body, an image with no alt, a canonical
# pointing somewhere else, noindex, and an insecure resource.
BAD_HTML = """
<html lang="en"><head>
  <title>Hi</title>
  <link rel="canonical" href="https://example.com/other">
  <meta name="robots" content="noindex">
</head><body>
  <h1>One</h1><h1>Two</h1>
  <img src="/a.png">
  <img src="http://cdn.example.com/b.png" alt="ok">
  <p>Short body.</p>
</body></html>
"""

PAGE_URL = "https://example.com/page"

# What this page is actually guilty of. Both surfaces must name all of them.
EXPECTED_PROBLEMS = {
    "title_length",
    "meta_description_presence",
    "h1_presence",
    "thin_content",
    "image_alt_presence",
    "meta_robots_conflicts",
    "canonical_conflicts",
    "mixed_content",
}


def _canonical_problems(**transport: Any) -> set[str]:
    """The verdicts straight from the ONE implementation, for comparison."""
    evidence = evidence_from_audit(audit_html(BAD_HTML, PAGE_URL), **transport)
    return {
        key
        for key, outcome in run_page_checks(evidence).items()
        if outcome.status in ("warn", "fail")
    }


# ---------------------------------------------------------------------------
# Surface 1 — quick_preview


class _FakeResponse:
    def __init__(self, url: str, status: int, text: str) -> None:
        self.url = url
        self.status_code = status
        self.text = text
        self.content = text.encode("utf-8")
        self.history: list[Any] = []

    async def aread(self) -> bytes:
        return self.content


class _FakeStream:
    def __init__(self, response: _FakeResponse) -> None:
        self.response = response

    async def __aenter__(self) -> _FakeResponse:
        return self.response

    async def __aexit__(self, *exc: Any) -> None:
        return None


class _FakeClient:
    """httpx stand-in: the homepage answers with BAD_HTML, robots.txt 404s."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        pass

    async def __aenter__(self) -> _FakeClient:
        return self

    async def __aexit__(self, *exc: Any) -> None:
        return None

    def stream(self, method: str, url: str) -> _FakeStream:
        assert method == "GET"
        if url.endswith("/robots.txt"):
            return _FakeStream(_FakeResponse(url, 404, ""))
        return _FakeStream(_FakeResponse(url, 200, BAD_HTML))


@pytest.fixture
def offline_preview(monkeypatch: pytest.MonkeyPatch):
    """quick_preview with no network and no browser."""
    from matrx_scraper import preview as preview_mod

    async def allow(url: str) -> str:
        return url

    async def no_screenshot(url: str) -> None:
        return None

    monkeypatch.setattr(preview_mod, "validate_public_http_url", allow)
    monkeypatch.setattr(preview_mod, "_take_homepage_screenshot", no_screenshot)
    monkeypatch.setattr(preview_mod.httpx, "AsyncClient", _FakeClient)
    return preview_mod


@pytest.mark.asyncio
async def test_quick_preview_returns_verdicts_with_reasoning(offline_preview) -> None:
    out = await offline_preview.quick_preview("example.com")

    assert out["ok"] is True
    checks = out["homepage"]["checks"]

    flagged = {c["key"] for c in checks["checks"] if c["status"] in ("warn", "fail")}
    assert EXPECTED_PROBLEMS <= flagged

    for check in checks["checks"]:
        assert check["reasoning"].strip(), f"{check['key']} returned an empty reason"
        assert check["key"] in PAGE_CHECKS
        if check["status"] == "n_a":
            assert check["score"] is None
        else:
            assert 1 <= check["score"] <= 100

    assert checks["tally"]["total"] == len(PAGE_CHECKS)
    assert checks["tally"]["failed"] + checks["tally"]["warned"] == len(flagged)


@pytest.mark.asyncio
async def test_quick_preview_verdicts_are_the_canonical_ones(offline_preview) -> None:
    """Not "looks similar" — the same set the ONE implementation produces."""
    out = await offline_preview.quick_preview("example.com")
    flagged = {
        c["key"] for c in out["homepage"]["checks"]["checks"] if c["status"] in ("warn", "fail")
    }
    assert flagged == _canonical_problems(
        http_status=200,
        redirect_chain=[{"status": 200, "url": PAGE_URL}],
        final_url=PAGE_URL,
        response_bytes=len(BAD_HTML.encode("utf-8")),
        response_time_ms=120,
    )


@pytest.mark.asyncio
async def test_quick_preview_still_returns_every_existing_measurement(
    offline_preview,
) -> None:
    """Additive — the checks join the evidence, they do not replace it."""
    out = await offline_preview.quick_preview("example.com")
    homepage = out["homepage"]
    for field in (
        "status",
        "title",
        "title_length",
        "meta_description",
        "meta_description_length",
        "lang",
        "canonical",
        "h1",
        "schema_types",
        "word_count",
        "link_count",
        "internal_links",
        "external_links",
        "images_total",
        "images_missing_alt",
        "flesch_reading_ease",
        "og",
    ):
        assert field in homepage, f"quick_preview dropped {field}"
    assert set(out) == {
        "ok",
        "input",
        "normalized_url",
        "homepage_url",
        "robots_url",
        "robots",
        "homepage",
        "screenshot",
    }


@pytest.mark.asyncio
async def test_quick_preview_captures_the_transport_facts(offline_preview) -> None:
    """Status, weight and latency are real here — those checks must not be n_a."""
    out = await offline_preview.quick_preview("example.com")
    by_key = {c["key"]: c for c in out["homepage"]["checks"]["checks"]}
    for key in ("broken_page_4xx", "server_error_5xx", "page_weight", "ttfb_server_response"):
        assert by_key[key]["status"] != "n_a", f"{key} lost a transport fact the fetch had"


# ---------------------------------------------------------------------------
# Surface 2 — the scraper_audit_html tool


@pytest.mark.asyncio
async def test_audit_html_tool_leads_with_the_problems() -> None:
    out = await _scraper_audit_html({"html": BAD_HTML, "url": PAGE_URL})

    problems = out["checks"]["problems"]
    assert {p["key"] for p in problems} >= EXPECTED_PROBLEMS
    for problem in problems:
        assert problem["reasoning"].strip(), f"{problem['key']} returned an empty reason"
        assert problem["status"] in ("fail", "warn")
    # Failures before warnings — the model reads the worst news first.
    statuses = [p["status"] for p in problems]
    assert statuses == sorted(statuses, key=lambda s: 0 if s == "fail" else 1)

    tally = out["checks"]["tally"]
    assert tally["total"] == len(PAGE_CHECKS)
    assert tally["failed"] + tally["warned"] == len(problems)
    # Passes are summarised, not dumped as verbose outcome objects.
    assert all(isinstance(key, str) for key in out["checks"]["passed_checks"])
    assert len(problems) + len(out["checks"]["passed_checks"]) + len(
        out["checks"]["not_applicable_checks"]
    ) == len(PAGE_CHECKS)


@pytest.mark.asyncio
async def test_audit_html_tool_verdicts_are_the_canonical_ones() -> None:
    out = await _scraper_audit_html({"html": BAD_HTML, "url": PAGE_URL})
    assert {p["key"] for p in out["checks"]["problems"]} == _canonical_problems(
        response_bytes=len(BAD_HTML.encode("utf-8"))
    )


@pytest.mark.asyncio
async def test_audit_html_tool_marks_uncaptured_transport_as_not_applicable() -> None:
    """No status supplied ⇒ n_a. A silent pass on evidence we never had is the bug."""
    out = await _scraper_audit_html({"html": BAD_HTML, "url": PAGE_URL})
    n_a = set(out["checks"]["not_applicable_checks"])
    assert {"broken_page_4xx", "server_error_5xx", "ttfb_server_response"} <= n_a

    supplied = await _scraper_audit_html(
        {"html": BAD_HTML, "url": PAGE_URL, "http_status": 404, "ttfb_ms": 9_000}
    )
    keys = {p["key"] for p in supplied["checks"]["problems"]}
    assert {"broken_page_4xx", "ttfb_server_response"} <= keys


@pytest.mark.asyncio
async def test_audit_html_tool_result_is_bounded() -> None:
    """A huge page must not produce a huge tool result.

    The old handler returned `to_dict()` — the whole structured-data blob, the
    complete resource inventory, every link row — straight into the prompt.
    """
    filler = "".join(
        f'<p>{"word " * 40}</p><a href="https://example.com/{i}">link {i}</a>'
        f'<script type="application/ld+json">{{"@type":"Thing","name":"{"x" * 500}"}}</script>'
        for i in range(700)
    )
    html = f"<html><head><title>{'t' * 5_000}</title></head><body>{filler}</body></html>"
    assert len(html) > 500_000

    out = await _scraper_audit_html({"html": html, "url": PAGE_URL})
    size = len(json.dumps(out))
    assert size < 25_000, f"tool result grew to {size} chars — it re-enters the prompt every turn"


def test_the_tool_advertises_its_transport_arguments() -> None:
    spec = next(t for t in ALL_TOOLS if t.name == "scraper_audit_html")
    properties = spec.input_schema["properties"]
    assert {"html", "url", "http_status", "response_time_ms", "ttfb_ms"} <= set(properties)
    assert spec.input_schema["required"] == ["html"]
