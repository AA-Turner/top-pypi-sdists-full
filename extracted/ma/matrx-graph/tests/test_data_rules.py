"""``data.rules`` — an ordered decision table, run through the real scheduler.

Every test runs a compiled graph, so the config is validated the way a saved
workflow's is and the output is what a downstream edge would receive. The last
three are the three unrelated users from SMART-ADD-IDENTIFY.md § "The three new
generic steps" (Rule 3): a web-result certainty table (list mode), a news
relevance floor (single mode + coalesce + default), and an agent-proof decision
(all_match, routed by conditional edges on ``label``).
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
from matrx_graph.nodes._sandbox import safe_eval

from tests._fixtures import make_app_context


def _registry() -> NodeRegistry:
    reg = NodeRegistry()
    register_builtin_nodes(reg)
    return reg


async def _run(inputs: dict[str, Any], config: dict[str, Any], *, ok: bool = True):
    registry = _registry()
    defn = Definition.model_validate(
        {
            "nodes": [
                {
                    "id": "n",
                    "type": "data.rules",
                    "position": {"x": 0, "y": 0},
                    "data": {"config": config, "inputs": inputs},
                }
            ],
            "edges": [],
        }
    )
    graph = compile_graph(defn, registry=registry)
    scheduler = Scheduler(graph, MemoryCheckpointer(), make_app_context(), registry=registry)
    result = await scheduler.run(run_id="t-rules", inputs=inputs)
    if ok:
        assert result.status is RunStatus.COMPLETED, result.error
        return result.last_outputs["n"]
    assert result.status is not RunStatus.COMPLETED
    return result


_TIERS = [
    {"when": "inputs['n'] >= 100", "then": {"label": "big", "score": 0.9}},
    {"when": "inputs['n'] >= 10", "then": {"label": "medium", "score": 0.5}},
    {"when": "inputs['n'] >= 0", "then": {"label": "small", "score": 0.1}},
]


async def test_first_match_takes_the_first_true_row_in_order():
    out = await _run({"n": 150}, {"rules": _TIERS})
    # Rows 1 and 2 are ALSO true; order decides, so only row 0 is reported.
    assert out["label"] == "big"
    assert out["score"] == 0.9
    assert out["matched"] is True
    assert out["matched_rules"] == [0]
    assert out["then"] == {"label": "big", "reason": None, "score": 0.9}

    out = await _run({"n": 42}, {"rules": _TIERS})
    assert (out["label"], out["matched_rules"]) == ("medium", [1])


async def test_all_match_returns_every_true_row_with_the_first_as_headline():
    out = await _run({"n": 150}, {"rules": _TIERS, "mode": "all_match"})
    assert out["matched_rules"] == [0, 1, 2]
    assert [hit["then"]["label"] for hit in out["matches"]] == ["big", "medium", "small"]
    assert out["label"] == "big"


async def test_default_answers_when_nothing_matches():
    out = await _run(
        {"n": -5},
        {"rules": _TIERS, "default": {"label": "invalid", "reason": "n is {n}", "score": 0}},
    )
    assert out["label"] == "invalid"
    assert out["reason"] == "n is -5"
    assert out["matched"] is False
    assert out["matched_rules"] == []


async def test_no_match_without_default_is_a_null_label_never_an_exception():
    out = await _run({"n": -5}, {"rules": _TIERS})
    assert out["label"] is None
    assert out["matched"] is False
    assert out["then"] is None
    assert out["matches"] == []


async def test_reason_interpolates_the_values_the_predicate_saw():
    out = await _run(
        {"name": "Acme", "hosts": ["acme.com"]},
        {
            "rules": [
                {
                    "when": "len(inputs['hosts']) > 0",
                    "then": {"label": "has_site", "reason": "{name} owns {hosts.0}; missing='{nope}'"},
                }
            ]
        },
    )
    assert out["reason"] == "Acme owns acme.com; missing=''"


async def test_extra_then_fields_are_carried_through():
    out = await _run(
        {"n": 1},
        {"rules": [{"when": "True", "then": {"label": "x", "fields": {"path": "deep", "review": True}}}]},
    )
    assert out["then"]["path"] == "deep"
    assert out["then"]["review"] is True


def test_fields_may_not_shadow_the_named_answer():
    from matrx_graph.nodes.data.rules import RuleThen

    with pytest.raises(ValidationError, match="may not repeat"):
        RuleThen.model_validate({"label": "x", "fields": {"label": "y"}})


async def test_a_predicate_that_cannot_evaluate_names_its_rule_index():
    result = await _run(
        {"n": 5},
        {
            "rules": [
                {"when": "inputs['n'] > 100", "then": {"label": "a"}},
                {"when": "inputs['missing'] > 1", "then": {"label": "b"}},
            ]
        },
        ok=False,
    )
    assert "rule 1" in (result.error or "")
    assert "'missing'" in (result.error or "")


def test_an_illegal_predicate_is_refused_at_authoring_with_its_rule_index():
    from matrx_graph.nodes.data.rules import RulesConfig

    with pytest.raises(ValidationError) as exc:
        RulesConfig.model_validate(
            {
                "rules": [
                    {"when": "True", "then": {"label": "a"}},
                    {"when": "inputs.keys()", "then": {"label": "b"}},
                ]
            }
        )
    assert "rule 1" in str(exc.value)
    assert "Disallowed" in str(exc.value)


async def test_list_mode_decides_each_item_and_counts_labels():
    out = await _run(
        {"results": [5, 50, 500, -1]},
        {
            "items_path": "results",
            "rules": [
                {"when": "inputs['item'] >= 100", "then": {"label": "big", "reason": "#{index}: {item}"}},
                {"when": "inputs['item'] >= 0", "then": {"label": "small"}},
            ],
        },
    )
    assert [i["label"] for i in out["items"]] == ["small", "small", "big", None]
    assert [i["item"] for i in out["items"]] == [5, 50, 500, -1]
    assert out["items"][2]["reason"] == "#2: 500"
    assert out["counts"] == {"small": 2, "big": 1}
    assert out["unlabeled"] == 1
    assert out["matched"] is True
    assert out["matched_rules"] == [0, 1]


async def test_list_mode_error_names_rule_and_item():
    result = await _run(
        {"results": [{"a": 1}, {"b": 2}]},
        {"items_path": "results", "rules": [{"when": "inputs['item']['a'] > 0", "then": {"label": "x"}}]},
        ok=False,
    )
    assert "rule 0" in (result.error or "")
    assert "item 1 of 2" in (result.error or "")


async def test_list_mode_refuses_a_path_that_is_not_a_list():
    result = await _run(
        {"results": {"a": 1}},
        {"items_path": "results", "rules": [{"when": "True", "then": {"label": "x"}}]},
        ok=False,
    )
    assert "not a list" in (result.error or "")


def test_coalesce_returns_the_first_non_empty_value():
    assert safe_eval("coalesce(inputs['a'], inputs['b'], 'z')", {"a": None, "b": ""}) == "z"
    assert safe_eval("coalesce(inputs['a'], [], inputs['b'])", {"a": "", "b": 0}) == 0
    assert safe_eval("coalesce(inputs['a'], inputs['b'])", {"a": None, "b": []}) == []


@pytest.mark.parametrize(("blank", "fallback"), [("   ", "Riverbend Dental Care"), ("\n\t", "Marigold Bakery")])
def test_coalesce_skips_a_whitespace_only_string(blank: str, fallback: str):
    # Break caught: a page title of "  " won over the real name ("the name, else the title, else the url").
    assert safe_eval("coalesce(inputs['title'], inputs['name'])", {"title": blank, "name": fallback}) == fallback


# ── The three unrelated users (Rule 3) ────────────────────────────────────────


async def test_user_1_web_result_certainty_for_every_search_result():
    """Identify's web certainty: each search hit gets a certainty by where it lives."""
    out = await _run(
        {
            "hosts": ["acme.com", "shop.acme.com"],
            "name": "acme",
            "results": [
                {"host": "acme.com", "title": "Acme — home"},
                {"host": "linkedin.com", "title": "Acme Inc | LinkedIn"},
                {"host": "news.example.com", "title": "Local roundup"},
            ],
        },
        {
            "items_path": "results",
            "rules": [
                {
                    "when": "inputs['item']['host'] in inputs['hosts']",
                    "then": {"label": "ours", "score": 1.0, "reason": "{item.host} is our own site"},
                },
                {
                    "when": "inputs['item']['host'] in ['linkedin.com', 'facebook.com', 'instagram.com']",
                    "then": {"label": "profile", "score": 0.7, "reason": "a profile page on {item.host}"},
                },
            ],
            "default": {"label": "mention", "score": 0.3},
        },
    )
    assert [(i["label"], i["score"]) for i in out["items"]] == [
        ("ours", 1.0),
        ("profile", 0.7),
        ("mention", 0.3),
    ]
    assert out["items"][0]["reason"] == "acme.com is our own site"
    assert out["counts"] == {"ours": 1, "profile": 1, "mention": 1}


async def test_user_2_news_relevance_floor_keeps_monitors_or_rejects():
    """News monitor coarse floors: safety and promotional floors beat the judge's score."""
    cfg = {
        "rules": [
            {"when": "inputs['unsafe']", "then": {"label": "reject", "reason": "safety floor"}},
            {"when": "inputs['promotional']", "then": {"label": "reject", "reason": "promotional"}},
            {
                "when": "coalesce(inputs['judge_score'], inputs['fallback_score'], 0) >= 0.6",
                "then": {"label": "keep", "reason": "relevant to {client}"},
            },
            {
                "when": "coalesce(inputs['judge_score'], inputs['fallback_score'], 0) >= 0.3",
                "then": {"label": "monitor"},
            },
        ],
        "default": {"label": "reject", "reason": "below every floor"},
    }
    base = {"client": "Acme", "unsafe": False, "promotional": False, "judge_score": None, "fallback_score": 0.8}
    assert (await _run(base, cfg))["label"] == "keep"
    assert (await _run(base, cfg))["reason"] == "relevant to Acme"
    assert (await _run({**base, "judge_score": 0.4}, cfg))["label"] == "monitor"
    assert (await _run({**base, "promotional": True}, cfg))["reason"] == "promotional"
    floor = await _run({**base, "fallback_score": None}, cfg)
    assert (floor["label"], floor["matched"]) == ("reject", False)


async def test_user_3_agent_proof_decision_routes_on_label():
    """Agent factory proof decision: all_match lists every reason it lost; edges route on label."""
    rules_cfg = {
        "mode": "all_match",
        "rules": [
            {"when": "not inputs['floor_met']", "then": {"label": "send_back", "reason": "missed the floor"}},
            {"when": "inputs['code_failures'] > 0", "then": {"label": "send_back", "reason": "{code_failures} code checks failed"}},
            {
                "when": "inputs['relation'] == 'costlier' and inputs['win_pct'] < inputs['min_win_pct']",
                "then": {"label": "keep_current", "reason": "costlier without enough wins"},
            },
        ],
        "default": {"label": "promote", "reason": "won the proof"},
    }
    registry = _registry()

    def defn(inputs: dict[str, Any]) -> Definition:
        return Definition.model_validate(
            {
                "nodes": [
                    {"id": "decide", "type": "data.rules", "position": {"x": 0, "y": 0},
                     "data": {"config": rules_cfg, "inputs": inputs}},
                    {"id": "promote", "type": "data.transform", "position": {"x": 200, "y": 0},
                     "data": {"config": {"expression": "'PROMOTED'"}}},
                    {"id": "send_back", "type": "data.transform", "position": {"x": 200, "y": 100},
                     "data": {"config": {"expression": "'SENT_BACK'"}}},
                ],
                "edges": [
                    {"id": "e1", "source": "decide", "target": "promote",
                     "data": {"kind": "conditional", "condition": "inputs['label'] == 'promote'"}},
                    {"id": "e2", "source": "decide", "target": "send_back",
                     "data": {"kind": "conditional", "condition": "inputs['label'] == 'send_back'"}},
                ],
            }
        )  # fmt: skip

    async def run(inputs: dict[str, Any]):
        graph = compile_graph(defn(inputs), registry=registry)
        sched = Scheduler(graph, MemoryCheckpointer(), make_app_context(), registry=registry)
        result = await sched.run(run_id="t-proof", inputs=inputs)
        assert result.status is RunStatus.COMPLETED, result.error
        return result.last_outputs

    lost = await run({"floor_met": False, "code_failures": 2, "relation": "same", "win_pct": 80, "min_win_pct": 60})
    assert lost["decide"]["label"] == "send_back"
    assert [h["then"]["reason"] for h in lost["decide"]["matches"]] == [
        "missed the floor",
        "2 code checks failed",
    ]
    assert "send_back" in lost and "promote" not in lost

    won = await run({"floor_met": True, "code_failures": 0, "relation": "same", "win_pct": 80, "min_win_pct": 60})
    assert won["decide"]["label"] == "promote"
    assert "promote" in won and "send_back" not in won


async def test_then_fields_fill_placeholders_like_reason_nested_and_missing_path_is_empty():
    out = await _run(
        {"name": "Maria Lopez", "city": "Fresno", "tags": ["a"]},
        {
            "rules": [
                {
                    "when": "True",
                    "then": {
                        "label": "city",
                        "fields": {
                            "keyword": "\"{name}\" {city}",
                            "nested": {"q": "{name}/{nope}", "list": ["{city}", 7]},
                            "flag": True,
                        },
                    },
                }
            ]
        },
    )
    assert out["then"]["keyword"] == '"Maria Lopez" Fresno'
    assert out["then"]["nested"] == {"q": "Maria Lopez/", "list": ["Fresno", 7]}
    assert out["then"]["flag"] is True


async def test_default_fields_fill_placeholders_too():
    out = await _run(
        {"name": "Dana Whitfield"},
        {
            "rules": [{"when": "False", "then": {"label": "x"}}],
            "default": {"label": "none", "fields": {"keyword": "{name} plumbing"}},
        },
    )
    assert out["then"]["keyword"] == "Dana Whitfield plumbing"
