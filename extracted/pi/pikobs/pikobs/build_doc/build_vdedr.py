"""Build the vdedr.py module docstring from its wrapper.

    python build_doc_vdedr.py pikobs/vdedr/vdedr.py pikobs/script [runtime_table.rst]
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
        ["``PATH_CONTROL_FILES``", "Directory of the control run (the reference)"],
        ["``CONTROL_NAME``", "Name of the control in the plots and the viewer"],
        ["``PATH_EXPERIENCE_FILES``", "One or more experience directories (array)"],
        ["``EXPERIENCE_NAME``", "One name per directory, same order (array)"],
        ["``PATHWORK``", "Output directory, wiped per family at each run"],
        ["``DATESTART`` / ``DATEEND``", "Period, ``YYYYMMDDHH`` UTC, both ends included"],
        ["``REGION``", "Regions, one selector entry each (array)"],
        ["``FLAGS_CRITERIA``", "Flag criteria, one selector entry each (array)"],
        ["``FAMILY``", "Observation families (array)"],
        ["``ID_STN``", "Station tokens, see section 3"],
        ["``VARNOS``", "Optional varno list, empty = the family default"],
        ["``MATCH``", "With a control: ``on`` tests the change on the observations both runs hold, ``off`` on each run with all of its own"],
        ["``SVG``", "``on`` also writes each figure as SVG, for editing"],
["``N_CPUS``", "Number of Dask workers"],
    ])

METRICS = grid(
    ["Figure", "Left series", "Right series", "Test"],
    [
        ["``omp_bias``", "residual bias, ``mean(O-B)`` exp - ctl", "raw bias, bias correction removed", "none"],
        ["``omp_rel``", "``100 (σ_exp - σ_ctl) / σ_ctl`` of O-B", "``100 (N_exp - N_ctl) / N_ctl``", "sigma test: Pitman-Morgan, F-test without pairs"],
        ["``oma_rel``", "the same for O-A", "the same count change", "sigma test: Pitman-Morgan, F-test without pairs"],
    ])

COLOURS = grid(
    ["Mark", "Meaning"],
    [
        ["red dot", "``% sigma`` below zero: the experience reduces the sigma"],
        ["blue dot", "``% sigma`` above zero: the control is the better one"],
        ["green line", "``% Nobs``: more or fewer observations, neither good nor bad"],
        ["red square", "sigma test above 95 %, and the experience wins"],
        ["blue square", "sigma test above 95 %, and the control wins"],
        ["empty square", "sigma test at or below 95 %: the change can be noise"],
    ])

STN_TOKENS = grid(
    ["Token", "Figures produced"],
    [
        ["``join``", "one figure, every platform pooled"],
        ["``all``", "one figure per platform"],
        ["``METOP`` or ``\"METOP*\"``", "the platforms whose id starts with METOP, pooled"],
        ["``=NOAA-20``", "that platform only"],
        ["``N%``", "SQL ``LIKE`` pattern on the platform id"],
    ])

TROUBLE = grid(
    ["Symptom", "Cause and fix"],
    [
        ["``ERROR: missing 6-h input files``",
         "At least one ``YYYYMMDDHH_<family>`` is missing; the report lists the gaps and the dates available."],
        ["The wrapper stops without a message",
         "``load_pikobs.sh`` failed; the guard in the wrapper prints it, otherwise run ``source`` by hand."],
        ["``run names must be unique``",
         "The control and an experience share a name; they would write the same database."],
        ["A channel is missing from a figure",
         "Only the channels present in both runs are drawn, since every value is a difference."],
        ["Every square is empty",
         "Few observations per channel: the sigma test cannot separate them. Use a longer period."],
        ["The figure is very tall",
         "That is on purpose: one row per channel so that all of them stay readable. Click it in the viewer to zoom."],
        ["The page shows old figures",
         "Browser cache: reload with Ctrl+Shift+R."],
    ])

DOC = r'''
===========================================
pikobs.vdedr -- Radiance Verification
===========================================

``vdedr`` answers the question that comes with every bias-correction or
radiative-transfer change: channel by channel, did the experience move the
departures, and can I trust what I am seeing? It compares a control with
one or several experiences and draws three figures per selection, with the
channels on the y axis so that a satellite can be read top to bottom.

The channel axis is the point of this module, so it never squeezes:
whether a family has four channels or thirteen hundred, every channel keeps
its own row and its own label, and the figure grows as tall as it needs.

Quick start
===========

.. code-block:: bash

   wget https://gitlab.science.gc.ca/dlo001/Pikobs/-/raw/master/pikobs/script/run_vdedr_cont_exp.sh
   chmod +x run_vdedr_cont_exp.sh

The wrapper runs on the node you are on and never submits to PBS, so open a
compute node first, edit the ``USER SETTINGS`` block and launch:

.. code-block:: bash

   qsub -I -lselect=1:ncpus=80:mem=185gb -lwalltime=2:0:0
   nano run_vdedr_cont_exp.sh
   ./run_vdedr_cont_exp.sh

.. warning::

   Do not run the wrapper on a login node: the extraction opens every 6-h
   file of the period in parallel.

.. important::

   Lists are **bash arrays**: ``FAMILY=(iasi cris)`` and
   ``REGION=(Monde Canada)``, not strings.

A run prints its phases and ends with the address of the viewer:

.. code-block:: text

   [vdedr] runs: control, exp1, exp2
   [vdedr] comparisons: control vs exp1, control vs exp2
   [vdedr] id_stn tokens: ['all']
   [vdedr] input check OK: 21 cycles x 3 run(s) x 2 family(ies), 126 files, 38.4 GB
   [vdedr] extraction: 126 tasks, 80 worker(s)
   [pikobs] extraction: 126/126 (100%) 96s elapsed
   [vdedr] plots: 48 tasks (144 figures)
   [vdedr] -------------------- run time --------------------
   [vdedr] input           38.4 GB   126 files, 21 cycles, 3 run(s)
   [vdedr] extraction       96.3 s
   [vdedr] compaction        4.1 s
   [vdedr] plots            71.5 s
   [vdedr] total           173.8 s   (2.9 min, 80 workers)
   Viewer: /home/dlo001/sites8/pikobs_vdedr_cont_exp/pikobs_vdedr_viewer.html
   Web:    to open it in a browser, link the folder under public_html once:
             ln -s /home/dlo001/sites8/pikobs_vdedr_cont_exp /home/dlo001/public_html/
           then: https://goc-dx-u3.science.gc.ca/~dlo001/pikobs_vdedr_cont_exp/pikobs_vdedr_viewer.html

One live instance: an experiment of the summer of 2025 against its
control, over two weeks of June. vdedr always compares, so there is no
single run to show:

`the live comparison <https://goc-dx-u3.science.gc.ca/~dlo001/sites8/pikobs_doc_vdedr/pikobs_vdedr_viewer.html>`__

How long a run takes, and how big a node to ask for: :doc:`runtime`.

----

1. How it works
===============

**Input check.** Every 6-h file of the control, of each experience and of
each family is looked up first. If one is missing the run stops, says which
cycles are missing and which dates the directory does hold, and leaves
``PATHWORK`` untouched.

**Extraction.** Each file is read once, grouped by station, varno and
channel. Every (region, criteria) pair carries its own conditional
aggregates in that single scan, so five regions and two criteria cost
almost the same as one of each. What is stored are the sums:

.. math::

   N,\quad \sum x,\quad \sum x^2 \quad\text{for O-B and O-A},
   \qquad
   N_{b},\quad \sum b \quad\text{for the bias correction}

Means and sigmas are derived when the figures are drawn:

.. math::

   \bar{x} = \frac{\sum x}{N},
   \qquad
   \sigma = \sqrt{\max\left(0,\ \frac{\sum x^2}{N} - \bar{x}^2\right)}

Keeping sums instead of means is what lets a figure pool several platforms
exactly, and it is also why this module no longer needs the SQLite
``STDDEV`` extension.

**Compaction.** The per-cycle rows are summed over the period and indexed
before plotting, so each figure reads a small table.

**Figures.** One task per (comparison, family, region, criteria, station
selection, varno); each task writes the three figures of that selection.

----

2. Configuration
================

Only the ``USER SETTINGS`` block of the wrapper is meant to be edited.

.. wrapper-settings:: run_vdedr_cont_exp.sh

With several experiences, the arrays keep the same length:

.. code-block:: bash

   PATH_EXPERIENCE_FILES=(/path/to/E22 /path/to/E23)
   EXPERIENCE_NAME=(E22 E23)

which gives *control vs E22* and *control vs E23*, selectable in the viewer.

----

3. Choosing the platforms
=========================

``ID_STN`` takes the tokens of the rest of Pikobs, and each one is its own
series of figures:

__STN_TOKENS__

``join`` pools the platforms by adding their moments, which is exact
because the sums are what is stored. The file names carry the selection:
``join``, ``METOP_grp`` for a prefix, ``NOAA-20_eq`` for an exact id.

----

4. Reading the figures
======================

__METRICS__

Everything is experience minus control. For the sigma the sign says who
wins, and the colours say it too:

__COLOURS__

__IMG_REL__

The column on the right of each figure holds, in order: the sigma-test square,
its confidence, and the number of observations of the control and of the
experience. Above it, the count of significant channels split by winner,
for example ``sigma test > 95%: 22/60  (22 A120, 0 CTL)``.

The bias figure keeps its two series, residual and raw. There the sign does
not tell who wins, since a difference of means can move towards or away
from zero depending on where each run started, so the marks keep their own
colour:

__IMG_BIAS__

The tests
---------

The sigma is compared with the Pitman-Morgan test and the bias with
the paired t-test, on the observations the two runs share; a channel
where they share nothing, or a run with ``MATCH=off``, falls back on
the F-test and Welch. Both live in :mod:`pikobs.stats`, which
documents them: the formulas, a worked example and how to read a
confidence.

One thing is worth knowing here. vdedr pairs the two runs observation by
observation before it sums a channel, so both tests work on the very same
radiances. That is what lets a small, steady change through: two runs of
the same suite agree on nearly every observation, and a paired test weighs
what differs against everything they share. Without the pairs, with
``MATCH=off``, the same change needs far more observations to show, and
may not show at all.

----

5. The viewer
=============

``pikobs_vdedr_viewer.html`` has seven dropdowns: Comparison, Metric,
Family, Region, Criteria, Station and Varno. Each one only offers what
exists for the choices on its left. **Flip** (key ``F``) swaps between the
current figure and the previous one, which is the quickest way to compare
two experiences on the same channel set, and a click opens the figure at
full size, which is how a 1300-channel figure is read.

----

6. Output layout
================

::

   $PATHWORK/
   ├── pikobs_vdedr_viewer.html
   ├── vdedr_timing.json
   └── <family>/
       ├── vdedr_<run>_<start>_<end>_<family>.db
       └── <metric>_<family>_<stn>_<ctl>-<exp>_<region>[_<surface>][_<special>]_<flag>_varno<varno>.png

With ``SVG="on"`` each figure is written again as ``.svg`` beside its PNG,
for editing before a presentation: in Inkscape or Illustrator the titles,
the legends and the colours stay editable. The viewer always uses the PNG,
so turning it on changes nothing else. An SVG keeps every element of the
figure, so ask for it on the one or two figures you actually need.

The ``.db`` files hold one row per (region, criteria, station, varno,
channel) in the table ``serie_vdedr`` and can be queried with ``sqlite3``.

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
       .replace("__IMG_REL__", image("vdedr_omp_rel.png",
                                     "Sigma change per channel, with the "
                                     "sigma-test column"))
       .replace("__IMG_BIAS__", image("vdedr_omp_bias.png",
                                      "Residual and raw bias per channel"))
       .replace("__SETTINGS__", user_settings(f"{SCRIPTS}/run_vdedr_cont_exp.sh"))
       .replace("__VARIABLES__", VARIABLES)
       .replace("__METRICS__", METRICS)
       .replace("__COLOURS__", COLOURS)
       .replace("__STN_TOKENS__", STN_TOKENS)
       .replace("__TROUBLE__", TROUBLE))
assert not re.findall(r"__[A-Z_]+__", doc), re.findall(r"__[A-Z_]+__", doc)
assert '"""' not in doc

write_docstring(MODULE, doc, __file__)
print("docstring lines:", doc.count("\n"))
