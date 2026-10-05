"""Driver figures: how one climate impact driver (CID) moves end-of-season yield.

For one region per case and each chosen CID, one two-panel figure:

    left   the CID against the yield anomaly (% departure from the region's
           linear yield trend), every year labelled, with an OLS fit and its
           90% confidence band; points shaded by the CID's tercile,
    right  when in the season the CID matters: r between the single-month CID
           and the yield anomaly, month by month, with the chosen window marked.

Inputs are indices_runner's statistics CSVs
({Country}_{Crop}_statistics_monthly_r.csv), which already pair every CID
window with the region's reported yield. Windows are StageRange codes 'a_b' =
calendar months b..a ('2_2' = Feb, '3_2' = Feb-Mar). Every PNG gets a PDF twin
and companion CSVs listed in lookup_plots_csvs.csv.

Usage::

    from geocif.experiments import cid_drivers
    cid_drivers.run("Z:/cmongp1/GEO/outputs/deliverables/cid_drivers_2026-10-04")
"""
import logging
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

from geocif.viz._style import MONTHS, despine, style_ctx

logger = logging.getLogger(__name__)

OUTPUT_ROOTS = (Path("/gpfs/data1/cmongp1/GEO/outputs"), Path("Z:/cmongp1/GEO/outputs"))

# One entry per case; `cids` = (Index, StageRange).
CASES = [
    dict(slug="zimbabwe_maize", country="Zimbabwe", crop="Maize", region="Mashonaland West",
         stats="zw8_b2001_am/cid/indices/monthly_r/global/Zimbabwe_Maize_statistics_monthly_r.csv",
         season=[11, 12, 1, 2, 3, 4, 5],
         cids=[("MEAN_ETREF", "2_2"), ("DTR", "3_3"), ("DD", "2_2")]),
    dict(slug="usa_soybean", country="United States", crop="Soybean", region="Iowa",
         stats="usa_admin1/cid/indices/monthly_r/global/United States Of America_Soybean_statistics_monthly_r.csv",
         season=[4, 5, 6, 7, 8, 9, 10],
         cids=[("MEAN_ESI4WK", "9_9"), ("TX90p", "9_8"), ("CDD", "8_8")]),
    dict(slug="afghanistan_poppy", country="Afghanistan", crop="Poppy", region="Eastern",
         stats="poppy/cid/indices/monthly_r/global/Afghanistan_Poppy_statistics_monthly_r.csv",
         season=[10, 11, 12, 1, 2, 3, 4, 5, 6, 7, 8],
         cids=[("MAX_ETREF", "3_2")]),
]

# Display name, units, and an optional decode from the stored value.
DISPLAY = {
    "MEAN_ETREF": ("Reference ET", "mm/day", None),
    "MAX_ETREF": ("Peak Reference ET", "mm/day", None),
    "TXx": ("Hottest Day", "°C", None),
    "DTR": ("Diurnal Temperature Range", "°C", None),
    "DD": ("Dry Days", "days", None),
    "CDD": ("Longest Dry Spell", "days", None),
    "TX90p": ("Hot Days", "% of days", None),
    "WD": ("Warm-Dry Days", "days", None),
    "SU": ("Summer Days", "days", None),
    "MEAN_ESI4WK": ("Evaporative Stress Index", "ESI", lambda v: v / 10.0 - 4.0),
    "MIN_ESI4WK": ("Evaporative Stress Index, Minimum", "ESI", lambda v: v / 10.0 - 4.0),
    "MAX_ESI4WK": ("Evaporative Stress Index, Peak", "ESI", lambda v: v / 10.0 - 4.0),
}

# Okabe-Ito; the yield-reducing tercile also gets its own marker.
STRESS, FAVOUR, MIDDLE = "#D55E00", "#0072B2", "#999999"
ROLE_STYLE = {
    "stress": dict(color=STRESS, marker="v"),
    "middle": dict(color=MIDDLE, marker="o"),
    "favour": dict(color=FAVOUR, marker="^"),
}
TERCILE_ORDER = ["Highest Third", "Middle Third", "Lowest Third"]
RC = {"font.size": 10, "axes.labelsize": 10.5, "axes.titlesize": 10.5, "xtick.labelsize": 9.5,
      "ytick.labelsize": 9.5, "legend.fontsize": 9, "hatch.linewidth": 0.6}


def window_months(stage_range):
    """Calendar months of a StageRange 'a_b' (months b..a)."""
    a, b = map(int, stage_range.split("_"))
    months = [b]
    while months[-1] != a:
        months.append(months[-1] % 12 + 1)
    return months


def window_label(stage_range):
    months = window_months(stage_range)
    if len(months) == 1:
        return MONTHS[months[0] - 1]
    return f"{MONTHS[months[0] - 1]}–{MONTHS[months[-1] - 1]}"


def _slug(text):
    return "".join(c if c.isalnum() else "_" for c in str(text).lower()).strip("_")


def _num(v, fmt=".2f"):
    """Format with a true minus sign."""
    return f"{v:{fmt}}".replace("-", "−")


def _outputs_root(outputs_root):
    if outputs_root:
        return Path(outputs_root)
    for root in OUTPUT_ROOTS:
        if root.exists():
            return root
    raise FileNotFoundError(f"none of {OUTPUT_ROOTS} exists; pass outputs_root")


def load_case(case, outputs_root):
    """The region's rows for the chosen indices (chosen windows + every single month), with yields."""
    path = _outputs_root(outputs_root) / case["stats"]
    indices = {ix for ix, _ in case["cids"]}
    windows = {sr for _, sr in case["cids"]} | {f"{m}_{m}" for m in case["season"]}
    cols = ["CID", "Region", "Stage Range", "Harvest Year", "Index", "Yield (tn per ha)"]
    parts = []
    for chunk in pd.read_csv(path, usecols=cols, chunksize=500_000):
        keep = (chunk.Region == case["region"]) & chunk.Index.isin(indices) & chunk["Stage Range"].isin(windows)
        parts.append(chunk[keep])
    df = pd.concat(parts).rename(columns={"Harvest Year": "Year", "Stage Range": "StageRange",
                                          "Yield (tn per ha)": "Yield"})
    df = df.drop_duplicates(["Year", "Index", "StageRange"])
    for index, (_, _, decode) in DISPLAY.items():
        if decode is not None:
            df.loc[df.Index == index, "CID"] = decode(df.loc[df.Index == index, "CID"])
    logger.info(f"{case['slug']}: {len(df)} CID rows for {case['region']} from {path}")
    return df


def yield_anomalies(df):
    """Linear trend through the reported yields and the % departure from it."""
    y = df.dropna(subset=["Yield"]).groupby("Year", as_index=False)["Yield"].first().sort_values("Year")
    trend = np.polyval(np.polyfit(y.Year, y.Yield, 1), y.Year)
    return y.assign(Trend=trend, Anom=100.0 * (y.Yield.values - trend) / trend)


def cid_frame(df, anoms, index, stage_range):
    """Year, Yield, Trend, Anom, CID (years with both)."""
    x = df[(df.Index == index) & (df.StageRange == stage_range)].set_index("Year")["CID"]
    f = anoms.set_index("Year").join(x, how="inner").dropna(subset=["CID"])
    return f.reset_index()


def r_crit(n, alpha=0.05):
    t = stats.t.ppf(1 - alpha / 2, n - 2)
    return float(t / np.sqrt(t * t + n - 2))


def terciles(values, sign):
    """Tercile labels; the yield-reducing tercile is 'stress' (high CID if sign < 0)."""
    q1, q2 = np.quantile(values, [1 / 3, 2 / 3])
    low, high = values <= q1, values >= q2
    lab = np.where(low, "Lowest Third", np.where(high, "Highest Third", "Middle Third"))
    stress = high if sign < 0 else low
    role = np.where(stress, "stress", np.where(low | high, "favour", "middle"))
    return lab, role


def _bold_title(ax, bold, rest=""):
    t = ax.set_title(bold, loc="left", fontweight="bold")
    if rest:
        ax.annotate(rest, xy=(1, 0), xycoords=t, xytext=(5, 0), textcoords="offset points",
                    fontsize=t.get_fontsize(), va="bottom")


def _line_label(ax, y, text):
    """Name a horizontal reference line just outside the right edge of the axes."""
    ax.annotate(text, xy=(1, y), xycoords=("axes fraction", "data"), xytext=(4, 0),
                textcoords="offset points", ha="left", va="center", fontsize=9, annotation_clip=False)


def _place_labels(ax, xs, ys, labels, avoid=(), fontsize=7.5, marker_pt=4.0):
    """Label every point, each in the first nearby slot clear of other labels, markers and `avoid` boxes."""
    fig = ax.figure
    fig.canvas.draw()
    px = fig.dpi / 72.0
    pts = ax.transData.transform(np.column_stack([xs, ys]))
    box = ax.get_window_extent()
    w, h = 1.15 * fontsize * px, 0.95 * fontsize * px  # two digits
    m = marker_pt * px
    slots = [(4, 1), (4, -1 - fontsize), (-4 - w / px, 1), (-4 - w / px, -1 - fontsize),
             (-w / px / 2, 5), (-w / px / 2, -5 - fontsize), (8, -fontsize / 2), (-8 - w / px, -fontsize / 2),
             (7, 6), (7, -6 - fontsize), (-7 - w / px, 6), (-7 - w / px, -6 - fontsize)]
    taken = [(p[0] - m, p[1] - m, p[0] + m, p[1] + m) for p in pts]
    taken += [(b.x0, b.y0, b.x1, b.y1) for b in avoid]
    crowd = [((np.hypot(*(pts - p).T) < 25 * px).sum()) for p in pts]

    def clear(b):
        inside = b[0] >= box.x0 and b[2] <= box.x1 and b[1] >= box.y0 and b[3] <= box.y1
        return inside and not any(b[0] < t[2] and b[2] > t[0] and b[1] < t[3] and b[3] > t[1] for t in taken)

    for i in np.argsort(crowd)[::-1]:
        for dx, dy in slots + [slots[0]]:
            b = (pts[i, 0] + dx * px, pts[i, 1] + dy * px, pts[i, 0] + dx * px + w, pts[i, 1] + dy * px + h)
            if clear(b):
                break
        taken.append(b)
        ax.annotate(labels[i], (xs[i], ys[i]), xytext=(dx, dy), textcoords="offset points", fontsize=fontsize,
                    ha="left", va="bottom", color="0.25")


def plot_driver(case, df, anoms, index, stage_range, out_png):
    """CID-vs-yield-anomaly scatter and month-by-month r for one CID; returns the CSV frames."""
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D
    from matplotlib.patches import Patch

    name, units, _ = DISPLAY.get(index, (index, "", None))
    wlab = window_label(stage_range)
    f = cid_frame(df, anoms, index, stage_range)
    x, y = f.CID.values, f.Anom.values
    n = len(f)
    r = float(np.corrcoef(x, y)[0, 1])
    rho = float(stats.spearmanr(x, y).statistic)
    slope, intercept = np.polyfit(x, y, 1)
    lab, role = terciles(x, np.sign(r))
    f = f.assign(Tercile=lab, Role=role)

    prof = []
    for m in case["season"]:
        g = cid_frame(df, anoms, index, f"{m}_{m}")
        if len(g) >= 10 and g.CID.std() > 0:
            prof.append(dict(Month=MONTHS[m - 1], month_num=m, n=len(g),
                             r=float(np.corrcoef(g.CID, g.Anom)[0, 1]),
                             in_window=m in window_months(stage_range)))
    prof = pd.DataFrame(prof)

    with style_ctx():
        plt.rcParams.update(RC)
        fig = plt.figure(figsize=(11.5, 4.6))
        gs = fig.add_gridspec(1, 2, width_ratios=[1.15, 1.0], wspace=0.3)
        ax_sc = fig.add_subplot(gs[0, 0])
        ax_mon = fig.add_subplot(gs[0, 1])

        # left: CID vs anomaly
        xs = np.linspace(x.min(), x.max(), 100)
        resid = y - (slope * x + intercept)
        s = np.sqrt((resid ** 2).sum() / (n - 2))
        se = s * np.sqrt(1 / n + (xs - x.mean()) ** 2 / ((x - x.mean()) ** 2).sum())
        tq = stats.t.ppf(0.95, n - 2)
        ax_sc.fill_between(xs, slope * xs + intercept - tq * se, slope * xs + intercept + tq * se,
                           color="black", alpha=0.12, lw=0)
        ax_sc.plot(xs, slope * xs + intercept, color="black", lw=1.2)
        ax_sc.axhline(0, color="0.6", lw=0.6, zorder=0)
        for _, row in f.iterrows():
            st = ROLE_STYLE[row.Role]
            ax_sc.plot(row.CID, row.Anom, marker=st["marker"], color=st["color"], ms=6.5, mec="black",
                       mew=0.4, ls="none", zorder=3)
        ax_sc.set_xlabel(f"{name}, {wlab} ({units})")
        ax_sc.set_ylabel(f"{case['crop']} Yield Anomaly (% of Trend)")
        _bold_title(ax_sc, f"{case['region']}, {case['country']}", f"r = {_num(r)}")
        handles = []
        for t in TERCILE_ORDER:
            sub = f[f.Tercile == t]
            if not sub.empty:
                st = ROLE_STYLE[sub.Role.iloc[0]]
                handles.append(Line2D([], [], marker=st["marker"], color=st["color"], mec="black", mew=0.4,
                                      ms=6.5, ls="none", label=f"{t} of {name}"))
        handles += [Line2D([], [], color="black", lw=1.2, label="Linear Fit"),
                    Patch(facecolor="black", alpha=0.12, lw=0, label="90% Confidence Band")]
        leg = ax_sc.legend(handles=handles, loc="best", frameon=False, fontsize=8.5)
        fig.canvas.draw()
        _place_labels(ax_sc, x, y, [f"{int(v) % 100:02d}" for v in f.Year], avoid=[leg.get_window_extent()])

        # right: month-by-month r
        if not prof.empty:
            pos = np.arange(len(prof))
            for i, row in prof.iterrows():
                ax_mon.bar(pos[i], row.r, width=0.7, color=STRESS if row.in_window else "0.75",
                           hatch="////" if row.in_window else "", edgecolor="black", linewidth=0.4)
            rc = r_crit(int(prof.n.median()))
            for v in (rc, -rc):
                ax_mon.axhline(v, color="black", lw=0.7, ls=(0, (4, 3)))
                _line_label(ax_mon, v, "p = 0.05")
            ax_mon.axhline(0, color="black", lw=0.6)
            ax_mon.set_xticks(pos, prof.Month)
            ax_mon.set_ylim(-1, 1)
            ax_mon.set_ylabel("Correlation with Yield Anomaly (r)")
            ax_mon.set_xlabel("Month")
            ax_mon.legend(handles=[Patch(facecolor=STRESS, hatch="////", edgecolor="black", lw=0.4,
                                         label=f"In the {wlab} Window"),
                                   Patch(facecolor="0.75", edgecolor="black", lw=0.4, label="Other Months")],
                          loc="upper left" if r < 0 else "lower left", frameon=False)
        _bold_title(ax_mon, "Correlation by Month", name)

        despine(ax_sc, ax_mon)
        fig.savefig(out_png, dpi=300, bbox_inches="tight", pad_inches=0.08)
        fig.savefig(out_png.with_suffix(".pdf"), bbox_inches="tight", pad_inches=0.08)
        plt.close(fig)

    fit = pd.DataFrame([dict(Region=case["region"], Index=index, StageRange=stage_range, Window=wlab, n=n, r=r,
                             spearman_rho=rho, slope_pct_per_unit=slope, intercept=intercept,
                             r_crit_p05=r_crit(n),
                             anom_mean_lowest_third=float(f.loc[f.Tercile == "Lowest Third", "Anom"].mean()),
                             anom_mean_middle_third=float(f.loc[f.Tercile == "Middle Third", "Anom"].mean()),
                             anom_mean_highest_third=float(f.loc[f.Tercile == "Highest Third", "Anom"].mean()))])
    return f.drop(columns="Role"), fit, prof


def run(out_dir, outputs_root=None, cases=None):
    """Render every case's driver figures into out_dir/{plots,csvs}."""
    out_dir = Path(out_dir)
    lookup = []
    for case in cases or CASES:
        df = load_case(case, outputs_root)
        anoms = yield_anomalies(df)
        dp, dc = out_dir / "plots" / case["slug"], out_dir / "csvs" / case["slug"]
        dp.mkdir(parents=True, exist_ok=True)
        dc.mkdir(parents=True, exist_ok=True)
        stem = f"{_slug(case['country'])}_{_slug(case['crop'])}"
        for index, sr in case["cids"]:
            q = f"{_slug(case['region'])}_{_slug(index)}_{_slug(window_label(sr))}"
            png = dp / f"driver_{stem}_{q}.png"
            years, fit, prof = plot_driver(case, df, anoms, index, sr, png)
            for kind, frame, desc in (("years", years, "CID, yield, trend, anomaly and tercile per year"),
                                      ("fit", fit, "correlation, fit and tercile means"),
                                      ("months", prof, "single-month r with the yield anomaly")):
                csv = dc / f"driver_{stem}_{q}_{kind}.csv"
                frame.to_csv(csv, index=False)
                lookup.append(dict(plot_file=str(png.relative_to(out_dir)), csv_file=str(csv.relative_to(out_dir)),
                                   description=desc))
            logger.info(f"wrote {png}")
    pd.DataFrame(lookup).to_csv(out_dir / "lookup_plots_csvs.csv", index=False)
    return out_dir


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    run(sys.argv[1] if len(sys.argv) > 1 else "cid_drivers")
