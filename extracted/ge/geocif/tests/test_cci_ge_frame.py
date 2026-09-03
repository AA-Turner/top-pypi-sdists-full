"""get_cci_frame must expose %Good+Excellent alongside the weighted index."""

import pandas as pd
import pytest

from geocif.cid.cci import get_cci_frame


@pytest.fixture()
def cci_csv(tmp_path):
    df = pd.DataFrame({
        "crop": ["maize"] * 4 + ["soybean"],
        "region": ["iowa"] * 4 + ["iowa"],
        "state_alpha": ["IA"] * 5,
        "year": [2018] * 5,
        "woy": [22, 23, 26, 27, 22],
        "week_ending": ["2018-06-03", "2018-06-10", "2018-07-01",
                        "2018-07-08", "2018-06-03"],
        "cci": [70.0, 74.0, 60.0, 64.0, 50.0],
        "very_poor": [1, 1, 2, 2, 3],
        "poor": [4, 3, 6, 5, 7],
        "fair": [20, 18, 26, 25, 30],
        "good": [55, 56, 50, 52, 45],
        "excellent": [20, 22, 16, 16, 15],
    })
    p = tmp_path / "cond.csv"
    df.to_csv(p, index=False)
    return p


def test_ge_is_monthly_mean_of_good_plus_excellent(cci_csv):
    out = get_cci_frame(cci_csv, "maize")
    assert set(out.columns) == {"region", "year", "Month", "cci", "cci_ge"}
    jun = out[(out.Month == 6)].iloc[0]
    jul = out[(out.Month == 7)].iloc[0]
    assert jun["cci_ge"] == pytest.approx((55 + 20 + 56 + 22) / 2)   # 76.5
    assert jul["cci_ge"] == pytest.approx((50 + 16 + 52 + 16) / 2)   # 67.0
    # weighted index untouched
    assert jun["cci"] == pytest.approx(72.0)


def test_ge_absent_when_categories_missing(cci_csv, tmp_path):
    df = pd.read_csv(cci_csv).drop(columns=["good", "excellent"])
    p = tmp_path / "old_format.csv"
    df.to_csv(p, index=False)
    out = get_cci_frame(p, "maize")
    assert "cci_ge" not in out.columns          # downstream no-ops
    assert "cci" in out.columns


def test_crop_filter_still_applies(cci_csv):
    out = get_cci_frame(cci_csv, "soybean")
    assert len(out) == 1 and out.iloc[0]["cci_ge"] == 60
