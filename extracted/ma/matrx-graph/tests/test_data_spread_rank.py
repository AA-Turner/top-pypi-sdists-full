"""``data.spread_rank`` (Rank by Spread) — through the real scheduler, every output checked against its kind.

Three unrelated callers (Rule 3), each with different settings:
- a person's knowledge buckets: notes and chats over weeks, entity-backed names, a filler cap;
- a site's topic coverage: pages with no dates, one kind, plural spellings;
- news story size: outlets as homes, headlines as the kind, a story told across days.

Hand-countable: with dates, score = (0.5 + backed share) x sum_kinds log(1 + homes) x log(1 + weeks).
"""

from __future__ import annotations

import math
from typing import Any

import jsonschema
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
from matrx_graph import knobs
from matrx_graph.nodes.data.spread_rank import SpreadRankInput, SpreadRankOutput

from tests._fixtures import make_app_context

#: The knob rows as seeded live (feature workflow.spread_rank).
ROWS: dict[str, Any] = {
    "min_homes": 2,
    "min_homes_share": 0,
    "min_homes_floor": 1,
    "filler_home_share": 0.5,
    "filler_cap_min_homes": 5,
    "backed_share": 0.5,
    "backed_home_share": 0.01,
    "longer_phrase_cover": 0.8,
    "fold_variants": True,
    "variant_min_homes": 2,
    "top_n": 500,
}


@pytest.fixture(autouse=True)
def _rows(monkeypatch: pytest.MonkeyPatch) -> dict[str, Any]:
    rows = dict(ROWS)

    async def _values(feature: str) -> dict[str, Any] | None:
        return rows if feature == knobs.SPREAD_RANK_FEATURE else None

    monkeypatch.setattr(knobs, "_feature_values", _values)
    return rows


def _registry() -> NodeRegistry:
    reg = NodeRegistry()
    register_builtin_nodes(reg)
    return reg


async def _run(items: list[Any], config: dict[str, Any] | None = None, *, ok: bool = True) -> Any:
    registry = _registry()
    inputs = {"items": items}
    jsonschema.validate(
        inputs | {"__kind": "spread_rank_request"}, SpreadRankInput.model_json_schema()
    )
    defn = Definition.model_validate(
        {
            "nodes": [
                {
                    "id": "n",
                    "type": "data.spread_rank",
                    "position": {"x": 0, "y": 0},
                    "data": {"config": config or {}, "inputs": inputs},
                }
            ],
            "edges": [],
        }
    )
    graph = compile_graph(defn, registry=registry)
    result = await Scheduler(
        graph, MemoryCheckpointer(), make_app_context(), registry=registry
    ).run(run_id="t-spread", inputs={})
    if not ok:
        assert result.status is not RunStatus.COMPLETED
        return result
    assert result.status is RunStatus.COMPLETED, result.error
    out = result.last_outputs["n"]
    payload = out.model_dump(mode="json", by_alias=True) if hasattr(out, "model_dump") else out
    jsonschema.validate(payload, SpreadRankOutput.model_json_schema())
    assert payload.get("__kind", "spread_ranking") == "spread_ranking"
    return payload


def _by_key(out: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {t["key"]: t for t in out["terms"]}


def test_registered_as_a_pure_kind_typed_step() -> None:
    spec = _registry().get("data.spread_rank").spec
    assert spec.determinism.value == "pure"
    assert spec.input_kind == "spread_rank_request" and spec.output_kind == "spread_ranking"
    assert spec.display_name == "Rank by Spread"


# ── caller 1: knowledge buckets ─────────────────────────────────────────────────────────────


def _notes() -> list[dict[str, Any]]:
    """Four notes and two chats over three weeks. "Kitchen remodel" spreads across both kinds and
    three weeks; "Acme" is backed (an entity pass named it) in every home; "next step" sits in
    every one of six homes — filler past the cap (max(0.5 x 6, 5) = 5)."""
    week = ["2026-10-05", "2026-10-12", "2026-10-19"]
    rows = [
        (
            "n1",
            "notes",
            week[0],
            ["Kitchen remodel", "next step", {"term": "Acme", "backed": True}],
        ),
        ("n2", "notes", week[1], ["kitchen remodel", "next step"]),
        ("n2", "notes", week[1], ["Kitchen Remodel", "next step"]),  # same home twice: counts once
        ("n3", "notes", week[2], ["next step", {"term": "Acme", "backed": True}]),
        ("n4", "notes", week[2], ["next step", "tile samples"]),
        (
            "c1",
            "chats",
            week[0],
            ["kitchen-remodel", "next step", {"term": "ACME", "backed": True}],
        ),
        ("c2", "chats", week[1], ["next step", "tile samples"]),
    ]
    return [{"home": h, "kind": k, "date": d, "terms": t} for h, k, d, t in rows]


async def test_knowledge_buckets_rank_by_spread_with_a_filler_cap() -> None:
    out = await _run(_notes())
    terms = _by_key(out)
    assert out["home_count"] == 6 and out["item_count"] == 7 and out["dated"] is True
    assert "next step" not in terms and out["dropped"]["filler_cap"] == 1
    remodel = terms["kitchen remodel"]
    assert (
        remodel["homes"] == 3
        and remodel["by_kind"] == {"chats": 1, "notes": 2}
        and remodel["weeks"] == 2
    )
    assert remodel["score"] == round(0.5 * (math.log(3) + math.log(2)) * math.log(3), 4)
    assert remodel["term"] in {
        "Kitchen remodel",
        "kitchen remodel",
        "Kitchen Remodel",
        "kitchen-remodel",
    }
    acme = terms["acme"]
    assert acme["backed_share"] == 1.0 and acme["homes"] == 3 and acme["weeks"] == 2
    assert acme["score"] == round(1.5 * (math.log(3) + math.log(2)) * math.log(3), 4)
    assert [t["key"] for t in out["terms"]][:2] == ["acme", "kitchen remodel"]
    assert terms["tile samples"]["homes"] == 2 and terms["tile samples"]["aliases"] == []
    assert out["settings_from"]["filler_home_share"] == "knob"


async def test_a_backed_term_escapes_the_filler_cap() -> None:
    items = [
        {
            "home": f"h{i}",
            "kind": "notes",
            "date": "2026-10-05",
            "terms": [{"term": "Acme", "backed": True}],
        }
        for i in range(8)
    ]
    out = await _run(items, {"filler_cap_min_homes": 0})
    assert _by_key(out)["acme"]["homes"] == 8 and out["dropped"]["filler_cap"] == 0
    unbacked = [{**it, "terms": ["Acme"]} for it in items]
    out = await _run(unbacked, {"filler_cap_min_homes": 0})
    assert out["terms"] == [] and out["dropped"]["filler_cap"] == 1


async def test_the_knob_row_governs_and_the_step_setting_wins(_rows: dict[str, Any]) -> None:
    items = _notes()
    _rows["min_homes"] = 4
    out = await _run(items)
    assert out["settings"]["min_homes"] == 4 and out["settings_from"]["min_homes"] == "knob"
    assert "kitchen remodel" not in _by_key(out)  # 3 homes < 4: the row decided
    out = await _run(items, {"min_homes": 2})
    assert out["settings_from"]["min_homes"] == "step" and "kitchen remodel" in _by_key(out)


# ── caller 2: a site's topic coverage ──────────────────────────────────────────────────────


async def test_site_pages_rank_undated_and_fold_plurals_and_phrase_variants() -> None:
    pages = [
        {"url": "/a", "terms": ["Running shoes", "sensory garden herbs"]},
        {"url": "/b", "terms": ["running shoe", "sensory garden plan"]},
        {"url": "/c", "terms": ["Running Shoes", "sensory garden herbs", "sensory garden plan"]},
        {"url": "/d", "terms": ["trail map", "sensory garden plan"]},
        {"url": "/e", "terms": ["trail map", "sensory garden herbs"]},
    ]
    out = await _run(
        pages, {"home_path": "url", "kind_path": "", "date_path": "", "filler_cap_min_homes": 10}
    )
    terms = _by_key(out)
    assert out["dated"] is False
    shoe = terms["running shoe"]  # plural spelling folded into the singular term
    assert shoe["homes"] == 3 and shoe["aliases"] == ["running shoes"] and shoe["weeks"] == 0
    assert shoe["score"] == round(0.5 * math.log(4), 4)  # undated: the weeks factor is 1
    garden = terms["sensory garden"]
    assert garden["homes"] == 5 and garden["aliases"] == [
        "sensory garden herbs",
        "sensory garden plan",
    ]
    assert "sensory garden herbs" not in terms and "sensory garden plan" not in terms
    out = await _run(
        pages,
        {
            "home_path": "url",
            "kind_path": "",
            "date_path": "",
            "filler_cap_min_homes": 10,
            "fold_variants": False,
        },
    )
    assert "sensory garden" not in _by_key(out) and "running shoes" in _by_key(out)


async def test_a_longer_phrase_replaces_a_shorter_one_it_covers() -> None:
    pages = [{"url": f"/p{i}", "terms": ["solar", "solar panel install"]} for i in range(4)]
    pages.append({"url": "/q", "terms": ["solar"]})
    cfg = {"home_path": "url", "kind_path": "", "date_path": "", "filler_cap_min_homes": 10}
    out = await _run(pages, cfg)
    assert "solar" not in _by_key(out) and out["dropped"]["longer_phrase"] == 1  # 4 >= 0.8 x 5
    out = await _run(pages, {**cfg, "longer_phrase_cover": 0.9})
    assert "solar" in _by_key(out)


# ── caller 3: news story size across outlets ──────────────────────────────────────────────


async def test_news_story_size_across_outlets_and_filler_terms() -> None:
    stories = [
        {
            "outlet": "Daily Ledger",
            "section": "business",
            "published": "2026-10-20T08:00:00Z",
            "names": ["Harbor Bridge closure", "breaking news"],
        },
        {
            "outlet": "City Wire",
            "section": "local",
            "published": "2026-10-21",
            "names": ["harbor bridge closure"],
        },
        {
            "outlet": "Metro Post",
            "section": "local",
            "published": "2026-10-28",
            "names": ["Harbor bridge closure"],
        },
        {
            "outlet": "Metro Post",
            "section": "local",
            "published": "2026-10-28",
            "names": ["breaking news"],
        },
    ]
    cfg = {
        "home_path": "outlet",
        "kind_path": "section",
        "date_path": "published",
        "terms_path": "names",
        "filler_terms": ["Breaking News"],
    }
    out = await _run(stories, cfg)
    story = _by_key(out)["harbor bridge closure"]
    assert (
        story["homes"] == 3
        and story["by_kind"] == {"business": 1, "local": 2}
        and story["weeks"] == 2
    )
    assert story["items"] == [0, 1, 2]
    assert out["dropped"]["filler_terms"] == 2 and "breaking news" not in _by_key(out)


async def test_same_input_same_ranking_and_top_n() -> None:
    a = await _run(_notes(), {"top_n": 1})
    b = await _run(_notes(), {"top_n": 1})
    assert a == b and len(a["terms"]) == 1 and a["dropped"]["past_top_n"] >= 1


@pytest.mark.parametrize(
    ("items", "code"),
    [
        ([{"kind": "notes", "terms": ["x"]}], "home_missing"),
        (
            [{"home": "h", "kind": "notes", "date": "last tuesday", "terms": ["x"]}],
            "date_unreadable",
        ),
        ([{"home": "h", "kind": "notes", "terms": "x"}], "terms_not_a_list"),
        ([{"home": "h", "kind": "notes", "terms": [7]}], "term_unreadable"),
    ],
)
async def test_unreadable_items_fail_with_a_sentence(items: list[Any], code: str) -> None:
    result = await _run(items, ok=False)
    assert code in str(result.error) or code in str(getattr(result, "errors", "")), result.error
