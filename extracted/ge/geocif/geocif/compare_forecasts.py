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

# CID categories excluding forecast types. ETREF is observational (added
# after this script was last updated) — leaving it out would silently
# handicap the "No Forecast" baseline and inflate the apparent gain
# attributed to FLDAS/S2S in the delta plot.
_OBSERVATIONAL_CIDS = [
    "Cold", "Heat", "Rain", "Drought", "Temperature",
    "Compound", "Snow", "VI", "ESI", "ETREF", "h-Index", "AEF",
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


_CANON_PRED = "Predicted Yield (tn per ha)"
_CANON_OBS = "Observed Yield (tn per ha)"


def _query_mape_by_stage(db_path, table, model, experiment_name="outlook"):
    """Query predictions and compute MAPE per row.

    Returns a DataFrame with canonical yield column names so it can be passed
    directly to ``yield_outlook._aggregate_national_yields`` and
    ``yield_outlook._compute_rrmsep`` without further renaming.
    """
    if not db_path or not db_path.exists():
        return pd.DataFrame()

    con = sqlite3.connect(db_path)
    try:
        table_cols = pd.read_sql(f'PRAGMA table_info("{table}")', con)["name"].tolist()

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

    rename = {}
    if pred_col != _CANON_PRED:
        rename[pred_col] = _CANON_PRED
    if obs_col != _CANON_OBS:
        rename[obs_col] = _CANON_OBS
    if rename:
        df = df.rename(columns=rename)

    df = df.dropna(subset=[_CANON_PRED, _CANON_OBS])
    df = df[df[_CANON_OBS] != 0]
    df["MAPE"] = (df[_CANON_PRED] - df[_CANON_OBS]).abs() / df[_CANON_OBS] * 100

    return df


def _compute_mape_summary(df):
    """Compute per-region and national MAPE per stage.

    National MAPE is the metric on production-aggregated national yields
    (Σ pred·area / Σ area per year), not the area-weighted average of per-
    region MAPEs.  The two differ whenever regional errors partially cancel
    in aggregation; the former is the quantity a stakeholder summing
    predicted production into a national total would actually observe.

    Delegates to ``yield_outlook._aggregate_national_yields`` so the
    aggregation rule stays consistent with the per-config diagnostics
    produced inside each outlook run.
    """
    if df.empty:
        return pd.DataFrame(), pd.DataFrame()

    regional = df.groupby(["Stage Name", "Region"])["MAPE"].mean().reset_index()

    rows = []
    for stage, ds in df.groupby("Stage Name"):
        nat = yield_outlook._aggregate_national_yields(ds)
        nat = nat[nat[_CANON_OBS] != 0]
        if nat.empty:
            mape = ds["MAPE"].mean()
        else:
            mape = (
                (nat[_CANON_PRED] - nat[_CANON_OBS]).abs()
                / nat[_CANON_OBS] * 100
            ).mean()
        rows.append({"Stage Name": stage, "MAPE": mape})

    return regional, pd.DataFrame(rows)


def _compute_rrmsep_summary(df):
    """Per-stage rRMSEp (paper-conformant, arxiv:2506.19046 sec 5).

    Reuses ``yield_outlook._compute_rrmsep`` so the metric definition
    (pooled denominator, per-LOOCV-year numerator) stays consistent with
    the rest of the codebase.
    """
    if df.empty:
        return pd.DataFrame()

    rows = []
    for stage, ds in df.groupby("Stage Name"):
        mean_rr, _std, n_yr = yield_outlook._compute_rrmsep(
            ds, _CANON_OBS, _CANON_PRED
        )
        rows.append({"Stage Name": stage, "rRMSEp": mean_rr, "N years": n_yr})
    return pd.DataFrame(rows)


def _plot_feature_selection_comparison(
    all_features, stages_sorted, friendly_labels, n_pre,
    base_title, dir_out, fname,
):
    """One stacked-bar subplot per config, sharing the stage x-axis.

    Reveals what CID types each forced-CID-subset config ends up selecting
    at every stage. Useful for answering "when forced to FLDAS-only, does
    the model actually lean on FLDAS or fall back to lag/trend features?"
    """
    import matplotlib.pyplot as plt
    import scienceplots  # noqa: F401

    type_map = yield_outlook._build_cid_type_map()

    pivots = {}
    all_types = set()
    for config_name, df_feat in all_features.items():
        rows = []
        for _, row in df_feat.iterrows():
            stage = row["Stage Name"]
            for feat in row["features"]:
                ct = yield_outlook._feature_to_cid_type(feat, type_map)
                rows.append({"Stage Name": stage, "CID Type": ct})
        if not rows:
            continue
        df_long = pd.DataFrame(rows)
        pv = (
            df_long.groupby(["Stage Name", "CID Type"]).size()
            .reset_index(name="Count")
            .pivot_table(
                index="CID Type", columns="Stage Name",
                values="Count", fill_value=0,
            )
        )
        # Align to the unified stage axis so every subplot shares x.
        pv = pv.reindex(columns=stages_sorted, fill_value=0)
        pivots[config_name] = pv
        all_types.update(pv.index)

    if not pivots:
        return

    all_types_sorted = sorted(all_types)
    cmap = plt.cm.get_cmap("tab20", max(len(all_types_sorted), 1))
    type_colors = {t: cmap(i) for i, t in enumerate(all_types_sorted)}

    # Shared y-max so subplots are visually comparable.
    y_max = max(pv.sum(axis=0).max() for pv in pivots.values())

    n_configs = len(pivots)
    with plt.style.context(["science", "no-latex"]):
        fig, axes = plt.subplots(
            n_configs, 1,
            figsize=(max(10, len(stages_sorted) * 0.9), 3 * n_configs),
            sharex=True,
        )
        if n_configs == 1:
            axes = [axes]

        for ax, (config_name, pv) in zip(axes, pivots.items()):
            pv = pv.reindex(index=all_types_sorted, fill_value=0)
            x = np.arange(len(stages_sorted))
            bottom = np.zeros(len(stages_sorted))
            for ct in all_types_sorted:
                vals = pv.loc[ct].values
                if vals.sum() == 0:
                    continue
                ax.bar(x, vals, bottom=bottom, color=type_colors[ct],
                       width=0.8, label=ct)
                bottom += vals
            ax.set_title(config_name, fontsize=10, loc="left")
            ax.set_ylabel("# features")
            ax.set_ylim(0, y_max * 1.1)
            if 0 < n_pre < len(stages_sorted):
                ax.axvline(x=n_pre - 0.5, color="gray",
                           linestyle="--", linewidth=1.2)

        axes[-1].set_xticks(range(len(stages_sorted)))
        axes[-1].set_xticklabels(friendly_labels, rotation=45,
                                 ha="right", fontsize=8)

        # De-dup legend across subplots.
        seen = {}
        for ax in axes:
            for h, l in zip(*ax.get_legend_handles_labels()):
                seen.setdefault(l, h)
        fig.legend(
            list(seen.values()), list(seen.keys()),
            bbox_to_anchor=(1.02, 0.5), loc="center left",
            fontsize=8, title="CID Type",
        )
        fig.suptitle(f"Selected CID Types by Stage — {base_title}",
                     fontsize=11, fontweight="bold")
        plt.tight_layout()
        fig.savefig(dir_out / fname, dpi=250, bbox_inches="tight")
        plt.close(fig)


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

    from geocif.yield_outlook import (
        _stage_sort_key,
        friendly_stage_label,
        _infer_planting_month,
        _query_selected_features,
    )

    for country in countries:
        for crop in crops:
            table = f"{country}_{crop}"
            for model in models:
                # Collect MAPE / rRMSEp / selected-features data from all configs
                all_national = {}
                all_regional = {}
                all_raw = {}
                all_rrmsep = {}
                all_features = {}

                for config_name, db_path in db_paths.items():
                    df = _query_mape_by_stage(db_path, table, model)
                    if df.empty:
                        logger.warning(f"No data for {config_name} {country} {crop} {model}")
                        continue
                    regional, national = _compute_mape_summary(df)
                    all_national[config_name] = national
                    all_regional[config_name] = regional
                    all_raw[config_name] = df
                    all_rrmsep[config_name] = _compute_rrmsep_summary(df)

                    df_feat = _query_selected_features(
                        db_path, table, model, experiment_name="outlook"
                    )
                    if not df_feat.empty:
                        all_features[config_name] = df_feat

                if not all_national:
                    continue

                # Unified stage list — planting-month-aware sort. Falling
                # back to the legacy March-planting wrap would mis-order
                # stages for any Nov/Dec/Jul-planted crop, which corrupts
                # the very thing these plots are meant to show.
                all_stages = set()
                for nat_df in all_national.values():
                    all_stages.update(nat_df["Stage Name"].values)
                planting_month = _infer_planting_month(all_stages)
                stages_sorted = sorted(
                    all_stages,
                    key=lambda s: _stage_sort_key(s, planting_month),
                )
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

                # --- Plot 3: National rRMSEp comparison ---
                # Mirrors the MAPE plot but uses paper-conformant rRMSEp
                # (pooled denominator, per-LOOCV-year numerator). Same x-axis
                # and color/marker mapping so the two are visually paired.
                if any(not d.empty for d in all_rrmsep.values()):
                    with plt.style.context(["science", "no-latex"]):
                        fig, ax = plt.subplots(figsize=(12, 6))

                        for config_name, rr_df in all_rrmsep.items():
                            if rr_df.empty:
                                continue
                            rr_df = rr_df.set_index("Stage Name").reindex(stages_sorted)
                            ax.plot(
                                stages_sorted, rr_df["rRMSEp"].values,
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

                        ax.set_ylabel("rRMSEp (%)")
                        ax.set_ylim(bottom=0)
                        ax.set_title(f"Forecast Impact on rRMSEp — {base_title}")
                        ax.legend(loc="best", fontsize=8)
                        plt.tight_layout()

                        fname = f"rrmsep_comparison_national_{country}_{crop}_{model}.png"
                        fig.savefig(dir_comparison / fname, dpi=250, bbox_inches="tight")
                        plt.close(fig)

                # --- Plot 4: Selected-features comparison across configs ---
                if all_features:
                    _plot_feature_selection_comparison(
                        all_features, stages_sorted, friendly_labels, n_pre,
                        base_title, dir_comparison,
                        f"feature_selection_comparison_{country}_{crop}_{model}.png",
                    )

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
                # National rows carry both MAPE and rRMSEp; regional rows
                # carry MAPE only (rRMSEp is a multi-region quantity by
                # construction — see _compute_rrmsep).
                rrmsep_lookup = {
                    cfg: dict(zip(df["Stage Name"], df["rRMSEp"]))
                    for cfg, df in all_rrmsep.items()
                    if not df.empty
                }
                csv_rows = []
                for config_name, nat_df in all_national.items():
                    cfg_rr = rrmsep_lookup.get(config_name, {})
                    for _, row in nat_df.iterrows():
                        csv_rows.append({
                            "Config": config_name,
                            "Stage Name": row["Stage Name"],
                            "Region": "National",
                            "MAPE": row["MAPE"],
                            "rRMSEp": cfg_rr.get(row["Stage Name"], np.nan),
                        })
                for config_name, reg_df in all_regional.items():
                    for _, row in reg_df.iterrows():
                        csv_rows.append({
                            "Config": config_name,
                            "Stage Name": row["Stage Name"],
                            "Region": row["Region"],
                            "MAPE": row["MAPE"],
                            "rRMSEp": np.nan,
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
