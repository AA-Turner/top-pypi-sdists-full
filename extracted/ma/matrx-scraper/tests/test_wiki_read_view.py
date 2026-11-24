"""A Wikipedia article reads cleanly (universal-search walk, 2026-10-30): no "Edit links" chrome, and an
infobox is a real markdown table with no invented "col2" header."""

from __future__ import annotations

from matrx_scraper.orchestrator import _parse_html_content
from matrx_scraper.parser.data_types import markdown_table

HTML = """<html><body>
<header><div class="vector-menu"><ul><li>中文</li></ul>
<div class="after-portlet after-portlet-lang"><span class="wb-langlinks-edit wb-langlinks-link">
<a href="https://www.wikidata.org/wiki/Special:EntityPage/Q822331" class="wbc-editpage">Edit links</a></span></div></div></header>
<main><div id="mw-content-text"><h1>Matcha</h1>
<table class="infobox"><tbody>
<tr><th colspan="2">Matcha</th></tr>
<tr><th>Type</th><td>Green tea</td></tr>
<tr><th>Origin</th><td>China | Japan</td></tr>
</tbody></table>
<p>Matcha is a finely ground powder of green tea specially processed from shade-grown tea leaves. It is
typically consumed suspended in hot water, and is used in many drinks and desserts around the world.</p>
<p>Shade growing gives matcha its characteristic bright green color and strong umami flavor, prized in the
Japanese tea ceremony for centuries.</p>
</div></main></body></html>"""


def test_the_read_view_has_no_edit_chrome_and_a_real_table() -> None:
    md = _parse_html_content(HTML, "https://en.wikipedia.org/wiki/Matcha").get("markdown_renderable") or ""
    assert "Edit links" not in md
    assert "col2" not in md
    assert "| Type | Green tea |" in md


def test_a_markdown_table_blanks_invented_headers_and_keeps_cells_on_one_line() -> None:
    table = markdown_table([{"Matcha": "Type", "col2": "Green\ntea | leaf"}])
    assert table.strip().splitlines() == ["| Matcha |  |", "| --- | --- |", "| Type | Green tea \\| leaf |"]
