"""
Tests for the content-addressed feature-selection cache (geocif/ml/fs_cache.py).

The cache exists because feature selection is model-independent but is
recomputed once per ML model per fold. The correctness bar is high: a wrong
hit would silently train models on the wrong feature set, so most of these
tests are about the key *missing* when it should.
"""

import json
import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from geocif.ml import fs_cache


def make_xy(seed=0, n_rows=40, n_cols=6):
    rng = np.random.default_rng(seed)
    X = pd.DataFrame(
        rng.normal(size=(n_rows, n_cols)),
        columns=[f"cid_{i}" for i in range(n_cols)],
    )
    y = pd.Series(X["cid_0"] * 2.0 + rng.normal(scale=0.1, size=n_rows), name="Yield")
    return X, y


class Counter:
    """Stand-in for an ML model's selection call; records invocations."""

    def __init__(self, features):
        self.features = list(features)
        self.calls = 0

    def __call__(self):
        self.calls += 1
        return list(self.features)


# ---------------------------------------------------------------- keying


def test_key_is_stable_across_calls():
    X, y = make_xy()
    assert fs_cache.compute_key(X, y, "gOMP_medium") == fs_cache.compute_key(X, y, "gOMP_medium")


def test_key_is_stable_for_an_equal_but_distinct_frame():
    X, y = make_xy()
    assert fs_cache.compute_key(X.copy(), y.copy(), "lasso") == fs_cache.compute_key(X, y, "lasso")


def test_key_changes_with_method():
    X, y = make_xy()
    assert fs_cache.compute_key(X, y, "gOMP_high") != fs_cache.compute_key(X, y, "gOMP_medium")


def test_key_changes_with_feature_values():
    X, y = make_xy()
    X2 = X.copy()
    X2.iloc[0, 0] += 1e-6
    assert fs_cache.compute_key(X, y, "lasso") != fs_cache.compute_key(X2, y, "lasso")


def test_key_changes_with_target_values():
    """A different fold year means a different y — must not reuse."""
    X, y = make_xy()
    y2 = y.copy()
    y2.iloc[3] += 0.5
    assert fs_cache.compute_key(X, y, "lasso") != fs_cache.compute_key(X, y2, "lasso")


def test_key_changes_with_column_names():
    """pandas' frame hash ignores column names; the cache must not."""
    X, y = make_xy()
    X2 = X.rename(columns={"cid_0": "cid_renamed"})
    assert fs_cache.compute_key(X, y, "lasso") != fs_cache.compute_key(X2, y, "lasso")


def test_key_changes_with_column_subset():
    X, y = make_xy()
    assert fs_cache.compute_key(X, y, "lasso") != fs_cache.compute_key(X.drop(columns=["cid_5"]), y, "lasso")


def test_key_changes_with_row_count():
    """Different training window (fewer years/regions) -> different key."""
    X, y = make_xy()
    assert fs_cache.compute_key(X, y, "lasso") != fs_cache.compute_key(X.iloc[:-1], y.iloc[:-1], "lasso")


def test_key_changes_with_row_order():
    X, y = make_xy()
    order = list(range(len(X)))[::-1]
    assert fs_cache.compute_key(X, y, "lasso") != fs_cache.compute_key(
        X.iloc[order].reset_index(drop=True), y.iloc[order].reset_index(drop=True), "lasso"
    )


def test_key_changes_with_extra():
    X, y = make_xy()
    assert fs_cache.compute_key(X, y, "lasso", extra={"stage": "A"}) != fs_cache.compute_key(
        X, y, "lasso", extra={"stage": "B"}
    )


def test_key_changes_when_selector_code_changes(monkeypatch):
    """A geocif upgrade that edits a selector must invalidate old entries."""
    X, y = make_xy()
    before = fs_cache.compute_key(X, y, "lasso")

    monkeypatch.setattr(fs_cache, "selector_code_fingerprint", lambda: "deadbeefdeadbeef")
    assert fs_cache.compute_key(X, y, "lasso") != before


def test_selector_code_fingerprint_is_stable_and_short():
    first = fs_cache.selector_code_fingerprint()
    assert isinstance(first, str) and len(first) == 16
    assert fs_cache.selector_code_fingerprint() == first


def test_key_accepts_numpy_target():
    X, y = make_xy()
    assert fs_cache.compute_key(X, y.to_numpy(), "lasso") is not None


def test_key_returns_none_when_unhashable():
    """Unhashable input degrades to 'run uncached', never raises."""
    X, y = make_xy()
    X_bad = X.copy()
    X_bad["obj"] = [{"a": 1}] * len(X_bad)  # dicts are unhashable for pandas
    assert fs_cache.compute_key(X_bad, y, "lasso") is None


# ------------------------------------------------------------ hit / miss


def test_second_model_reuses_first_models_selection(tmp_path):
    """The whole point: model B must not recompute model A's selection."""
    X, y = make_xy()
    model_a = Counter(["cid_0", "cid_2"])
    model_b = Counter(["cid_0", "cid_2"])

    feats_a, hit_a = fs_cache.cached_select(X, y, "gOMP_medium", tmp_path, model_a)
    feats_b, hit_b = fs_cache.cached_select(X, y, "gOMP_medium", tmp_path, model_b)

    assert (hit_a, hit_b) == (False, True)
    assert model_a.calls == 1 and model_b.calls == 0
    assert feats_a == feats_b == ["cid_0", "cid_2"]


def test_cache_survives_a_fresh_process_view(tmp_path):
    """Workers are separate processes: only on-disk state may be relied on."""
    X, y = make_xy()
    fs_cache.cached_select(X, y, "gOMP_medium", tmp_path, Counter(["cid_1"]))

    key = fs_cache.compute_key(X, y, "gOMP_medium")
    assert fs_cache.load(tmp_path, key) == ["cid_1"]


def test_different_fold_does_not_hit(tmp_path):
    X, y = make_xy()
    _, y_other = make_xy(seed=1)
    first = Counter(["cid_0"])
    second = Counter(["cid_3"])

    fs_cache.cached_select(X, y, "gOMP_medium", tmp_path, first)
    feats, hit = fs_cache.cached_select(X, y_other, "gOMP_medium", tmp_path, second)

    assert hit is False
    assert feats == ["cid_3"]


def test_empty_selection_is_cached_not_treated_as_miss(tmp_path):
    """An empty selection is a legitimate result, not a cache miss."""
    X, y = make_xy()
    first, second = Counter([]), Counter([])

    fs_cache.cached_select(X, y, "lasso", tmp_path, first)
    feats, hit = fs_cache.cached_select(X, y, "lasso", tmp_path, second)

    assert hit is True and feats == [] and second.calls == 0


def test_disabled_cache_always_computes(tmp_path):
    X, y = make_xy()
    counter = Counter(["cid_0"])

    fs_cache.cached_select(X, y, "lasso", None, counter)
    _, hit = fs_cache.cached_select(X, y, "lasso", None, counter)

    assert hit is False and counter.calls == 2
    assert list(Path(tmp_path).iterdir()) == []


def test_unhashable_input_computes_without_caching(tmp_path):
    X, y = make_xy()
    X["obj"] = [{"a": 1}] * len(X)
    counter = Counter(["cid_0"])

    feats, hit = fs_cache.cached_select(X, y, "lasso", tmp_path, counter)

    assert hit is False and feats == ["cid_0"] and counter.calls == 1


# ------------------------------------------------------- robustness


def test_corrupt_entry_recomputes(tmp_path):
    X, y = make_xy()
    fs_cache.cached_select(X, y, "lasso", tmp_path, Counter(["cid_0"]))

    key = fs_cache.compute_key(X, y, "lasso")
    path = tmp_path / key[:2] / f"{key}.json"
    path.write_text("{not json", encoding="utf-8")

    counter = Counter(["cid_4"])
    feats, hit = fs_cache.cached_select(X, y, "lasso", tmp_path, counter)
    assert hit is False and feats == ["cid_4"] and counter.calls == 1


def test_malformed_payload_recomputes(tmp_path):
    X, y = make_xy()
    key = fs_cache.compute_key(X, y, "lasso")
    path = tmp_path / key[:2] / f"{key}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"selected_features": "cid_0"}), encoding="utf-8")

    counter = Counter(["cid_0"])
    _, hit = fs_cache.cached_select(X, y, "lasso", tmp_path, counter)
    assert hit is False and counter.calls == 1


def test_entry_referencing_unknown_column_recomputes(tmp_path):
    """Defense against a hand-edited entry or a hash collision."""
    X, y = make_xy()
    key = fs_cache.compute_key(X, y, "lasso")
    fs_cache.store(tmp_path, key, ["cid_0", "not_a_column"])

    counter = Counter(["cid_0"])
    feats, hit = fs_cache.cached_select(X, y, "lasso", tmp_path, counter)
    assert hit is False and feats == ["cid_0"]


def test_load_missing_entry_returns_none(tmp_path):
    assert fs_cache.load(tmp_path, "deadbeef" * 8) is None
    assert fs_cache.load(None, "deadbeef" * 8) is None
    assert fs_cache.load(tmp_path, None) is None


def test_store_writes_atomically_and_leaves_no_temp_files(tmp_path):
    X, y = make_xy()
    key = fs_cache.compute_key(X, y, "lasso")
    assert fs_cache.store(tmp_path, key, ["cid_0"], meta={"country": "usa"}) is True

    written = [p for p in Path(tmp_path).rglob("*") if p.is_file()]
    assert len(written) == 1
    assert written[0].name == f"{key}.json"
    assert not [p for p in Path(tmp_path).rglob("*.tmp")]

    payload = json.loads(written[0].read_text(encoding="utf-8"))
    assert payload["selected_features"] == ["cid_0"]
    assert payload["meta"]["country"] == "usa"


def test_repeated_store_of_same_key_is_idempotent(tmp_path):
    """Two workers racing on the same key must converge, not duplicate."""
    X, y = make_xy()
    key = fs_cache.compute_key(X, y, "lasso")
    fs_cache.store(tmp_path, key, ["cid_0"])
    fs_cache.store(tmp_path, key, ["cid_0"])

    assert len([p for p in Path(tmp_path).rglob("*.json")]) == 1
    assert fs_cache.load(tmp_path, key) == ["cid_0"]


def test_entries_are_sharded_by_key_prefix(tmp_path):
    X, y = make_xy()
    key = fs_cache.compute_key(X, y, "lasso")
    fs_cache.store(tmp_path, key, ["cid_0"])
    assert (tmp_path / key[:2] / f"{key}.json").is_file()


def test_store_failure_is_non_fatal(tmp_path, monkeypatch):
    """An unwritable cache directory must not break the run."""
    X, y = make_xy()

    def boom(*args, **kwargs):
        raise OSError("read-only filesystem")

    monkeypatch.setattr(fs_cache.os, "replace", boom)
    counter = Counter(["cid_0"])
    feats, hit = fs_cache.cached_select(X, y, "lasso", tmp_path, counter)

    assert feats == ["cid_0"] and hit is False


def test_cache_dir_for_builds_expected_path(tmp_path):
    assert fs_cache.cache_dir_for(tmp_path) == tmp_path / "cache" / "feature_selection"


# ------------------------------------------ degraded results are not cached


def test_degraded_selection_is_used_but_not_persisted(tmp_path):
    """A 'multi' run whose sub-selector died must not poison later models."""
    X, y = make_xy()
    counter = Counter(["cid_0"])

    feats, hit = fs_cache.cached_select(
        X, y, "multi", tmp_path, counter, should_cache=lambda: False
    )

    assert feats == ["cid_0"] and hit is False
    assert not [p for p in Path(tmp_path).rglob("*.json")]


def test_degraded_result_does_not_block_a_later_clean_one(tmp_path):
    """The remedy of re-running must still work after a degraded call."""
    X, y = make_xy()
    fs_cache.cached_select(X, y, "multi", tmp_path, Counter(["cid_0"]), should_cache=lambda: False)

    clean = Counter(["cid_0", "cid_1", "cid_2"])
    feats, hit = fs_cache.cached_select(X, y, "multi", tmp_path, clean, should_cache=lambda: True)
    assert hit is False and feats == ["cid_0", "cid_1", "cid_2"]

    reuse = Counter(["ignored"])
    feats2, hit2 = fs_cache.cached_select(X, y, "multi", tmp_path, reuse)
    assert hit2 is True and feats2 == ["cid_0", "cid_1", "cid_2"] and reuse.calls == 0


def test_clean_selection_is_still_cached(tmp_path):
    X, y = make_xy()
    fs_cache.cached_select(X, y, "multi", tmp_path, Counter(["cid_0"]), should_cache=lambda: True)
    assert fs_cache.load(tmp_path, fs_cache.compute_key(X, y, "multi")) == ["cid_0"]


def test_multi_flags_degradation_via_status():
    """select_features must report a swallowed sub-selector failure."""
    from geocif.ml import feature_selection as fs

    X, y = make_xy(n_rows=30, n_cols=4)
    status = {}

    # 'multi' recurses into sub-selectors; force them all to fail.
    def boom(*args, **kwargs):
        raise MemoryError("simulated contention failure")

    import geocif.ml.feature_selection as fs_mod

    original = fs_mod.select_features

    def fake_sub(*args, **kwargs):
        if kwargs.get("method") in ("BorutaPy", "mrmr", "gOMP_high"):
            raise MemoryError("simulated contention failure")
        return original(*args, **kwargs)

    fs_mod.select_features = fake_sub
    try:
        original(X, y, method="multi", dir_output=".", status=status)
    except Exception:
        pass
    finally:
        fs_mod.select_features = original

    assert status.get("degraded") is True
    assert status.get("failed_methods")


def test_status_is_optional():
    """Callers that pass no status must be unaffected."""
    from geocif.ml import feature_selection as fs

    X, y = make_xy(seed=3, n_rows=50, n_cols=6)
    _, _, feats = fs.select_features(X, y, method="lasso", dir_output=".")
    assert isinstance(feats, list)


# ------------------------------------------------------- equivalence


def test_cached_result_matches_uncached_real_selector(tmp_path):
    """End-to-end: the cached path returns exactly what the selector did."""
    from geocif.ml import feature_selection as fs

    X, y = make_xy(seed=7, n_rows=60, n_cols=8)

    _, _, direct = fs.select_features(X, y, method="lasso", dir_output=str(tmp_path))

    calls = {"n": 0}

    def compute():
        calls["n"] += 1
        _, _, feats = fs.select_features(X, y, method="lasso", dir_output=str(tmp_path))
        return feats

    first, hit_first = fs_cache.cached_select(X, y, "lasso", tmp_path, compute)
    second, hit_second = fs_cache.cached_select(X, y, "lasso", tmp_path, compute)

    assert first == list(direct)
    assert second == list(direct)
    assert (hit_first, hit_second) == (False, True)
    assert calls["n"] == 1
