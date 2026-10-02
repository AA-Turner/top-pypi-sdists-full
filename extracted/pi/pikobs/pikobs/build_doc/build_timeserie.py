"""Build the timeserie.py module docstring from its wrapper.

    python build_timeserie.py pikobs/timeserie/timeserie.py pikobs/script [runtime_table.rst]
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
        ["``PATH_CONTROL_FILES``", "Control run; empty for the series of each run on its own"],
        ["``CONTROL_NAME``", "Name of the control in the figures"],
        ["``PATH_EXPERIENCE_FILES``", "One or more run directories (array)"],
        ["``EXPERIENCE_NAME``", "One name per directory, same order (array)"],
        ["``PATHWORK``", "Output directory, wiped per family at each run"],
        ["``DATESTART`` / ``DATEEND``", "Period, ``YYYYMMDDHH`` UTC; empty = relative to today"],
        ["``DAYS_BACK_END`` / ``WINDOW_DAYS``", "The relative window, used when the dates are empty"],
        ["``REGION``", "Regions, one series each (array)"],
        ["``FAMILY``", "Observation families (array)"],
        ["``FLAGS_CRITERIA``", "Flag criteria (array); ``all`` shows every decision of the quality control"],
        ["``CHANNEL``", "``join``, ``all`` (one series per channel or level), or a list"],
        ["``PRESSURE_LAYERS``", "Pressure families: layer bounds in hPa, one series per layer, see section 7"],
        ["``HEIGHT_LAYERS``", "Height families (GPS-RO, radar): layer bounds in km, one series per layer"],
        ["``LAND_OCEAN``", "``all``, ``land``, ``ocean``; needs ``global_land_mask``"],
        ["``ID_STN``", "Station tokens, see section 6 (array)"],
        ["``VARNOS``", "Varno list; empty = the family default"],
        ["``MATCH``", "``on``: test the change of every cycle on the observations the runs share"],
        ["``FONCTION``", "The comparison in O-P (``omp``), O-A (``oma``) or both; the figure of one run draws both"],
        ["``ALERT_PCT``", "0 = none; X = mark a cycle that falls X %% below its usual count"],
        ["``SVG``", "``on`` also writes each figure as SVG, for editing"],
        ["``N_CPUS``", "Number of Dask workers"],
    ])

RUN_PANELS = grid(
    ["Panel", "What it shows"],
    [
        ["Flag combinations", "the observations of every cycle, stacked by their flag combination: the ones carrying bit 12 in blues, the others in their own colour"],
        ["By station", "with a pooled selection, the same counts stacked by station -- or by instrument type on ai, sf, ua, gp and csr"],
        ["Mean", "the mean of O-P and O-A, and the bias correction, per cycle"],
        ["Sigma", "their sigma, and the mean assigned observation error"],
    ])

CMP_PANELS = grid(
    ["Panel", "What it shows"],
    [
        ["Observations", "every run, its assimilated observations thick and its total faint; the control solid, the experiences dashed"],
        ["Assimilated, exp - control", "how many more, or fewer, each cycle brings"],
        ["Mean and sigma", "one curve per run, every run with all of its own observations; the value of each run over the period above the panel"],
        ["Change of the mean, change of sigma", "experience minus control, cycle by cycle; the bar is filled when the test says the change is real, pale when it is not. Above each, the change over the period and how many cycles pass the test"],
    ])

MATCH_TABLE = grid(
    ["MATCH", "What changes"],
    [
        ["``off``", "the bars of the change panels are drawn pale: the change is shown, not judged"],
        ["``on``", "the change of every cycle is tested on the observations the two runs share -- paired t-test on the mean, Pitman-Morgan on sigma (see :doc:`stats`) -- and the bars are filled accordingly. The summary also says how much of the data the runs share"],
    ])

READING = grid(
    ["What you see", "What it usually means"],
    [
        ["a step in the stack, one colour growing", "a decision of the quality control changed: a channel blacklisted, thinning tightened"],
        ["a cycle far below the others", "a satellite missing, a late file, a failed retrieval -- ALERT_PCT marks them"],
        ["more observations and a larger sigma", "the experience assimilates more, and the ones it adds are harder; MATCH=on tells the two apart"],
        ["the assigned error far from sigma", "the errors the system assigns do not match the data; see profile for the same by level"],
    ])

STN_TOKENS = grid(
    ["Token", "Series produced"],
    [
        ["``join``", "one, every station together, with the panel by station"],
        ["``all``", "one per station; on ai, sf, ua, gp and csr one per instrument type"],
        ["``C%``", "the stations whose id starts with C, together"],
        ["``=METOP-1``", "that station only"],
    ])

TROUBLE = grid(
    ["Symptom", "Cause and fix"],
    [
        ["Only the counts are drawn",
         "The files carry no O-P or O-A: the figure says so and keeps the counts, which is the point of the module."],
        ["Alerts on every 06 and 18 cycle",
         "Not a failure: those cycles are small for ua and sf. Each cycle is compared with the median of the SAME hour on the days before, so start ALERT_PCT around 40 or 50."],
        ["The runs share little of the data",
         "With MATCH=on the summary gives the share. A low one is real when the runs thin differently; if it looks impossible, check that both write the same time and the same position for an observation."],
        ["The change bars are all pale",
         "MATCH is off, so nothing is tested."],
        ["Too many figures",
         "They multiply: regions x criteria x surfaces x stations x levels. Keep CHANNEL=(join) and ID_STN=(join all) for a daily run."],
    ])

DOC = r"""
======================================================================
pikobs.timeserie -- Availability and quality control, cycle by cycle
======================================================================

The first thing I want to know about a run is not how good the
observations are, but how many arrived and what the system did with them.
A channel goes on the blacklist, a satellite drops for a day, thinning is
tightened: none of that shows in a mean or a sigma, and all of it changes
what the analysis had to work with.

``timeserie`` draws that, every 6-h cycle: the observations stacked by
their flag combination, who brings them, and -- when the files carry
departures -- the mean and the sigma of O-P and O-A with the error the
system assigned. A file without O-P still gives the counts: the figure
draws what the data has, and says what it does not.

With a control, one more figure puts the runs side by side and adds the
change of the mean and of sigma, cycle by cycle.

Quick start
===========

.. code-block:: bash

   # one or several experiences, each on its own figures
   wget https://gitlab.science.gc.ca/dlo001/Pikobs/-/raw/master/pikobs/script/run_timeserie_exp.sh
   chmod +x run_timeserie_exp.sh

   # a control against one or several experiences
   wget https://gitlab.science.gc.ca/dlo001/Pikobs/-/raw/master/pikobs/script/run_timeserie_cont_exp.sh
   chmod +x run_timeserie_cont_exp.sh

The wrapper runs on the node you are on and never submits to PBS, so open
a compute node first, edit the ``USER SETTINGS`` block and launch:

.. code-block:: bash

   qsub -I -lselect=1:ncpus=80:mem=185gb -lwalltime=2:0:0
   nano run_timeserie_cont_exp.sh
   ./run_timeserie_cont_exp.sh

.. warning::

   Do not run the wrapper on a login node: the extraction opens every 6-h
   file of the period, of every run, in parallel.

.. code-block:: text

   [timeserie] runs: control, experience  |  control: control
   [timeserie] regions: ['Monde']  |  flags: ['all']  |  id_stn: ['join']  |  channel: ['join']  |  land_ocean: ['all']
   [timeserie] match: the figures keep every observation of every run; the change of each cycle is tested on the ones the runs share with control
   [timeserie] extraction time: 41.2s (192/192 files)
   [timeserie] plots: 18 tasks
   [timeserie] alerts: 2 cycle(s): .../timeserie_alerts.csv

Two live instances, both made by ``run_doc_examples.sh`` from the same
two suites over the same days, and refreshed with the documentation:

* `one run on its own <https://goc-dx-u3.science.gc.ca/~dlo001/sites8/pikobs_doc_timeserie_exp/pikobs_timeserie_viewer.html>`__
* `G0 against G2 <https://goc-dx-u3.science.gc.ca/~dlo001/sites8/pikobs_doc_timeserie/pikobs_timeserie_viewer.html>`__, the operational suite as the control, with the comparison panels and the tests

How long a run takes, and how big a node to ask for: :doc:`runtime`.

----

1. How it works
===============

**One pass per file, every selection at once.** Regions, criteria,
surfaces, stations and levels come out of the same scan, so adding four
regions costs almost nothing.

**The flags are grouped in SQL.** The counts are kept per flag
combination -- a few dozen values -- and the diagnosis of ``flag_reason``
is attached later, when the figure is drawn. Calling it per observation
would mean tens of millions of Python calls on a family like IASI.

**Only numbers count.** A departure enters the sums when it is a number;
an empty field is not a zero, and each quantity keeps its own count, so a
file with O-P and no O-A still gives its O-P statistics.

**Matching** happens only with ``MATCH="on"``, and only to test: an
observation is the same in both runs when its station, position, time,
varno and level agree.

----

2. Configuration
================

Only the ``USER SETTINGS`` block of a wrapper is meant to be edited.

.. wrapper-settings:: run_timeserie_exp.sh run_timeserie_cont_exp.sh

----

3. A run
========

__RUN_PANELS__

__IMG_RUN__

The colours of the top panel are the flag combinations themselves, not a
summary of them: every combination that carries **bit 12** is a shade of
blue, from light to dark, and everything else has its own colour. So the
blue is what entered the analysis and the rest is what the quality
control stopped, with ``12+13`` -- assimilated, but the rogue check
raised a level-1 warning -- separate from a plain ``12``. The key below
the legend gives the meaning of every bit that appears, and nothing more:
the combinations themselves are already in the legend.

With a pooled selection (``join``, or a group such as ``C%``) the second
panel shows who brings the observations, and the header lists them:
``station join -> GOES18, METOP-1, NOAA20``.

----

4. Comparing with a control
===========================

__CMP_PANELS__

__IMG_CMP__

The curves always hold **every observation of every run**, so what you
see is the system as it really is, quality and quantity together. The
control is solid and the experiences dashed: where two curves agree, one
would otherwise hide the other.

__MATCH_TABLE__

That separation matters. An experience that assimilates 20 % more
observations often shows a slightly larger sigma, and the question is
whether it got worse or whether the observations it added are harder.
``MATCH="on"`` answers it: the bars are filled only where the change
holds on the data both runs share, and the summary says what that share
is.

----

5. Reading it
=============

__READING__

----

6. Stations and instrument types
================================

__STN_TOKENS__

On ``ai``, ``sf``, ``ua``, ``gp`` and ``csr`` the tokens name instrument
types rather than stations -- ``pilot``, ``=TEMP``, ``35`` -- the same
way in every module; see :doc:`families`.

----

7. Levels and layers
====================

``CHANNEL`` decides what a series holds in the vertical: ``join`` pools the
whole column, ``all`` gives one series per level or channel, and a list
picks some of them. For radiances one series per channel is what you want.
For radiosondes or GPS-RO it is not: ``all`` gives dozens of levels, many of
them with a handful of observations, and ``join`` puts the boundary layer
and the stratosphere in the same number.

Layers sit in between, as in scatter. ``PRESSURE_LAYERS`` takes bounds in
hPa for the families on pressure levels, ``HEIGHT_LAYERS`` bounds in km for
those on heights, and every two consecutive bounds make a series, beside
what ``CHANNEL`` asks for:

.. code-block:: bash

   CHANNEL=(join)
   PRESSURE_LAYERS=(1100 850 500 250 100 10)   # ua, ai, ...: five layers
   HEIGHT_LAYERS=(0 5 10 20 30 40)             # ro, radar: five layers

They are the layers of scatter, the same edges and the same rule: a level
on an edge belongs to the layer where it is the larger number, so 500 hPa
falls in 500-250 and 5 km in 0-5, never in two layers at once. Channel
families ignore both settings. The layers are read from the levels already
extracted, so adding or changing them costs the figures and nothing else.
Each is labelled with its rank from the ground, ``2 | 850-500 hPa``, so that
the viewer lists them by height and not alphabetically.

----

8. Alerts
=========

``ALERT_PCT`` marks the cycles that bring far fewer observations than
they usually do, with a triangle on the figure and a line in
``timeserie_alerts.csv``: the run, the family, the region, the criteria,
the station, the cycle, the count, the median it was compared with and
the drop in percent.

Each cycle is compared with the median of the **same hour** on the days
before it, up to four. A family like ``ua`` brings thousands of
observations at 00 and 12 UTC and a handful at 06 and 18; comparing a
cycle with the ones just before it would flag every 06 and every 18, day
after day, and say nothing.

----

9. Output layout
================

::

   $PATHWORK/
   ├── pikobs_timeserie_viewer.html
   ├── timeserie_timing.json
   ├── timeserie_alerts.csv                (with ALERT_PCT)
   └── <family>/
       ├── timeserie_<run>_<start>_<end>_<family>.db
       └── timeserie_<run>_<family>_varno<N>_lev<level>_<station>_<region>[_<surface>][_<special>]_<flag>.png

``<level>`` is ``join``, a level or a channel, or a layer, written
``2___850-500_hPa`` for ``2 | 850-500 hPa``.

----

10. Support
===========

Bugs and feature requests:
   `<https://gitlab.science.gc.ca/dlo001/Pikobs/-/issues>`_
"""

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
       .replace("__IMG_RUN__", image("timeserie_run.png",
                                     "One run: counts by flag combination, "
                                     "by station, and the departures"))
       .replace("__IMG_CMP__", image("timeserie_comparison.png",
                                     "An experience against a control"))
       .replace("__SETTINGS_EXP__",
                user_settings(f"{SCRIPTS}/run_timeserie_exp.sh"))
       .replace("__SETTINGS_CMP__",
                user_settings(f"{SCRIPTS}/run_timeserie_cont_exp.sh"))
       .replace("__VARIABLES__", VARIABLES)
       .replace("__RUN_PANELS__", RUN_PANELS)
       .replace("__CMP_PANELS__", CMP_PANELS)
       .replace("__MATCH_TABLE__", MATCH_TABLE)
       .replace("__READING__", READING)
       .replace("__STN_TOKENS__", STN_TOKENS)
       .replace("__TROUBLE__", TROUBLE))
assert not re.findall(r"__[A-Z_]+__", doc), re.findall(r"__[A-Z_]+__", doc)
assert '"""' not in doc

write_docstring(MODULE, doc, __file__)
print("docstring lines:", doc.count("\n"))
