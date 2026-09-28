"""FORCING FUNCTION: the Python block detector reads tables by THE GFM rule.

THE rule is defined once, in TypeScript, in matrx-frontend: the one row
splitter (``components/rich-editor/core/table-source.ts``), the one cell-pipe
rule (``components/markdown-core/syntax/gfm-cell-pipes.ts``) and where a table
starts and runs (``processors/utils/gfm-table-lines.ts``, used by the chat
splitter and the live stream). Python cannot import it, so
``gfm_table_lines.py`` + ``block_detector`` + ``parsers/table_parser`` are held
to it by vectors COMPUTED from the TypeScript rule
(matrx-frontend ``processors/utils/__tests__/gfm-table-vectors.json``, never
hand-edited) whose byte-identical copy is ``tests/fixtures/gfm_table_vectors.json``
(verify-RC-B4 R5-2 / R5-3).

Use case: an assistant answers a warehouse shift handover as a table written
without edge pipes; the server's blocks, the chat renderer and the editor must
all see the same table with the same cells.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from matrx_ai.processing.blocks.block_detector import (
    ALLOWED_RAW_HTML_TAGS,
    split_content_into_blocks,
)
from matrx_ai.processing.blocks.gfm_table_lines import (
    continues_table,
    find_table_end,
    is_html_block_tag_name,
    opens_table,
    row_cells,
    table_starts_at,
    unescape_cell_pipes,
)
from matrx_ai.processing.blocks.parsers.table_parser import parse_table

_PACKAGE_ROOT = Path(__file__).resolve().parents[4]
_FIXTURE = _PACKAGE_ROOT / "tests" / "fixtures" / "gfm_table_vectors.json"
# On this machine layout the TypeScript source sits in the sibling repo.
_TS_SOURCE = (
    _PACKAGE_ROOT.parents[2]
    / "matrx-frontend"
    / "components"
    / "mardown-display"
    / "markdown-classification"
    / "processors"
    / "utils"
    / "__tests__"
    / "gfm-table-vectors.json"
)

_VECTORS = json.loads(_FIXTURE.read_text(encoding="utf-8"))


def test_fixture_is_the_typescript_rules_vectors() -> None:
    if not _TS_SOURCE.exists():
        pytest.skip("matrx-frontend is not beside this checkout")
    assert _FIXTURE.read_bytes() == _TS_SOURCE.read_bytes(), (
        "tests/fixtures/gfm_table_vectors.json drifted from the TypeScript rule's vectors — "
        "copy matrx-frontend processors/utils/__tests__/gfm-table-vectors.json over it, "
        "then make gfm_table_lines.py pass"
    )


@pytest.mark.parametrize("vector", _VECTORS["rows"], ids=[repr(v["line"]) for v in _VECTORS["rows"]])
def test_row_cells_match_the_one_splitter(vector: dict) -> None:
    assert row_cells(vector["line"]) == vector["cells"]


@pytest.mark.parametrize("vector", _VECTORS["cellPipes"], ids=[repr(v["cell"]) for v in _VECTORS["cellPipes"]])
def test_cell_pipe_rule(vector: dict) -> None:
    assert unescape_cell_pipes(vector["cell"]) == vector["display"]


@pytest.mark.parametrize("vector", _VECTORS["tables"], ids=[repr(v["table"][:30]) for v in _VECTORS["tables"]])
def test_parsed_table_cells(vector: dict) -> None:
    parsed = parse_table(vector["table"], is_final=True)
    if vector.get("notATable"):
        assert parsed is None
        return
    assert parsed is not None
    assert parsed.headers == vector["headers"]
    assert parsed.rows == vector["rows"]


@pytest.mark.parametrize("doc", _VECTORS["documents"], ids=[d["name"] for d in _VECTORS["documents"]])
def test_blocks_match_the_chat_splitter(doc: dict) -> None:
    blocks = split_content_into_blocks(doc["text"])
    got = [[b.type, (b.content or "").strip()] for b in blocks if (b.content or "").strip()]
    assert got == doc["blocks"]


@pytest.mark.parametrize(
    ("line", "continues"),
    [
        ("B4 clear", True),  # GFM spec example 202: a line without a pipe is a row
        (" | ", True),  # a lone pipe is an (empty) row
        ("| B4 | clear |", True),
        ("", False),
        ("> 8C | alarm", False),
        ("- B4 | clear", False),
        ("# Next", False),
        ("```` code ```` | b", True),  # a backtick in the info string: not a fence (CommonMark 4.5)
        ("``` `x` | b", True),
        ("````x | b", False),  # a real backtick fence
        ("~~~x | b", False),
    ],
)
def test_table_continuation_is_gfm(line: str, continues: bool) -> None:
    assert continues_table(line) is continues


@pytest.mark.parametrize(
    "vector", _VECTORS["tableEnds"], ids=[repr(v["lines"][v["start"] + 3]) for v in _VECTORS["tableEnds"]]
)
def test_table_ends_where_gfm_ends_it(vector: dict) -> None:
    """verify-RC-B4 round 9: every CommonMark 4.6 HTML block start and indented code
    (4+ columns past the table's container) ends a table — each vector judged
    against remark-gfm in matrx-frontend."""
    lines = vector["lines"]
    assert opens_table(lines, vector["start"])
    assert find_table_end(lines, vector["start"]) == vector["end"]


@pytest.mark.parametrize(
    "vector", _VECTORS["tableStarts"], ids=[repr(v["lines"][: v["index"]]) for v in _VECTORS["tableStarts"]]
)
def test_table_opens_where_gfm_opens_it(vector: dict) -> None:
    """A header lazily continuing a list item's or quote's paragraph is no table (round 9)."""
    lines = vector["lines"]
    index = vector["index"]
    assert table_starts_at(lines, index) is vector["opens"]


def test_a_lone_pipe_is_an_empty_row() -> None:
    assert row_cells("|") == [""]
    assert row_cells(" | ") == [""]
    assert row_cells("") == []


def test_raw_html_tags_are_the_renderers_list() -> None:
    """One list, not two: the raw HTML the renderer keeps (rehypeSafeRawHtml) — verify-RC-B4 round 9."""
    assert sorted(ALLOWED_RAW_HTML_TAGS) == _VECTORS["rawHtmlTags"]


@pytest.mark.parametrize("vector", _VECTORS["htmlBlockTagNames"], ids=[v["name"] for v in _VECTORS["htmlBlockTagNames"]])
def test_html_block_tag_names(vector: dict) -> None:
    """A tag CommonMark reads as an HTML block is HTML, never a custom XML container."""
    assert is_html_block_tag_name(vector["name"]) is vector["isBlock"]
