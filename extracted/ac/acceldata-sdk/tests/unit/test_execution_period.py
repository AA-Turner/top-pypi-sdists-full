import unittest
from datetime import datetime, timedelta
from acceldata_sdk.time_range_utils import TimeRangeCalculator
from acceldata_sdk.models.ruleExecutionResult import ExecutionPeriod
from acceldata_sdk.models.ruleExecutionResult import PolicyFilter
from dateutil.relativedelta import relativedelta

class TestCalculateTimeRange(unittest.TestCase):
    def test_last15minutes(self):
        filter = PolicyFilter(period=ExecutionPeriod.Last15minutes)
        finished_before, started_after = TimeRangeCalculator.calculate_time_range(filter)
        expected_finished_before = datetime.now()
        expected_started_after = expected_finished_before - timedelta(minutes=15)
        print("ExecutionPeriod.Last15minutes")
        print("started_after: "+str(started_after))
        print("finished_before: "+str(finished_before))
        print("===========================================")
        self.assertEqual(finished_before.year, expected_finished_before.year)
        self.assertEqual(finished_before.month, expected_finished_before.month)
        self.assertEqual(finished_before.day, expected_finished_before.day)
        self.assertEqual(finished_before.hour, expected_finished_before.hour)
        self.assertEqual(finished_before.minute, expected_finished_before.minute)
        self.assertEqual(started_after.year, expected_started_after.year)
        self.assertEqual(started_after.month, expected_started_after.month)
        self.assertEqual(started_after.day, expected_started_after.day)
        self.assertEqual(started_after.hour, expected_started_after.hour)
        self.assertEqual(started_after.minute, expected_started_after.minute)

    def test_last30minutes(self):
        filter = PolicyFilter(period=ExecutionPeriod.Last30minutes)
        finished_before, started_after = TimeRangeCalculator.calculate_time_range(filter)
        expected_finished_before = datetime.now()
        expected_started_after = expected_finished_before - timedelta(minutes=30)
        print("ExecutionPeriod.Last30minutes")
        print("started_after: "+str(started_after))
        print("finished_before: "+str(finished_before))
        print("===========================================")
        self.assertEqual(finished_before.year, expected_finished_before.year)
        self.assertEqual(finished_before.month, expected_finished_before.month)
        self.assertEqual(finished_before.day, expected_finished_before.day)
        self.assertEqual(finished_before.hour, expected_finished_before.hour)
        self.assertEqual(finished_before.minute, expected_finished_before.minute)
        self.assertEqual(started_after.year, expected_started_after.year)
        self.assertEqual(started_after.month, expected_started_after.month)
        self.assertEqual(started_after.day, expected_started_after.day)
        self.assertEqual(started_after.hour, expected_started_after.hour)
        self.assertEqual(started_after.minute, expected_started_after.minute)

    def test_last_1_hour(self):
        filter = PolicyFilter(period=ExecutionPeriod.Last1hour)
        finished_before, started_after = TimeRangeCalculator.calculate_time_range(filter)
        expected_finished_before = datetime.now()
        expected_started_after = expected_finished_before - timedelta(hours=1)
        print("ExecutionPeriod.Last1hour")
        print("started_after: "+str(started_after))
        print("finished_before: "+str(finished_before))
        print("===========================================")
        self.assertEqual(finished_before.year, expected_finished_before.year)
        self.assertEqual(finished_before.month, expected_finished_before.month)
        self.assertEqual(finished_before.day, expected_finished_before.day)
        self.assertEqual(finished_before.hour, expected_finished_before.hour)
        self.assertEqual(finished_before.minute, expected_finished_before.minute)
        self.assertEqual(started_after.year, expected_started_after.year)
        self.assertEqual(started_after.month, expected_started_after.month)
        self.assertEqual(started_after.day, expected_started_after.day)
        self.assertEqual(started_after.hour, expected_started_after.hour)
        self.assertEqual(started_after.minute, expected_started_after.minute)

    def test_last_3_hour(self):
        filter = PolicyFilter(period=ExecutionPeriod.Last3hours)
        finished_before, started_after = TimeRangeCalculator.calculate_time_range(filter)
        expected_finished_before = datetime.now()
        expected_started_after = expected_finished_before - timedelta(hours=3)
        print("ExecutionPeriod.Last3hours")
        print("started_after: "+str(started_after))
        print("finished_before: "+str(finished_before))
        print("===========================================")
        self.assertEqual(finished_before.year, expected_finished_before.year)
        self.assertEqual(finished_before.month, expected_finished_before.month)
        self.assertEqual(finished_before.day, expected_finished_before.day)
        self.assertEqual(finished_before.hour, expected_finished_before.hour)
        self.assertEqual(finished_before.minute, expected_finished_before.minute)
        self.assertEqual(started_after.year, expected_started_after.year)
        self.assertEqual(started_after.month, expected_started_after.month)
        self.assertEqual(started_after.day, expected_started_after.day)
        self.assertEqual(started_after.hour, expected_started_after.hour)
        self.assertEqual(started_after.minute, expected_started_after.minute)

    def test_last_6_hour(self):
        filter = PolicyFilter(period=ExecutionPeriod.Last6hours)
        finished_before, started_after = TimeRangeCalculator.calculate_time_range(filter)
        expected_finished_before = datetime.now()
        expected_started_after = expected_finished_before - timedelta(hours=6)
        print("ExecutionPeriod.Last6hours")
        print("started_after: "+str(started_after))
        print("finished_before: "+str(finished_before))
        print("===========================================")
        self.assertEqual(finished_before.year, expected_finished_before.year)
        self.assertEqual(finished_before.month, expected_finished_before.month)
        self.assertEqual(finished_before.day, expected_finished_before.day)
        self.assertEqual(finished_before.hour, expected_finished_before.hour)
        self.assertEqual(finished_before.minute, expected_finished_before.minute)
        self.assertEqual(started_after.year, expected_started_after.year)
        self.assertEqual(started_after.month, expected_started_after.month)
        self.assertEqual(started_after.day, expected_started_after.day)
        self.assertEqual(started_after.hour, expected_started_after.hour)
        self.assertEqual(started_after.minute, expected_started_after.minute)

    def test_last_12_hour(self):
        filter = PolicyFilter(period=ExecutionPeriod.Last12hours)
        finished_before, started_after = TimeRangeCalculator.calculate_time_range(filter)
        expected_finished_before = datetime.now()
        expected_started_after = expected_finished_before - timedelta(hours=12)
        print("ExecutionPeriod.Last12hours")
        print("started_after: "+str(started_after))
        print("finished_before: "+str(finished_before))
        print("===========================================")
        self.assertEqual(finished_before.year, expected_finished_before.year)
        self.assertEqual(finished_before.month, expected_finished_before.month)
        self.assertEqual(finished_before.day, expected_finished_before.day)
        self.assertEqual(finished_before.hour, expected_finished_before.hour)
        self.assertEqual(finished_before.minute, expected_finished_before.minute)
        self.assertEqual(started_after.year, expected_started_after.year)
        self.assertEqual(started_after.month, expected_started_after.month)
        self.assertEqual(started_after.day, expected_started_after.day)
        self.assertEqual(started_after.hour, expected_started_after.hour)
        self.assertEqual(started_after.minute, expected_started_after.minute)

    def test_last_24_hour(self):
        filter = PolicyFilter(period=ExecutionPeriod.Last24hours)
        finished_before, started_after = TimeRangeCalculator.calculate_time_range(filter)
        expected_finished_before = datetime.now()
        expected_started_after = expected_finished_before - timedelta(hours=24)
        print("ExecutionPeriod.Last24hours")
        print("started_after: "+str(started_after))
        print("finished_before: "+str(finished_before))
        print("===========================================")
        self.assertEqual(finished_before.year, expected_finished_before.year)
        self.assertEqual(finished_before.month, expected_finished_before.month)
        self.assertEqual(finished_before.day, expected_finished_before.day)
        self.assertEqual(finished_before.hour, expected_finished_before.hour)
        self.assertEqual(finished_before.minute, expected_finished_before.minute)
        self.assertEqual(started_after.year, expected_started_after.year)
        self.assertEqual(started_after.month, expected_started_after.month)
        self.assertEqual(started_after.day, expected_started_after.day)
        self.assertEqual(started_after.hour, expected_started_after.hour)
        self.assertEqual(started_after.minute, expected_started_after.minute)

    def test_execution_period_today(self):
        filter = PolicyFilter(period=ExecutionPeriod.Today)
        finished_before, started_after = TimeRangeCalculator.calculate_time_range(filter)

        now = datetime.now()
        expected_started_after = datetime.combine(now.date(), datetime.min.time())
        expected_finished_before = now

        print("ExecutionPeriod.Today")
        print("started_after: "+str(started_after))
        print("finished_before: "+str(finished_before))
        print("===========================================")
        self.assertEqual(finished_before.year, expected_finished_before.year)
        self.assertEqual(finished_before.month, expected_finished_before.month)
        self.assertEqual(finished_before.day, expected_finished_before.day)
        self.assertEqual(finished_before.hour, expected_finished_before.hour)
        self.assertEqual(finished_before.minute, expected_finished_before.minute)

        self.assertEqual(started_after.year, expected_started_after.year)
        self.assertEqual(started_after.month, expected_started_after.month)
        self.assertEqual(started_after.day, expected_started_after.day)
        self.assertEqual(started_after.hour, expected_started_after.hour)
        self.assertEqual(started_after.minute, expected_started_after.minute)

    def test_execution_period_yesterday(self):
        filter = PolicyFilter(period=ExecutionPeriod.Yesterday)
        finished_before, started_after = TimeRangeCalculator.calculate_time_range(filter)

        now = datetime.now()
        expected_finished_before = datetime.combine(now.date(), datetime.min.time())
        expected_started_after = datetime.combine((now - timedelta(days=1)).date(), datetime.min.time())
        print("ExecutionPeriod.Yesterday")
        print("started_after: "+str(started_after))
        print("finished_before: "+str(finished_before))
        print("===========================================")
        self.assertEqual(finished_before.year, expected_finished_before.year)
        self.assertEqual(finished_before.month, expected_finished_before.month)
        self.assertEqual(finished_before.day, expected_finished_before.day)
        self.assertEqual(finished_before.hour, expected_finished_before.hour)
        self.assertEqual(finished_before.minute, expected_finished_before.minute)
        self.assertEqual(started_after.year, expected_started_after.year)
        self.assertEqual(started_after.month, expected_started_after.month)
        self.assertEqual(started_after.day, expected_started_after.day)
        self.assertEqual(started_after.hour, expected_started_after.hour)
        self.assertEqual(started_after.minute, expected_started_after.minute)


    def test_execution_period_last_7_days(self):
        filter = PolicyFilter(period=ExecutionPeriod.Last7days)
        finished_before, started_after = TimeRangeCalculator.calculate_time_range(filter)
        expected_started_after = datetime.combine((datetime.now() - timedelta(days=7)).date(), datetime.min.time())
        expected_finished_before = datetime.combine(datetime.now().date(), datetime.min.time())
        print("ExecutionPeriod.Last7days")
        print("started_after: "+str(started_after))
        print("finished_before: "+str(finished_before))
        print("===========================================")
        self.assertEqual(finished_before.year, expected_finished_before.year)
        self.assertEqual(finished_before.month, expected_finished_before.month)
        self.assertEqual(finished_before.day, expected_finished_before.day)
        self.assertEqual(finished_before.hour, expected_finished_before.hour)
        self.assertEqual(finished_before.minute, expected_finished_before.minute)
        self.assertEqual(started_after.year, expected_started_after.year)
        self.assertEqual(started_after.month, expected_started_after.month)
        self.assertEqual(started_after.day, expected_started_after.day)
        self.assertEqual(started_after.hour, expected_started_after.hour)
        self.assertEqual(started_after.minute, expected_started_after.minute)


    def test_execution_period_this_month(self):
        filter = PolicyFilter(period=ExecutionPeriod.Thismonth)
        finished_before, started_after = TimeRangeCalculator.calculate_time_range(filter)

        now = datetime.now()
        expected_finished_before = now
        expected_started_after = datetime(datetime.now().year, datetime.now().month, 1)
        print("ExecutionPeriod.Thismonth")
        print("started_after: "+str(started_after))
        print("finished_before: "+str(finished_before))
        print("===========================================")

        self.assertEqual(finished_before.year, expected_finished_before.year)
        self.assertEqual(finished_before.month, expected_finished_before.month)
        self.assertEqual(finished_before.day, expected_finished_before.day)
        self.assertEqual(finished_before.hour, expected_finished_before.hour)
        self.assertEqual(finished_before.minute, expected_finished_before.minute)
        self.assertEqual(started_after.year, expected_started_after.year)
        self.assertEqual(started_after.month, expected_started_after.month)
        self.assertEqual(started_after.day, expected_started_after.day)
        self.assertEqual(started_after.hour, expected_started_after.hour)
        self.assertEqual(started_after.minute, expected_started_after.minute)


    def test_execution_period_last3month(self):
        filter = PolicyFilter(period=ExecutionPeriod.Last3month)
        finished_before, started_after = TimeRangeCalculator.calculate_time_range(filter)

        now = datetime.now()
        expected_started_after = (now - relativedelta(months=3)).replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        expected_finished_before = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        print("ExecutionPeriod.Last3month")
        print("started_after: "+str(started_after))
        print("finished_before: "+str(finished_before))
        print("===========================================")

        self.assertEqual(finished_before.year, expected_finished_before.year)
        self.assertEqual(finished_before.month, expected_finished_before.month)
        self.assertEqual(finished_before.day, expected_finished_before.day)
        self.assertEqual(finished_before.hour, expected_finished_before.hour)
        self.assertEqual(finished_before.minute, expected_finished_before.minute)

        self.assertEqual(started_after.year, expected_started_after.year)
        self.assertEqual(started_after.month, expected_started_after.month)
        self.assertEqual(started_after.day, expected_started_after.day)
        self.assertEqual(started_after.hour, expected_started_after.hour)
        self.assertEqual(started_after.minute, expected_started_after.minute)

    def test_calculate_days_before_time(self):
        days = 7  # Adjust the number of days as needed
        started_after, finished_before = TimeRangeCalculator.calculate_days_before_time(days)

        now = datetime.now()
        expected_started_after = datetime.combine((now - timedelta(days=days)).date(), datetime.min.time())
        expected_finished_before = datetime.combine(now.date(), datetime.min.time())

        self.assertEqual(started_after.year, expected_started_after.year)
        self.assertEqual(started_after.month, expected_started_after.month)
        self.assertEqual(started_after.day, expected_started_after.day)
        self.assertEqual(started_after.hour, expected_started_after.hour)
        self.assertEqual(started_after.minute, expected_started_after.minute)

        self.assertEqual(finished_before.year, expected_finished_before.year)
        self.assertEqual(finished_before.month, expected_finished_before.month)
        self.assertEqual(finished_before.day, expected_finished_before.day)
        self.assertEqual(finished_before.hour, expected_finished_before.hour)
        self.assertEqual(finished_before.minute, expected_finished_before.minute)


    def test_calculate_hours_before_time(self):
        hours = 6  # Adjust the number of hours as needed
        started_after, finished_before = TimeRangeCalculator.calculate_hours_before_time(hours)

        now = datetime.now()
        expected_started_after = now - timedelta(hours=hours)
        expected_finished_before = now

        self.assertEqual(started_after.year, expected_started_after.year)
        self.assertEqual(started_after.month, expected_started_after.month)
        self.assertEqual(started_after.day, expected_started_after.day)
        self.assertEqual(started_after.hour, expected_started_after.hour)
        self.assertEqual(started_after.minute, expected_started_after.minute)

        self.assertEqual(finished_before.year, expected_finished_before.year)
        self.assertEqual(finished_before.month, expected_finished_before.month)
        self.assertEqual(finished_before.day, expected_finished_before.day)
        self.assertEqual(finished_before.hour, expected_finished_before.hour)
        self.assertEqual(finished_before.minute, expected_finished_before.minute)

    def test_calculate_minutes_before_time(self):
        minutes = 30  # Adjust the number of minutes as needed
        started_after, finished_before = TimeRangeCalculator.calculate_minutes_before_time(minutes)

        now = datetime.now()
        expected_started_after = now - timedelta(minutes=minutes)
        expected_finished_before = now

        self.assertEqual(started_after.year, expected_started_after.year)
        self.assertEqual(started_after.month, expected_started_after.month)
        self.assertEqual(started_after.day, expected_started_after.day)
        self.assertEqual(started_after.hour, expected_started_after.hour)
        self.assertEqual(started_after.minute, expected_started_after.minute)
        self.assertEqual(finished_before.year, expected_finished_before.year)
        self.assertEqual(finished_before.month, expected_finished_before.month)
        self.assertEqual(finished_before.day, expected_finished_before.day)
        self.assertEqual(finished_before.hour, expected_finished_before.hour)
        self.assertEqual(finished_before.minute, expected_finished_before.minute)

    def test_calculate_months_before_time(self):
        months_before = 3  # Adjust the number of months as needed
        started_after, finished_before = TimeRangeCalculator.calculate_months_before_time(months_before)

        now = datetime.now()

        # Calculate the expected first day of 'months_before' months ago
        expected_first_day_of_months_before = (now - relativedelta(months=months_before)).replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        # Calculate the expected last day of the previous month
        expected_last_day_of_prev_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        self.assertEqual(started_after, expected_first_day_of_months_before)
        self.assertEqual(finished_before, expected_last_day_of_prev_month)


if __name__ == '__main__':
    unittest.main()
