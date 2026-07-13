"""Structural test for :func:`geocif.report_lite.generate_report_lite`.

Builds a tiny emulated ``outlook/`` tree (a few placeholder PNGs + a minimal
rRMSEp ranking CSV) and a fake configparser ``parser``, then asserts one
non-empty per-country PDF is written. Skipped where reportlab / PIL are absent.
"""
import configparser

import pandas as pd
import pytest

# Soft deps: reportlab builds the PDF, PIL both scales images and writes the
# placeholder PNGs. Skip the whole module if either is missing.
pytest.importorskip("reportlab")
PILImage = pytest.importorskip("PIL.Image")

from geocif.report_lite import (
    generate_report_lite,
    _best_model,
    _scatter_plot,
    _build_yield_table_rows,
)


def _png(path, size=(48, 32), color=(120, 160, 90)):
    path.parent.mkdir(parents=True, exist_ok=True)
    PILImage.new("RGB", size, color).save(path)


def _build_tree(root, country, crop, best, year):
    """Emulate the yield-outlook output tree for one (country, crop, model)."""
    stage_name = "Jan 1-Oct 31"
    stage_safe = stage_name.replace(" - ", "-").replace(" ", "_")

    map_dir = root / "maps" / best / country / stage_safe
    _png(map_dir / f"predicted_yield_{country}_{crop}_{best}_{stage_name}_{year}.png")
    _png(map_dir / f"yield_outlook_{country}_{crop}_{best}_{stage_name}_{year}.png")
    # A twin that MUST be ignored (obs_anomaly + _filtered).
    obs_dir = map_dir / "obs_anomaly" / "period1"
    _png(obs_dir / f"yield_outlook_{country}_{crop}_{best}_{year}_filtered.png")

    plot_dir = root / "plots" / "model_comparison" / country
    _png(plot_dir / f"rrmsep_summary_{country}_{crop}.png")

    # Best-model scatter (plus the national + by-year twins that MUST be ignored).
    scatter_dir = root / "plots" / best / country
    _png(scatter_dir / f"scatter_{country}_{crop}_{best}.png")
    _png(scatter_dir / f"scatter_national_{country}_{crop}_{best}.png")
    _png(scatter_dir / "scatter_by_year" / f"scatter_{country}_{crop}_{best}_2020.png")

    csv_dir = root / "csvs" / "model_comparison" / country
    csv_dir.mkdir(parents=True, exist_ok=True)
    (csv_dir / f"rrmsep_summary_{country}_{crop}.csv").write_text(
        "Model,rrmsep_mean,rrmsep_std,n_years\n"
        f"{best},8.10,1.20,12\n"
        "xgboost,11.40,2.30,12\n",
        encoding="utf-8",
    )


def test_generate_report_lite_writes_nonempty_pdf(tmp_path):
    country, crop, best, year = "testland", "maize", "catboost", 2026

    dir_outlook = tmp_path / "outlook"
    _build_tree(dir_outlook, country, crop, best, year)

    dir_output = tmp_path / "reports"

    parser = configparser.ConfigParser()
    parser.add_section("PATHS")
    parser.set("PATHS", "dir_output", str(dir_output))
    parser.set("PATHS", "dir_metadata", str(tmp_path / "metadata"))
    parser.add_section(country)
    parser.set(country, "crops", "['maize']")

    written = generate_report_lite(
        dir_outlook, parser, year,
        [country], [crop], [best, "xgboost"],
        dir_output=dir_output,
    )

    expected = dir_output / f"yield_outlook_report_lite_{country}_{year}.pdf"
    assert written == [expected]
    assert expected.exists()
    assert expected.stat().st_size > 0


def test_generate_report_lite_missing_csv_falls_back(tmp_path):
    """No rRMSEp CSV -> best model falls back to models[0]; PDF still built."""
    country, crop, best, year = "testland", "maize", "catboost", 2026

    dir_outlook = tmp_path / "outlook"
    # Only the predicted map exists; no CSV, no scorecard, no outlook map.
    stage_safe = "Jan_1-Oct_31"
    map_dir = dir_outlook / "maps" / best / country / stage_safe
    _png(map_dir / f"predicted_yield_{country}_{crop}_{best}_Jan 1-Oct 31_{year}.png")

    parser = configparser.ConfigParser()
    parser.add_section("PATHS")
    parser.set("PATHS", "dir_output", str(dir_outlook))
    parser.add_section(country)
    parser.set(country, "crops", "['maize']")

    written = generate_report_lite(
        dir_outlook, parser, year,
        [country], [crop], [best, "xgboost"],
    )

    expected = dir_outlook / f"yield_outlook_report_lite_{country}_{year}.pdf"
    assert written == [expected]
    assert expected.exists() and expected.stat().st_size > 0


def test_generate_report_lite_with_outlook_db_adds_yield_table(tmp_path):
    """Passing outlook_db adds a per-region predicted-yield table, so the PDF is
    strictly larger than the same report built without the DB."""
    import sqlite3

    country, crop, best, year = "testland", "maize", "catboost", 2026

    dir_outlook = tmp_path / "outlook"
    _build_tree(dir_outlook, country, crop, best, year)

    # Tiny outlook DB: table testland_maize with a handful of 2026 rows plus a
    # wrong-year and wrong-model row that MUST be filtered out.
    db_path = tmp_path / "outlook.db"
    con = sqlite3.connect(str(db_path))
    con.execute(
        f'CREATE TABLE "{country}_{crop}" ('
        '"Region" TEXT, "Season" INTEGER, "Model" TEXT, '
        '"Harvest Year" INTEGER, "Predicted Yield (tn per ha)" REAL, '
        '"Last Observed Yield (tn per ha)" REAL, "Last Observed Year" INTEGER, '
        '"Median Yield (tn per ha)" REAL)'
    )
    con.executemany(
        f'INSERT INTO "{country}_{crop}" VALUES (?,?,?,?,?,?,?,?)',
        [
            ("North", 1, best, 2026, 3.10, 2.90, 2024, 2.80),
            ("South", 1, best, 2026, 2.40, 2.20, 2024, 2.30),
            ("North", 2, best, 2026, 1.90, 1.75, 2024, 1.80),
            ("South", 2, best, 2026, 2.75, 2.60, 2024, 2.55),
            ("North", 1, best, 2025, 2.00, 1.90, 2023, 1.95),      # wrong year
            ("North", 1, "xgboost", 2026, 9.99, 9.0, 2024, 9.5),   # wrong model
        ],
    )
    con.commit()
    con.close()

    parser = configparser.ConfigParser()
    parser.add_section("PATHS")
    parser.set("PATHS", "dir_metadata", str(tmp_path / "metadata"))
    parser.add_section(country)
    parser.set(country, "crops", "['maize']")

    out_no_table = tmp_path / "reports_no_table"
    out_with_table = tmp_path / "reports_with_table"

    written_no = generate_report_lite(
        dir_outlook, parser, year, [country], [crop], [best, "xgboost"],
        dir_output=out_no_table,
    )
    written_with = generate_report_lite(
        dir_outlook, parser, year, [country], [crop], [best, "xgboost"],
        dir_output=out_with_table, outlook_db=db_path,
    )

    assert len(written_no) == 1 and len(written_with) == 1
    pdf_no, pdf_with = written_no[0], written_with[0]
    assert pdf_no.exists() and pdf_with.exists()
    assert pdf_with.stat().st_size > pdf_no.stat().st_size


def test_read_predicted_yield_table_filters_year_and_model(tmp_path):
    """The DB read keeps only forecast-year + best-model rows and reports the
    distinct Season integers present."""
    import sqlite3
    from geocif.report_lite import _read_predicted_yield_table

    country, crop, best, year = "testland", "maize", "catboost", 2026
    db_path = tmp_path / "outlook.db"
    con = sqlite3.connect(str(db_path))
    con.execute(
        f'CREATE TABLE "{country}_{crop}" ('
        '"Region" TEXT, "Season" INTEGER, "Model" TEXT, '
        '"Harvest Year" TEXT, "Predicted Yield (tn per ha)" REAL, '
        '"Last Observed Yield (tn per ha)" REAL, "Last Observed Year" INTEGER, '
        '"Median Yield (tn per ha)" REAL)'
    )
    con.executemany(
        f'INSERT INTO "{country}_{crop}" VALUES (?,?,?,?,?,?,?,?)',
        [
            ("North", 1, best, "2026", 3.10, 2.90, 2024, 2.80),
            ("South", 2, best, "2026", 2.75, 2.60, 2024, 2.55),
            ("North", 1, best, "2025", 2.00, 1.90, 2023, 1.95),      # wrong year
            ("North", 1, "xgboost", "2026", 9.99, 9.0, 2024, 9.5),   # wrong model
        ],
    )
    con.commit()
    con.close()

    df, seasons = _read_predicted_yield_table(db_path, country, crop, best, year)
    assert df is not None and len(df) == 2
    assert seasons == [1, 2]
    assert set(df["Region"]) == {"North", "South"}
    # The context columns are read when present in the table.
    for col in (
        "Last Observed Yield (tn per ha)",
        "Last Observed Year",
        "Median Yield (tn per ha)",
    ):
        assert col in df.columns

    # Missing DB -> graceful skip.
    df2, seasons2 = _read_predicted_yield_table(
        tmp_path / "nope.db", country, crop, best, year
    )
    assert df2 is None and seasons2 == []


def test_scatter_plot_excludes_national_and_by_year(tmp_path):
    """_scatter_plot returns the plain best-model scatter and never the national
    or per-year variants."""
    country, crop, best = "testland", "maize", "catboost"
    scatter_dir = tmp_path / "plots" / best / country
    _png(scatter_dir / f"scatter_{country}_{crop}_{best}.png")
    _png(scatter_dir / f"scatter_national_{country}_{crop}_{best}.png")
    _png(scatter_dir / "scatter_by_year" / f"scatter_{country}_{crop}_{best}_2020.png")

    hit = _scatter_plot(tmp_path, country, crop, best)
    assert hit is not None
    assert hit.name == f"scatter_{country}_{crop}_{best}.png"
    assert "scatter_national_" not in hit.name
    assert "scatter_by_year" not in str(hit).replace("\\", "/")

    # Missing directory -> None (graceful skip).
    assert _scatter_plot(tmp_path, "nowhere", crop, best) is None


def test_build_yield_table_rows_columns_and_units(tmp_path):
    """Multi-season table keeps a Season column and exposes the context columns
    with the display unit; single-season drops Season. Values are formatted."""
    parser = configparser.ConfigParser()  # no hvstat -> season labels fall back

    df = pd.DataFrame({
        "Region": ["North", "South", "North"],
        "Season": [1, 1, 2],
        "Predicted Yield (tn per ha)": [2.40, 3.10, 1.90],
        "Last Observed Yield (tn per ha)": [2.20, 2.90, None],
        "Last Observed Year": [2024, 2024, 2024],
        "Median Yield (tn per ha)": [2.30, 2.80, 1.80],
    })

    header, rows = _build_yield_table_rows(
        df, [1, 2], parser, "testland", "maize", "Mg/ha"
    )
    assert header == [
        "Region", "Season", "Predicted yield (Mg/ha)",
        "Last observed yield (Mg/ha)", "Last obs. year", "Median yield (Mg/ha)",
    ]
    # Sorted by Season, then predicted-yield DESC within season.
    assert rows[0][0] == "South" and rows[0][2] == "3.10"   # season 1, highest
    assert rows[1][0] == "North" and rows[1][2] == "2.40"
    assert rows[2][0] == "North" and rows[2][2] == "1.90"   # season 2
    # 2-decimal yields, integer year, blank for a NULL context value.
    assert rows[0][4] == "2024"          # last obs year as integer
    assert rows[2][3] == ""              # NULL last observed yield -> blank
    assert rows[0][5] == "2.80"          # median yield 2 decimals

    # Single-season -> Season column dropped.
    df1 = df[df["Season"] == 1].copy()
    header1, rows1 = _build_yield_table_rows(
        df1, [1], parser, "testland", "maize", "Mg/ha"
    )
    assert header1 == [
        "Region", "Predicted yield (Mg/ha)",
        "Last observed yield (Mg/ha)", "Last obs. year", "Median yield (Mg/ha)",
    ]
    assert rows1[0][0] == "South" and rows1[0][1] == "3.10"


def test_cover_title_has_no_lite(tmp_path, monkeypatch):
    """The cover title drops the '(Lite)' tag."""
    import geocif.report_lite as rl

    captured = {}
    orig = rl._LiteReport.add_cover

    def _spy(self, title, subtitle_lines):
        captured["title"] = title
        return orig(self, title, subtitle_lines)

    monkeypatch.setattr(rl._LiteReport, "add_cover", _spy)

    country, crop, best, year = "testland", "maize", "catboost", 2026
    dir_outlook = tmp_path / "outlook"
    _build_tree(dir_outlook, country, crop, best, year)

    parser = configparser.ConfigParser()
    parser.add_section("PATHS")
    parser.set("PATHS", "dir_metadata", str(tmp_path / "metadata"))
    parser.add_section(country)
    parser.set(country, "crops", "['maize']")

    written = generate_report_lite(
        dir_outlook, parser, year, [country], [crop], [best, "xgboost"],
        dir_output=tmp_path / "reports",
    )
    assert written
    assert "(Lite)" not in captured["title"]
    assert captured["title"].startswith("GeoCIF Yield Outlook —")


def test_best_model_excludes_blend_pseudomodels(tmp_path):
    """A blend/ensemble pseudo-model (inv_rmse) may top the rRMSEp ranking but
    lacks the full map set; _best_model must pick the best REAL model instead."""
    country, crop = "testland", "maize"
    csv_dir = tmp_path / "csvs" / "model_comparison" / country
    csv_dir.mkdir(parents=True)
    (csv_dir / f"rrmsep_summary_{country}_{crop}.csv").write_text(
        "Model,rrmsep_mean,rrmsep_std,n_years\n"
        "inv_rmse,10.0,1.0,12\n"   # blend, lowest — must be ignored
        "cubist,12.0,1.0,12\n"     # best REAL model
        "catboost,15.0,1.0,12\n",
        encoding="utf-8",
    )
    best = _best_model(tmp_path, country, crop,
                       ["catboost", "cubist", "tabpfn", "null", "trend"])
    assert best == "cubist"
