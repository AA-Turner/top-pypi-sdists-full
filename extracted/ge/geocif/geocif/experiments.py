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

from geocif import geocif_runner as gc
from geocif import logger as log
from geocif import utils as ut

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

plt.style.use("default")
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
        gc.execute_models(inputs, logger, parser)

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
        gc.execute_models(inputs, logger, parser)

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


def experiment_1_cei_ablation(logger, parser, best_models, all_ceis):
    """Experiment 1: Run each CEI type individually using the best model per country."""
    countries = ast.literal_eval(parser.get("DEFAULT", "countries"))

    # Save originals — use_ceis lives in [DEFAULT], not [ML]
    orig_use_ceis = parser.get("DEFAULT", "use_ceis")
    orig_experiment_name = parser.get("ML", "experiment_name")
    orig_models = {c: parser.get(c, "models") for c in countries}

    # Set best model per country
    for country, model in best_models.items():
        parser.set(country, "models", f'["{model}"]')

    for cei in all_ceis:
        logger.info(f"  CEI ablation: {cei}")
        parser.set("ML", "experiment_name", f"cei_{cei}")
        parser.set("DEFAULT", "use_ceis", f'["{cei}"]')

        inputs = gc.gather_inputs(parser)
        gc.execute_models(inputs, logger, parser)

    # Restore originals
    parser.set("DEFAULT", "use_ceis", orig_use_ceis)
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
            gc.execute_models(inputs, logger, parser)
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
    dir_plots = dir_output / project_name / "ml" / "analysis" / today / "optimization"
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

    # Experiment 0: Model comparison (runs each model independently)
    model_experiment = ["catboost", "tabpfn", "tabicl"]

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

    all_ceis = ast.literal_eval(parser.get("ML", "use_ceis"))

    params = gc._build_summary_params(parser, inputs)
    params.append(("Exp 0: models", ", ".join(model_experiment)))
    params.append(("Exp 1: CEIs", ", ".join(all_ceis)))
    params.append(("Optimization", f"Optuna TPE, {n_trials} trials"))
    for name, values in hp_space:
        params.append((f"  {name}", ", ".join(str(v) for v in values)))
    params.append(("Search space", f"{total_combos} combinations"))
    ut.display_run_summary("GeoCIF Experiments Runner", params, wait=20)

    # Experiment 0: model comparison
    logger.info("Experiment 0: Model comparison")
    parser = main_models(logger, parser, model_experiment)

    # Analyze model comparison (Experiment 0) — before Optuna so plots are available early
    # Lookup is handled via "Model" column in _load_experiment_results;
    # tuple only provides the experiment label ("models") for plot grouping
    model_exp_list = [("models", "model_comparison", "", "str", model_experiment)]
    analyze_experiments(parser, model_exp_list, logger)

    # Experiment 1: CEI ablation — run each CEI type individually with best model
    logger.info("Experiment 1: CEI ablation")
    all_ceis = ast.literal_eval(parser.get("ML", "use_ceis"))
    best_models = _get_best_models_from_exp0(parser, model_experiment)
    logger.info(f"  Best models from Exp 0: {best_models}")
    parser = experiment_1_cei_ablation(logger, parser, best_models, all_ceis)

    cei_exp_list = [("ceis", "", "", "str", all_ceis)]
    analyze_experiments(parser, cei_exp_list, logger)

    # Bayesian hyperparameter optimization
    logger.info(f"Starting Optuna optimization ({n_trials} trials)...")
    study = optimize_hyperparameters(inputs, logger, parser, n_trials=n_trials)

    # Analyze optimization results
    analyze_optimization(parser, study, logger)


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

    # For CEI ablation experiments (cei_<type>), extract CEI type as param_value
    cei_mask = df_all["Experiment Name"].str.startswith("cei_")
    if cei_mask.any():
        df_all.loc[cei_mask, "experiment"] = "ceis"
        df_all.loc[cei_mask, "param_value"] = (
            df_all.loc[cei_mask, "Experiment Name"].str.replace("cei_", "", n=1)
        )

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

    fig, ax = plt.subplots(figsize=(max(8, df_exp["param_value"].nunique() * 1.5), 6))
    sns.boxplot(data=df_exp, x="param_value", y="APE_calc", hue="Country", ax=ax)
    ax.set_title(f"APE Distribution — {experiment_name}")
    ax.set_xlabel("Parameter Value")
    ax.set_ylabel("Absolute Percentage Error (%)")
    ax.set_ylim(0, min(100, df_exp["APE_calc"].quantile(0.95) * 1.2))
    ax.legend(bbox_to_anchor=(1.02, 1), loc="upper left", fontsize=8)
    plt.tight_layout()
    fig.savefig(dir_plots / f"boxplot_{experiment_name}.png", dpi=250)
    plt.close(fig)


def _compute_production_pct(df_raw, country):
    """Compute production share % per region (5-year avg, geoagmet approach)."""
    df_c = df_raw[df_raw["Country"] == country].copy()
    if df_c.empty or "Area (ha)" not in df_c.columns:
        return {}

    obs_col, _ = _get_obs_pred_cols(df_c)
    if not obs_col:
        return {}

    df_c["_prod"] = df_c["Area (ha)"] * df_c[obs_col]
    df_c = df_c.dropna(subset=["_prod", "Harvest Year"])

    # Last 5 years
    last_5 = sorted(df_c["Harvest Year"].unique())[-5:]
    df_c = df_c[df_c["Harvest Year"].isin(last_5)]

    mean_by_region = df_c.groupby("Region")["_prod"].mean()
    total = mean_by_region.sum()
    if total <= 0:
        return {}
    return (mean_by_region / total * 100).to_dict()


def _plot_regional_mape(df_metrics, df_exp_data, experiment_name, dir_plots):
    """Plot 3: Regional MAPE bar chart per country, ordered by production share."""
    df_exp = _filter_experiment(df_metrics, experiment_name)
    if df_exp.empty or "Region" not in df_exp.columns:
        return

    df_raw = _filter_experiment(df_exp_data, experiment_name)

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

        # Order by descending production share
        pivot = _order_by_production(pivot, prod_pct, ascending=True)

        fig, ax = plt.subplots(figsize=(max(10, len(pivot.columns) * 1.2), max(5, len(pivot) * 0.4)))
        pivot.plot(kind="barh", ax=ax)
        ax.set_title(f"Mean MAPE by Region — {experiment_name} — {country}")
        ax.set_xlabel("MAPE (%)")
        ax.set_ylabel("Region (% of national production)")
        ax.legend(title="Model", bbox_to_anchor=(1.02, 1), loc="upper left", fontsize=8)
        plt.tight_layout()
        fig.savefig(dir_plots / f"regional_mape_{experiment_name}_{country}.png", dpi=250)
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

    fig, ax = plt.subplots(figsize=(10, 6))
    for val in sorted(df_plot["param_value"].unique()):
        subset = df_plot[df_plot["param_value"] == val]["APE_calc"]
        if len(subset) > 5:
            subset.plot.kde(ax=ax, label=val)

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
    df_exp["_parsed_features"] = df_exp["Selected Features"].apply(
        lambda x: ast.literal_eval(x) if isinstance(x, str) else x
    )

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
        fig, ax = plt.subplots(figsize=(8, max(4, n_features * 0.35)))
        ax.barh(grp_sorted["Feature"], grp_sorted["Count"], color="steelblue")
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

    fig, ax = plt.subplots(figsize=(10, 5))
    for pv, grp in mape_by_year.groupby("param_value"):
        ax.plot(grp["Harvest Year"], grp["MAPE"], marker="o", label=pv)
    ax.set_xlabel("Harvest Year")
    ax.set_ylabel("MAPE (%)")
    ax.set_title(f"MAPE by Year — {experiment_name}")
    ax.legend(title="Model", bbox_to_anchor=(1.02, 1), loc="upper left", fontsize=8)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    fig.savefig(dir_plots / f"mape_by_year_{experiment_name}.png", dpi=250)
    plt.close(fig)


def _plot_mape_by_cei(df_exp_data, experiment_name, dir_plots):
    """Bar chart of mean MAPE per CEI type."""
    df_exp = _compute_ape(_filter_experiment(df_exp_data, experiment_name))
    if df_exp.empty:
        return

    mape = df_exp.groupby("param_value")["APE"].mean().sort_values()
    fig, ax = plt.subplots(figsize=(max(8, len(mape) * 0.8), 5))
    mape.plot(kind="bar", ax=ax, color="steelblue")
    ax.set_xlabel("CEI Type")
    ax.set_ylabel("MAPE (%)")
    ax.set_title(f"MAPE by CEI Type — {experiment_name}")
    ax.tick_params(axis="x", rotation=45)
    plt.tight_layout()
    fig.savefig(dir_plots / f"mape_by_cei_{experiment_name}.png", dpi=250)
    plt.close(fig)


def _plot_mape_by_cei_region(df_exp_data, experiment_name, dir_plots):
    """Heatmap of MAPE: regions (rows) vs CEI types (cols), ordered by production %."""
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

        fig, ax = plt.subplots(figsize=(max(8, len(pivot.columns) * 1.2), max(5, len(pivot) * 0.4)))
        sns.heatmap(pivot, annot=True, fmt=".1f", cmap="YlOrRd", ax=ax, linewidths=0.5)
        ax.set_title(f"MAPE by Region × CEI — {country}\n({experiment_name})")
        ax.set_xlabel("CEI Type")
        ax.set_ylabel("Region (% of production)")
        plt.tight_layout()
        fig.savefig(dir_plots / f"mape_by_cei_region_{experiment_name}_{country}.png", dpi=250)
        plt.close(fig)


def _plot_mape_by_cei_year(df_exp_data, experiment_name, dir_plots):
    """Line plot of MAPE by harvest year, one line per CEI type."""
    df_exp = _compute_ape(_filter_experiment(df_exp_data, experiment_name))
    if df_exp.empty or "Harvest Year" not in df_exp.columns:
        return

    mape_by_year = (
        df_exp.groupby(["Harvest Year", "param_value"])["APE"]
        .mean().reset_index().rename(columns={"APE": "MAPE"})
        .sort_values("Harvest Year")
    )

    fig, ax = plt.subplots(figsize=(10, 5))
    for pv, grp in mape_by_year.groupby("param_value"):
        ax.plot(grp["Harvest Year"], grp["MAPE"], marker="o", label=pv)
    ax.set_xlabel("Harvest Year")
    ax.set_ylabel("MAPE (%)")
    ax.set_title(f"MAPE by Year × CEI — {experiment_name}")
    ax.legend(title="CEI Type", bbox_to_anchor=(1.02, 1), loc="upper left", fontsize=8)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    fig.savefig(dir_plots / f"mape_by_cei_year_{experiment_name}.png", dpi=250)
    plt.close(fig)


def analyze_experiments(parser, experiments, logger):
    """Read experiment results from DB and generate comparison plots."""
    logger.info("Analyzing experiment results...")

    df_exp = _load_experiment_results(parser, experiments)
    if df_exp.empty:
        logger.warning("No experiment results found in database")
        return

    dir_output = Path(parser.get("PATHS", "dir_output"))
    project_name = parser.get("DEFAULT", "project_name")
    today = ar.utcnow().to("America/New_York").format("MMMM_DD_YYYY")
    dir_plots = dir_output / project_name / "ml" / "analysis" / today / "experiments"
    os.makedirs(dir_plots, exist_ok=True)
    _save_config(parser, dir_plots)

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
    
    # Generate all plots
    experiment_names = [name for name, *_ in experiments]
    for exp_name in experiment_names:
        logger.info(f"  Plotting {exp_name}...")
        _plot_heatmap(df_metrics, exp_name, dir_plots)
        _plot_boxplot(df_exp, exp_name, dir_plots)
        _plot_regional_mape(df_metrics, df_exp, exp_name, dir_plots)
        _plot_error_distribution(df_exp, exp_name, dir_plots)
        _plot_feature_frequency(df_exp, exp_name, dir_plots)
        _plot_mape_by_year(df_exp, exp_name, dir_plots)
        if exp_name == "ceis":
            _plot_mape_by_cei(df_exp, exp_name, dir_plots)
            _plot_mape_by_cei_region(df_exp, exp_name, dir_plots)
            _plot_mape_by_cei_year(df_exp, exp_name, dir_plots)

    _plot_overall_comparison(df_metrics, experiments, dir_plots)

    logger.info(f"Experiment analysis plots saved to {dir_plots}")


if __name__ == "__main__":
    run()
