import unittest

import pytz
from datetime import datetime

from cstriggers.core.trigger import QuartzCron, Rate


class TestRateBasicSet(unittest.TestCase):
    def test_rate_minute_trigger(self):
        schedule_string = "1 minute"
        start_date = "2019-10-13T00:00:00"
        rate = Rate(
            schedule_string=schedule_string,
            start_date=start_date
        ).next_trigger(isoformat=True)

        expecting = "2019-10-13T00:01:00"

        self.assertEquals(rate, expecting)

    def test_rate_minute_trigger_multiple(self):
        schedule_string = "1 minute"
        start_date = "2019-10-13T00:00:00"
        rate = Rate(
            schedule_string=schedule_string,
            start_date=start_date
        ).next_triggers(10, isoformat=True)

        expecting = [
            '2019-10-13T00:01:00',
            '2019-10-13T00:02:00',
            '2019-10-13T00:03:00',
            '2019-10-13T00:04:00',
            '2019-10-13T00:05:00',
            '2019-10-13T00:06:00',
            '2019-10-13T00:07:00',
            '2019-10-13T00:08:00',
            '2019-10-13T00:09:00',
            '2019-10-13T00:10:00'
        ]

        self.assertEquals(rate, expecting)

    def test_rate_minutes_trigger(self):
        schedule_string = "5 minutes"
        start_date = "2019-10-13T00:00:00"
        rate = Rate(
            schedule_string=schedule_string,
            start_date=start_date
        ).next_trigger(isoformat=True)

        expecting = "2019-10-13T00:05:00"

        self.assertEquals(rate, expecting)

    def test_rate_minutes_trigger_multiple(self):
        schedule_string = "5 minutes"
        start_date = "2019-10-13T00:00:00"
        rate = Rate(
            schedule_string=schedule_string,
            start_date=start_date
        ).next_triggers(13, isoformat=True)

        expecting = [
            '2019-10-13T00:05:00',
            '2019-10-13T00:10:00',
            '2019-10-13T00:15:00',
            '2019-10-13T00:20:00',
            '2019-10-13T00:25:00',
            '2019-10-13T00:30:00',
            '2019-10-13T00:35:00',
            '2019-10-13T00:40:00',
            '2019-10-13T00:45:00',
            '2019-10-13T00:50:00',
            '2019-10-13T00:55:00',
            '2019-10-13T01:00:00',
            '2019-10-13T01:05:00'
        ]

        self.assertEquals(rate, expecting)

    def test_rate_hour_trigger(self):
        schedule_string = "1 hour"
        start_date = "2019-10-13T00:00:00"
        rate = Rate(
            schedule_string=schedule_string,
            start_date=start_date
        ).next_trigger(isoformat=True)

        expecting = "2019-10-13T01:00:00"

        self.assertEquals(rate, expecting)

    def test_rate_hour_trigger_multiple(self):
        schedule_string = "1 hour"
        start_date = "2019-10-13T00:00:00"
        rate = Rate(
            schedule_string=schedule_string,
            start_date=start_date
        ).next_triggers(13, isoformat=True)

        expecting = [
            '2019-10-13T01:00:00',
            '2019-10-13T02:00:00',
            '2019-10-13T03:00:00',
            '2019-10-13T04:00:00',
            '2019-10-13T05:00:00',
            '2019-10-13T06:00:00',
            '2019-10-13T07:00:00',
            '2019-10-13T08:00:00',
            '2019-10-13T09:00:00',
            '2019-10-13T10:00:00',
            '2019-10-13T11:00:00',
            '2019-10-13T12:00:00',
            '2019-10-13T13:00:00'
        ]

        self.assertEquals(rate, expecting)

    def test_rate_hours_trigger(self):
        schedule_string = "5 hours"
        start_date = "2019-10-13T00:00:00"
        rate = Rate(
            schedule_string=schedule_string,
            start_date=start_date
        ).next_trigger(isoformat=True)

        expecting = "2019-10-13T05:00:00"

        self.assertEquals(rate, expecting)

    def test_rate_hours_trigger_multiple(self):
        schedule_string = "5 hours"
        start_date = "2019-10-13T00:00:00"
        rate = Rate(
            schedule_string=schedule_string,
            start_date=start_date
        ).next_triggers(13, isoformat=True)

        expecting = [
            '2019-10-13T05:00:00',
            '2019-10-13T10:00:00',
            '2019-10-13T15:00:00',
            '2019-10-13T20:00:00',
            '2019-10-14T01:00:00',
            '2019-10-14T06:00:00',
            '2019-10-14T11:00:00',
            '2019-10-14T16:00:00',
            '2019-10-14T21:00:00',
            '2019-10-15T02:00:00',
            '2019-10-15T07:00:00',
            '2019-10-15T12:00:00',
            '2019-10-15T17:00:00'
        ]

        self.assertEquals(rate, expecting)

    def test_rate_day_trigger(self):
        schedule_string = "1 day"
        start_date = "2019-10-13T00:00:00"
        rate = Rate(
            schedule_string=schedule_string,
            start_date=start_date
        ).next_trigger(isoformat=True)

        expecting = "2019-10-14T00:00:00"

        self.assertEquals(rate, expecting)

    def test_rate_day_trigger_multiple(self):
        schedule_string = "1 day"
        start_date = "2019-10-13T00:00:00"
        rate = Rate(
            schedule_string=schedule_string,
            start_date=start_date
        ).next_triggers(13, isoformat=True)

        expecting = [
            '2019-10-14T00:00:00',
            '2019-10-15T00:00:00',
            '2019-10-16T00:00:00',
            '2019-10-17T00:00:00',
            '2019-10-18T00:00:00',
            '2019-10-19T00:00:00',
            '2019-10-20T00:00:00',
            '2019-10-21T00:00:00',
            '2019-10-22T00:00:00',
            '2019-10-23T00:00:00',
            '2019-10-24T00:00:00',
            '2019-10-25T00:00:00',
            '2019-10-26T00:00:00'
        ]

        self.assertEquals(rate, expecting)

    def test_rate_days_trigger(self):
        schedule_string = "5 days"
        start_date = "2019-10-13T00:00:00"
        rate = Rate(
            schedule_string=schedule_string,
            start_date=start_date
        ).next_trigger(isoformat=True)

        expecting = "2019-10-18T00:00:00"

        self.assertEquals(rate, expecting)

    def test_rate_days_trigger_multiple(self):
        schedule_string = "5 days"
        start_date = "2019-10-13T00:00:00"
        rate = Rate(
            schedule_string=schedule_string,
            start_date=start_date
        ).next_triggers(13, isoformat=True)

        expecting = [
            '2019-10-18T00:00:00',
            '2019-10-23T00:00:00',
            '2019-10-28T00:00:00',
            '2019-11-02T00:00:00',
            '2019-11-07T00:00:00',
            '2019-11-12T00:00:00',
            '2019-11-17T00:00:00',
            '2019-11-22T00:00:00',
            '2019-11-27T00:00:00',
            '2019-12-02T00:00:00',
            '2019-12-07T00:00:00',
            '2019-12-12T00:00:00',
            '2019-12-17T00:00:00'
        ]

        self.assertEquals(rate, expecting)


class TestQuartzCronBasicSet(unittest.TestCase):
    def test_every_four_months(self):
        start_time = '2019-11-01 00:00:00'
        schedule_string = "0 0 0 24 NOV,MAR,JUL ? *"

        cron_obj = QuartzCron(schedule_string=schedule_string, start_date=start_time)
        schedule = cron_obj.next_trigger(isoformat=True)
        expecting = "2019-11-24T00:00:00"

        self.assertEquals(schedule, expecting)

    def test_every_four_months_ii(self):
        start_time = '2019-12-01 00:00:00'
        schedule_string = "0 0 0 24 NOV,MAR,JUL ? *"

        cron_obj = QuartzCron(schedule_string=schedule_string, start_date=start_time)
        schedule = cron_obj.next_trigger(isoformat=True)
        expecting = "2020-03-24T00:00:00"

        self.assertEquals(schedule, expecting)

    def test_basic_cron_mostly_digits(self):
        schedule_string = "0 0 0 27 11 ? *"
        start_time = '2019-11-01T00:00:00'

        cron_obj = QuartzCron(schedule_string=schedule_string, start_date=start_time)
        schedule = cron_obj.next_trigger(isoformat=True)
        expecting = "2019-11-27T00:00:00"

        self.assertEquals(schedule, expecting)

    def test_basic_cron_no_boundaries_reached(self):
        start_time_aware = datetime(2019, 10, 31, 11, 0, 0, 0, pytz.UTC)
        end_time_aware = datetime(2020, 8, 15, 8, 15, 12, 0, pytz.UTC)
        schedule_string = "0 0 13 15 * ? *"

        cron_obj = QuartzCron(schedule_string=schedule_string, start_date=start_time_aware, end_date=end_time_aware)
        schedule = cron_obj.next_trigger(isoformat=True)

        expecting = '2019-11-15T13:00:00+00:00'

        self.assertEquals(schedule, expecting)

    def test_basic_cron_no_boundaries_reached_month_skip(self):
        schedule_string = "0 0 13 21 JAN,JUL ? *"
        start_time = '2019-11-07T00:00:00'

        cron_obj = QuartzCron(schedule_string=schedule_string, start_date=start_time)

        schedule = cron_obj.next_trigger(isoformat=True)

        expecting = '2020-01-21T13:00:00'

        self.assertEquals(schedule, expecting)

    def test_basic_cron_no_boundaries_reached_month_skip_and_specific_dow(self):
        schedule_string = "0 0 13 ? NOV,FEB,MAY,AUG MON#2 *"
        start_time = '2019-10-31T11:00:00'

        cron_obj = QuartzCron(schedule_string=schedule_string, start_date=start_time)

        schedule = cron_obj.next_trigger(isoformat=True)

        expecting = '2019-11-11T13:00:00'

        self.assertEquals(schedule, expecting)

    def test_timezone_awareness(self):
        start_time_aware = datetime(2019, 8, 15, 8, 15, 12, 0, pytz.UTC)
        end_time_aware = datetime(2020, 8, 15, 8, 15, 12, 0, pytz.UTC)
        schedule_string = "0 0 13 ? 11,12 TUE *"

        cron_obj = QuartzCron(schedule_string=schedule_string, start_date=start_time_aware, end_date=end_time_aware)
        schedule = cron_obj.next_trigger(isoformat=True)

        expecting = '2019-11-05T13:00:00+00:00'

        self.assertEquals(schedule, expecting)

    def test_timezone_awareness_ii(self):
        start_time_aware = datetime(2019, 11, 5, 13, 00, 00, 0, pytz.UTC)
        end_time_aware = datetime(2020, 8, 15, 8, 15, 12, 0, pytz.UTC)
        schedule_string = "0 0 13 ? 11,12 TUE *"

        # TODO: solve for every month variation
        # TODO: solve for every dow variation

        cron_obj = QuartzCron(schedule_string=schedule_string, start_date=start_time_aware, end_date=end_time_aware)
        schedule = cron_obj.next_trigger(isoformat=True)

        expecting = '2019-11-12T13:00:00+00:00'

        self.assertEquals(schedule, expecting)

    def test_timezone_awareness_iii(self):
        start_time_aware = datetime(2019, 12, 3, 13, 00, 00, 0, pytz.UTC)
        end_time_aware = datetime(2020, 8, 15, 8, 15, 12, 0, pytz.UTC)
        schedule_string = "0 0 13 ? 11,12 TUE *"
        # TODO: solve for every month variation
        # TODO: solve for every dow variation

        cron_obj = QuartzCron(schedule_string=schedule_string, start_date=start_time_aware, end_date=end_time_aware)
        schedule = cron_obj.next_trigger(isoformat=True)

        expecting = '2019-12-10T13:00:00+00:00'

        self.assertEquals(schedule, expecting)

    def test_timezone_awareness_multiple(self):
        start_time_aware = datetime(2019, 8, 15, 8, 15, 12, 0, pytz.UTC)
        end_time_aware = datetime(2020, 8, 15, 8, 15, 12, 0, pytz.UTC)
        schedule_string = "0 0 13 ? 11,12 TUE *"

        cron_obj = QuartzCron(schedule_string=schedule_string, start_date=start_time_aware, end_date=end_time_aware)
        schedule = cron_obj.all_triggers(isoformat=True)

        expecting = [
            '2019-11-05T13:00:00+00:00',
            '2019-11-12T13:00:00+00:00',
            '2019-11-19T13:00:00+00:00',
            '2019-11-26T13:00:00+00:00',
            '2019-12-03T13:00:00+00:00',
            '2019-12-10T13:00:00+00:00',
            '2019-12-17T13:00:00+00:00',
            '2019-12-24T13:00:00+00:00',
            '2019-12-31T13:00:00+00:00'
        ]

        self.assertEquals(schedule, expecting)

    def test_multiple_months(self):
        schedule_string = "0 0 13 1 NOV,JAN,MAR,MAY,JUL,SEP ? *"
        schedule = QuartzCron(
            schedule_string=schedule_string,
            start_date='2019-10-10T10:47:27',
            end_date='2020-04-18T10:47:27'
        ).next_trigger(isoformat=True)

        expecting = '2019-11-01T13:00:00'
        self.assertEquals(schedule, expecting)

    def test_all_triggers(self):
        schedule = QuartzCron(
            schedule_string="0 0 0 * * ? *",
            start_date='2019-10-10T10:47:27',
            end_date='2019-10-18T10:47:27'
        ).all_triggers(isoformat=True)

        expecting = [
            '2019-10-11T00:00:00',
            '2019-10-12T00:00:00',
            '2019-10-13T00:00:00',
            '2019-10-14T00:00:00',
            '2019-10-15T00:00:00',
            '2019-10-16T00:00:00',
            '2019-10-17T00:00:00',
            '2019-10-18T00:00:00'
        ]

        self.assertEquals(schedule, expecting)

    def test_every_tuesday_of_every_month(self):
        schedule_string = "0 0 13 ? * TUE *"
        start_date = "2019-10-13T00:00:00"
        end_date = "2019-12-13T00:00:00"

        cron_obj = QuartzCron(schedule_string=schedule_string, start_date=start_date, end_date=end_date)
        schedule = cron_obj.next_trigger(isoformat=True)

        expecting = '2019-10-15T13:00:00'

        self.assertEquals(schedule, expecting)

    def test_every_tuesday_of_every_month_multiple(self):
        schedule_string = "0 0 13 ? * TUE *"
        start_date = "2019-10-13T00:00:00"
        end_date = "2019-12-13T00:00:00"

        cron_obj = QuartzCron(schedule_string=schedule_string, start_date=start_date, end_date=end_date)
        schedule = cron_obj.all_triggers(isoformat=True)

        expecting = [
            '2019-10-15T13:00:00',
            '2019-10-22T13:00:00',
            '2019-10-29T13:00:00',
            '2019-11-05T13:00:00',
            '2019-11-12T13:00:00',
            '2019-11-19T13:00:00',
            '2019-11-26T13:00:00',
            '2019-12-03T13:00:00',
            '2019-12-10T13:00:00'
        ]

        self.assertEquals(schedule, expecting)

    def test_last_trigger(self):
        schedule_string = "0 0 0 1 JAN-MAR ? 2010-2015"
        start_date = "2019-10-13T00:00:00"
        end_date = "2022-10-13T00:00:00"

        with self.assertRaises(NotImplementedError):
            cron_obj = QuartzCron(schedule_string=schedule_string, start_date=start_date, end_date=end_date)
            cron_obj.last_trigger()

    def test_last_triggers(self):
        schedule_string = "0 0 0 1 JAN-MAR ? 2010-2015"
        start_date = "2019-10-13T00:00:00"
        end_date = "2022-10-13T00:00:00"

        with self.assertRaises(NotImplementedError):
            cron_obj = QuartzCron(schedule_string=schedule_string, start_date=start_date, end_date=end_date)
            cron_obj.last_triggers()

    def test_multiple_trigger_calls_after_schedule_ends(self):
        schedule_string = "0 0 0 1 JAN-MAR ? 2010-2015"
        start_date = "2019-10-13T00:00:00"
        end_date = "2022-10-13T00:00:00"

        with self.assertRaises(StopIteration):
            cron_obj = QuartzCron(schedule_string=schedule_string, start_date=start_date, end_date=end_date)
            cron_obj.next_trigger()
            cron_obj.next_trigger()
            cron_obj.next_trigger()

    def test_end_date_in_the_past(self):
        schedule_string = "0 0 0 1 JAN-MAR ? 2010-2030"
        start_date = "2019-10-13T00:00:00"
        end_date = "2015-10-13T00:00:00"

        with self.assertRaises(StopIteration):
            cron_obj = QuartzCron(schedule_string=schedule_string, start_date=start_date, end_date=end_date)
            cron_obj.next_trigger()
            cron_obj.next_trigger()
            cron_obj.next_trigger()

    def test_multiple_trigger_calls(self):
        cron = QuartzCron(
            schedule_string="0 0 0 * * ? *",
            start_date='2019-10-10T10:47:27',
            end_date='2019-10-13T10:47:28'
        )

        self.assertEquals('2019-10-11T00:00:00', cron.next_trigger(isoformat=True))
        self.assertEquals('2019-10-12T00:00:00', cron.next_trigger(isoformat=True))

    def test_end_date_usage(self):
        with self.assertRaises(StopIteration):
            QuartzCron(
                schedule_string="0 0 0 * * ? *",
                start_date='2019-10-10T10:47:27',
                end_date='2019-10-10T10:47:28'
            ).next_trigger()

    def test_end_date_usage_multi(self):
        cron = QuartzCron(
            schedule_string="0 0 0 * * ? *",
            start_date='2019-10-10T10:47:27',
            end_date='2019-10-12T10:47:27'
        ).next_triggers(10, isoformat=True)

        expecting = [
            '2019-10-11T00:00:00',
            '2019-10-12T00:00:00'
        ]

        self.assertEquals(cron, expecting)

    def test_simple_second_trigger(self):
        cron = QuartzCron(
            schedule_string="* * * * * ? *",
            start_date='2019-10-10T10:47:27',
            end_date=None
        ).next_trigger()

        expecting = '2019-10-10T10:47:28'

        self.assertEquals(cron.isoformat(), expecting)

    def test_simple_minute_trigger(self):
        cron = QuartzCron(
            schedule_string="0 * * * * ? *",
            start_date='2019-10-10T10:47:27',
            end_date=None
        ).next_trigger()

        expecting = '2019-10-10T10:48:00'

        self.assertEquals(cron.isoformat(), expecting)

    def test_simple_hour_trigger(self):
        cron = QuartzCron(
            schedule_string="0 0 * * * ? *",
            start_date='2019-10-10T10:47:27',
            end_date=None
        ).next_trigger()

        expecting = '2019-10-10T11:00:00'

        self.assertEquals(cron.isoformat(), expecting)

    def test_simple_day_trigger(self):
        cron = QuartzCron(
            schedule_string="0 0 0 * * ? *",
            start_date='2019-10-10T10:47:27',
            end_date=None
        ).next_trigger()

        expecting = '2019-10-11T00:00:00'

        self.assertEquals(cron.isoformat(), expecting)

    def test_simple_month_trigger(self):
        cron = QuartzCron(
            schedule_string="0 0 0 1 * ? *",
            start_date='2019-10-10T10:47:27',
            end_date=None
        ).next_trigger()

        expecting = '2019-11-01T00:00:00'

        self.assertEquals(cron.isoformat(), expecting)

    def test_simple_dow_trigger(self):
        cron = QuartzCron(
            schedule_string="0 0 0 ? * MON *",
            start_date='2019-10-10T10:47:27',
            end_date=None
        ).next_trigger()

        expecting = '2019-10-14T00:00:00'

        self.assertEquals(cron.isoformat(), expecting)

    def test_simple_year_trigger(self):
        cron = QuartzCron(
            schedule_string="0 0 0 1 1 ? *",
            start_date='2019-10-10T10:47:27',
            end_date=None
        ).next_trigger()

        expecting = '2020-01-01T00:00:00'

        self.assertEquals(cron.isoformat(), expecting)


class TestQuartzCronHourSet(unittest.TestCase):
    def test_hour_every_12_hours(self):
        cron = QuartzCron(
            schedule_string="0 0 0/12 1/1 * ? *",
            start_date='2019-12-31T13:47:27',
            end_date=None
        ).next_trigger()

        expecting = '2020-01-01T00:00:00'

        self.assertEquals(cron.isoformat(), expecting)

    def test_hour_every_12_hours_multiple(self):
        cron = QuartzCron(
            schedule_string="0 0 0/12 1/1 * ? *",
            start_date='2019-12-31T13:47:27',
            end_date=None
        ).next_triggers(10, isoformat=True)

        expecting = [
            '2020-01-01T00:00:00',
            '2020-01-01T12:00:00',
            '2020-01-02T00:00:00',
            '2020-01-02T12:00:00',
            '2020-01-03T00:00:00',
            '2020-01-03T12:00:00',
            '2020-01-04T00:00:00',
            '2020-01-04T12:00:00',
            '2020-01-05T00:00:00',
            '2020-01-05T12:00:00'
        ]

        self.assertEquals(cron, expecting)

    def test_hour_every_6_hours(self):
        cron = QuartzCron(
            schedule_string="0 0 0/6 1/1 * ? *",
            start_date='2019-12-31T10:47:27',
            end_date=None
        ).next_trigger()

        expecting = '2019-12-31T12:00:00'

        self.assertEquals(cron.isoformat(), expecting)

    def test_hour_every_6_hours_ending_on_00_00_00(self):
        cron = QuartzCron(
            schedule_string="0 0 0/6 1/1 * ? *",
            start_date='2019-12-31T18:00:00',
            end_date=None
        ).next_trigger()

        expecting = '2020-01-01T00:00:00'

        self.assertEquals(cron.isoformat(), expecting)

    def test_hour_every_6_hours_multiple(self):
        cron = QuartzCron(
            schedule_string="0 0 0/6 1/1 * ? *",
            start_date='2019-12-31T10:47:27',
            end_date=None
        ).next_triggers(10, isoformat=True)

        expecting = [
            '2019-12-31T12:00:00',
            '2019-12-31T18:00:00',
            '2020-01-01T00:00:00',
            '2020-01-01T06:00:00',
            '2020-01-01T12:00:00',
            '2020-01-01T18:00:00',
            '2020-01-02T00:00:00',
            '2020-01-02T06:00:00',
            '2020-01-02T12:00:00',
            '2020-01-02T18:00:00',
        ]

        self.assertEquals(cron, expecting)


class TestQuartzCronDaySet(unittest.TestCase):
    def test_day_between_friday_and_monday(self):
        cron = QuartzCron(
            schedule_string="0 0 0 ? * MON-FRI *",
            start_date='2019-10-13T15:47:27',
            end_date=None
        ).next_trigger()

        expecting = '2019-10-14T00:00:00'

        self.assertEquals(cron.isoformat(), expecting)

    def test_day_between_friday_and_monday_multiple(self):
        cron = QuartzCron(
            schedule_string="0 0 0 ? * MON-FRI *",
            start_date='2019-10-13T15:47:27',
            end_date=None
        ).next_triggers(10, isoformat=True)

        expecting = [
            '2019-10-14T00:00:00',
            '2019-10-15T00:00:00',
            '2019-10-16T00:00:00',
            '2019-10-17T00:00:00',
            '2019-10-18T00:00:00',
            '2019-10-21T00:00:00',
            '2019-10-22T00:00:00',
            '2019-10-23T00:00:00',
            '2019-10-24T00:00:00',
            '2019-10-25T00:00:00'
        ]

        self.assertEquals(cron, expecting)

    def test_day_every_day_of_week(self):
        cron = QuartzCron(
            schedule_string="0 0 12 ? * MON,TUE,WED,THU,FRI,SAT,SUN *",
            start_date='2019-10-11T10:00:00',
            end_date=None
        ).next_trigger()

        expecting = '2019-10-11T12:00:00'

        self.assertEquals(cron.isoformat(), expecting)

    def test_day_every_day_of_week_ii(self):
        cron = QuartzCron(
            schedule_string="0 0 12 ? * MON,TUE,WED,THU,FRI,SAT,SUN *",
            start_date='2019-10-11T13:00:00',
            end_date=None
        ).next_trigger()

        expecting = '2019-10-12T12:00:00'

        self.assertEquals(cron.isoformat(), expecting)

    def test_day_every_day_of_week_multiple(self):
        cron = QuartzCron(
            schedule_string="0 0 12 ? * MON,TUE,WED,THU,FRI,SAT,SUN *",
            start_date='2019-10-11T10:00:00',
            end_date=None
        ).next_triggers(10, isoformat=True)

        expecting = [
            '2019-10-11T12:00:00',
            '2019-10-12T12:00:00',
            '2019-10-13T12:00:00',
            '2019-10-14T12:00:00',
            '2019-10-15T12:00:00',
            '2019-10-16T12:00:00',
            '2019-10-17T12:00:00',
            '2019-10-18T12:00:00',
            '2019-10-19T12:00:00',
            '2019-10-20T12:00:00'
        ]

        self.assertEquals(cron, expecting)

    def test_day_skip_to_sat(self):
        cron = QuartzCron(
            schedule_string="0 0 12 ? * TUE,THU,SAT *",
            start_date='2019-10-12T12:00:00',
            end_date=None
        ).next_trigger()

        expecting = '2019-10-15T12:00:00'

        self.assertEquals(cron.isoformat(), expecting)

    def test_day_not_quite_ready_to_skip_to_sat(self):
        cron = QuartzCron(
            schedule_string="0 0 12 ? * TUE,THU,SAT *",
            start_date='2019-10-12T10:00:00',
            end_date=None
        ).next_trigger()

        expecting = '2019-10-12T12:00:00'

        self.assertEquals(cron.isoformat(), expecting)

    def test_day_skip_to_sat_multiple(self):
        cron = QuartzCron(
            schedule_string="0 0 12 ? * TUE,THU,SAT *",
            start_date='2019-10-12T10:00:00',
            end_date=None
        ).next_triggers(5, isoformat=True)

        expecting = [
            '2019-10-12T12:00:00',
            '2019-10-15T12:00:00',
            '2019-10-17T12:00:00',
            '2019-10-19T12:00:00',
            '2019-10-22T12:00:00',
        ]

        self.assertEquals(cron, expecting)

    def test_day_single_skip_month_spill_over(self):
        cron = QuartzCron(
            schedule_string="0 0 0 * * ? *",
            start_date='2019-10-31T10:47:27',
            end_date=None
        ).next_trigger()

        expecting = '2019-11-01T00:00:00'

        self.assertEquals(cron.isoformat(), expecting)

    def test_day_single_skip_month_spill_over_multiple(self):
        cron = QuartzCron(
            schedule_string="0 0 0 * * ? *",
            start_date='2019-10-31T10:47:27',
            end_date=None
        ).next_triggers(5, isoformat=True)

        expecting = [
            '2019-11-01T00:00:00',
            '2019-11-02T00:00:00',
            '2019-11-03T00:00:00',
            '2019-11-04T00:00:00',
            '2019-11-05T00:00:00'
        ]

        self.assertEquals(cron, expecting)

    def test_day_multiple_skip_month_spill_over(self):
        cron = QuartzCron(
            schedule_string="0 0 0 1/8 * ? *",
            start_date='2019-10-27T10:47:27',
            end_date=None
        ).next_trigger()

        expecting = '2019-11-01T00:00:00'

        self.assertEquals(cron.isoformat(), expecting)

    def test_day_multiple_skip_month_spill_over_multiple(self):
        cron = QuartzCron(
            schedule_string="0 0 0 1/8 * ? *",
            start_date='2019-10-27T10:47:27',
            end_date=None
        ).next_triggers(5, isoformat=True)

        expecting = [
            '2019-11-01T00:00:00',
            '2019-11-09T00:00:00',
            '2019-11-17T00:00:00',
            '2019-11-25T00:00:00',
            '2019-12-01T00:00:00'
        ]

        self.assertEquals(cron, expecting)

    def test_day_friday_only(self):
        cron = QuartzCron(
            schedule_string="0 0 9 ? * FRI *",
            start_date='2019-10-11T09:00:00',
            end_date=None
        ).next_trigger()

        expecting = '2019-10-18T09:00:00'

        self.assertEquals(cron.isoformat(), expecting)

    def test_day_friday_only_multiple(self):
        cron = QuartzCron(
            schedule_string="0 0 9 ? * FRI *",
            start_date='2019-10-11T09:00:00',
            end_date=None
        ).next_triggers(5, isoformat=True)

        expecting = [
            '2019-10-18T09:00:00',
            '2019-10-25T09:00:00',
            '2019-11-01T09:00:00',
            '2019-11-08T09:00:00',
            '2019-11-15T09:00:00'
        ]

        self.assertEquals(cron, expecting)

    def test_day_skip_to_sunday(self):
        cron = QuartzCron(
            schedule_string="0 0 0 ? * SUN *",
            start_date='2019-10-27T10:47:27',
            end_date=None
        ).next_trigger()

        expecting = '2019-11-03T00:00:00'

        self.assertEquals(cron.isoformat(), expecting)

    def test_day_skip_to_sunday_the_first(self):
        cron = QuartzCron(
            schedule_string="0 0 0 ? * SUN *",
            start_date='2019-11-24T00:00:00',
            end_date=None
        ).next_trigger()

        expecting = '2019-12-01T00:00:00'

        self.assertEquals(cron.isoformat(), expecting)

    def test_day_skip_to_sunday_multiple(self):
        cron = QuartzCron(
            schedule_string="0 0 0 ? * SUN *",
            start_date='2019-10-27T10:47:27',
            end_date=None
        ).next_triggers(5, isoformat=True)

        expecting = [
            '2019-11-03T00:00:00',
            '2019-11-10T00:00:00',
            '2019-11-17T00:00:00',
            '2019-11-24T00:00:00',
            '2019-12-01T00:00:00'
        ]

        self.assertEquals(cron, expecting)

    def test_day_weekdays_friday_skips_to_monday(self):
        cron = QuartzCron(
            schedule_string="0 0 0 ? * MON-FRI *",
            start_date='2019-10-11T10:47:27',
            end_date=None
        ).next_trigger()

        expecting = '2019-10-14T00:00:00'

        self.assertEquals(cron.isoformat(), expecting)

    def test_day_weekdays_friday_skips_to_monday_multiple(self):
        cron = QuartzCron(
            schedule_string="0 0 0 ? * MON-FRI *",
            start_date='2019-10-11T10:47:27',
            end_date=None
        ).next_triggers(5, isoformat=True)

        expecting = [
            '2019-10-14T00:00:00',
            '2019-10-15T00:00:00',
            '2019-10-16T00:00:00',
            '2019-10-17T00:00:00',
            '2019-10-18T00:00:00'
        ]

        self.assertEquals(cron, expecting)

    def test_day_first_monday(self):
        cron = QuartzCron(
            schedule_string="0 0 0 ? * MON#1 *",
            start_date='2019-10-11T10:47:27',
            end_date=None
        ).next_trigger()

        expecting = '2019-11-04T00:00:00'

        self.assertEquals(cron.isoformat(), expecting)

    def test_day_first_monday_multiple(self):
        cron = QuartzCron(
            schedule_string="0 0 0 ? * MON#1 *",
            start_date='2019-10-11T10:47:27',
            end_date=None
        ).next_triggers(5, isoformat=True)

        expecting = [
            '2019-11-04T00:00:00',
            '2019-12-02T00:00:00',
            '2020-01-06T00:00:00',
            '2020-02-03T00:00:00',
            '2020-03-02T00:00:00'
        ]

        self.assertEquals(cron, expecting)

    def test_day_second_monday(self):
        cron = QuartzCron(
            schedule_string="0 0 0 ? * MON#2 *",
            start_date='2019-10-11T10:47:27',
            end_date=None
        ).next_trigger()

        expecting = '2019-10-14T00:00:00'

        self.assertEquals(cron.isoformat(), expecting)

    def test_day_second_monday_multiple(self):
        cron = QuartzCron(
            schedule_string="0 0 0 ? * MON#2 *",
            start_date='2019-10-11T10:47:27',
            end_date=None
        ).next_triggers(5, isoformat=True)

        expecting = [
            '2019-10-14T00:00:00',
            '2019-11-11T00:00:00',
            '2019-12-09T00:00:00',
            '2020-01-13T00:00:00',
            '2020-02-10T00:00:00'
        ]

        self.assertEquals(cron, expecting)

    def test_day_third_monday(self):
        cron = QuartzCron(
            schedule_string="0 0 0 ? * MON#3 *",
            start_date='2019-10-11T10:47:27',
            end_date=None
        ).next_trigger()

        expecting = '2019-10-21T00:00:00'

        self.assertEquals(cron.isoformat(), expecting)

    def test_day_third_monday_multiple(self):
        cron = QuartzCron(
            schedule_string="0 0 0 ? * MON#3 *",
            start_date='2019-10-11T10:47:27',
            end_date=None
        ).next_triggers(5, isoformat=True)

        expecting = [
            '2019-10-21T00:00:00',
            '2019-11-18T00:00:00',
            '2019-12-16T00:00:00',
            '2020-01-20T00:00:00',
            '2020-02-17T00:00:00'
        ]

        self.assertEquals(cron, expecting)

    def test_day_fourth_monday(self):
        cron = QuartzCron(
            schedule_string="0 0 0 ? * MON#4 *",
            start_date='2019-10-11T10:47:27',
            end_date=None
        ).next_trigger()

        expecting = '2019-10-28T00:00:00'

        self.assertEquals(cron.isoformat(), expecting)

    def test_day_fourth_monday_multiple(self):
        cron = QuartzCron(
            schedule_string="0 0 0 ? * MON#4 *",
            start_date='2019-10-11T10:47:27',
            end_date=None
        ).next_triggers(5, isoformat=True)

        expecting = [
            '2019-10-28T00:00:00',
            '2019-11-25T00:00:00',
            '2019-12-23T00:00:00',
            '2020-01-27T00:00:00',
            '2020-02-24T00:00:00'
        ]

        self.assertEquals(cron, expecting)

    def test_day_fifth_monday(self):
        cron = QuartzCron(
            schedule_string="0 0 0 ? * MON#5 *",
            start_date='2019-10-11T10:47:27',
            end_date=None
        ).next_trigger()

        expecting = '2019-12-30T00:00:00'

        self.assertEquals(cron.isoformat(), expecting)

    def test_day_fifth_monday_multiple(self):
        cron = QuartzCron(
            schedule_string="0 0 0 ? * MON#5 *",
            start_date='2019-10-11T10:47:27',
            end_date=None
        ).next_triggers(5, isoformat=True)

        expecting = [
            '2019-12-30T00:00:00',
            '2020-03-30T00:00:00',
            '2020-06-29T00:00:00',
            '2020-08-31T00:00:00',
            '2020-11-30T00:00:00'
        ]

        self.assertEquals(cron, expecting)

    def test_day_last_monday(self):
        cron = QuartzCron(
            schedule_string="0 0 0 ? * MONL *",
            start_date='2019-10-11T10:47:27',
            end_date=None
        ).next_trigger()

        expecting = '2019-10-28T00:00:00'

        self.assertEquals(cron.isoformat(), expecting)

    def test_day_last_monday_multiple(self):
        cron = QuartzCron(
            schedule_string="0 0 0 ? * MONL *",
            start_date='2019-10-11T10:47:27',
            end_date=None
        ).next_triggers(5, isoformat=True)

        expecting = [
            '2019-10-28T00:00:00',
            '2019-11-25T00:00:00',
            '2019-12-30T00:00:00',
            '2020-01-27T00:00:00',
            '2020-02-24T00:00:00'
        ]

        self.assertEquals(cron, expecting)

    def test_day_last_weekday(self):
        cron = QuartzCron(
            schedule_string="0 0 0 LW * ? *",
            start_date='2019-11-11T10:47:27',
            end_date=None
        ).next_trigger()

        expecting = '2019-11-29T00:00:00'

        self.assertEquals(cron.isoformat(), expecting)

    def test_day_last_weekday_multiple(self):
        cron = QuartzCron(
            schedule_string="0 0 0 LW * ? *",
            start_date='2019-11-11T10:47:27',
            end_date=None
        ).next_triggers(5, isoformat=True)

        expecting = [
            '2019-11-29T00:00:00',
            '2019-12-31T00:00:00',
            '2020-01-31T00:00:00',
            '2020-02-28T00:00:00',
            '2020-03-31T00:00:00'
        ]

        self.assertEquals(cron, expecting)

    def test_day_last_day(self):
        cron = QuartzCron(
            schedule_string="0 0 0 L * ? *",
            start_date='2019-10-11T10:47:27',
            end_date=None
        ).next_trigger()

        expecting = '2019-10-31T00:00:00'

        self.assertEquals(cron.isoformat(), expecting)

    def test_day_last_day_multiple(self):
        cron = QuartzCron(
            schedule_string="0 0 0 L * ? *",
            start_date='2019-10-11T10:47:27',
            end_date=None
        ).next_triggers(5, isoformat=True)

        expecting = [
            '2019-10-31T00:00:00',
            '2019-11-30T00:00:00',
            '2019-12-31T00:00:00',
            '2020-01-31T00:00:00',
            '2020-02-29T00:00:00'
        ]

        self.assertEquals(cron, expecting)

    def test_day_start_3rd_every_4th_day(self):
        cron = QuartzCron(
            schedule_string="0 0 0 3/4 * ? *",
            start_date='2019-10-11T10:47:27',
            end_date=None
        ).next_trigger()

        expecting = '2019-10-15T00:00:00'

        self.assertEquals(cron.isoformat(), expecting)

    def test_day_start_3rd_every_4th_day_mutiple(self):
        cron = QuartzCron(
            schedule_string="0 0 0 3/4 * ? *",
            start_date='2019-10-11T10:47:27',
            end_date=None
        ).next_triggers(5, isoformat=True)

        expecting = [
            '2019-10-15T00:00:00',
            '2019-10-19T00:00:00',
            '2019-10-23T00:00:00',
            '2019-10-27T00:00:00',
            '2019-10-31T00:00:00'
        ]

        self.assertEquals(cron, expecting)

    def test_day_start_31st_every_day(self):
        cron = QuartzCron(
            schedule_string="0 0 0 31/1 * ? *",
            start_date='2019-11-11T10:47:27',
            end_date=None
        ).next_trigger()

        expecting = '2019-12-31T00:00:00'

        self.assertEquals(cron.isoformat(), expecting)

    def test_day_start_31st_every_day_multiple(self):
        cron = QuartzCron(
            schedule_string="0 0 0 31/1 * ? *",
            start_date='2019-11-11T10:47:27',
            end_date=None
        ).next_triggers(5, isoformat=True)

        expecting = [
            '2019-12-31T00:00:00',
            '2020-01-31T00:00:00',
            '2020-03-31T00:00:00',
            '2020-05-31T00:00:00',
            '2020-07-31T00:00:00'
        ]
        self.assertEquals(cron, expecting)

    def test_day_start_31st_every_day_ordinal_support(self):
        cron = QuartzCron(
            schedule_string="0 0 0 31/31 * ? *",
            start_date='2019-11-11T10:47:27',
            end_date=None
        ).next_trigger()

        expecting = '2019-12-31T00:00:00'

        self.assertEquals(cron.isoformat(), expecting)

    def test_day_start_31st_every_day_ordinal_support_starting_jan_2020(self):
        cron = QuartzCron(
            schedule_string="0 0 0 31/31 * ? *",
            start_date='2020-01-31T00:00:00',
            end_date=None
        ).next_trigger()

        expecting = '2020-03-31T00:00:00'

        self.assertEquals(cron.isoformat(), expecting)

    def test_day_start_31st_every_day_ordinal_support_multiple(self):
        cron = QuartzCron(
            schedule_string="0 0 0 31/31 * ? *",
            start_date='2019-11-11T10:47:27',
            end_date=None
        ).next_triggers(5, isoformat=True)

        expecting = [
            '2019-12-31T00:00:00',
            '2020-01-31T00:00:00',
            '2020-03-31T00:00:00',
            '2020-05-31T00:00:00',
            '2020-07-31T00:00:00'
        ]

        self.assertEquals(cron, expecting)

    def test_day_first_weekday(self):
        cron = QuartzCron(
            schedule_string="0 0 0 1W * ? *",
            start_date='2019-11-11T10:47:27',
            end_date=None
        ).next_trigger()

        expecting = '2019-12-02T00:00:00'

        self.assertEquals(cron.isoformat(), expecting)

    def test_day_first_weekday_starting_on_weekday(self):
        cron = QuartzCron(
            schedule_string="0 0 0 1W * ? *",
            start_date='2019-12-02T00:00:00',
            end_date=None
        ).next_trigger()

        expecting = '2020-01-01T00:00:00'

        self.assertEquals(cron.isoformat(), expecting)

    def test_day_first_weekday_multiple(self):
        cron = QuartzCron(
            schedule_string="0 0 0 1W * ? *",
            start_date='2019-11-11T10:47:27',
            end_date=None
        ).next_triggers(5, isoformat=True)

        expecting = [
            '2019-12-02T00:00:00',
            '2020-01-01T00:00:00',
            '2020-02-03T00:00:00',
            '2020-03-02T00:00:00',
            '2020-04-01T00:00:00'
        ]

        self.assertEquals(cron, expecting)


class TestQuartzCronMonthSet(unittest.TestCase):
    def test_month_every_month(self):
        cron = QuartzCron(
            schedule_string="0 0 0 1 1/1 ? *",
            start_date='2019-11-13T12:47:27',
            end_date=None
        ).next_trigger()

        expecting = '2019-12-01T00:00:00'

        self.assertEquals(cron.isoformat(), expecting)

        cron = QuartzCron(
            schedule_string="0 0 0 1 * ? *",
            start_date='2019-11-13T12:47:27',
            end_date=None
        ).next_trigger()

        self.assertEquals(cron.isoformat(), expecting)

    def test_month_every_month_multiple(self):
        cron = QuartzCron(
            schedule_string="0 0 0 1 1/1 ? *",
            start_date='2019-11-13T12:47:27',
            end_date=None
        ).next_triggers(5, isoformat=True)

        expecting = [
            '2019-12-01T00:00:00',
            '2020-01-01T00:00:00',
            '2020-02-01T00:00:00',
            '2020-03-01T00:00:00',
            '2020-04-01T00:00:00'
        ]

        self.assertEquals(cron, expecting)

        cron = QuartzCron(
            schedule_string="0 0 0 1 * ? *",
            start_date='2019-11-13T12:47:27',
            end_date=None
        ).next_triggers(5, isoformat=True)

        self.assertEquals(cron, expecting)

    def test_month_every_6_months(self):
        cron = QuartzCron(
            schedule_string="0 0 12 15 1/6 ? *",
            start_date='2019-03-15T23:00:00',
            end_date=None
        ).next_trigger()

        expecting = '2019-07-15T12:00:00'

        self.assertEquals(cron.isoformat(), expecting)

    def test_month_every_6_months_multiple(self):
        cron = QuartzCron(
            schedule_string="0 0 12 15 1/6 ? *",
            start_date='2019-03-15T23:00:00',
            end_date=None
        ).next_triggers(5, isoformat=True)

        expecting = [
            '2019-07-15T12:00:00',
            '2020-01-15T12:00:00',
            '2020-07-15T12:00:00',
            '2021-01-15T12:00:00',
            '2021-07-15T12:00:00'
        ]

        self.assertEquals(cron, expecting)

    def test_month_march_only(self):
        cron = QuartzCron(
            schedule_string="0 0 0 1 MAR ? *",
            start_date='2019-10-13T17:00:00',
            end_date=None
        ).next_trigger()

        expecting = '2020-03-01T00:00:00'

        self.assertEquals(cron.isoformat(), expecting)

    def test_month_march_only_multiple(self):
        cron = QuartzCron(
            schedule_string="0 0 0 1 MAR ? *",
            start_date='2019-10-13T17:00:00',
            end_date=None
        ).next_triggers(5, isoformat=True)

        expecting = [
            '2020-03-01T00:00:00',
            '2021-03-01T00:00:00',
            '2022-03-01T00:00:00',
            '2023-03-01T00:00:00',
            '2024-03-01T00:00:00'
        ]

        self.assertEquals(cron, expecting)

    def test_month_jan_feb_dec_only(self):
        cron = QuartzCron(
            schedule_string="0 0 0 1 DEC,JAN,FEB ? *",
            start_date='2019-10-13T00:00:00',
            end_date=None
        ).next_trigger()

        expecting = '2019-12-01T00:00:00'

        self.assertEquals(cron.isoformat(), expecting)

    def test_month_jan_feb_dec_only_multiple(self):
        cron = QuartzCron(
            schedule_string="0 0 0 1 DEC,JAN,FEB ? *",
            start_date='2019-10-13T00:00:00',
            end_date=None
        ).next_triggers(5, isoformat=True)

        expecting = [
            '2019-12-01T00:00:00',
            '2020-01-01T00:00:00',
            '2020-02-01T00:00:00',
            '2020-12-01T00:00:00',
            '2021-01-01T00:00:00'
        ]

        self.assertEquals(cron, expecting)

    def test_month_jan_feb_mar_only_via_comma(self):
        cron = QuartzCron(
            schedule_string="0 0 0 1 JAN,FEB,MAR ? *",
            start_date='2019-10-13T00:00:00',
            end_date=None
        ).next_trigger()

        expecting = '2020-01-01T00:00:00'

        self.assertEquals(cron.isoformat(), expecting)

    def test_month_jan_feb_mar_starting_feb(self):
        cron = QuartzCron(
            schedule_string="0 0 0 1 JAN,FEB,MAR ? *",
            start_date='2020-02-01T00:00:00',
        ).next_trigger()

        expecting = '2020-03-01T00:00:00'

        self.assertEquals(cron.isoformat(), expecting)

    def test_month_jan_feb_mar_only_via_comma_multiple(self):
        cron = QuartzCron(
            schedule_string="0 0 0 1 JAN,FEB,MAR ? *",
            start_date='2019-10-13T00:00:00',
        ).next_triggers(5, isoformat=True)

        expecting = [
            '2020-01-01T00:00:00',
            '2020-02-01T00:00:00',
            '2020-03-01T00:00:00',
            '2021-01-01T00:00:00',
            '2021-02-01T00:00:00'
        ]

        self.assertEquals(cron, expecting)

    def test_month_jan_feb_mar_only_via_minus(self):
        cron = QuartzCron(
            schedule_string="0 0 0 1 JAN-MAR ? *",
            start_date='2019-10-13T00:00:00',
            end_date=None
        ).next_trigger()

        expecting = '2020-01-01T00:00:00'

        self.assertEquals(cron.isoformat(), expecting)

    def test_month_jan_feb_mar_only_via_minus_multiple(self):
        cron = QuartzCron(
            schedule_string="0 0 0 1 JAN-MAR ? *",
            start_date='2019-10-13T00:00:00',
            end_date=None
        ).next_triggers(5, isoformat=True)

        expecting = [
            '2020-01-01T00:00:00',
            '2020-02-01T00:00:00',
            '2020-03-01T00:00:00',
            '2021-01-01T00:00:00',
            '2021-02-01T00:00:00'
        ]

        self.assertEquals(cron, expecting)


class TestQuartzCronYearSet(unittest.TestCase):
    def test_year_range(self):
        cron = QuartzCron(
            schedule_string="0 0 0 1 JAN-MAR ? 1970-2099",
            start_date='2019-10-13T00:00:00',
            end_date=None
        ).next_trigger()

        expecting = '2020-01-01T00:00:00'

        self.assertEquals(cron.isoformat(), expecting)

    def test_year_range_multiple(self):
        cron = QuartzCron(
            schedule_string="0 0 0 1 JAN-MAR ? 1970-2099",
            start_date='2019-10-13T00:00:00',
            end_date=None
        ).next_triggers(5, isoformat=True)

        expecting = [
            '2020-01-01T00:00:00',
            '2020-02-01T00:00:00',
            '2020-03-01T00:00:00',
            '2021-01-01T00:00:00',
            '2021-02-01T00:00:00'
        ]

        self.assertEquals(cron, expecting)

    def test_year_future_only(self):
        cron = QuartzCron(
            schedule_string="0 0 0 1 JAN-MAR ? 2030-2099",
            start_date='2019-10-13T00:00:00',
            end_date=None
        ).next_trigger()

        expecting = '2030-01-01T00:00:00'

        self.assertEquals(cron.isoformat(), expecting)

    def test_year_future_only_multiple(self):
        cron = QuartzCron(
            schedule_string="0 0 0 1 JAN-MAR ? 2030-2099",
            start_date='2019-10-13T00:00:00',
            end_date=None
        ).next_triggers(5, isoformat=True)

        expecting = [
            '2030-01-01T00:00:00',
            '2030-02-01T00:00:00',
            '2030-03-01T00:00:00',
            '2031-01-01T00:00:00',
            '2031-02-01T00:00:00'
        ]

        self.assertEquals(cron, expecting)

    def test_year_past_only(self):
        with self.assertRaises(StopIteration):
            QuartzCron(
                schedule_string="0 0 0 1 JAN-MAR ? 2010-2015",
                start_date='2019-10-13T00:00:00',
                end_date=None
            ).next_trigger()

    def test_year_past_only_multiple(self):
        cron = QuartzCron(
            schedule_string="0 0 0 1 JAN-MAR ? 2010-2015",
            start_date='2019-10-13T00:00:00',
            end_date=None
        ).next_triggers(5)

        self.assertEquals(cron, [])


if __name__ == '__main__':
    unittest.main()
