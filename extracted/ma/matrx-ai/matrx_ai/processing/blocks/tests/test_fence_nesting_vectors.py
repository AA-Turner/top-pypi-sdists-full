"""FORCING FUNCTION: the Python nested-fence twin agrees with THE rule.

THE rule is defined once, in TypeScript: ``@ai-matrx/content-ir``
``source/fence-nesting.ts`` (aidream ``apps/shared/content-ir-core``), which
also drives the source tokenizer and matrx-frontend's splitters. Python cannot
import it, so ``fence_nesting.py`` + ``block_detector`` are held to it by
vectors GENERATED from the TypeScript rule
(``apps/shared/content-ir-core/__tests__/fence-nesting-vectors.json``, never
hand-edited) whose byte-identical copy is ``tests/fixtures/fence_nesting_vectors.json``.

Use case: an operations lead asks the assistant for a README; the answer is a
```markdown document carrying its own ```bash and ```python blocks, and every
surface — server blocks, frontend renderer, the editor's locked islands —
must end that document at the same line.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from matrx_ai.processing.blocks.block_detector import split_content_into_blocks
from matrx_ai.processing.blocks.fence_nesting import (
    FENCE_OPENER_WHITESPACE,
    FENCE_WHITESPACE,
    parse_fence_opener,
    classify_inner_fence_line,
    trim_fence_line,
)

_PACKAGE_ROOT = Path(__file__).resolve().parents[4]
_FIXTURE = _PACKAGE_ROOT / "tests" / "fixtures" / "fence_nesting_vectors.json"
# In the aidream monorepo the TypeScript source of the vectors sits beside us.
_TS_SOURCE = _PACKAGE_ROOT.parents[1] / "apps" / "shared" / "content-ir-core" / "__tests__" / "fence-nesting-vectors.json"

_VECTORS = json.loads(_FIXTURE.read_text(encoding="utf-8"))


def test_fence_whitespace_is_the_shared_definition() -> None:
    assert FENCE_WHITESPACE == _VECTORS["fenceWhitespace"]


def test_fence_opener_whitespace_is_the_shared_definition() -> None:
    assert FENCE_OPENER_WHITESPACE == _VECTORS["fenceOpenerWhitespace"]


@pytest.mark.parametrize("vector", _VECTORS["openers"], ids=[repr(v["line"]) for v in _VECTORS["openers"]])
def test_opener_parse_matches_the_rule(vector: dict) -> None:
    parsed = parse_fence_opener(vector["line"])
    expected = vector["parsed"]
    assert (None if parsed is None else {"ticks": parsed[0], "lang": parsed[1]}) == expected


def test_fixture_is_the_generated_typescript_corpus() -> None:
    if not _TS_SOURCE.exists():
        pytest.skip("standalone install: the TypeScript corpus is not beside this package")
    assert _FIXTURE.read_bytes() == _TS_SOURCE.read_bytes(), (
        "tests/fixtures/fence_nesting_vectors.json drifted from the TypeScript rule's "
        "generated corpus — copy apps/shared/content-ir-core/__tests__/fence-nesting-vectors.json "
        "over it, then make fence_nesting.py pass"
    )


@pytest.mark.parametrize(
    "vector", _VECTORS["classifier"], ids=[f"{v['line']}|{v['openTicks']}|{v['nests']}|{v['depth']}" for v in _VECTORS["classifier"]]
)
def test_classifier_matches_the_rule(vector: dict) -> None:
    got = classify_inner_fence_line(
        trim_fence_line(vector["line"]), vector["openTicks"], vector["nests"], vector["depth"]
    )
    assert got == vector["expected"]


@pytest.mark.parametrize("doc", _VECTORS["documents"], ids=[d["name"] for d in _VECTORS["documents"]])
def test_block_detector_ends_every_fence_where_the_rule_does(doc: dict) -> None:
    blocks = split_content_into_blocks(doc["text"])
    bodies = [b.content for b in blocks if b.type == "code"]
    assert bodies == doc["fenceBodies"]
