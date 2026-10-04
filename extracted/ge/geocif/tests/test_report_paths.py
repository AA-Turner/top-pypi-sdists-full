"""Regression tests: report.py must look for the run's outputs where they are
written. Only the module-level path helpers are exercised, so reportlab is not
needed.
"""
import configparser

from geocif import report


def _touch(path):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(b"")
    return path


def test_report_reads_pearson_summary_from_analysis_date_folder(tmp_path):
    # 2026-10-03: G2a, introduced in 3e4e2f6 (0.4.734) — only searched roots
    # relative to dir_outlook (<stamp>/outlook), never the Geocif date folder.
    analysis = tmp_path / "outputs" / "kenya_proj" / "ml" / "analysis"
    dir_outlook = analysis / "October_03_2026_14h05" / "outlook"
    dir_outlook.mkdir(parents=True)
    date_dir = analysis / "October_03_2026"
    csv = _touch(date_dir / "explore" / "cid_vs_yield" / "kenya" / "maize"
                 / "csvs" / "pearson_summary.csv")

    assert report._pearson_summary_paths(dir_outlook, [], "kenya", "maize") == []
    assert report._pearson_summary_paths(dir_outlook, [date_dir], "kenya", "maize") == [csv]


def test_report_finds_xai_images_in_analysis_date_folder(tmp_path):
    # 2026-10-03: G2b, introduced in 8ff388a (0.4.465) — looked in <stamp>/xai,
    # which nothing writes; ml/xai.py writes <date>/<country>/<crop>/<model>/<year>/.
    analysis = tmp_path / "outputs" / "kenya_proj" / "ml" / "analysis"
    (analysis / "October_03_2026_14h05" / "outlook").mkdir(parents=True)
    date_dir = analysis / "October_03_2026"
    year_dir = date_dir / "kenya" / "maize" / "catboost" / "2026"
    beeswarm = _touch(year_dir / "beeswarm_101_2026.png")
    waterfall = _touch(year_dir / "waterfall_Nakuru_maize_2026.png")
    _touch(date_dir / "kenya" / "maize" / "catboost" / "2025" / "beeswarm_101_2025.png")

    found = report._find_xai_images([date_dir], ["kenya"], ["maize"], ["catboost"], 2026)
    assert found == [beeswarm, waterfall]


def test_report_finds_agmet_plots_in_adm1_and_district(tmp_path):
    # 2026-10-03: G2c, introduced in 8ff388a (0.4.465) — no project segment,
    # crop code crop[:2] ("ma" for maize, geoagmet writes "mz"), and PNGs
    # globbed in condition/ instead of its adm1/ adm2/ district/ subfolders.
    parser = configparser.ConfigParser()
    parser.read_dict({
        "DEFAULT": {"project_name": "agmet"},
        "PATHS": {"dir_output": str(tmp_path / "outputs")},
        "kenya": {"category": "EWCM"},
    })
    condition = (tmp_path / "outputs" / "agmet" / "crop_condition" / "October_03_2026"
                 / "plots" / "EWCM" / "kenya" / "mz_s1_2026" / "condition")
    region_png = _touch(condition / "adm1" / "nakuru.png")
    district_png = _touch(condition / "district" / "rift_valley.png")

    agmet_dir = report._find_agmet_dir(parser, "kenya", "maize", 1, 2026)
    assert agmet_dir == condition
    assert report._agmet_pngs(agmet_dir) == [region_png, district_png]


def test_report_picks_newest_agmet_date_folder_not_alphabetical(tmp_path):
    # 2026-10-03: _find_agmet_dir sorted MMMM_DD_YYYY folder names as plain
    # strings (since 8ff388a, 0.4.465), so September_26 beat October_03 and the
    # report embedded last week's AgMet charts once the G2c lookup found them.
    parser = configparser.ConfigParser()
    parser.read_dict({
        "DEFAULT": {"project_name": "agmet"},
        "PATHS": {"dir_output": str(tmp_path / "outputs")},
        "canada": {"category": "AMIS"},
    })
    base = tmp_path / "outputs" / "agmet" / "crop_condition"
    rel = ("plots", "AMIS", "canada", "mz_s1_2026", "condition")
    for day in ("September_26_2026", "October_03_2026", "September_12_2026"):
        _touch(base.joinpath(day, *rel, "adm1", "manitoba.png"))
    (base / "notes").mkdir()  # a non-date entry must not break the sort

    assert report._find_agmet_dir(parser, "canada", "maize", 1, 2026) == base.joinpath("October_03_2026", *rel)
