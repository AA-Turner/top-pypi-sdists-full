"""The live stream splits INCREMENTALLY, answers exactly what a whole-buffer split answers, and
its cost grows linearly with the answer.

WHY THIS EXISTS (2026-10-08, lane S). ``StreamBlockProcessor`` used to re-split its WHOLE
buffer on every token, and the splitter itself re-joined every remaining line at every line
(``extract_unrecognized_xml_block``) — a streamed answer cost (tokens x lines x length). A
9 KB answer took 2 s of CPU in 16-character tokens; the 56 KB one-line answer of an Applet
build ~90 s, all of it on the worker's event loop. The kind_records replay had the same class
(aidream 2e43ffdd40).

Two halves held here:

* IDENTITY — ``IncrementalBlockSplitter.split`` equals ``split_content_into_blocks(buffer)`` at
  every token, over every shape the detector types (fences, tables, XML regions, mid-line
  splices, generic XML, trees, front matter, directive containers, bare and root-kind JSON,
  CRLF), and the processor's finished blocks equal a whole-buffer re-split processor's.
  (Also proven on 113 real stored assistant answers on 2026-10-08 — the lane S report.)
* LINEARITY — a 200 KB answer in 16-character tokens finishes inside a budget a 4-core box
  meets with room, and doubling the answer at most ~triples the time. Restoring the
  whole-buffer re-split turns these red (the stream is abandoned at the budget).

Run: ``uv run pytest packages/matrx-ai/matrx_ai/processing/blocks/tests/test_incremental_split.py -q``
"""

from __future__ import annotations

import json
import time

import pytest

from matrx_ai.processing.blocks import stream_processor as sp_module
from matrx_ai.processing.blocks.block_detector import (
    IncrementalBlockSplitter,
    split_content_into_blocks,
)
from matrx_ai.processing.blocks.stream_processor import IR_PARTIAL_KEY, StreamBlockProcessor


def _key(block) -> tuple:
    return (
        block.type,
        block.content,
        block.language,
        block.src,
        block.alt,
        json.dumps(block.metadata, sort_keys=True, default=str),
    )


SHAPES: dict[str, str] = {
    "prose": "# Title\n\nFirst paragraph with **bold**.\nSecond line.\n\n- a\n- b\n\nEnd.\n",
    "table": "Intro:\n\n| Name | Score |\n| --- | --- |\n| Ada | 9 |\n| Lin | 7 |\n\nAfter the table.\n",
    "pipeless_table": "Notes | Value\n--- | ---\nx | 1\n\nDone.\n",
    "fences": "Code:\n\n```python\nprint('hi')\n```\n\n````md\n```js\nx\n```\n````\n\nTail text.\n",
    "unclosed_fence": "Before\n\n```python\nwhile True:\n    pass\n",
    "fenced_json": "Quiz:\n\n```json\n" + json.dumps({"quiz_title": "Q", "multiple_choice": [{"question": "a?", "options": ["x", "y"], "correctAnswer": 0, "explanation": "e"}]}, indent=2) + "\n```\n\nMore.\n",
    "xml_block": "Thinking done.\n\n<timeline>\n- 2020: start\n- 2021: grow\n</timeline>\n\nAfter.\n",
    "thinking": "<thinking>\nstep one\nstep two\n</thinking>\n\nThe answer is 4.\n",
    "orphan_close": "still thinking about it\n</thinking>\nHere is the answer.\n",
    "mid_line_decision": 'Pick one: <decision prompt="Which?">\n<option value="a">A</option>\n<option value="b">B</option>\n</decision>\n\nThanks.\n',
    "generic_xml": "Data:\n\n<inventory>\n  <item id=\"1\">Bolt</item>\n  <item id=\"2\">Nut</item>\n</inventory>\n\nThat's all.\n",
    "unclosed_generic_xml": "Data:\n\n<inventory>\n  <item id=\"1\">Bolt</item>\n",
    "html_block": "<div class=\"x\">\nhello\n\nprose after\n",
    "tree": "Layout:\n\nsrc\n├── app\n│   └── page.tsx\n└── lib\n    └── util.ts\n\nDone.\n",
    "front_matter": "---\ntitle: Doc\ntags: [a, b]\n---\n\n# Heading\n\nBody.\n",
    "directive_container": ":::tabs\n## One\nfirst\n## Two\n```js\nx\n```\n:::\n\nAfter.\n",
    "bare_json": 'Here:\n{"a": 1, "b": {"c": [1, 2]}}\nThen prose.\n',
    "root_kind_json": json.dumps({"__kind": "note_probe", "title": "T", "items": [{"n": i} for i in range(30)]}),
    "embedded_kind": 'See {"__kind": "note_probe", "title": "inline"} in prose.\n\nMore {not json}.\n',
    "media": "![alt](https://example.com/a.png)\n\n[video](https://example.com/v.mp4)\n\nText.\n",
    "dividers": "Above\n\n***\n\nBelow\n\n#===\n\nEnd\n",
    "crlf": "Line one\r\nLine two\r\n\r\n| a | b |\r\n| - | - |\r\n| 1 | 2 |\r\n\r\nEnd\r\n",
    "long_line": "word " * 1500 + "\n\n```json\n" + json.dumps({"k": "v" * 5000}) + "\n```\n",
}
SHAPES["everything"] = "\n\n".join(SHAPES[k] for k in sorted(SHAPES) if k not in ("root_kind_json", "front_matter"))


@pytest.mark.parametrize("chunk", [1, 3, 16])
@pytest.mark.parametrize("shape", sorted(SHAPES))
def test_the_incremental_split_equals_the_whole_buffer_split_at_every_token(shape: str, chunk: int) -> None:
    text = SHAPES[shape]
    if chunk == 1 and len(text) > 4000:
        pytest.skip("one-character feeding of the long shapes is covered at 3 and 16")
    splitter = IncrementalBlockSplitter()
    buffer = ""
    for start in range(0, len(text), chunk):
        piece = text[start : start + chunk]
        buffer += piece
        got = splitter.split(piece)
        assert [_key(b) for b in got] == [_key(b) for b in split_content_into_blocks(buffer)], (
            f"{shape}: diverged at {len(buffer)} chars"
        )


def test_settled_blocks_are_the_same_objects_and_never_re_read() -> None:
    # Every construct here closes (an unclosed fence or XML root owns the rest of the answer,
    # so nothing after one can settle — correctly).
    text = _markdown_answer(30_000)
    splitter = IncrementalBlockSplitter()
    previous: list = []
    previous_settled = 0
    for start in range(0, len(text), 16):
        got = splitter.split(text[start : start + 16])
        assert all(got[i] is previous[i] for i in range(previous_settled))
        previous, previous_settled = got, splitter.settled_count
    assert splitter.settled_count > 0.8 * len(previous)


class _WholeBufferProcessor(StreamBlockProcessor):
    """The processor as it was: a whole-buffer re-split on every token, every block compared."""

    def _detect_and_emit(self):
        return self._reconcile_blocks(split_content_into_blocks(self._buffer), is_final=False)


def _finished(processor_class: type[StreamBlockProcessor], text: str, chunk: int) -> list[tuple]:
    processor = processor_class()
    for start in range(0, len(text), chunk):
        processor.process_token(text[start : start + chunk])
    processor.finalize()
    return [
        (
            b.block_id,
            b.type,
            b.status,
            b.content,
            json.dumps(b.data, sort_keys=True, default=str),
            json.dumps({k: v for k, v in b.metadata.items() if k != IR_PARTIAL_KEY}, sort_keys=True, default=str),
        )
        for b in processor.get_blocks()
    ]


@pytest.mark.parametrize("chunk", [3, 16])
@pytest.mark.parametrize("shape", sorted(SHAPES))
def test_the_finished_blocks_equal_a_whole_buffer_processor(
    shape: str, chunk: int, monkeypatch: pytest.MonkeyPatch
) -> None:
    text = SHAPES[shape]
    got = _finished(StreamBlockProcessor, text, chunk)
    # The reference detects on every token, unthrottled, exactly as before.
    monkeypatch.setattr(sp_module, "_LONG_LINE_FLOOR", 10**12)
    monkeypatch.setattr(sp_module, "_PARTIAL_FLOOR", 10**12)
    assert got == _finished(_WholeBufferProcessor, text, chunk)


# ---------------------------------------------------------------------------
# Linearity
# ---------------------------------------------------------------------------

#: Generous for a loaded 4-core CI box: measured ~2 s for 200 KB on one core, 2026-10-08.
#: The whole-buffer processor needs many minutes for the same answer.
_BUDGET_S = 30.0


def _markdown_answer(size: int) -> str:
    parts: list[str] = []
    k = 0
    while sum(len(p) for p in parts) < size:
        parts.append(
            f"## Section {k}\n\nA paragraph about item {k} with **bold**, `code` and a "
            f"[link](https://example.com/{k}).\nA second line of prose.\n\n"
        )
        if k % 3 == 0:
            parts.append("| Name | Value |\n| --- | --- |\n| a | 1 |\n| b | 2 |\n\n")
        if k % 4 == 1:
            parts.append("```python\ndef f(x):\n    return x * 2\n```\n\n")
        if k % 5 == 2:
            parts.append("- one\n- two\n  - nested\n\n")
        if k % 7 == 3:
            parts.append("<timeline>\n- 2020: start\n- 2021: grow\n</timeline>\n\n")
        k += 1
    return "".join(parts)[:size]


def _one_line_kind_answer(size: int) -> str:
    items = []
    doc = {"__kind": "applet_build_probe", "title": "Build", "files": items}
    while len(json.dumps(doc)) < size:
        items.append({"path": f"src/file_{len(items)}.tsx", "source": "export const x = 1;\\n" * 20})
    return json.dumps(doc)


def _stream_seconds(text: str) -> float:
    processor = StreamBlockProcessor()
    started = time.perf_counter()
    for start in range(0, len(text), 16):
        processor.process_token(text[start : start + 16])
        if start % 4096 == 0 and time.perf_counter() - started > _BUDGET_S:
            pytest.fail(f"streaming {len(text)} chars passed the {_BUDGET_S:.0f}s budget at {start} chars")
    processor.finalize()
    return time.perf_counter() - started


@pytest.mark.parametrize("make", [_markdown_answer, _one_line_kind_answer], ids=["markdown", "one_line_kind_json"])
def test_a_200kb_answer_streams_in_linear_time(make) -> None:
    half = _stream_seconds(make(100_000))
    full = _stream_seconds(make(200_000))
    assert full < _BUDGET_S, f"200 KB took {full:.1f}s"
    # Linear work doubles; quadratic quadruples. 3x leaves room for timer noise.
    assert full <= 3 * max(half, 0.05), f"100 KB {half:.2f}s -> 200 KB {full:.2f}s: not linear"
