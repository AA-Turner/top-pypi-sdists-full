"""Score Items (``data.score``, packages/matrx-graph/matrx_graph/nodes/data/FEATURE.md § Score Items, the G2 contract).

One test per factor type, then each stage around them: aggregates (per item and over the whole list),
settings with overrides merged key by key and the source of every value, the derived normalizer (the
62.5 trap: a hand-typed divisor put 100 out of reach), combine, ``then`` factors, rounded named
outputs, the authoring refusals, and one real run through the Scheduler. The research parity proof
over real rows lives in ``research/tests/test_score_items_matches_source_scoring.py``.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import pytest
from pydantic import ValidationError

from matrx_graph import Definition, MemoryCheckpointer, NodeRegistry, RunStatus, Scheduler, compile_graph
from matrx_graph import register_builtin_nodes
from matrx_graph.errors import ExecutionError
from matrx_graph.nodes.data.score import ScoreConfig, ScoreExecutor, ScoreInput, score_items
from tests._fixtures import FakeEmitter, make_app_context


def _one(factor: dict[str, Any], item: dict[str, Any], **kw: Any) -> Any:
    """Score one item with one factor; return that factor's value."""
    config = ScoreConfig.model_validate(
        {"settings": kw.pop("settings", {}), "factors": [factor], "outputs": [{"key": factor["name"]}]}
    )
    return score_items(config, [item], **kw).items[0][factor["name"]]


# --- factor types ---------------------------------------------------------------------------------


def test_expression_reads_item_settings_inputs_and_earlier_factors_by_bare_name() -> None:
    config = ScoreConfig.model_validate(
        {
            "settings": {"boost": 0.5},
            "factors": [
                {"name": "base", "type": "expression", "of": "item['n'] * 2"},
                {"name": "lifted", "type": "expression", "of": "base * (1 + boost) + bonus"},
            ],
            "outputs": [{"key": "lifted"}],
        }
    )
    assert score_items(config, [{"n": 4}], others={"bonus": 1}).items[0]["lifted"] == 13.0


def test_curve_takes_the_first_point_at_or_above_the_value_and_the_tail_past_the_last() -> None:
    curve = {
        "name": "c", "type": "curve", "of": "item['rank']",
        "points": [{"up_to": 1, "value": 1.0}, {"up_to": 3, "value": 0.8}, {"up_to": 10, "value": "top10"}],
        "tail": 0.1,
    }
    got = [_one(curve, {"rank": r}, settings={"top10": 0.5}) for r in (1, 2, 3, 4, 10, 11)]
    assert got == [1.0, 0.8, 0.8, 0.5, 0.5, 0.1]


def test_bands_take_the_first_band_that_fits_with_open_and_closed_ends() -> None:
    bands = {
        "name": "b", "type": "bands", "of": "item['m']",
        "bands": [{"below": 1, "value": 0.2}, {"at_least": 1, "at_most": 60, "value": 1.0},
                  {"above": 60, "below": 120, "value": "'long'"}],
        "default": 0.6,
    }
    assert [_one(bands, {"m": m}) for m in (0.5, 1, 60, 61, 120)] == [0.2, 1.0, 1.0, "long", 0.6]


def test_clamp_holds_the_value_between_low_and_high_given_as_settings() -> None:
    clamp = {"name": "c", "type": "clamp", "of": "item['x']", "low": "lo", "high": 1.3}
    assert [_one(clamp, {"x": x}, settings={"lo": 0.9}) for x in (0.5, 1.1, 2.0)] == [0.9, 1.1, 1.3]


def test_log_scale_saturates_and_leaves_an_unmeasured_value_empty() -> None:
    log = {"name": "r", "type": "log_scale", "of": "get(item, 'views')", "saturates_at": 6.0}
    assert _one(log, {"views": 999}) == pytest.approx(0.5)
    assert _one(log, {"views": 10**9}) == 1.0
    assert _one(log, {"views": None}) is None
    assert _one(log, {"views": -5}) is None


def test_half_life_halves_per_half_life_of_age_and_never_rises_past_one() -> None:
    hl = {"name": "f", "type": "half_life", "of": "item['at']", "half_life": 3.0, "unit": "years"}
    now = "2026-01-01T00:00:00+00:00"
    assert _one(hl, {"at": "2023-01-01T06:00:00Z"}, now=now) == pytest.approx(0.5)
    assert _one(hl, {"at": "2027-01-01T00:00:00"}, now=now) == 1.0  # a future time is age 0
    assert _one(hl, {"at": "not a time"}, now=now) is None
    assert _one({**hl, "unit": "days", "half_life": 1}, {"at": "2025-12-31T00:00:00Z"}, now=now) == 0.5


def test_lookup_reads_the_table_by_the_value_else_the_default() -> None:
    lookup = {"name": "t", "type": "lookup", "of": "item['tier']", "table": {"gov": 1.3, "blog": "low"},
              "default": 1.0}
    assert [_one(lookup, {"tier": t}, settings={"low": 0.8}) for t in ("gov", "blog", "x")] == [1.3, 0.8, 1.0]


def test_only_when_gates_a_factor_and_missing_fills_an_empty_value() -> None:
    gated = {"name": "g", "type": "clamp", "of": "item['x'] / item['n']", "low": 0, "high": 1,
             "only_when": "item['n'] > 0", "if_not": None}
    assert _one(gated, {"x": 1, "n": 0}) is None
    assert _one({"name": "m", "type": "curve", "of": "get(item, 'r')", "points": [{"up_to": 1, "value": 1}],
                 "missing": 0.25}, {}) == 0.25


# --- aggregates -----------------------------------------------------------------------------------


def test_aggregates_per_item_with_each_factors_and_every_op() -> None:
    config = ScoreConfig.model_validate(
        {
            "aggregates": [{
                "over": "item['links']", "as": "link",
                "each": [{"name": "s", "type": "curve", "of": "link['rank']",
                          "points": [{"up_to": 1, "value": 1.0}, {"up_to": 5, "value": 0.5}], "tail": 0.0}],
                "values": [
                    {"name": "wmean", "op": "weighted_mean", "of": "s", "weight": "link['w']", "empty": 0},
                    {"name": "avg", "op": "mean", "of": "link['rank']", "empty": 0},
                    {"name": "best", "op": "max", "of": "s", "empty": 0},
                    {"name": "low", "op": "min", "of": "link['rank']", "empty": 0},
                    {"name": "total", "op": "sum", "of": "link['w']", "empty": 0},
                    {"name": "n", "op": "count"},
                ],
            }],
            "outputs": [{"key": k} for k in ("wmean", "avg", "best", "low", "total", "n")],
        }
    )
    links = [{"rank": 1, "w": 3}, {"rank": 4, "w": 1}, {"rank": None, "w": 1}]
    a, empty = score_items(config, [{"links": links}, {"links": []}]).items
    # rank None: the per-element curve is empty (no `missing`), so it is skipped by weighted_mean/max.
    assert (a["wmean"], a["avg"], a["best"], a["low"], a["total"], a["n"]) == (3.5 / 4, 2.5, 1.0, 1, 5, 3)
    assert (empty["wmean"], empty["n"]) == (0, 0)


def test_an_aggregate_over_the_whole_list_is_read_by_every_item() -> None:
    config = ScoreConfig.model_validate(
        {
            "aggregates": [{"over": "items", "as": "row", "scope": "all",
                            "values": [{"name": "best", "op": "max", "of": "get(row, 'v')"}]}],
            "factors": [{"name": "rel", "type": "expression", "of": "get(item, 'v', 0) / best"}],
            "outputs": [{"key": "rel"}],
        }
    )
    assert [i["rel"] for i in score_items(config, [{"v": 5}, {"v": 10}, {"v": None}]).items] == [0.5, 1.0, 0.0]


# --- settings and overrides -----------------------------------------------------------------------


def test_overrides_merge_key_by_key_and_every_value_records_its_source() -> None:
    config = ScoreConfig.model_validate(
        {
            "settings": {"w": 0.25, "floor": 35, "locked_one": 1.2, "label": "x"},
            "locked": ["locked_one"],
            "overrides_section": "post_read",
            "factors": [{"name": "s", "type": "expression", "of": "item['x'] * w + floor"}],
            "outputs": [{"key": "s"}],
        }
    )
    out = score_items(
        config,
        [{"x": 100}],
        overrides={"post_read": {"w": 0.5, "locked_one": 2.0, "label": 3, "nope": 1, "floor": True}, "pre_read": {"w": 9}},
        overrides_source="intent:news_monitoring",
    )
    assert out.items[0]["s"] == 85.0
    eff = {k: (v.value, v.default, v.source) for k, v in out.effective_settings.items()}
    assert eff == {
        "w": (0.5, 0.25, "intent:news_monitoring"),
        "floor": (35, 35, "default"),
        "locked_one": (1.2, 1.2, "default"),
        "label": ("x", "x", "default"),
    }
    assert {(i.key, i.reason) for i in out.ignored_overrides} == {
        ("locked_one", "locked on this step"),
        ("label", "not a str"),
        ("nope", "not a setting of this step"),
        ("floor", "not a int"),
    }


# --- combine, normalize, then, outputs ------------------------------------------------------------


def _scale(settings: dict[str, Any]) -> ScoreConfig:
    return ScoreConfig.model_validate(
        {
            "settings": settings,
            "factors": [
                {"name": "rank", "type": "curve", "of": "item['rank']", "points": [{"up_to": 1, "value": 1.0}], "tail": 0.5},
                {"name": "authority", "type": "clamp", "of": "1 + boost * item['a'] / 100", "low": 0.9, "high": "cap",
                 "max": "max(0.9, min(cap, 1 + boost))"},
            ],
            "combine": {"op": "product", "of": ["rank", "authority"]},
            "normalize": {"to": 100},
            "outputs": [{"key": "score", "round": 2}, {"key": "combined", "round": 4}],
        }
    )


def test_normalize_is_derived_from_the_declared_maxima_so_the_best_item_scores_exactly_100() -> None:
    # The 62.5 trap: a divisor typed as a number goes stale when a setting moves, and 100 is out of
    # reach. Here it is the product of each factor's declared maximum (expressions over the settings),
    # so raising the cap without the boost, or the boost without the cap, still lets the best reach 100.
    for settings in ({"boost": 0.3, "cap": 1.3}, {"boost": 0.3, "cap": 2.0}, {"boost": 0.6, "cap": 1.3}):
        out = score_items(_scale(settings), [{"rank": 1, "a": 100}, {"rank": 7, "a": 0}])
        assert out.items[0]["score"] == 100.0, settings
        assert out.items[1]["score"] < 100.0
    out = score_items(_scale({"boost": 0.3, "cap": 1.3}), [{"rank": 1, "a": 100}])
    assert out.normalizer is not None and out.normalizer.combined_max == 1.3


def test_a_curve_and_a_clamp_derive_their_own_maximum_when_none_is_declared() -> None:
    config = ScoreConfig.model_validate(
        {
            "factors": [
                {"name": "r", "type": "curve", "of": "item['r']", "points": [{"up_to": 1, "value": 0.8}], "tail": 0.1},
                {"name": "c", "type": "clamp", "of": "item['c']", "low": 0, "high": 0.5},
            ],
            "combine": {"op": "product", "of": ["r", "c"]},
            "normalize": {"to": 100},
            "outputs": [{"key": "score"}],
        }
    )
    out = score_items(config, [{"r": 1, "c": 9}])
    assert out.normalizer is not None and out.normalizer.combined_max == 0.4
    assert out.items[0]["score"] == 100.0


def test_weighted_sum_fills_an_empty_factor_with_missing_and_normalizes_by_the_weights() -> None:
    config = ScoreConfig.model_validate(
        {
            "settings": {"neutral": 0.5},
            "factors": [
                {"name": "a", "type": "clamp", "of": "item['a']", "low": 0, "high": 1},
                {"name": "b", "type": "log_scale", "of": "get(item, 'b')", "saturates_at": 6},
                {"name": "penalty", "type": "clamp", "of": "item['p']", "low": 0, "high": 1},
            ],
            "combine": {"op": "weighted_sum", "of": ["a", "b", "penalty"],
                        "weights": {"a": 0.6, "b": 0.4, "penalty": -0.2}, "missing": "neutral"},
            "normalize": {"to": 100},
            "outputs": [{"key": "score", "round": 0}, {"key": "combined", "round": 4}],
        }
    )
    out = score_items(config, [{"a": 1, "p": 0}, {"a": 0.5, "p": 1}])
    assert out.normalizer is not None and out.normalizer.combined_max == pytest.approx(1.0)
    assert [i["combined"] for i in out.items] == [0.8, 0.3]
    assert [i["score"] for i in out.items] == [80, 30]


def test_then_factors_read_the_score_and_outputs_are_named_rounded_and_written_under_write_as() -> None:
    config = ScoreConfig.model_validate(
        {
            "settings": {"cite": 80},
            "factors": [{"name": "q", "type": "expression", "of": "item['q']", "max": 100}],
            "combine": {"op": "expression", "expression": "q * 0.85", "max": 85},
            "normalize": {"to": 100},
            "then": [{"name": "use", "type": "bands", "of": "score",
                      "bands": [{"at_least": "cite", "value": "'cite_directly'"}], "default": "'background'"}],
            "outputs": [{"key": "score", "round": 1}, {"key": "display", "value": "score", "round": 0},
                        {"key": "use"}, {"key": "score_version"}],
            "write_as": "verdict",
        }
    )
    out = score_items(config, [{"id": "a", "q": 90}, {"id": "b", "q": 33.333}], score_version="v7")
    assert out.items[0] == {"id": "a", "q": 90, "verdict": {"score": 90.0, "display": 90, "use": "cite_directly",
                                                             "score_version": "v7"}}
    assert out.items[1]["verdict"]["score"] == 33.3 and out.items[1]["verdict"]["display"] == 33


def test_without_a_given_version_the_score_version_is_a_digest_of_the_definition() -> None:
    a = score_items(_scale({"boost": 0.3, "cap": 1.3}), [{"rank": 1, "a": 1}]).score_version
    b = score_items(_scale({"boost": 0.31, "cap": 1.3}), [{"rank": 1, "a": 1}]).score_version
    assert a.startswith("config:") and a != b


def _labelled(settings: dict[str, Any], label: str, setting_label: str) -> ScoreConfig:
    raw = _scale(settings).model_dump(mode="json", by_alias=True)
    raw["factors"][0]["label"] = label
    raw["setting_labels"] = {"boost": setting_label}
    raw["locked"] = []
    return ScoreConfig.model_validate(raw)


def test_a_cosmetic_change_keeps_the_score_version_and_a_weight_change_moves_it() -> None:
    """research/FEATURE.md § A weight change marks stored scores out of date: the stamp is the scoring, not the publish. Words for people (labels) and a lock
    that changes no value keep the version, so a cosmetic publish leaves every stored score current; a weight
    change, or an intent override that actually applies, gives a new version (stored scores go scoring_changed)."""
    items = [{"rank": 1, "a": 1}]
    base = score_items(_labelled({"boost": 0.3, "cap": 1.3}, "Boost", "How much"), items).score_version
    cosmetic = score_items(_labelled({"boost": 0.3, "cap": 1.3}, "A top-rank boost", "Size of it"), items).score_version
    weight = score_items(_labelled({"boost": 0.35, "cap": 1.3}, "Boost", "How much"), items).score_version
    assert base == cosmetic
    assert weight != base
    cfg = _labelled({"boost": 0.3, "cap": 1.3}, "Boost", "How much")
    same_value = score_items(cfg, items, overrides={"boost": 0.3}, overrides_source="intent:news").score_version
    applied = score_items(cfg, items, overrides={"boost": 0.5}, overrides_source="intent:news").score_version
    not_a_setting = score_items(cfg, items, overrides={"nope": 1.0}, overrides_source="intent:news").score_version
    assert same_value == base and not_a_setting == base
    assert applied not in (base, weight)


# --- refusals -------------------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("config", "says"),
    [
        ({"factors": [{"name": "x", "type": "expression", "of": "1"}, {"name": "x", "type": "expression", "of": "2"}],
          "outputs": [{"key": "x"}]}, "give each its own name"),
        ({"factors": [{"name": "max", "type": "expression", "of": "1"}], "outputs": [{"key": "max"}]}, "taken by the language"),
        ({"factors": [{"name": "a", "type": "expression", "of": "1"}], "combine": {"op": "product", "of": ["a"]},
          "normalize": {"to": 100}, "outputs": [{"key": "score"}]}, "declare its max"),
        ({"factors": [{"name": "a", "type": "expression", "of": "x.y"}], "outputs": [{"key": "a"}]}, "Disallowed"),
        ({"factors": [{"name": "a", "type": "curve", "of": "1"}], "outputs": [{"key": "a"}]}, "needs points"),
        ({"settings": {"w": 1}, "locked": ["v"], "outputs": [{"key": "w"}]}, "are not settings"),
        ({"factors": [{"name": "a", "type": "expression", "of": "1"}],
          "combine": {"op": "weighted_sum", "of": ["a"]}, "outputs": [{"key": "a"}]}, "weights must name"),
    ],
)
def test_a_definition_that_cannot_work_is_refused_when_it_is_written(config: dict[str, Any], says: str) -> None:
    with pytest.raises(ValidationError, match=says):
        ScoreConfig.model_validate(config)


def test_an_unknown_name_fails_the_step_naming_the_factor_and_item() -> None:
    config = ScoreConfig.model_validate(
        {"factors": [{"name": "a", "type": "expression", "of": "nowhere + 1"}], "outputs": [{"key": "a"}]}
    )
    with pytest.raises(ExecutionError, match=r"item 0, factor 'a'.*reads `nowhere`"):
        score_items(config, [{}])


async def test_the_executor_reads_other_inputs_by_name() -> None:
    config = ScoreConfig.model_validate(
        {"factors": [{"name": "a", "type": "expression", "of": "item['x'] / total"}], "outputs": [{"key": "a"}]}
    )
    res = await ScoreExecutor().execute(SimpleNamespace(node_id="s"), ScoreInput(items=[{"x": 1}], total=4), config)
    assert res.status == "success" and res.result.items == [{"x": 1, "a": 0.25}]


async def test_a_real_run_through_the_scheduler_scores_the_items() -> None:
    config = _scale({"boost": 0.3, "cap": 1.3}).model_dump(mode="json", by_alias=True, exclude_none=True)
    definition = Definition.model_validate(
        {
            "nodes": [{
                "id": "score",
                "type": "data.score",
                "position": {"x": 0, "y": 0},
                "data": {"label": "Score", "config": config,
                         "input": {"items": [{"rank": 1, "a": 100}, {"rank": 3, "a": 10}],
                                   "overrides": {"boost": 0.0}, "overrides_source": "intent:x"}},
            }],
            "edges": [],
            "entry_nodes": ["score"],
        }
    )
    registry = NodeRegistry()
    register_builtin_nodes(registry)
    scheduler = Scheduler(compile_graph(definition, registry=registry), MemoryCheckpointer(),
                          make_app_context(FakeEmitter()), registry=registry)
    result = await scheduler.run(run_id="score-items")
    assert result.status is RunStatus.COMPLETED, result.error
    out = result.last_outputs["score"]
    out = out if isinstance(out, dict) else out.model_dump(by_alias=True)
    # boost 0 from the override: the best reachable is max(1.0, 0.9) = 1.0, so the #1 item scores 100.
    assert out["normalizer"]["combined_max"] == 1.0
    assert [i["score"] for i in out["items"]] == [100.0, 50.0]
    assert out["effective_settings"]["boost"]["source"] == "intent:x"
