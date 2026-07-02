import datetime as dt

import pytz

from django.test import TestCase

from app_utils.datetime import (
    datetime_round_hour,
    ldap_time_2_datetime,
    ldap_timedelta_2_timedelta,
    timeuntil_str,
)


class TestTimeUntil(TestCase):
    def test_timeuntil(self):
        duration = dt.timedelta(days=365 + 30 * 4 + 5, seconds=3600 * 14 + 60 * 33 + 10)
        expected = "1y 4mt 5d 14h 33m 10s"
        self.assertEqual(timeuntil_str(duration), expected)

        duration = dt.timedelta(days=2, seconds=3600 * 14 + 60 * 33 + 10)
        expected = "2d 14h 33m 10s"
        self.assertEqual(timeuntil_str(duration), expected)

        duration = dt.timedelta(days=2, seconds=3600 * 14 + 60 * 33 + 10)
        expected = "2d 14h 33m 10s"
        self.assertEqual(timeuntil_str(duration), expected)

        duration = dt.timedelta(days=0, seconds=60 * 33 + 10)
        expected = "0h 33m 10s"
        self.assertEqual(timeuntil_str(duration), expected)

        duration = dt.timedelta(days=0, seconds=10)
        expected = "0h 0m 10s"
        self.assertEqual(timeuntil_str(duration), expected)

        duration = dt.timedelta(days=-10, seconds=-20)
        expected = ""
        self.assertEqual(timeuntil_str(duration), expected)


class TestDatetimeRoundHour(TestCase):
    def test_round_down(self):
        obj = dt.datetime(2020, 12, 18, 22, 19)
        self.assertEqual(datetime_round_hour(obj), dt.datetime(2020, 12, 18, 22, 0))

    def test_round_up(self):
        obj = dt.datetime(2020, 12, 18, 22, 44)
        self.assertEqual(datetime_round_hour(obj), dt.datetime(2020, 12, 18, 23, 0))

    def test_before_midnight(self):
        obj = dt.datetime(2020, 12, 18, 23, 44)
        self.assertEqual(datetime_round_hour(obj), dt.datetime(2020, 12, 19, 0, 0))

    def test_after_midnight(self):
        obj = dt.datetime(2020, 12, 19, 00, 14)
        self.assertEqual(datetime_round_hour(obj), dt.datetime(2020, 12, 19, 0, 0))


class TestLdapDateConversion(TestCase):
    def test_ldap_datetime_2_dt(self):
        self.assertEqual(
            ldap_time_2_datetime(131924601300000000),
            pytz.utc.localize(
                dt.datetime(year=2019, month=1, day=20, hour=12, minute=15, second=30)
            ),
        )

    def test_ldap_timedelta_2_timedelta(self):
        expected = dt.timedelta(minutes=15)
        self.assertEqual(ldap_timedelta_2_timedelta(9000000000), expected)
