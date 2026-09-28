"""Hand the crop-calendar benchmark to someone else's model, then score what comes back.

``export`` writes a self-contained package from a ``calendar_validator`` run:
the model inputs, the four calendar targets, the EXACT cross-validation folds
the in-house models were scored on, a blank predictions sheet in the shape
``score`` reads, a column dictionary and a README. Using our folds is what
makes the comparison paired: every region is predicted once per scheme by a
model that never saw that region's fold, and their error and ours are
compared on the same rows with the same tile bootstrap.

The folds are rebuilt with :func:`geocif.cropcal.cv.build_schemes` and then
checked against the run itself: the out-of-fold climatology null recomputed on
the rebuilt folds must reproduce the run's ``predictions.csv`` exactly, or the
export refuses to write anything.

``score`` reads the filled sheet, validates it (coverage, day range, folds
untouched), and scores it with :func:`geocif.cropcal.models.summarise_predictions`
against the run's own climatology null, plus a paired MAE difference against
each in-house model.

Usage::

    from geocif.experiments import cropcal_external as ext
    ext.export("/gpfs/.../calendar_validation/September_26_2026")
    ext.score("/gpfs/.../calendar_validation/September_26_2026",
              "their_predictions.csv", name="colleague_rf")
"""
from __future__ import annotations

import json
import logging
import shutil
from pathlib import Path
from typing import Optional, Sequence

import numpy as np
import pandas as pd

from geocif.cropcal import circular, cv, features, models
from geocif.experiments import cropcal_hemisphere

logger = logging.getLogger(__name__)

#: Schemes in the package, most important first. country_block is the
#: headline; spatial_block is the common literature choice; random is the
#: leaky reference; country (leave-one-country-out) is the clean one.
SCHEMES = ("country_block", "spatial_block", "random", "country")

ID_COLUMNS = ("row_id", "key", "country", "region")
PRED_COLUMNS = {target: f"pred_{target}_doy" for target in features.TARGETS}
PACKAGE_DIR = "share_ml_template"

#: Largest climatology-null disagreement, in days, accepted as "same folds".
FOLD_TOLERANCE_DAYS = 1e-6

# --------------------------------------------------------------------------
# Column dictionary
# --------------------------------------------------------------------------
_DAY = "day of year counted from 0 (0 = 1 January, 364 = 31 December)"

#: Descriptions of every non-circular feature. ``_sin``/``_cos`` companions are
#: described from their base name; ``{var}_{block}_{stat}`` season blocks are
#: generated.
_FEATURE_TEXT = {
    # geography
    "lat": ("degrees", "region centroid latitude"),
    "lon": ("degrees", "region centroid longitude"),
    "abs_lat": ("degrees", "absolute latitude"),
    "hemisphere": ("category", "N or S from the sign of the centroid latitude"),
    "climate_zone": ("category", "Temperate or Tropical, from the GEOGLAM zone file"),
    "cm_group": ("category", "Crop Monitor group: AMIS, EW (Early Warning), AMIS & EW, Global"),
    "crop": ("category", "crop: maize, millet, rice, sorghum, soybean, spring_wheat, teff, winter_wheat"),
    "season": ("category", "season index of the calendar sheet (1, 2, 3); a label, not a date"),
    # NDVI curve
    "ndvi_min": ("NDVI", "minimum of the daily NDVI climatology"),
    "ndvi_max": ("NDVI", "maximum of the daily NDVI climatology"),
    "ndvi_mean": ("NDVI", "mean of the daily NDVI climatology"),
    "ndvi_std": ("NDVI", "standard deviation of the daily NDVI climatology over the year"),
    "ndvi_amplitude": ("NDVI", "ndvi_max - ndvi_min"),
    "ndvi_integral": ("NDVI x day", "sum of the daily NDVI climatology over the year"),
    "ndvi_days_observed": ("days", "days of the year with an NDVI value"),
    "n_peaks": ("count", "NDVI peaks on the Fourier-fitted curve"),
    "n_valleys": ("count", "NDVI valleys on the Fourier-fitted curve"),
    "max_rise": ("NDVI/day", "largest one-day NDVI increase (raw climatology)"),
    "max_fall": ("NDVI/day", "largest one-day NDVI decrease (raw climatology, negative)"),
    "doy_max_rise": ("day", f"{_DAY} of max_rise"),
    "doy_max_fall": ("day", f"{_DAY} of max_fall"),
    "season_span": ("days", "circular days between doy_max_rise and doy_max_fall"),
    "doy_peak": ("day", f"{_DAY} of the NDVI maximum (raw climatology)"),
    "ndvi_at_peak": ("NDVI", "NDVI on doy_peak"),
    "doy_fitted_max_rise": ("day", f"{_DAY} of the steepest rise of the Fourier-fitted NDVI curve"),
    "doy_fitted_max_fall": ("day", f"{_DAY} of the steepest fall of the Fourier-fitted NDVI curve"),
    "doy_fitted_peak": ("day", f"{_DAY} of the maximum of the Fourier-fitted NDVI curve"),
    "ndvi_second_peak_ratio": ("ratio", "height of the second-highest NDVI peak / the highest (0 with one peak)"),
    "ndvi_peak_separation_days": ("days", "circular days between the two highest NDVI peaks"),
    # GDD
    "agdd_total": ("degC x day", "annual accumulated growing degree days"),
    "gdd_max": ("degC", "largest daily GDD"),
    "gdd_mean": ("degC", "mean daily GDD"),
    "gdd_days_positive": ("days", "days with GDD > 0"),
    "doy_agdd_p25": ("day", f"{_DAY} when accumulated GDD reaches 25% of the annual total"),
    "doy_agdd_p50": ("day", f"{_DAY} when accumulated GDD reaches 50% of the annual total"),
    "doy_agdd_p75": ("day", f"{_DAY} when accumulated GDD reaches 75% of the annual total"),
    # thermal
    "tmean_min": ("degC", "minimum of the 15-day-smoothed daily mean temperature"),
    "tmean_max": ("degC", "maximum of the 15-day-smoothed daily mean temperature"),
    "doy_tmean_min": ("day", f"{_DAY} of the coldest point of the year"),
    "doy_tmean_max": ("day", f"{_DAY} of the warmest point of the year"),
    "doy_gdd_onset": ("day", f"{_DAY} starting the first run of >= 10 days with GDD > 0, walking from the coldest day"),
    "doy_gdd_end": ("day", f"{_DAY} ending the last such run"),
    "gdd_season_length_days": ("days", "days from doy_gdd_onset to doy_gdd_end"),
    # precipitation
    "precip_regime": ("category", "arid, unimodal, bimodal, multimodal, everwet or unknown"),
    "precip_total_mm": ("mm", "annual rainfall"),
    "precip_max_30d_mm": ("mm", "wettest 30-day rainfall total"),
    "precip_seasonality": ("ratio", "wettest 30-day total / mean monthly total"),
    "precip_wet_days_per_year": ("days", "days per year with > 1 mm"),
    "precip_n_wet_seasons": ("count", "distinct wet seasons in the 30-day rainfall curve"),
    "doy_precip_anchor": ("day", f"{_DAY} at the centre of the driest 90-day window (the timing reference for rain)"),
    "doy_precip_p10": ("day", f"{_DAY} by which 10% of the annual rain has fallen, counting from doy_precip_anchor"),
    "doy_precip_p50": ("day", f"{_DAY} by which 50% of the annual rain has fallen, counting from doy_precip_anchor"),
    "doy_precip_p90": ("day", f"{_DAY} by which 90% of the annual rain has fallen, counting from doy_precip_anchor"),
    "doy_wet1_onset": ("day", f"{_DAY} the first wet season starts (30-day rain rises to 25% of its peak)"),
    "doy_wet1_peak": ("day", f"{_DAY} of the first wet season's peak"),
    "doy_wet1_end": ("day", f"{_DAY} the first wet season ends (falls below 25% of its peak)"),
    "doy_wet1_onset_median": ("day", f"{_DAY}: median across years of the per-year rain onset in the first wet season "
                                     "(>= 20 mm in 3 days, no 10-day dry spell in the next 30 days)"),
    "wet1_onset_std_days": ("days", "circular standard deviation of that per-year onset"),
    "wet1_onset_n_years": ("count", "years in which that onset was detected"),
    "doy_wet2_onset": ("day", f"{_DAY} the second wet season starts (bimodal regimes only)"),
    "doy_wet2_peak": ("day", f"{_DAY} of the second wet season's peak"),
    "doy_wet2_end": ("day", f"{_DAY} the second wet season ends"),
    "doy_wet2_onset_median": ("day", f"{_DAY}: median per-year rain onset in the second wet season"),
    "wet2_onset_std_days": ("days", "circular standard deviation of the second-season per-year onset"),
    "wet2_onset_n_years": ("count", "years in which the second-season onset was detected"),
    "precip_available": ("0/1", "1 if rainfall data exist for the region"),
    # ESI
    "esi_std_max": ("ESI sd", "highest interannual standard deviation of ESI across the year (15-day smoothed)"),
    "esi_std_min": ("ESI sd", "lowest interannual standard deviation of ESI across the year"),
    "esi_std_mean": ("ESI sd", "mean interannual standard deviation of ESI"),
    "doy_esi_std_max": ("day", f"{_DAY} of the highest ESI variability (typically inside the growing season)"),
    "esi_frac_observed_mean": ("fraction", "mean share of years with an ESI retrieval on a given day"),
    "esi_frac_observed_min": ("fraction", "lowest 15-day-smoothed share of years with an ESI retrieval"),
    "esi_available": ("0/1", "1 if ESI data exist for the region"),
    # soil moisture
    "sm_surface_min": ("m3/m3", "minimum of the smoothed surface soil-moisture climatology"),
    "sm_surface_max": ("m3/m3", "maximum of the smoothed surface soil-moisture climatology"),
    "sm_surface_mean": ("m3/m3", "mean surface soil moisture"),
    "doy_sm_surface_min": ("day", f"{_DAY} of the driest surface soil"),
    "doy_sm_surface_max": ("day", f"{_DAY} of the wettest surface soil"),
    "doy_sm_surface_max_rise": ("day", f"{_DAY} of the largest 30-day increase in surface soil moisture (wetting-up)"),
    "doy_sm_surface_rise_median": ("day", f"{_DAY}: median across years of the per-year wetting-up day"),
    "sm_surface_rise_std_days": ("days", "circular standard deviation of the per-year wetting-up day"),
    "sm_surface_rise_n_years": ("count", "years with a detected wetting-up day"),
    "sm_surface_available": ("0/1", "1 if surface soil-moisture data exist for the region"),
    "sm_rootzone_min": ("m3/m3", "minimum of the smoothed root-zone soil-moisture climatology"),
    "sm_rootzone_max": ("m3/m3", "maximum of the smoothed root-zone soil-moisture climatology"),
    "sm_rootzone_mean": ("m3/m3", "mean root-zone soil moisture"),
    "doy_sm_rootzone_min": ("day", f"{_DAY} of the driest root zone"),
    "doy_sm_rootzone_max": ("day", f"{_DAY} of the wettest root zone"),
    "doy_sm_rootzone_max_fall": ("day", f"{_DAY} of the largest 30-day decrease in root-zone moisture (drawdown)"),
    "sm_rootzone_available": ("0/1", "1 if root-zone soil-moisture data exist for the region"),
    # terrain
    "elevation_m": ("m", "crop-weighted mean elevation (GMT earth_relief, 3 arc-minutes)"),
    "terrain_slope": ("m/m", "crop-weighted slope between 0.05-degree cells (ranks flat vs hilly, not an agronomic slope)"),
    "terrain_available": ("0/1", "1 if elevation data exist for the region"),
    # dew point
    "tdew_min": ("degC", "minimum of the 15-day-smoothed 2 m dew point (AgERA5)"),
    "tdew_max": ("degC", "maximum of the smoothed dew point"),
    "tdew_mean": ("degC", "mean dew point"),
    "tdew_amplitude": ("degC", "tdew_max - tdew_min"),
    "dewpoint_depression_min": ("degC", "minimum of temperature minus dew point (most humid air)"),
    "dewpoint_depression_max": ("degC", "maximum of temperature minus dew point (driest air)"),
    "dewpoint_depression_mean": ("degC", "mean temperature minus dew point"),
    "doy_tdew_min": ("day", f"{_DAY} of the lowest dew point"),
    "doy_tdew_max": ("day", f"{_DAY} of the highest dew point"),
    "doy_dewpoint_depression_min": ("day", f"{_DAY} of the most humid air"),
    "tdew_available": ("0/1", "1 if dew-point data exist for the region"),
}

_BLOCK_VAR = {"tmean": ("degC", "mean temperature"), "precip": ("mm/day", "rainfall rate"), "tdew": ("degC", "dew point")}
_BLOCK_TEXT = {
    "winter": "winter months (Dec-Feb in the north, Jun-Aug in the south)",
    "spring": "spring months (Mar-May north, Sep-Nov south)",
    "summer": "summer months (Jun-Aug north, Dec-Feb south)",
    "fall": "autumn months (Sep-Nov north, Mar-May south)",
    "annual": "all 12 months",
}
_STAT_TEXT = {"min": "lowest", "max": "highest", "amplitude": "highest minus lowest"}


def _group_of(name: str) -> str:
    for group, names in features.FEATURE_GROUPS.items():
        if name in names:
            return group
    return ""


def describe_feature(name: str) -> tuple[str, str]:
    """``(units, description)`` for one feature name."""
    if name in _FEATURE_TEXT:
        return _FEATURE_TEXT[name]
    for suffix, fn in (("_sin", "sine"), ("_cos", "cosine")):
        if name.endswith(suffix):
            base = name[: -len(suffix)]
            return ("-1..1", f"{fn} of {base} on the annual circle (2*pi*day/365); use the pair, not the raw day, "
                             f"if your model is not circular-aware")
    parts = name.split("_")
    if len(parts) == 3 and parts[0] in _BLOCK_VAR and parts[1] in _BLOCK_TEXT and parts[2] in _STAT_TEXT:
        units, what = _BLOCK_VAR[parts[0]]
        return units, f"{_STAT_TEXT[parts[2]]} monthly mean of {what} over the {_BLOCK_TEXT[parts[1]]}"
    raise KeyError(f"no description for feature {name!r}")


def column_dictionary() -> pd.DataFrame:
    """One row per column of every file in the package."""
    rows = [
        ("features.csv", "row_id", "identifier", "", "row number; the join key across every file. NOT a feature"),
        ("features.csv", "key", "identifier", "", "GEOGLAM Crop Monitor calendar-region name. NOT a feature"),
        ("features.csv", "country", "identifier", "", "country. NOT a feature (it would let the model memorise national calendars)"),
        ("features.csv", "region", "identifier", "", "region name as extracted. NOT a feature"),
    ]
    for name in features.FEATURE_NAMES:
        units, text = describe_feature(name)
        rows.append(("features.csv", name, f"feature: {_group_of(name)}", units, text))
    rows.append(("targets.csv", "row_id", "identifier", "", "join key to features.csv"))
    for target in features.TARGETS:
        label = {"planting": "planting (start of calendar stage 1)",
                 "midgreenup": "mid-greenup (end of calendar stage 1)",
                 "midgreendown": "mid-greendown (end of calendar stage 2)",
                 "harvest": "harvest (end of calendar stage 3)"}[target]
        rows.append(("targets.csv", f"target_{target}", "target", "day 1-365",
                     f"calendar day of year of {label}, counted from 1 (1 = 1 January); circular"))
        rows.append(("targets.csv", f"target_{target}_sin", "target", "-1..1", f"sin(2*pi*target_{target}/365)"))
        rows.append(("targets.csv", f"target_{target}_cos", "target", "-1..1", f"cos(2*pi*target_{target}/365)"))
    rows.append(("folds.csv", "row_id", "identifier", "", "join key to features.csv"))
    rows.append(("folds.csv", "tile", "grouping", "", "10-degree centroid tile, 'latrow_loncol' (floor(lat/10)_floor(lon/10))"))
    for scheme in SCHEMES:
        rows.append(("folds.csv", f"fold_{scheme}", "fold", "integer",
                     f"test fold of this row under the {scheme} scheme: train on every other fold, predict this one"))
    for name, text in (
        ("row_id", "join key (do not change)"), ("key", "calendar region (for reading only)"),
        ("country", "country (for reading only)"), ("crop", "crop (for reading only)"),
        ("season", "season index (for reading only)"), ("scheme", "CV scheme of this row"),
        ("fold", "the fold this row is predicted in under this scheme (copied from folds.csv)"),
    ):
        rows.append(("predictions_template.csv", name, "given", "", text))
    for target, column in PRED_COLUMNS.items():
        rows.append(("predictions_template.csv", column, "TO FILL", "day 1-365",
                     f"your out-of-fold predicted day of year for {target}, 1 = 1 January; decimals fine"))
    for name, text in (
        ("model", "model name (ours: tabpfn, tabicl, catboost, cubist, rule_based, climatology)"),
        ("target", "planting, midgreenup, midgreendown or harvest"), ("scheme", "cross-validation scheme"),
        ("n", "regions scored"), ("mae_days", "mean absolute circular error, days"),
        ("rmse_days", "root mean square circular error, days"), ("bias_days", "mean of calendar minus prediction, days"),
        ("pct_within_15d", "% of regions within 15 days"), ("pct_within_30d", "% within 30 days"),
        ("pct_within_45d", "% within 45 days"), ("pct_blunders", "% more than 60 days off"),
        ("r2_circular", "squared circular correlation"),
        ("skill_vs_climatology", "1 - MAE / MAE of the climatology baseline on the same rows"),
        ("skill_ci_low", "90% tile-bootstrap interval, low"), ("skill_ci_high", "90% tile-bootstrap interval, high"),
    ):
        rows.append(("reference_scores.csv", name, "", "", text))
    return pd.DataFrame(rows, columns=["file", "column", "role", "units", "description"])


# --------------------------------------------------------------------------
# Folds
# --------------------------------------------------------------------------
def rebuild_folds(
    frame: pd.DataFrame,
    *,
    schemes: Sequence[str] = SCHEMES,
    n_splits: int = cv.DEFAULT_N_SPLITS,
    block_degrees: float = cv.DEFAULT_BLOCK_DEGREES,
    seed: int = 0,
) -> tuple[dict, pd.DataFrame]:
    """The run's CV schemes and a ``row_id x fold_<scheme>`` table."""
    built = cv.build_schemes(frame, n_splits=n_splits, block_degrees=block_degrees, seed=seed, names=schemes)
    return built, cv.fold_table(built, frame, block_degrees)


def verify_folds(frame: pd.DataFrame, built: dict, run_predictions: pd.DataFrame) -> dict[str, float]:
    """Recompute the climatology null on ``built`` and compare with the run's.

    Returns the largest circular gap per scheme; all must be ~0 (float noise)
    for the folds to be the ones the in-house models were scored on.
    """
    clim = run_predictions[run_predictions["model"] == models.CLIMATOLOGY]
    worst = {}
    for name, scheme in built.items():
        gaps = []
        for target in features.TARGETS:
            column = f"target_{target}"
            valid = np.isfinite(frame[column].to_numpy(dtype=float))
            recomputed = np.full(len(frame), np.nan)
            for train_idx, test_idx in scheme.splits:
                train_rows = frame.iloc[train_idx][valid[train_idx]]
                days, *_ = models.climatology_predict(train_rows, frame.iloc[test_idx], target)
                recomputed[test_idx] = days
            ours = clim[(clim["scheme"] == name) & (clim["target"] == target)].set_index("row_id")["predicted"]
            if ours.empty:
                gaps.append(np.nan)
                continue
            aligned = recomputed[ours.index.to_numpy()]
            reference = ours.to_numpy(dtype=float)
            if not (np.isnan(aligned) == np.isnan(reference)).all():
                gaps.append(np.inf)          # a row predicted in one and not the other
                continue
            gaps.append(max((circular.circular_gap(a, b) for a, b in zip(aligned, reference)
                             if np.isfinite(a) and np.isfinite(b)), default=0.0))
        # NaN (no climatology rows for this scheme in the run) counts as a failure.
        known = [g for g in gaps if not np.isnan(g)]
        worst[name] = float(max(known)) if len(known) == len(gaps) else float("nan")
    return worst


# --------------------------------------------------------------------------
# Export
# --------------------------------------------------------------------------
def _reference_scores(run_metrics: pd.DataFrame) -> pd.DataFrame:
    keep = ["model", "target", "scheme", "n", "mae_days", "rmse_days", "bias_days", "pct_within_15d",
            "pct_within_30d", "pct_within_45d", "pct_blunders", "r2_circular",
            "skill_vs_climatology", "skill_ci_low", "skill_ci_high"]
    m = run_metrics[(run_metrics["split"] == "overall") & (run_metrics["sample"] == "all")]
    m = m[m["encoding"].isin(["sincos", "none"])]
    order = {t: i for i, t in enumerate(features.TARGETS)}
    m = m.assign(_o=m["target"].map(order)).sort_values(["_o", "scheme", "mae_days"])
    return m[[c for c in keep if c in m.columns]].round(3)


def export(
    run_dir,
    *,
    out_dir=None,
    schemes: Sequence[str] = SCHEMES,
    n_splits: int = cv.DEFAULT_N_SPLITS,
    block_degrees: float = cv.DEFAULT_BLOCK_DEGREES,
    seed: int = 0,
    zip_name: Optional[str] = None,
) -> Path:
    """Write the package under ``<run_dir>/share_ml_template`` and zip it."""
    run_dir = Path(run_dir)
    model_dir = run_dir / "models"
    out_dir = Path(out_dir) if out_dir else run_dir / PACKAGE_DIR
    frame = cropcal_hemisphere.load_design(model_dir / "design_matrix.csv").reset_index(drop=True)
    run_predictions = pd.read_csv(model_dir / "predictions.csv", low_memory=False)

    saved = model_dir / "folds.csv"
    if saved.is_file():
        # Written by the run itself (geocif >= 0.4.1052): the folds as scored.
        folds = pd.read_csv(saved)
        built = cv.schemes_from_table(folds, [s for s in schemes if f"fold_{s}" in folds.columns])
        folds = folds[["row_id", "tile"] + [f"fold_{s}" for s in built]]
    else:
        # Older runs: rebuild, which is only valid in the run's own
        # environment (GroupKFold differs between scikit-learn versions);
        # the check below refuses a mismatch.
        built, folds = rebuild_folds(frame, schemes=schemes, n_splits=n_splits,
                                     block_degrees=block_degrees, seed=seed)
    worst = verify_folds(frame, built, run_predictions)
    # CSV round trips leave ~1e-14-day float noise; anything real is >= 1 day.
    bad = {k: v for k, v in worst.items() if not (v <= FOLD_TOLERANCE_DAYS)}
    if bad:
        raise ValueError(
            f"rebuilt folds do not reproduce the run's climatology null: {bad}. Rebuilding is only "
            f"valid in the run's own environment (scikit-learn GroupKFold changes between versions); "
            f"export from there, or from a run that saved models/folds.csv"
        )
    logger.info(f"folds verified against the run's climatology null: {worst}")

    out_dir.mkdir(parents=True, exist_ok=True)
    feature_names = list(features.FEATURE_NAMES)
    ids = frame[["key", "country", "region"]].copy()
    ids.insert(0, "row_id", np.arange(len(frame)))
    pd.concat([ids, frame[feature_names]], axis=1).to_csv(out_dir / "features.csv", index=False)

    target_cols = [c for t in features.TARGETS for c in (f"target_{t}", f"target_{t}_sin", f"target_{t}_cos")]
    targets = frame[target_cols].copy()
    targets.insert(0, "row_id", np.arange(len(frame)))
    targets.to_csv(out_dir / "targets.csv", index=False)
    folds.to_csv(out_dir / "folds.csv", index=False)

    blocks = []
    for name in built:
        block = pd.DataFrame({
            "row_id": np.arange(len(frame)), "key": frame["key"].to_numpy(), "country": frame["country"].to_numpy(),
            "crop": frame["crop"].astype(str).to_numpy(), "season": frame["season"].astype(str).to_numpy(),
            "scheme": name, "fold": folds[f"fold_{name}"].to_numpy(),
        })
        for column in PRED_COLUMNS.values():
            block[column] = np.nan
        blocks.append(block)
    pd.concat(blocks, ignore_index=True).to_csv(out_dir / "predictions_template.csv", index=False)

    metrics_path = model_dir / "metrics.csv"
    reference = _reference_scores(pd.read_csv(metrics_path)) if metrics_path.is_file() else pd.DataFrame()
    reference.to_csv(out_dir / "reference_scores.csv", index=False)
    column_dictionary().to_csv(out_dir / "columns.csv", index=False)

    manifest = {}
    manifest_path = run_dir / "run_manifest.json"
    if manifest_path.is_file():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    (out_dir / "README.md").write_text(
        _readme(frame, built, reference, manifest, n_splits=n_splits, block_degrees=block_degrees),
        encoding="utf-8",
    )

    zip_base = out_dir.parent / (zip_name or f"cropcal_ml_benchmark_{run_dir.name}")
    archive = shutil.make_archive(str(zip_base), "zip", root_dir=out_dir)
    logger.info(f"package written to {out_dir} and {archive}")
    return Path(archive)


def _headline(reference: pd.DataFrame, scheme: str) -> str:
    if reference.empty:
        return ""
    r = reference[reference["scheme"] == scheme]
    if r.empty:
        return ""
    lines = ["| model | " + " | ".join(features.TARGETS) + " |", "|---|" + "---|" * len(features.TARGETS)]
    for model_name in ("tabpfn", "tabicl", "catboost", "cubist", "climatology"):
        cells = []
        for target in features.TARGETS:
            row = r[(r["model"] == model_name) & (r["target"] == target)]
            if row.empty:
                cells.append("")
                continue
            row = row.iloc[0]
            skill = "" if pd.isna(row["skill_vs_climatology"]) else f" ({row['skill_vs_climatology']:.2f})"
            cells.append(f"{row['mae_days']:.1f}{skill}")
        lines.append(f"| {model_name} | " + " | ".join(cells) + " |")
    return "\n".join(lines)


def _readme(frame, built, reference, manifest, *, n_splits, block_degrees) -> str:
    counts = frame["crop"].astype(str).value_counts()
    crops = ", ".join(f"{c} {n}" for c, n in counts.items())
    folds_text = "\n".join(
        f"| `{name}` | {s.n_splits} | {s.description} |" for name, s in built.items()
    )
    version = manifest.get("geocif_version", "")
    return f"""# Crop-calendar prediction benchmark

Predict four crop-calendar dates for {len(frame):,} crop regions in {frame['country'].nunique()} countries
from satellite and weather climatology, on the same cross-validation folds our
models used, and send back the filled `predictions_template.csv`. We score it
with the same code and compare it with our models region by region.

Source: GEOCIF crop-calendar run `{manifest.get('finished', '')[:10]}` (geocif {version}).

## The task

Each row is one calendar region x crop x season ({crops}). The targets are the
GEOGLAM Crop Monitor calendar's four dates for that row:

| Target | Meaning |
|---|---|
| `target_planting` | planting: first day of calendar stage 1 |
| `target_midgreenup` | mid-greenup: last day of stage 1 |
| `target_midgreendown` | mid-greendown: last day of stage 2 |
| `target_harvest` | harvest: last day of stage 3 |

Days run 1-365 (1 = 1 January, non-leap year) and are **circular**: 31 December
and 1 January are 1 day apart. The calendar is recorded in half-month bins, so
each target is only known to about +/-7.5 days. Differences between models
smaller than about 8 days are not meaningful.

The features are {len(features.FEATURE_NAMES)} descriptors of a five-year daily climatology of each
region (crop-mask-weighted regional means): NDVI curve shape and timing,
growing degree days, temperature, rainfall regime and onset, ESI variability,
surface and root-zone soil moisture, dew point, elevation, and seasonal
temperature/rain/dew-point summaries. None is derived from the calendar.
Every column is defined in `columns.csv`.

## Files

| File | Rows | What it is |
|---|---|---|
| `features.csv` | {len(frame):,} | `row_id`, 3 identifier columns, then the {len(features.FEATURE_NAMES)} model inputs |
| `targets.csv` | {len(frame):,} | `row_id` and the four target days, each with its sin/cos |
| `folds.csv` | {len(frame):,} | `row_id`, the 10-degree `tile`, and the test fold of every row under each scheme |
| `predictions_template.csv` | {len(frame) * len(built):,} | one row per region x scheme; **fill the four `pred_*_doy` columns** |
| `reference_scores.csv` | | our models' scores, for comparison |
| `columns.csv` | | every column of every file: role, units, meaning |

Join everything on `row_id`.

## Cross-validation schemes

| Scheme | Folds | How regions are held out |
|---|---|---|
{folds_text}

For each scheme, and each fold k: train on every row whose `fold_<scheme>` is
not k, predict the rows where it is k. Every row gets exactly one prediction
per scheme.

- **`country_block` is required**; it is the headline comparison.
- `spatial_block` is recommended. `random` and `country` (leave-one-country-out,
  {built['country'].n_splits if 'country' in built else 'n/a'} folds) are optional; leave their `pred_*` columns empty if you skip them.
- The schemes differ in how much a test region's identical twin (a national
  calendar copied across a country's regions) sits in training: random 74%,
  spatial_block 50%, country_block 24%, country 0%. That is why `random`
  scores look much better and are not a fair comparison.

## Rules (so the comparison is fair)

1. **Fit everything inside the training folds**: imputation, scaling, feature
   selection and hyperparameter tuning. If you tune, use an inner split of the
   training rows only.
2. **Do not use as features**: `row_id`, `key`, `country`, `region`, anything
   in `targets.csv` or `folds.csv`. Do not add features built from the targets
   of other rows (nearest-neighbour or distance-to-training-point features):
   they turn the model into an interpolator of the calendar it is predicting.
3. **No outside calendar data**.
4. Categorical columns: `crop`, `season`, `cm_group`, `climate_zone`,
   `hemisphere`, `precip_regime`. `season` is a label (1, 2, 3), not a date.
5. Missing values are real gaps, not zeros: `wet2_*` is empty unless the
   region has two wet seasons; `*_available` = 0 means that data source is
   missing for the region.
6. Feature days (`doy_*`) count from **0** (0 = 1 January); target days count
   from **1**. Each `doy_*` has `_sin`/`_cos` companions; circular encodings of
   the targets are strongly recommended (ours regress sin and cos and recover
   the day with atan2).

## What to send back

`predictions_template.csv` with the `pred_*_doy` columns filled (day 1-365,
decimals fine), `row_id`/`scheme`/`fold` unchanged, plus a short note on the
model and settings. We then compute, for each target and scheme: circular MAE,
RMSE, bias, share within 15/30/45 days, share more than 60 days off, skill
against the climatology baseline (1 - MAE / MAE_climatology) with a 90%
spatial-tile bootstrap interval, and the paired MAE difference against each
of our models on the same rows.

## Our scores, `country_block` (MAE in days; skill vs climatology in brackets)

{_headline(reference, 'country_block')}

The full table, every scheme and more metrics, is `reference_scores.csv`.
"""


# --------------------------------------------------------------------------
# Scoring
# --------------------------------------------------------------------------
def validate_submission(sub: pd.DataFrame, folds: pd.DataFrame) -> list[str]:
    """Problems with a filled template; empty when it can be scored."""
    problems = []
    missing = {"row_id", "scheme", "fold", *PRED_COLUMNS.values()} - set(sub.columns)
    if missing:
        return [f"missing columns: {sorted(missing)}"]
    for scheme, part in sub.groupby("scheme"):
        column = f"fold_{scheme}"
        if column not in folds.columns:
            problems.append(f"unknown scheme {scheme!r}")
            continue
        if part["row_id"].duplicated().any():
            problems.append(f"{scheme}: duplicated row_id")
        expected = folds.set_index("row_id")[column]
        if not (part.set_index("row_id")["fold"] == expected.reindex(part["row_id"]).to_numpy()).all():
            problems.append(f"{scheme}: fold column differs from folds.csv")
        preds = part[list(PRED_COLUMNS.values())].to_numpy(dtype=float)
        if not np.isfinite(preds).any():
            continue            # a scheme left blank is skipped, not an error
        finite = preds[np.isfinite(preds)]
        if (finite < 0).any() or (finite > 366).any():
            problems.append(f"{scheme}: predictions outside 0-366")
        n_missing = int((~np.isfinite(preds)).sum())
        if n_missing:
            problems.append(f"{scheme}: {n_missing} blank predictions (scored on the rest)")
    return problems


def score(
    run_dir,
    submission_path,
    *,
    name: str = "external",
    out_dir=None,
    seed: int = 0,
) -> pd.DataFrame:
    """Score a filled template against the run's null and models.

    Writes ``metrics_<name>.csv`` (the ``metrics.csv`` layout) and
    ``paired_<name>.csv`` (``<name>`` MAE minus each in-house model's, with a
    tile-bootstrap interval; negative means ``<name>`` is better).
    """
    run_dir = Path(run_dir)
    package = run_dir / PACKAGE_DIR
    out_dir = Path(out_dir) if out_dir else package / f"scored_{name}"
    out_dir.mkdir(parents=True, exist_ok=True)
    sub = pd.read_csv(submission_path)
    folds = pd.read_csv(package / "folds.csv")
    problems = validate_submission(sub, folds)
    fatal = [p for p in problems if "blank predictions" not in p]
    if fatal:
        raise ValueError(f"submission cannot be scored: {fatal}")
    for problem in problems:
        logger.warning(problem)

    ours = pd.read_csv(run_dir / "models" / "predictions.csv", low_memory=False)
    clim = ours[ours["model"] == models.CLIMATOLOGY]
    blocks = []
    for (scheme, target), ref in clim.groupby(["scheme", "target"]):
        part = sub[sub["scheme"] == scheme]
        if part.empty or not np.isfinite(part[PRED_COLUMNS[target]].to_numpy(dtype=float)).any():
            continue
        block = ref.drop(columns=["predicted"]).merge(
            part[["row_id", PRED_COLUMNS[target]]].rename(columns={PRED_COLUMNS[target]: "predicted"}),
            on="row_id", how="left",
        )
        block["model"], block["encoding"], block["resultant"], block["null_level"] = name, "external", np.nan, ""
        blocks.append(block)
    if not blocks:
        raise ValueError("no scheme in the submission has predictions")
    theirs = pd.concat(blocks, ignore_index=True)
    combined = pd.concat([theirs, clim[clim["scheme"].isin(theirs["scheme"].unique())]], ignore_index=True)
    metrics = models.summarise_predictions(combined, seed=seed)
    metrics = metrics[metrics["model"] == name]
    metrics.to_csv(out_dir / f"metrics_{name}.csv", index=False)

    records = []
    in_house = ours[~ours["model"].isin([models.CLIMATOLOGY])]
    for (model_name, scheme, target), a in in_house.groupby(["model", "scheme", "target"]):
        if model_name == models.BASELINE:
            b = theirs[(theirs["target"] == target) & (theirs["scheme"] == "country_block")]
            scheme = "country_block"
        else:
            b = theirs[(theirs["target"] == target) & (theirs["scheme"] == scheme)]
        if b.empty:
            continue
        stats = cropcal_hemisphere.paired_difference(a, b, seed=seed)
        records.append({"versus": model_name, "scheme": scheme, "target": target, "n": stats["n"],
                        "mae_versus": stats["mae_a"], f"mae_{name}": stats["mae_b"],
                        "d_mae": stats["d_mae"], "d_mae_ci_low": stats["d_mae_ci_low"],
                        "d_mae_ci_high": stats["d_mae_ci_high"]})
    paired = pd.DataFrame(records)
    paired.to_csv(out_dir / f"paired_{name}.csv", index=False)
    logger.info(f"scored {name}: {out_dir}")
    return metrics
