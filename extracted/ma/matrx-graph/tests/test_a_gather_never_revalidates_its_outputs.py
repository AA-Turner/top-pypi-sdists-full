"""A gather's result is never re-walked by validation (event_loop_stall 21c459d7, 2026-11-17).

``GatherOutput(...)`` validated every item's ``structured_output`` as ``JsonValue`` on the loop: 1.23 s
on a wide fan-out. ``values`` already skipped validation; ``structured_outputs`` is cut from it.
"""

from __future__ import annotations

import time

from matrx_graph.nodes.control.gather import GatherOutput


def _structured(n: int) -> list[dict]:
    return [{"rows": [{"i": i, "t": "word " * 20, "tags": ["a", "b"]} for i in range(200)], "n": k} for k in range(n)]


def test_structured_outputs_are_kept_verbatim_and_not_walked() -> None:
    structured = _structured(1000)  # ~0.4 s of JsonValue validation before the fix
    started = time.perf_counter()
    out = GatherOutput(values=structured, structured_outputs=structured, count=len(structured))
    took = time.perf_counter() - started
    assert out.structured_outputs is structured or out.structured_outputs == structured
    assert took < 0.05, f"GatherOutput spent {took:.3f}s validating gathered outputs"


def test_the_published_schema_still_types_structured_outputs() -> None:
    prop = GatherOutput.model_json_schema()["properties"]["structured_outputs"]
    assert prop.get("type") == "array"
