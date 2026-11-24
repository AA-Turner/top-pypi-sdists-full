"""Score Items' clamp keeps the value's own kind of number at a bound.

Research's keyword coverage is matched / total clamped to [0, 1]. At exactly 1.0 (or above) Python's
``min(1, 1.0)`` answers the INTEGER bound, so the workflow stored ``keyword_coverage_score: 1`` where the
code path stores ``1.0`` (PBW pick parity, 2026-11-09).
"""

from __future__ import annotations

from matrx_graph.nodes.data.score import ScoreConfig, score_items


def _clamped(value_of: str, item: dict) -> object:
    config = ScoreConfig.model_validate({
        "settings": {},
        "factors": [{"name": "c", "type": "clamp", "of": value_of, "low": 0, "high": 1}],
        "outputs": [{"key": "c", "value": "c"}],
    })
    return score_items(config, [item]).items[0]["c"]


def test_a_float_clamped_at_an_integer_bound_stays_a_float() -> None:
    got = [_clamped("item['m'] / item['t']", {"m": m, "t": 2.0}) for m in (2.0, 3.0, -1.0, 1.0)]
    assert got == [1.0, 1.0, 0.0, 0.5]
    assert [type(v) for v in got] == [float, float, float, float], got


def test_an_integer_clamped_stays_an_integer() -> None:
    assert type(_clamped("item['m']", {"m": 5})) is int


def _scored(factor: dict, output: dict, item: dict, settings: dict | None = None) -> object:
    config = ScoreConfig.model_validate({"settings": settings or {}, "factors": [factor], "outputs": [output]})
    return score_items(config, [item]).items[0][output["key"]]


def test_an_output_rounded_to_digits_is_a_decimal_number() -> None:
    # matched_keyword_weight: a sum of whole weights, rounded to 4 digits; the code stores 2.0, not 2.
    f = {"name": "w", "type": "expression", "of": "item['a'] + item['b']"}
    got = _scored(f, {"key": "w", "round": 4}, {"a": 1, "b": 1})
    assert got == 2.0 and type(got) is float
    whole = _scored(f, {"key": "w", "round": 0}, {"a": 1, "b": 1})
    assert whole == 2 and type(whole) is int  # 0 digits stays a whole number


def test_bands_mixing_whole_and_decimal_values_answer_decimals() -> None:
    # top_rank_boost: bands worth 1.08 / 1.04 and a default worth 1 — the code's default is 1.0.
    f = {"name": "boost", "type": "bands", "of": "item['rank']", "default": "dflt",
         "bands": [{"at_least": 1, "at_most": 1, "value": 1.08}, {"at_least": 2, "at_most": 3, "value": 1.04}]}
    got = [_scored(f, {"key": "boost"}, {"rank": r}, {"dflt": 1}) for r in (1, 2, 9)]
    assert got == [1.08, 1.04, 1.0] and [type(v) for v in got] == [float, float, float], got
    only_whole = {**f, "bands": [{"at_least": 1, "at_most": 1, "value": 3}]}
    assert type(_scored(only_whole, {"key": "boost"}, {"rank": 9}, {"dflt": 1})) is int
