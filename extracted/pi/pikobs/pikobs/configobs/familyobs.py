"""Per-family configuration: what to read, and how the vertical axis works.

``family(name)`` returns the six values every Pikobs module unpacks::

    FAM, VCOORD, VCOCRIT, STATB, elem, VCOTYP = pikobs.family('sw')

FAM
    label of the family in the figures.
VCOORD
    SQL expression giving the vertical coordinate. It is an expression,
    not a column: ``sw`` rounds the pressure to 2000 Pa and ``ua`` to
    20000 Pa, which is what makes their levels a short list instead of a
    continuum. Always read it through this, never ``vcoord`` directly, or
    a module ends up with thousands of levels where the others have
    tens.
VCOCRIT
    extra SQL criteria of the family, appended to the WHERE clause.
    Starts with ``and`` when it is not empty.
STATB
    column holding the bias estimate, or a constant when the family has
    none.
elem
    the varnos of the family, comma separated.
VCOTYP
    what the vertical coordinate is: ``CANAL``, ``PRESSION``,
    ``HAUTEUR(metres)``, ``LATITUDE``, ``LEVEL`` or ``SURFACE``. A module
    reads it to decide whether the axis is a list of rows, whether it is
    inverted (pressure has the ground at the bottom), or whether there is
    no vertical axis at all.

What changed from the previous version, and why
-----------------------------------------------

* ``synop_b`` never defined ``elem`` and raised ``NameError`` on the
  return. It now has its varnos, the ones of a surface family.
* ``sc`` and ``radar`` returned an empty ``VCOORD``, which pastes an
  empty expression into the SQL and makes the query fail. They now
  return the constant used by the other families without a vertical
  coordinate.
* ``ua`` had ``round(vcoord/025000.)*02500``, which divides by 25000 and
  multiplies by 2500: the levels it produced were ten times too small.
  It was dead code, overwritten on the next line, and it is gone.
* Every other overwritten assignment is gone too. There were eight of
  them, and reading which one wins is exactly how the line above
  survived.
* ``gp`` is grouped by ``round(lat/10)*10``, a latitude band, while
  claiming ``SURFACE``. Its VCOTYP is now ``LATITUDE``, so a module does
  not invert the axis or label it as a height.
* An unknown family used to print and return ``None``, which then blew
  up in the caller's tuple unpacking, far from the cause. It now raises
  ``ValueError`` naming the family and listing the known ones.
* ``ch`` defined ``FONCTION``, ``FONCTION2`` and ``STN_IDS``, which are
  not returned and were dead. They are kept as comments next to the
  family, in case they are needed again.
"""

from typing import Dict, List, Tuple

__all__ = ["family", "families", "FAMILIES", "VCOTYP_CHANNEL",
           "VCOTYP_PRESSURE", "VCOTYP_HEIGHT", "VCOTYP_SURFACE",
           "VCOTYP_LEVEL", "VCOTYP_LATITUDE", "has_vertical_axis",
           "axis_is_inverted"]

VCOTYP_CHANNEL = 'CANAL'
VCOTYP_PRESSURE = 'PRESSION'
VCOTYP_HEIGHT = 'HAUTEUR(metres)'
VCOTYP_SURFACE = 'SURFACE'
VCOTYP_LEVEL = 'LEVEL'
VCOTYP_LATITUDE = 'LATITUDE'

# Families with no vertical coordinate group everything under this value,
# so the SQL stays valid and every module sees a single level.
NO_VCOORD = " 9999 "

# Radiances: the channel is the vertical coordinate, read as it comes.
_CHANNEL = dict(VCOORD="  vcoord ", VCOTYP=VCOTYP_CHANNEL,
                STATB="BIAS_CORR", VCOCRIT="  ", elem="12163")

# name -> configuration. The keys are every alias a family answers to.
FAMILIES: Dict[Tuple[str, ...], Dict[str, str]] = {

    # ---- conventional -----------------------------------------------
    ('ua', 'ua_qc'): dict(
        FAM="Radiosondes",
        VCOORD=" round(vcoord/2000.)*2000 ",
        VCOCRIT="    ",
        STATB=" 0.",
        elem="11004,11003,12001,12192",
        VCOTYP=VCOTYP_PRESSURE),

    ('ai', 'ai_qc', '012_ai.sqlite'): dict(
        FAM="AIRCRAFTS",
        VCOORD=" round(vcoord/2000.)*2000 ",
        VCOCRIT=" and vcoord > 00000 ",
        STATB="BIAS_CORR",
        elem="11004,11003,12001,12192",
        VCOTYP=VCOTYP_PRESSURE),

    ('sf', 'swobnchwos'): dict(
        FAM="Surface",
        VCOORD=" 10    ",
        VCOCRIT="  ",
        STATB="0. ",
        elem="11215,11216,10051,10004,12004,12203,11011,11012 ",
        VCOTYP=VCOTYP_SURFACE),

    ('synop_b',): dict(
        FAM="SHIPS",
        # was "'SURF'", a text literal where every module expects a
        # number, and it had no elem at all
        VCOORD=NO_VCOORD,
        VCOCRIT="    ",
        STATB="OBS_ERROR",
        elem="11215,11216,10051,10004,12004,12203,11011,11012",
        VCOTYP=VCOTYP_SURFACE),

    ('sc', 'sc_qc'): dict(
        FAM="SCATS",
        VCOORD=NO_VCOORD,          # was empty: invalid SQL
        VCOCRIT="      ",
        STATB="0. ",
        elem="11011,11012,11215,11216",
        VCOTYP=VCOTYP_SURFACE),

    ('gp', 'gp_qc', 'gpssfc_b'): dict(
        FAM="GBGPS",
        # grouped by latitude band, not by height: the label says so
        VCOORD=" round(lat/10)*10    ",
        VCOCRIT="  ",
        STATB="0. ",
        elem="15031 ",
        VCOTYP=VCOTYP_LATITUDE),

    ('ro', 'ro_qc', 'gpsocc'): dict(
        FAM="GPSRO",
        VCOORD=" round(vcoord/1000.)*1000 ",
        VCOCRIT="      ",
        STATB=" 0. ",
        elem="15036",
        VCOTYP=VCOTYP_HEIGHT),

    ('radar', 'ra'): dict(
        FAM="RADAR",
        VCOORD=NO_VCOORD,          # was empty: invalid SQL
        VCOCRIT="  ",
        STATB=" ",
        elem="21014",
        VCOTYP=VCOTYP_HEIGHT),

    ('sw', 'sw_qc', 'sw_polar', 'sw_polaireDB'): dict(
        FAM="AMVS",
        VCOORD=" round(vcoord/2000.)*2000 ",
        VCOCRIT="  ",
        STATB=" 0.",
        elem="11002,11004,11003",
        VCOTYP=VCOTYP_PRESSURE),

    ('ch', 'ch_db'): dict(
        FAM="OZONE",
        VCOORD="  vcoord    ",
        VCOCRIT='    ',
        STATB='    ',
        elem="15198,15008",
        VCOTYP=VCOTYP_LEVEL),
        # kept from the previous version, unused by any caller:
        #   FONCTION  = "(100.*omp/obsvalue)"
        #   FONCTION2 = "(omp*0.)"
        #   STN_IDS   = " id_stn in ('AURA-MLS') and vcoord = 100"

    # ---- radiances ---------------------------------------------------
    # RARS is a retransmission of the same instrument, so it shares the
    # configuration of the family it retransmits.
    ('to_amsua_qc', 'to_amsua', 'to_amsua_allsky', 'to_amsua_allsky_qc',
     'to_amsua_allsky_rars'): dict(FAM="AMSUA", **_CHANNEL),

    ('to_amsub_qc', 'to_amsub', 'to_amsub_allsky', 'to_amsub_allsky_qc',
     'to_amsub_allsky_rars'): dict(FAM="AMSUB", **_CHANNEL),

    ('mwhs2', 'mwhs2_qc', 'mwhs2_rars'): dict(FAM="MWHS2", **_CHANNEL),

    ('ssmis_qc', 'ssmis'): dict(FAM="SSMIS", **_CHANNEL),

    ('iasi', 'iasi_qc'): dict(FAM="IASI", **_CHANNEL),

    ('crisfsr1_qc', 'crisfsr2_qc', 'cris', 'crisfsr'): dict(
        FAM="CRISFSR", **_CHANNEL),

    ('atms_allsky', 'atms_allsky_qc', 'atms_qc', 'atms'): dict(
        FAM="ATMS", **_CHANNEL),

    ('csr', 'csr_qc'): dict(FAM="CSR", **_CHANNEL),
}

_BY_NAME: Dict[str, Dict[str, str]] = {
    name: cfg for names, cfg in FAMILIES.items() for name in names}


def families() -> List[str]:
    """Every family name that is recognised, sorted."""
    return sorted(_BY_NAME)


def family(famille: str) -> Tuple[str, str, str, str, str, str]:
    """Configuration of a family: FAM, VCOORD, VCOCRIT, STATB, elem, VCOTYP.

    :raises ValueError: for an unknown family. The previous version
        printed a message and returned ``None``, which then failed in the
        caller's tuple unpacking with no clue about which family it was.
    """
    cfg = _BY_NAME.get(str(famille))
    if cfg is None:
        raise ValueError(
            f"unknown family '{famille}'. Known families: "
            f"{', '.join(families())}")
    return (cfg['FAM'], cfg['VCOORD'], cfg['VCOCRIT'], cfg['STATB'],
            cfg['elem'], cfg['VCOTYP'])


def has_vertical_axis(vcotyp: str) -> bool:
    """Does this family have a vertical coordinate worth a panel?"""
    return str(vcotyp).upper() not in (VCOTYP_SURFACE, VCOTYP_LATITUDE)


def axis_is_inverted(vcotyp: str) -> bool:
    """Pressure reads with the ground at the bottom; the rest does not."""
    return str(vcotyp).upper() == VCOTYP_PRESSURE
