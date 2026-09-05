"""Tests for ``[ML] exclude_years``.

Motivation: usa_admin1 soybean harvest year 2025 fails at the Oct 1-Apr 30
stage in every configuration tried (uniform ~0.57x scaling, cause
unidentified), which drags the all-years per-year R2 from 0.830 to 0.060.
``training_start_year`` can only move a lower bound, so there was no way to
excise an interior year. ``exclude_years`` drops it from ``df_inputs``, which
feeds BOTH ``df_train`` and ``df_test`` -- so the year leaves the fit and the
scored set together.

These exercise the filter logic directly rather than booting the full class,
which needs a live config tree, EO inputs and a DB.
"""

import ast

import pandas as pd
import pytest


def _parse_exclude_years(raw):
    """Mirror of the parsing in ``_initialize_ml_configuration``."""
    raw = (raw or "").strip()
    if not raw:
        return []
    try:
        parsed = ast.literal_eval(raw)
        if isinstance(parsed, (int, float)):
            parsed = [parsed]
        if not isinstance(parsed, (list, tuple, set)):
            raise TypeError(type(parsed).__name__)
        return sorted({int(y) for y in parsed})
    except (ValueError, SyntaxError, TypeError):
        raise ValueError(
            f"[ML] exclude_years is malformed: {raw!r}. Use a list of integer "
            f"Harvest Years, e.g. exclude_years = [2025]"
        )


def _apply(df, exclude_years):
    """Mirror of the drop in ``_apply_training_year_filter``."""
    return df[~df["Harvest Year"].isin(exclude_years)].reset_index(drop=True)


@pytest.fixture()
def frame():
    return pd.DataFrame({
        "Harvest Year": [2023, 2023, 2024, 2024, 2025, 2025, 2026, 2026],
        "Region": ["Iowa", "Ohio"] * 4,
        "Yield (tn per ha)": [4.0, 3.5, 4.1, 3.6, 4.3, 3.6, None, None],
    })


# ---------------------------------------------------------------- parsing
@pytest.mark.parametrize("raw,expected", [
    ("", []),
    ("   ", []),
    ("[2025]", [2025]),
    ("[2025, 2012]", [2012, 2025]),
    ("2025", [2025]),                       # bare scalar is accepted
    ("[2025, 2025]", [2025]),               # de-duplicated
    ("[2025.0]", [2025]),                   # float coerced
])
def test_parse_valid(raw, expected):
    assert _parse_exclude_years(raw) == expected


@pytest.mark.parametrize("raw", ["[2025", "twenty-25", "[a, b]", "{2025:1}"])
def test_parse_malformed_raises(raw):
    """A malformed value must NOT silently degrade to 'exclude nothing' --
    the run would look successful while testing the wrong thing."""
    with pytest.raises(ValueError, match="exclude_years"):
        _parse_exclude_years(raw)


# ---------------------------------------------------------------- filtering
def test_excluded_year_removed_entirely(frame):
    out = _apply(frame, [2025])
    assert 2025 not in set(out["Harvest Year"])
    assert len(out) == 6


def test_other_years_untouched(frame):
    out = _apply(frame, [2025])
    assert sorted(set(out["Harvest Year"])) == [2023, 2024, 2026]
    # every surviving row is bit-identical to its original
    keep = frame[frame["Harvest Year"] != 2025].reset_index(drop=True)
    pd.testing.assert_frame_equal(out, keep)


def test_excluded_year_absent_from_both_train_and_test(frame):
    """The whole point: df_train and df_test are both derived from the
    filtered frame, so the year cannot leak into either."""
    out = _apply(frame, [2025])
    for forecast_season in (2023, 2024, 2026):
        mask = out["Harvest Year"] == forecast_season
        df_train, df_test = out[~mask], out[mask]
        assert 2025 not in set(df_train["Harvest Year"])
        assert 2025 not in set(df_test["Harvest Year"])


def test_empty_list_is_a_noop(frame):
    pd.testing.assert_frame_equal(_apply(frame, []), frame)


def test_excluding_absent_year_is_harmless(frame):
    """Config asking for a year the data lacks changes nothing (the caller
    logs a warning so the mismatch is visible)."""
    pd.testing.assert_frame_equal(_apply(frame, [1999]), frame)


def test_multiple_years(frame):
    out = _apply(frame, [2024, 2025])
    assert sorted(set(out["Harvest Year"])) == [2023, 2026]


def test_composes_with_training_start_year(frame):
    """exclude_years runs AFTER the window filter; the two are independent."""
    windowed = frame[frame["Harvest Year"] >= 2024].reset_index(drop=True)
    out = _apply(windowed, [2025])
    assert sorted(set(out["Harvest Year"])) == [2024, 2026]


def test_excluding_every_year_leaves_empty_frame(frame):
    out = _apply(frame, [2023, 2024, 2025, 2026])
    assert out.empty
