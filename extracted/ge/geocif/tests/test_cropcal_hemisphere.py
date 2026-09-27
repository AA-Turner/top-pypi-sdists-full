"""Per-hemisphere fitting (models.evaluate stratify_by) and its experiment harness.

Guards:

* a stratified fit predicts each test row with a model trained ONLY on its own
  stratum, and a stratum too small to fit falls back to the pooled fit and
  says so;
* the folds and the climatology null are identical across the two arms, so
  the comparison is paired;
* the experiment splits on latitude, not on the zone file's hemisphere column
  (wrong for Ethiopia and friends), and survives a CSV round trip.
"""

import numpy as np
import pandas as pd
import pytest

from geocif.cropcal import cv, features, models
from geocif.experiments import cropcal_hemisphere as hemi


class _Mean:
    def __init__(self, y):
        self.value = float(np.nanmean(np.asarray(y, dtype=float)))

    def predict(self, X):
        return np.full(len(X), self.value)


def _two_hemisphere_frame(n_per_side=40, north_day=100.0, south_day=280.0):
    """North plants on day 100, south on day 280; nothing else distinguishes them."""
    rng = np.random.default_rng(0)
    rows = []
    for side, day, sign in (("N", north_day, 1.0), ("S", south_day, -1.0)):
        for i in range(n_per_side):
            rows.append({
                "key": f"{side}{i}", "country": f"{side}c{i % 5}", "crop": "maize", "season": "1",
                "cm_group": "AMIS", "climate_zone": "Temperate", "hemisphere": side,
                "lat": sign * (20.0 + rng.uniform(0, 20)), "lon": rng.uniform(-60, 60),
                "target_planting": day,
            })
    frame = pd.DataFrame(rows)
    angle = 2 * np.pi * frame["target_planting"] / 365.0
    frame["target_planting_sin"], frame["target_planting_cos"] = np.sin(angle), np.cos(angle)
    return frame


def _evaluate(frame, **kwargs):
    schemes = cv.build_schemes(frame, n_splits=4, names=("random",))
    return models.evaluate(
        frame, models=["stub"], targets=("planting",), schemes=schemes,
        encodings=("sincos",), bootstrap_resamples=0, baseline_columns={}, **kwargs,
    )


def _stub_rows(evaluation, model="stub"):
    p = evaluation.predictions
    return p[p["model"] == model].sort_values("row_id")


def test_stratified_fit_predicts_each_row_from_its_own_stratum(monkeypatch):
    monkeypatch.setattr(models, "_fit_one", lambda name, X, y, names: _Mean(y))
    frame = _two_hemisphere_frame()
    pooled = _stub_rows(_evaluate(frame))
    # ~30 training rows per stratum per fold: below the default threshold, so set it.
    stratified_eval = _evaluate(frame, stratify_by="hemisphere", min_stratum_rows=5)
    stratified = _stub_rows(stratified_eval)

    north = (frame["hemisphere"] == "N").to_numpy()
    # A pooled mean of two antipodal-ish days is neither; the per-stratum mean is exact.
    assert np.abs(pooled["predicted"].to_numpy() - frame["target_planting"].to_numpy()).mean() > 30
    assert stratified["predicted"].to_numpy()[north] == pytest.approx(100.0, abs=1e-6)
    assert stratified["predicted"].to_numpy()[~north] == pytest.approx(280.0, abs=1e-6)
    assert stratified_eval.notes == []


def test_small_stratum_falls_back_to_the_pooled_fit_and_is_reported(monkeypatch):
    monkeypatch.setattr(models, "_fit_one", lambda name, X, y, names: _Mean(y))
    frame = _two_hemisphere_frame()
    pooled = _stub_rows(_evaluate(frame))
    fallback_eval = _evaluate(frame, stratify_by="hemisphere", min_stratum_rows=10_000)
    np.testing.assert_allclose(_stub_rows(fallback_eval)["predicted"], pooled["predicted"])
    assert fallback_eval.notes and "pooled fit" in fallback_eval.notes[0]


def test_stratification_leaves_the_climatology_null_untouched(monkeypatch):
    monkeypatch.setattr(models, "_fit_one", lambda name, X, y, names: _Mean(y))
    frame = _two_hemisphere_frame()
    a = _stub_rows(_evaluate(frame), models.CLIMATOLOGY)
    b = _stub_rows(_evaluate(frame, stratify_by="hemisphere"), models.CLIMATOLOGY)
    np.testing.assert_array_equal(a["predicted"].to_numpy(), b["predicted"].to_numpy())


def test_unknown_stratify_column_is_an_error():
    with pytest.raises(ValueError, match="stratify_by"):
        _evaluate(_two_hemisphere_frame(), stratify_by="no_such_column")


def test_latitude_hemisphere_and_the_zone_label_is_kept(tmp_path):
    frame = _two_hemisphere_frame(n_per_side=3)
    frame.loc[0, "hemisphere"] = "S"                    # an Ethiopia: north of the equator, labelled S
    frame["calendar_wall_to_wall"] = ["False", "True"] + [np.nan] * (len(frame) - 2)
    frame["season"] = 1
    path = tmp_path / "design_matrix.csv"
    frame.to_csv(path, index=False)

    loaded = hemi.load_design(path)
    assert loaded.loc[0, "hemisphere_zone"] == "S" and loaded.loc[0, "hemisphere"] == "N"
    assert (loaded["hemisphere"] == np.where(loaded["lat"] < 0, "S", "N")).all()
    assert loaded["calendar_wall_to_wall"].tolist()[:2] == [False, True]    # "False" is not truthy
    assert not loaded["calendar_wall_to_wall"].iloc[2:].any()
    assert loaded["season"].iloc[0] == "1"
    assert hemi.latitude_hemisphere([-0.1, 0.0, 5.0]).tolist() == ["S", "N", "N"]


def test_paired_difference_sign_and_interval():
    n = 60
    base = pd.DataFrame({"row_id": np.arange(n), "tile": [f"t{i % 12}" for i in range(n)],
                         "predicted": np.full(n, 110.0), "observed": np.full(n, 100.0)})
    better = base.assign(predicted=104.0)
    out = hemi.paired_difference(base, better, resamples=300)
    assert out["d_mae"] == pytest.approx(-6.0)
    assert out["d_mae_ci_low"] <= -6.0 <= out["d_mae_ci_high"]
    assert out["share_b_better"] == 1.0 and out["n"] == n


def test_compare_reports_subsets_and_a_zero_climatology_difference(monkeypatch):
    monkeypatch.setattr(models, "_fit_one", lambda name, X, y, names: _Mean(y))
    frame = _two_hemisphere_frame()
    frame["hemisphere_zone"] = frame["hemisphere"]
    pooled = _evaluate(frame).predictions
    stratified = _evaluate(frame, stratify_by="hemisphere", min_stratum_rows=5).predictions
    table = hemi.compare(pooled, stratified, frame, resamples=100)

    assert {"all", "north", "south", "relabelled"} <= set(table["subset"])
    clim = table[(table["model"] == models.CLIMATOLOGY) & (table["subset"] == "all")]
    assert clim["d_mae"].iloc[0] == pytest.approx(0.0)
    stub = table[(table["model"] == "stub") & (table["subset"] == "all")].iloc[0]
    assert stub["d_mae"] < -30 and bool(stub["ci_excludes_zero"])


def test_figure_has_no_panels_for_the_null_or_the_rule(tmp_path):
    rows = []
    for model, scheme in (("stub", "spatial_block"), (models.CLIMATOLOGY, "spatial_block"), (models.BASELINE, "none")):
        for subset in ("all", "north", "south"):
            rows.append({"model": model, "scheme": scheme, "target": "planting", "subset": subset,
                         "d_mae": 1.0, "d_mae_ci_low": 0.0, "d_mae_ci_high": 2.0})
    panels = hemi.plot_comparison(pd.DataFrame(rows), tmp_path / "comparison.png")
    assert panels == [("spatial_block", "stub")]
    assert (tmp_path / "comparison.png").is_file()


def _bare_row(**overrides):
    nan_year = np.full(366, np.nan)
    kwargs = dict(key="k", country="Ethiopia", region="r", crop="maize", season=1, cm_group="EW",
                  climate_zone="Tropical", hemisphere="S", lat=9.0, lon=39.0, ndvi=nan_year,
                  gdd=nan_year, agdd=nan_year, peaks=[], valleys=[])
    kwargs.update(overrides)
    return features.build_row(**kwargs)


def test_hemisphere_feature_is_the_latitude_sign_and_the_zone_label_is_kept_aside():
    row = _bare_row()                                   # Ethiopia: zone file says S, latitude says N
    assert row["hemisphere"] == "N" and row["hemisphere_zone"] == "S"
    assert _bare_row(hemisphere="N", lat=-0.6)["hemisphere"] == "S"      # Kenya's Nairobi side
    assert _bare_row(lat=float("nan"))["hemisphere"] == "S"             # unknown latitude: zone label
    assert _bare_row(lat=0.0)["hemisphere"] == "N"
    assert "hemisphere_zone" not in features.FEATURE_NAMES
    assert "hemisphere" in features.FEATURE_NAMES


def test_season_blocks_follow_the_latitude_not_the_zone_label():
    doy = np.arange(366)
    july_warm = 20.0 + 10.0 * np.cos(2 * np.pi * (doy - 200) / 365.0)
    row = _bare_row(tmean=july_warm)                    # 9 N, labelled S: July is summer
    assert row["tmean_summer_max"] > row["tmean_winter_max"] + 10
