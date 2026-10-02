#!/usr/bin/python3
# GENERATED -- this docstring is written by pikobs/build_doc/build_verifprofile.py.
# Edit that file and run ./pikobs_doc.sh; a change made here is lost.
r"""============================================================
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

+----------------+-----------------------------------------------------------------------------------------+
| Panel          | What it shows                                                                           |
+================+=========================================================================================+
| Mean           | the mean departure of each run: control black with squares, experience red with circles |
+----------------+-----------------------------------------------------------------------------------------+
| Bias change    | abs(mean_exp) - abs(mean_ctl) at its own scale, with the paired t-test dots             |
+----------------+-----------------------------------------------------------------------------------------+
| Relative sigma | 100 x (sigma_exp - sigma_ctl) / sigma_ctl, with the sigma-test dots                     |
+----------------+-----------------------------------------------------------------------------------------+
| Observations   | matched observations per level, as bars                                                 |
+----------------+-----------------------------------------------------------------------------------------+

.. image:: _static/verifprofile_comparison.png
   :alt: Four panels of a comparison, MLS ozone
   :align: center
   :width: 100%

The mean panel is context. The two curves usually lie on top of each
other, and the change the tests are about is a hundred times smaller than
the values themselves: that is what the bias-change panel shows, at its own
scale, with the background tinted red on the side where the experience
comes closer to zero and blue on the other.

Each level of the two change panels carries a mark on its left edge:

+------------+------------------------------------------------------------------+
| Mark       | Meaning                                                          |
+============+==================================================================+
| red dot    | the experience is better at that level, and the test passes 95 % |
+------------+------------------------------------------------------------------+
| blue dot   | the control is better, and the test passes 95 %                  |
+------------+------------------------------------------------------------------+
| hollow dot | the change is not larger than noise                              |
+------------+------------------------------------------------------------------+
| grey cross | the level cannot be tested: the control has no sigma there       |
+------------+------------------------------------------------------------------+

Without a control, three panels give the profile of the run itself:

+--------------+-------------------------------+
| Panel        | What it shows                 |
+==============+===============================+
| Mean         | the mean departure of the run |
+--------------+-------------------------------+
| Sigma        | sigma of the departure        |
+--------------+-------------------------------+
| Observations | observations per level        |
+--------------+-------------------------------+

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

.. image:: _static/verifprofile_scorecard.png
   :alt: The O-P scorecard of an experiment, by layers of height
   :align: center
   :width: 100%

The layers are the same for every family, in km: 0-2, 2-5, 5-10, 10-15,
15-20, 20-30, 30-40 and 40-60. A level given in pressure is placed with a
standard atmosphere, z = -7 km x ln(p / 1013.25 hPa), and each column gives
both.

A cell adds up every matched observation of its layer: the counts, the
sums, the sums of squares and of products of all its levels, as if the
layer were a single level. That gives the mean and the sigma of each run,
and the two numbers of the table:

+-------+-------------------------------------------------------------------------------------+
| Table | In each cell                                                                        |
+=======+=====================================================================================+
| sigma | 100 x (sigma Exp - sigma Ctl) / sigma Ctl, in %                                     |
+-------+-------------------------------------------------------------------------------------+
| bias  | 100 x (abs(mean Exp) - abs(mean Ctl)) / sigma Ctl, in % of the sigma of the control |
+-------+-------------------------------------------------------------------------------------+

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

+---------------------------+---------------------------------------------------------------------+
| Token                     | Profiles produced                                                   |
+===========================+=====================================================================+
| ``join``                  | one, every station together                                         |
+---------------------------+---------------------------------------------------------------------+
| ``all``                   | one per station; on ai, sf, ua, gp and csr one per instrument type  |
+---------------------------+---------------------------------------------------------------------+
| ``C%``                    | the stations whose id starts with C, together; the title lists them |
+---------------------------+---------------------------------------------------------------------+
| ``pilot``, ``AMDAR (42)`` | on a composite family, that instrument type                         |
+---------------------------+---------------------------------------------------------------------+
| ``=COSMIC2-E1``           | that station only                                                   |
+---------------------------+---------------------------------------------------------------------+

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

import json
import os
import shutil
import sys
import tempfile
import time
from typing import Any, Dict, List, Optional, Sequence, Tuple

import dask
from dask.distributed import Client

import pikobs
from pikobs.figures import svg_enabled
from pikobs.obsdb import (check_input_files, cycle_path, cycles as _cycles,
                          fmt_bytes, input_size)
from pikobs.parallel import run_tasks
from pikobs.pbs_submit import maybe_submit_to_pbs
from pikobs.stations.stations import parse_station_tokens
from pikobs.verifprofile.verifprofile_plot import (MIN_OBS_PER_LEVEL,
                                                   verifprofile_overlay_task,
                                                   verifprofile_plot_task,
                                                   verifprofile_scale_task)
from pikobs.web.viewer import generate_web
from pikobs.web.runs import runs_block
from pikobs.zone.zone import (RO_FAMILIES, _distinct, _extract_task,
                              _index_task, _is_composite, _safe, _selections,
                              _special_label, _split_tokens)
from pikobs.zone.zone_plot import LAND_OCEAN_CHOICES

# The profile has no latitude axis: one band per hemisphere is enough,
# and the bands are summed away when the profile is read.
PROFILE_BAND = 180.0


def db_path(work_path: str, family: str, tag: str, date_start: str,
            date_end: str) -> str:
    return os.path.join(work_path, family,
                        f"verifprofile_{_safe(tag)}_{date_start}_{date_end}_"
                        f"{family}.db")


def _plot_tasks(work_path, family, tag, date_start, date_end, functions,
                matched: bool, names, svg: bool, min_obs: int,
                label: str) -> List[Dict[str, Any]]:
    table = 'zone_pairs' if matched else 'zone'
    path = db_path(work_path, family, tag, date_start, date_end)
    rows = _distinct(path, table,
                     f"SELECT DISTINCT region, flag, land_ocean, id_stn, "
                     f"special, varno FROM {table} "
                     f"WHERE channel_mode = 'all';")
    word = "type" if _is_composite(family) else "station"
    tasks = []
    for region, flag, lo, id_stn, special, varno in rows:
        for function in functions:
            tasks.append({
                'pathwork': work_path, 'db_file': path, 'family': family,
                'region': region, 'flag': flag, 'land_ocean': lo,
                'id_stn': id_stn, 'stn_tag': _safe(id_stn),
                'special': special if special is not None else 'all',
                'special_label': _special_label(family, special),
                'member_word': word, 'varno': varno, 'function': function,
                'datestart': date_start, 'dateend': date_end,
                'names': list(names), 'matched': matched, 'svg': svg,
                'min_obs': min_obs, 'experience': label,
                'gpsro': family in RO_FAMILIES,
            })
    return tasks


def _scale_group(task) -> tuple:
    return (task['family'], str(task['varno']), task['function'],
            bool(task['matched']))


def _report_timing(timing: Dict[str, Any], pathwork: str) -> None:
    sec = timing['seconds']
    p = "[verifprofile]"
    print(f"{p} -------------------- run time --------------------",
          flush=True)
    print(f"{p} input        {fmt_bytes(timing['input_bytes']):>10s}   "
          f"{timing['input_files']} files, {timing['cycles']} cycles, "
          f"{timing['runs']} run(s)", flush=True)
    for phase in ('extraction', 'scales', 'plots', 'ratio figures'):
        if phase in sec:
            print(f"{p} {phase:<12s} {sec[phase]:>8.1f} s", flush=True)
    print(f"{p} total        {sec['total']:>8.1f} s   "
          f"({sec['total'] / 60:.1f} min, {timing['n_cpus']} workers)",
          flush=True)
    try:
        with open(os.path.join(pathwork, "verifprofile_timing.json"),
                  "w") as fh:
            json.dump(timing, fh, indent=1)
    except OSError as exc:
        print(f"{p} could not write verifprofile_timing.json: {exc}",
              file=sys.stderr, flush=True)


def make_verifprofile(runs, pathwork, datestart, dateend, regions, families,
                      flags_criteria, functions, varnos, id_stn, land_ocean,
                      n_cpu, control=None, svg: bool = False,
                      min_obs: int = MIN_OBS_PER_LEVEL,
                      special_on: bool = True,
                      ratio_figure: bool = False,
                 match: bool = True) -> int:
    """Read the cycles, match them, draw one profile per selection."""
    # MATCH: on, off, or the fields of the key -- pikobs.match decides.
    # Past this point match is True / False as before; the key travels
    # in match_spec.
    from pikobs.match import parse_match
    if match is True or match is False:
        match = 'on' if match else 'off'
    match_spec = parse_match(match)
    match = match_spec.enabled
    p = "[verifprofile]"
    regions = _split_tokens(regions)
    flags = _split_tokens(flags_criteria)
    functions = _split_tokens(functions) or ['omp']
    land_oceans = [lo for lo in (_split_tokens(land_ocean) or ['all'])
                   if lo in LAND_OCEAN_CHOICES] or ['all']
    stn_tokens = parse_station_tokens(id_stn)
    varnos = _split_tokens(varnos)
    # with the option off the task never gets a control file, so the
    # extraction takes its unmatched branch and nothing else changes
    matched = control is not None and match
    all_runs = ([control] if control else []) + list(runs)

    print(f"{p} runs: {', '.join(n for n, _ in all_runs)}", flush=True)
    if matched:
        print(f"{p} control: {control[0]}  |  matched observation by "
              f"observation with: {', '.join(n for n, _ in runs)}",
              flush=True)
    print(f"{p} regions: {regions}", flush=True)
    print(f"{p} flags_criteria: {flags}", flush=True)
    print(f"{p} fonction: {functions}", flush=True)
    print(f"{p} id_stn tokens: {stn_tokens}", flush=True)
    print(f"{p} levels with fewer than {min_obs} observations are dropped",
          flush=True)
    for fam in families:
        _, vcoord, _, _, _, vcotyp = pikobs.family(fam)
        extra = ("  -- normalised by B_ref = 300 exp(-h/6500), with the "
                 "GPS-RO quality gates" if fam in RO_FAMILIES else "")
        print(f"{p} {fam}: vcoord = {vcoord.strip()}  ({vcotyp}){extra}",
              flush=True)

    if not check_input_files(all_runs, families, datestart, dateend,
                             'verifprofile'):
        return 1

    t_start = time.time()
    cycle_list = _cycles(datestart, dateend)
    n_input, input_bytes = input_size(all_runs, families, cycle_list)
    timing: Dict[str, Any] = {
        'datestart': datestart, 'dateend': dateend, 'cycles': len(cycle_list),
        'families': list(families), 'runs': len(all_runs),
        'regions': regions, 'flags': flags, 'fonction': functions,
        'id_stn': stn_tokens, 'land_ocean': land_oceans, 'matched': matched,
        'min_obs': min_obs, 'special_column': special_on, 'svg': svg,
        'n_cpus': n_cpu, 'input_files': n_input, 'input_bytes': input_bytes,
        'seconds': {},
    }
    for family in families:
        pikobs.delete_create_folder(pathwork, family)

    comparisons = [
        {'label': f"{name} vs {control[0]}" if matched else name,
         'tag': f"{control[0]}_vs_{name}" if matched else name,
         'names': [control[0], name] if matched else [name], 'path': path}
        for name, path in runs]
    selectors = {f: _selections(stn_tokens, f) for f in families}

    tasks = []
    for comp in comparisons:
        for cycle in cycle_list:
            for family in families:
                for sel in selectors[family]:
                    task = {
                        'family': family,
                        'db_new': db_path(pathwork, family,
                                          f"{comp['tag']}_{sel.tag}",
                                          datestart, dateend),
                        'regions': regions, 'flags': flags,
                        'channels': ['all'], 'land_oceans': land_oceans,
                        'id_stn_sql': sel.sql(), 'stn_label': sel.label,
                        'special_on': special_on, 'varnos': varnos,
                        'box_y': PROFILE_BAND, 'pathwork': pathwork,
                        # GPS-RO is normalised by its reference profile and
                        # passes the operational quality gates
                        'gpsro': family in RO_FAMILIES,
                    }
                    if matched:
                        task['ctl_file'] = cycle_path(control[1], cycle,
                                                      family)
                        task['match_fields'] = match_spec.fields
                        task['names'] = (control[0], 'experience')
                        task['exp_file'] = cycle_path(comp['path'], cycle,
                                                      family)
                    else:
                        task['filein'] = cycle_path(comp['path'], cycle,
                                                    family)
                    tasks.append(task)

    client, dask_dir = None, None
    if n_cpu > 1:
        os.environ["DASK_LOGGING__DISTRIBUTED"] = "error"
        dask_dir = tempfile.mkdtemp(prefix="pikobs_verifprofile_dask_",
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
        t0 = time.time()
        print(f"{p} extraction: {len(tasks)} tasks, {n_cpu} worker(s)",
              flush=True)
        res = run_tasks(_extract_task, [(t,) for t in tasks], client,
                        label='extraction')
        timing['seconds']['extraction'] = time.time() - t0
        print(f"{p} extraction time: {timing['seconds']['extraction']:.1f}s "
              f"({sum(r is not None for r in res)}/{len(tasks)} files)",
              flush=True)
        # one line per family when the pairing key was not unique
        from pikobs.match import add_counts, repeat_warning
        repeats = {}
        for t, r in zip(tasks, res):
            if isinstance(r, dict):
                add_counts(repeats.setdefault(t['family'], {}),
                           r.get('repeats'))
        for fam in sorted(repeats):
            msg = repeat_warning('verifprofile', fam, match_spec,
                                 repeats[fam])
            if msg:
                print(msg, file=sys.stderr, flush=True)
        dbs = sorted({t['db_new'] for t in tasks})
        run_tasks(_index_task, [(d,) for d in dbs], client, label='indexing')

        for comp in comparisons:
            for family in families:
                for sel in selectors[family]:
                    plot_tasks += _plot_tasks(
                        pathwork, family, f"{comp['tag']}_{sel.tag}",
                        datestart, dateend, functions, matched,
                        comp['names'], svg, min_obs, comp['label'])
        if not plot_tasks:
            print(f"{p} WARNING: nothing to plot, check the selectors.",
                  file=sys.stderr, flush=True)
            return 1

        # the x axes of a group are shared, as the colours are in zone:
        # the same family, varno and function read on the same scale
        t0 = time.time()
        extremes = run_tasks(verifprofile_scale_task,
                             [(t,) for t in plot_tasks], client,
                             label='scales')
        groups: Dict[tuple, Dict[str, float]] = {}
        for task, ext in zip(plot_tasks, extremes):
            if not ext:
                continue
            g = groups.setdefault(_scale_group(task), {})
            for key, value in ext.items():
                g[key] = max(g.get(key, 0.0), float(value))
        for task in plot_tasks:
            task['scales'] = groups.get(_scale_group(task), {})
        timing['seconds']['scales'] = time.time() - t0

        t0 = time.time()
        print(f"{p} plots: {len(plot_tasks)} tasks", flush=True)
        results = run_tasks(verifprofile_plot_task,
                            [(t,) for t in plot_tasks], client,
                            label='plots')
        timing['seconds']['plots'] = time.time() - t0
        print(f"{p} plot time: {timing['seconds']['plots']:.1f}s "
              f"({sum(r is not None for r in results)}/{len(plot_tasks)})",
              flush=True)

        # with a control and at least two experiences, one more figure per
        # selection: the sigma ratio of every experience against it, on
        # the same axes. With a single experience it would only repeat the
        # middle panel of its own figure
        if matched and ratio_figure and len(runs) > 1:
            overlays: Dict[tuple, Dict[str, Any]] = {}
            for t in plot_tasks:
                key = (t['family'], t['region'], t['flag'], t['land_ocean'],
                       t['id_stn'], str(t['special']), str(t['varno']),
                       t['function'])
                o = overlays.setdefault(key, dict(
                    t, control=control[0], members=[],
                    experience=f"all vs {control[0]}"))
                o['members'].append({'name': t['names'][1],
                                     'db_file': t['db_file']})
            overlay_tasks = list(overlays.values())
            t0 = time.time()
            overlay_results = run_tasks(verifprofile_overlay_task,
                                        [(t,) for t in overlay_tasks],
                                        client, label='ratio figures')
            timing['seconds']['ratio figures'] = time.time() - t0
            print(f"{p} ratio figures: "
                  f"{sum(r is not None for r in overlay_results)}/"
                  f"{len(overlay_tasks)}", flush=True)
            plot_tasks += overlay_tasks
            results = list(results) + list(overlay_results)
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

    # the scorecard: every family, variable and region of a comparison, by
    # layers of height -- where the experience is better, where it is worse
    if matched:
        try:
            from pikobs.verifprofile.scorecard import make_scorecards
            sc_tasks, sc_results = make_scorecards(plot_tasks, pathwork)
            plot_tasks = list(plot_tasks) + sc_tasks
            results = list(results) + sc_results
            if sc_results:
                print(f"{p} scorecard: {len(sc_results)} figure(s) in "
                      f"{os.path.join(pathwork, 'scorecard')}", flush=True)
        except Exception as exc:                            # never fatal
            print(f"{p} scorecard failed: {exc}", file=sys.stderr, flush=True)

    items = [{'experience': t['experience'], 'family': t['family'],
              'fonction': t['function'], 'region': t['region'],
              'flag_criteria': t['flag'], 'id_stn': t['id_stn'],
              'special': t['special_label'], 'land_ocean': t['land_ocean'],
              'varno': str(t['varno']), 'filename': os.path.basename(r)}
             for t, r in zip(plot_tasks, results) if r]
    if not items:
        print(f"{p} ERROR: no figure was produced.", file=sys.stderr,
              flush=True)
        return 1
    keys = ["experience", "family", "fonction", "region", "flag_criteria",
            "id_stn", "special", "land_ocean", "varno"]
    generate_web(
        items, keys, os.path.join(pathwork, "pikobs_verifprofile_viewer.html"),
        title="Pikobs Vertical Profile Viewer",
        subtitle=(
            "Mean, sigma and number of observations, level by level. " +
            (f"Each experience against <b>{control[0]}</b>, matched "
             "observation by observation, so both runs rest on the same "
             "observations at every level. The dots on the left of each "
             "panel are the test of that panel: <b>red</b> where the "
             "experience is better, <b>blue</b> where the control is, "
             "hollow where the change is not larger than noise."
             if matched else
             "One run, so the panels are the profile itself.")) + runs_block(all_runs, control, (datestart, dateend)),
        image_subdir_key="family",
        issues_url="https://gitlab.science.gc.ca/dlo001/Pikobs")

    timing['seconds']['total'] = time.time() - t_start
    _report_timing(timing, pathwork)
    print(f"{p} done -- output in: {pathwork}", flush=True)
    return 0


def arg_call() -> None:
    import argparse

    ap = argparse.ArgumentParser(
        prog="pikobs-verifprofile",
        description="Vertical profiles of the departures, one run or a "
                    "control against experiences.")
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
                    choices=['omp', 'oma', 'obs_error'])
    ap.add_argument('--varnos', nargs='*', default=[])
    ap.add_argument('--id_stn', nargs='+', default=['join'])
    ap.add_argument('--land_ocean', nargs='+', default=['all'],
                    choices=list(LAND_OCEAN_CHOICES))
    ap.add_argument('--special_column', default='off', choices=['on', 'off'])
    ap.add_argument('--min_obs', default=MIN_OBS_PER_LEVEL, type=int,
                    help="Levels with fewer observations are dropped.")
    ap.add_argument('--ratio_figure', default='off', choices=['on', 'off'],
                    help="on: with two or more experiences, one more figure "
                         "per selection with the sigma ratio of all of "
                         "them against the control (default off).")
    ap.add_argument('--match', nargs='+', default=['on'],
                      help="on: with a control, the same observations in both "
                         "runs, paired tests. off: each run with all its "
                         "observations and its own flags, Welch and F tests.")
    ap.add_argument('--svg', default='off', choices=['on', 'off'])
    ap.add_argument('--n_cpus', '--n_cpu', default=1, type=int,
                    dest='n_cpus')
    ap.add_argument('--no_submit', action='store_true')
    # options of the old progps, accepted so its wrappers keep working
    ap.add_argument('--channel', default='all', help=argparse.SUPPRESS)
    ap.add_argument('--surface', default=None, help=argparse.SUPPRESS)
    ap.add_argument('--common_sample', action='store_true',
                    help=argparse.SUPPRESS)
    ap.add_argument('--ftest_mode', default=None, help=argparse.SUPPRESS)

    args = ap.parse_args()
    for arg in vars(args):
        print(f'--{arg} {getattr(args, arg)}', flush=True)
    if args.ftest_mode or args.common_sample:
        print("[verifprofile] note: --ftest_mode and --common_sample belong "
              "to the old progps; with a control the runs are always "
              "matched and tested as in pikobs.stats", flush=True)
    if args.surface and args.land_ocean == ['all']:
        args.land_ocean = [{'sea': 'ocean', 'land': 'land'}.get(args.surface,
                                                               'all')]

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
    if args.path_control_files and args.path_control_files.strip() \
            and args.path_control_files != 'undefined':
        ctl_name = (args.control_name or 'control').strip() or 'control'
        if ctl_name in names:
            raise ValueError(f"the control and an experience share the "
                             f"name '{ctl_name}'")
        control = (ctl_name,
                   args.path_control_files.strip().rstrip('/') or '/')

    maybe_submit_to_pbs(args)
    sys.exit(make_verifprofile(
        runs, args.pathwork, args.datestart, args.dateend, args.region,
        _split_tokens(args.family), args.flags_criteria, args.fonction,
        _split_tokens(args.varnos), args.id_stn, args.land_ocean,
        args.n_cpus, control, svg_enabled(args.svg), args.min_obs,
        args.special_column == 'on', args.ratio_figure == 'on',
                 match=args.match))


if __name__ == '__main__':
    arg_call()
