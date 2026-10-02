"""``_load_observed_baselines`` / ``_merge_obs_baseline`` (audit B rows):

* the "10yr" window spanned ELEVEN years (``max_year - 10 .. current_year - 1``);
* multi-country baselines were grouped and merged on Region only, so
  namesake regions across countries (Malawi / Zambia "Central") shared one
  baseline.
"""
import configparser

import pandas as pd
import pytest

from geocif import utils
from geocif.yield_outlook import _load_observed_baselines, _merge_obs_baseline

METHOD = "monthly_r"
PROJECT = "geocif"
CROP = "maize"


def _parser(dir_output):
    p = configparser.ConfigParser()
    p.add_section("PATHS")
    p.set("PATHS", "dir_output", str(dir_output))
    p["DEFAULT"]["project_name"] = PROJECT
    p["DEFAULT"]["method"] = METHOD
    return p


def _write_stats(tmp_path, country, df):
    f = utils.statistics_file_path(tmp_path / PROJECT, METHOD, country, CROP)
    f.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(f, index=False)


def test_10yr_window_is_ten_years(tmp_path):
    years = list(range(2010, 2026))  # last observed = 2025 = current_year - 1
    _write_stats(tmp_path, "kenya", pd.DataFrame({
        "Region": ["a"] * len(years),
        "Harvest Year": years,
        "Yield (tn per ha)": [float(y - 2000) for y in years],   # 10..25
    }))
    out = _load_observed_baselines(["kenya"], CROP, _parser(tmp_path), current_year=2026)
    # 2016..2025 inclusive -> mean of 16..25 = 20.5 (eleven years 2015..2025
    # would give 20.0).
    assert out["10yr"]["obs_mean"].iloc[0] == pytest.approx(20.5)


def test_multi_country_baselines_keyed_on_country_and_region(tmp_path):
    _write_stats(tmp_path, "malawi", pd.DataFrame({
        "Region": ["Central"] * 5, "Harvest Year": [2013, 2014, 2015, 2016, 2017],
        "Yield (tn per ha)": [1.0] * 5,
    }))
    _write_stats(tmp_path, "zambia", pd.DataFrame({
        "Region": ["Central"] * 5, "Harvest Year": [2013, 2014, 2015, 2016, 2017],
        "Yield (tn per ha)": [3.0] * 5,
    }))
    out = _load_observed_baselines(["malawi", "zambia"], CROP, _parser(tmp_path),
                                   current_year=2026)
    base = out["2013-2017"]
    assert list(base.columns) == ["Country", "Region", "obs_mean"]
    assert len(base) == 2  # one baseline PER COUNTRY, not one shared "Central"

    left = pd.DataFrame({
        "Country": ["malawi", "zambia"], "Region": ["Central", "Central"],
        "Country Region": ["malawi central", "zambia central"],
        "current_predicted": [2.0, 2.0],
    })
    merged = _merge_obs_baseline(left, base)
    assert len(merged) == 2
    got = dict(zip(merged["Country"], merged["obs_mean"]))
    assert got == {"malawi": 1.0, "zambia": 3.0}
    assert "_ckey" not in merged.columns


def test_merge_is_country_spelling_tolerant_and_falls_back_to_region():
    base = pd.DataFrame({"Country": ["south_africa"], "Region": ["Free State"],
                         "obs_mean": [4.0]})
    left = pd.DataFrame({"Country": ["South Africa"], "Region": ["Free State"],
                         "current_predicted": [5.0]})
    assert _merge_obs_baseline(left, base)["obs_mean"].iloc[0] == 4.0
    # No Country on the left: the legacy Region-only join still works.
    left2 = pd.DataFrame({"Region": ["Free State"], "current_predicted": [5.0]})
    assert _merge_obs_baseline(left2, base)["obs_mean"].iloc[0] == 4.0
