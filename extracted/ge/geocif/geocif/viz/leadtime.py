"""Lead-time skill curves: when do EO-driven models overtake the baselines?

A ``run_time_steps = all`` run scores every cumulative stage of the season, so
skill can be read as a function of how much of the season has been observed.
This module turns that into the one view the per-model progression plots in
``yield_outlook._plot_all_progressions`` cannot give: every model on one axis,
with the ``trend`` and ``null`` baselines as horizontal references. The
**crossing point** — the earliest forecast date at which an ML model beats a
baseline — gets its own clearly-labelled figure via :func:`plot_crossings`,
rather than being encoded a second time on the metric curves.

Stage semantics (the part that is easy to get backwards): under ``monthly_r``
the stages are REVERSE-cumulative. In a ``Stage Name`` like ``"Aug 1-Mar 31"``
the FIRST month is the data cutoff and the second is the earliest (planting)
month, i.e. the window is really Mar 1 - Aug 31. The DB spells this out in its
own ``Stage Window Display`` column (``"Mar 1-Aug 31"``) and ``Prediction
Month`` (``Aug``); see ``geocif/ml/stages.py:343-362`` and
``geocif/cid/indices.py:1671-1676``. So ``"Apr 1-Mar 31"`` is the NARROWEST
window, not a 12-month one. The x-axis here is the as-of month, never the raw
range string, because the range reads as a span and invites that misreading.

The ``trend`` and ``null`` baselines consume no EO features, so their score is
identical at every stage (verified: spread 0.00000 on a common sample). They
are therefore drawn as horizontal lines rather than curves.

Usage:
    python -m geocif.viz.leadtime --db <outlook.db> --out <dir>
"""

import argparse
import sqlite3
import sys
from pathlib import Path

import numpy as np
import pandas as pd

OBS = "Observed Yield (tn per ha)"
PRED = "Predicted Yield (tn per ha)"

# Baselines fit on absolute yield with no EO input -> flat across stages.
BASELINES = ("trend", "null")
# Drawn as curves, in a fixed order so colors are stable across figures.
ML_ORDER = ("tabpfn", "cubist", "catboost")

_MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
           "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
_MONTH_NUM = {m: i + 1 for i, m in enumerate(_MONTHS)}

# CVD-safe, distinguishable in grayscale by marker as well as hue.
COLORS = {"tabpfn": "#1f4e79", "cubist": "#c1666b", "catboost": "#3f8f5b"}
MARKERS = {"tabpfn": "o", "cubist": "s", "catboost": "^"}
BASE_STYLE = {"trend": ("#7a6a9b", (0, (6, 3))), "null": ("#8a8a8a", (0, (2, 2)))}

METRICS = [
    ("rmse", "RMSE", "RMSE ({units})", False),
    ("mape", "MAPE", "MAPE (%)", False),
    ("r2", "R2", "R$^2$", True),
]


def style_ctx():
    """scienceplots when available, plain matplotlib otherwise."""
    import matplotlib.pyplot as plt

    try:
        import scienceplots  # noqa: F401
        return plt.style.context(["science", "no-latex"])
    except Exception:
        return plt.style.context("default")


def _asof_month(stage_name, swd):
    """As-of (data cutoff) month number for a stage.

    Prefers ``Stage Window Display`` (already calendar-ordered, so its LATER
    endpoint is the cutoff); falls back to the first token of ``Stage Name``,
    which is the cutoff under the reverse-cumulative convention.
    """
    if isinstance(swd, str) and "-" in swd:
        right = swd.split("-", 1)[1].strip()[:3].title()
        if right in _MONTH_NUM:
            return _MONTH_NUM[right]
    if isinstance(stage_name, str):
        left = stage_name.split("-", 1)[0].strip()[:3].title()
        if left in _MONTH_NUM:
            return _MONTH_NUM[left]
    return None


def load(db_path, table):
    """Read one crop table, keeping only the outlook experiment."""
    cols = ['"Model"', '"Region"', '"Harvest Year"', '"Stage Name"', f'"{PRED}"', f'"{OBS}"']
    con = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    try:
        present = pd.read_sql(f'PRAGMA table_info("{table}")', con)["name"].tolist()
        for opt in ("Stage Window Display", "Area (ha)"):
            if opt in present:
                cols.append(f'"{opt}"')
        df = pd.read_sql(
            f'SELECT {",".join(cols)} FROM "{table}" '
            f"WHERE \"Experiment Name\" = 'outlook'", con
        )
    finally:
        con.close()
    if "Stage Window Display" not in df.columns:
        df["Stage Window Display"] = np.nan
    df = df.rename(columns={"Harvest Year": "year", "Stage Name": "stage",
                            "Stage Window Display": "swd"})
    df["year"] = pd.to_numeric(df["year"], errors="coerce").astype("Int64")
    for c in (OBS, PRED, "Area (ha)"):
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    df = df.dropna(subset=[OBS, PRED, "year"])
    return df[df[OBS] > 0].copy()


def prepare(df, min_region_frac=0.5):
    """Drop unrepresentative stages and restrict to a common sample.

    A stage covering only a small minority of regions (e.g. maize
    ``Mar 1-Mar 31``, which exists solely because Missouri's calendar starts in
    March) is not comparable with the rest — its score describes a different
    pool of states, not an earlier forecast. Those stages are removed, then the
    frame is restricted to the (region, year) pairs present in EVERY surviving
    stage so all curves and both baselines are scored on identical rows.
    """
    n_regions = df["Region"].nunique()
    per_stage = df.groupby("stage")["Region"].nunique()
    keep = per_stage[per_stage >= min_region_frac * n_regions].index.tolist()
    dropped = {s: int(per_stage[s]) for s in per_stage.index if s not in keep}
    df = df[df["stage"].isin(keep)].copy()

    df["asof"] = [_asof_month(s, w) for s, w in zip(df["stage"], df["swd"])]
    df = df.dropna(subset=["asof"])
    df["asof"] = df["asof"].astype(int)

    # common (region, year) sample across stages, using any single model
    probe = df[df["Model"] == df["Model"].iloc[0]]
    piv = probe.pivot_table(index=["Region", "year"], columns="stage",
                            values=PRED, aggfunc="first")
    common = piv.dropna().index
    if len(common):
        df = df.set_index(["Region", "year"]).loc[common].reset_index()
    return df, dropped, len(common)


def _metrics(obs, pred):
    from sklearn.metrics import r2_score

    obs = np.asarray(obs, dtype=float)
    pred = np.asarray(pred, dtype=float)
    rmse = float(np.sqrt(np.mean((pred - obs) ** 2)))
    mape = float(np.mean(np.abs(pred - obs) / obs) * 100)
    r2 = float(r2_score(obs, pred)) if len(obs) > 1 and len(set(obs)) > 1 else np.nan
    return rmse, mape, r2


def score(df, national=False):
    """Metric table: one row per (stage, model).

    ``national=False`` pools every region-year at a stage. ``national=True``
    first collapses regions to one area-weighted national yield per year (the
    identity a national forecast is actually judged on), then scores across
    years. Falls back to an unweighted mean where ``Area (ha)`` is missing.
    """
    rows = []
    for (stage, asof, model), g in df.groupby(["stage", "asof", "Model"]):
        if national:
            recs = []
            for yr, gy in g.groupby("year"):
                w = gy["Area (ha)"] if "Area (ha)" in gy.columns else None
                if w is None or w.isna().all() or float(w.sum()) <= 0:
                    recs.append((gy[OBS].mean(), gy[PRED].mean()))
                else:
                    w = w.fillna(0.0)
                    recs.append((np.average(gy[OBS], weights=w),
                                 np.average(gy[PRED], weights=w)))
            if len(recs) < 3:
                continue
            obs, pred = zip(*recs)
            n = len(recs)
        else:
            obs, pred = g[OBS].values, g[PRED].values
            n = len(g)
        rmse, mape, r2 = _metrics(obs, pred)
        rows.append({"stage": stage, "asof": asof, "asof_month": _MONTHS[asof - 1],
                     "Model": model, "RMSE": rmse, "MAPE": mape, "R2": r2, "n": n})
    out = pd.DataFrame(rows)
    return out.sort_values(["asof", "Model"]).reset_index(drop=True)


def _crossings(sub, metric, base_val, higher_better):
    """First as-of month at which a model's curve passes a baseline."""
    sub = sub.sort_values("asof")
    for _, r in sub.iterrows():
        v = r[metric]
        if pd.isna(v):
            continue
        if (higher_better and v > base_val) or (not higher_better and v < base_val):
            return int(r["asof"])
    return None


def plot_metric(tab, metric, ylabel, higher_better, title, out_stem, units="Mg/ha"):
    """One figure: ML curves vs as-of month, baselines as horizontal lines."""
    import matplotlib.pyplot as plt

    ml = [m for m in ML_ORDER if m in set(tab["Model"])]
    if not ml:
        return None
    base_vals = {}
    for b in BASELINES:
        s = tab[tab["Model"] == b][metric].dropna()
        if len(s):
            base_vals[b] = float(s.median())   # flat by construction

    xs_all = sorted(tab["asof"].unique())
    with style_ctx():
        fig, ax = plt.subplots(figsize=(7.0, 4.4))

        for b, val in base_vals.items():
            color, dash = BASE_STYLE[b]
            ax.axhline(val, color=color, linestyle=dash, linewidth=1.3, zorder=1)
            ax.annotate(f"{b}  {val:.3f}", xy=(1.0, val),
                        xycoords=ax.get_yaxis_transform(),
                        xytext=(4, 0), textcoords="offset points",
                        va="center", ha="left", fontsize=8.5, color=color)

        for m in ml:
            sub = tab[tab["Model"] == m].sort_values("asof")
            ax.plot(sub["asof"], sub[metric], marker=MARKERS[m], ms=5, lw=1.7,
                    color=COLORS[m], label=m, zorder=3)

        # Crossing months are deliberately NOT marked here. An earlier version
        # drew a coloured tick on each baseline at the crossing, but the glyph
        # had no legend entry and so was undiscoverable. That information now
        # lives in one clearly-labelled place: plot_crossings().
        ax.set_xticks(xs_all)
        ax.set_xticklabels([_MONTHS[x - 1] for x in xs_all], fontsize=9)
        ax.set_xlabel("Forecast issue month (EO data through end of month)", fontsize=10)
        ax.set_ylabel(ylabel.format(units=units), fontsize=10)
        ax.tick_params(labelsize=9)
        ax.grid(True, linestyle=":", alpha=0.4)
        ax.spines[["top", "right"]].set_visible(False)
        # scienceplots turns ticks on all four sides; with the top/right spines
        # hidden those become orphaned dashes floating at the plot edge.
        ax.tick_params(which="both", top=False, right=False)
        ax.legend(frameon=False, fontsize=9,
                  loc="lower right" if higher_better else "upper right")
        ax.set_title(title, fontsize=10.5, loc="left")
        # leave room for the right-edge baseline labels
        fig.subplots_adjust(right=0.82)

        out_stem = Path(out_stem)
        out_stem.parent.mkdir(parents=True, exist_ok=True)
        for ext in ("png", "pdf"):
            fig.savefig(out_stem.with_suffix(f".{ext}"), dpi=300, bbox_inches="tight")
        plt.close(fig)
    return out_stem.with_suffix(".png")


def crossing_table(tab, crop):
    """When does each model first beat each baseline, per metric?

    Returns one row per (crop, model, baseline) with the crossing as-of month
    for R2 (the headline) plus the min/max across all three metrics, so a
    metric disagreement is visible instead of hidden behind one number.
    """
    rows = []
    ml = [m for m in ML_ORDER if m in set(tab["Model"])]
    for b in BASELINES:
        bt = tab[tab["Model"] == b]
        if bt.empty:
            continue
        for m in ml:
            sub = tab[tab["Model"] == m]
            per_metric = {}
            for col, hb in (("R2", True), ("RMSE", False), ("MAPE", False)):
                s = bt[col].dropna()
                if not len(s):
                    continue
                per_metric[col] = _crossings(sub, col, float(s.median()), hb)
            got = [v for v in per_metric.values() if v is not None]
            rows.append({
                "crop": crop, "Model": m, "baseline": b,
                "cross_r2": per_metric.get("R2"),
                "cross_rmse": per_metric.get("RMSE"),
                "cross_mape": per_metric.get("MAPE"),
                "cross_min": min(got) if got else None,
                "cross_max": max(got) if got else None,
                "n_metrics_crossing": len(got),
            })
    return pd.DataFrame(rows)


def plot_crossings(cross, out_stem, agg):
    """Dumbbell chart: months at which each model overtakes null, then trend.

    One row per (crop, model). The bar spans null-crossing to trend-crossing —
    its length is the extra season needed to beat the harder baseline. Marker
    position is the R2 crossing; a thin whisker shows the spread across
    RMSE/MAPE/R2 when the metrics disagree. Models that never cross are drawn
    at the right margin and labelled.
    """
    import matplotlib.pyplot as plt

    cross = cross.dropna(subset=["cross_min"], how="all")
    if cross.empty:
        return None
    crops = sorted(cross["crop"].unique())
    months = [v for v in cross[["cross_min", "cross_max"]].stack().dropna().unique()]
    if not months:
        return None
    lo, hi = int(min(months)), int(max(months))

    rows = []
    for crop in crops:
        for m in ML_ORDER:
            sel = cross[(cross["crop"] == crop) & (cross["Model"] == m)]
            if not sel.empty:
                rows.append((crop, m))
    if not rows:
        return None

    any_never = False
    with style_ctx():
        fig, ax = plt.subplots(figsize=(7.4, 0.46 * len(rows) + 1.5))
        ytick, ylab = [], []
        for i, (crop, m) in enumerate(rows):
            y = len(rows) - 1 - i
            ytick.append(y)
            ylab.append(f"{crop} · {m}")
            vals = {}
            for b in BASELINES:
                r = cross[(cross["crop"] == crop) & (cross["Model"] == m)
                          & (cross["baseline"] == b)]
                if r.empty:
                    continue
                r = r.iloc[0]
                vals[b] = (r["cross_r2"], r["cross_min"], r["cross_max"])
            pts = {b: v[0] for b, v in vals.items() if v[0] is not None}
            if len(pts) == 2 and pts["null"] != pts["trend"]:
                ax.plot([pts["null"], pts["trend"]], [y, y], color="#bcc4cf",
                        lw=2.6, solid_capstyle="round", zorder=1)

            coincident = (len(pts) == 2 and pts["null"] == pts["trend"])
            if coincident:
                # both baselines fall in the same month — one split marker
                # (left half = null, right half = trend) instead of two
                # markers hiding each other.
                ax.plot([pts["null"]], [y], marker=MARKERS[m], ms=8.5,
                        fillstyle="right", color=BASE_STYLE["trend"][0],
                        markerfacecoloralt=BASE_STYLE["null"][0],
                        markeredgecolor="white", markeredgewidth=0.8, zorder=3)
            for b, (c_r2, c_lo, c_hi) in vals.items():
                color = BASE_STYLE[b][0]
                if c_r2 is None:
                    any_never = True
                    ax.annotate(f"never beats {b}", xy=(hi + 0.3, y),
                                va="center", ha="left", fontsize=8, color=color)
                    continue
                if c_lo is not None and c_hi is not None and c_hi > c_lo:
                    ax.plot([c_lo, c_hi], [y, y], color=color, lw=1.0,
                            alpha=0.55, zorder=2)
                if not coincident:
                    ax.plot([c_r2], [y], marker=MARKERS[m], ms=7.5, color=color,
                            markeredgecolor="white", markeredgewidth=0.8, zorder=3)

        ax.set_yticks(ytick)
        ax.set_yticklabels(ylab, fontsize=9)
        ax.set_ylim(-0.6, len(rows) - 0.4)
        ax.set_yticks([], minor=True)
        ax.set_xticks(list(range(lo, hi + 1)))
        ax.set_xticks([], minor=True)
        ax.set_xticklabels([_MONTHS[x - 1] for x in range(lo, hi + 1)], fontsize=9)
        ax.set_xlim(lo - 0.45, hi + (1.7 if any_never else 0.45))
        ax.set_xlabel("First forecast issue month beating the baseline "
                      "(EO data through end of month)", fontsize=10)
        ax.grid(True, axis="x", linestyle=":", alpha=0.45)
        ax.spines[["top", "right", "left"]].set_visible(False)
        ax.tick_params(axis="y", length=0)
        # see note in plot_metric: kill the all-four-sides ticks scienceplots adds
        ax.tick_params(which="both", top=False, right=False)

        handles = [
            plt.Line2D([], [], marker="o", ls="none", color=BASE_STYLE["null"][0],
                       ms=8, markeredgecolor="white", label="beats null"),
            plt.Line2D([], [], marker="o", ls="none", color=BASE_STYLE["trend"][0],
                       ms=8, markeredgecolor="white", label="beats trend"),
        ]
        ax.legend(handles=handles, frameon=False, fontsize=9, ncol=2,
                  loc="upper center", bbox_to_anchor=(0.5, -0.22))
        ax.set_title(f"Crossing months — {agg} aggregation", fontsize=10.5, loc="left")

        out_stem = Path(out_stem)
        out_stem.parent.mkdir(parents=True, exist_ok=True)
        for ext in ("png", "pdf"):
            fig.savefig(out_stem.with_suffix(f".{ext}"), dpi=300, bbox_inches="tight")
        plt.close(fig)
    return out_stem.with_suffix(".png")


def run(db, out_dir, tables=None, units="Mg/ha"):
    out_dir = Path(out_dir)
    con = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
    all_tabs = pd.read_sql(
        "SELECT name FROM sqlite_master WHERE type='table'", con)["name"].tolist()
    con.close()
    tables = tables or [t for t in all_tabs if not t.startswith("config")]

    written = []
    cross_by_agg = {"pooled": [], "national": []}
    for table in tables:
        df = load(db, table)
        if df.empty:
            print(f"{table}: no outlook rows, skipping")
            continue
        df, dropped, n_common = prepare(df)
        crop = table.split("_")[-1]
        print(f"\n{table}: {df['Region'].nunique()} regions, "
              f"{df['stage'].nunique()} stages, {n_common} common (region,year) pairs")
        if dropped:
            print(f"  dropped unrepresentative stage(s): {dropped} "
                  f"(too few regions to compare)")

        for national in (False, True):
            agg = "national" if national else "pooled"
            tab = score(df, national=national)
            if tab.empty:
                continue
            csv = out_dir / f"leadtime_metrics_{agg}_{table}.csv"
            csv.parent.mkdir(parents=True, exist_ok=True)
            tab.to_csv(csv, index=False)
            written.append(csv)
            for key, col, ylab, hb in METRICS:
                title = (f"{crop.title()} — {agg} skill vs forecast issue month")
                p = plot_metric(tab, col, ylab, hb, title,
                                out_dir / f"leadtime_{key}_{agg}_{table}", units)
                if p:
                    written.append(p)
            cross_by_agg[agg].append(crossing_table(tab, crop))
            # crossing summary to stdout
            for col, hb in (("R2", True), ("RMSE", False), ("MAPE", False)):
                bits = []
                for b in BASELINES:
                    s = tab[tab["Model"] == b][col].dropna()
                    if not len(s):
                        continue
                    bv = float(s.median())
                    for m in [x for x in ML_ORDER if x in set(tab["Model"])]:
                        x = _crossings(tab[tab["Model"] == m], col, bv, hb)
                        bits.append(f"{m}>{b}:{_MONTHS[x-1] if x else 'never'}")
                print(f"  [{agg}] {col:4s} crossings — " + "  ".join(bits))

    # cross-crop crossing summary, one figure + CSV per aggregation
    for agg, frames in cross_by_agg.items():
        frames = [f for f in frames if f is not None and not f.empty]
        if not frames:
            continue
        cross = pd.concat(frames, ignore_index=True)
        csv = out_dir / f"leadtime_crossings_{agg}.csv"
        csv.parent.mkdir(parents=True, exist_ok=True)
        # month numbers -> names for the readable columns, keep numbers too
        out = cross.copy()
        for c in ("cross_r2", "cross_rmse", "cross_mape", "cross_min", "cross_max"):
            out[c + "_month"] = [
                _MONTHS[int(v) - 1] if pd.notna(v) else "never" for v in cross[c]
            ]
        out.to_csv(csv, index=False)
        written.append(csv)
        p = plot_crossings(cross, out_dir / f"leadtime_crossings_{agg}", agg)
        if p:
            written.append(p)

    print(f"\nwrote {len(written)} file(s) to {out_dir}")
    return written


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--db", required=True, help="outlook_*.db from a run_time_steps=all run")
    p.add_argument("--out", required=True, help="output directory")
    p.add_argument("--table", action="append", default=None,
                   help="crop table (repeatable); default = all non-config tables")
    p.add_argument("--units", default="Mg/ha")
    a = p.parse_args(argv)
    run(a.db, a.out, tables=a.table, units=a.units)


if __name__ == "__main__":
    sys.exit(main())
