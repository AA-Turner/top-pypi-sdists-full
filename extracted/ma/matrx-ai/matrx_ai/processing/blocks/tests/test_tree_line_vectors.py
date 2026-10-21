"""FORCING FUNCTION: the Python tree-line twin agrees with THE rule.

THE rule is defined once, in TypeScript: ``@ai-matrx/content-ir``
``source/tree-line.ts`` (aidream ``apps/shared/content-ir-core``), which the
source tokenizer and rich-content's content splitter import. Python cannot
import it, so ``tree_line.py`` (used by ``block_detector`` and
``source_islands``) is held to it by vectors GENERATED from the TypeScript rule
(``apps/shared/content-ir-core/__tests__/tree-line-vectors.json``, never
hand-edited) whose byte-identical copy is ``tests/fixtures/tree_line_vectors.json``.

Use case: an assistant answers with a repository layout drawn in plain ASCII
(``|-- bin`` / ``\\`-- README.md``) beside a table; the server's blocks, the chat
renderer and the editor must all see one tree and one table.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from matrx_ai.processing.blocks.block_detector import split_content_into_blocks
from matrx_ai.processing.blocks.tree_line import MIN_TREE_LINES, is_tree_line

_PACKAGE_ROOT = Path(__file__).resolve().parents[4]
_FIXTURE = _PACKAGE_ROOT / "tests" / "fixtures" / "tree_line_vectors.json"
# In the aidream monorepo the TypeScript source of the vectors sits beside us.
_TS_SOURCE = _PACKAGE_ROOT.parents[1] / "apps" / "shared" / "content-ir-core" / "__tests__" / "tree-line-vectors.json"

_VECTORS = json.loads(_FIXTURE.read_text(encoding="utf-8"))


def test_min_tree_lines_is_the_shared_definition() -> None:
    assert MIN_TREE_LINES == _VECTORS["minTreeLines"]


@pytest.mark.parametrize("vector", _VECTORS["lines"], ids=[repr(v["line"]) for v in _VECTORS["lines"]])
def test_line_reads_as_the_rule_reads_it(vector: dict) -> None:
    assert is_tree_line(vector["line"]) is vector["tree"]


def test_an_ascii_tree_is_one_tree_block_with_its_root() -> None:
    text = "Repo layout:\n\nmatrx-sync/\n|-- bin\n|   `-- sync\n+-- lib\n`-- README.md\n\nDone."
    trees = [b for b in split_content_into_blocks(text) if b.type == "tree"]
    assert [b.content for b in trees] == ["matrx-sync/\n|-- bin\n|   `-- sync\n+-- lib\n`-- README.md"]


def test_fixture_is_the_generated_typescript_corpus() -> None:
    if not _TS_SOURCE.exists():
        pytest.skip("standalone install: the TypeScript corpus is not beside this package")
    assert _FIXTURE.read_bytes() == _TS_SOURCE.read_bytes(), (
        "tests/fixtures/tree_line_vectors.json drifted from the TypeScript rule's corpus: "
        "regenerate it (UPDATE_TREE_VECTORS=1 in apps/shared/content-ir-core) and copy it here"
    )
