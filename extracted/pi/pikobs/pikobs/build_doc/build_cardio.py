"""Build the cardio.py module docstring from its wrapper.

    python build_doc_cardio.py pikobs/cardio/cardio.py pikobs/script [runtime_table.rst]
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
        ["``PATH_CONTROL_FILES``", "Control run; empty means plain time series, no comparison"],
        ["``CONTROL_NAME``", "Name of the control in the figures"],
        ["``PATH_EXPERIENCE_FILES``", "One or more run directories (array)"],
        ["``EXPERIENCE_NAME``", "One name per directory, same order (array)"],
        ["``PATHWORK``", "Output directory, wiped per family at each run"],
        ["``DATESTART`` / ``DATEEND``", "Period, ``YYYYMMDDHH`` UTC, both ends included"],
        ["``REGION``", "Regions, one selector entry each (array)"],
        ["``FLAGS_CRITERIA``", "Flag criteria, one selector entry each (array)"],
        ["``FAMILY``", "Observation families (array)"],
        ["``ID_STN``", "Station tokens, see section 3 (array)"],
        ["``CHANNEL``", "``join``, ``all`` or an explicit list (array)"],
        ["``PLOT_TYPE``", "``wide`` or ``narrow`` figure"],
        ["``VARNOS``", "Optional varno list, empty = the family default"],
        ["``MATCH``", "With a control: ``on`` tests the change on the observations both runs hold, ``off`` on each run with all of its own"],
        ["``SVG``", "``on`` also writes each figure as SVG, for editing"],
["``N_CPUS``", "Number of Dask workers"],
    ])

PANELS = grid(
    ["Panel", "Lines", "Read it for"],
    [
        ["Bias", "O-P, O-A and the bias correction, per cycle", "a drift of the bias, a jump after a change"],
        ["Sigma", "sigma of O-P and O-A per cycle", "a run getting noisier or calmer"],
        ["Obsvalue", "observation, trial and analysis", "whether the values themselves moved"],
        ["Counts", "Ndata and Nlocs per cycle", "data lost or gained, gaps in the suite"],
        ["O-P range", "the minimum and the maximum of each cycle", "one bad observation that a mean hides"],
        ["O-A range", "the same for O-A", "the same, after the analysis"],
    ])

STN_TOKENS = grid(
    ["Token", "Figures produced"],
    [
        ["``join``", "one figure, every station pooled"],
        ["``all``", "one figure per station, per instrument type for ai, sf, ua, gp, csr"],
        ["``CAS`` or ``\"CAS*\"``", "the stations whose id starts with CAS, pooled"],
        ["``=NENE``", "that station only"],
        ["``C%``", "SQL ``LIKE`` pattern on the station id"],
        ["``pilot``, ``\"AMDAR (42)\"``", "instrument types, for the codtyp families"],
    ])

TROUBLE = grid(
    ["Symptom", "Cause and fix"],
    [
        ["``ERROR: missing 6-h input files``",
         "At least one ``YYYYMMDDHH_<family>`` is missing; the report lists the gaps and the dates available."],
        ["The wrapper stops without a message",
         "``load_pikobs.sh`` failed; the guard in the wrapper prints it, otherwise run ``source`` by hand."],
        ["``nothing to plot, check the selectors``",
         "No row matched the tokens: check ``ID_STN`` and ``CHANNEL`` against the log line that lists them."],
        ["``experience names must be unique``",
         "Two runs share a name; they would write the same database and the same figures."],
        ["Panels of two experiences look differently scaled",
         "They should not: the y limits are shared through ``y_limits_<region>.json``. Delete it to recompute."],
        ["No circles anywhere",
         "Either no control was given, or no cycle passed 95 %. The header says which: with a control it always prints the count."],
        ["The two runs have different cycles",
         "Only the cycles both runs hold are drawn; the rest are dropped silently, since a comparison needs both sides."],
        ["``the control and an experience share the name``",
         "They would write the same database. Give the control its own ``CONTROL_NAME``."],
        ["A panel is missing",
         "Its column is empty in the files, for instance O-A in a monitoring run."],
        ["The page shows old figures",
         "Browser cache: reload with Ctrl+Shift+R."],
    ])

DOC = r'''
====================================================
pikobs.cardio -- Observation Cardiogram Time Series
====================================================

``cardio`` is the module I open first when a suite misbehaves. It draws the
heartbeat of an experience: for every cycle of the period, the bias, the
sigma, the physical values, the number of observations and the extremes
of the departures, one panel above the other and sharing the same time
axis, so a gap in the data and a jump in the departures line up at a
glance.

Give it a control and it stops being a description and becomes a
comparison: the two runs share every panel and each cycle is tested.

It takes several experiences in one run, each with its own time series, and
the viewer switches between them. Regions and flag criteria are computed in
a single pass over the input files, so asking for five regions costs almost
what one costs.

Quick start
===========

.. code-block:: bash

   # one or several experiences, each on its own figures
   wget https://gitlab.science.gc.ca/dlo001/Pikobs/-/raw/master/pikobs/script/run_cardio_exp.sh
   chmod +x run_cardio_exp.sh

   # a control against one or several experiences
   wget https://gitlab.science.gc.ca/dlo001/Pikobs/-/raw/master/pikobs/script/run_cardio_cont_exp.sh
   chmod +x run_cardio_cont_exp.sh

The wrapper runs on the node you are on and never submits to PBS, so open a
compute node first, edit the ``USER SETTINGS`` block and launch:

.. code-block:: bash

   qsub -I -lselect=1:ncpus=80:mem=185gb -lwalltime=2:0:0
   nano run_cardio_cont_exp.sh
   ./run_cardio_cont_exp.sh

.. warning::

   Do not run the wrapper on a login node: the extraction opens every 6-h
   file of the period in parallel.

.. important::

   Lists are **bash arrays**: ``FAMILY=(ai sw)`` and ``ID_STN=(join all)``,
   not strings. Quote any token with a ``*`` or a space:
   ``ID_STN=(join "CAS*" "AMDAR (42)")``.

A run prints its phases and ends with the address of the viewer:

.. code-block:: text

   [cardio] runs: E22, E23
   [cardio] id_stn tokens: ['join', 'all']
   [cardio] channel tokens: ['join']
   [cardio] input check OK: 41 cycles x 2 run(s) x 6 family(ies), 492 files, 121.5 GB
   [cardio] extraction: 492 tasks, 80 worker(s)
   [pikobs] extraction: 492/492 (100%) 287s elapsed
   [cardio] plots: 640 tasks
   [cardio] -------------------- run time --------------------
   [cardio] input          121.5 GB   492 files, 41 cycles, 2 run(s)
   [cardio] extraction      287.4 s
   [cardio] plots           212.9 s
   [cardio] total           507.8 s   (8.5 min, 80 workers)
   Viewer: /home/dlo001/sites8/pikobs_cardio_cont_exp/pikobs_cardio_viewer.html
   Web:    https://goc-dx-u3.science.gc.ca/~dlo001/sites8/pikobs_cardio_cont_exp/pikobs_cardio_viewer.html

Two live instances, both made by ``run_doc_examples.sh`` from the same
two suites over the same days, and refreshed with the documentation:

* `one run on its own <https://goc-dx-u3.science.gc.ca/~dlo001/sites8/pikobs_doc_cardio_exp/pikobs_cardio_viewer.html>`__
* `G0 against G2 <https://goc-dx-u3.science.gc.ca/~dlo001/sites8/pikobs_doc_cardio/pikobs_cardio_viewer.html>`__, the operational suite as the control, with the comparison panels and the tests

How long a run takes, and how big a node to ask for: :doc:`runtime`.

----

1. How it works
===============

**Input check.** Every 6-h file of every run and family is looked up first.
A missing one does not stop the run: a time series with a hole is still a
time series. The suites keep about ten days and delete from the front,
so a period chosen in the morning can lose its first cycle by the
afternoon. The run goes on with the files there are, the log says which
cycles are missing for which run and family, and the viewer says it where
it is seen: *input incomplete* in its title and an orange box at the head
of its About. Only a period without a single file stops the run.

**Extraction.** Each file is read once, grouped by station, varno and
channel, with one set of conditional aggregates per (region, criteria)
pair. What is stored are sums, never means:

.. math::

   N,\quad \sum x,\quad \sum x^2 \quad\text{for O-P, O-A and the
   observation},
   \qquad
   N_{b},\quad \sum b \quad\text{for the bias correction}

plus the rejected and accepted counts, the profiles and the locations of
the region. A figure that pools stations or channels then adds sums, which
is exact; averaging per-cycle means and sigmas would not be. This is also
why the module no longer needs the SQLite ``STDDEV`` extension.

**Figures.** One task per (run, family, region, criteria, station
selection, channel, varno), spread over the workers.

----

2. Configuration
================

Only the ``USER SETTINGS`` block of a wrapper is meant to be edited.

.. wrapper-settings:: run_cardio_exp.sh run_cardio_cont_exp.sh

----

3. Choosing the stations and channels
=====================================

``ID_STN`` takes the tokens of the rest of Pikobs, and each one is its own
series of figures:

__STN_TOKENS__

``CHANNEL`` works the same way: ``join`` merges every channel or level into
one figure, ``all`` gives one figure per channel, and an explicit list
keeps only those. The two combine: ``ID_STN=(all)`` with ``CHANNEL=(all)``
is one figure per station and channel, which is where the count of figures
grows fastest.

----

4. Reading a figure
===================

Four panels share the same time axis:

__PANELS__

__IMG_PANELS__

The line above each panel repeats the numbers of the whole period,
weighted by the number of observations of each cycle, one run after the
other.

The last two panels are the ones worth a second look before trusting a
mean. They show the extreme departure of every cycle, the lowest and the
highest, with the interval shaded. A cycle whose maximum jumps far away
from its neighbours almost always means one bad observation got through,
not that the background changed; the mean of that cycle will barely
move, and the sigma will.

Comparing with a control
------------------------

Fill ``PATH_CONTROL_FILES`` and every experience is drawn on the same
panels as the control. **Red is the experience and blue the control**,
in a single run as well; the line says the quantity: O-P and the trial
solid, O-A and the analysis dashed, the observation dash-dot in black,
the bias correction dotted. One key at the top of the figure says it for
every panel, so no legend sits on the curves. With two
experiences you get two figures, each against the same control, and the
viewer switches between them.

Then every cycle is tested, and the ones where the change is more than
noise get a **transparent circle**: red when the experience wins, blue
when the control does. The count is in the header, something like
``14 in this figure``.

The bias goes through the paired t-test and the sigma through the
Pitman-Morgan test, both from :mod:`pikobs.stats`, which explains them.
cardio pairs the two runs observation by observation before it sums
anything, so both tests look at the very same observations on each side,
and that is why a small but steady change shows up. A cycle where the
runs share nothing falls back on Welch and the F-test, which only see each
run's own moments and are far more cautious. With ``MATCH=off`` every
cycle goes that way.

A circle says the change is real, not that it is large: on a cycle with
half a million observations a difference of two hundredths passes
easily. Read the circle together with the line.

The y limits are shared by every figure of a region through
``y_limits_<region>.json``: a larger limit replaces a smaller one, so the
same channel of two experiences, or of two criteria, can be compared
without rescaling by eye. Delete that file to recompute the limits from
scratch.

----

5. The viewer
=============

``pikobs_cardio_viewer.html`` has seven dropdowns: Experience, Criteria,
Family, Region, Station, Varno and Channel; each one only offers what
exists for the choices on its left. **Flip** (key ``F``) swaps between the
current figure and the previous one, which is how two experiences are
compared on the same station, and a click opens the figure at full size.

----

6. Output layout
================

::

   $PATHWORK/
   ├── pikobs_cardio_viewer.html
   ├── cardio_timing.json
   ├── y_limits_<region>.json
   └── <family>/
       ├── cardio_<run>_<start>_<end>_<family>.db
       └── serie_<run>_<flag>_<family>_<stn>_id_stn_<region>[_<surface>][_<special>]_ch<chan>_varno<varno>.png

With ``SVG="on"`` each figure is written again as ``.svg`` beside its PNG,
for editing before a presentation: in Inkscape or Illustrator the titles,
the legends and the colours stay editable. The viewer always uses the PNG,
so turning it on changes nothing else. An SVG keeps every element of the
figure, so ask for it on the one or two figures you actually need.

The ``.db`` files hold one row per (region, criteria, station, varno,
channel, cycle) in the table ``serie_cardio`` and can be queried with
``sqlite3``.

----

7. Support
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
       .replace("__IMG_PANELS__", image("cardio_panels.png",
                                        "The four panels of a cardiogram"))
       .replace("__SETTINGS_EXP__",
                user_settings(f"{SCRIPTS}/run_cardio_exp.sh"))
       .replace("__SETTINGS_CMP__",
                user_settings(f"{SCRIPTS}/run_cardio_cont_exp.sh"))
       .replace("__VARIABLES__", VARIABLES)
       .replace("__PANELS__", PANELS)
       .replace("__STN_TOKENS__", STN_TOKENS)
       .replace("__TROUBLE__", TROUBLE))
assert not re.findall(r"__[A-Z_]+__", doc), re.findall(r"__[A-Z_]+__", doc)
assert '"""' not in doc

write_docstring(MODULE, doc, __file__)
print("docstring lines:", doc.count("\n"))
