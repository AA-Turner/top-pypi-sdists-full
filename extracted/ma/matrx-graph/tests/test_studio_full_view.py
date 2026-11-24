"""The full run view (the Workflow Studio, Arman 2026-11-01: "the studio is for building so we cannot hide
things"): every by-reference and held value is resolved inline, nothing screened, trimmed or withheld."""

from __future__ import annotations

from typing import Any

from matrx_graph.checkpoint import value_store
from matrx_graph.checkpoint.value_store import HELD_KEY, MISSING_VALUE_KEY, full_views, screen_views
from matrx_graph.checkpoint.values import REF_KEY


def _store(monkeypatch, values: dict[str, Any]) -> None:
    async def _load(run_id: str, hashes: Any) -> dict[str, Any]:
        return {h: values[h] for h in hashes if h in values}

    monkeypatch.setattr(value_store, "load_run_values", _load)


async def test_every_stored_value_comes_back_whole(monkeypatch) -> None:
    page = "<html>" + "x" * 50_000 + "</html>"
    _store(
        monkeypatch,
        {
            "a" * 64: {"html": page, "nested": {REF_KEY: "b" * 64}},
            "b" * 64: ["deep", "value"],
            "c" * 64: {"provision": "snapshot"},
        },
    )
    payload = {
        "event": "node_completed",
        "output": {"pages": {REF_KEY: "a" * 64}, "requests": [1, 2], "messages": [{"role": "user"}]},
        "inputs": {"provision": {HELD_KEY: "c" * 64}},
    }
    [view] = await full_views("run", [payload])
    assert view["output"]["pages"] == {"html": page, "nested": ["deep", "value"]}
    assert view["output"]["requests"] == [1, 2]  # a debug-only key is NOT dropped
    assert view["output"]["messages"] == [{"role": "user"}]  # NOT emptied
    assert view["inputs"]["provision"] == {"provision": "snapshot"}  # a held value is shown
    assert "withheld" not in view


async def test_a_value_the_run_lost_is_named_never_a_silent_gap(monkeypatch) -> None:
    _store(monkeypatch, {})
    [view] = await full_views("run", [{"output": {REF_KEY: "d" * 64}}])
    assert view == {"output": {MISSING_VALUE_KEY: "d" * 64}}


async def test_the_screen_view_still_screens(monkeypatch) -> None:
    """The full view is a separate door: everyone outside the Studio keeps the screen view."""
    _store(monkeypatch, {})

    async def _cap() -> int:
        return 20

    monkeypatch.setattr("matrx_graph.knobs.withheld_list_max", _cap)
    [view] = await screen_views("run", [{"event": "node_completed", "output": {"requests": [1], "answer": "ok"}}])
    assert "requests" not in view["output"]
    assert view["output"]["answer"] == "ok"
