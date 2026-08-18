"""
Tests for model-major fold-task ordering (geocif/geocif_runner.py).

gather_inputs nests model innermost, so same-fold tasks for different models
land next to each other and the pool starts them simultaneously — every one
misses the feature-selection cache and recomputes the same selection.
Ordering model-major is what makes the cache pay off.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from geocif.geocif_runner import order_inputs_model_major


def gather_like(years, models, crop="maize", country="usa"):
    """Mimic gather_inputs' nesting: season outer, model inner."""
    return [["proj", country, crop, year, model] for year in years for model in models]


def models_of(inputs):
    return [item[4] for item in inputs]


def years_of(inputs):
    return [item[3] for item in inputs]


def test_models_are_grouped_together():
    ordered = order_inputs_model_major(gather_like([2005, 2006, 2007], ["catboost", "cubist"]))
    assert models_of(ordered) == ["catboost"] * 3 + ["cubist"] * 3


def test_year_order_is_preserved_within_a_model():
    ordered = order_inputs_model_major(gather_like([2005, 2006, 2007], ["catboost", "cubist"]))
    assert years_of(ordered[:3]) == [2005, 2006, 2007]
    assert years_of(ordered[3:]) == [2005, 2006, 2007]


def test_configured_model_order_is_kept():
    """Not alphabetical — the user's [models] order still leads."""
    ordered = order_inputs_model_major(gather_like([2005, 2006], ["cubist", "catboost"]))
    assert models_of(ordered) == ["cubist", "cubist", "catboost", "catboost"]


def test_no_task_is_lost_or_duplicated():
    original = gather_like(range(2005, 2027), ["catboost", "cubist", "tabpfn"])
    ordered = order_inputs_model_major(original)
    assert len(ordered) == len(original)
    assert sorted(map(str, ordered)) == sorted(map(str, original))


def test_same_fold_tasks_are_far_apart():
    """The point of the reorder: a fold's models must not be dispatched together."""
    years = list(range(2005, 2027))
    ordered = order_inputs_model_major(gather_like(years, ["catboost", "cubist"]))
    positions = [i for i, item in enumerate(ordered) if item[3] == 2005]
    assert positions[1] - positions[0] == len(years)


def test_multiple_crops_are_handled():
    inputs = [["proj", "usa", crop, year, model]
              for year in (2005, 2006) for crop in ("maize", "soybean")
              for model in ("catboost", "cubist")]
    ordered = order_inputs_model_major(inputs)
    assert models_of(ordered) == ["catboost"] * 4 + ["cubist"] * 4


def test_pooled_input_shape_with_country_list():
    """gather_pooled_inputs puts a list at index 1; model is still index 4."""
    inputs = [["proj", ["usa", "canada"], "maize", year, model]
              for year in (2005, 2006) for model in ("catboost", "cubist")]
    ordered = order_inputs_model_major(inputs)
    assert models_of(ordered) == ["catboost", "catboost", "cubist", "cubist"]


def test_single_model_is_unchanged():
    original = gather_like([2005, 2006, 2007], ["cubist"])
    assert order_inputs_model_major(original) == original


def test_empty_input_is_unchanged():
    assert order_inputs_model_major([]) == []


def test_unexpected_shape_is_returned_untouched():
    """Ordering is an optimisation — a odd shape must never raise."""
    weird = [["proj", "usa", "maize", 2005]]  # no model field
    assert order_inputs_model_major(weird) == weird

    non_string_model = [["proj", "usa", "maize", 2005, 7]]
    assert order_inputs_model_major(non_string_model) == non_string_model
