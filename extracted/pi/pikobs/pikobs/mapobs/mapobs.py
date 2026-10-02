#!/usr/bin/python3
# GENERATED -- this docstring is written by pikobs/build_doc/build_mapobs.py.
# Edit that file and run ./pikobs_doc.sh; a change made here is lost.
r"""================================================
pikobs.mapobs -- Observation Coverage Dashboards
================================================

When a family suddenly brings fewer observations, the first question is
where they went: a satellite that stopped reporting, a region that fell
out of the domain, a channel that got switched off, a pass that arrived
late. ``mapobs`` answers it with nine panels that share the same window:
the map, its longitude and latitude profiles, the two cross-sections, the
vertical distribution and the per-station contributions.

Each sub-interval of a cycle -- 15 minutes unless you change it -- gets its
own dashboard, and that is where a single satellite pass shows up. Over a
day or less, each cycle also gets a master dashboard with its six hours at
once. On a radiance family those are heavy images, so over a longer period
they are left out unless ``DASHBOARD_6H`` asks for them.

Quick start
===========

.. code-block:: bash

   wget https://gitlab.science.gc.ca/dlo001/Pikobs/-/raw/master/pikobs/script/run_mapobs.sh
   chmod +x run_mapobs.sh

The wrapper runs on the node you are on and never submits to PBS, so open a
compute node first, edit the ``USER SETTINGS`` block and launch:

.. code-block:: bash

   qsub -I -lselect=1:ncpus=80:mem=185gb -lwalltime=2:0:0
   nano run_mapobs.sh
   ./run_mapobs.sh

.. note::

   mapobs is the heaviest module in memory. Each cycle is read whole by
   its own task, and a task needs about seven times the size of its file:
   a week of iasi (28 cycles) peaked at 188 GB, more than the 185 GB asked
   for above. For a week or more of a radiance family, ask for more memory
   -- a ppp7 node has about 690 GB, and ``mem=400gb`` is accepted -- or
   for fewer workers (``N_CPUS=40``). The 6-h dashboards add to it, which
   is why ``DASHBOARD_6H=auto`` only draws them for four cycles or fewer;
   keep it that way, or ``off``, for anything longer.

.. warning::

   Do not run the wrapper on a login node: the extraction opens every 6-h
   file of the period in parallel.

.. important::

   Lists are **bash arrays**: ``FAMILY=(iasi cris)`` and
   ``REGION=(cyl npolar)``, not strings.

A run prints its phases and ends with the address of the viewer:

.. code-block:: text

   [mapobs] runs: g0
   [mapobs] regions: ['cyl', 'npolar']
   [mapobs] id_stn tokens: ['join', 'all']
   [mapobs] map drawing: auto (density above 100000 observations)
   [mapobs] input check OK: 21 cycles x 1 run(s) x 3 family(ies), 63 files, 18.2 GB
   [mapobs] scan: 63 tasks, 80 worker(s)
   [mapobs] scan time: 71.4s (24 groups, 63/63 files)
   [mapobs] plots: 63 cycle tasks
   [mapobs] plot time: 402.8s (1176 dashboards)
   Viewer: /home/dlo001/sites8/pikobs_mapobs/index.html
   Web:    to open it in a browser, link the folder under public_html once:
             ln -s /home/dlo001/sites8/pikobs_mapobs /home/dlo001/public_html/
           then: https://goc-dx-u3.science.gc.ca/~dlo001/pikobs_mapobs/index.html

`A live reference instance <https://goc-dx-u3.science.gc.ca/~dlo001/sites8/pikobs_doc_mapobs/pikobs_mapobs_viewer.html>`__.

How long a run takes, and how big a node to ask for: :doc:`runtime`.

----

1. How it works
===============

**Input check.** Every 6-h file of every run and family is looked up first.
If one is missing the run stops, says which cycles are missing and which
dates the directory does hold, and leaves ``PATHWORK`` untouched. The
module also refuses a ``PATHWORK`` that resolves to a home or a system
directory, since it wipes what it is given.

**Two passes, and a cycle at a time.** This module does not aggregate into
a database: the dashboards show the observations themselves, so it reads
them. What it does not do any more is hold the period in memory. The
**scan** reads each cycle once and keeps only its maxima, its vertical
range and its stations; those give the axes and the colours that every
dashboard of a group shares. The **plots** phase reads each cycle again,
inside the worker that draws it, and releases it right after. Memory is
therefore one cycle per worker, whatever the length of the period.

**Colours.** A station keeps its colour in every dashboard, on any machine,
because the colour comes from a hash of its name rather than from the
order it was met.

----

2. Configuration
================

Only the ``USER SETTINGS`` block of the wrapper is meant to be edited.

.. wrapper-settings:: run_mapobs.sh

----

3. Choosing the stations and levels
===================================

``ID_STN`` takes the tokens of the rest of Pikobs, and each one is its own
series of dashboards:

+-----------------------+---------------------------------------------------------------------+
| Token                 | Dashboards produced                                                 |
+=======================+=====================================================================+
| ``join``              | one series, every station together                                  |
+-----------------------+---------------------------------------------------------------------+
| ``all``               | one series per station, per instrument type for ai, sf, ua, gp, csr |
+-----------------------+---------------------------------------------------------------------+
| ``CAS`` or ``"CAS*"`` | the stations whose id starts with CAS, together                     |
+-----------------------+---------------------------------------------------------------------+
| ``=NOAA20``           | that station only                                                   |
+-----------------------+---------------------------------------------------------------------+
| ``N%``                | SQL ``LIKE`` pattern on the station id                              |
+-----------------------+---------------------------------------------------------------------+

``CHANNEL`` works the same way: ``join`` puts every level in one dashboard,
``all`` gives one per level, and an explicit list keeps only those.

----

4. One figure per panel
=======================

+--------------+-------------------------------------------------------------------------------+
| Figure       | What it shows                                                                 |
+==============+===============================================================================+
| ``map``      | each observation at its position, with the longitude and latitude profiles    |
+--------------+-------------------------------------------------------------------------------+
| ``cross``    | the zonal and meridional cross-sections: level against latitude and longitude |
+--------------+-------------------------------------------------------------------------------+
| ``vertical`` | observation count per level or channel, split by station                      |
+--------------+-------------------------------------------------------------------------------+
| ``stations`` | count and share per station or instrument type                                |
+--------------+-------------------------------------------------------------------------------+
| ``all``      | the four above stacked into a single image                                    |
+--------------+-------------------------------------------------------------------------------+

They are separate files on purpose. The panels do not want the same
shape: a map is wide, and the vertical distribution of an interferometer
with six hundred channels needs a metre of height. Together on one sheet,
the tall one squashes the rest and every figure costs what the worst of
them costs; apart, each grows to what it needs, and you can ask for only
the one you are going to look at.

``PANELS`` chooses them, and the viewer has a **Panel** selector:

.. code-block:: bash

   PANELS=(map cross vertical stations all)   # the four, plus the sheet
   PANELS=(map)                               # a first look, four times fewer files
   PANELS=(all)                               # only the sheet, the parts are removed

Colour always means the station, in every panel and in every figure of
the group, and it comes from a hash of the station name rather than from
the order the stations were met: the same platform keeps its colour on
any machine and in any run. Where the observations pile up the dots get
smaller and more transparent, which keeps a busy region readable without
replacing the station by an average.

.. image:: _static/mapobs_dashboard.png
   :alt: A 6-hour dashboard, nine panels
   :align: center
   :width: 100%

The vertical axis
-----------------

Levels are rows, not values. Channel numbers of an interferometer run to
thousands and are not consecutive; a pressure list has holes. Drawing
them at their value piles everything into a handful of lines, so each
level gets its own row, labelled with its number, and the panel grows as
tall as there are rows.

Which levels those are comes from the family, not from the column: the
module reads ``VCOORD`` from :func:`pikobs.family`, so ``sw`` is rounded
to 2000 Pa and ``ua`` to 20000 Pa exactly as in the other modules, and
``VCOTYP`` says whether the axis is a list of channels, a pressure that
reads with the ground at the bottom, or no vertical axis at all. The rows
are collected during the scan, over the whole period, so two cycles show
the same rows and can be compared by flipping between them.

----

5. Regions and projections
==========================

``REGION`` here means a projection, the same ones scatter uses:

+-------------------------------+-------------------------------+-------------+
| Region                        | Projection                    | Map cell    |
+===============================+===============================+=============+
| ``cyl``                       | Plate Carree, the whole globe | rectangular |
+-------------------------------+-------------------------------+-------------+
| ``npolar`` / ``spolar``       | Polar stereographic           | square      |
+-------------------------------+-------------------------------+-------------+
| ``orthon`` / ``orthos``       | Orthographic over a pole      | square      |
+-------------------------------+-------------------------------+-------------+
| ``canada`` / ``ameriquenord`` | Polar stereographic, centred  | square      |
+-------------------------------+-------------------------------+-------------+
| ``europe``                    | Polar stereographic, centred  | square      |
+-------------------------------+-------------------------------+-------------+
| ``robinson``                  | Robinson, the whole globe     | rectangular |
+-------------------------------+-------------------------------+-------------+

A pole-centred projection draws a disc, so it gets a round boundary in a
square cell: no empty corners, and the whole cap is visible.

Where the profiles sit follows from that. On ``cyl`` the axes of the map
**are** longitude and latitude, so a profile pinned to its edge lines up
with it column by column, and that is where they stay. On a polar or
rotated projection the map is projected: pinning the profiles to its
edges would suggest a correspondence that does not exist, so they go
underneath, each with its own degree axis. It is the same data either
way; what changes is whether the layout claims an alignment it has.

.. image:: _static/mapobs_polar.png
   :alt: A polar projection inside a square cell
   :align: center
   :width: 100%

----

6. The viewer
=============

``index.html`` has nine dropdowns: Experience, Family, Mode, Region,
Criteria, Varno, Station, Channel and Date; each one only offers what
exists for the choices on its left. **Play** runs through the dates, which
is the quickest way to watch a satellite sweep the globe, and a click
opens a dashboard at full size.

----

7. Output layout
================

::

   $PATHWORK/
   ├── pikobs_mapobs_viewer.html
   ├── mapobs_timing.json
   ├── <family>_6h/            (the 6-h dashboards, when they are drawn)
   │   └── <panel>_<run>_<family>_<region>[_<surface>][_<special>]_<flag>_<varno>_<stn>_<level>_<date>.png
   └── <family>_<interval>min/
       └── <panel>_<run>_..._<date>_<HHMM>.png

With ``SVG="on"`` each figure is written again as ``.svg`` beside its PNG,
for editing before a presentation. A dashboard in points mode with
millions of observations gives a very large SVG, so ask for it on a small
selection.

----

8. Support
==========

Bugs and feature requests:
   `<https://gitlab.science.gc.ca/dlo001/Pikobs/-/issues>`_
"""

import json
import os
import re
import shutil
import sys
import tempfile
import time
import traceback
import warnings
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Sequence, Tuple

import dask
import numpy as np
import pandas as pd
from dask.distributed import Client

import pikobs
from pikobs.figures import svg_enabled
from pikobs.mapobs.mapobs_plot import (ALL_PANELS, N_BINS_LAT, N_BINS_LON,
                                       N_BINS_VCONT, PANELS, PlotContext,
                                       PAD_FACTOR_HIST,
                                       PAD_FACTOR_STN, VRANGE_PAD,
                                       build_global_color_map, is_round,
                                       map_projection, plot_panels,
                                       region_label,
                                       vertical_axis_orientation)
from pikobs.obsdb import check_input_files, cycle_path, open_cycle
from pikobs.obsdb.obsdb import split_tokens as _split_tokens, cycles as _cycles, input_size as _input_size  # shared, once
from pikobs.parallel import run_tasks
from pikobs.pbs_submit import maybe_submit_to_pbs
from pikobs.stations.stations import (StationSelector, _token_to_selector,
                                      parse_station_tokens)
from pikobs.web.viewer import generate_web

warnings.filterwarnings("ignore")

CYCLE_HOURS = 6

# How many distinct levels a group may carry before they stop being a
# list: past this the vertical panels fall back on a histogram.
MAX_LEVELS_KEPT = 2000

# Never wipe these, whatever --pathwork says.
_FORBIDDEN_PATHWORK = {"/", "/home", "/root", "/tmp", "/usr", "/var", "/etc"}


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────


def _safe(text: Any) -> str:
    return re.sub(r'[^A-Za-z0-9._+-]', '_', str(text))


def _fmt_bytes(n: float) -> str:
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if n < 1024 or unit == "TB":
            return f"{n:.1f} {unit}"
        n /= 1024.0


def _rdb_candidates(exp_path: str, fdate: str, family: str) -> List[str]:
    """The naming conventions a cycle file may follow."""
    return [os.path.join(exp_path, f"{fdate}_{family}"),
            os.path.join(exp_path, f"{fdate}_{family}.db")]


def resolve_rdb_path(exp_path: str, fdate: str, family: str) -> str:
    for c in _rdb_candidates(exp_path, fdate, family):
        if os.path.isfile(c):
            return c
    return _rdb_candidates(exp_path, fdate, family)[0]


def _validate_pathwork(pathwork: str) -> None:
    abs_p = os.path.abspath(pathwork).rstrip("/")
    if abs_p in _FORBIDDEN_PATHWORK or abs_p == os.path.expanduser("~"):
        raise ValueError(f"Refusing to wipe '{abs_p}'. "
                         f"Choose a dedicated --pathwork.")


def resolve_type_varno(varno) -> Tuple[str, str, str]:
    try:
        from pikobs.configobs.type_varno import type_varno
        return type_varno(str(varno))
    except Exception:                                    # pragma: no cover
        try:
            return pikobs.type_varno(str(varno))
        except Exception:
            return f"Varno: {varno}", "", "Vcoord"


# ─────────────────────────────────────────────────────────────────────────────
# Input check
# ─────────────────────────────────────────────────────────────────────────────

def load_cycle(db_path: str, varno, flag_sql: str, family: str,
               vcoord_expr: str = "d.vcoord",
               vcocrit: str = "", with_flag: bool = False,
               land: bool = False, pathwork: Optional[str] = None,
               special_on: bool = False) -> pd.DataFrame:
    """Read one cycle: position, level, station and time of each obs.

    The level comes from the family's ``VCOORD`` expression, not from the
    raw column: ``sw`` rounds the pressure to 2000 Pa and ``ua`` to
    20000 Pa, and reading the column directly would give this module
    thousands of levels where every other module has tens.

    Only one cycle at a time is ever in memory, and it is read inside the
    worker that needs it.
    """
    if not os.path.isfile(db_path):
        return pd.DataFrame()
    query = (f"SELECT h.lat, h.lon, {vcoord_expr} AS vcoord, h.id_stn, "
             f"h.codtyp, h.DATE, h.TIME"
             f"{', d.flag AS flag' if with_flag else ''} "
             f"FROM header h JOIN data d USING(id_obs) "
             f"WHERE d.varno = {varno} {flag_sql} {vcocrit}")
    try:
        with open_cycle(db_path) as conn:
            if special_on:
                query = _with_special(query, conn, family)
            df = pd.read_sql_query(query, conn)
    except Exception as exc:
        print(f"[mapobs] reading {os.path.basename(db_path)}: {exc}",
              file=sys.stderr, flush=True)
        return pd.DataFrame()
    if df.empty:
        return df

    df.columns = [c.lower() for c in df.columns]
    for col in ("lat", "lon", "vcoord"):
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df = df.dropna(subset=["lat", "lon"])
    if df.empty:
        return df
    if land:
        # land 1, sea 0: the grid and the rule of is_land_sql, for the
        # whole column at once
        from pikobs.configobs.landmask import is_land_array
        df["land"] = is_land_array(df["lat"].to_numpy(),
                                   df["lon"].to_numpy(), pathwork)
    if "special" in df.columns:
        # a few values for millions of rows: shared, not one string each
        df["special"] = pd.Categorical(df["special"])
    # one Python string per station, not one per row: SQLite hands back a
    # new string for every row -- 12 million on a cycle of iasi, most of its
    # memory -- and a trip through a categorical makes the rows share them;
    # the column stays plain text, for value_counts and the comparisons
    if df["id_stn"].dtype == object:
        df["id_stn"] = pd.Categorical(df["id_stn"]).astype(object)

    # composite families are grouped by instrument type, not by station
    try:
        from pikobs.configobs.special_family import (codtyp_label,
                                                     has_codtyp_groups)
        if has_codtyp_groups(family) and "codtyp" in df.columns:
            df["id_stn"] = df["codtyp"].map(codtyp_label)
    except Exception:
        pass

    # the time of each row, from the few thousand distinct date + time pairs
    # of a cycle: built from strings row by row, it took most of the
    # reading time and several GB on a cycle of iasi. Same format as before.
    key = (pd.to_numeric(df["date"], errors="coerce") * 1_000_000
           + pd.to_numeric(df["time"], errors="coerce"))
    uniq = pd.unique(key.dropna())
    stamps = pd.to_datetime(
        pd.Series(uniq).astype("int64").astype(str).str.zfill(14),
        format="%Y%m%d%H%M%S", errors="coerce")
    df["datetime"] = key.map(pd.Series(stamps.values, index=uniq))
    df = df.drop(columns=["date", "time"])
    return df.dropna(subset=["datetime"])


def selector_mask(df: pd.DataFrame, sel) -> pd.Series:
    """The rows of a cycle that belong to one station selection."""
    if sel.kind == 'join':
        return pd.Series(True, index=df.index)
    ids = df["id_stn"].astype(str)
    if sel.kind in ('station', 'exact'):
        return ids == str(sel.value)
    if sel.kind == 'prefix':
        return ids.str.startswith(str(sel.value))
    if sel.kind == 'like':
        pattern = ('^' + re.escape(str(sel.value))
                   .replace('%', '.*').replace('_', '.') + '$')
        return ids.str.match(pattern)
    if sel.kind == 'codtyp' and "codtyp" in df.columns:
        return df["codtyp"].astype('Int64').isin(list(sel.codes))
    return pd.Series(True, index=df.index)


def selectors_for(df: pd.DataFrame, tokens: Sequence[str],
                  family: str) -> List[StationSelector]:
    """Turn the --id_stn tokens into selections, using the stations of
    this cycle for ``all``.

    mapobs reads the observation files directly, with no aggregated
    database to look the stations up in, so the expansion happens where
    the data is.
    """
    out: List[StationSelector] = []
    seen = set()

    def _add(sel):
        if sel is not None and sel.tag not in seen:
            seen.add(sel.tag)
            out.append(sel)

    present = sorted(map(str, df["id_stn"].unique())) if not df.empty else []
    for tok in tokens:
        if str(tok).lower() == 'all':
            for stn in present:
                _add(StationSelector('station', stn))
        else:
            try:
                _add(_token_to_selector(str(tok)))
            except Exception as exc:
                print(f"[mapobs] id_stn token '{tok}' not understood ({exc}), "
                      f"read as an exact station id", file=sys.stderr,
                      flush=True)
                _add(StationSelector('exact', str(tok).lstrip('=')))
    return out or [StationSelector('join', 'join')]


def region_mask(df: pd.DataFrame, extent: Sequence[float]) -> pd.Series:
    lon_w, lon_e, lat_s, lat_n = extent
    return ((df["lat"] >= lat_s) & (df["lat"] <= lat_n)
            & (df["lon"] >= lon_w) & (df["lon"] <= lon_e))


def _layer_bounds(family: str, vsel) -> Optional[Tuple[float, float]]:
    """(low, high) of vcoord for a layer label such as '2 | 850-500 hPa',
    else None. The layers of scatter: low < vcoord <= high."""
    m = re.fullmatch(r"\d+ \| ([0-9.]+)-([0-9.]+) (hPa|km)", str(vsel))
    if not m:
        return None
    from pikobs.scatter.scatter import layer_unit_scale, _vcotyp
    scale = layer_unit_scale(_vcotyp(family))
    a, b = float(m.group(1)) * scale, float(m.group(2)) * scale
    return min(a, b), max(a, b)


def _vsel_rows(dfs: pd.DataFrame, vsel, family: str) -> pd.DataFrame:
    """The rows of one vertical selection: join, a level, or a layer."""
    if vsel == 'join':
        return dfs
    layer = _layer_bounds(family, vsel)
    if layer:
        return dfs[(dfs["vcoord"] > layer[0]) & (dfs["vcoord"] <= layer[1])]
    return dfs[dfs["vcoord"] == float(vsel)]


def _family_vsel(family: str, vcoord_sel, pressure_layers,
                 height_layers) -> List[str]:
    """What CHANNEL asks for, then the layers of scatter for this family."""
    from pikobs.scatter.scatter import family_layers, _layer_display, _vcotyp
    layers = family_layers(family, pressure_layers, height_layers)[1:]
    return list(vcoord_sel) + [_layer_display(iv, _vcotyp(family))
                               for iv in layers]


# the projections map_projection knows
_PROJECTIONS = ('cyl', 'robinson', 'npolar', 'spolar', 'orthon', 'orthos',
                'canada', 'ameriquenord', 'europe')


def _region_combos(regions, projections) -> List[Tuple[str, str, str]]:
    """(tag, region, projection) of every map: each region in each
    projection, or in the one it names (hrdps:canada). An old token that
    names a projection (cyl, npolar) reads as Monde in that projection."""
    from pikobs.configobs import regionsobs
    known = set(regionsobs.list_regions())
    out = []
    for token in regions:
        name, _, pin = str(token).partition(':')
        if not pin and name not in known and name.lower() in _PROJECTIONS:
            name, pin = 'Monde', name.lower()
        if name not in known:
            raise ValueError(f"unknown region {name!r}; the regions are: "
                             f"{', '.join(sorted(known))}")
        for proj in ([pin] if pin else projections):
            if str(proj).lower() not in _PROJECTIONS:
                raise ValueError(f"unknown projection {proj!r}; the "
                                 f"projections are: {', '.join(_PROJECTIONS)}")
            out.append((f"{name}@{str(proj).lower()}", name, str(proj).lower()))
    return list(dict.fromkeys(out))


def _pikobs_region_mask(df: pd.DataFrame, name: str,
                        pathwork: Optional[str]) -> np.ndarray:
    """The rows of a region of Pikobs, the whole cycle at once: a box with
    the rule of generate_latlon_criteria, a polygon with its raster mask --
    what the SQL of the other modules tests, row by row."""
    from pikobs.configobs import regionsobs
    lat = df["lat"].to_numpy(float)
    lon = df["lon"].to_numpy(float)
    lon = np.where(lon > 180.0, lon - 360.0, lon)
    if regionsobs.is_polygon(name):
        mask, lat0, lon0, res = regionsobs.cached_mask(
            name, pathwork or regionsobs.cache_dir())
        i = np.rint((lat - lat0) / res).astype(np.int64)
        j = np.rint((lon - lon0) / res).astype(np.int64)
        ok = (i >= 0) & (j >= 0) & (i < mask.shape[0]) & (j < mask.shape[1])
        inside = np.zeros(lat.shape, bool)
        inside[ok] = np.asarray(mask)[i[ok], j[ok]].astype(bool)
        return inside
    lat1, lat2, lon1, lon2 = regionsobs.regions(name)
    top_lat = lat <= lat2 if lat2 == 90 else lat < lat2
    top_lon = lon <= lon2 if lon2 == 180 else lon < lon2
    if lon1 >= lon2:                  # across the antimeridian
        return (lat >= lat1) & top_lat & ((lon >= lon1) | top_lon)
    return (lat >= lat1) & top_lat & (lon >= lon1) & top_lon


def _combo_mask(df: pd.DataFrame, tag: str, extent,
                pathwork: Optional[str]) -> np.ndarray:
    """A region in a projection: its observations that the map shows."""
    name = str(tag).split('@', 1)[0]
    return (region_mask(df, extent).to_numpy()
            & _pikobs_region_mask(df, name, pathwork))


def _extras(task: Dict[str, Any]) -> Dict[str, Any]:
    """What load_cycle reads beyond the usual columns: the surface when a
    run splits land and ocean, the special column when it is on."""
    return {'land': any(lo != 'all' for lo in task.get('land_oceans') or ['all']),
            'pathwork': task.get('pathwork'),
            'special_on': bool(task.get('special_on'))}


def _splits(df: pd.DataFrame, task: Dict[str, Any], selectors):
    """(surface, special value, rows, selection) of one region's rows.

    With all and off it is (all, all, df, sel) for every selection: the
    same rows, in the same order, as before.
    """
    for surf in task.get('land_oceans') or ['all']:
        d1 = (df if surf == 'all'
              else df[df["land"] == (1 if surf == 'land' else 0)])
        if d1.empty:
            continue
        values = (sorted(str(v) for v in d1["special"].dropna().unique())
                  if "special" in d1.columns else ['all'])
        for sp in values:
            d2 = d1 if sp == 'all' else d1[d1["special"] == sp]
            if d2.empty:
                continue
            for sel in selectors:
                yield surf, sp, d2, sel


def _sp_label(family: str, sp) -> str:
    """The name of a special value: IR channel, 0.5 ...; all when off."""
    from pikobs.configobs.special_family import special_label
    return special_label(family, sp)


def _where_tag(family: str, surf, sp) -> str:
    """The surface and the special value in a file name, only when they
    split something: with all the name is the one it always was."""
    return "".join(f"_{_safe(x)}" for x in (surf, _sp_label(family, sp))
                   if x not in (None, '', 'all'))


def _where_txt(family: str, surf, sp) -> str:
    """The same after the region of a title: ', land', ', IR channel'."""
    return "".join(f", {x}" for x in (surf, _sp_label(family, sp))
                   if x not in (None, '', 'all'))


def _with_special(query: str, conn, family: str) -> str:
    """The query with the family's special column as ``special``, or the
    constant 'all' when the file does not carry it."""
    from pikobs.configobs.special_family import special_select
    hcols = [r[1] for r in conn.execute("PRAGMA table_info(header);").fetchall()]
    sp, _ = special_select(family, hcols, True, prefix="h.")
    return query.replace(" FROM header h", f", {sp} AS special FROM header h", 1)


# ─────────────────────────────────────────────────────────────────────────────
# Phase 1: the scales every dashboard of a group shares
# ─────────────────────────────────────────────────────────────────────────────

def _summary(df: pd.DataFrame, extent, is_channel: bool,
             interval_min: int) -> Dict[str, Any]:
    """Maxima and ranges of one cycle, for the common scales."""
    lon_ext = (extent[0], extent[1])
    lat_ext = (extent[2], extent[3])

    def _counts(g: pd.DataFrame) -> Tuple[int, int, int, int]:
        if g.empty:
            return 0, 0, 0, 0
        lon = int(np.histogram(g["lon"], bins=N_BINS_LON,
                               range=lon_ext)[0].max())
        lat = int(np.histogram(g["lat"], bins=N_BINS_LAT,
                               range=lat_ext)[0].max())
        stn = int(g["id_stn"].value_counts().max())
        v = g["vcoord"].dropna()
        if v.empty:
            vmax = 0
        elif is_channel:
            vmax = int(v.astype(int).value_counts().max())
        else:
            vmax = int(np.histogram(v, bins=N_BINS_VCONT)[0].max())
        return lon, lat, vmax, stn

    six = _counts(df)
    slot = (0, 0, 0, 0)
    for _, g in df.groupby(pd.Grouper(key="datetime",
                                      freq=f"{interval_min}min")):
        if not g.empty:
            slot = tuple(max(a, b) for a, b in zip(slot, _counts(g)))
    v = df["vcoord"].dropna()
    # the levels of the whole period, not of this cycle: two cycles must
    # show the same rows, otherwise they cannot be compared by flipping
    levels = sorted(set(v.unique().tolist()))[:MAX_LEVELS_KEPT]
    return {
        'six': six, 'slot': slot, 'n': int(len(df)),
        'v_min': float(v.min()) if not v.empty else None,
        'v_max': float(v.max()) if not v.empty else None,
        'stations': sorted(map(str, df["id_stn"].unique())),
        'levels': levels,
    }


# ─────────────────────────────────────────────────────────────────────────────
# The cycle cache: read once by the scan, mapped by every drawing shard
# ─────────────────────────────────────────────────────────────────────────────

_CACHE_COLS = ("lat", "lon", "vcoord", "codtyp", "flag", "dt", "stn")


def _cache_dir(pathwork: str) -> str:
    return os.path.join(pathwork, ".mapobs_cache")


def _cache_path(task: Dict[str, Any], varno) -> str:
    """One folder per run, cycle and varno: control and experience files
    share their names."""
    return os.path.join(_cache_dir(task.get('pathwork') or '.'),
                        f"{_safe(task['exp_name'])}_"
                        f"{os.path.basename(task['filein'])}_{varno}")


def _flag_values(values, criterion: str) -> set:
    """The flag values that meet a criterion, asked of SQLite itself: the
    criterion is the SQL of pikobs.flag_criteria, so its meaning stays
    exact."""
    import sqlite3
    with sqlite3.connect(":memory:") as con:
        con.execute("CREATE TABLE t (flag INTEGER);")
        con.executemany("INSERT INTO t VALUES (?);", [(int(v),) for v in values])
        return {r[0] for r in con.execute(
            f"SELECT flag FROM t WHERE 1=1 {criterion};")}


def _flag_mask(flags: "pd.Series", criterion: str) -> "pd.Series":
    return flags.isin(_flag_values(pd.unique(flags.dropna()), criterion))


def _write_cache(df: pd.DataFrame, path: str) -> None:
    """The columns of one cycle and varno, as .npy files (never raises)."""
    if df is None or df.empty or os.path.isdir(path):
        return
    try:
        import json
        tmp = f"{path}.tmp{os.getpid()}"
        os.makedirs(tmp, exist_ok=True)
        cat = pd.Categorical(df["id_stn"])
        cols = {"lat": df["lat"].to_numpy(), "lon": df["lon"].to_numpy(),
                "vcoord": df["vcoord"].to_numpy(),
                "codtyp": df["codtyp"].to_numpy(),
                "flag": df["flag"].to_numpy(),
                "dt": df["datetime"].to_numpy().view("int64"),
                "stn": cat.codes.astype(np.int32)}
        # the surface and the special column, only when a run asks
        if "land" in df.columns:
            cols["land"] = df["land"].to_numpy()
        spcat = (pd.Categorical(df["special"]) if "special" in df.columns
                 else None)
        if spcat is not None:
            cols["special"] = spcat.codes.astype(np.int32)
        for name, arr in cols.items():
            np.save(os.path.join(tmp, f"{name}.npy"), arr)
        flags = pd.unique(df["flag"].dropna())
        with open(os.path.join(tmp, "meta.json"), "w") as fh:
            json.dump({"stations": [str(c) for c in cat.categories],
                       "flags": [int(v) for v in flags],
                       "dt_dtype": str(df["datetime"].to_numpy().dtype),
                       "specials": ([str(c) for c in spcat.categories]
                                    if spcat is not None else None)}, fh)
        try:
            os.rename(tmp, path)
        except OSError:                   # another scan wrote it first
            shutil.rmtree(tmp, ignore_errors=True)
    except Exception as exc:
        print(f"[mapobs] cache not written for {os.path.basename(path)}: "
              f"{exc}", file=sys.stderr, flush=True)


def _read_cache(path: str, criterion: str) -> Optional[pd.DataFrame]:
    """The rows of a cached cycle that meet a criterion; None without one."""
    if not os.path.isdir(path):
        return None
    try:
        import json
        with open(os.path.join(path, "meta.json")) as fh:
            meta = json.load(fh)
        arr = {n: np.load(os.path.join(path, f"{n}.npy"), mmap_mode="r")
               for n in _CACHE_COLS}
        keep = np.fromiter(_flag_values(meta["flags"], criterion), dtype=float)
        idx = np.flatnonzero(np.isin(arr["flag"], keep))
        # a station code of -1 (no station) points at the last entry, NaN
        names = np.asarray(meta["stations"] + [np.nan], dtype=object)
        out = pd.DataFrame({
            "lat": arr["lat"][idx], "lon": arr["lon"][idx],
            "vcoord": arr["vcoord"][idx],
            "id_stn": names[arr["stn"][idx]],
            "codtyp": arr["codtyp"][idx],
            "flag": arr["flag"][idx],
            "datetime": np.asarray(arr["dt"][idx]).view(meta["dt_dtype"]),
        })
        # the surface and the special column, when the scan wrote them
        if os.path.isfile(os.path.join(path, "land.npy")):
            out["land"] = np.asarray(np.load(os.path.join(path, "land.npy"),
                                             mmap_mode="r")[idx])
        if meta.get("specials") is not None:
            codes = np.load(os.path.join(path, "special.npy"), mmap_mode="r")
            out["special"] = pd.Categorical.from_codes(
                np.asarray(codes[idx]), meta["specials"])
        return out
    except Exception as exc:
        print(f"[mapobs] cache unreadable ({os.path.basename(path)}): {exc}; "
              f"reading the base", file=sys.stderr, flush=True)
        return None


def _scan_task(task: Dict[str, Any]) -> Optional[List[Dict[str, Any]]]:
    """One cycle: the summaries of every combination it contributes to."""
    try:
        out = []
        for varno in task['varnos']:
            # read once per varno, every criterion taken from it, and left
            # in the cache for the drawing shards
            df_all = load_cycle(task['filein'], varno, "", task['family'],
                                task['vcoord_expr'], task['vcocrit'],
                                with_flag=True, **_extras(task))
            if task.get('pathwork'):
                _write_cache(df_all, _cache_path(task, varno))
            for flag in task['flags']:
                df = (df_all[_flag_mask(df_all['flag'],
                                        pikobs.flag_criteria(flag))]
                      if not df_all.empty else df_all)
                if df.empty:
                    continue
                selectors = selectors_for(df, task['stn_tokens'],
                                          task['family'])
                for region, extent in task['regions']:
                    dfr = df[_combo_mask(df, region, extent,
                                         task.get('pathwork'))]
                    if dfr.empty:
                        continue
                    for surf, sp, dfx, sel in _splits(dfr, task, selectors):
                        dfs = dfx[selector_mask(dfx, sel)]
                        if dfs.empty:
                            continue
                        for vsel in task['vcoord_sel']:
                            dfv = _vsel_rows(dfs, vsel, task['family'])
                            if dfv.empty:
                                continue
                            out.append({
                                'key': (task['exp_name'], task['family'],
                                        region, flag, str(varno),
                                        sel.tag, str(vsel), surf, sp),
                                **_summary(dfv, extent,
                                           task['is_channel'][str(varno)],
                                           task['interval_min']),
                            })
                del df
        return out
    except Exception:
        print(f"[mapobs] scan failed for {task['filein']}:\n"
              f"{traceback.format_exc()}", file=sys.stderr, flush=True)
        return None


def _merge_summaries(results) -> Dict[tuple, Dict[str, Any]]:
    merged: Dict[tuple, Dict[str, Any]] = {}
    for res in results:
        for row in res or []:
            key = tuple(row['key'])
            cur = merged.setdefault(key, {
                'six': (0, 0, 0, 0), 'slot': (0, 0, 0, 0), 'n': 0,
                'v_min': None, 'v_max': None, 'stations': set(),
                'levels': set(),
            })
            cur['six'] = tuple(max(a, b) for a, b in zip(cur['six'],
                                                         row['six']))
            cur['slot'] = tuple(max(a, b) for a, b in zip(cur['slot'],
                                                          row['slot']))
            cur['n'] += row['n']
            for name, op in (('v_min', min), ('v_max', max)):
                if row[name] is not None:
                    cur[name] = (row[name] if cur[name] is None
                                 else op(cur[name], row[name]))
            cur['stations'].update(row['stations'])
            cur['levels'].update(row.get('levels', ()))
    return merged


# ─────────────────────────────────────────────────────────────────────────────
# Phase 2: the dashboards of one cycle
# ─────────────────────────────────────────────────────────────────────────────

def _plot_task(task: Dict[str, Any]) -> Optional[List[Dict[str, str]]]:
    """Every dashboard a cycle produces: the 6-h master and its slices."""
    try:
        items: List[Dict[str, str]] = []
        fdate = task['cycle']
        # this task draws every nshard-th piece of the cycle -- a 6-h
        # dashboard or one slice -- from shard; the walk is the same in
        # every shard, so each piece is drawn exactly once between them
        shard, nshard = task.get('shard', 0), task.get('nshard', 1)
        count = [-1]

        def pick():
            count[0] += 1
            return count[0] % nshard == shard
        fdt = datetime.strptime(fdate, "%Y%m%d%H")
        import time as _time
        _tr = _td = 0.0
        _rss = _dfb = 0
        for varno in task['varnos']:
            cache = _cache_path(task, varno)
            for flag in task['flags']:
                _t = _time.time()
                # the cycle the scan left in the cache, this criterion's rows
                df = _read_cache(cache, pikobs.flag_criteria(flag))
                if df is None:           # no cache: the base, as before
                    df = load_cycle(task['filein'], varno,
                                    pikobs.flag_criteria(flag),
                                    task['family'], task['vcoord_expr'],
                                    task['vcocrit'], **_extras(task))
                _tr += _time.time() - _t
                if os.environ.get('PIKOBS_TIMING') and not df.empty:
                    import psutil as _ps
                    _rss = max(_rss, _ps.Process().memory_info().rss)
                    _dfb = max(_dfb, int(df.memory_usage(deep=True).sum()))
                if df.empty:
                    continue
                selectors = selectors_for(df, task['stn_tokens'],
                                          task['family'])
                for region, extent in task['regions']:
                    dfr = df[_combo_mask(df, region, extent,
                                         task.get('pathwork'))]
                    if dfr.empty:
                        continue
                    for surf, sp, dfx, sel in _splits(dfr, task, selectors):
                        dfs = dfx[selector_mask(dfx, sel)]
                        if dfs.empty:
                            continue
                        for vsel in task['vcoord_sel']:
                            dfv = _vsel_rows(dfs, vsel, task['family'])
                            if dfv.empty:
                                continue
                            key = (task['exp_name'], task['family'], region,
                                   flag, str(varno), sel.tag, str(vsel),
                                   surf, sp)
                            ctx6, ctx15 = task['contexts'].get(key, (None,
                                                                     None))
                            if ctx6 is None:
                                continue
                            _t = _time.time()
                            items += _draw_group(dfv, fdate, fdt, task, ctx6,
                                                 ctx15, region, flag, varno,
                                                 sel, vsel, pick=pick,
                                                 surface=surf, special=sp)
                            _td += _time.time() - _t
                del df
        if os.environ.get('PIKOBS_TIMING'):
            print(f"[mapobs timing] {os.path.basename(task['filein'])} shard {shard}: "
                  f"read {_tr:.1f}s, draw {_td:.1f}s, {len(items)} pieces, "
                  f"cycle {_dfb / 1e9:.2f} GB in pandas, process {_rss / 1e9:.2f} GB",
                  file=sys.stderr, flush=True)
        return items
    except Exception:
        print(f"[mapobs] plots failed for {task['filein']}:\n"
              f"{traceback.format_exc()}", file=sys.stderr, flush=True)
        return None


def _draw_group(dfv, fdate, fdt, task, ctx6, ctx15, region, flag, varno, sel,
                vsel, pick=None, surface='all',
                special='all') -> List[Dict[str, str]]:
    """Every panel of every window this cycle contributes to.

    ``pick()`` is asked before each piece -- the 6-h dashboard, then each
    slice with data -- and the piece is drawn only when it says yes, so
    the shards of a cycle share its pieces.
    """
    pick = pick or (lambda: True)
    items = []
    fam = task['family']
    vlabel = f"{task['vcoord_prefix']}_{_safe(vsel)}"
    stem = (f"{_safe(task['exp_name'])}_{fam}_{_safe(region)}"
            f"{_where_tag(fam, surface, special)}_{_safe(flag)}_"
            f"{varno}_{sel.tag}_{vlabel}")
    panels = task.get('panels', PANELS)

    def _entry(mode, date, paths, subdir):
        for panel, path in paths.items():
            items.append(dict(experience=task['exp_name'], family=fam,
                              mode=mode, panel=panel,
                              region=str(region).split('@')[0],
                              projection=str(region).split('@', 1)[-1],
                              flag=flag, varno=str(varno),
                              land_ocean=surface,
                              special=_sp_label(fam, special),
                              id_stn=sel.display,
                              # a layer in its own section, as in timeserie
                              layer=(str(vsel) if _layer_bounds(fam, vsel)
                                     else 'layer_all'),
                              vcoord=('join' if _layer_bounds(fam, vsel)
                                      else str(vsel)),
                              date=date,
                              filename=f"{subdir}/{os.path.basename(path)}"))

    # the 6-h dashboard: every point of the cycle in one image -- heavy on
    # the radiances (10 to 16 MB on iasi), so only when DASHBOARD_6H asks
    # for it (auto: 4 cycles or fewer)
    subdir6 = f"{fam}_6h"
    if task.get('dashboard_6h') and pick():
        os.makedirs(os.path.join(task['pathwork'], subdir6), exist_ok=True)
        _entry("6h", fdate,
               plot_panels(dfv, fdt - timedelta(hours=3),
                           fdt + timedelta(hours=3),
                           os.path.join(task['pathwork'], subdir6),
                           f"{stem}_{fdate}", ctx6, True, panels), subdir6)

    subdir15 = f"{fam}_{task['interval_min']}min"
    tc = fdt - timedelta(hours=3)
    while tc < fdt + timedelta(hours=3):
        tn = tc + timedelta(minutes=task['interval_min'])
        dfs = dfv[(dfv["datetime"] >= tc) & (dfv["datetime"] < tn)]
        if not dfs.empty and pick():
            ts = tc.strftime("%H%M")
            _entry(f"{task['interval_min']}min", f"{fdate}_{ts}",
                   plot_panels(dfs, tc, tn,
                               os.path.join(task['pathwork'], subdir15),
                               f"{stem}_{fdate}_{ts}", ctx15, False, panels),
                   subdir15)
        tc = tn
    return items


# ─────────────────────────────────────────────────────────────────────────────
# Orchestrator
# ─────────────────────────────────────────────────────────────────────────────

def _report_timing(timing: Dict[str, Any], pathwork: str) -> None:
    sec = timing['seconds']
    print("[mapobs] -------------------- run time --------------------",
          flush=True)
    print(f"[mapobs] input        {_fmt_bytes(timing['input_bytes']):>10s}"
          f"   {timing['input_files']} files, {timing['cycles']} cycles, "
          f"{timing['runs']} run(s)", flush=True)
    for phase in ('scan', 'plots'):
        if phase in sec:
            print(f"[mapobs] {phase:<12s} {sec[phase]:>8.1f} s", flush=True)
    print(f"[mapobs] total        {sec['total']:>8.1f} s   "
          f"({sec['total'] / 60:.1f} min, {timing['n_cpus']} workers)",
          flush=True)
    try:
        with open(os.path.join(pathwork, "mapobs_timing.json"), "w") as fh:
            json.dump(timing, fh, indent=1)
    except OSError as exc:
        print(f"[mapobs] could not write mapobs_timing.json: {exc}",
              file=sys.stderr, flush=True)


def _empty_maps(items, region_info, contexts, pathwork, dt_start, dt_end):
    """One empty map per run, family and region x projection that drew
    nothing, offered for every panel and mode of the family, "*" for the
    rest: the viewer shows every region in every projection, as scatter."""
    import dataclasses
    from pikobs.mapobs.mapobs_plot import plot_empty_map
    have = {(it['experience'], it['family'], it.get('projection'), it['region'])
            for it in items}
    shape: Dict[tuple, Dict[str, set]] = {}
    for it in items:
        g = shape.setdefault((it['experience'], it['family']),
                             {'panels': set(), 'modes': set()})
        g['panels'].add(it['panel'])
        g['modes'].add(it['mode'])
    dress = {}
    for key, (ctx6, _ctx15) in contexts.items():
        dress.setdefault((key[0], key[1]), ctx6)
    out = []
    for (exp, fam), g in sorted(shape.items()):
        base = dress.get((exp, fam))
        if base is None:
            continue
        for tag, (proj, extent, square, name, proj_name) in region_info.items():
            if (exp, fam, proj_name, name) in have:
                continue
            ctx = dataclasses.replace(
                base, proj=proj, extent=extent,
                lon_ext=(extent[0], extent[1]), lat_ext=(extent[2], extent[3]),
                square_map=square, round_map=is_round(proj_name),
                region=f"{name}, {proj_name}", region_lbl=region_label(extent))
            sub = f"{fam}_empty"
            os.makedirs(os.path.join(pathwork, sub), exist_ok=True)
            fname = f"{_safe(exp)}_{fam}_{_safe(tag)}_empty.png"
            plot_empty_map(ctx, os.path.join(pathwork, sub, fname), dt_start,
                           dt_end, f"No observations of {name} in this projection")
            for panel in sorted(g['panels']):
                for mode in sorted(g['modes']):
                    out.append(dict(experience=exp, family=fam, mode=mode,
                                    panel=panel, region=name,
                                    projection=proj_name, land_ocean='*',
                                    flag='*', varno='*', id_stn='*',
                                    special='*', layer='*', vcoord='*',
                                    date='*', filename=f"{sub}/{fname}"))
            print(f"[mapobs] {exp} {fam}: {name} has nothing in {proj_name}, "
                  f"an empty map", flush=True)
    return out


def make_coverage(runs: Sequence[Tuple[str, str]], pathwork: str,
                  datestart: str, dateend: str, families: List[str],
                  flag_criteria: List[str], regions: List[str],
                  id_stn, varno_list=None, vcoord_sel=None,
                  vcoord_prefix: str = "vcoord", interval_min: int = 15,
                  n_cpus: int = 1, build_viewer: bool = True,
                  panels: Sequence[str] = PANELS,
                  svg: bool = False, dashboard_6h: str = "auto",
                  land_ocean=('all',), special_column: str = 'off',
                  pressure_layers=(), height_layers=(),
                  projections=('cyl',)) -> int:
    """Read the cycles, draw the dashboards, write the viewer."""
    regions = _split_tokens(regions)
    flags = _split_tokens(flag_criteria)
    stn_tokens = parse_station_tokens(id_stn)
    vcoord_sel = _split_tokens(vcoord_sel) or ['join']
    land_oceans = [lo for lo in (_split_tokens(land_ocean) or ['all'])
                   if lo in ('all', 'land', 'ocean')] or ['all']
    special_on = str(special_column).strip().lower() in ('on', 'true', '1',
                                                         'yes')

    print(f"[mapobs] runs: {', '.join(n for n, _ in runs)}", flush=True)
    print(f"[mapobs] regions: {regions}", flush=True)
    print(f"[mapobs] flags_criteria: {flags}", flush=True)
    print(f"[mapobs] id_stn tokens: {stn_tokens}", flush=True)
    print(f"[mapobs] {vcoord_prefix} tokens: {vcoord_sel}", flush=True)
    print(f"[mapobs] surface: {land_oceans}  |  special column: "
          f"{'on' if special_on else 'off'}", flush=True)
    panels = [p_ for p_ in (_split_tokens(panels) or list(PANELS))
              if p_ in ALL_PANELS] or list(PANELS)
    print(f"[mapobs] panels: {panels}", flush=True)

    _validate_pathwork(pathwork)
    if not check_input_files(runs, families, datestart, dateend,
                             'mapobs'):
        return 1

    t_start = time.time()
    cycles = _cycles(datestart, dateend)
    n_input, input_bytes = _input_size(runs, families, cycles)
    timing: Dict[str, Any] = {
        'datestart': datestart, 'dateend': dateend, 'cycles': len(cycles),
        'families': list(families), 'runs': len(runs), 'regions': regions,
        'flags': flags, 'id_stn': stn_tokens, 'channel': vcoord_sel,
        'interval_min': interval_min, 'panels': panels, 'svg': svg,
        'land_ocean': land_oceans, 'special_column': special_on,
        'n_cpus': n_cpus, 'input_files': n_input, 'input_bytes': input_bytes,
        'seconds': {},
    }

    if os.path.exists(pathwork):
        shutil.rmtree(pathwork, ignore_errors=True)
    for fam in families:
        os.makedirs(os.path.join(pathwork, f"{fam}_{interval_min}min"),
                    exist_ok=True)

    # regions as (name, extent); the projection comes with them
    # a region chooses the observations, a projection draws the map: each
    # region in each projection, or in the one it names (hrdps:canada)
    combos = _region_combos(regions, _split_tokens(projections) or ['cyl'])
    region_info = {}
    for tag, name, proj_name in combos:
        proj, extent, square = map_projection(proj_name)
        region_info[tag] = (proj, extent, square, name, proj_name)
    region_extents = [(t, region_info[t][1]) for t, _, _ in combos]
    print(f"[mapobs] region x projection: {[t for t, _, _ in combos]}",
          flush=True)

    # what each family says about its vertical coordinate: the SQL
    # expression that builds it, its extra criteria, and its type
    fam_varnos: Dict[str, List[str]] = {}
    fam_vcoord: Dict[str, Tuple[str, str, str]] = {}
    is_channel: Dict[str, Dict[str, bool]] = {}
    for fam in families:
        _, vcoord, vcocrit, _, elem, vcotyp = pikobs.family(fam)
        expr = (vcoord or '').strip() or 'd.vcoord'
        fam_vcoord[fam] = (expr, (vcocrit or '').strip(),
                           (vcotyp or '').strip())
        varnos = ([str(v) for v in varno_list] if varno_list else
                  [v.strip() for v in str(elem).replace("(", "")
                   .replace(")", "").split(",") if v.strip()])
        fam_varnos[fam] = varnos
        chan = vcotyp and vcotyp.upper().startswith('CANAL')
        is_channel[fam] = {v: bool(chan) for v in varnos}
        print(f"[mapobs] {fam}: vcoord = {expr}  ({vcotyp})", flush=True)

    client = None
    dask_dir = None
    if n_cpus > 1:
        os.environ["DASK_LOGGING__DISTRIBUTED"] = "error"
        base = os.environ.get("TMPDIR") or None
        dask_dir = tempfile.mkdtemp(prefix="pikobs_mapobs_dask_", dir=base)
        os.environ["DASK_TEMPORARY_DIRECTORY"] = dask_dir
        dask.config.set({"temporary-directory": dask_dir,
                         "logging.distributed": "error"})
        client = Client(n_workers=n_cpus, threads_per_worker=1,
                        processes=True, silence_logs=50,
                        dashboard_address=None)
    items: List[Dict[str, str]] = []
    try:
        # ---- phase 1: the common scales ----
        scan_tasks = []
        for cycle in cycles:
            for fam in families:
                for name, path in runs:
                    scan_tasks.append({
                        'exp_name': name, 'family': fam,
                        'filein': resolve_rdb_path(path, cycle, fam),
                        'cycle': cycle, 'varnos': fam_varnos[fam],
                        'vcoord_expr': fam_vcoord[fam][0],
                        'vcocrit': fam_vcoord[fam][1],
                        'flags': flags, 'regions': region_extents,
                        'stn_tokens': stn_tokens,
                        'vcoord_sel': _family_vsel(fam, vcoord_sel,
                                                   pressure_layers,
                                                   height_layers),
                        'is_channel': is_channel[fam],
                        'land_oceans': land_oceans,
                        'special_on': special_on,
                        'interval_min': interval_min,
                    })
        t0 = time.time()
        print(f"[mapobs] scan: {len(scan_tasks)} tasks, {n_cpus} worker(s)",
              flush=True)
        res = run_tasks(_scan_task,
                        [({**t, 'pathwork': pathwork},) for t in scan_tasks],
                        client,
                        label='scan')
        timing['seconds']['scan'] = time.time() - t0
        merged = _merge_summaries(res)
        print(f"[mapobs] scan time: {timing['seconds']['scan']:.1f}s "
              f"({len(merged)} groups, "
              f"{sum(r is not None for r in res)}/{len(scan_tasks)} files)",
              flush=True)
        if not merged:
            print("[mapobs] WARNING: nothing to plot, check the selectors.",
                  file=sys.stderr, flush=True)
            return 1

        # ---- contexts, one per group ----
        contexts: Dict[tuple, Tuple[PlotContext, PlotContext]] = {}
        for key, summ in merged.items():
            exp_name, fam, region, flag, varno, stn_tag, vsel, surf, sp = key
            proj, extent, square, reg_name, proj_name = region_info[region]
            v_name, v_unit, v_lab = resolve_type_varno(varno)
            chan = is_channel[fam][varno]
            v_min = summ['v_min'] if summ['v_min'] is not None else 0.0
            v_max = summ['v_max'] if summ['v_max'] is not None else 1.0
            if not chan:
                v_min *= (1 - VRANGE_PAD)
                v_max *= (1 + VRANGE_PAD)
            if abs(v_max - v_min) < 1e-9:
                v_min, v_max = v_min - 1, v_max + 1
            base = dict(
                proj=proj, extent=extent,
                lon_ext=(extent[0], extent[1]), lat_ext=(extent[2], extent[3]),
                square_map=square, round_map=is_round(proj_name),
                vcoord_label=v_lab, var_name=v_name, var_units=v_unit,
                flag_label=flag, family=fam, exp_name=exp_name,
                region=f"{reg_name}, {proj_name}" + _where_txt(fam, surf, sp),
                color_map=build_global_color_map(summ['stations']),
                v_min=v_min, v_max=v_max, is_channel=chan,
                v_orient=vertical_axis_orientation(fam_vcoord[fam][2], chan),
                levels=sorted(summ.get('levels', ())),
                region_lbl=region_label(extent), svg=svg)
            pad6 = tuple(max(1, int(v * (PAD_FACTOR_HIST if i < 3
                                         else PAD_FACTOR_STN)))
                         for i, v in enumerate(summ['six']))
            pad15 = tuple(max(1, int(v * (PAD_FACTOR_HIST if i < 3
                                          else PAD_FACTOR_STN)))
                          for i, v in enumerate(summ['slot']))
            contexts[key] = (PlotContext(max_counts=pad6, **base),
                             PlotContext(max_counts=pad15, **base))

        # ---- phase 2: the dashboards ----
        # one task per cycle kept 12 workers busy out of 80; each cycle is
        # split into shards, about three tasks per worker
        nshard = max(1, -(-3 * max(n_cpus, 1) // max(len(scan_tasks), 1)))
        # the 6-h dashboards: auto draws them for a day or less
        n_cyc = len({t['cycle'] for t in scan_tasks})
        draw6 = (dashboard_6h == 'on'
                 or (dashboard_6h == 'auto' and n_cyc <= 4))
        if dashboard_6h == 'on' and n_cyc > 4:
            print(f"[mapobs] WARNING: DASHBOARD_6H=on over {n_cyc} cycles: "
                  f"every observation of each cycle in one image, the "
                  f"heaviest piece on the radiances -- ask a node with much "
                  f"more memory, or use auto", file=sys.stderr, flush=True)
        print(f"[mapobs] 6-h dashboards: {'on' if draw6 else 'off'} "
              f"(DASHBOARD_6H={dashboard_6h}, {n_cyc} cycle(s))", flush=True)
        slices = max(1, (6 * 60) // max(1, interval_min))
        plot_tasks = []
        for t in scan_tasks:
            # never more shards than pieces to draw: every shard reads the
            # whole cycle, and one that draws nothing read it for nothing
            # (a day of iasi: 60 shards a cycle, most of them empty)
            groups = sum(1 for k in contexts
                         if k[0] == t['exp_name'] and k[1] == t['family'])
            n = max(1, min(nshard, -(-groups * (slices + draw6) // 8)))
            for shard in range(n):
                plot_tasks.append({**t, 'pathwork': pathwork,
                                   'contexts': contexts, 'panels': panels,
                                   'vcoord_prefix': vcoord_prefix, 'svg': svg,
                                   'shard': shard, 'nshard': n,
                                   'dashboard_6h': draw6})
        t0 = time.time()
        print(f"[mapobs] plots: {len(plot_tasks)} tasks "
              f"({len(scan_tasks)} cycles, at most {nshard} shards each)",
              flush=True)
        res = run_tasks(_plot_task, [(t,) for t in plot_tasks], client,
                        label='plots')
        shutil.rmtree(_cache_dir(pathwork), ignore_errors=True)
        timing['seconds']['plots'] = time.time() - t0
        for r in res:
            items += r or []
        # a region with nothing in a projection: one empty map, as scatter
        # does, so that the viewer offers every region in every projection
        items += _empty_maps(items, region_info, contexts, pathwork,
                             datetime.strptime(str(datestart)[:10], "%Y%m%d%H"),
                             datetime.strptime(str(dateend)[:10], "%Y%m%d%H"))
        # one figure per panel; the 6-h ones and the slices apart
        modes = {}
        for it in items:
            modes[it["mode"]] = modes.get(it["mode"], 0) + 1
        kinds = ", ".join(f"{n} {m}" for m, n in sorted(modes.items()))
        print(f"[mapobs] plot time: {timing['seconds']['plots']:.1f}s "
              f"({len(items)} figures: {kinds})", flush=True)
    finally:
        if client is not None:
            try:
                client.close(timeout=30)
            except Exception:
                pass
            try:
                client.shutdown()
            except Exception:
                pass
        if dask_dir:
            shutil.rmtree(dask_dir, ignore_errors=True)

    if not items:
        print("[mapobs] ERROR: no dashboard was produced.", file=sys.stderr,
              flush=True)
        return 1

    if build_viewer:
        from pikobs.configobs.special_family import (
            special_key_label as _special_key)
        keys = ["experience", "family", "panel", "mode", "projection", "region", "land_ocean", "flag",
                "varno", "id_stn", "special", "layer", "vcoord", "date"]
        print(f"[mapobs] viewer selectors: {keys}", flush=True)
        generate_web(
            items, keys, os.path.join(pathwork, "pikobs_mapobs_viewer.html"),
            title="Pikobs Coverage Dashboard",
            subtitle=(
                "Every observation that entered the system in this window, "
                "read from the observation files with no aggregation step, "
                "and always coloured by station. Each panel is its own "
                "figure, so a map stays wide and the vertical distribution "
                "of an interferometer can be as tall as it needs: pick one "
                "in <b>Panel</b>. The 6-hour figures, when there are any "
                "(DASHBOARD_6H: a day or less by default), are the master of "
                f"the cycle; each {interval_min}-minute one zooms into a "
                "sub-interval, which is where a satellite pass or a bursty "
                "platform shows up."),
            enable_play=True,
            key_labels={"land_ocean": "Surface", "layer": "Layer",
                        "projection": "Projection",
                        "special": _special_key(families)})

    timing['seconds']['total'] = time.time() - t_start
    _report_timing(timing, pathwork)
    print(f"[mapobs] done -- output in: {pathwork}", flush=True)
    return 0


# ─────────────────────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────────────────────

def arg_call() -> None:
    import argparse

    p = argparse.ArgumentParser(
        prog="pikobs-mapobs",
        description="Observation coverage dashboards, 6-hour and sub-cycle.")
    p.add_argument('--path_experience_files', '--path_experience', nargs='+',
                   default=[], dest='path_experience_files')
    p.add_argument('--experience_name', nargs='+', default=[])
    p.add_argument('--pathwork', default=None)
    p.add_argument('--datestart', default=None)
    p.add_argument('--dateend', default=None)
    p.add_argument('--region', nargs='+', default=['Monde'],
                   help="the regions of Pikobs, polygons included; "
                        "name:projection draws one in that projection only")
    p.add_argument('--projection', nargs='+', default=['cyl'],
                   help="cyl, robinson, npolar, spolar, orthon, orthos, "
                        "canada, ameriquenord, europe")
    p.add_argument('--family', nargs='+', default=[])
    p.add_argument('--flags_criteria', nargs='+', default=['all'])
    p.add_argument('--id_stn', nargs='+', default=['join'],
                   help="Tokens, one dashboard series each: join, all, "
                        "PREFIX, LIKE%%pattern, =EXACT, 'NAME (codtyp)'.")
    p.add_argument('--varnos', '--varno', nargs='*', default=[],
                   dest='varnos')
    p.add_argument('--vcoord', nargs='+', default=None,
                   help="join (all levels together), all (one per level), "
                        "or an explicit list.")
    p.add_argument('--channel', nargs='+', default=None,
                   help="Alias of --vcoord for satellite channels.")
    p.add_argument('--land_ocean', nargs='+', default=['all'],
                   choices=['all', 'land', 'ocean'],
                   help="all: no filter; land, ocean: one series of "
                        "dashboards each.")
    p.add_argument('--special_column', default='off', choices=['on', 'off'],
                   help="on: one series of dashboards per value of the "
                        "family's special column (sw: the method; ra: "
                        "the elevation); off: all together (default).")
    p.add_argument('--interval_min', type=int, default=15)
    # one set of dashboards per layer: pressure families in hPa, height ones in km
    p.add_argument('--pressure_layers', nargs='*', default=[])
    p.add_argument('--height_layers', nargs='*', default=[])
    p.add_argument('--panels', nargs='+', default=list(PANELS),
                   help="Which panels to draw, each one its own figure: "
                        "map, cross, vertical, stations. Add 'all' for one "
                        "more image with the panels stacked together; "
                        "'--panels all' keeps only that one.")
    p.add_argument('--svg', default='off', choices=['on', 'off'],
                   help="Also write each figure as SVG, next to the PNG, for "
                        "editing before a presentation (default off).")
    p.add_argument('--dashboard_6h', default='auto',
                   choices=['auto', 'on', 'off'],
                   help="6-h dashboards: auto (4 cycles or fewer), on, off")
    p.add_argument('--no_viewer', action='store_true')
    p.add_argument('--n_cpus', '--n_cpu', default=1, type=int, dest='n_cpus')
    p.add_argument('--walltime', default="02:00:00")
    p.add_argument('--no_submit', action='store_true')

    args = p.parse_args()
    for arg in vars(args):
        print(f'--{arg} {getattr(args, arg)}', flush=True)

    if args.channel is not None and args.vcoord is not None:
        raise ValueError("Use only one of --vcoord / --channel "
                         "(they are aliases).")
    if args.channel is not None:
        vcoord_sel, vcoord_prefix = _split_tokens(args.channel), "channel"
    elif args.vcoord is not None:
        vcoord_sel, vcoord_prefix = _split_tokens(args.vcoord), "vcoord"
    else:
        vcoord_sel, vcoord_prefix = ["join"], "vcoord"

    paths = _split_tokens(args.path_experience_files)
    names = _split_tokens(args.experience_name)
    if not paths or not names or len(paths) != len(names):
        raise ValueError("--path_experience_files and --experience_name must "
                         "have the same number of entries")
    if len(set(names)) != len(names):
        raise ValueError(f"experience names must be unique: {names}")
    for attr, flag in [('pathwork', '--pathwork'),
                       ('datestart', '--datestart'),
                       ('dateend', '--dateend'), ('family', '--family')]:
        if getattr(args, attr) in (None, [], 'undefined', ''):
            raise ValueError(f"{flag} is required")

    runs = [(n, p_.rstrip('/') or '/') for n, p_ in zip(names, paths)]
    maybe_submit_to_pbs(args)

    sys.exit(make_coverage(
        runs=runs, pathwork=args.pathwork, datestart=args.datestart,
        dateend=args.dateend, families=_split_tokens(args.family),
        flag_criteria=args.flags_criteria, regions=args.region,
        projections=args.projection,
        id_stn=args.id_stn, varno_list=_split_tokens(args.varnos) or None,
        vcoord_sel=vcoord_sel, vcoord_prefix=vcoord_prefix,
        interval_min=args.interval_min, n_cpus=args.n_cpus,
        build_viewer=not args.no_viewer, panels=args.panels,
        svg=svg_enabled(args.svg), dashboard_6h=args.dashboard_6h,
        land_ocean=args.land_ocean, special_column=args.special_column,
        pressure_layers=[float(x) for x in _split_tokens(args.pressure_layers)],
        height_layers=[float(x) for x in _split_tokens(args.height_layers)]))


if __name__ == "__main__":
    arg_call()
