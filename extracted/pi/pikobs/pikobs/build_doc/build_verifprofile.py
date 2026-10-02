"""Build the verifprofile.py module docstring from its wrapper.

    python build_verifprofile.py pikobs/verifprofile/verifprofile.py pikobs/script [runtime_table.rst]
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
        ["``FAMILY``", "Observation families (array); ``ro`` and ``ch`` get their own treatment"],
        ["``FLAGS_CRITERIA``", "Flag criteria (array); ``all`` on ``bgckalt``, which has no ``assimilee``"],
        ["``FONCTION``", "``omp``, ``oma`` or ``obs_error``, one figure each"],
        ["``VARNOS``", "Varno list; empty = the family default"],
        ["``ID_STN``", "Station tokens, see section 7 (array)"],
        ["``LAND_OCEAN``", "``all``, ``land``, ``ocean``; needs ``global_land_mask``"],
        ["``MIN_OBS``", "Levels resting on fewer observations are dropped (default 30)"],
        ["``SPECIAL_COLUMN``", "``on``: one figure per wind method for ``sw`` (IR / WV)"],
        ["``RATIO_FIGURE``", "``on``: with two experiences or more, their sigma ratios on one figure"],
        ["``MATCH``", "With a control: ``on`` tests the change on the observations both runs hold, ``off`` on each run with all of its own"],
        ["``SVG``", "``on`` also writes each figure as SVG, for editing"],
        ["``N_CPUS``", "Number of Dask workers"],
    ])

PANELS_CMP = grid(
    ["Panel", "What it shows"],
    [
        ["Mean", "the mean departure of each run: control black with squares, experience red with circles"],
        ["Bias change", "abs(mean_exp) - abs(mean_ctl) at its own scale, with the paired t-test dots"],
        ["Relative sigma", "100 x (sigma_exp - sigma_ctl) / sigma_ctl, with the sigma-test dots"],
        ["Observations", "matched observations per level, as bars"],
    ])

PANELS_SINGLE = grid(
    ["Panel", "What it shows"],
    [
        ["Mean", "the mean departure of the run"],
        ["Sigma", "sigma of the departure"],
        ["Observations", "observations per level"],
    ])

MARKS = grid(
    ["Mark", "Meaning"],
    [
        ["red dot", "the experience is better at that level, and the test passes 95 %"],
        ["blue dot", "the control is better, and the test passes 95 %"],
        ["hollow dot", "the change is not larger than noise"],
        ["grey cross", "the level cannot be tested: the control has no sigma there"],
    ])

SCORE_TABLE = grid(
    ["Table", "In each cell"],
    [
        ["sigma", "100 x (sigma Exp - sigma Ctl) / sigma Ctl, in %"],
        ["bias", "100 x (abs(mean Exp) - abs(mean Ctl)) / sigma Ctl, in % of the sigma of the control"],
    ])

STN_TOKENS = grid(
    ["Token", "Profiles produced"],
    [
        ["``join``", "one, every station together"],
        ["``all``", "one per station; on ai, sf, ua, gp and csr one per instrument type"],
        ["``C%``", "the stations whose id starts with C, together; the title lists them"],
        ["``pilot``, ``AMDAR (42)``", "on a composite family, that instrument type"],
        ["``=COSMIC2-E1``", "that station only"],
    ])

TROUBLE = grid(
    ["Symptom", "Cause and fix"],
    [
        ["GPS-RO stops well below 60 km",
         "Count the observations per kilometre in one cycle file, before and after the quality gates: the drop tells whether the file, the gates or the experience is missing the levels."],
        ["``N level(s) dropped: O-P identical for every observation``",
         "Levels the system does not use, with O-P stored as 0. Typical of MLS at the top of the profile on ``bgckalt``."],
        ["A level has a grey cross",
         "The control has no sigma there and the experience does: nothing to test."],
        ["Almost every dot is red or blue",
         "Hundreds of thousands of observations per level: every change is real, however small. Read the bias-change and sigma panels for the size."],
        ["``run 'control' ( )  directory not found``",
         "``PATH_CONTROL_FILES`` holds a space. Leave it truly empty, ``\"\"``."],
        ["A figure of sigma ratios appears with one experience",
         "The installed ``verifprofile.py`` is an older one; the ratio figure is off by default."],
        ["An old ``run_progps.sh`` still runs",
         "``pikobs.progps`` now calls verifprofile and accepts the old options, with a note in the log. Move to ``run_verifprofile_cont_exp.sh`` (or ``run_verifprofile_exp.sh`` for runs on their own)."],
    ])

DOC = r"""
============================================================
pikobs.verifprofile -- Vertical profiles of the departures
============================================================

Some observations see a change long before anything else does. GPS radio
occultation measures refractivity from the ground to 60 km with almost
no bias of its own, and MLS measures ozone up to a few hundredths of a
hectopascal: both sit where the model is least constrained, the upper
troposphere and the stratosphere, and both answer to a change in the
background almost at once. When an experiment touches the model top, the
radiation, the humidity or the bias correction of the radiances, these
are the profiles that move first.

``verifprofile`` draws that answer level by level: the mean departure of
each run, the change of the bias, the change of the sigma, and how many
observations every level rests on. Given a control, the two runs are
matched observation by observation, so both sides of a level are the very
same measurements, and every level is tested.

It replaces ``progps``, which still answers and passes everything here.

Quick start
===========

.. code-block:: bash

   # one or several experiences, each on its own figures
   wget https://gitlab.science.gc.ca/dlo001/Pikobs/-/raw/master/pikobs/script/run_verifprofile_exp.sh
   chmod +x run_verifprofile_exp.sh

   # a control against one or several experiences
   wget https://gitlab.science.gc.ca/dlo001/Pikobs/-/raw/master/pikobs/script/run_verifprofile_cont_exp.sh
   chmod +x run_verifprofile_cont_exp.sh

The wrapper runs on the node you are on and never submits to PBS, so open
a compute node first, edit the ``USER SETTINGS`` block and launch:

.. code-block:: bash

   qsub -I -lselect=1:ncpus=80:mem=185gb -lwalltime=2:0:0
   nano run_verifprofile_cont_exp.sh
   ./run_verifprofile_cont_exp.sh

.. warning::

   Do not run the wrapper on a login node: the extraction opens every 6-h
   file of the period, of every run, in parallel.

A real run, GPS-RO and MLS on ``bgckalt``, three and a half months against
a control:

.. code-block:: text

   [verifprofile] control: Control  |  matched observation by observation with: expericience
   [verifprofile] ch: vcoord = vcoord  (PRESSION)
   [verifprofile] ro: vcoord = round(vcoord/1000.)*1000  (HAUTEUR(metres))  -- normalised by B_ref = 300 exp(-h/6500), with the GPS-RO quality gates
   [verifprofile] input check OK: 432 cycles x 2 run(s) x 2 family(ies), 1728 files, 99.7 GB
   [verifprofile] extraction time: 172.0s (4320/4320 files)
   [verifprofile] plot time: 1.9s (81/81)
   [verifprofile] total           187.1 s   (3.1 min, 80 workers)
   Viewer: /home/dlo001/sites8/pikobs_verifprofile_cont_exp/pikobs_verifprofile_viewer.html
   Web:    to open it in a browser, link the folder under public_html once:
             ln -s /home/dlo001/sites8/pikobs_verifprofile_cont_exp /home/dlo001/public_html/
           then: https://goc-dx-u3.science.gc.ca/~dlo001/pikobs_verifprofile_cont_exp/pikobs_verifprofile_viewer.html

Two live instances, both made by ``run_doc_examples.sh`` from the same
two suites over the same days, and refreshed with the documentation:

* `one run on its own <https://goc-dx-u3.science.gc.ca/~dlo001/sites8/pikobs_doc_verifprofile_exp/pikobs_verifprofile_viewer.html>`__
* `G0 against G2 <https://goc-dx-u3.science.gc.ca/~dlo001/sites8/pikobs_doc_verifprofile/pikobs_verifprofile_viewer.html>`__, the operational suite as the control, with the comparison panels and the tests

How long a run takes, and how big a node to ask for: :doc:`runtime`.

----

1. How it works
===============

**Input check.** Every 6-h file of every run and family is looked up
first; if one is missing the run stops before touching ``PATHWORK``.

**Matching.** With a control, an observation is the same in both runs when
its station, position, date, time, varno and level all agree -- the key
of scatter. Each run is read once into a temporary table indexed on that
key, so the matching costs a single pass whatever the size of the file:
four months of GPS-RO and MLS, one hundred gigabytes, take three minutes on
a node. A level one run drops and the other keeps does not shift the rest
of the profile: the levels are matched by value, not by rank.

**Only real departures count.** A value counts when it is a number. An
empty field is not read as a zero, and each quantity keeps its own count:
an observation without O-A still counts fully for O-P.

**Shared extraction.** The extraction is the one of :doc:`zone`, with one
latitude band per hemisphere, summed away when the profile is drawn. Both
modules therefore agree on the same data to the last observation.

----

2. Configuration
================

Only the ``USER SETTINGS`` block of a wrapper is meant to be edited.

.. wrapper-settings:: run_verifprofile_exp.sh run_verifprofile_cont_exp.sh

----

3. Reading a figure
===================

With a control, four panels in a row, sharing the vertical axis:

__PANELS_CMP__

__IMG_PROFILE__

The mean panel is context. The two curves usually lie on top of each
other, and the change the tests are about is a hundred times smaller than
the values themselves: that is what the bias-change panel shows, at its own
scale, with the background tinted red on the side where the experience
comes closer to zero and blue on the other.

Each level of the two change panels carries a mark on its left edge:

__MARKS__

Without a control, three panels give the profile of the run itself:

__PANELS_SINGLE__

Very small or very large values carry their power of ten in the unit of
the axis, ``O-P [10⁻⁷ mol/mol]``, rather than in a corner. Levels resting on
fewer than ``MIN_OBS`` observations are dropped, and so are levels where O-P
is the same number for every observation; the header says how many.

----

4. GPS radio occultation
========================

For ``ro`` every departure is divided by a reference refractivity profile
before it is summed:

.. math::

   B_{ref}(h) = 300 \, e^{-h / 6500}

Refractivity falls by a factor of ten every fifteen kilometres. Without the
normalisation, the lowest levels, hundreds of times larger, would decide
every scale and the stratosphere would read as a flat line; with it, a
change at 45 km weighs as much as one at 5 km. A profile passes the quality
gates of the operational verification before it counts: height between -1
and 100 km, background between 0 and 500, ``obs / B_ref`` between 0.3 and 3,
``(O-P) / B_ref`` within +/-0.05, and ``obs_error / B_ref`` between 0 and 1.
Levels are 1 km bins, from the surface to 60 km.

----

5. MLS and other pressure profiles
==================================

MLS ozone levels are pressures, from about 260 hPa to 0.02 hPa: four
decades. The axis is in hPa, inverted, and logarithmic as soon as a profile
spans more than one decade.

Two things are specific to MLS on ``bgckalt``. There is no assimilation
decision yet at that stage, so ``FLAGS_CRITERIA=(all)``. And the top levels
the system does not use come with O-P stored as zero for every
observation; they are dropped, and the header says so.

----

6. The tests
============

The bias is tested with the paired t-test and the sigma with the Pitman-Morgan test,
both from :doc:`stats`, which explains them with formulas and worked
examples. The pairing is what makes them sharp here: both sides of a level
are the same observations, so what the two runs share cancels, and even a
small change can be seen.

It cuts both ways. MLS brings close to three hundred thousand observations
per level over a season, and at that size almost any change is
significant: a change of sigma of half a percent will fill the dot. A
filled dot says the change is real; the panels say whether it matters.
Read them together, and see :doc:`stats` for why a significant change and a
large one are not the same thing.

----

7. The scorecard
================

With a control, the run ends with one more figure per function and
criterion: every family, variable and region of the comparison in a single
table, by layers of height, with the change of the experience against the
control in each cell. It is made from the figures that pool every station
(``join`` in ``ID_STN``).

__IMG_SCORECARD__

The layers are the same for every family, in km: 0-2, 2-5, 5-10, 10-15,
15-20, 20-30, 30-40 and 40-60. A level given in pressure is placed with a
standard atmosphere, z = -7 km x ln(p / 1013.25 hPa), and each column gives
both.

A cell adds up every matched observation of its layer: the counts, the
sums, the sums of squares and of products of all its levels, as if the
layer were a single level. That gives the mean and the sigma of each run,
and the two numbers of the table:

__SCORE_TABLE__

A cell is red where the experience is better and blue where it is worse,
only when its change holds over the cycles and reaches 0.5 %; grey
otherwise. The test is not the one of section 6. With a season of
observations those call almost any change real, since the observations
of one cycle share the error of that forecast. Here the change of the
cell is computed cycle by cycle, and
:func:`pikobs.stats.cycle_confidence` asks whether its mean over the
cycles is away from zero at 95 %, counting the memory from one cycle to
the next: a change made by a few days does not pass. It is empty when the family does not reach the layer
or the layer holds fewer than 30 observations. Quantities of the whole
column, such as total ozone, have no height and are left out. The numbers
of every cell, with their counts and confidences, are in a CSV next to the
figure.

----

8. Stations and instrument types
================================

__STN_TOKENS__

On ``ai``, ``sf``, ``ua``, ``gp`` and ``csr`` the tokens name instrument
types rather than stations -- ``pilot``, ``=TEMP``, ``35`` -- the same
way in every module; see :doc:`families`.

A prefix such as ``C%`` is one profile of all the stations it matches, and
the title lists them: ``C% -> COSMIC2-E1, COSMIC2-E2, ... (+5 more)``.

----

9. The viewer
=============

``pikobs_verifprofile_viewer.html`` has one selector per dimension:
Experience, Family, Fonction, Region, Criteria, Station, Special,
Land/ocean and Varno. With several experiences each is its own comparison,
and **Flip** switches between them on the same axes. With
``RATIO_FIGURE="on"`` and two experiences or more, ``all vs <control>``
adds one figure with every sigma ratio on the same axes. The scorecard
is the family ``scorecard``: the sections it holds entirely -- the
regions, the variables, the stations -- show every button on.

----

10. Output layout
=================

::

   $PATHWORK/
   ├── pikobs_verifprofile_viewer.html
   ├── verifprofile_timing.json
   ├── scorecard/                 (with a control)
   │   ├── scorecard_<exp>_vs_<control>_<fonction>_<flag>_<surface>.png
   │   └── scorecard_<exp>_vs_<control>_<fonction>_<flag>_<surface>.csv
   └── <family>/
       ├── verifprofile_<control>_vs_<exp>_<selection>_<start>_<end>_<family>.db
       └── verifprofile_<control>_vs_<exp>_<family>_<fonction>_varno<N>_<station>_<region>[_<surface>][_<special>]_<flag>.png

----

11. Support
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
       .replace("__IMG_SCORECARD__", image("verifprofile_scorecard.png",
                                           "The O-P scorecard of an "
                                           "experiment, by layers of "
                                           "height"))
       .replace("__SCORE_TABLE__", SCORE_TABLE)
       .replace("__IMG_PROFILE__", image("verifprofile_comparison.png",
                                         "Four panels of a comparison, "
                                         "MLS ozone"))
       .replace("__SETTINGS_EXP__",
                user_settings(f"{SCRIPTS}/run_verifprofile_exp.sh"))
       .replace("__SETTINGS_CMP__",
                user_settings(f"{SCRIPTS}/run_verifprofile_cont_exp.sh"))
       .replace("__VARIABLES__", VARIABLES)
       .replace("__PANELS_SINGLE__", PANELS_SINGLE)
       .replace("__PANELS_CMP__", PANELS_CMP)
       .replace("__MARKS__", MARKS)
       .replace("__STN_TOKENS__", STN_TOKENS)
       .replace("__TROUBLE__", TROUBLE))
assert not re.findall(r"__[A-Z_]+__", doc), re.findall(r"__[A-Z_]+__", doc)
assert '"""' not in doc

write_docstring(MODULE, doc, __file__)
print("docstring lines:", doc.count("\n"))
