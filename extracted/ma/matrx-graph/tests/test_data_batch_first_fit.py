"""``data.batch`` fit / overflow options (2026-10-27).

The break this catches: a batch closes at the first item that does not fit, so one big
page part at the front of a reading budget (or one big prompt/file in a pack) wastes
the room that later, smaller items would have filled.
Users: a reading budget over page parts (one batch, rest listed), packing prompts under
a token budget, packing files under an upload size (several batches).
"""

from __future__ import annotations

import pytest

from matrx_graph.errors import CompilationError
from tests.test_data_collections import _out, _run

# sizes are characters in `text`
def _parts(*sizes):
    return [{"id": i, "label": f"p{i}", "text": "x" * n} for i, n in enumerate(sizes)]


def _ids(batches):
    return [[i["id"] for i in b] for b in batches]


async def test_in_order_stops_at_the_first_misfit_first_fit_keeps_filling():
    items = _parts(40, 70, 30, 20)  # budget 100: 40 | 70 does not fit | 30 fits | 20 fits? 40+30=70, +20=90
    base = {"size": 100, "measure": "chars", "text_path": "text"}
    plain = await _out("data.batch", {"items": items}, base)
    assert _ids(plain["batches"]) == [[0], [1, 2], [3]]  # in_order closed batch 1 at item 1
    ff = await _out("data.batch", {"items": items}, {**base, "fit": "first_fit"})
    assert _ids(ff["batches"]) == [[0, 2, 3], [1]]
    assert ff["parts"][0]["size"] == 90 and ff["parts"][0]["ended_by"] == "budget"
    assert ff["parts"][1]["ended_by"] == "end"


async def test_first_fit_passed_over_items_keep_their_order_in_later_batches():
    items = _parts(60, 60, 60, 30, 30)
    out = await _out("data.batch", {"items": items}, {"size": 100, "measure": "chars", "text_path": "text", "fit": "first_fit"})
    assert _ids(out["batches"]) == [[0, 3], [1, 4], [2]]


async def test_left_out_makes_one_batch_and_lists_the_rest_with_sizes():
    items = _parts(40, 70, 30, 20, 500)
    cfg = {"size": 100, "measure": "chars", "text_path": "text", "overflow": "left_out", "label_path": "label"}
    out = await _out("data.batch", {"items": items}, {**cfg, "fit": "first_fit", "split_oversized": False})
    assert _ids(out["batches"]) == [[0, 2, 3]]
    assert [(row["item"], row["size"], row["label"]) for row in out["left_out"]] == [(1, 70, "p1"), (4, 500, "p4")]
    stop = await _out("data.batch", {"items": items}, {**cfg, "split_oversized": False})
    assert _ids(stop["batches"]) == [[0]]  # in_order + left_out: closes at the first misfit
    assert [row["item"] for row in stop["left_out"]] == [1, 2, 3, 4]


async def test_everything_fits_leaves_nothing_out():
    out = await _out("data.batch", {"items": _parts(10, 20)}, {"size": 100, "measure": "chars", "text_path": "text", "overflow": "left_out"})
    assert out["left_out"] == [] and out["count"] == 1


async def test_oversized_uncut_item_gets_its_own_batch_with_first_fit():
    items = [{"id": 0, "text": "x" * 10}, {"id": 1, "text": {"a": "y" * 300}}, {"id": 2, "text": "x" * 10}]
    out = await _out("data.batch", {"items": items}, {"size": 100, "measure": "chars", "text_path": "text", "fit": "first_fit", "split_oversized": False})
    assert _ids(out["batches"]) == [[0, 2], [1]]


async def test_default_is_unchanged():
    items = _parts(40, 70, 30)
    out = await _out("data.batch", {"items": items}, {"size": 100, "measure": "chars", "text_path": "text"})
    assert out["left_out"] is None  # off: null, the one left_out contract
    assert _ids(out["batches"]) == [[0], [1, 2]]


async def test_first_fit_refuses_settings_it_cannot_honour():
    with pytest.raises(CompilationError, match="cannot combine with overlap"):
        await _run("data.batch", {"items": []}, {"size": 10, "fit": "first_fit", "overlap": 1})
    with pytest.raises(CompilationError, match="max_batches"):
        await _run("data.batch", {"items": []}, {"size": 10, "overflow": "left_out", "max_batches": 2})
