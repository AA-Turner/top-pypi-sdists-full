#!/usr/bin/python3
# GENERATED -- this docstring is written by pikobs/build_doc/build_histogram.py.
# Edit that file and run ./pikobs_doc.sh; a change made here is lost.
r"""======================================================
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

+--------------+-----------------------------------------------------------------------+
| Part         | What it shows                                                         |
+==============+=======================================================================+
| Histogram    | the density of the run: counts divided by N and by the width of a bin |
+--------------+-----------------------------------------------------------------------+
| Dashed curve | the Gaussian of the same mean and sigma                               |
+--------------+-----------------------------------------------------------------------+
| Brown lines  | +/-3 sigma around the mean; the legend gives the share outside        |
+--------------+-----------------------------------------------------------------------+
| Statistics   | N, mean, sigma, skewness, excess kurtosis, share beyond 3 sigma       |
+--------------+-----------------------------------------------------------------------+
| Notes        | the Gaussian references, how the bins were merged, the units          |
+--------------+-----------------------------------------------------------------------+

.. image:: _static/histogram_single.png
   :alt: The distribution of one run
   :align: center
   :width: 100%

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

+------------+-------------------------------------------------------------------------+
| Part       | What it shows                                                           |
+============+=========================================================================+
| Histogram  | both densities on the same bins: control blue, experience red           |
+------------+-------------------------------------------------------------------------+
| Difference | experience minus control, bin by bin: red where the experience has more |
+------------+-------------------------------------------------------------------------+
| Statistics | the same table, one column per run                                      |
+------------+-------------------------------------------------------------------------+
| Tests      | mean, sigma and shape, with the verdict in the colour of the winner     |
+------------+-------------------------------------------------------------------------+

.. image:: _static/histogram_comparison.png
   :alt: An experience against a control
   :align: center
   :width: 100%

The example is O-A, and on purpose: G0 and G2 are two passes of the same
operational cycle and start from the same background, so their O-P is the
same observation by observation and the red histogram would sit exactly on
the blue one. The analysis is where they part (:doc:`scatter` works the
case through).

``MATCH`` decides which observations are compared:

+---------+---------------------------------------------+-----------------+----------------------------------------------------------+
| MATCH   | Observations                                | Tests           | Question it answers                                      |
+=========+=============================================+=================+==========================================================+
| ``on``  | the same in both runs, matched one by one   | paired t, F, KS | does the experience fit the same observations better?    |
+---------+---------------------------------------------+-----------------+----------------------------------------------------------+
| ``off`` | each run with all of its own, its own flags | Welch t, F, KS  | what happens with everything the experience assimilates? |
+---------+---------------------------------------------+-----------------+----------------------------------------------------------+

With ``on``, observations present in one run only are left out, and so
are new observations the experience brings. With ``off``, the header gives
the change in the number of observations, ``(+25.0 % in A120)``, and a
station only the experience has still gets its figure.

The difference panel is read by **where** each colour falls, not by the
colour alone:

+--------------------------------------------+-------------------------------------------------+
| Pattern of the difference panel            | Reading                                         |
+============================================+=================================================+
| red at the centre, blue on the shoulders   | the experience is narrower: better              |
+--------------------------------------------+-------------------------------------------------+
| blue at the centre, red on the shoulders   | the experience is wider: worse                  |
+--------------------------------------------+-------------------------------------------------+
| red on one side of zero, blue on the other | the distribution moves: the bias changes        |
+--------------------------------------------+-------------------------------------------------+
| red only far in the tails                  | the experience has more gross errors            |
+--------------------------------------------+-------------------------------------------------+
| scattered bars of a few 1e-4               | nothing: a handful of observations changing bin |
+--------------------------------------------+-------------------------------------------------+

Mind the power of ten in its label: ``[10-4]`` is a few observations.

----

5. The statistics
=================

+-------------------+----------+-------------------------------------------------------------------------------------------+
| Number            | Gaussian | Reading                                                                                   |
+===================+==========+===========================================================================================+
| skewness          | 0        | positive: the long tail is on the right; beyond about 0.5 the bias is not the whole story |
+-------------------+----------+-------------------------------------------------------------------------------------------+
| excess kurtosis   | 0        | positive: sharper peak, heavier tails, more gross errors than sigma suggests              |
+-------------------+----------+-------------------------------------------------------------------------------------------+
| beyond 3 sigma    | 0.27 %   | the weight of the tails, where the quality control decides                                |
+-------------------+----------+-------------------------------------------------------------------------------------------+
| sigma of omp_norm | 1        | above 1 the assigned errors are too small, below 1 too large                              |
+-------------------+----------+-------------------------------------------------------------------------------------------+

Pooling channels or levels of different sigmas -- ``CHANNEL=(join)`` on
IASI, all levels of ``ua`` -- gives a large kurtosis on its own, every
channel being Gaussian. Before concluding the errors are not Gaussian,
look at one channel or layer, or at ``omp_norm``: departures divided by the
error the system assigns to each observation. If those errors are right,
that histogram is the green N(0, 1) drawn beside it.

----

6. The tests
============

+--------------------+-----------------+------------------------------------------------------------------------------------------------------------------+
| Test               | On              | Reads                                                                                                            |
+====================+=================+==================================================================================================================+
| paired t / Welch t | the mean        | which run is closer to zero                                                                                      |
+--------------------+-----------------+------------------------------------------------------------------------------------------------------------------+
| Pitman-Morgan / F  | the sigma       | which run is narrower -- Pitman-Morgan on matched observations, F otherwise; with omp_norm, which is closer to 1 |
+--------------------+-----------------+------------------------------------------------------------------------------------------------------------------+
| Kolmogorov-Smirnov | the whole shape | D, the share of the observations on the other side                                                               |
+--------------------+-----------------+------------------------------------------------------------------------------------------------------------------+

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

.. image:: _static/histogram_qc_split.png
   :alt: One colour per flag combination
   :align: center
   :width: 100%

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

+--------------+---------------------------------------------------------------------+
| Token        | Histograms produced                                                 |
+==============+=====================================================================+
| ``join``     | one, every station together                                         |
+--------------+---------------------------------------------------------------------+
| ``all``      | one per station; on ai, sf, ua, gp and csr one per instrument type  |
+--------------+---------------------------------------------------------------------+
| ``C%``       | the stations whose id starts with C, together; the title lists them |
+--------------+---------------------------------------------------------------------+
| ``=METOP-1`` | that station only                                                   |
+--------------+---------------------------------------------------------------------+

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

import json
import math
import os
import shutil
import sys
import tempfile
import time
from typing import Any, Dict, List, Optional, Tuple

import dask
from dask.distributed import Client

import pikobs
from pikobs.figures import svg_enabled
from pikobs.obsdb import (check_input_files, combine as _combine_rows,
                          cycle_path, cycles as _cycles, fmt_bytes,
                          input_size, open_result, table_columns, work_db)
from pikobs.parallel import run_tasks
from pikobs.pbs_submit import maybe_submit_to_pbs
from pikobs.stations.stations import parse_station_tokens
from pikobs.web.viewer import generate_web
from pikobs.web.runs import runs_block
from pikobs.zone.zone import (RO_FAMILIES, _combinations, _distinct,
                              _is_composite, _is_land_function, _is_num,
                              _num, _ro_ref, _safe, _save_members,
                              _selections, _special, _special_label,
                              _split_tokens, _station_select)
from pikobs.zone.zone_plot import (LAND_OCEAN_CHOICES,
                                   level_selector_label)
from pikobs.histogram.histogram_plot import (MIN_OBS_PER_HISTOGRAM,
                                             histogram_plot_task)

# omp_norm and oma_norm divide the departure by the error the system
# assigns to the observation: if that error is right, the histogram is a
# normal distribution of sigma 1.
FUNCTIONS = ('omp', 'oma', 'omp_norm', 'oma_norm', 'omp_std', 'oma_std')

# The QC split stacks every observation that has an O-P by its flag
# combination: one colour per combination really present in the data,
# assimilated or not -- 12, 12+13, 9+16 with its O-P computed, 11 ... --
# so the histogram shows where each of them sits. The label gives the bits
# and the diagnosis of configobs.flags_criteria.flag_reason, the same words
# as the flags module. The most common combinations are drawn, the rest
# pooled, and the scan lists them in the log.
QC_MAX_CATEGORIES = 10
QC_OTHER = "OTHER COMBINATIONS"


def _register_reason(conn) -> None:
    from pikobs.configobs.flags_criteria import register_flag_reason
    register_flag_reason(conn)


def combo_label(sig: int) -> str:
    """'12+13  Assimilated': the bits, then the diagnosis."""
    try:
        from pikobs.configobs.flags_criteria import flag_reason
        reason = (flag_reason(sig) or "no QC flag").title()
    except Exception:                                      # pragma: no cover
        reason = ""
    bits = "+".join(str(b) for b in range(24) if sig >> b & 1) or "none"
    return f"{bits}  {reason}".strip()


def qc_categories(counts: Dict[int, int]) -> List[Tuple[int, str, float]]:
    """The most common combinations: [(signature, label, share %)]."""
    total = sum(counts.values())
    if not total:
        return []
    top = sorted(counts.items(), key=lambda kv: -kv[1])[:QC_MAX_CATEGORIES]
    return [(sig, combo_label(sig), 100.0 * n / total) for sig, n in top]


def _qc_case(categories, flag_col: str = "flag") -> str:
    """SQL naming the combination of an observation; the rare ones pooled."""
    if not categories:
        return "'all'"
    whens = " ".join(f"WHEN {int(sig)} THEN '{label.replace(chr(39), '')}'"
                     for sig, label, _ in categories)
    return f"(CASE ({flag_col} & {QC_MASK}) {whens} ELSE '{QC_OTHER}' END)"

# One twentieth of the sigma per bin, out to six sigmas on either side:
# some 240 bins, fine enough to see the shape, coarse enough to be filled.
BINS_PER_SIGMA = 20
SIGMAS_OUT = 6
SCAN_CYCLES = 4

_HIST_COLS = ("region, flag, land_ocean, id_stn, special, varno, lkey, "
              "fonction, qc, bin, n_ctl, n_exp")
_DDL_HIST = """
    CREATE TABLE IF NOT EXISTS hist (
        region TEXT, flag TEXT, land_ocean TEXT, id_stn TEXT, special TEXT,
        varno INTEGER, lkey TEXT, fonction TEXT, qc TEXT, bin INTEGER,
        n_ctl INTEGER, n_exp INTEGER
    );
"""
# Moments from the exact values, not from the bins: the mean and the
# sigma of a histogram would carry the rounding of its bins.
_MOM_COLS = ("region, flag, land_ocean, id_stn, special, varno, lkey, "
             "fonction, n, c1, c2, c3, c4, e1, e2, e3, e4, ce")
_DDL_MOM = """
    CREATE TABLE IF NOT EXISTS moments (
        region TEXT, flag TEXT, land_ocean TEXT, id_stn TEXT, special TEXT,
        varno INTEGER, lkey TEXT, fonction TEXT, n INTEGER,
        c1 FLOAT, c2 FLOAT, c3 FLOAT, c4 FLOAT,
        e1 FLOAT, e2 FLOAT, e3 FLOAT, e4 FLOAT, ce FLOAT
    );
"""
# Every flag combination of a selection, split by whether the observation
# has an O-P: those that have one are in the histogram, those that do not
# cannot be -- on a postalt file they are most of the rejected ones. The
# figure lists both, with their bits and their diagnosis. Bits 5, 6 and 10
# (interpolated, bias corrected, generated) record what was done to a
# value, not a quality decision, and are left out of the combination.
QC_INFO_BITS = (5, 6, 10)
QC_MASK = sum(1 << b for b in range(24) if b not in QC_INFO_BITS)
# sx and sxx are the sums of O-P over the observations of the
# combination, so the figure can say what the rejected ones looked like
# rather than only how many there were. A combination with no O-P leaves
# them NULL, which is the honest answer: there was nothing to average.
_FLAGCOMB_COLS = ("region, flag, land_ocean, id_stn, special, varno, lkey, "
                  "has_omp, sig, n, sx, sxx")
_DDL_FLAGCOMB = """
    CREATE TABLE IF NOT EXISTS flagcomb (
        region TEXT, flag TEXT, land_ocean TEXT, id_stn TEXT, special TEXT,
        varno INTEGER, lkey TEXT, has_omp INTEGER, sig INTEGER, n INTEGER,
        sx FLOAT, sxx FLOAT
    );
"""

_DDL_BINSPEC = """
    CREATE TABLE IF NOT EXISTS binspec (
        family TEXT, fonction TEXT, varno INTEGER, lkey TEXT, w FLOAT,
        kmin INTEGER, kmax INTEGER, PRIMARY KEY (family, fonction, varno, lkey)
    );
"""


def db_path(work_path: str, family: str, tag: str, date_start: str,
            date_end: str) -> str:
    return os.path.join(work_path, family,
                        f"histogram_{_safe(tag)}_{date_start}_{date_end}_"
                        f"{family}.db")


def _nice_width(value: float) -> float:
    """The round bin width just below value: 1, 2, 2.5 or 5 x 10^k."""
    if not value or not math.isfinite(value) or value <= 0:
        return 0.1
    mag = 10 ** math.floor(math.log10(value))
    for m in (5, 2.5, 2, 1):
        if m * mag <= value:
            return m * mag
    return mag


# Layers for the families on pressure or height. A histogram per level
# of the family would be dozens of near-identical figures -- the levels
# are fine so that zone has many rows -- so levels are grouped into layers
# with a meaning of their own. Pressure in hPa from the ground up, height
# in km; both can be changed from the wrapper.
# The layers come from the shared module, so a histogram of 850-500 hPa
# is the same slice of atmosphere as the profile and the map of the same
# experiment, and one change of the edges moves all three.
from pikobs.configobs.levels import (HEIGHT_LAYERS_KM, PRESSURE_LAYERS_HPA,
                                     layer_case as _layer_case,
                                     layer_of as _layer_of, layers_for)


def _level_key(vcoord_expr: str, channel_mode: str, layers=None) -> str:
    """The level of a row as text: 'join' when pooled, the layer on a
    pressure or height family, the value itself on channels."""
    if channel_mode == 'join':
        return "'join'"
    if layers:
        return _layer_case(vcoord_expr, layers)
    return f"printf('%g', {vcoord_expr})"


def _values(alias: str, fn: str, gpsro: bool, has_oma: bool,
            has_err: bool = False) -> str:
    """The value histogrammed.

    O-P or O-A, divided by B_ref for GPS-RO; or, for the _norm functions,
    divided by the error the system assigns to the observation. B_ref then
    cancels, so the normalised departure is the same with or without it.
    """
    base = fn.replace('_norm', '')
    a = f"{alias}." if alias else ""
    if base == 'oma' and not has_oma:
        return "NULL"
    if fn.endswith('_norm'):
        if not has_err:
            return "NULL"
        err = _num(f"{a}obs_error")
        return (f"(CASE WHEN {err} > 0 THEN {_num(a + base)} / {err} END)")
    if not gpsro:
        return _num(a + base)
    return f"({_num(a + base)} / ro_ref({a}vcoord))"


def _ro_gates(alias: str) -> str:
    """The quality gates of the operational GPS-RO verification."""
    a = f"{alias}." if alias else ""
    ref = f"ro_ref({a}vcoord)"
    return (f" AND {a}vcoord > -1000 AND {a}vcoord < 100000"
            f" AND ({a}obsvalue - {a}omp) > 0 AND ({a}obsvalue - {a}omp) < 500"
            f" AND {a}obsvalue / {ref} > 0.3 AND {a}obsvalue / {ref} < 3"
            f" AND {a}omp / {ref} > -0.05 AND {a}omp / {ref} < 0.05")


# ─────────────────────────────────────────────────────────────────────────────
# Scan: the sigma of every variable, to set its bins
# ─────────────────────────────────────────────────────────────────────────────

def scan_sigma(task: Dict[str, Any]) -> List[tuple]:
    """(family, varno, lkey, n, s, s2) of O-P in one cycle file."""
    family, path = task['family'], task['filein']
    if not os.path.isfile(path):
        return []
    FAM, VCOORD, VCOCRIT, STATB, element, VCOTYP = pikobs.family(family)
    vcoord_expr = (VCOORD or '').strip() or 'vcoord'
    if task['varnos']:
        element = ",".join(str(v) for v in task['varnos'])
    gpsro = family in RO_FAMILIES
    out = []
    try:
        with work_db(attach={'db': path}) as (conn, _):
            if gpsro:
                conn.create_function("ro_ref", 1, _ro_ref, deterministic=True)
            cols = table_columns(conn, 'DATA', 'db')
            gates = _ro_gates('') if gpsro else ""
            # always level by level: the pooled bins are built from these,
            # and a level whose O-P never changes has to be seen to be
            # left out
            lk = _level_key(vcoord_expr, 'all')
            if task.get('qc_split'):
                # every diagnosis, with and without O-P: a histogram of O-P
                # can only draw the first, but the second must be said
                for sig, n_with, n_without in conn.execute(f"""
                    SELECT (flag & {QC_MASK}),
                           SUM({_is_num('omp')}),
                           SUM(NOT {_is_num('omp')})
                    FROM db.data WHERE varno IN ({element}) {VCOCRIT}
                    GROUP BY 1;"""):
                    if n_with:
                        out.append(('F', family, int(sig), n_with))
                    if n_without:
                        out.append(('N', family, int(sig), n_without))
            # O-P always: the dead levels are found on it
            for fn in sorted(set(task['functions']) | {'omp'}):
                v = _values('', fn, gpsro, 'oma' in cols,
                            'obs_error' in cols)
                if v == "NULL":
                    continue
                out += [(family, fn) + tuple(r) for r in conn.execute(f"""
                    SELECT varno, {lk}, COUNT({v}), SUM({v}), SUM({v}*{v})
                    FROM db.header NATURAL JOIN db.data
                    WHERE varno IN ({element}) AND {_is_num('omp')}
                      AND {_is_num('obsvalue')} {VCOCRIT} {gates}
                    GROUP BY varno, {lk};""")]
                # a departure stored with a fixed step -- BURP keeps values
                # as integers with a scale, so O-P comes in steps of 0.01 K
                # -- is found here; a normalised one is not stepped
                if fn.endswith('_norm') or gpsro:
                    continue
                for (varno,) in conn.execute(
                        f"SELECT DISTINCT varno FROM db.data WHERE varno IN "
                        f"({element});").fetchall():
                    vals = [r[0] for r in conn.execute(
                        f"SELECT {v} FROM db.data WHERE varno = ? AND "
                        f"{_is_num(fn.replace('_norm', ''))} LIMIT 50000;",
                        (varno,)).fetchall()]
                    q = _quantum(vals)
                    if q:
                        out.append(('Q', family, fn, varno, q))
    except Exception as exc:
        print(f"[histogram] scan of {os.path.basename(path)} failed: {exc}",
              file=sys.stderr, flush=True)
    return out


def _quantum(values) -> Optional[float]:
    """The step of stored values, if they come in steps; None otherwise.

    The smallest gap between distinct values is a candidate; it is the step
    when nearly every other gap is a whole multiple of it. A bin width that
    is not a multiple of the step catches one possible value more in some
    bins than in their neighbours, and the histogram shows a saw tooth.
    """
    import numpy as np
    raw = np.asarray([x for x in values if x is not None], float)
    raw = raw[np.isfinite(raw)]
    if len(raw) < 50:
        return None
    # round to the scale of the values first: a value that went through a
    # 32-bit float is 0.29999995 or 0.3000001, and those are one value.
    # Five significant digits of the typical size keep any real step
    # (0.1 m/s, 0.01 K, or 1e-9 mol/mol for ozone) and merge that noise
    scale = float(np.median(np.abs(raw[raw != 0]))) if np.any(raw != 0) else 0
    if scale <= 0:
        return None
    res = 10 ** (np.floor(np.log10(scale)) - 4)
    v = np.unique(np.round(raw / res) * res)
    if len(v) < 50:
        return None
    gaps = np.diff(v)
    gaps = gaps[gaps > 0]
    if not len(gaps):
        return None
    q = float(np.min(gaps))
    # a gap no larger than the rounding just applied is the rounding itself,
    # not a step of the data: continuous values end up here
    if q < 10 * res:
        return None
    ratio = gaps / q
    whole = np.abs(ratio - np.round(ratio)) < 0.02
    if whole.mean() <= 0.97:
        return None
    # the values went through 32-bit floats on their way from BURP, so a
    # step of 0.1 is seen as 0.0999985 or 0.1000006: take the round value
    # it stands for, 1, 2 or 5 times a power of ten, when it is that close
    mag = 10 ** np.floor(np.log10(q))
    for m in (1, 2, 5, 10):
        snap = m * mag
        if abs(q - snap) / snap < 1e-3:
            return float(round(snap, 12))
    return q


def _spec(fam, fn, varno, lkey, n, s, s2, quantum=None):
    mean = s / n
    sigma = math.sqrt(max(s2 / n - mean * mean, 0.0))
    if sigma <= 0:
        return None
    w = _nice_width(sigma / BINS_PER_SIGMA)
    if quantum:
        # a whole number of steps per bin, never less than one
        w = round(max(1, round(w / quantum)) * quantum, 12)
    return (fam, fn, varno, lkey, w,
            math.floor((mean - SIGMAS_OUT * sigma) / w),
            math.ceil((mean + SIGMAS_OUT * sigma) / w))


def bin_specs(scans, modes, layers_by_family=None
              ) -> Tuple[List[tuple], List[tuple]]:
    """The bins of every level, of the pooled levels, and the dead levels.

    A dead level is one where O-P is the same number for every
    observation -- a level the system does not use, stored as 0. It has no
    distribution, and pooled with the others it would draw a spike at
    zero, so it is left out everywhere.
    """
    acc: Dict[tuple, List[float]] = {}
    quanta: Dict[tuple, float] = {}
    rows = []
    for row in scans:
        if row[0] in ('F', 'N'):
            continue
        if row[0] == 'Q':
            _, fam, fn, varno, q = row
            key = (fam, fn, varno)
            quanta[key] = min(quanta.get(key, q), q)
        else:
            rows.append(row)
    for fam, fn, varno, lkey, n, s, s2 in rows:
        if not n:
            continue
        a = acc.setdefault((fam, fn, varno, lkey), [0, 0.0, 0.0])
        a[0] += n
        a[1] += s or 0.0
        a[2] += s2 or 0.0
    # dead levels first, from O-P: left out of every function
    dead = [(fam, varno, lkey) for (fam, fn, varno, lkey), (n, s, s2)
            in acc.items() if fn == 'omp'
            and _spec(fam, fn, varno, lkey, n, s, s2) is None]
    dead_set = set(dead)
    specs = []
    pooled: Dict[tuple, List[float]] = {}
    by_layer: Dict[tuple, List[float]] = {}
    layers_by_family = layers_by_family or {}
    for (fam, fn, varno, lkey), (n, s, s2) in acc.items():
        if (fam, varno, lkey) in dead_set:
            continue
        layers = layers_by_family.get(fam)
        if 'all' in modes:
            if layers:
                try:
                    label = _layer_of(float(lkey), layers)
                except ValueError:
                    label = None
                if label:
                    a = by_layer.setdefault((fam, fn, varno, label),
                                            [0, 0.0, 0.0])
                    a[0] += n
                    a[1] += s
                    a[2] += s2
            else:
                spec = _spec(fam, fn, varno, lkey, n, s, s2,
                             quanta.get((fam, fn, varno)))
                if spec:
                    specs.append(spec)
        p = pooled.setdefault((fam, fn, varno), [0, 0.0, 0.0])
        p[0] += n
        p[1] += s
        p[2] += s2
    for (fam, fn, varno, label), (n, s, s2) in by_layer.items():
        spec = _spec(fam, fn, varno, label, n, s, s2,
                     quanta.get((fam, fn, varno)))
        if spec:
            specs.append(spec)
    if 'join' in modes:
        for (fam, fn, varno), (n, s, s2) in pooled.items():
            spec = _spec(fam, fn, varno, 'join', n, s, s2,
                         quanta.get((fam, fn, varno)))
            if spec:
                specs.append(spec)
    for (fam, fn, varno), q in sorted(quanta.items()):
        print(f"[histogram] {fam} {fn} varno {varno}: values stored in steps "
              f"of {q:g}; bins are whole multiples of it", flush=True)
    return specs, dead


# ─────────────────────────────────────────────────────────────────────────────
# Extraction
# ─────────────────────────────────────────────────────────────────────────────

def _bin_expr(v: str) -> str:
    """The bin of a value, the ends folded into two overflow bins.

    The tiny margin keeps a stepped value that sits exactly on a bin edge
    -- -0.06 with bins of 0.02 -- in its own bin whatever the rounding of
    the division: without it, one side of zero loses values to the next.
    """
    return (f"MIN(MAX(CAST(floor({v} / b.w + 1e-6) AS INTEGER), "
            f"b.kmin - 1), b.kmax + 1)")


def _prepare(conn, task, specs, dead=()):
    conn.execute(_DDL_HIST)
    conn.execute(_DDL_MOM)
    conn.execute("CREATE TEMP TABLE dead (d_varno INTEGER, d_lkey TEXT);")
    conn.executemany("INSERT INTO dead VALUES (?, ?);",
                     [d[1:] for d in dead if d[0] == task['family']])
    # looked up once per row: without an index every row scanned the list
    conn.execute("CREATE INDEX dead_key ON dead (d_varno, d_lkey);")
    # names of their own, so they never clash with the columns of the data
    conn.execute("CREATE TEMP TABLE b (b_fn TEXT, b_varno INTEGER, "
                 "b_lkey TEXT, w FLOAT, kmin INTEGER, kmax INTEGER);")
    conn.executemany("INSERT INTO b VALUES (?, ?, ?, ?, ?, ?);",
                     [s[1:] for s in specs if s[0] == task['family']])
    # the bins of every row come from here: with hundreds of channels
    # (iasi) a lookup without an index cost minutes per file
    conn.execute("CREATE INDEX b_key ON b (b_fn, b_varno, b_lkey);")
    # and the queries join it as "rows CROSS JOIN b": SQLite then walks the
    # rows once and looks each bin up here. With a plain JOIN it chose the
    # other way round -- every row scanned once per channel, minutes on iasi.
    if any(lo != 'all' for lo in task['land_oceans']):
        conn.create_function("is_land_sql", 2,
                             _is_land_function(task['pathwork']))
    # a polygon region (hrdps, the EMET domains) is an SQL function of its
    # own: without it a polygon stopped the extraction
    from pikobs.configobs import regionsobs
    regionsobs.register(conn, list(task.get('regions') or []))


def _alive(level_expr: str) -> str:
    return (f" AND NOT EXISTS (SELECT 1 FROM dead WHERE d_varno = varno "
            f"AND d_lkey = printf('%g', {level_expr}))")


def create_hist_single(task: Dict[str, Any], specs, dead=()) -> Optional[int]:
    family, path = task['family'], task['filein']
    if not os.path.isfile(path):
        print(f"[histogram] missing file, skipped: {path}", file=sys.stderr,
              flush=True)
        return None
    FAM, VCOORD, VCOCRIT, STATB, element, VCOTYP = pikobs.family(family)
    vcoord_expr = (VCOORD or '').strip() or 'vcoord'
    if task['varnos']:
        element = ",".join(str(v) for v in task['varnos'])
    gpsro = family in RO_FAMILIES

    with work_db(attach={'db': path}) as (conn, mem_uri):
        _prepare(conn, task, specs, dead)
        if gpsro:
            conn.create_function("ro_ref", 1, _ro_ref, deterministic=True)
        cols = table_columns(conn, 'DATA', 'db')
        head = table_columns(conn, 'HEADER', 'db')
        sp_sel, sp_grp = _special(family, head, task['special_on'])
        codtyp = "codtyp" if 'codtyp' in head else "NULL"
        stn_sel, stn_grp = _station_select(task['stn_label'], family, codtyp)
        gates = _ro_gates('') if gpsro else ""

        # the rows every histogram and moment of this file reads, copied once:
        # the passes below (modes x regions x criteria x functions) walk this
        # table instead of joining the whole file again each time
        import re as _re
        import time as _time
        _t0 = _time.time()
        _combos = list(_combinations(task['regions'], task['flags'], ['all'],
                                     task['land_oceans'], vcoord_expr))
        _frag = " ".join(
            [stn_sel, sp_sel, stn_grp or "", sp_grp or "", vcoord_expr,
             VCOCRIT or "", gates, task['id_stn_sql'] or "",
             _alive(vcoord_expr)]
            + [_level_key(vcoord_expr, 'join' if m == 'join' else 'all',
                          task.get('layers')) for m in task['channels']]
            + [c['cond'] for c in _combos]
            + [_values('', fn, gpsro, 'oma' in cols, 'obs_error' in cols)
               for fn in task['functions']])
        _need = [c for c in dict.fromkeys(list(head) + list(cols))
                 if c.lower() in ('varno', 'flag', 'omp', 'obsvalue', 'vcoord')
                 or _re.search(rf"\b{_re.escape(c)}\b", _frag, _re.I)]
        conn.execute(f"""
            CREATE TEMP TABLE r AS
            SELECT {", ".join(_need)}
            FROM db.header NATURAL JOIN db.data
            WHERE varno IN ({element}) AND {_is_num('omp')}
              AND {_is_num('obsvalue')} {VCOCRIT} {task['id_stn_sql']};""")
        _t1 = _time.time()

        for mode in task['channels']:
            lk = _level_key(vcoord_expr, 'join' if mode == 'join' else 'all',
                            task.get('layers'))
            chan_sql = ("" if mode in ('all', 'join')
                        else f" AND {vcoord_expr} = {float(mode)}")
            for combo in _combinations(task['regions'], task['flags'],
                                       ['all'], task['land_oceans'],
                                       vcoord_expr):
                labels = (f"'{combo['region']}', '{combo['flag']}', "
                          f"'{combo['land_ocean']}', {stn_sel}, {sp_sel}")
                grp = ", ".join(t for t in (stn_grp, sp_grp) if t)
                grp = (grp + ", " if grp else "")
                if task.get('qc_split'):
                    qc = _qc_case(task.get('qc_categories'))
                    conn.execute(_DDL_FLAGCOMB)
                    has = (f"({_is_num('omp')} AND "
                           f"{_is_num('obsvalue')})")
                    conn.execute(f"""
                        INSERT INTO flagcomb ({_FLAGCOMB_COLS})
                        SELECT {labels}, varno, {lk}, {has} AS h,
                               (flag & {QC_MASK}) AS sg, COUNT(*),
                               SUM(CASE WHEN {_is_num('omp')} THEN omp END),
                               SUM(CASE WHEN {_is_num('omp')}
                                        THEN omp * omp END)
                        FROM db.header NATURAL JOIN db.data
                        WHERE varno IN ({element})
                          {VCOCRIT} {chan_sql}
                          {task['id_stn_sql']} AND {combo['cond']}
                        GROUP BY {grp} varno, {lk}, h, sg;""")
                else:
                    qc = "'all'"
                for fn in task['functions']:
                    v = _values('', fn, gpsro, 'oma' in cols,
                                'obs_error' in cols)
                    if v == "NULL":
                        continue
                    base = f"""
                        FROM r
                        CROSS JOIN b ON b.b_fn = '{fn}' AND b.b_varno = varno AND b.b_lkey = {lk}
                        WHERE varno IN ({element}) AND {_is_num('omp')}
                          AND {_is_num('obsvalue')} AND {v} IS NOT NULL
                          {VCOCRIT} {gates} {chan_sql}
                          {_alive(vcoord_expr)}
                          {task['id_stn_sql']} AND {combo['cond']}"""
                    conn.execute(f"""
                        INSERT INTO hist ({_HIST_COLS})
                        SELECT {labels}, varno, {lk}, '{fn}', {qc} AS q,
                               {_bin_expr(v)} AS k, COUNT(*), 0
                        {base}
                        GROUP BY {grp} varno, {lk}, q, k;""")
                    conn.execute(f"""
                        INSERT INTO moments ({_MOM_COLS})
                        SELECT {labels}, varno, {lk}, '{fn}', COUNT(*),
                               SUM({v}), SUM({v}*{v}), SUM({v}*{v}*{v}),
                               SUM({v}*{v}*{v}*{v}),
                               NULL, NULL, NULL, NULL, NULL
                        {base}
                        GROUP BY {grp} varno, {lk};""")
        if os.environ.get("PIKOBS_TIMING"):
            _n = conn.execute("SELECT COUNT(*) FROM r;").fetchone()[0]
            print(f"[histogram timing] {family} (no pairs): copy "
                  f"{_t1 - _t0:.1f}s ({_n} rows), passes "
                  f"{_time.time() - _t1:.1f}s", file=sys.stderr, flush=True)
        _combine_rows(task['db_new'], mem_uri, 'hist', _HIST_COLS,
                      ddl=_DDL_HIST, module='histogram')
        _combine_rows(task['db_new'], mem_uri, 'moments', _MOM_COLS,
                      ddl=_DDL_MOM, module='histogram')
        if task.get('qc_split'):
            _combine_rows(task['db_new'], mem_uri, 'flagcomb',
                          _FLAGCOMB_COLS, ddl=_DDL_FLAGCOMB,
                          module='histogram')
        if task['stn_label'] and task['stn_label'] != 'join' \
                and not _is_composite(family):
            _save_members(task['db_new'], task['stn_label'], conn.execute(
                f"SELECT DISTINCT id_stn FROM db.header WHERE 1=1 "
                f"{task['id_stn_sql']};").fetchall())
        return 1


def create_hist_matched(task: Dict[str, Any], specs,
                        dead=()) -> Optional[int]:
    """Both runs on the same observations: matched by station, position,
    time, varno and level, as in scatter, zone and verifprofile."""
    family = task['family']
    for path in (task['ctl_file'], task['exp_file']):
        if not os.path.isfile(path):
            print(f"[histogram] missing file, skipped: {path}",
                  file=sys.stderr, flush=True)
            return None
    FAM, VCOORD, VCOCRIT, STATB, element, VCOTYP = pikobs.family(family)
    vcoord_expr = (VCOORD or '').strip() or 'vcoord'
    if task['varnos']:
        element = ",".join(str(v) for v in task['varnos'])
    gpsro = family in RO_FAMILIES
    from pikobs.match import (DEFAULT_KEY, MatchSpec, count_repeats,
                              key_aliases, key_join, key_select)
    spec = MatchSpec(True, tuple(task.get('match_fields') or DEFAULT_KEY))
    kc = key_select(spec, 'ch', 'cd')
    ke = key_select(spec, 'eh', 'ed')
    join_on = key_join(spec, 'e', 'c')
    names = tuple(task.get('names') or ('control', 'experience'))

    with work_db(attach={'ctl': task['ctl_file'],
                         'exp': task['exp_file']}) as (conn, mem_uri):
        _prepare(conn, task, specs, dead)
        if gpsro:
            conn.create_function("ro_ref", 1, _ro_ref, deterministic=True)
        ccols = table_columns(conn, 'DATA', 'ctl')
        ecols = table_columns(conn, 'DATA', 'exp')
        chead = table_columns(conn, 'HEADER', 'ctl')
        sp_sel, _ = _special(family, chead, task['special_on'], "ch.")
        codtyp = "ch.codtyp" if 'codtyp' in chead else "NULL"
        vcd = vcoord_expr.replace("vcoord", "cd.vcoord") \
            if vcoord_expr != 'vcoord' else "cd.vcoord"

        import time as _time
        _t0 = _time.time()
        conn.execute(f"""
            CREATE TEMP TABLE c AS
            SELECT {kc}, ch.id_stn AS id_stn, ROUND(ch.lat, 4) AS klat,
                   ROUND(ch.lon, 4) AS klon, ch.lat AS lat, ch.lon AS lon,
                   ch.DATE AS date, ch.TIME AS time, cd.varno AS varno,
                   cd.vcoord AS vraw, {vcd} AS lev, cd.flag AS flag,
                   {sp_sel} AS special, {codtyp} AS codtyp,
                   {_values('cd', 'omp', gpsro, True)} AS omp,
                   {_values('cd', 'oma', gpsro, 'oma' in ccols)} AS oma,
                   {_values('cd', 'omp_norm', gpsro, True,
                            'obs_error' in ccols)} AS omp_norm,
                   {_values('cd', 'oma_norm', gpsro, 'oma' in ccols,
                            'obs_error' in ccols)} AS oma_norm
            FROM ctl.header ch JOIN ctl.data cd USING(id_obs)
            WHERE cd.varno IN ({element}) AND {_is_num('cd.omp')}
              AND {_is_num('cd.obsvalue')} {VCOCRIT.replace('vcoord', 'cd.vcoord')}
              {_ro_gates('cd') if gpsro else ''};
        """)
        _t1 = _time.time()
        conn.execute(f"""
            CREATE TEMP TABLE e AS
            SELECT {ke}, eh.id_stn AS id_stn, ROUND(eh.lat, 4) AS klat,
                   ROUND(eh.lon, 4) AS klon, eh.DATE AS date,
                   eh.TIME AS time, ed.varno AS varno, ed.vcoord AS vraw,
                   {_values('ed', 'omp', gpsro, True)} AS omp,
                   {_values('ed', 'oma', gpsro, 'oma' in ecols)} AS oma,
                   {_values('ed', 'omp_norm', gpsro, True,
                            'obs_error' in ecols)} AS omp_norm,
                   {_values('ed', 'oma_norm', gpsro, 'oma' in ecols,
                            'obs_error' in ecols)} AS oma_norm
            FROM exp.header eh JOIN exp.data ed USING(id_obs)
            WHERE ed.varno IN ({element}) AND {_is_num('ed.omp')}
              AND {_is_num('ed.obsvalue')}
              {_ro_gates('ed') if gpsro else ''};
        """)
        _t2 = _time.time()
        conn.execute(f"CREATE INDEX e_key ON e "
                     f"({', '.join(key_aliases(spec))});")
        repeats = {names[0]: count_repeats(conn, 'c', spec),
                   names[1]: count_repeats(conn, 'e', spec)}
        _t3 = _time.time()
        conn.execute(f"""
            CREATE TEMP TABLE pairs AS
            SELECT c.id_stn AS id_stn, c.lat AS lat, c.lon AS lon,
                   c.varno AS varno, c.lev AS lev, c.flag AS flag,
                   c.special AS special, c.codtyp AS codtyp,
                   c.omp AS c_omp, e.omp AS e_omp,
                   c.oma AS c_oma, e.oma AS e_oma,
                   c.omp_norm AS c_omp_norm, e.omp_norm AS e_omp_norm,
                   c.oma_norm AS c_oma_norm, e.oma_norm AS e_oma_norm
            FROM c JOIN e ON {join_on};
        """)
        _t4 = _time.time()
        n_pairs = conn.execute("SELECT COUNT(*) FROM pairs;").fetchone()[0]
        if not n_pairs:
            return {'pairs': 0, 'repeats': repeats}

        stn_sel, stn_grp = _station_select(task['stn_label'], family,
                                           "codtyp")
        grp = (stn_grp + ", ") if stn_grp else ""
        for mode in task['channels']:
            lk = _level_key('lev', 'join' if mode == 'join' else 'all',
                            task.get('layers'))
            chan_sql = ("" if mode in ('all', 'join')
                        else f" AND lev = {float(mode)}")
            for combo in _combinations(task['regions'], task['flags'],
                                       ['all'], task['land_oceans'], 'lev'):
                labels = (f"'{combo['region']}', '{combo['flag']}', "
                          f"'{combo['land_ocean']}', {stn_sel}, special")
                for fn in task['functions']:
                    cv, ev = f"c_{fn}", f"e_{fn}"
                    base = f"""
                        FROM pairs CROSS JOIN b ON b.b_fn = '{fn}' AND b.b_varno = varno AND b.b_lkey = {lk}
                        WHERE {cv} IS NOT NULL AND {ev} IS NOT NULL
                          {chan_sql} {_alive('lev')} {task['id_stn_sql']}
                          AND {combo['cond']}"""
                    conn.execute(f"""
                        INSERT INTO hist ({_HIST_COLS})
                        SELECT r, f, lo, s, sp, varno, lk, '{fn}', 'all', k,
                               SUM(nc), SUM(ne)
                        FROM (
                            SELECT '{combo['region']}' AS r,
                                   '{combo['flag']}' AS f,
                                   '{combo['land_ocean']}' AS lo,
                                   {stn_sel} AS s, special AS sp, varno,
                                   {lk} AS lk, {_bin_expr(cv)} AS k,
                                   1 AS nc, 0 AS ne
                            {base}
                            UNION ALL
                            SELECT '{combo['region']}', '{combo['flag']}',
                                   '{combo['land_ocean']}', {stn_sel},
                                   special, varno, {lk}, {_bin_expr(ev)},
                                   0, 1
                            {base}
                        )
                        GROUP BY r, f, lo, s, sp, varno, lk, k;""")
                    conn.execute(f"""
                        INSERT INTO moments ({_MOM_COLS})
                        SELECT {labels}, varno, {lk}, '{fn}', COUNT(*),
                               SUM({cv}), SUM({cv}*{cv}),
                               SUM({cv}*{cv}*{cv}), SUM({cv}*{cv}*{cv}*{cv}),
                               SUM({ev}), SUM({ev}*{ev}),
                               SUM({ev}*{ev}*{ev}), SUM({ev}*{ev}*{ev}*{ev}),
                               SUM({cv}*{ev})
                        {base}
                        GROUP BY {grp} special, varno, {lk};""")
        _t5 = _time.time()
        if os.environ.get("PIKOBS_TIMING"):
            print(f"[histogram timing] {family}: copy ctl {_t1 - _t0:.1f}s, "
                  f"copy exp {_t2 - _t1:.1f}s, index+repeats {_t3 - _t2:.1f}s, "
                  f"pairs {_t4 - _t3:.1f}s ({n_pairs} pairs), "
                  f"histograms {_t5 - _t4:.1f}s", file=sys.stderr, flush=True)
        _combine_rows(task['db_new'], mem_uri, 'hist', _HIST_COLS,
                      ddl=_DDL_HIST, module='histogram')
        _combine_rows(task['db_new'], mem_uri, 'moments', _MOM_COLS,
                      ddl=_DDL_MOM, module='histogram')
        if task['stn_label'] and task['stn_label'] != 'join' \
                and not _is_composite(family):
            _save_members(task['db_new'], task['stn_label'], conn.execute(
                f"SELECT DISTINCT id_stn FROM pairs WHERE 1=1 "
                f"{task['id_stn_sql']};").fetchall())
        return {'pairs': n_pairs, 'repeats': repeats}


def _extract_task(task, specs, dead=()) -> Optional[int]:
    import traceback
    try:
        if task.get('ctl_file'):
            return create_hist_matched(task, specs, dead)
        return create_hist_single(task, specs, dead)
    except Exception:
        print(f"[histogram] extraction failed for "
              f"{task.get('filein') or task.get('ctl_file')}:\n"
              f"{traceback.format_exc()}", file=sys.stderr, flush=True)
        return None


def _finish_db(path: str, specs) -> Optional[str]:
    """Index the result, and keep the bins with it for the figures."""
    try:
        with open_result(path) as conn:
            conn.execute(_DDL_BINSPEC)
            conn.executemany("INSERT OR REPLACE INTO binspec VALUES "
                             "(?, ?, ?, ?, ?, ?, ?);", specs)
            for table in ('hist', 'moments'):
                conn.execute(f"CREATE INDEX IF NOT EXISTS idx_{table} ON "
                             f"{table} (region, flag, land_ocean, id_stn, "
                             f"special, varno, lkey, fonction);")
            # the flag table is read once per figure: without an index
            # every figure walked through all of it
            if conn.execute("SELECT 1 FROM sqlite_master WHERE type = "
                            "'table' AND name = 'flagcomb';").fetchone():
                conn.execute("CREATE INDEX IF NOT EXISTS idx_flagcomb ON "
                             "flagcomb (region, flag, land_ocean, id_stn, "
                             "special, varno, lkey);")
        return path
    except Exception as exc:
        print(f"[histogram] finishing {path} failed: {exc}", file=sys.stderr,
              flush=True)
        return None


# ─────────────────────────────────────────────────────────────────────────────
# Orchestrator
# ─────────────────────────────────────────────────────────────────────────────

# How to read every number of the figures, shown in the viewer.
_GLOSSARY = """
<br><br><b>How to read a figure</b>
<table style="margin:8px auto;border-collapse:collapse;text-align:left;
font-size:12px;color:inherit;max-width:1100px">
<tr><td style="padding:3px 10px;vertical-align:top"><b>density</b></td>
<td style="padding:3px 10px">the count of a bin divided by the number of
observations and by the width of the bin, so two runs of different size
compare on the same footing. The vertical axis is logarithmic by default:
the tails, where the quality control decides, would be invisible
otherwise.</td></tr>
<tr><td style="padding:3px 10px;vertical-align:top"><b>dashed curve</b></td>
<td style="padding:3px 10px">the Gaussian of the same mean and sigma.
Where the histogram rises above it in the tails, the errors are not
Gaussian.</td></tr>
<tr><td style="padding:3px 10px;vertical-align:top"><b>+/-3 sigma</b></td>
<td style="padding:3px 10px">the brown lines. A Gaussian leaves 0.27 % of
its observations outside; the share the data leaves there is the weight
of its tails.</td></tr>
<tr><td style="padding:3px 10px;vertical-align:top"><b>skewness</b></td>
<td style="padding:3px 10px">the asymmetry. 0 for a Gaussian; positive when
the long tail is on the right (more large positive departures), negative
when it is on the left. Beyond about 0.5 the bias is not the whole
story.</td></tr>
<tr><td style="padding:3px 10px;vertical-align:top"><b>excess kurtosis</b></td>
<td style="padding:3px 10px">how heavy the tails are against a Gaussian,
which has 0. Positive: a sharper peak and heavier tails, more gross
errors than the sigma suggests. Pooling channels or levels of different
sigmas gives a large value on its own, with every channel Gaussian:
look at one channel, or at the normalised departures, before concluding.
</td></tr>
<tr><td style="padding:3px 10px;vertical-align:top"><b>(O-P) / sigma_o</b></td>
<td style="padding:3px 10px">the departure divided by the error the system
assigns to the observation. If that error is right, the histogram is the
green N(0, 1): a sigma above 1 means the assigned error is too small,
below 1 too large.</td></tr>
<tr><td style="padding:3px 10px;vertical-align:top"><b>tests</b></td>
<td style="padding:3px 10px">from pikobs.stats, at 95 %: the paired
t-test on the mean, Pitman-Morgan on the sigma (Welch and F when the
runs are not matched), and Kolmogorov-Smirnov on
the whole shape. KS gives D, the share of the observations on the other
side, 0.01 = 1 %: read D first, since with a season of data any shape
change is significant.</td></tr>
<tr><td style="padding:3px 10px;vertical-align:top"><b>QC split</b></td>
<td style="padding:3px 10px">with QC_SPLIT on, every observation that has
an O-P is in the histogram, assimilated or not, one colour per flag
combination: 12 in blue, 12+13, 11, 9+16 ... each in its own colour, so it
shows where each of them sits. The label gives the bits and the diagnosis
of flag_reason. The table on the right lists every combination with the
meaning of each bit, and those left out because they have no O-P.</td></tr>
</table>"""


def _report_timing(timing, pathwork) -> None:
    sec, p = timing['seconds'], "[histogram]"
    print(f"{p} -------------------- run time --------------------",
          flush=True)
    print(f"{p} input        {fmt_bytes(timing['input_bytes']):>10s}   "
          f"{timing['input_files']} files, {timing['cycles']} cycles, "
          f"{timing['runs']} run(s)", flush=True)
    for phase in ('scan', 'extraction', 'plots'):
        if phase in sec:
            print(f"{p} {phase:<12s} {sec[phase]:>8.1f} s", flush=True)
    print(f"{p} total        {sec['total']:>8.1f} s   "
          f"({sec['total'] / 60:.1f} min, {timing['n_cpus']} workers)",
          flush=True)
    try:
        with open(os.path.join(pathwork, "histogram_timing.json"), "w") as fh:
            json.dump(timing, fh, indent=1)
    except OSError:
        pass


def make_histogram(runs, pathwork, datestart, dateend, regions, families,
                   flags_criteria, functions, varnos, id_stn, channel,
                   land_ocean, n_cpu, control=None, svg: bool = False,
                   min_obs: int = MIN_OBS_PER_HISTOGRAM,
                   special_on: bool = True, log_scale: bool = True,
                   qc_split: bool = False,
                   pressure_layers=PRESSURE_LAYERS_HPA,
                   height_layers=HEIGHT_LAYERS_KM,
                   match: bool = True) -> int:
    # MATCH: on, off, or the fields of the key -- pikobs.match decides.
    # Past this point match is True / False as before; the key travels
    # in match_spec.
    from pikobs.match import parse_match
    if match is True or match is False:
        match = 'on' if match else 'off'
    match_spec = parse_match(match)
    match = match_spec.enabled
    p = "[histogram]"
    regions = _split_tokens(regions)
    flags = _split_tokens(flags_criteria)
    functions = [f for f in (_split_tokens(functions) or ['omp'])
                 if f in FUNCTIONS] or ['omp']
    # omp_std and oma_std are omp and oma read in sigmas: extracted once,
    # as their base function
    extracted = sorted({f[:-4] if f.endswith('_std') else f
                        for f in functions})
    channels = _split_tokens(channel) or ['join']
    land_oceans = [lo for lo in (_split_tokens(land_ocean) or ['all'])
                   if lo in LAND_OCEAN_CHOICES] or ['all']
    stn_tokens = parse_station_tokens(id_stn)
    varnos = _split_tokens(varnos)
    matched = control is not None
    all_runs = ([control] if control else []) + list(runs)

    print(f"{p} runs: {', '.join(n for n, _ in all_runs)}", flush=True)
    if matched and match:
        print(f"{p} control: {control[0]}  |  matched observation by "
              f"observation with: {', '.join(n for n, _ in runs)}",
              flush=True)
    elif matched:
        print(f"{p} control: {control[0]}  |  compared, NOT matched, with: "
              f"{', '.join(n for n, _ in runs)}: each run with all its "
              f"observations and its own flags; Welch and F tests",
              flush=True)
    print(f"{p} regions: {regions}  |  flags: {flags}  |  fonction: "
          f"{functions}", flush=True)
    print(f"{p} id_stn tokens: {stn_tokens}  |  channel: {channels}",
          flush=True)
    print(f"{p} y axis: {'logarithmic' if log_scale else 'linear'}  |  "
          f"histograms with fewer than {min_obs} observations are skipped",
          flush=True)
    if qc_split:
        print(f"{p} QC split: " + (
            "each run on its own shows what quality control did; with a "
            "control the runs are matched and the split is left out"
            if matched else
            "the histogram is stacked by what quality control did "
            "(assimilated, background check, thinning, other QC, kept)"),
              flush=True)
    layers_by_family = {f: layers_for(f, pressure_layers, height_layers)
                        for f in families}
    for fam in families:
        _, vcoord, _, _, _, vcotyp = pikobs.family(fam)
        extra = ("  -- (O-P) / B_ref, with the GPS-RO quality gates"
                 if fam in RO_FAMILIES else "")
        print(f"{p} {fam}: vcoord = {vcoord.strip()}  ({vcotyp}){extra}",
              flush=True)
        if layers_by_family[fam] and any(c != 'join' for c in channels):
            print(f"{p} {fam}: one histogram per layer, not per level: "
                  + ", ".join(l[2].split(' | ')[1]
                              for l in layers_by_family[fam]), flush=True)

    if not check_input_files(all_runs, families, datestart, dateend,
                             'histogram'):
        return 1

    t_start = time.time()
    cycle_list = _cycles(datestart, dateend)
    n_input, input_bytes = input_size(all_runs, families, cycle_list)
    timing: Dict[str, Any] = {
        'datestart': datestart, 'dateend': dateend,
        'cycles': len(cycle_list), 'families': list(families),
        'runs': len(all_runs), 'regions': regions, 'flags': flags,
        'fonction': functions, 'id_stn': stn_tokens, 'channel': channels,
        'land_ocean': land_oceans, 'matched': matched, 'match': match,
        'min_obs': min_obs,
        'log_scale': log_scale, 'svg': svg, 'n_cpus': n_cpu,
        'input_files': n_input, 'input_bytes': input_bytes, 'seconds': {},
    }
    for family in families:
        pikobs.delete_create_folder(pathwork, family)

    comparisons = [
        {'label': f"{name} vs {control[0]}" if matched else name,
         'tag': f"{control[0]}_vs_{name}" if matched else name,
         'names': [control[0], name] if matched else [name], 'path': path}
        for name, path in runs]
    selectors = {f: _selections(stn_tokens, f) for f in families}
    modes = sorted({'join' if c == 'join' else 'all' for c in channels})

    client, dask_dir = None, None
    if n_cpu > 1:
        os.environ["DASK_LOGGING__DISTRIBUTED"] = "error"
        dask_dir = tempfile.mkdtemp(prefix="pikobs_histogram_dask_",
                                    dir=os.environ.get("TMPDIR") or None)
        os.environ["DASK_TEMPORARY_DIRECTORY"] = dask_dir
        os.environ["SQLITE_TMPDIR"] = dask_dir
        dask.config.set({"temporary-directory": dask_dir,
                         "logging.distributed": "error"})
        client = Client(processes=True, threads_per_worker=1, n_workers=n_cpu,
                        silence_logs=50, dashboard_address=None)
    plot_tasks: List[Dict[str, Any]] = []
    results: List[Any] = []
    try:
        # ---- scan: the sigma of every variable, from a few cycles of the
        # reference run, so the bins are the same for every run
        t0 = time.time()
        ref_path = control[1] if matched else runs[0][1]
        step = max(1, len(cycle_list) // SCAN_CYCLES)
        sample = cycle_list[::step][:SCAN_CYCLES]
        scan_tasks = [{'family': f, 'filein': cycle_path(ref_path, c, f),
                       'varnos': varnos, 'modes': modes,
                       'functions': extracted,
                       'qc_split': qc_split and not matched}
                      for f in families for c in sample]
        scans = [row for res in run_tasks(scan_sigma,
                                          [(t,) for t in scan_tasks], client,
                                          label='scan') if res
                 for row in res]
        specs, dead = bin_specs(scans, modes, layers_by_family)
        qc_by_family: Dict[str, List[tuple]] = {}
        if qc_split and not matched:
            for fam in families:
                counts: Dict[int, int] = {}
                for row in scans:
                    if row[0] == 'F' and row[1] == fam:
                        counts[row[2]] = counts.get(row[2], 0) + row[3]
                qc_by_family[fam] = qc_categories(counts)
                cats = qc_by_family[fam]
                shown = sum(c[2] for c in cats)
                print(f"{p} {fam}: flag combinations with O-P, one colour each "
                      f"({len(counts)} found, {len(cats)} drawn, "
                      f"{100 - shown:.1f} % pooled as '{QC_OTHER}'):",
                      flush=True)
                for _, label, share in cats:
                    print(f"{p}     {share:5.1f} %  {label}", flush=True)
                # what cannot be drawn: observations with no O-P at all
                no_omp: Dict[int, int] = {}
                for row in scans:
                    if row[0] == 'N' and row[1] == fam:
                        no_omp[row[2]] = no_omp.get(row[2], 0) + row[3]
                if no_omp:
                    total_n = sum(no_omp.values())
                    total_all = total_n + sum(counts.values())
                    print(f"{p} {fam}: {total_n} observation(s) "
                          f"({100.0 * total_n / total_all:.1f} %) have no O-P "
                          f"and cannot be drawn -- typically rejected before "
                          f"the departure is computed:", flush=True)
                    for sig, n in sorted(no_omp.items(), key=lambda kv: -kv[1])[:8]:
                        print(f"{p}     {100.0 * n / total_all:5.1f} %  "
                              f"{combo_label(sig)}", flush=True)
        timing['seconds']['scan'] = time.time() - t0
        print(f"{p} bins: {len(specs)} variable(s) and level(s), from "
              f"{len(sample)} cycle(s)", flush=True)
        for fam in families:
            fd = [d for d in dead if d[0] == fam]
            if fd:
                print(f"{p} {fam}: {len(fd)} level(s) left out, O-P "
                      f"identical for every observation (levels the system "
                      f"does not use): "
                      f"{', '.join(str(d[2]) for d in fd[:8])}"
                      f"{' ...' if len(fd) > 8 else ''}", flush=True)
        if not specs:
            print(f"{p} ERROR: nothing to bin, check FAMILY and VARNOS.",
                  file=sys.stderr, flush=True)
            return 1

        # with MATCH off every run -- the control included -- is read on
        # its own, all its observations with its own flags; the figures
        # then put two bases side by side
        independent = matched and not match
        extract_runs = ([{'tag': control[0], 'path': control[1]}]
                        + [{'tag': c['names'][1], 'path': c['path']}
                           for c in comparisons]) if independent else \
            comparisons
        tasks = []
        for comp in extract_runs:
            for cycle in cycle_list:
                for family in families:
                    for sel in selectors[family]:
                        t = {'family': family,
                             'db_new': db_path(pathwork, family,
                                               f"{comp['tag']}_{sel.tag}",
                                               datestart, dateend),
                             'regions': regions, 'flags': flags,
                             'channels': channels,
                             'land_oceans': land_oceans,
                             'functions': extracted,
                             'id_stn_sql': sel.sql(),
                             'stn_label': sel.label,
                             'special_on': special_on, 'varnos': varnos,
                             'pathwork': pathwork,
                             'qc_split': qc_split and not matched,
                             'qc_categories': qc_by_family.get(family, []),
                             'layers': layers_by_family[family]}
                        if matched and not independent:
                            t['ctl_file'] = cycle_path(control[1], cycle,
                                                       family)
                            t['exp_file'] = cycle_path(comp['path'], cycle,
                                                       family)
                            t['match_fields'] = match_spec.fields
                            t['names'] = (control[0], 'experience')
                        else:
                            t['filein'] = cycle_path(comp['path'], cycle,
                                                     family)
                        tasks.append(t)
        t0 = time.time()
        print(f"{p} extraction: {len(tasks)} tasks, {n_cpu} worker(s)",
              flush=True)
        res = run_tasks(_extract_task, [(t, specs, dead) for t in tasks],
                        client, label='extraction')
        # one line per family when the pairing key was not unique
        from pikobs.match import add_counts, repeat_warning
        repeats = {}
        for t, r in zip(tasks, res):
            if isinstance(r, dict):
                add_counts(repeats.setdefault(t['family'], {}),
                           r.get('repeats'))
        for fam in sorted(repeats):
            msg = repeat_warning('histogram', fam, match_spec, repeats[fam])
            if msg:
                print(msg, file=sys.stderr, flush=True)
        timing['seconds']['extraction'] = time.time() - t0
        print(f"{p} extraction time: {timing['seconds']['extraction']:.1f}s "
              f"({sum(r is not None for r in res)}/{len(tasks)} files)",
              flush=True)
        dbs = sorted({t['db_new'] for t in tasks})
        run_tasks(_finish_db, [(d, specs) for d in dbs], client,
                  label='indexing')

        for comp in comparisons:
            for family in families:
                word = "type" if _is_composite(family) else "station"
                for sel in selectors[family]:
                    sql = ("SELECT DISTINCT region, flag, land_ocean, id_stn, "
                           "special, varno, lkey, fonction FROM moments;")
                    if independent:
                        db_ctl = db_path(pathwork, family,
                                         f"{control[0]}_{sel.tag}",
                                         datestart, dateend)
                        path = db_path(pathwork, family,
                                       f"{comp['names'][1]}_{sel.tag}",
                                       datestart, dateend)
                        # every selection either run has: a station only
                        # the experience brought still gets its figure
                        rows_sel = sorted(set(_distinct(db_ctl, 'moments',
                                                        sql))
                                          | set(_distinct(path, 'moments',
                                                          sql)),
                                          key=lambda r: tuple(map(str, r)))
                    else:
                        db_ctl = None
                        path = db_path(pathwork, family,
                                       f"{comp['tag']}_{sel.tag}", datestart,
                                       dateend)
                        rows_sel = _distinct(path, 'moments', sql)
                    for row in rows_sel:
                        region, flag, lo, idst, sp, varno, lkey, fn = row
                        plot_tasks.append({
                            'pathwork': pathwork, 'db_file': path,
                            'family': family, 'region': region, 'flag': flag,
                            'land_ocean': lo, 'id_stn': idst,
                            'stn_tag': _safe(idst), 'special': sp,
                            'special_label': _special_label(family, sp),
                            'member_word': word, 'varno': varno,
                            'lkey': lkey, 'function': fn,
                            'datestart': datestart, 'dateend': dateend,
                            'names': comp['names'], 'matched': matched,
                            'experience': comp['label'], 'svg': svg,
                            'min_obs': min_obs, 'log_scale': log_scale,
                            'gpsro': family in RO_FAMILIES,
                            'qc_split': qc_split and not matched,
                            'qc_order': [c[1] for c in
                                         qc_by_family.get(family, [])]
                            + [QC_OTHER],
                            'db_ctl': db_ctl,
                            'db_exp': path if independent else None})
        # a _std figure is its base function read in sigmas: the same rows
        std_tasks = [dict(t, function=f"{t['function']}_std",
                          source_function=t['function'])
                     for t in plot_tasks if f"{t['function']}_std" in functions]
        plot_tasks = [t for t in plot_tasks if t['function'] in functions] \
            + std_tasks
        if not plot_tasks:
            print(f"{p} WARNING: nothing to plot, check the selectors.",
                  file=sys.stderr, flush=True)
            return 1
        t0 = time.time()
        print(f"{p} plots: {len(plot_tasks)} tasks", flush=True)
        results = run_tasks(histogram_plot_task, [(t,) for t in plot_tasks],
                            client, label='plots')
        timing['seconds']['plots'] = time.time() - t0
        print(f"{p} plot time: {timing['seconds']['plots']:.1f}s "
              f"({sum(r is not None for r in results)}/{len(plot_tasks)})",
              flush=True)
    finally:
        if client is not None:
            try:
                client.close(timeout=30)
            except Exception:
                pass
            try:
                client.shutdown()
            except Exception:
                pass
        if dask_dir:
            shutil.rmtree(dask_dir, ignore_errors=True)

    items = [{'experience': t['experience'], 'family': t['family'],
              'fonction': t['function'], 'region': t['region'],
              'flag_criteria': t['flag'], 'id_stn': t['id_stn'],
              'special': t['special_label'], 'channel': str(t['lkey']),
              'land_ocean': t['land_ocean'], 'varno': str(t['varno']),
              'filename': os.path.basename(r)}
             for t, r in zip(plot_tasks, results) if r]
    if not items:
        print(f"{p} ERROR: no figure was produced.", file=sys.stderr,
              flush=True)
        return 1
    keys = ["experience", "family", "fonction", "region", "flag_criteria",
            "id_stn", "special", "channel", "land_ocean", "varno"]
    from pikobs.configobs.special_family import special_key_label
    generate_web(
        items, keys, os.path.join(pathwork, "pikobs_histogram_viewer.html"),
        title="Pikobs Histogram Viewer",
        subtitle=(
            "The distribution of the departures, as a density, with the "
            "Gaussian of the same mean and sigma for reference. " +
            ("<b>Red is the experience, blue the control</b>, matched "
             "observation by observation, so both distributions are built "
             "on the same observations."
             if matched else "One run, in red.") + _GLOSSARY) + runs_block(all_runs, control, (datestart, dateend)),
        image_subdir_key="family",
        # join said in words, as in the figures
        value_labels={'channel': {'join': (
            'all channels' if all(str(pikobs.family(f)[5]).upper() == 'CANAL'
                                  for f in families)
            else 'whole column' if not any(
                str(pikobs.family(f)[5]).upper() == 'CANAL' for f in families)
            else 'whole column / all channels')}},
        key_labels={'channel': level_selector_label(families),
                    'land_ocean': 'Surface',
                    'special': special_key_label(families)},
        issues_url="https://gitlab.science.gc.ca/dlo001/Pikobs")

    timing['seconds']['total'] = time.time() - t_start
    _report_timing(timing, pathwork)
    print(f"{p} done -- output in: {pathwork}", flush=True)
    return 0


def arg_call() -> None:
    import argparse

    ap = argparse.ArgumentParser(
        prog="pikobs-histogram",
        description="Distribution of the departures, one run or a control "
                    "against experiences.")
    ap.add_argument('--path_control_files', default=None)
    ap.add_argument('--control_name', default=None)
    ap.add_argument('--path_experience_files', nargs='+', default=[])
    ap.add_argument('--experience_name', nargs='+', default=[])
    ap.add_argument('--pathwork', default=None)
    ap.add_argument('--datestart', default=None)
    ap.add_argument('--dateend', default=None)
    ap.add_argument('--region', nargs='+', default=['Monde'])
    ap.add_argument('--family', nargs='+', default=[])
    ap.add_argument('--flags_criteria', nargs='+', default=['all'])
    ap.add_argument('--fonction', nargs='+', default=['omp'],
                    choices=list(FUNCTIONS))
    ap.add_argument('--varnos', nargs='*', default=[])
    ap.add_argument('--id_stn', nargs='+', default=['join'])
    ap.add_argument('--channel', '--vcoord', dest='channel', nargs='+',
                    default=['join'],
                    help="join (all levels together), all (one histogram "
                         "per channel or level), or explicit levels.")
    ap.add_argument('--land_ocean', nargs='+', default=['all'],
                    choices=list(LAND_OCEAN_CHOICES))
    ap.add_argument('--special_column', default='off', choices=['on', 'off'])
    ap.add_argument('--min_obs', default=MIN_OBS_PER_HISTOGRAM, type=int)
    ap.add_argument('--y_scale', default='log', choices=['log', 'linear'])
    ap.add_argument('--pressure_layers', nargs='+', type=float,
                    default=list(PRESSURE_LAYERS_HPA),
                    help="Layer edges in hPa for families on pressure, with "
                         "CHANNEL all: one histogram per layer.")
    ap.add_argument('--height_layers', nargs='+', type=float,
                    default=list(HEIGHT_LAYERS_KM),
                    help="Layer edges in km for families on height.")
    ap.add_argument('--match', nargs='+', default=['on'],
                    help="on: with a control, the same observations in both "
                         "runs, paired tests. off: each run with all its "
                         "observations and its own flags, Welch and F tests.")
    ap.add_argument('--qc_split', default='off', choices=['on', 'off'],
                    help="on: stack each histogram by what quality control "
                         "did with the observations; meant for "
                         "FLAGS_CRITERIA=all, one run at a time.")
    ap.add_argument('--svg', default='off', choices=['on', 'off'])
    ap.add_argument('--n_cpus', '--n_cpu', default=1, type=int,
                    dest='n_cpus')
    ap.add_argument('--no_submit', action='store_true')
    # options of the old module, accepted so its wrappers keep working
    for old in ('--boxsizex', '--boxsizey', '--projection', '--mode',
                '--Points', '--layer'):
        ap.add_argument(old, nargs='*', default=None, help=argparse.SUPPRESS)

    args = ap.parse_args()
    for arg in vars(args):
        print(f'--{arg} {getattr(args, arg)}', flush=True)
    for attr in ('path_control_files', 'control_name'):
        val = getattr(args, attr)
        if isinstance(val, str) and (not val.strip() or val == 'undefined'):
            setattr(args, attr, None)

    paths = _split_tokens(args.path_experience_files)
    names = _split_tokens(args.experience_name)
    if not paths or not names or len(paths) != len(names):
        raise ValueError("--path_experience_files and --experience_name must "
                         "have the same number of entries")
    for attr, flag in [('pathwork', '--pathwork'),
                       ('datestart', '--datestart'),
                       ('dateend', '--dateend'), ('family', '--family')]:
        if getattr(args, attr) in (None, [], 'undefined', ''):
            raise ValueError(f"{flag} is required")
    runs = [(n, p_.rstrip('/') or '/') for n, p_ in zip(names, paths)]
    control = None
    if args.path_control_files:
        ctl_name = (args.control_name or 'control').strip() or 'control'
        control = (ctl_name, args.path_control_files.strip().rstrip('/')
                   or '/')

    maybe_submit_to_pbs(args)
    sys.exit(make_histogram(
        runs, args.pathwork, args.datestart, args.dateend, args.region,
        _split_tokens(args.family), args.flags_criteria, args.fonction,
        _split_tokens(args.varnos), args.id_stn, args.channel,
        args.land_ocean, args.n_cpus, control, svg_enabled(args.svg),
        args.min_obs, args.special_column == 'on', args.y_scale == 'log',
        args.qc_split == 'on', args.pressure_layers, args.height_layers,
        args.match))


if __name__ == '__main__':
    arg_call()
