"""THE ORDER, server twin: real HTML before any XML section (production regression, 2026-10-21).

The chat splitter (rich-content ``html-before-xml-order.test.ts``) writes the corpus and the HTML
element list to ``tests/fixtures/html_root_vectors.json``; this block detector must split every
document the same way and hold the same list. On the pre-fix detector every <div>, page and <svg>
in the corpus split as a ``code``/``xml`` generic container instead.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from matrx_ai.processing.blocks.block_detector import (
    ALLOWED_RAW_HTML_TAGS,
    KNOWN_XML_TAG_NAMES,
    split_content_into_blocks,
)
from matrx_ai.processing.blocks.html_elements import HTML_ELEMENT_NAMES, HTML_MARKUP_ROOTS
from matrx_ai.processing.blocks.source_islands import list_islands

_PACKAGE_ROOT = Path(__file__).resolve().parents[4]
_FIXTURE = _PACKAGE_ROOT / "tests" / "fixtures" / "html_root_vectors.json"
_TS_SOURCE = (
    _PACKAGE_ROOT.parents[1]
    / "apps"
    / "shared"
    / "rich-content"
    / "src"
    / "display"
    / "markdown-classification"
    / "processors"
    / "utils"
    / "__tests__"
    / "html-root-vectors.json"
)
_VECTORS = json.loads(_FIXTURE.read_text(encoding="utf-8"))


def test_fixture_is_the_typescript_vectors() -> None:
    if not _TS_SOURCE.exists():
        pytest.skip("the rich-content source is not beside this package")
    assert _FIXTURE.read_bytes() == _TS_SOURCE.read_bytes()


def test_html_element_list_is_the_typescript_list() -> None:
    assert sorted(HTML_ELEMENT_NAMES) == _VECTORS["htmlElementNames"]


def test_no_name_is_both_html_and_a_matrx_tag() -> None:
    assert sorted(name for name in KNOWN_XML_TAG_NAMES if name.lower() in HTML_ELEMENT_NAMES) == []
    assert sorted(ALLOWED_RAW_HTML_TAGS - HTML_ELEMENT_NAMES) == []


@pytest.mark.parametrize("doc", _VECTORS["documents"], ids=[d["name"] for d in _VECTORS["documents"]])
def test_blocks_match_the_chat_splitter(doc: dict) -> None:
    blocks = split_content_into_blocks(doc["text"])
    got = [[b.type, (b.content or "").strip()] for b in blocks if (b.content or "").strip()]
    assert got == doc["blocks"]


@pytest.mark.parametrize("name", sorted(HTML_ELEMENT_NAMES))
def test_html_markup_is_never_a_section(name: str) -> None:
    for text in (
        f'<{name} class="a">\ninside\n</{name}>',
        f'<{name} class="a">inside</{name}>',
        f"<{name}>\n<p>inside</p>\n</{name}>",
        f"<{name}><b>inside</b></{name}>",
        f'<{name} class="a">\ninside',
    ):
        for block in split_content_into_blocks(text):
            assert not block.metadata.get("genericXmlContainer"), (text, block)
        assert all(island.island_type != "xml_container" for island in list_islands(text)), text


@pytest.mark.parametrize("name", sorted(HTML_MARKUP_ROOTS))
def test_a_markup_root_is_never_a_section_even_bare(name: str) -> None:
    for text in (f"<{name}>\ninside\n</{name}>", f"<{name}>inside</{name}>"):
        for block in split_content_into_blocks(text):
            assert not block.metadata.get("genericXmlContainer"), (text, block)


def test_a_bare_wrapper_word_stays_a_section() -> None:
    blocks = split_content_into_blocks("<output>\nthe answer\n</output>")
    assert [b.metadata.get("genericXmlContainer") for b in blocks] == [True]
