# -*- coding: utf-8 -*-
"""Names, aliases and crop parameters -- the single place text is normalised.

Three vocabularies have to line up before anything else in this package works:

1. the calendar workbook (``GlobalCM_2026-09-11.xlsx``): sheets ``Maize 1`` /
   ``Winter Wheat``, columns ``Country``, ``Name``, ``Key``;
2. the region shapefile (``Global_Regions_202609.shp``): ``ADM0_NAME``,
   ``Name``, ``Key``, ``CM_Group``;
3. geoprepare's extraction config, which matches a country by the *exact*
   string ``adm0_name.lower().replace(" ", "_")`` with no fuzzy fallback
   (``geoprepare/extract/extract_EO.py``, ``load_country_boundary``).

Every function that needs to compare two of those strings calls into this
module rather than rolling its own ``.lower().replace(...)``. The original
GEOGLAM code did the latter and ended up with two incompatible definitions of
the same helper; see ``DEVIATIONS.md``.
"""
from __future__ import annotations

import re
import unicodedata
from typing import NamedTuple, Optional

# U+00A0 NO-BREAK SPACE. Exactly one workbook row carries it (Timor-Leste), and
# it is invisible in every viewer, so it silently breaks an equality join.
NBSP = " "

_WS_RE = re.compile(r"\s+")


def denbsp(text: str) -> str:
    """Replace non-breaking (and other exotic) spaces with a plain space.

    ``unicodedata.normalize("NFKC", ...)`` maps U+00A0 and friends onto U+0020
    while leaving ordinary ASCII untouched, so this also catches the narrow and
    figure spaces that turn up in hand-edited workbooks.

    Anything that is not a string -- a NaN from a blank spreadsheet cell, which
    the shipped ``EWCM_2026-01-05.xlsx`` has several of -- becomes the empty
    string, so callers get a value they can test for rather than an
    ``AttributeError`` halfway through a sheet.
    """
    if not isinstance(text, str):
        return ""
    return unicodedata.normalize("NFKC", text.replace(NBSP, " "))


def clean_text(text: str) -> str:
    """Canonical display form: no exotic spaces, no runs of whitespace, no edges."""
    return _WS_RE.sub(" ", denbsp(text)).strip()


def normalize(text: str) -> str:
    """Canonical *comparison* form: ``clean_text`` lower-cased, spaces -> ``_``.

    Matches ``geoprepare.georegion._normalize`` for ordinary inputs while also
    surviving the NBSP and the double spaces that appear in these two files.
    Use this to join a calendar row to a polygon -- never to build a country
    slug for geoextract, which needs :func:`country_slug` instead.
    """
    return clean_text(text).lower().replace(" ", "_")


def country_slug(adm0_name: str) -> str:
    """The exact string geoextract expects in ``countries`` / ``countries.txt``.

    geoextract compares ``ADM0_NAME.str.lower().str.replace(" ", "_")`` against
    the configured country **verbatim** -- it does not strip, and it does not
    collapse runs of spaces. ``"Iran  (Islamic Republic of)"`` therefore has to
    become ``"iran__(islamic_republic_of)"``, double underscore and all, which
    is precisely what the existing agmet config carries. So this deliberately
    does NOT go through :func:`clean_text`; it only removes the NBSP, which
    would otherwise survive into a filename.
    """
    return denbsp(adm0_name).lower().replace(" ", "_")


# --------------------------------------------------------------------------
# Aliases: calendar workbook spelling -> region shapefile spelling
# --------------------------------------------------------------------------
# 572 of the 574 keys join on an exact (NBSP-cleaned) match. These are the two
# that do not. Both are single-region countries, so the region name differs in
# the same way the country name does and the key can simply be rebuilt.
COUNTRY_ALIASES: dict[str, str] = {
    "east_timor_(timor-leste)": "Timor-Leste",
    "gaza_&_the_west_bank": "Gaza Strip",
}

# Region ("Name") aliases, keyed on (normalised country, normalised name).
REGION_ALIASES: dict[tuple[str, str], str] = {
    ("east_timor_(timor-leste)", "east_timor_(timor-leste)"): "Timor-Leste",
    ("gaza_&_the_west_bank", "gaza_&_the_west_bank"): "Gaza Strip",
}


def resolve_country(name: str) -> str:
    """Map a calendar-workbook country onto its shapefile spelling."""
    return COUNTRY_ALIASES.get(normalize(name), clean_text(name))


def resolve_region(country: str, name: str) -> str:
    """Map a calendar-workbook region onto its shapefile spelling."""
    key = (normalize(country), normalize(name))
    return REGION_ALIASES.get(key, clean_text(name))


def build_key(region: str, country: str) -> str:
    """The join key both files use: ``"<Name> <Country>"``.

    Verified to hold for every row of ``Global_Regions_202609.shp`` and of
    every sheet of ``GlobalCM_2026-09-11.xlsx``.
    """
    return f"{clean_text(region)} {clean_text(country)}"


def resolve_key(country: str, name: str) -> str:
    """Alias-resolved join key for one calendar row."""
    return build_key(resolve_region(country, name), resolve_country(country))


# --------------------------------------------------------------------------
# Sheet names <-> (crop, season)
# --------------------------------------------------------------------------
# The current workbook titles sheets ``Maize 1`` / ``Winter Wheat``; the older
# AMISCM/EWCM workbooks used ``maize_1`` / ``winter_wheat``. Both parse here so
# the reference comparison in the test suite can run the same code over the old
# files.
_SHEET_RE = re.compile(r"^(?P<crop>.+?)[ _](?P<season>\d+)$")


class CropSeason(NamedTuple):
    crop: str
    season: int


def parse_sheet_name(sheet: str) -> CropSeason:
    """``"Maize 1"`` -> ``("maize", 1)``; ``"Winter Wheat"`` -> ``("winter_wheat", 1)``.

    A sheet with no trailing season number is season 1 (winter_wheat,
    spring_wheat, rangelands).
    """
    token = normalize(sheet)
    match = _SHEET_RE.match(token)
    if match:
        return CropSeason(match.group("crop"), int(match.group("season")))
    return CropSeason(token, 1)


def sheet_names_for_crop(sheet_names, crop: str) -> dict[int, str]:
    """Map ``season -> sheet name`` for one crop, over a workbook's sheet list."""
    wanted = normalize(crop)
    out: dict[int, str] = {}
    for sheet in sheet_names:
        parsed = parse_sheet_name(sheet)
        if parsed.crop == wanted:
            out[parsed.season] = str(sheet)
    return out


# --------------------------------------------------------------------------
# Crop parameters
# --------------------------------------------------------------------------
class CropParams(NamedTuple):
    """Thermal parameters for one crop.

    ``min_base_temp`` / ``max_base_temp`` clip the daily mean temperature
    before GDD is accumulated; ``min_gdd`` / ``max_gdd`` bound the accumulated
    GDD between the two remote-sensing transitions and are scaled by
    :data:`EXTRATROPICAL_GDD_SCALE` outside the tropics.
    """

    short: str
    min_base_temp: float
    max_base_temp: float
    max_gdd: float
    min_gdd: float
    trusted: bool = True


# Transcribed from GEOGLAM ``Code/base/constants.py::dict_crop``. Indices 4 and
# 5 of the original tuples are unreachable there (both `elif` branches test the
# same 'TODO' string) and nothing reads them, so they are dropped.
#
# ``trusted=False`` carries forward the source's own comment that the millet,
# sorghum and teff parameters are copies of maize's and are not correct.
CROP_PARAMS: dict[str, CropParams] = {
    "spring_wheat": CropParams("sw", 5, 25, 700, 500),
    "winter_wheat": CropParams("ww", 5, 30, 800, 500),
    "maize": CropParams("mz", 8, 25, 2000, 750),
    "rice": CropParams("rc", 10, 25, 1500, 750),
    "soybean": CropParams("sb", 10, 25, 1200, 600),
    "millet": CropParams("ml", 8, 25, 2000, 750, trusted=False),
    "sorghum": CropParams("sr", 8, 25, 2000, 750, trusted=False),
    "teff": CropParams("tf", 8, 25, 2000, 750, trusted=False),
}

# Crops present in the workbook that have no thermal parameters at all. Beans
# is new in GlobalCM_2026-09-11 and was never in the GEOGLAM table; rangelands
# has no phenological stage structure (codes 0/1 only). Both are skipped with a
# recorded reason rather than scored against borrowed numbers.
UNPARAMETERISED_CROPS: dict[str, str] = {
    "beans": "no thermal parameters (new crop in GlobalCM_2026-09-11)",
    "rangelands": "no growth stages (codes 0/1 only)",
}

EXTRATROPICAL_GDD_SCALE = 0.75


def crop_params(crop: str) -> Optional[CropParams]:
    """Thermal parameters for a crop, or ``None`` if it has none."""
    return CROP_PARAMS.get(normalize(crop))


def skip_reason_for_crop(crop: str) -> Optional[str]:
    """Why this crop cannot be scored, or ``None`` if it can."""
    key = normalize(crop)
    if key in CROP_PARAMS:
        return None
    return UNPARAMETERISED_CROPS.get(key, f"unknown crop {crop!r}")
