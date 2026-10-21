"""THE ONE TREE-LINE RULE, Python twin: is this line part of a text tree diagram?

The rule is defined once, in TypeScript: ``@ai-matrx/content-ir``
``source/tree-line.ts`` (aidream ``apps/shared/content-ir-core``), which the
source tokenizer and rich-content's content splitter import. Python cannot
import it, so this module is held to it by vectors GENERATED from the
TypeScript rule (``apps/shared/content-ir-core/__tests__/tree-line-vectors.json``,
never hand-edited) whose byte-identical copy is
``tests/fixtures/tree_line_vectors.json`` (``tests/test_tree_line_vectors.py``).

Used by ``block_detector`` (the server's block split) and ``source_islands``
(the tokenizer twin), so both read a tree exactly as the renderer does.
"""

from __future__ import annotations

import re

from matrx_ai.processing.blocks.gfm_table_lines import is_gfm_delimiter_row

TREE_GLYPHS = re.compile("[├└│┌┐┘┬┴┤┼─]")
# An ASCII connector after any run of rails: `+--`/`|--`, or a last branch `` `-- ``
# (dashes then a space, so a line opening with `` `--flag` `` stays prose). A bare
# `| ` is a table row's edge, never a connector. Spacing is [ \t], never \s.
ASCII_TREE_CONNECTOR = re.compile("[ \t│|]*(?:[├└]|[+|][─-]|`[─-]+[ \t])")
MIN_TREE_LINES = 3


def is_tree_line(line: str) -> bool:
    """True for a tree diagram line: box glyphs, or an ASCII connector that is not a GFM delimiter row."""
    if not line:
        return False
    if TREE_GLYPHS.search(line):
        return True
    return ASCII_TREE_CONNECTOR.match(line) is not None and not is_gfm_delimiter_row(line)
