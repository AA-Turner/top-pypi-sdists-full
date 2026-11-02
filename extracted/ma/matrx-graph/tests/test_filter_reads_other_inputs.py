"""``data.filter`` compares each item against another step's list (2026-10-26).

The break this catches: the predicate sees only the item, so "skip the articles
we already saved" cannot be written — the step either refuses the extra input
(``extra="forbid"``) or the predicate has no way to reach it. Users: a news
digest skipping articles already seen, a social lookup skipping links already
looked up, a study kit skipping outputs already saved.
"""

from __future__ import annotations

import pytest
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

ARTICLES = [
    {"url": "https://coastalgazette.news/2026/10/harbor-dredging-vote", "title": "Harbor dredging vote"},
    {"url": "https://coastalgazette.news/2026/10/ferry-schedule-winter", "title": "Winter ferry schedule"},
    {"url": "https://coastalgazette.news/2026/10/school-board-budget", "title": "School board budget"},
]


async def _run(inputs: dict, predicate: str) -> dict:
    registry = NodeRegistry()
    register_builtin_nodes(registry)
    defn = Definition.model_validate(
        {
            "nodes": [
                {
                    "id": "skip_seen",
                    "type": "data.filter",
                    "position": {"x": 0, "y": 0},
                    "data": {"config": {"predicate": predicate}, "inputs": inputs},
                }
            ],
            "edges": [],
        }
    )
    graph = compile_graph(defn, registry=registry)
    scheduler = Scheduler(graph, MemoryCheckpointer(), make_app_context(), registry=registry)
    result = await scheduler.run(run_id="t-filter-in", inputs=inputs)
    assert result.status is RunStatus.COMPLETED, result
    return result.last_outputs["skip_seen"]


@pytest.mark.parametrize(
    ("seen", "expected_titles"),
    [
        (
            ["https://coastalgazette.news/2026/10/ferry-schedule-winter"],
            ["Harbor dredging vote", "School board budget"],
        ),
        (
            [
                "https://coastalgazette.news/2026/10/harbor-dredging-vote",
                "https://coastalgazette.news/2026/10/school-board-budget",
            ],
            ["Winter ferry schedule"],
        ),
    ],
)
async def test_filter_drops_items_found_in_another_inputs_list(seen, expected_titles):
    out = await _run(
        {"items": ARTICLES, "seen": seen},
        "inputs['url'] not in inputs['$in']['seen']",
    )
    assert [a["title"] for a in out["items"]] == expected_titles
    assert out["dropped"] == len(ARTICLES) - len(expected_titles)


async def test_filter_scalar_items_compare_against_another_inputs_list():
    out = await _run(
        {
            "items": ["@harborwatch", "@ferrytimes", "@schoolboardlive"],
            "already_looked_up": ["@ferrytimes"],
        },
        "inputs['value'] not in inputs['$in']['already_looked_up']",
    )
    assert out["items"] == ["@harborwatch", "@schoolboardlive"]


async def test_filter_without_other_inputs_binds_exactly_the_item():
    # Backward compatibility: no other inputs -> no '$in' key is added, so a
    # predicate that counts the item's keys still sees only the item.
    out = await _run({"items": ARTICLES}, "len(inputs) == 2")
    assert out["kept"] == 3
