"""Figures and HTML report of pikobs.obscountdb.

The look of the report is the one of the previous version: same tables,
same green / red gains and losses, same station cards. What changed is
that one report now holds every region and every flag criteria, selected
with two rows of buttons, and that the station figures are drawn in
parallel, one task each.
"""

import os
import re
import traceback
from typing import Any, Dict, List, Optional, Sequence

import matplotlib
matplotlib.use('Agg')

import pikobs
from pikobs.figures import save_figure
from pikobs.obsdb import open_result
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from rich import box
from rich.console import Console
from rich.table import Table

AGR_METRICS = ('omp', 'oma')

# Row holding the counts of a station over every varno (see obscountdb.py).
TOTAL_VARNO = -1

# the two runs, in the colours every module uses
from pikobs.configobs.style import (CTL_COLOUR as REF_COLOR,
                                    EXP_COLOUR as EXP_COLOR)

_AGR_STYLE = {
    'nobs': {'ls': '-',  'marker_ref': 'o', 'marker_exp': 's'},
    'omp':  {'ls': '--', 'marker_ref': '^', 'marker_exp': 'v'},
    'oma':  {'ls': ':',  'marker_ref': 'D', 'marker_exp': 'X'},
}

_PALETTE = ['#4C72B0', '#DD8452', '#55A868', '#C44E52', '#8172B3',
            '#937860', '#DA8BC3', '#8C8C8C', '#CCB974', '#64B5CD']


def _norm_agr(agr):
    if agr is None:
        return []
    if isinstance(agr, str):
        agr = [agr]
    out = []
    for a in agr:
        a = str(a).strip().lower()
        if a in AGR_METRICS and a not in out:
            out.append(a)
    return out


def _safe(text) -> str:
    return re.sub(r'[^A-Za-z0-9._+-]', '_', str(text))


FIGURE_DIR = "figures"


def _stn_color(stn) -> str:
    import hashlib
    h = int(hashlib.md5(str(stn).encode()).hexdigest(), 16)
    return _PALETTE[h % len(_PALETTE)]


def varno_label(varno) -> str:
    """'11215 U [m/s]' when pikobs knows the variable, the code otherwise."""
    if varno is None or int(varno) == TOTAL_VARNO:
        return 'all'
    try:
        name, units, _ = pikobs.type_varno(int(varno))
        return f"{int(varno)} {name} {units}".strip()
    except Exception:
        return str(int(varno))


def _db_path(pathwork, family, name, datestart, dateend) -> str:
    safe = str(name).replace(' ', '_').replace('/', '_')
    return os.path.join(pathwork, family,
                        f"{safe}_{datestart}_{dateend}_{family}.db")


def _read(pathwork, family, name, datestart, dateend, sql, params=()):
    """The query, or an empty table when there is nothing to read.

    A family whose files were all missing leaves a database with no
    'moyenne' table at all: that is not an error, it is a family with no
    data, and the report says so in its own way.
    """
    path = _db_path(pathwork, family, name, datestart, dateend)
    if not os.path.isfile(path):
        return pd.DataFrame()
    try:
        with open_result(path) as conn:
            if not conn.execute("SELECT 1 FROM sqlite_master WHERE type = "
                                "'table' AND name = 'moyenne';").fetchone():
                return pd.DataFrame()
            return pd.read_sql_query(sql, conn, params=params)
    except Exception as exc:
        print(f"[obscountdb] could not read {os.path.basename(path)}: {exc}",
              flush=True)
        return pd.DataFrame()


# ─────────────────────────────────────────────────────────────────────────────
# Figures: one task per (region, flag, family, station)
# ─────────────────────────────────────────────────────────────────────────────

def obscountdb_figure_tasks(pathwork: str, families: Sequence[str],
                            names_in: Sequence[str], regions: Sequence[str],
                            flags: Sequence[str], datestart: str, dateend: str,
                            agr: Optional[Sequence[str]] = None
                            ) -> List[Dict[str, Any]]:
    """List the station figures to draw, from what the databases hold."""
    agr_list = _norm_agr(agr)
    tasks: List[Dict[str, Any]] = []
    for family in families:
        found = pd.DataFrame()
        for name in names_in:
            df = _read(pathwork, family, name, datestart, dateend,
                       "SELECT DISTINCT region, flag, id_stn, varno "
                       "FROM moyenne;")
            found = pd.concat([found, df]) if not found.empty else df
        if found.empty:
            continue
        found = found.drop_duplicates()
        for region in regions:
            for flag in flags:
                sel = found[(found['region'] == region) &
                            (found['flag'] == flag)]
                if sel.empty:
                    continue
                # one figure per varno when the departures are drawn, one
                # per station otherwise
                varnos = [TOTAL_VARNO]
                if agr_list:
                    varnos += sorted(int(v) for v in sel['varno'].unique()
                                     if int(v) != TOTAL_VARNO)
                for varno in varnos:
                    stns = sel[sel['varno'].isin([varno, TOTAL_VARNO])]
                    for stn in sorted(stns['id_stn'].astype(str).unique()):
                        tasks.append({
                            'pathwork': pathwork, 'family': family,
                            'names_in': list(names_in), 'region': region,
                            'flag': flag, 'id_stn': stn, 'varno': varno,
                            'agr': agr_list, 'datestart': datestart,
                            'dateend': dateend,
                        })
    return tasks


def _series(task, name) -> pd.DataFrame:
    """Per-cycle counts of the station and departure moments of one varno."""
    metrics = task['agr']
    varno = int(task.get('varno', TOTAL_VARNO))
    where = "WHERE region = ? AND flag = ? AND id_stn = ?"
    args = (task['region'], task['flag'], task['id_stn'])

    df = _read(task['pathwork'], task['family'], name, task['datestart'],
               task['dateend'],
               f"SELECT date, SUM(Nobsdata) AS nobs, "
               f"SUM(Nobsprofile) AS profiles FROM moyenne {where} "
               f"AND varno = {TOTAL_VARNO} GROUP BY date ORDER BY date;", args)
    if df.empty:
        return df
    if metrics and varno != TOTAL_VARNO:
        cols = ["date"]
        for m in AGR_METRICS:
            if m in metrics:
                cols += [f"SUM(n_{m}) AS n_{m}", f"SUM(s_{m}) AS s_{m}",
                         f"SUM(s2_{m}) AS s2_{m}",
                         f"MIN(min_{m}) AS min_{m}", f"MAX(max_{m}) AS max_{m}"]
        dep = _read(task['pathwork'], task['family'], name, task['datestart'],
                    task['dateend'],
                    f"SELECT {', '.join(cols)} FROM moyenne {where} "
                    f"AND varno = {varno} GROUP BY date ORDER BY date;", args)
        if not dep.empty:
            df = df.merge(dep, on='date', how='left')
    df['date'] = pd.to_datetime(df['date'].astype(str), format='%Y%m%d%H',
                                errors='coerce')
    df = df.dropna(subset=['date'])
    for m in metrics:
        n, s, s2 = df.get(f'n_{m}'), df.get(f's_{m}'), df.get(f's2_{m}')
        if n is None or s is None:
            continue
        with np.errstate(invalid='ignore', divide='ignore'):
            mean = np.where(n > 0, s / n, np.nan)
            df[f'avg_{m}'] = mean
            if s2 is not None:
                var = np.where(n > 0, s2 / n - mean ** 2, np.nan)
                df[f'std_{m}'] = np.sqrt(np.maximum(np.asarray(var, dtype=float), 0.0))
    return df


def _finite(frames, cols) -> np.ndarray:
    vals = [df[c].to_numpy(dtype=float) for df in frames for c in cols
            if not df.empty and c in df.columns]
    if not vals:
        return np.array([])
    data = np.concatenate(vals)
    return data[np.isfinite(data)]


def _scale_panel(ax, frames, cols) -> None:
    """Fit the y axis to the given columns, with a small margin."""
    data = _finite(frames, cols)
    if data.size == 0:
        return
    lo, hi = float(data.min()), float(data.max())
    pad = max((hi - lo) * 0.12, abs(hi) * 0.05, 1e-6)
    ax.set_ylim(min(lo - pad, -pad / 3), hi + pad)


def _units(task) -> str:
    varno = int(task.get('varno', TOTAL_VARNO))
    if varno == TOTAL_VARNO:
        return ''
    try:
        _, units, _ = pikobs.type_varno(varno)
        return str(units)
    except Exception:
        return ''


def _fmt_departure(val) -> str:
    if val is None or (isinstance(val, float) and np.isnan(val)):
        return "n/a"
    a = abs(val)
    if a == 0:
        return "0"
    if a >= 100:
        return f"{val:,.1f}"
    if a >= 1:
        return f"{val:.2f}"
    if a >= 0.001:
        return f"{val:.3f}"
    return f"{val:.2e}"


def obscountdb_station_figure(task: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Draw the time series of one station and return it as an HTML card."""
    try:
        return _station_figure(task)
    except Exception:
        print(f"[obscountdb] figure failed for {task.get('id_stn')} "
              f"({task.get('family')}, {task.get('region')}, "
              f"{task.get('flag')}):\n{traceback.format_exc()}", flush=True)
        plt.close('all')
        return None


def _station_figure(task: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    name1, name2 = task['names_in'][0], task['names_in'][1]
    stn = task['id_stn']
    agr_list = task['agr']

    df_ref = _series(task, name1)
    df_exp = _series(task, name2)
    if df_ref.empty and df_exp.empty:
        return None

    # metrics with data on either side
    general = int(task.get('varno', TOTAL_VARNO)) == TOTAL_VARNO
    plotted, empty = [], []
    if not general:
        for metric in agr_list:
            has = any(not df.empty and f'avg_{metric}' in df.columns
                      and df[f'avg_{metric}'].notna().any()
                      for df in (df_ref, df_exp))
            (plotted if has else empty).append(metric)
        if not plotted:
            return None

    has_range = {m: any(not df.empty and f'min_{m}' in df.columns
                        and df[f'min_{m}'].notna().any()
                        for df in (df_ref, df_exp)) for m in plotted}
    # general card: observations and profiles per cycle
    # varno card: the departure rows of that varno
    n_rows = (2 if general else 0) + len(plotted) + sum(has_range.values())
    row_h = 3.0
    fig, axes = plt.subplots(n_rows, 1, figsize=(10, 1.4 + row_h * n_rows),
                             sharex=True, squeeze=False)
    axes = axes[:, 0]
    stn_col = _stn_color(stn)

    summary = []
    k = -1
    s_nobs = _AGR_STYLE['nobs']
    if general:
        for k, (col, label) in enumerate((('nobs', 'Nobs'),
                                          ('profiles', 'Profiles'))):
            ax_n = axes[k]
            for df, name, color, marker, tag in (
                    (df_ref, name1, REF_COLOR, s_nobs['marker_ref'], 'Ref'),
                    (df_exp, name2, EXP_COLOR, s_nobs['marker_exp'], 'Exp')):
                if df.empty or col not in df.columns:
                    continue
                ax_n.plot(df['date'], df[col], marker=marker, markersize=5,
                          linestyle=s_nobs['ls'], linewidth=1.8,
                          label=f'{tag}: {name}', color=color)
                summary.append(f'{label}({tag})='
                               f'{int(np.nansum(df[col].to_numpy())):,}')
            ax_n.set_ylabel(label, fontsize=11, fontweight='bold')
            ax_n.grid(True, linestyle=':', alpha=0.6)
            ax_n.legend(fontsize=9, loc='best', ncol=2)
            ax_n.tick_params(labelsize=9)

    # One row per departure metric (mean and std), plus one row with the
    # extremes of each cycle when they are available
    for metric in plotted:
        k += 1
        ax_m = axes[k]
        st = _AGR_STYLE.get(metric, _AGR_STYLE['omp'])
        ax_m.axhline(0.0, color='gray', lw=0.8, ls='-', alpha=0.5)
        for df, name, color, marker, tag in (
                (df_ref, name1, REF_COLOR, st['marker_ref'], 'Ref'),
                (df_exp, name2, EXP_COLOR, st['marker_exp'], 'Exp')):
            acol, scol = f'avg_{metric}', f'std_{metric}'
            if df.empty or acol not in df.columns or not df[acol].notna().any():
                continue
            ax_m.plot(df['date'], df[acol], marker=marker, markersize=4.5,
                      linestyle=st['ls'], linewidth=1.6, zorder=3,
                      label=f'{tag} {metric} (mean)', color=color)
            summary.append(f'{metric}({tag})='
                           f'{_fmt_departure(float(np.nanmean(df[acol])))}')
            if scol in df.columns and df[scol].notna().any():
                ax_m.plot(df['date'], df[scol], marker='o', markersize=3.5,
                          markerfacecolor='none', linestyle=':', linewidth=1.2,
                          zorder=3, label=f'{tag} {metric} (std)', color=color,
                          alpha=0.6)
                summary.append(f'std({tag})='
                               f'{_fmt_departure(float(np.nanmean(df[scol])))}')
        ax_m.set_ylabel(f'{metric} {_units(task)}\n(solid=mean, dotted=std)',
                        fontsize=10,
                        fontweight='bold')
        _scale_panel(ax_m, (df_ref, df_exp), (f'avg_{metric}', f'std_{metric}'))
        ax_m.grid(True, linestyle=':', alpha=0.6)
        ax_m.legend(fontsize=8, loc='best', ncol=2)
        ax_m.tick_params(labelsize=9)

        if not has_range[metric]:
            continue
        k += 1
        ax_r = axes[k]
        ax_r.axhline(0.0, color='gray', lw=0.8, ls='-', alpha=0.5)
        for df, color, tag in ((df_ref, REF_COLOR, 'Ref'),
                               (df_exp, EXP_COLOR, 'Exp')):
            lo, hi = f'min_{metric}', f'max_{metric}'
            if df.empty or lo not in df.columns or not df[lo].notna().any():
                continue
            ax_r.plot(df['date'], df[hi], linestyle='-', linewidth=1.3,
                      marker='^', markersize=3.5, color=color,
                      label=f'{tag} max')
            ax_r.plot(df['date'], df[lo], linestyle='--', linewidth=1.3,
                      marker='v', markersize=3.5, color=color,
                      label=f'{tag} min')
            ax_r.fill_between(df['date'], df[lo], df[hi], color=color,
                              alpha=0.07, linewidth=0)
            summary.append(f'{tag} {metric} in ['
                           f'{_fmt_departure(float(np.nanmin(df[lo])))}, '
                           f'{_fmt_departure(float(np.nanmax(df[hi])))}]')
        ax_r.set_ylabel(f'{metric} {_units(task)}\n(min / max per cycle)',
                        fontsize=10,
                        fontweight='bold')
        ax_r.grid(True, linestyle=':', alpha=0.6)
        ax_r.legend(fontsize=8, loc='best', ncol=2)
        ax_r.tick_params(labelsize=9)

    ax_bottom = axes[-1]
    ax_bottom.set_xlabel('Date', fontsize=10)
    locator = mdates.AutoDateLocator(minticks=5, maxticks=10)
    ax_bottom.xaxis.set_major_locator(locator)
    ax_bottom.xaxis.set_major_formatter(mdates.ConciseDateFormatter(locator))

    head = f'Station: {stn}'
    if int(task.get('varno', TOTAL_VARNO)) != TOTAL_VARNO:
        head += f'   |   varno {varno_label(task["varno"])}'
    fig.suptitle(head, fontsize=14, fontweight='bold',
                 color='white', x=0.5, y=1.02,
                 bbox=dict(boxstyle='round,pad=0.4', facecolor=stn_col,
                           edgecolor='none'))
    if summary:
        # the numbers of the period on two balanced lines: one long line
        # would force the card to be much wider than the plots need
        half = (len(summary) + 1) // 2
        text = "  |  ".join(summary[:half])
        if summary[half:]:
            text += "\n" + "  |  ".join(summary[half:])
        fig.text(0.5, 0.975, text, ha='center', va='top', linespacing=1.5,
                 fontsize=10.5, fontweight='bold', color='#222')

    for ax_ in axes:
        for spine in ax_.spines.values():
            spine.set_edgecolor(stn_col)
            spine.set_linewidth(1.6)

    fig.tight_layout(rect=[0, 0, 1, 0.93])
    # One PNG per station on disk: a report with several regions and
    # criteria would weigh hundreds of MB with the images embedded.
    rel = os.path.join(FIGURE_DIR,
                       f"{_safe(task['region'])}_{_safe(task['flag'])}_"
                       f"{_safe(task['family'])}_"
                       f"{_safe(task.get('varno', TOTAL_VARNO))}_"
                       f"{_safe(stn)}.png")
    out = os.path.join(task['pathwork'], rel)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    save_figure(fig, out, svg=task.get('svg', False), dpi=110)
    plt.close(fig)

    cell = (f"<div style='background: white; padding: 12px; "
            f"border: 1px solid #ddd; border-left: 7px solid {stn_col}; "
            f"border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); "
            f"flex: 1 1 560px; max-width: 720px;'>"
            f"<img src='{rel}' alt='Plot {stn}' loading='lazy' "
            f"class='zoom' onclick=\"openLightbox(this.src)\" "
            f"style='width:100%; height:auto; display:block;'>")
    if empty:
        cell += (f"<p class='note-warn'>Note: the <b>{', '.join(empty)}</b> "
                 f"column{'s are' if len(empty) > 1 else ' is'} empty for "
                 f"station {stn} - no panel plotted for "
                 f"{'them' if len(empty) > 1 else 'it'}.</p>")
    cell += "</div>"

    return {'region': task['region'], 'flag': task['flag'],
            'family': task['family'], 'id_stn': stn,
            'varno': int(task.get('varno', TOTAL_VARNO)), 'html': cell}


# ─────────────────────────────────────────────────────────────────────────────
# Tables
# ─────────────────────────────────────────────────────────────────────────────

def _calculate_pct(diff, ref):
    return np.where(ref == 0, np.where(diff > 0, 100.0, 0.0),
                    (diff / ref) * 100.0)


def _fmt_mean(val):
    if val >= 100:
        return f"{val:,.1f}" if val < 1000 else f"{val:,.0f}"
    if val >= 10:
        return f"{val:.1f}"
    if val >= 1:
        return f"{val:.2f}"
    return f"{val:.3f}"


def _add_mean_cols(df, nobs_ref, nobs_exp, prof_ref, prof_exp, n_ts):
    df['MeanNobs_REF'] = (df[nobs_ref] / n_ts).apply(_fmt_mean)
    df['MeanNobs_EXP'] = (df[nobs_exp] / n_ts).apply(_fmt_mean)
    if prof_ref in df.columns and prof_exp in df.columns:
        df['MeanProf_REF'] = (df[prof_ref] / n_ts).apply(_fmt_mean)
        df['MeanProf_EXP'] = (df[prof_exp] / n_ts).apply(_fmt_mean)
    return df


def _totals(pathwork, families, names_in, region, flag, datestart, dateend,
            by_station: bool) -> pd.DataFrame:
    frames = []
    group = "id_stn, " if by_station else ""
    for family in families:
        for name in names_in:
            sql = (f"SELECT {group}SUM(Nobsdata) AS Nobs, "
                   f"SUM(Nobsprofile) AS NobsProfiles FROM moyenne "
                   f"WHERE region = ? AND flag = ? AND varno = {TOTAL_VARNO}"
                   + (" GROUP BY id_stn;" if by_station else ";"))
            df = _read(pathwork, family, name, datestart, dateend, sql,
                       (region, flag))
            if df.empty or df['Nobs'].isna().all():
                continue
            df['family'], df['name'] = family, name
            frames.append(df)
    return pd.concat(frames) if frames else pd.DataFrame()


def _pivot(df, names_in, index) -> pd.DataFrame:
    name1, name2 = names_in
    piv = df.pivot_table(index=index, columns='name',
                         values=['Nobs', 'NobsProfiles'],
                         aggfunc='sum').fillna(0)
    piv.columns = [f"{a}_{b}" for a, b in piv.columns]
    for col in (f'Nobs_{name1}', f'Nobs_{name2}',
                f'NobsProfiles_{name1}', f'NobsProfiles_{name2}'):
        if col not in piv.columns:
            piv[col] = 0
    piv['Diff_Nobs'] = piv[f'Nobs_{name2}'] - piv[f'Nobs_{name1}']
    piv['Pct_Nobs'] = _calculate_pct(piv['Diff_Nobs'], piv[f'Nobs_{name1}'])
    piv['Diff_Profiles'] = (piv[f'NobsProfiles_{name2}']
                            - piv[f'NobsProfiles_{name1}'])
    piv['Pct_Profiles'] = _calculate_pct(piv['Diff_Profiles'],
                                         piv[f'NobsProfiles_{name1}'])
    piv = piv.rename(columns={
        f'Nobs_{name1}': f'Nobs (Ref: {name1})',
        f'Nobs_{name2}': f'Nobs ({name2})',
        f'NobsProfiles_{name1}': f'Profiles (Ref: {name1})',
        f'NobsProfiles_{name2}': f'Profiles ({name2})',
    }).reset_index()
    return piv


def _order_columns(piv, names_in, index_cols, n_timesteps):
    name1, name2 = names_in
    piv = _add_mean_cols(piv, f'Nobs (Ref: {name1})', f'Nobs ({name2})',
                         f'Profiles (Ref: {name1})', f'Profiles ({name2})',
                         n_timesteps)
    order = index_cols + [
        f'Nobs (Ref: {name1})', f'Nobs ({name2})', 'Diff_Nobs', 'Pct_Nobs',
        'MeanNobs_REF', 'MeanNobs_EXP',
        f'Profiles (Ref: {name1})', f'Profiles ({name2})', 'Diff_Profiles',
        'Pct_Profiles', 'MeanProf_REF', 'MeanProf_EXP']
    piv = piv[[c for c in order if c in piv.columns]]
    for col in (f'Nobs (Ref: {name1})', f'Nobs ({name2})', 'Diff_Nobs',
                f'Profiles (Ref: {name1})', f'Profiles ({name2})',
                'Diff_Profiles'):
        if col in piv.columns:
            piv[col] = piv[col].astype(int)
    return piv


def _color_html_diff(val):
    if isinstance(val, (int, float)):
        if val > 0:
            return 'color: green; font-weight: bold;'
        if val < 0:
            return 'color: red; font-weight: bold;'
    return ''


def _styled_html(df) -> str:
    subset = [c for c in ('Diff_Nobs', 'Pct_Nobs', 'Diff_Profiles',
                          'Pct_Profiles') if c in df.columns]
    fmt = {'Pct_Nobs': '{:+.1f}%', 'Pct_Profiles': '{:+.1f}%'}
    styler = df.style
    apply_map = getattr(styler, 'map', None) or styler.applymap
    return (apply_map(_color_html_diff, subset=subset)
            .format({k: v for k, v in fmt.items() if k in df.columns})
            .hide(axis='index').to_html())


TABLE_DIR = "tables"


def _save_csv(df, pathwork: str, name: str) -> str:
    """Same numbers as the HTML table, ready for a spreadsheet."""
    out = os.path.join(pathwork, TABLE_DIR, name)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    df.to_csv(out, index=False)
    return out


_RICH_LABELS = {
    'Diff_Nobs': 'dNobs', 'Pct_Nobs': '%Nobs',
    'Diff_Profiles': 'dProf', 'Pct_Profiles': '%Prof',
    'MeanNobs_REF': '~Nobs_REF\n(/6h)', 'MeanNobs_EXP': '~Nobs_EXP\n(/6h)',
    'MeanProf_REF': '~Prof_REF\n(/6h)', 'MeanProf_EXP': '~Prof_EXP\n(/6h)',
}


def _rich_table(console, df, names_in, title, index_cols):
    name1, name2 = names_in
    labels = dict(_RICH_LABELS)
    labels.update({
        f'Nobs (Ref: {name1})': 'Nobs_REF', f'Nobs ({name2})': 'Nobs_EXP',
        f'Profiles (Ref: {name1})': 'Prof_REF',
        f'Profiles ({name2})': 'Prof_EXP',
    })
    table = Table(title=title, box=box.ROUNDED, header_style="bold cyan")
    for col in df.columns:
        table.add_column(labels.get(col, col), justify="right",
                         min_width=10, overflow="fold", no_wrap=True)

    def colored(val, pct=False):
        txt = f"{val:+.1f}%" if pct else f"{int(val):+,}"
        if val > 0:
            return f"[bold green]{txt}[/]"
        if val < 0:
            return f"[bold red]{txt}[/]"
        return "0.0%" if pct else "0"

    for _, row in df.iterrows():
        vals = [str(row[c]) for c in index_cols]
        vals += [f"{int(row[f'Nobs (Ref: {name1})']):,}",
                 f"{int(row[f'Nobs ({name2})']):,}",
                 colored(row['Diff_Nobs']), colored(row['Pct_Nobs'], True),
                 str(row['MeanNobs_REF']), str(row['MeanNobs_EXP']),
                 f"{int(row[f'Profiles (Ref: {name1})']):,}",
                 f"{int(row[f'Profiles ({name2})']):,}",
                 colored(row['Diff_Profiles']),
                 colored(row['Pct_Profiles'], True)]
        if 'MeanProf_REF' in df.columns:
            vals += [str(row['MeanProf_REF']), str(row['MeanProf_EXP'])]
        table.add_row(*vals)
    console.print(table)


# ─────────────────────────────────────────────────────────────────────────────
# HTML report
# ─────────────────────────────────────────────────────────────────────────────

_HTML_HEAD = """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>{title}</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 40px; background-color: #f9f9f9; }}
        h1, h2, h3, h4 {{ color: #333; }}
        h1 {{ border-bottom: 2px solid #4C72B0; padding-bottom: 10px; }}
        table {{ border-collapse: collapse; width: 95%; margin-bottom: 40px; background-color: white; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }}
        th, td {{ border: 1px solid #ddd; padding: 12px; text-align: center; }}
        th {{ background-color: #4C72B0; color: white; position: sticky; top: 0; }}
        tr:nth-child(even) {{ background-color: #f2f2f2; }}
        tr:hover {{ background-color: #ddd; }}
        td.mean-col {{ background-color: #eef4ff; font-style: italic; color: #2a4d8f; }}
        .note {{ font-size: 0.85em; color: #666; font-style: italic; margin-bottom: 8px; }}
        .note-warn {{ font-size: 0.85em; color: #b00; font-style: italic; margin-bottom: 8px; }}
        .selector {{ position: sticky; top: 0; z-index: 20; background: #f9f9f9;
                     padding: 10px 0 12px 0; border-bottom: 1px solid #e2e2e2;
                     margin-bottom: 20px; }}
        .selector .row {{ margin: 6px 0; }}
        .selector .lab {{ display: inline-block; min-width: 90px; font-size: 0.85em;
                          text-transform: uppercase; letter-spacing: .4px;
                          color: #34495e; font-weight: bold; }}
        .selector button {{ background: white; color: #4C72B0; border: 1px solid #4C72B0;
                            border-radius: 4px; padding: 6px 14px; margin-right: 6px;
                            font-size: 13px; cursor: pointer; }}
        .selector button:hover {{ background: #eef4ff; }}
        .selector button.active {{ background: #4C72B0; color: white; font-weight: bold; }}
        .varno-bar {{ margin: 6px 0 16px 0; }}
        .varno-bar .lab {{ display: inline-block; min-width: 90px;
                           font-size: 0.85em; text-transform: uppercase;
                           letter-spacing: .4px; color: #34495e;
                           font-weight: bold; }}
        .varno-bar button {{ background: white; color: #4C72B0;
                             border: 1px solid #4C72B0; border-radius: 4px;
                             padding: 5px 12px; margin-right: 6px;
                             font-size: 12.5px; cursor: pointer; }}
        .varno-bar button:hover {{ background: #eef4ff; }}
        .varno-bar button.active {{ background: #4C72B0; color: white;
                                    font-weight: bold; }}
        .panel {{ display: none; }}
        .panel.active {{ display: block; }}
        img.zoom {{ cursor: zoom-in; }}
        .lightbox {{ display: none; position: fixed; top: 0; left: 0; width: 100%;
                     height: 100%; background: rgba(20,20,20,.92); z-index: 1000;
                     overflow: auto; text-align: center; cursor: zoom-out; }}
        .lightbox.open {{ display: block; }}
        .lightbox img {{ max-width: none; margin: 40px auto; display: block; }}
        .lightbox-hint {{ position: fixed; top: 14px; right: 18px; color: #ecf0f1;
                          font-size: 13px; font-family: monospace; z-index: 1001; }}
    </style>
</head>
<body>
"""

_HTML_JS = """
<div id="lightbox" class="lightbox" onclick="closeLightbox()">
  <div class="lightbox-hint">Click anywhere or press Esc to close</div>
  <img id="lightboxImg" alt="">
</div>
<script>
const STATE = {{region: {region0}, flag: {flag0}}};
function pickVarno(group, varno) {{
  document.querySelectorAll(`.cards[data-group="${{group}}"]`).forEach(d => {{
    if (d.dataset.varno === '{total_varno}') return;   // general cards stay
    d.style.display = (d.dataset.varno === varno) ? 'flex' : 'none';
  }});
  document.querySelectorAll(`.varno-bar button[data-group="${{group}}"]`)
    .forEach(b => b.classList.toggle('active', b.dataset.varno === varno));
}}
function openLightbox(src) {{
  document.getElementById('lightboxImg').src = src;
  document.getElementById('lightbox').classList.add('open');
}}
function closeLightbox() {{
  document.getElementById('lightbox').classList.remove('open');
}}
document.addEventListener('keydown', e => {{
  if (e.key === 'Escape') closeLightbox();
}});
function show() {{
  document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));
  const id = 'panel-' + STATE.region + '|' + STATE.flag;
  const panel = document.getElementById(id);
  if (panel) panel.classList.add('active');
  document.querySelectorAll('button[data-kind]').forEach(b => {{
    b.classList.toggle('active', STATE[b.dataset.kind] === b.dataset.value);
  }});
  document.getElementById('missing').style.display = panel ? 'none' : 'block';
  location.hash = encodeURIComponent(STATE.region + '|' + STATE.flag);
}}
function pick(kind, value) {{ STATE[kind] = value; show(); }}
if (location.hash.length > 1) {{
  const parts = decodeURIComponent(location.hash.substring(1)).split('|');
  if (parts.length === 2) {{ STATE.region = parts[0]; STATE.flag = parts[1]; }}
}}
show();
</script>
</body>
</html>
"""


def obscountdb_report(pathwork: str, families: Sequence[str],
                      names_in: Sequence[str], paths_in: Sequence[str],
                      regions: Sequence[str], flags: Sequence[str],
                      datestart: str, dateend: str,
                      agr: Optional[Sequence[str]] = None,
                      figures: Optional[List[Dict[str, Any]]] = None,
                      skipped: Optional[Dict[tuple, List[str]]] = None
                      ) -> str:
    """Build the single HTML report holding every region and criteria."""
    if len(names_in) != 2:
        raise ValueError("obscountdb compares exactly two runs")
    name1, name2 = names_in
    agr_list = _norm_agr(agr)
    figures = figures or []
    console = Console(width=220)

    try:
        dt_start = pd.to_datetime(str(datestart), format='%Y%m%d%H')
        dt_end = pd.to_datetime(str(dateend), format='%Y%m%d%H')
        n_timesteps = max(1, int((dt_end - dt_start).total_seconds()
                                 / (6 * 3600)) + 1)
    except Exception:
        n_timesteps = 1

    # station cards, grouped by (region, flag, family)
    cards: Dict[tuple, List[str]] = {}
    varnos: List[int] = []
    for fig in figures:
        varno = int(fig.get('varno', TOTAL_VARNO))
        cards.setdefault((fig['region'], fig['flag'], fig['family'], varno),
                         []).append((fig['id_stn'], fig['html']))
        if varno not in varnos:
            varnos.append(varno)
    varnos = sorted(varnos)

    title = (f"Observation Report | {name1} (Ref) vs {name2} | "
             f"Period: {datestart} {dateend}")
    html = [_HTML_HEAD.format(title=title)]
    html.append(f"<h1>Period: {datestart}-{dateend} every 06h: {name1} (Ref) "
                f"vs {name2}</h1>")
    if paths_in and len(paths_in) == 2:
        html.append(
            "<div style='background:#eef4ff; border:1px solid #cdd9f0; "
            "border-radius:8px; padding:10px 14px; margin-bottom:12px; "
            "font-size:0.9em; color:#2a4d8f;'>"
            f"<b>REF</b> ({name1}) &nbsp;=&nbsp; <code>{paths_in[0]}</code><br>"
            f"<b>EXP</b> ({name2}) &nbsp;=&nbsp; <code>{paths_in[1]}</code>"
            "</div>")
    html.append(f"<p class='note'>Mean columns = total / {n_timesteps} 6h "
                f"timesteps in the period.</p>")
    if skipped:
        # the numbers still stand, but they rest on fewer cycles: say which
        rows = []
        for (kind, family), cycles_ in sorted(skipped.items()):
            uniq = sorted(set(cycles_))
            rows.append(f"<li><b>{family}</b>: {len(uniq)} {kind} file(s), "
                        f"counted as zero &mdash; "
                        f"{', '.join(uniq[:12])}"
                        f"{' ...' if len(uniq) > 12 else ''}</li>")
        html.append(
            "<div style='background:#fff6e5; border:1px solid #f0d9a8; "
            "border-radius:8px; padding:10px 14px; margin-bottom:12px; "
            "font-size:0.9em; color:#8a5a00;'>"
            "<b>Warning:</b> some 6-h files could not be read. The run went "
            "on and those cycles count zero, so the totals and the means "
            "below rest on fewer cycles than the period suggests."
            f"<ul style='margin:6px 0 0 18px'>{''.join(rows)}</ul></div>")
    if agr_list:
        html.append(f"<p class='note'>Time-series secondary panel(s) show "
                    f"{', '.join(agr_list)} per cycle for REF and EXP -- "
                    f"solid/dashed/dotted line = mean, thin dotted line "
                    f"(hollow markers) = std, both per cycle; the period mean "
                    f"of each is shown in the plot title.</p>")

    # selector bar
    html.append("<div class='selector'>")
    for kind, values, label in (('region', regions, 'Region'),
                                ('flag', flags, 'Criteria')):
        html.append(f"<div class='row'><span class='lab'>{label}</span>")
        for v in values:
            html.append(f"<button data-kind='{kind}' data-value='{v}' "
                        f"onclick=\"pick('{kind}', '{v}')\">{v}</button>")
        html.append("</div>")
    html.append("</div>")
    html.append("<div id='missing' style='display:none' class='note-warn'>"
                "No data for this region and criteria.</div>")

    for region in regions:
        for flag in flags:
            panel = _panel_html(pathwork, families, names_in, region, flag,
                                datestart, dateend, n_timesteps, cards,
                                console)
            if panel is None:
                continue
            html.append(f"<div class='panel' id='panel-{region}|{flag}'>")
            html.append(panel)
            html.append("</div>")

    html.append(_HTML_JS.format(region0=repr(regions[0]),
                                flag0=repr(flags[0]),
                                total_varno=TOTAL_VARNO))

    out = os.path.join(pathwork, "pikobs_obscountdb_viewer.html")
    with open(out, "w", encoding="utf-8") as fh:
        fh.write("\n".join(html))
    console.print(f"[bold cyan]Report saved to: {out}[/bold cyan]")
    return out


def _panel_html(pathwork, families, names_in, region, flag, datestart,
                dateend, n_timesteps, cards, console) -> Optional[str]:
    name1, name2 = names_in
    parts: List[str] = []

    df_ov = _totals(pathwork, families, names_in, region, flag,
                    datestart, dateend, by_station=False)
    if df_ov.empty:
        return None
    piv_ov = _order_columns(_pivot(df_ov, names_in, 'family'), names_in,
                            ['family'], n_timesteps)

    _rich_table(console, piv_ov, names_in,
                f"OVERALL SUMMARY - {region} {flag} | Period: {datestart} "
                f"{dateend} every 06h | {name1} (Ref) vs {name2}", ['family'])

    parts.append(f"<h2>Overall Summary &mdash; {region} / {flag}</h2>")
    parts.append(f"<p class='note'>Mean columns = total obs / {n_timesteps} "
                 f"6h timesteps (YYYYMMDDHH format).</p>")
    parts.append(_styled_html(piv_ov))
    _save_csv(piv_ov, pathwork, f"Overall_{region}_{flag}.csv")

    df_stn = _totals(pathwork, families, names_in, region, flag,
                     datestart, dateend, by_station=True)
    if not df_stn.empty:
        piv_stn = _order_columns(
            _pivot(df_stn, names_in, ['family', 'id_stn']), names_in,
            ['family', 'id_stn'], n_timesteps)
        parts.append("<h2>Station Breakdown by Family</h2>")
        for fam in families:
            df_fam = piv_stn[piv_stn['family'] == fam].drop(columns=['family'])
            if df_fam.empty:
                continue
            _rich_table(console, df_fam, names_in,
                        f"STATIONS - {region} {flag} - Family: {fam} | "
                        f"Mean per 6h timestep ({n_timesteps} steps)",
                        ['id_stn'])
            parts.append(f"<h3>Family: {fam}</h3>")
            parts.append(_styled_html(df_fam))
            _save_csv(df_fam, pathwork,
                      f"Stations_{_safe(fam)}_{region}_{flag}.csv")

            fam_varnos = sorted(v for (r, f, fm, v) in cards
                                if (r, f, fm) == (region, flag, fam))
            if not fam_varnos:
                continue

            def _cards_div(varno, style):
                out = [f"<div class='cards' data-group='{group}' "
                       f"data-varno='{varno}' style='{style} flex-wrap: wrap; "
                       f"gap: 20px; justify-content: center; "
                       f"margin-bottom: 50px;'>"]
                out += [cell for _, cell in
                        sorted(cards[(region, flag, fam, varno)],
                               key=lambda c: str(c[0]))]
                out.append("</div>")
                return out

            group = f"{region}|{flag}|{fam}"

            # observations and profiles per cycle, one card per station
            if TOTAL_VARNO in fam_varnos:
                parts.append("<h4 style='margin-top: 30px; color: #4C72B0;'>"
                             f"Time Series: Nobs and profiles per station "
                             f"({fam})</h4>")
                parts += _cards_div(TOTAL_VARNO, "display: flex;")

            # departures, one card per station and varno
            dep_varnos = [v for v in fam_varnos if v != TOTAL_VARNO]
            if dep_varnos:
                parts.append("<h4 style='margin-top: 30px; color: #4C72B0;'>"
                             f"Departures per station and varno ({fam})</h4>")
                parts.append("<div class='varno-bar'>"
                             "<span class='lab'>Varno</span>")
                for i, v in enumerate(dep_varnos):
                    cls = " class='active'" if i == 0 else ""
                    parts.append(
                        f"<button data-group='{group}' data-varno='{v}'{cls} "
                        f"onclick=\"pickVarno('{group}', '{v}')\">"
                        f"{varno_label(v)}</button>")
                parts.append("</div>")
                for i, v in enumerate(dep_varnos):
                    parts += _cards_div(
                        v, "display: flex;" if i == 0 else "display: none;")
    return "\n".join(parts)
