"""FORCING FUNCTION: the Python protected-region twin agrees with THE island rule.

THE rule is defined once, in TypeScript: ``@ai-matrx/content-ir``
``source/tokenize.ts`` (``listIslands(tokenizeSource(text))``, aidream
``apps/shared/content-ir-core``) — the islands the client editor locks.
Python cannot import it, so ``source_islands.py`` is held to it by vectors
GENERATED from the TypeScript rule
(``apps/shared/content-ir-core/__tests__/source-island-vectors.json``, never
hand-edited) whose byte-identical copy is
``tests/fixtures/source_island_vectors.json``.

Use case: an assistant patches a stored note server-side ("change the pickup
day to Tuesday"); the patch must refuse to touch a ``{{variable}}``, a
formula, a fenced block or a ``__kind`` card exactly where the editor would.
"""

from __future__ import annotations

import json
import time
from pathlib import Path

import pytest

from matrx_ai.processing.blocks.source_islands import (
    BLOCK_ISLAND_TYPES,
    INLINE_ISLAND_TYPES,
    SourceIsland,
    list_islands,
)

_PACKAGE_ROOT = Path(__file__).resolve().parents[4]
_FIXTURE = _PACKAGE_ROOT / "tests" / "fixtures" / "source_island_vectors.json"
# In the aidream monorepo the TypeScript source of the vectors sits beside us.
_TS_SOURCE = _PACKAGE_ROOT.parents[1] / "apps" / "shared" / "content-ir-core" / "__tests__" / "source-island-vectors.json"

_VECTORS = json.loads(_FIXTURE.read_text(encoding="utf-8"))["vectors"]


def test_fixture_is_the_generated_typescript_corpus() -> None:
    if not _TS_SOURCE.exists():
        pytest.skip("standalone install: the TypeScript corpus is not beside this package")
    assert _FIXTURE.read_bytes() == _TS_SOURCE.read_bytes(), (
        "tests/fixtures/source_island_vectors.json drifted from the TypeScript rule's generated corpus — "
        "copy apps/shared/content-ir-core/__tests__/source-island-vectors.json over it, then make "
        "source_islands.py pass"
    )


def test_the_corpus_is_not_empty_and_names_every_island_type() -> None:
    assert len(_VECTORS) > 500
    seen = {(i["type"], i["inline"]) for v in _VECTORS for i in v["islands"]}
    assert {t for t, inline in seen if not inline} == BLOCK_ISLAND_TYPES
    assert {t for t, inline in seen if inline} == INLINE_ISLAND_TYPES


@pytest.mark.parametrize("vector", _VECTORS, ids=[v["name"] for v in _VECTORS])
def test_islands_match_the_rule(vector: dict) -> None:
    text = vector["text"]
    got = [
        {"type": i.island_type, "startCp": i.start, "endCp": i.end, "inline": i.inline, "complete": i.complete}
        for i in list_islands(text)
    ]
    assert got == vector["islands"]
    for island in list_islands(text):
        assert island.raw == text[island.start : island.end]


def test_realistic_answer_protects_what_a_patch_must_not_touch() -> None:
    text = (
        "Hi {{customer_name}}, the loop costs $r = \\frac{d}{t}$ per mile.\n\n"
        '```python\nroute = plan()\n```\n\n{"__kind":"checklist","items":[{"text":"Scale"}]}\n'
    )
    islands = list_islands(text)
    assert [(i.island_type, i.raw) for i in islands] == [
        ("variable", "{{customer_name}}"),
        ("math_inline", "$r = \\frac{d}{t}$"),
        ("fence", "```python\nroute = plan()\n```"),
        ("json", '{"__kind":"checklist","items":[{"text":"Scale"}]}'),
    ]
    assert all(isinstance(i, SourceIsland) and i.complete for i in islands)


def test_code_point_offsets_are_python_str_indices() -> None:
    text = "🚚 Load {{truck}} 😀 $x^2$ done"
    islands = list_islands(text)
    assert [text[i.start : i.end] for i in islands] == ["{{truck}}", "$x^2$"]


def test_two_hundred_kilobytes_list_in_well_under_a_second() -> None:
    unit = (
        "Pickup for {{client}} costs $5 while $x^2$ holds; see <b>bold</b> and [[Rates]].\n\n"
        "```js\nconst tons = 3.8;\n```\n\n<thinking>\nweigh first\n</thinking>\n\n"
        "| Day | Tons |\n|---|---|\n| Mon | 3.8 |\n\n"
        '{"__kind":"badge","label":"ok"}\n\n> [!NOTE]\n> Drive safe.\n\n'
        "src/\n├── a.ts\n├── b.ts\n└── c.ts\n\n$$\nE = mc^2\n$$\n\n"
    )
    text = unit * (200_000 // len(unit) + 1)
    assert len(text) >= 200_000
    list_islands(text)  # warm regex caches
    t0 = time.perf_counter()
    islands = list_islands(text)
    elapsed = time.perf_counter() - t0
    assert len(islands) > 5_000
    assert elapsed < 1.0, f"200 KB took {elapsed:.3f}s"


@pytest.mark.parametrize(
    "unit",
    ["{{", "{", "$$ a ", "$a b", "a`b``c", "\\(", "\\[", 'text {"__kind":"k", ', '<a x="', "a <thinking> ", "x <!-- ", "~~~\n", "<foo>\n"],
)
def test_pathological_200kb_units_stay_fast(unit: str) -> None:
    text = unit * (200_000 // len(unit))
    t0 = time.perf_counter()
    list_islands(text)
    assert time.perf_counter() - t0 < 2.0
