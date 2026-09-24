"""Generate the four-file geoprepare config for the crop-calendar-region extract.

145 countries, each needing its own section, is not a hand-editing job -- and
two of geoextract's failure modes here are silent:

* a country listed in ``geoextract.txt`` ``countries`` with **no section** in
  ``countries.txt`` raises ``NoSectionError`` before any work starts, because
  ``[DEFAULT]`` inheritance does not create a section;
* the country is matched against ``ADM0_NAME`` by an exact
  ``lower().replace(" ", "_")`` with no fuzzy fallback, and a non-match yields
  an **empty** frame rather than an error -- zero files, run reports success.

So every slug is derived from the prepared shapefile itself, and a section is
emitted for every country unconditionally. Crop lists come from the calendar
workbook's active (non ``-1``) rows, so a country is only asked for crops it
actually grows.

Usage::

    python -m geocif.data_prep.make_cropcal_config \
        --lookup  ".../cropcal_audit/calendar_regions_lookup.csv" \
        --calendar ".../crop_calendars/GlobalCM_2026-09-11.xlsx"
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd

from geocif.cropcal import calendar as cropcal_calendar
from geocif.cropcal import naming

DEFAULT_CONFIG_ROOT = Path(r"D:/Users/ritvik/projects/GEO/config")
DEFAULT_TEMPLATE = DEFAULT_CONFIG_ROOT / "agmet" / "geobase.txt"

PROJECT = "cropcal"
BOUNDARY_FILE = "Global_Regions_202609.shp"
BOUNDARY_STEM = "Global_Regions_202609"
# The geomerge-schema copy written by convert_calendar_for_geomerge.py.
# geoprepare needs sheets named `maize_1` and a `country2` column, and skips
# every combination without them -- silently, as a logged error. geocif's own
# reader accepts either schema, so one file serves both.
CALENDAR_FILE = "GlobalCM_2026-09-11_geomerge.xlsx"

#: NDVI plus the two CHIRTS-ERA5 temperature fields the GDD accumulation needs.
#: The rule-based validator uses ONLY those three -- a vegetation index and air
#: temperature. The rest are extracted for the model comparison and for
#: diagnosing disagreements (is a late satellite greenup a wet-season onset
#: effect, a moisture limit, or a stress signal?), not by the ported algorithm.
EO_MODEL = [
    "ndvi",
    "chirts_era5_tmax",
    "chirts_era5_tmin",
    "chirps",          # daily precipitation, CHIRPS v3 (see geobase [CHIRPS])
    "esi_4wk",         # evaporative stress index, 4-week composite, weekly
    "nsidc_surface",   # soil moisture, surface layer
    "nsidc_rootzone",  # soil moisture, root zone
]

START_YEAR, END_YEAR = 2015, 2026

#: Per-crop masks that already exist in dir_crop_masks, reused from agmet.
#: Crops with no dedicated mask fall back to generic cropland.
CROP_MASKS = {
    "winter_wheat": "Percent_Winter_Wheat.tif",
    "spring_wheat": "Percent_Spring_Wheat.tif",
    "maize": "Percent_Maize.tif",
    "soybean": "Percent_Soybean.tif",
    "rice": "Percent_Rice.tif",
}
FALLBACK_MASK = "cropland_v9.tif"

BOUNDARY_SECTION = """
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; Crop-calendar regions (GEOGLAM Crop Monitor, 2026-09).
; num_ID is assigned by geocif.data_prep.prepare_calendar_regions:
; geoextract REQUIRES an ADM_ID and drops the country silently without one.
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
[Global_Regions_202609]
adm0_col = ADM0_NAME
adm1_col = Name
id_col = num_ID

"""


def country_crops(calendar_path: Path) -> dict[str, dict]:
    """``country_slug -> {"name": ADM0_NAME, "crops": [...], "seasons": [...]}``.

    Only crops with at least one active row in that country, and only crops the
    validator can actually score (see ``naming.skip_reason_for_crop``).
    """
    out: dict[str, dict] = {}
    for crop_season, frame in cropcal_calendar.read_workbook(calendar_path).items():
        if naming.skip_reason_for_crop(crop_season.crop):
            continue
        codes = frame[cropcal_calendar.code_columns(frame)].to_numpy(dtype=float)
        active = ~np.all(codes == cropcal_calendar.CODE_NOT_GROWN, axis=1)
        for slug, name in zip(
            frame.loc[active, "country_slug"], frame.loc[active, "country"]
        ):
            entry = out.setdefault(slug, {"name": name, "crops": set(), "seasons": set()})
            entry["crops"].add(crop_season.crop)
            entry["seasons"].add(crop_season.season)
    for entry in out.values():
        entry["crops"] = sorted(entry["crops"])
        entry["seasons"] = sorted(entry["seasons"])
    return out


def _py_list(values) -> str:
    return "[" + ", ".join(f"'{v}'" for v in values) + "]"


def write_geobase(template: Path, out_path: Path) -> None:
    """agmet's geobase plus the new boundary-column section."""
    text = template.read_text(encoding="utf-8")
    if f"[{BOUNDARY_STEM}]" not in text:
        marker = "[LOGGING]"
        insert_at = text.index(marker) if marker in text else len(text)
        text = text[:insert_at] + BOUNDARY_SECTION + text[insert_at:]
    out_path.write_text(text, encoding="utf-8")


def write_countries(entries: dict[str, dict], out_path: Path) -> None:
    lines = [
        ";;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;",
        ";;  Crop-calendar-region extraction -- GENERATED FILE, do not hand-edit.    ;;",
        ";;  Rebuild: python -m geocif.data_prep.make_cropcal_config                 ;;",
        ";;                                                                          ;;",
        ";;  Every country gets a section even when it only inherits defaults: a     ;;",
        ";;  country in geoextract.txt `countries` with no section here raises       ;;",
        ";;  NoSectionError before the run starts.                                   ;;",
        ";;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;",
        "[DEFAULT]",
        f"boundary_file = {BOUNDARY_FILE}",
        "admin_level = admin_1",
        f"shp_region = {BOUNDARY_FILE}",
        f"calendar_file = {CALENDAR_FILE}",
        "use_cropland_mask = False",
        f"mask = {FALLBACK_MASK}",
        "statistics_file = statistics.csv",
        # Deduplicated copy: the zone merge is a plain left join on country, so
        # duplicate rows fan out EVERY merged row. The live file is shared with
        # other projects and is left untouched.
        "zone_file = countries_dedup.csv",
        "annotate_regions = False",
        f"eo_model = {_py_list(EO_MODEL)}",
        "seasons = [1]",
        "crops = ['maize']",
        "",
    ]
    for slug in sorted(entries):
        entry = entries[slug]
        lines.append(f"[{slug}]")
        lines.append(f"; {entry['name']}")
        lines.append(f"crops = {_py_list(entry['crops'])}")
        lines.append(f"seasons = {list(entry['seasons'])}")
        lines.append("")
    out_path.write_text("\n".join(lines), encoding="utf-8")


def write_crops(entries: dict[str, dict], out_path: Path) -> None:
    used = sorted({crop for e in entries.values() for crop in e["crops"]})
    lines = [
        ";;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;",
        ";;  Crop masks -- GENERATED FILE. Masks are the ones agmet already uses.     ;;",
        ";;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;",
        "",
    ]
    for crop in used:
        mask = CROP_MASKS.get(crop, FALLBACK_MASK)
        lines.append(f"[{crop}]")
        if crop not in CROP_MASKS:
            lines.append(f"; no dedicated mask exists for {crop}; generic cropland")
        lines.append(f"mask = {mask}")
        lines.append("")
    out_path.write_text("\n".join(lines), encoding="utf-8")


def write_geoextract(entries: dict[str, dict], out_path: Path) -> None:
    slugs = sorted(entries)
    country_block = "\n".join(f'    "{s}",' for s in slugs)
    text = f"""\
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;  Extraction settings -- GENERATED FILE.                                   ;;
;;  Rebuild: python -m geocif.data_prep.make_cropcal_config                  ;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

[DEFAULT]
project_name = {PROJECT}
method = JRC
start_year = {START_YEAR}
end_year = {END_YEAR}
; redo = False gap-FILLS daily EO rather than skipping the file, so a re-run
; still opens every daily raster. It does not make a second pass cheap.
redo = False
; AFI-weighted mean over every cell with crop fraction > 1%, matching the
; crop-area-weighted spatial mean the original NDVI extractor used.
threshold = True
floor = 1
ceil = 90
parallel_extract = True
parallel_merge = True
fraction_cpus = 0.35
pre_season_months = 6
check_csv = False
clean_csv = False

; {len(slugs)} countries, derived from ADM0_NAME in {BOUNDARY_FILE} so the slug
; cannot drift from what load_country_boundary matches on.
countries = [
{country_block}
    ]

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;  Validator settings (geocif.calendar_validator).                          ;;
;;  Defaults reproduce the GEOGLAM original except where                     ;;
;;  geocif/cropcal/DEVIATIONS.md says otherwise -- each item there names     ;;
;;  the knob that restores the old behaviour.                                ;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
[CROPCAL]
; Years of NDVI/temperature behind the per-day median. The newest year is
; dropped first because it is usually partial.
num_years = 5
; Tolerance, in days, for calling a transition a match.
max_delta = 45

; calendar = real month halves (365-day year, the default).
; legacy   = the original's flat index * 15 (360-day year, runs up to 5 days
;            early by December). Use for a like-for-like comparison with
;            published numbers.
doy_convention = calendar

; True restores the original's behaviour of skipping multi-peak suppression for
; every season that crosses 1 January. That gate was invisible on the AMIS
; regions the method was tested on and wrong for the EW ones that dominate here.
legacy_wrap_gate = False
; False restores the original's non-circular "closest peak" distance.
circular_peak_distance = True
; True anchors the 100-GDD offset to the planting date instead of reproducing
; the original's overshoot. Run both to measure it.
fix_gdd100_offset = False

; Model comparison. Targets are the calendar's FOUR transition days --
; planting, midgreenup, midgreendown, harvest -- predicted from calendar-free
; features of the NDVI, temperature, rainfall, ESI and soil-moisture
; climatologies. Two references sit in every table: the rule-based port (the
; two interior transitions only; there is no satellite rule for planting or
; harvest) and an out-of-fold climatology null (all four). Models are
; dispatched by geocif.ml.trainers.auto_train.
run_models = True
models = ['catboost', 'cubist', 'tabpfn', 'tabicl']
; sincos   = regress sin and cos of the day, recombine with atan2 (resultant
;            length reported: short means the model was torn between modes);
; anchored = regress the signed offset from the NDVI steepest-rise day, which
;            is unimodal across hemispheres. Both run; the table says which won.
target_encodings = ['sincos', 'anchored']
; random = shuffled K-fold, LEAKY, reported as the optimistic reference;
; country = leave-one-country-out; spatial_block = grouped K-fold over tiles;
; country_block = spatial_block with small countries held out whole, which
; stops a national calendar row copied across zones from sitting on both sides
; of a fold. cv_schemes.csv reports that duplicate rate per scheme.
cv_schemes = ['random', 'country', 'spatial_block', 'country_block']
; Optional {scheme: [models]} -- run only those models under that scheme.
; Leave-one-country-out is 145 folds; at ~3 min a fold tabpfn/tabicl need
; 30+ h there, catboost minutes. Leave unset to run every model everywhere.
; cv_scheme_models = {'country': ['catboost']}
n_splits = 5
block_degrees = 10
seed = 0

make_plots = True
; Per-region diagnostics are drawn worst-disagreement first; this caps how many.
max_region_figures = 200

; Optional subsetting for the validator. These are deliberately NOT called
; `crops` / `countries`: those names already belong to geoextract in
; countries.txt / geoextract.txt [DEFAULT], and reusing them silently narrows
; the validation instead of subsetting it. Leave unset to validate everything.
; validate_crops = ['maize', 'winter_wheat']
; validate_countries = ['united_states_of_america', 'kenya']
"""
    out_path.write_text(text, encoding="utf-8")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--lookup", required=True, type=Path)
    ap.add_argument("--calendar", required=True, type=Path)
    ap.add_argument("--template-geobase", type=Path, default=DEFAULT_TEMPLATE)
    ap.add_argument("--config-root", type=Path, default=DEFAULT_CONFIG_ROOT)
    args = ap.parse_args(argv)

    out_dir = args.config_root / PROJECT
    out_dir.mkdir(parents=True, exist_ok=True)

    lookup = pd.read_csv(args.lookup)
    shapefile_slugs = set(lookup["country_slug"])

    entries = country_crops(args.calendar)
    unmatched = sorted(set(entries) - shapefile_slugs)
    if unmatched:
        print(f"ERROR: calendar slugs with no polygon: {unmatched}")
        return 1

    write_geobase(args.template_geobase, out_dir / "geobase.txt")
    write_countries(entries, out_dir / "countries.txt")
    write_crops(entries, out_dir / "crops.txt")
    write_geoextract(entries, out_dir / "geoextract.txt")

    crops = sorted({c for e in entries.values() for c in e["crops"]})
    combos = sum(len(e["crops"]) for e in entries.values())
    years = END_YEAR - START_YEAR + 1
    print(f"wrote {out_dir}")
    print(f"  countries        : {len(entries)}")
    print(f"  crops            : {', '.join(crops)}")
    print(f"  (country, crop)  : {combos}")
    print(f"  EO vars          : {', '.join(EO_MODEL)}")
    print(f"  years            : {START_YEAR}-{END_YEAR}")
    print(f"  extraction combos: {combos * len(EO_MODEL) * years}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
