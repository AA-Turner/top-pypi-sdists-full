"""A code block inside a list item must not swallow the rest of the page.

Live 2026-10-30: Wikipedia's Matcha references hold ``<code>{{cite book}}</code>``
in a list item; the item was written ``- ```…``` `` with the closing fence at
column 0, which closes nothing — the whole tail (14k characters) rendered raw.
"""

from __future__ import annotations

from matrx_scraper.orchestrator import _parse_html_content
from matrx_scraper.parser.data_types import _code_in_list_item

PAGE = """<html><body><main><h1>Matcha</h1><p>Intro paragraph about tea.</p>
<ol class="references">
<li>Heiss (2007). A Brief History of Tea.</li>
<li>Sen (1958). Classics. <span class="cs1-maint"><code class="cs1-code">{{cite book}}</code></span></li>
<li>Last reference.<pre>line one
line two</pre></li>
</ol>
<p>Closing paragraph after the list.</p></main></body></html>"""


def _open_fence_at(markdown: str, needle: str) -> bool:
    """Whether ``needle`` sits inside a fenced block, the way a CommonMark renderer reads it:
    a fence opened inside ``- `` closes only at the item's indentation."""
    inside, indent = False, 0
    for line in markdown.splitlines():
        stripped = line.lstrip()
        lead = len(line) - len(stripped)
        marker = stripped[2:] if stripped.startswith("- ") else stripped
        marker_lead = lead + (2 if stripped.startswith("- ") else 0)
        if marker.startswith("```"):
            if not inside:
                inside, indent = True, marker_lead
            elif lead >= indent:
                inside = False
            continue
        if needle in line:
            return inside
    return False


def test_single_line_code_in_an_item_is_inline_code() -> None:
    assert _code_in_list_item("{{cite book}}") == "`{{cite book}}`"
    assert _code_in_list_item("a `b` c") == "`` a `b` c ``"


def test_multi_line_code_in_an_item_keeps_its_fence_inside_the_item() -> None:
    assert _code_in_list_item("line one\nline two") == "```\n  line one\n  line two\n  ```"


def test_text_after_a_code_item_is_not_swallowed() -> None:
    md = _parse_html_content(PAGE, "https://en.wikipedia.org/wiki/Matcha", fast=False).get("markdown_renderable") or ""
    assert "Closing paragraph after the list" in md
    assert not _open_fence_at(md, "Closing paragraph after the list"), md
    assert not _open_fence_at(md, "Last reference"), md
