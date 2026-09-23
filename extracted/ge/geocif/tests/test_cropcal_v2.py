"""cropcal v2: renamed outputs, four targets, moisture/stress features, honest nulls.

Everything here guards a decision the 2026-09-22 design critique forced:

* the result frame has ONE vocabulary (score.RegionScore) and a map from the
  original's names, so a reader of the September-17 outputs can rename them;
* the rule-based satellite days are not features (they are computed inside a
  window the calendar defines), enforced by an allow-list, not a deny-list;
* planting and harvest are predicted, with a climatology null that is
  hemisphere- and season-aware and out of fold;
* rainfall is a per-day MEAN (the median kept a quarter of it), ESI is used
  for its spread, not its level (it is an anomaly), and every optional variable
  is read over the SAME years as NDVI;
* the model sample is not gated on the rule-based method succeeding.
"""

import inspect
import re
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from geocif.cropcal import calendar as cropcal_calendar
from geocif.cropcal import circular, cv, features, models, pipeline, score, series, transitions

N_DOY = 366
CROP = "maize"
COUNTRY_SLUG = "testland"
REGION = "central"
REGION_ID = 42
YEARS = tuple(range(2019, 2025))


# --------------------------------------------------------------------------
# Synthetic archive, with the optional variables
# --------------------------------------------------------------------------
def _ndvi_curve(peak_doy=200, width=35.0):
    doy = np.arange(N_DOY)
    return 0.15 + 0.65 * np.exp(-0.5 * ((doy - peak_doy) / width) ** 2)


def _temperature_curve(mean=15.0, amplitude=12.0, phase=200):
    doy = np.arange(N_DOY)
    return mean + amplitude * np.cos(2 * np.pi * (doy - phase) / 365.0)


def _rain_year(seed, centre=160, width=40, scale=12.0):
    rng = np.random.default_rng(seed)
    doy = np.arange(N_DOY)
    p_wet = 0.05 + 0.45 * np.exp(-0.5 * ((doy - centre) / width) ** 2)
    return np.where(rng.random(N_DOY) < p_wet, rng.exponential(scale, N_DOY), 0.0)


def _write_var(root, var, values_by_year, *, region_id=REGION_ID, region=REGION, encode=None):
    directory = series.region_dir(root, 1, COUNTRY_SLUG, "admin_1", CROP, var)
    directory.mkdir(parents=True, exist_ok=True)
    for year, values in values_by_year.items():
        stored = encode(values) if encode else values
        pd.DataFrame(
            {
                "country": COUNTRY_SLUG, "region": region, "region_id": region_id,
                "lat": 10.0, "lon": 20.0, "year": year, "doy": np.arange(1, N_DOY + 1),
                var: stored, "total_pixels": 1000, "valid_data": 900,
                "valid_data_after_masking": 800, "weight_sum": 1.0, "weight_sum_used": 1.0,
            }
        ).to_csv(directory / f"{region_id}_{region}_{year}_{var}_{CROP}.csv", index=False)


@pytest.fixture
def archive(tmp_path):
    """Six years of every variable, including the four optional ones."""
    ndvi = _ndvi_curve()
    _write_var(tmp_path, series.VAR_NDVI, {y: ndvi for y in YEARS},
               encode=lambda v: v * series.NDVI_GAIN + series.NDVI_OFFSET)
    _write_var(tmp_path, series.VAR_TMAX, {y: _temperature_curve(20.0) for y in YEARS})
    _write_var(tmp_path, series.VAR_TMIN, {y: _temperature_curve(10.0) for y in YEARS})
    _write_var(tmp_path, series.VAR_PRECIP, {y: _rain_year(y) for y in YEARS})
    esi = {}
    for y in YEARS:
        col = np.full(N_DOY, np.nan)
        weekly = np.arange(7, N_DOY, 7)
        col[weekly] = np.random.default_rng(y).normal(0.0, 0.8, weekly.size)
        esi[y] = col
    _write_var(tmp_path, series.VAR_ESI, esi, encode=lambda v: (v + series.ESI_OFFSET) * series.ESI_GAIN)
    sm = 0.15 + 0.2 * np.exp(-0.5 * ((np.arange(N_DOY) - 190) / 50) ** 2)
    _write_var(tmp_path, series.VAR_SM_SURFACE, {y: sm for y in YEARS})
    _write_var(tmp_path, series.VAR_SM_ROOTZONE, {y: sm * 0.9 for y in YEARS})
    return tmp_path


def _calendar_row(codes):
    return pd.Series({f"code_{i}": float(v) for i, v in enumerate(codes)})


def _codes_for_season(start_bin, stage1=3, stage2=4, stage3=3):
    codes = [0] * 24
    cursor = start_bin
    for stage, length in ((1, stage1), (2, stage2), (3, stage3)):
        for _ in range(length):
            codes[cursor % 24] = stage
            cursor += 1
    return codes


def _context(**overrides):
    base = dict(
        key="Central Testland", country="Testland", country_slug=COUNTRY_SLUG,
        region=REGION, region_id=REGION_ID, crop=CROP, season=1, cm_group="AMIS",
        climate_zone="Temperate", hemisphere="N", lat=10.0, lon=20.0,
    )
    base.update(overrides)
    return pipeline.RegionContext(**base)


def _settings(root, **overrides):
    return pipeline.Settings(root=root, years=YEARS, **overrides)


def _design(archive, n=8):
    rows = []
    for index in range(n):
        context = _context(
            key=f"Region{index} Country{index % 3}", country=f"Country{index % 3}",
            lat=10.0 + 12.0 * index, lon=20.0 + 12.0 * index,
            hemisphere="N" if index % 4 else "S",
        )
        outcome = pipeline.run_region(context, _calendar_row(_codes_for_season(7 + index % 6)), _settings(archive))
        assert outcome.scored, outcome.row.get("skip_reason")
        rows.append(outcome.feature_row)
    return features.design_matrix(rows)


# --------------------------------------------------------------------------
# A. one column vocabulary
# --------------------------------------------------------------------------
def test_scored_and_skipped_rows_carry_exactly_the_regionscore_columns(archive, tmp_path):
    scored = pipeline.run_region(_context(), _calendar_row(_codes_for_season(9)), _settings(archive))
    skipped = pipeline.run_region(_context(), _calendar_row(_codes_for_season(9)), _settings(tmp_path / "empty"))
    assert scored.scored and not skipped.scored
    assert set(scored.row) == set(score.COLUMNS)
    assert set(skipped.row) == set(score.COLUMNS)


def test_column_names_are_lowercase_snake_case():
    pattern = re.compile(r"^[a-z][a-z0-9_]*$")
    for name in score.COLUMNS:
        assert pattern.match(name), name


#: The header the September-17 run wrote, verbatim.
SEP17_HEADER = (
    "key,country,region,crop,season,cm_group,grouping,climate_zone,hemisphere,lat,lon,"
    "skip_reason,num_peaks,depeaked,n_years,params_trusted,notes,doy_GEOGLAM_midgreenup,"
    "doy_GEOGLAM_midgreendown,doy_GEOGLAM_plant,doy_GEOGLAM_harvest,doy_RS_midgreenup,"
    "doy_RS_midgreendown,delta_midgreenup,delta_midgreendown,delta_midgreenup_signed,"
    "delta_midgreendown_signed,combined_delta,doy_Peak,Peak_in_2ndStage,len_growth_stage1,"
    "len_growth_stage2,len_growth_stage3,ndvi_midgreenup,ndvi_peak,ndvi_midgreendown,"
    "gdd_in_2ndStage,Assessment,Assessment_midgreenup,Assessment_midgreendown,"
    "Agreement_midgreenup,Agreement_midgreendown,Agreement"
).split(",")


def test_legacy_map_covers_exactly_the_renamed_september_columns():
    unchanged = {c for c in SEP17_HEADER if c in score.COLUMNS}
    renamed = set(SEP17_HEADER) - unchanged
    assert renamed == set(score.LEGACY_FRAME_COLUMNS)
    assert set(score.LEGACY_FRAME_COLUMNS.values()) <= set(score.COLUMNS)


def test_modernise_columns_renames_and_is_idempotent():
    old = pd.DataFrame({c: [1.0] for c in SEP17_HEADER})
    new = score.modernise_columns(old)
    assert set(new.columns) <= set(score.COLUMNS)
    assert score.modernise_columns(new).columns.tolist() == new.columns.tolist()
    # Summary and design-matrix names are covered too.
    summary = pd.DataFrame({"pct_works": [1.0], "max_delta": [45], "rule_midgreenup": [100.0]})
    assert set(score.modernise_columns(summary).columns) == {
        "pct_within_tolerance", "tolerance_days", "satellite_midgreenup_doy"
    }


def test_within_tolerance_is_one_zero_or_nan():
    common = dict(
        geoglam={"midgreenup": 100, "midgreendown": 200, "plant": 80, "harvest": 220,
                 "len_stage1": 30, "len_stage2": 60, "len_stage3": 30},
        fitted=_ndvi_curve(150), masked=_ndvi_curve(150), gdd=np.full(N_DOY, 5.0),
    )
    hit = score.score_region(rs_midgreenup=110, rs_midgreendown=210, **common)
    miss = score.score_region(rs_midgreenup=110, rs_midgreendown=10, **common)
    none = score.score_region(rs_midgreenup=float("nan"), rs_midgreendown=210, **common)
    assert hit["within_tolerance"] == 1 and miss["within_tolerance"] == 0
    assert np.isnan(none["midgreenup_within_tolerance"]) and np.isnan(none["within_tolerance"])
    # Sign convention: calendar minus satellite.
    assert hit["midgreenup_diff_days"] == -10


def test_summary_speaks_the_new_vocabulary(archive):
    outcome = pipeline.run_region(_context(), _calendar_row(_codes_for_season(9)), _settings(archive))
    summary = score.summarise(pd.DataFrame([outcome.row]), by="crop")
    for column in ("median_abs_diff_days_midgreenup", "pct_within_tolerance",
                   "pct_within_tolerance_subset_midgreendown", "n_peak_in_calendar_stage2", "tolerance_days"):
        assert column in summary.columns
    assert not any(c.startswith("pct_works") or "delta" in c for c in summary.columns)


# --------------------------------------------------------------------------
# B. targets and the leak
# --------------------------------------------------------------------------
def test_calendar_key_binds_the_target_names_to_the_calendar_dict():
    assert set(features.CALENDAR_KEY) == set(features.TARGETS)
    bins = cropcal_calendar.stage_bins(np.array(_codes_for_season(9)))
    days = cropcal_calendar.to_days(bins)
    assert set(features.CALENDAR_KEY.values()) <= set(days)


def test_feature_allow_list_excludes_baselines_targets_and_calendar_columns(archive):
    design = _design(archive)
    columns = features.feature_columns(design)
    assert set(columns).isdisjoint(features.BASELINE_COLUMNS.values())
    assert not any(c.startswith(("target_", "calendar_", "satellite_")) for c in columns)
    assert set(features.IDENTIFIER_COLUMNS).isdisjoint(columns)
    # The baselines ARE in the frame; they are just not features.
    for column in features.BASELINE_COLUMNS.values():
        assert column in design.columns
    # And encode() refuses a corrupted allow-list.
    X, names = models.encode(design)
    assert set(names).isdisjoint(features.BASELINE_COLUMNS.values())


def test_encode_refuses_a_baseline_smuggled_into_the_allow_list(archive, monkeypatch):
    design = _design(archive)
    monkeypatch.setattr(features, "FEATURE_NAMES", features.FEATURE_NAMES + ("satellite_midgreenup_doy",))
    with pytest.raises(ValueError, match="non-features"):
        models.encode(design)


def test_feature_row_survives_a_transition_failure(archive, monkeypatch):
    """The model sample must not be gated on the rule-based method."""

    def boom(*_args, **_kwargs):
        raise transitions.TransitionError("forced")

    monkeypatch.setattr(transitions, "rs_transitions", boom)
    outcome = pipeline.run_region(_context(), _calendar_row(_codes_for_season(9)), _settings(archive))
    assert not outcome.scored and "no usable curve" in outcome.row["skip_reason"]
    assert outcome.feature_row is not None
    for target in features.TARGETS:
        assert np.isfinite(outcome.feature_row[f"target_{target}"])
    for column in features.BASELINE_COLUMNS.values():
        assert np.isnan(outcome.feature_row[column])


def test_wall_to_wall_rows_are_flagged_and_masked_for_planting_and_harvest(archive):
    codes = [1] * 6 + [2] * 12 + [3] * 6            # no off-season bin at all
    bins = cropcal_calendar.stage_bins(np.array(codes))
    assert bins.wall_to_wall is True
    outcome = pipeline.run_region(_context(), _calendar_row(codes), _settings(archive))
    assert outcome.row["calendar_wall_to_wall"] is True
    assert outcome.feature_row["calendar_wall_to_wall"] is True

    design = features.design_matrix([outcome.feature_row] * 4)
    design["key"] = [f"k{i}" for i in range(4)]
    design["lat"] = [10.0, 30.0, 50.0, -20.0]
    schemes = {"random": cv.build_schemes(design, n_splits=2, names=("random",))["random"]}
    evaluation = models.evaluate(design, models=[], schemes=schemes, bootstrap_resamples=0)
    clim = evaluation.predictions[evaluation.predictions["model"] == models.CLIMATOLOGY]
    assert clim[clim["target"] == "planting"]["observed"].isna().all()
    assert clim[clim["target"] == "midgreenup"]["observed"].notna().all()


# --------------------------------------------------------------------------
# C. the climatology null
# --------------------------------------------------------------------------
def test_circular_median_respects_the_year_wrap():
    median = features.circular_median_day([355, 360, 2, 5, 10])
    assert circular.circular_gap(median, 2) <= 5
    assert features.circular_std_days([355, 360, 2, 5, 10]) < 15
    assert np.isnan(features.circular_median_day([]))


def _train_frame(spec):
    """``spec``: list of (crop, hemisphere, season, day, count)."""
    rows = []
    for crop, hemi, season, day, count in spec:
        for i in range(count):
            rows.append({"crop": crop, "hemisphere": hemi, "season": str(season),
                         "target_planting": float((day + i) % 365)})
    return pd.DataFrame(rows)


def test_climatology_null_uses_season_then_hemisphere_then_shifted_pooling():
    train = _train_frame([("maize", "N", 1, 100, 6), ("maize", "N", 2, 280, 6), ("maize", "S", 1, 300, 6)])
    test = pd.DataFrame([
        {"crop": "maize", "hemisphere": "N", "season": "1"},
        {"crop": "maize", "hemisphere": "N", "season": "2"},
        {"crop": "maize", "hemisphere": "S", "season": "2"},   # no S season 2 in training
        {"crop": "wheat", "hemisphere": "S", "season": "1"},   # no wheat at all
    ])
    days, levels, n_group, conc = models.climatology_predict(train, test, "planting")
    assert circular.circular_gap(days[0], 102) <= 3 and levels[0] == "crop_hemisphere_season"
    assert circular.circular_gap(days[1], 282) <= 3 and levels[1] == "crop_hemisphere_season"
    assert circular.circular_gap(days[2], 302) <= 3 and levels[2] == "crop_hemisphere"
    assert levels[3] == "all_shifted" and np.isfinite(days[3])
    assert (n_group[:3] == 6).all() and (conc[:3] > 0.9).all()


def test_climatology_null_shifts_hemispheres_instead_of_predicting_the_north_for_the_south():
    train = _train_frame([("maize", "N", 1, 100, 8)])
    test = pd.DataFrame([{"crop": "maize", "hemisphere": "S", "season": "1"}])
    days, levels, *_ = models.climatology_predict(train, test, "planting")
    assert levels[0] == "crop_shifted"
    expected = (103.5 - models.HEMISPHERE_SHIFT_DAYS) % 365
    assert circular.circular_gap(days[0], expected) <= 4, days[0]


def test_climatology_null_falls_through_a_sparse_or_dispersed_group():
    # Two rows: too few. Then a dispersed crop_hemisphere group spread round the year.
    train = _train_frame([("maize", "N", 1, 100, 2)] + [("maize", "N", 2, d, 1) for d in range(0, 360, 30)])
    test = pd.DataFrame([{"crop": "maize", "hemisphere": "N", "season": "1"}])
    _days, levels, n_group, conc = models.climatology_predict(train, test, "planting")
    assert levels[0] not in ("crop_hemisphere_season",)          # only 2 rows
    assert levels[0] != "crop_hemisphere" or conc[0] >= models.MIN_GROUP_CONCENTRATION


# --------------------------------------------------------------------------
# D. encodings, metrics, evaluation
# --------------------------------------------------------------------------
@pytest.mark.parametrize("day,anchor", [(10, 350), (350, 10), (200, 100), (0, 364)])
def test_anchored_encoding_round_trips_across_the_wrap(day, anchor):
    offset = circular.signed_difference(day, anchor)
    assert abs(offset) <= 182.5
    assert features.anchored_to_day(anchor, offset) == pytest.approx(day % 365)


def test_bias_is_calendar_minus_prediction_and_extra_thresholds_exist():
    out = models.circular_metrics(predicted=[100, 200], observed=[110, 190], tolerance=45)
    assert out["bias_days"] == pytest.approx(0.0)
    assert out["median_ae_days"] == pytest.approx(10.0)
    assert {"pct_within_15d", "pct_within_30d", "pct_within_45d"} <= set(out)
    single = models.circular_metrics(predicted=[100], observed=[110])
    assert single["bias_days"] == pytest.approx(10.0)          # calendar later than prediction


def test_paired_skill_and_bootstrap_interval():
    keys = [f"k{i}" for i in range(40)]
    tiles = [f"t{i % 8}" for i in range(40)]
    observed = np.full(40, 200.0)
    rows = np.arange(40)
    model = pd.DataFrame({"row_id": rows, "key": keys, "tile": tiles, "predicted": observed + 10, "observed": observed})
    clim = pd.DataFrame({"row_id": rows, "key": keys, "predicted": observed + 20})
    out = models._paired_skill(model, clim, seed=0, resamples=200)
    assert out["skill_vs_climatology"] == pytest.approx(0.5)
    assert out["skill_ci_low"] <= 0.5 <= out["skill_ci_high"]
    assert out["n_skill"] == 40


def test_paired_skill_pairs_rows_not_region_keys():
    """A calendar-region key repeats once per crop sheet and per season.

    Merging on it was a cartesian product: 4 rows with 2 distinct keys gave
    n_skill = 8 and skill 0.77 where the paired answer is n_skill = 4, 0.5.
    """
    keys = ["r1", "r1", "r2", "r2"]
    observed = np.array([100.0, 200.0, 100.0, 200.0])
    model = pd.DataFrame({"row_id": np.arange(4), "key": keys, "tile": ["a", "a", "b", "b"],
                          "predicted": observed + 10, "observed": observed})
    clim = pd.DataFrame({"row_id": np.arange(4), "key": keys, "predicted": observed + 20})
    out = models._paired_skill(model, clim, seed=0, resamples=0)
    assert out["n_skill"] == 4
    assert out["skill_vs_climatology"] == pytest.approx(0.5)


def test_rule_scored_sample_exists_for_planting_and_harvest(archive, monkeypatch):
    monkeypatch.setattr(models, "_fit_one", lambda name, X, y, names: _Mean(y))
    design = _design(archive, n=6)
    schemes = cv.build_schemes(design, n_splits=2, names=("random",))
    evaluation = models.evaluate(design, models=["stub"], schemes=schemes, bootstrap_resamples=0)
    m = evaluation.metrics
    for target in ("planting", "harvest"):
        cell = m[(m["target"] == target) & (m["sample"] == "rule_scored") & (m["split"] == "overall")]
        assert len(cell) and (cell["n"] > 0).all()


class _Mean:
    def __init__(self, y):
        self.value = float(np.nanmean(np.asarray(y, dtype=float)))

    def predict(self, X):
        return np.full(len(X), self.value)


def test_evaluate_end_to_end_with_a_stub_model(archive, monkeypatch):
    monkeypatch.setattr(models, "_fit_one", lambda name, X, y, names: _Mean(y))
    design = _design(archive, n=9)
    schemes = cv.build_schemes(design, n_splits=3, names=("random", "spatial_block"))
    evaluation = models.evaluate(design, models=["stub"], schemes=schemes, bootstrap_resamples=50)

    preds, metrics = evaluation.predictions, evaluation.metrics
    assert evaluation.failures == []
    assert set(preds["model"]) == {models.BASELINE, models.CLIMATOLOGY, "stub"}
    assert set(preds["target"]) == set(features.TARGETS)
    assert set(preds[preds["model"] == "stub"]["encoding"]) == set(models.ENCODINGS)
    # rule_based exists only where a satellite rule exists.
    assert set(preds[preds["model"] == models.BASELINE]["target"]) == set(features.BASELINE_COLUMNS)
    # climatology under every scheme, every target
    clim = preds[preds["model"] == models.CLIMATOLOGY]
    assert set(clim["scheme"]) == set(schemes) and set(clim["target"]) == set(features.TARGETS)
    assert clim["null_level"].ne("").all()
    # sincos rows carry a resultant, anchored rows do not
    stub = preds[preds["model"] == "stub"]
    assert stub[stub["encoding"] == "sincos"]["resultant"].notna().all()
    assert stub[stub["encoding"] == "anchored"]["resultant"].isna().all()
    # metrics: samples, skill columns, sorted table
    assert set(metrics["sample"]) == {"all", "rule_scored"}
    assert {"skill_vs_climatology", "skill_ci_low", "skill_ci_high", "skill_reference", "n_skill"} <= set(metrics.columns)
    overall = metrics[(metrics["split"] == "overall") & (metrics["sample"] == "all")]
    assert set(overall["target"]) == set(features.TARGETS)
    assert overall[overall["model"] == models.CLIMATOLOGY]["skill_vs_climatology"].isna().all()


# --------------------------------------------------------------------------
# E. features
# --------------------------------------------------------------------------
def _rain_frame(builder):
    return pd.DataFrame({y: builder(y) for y in YEARS[:5]}, index=range(1, N_DOY + 1))


def test_rainfall_climatology_is_a_mean_because_the_median_loses_most_of_it():
    frame = _rain_frame(lambda y: _rain_year(y))
    truth = np.mean([frame[y].sum() for y in frame.columns])
    mean_total = np.nansum(series.per_day_statistic(frame, "mean"))
    median_total = np.nansum(series.per_day_statistic(frame, "median"))
    assert mean_total == pytest.approx(truth, rel=0.02)
    assert median_total < 0.5 * truth


def test_precip_regimes_and_timing():
    uni = _rain_frame(lambda y: _rain_year(y, centre=200))
    out = features.precip_features(series.per_day_statistic(uni, "mean"), uni)
    assert out["precip_regime"] == "unimodal" and out["precip_n_wet_seasons"] == 1
    assert circular.circular_gap(out["doy_precip_p50"], 200) <= 15
    assert circular.circular_gap(out["doy_wet1_peak"], 200) <= 15
    assert out["doy_wet1_onset"] < out["doy_wet1_peak"] < out["doy_wet1_end"]
    assert out["wet1_onset_n_years"] >= 4 and np.isfinite(out["doy_wet1_onset_median"])
    assert np.isnan(out["doy_wet2_peak"])

    def bimodal(y):
        rng = np.random.default_rng(y)
        doy = np.arange(N_DOY)
        p = 0.04 + 0.45 * np.exp(-0.5 * ((doy - 100) / 25) ** 2) + 0.35 * np.exp(-0.5 * ((doy - 300) / 25) ** 2)
        return np.where(rng.random(N_DOY) < p, rng.exponential(10.0, N_DOY), 0.0)

    bi = _rain_frame(bimodal)
    out2 = features.precip_features(series.per_day_statistic(bi, "mean"), bi)
    assert out2["precip_regime"] == "bimodal" and out2["precip_n_wet_seasons"] == 2
    # Peaks of a 30-day sum over five years of Bernoulli rain on a 25-day-wide
    # season wander by a couple of weeks; the claim is "two seasons, roughly
    # here", not a day.
    assert circular.circular_gap(out2["doy_wet1_peak"], 100) <= 25
    assert circular.circular_gap(out2["doy_wet2_peak"], 300) <= 25
    assert out2["doy_wet1_onset_median"] < out2["doy_wet1_peak"]

    arid = uni * 0.05
    out3 = features.precip_features(series.per_day_statistic(arid, "mean"), arid)
    assert out3["precip_regime"] == "arid"
    assert np.isnan(out3["doy_precip_p50"]) and np.isnan(out3["doy_wet1_peak"])


def test_year_round_gdd_reads_as_a_full_year_whatever_day_is_coldest():
    """(end - onset) mod 365 on 366-index labels gave 0 or 364 for the tropics."""
    for coldest in (0, 17, 200, 365):
        tmean = 25 + 3 * np.cos(2 * np.pi * (np.arange(N_DOY) - coldest - 183) / 365)
        gdd = series.growing_degree_days(tmean, 8, 25)
        out = features.thermal_features(tmean, gdd)
        assert out["gdd_season_length_days"] == N_DOY, (coldest, out["gdd_season_length_days"])


def test_per_year_onset_search_does_not_borrow_the_second_season():
    def bimodal(y, first_fails=False):
        rng = np.random.default_rng(y)
        doy = np.arange(N_DOY)
        p1 = 0.0 if first_fails else 0.45
        p = 0.02 + p1 * np.exp(-0.5 * ((doy - 100) / 20) ** 2) + 0.45 * np.exp(-0.5 * ((doy - 300) / 20) ** 2)
        return np.where(rng.random(N_DOY) < p, rng.exponential(12.0, N_DOY), 0.0)

    normal = pd.DataFrame({y: bimodal(y) for y in YEARS[:5]}, index=range(1, N_DOY + 1))
    failed = normal.copy()
    failed[YEARS[0]] = bimodal(YEARS[0], first_fails=True)
    out_normal = features.precip_features(series.per_day_statistic(normal, "mean"), normal)
    out_failed = features.precip_features(series.per_day_statistic(normal, "mean"), failed)
    assert out_normal["precip_regime"] == "bimodal"
    # The failed year contributes no wet1 onset instead of wet2's.
    assert out_failed["wet1_onset_n_years"] == out_normal["wet1_onset_n_years"] - 1
    assert circular.circular_gap(out_failed["doy_wet1_onset_median"], 100) < 60


def test_flat_temperate_rain_with_bumps_is_one_season_not_three():
    """Height alone counted every bump on a Corn-Belt-like curve as a season."""
    def temperate(y):
        rng = np.random.default_rng(y)
        doy = np.arange(N_DOY)
        p = 0.25 + 0.15 * np.exp(-0.5 * ((doy - 170) / 60) ** 2) + 0.05 * np.cos(2 * np.pi * doy / 91)
        return np.where(rng.random(N_DOY) < p, rng.exponential(8.0, N_DOY), 0.0)

    frame = _rain_frame(temperate)
    out = features.precip_features(series.per_day_statistic(frame, "mean"), frame)
    assert out["precip_regime"] in ("unimodal", "everwet"), out["precip_regime"]
    if out["precip_regime"] == "unimodal":
        assert out["precip_n_wet_seasons"] == 1


def test_anchor_is_the_fitted_curve_not_the_raw_median():
    assert features.ANCHOR_FEATURE == "doy_fitted_max_rise"
    row = features.curve_features(_ndvi_curve() + np.random.default_rng(0).normal(0, 0.05, N_DOY),
                                  peaks=[200], valleys=[], fitted=_ndvi_curve())
    # The smooth curve's steepest rise sits one width before the peak; the noisy
    # raw median's does not reliably.
    assert circular.circular_gap(row["doy_fitted_max_rise"], 200 - 35) <= 3


def test_thermal_onset_lies_between_the_coldest_day_and_the_warmest():
    tmean = 12 + 14 * np.cos(2 * np.pi * (np.arange(N_DOY) - 200) / 365)
    gdd = series.growing_degree_days(tmean, 8, 25)
    out = features.thermal_features(tmean, gdd)
    assert circular.circular_gap(out["doy_tmean_min"], 17) <= 3
    assert circular.circular_gap(out["doy_tmean_max"], 200) <= 3
    assert out["doy_tmean_min"] < out["doy_gdd_onset"] < out["doy_tmean_max"] < out["doy_gdd_end"]
    assert 150 < out["gdd_season_length_days"] < 300


def test_esi_features_describe_spread_and_coverage_never_level():
    frame = pd.DataFrame(np.nan, index=range(1, N_DOY + 1), columns=list(YEARS[:5]))
    weekly = np.arange(8, N_DOY, 7)
    for y in frame.columns:
        frame.loc[weekly, y] = np.random.default_rng(y).normal(0, 0.4 + 1.2 * np.exp(-0.5 * ((weekly - 220) / 30) ** 2), weekly.size)
    out = features.esi_features(frame)
    assert not any(k in out for k in ("esi_min", "esi_mean", "esi_max", "doy_esi_min"))
    assert circular.circular_gap(out["doy_esi_std_max"], 220) <= 25
    assert 0.1 < out["esi_frac_observed_mean"] < 0.2          # weekly = 1/7 of days


def test_absent_optional_inputs_yield_nan_features_flags_and_a_complete_row():
    nan_year = np.full(N_DOY, np.nan)
    row = features.build_row(
        key="k", country="c", region="r", crop="maize", season=1, cm_group="", climate_zone="",
        hemisphere="N", lat=0.0, lon=0.0, ndvi=_ndvi_curve(), gdd=nan_year, agdd=nan_year,
        peaks=[200], valleys=[], targets={t: 100.0 for t in features.TARGETS},
    )
    for flag in ("precip_available", "esi_available", "sm_surface_available", "sm_rootzone_available"):
        assert row[flag] == 0
    assert np.isnan(row["doy_wet1_peak"]) and np.isnan(row["sm_surface_min"]) and row["precip_regime"] == "unknown"
    assert set(features.FEATURE_NAMES) <= set(row)


def test_optional_variables_follow_the_ndvi_year_window(archive):
    """A feed that stopped early must not get its own five-year window."""
    sm_dir = series.region_dir(archive, 1, COUNTRY_SLUG, "admin_1", CROP, series.VAR_SM_SURFACE)
    (sm_dir / f"{REGION_ID}_{REGION}_2024_{series.VAR_SM_SURFACE}_{CROP}.csv").unlink()
    (sm_dir / f"{REGION_ID}_{REGION}_2023_{series.VAR_SM_SURFACE}_{CROP}.csv").unlink()
    esi_dir = series.region_dir(archive, 1, COUNTRY_SLUG, "admin_1", CROP, series.VAR_ESI)
    for year in YEARS[:-2]:                      # leave ESI only 2024 (dropped) + 2023
        (esi_dir / f"{REGION_ID}_{REGION}_{year}_{series.VAR_ESI}_{CROP}.csv").unlink()

    from geocif.cropcal import naming
    clim = series.build_climatology(archive, 1, COUNTRY_SLUG, "admin_1", CROP, REGION, REGION_ID,
                                    params=naming.crop_params(CROP), years=YEARS, num_years=5)
    assert clim.years_used == (2019, 2020, 2021, 2022, 2023)
    assert list(clim.sm_surface_years.columns) == list(clim.years_used)      # aligned, 2023 NaN
    assert clim.n_years_by_var[series.VAR_SM_SURFACE] == 4
    assert clim.esi_years is None and clim.n_years_by_var[series.VAR_ESI] == 1
    assert clim.available[series.VAR_ESI] is False and clim.available[series.VAR_PRECIP] is True
    assert clim.tmean is not None and np.isfinite(clim.tmean).all()


def test_rescale_decodes_esi_and_masks_physical_ranges():
    esi = series.rescale(np.array([0.0, 40.0, 80.0, 568.0, -5.0]), series.VAR_ESI)
    assert esi[:3] == pytest.approx([-4.0, 0.0, 4.0])
    assert np.isnan(esi[3]) and np.isnan(esi[4])
    sm = series.rescale(np.array([0.3, 1250.4, -0.1, 9999.0]), series.VAR_SM_ROOTZONE)
    assert sm[0] == 0.3 and np.isnan(sm[1:]).all()
    assert series.rescale(np.array([159.46]), series.VAR_NDVI)[0] == pytest.approx(0.5473)


# --------------------------------------------------------------------------
# F. cross-validation diagnostics
# --------------------------------------------------------------------------
def _dup_frame():
    rows = []
    for c, lat in (("A", 5.0), ("B", 25.0), ("C", 45.0), ("D", -25.0)):
        for i in range(3):                       # a national row copied across three zones
            rows.append({"key": f"{c}{i}", "country": c, "crop": "maize", "season": "1",
                         "lat": lat + i, "lon": 3.0 * i, "target_planting": 100.0 + ord(c),
                         "target_midgreenup": 130.0, "target_midgreendown": 200.0, "target_harvest": 250.0})
    return pd.DataFrame(rows)


def test_duplicate_leakage_is_high_for_random_and_zero_for_country():
    frame = _dup_frame()
    schemes = cv.build_schemes(frame, n_splits=3, names=("random", "country"))
    assert cv.duplicate_leakage(frame, schemes["random"]) > 50.0
    assert cv.duplicate_leakage(frame, schemes["country"]) == 0.0
    table = cv.describe(schemes, frame)
    assert "pct_test_rows_with_train_duplicate" in table.columns


def test_country_block_holds_small_countries_whole():
    frame = _dup_frame()
    groups = cv.country_blocks(frame["country"], frame["lat"], frame["lon"], block_degrees=10.0)
    for c in "ABCD":
        labels = set(groups[frame["country"] == c])
        assert len(labels) == 1 and labels.pop().startswith("country:")


# --------------------------------------------------------------------------
# G. runner wiring
# --------------------------------------------------------------------------
def test_runner_and_config_generator_know_about_encodings_and_baselines():
    from geocif import calendar_validator
    from geocif.data_prep import make_cropcal_config

    runner = inspect.getsource(calendar_validator)
    assert '_getlist("target_encodings"' in runner
    assert "baseline_columns=features.BASELINE_COLUMNS" in runner
    assert "peak_in_calendar_stage2" in runner and "Peak_in_2ndStage" not in runner
    assert '"column_scheme": 2' in runner
    generator = inspect.getsource(make_cropcal_config)
    assert "target_encodings" in generator
    assert "cv_schemes = ['random', 'country', 'spatial_block', 'country_block']" in generator
    # and the runner hands the tile size it built the folds with to the bootstrap
    assert "block_degrees=obj.block_degrees," in runner
