"""`parse_content` must produce real text — at the source, not via a fallback.

`_build_text_data` used to hand the `OrganizedData` OBJECT to
`json_to_text_lines`, a flattener that only walked dicts/lists. It matched no
branch, returned [], and every html page came back with `text_data == ""` and
`overview.char_count == 0`. The orchestrator patched the symptom by falling
back to `markdown_renderable`; `char_count` stayed 0. Rendering now lives on
`OrganizedData.to_text()` and these tests pin the pipeline output itself.
"""

from matrx_scraper.parser.core import ParserOrchestrator

HTML = (
    "<html><head><title>T</title></head><body>"
    "<h1>Hello</h1>"
    "<p>Some real body copy here for the parser.</p>"
    "<h2>Second section</h2>"
    "<ul><li>first item</li><li>second item</li></ul>"
    "</body></html>"
)


def _parse():
    return ParserOrchestrator().parse_content(HTML, url="https://example.test/x")


def test_parse_content_text_data_is_real_page_text():
    out = _parse()
    text = out["text_data"]

    assert text, "parse_content reported no text at all"
    assert "Hello" in text
    assert "Some real body copy here for the parser." in text
    assert "Second section" in text
    assert "first item" in text and "second item" in text


def test_parse_content_text_data_has_no_type_labels():
    """The `data` extraction form leaks its `{"type": ...}` keys as prose."""
    text = _parse()["text_data"]

    for label in ("unassociated", "header", "text", "list"):
        assert label not in text.lower().split(), f"type label {label!r} leaked into text_data"


def test_parse_content_char_counts_reflect_the_text():
    out = _parse()
    overview = out["overview"]

    assert overview["char_count"] == len(out["text_data"])
    assert overview["char_count"] > 0
    # The marker variant wraps each block, so it is strictly longer.
    assert overview["char_count_formatted"] > overview["char_count"]


def test_parse_content_text_matches_markdown_renderable_rule():
    """One rendering: `text_data` is the `markdown_renderable` rule's output."""
    from matrx_scraper.parser.extraction_rules import rules

    out = _parse()
    rule = [r for r in rules if r["name"] == "markdown_renderable"]
    rendered = out["organized_data"].extract(rules=rule)["markdown_renderable"]

    assert out["text_data"] == rendered
