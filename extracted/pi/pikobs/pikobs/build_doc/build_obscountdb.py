"""Build the obscountdb.py module docstring from its wrapper.

    python build_doc_obscountdb.py pikobs/obscountdb/obscountdb.py pikobs/script [runtime_table.rst]

obscountdb.py   module whose docstring is replaced
script dir      directory holding run_obscountdb_cont_exp.sh (its USER SETTINGS
                block is copied into the doc)
runtime table   optional output of obscountdb_timing_table.py, shown in
                the "Run time" section
"""
import os as _os_dw, sys as _sys_dw  # noqa: E401
_sys_dw.path.insert(0, _os_dw.path.dirname(_os_dw.path.abspath(__file__)))
from docwrite import write_docstring  # noqa: E402
import os
import re
import sys

if len(sys.argv) < 3:
    sys.exit(__doc__)
MODULE = sys.argv[1]
SCRIPTS = sys.argv[2]
RUNTIME_FILE = sys.argv[3] if len(sys.argv) > 3 else None


def user_settings(path):
    txt = open(path).read()
    a = txt.index("# 1. USER SETTINGS")
    a = txt.index("\n", txt.index("# ====", a)) + 1
    b = txt.index("# ====", a)
    block = txt[a:b].strip("\n")
    return "\n".join("   " + l if l else "" for l in block.splitlines())


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


def image(name, alt):
    return (f".. image:: _static/{name}\n"
            f"   :alt: {alt}\n"
            f"   :align: center\n"
            f"   :width: 100%")


VARIABLES = grid(
    ["Variable", "What it does"],
    [
        ["``PATH_CONTROL_FILES``", "Directory of the control run (the reference)"],
        ["``CONTROL_NAME``", "Name of the control in the tables and the plots"],
        ["``PATH_EXPERIENCE_FILES``", "Directory of the experience"],
        ["``EXPERIENCE_NAME``", "Name of the experience"],
        ["``PATHWORK``", "Output directory, wiped per family at each run"],
        ["``DATESTART`` / ``DATEEND``", "Period, ``YYYYMMDDHH`` UTC, both ends included"],
        ["``REGION``", "Regions, one selector entry each (array)"],
        ["``FLAGS_CRITERIA``", "Flag criteria, one selector entry each (array)"],
        ["``FAMILY``", "Observation families (array)"],
        ["``AGR``", "``omp``, ``oma`` or both: departure rows in the station plots"],
        ["``SVG``", "``on`` also writes each figure as SVG, for editing"],
["``N_CPUS``", "Number of Dask workers"],
    ])

REPORT = grid(
    ["Section", "Content"],
    [
        ["Selectors", "Region and Criteria; the choice is kept in the page address"],
        ["Overall Summary", "Nobs and profiles per family, difference and percentage, mean per 6 h"],
        ["Station Breakdown", "The same per station (per instrument type for ai, sf, ua, gp, csr)"],
        ["Time series", "One card per station with Nobs and profiles per cycle"],
        ["Departures", "With ``AGR``: one card per station and varno, with its own Varno buttons"],
    ])

ROWS = grid(
    ["Card", "Rows"],
    [
        ["General, always", "observations per cycle, then profiles per cycle"],
        ["Departures, per varno", "mean (solid / dashed) and std (thin dotted, hollow markers) per cycle"],
        ["", "max (solid) and min (dashed) of the cycle, with the interval shaded"],
    ])

TROUBLE = grid(
    ["Symptom", "Cause and fix"],
    [
        ["``ERROR: missing 6-h input files``",
         "At least one ``YYYYMMDDHH_<family>`` is missing; the report lists the gaps and the dates available. Fix the period or the path."],
        ["The wrapper stops without a message",
         "``load_pikobs.sh`` failed under ``set -e``. Run ``source`` by hand to see its error, usually a broken environment."],
        ["Families glued together, missing files",
         "A list was written as a string: use ``FAMILY=(ai sw)``, not ``FAMILY=\"ai sw\"``."],
        ["``WARNING: n/N ... tasks lost``",
         "A worker ran out of memory or a figure failed; the rest of the run continues. Lower ``N_CPUS`` or check the traceback above."],
        ["A station has no departure row",
         "Its ``omp`` / ``oma`` column is empty in the databases; a note under the card says so."],
        ["No Varno buttons",
         "``AGR`` is empty, so no departure card is drawn; only the general Nobs and profiles cards."],
        ["Too many figures",
         "With ``AGR`` the count is multiplied by the varnos of each family. Leave ``AGR`` empty, or split conventional families and radiances into two runs."],
        ["The report says no data for a region",
         "No observation of the selected families passed that region and criteria."],
        ["The page shows old figures",
         "Browser cache: reload with Ctrl+Shift+R."],
    ])

DOC = r'''
================================================================
pikobs.obscountdb -- Observation Volume Diagnostics
================================================================

``obscountdb`` answers the first question I ask about any new experience:
did it use more observations than the control, or fewer, and where? It
counts what each run assimilated, family by family, station by station and
cycle by cycle, and puts everything in one HTML report where gains are
green and losses red.

One run covers **every region and every flag criteria at once**. The input
files are read a single time and all the combinations are computed in that
pass, so adding four regions and a second criteria costs almost nothing:
in my tests, fifteen combinations took 2.5 times the time of one, not
fifteen. The report then lets you switch between them with two rows of
buttons.

Quick start
===========

.. code-block:: bash

   wget https://gitlab.science.gc.ca/dlo001/Pikobs/-/raw/master/pikobs/script/run_obscountdb_cont_exp.sh
   chmod +x run_obscountdb_cont_exp.sh

The wrapper runs on the node you are on and never submits to PBS, so open
a compute node first, edit the ``USER SETTINGS`` block and launch:

.. code-block:: bash

   qsub -I -lselect=1:ncpus=80:mem=185gb -lwalltime=2:0:0
   nano run_obscountdb_cont_exp.sh
   ./run_obscountdb_cont_exp.sh

.. warning::

   Do not run the wrapper on a login node: the extraction opens every 6-h
   file of the period in parallel.

.. important::

   Lists are **bash arrays**: ``FAMILY=(ai sw)`` and ``REGION=(Monde
   Canada)``, not strings. The wrapper passes them as ``"${FAMILY[@]}"``;
   a plain string arrives glued and ends in "missing file" errors.

A run prints its phases and finishes with the address of the report:

.. code-block:: text

   [obscountdb] runs: Control, Experience
   [obscountdb] regions: ['Monde', 'HemisphereNord', 'HemisphereSud', 'Tropiques', 'Canada']
   [obscountdb] flags_criteria: ['assimilee', 'rejets']
   [obscountdb] input check OK: 21 cycles x 2 run(s) x 8 family(ies), 336 files, 94.7 GB
   [obscountdb] extraction: 336 tasks, 80 worker(s)
   [pikobs] extraction: 336/336 (100%) 224s elapsed
   [obscountdb] extraction time: 223.8s (336/336 files)
   [obscountdb] figures: 1240 station plots
   [pikobs] figures: 1240/1240 (100%) 196s elapsed
   [obscountdb] ------------------ run time ------------------
   [obscountdb] input           94.7 GB   336 files, 21 cycles, 2 run(s)
   [obscountdb] extraction      223.8 s
   [obscountdb] figures         196.4 s
   [obscountdb] report           12.7 s
   [obscountdb] total           434.1 s   (7.2 min, 80 workers)
   Report: /home/dlo001/sites8/pikobs_obscountdb_cont_exp/pikobs_obscountdb_viewer.html
   Web:    to open it in a browser, link the folder under public_html once:
             ln -s /home/dlo001/sites8/pikobs_obscountdb_cont_exp /home/dlo001/public_html/
           then: https://goc-dx-u3.science.gc.ca/~dlo001/pikobs_obscountdb_cont_exp/pikobs_obscountdb_viewer.html

`A live reference instance <https://goc-dx-u3.science.gc.ca/~dlo001/sites8/pikobs_doc_obscountdb/pikobs_obscountdb_viewer.html>`__.

How long a run takes, and how big a node to ask for: :doc:`runtime`.

----

1. How it works
===============

**Input check.** Every 6-h file of both runs and every family is looked up
first. If one is missing the run stops, says which cycles are missing and
which dates the directory does hold, and leaves ``PATHWORK`` untouched, so
a typo in the dates does not erase the previous report.

**Extraction.** Each file is read once. For every (region, criteria) pair
the query carries its own conditional aggregates, so one scan feeds them
all:

.. code-block:: sql

   SUM(CASE WHEN <region> AND <criteria> THEN 1 ELSE 0 END)          -- Nobs
   COUNT(DISTINCT CASE WHEN <region> AND <criteria> THEN id_obs END) -- profiles

For ``ai``, ``sf``, ``ua``, ``gp`` and ``csr`` the rows are grouped by
``codtyp`` and named after the instrument type (AMDAR, TEMP, SYNOP...);
the other families are grouped by ``id_stn``.

**What is stored.** One row per (region, criteria, station, varno,
cycle), with the raw moments of the departures when ``AGR`` asks for them:
:math:`N`, :math:`\sum x`, :math:`\sum x^2`, plus the minimum and the
maximum of the cycle. Next to them sits one row per station holding the
counts of every varno together: the profiles of a station cannot be added
over varnos, since the same ``id_obs`` carries several of them, so they
are counted once there. Means and standard deviations are derived when the
report is built:

.. math::

   \bar{x} = \frac{\sum x}{N},
   \qquad
   \sigma = \sqrt{\max\left(0,\ \frac{\sum x^2}{N} - \bar{x}^2\right)}

Keeping the sums instead of the means is what makes any later grouping
exact: several ``codtyp`` rows folding into one instrument label, or a
whole period folding into one number, are simple additions.

**Figures.** One task per (region, criteria, family, station), spread over
the workers. Each writes its PNG in ``figures/``; the report links them
instead of embedding them, which keeps the HTML at a few hundred kB
instead of hundreds of MB.

**Report.** One ``pikobs_obscountdb_viewer.html`` with the selectors, plus the same
tables as CSV in ``tables/``.

----

2. Configuration
================

Only the ``USER SETTINGS`` block of the wrapper is meant to be edited.
obscountdb always compares, so the control is not optional: without it
the run stops on the first line.

.. wrapper-settings:: run_obscountdb_cont_exp.sh

----

3. The report
=============

__REPORT__

The **Region** and **Criteria** buttons sit at the top of the page and
stay there while you scroll. The current choice is written in the page
address, so a link like ``pikobs_obscountdb_viewer.html#Canada|assimilee`` opens
straight on that panel, which is handy in an email.

Everything below the buttons is what the report always showed: the
summary per family, the breakdown per station, and the time-series cards.
Gains are green, losses red, and the mean columns are the totals divided
by the number of 6-h cycles in the period.

Station cards
-------------

Each family has one or two blocks of cards, each card a station framed in
its own colour.

The first block, **Nobs and profiles per station**, is always there, with
or without ``AGR``. The second, **Departures per station and varno**,
appears when ``AGR`` asks for ``omp`` or ``oma``, and above it sits a row
of **Varno** buttons listing the varnos that family really has for the
region and criteria selected at the top of the page. Pressing one changes
the departure cards of that family only; the general cards stay where they
are, and every family keeps its own buttons.

__ROWS__

REF is always blue and EXP always red, in every row. The line above the
card repeats the numbers of the period on two lines, one per metric: mean
and std of each run, and the interval in which the departures stayed.

__IMG_STATION__

Why the varnos are separate: a family such as ``ua`` carries temperatures
in K, winds in m/s and pressures in Pa, so a mean over all of them means
nothing. The counts are different, and they stay together: ``Nobs`` and
the tables add every varno of the station.

The extremes are worth a look before trusting a mean: a cycle whose
minimum or maximum jumps far away from the others usually means a bad
observation got through, not that the background changed.

----

4. Output layout
================

::

   $PATHWORK/
   ├── pikobs_obscountdb_viewer.html                  <- the report, with the selectors
   ├── obscountdb_timing.json            <- settings and time of each phase
   ├── figures/
   │   └── <region>_<flag>_<family>_<varno>_<station>.png
   ├── tables/
   │   ├── Overall_<region>_<flag>.csv
   │   └── Stations_<family>_<region>_<flag>.csv
   └── <family>/
       └── <run>_<start>_<end>_<family>.db

The ``.db`` files hold one row per (region, criteria, station, varno,
cycle) in the table ``moyenne``, where ``varno = -1`` marks the row with
the counts of the whole station, and can be queried with ``sqlite3``. The CSV files
hold exactly the numbers of the HTML tables, ready for a spreadsheet or a
presentation.

With ``SVG="on"`` each figure is written again as ``.svg`` beside its PNG,
for editing before a presentation: in Inkscape or Illustrator the titles,
the legends and the colours stay editable. The viewer always uses the PNG,
so turning it on changes nothing else.

----

5. Support
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
       .replace("__IMG_STATION__",
                image("obscountdb_station.png",
                      "Station card: Nobs, departures and extremes"))
       .replace("__SETTINGS__", user_settings(f"{SCRIPTS}/run_obscountdb_cont_exp.sh"))
       .replace("__VARIABLES__", VARIABLES)
       .replace("__REPORT__", REPORT)
       .replace("__ROWS__", ROWS)
       .replace("__TROUBLE__", TROUBLE))
assert not re.findall(r"__[A-Z_]+__", doc), re.findall(r"__[A-Z_]+__", doc)
assert '"""' not in doc

write_docstring(MODULE, doc, __file__)
print("docstring lines:", doc.count("\n"))
