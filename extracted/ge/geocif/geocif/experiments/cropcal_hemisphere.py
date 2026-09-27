"""Does fitting one model per hemisphere beat one pooled model? (crop calendars)

The calendar models are fitted on every region at once, with ``hemisphere``,
``lat`` and ``abs_lat`` among the features. The alternative tested here fits a
separate northern and southern model in every fold and predicts each test row
with its own hemisphere's model. Everything else is held fixed so the two arms
are paired row for row: the same design matrix, the same folds (same seed),
the same features and the same out-of-fold climatology null.

Hemisphere comes from the region's centroid latitude, NOT from the zone
file's ``hemisphere`` column: that column is wrong for 123 of the 1,354 design
rows (Ethiopia, Sudan, South Sudan, Eritrea, Yemen, Cote d'Ivoire, Sri Lanka,
CAR and part of DRC marked S; Gabon, Timor-Leste and part of Kenya marked N).
Splitting on it would test the wrong split. The corrected label replaces the
column in BOTH arms, so the pooled model's ``hemisphere`` feature and the
climatology null see the same labels as the split. The published run with the
zone-file labels can be passed as ``reference`` to show what the label fix
alone does.

Usage (on the cluster; each arm can run as its own process)::

    from geocif.experiments import cropcal_hemisphere
    cropcal_hemisphere.run(design, arm="pooled")
    cropcal_hemisphere.run(design, arm="stratified")    # compares once both exist

Outputs, under ``out_dir`` (default ``<run>/experiments/hemisphere``):

    predictions_<arm>.csv       out-of-fold days, the models' predictions format
    metrics_<arm>.csv           models.summarise_predictions for that arm
    comparison.csv              paired stratified - pooled MAE, tile-bootstrap
                                interval, by target x scheme x model x subset
    comparison.png              the same table as a figure (companion CSV above)
    label_fix.csv               pooled (latitude labels) - published run (zone
                                labels), when ``reference`` is given
"""
from __future__ import annotations

import logging
import sys
from pathlib import Path
from typing import Optional, Sequence

import numpy as np
import pandas as pd

from geocif.cropcal import circular, cv, features, models

logger = logging.getLogger(__name__)

ARMS = ("pooled", "stratified")
DEFAULT_MODELS = ("catboost", "tabpfn")
DEFAULT_SCHEMES = ("spatial_block", "country_block")

#: The band where "hemisphere" says least about the season: a region at 2 N
#: has more in common with one at 2 S than with one at 40 N.
TROPICAL_BAND_DEGREES = 10.0

BOOTSTRAP_RESAMPLES = 2000
BOOTSTRAP_LEVEL = 0.90


def latitude_hemisphere(lat) -> np.ndarray:
    """Vectorised :func:`geocif.cropcal.features.latitude_hemisphere` (the equator is N)."""
    return np.array([features.latitude_hemisphere(value) for value in np.atleast_1d(lat)], dtype=object)


def load_design(path) -> pd.DataFrame:
    """Read a saved design matrix back into the dtypes ``models.evaluate`` expects.

    A CSV round trip turns ``season`` into integers and can turn a boolean
    column holding NaN into strings, and ``"False"`` is truthy. The zone-file
    hemisphere is kept as ``hemisphere_zone`` (when the matrix predates that
    column) and ``hemisphere`` is set to the latitude sign.
    """
    frame = pd.read_csv(path, low_memory=False)
    for name in features.CATEGORICAL_FEATURES:
        if name in frame.columns:
            frame[name] = frame[name].where(frame[name].isna(), frame[name].astype(str))
    for name in ("calendar_wall_to_wall", "calendar_wraps_year"):
        if name in frame.columns and frame[name].dtype != bool:
            frame[name] = frame[name].map({True: True, False: False, "True": True, "False": False}).eq(True)
    # A matrix built by geocif >= 0.4.1051 already carries both; older ones
    # carry only the zone label in ``hemisphere``.
    if "hemisphere_zone" not in frame.columns:
        frame["hemisphere_zone"] = frame["hemisphere"]
    frame["hemisphere"] = latitude_hemisphere(frame["lat"])
    return frame


def _subsets(frame: pd.DataFrame) -> dict[str, np.ndarray]:
    """Row masks the comparison is reported on."""
    hemi = frame["hemisphere"].astype(str).to_numpy()
    tropical = np.abs(frame["lat"].to_numpy(dtype=float)) < TROPICAL_BAND_DEGREES
    relabelled = hemi != frame["hemisphere_zone"].astype(str).to_numpy()
    return {
        "all": np.ones(len(frame), bool),
        "north": hemi == "N",
        "south": hemi == "S",
        f"tropics_abs_lat_lt_{TROPICAL_BAND_DEGREES:g}": tropical,
        f"extratropics_abs_lat_ge_{TROPICAL_BAND_DEGREES:g}": ~tropical,
        "relabelled": relabelled,
    }


def paired_difference(
    a: pd.DataFrame, b: pd.DataFrame, *, seed: int = 0, resamples: int = BOOTSTRAP_RESAMPLES
) -> dict:
    """MAE of ``b`` minus MAE of ``a`` on common rows, with a paired tile bootstrap.

    Negative means ``b`` is better. The bootstrap resamples spatial tiles, as
    the skill interval in :mod:`geocif.cropcal.models` does, because
    neighbouring regions are not independent.
    """
    merged = a[["row_id", "tile", "predicted", "observed"]].merge(
        b[["row_id", "predicted"]].rename(columns={"predicted": "predicted_b"}), on="row_id", how="inner"
    )
    merged = merged[
        np.isfinite(merged["predicted"]) & np.isfinite(merged["predicted_b"]) & np.isfinite(merged["observed"])
    ]
    out = {"n": int(len(merged)), "mae_a": np.nan, "mae_b": np.nan, "d_mae": np.nan,
           "d_mae_ci_low": np.nan, "d_mae_ci_high": np.nan, "share_b_better": np.nan}
    if merged.empty:
        return out
    gap_a = np.array([circular.circular_gap(p, o) for p, o in zip(merged["predicted"], merged["observed"])])
    gap_b = np.array([circular.circular_gap(p, o) for p, o in zip(merged["predicted_b"], merged["observed"])])
    out.update(mae_a=float(gap_a.mean()), mae_b=float(gap_b.mean()), d_mae=float(gap_b.mean() - gap_a.mean()),
               share_b_better=float(np.mean(gap_b < gap_a)))

    tiles, tile_id = np.unique(merged["tile"].astype(str).to_numpy(), return_inverse=True)
    if tiles.size < 2 or resamples <= 0:
        return out
    diff = np.bincount(tile_id, weights=gap_b - gap_a, minlength=tiles.size)
    count = np.bincount(tile_id, minlength=tiles.size).astype(float)
    rng = np.random.default_rng(seed)
    weights = rng.multinomial(tiles.size, np.full(tiles.size, 1.0 / tiles.size), size=resamples).astype(float)
    with np.errstate(all="ignore"):
        boot = (weights @ diff) / (weights @ count)
    boot = boot[np.isfinite(boot)]
    if boot.size:
        alpha = (1.0 - BOOTSTRAP_LEVEL) / 2.0
        out["d_mae_ci_low"] = float(np.quantile(boot, alpha))
        out["d_mae_ci_high"] = float(np.quantile(boot, 1.0 - alpha))
    return out


def compare(
    first: pd.DataFrame,
    second: pd.DataFrame,
    frame: pd.DataFrame,
    *,
    labels: tuple[str, str] = ("pooled", "stratified"),
    seed: int = 0,
    resamples: int = BOOTSTRAP_RESAMPLES,
) -> pd.DataFrame:
    """Paired ``second - first`` MAE per target x scheme x model x subset.

    The climatology null is included as a model so its (identical) rows show
    a zero difference -- a check that the two arms really share their folds.
    """
    subsets = _subsets(frame)
    records = []
    keys = ["model", "target", "scheme"]
    second_groups = {k: g for k, g in second.groupby(keys)}
    for key, part_a in first.groupby(keys):
        part_b = second_groups.get(key)
        if part_b is None:
            continue
        for subset, mask in subsets.items():
            rows = np.flatnonzero(mask)
            a = part_a[part_a["row_id"].isin(rows)]
            b = part_b[part_b["row_id"].isin(rows)]
            record = dict(zip(keys, key))
            record["subset"] = subset
            stats = paired_difference(a, b, seed=seed, resamples=resamples)
            record.update({
                "n": stats["n"],
                f"mae_{labels[0]}": stats["mae_a"],
                f"mae_{labels[1]}": stats["mae_b"],
                "d_mae": stats["d_mae"],
                "d_mae_ci_low": stats["d_mae_ci_low"],
                "d_mae_ci_high": stats["d_mae_ci_high"],
                f"share_{labels[1]}_better": stats["share_b_better"],
            })
            records.append(record)
    out = pd.DataFrame(records)
    if out.empty:
        return out
    out["ci_excludes_zero"] = (out["d_mae_ci_low"] > 0) | (out["d_mae_ci_high"] < 0)
    return out.sort_values(["scheme", "model", "target", "subset"]).reset_index(drop=True)


def plot_comparison(table: pd.DataFrame, path: Path) -> list[tuple[str, str]]:
    """ΔMAE (stratified - pooled) per target, by hemisphere; one panel per scheme x model.

    The climatology null and the rule-based baseline are identical in both arms
    (the rule has no folds at all), so they get no panel. Returns the
    ``(scheme, model)`` panels drawn.
    """
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    shown = table[
        ~table["model"].isin([models.CLIMATOLOGY, models.BASELINE])
        & (table["scheme"] != "none")
        & table["subset"].isin(["all", "north", "south"])
    ]
    if shown.empty:
        return []
    schemes = list(dict.fromkeys(shown["scheme"]))
    model_names = list(dict.fromkeys(shown["model"]))
    targets = [t for t in features.TARGETS if t in set(shown["target"])]
    subset_style = {"all": ("All Regions", "#4d4d4d"), "north": ("North", "#2166ac"), "south": ("South", "#b2182b")}
    target_label = {"planting": "Planting", "midgreenup": "Mid-Greenup", "midgreendown": "Mid-Greendown", "harvest": "Harvest"}
    scheme_label = {"spatial_block": "Spatial Block", "country_block": "Country Block", "country": "Country", "random": "Random"}
    model_label = {"catboost": "CatBoost", "tabpfn": "TabPFN", "tabicl": "TabICL", "cubist": "Cubist"}

    fig, axes = plt.subplots(len(schemes), len(model_names), figsize=(4.6 * len(model_names), 3.4 * len(schemes)),
                             sharey=True, squeeze=False)
    width = 0.26
    x = np.arange(len(targets))
    for i, scheme in enumerate(schemes):
        for j, model in enumerate(model_names):
            ax = axes[i, j]
            for k, (subset, (label, colour)) in enumerate(subset_style.items()):
                part = shown[(shown["scheme"] == scheme) & (shown["model"] == model) & (shown["subset"] == subset)]
                part = part.set_index("target").reindex(targets)
                y = part["d_mae"].to_numpy(dtype=float)
                err = np.vstack([y - part["d_mae_ci_low"].to_numpy(dtype=float),
                                 part["d_mae_ci_high"].to_numpy(dtype=float) - y])
                ax.bar(x + (k - 1) * width, y, width, yerr=err, color=colour, label=label,
                       capsize=2, error_kw={"lw": 0.8})
            ax.axhline(0.0, color="black", lw=0.8)
            ax.set_xticks(x, [target_label.get(t, t) for t in targets], rotation=20)
            ax.set_title(f"{model_label.get(model, model)}, {scheme_label.get(scheme, scheme)}")
            if j == 0:
                ax.set_ylabel("Δ MAE (Days)")
    axes[0, -1].legend(frameon=False, fontsize=8)
    fig.suptitle("Per-Hemisphere Minus Pooled Model")
    fig.tight_layout()
    fig.savefig(path, dpi=200)
    plt.close(fig)
    return [(scheme, model) for scheme in schemes for model in model_names]


def _default_out_dir(design_path: Path) -> Path:
    return design_path.resolve().parent.parent / "experiments" / "hemisphere"


def run(
    design_path,
    *,
    arm: str = "both",
    out_dir=None,
    model_names: Sequence[str] = DEFAULT_MODELS,
    scheme_names: Sequence[str] = DEFAULT_SCHEMES,
    targets: Sequence[str] = features.TARGETS,
    n_splits: int = cv.DEFAULT_N_SPLITS,
    block_degrees: float = cv.DEFAULT_BLOCK_DEGREES,
    seed: int = 0,
    min_stratum_rows: int = models.MIN_STRATUM_ROWS,
    reference: Optional[str] = None,
) -> Optional[pd.DataFrame]:
    """Run one arm (or both) and compare once both arms' predictions exist.

    Args:
        design_path: a run's ``models/design_matrix.csv``.
        arm: ``"pooled"``, ``"stratified"`` or ``"both"``.
        reference: a run's ``models/predictions.csv`` fitted with the zone-file
            labels; defaults to the one beside ``design_path`` when present.
    """
    if not logging.getLogger().handlers:
        logging.basicConfig(level=logging.INFO, stream=sys.stdout,
                            format="%(asctime)s %(name)s %(levelname)s %(message)s")
    design_path = Path(design_path)
    out_dir = Path(out_dir) if out_dir else _default_out_dir(design_path)
    out_dir.mkdir(parents=True, exist_ok=True)
    arms = ARMS if arm == "both" else (arm,)
    unknown = set(arms) - set(ARMS)
    if unknown:
        raise ValueError(f"unknown arm(s) {sorted(unknown)}; use one of {ARMS} or 'both'")

    frame = load_design(design_path).reset_index(drop=True)
    n_moved = int((frame["hemisphere"] != frame["hemisphere_zone"]).sum())
    logger.info(
        f"{len(frame)} design rows; latitude hemisphere N={int((frame['hemisphere'] == 'N').sum())} "
        f"S={int((frame['hemisphere'] == 'S').sum())}; {n_moved} rows relabelled from the zone file"
    )
    schemes = cv.build_schemes(frame, n_splits=n_splits, block_degrees=block_degrees, seed=seed, names=scheme_names)

    for name in arms:
        logger.info(f"arm {name}: models {list(model_names)}, schemes {list(schemes)}")
        evaluation = models.evaluate(
            frame,
            models=model_names,
            targets=targets,
            schemes=schemes,
            encodings=("sincos",),
            seed=seed,
            n_splits=n_splits,
            block_degrees=block_degrees,
            stratify_by="hemisphere" if name == "stratified" else None,
            min_stratum_rows=min_stratum_rows,
        )
        evaluation.predictions.to_csv(out_dir / f"predictions_{name}.csv", index=False)
        evaluation.metrics.to_csv(out_dir / f"metrics_{name}.csv", index=False)
        pd.DataFrame({"failure": evaluation.failures}).to_csv(out_dir / f"failures_{name}.csv", index=False)
        pd.DataFrame({"note": evaluation.notes}).to_csv(out_dir / f"notes_{name}.csv", index=False)
        logger.info(f"arm {name}: {len(evaluation.predictions)} prediction rows, {len(evaluation.failures)} failures")

    paths = {name: out_dir / f"predictions_{name}.csv" for name in ARMS}
    if not all(p.is_file() for p in paths.values()):
        logger.info(f"waiting for the other arm before comparing: {[str(p) for p in paths.values() if not p.is_file()]}")
        return None

    pooled, stratified = (pd.read_csv(paths[name], low_memory=False) for name in ARMS)
    table = compare(pooled, stratified, frame, seed=seed)
    table.to_csv(out_dir / "comparison.csv", index=False)
    plot_comparison(table, out_dir / "comparison.png")

    reference = Path(reference) if reference else design_path.parent / "predictions.csv"
    if reference.is_file():
        published = pd.read_csv(reference, low_memory=False)
        published = published[published["scheme"].isin(list(schemes)) & (published["encoding"].isin(["sincos", "none"]))]
        published = published[published["model"].isin(list(model_names) + [models.CLIMATOLOGY])]
        # Row ids pair the runs only if both enumerate the same design rows.
        keyed = published.drop_duplicates("row_id").set_index("row_id")["key"].astype(str)
        in_range = keyed.index[keyed.index < len(frame)]
        aligned = len(in_range) == len(keyed) and (keyed.loc[in_range].to_numpy() == frame["key"].astype(str).to_numpy()[in_range]).all()
        if aligned:
            label_fix = compare(published, pooled, frame, labels=("zone_labels", "latitude_labels"), seed=seed)
            label_fix.to_csv(out_dir / "label_fix.csv", index=False)
        else:
            logger.warning(f"{reference} does not enumerate the same design rows; label_fix.csv not written")

    headline = table[(table["subset"].isin(["all", "north", "south"])) & (table["model"] != models.CLIMATOLOGY)]
    with pd.option_context("display.width", 200, "display.max_rows", 200):
        print(headline.round(2).to_string(index=False))
    logger.info(f"comparison written to {out_dir}")
    return table
