import unittest

from abstra_internals.utils.cron import cron_schedule_error


class TestCronScheduleError(unittest.TestCase):
    def test_valid_schedules_pass(self):
        for expr in [
            "0 0 * * *",  # daily
            "*/30 * * * *",  # every 30 min
            "0 9-17 * * 1-5",  # weekday business hours
            "0 0 29 2 *",  # Feb 29 — rare but valid (leap years)
        ]:
            self.assertIsNone(cron_schedule_error(expr), f"{expr!r} should be valid")

    def test_impossible_dates_are_flagged(self):
        for expr in [
            "0 0 31 2 *",  # Feb 31 — never exists
            "0 0 30 2 *",  # Feb 30 — never exists
            "0 0 31 4 *",  # Apr 31 — never exists
        ]:
            self.assertIsNotNone(
                cron_schedule_error(expr), f"{expr!r} should be flagged"
            )

    def test_malformed_is_flagged(self):
        self.assertIsNotNone(cron_schedule_error("not a cron"))
        self.assertIsNotNone(cron_schedule_error("0 0 * *"))  # too few fields

    def test_blank_schedule_is_allowed(self):
        self.assertIsNone(cron_schedule_error(""))
        self.assertIsNone(cron_schedule_error("   "))
        self.assertIsNone(cron_schedule_error(None))
