"""production_statistics_file may name an AMIS/EWCM workbook (.xlsx).

The workbook (one sheet per statistic, one column per year -- the layout of
bangladesh_rice.xlsx and the GEOGLAM <crop>_<season>.xlsx files) is turned
into the long HarvestStat table on read, so it goes through the same join as
a CSV. A run's season picks rows by CM_Season when the file has it.
"""
import configparser
import logging
import os

import numpy as np
import pandas as pd
import pytest

from geocif.ml import stats as ml_stats

TARGET = "Yield (tn per ha)"
STATS = [TARGET, "Area (ha)", "Production (tn)"]
WB = "bd_rice.xlsx"


@pytest.fixture(autouse=True)
def _fresh_state(monkeypatch):
    monkeypatch.setattr(ml_stats, "_WARNED", set())
    monkeypatch.setattr(ml_stats, "_WORKBOOK_CACHE", {})


def _bd_workbook(path, scale=1.0):
    """Two districts x Boro/Aman/Aus (CM_Season 1/2/3), string year headers."""
    ids = pd.DataFrame({
        "ADM0_NAME": ["Bangladesh"] * 6,
        "ADM1_NAME": ["Chittagong"] * 3 + ["Dhaka"] * 3,
        "ADM2_NAME": ["Cox's Bazar"] * 3 + ["Dhaka"] * 3,
        "Season": ["Boro", "Aman", "Aus"] * 2,
        "CM_Season": [1, 2, 3] * 2,
        "Source": ["BBS"] * 6,
        "num_ID": ["BD2022"] * 3 + ["BD3026"] * 3,
    })
    values = {  # rows: Cox's Bazar Boro/Aman/Aus, Dhaka Boro/Aman/Aus
        "Yield (tn per ha)": [4.0, 2.5, 2.0, 4.2, 2.6, 2.1],
        "Area (ha)": [100.0, 200.0, 50.0, 80.0, 90.0, 10.0],
        "Production (tn)": [400.0, 500.0, 100.0, 336.0, 234.0, 21.0],
    }
    with pd.ExcelWriter(path) as writer:
        for sheet, col in values.items():
            frame = ids.copy()
            frame["2019"] = [v * scale for v in col]
            frame["2020"] = [v * scale + 0.5 for v in col]
            frame.to_excel(writer, sheet_name=sheet, index=False)
    return path


def _parser(fn=WB, **extra):
    parser = configparser.ConfigParser()
    parser["bangladesh"] = {"production_statistics_file": fn, **extra}
    return parser


def _frame(season):
    return pd.DataFrame({
        "Region": ["cox's_bazar", "dhaka", "cox's_bazar", "dhaka"],
        "Harvest Year": [2019, 2019, 2020, 2020],
        "Season": season,
    })


def _join(tmp_path, season, parser=None):
    return ml_stats.add_statistics(
        tmp_path, _frame(season), "Bangladesh", "Rice", "admin_2", STATS, "",
        parser=parser or _parser(),
    )


def test_season_one_joins_the_boro_rows(tmp_path):
    _bd_workbook(tmp_path / WB)
    out = _join(tmp_path, 1)
    assert out[TARGET].tolist() == pytest.approx([4.0, 4.2, 4.5, 4.7])
    assert out["Area (ha)"].tolist() == pytest.approx([100.0, 80.0, 100.5, 80.5])
    assert out["Production (tn)"].tolist() == pytest.approx([400.0, 336.0, 400.5, 336.5])


def test_season_number_picks_cm_season_rows(tmp_path):
    _bd_workbook(tmp_path / WB)
    assert _join(tmp_path, 2)[TARGET].tolist() == pytest.approx([2.5, 2.6, 3.0, 3.1])  # Aman
    assert _join(tmp_path, 3)[TARGET].tolist() == pytest.approx([2.0, 2.1, 2.5, 2.6])  # Aus


def test_mixed_seasons_in_one_frame(tmp_path):
    _bd_workbook(tmp_path / WB)
    df = pd.DataFrame({"Region": ["dhaka", "dhaka"], "Harvest Year": [2019, 2019], "Season": [1, 2]})
    out = ml_stats.add_statistics(
        tmp_path, df, "Bangladesh", "Rice", "admin_2", STATS, "", parser=_parser(),
    )
    assert out[TARGET].tolist() == pytest.approx([4.2, 2.6])


def test_valid_override_beats_cm_season(tmp_path):
    _bd_workbook(tmp_path / WB)
    out = _join(tmp_path, 1, parser=_parser(hvstat_season_override="Aus"))
    assert out[TARGET].tolist() == pytest.approx([2.0, 2.1, 2.5, 2.6])


def test_blank_season_name_is_picked_by_cm_season(tmp_path):
    # AMIS admin_1 rows often have no Season label (rice_1.xlsx has 260)
    frame = pd.DataFrame({
        "ADM0_NAME": ["Japan", "Japan"], "ADM1_NAME": ["Hokkaido", "Hokkaido"],
        "Season": [np.nan, np.nan], "CM_Season": [1, 2], "num_ID": [1, 1],
        2019: [5.5, 3.0],
    })
    with pd.ExcelWriter(tmp_path / "jp.xlsx") as writer:
        frame.to_excel(writer, sheet_name="Yield (tn per ha)", index=False)
    parser = configparser.ConfigParser()
    parser["japan"] = {"production_statistics_file": "jp.xlsx"}
    df = pd.DataFrame({"Region": ["hokkaido"], "Harvest Year": [2019], "Season": [1]})
    out = ml_stats.add_statistics(tmp_path, df, "Japan", "Rice", "admin_1", [TARGET], "", parser=parser)
    assert out[TARGET].tolist() == pytest.approx([5.5])


def test_season_number_absent_from_the_file_warns(tmp_path, caplog):
    _bd_workbook(tmp_path / WB)
    with caplog.at_level(logging.WARNING, logger="geocif.ml.stats"):
        out = _join(tmp_path, 4)
    assert TARGET not in out.columns
    assert any("CM_Season == 4" in r.getMessage() for r in caplog.records)


def test_workbook_without_the_country_warns(tmp_path, caplog):
    _bd_workbook(tmp_path / WB)
    parser = configparser.ConfigParser()
    parser["nepal"] = {"production_statistics_file": WB}
    with caplog.at_level(logging.WARNING, logger="geocif.ml.stats"):
        ml_stats.add_statistics(
            tmp_path, _frame(1), "Nepal", "Rice", "admin_2", STATS, "", parser=parser,
        )
    assert any("no rows with ADM0_NAME == 'Nepal'" in r.getMessage() for r in caplog.records)


def test_admin1_lookup_and_regions_with_yields_read_the_workbook(tmp_path):
    _bd_workbook(tmp_path / WB)
    lookup = ml_stats.admin1_lookup(tmp_path, "Bangladesh", parser=_parser())
    assert lookup == {"cox's bazar": "Chittagong", "dhaka": "Dhaka",
                      "chittagong cox's bazar": "Chittagong", "dhaka dhaka": "Dhaka"}
    keep = ml_stats.regions_with_yields(tmp_path, "Bangladesh", "Rice", "admin_2", parser=_parser())
    assert keep == {"cox's bazar", "dhaka", "chittagong cox's bazar", "dhaka dhaka"}


def test_edited_workbook_is_reread(tmp_path):
    path = _bd_workbook(tmp_path / WB)
    assert _join(tmp_path, 1)[TARGET].iloc[0] == pytest.approx(4.0)
    _bd_workbook(path, scale=2.0)
    st = path.stat()
    os.utime(path, ns=(st.st_atime_ns, st.st_mtime_ns + 10**9))
    assert _join(tmp_path, 1)[TARGET].iloc[0] == pytest.approx(8.0)


def test_cached_table_is_not_shared_with_callers(tmp_path):
    path = _bd_workbook(tmp_path / WB)
    a = ml_stats.read_production_statistics(path, product="Rice")
    a.loc[:, "yield"] = -1.0
    b = ml_stats.read_production_statistics(path, product="Maize")
    assert (b["yield"] > 0).all()
    assert (b["product"] == "Maize").all()


def test_fdw_historical_export_reads_the_workbook(tmp_path, monkeypatch):
    from geocif import fdw_export, yield_outlook

    _bd_workbook(tmp_path / WB)
    monkeypatch.setattr(yield_outlook, "_load_shapefiles", lambda parser: (None, {}))
    monkeypatch.setattr(
        fdw_export, "_build_shapefile_lookup",
        lambda dg, levels: pd.DataFrame({
            "_country_lc": ["bangladesh"], "_region_lc": ["dhaka"],
            "ADM_ID": ["BD3026"], "ADM1_NAME": ["Dhaka"], "ADM2_NAME": ["Dhaka"],
        }),
    )
    parser = _parser()
    parser["DEFAULT"] = {"countries": '["bangladesh"]', "project_name": "t"}
    parser["PATHS"] = {"dir_output": str(tmp_path), "dir_production_statistics": str(tmp_path)}
    parser["bangladesh"]["crops"] = "['rice']"
    parser["bangladesh"]["admin_level"] = "admin_2"

    path = fdw_export.export_historical(parser, source_name_version="test", dir_out=tmp_path / "fdw")

    out = pd.read_csv(path)
    assert len(out) == 12  # 2 districts x 3 seasons x 2 years
    assert set(out["crop"]) == {"Rice"}
    dhaka_boro = out[(out.admin_2 == "Dhaka") & (out.crop_season == "Boro") & (out.harvest_year == 2019)]
    assert dhaka_boro["yield_obs"].iloc[0] == pytest.approx(4.2)
