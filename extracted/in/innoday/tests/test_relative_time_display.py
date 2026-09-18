"""`format_datetime` renders a timestamp a person can read, or crashes trying.

Two defects, both found by running `innoday auth tokens` — which could not
reach the API until the team-secret header was fixed, so nothing had ever
rendered its output:

1. A **naive** datetime was compared against an **aware** `now`, raising
   `TypeError: can't subtract offset-naive and offset-aware datetimes`. The two
   branches were the wrong way round. It hid because most callers pass an ISO
   string carrying an offset; anything serialised from one of this schema's ~99
   naive columns arrives without one.
2. A **future** timestamp fell through branches that all assume the past and
   rendered as `-2d ago` — so a token expiring in two days read as one that
   lapsed two days ago, in the column whose entire job is that distinction.

This function had no tests at all.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

from src.cli.utils.formatters import format_datetime


class TestANaiveTimestampDoesNotCrash:
    """The database hands these over naive. `as_utc` at the boundary is the
    convention this codebase already settled on."""

    def test_a_naive_datetime_renders(self):
        naive = datetime.utcnow() - timedelta(hours=3)
        assert format_datetime(naive) == "3h ago"

    def test_a_naive_iso_string_renders(self):
        """No offset in the string, which is how a naive column serialises."""
        stamp = (datetime.utcnow() - timedelta(days=2)).isoformat()
        assert format_datetime(stamp) == "2d ago"

    def test_an_aware_datetime_still_renders(self):
        aware = datetime.now(timezone.utc) - timedelta(hours=3)
        assert format_datetime(aware) == "3h ago"

    def test_the_two_agree(self):
        """The same instant, spelled both ways, must read the same. This is the
        property the inverted branches broke."""
        now = datetime.now(timezone.utc) - timedelta(days=3)
        assert format_datetime(now) == format_datetime(now.replace(tzinfo=None))


class TestAFutureTimestampIsNotAgo:
    """Each offset carries a small buffer past the unit boundary.

    The function reads its own clock microseconds after the test reads one, so
    an exact `timedelta(days=2)` is really 1d 23h 59m 59.99s by the time it is
    measured, and truncates to `in 1d`. That truncation is correct and worth
    keeping — downward is the safe direction for an expiry, since it understates
    the time left rather than overstating it — so the tests step past the
    boundary instead of asserting a value only a frozen clock could produce.
    """

    def test_days_ahead(self):
        assert (
            format_datetime(datetime.now(timezone.utc) + timedelta(days=2, minutes=1))
            == "in 2d"
        )

    def test_hours_ahead(self):
        assert (
            format_datetime(datetime.now(timezone.utc) + timedelta(hours=5, minutes=1))
            == "in 5h"
        )

    def test_minutes_ahead(self):
        assert (
            format_datetime(
                datetime.now(timezone.utc) + timedelta(minutes=9, seconds=1)
            )
            == "in 9m"
        )

    def test_truncation_understates_rather_than_overstates(self):
        """Just short of two days reads as one, never as two. For a credential
        that is the direction you want to be wrong in."""
        assert (
            format_datetime(datetime.now(timezone.utc) + timedelta(days=1, hours=23))
            == "in 1d"
        )

    def test_a_moment_ahead_never_reads_as_zero_minutes(self):
        """`in 0m` reads as "now", which for an expiry is the opposite of the
        truth. Anything still in the future rounds up to a minute."""
        assert format_datetime(datetime.now(timezone.utc) + timedelta(seconds=5)) == (
            "in 1m"
        )

    def test_nothing_ahead_renders_with_a_minus(self):
        for ahead in (timedelta(seconds=30), timedelta(hours=4), timedelta(days=9)):
            assert "-" not in format_datetime(datetime.now(timezone.utc) + ahead)


class TestTheUnchangedCases:
    def test_absent_is_not_applicable(self):
        assert format_datetime(None) == "N/A"
        assert format_datetime("") == "N/A"

    def test_recent_minutes(self):
        assert format_datetime(datetime.now(timezone.utc) - timedelta(minutes=5)) == (
            "5m ago"
        )

    def test_yesterday_is_named(self):
        assert (
            format_datetime(datetime.now(timezone.utc) - timedelta(days=1, hours=1))
            == "Yesterday"
        )

    def test_beyond_a_week_is_a_date(self):
        old = datetime.now(timezone.utc) - timedelta(days=30)
        assert format_datetime(old) == old.strftime("%Y-%m-%d")

    def test_unparseable_falls_back_to_the_raw_value(self):
        assert format_datetime("not a date") == "not a date"
