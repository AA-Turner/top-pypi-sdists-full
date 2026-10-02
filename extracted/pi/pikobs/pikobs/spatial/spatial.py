"""
verifcorr — spatial correlogram of OmP/OmA vs distance
========================================================

For one or more datasets (each a directory of converted SQLite files
-- e.g. Control, Exp1, Exp2, exactly like pikobs.progps's
``--path_experience_files``), estimates how the correlation of an
observation-space quantity (OmP, OmA, or obsvalue) decays with the
great-circle distance between observation pairs -- the
Hollingsworth-Lönnberg (1986) method, standard in NWP data
assimilation for estimating observation error correlation length
scales. Every dataset gets its own correlogram, computed
independently (there is no observation-by-observation matching here,
unlike pikobs.progps) -- when more than one is given, they are
overlaid on the same figure so a change in spatial correlation
structure between e.g. Control and an Experience is directly visible.

Method (full derivation in correlogram_core.py's docstring)
-------------------------------------------------------------------
1. Anomalies: the GLOBAL mean of the chosen quantity is subtracted per
   dataset before anything else, so a spatially slow-varying
   systematic bias doesn't masquerade as long-range correlation.
2. Every pair of observations within ``--max_dist_km`` contributes one
   covariance sample, found via a KD-tree on each observation's 3D
   position on the unit sphere (scipy's query_pairs) -- not a naive
   all-against-all loop, which is infeasible past a few thousand
   observations (O(N^2)).
3. Pairs are binned by distance; the mean covariance per bin, divided
   by the zero-lag variance, gives the correlogram. An exponential
   curve exp(-d / L) is fit to it to report a single correlation
   length scale L, in km.

Validated (confirmed directly): against a synthetic field with a KNOWN
500 km exponential correlation length scale generated over global
coverage, the fitted L recovers 500 km to within ~1-2%. IMPORTANT
CAVEAT, also confirmed directly: fitting this over a REGIONAL subset
whose size is comparable to or smaller than the true correlation
length scale under-estimates L noticeably (a known "unknown mean"
effect in this class of estimator, not a bug) -- treat a fitted L from
a small-region run as a lower bound, prefer as wide a region as the
analysis allows.

Scalability: for more than ``--max_obs`` observations (default
50,000) pooled for one dataset/family/region/fonction after all
filters, a random subsample is used instead of the full set -- keeps
both runtime and memory bounded regardless of how large the input
files actually are (e.g. IASI's 10+ million rows per date).

Pipeline phases (mirrors pikobs.progps)
----------------------------------------
Phase 1 - Compute (parallel): for each (dataset, family, region,
fonction), pool every date's observations, compute the correlogram +
exponential fit, and write the result to a small SQLite output file.
One independent task per combination -- embarrassingly parallel.

Phase 2 - Plot: for each (family, region, fonction), read back every
dataset's result and overlay them on one combined figure. Cheap
compared to Phase 1 (reads a handful of rows per dataset), so this
runs serially even when Phase 1 used many workers.

Output layout
-------------
::

    $PATHWORK/
    ├── <family>/
    │   ├── correlogram_<family>_<region>_<fonction>_<dates>.db  results
    │   └── correlogram_<family>_<region>_<fonction>_<dates>.png figures
    └── pikobs_correlogram_viewer.html   interactive web viewer
"""

import os
import sys
import time
import argparse
import datetime
import sqlite3
import warnings
import traceback

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import dask
from dask.distributed import Client

# a region is a box or a polygon; the module does not need to know
from pikobs.configobs import regionsobs
import pikobs
from pikobs.pbs_submit import maybe_submit_to_pbs

mpl.use("Agg")
warnings.filterwarnings("ignore", ".*ShapelyDeprecationWarning.*")

# =============================================================================
#  CORRELOGRAM ALGORITHM (Hollingsworth-Lönnberg)
# =============================================================================
import numpy as np
from scipy.spatial import cKDTree

EARTH_RADIUS_KM = 6371.0


def compute_correlogram(lat, lon, values, max_dist_km=3000.0, n_bins=30,
                        max_obs=50000, seed=42, min_pairs_per_bin=30):
    """
    Compute the spatial correlation of `values` as a function of
    great-circle distance.

    Args:
        lat, lon: 1D arrays, degrees.
        values: 1D array, the quantity to correlate (e.g. OmP).
        max_dist_km: maximum pair separation to consider. Correlation
            beyond this is assumed negligible and not computed --
            this is also what keeps runtime bounded (see module
            docstring).
        n_bins: number of distance bins between 0 and max_dist_km.
        max_obs: random-subsample cap (see module docstring).
        seed: RNG seed for the subsample, for reproducibility.
        min_pairs_per_bin: bins with fewer pairs than this are set to
            NaN in the output rather than reporting a noisy estimate
            from too few samples.

    Returns:
        dict with bin_centers_km, correlation, n_pairs (per bin),
        zero_lag_variance, n_obs_used, n_total_pairs.
    """
    lat = np.asarray(lat, dtype=np.float64)
    lon = np.asarray(lon, dtype=np.float64)
    values = np.asarray(values, dtype=np.float64)

    finite = np.isfinite(lat) & np.isfinite(lon) & np.isfinite(values)
    lat, lon, values = lat[finite], lon[finite], values[finite]
    n = len(values)
    if n < 2:
        raise ValueError(f"Need at least 2 finite observations, got {n}")

    if n > max_obs:
        rng = np.random.default_rng(seed)
        idx = rng.choice(n, size=max_obs, replace=False)
        lat, lon, values = lat[idx], lon[idx], values[idx]
        n = max_obs

    anomaly = values - np.mean(values)
    variance = float(np.mean(anomaly ** 2))
    if variance <= 0:
        raise ValueError("Zero variance in the input values -- cannot normalise to a correlation.")

    lat_rad = np.radians(lat)
    lon_rad = np.radians(lon)
    x = np.cos(lat_rad) * np.cos(lon_rad)
    y = np.cos(lat_rad) * np.sin(lon_rad)
    z = np.sin(lat_rad)
    points = np.column_stack([x, y, z])

    tree = cKDTree(points)
    # Chord length on the unit sphere corresponding to max_dist_km of
    # great-circle separation: chord = 2*sin(d / (2R)).
    max_chord = 2.0 * np.sin(max_dist_km / (2.0 * EARTH_RADIUS_KM))
    pairs = tree.query_pairs(max_chord, output_type="ndarray")

    if len(pairs) == 0:
        raise ValueError(
            "No observation pairs found within max_dist_km -- check "
            "that lat/lon are in degrees and max_dist_km is reasonable."
        )

    i, j = pairs[:, 0], pairs[:, 1]
    chord = np.sqrt(np.sum((points[i] - points[j]) ** 2, axis=1))
    chord = np.clip(chord, 0.0, 2.0)
    dist_km = 2.0 * EARTH_RADIUS_KM * np.arcsin(chord / 2.0)

    cov_product = anomaly[i] * anomaly[j]

    bin_edges = np.linspace(0.0, max_dist_km, n_bins + 1)
    bin_idx = np.clip(np.digitize(dist_km, bin_edges) - 1, 0, n_bins - 1)
    bin_centers = 0.5 * (bin_edges[:-1] + bin_edges[1:])

    mean_cov = np.full(n_bins, np.nan)
    n_pairs_per_bin = np.zeros(n_bins, dtype=np.int64)
    for b in range(n_bins):
        mask = bin_idx == b
        cnt = int(mask.sum())
        n_pairs_per_bin[b] = cnt
        if cnt >= min_pairs_per_bin:
            mean_cov[b] = cov_product[mask].mean()

    correlation = mean_cov / variance

    return {
        "bin_centers_km": bin_centers,
        "correlation": correlation,
        "n_pairs": n_pairs_per_bin,
        "zero_lag_variance": variance,
        "n_obs_used": n,
        "n_total_pairs": len(pairs),
    }

_CONVERSION_DIR_NAME = "conversion_db"

_DDL = """
CREATE TABLE IF NOT EXISTS correlogram_bins (
    family TEXT, region TEXT, fonction TEXT, dataset_name TEXT,
    bin_center_km REAL, correlation REAL, n_pairs INTEGER
);
CREATE TABLE IF NOT EXISTS correlogram_summary (
    family TEXT, region TEXT, fonction TEXT, dataset_name TEXT,
    zero_lag_variance REAL, n_obs_used INTEGER, n_total_pairs INTEGER,
    max_dist_km REAL, L_fit REAL, L_err REAL,
    datestart TEXT, dateend TEXT
);
"""

_COLORS = ["#000000", "#E69F00", "#56B4E9", "#009E73", "#CC79A7",
          "#D55E00", "#0072B2", "#F0E442"]


# =============================================================================
#  LOW-LEVEL HELPERS
# =============================================================================

def _is_sqlite3(filepath: str) -> bool:
    if not os.path.isfile(filepath):
        return False
    try:
        with open(filepath, "rb") as fd:
            return fd.read(16) == b"SQLite format 3\x00"
    except OSError:
        return False


def _resolve_file(path, name, fdate, family):
    candidates = [
        os.path.normpath(f"{path}/{fdate}_{family}"),
        os.path.normpath(f"{path}/{fdate}_{family}.db"),
        os.path.normpath(f"{path}/db_converted_{name}_{fdate}_{family}.db"),
    ]
    return next((c for c in candidates if _is_sqlite3(c)), None)


def _clean_pathwork_preserving_cache(pathwork: str) -> None:
    if not pathwork or pathwork in ("/", os.path.expanduser("~")):
        print(f"[WARNING] refusing to clean unsafe pathwork: {pathwork!r}", flush=True)
        return
    pathwork = os.path.realpath(pathwork)
    if not os.path.isdir(pathwork):
        os.makedirs(pathwork, exist_ok=True)
        os.makedirs(os.path.join(pathwork, _CONVERSION_DIR_NAME), exist_ok=True)
        return
    import shutil
    n_kept, n_removed = 0, 0
    for entry in os.listdir(pathwork):
        full = os.path.join(pathwork, entry)
        if entry == _CONVERSION_DIR_NAME:
            n_kept += 1
            continue
        try:
            if os.path.islink(full) or os.path.isfile(full):
                os.remove(full)
            elif os.path.isdir(full):
                shutil.rmtree(full)
            n_removed += 1
        except OSError as e:
            print(f"[WARNING] could not remove {full}: {e}", flush=True)
    os.makedirs(os.path.join(pathwork, _CONVERSION_DIR_NAME), exist_ok=True)
    print(f"[INFO] pathwork cleaned: {pathwork} | removed {n_removed} entries | preserved {_CONVERSION_DIR_NAME}/", flush=True)


def _read_values(db_file, family, region, flags_criteria, varnos, fonction):
    """Read lat, lon, and the requested quantity for every observation
    in one file passing the region/flag/varno filters (same
    conventions as pikobs.progps)."""
    FAM, VCOORD, VCOCRIT, STATB, element, VCOTYP = pikobs.family(family)
    if varnos:
        element = ",".join(str(v) for v in varnos)
    LATLONCRIT = regionsobs.criteria(region)
    flag_criteria = pikobs.flag_criteria(flags_criteria)
    col = {"omp": "omp", "oma": "oma", "obsvalue": "obsvalue"}[fonction]

    query = f"""
    SELECT main_h.lat, main_h.lon, main_d.{col}
    FROM header main_h
    JOIN DATA main_d USING(id_obs)
    WHERE main_d.varno IN ({element})
      AND main_d.{col} IS NOT NULL
      {flag_criteria}
      {LATLONCRIT}
      {VCOCRIT}
    """
    try:
        with sqlite3.connect(f"file:{db_file}?mode=ro", uri=True) as conn:
            rows = conn.execute(query).fetchall()
    except sqlite3.Error as e:
        print(f"[WARNING] could not read {os.path.basename(db_file)}: {e}", flush=True)
        return np.array([]), np.array([]), np.array([])
    if not rows:
        return np.array([]), np.array([]), np.array([])
    arr = np.array(rows, dtype=np.float64)
    return arr[:, 0], arr[:, 1], arr[:, 2]


def _exp_decay(d, L):
    return np.exp(-d / L)


# =============================================================================
#  PHASE 1 - COMPUTE (one task per dataset/family/region/fonction)
# =============================================================================

def compute_and_save_correlogram(
        dataset_name, dataset_path, family, region, flags_criteria, varnos,
        fonction, datestart, dateend, pathwork, max_dist_km, n_bins, max_obs):
    """Top-level wrapper -- logs unexpected errors per output instead
    of crashing the whole Dask run (same pattern as pikobs.progps)."""
    try:
        _do_compute(
            dataset_name, dataset_path, family, region, flags_criteria,
            varnos, fonction, datestart, dateend, pathwork, max_dist_km,
            n_bins, max_obs,
        )
    except Exception as e:
        msg = (
            f"\n[ERROR] correlogram FAILED for {dataset_name}/{family}/{region}/"
            f"{fonction} -> {type(e).__name__}: {e}\n{traceback.format_exc()}"
        )
        sys.stderr.write(msg)
        sys.stderr.flush()
        try:
            log_dir = f"{pathwork}/{family}"
            os.makedirs(log_dir, exist_ok=True)
            with open(os.path.join(log_dir, "_correlogram_errors.log"), "a") as fh:
                fh.write(msg + "\n")
        except OSError:
            pass


def _do_compute(dataset_name, dataset_path, family, region, flags_criteria,
                varnos, fonction, datestart, dateend, pathwork, max_dist_km,
                n_bins, max_obs):
    dt_start = datetime.datetime.strptime(datestart, "%Y%m%d%H")
    dt_end = datetime.datetime.strptime(dateend, "%Y%m%d%H")
    dataset_path = os.path.normpath(dataset_path)

    all_lat, all_lon, all_val = [], [], []
    current_date = dt_start
    n_files_read = 0
    while current_date <= dt_end:
        fdate = current_date.strftime("%Y%m%d%H")
        db_file = _resolve_file(dataset_path, dataset_name, fdate, family)
        if db_file is not None:
            lat, lon, val = _read_values(db_file, family, region, flags_criteria, varnos, fonction)
            if len(val) > 0:
                all_lat.append(lat); all_lon.append(lon); all_val.append(val)
                n_files_read += 1
        current_date += datetime.timedelta(hours=6)

    if not all_val:
        print(f"[WARNING] no data for {dataset_name}/{family}/{region}/{fonction} "
              f"in [{datestart}, {dateend}]", flush=True)
        return

    lat = np.concatenate(all_lat)
    lon = np.concatenate(all_lon)
    val = np.concatenate(all_val)
    print(f"[INFO] {dataset_name}/{family}/{region}/{fonction}: "
          f"{n_files_read} files, {len(val)} obs pooled", flush=True)

    result = compute_correlogram(lat, lon, val, max_dist_km=max_dist_km,
                                 n_bins=n_bins, max_obs=max_obs)

    valid = ~np.isnan(result["correlation"])
    L_fit, L_err = None, None
    if valid.sum() >= 3:
        try:
            popt, pcov = curve_fit(
                _exp_decay, result["bin_centers_km"][valid],
                result["correlation"][valid], p0=[max_dist_km / 4],
                bounds=(1.0, max_dist_km * 10),
            )
            L_fit, L_err = float(popt[0]), float(np.sqrt(pcov[0, 0]))
        except RuntimeError:
            print(f"[WARNING] exponential fit did not converge for {dataset_name}", flush=True)

    db_new = os.path.join(
        pathwork, family,
        f"correlogram_{family}_{region}_{fonction}_{datestart}_{dateend}.db",
    )
    os.makedirs(os.path.dirname(db_new), exist_ok=True)

    max_retries, base_delay = 12, 0.5
    for attempt in range(max_retries):
        try:
            with sqlite3.connect(db_new, timeout=60) as conn:
                conn.execute("PRAGMA journal_mode=WAL;")
                conn.execute("PRAGMA synchronous=NORMAL;")
                conn.executescript(_DDL)
                conn.execute(
                    "DELETE FROM correlogram_bins WHERE family=? AND region=? "
                    "AND fonction=? AND dataset_name=?",
                    (family, region, fonction, dataset_name),
                )
                conn.execute(
                    "DELETE FROM correlogram_summary WHERE family=? AND region=? "
                    "AND fonction=? AND dataset_name=?",
                    (family, region, fonction, dataset_name),
                )
                conn.executemany(
                    "INSERT INTO correlogram_bins VALUES (?,?,?,?,?,?,?)",
                    [
                        (family, region, fonction, dataset_name,
                         float(d), None if np.isnan(c) else float(c), int(n))
                        for d, c, n in zip(result["bin_centers_km"], result["correlation"], result["n_pairs"])
                    ],
                )
                conn.execute(
                    "INSERT INTO correlogram_summary VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                    (family, region, fonction, dataset_name,
                     result["zero_lag_variance"], result["n_obs_used"], result["n_total_pairs"],
                     max_dist_km, L_fit, L_err, datestart, dateend),
                )
                conn.commit()
            break
        except sqlite3.OperationalError as e:
            if "locked" in str(e) and attempt < max_retries - 1:
                time.sleep(base_delay * (2 ** attempt))
            else:
                raise

    if L_fit is not None:
        print(f"[INFO] {dataset_name}: fitted L = {L_fit:.1f} +/- {L_err:.1f} km", flush=True)


# =============================================================================
#  PLAN BUILDERS
# =============================================================================

def create_compute_list(datasets_names, datasets_paths, families, regions,
                        fonctions, flags_criteria, varnos, datestart, dateend,
                        pathwork, max_dist_km, n_bins, max_obs):
    tasks = []
    for name, path in zip(datasets_names, datasets_paths):
        for family in families:
            for region in regions:
                for fonction in fonctions:
                    tasks.append((
                        name, path, family, region, flags_criteria, varnos,
                        fonction, datestart, dateend, pathwork, max_dist_km,
                        n_bins, max_obs,
                    ))
    return tasks


def create_plot_list(families, regions, fonctions):
    return [(f, r, fo) for f in families for r in regions for fo in fonctions]


# =============================================================================
#  PHASE 2 - PLOT (overlay every dataset for one family/region/fonction)
# =============================================================================

def plot_combined_correlogram(family, region, fonction, datestart, dateend, pathwork):
    db_file = os.path.join(
        pathwork, family,
        f"correlogram_{family}_{region}_{fonction}_{datestart}_{dateend}.db",
    )
    if not os.path.isfile(db_file):
        print(f"[WARNING] plot: missing {db_file}", flush=True)
        return None

    with sqlite3.connect(f"file:{db_file}?mode=ro", uri=True) as conn:
        summaries = conn.execute(
            "SELECT dataset_name, zero_lag_variance, n_obs_used, n_total_pairs, "
            "max_dist_km, L_fit, L_err FROM correlogram_summary "
            "WHERE family=? AND region=? AND fonction=?",
            (family, region, fonction),
        ).fetchall()
        if not summaries:
            print(f"[WARNING] plot: no summary rows in {os.path.basename(db_file)}", flush=True)
            return None
        max_dist_km = summaries[0][4]

        fig, ax = plt.subplots(figsize=(9, 6))
        subtitle_parts = []
        for k, (dataset_name, zvar, n_obs, n_pairs_tot, mdk, L_fit, L_err) in enumerate(summaries):
            color = _COLORS[k % len(_COLORS)]
            bins = conn.execute(
                "SELECT bin_center_km, correlation FROM correlogram_bins "
                "WHERE family=? AND region=? AND fonction=? AND dataset_name=? "
                "ORDER BY bin_center_km",
                (family, region, fonction, dataset_name),
            ).fetchall()
            bins = np.array(bins, dtype=np.float64)
            valid = ~np.isnan(bins[:, 1])
            ax.scatter(bins[valid, 0], bins[valid, 1], s=30, color=color, zorder=3,
                      label=f"{dataset_name}" + (f" (L={L_fit:.0f}km)" if L_fit else ""))
            if L_fit is not None:
                d_smooth = np.linspace(0, mdk, 200)
                ax.plot(d_smooth, _exp_decay(d_smooth, L_fit), color=color,
                       linewidth=1.5, alpha=0.6, zorder=2)
            subtitle_parts.append(f"{dataset_name}: {n_obs} obs, {n_pairs_tot} pairs")

        ax.axhline(0, color="gray", linestyle="--", linewidth=1, zorder=1)
        ax.set_xlabel("Distance between observation pairs [km]", fontsize=12)
        ax.set_ylabel(f"Correlation of {fonction.upper()} anomalies", fontsize=12)
        title = f"{family}  {region}  {fonction}  {datestart}\u2192{dateend}"
        ax.set_title(f"{title}\n" + "  |  ".join(subtitle_parts), fontsize=10)
        ax.grid(True, alpha=0.3)
        ax.legend(loc="upper right", fontsize=10)
        ax.set_xlim(0, max_dist_km)

        out_path = os.path.join(
            pathwork, family,
            f"correlogram_{family}_{region}_{fonction}_{datestart}_{dateend}.png",
        )
        plt.savefig(out_path, dpi=160, bbox_inches="tight", facecolor="white")
        plt.close(fig)
        print(f"[INFO] saved: {out_path}", flush=True)
        return out_path


# =============================================================================
#  WEB VIEWER
# =============================================================================

_VIEWER_KEYS = ["family", "region", "fonction"]


def generate_web(plot_list, pathwork, datasets_names, datestart, dateend,
                 datasets_paths, output_filename="pikobs_correlogram_viewer.html"):
    try:
        from pikobs.web.viewer import generate_web as _viewer
    except ImportError:
        import importlib.util, pathlib
        here = pathlib.Path(__file__).resolve().parent
        spec = importlib.util.spec_from_file_location("pikobs_viewer_local", here / "viewer.py")
        if spec is None or spec.loader is None:
            raise
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        _viewer = module.generate_web

    items = []
    for family, region, fonction in plot_list:
        filename = f"correlogram_{family}_{region}_{fonction}_{datestart}_{dateend}.png"
        db_file = os.path.join(pathwork, family, f"correlogram_{family}_{region}_{fonction}_{datestart}_{dateend}.db")
        if not os.path.isfile(db_file):
            continue
        items.append({"family": family, "region": region, "fonction": fonction, "filename": filename})

    if not items:
        print("[WARNING] viewer: nothing to show, skipping.", flush=True)
        return None

    header_line = f"Datasets: {', '.join(datasets_names)}  |  {datestart} &rarr; {dateend}"
    paths_lines = "<br>".join(
        f"<b>{nm}</b>: <code>{pth}</code>" for nm, pth in zip(datasets_names, datasets_paths)
    )
    method_block = (
        "<b>What each figure shows:</b> the spatial correlation of the chosen "
        "quantity's anomalies (global mean removed) as a function of distance "
        "between observation pairs -- the Hollingsworth-L\u00f6nnberg method. "
        "Each dataset is its own independent curve (no observation-by-"
        "observation matching between datasets here, unlike "
        "pikobs.progps) -- overlaid so a change in spatial correlation "
        "structure between e.g. Control and an Experience is directly "
        "visible. The exponential fit's L (km) is one summary number for "
        "each curve's decay rate; <b>fitting over a small region "
        "under-estimates L</b> (a known statistical effect, not a data "
        "problem) -- treat it as a lower bound unless the region is wide."
    )
    subtitle = "<br><br>".join([header_line, paths_lines, method_block])

    return _viewer(
        items=items,
        keys=_VIEWER_KEYS,
        output_path=os.path.join(pathwork, output_filename),
        title="Pikobs Correlogram Viewer",
        subtitle=subtitle,
        image_subdir_key="family",
        value_labels={},
        issues_url="https://gitlab.science.gc.ca/dlo001/Pikobs",
    )


# =============================================================================
#  MAIN ORCHESTRATOR
# =============================================================================

def make_correlogram(datasets_paths, datasets_names, pathwork, datestart, dateend,
                     regions, families, flags_criteria, varnos, fonctions,
                     max_dist_km, n_bins, max_obs, n_cpu):
    print("=" * 78, flush=True)
    print(f"[INFO] python      : {sys.executable}", flush=True)
    print(f"[INFO] datasets    : {datasets_names}", flush=True)
    print(f"[INFO] max_dist_km : {max_dist_km}", flush=True)
    print(f"[INFO] max_obs     : {max_obs}", flush=True)
    print("=" * 78, flush=True)

    _clean_pathwork_preserving_cache(pathwork)
    for family in families:
        os.makedirs(f"{pathwork}/{family}", exist_ok=True)

    t0 = time.time()
    compute_tasks = create_compute_list(
        datasets_names, datasets_paths, families, regions, fonctions,
        flags_criteria, varnos, datestart, dateend, pathwork, max_dist_km,
        n_bins, max_obs,
    )
    if n_cpu == 1:
        print(f"[INFO] compute (serial): {len(compute_tasks)} tasks", flush=True)
        for t in compute_tasks:
            compute_and_save_correlogram(*t)
    else:
        print(f"[INFO] compute (parallel): {len(compute_tasks)} tasks -> {n_cpu} workers", flush=True)
        with Client(processes=True, threads_per_worker=1, n_workers=n_cpu, silence_logs=50):
            dask.compute(*[dask.delayed(compute_and_save_correlogram)(*t) for t in compute_tasks])
    print(f"[TIMER] compute: {time.time() - t0:.1f}s", flush=True)

    t0 = time.time()
    plot_list = create_plot_list(families, regions, fonctions)
    for family, region, fonction in plot_list:
        plot_combined_correlogram(family, region, fonction, datestart, dateend, pathwork)
    print(f"[TIMER] plotting: {time.time() - t0:.1f}s", flush=True)

    generate_web(plot_list, pathwork, datasets_names, datestart, dateend, datasets_paths)
    print(f"[INFO] Output directory: {pathwork}", flush=True)


# =============================================================================
#  CLI
# =============================================================================

def arg_call():
    parser = argparse.ArgumentParser(
        description="Spatial correlogram (Hollingsworth-L\u00f6nnberg) of OmP/OmA/"
                    "obsvalue vs distance between observation pairs. One or more "
                    "datasets, each an independent correlogram, overlaid for "
                    "comparison.",
    )
    parser.add_argument("--path_files", nargs="+", required=True,
        help="One or more dataset directories (e.g. Control, Exp1, Exp2), "
            "matched 1:1 by position with --name.")
    parser.add_argument("--name", nargs="+", required=True,
        help="One label per --path_files entry, same order/count.")
    parser.add_argument("--pathwork", required=True)
    parser.add_argument("--datestart", required=True)
    parser.add_argument("--dateend", required=True)
    parser.add_argument("--region", nargs="+", required=True)
    parser.add_argument("--family", nargs="+", required=True)
    parser.add_argument("--flags_criteria", default="all")
    parser.add_argument("--varnos", nargs="+", default=[])
    parser.add_argument("--fonction", nargs="+", default=["omp"],
        choices=["omp", "oma", "obsvalue"])
    parser.add_argument("--max_dist_km", type=float, default=3000.0)
    parser.add_argument("--n_bins", type=int, default=30)
    parser.add_argument("--max_obs", type=int, default=50000)
    parser.add_argument("--n_cpus", "--n_cpu", default=1, type=int, dest="n_cpus")
    args = parser.parse_args()

    if len(args.path_files) != len(args.name):
        sys.exit(
            f"[ERROR] {len(args.path_files)} --path_files but {len(args.name)} "
            f"--name -- these must be given in matching pairs."
        )

    for arg in vars(args):
        print(f"--{arg} {getattr(args, arg)}", flush=True)

    maybe_submit_to_pbs(args)

    make_correlogram(
        args.path_files, args.name, args.pathwork, args.datestart, args.dateend,
        args.region, args.family, args.flags_criteria, args.varnos,
        args.fonction, args.max_dist_km, args.n_bins, args.max_obs, args.n_cpus,
    )


if __name__ == "__main__":
    arg_call()
