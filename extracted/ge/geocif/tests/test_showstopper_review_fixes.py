"""
Regressions for defects found by the 0.4.920-0.4.928 show-stopper review.

All four were in code shipped the same day, and none were caught by that code's
own unit tests — they only showed up when the review traced the ACTUAL config
that was about to run.
"""

import logging
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from geocif.cid import indices
from geocif.ml import fs_cache
from geocif.viz.plot import effective_annotate_regions

PLOT_PY = Path(__file__).resolve().parents[1] / "geocif" / "viz" / "plot.py"
TRAINERS_PY = Path(__file__).resolve().parents[1] / "geocif" / "ml" / "trainers.py"


# ---- 1. annotate_values bypassed the county-scale label suppression --------


def test_annotate_values_does_not_bypass_suppression():
    """diagnostics hardcodes annotate_values=True, so `or annotate_values`
    re-enabled labels on every county map.

    The invariant: ``annotate_values`` must be folded INTO the suppression
    decision (``effective_annotate_regions(annotate_regions or annotate_values,
    ...)``), never OR-ed with its result. Whitespace is normalised so the test
    guards that invariant rather than one particular line-wrapping — an earlier
    literal-string version broke merely because the call gained a ``gdf=``
    argument and wrapped onto two lines.
    """
    source = PLOT_PY.read_text(encoding="utf-8", errors="replace")
    flat = " ".join(source.split())
    # the broken form: suppression computed first, then bypassed by values
    assert "effective_annotate_regions(annotate_regions, len(gdf)) or annotate_values" not in flat
    assert "effective_annotate_regions(annotate_regions, len(df_comb)) or annotate_values" not in flat
    # the correct form: both flags feed the decision. Once per backend path.
    assert flat.count("effective_annotate_regions( annotate_regions or annotate_values") \
        + flat.count("effective_annotate_regions(annotate_regions or annotate_values") == 2


def test_county_scale_suppresses_even_with_values():
    """annotate_regions OR annotate_values, at county scale -> no labels."""
    assert effective_annotate_regions(True, 1004) is False
    assert effective_annotate_regions(True or True, 1004) is False


def test_admin1_metric_maps_keep_name_and_value():
    """The parent choropleths (state name + error value) must be untouched."""
    assert effective_annotate_regions(True, 11) is True
    assert effective_annotate_regions(True, 50) is True


def test_matplotlib_path_resolves_both_flags_together():
    source = PLOT_PY.read_text(encoding="utf-8", errors="replace")
    assert "annotate_values and _keep_labels" in source
    assert "annotate_regions and _keep_labels" in source


# ---- 2. thread budget never reached the CatBoost that actually trains ------


def test_optimize_false_catboost_gets_the_thread_budget():
    """usa_admin2 sets optimize=False, so auto_train's else-branch is the one
    production takes — the two patched sites were both in optimized_model()."""
    source = TRAINERS_PY.read_text(encoding="utf-8", errors="replace")
    marker = source.index('if model_name in ("catboost", "catboost_quantile"):')
    preceding = source[max(0, marker - 600):marker]
    assert 'hyperparams.setdefault("thread_count", ml_threads.thread_count(-1))' in preceding


def test_thread_count_default_is_catboost_all_cores_sentinel(monkeypatch):
    monkeypatch.delenv(fs_cache.os.environ and "GEOCIF_THREADS_PER_WORKER", raising=False)
    from geocif.ml import threads as ml_threads
    assert ml_threads.thread_count(-1) == -1
    monkeypatch.setenv("GEOCIF_THREADS_PER_WORKER", "5")
    assert ml_threads.thread_count(-1) == 5


# ---- 3. ndarray truthiness crash in cached_select --------------------------


def test_selector_returning_ndarray_does_not_crash(tmp_path):
    """`compute_fn() or []` raises ValueError on a numpy array."""
    X = pd.DataFrame({"a": [1.0, 2.0, 3.0], "b": [4.0, 5.0, 6.0]})
    y = pd.Series([1.0, 2.0, 3.0])

    feats, hit = fs_cache.cached_select(
        X, y, "gOMP_medium", tmp_path, lambda: np.array(["a", "b"])
    )
    assert feats == ["a", "b"] and hit is False


def test_selector_returning_none_still_yields_empty_list(tmp_path):
    X = pd.DataFrame({"a": [1.0, 2.0]})
    y = pd.Series([1.0, 2.0])
    feats, _ = fs_cache.cached_select(X, y, "lasso", tmp_path, lambda: None)
    assert feats == []


def test_ndarray_result_round_trips_through_the_cache(tmp_path):
    X = pd.DataFrame({"a": [1.0, 2.0, 3.0], "b": [4.0, 5.0, 6.0]})
    y = pd.Series([1.0, 2.0, 3.0])
    fs_cache.cached_select(X, y, "gOMP_medium", tmp_path, lambda: np.array(["a"]))
    feats, hit = fs_cache.cached_select(
        X, y, "gOMP_medium", tmp_path, lambda: pytest.fail("should have hit cache")
    )
    assert hit is True and feats == ["a"]


# ---- 4. region filter silently no-opped with no region column --------------


def test_missing_region_column_warns_instead_of_silently_passing(tmp_path, caplog):
    """A filter that quietly returns everything is how the 1,759-vs-1,004
    county bug stayed hidden for a whole run."""
    path = tmp_path / "kenya_maize_s1.csv"
    pd.DataFrame({"year": [2020, 2021], "chirps": [1.0, 2.0]}).to_csv(path, index=False)

    with caplog.at_level(logging.WARNING):
        df = indices._read_input_csv(path, keep_regions={"illinois"})

    assert len(df) == 2, "unfiltered fallback should still return the data"
    assert any("unfiltered" in r.message.lower() for r in caplog.records)


def test_no_warning_when_no_filter_requested(tmp_path, caplog):
    path = tmp_path / "kenya_maize_s1.csv"
    pd.DataFrame({"year": [2020], "chirps": [1.0]}).to_csv(path, index=False)
    with caplog.at_level(logging.WARNING):
        indices._read_input_csv(path)
    assert not [r for r in caplog.records if "unfiltered" in r.message.lower()]
