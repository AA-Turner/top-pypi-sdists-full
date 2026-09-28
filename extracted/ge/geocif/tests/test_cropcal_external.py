"""The external-model benchmark package: export, fold verification, scoring.

Guards:

* the exported folds are the run's folds -- a package built with different CV
  settings is refused, because it would not reproduce the run's climatology
  null;
* no identifier, target or fold column leaks into features.csv;
* scoring a copy of an in-house model's own predictions reproduces that
  model's metrics exactly and a zero paired difference;
* every column of every file has a definition.
"""

import numpy as np
import pandas as pd
import pytest

from geocif.cropcal import cv, features, models
from geocif.experiments import cropcal_external as ext


class _Mean:
    def __init__(self, y):
        self.value = float(np.nanmean(np.asarray(y, dtype=float)))

    def predict(self, X):
        return np.full(len(X), self.value)


def _run_dir(tmp_path, monkeypatch, n=48):
    monkeypatch.setattr(models, "_fit_one", lambda name, X, y, names: _Mean(y))
    rng = np.random.default_rng(1)
    nan_year = np.full(366, np.nan)
    rows = []
    for i in range(n):
        south = i % 3 == 0
        lat = (-1 if south else 1) * (5.0 + 45.0 * rng.random())
        base = 290.0 if south else 110.0
        days = {"planting": base, "midgreenup": base + 40, "midgreendown": base + 90, "harvest": base + 130}
        days = {k: float((v + rng.normal(0, 10)) % 365) + 1 for k, v in days.items()}
        rows.append(features.build_row(
            key=f"r{i}", country=f"c{i % 8}", region=f"reg{i}", crop="maize" if i % 2 else "sorghum",
            season=1, cm_group="EW", climate_zone="Tropical", hemisphere="S" if south else "N",
            lat=lat, lon=-170.0 + 340.0 * rng.random(), ndvi=nan_year, gdd=nan_year, agdd=nan_year,
            peaks=[], valleys=[], targets=days,
        ))
    design = features.design_matrix(rows)
    schemes = cv.build_schemes(design, n_splits=3, names=ext.SCHEMES)
    evaluation = models.evaluate(design, models=["stub"], schemes=schemes, encodings=("sincos",),
                                 bootstrap_resamples=50, baseline_columns={})
    run = tmp_path / "September_26_2026"
    (run / "models").mkdir(parents=True)
    design.to_csv(run / "models" / "design_matrix.csv", index=False)
    evaluation.predictions.to_csv(run / "models" / "predictions.csv", index=False)
    evaluation.metrics.to_csv(run / "models" / "metrics.csv", index=False)
    return run, evaluation


def test_export_writes_a_clean_verified_package(tmp_path, monkeypatch):
    run, _ = _run_dir(tmp_path, monkeypatch)
    archive = ext.export(run, n_splits=3)
    package = run / ext.PACKAGE_DIR
    assert archive.is_file()
    for name in ("features.csv", "targets.csv", "folds.csv", "predictions_template.csv",
                 "reference_scores.csv", "columns.csv", "README.md"):
        assert (package / name).is_file(), name

    feats = pd.read_csv(package / "features.csv")
    assert list(feats.columns[:4]) == ["row_id", "key", "country", "region"]
    assert set(feats.columns[4:]) == set(features.FEATURE_NAMES)
    assert not [c for c in feats.columns if c.startswith(("target_", "satellite_", "calendar_", "fold_"))]
    assert "hemisphere_zone" not in feats.columns

    template = pd.read_csv(package / "predictions_template.csv")
    assert len(template) == 48 * len(ext.SCHEMES)
    assert template[list(ext.PRED_COLUMNS.values())].isna().all().all()
    folds = pd.read_csv(package / "folds.csv")
    for scheme in ext.SCHEMES:
        assert folds[f"fold_{scheme}"].min() == 0


def test_export_refuses_folds_that_are_not_the_runs(tmp_path, monkeypatch):
    run, _ = _run_dir(tmp_path, monkeypatch)
    with pytest.raises(ValueError, match="do not reproduce"):
        ext.export(run, n_splits=4)            # the run used 3


def test_scoring_our_own_predictions_reproduces_our_metrics(tmp_path, monkeypatch):
    run, evaluation = _run_dir(tmp_path, monkeypatch)
    ext.export(run, n_splits=3)
    template = pd.read_csv(run / ext.PACKAGE_DIR / "predictions_template.csv")
    stub = evaluation.predictions[evaluation.predictions["model"] == "stub"]
    for target, column in ext.PRED_COLUMNS.items():
        part = stub[stub["target"] == target][["scheme", "row_id", "predicted"]]
        filled = template[["scheme", "row_id"]].merge(part, on=["scheme", "row_id"], how="left")["predicted"]
        template[column] = filled.to_numpy()
    submission = tmp_path / "theirs.csv"
    template.to_csv(submission, index=False)

    scored = ext.score(run, submission, name="copy", seed=0)
    ours = evaluation.metrics
    key = ["target", "scheme", "split", "split_value", "sample"]
    a = ours[ours["model"] == "stub"].set_index(key)["mae_days"]
    b = scored.set_index(key)["mae_days"]
    np.testing.assert_allclose(b.loc[a.index].to_numpy(), a.to_numpy())
    paired = pd.read_csv(run / ext.PACKAGE_DIR / "scored_copy" / "paired_copy.csv")
    assert (paired[paired["versus"] == "stub"]["d_mae"].abs() < 1e-9).all()


def test_submission_with_edited_folds_is_rejected(tmp_path, monkeypatch):
    run, _ = _run_dir(tmp_path, monkeypatch)
    ext.export(run, n_splits=3)
    template = pd.read_csv(run / ext.PACKAGE_DIR / "predictions_template.csv")
    template[list(ext.PRED_COLUMNS.values())] = 100.0
    template.loc[0, "fold"] = template.loc[0, "fold"] + 1
    path = tmp_path / "bad.csv"
    template.to_csv(path, index=False)
    with pytest.raises(ValueError, match="fold column differs"):
        ext.score(run, path, name="bad")


def test_every_column_has_a_definition():
    table = ext.column_dictionary()
    assert set(features.FEATURE_NAMES) <= set(table[table["file"] == "features.csv"]["column"])
    assert table["description"].str.len().min() > 5


def test_a_saved_fold_table_wins_over_a_rebuild(tmp_path, monkeypatch):
    run, _ = _run_dir(tmp_path, monkeypatch)
    design = pd.read_csv(run / "models" / "design_matrix.csv")
    schemes = cv.build_schemes(design, n_splits=3, names=ext.SCHEMES)
    cv.fold_table(schemes, design).to_csv(run / "models" / "folds.csv", index=False)
    ext.export(run, n_splits=4)        # wrong settings are ignored: the saved folds are used
    folds = pd.read_csv(run / ext.PACKAGE_DIR / "folds.csv")
    assert folds["fold_spatial_block"].max() == 2


def test_fold_table_round_trips():
    frame = pd.DataFrame({"country": [f"c{i % 6}" for i in range(30)],
                          "lat": np.linspace(-40, 40, 30), "lon": np.linspace(-150, 150, 30)})
    schemes = cv.build_schemes(frame, n_splits=3, names=("spatial_block", "country"))
    back = cv.schemes_from_table(cv.fold_table(schemes, frame))
    for name, scheme in schemes.items():
        a = sorted(tuple(sorted(te)) for _tr, te in scheme.splits)
        b = sorted(tuple(sorted(te)) for _tr, te in back[name].splits)
        assert a == b
