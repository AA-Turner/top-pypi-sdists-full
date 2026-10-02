"""Build the zone.py module docstring from its wrapper.

    python build_doc_zone.py pikobs/zone/zone.py pikobs/script [runtime_table.rst]
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
        ["``PATH_CONTROL_FILES``", "Control run; empty for plain sections, no comparison"],
        ["``CONTROL_NAME``", "Name of the control in the figures"],
        ["``PATH_EXPERIENCE_FILES``", "One or more run directories (array)"],
        ["``EXPERIENCE_NAME``", "One name per directory, same order (array)"],
        ["``PATHWORK``", "Output directory, wiped per family at each run"],
        ["``DATESTART`` / ``DATEEND``", "Period, ``YYYYMMDDHH`` UTC; empty = relative to today"],
        ["``DAYS_BACK_END`` / ``WINDOW_DAYS``", "The relative window, used when the dates are empty"],
        ["``REGION``", "Regions, one series each; they filter, the x axis stays -90 to 90"],
        ["``FAMILY``", "Observation families (array)"],
        ["``FLAGS_CRITERIA``", "Flag criteria, one series each (array)"],
        ["``FONCTION``", "``omp``, ``oma`` or ``obs_error``, one figure each"],
        ["``BOXSIZEY``", "Width of the latitude bands, in degrees"],
        ["``ID_STN``", "Station tokens, see section 3 (array)"],
        ["``CHANNEL``", "``all`` puts every level on the y axis; ``join`` collapses them"],
        ["``LAND_OCEAN``", "``all``, ``land``, ``ocean``; needs ``global_land_mask``"],
        ["``MIN_OBS``", "Cells with fewer observations are left empty"],
        ["``SPECIAL_COLUMN``", "``on``: one figure per wind method for sw (IR / WV)"],
        ["``WHITE_BAND``", "Differences inside +/- this, in the units of the variable, are white"],
        ["``MATCH``", "With a control: ``on`` tests the change on the observations both runs hold, ``off`` on each run with all of its own"],
        ["``SVG``", "``on`` also writes each figure as SVG, for editing"],
        ["``N_CPUS``", "Number of Dask workers"],
    ])

PANELS_SINGLE = grid(
    ["Panel", "What it shows"],
    [
        ["Sigma", "sigma of the departure in each cell"],
        ["Mean", "the departure itself: red above zero, blue below, white within the band"],
        ["Observations per cell", "how many observations each cell rests on"],
    ])

PANELS_CMP = grid(
    ["Panel", "What it shows"],
    [
        ["Sigma, Exp - Ctl", "sigma of Exp minus sigma of Ctl, in the units of the variable"],
        ["Bias, Exp - Ctl", "abs(mean Exp) - abs(mean Ctl): negative is closer to zero"],
        ["Pitman-Morgan test on the sigma", "red or blue where the sigma change passes 95 %"],
        ["Paired t-test on the bias", "the same for the bias, on the matched observations"],
        ["Sample size", "matched observations per cell: the same in both runs"],
    ])

STN_TOKENS = grid(
    ["Token", "Figures produced"],
    [
        ["``join``", "one, every station together: the natural choice for a section"],
        ["``all``", "one per station; on ai, sf, ua, gp and csr one per instrument type"],
        ["``pilot``, ``AMDAR (42)``", "on a composite family, that instrument type"],
        ["``CAS`` or ``\"CAS*\"``", "the stations whose id starts with CAS, together"],
        ["``=NOAA20``", "that station only"],
    ])

AXES = grid(
    ["VCOTYP of the family", "The y axis"],
    [
        ["``CANAL``", "one row per channel, first channel at the top, every one labelled"],
        ["``PRESSION``", "hPa, ground at the bottom; one row per level while there are fewer than 60"],
        ["``HAUTEUR(metres)``", "metres, upwards"],
        ["``SURFACE`` / ``LATITUDE``", "no vertical axis: these families are not drawn as sections"],
    ])

TROUBLE = grid(
    ["Symptom", "Cause and fix"],
    [
        ["``ERROR: missing 6-h input files``",
         "At least one ``YYYYMMDDHH_<family>`` is missing; the report lists the gaps and the dates available. With relative dates, check ``DAYS_BACK_END`` against how many days the source keeps."],
        ["``run 'control' ( )  directory not found``",
         "``PATH_CONTROL_FILES`` holds a space. Leave it truly empty, ``\"\"``, for a run without control."],
        ["``N selection(s) skipped, a single latitude band``",
         "Those selections sit in one band, a single radiosonde or a geostationary satellite at the edge of a small region. Nothing is lost: the data is in every other figure of the family."],
        ["``N cells left empty``",
         "Fewer than ``MIN_OBS`` observations there. Lower it, or widen ``BOXSIZEY``."],
        ["Every difference panel is white",
         "The control and the experience are the same directory, or the experience really changed nothing within ``WHITE_BAND``."],
        ["A level reads ``< 100``",
         "The family rounds its pressure, and everything above the first bin lands in bin 0, which is not 0 hPa."],
        ["The figure is tiny in the browser",
         "A tall figure squeezed to the screen: press **W** in the viewer to fit it to the width."],
    ])

DOC = r"""
======================================================
pikobs.zone -- Zonal cross-sections of the departures
======================================================

A map tells you where a departure is wrong; a zonal section tells you at
which height. That is the question behind most of what goes wrong with
winds and radiances: the jet level that drifts, the lower troposphere that
a new bias correction overdoes, the stratospheric channels that nobody
looks at until they hurt. ``zone`` puts latitude on the x axis and the
vertical coordinate of the family on the y axis, and fills every cell
with the statistics of the observations that fell in it.

Given a control, it compares, and it does it on the same observations:
the two runs are matched one by one before anything is summed.

Quick start
===========

.. code-block:: bash

   # one or several experiences, each on its own figures
   wget https://gitlab.science.gc.ca/dlo001/Pikobs/-/raw/master/pikobs/script/run_zone_exp.sh
   chmod +x run_zone_exp.sh

   # a control against one or several experiences
   wget https://gitlab.science.gc.ca/dlo001/Pikobs/-/raw/master/pikobs/script/run_zone_cont_exp.sh
   chmod +x run_zone_cont_exp.sh

The wrapper runs on the node you are on and never submits to PBS, so open
a compute node first, edit the ``USER SETTINGS`` block and launch:

.. code-block:: bash

   qsub -I -lselect=1:ncpus=80:mem=185gb -lwalltime=2:0:0
   nano run_zone_cont_exp.sh
   ./run_zone_cont_exp.sh

.. warning::

   Do not run the wrapper on a login node: the extraction opens every 6-h
   file of the period, of every run, in parallel.

A real run, six families and five regions against a control, over six
days:

.. code-block:: text

   [zone] control: control  |  matched observation by observation with: experience
   [zone] sw: vcoord = round(vcoord/2000.)*2000  (PRESSION)
   [zone] iasi: vcoord = vcoord  (CANAL)
   [zone] input check OK: 24 cycles x 2 run(s) x 6 family(ies), 288 files, 56.3 GB
   [zone] extraction time: 29.9s (288/288 files)
   [zone] colour scales: 18 group(s) shared (family x varno x fonction x region)
   [zone] plot time: 10.9s (597/597)
   [zone] total            62.9 s   (1.0 min, 80 workers)
   Viewer: /home/dlo001/sites8/pikobs_zone_cont_exp/pikobs_zone_viewer.html
   Web:    https://goc-dx-u3.science.gc.ca/~dlo001/sites8/pikobs_zone_cont_exp/pikobs_zone_viewer.html

The last two lines come from the module: when a link of ``~/public_html``
already shows the folder the address goes through it, otherwise the run
prints the one ``ln -s`` that would make the page reachable.

Two live instances, both made by ``run_doc_examples.sh`` from the same
two suites over the same days, and refreshed with the documentation:

* `one run on its own <https://goc-dx-u3.science.gc.ca/~dlo001/sites8/pikobs_doc_zone_exp/pikobs_zone_viewer.html>`__
* `G0 against G2 <https://goc-dx-u3.science.gc.ca/~dlo001/sites8/pikobs_doc_zone/pikobs_zone_viewer.html>`__, the operational suite as the control, with the comparison panels and the tests

How long a run takes, and how big a node to ask for: :doc:`runtime`.

----

1. How it works
===============

**Input check.** Every 6-h file of every run and family is looked up
first. If one is missing the run stops before touching ``PATHWORK``, says
which cycles are missing and which dates the directory does hold.

**One pass per file.** Each cycle is read once. Regions, criteria, levels
and the land/ocean split are all summed in that pass, as sums rather than
means, so combining cycles later is an addition and the sigma stays
exact.

**Matching, with a control.** The observations of the two runs are paired
on station, position, date, time and their rank inside the profile, and
only the pairs are kept. Both sides of a cell therefore rest on exactly
the same observations: a flag that differs between the runs cannot change
the sample under your feet. The cross sum of the pair is stored as well,
which is what makes the paired t-test possible.

**One grid per region.** Before drawing, the module collects every level
the family has in the period and puts every figure of a region on the
same grid: the latitudes of the region in bands of ``BOXSIZEY`` --
``Canada`` from 45 to 90, not a globe three quarters empty -- and the same
rows on the y axis. Two runs, or two experiences, line up band by band
when you flip between them. A polygon region is drawn on the whole globe.

**Shared colours.** Every figure of the same family, varno, function and
region gets the same colour scales: a pale red is the same value for one
station and for all of them, for one experience and for the next. The
scales follow the region rather than the most extreme one of the run, so
``Canada`` gets its own colours instead of the two darkest of the globe.

----

2. Configuration
================

Only the ``USER SETTINGS`` block of a wrapper is meant to be edited.

.. wrapper-settings:: run_zone_exp.sh run_zone_cont_exp.sh

With ``DATESTART`` and ``DATEEND`` empty, the window is worked out from
today: it ends ``DAYS_BACK_END`` days ago and covers ``WINDOW_DAYS`` days.
That is what a daily run wants, from a source that only keeps the last
days.

----

3. Stations and instrument types
================================

__STN_TOKENS__

A section is about latitude, so ``join`` is usually the right choice. On
``ai``, ``sf``, ``ua``, ``gp`` and ``csr`` a station id is one aircraft or one
radiosonde, and one figure each would say nothing: there ``all`` groups by
instrument type instead, as every module does (see :doc:`families`).

A selection that sits in a single latitude band is not drawn, and the log
lists which one and where. It is usually a geostationary satellite at the
edge of a small region, or an instrument type with very few stations.

For ``sw``, ``SPECIAL_COLUMN="on"`` splits the winds by method, infrared or
water vapour: two populations with different errors that a single figure
would average together.

----

4. Reading a figure
===================

One run gives three panels:

__PANELS_SINGLE__

With a control, five, all in one row and sharing the same y axis, so a
row can be followed from one panel to the next:

__PANELS_CMP__

__IMG_ZONE__

Everything follows the convention of Pikobs: **experience minus
control**, so a negative value is an improvement and is drawn in red;
blue is where the control was better.

The example above compares O-A, and on purpose. G0 and G2 are two passes
of the same operational cycle, G2 later and with more observations, and
they start from the same background: an observation both have gets the
same O-P in each, to the last bit, so every O-P panel of their comparison
is white. The analysis is where they part, and O-A shows it (the same
case is worked through in :doc:`scatter`).

The differences are in the units of the variable, not in percent. A
percentage of the control bias explodes wherever that bias is close to
zero: going from 0.01 to 0.07 m/s would read as +600 %, when it is six
hundredths of a metre per second. Inside ``+/- WHITE_BAND`` the cell is
white, so what is coloured is a change worth reading. On a variable
whose values are much smaller than the band -- the departures of
``ro`` are a few hundredths -- the band follows the data instead: a
tenth of its order of magnitude, and the colour bar says which.

Refractivity goes further: its sigma is 3 to 5 near the ground and a
few tenths above 6 km, and on a linear scale the upper half of the
figure was one colour. When the largest sigma of a figure is more than
five times the typical one, the scales go in 1-2-5 steps -- 0.1, 0.2,
0.5, 1, 2, 5 -- and the white band is at most a tenth of the typical
sigma, so the tenths aloft and the units below both read. Winds and
temperatures, whose sigma varies little, keep their linear scales.

The sample-size panel is not a comparison. With matched observations the
count is the same in both runs; it is there to read the tests against.

----

5. The tests
============

The sigma is tested with the Pitman-Morgan test and the bias with a paired t-test,
both from :mod:`pikobs.stats`, which explains them. The pairing matters
here: because both sides of a cell are the same observations, what the
two runs have in common cancels, and a small change can pass the test.
That is why the bias panel often lights up while the sigma one stays
grey on the same cells.

Two things to keep in mind. A cell with twenty observations will rarely
pass, however good the change; and one with two thousand will pass on a
change that may not matter. The sample-size panel is there to tell the
two apart.

----

6. The vertical axis
====================

__AXES__

The level comes from the ``VCOORD`` of the family, not from the raw
column: ``sw`` and ``ua`` round their pressure, and reading the column
directly would give thousands of levels where every other module has a
few tens. A family that rounds its pressure puts everything above its
first bin into the bin 0, which is labelled ``< 100`` rather than a 0 hPa
that does not exist.

With many channels the figure grows in height, 0.14 inch per row, so
that every channel keeps its number.

----

7. The viewer
=============

``pikobs_zone_viewer.html`` has one selector per dimension: Experience,
Family, Fonction, Region, Criteria, Station, Special, Channel, Land/ocean
and Varno. With several experiences each is its own comparison, ``A120 vs
CTL`` and ``A125 vs CTL``, and **Flip** switches between them on the same
grid and the same colours. Tall figures are shown at the full width of the
page; **W** switches between fitting the width and fitting the screen.

----

8. Output layout
================

::

   $PATHWORK/
   ├── pikobs_zone_viewer.html
   ├── zone_timing.json
   └── <family>/
       ├── zone_<tag>_<selection>_<start>_<end>_<family>.db
       └── zone_<runs>_<family>_<fonction>_varno<N>_<station>_<region>[_<surface>][_<special>]_<flag>_ch<mode>.png

The databases hold the sums per region, criteria, station, level,
latitude band and cycle, and can be queried with any SQLite client.

With ``SVG="on"`` each figure is written again as ``.svg`` beside its PNG,
for editing before a presentation.

----

9. Support
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
       .replace("__IMG_ZONE__", image("zone_comparison.png",
                                      "Five panels of a comparison, "
                                      "sharing the same levels"))
       .replace("__SETTINGS_EXP__",
                user_settings(f"{SCRIPTS}/run_zone_exp.sh"))
       .replace("__SETTINGS_CMP__",
                user_settings(f"{SCRIPTS}/run_zone_cont_exp.sh"))
       .replace("__VARIABLES__", VARIABLES)
       .replace("__PANELS_SINGLE__", PANELS_SINGLE)
       .replace("__PANELS_CMP__", PANELS_CMP)
       .replace("__STN_TOKENS__", STN_TOKENS)
       .replace("__AXES__", AXES)
       .replace("__TROUBLE__", TROUBLE))
assert not re.findall(r"__[A-Z_]+__", doc), re.findall(r"__[A-Z_]+__", doc)
assert '"""' not in doc

write_docstring(MODULE, doc, __file__)
print("docstring lines:", doc.count("\n"))
