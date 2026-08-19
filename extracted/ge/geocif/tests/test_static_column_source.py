"""
A missing static EO column must be explained accurately.

geoextract/geomerge read countries.txt; geocif.txt is never in their config
list. A dataset listed only in geocif.txt's eo_model is therefore never
extracted, and the old warning ("re-run geomerge to populate") was actively
misleading — it sent a ~9h extract+merge chain after usa_admin2 soilgrids
columns that could not possibly appear (2026-08-18).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from geocif.cid import definitions as di

GEOCIF_PY = Path(__file__).resolve().parents[1] / "geocif" / "geocif.py"


def test_every_static_column_maps_to_an_eo_model_dataset():
    """Each static crop_t0 column must name the dataset that produces it."""
    for column in di.STATIC_EO_COL_MAP.values():
        assert column in di.STATIC_COLUMN_SOURCE, f"{column} has no source dataset"


def test_sources_are_the_literal_eo_model_names():
    """geoprepare dispatches on these exact strings (extract_EO.py)."""
    assert set(di.STATIC_COLUMN_SOURCE.values()) == {"aridity", "soilgrids"}


def test_soil_columns_map_to_soilgrids():
    for column in ("soil_sand", "soil_clay", "soil_soc", "soil_bdod"):
        assert di.STATIC_COLUMN_SOURCE[column] == "soilgrids"


def test_aridity_column_maps_to_aridity():
    assert di.STATIC_COLUMN_SOURCE["aridity"] == "aridity"


def test_source_map_is_derived_not_hardcoded():
    """Adding a static CID must not require editing a second list."""
    assert set(di.STATIC_COLUMN_SOURCE) == set(di.STATIC_EO_COL_MAP.values())


def test_warning_names_countries_txt_and_stops_promising_geomerge():
    """The message must point at the real fix, not at re-running geomerge."""
    source = GEOCIF_PY.read_text(encoding="utf-8", errors="replace")
    assert "STATIC_COLUMN_SOURCE" in source
    assert "countries.txt" in source
    assert "NOT geocif.txt" in source
