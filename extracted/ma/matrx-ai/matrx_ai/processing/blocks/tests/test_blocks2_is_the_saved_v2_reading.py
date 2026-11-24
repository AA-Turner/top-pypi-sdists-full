"""blocks2 — the saved half of blocks v2 is the server's reading, never the client's parse (P1-CHAT T1 v2.1).

A saved text part carries the unchanged v1 fields (installed phones and web builds decode only those) and, while
``platform.debug.blocks_v2_save_enabled`` is on, a SIBLING key ``blocks2``: the full reading — regions with
``region_kind`` / ``display`` / ``language`` / ``container`` / ``complete``, kind statuses, the digest's label,
citations, every block's ``complete`` and a stopped reply's mark. Breaks this guards:

* v1 gains a field when the knob is on (an installed decoder meets an undeclared key);
* blocks2's regions differ from what the live v2 events announced for the same text (a second reading);
* a stopped reply saves its open block or region as complete, or does not say it was stopped;
* the close-off of a Stop closes past the cut the save keeps (the client's ``seen_seq`` cut);
* the forced-degraded debug knob does not reach the wire.
"""

from __future__ import annotations

import asyncio
from types import SimpleNamespace
from typing import Any

import pytest

from matrx_ai.processing.blocks import saved_blocks
from matrx_ai.processing.blocks.live_blocks_v2 import LiveBlocksStreamV2

MIXED = (
    "Here is the area:\n\n"
    "$$\nA = \\pi r^2\n$$\n\n"
    "- a list item with code:\n\n"
    "  ```python\n  print(1)\n  ```\n\n"
    "<svg viewBox=\"0 0 10 10\">\n<circle r=\"4\"/>\n</svg>\n\n"
    '{"__kind": "nonexistent_test_kind_zz", "title": "x"}\n\n'
    "And prose after the kind.\n"
)
TABLE = "Prices:\n\n| item | cost |\n| --- | --- |\n| tea | 2 |\n| cake | 4 |\n"


@pytest.fixture
def v2_on():
    saved_blocks.configure_block_regions_save(lambda: True)
    saved_blocks.configure_blocks_v2_save(lambda: True)
    try:
        yield
    finally:
        saved_blocks.configure_blocks_v2_save(None)
        saved_blocks.configure_block_regions_save(None)


def _v1(text: str) -> dict[str, Any]:
    """The fields with the v2 knob OFF (what installed readers get), whatever the test's knob state."""
    was = saved_blocks._v2_enabled
    saved_blocks.configure_block_regions_save(lambda: True)
    saved_blocks.configure_blocks_v2_save(None)
    try:
        return saved_blocks.block_fields(text)
    finally:
        saved_blocks.configure_blocks_v2_save(was)


def _live_regions(text: str) -> list[dict[str, Any]]:
    """What the live v2 stream announced for ``text`` (word-sized chunks), as blocks2 regions."""
    stream = LiveBlocksStreamV2("m")
    events: list[Any] = []
    for i in range(0, len(text), 5):
        events.extend(stream.feed(text[i : i + 5]))
    events.extend(stream.finish())
    opened: dict[tuple[int, int], dict[str, Any]] = {}
    starts: dict[int, int] = {}
    for e in events:
        d = e.model_dump()
        if d["type"] == "block.open":
            starts[d["index"]] = d["start"]
        elif d["type"] == "region.open":
            opened[(d["index"], d["region"])] = {
                "region_kind": d["region_kind"],
                "display": d["display"],
                "start": d["start"],
                "container": d.get("container"),
                "language": d.get("language"),
            }
        elif d["type"] == "region.close":
            opened[(d["index"], d["region"])]["complete"] = d["complete"]
    return [opened[k] for k in sorted(opened)]


def test_knob_off_saves_v1_only_and_unchanged() -> None:
    fields = _v1(MIXED)
    assert "blocks2" not in fields
    assert set(fields) == {"blocks_version", "blocks_of", "blocks"}


def test_knob_on_adds_blocks2_beside_an_identical_v1(v2_on) -> None:
    on = saved_blocks.block_fields(MIXED)
    off = _v1(MIXED)
    assert {k: on[k] for k in saved_blocks.BLOCK_FIELDS} == off, "v1 must not change when the v2 knob is on"
    b2 = on["blocks2"]
    assert b2["version"] == 2 and b2["of"] == saved_blocks.text_fingerprint(MIXED)
    kinds = [r["region_kind"] for b in b2["blocks"] if b["type"] == "markdown" for r in b["regions"]]
    assert "math" in kinds and "svg" in kinds and "code" in kinds
    nested = [r for b in b2["blocks"] if b["type"] == "markdown" for r in b["regions"] if r["region_kind"] == "code"]
    assert nested[0]["container"] == ["list_item"] and nested[0]["language"] == "python"
    kind = next(b for b in b2["blocks"] if b["type"] == "kind")
    assert kind["status"] in {"valid", "invalid", "unknown_kind", "unchecked", "repaired", "incomplete"}
    assert all(b["complete"] is True for b in b2["blocks"]), "a finished reply's blocks are complete"
    assert b2["blocks"][-1]["type"] == "markdown", "the prose after the kind is its own block"
    assert "stopped" not in b2


@pytest.mark.parametrize("text", [MIXED, TABLE, "```js\nlet x\n", "> quote\n> ```sh\n> ls\n> ```\n\ntail\n"])
def test_blocks2_regions_are_the_live_v2_reading(v2_on, text: str) -> None:
    b2 = saved_blocks.block_fields(text)["blocks2"]
    saved = []
    for b in b2["blocks"]:
        if b["type"] != "markdown":
            continue
        for r in b["regions"]:
            saved.append(
                {
                    "region_kind": r["region_kind"],
                    "display": r["display"],
                    "start": r["start"] - b["start"],
                    "container": r.get("container"),
                    "language": r.get("language"),
                    "complete": r["complete"],
                }
            )
    live = _live_regions(text)
    # live region starts are part-relative too when the block starts at 0; compare block-relative by rebasing
    assert [{**r, "start": None} for r in saved] == [{**r, "start": None} for r in live]


def test_a_stopped_reply_saves_its_open_block_and_region_incomplete(v2_on) -> None:
    cut = TABLE[: TABLE.index("| cake")]  # Stop mid-table
    fields = saved_blocks.annotate_content([{"type": "text", "text": cut}], stopped=True)[0]
    b2 = fields["blocks2"]
    assert b2["stopped"] is True
    last = b2["blocks"][-1]
    assert last["complete"] is False
    assert last["regions"][-1]["region_kind"] == "table" and last["regions"][-1]["complete"] is False
    assert {k: fields[k] for k in saved_blocks.BLOCK_FIELDS} == _v1(cut), "the stop never changes v1"


def test_only_the_last_text_part_of_a_stopped_reply_is_marked(v2_on) -> None:
    content = [{"type": "text", "text": "first.\n"}, {"type": "thinking", "text": "t"}, {"type": "text", "text": "```py\nx"}]
    out = saved_blocks.annotate_content(content, stopped=True)
    assert "stopped" not in out[0]["blocks2"] and out[0]["blocks2"]["blocks"][-1]["complete"] is True
    assert out[2]["blocks2"]["stopped"] is True


def test_a_part_with_current_v1_gains_blocks2_and_keeps_its_v1(v2_on) -> None:
    saved_blocks.configure_blocks_v2_save(None)
    part = {"type": "text", "text": MIXED, **_v1(MIXED)}
    part["blocks"][0]["canvas"] = []  # what the host's canvas step recorded
    saved_blocks.configure_blocks_v2_save(lambda: True)
    out = saved_blocks.annotate_content([part])[0]
    assert out["blocks"] is part["blocks"] and out["blocks"][0]["canvas"] == []
    assert out["blocks2"]["of"] == saved_blocks.text_fingerprint(MIXED)
    # and a later stop of the same text re-marks it
    again = saved_blocks.annotate_content([out], stopped=True)[0]
    assert again["blocks2"]["stopped"] is True


def test_message_blocks_carries_blocks2_and_the_models_accept_it(v2_on) -> None:
    from matrx_ai.db.message_parts import TextPart

    citations = [{"cited_text": "pi", "answer_start": 0, "answer_end": 4}]
    part = saved_blocks.annotate_content([{"type": "text", "text": MIXED, "id": "p1"}])[0]
    part["blocks2"] = saved_blocks.blocks2_reading(MIXED, part["blocks"], citations=citations)
    payload = saved_blocks.message_blocks_payload("m", [part])
    sent = payload.model_dump(exclude_none=True)["parts"][0]
    from matrx_connect.context.reply_blocks import SavedBlocks2

    row = SavedBlocks2.model_validate(part["blocks2"]).model_dump(exclude_none=True)
    assert sent["blocks2"] == row, "message_blocks and the row carry the same object"
    assert sent["blocks2"]["citations"] == citations
    TextPart.model_validate({k: v for k, v in part.items()})


def test_a_stop_closes_off_at_the_press_not_at_the_last_watermark_sent() -> None:
    text = "one two three four five six seven eight nine ten.\n"
    stream = LiveBlocksStreamV2("m")
    for word in text.split(" "):
        stream.feed(word + " ")
    assert stream.shown_chars > 20
    closes = [e.model_dump() for e in stream.close_off(cut_chars=8)]
    block = next(c for c in closes if c["type"] == "block.close")
    assert block["end"] == 8 and block["complete"] is False and block["block"]["end"] == 8


def test_a_stop_with_no_press_cut_closes_at_the_last_watermark_sent() -> None:
    stream = LiveBlocksStreamV2("m")
    stream.feed("alpha beta gamma ")
    shown = len(b"alpha beta gamma "[: len(stream._all)])
    closes = [e.model_dump() for e in stream.close_off()]
    block = next(c for c in closes if c["type"] == "block.close")
    assert 0 < block["end"] <= shown


class _Recorder:
    def __init__(self) -> None:
        self.wire: list[tuple[str, Any]] = []

    async def send_chunk(self, text: str) -> None:
        self.wire.append(("chunk", text))

    async def send_data(self, payload: Any) -> None:
        self.wire.append(("data", payload.model_dump()))


def test_the_forced_degraded_knob_sends_blocks_degraded_on_a_v2_turn() -> None:
    from matrx_connect.context.app_context import (
        AppContext,
        clear_app_context,
        get_app_context,
        set_app_context,
    )

    from matrx_ai.processing.blocks.live_blocks import streaming_live_blocks

    async def run(forced: bool) -> list[str]:
        rec = _Recorder()
        saved_blocks.configure_force_blocks_degraded(lambda: forced)
        token = set_app_context(AppContext(user_id="u", emitter=rec, metadata={"client_reads": ["blocks-v2"]}))
        try:
            state = SimpleNamespace(reserved_message_ids={1: "row-1"}, streamed_message_ids={})
            config = SimpleNamespace(messages=SimpleNamespace(to_list=lambda: [0]))
            async with streaming_live_blocks(state, config) as live:
                await get_app_context().emitter.send_chunk("Hello there.\n")
                await live.finish()
        finally:
            clear_app_context(token)
            saved_blocks.configure_force_blocks_degraded(None)
        return [v["type"] for k, v in rec.wire if k == "data"]

    forced = asyncio.run(run(True))
    assert forced[:2] == ["blocks.ack", "blocks.degraded"] and "block.grow" in forced
    assert "blocks.degraded" not in asyncio.run(run(False))


def test_the_save_funnel_carries_the_rows_stop_into_blocks2(v2_on, monkeypatch) -> None:
    """``queue_helpers._with_saved_blocks`` reads ``metadata.stopped`` (written with the cut text by the live stop and
    the late door) and hands it to ``annotate_content``: the saved row itself says it was stopped."""
    from matrx_ai.persistence import queue_helpers

    monkeypatch.setattr(queue_helpers, "get_coordinator", lambda: None)
    saved_blocks.configure_blocks_save(lambda: True)
    try:
        cut = TABLE[: TABLE.index("| cake")]
        for stopped in (True, False):
            payload = {"id": "r", "role": "assistant", "content": [{"type": "text", "text": cut}], "metadata": {"stopped": stopped}}
            out = queue_helpers._with_saved_blocks(payload, op_type="insert", primary_key=None)
            b2 = out["content"][0]["blocks2"]
            assert bool(b2.get("stopped")) is stopped
            assert b2["blocks"][-1]["complete"] is (not stopped)
    finally:
        saved_blocks.configure_blocks_save(None)


def test_an_update_write_carries_the_rows_stop_into_blocks2(v2_on, monkeypatch) -> None:
    """The live Stop and the late door write the reserved row by UPDATE, whose ``metadata`` reaches the funnel as the
    key-level ``JsonbPatch`` ``_with_run_ids`` makes of it, never a dict. Reading only a dict saved and announced every
    stopped reply's ``blocks2`` unmarked and its cut block ``complete: true`` (S3 --v2 on c5b96fab: 6 of 6 Stop cases)."""
    from matrx_ai.persistence import queue_helpers

    monkeypatch.setattr(queue_helpers, "get_coordinator", lambda: None)
    saved_blocks.configure_blocks_save(lambda: True)
    try:
        cut = TABLE[: TABLE.index("| cake")]
        fields = {"role": "assistant", "content": [{"type": "text", "text": cut}], "metadata": {"stopped": True}}
        payload = queue_helpers._with_run_ids(fields, creating=False, row_id="r")
        assert not isinstance(payload["metadata"], dict), "an UPDATE's metadata is a key-level patch"
        out = queue_helpers._with_saved_blocks(payload, op_type="update", primary_key=("id", "r"))
        b2 = out["content"][0]["blocks2"]
        assert b2.get("stopped") is True
        assert b2["blocks"][-1]["complete"] is False
        assert b2["blocks"][-1]["regions"][-1]["complete"] is False
    finally:
        saved_blocks.configure_blocks_save(None)


FENCED = "Intro line.\n\n```python\nx = 1\ny = 2\nz = 3\n```\n\nMore prose after the code, and then some more words.\n"


def _fed(text: str) -> tuple[LiveBlocksStreamV2, list[dict[str, Any]]]:
    stream = LiveBlocksStreamV2("m")
    events: list[dict[str, Any]] = []
    for i in range(0, len(text), 4):
        events.extend(e.model_dump() for e in stream.feed(text[i : i + 4]))
    return stream, events


def test_a_late_stop_closes_the_region_open_at_the_cut_even_after_the_server_closed_it() -> None:
    """The cancel reaches the run after the server streamed past the press (another task's Stop, a fast model): the
    reader already closed the fence ``complete: true``. The close-off must close it again ``complete: false`` AT THE
    CUT — before, it closed only what was open NOW and sent no region.close (S3 ``stop``, server c5b96fab)."""
    stream, events = _fed(FENCED)
    live_close = next(e for e in events if e["type"] == "region.close")
    assert live_close["complete"] is True, "the server closed the fence before the stop reached it"
    cut = FENCED.index("y = 2")
    closes = [e.model_dump() for e in stream.close_off(cut_chars=cut)]
    region = [c for c in closes if c["type"] == "region.close"]
    assert region and region[0]["complete"] is False and region[0]["end"] == cut
    block = next(c for c in closes if c["type"] == "block.close")
    assert block["end"] == cut and block["complete"] is False


def test_a_late_stop_leaves_a_region_closed_before_the_cut_alone() -> None:
    stream, _ = _fed(FENCED)
    cut = FENCED.index("More prose") + 4
    closes = [e.model_dump() for e in stream.close_off(cut_chars=cut)]
    assert not [c for c in closes if c["type"] == "region.close"], "the fence closed before the cut: nothing to re-close"
    block = next(c for c in closes if c["type"] == "block.close")
    assert block["end"] == cut and block["complete"] is False


def test_a_late_stop_recloses_a_block_the_server_closed_past_the_cut() -> None:
    """A markdown block closed by what followed it (a kind) after the press is open at the cut: closed again there."""
    text = "Some words before the kind and more of them.\n\n" + '{"__kind": "nonexistent_test_kind_zz", "title": "x"}\n\nTail.\n'
    stream, events = _fed(text)
    first = next(e for e in events if e["type"] == "block.close")
    assert first["index"] == 0 and first["complete"] is True
    cut = text.index("before")
    closes = [e.model_dump() for e in stream.close_off(cut_chars=cut)]
    again = [c for c in closes if c["type"] == "block.close" and c["index"] == 0]
    assert again and again[0]["end"] == cut and again[0]["complete"] is False


def test_a_stop_withdraws_every_region_announced_wholly_past_the_cut() -> None:
    """The server streamed on past the press and announced + closed later regions; the saved text ends at the cut.
    The close-off closes each of them ``complete: false`` at its own start (an empty region = withdrawn), so the
    regions a client holds after it are the saved row's regions only (live stop_math, 2026-11-15)."""
    text = "Intro.\n\n$$\na^2\n$$\n\nMiddle prose.\n\n$$\nb^2\n$$\n\n$$\nc^2\n$$\n\nEnd.\n"
    stream, events = _fed(text)
    cut = text.index("Middle")
    held: dict[int, dict[str, Any]] = {}
    for e in events:
        if e["type"] == "region.open":
            held[e["region"]] = {"start": e["start"], "end": None}
        elif e["type"] == "region.close":
            held[e["region"]]["end"] = e["end"]
    assert len(held) == 3 and all(r["end"] is not None for r in held.values()), "all three were announced and closed"
    for e in stream.close_off(cut_chars=cut):
        d = e.model_dump()
        if d["type"] == "region.close":
            held[d["region"]]["end"], held[d["region"]]["complete"] = d["end"], d["complete"]
    visible = {k: r for k, r in held.items() if not (r.get("complete") is False and r["end"] <= r["start"])}
    assert list(visible) == [0], f"only the region before the cut survives: {held}"
    assert visible[0]["end"] <= cut
