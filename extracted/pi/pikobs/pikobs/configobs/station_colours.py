"""The colour of a station or a satellite, the same in every figure.

A satellite listed here always gets its colour, and any two of them can be
told apart: the colours are not picked by eye but computed, so that the
closest pair of the palette is as far apart as possible as the eye sees it
(CIEDE2000 in CIELAB, 14.9 for the closest pair; two colours an eye barely
separates are about 2 apart). Only vivid colours of middle lightness are
used, the ones a dot keeps on the map. The first colours, the most apart,
go to the satellites that fly together most often: the three METOP, NPP
and the two JPSS, the NOAA of AMSU.

A name is compared without its dashes, spaces or case, so METOP-3, METOP3
and Metop-3 are one satellite. Any other station takes a colour of the same
palette by a hash of its name: always the same one for the same name.

Adding a satellite is one line in SATELLITES; take a colour of PALETTE that
no satellite flying with it uses.
"""

import re
from typing import Dict

# Twenty-eight colours, each as far as possible from the closest other one.
PALETTE = [
    "#006BA1", "#A1BC00", "#FF5100", "#FF36FF", "#28511B", "#861B43", "#00BCBC",
    "#794300", "#6B00E4", "#94AEF2", "#F294A1", "#D79400", "#51945E", "#BC000D",
    "#866BAE", "#797900", "#F20079", "#364386", "#00A1D7", "#00C943", "#C9A1E4",
    "#AE1B94", "#BC6B5E", "#E4A179", "#5179FF", "#AE6B28", "#367900", "#5E5100",
]

# Satellites: normalised name (no dashes, spaces or case) -> colour.
SATELLITES: Dict[str, str] = {
    # IASI, AMSU, MHS, AVHRR winds: the METOP
    "METOP1": "#006BA1", "METOP2": "#A1BC00", "METOP3": "#FF5100",
    # CrIS, ATMS, VIIRS: NPP and the JPSS
    "NOAA20": "#FF36FF", "NOAA21": "#28511B", "NPP": "#861B43",
    "SNPP": "#861B43", "SUOMINPP": "#861B43",
    # AMSU, MHS: the older NOAA
    "NOAA19": "#00BCBC", "NOAA18": "#794300", "NOAA15": "#6B00E4",
    # MODIS, AIRS, AMSR
    "AQUA": "#94AEF2", "TERRA": "#C9A1E4", "GCOMW1": "#AE1B94",
    # the geostationary ones: GOES, Meteosat, Himawari
    "GOES16": "#F294A1", "GOES17": "#00C943", "GOES18": "#D79400",
    "GOES19": "#51945E", "METEOSAT9": "#F20079", "METEOSAT10": "#BC000D",
    "METEOSAT11": "#364386", "METEOSAT12": "#866BAE", "HIMAWARI8": "#00A1D7",
    "HIMAWARI9": "#797900",
    # FY-3, DMSP
    "FY3D": "#BC6B5E", "FY3E": "#E4A179", "FY3F": "#5179FF",
    "DMSPF17": "#AE6B28", "DMSPF18": "#367900",
    # the names as the files of sw write them
    "HMWARI8": "#00A1D7", "HMWARI9": "#797900", "METSAT9": "#F20079",
    "METSAT10": "#BC000D", "METSAT11": "#364386", "METSAT12": "#866BAE",
    "METOP13": "#00BCBC",
    # GPS radio occultation (ro): colours the METOP and FY-3D of ro do not
    # use, so that the seventeen of the family can be told apart
    "COSM2E1": "#FF36FF", "COSM2E2": "#28511B", "COSM2E3": "#861B43",
    "COSM2E4": "#00BCBC", "COSM2E5": "#794300", "COSM2E6": "#6B00E4",
    "GNOMES": "#94AEF2", "LEMUR3U": "#F294A1", "YAMLBOW": "#D79400",
    "PAZ": "#51945E", "SEN6A": "#BC000D", "TERRASARX": "#866BAE",
    "TANDEMX": "#797900", "GRACEC": "#F20079", "GRACED": "#364386",
    "SPIRE": "#00A1D7", "KOMPSAT5": "#00C943",
}


def _norm(name: str) -> str:
    return re.sub(r"[^A-Z0-9]", "", str(name).upper())


def _fnv1a_32(text: str) -> int:
    h = 0x811C9DC5
    for ch in text:
        h = ((h ^ ord(ch)) * 0x01000193) & 0xFFFFFFFF
    return h


def station_colour(name: str) -> str:
    """The colour of a station: from SATELLITES when it is one, else from
    PALETTE by a hash of its name -- always the same for the same name."""
    key = _norm(name)
    if key in SATELLITES:
        return SATELLITES[key]
    return PALETTE[_fnv1a_32(key) % len(PALETTE)]
