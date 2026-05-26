"""Spatial co-occurrence analysis of BEAST changepoints (PySAL).

Answers the science follow-up to ``beast_runner``: do the detected
changepoints (CPs) tend to cluster spatially, both per-year and per-
region? Runs three independent tests on the same boundary-merged data:

1. **Global Moran's I** per (country, crop): is the count of CPs per
   region spatially autocorrelated across the full record?
2. **Local Moran / LISA** per region: HH/LL/LH/HL/NS cluster labels —
   identifies persistent hotspots and cold-spots.
3. **Join-Count BB** per (country, crop, CP year): for each major CP
   year, is the binary "had a CP this year" indicator significantly
   clustered vs spatially random?

Inputs (under ``[BEAST].output_dir`` — must run ``beast_runner.run()``
first):
  beast_top_cps.csv

Outputs (same dir):
  beast_spatial_morans.csv         one row per (country, crop) global I
  beast_spatial_lisa.csv           one row per (country, crop, region) local I
  beast_spatial_join_counts.csv    one row per (country, crop, cp_year) BB
  fig6_spatial_summary.png         three-panel summary figure

Run::

    from geocif.production_analysis import beast_spatial
    beast_spatial.run("path/to/geocif.txt")

pysal is loaded lazily — if ``libpysal`` / ``esda`` are not installed
the run logs a clear message and returns cleanly. Install with
``pip install geocif[spatial]``.
"""
import logging
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scienceplots  # noqa: F401 — registers the "science" style

from geocif.production_analysis.config import load_config
from geocif.production_analysis import _common
from geocif import utils

logger = logging.getLogger(__name__)


def _try_import_pysal():
    """Soft-import the pysal stack. Returns ``(libpysal, esda)`` or
    ``(None, None)`` with an info log when the extras aren't installed.
    """
    try:
        import libpysal
        import esda
        return libpysal, esda
    except ImportError as exc:
        logger.info(
            "beast_spatial: pysal not available (%s) — install with "
            "'pip install geocif[spatial]'. Skipping spatial analysis.",
            exc,
        )
        return None, None


def _load_country_gdf(parser, country, cfg_boundary_shp):
    """Load + filter a country's admin boundaries.

    Prefers the explicit ``[BEAST] boundary_shp`` config entry; falls
    back to the standard ``${PATHS:dir_boundary_files}/gaul2014_admin1.shp``
    when unset. Reuses ``utils.load_country_boundary_gdf`` so the column
    rename / Tanzania normalisation stay consistent with the rest of
    geocif.
    """
    if cfg_boundary_shp is not None:
        shp = cfg_boundary_shp
    else:
        try:
            base = Path(parser.get("PATHS", "dir_boundary_files"))
        except Exception:  # noqa: BLE001
            return None
        shp = base / "gaul2014_admin1.shp"
    if not Path(shp).exists():
        logger.warning("  boundary shapefile not found: %s", shp)
        return None
    try:
        gdf = utils.load_country_boundary_gdf(parser, shp, country=country)
    except Exception as exc:  # noqa: BLE001
        logger.warning("  load_country_boundary_gdf failed for %s: %s", country, exc)
        return None
    return gdf


_LISA_QUADRANTS = ["NS", "HH", "LH", "LL", "HL"]


def _run_one_country_crop(country, product, grp, gdf, libpysal, esda):
    """Run all three spatial tests for one (country, crop). Returns
    three lists of dicts (morans_rows, lisa_rows, join_count_rows).
    """
    morans_rows, lisa_rows, join_count_rows = [], [], []

    gdf_col, df_col = _common.pick_admin_col(gdf, grp)
    if gdf_col is None:
        logger.info(
            "  %s / %s: no admin-column overlap between gdf and CPs — skipped",
            country, product,
        )
        return morans_rows, lisa_rows, join_count_rows

    # Per-region CP count (after dedup at series level — one CP per
    # (region, fnid, year), since a region may have multiple series).
    cp_count = (
        grp.drop_duplicates(subset=["fnid", "cp_year"])
        .groupby(df_col).size().reset_index(name="n_cps")
    )
    # Normalise both sides for the merge.
    cp_count[df_col] = cp_count[df_col].astype(str).str.strip()
    gdf_join = gdf.copy()
    gdf_join[gdf_col] = gdf_join[gdf_col].astype(str).str.strip()
    gdf_join = gdf_join.merge(
        cp_count, left_on=gdf_col, right_on=df_col, how="left",
    )
    gdf_join["n_cps"] = gdf_join["n_cps"].fillna(0).astype(int)

    if len(gdf_join) < 4 or gdf_join["n_cps"].sum() == 0:
        logger.info(
            "  %s / %s: only %d regions or 0 total CPs — skipped",
            country, product, len(gdf_join),
        )
        return morans_rows, lisa_rows, join_count_rows

    # Weights — queen contiguity, row-standardised. Disconnected
    # components (e.g. islands) get a silent identity row.
    try:
        w = libpysal.weights.Queen.from_dataframe(gdf_join, use_index=False)
        w.transform = "r"
    except Exception as exc:  # noqa: BLE001
        logger.warning(
            "  %s / %s: queen weights failed (%s) — skipped",
            country, product, exc,
        )
        return morans_rows, lisa_rows, join_count_rows

    # (a) Global Moran's I on n_cps
    try:
        mi = esda.Moran(gdf_join["n_cps"].values.astype(float), w, permutations=999)
        morans_rows.append({
            "country": country, "product": product,
            "n_regions": int(w.n),
            "morans_i": float(mi.I), "expected_i": float(mi.EI),
            "z_score": float(mi.z_sim), "p_value": float(mi.p_sim),
        })
    except Exception as exc:  # noqa: BLE001
        logger.warning("  %s / %s: global Moran failed: %s", country, product, exc)

    # (b) Local Moran / LISA per region
    try:
        lm = esda.Moran_Local(
            gdf_join["n_cps"].values.astype(float), w,
            permutations=999, seed=0,
        )
        for i in range(len(gdf_join)):
            sig = lm.p_sim[i] < 0.05
            q_idx = int(lm.q[i]) if sig else 0
            quadrant = _LISA_QUADRANTS[q_idx] if 0 <= q_idx < len(_LISA_QUADRANTS) else "NS"
            lisa_rows.append({
                "country": country, "product": product,
                "region": str(gdf_join.iloc[i][gdf_col]),
                "n_cps": int(gdf_join.iloc[i]["n_cps"]),
                "local_i": float(lm.Is[i]), "p_value": float(lm.p_sim[i]),
                "quadrant": quadrant,
            })
    except Exception as exc:  # noqa: BLE001
        logger.warning("  %s / %s: LISA failed: %s", country, product, exc)

    # (c) Join-Count BB per CP year
    for cp_year in sorted(grp["cp_year"].dropna().unique()):
        cp_year = int(cp_year)
        regions_with_cp = (
            grp.loc[grp["cp_year"] == cp_year, df_col]
            .astype(str).str.strip().unique()
        )
        binary = gdf_join[gdf_col].astype(str).str.strip().isin(regions_with_cp)
        binary = binary.astype(int).values
        n_with = int(binary.sum())
        if not (2 <= n_with <= len(binary) - 2):
            continue
        try:
            jc = esda.Join_Counts(binary, w, permutations=999)
            join_count_rows.append({
                "country": country, "product": product, "cp_year": cp_year,
                "n_regions_with_cp": n_with, "n_regions_total": int(w.n),
                "bb": float(jc.bb), "bb_expected": float(jc.mean_bb),
                "z_score": float(jc.z_sim), "p_value": float(jc.p_sim_bb),
            })
        except Exception as exc:  # noqa: BLE001
            logger.warning(
                "  %s / %s / %d: Join_Counts failed: %s",
                country, product, cp_year, exc,
            )

    return morans_rows, lisa_rows, join_count_rows


def _render_summary_figure(morans_df, lisa_df, jc_df, out_path):
    """Three-panel summary figure for the run."""
    _common.init_mpl_rcparams()
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    # Left: global Moran's I per (country, crop), sorted by Z.
    ax = axes[0]
    if not morans_df.empty:
        m = morans_df.sort_values("z_score", ascending=True).tail(25)
        labels = m["country"] + " / " + m["product"]
        colors = ["#c44e52" if z < 0 else "#55a868" for z in m["z_score"]]
        ax.barh(range(len(m)), m["z_score"], color=colors, edgecolor="white")
        ax.axvline(1.96, color="gray", linestyle="--", linewidth=0.8, alpha=0.6)
        ax.axvline(-1.96, color="gray", linestyle="--", linewidth=0.8, alpha=0.6)
        ax.set_yticks(range(len(m)))
        ax.set_yticklabels(labels, fontsize=7)
        ax.set_xlabel("Moran's I Z-score (CP count per region)", fontsize=9)
        ax.set_title(f"Global spatial autocorrelation (top {len(m)})", fontsize=10)
    else:
        ax.text(0.5, 0.5, "no Moran's I rows", ha="center", va="center",
                transform=ax.transAxes)
        ax.set_axis_off()

    # Middle: top 20 BB join-count Z-scores by (country, crop, year).
    ax = axes[1]
    if not jc_df.empty:
        j = jc_df.sort_values("z_score", ascending=True).tail(20)
        labels = j["country"] + " / " + j["product"] + " " + j["cp_year"].astype(str)
        colors = ["#4c72b0" if z > 0 else "#bdbdbd" for z in j["z_score"]]
        ax.barh(range(len(j)), j["z_score"], color=colors, edgecolor="white")
        ax.axvline(1.96, color="gray", linestyle="--", linewidth=0.8, alpha=0.6)
        ax.set_yticks(range(len(j)))
        ax.set_yticklabels(labels, fontsize=7)
        ax.set_xlabel("BB Join-Count Z-score", fontsize=9)
        ax.set_title(f"Same-year CP clustering (top {len(j)})", fontsize=10)
    else:
        ax.text(0.5, 0.5, "no Join-Count rows", ha="center", va="center",
                transform=ax.transAxes)
        ax.set_axis_off()

    # Right: LISA quadrant counts pooled.
    ax = axes[2]
    if not lisa_df.empty:
        counts = lisa_df["quadrant"].value_counts().reindex(
            _LISA_QUADRANTS, fill_value=0,
        )
        colors_q = {"NS": "#bdbdbd", "HH": "#c44e52", "LL": "#4c72b0",
                    "LH": "#dd8452", "HL": "#8172b3"}
        ax.bar(counts.index, counts.values,
               color=[colors_q.get(c, "gray") for c in counts.index],
               edgecolor="white")
        for i, v in enumerate(counts.values):
            ax.text(i, v, str(int(v)), ha="center", va="bottom", fontsize=8)
        ax.set_xlabel("LISA quadrant", fontsize=9)
        ax.set_ylabel("Region count")
        ax.set_title(
            "Local cluster labels (HH=hotspot, LL=cold-spot, "
            "LH/HL=outlier, NS=not sig)",
            fontsize=9,
        )
    else:
        ax.text(0.5, 0.5, "no LISA rows", ha="center", va="center",
                transform=ax.transAxes)
        ax.set_axis_off()

    fig.suptitle(
        "BEAST changepoints — spatial co-occurrence (PySAL)",
        fontsize=12, fontweight="bold",
    )
    plt.tight_layout()
    fig.savefig(out_path, dpi=200, bbox_inches="tight")
    plt.close(fig)


def run(path_config_file):
    """Run the spatial co-occurrence analysis end-to-end."""
    cfg = load_config(path_config_file)
    parser = cfg.parser

    libpysal, esda = _try_import_pysal()
    if libpysal is None:
        return

    cps_path = cfg.output_dir / "beast_top_cps.csv"
    if not cps_path.exists():
        logger.warning(
            "beast_spatial: %s missing — run beast_runner.run() first",
            cps_path,
        )
        return

    cps = pd.read_csv(cps_path)
    if cps.empty:
        logger.info("beast_spatial: no CPs in %s — nothing to do", cps_path)
        return
    if "admin" not in cps.columns:
        # Older runs may not have the unified admin column — recompute.
        cps["admin"] = np.where(
            cps["admin_2"].astype(str) != "none",
            cps["admin_2"], cps["admin_1"],
        )

    morans_rows, lisa_rows, jc_rows = [], [], []
    gdf_cache: dict = {}
    n_pairs = cps.groupby(["country", "product"]).ngroups
    logger.info(
        "beast_spatial: %d (country, crop) pairs across %d CPs",
        n_pairs, len(cps),
    )

    for (country, product), grp in cps.groupby(["country", "product"]):
        gdf = gdf_cache.get(country)
        if gdf is None:
            gdf = _load_country_gdf(parser, country, cfg.boundary_shp)
            gdf_cache[country] = gdf
        if gdf is None or gdf.empty:
            logger.info("  %s: no boundary gdf — skipped", country)
            continue
        m_rows, l_rows, j_rows = _run_one_country_crop(
            country, product, grp, gdf, libpysal, esda,
        )
        morans_rows.extend(m_rows)
        lisa_rows.extend(l_rows)
        jc_rows.extend(j_rows)

    morans_df = pd.DataFrame(morans_rows)
    lisa_df = pd.DataFrame(lisa_rows)
    jc_df = pd.DataFrame(jc_rows)

    morans_df.to_csv(cfg.output_dir / "beast_spatial_morans.csv", index=False)
    lisa_df.to_csv(cfg.output_dir / "beast_spatial_lisa.csv", index=False)
    jc_df.to_csv(cfg.output_dir / "beast_spatial_join_counts.csv", index=False)
    logger.info(
        "beast_spatial: wrote %d Moran rows, %d LISA rows, %d Join-Count rows",
        len(morans_df), len(lisa_df), len(jc_df),
    )

    _render_summary_figure(
        morans_df, lisa_df, jc_df,
        cfg.output_dir / "fig6_spatial_summary.png",
    )
    logger.info(
        "beast_spatial: wrote fig6_spatial_summary.png → %s",
        cfg.output_dir,
    )


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("config", help="Path to geocif.txt (or list of configs)")
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    run(args.config)
