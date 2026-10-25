# -*- coding: utf-8 -*-
"""Snake chart: how a forecast and its indicators moved from issue to issue.

The layout is the NYT "How support for Trump has changed" chart: one row per
series, every row on one shared horizontal axis, a light thick path tracing
the history and a dot at every issue, coloured by issue month (viridis by
default: yellow for the first issue to purple for the latest), the same month
the same colour in every row.
A row switches lanes when its trajectory reverses, so the way back never
overlaps the way out; the lanes join with a U-turn cap at the turning point.

The module is a pure function of one tidy long table (``TRACK_COLUMNS``) and
knows nothing about outlook DBs, CIDs or configs: the data layer
(``geocif.viz.snake_data``) builds the table and the runner
(``geocif.viz.snake_run``) saves the files. Its only geocif import is
``geocif.viz._style`` (stdlib-only at import), which the house style and the
drift guards in ``tests/test_viz_style.py`` require.

Geometry, in short:

* every row owns a band of height 1 (data units, y grows downward); lanes sit
  at fixed offsets inside it, ``LANE_GAP`` of the band apart;
* a lane run is one :class:`matplotlib.path.Path`; consecutive runs on
  different lanes are joined by a cubic Bézier cap whose bulge is computed in
  DATA units from the lane gap in PIXELS (:func:`cap_bulge`), so the cap
  renders as a true semicircle whatever the axis scales. Set the figure size
  and the x limits before drawing any path; :func:`plot_snake` does;
* ``layout="runs"`` (default) splits each row into monotonic runs
  (:func:`split_runs`; a step smaller than ``deadband`` does not start a run)
  and gives each run its own lane (:func:`assign_lanes`, at most ``max_lanes``;
  beyond that the neighbouring runs whose overlap hides the least share a
  lane, need no cap, and every dot of that row is labelled); ``layout="split"`` reproduces the NYT layout
  literally: issues up to the ``split`` index on the upper lane, the rest on
  the lower one, joined by a U-turn cap when the direction reverses and an
  S-bend otherwise (:func:`connector_kind`).

``value_std`` is already signed so that right means more favorable: the data
layer flips rows where higher hurts the crop and sets ``invert`` so the label
can say "(inverted)". The plotter never flips a value.
"""
import math
import textwrap
from datetime import date, datetime

import numpy as np
import pandas as pd

from geocif.viz._style import despine, style_ctx

#: Required columns of the tidy long table (one row per series and issue).
TRACK_COLUMNS = ("row", "role", "issue_date", "value_std", "value_raw",
                 "unit", "invert", "obs_date")
#: Optional columns: ``display`` (right-hand column text), ``order`` (row
#: order), ``issue_label`` (text next to a dot), ``obs_date_kind``,
#: ``source``, ``window``.
ROLES = ("target", "input", "independent")
ROLE_TEXT = {"target": "Model forecast", "input": "Model input",
             "independent": "Independent"}
LAYOUTS = ("runs", "split")
LABEL_ROWS = ("first", "all", "none")
FONT_STACK = ("Helvetica Neue", "Helvetica", "Arial", "DejaVu Sans")

#: One hue: the path is light; the dots run from DOT_LIGHT (first issue) to
#: DOT_DARK (latest issue).
PATH = "#d3dbee"
DOT = "#8d9bc6"
DOT_LIGHT = "#b4bfe2"
DOT_DARK = "#2e3a74"
ZERO = "#1a1a1a"
GRID = "#e4e4e4"
SEPARATOR = "#cfcfcf"
BAND = "#f2f2f2"
TEXT = "#1a1a1a"
MUTED = "#7a7a7a"
#: Lane spacing as a fraction of the row height.
LANE_GAP = 0.35
#: Bézier circle constant (control distance for a quarter arc of radius 1).
KAPPA = 0.5523
#: Stroke width and marker size in points.
PATH_LW = 9.0
DOT_SIZE = 8.0
#: Text sizes in points.
TITLE_PT, SUBTITLE_PT, SOURCE_PT = 13.5, 10.0, 8.0
LABEL_PT, ROLE_PT, TICK_PT, ISSUE_PT = 10.5, 8.5, 9.5, 9.0
#: Row labels wrap at this many characters (the gutter is 27% of the width).
LABEL_WRAP = 22
#: Figure proportions in inches.
ROW_IN = 0.9
HEADER_BASE_IN = 0.6
#: Header height when there are no column headers, only the tick labels.
HEADER_TICKS_IN = 0.32
FOOTER_BASE_IN = 0.2
#: Room for the issue-month key under the axes.
KEY_IN = 0.35
#: Gap between a dot and its issue label, in points.
LABEL_GAP_PT = 6.5
#: Inches per wrapped line of title, subtitle and source text.
TITLE_LINE_IN, SUBTITLE_LINE_IN, SOURCE_LINE_IN = 0.27, 0.19, 0.15
#: Left margin of the figure for all free text.
MARGIN_X = 0.015
#: Deadband comparisons tolerate this much floating-point noise.
EPS = 1e-9

UNICODE_MINUS = "−"

_FONT_FAMILY = None


# ---------------------------------------------------------------------------
# table validation
# ---------------------------------------------------------------------------
def _is_missing(v):
    if v is None:
        return True
    if isinstance(v, str):
        return not v.strip()
    try:
        return bool(pd.isna(v))
    except (TypeError, ValueError):
        return False


def _to_date(v):
    if _is_missing(v):
        raise ValueError(f"missing date {v!r}")
    if isinstance(v, datetime):
        return v.date()
    if isinstance(v, date):
        return v
    ts = pd.Timestamp(v)
    if pd.isna(ts):
        raise ValueError(f"unparseable date {v!r}")
    return ts.date()


def validate_tracks(tracks, *, max_rows=5, require_target=True):
    """Check the tidy table and return a cleaned copy.

    Raises ``ValueError`` on a missing column, an unknown role, a non-bool
    ``invert``, more than ``max_rows`` distinct rows (one target plus up to
    four indicators), zero or several target rows when ``require_target``,
    or any observation dated after its issue date (the causality guard: a
    value the model could not have seen must not be drawn as if it had).
    A missing ``obs_date`` (None, NaN, NaT) is allowed and skips the guard.
    Points whose ``value_std`` is not finite are dropped (they are gaps).
    The caller's frame is never modified.
    """
    df = pd.DataFrame(tracks).copy()
    missing = [c for c in TRACK_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"tracks is missing columns {missing}")
    if df.empty:
        raise ValueError("tracks is empty")
    bad_roles = sorted(set(df["role"].astype(str)) - set(ROLES))
    if bad_roles:
        raise ValueError(f"unknown role(s) {bad_roles}; expected one of {ROLES}")
    if not all(isinstance(v, (bool, np.bool_)) for v in df["invert"]):
        raise ValueError("invert must be boolean for every row")
    df["issue_date"] = [_to_date(v) for v in df["issue_date"]]
    df["obs_date"] = [None if _is_missing(v) else _to_date(v) for v in df["obs_date"]]
    df["obs_date"] = df["obs_date"].astype(object)
    late = [(r.row, r.obs_date, r.issue_date) for r in df.itertuples()
            if r.obs_date is not None and r.obs_date > r.issue_date]
    if late:
        row, obs, iss = late[0]
        raise ValueError(
            f"causality guard: {len(late)} point(s) observed after their issue "
            f"date, e.g. row {row!r} obs_date {obs} > issue_date {iss}")
    rows = list(dict.fromkeys(df["row"]))
    if len(rows) > max_rows:
        raise ValueError(f"{len(rows)} rows requested; at most {max_rows} "
                         f"(one target plus {max_rows - 1} indicators)")
    role_by_row = {}
    for row, g in df.groupby("row", sort=False):
        roles = set(g["role"])
        if len(roles) > 1:
            raise ValueError(f"row {row!r} carries several roles {sorted(roles)}")
        role_by_row[row] = roles.pop()
    targets = [r for r, role in role_by_row.items() if role == "target"]
    if require_target and len(targets) != 1:
        raise ValueError(f"expected exactly one target row, found {targets}")
    df["value_std"] = pd.to_numeric(df["value_std"], errors="coerce")
    df = df[np.isfinite(df["value_std"])]
    if df.empty:
        raise ValueError("no finite value_std in tracks")
    dup = df.duplicated(["row", "issue_date"])
    if dup.any():
        raise ValueError(f"duplicate (row, issue_date) pairs: "
                         f"{df.loc[dup, ['row', 'issue_date']].values.tolist()[:3]}")
    return df.reset_index(drop=True)


def row_order(tracks):
    """Display order: ``order`` column if present, else target first, then
    first appearance."""
    if "order" in tracks.columns:
        return list(tracks.groupby("row", sort=False)["order"].min()
                    .sort_values(kind="stable").index)
    rows = list(dict.fromkeys(tracks["row"]))
    targets = [r for r in rows if (tracks.loc[tracks["row"] == r, "role"] == "target").all()]
    return targets + [r for r in rows if r not in targets]


# ---------------------------------------------------------------------------
# geometry
# ---------------------------------------------------------------------------
def step_direction(a, b, deadband):
    """+1 right, -1 left, 0 for no change or a change smaller than
    ``deadband`` (a step of exactly ``deadband`` counts as a step)."""
    d = float(b) - float(a)
    if d == 0.0 or abs(d) < deadband - EPS:
        return 0
    return 1 if d > 0 else -1


def split_runs(values, deadband=0.1):
    """Split a sequence into monotonic runs.

    Returns ``(runs, dirs)``: ``runs`` is a list of index lists, consecutive
    runs sharing their turning point (the last index of one run is the first
    of the next); ``dirs`` holds each run's direction (+1 right, -1 left, 0
    when the run never moved beyond the deadband). A step smaller than
    ``deadband`` keeps the current run and its direction.
    """
    values = [float(v) for v in values]
    n = len(values)
    if n == 0:
        return [], []
    runs, dirs = [[0]], [0]
    for i in range(1, n):
        s = step_direction(values[i - 1], values[i], deadband)
        if s != 0 and dirs[-1] != 0 and s != dirs[-1]:
            runs.append([i - 1, i])
            dirs.append(s)
            continue
        runs[-1].append(i)
        if s != 0 and dirs[-1] == 0:
            dirs[-1] = s
    return runs, dirs


def assign_lanes(runs, max_lanes=3, values=None):
    """Lane index per run. With more runs than lanes, neighbouring runs share
    a lane, where the later one retraces the earlier and hides the shorter of
    the two; the pair hiding the least (by x extent of ``values``) is merged
    first, ties to the earliest, so a big reversal keeps its own U-turn.
    Without ``values`` every run counts as flat and the earliest runs share
    lane 0. Returns ``(lanes, merged)``."""
    n = len(runs)
    if n <= max_lanes:
        return list(range(n)), False
    span = [0.0] * n
    if values is not None:
        span = [max(values[i] for i in run) - min(values[i] for i in run) for run in runs]
    groups = [[r] for r in range(n)]
    while len(groups) > max_lanes:
        g = min(range(len(groups) - 1),
                key=lambda k: min(span[groups[k][-1]], span[groups[k + 1][0]]))
        groups[g:g + 2] = [groups[g] + groups[g + 1]]
    lanes = [0] * n
    for lane, group in enumerate(groups):
        for r in group:
            lanes[r] = lane
    return lanes, True


def connector_kind(prev_dir, next_dir):
    """``"uturn"`` when the direction reverses at the junction, ``"sbend"``
    when the next lane continues the same way (or either side is flat)."""
    if prev_dir != 0 and next_dir != 0 and prev_dir != next_dir:
        return "uturn"
    return "sbend"


def lane_y(center, lane, n_lanes, gap=LANE_GAP):
    """y of ``lane`` (0 = upper) among ``n_lanes`` centred on ``center``;
    y grows downward."""
    return center + (lane - (n_lanes - 1) / 2.0) * gap


def px_per_unit(ax):
    """``(px_per_x, px_per_y)`` of the axes' data transform (y as a positive
    magnitude; the snake's y axis runs downward)."""
    tr = ax.transData
    o = tr.transform((0.0, 0.0))
    px_x = tr.transform((1.0, 0.0))[0] - o[0]
    px_y = abs(tr.transform((0.0, 1.0))[1] - o[1])
    return px_x, px_y


def cap_bulge(ax, lane_gap_data):
    """Horizontal half-width of a U-turn cap, in x data units, that renders
    as a semicircle: half the lane gap measured in pixels, divided by the
    pixels per x unit. Call after the figure size, margins and limits are set.
    """
    px_x, px_y = px_per_unit(ax)
    return (lane_gap_data * px_y / 2.0) / px_x


def pt_to_x(ax, points):
    """Length in x data units of ``points`` typographic points."""
    px_x, _ = px_per_unit(ax)
    return points * ax.figure.dpi / 72.0 / px_x


def cap_path(x, y0, y1, bulge):
    """Vertices and codes of a semicircular cap from ``(x, y0)`` to
    ``(x, y1)`` bulging ``bulge`` x-units sideways (signed), as two cubic
    Bézier quarter arcs. The first vertex is a MOVETO."""
    from matplotlib.path import Path

    dy = (y1 - y0) / 2.0
    ym = y0 + dy
    k = KAPPA
    verts = [
        (x, y0),
        (x + k * bulge, y0), (x + bulge, ym - k * dy), (x + bulge, ym),
        (x + bulge, ym + k * dy), (x + k * bulge, y1), (x, y1),
    ]
    codes = [Path.MOVETO] + [Path.CURVE4] * 6
    return verts, codes


def sbend_path(x0, y0, x1, y1):
    """Vertices and codes of a smooth S-bend from ``(x0, y0)`` to ``(x1, y1)``."""
    from matplotlib.path import Path

    xm = x0 + (x1 - x0) / 2.0
    verts = [(x0, y0), (xm, y0), (xm, y1), (x1, y1)]
    codes = [Path.MOVETO, Path.CURVE4, Path.CURVE4, Path.CURVE4]
    return verts, codes


def _last_step_direction(values, run):
    """Direction of travel INTO the end of ``run``: its last non-flat step."""
    for j in range(len(run) - 1, 0, -1):
        s = step_direction(values[run[j - 1]], values[run[j]], 0.0)
        if s:
            return s
    return 0


def layout_row(values, steps, *, layout="runs", split=None, deadband=0.1,
               max_lanes=3):
    """Lane plan of one row.

    ``values`` are the row's x values in step order and ``steps`` their step
    indices (positions in the figure-wide list of issues), so a skipped issue
    shows as a jump in ``steps``. In ``split`` mode ``split`` is a step index
    (the last issue drawn on the upper lane), so every row turns at the same
    issue even when it misses an early one.

    Returns a dict with ``runs`` (index lists into ``values``), ``dirs``,
    ``turn_dirs`` (direction of travel into each run's last point, which
    decides the side a cap bulges to), ``lanes`` (lane per run),
    ``n_lanes``, ``merged`` (some runs share a lane), ``connectors``
    (``"uturn"`` / ``"sbend"`` / ``"same"`` between consecutive runs) and
    ``point_lane`` (lane of every point, the turning point on the lane it
    was reached on).
    """
    if layout not in LAYOUTS:
        raise ValueError(f"layout must be one of {LAYOUTS}, got {layout!r}")
    values = [float(v) for v in values]
    steps = list(steps)
    n = len(values)
    if layout == "runs":
        runs, dirs = split_runs(values, deadband)
        lanes, merged = assign_lanes(runs, max_lanes, values)
    else:
        if split is None:
            raise ValueError("layout='split' needs split=<step index of the last upper-lane issue>")
        k = sum(1 for s in steps if s <= split) - 1        # per-row position of the turn
        if not 0 <= k < n - 1:
            runs, lanes, merged = [list(range(n))], [0], False
            dirs = [_last_step_direction(values, runs[0])]
        else:
            runs = [list(range(k + 1)), list(range(k, n))]
            dirs = [_last_step_direction(values, runs[0]),
                    step_direction(values[k], values[-1], 0.0)]
            lanes, merged = [0, 1], False
    # The direction of travel INTO each run's last point decides whether the
    # junction is a reversal (raw, 0 when the run was flat) and which side a
    # cap bulges to (turn_dirs, falling back to the opposite of the next run
    # so a flat run still gets a sensible cap when one is drawn).
    # In "runs" layout a run's direction is deadband-aware, and a dip smaller
    # than the deadband at its end is not a turn; in "split" layout the upper
    # lane need not be monotonic, so the last real step into the turn counts.
    raw_dirs = [_last_step_direction(values, run) for run in runs]
    if layout == "runs":
        raw_dirs = [d if d else raw for d, raw in zip(dirs, raw_dirs)]
    turn_dirs = []
    for r, d in enumerate(raw_dirs):
        if d == 0 and r + 1 < len(runs) and dirs[r + 1]:
            d = -dirs[r + 1]
        turn_dirs.append(d or dirs[r])
    connectors = []
    for r in range(len(runs) - 1):
        if lanes[r] == lanes[r + 1]:
            connectors.append("same")
        else:
            nxt = runs[r + 1]
            next_dir = (step_direction(values[nxt[0]], values[nxt[1]], 0.0)
                        if len(nxt) > 1 else 0) or dirs[r + 1]
            connectors.append(connector_kind(raw_dirs[r], next_dir))
    n_lanes = max(lanes) + 1 if lanes else 1
    point_lane = [None] * n
    for run, lane in zip(runs, lanes):
        for idx in run:
            if point_lane[idx] is None:
                point_lane[idx] = lane
    return {"runs": runs, "dirs": dirs, "turn_dirs": turn_dirs, "lanes": lanes,
            "n_lanes": n_lanes, "merged": merged, "connectors": connectors,
            "point_lane": point_lane, "steps": steps}


# ---------------------------------------------------------------------------
# text helpers
# ---------------------------------------------------------------------------
def sigma_formatter(v, pos=None):
    """``−2σ``, ``−1σ``, ``0``, ``+1σ``, ``+2σ`` with a Unicode minus."""
    if abs(v) < 1e-9:
        return "0"
    return f"{v:+g}σ".replace("-", UNICODE_MINUS)


def fmt_signed(v, digits=2):
    """Signed number with a Unicode minus; a value that rounds to zero prints
    as +0.00, never as a negative zero."""
    v = round(float(v), digits) + 0.0
    return f"{v:+.{digits}f}".replace("-", UNICODE_MINUS)


def fmt_number(v, digits=2):
    return f"{v:,.{digits}f}".replace("-", UNICODE_MINUS)


#: Named dot palettes, each ordered first issue -> latest issue. A tuple of
#: two hex colours is a linear ramp; ``(cmap, start, stop)`` samples a
#: matplotlib colormap; ``("accent", past_light, past_dark, latest)`` greys
#: the past issues and gives the latest one its own colour.
PALETTES = {
    "blues": (DOT_LIGHT, DOT_DARK),
    "viridis": ("viridis", 0.90, 0.10),
    "magma": ("magma", 0.85, 0.15),
    "oranges": ("YlOrBr", 0.30, 0.90),
    "teal": ("#b2dfdb", "#00544b"),
    "accent": ("accent", "#d4d4d4", "#7a7a7a", "#d95f02"),
}
#: Default dot palette: every month distinct, monotonic in lightness and
#: readable with colour-vision deficiency.
DEFAULT_PALETTE = "viridis"


def issue_colors(n, palette=DEFAULT_PALETTE):
    """``n`` colours, first issue to latest, from a named palette
    (``PALETTES``), a matplotlib colormap name or an explicit list."""
    from matplotlib import colormaps
    from matplotlib.colors import to_hex, to_rgb

    if n <= 0:
        return []
    if isinstance(palette, (list, tuple)) and palette and palette[0] != "accent" \
            and len(palette) == n and all(isinstance(c, str) for c in palette):
        return [to_hex(c) for c in palette]
    spec = PALETTES.get(palette, palette) if isinstance(palette, str) else palette
    if isinstance(spec, str):                       # a bare colormap name
        spec = (spec, 0.2, 0.9)

    def ramp(a, b, m):
        a, b = np.array(to_rgb(a)), np.array(to_rgb(b))
        if m <= 1:
            return [to_hex(b)] * m
        return [to_hex(a + (b - a) * k / (m - 1)) for k in range(m)]

    if spec[0] == "accent":
        _, light, dark, latest = spec
        return ramp(light, dark, n - 1) + [to_hex(latest)]
    if len(spec) == 2:
        return ramp(spec[0], spec[1], n)
    name, start, stop = spec
    cmap = colormaps[name]
    pos = [stop] if n == 1 else np.linspace(start, stop, n)
    return [to_hex(cmap(float(t))) for t in pos]


def default_display(group, change=False):
    """Right-hand column text: the latest raw value, ``514.6 mm``; with
    ``change=True`` also, in brackets, how its gap to normal moved since the
    previous issue, ``514.6 mm (−69.5)``.

    The gap uses ``normal_raw`` (the baseline in the row's own units) when the
    table carries it, so the change has the sign of the dot's move (before an
    inversion); without it the bracket is the plain change of the raw value.
    """
    g = group.sort_values("issue_date")
    raw = pd.to_numeric(g["value_raw"], errors="coerce").values
    unit = str(g["unit"].iloc[-1]) if "unit" in g and isinstance(g["unit"].iloc[-1], str) else ""
    if len(raw) == 0 or not np.isfinite(raw[-1]):
        return ""
    last = raw[-1]
    digits = 2 if abs(last) < 100 else 1 if abs(last) < 1000 else 0
    text = f"{fmt_number(last, digits)} {unit}".strip()
    if change and len(raw) > 1 and np.isfinite(raw[-2]):
        if "normal_raw" in g.columns:
            normal = pd.to_numeric(g["normal_raw"], errors="coerce").values
            if np.isfinite(normal[-1]) and np.isfinite(normal[-2]):
                change = (last - normal[-1]) - (raw[-2] - normal[-2])
                return f"{text} ({fmt_signed(change, digits)})"
        text += f" ({fmt_signed(last - raw[-2], digits)})"
    return text


def issue_label(d, span_years):
    """``Jun`` within one year, ``Jun 2026`` when the issues span years."""
    return d.strftime("%b %Y") if span_years else d.strftime("%b")


def suggest_title(tracks):
    """Draft headline from the latest step: direction of the target row and
    how many indicator rows moved the same way. The analyst edits it."""
    df = validate_tracks(tracks, require_target=False)
    order = row_order(df)
    moves = {}
    for row in order:
        g = df[df["row"] == row].sort_values("issue_date")
        if len(g) >= 2:
            moves[row] = float(g["value_std"].iloc[-1] - g["value_std"].iloc[-2])
    if not moves:
        return "Forecast and indicators by issue month"
    target = next((r for r in order if (df.loc[df["row"] == r, "role"] == "target").all()), order[0])
    if target not in moves:
        return "Forecast and indicators by issue month"
    tm = moves[target]
    month = df["issue_date"].max().strftime("%B")
    verb = "held steady" if abs(tm) < 0.1 else ("improved" if tm > 0 else "weakened")
    others = {r: m for r, m in moves.items() if r != target}
    if not others or abs(tm) < 0.1:
        return f"{target} {verb} in the {month} issue"
    same = [r for r, m in others.items() if m * tm > 0 and abs(m) >= 0.1]
    return (f"{target} {verb} in the {month} issue; "
            f"{len(same)} of {len(others)} indicators moved the same way")


def source_line(meta):
    """Provenance line from metadata.

    ``meta`` keys (all optional): ``issues`` (dates), ``sources`` (names),
    ``baseline`` (``(first, last)`` years), ``target_year``, ``notes`` (list
    of short sentences, e.g. a missing issue or the re-forecast caveat).
    Ends with the reading rule "Right = more favorable for yield."
    """
    parts = []
    issues = meta.get("issues") or []
    if issues:
        ds = sorted(_to_date(d) for d in issues)
        span_years = ds[0].year != ds[-1].year
        first = ds[0].strftime("%b %Y") if span_years else ds[0].strftime("%b")
        last = ds[-1].strftime("%b %Y")
        parts.append(f"Issues {first} to {last}" if len(ds) > 1 else f"Issue {last}")
    if meta.get("sources"):
        parts.append("Sources: " + ", ".join(str(s) for s in meta["sources"]))
    if meta.get("baseline"):
        b0, b1 = meta["baseline"]
        tail = f", {meta['target_year']} excluded" if meta.get("target_year") else ""
        parts.append(f"Baseline {b0}-{b1}{tail}")
    for note in meta.get("notes") or []:
        parts.append(str(note).rstrip("."))
    parts.append("Right = more favorable for yield")
    return ". ".join(parts) + "."


def wrap_to_width(text, width_in, fontsize, factor=0.52):
    """Wrap ``text`` so each line fits ``width_in`` inches at ``fontsize``
    (average glyph width taken as ``factor`` em). Returns the lines."""
    if not text:
        return []
    chars = max(20, int(width_in * 72.0 / (fontsize * factor)))
    lines = []
    for para in str(text).splitlines() or [""]:
        lines.extend(textwrap.wrap(para, chars) or [""])
    return lines


# ---------------------------------------------------------------------------
# fonts
# ---------------------------------------------------------------------------
def resolve_font_family(stack=FONT_STACK):
    """First family of ``stack`` that matplotlib can find, probed once."""
    global _FONT_FAMILY
    if _FONT_FAMILY is None:
        from matplotlib import font_manager

        names = {f.name for f in font_manager.fontManager.ttflist}
        _FONT_FAMILY = next((f for f in stack if f in names), "sans-serif")
    return _FONT_FAMILY


def font_stack():
    """The resolved family first, then the other installed families of
    ``FONT_STACK`` (listing a missing family makes matplotlib warn on every
    text it draws)."""
    from matplotlib import font_manager

    fam = resolve_font_family()
    names = {f.name for f in font_manager.fontManager.ttflist}
    return [fam] + [f for f in FONT_STACK if f != fam and f in names]


def font_ctx():
    """``rc_context`` whose ``font.family`` IS the concrete stack, so every
    Text created inside stores the family names and renders the same at
    save time, outside the context; nothing leaks into the global rcParams."""
    import matplotlib

    return matplotlib.rc_context({"font.family": font_stack(),
                                  "axes.unicode_minus": True})


# ---------------------------------------------------------------------------
# the figure
# ---------------------------------------------------------------------------
def header_inches(title_lines=0, subtitle_lines=0, headers=True):
    h = HEADER_BASE_IN if headers else HEADER_TICKS_IN
    if title_lines:
        h += 0.08 + title_lines * TITLE_LINE_IN
    if subtitle_lines:
        h += 0.1 + subtitle_lines * SUBTITLE_LINE_IN
    return h


def footer_inches(source_lines=0, key=True):
    return (FOOTER_BASE_IN + (KEY_IN if key else 0)
            + (0.1 + source_lines * SOURCE_LINE_IN if source_lines else 0))


def _wrapped(title, subtitle, source, width_in):
    usable = width_in * (1 - 2 * MARGIN_X)
    return (wrap_to_width(title, usable, TITLE_PT, 0.56),
            wrap_to_width(subtitle, usable, SUBTITLE_PT),
            wrap_to_width(source, usable, SOURCE_PT))


def figure_size(n_rows, width_in=7.0, *, title=None, subtitle=None, source=None, key=True,
                headers=True):
    """``(width, height)`` in inches: a header sized for the wrapped title and
    subtitle, one band per row, a footer for the issue-month key and the
    wrapped source line."""
    t, s, src = _wrapped(title, subtitle, source, width_in)
    return width_in, (header_inches(len(t), len(s), headers) + n_rows * ROW_IN
                      + footer_inches(len(src), key))


def symmetric_xmax(values, floor=2.0, step=0.5):
    """Max |x| rounded UP to ``step``, at least ``floor``."""
    m = float(np.nanmax(np.abs(values))) if len(values) else 0.0
    return max(floor, math.ceil(m / step - 1e-9) * step)


def _place_issue_labels(ax, xs, ys, labels, *, runs, first_row, last_dir):
    """Label the dots of one row without overlaps.

    The latest point is labelled first, beyond its arrowhead when the lane is
    clear in that direction, else above or below; the other points go above
    the upper lane and below the others, then the opposite side. A label that
    would overlap a dot, a lane path, another label or (on the first row) the
    tick labels is dropped: the companion CSV carries every issue.
    """
    fig = ax.figure
    renderer = fig.canvas.get_renderer()
    pt = fig.dpi / 72.0
    disp = ax.transData.transform
    r_dot = DOT_SIZE / 2.0 * pt + 1
    half_lw = PATH_LW / 2.0 * pt
    obstacles = []
    for x, y in zip(xs, ys):
        cx, cy = disp((x, y))
        obstacles.append((cx - r_dot, cy - r_dot, cx + r_dot, cy + r_dot))
    for x0, x1, y in runs:
        a, b = disp((x0, y)), disp((x1, y))
        obstacles.append((min(a[0], b[0]) - half_lw, a[1] - half_lw,
                          max(a[0], b[0]) + half_lw, a[1] + half_lw))
    top = ax.get_window_extent(renderer).y1 - 2

    def hits(bb):
        if first_row and bb.y1 > top:
            return True
        return any(bb.x0 < o[2] and bb.x1 > o[0] and bb.y0 < o[3] and bb.y1 > o[1]
                   for o in obstacles)

    upper = min(ys) if len(ys) else 0
    n = len(xs)
    order = ([n - 1] if n else []) + list(range(n - 1))
    for idx in order:
        lab = labels[idx]
        if not isinstance(lab, str) or not lab:
            continue
        x, y = xs[idx], ys[idx]
        vert = [((0, LABEL_GAP_PT), "center", "bottom"),
                ((0, -LABEL_GAP_PT), "center", "top")]
        if abs(y - upper) > 1e-9:
            vert.reverse()
        cands = list(vert)
        if idx == n - 1 and n >= 2:
            side = (((LABEL_GAP_PT + 3, 0), "left", "center") if last_dir > 0
                    else ((-LABEL_GAP_PT - 3, 0), "right", "center"))
            cands = [side] + cands
        for off, ha, va in cands:
            t = ax.annotate(lab, (x, y), xytext=off, textcoords="offset points",
                            ha=ha, va=va, fontsize=ISSUE_PT, color=TEXT, zorder=6)
            bb = t.get_window_extent(renderer)
            if hits(bb):
                t.remove()
                continue
            obstacles.append((bb.x0 - 2, bb.y0 - 1, bb.x1 + 2, bb.y1 + 1))
            break


def plot_snake(tracks, *, layout="runs", split=None, deadband=0.1, max_lanes=3,
               title=None, subtitle=None, source=None, ax=None, highlight=None,
               show_roles=False, show_values=True, show_key=True, palette=DEFAULT_PALETTE,
               tick_formatter=None, show_change=False,
               xlabel=None, gutter_label=None, values_label=None, xmax=None, xlim=None,
               xtick_step=1.0, width_in=7.0, require_target=True, label_rows="none"):
    """Draw the snake chart and return ``(fig, ax)``.

    Parameters
    ----------
    tracks : DataFrame
        The tidy long table, see ``TRACK_COLUMNS``.
    layout, split, deadband, max_lanes
        Lane layout, see the module docstring. ``split`` is a step index
        into the sorted list of issues. A reversal smaller than ``deadband``
        (0.1 sigma) stays on its lane without a curve; the dot colours keep the
        order readable. ``deadband=0`` gives every reversal its own lane.
    title, subtitle, source
        Headline (the analyst's; :func:`suggest_title` drafts one), deck and
        provenance line (:func:`source_line` builds one from metadata). All
        three are wrapped to the figure width and the header and footer grow
        with the number of lines.
    ax : Axes or None
        Draw into an existing axes (its figure size and margins must already
        be set) or create a figure sized by :func:`figure_size`.
    highlight : str or None
        Row whose band is shaded; the target row by default.
    show_roles : bool
        Gray role subtitle under each row label (off by default; the role is
        in the companion table).
    show_values : bool
        Right-hand column with the latest raw value and the change of its gap
        to normal since the previous issue (``display`` column, else
        :func:`default_display`).
    show_change : bool
        Add the change of the gap to normal since the previous issue, in
        brackets, to the right-hand column (off by default).
    xlabel, gutter_label, values_label : str or None
        Column headers over the axis, the row labels and the value column;
        none by default (the tick labels read in sigma on their own).
    show_key : bool
        Issue-month colour key under the axes.
    palette : str or list
        Dot colours, first issue to latest: a name in ``PALETTES``, a
        matplotlib colormap name, or a list with one colour per issue.
    tick_formatter : callable or None
        ``f(value, pos) -> str`` for the top tick labels; sigma labels by
        default. Also formats the annotation of a clipped value.
    xmax : float or None
        Fixed half-width of a symmetric axis; values beyond it are clipped at
        the edge with a wedge marker and annotated with the true value.
        ``None`` picks the max |value| plus room for a U-turn cap and the
        stroke end, rounded up to 0.5, at least 2.
    xlim : (float, float) or None
        Explicit, possibly asymmetric limits (the NYT fixture runs from -65
        to +15); overrides ``xmax``. Clipping applies the same way.
    label_rows : {"none", "first", "all"}
        Issue labels next to the dots: nowhere (default; the colour key under
        the axes names the months), on the first row only (NYT direct
        labelling), or on every row. When labels are on, a row that merged
        lanes labels all its dots.
    """
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D
    from matplotlib.patches import PathPatch
    from matplotlib.path import Path
    from matplotlib.ticker import FixedLocator, FuncFormatter
    from matplotlib.transforms import blended_transform_factory

    if label_rows not in LABEL_ROWS:
        raise ValueError(f"label_rows must be one of {LABEL_ROWS}, got {label_rows!r}")
    if layout not in LAYOUTS:
        raise ValueError(f"layout must be one of {LAYOUTS}, got {layout!r}")
    df = validate_tracks(tracks, require_target=require_target)
    rows = row_order(df)
    n_rows = len(rows)
    issues = sorted(set(df["issue_date"]))
    step_of = {d: i for i, d in enumerate(issues)}
    span_years = issues[0].year != issues[-1].year
    if highlight is None:
        tg = [r for r in rows if (df.loc[df["row"] == r, "role"] == "target").all()]
        highlight = tg[0] if tg else None

    auto_x = xlim is None and xmax is None
    if xlim is not None:
        lo, hi = float(xlim[0]), float(xlim[1])
    else:
        if xmax is None:
            xmax = symmetric_xmax(df["value_std"].values)
        lo, hi = -float(xmax), float(xmax)
    if not lo < hi:
        raise ValueError(f"x limits must increase, got ({lo}, {hi})")
    fmt = FuncFormatter(tick_formatter) if tick_formatter else FuncFormatter(sigma_formatter)

    def clip_text(v):
        return str(fmt(v)) if tick_formatter else fmt_signed(v, 1) + "σ"

    headers = bool(xlabel or gutter_label or (show_values and values_label))
    with style_ctx(), font_ctx():
        title_lines, subtitle_lines, source_lines = _wrapped(title, subtitle, source, width_in)
        if ax is None:
            fig, ax = plt.subplots(figsize=figure_size(
                n_rows, width_in, title=title, subtitle=subtitle, source=source, key=show_key,
                headers=headers))
            created = True
        else:
            fig = ax.figure
            created = False
        w_in, h_in = fig.get_size_inches()
        head_in = header_inches(len(title_lines), len(subtitle_lines), headers)
        if created:
            fig.subplots_adjust(left=0.27, right=0.80 if show_values else 0.97,
                                top=1 - head_in / h_in,
                                bottom=footer_inches(len(source_lines), show_key) / h_in)

        if auto_x:
            # Leave room for a U-turn cap and the round stroke end beyond the
            # most extreme value, so nothing is cut at the axis edge.
            ax.set_xlim(lo, hi)
            ax.set_ylim(n_rows, 0)
            pad = cap_bulge(ax, LANE_GAP) + pt_to_x(ax, PATH_LW / 2.0 + 2.0)
            xmax = symmetric_xmax(np.abs(df["value_std"].values) + pad)
            lo, hi = -float(xmax), float(xmax)

        # Limits and furniture first: the cap geometry reads the pixel scale.
        ax.set_xlim(lo, hi)
        ax.set_ylim(n_rows, 0)
        despine(ax, sides=("top", "right", "left", "bottom"))
        ticks = np.arange(math.ceil(lo / xtick_step - 1e-9) * xtick_step,
                          math.floor(hi / xtick_step + 1e-9) * xtick_step + 1e-9, xtick_step)
        ax.xaxis.set_major_locator(FixedLocator(ticks))
        ax.xaxis.set_major_formatter(fmt)
        ax.xaxis.set_minor_locator(FixedLocator([]))
        ax.xaxis.tick_top()
        ax.tick_params(axis="x", which="both", top=False, bottom=False, length=0,
                       labeltop=True, labelbottom=False, labelsize=TICK_PT,
                       labelcolor=MUTED, pad=4)
        ax.set_yticks([])
        ax.set_yticks([], minor=True)
        for t in ticks:
            if abs(t) > 1e-9:
                ax.axvline(t, color=GRID, lw=0.8, zorder=0.5)
        ax.axvline(0, color=ZERO, lw=1.6, zorder=1.5)
        for i in range(1, n_rows):
            ax.axhline(i, color=SEPARATOR, lw=0.6, zorder=0.6)
        if highlight in rows:
            i = rows.index(highlight)
            ax.axhspan(i, i + 1, color=BAND, zorder=0.2, lw=0)

        lane_gap = LANE_GAP
        bulge = cap_bulge(ax, lane_gap)
        colors = issue_colors(len(issues), palette)
        label_tr = blended_transform_factory(fig.transFigure, ax.transData)
        value_tr = blended_transform_factory(ax.transAxes, ax.transData)

        for i, row in enumerate(rows):
            g = df[df["row"] == row].sort_values("issue_date")
            center = i + 0.5
            vals = g["value_std"].values.astype(float)
            steps = [step_of[d] for d in g["issue_date"]]
            dates = list(g["issue_date"])
            plan = layout_row(vals, steps, layout=layout, split=split,
                              deadband=deadband, max_lanes=max_lanes)
            n_lanes = plan["n_lanes"]
            ys = {k: lane_y(center, k, n_lanes, lane_gap) for k in range(n_lanes)}
            xs = np.clip(vals, lo, hi)
            clipped = (vals > hi + 1e-12) | (vals < lo - 1e-12)
            runs, lanes, conns = plan["runs"], plan["lanes"], plan["connectors"]
            last = len(vals) - 1

            # --- lane paths (solid), dashed where an issue is skipped
            for r, (run, lane) in enumerate(zip(runs, lanes)):
                y = ys[lane]
                # After an S-bend the bend itself covers the first step of this
                # run; after a U-turn (or on the same lane) the path continues
                # from the turning point.
                start = 1 if (r > 0 and conns[r - 1] == "sbend") else 0
                verts, codes = [], []
                for j in range(start, len(run)):
                    idx = run[j]
                    p = (xs[idx], y)
                    if not verts:
                        verts.append(p)
                        codes.append(Path.MOVETO)
                        continue
                    prev_idx = run[j - 1]
                    if steps[idx] - steps[prev_idx] > 1:   # skipped issue: dashed
                        ax.add_line(Line2D([xs[prev_idx], xs[idx]], [y, y], color=PATH,
                                           lw=PATH_LW, ls=(0, (1.0, 1.6)),
                                           solid_capstyle="round", dash_capstyle="round",
                                           zorder=2))
                        if codes[-1] == Path.MOVETO:
                            verts[-1] = p          # the previous point stood alone
                        else:
                            verts.append(p)
                            codes.append(Path.MOVETO)
                    else:
                        verts.append(p)
                        codes.append(Path.LINETO)
                if len(codes) > 1 and codes[-1] == Path.MOVETO:
                    verts.pop()                    # a trailing lone MOVETO draws nothing
                    codes.pop()
                if len(verts) > 1:
                    ax.add_patch(PathPatch(Path(verts, codes), facecolor="none",
                                           edgecolor=PATH, lw=PATH_LW, capstyle="round",
                                           joinstyle="round", zorder=2))
                # connector into the next run (none when both share a lane)
                if r < len(runs) - 1 and conns[r] != "same":
                    y_next = ys[lanes[r + 1]]
                    turn = run[-1]
                    if conns[r] == "uturn":
                        d = plan["turn_dirs"][r] or 1
                        cv, cc = cap_path(xs[turn], y, y_next, d * bulge)
                    else:
                        nxt = runs[r + 1]
                        target_idx = nxt[1] if len(nxt) > 1 else nxt[0]
                        cv, cc = sbend_path(xs[turn], y, xs[target_idx], y_next)
                    ax.add_patch(PathPatch(Path(cv, cc), facecolor="none", edgecolor=PATH,
                                           lw=PATH_LW, capstyle="round", joinstyle="round",
                                           zorder=2))

            # --- dots, light (first issue) to dark (latest); later issues on
            # top. Clipped values get a wedge at the edge and their true value.
            for idx, (x, v) in enumerate(zip(xs, vals)):
                y = ys[plan["point_lane"][idx]]
                step = steps[idx]
                z = 5 + step / max(len(issues), 1)
                if clipped[idx]:
                    beyond_hi = v > hi
                    ax.plot([x], [y], marker=">" if beyond_hi else "<", ms=DOT_SIZE + 1,
                            mfc=colors[step], mec="white", mew=1.0, zorder=z, ls="none")
                    ax.annotate(clip_text(v), (x, y),
                                xytext=(-8 if beyond_hi else 8, 0), textcoords="offset points",
                                ha="right" if beyond_hi else "left", va="center",
                                fontsize=ROLE_PT, color=MUTED, zorder=6)
                else:
                    ax.plot([x], [y], marker="o", ms=DOT_SIZE, mfc=colors[step], mec="white",
                            mew=1.0, zorder=z, ls="none")

            # --- issue labels, placed only where they collide with nothing
            want = label_rows != "none" and (label_rows == "all" or i == 0 or plan["merged"])
            if want:
                labels = (list(g["issue_label"]) if "issue_label" in g.columns
                          else [issue_label(d, span_years) for d in dates])
                last_dir = (1 if xs[last] >= xs[last - 1] else -1) if len(vals) >= 2 else 1
                _place_issue_labels(ax, xs, [ys[k] for k in plan["point_lane"]], labels,
                                    runs=[(xs[run].min(), xs[run].max(), ys[lane])
                                          for run, lane in zip(runs, lanes)],
                                    first_row=(i == 0), last_dir=last_dir)

            # --- row label (wrapped) + role, left gutter
            role = str(g["role"].iloc[0])
            inv = bool(g["invert"].iloc[0])
            label = f"{row} (inverted)" if inv and "inverted" not in str(row) else str(row)
            lines = textwrap.wrap(label, LABEL_WRAP) or [label]
            if len(lines) > 2:
                lines = lines[:2]
                lines[1] = lines[1][:LABEL_WRAP - 1].rstrip() + "…"
            y_lab = center - (0.11 if show_roles else 0.0) - (0.06 if len(lines) > 1 else 0.0)
            ax.text(MARGIN_X, y_lab, "\n".join(lines), transform=label_tr, ha="left",
                    va="center", fontsize=LABEL_PT, color=TEXT, zorder=6, linespacing=1.15)
            if show_roles:
                y_role = center + 0.14 + (0.1 if len(lines) > 1 else 0.0)
                ax.text(MARGIN_X, y_role, ROLE_TEXT.get(role, role), transform=label_tr,
                        ha="left", va="center", fontsize=ROLE_PT, color=MUTED, zorder=6)

            # --- right-hand value column
            if show_values:
                disp = g["display"].iloc[-1] if "display" in g.columns else None
                text = disp if isinstance(disp, str) else default_display(g, change=show_change)
                if text:
                    ax.text(1.02, center, text, transform=value_tr, ha="left", va="center",
                            fontsize=TICK_PT, color=TEXT)

        # --- column headers above the tick labels (text is not clipped)
        y_head = -0.42
        if gutter_label:
            ax.text(MARGIN_X, y_head, gutter_label, transform=label_tr, ha="left",
                    va="center", fontsize=LABEL_PT, color=TEXT, fontweight="bold")
        if xlabel:
            ax.text(lo, y_head, xlabel, ha="left", va="center", fontsize=LABEL_PT,
                    color=TEXT, fontweight="bold", clip_on=False)
        if show_values and values_label:
            ax.text(1.02, y_head, values_label, transform=value_tr, ha="left",
                    va="center", fontsize=TICK_PT, color=MUTED, linespacing=1.15)
        if show_key:
            labels = [issue_label(d, span_years) for d in issues]
            handles = [Line2D([], [], ls="none", marker="o", ms=DOT_SIZE, mfc=c, mec="white",
                              mew=1.0, label=lab) for c, lab in zip(colors, labels)]
            ax.legend(handles=handles, loc="upper center", bbox_to_anchor=(0.5, -0.015),
                      ncol=len(handles), frameon=False, fontsize=ISSUE_PT,
                      handletextpad=0.15, columnspacing=1.0, borderaxespad=0.0)

        # --- title, subtitle, source: wrapped, each block sized by its lines
        y = 1 - 0.14 / h_in
        if title_lines:
            fig.text(MARGIN_X, y, "\n".join(title_lines), ha="left", va="top",
                     fontsize=TITLE_PT, fontweight="bold", color=TEXT, linespacing=1.15)
            y -= (0.08 + len(title_lines) * TITLE_LINE_IN) / h_in
        if subtitle_lines:
            fig.text(MARGIN_X, y, "\n".join(subtitle_lines), ha="left", va="top",
                     fontsize=SUBTITLE_PT, color=MUTED, linespacing=1.3)
        if source_lines:
            fig.text(MARGIN_X, 0.1 / h_in, "\n".join(source_lines), ha="left", va="bottom",
                     fontsize=SOURCE_PT, color=MUTED, linespacing=1.3)
    return fig, ax


def save_snake(fig, out_stem, *, formats=("png", "pdf"), dpi=300):
    """Write ``<out_stem>.png`` (and ``.pdf``) with a tight bounding box, in
    the house font context so the saved files render like the figure.
    Returns the paths written."""
    from pathlib import Path as _P

    out_stem = _P(out_stem)
    out_stem.parent.mkdir(parents=True, exist_ok=True)
    written = []
    with style_ctx(), font_ctx():
        for ext in formats:
            p = out_stem.with_suffix(f".{ext}")
            fig.savefig(p, dpi=dpi, bbox_inches="tight", pad_inches=0.15, facecolor="white")
            written.append(p)
    return written
