"""Build the histogram.py module docstring from its wrapper.

    python build_histogram.py pikobs/histogram/histogram.py pikobs/script [runtime_table.rst]
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
        ["``PATH_CONTROL_FILES``", "Control run; empty for the distribution of each run on its own"],
        ["``CONTROL_NAME``", "Name of the control in the figures"],
        ["``PATH_EXPERIENCE_FILES``", "One or more run directories (array)"],
        ["``EXPERIENCE_NAME``", "One name per directory, same order (array)"],
        ["``PATHWORK``", "Output directory, wiped per family at each run"],
        ["``DATESTART`` / ``DATEEND``", "Period, ``YYYYMMDDHH`` UTC; empty = relative to today"],
        ["``DAYS_BACK_END`` / ``WINDOW_DAYS``", "The relative window, used when the dates are empty"],
        ["``REGION``", "Regions, one histogram each (array)"],
        ["``FAMILY``", "Observation families (array)"],
        ["``FLAGS_CRITERIA``", "Flag criteria (array); ``all`` for the QC split"],
        ["``FONCTION``", "``omp``, ``oma``, ``omp_norm``, ``oma_norm``, ``omp_std``, ``oma_std``, one figure each"],
        ["``VARNOS``", "Varno list; empty = the family default"],
        ["``CHANNEL``", "``join``, ``all`` (per channel, or per layer), or a list of channels"],
        ["``PRESSURE_LAYERS`` / ``HEIGHT_LAYERS``", "Layer edges from the ground up, hPa and km"],
        ["``ID_STN``", "Station tokens, see section 9 (array)"],
        ["``LAND_OCEAN``", "``all``, ``land``, ``ocean``; needs ``global_land_mask``"],
        ["``MIN_OBS``", "Histograms resting on fewer observations are not drawn (default 100)"],
        ["``Y_SCALE``", "``log`` shows the tails, ``linear`` the core"],
        ["``QC_SPLIT``", "``on``: one colour per flag combination, one run at a time"],
        ["``MATCH``", "With a control: ``on`` the same observations, ``off`` each run with all of its own"],
        ["``SPECIAL_COLUMN``", "``on``: one figure per wind method for ``sw`` (IR / WV)"],
        ["``SVG``", "``on`` also writes each figure as SVG, for editing"],
        ["``N_CPUS``", "Number of Dask workers"],
    ])

SINGLE_PARTS = grid(
    ["Part", "What it shows"],
    [
        ["Histogram", "the density of the run: counts divided by N and by the width of a bin"],
        ["Dashed curve", "the Gaussian of the same mean and sigma"],
        ["Brown lines", "+/-3 sigma around the mean; the legend gives the share outside"],
        ["Statistics", "N, mean, sigma, skewness, excess kurtosis, share beyond 3 sigma"],
        ["Notes", "the Gaussian references, how the bins were merged, the units"],
    ])

COMPARE_PARTS = grid(
    ["Part", "What it shows"],
    [
        ["Histogram", "both densities on the same bins: control blue, experience red"],
        ["Difference", "experience minus control, bin by bin: red where the experience has more"],
        ["Statistics", "the same table, one column per run"],
        ["Tests", "mean, sigma and shape, with the verdict in the colour of the winner"],
    ])

MATCH_MODES = grid(
    ["MATCH", "Observations", "Tests", "Question it answers"],
    [
        ["``on``", "the same in both runs, matched one by one", "paired t, F, KS",
         "does the experience fit the same observations better?"],
        ["``off``", "each run with all of its own, its own flags", "Welch t, F, KS",
         "what happens with everything the experience assimilates?"],
    ])

DIFF_PATTERNS = grid(
    ["Pattern of the difference panel", "Reading"],
    [
        ["red at the centre, blue on the shoulders", "the experience is narrower: better"],
        ["blue at the centre, red on the shoulders", "the experience is wider: worse"],
        ["red on one side of zero, blue on the other", "the distribution moves: the bias changes"],
        ["red only far in the tails", "the experience has more gross errors"],
        ["scattered bars of a few 1e-4", "nothing: a handful of observations changing bin"],
    ])

STATS = grid(
    ["Number", "Gaussian", "Reading"],
    [
        ["skewness", "0", "positive: the long tail is on the right; beyond about 0.5 the bias is not the whole story"],
        ["excess kurtosis", "0", "positive: sharper peak, heavier tails, more gross errors than sigma suggests"],
        ["beyond 3 sigma", "0.27 %", "the weight of the tails, where the quality control decides"],
        ["sigma of omp_norm", "1", "above 1 the assigned errors are too small, below 1 too large"],
    ])

TESTS = grid(
    ["Test", "On", "Reads"],
    [
        ["paired t / Welch t", "the mean", "which run is closer to zero"],
        ["Pitman-Morgan / F", "the sigma", "which run is narrower -- Pitman-Morgan on matched observations, F otherwise; with omp_norm, which is closer to 1"],
        ["Kolmogorov-Smirnov", "the whole shape", "D, the share of the observations on the other side"],
    ])

STN_TOKENS = grid(
    ["Token", "Histograms produced"],
    [
        ["``join``", "one, every station together"],
        ["``all``", "one per station; on ai, sf, ua, gp and csr one per instrument type"],
        ["``C%``", "the stations whose id starts with C, together; the title lists them"],
        ["``=METOP-1``", "that station only"],
    ])

TROUBLE = grid(
    ["Symptom", "Cause and fix"],
    [
        ["The QC split is all blue",
         "On a postalt file most rejected observations have no O-P and cannot sit in a histogram of O-P. The table on the right lists them under LEFT OUT; the log gives the totals. On bgckalt the rejected ones usually keep their O-P."],
        ["``9+12+17`` in an assimilated run",
         "Bit 12 means the observation entered the analysis; QC-Var (bit 17) can still reject it during the minimisation. FLAGS_CRITERIA=(assimilee) keeps them."],
        ["A large kurtosis with ``CHANNEL=(join)``",
         "Pooling channels or levels of different sigmas gives heavy tails on its own. Look at CHANNEL=(all), or at omp_norm."],
        ["A spike at zero",
         "Levels where O-P is 0 for every observation are left out and listed in the log; a spike that remains is in the data."],
        ["A saw tooth in the bins",
         "Values stored in steps. The scan finds the step and the bins become whole multiples of it; the log says so."],
        ["Too many figures, a slow run",
         "Figures multiply: regions x stations x surfaces x functions x channels. A list of channels instead of all, QC_SPLIT only when it is read, N_CPUS to the node."],
    ])

DOC = r"""
======================================================
pikobs.histogram -- Distribution of the departures
======================================================

Data assimilation rests on one assumption about every observation: its
departure from the background is Gaussian, centred on zero, with the sigma
the system assigns to it. The mean and the sigma of the other modules
check the first two words of that sentence. A histogram checks the whole
of it, and above all the tails, which a mean and a sigma do not see and
where the quality control decides what goes in.

``histogram`` draws that distribution for one run, or for experiences
against a control, per region, station, channel or layer, with the
Gaussian of the same mean and sigma beside it, the statistics that say
how far from Gaussian it is, and -- when asked -- one colour per flag
combination, to see where each decision of the quality control falls.

Quick start
===========

.. code-block:: bash

   # one or several experiences, each on its own figures
   wget https://gitlab.science.gc.ca/dlo001/Pikobs/-/raw/master/pikobs/script/run_histogram_exp.sh
   chmod +x run_histogram_exp.sh

   # a control against one or several experiences
   wget https://gitlab.science.gc.ca/dlo001/Pikobs/-/raw/master/pikobs/script/run_histogram_cont_exp.sh
   chmod +x run_histogram_cont_exp.sh

The wrapper runs on the node you are on and never submits to PBS, so open
a compute node first, edit the ``USER SETTINGS`` block and launch:

.. code-block:: bash

   qsub -I -lselect=1:ncpus=80:mem=185gb -lwalltime=2:0:0
   nano run_histogram_cont_exp.sh
   ./run_histogram_cont_exp.sh

.. warning::

   Do not run the wrapper on a login node: the extraction opens every 6-h
   file of the period, of every run, in parallel.

The log opens with what the scan found, before anything is drawn:

.. code-block:: text

   [histogram] ua: one histogram per layer, not per level: 1100-850 hPa, 850-500 hPa, ...
   [histogram] ua omp varno 11003: values stored in steps of 0.1; bins are whole multiples of it
   [histogram] sw: flag combinations with O-P, one colour each (4 found, 4 drawn, ...):
   [histogram]      96.6 %  12  Assimilated
   [histogram]       2.2 %  12+13  Assimilated
   [histogram]       0.9 %  9+12+17  Erroneous Data

Two live instances, both made by ``run_doc_examples.sh`` from the same
two suites over the same days, and refreshed with the documentation:

* `one run on its own <https://goc-dx-u3.science.gc.ca/~dlo001/sites8/pikobs_doc_histogram_exp/pikobs_histogram_viewer.html>`__
* `G0 against G2 <https://goc-dx-u3.science.gc.ca/~dlo001/sites8/pikobs_doc_histogram/pikobs_histogram_viewer.html>`__, the operational suite as the control, with the comparison panels and the tests

How long a run takes, and how big a node to ask for: :doc:`runtime`.

----

1. How it works
===============

**The bins follow the variable.** A wind in m/s, a brightness temperature
in K and ozone in mol/mol cannot share a bin width. A short scan of a few
cycles measures the sigma of every variable and level, and the bins are a
twentieth of it, out to six sigmas on either side, with one overflow bin
at each end. When the values come in steps -- 0.1 for conventional data,
0.01 K for radiances, as BURP stores them -- the bins become whole
multiples of the step, or the histogram grows a saw tooth. With few
observations the bins are merged for the drawing, to about 2 N^(1/3) of
them; the statistics are untouched, they come from the exact values.

**Only real departures.** A value counts when it is a number: an empty
field is not a zero. Levels where O-P is the same for every observation --
levels the system does not use, stored as 0 -- are left out and listed in
the log, since pooled with the others they would draw a spike at zero.

**Levels.** ``CHANNEL=(join)`` puts every level in one histogram. With
``all``, a radiance family gives one histogram per channel; a family on
pressure or height gives one per **layer** -- 1100-850 hPa, 850-500 hPa ...
or 0-5 km, 5-10 km ... -- since one per level of the family would be dozens
of near-identical figures. The viewer selector reads *Channel* or *Vcoord*
to match.

**GPS-RO** departures are divided by the reference refractivity profile, as
in :doc:`verifprofile`.

----

2. Configuration
================

Only the ``USER SETTINGS`` block of a wrapper is meant to be edited.

.. wrapper-settings:: run_histogram_exp.sh run_histogram_cont_exp.sh

----

3. A single run
===============

Without a control, every figure is the distribution of one run:

__SINGLE_PARTS__

__IMG_SINGLE__

``omp_std`` and ``oma_std`` read the same histograms in sigmas of the
control -- of the run itself when it is alone. The control then has
sigma 1, its Gaussian the same peak whatever the variable, and shapes
compare at a glance: a wind, a temperature, a radiance. The mean reads
as mean / sigma, the weight of the bias. Nothing is extracted twice: the
bins are those of ``omp`` and ``oma``, on another scale.

The vertical axis is logarithmic, each line ten times the one below. On
a linear axis the centre is 0.2 and the tails 0.0001, and the tails --
where the bad observations and the rejections are -- would not show. On
this one a Gaussian is an upturned parabola, and a bar above the dashed
curve in a tail is an excess of large departures. Beside the numbers,
the header says what each one means: symmetric or not, tails like a
Gaussian or heavier, and how many times a Gaussian's 0.27 % lies beyond
3 sigma.

The axis is a **density** -- counts divided by the number of observations
and by the width of a bin -- so histograms with different numbers of
observations compare on the same footing. The vertical axis is logarithmic
by default: at four sigmas a departure is a thousand times rarer than at
the centre, and on a linear axis the tails would be a line along zero.

Where the histogram rises above the dashed Gaussian in the tails, the
errors are not Gaussian. The brown lines at +/-3 sigma make that a number:
a Gaussian leaves 0.27 % outside, and the legend says what the data leaves.

----

4. Comparing with a control
===========================

With a control, both runs are drawn on the same bins, the control in
**blue** and the experience in **red**, and two more parts appear:

__COMPARE_PARTS__

__IMG_COMPARE__

The example is O-A, and on purpose: G0 and G2 are two passes of the same
operational cycle and start from the same background, so their O-P is the
same observation by observation and the red histogram would sit exactly on
the blue one. The analysis is where they part (:doc:`scatter` works the
case through).

``MATCH`` decides which observations are compared:

__MATCH_MODES__

With ``on``, observations present in one run only are left out, and so
are new observations the experience brings. With ``off``, the header gives
the change in the number of observations, ``(+25.0 % in A120)``, and a
station only the experience has still gets its figure.

The difference panel is read by **where** each colour falls, not by the
colour alone:

__DIFF_PATTERNS__

Mind the power of ten in its label: ``[10-4]`` is a few observations.

----

5. The statistics
=================

__STATS__

Pooling channels or levels of different sigmas -- ``CHANNEL=(join)`` on
IASI, all levels of ``ua`` -- gives a large kurtosis on its own, every
channel being Gaussian. Before concluding the errors are not Gaussian,
look at one channel or layer, or at ``omp_norm``: departures divided by the
error the system assigns to each observation. If those errors are right,
that histogram is the green N(0, 1) drawn beside it.

----

6. The tests
============

__TESTS__

All three come from :doc:`stats`. With ``MATCH="on"`` the mean is tested
with the paired t-test, the most sensitive, since what the runs share
cancels; with ``off``, with Welch, the cautious form. The sigma the same
way: Pitman-Morgan on the pairs, the F-test without them. Kolmogorov-Smirnov
looks at the whole shape: two distributions can share their mean and
their sigma and still differ, an experiment that trims the tails and
fattens the shoulders moves neither.

**Read D before the confidence.** With a season of data every change is
significant; D says how large it is. 0.01 is one percent of the
observations on the other side, 0.001 is nothing to worry about.

----

7. The quality control, flag by flag
====================================

``QC_SPLIT="on"``, one run at a time, stacks every observation that has an
O-P by its flag combination: one colour per combination found in the data,
assimilated or not, so the histogram shows where each of them sits.

__IMG_QC__

The legend gives the bits of each colour; the table beside it lists every
combination with its share of the selection, in two blocks, and below
them the meaning of every bit that appears, from ``flag_groups``. Bits 5, 6
and 10 are not counted: they record what was done to a value, not a
decision.

* **IN THE HISTOGRAM** -- the combinations with an O-P.
* **LEFT OUT** -- the observations with no O-P. On a postalt file most
  rejected observations are stored without one; they cannot sit in a
  histogram of O-P, but they are counted and listed.

Three things a first look usually finds. The background check (bit 9 with
16) sits in the tails, where it should. Thinning (bit 11) sigmas over the
whole range, since it does not depend on O-P. And bit 12 alone does not
mean an observation weighed in the analysis: it entered it, and QC-Var
(bit 17) can still reject it during the minimisation -- ``9+12+17`` is such
an observation, and ``FLAGS_CRITERIA=(assimilee)`` keeps it.

----

8. Levels and layers
====================

The layers are set from the wrapper, from the ground up, each holding its
top level:

.. code-block:: bash

   PRESSURE_LAYERS=(1100 850 500 250 100 10 1 0)   # hPa
   HEIGHT_LAYERS=(0 5 10 20 30 40 60 100)          # km

``PRESSURE_LAYERS=(1100 500 300 200 150 100 50 0)`` looks closer at the
tropopause. Zone keeps the fine levels of ``family.py``: the histogram
groups them on its own.

----

9. Stations and instrument types
================================

__STN_TOKENS__

On ``ai``, ``sf``, ``ua``, ``gp`` and ``csr`` the tokens name instrument
types rather than stations -- ``pilot``, ``=TEMP``, ``35`` -- the same
way in every module; see :doc:`families`.

----

10. The viewer
==============

``pikobs_histogram_viewer.html`` has one selector per dimension: Experience,
Family, Fonction, Region, Criteria, Station, Special, Channel or Vcoord,
Land/ocean and Varno. Under the title, a short guide explains every number
of the figures.

----

11. Output layout
=================

::

   $PATHWORK/
   ├── pikobs_histogram_viewer.html
   ├── histogram_timing.json
   └── <family>/
       ├── histogram_<run>_<selection>_<start>_<end>_<family>.db
       └── histogram_<runs>_<family>_<fonction>_varno<N>_lev<level>_<station>_<region>[_<surface>][_<special>]_<flag>.png

----

12. Support
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
       .replace("__IMG_SINGLE__", image("histogram_single.png",
                                        "The distribution of one run"))
       .replace("__IMG_COMPARE__", image("histogram_comparison.png",
                                         "An experience against a control"))
       .replace("__IMG_QC__", image("histogram_qc_split.png",
                                    "One colour per flag combination"))
       .replace("__SETTINGS_EXP__",
                user_settings(f"{SCRIPTS}/run_histogram_exp.sh"))
       .replace("__SETTINGS_CMP__",
                user_settings(f"{SCRIPTS}/run_histogram_cont_exp.sh"))
       .replace("__VARIABLES__", VARIABLES)
       .replace("__SINGLE_PARTS__", SINGLE_PARTS)
       .replace("__COMPARE_PARTS__", COMPARE_PARTS)
       .replace("__MATCH_MODES__", MATCH_MODES)
       .replace("__DIFF_PATTERNS__", DIFF_PATTERNS)
       .replace("__STATS__", STATS)
       .replace("__TESTS__", TESTS)
       .replace("__STN_TOKENS__", STN_TOKENS)
       .replace("__TROUBLE__", TROUBLE))
assert not re.findall(r"__[A-Z_]+__", doc), re.findall(r"__[A-Z_]+__", doc)
assert '"""' not in doc

write_docstring(MODULE, doc, __file__)
print("docstring lines:", doc.count("\n"))
