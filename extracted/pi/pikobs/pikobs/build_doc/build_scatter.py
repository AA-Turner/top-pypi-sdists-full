"""Build the scatter.py module docstring from the two wrappers.

    python build_doc.py pikobs/scatter/scatter.py pikobs/script [runtime_table.rst]

scatter.py      module whose docstring is replaced
script dir      directory holding run_scatter_exp.sh / run_scatter_cont_exp.sh
                (their USER SETTINGS blocks are copied into the doc)
runtime table   optional output of scatter_timing_table.py, shown in the
                "Run time" section
"""
import os as _os_dw, sys as _sys_dw  # noqa: E401
_sys_dw.path.insert(0, _os_dw.path.dirname(_os_dw.path.abspath(__file__)))
from docwrite import write_docstring  # noqa: E402
import os
import re
import sys

if len(sys.argv) < 3:
    sys.exit(__doc__)
SCATTER = sys.argv[1]
OUT = sys.argv[2]
RUNTIME_FILE = sys.argv[3] if len(sys.argv) > 3 else None


def user_settings(path):
    txt = open(path).read()
    a = txt.index("# 1. USER SETTINGS")
    a = txt.index("\n", txt.index("# ====", a)) + 1
    b = txt.index("# ====", a)
    block = txt[a:b].strip("\n")
    return "\n".join("   " + l if l else "" for l in block.splitlines())


def grid(headers, rows):
    """reStructuredText grid table."""
    cols = list(zip(*([headers] + rows)))
    widths = [max(len(c) for c in col) for col in cols]
    sep = "+" + "+".join("-" * (w + 2) for w in widths) + "+"
    hsep = sep.replace("-", "=")

    def line(r):
        return "|" + "|".join(f" {c:<{w}} " for c, w in zip(r, widths)) + "|"

    out = [sep, line(headers), hsep]
    for r in rows:
        out += [line(r), sep]
    return "\n".join(out)


def image(name, alt):
    return (f".. image:: _static/{name}\n"
            f"   :alt: {alt}\n"
            f"   :align: center\n"
            f"   :width: 100%")


VARIABLES = grid(
    ["Variable", "Wrapper", "What it does"],
    [
        ["``PATH_CONTROL_FILES``", "cont_exp", "Directory of the control run (the reference)"],
        ["``CONTROL_NAME``", "cont_exp", "Name of the control in titles and in the viewer"],
        ["``PATH_EXPERIENCE_FILES``", "both", "One or more run directories (array)"],
        ["``EXPERIENCE_NAME``", "both", "One name per directory, same order (array)"],
        ["``PATHWORK``", "both", "Output directory, wiped per family at each run"],
        ["``DATESTART`` / ``DATEEND``", "both", "Period, ``YYYYMMDDHH`` UTC, both ends included"],
        ["``REGION``", "both", "Regions: boxes and polygons, see :doc:`regions` (array)"],
        ["``FAMILY``", "both", "Observation families (array)"],
        ["``FLAGS_CRITERIA``", "both", "Flag filters, ``all`` = no filter (array)"],
        ["``FONCTION``", "both", "Functions to map, see section 4 (array)"],
        ["``VARNOS``", "both", "Optional varno list, empty = family default"],
        ["``BOXSIZEX`` / ``BOXSIZEY``", "both", "Box size in degrees of longitude / latitude"],
        ["``PROJECTION``", "both", "Map projection(s) (array)"],
        ["``PRESSURE_LAYERS``", "both", "Layer edges in hPa, for the families on pressure (ua ai sw ch)"],
        ["``HEIGHT_LAYERS``", "both", "Layer edges in km, for the families on height (ro radar)"],
        ["``ID_STN``", "both", "Station grouping tokens, see section 3 (array)"],
        ["``CHANNEL``", "both", "Channel / vcoord tokens, see section 3 (array)"],
        ["``POINTS``", "both", "``ON`` writes the obs count in each box"],
        ["``SPECIAL_COLUMN``", "both", "``on``: one map per special value (wind method...)"],
        ["``MATCH``", "cont_exp", "``on`` tests the change on the observations both runs hold, ``off`` on each run with all of its own"],
        ["``N_CPUS``", "both", "Number of Dask workers"],
    ])

STN_TOKENS = grid(
    ["Token", "Maps produced"],
    [
        ["``join``", "one map, every station merged"],
        ["``all``", "one map per station"],
        ["``CAS`` or ``\"CAS*\"``", "one map with every station whose id starts with CAS"],
        ["``C%``", "SQL ``LIKE`` pattern on the station id, used as given"],
        ["``=NENE``", "station NENE only"],
        ["``\"AMDAR (42)\"``", "every station of codtyp 42"],
    ])

CODTYP_TOKENS = grid(
    ["Token", "Result (ua)"],
    [
        ["``all``", "one map per codtyp present: PILOT (32), TEMP (35), ..."],
        ["``pilot``", "PILOT, PILOT SHIP, PILOT MOBIL merged: ``PILOT* (32,33,34)``"],
        ["``=PILOT``", "PILOT (32) only"],
        ["``temp_ship``", "TEMP SHIP and TEMP SHIP + PILOT SHIP: ``TEMP SHIP* (36,139)``"],
        ["``35``", "TEMP (35)"],
        ["``71627``", "not a codtyp: station id prefix"],
        ["``12%``", "station ids starting with 12 (sf, where 12 is SYNOP)"],
    ])

CHAN_TOKENS = grid(
    ["Token", "Maps produced"],
    [
        ["``join``", "all channels / levels merged"],
        ["``all``", "one map per channel / level"],
        ["``32 40``", "channels 32 and 40 only, one map each"],
    ])

SINGLE_FUNCS = grid(
    ["Function", "Box value", "Colours"],
    [
        ["``omp``", "mean O-B", "blue < 0 < red, white near 0"],
        ["``oma``", "mean O-A", "blue < 0 < red, white near 0"],
        ["``stdomp``", "standard deviation of O-B", "light to dark"],
        ["``stdoma``", "standard deviation of O-A", "light to dark"],
        ["``obs``", "mean observed value", "blue to red"],
        ["``bcorr``", "mean bias correction (radiances only)", "blue to red"],
        ["``nobs``", "observations per day", "viridis"],
        ["``dens``", "observations per km² per day", "viridis"],
    ])

DIFF_FUNCS = grid(
    ["Function", "Box value (experience - control)", "Red means", "Observations", "Test"],
    [
        ["``omp``, ``oma``", "``|bias_exp| - |bias_ctl|``, units", "negative: exp better", "common", "paired t and Pitman-Morgan"],
        ["``stdomp``, ``stdoma``", "``100 (σ_exp - σ_ctl) / σ_ctl``", "negative: exp better", "common", "Pitman-Morgan"],
        ["``bcorr``", "``100 (|bc_exp| - |bc_ctl|) / |bc_ctl|``", "positive: larger", "all", "none"],
        ["``obs``", "``obs_exp - obs_ctl``, units", "positive: higher", "all", "none"],
        ["``nobs``, ``dens``", "``100 (N_exp - N_ctl) / N_ctl``", "positive: more obs", "all", "none"],
    ])

PANELS = grid(
    ["Map", "File suffix", "Content"],
    [
        ["``difference``", "``_<ctl>_vs_<exp>.png``", "every box, blue / white / red"],
        ["``significance``", "``..._signif.png``", "test confidence, 0 to 100 %"],
        ["``significant only``", "``..._sigonly.png``", "difference map, boxes above 95 % only"],
    ])

TROUBLE = grid(
    ["Symptom", "Cause and fix"],
    [
        ["``ERROR: missing 6-h input files``",
         "At least one ``YYYYMMDDHH_<family>`` is missing; the report lists the gaps and the dates available. Fix the period or the path."],
        ["``PATH_EXPERIENCE_FILES (2) and EXPERIENCE_NAME (1)``",
         "The two arrays must have the same length."],
        ["Paths glued together, missing files",
         "A list was written as a string: use ``FAMILY=(sw ai)``, not ``FAMILY=\"sw ai\"``."],
        ["``id_stn 'xyz*' matches no data``",
         "The token matched nothing for the selected channels; the log line above it shows how it was resolved."],
        ["Low ``common obs`` percentage",
         "The runs do not hold the same observations: more channels or platforms in one of them, other thinning, or positions written differently. Compare one cycle with ``sqlite3`` (section 9.1)."],
        ["``observation key not unique``",
         "Some observations share station, date, time, position, channel and varno in one file; they are left out of the comparison. A few are harmless; many mean the key misses a field for that family."],
        ["``WARNING: n/N ... tasks lost, KilledWorker``",
         "A worker ran out of memory. The other maps are still produced. Use fewer workers (``N_CPUS``) or explicit channels instead of ``join`` / ``all``."],
        ["No *Difference / Significance* selector",
         "Only with a control, and only for omp, oma, stdomp, stdoma: pick one of them in *Function* (the page opens on the first function alphabetically)."],
        ["No bcorr maps",
         "The family has no ``BIAS_CORR`` column (non-radiance); the log says so once."],
        ["Almost nothing significant",
         "Few observations per box. Use larger boxes (5° or 10°) or a longer period."],
        ["Formulas missing in the web page",
         "``sphinx.ext.mathjax`` is not in ``docs/source/conf.py``, or the browser cannot load MathJax."],
        ["The page shows old maps",
         "Browser cache: reload with Ctrl+Shift+R."],
    ])

DOC = r'''
================================================================
pikobs.scatter -- Geographic Tiled Observation Statistics
================================================================

``scatter`` answers a question that global scores hide: *where* do the
observations behave differently? It cuts the globe into longitude /
latitude boxes, gathers every observation that falls in a box over the
period, and paints the box with the statistic you ask for: O-B, O-A,
their sigma, the observed value, the bias correction, or simply how many
observations arrived.

Quick start
===========

Download the wrapper you need. Take it from GitLab every time you start a
new study: the copy there follows the options of the installed module.

.. code-block:: bash

   # one or several experiences, single-run maps
   wget https://gitlab.science.gc.ca/dlo001/Pikobs/-/raw/master/pikobs/script/run_scatter_exp.sh
   chmod +x run_scatter_exp.sh

   # control against one or several experiences
   wget https://gitlab.science.gc.ca/dlo001/Pikobs/-/raw/master/pikobs/script/run_scatter_cont_exp.sh
   chmod +x run_scatter_cont_exp.sh

The wrappers run on the node you are on and never submit to PBS, so open a
compute node first, edit the ``USER SETTINGS`` block and launch:

.. code-block:: bash

   qsub -I -lselect=1:ncpus=80:mem=185gb -lwalltime=2:0:0
   nano run_scatter_cont_exp.sh
   ./run_scatter_cont_exp.sh

.. warning::

   Do not run the wrappers on a login node. The aggregation opens every
   6-h file of the period in parallel.

.. important::

   Lists are **bash arrays**: ``FAMILY=(sw ai)`` and not
   ``FAMILY="sw ai"``. The wrappers pass them as ``"${FAMILY[@]}"``; a
   plain string arrives glued and ends in "missing file" errors.
   Quote any token with a ``*`` or a space, otherwise bash expands or
   splits it: ``ID_STN=(join "CAS*" "AMDAR (42)")``.

A comparison run prints something like this:

.. code-block:: text

   [scatter] runs: control, experience
   [scatter] comparisons: control vs experience
   [scatter] id_stn tokens: ['all']
   [scatter] channel tokens: ['32']
   [scatter] input check OK: 21 cycles x 2 run(s) x 1 family(ies), 42 files, 61.3 GB
   [scatter] aggregation: 84 tasks, 80 worker(s)
   [scatter] aggregation time: 190.2s (84/84 files aggregated)
   [scatter] matching control and experience: 42 tasks
   [scatter] matching time: 214.7s (42/42 tasks)
   [scatter]   iasi experience: 18204417 common obs (96.2% of control, 95.8% of experience)
   [scatter] compaction time: 38.1s (6/6 databases)
   [scatter] plots: 36 tasks, 80 worker(s)
   [scatter] plot time: 58.4s (36/36 maps written)
   [scatter]   difference       maps: 16/16
   [scatter]   significance     maps: 10/10
   [scatter]   significant only maps: 10/10
   [scatter] viewer selectors: ['experience', 'family', 'region', 'flag', 'function', 'panel', ...]
   [viewer] wrote /home/dlo001/sites8/pikobs_scatter_cont_exp/pikobs_scatter_viewer.html  (36 items, 11 keys)
   Viewer: /home/dlo001/sites8/pikobs_scatter_cont_exp/pikobs_scatter_viewer.html
   Web:    https://goc-dx-u3.science.gc.ca/~dlo001/sites8/pikobs_scatter_cont_exp/pikobs_scatter_viewer.html
   [scatter] ------------------- run time -------------------
   [scatter] input           61.3 GB   42 files, 21 cycles, 2 run(s)
   [scatter] aggregation    190.2 s
   [scatter] matching       214.7 s
   [scatter] compaction      38.1 s
   [scatter] plots           58.4 s   36 maps
   [scatter] total          503.9 s   (8.4 min, 80 workers)
   [scatter] done -- output in: /home/dlo001/sites8/pikobs_scatter_cont_exp

The ``Viewer`` and ``Web`` lines come from the module, whichever way it
was launched. If a link in ``~/public_html`` already shows the folder --
one ``sites8 -> ~/sites8`` covers every run under it -- the address goes
through that link; otherwise the run prints the one ``ln -s`` that would
make the page reachable.

How long a run takes, and how big a node to ask for: :doc:`runtime`.

----

When to use which wrapper
=========================

I reach for it in two situations. The first is a look at one run. A new
channel selection goes in, a blacklist changes, a satellite comes back, and
before trusting any global number I want to see the O-B pattern on a map.
The second is a comparison. A parallel suite against the operational one,
box by box, with a statistical test behind every coloured box, because a
2° box over the Southern Ocean that received a dozen observations can turn
red for no reason at all.

Each situation has its own wrapper:

* ``run_scatter_exp.sh`` draws one or several experiences, each on its own
  maps;
* ``run_scatter_cont_exp.sh`` compares one control with one or several
  experiences and draws, for every comparison, a difference map plus two
  significance maps.

Both end in the same HTML viewer, so hundreds of maps can be flipped through
from dropdowns instead of opening PNG files one by one.

__IMG_EXP_OMP__

Live examples, made with the two wrappers:

* `single run <https://goc-dx-u3.science.gc.ca/~dlo001/sites8/pikobs_doc_scatter_exp/pikobs_scatter_viewer.html>`__
* `control vs experience <https://goc-dx-u3.science.gc.ca/~dlo001/sites8/pikobs_doc_scatter/pikobs_scatter_viewer.html>`__

----

1. How it works
===============

The run goes through six steps.

**Input check.** Before anything else, every 6-h file
``<path>/YYYYMMDDHH_<family>`` of the period is looked up, for the control
and for every experience. If a single one is missing the run stops, says
which cycles are missing (grouped in ranges) and which dates the directory
does contain. ``PATHWORK`` is not touched in that case, so a typo in the
dates does not erase the maps of the previous run.

**Aggregation.** Each 6-h file is read in parallel and reduced to sums per
box: :math:`\sum x`, :math:`\sum x^2` and :math:`N` for O-B, O-A, the
observed value and the bias correction. A box is identified by

.. math::

   b = \left\lfloor \frac{360}{\Delta x} \right\rfloor
       \left\lfloor \frac{\varphi}{\Delta y} \right\rfloor
     + \left\lfloor \frac{\min(179.99,\ \lambda)}{\Delta x} \right\rfloor

with :math:`\Delta x, \Delta y` the box size, :math:`\varphi` the latitude
and :math:`\lambda` the longitude. The sums are kept per station, per
channel and per special value only when the ``ID_STN`` / ``CHANNEL``
tokens need it, and the list of stations that contributed is saved
separately so the titles can name them.

**Matching** (comparison runs only). For ``omp``, ``oma``, ``stdomp``,
and ``stdoma`` the two runs are compared on the *same*
observations. Each 6-h file of the control is joined with the same file of
the experience on

.. code-block:: text

   ID_STN + DATE + TIME + ROUND(LAT, 4) + ROUND(LON, 4) + VCOORD + VARNO

Both runs go through the same filters, and each run's flags are checked on
its own data, so a pair exists only when the observation passes the flag
criterion in both. A key that appears more than once in a file is not
dropped: its observations are paired one to one, in order. ``MATCH``
decides all this -- ``on`` for this key, a list of fields for another,
``off`` to compare every observation of each run, with Welch and F
tests -- see :doc:`match`. The
pair database keeps, per box, the number of pairs and
:math:`\sum x`, :math:`\sum y`, :math:`\sum x^2`, :math:`\sum y^2`,
:math:`\sum xy` (:math:`x` control, :math:`y` experience). The log says how
much was matched:

.. code-block:: text

   [scatter]   iasi experience: 18204417 common obs (96.2% of control, 95.8% of experience)

Two suites fed with the same observations should be close to 100 %. A low
figure means the runs do not hold the same observations (other channels,
other platforms, other thinning); the comparison is then limited to what
they share, while ``nobs`` and ``dens`` still use everything.

**Compaction.** The maps never need the cycle, so every database is summed
over the period and indexed before plotting. This keeps the plotting
queries small even with 120 cycles of a hyperspectral instrument.

**Maps.** Every statistic is derived from those sums, so one aggregation
feeds every function, projection and grouping. For a box with :math:`N`
observations :math:`x_i`:

.. math::

   \bar{x} = \frac{1}{N}\sum_{i=1}^{N} x_i ,
   \qquad
   \sigma = \sqrt{\max\left(0,\ \frac{1}{N}\sum_{i=1}^{N} x_i^2 - \bar{x}^2\right)}

``dens`` divides the daily count by the box area on the sphere,

.. math::

   A = R^2 \,\left|\sin\varphi_2 - \sin\varphi_1\right|\, |\lambda_2 - \lambda_1|,
   \qquad R = 6371\ \mathrm{km}

and the number of days counts every cycle as 6 h, so ``2026091000`` to
``2026091500`` is 5.25 days.

**Viewer.** All maps are indexed in ``pikobs_scatter_viewer.html``
(section 6).

The module is two files. ``scatter.py`` reads the observations -- the
input check, the aggregation, the matching, the compaction -- and
``scatter_plot.py`` draws. That is what lets a colour, a title or a
colour bar be changed without reading a single database again.

----

2. Configuration
================

Everything is set in the ``USER SETTINGS`` block at the top of the wrapper
you downloaded: ``run_scatter_exp.sh`` maps one or more runs on their own,
``run_scatter_cont_exp.sh`` compares one or more experiences with a
control. The two share every setting except the control. Lists are bash
arrays: ``FAMILY=(iasi cris)``, not ``FAMILY="iasi cris"``.

.. wrapper-settings:: run_scatter_exp.sh run_scatter_cont_exp.sh

With several experiences, ``PATH_EXPERIENCE_FILES`` and
``EXPERIENCE_NAME`` are arrays of the same length:

.. code-block:: bash

   PATH_EXPERIENCE_FILES=(/path/to/E22 /path/to/E23)
   EXPERIENCE_NAME=(E22 E23)

``run_scatter_exp.sh`` then draws E22 and E23 separately;
``run_scatter_cont_exp.sh`` draws *control vs E22* and *control vs E23*.

----

3. Choosing stations and channels
=================================

``ID_STN`` and ``CHANNEL`` decide how many maps come out. Each token is a
separate series of maps, and both combine: ``ID_STN=(all)`` with
``CHANNEL=(all)`` gives one map per station and per channel.

Stations
--------

__STN_TOKENS__

Tokens mix freely. ``ID_STN=(join all CAS SER)`` gives one merged map, one
map per station, one for the CAS stations and one for the SER stations.

When a map covers a group (``join``, a prefix, a pattern or a codtyp), the
title says how many stations went into it and lists them, cut after 15
names. Filenames tag the groups so that they never collide with a station
of the same name: ``CAS_grp`` for a prefix, ``NENE_eq`` for an exact id,
``Cpct`` for ``C%``, ``codtyp_32-33`` for a codtyp group.

For ai, sf, ua, gp and csr the tokens name instrument types rather than
stations -- ``pilot``, ``=TEMP``, ``35`` -- the same way in every module;
see :doc:`families`.

Channels and vertical coordinates
---------------------------------

``CHANNEL`` (``--vcoord`` is an alias on the command line):

__CHAN_TOKENS__

``CHANNEL=(join 32)`` gives the merged map and the channel 32 map.

Layers
------

A family whose vertical coordinate is a pressure or a height gets one
series of maps per layer, on top of the series with the whole column.
The edges are read in the unit of that coordinate:

.. code-block:: bash

   PRESSURE_LAYERS=(1100 850 500 250 100 10 1 0)   # hPa: ua ai sw ch
   HEIGHT_LAYERS=(0 5 10 20 30 40 60 100)          # km:  ro radar

Each family reads the list of its own coordinate, so ``FAMILY=(sw ro)``
in one run gives sw in hPa layers and ro in km layers, each labelled in
its own unit. A radiance takes neither: a channel is a named thing and
is chosen with ``CHANNEL``. An empty list means the whole column, in one
series.

A layer holds its top edge, so 500 hPa falls in ``500-250 hPa`` and
never in two layers at once, and the label carries its rank from the
ground -- ``2 | 850-500 hPa`` -- so the viewer lists them by height and
not alphabetically, where 1000 would come before 500.

The run prints what each family will do before it starts:

.. code-block:: text

   [scatter] sw: 1 | 1100-850 hPa, 2 | 850-500 hPa, 3 | 500-250 hPa, ...
   [scatter] ro: 1 | 0-5 km, 2 | 5-10 km, 3 | 10-20 km, ...
   [scatter] cris: the whole column in one series

A layer with no observation in it simply has no map, and the log says
which one: the AMVs of ``sw`` stop below 100 hPa, and GPS-RO above
40 km, so the top layers of each are empty and that is the right
answer.

Surface and special column
--------------------------

Two more settings split the maps. Both are off by default, as in every
module.

``LAND_OCEAN=(all land ocean)`` draws each map three times: everything,
land only, sea only. The mask is the one every module uses
(``global_land_mask``, nearest cell) and it is applied to each
observation before it is summed, so a coastal box can show up on both
maps, each time with its own observations. The name carries ``_land``
or ``_ocean`` right after the region, and the viewer gets a *Surface*
selector.

``SPECIAL_COLUMN="on"`` splits a family by its special column: the wind
method for ``sw`` (IR channel, water vapour channel...), the antenna
elevation for radar. Two populations with different errors then stop
averaging each other out. The label follows the surface in the name --
``..._Monde_land_IR_channel_...`` -- and the viewer gets its selector
(*Method* for ``sw``). A family without a special column is drawn as
usual.

----

4. Single-run maps
==================

``run_scatter_exp.sh`` draws every experience on its own. The colour scale
of each map is set from its own values.

__SINGLE_FUNCS__

For ``omp`` and ``oma`` the scale is symmetric, built from steps like
0.05, 0.1, 0.2, 0.3, 0.5, 1 chosen so that the last one covers 95 % of the
boxes; the white band around zero is the first step. The box at the top
right gives the mean over the boxes (:math:`\bar{\mu}`,
:math:`\bar{\sigma}`) and the number of observations drawn, and the title
gives the variable, the station group, the channel and the layer. The
``omp`` map is the one at the top of this page; the others look like this:

__IMG_EXP_OMA__

__IMG_EXP_STDOMP__

__IMG_EXP_OBS__

__IMG_EXP_NOBS__

__IMG_EXP_DENS__

__IMG_EXP_BCORR__

``bcorr`` exists only for radiance families. When the files have no
``BIAS_CORR`` column the maps are skipped and the log says it once.

----

5. Control vs experience maps
=============================

``run_scatter_cont_exp.sh`` does not show two sets of absolute values. It
shows, box by box, **experience minus control**. The direction and the
tests are the ones of ``pikobs.stats``, shared with the other comparison
modules, so a map and a channel plot of the same experiment tell the same
story.

__DIFF_FUNCS__

For the departures the question is whether the experience gets closer to
zero, so the bias is compared in absolute value:

.. math::

   \Delta_{\mathrm{bias}} = \left|\bar{d}_{\mathrm{exp}}\right|
                          - \left|\bar{d}_{\mathrm{ctl}}\right|
   \qquad
   \Delta_{\sigma} = 100\,\frac{\sigma_{\mathrm{exp}} - \sigma_{\mathrm{ctl}}}
                               {\sigma_{\mathrm{ctl}}}

For these two a **negative value is an improvement, and it is drawn in
red**. A box at -12 on a ``stdomp`` map means the experience has a 12 %
smaller O-B sigma there. Positive values, the experience doing worse, are
blue. The colour bar says it too, formula included: for the bias,
*negative / red = Exp bias closer to zero*; for sigma,
*negative / red = Exp better*.

For the other functions the sign simply follows the change: more
observations, a higher observed value or a larger correction are red.

.. math::

   \Delta_{N} = 100\,\frac{N_{\mathrm{exp}} - N_{\mathrm{ctl}}}{N_{\mathrm{ctl}}}
   \qquad
   \Delta_{\mathrm{bcorr}} = 100\,\frac{\left|b_{\mathrm{exp}}\right|
                                    - \left|b_{\mathrm{ctl}}\right|}
                                   {\left|b_{\mathrm{ctl}}\right|}

The bias correction :math:`b` can be negative, so its size is compared. In
regions where the control barely corrects anything the percentage gets
large and saturates at ±100 %; read those boxes with the single-run
``bcorr`` map at hand.

Why not a percentage for the bias? It would divide by a control bias that
is often close to zero: a box going from 0.01 K to 0.03 K is +200 % and
means nothing.

The colour scale is symmetric, uses steps such as 0.05, 0.1, 0.2, 0.3, 0.5,
1, and is set on the significant boxes, so a few boxes with a handful of
observations do not stretch it. Percentages are capped at ±100 %; beyond
the last step a box takes the darkest colour.

Three maps per comparison
-------------------------

For ``omp``, ``oma``, ``stdomp`` and ``stdoma`` every comparison
produces three maps, switched with the *Difference / Significance*
selector of the viewer:

__PANELS__

``obs``, ``bcorr``, ``nobs`` and ``dens`` only have the difference map,
computed on all the observations of each run.

The examples are O-A (``oma``); the section *Two passes of the same
cycle* below says why.

**difference** shows every box:

__IMG_CMP_OMP_DIFFERENCE__

**significance** shows how sure the test is, from 0 to 100 %. Grey boxes
stay at or below 95 % (darker when closer), orange ones are above 95 % and
red ones above 99 %; the thick line on the colour bar marks 95 %. For
``omp`` and ``oma``, a crossed box (``xxx``) passed both tests but its bias
and sigma moved in opposite directions, so it is not counted. The box at
the top right recalls which test was run and counts the significant boxes:

__IMG_CMP_OMP_SIGNIFICANCE__

**significant only** is the difference map with the same colours and the
same scale, where only the boxes that pass are drawn (for ``omp`` / ``oma``:
both tests, same direction). It is usually the
one to show in a meeting:

__IMG_CMP_OMP_SIGONLY__

The same for sigma:

__IMG_CMP_STDOMP_DIFFERENCE__

__IMG_CMP_STDOMP_SIGONLY__

and the change in the number of observations, which has no test:

__IMG_CMP_NOBS_DIFFERENCE__

What decides a box
------------------

The tests, their formulas, the worked example and the reason a paired
test sees changes an independent one misses are in :mod:`pikobs.stats`,
which every comparison module shares. On a map:

* ``stdomp`` and ``stdoma`` are decided by the **Pitman-Morgan test** on sigma alone.
* ``omp`` and ``oma`` need the **paired t-test** on the bias *and* the
  Pitman-Morgan test on sigma, both above 95 %, and both changes pointing the same
  way: bias and sigma better gives a red box, both worse a blue one.
  When they disagree the box is crossed on the significance map and left
  out of the significant-only one -- a background that aims better but
  shakes more has not improved.
* ``obs``, ``bcorr``, ``nobs`` and ``dens`` have no test: they are
  differences, not verdicts.

Two things to keep in mind while reading a map, both of which pull in
opposite directions. Observations inside a box are not independent -- one
satellite pass, one cycle -- which makes both tests look more certain
than they are. And a map has thousands of boxes, so at 95 % about one in
twenty passes by chance: on 14 000 boxes that is 700. An isolated
significant box proves nothing; a region of them, all the same colour,
does.

Black boxes
-----------

A black box cannot be compared: it has observations in the control or in
the experience, but none in common (for ``obs``, ``nobs`` and ``dens``:
data in only one of the two runs). Black boxes point to a coverage change,
a channel switched off, a new platform, a different blacklist, not to a
score. The box at the top right counts them.

The same box gives the number of observations of each run on the map, all
of them, and how many were compared, for example
``common obs compared: 18204417 (96% of ctl)``.

Two passes of the same cycle
----------------------------

The first time I compared G0 and G2 the ``omp`` map came out white, every
box of it, and the colour bar stopped at 0.00002 K. Nothing was broken.
G0, G1 and G2 are passes of the same operational cycle: G0 goes first with
a short cut-off, G1 (00 and 12 UTC only) and G2 later, with more
observations -- half as many IASI radiances again in G2. They start from
the same background, so an observation that two passes both have gets the
same O-B in each, to the last bit. On six days of assimilated IASI the
sums of the pair database were identical to the last digit, over 13
million pairs. There is nothing to compare.

The analysis is where they part. With more observations G2 lands
somewhere else, and O-A shows it:

+-------+-----------+-----------+-------------------------+
| O-A   | G0 (Ctl)  | G2 (Exp)  | change                  |
+=======+===========+===========+=========================+
| bias  | -0.0129 K | -0.0112 K | 0.0017 K closer to zero |
+-------+-----------+-----------+-------------------------+
| sigma | 0.4017 K  | 0.4002 K  | -0.38 %                 |
+-------+-----------+-----------+-------------------------+

Small, and 13 million pairs are enough for the tests to see it. That is
why the comparison maps on this page are O-A. To look at O-B, compare two
runs with backgrounds of their own -- an experiment against the operational
suite -- never two passes of one cycle.

When few observations are compared
----------------------------------

The ``common obs compared`` line is worth a look before any colour. Two
suites fed with the same observations reach 95 % or more; 8 % means
they did not keep the same ones -- other channels, other platforms,
another thinning -- and the maps then speak for that small shared part
only. One cycle of both runs is enough to see which:

.. code-block:: bash

   c=<PATH_CONTROL_FILES>/2026091000_cris
   e=<PATH_EXPERIENCE_FILES>/2026091000_cris
   sqlite3 -header -column :memory: <<EOF
   ATTACH '$c' AS c;  ATTACH '$e' AS e;
   SELECT 'ctl' AS run, id_stn, COUNT(*) AS nobs, COUNT(DISTINCT vcoord) AS nchan
     FROM c.header NATURAL JOIN c.data GROUP BY id_stn
   UNION ALL
   SELECT 'exp', id_stn, COUNT(*), COUNT(DISTINCT vcoord)
     FROM e.header NATURAL JOIN e.data GROUP BY id_stn;
   SELECT COUNT(*) AS common_pixels FROM
     (SELECT DISTINCT id_stn,date,time,ROUND(lat,4) a,ROUND(lon,4) b FROM c.header)
     JOIN (SELECT DISTINCT id_stn,date,time,ROUND(lat,4) a,ROUND(lon,4) b FROM e.header)
     USING (id_stn,date,time,a,b);
   EOF

More channels or platforms on one side explain a low figure and are fine.
Few common pixels mean the suites did not select the same observations.

----

6. The web viewer
=================

Open ``$PATHWORK/pikobs_scatter_viewer.html`` in a browser, no server
needed, or the web address printed at the end of the run. The page starts
with a short explanation of the maps, written for the mode of the run
(single run or comparison), then a row of dropdowns:

* **Experience** (single run) or **Comparison** (control vs experience),
  always first;
* Family, Region, Surface, Flag, Function;
* **Difference / Significance**, only in comparison runs;
* Layer, Varno, Vcoord / Channel, Projection, Station, and the special
  column (*Method* for ``sw``) when ``SPECIAL_COLUMN="on"``.

Each dropdown only offers what exists for the choices on its left. The
page opens on the first function in alphabetical order, often ``bcorr`` or
``dens``; pick ``omp`` to see the significance maps. The **Flip** button
(key ``F``) toggles between the current map and the previous one, which is
the quickest way to go from *difference* to *significant only*, or from
one experience to the next with everything else fixed. A click on the map
opens it at full size.

----

7. Output layout
================

::

   $PATHWORK/
   ├── pikobs_scatter_viewer.html
   └── <family>/
       ├── scatter_<layer>_<run>_<region>[_<surface>]_<start>_<end>_bx<X>_by<Y>_<flag>_<family>.db
       ├── scatter_pair_<layer>_<control>_vs_<exp>_<region>[_<surface>]_..._<flag>_<family>.db
       ├── <fn>_<proj>_layer_<edges><unit>_flag_<flag>_id_stn_<stn>_<region>[_<surface>][_<special>]_vcoord_<vc>_varno<varno>_<run>.png
       ├── <fn>_..._<control>_vs_<exp>.png            difference
       ├── <fn>_..._<control>_vs_<exp>_signif.png     significance
       └── <fn>_..._<control>_vs_<exp>_sigonly.png    significant only

With ``SVG="on"`` each figure is written again as ``.svg`` beside its PNG,
for editing before a presentation: in Inkscape or Illustrator the titles,
the legends and the colours stay editable. The viewer always uses the PNG,
so turning it on changes nothing else. An SVG keeps every element of the
figure, so ask for it on the one or two figures you actually need.

The ``scatter_*.db`` files hold the per-box sums of each run (tables
``moyenne`` and ``stations``), the ``scatter_pair_*.db`` files the sums of
the common observations (table ``pairs``, columns ``n_omp``, ``sx_omp``,
``sy_omp``, ``sxx_omp``, ``syy_omp``, ``sxy_omp`` and the same with
``oma``). Both can be queried with ``sqlite3``. ``PATHWORK/<family>``
is wiped at the start of every run that passes the input check.

----

8. Support
==========

Bugs and feature requests:
   `<https://gitlab.science.gc.ca/dlo001/Pikobs/-/issues>`_
'''

IMAGES = {
    "__IMG_EXP_OMP__": ("scatter_exp_omp.png", "Single-run OMP map"),
    "__IMG_EXP_OMA__": ("scatter_exp_oma.png", "Single-run OMA map"),
    "__IMG_EXP_STDOMP__": ("scatter_exp_stdomp.png", "Single-run STD(OMP) map"),
    "__IMG_EXP_OBS__": ("scatter_exp_obs.png", "Single-run observed value map"),
    "__IMG_EXP_NOBS__": ("scatter_exp_nobs.png", "Single-run observation count map"),
    "__IMG_EXP_DENS__": ("scatter_exp_dens.png", "Single-run density map"),
    "__IMG_EXP_BCORR__": ("scatter_exp_bcorr.png", "Single-run bias correction map"),
    "__IMG_CMP_OMP_DIFFERENCE__": ("scatter_cmp_oma_difference.png", "O-A difference map"),
    "__IMG_CMP_OMP_SIGNIFICANCE__": ("scatter_cmp_oma_significance.png", "O-A significance map"),
    "__IMG_CMP_OMP_SIGONLY__": ("scatter_cmp_oma_sigonly.png", "O-A significant-only map"),
    "__IMG_CMP_STDOMP_DIFFERENCE__": ("scatter_cmp_stdoma_difference.png", "Sigma of O-A difference map"),
    "__IMG_CMP_STDOMP_SIGONLY__": ("scatter_cmp_stdoma_sigonly.png", "Sigma of O-A significant-only map"),
    "__IMG_CMP_NOBS_DIFFERENCE__": ("scatter_cmp_nobs_difference.png", "Observation count difference map"),
}

RUNTIME_TABLE = ""
if RUNTIME_FILE and os.path.isfile(RUNTIME_FILE):
    RUNTIME_TABLE = open(RUNTIME_FILE).read().strip()

doc = DOC
if RUNTIME_TABLE:
    doc = doc.replace("__RUNTIME_TABLE__",
                      "Reference runs on ppp7 (one compute node):\n\n"
                      + RUNTIME_TABLE)
else:
    doc = doc.replace("\n__RUNTIME_TABLE__\n", "")
for key, (name, alt) in IMAGES.items():
    doc = doc.replace(key, image(name, alt))
doc = (doc
       .replace("__SETTINGS_EXP__", user_settings(f"{OUT}/run_scatter_exp.sh"))
       .replace("__SETTINGS_CMP__", user_settings(f"{OUT}/run_scatter_cont_exp.sh"))
       .replace("__VARIABLES__", VARIABLES)
       .replace("__STN_TOKENS__", STN_TOKENS)
       .replace("__CODTYP_TOKENS__", CODTYP_TOKENS)
       .replace("__CHAN_TOKENS__", CHAN_TOKENS)
       .replace("__SINGLE_FUNCS__", SINGLE_FUNCS)
       .replace("__DIFF_FUNCS__", DIFF_FUNCS)
       .replace("__PANELS__", PANELS)
       .replace("__TROUBLE__", TROUBLE))
# a marker left unfilled; `...`__ is an anonymous link, not a marker
assert not re.findall(r"__[A-Z_]+__", doc), re.findall(r"__[A-Z_]+__", doc)
assert '"""' not in doc

write_docstring(SCATTER, doc, __file__)
print("docstring lines:", doc.count("\n"))
