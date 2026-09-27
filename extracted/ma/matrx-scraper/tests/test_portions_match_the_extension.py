"""The server's portioner and the extension's cut the same page into the same sections.

``tests/fixtures/portions/*.json`` are three real pages (example.com, the Wikipedia HTTP article,
python.org with tracking parameters), each with its HTML-path and markdown-path sections as the
extension's ``portions.ts`` produces them (measured 2026-09-25: 0 differing portions of 92 against
the extension's own code under happy-dom; 86 differed before the port). matrx-extend pins its tests
to the same files, so either side drifting turns one of the two suites red.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from matrx_scraper.canonical import canonical_url
from matrx_scraper.portions import from_article_html, from_markdown

FIXTURES = sorted((Path(__file__).parent / "fixtures" / "portions").glob("*.json"))


def test_the_three_pages_are_pinned() -> None:
    assert {p.stem for p in FIXTURES} == {"example_com", "wikipedia_http", "python_org_tracking"}


@pytest.mark.parametrize("fixture", FIXTURES, ids=lambda p: p.stem)
def test_server_sections_equal_the_pinned_extension_sections(fixture: Path) -> None:
    fx = json.loads(fixture.read_text(encoding="utf-8"))
    assert from_article_html(fx["html"]) == fx["html_portions"]
    assert from_markdown(fx["markdown"]) == fx["markdown_portions"]
    assert canonical_url(fx["url"]) == fx["canonical_url"]


def test_heading_path_is_by_level_and_inline_markup_adds_no_space() -> None:
    """The two defects the fixtures caught, stated small."""
    html = "<h2>Versions</h2><p>a</p><h2>Use</h2><p>HTTP (<b>Hypertext</b> Transfer)</p>"
    ps = from_article_html(html)
    assert [p["locator"]["heading_path"] for p in ps] == [["Versions"], ["Use"]]
    assert "HTTP (Hypertext Transfer)" in ps[1]["text"]
    md = from_markdown("## Versions\na\n## Use\nb")
    assert [p["locator"]["heading_path"] for p in md] == [["Versions"], ["Use"]]


# ─── Plain text on every path, and one page is one text in every process ───────────────────

import subprocess  # noqa: E402
import sys  # noqa: E402

from matrx_scraper.portions import from_parsed_page  # noqa: E402

IANA = Path(__file__).parent / "__fixtures__" / "pages" / "iana-reserved-domains.html"
_MARKUP = ("](", "**", "`", "![", "\n#", "| ")


def test_no_markdown_reaches_a_portion() -> None:
    md = (
        "## History\nAs described in [RFC 2606](https://www.iana.org/go/rfc2606) and **bold** `code`.\n"
        "- [IANA-managed Reserved Domains](https://www.iana.org/domains/reserved)\n"
        "![logo](https://x/logo.png)\n| Language | Script |\n|---|---|\n| Arabic | Arabic |\n---"
    )
    [p] = from_markdown(md)
    assert p["locator"]["heading_path"] == ["History"]
    assert p["text"] == (
        "History\nAs described in RFC 2606 and bold code.\nIANA-managed Reserved Domains\n"
        "Language\nScript\nArabic\nArabic"
    )
    assert p["locator"]["text_fragment"].startswith("History As described in RFC 2606")


def _parse_in_a_fresh_process(seed: int) -> str:
    """The IANA page parsed and portioned in a NEW interpreter with its own hash seed — the
    condition under which one page used to render as two texts (a column set)."""
    code = (
        "import json,sys\n"
        "from matrx_scraper.orchestrator import _parse_html_content\n"
        "from matrx_scraper.portions import from_parsed_page\n"
        f"out=_parse_html_content(open({str(IANA)!r}).read(),'https://www.iana.org/domains/reserved')\n"
        "sys.stdout.write('\\x00'+json.dumps({'md':out['markdown_renderable'],"
        "'portions':from_parsed_page(out)},ensure_ascii=False))\n"
    )
    done = subprocess.run(
        [sys.executable, "-c", code],
        capture_output=True,
        text=True,
        env={**__import__("os").environ, "PYTHONHASHSEED": str(seed)},
        timeout=300,
        check=True,
    )
    return done.stdout.rsplit("\x00", 1)[1]


def test_one_page_is_one_text_in_every_process() -> None:
    runs = {seed: _parse_in_a_fresh_process(seed) for seed in (1, 2, 3, 4)}
    assert len(set(runs.values())) == 1, "the IANA page parsed to different texts under different hash seeds"
    portions = json.loads(runs[1])["portions"]
    table = next(p for p in portions if p["locator"]["heading_path"][-1:] == ["Test IDN top-level domains"])
    lines = table["text"].split("\n")
    at = lines.index("Domain")
    assert lines[at : at + 8] == [  # the page's own <th> order, then each row's cells
        "Domain", "Domain (A-label)", "Language", "Script", "إختبار", "xn--kgbechtv", "Arabic", "Arabic",
    ]
    for p in portions:
        assert not any(m in p["text"] for m in _MARKUP), f"markup in a server portion: {p['text'][:200]!r}"


def test_a_server_parse_portions_as_plain_text() -> None:
    from matrx_scraper.orchestrator import _parse_html_content

    out = _parse_html_content(IANA.read_text(encoding="utf-8"), "https://www.iana.org/domains/reserved")
    portions = from_parsed_page(out)
    assert [p["locator"]["heading_path"] for p in portions][:3] == [
        ["IANA-managed Reserved Domains"],
        ["IANA-managed Reserved Domains", "Example domains"],
        ["IANA-managed Reserved Domains", "Test IDN top-level domains"],
    ]
    assert portions[1]["text"].startswith("Example domains\nAs described in RFC 2606 and RFC 6761")
