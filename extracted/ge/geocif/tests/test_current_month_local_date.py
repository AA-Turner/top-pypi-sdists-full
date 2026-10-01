"""Current-month stage filtering uses the run's local date, not UTC.

2026-09-30: a run launched at 19:09 EDT dropped September's partial stages,
one launched at 19:55 EDT ran into 00:00 UTC (= October 1 in UTC) and kept
them — so its hindcast saw September windows and its 2026 forecast was built
from an incomplete September (20-30 % low in every state).
"""
from pathlib import Path
from types import SimpleNamespace

import arrow as ar

from geocif.geocif import Geocif

ROOT = Path(__file__).resolve().parents[1] / "geocif"


def _stub(when, stages):
    return SimpleNamespace(
        _date=ar.get(when, tzinfo="America/New_York"), align_hindcast_stage=True,
        forecast_season=2026, today_year=2026, all_stages=list(stages),
    )


def test_late_evening_on_the_last_day_still_drops_the_local_month():
    o = _stub("2026-09-30T20:30:00", ["9_8_7_6", "9", "8_7_6", "8", "PS_3"])
    assert ar.get(o._date).to("UTC").month == 10, "the case: UTC is already October"
    Geocif._filter_current_month_stages(o)
    assert o.all_stages == ["8_7_6", "8", "PS_3"]


def test_january_does_not_drop_october_to_december_stages():
    o = _stub("2027-01-15T12:00:00", ["1_12_11", "1", "12_11", "11_10", "10_9"])
    Geocif._filter_current_month_stages(o)
    assert o.all_stages == ["12_11", "11_10", "10_9"]


def test_no_utc_month_or_day_reads_remain():
    src = (ROOT / "geocif.py").read_text(encoding="utf-8")
    assert "ar.utcnow().month" not in src and "ar.utcnow().day" not in src
