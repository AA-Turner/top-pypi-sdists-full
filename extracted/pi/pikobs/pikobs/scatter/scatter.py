# GENERATED -- this docstring is written by pikobs/build_doc/build_scatter.py.
# Edit that file and run ./pikobs_doc.sh; a change made here is lost.
r"""================================================================
pikobs.scatter -- Geographic Tiled Observation Statistics
================================================================

``scatter`` answers a question that global scores hide: *where* do the
observations behave differently? It cuts the globe into longitude /
latitude boxes, gathers every observation that falls in a box over the
period, and paints the box with the statistic you ask for: O-B, O-A,
their sigma, the observed value, the bias correction, or simply how many
observations arrived.

Quick start
===========

Download the wrapper you need. Take it from GitLab every time you start a
new study: the copy there follows the options of the installed module.

.. code-block:: bash

   # one or several experiences, single-run maps
   wget https://gitlab.science.gc.ca/dlo001/Pikobs/-/raw/master/pikobs/script/run_scatter_exp.sh
   chmod +x run_scatter_exp.sh

   # control against one or several experiences
   wget https://gitlab.science.gc.ca/dlo001/Pikobs/-/raw/master/pikobs/script/run_scatter_cont_exp.sh
   chmod +x run_scatter_cont_exp.sh

The wrappers run on the node you are on and never submit to PBS, so open a
compute node first, edit the ``USER SETTINGS`` block and launch:

.. code-block:: bash

   qsub -I -lselect=1:ncpus=80:mem=185gb -lwalltime=2:0:0
   nano run_scatter_cont_exp.sh
   ./run_scatter_cont_exp.sh

.. warning::

   Do not run the wrappers on a login node. The aggregation opens every
   6-h file of the period in parallel.

.. important::

   Lists are **bash arrays**: ``FAMILY=(sw ai)`` and not
   ``FAMILY="sw ai"``. The wrappers pass them as ``"${FAMILY[@]}"``; a
   plain string arrives glued and ends in "missing file" errors.
   Quote any token with a ``*`` or a space, otherwise bash expands or
   splits it: ``ID_STN=(join "CAS*" "AMDAR (42)")``.

A comparison run prints something like this:

.. code-block:: text

   [scatter] runs: control, experience
   [scatter] comparisons: control vs experience
   [scatter] id_stn tokens: ['all']
   [scatter] channel tokens: ['32']
   [scatter] input check OK: 21 cycles x 2 run(s) x 1 family(ies), 42 files, 61.3 GB
   [scatter] aggregation: 84 tasks, 80 worker(s)
   [scatter] aggregation time: 190.2s (84/84 files aggregated)
   [scatter] matching control and experience: 42 tasks
   [scatter] matching time: 214.7s (42/42 tasks)
   [scatter]   iasi experience: 18204417 common obs (96.2% of control, 95.8% of experience)
   [scatter] compaction time: 38.1s (6/6 databases)
   [scatter] plots: 36 tasks, 80 worker(s)
   [scatter] plot time: 58.4s (36/36 maps written)
   [scatter]   difference       maps: 16/16
   [scatter]   significance     maps: 10/10
   [scatter]   significant only maps: 10/10
   [scatter] viewer selectors: ['experience', 'family', 'region', 'flag', 'function', 'panel', ...]
   [viewer] wrote /home/dlo001/sites8/pikobs_scatter_cont_exp/pikobs_scatter_viewer.html  (36 items, 11 keys)
   Viewer: /home/dlo001/sites8/pikobs_scatter_cont_exp/pikobs_scatter_viewer.html
   Web:    https://goc-dx-u3.science.gc.ca/~dlo001/sites8/pikobs_scatter_cont_exp/pikobs_scatter_viewer.html
   [scatter] ------------------- run time -------------------
   [scatter] input           61.3 GB   42 files, 21 cycles, 2 run(s)
   [scatter] aggregation    190.2 s
   [scatter] matching       214.7 s
   [scatter] compaction      38.1 s
   [scatter] plots           58.4 s   36 maps
   [scatter] total          503.9 s   (8.4 min, 80 workers)
   [scatter] done -- output in: /home/dlo001/sites8/pikobs_scatter_cont_exp

The ``Viewer`` and ``Web`` lines come from the module, whichever way it
was launched. If a link in ``~/public_html`` already shows the folder --
one ``sites8 -> ~/sites8`` covers every run under it -- the address goes
through that link; otherwise the run prints the one ``ln -s`` that would
make the page reachable.

How long a run takes, and how big a node to ask for: :doc:`runtime`.

----

When to use which wrapper
=========================

I reach for it in two situations. The first is a look at one run. A new
channel selection goes in, a blacklist changes, a satellite comes back, and
before trusting any global number I want to see the O-B pattern on a map.
The second is a comparison. A parallel suite against the operational one,
box by box, with a statistical test behind every coloured box, because a
2° box over the Southern Ocean that received a dozen observations can turn
red for no reason at all.

Each situation has its own wrapper:

* ``run_scatter_exp.sh`` draws one or several experiences, each on its own
  maps;
* ``run_scatter_cont_exp.sh`` compares one control with one or several
  experiences and draws, for every comparison, a difference map plus two
  significance maps.

Both end in the same HTML viewer, so hundreds of maps can be flipped through
from dropdowns instead of opening PNG files one by one.

.. image:: _static/scatter_exp_omp.png
   :alt: Single-run OMP map
   :align: center
   :width: 100%

Live examples, made with the two wrappers:

* `single run <https://goc-dx-u3.science.gc.ca/~dlo001/sites8/pikobs_doc_scatter_exp/pikobs_scatter_viewer.html>`__
* `control vs experience <https://goc-dx-u3.science.gc.ca/~dlo001/sites8/pikobs_doc_scatter/pikobs_scatter_viewer.html>`__

----

1. How it works
===============

The run goes through six steps.

**Input check.** Before anything else, every 6-h file
``<path>/YYYYMMDDHH_<family>`` of the period is looked up, for the control
and for every experience. If a single one is missing the run stops, says
which cycles are missing (grouped in ranges) and which dates the directory
does contain. ``PATHWORK`` is not touched in that case, so a typo in the
dates does not erase the maps of the previous run.

**Aggregation.** Each 6-h file is read in parallel and reduced to sums per
box: :math:`\sum x`, :math:`\sum x^2` and :math:`N` for O-B, O-A, the
observed value and the bias correction. A box is identified by

.. math::

   b = \left\lfloor \frac{360}{\Delta x} \right\rfloor
       \left\lfloor \frac{\varphi}{\Delta y} \right\rfloor
     + \left\lfloor \frac{\min(179.99,\ \lambda)}{\Delta x} \right\rfloor

with :math:`\Delta x, \Delta y` the box size, :math:`\varphi` the latitude
and :math:`\lambda` the longitude. The sums are kept per station, per
channel and per special value only when the ``ID_STN`` / ``CHANNEL``
tokens need it, and the list of stations that contributed is saved
separately so the titles can name them.

**Matching** (comparison runs only). For ``omp``, ``oma``, ``stdomp``,
and ``stdoma`` the two runs are compared on the *same*
observations. Each 6-h file of the control is joined with the same file of
the experience on

.. code-block:: text

   ID_STN + DATE + TIME + ROUND(LAT, 4) + ROUND(LON, 4) + VCOORD + VARNO

Both runs go through the same filters, and each run's flags are checked on
its own data, so a pair exists only when the observation passes the flag
criterion in both. A key that appears more than once in a file is not
dropped: its observations are paired one to one, in order. ``MATCH``
decides all this -- ``on`` for this key, a list of fields for another,
``off`` to compare every observation of each run, with Welch and F
tests -- see :doc:`match`. The
pair database keeps, per box, the number of pairs and
:math:`\sum x`, :math:`\sum y`, :math:`\sum x^2`, :math:`\sum y^2`,
:math:`\sum xy` (:math:`x` control, :math:`y` experience). The log says how
much was matched:

.. code-block:: text

   [scatter]   iasi experience: 18204417 common obs (96.2% of control, 95.8% of experience)

Two suites fed with the same observations should be close to 100 %. A low
figure means the runs do not hold the same observations (other channels,
other platforms, other thinning); the comparison is then limited to what
they share, while ``nobs`` and ``dens`` still use everything.

**Compaction.** The maps never need the cycle, so every database is summed
over the period and indexed before plotting. This keeps the plotting
queries small even with 120 cycles of a hyperspectral instrument.

**Maps.** Every statistic is derived from those sums, so one aggregation
feeds every function, projection and grouping. For a box with :math:`N`
observations :math:`x_i`:

.. math::

   \bar{x} = \frac{1}{N}\sum_{i=1}^{N} x_i ,
   \qquad
   \sigma = \sqrt{\max\left(0,\ \frac{1}{N}\sum_{i=1}^{N} x_i^2 - \bar{x}^2\right)}

``dens`` divides the daily count by the box area on the sphere,

.. math::

   A = R^2 \,\left|\sin\varphi_2 - \sin\varphi_1\right|\, |\lambda_2 - \lambda_1|,
   \qquad R = 6371\ \mathrm{km}

and the number of days counts every cycle as 6 h, so ``2026091000`` to
``2026091500`` is 5.25 days.

**Viewer.** All maps are indexed in ``pikobs_scatter_viewer.html``
(section 6).

The module is two files. ``scatter.py`` reads the observations -- the
input check, the aggregation, the matching, the compaction -- and
``scatter_plot.py`` draws. That is what lets a colour, a title or a
colour bar be changed without reading a single database again.

----

2. Configuration
================

Everything is set in the ``USER SETTINGS`` block at the top of the wrapper
you downloaded: ``run_scatter_exp.sh`` maps one or more runs on their own,
``run_scatter_cont_exp.sh`` compares one or more experiences with a
control. The two share every setting except the control. Lists are bash
arrays: ``FAMILY=(iasi cris)``, not ``FAMILY="iasi cris"``.

.. wrapper-settings:: run_scatter_exp.sh run_scatter_cont_exp.sh

With several experiences, ``PATH_EXPERIENCE_FILES`` and
``EXPERIENCE_NAME`` are arrays of the same length:

.. code-block:: bash

   PATH_EXPERIENCE_FILES=(/path/to/E22 /path/to/E23)
   EXPERIENCE_NAME=(E22 E23)

``run_scatter_exp.sh`` then draws E22 and E23 separately;
``run_scatter_cont_exp.sh`` draws *control vs E22* and *control vs E23*.

----

3. Choosing stations and channels
=================================

``ID_STN`` and ``CHANNEL`` decide how many maps come out. Each token is a
separate series of maps, and both combine: ``ID_STN=(all)`` with
``CHANNEL=(all)`` gives one map per station and per channel.

Stations
--------

+-----------------------+-------------------------------------------------------+
| Token                 | Maps produced                                         |
+=======================+=======================================================+
| ``join``              | one map, every station merged                         |
+-----------------------+-------------------------------------------------------+
| ``all``               | one map per station                                   |
+-----------------------+-------------------------------------------------------+
| ``CAS`` or ``"CAS*"`` | one map with every station whose id starts with CAS   |
+-----------------------+-------------------------------------------------------+
| ``C%``                | SQL ``LIKE`` pattern on the station id, used as given |
+-----------------------+-------------------------------------------------------+
| ``=NENE``             | station NENE only                                     |
+-----------------------+-------------------------------------------------------+
| ``"AMDAR (42)"``      | every station of codtyp 42                            |
+-----------------------+-------------------------------------------------------+

Tokens mix freely. ``ID_STN=(join all CAS SER)`` gives one merged map, one
map per station, one for the CAS stations and one for the SER stations.

When a map covers a group (``join``, a prefix, a pattern or a codtyp), the
title says how many stations went into it and lists them, cut after 15
names. Filenames tag the groups so that they never collide with a station
of the same name: ``CAS_grp`` for a prefix, ``NENE_eq`` for an exact id,
``Cpct`` for ``C%``, ``codtyp_32-33`` for a codtyp group.

For ai, sf, ua, gp and csr the tokens name instrument types rather than
stations -- ``pilot``, ``=TEMP``, ``35`` -- the same way in every module;
see :doc:`families`.

Channels and vertical coordinates
---------------------------------

``CHANNEL`` (``--vcoord`` is an alias on the command line):

+-----------+---------------------------------------+
| Token     | Maps produced                         |
+===========+=======================================+
| ``join``  | all channels / levels merged          |
+-----------+---------------------------------------+
| ``all``   | one map per channel / level           |
+-----------+---------------------------------------+
| ``32 40`` | channels 32 and 40 only, one map each |
+-----------+---------------------------------------+

``CHANNEL=(join 32)`` gives the merged map and the channel 32 map.

Layers
------

A family whose vertical coordinate is a pressure or a height gets one
series of maps per layer, on top of the series with the whole column.
The edges are read in the unit of that coordinate:

.. code-block:: bash

   PRESSURE_LAYERS=(1100 850 500 250 100 10 1 0)   # hPa: ua ai sw ch
   HEIGHT_LAYERS=(0 5 10 20 30 40 60 100)          # km:  ro radar

Each family reads the list of its own coordinate, so ``FAMILY=(sw ro)``
in one run gives sw in hPa layers and ro in km layers, each labelled in
its own unit. A radiance takes neither: a channel is a named thing and
is chosen with ``CHANNEL``. An empty list means the whole column, in one
series.

A layer holds its top edge, so 500 hPa falls in ``500-250 hPa`` and
never in two layers at once, and the label carries its rank from the
ground -- ``2 | 850-500 hPa`` -- so the viewer lists them by height and
not alphabetically, where 1000 would come before 500.

The run prints what each family will do before it starts:

.. code-block:: text

   [scatter] sw: 1 | 1100-850 hPa, 2 | 850-500 hPa, 3 | 500-250 hPa, ...
   [scatter] ro: 1 | 0-5 km, 2 | 5-10 km, 3 | 10-20 km, ...
   [scatter] cris: the whole column in one series

A layer with no observation in it simply has no map, and the log says
which one: the AMVs of ``sw`` stop below 100 hPa, and GPS-RO above
40 km, so the top layers of each are empty and that is the right
answer.

Surface and special column
--------------------------

Two more settings split the maps. Both are off by default, as in every
module.

``LAND_OCEAN=(all land ocean)`` draws each map three times: everything,
land only, sea only. The mask is the one every module uses
(``global_land_mask``, nearest cell) and it is applied to each
observation before it is summed, so a coastal box can show up on both
maps, each time with its own observations. The name carries ``_land``
or ``_ocean`` right after the region, and the viewer gets a *Surface*
selector.

``SPECIAL_COLUMN="on"`` splits a family by its special column: the wind
method for ``sw`` (IR channel, water vapour channel...), the antenna
elevation for radar. Two populations with different errors then stop
averaging each other out. The label follows the surface in the name --
``..._Monde_land_IR_channel_...`` -- and the viewer gets its selector
(*Method* for ``sw``). A family without a special column is drawn as
usual.

----

4. Single-run maps
==================

``run_scatter_exp.sh`` draws every experience on its own. The colour scale
of each map is set from its own values.

+------------+---------------------------------------+------------------------------+
| Function   | Box value                             | Colours                      |
+============+=======================================+==============================+
| ``omp``    | mean O-B                              | blue < 0 < red, white near 0 |
+------------+---------------------------------------+------------------------------+
| ``oma``    | mean O-A                              | blue < 0 < red, white near 0 |
+------------+---------------------------------------+------------------------------+
| ``stdomp`` | standard deviation of O-B             | light to dark                |
+------------+---------------------------------------+------------------------------+
| ``stdoma`` | standard deviation of O-A             | light to dark                |
+------------+---------------------------------------+------------------------------+
| ``obs``    | mean observed value                   | blue to red                  |
+------------+---------------------------------------+------------------------------+
| ``bcorr``  | mean bias correction (radiances only) | blue to red                  |
+------------+---------------------------------------+------------------------------+
| ``nobs``   | observations per day                  | viridis                      |
+------------+---------------------------------------+------------------------------+
| ``dens``   | observations per km² per day          | viridis                      |
+------------+---------------------------------------+------------------------------+

For ``omp`` and ``oma`` the scale is symmetric, built from steps like
0.05, 0.1, 0.2, 0.3, 0.5, 1 chosen so that the last one covers 95 % of the
boxes; the white band around zero is the first step. The box at the top
right gives the mean over the boxes (:math:`\bar{\mu}`,
:math:`\bar{\sigma}`) and the number of observations drawn, and the title
gives the variable, the station group, the channel and the layer. The
``omp`` map is the one at the top of this page; the others look like this:

.. image:: _static/scatter_exp_oma.png
   :alt: Single-run OMA map
   :align: center
   :width: 100%

.. image:: _static/scatter_exp_stdomp.png
   :alt: Single-run STD(OMP) map
   :align: center
   :width: 100%

.. image:: _static/scatter_exp_obs.png
   :alt: Single-run observed value map
   :align: center
   :width: 100%

.. image:: _static/scatter_exp_nobs.png
   :alt: Single-run observation count map
   :align: center
   :width: 100%

.. image:: _static/scatter_exp_dens.png
   :alt: Single-run density map
   :align: center
   :width: 100%

.. image:: _static/scatter_exp_bcorr.png
   :alt: Single-run bias correction map
   :align: center
   :width: 100%

``bcorr`` exists only for radiance families. When the files have no
``BIAS_CORR`` column the maps are skipped and the log says it once.

----

5. Control vs experience maps
=============================

``run_scatter_cont_exp.sh`` does not show two sets of absolute values. It
shows, box by box, **experience minus control**. The direction and the
tests are the ones of ``pikobs.stats``, shared with the other comparison
modules, so a map and a channel plot of the same experiment tell the same
story.

+------------------------+------------------------------------------+----------------------+--------------+----------------------------+
| Function               | Box value (experience - control)         | Red means            | Observations | Test                       |
+========================+==========================================+======================+==============+============================+
| ``omp``, ``oma``       | ``|bias_exp| - |bias_ctl|``, units       | negative: exp better | common       | paired t and Pitman-Morgan |
+------------------------+------------------------------------------+----------------------+--------------+----------------------------+
| ``stdomp``, ``stdoma`` | ``100 (σ_exp - σ_ctl) / σ_ctl``          | negative: exp better | common       | Pitman-Morgan              |
+------------------------+------------------------------------------+----------------------+--------------+----------------------------+
| ``bcorr``              | ``100 (|bc_exp| - |bc_ctl|) / |bc_ctl|`` | positive: larger     | all          | none                       |
+------------------------+------------------------------------------+----------------------+--------------+----------------------------+
| ``obs``                | ``obs_exp - obs_ctl``, units             | positive: higher     | all          | none                       |
+------------------------+------------------------------------------+----------------------+--------------+----------------------------+
| ``nobs``, ``dens``     | ``100 (N_exp - N_ctl) / N_ctl``          | positive: more obs   | all          | none                       |
+------------------------+------------------------------------------+----------------------+--------------+----------------------------+

For the departures the question is whether the experience gets closer to
zero, so the bias is compared in absolute value:

.. math::

   \Delta_{\mathrm{bias}} = \left|\bar{d}_{\mathrm{exp}}\right|
                          - \left|\bar{d}_{\mathrm{ctl}}\right|
   \qquad
   \Delta_{\sigma} = 100\,\frac{\sigma_{\mathrm{exp}} - \sigma_{\mathrm{ctl}}}
                               {\sigma_{\mathrm{ctl}}}

For these two a **negative value is an improvement, and it is drawn in
red**. A box at -12 on a ``stdomp`` map means the experience has a 12 %
smaller O-B sigma there. Positive values, the experience doing worse, are
blue. The colour bar says it too, formula included: for the bias,
*negative / red = Exp bias closer to zero*; for sigma,
*negative / red = Exp better*.

For the other functions the sign simply follows the change: more
observations, a higher observed value or a larger correction are red.

.. math::

   \Delta_{N} = 100\,\frac{N_{\mathrm{exp}} - N_{\mathrm{ctl}}}{N_{\mathrm{ctl}}}
   \qquad
   \Delta_{\mathrm{bcorr}} = 100\,\frac{\left|b_{\mathrm{exp}}\right|
                                    - \left|b_{\mathrm{ctl}}\right|}
                                   {\left|b_{\mathrm{ctl}}\right|}

The bias correction :math:`b` can be negative, so its size is compared. In
regions where the control barely corrects anything the percentage gets
large and saturates at ±100 %; read those boxes with the single-run
``bcorr`` map at hand.

Why not a percentage for the bias? It would divide by a control bias that
is often close to zero: a box going from 0.01 K to 0.03 K is +200 % and
means nothing.

The colour scale is symmetric, uses steps such as 0.05, 0.1, 0.2, 0.3, 0.5,
1, and is set on the significant boxes, so a few boxes with a handful of
observations do not stretch it. Percentages are capped at ±100 %; beyond
the last step a box takes the darkest colour.

Three maps per comparison
-------------------------

For ``omp``, ``oma``, ``stdomp`` and ``stdoma`` every comparison
produces three maps, switched with the *Difference / Significance*
selector of the viewer:

+----------------------+-------------------------+---------------------------------------+
| Map                  | File suffix             | Content                               |
+======================+=========================+=======================================+
| ``difference``       | ``_<ctl>_vs_<exp>.png`` | every box, blue / white / red         |
+----------------------+-------------------------+---------------------------------------+
| ``significance``     | ``..._signif.png``      | test confidence, 0 to 100 %           |
+----------------------+-------------------------+---------------------------------------+
| ``significant only`` | ``..._sigonly.png``     | difference map, boxes above 95 % only |
+----------------------+-------------------------+---------------------------------------+

``obs``, ``bcorr``, ``nobs`` and ``dens`` only have the difference map,
computed on all the observations of each run.

The examples are O-A (``oma``); the section *Two passes of the same
cycle* below says why.

**difference** shows every box:

.. image:: _static/scatter_cmp_oma_difference.png
   :alt: O-A difference map
   :align: center
   :width: 100%

**significance** shows how sure the test is, from 0 to 100 %. Grey boxes
stay at or below 95 % (darker when closer), orange ones are above 95 % and
red ones above 99 %; the thick line on the colour bar marks 95 %. For
``omp`` and ``oma``, a crossed box (``xxx``) passed both tests but its bias
and sigma moved in opposite directions, so it is not counted. The box at
the top right recalls which test was run and counts the significant boxes:

.. image:: _static/scatter_cmp_oma_significance.png
   :alt: O-A significance map
   :align: center
   :width: 100%

**significant only** is the difference map with the same colours and the
same scale, where only the boxes that pass are drawn (for ``omp`` / ``oma``:
both tests, same direction). It is usually the
one to show in a meeting:

.. image:: _static/scatter_cmp_oma_sigonly.png
   :alt: O-A significant-only map
   :align: center
   :width: 100%

The same for sigma:

.. image:: _static/scatter_cmp_stdoma_difference.png
   :alt: Sigma of O-A difference map
   :align: center
   :width: 100%

.. image:: _static/scatter_cmp_stdoma_sigonly.png
   :alt: Sigma of O-A significant-only map
   :align: center
   :width: 100%

and the change in the number of observations, which has no test:

.. image:: _static/scatter_cmp_nobs_difference.png
   :alt: Observation count difference map
   :align: center
   :width: 100%

What decides a box
------------------

The tests, their formulas, the worked example and the reason a paired
test sees changes an independent one misses are in :mod:`pikobs.stats`,
which every comparison module shares. On a map:

* ``stdomp`` and ``stdoma`` are decided by the **Pitman-Morgan test** on sigma alone.
* ``omp`` and ``oma`` need the **paired t-test** on the bias *and* the
  Pitman-Morgan test on sigma, both above 95 %, and both changes pointing the same
  way: bias and sigma better gives a red box, both worse a blue one.
  When they disagree the box is crossed on the significance map and left
  out of the significant-only one -- a background that aims better but
  shakes more has not improved.
* ``obs``, ``bcorr``, ``nobs`` and ``dens`` have no test: they are
  differences, not verdicts.

Two things to keep in mind while reading a map, both of which pull in
opposite directions. Observations inside a box are not independent -- one
satellite pass, one cycle -- which makes both tests look more certain
than they are. And a map has thousands of boxes, so at 95 % about one in
twenty passes by chance: on 14 000 boxes that is 700. An isolated
significant box proves nothing; a region of them, all the same colour,
does.

Black boxes
-----------

A black box cannot be compared: it has observations in the control or in
the experience, but none in common (for ``obs``, ``nobs`` and ``dens``:
data in only one of the two runs). Black boxes point to a coverage change,
a channel switched off, a new platform, a different blacklist, not to a
score. The box at the top right counts them.

The same box gives the number of observations of each run on the map, all
of them, and how many were compared, for example
``common obs compared: 18204417 (96% of ctl)``.

Two passes of the same cycle
----------------------------

The first time I compared G0 and G2 the ``omp`` map came out white, every
box of it, and the colour bar stopped at 0.00002 K. Nothing was broken.
G0, G1 and G2 are passes of the same operational cycle: G0 goes first with
a short cut-off, G1 (00 and 12 UTC only) and G2 later, with more
observations -- half as many IASI radiances again in G2. They start from
the same background, so an observation that two passes both have gets the
same O-B in each, to the last bit. On six days of assimilated IASI the
sums of the pair database were identical to the last digit, over 13
million pairs. There is nothing to compare.

The analysis is where they part. With more observations G2 lands
somewhere else, and O-A shows it:

+-------+-----------+-----------+-------------------------+
| O-A   | G0 (Ctl)  | G2 (Exp)  | change                  |
+=======+===========+===========+=========================+
| bias  | -0.0129 K | -0.0112 K | 0.0017 K closer to zero |
+-------+-----------+-----------+-------------------------+
| sigma | 0.4017 K  | 0.4002 K  | -0.38 %                 |
+-------+-----------+-----------+-------------------------+

Small, and 13 million pairs are enough for the tests to see it. That is
why the comparison maps on this page are O-A. To look at O-B, compare two
runs with backgrounds of their own -- an experiment against the operational
suite -- never two passes of one cycle.

When few observations are compared
----------------------------------

The ``common obs compared`` line is worth a look before any colour. Two
suites fed with the same observations reach 95 % or more; 8 % means
they did not keep the same ones -- other channels, other platforms,
another thinning -- and the maps then speak for that small shared part
only. One cycle of both runs is enough to see which:

.. code-block:: bash

   c=<PATH_CONTROL_FILES>/2026091000_cris
   e=<PATH_EXPERIENCE_FILES>/2026091000_cris
   sqlite3 -header -column :memory: <<EOF
   ATTACH '$c' AS c;  ATTACH '$e' AS e;
   SELECT 'ctl' AS run, id_stn, COUNT(*) AS nobs, COUNT(DISTINCT vcoord) AS nchan
     FROM c.header NATURAL JOIN c.data GROUP BY id_stn
   UNION ALL
   SELECT 'exp', id_stn, COUNT(*), COUNT(DISTINCT vcoord)
     FROM e.header NATURAL JOIN e.data GROUP BY id_stn;
   SELECT COUNT(*) AS common_pixels FROM
     (SELECT DISTINCT id_stn,date,time,ROUND(lat,4) a,ROUND(lon,4) b FROM c.header)
     JOIN (SELECT DISTINCT id_stn,date,time,ROUND(lat,4) a,ROUND(lon,4) b FROM e.header)
     USING (id_stn,date,time,a,b);
   EOF

More channels or platforms on one side explain a low figure and are fine.
Few common pixels mean the suites did not select the same observations.

----

6. The web viewer
=================

Open ``$PATHWORK/pikobs_scatter_viewer.html`` in a browser, no server
needed, or the web address printed at the end of the run. The page starts
with a short explanation of the maps, written for the mode of the run
(single run or comparison), then a row of dropdowns:

* **Experience** (single run) or **Comparison** (control vs experience),
  always first;
* Family, Region, Surface, Flag, Function;
* **Difference / Significance**, only in comparison runs;
* Layer, Varno, Vcoord / Channel, Projection, Station, and the special
  column (*Method* for ``sw``) when ``SPECIAL_COLUMN="on"``.

Each dropdown only offers what exists for the choices on its left. The
page opens on the first function in alphabetical order, often ``bcorr`` or
``dens``; pick ``omp`` to see the significance maps. The **Flip** button
(key ``F``) toggles between the current map and the previous one, which is
the quickest way to go from *difference* to *significant only*, or from
one experience to the next with everything else fixed. A click on the map
opens it at full size.

----

7. Output layout
================

::

   $PATHWORK/
   ├── pikobs_scatter_viewer.html
   └── <family>/
       ├── scatter_<layer>_<run>_<region>[_<surface>]_<start>_<end>_bx<X>_by<Y>_<flag>_<family>.db
       ├── scatter_pair_<layer>_<control>_vs_<exp>_<region>[_<surface>]_..._<flag>_<family>.db
       ├── <fn>_<proj>_layer_<edges><unit>_flag_<flag>_id_stn_<stn>_<region>[_<surface>][_<special>]_vcoord_<vc>_varno<varno>_<run>.png
       ├── <fn>_..._<control>_vs_<exp>.png            difference
       ├── <fn>_..._<control>_vs_<exp>_signif.png     significance
       └── <fn>_..._<control>_vs_<exp>_sigonly.png    significant only

With ``SVG="on"`` each figure is written again as ``.svg`` beside its PNG,
for editing before a presentation: in Inkscape or Illustrator the titles,
the legends and the colours stay editable. The viewer always uses the PNG,
so turning it on changes nothing else. An SVG keeps every element of the
figure, so ask for it on the one or two figures you actually need.

The ``scatter_*.db`` files hold the per-box sums of each run (tables
``moyenne`` and ``stations``), the ``scatter_pair_*.db`` files the sums of
the common observations (table ``pairs``, columns ``n_omp``, ``sx_omp``,
``sy_omp``, ``sxx_omp``, ``syy_omp``, ``sxy_omp`` and the same with
``oma``). Both can be queried with ``sqlite3``. ``PATHWORK/<family>``
is wiped at the start of every run that passes the input check.

----

8. Support
==========

Bugs and feature requests:
   `<https://gitlab.science.gc.ca/dlo001/Pikobs/-/issues>`_
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import logging
import os
import re
import shutil
import sqlite3
import sys
import tempfile
import time
import traceback
import warnings
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Sequence, Tuple

import dask
import matplotlib as mpl
import numpy as np
import pandas as pd
from dask.distributed import Client

mpl.use('Agg')


from pikobs.pbs_submit import maybe_submit_to_pbs
from pikobs.figures import svg_enabled
# every touch of the observation files goes through this layer
from pikobs.obsdb import (check_input_files as _check_inputs,
                          combine as _combine_rows, cycle_path,
                          cycles as _cycles, fmt_bytes as _fmt_bytes,
                          input_size as _input_size, open_result, work_db)
from pikobs.parallel import run_tasks
# the significance tests live in one place, with their explanation
from pikobs.stats import MIN_CONFIDENCE as _MIN_CONF_SHARED
# station selection lives in its own module; re-exported here so that
# anything importing it from scatter keeps working
from pikobs.stations.stations import (StationSelector,
                                      expand_station_selectors,
                                      parse_channel_tokens,
                                      parse_station_tokens, _dedupe,
                                      _safe_filename, _split_tokens)
# a region is a box or a polygon; scatter does not need to know which
from pikobs.configobs import regionsobs as _regionsobs
# layers are the ones every module uses: hPa on a pressure family, km
# on a height one, none on a radiance
from pikobs.configobs.levels import (HEIGHT_LAYERS_KM, PRESSURE_LAYERS_HPA,
                                     layer_unit_scale, needs_layers)
from pikobs.configobs.special_family import special_select
from pikobs.configobs.landmask import register_surface, surface_sql

from pikobs.stations.stations import _RESOLUTION_LOGGED

import pikobs

warnings.filterwarnings("ignore", ".*ShapelyDeprecationWarning.*")


# ─────────────────────────────────────────────────────────────────────────────
# Module-level configuration
# ─────────────────────────────────────────────────────────────────────────────

# the resolution every module draws at (configobs/style.py): at 600 a map
# was 7760 x 4640 px, 3 MB, about 2 s and a few hundred MB to draw
from pikobs.configobs.style import DPI as _STYLE_DPI
DPI:             int   = _STYLE_DPI
FIG_SIZE:        tuple = (10, 10)
ALPHA_TILES:     float = 0.85
N_INTERVALS:     int   = 10
EARTH_RADIUS_KM: float = 6371.0
CYCLE_HOURS:     int   = 6

# Signed maps (difference maps, single omp/oma): symmetric "nice" levels
# m x 10^k with m in 1-2-3-5, e.g. 0.1 0.2 0.3 0.5 1 2. The first level
# is the white band, values beyond the last one are saturated.
_NICE_MANTISSAS  = (1, 2, 3, 5)
_NICE_N_LEVELS   = 6      # positive boundaries per map
_NICE_PERCENTILE = 95     # the scale covers this percentile of |value|

# Significance of a box difference: test confidence (1 - p) * 100 >= this.
# omp/oma need both the t-test (bias) and the F-test (sigma),
# stdomp/stdoma the F-test; obs, bcorr, nobs, dens: no test.
_MIN_CONFIDENCE = _MIN_CONF_SHARED

_WHITE_RGBA   = (1.0, 1.0, 1.0, 1.0)

# Map panels. In a control-vs-experience run every tested function gets a
# 'difference' map and a 'significance' map (test confidence 0-100 %).
PANEL_VALUE   = 'difference'
PANEL_CONF    = 'significance'
PANEL_SIGONLY = 'significant only'
_TESTED_FUNCS = ('omp', 'oma', 'stdomp', 'stdoma')
# Tested functions are compared on the observations common to both runs,
# matched one by one; quantity of the pair table used by each function.
_PAIR_Q = {'omp': 'omp', 'stdomp': 'omp',
           'oma': 'oma', 'stdoma': 'oma'}
_PAIR_QUANTITIES = ('omp', 'oma')


# difference maps expressed in percent
_PERCENT_FUNCS = ('stdomp', 'stdoma', 'nobs', 'NOBSHDR', 'dens', 'dens%',
                  'bcorr')

# Significance map: greys below the threshold, colours at/above it.
_CONF_BOUNDS = (0, 50, 80, 90, 95, 99, 100)
_CONF_COLORS = ('#f7f7f7', '#d9d9d9', '#bdbdbd', '#8c8c8c',
                '#fd8d3c', '#bd0026')
_BAD_RGBA     = (0.70, 0.70, 0.70, 0.5)

# Station list in the map title.
_TITLE_MAX_STATIONS = 15
_TITLE_WRAP_CHARS   = 60

# Wind-derivation method codes (BUFR table 002023).
WIND_TYPE_MAPPING: Dict[int, str] = {
    1: "Wind derived from cloud motion observed in the infrared channel",
    2: "Wind derived from cloud motion observed in the visible channel",
    3: "Wind derived from cloud motion observed in the water vapour channel",
    4: "Wind derived from motion observed in a combination of spectral channels",
    5: "Wind derived from motion observed in the water vapour channel in clear air",
    6: "Wind derived from motion observed in the ozone channel",
    7: "Wind derived from motion observed in water vapour channel (cloud or clear air not specified)",
}


# ─────────────────────────────────────────────────────────────────────────────
# Schema
# ─────────────────────────────────────────────────────────────────────────────

_MOYENNE_COLS = (
    "Nrej, Nacc, Nprofile, DATE, lat, lon, boite, id_stn, varno, vcoord, "
    "sumx, sumy, sumz, sumStat, sumx2, sumy2, sumz2, sumStat2, n, flag, CODTYP"
)

_DDL_MOYENNE = """
    CREATE TABLE IF NOT EXISTS moyenne (
        Nrej     INTEGER, Nacc      INTEGER, Nprofile INTEGER,
        DATE     INTEGER, lat       FLOAT,   lon      FLOAT,
        boite    INTEGER, id_stn    TEXT,    varno    INTEGER,
        vcoord   FLOAT,
        sumx     FLOAT,   sumy      FLOAT,   sumz     FLOAT, sumStat  FLOAT,
        sumx2    FLOAT,   sumy2     FLOAT,   sumz2    FLOAT, sumStat2 FLOAT,
        n        INTEGER, flag      INTEGER, CODTYP   INTEGER
        {extra}
    );
"""

# Every station that contributed to the aggregation, kept even when the
# tiles themselves are merged ("join"), so map titles can list them.
_DDL_STATIONS = """
    CREATE TABLE IF NOT EXISTS stations (
        id_stn TEXT, CODTYP INTEGER, varno INTEGER,
        UNIQUE (id_stn, CODTYP, varno)
    );
"""


_PAIR_STAT_COLS = ", ".join(
    f"n_{q}, sx_{q}, sy_{q}, sxx_{q}, syy_{q}, sxy_{q}"
    for q in _PAIR_QUANTITIES)

_PAIR_COLS = ("DATE, lat, lon, boite, varno, vcoord, id_stn, CODTYP, "
              + _PAIR_STAT_COLS)

_DDL_PAIRS = """
    CREATE TABLE IF NOT EXISTS pairs (
        DATE INTEGER, lat FLOAT, lon FLOAT, boite INTEGER,
        varno INTEGER, vcoord FLOAT, id_stn TEXT, CODTYP INTEGER,
        """ + ",\n        ".join(
            f"n_{q} INTEGER, sx_{q} FLOAT, sy_{q} FLOAT, "
            f"sxx_{q} FLOAT, syy_{q} FLOAT, sxy_{q} FLOAT"
            for q in _PAIR_QUANTITIES) + """
        {extra}
    );
"""


# ─────────────────────────────────────────────────────────────────────────────
# Small helpers
# ─────────────────────────────────────────────────────────────────────────────

def _n_days(d1: str, d2: str) -> float:
    """Days covered by the inclusive window of 6-h cycles [d1, d2]."""
    a = _dt.datetime.strptime(d1, "%Y%m%d%H")
    b = _dt.datetime.strptime(d2, "%Y%m%d%H")
    return (b - a).total_seconds() / 86_400.0 + CYCLE_HOURS / 24.0


def _surface_area_km2(lat1: np.ndarray, lat2: np.ndarray,
                      lon1: np.ndarray, lon2: np.ndarray) -> np.ndarray:
    lat1 = np.clip(lat1, -90.0, 90.0)
    lat2 = np.clip(lat2, -90.0, 90.0)
    return (EARTH_RADIUS_KM ** 2
            * np.abs(np.sin(np.deg2rad(lat2)) - np.sin(np.deg2rad(lat1)))
            * np.abs(lon2 - lon1)
            * np.deg2rad(1.0))


def _format_scientific_adaptive(x: float) -> str:
    if x is None or not np.isfinite(x):
        return ""
    if x == 0:
        return "0"
    a = abs(x)
    if a >= 10:
        return f"{int(x)}"
    if a >= 0.1:
        return f"{round(x, 2)}"
    m, e = f"{x:.1e}".split("e")
    return f"{m.split('.')[0]}e{int(e)}"


def get_wind_type(code: Any) -> Any:
    def _one(c: Any) -> str:
        try:
            return WIND_TYPE_MAPPING.get(int(c), f"Unknown code {c}")
        except (ValueError, TypeError):
            return f"Unknown code {c}"

    if isinstance(code, (list, tuple, set)):
        return [_one(c) for c in code]
    if isinstance(code, pd.Series):
        return code.map(_one)
    return _one(code)


# the special column of every table: the value as text, 'all' when the
# run does not split it (special_family.special_select)
_SPECIAL_DDL = ", special TEXT"


def _special_where(sp) -> str:
    """The condition of one special value; nothing for all."""
    if sp in (None, '', 'all'):
        return ''
    return " AND special = '" + str(sp).replace("'", "''") + "'"


def _strip_sql_types(extra_sw: str) -> str:
    return (extra_sw.replace(' INTEGER', '')
                    .replace(' FLOAT', '')
                    .replace(' TEXT', ''))


def _num(text: str) -> float:
    """argparse type: int when integral, float otherwise (10 -> 10, 2.5 -> 2.5)."""
    v = float(text)
    return int(v) if v.is_integer() else v


def _is_join(vc: Any) -> bool:
    return vc is None or (isinstance(vc, str) and vc.strip() == 'join')


def _vc_tag(vc: Any) -> str:
    if _is_join(vc):
        return "_join"
    try:
        f = float(vc)
    except (TypeError, ValueError):
        return "_" + _safe_filename(vc)
    if f.is_integer():
        return f"_{int(f)}"
    return "_" + f"{f:g}".replace('.', 'p').replace('-', 'm')


def _vc_display(vc: Any) -> str:
    if _is_join(vc):
        return "join"
    try:
        f = float(vc)
    except (TypeError, ValueError):
        return str(vc)
    return str(int(f)) if f.is_integer() else f"{f:g}"


def _vcoord_sql(vc: Any) -> str:
    if _is_join(vc):
        return ""
    return f" AND vcoord = {float(vc)!r}"


def _get_cmap(name: str, n: Optional[int] = None):
    try:
        base = mpl.colormaps[name]
    except AttributeError:                       # matplotlib < 3.5
        import matplotlib.cm as cm
        return cm.get_cmap(name, lut=n)
    return base.resampled(n) if n else base


def _mixed_sort_key(v: Any):
    if v is None:
        return (0, 0.0, "")
    if isinstance(v, (int, float)):
        return (1, float(v), "")
    return (2, 0.0, str(v))


# ─────────────────────────────────────────────────────────────────────────────
# Station / channel selection
# ─────────────────────────────────────────────────────────────────────────────

def _needs_station_detail(stn_tokens: Sequence[str]) -> bool:
    return any(t != 'join' for t in stn_tokens)


def _needs_vcoord_detail(chan_tokens: Sequence[str]) -> bool:
    return any(t != 'join' for t in chan_tokens)


# ─────────────────────────────────────────────────────────────────────────────
# Runs and comparisons
# ─────────────────────────────────────────────────────────────────────────────

@dataclass(frozen=True)
class Comparison:
    """One entry of the viewer experience/comparison selector."""
    key:   str                 # used in file names
    names: Tuple[str, ...]     # (run,) or (control, experiment)
    label: str                 # shown in the viewer


def build_comparisons(control: Optional[Tuple[str, str]],
                      experiments: Sequence[Tuple[str, str]]
                      ) -> List[Comparison]:
    """No control: one single-run entry per experiment.
    With control: one 'control vs experiment' entry per experiment."""
    if control is None:
        return [Comparison(name, (name,), name) for name, _ in experiments]
    ctrl = control[0]
    return [Comparison(f"{ctrl}_vs_{name}", (ctrl, name), f"{ctrl} vs {name}")
            for name, _ in experiments]


def _land_tag(land_ocean) -> str:
    """The surface in a file name, only when there is a filter."""
    return '' if land_ocean in (None, '', 'all') else f"_{land_ocean}"


def _agg_db_path(work_path: str, family: str, layer: str, name: str,
                 region: str, date_start: str, date_end: str,
                 box_size_x: float, box_size_y: float, fc: str,
                 land_ocean: str = 'all') -> str:
    return (f'{work_path}/{family}/scatter_{layer}_{_safe_filename(name)}_'
            f'{region}{_land_tag(land_ocean)}_{date_start}_{date_end}_'
            f'bx{box_size_x}_by{box_size_y}_{fc}_{family}.db')


# ─────────────────────────────────────────────────────────────────────────────
# SQLite helpers
# ─────────────────────────────────────────────────────────────────────────────

def create_table_if_not_exists(cursor, extra_sw: str = "") -> None:
    cursor.execute(_DDL_MOYENNE.format(extra=extra_sw))
    cursor.execute(_DDL_STATIONS)


def combine(pathfileout: str, filememory: str, extra_sw: str = "") -> None:
    """Append the moyenne/stations tables of *filememory* to *pathfileout*."""
    cols = _MOYENNE_COLS + _strip_sql_types(extra_sw)
    with open_result(pathfileout) as conn:
        conn.execute("PRAGMA journal_mode=OFF;")
        conn.execute("PRAGMA synchronous=OFF;")
        create_table_if_not_exists(conn, extra_sw)
        conn.execute("ATTACH DATABASE ? AS src;", (filememory,))
        conn.execute("BEGIN IMMEDIATE;")
        conn.execute(f"INSERT INTO moyenne ({cols}) "
                     f"SELECT {cols} FROM src.moyenne;")
        conn.execute("INSERT OR IGNORE INTO stations (id_stn, CODTYP, varno) "
                     "SELECT id_stn, CODTYP, varno FROM src.stations;")
        conn.execute("COMMIT;")
        conn.execute("DETACH DATABASE src;")


def _table_columns(db_path: str, table: str) -> List[str]:
    try:
        with open_result(db_path) as conn:
            return [c[1] for c in
                    conn.execute(f"PRAGMA table_info('{table}');")]
    except Exception:
        return []


def _query_distinct(db_paths: Sequence[str], sql: str,
                    params: Sequence[Any] = ()) -> List[tuple]:
    """Run *sql* on every db and return the ordered union of the rows."""
    seen: Dict[tuple, None] = {}
    for path in db_paths:
        if not os.path.isfile(path):
            continue
        try:
            with open_result(path) as conn:
                rows = conn.execute(sql, params).fetchall()
        except sqlite3.Error as exc:
            print(f"[scatter] query failed on {os.path.basename(path)}: {exc}",
                  file=sys.stderr)
            continue
        for r in rows:
            seen.setdefault(tuple(r), None)
    return list(seen)


# ─────────────────────────────────────────────────────────────────────────────
# PHASE 1 -- Aggregation
# ─────────────────────────────────────────────────────────────────────────────

def create_and_populate_moyenne_table(
        family:               str,
        new_db_filename:      str,
        existing_db_filename: str,
        selected_region:      str,
        selected_flags:       str,
        boxsizex:             float,
        boxsizey:             float,
        varnos:               Sequence[str],
        keep_station:         bool,
        keep_vcoord:          bool,
        interval:             Tuple[Optional[int], Optional[int]],
        special_column_on:    bool = False,
        pathwork:             str = '.',
        channels:             Sequence[float] = (),
        land_ocean:           str = 'all') -> Optional[str]:
    """Aggregate one source RDB file into per-box sums.

    The source is always read at station resolution into a temporary
    table; the station list is saved from it, then the tiles are written
    either per station (keep_station) or merged.
    """
    if not os.path.isfile(existing_db_filename):
        print(f"[scatter] missing file, skipped: {existing_db_filename}",
              file=sys.stderr)
        return None

    date_match = re.search(r'(\d{10})', os.path.basename(existing_db_filename))
    if not date_match:
        raise ValueError("No 10-digit date in source filename: "
                         f"{os.path.basename(existing_db_filename)}")
    date_int = int(date_match.group(1))

    FAM, VCOORD, VCOCRIT, STATB, element, VCOTYP = pikobs.family(family)
    if varnos:
        element = ",".join(str(v) for v in varnos)

    latlon_crit = _regionsobs.criteria(selected_region, pathwork)
    latlon_crit += surface_sql(land_ocean)        # nothing for all
    flag_crit   = pikobs.flag_criteria(selected_flags)
    # the channels asked for, as the matching filters them: without
    # this every channel of a hyperspectral file was aggregated,
    # stored and compacted, and all but the requested ones dropped at
    # the plots (616 IASI channels for CHANNEL=(32))
    chan_crit = ''
    if channels:
        chan_crit = "AND (" + " OR ".join(
            f"ABS({VCOORD} - {float(c)!r}) < 1e-5" for c in channels) + ")"

    boite = (f"floor(360. / {boxsizex}) * floor(lat / {boxsizey}) "
             f"+ floor(MIN(179.99, lon) / {boxsizex})")
    lat_c = f"floor(lat / {boxsizey}) * {boxsizey} + {boxsizey} / 2."
    lon_c = (f"floor(MIN(179.99, lon) / {boxsizex}) * {boxsizex} "
             f"+ {boxsizex} / 2.")

    # a layer carries its rank as a third element, so take the edges by
    # position; they are stored low, high whichever way the list is read
    a, b = interval[0], interval[1]
    if a is not None and b is not None and a > b:
        a, b = b, a
    scale = layer_unit_scale(VCOTYP)
    interval_crit = ('' if (a is None and b is None)
                     # a layer keeps its larger number: 500 hPa in 500-250 only
                     else f"AND vcoord > {a * scale} "
                          f"AND vcoord <= {b * scale}")

    with work_db(attach={'db': existing_db_filename}) as (mem_conn, mem_uri):
        _regionsobs.register(mem_conn, [selected_region], pathwork)
        register_surface(mem_conn, [land_ocean], pathwork)

        data_cols = [c[1].upper() for c in
                     mem_conn.execute("PRAGMA db.table_info('DATA');")]
        head_cols = [c[1] for c in
                     mem_conn.execute("PRAGMA db.table_info('HEADER');")]
        if not data_cols or not head_cols:
            print(f"[scatter] no HEADER/DATA in {existing_db_filename}",
                  file=sys.stderr)
            return None

        has_bias_corr = 'BIAS_CORR' in data_cols
        # the special column, or the constant 'all': grouping by a
        # constant changes no group (special_family.special_select)
        sp_expr, _    = special_select(family, head_cols, special_column_on)
        has_special   = True
        extra_sw      = _SPECIAL_DDL
        extra_cols    = _strip_sql_types(extra_sw)

        sum_bc  = "SUM(bias_corr)"           if has_bias_corr else "NULL"
        sum_bc2 = "SUM(bias_corr*bias_corr)" if has_bias_corr else "NULL"
        vc_sel  = VCOORD if keep_vcoord else "'join'"
        sp_sel  = f",\n               {sp_expr} AS d_special"

        # Positional GROUP BY: 4=d_boite 5=d_varno 6=d_vcoord
        #                      19=d_id_stn 20=d_codtyp 21=d_special
        group_by = ["4", "5"]
        if keep_vcoord:
            group_by.append("6")
        group_by += ["19", "20"]
        if has_special:
            group_by.append("21")

        # d_ prefixes avoid any alias / source-column ambiguity in WHERE.
        mem_conn.execute(f"""
        CREATE TABLE detail AS
        SELECT {date_int}                 AS DATE,
               {lat_c}                    AS d_lat,
               {lon_c}                    AS d_lon,
               {boite}                    AS d_boite,
               varno                      AS d_varno,
               {vc_sel}                   AS d_vcoord,
               SUM(omp)                   AS sumx,
               SUM(oma)                   AS sumy,
               SUM(obsvalue)              AS sumz,
               {sum_bc}                   AS sumStat,
               SUM(omp*omp)               AS sumx2,
               SUM(oma*oma)               AS sumy2,
               SUM(obsvalue*obsvalue)     AS sumz2,
               {sum_bc2}                  AS sumStat2,
               COUNT(*)                   AS n,
               SUM((flag & 512)  = 512)   AS Nrej,
               SUM((flag & 4096) = 4096)  AS Nacc,
               COUNT(DISTINCT id_obs)     AS Nprofile,
               id_stn                     AS d_id_stn,
               CODTYP                     AS d_codtyp{sp_sel}
        FROM db.header NATURAL JOIN db.data
        WHERE varno IN ({element})
          AND obsvalue IS NOT NULL
          {flag_crit}
          {latlon_crit}
          {VCOCRIT}
          {chan_crit}
          {interval_crit}
        GROUP BY {', '.join(group_by)};
        """)

        create_table_if_not_exists(mem_conn, extra_sw)
        cols    = _MOYENNE_COLS + extra_cols
        sp_pass = ", d_special" if has_special else ""

        if keep_station:
            mem_conn.execute(f"""
            INSERT INTO moyenne ({cols})
            SELECT Nrej, Nacc, Nprofile, DATE, d_lat, d_lon, d_boite,
                   d_id_stn, d_varno, d_vcoord,
                   sumx, sumy, sumz, sumStat, sumx2, sumy2, sumz2, sumStat2,
                   n, NULL, d_codtyp{sp_pass}
            FROM detail;
            """)
        else:
            mem_conn.execute(f"""
            INSERT INTO moyenne ({cols})
            SELECT SUM(Nrej), SUM(Nacc), SUM(Nprofile), DATE,
                   MIN(d_lat), MIN(d_lon), d_boite,
                   'join', d_varno, d_vcoord,
                   SUM(sumx), SUM(sumy), SUM(sumz), SUM(sumStat),
                   SUM(sumx2), SUM(sumy2), SUM(sumz2), SUM(sumStat2),
                   SUM(n), NULL, NULL{sp_pass}
            FROM detail
            GROUP BY d_boite, d_varno, d_vcoord{sp_pass};
            """)

        mem_conn.execute("""
        INSERT OR IGNORE INTO stations (id_stn, CODTYP, varno)
        SELECT DISTINCT d_id_stn, d_codtyp, d_varno FROM detail;
        """)
        mem_conn.execute("DROP TABLE detail;")
        mem_conn.execute("DETACH DATABASE db;")

        # The memory db stays alive while mem_conn is open.
        combine(new_db_filename, mem_uri, extra_sw)
        return new_db_filename


def _aggregate_task(task: Dict[str, Any]) -> Optional[str]:
    try:
        return create_and_populate_moyenne_table(
            task['family'], task['db_new'], task['filein'],
            task['region'], task['flag_criteria'],
            task['boxsizex'], task['boxsizey'], task['varnos'],
            task['keep_station'], task['keep_vcoord'], task['interval'],
            special_column_on=task['special_column_on'],
            pathwork=task.get('pathwork', '.'),
            channels=task.get('channels', ()),
            land_ocean=task.get('land_ocean', 'all'),
        )
    except Exception:
        print(f"[scatter] aggregation failed for {task['filein']}:\n"
              f"{traceback.format_exc()}", file=sys.stderr)
        return None


def _pair_db_path(work_path: str, family: str, layer: str, ctl: str,
                  exp: str, region: str, date_start: str, date_end: str,
                  box_size_x: float, box_size_y: float, fc: str,
                  land_ocean: str = 'all') -> str:
    return (f'{work_path}/{family}/scatter_pair_{layer}_'
            f'{_safe_filename(ctl)}_vs_{_safe_filename(exp)}_'
            f'{region}{_land_tag(land_ocean)}_{date_start}_{date_end}_'
            f'bx{box_size_x}_by{box_size_y}_{fc}_{family}.db')


def _combine_pairs(pathfileout: str, filememory: str, extra_sw: str) -> None:
    cols = _PAIR_COLS + _strip_sql_types(extra_sw)
    _combine_rows(pathfileout, filememory, 'pairs', cols,
                  ddl=_DDL_PAIRS.format(extra=extra_sw), module='scatter')


def create_pair_table(family:            str,
                      pair_db:           str,
                      ctl_file:          str,
                      exp_file:          str,
                      selected_region:   str,
                      selected_flags:    str,
                      boxsizex:          float,
                      boxsizey:          float,
                      varnos:            Sequence[str],
                      keep_station:      bool,
                      keep_vcoord:       bool,
                      interval:          Tuple[Optional[int], Optional[int]],
                      special_column_on: bool = False,
                      channels:          Sequence[float] = (),
                      pathwork:          str = '.',
                      match_fields:      Sequence[str] = (),
                      names=None,
                      land_ocean:        str = 'all'
                      ) -> Optional[Dict[str, int]]:
    """Match control and experience observation by observation.

    Key: ID_STN, DATE, TIME, LAT and LON rounded to 1e-4 degree, VCOORD,
    VARNO (see pikobs.match). Both runs are filtered the same way (flag criteria applied to
    each run's own flags). The key and what happens when it repeats are
    pikobs.match's: a repeated key is paired one to one by value and
    counted, never dropped. For every box the pair table keeps, per quantity
    (omp, oma, bias correction), the number of pairs and
    Σx, Σy, Σx², Σy², Σxy with x = control and y = experience.
    """
    for f in (ctl_file, exp_file):
        if not os.path.isfile(f):
            print(f"[scatter] missing file, pairs skipped: {f}",
                  file=sys.stderr)
            return None

    date_match = re.search(r'(\d{10})', os.path.basename(ctl_file))
    if not date_match:
        raise ValueError("No 10-digit date in source filename: "
                         f"{os.path.basename(ctl_file)}")
    date_int = int(date_match.group(1))

    FAM, VCOORD, VCOCRIT, STATB, element, VCOTYP = pikobs.family(family)
    if varnos:
        element = ",".join(str(v) for v in varnos)
    latlon_crit = _regionsobs.criteria(selected_region, pathwork)
    latlon_crit += surface_sql(land_ocean)        # nothing for all
    flag_crit   = pikobs.flag_criteria(selected_flags)

    boite = (f"floor(360. / {boxsizex}) * floor(lat / {boxsizey}) "
             f"+ floor(MIN(179.99, lon) / {boxsizex})")
    lat_c = f"floor(lat / {boxsizey}) * {boxsizey} + {boxsizey} / 2."
    lon_c = (f"floor(MIN(179.99, lon) / {boxsizex}) * {boxsizex} "
             f"+ {boxsizex} / 2.")

    a, b = interval[0], interval[1]
    if a is not None and b is not None and a > b:
        a, b = b, a
    scale = layer_unit_scale(VCOTYP)
    interval_crit = ('' if (a is None and b is None)
                     # a layer keeps its larger number: 500 hPa in 500-250 only
                     else f"AND vcoord > {a * scale} "
                          f"AND vcoord <= {b * scale}")
    chan_crit = ''
    if channels:
        chan_crit = "AND (" + " OR ".join(
            f"ABS({VCOORD} - {float(c)!r}) < 1e-5" for c in channels) + ")"

    with work_db(attach={'c': ctl_file, 'e': exp_file}) as (mem_conn,
                                                            mem_uri):
        _regionsobs.register(mem_conn, [selected_region], pathwork)
        register_surface(mem_conn, [land_ocean], pathwork)

        def cols(schema, table):
            return [r[1] for r in mem_conn.execute(
                f"PRAGMA {schema}.table_info('{table}');")]

        head_c, head_e = cols('c', 'HEADER'), cols('e', 'HEADER')
        data_c, data_e = cols('c', 'DATA'), cols('e', 'DATA')
        if not (head_c and head_e and data_c and data_e):
            return None
        has_bc = ('BIAS_CORR' in [x.upper() for x in data_c]
                  and 'BIAS_CORR' in [x.upper() for x in data_e])
        # the special column when both runs carry it, else 'all'
        sp_c, _ = special_select(family, head_c, special_column_on)
        sp_e, _ = special_select(family, head_e, special_column_on)
        sp_expr = sp_c if sp_c == sp_e else "'all'"
        has_special = True
        extra_sw = _SPECIAL_DDL

        # the pairing key from pikobs.match, as m_* columns: the k_*
        # columns stay, they are read after the join
        from pikobs.match import (DEFAULT_KEY, MatchSpec, count_repeats,
                                  key_aliases, key_join, key_select)
        spec = MatchSpec(True, tuple(match_fields) or DEFAULT_KEY)
        msel = key_select(spec, prefix='m_')
        join_on = key_join(spec, prefix='m_')
        vc_sel = VCOORD if keep_vcoord else "'join'"
        sp_sel = f", {sp_expr} AS p_special"
        bc_sel = "bias_corr" if has_bc else "NULL"

        counts: Dict[str, int] = {}
        for schema in ('c', 'e'):
            mem_conn.execute(f"""
            CREATE TABLE raw_{schema} AS
            SELECT {msel},
                   id_stn             AS k_stn,
                   date               AS k_date,
                   time               AS k_time,
                   ROUND(lat, 4)      AS k_lat,
                   ROUND(lon, 4)      AS k_lon,
                   varno              AS k_varno,
                   vcoord             AS k_vcoord,
                   {lat_c}            AS p_lat,
                   {lon_c}            AS p_lon,
                   {boite}            AS p_boite,
                   {vc_sel}           AS p_vcoord,
                   codtyp             AS p_codtyp{sp_sel},
                   omp, oma, {bc_sel} AS bc
            FROM {schema}.header AS h NATURAL JOIN {schema}.data AS d
            WHERE varno IN ({element})
              AND obsvalue IS NOT NULL
              {flag_crit}
              {latlon_crit}
              {VCOCRIT}
              {interval_crit}
              {chan_crit};
            """)
            key = ", ".join(key_aliases(spec, prefix='m_'))
            # a repeated key is not dropped any more: the rank inside it
            # pairs its observations one to one (pikobs.match); the count
            # looks at the rows a sum can use
            n_keys, n_rows = count_repeats(
                mem_conn, f"raw_{schema}",
                key_aliases(spec, with_rank=False, prefix='m_'),
                where="omp IS NOT NULL OR oma IS NOT NULL")
            counts[f'obs_{schema}'] = mem_conn.execute(
                f"SELECT COUNT(*) FROM raw_{schema};").fetchone()[0]
            counts[f'rep_keys_{schema}'] = n_keys
            counts[f'rep_rows_{schema}'] = n_rows
            mem_conn.execute(f"ALTER TABLE raw_{schema} RENAME TO key_{schema};")
            mem_conn.execute(
                f"CREATE INDEX idx_{schema} ON key_{schema} ({key});")

        stats = []
        for q in _PAIR_QUANTITIES:
            both = f"(c.{q} IS NOT NULL AND e.{q} IS NOT NULL)"
            stats.append(
                f"SUM({both}) AS n_{q}, "
                f"SUM(CASE WHEN {both} THEN c.{q} END) AS sx_{q}, "
                f"SUM(CASE WHEN {both} THEN e.{q} END) AS sy_{q}, "
                f"SUM(CASE WHEN {both} THEN c.{q} * c.{q} END) AS sxx_{q}, "
                f"SUM(CASE WHEN {both} THEN e.{q} * e.{q} END) AS syy_{q}, "
                f"SUM(CASE WHEN {both} THEN c.{q} * e.{q} END) AS sxy_{q}")
        sp_pass  = ", c.p_special AS d_special" if has_special else ""
        group_by = ["c.p_boite", "c.k_varno"]
        if keep_vcoord:
            group_by.append("c.p_vcoord")
        group_by += ["c.k_stn", "c.p_codtyp"]
        if has_special:
            group_by.append("c.p_special")

        mem_conn.execute(f"""
        CREATE TABLE pdetail AS
        SELECT {date_int}   AS DATE,
               MIN(c.p_lat) AS d_lat, MIN(c.p_lon) AS d_lon,
               c.p_boite    AS d_boite, c.k_varno AS d_varno,
               c.p_vcoord   AS d_vcoord,
               c.k_stn      AS d_id_stn, c.p_codtyp AS d_codtyp{sp_pass},
               COUNT(*)     AS n_pairs,
               {", ".join(stats)}
        FROM key_c AS c JOIN key_e AS e ON {join_on}
        GROUP BY {", ".join(group_by)};
        """)
        counts['pairs'] = mem_conn.execute(
            "SELECT COALESCE(SUM(n_pairs), 0) FROM pdetail;").fetchone()[0]

        mem_conn.execute(_DDL_PAIRS.format(extra=extra_sw))
        extra_cols = _strip_sql_types(extra_sw)
        sp_out     = ", d_special" if has_special else ""
        stat_cols  = [c.strip() for c in _PAIR_STAT_COLS.split(",")]
        if keep_station:
            mem_conn.execute(f"""
            INSERT INTO pairs ({_PAIR_COLS}{extra_cols})
            SELECT DATE, d_lat, d_lon, d_boite, d_varno, d_vcoord,
                   d_id_stn, d_codtyp, {", ".join(stat_cols)}{sp_out}
            FROM pdetail;
            """)
        else:
            sums = ", ".join(f"SUM({c})" for c in stat_cols)
            mem_conn.execute(f"""
            INSERT INTO pairs ({_PAIR_COLS}{extra_cols})
            SELECT DATE, MIN(d_lat), MIN(d_lon), d_boite, d_varno, d_vcoord,
                   'join', NULL, {sums}{sp_out}
            FROM pdetail
            GROUP BY d_boite, d_varno, d_vcoord{sp_out};
            """)
        for t in ('pdetail', 'key_c', 'key_e'):
            mem_conn.execute(f"DROP TABLE {t};")
        mem_conn.execute("DETACH DATABASE c;")
        mem_conn.execute("DETACH DATABASE e;")

        _combine_pairs(pair_db, mem_uri, extra_sw)
        return counts


_SUM_COLS = {
    'moyenne': ('Nrej', 'Nacc', 'Nprofile', 'sumx', 'sumy', 'sumz', 'sumStat',
                'sumx2', 'sumy2', 'sumz2', 'sumStat2', 'n'),
    'pairs':   tuple(c.strip() for c in _PAIR_STAT_COLS.split(",")),
}
_FIRST_COLS = ('DATE', 'lat', 'lon')
_NULL_COLS  = ('flag',)


def compact_db(path: str, table: str, tmp_dir: str) -> Optional[str]:
    """Sum the per-cycle rows of an aggregated database over the period.

    The aggregation writes one row per (box, station, channel, cycle);
    the maps never need the cycle, so rows are merged on every other key
    and an index is added. This keeps the plotting queries small.
    """
    if not os.path.isfile(path):
        return None
    os.makedirs(tmp_dir, exist_ok=True)
    os.environ["SQLITE_TMPDIR"] = tmp_dir
    new = path + ".compact"
    if os.path.exists(new):
        os.remove(new)
    with open_result(new) as conn:
        conn.execute("PRAGMA journal_mode = OFF;")
        conn.execute("PRAGMA synchronous = OFF;")
        conn.execute("PRAGMA temp_store = FILE;")
        conn.execute("ATTACH DATABASE ? AS src;", (path,))
        ddl = dict(conn.execute(
            "SELECT name, sql FROM src.sqlite_master WHERE type = 'table';"
        ).fetchall())
        if table not in ddl:
            return None
        cols = [r[1] for r in conn.execute(f"PRAGMA src.table_info('{table}');")]
        sums = set(_SUM_COLS[table])
        keys = [c for c in cols
                if c not in sums and c not in _FIRST_COLS and c not in _NULL_COLS]
        select = []
        for c in cols:
            if c in sums:
                select.append(f"SUM({c})")
            elif c in _FIRST_COLS:
                select.append(f"MIN({c})")
            elif c in _NULL_COLS:
                select.append("NULL")
            else:
                select.append(c)

        conn.execute(ddl[table].replace(f"IF NOT EXISTS {table}", table))
        conn.execute("BEGIN;")
        conn.execute(f"""
            INSERT INTO {table} ({", ".join(cols)})
            SELECT {", ".join(select)}
            FROM src.{table}
            GROUP BY {", ".join(keys)};
        """)
        if 'stations' in ddl:
            conn.execute(ddl['stations'].replace("IF NOT EXISTS stations",
                                                 "stations"))
            conn.execute("INSERT OR IGNORE INTO stations "
                         "SELECT * FROM src.stations;")
        conn.execute("COMMIT;")
        index_cols = [c for c in ('varno', 'vcoord', 'id_stn', 'CODTYP')
                      if c in cols]
        conn.execute(f"CREATE INDEX idx_{table} ON {table} "
                     f"({', '.join(index_cols)});")
        conn.execute("DETACH DATABASE src;")
    os.replace(new, path)
    return path


def _compact_task(path: str, table: str, tmp_dir: str) -> Optional[str]:
    try:
        return compact_db(path, table, tmp_dir)
    except Exception:
        print(f"[scatter] compaction failed for {path}:\n"
              f"{traceback.format_exc()}", file=sys.stderr)
        return None


def _pair_task(task: Dict[str, Any]) -> Optional[Dict[str, int]]:
    try:
        return create_pair_table(
            task['family'], task['pair_db'], task['ctl_file'],
            task['exp_file'], task['region'], task['flag_criteria'],
            task['boxsizex'], task['boxsizey'], task['varnos'],
            task['keep_station'], task['keep_vcoord'], task['interval'],
            special_column_on=task['special_column_on'],
            channels=task['channels'],
            pathwork=task.get('pathwork', '.'),
            match_fields=task.get('match_fields') or (),
            names=task.get('names'),
            land_ocean=task.get('land_ocean', 'all'),
        )
    except Exception:
        print(f"[scatter] pairing failed for {task['exp_file']}:\n"
              f"{traceback.format_exc()}", file=sys.stderr)
        return None


def create_pair_list(date_start: str, date_end: str, families: List[str],
                     control: Tuple[str, str],
                     experiments: Sequence[Tuple[str, str]],
                     work_path: str, box_size_x: float, box_size_y: float,
                     flag_criteria: List[str], regions: List[str],
                     varnos: List[str],
                     keep_station: bool, keep_vcoord: bool,
                     channels: Sequence[float],
                     special_column_on: bool = False,
                     pressure_layers: Sequence[float] = (),
                     height_layers: Sequence[float] = (),
                     land_oceans: Sequence[str] = ('all',)
                     ) -> List[Dict[str, Any]]:
    """One pairing task per (cycle, flag, family, region, experiment, layer)."""
    ctl_name, ctl_path = control
    tasks: List[Dict[str, Any]] = []
    for fdate in _cycles(date_start, date_end):
        for fc in flag_criteria:
            for family in families:
                for region, land_ocean in [(r, s) for r in regions
                                           for s in land_oceans]:
                    for exp_name, exp_path in experiments:
                        for interval in family_layers(
                                family, pressure_layers, height_layers):
                            tasks.append({
                                'family':            family,
                                'ctl_file':          cycle_path(
                                    ctl_path, fdate, family),
                                'exp_file':          cycle_path(
                                    exp_path, fdate, family),
                                'exp_name':          exp_name,
                                'pair_db':           _pair_db_path(
                                    work_path, family,
                                    _layer_label(interval, _vcotyp(family)),
                                    ctl_name, exp_name, region, date_start,
                                    date_end, box_size_x, box_size_y, fc,
                                    land_ocean),
                                'region':            region,
                                'land_ocean':        land_ocean,
                                'flag_criteria':     fc,
                                'boxsizex':          box_size_x,
                                'boxsizey':          box_size_y,
                                'varnos':            varnos,
                                'interval':          interval,
                                'keep_station':      keep_station,
                                'keep_vcoord':       keep_vcoord,
                                'channels':          list(channels),
                                'special_column_on': special_column_on,
                                'pathwork':          work_path,
                            })
    return tasks


# ─────────────────────────────────────────────────────────────────────────────
# Task list builders
# ─────────────────────────────────────────────────────────────────────────────

def _vcotyp(family: str) -> str:
    """What the vertical coordinate of a family is."""
    try:
        return pikobs.family(family)[5]
    except Exception:
        return ''


def _layer_unit(vcotyp: str) -> str:
    return 'km' if layer_unit_scale(vcotyp) == 1000.0 else 'hPa'


def _layer_label(interval, vcotyp: str = '') -> str:
    """Tag of a layer in file names: sorts by height, reads as written."""
    a, b = interval[0], interval[1]
    if a is None and b is None:
        return 'layer_all'
    return f'layer_{a:g}_{b:g}{_layer_unit(vcotyp)}'


def _layer_display(interval, vcotyp: str = '') -> str:
    """'2 | 850-500 hPa': the rank first, so a viewer sorts by height and
    not alphabetically, where 1000 would come before 500."""
    a, b = interval[0], interval[1]
    if a is None and b is None:
        return 'layer_all'
    rank = interval[2] if len(interval) > 2 else 0
    return f'{rank} | {a:g}-{b:g} {_layer_unit(vcotyp)}'


def family_layers(family: str,
                  pressure: Sequence[float] = (),
                  height: Sequence[float] = ()) -> List[tuple]:
    """The layers of one family: the whole column, then each layer.

    A family whose vertical coordinate is a channel, a surface or a band
    of latitude has no layer to speak of, and an empty list of edges
    means the whole column: in both cases the run keeps the single
    ``layer_all`` series it always had.
    """
    vcotyp = _vcotyp(family)
    if not needs_layers(vcotyp):
        return [(None, None)]
    edges = list(pressure if _layer_unit(vcotyp) == 'hPa' else height)
    if not edges:
        return [(None, None)]          # the whole column, in one series
    out = [(None, None)]
    for i, (a, b) in enumerate(zip(edges[:-1], edges[1:]), start=1):
        out.append((float(a), float(b), i))
    return out


def create_data_list(date_start:        str,
                     date_end:          str,
                     families:          List[str],
                     runs:              Sequence[Tuple[str, str]],
                     work_path:         str,
                     box_size_x:        float,
                     box_size_y:        float,
                     flag_criteria:     List[str],
                     regions:           List[str],
                     varnos:            List[str],
                     keep_station:      bool,
                     keep_vcoord:       bool,
                     special_column_on: bool = False,
                     pressure_layers:   Sequence[float] = (),
                     height_layers:     Sequence[float] = (),
                     land_oceans:       Sequence[str] = ('all',),
                     ) -> List[Dict[str, Any]]:
    """One aggregation task per (cycle, flag, family, region, surface,
    run, layer)."""
    tasks: List[Dict[str, Any]] = []
    cur    = _dt.datetime.strptime(date_start, '%Y%m%d%H')
    dt_end = _dt.datetime.strptime(date_end,   '%Y%m%d%H')

    while cur <= dt_end:
        fdate = cur.strftime('%Y%m%d%H')
        for fc in flag_criteria:
            for family in families:
                for region, land_ocean in [(r, s) for r in regions
                                           for s in land_oceans]:
                    for name, in_path in runs:
                        for interval in family_layers(
                                family, pressure_layers, height_layers):
                            tasks.append({
                                'family':            family,
                                'filein':            cycle_path(
                                    in_path, fdate, family),
                                'db_new':            _agg_db_path(
                                    work_path, family,
                                    _layer_label(interval, _vcotyp(family)),
                                    name, region, date_start, date_end,
                                    box_size_x, box_size_y, fc, land_ocean),
                                'region':            region,
                                'land_ocean':        land_ocean,
                                'flag_criteria':     fc,
                                'boxsizex':          box_size_x,
                                'boxsizey':          box_size_y,
                                'varnos':            varnos,
                                'interval':          interval,
                                'keep_station':      keep_station,
                                'keep_vcoord':       keep_vcoord,
                                'special_column_on': special_column_on,
                                'pathwork':          work_path,
                            })
        cur += _dt.timedelta(hours=CYCLE_HOURS)
    return tasks


def _vcoord_items(db_paths: Sequence[str], where: str,
                  chan_tokens: Sequence[str]) -> List[Tuple[Any, int]]:
    items:     List[Tuple[Any, int]] = []
    requested: List[str]             = []

    for tok in chan_tokens:
        if tok == 'join':
            rows = _query_distinct(
                db_paths, f"SELECT DISTINCT varno FROM moyenne {where};")
            items += [('join', r[0]) for r in rows]
        elif tok == 'all':
            items += _query_distinct(
                db_paths,
                f"SELECT DISTINCT vcoord, varno FROM moyenne {where} "
                f"AND typeof(vcoord) != 'text';")
        else:
            requested.append(tok)

    if requested:
        rows = _query_distinct(
            db_paths,
            f"SELECT DISTINCT vcoord, varno FROM moyenne {where} "
            f"AND typeof(vcoord) != 'text';")
        for vc, vn in rows:
            for rc in requested:
                try:
                    if abs(float(vc) - float(rc)) < 1e-5:
                        items.append((vc, vn))
                        break
                except (TypeError, ValueError):
                    if str(vc).strip() == rc:
                        items.append((vc, vn))
                        break

    items = _dedupe(items)
    items.sort(key=lambda it: (it[1],
                               0 if _is_join(it[0]) else 1,
                               0.0 if _is_join(it[0]) else float(it[0])))
    return items


def _enumerate_selections(db_paths: Sequence[str], family: str,
                          stn_tokens: Sequence[str],
                          chan_tokens: Sequence[str],
                          special_col: Optional[str],
                          layer_note: str = 'this selection'
                          ) -> List[Tuple[StationSelector, Any, Any, int]]:
    out = []
    for sel in expand_station_selectors(db_paths, stn_tokens, family):
        base    = sel.sql()
        sp_vals: List[Any] = [None]
        if special_col:
            rows = _query_distinct(
                db_paths,
                f"SELECT DISTINCT {special_col} FROM moyenne "
                f"WHERE {special_col} IS NOT NULL{base};")
            vals = sorted((r[0] for r in rows), key=_mixed_sort_key)
            sp_vals = vals or [None]

        n_before = len(out)
        for sp in sp_vals:
            where = f"WHERE 1=1{base}{_special_where(sp)}"
            for vc, vn in _vcoord_items(db_paths, where, chan_tokens):
                out.append((sel, sp, vc, vn))
        if len(out) == n_before:
            key = (family, 'nodata', sel, layer_note)
            if key not in _RESOLUTION_LOGGED:
                _RESOLUTION_LOGGED.add(key)
                print(f"[scatter] {family}: nothing in {layer_note} for "
                      f"id_stn '{sel.display}', no map there (the other "
                      f"layers are drawn as usual)")
    return out


def _has_bias_corr(db_paths: Sequence[str]) -> bool:
    """True when the aggregated data hold a bias correction (radiances)."""
    return bool(_query_distinct(
        db_paths,
        "SELECT 1 FROM moyenne WHERE sumStat IS NOT NULL LIMIT 1;"))


def _log_once(key, text: str) -> None:
    if key not in _RESOLUTION_LOGGED:
        _RESOLUTION_LOGGED.add(key)
        print(text)


def create_data_list_plot(date_start:        str,
                          date_end:          str,
                          families:          List[str],
                          run_names:         Sequence[str],
                          comparisons:       Sequence[Comparison],
                          work_path:         str,
                          box_size_x:        float,
                          box_size_y:        float,
                          functions:         List[str],
                          flag_criteria:     List[str],
                          regions:           List[str],
                          stn_tokens:        Sequence[str],
                          chan_tokens:       Sequence[str],
                          projections:       List[str],
                          special_column_on: bool = False,
                          pressure_layers:   Sequence[float] = (),
                          height_layers:     Sequence[float] = (),
                          land_oceans:       Sequence[str] = ('all',),
                          ) -> List[Dict[str, Any]]:
    """One plot task per (selection x comparison x function x projection).

    Selections are enumerated once on the union of all run databases, so
    every comparison is drawn for the same stations and channels.
    """
    tasks: List[Dict[str, Any]] = []
    for fc in flag_criteria:
        for family in families:
            for interval in family_layers(family, pressure_layers,
                                          height_layers):
                layer = _layer_label(interval, _vcotyp(family))
                for region, land_ocean in [(r, s) for r in regions
                                           for s in land_oceans]:
                    db_of = {name: _agg_db_path(work_path, family, layer, name,
                                                region, date_start, date_end,
                                                box_size_x, box_size_y, fc,
                                                land_ocean)
                             for name in run_names}
                    db_paths = [p for p in db_of.values() if os.path.isfile(p)]
                    if not db_paths:
                        print(f"[scatter] no aggregated data for {family} / "
                              f"{region} / {fc} / {layer}", file=sys.stderr)
                        continue

                    # every table has the special column, 'all' when off
                    sp_col, has_sp = 'special', True

                    selections = _enumerate_selections(
                        db_paths, family, stn_tokens, chan_tokens,
                        sp_col if has_sp else None,
                        _layer_display(interval, _vcotyp(family)))

                    has_bc = _has_bias_corr(db_paths)
                    if 'bcorr' in functions and not has_bc:
                        _log_once((family, 'nobcorr'),
                                  f"[scatter] {family}: no BIAS_CORR column "
                                  f"in the data, bcorr maps skipped "
                                  f"(radiance families only)")

                    for comp in comparisons:
                        files = [db_of[n] for n in comp.names]
                        for function in functions:
                            if function == 'bcorr' and not has_bc:
                                continue
                            panels = [PANEL_VALUE]
                            if (len(comp.names) == 2
                                    and function in _TESTED_FUNCS):
                                panels += [PANEL_CONF, PANEL_SIGONLY]
                            for proj in projections:
                                for panel in panels:
                                    for sel, sp_val, vc, vn in selections:
                                        tasks.append({
                                            'family':        family,
                                            'region':        region,
                                            'land_ocean':    land_ocean,
                                            'flag_criteria': fc,
                                            'interval':      interval,
                                            'vcotyp':        _vcotyp(family),
                                            'function':      function,
                                            'proj':          proj,
                                            'selector':      sel,
                                            'special_val':   sp_val,
                                            'vcoord':        vc,
                                            'varno':         vn,
                                            'comparison':    comp,
                                            'files_in':      files,
                                            'pair_db':       (
                                                _pair_db_path(
                                                    work_path, family, layer,
                                                    comp.names[0],
                                                    comp.names[1], region,
                                                    date_start, date_end,
                                                    box_size_x, box_size_y,
                                                    fc, land_ocean)
                                                if len(comp.names) == 2
                                                else None),
                                            'panel':         panel,
                                        })
    return tasks


# ─────────────────────────────────────────────────────────────────────────────
# Orchestrator
# ─────────────────────────────────────────────────────────────────────────────

def _silence_distributed_loggers() -> None:
    for name in (
        "distributed", "distributed.client", "distributed.scheduler",
        "distributed.worker", "distributed.nanny",
        "distributed.core", "distributed.comm",
        "distributed.utils", "distributed.utils_perf",
        "tornado", "tornado.application", "asyncio",
    ):
        logging.getLogger(name).setLevel(logging.CRITICAL)


def _is_number(text: str) -> bool:
    try:
        float(text)
        return True
    except (TypeError, ValueError):
        return False


def _report_pairing(tasks: List[Dict[str, Any]],
                    results: List[Optional[Dict[str, int]]],
                    elapsed: float) -> None:
    """Print, per family and experiment, how many observations matched."""
    summary: Dict[Tuple[str, str], Dict[str, int]] = {}
    failed = 0
    for t, r in zip(tasks, results):
        if r is None:
            failed += 1
            continue
        key = (t['family'], t.get('exp_name', os.path.dirname(t['exp_file'])))
        acc = summary.setdefault(key, {})
        for k, v in r.items():
            acc[k] = acc.get(k, 0) + int(v or 0)
    print(f"[scatter] matching time: {elapsed:.1f}s "
          f"({len(tasks) - failed}/{len(tasks)} tasks)")
    for (family, exp_name), acc in summary.items():
        ctl, exp, pairs = acc.get('obs_c', 0), acc.get('obs_e', 0), acc.get('pairs', 0)
        pct_c = pairs / ctl * 100.0 if ctl else 0.0
        pct_e = pairs / exp * 100.0 if exp else 0.0
        print(f"[scatter]   {family} {exp_name}: "
              f"{pairs} common obs ({pct_c:.1f}% of control, "
              f"{pct_e:.1f}% of experience)")
        # the pairing key was not unique somewhere: say so once
        from pikobs.match import DEFAULT_KEY, MatchSpec, repeat_warning
        t0 = next((t for t in tasks if t['family'] == family), {})
        spec = MatchSpec(True, tuple(t0.get('match_fields') or DEFAULT_KEY))
        msg = repeat_warning(
            'scatter', f"{family} ({exp_name})", spec,
            {'control': (acc.get('rep_keys_c', 0), acc.get('rep_rows_c', 0)),
             exp_name: (acc.get('rep_keys_e', 0), acc.get('rep_rows_e', 0))})
        if msg:
            print(msg, file=sys.stderr, flush=True)
        if pairs == 0 and (ctl or exp):
            print(f"[scatter]   WARNING {family}: no common observation, "
                  f"the tested maps will be empty", file=sys.stderr)


def _report_timing(timing: Dict[str, Any], pathwork: str) -> None:
    """Print the time spent in each phase and save it as JSON."""
    sec = timing['seconds']
    print("[scatter] ------------------- run time -------------------")
    print(f"[scatter] input        {_fmt_bytes(timing['input_bytes']):>10s}"
          f"   {timing['input_files']} files, {timing['cycles']} cycles, "
          f"{timing['runs']} run(s)")
    for phase in ('aggregation', 'matching', 'compaction', 'plots'):
        if phase in sec:
            extra = (f"   {timing.get('maps', 0)} maps"
                     if phase == 'plots' else "")
            print(f"[scatter] {phase:<12s} {sec[phase]:>8.1f} s{extra}")
    print(f"[scatter] total        {sec['total']:>8.1f} s"
          f"   ({sec['total'] / 60:.1f} min, {timing['n_cpus']} workers)")
    try:
        with open(os.path.join(pathwork, "scatter_timing.json"), "w") as fh:
            json.dump(timing, fh, indent=1)
    except OSError as exc:
        print(f"[scatter] could not write scatter_timing.json: {exc}",
              file=sys.stderr)


def _run(func, arg_tuples: List[tuple], client, label=None) -> List[Any]:
    """Thin wrapper over the shared runner (progress + fault tolerance)."""
    return run_tasks(func, arg_tuples, client, label=label)


def make_scatter(experiments:       Sequence[Tuple[str, str]],
                 control:           Optional[Tuple[str, str]],
                 pathwork:          str,
                 datestart:         str,
                 dateend:           str,
                 regions:           List[str],
                 families:          List[str],
                 flag_criteria:     List[str],
                 fonctions:         List[str],
                 varnos:            List[str],
                 boxsizex:          float,
                 boxsizey:          float,
                 projs:             List[str],
                 Points:            str = 'OFF',
                 id_stn:            Any = 'join',
                 channel:           Any = 'join',
                 n_cpu:             int = 1,
                 special_column_on: bool = False,
                 svg:                bool = False,
                 pressure_layers:   Sequence[float] = (),
                 height_layers:     Sequence[float] = (),
                 match:             bool = True,
                 land_ocean:        Any = ('all',)) -> int:
    """Run aggregation, plotting and viewer generation.

    experiments: [(name, rdb_dir), ...] -- at least one
    control:     (name, rdb_dir) or None
    """
    # MATCH: on, off, or the fields of the key -- pikobs.match decides.
    # Past this point match is True / False as before; the key travels
    # in match_spec.
    from pikobs.match import parse_match
    if match is True or match is False:
        match = 'on' if match else 'off'
    match_spec = parse_match(match)
    match = match_spec.enabled
    from pikobs.scatter.scatter_plot import (
        _build_viewer_items,
        _render_tile_map,
        _write_viewer)
    if not experiments:
        raise ValueError("at least one experiment is required")

    runs        = ([control] if control else []) + list(experiments)
    run_names   = [n for n, _ in runs]
    stn_tokens  = parse_station_tokens(id_stn)
    chan_tokens = parse_channel_tokens(channel)
    comparisons = build_comparisons(control, experiments)
    land_oceans = _split_tokens(land_ocean) or ['all']
    bad = [s for s in land_oceans if s not in ('all', 'land', 'ocean')]
    if bad:
        raise ValueError(f"LAND_OCEAN takes all, land and ocean, not {bad}")

    print(f"[scatter] runs: {', '.join(run_names)}")
    if control is not None:
        print("[scatter] " + (
            "matched observation by observation"
            if match else
            "compared, NOT matched: each run with all its observations, "
            "Welch and F tests"))
    print(f"[scatter] comparisons: {', '.join(c.label for c in comparisons)}")
    print(f"[scatter] id_stn tokens: {stn_tokens}")
    print(f"[scatter] channel tokens: {chan_tokens}")
    print(f"[scatter] land_ocean: {land_oceans}")
    for family in families:
        layers = family_layers(family, pressure_layers, height_layers)
        if len(layers) > 1:
            print(f"[scatter] {family}: "
                  + ", ".join(_layer_display(i, _vcotyp(family))
                              for i in layers[1:]))
        else:
            print(f"[scatter] {family}: the whole column in one series")

    if not _check_inputs(runs, families, datestart, dateend,
                         'scatter'):
        return 1

    t_start = time.time()
    cycles  = _cycles(datestart, dateend)
    n_input, input_bytes = _input_size(runs, families, cycles)
    timing: Dict[str, Any] = {
        'datestart': datestart, 'dateend': dateend,
        'cycles': len(cycles), 'families': list(families),
        'runs': len(runs), 'comparison': control is not None,
        'flags': list(flag_criteria), 'regions': list(regions),
        'functions': list(fonctions), 'projections': list(projs),
        'boxsize': [boxsizex, boxsizey], 'id_stn': list(stn_tokens),
        'channel': list(chan_tokens), 'n_cpus': n_cpu, 'svg': svg,
        'land_ocean': land_oceans,
        'input_files': n_input, 'input_bytes': input_bytes,
        'seconds': {},
    }

    for family in families:
        pikobs.delete_create_folder(pathwork, family)

    agg_tasks = create_data_list(
        datestart, dateend, families, runs, pathwork,
        boxsizex, boxsizey, flag_criteria, regions, varnos,
        keep_station=_needs_station_detail(stn_tokens),
        keep_vcoord=_needs_vcoord_detail(chan_tokens),
        special_column_on=special_column_on,
        pressure_layers=pressure_layers, height_layers=height_layers,
        land_oceans=land_oceans,
    )
    # the same channel rule as the matching below: explicit numbers
    # are the channels to keep; join or all keep every channel
    agg_channels = ([float(t) for t in chan_tokens]
                    if all(_is_number(t) for t in chan_tokens) else [])
    for _t in agg_tasks:
        _t['channels'] = agg_channels

    common = dict(datestart=datestart, dateend=dateend,
                  boxsizex=boxsizex, boxsizey=boxsizey,
                  pathwork=pathwork, Points=Points)

    parallel = n_cpu > 1
    client   = None
    dask_dir = None
    if parallel:
        _silence_distributed_loggers()
        # Worker processes start with dask's default logging: the
        # environment is inherited, so set the level there too.
        os.environ["DASK_LOGGING__DISTRIBUTED"] = "error"
        # Private scratch space, removed at the end: no stale worker
        # directories left for the next run to purge.
        base = os.environ.get("TMPDIR") or None
        dask_dir = tempfile.mkdtemp(prefix="pikobs_scatter_dask_", dir=base)
        os.environ["DASK_TEMPORARY_DIRECTORY"] = dask_dir
        dask.config.set({"temporary-directory": dask_dir,
                         "logging.distributed": "error"})
        client = Client(processes=True, threads_per_worker=1,
                        n_workers=n_cpu, silence_logs=logging.ERROR,
                        dashboard_address=None)
    try:
        # Phase 1: aggregation
        t0 = time.time()
        print(f"[scatter] aggregation: {len(agg_tasks)} tasks, "
              f"{n_cpu} worker(s)")
        agg_res = _run(_aggregate_task, [(t,) for t in agg_tasks], client,
                       label='aggregation')
        n_ok = sum(r is not None for r in agg_res)
        timing['seconds']['aggregation'] = time.time() - t0
        print(f"[scatter] aggregation time: {time.time() - t0:.1f}s "
              f"({n_ok}/{len(agg_tasks)} files aggregated)")

        # Phase 1b: control / experience matching for the tested functions
        if (control is not None and match
                and any(f in _PAIR_Q for f in fonctions)):
            chan_values: List[float] = []
            if all(_is_number(t) for t in chan_tokens):
                chan_values = [float(t) for t in chan_tokens]
            pair_tasks = create_pair_list(
                datestart, dateend, families, control, experiments,
                pathwork, boxsizex, boxsizey, flag_criteria, regions,
                varnos,
                keep_station=_needs_station_detail(stn_tokens),
                keep_vcoord=_needs_vcoord_detail(chan_tokens),
                channels=chan_values,
                special_column_on=special_column_on,
                pressure_layers=pressure_layers,
                height_layers=height_layers,
                land_oceans=land_oceans,
            )
            t0 = time.time()
            for t in pair_tasks:
                t['match_fields'] = match_spec.fields
            print(f"[scatter] matching control and experience: "
                  f"{len(pair_tasks)} tasks")
            pair_res = _run(_pair_task, [(t,) for t in pair_tasks], client,
                            label='matching')
            timing['seconds']['matching'] = time.time() - t0
            _report_pairing(pair_tasks, pair_res, time.time() - t0)

        # Phase 1c: one row per box / station / channel over the period
        compact_jobs = []
        for family in families:
            fam_dir = os.path.join(pathwork, family)
            tmp_dir = os.path.join(fam_dir, ".sqlite_tmp")
            for name in sorted(os.listdir(fam_dir)):
                if not name.endswith(".db"):
                    continue
                table = 'pairs' if name.startswith("scatter_pair_") else 'moyenne'
                compact_jobs.append((os.path.join(fam_dir, name), table, tmp_dir))
        t0 = time.time()
        comp_res = _run(_compact_task, compact_jobs, client,
                        label='compaction')
        timing['seconds']['compaction'] = time.time() - t0
        print(f"[scatter] compaction time: {time.time() - t0:.1f}s "
              f"({sum(r is not None for r in comp_res)}/{len(compact_jobs)} "
              f"databases)")
        for family in families:
            shutil.rmtree(os.path.join(pathwork, family, ".sqlite_tmp"),
                          ignore_errors=True)

        # Phase 2: plots
        plot_tasks = create_data_list_plot(
            datestart, dateend, families, run_names, comparisons, pathwork,
            boxsizex, boxsizey, fonctions, flag_criteria, regions,
            stn_tokens, chan_tokens, projs,
            special_column_on=special_column_on,
            pressure_layers=pressure_layers, height_layers=height_layers,
        land_oceans=land_oceans)
        t0 = time.time()
        # the drawing runs in a fresh cluster held to the job's memory: the
        # extraction workers hold memory they do not give back, drawing in
        # long-lived processes keeps adding to it, and Dask, sized from the
        # node's physical memory, never held any of them back -- 80 of them
        # reached the job's limit about four maps in five.
        t0 = time.time()
        try:
            from pikobs.parallel.parallel import drawing_client
            client, n_draw = drawing_client(client, n_cpu)
            print(f"[scatter] drawing cluster: {n_draw} worker(s), held to "
                  f"the job's memory ({time.time() - t0:.1f}s)", flush=True)
        except Exception as exc:
            print(f"[scatter] could not start the drawing cluster ({exc}); "
                  f"drawing with the extraction workers", flush=True)
        print(f"[scatter] plots: {len(plot_tasks)} tasks, {n_cpu} worker(s)")
        for t in plot_tasks:
            t['svg'] = svg
        plot_res = _run(_render_tile_map,
                        [(t, common) for t in plot_tasks], client,
                        label='plots')
        n_ok = sum(r is not None for r in plot_res)
        timing['seconds']['plots'] = time.time() - t0
        timing['maps'] = sum(r is not None for r in plot_res)
        print(f"[scatter] plot time: {time.time() - t0:.1f}s "
              f"({n_ok}/{len(plot_tasks)} maps written)")
        for panel in (PANEL_VALUE, PANEL_CONF, PANEL_SIGONLY):
            n_task = sum(t.get('panel') == panel for t in plot_tasks)
            n_done = sum(r is not None for t, r in zip(plot_tasks, plot_res)
                         if t.get('panel') == panel)
            if n_task:
                label = panel if control is not None else 'single-run'
                print(f"[scatter]   {label:<16s} maps: {n_done}/{n_task}")
        if control is not None:
            tested = [f for f in fonctions if f in _TESTED_FUNCS]
            n_conf = sum(t.get('panel') == PANEL_CONF for t in plot_tasks)
            if not tested:
                print(f"[scatter] note: no significance maps, FONCTION has "
                      f"none of {list(_TESTED_FUNCS)}")
            elif n_conf and not any(
                    r for t, r in zip(plot_tasks, plot_res)
                    if t.get('panel') == PANEL_CONF):
                print("[scatter] WARNING: every significance map failed, "
                      "see the tracebacks above", file=sys.stderr)
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

    # Phase 3: HTML viewer
    items = _build_viewer_items(plot_tasks, plot_res)
    if not items:
        print("[scatter] ERROR: no map was produced, viewer not written.",
              file=sys.stderr)
        return 1
    _write_viewer(items, pathwork, is_diff=control is not None,
                  common=common)
    timing['seconds']['total'] = time.time() - t_start
    _report_timing(timing, pathwork)
    print(f"[scatter] done -- output in: {pathwork}")
    return 0


# ─────────────────────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────────────────────

_UNSET = ('', 'undefined', None)


def _resolve_runs(args) -> Tuple[List[Tuple[str, str]],
                                 Optional[Tuple[str, str]]]:
    paths = _split_tokens(args.path_experience_files)
    names = _split_tokens(args.experience_name)
    paths = [p for p in paths if p not in _UNSET]
    names = [n for n in names if n not in _UNSET]

    if not paths:
        raise ValueError("--path_experience_files is required")
    if not names:
        raise ValueError("--experience_name is required")
    if len(paths) != len(names):
        raise ValueError(f"--path_experience_files ({len(paths)}) and "
                         f"--experience_name ({len(names)}) must have the "
                         "same number of entries")
    paths = [p.rstrip('/') or '/' for p in paths]
    experiments = list(zip(names, paths))

    control = None
    if args.path_control_files not in _UNSET:
        if args.control_name in _UNSET:
            raise ValueError("--control_name is required with "
                             "--path_control_files")
        control = (args.control_name,
                   args.path_control_files.rstrip('/') or '/')

    all_names = [n for n, _ in ([control] if control else []) + experiments]
    safe = [_safe_filename(n) for n in all_names]
    if len(set(safe)) != len(safe):
        raise ValueError(f"run names must be unique: {all_names}")
    return experiments, control


def arg_call() -> None:
    p = argparse.ArgumentParser(
        prog="pikobs-scatter",
        description="Geographic tiled statistics with control vs "
                    "multi-experiment comparison.",
    )
    p.add_argument('--path_control_files', default='',
                   help="RDB directory of the control run (optional).")
    p.add_argument('--control_name', default='')
    p.add_argument('--path_experience_files', nargs='+', default=[],
                   help="One or more RDB directories (exp1 exp2 ...).")
    p.add_argument('--experience_name', nargs='+', default=[],
                   help="One label per experiment, same order.")
    p.add_argument('--pathwork',  default=None)
    p.add_argument('--datestart', default=None)
    p.add_argument('--dateend',   default=None)
    p.add_argument('--region',         nargs='+', default=None)
    p.add_argument('--family',         nargs='+', default=None)
    p.add_argument('--flags_criteria', nargs='+', default=None)
    p.add_argument('--fonction',       nargs='+', default=None)
    p.add_argument('--varnos',         nargs='+', default=[])
    p.add_argument('--boxsizex', type=_num, default=None)
    p.add_argument('--boxsizey', type=_num, default=None)
    p.add_argument('--projection', nargs='+', default=['cyl'],
                   help="cyl, OrthoN, OrthoS, robinson, Europe, Canada, "
                        "AmeriqueNord, Npolar, Spolar, reg.")
    p.add_argument('--mode',   default='SIGMA', help="Kept for compatibility.")
    p.add_argument('--Points', default='OFF')
    p.add_argument('--id_stn', nargs='+', default=['join'],
                   help="Tokens, one map series each: join, all, PREFIX, "
                        "LIKE%%pattern, =EXACT, 'NAME (codtyp)'.")
    p.add_argument('--channel', '--vcoord', nargs='+', dest='channel',
                   default=['join'],
                   help="Tokens: join, all, or explicit channel/level values.")
    p.add_argument('--match', nargs='+', default=['on'],
                   help="on: with a control, the same observations in both "
                        "runs, paired tests. off: each run with all its "
                        "observations and its own flags, Welch and F tests.")
    p.add_argument('--svg', default='off', choices=['on', 'off'],
                   help="Also write each map as SVG, next to the PNG, for "
                        "editing before a presentation (default off). A map "
                        "with small boxes gives a very large SVG.")
    p.add_argument('--n_cpus', type=int, default=1)
    p.add_argument('--land_ocean', nargs='+', default=['all'],
                   choices=['all', 'land', 'ocean'],
                   help="all (no filter), land, ocean: one series of maps "
                        "each; land and ocean read the land mask.")
    p.add_argument('--special_column', default='off', choices=['on', 'off'],
                   help="on: one series of maps per value of the family's special "
                        "column (sw: the method; ra: the elevation). "
                        "off: all together (default).")
    p.add_argument('--pressure_layers', nargs='*', type=float,
                   default=[],
                   help="Layer edges in hPa, from the ground up, for the "
                        "families whose vertical coordinate is a pressure "
                        "(ua ai sw ch): 1100 850 500 250 100 10 1 0. Empty "
                        "means the whole column in one series of maps.")
    p.add_argument('--height_layers', nargs='*', type=float, default=[],
                   help="Layer edges in km for the families on height "
                        "(ro radar): 0 5 10 20 30 40 60 100. Empty means "
                        "the whole column.")
    p.add_argument('--walltime', default='02:00:00',
                   help="PBS walltime HH:MM:SS.")
    p.add_argument('--no_submit', action='store_true',
                   help="Skip PBS auto-submission and run locally.")

    args = p.parse_args()
    # blank control values are no control: an empty variable in the
    # wrapper must not become a directory called ' '
    for _attr in ('path_control_files', 'control_name'):
        _val = getattr(args, _attr, None)
        if isinstance(_val, str) and not _val.strip():
            setattr(args, _attr, None)

    for attr in ('region', 'family', 'flags_criteria', 'fonction',
                 'projection', 'varnos'):
        val = getattr(args, attr)
        if isinstance(val, list):
            setattr(args, attr, _split_tokens(val))

    for arg in vars(args):
        print(f'--{arg} {getattr(args, arg)}')

    for attr, flag in [
        ('pathwork',       '--pathwork'),
        ('datestart',      '--datestart'),
        ('dateend',        '--dateend'),
        ('region',         '--region'),
        ('family',         '--family'),
        ('flags_criteria', '--flags_criteria'),
        ('fonction',       '--fonction'),
        ('boxsizex',       '--boxsizex'),
        ('boxsizey',       '--boxsizey'),
    ]:
        if getattr(args, attr) in (None, [], 'undefined', ''):
            raise ValueError(f"{flag} is required")

    experiments, control = _resolve_runs(args)

    maybe_submit_to_pbs(args)

    sys.exit(make_scatter(
        experiments, control, args.pathwork,
        args.datestart, args.dateend,
        args.region, args.family, args.flags_criteria,
        args.fonction, args.varnos,
        args.boxsizex, args.boxsizey, args.projection,
        Points=args.Points,
        id_stn=args.id_stn,
        channel=args.channel,
        n_cpu=args.n_cpus,
        special_column_on=(args.special_column == 'on'),
        svg=svg_enabled(args.svg),
        pressure_layers=args.pressure_layers,
        height_layers=args.height_layers,
        match=args.match,
        land_ocean=args.land_ocean,
    ))


if __name__ == "__main__":
    arg_call()
