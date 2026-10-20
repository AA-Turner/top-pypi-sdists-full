"""
pikobs.special_family
=====================
Central registry for observation family metadata.

Provides:
  - DICT_CODTYP     : BUFR type code → long name
  - FAMILY_CODES    : family key → list of BUFR type codes
  - FAMILY_SPECIAL_COL : family key → special grouping column in header
  - Helper functions for label resolution and special-column handling
"""

from __future__ import annotations
from typing import Dict, List, Optional, Tuple


# ─────────────────────────────────────────────────────────────────────────────
# BUFR type codes → long names
# ─────────────────────────────────────────────────────────────────────────────

DICT_CODTYP: Dict[str, str] = {
     '12': 'SYNOP',         '13': 'SHIP',           '14': 'SYNOP MOBIL',
     '15': 'METAR',         '16': 'SPECI',           '18': 'DRIFTER',
     '32': 'PILOT',         '33': 'PILOT SHIP',      '34': 'PILOT MOBIL',
     '35': 'TEMP',          '36': 'TEMP SHIP',       '37': 'TEMP DROP',
     '38': 'TEMP MOBIL',    '42': 'AMDAR',           '128': 'AIREP',
    '134': 'PAOBS',        '135': 'TEMP + PILOT',   '136': 'TEMP + SYNOP',
    '139': 'TEMP SHIP + PILOT SHIP',                '143': 'SWOB-NONAUTO',
    '144': 'SWOB-AUTO',    '145': 'Patrol ship',    '146': 'ASYNOP',
    '147': 'BUOYS',        '148': 'SWOBNONAUTO-SPECIAL',
    '149': 'SWOBAUTO-SPECIAL',                      '157': 'BUFR',
    '159': 'TEMP PILOT MOBIL',                      '163': 'RADAR',
    '164': 'AMSUA',        '168': 'SSMIS',          '169': 'GPSRO',
    '177': 'ADS',          '181': 'AMSUB',          '182': 'MHS',
    '183': 'AIRS',         '185': 'CSR',             '186': 'IASI',
    '188': 'AMVS',         '189': 'GROUND BASED GPS',
    '192': 'ATMS',         '193': 'CRIS NSR',
    '195': 'constituants chimiques (remote)',
    '196': 'constituants chimiques (in-situ)',
    '198': 'NetWork of Network',
    '200': 'MWHS-2',       '202': 'CRIS FSR',       '254': 'SCAT',
}


# ─────────────────────────────────────────────────────────────────────────────
# Family → BUFR type codes
# ─────────────────────────────────────────────────────────────────────────────

FAMILY_CODES: Dict[str, List[str]] = {
    'ai':  ['42', '128', '157', '177'],
    'sf':  ['12', '13', '14', '15', '16', '18',
            '143', '144', '145', '146', '147', '148', '149', '198'],
    'gp':  ['189'],
    'csr': ['185'],
    'ua':  ['32', '33', '34', '35', '36', '37', '38', '135', '139'],
}


# ─────────────────────────────────────────────────────────────────────────────
# Family → special grouping column in header table
#
# Each entry defines:
#   column  : column name in the header SQLite table
#   title   : what the column is, as the viewers name its group
#   labels  : optional dict mapping column values to human-readable strings
#             (None = use the raw value as label)
#
# To add a new family:
#   'myfam': {'column': 'MY_COLUMN', 'title': 'Type',
#             'labels': {1: 'Type A', 2: 'Type B'}}
# ─────────────────────────────────────────────────────────────────────────────

FAMILY_SPECIAL_COL: Dict[str, Dict] = {
    'sw': {
        'column': 'WIND_COMP_METHOD',
        'title': 'Method',
        'labels': {
            1: 'IR channel',
            2: 'Visible channel',
            3: 'Water vapour channel',
            4: 'Multi-spectral',
            5: 'WV clear air',
            6: 'Ozone channel',
            7: 'WV cloud/clear unspecified',
        },
    },
    'ra': {
        'column': 'elevation',
        'title': 'Elevation',
        'labels': None,   # use raw elevation value as label
    },
}


# ─────────────────────────────────────────────────────────────────────────────
# Family → BUFR type codes (used to group id_stn by instrument type)
# ─────────────────────────────────────────────────────────────────────────────

FAMILY_CODES: Dict[str, List[str]] = {
    'ai':  ['42', '128', '157', '177'],
    'sf':  ['12', '13', '14', '15', '16', '18',
            '143', '144', '145', '146', '147', '148', '149', '198'],
    'gp':  ['189'],
    'csr': ['185'],
    'ua':  ['32', '33', '34', '35', '36', '37', '38', '135', '139'],
}


# ─────────────────────────────────────────────────────────────────────────────
# Helper functions
# ─────────────────────────────────────────────────────────────────────────────

def codtyp_label(id_stn: str) -> str:
    """Return a human-readable label for an id_stn value.

    If id_stn starts with a numeric code present in DICT_CODTYP
    (e.g. '35_XXXXX') returns 'TEMP (35_XXXXX)'.
    Otherwise returns id_stn unchanged.
    """
    code = str(id_stn).strip()
    if code in DICT_CODTYP:
        return f"{DICT_CODTYP[code]} ({code})"
    for c, name in DICT_CODTYP.items():
        if code.startswith(c + '_') or code.startswith(c + ' '):
            return f"{name} ({code})"
    return code


def get_special_col(family: str) -> Optional[str]:
    """Return the special grouping column name for a family, or None."""
    entry = FAMILY_SPECIAL_COL.get(family)
    return entry['column'] if entry else None


def get_special_label(family: str, value) -> str:
    """Return the human-readable label for a special column value."""
    entry = FAMILY_SPECIAL_COL.get(family)
    if entry is None:
        return str(value)
    labels = entry.get('labels')
    if labels is None:
        return str(value)
    try:
        return labels.get(int(value), str(value))
    except (ValueError, TypeError):
        return str(value)


def has_codtyp_groups(family: str) -> bool:
    """Return True if this family should be grouped by CODTYP."""
    return family in FAMILY_CODES



# ─────────────────────────────────────────────────────────────────────────────
# The special column in a query, for every module
# ─────────────────────────────────────────────────────────────────────────────

def special_select(family: str, head_cols, enabled: bool,
                   prefix: str = "") -> Tuple[str, str]:
    """(SELECT expression, GROUP BY term) of the family's special column.

    For sw that is WIND_COMP_METHOD, which separates the infrared from the
    water-vapour winds: two populations with different errors, whose sum
    would hide both. When it is off, or the column is not in the file,
    every row goes to the constant 'all' -- grouping by a constant changes
    no group, so a module gives the same numbers as without it.
    """
    col = get_special_col(family)
    cols = {str(c).lower() for c in head_cols or ()}
    # the radar elevation: the column its files carry, to a tenth of a
    # degree -- the same text in every module (0.5, not 0.400000005960464)
    if enabled and col and col.lower() == 'elevation':
        if radar_elevation_column(head_cols) is None:
            return "'all'", ""
        expr = radar_elevation_select(head_cols, prefix)
        return expr, expr
    if not enabled or not col or col.lower() not in cols:
        return "'all'", ""
    ref = f"{prefix}{col}" if prefix else col
    return f"CAST({ref} AS TEXT)", ref


def special_label(family: str, value) -> str:
    """The name of a value: IR / WV for sw, the value itself otherwise,
    'all' when the column is not split."""
    if value in (None, 'all'):
        return 'all'
    try:
        f = float(value)
    except (TypeError, ValueError):
        return str(value)
    # a code is an integer (1, IR channel); an elevation of 0.5 degree
    # stays 0.5, it is not rounded to another one
    if not f.is_integer():
        return str(value)
    try:
        return str(get_special_label(family, int(f)))
    except Exception:
        return str(value)



def special_title(family: str) -> str:
    """What the special column of a family is called: Method for sw,
    Elevation for ra; the column name when the table gives no title."""
    entry = FAMILY_SPECIAL_COL.get(family) or {}
    return (entry.get('title')
            or str(entry.get('column') or 'Special').replace('_', ' ').title())


def special_key_label(families) -> str:
    """The name of the special group in a viewer holding these families:
    the one title when they share it, all of them otherwise."""
    titles = sorted({special_title(f) for f in families
                     if f in FAMILY_SPECIAL_COL})
    if len(titles) == 1:
        return titles[0]
    return "Special" + (f" ({', '.join(titles)})" if titles else "")



# ─────────────────────────────────────────────────────────────────────────────
# The radar elevation
# ─────────────────────────────────────────────────────────────────────────────

# The antenna elevation of a radar observation. The files have named it
# three ways; the first one a file carries is used.
RADAR_ELEVATION_COLUMNS = ('NOMINAL_PPI_ELEVATION', 'CENTER_ELEVATION',
                           'ELEVATION')


def radar_elevation_column(head_cols) -> Optional[str]:
    """The elevation column of a radar file, or None when it has none."""
    cols = {str(c).upper() for c in head_cols or ()}
    return next((c for c in RADAR_ELEVATION_COLUMNS if c in cols), None)


def radar_elevation_select(head_cols, prefix: str = "") -> str:
    """The elevation of a radar observation as text, to a tenth of a
    degree: '0.5', '1.5'. Every observation of a sweep lands in the same
    group, and that text names its figures, its colour and its line in the
    calibration table. 'na' when the file has no elevation."""
    col = radar_elevation_column(head_cols)
    return f"printf('%.1f', {prefix}{col})" if col else "'na'"


# ─────────────────────────────────────────────────────────────────────────────
# The themes of obsscorecard
# ─────────────────────────────────────────────────────────────────────────────

# The surface stations at sea, by codtyp: SHIP, DRIFTER, Patrol ship, BUOYS.
# Every other codtyp of sf is a station on land.
SF_SEA_CODES: List[str] = ['13', '18', '145', '147']
SF_LAND_CODES: List[str] = [c for c in FAMILY_CODES['sf'] if c not in SF_SEA_CODES]

# One scorecard per theme; a theme is a list of rows, each a family and the
# BUFR codes it is scored on. ``combine``:
#   scalar   one variable (temperature, ZTD ...): its bias and sigma
#   vector   the two components of a wind, as one: the sigma of the vector
#            sqrt((var_u + var_v) / 2) and the length of the mean vector
#   channels a family of channels: the sigma, the channels pooled by their
#            counts, and the number of observations used -- no bias, which
#            the bias correction takes away
# ``codtyp`` keeps only the observations of those types, and ``block`` names
# the rows on the card instead of the family (land stations, ships and
# buoys). ``column: True`` puts a row in the column of the families with no height
# (a total column has none, whatever its vcoord says). A family missing
# from a run's directory is left out, and said; a row of the card shows
# only the layers its family reaches.
SCORECARD_THEMES: Dict[str, List[Dict]] = {
    'winds': [
        {'family': 'ua',    'label': 'wind',        'varnos': [11003, 11004], 'combine': 'vector'},
        {'family': 'ai',    'label': 'wind',        'varnos': [11003, 11004], 'combine': 'vector'},
        {'family': 'sw',    'label': 'wind',        'varnos': [11003, 11004], 'combine': 'vector'},
        {'family': 'radar', 'label': 'radial wind', 'varnos': [21014],        'combine': 'scalar'},
    ],
    'thermodynamics': [
        {'family': 'ua', 'label': 'temperature',    'varnos': [12001], 'combine': 'scalar'},
        {'family': 'ua', 'label': 'dew-point depr.', 'varnos': [12192], 'combine': 'scalar'},
        {'family': 'ai', 'label': 'temperature',    'varnos': [12001], 'combine': 'scalar'},
    ],
    # everything observed at the surface (or over the whole column), on a
    # card of its own: one column per region instead of empty layers; the
    # land stations and the ships and buoys apart, their errors differ
    'surface': [
        # by variable, the kinds of station of each one together
        *[{'family': 'sf', 'block': block, 'codtyp': codes, **row}
          for row in ({'label': 'temperature 2 m',     'varnos': [12004], 'combine': 'scalar'},
                      {'label': 'dew-point depr. 2 m', 'varnos': [12203], 'combine': 'scalar'},
                      {'label': 'surface pressure',    'varnos': [10004], 'combine': 'scalar'})
          for block, codes in (('Land stations', SF_LAND_CODES),
                               ('Ships and buoys', SF_SEA_CODES))],
        {'family': 'gp', 'block': 'Ground-based GPS', 'label': 'zenith delay',
         'varnos': [15031], 'combine': 'scalar'},
        *[{'family': 'sf', 'block': block, 'codtyp': codes, 'label': 'wind 10 m',
           'varnos': [11215, 11216], 'combine': 'vector'}
          for block, codes in (('Land stations', SF_LAND_CODES),
                               ('Ships and buoys', SF_SEA_CODES))],
        {'family': 'sc', 'block': 'Scatterometers', 'label': 'wind 10 m',
         'varnos': [11215, 11216], 'combine': 'vector'},
    ],
    # the profiles that reach the stratosphere, together
    'ro_ch': [
        {'family': 'ro', 'label': 'refractivity',   'varnos': [15036], 'combine': 'scalar'},
        {'family': 'ch', 'label': 'mixing ratio', 'varnos': [15008], 'combine': 'scalar'},
        {'family': 'ch', 'label': 'total column', 'varnos': [15198], 'combine': 'scalar',
         'column': True},
    ],
    'radiances': [
        {'family': f, 'label': 'Tb', 'varnos': [12163], 'combine': 'channels'}
        for f in ('to_amsua', 'to_amsub', 'atms', 'mwhs2', 'ssmis', 'iasi', 'cris', 'csr')
    ],
}


def scorecard_families(themes=None) -> List[str]:
    """Every family the themes read, each once, in the order of the themes."""
    themes = themes or list(SCORECARD_THEMES)
    return list(dict.fromkeys(r['family'] for t in themes for r in SCORECARD_THEMES[t]))
