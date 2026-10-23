"""Annotated SHAP waterfall: how to read the explanation of one forecast.

``yield_outlook`` with ``[ML] do_xai = True`` writes a plain SHAP waterfall per
model, region and forecast season (``ml/xai.py``) and stores the SHAP values in
the ``shap_values`` table of the outlook DB. This module reads one row of that
table, redraws shap's own waterfall for it and puts reading notes around the
plot, for teaching and reports:

* **Start here**: the base value E[f(X)] and what it averages over;
* each bar is a SHAP value (red up, blue down), with the biggest push and pull;
* the inputs, biggest push at the top, with their values in grey;
* inputs that come in several stage windows, summed per input;
* the small inputs shap folds into one "N other features" bar;
* **End here**: the forecast, f(x) = base value + the sum of all the bars.

"Start here" and "End here" are green. Values are shown in the project's
display units (``[ML] yield_units`` / ``yield_display``, read from the DB's own
config table), as in the other yield_outlook figures. Nothing is refitted: the
figure comes from the DB alone, so any outlook DB written with do_xai = True can
be explained after the run. DBs written before 0.4.1089 do not record what the
base value averages over; pass ``--background-note`` to say it.

Usage:
    python -m geocif.viz.shap_explained --db <outlook.db> --model kumo \\
        --region Eastern --year 2026 --out <dir> [--country C] [--crop C]
"""

from __future__ import annotations

import argparse
import ast
import math
import re
import sqlite3
import textwrap
from contextlib import closing
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd

GREEN = "#50a14f"
FONT = 11.5
LINE_GAP = 3.5  # points between the lines of a note
BOX_PAD = 7  # points between a note's text and its frame
FRAME = dict(boxstyle="square", fc="white", ec="black", lw=1.0)
ARROW = dict(arrowstyle="-|>", lw=1.0, color="black", mutation_scale=12, shrinkA=0, shrinkB=2)
# Inches added around shap's figure for the notes.
LEFT, RIGHT, TOP, BOTTOM = 4.3, 4.4, 1.25, 1.75
WRAP = 50  # characters per line of a note's plain text

# "MIN_ESI4WK Jan 1-Jan 31" -> input "MIN_ESI4WK", window "Jan 1-Jan 31".
_STAGE = re.compile(r" ([A-Z][a-z]{2} \d+-[A-Z][a-z]{2} \d+)$")
# Note markup: [[green bold]], **bold**, the rest plain (plain may hold $mathtext$).
_RUN = re.compile(r"\[\[(.+?)\]\]|\*\*(.+?)\*\*|(.+?)(?=\[\[|\*\*|\Z)")


def _connect(db) -> sqlite3.Connection:
    # A plain path, not a read-only file: URI. On a mapped network drive the
    # resolved path is a UNC path, whose host sqlite rejects as a URI authority.
    # Only SELECTs run here, and a missing file is refused rather than created.
    if not Path(db).is_file():
        raise FileNotFoundError(f"no outlook DB at {db}")
    return sqlite3.connect(str(db))


def load_row(db, model, region, year, country=None, crop=None) -> pd.Series:
    """The ``shap_values`` row of one model, region and harvest year."""
    sql = ('SELECT * FROM shap_values WHERE Model = ? AND Region = ? '
           'AND CAST("Harvest Year" AS INTEGER) = ?')
    params = [model, region, int(year)]
    if country:
        sql += " AND Country = ?"
        params.append(country)
    if crop:
        sql += " AND Crop = ?"
        params.append(crop)
    with closing(_connect(db)) as con:
        try:
            df = pd.read_sql_query(sql, con, params=params)
        except pd.errors.DatabaseError as exc:
            raise ValueError(
                f"{db} has no shap_values table: run yield_outlook with [ML] do_xai = True"
            ) from exc
        if df.empty:
            have = pd.read_sql_query(
                'SELECT DISTINCT Model, Region, "Harvest Year" FROM shap_values', con
            )
            raise ValueError(
                f"no SHAP row for model={model!r}, region={region!r}, year={year} in {db}; "
                f"it has models {sorted(have['Model'].unique())} and regions "
                f"{sorted(have['Region'].unique())}"
            )
    if len(df) > 1 and "Forecast Season" in df.columns:
        same = df[df["Forecast Season"].astype(str) == str(int(year))]
        if len(same):
            df = same
    if len(df) > 1:
        keys = df[[c for c in ("Country", "Crop") if c in df.columns]].drop_duplicates()
        raise ValueError(
            f"{len(df)} SHAP rows match; pass --country and --crop "
            f"(choices: {keys.to_dict('records')})"
        )
    return df.iloc[0]


def display_units(db, crop) -> tuple:
    """(unit label, factor from the stored units), as yield_outlook displays them.

    Reads ``[ML] yield_units`` and ``yield_display`` from the newest config
    table that yield_outlook wrote into the DB; Mg/ha and 1.0 without one.
    """
    with closing(_connect(db)) as con:
        tables = [r[0] for r in con.execute(
            "SELECT name FROM sqlite_master WHERE type = 'table' AND name LIKE 'config_%'"
        )]

        def stamp(name):
            try:
                return datetime.strptime(name[len("config_"):], "%B_%d_%Y")
            except ValueError:
                return datetime.min

        opts = {}
        if tables:
            try:
                cfg = pd.read_sql_query(
                    f'SELECT Option, Value FROM "{max(tables, key=stamp)}" WHERE Section = ?',
                    con, params=["ML"],
                )
                opts = dict(zip(cfg["Option"], cfg["Value"]))
            except pd.errors.DatabaseError:
                opts = {}
    clean = lambda v: str(v).split(";")[0].strip()  # noqa: E731  (inline config comments)
    base = clean(opts.get("yield_units", "Mg/ha")) or "Mg/ha"
    try:
        disp = ast.literal_eval(clean(opts.get("yield_display", "{}")) or "{}")
    except (ValueError, SyntaxError):
        disp = {}
    for key in (crop, str(crop).lower()):
        if key in disp:
            return str(disp[key][0]), float(disp[key][1])
    return base, 1.0


def shap_inputs(row) -> list:
    """(name, SHAP value, input value) for every input the row explains."""
    out = []
    for col, val in row.items():
        if not str(col).startswith("SHAP_") or val is None:
            continue
        if isinstance(val, float) and math.isnan(val):
            continue
        name = str(col)[len("SHAP_"):]
        out.append((name, float(val), row.get(f"VALUE_{name}")))
    return out


def window_families(names, values) -> list:
    """Inputs that come in two or more stage windows: (input, [(name, value)]),
    largest summed effect first."""
    fam = {}
    for name, val in zip(names, values):
        m = _STAGE.search(name)
        if m:
            fam.setdefault(name[:m.start()], []).append((name, float(val)))
    out = [(k, v) for k, v in fam.items() if len(v) >= 2]
    return sorted(out, key=lambda kv: -abs(sum(x for _, x in kv[1])))


def background_text(row, model_label, background_note=None) -> str:
    """What the base value averages over, from the row when it says so."""
    if background_note:
        return f"{model_label}'s average forecast over {background_note}."
    n, years = row.get("Background Rows"), row.get("Background Years")
    if n is not None and not (isinstance(n, float) and math.isnan(n)):
        n = int(n)
        if years and str(years) != "all":
            return f"{model_label}'s average forecast over {n} training region-years from {years}."
        return f"{model_label}'s average forecast over its {n} training region-years."
    return f"{model_label}'s average forecast over its SHAP background, a sample of its training data."


def _fmt(v, units=""):
    s = f"{v:.1f}" if abs(v) >= 10 else f"{v:.2f}"
    return f"{s} {units}".strip()


def _line(text):
    from matplotlib.offsetbox import HPacker, TextArea

    runs = []
    for m in _RUN.finditer(text or " "):
        green, bold, plain = m.groups()
        props = dict(fontsize=FONT, color="black")
        if green is not None:
            props.update(fontweight="bold", color=GREEN)
        elif bold is not None:
            props.update(fontweight="bold")
        runs.append(TextArea(green or bold or plain, textprops=props))
    return HPacker(children=runs, align="baseline", pad=0, sep=0)


def _note(ov, x, y, lines, targets=(), side="left", ha="left", va="top"):
    """A framed note at (x, y) inches, one arrow per target leaving from the box
    side named. Returns the box extent (x0, y0, x1, y1) in inches, y up."""
    from matplotlib.offsetbox import AnnotationBbox, VPacker

    body = VPacker(children=[_line(s) for s in lines], align="left", pad=BOX_PAD, sep=LINE_GAP)
    align = ({"left": 0, "center": 0.5, "right": 1}[ha], {"top": 1, "center": 0.5, "bottom": 0}[va])
    box = AnnotationBbox(body, (x, y), xycoords="data", box_alignment=align, frameon=True,
                         pad=0, bboxprops=FRAME, zorder=5)
    ov.add_artist(box)
    fig = ov.figure
    w, h = fig.get_size_inches()

    def extent():
        fig.canvas.draw()
        bb = box.patch.get_window_extent(fig.canvas.get_renderer())
        return bb.x0 / fig.dpi, bb.y0 / fig.dpi, bb.x1 / fig.dpi, bb.y1 / fig.dpi

    x0, y0, x1, y1 = extent()
    # Keep the note on the canvas.
    dx = max(0.1 - x0, 0) - max(x1 - (w - 0.1), 0)
    dy = max(0.1 - y0, 0) - max(y1 - (h - 0.1), 0)
    if dx or dy:
        box.xybox = (x + dx, y + dy)
        x0, y0, x1, y1 = extent()
    m = 0.08
    for tx, ty in targets:
        if side == "left":
            start = (x0, min(max(ty, y0 + m), y1 - m))
        elif side == "right":
            start = (x1, min(max(ty, y0 + m), y1 - m))
        elif side == "top":
            start = (min(max(tx, x0 + m), x1 - m), y1)
        else:
            start = (min(max(tx, x0 + m), x1 - m), y0)
        ov.annotate("", xy=(tx, ty), xytext=start, arrowprops=ARROW, zorder=4)
    return x0, y0, x1, y1


def _wrap(text):
    return textwrap.wrap(text, WRAP, break_on_hyphens=False)


def draw(row, out_path, units="Mg/ha", factor=1.0, max_display=10,
         background_note=None, model_label=None, dpi=250) -> dict:
    """Draw the annotated waterfall for one ``shap_values`` row to ``out_path``.

    Returns the notes' text lines by name (for tests and logs).
    """
    import matplotlib.pyplot as plt
    import shap

    inputs = shap_inputs(row)
    if not inputs:
        raise ValueError("the SHAP row holds no values")
    names = [n for n, _, _ in inputs]
    values = np.array([v for _, v, _ in inputs]) * factor
    data = np.array([d for _, _, d in inputs], dtype=object)
    base = float(row["Base Value"]) * factor
    fx = base + float(values.sum())
    region = str(row["Region"])
    year = int(float(row["Harvest Year"]))
    model = model_label or str(row["Model"])

    plt.figure()
    shap.plots.waterfall(
        shap.Explanation(values=values, base_values=base, data=data, feature_names=names),
        max_display=max_display, show=False,
    )
    plt.title(f"Region: {region}\n{year}")
    fig = plt.gcf()
    ax = fig.axes[0]

    # Grow the canvas without resizing the plot: shap decided while drawing
    # whether each bar's number fits inside the bar, so the axes keep their size.
    # shap's three axes are twins, and setting one twin's position moves all of
    # them, so every new position is computed from the positions read first.
    w0, h0 = fig.get_size_inches()
    h = h0 + TOP + BOTTOM
    before = [(a, a.get_position()) for a in fig.axes]

    def place(left):
        ww = w0 + left + RIGHT
        for a, p in before:
            a.set_position([(p.x0 * w0 + left) / ww, (p.y0 * h0 + BOTTOM) / h,
                            p.width * w0 / ww, p.height * h0 / h])
        fig.set_size_inches(ww, h)
        fig.canvas.draw()
        return ww

    # shap's row labels run past the left edge of its own figure (by how much
    # depends on the names), so measure them and leave LEFT inches beside them.
    w = place(LEFT)
    rend = fig.canvas.get_renderer()
    lab = [t.get_window_extent(rend).x0 / fig.dpi for t in ax.get_yticklabels() if t.get_text()]
    left = LEFT + max(0.0, LEFT - min(lab)) if lab else LEFT
    if left != LEFT:
        w = place(left)
        rend = fig.canvas.get_renderer()

    def inches(disp_xy):
        return disp_xy[0] / fig.dpi, disp_xy[1] / fig.dpi

    def text_box(match):
        for a in fig.axes:
            for t in a.get_xticklabels() + a.get_yticklabels() + a.texts:
                if t.get_visible() and match(t.get_text()):
                    bb = t.get_window_extent(rend)
                    return bb.x0 / fig.dpi, bb.y0 / fig.dpi, bb.x1 / fig.dpi, bb.y1 / fig.dpi
        return None

    # Rows top to bottom, as shap orders them: the biggest |SHAP| first, then
    # one bar for the rest when there are more inputs than max_display.
    order = list(np.argsort(-np.abs(values), kind="stable"))
    if len(order) > max_display:
        shown, rest = order[:max_display - 1], order[max_display - 1:]
    else:
        shown, rest = order, []
    rows = [values[i] for i in shown] + ([values[rest].sum()] if rest else [])
    # shap puts row r (counted from the bottom) at y = r, and lists every tick
    # twice (the grey value labels and the names), so the ticks are not used.
    ticks = [len(rows) - 1 - k for k in range(len(rows))]
    ends, start = [None] * len(rows), base
    for k in range(len(rows) - 1, -1, -1):  # bars stack from the base value up
        ends[k] = (min(start, start + rows[k]), max(start, start + rows[k]))
        start += rows[k]
    def bar_tip(k):
        """Just right of row k's bar, or of its number when shap printed it
        outside the bar, so an arrow never lands on the number."""
        x, y = inches(ax.transData.transform((ends[k][1], ticks[k])))
        for t in ax.texts:
            if abs(t.get_position()[1] - ticks[k]) < 0.25 and t.get_visible():
                x = max(x, t.get_window_extent(rend).x1 / fig.dpi)
        return x + 0.04, y
    row_of = {int(i): k for k, i in enumerate(shown)}

    ov = fig.add_axes([0, 0, 1, 1], zorder=10)
    ov.set_xlim(0, w)
    ov.set_ylim(0, h)
    ov.axis("off")
    ov.patch.set_alpha(0)

    ax_x0, ax_y0 = inches(ax.transAxes.transform((0, 0)))
    ax_x1, ax_y1 = inches(ax.transAxes.transform((1, 1)))
    labels = [t.get_window_extent(rend) for t in ax.get_yticklabels() if t.get_text()]
    lab_x0 = min(b.x0 for b in labels) / fig.dpi if labels else ax_x0 - 2.5
    right_x = left + w0 + 0.15
    notes = {}

    # Start here: the base value, under the x axis.
    ebox = text_box(lambda s: "E[f(X)]" in s)
    ex = (ebox[0] + ebox[2]) / 2 if ebox else inches(ax.transData.transform((base, 0)))[0]
    notes["start"] = [
        f"[[Start here]]: **the base value** $E[f(X)]$ = **{_fmt(base, units)}**",
        *_wrap(background_text(row, model, background_note)
               + " Every region of this run starts here. Read upwards: add each bar"
                 " to reach the forecast."),
    ]
    _note(ov, ex, BOTTOM - 0.2, notes["start"],
          [(ex, (ebox[1] if ebox else ax_y0 - 0.4) - 0.03)], side="top", ha="center")

    # End here: the forecast, above the plot.
    fbox = text_box(lambda s: "f(x)" in s and "E[" not in s)
    fx_x = (fbox[0] + fbox[2]) / 2 if fbox else inches(ax.transData.transform((fx, 0)))[0]
    fx_top = fbox[3] if fbox else ax_y1 + 0.3
    notes["end"] = [
        f"[[End here]]: **the forecast** $f(x)$ = **{_fmt(fx, units)}**",
        f"{model}, {region}, {year}.",
        "$f(x)$ = base value + the sum of all the bars.",
    ]
    _note(ov, min(fx_x + 0.9, w - 0.1), BOTTOM + h0 + 0.2, notes["end"],
          [(fx_x, fx_top + 0.03)], side="bottom", ha="right", va="bottom")

    # Each bar is a SHAP value: arrows to the biggest push and the biggest pull.
    up = max(shown, key=lambda i: values[i])
    down = min(shown, key=lambda i: values[i])
    notes["bars"] = [
        "**Each bar is a SHAP value**:",
        f"how far one input pushed this forecast, in {units}.",
        "**Red** bars push it up, **blue** bars pull it down.",
        "",
        f"Biggest push: {names[up]} **{values[up]:+.2f}**",
    ]
    targets = [bar_tip(row_of[int(up)])]
    if values[down] < 0:
        notes["bars"].append(f"Biggest pull: {names[down]} **{values[down]:+.2f}**")
        targets.append(bar_tip(row_of[int(down)]))
    _, by0, _, _ = _note(ov, right_x, ax_y1 + 0.1, notes["bars"], targets, side="left")

    # Inputs with several stage windows, summed per input.
    fams = window_families(names, values)
    if fams:
        notes["windows"] = ["**Inputs with several stage windows**"] + [
            f"{k}: {len(v)} windows, **{sum(x for _, x in v):+.2f}** together"
            for k, v in fams[:3]
        ]
        top = [names.index(n) for n, _ in sorted(fams[0][1], key=lambda t: -abs(t[1]))]
        targets = [bar_tip(row_of[i]) for i in top if i in row_of][:2]
        _note(ov, right_x, min(by0 - 0.35, (ax_y0 + ax_y1) / 2), notes["windows"],
              targets, side="left")

    # The inputs and their values: a bracket along the labels, the note against it.
    yt = inches(ax.transData.transform((0, ticks[0])))[1] + 0.12
    yb = inches(ax.transData.transform((0, ticks[-1])))[1] - 0.12
    bx = lab_x0 - 0.08
    ov.plot([bx + 0.06, bx, bx, bx + 0.06], [yt, yt, yb, yb], color="black", lw=1.0)
    notes["inputs"] = [
        "**The inputs, biggest push at the top**",
        *_wrap(f"Grey numbers are {region}'s values in {year}."),
    ]
    _, _, nx1, _ = _note(ov, bx - 0.25, (yt + yb) / 2, notes["inputs"],
                         side="right", ha="right", va="center")
    ov.plot([bx, nx1], [(yt + yb) / 2] * 2, color="black", lw=1.0, zorder=4)

    # The small inputs shap folds into one bar.
    if rest:
        notes["others"] = [
            f"**{len(rest)} small inputs, one bar**",
            f"Together they add **{values[rest].sum():+.2f}** {units}.",
        ]
        # Under the labels, pointing up at the "N other features" label.
        obox = text_box(lambda s: s.endswith("other features"))
        ox = (obox[0] + obox[2]) / 2 if obox else lab_x0 + 1.0
        _note(ov, lab_x0, yb - 0.3, notes["others"],
              [(ox, (obox[1] if obox else yb) - 0.03)], side="top")

    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=dpi, facecolor="white")
    plt.close(fig)
    return notes


def run(db, model, region, year, out_dir, country=None, crop=None, units=None,
        max_display=10, background_note=None, dpi=250) -> Path:
    """Explain one forecast of an outlook DB; returns the PNG path."""
    from geocif.utils import display_model_name

    row = load_row(db, model, region, year, country=country, crop=crop)
    label, factor = (units, 1.0) if units else display_units(db, row.get("Crop", crop))
    safe = lambda s: re.sub(r"[^\w.-]+", "_", str(s))  # noqa: E731
    out = Path(out_dir) / (
        f"shap_explained_{safe(row.get('Country', ''))}_{safe(row.get('Crop', ''))}_"
        f"{safe(model)}_{safe(region)}_{int(year)}.png"
    )
    draw(row, out, units=label, factor=factor, max_display=max_display,
         background_note=background_note, model_label=display_model_name(model), dpi=dpi)
    return out


def main(argv=None):
    import matplotlib

    matplotlib.use("Agg")
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--db", required=True, help="outlook DB written with [ML] do_xai = True")
    ap.add_argument("--model", required=True, help="Model column value, e.g. kumo")
    ap.add_argument("--region", required=True)
    ap.add_argument("--year", required=True, type=int, help="harvest year")
    ap.add_argument("--out", required=True, help="output directory")
    ap.add_argument("--country")
    ap.add_argument("--crop")
    ap.add_argument("--units", help="unit label; default: [ML] yield_units / yield_display from the DB")
    ap.add_argument("--max-display", type=int, default=10, help="bars shown (shap's max_display)")
    ap.add_argument("--background-note",
                    help='what the base value averages over, for DBs older than 0.4.1089, '
                         'e.g. "10 training region-years from 2017-2021"')
    ap.add_argument("--dpi", type=int, default=250)
    a = ap.parse_args(argv)
    out = run(a.db, a.model, a.region, a.year, a.out, country=a.country, crop=a.crop,
              units=a.units, max_display=a.max_display, background_note=a.background_note,
              dpi=a.dpi)
    print(out)


if __name__ == "__main__":
    main()
