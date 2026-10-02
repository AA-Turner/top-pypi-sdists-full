"""Build the mapobs.py module docstring from its wrapper.

    python build_doc_mapobs.py pikobs/mapobs/mapobs.py pikobs/script [runtime_table.rst]
"""
import os as _os_dw, sys as _sys_dw  # noqa: E401
_sys_dw.path.insert(0, _os_dw.path.dirname(_os_dw.path.abspath(__file__)))
from docwrite import write_docstring  # noqa: E402
import os
import re
import sys

if len(sys.argv) < 3:
    sys.exit(__doc__)
MODULE, SCRIPTS = sys.argv[1], sys.argv[2]
RUNTIME_FILE = sys.argv[3] if len(sys.argv) > 3 else None


def user_settings(path):
    txt = open(path).read()
    a = txt.index("# 1. USER SETTINGS")
    a = txt.index("\n", txt.index("# ====", a)) + 1
    b = txt.index("# ====", a)
    return "\n".join("   " + l if l else ""
                     for l in txt[a:b].strip("\n").splitlines())


def grid(headers, rows):
    cols = list(zip(*([headers] + rows)))
    widths = [max(len(c) for c in col) for col in cols]
    sep = "+" + "+".join("-" * (w + 2) for w in widths) + "+"

    def line(r):
        return "|" + "|".join(f" {c:<{w}} " for c, w in zip(r, widths)) + "|"

    out = [sep, line(headers), sep.replace("-", "=")]
    for r in rows:
        out += [line(r), sep]
    return "\n".join(out)


def image(name, alt, static="docs/source/_static"):
    """The figure, or nothing when the run that makes it has not been
    done yet: a page reads better without one image than with a broken
    link and a warning at every build."""
    if not os.path.isfile(os.path.join(static, name)):
        print(f"  (no {name} yet: left out of the page)")
        return ""
    return (f".. image:: _static/{name}\n   :alt: {alt}\n"
            f"   :align: center\n   :width: 100%")


VARIABLES = grid(
    ["Variable", "What it does"],
    [
        ["``PATH_EXPERIENCE_FILES``", "One or more run directories (array)"],
        ["``EXPERIENCE_NAME``", "One name per directory, same order (array)"],
        ["``PATHWORK``", "Output directory, wiped at each run"],
        ["``DATESTART`` / ``DATEEND``", "Period, ``YYYYMMDDHH`` UTC, both ends included"],
        ["``REGION``", "Map projections, one dashboard series each (array)"],
        ["``FAMILY``", "Observation families (array)"],
        ["``FLAGS_CRITERIA``", "Flag criteria, one series each (array)"],
        ["``ID_STN``", "Station tokens, see section 3 (array)"],
        ["``CHANNEL``", "``join``, ``all`` or an explicit list (array)"],
        ["``INTERVAL_MIN``", "Sub-cycle length in minutes (15 gives 24 per cycle)"],
        ["``PANELS``", "Which figures to draw: map, cross, vertical, stations, all"],
        ["``SVG``", "``on`` also writes each figure as SVG, for editing"],
        ["``N_CPUS``", "Number of Dask workers"],
    ])

PANELS = grid(
    ["Figure", "What it shows"],
    [
        ["``map``", "each observation at its position, with the longitude and latitude profiles"],
        ["``cross``", "the zonal and meridional cross-sections: level against latitude and longitude"],
        ["``vertical``", "observation count per level or channel, split by station"],
        ["``stations``", "count and share per station or instrument type"],
        ["``all``", "the four above stacked into a single image"],
    ])

PROJECTIONS = grid(
    ["Region", "Projection", "Map cell"],
    [
        ["``cyl``", "Plate Carree, the whole globe", "rectangular"],
        ["``npolar`` / ``spolar``", "Polar stereographic", "square"],
        ["``orthon`` / ``orthos``", "Orthographic over a pole", "square"],
        ["``canada`` / ``ameriquenord``", "Polar stereographic, centred", "square"],
        ["``europe``", "Polar stereographic, centred", "square"],
        ["``robinson``", "Robinson, the whole globe", "rectangular"],
    ])

STN_TOKENS = grid(
    ["Token", "Dashboards produced"],
    [
        ["``join``", "one series, every station together"],
        ["``all``", "one series per station, per instrument type for ai, sf, ua, gp, csr"],
        ["``CAS`` or ``\"CAS*\"``", "the stations whose id starts with CAS, together"],
        ["``=NOAA20``", "that station only"],
        ["``N%``", "SQL ``LIKE`` pattern on the station id"],
    ])

TROUBLE = grid(
    ["Symptom", "Cause and fix"],
    [
        ["``ERROR: missing 6-h input files``",
         "At least one ``YYYYMMDDHH_<family>`` is missing; the report lists the gaps and the dates available."],
        ["``Refusing to wipe ...``",
         "``PATHWORK`` points at a home or a system directory. Choose a dedicated one."],
        ["``coastlines not drawn``",
         "The cartopy cache is empty and the node cannot reach the Natural Earth archive. The dashboards are still drawn; warm the cache from a node with network access."],
        ["Every dot is the same colour",
         "The selection holds a single station. Use ``ID_STN=(all)`` to split it, or check the family."],
        ["A level is missing from a figure",
         "The rows come from the whole period: a level with no data in that cycle stays empty, which is itself information."],
        ["Too many dashboards",
         "The count is runs x families x regions x criteria x stations x levels x cycles x sub-intervals. Raise ``INTERVAL_MIN`` or cut ``ID_STN``."],
        ["A polar map looks cut",
         "It should not: polar projections get a square cell. If the profiles look out of range, check that the region covers the data."],
        ["The page shows old figures",
         "Browser cache: reload with Ctrl+Shift+R."],
    ])

DOC = r'''
================================================
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

__STN_TOKENS__

``CHANNEL`` works the same way: ``join`` puts every level in one dashboard,
``all`` gives one per level, and an explicit list keeps only those.

----

4. One figure per panel
=======================

__PANELS__

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

__IMG_DASHBOARD__

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

__PROJECTIONS__

A pole-centred projection draws a disc, so it gets a round boundary in a
square cell: no empty corners, and the whole cap is visible.

Where the profiles sit follows from that. On ``cyl`` the axes of the map
**are** longitude and latitude, so a profile pinned to its edge lines up
with it column by column, and that is where they stay. On a polar or
rotated projection the map is projected: pinning the profiles to its
edges would suggest a correspondence that does not exist, so they go
underneath, each with its own degree axis. It is the same data either
way; what changes is whether the layout claims an alignment it has.

__IMG_POLAR__

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
'''

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
doc = (doc
       .replace("__IMG_DASHBOARD__", image("mapobs_dashboard.png",
                                           "A 6-hour dashboard, nine panels"))
       .replace("__IMG_POLAR__", image("mapobs_polar.png",
                                       "A polar projection inside a square "
                                       "cell"))
       .replace("__SETTINGS__", user_settings(f"{SCRIPTS}/run_mapobs.sh"))
       .replace("__VARIABLES__", VARIABLES)
       .replace("__PANELS__", PANELS)
       .replace("__PROJECTIONS__", PROJECTIONS)
       .replace("__STN_TOKENS__", STN_TOKENS)
       .replace("__TROUBLE__", TROUBLE))
assert not re.findall(r"__[A-Z_]+__", doc), re.findall(r"__[A-Z_]+__", doc)
assert '"""' not in doc

write_docstring(MODULE, doc, __file__)
print("docstring lines:", doc.count("\n"))
