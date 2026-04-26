"""Experiments Runner.

Runs model comparison, CID ablation, region filtering, and Optuna
hyperparameter search experiments. Results are stored in a dedicated
experiments database and analysis folder.

Usage::

    from geocif import experiments
    experiments.run(cfg_geocif, n_trials=30)
"""

import ast
import os
import sqlite3
import warnings
from pathlib import Path

import arrow as ar
import matplotlib.pyplot as plt
import numpy as np
import optuna
import pandas as pd
import seaborn as sns
import sklearn

import scienceplots  # noqa: F401

from geocif import geocif_runner as gc
from geocif import logger as log
from geocif import utils as ut

# Shared fixed palette for model/experiment colors
_FIXED_PALETTE = [
    (0.122, 0.467, 0.706, 1.0),  # steel blue
    (0.839, 0.153, 0.157, 1.0),  # brick red
    (0.173, 0.627, 0.173, 1.0),  # forest green
    (0.580, 0.404, 0.741, 1.0),  # muted purple
    (1.000, 0.498, 0.055, 1.0),  # orange
    (0.549, 0.337, 0.294, 1.0),  # brown
    (0.890, 0.467, 0.761, 1.0),  # pink
    (0.498, 0.498, 0.498, 1.0),  # grey
]


def _fmt(name: str) -> str:
    """Format a param_value that might be a model name for display."""
    return ut.display_model_name(name)

# Show usage info on import
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

_console = Console()
_table = Table(show_header=False, box=None, padding=(0, 1))
_table.add_column(style="bold cyan", no_wrap=True)
_table.add_column()
_table.add_row("Usage", "from geocif import experiments; experiments.run(cfg)")
_table.add_row("cfg", "\\[geobase.txt, countries.txt, crops.txt, geocif.txt]")
_console.print(Panel(_table, title="[bold bright_white]GeoCIF Experiments Runner[/]", border_style="bright_blue", padding=(1, 2)))

import scienceplots  # noqa: F401 — required to register the 'science' style (SciencePlots ≥2.0.0)
# Note: scienceplots style is applied per-plot via plt.style.context() in
# diagnostic functions, not globally — avoids affecting maps and heatmaps.
sklearn.set_config(transform_output="pandas")
warnings.simplefilter(action="ignore", category=FutureWarning)


def _save_config(parser, dir_plots):
    """Save current parser config as INI file alongside plots."""
    with open(dir_plots / "config.ini", "w") as f:
        parser.write(f)


def _get_obs_pred_cols(df):
    """Return (obs_col_name, pred_col_name) or (None, None)."""
    obs = [c for c in df.columns if c.startswith("Observed") and "Yield" in c]
    pred = [c for c in df.columns if c.startswith("Predicted") and "Yield" in c]
    if obs and pred:
        return obs[0], pred[0]
    return None, None


def _compute_ape(df):
    """Add 'APE' column, return filtered df with only valid rows."""
    obs_col, pred_col = _get_obs_pred_cols(df)
    if not obs_col:
        return pd.DataFrame()
    obs, pred = df[obs_col], df[pred_col]
    valid = obs.notna() & pred.notna() & (obs != 0)
    result = df[valid].copy()
    result["APE"] = np.abs((obs[valid] - pred[valid]) / obs[valid]) * 100
    return result


def _filter_experiment(df, experiment_name):
    """Filter to a single experiment, return copy."""
    return df[df["experiment"] == experiment_name].copy()


def _order_by_production(pivot, prod_pct, ascending=True):
    """Sort pivot rows by production %, relabel index with pct suffix."""
    if not prod_pct:
        return pivot
    pivot["_pct"] = pivot.index.map(lambda r: prod_pct.get(r, 0))
    pivot = pivot.sort_values("_pct", ascending=ascending)
    pivot.index = [f"{r} ({prod_pct.get(r, 0):.1f}%)" for r in pivot.index]
    return pivot.drop(columns=["_pct"])


def main(inputs, logger, parser, section, item, values):
    original_value = parser.get(section, item)

    for value in values:
        # Each value gets a unique experiment name for tracking
        parser.set("DEFAULT", "experiment_name", f"{section}_{item}_{value}")
        parser.set(section, item, str(value))
        gc.execute_models(inputs, logger, parser,
                          desc=f"{section}.{item} = {value}")

    parser.set(section, item, str(original_value))

    return parser


def main_models(logger, parser, models):
    """Run model comparison experiment by overriding per-country models list."""
    import ast

    countries = ast.literal_eval(parser.get("DEFAULT", "countries"))

    # Save original models for each country
    originals = {c: parser.get(c, "models") for c in countries}

    for model in models:
        parser.set("DEFAULT", "experiment_name", "model_comparison")
        # Override every country's models list to just this one model
        for country in countries:
            parser.set(country, "models", f'["{model}"]')

        inputs = gc.gather_inputs(parser)
        gc.execute_models(inputs, logger, parser,
                          desc=f"Exp 0: model_comparison — {model}")

    # Restore originals
    for country, orig in originals.items():
        parser.set(country, "models", orig)

    return parser


def _get_best_models_from_exp0(parser, model_experiment):
    """Determine best model per country from Experiment 0 results.

    Returns dict: {country: best_model_name}. Falls back to first model if
    no results are available.
    """
    exp_list = [("models", "model_comparison", "", "str", model_experiment)]
    df = _load_experiment_results(parser, exp_list)
    if df.empty:
        countries = ast.literal_eval(parser.get("DEFAULT", "countries"))
        return {c: model_experiment[0] for c in countries}

    df = _compute_ape(df)
    if df.empty:
        countries = ast.literal_eval(parser.get("DEFAULT", "countries"))
        return {c: model_experiment[0] for c in countries}
    df["_ape"] = df["APE"]

    best = (
        df.groupby(["Country", "param_value"])["_ape"]
        .mean()
        .reset_index()
        .loc[lambda d: d.groupby("Country")["_ape"].idxmin()]
    )

    result = {row["Country"]: row["param_value"] for _, row in best.iterrows()}

    # Fill missing countries with first model
    countries = ast.literal_eval(parser.get("DEFAULT", "countries"))
    for c in countries:
        if c not in result:
            result[c] = model_experiment[0]

    return result


def experiment_2_region_filter(logger, parser, best_models):
    """Experiment 2: Exclude low-production / data-sparse regions, retrain+test on rest."""
    countries = ast.literal_eval(parser.get("DEFAULT", "countries"))
    orig_models = {c: parser.get(c, "models") for c in countries}
    orig_experiment_name = parser.get("DEFAULT", "experiment_name")

    for country, model in best_models.items():
        parser.set(country, "models", f'["{model}"]')

    parser.set("DEFAULT", "experiment_name", "region_filter")
    parser.set("DEFAULT", "filter_low_production_regions", "True")

    inputs = gc.gather_inputs(parser)
    gc.execute_models(inputs, logger, parser, desc="Exp 2: region_filter")

    # Restore originals
    parser.set("DEFAULT", "filter_low_production_regions", "False")
    parser.set("DEFAULT", "experiment_name", orig_experiment_name)
    for country, orig in orig_models.items():
        parser.set(country, "models", orig)

    return parser


def experiment_1_cid_ablation(logger, parser, best_models, all_cids):
    """Experiment 1: Run each CID type individually using the best model per country."""
    countries = ast.literal_eval(parser.get("DEFAULT", "countries"))

    # Save originals — use_cids lives in [DEFAULT], not [ML]
    orig_use_cids = parser.get("DEFAULT", "use_cids")
    orig_experiment_name = parser.get("ML", "experiment_name")
    orig_models = {c: parser.get(c, "models") for c in countries}

    # Set best model per country
    for country, model in best_models.items():
        parser.set(country, "models", f'["{model}"]')

    for cid in all_cids:
        logger.info(f"  CID ablation: {cid}")
        parser.set("ML", "experiment_name", f"cid_{cid}")
        parser.set("DEFAULT", "use_cids", f'["{cid}"]')

        inputs = gc.gather_inputs(parser)
        gc.execute_models(inputs, logger, parser,
                          desc=f"Exp 1: cid_ablation — {cid}")

    # Restore originals
    parser.set("DEFAULT", "use_cids", orig_use_cids)
    parser.set("ML", "experiment_name", orig_experiment_name)
    for country, orig in orig_models.items():
        parser.set(country, "models", orig)

    return parser


# ---------------------------------------------------------------------------
# Bayesian hyperparameter optimization (Optuna TPE)
# ---------------------------------------------------------------------------

def _extract_trial_mape(parser, experiment_name):
    """Extract mean APE for a specific experiment trial from the results DB."""
    dir_output = Path(parser.get("PATHS", "dir_output"))
    project_name = parser.get("DEFAULT", "project_name")
    db_name = parser.get("DEFAULT", "db")
    db_path = dir_output / project_name / "ml" / "db" / db_name

    if not db_path.exists():
        return float("inf")

    con = sqlite3.connect(db_path)
    tables = pd.read_sql(
        "SELECT name FROM sqlite_master WHERE type='table' "
        "AND name NOT LIKE 'config%' AND name != 'models'",
        con,
    )

    ape_values = []
    for table in tables["name"]:
        try:
            df = pd.read_sql(
                f'SELECT APE FROM "{table}" WHERE "Experiment Name" = ?',
                con, params=(experiment_name,),
            )
            if not df.empty:
                valid = df["APE"].dropna()
                ape_values.extend(valid.tolist())
        except Exception:
            continue
    con.close()

    return float(np.mean(ape_values)) if ape_values else float("inf")


def _all_cid_types():
    """Canonical list of CID category labels present in cid/definitions.py."""
    from geocif.cid import definitions as di
    types = set()
    for d in (
        di.dict_indices, di.dict_ndvi, di.dict_gcvi, di.dict_esi4wk,
        di.dict_hindex, di.dict_aef, di.dict_fldas,
    ):
        for v in d.values():
            types.add(v[0])
    return sorted(types)


def _all_cid_indices():
    """Canonical list of individual CID index names from cid/definitions.py."""
    from geocif.cid import definitions as di
    keys = []
    for d in (
        di.dict_indices, di.dict_ndvi, di.dict_gcvi, di.dict_esi4wk,
        di.dict_hindex, di.dict_aef, di.dict_fldas,
    ):
        keys.extend(d.keys())
    return sorted(set(keys))


def _optimize_cid_subset(mode, inputs, logger, parser, n_trials=30,
                        min_size=1, max_size=None):
    """Optuna TPE search over subsets of CID ``Type`` or ``Index`` values.

    Each trial samples a binary inclusion flag per CID label.  The resulting
    subset is written to ``ML.use_cids`` / ``ML.select_cid_by`` and the
    pipeline runs once per trial; MAPE is extracted from the results DB via
    ``_extract_trial_mape``.

    Args:
        mode: ``"Type"`` (category-level, ~12 flags) or ``"Index"``
            (individual indices, ~100 flags).
        min_size: trials with fewer than this many selected labels are
            pruned (return inf) so Optuna learns to avoid empty subsets.
        max_size: optional cap.  Leave None for ``Type`` (small space);
            set e.g. 25 for ``Index`` to keep models trainable.
    """
    if mode not in ("Type", "Index"):
        raise ValueError(f"mode must be 'Type' or 'Index', got {mode!r}")

    labels = _all_cid_types() if mode == "Type" else _all_cid_indices()
    logger.info(f"CID subset search ({mode}) over {len(labels)} labels, {n_trials} trials")

    model_names = sorted(set(inp[4] for inp in inputs))
    model_tag = "_".join(model_names)
    tag = "cid_types" if mode == "Type" else "cid_indices"

    # Snapshot original values so we can restore after the study.
    originals = {
        key: parser.get("ML", key)
        for key in ("select_cid_by", "use_cids")
        if parser.has_option("ML", key)
    }
    # select_cid_by / use_cids can also live on [DEFAULT]; snapshot those too.
    default_originals = {
        key: parser.get("DEFAULT", key)
        for key in ("select_cid_by", "use_cids")
        if parser.has_option("DEFAULT", key)
    }

    def objective(trial):
        flags = [
            trial.suggest_categorical(f"{tag}__{label}", [True, False])
            for label in labels
        ]
        selected = [label for label, keep in zip(labels, flags) if keep]
        n = len(selected)
        if n < min_size or (max_size is not None and n > max_size):
            # Invalid subset — tell Optuna this is a bad region.
            return float("inf")

        experiment_name = f"{tag}_{model_tag}_trial{trial.number + 1}"
        parser.set("DEFAULT", "experiment_name", experiment_name)
        # Write to DEFAULT so per-country sections inherit — mirrors how
        # experiment_1_cid_ablation sets the subset.
        parser.set("DEFAULT", "select_cid_by", mode)
        parser.set("DEFAULT", "use_cids", str(selected))

        try:
            gc.execute_models(inputs, logger, parser,
                              desc=f"Optuna {tag} trial {trial.number + 1} (n={n})")
        except Exception as e:
            logger.warning(f"Trial {trial.number} ({tag}, n={n}) failed: {e}")
            return float("inf")

        mape = _extract_trial_mape(parser, experiment_name)
        logger.info(f"Trial {trial.number}: {tag} n={n} MAPE={mape:.2f}%")
        return mape

    optuna.logging.set_verbosity(optuna.logging.WARNING)
    study = optuna.create_study(
        sampler=optuna.samplers.TPESampler(seed=42),
        direction="minimize",
        study_name=f"geocif_{tag}",
    )
    study.optimize(objective, n_trials=n_trials)

    # Restore originals so subsequent stages see untouched config.
    for key, value in originals.items():
        parser.set("ML", key, value)
    for key, value in default_originals.items():
        parser.set("DEFAULT", key, value)

    best = study.best_trial
    logger.info(f"{tag} search complete — best trial {best.number}, MAPE {best.value:.2f}%")
    best_selected = [
        label for label in labels
        if best.params.get(f"{tag}__{label}", False)
    ]
    logger.info(f"  Best {mode} subset ({len(best_selected)}): {best_selected}")

    return study


def optimize_hyperparameters(inputs, logger, parser, n_trials=30):
    """Use Optuna TPE to find the best ML hyperparameter combination."""
    # Build model tag from unique models in the inputs list
    model_names = sorted(set(inp[4] for inp in inputs))
    model_tag = "_".join(model_names)

    ml_keys = [
        "feature_selection", "lag_years", "lag_yield_as_feature",
        "check_yield_trend",
        "use_spatial_neighbors", "spatial_neighbor_method", "spatial_neighbor_k",
    ]
    originals = {
        key: parser.get("ML", key)
        for key in ml_keys
        if parser.has_option("ML", key)
    }

    def objective(trial):
        params = {
            "feature_selection": trial.suggest_categorical(
                "feature_selection",
                ["SelectKBest", "gOMP", "none"],
            ),
            "lag_years": trial.suggest_int("lag_years", 1, 5),
            "lag_yield_as_feature": trial.suggest_categorical(
                "lag_yield_as_feature", ["True", "False"],
            ),
            "check_yield_trend": trial.suggest_categorical(
                "check_yield_trend", ["True", "False"],
            ),
            "use_spatial_neighbors": trial.suggest_categorical(
                "use_spatial_neighbors", ["True", "False"],
            ),
            "spatial_neighbor_method": trial.suggest_categorical(
                "spatial_neighbor_method", ["knn", "full"],
            ),
            "spatial_neighbor_k": trial.suggest_int("spatial_neighbor_k", 2, 8),
        }

        experiment_name = f"exp0_{model_tag}_trial{trial.number + 1}"
        parser.set("DEFAULT", "experiment_name", experiment_name)
        for key, value in params.items():
            parser.set("ML", key, str(value))

        try:
            gc.execute_models(inputs, logger, parser,
                              desc=f"Optuna HP trial {trial.number + 1}")
        except Exception as e:
            logger.warning(f"Trial {trial.number} failed: {e}")
            return float("inf")

        mape = _extract_trial_mape(parser, experiment_name)
        logger.info(
            f"Trial {trial.number}: MAPE={mape:.2f}% | "
            + ", ".join(f"{k}={v}" for k, v in params.items())
        )
        return mape

    optuna.logging.set_verbosity(optuna.logging.WARNING)
    study = optuna.create_study(
        sampler=optuna.samplers.TPESampler(seed=42),
        direction="minimize",
        study_name="geocif_hyperopt",
    )
    study.optimize(objective, n_trials=n_trials)

    # Restore original ML values
    for key, value in originals.items():
        parser.set("ML", key, value)

    # Log best result
    best = study.best_trial
    logger.info(f"Optimization complete — best trial: {best.number}")
    logger.info(f"Best MAPE: {best.value:.2f}%")
    for k, v in best.params.items():
        logger.info(f"  {k}: {v}")

    return study


def analyze_optimization(parser, study, logger):
    """Generate optimization analysis: CSV of all trials and diagnostic plots."""
    dir_output = Path(parser.get("PATHS", "dir_output"))
    project_name = parser.get("DEFAULT", "project_name")
    today = ar.utcnow().to("America/New_York").format("MMMM_DD_YYYY")
    dir_plots = dir_output / project_name / "ml" / "optimization" / today
    os.makedirs(dir_plots, exist_ok=True)
    _save_config(parser, dir_plots)

    # Save all trials to CSV
    df_trials = study.trials_dataframe()
    df_trials.to_csv(dir_plots / "optuna_trials.csv", index=False)
    logger.info(f"Saved {len(df_trials)} trials to {dir_plots / 'optuna_trials.csv'}")

    # Save best params
    best = study.best_trial
    best_row = {"trial": best.number, "mape": best.value, **best.params}
    pd.DataFrame([best_row]).to_csv(dir_plots / "best_params.csv", index=False)
    logger.info(f"Best params saved to {dir_plots / 'best_params.csv'}")

    # Convergence plot
    values = [t.value for t in study.trials if t.value < float("inf")]
    if values:
        best_so_far = np.minimum.accumulate(values)
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(range(len(values)), values, "o", alpha=0.4, label="Trial MAPE")
        ax.plot(range(len(best_so_far)), best_so_far, "r-", linewidth=2, label="Best so far")
        ax.set_xlabel("Trial")
        ax.set_ylabel("MAPE (%)")
        ax.set_title("Optimization Convergence")
        ax.legend()
        plt.tight_layout()
        fig.savefig(dir_plots / "convergence.png", dpi=250)
        plt.close(fig)

    # Optuna built-in diagnostic plots
    try:
        from optuna.visualization.matplotlib import (
            plot_optimization_history,
            plot_param_importances,
            plot_parallel_coordinate,
        )

        ax = plot_optimization_history(study)
        ax.get_figure().savefig(
            dir_plots / "optimization_history.png", dpi=250, bbox_inches="tight"
        )
        plt.close("all")

        ax = plot_param_importances(study)
        ax.get_figure().savefig(
            dir_plots / "param_importances.png", dpi=250, bbox_inches="tight"
        )
        plt.close("all")

        ax = plot_parallel_coordinate(study)
        ax.get_figure().savefig(
            dir_plots / "parallel_coordinate.png", dpi=250, bbox_inches="tight"
        )
        plt.close("all")

        logger.info(f"Optimization plots saved to {dir_plots}")
    except Exception as e:
        logger.warning(f"Could not generate Optuna visualization plots: {e}")


# ---------------------------------------------------------------------------
# Bradley-Terry / Plackett-Luce model intercomparison
# ---------------------------------------------------------------------------

def _compute_instance_scores(df, metric="rmse"):
    """Compute a scalar error score per (Country, Crop, Region, Harvest Year, Model)."""
    obs_col, pred_col = _get_obs_pred_cols(df)
    if not obs_col:
        return pd.DataFrame()

    def _score(g):
        obs = g[obs_col]
        pred = g[pred_col]
        valid = obs.notna() & pred.notna() & (obs != 0)
        if valid.sum() < 1:
            return np.nan
        o, p = obs[valid].values, pred[valid].values
        if metric == "rmse":
            return np.sqrt(np.mean((o - p) ** 2))
        elif metric == "mae":
            return np.mean(np.abs(o - p))
        else:  # mape
            return np.mean(np.abs((o - p) / o)) * 100

    scores = (
        df.groupby(["Country", "Crop", "Region", "Harvest Year", "Model"])
        .apply(_score)
        .reset_index(name="score")
    )
    return scores.dropna(subset=["score"])


def _build_pairwise_comparisons(df_scores):
    """Return (models, comparisons) for Bradley-Terry; lower score = winner."""
    models = sorted(df_scores["Model"].unique())
    idx = {m: i for i, m in enumerate(models)}
    comparisons = []
    for _, grp in df_scores.groupby(["Country", "Crop", "Region", "Harvest Year"]):
        grp = grp.dropna(subset=["score"])
        if len(grp) < 2:
            continue
        rows = list(grp.itertuples())
        for r1 in rows:
            for r2 in rows:
                if r1.Model != r2.Model and r1.score < r2.score:
                    comparisons.append((idx[r1.Model], idx[r2.Model]))
    return models, comparisons


def _build_full_rankings(df_scores):
    """Return (models, rankings) for Plackett-Luce; each ranking ordered best→worst."""
    models = sorted(df_scores["Model"].unique())
    idx = {m: i for i, m in enumerate(models)}
    rankings = []
    for _, grp in df_scores.groupby(["Country", "Crop", "Region", "Harvest Year"]):
        grp = grp.dropna(subset=["score"]).sort_values("score")
        if len(grp) < 2:
            continue
        rankings.append([idx[m] for m in grp["Model"]])
    return models, rankings


def _bootstrap_bt(n_items, instance_comparisons_map, n_bootstrap=200, rng=None):
    """Bootstrap BT by resampling instances. Returns array (n_bootstrap, n_items)."""
    import choix
    if rng is None:
        rng = np.random.default_rng(42)
    instance_keys = list(instance_comparisons_map.keys())
    boots = []
    for _ in range(n_bootstrap):
        sampled_idx = rng.choice(len(instance_keys), size=len(instance_keys), replace=True)
        sample_comps = [c for i in sampled_idx for c in instance_comparisons_map[instance_keys[i]]]
        if len(sample_comps) < n_items:
            continue
        try:
            boots.append(choix.ilsr_pairwise(n_items, sample_comps, alpha=0.01))
        except Exception:
            pass
    return np.array(boots) if boots else np.empty((0, n_items))


def analyze_model_ranking(parser, logger, metric="rmse", n_bootstrap=200):
    """Bradley-Terry / Plackett-Luce model intercomparison with bootstrap CIs."""
    try:
        import choix
    except ImportError:
        logger.warning("choix not installed — skipping model ranking analysis (pip install choix)")
        return

    logger.info("Model ranking analysis (Bradley-Terry / Plackett-Luce)...")

    # Load model comparison results
    model_exp_list = [("models", "model_comparison", "", "str", [])]
    df = _load_experiment_results(parser, model_exp_list)
    if df.empty:
        logger.warning("No model comparison results found for ranking analysis")
        return

    dir_output = Path(parser.get("PATHS", "dir_output"))
    project_name = parser.get("DEFAULT", "project_name")
    today = ar.utcnow().to("America/New_York").format("MMMM_DD_YYYY")
    dir_plots = dir_output / project_name / "ml" / "experiments" / today / "model_ranking"
    os.makedirs(dir_plots, exist_ok=True)

    df_scores = _compute_instance_scores(df, metric=metric)
    if df_scores.empty or df_scores["Model"].nunique() < 2:
        logger.warning("Insufficient data for model ranking analysis")
        return

    models, comparisons = _build_pairwise_comparisons(df_scores)
    n = len(models)
    if len(comparisons) < n:
        logger.warning("Too few pairwise comparisons for Bradley-Terry fit")
        return

    # ── Bradley-Terry global fit ──────────────────────────────────────────────
    bt_params = choix.ilsr_pairwise(n, comparisons, alpha=0.01)

    # Build instance→comparisons map for bootstrap (resample at instance level)
    instance_comps = {}
    idx = {m: i for i, m in enumerate(models)}
    for key, grp in df_scores.groupby(["Country", "Crop", "Region", "Harvest Year"]):
        grp = grp.dropna(subset=["score"])
        pairs = []
        rows = list(grp.itertuples())
        for r1 in rows:
            for r2 in rows:
                if r1.Model != r2.Model and r1.score < r2.score:
                    pairs.append((idx[r1.Model], idx[r2.Model]))
        if pairs:
            instance_comps[key] = pairs

    boots = _bootstrap_bt(n, instance_comps, n_bootstrap=n_bootstrap)
    ci_lo = np.percentile(boots, 2.5, axis=0) if len(boots) else bt_params
    ci_hi = np.percentile(boots, 97.5, axis=0) if len(boots) else bt_params

    order = np.argsort(bt_params)[::-1]
    sorted_models = [models[i] for i in order]
    sorted_params = bt_params[order]
    sorted_lo = ci_lo[order]
    sorted_hi = ci_hi[order]

    fig, ax = plt.subplots(figsize=(max(6, n * 1.2), 5))
    x = np.arange(n)
    ax.bar(x, sorted_params, color="steelblue", alpha=0.8)
    ax.errorbar(x, sorted_params,
                yerr=[sorted_params - sorted_lo, sorted_hi - sorted_params],
                fmt="none", color="black", capsize=5)
    ax.set_xticks(x)
    ax.set_xticklabels(sorted_models, rotation=30, ha="right")
    ax.set_ylabel("Log-strength score")
    ax.set_title(f"Bradley-Terry Model Strengths ± 95% CI ({metric.upper()})")
    ax.axhline(0, color="gray", linestyle="--", linewidth=0.8)
    plt.tight_layout()
    fig.savefig(dir_plots / "bt_strength_scores.png", dpi=250)
    plt.close(fig)

    # ── Win matrix ────────────────────────────────────────────────────────────
    win_matrix = np.zeros((n, n), dtype=int)
    for w, l in comparisons:
        win_matrix[w, l] += 1
    total = win_matrix + win_matrix.T
    with np.errstate(divide="ignore", invalid="ignore"):
        win_rate = np.where(total > 0, win_matrix / total, np.nan)

    fig, ax = plt.subplots(figsize=(max(5, n * 1.1), max(4, n * 0.9)))
    sns.heatmap(
        win_rate, annot=True, fmt=".2f", cmap="RdYlGn",
        xticklabels=models, yticklabels=models,
        ax=ax, linewidths=0.5, vmin=0, vmax=1,
        cbar_kws={"label": "Win rate (row beats col)"},
    )
    ax.set_title(f"Pairwise Win Rate ({metric.upper()})")
    plt.tight_layout()
    fig.savefig(dir_plots / "win_matrix.png", dpi=250)
    plt.close(fig)

    # ── Plackett-Luce ─────────────────────────────────────────────────────────
    models_pl, rankings = _build_full_rankings(df_scores)
    pl_params = None
    if len(rankings) >= n:
        try:
            pl_params = choix.ilsr_rankings(n, rankings, alpha=0.01)
        except Exception as e:
            logger.warning(f"Plackett-Luce fit failed: {e}")

    if pl_params is not None:
        fig, ax = plt.subplots(figsize=(max(6, n * 1.2), 5))
        x = np.arange(n)
        w = 0.35
        bt_norm = bt_params - bt_params.min()
        pl_norm = pl_params - pl_params.min()
        ax.bar(x - w / 2, bt_norm[order], w, label="Bradley-Terry", color="steelblue", alpha=0.8)
        ax.bar(x + w / 2, pl_norm[order], w, label="Plackett-Luce", color="coral", alpha=0.8)
        ax.set_xticks(x)
        ax.set_xticklabels(sorted_models, rotation=30, ha="right")
        ax.set_ylabel("Normalised strength score")
        ax.set_title(f"BT vs Plackett-Luce Scores ({metric.upper()})")
        ax.legend()
        plt.tight_layout()
        fig.savefig(dir_plots / "pl_vs_bt_scores.png", dpi=250)
        plt.close(fig)

    # ── Stratified fits ───────────────────────────────────────────────────────
    for strata_cols, fname in [
        (["Country"], "stratified_by_country"),
        (["Crop"],    "stratified_by_crop"),
        (["Country", "Crop"], "stratified_by_country_crop"),
    ]:
        strata_scores = {}
        for key, grp in df_scores.groupby(strata_cols):
            label = " / ".join(key) if isinstance(key, tuple) else key
            if grp["Model"].nunique() < 2:
                continue
            _, comps = _build_pairwise_comparisons(grp)
            if len(comps) < n:
                continue
            try:
                p = choix.ilsr_pairwise(n, comps, alpha=0.01)
                strata_scores[label] = p
            except Exception:
                pass

        if not strata_scores:
            continue

        labels = list(strata_scores.keys())
        scores_mat = np.array([strata_scores[l] for l in labels])  # (n_strata, n_models)
        colors = [_FIXED_PALETTE[i % len(_FIXED_PALETTE)] for i in range(n)]

        with plt.style.context(["science", "no-latex"]):
            fig, ax = plt.subplots(figsize=(max(8, len(labels) * 1.4), 5))
            x = np.arange(len(labels))
            bar_w = 0.8 / n
            for mi, model in enumerate(models):
                ax.bar(x + mi * bar_w - 0.4 + bar_w / 2,
                       scores_mat[:, mi], bar_w, label=_fmt(model),
                       color=colors[mi], alpha=0.85)
            ax.set_xticks(x)
            ax.set_xticklabels(labels, rotation=30, ha="right")
            ax.set_ylabel("Log-strength score")
            ax.set_title(f"BT Strengths by {' / '.join(strata_cols)} ({metric.upper()})")
            ax.legend(title="Model", bbox_to_anchor=(1.02, 1), loc="upper left", fontsize=8)
            plt.tight_layout()
            fig.savefig(dir_plots / f"{fname}.png", dpi=250)
            plt.close(fig)

    # ── Save scores CSV ───────────────────────────────────────────────────────
    rows = [{"Model": models[i], "BT_score": bt_params[i],
             "BT_ci_lo": ci_lo[i], "BT_ci_hi": ci_hi[i],
             "PL_score": pl_params[i] if pl_params is not None else np.nan}
            for i in range(n)]
    pd.DataFrame(rows).sort_values("BT_score", ascending=False).to_csv(
        dir_plots / "model_ranking_scores.csv", index=False
    )

    logger.info(f"Model ranking plots saved to {dir_plots}")


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def run(path_config_files=[Path("../config/geocif.txt")], n_trials=30):
    logger, parser = log.setup_logger_parser(path_config_files)

    # Dedicated experiments DB (not the main geocif.db)
    now = ar.utcnow().to("America/New_York")
    db_name = f"experiments_{now.format('MMMM_DD_YYYY_HH')}H.db"
    parser.set("DEFAULT", "db", db_name)
    logger.info(f"Experiments DB: {db_name}")

    inputs = gc.gather_inputs(parser)

    # ----- Read [experiments] config with back-compat fallbacks -----
    ALL_EXPS = [
        "model_comparison", "cid_ablation", "region_filter",
        "optuna", "optuna_cid_types", "optuna_cid_indices",
    ]

    if parser.has_section("experiments") and parser.has_option("experiments", "run_experiments"):
        run_experiments = ast.literal_eval(parser.get("experiments", "run_experiments"))
    else:
        run_experiments = list(ALL_EXPS)

    if parser.has_section("experiments") and parser.has_option("experiments", "comparison_models"):
        model_experiment = ast.literal_eval(parser.get("experiments", "comparison_models"))
    else:
        model_experiment = ["catboost", "tabpfn", "tabicl"]

    if parser.has_section("experiments") and parser.has_option("experiments", "n_trials"):
        n_trials = parser.getint("experiments", "n_trials")

    # CID-subset Optuna searches can run larger budgets — separate knobs.
    n_trials_cid_types = parser.getint(
        "experiments", "n_trials_cid_types", fallback=n_trials,
    ) if parser.has_section("experiments") else n_trials
    n_trials_cid_indices = parser.getint(
        "experiments", "n_trials_cid_indices", fallback=n_trials,
    ) if parser.has_section("experiments") else n_trials
    max_cid_indices = parser.getint(
        "experiments", "max_cid_indices", fallback=25,
    ) if parser.has_section("experiments") else 25

    # Auto-promote model_comparison if any dependent stage is requested.
    if ("cid_ablation" in run_experiments or "region_filter" in run_experiments) \
            and "model_comparison" not in run_experiments:
        logger.warning(
            "cid_ablation/region_filter require model_comparison for best-model "
            "selection; auto-including model_comparison."
        )
        run_experiments = ["model_comparison"] + [
            e for e in run_experiments if e != "model_comparison"
        ]

    # Filter unknown names.
    unknown = [e for e in run_experiments if e not in ALL_EXPS]
    if unknown:
        logger.warning(f"Unknown experiment name(s) in run_experiments: {unknown} — ignored")
    run_experiments = [e for e in run_experiments if e in ALL_EXPS]

    # Hyperparameter search space (for summary display)
    hp_space = [
        ("feature_selection", ["SelectKBest", "gOMP", "none"]),
        ("lag_years", list(range(1, 6))),
        ("lag_yield_as_feature", [True, False]),
        ("check_yield_trend", [True, False]),
        ("use_spatial_neighbors", [True, False]),
        ("spatial_neighbor_method", ["knn", "full"]),
        ("spatial_neighbor_k", list(range(2, 9))),
        ("cluster_strategy", ["auto_detect", "single"]),
    ]

    total_combos = 1
    for _, values in hp_space:
        total_combos *= len(values)

    all_cids = ast.literal_eval(parser.get("ML", "use_cids"))
    if all_cids == ["all"]:
        select_by = parser.get("DEFAULT", "select_cid_by", fallback="Type")
        all_cids_display = _all_cid_types() if select_by == "Type" else _all_cid_indices()
    else:
        all_cids_display = all_cids

    params = gc._build_summary_params(parser, inputs)
    params.append(("Experiments", ", ".join(run_experiments) if run_experiments else "(none)"))
    if "model_comparison" in run_experiments:
        params.append(("Exp 0: models", ", ".join(model_experiment)))
    if "cid_ablation" in run_experiments:
        params.append(("Exp 1: CIDs", ", ".join(all_cids_display)))
    if "optuna" in run_experiments:
        params.append(("Optimization", f"Optuna TPE, {n_trials} trials"))
        for name, values in hp_space:
            params.append((f"  {name}", ", ".join(str(v) for v in values)))
        params.append(("Search space", f"{total_combos} combinations"))
    if "optuna_cid_types" in run_experiments:
        params.append(
            ("Optuna CID Types", f"{len(_all_cid_types())} labels, {n_trials_cid_types} trials")
        )
    if "optuna_cid_indices" in run_experiments:
        params.append((
            "Optuna CID Indices",
            f"{len(_all_cid_indices())} labels, {n_trials_cid_indices} trials, "
            f"max {max_cid_indices} per subset",
        ))
    ut.display_run_summary("GeoCIF Experiments Runner", params, wait=20)

    best_models = None  # set by model_comparison; reused by cid_ablation/region_filter

    # Experiment 0: model comparison
    if "model_comparison" in run_experiments:
        logger.info("Experiment 0: Model comparison")
        parser = main_models(logger, parser, model_experiment)

        # Analyze model comparison (Experiment 0) — before Optuna so plots are available early
        # Lookup is handled via "Model" column in _load_experiment_results;
        # tuple only provides the experiment label ("models") for plot grouping
        model_exp_list = [("models", "model_comparison", "", "str", model_experiment)]
        analyze_experiments(parser, model_exp_list, logger)
        analyze_model_ranking(parser, logger, metric="rmse", n_bootstrap=200)

        best_models = _get_best_models_from_exp0(parser, model_experiment)
        logger.info(f"  Best models from Exp 0: {best_models}")

    # Experiment 1: CID ablation — run each CID type individually with best model
    if "cid_ablation" in run_experiments:
        logger.info("Experiment 1: CID ablation")
        all_cids = ast.literal_eval(parser.get("ML", "use_cids"))
        if all_cids == ["all"]:
            select_by = parser.get("DEFAULT", "select_cid_by", fallback="Type")
            all_cids = _all_cid_types() if select_by == "Type" else _all_cid_indices()
            logger.info(f"  Expanded 'all' to {len(all_cids)} CID {select_by}s: {all_cids}")
        parser = experiment_1_cid_ablation(logger, parser, best_models, all_cids)

        cid_exp_list = [("cids", "", "", "str", all_cids)]
        analyze_experiments(parser, cid_exp_list, logger, best_models=best_models)

    # Experiment 2: Region filter
    if "region_filter" in run_experiments:
        logger.info("Experiment 2: Region filter")
        parser = experiment_2_region_filter(logger, parser, best_models)

        region_exp_list = [("region_filter", "region_filter", "", "str", list(best_models.values()))]
        analyze_experiments(parser, region_exp_list, logger)

    # Bayesian hyperparameter optimization
    if "optuna" in run_experiments:
        logger.info(f"Starting Optuna optimization ({n_trials} trials)...")
        study = optimize_hyperparameters(inputs, logger, parser, n_trials=n_trials)

        # Analyze optimization results
        analyze_optimization(parser, study, logger)

    # Optuna: best subset of CID Types
    if "optuna_cid_types" in run_experiments:
        logger.info(f"Optuna CID Types search ({n_trials_cid_types} trials)...")
        study_types = _optimize_cid_subset(
            "Type", inputs, logger, parser,
            n_trials=n_trials_cid_types,
            min_size=1,
        )
        analyze_optimization(parser, study_types, logger)

    # Optuna: best subset of CID Indices (individual indicators)
    if "optuna_cid_indices" in run_experiments:
        logger.info(f"Optuna CID Indices search ({n_trials_cid_indices} trials)...")
        study_idx = _optimize_cid_subset(
            "Index", inputs, logger, parser,
            n_trials=n_trials_cid_indices,
            min_size=3,
            max_size=max_cid_indices,
        )
        analyze_optimization(parser, study_idx, logger)


# ---------------------------------------------------------------------------
# Experiment analysis helpers (model comparison plots)
# ---------------------------------------------------------------------------

def _compute_metrics(group):
    """Compute error metrics for a group of observed/predicted pairs."""
    from sklearn.metrics import mean_squared_error, mean_absolute_error

    obs = group["Observed Yield (tn per ha)"]
    pred = group["Predicted Yield (tn per ha)"]
    valid = obs.notna() & pred.notna() & (obs != 0)
    obs, pred = obs[valid], pred[valid]
    if len(obs) < 3:
        return pd.Series({"RMSE": np.nan, "R2": np.nan, "MAE": np.nan, "MAPE": np.nan})
    rmse = np.sqrt(mean_squared_error(obs, pred))
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)
        r2 = np.corrcoef(obs, pred)[0, 1] ** 2
    mae = mean_absolute_error(obs, pred)
    mape_val = np.mean(np.abs((obs - pred) / obs)) * 100
    return pd.Series({"RMSE": rmse, "R2": r2, "MAE": mae, "MAPE": mape_val})


def _load_all_cids_reference(parser, best_models):
    """Load model_comparison results for best model per country, tagged as 'All CIDs'.

    Returns a DataFrame with experiment='cids', param_value='All CIDs' ready to
    concat with the CID ablation data so the 3 CID plots include a baseline.
    """
    exp_list = [("models", "model_comparison", "", "str", list(best_models.values()))]
    df = _load_experiment_results(parser, exp_list)
    if df.empty:
        return pd.DataFrame()

    # Keep only the best model rows for each country
    frames = []
    for country, model in best_models.items():
        mask = (df["Country"] == country) & (df["param_value"] == model)
        frames.append(df[mask])

    if not frames:
        return pd.DataFrame()

    ref = pd.concat(frames, ignore_index=True).copy()
    ref["experiment"] = "cids"
    ref["param_value"] = "All CIDs"
    return ref


def _load_experiment_results(parser, experiments):
    """Read all result tables from the DB and tag with experiment info."""
    dir_output = Path(parser.get("PATHS", "dir_output"))
    project_name = parser.get("DEFAULT", "project_name")
    db_name = parser.get("DEFAULT", "db")
    db_path = dir_output / project_name / "ml" / "db" / db_name

    if not db_path.exists():
        return pd.DataFrame()

    con = sqlite3.connect(db_path)
    tables = pd.read_sql(
        "SELECT name FROM sqlite_master WHERE type='table' "
        "AND name NOT LIKE 'config%' AND name != 'models'",
        con,
    )

    frames = []
    for table in tables["name"]:
        df = pd.read_sql(f'SELECT * FROM "{table}"', con)
        frames.append(df)
    con.close()

    if not frames:
        return pd.DataFrame()

    df_all = pd.concat(frames, ignore_index=True)

    # Build lookup: experiment_name_string -> (experiment_label, param_value)
    lookup = {}
    for name, section, item, _, values in experiments:
        for value in values:
            key = f"{section}_{item}_{value}"
            lookup[key] = {"experiment": name, "value": str(value)}

    df_all["experiment"] = df_all["Experiment Name"].map(
        lambda x: lookup.get(x, {}).get("experiment", "unknown")
    )
    df_all["param_value"] = df_all["Experiment Name"].map(
        lambda x: lookup.get(x, {}).get("value", "unknown")
    )

    # For model_comparison experiments, use the "Model" DB column as param_value
    if "model_comparison" in df_all["Experiment Name"].values:
        mask = df_all["Experiment Name"] == "model_comparison"
        df_all.loc[mask, "experiment"] = "models"
        df_all.loc[mask, "param_value"] = df_all.loc[mask, "Model"]

    # For CID ablation experiments (cid_<type>), extract CID type as param_value
    cid_mask = df_all["Experiment Name"].str.startswith("cid_")
    if cid_mask.any():
        df_all.loc[cid_mask, "experiment"] = "cids"
        df_all.loc[cid_mask, "param_value"] = (
            df_all.loc[cid_mask, "Experiment Name"].str.replace("cid_", "", n=1, regex=False)
        )

    # For region_filter experiment, use Model column as param_value
    if "region_filter" in df_all["Experiment Name"].values:
        mask = df_all["Experiment Name"] == "region_filter"
        df_all.loc[mask, "experiment"] = "region_filter"
        df_all.loc[mask, "param_value"] = df_all.loc[mask, "Model"]

    return df_all[df_all["experiment"] != "unknown"].copy()


def _plot_heatmap(df_metrics, experiment_name, dir_plots):
    """Plot 1: Heatmap of mean MAPE — countries vs parameter values."""
    df_exp = _filter_experiment(df_metrics, experiment_name)
    if df_exp.empty:
        return
    pivot = df_exp.pivot_table(
        index="Country", columns="param_value", values="MAPE", aggfunc="mean"
    )
    if pivot.empty:
        return

    fig, ax = plt.subplots(figsize=(max(8, len(pivot.columns) * 1.5), max(4, len(pivot) * 0.8)))
    sns.heatmap(pivot, annot=True, fmt=".1f", cmap="YlOrRd", ax=ax, linewidths=0.5)
    ax.set_title(f"Mean MAPE by Country — {experiment_name}")
    ax.set_xlabel("Parameter Value")
    ax.set_ylabel("Country")
    plt.tight_layout()
    fig.savefig(dir_plots / f"heatmap_{experiment_name}.png", dpi=250)
    plt.close(fig)


def _plot_boxplot(df_exp_data, experiment_name, dir_plots):
    """Plot 2: Box plots of MAPE distribution per parameter value."""
    df_exp = _compute_ape(_filter_experiment(df_exp_data, experiment_name))
    if df_exp.empty:
        return
    df_exp["APE_calc"] = df_exp["APE"]
    df_exp["param_display"] = df_exp["param_value"].map(_fmt)

    fig, ax = plt.subplots(figsize=(max(8, df_exp["param_display"].nunique() * 1.5), 6))
    sns.boxplot(data=df_exp, x="param_display", y="APE_calc", hue="Country", ax=ax)
    ax.set_title(f"APE Distribution — {experiment_name}")
    ax.set_xlabel("")
    ax.set_ylabel("Absolute Percentage Error (%)")
    ax.set_ylim(0, min(100, df_exp["APE_calc"].quantile(0.95) * 1.2))
    ax.legend(bbox_to_anchor=(1.02, 1), loc="upper left", fontsize=8)
    plt.tight_layout()
    fig.savefig(dir_plots / f"boxplot_{experiment_name}.png", dpi=250)
    plt.close(fig)


def _compute_production_pct(df_raw, country):
    """Compute production share % per region (5-year avg).

    Thin wrapper around viz.diagnostics.compute_production_pct so the
    logic lives in one place; experiments.py allows an arbitrary
    Observed-Yield column name so we resolve it here first.
    """
    obs_col, _ = _get_obs_pred_cols(df_raw[df_raw["Country"] == country])
    if not obs_col:
        return {}
    from .viz import diagnostics as diag
    return diag.compute_production_pct(df_raw, country, obs_col=obs_col)


def _plot_regional_mape(df_metrics, df_exp_data, experiment_name, dir_plots):
    """Plot 3: Regional MAPE bar chart per country, ordered by production share."""
    df_exp = _filter_experiment(df_metrics, experiment_name)
    if df_exp.empty or "Region" not in df_exp.columns:
        return

    df_raw = _filter_experiment(df_exp_data, experiment_name)

    with plt.style.context(["science", "no-latex"]):
        for country in df_exp["Country"].unique():
            df_c = df_exp[df_exp["Country"] == country]
            if df_c.empty:
                continue

            prod_pct = _compute_production_pct(df_raw, country)

            pivot = df_c.pivot_table(
                index="Region", columns="param_value", values="MAPE", aggfunc="mean"
            )
            if pivot.empty:
                continue

            # Display names for model columns
            pivot.columns = [_fmt(c) for c in pivot.columns]
            bar_colors = [_FIXED_PALETTE[i % len(_FIXED_PALETTE)] for i in range(len(pivot.columns))]

            # Order by descending production share
            pivot = _order_by_production(pivot, prod_pct, ascending=True)

            fig, ax = plt.subplots(figsize=(max(10, len(pivot.columns) * 1.2), max(5, len(pivot) * 0.4)))
            pivot.plot(kind="barh", ax=ax, color=bar_colors)
            ax.set_title(f"Mean MAPE by Region — {experiment_name} — {country}")
            ax.set_xlabel("MAPE (%)")
            ax.set_ylabel("")
            ax.legend(title="Model", bbox_to_anchor=(1.02, 1), loc="upper left", fontsize=8)
            plt.tight_layout()
            fig.savefig(dir_plots / f"mape_region_{experiment_name}_{country}.png", dpi=250)
            plt.close(fig)


def _plot_overall_comparison(df_metrics, experiments, dir_plots):
    """Plot 4: Summary — best parameter value per experiment, grouped by country."""
    rows = []
    for name, *_ in experiments:
        df_exp = _filter_experiment(df_metrics, name)
        if df_exp.empty:
            continue
        best = (
            df_exp.groupby(["Country", "param_value"])["MAPE"]
            .mean()
            .reset_index()
            .loc[lambda d: d.groupby("Country")["MAPE"].idxmin()]
        )
        for _, row in best.iterrows():
            rows.append({
                "Experiment": name,
                "Country": row["Country"],
                "Best Value": row["param_value"],
                "MAPE": row["MAPE"],
            })

    if not rows:
        return

    df_best = pd.DataFrame(rows)
    fig, ax = plt.subplots(figsize=(max(10, len(df_best) * 0.6), 6))
    sns.barplot(data=df_best, x="Experiment", y="MAPE", hue="Country", ax=ax)

    # Annotate bars with the best value
    for container in ax.containers:
        for bar in container:
            h = bar.get_height()
            if h > 0:
                ax.text(
                    bar.get_x() + bar.get_width() / 2, h,
                    f"{h:.1f}", ha="center", va="bottom", fontsize=7
                )

    ax.set_title("Best MAPE Across Experiments by Country")
    ax.set_xlabel("Experiment")
    ax.set_ylabel("MAPE (%)")
    ax.tick_params(axis="x", rotation=30)
    ax.legend(bbox_to_anchor=(1.02, 1), loc="upper left", fontsize=8)
    plt.tight_layout()
    fig.savefig(dir_plots / "metric_comparison.png", dpi=250)
    plt.close(fig)


def _plot_error_distribution(df_exp_data, experiment_name, dir_plots):
    """Plot 5: Overlaid KDE of APE per parameter value."""
    df_exp = _compute_ape(_filter_experiment(df_exp_data, experiment_name))
    if df_exp.empty:
        return
    df_exp["APE_calc"] = df_exp["APE"]

    # Cap for readability
    cap = df_exp["APE_calc"].quantile(0.95)
    df_plot = df_exp[df_exp["APE_calc"] <= cap]

    with plt.style.context(["science", "no-latex"]):
        fig, ax = plt.subplots(figsize=(10, 6))
        for val in sorted(df_plot["param_value"].unique()):
            subset = df_plot[df_plot["param_value"] == val]["APE_calc"]
            if len(subset) > 5:
                subset.plot.kde(ax=ax, label=_fmt(val))

        ax.set_title(f"APE Distribution — {experiment_name}")
        ax.set_xlabel("Absolute Percentage Error (%)")
        ax.set_ylabel("Density")
        ax.set_xlim(0, None)
        ax.legend(title="Value", fontsize=8)
        plt.tight_layout()
        fig.savefig(dir_plots / f"error_distribution_{experiment_name}.png", dpi=250)
        plt.close(fig)


def _plot_feature_frequency(df_exp_data, experiment_name, dir_plots):
    """Plot feature selection frequency per country-crop combo."""
    df_exp = _filter_experiment(df_exp_data, experiment_name)
    if df_exp.empty or "Selected Features" not in df_exp.columns:
        return

    # Parse string-encoded feature lists
    def _safe_parse(x):
        if isinstance(x, list):
            return x
        try:
            return ast.literal_eval(x)
        except Exception:
            return []

    df_exp["_parsed_features"] = df_exp["Selected Features"].apply(_safe_parse)

    # Deduplicate: one feature list per (Country, Crop, Region, Harvest Year, param_value)
    dedup_cols = ["Country", "Crop", "Region", "Harvest Year", "param_value"]
    existing = [c for c in dedup_cols if c in df_exp.columns]
    df_dedup = df_exp.drop_duplicates(subset=existing)

    # Build frequency table per (Country, Crop)
    records = []
    for (country, crop), grp in df_dedup.groupby(["Country", "Crop"]):
        from collections import Counter
        counter = Counter()
        for feat_list in grp["_parsed_features"]:
            if isinstance(feat_list, list):
                counter.update(feat_list)
        for feat, count in counter.items():
            records.append({"Country": country, "Crop": crop, "Feature": feat, "Count": count})

    if not records:
        return

    df_freq = pd.DataFrame(records)

    # Save CSV
    df_freq.to_csv(dir_plots / f"feature_freq_{experiment_name}.csv", index=False)

    # Plot per country-crop
    for (country, crop), grp in df_freq.groupby(["Country", "Crop"]):
        grp_sorted = grp.sort_values("Count", ascending=True).tail(20)
        n_features = len(grp_sorted)
        with plt.style.context(["science", "no-latex"]):
            fig, ax = plt.subplots(figsize=(8, max(4, n_features * 0.35)))
            ax.barh(grp_sorted["Feature"], grp_sorted["Count"],
                    color=_FIXED_PALETTE[0])
            ax.set_xlabel("Selection Frequency")
            ax.set_title(f"Feature Selection Frequency — {country} {crop}\n({experiment_name})")
            plt.tight_layout()
        fig.savefig(
            dir_plots / f"feature_freq_{experiment_name}_{country}_{crop}.png",
            dpi=250,
        )
        plt.close(fig)


def _plot_mape_by_year(df_exp_data, experiment_name, dir_plots):
    """Plot MAPE by harvest year, one line per model/param_value."""
    df_exp = _compute_ape(_filter_experiment(df_exp_data, experiment_name))
    if df_exp.empty or "Harvest Year" not in df_exp.columns:
        return

    mape_by_year = (
        df_exp.groupby(["Harvest Year", "param_value"])["APE"]
        .mean()
        .reset_index()
        .rename(columns={"APE": "MAPE"})
    )
    mape_by_year = mape_by_year.sort_values("Harvest Year")

    with plt.style.context(["science", "no-latex"]):
        fig, ax = plt.subplots(figsize=(10, 5))
        pv_list = sorted(mape_by_year["param_value"].unique())
        for i, pv in enumerate(pv_list):
            grp = mape_by_year[mape_by_year["param_value"] == pv]
            ax.plot(grp["Harvest Year"], grp["MAPE"], marker="o",
                    label=_fmt(pv), color=_FIXED_PALETTE[i % len(_FIXED_PALETTE)])
        ax.set_xlabel("")
        ax.set_ylabel("MAPE (%)")
        ax.set_title(f"MAPE by Year — {experiment_name}")
        ax.legend(title="Model", bbox_to_anchor=(1.02, 1), loc="upper left", fontsize=8)
        plt.tight_layout()
        fig.savefig(dir_plots / f"mape_year_{experiment_name}.png", dpi=250)
        plt.close(fig)


def _plot_mape_by_cid(df_exp_data, experiment_name, dir_plots):
    """Bar chart of mean MAPE per CID type."""
    df_exp = _compute_ape(_filter_experiment(df_exp_data, experiment_name))
    if df_exp.empty:
        return

    mape = df_exp.groupby("param_value")["APE"].mean().sort_values()
    # Place "All CIDs" first
    if "All CIDs" in mape.index:
        all_cids_val = mape.pop("All CIDs")
        mape = pd.concat([pd.Series({"All CIDs": all_cids_val}), mape])

    with plt.style.context(["science", "no-latex"]):
        fig, ax = plt.subplots(figsize=(max(8, len(mape) * 0.8), 5))
        bar_colors = ["black" if idx == "All CIDs" else _FIXED_PALETTE[0]
                       for idx in mape.index]
        mape.plot(kind="bar", ax=ax, color=bar_colors)
        ax.set_xlabel("")
        ax.set_ylabel("MAPE (%)")
        ax.set_title(f"MAPE by CID Type — {experiment_name}")
        ax.tick_params(axis="x", rotation=45)
        plt.tight_layout()
        fig.savefig(dir_plots / f"mape_cid_{experiment_name}.png", dpi=250)
        plt.close(fig)


def _plot_mape_by_cid_region(df_exp_data, experiment_name, dir_plots):
    """Heatmap of MAPE: regions (rows) vs CID types (cols), ordered by production %."""
    df_exp = _compute_ape(_filter_experiment(df_exp_data, experiment_name))
    if df_exp.empty:
        return

    for country in df_exp["Country"].unique():
        df_c = df_exp[df_exp["Country"] == country]
        prod_pct = _compute_production_pct(df_exp, country)

        pivot = df_c.pivot_table(
            index="Region", columns="param_value", values="APE", aggfunc="mean"
        )
        if pivot.empty:
            continue

        # Order by production %
        pivot = _order_by_production(pivot, prod_pct, ascending=False)
        # Place "All CIDs" first column
        if "All CIDs" in pivot.columns:
            cols = ["All CIDs"] + [c for c in pivot.columns if c != "All CIDs"]
            pivot = pivot[cols]

        fig, ax = plt.subplots(figsize=(max(8, len(pivot.columns) * 1.2), max(5, len(pivot) * 0.4)))
        sns.heatmap(pivot, annot=True, fmt=".1f", cmap="YlOrRd", ax=ax, linewidths=0.5)
        ax.set_title(f"MAPE by Region × CID — {country}\n({experiment_name})")
        ax.set_xlabel("")
        ax.set_ylabel("Region (% of production)")
        for tick in ax.get_xticklabels():
            if tick.get_text() == "All CIDs":
                tick.set_fontweight("bold")
        plt.tight_layout()
        fig.savefig(dir_plots / f"mape_cid_region_{experiment_name}_{country}.png", dpi=250)
        plt.close(fig)


def _plot_mape_by_cid_year(df_exp_data, experiment_name, dir_plots):
    """Line plot of MAPE by harvest year, one line per CID type."""
    df_exp = _compute_ape(_filter_experiment(df_exp_data, experiment_name))
    if df_exp.empty or "Harvest Year" not in df_exp.columns:
        return

    mape_by_year = (
        df_exp.groupby(["Harvest Year", "param_value"])["APE"]
        .mean().reset_index().rename(columns={"APE": "MAPE"})
        .sort_values("Harvest Year")
    )

    cid_names = sorted(pv for pv in mape_by_year["param_value"].unique() if pv != "All CIDs")
    cid_colors = {name: _FIXED_PALETTE[i % len(_FIXED_PALETTE)]
                  for i, name in enumerate(cid_names)}
    groups = dict(list(mape_by_year.groupby("param_value")))

    with plt.style.context(["science", "no-latex"]):
        fig, ax = plt.subplots(figsize=(10, 5))
        # Plot individual CIDs first, then "All CIDs" on top
        for pv in cid_names:
            if pv in groups:
                grp = groups[pv]
                ax.plot(grp["Harvest Year"], grp["MAPE"], marker="o",
                        label=pv, color=cid_colors[pv])
        if "All CIDs" in groups:
            grp = groups["All CIDs"]
            ax.plot(grp["Harvest Year"], grp["MAPE"], marker="o", label="All CIDs",
                    color="black", linewidth=2.5, zorder=10)
        ax.set_xlabel("")
        ax.set_ylabel("MAPE (%)")
        ax.set_title(f"MAPE by Year × CID — {experiment_name}")
        # Place "All CIDs" first in legend
        handles, labels = ax.get_legend_handles_labels()
        if "All CIDs" in labels:
            idx = labels.index("All CIDs")
            handles = [handles[idx]] + handles[:idx] + handles[idx + 1:]
            labels = [labels[idx]] + labels[:idx] + labels[idx + 1:]
        ax.legend(handles, labels, title="CID Type", bbox_to_anchor=(1.02, 1), loc="upper left", fontsize=8)
        plt.tight_layout()
        fig.savefig(dir_plots / f"mape_cid_year_{experiment_name}.png", dpi=250)
        plt.close(fig)


def _plot_cid_rank_by_year(df_exp_data, experiment_name, dir_plots):
    """Heatmap of CID rank per harvest year (rank 1 = lowest MAPE that year)."""
    df_exp = _compute_ape(_filter_experiment(df_exp_data, experiment_name))
    if df_exp.empty or "Harvest Year" not in df_exp.columns:
        return

    mape_by_year = (
        df_exp.groupby(["Harvest Year", "param_value"])["APE"]
        .mean().reset_index().rename(columns={"APE": "MAPE"})
    )
    mape_by_year["Rank"] = mape_by_year.groupby("Harvest Year")["MAPE"].rank(method="min")

    pivot = mape_by_year.pivot(index="Harvest Year", columns="param_value", values="Rank")
    # Place "All CIDs" first column
    if "All CIDs" in pivot.columns:
        cols = ["All CIDs"] + [c for c in pivot.columns if c != "All CIDs"]
        pivot = pivot[cols]

    n_cids = len(pivot.columns)
    fig, ax = plt.subplots(figsize=(max(8, n_cids * 1.0), max(4, len(pivot) * 0.5)))
    sns.heatmap(
        pivot, annot=True, fmt=".0f", cmap="RdYlGn_r",
        ax=ax, linewidths=0.5, vmin=1, vmax=n_cids,
        cbar_kws={"label": "Rank (1 = best)"},
    )
    ax.set_title(f"CID Rank by Year (1 = lowest MAPE) — {experiment_name}")
    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.tick_params(axis="x", rotation=45)
    ax.tick_params(axis="y", rotation=0)
    for tick in ax.get_xticklabels():
        tick.set_ha("right")
        if tick.get_text() == "All CIDs":
            tick.set_fontweight("bold")
    plt.tight_layout()
    fig.savefig(dir_plots / f"cid_rank_year_{experiment_name}.png", dpi=250)
    plt.close(fig)


def _generate_diagnostics_for_experiment(df_exp_data, exp_name, dg, dir_experiments):
    """Scatter, MAPE bar chart, and MAPE choropleth for one experiment.

    Args:
        df_exp_data: full experiment DataFrame (all experiments)
        exp_name: experiment label to filter on
        dg: GeoDataFrame of boundaries (may be None if shapefiles unavailable)
        dir_experiments: Path to ml/experiments/{today}/
    Output dirs:
        dir_experiments/plots/{exp_name}/  — scatter, MAPE bar
        dir_experiments/maps/{exp_name}/   — MAPE choropleth
    """
    from geocif.viz import diagnostics as diag

    df_exp = _filter_experiment(df_exp_data, exp_name)
    obs_col, pred_col = _get_obs_pred_cols(df_exp)
    if obs_col is None or df_exp.empty:
        return

    df_exp = df_exp.dropna(subset=[obs_col, pred_col]).copy()
    df_exp = df_exp.rename(columns={obs_col: "Observed Yield (tn per ha)",
                                     pred_col: "Predicted Yield (tn per ha)"})
    if df_exp.empty:
        return

    dir_plots = dir_experiments / "plots" / exp_name
    dir_maps  = dir_experiments / "maps"  / exp_name
    os.makedirs(dir_plots, exist_ok=True)
    os.makedirs(dir_maps, exist_ok=True)

    # Scatter
    diag.scatter_obs_pred(df_exp, exp_name, dir_plots, f"scatter_{exp_name}.png")

    # MAPE bar chart
    df_mape = df_exp.assign(
        MAPE=lambda d: (
            (d["Predicted Yield (tn per ha)"] - d["Observed Yield (tn per ha)"]).abs()
            / d["Observed Yield (tn per ha)"].replace(0, np.nan) * 100
        )
    ).groupby("Region", as_index=False)["MAPE"].mean()
    diag.mape_bar_chart(df_mape, exp_name, dir_plots, f"mape_bar_{exp_name}.png")

    # MAPE choropleth map
    if dg is not None and not dg.empty and not df_mape.empty:
        country_map = (
            df_exp.drop_duplicates("Region")
            .set_index("Region")["Country"]
            .str.lower().str.replace("_", " ")
        )
        df_mape["Country Region"] = (
            country_map.reindex(df_mape["Region"]).values
            + " "
            + df_mape["Region"].str.lower()
        )
        df_mape = df_mape.rename(columns={"MAPE": "Mean Absolute Percentage Error"})
        countries_display = df_exp["Country"].str.title().str.replace("_", " ").unique().tolist()
        dg_sub = dg[dg["ADM0_NAME"].isin(countries_display)].copy()
        diag.mape_choropleth(
            dg_sub, df_mape, countries_display, False,
            dir_maps, f"mape_map_{exp_name}.png",
        )


def analyze_experiments(parser, experiments, logger, best_models=None):
    """Read experiment results from DB and generate comparison plots."""
    logger.info("Analyzing experiment results...")

    df_exp = _load_experiment_results(parser, experiments)
    if df_exp.empty:
        logger.warning("No experiment results found in database")
        return

    # Inject All-CIDs reference into CID ablation data
    experiment_names = [name for name, *_ in experiments]
    if "cids" in experiment_names and best_models:
        df_ref = _load_all_cids_reference(parser, best_models)
        if not df_ref.empty:
            df_exp = pd.concat([df_exp, df_ref], ignore_index=True)

    dir_output = Path(parser.get("PATHS", "dir_output"))
    project_name = parser.get("DEFAULT", "project_name")
    today = ar.utcnow().to("America/New_York").format("MMMM_DD_YYYY")
    dir_experiments = dir_output / project_name / "ml" / "experiments" / today
    dir_plots = dir_experiments  # existing flat plots land here (unchanged)
    os.makedirs(dir_plots, exist_ok=True)
    _save_config(parser, dir_plots)

    # Load shapefiles once for choropleth maps (gracefully skip if unavailable)
    try:
        from geocif.yield_outlook import _load_shapefiles
        dg, _ = _load_shapefiles(parser)
    except Exception:
        dg = None

    # Compute metrics grouped by experiment variant, country, crop, region
    df_metrics = (
        df_exp.groupby(["experiment", "param_value", "Country", "Crop", "Region"])
        .apply(_compute_metrics)
        .reset_index()
    )
    df_metrics = df_metrics.dropna(subset=["MAPE"])

    if df_metrics.empty:
        logger.warning("Could not compute metrics from experiment results")
        return

    # Save metrics table as CSV
    df_metrics.to_csv(dir_plots / "experiment_metrics.csv", index=False)
    logger.info(f"Saved experiment metrics to {dir_plots / 'experiment_metrics.csv'}")
    
    # Generate all plots — wrap each call so one failure doesn't skip the rest
    def _safe_plot(fn, *args, name=""):
        try:
            fn(*args)
        except Exception as e:
            logger.warning(f"Plot {name or fn.__name__} failed: {e}")

    for exp_name in experiment_names:
        logger.info(f"  Plotting {exp_name}...")
        dir_exp_plots = dir_experiments / "plots" / exp_name
        os.makedirs(dir_exp_plots, exist_ok=True)
        _safe_plot(_plot_heatmap, df_metrics, exp_name, dir_exp_plots)
        _safe_plot(_plot_boxplot, df_exp, exp_name, dir_exp_plots)
        _safe_plot(_plot_regional_mape, df_metrics, df_exp, exp_name, dir_exp_plots)
        _safe_plot(_plot_error_distribution, df_exp, exp_name, dir_exp_plots)
        _safe_plot(_plot_feature_frequency, df_exp, exp_name, dir_exp_plots)
        _safe_plot(_plot_mape_by_year, df_exp, exp_name, dir_exp_plots)
        if exp_name == "cids":
            _safe_plot(_plot_mape_by_cid, df_exp, exp_name, dir_exp_plots)
            _safe_plot(_plot_mape_by_cid_region, df_exp, exp_name, dir_exp_plots)
            _safe_plot(_plot_mape_by_cid_year, df_exp, exp_name, dir_exp_plots)
            _safe_plot(_plot_cid_rank_by_year, df_exp, exp_name, dir_exp_plots)
        # Diagnostic plots: scatter, MAPE bar, MAPE map
        _safe_plot(_generate_diagnostics_for_experiment, df_exp, exp_name, dg, dir_experiments,
                   name=f"diagnostics_{exp_name}")

    _plot_overall_comparison(df_metrics, experiments, dir_plots)

    logger.info(f"Experiment analysis plots saved to {dir_plots}")


if __name__ == "__main__":
    run()
