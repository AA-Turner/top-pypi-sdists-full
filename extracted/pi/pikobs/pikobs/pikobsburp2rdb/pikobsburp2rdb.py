#!/usr/bin/env python3
"""
================================================================
pikobs.pikobsburp2rdb — BURP to SQLite Conversion Module
================================================================

Convert meteorological **BURP** binary files into **SQLite RDB**
databases consumable by the Pikobs diagnostic pipeline.

The module wraps the external ``burp2rdb`` CMC binary and executes
many conversions in parallel through Dask. It is the typical first
step before running any other Pikobs module (``mapobs``, ``pipeline``,
``profile``, ...) on raw assimilation outputs.

For each ``(experience, family, date)`` triplet the module produces
one SQLite file::

    <pathwork>/<experience_name>/<YYYYMMDDHH>_<family>

:Author:        D. Lo / CMC pikobs maintainers
:Module:        ``pikobs.pikobsburp2rdb``
:Last revision: 2026-05

Highlights
----------

* **Single source of truth** for the ``burp2rdb`` binary, resolved via
  ``$BURP2RDB_BIN`` first, then ``shutil.which()``. The orchestrator
  refuses to start if it cannot find a working binary.
* **Hard timeout** on every ``subprocess.run`` call (default 30 min)
  so a stuck conversion can never block the whole job.
* **No PIPE deadlock** — stderr is merged into stdout and captured as
  bytes, avoiding the well-known full-PIPE hang when ``burp2rdb``
  emits large amounts of progress output.
* **No interactive prompt in parallel mode** — when ``--n_cpus > 1``
  the script never calls ``input()`` (which would hang waiting for
  stdin in a PBS batch job). ``--force_clean`` is required for those
  cases.
* **Automatic family discovery** when ``--family`` is not given,
  scanning the input directories for ``YYYYMMDDHH_<family>`` files.
* **Integrity verification** of every produced SQLite file before
  declaring the conversion successful.

.. note::
   This module shells out to the ``burp2rdb`` binary shipped by CMC.
   Make sure the matching SSM packages are loaded before launching.
   The wrapper ``run_pikobsburp2rdb.sh`` handles this for you.

---

1. How to run
=============

Download the example script, make it executable, and launch it. The
script submits itself to PBS automatically if run from a login node.

.. code-block:: bash

   wget https://gitlab.science.gc.ca/dlo001/Pikobs/-/raw/master/pikobs/script/run_pikobsburp2rdb.sh
   chmod +x run_pikobsburp2rdb.sh
   ./run_pikobsburp2rdb.sh

.. note::
   The script handles PBS submission and environment activation
   automatically. You do **not** need to call ``qsub`` yourself.

Expected output:

.. code-block:: text

   🚀 Launching from login node. Auto-submitting to qsub...
   ✅ Job submitted: 52919002.ppp8pbs-01-ib
   👀 Waiting for output...
   =================================================================
   🖥️  Running on: ppp8cn-046  JobID: 52919002.ppp8pbs-01-ib
   🐍 Python: 3.11.x  |  📦 Pikobs: 1.2.0
   =================================================================
   [burp2rdb] Converting 240 files on 40 workers...
   [burp2rdb] OK  2026020100_ua  →  experiment/2026020100_ua  (4.2s)
   [burp2rdb] OK  2026020106_ua  →  experiment/2026020106_ua  (3.9s)
   ...
   ✅ Process completed successfully.
   🏁 Job finished. Log: /home/.../burp2rdb_20260515_175019.log

---

2. Configuration
================

Open ``run_pikobsburp2rdb.sh`` and edit the ``USER SETTINGS`` block:

.. code-block:: bash

   # === USER SETTINGS — edit these ================================
   PATHWORK="/path/to/output_dir"            # where SQLite files go
   PATH_EXPERIENCE="/path/to/burp_files/"   # where raw BURP files live
   EXPERIENCE_NAME="your_experiment_label"  # subfolder name in PATHWORK
   DATESTART="2026020100"                   # YYYYMMDDHH (UTC)
   DATEEND="2026020200"                     # YYYYMMDDHH (UTC), inclusive
   FAMILY="ua sw ai sc ro"                  # space-separated, or leave
                                            # empty for auto-discovery
   N_CPUS=40                                # Dask workers
   WALLTIME="02:00:00"
   # ================================================================

+----------------------+--------------------------------------------------+
| Variable             | Description                                      |
+======================+==================================================+
| ``PATHWORK``         | Root output directory for SQLite RDB files       |
+----------------------+--------------------------------------------------+
| ``PATH_EXPERIENCE``  | Directory containing raw BURP binary files       |
+----------------------+--------------------------------------------------+
| ``EXPERIENCE_NAME``  | Subfolder name and label for the run             |
+----------------------+--------------------------------------------------+
| ``DATESTART``        | Start of the period ``YYYYMMDDHH``               |
+----------------------+--------------------------------------------------+
| ``DATEEND``          | End of the period ``YYYYMMDDHH`` (inclusive)     |
+----------------------+--------------------------------------------------+
| ``FAMILY``           | Observation families — leave empty to            |
|                      | auto-discover from the input directory           |
+----------------------+--------------------------------------------------+
| ``N_CPUS``           | Number of parallel Dask workers                  |
+----------------------+--------------------------------------------------+
| ``WALLTIME``         | PBS walltime limit ``HH:MM:SS``                  |
+----------------------+--------------------------------------------------+

---

3. Family name resolution & ``-ade``
=====================================

Raw archive filenames don't match ``burp2rdb``'s ``-type`` values
directly (e.g. ``ua_radiosonde``, ``rars_amsua``, ``sf2_a`` aren't
valid ``-type`` arguments). :func:`get_burp_type` resolves the real
``-type`` for any family name seen across the four BANCO source
directories in production (``cutoff``, ``derialt``, ``bgckalt``,
``postalt``):

* **Umbrella prefixes** (``ai``, ``sf``, ``sw``, ``sc``->``scat``,
  ``ua``, ``ch``/``tar_ch``->``sf``) — the prefix itself IS the
  ``-type``; any subtype suffix (``ai_acars``, ``sf_metar``,
  ``ch_o3_gome2b``...) is discarded.
* **``rars_<X>``** — RARS is a retransmission source; strips to ``X``
  directly (``rars_amsua`` -> ``amsua``).
* **Non-taxonomic suffixes** stripped before matching: ``_qc``,
  ``_allsky``, ``_a``, ``_b`` (paired secondary/backup feed markers —
  e.g. ``ua_a``/``ua_b``, ``sf2_a``/``sf2_b``), ``fsr1``/``fsr2``.
* **Bare confirmed names** (:data:`_CONFIRMED_RENAME`) — e.g.
  ``to_amsua``->``amsua``, ``gp``->``gbgps``, ``mwhs2``->``mwhs``.

.. warning::
   **Confidence levels differ.** Most of the table above is confirmed
   directly against burp2rdb's own documentation and/or a real run's
   record count. A few entries are **inferred** from the parallel
   naming pattern only, NOT individually verified the same way:
   ``gp2``->``gbgps`` (parallel to ``gp``/``gp_b``), ``sf2``->``sf``
   (parallel to ``sf``/``sf_a``/``sf_b``), and treating ``_a`` the
   same as ``_b`` in general. If a conversion for one of these comes
   back with ``0 Records`` unexpectedly, don't assume it's correct —
   spot-check it the same way ``ua_radiosonde`` was originally
   confirmed (see :func:`needs_ade_from_path` below).

**``-ade``** is a SEPARATE question from ``-type``, and — this was the
hard-won finding — depends on the SOURCE DIRECTORY, not the family
name:

* ``.../banco/cutoff/...`` -> ``-ade`` REQUIRED. Confirmed on a real
  run (2026081800): 14 different families with real data — including
  *bare* names like ``ro``, ``pr``, ``iasi``, ``csr``, ``atms``,
  ``ssmis``, ``crisfsr``, ``to_amsua``, ``to_amsub`` — ALL silently
  selected 0 records without ``-ade``, 14/14 with zero exceptions.
* ``.../banco/derialt/...``, ``.../banco/bgckalt/...``,
  ``.../banco/postalt/...`` -> ``-ade`` NOT used (BANCO-native,
  pre-dating the ADE pipeline). This is the strong operational
  assumption but, unlike ``cutoff``, has NOT been individually
  confirmed the same way — verify with
  ``diagnose_empty_families.sh`` if a conversion from one of these
  looks empty unexpectedly.
* The **same family name needs ``-ade`` from one directory and not
  from another** (e.g. ``to_amsua`` from ``cutoff`` vs. ``derialt``) —
  no name-based rule can express this, which is why
  :func:`needs_ade_from_path` inspects the INPUT FILE PATH directly
  instead of guessing from the family name. The older
  :func:`needs_ade` (name-only) is kept only as a last-resort fallback
  for an unrecognised source directory.

---

4. Output
=========

After a successful run ``$PATHWORK`` contains::

   $PATHWORK/
   └── <experience_name>/
       ├── 2026020100_ua
       ├── 2026020100_sw
       ├── 2026020106_ua
       ├── 2026020106_sw
       └── ...

Each file is a valid SQLite database containing the ``header`` and
``DATA`` tables consumed by ``mapobs``, ``pipeline``, and all other
Pikobs diagnostic modules.

---

5. Support
==========

For bugs, feature requests or questions, open an issue at:

* **GitLab issues**:
  `<https://gitlab.science.gc.ca/dlo001/Pikobs/-/issues>`_
"""
from __future__ import annotations
import argparse
import datetime
import logging
import os
import shlex
import shutil
import subprocess
import sys
from datetime import timedelta
from typing import List, Optional, Tuple
import dask
from dask.distributed import Client
# =============================================================================
# Module-level configuration
# =============================================================================
#: Per-conversion hard timeout (seconds). Prevents a stuck burp2rdb
#: process from holding up the whole job until PBS walltime.
SUBPROCESS_TIMEOUT_S: int = 30 * 60      # 30 minutes
#: Minimum BURP file size in bytes; smaller files are flagged as
#: probably empty and skipped (not an error, just a warning).
MIN_BURP_SIZE_BYTES: int = 100
#: SSM tip printed when burp2rdb is not found (this is only a
#: fallback message now -- _resolve_burp2rdb() itself defaults to the
#: hardcoded _PREFERRED_BURP2RDB_BIN path above and doesn't actually
#: need this loaded, but the hint still matters if that hardcoded
#: path is ever missing on a different system).
#: CORRECTED (2026-08): earlier revisions of this hint recommended
#: "20260202" (no suffix) as "the confirmed one" -- that was wrong.
#: It was only "confirmed" in the sense of "what the pipeline
#: happened to already be using", not "known to work correctly". It
#: has a real bug: SEGFAULTs on MWHS records (e.g. rars_mwhs2) with
#: "forrtl: error (65): floating invalid", reproducible 2/2 cycles.
#: The IDENTICAL command against "20260202-2" (Version-5.26) completed
#: cleanly on the same input file. Use "20260202-2".
#: Second domain (cmo/cmoi/base) is still UNVERIFIED -- carried over
#: as-is, never independently checked the way the first one was.
_SSM_HINT = (
    "Load the burp2rdb SSM packages first, e.g.:\n"
    ". ssmuse-sh -d eccc/cmd/cmda/utils/20260202-2\n"
    ". ssmuse-sh -d eccc/cmo/cmoi/base/20260205  # unverified, see comment above\n"
    "Or use the wrapper run_pikobsburp2rdb.sh."
)
logging.basicConfig(
    format="[%(levelname)s] %(message)s",
    level=logging.INFO,
)
log = logging.getLogger("pikobsburp2rdb")
# =============================================================================
# BURP type mapping
# =============================================================================
#: Umbrella-family prefixes seen on real archive filenames
#: (e.g. ``ai_acars``, ``sf_metar``, ``rars_amsua``, ``tar_ch_mlso3``).
#: Confirmed directly from burp2rdb's own documentation (the
#: "Conversion des observations de BANCO/ADE" tables). These umbrella
#: prefixes group SEVERAL distinct networks/codtypes under ONE
#: burp2rdb ``-type`` model — the suffix (acars/ads/metar/synop/...)
#: only tells you which CODTYP SUBSET is in that particular archive
#: file, it is NOT a different burp2rdb type:
#:   ACARS/ADS/AIREP/AMDAR              -> type "ai"   (ADE UPRAIR table)
#:   BATHY/BUOY/METAR/NEIGE/OZONE/PM25/
#:   SA/SHEF/SYNOP (and AWOS/CA/HWOS/
#:   WINIDE/DRIFTER by the same pattern) -> type "sf"   (ADE SURFACE table)
#:   METEOSAT/MODIS/SATWINDS (GEO/POLAR
#:   by the same pattern)                -> type "sw"   (ADE REMOTE table)
#:   SCAT (ASCAT/HSCAT)                  -> type "scat" (BANCO + ADE REMOTE)
#:   RADIOSONDE (and CMC by the same
#:   pattern)                            -> type "ua"   (ADE UPRAIR table)
#:   CH / TAR_CH (chemistry constituents,
#:   GOME/OMPS/MLS-O3/OMTO3/TROPOMI...)   -> type "sf"   (confirmed: same
#:   rule as the pre-existing bare "ch" -> "sf" entry, extended to every
#:   compound family that contains "ch" — including the "tar_ch_" ones)
_UMBRELLA_TO_TYPE = {
    "ai": "ai",
    "sf": "sf",
    "sw": "sw",
    "sc": "scat",
    "ua": "ua",
    "ch": "sf",
    "tar_ch": "sf",
}

#: ``rars_<X>`` — RARS is just a retransmission SOURCE for the SAME
#: instrument, not a different burp2rdb type: X itself is the type
#: (confirmed: TOVS1B AMSUA/AMSUB -> amsua/amsub; ATMS -> atms).
_RARS_PREFIX = "rars_"

#: Non-taxonomic suffixes: they mark a SECONDARY/backup feed of the
#: SAME underlying BURP type (``_a``/``_b`` — a matched PAIR, e.g.
#: ``ua_a``/``ua_b``, ``sf2_a``/``sf2_b``; INFERRED from the parallel
#: naming, not individually confirmed the way ``ua_radiosonde`` was —
#: verify with the diagnose script if in doubt), or a QC/allsky/
#: channel-set variant (``_qc``/``_allsky``) — none of these change
#: what ``-type`` should be.
_STRIP_SUFFIXES = ("_qc", "_allsky", "_a", "_b", "fsr1", "fsr2")

#: Bare (non-umbrella) family names confirmed directly against
#: burp2rdb's documentation tables, plus the pre-existing entries this
#: rename table already had before it was extended.
_CONFIRMED_RENAME = {
    "to_amsua": "amsua",
    "to_amsub": "amsub",
    "gp":       "gbgps",
    "gp2":      "gbgps",  # INFERRED: parallel GPS-RO feed, same as gp/gp_b — not individually verified
    "crisfsr":  "cris",
    "cris":     "cris",   # bare "cris" (postalt/bgckalt) — BANCO table: CRIS -> cris
    "sc":       "scat",
    "mwhs2":    "mwhs",
    "ssmis":    "ssmi",
    "amsua":  "amsua",
    "amsub":  "amsub",
    "atms":   "atms",
    "csr":    "csr",
    "iasi":   "iasi",
    "ro":     "ro",
    "pr":     "pr",
    "go":     "go",
    "airs":   "airs",
    "ai": "ai", "sf": "sf", "sw": "sw", "ua": "ua",
    "sf2": "sf",  # INFERRED: parallel surface feed, same as sf/sf_a/sf_b — not individually verified
}



def _classify_family(family_name: str) -> Tuple[str, bool]:
    """Resolve a Pikobs family name to ``(burp_type, needs_ade)``.

    Real archive filenames carry TWO kinds of naming noise beyond the
    base BURP type:

    * **Umbrella prefixes** — ``ai_acars``, ``sf_metar``,
      ``sw_geo``... group several distinct networks/codtypes under
      ONE burp2rdb ``-type`` model. Per burp2rdb's own documentation,
      the prefix itself (``ai``/``sf``/``sw``/``sc``->``scat``/``ua``)
      IS the correct ``-type`` — the suffix (acars/metar/geo/...) only
      says which codtyp subset is in that file, and is discarded here.
    * **``rars_<X>``** — RARS is a retransmission source, not a
      different instrument: stripping the prefix and resolving ``X``
      directly gives the correct type (``rars_amsua`` -> ``amsua``).
    * **Non-taxonomic suffixes** — ``_qc``, ``_allsky``, ``_b``
      (secondary/backup feed), ``fsr1``/``fsr2`` — stripped as before.

    **``-ade``**: confirmed by a real run (``ua_radiosonde`` selected 0
    of 692 records without it, matching the docs' ADE UPRAIR table).
    The pattern that decides it is exactly the umbrella-PREFIX-with-
    SUFFIX case above: a *bare* umbrella name (``ai``, ``sf``, ``sw``,
    ``ua``, ``sc``, ``ch``) comes from BANCO (bgckalt/postalt/evalalt)
    and does NOT take ``-ade``; the SAME umbrella with a subtype suffix
    (``ai_acars``, ``sf_metar``, ``sw_geo``, ``ua_radiosonde``,
    ``sc_ascat``, ``ch_gome``, ``tar_ch_mlso3``...) comes from the ADE
    and DOES need ``-ade``. This is directly CONFIRMED for
    ``ai``/``sf``/``sw``/``ua``/``sc`` against the ADE UPRAIR / ADE
    SURFACE / ADE REMOTE tables in burp2rdb's own documentation (and
    empirically for ``ua_radiosonde``: it silently selected 0 of 692
    records without ``-ade``). For ``ch``/``tar_ch`` it is an
    EXTRAPOLATION of the same confirmed pattern (not independently
    verified against a doc table) — check the "Select Codtyp" / record
    count in a real run's output before fully trusting a ``ch_*`` or
    ``tar_ch_*`` conversion.

    ``rars_*`` is different in kind (a retransmission SOURCE, not an
    umbrella+subtype pair) but empirically needs ``-ade`` too: RARS
    retransmits data from instruments whose native archive IS the ADE.
    CONFIRMED for ``rars_amsua`` (0 of 846 records selected without
    ``-ade``, the same failure signature ``-ade`` fixed for
    ``ua_radiosonde``). The other ``rars_*`` families return
    ``needs_ade=True`` by the same extrapolated reasoning — verify
    individually the same way if in doubt.

    :param family_name: Pikobs family name (e.g. ``"ai_acars"``,
        ``"sf_metar"``, ``"rars_amsua"``, ``"sf_drifter_b"``).
    :returns: ``(burp_type, needs_ade)``.
    :rtype: Tuple[str, bool]
    """
    f = family_name.lower()

    for suffix in _STRIP_SUFFIXES:
        if f.endswith(suffix):
            f = f[: -len(suffix)]

    # rars_<X>: strip the source prefix, resolve X directly. RARS
    # retransmits data from instruments (AMSU-A, AMSU-B, ATMS, MHS...)
    # whose native archive IS the ADE, so -ade is needed here too —
    # CONFIRMED empirically for rars_amsua (846 records in file, 0
    # selected without -ade; matches the exact ua_radiosonde failure
    # signature that -ade fixed). The other rars_* families below are
    # extrapolated from the same reasoning, not yet individually
    # verified — check "Select Codtyp ... 0 Records" the same way if
    # in doubt.
    if f.startswith(_RARS_PREFIX):
        f = f[len(_RARS_PREFIX):]
        if f in _CONFIRMED_RENAME:
            return _CONFIRMED_RENAME[f], True
        log.warning(
            "get_burp_type: '%s' -> '%s' (stripped 'rars_') is NOT in "
            "the confirmed rename table. Verify this -type before "
            "trusting the conversion for this family.",
            family_name, f,
        )
        return f, True

    # Confirmed umbrella families: the PREFIX itself is the -type; the
    # suffix (subtype) is intentionally discarded, per burp2rdb's docs.
    # A BARE umbrella name (no "_subtype") is BANCO -> no -ade; the
    # SAME umbrella WITH a subtype suffix is ADE -> needs -ade.
    for umbrella, burp_type in _UMBRELLA_TO_TYPE.items():
        if f == umbrella:
            return burp_type, False
        if f.startswith(umbrella + "_"):
            return burp_type, True

    # Bare family name (no umbrella prefix at all) — BANCO, no -ade.
    if f in _CONFIRMED_RENAME:
        return _CONFIRMED_RENAME[f], False

    # Genuinely unrecognised — behaves exactly as the original function
    # did (pass through unchanged), no new warning, no -ade.
    return f, False


def get_burp_type(family_name: str) -> str:
    """Map a Pikobs family name to the ``-type`` argument of burp2rdb.

    See :func:`_classify_family` for the full resolution rules.

    :param family_name: Pikobs family name (e.g. ``"ai_acars"``).
    :returns: BURP type accepted by ``burp2rdb -type ...``.
    :rtype: str
    """
    return _classify_family(family_name)[0]


def needs_ade(family_name: str) -> bool:
    """Whether ``family_name`` requires the ``-ade`` flag on burp2rdb.

    .. warning::
       **Superseded by** :func:`needs_ade_from_path`. Kept only as a
       documented fallback for callers that genuinely have no input
       path to inspect (e.g. purely offline family-name classification,
       or the ``main`` CLI's dry-run listing) — real conversions should
       always use :func:`needs_ade_from_path` instead, per the finding
       below.

       Real-run evidence (2026081800, ``.../banco/cutoff/``) showed
       this NAME-based heuristic is wrong in its premise: 14 different
       families with real data — including *bare* names this function
       classifies as ``False`` (``ro``, ``pr``, ``iasi``, ``csr``,
       ``atms``, ``ssmis``, ``crisfsr``, ``to_amsua``, ``to_amsub``) —
       ALL needed ``-ade`` when read from ``cutoff``, 14/14 with zero
       exceptions. ``-ade`` is a property of the SOURCE DIRECTORY
       (``cutoff`` = ADE-formatted; ``derialt``/``bgckalt``/``postalt``
       = BANCO-native), not of the family name — the same family name
       (e.g. ``to_amsua``) needs ``-ade`` from one directory and not
       from another, which no name-based rule can express.

    See :func:`_classify_family` for the full name-based resolution
    rules this still applies (unreliable — see warning above).

    :param family_name: Pikobs family name (e.g. ``"ua_radiosonde"``).
    :returns: ``True`` if ``-ade`` should be added to the command.
    :rtype: bool
    """
    return _classify_family(family_name)[1]


# Source directories confirmed (or assumed by strong operational
# convention) to require/not require -ade. Matched against any path
# COMPONENT of the input file's directory (e.g. ".../banco/cutoff/x"
# matches "cutoff" whether or not there's more path before/after it).
_ADE_SOURCE_DIRS    = frozenset({"cutoff"})
_NON_ADE_SOURCE_DIRS = frozenset({"derialt", "bgckalt", "postalt"})


def needs_ade_from_path(file_path: str, family_name: Optional[str] = None) -> bool:
    """Whether ``-ade`` is needed, based on the INPUT FILE's directory.

    This is the PRIMARY, preferred way to decide ``-ade`` — see the
    warning on :func:`needs_ade` for why the family-name-based version
    is unreliable. Confirmed empirically for the ``cutoff`` case
    (2026081800: 14/14 families with real data needed ``-ade`` when
    read from ``.../banco/cutoff/...``, including several BARE family
    names the old name-based heuristic classified as not needing it).
    ``derialt``/``bgckalt``/``postalt`` = ``False`` is the strong
    operational assumption (BANCO-native, pre-dating the ADE pipeline)
    but has NOT been individually verified the same way ``cutoff``
    was — spot-check with :func:`~pikobs.pikobsburp2rdb.diagnose
    <the diagnose_empty_families.sh script>` the same way if a
    conversion from one of these looks empty unexpectedly.

    :param file_path: Full path to the input BURP file (e.g.
        ``".../banco/cutoff/2026081800_ro"``). Only the DIRECTORY
        portion is inspected — any path component matching a known
        source directory name decides the answer.
    :param family_name: Optional — used ONLY as a last-resort fallback
        (via :func:`needs_ade`) if the path doesn't match any known
        source directory, so an unrecognised path still gets a
        best-effort answer instead of silently defaulting to one side.
    :returns: ``True`` if ``-ade`` should be added to the command.
    :rtype: bool
    """
    parts = os.path.normpath(file_path).split(os.sep)
    if any(p in _ADE_SOURCE_DIRS for p in parts):
        return True
    if any(p in _NON_ADE_SOURCE_DIRS for p in parts):
        return False
    log.warning(
        "needs_ade_from_path: '%s' matches neither a known ADE source "
        "dir %s nor a known non-ADE source dir %s — falling back to "
        "the (unreliable) family-name heuristic for '%s'. Verify this "
        "conversion's record count explicitly.",
        file_path, sorted(_ADE_SOURCE_DIRS), sorted(_NON_ADE_SOURCE_DIRS),
        family_name,
    )
    return needs_ade(family_name) if family_name is not None else False


# =============================================================================
# burp2rdb binary resolution
# =============================================================================
#: Confirmed-good burp2rdb build. The base "20260202" domain (no
#: suffix) has a real bug: it SEGFAULTs with "forrtl: error (65):
#: floating invalid" while writing MWHS records (e.g. rars_mwhs2),
#: confirmed reproducible 2/2 cycles (2026081800, 2026081900) -- same
#: input file, same command, ONLY the domain differs. Running the
#: identical command against "20260202-2" (Version-5.26) completed
#: cleanly. Checked here BEFORE the $PATH search so the pipeline uses
#: the known-good build by default, regardless of which domain
#: happens to be sourced in the calling shell.
_PREFERRED_BURP2RDB_BIN = (
    "/fs/ssm/eccc/cmd/cmda/utils/20260202-2/rhel-9-amd64-64/bin/burp2rdb"
)


def _resolve_burp2rdb() -> Optional[str]:
    """Locate the ``burp2rdb`` binary.

    Resolution order:

    1. ``$BURP2RDB_BIN`` environment variable, if explicitly set —
       always wins, so a deliberate override (e.g. testing a newer
       build later) still works without editing this file.
    2. :data:`_PREFERRED_BURP2RDB_BIN` — the confirmed-good
       "20260202-2" build (see its docstring for why "20260202", no
       suffix, is NOT used here).
    3. ``shutil.which("burp2rdb")`` — searches the current ``$PATH``,
       in case this runs on a system where the hardcoded path above
       doesn't exist.

    :returns: Absolute path to a usable binary, or ``None`` if not found.
    """
    env_path = os.environ.get("BURP2RDB_BIN", "").strip()
    if env_path and os.path.isfile(env_path) and os.access(env_path, os.X_OK):
        return env_path

    if os.path.isfile(_PREFERRED_BURP2RDB_BIN) and os.access(_PREFERRED_BURP2RDB_BIN, os.X_OK):
        return _PREFERRED_BURP2RDB_BIN

    return shutil.which("burp2rdb")
# =============================================================================
# Conversion engine
# =============================================================================
def _is_sqlite3_intact(filepath: str) -> bool:
    """Cheap integrity check on a SQLite file.
    Opens the file read-only and runs a trivial query against
    ``sqlite_master``. Any database-level error is reported as "not
    intact" — corrupted files, partially-written files and non-SQLite
    files all fail this check.
    :param filepath: file to check.
    :returns: ``True`` if the file opens and answers a SELECT.
    :rtype: bool
    """
    if not os.path.isfile(filepath):
        return False
    try:
        import sqlite3
        with sqlite3.connect(filepath, timeout=5) as conn:
            conn.execute("SELECT name FROM sqlite_master LIMIT 1;").fetchone()
        return True
    except sqlite3.DatabaseError:
        return False
def convert_single_file(f_in:     str,
                        exp_name: str,
                        family:   str,
                        f_out:    str,
                        fdate:    str) -> bool:
    """Convert one BURP file to SQLite via ``burp2rdb``.
    This function is invoked once per ``(experience, family, date)``
    triplet by Dask workers. It is **idempotent**: if ``f_out`` is
    already a valid SQLite file the function returns immediately.
    The conversion is **atomic**: ``burp2rdb`` writes to ``f_out.tmp``
    first; only if the produced file passes :func:`_is_sqlite3_intact`
    is it renamed to ``f_out``.
    :param f_in:     path to the input BURP file.
    :param exp_name: experiment label (for log messages).
    :param family:   Pikobs family name.
    :param f_out:    target SQLite path.
    :param fdate:    ``YYYYMMDDHH`` (for log messages only).
    :returns: ``True`` on success, ``False`` on any error.
    :rtype: bool
    """
    # Idempotency: skip if already converted.
    if _is_sqlite3_intact(f_out):
        log.info("OK    Already converted: %s/%s",
                 exp_name, os.path.basename(f_out))
        return True
    if not os.path.isfile(f_in):
        log.warning("Missing input: %s for %s in %s", fdate, family, exp_name)
        return False
    try:
        size = os.path.getsize(f_in)
    except OSError as exc:
        log.warning("Cannot stat %s: %s", f_in, exc)
        return False
    if size < MIN_BURP_SIZE_BYTES:
        log.warning("Probably-empty file %s (%d bytes); skipped.",
                    os.path.basename(f_in), size)
        return False
    burp2rdb_bin = _resolve_burp2rdb()
    if not burp2rdb_bin:
        log.error("burp2rdb binary not found in this worker.\n%s", _SSM_HINT)
        return False
    f_tmp = f_out + ".tmp"
    if os.path.isfile(f_tmp):
        try:
            os.remove(f_tmp)
        except OSError:
            pass
    cmd = [burp2rdb_bin,
           "-in", f_in,
           "-type", get_burp_type(family),
           "-out", f_tmp]
    if needs_ade_from_path(f_in, family):
        cmd.append("-ade")
    cmd_str = " ".join(shlex.quote(c) for c in cmd)
    log.info("RUN   %s (%s) for %s\n    %s", fdate, family, exp_name, cmd_str)
    try:
        # Merge stderr into stdout to avoid a deadlock if burp2rdb
        # emits more than a pipe's worth on stderr.
        # capture_output=True keeps the parent's stderr clean.
        subprocess.run(
            cmd,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=SUBPROCESS_TIMEOUT_S,
        )
    except subprocess.TimeoutExpired:
        log.error("TIMEOUT after %ds on %s (%s, %s)\n    %s",
                  SUBPROCESS_TIMEOUT_S, fdate, family, exp_name, cmd_str)
        if os.path.isfile(f_tmp):
            os.remove(f_tmp)
        return False
    except subprocess.CalledProcessError as exc:
        out = exc.stdout.decode("utf-8", errors="ignore") if exc.stdout else ""

        # burp2rdb's own RMN/XDF library SEGFAULTs (instead of returning a
        # clean error) when the source file isn't valid BURP/XDF data —
        # empty, truncated, or genuinely corrupted. Detect that specific
        # crash signature and lead with an unambiguous, actionable summary
        # BEFORE the raw Fortran/C stack trace, so it's immediately clear
        # this is a SOURCE FILE problem, not a Pikobs -type/config issue
        # (the "-type" was already accepted fine at this point — the crash
        # happens strictly later, while opening the file).
        crashed_on_open = (
            "not XDF type" in out
            or "SIGSEGV" in out
            or (exc.returncode is not None and exc.returncode < 0)
        )
        # DIFFERENT crash signature, confirmed reproducible 2/2 cycles on
        # rars_mwhs2 (2026081800: 880 records, 2026081900: 870 records) --
        # the file OPENS fine and burp2rdb's own adeBurpSelector reports
        # selecting all records successfully ("Select Codtyp"/"...Selector
        # ... N Records" appear in the log BEFORE this crash), so this is
        # NOT a corrupt/empty source file like crashed_on_open above. The
        # crash happens strictly LATER, inside burp2rdb's MWHS-specific
        # header-writing code (putHeader3D in mwhsObs.h) -- looks like a
        # burp2rdb bug triggered by some specific field value in certain
        # MWHS records (e.g. a NaN/out-of-range scan geometry value), not
        # something fixable on the Pikobs/config side. If this keeps
        # happening across most/all cycles for a family, it's worth
        # reporting to the burp2rdb maintainers with one of the failing
        # files attached, rather than continuing to just skip it.
        mwhs_floating_crash = "floating invalid" in out and "mwhsObs" in out

        if crashed_on_open:
            log.error(
                "burp2rdb CRASHED (segfault) opening the source file for "
                "%s (%s, %s) — the BURP/cutoff file is likely empty, "
                "truncated, or not valid XDF/BURP data. This is NOT a "
                "-type or Pikobs config issue (the type was already "
                "accepted). Reproduce/inspect directly:\n"
                "    %s\n"
                "    ls -la %s\n"
                "Skipping this file; other conversions are unaffected.",
                fdate, family, exp_name, cmd_str, f_in,
            )
        elif mwhs_floating_crash:
            log.error(
                "burp2rdb CRASHED (floating-point exception) for %s (%s, "
                "%s) -- NOT a corrupt/empty file: the log shows records "
                "WERE selected successfully before the crash. This looks "
                "like a burp2rdb bug in its MWHS header-writing code "
                "(putHeader3D/mwhsObs.h), likely triggered by a specific "
                "field value in one or more records of this file. "
                "Reproduce directly:\n"
                "    %s\n"
                "If this recurs across most/all cycles for this family, "
                "report it to the burp2rdb maintainers with a failing "
                "file attached -- it is probably not fixable from the "
                "Pikobs/config side. Skipping this file; other "
                "conversions are unaffected.",
                fdate, family, exp_name, cmd_str,
            )
        log.error("burp2rdb failed for %s (%s, %s):\n    %s\n%s",
                  fdate, family, exp_name, cmd_str, out.strip())
        if os.path.isfile(f_tmp):
            os.remove(f_tmp)
        return False
    if not _is_sqlite3_intact(f_tmp):
        log.error("Generated file is not a valid SQLite: %s", f_tmp)
        try:
            os.remove(f_tmp)
        except OSError:
            pass
        return False
    try:
        os.replace(f_tmp, f_out)
    except OSError as exc:
        log.error("Cannot move %s -> %s: %s", f_tmp, f_out, exc)
        return False
    return True
# =============================================================================
# Orchestrator
# =============================================================================
def _detect_families(paths: List[str]) -> List[str]:
    """Scan input directories for ``YYYYMMDDHH_<family>`` files.
    Returns the sorted union of every family seen in any directory.
    """
    detected: set = set()
    for path_exp in paths:
        if not os.path.isdir(path_exp):
            continue
        for item in os.listdir(path_exp):
            # Expected format: 10 digits + "_" + family
            if len(item) > 11 and item[10] == "_" and item[:10].isdigit():
                detected.add(item[11:])
    return sorted(detected)
# the official copy of the CMC tables, used when the shell has none
_TABLES_DEFAULT = "/home/smco502/datafiles/constants"


def _ensure_burp_tables() -> None:
    """Give burp2rdb its BUFR tables, or stop.

    burp2rdb reads table_b_bufr and tableburp from $CMCCONST (set by
    ordenv). Without them it still writes its files, with every value and
    every channel at 0 -- a silent failure. When $CMCCONST is not set, the
    official copy is used; when no table is found, the run stops."""
    if not os.environ.get("CMCCONST"):
        os.environ["CMCCONST"] = _TABLES_DEFAULT
        print(f"[INFO] CMCCONST was not set: using {_TABLES_DEFAULT}", flush=True)
    if not os.environ.get("AFSISIO"):
        os.environ["AFSISIO"] = os.path.dirname(os.path.dirname(os.environ["CMCCONST"]))
    need = ("table_b_bufr", "tableburp")
    lost = [n for n in need if not os.path.isfile(os.path.join(os.environ["CMCCONST"], n))]
    if lost:
        print(f"[CRITICAL] burp2rdb needs {', '.join(lost)} in $CMCCONST "
              f"({os.environ['CMCCONST']}), and they are not there: without them every "
              f"value would be converted as 0. Load ordenv, or set CMCCONST to the "
              f"folder of the CMC tables.", file=sys.stderr, flush=True)
        sys.exit(1)


def run_pikobsburp2db(args: argparse.Namespace) -> None:
    """Top-level orchestrator.
    Validates inputs, plans the (experience × family × date) task
    matrix, and dispatches the conversions through Dask.
    :param args: argparse namespace from :func:`arg_call`.
    """
    _ensure_burp_tables()
    # --- Resolve binary up-front ---------------------------------------
    burp_bin = _resolve_burp2rdb()
    if not burp_bin:
        log.critical("burp2rdb not found.\n%s", _SSM_HINT)
        sys.exit(1)
    log.info("Using burp2rdb at: %s", burp_bin)
    # Propagate to workers via env var (Dask Client uses os.environ).
    os.environ["BURP2RDB_BIN"] = burp_bin
    # --- Date range ----------------------------------------------------
    try:
        dt_start = datetime.datetime.strptime(args.datestart, "%Y%m%d%H")
        dt_end   = datetime.datetime.strptime(args.dateend,   "%Y%m%d%H")
    except ValueError:
        log.critical("Dates must be in YYYYMMDDHH format.")
        sys.exit(1)
    if dt_end < dt_start:
        log.critical("--dateend (%s) precedes --datestart (%s).",
                     args.dateend, args.datestart)
        sys.exit(1)
    # --- Output directory ---------------------------------------------
    # Three cases:
    #   1. Doesn't exist        → create it.
    #   2. Exists + force_clean → wipe and recreate.
    #   3. Exists + interactive → ask; on "yes" wipe; on "no" keep
    #      existing files (only missing ones will be (re)produced).
    #   4. Exists + parallel    → refuse, demand --force_clean.
    #
    # We use ignore_errors=True on rmtree to survive stale NFS handles
    # on CMC shared filesystems.
    if not os.path.exists(args.pathwork):
        log.info("Creating output directory: %s", args.pathwork)
        os.makedirs(args.pathwork, exist_ok=True)
    else:
        if args.force_clean:
            log.info("Wiping existing output directory: %s", args.pathwork)
            shutil.rmtree(args.pathwork, ignore_errors=True)
            os.makedirs(args.pathwork, exist_ok=True)
        elif args.n_cpus > 1:
            log.critical(
                "Output dir '%s' already exists. "
                "Use --force_clean (mandatory in parallel mode).",
                args.pathwork,
            )
            sys.exit(1)
        else:
            ans = input(f"[?] Output dir '{args.pathwork}' exists. "
                        f"Delete? (yes/no): ")
            if ans.strip().lower() == "yes":
                shutil.rmtree(args.pathwork, ignore_errors=True)
                os.makedirs(args.pathwork, exist_ok=True)
            else:
                log.info("Keeping existing files; only missing ones "
                         "will be produced.")
                # Make sure the directory really exists (race-safe).
                os.makedirs(args.pathwork, exist_ok=True)
    # --- Family list ---------------------------------------------------
    families = args.family or _detect_families(args.path_experience_files)
    if not families:
        log.critical("No families given and none auto-detected in inputs.")
        sys.exit(1)
    log.info("Processing %d families: %s",
             len(families), ", ".join(families))
    # --- Build task list ----------------------------------------------
    tasks: List[Tuple[str, str, str, str, str]] = []
    current = dt_start
    while current <= dt_end:
        fdate = current.strftime("%Y%m%d%H")
        for path_exp, name_exp in zip(args.path_experience_files,
                                      args.experience_name):
            exp_out_dir = os.path.join(args.pathwork, name_exp)
            os.makedirs(exp_out_dir, exist_ok=True)
            for family in families:
                tasks.append((
                    os.path.join(path_exp, f"{fdate}_{family}"),
                    name_exp,
                    family,
                    os.path.join(exp_out_dir, f"{fdate}_{family}"),
                    fdate,
                ))
        current += timedelta(hours=6)
    log.info("Total tasks: %d (%d dates × %d experiments × %d families)",
             len(tasks),
             ((dt_end - dt_start).total_seconds() // 21600) + 1,
             len(args.experience_name),
             len(families))
    # --- Run -----------------------------------------------------------
    if args.n_cpus <= 1:
        log.info("Sequential mode (n_cpus=%d)", args.n_cpus)
        results = [convert_single_file(*t) for t in tasks]
    else:
        log.info("Parallel mode with %d Dask workers", args.n_cpus)
        with Client(processes=True,
                    threads_per_worker=1,
                    n_workers=args.n_cpus,
                    silence_logs=50):
            results = list(dask.compute(
                *[dask.delayed(convert_single_file)(*t) for t in tasks]
            ))
    n_ok   = sum(1 for r in results if r)
    n_fail = len(results) - n_ok
    log.info("Done. %d successful, %d failed/skipped, total %d.",
             n_ok, n_fail, len(results))
    if n_fail > 0:
        # Non-zero exit so the PBS job is marked as failed but the user
        # still gets all the successful files.
        sys.exit(2)
# =============================================================================
# CLI
# =============================================================================
from pikobs.pbs_submit import maybe_submit_to_pbs
def arg_call() -> None:
   
    """Parse CLI arguments and dispatch to :func:`run_pikobsburp2db`."""
    parser = argparse.ArgumentParser(
        prog="pikobs-burp2rdb",
        description="Mass-convert BURP files to SQLite RDB databases.",
    )
    parser.add_argument("--path_experience_files", nargs="+", required=True,
                        help="One or more directories containing BURP files "
                             "named YYYYMMDDHH_<family>.")
    parser.add_argument("--experience_name", nargs="+", required=True,
                        help="One label per input directory (same length).")
    parser.add_argument("--pathwork", required=True,
                        help="Output directory (one subfolder per experience).")
    parser.add_argument("--datestart", required=True,
                        help="Start date YYYYMMDDHH (UTC).")
    parser.add_argument("--dateend",   required=True,
                        help="End date YYYYMMDDHH (UTC), inclusive.")
    parser.add_argument("--n_cpus", type=int, default=1,
                        help="Number of Dask workers (default: 1 = sequential).")
    parser.add_argument("--family", nargs="+", default=[],
                        help="Families to convert. Empty = auto-detect from inputs.")
    parser.add_argument("--force_clean", action="store_true",
                        help="Wipe the output directory if it already exists. "
                             "Mandatory when --n_cpus > 1.")
    parser.add_argument('--no_submit', action='store_true',
                   help="Skip PBS auto-submission and run locally.")
    args = parser.parse_args()
    if len(args.path_experience_files) != len(args.experience_name):
        log.critical(
            "Number of --path_experience_files (%d) does not match "
            "--experience_name (%d).",
            len(args.path_experience_files), len(args.experience_name),
        )
        sys.exit(1)
    args = parser.parse_args()
    maybe_submit_to_pbs(args)
    run_pikobsburp2db(args)
if __name__ == "__main__":
    arg_call()
