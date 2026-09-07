"""Tests for the Kansas irrigation x drought diagnostic.

The load path is exercised only for its filtering/pivot logic; the statistical
core gets the real scrutiny, because a diagnostic that reports a spurious
interaction is worse than no diagnostic at all. The two tests that matter are
``test_interaction_fit_recovers_planted_effect`` and its null counterpart:
together they establish that delta_r2 responds to a real interaction and stays
at the noise floor without one.
"""
import matplotlib

matplotlib.use("Agg")  # headless: never open a Tk window during tests

import pathlib

import numpy as np
import pandas as pd
import pytest

from geocif.experiments import irrigation_kansas as ik


# ---------------------------------------------------------------------------
# Theil-Sen
# ---------------------------------------------------------------------------

def test_theilsen_recovers_exact_line():
    x = np.arange(2005, 2025, dtype=float)
    y = 3.0 + 0.15 * x
    m, b = ik._theilsen(x, y)
    assert m == pytest.approx(0.15, abs=1e-9)
    assert b == pytest.approx(3.0, abs=1e-6)


def test_theilsen_ignores_a_single_catastrophic_year():
    """The 2012-style collapse must not drag the trend down.

    An OLS slope would move noticeably; the median of pairwise slopes should
    barely notice one outlier in twenty.
    """
    x = np.arange(2005, 2025, dtype=float)
    y = 3.0 + 0.15 * x
    y[7] -= 5.0
    m, _ = ik._theilsen(x, y)
    assert m == pytest.approx(0.15, abs=0.02)


def test_theilsen_too_short_returns_nan():
    m, b = ik._theilsen(np.array([1.0, 2.0]), np.array([1.0, 2.0]))
    assert np.isnan(m) and np.isnan(b)


# ---------------------------------------------------------------------------
# Yield anomaly
# ---------------------------------------------------------------------------

def _obs_frame(n_regions=4, n_years=20, start=2005):
    rows = []
    for r in range(n_regions):
        for i in range(n_years):
            year = start + i
            rows.append({
                "Region": f"Kansas C{r}",
                "Harvest Year": year,
                "obs": 5.0 + 0.1 * i + 0.3 * ((i % 3) - 1),
            })
    return pd.DataFrame(rows)


def test_yield_anomaly_is_detrended_and_standardised():
    out, dropped = ik._yield_anomaly(_obs_frame(), min_years=12)
    assert dropped.empty
    for _, g in out.groupby("Region"):
        assert g["yield_resid"].mean() == pytest.approx(0.0, abs=0.15)
        assert g["yield_z"].std(ddof=1) == pytest.approx(1.0, abs=1e-6)


def test_yield_anomaly_drops_short_counties_with_a_reason():
    df = _obs_frame(n_regions=2, n_years=20)
    short = df[df["Region"] == "Kansas C0"].head(5)
    df = pd.concat([short, df[df["Region"] == "Kansas C1"]], ignore_index=True)
    out, dropped = ik._yield_anomaly(df, min_years=12)
    assert set(out["Region"]) == {"Kansas C1"}
    assert list(dropped["Region"]) == ["Kansas C0"]
    assert "fewer than 12 years" in dropped.iloc[0]["reason"]


def test_yield_anomaly_drops_constant_series():
    df = _obs_frame(n_regions=1, n_years=20)
    df["obs"] = 7.0
    out, dropped = ik._yield_anomaly(df, min_years=12)
    assert out.empty
    assert dropped.iloc[0]["reason"] == "zero residual variance"


# ---------------------------------------------------------------------------
# Within-county z
# ---------------------------------------------------------------------------

def test_within_county_z_strips_the_between_county_level():
    """Two counties with different levels but identical variation.

    This is the Kansas west-east problem in miniature: if the z-score leaked
    the level, the two counties would not come out identical.
    """
    df = pd.DataFrame({
        "Region": ["A"] * 4 + ["B"] * 4,
        "v": [10.0, 11.0, 12.0, 13.0, 100.0, 101.0, 102.0, 103.0],
    })
    z = ik._within_county_z(df, "v")
    assert z[:4].to_numpy() == pytest.approx(z[4:].to_numpy())
    assert z[:4].mean() == pytest.approx(0.0, abs=1e-12)


def test_within_county_z_constant_county_is_nan_not_inf():
    df = pd.DataFrame({"Region": ["A", "A", "A"], "v": [5.0, 5.0, 5.0]})
    z = ik._within_county_z(df, "v")
    assert z.isna().all()


# ---------------------------------------------------------------------------
# OLS
# ---------------------------------------------------------------------------

def test_ols_recovers_known_coefficients():
    rng = np.random.default_rng(0)
    n = 400
    x1 = rng.normal(size=n)
    x2 = rng.normal(size=n)
    y = 1.5 + 2.0 * x1 - 0.75 * x2 + rng.normal(scale=0.05, size=n)
    beta, t, r2, nn = ik._ols(np.column_stack([np.ones(n), x1, x2]), y)
    assert beta == pytest.approx([1.5, 2.0, -0.75], abs=0.02)
    assert r2 > 0.99
    assert nn == n
    assert abs(t[1]) > 50


def test_ols_underdetermined_returns_none():
    assert ik._ols(np.ones((2, 3)), np.ones(2)) is None


# ---------------------------------------------------------------------------
# The interaction fit -- the load-bearing test
# ---------------------------------------------------------------------------

def _panel(rng, n_regions=100, n_years=20, interaction=0.0, noise=0.3):
    """Synthetic county panel with a planted irrigation x stress effect.

    yield_z = 0.6 * stress_z + interaction * irr_share * stress_z + noise

    A positive ``interaction`` is the irrigation-buffers-drought hypothesis:
    when stress_z is low (bad year), a high irr_share county loses less.
    """
    irr_by_region = rng.uniform(0.0, 0.8, size=n_regions)
    rows = []
    for r in range(n_regions):
        for i in range(n_years):
            s = rng.normal()
            rows.append({
                "Region": f"Kansas C{r}",
                "Harvest Year": 2005 + i,
                "irr_share": irr_by_region[r],
                "cid_z": s,
                "yield_z": (
                    0.6 * s
                    + interaction * irr_by_region[r] * s
                    + rng.normal(scale=noise)
                ),
            })
    return pd.DataFrame(rows)


def test_interaction_fit_recovers_planted_effect():
    rng = np.random.default_rng(42)
    df = _panel(rng, interaction=1.2)
    fit = ik._interaction_fit(df, "cid_z")
    assert fit is not None
    assert fit["beta_interaction"] == pytest.approx(1.2, abs=0.12)
    assert fit["t_interaction"] > 8
    assert fit["delta_r2"] > 0.01
    assert fit["r2_full"] > fit["r2_base"]


def test_interaction_fit_reports_noise_floor_when_no_effect():
    """No planted interaction -> delta_r2 must stay negligible.

    This is the test that stops the diagnostic from manufacturing a reason to
    turn the feature on.
    """
    rng = np.random.default_rng(7)
    df = _panel(rng, interaction=0.0)
    fit = ik._interaction_fit(df, "cid_z")
    assert fit is not None
    assert abs(fit["beta_interaction"]) < 0.15
    assert fit["delta_r2"] < 0.002
    assert abs(fit["t_interaction"]) < 3.0


def test_interaction_fit_sign_follows_the_hypothesis():
    """A negative planted interaction must come back negative."""
    rng = np.random.default_rng(11)
    fit = ik._interaction_fit(_panel(rng, interaction=-1.0), "cid_z")
    assert fit["beta_interaction"] < -0.5


def test_interaction_fit_too_few_rows_returns_none():
    df = pd.DataFrame({
        "yield_z": [1.0, 2.0, 3.0],
        "irr_share": [0.1, 0.2, 0.3],
        "cid_z": [0.5, 0.4, 0.3],
    })
    assert ik._interaction_fit(df, "cid_z") is None


def test_interaction_fit_drops_non_finite_rows():
    rng = np.random.default_rng(3)
    df = _panel(rng, n_regions=20, interaction=1.0)
    df.loc[0, "cid_z"] = np.inf
    df.loc[1, "yield_z"] = np.nan
    fit = ik._interaction_fit(df, "cid_z")
    assert fit is not None
    assert fit["n"] == len(df) - 2


# ---------------------------------------------------------------------------
# Stage pivot
# ---------------------------------------------------------------------------

def _long_frame():
    rows = []
    for stage in (ik.FULL_SEASON_STAGE, "7", "8"):
        for region in ("Kansas Ford", "Kansas Allen"):
            for cid, val in (("MEAN_ESI4WK", 40.0), ("PRCPTOT", 300.0)):
                rows.append({
                    "Region": region, "Harvest Year": 2012, "Stage": stage,
                    "Index": cid, "CID": val + len(stage),
                })
    return pd.DataFrame(rows)


def test_pivot_stage_selects_one_stage_and_widens():
    w = ik._pivot_stage(_long_frame(), "7")
    assert set(w.columns) == {"Region", "Harvest Year",
                              "MEAN_ESI4WK", "PRCPTOT"}
    assert len(w) == 2
    assert w["MEAN_ESI4WK"].iloc[0] == pytest.approx(41.0)


def test_pivot_stage_full_season_differs_from_single_month():
    long = _long_frame()
    season = ik._pivot_stage(long, ik.FULL_SEASON_STAGE)
    july = ik._pivot_stage(long, "7")
    assert season["MEAN_ESI4WK"].iloc[0] != july["MEAN_ESI4WK"].iloc[0]


def test_pivot_stage_unknown_stage_is_empty():
    assert ik._pivot_stage(_long_frame(), "99").empty


def test_single_month_stages_cover_the_season_stage():
    """The full-season stage string must be exactly the single months.

    Guards against a monthly_r encoding change silently making the season
    stage unresolvable, which would empty the whole diagnostic.
    """
    assert set(ik.FULL_SEASON_STAGE.split("_")) == set(ik.SINGLE_MONTH_STAGES)
    assert set(ik._MONTH_LABEL) == set(ik.SINGLE_MONTH_STAGES)


# ---------------------------------------------------------------------------
# Residual headroom -- the upper bound on what the feature can buy
# ---------------------------------------------------------------------------

def _pred_panel(rng, n_regions=60, n_years=21, leak=0.0, noise=8.0):
    """Outlook-DB-shaped predictions whose % error carries a planted
    irrigation x stress structure of strength ``leak``.

    leak = 0 means the model's error has no irrigation signal left in it, so
    the headroom must come back at the noise floor.
    """
    irr_by_region = rng.uniform(0.0, 0.8, size=n_regions)
    rows = []
    for r in range(n_regions):
        for i in range(n_years):
            s = rng.normal()
            err = leak * irr_by_region[r] * s + rng.normal(scale=noise)
            obs = 8.0
            rows.append({
                "Region": f"Kansas C{r}",
                "Harvest Year": 2005 + i,
                "Model": "tabpfn",
                "Stage Name": "Sep 1-Apr 30",
                "obs": obs,
                "pred": obs * (1.0 + err / 100.0),
                "irr_share": irr_by_region[r],
                "TX90p__z": s,
            })
    df = pd.DataFrame(rows)
    pred = df[["Region", "Harvest Year", "Model", "Stage Name", "obs", "pred"]]
    irr = df[["Region", "Harvest Year", "irr_share"]].drop_duplicates()
    season = df[["Region", "Harvest Year", "TX90p__z"]].drop_duplicates()
    return pred, irr, season


def test_residual_headroom_finds_planted_structure(tmp_path):
    rng = np.random.default_rng(5)
    pred, irr, season = _pred_panel(rng, leak=60.0)
    res = ik._analysis_residual_headroom(
        pred, irr, season, "TX90p", tmp_path, tmp_path, "Sep 1-Apr 30"
    )
    assert not res.empty
    allrow = res[res["years"] == "all"].iloc[0]
    assert allrow["r2_irr_x_stress"] > 0.10
    # The interaction, not irrigated share on its own, is what carries it.
    assert allrow["r2_irr_x_stress"] > allrow["r2_irr_only"] + 0.05
    assert allrow["t_interaction"] > 5


def test_residual_headroom_floor_when_error_is_clean(tmp_path):
    """No irrigation structure in the residuals -> near-zero headroom.

    Stops the diagnostic from promising a skill gain that isn't available.
    """
    rng = np.random.default_rng(9)
    pred, irr, season = _pred_panel(rng, leak=0.0)
    res = ik._analysis_residual_headroom(
        pred, irr, season, "TX90p", tmp_path, tmp_path, "Sep 1-Apr 30"
    )
    allrow = res[res["years"] == "all"].iloc[0]
    assert allrow["r2_irr_x_stress"] < 0.01
    assert abs(allrow["t_interaction"]) < 3.0


def test_residual_headroom_splits_stressed_from_other(tmp_path):
    rng = np.random.default_rng(13)
    pred, irr, season = _pred_panel(rng, leak=40.0)
    res = ik._analysis_residual_headroom(
        pred, irr, season, "TX90p", tmp_path, tmp_path, "Sep 1-Apr 30",
        drought_frac=0.33,
    )
    labels = set(res["years"])
    assert labels == {"all", "stressed", "other"}
    n_stressed = res[res["years"] == "stressed"].iloc[0]["n_years"]
    n_other = res[res["years"] == "other"].iloc[0]["n_years"]
    assert n_stressed == 7          # round(21 * 0.33)
    assert n_stressed + n_other == 21


def test_residual_headroom_writes_its_backing_csv(tmp_path):
    rng = np.random.default_rng(17)
    pred, irr, season = _pred_panel(rng, leak=30.0)
    ik._analysis_residual_headroom(
        pred, irr, season, "TX90p", tmp_path, tmp_path, "Sep 1-Apr 30"
    )
    assert (tmp_path / "residual_headroom.csv").exists()
    assert (tmp_path / "residual_headroom.png").exists()


def test_residual_headroom_unknown_stage_is_empty(tmp_path):
    rng = np.random.default_rng(21)
    pred, irr, season = _pred_panel(rng, leak=30.0)
    res = ik._analysis_residual_headroom(
        pred, irr, season, "TX90p", tmp_path, tmp_path, "Nonexistent stage"
    )
    assert res.empty


def test_residual_headroom_stress_sign_picks_the_opposite_tail():
    """stress_sign flips which seasons count as stressed.

    With stress_sign=-1 the hottest years are stressed; with +1 (a CID where
    high is good, like NDVI) the LOWEST years are. Getting this backwards
    would label the best seasons as drought and invert the headline, so the
    two calls must select disjoint year sets.
    """
    import tempfile
    rng = np.random.default_rng(23)
    pred, irr, season = _pred_panel(rng, leak=30.0, n_years=21)

    def stressed_years(sign):
        with tempfile.TemporaryDirectory() as d:
            d = pathlib.Path(d)
            ik._analysis_residual_headroom(
                pred, irr, season, "TX90p", d, d, "Sep 1-Apr 30",
                drought_frac=0.33, stress_sign=sign,
            )
        # Recompute the split the function used, to compare membership.
        m = pred.merge(irr, on=["Region", "Harvest Year"]).merge(
            season, on=["Region", "Harvest Year"])
        per_year = m.groupby("Harvest Year")["TX90p__z"].mean()
        n = max(1, int(round(len(per_year) * 0.33)))
        return set(per_year.sort_values(ascending=(sign > 0)).head(n).index)

    hot = stressed_years(-1.0)
    cold = stressed_years(+1.0)
    assert len(hot) == len(cold) == 7
    assert hot.isdisjoint(cold)
