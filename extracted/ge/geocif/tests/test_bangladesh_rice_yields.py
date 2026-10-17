"""Bangladesh rice yields come from config, not from code.

stats.py used to route Bangladesh rice to a hard-coded ``bangladesh_rice.xlsx``
and keep its ``Season == "Boro"`` rows. Now the country's
``production_statistics_file`` names the file. These tests cover the CSV
form (geocif.data_prep.convert_geoglam_xlsx output); test_amis_stats_file.py
covers pointing at the workbook itself. ``Boro`` also resolves as season 1
through PRIMARY_SEASON_NAMES for CSVs without cm_season. Season names that
resolve to nothing are logged instead of silently joining no yields.
"""
import configparser
import logging

import numpy as np
import pandas as pd
import pytest

from geocif.data_prep import convert_geoglam_xlsx
from geocif.ml import stats as ml_stats

TARGET = "Yield (tn per ha)"
STATS = [TARGET, "Area (ha)", "Production (tn)"]
IDS = {
    "ADM0_NAME": ["Bangladesh"] * 6,
    "ADM1_NAME": ["Chittagong"] * 3 + ["Dhaka"] * 3,
    "ADM2_NAME": ["Cox's Bazar"] * 3 + ["Dhaka "] * 3,  # trailing space is stripped
    "Season": ["Boro", "Aman", "Aus"] * 2,
    "CM_Season": [1, 2, 3] * 2,
    "Source": ["BBS"] * 6,
    "num_ID": [2022, 2022, 2022, 3026, 3026, 3026],
}


@pytest.fixture(autouse=True)
def _fresh_warnings(monkeypatch):
    monkeypatch.setattr(ml_stats, "_WARNED", set())


def _workbook(path, scale=1.0):
    """GEOGLAM-format workbook with string year headers, as BBS ships it."""
    values = {
        "Yield (tn per ha)": [[4.0, 2.5, 2.0], [4.2, 2.6, np.nan]],
        "Area (ha)": [[100.0, 200.0, 50.0], [80.0, 90.0, np.nan]],
        "Production (tn)": [[400.0, 500.0, 100.0], [336.0, 234.0, np.nan]],
    }
    with pd.ExcelWriter(path) as writer:
        for sheet, (cox, dhaka) in values.items():
            frame = pd.DataFrame(IDS)
            col = [v * scale for v in cox + dhaka]
            frame["2019"] = col
            frame["2020"] = [v + 0.5 for v in col]
            frame.to_excel(writer, sheet_name=sheet, index=False)
    return path


def _csv_parser(csv_name, **extra):
    parser = configparser.ConfigParser()
    parser["bangladesh"] = {"production_statistics_file": csv_name, **extra}
    return parser


def _frame(season=1):
    return pd.DataFrame({
        "Region": ["cox's_bazar", "dhaka", "cox's_bazar", "dhaka"],
        "Harvest Year": [2019, 2019, 2020, 2020],
        "Season": season,
    })


def test_boro_is_a_season_one_name():
    from geocif.utils import PRIMARY_SEASON_NAMES, SECONDARY_SEASON_NAMES

    assert "Boro" in PRIMARY_SEASON_NAMES
    assert "Boro" not in SECONDARY_SEASON_NAMES


def test_converter_long_format(tmp_path):
    out = convert_geoglam_xlsx.convert(_workbook(tmp_path / "bd.xlsx"), "Rice")

    # 2 districts x 3 seasons x 2 years, minus Dhaka Aus (all three stats NaN) x 2 years
    assert len(out) == 10
    for col in ("country", "admin_1", "admin_2", "product", "season_name",
                "crop_production_system", "qc_flag", "harvest_year",
                "yield", "area", "production"):
        assert col in out.columns
    assert set(out["admin_2"]) == {"Cox's Bazar", "Dhaka"}
    assert out["harvest_year"].tolist().count(2019) == 5
    row = out[(out.admin_2 == "Cox's Bazar") & (out.season_name == "Boro") & (out.harvest_year == 2020)]
    assert row[["yield", "area", "production"]].iloc[0].tolist() == [4.5, 100.5, 400.5]
    assert (out["product"] == "Rice").all()
    assert (out["qc_flag"] == 0).all()


def test_boro_rows_join_from_config_without_override(tmp_path):
    csv = "bangladesh_rice_hvstat.csv"
    convert_geoglam_xlsx.convert(_workbook(tmp_path / "bd.xlsx"), "Rice").to_csv(tmp_path / csv, index=False)
    # A workbook at the old hard-coded name, with different numbers, must be ignored.
    _workbook(tmp_path / "bangladesh_rice.xlsx", scale=10.0)

    out = ml_stats.add_statistics(
        tmp_path, _frame(), "Bangladesh", "Rice", "admin_2", STATS, "", parser=_csv_parser(csv),
    )

    assert out[TARGET].tolist() == pytest.approx([4.0, 4.2, 4.5, 4.7])
    assert out["Area (ha)"].tolist() == pytest.approx([100.0, 80.0, 100.5, 80.5])
    assert out["Production (tn)"].tolist() == pytest.approx([400.0, 336.0, 400.5, 336.5])


def test_season_without_a_known_name_warns_once(tmp_path, caplog):
    csv = "aman_only.csv"
    full = convert_geoglam_xlsx.convert(_workbook(tmp_path / "bd.xlsx"), "Rice")
    # without cm_season the season is matched by name, as in a HarvestStat CSV
    full[full.season_name == "Aman"].drop(columns="cm_season").to_csv(tmp_path / csv, index=False)
    parser = _csv_parser(csv)

    with caplog.at_level(logging.WARNING, logger="geocif.ml.stats"):
        for _ in range(2):
            out = ml_stats.add_statistics(
                tmp_path, _frame(), "Bangladesh", "Rice", "admin_2", STATS, "", parser=parser,
            )

    assert TARGET not in out.columns
    hits = [r for r in caplog.records if "no season_name" in r.getMessage()]
    assert len(hits) == 1
    assert "Aman" in hits[0].getMessage()


def test_override_not_in_file_warns(tmp_path, caplog):
    csv = "bangladesh_rice_hvstat.csv"
    convert_geoglam_xlsx.convert(_workbook(tmp_path / "bd.xlsx"), "Rice").to_csv(tmp_path / csv, index=False)
    parser = _csv_parser(csv, hvstat_season_override="boro")  # wrong case

    with caplog.at_level(logging.WARNING, logger="geocif.ml.stats"):
        out = ml_stats.add_statistics(
            tmp_path, _frame(), "Bangladesh", "Rice", "admin_2", STATS, "", parser=parser,
        )

    assert any("hvstat_season_override" in r.getMessage() for r in caplog.records)
    # The ignored override falls through to PRIMARY_SEASON_NAMES, which finds Boro.
    assert out[TARGET].tolist() == pytest.approx([4.0, 4.2, 4.5, 4.7])
