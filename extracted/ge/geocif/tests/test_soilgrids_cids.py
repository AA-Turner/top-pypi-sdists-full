"""Static per-region EO features: SoilGrids (SOIL_*) + Aridity (AI).

Design (post per-stage-emission rework): static variables are NOT emitted as
staged CID rows — cid/indices.py skips them entirely, and geocif joins the
raw geomerge columns (soil_sand/.../aridity) from the crop_t0 CSV onto the
wide ML frame post-pivot as bare stage-less columns
(``_add_static_eo_features``), then force-includes them in
``create_feature_names`` gated by ``use_cids``.
"""

import types
from pathlib import Path

import pandas as pd

GEOCIF_DIR = Path(__file__).resolve().parents[1] / "geocif"


def test_definitions_registered():
    from geocif.cid import definitions as di

    soil = {"SOIL_SAND", "SOIL_CLAY", "SOIL_SOC", "SOIL_BDOD"}
    assert set(di.dict_soilgrids) == soil
    assert all(v[0] == "Soil" for v in di.dict_soilgrids.values())
    assert set(di.soilgrids_col_map) == soil
    assert set(di.soilgrids_col_map.values()) == {
        "soil_sand", "soil_clay", "soil_soc", "soil_bdod"
    }
    # combined static registry = aridity + soilgrids, col map consistent
    assert set(di.dict_static_eo) == soil | {"AI"}
    assert set(di.STATIC_EO_COL_MAP) == soil | {"AI"}
    assert di.STATIC_EO_COL_MAP["AI"] == "aridity"


def test_indices_does_not_emit_static_vars():
    """Static variables must NOT go through the staged CID emission."""
    src = (GEOCIF_DIR / "cid" / "indices.py").read_text(encoding="utf-8")
    assert 'eo_vars.append("SOILGRIDS")' not in src
    assert 'eo_vars.append("Aridity")' not in src
    assert "__aridity__" not in src
    assert "dict_soilgrids" not in src


def test_geocif_wiring():
    src = (GEOCIF_DIR / "geocif.py").read_text(encoding="utf-8")
    # join step present and in the _prepare_ml_dataframe chain
    assert "def _add_static_eo_features" in src
    assert "df = self._add_static_eo_features(df)" in src
    # force-include block in create_feature_names
    assert "di.dict_static_eo" in src
    # static AI guarded from per-region z-scoring (soil_* covered by soil_kw)
    assert '"Trend All", "Yield Trend", "AI",' in src


def test_add_static_eo_features_joins_bare_columns():
    """Functional: the join maps normalized region names to values and
    produces numeric bare columns; variables absent from crop_t0 are
    skipped without creating a column."""
    from geocif.geocif import Geocif

    stub = types.SimpleNamespace(
        countries_pooled=None,
        country="testland",
        crop="maize",
        logger=types.SimpleNamespace(info=lambda *a, **k: None,
                                     warning=lambda *a, **k: None),
    )

    values = {
        "soil_sand": {"region_a": 410.0, "region_b": 520.0},
        "aridity": {"region_a": 0.35},
        # soil_clay/soc/bdod absent -> reader returns {}
    }
    stub._read_region_static_from_crop_t0 = (
        lambda country, crop, col: values.get(col, {})
    )

    df = pd.DataFrame({
        "Region": ["Region A", "Region-B", "Region A"],
        "Harvest Year": [2020, 2020, 2021],
    })
    out = Geocif._add_static_eo_features(stub, df.copy())

    assert list(out["SOIL_SAND"]) == [410.0, 520.0, 410.0]
    assert out["AI"].tolist()[0] == 0.35
    assert pd.isna(out["AI"].iloc[1])  # region_b has no aridity value
    assert "SOIL_CLAY" not in out.columns  # absent everywhere -> skipped
    assert out["SOIL_SAND"].dtype.kind == "f"
