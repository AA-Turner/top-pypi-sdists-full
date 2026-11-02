"""``text.regex_extract`` items mode — one pattern over a list of texts, each item keeping its own matches,
through the real scheduler.

Unit 8 (Find the key people) pulls "founded by X" out of every web result's snippet; with one text only, the
snippets had to be joined and split back, losing which page named whom (SMART-ADD-IDENTIFY.md behavior 4).
"""

from __future__ import annotations

from typing import Any

from matrx_graph import (
    Definition,
    MemoryCheckpointer,
    NodeRegistry,
    RunStatus,
    Scheduler,
    compile_graph,
    register_builtin_nodes,
)

from tests._fixtures import make_app_context

FOUNDER = r"(?:founded by|co-founder) (?P<name>[A-Z][a-z]+ [A-Z][a-z]+)"
RESULTS = [
    {"url": "https://a.example/about", "snippet": "Acme was founded by Ana Ruiz in 2009."},
    {"url": "https://b.example/news", "snippet": "No names here."},
    {"url": "https://c.example/p", "snippet": "Talk with co-founder Ben Ode and later founded by Cy Dee."},
    {"url": "https://d.example/x"},
]


async def _run(inputs: dict[str, Any], config: dict[str, Any]):
    reg = NodeRegistry()
    register_builtin_nodes(reg)
    defn = Definition.model_validate(
        {"nodes": [{"id": "n", "type": "text.regex_extract", "position": {"x": 0, "y": 0},
                    "data": {"config": config, "inputs": inputs}}], "edges": []}
    )
    graph = compile_graph(defn, registry=reg)
    return await Scheduler(graph, MemoryCheckpointer(), make_app_context(), registry=reg).run(
        run_id="t-regex-items", inputs={}
    )


async def test_each_item_keeps_its_own_matches_and_the_page_they_came_from() -> None:
    result = await _run({"items": RESULTS}, {"pattern": FOUNDER, "text_path": "snippet"})
    assert result.status is RunStatus.COMPLETED, result.error
    out = result.last_outputs["n"]
    assert [(r["item"]["url"], [m["name"] for m in r["matches"]]) for r in out["results"]] == [
        ("https://a.example/about", ["Ana Ruiz"]),
        ("https://b.example/news", []),
        ("https://c.example/p", ["Ben Ode", "Cy Dee"]),
        ("https://d.example/x", []),
    ]
    assert out["count"] == 3 and out["first"] == {"name": "Ana Ruiz"}
    assert out["unread"] == 1


async def test_one_text_still_works_and_neither_input_is_refused_by_name() -> None:
    one = await _run({"text": "founded by Ana Ruiz"}, {"pattern": FOUNDER})
    assert one.status is RunStatus.COMPLETED, one.error
    assert one.last_outputs["n"]["matches"] == [{"name": "Ana Ruiz"}]
    assert "results" not in one.last_outputs["n"]  # one-text mode emits only the published keys
    neither = await _run({}, {"pattern": FOUNDER})
    assert neither.status is not RunStatus.COMPLETED
    assert "`text` (one text) or `items`" in str(neither.error)
