"""Compare forecast impact on crop yield prediction accuracy.

Runs yield_outlook with 4 different CID configurations and compares
MAPE scores across time steps (pre-season through in-season).

Usage::

    from geocif import compare_forecasts
    compare_forecasts.run(cfg)

Configurations compared:
    1. All CIDs (baseline)
    2. No forecast data (observational CIDs only)
    3. FLDAS only
    4. S2S only
"""

import ast
import logging
import os
import sqlite3
from pathlib import Path

import arrow as ar
import numpy as np
import pandas as pd

from geocif import yield_outlook
from geocif import logger as log

logger = logging.getLogger(__name__)

# CID categories excluding forecast types
_OBSERVATIONAL_CIDS = [
    "Cold", "Heat", "Rain", "Drought", "Temperature",
    "Compound", "Snow", "VI", "ESI", "h-Index", "AEF",
]

CONFIGS = {
    "All CIDs": "['all']",
    "No Forecast": str(_OBSERVATIONAL_CIDS),
    "FLDAS Only": "['FLDAS']",
    "S2S Only": "['S2S']",
}


def _run_single_config(cfg, config_name, use_cids_str, parent_dir, since_year=None):
    """Run yield_outlook with a specific use_cids and return the DB path."""
    logger_obj, parser = log.setup_logger_parser(cfg)

    # Override use_cids in DEFAULT and ALL model-specific sections
    parser.set("DEFAULT", "use_cids", use_cids_str)
    parser.set("DEFAULT", "select_cid_by", "Type")
    for section in parser.sections():
        if parser.has_option(section, "use_cids"):
            parser.set(section, "use_cids", use_cids_str)
        if parser.has_option(section, "select_cid_by"):
            parser.set(section, "select_cid_by", "Type")

    # Config-specific DB name and analysis subfolder
    config_safe = config_name.lower().replace(" ", "_")
    db_name = f"comparison_{config_safe}.db"
    analysis_dir = parent_dir / config_safe

    logger.info(f"=== Running: {config_name} (use_cids={use_cids_str}) ===")

    yield_outlook.run(parser=parser, logger_obj=logger_obj, since_year=since_year,
                      outlook_db_name=db_name, analysis_dir=analysis_dir)

    # Return the DB path
    project_name = parser.get("DEFAULT", "project_name", fallback="geocif")
    dir_output = Path(parser.get("PATHS", "dir_output")) / project_name
    db_path = dir_output / "ml" / "db" / db_name
    if not db_path.exists():
        logger.error(f"DB not found for {config_name}: {db_path}")
        return None
    return db_path


def _query_mape_by_stage(db_path, table, model, experiment_name="outlook"):
    """Query predictions and compute MAPE per (Region, Stage Name)."""
    if not db_path or not db_path.exists():
        return pd.DataFrame()

    con = sqlite3.connect(db_path)
    try:
        table_cols = pd.read_sql(f'PRAGMA table_info("{table}")', con)["name"].tolist()

        # Find yield columns
        pred_col = next((c for c in table_cols if "predicted" in c.lower() and "yield" in c.lower()), None)
        obs_col = next((c for c in table_cols if "observed" in c.lower() and "yield" in c.lower()), None)
        if not pred_col or not obs_col:
            return pd.DataFrame()

        area_select = ', "Area (ha)"' if "Area (ha)" in table_cols else ""

        df = pd.read_sql(
            f'SELECT "Country", "Region", "Harvest Year", "Stage Name", '
            f'"{pred_col}", "{obs_col}"{area_select} '
            f'FROM "{table}" WHERE "Experiment Name" = ? AND "Model" = ?',
            con, params=(experiment_name, model),
        )
    except Exception as e:
        logger.error(f"Query failed for {db_path}: {e}")
        return pd.DataFrame()
    finally:
        con.close()

    if df.empty:
        return pd.DataFrame()

    df = df.rename(columns={pred_col: "Predicted", obs_col: "Observed"})
    df = df.dropna(subset=["Predicted", "Observed"])
    df = df[df["Observed"] != 0]
    df["MAPE"] = (df["Predicted"] - df["Observed"]).abs() / df["Observed"] * 100

    return df


def _compute_mape_summary(df):
    """Compute per-region and national MAPE per stage.

    National MAPE is the metric on production-aggregated national yields
    (Σ pred·area / Σ area per year), not the area-weighted average of per-
    region MAPEs.  The two differ whenever regional errors partially cancel
    in aggregation; the former is the quantity a stakeholder summing
    predicted production into a national total would actually observe.
    """
    if df.empty:
        return pd.DataFrame(), pd.DataFrame()

    # Per-region MAPE
    regional = df.groupby(["Stage Name", "Region"])["MAPE"].mean().reset_index()

    has_area = "Area (ha)" in df.columns and df["Area (ha)"].notna().any()
    rows = []
    for stage in df["Stage Name"].unique():
        ds = df[df["Stage Name"] == stage]
        national = np.nan
        if has_area:
            ds2 = ds.copy()
            ds2["_prod_obs"] = ds2["Observed"] * ds2["Area (ha)"]
            ds2["_prod_pred"] = ds2["Predicted"] * ds2["Area (ha)"]
            nat = ds2.groupby("Harvest Year").agg(
                _prod_obs=("_prod_obs", "sum"),
                _prod_pred=("_prod_pred", "sum"),
                _area=("Area (ha)", "sum"),
            )
            nat = nat[(nat["_area"] > 0) & (nat["_prod_obs"] != 0)]
            if not nat.empty:
                obs_y = nat["_prod_obs"] / nat["_area"]
                pred_y = nat["_prod_pred"] / nat["_area"]
                national = ((pred_y - obs_y).abs() / obs_y * 100).mean()
        if pd.isna(national):
            national = ds["MAPE"].mean()
        rows.append({"Stage Name": stage, "MAPE": national})

    national_df = pd.DataFrame(rows)
    return regional, national_df


def run(path_config_files=None, since_year=None):
    """Run 4 yield_outlook configurations and compare MAPE.

    Args:
        path_config_files: List of config file paths.
        since_year: Start year for ML execution.
    """
    import matplotlib.pyplot as plt
    import scienceplots  # noqa: F401

    if path_config_files is None:
        path_config_files = [Path("../config/geocif.txt")]

    _, parser = log.setup_logger_parser(path_config_files)

    # Determine country/crop/model from config
    countries = ast.literal_eval(parser.get("DEFAULT", "countries"))
    crops = ast.literal_eval(parser.get("DEFAULT", "crops"))
    models = ast.literal_eval(parser.get("DEFAULT", "models"))

    # Create parent folder for all comparison runs
    project_name = parser.get("DEFAULT", "project_name", fallback="geocif")
    dir_output = Path(parser.get("PATHS", "dir_output")) / project_name
    today = ar.utcnow().to("America/New_York").format("MMMM_DD_YYYY_HH[h]mm")
    parent_dir = dir_output / "ml" / "analysis" / today

    # Run all 4 configs
    db_paths = {}
    for config_name, use_cids_str in CONFIGS.items():
        db_paths[config_name] = _run_single_config(
            path_config_files, config_name, use_cids_str,
            parent_dir=parent_dir, since_year=since_year,
        )

    # Comparison plots go in the parent folder
    dir_comparison = parent_dir / "comparison_plots"
    os.makedirs(dir_comparison, exist_ok=True)

    from geocif.yield_outlook import _stage_sort_key, friendly_stage_label

    for country in countries:
        for crop in crops:
            table = f"{country}_{crop}"
            for model in models:
                # Collect MAPE data from all configs
                all_national = {}
                all_regional = {}
                all_raw = {}

                for config_name, db_path in db_paths.items():
                    df = _query_mape_by_stage(db_path, table, model)
                    if df.empty:
                        logger.warning(f"No data for {config_name} {country} {crop} {model}")
                        continue
                    regional, national = _compute_mape_summary(df)
                    all_national[config_name] = national
                    all_regional[config_name] = regional
                    all_raw[config_name] = df

                if not all_national:
                    continue

                # Unified stage list
                all_stages = set()
                for nat_df in all_national.values():
                    all_stages.update(nat_df["Stage Name"].values)
                stages_sorted = sorted(all_stages, key=_stage_sort_key)
                friendly_labels = [friendly_stage_label(s) for s in stages_sorted]

                n_pre = sum(1 for s in stages_sorted if s.startswith("Pre-Season"))
                base_title = f"{country.title().replace('_', ' ')} {crop.title().replace('_', ' ')} ({model})"

                colors = {
                    "All CIDs": "black",
                    "No Forecast": "#d62728",
                    "FLDAS Only": "#1f77b4",
                    "S2S Only": "#2ca02c",
                }
                markers = {
                    "All CIDs": "o",
                    "No Forecast": "s",
                    "FLDAS Only": "D",
                    "S2S Only": "^",
                }

                # --- Plot 1: National MAPE comparison ---
                with plt.style.context(["science", "no-latex"]):
                    fig, ax = plt.subplots(figsize=(12, 6))

                    for config_name, nat_df in all_national.items():
                        nat_df = nat_df.set_index("Stage Name").reindex(stages_sorted)
                        ax.plot(
                            stages_sorted, nat_df["MAPE"].values,
                            color=colors.get(config_name, "gray"),
                            marker=markers.get(config_name, "o"),
                            linewidth=2, markersize=6, label=config_name,
                        )

                    ax.set_xticks(range(len(stages_sorted)))
                    ax.set_xticklabels(friendly_labels, rotation=45, ha="right", fontsize=8)

                    if 0 < n_pre < len(stages_sorted):
                        ax.axvline(x=n_pre - 0.5, color="gray", linestyle="--", linewidth=1.2)
                        ax.text(n_pre - 0.5, ax.get_ylim()[1] * 0.97, " Start of planting",
                                fontsize=7, color="gray", ha="left", va="top")

                    ax.set_ylabel("Mean Absolute Percentage Error (%)")
                    ax.set_ylim(bottom=0)
                    ax.set_title(f"Forecast Impact on MAPE — {base_title}")
                    ax.legend(loc="best", fontsize=8)
                    plt.tight_layout()

                    fname = f"mape_comparison_national_{country}_{crop}_{model}.png"
                    fig.savefig(dir_comparison / fname, dpi=250, bbox_inches="tight")
                    plt.close(fig)

                # --- Plot 2: Delta (improvement from adding forecasts) ---
                if "No Forecast" in all_national and len(all_national) > 1:
                    baseline = all_national["No Forecast"].set_index("Stage Name").reindex(stages_sorted)

                    with plt.style.context(["science", "no-latex"]):
                        fig, ax = plt.subplots(figsize=(12, 6))

                        for config_name, nat_df in all_national.items():
                            if config_name == "No Forecast":
                                continue
                            nat_df = nat_df.set_index("Stage Name").reindex(stages_sorted)
                            delta = baseline["MAPE"].values - nat_df["MAPE"].values
                            ax.plot(
                                stages_sorted, delta,
                                color=colors.get(config_name, "gray"),
                                marker=markers.get(config_name, "o"),
                                linewidth=2, markersize=6, label=config_name,
                            )

                        ax.axhline(y=0, color="gray", linestyle="-", linewidth=0.8)
                        ax.set_xticks(range(len(stages_sorted)))
                        ax.set_xticklabels(friendly_labels, rotation=45, ha="right", fontsize=8)

                        if 0 < n_pre < len(stages_sorted):
                            ax.axvline(x=n_pre - 0.5, color="gray", linestyle="--", linewidth=1.2)

                        ax.set_ylabel("MAPE reduction (pp)")
                        ax.set_title(f"MAPE Improvement from Forecast Data — {base_title}")
                        ax.legend(loc="best", fontsize=8)

                        # Shade positive region (forecast helps)
                        ymin, ymax = ax.get_ylim()
                        if ymax > 0:
                            ax.fill_between(range(len(stages_sorted)), 0, ymax,
                                            alpha=0.05, color="green", label="_nolegend_")
                        if ymin < 0:
                            ax.fill_between(range(len(stages_sorted)), ymin, 0,
                                            alpha=0.05, color="red", label="_nolegend_")
                        plt.tight_layout()

                        fname = f"mape_comparison_delta_{country}_{crop}_{model}.png"
                        fig.savefig(dir_comparison / fname, dpi=250, bbox_inches="tight")
                        plt.close(fig)

                # --- Per-region comparison ---
                all_regions = set()
                for reg_df in all_regional.values():
                    all_regions.update(reg_df["Region"].values)

                for region in sorted(all_regions):
                    with plt.style.context(["science", "no-latex"]):
                        fig, ax = plt.subplots(figsize=(12, 6))

                        for config_name, reg_df in all_regional.items():
                            rdf = reg_df[reg_df["Region"] == region]
                            rdf = rdf.set_index("Stage Name").reindex(stages_sorted)
                            ax.plot(
                                stages_sorted, rdf["MAPE"].values,
                                color=colors.get(config_name, "gray"),
                                marker=markers.get(config_name, "o"),
                                linewidth=2, markersize=5, label=config_name,
                            )

                        ax.set_xticks(range(len(stages_sorted)))
                        ax.set_xticklabels(friendly_labels, rotation=45, ha="right", fontsize=8)

                        if 0 < n_pre < len(stages_sorted):
                            ax.axvline(x=n_pre - 0.5, color="gray", linestyle="--", linewidth=1.2)

                        ax.set_ylabel("Mean Absolute Percentage Error (%)")
                        ax.set_ylim(bottom=0)
                        ax.set_title(f"Forecast Impact — {region} — {base_title}")
                        ax.legend(loc="best", fontsize=8)
                        plt.tight_layout()

                        region_safe = region.lower().replace(" ", "_")
                        fname = f"mape_comparison_{region_safe}_{country}_{crop}_{model}.png"
                        fig.savefig(dir_comparison / fname, dpi=250, bbox_inches="tight")
                        plt.close(fig)

                # --- CSV ---
                csv_rows = []
                for config_name, nat_df in all_national.items():
                    for _, row in nat_df.iterrows():
                        csv_rows.append({
                            "Config": config_name,
                            "Stage Name": row["Stage Name"],
                            "Region": "National",
                            "MAPE": row["MAPE"],
                        })
                for config_name, reg_df in all_regional.items():
                    for _, row in reg_df.iterrows():
                        csv_rows.append({
                            "Config": config_name,
                            "Stage Name": row["Stage Name"],
                            "Region": row["Region"],
                            "MAPE": row["MAPE"],
                        })
                df_csv = pd.DataFrame(csv_rows)
                stage_order = {s: i for i, s in enumerate(stages_sorted)}
                df_csv["_order"] = df_csv["Stage Name"].map(stage_order)
                df_csv = df_csv.sort_values(["Config", "_order", "Region"]).drop(columns="_order")
                df_csv.to_csv(
                    dir_comparison / f"mape_comparison_{country}_{crop}_{model}.csv",
                    index=False,
                )

                logger.info(f"Comparison plots saved to {dir_comparison}")
