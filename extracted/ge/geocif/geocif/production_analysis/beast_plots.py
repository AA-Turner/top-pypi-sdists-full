"""Visualizations of BEAST changepoint results.

Inputs (from ``beast_runner.run``):
  beast_results.csv, beast_top_cps.csv
  plus the raw HvStat CSV (for the case-study panel reruns of BEAST)

Outputs (under ``[BEAST].output_dir``):
  fig1_summary.png                 normalized CP year rate, #CPs hist, top crops/countries
  fig2_examples.png                case-study series with BEAST trend + CP probabilities
  fig3_heatmap_overall.png         crop x year heatmap of strong CPs
  fig4_per_crop_country_year.png   small-multiples country x year heatmaps per top crop

Run::

    from geocif.production_analysis import beast_plots
    beast_plots.run("path/to/geocif.txt")
"""
import argparse
import warnings

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scienceplots  # noqa: F401 - registers 'science' style with matplotlib

from geocif.production_analysis.config import load_config
from geocif.production_analysis import _common

warnings.filterwarnings("ignore")

_common.init_mpl_rcparams()

# Applied only to non-heatmap figures (fig1, fig2). Heatmaps keep the
# default style because scienceplots' tight serif look fights with imshow.
SCIENCE_STYLE = ["science", "no-latex"]


def _load_raw_and_results(cfg):
    df = _common.load_filtered_hvstat(cfg.input_csv)
    res = pd.read_csv(cfg.output_dir / "beast_results.csv")
    cps = pd.read_csv(cfg.output_dir / "beast_top_cps.csv")
    return df, res, cps


def _plot_summary(res, cps, output_path):
    with plt.style.context(SCIENCE_STYLE):
        fig, axes = plt.subplots(2, 2, figsize=(13, 8.5))

        ax = axes[0, 0]
        # Normalize: at each year, # strong CPs / # series active in that year.
        # Avoids the bias that mid-record years (~2008) have far more series in
        # play than 1965 or 2023, which inflated the raw count there.
        yr_min = int(res["year_start"].min())
        yr_max = int(res["year_end"].max())
        years_range = np.arange(yr_min, yr_max + 1)
        active = np.array([
            ((res["year_start"] <= Y) & (res["year_end"] >= Y)).sum()
            for Y in years_range
        ])
        cp_by_year = (cps["cp_year"].value_counts()
                          .reindex(years_range, fill_value=0).values)
        with np.errstate(divide="ignore", invalid="ignore"):
            rate = 100 * cp_by_year / np.where(active > 0, active, np.nan)
        # Hide years with very thin support — ratio is meaningless when n<20
        rate = np.where(active >= 20, rate, np.nan)

        ax.bar(years_range, rate, color="#c0392b", alpha=0.85,
               edgecolor="white", linewidth=0.5)
        ax.set_xlabel("Changepoint year")
        ax.set_ylabel("% of active series with strong CP")
        ax.set_title("(a) Strong-CP detection rate by year\n"
                     "(normalized by # series active in each year)")
        ax.axvspan(2007, 2008, color="gray", alpha=0.2, zorder=0)
        ax.text(2007.5, np.nanmax(rate) * 0.92, "2007–08\nfood crisis",
                ha="center", fontsize=8, style="italic")
        ax_n = ax.twinx()
        ax_n.plot(years_range, active, color="#7f8c8d", lw=1, alpha=0.7)
        ax_n.set_ylabel("# series active (grey)", color="#7f8c8d", fontsize=8)
        ax_n.tick_params(axis="y", labelcolor="#7f8c8d", labelsize=8)
        ax_n.grid(False)

        ax = axes[0, 1]
        ncp_counts = res["ncp_median"].value_counts(dropna=False).sort_index()
        ax.bar(ncp_counts.index, ncp_counts.values, color="#2980b9",
               alpha=0.85, edgecolor="white")
        ax.set_xlabel("Number of trend changepoints (posterior median)")
        ax.set_ylabel("Number of series")
        ax.set_title(f"(b) How many changepoints per series? (n = {len(res):,})")
        for x, y in zip(ncp_counts.index, ncp_counts.values):
            ax.text(x, y + max(ncp_counts.values) * 0.01,
                    f"{int(y)}", ha="center", fontsize=8)

        total_cps = len(cps)

        ax = axes[1, 0]
        crop_cp = (cps.groupby("product").size()
                       .sort_values(ascending=True).tail(15))
        ax.barh(crop_cp.index, crop_cp.values, color="#27ae60", alpha=0.85)
        ax.set_xlabel("Number of strong CPs")
        ax.set_title("(c) Crops with most detected changepoints")
        ax.grid(axis="y", alpha=0)
        for i, v in enumerate(crop_cp.values):
            ax.text(v + crop_cp.max() * 0.01, i,
                    f"{int(v)} ({100 * v / total_cps:.1f}%)",
                    va="center", fontsize=7.5)
        ax.set_xlim(0, crop_cp.max() * 1.22)

        ax = axes[1, 1]
        ctry_cp = (cps.groupby("country").size()
                       .sort_values(ascending=True).tail(15))
        ax.barh(ctry_cp.index, ctry_cp.values, color="#8e44ad", alpha=0.85)
        ax.set_xlabel("Number of strong CPs")
        ax.set_title("(d) Countries with most detected changepoints")
        ax.grid(axis="y", alpha=0)
        for i, v in enumerate(ctry_cp.values):
            ax.text(v + ctry_cp.max() * 0.01, i,
                    f"{int(v)} ({100 * v / total_cps:.1f}%)",
                    va="center", fontsize=7.5)
        ax.set_xlim(0, ctry_cp.max() * 1.22)

        plt.suptitle(
            "BEAST changepoint analysis · HarvestStat Africa subnational yields",
            fontsize=13, y=1.00, fontweight="bold",
        )
        plt.tight_layout()
        plt.savefig(output_path, bbox_inches="tight")
        plt.close()


def _find_series(df, country, admin, product, season, cps_label):
    """Return DataFrame for a given (country, admin, product, season, CPS)."""
    m = df[
        (df["country"] == country)
        & (df["product"] == product)
        & (df["season_name"] == season)
        & (df["crop_production_system"] == cps_label)
        & df["admin"].str.contains(admin, case=False, na=False)
    ]
    if m.empty:
        return None
    fnid = m["fnid"].iloc[0]
    return df[
        (df["fnid"] == fnid)
        & (df["product"] == product)
        & (df["season_name"] == season)
        & (df["crop_production_system"] == cps_label)
    ]


def _plot_examples(df, cfg, output_path):
    """Six case-study panels using ``cfg.example_series``."""
    picks = cfg.example_series
    nrows = (len(picks) + 1) // 2
    with plt.style.context(SCIENCE_STYLE):
        fig, axes = plt.subplots(nrows, 2, figsize=(14, 11))
        axes = np.atleast_1d(axes).flatten()

        for i, entry in enumerate(picks):
            country, admin, product, season, cps_label, note = entry
            ax = axes[i]
            sub = _find_series(df, country, admin, product, season, cps_label)
            if sub is None or sub.empty:
                ax.text(0.5, 0.5,
                        f"Not found:\n{country}/{admin}\n{product} ({season})",
                        ha="center", va="center")
                ax.set_axis_off()
                continue

            actual_admin = sub["admin"].iloc[0]
            y, y0, full = _common.build_annual_series(sub)
            years = full["harvest_year"].values

            o = _common.run_beast(y, y0, cfg)

            trend_Y = np.atleast_1d(o.trend.Y).ravel()
            trend_SD = np.atleast_1d(o.trend.SD).ravel()
            cp_occ = np.atleast_1d(o.trend.cpOccPr).ravel()

            ax.plot(years, y, "o", ms=4, color="#34495e", alpha=0.7,
                    label="observed yield")
            ax.plot(years, trend_Y, "-", color="#c0392b", lw=2,
                    label="BEAST trend")
            ax.fill_between(years, trend_Y - 1.96 * trend_SD,
                            trend_Y + 1.96 * trend_SD,
                            color="#c0392b", alpha=0.15, label="95% CI")

            ax2 = ax.twinx()
            ax2.fill_between(years, 0, cp_occ, color="#2980b9", alpha=0.35,
                             step="mid", label="P(CP)")
            ax2.set_ylim(0, 1)
            ax2.set_ylabel("P(changepoint)", color="#2980b9", fontsize=8)
            ax2.tick_params(axis="y", labelcolor="#2980b9", labelsize=8)
            ax2.grid(False)
            ax2.spines["right"].set_visible(True)

            cp_years, cp_probs = _common.extract_sorted_cps(o)
            for cy, cp in zip(cp_years, cp_probs):
                if cp >= cfg.strong_cp_threshold:
                    ax.axvline(cy, color="#c0392b", ls="--", lw=1, alpha=0.7)
                    ax.text(cy, ax.get_ylim()[1] * 0.95,
                            f"{int(cy)}\np={cp:.2f}",
                            ha="center", fontsize=7, color="#c0392b",
                            bbox=dict(boxstyle="round,pad=0.2", fc="white",
                                      ec="#c0392b", alpha=0.85))

            ax.set_title(
                f"{country} · {actual_admin} · {product} ({season})\n{note}",
                fontsize=9.5,
            )
            ax.set_xlabel("Year")
            ax.set_ylabel("Yield (t/ha)")
            if i == 0:
                ax.legend(loc="upper left", fontsize=7, framealpha=0.9)

        # Hide unused axes
        for j in range(len(picks), len(axes)):
            axes[j].set_axis_off()

        plt.suptitle(
            "BEAST decomposition: yield, posterior trend, "
            "and changepoint probability",
            fontsize=12, fontweight="bold", y=1.00,
        )
        plt.tight_layout()
        plt.savefig(output_path, bbox_inches="tight")
        plt.close()


def _plot_overall_heatmap(cps, top_n, output_path):
    top_crops = (cps.groupby("product").size().sort_values(ascending=False)
                     .head(top_n).index.tolist())
    cps_top = cps[cps["product"].isin(top_crops)]
    pivot = (cps_top.groupby(["product", "cp_year"]).size()
                    .unstack(fill_value=0)
                    .reindex(top_crops))
    pivot = pivot.loc[:, (pivot.sum(axis=0) >= 5)]

    fig, ax = plt.subplots(figsize=(14, 6))
    im = ax.imshow(
        pivot.values, aspect="auto", cmap="YlOrRd",
        extent=[pivot.columns.min() - 0.5, pivot.columns.max() + 0.5,
                len(pivot) - 0.5, -0.5],
    )
    ax.set_yticks(range(len(pivot)))
    ax.set_yticklabels(pivot.index)
    ax.set_xlabel("Changepoint year")
    ax.set_title(
        "Strong changepoints by crop and year — heatmap of detection counts",
        fontweight="bold",
    )
    cb = plt.colorbar(im, ax=ax, shrink=0.8)
    cb.set_label("# series with strong CP")
    ax.grid(False)
    plt.tight_layout()
    plt.savefig(output_path, bbox_inches="tight")
    plt.close()
    return top_crops


def _plot_per_crop_heatmaps(cps, res, top_crops, output_path):
    top_n = len(top_crops)
    all_years = sorted(cps["cp_year"].unique())
    year_min = max(1975, min(all_years))
    year_max = min(2022, max(all_years))

    ncols = 3
    nrows = int(np.ceil(top_n / ncols))
    fig, axes = plt.subplots(nrows, ncols, figsize=(18, 4.0 * nrows))
    axes = np.atleast_1d(axes).flatten()

    crop_data = {}
    vmax = 0
    for crop in top_crops:
        sub = cps[(cps["product"] == crop)
                  & (cps["cp_year"].between(year_min, year_max))]
        p = sub.groupby(["country", "cp_year"]).size().unstack(fill_value=0)
        p = p.loc[p.sum(axis=1).sort_values(ascending=False).index]
        p = p[p.sum(axis=1) >= 2]
        crop_data[crop] = p
        if p.size > 0:
            vmax = max(vmax, int(p.values.max()))

    im = None
    for i, crop in enumerate(top_crops):
        ax = axes[i]
        p = crop_data[crop]
        if p.empty:
            ax.text(0.5, 0.5, f"no data\n{crop}", ha="center", va="center")
            ax.set_axis_off()
            continue
        im = ax.imshow(
            p.values, aspect="auto", cmap="YlOrRd",
            vmin=0, vmax=vmax,
            extent=[p.columns.min() - 0.5, p.columns.max() + 0.5,
                    len(p) - 0.5, -0.5],
        )
        ax.set_yticks(range(len(p)))
        ax.set_yticklabels(p.index, fontsize=7)
        n_series = res.query("product == @crop").shape[0]
        n_strong = int(p.values.sum())
        ax.set_title(
            f"{crop}  ({n_series} series · {n_strong} strong CPs)",
            fontsize=9.5,
        )
        ax.set_xlabel("Year", fontsize=8)
        ax.tick_params(axis="x", labelsize=7)
        ax.grid(False)

    for j in range(len(top_crops), len(axes)):
        axes[j].set_axis_off()

    fig.subplots_adjust(right=0.93)
    if im is not None:
        cbar_ax = fig.add_axes([0.95, 0.15, 0.015, 0.7])
        cb = fig.colorbar(im, cax=cbar_ax)
        cb.set_label("# subnational series with strong CP", fontsize=9)

    plt.suptitle(
        "Strong changepoints by country and year, per crop "
        "(posterior probability ≥ threshold)",
        fontsize=13, fontweight="bold", y=1.0,
    )
    plt.tight_layout(rect=[0, 0, 0.93, 0.97])
    plt.savefig(output_path, bbox_inches="tight")
    plt.close()


def run(path_config_file):
    cfg = load_config(path_config_file)
    df, res, cps = _load_raw_and_results(cfg)

    _plot_summary(res, cps, cfg.output_dir / "fig1_summary.png")
    print("Saved fig1_summary.png")

    _plot_examples(df, cfg, cfg.output_dir / "fig2_examples.png")
    print("Saved fig2_examples.png")

    top_crops = _plot_overall_heatmap(
        cps, cfg.top_n_crops_heatmap, cfg.output_dir / "fig3_heatmap_overall.png"
    )
    print("Saved fig3_heatmap_overall.png")

    _plot_per_crop_heatmaps(
        cps, res, top_crops, cfg.output_dir / "fig4_per_crop_country_year.png"
    )
    print("Saved fig4_per_crop_country_year.png")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("config", nargs="+",
                   help="Path(s) to config file(s); later files override earlier")
    args = p.parse_args()
    run(args.config if len(args.config) > 1 else args.config[0])
