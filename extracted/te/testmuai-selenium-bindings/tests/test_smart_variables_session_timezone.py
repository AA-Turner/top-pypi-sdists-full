"""Smart date/time variables resolve in the session timezone, not the box's.

auteur computes them against KANE_SESSION_TIMEZONE; the binding used a naive
datetime.now(), so authoring and replay disagreed by the UTC offset. And
current_timezone returned the "%Z" abbreviation where auteur returns the IANA
region — a different kind of value, so an authored assertion never matched.
"""
import calendar
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import pytest


@pytest.fixture
def smart(monkeypatch):
    """_resolve_smart with a chosen session timezone.

    No module reload — the env is read per call, and reloading resets
    _variable_store under every other test file holding the module.
    """
    from testmu_selenium._vars import _resolve_smart

    def _with(tz):
        if tz is None:
            monkeypatch.delenv("KANE_SESSION_TIMEZONE", raising=False)
        else:
            monkeypatch.setenv("KANE_SESSION_TIMEZONE", tz)
        return _resolve_smart
    return _with


def _auteur_expected(tz):
    """auteur's smart_variables_init, verbatim — the contract to match."""
    d = datetime.now(ZoneInfo(tz))
    return {
        "current_date": d.strftime("%Y-%m-%d"),
        "current_day": d.strftime("%A"),
        "current_month_number": d.strftime("%m"),
        "current_year": d.strftime("%Y"),
        "current_month": d.strftime("%B"),
        "current_hour": d.strftime("%H"),
        "current_minute": d.strftime("%M"),
        "current_timezone": tz,
        "next_day": (d + timedelta(days=1)).strftime("%Y-%m-%d"),
        "previous_day": (d - timedelta(days=1)).strftime("%Y-%m-%d"),
        "start_of_week": (d - timedelta(days=d.weekday())).strftime("%Y-%m-%d"),
        "end_of_week": (d + timedelta(days=6 - d.weekday())).strftime("%Y-%m-%d"),
        "start_of_month": d.replace(day=1).strftime("%Y-%m-%d"),
        "end_of_month": d.replace(
            day=calendar.monthrange(d.year, d.month)[1]).strftime("%Y-%m-%d"),
    }


@pytest.mark.parametrize("tz", ["Asia/Kolkata", "America/New_York", "UTC"])
def test_matches_auteur_for_every_date_time_variable(smart, tz):
    """Authoring and replay must produce identical values."""
    resolve = smart(tz)
    for name, expected in _auteur_expected(tz).items():
        assert str(resolve(name)) == expected, f"{name} diverged from auteur in {tz}"


def test_current_timezone_is_the_iana_region_not_the_abbreviation(smart):
    """strftime('%Z') gave 'IST'; auteur gives 'Asia/Kolkata'."""
    assert smart("Asia/Kolkata")("current_timezone") == "Asia/Kolkata"


def test_hour_follows_the_session_timezone(smart):
    """A naive clock would give the same hour in both zones."""
    assert int(smart("Asia/Kolkata")("current_hour")) != int(
        smart("America/New_York")("current_hour"))


def test_defaults_to_utc_when_unset(smart):
    """Local run / standalone export — auteur's fallback."""
    assert smart(None)("current_timezone") == "UTC"


def test_unknown_region_falls_back_instead_of_raising(smart):
    """A config typo must not abort the run."""
    assert smart("Not/AZone")("current_timezone") == "UTC"


def test_non_datetime_smart_variables_still_resolve(smart):
    """The tz change must not disturb the random/geo family."""
    resolve = smart("Asia/Kolkata")
    assert resolve("country") == "India"
    assert len(resolve("random_string_8")) == 8
    assert 100 <= int(resolve("random_int")) <= 999
