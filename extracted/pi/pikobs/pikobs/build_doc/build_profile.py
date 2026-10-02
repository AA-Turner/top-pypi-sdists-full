"""Build the profile.py module docstring from its wrapper.

    python build_profile.py pikobs/profile/profile.py pikobs/script [runtime_table.rst]
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
        ["``PATH_CONTROL_FILES``", "Control run; empty for the profile of each run on its own"],
        ["``CONTROL_NAME``", "Name of the control in the figures"],
        ["``PATH_EXPERIENCE_FILES``", "One or more run directories (array)"],
        ["``EXPERIENCE_NAME``", "One name per directory, same order (array)"],
        ["``PATHWORK``", "Output directory, wiped per family at each run"],
        ["``DATESTART`` / ``DATEEND``", "Period, ``YYYYMMDDHH`` UTC; empty = relative to today"],
        ["``DAYS_BACK_END`` / ``WINDOW_DAYS``", "The relative window, used when the dates are empty"],
        ["``REGION``", "Regions, one profile each (array)"],
        ["``FAMILY``", "Observation families (array)"],
        ["``FLAGS_CRITERIA``", "Flag criteria (array)"],
        ["``FONCTION``", "``omp`` or ``oma``, one figure each"],
        ["``VARNOS``", "Varno list; empty = the family default"],
        ["``ID_STN``", "Station tokens, see section 7 (array)"],
        ["``MIN_OBS``", "Levels resting on fewer observations are dropped (default 30)"],
        ["``MATCH``", "With a control: ``on`` tests the change on the observations both runs hold, ``off`` on each run with all of its own"],
        ["``SVG``", "``on`` also writes each figure as SVG, for editing"],
        ["``N_CPUS``", "Number of Dask workers"],
    ])

RUN_PANELS = grid(
    ["Panel", "What it shows"],
    [
        ["Observations", "how many observations every level rests on"],
        ["Departure", "the bias (thin) and the sigma (thick) of each level, with the assigned observation error (dotted) and the Desroziers estimate of it (crosses)"],
        ["Key", "the lines, and the elevations with their number of observations"],
    ])

RATIO = grid(
    ["Ratio", "Reading"],
    [
        ["about 1", "the errors the system assigns match what the data shows"],
        ["above 1", "the assigned error is too small: the data varies more than the system expects"],
        ["below 1", "the assigned error is too large, a conservative choice"],
    ])

DIFF_PANELS = grid(
    ["Panel", "What it shows"],
    [
        ["Bias change", "abs(bias of the experience) - abs(bias of the control): left of zero the experience is closer to zero"],
        ["Sigma change", "100 x (sigma_exp - sigma_ctl) / sigma_ctl, in percent: left of zero the experience is narrower"],
    ])

MARKS = grid(
    ["Mark", "Meaning"],
    [
        ["red dot", "the experience is better at that level, and the test passes 95 %"],
        ["blue dot", "the control is better, and the test passes 95 %"],
        ["hollow dot", "the change is not larger than noise (one elevation at a time)"],
    ])

RADAR_VIEWS = grid(
    ["View", "What it gives"],
    [
        ["axis ``range``", "the slant range in km, as the superobservations come"],
        ["axis ``height``", "the beam height above sea level, in 1-km bins"],
        ["elevation ``join``", "every elevation of the selection on the same panels, one colour each"],
        ["one elevation", "that elevation alone, and with OBS_ERROR_MODEL its own model curve"],
    ])

STN_TOKENS = grid(
    ["Token", "Figures produced"],
    [
        ["``join``", "one, every station together"],
        ["``all``", "one per station; on ai, sf, ua, gp and csr one per instrument type"],
        ["``C%``", "the stations whose id starts with C, together"],
        ["``=cashr``", "that station only"],
    ])

TROUBLE = grid(
    ["Symptom", "Cause and fix"],
    [
        ["The change figure holds far fewer observations than the runs",
         "The matching found few pairs. On radar the key is the station, the time of the sweep, the azimuth, the elevation and the range: check that both runs write the same TIME_START and CENTER_AZIMUTH."],
        ["``sigma / expected`` says 'no assigned observation error'",
         "The files have no OBS_ERROR column with data; the other panels are drawn as usual."],
        ["The ratio sits below 1 everywhere",
         "The assigned error is larger than the whole sigma of the departure -- a conservative setting, and what a model calibrated to stay above the real sigma gives."],
        ["An elevation is missing from the figure of all of them",
         "Elevations with less than 1 % of the observations are left out of that figure to keep it readable; each still has its own."],
        ["The model line is not drawn",
         "OBS_ERROR_MODEL is off, the axis is the range, or the selection mixes radar networks (join): the model belongs to a network, C or U."],
        ["Too many figures, a slow run",
         "Figures multiply: regions x criteria x stations x functions, and on radar x elevations x two axes. Cut regions or use ID_STN=(join C% U%)."],
    ])

DOC = r"""
===================================================
pikobs.profile -- Vertical profiles, level by level
===================================================

Every observation carries an error the system assigns to it, and the whole
analysis rests on that number being right. A profile is where you see
whether it is: level by level, the sigma of the departures against the
error the system expects.

``profile`` draws, for every run and every level: how many observations
there are, the bias and the sigma of the departures, the assigned
observation error, and their ratio.

With a control, each experience gets one more figure with the change of
the bias and of the sigma, level by level, the runs matched observation by
observation and every level tested.

Quick start
===========

.. code-block:: bash

   # one or several experiences, each on its own figures
   wget https://gitlab.science.gc.ca/dlo001/Pikobs/-/raw/master/pikobs/script/run_profile_exp.sh
   chmod +x run_profile_exp.sh

   # a control against one or several experiences
   wget https://gitlab.science.gc.ca/dlo001/Pikobs/-/raw/master/pikobs/script/run_profile_cont_exp.sh
   chmod +x run_profile_cont_exp.sh

The wrapper runs on the node you are on and never submits to PBS, so open
a compute node first, edit the ``USER SETTINGS`` block and launch:

.. code-block:: bash

   qsub -I -lselect=1:ncpus=80:mem=185gb -lwalltime=2:0:0
   nano run_profile_cont_exp.sh
   ./run_profile_cont_exp.sh

.. warning::

   Do not run the wrapper on a login node: the extraction opens every 6-h
   file of the period, of every run, in parallel.

.. code-block:: text

   [profile] input check OK: 17 cycles x 1 run(s) x 1 family(ies), 17 files, 2.0 GB
   [profile] extraction time: 10.4s (17/17 files)
   [profile] plots: 168 tasks
   [profile] plot time: 91.4s (168/168)

Two live instances, both made by ``run_doc_examples.sh`` from the same
two suites over the same days, and refreshed with the documentation:

* `one run on its own <https://goc-dx-u3.science.gc.ca/~dlo001/sites8/pikobs_doc_profile_exp/pikobs_profile_viewer.html>`__
* `G0 against G2 <https://goc-dx-u3.science.gc.ca/~dlo001/sites8/pikobs_doc_profile/pikobs_profile_viewer.html>`__, the operational suite as the control, with the comparison panels and the tests

How long a run takes, and how big a node to ask for: :doc:`runtime`.

----

1. How it works
===============

**One pass per file.** Every 6-h file is read once and the sums of every
station, level and varno come out of that single scan. Only
numbers count: an empty field is not a zero, and each quantity keeps its
own count, so an observation without O-A still counts for O-P.

**The levels.** Each family uses its own vertical coordinate, as
``family.py`` defines it; see :doc:`families`.

**Matching.** With a control, an observation is the same in both runs when
its key agrees: the station, position, time and level, as in every module
(see :doc:`match`).

**The same axes everywhere.** The limits of every panel are computed once
across all the runs of a group, so flipping between them in the viewer
never makes the axes jump.

----

2. Configuration
================

Only the ``USER SETTINGS`` block of a wrapper is meant to be edited.

.. wrapper-settings:: run_profile_exp.sh run_profile_cont_exp.sh

----

3. A run
========

__RUN_PANELS__

__IMG_RUN__

Read the sigma against the two errors beside it. The assigned error is
what the system gives each observation; the Desroziers estimate,
sqrt(E[(O-A)(O-P)]), is the error the analysis actually sees in the data
(Desroziers et al., 2005). Where the two part, the assigned error is off.

For radar, ``FIT_RADAR="on"`` goes one step further: after the run, profile
fits the error model of the radar -- per network, C or U, and per class of
elevation, the form base + slope dh + accel dh^2 above an onset -- to the
Desroziers estimate of that run. It leaves in ``<family>/fit_<run>/`` the
coefficients, the table ready to paste into ``radar_obs_error.py`` and one
figure of the fit per network, and on the figures of one elevation against
height it draws the fitted error (long dashes) beside the current model
(dash-dot). Off by default: it is a calibration, not a daily diagnostic.

``FIT_RADAR_TARGET`` says what the fit aims at: ``desroziers`` (the
default, which needs O-A; without it the fit falls back on the sigma of
O-P, and says so), ``sigma`` (the sigma of O-P), or ``sigma3`` -- the sigma
of O-P within 3 sigma of its cell, a network, an elevation and one vcoord,
each on its own: the sums of the run give every cell its mean and sigma,
the radar files are read a second time and what lies beyond 3 sigma is
left out. The table ``radar_obs_error_calibration_sigma3_<run>.csv`` says
how much.

A missing or empty file does not stop a run: the log and the viewer say
which cycles, and the figures are drawn without them.

The OBS_ERROR the assimilation used is always drawn, beside the sigma and
the bias. ``ERROR_CURVES`` adds other error curves: ``desroziers``, and on
radar ``model`` and ``model_fit``. The
viewer gives the formula of those drawn, and of those only.

----

4. Comparing with a control
===========================

Each experience gets one more figure with the change, the runs matched
observation by observation:

__DIFF_PANELS__

__IMG_DIFF__

The tests come from :doc:`stats`: the paired t-test on the bias, the Pitman-Morgan test
on the sigma. With one elevation, every level carries its mark on the left
edge; with several, the mark sits on the point itself:

__MARKS__

The background is tinted on the side where each run wins, and the header
counts the levels: ``bias: 3 red, 1 blue   sigma: 12 red, 0 blue``.

----

5. Stations and instrument types
================================

__STN_TOKENS__

On ``ai``, ``sf``, ``ua``, ``gp`` and ``csr`` the tokens name instrument
types rather than stations -- ``pilot``, ``=TEMP``, ``35`` -- the same
way in every module; see :doc:`families`.

----

6. The viewer
=============

``pikobs_profile_viewer.html`` has one selector per dimension: Experience,
Family, Fonction, Region, Criteria, Station, Varno, Elevation and Axis.
Each run is its own entry, and with a control the change of each experience
is another, so **Flip** moves between them on the same axes.

----

7. Output layout
================

::

   $PATHWORK/
   ├── pikobs_profile_viewer.html
   ├── profile_timing.json
   └── <family>/
       ├── profile_<run>_<start>_<end>_<family>.db
       └── profile_<run>_<family>_<fonction>_varno<N>_<station>_<region>[_<surface>][_<special>]_<flag>[_elev<E>_<axis>].png

----

8. Support
==========

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
       .replace("__IMG_RUN__", image("profile_run.png",
                                     "One run: observations, departure and "
                                     "ratio"))
       .replace("__IMG_DIFF__", image("profile_change.png",
                                      "An experience against a control"))
       .replace("__IMG_RADAR__", image("profile_radar.png",
                                       "Radar: one line per elevation"))
       .replace("__SETTINGS_EXP__",
                user_settings(f"{SCRIPTS}/run_profile_exp.sh"))
       .replace("__SETTINGS_CMP__",
                user_settings(f"{SCRIPTS}/run_profile_cont_exp.sh"))
       .replace("__VARIABLES__", VARIABLES)
       .replace("__RUN_PANELS__", RUN_PANELS)
       .replace("__RATIO__", RATIO)
       .replace("__DIFF_PANELS__", DIFF_PANELS)
       .replace("__MARKS__", MARKS)
       .replace("__RADAR_VIEWS__", RADAR_VIEWS)
       .replace("__STN_TOKENS__", STN_TOKENS)
       .replace("__TROUBLE__", TROUBLE))
assert not re.findall(r"__[A-Z_]+__", doc), re.findall(r"__[A-Z_]+__", doc)
assert '"""' not in doc

write_docstring(MODULE, doc, __file__)
print("docstring lines:", doc.count("\n"))
