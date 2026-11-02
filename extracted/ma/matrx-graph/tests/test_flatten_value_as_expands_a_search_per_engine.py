"""``data.flatten`` ``value_as``: a list of plain values (engine names) expands into one object per value, the
parent's fields carried onto each — through the real scheduler.

The Smart Add rules-check finding (CONVERSION-PLAYBOOK, 2026-10-28): Run web searches kept one copied arm per
engine because ``path: engines`` gave bare strings and ``carry`` refused a child that is not an object.
"""

from __future__ import annotations

from typing import Any

import pytest
from pydantic import ValidationError

from matrx_graph import (
    Definition,
    MemoryCheckpointer,
    NodeRegistry,
    RunStatus,
    Scheduler,
    compile_graph,
    register_builtin_nodes,
)
from matrx_graph.nodes.data.flatten import FlattenConfig

from tests._fixtures import make_app_context

SEARCHES = [
    {"role": "name", "query": '"Ana Ruiz"', "count": 10, "engines": ["brave", "google"]},
    {"role": "name_place", "query": '"Ana Ruiz" "Portland"', "count": 10, "engines": ["google"]},
]


async def _run(items: list[Any], config: dict[str, Any]):
    reg = NodeRegistry()
    register_builtin_nodes(reg)
    defn = Definition.model_validate(
        {"nodes": [{"id": "n", "type": "data.flatten", "position": {"x": 0, "y": 0},
                    "data": {"config": config, "inputs": {"items": items}}}], "edges": []}
    )
    graph = compile_graph(defn, registry=reg)
    return await Scheduler(graph, MemoryCheckpointer(), make_app_context(), registry=reg).run(
        run_id="t-flatten-value-as", inputs={}
    )


async def test_one_call_per_engine_each_carrying_its_search() -> None:
    result = await _run(SEARCHES, {"path": "engines", "value_as": "engine",
                                   "carry": {"role": "role", "query": "query", "count": "count"}})
    assert result.status is RunStatus.COMPLETED, result.error
    out = result.last_outputs["n"]
    assert out["items"] == [
        {"engine": "brave", "role": "name", "query": '"Ana Ruiz"', "count": 10},
        {"engine": "google", "role": "name", "query": '"Ana Ruiz"', "count": 10},
        {"engine": "google", "role": "name_place", "query": '"Ana Ruiz" "Portland"', "count": 10},
    ]
    assert out["sources"] == 2


async def test_without_value_as_a_plain_child_is_still_refused_by_name() -> None:
    result = await _run(SEARCHES, {"path": "engines", "carry": {"query": "query"}})
    assert result.status is not RunStatus.COMPLETED
    assert "value_as" in str(result.error)


def test_value_as_alone_or_clashing_with_a_carry_name_is_refused() -> None:
    with pytest.raises(ValidationError, match="value_as"):
        FlattenConfig.model_validate({"path": "engines", "value_as": "engine"})
    with pytest.raises(ValidationError, match="more than once"):
        FlattenConfig.model_validate({"path": "engines", "value_as": "engine", "carry": {"engine": "role"}})
