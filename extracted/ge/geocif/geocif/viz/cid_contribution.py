"""CID contribution: per-year R² as CID classes are added, best class first.

yield_outlook's ``[ML] cid_contribution`` retrains the run's best ML model on
subsets of the CID classes (the category column of cid/definitions.py: Heat,
Rain, VI, ESI, FPAR, ...) and tags each run in the outlook DB's
"Experiment Name":

    cidc_single_<Class>      the class alone -- ranks the classes
    cidc_cum_<kk>_<Class>    the kk best classes, <Class> added last

Step 1 of the cumulative series IS the best class's single run, so it is not
rerun. Step 0 is the outlook run's own ``trend`` baseline (no CIDs). The figure
has one box of per-year R² per step: the learning-curve layout, with "classes
added" on the x-axis in place of training-set size.

Scoring follows the yield-model-analysis rules: final stage only, every arm
cut to the region-years all arms scored, and R² = r2_score across the regions
of one held-out year.
"""

import logging
import re
from pathlib import Path

import pandas as pd

from geocif.ml.stage_labels import latest_stage_rows

logger = logging.getLogger(__name__)

OBS = "Observed Yield (tn per ha)"
PRED = "Predicted Yield (tn per ha)"
SINGLE = "cidc_single_"
CUM = "cidc_cum_"
PREFIX = "cidc_"
TREND = "trend"
MIN_REGIONS = 3

_KEY = ("Region", "Season", "Harvest Year")
# Okabe-Ito; the trend box is also named by its tick label, not colour alone.
_MODEL_COLOR = "#0072B2"
_TREND_COLOR = "#009E73"


def classes_from_columns(columns, use_cids, drop_bases=()):
    """CID classes behind a model's input columns, as the config allows them.

    A feature column is ``"<CID base> <stage>"`` (static ones are the bare
    base), so its first token looks the class up in ``cid_category_map``;
    non-CID columns (Region, lag yields, lat/lon) match nothing. Bases in
    ``drop_bases`` (exclude_cids + exclude_cid_categories, already expanded)
    are skipped, so a class whose every index is excluded drops out. With
    ``use_cids`` other than ['all'], only the listed classes are kept.
    """
    from geocif.ml.stages import cid_category_map

    cmap = cid_category_map()
    drop = set(drop_bases)
    bases = {str(c).split(" ")[0] for c in columns}
    found = {cmap[b] for b in bases if b in cmap and b not in drop}
    if "all" not in use_cids:
        found &= set(use_cids)
    return sorted(found)


def per_year_r2(df, arm_col):
    """Per-year R² of every arm on a common, final-stage sample.

    ``df`` holds prediction rows (``OBS``/``PRED``, Region, Harvest Year,
    Stage Name, optional Season / Stage Window Display) plus ``arm_col``
    naming the run each row came from. Each arm keeps its chronologically
    last stage per region-year; then every arm is cut to the region-years all
    arms scored, so arms differ only in their inputs. Years with fewer than
    ``MIN_REGIONS`` regions are dropped.

    Returns columns [arm_col, "Harvest Year", "N Regions", "R2"].
    """
    from sklearn.metrics import r2_score

    cols = [arm_col, "Harvest Year", "N Regions", "R2"]
    d = df.dropna(subset=[OBS, PRED])
    key = [c for c in _KEY if c in d.columns]
    d = latest_stage_rows(d, by=[arm_col] + key, keep="last")
    if d is None or d.empty:
        return pd.DataFrame(columns=cols)

    logger.info(
        f"cid_contribution: region-years per arm before the common cut "
        f"{d.groupby(arm_col).size().to_dict()}"
    )
    n_arms = d[arm_col].nunique()
    d = d[d.groupby(key, dropna=False)[arm_col].transform("nunique") == n_arms]

    rows = [
        (arm, year, len(g), r2_score(g[OBS], g[PRED]))
        for (arm, year), g in d.groupby([arm_col, "Harvest Year"])
        if len(g) >= MIN_REGIONS
    ]
    return pd.DataFrame(rows, columns=cols)


def rank_classes(df):
    """Rank classes by stand-alone skill, best first.

    Uses the ``cidc_single_*`` rows of ``df``. Score = median per-year R² on
    the sample every single-class run scored; ties go alphabetically so the
    order is reproducible. Returns [Class, Median R2, Mean R2, N Years].
    """
    cols = ["Class", "Median R2", "Mean R2", "N Years"]
    if df.empty:
        return pd.DataFrame(columns=cols)
    single = df[df["Experiment Name"].str.startswith(SINGLE)]
    if single.empty:
        return pd.DataFrame(columns=cols)
    single = single.assign(Class=single["Experiment Name"].str[len(SINGLE):])
    r2 = per_year_r2(single, "Class")
    if r2.empty:
        return pd.DataFrame(columns=cols)
    out = r2.groupby("Class")["R2"].agg(["median", "mean", "size"]).reset_index()
    out.columns = cols
    return out.sort_values(["Median R2", "Class"], ascending=[False, True],
                           ignore_index=True)


def cumulative_r2(df, model):
    """Per-year R² for each step of ``model``'s cumulative series.

    ``df`` holds the cidc_* rows plus the outlook run's trend rows. Step 0 is
    trend, step 1 the best class alone (per :func:`rank_classes`), step k the
    ``cidc_cum_<k>`` run. Returns ``(r2, ranking)``; ``r2`` has
    [Step, Class, Harvest Year, N Regions, R2].
    """
    ranking = rank_classes(df[df["Model"] == model])
    if ranking.empty:
        return pd.DataFrame(), ranking
    top = ranking["Class"].iloc[0]

    def _step(experiment, row_model):
        if experiment == "outlook" and row_model == TREND:
            return 0, "Trend"
        if row_model != model:
            return None, None
        if experiment == f"{SINGLE}{top}":
            return 1, top
        m = re.match(rf"^{CUM}(\d+)_(.+)$", experiment)
        return (int(m.group(1)), m.group(2)) if m else (None, None)

    arms = df[["Experiment Name", "Model"]].drop_duplicates()
    arms[["Step", "Class"]] = [_step(e, m) for e, m in arms.itertuples(index=False)]
    arms = arms.dropna(subset=["Step"]).astype({"Step": int})
    d = df.merge(arms, on=["Experiment Name", "Model"])

    r2 = per_year_r2(d, "Step")
    r2.insert(1, "Class", r2["Step"].map(arms.set_index("Step")["Class"]))
    return r2, ranking


def plot_contribution(r2, model, title, path_png):
    """One box of per-year R² per step: Trend, +class 1, +class 2, ..."""
    import matplotlib.pyplot as plt
    from matplotlib.patches import Patch

    from geocif.utils import display_model_name
    from geocif.viz._style import despine, style_ctx

    steps = r2[["Step", "Class"]].drop_duplicates("Step").sort_values("Step")
    with style_ctx():
        fig, ax = plt.subplots(figsize=(max(6.0, 0.7 * len(steps) + 2), 4.2))
        for step in steps["Step"]:
            color = _TREND_COLOR if step == 0 else _MODEL_COLOR
            bp = ax.boxplot(
                [r2.loc[r2["Step"] == step, "R2"].to_numpy()],
                positions=[step], widths=0.6, patch_artist=True,
                manage_ticks=False,
                medianprops={"color": "black", "linewidth": 1.2},
                flierprops={"marker": "o", "markersize": 4,
                            "markerfacecolor": "none", "markeredgecolor": color},
            )
            for patch in bp["boxes"]:
                patch.set_facecolor(color)
                patch.set_edgecolor("black")

        ax.set_xticks(steps["Step"].to_list())
        ax.set_xticklabels(
            ["Trend" if s == 0 else f"+{c}"
             for s, c in zip(steps["Step"], steps["Class"])],
            rotation=45, ha="right",
        )
        ax.set_xlim(steps["Step"].min() - 0.6, steps["Step"].max() + 0.6)
        ax.tick_params(axis="x", which="minor", bottom=False)
        ax.set_xlabel("CID Classes Added (Cumulative)")
        ax.set_ylabel("R²")
        ax.set_title(title)
        despine(ax)

        handles = [Patch(facecolor=_MODEL_COLOR, edgecolor="black",
                         label=display_model_name(model))]
        if (steps["Step"] == 0).any():
            handles.append(Patch(facecolor=_TREND_COLOR, edgecolor="black",
                                 label="Trend"))
        fig.tight_layout()
        fig.legend(handles=handles, loc="upper center",
                   bbox_to_anchor=(0.5, 0.0), ncol=len(handles), frameon=False)
        fig.savefig(path_png, dpi=300, bbox_inches="tight")
        plt.close(fig)


def render(df, country, crop, dir_outlook):
    """Write the figure, its CSV, the ranking CSV and the lookup per model.

    ``df`` is every cidc_* row of one country x crop table plus the outlook
    run's trend rows. Output lands under
    ``plots|csvs/{model}/{country}/{crop}/cid_contribution/``. Returns the
    PNG paths written.
    """
    from geocif.utils import display_name

    written = []
    is_cidc = df["Experiment Name"].str.startswith(PREFIX)
    for model in sorted(df.loc[is_cidc, "Model"].unique()):
        r2, ranking = cumulative_r2(df, model)
        if r2.empty or r2["Step"].nunique() < 2:
            continue

        dir_plots = Path(dir_outlook) / "plots" / model / country / crop / "cid_contribution"
        dir_csvs = Path(dir_outlook) / "csvs" / model / country / crop / "cid_contribution"
        dir_plots.mkdir(parents=True, exist_ok=True)
        dir_csvs.mkdir(parents=True, exist_ok=True)

        stem = f"r2_{country}_{crop}_{model}_cid_contribution"
        rank_stem = f"ranking_{country}_{crop}_{model}_cid_contribution"
        plot_contribution(r2, model, f"{display_name(country)} {display_name(crop)}",
                          dir_plots / f"{stem}.png")
        r2.to_csv(dir_csvs / f"{stem}.csv", index=False)
        ranking.to_csv(dir_csvs / f"{rank_stem}.csv", index=False)

        lookup = pd.DataFrame(
            [(f"{stem}.png", f"{stem}.csv",
              "per-year R² as CID classes are added, best class first"),
             (f"{stem}.png", f"{rank_stem}.csv",
              "stand-alone class ranking that sets the order")],
            columns=["plot_file", "csv_file", "description"],
        )
        lookup.to_csv(dir_plots / "lookup_plots_csvs.csv", index=False)
        lookup.to_csv(dir_csvs / "lookup_plots_csvs.csv", index=False)
        written.append(dir_plots / f"{stem}.png")
    return written
