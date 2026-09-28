"""get_cci_frame gap-fill: unreported in-season months take the last weekly report.

Motivating case: the Oct 1 - Nov 12 2025 federal shutdown cancelled every NASS Crop
Progress release from Oct 6 to Nov 10, so October 2025 has no condition anywhere. Without
a fill the October CCI windows stay empty and the ML stage zero-fills them, which reads as
total crop failure.
"""

import pandas as pd
import pytest

from geocif.cid.cci import get_cci_frame


def _season(region, year, start, end, base, crop="soybean"):
    """Weekly reports every 7 days from ``start`` to ``end`` (inclusive)."""
    rows = []
    for i, d in enumerate(pd.date_range(f"{year}-{start}", f"{year}-{end}", freq="7D")):
        cci = base + (i % 5)
        rows.append({"crop": crop, "region": region, "state_alpha": "XX", "year": year,
                     "woy": int(d.isocalendar().week), "week_ending": d.strftime("%Y-%m-%d"),
                     "cci": float(cci), "very_poor": 2, "poor": 5, "fair": 20,
                     "good": 50 + (i % 3), "excellent": 23 - (i % 3)})
    return rows


def _history(region="iowa", last_2025="09-28", years=range(2014, 2025)):
    rows = []
    for y in years:
        rows += _season(region, y, "06-01", "10-26", 70)
    rows += _season(region, 2025, "06-01", last_2025, 60)
    return rows


def _write(tmp_path, rows, vintage="2025-11-16"):
    # Another crop keeps reporting after soybean stops (winter wheat, Nov 2025): that is
    # what makes October 2025 a finished month rather than a future one.
    if vintage:
        rows = rows + [{"crop": "winter_wheat", "region": "kansas", "state_alpha": "KS", "year": 2025,
                        "woy": 46, "week_ending": vintage, "cci": 65.0, "very_poor": 1, "poor": 4,
                        "fair": 30, "good": 50, "excellent": 15}]
    p = tmp_path / "cond.csv"
    pd.DataFrame(rows).to_csv(p, index=False)
    return p


def _oct(out, year=2025, region="iowa"):
    return out[(out.region == region) & (out.year == year) & (out.Month == 10)]


def test_truncated_october_takes_last_weekly_report(tmp_path):
    rows = _history()
    p = _write(tmp_path, rows)
    out = get_cci_frame(p, "soybean")
    oct25 = _oct(out)
    assert len(oct25) == 1
    last = [r for r in rows if r["year"] == 2025][-1]            # the 2025-09-28 report
    assert last["week_ending"] == "2025-09-28"
    assert oct25.iloc[0]["cci"] == pytest.approx(last["cci"])
    assert oct25.iloc[0]["cci_ge"] == pytest.approx(last["good"] + last["excellent"])


def test_schema_unchanged(tmp_path):
    out = get_cci_frame(_write(tmp_path, _history()), "soybean")
    assert set(out.columns) == {"region", "year", "Month", "cci", "cci_ge"}


def test_reported_months_untouched(tmp_path):
    p = _write(tmp_path, _history())
    on = get_cci_frame(p, "soybean")
    off = get_cci_frame(p, "soybean", gap_fill=False)
    key = ["region", "year", "Month"]
    merged = off.merge(on, on=key, suffixes=("_off", "_on"))
    assert len(merged) == len(off)                                # nothing dropped
    assert (merged.cci_off == merged.cci_on).all()
    assert len(on) == len(off) + 1                                # only Oct 2025 added


def test_switch_off_leaves_gap(tmp_path):
    out = get_cci_frame(_write(tmp_path, _history()), "soybean", gap_fill=False)
    assert _oct(out).empty


def test_future_month_never_filled(tmp_path):
    # Latest report anywhere is the 2025-09-28 soybean week -> October 2025 has not
    # happened yet from this file's point of view.
    out = get_cci_frame(_write(tmp_path, _history(), vintage=None), "soybean")
    assert _oct(out).empty


def test_structural_month_not_filled(tmp_path):
    rows = _history()
    rows += _season("iowa", 2016, "05-03", "05-31", 50)          # May in 1 of 12 years
    out = get_cci_frame(_write(tmp_path, rows), "soybean")
    assert out[(out.Month == 5) & (out.year != 2016)].empty


def test_gap_longer_than_two_months_not_filled(tmp_path):
    # 2025 stops in June: Jul-Oct missing (4 months) -> too long to persist.
    out = get_cci_frame(_write(tmp_path, _history(last_2025="06-29")), "soybean")
    assert out[(out.year == 2025) & (out.Month > 6)].empty


def test_stale_last_report_not_filled(tmp_path):
    # Last 2025 report Aug 10, then Sep-Oct missing: a 2-month gap, but the last report
    # is 22 days before the gap -> too old to carry forward.
    out = get_cci_frame(_write(tmp_path, _history(last_2025="08-10")), "soybean")
    assert out[(out.year == 2025) & (out.Month >= 9)].empty


def test_interior_gap_filled_from_previous_month(tmp_path):
    rows = [r for r in _history() if not (r["year"] == 2020 and r["week_ending"].startswith("2020-08"))]
    out = get_cci_frame(_write(tmp_path, rows), "soybean")
    aug = out[(out.year == 2020) & (out.Month == 8)]
    last_jul = [r for r in rows if r["week_ending"].startswith("2020-07")][-1]
    assert len(aug) == 1 and aug.iloc[0]["cci"] == pytest.approx(last_jul["cci"])


def test_years_filter_applies_after_fill(tmp_path):
    out = get_cci_frame(_write(tmp_path, _history()), "soybean", years=[2025])
    assert set(out.year) == {2025}
    assert len(_oct(out)) == 1


def test_short_record_not_filled(tmp_path):
    rows = _history(years=range(2022, 2025))                      # 4 years < MIN_YEARS
    out = get_cci_frame(_write(tmp_path, rows), "soybean")
    assert _oct(out).empty


def test_other_crops_unaffected(tmp_path):
    out = get_cci_frame(_write(tmp_path, _history()), "winter_wheat")
    assert len(out) == 1                                          # its single report, no fills
