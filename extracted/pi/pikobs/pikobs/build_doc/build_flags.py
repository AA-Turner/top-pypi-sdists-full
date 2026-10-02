"""Build the flags.py module docstring from its wrapper.

    python build_doc_flags.py pikobs/flags/flags.py pikobs/script [runtime_table.rst]
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
        ["``PATHWORK``", "Output directory, wiped per family at each run"],
        ["``DATESTART`` / ``DATEEND``", "Period, ``YYYYMMDDHH`` UTC, both ends included"],
        ["``REGION``", "Regions, one selector entry each (array)"],
        ["``FAMILY``", "Observation families (array)"],
        ["``ID_STN``", "Station tokens, see section 3 (array)"],
        ["``CHANNEL``", "``join``, ``all`` or an explicit list (array)"],
        ["``VARNOS``", "Optional varno list, empty = the family default"],
        ["``SVG``", "``on`` also writes each figure as SVG, for editing"],
["``N_CPUS``", "Number of Dask workers"],
    ])

BLOCKS = grid(
    ["Block", "What it shows"],
    [
        ["Header", "the variable, the period, the family, region, stations and channel, and the run"],
        ["Stacked bars", "one bar per 6-h cycle, the share of each flag combination"],
        ["Legend", "per combination: its bits, their meaning, its share of the period and its observations per cycle"],
        ["Table", "every observation once: assimilated with its combinations, not assimilated with its reasons, 100 % in all, with the counts"],
        ["Group lists", "each line of the table opened: its flag combinations, largest first, with a bar and the numbers"],
    ])

STN_TOKENS = grid(
    ["Token", "Figures produced"],
    [
        ["``join``", "one figure, every station pooled"],
        ["``all``", "one figure per station, per instrument type for ai, sf, ua, gp, csr"],
        ["``METOP`` or ``\"METOP*\"``", "the stations whose id starts with METOP, pooled"],
        ["``=METOP-1``", "that station only"],
        ["``N%``", "SQL ``LIKE`` pattern on the station id"],
    ])

TROUBLE = grid(
    ["Symptom", "Cause and fix"],
    [
        ["``ERROR: missing 6-h input files``",
         "At least one ``YYYYMMDDHH_<family>`` is missing; the report lists the gaps and the dates available."],
        ["The wrapper stops without a message",
         "``load_pikobs.sh`` failed; the guard in the wrapper prints it, otherwise run ``source`` by hand."],
        ["``nothing to plot, check the selectors``",
         "No row matched the tokens: check ``ID_STN`` and ``CHANNEL`` against the log lines that list them."],
        ["OTHER, NOT ASSIMILATED is large",
         "A reason is missing from ``REASONS_RADIANCE`` or ``REASONS_DEFAULT`` in ``pikobs/configobs/flag_groups.py``: the mouse over its rows gives the bits, add the reason."],
        ["``rarer flags not listed``",
         "The legend stops at 40 combinations; the bars still show all of them. Raise ``MAX_LEGEND_ENTRIES`` if you need more."],
        ["The bar chart looks like one colour",
         "One combination dominates. Open the figure full size in the viewer: the thin bands at the top are the rest."],
    ])

DOC = r'''
=========================================================
pikobs.flags -- Distribution of the quality-control flags
=========================================================

Every observation carries a 24-bit flag that says what quality control did
with it: bias corrected, blacklisted, rejected by the background check,
affected by clouds, assimilated. ``flags`` reads those bits and shows, for
every 6-h cycle, what share of the data ended up in each state. It is the
module to open when a suite suddenly assimilates less and nobody knows
why.

There is no ``FLAGS_CRITERIA`` here, on purpose: filtering by criteria is
what the other modules do, and this one exists to show the whole spectrum
at once.

Quick start
===========

.. code-block:: bash

   wget https://gitlab.science.gc.ca/dlo001/Pikobs/-/raw/master/pikobs/script/run_flags.sh
   chmod +x run_flags.sh

The wrapper runs on the node you are on and never submits to PBS, so open a
compute node first, edit the ``USER SETTINGS`` block and launch:

.. code-block:: bash

   qsub -I -lselect=1:ncpus=80:mem=185gb -lwalltime=2:0:0
   nano run_flags.sh
   ./run_flags.sh

.. warning::

   Do not run the wrapper on a login node: the extraction opens every 6-h
   file of the period in parallel.

.. important::

   Lists are **bash arrays**: ``FAMILY=(iasi cris)`` and
   ``ID_STN=(join all)``, not strings.

A run prints its phases and ends with the address of the viewer:

.. code-block:: text

   [flags] runs: experience
   [flags] id_stn tokens: ['join', 'all']
   [flags] channel tokens: ['join']
   [flags] input check OK: 29 cycles x 1 run(s) x 4 family(ies), 116 files, 31.8 GB
   [flags] extraction: 116 tasks, 80 worker(s)
   [pikobs] extraction: 116/116 (100%) 78s elapsed
   [flags] plots: 34 tasks
   [flags] -------------------- run time --------------------
   [flags] input           31.8 GB   116 files, 29 cycles, 1 run(s)
   [flags] extraction       78.4 s
   [flags] plots            41.2 s
   [flags] total           122.9 s   (2.0 min, 80 workers)
   Viewer: /home/dlo001/sites8/pikobs_flags/pikobs_flags_viewer.html
   Web:    to open it in a browser, link the folder under public_html once:
             ln -s /home/dlo001/sites8/pikobs_flags /home/dlo001/public_html/
           then: https://goc-dx-u3.science.gc.ca/~dlo001/pikobs_flags/pikobs_flags_viewer.html

`A live reference instance <https://goc-dx-u3.science.gc.ca/~dlo001/sites8/pikobs_doc_flags/pikobs_flags_viewer.html>`__.

How long a run takes, and how big a node to ask for: :doc:`runtime`.

----

1. How it works
===============

**Input check.** Every 6-h file of every run and family is looked up first.
If one is missing the run stops, says which cycles are missing and which
dates the directory does hold, and leaves ``PATHWORK`` untouched.

**Extraction.** Each file is read once and counted by station, varno,
channel and flag value; every region is a conditional sum inside that
single scan, so five regions cost almost what one costs. No criteria is
applied: the flag itself is the subject.

**Figures.** One task per (run, family, region, station selection,
channel, varno), spread over the workers.

----

2. Configuration
================

Only the ``USER SETTINGS`` block of the wrapper is meant to be edited.

.. wrapper-settings:: run_flags.sh

----

3. Choosing the stations and channels
=====================================

``ID_STN`` takes the tokens of the rest of Pikobs, and each one is its own
figure:

__STN_TOKENS__

``CHANNEL`` works the same way: ``join`` merges every channel into one
figure, ``all`` gives one figure per channel, and an explicit list keeps
only those. For a first look at a radiance family, ``ID_STN=(all)`` with
``CHANNEL=(join)`` is usually the right pair: one figure per satellite,
every channel together.

----

4. Reading a figure
===================

__BLOCKS__

__IMG_FLAGS__

The **bars** are normalised, so each cycle adds up to 100 %: what matters
is the share of each state, not the volume, and a sudden change of colour
in one cycle is what you are looking for. The bar width follows the
period: four months are 480 bars, and the figure grows accordingly, which
is why it is meant to be opened full size in the viewer.

The **colour of a flag combination is always the same**, in every figure
and every family, because it is derived from the flag value itself. Two
figures of the same satellite can therefore be compared by colour alone.

The **table** answers the question people actually come with: of what came
in, how much was used, and why was the rest not. Every observation is counted
once. With bit 12 set it is assimilated, and the table lists the combinations
it came with -- on ``sw`` almost all of it is plain 12, some 12+13 (the O-P
rogue check at level 1), and a handful 9+12+17: observations QC-Var kept with
a reduced weight. Without bit 12 an observation gets a reason, the first one
of the list that matches, so the reasons add up to what is not assimilated
and the whole table to 100 %.

An observation often carries several reasons at once, rejected and
erroneous, unselected and cloudy. That is what the second column is for.
*first reason* counts each observation under one reason only, the first in
the order of the list; *carries it* counts every observation that has the
reason, whatever came first. On IASI the first column puts most of the loss
on clouds, while the second shows that nearly everything not assimilated also
carries bit 11. Both are true: they answer different questions.

For a radiance the blacklist (bit 8) is taken out before anything else. Most
IASI channels are never meant to be assimilated, and counting them would
squash every other share to nothing, so the line above the table says how
many observations were left out and the shares are over the channels in use.
Tiny shares are written in scientific notation instead of being rounded to
0.00 %, and the ``obs`` column gives the counts, so any other ratio can be
worked out by hand.

The **group lists** under the table open each of its lines: ASSIMILATED and
every reason present, each split into its flag combinations, largest first,
with a bar as long as its share of the group and the numbers written beside
it. They replace the pies of the earlier versions, which had no way of
showing a slice of 0.02 % next to one of 80 %.

Groups and bits
---------------

The meaning of the 24 bits, and the reasons with their order, live in
``pikobs/configobs/flag_groups.py``, not in the plotting code.
``REASONS_RADIANCE`` serves the families on channels and ``REASONS_DEFAULT``
the others. Each entry is a combination and its title, and the order
matters: the first entry that matches is the reason of an observation.

.. code-block:: python

   REASONS_DEFAULT = _titled([
       ((0, 'or', 2, 'or', 9, 'n16'), "ERRONEOUS DATA"),
       ((8,),                         "BLACKLISTED"),
       ((9, 16),                      "BACKGROUND CHECK (O-P INNOVATION ROGUE CHECK)"),
       ((18,),                        "REJECTED OVER LAND DUE TO HIGHER TOPOGRAPHY"),
       ((11,),                        "REJECTED BY THINNING"),
       ((9, 'or', 17),                "REJECTED BY OVERALL QUALITY CONTROL"),
   ])

A combination is read as sets of conditions: ``(9, 16)`` means both bits,
``(0, 'or', 7)`` means either of them, and ``(9, 16, 'n8')`` adds that bit
8 must not be set. An observation with no bit at all goes to NO BIT SET, and
one that no reason explains to OTHER, NOT ASSIMILATED; if OTHER grows, a
reason is missing from the list.

What each of the 24 bits means, and which bits the criteria of the other
modules require (``assimilee``, ``bgckalt``, ``postalt`` ...), is on
:doc:`flags_criteria`.

----

5. The viewer
=============

``pikobs_flags_viewer.html`` has six dropdowns: Experience, Family, Region,
Station, Varno and Channel; each one only offers what exists for the
choices on its left. **Flip** (key ``F``) swaps between the current figure
and the previous one, and a click opens the figure at full size, which is
how a four-month bar chart is read.

Move the mouse over a band of the bars or a row of a group list and a box
says what it is: the cycle, the flag and its bits, what each bit means, how
many observations. This needs the viewer opened through its web address; a
page opened straight from the disk cannot read the small map file that sits
beside each figure.

----

6. Output layout
================

::

   $PATHWORK/
   ├── pikobs_flags_viewer.html
   ├── flags_timing.json
   └── <family>/
       ├── flags_<run>_<start>_<end>_<family>.db
       ├── flags_<run>_<family>_<region>[_<surface>][_<special>]_<stn>_ch<chan>_varno<varno>.png
       └── flags_<...>.png.map.json

Beside each figure, ``.map.json`` holds where every band of the bars and
every row of the group lists is in the image, with its text: it is what the
box under the mouse reads.

With ``SVG="on"`` each figure is written again as ``.svg`` beside its PNG,
for editing before a presentation: in Inkscape or Illustrator the titles,
the legends and the colours stay editable. The viewer always uses the PNG,
so turning it on changes nothing else. An SVG keeps every element of the
figure, so ask for it on the one or two figures you actually need.

The ``.db`` files hold one row per (region, station, varno, channel, flag,
cycle) in the table ``flag_observations`` and can be queried with
``sqlite3``, which is the quickest way to answer "how many observations had
bit 9 set last Tuesday".

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
       .replace("__IMG_FLAGS__", image("flags_plot.png",
                                       "Flag distribution: bars, legend, table "
                                       "and group lists"))
       .replace("__SETTINGS__", user_settings(f"{SCRIPTS}/run_flags.sh"))
       .replace("__VARIABLES__", VARIABLES)
       .replace("__BLOCKS__", BLOCKS)
       .replace("__STN_TOKENS__", STN_TOKENS)
       .replace("__TROUBLE__", TROUBLE))
assert not re.findall(r"__[A-Z_]+__", doc), re.findall(r"__[A-Z_]+__", doc)
assert '"""' not in doc

write_docstring(MODULE, doc, __file__)
print("docstring lines:", doc.count("\n"))
