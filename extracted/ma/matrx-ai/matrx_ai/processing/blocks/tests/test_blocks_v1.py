"""Blocks v1 (CGU-14): grammar, tiling, streamed == one-shot at every chunking, linear cost.

The corpus-wide proof over every golden input is ``scripts/blocks_golden_v2.py --check`` (repo
root); these tests hold the package on its own.
"""

from __future__ import annotations

import random
import time

import pytest

from matrx_ai.processing.blocks.blocks_v1 import (
    BlocksV1Splitter,
    KindRegistryView,
    blocks_v1_dicts,
    kind_validator,
)

FLASH = {
    "type": "object",
    "required": ["__kind", "title"],
    "properties": {"__kind": {"const": "flashcard_set"}, "title": {"type": "string"}},
}
REGISTRY = KindRegistryView(
    schema=lambda s: FLASH if s == "flashcard_set" else None,
    version=lambda s: 3 if s == "flashcard_set" else None,
    known=lambda s: s == "flashcard_set",
    warm=lambda: True,
)


def _read(text: str, **kw):
    blocks = blocks_v1_dicts(text, **kw)
    raw = text.encode("utf-8")
    return [(b["type"], raw[b["start"] : b["end"]].decode("utf-8"), b) for b in blocks]


def _types(text: str) -> list[str]:
    return [t for t, _s, _b in _read(text)]


CASES: dict[str, tuple[str, list[str]]] = {
    "prose": ("Hello **world**\n\n| a | b |\n|---|---|\n| 1 | 2 |\n", ["markdown"]),
    "fenced kind": ('Intro\n```json\n{"__kind": "flashcard_set", "title": "T"}\n```\nafter', ["markdown", "kind", "markdown"]),
    "bare kind": ('{"__kind":"flashcard_set","title":"T"}', ["kind"]),
    "multi-line bare kind": ('{\n  "__kind": "flashcard_set",\n  "title": "T"\n}\nDone', ["kind", "markdown"]),
    "mid-line kind": ('See {"__kind":"flashcard_set","title":"T"} here', ["markdown", "kind", "markdown"]),
    "adjacent roots": ('{"__kind":"a"}{"__kind":"b"}\n', ["kind", "kind"]),
    "array of kinds": ('Sets:\n[\n{"__kind":"a"},\n{"__kind":"b"}\n]\nEnd', ["markdown", "kind", "markdown"]),
    "python fence with kind json": ('```python\n{"__kind":"x"}\n```\n', ["markdown"]),
    "kind in inline code": ('Use `{"__kind":"x"}` like so\n', ["markdown"]),
    "kind in html comment": ('a <!-- {"__kind":"x"} --> b\n', ["markdown"]),
    "non-kind json": ('{"label": "x"}\n', ["markdown"]),
    "jsonc fence": ('```json\n// note\n{"__kind":"flashcard_set","title":"T"}\n```', ["kind"]),
    "reasoning": ("<think>\nhmm\n</think>\nAnswer", ["reasoning", "markdown"]),
    "reasoning same line": ("<thinking>short</thinking> then text\n", ["reasoning", "markdown"]),
    "unclosed reasoning": ("<reasoning>\nstill going", ["reasoning"]),
    "artifact": ('<artifact id="a1" type="code" title="T">\nx = 1\n</artifact>\n', ["artifact"]),
    "decision with attrs": ('<decision prompt="Pick">\n<option label="A">a</option>\n</decision>\n', ["decision"]),
    "bare decision stays": ("<decision>NOTIFY</decision>\n", ["markdown"]),
    "heartbeat protocol": ("<heartbeat>\n<decision>NOTIFY</decision>\n</heartbeat>\n", ["protocol"]),
    "unknown tag stays": ("<notes>\nhello\n</notes>\n", ["markdown"]),
    "tag inside fence stays": ("```\n<think>x</think>\n```\n", ["markdown"]),
    "indented 4 is code": ('    {"__kind":"x"}\n', ["markdown"]),
    "front matter kind stays": ('---\nk: {"__kind":"x"}\n---\nbody', ["markdown"]),
    "truncated kind": ('{"__kind":"flashcard_set","cards":[1,', ["kind"]),
    "empty": ("", []),
    "unicode offsets": ('héllo 👋\n{"__kind":"flashcard_set","title":"é"}\n', ["markdown", "kind"]),
}


@pytest.mark.parametrize("name", list(CASES))
def test_grammar_cases(name: str) -> None:
    text, want = CASES[name]
    assert _types(text) == want


@pytest.mark.parametrize("name", list(CASES))
def test_blocks_tile_the_text_in_utf8_bytes(name: str) -> None:
    text, _ = CASES[name]
    blocks = blocks_v1_dicts(text)
    raw = text.encode("utf-8")
    assert b"".join(raw[b["start"] : b["end"]] for b in blocks) == raw
    for a, b in zip(blocks, blocks[1:]):
        assert a["end"] == b["start"]


def _stream(text: str, sizes: list[int], **kw):
    sp = BlocksV1Splitter(**kw)
    events = []
    i = 0
    k = 0
    while i < len(text):
        n = sizes[k % len(sizes)]
        events += sp.feed(text[i : i + n])
        i += n
        k += 1
    events += sp.finish()
    return [b.to_dict() for b in sp.blocks], events


@pytest.mark.parametrize("name", list(CASES))
def test_streamed_equals_one_shot_at_every_chunking(name: str) -> None:
    text, _ = CASES[name]
    validate = kind_validator(REGISTRY)
    one = blocks_v1_dicts(text, validate=validate)
    rng = random.Random(name)
    chunkings = [[1], [2], [3], [7], [len(text) or 1]] + [[rng.randint(1, 23) for _ in range(50)] for _ in range(20)]
    for sizes in chunkings:
        streamed, events = _stream(text, sizes, validate=validate)
        assert streamed == one, sizes
        closed = [dict(e["block"]) for e in events if e["event"] == "block.close"]
        regions = [e for e in events if e["event"] == "block.regions"]
        # PF-1 D9: one regions event per markdown block, after every close (never on the token path).
        assert [e["index"] for e in regions] == [i for i, b in enumerate(one) if b["type"] == "markdown"]
        assert all(e["event"] == "block.regions" for e in events[len(events) - len(regions) :])
        for e in regions:
            assert "regions" not in closed[e["index"]]
            closed[e["index"]]["regions"] = e["regions"]
        assert closed == one
        opens = [e["index"] for e in events if e["event"] == "block.open"]
        assert opens == list(range(len(one)))
        assert not any(e["event"] == "block.retract" for e in events)


def test_validation_statuses() -> None:
    v = kind_validator(REGISTRY)
    good = blocks_v1_dicts('{"__kind":"flashcard_set","title":"T"}', validate=v)[0]
    assert (good["status"], good["kind_version"], good["errors"]) == ("valid", 3, [])
    bad = blocks_v1_dicts('{"__kind":"flashcard_set"}', validate=v)[0]
    assert bad["status"] == "invalid" and bad["errors"]
    unknown = blocks_v1_dicts('{"__kind":"nope"}', validate=v)[0]
    assert unknown["status"] == "unknown_kind"
    cut = blocks_v1_dicts('{"__kind":"flashcard_set","ti', validate=v)[0]
    assert (cut["status"], cut["complete"]) == ("incomplete", False)
    mixed = blocks_v1_dicts('[{"__kind":"flashcard_set","title":"T"},{"__kind":"nope"}]', validate=v)[0]
    assert mixed["kind"] is None and [i["status"] for i in mixed["items"]] == ["valid", "unknown_kind"]
    cold = KindRegistryView(schema=REGISTRY.schema, version=REGISTRY.version, known=REGISTRY.known, warm=lambda: False)
    assert blocks_v1_dicts('{"__kind":"flashcard_set","title":"T"}', validate=kind_validator(cold))[0]["status"] == "unchecked"


def test_text_is_never_changed_and_value_is_parsed() -> None:
    text = '```json\n{"__kind": "flashcard_set", "title": "T",}\n```'
    (_t, src, b), = _read(text)
    assert src == text
    assert b["value"] == {"__kind": "flashcard_set", "title": "T"}


def _doc(n: int) -> str:
    para = "Here is some **markdown** prose with a [link](http://x) and `code`.\n" * 3 + "\n"
    parts: list[str] = []
    i = 0
    while sum(map(len, parts)) < n:
        i += 1
        parts.append(para)
        if i % 4 == 0:
            parts.append("```python\nprint(1)\n```\n\n")
        if i % 7 == 0:
            parts.append('```json\n{"__kind":"flashcard_set","title":"T"}\n```\n\n')
        if i % 9 == 0:
            parts.append("<think>\nthought\n</think>\n")
    return "".join(parts)[:n]


def _per_token(text: str) -> float:
    # GC paused (as the p99 test does): inside a full-suite run the heap other tests left behind makes
    # a collector pass cost more than the splitter's whole per-token budget, and that is not the splitter.
    import gc

    toks = [text[i : i + 16] for i in range(0, len(text), 16)]
    best = float("inf")
    was_enabled = gc.isenabled()
    gc.disable()
    try:
        for _ in range(9):
            sp = BlocksV1Splitter()
            t0 = time.perf_counter()
            for t in toks:
                sp.feed(t)
            sp.finish()
            best = min(best, (time.perf_counter() - t0) / len(toks))
    finally:
        if was_enabled:
            gc.enable()
    return best


def test_per_token_cost_is_flat_and_small() -> None:
    small, large = _per_token(_doc(2_000)), _per_token(_doc(70_000))
    one_line = '{"__kind":"x","items":[' + ",".join(f'{{"a":"{i} bbbbbbbbbbbbbbbbbbbb"}}' for i in range(2500)) + "]}"
    assert large < small * 3, (small, large)
    assert _per_token(one_line) < small * 4
    assert large < 20e-6, large


def test_per_token_p99_is_within_budget() -> None:
    """The plan's budget: ≤ 20 µs per token at p99 (CGU-14 §3). Measured on kind-bearing text,
    best of 9 runs (a loaded machine inflates single runs, never the best), garbage collection paused so a collector pause is not billed to a token."""
    import gc

    text = _doc(20_000)
    toks = [text[i : i + 16] for i in range(0, len(text), 16)]
    best = float("inf")
    was_enabled = gc.isenabled()
    gc.disable()
    try:
        for _ in range(9):
            per: list[float] = []
            sp = BlocksV1Splitter()
            for t in toks:
                t0 = time.perf_counter()
                sp.feed(t)
                per.append(time.perf_counter() - t0)
            sp.finish()
            per.sort()
            best = min(best, per[int(len(per) * 0.99)])
    finally:
        if was_enabled:
            gc.enable()
    assert best < 20e-6, best


def test_mixed_array_names_no_kind_before_validation() -> None:
    (b,) = blocks_v1_dicts('[{"__kind":"a"},{"__kind":"b"}]\n')
    assert (b["kind"], b["array"], b["items"]) == (None, True, [{"kind": "a"}, {"kind": "b"}])
    (same,) = blocks_v1_dicts('[{"__kind":"a"},{"__kind":"a"}]\n')
    assert same["kind"] == "a"


# ── PF-1 D9: a markdown block's regions (fences and GFM tables, read by markdown-it-py) ──────


def _regions(text: str) -> list[tuple[str, str | None, str]]:
    raw = text.encode("utf-8")
    return [
        (r["type"], r["language"], raw[r["start"] : r["end"]].decode("utf-8"))
        for b in blocks_v1_dicts(text)
        if b["type"] == "markdown"
        for r in b["regions"]
    ]


REGION_CASES: dict[str, tuple[str, list[tuple[str, str | None, str]]]] = {
    "no regions": ("Just prose | with a pipe.\n", []),
    "fence with language": ("Hi\n\n```python title\nx = 1\n```\nafter\n", [("code", "python", "```python title\nx = 1\n```\n")]),
    "bare fence": ("```\nplain\n```", [("code", None, "```\nplain\n```")]),
    "tilde fence": ("~~~mermaid\ngraph TD\n~~~\n", [("code", "mermaid", "~~~mermaid\ngraph TD\n~~~\n")]),
    "gfm table": ("Intro\n\n| a | b |\n|---|---|\n| 1 | 2 |\n\nafter\n", [("table", None, "| a | b |\n|---|---|\n| 1 | 2 |\n")]),
    "table in a fence is code": ("```\n| a |\n|---|\n```\n", [("code", None, "```\n| a |\n|---|\n```\n")]),
    "nested fence follows the parser": (
        "````markdown\n```js\nx\n```\n````\n",
        [("code", "markdown", "````markdown\n```js\nx\n```\n````\n")],
    ),
    "indented code is not a region": ("    ```python\n    x\n", []),
    "cut-off fence runs to the end": ("```html\n<b>x</b>\n", [("code", "html", "```html\n<b>x</b>\n")]),
    "fence in a list item": ("- item\n  ```sh\n  ls\n  ```\n", [("code", "sh", "  ```sh\n  ls\n  ```\n")]),
    "crlf and unicode offsets": (
        "héllo 👋\r\n\r\n```py\r\né = 1\r\n```\r\n| é |\r\n|---|\r\n",
        [("code", "py", "```py\r\né = 1\r\n```\r\n"), ("table", None, "| é |\r\n|---|\r\n")],
    ),
    "json fence that is not a kind": ('```json\n{"a": 1}\n```\n', [("code", "json", '```json\n{"a": 1}\n```\n')]),
}


@pytest.mark.parametrize("name", list(REGION_CASES))
def test_markdown_regions(name: str) -> None:
    text, want = REGION_CASES[name]
    assert _regions(text) == want


def test_a_kind_fence_is_a_kind_block_not_a_region() -> None:
    text = 'Before\n\n```json\n{"__kind":"flashcard_set","title":"T"}\n```\n\n```py\nx\n```\n'
    blocks = blocks_v1_dicts(text)
    assert [b["type"] for b in blocks] == ["markdown", "kind", "markdown"]
    assert blocks[0]["regions"] == []
    assert [(r["type"], r["language"]) for r in blocks[2]["regions"]] == [("code", "py")]


def test_every_markdown_block_carries_regions_and_others_never() -> None:
    for text, _ in [*CASES.values(), *REGION_CASES.values()]:
        for b in blocks_v1_dicts(text):
            assert ("regions" in b) == (b["type"] == "markdown")


def test_regions_are_read_once_at_the_end_not_on_the_token_path() -> None:
    sp = BlocksV1Splitter()
    events = sp.feed("```py\nx\n```\n\n")
    events += sp.feed('{"__kind":"flashcard_set","title":"T"}\n')
    assert not any(e["event"] == "block.regions" for e in events)
    assert "regions" not in sp.blocks[0].fields
    tail = sp.finish()
    assert [e["event"] for e in tail][-1] == "block.regions"
    assert sp.blocks[0].fields["regions"][0]["language"] == "py"


def test_reading_regions_at_the_end_is_bounded() -> None:
    """One GFM parse per markdown block, once per reply: 70 KB of fenced markdown stays well under 100 ms."""
    text = _doc(70_000)
    best = float("inf")
    for _ in range(3):
        sp = BlocksV1Splitter()
        sp.feed(text)
        t0 = time.perf_counter()
        sp.finish()
        best = min(best, time.perf_counter() - t0)
    assert best < 0.1, best
