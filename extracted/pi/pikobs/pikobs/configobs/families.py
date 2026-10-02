# GENERATED -- this docstring is written by pikobs/build_doc/build_config.py.
# Edit that file and run ./pikobs_doc.sh; a change made here is lost.
r"""===========================================================
pikobs.configobs.families -- What to read, family by family
===========================================================

Every module starts the same way::

    FAM, VCOORD, VCOCRIT, STATB, ELEM, VCOTYP = pikobs.family('sw')

Those six values are the whole contract between a family and the rest of
pikobs: the label of the figures, the SQL expression of the vertical
coordinate, the extra criteria of the family, the column holding the bias
estimate, the varnos to read, and what kind of vertical axis it is.

The families
============

+--------------+------------------+----------+--------------------------------------------------------+
| Family       | Label            | Vertical | Varnos                                                 |
+==============+==================+==========+========================================================+
| ``ua``       | Radiosondes      | pressure | 11004, 11003, 12001, 12192                             |
+--------------+------------------+----------+--------------------------------------------------------+
| ``ai``       | Aircrafts        | pressure | 11004, 11003, 12001, 12192                             |
+--------------+------------------+----------+--------------------------------------------------------+
| ``sf``       | Surface          | surface  | 11215, 11216, 10051, 10004, 12004, 12203, 11011, 11012 |
+--------------+------------------+----------+--------------------------------------------------------+
| ``sc``       | Scatterometers   | surface  | 11011, 11012, 11215, 11216                             |
+--------------+------------------+----------+--------------------------------------------------------+
| ``gp``       | Ground-based GPS | latitude | 15031                                                  |
+--------------+------------------+----------+--------------------------------------------------------+
| ``ro``       | GPS-RO           | height   | 15036                                                  |
+--------------+------------------+----------+--------------------------------------------------------+
| ``radar``    | Radar            | height   | 21014                                                  |
+--------------+------------------+----------+--------------------------------------------------------+
| ``sw``       | AMVs             | pressure | 11002, 11004, 11003                                    |
+--------------+------------------+----------+--------------------------------------------------------+
| ``ch``       | Ozone            | pressure | 15198, 15008                                           |
+--------------+------------------+----------+--------------------------------------------------------+
| ``to_amsua`` | AMSU-A           | channel  | 12163                                                  |
+--------------+------------------+----------+--------------------------------------------------------+
| ``to_amsub`` | AMSU-B           | channel  | 12163                                                  |
+--------------+------------------+----------+--------------------------------------------------------+
| ``mwhs2``    | MWHS-2           | channel  | 12163                                                  |
+--------------+------------------+----------+--------------------------------------------------------+
| ``ssmis``    | SSMIS            | channel  | 12163                                                  |
+--------------+------------------+----------+--------------------------------------------------------+
| ``iasi``     | IASI             | channel  | 12163                                                  |
+--------------+------------------+----------+--------------------------------------------------------+
| ``cris``     | CrIS FSR         | channel  | 12163                                                  |
+--------------+------------------+----------+--------------------------------------------------------+
| ``atms``     | ATMS             | channel  | 12163                                                  |
+--------------+------------------+----------+--------------------------------------------------------+
| ``csr``      | CSR              | channel  | 12163                                                  |
+--------------+------------------+----------+--------------------------------------------------------+

One row per family, by the name ``FAMILY`` takes in a wrapper. The files it
has at each stage of the chain are in *From cutoff to postalt*, below.

A name is matched without regard to case, so ``sw_polaireDB`` and
``sw_polairedb`` are the same family. An unknown name raises an error
that lists the ones that exist, rather than failing later in someone
else's tuple unpacking.

RARS families -- the regional retransmission of an instrument -- share
the configuration of what they retransmit, so the table lists them with
it; in the figures they keep a label of their own (AMSU-A RARS), so a
figure never leaves in doubt which broadcast it shows.

From dbase to cutoff
====================

The files a module reads are the end of a chain. What arrives lands in
``dbase``, sorted by source -- ``remote/iasi``, ``surface/synop_b``,
``swob/ca`` -- and ``cutoff`` gathers it into the files the analysis
starts from, one per network: ``YYYYMMDDHH_sf_synop_b``. A ``_b`` marks
the BUFR broadcast of a network, no ``_b`` its text (TAC) broadcast; the
radiances all arrive in BUFR without saying it. From ``derialt`` on, the
networks of a family are joined -- ``ai_acars``, ``ai_amdar`` and the
others become ``ai``; the ``_qc`` files of ``evalalt`` carry the quality
control, and ``bgckalt`` and ``postalt`` hold the families the modules
read. A RARS broadcast keeps files of its own to the end -- ``mwhs2_rars``
next to ``mwhs2`` in postalt -- so it can be looked at apart from the
global data of its instrument.

**Satellites**

.. list-table::
   :header-rows: 1
   :widths: 34 26 40

   * - dbase
     - cutoff
     - Note
   * - ``remote/iasi``
     - ``iasi``
     -  
   * - ``remote/crisfsr``
     - ``crisfsr``
     -  
   * - ``remote/airs``
     - --
     - no cutoff file
   * - ``remote/csr``
     - ``csr``
     -  
   * - ``remote/ssmis``
     - ``ssmis``
     -  
   * - ``remote/ascat``
     - ``sc_ascat``
     -  
   * - ``remote/hscat``
     - ``sc_hscat``
     -  
   * - ``remote/satwinds/geo``
     - ``sw_geo``
     -  
   * - ``remote/satwinds/polar``
     - ``sw_polar``
     -  
   * - ``remote/tovs1b/mhs``
     - ``to_amsub``
     - renamed; MHS files are named after AMSU-B
   * - ``remote/tovs1b/amsua``
     - ``to_amsua``
     -  
   * - ``remote/rars/mhs``
     - ``rars_amsub``
     - renamed; MHS files are named after AMSU-B
   * - ``remote/rars/amsua``
     - ``rars_amsua``
     -  
   * - ``remote/rars/mwhs2``
     - ``rars_mwhs2``
     -  
   * - ``remote/gpsocc``
     - ``ro``
     -  
   * - ``remote/gpssfc``
     - ``gp``
     -  
   * - ``remote/gpssfc_b``
     - ``gp_b``
     -  
   * - ``remote/atms``
     - ``atms``
     -  

**Upper air**

.. list-table::
   :header-rows: 1
   :widths: 34 26 40

   * - dbase
     - cutoff
     - Note
   * - ``uprair/acars``
     - ``ai_acars``
     -  
   * - ``uprair/amdar``
     - ``ai_amdar``
     -  
   * - ``uprair/airep``
     - ``ai_airep``
     -  
   * - ``uprair/ads``
     - ``ai_ads``
     -  
   * - ``uprair/radiosonde``
     - ``ua_radiosonde``
     -  
   * - ``uprair/radiosonde_b``
     - ``ua_radiosonde_b``
     -  
   * - ``uprair/profiler``
     - --
     - no cutoff file; not assimilated for years and not planned

**Surface**

.. list-table::
   :header-rows: 1
   :widths: 34 26 40

   * - dbase
     - cutoff
     - Note
   * - ``surface/synop``
     - ``sf_synop``
     -  
   * - ``surface/synop_b``
     - ``sf_synop_b``
     -  
   * - ``surface/metar``
     - ``sf_metar``
     -  
   * - ``surface/buoy``
     - --
     - no cutoff file; equivalence being settled
   * - ``surface/buoy_b``
     - --
     - no cutoff file; equivalence being settled

**SWOB**

.. list-table::
   :header-rows: 1
   :widths: 34 26 40

   * - dbase
     - cutoff
     - Note
   * - ``swob/ca``
     - ``sf_ca``
     - assimilated
   * - ``swob/winide``
     - ``sf_winide``
     - assimilated
   * - ``swob/nchwos``
     - ``sf_hwos``
     - renamed; assimilated
   * - ``swob/ncawos``
     - ``sf_awos``
     - renamed; assimilated
   * - ``swob/non/bcforest``
     - ``sf_drifter``
     - several networks in one file; not assimilated; reception monitored
   * - ``swob/non/cocorahs``
     - ``sf_drifter``
     - several networks in one file; not assimilated; reception monitored
   * - ``swob/non/bctran``
     - ``sf_drifter``
     - several networks in one file; not assimilated; reception monitored
   * - ``swob/non/mnr``
     - ``sf_drifter``
     - several networks in one file; not assimilated; reception monitored
   * - ``swob/non/trca``
     - ``sf_drifter``
     - several networks in one file; not assimilated; reception monitored
   * - ``swob/non/grca``
     - ``sf_drifter``
     - several networks in one file; not assimilated; reception monitored
   * - ``swob/ra``
     - --
     - no cutoff file; network discontinued

**Chemistry**

.. list-table::
   :header-rows: 1
   :widths: 34 26 40

   * - dbase
     - cutoff
     - Note
   * - ``derialt/ch/gome2b``
     - ``ch_gome``
     -  
   * - ``derialt/ch/mls``
     - ``tar_ch_mlso3``
     - renamed
   * - ``derialt/ch/omi``
     - ``tar_ch_omto3``
     - renamed
   * - ``derialt/ch/ompsnm``
     - ``ch_omps_np``
     - to confirm: the nadir mapper is a total column (tc)
   * - ``derialt/ch/ompsnmb``
     - ``ch_omps_np``
     - several networks in one file; to confirm: the nadir mapper is a total column (tc)
   * - ``derialt/ch/ompsnmc``
     - ``ch_omps_tc``
     - several networks in one file
   * - ``derialt/ch/ompsnp``
     - ``ch_omps_tc``
     - to confirm: the nadir profiler is a profile (np)
   * - ``derialt/ch/tropomi``
     - ``tar_ch_tropomi``
     -  
   * - ``derialt/ch/subuv2``
     - --
     - no cutoff file; mission ended

The table lives in ``configobs/dbase_to_cutoff.csv``: a network that moves
is one line there.

From cutoff to postalt
======================

From ``cutoff`` on, every stage writes one file per name and cycle, and the
names of a family keep its start -- ``sf_synop_b`` in cutoff, ``sf`` in
postalt -- which is what puts them on one row below. The table is one cycle
of G2: ``cutoff`` and ``derialt`` from the banco of the suite, ``evalalt``,
``bgckalt`` and ``postalt`` from ``monitoring/banco``, the SQLite files the
modules read. It is written by ``pikobs/build_doc/make_chain_csv.py`` into
``configobs/cutoff_to_postalt.csv``; run it again when the chain changes.

.. list-table::
   :header-rows: 1
   :widths: 10 30 16 16 14 14

   * - Family
     - cutoff
     - derialt
     - evalalt
     - bgckalt
     - postalt
   * - **ai**
     - ``ai_acars``, ``ai_ads``, ``ai_airep``, ``ai_amdar``
     - ``ai``
     - ``ai_qc``
     - ``ai``
     - ``ai``
   * - **asr**
     - ``asr``
     - ``asr``
     - --
     - --
     - --
   * - **atms**
     - ``atms``, ``rars_atms``
     - ``atms``, ``rars_atms``
     - ``atms_allsky_qc``, ``atms_qc``
     - ``atms``, ``atms_allsky``
     - ``atms_allsky``
   * - **ch**
     - ``ch_gome``, ``ch_omps_np``, ``ch_omps_tc``, ``tar_ch_mlso3``, ``tar_ch_omto3``, ``tar_ch_tropomi``
     - ``ch_o3_gome2b``, ``ch_o3_mls``, ``ch_o3_omi``, ``ch_o3_ompsnm``, ``ch_o3_ompsnmb``, ``ch_o3_ompsnmc``, ``ch_o3_ompsnp``, ``ch_o3_tropomi``
     - --
     - ``ch``
     - ``ch``
   * - **cris**
     - ``crisfsr``
     - ``crisfsr``
     - ``crisfsr1_qc``, ``crisfsr2_qc``
     - ``cris``
     - ``cris``
   * - **csr**
     - ``csr``
     - ``csr``
     - ``csr_qc``
     - ``csr``
     - ``csr``
   * - **gp**
     - ``gp``, ``gp_b``
     - ``gp``, ``gp2``
     - ``gp_qc``
     - ``gp``
     - ``gp``
   * - **iasi**
     - ``iasi``
     - ``iasi``
     - ``iasi_qc``
     - ``iasi``
     - ``iasi``
   * - **mwhs2**
     - ``mwhs2``, ``rars_mwhs2``
     - ``mwhs2``, ``rars_mwhs2``
     - ``mwhs2_qc``, ``mwhs2_rars_qc``
     - ``mwhs2``, ``mwhs2_rars``
     - ``mwhs2``, ``mwhs2_rars``
   * - **pr**
     - ``pr``
     - --
     - --
     - --
     - --
   * - **ro**
     - ``ro``
     - ``ro``
     - ``ro_qc``
     - ``ro``
     - ``ro``
   * - **sc**
     - ``sc_ascat``, ``sc_hscat``
     - ``sc``
     - ``sc_qc``
     - ``sc``
     - ``sc``
   * - **sf**
     - ``sf_awos``, ``sf_ca``, ``sf_drifter``, ``sf_drifter_b``, ``sf_hwos``, ``sf_metar``, ``sf_synop``, ``sf_synop_b``, ``sf_winide``
     - ``sf``, ``sf2``, ``sf2_a``, ``sf2_b``, ``sf_a``, ``sf_b``
     - ``sf_qc``
     - ``sf``
     - ``sf``
   * - **ssmis**
     - ``ssmis``
     - ``ssmis``
     - ``ssmis_qc``
     - ``ssmis``
     - ``ssmis``
   * - **sw**
     - ``sw_geo``, ``sw_polar``
     - ``sw``
     - ``sw_polaireDB_qc``, ``sw_qc``
     - ``sw``, ``sw_polaireDB``
     - ``sw``, ``sw_polaireDB``
   * - **to_amsua**
     - ``rars_amsua``, ``to_amsua``
     - ``rars_amsua``, ``to_amsua``
     - ``to_amsua_allsky_qc``, ``to_amsua_allsky_rars_qc``, ``to_amsua_qc``
     - ``to_amsua``, ``to_amsua_allsky``, ``to_amsua_allsky_rars``
     - ``to_amsua_allsky``, ``to_amsua_allsky_rars``
   * - **to_amsub**
     - ``rars_amsub``, ``to_amsub``
     - ``rars_amsub``, ``to_amsub``
     - ``to_amsub_allsky_qc``, ``to_amsub_allsky_rars_qc``, ``to_amsub_qc``
     - ``to_amsub``, ``to_amsub_allsky``, ``to_amsub_allsky_rars``
     - ``to_amsub_allsky``, ``to_amsub_allsky_rars``
   * - **ua**
     - ``ua_cmc``, ``ua_radiosonde``, ``ua_radiosonde_b``
     - ``ua``, ``ua_a``, ``ua_b``
     - ``ua_qc``
     - ``ua``
     - ``ua``

The vertical coordinate
=======================

``VCOORD`` is an expression, not a column. This is what makes a family
have twenty levels rather than three hundred thousand, and it is why a
module must always read the coordinate through it. The rounding is
chosen so that each family gets a number of levels that reads well in
the modules that group by the vertical -- profile, zone, verifprofile,
the layers of scatter: about twenty pressure levels, one per kilometre
of height, one per channel. Families whose files carry no vertical
coordinate get a constant: 10 for observations at 10 m, 9999 for the
surface.

+--------------+----------------------------------+----------------------------------------------------------------------------------+
| Family       | VCOORD                           | What that gives                                                                  |
+==============+==================================+==================================================================================+
| ``ua``       | ``ROUND(VCOORD / 2000.) * 2000`` | pressure, grouped by ROUND(VCOORD / 2000.) * 2000                                |
+--------------+----------------------------------+----------------------------------------------------------------------------------+
| ``ai``       | ``ROUND(VCOORD / 2000.) * 2000`` | pressure, grouped by ROUND(VCOORD / 2000.) * 2000                                |
+--------------+----------------------------------+----------------------------------------------------------------------------------+
| ``sf``       | ``10``                           | no vertical coordinate in the files: every observation at 10 m, one level        |
+--------------+----------------------------------+----------------------------------------------------------------------------------+
| ``sc``       | ``9999``                         | no vertical coordinate in the files: every observation at the surface, one level |
+--------------+----------------------------------+----------------------------------------------------------------------------------+
| ``gp``       | ``ROUND(LAT / 10) * 10``         | band of latitude, grouped by ROUND(LAT / 10) * 10                                |
+--------------+----------------------------------+----------------------------------------------------------------------------------+
| ``ro``       | ``ROUND(VCOORD / 1000.) * 1000`` | height, grouped by ROUND(VCOORD / 1000.) * 1000                                  |
+--------------+----------------------------------+----------------------------------------------------------------------------------+
| ``radar``    | ``VCOORD``                       | height, grouped by VCOORD                                                        |
+--------------+----------------------------------+----------------------------------------------------------------------------------+
| ``sw``       | ``ROUND(VCOORD / 2000.) * 2000`` | pressure, grouped by ROUND(VCOORD / 2000.) * 2000                                |
+--------------+----------------------------------+----------------------------------------------------------------------------------+
| ``ch``       | ``VCOORD``                       | pressure, grouped by VCOORD                                                      |
+--------------+----------------------------------+----------------------------------------------------------------------------------+
| ``to_amsua`` | ``VCOORD``                       | one level per channel, grouped by VCOORD                                         |
+--------------+----------------------------------+----------------------------------------------------------------------------------+
| ``to_amsub`` | ``VCOORD``                       | one level per channel, grouped by VCOORD                                         |
+--------------+----------------------------------+----------------------------------------------------------------------------------+
| ``mwhs2``    | ``VCOORD``                       | one level per channel, grouped by VCOORD                                         |
+--------------+----------------------------------+----------------------------------------------------------------------------------+
| ``ssmis``    | ``VCOORD``                       | one level per channel, grouped by VCOORD                                         |
+--------------+----------------------------------+----------------------------------------------------------------------------------+
| ``iasi``     | ``VCOORD``                       | one level per channel, grouped by VCOORD                                         |
+--------------+----------------------------------+----------------------------------------------------------------------------------+
| ``cris``     | ``VCOORD``                       | one level per channel, grouped by VCOORD                                         |
+--------------+----------------------------------+----------------------------------------------------------------------------------+
| ``atms``     | ``VCOORD``                       | one level per channel, grouped by VCOORD                                         |
+--------------+----------------------------------+----------------------------------------------------------------------------------+
| ``csr``      | ``VCOORD``                       | one level per channel, grouped by VCOORD                                         |
+--------------+----------------------------------+----------------------------------------------------------------------------------+

Rounding the pressure to 2000 Pa suits the troposphere, where most
conventional observations are: it gives about twenty levels between the
ground and 200 hPa. Above that the levels grow coarse in relative terms,
so a run that cares about the stratosphere is better served by a family
that keeps its coordinate -- ``ch`` does, and so does ``radar``.

Each module prints what it groups by when it starts:

.. code-block:: text

   [zone] ua: pressure, grouped by ROUND(VCOORD / 2000.) * 2000
   [profile] radar: height, grouped by VCOORD

``VCOTYP`` says what the coordinate means, and the modules read it rather
than guessing from the family: ``PRESSION`` is drawn with the ground at
the bottom, ``CANAL`` is a list of channels, ``SURFACE`` and ``LATITUDE``
have no vertical axis at all. Two helpers save repeating that test:
:func:`has_vertical_axis` and :func:`axis_is_inverted`.

Stations of ai, sf, ua, gp and csr
==================================

For these families the station id is not what you want to group by. The
tokens are read as instrument types (``CODTYP`` column, names from
``DICT_CODTYP``), without regard to case:

.. list-table::
   :header-rows: 1
   :widths: 12 88

   * - Family
     - Instrument types (codtyp)
   * - ``ai``
     - AMDAR (42), AIREP (128), BUFR (157), ADS (177)
   * - ``sf``
     - SYNOP (12), SHIP (13), SYNOP MOBIL (14), METAR (15), SPECI (16), DRIFTER (18), SWOB-NONAUTO (143), SWOB-AUTO (144), Patrol ship (145), ASYNOP (146), BUOYS (147), SWOBNONAUTO-SPECIAL (148), SWOBAUTO-SPECIAL (149), NetWork of Network (198)
   * - ``ua``
     - PILOT (32), PILOT SHIP (33), PILOT MOBIL (34), TEMP (35), TEMP SHIP (36), TEMP DROP (37), TEMP MOBIL (38), TEMP + PILOT (135), TEMP SHIP + PILOT SHIP (139)
   * - ``gp``
     - GROUND BASED GPS (189)
   * - ``csr``
     - CSR (185)

A name matches every codtyp that *starts* with it: ``temp`` takes TEMP,
TEMP SHIP, TEMP DROP, TEMP MOBIL and the combined TEMP + PILOT types.
Use ``=TEMP`` or ``35`` for land radiosondes only. Spaces in names are
written ``_`` because bash splits on spaces. Only codtyps present in the
data are considered, and the log shows how each token was read:

.. code-block:: text

   [scatter] ua: id_stn 'pilot' -> PILOT (32), PILOT SHIP (33), PILOT MOBIL (34)
   [scatter] ua: id_stn 'CYUL' -> no codtyp name matches, used as station id prefix
   [scatter] WARNING ua: id_stn 'xyz*' matches no data for the selected channel(s), no map produced

Reading a family from code
==========================

.. code-block:: python

   from pikobs.configobs import families

   families.family('iasi')            # the six values
   families.family_varnos('ua')       # [11004, 11003, 12001, 12192]
   families.families_of_varno(12163)  # every family that reads it
   families.level_summary('ua')       # the line the modules print
   families.families()                # every name recognised
"""

from typing import Dict, List, Tuple

__all__ = ["family", "families", "FAMILIES", "VCOTYP_CHANNEL",
           "VCOTYP_PRESSURE", "VCOTYP_HEIGHT", "VCOTYP_SURFACE",
           "VCOTYP_LATITUDE", "has_vertical_axis", "axis_is_inverted",
           "level_summary", "family_varnos", "families_of_varno"]

VCOTYP_CHANNEL = 'CANAL'
VCOTYP_PRESSURE = 'PRESSION'
VCOTYP_HEIGHT = 'HAUTEUR(metres)'
VCOTYP_SURFACE = 'SURFACE'
VCOTYP_LATITUDE = 'LATITUDE'

# A family with no vertical coordinate groups everything under this value,
# so the SQL stays valid and every module sees a single level.
NO_VCOORD = " 9999 "

# Conventional profiles and AMVs: the pressure rounded to 2000 Pa, which
# gives about twenty levels through the troposphere. The modules print
# what they group by when they start, so the choice is never a surprise.
_PRESSURE_2000 = " ROUND(VCOORD / 2000.) * 2000 "

# Radiances: the channel is the vertical coordinate, read as it comes.
_CHANNEL = dict(VCOORD=" VCOORD ", VCOTYP=VCOTYP_CHANNEL,
                STATB="BIAS_CORR", VCOCRIT="  ", ELEM="12163")

# name -> configuration. The keys are every alias a family answers to.
FAMILIES: Dict[Tuple[str, ...], Dict[str, str]] = {

    # ---- conventional -------------------------------------------------
    ('ua', 'ua_qc'): dict(
        FAM="Radiosondes",
        VCOORD=_PRESSURE_2000,
        VCOCRIT="  ",
        STATB=" 0. ",
        ELEM="11004,11003,12001,12192",
        VCOTYP=VCOTYP_PRESSURE),

    ('ai', 'ai_qc', '012_ai.sqlite'): dict(
        FAM="Aircrafts",
        VCOORD=_PRESSURE_2000,
        VCOCRIT=" AND VCOORD > 0 ",
        STATB="BIAS_CORR",
        ELEM="11004,11003,12001,12192",
        VCOTYP=VCOTYP_PRESSURE),

    ('sf', 'swobnchwos'): dict(
        FAM="Surface",
        VCOORD=" 10 ",
        VCOCRIT="  ",
        STATB=" 0. ",
        ELEM="11215,11216,10051,10004,12004,12203,11011,11012",
        VCOTYP=VCOTYP_SURFACE),

    ('sc', 'sc_qc'): dict(
        FAM="Scatterometers",
        VCOORD=NO_VCOORD,
        VCOCRIT="  ",
        STATB=" 0. ",
        ELEM="11011,11012,11215,11216",
        VCOTYP=VCOTYP_SURFACE),

    ('gp', 'gp_qc', 'gpssfc_b'): dict(
        FAM="Ground-based GPS",
        # grouped by band of latitude, not by height: VCOTYP says so, and
        # a module reading it does not invert the axis or call it a height
        VCOORD=" ROUND(LAT / 10) * 10 ",
        VCOCRIT="  ",
        STATB=" 0. ",
        ELEM="15031",
        VCOTYP=VCOTYP_LATITUDE),

    ('ro', 'ro_qc', 'gpsocc'): dict(
        FAM="GPS-RO",
        VCOORD=" ROUND(VCOORD / 1000.) * 1000 ",
        VCOCRIT="  ",
        STATB=" 0. ",
        ELEM="15036",
        VCOTYP=VCOTYP_HEIGHT),

    ('radar', 'ra'): dict(
        FAM="Radar",
        # the beam height in metres, as it comes: a radar profile is
        # binned by the module that draws it, not here
        VCOORD=" VCOORD ",
        VCOCRIT="  ",
        STATB=" 0. ",
        ELEM="21014",
        VCOTYP=VCOTYP_HEIGHT),

    ('sw', 'sw_qc', 'sw_polar', 'sw_polairedb'): dict(
        FAM="AMVs",
        VCOORD=_PRESSURE_2000,
        VCOCRIT="  ",
        STATB=" 0. ",
        ELEM="11002,11004,11003",
        VCOTYP=VCOTYP_PRESSURE),

    ('ch', 'ch_db'): dict(
        FAM="Ozone",
        # the MLS levels are pressures in Pa, read as such, so the axis is
        # in hPa, inverted, and logarithmic over its four decades
        VCOORD=" VCOORD ",
        VCOCRIT="  ",
        STATB=" 0. ",
        ELEM="15198,15008",
        VCOTYP=VCOTYP_PRESSURE),

    # ---- radiances ----------------------------------------------------
    ('to_amsua', 'to_amsua_qc', 'to_amsua_allsky', 'to_amsua_allsky_qc'):
        dict(FAM="AMSU-A", **_CHANNEL),

    ('to_amsub', 'to_amsub_qc', 'to_amsub_allsky', 'to_amsub_allsky_qc'):
        dict(FAM="AMSU-B", **_CHANNEL),

    ('mwhs2', 'mwhs2_qc'): dict(FAM="MWHS-2", **_CHANNEL),

    ('ssmis', 'ssmis_qc'): dict(FAM="SSMIS", **_CHANNEL),

    ('iasi', 'iasi_qc'): dict(FAM="IASI", **_CHANNEL),

    ('cris', 'crisfsr', 'crisfsr1_qc', 'crisfsr2_qc'): dict(
        FAM="CrIS FSR", **_CHANNEL),

    ('atms', 'atms_qc', 'atms_allsky', 'atms_allsky_qc'): dict(
        FAM="ATMS", **_CHANNEL),

    ('csr', 'csr_qc'): dict(FAM="CSR", **_CHANNEL),

    # ---- RARS ---------------------------------------------------------
    # The same instrument, retransmitted regionally: same channels, same
    # varno, and a label of its own so a figure never leaves in doubt
    # whether it shows the direct broadcast or the retransmission.
    ('to_amsua_allsky_rars',): dict(FAM="AMSU-A RARS", **_CHANNEL),
    ('to_amsub_allsky_rars',): dict(FAM="AMSU-B RARS", **_CHANNEL),
    ('mwhs2_rars',): dict(FAM="MWHS-2 RARS", **_CHANNEL),
}

_BY_NAME: Dict[str, Dict[str, str]] = {
    name.lower(): cfg for names, cfg in FAMILIES.items() for name in names}
_ALIASES: Dict[str, Tuple[str, ...]] = {
    names[0]: names for names in FAMILIES}


def families() -> List[str]:
    """Every family name that is recognised, sorted."""
    return sorted(_BY_NAME)


def family(famille: str) -> Tuple[str, str, str, str, str, str]:
    """Configuration of a family: FAM, VCOORD, VCOCRIT, STATB, ELEM, VCOTYP.

    :raises ValueError: for an unknown family, naming it and listing the
        ones that exist.
    """
    cfg = _BY_NAME.get(str(famille).lower())
    if cfg is None:
        raise ValueError(
            f"unknown family '{famille}'. Known families: "
            f"{', '.join(families())}")
    return (cfg['FAM'], cfg['VCOORD'], cfg['VCOCRIT'], cfg['STATB'],
            cfg['ELEM'], cfg['VCOTYP'])


def family_varnos(famille: str) -> List[int]:
    """The varnos of a family, as integers."""
    return [int(v) for v in family(famille)[4].split(',') if v.strip()]


def families_of_varno(varno) -> List[str]:
    """Every family that reads this varno, by its first name."""
    out = []
    for names, cfg in FAMILIES.items():
        if str(varno) in [v.strip() for v in cfg['ELEM'].split(',')]:
            out.append(names[0])
    return sorted(out)


def has_vertical_axis(vcotyp: str) -> bool:
    """Does this family have a vertical coordinate worth a panel?"""
    return str(vcotyp).upper() not in (VCOTYP_SURFACE, VCOTYP_LATITUDE)


def axis_is_inverted(vcotyp: str) -> bool:
    """Pressure reads with the ground at the bottom; the rest does not."""
    return str(vcotyp).upper() == VCOTYP_PRESSURE


def level_summary(famille: str) -> str:
    """One line saying how this family's levels are grouped.

    Every module prints it when it starts, so nobody has to guess why a
    family has twenty levels and another has three hundred.
    """
    fam, vcoord, _, _, _, vcotyp = family(famille)
    expr = " ".join(str(vcoord).split())
    kind = {VCOTYP_CHANNEL: "one level per channel",
            VCOTYP_PRESSURE: "pressure",
            VCOTYP_HEIGHT: "height",
            VCOTYP_LATITUDE: "band of latitude",
            VCOTYP_SURFACE: "no vertical axis"}.get(vcotyp, vcotyp)
    try:                          # a constant: every observation is on
        float(expr)               # the same level, whatever the number
        return f"{famille}: {kind}, every observation on one level"
    except ValueError:
        return f"{famille}: {kind}, grouped by {expr}"
