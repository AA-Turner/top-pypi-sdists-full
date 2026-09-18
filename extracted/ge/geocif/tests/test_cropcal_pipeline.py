"""End-to-end wiring of the crop-calendar validator.

Synthetic extraction CSVs are written in the exact layout and schema geoextract
produces, then driven through :func:`geocif.cropcal.pipeline.run_region`. The
point is to catch the joins -- directory template, filename prefix, NDVI
rescaling, the (tmax, tmin) -> GDD path -- without waiting on a cluster run.

The NDVI is constructed so the true transitions are known, which lets the test
assert that a calendar agreeing with the satellite scores as agreement and a
calendar two months out of step does not.
"""

from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from geocif.cropcal import calendar as cropcal_calendar
from geocif.cropcal import features, naming, pipeline, score, series

N_DOY = 366
PEAK_DOY = 200
CROP = "maize"
COUNTRY_SLUG = "testland"
REGION = "central"
REGION_ID = 42


# --------------------------------------------------------------------------
# Synthetic extraction archive
# --------------------------------------------------------------------------
def _ndvi_curve(peak_doy=PEAK_DOY, width=35.0):
    """A single clean season, in real NDVI units."""
    doy = np.arange(N_DOY)
    return 0.15 + 0.65 * np.exp(-0.5 * ((doy - peak_doy) / width) ** 2)


def _temperature_curve(mean=15.0, amplitude=12.0, phase=200):
    doy = np.arange(N_DOY)
    return mean + amplitude * np.cos(2 * np.pi * (doy - phase) / 365.0)


def _write_var(root: Path, var: str, values: np.ndarray, years, *, store_raw_ndvi: bool):
    """Write one variable's per-year CSVs exactly as geoextract does."""
    directory = series.region_dir(root, 1, COUNTRY_SLUG, "admin_1", CROP, var)
    directory.mkdir(parents=True, exist_ok=True)
    for year in years:
        stored = values * series.NDVI_GAIN + series.NDVI_OFFSET if store_raw_ndvi else values
        frame = pd.DataFrame(
            {
                "country": COUNTRY_SLUG,
                "region": REGION,
                "region_id": REGION_ID,
                "lat": 10.0,
                "lon": 20.0,
                "year": year,
                "doy": np.arange(1, N_DOY + 1),
                var: stored,
                "total_pixels": 1000,
                "valid_data": 900,
                "valid_data_after_masking": 800,
                "weight_sum": 1.0,
                "weight_sum_used": 1.0,
            }
        )
        frame.to_csv(
            directory / f"{REGION_ID}_{REGION}_{year}_{var}_{CROP}.csv", index=False
        )


@pytest.fixture
def archive(tmp_path):
    """A six-year extraction archive for one region."""
    years = range(2019, 2025)
    ndvi = _ndvi_curve()
    _write_var(tmp_path, series.VAR_NDVI, ndvi, years, store_raw_ndvi=True)
    _write_var(tmp_path, series.VAR_TMAX, _temperature_curve(20.0), years, store_raw_ndvi=False)
    _write_var(tmp_path, series.VAR_TMIN, _temperature_curve(10.0), years, store_raw_ndvi=False)
    return tmp_path


def _calendar_row(codes):
    return pd.Series({f"code_{i}": float(v) for i, v in enumerate(codes)})


def _codes_for_season(start_bin, stage1=3, stage2=4, stage3=3):
    """Build a 24-bin row with a contained season starting at ``start_bin``."""
    codes = [0] * 24
    cursor = start_bin
    for stage, length in ((1, stage1), (2, stage2), (3, stage3)):
        for _ in range(length):
            codes[cursor % 24] = stage
            cursor += 1
    return codes


def _context():
    return pipeline.RegionContext(
        key="Central Testland",
        country="Testland",
        country_slug=COUNTRY_SLUG,
        region=REGION,
        region_id=REGION_ID,
        crop=CROP,
        season=1,
        cm_group="AMIS",
        climate_zone="Temperate",
        hemisphere="N",
        lat=10.0,
        lon=20.0,
    )


def _settings(root, **overrides):
    return pipeline.Settings(root=root, years=tuple(range(2019, 2025)), **overrides)


# --------------------------------------------------------------------------
# Loading and scaling
# --------------------------------------------------------------------------
def test_doy_year_frame_is_366_by_n_years_and_rescaled(archive):
    directory = series.region_dir(archive, 1, COUNTRY_SLUG, "admin_1", CROP, series.VAR_NDVI)
    frame = series.load_doy_year_frame(directory, series.VAR_NDVI, REGION_ID)
    assert frame.shape == (N_DOY, 6)
    assert list(frame.columns) == list(range(2019, 2025))
    # The archive stores MOD09 digital numbers; the loader must undo that.
    assert frame.max().max() == pytest.approx(0.80, abs=1e-6)
    assert frame.min().min() == pytest.approx(0.15, abs=1e-3)


def test_region_dir_does_not_repeat_the_project_name():
    """Regression: dir_output already ends in the project name.

    geoprepare's ``base.BaseGeo.parse_config`` appends ``project_name`` to
    ``dir_output``. An earlier version of ``region_dir`` prepended it a second
    time, producing ``outputs/cropcal/cropcal/crop_t1/...``; every region on the
    first cluster run came back as "no EO data" while the extraction sat
    happily one level up.
    """
    got = series.region_dir(
        Path("/gpfs/x/outputs/cropcal"), 1, "france", "admin_1", "maize", "ndvi"
    )
    assert got == Path("/gpfs/x/outputs/cropcal/crop_t1/france/admin_1/maize/ndvi")
    assert "cropcal/cropcal" not in got.as_posix()


def test_missing_region_is_an_explicit_error_not_an_empty_frame(archive):
    directory = series.region_dir(archive, 1, COUNTRY_SLUG, "admin_1", CROP, series.VAR_NDVI)
    with pytest.raises(series.SeriesError):
        series.load_doy_year_frame(directory, series.VAR_NDVI, 9999)


def test_climatology_drops_the_newest_year(archive):
    directory = series.region_dir(archive, 1, COUNTRY_SLUG, "admin_1", CROP, series.VAR_NDVI)
    frame = series.load_doy_year_frame(directory, series.VAR_NDVI, REGION_ID)
    selected = series.select_climatology_years(frame, num_years=5)
    assert 2024 not in selected.columns, "the newest year is usually partial"
    assert list(selected.columns) == [2019, 2020, 2021, 2022, 2023]


def test_gdd_is_clipped_and_floored():
    params = naming.crop_params("maize")          # base 8 C, cap 25 C
    tmean = np.array([0.0, 8.0, 15.0, 30.0, np.nan])
    gdd = series.growing_degree_days(tmean, params.min_base_temp, params.max_base_temp)
    assert gdd[0] == 0.0                           # below base
    assert gdd[1] == 0.0                           # at base
    assert gdd[2] == pytest.approx(7.0)
    assert gdd[3] == pytest.approx(17.0)           # capped at 25, not 30
    assert np.isnan(gdd[4])


# --------------------------------------------------------------------------
# End to end
# --------------------------------------------------------------------------
def test_agreeing_calendar_scores_as_agreement(archive):
    """A calendar whose stage 2 brackets the NDVI peak should agree."""
    # Season bins 10..19 -> roughly mid-May to late September, peak mid-July.
    row = _calendar_row(_codes_for_season(9))
    outcome = pipeline.run_region(_context(), row, _settings(archive))

    assert outcome.scored, outcome.row.get("skip_reason")
    assert outcome.row["Assessment"] == score.ALGO_WORKS
    assert abs(outcome.row["delta_midgreenup"]) <= 45
    assert abs(outcome.row["delta_midgreendown"]) <= 45
    assert outcome.row["Peak_in_2ndStage"] is True


def test_calendar_two_months_out_of_step_is_flagged(archive):
    """Shifting the calendar four bins (~60 days) must break the assessment."""
    aligned = pipeline.run_region(_context(), _calendar_row(_codes_for_season(9)), _settings(archive))
    shifted = pipeline.run_region(_context(), _calendar_row(_codes_for_season(3)), _settings(archive))

    assert shifted.scored, shifted.row.get("skip_reason")
    assert abs(shifted.row["delta_midgreenup"]) > abs(aligned.row["delta_midgreenup"])
    assert np.isnan(shifted.row["Assessment"])


def test_outcome_carries_a_feature_row_with_both_targets(archive):
    outcome = pipeline.run_region(_context(), _calendar_row(_codes_for_season(9)), _settings(archive))
    row = outcome.feature_row
    assert row is not None
    for target in features.TARGETS:
        assert np.isfinite(row[f"target_{target}"])
        assert np.isfinite(row[f"target_{target}_sin"])
    # The rule-based answer rides along so the baseline needs no recomputation.
    assert np.isfinite(row["rule_midgreenup"])
    assert row["doy_peak"] == pytest.approx(PEAK_DOY, abs=5)


def test_missing_extraction_is_a_reason_not_a_crash(tmp_path):
    outcome = pipeline.run_region(
        _context(), _calendar_row(_codes_for_season(9)), _settings(tmp_path)
    )
    assert not outcome.scored
    assert "no EO data" in outcome.row["skip_reason"]


def test_unparameterised_crop_is_skipped_with_its_reason(archive):
    context = _context()
    context.crop = "beans"
    outcome = pipeline.run_region(context, _calendar_row(_codes_for_season(9)), _settings(archive))
    assert not outcome.scored
    assert "thermal parameters" in outcome.row["skip_reason"]


def test_malformed_calendar_row_is_skipped_with_its_reason(archive):
    codes = _codes_for_season(9)
    codes[20] = -1                       # partial not-grown sentinel
    outcome = pipeline.run_region(_context(), _calendar_row(codes), _settings(archive))
    assert not outcome.scored
    assert "-1" in outcome.row["skip_reason"]


def test_design_matrix_and_cv_run_on_pipeline_output(archive):
    """The feature rows a real run emits must survive design_matrix + CV."""
    from geocif.cropcal import cv as cropcal_cv

    rows = []
    for index, start_bin in enumerate((7, 8, 9, 10, 11, 12)):
        context = _context()
        context.key = f"Region{index} Testland"
        context.country = f"Country{index % 3}"
        context.lat = 10.0 + 12.0 * index
        context.lon = 20.0 + 12.0 * index
        outcome = pipeline.run_region(
            context, _calendar_row(_codes_for_season(start_bin)), _settings(archive)
        )
        assert outcome.scored, outcome.row.get("skip_reason")
        rows.append(outcome.feature_row)

    design = features.design_matrix(rows)
    assert len(design) == 6
    assert "target_midgreenup_sin" in design.columns

    schemes = cropcal_cv.build_schemes(design, n_splits=3)
    assert {"random", "country", "spatial_block"} <= set(schemes)
    for scheme in schemes.values():
        covered = sorted(np.concatenate([test for _train, test in scheme.splits]))
        assert covered == list(range(6)), f"{scheme.name} must predict every row once"


# --------------------------------------------------------------------------
# Config option names
# --------------------------------------------------------------------------
def test_validator_subset_options_cannot_collide_with_geoextract_keys():
    """Regression: the validator's crop filter must not be spelled `crops`.

    ConfigParser resolves a missing option against [DEFAULT], and
    countries.txt [DEFAULT] already carries `crops = ['maize']` for geoextract.
    Reading `crops` from the [CROPCAL] section therefore returned geoextract's
    default and silently narrowed a 145-country, 8-crop validation to maize
    alone -- 433 rows scored, exit code 0, no warning. Same hazard for
    `countries`.
    """
    import configparser
    import inspect

    from geocif import calendar_validator

    parser = configparser.ConfigParser()
    parser["DEFAULT"] = {"crops": "['maize']", "countries": "['france']"}
    parser.add_section("CROPCAL")

    # The trap: [DEFAULT] makes these look present in every section.
    assert parser.has_option("CROPCAL", "crops")
    assert parser.has_option("CROPCAL", "countries")
    # The fix: the validator's own names are not shadowed by anything.
    assert not parser.has_option("CROPCAL", "validate_crops")
    assert not parser.has_option("CROPCAL", "validate_countries")

    source = inspect.getsource(calendar_validator.CalendarValidator.parse_config)
    assert '_getlist("validate_crops"' in source
    assert '_getlist("validate_countries"' in source
    assert '_getlist("crops"' not in source


def test_duplicate_zone_rows_never_reach_the_algorithm():
    """Regression: countries.csv has duplicate rows with conflicting values.

    bangladesh is listed both Temperate and Tropical, bolivia both Tropical and
    Temperate, and the russian federation appears under two spellings that
    normalise to one key. A ``.loc`` on the resulting duplicated index returns a
    Series, and ``str()`` of that is a multi-line repr -- which equals neither
    "Temperate" nor "Tropical", so the winter-wheat greenup rules silently never
    fire and the GDD scaling is decided by accident. It corrupted 82 of 1,351
    scored regions and was only caught because Cubist's C backend rejected the
    resulting one-hot column name.
    """
    import pandas as pd

    from geocif import calendar_validator

    series = pd.Series(["Temperate", "Tropical"], index=["bangladesh", "bangladesh"])
    assert calendar_validator._scalar(series, "Temperate") == "Temperate"
    assert calendar_validator._scalar("Tropical", "Temperate") == "Tropical"
    assert calendar_validator._scalar("", "Temperate") == "Temperate"
    assert calendar_validator._scalar(pd.Series([], dtype=object), "N") == "N"

    # The corrupted form must never compare equal to a real zone.
    corrupted = str(series)
    assert corrupted not in ("Temperate", "Tropical")
    assert "\n" in corrupted


def test_zone_metadata_deduplicates_on_the_normalised_key():
    """Two spellings of one country must collapse to a single row."""
    import inspect

    from geocif import calendar_validator

    source = inspect.getsource(calendar_validator.CalendarValidator.zone_metadata)
    assert 'drop_duplicates("_join", keep="first")' in source
    assert "Conflicting values for" in source, "a silent dedup is how this got missed"
