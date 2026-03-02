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
        parser.set("DEFAULT", "experiment_name", f"models_models_{model}")
        # Override every country's models list to just this one model
        for country in countries:
            parser.set(country, "models", f'["{model}"]')

        inputs = gc.gather_inputs(parser)
        gc.execute_models(inputs, logger, parser)

    # Restore originals
    for country, orig in originals.items():
        parser.set(country, "models", orig)

    return parser


# ---------------------------------------------------------------------------
# Bayesian hyperparameter optimization (Optuna TPE)
# ---------------------------------------------------------------------------

def _extract_trial_mape(parser, experiment_name):
    """Extract mean APE for a specific experiment trial from the results DB."""
    dir_output = Path(parser.get("PATHS", "dir_output"))
    db_name = parser.get("DEFAULT", "db")
    db_path = dir_output / "ml" / "db" / db_name

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
    ml_keys = [
        "feature_selection", "lag_years", "lag_yield_as_feature",
        "median_years", "median_yield_as_feature",
        "analogous_year_yield_as_feature", "check_yield_trend",
    ]
    originals = {key: parser.get("ML", key) for key in ml_keys}

    def objective(trial):
        params = {
            "feature_selection": trial.suggest_categorical(
                "feature_selection",
                ["SelectKBest", "BorutaPy", "Leshy", "RFECV", "RFE", "gOMP", "none"],
            ),
            "lag_years": trial.suggest_int("lag_years", 1, 5),
            "lag_yield_as_feature": trial.suggest_categorical(
                "lag_yield_as_feature", ["True", "False"],
            ),
            "median_years": trial.suggest_int("median_years", 2, 5),
            "median_yield_as_feature": trial.suggest_categorical(
                "median_yield_as_feature", ["True", "False"],
            ),
            "analogous_year_yield_as_feature": trial.suggest_categorical(
                "analogous_year_yield_as_feature", ["True", "False"],
            ),
            "check_yield_trend": trial.suggest_categorical(
                "check_yield_trend", ["True", "False"],
            ),
        }

        experiment_name = f"optuna_trial_{trial.number}"
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
    today = ar.utcnow().to("America/New_York").format("MMMM_DD_YYYY")
    dir_plots = dir_output / "ml" / "analysis" / today / "optimization"
    os.makedirs(dir_plots, exist_ok=True)

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
        ("feature_selection", ["SelectKBest", "BorutaPy", "Leshy", "RFECV", "RFE", "gOMP", "none"]),
        ("lag_years", list(range(1, 6))),
        ("lag_yield_as_feature", [True, False]),
        ("median_years", list(range(2, 6))),
        ("median_yield_as_feature", [True, False]),
        ("analogous_year_yield_as_feature", [True, False]),
        ("check_yield_trend", [True, False]),
    ]

    total_combos = 1
    for _, values in hp_space:
        total_combos *= len(values)

    params = gc._build_summary_params(parser, inputs)
    params.append(("Exp 0: models", ", ".join(model_experiment)))
    params.append(("Optimization", f"Optuna TPE, {n_trials} trials"))
    for name, values in hp_space:
        params.append((f"  {name}", ", ".join(str(v) for v in values)))
    params.append(("Search space", f"{total_combos} combinations"))
    ut.display_run_summary("GeoCIF Experiments Runner", params, wait=20)

    # Experiment 0: model comparison
    logger.info("Experiment 0: Model comparison")
    parser = main_models(logger, parser, model_experiment)

    # Bayesian hyperparameter optimization
    logger.info(f"Starting Optuna optimization ({n_trials} trials)...")
    study = optimize_hyperparameters(inputs, logger, parser, n_trials=n_trials)

    # Analyze model comparison (Experiment 0)
    model_exp_list = [("models", "models", "models", "str", model_experiment)]
    analyze_experiments(parser, model_exp_list, logger)

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
        return pd.Series(dtype=float)
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
    db_name = parser.get("DEFAULT", "db")
    db_path = dir_output / "ml" / "db" / db_name

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
    return df_all[df_all["experiment"] != "unknown"].copy()


def _plot_heatmap(df_metrics, experiment_name, dir_plots):
    """Plot 1: Heatmap of mean MAPE — countries vs parameter values."""
    df_exp = df_metrics[df_metrics["experiment"] == experiment_name]
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
    df_exp = df_exp_data[df_exp_data["experiment"] == experiment_name].copy()
    if df_exp.empty:
        return

    obs = df_exp["Observed Yield (tn per ha)"]
    pred = df_exp["Predicted Yield (tn per ha)"]
    valid = obs.notna() & pred.notna() & (obs != 0)
    df_exp = df_exp[valid].copy()
    df_exp["APE_calc"] = np.abs((obs[valid] - pred[valid]) / obs[valid]) * 100

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


def _plot_regional_mape(df_metrics, experiment_name, dir_plots):
    """Plot 3: Regional MAPE bar chart per country."""
    df_exp = df_metrics[df_metrics["experiment"] == experiment_name]
    if df_exp.empty or "Region" not in df_exp.columns:
        return

    for country in df_exp["Country"].unique():
        df_c = df_exp[df_exp["Country"] == country]
        if df_c.empty:
            continue

        pivot = df_c.pivot_table(
            index="Region", columns="param_value", values="MAPE", aggfunc="mean"
        )
        if pivot.empty:
            continue

        fig, ax = plt.subplots(figsize=(max(10, len(pivot.columns) * 1.2), max(5, len(pivot) * 0.4)))
        pivot.plot(kind="barh", ax=ax)
        ax.set_title(f"Mean MAPE by Region — {experiment_name} — {country}")
        ax.set_xlabel("MAPE (%)")
        ax.set_ylabel("Region")
        ax.legend(title="Value", bbox_to_anchor=(1.02, 1), loc="upper left", fontsize=8)
        plt.tight_layout()
        fig.savefig(dir_plots / f"regional_mape_{experiment_name}_{country}.png", dpi=250)
        plt.close(fig)


def _plot_overall_comparison(df_metrics, experiments, dir_plots):
    """Plot 4: Summary — best parameter value per experiment, grouped by country."""
    rows = []
    for name, *_ in experiments:
        df_exp = df_metrics[df_metrics["experiment"] == name]
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
    df_exp = df_exp_data[df_exp_data["experiment"] == experiment_name].copy()
    if df_exp.empty:
        return

    obs = df_exp["Observed Yield (tn per ha)"]
    pred = df_exp["Predicted Yield (tn per ha)"]
    valid = obs.notna() & pred.notna() & (obs != 0)
    df_exp = df_exp[valid].copy()
    df_exp["APE_calc"] = np.abs((obs[valid] - pred[valid]) / obs[valid]) * 100

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


def analyze_experiments(parser, experiments, logger):
    """Read experiment results from DB and generate comparison plots."""
    logger.info("Analyzing experiment results...")

    df_exp = _load_experiment_results(parser, experiments)
    if df_exp.empty:
        logger.warning("No experiment results found in database")
        return

    dir_output = Path(parser.get("PATHS", "dir_output"))
    today = ar.utcnow().to("America/New_York").format("MMMM_DD_YYYY")
    dir_plots = dir_output / "ml" / "analysis" / today / "experiments"
    os.makedirs(dir_plots, exist_ok=True)

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
        _plot_regional_mape(df_metrics, exp_name, dir_plots)
        _plot_error_distribution(df_exp, exp_name, dir_plots)

    _plot_overall_comparison(df_metrics, experiments, dir_plots)

    logger.info(f"Experiment analysis plots saved to {dir_plots}")


if __name__ == "__main__":
    run()
