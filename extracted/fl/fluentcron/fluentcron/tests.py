import unittest

from . import (
    CommonSchedules,
    CronSchedule,
    WeekdayStr,
    daily_at,
    every_n_hours,
    every_n_minutes,
    monthly_on_day,
    weekly_on,
)
from .schedule import _jitter_offset


class TestCronSchedule(unittest.TestCase):
    """Test cases for the CronSchedule builder class."""

    def test_basic_construction(self) -> None:
        """Test basic construction and string conversion."""
        schedule = CronSchedule()
        self.assertEqual(schedule.to_str(), "* * * * *")

    def test_at_method(self) -> None:
        """Test setting time with at() method."""
        schedule = CronSchedule().at(5, 30)
        self.assertEqual(str(schedule), "30 5 * * *")

        # Test with default minute
        schedule = CronSchedule().at(8)
        self.assertEqual(str(schedule), "0 8 * * *")

    def test_at_method_validation(self) -> None:
        """Test validation in at() method."""
        schedule = CronSchedule()

        # Invalid hour
        with self.assertRaises(ValueError):
            schedule.at(24)  # type: ignore[arg-type]

        with self.assertRaises(ValueError):
            schedule.at(-1)  # type: ignore[arg-type]

        # Invalid minute
        with self.assertRaises(ValueError):
            schedule.at(5, 60)  # type: ignore[arg-type]

        with self.assertRaises(ValueError):
            schedule.at(5, -1)  # type: ignore[arg-type]

    def test_daily_schedule(self) -> None:
        """Test daily schedule creation."""
        schedule = CronSchedule().daily().at(5)
        self.assertEqual(str(schedule), "0 5 * * *")

    def test_weekly_schedule(self) -> None:
        """Test weekly schedule creation."""
        schedule = CronSchedule().weekly().on_monday().at(5)
        self.assertEqual(str(schedule), "0 5 * * 1")

        schedule = CronSchedule().weekly().on_friday().at(17, 30)
        self.assertEqual(str(schedule), "30 17 * * 5")

    def test_monthly_schedule(self) -> None:
        """Test monthly schedule creation."""
        schedule = CronSchedule().monthly().on_day(1).at(5)
        self.assertEqual(str(schedule), "0 5 1 * *")

        schedule = CronSchedule().monthly().on_day(15).at(12, 30)
        self.assertEqual(str(schedule), "30 12 15 * *")

    def test_weekday_methods(self) -> None:
        """Test all weekday methods."""
        test_cases = [
            (CronSchedule().on_sunday(), "0"),
            (CronSchedule().on_monday(), "1"),
            (CronSchedule().on_tuesday(), "2"),
            (CronSchedule().on_wednesday(), "3"),
            (CronSchedule().on_thursday(), "4"),
            (CronSchedule().on_friday(), "5"),
            (CronSchedule().on_saturday(), "6"),
        ]

        for schedule, expected_weekday in test_cases:
            self.assertEqual(schedule.weekday, expected_weekday)

    def test_on_weekday_with_numbers(self) -> None:
        """Test on_weekday with numeric values."""
        for i in range(7):
            schedule = CronSchedule().on_weekday(i)  # type: ignore[arg-type]
            self.assertEqual(schedule.weekday, str(i))

    def test_on_weekday_with_names(self) -> None:
        """Test on_weekday with string names."""
        test_cases: list[tuple[WeekdayStr, str]] = [
            ("sunday", "0"),
            ("sunday", "0"),
            ("monday", "1"),
            ("mon", "1"),
            ("tuesday", "2"),
            ("tue", "2"),
            ("wednesday", "3"),
            ("wed", "3"),
            ("thursday", "4"),
            ("thu", "4"),
            ("friday", "5"),
            ("fri", "5"),
            ("saturday", "6"),
            ("sat", "6"),
        ]

        for name, expected in test_cases:
            schedule = CronSchedule().on_weekday(name)
            self.assertEqual(schedule.weekday, expected)

        # Test case insensitivity
        schedule = CronSchedule().on_weekday("MONDAY")
        self.assertEqual(schedule.weekday, "1")

    def test_on_weekday_validation(self) -> None:
        """Test validation in on_weekday method."""
        schedule = CronSchedule()

        # Invalid numeric weekday
        with self.assertRaises(ValueError):
            schedule.on_weekday(7)  # type: ignore[arg-type]

        with self.assertRaises(ValueError):
            schedule.on_weekday(-1)  # type: ignore[arg-type]

        # Invalid string weekday
        with self.assertRaises(ValueError):
            schedule.on_weekday("invalid")  # type: ignore[arg-type]

    def test_on_day_validation(self) -> None:
        """Test validation in on_day method."""
        schedule = CronSchedule()

        # Invalid day
        with self.assertRaises(ValueError):
            schedule.on_day(0)  # type: ignore[arg-type]

        with self.assertRaises(ValueError):
            schedule.on_day(32)  # type: ignore[arg-type]

    def test_every_n_minutes(self) -> None:
        """Test every N minutes functionality."""
        schedule = CronSchedule().every_n_minutes(5)
        self.assertEqual(str(schedule), "*/5 * * * *")

        schedule = CronSchedule().every_n_minutes(30)
        self.assertEqual(str(schedule), "*/30 * * * *")

        # Test edge case: every 1 minute should be "*"
        schedule = CronSchedule().every_n_minutes(1)
        self.assertEqual(str(schedule), "* * * * *")

    def test_every_n_minutes_validation(self) -> None:
        """Test validation in every_n_minutes method."""
        schedule = CronSchedule()

        with self.assertRaises(ValueError):
            schedule.every_n_minutes(0)  # type: ignore[arg-type]

        with self.assertRaises(ValueError):
            schedule.every_n_minutes(60)  # type: ignore[arg-type]

    def test_every_n_hours(self) -> None:
        """Test every N hours functionality."""
        schedule = CronSchedule().every_n_hours(2)
        self.assertEqual(str(schedule), "* */2 * * *")

        schedule = CronSchedule().every_n_hours(6)
        self.assertEqual(str(schedule), "* */6 * * *")

        # Test edge case: every 1 hour should be "*"
        schedule = CronSchedule().every_n_hours(1)
        self.assertEqual(str(schedule), "* * * * *")

    def test_every_n_hours_validation(self) -> None:
        """Test validation in every_n_hours method."""
        schedule = CronSchedule()

        with self.assertRaises(ValueError):
            schedule.every_n_hours(0)  # type: ignore[arg-type]

        with self.assertRaises(ValueError):
            schedule.every_n_hours(24)  # type: ignore[arg-type]

    def test_method_chaining(self) -> None:
        """Test that methods can be chained together."""
        schedule = CronSchedule().weekly().on_monday().at(5, 30)
        self.assertEqual(str(schedule), "30 5 * * 1")

        schedule = CronSchedule().monthly().on_day(15).at(12)
        self.assertEqual(str(schedule), "0 12 15 * *")

    def test_immutability(self) -> None:
        """Test that CronSchedule instances are truly immutable."""
        schedule = CronSchedule()

        # Verify that we can't modify fields directly
        with self.assertRaises(AttributeError):
            schedule.minute = "30"  # type: ignore

        with self.assertRaises(AttributeError):
            schedule.hour = "5"  # type: ignore

    def test_hashability(self) -> None:
        """Test that CronSchedule instances are hashable and can be used as dict keys."""
        schedule1 = CronSchedule().daily().at(5)
        schedule2 = CronSchedule().weekly().on_monday().at(8, 30)
        schedule3 = CronSchedule().daily().at(5)  # Same as schedule1

        # Test using schedules as dictionary keys
        schedule_dict = {
            schedule1: "Daily morning task",
            schedule2: "Weekly Monday task",
        }

        self.assertEqual(schedule_dict[schedule1], "Daily morning task")
        self.assertEqual(schedule_dict[schedule2], "Weekly Monday task")

        # Test that equivalent schedules work as the same key
        self.assertEqual(schedule_dict[schedule3], "Daily morning task")

        # Test using schedules in sets
        schedule_set = {schedule1, schedule2, schedule3}
        self.assertEqual(len(schedule_set), 2)  # schedule1 and schedule3 are the same

    def test_equality(self) -> None:
        """Test that CronSchedule instances with same values are equal."""
        schedule1 = CronSchedule().daily().at(5, 30)
        schedule2 = CronSchedule().daily().at(5, 30)
        schedule3 = CronSchedule().daily().at(6, 30)

        # Test equality
        self.assertEqual(schedule1, schedule2)
        self.assertNotEqual(schedule1, schedule3)

        # Test that they're not the same object (different instances)
        self.assertIsNot(schedule1, schedule2)

        # Test equality with different construction paths
        schedule4 = CronSchedule(minute="30", hour="5", day="*", month="*", weekday="*")
        self.assertEqual(schedule1, schedule4)

    def test_namedtuple_features(self) -> None:
        """Test additional NamedTuple features like _replace and _asdict."""
        schedule = CronSchedule().daily().at(5, 30)

        # Test that _replace is available (used internally by our methods)
        new_schedule = schedule._replace(hour="6")
        self.assertEqual(new_schedule.hour, "6")
        self.assertEqual(new_schedule.minute, "30")
        self.assertEqual(schedule.hour, "5")  # Original unchanged

        # Test _asdict (useful for serialization)
        schedule_dict = schedule._asdict()
        expected_dict = {
            "minute": "30",
            "hour": "5",
            "day": "*",
            "month": "*",
            "weekday": "*",
        }
        self.assertEqual(schedule_dict, expected_dict)


class TestConvenienceFunctions(unittest.TestCase):
    """Test cases for convenience functions."""

    def test_daily_at(self) -> None:
        """Test daily_at convenience function."""
        self.assertEqual(daily_at(5), "0 5 * * *")
        self.assertEqual(daily_at(8, 30), "30 8 * * *")

    def test_weekly_on(self) -> None:
        """Test weekly_on convenience function."""
        self.assertEqual(weekly_on("monday", 5), "0 5 * * 1")
        self.assertEqual(weekly_on(1, 5, 30), "30 5 * * 1")
        self.assertEqual(weekly_on("fri", 17), "0 17 * * 5")

    def test_monthly_on_day(self) -> None:
        """Test monthly_on_day convenience function."""
        self.assertEqual(monthly_on_day(1, 5), "0 5 1 * *")
        self.assertEqual(monthly_on_day(15, 12, 30), "30 12 15 * *")

    def test_every_n_minutes_function(self) -> None:
        """Test every_n_minutes convenience function."""
        self.assertEqual(every_n_minutes(5), "*/5 * * * *")
        self.assertEqual(every_n_minutes(30), "*/30 * * * *")

    def test_every_n_hours_function(self) -> None:
        """Test every_n_hours convenience function."""
        self.assertEqual(every_n_hours(2), "* */2 * * *")
        self.assertEqual(every_n_hours(6), "* */6 * * *")


class TestCommonSchedules(unittest.TestCase):
    """Test cases for common schedule presets."""

    def test_common_schedules_exist(self) -> None:
        """Test that common schedule constants exist and are valid."""
        # Test that all attributes exist and are strings
        schedules = [
            CommonSchedules.EVERY_MINUTE,
            CommonSchedules.EVERY_5_MINUTES,
            CommonSchedules.EVERY_15_MINUTES,
            CommonSchedules.EVERY_30_MINUTES,
            CommonSchedules.EVERY_HOUR,
            CommonSchedules.EVERY_2_HOURS,
            CommonSchedules.EVERY_6_HOURS,
            CommonSchedules.EVERY_12_HOURS,
            CommonSchedules.DAILY_MIDNIGHT,
            CommonSchedules.DAILY_NOON,
            CommonSchedules.WEEKLY_SUNDAY_MIDNIGHT,
            CommonSchedules.WEEKLY_MONDAY_MIDNIGHT,
            CommonSchedules.MONTHLY_FIRST_MIDNIGHT,
            CommonSchedules.YEARLY_JAN_FIRST,
        ]

        for schedule in schedules:
            self.assertIsInstance(schedule, str)
            # Basic format check: should have 5 parts separated by spaces
            parts = schedule.split()
            self.assertEqual(len(parts), 5, f"Invalid cron format: {schedule}")

    def test_specific_common_schedules(self) -> None:
        """Test specific common schedule values."""
        self.assertEqual(CommonSchedules.EVERY_MINUTE, "* * * * *")
        self.assertEqual(CommonSchedules.EVERY_5_MINUTES, "*/5 * * * *")
        self.assertEqual(CommonSchedules.EVERY_30_MINUTES, "*/30 * * * *")
        self.assertEqual(CommonSchedules.EVERY_HOUR, "0 * * * *")
        self.assertEqual(CommonSchedules.DAILY_MIDNIGHT, "0 0 * * *")
        self.assertEqual(CommonSchedules.DAILY_NOON, "0 12 * * *")
        self.assertEqual(CommonSchedules.WEEKLY_MONDAY_MIDNIGHT, "0 0 * * 1")
        self.assertEqual(CommonSchedules.MONTHLY_FIRST_MIDNIGHT, "0 0 1 * *")


class TestRealWorldExamples(unittest.TestCase):
    """Test cases for real-world schedule examples."""

    def test_original_schedules(self) -> None:
        """Test that our DSL produces the same schedules as the original strings."""
        # Original schedules from your code
        original_schedules = {
            "0 5 * * *": daily_at(5),  # Daily at 5:00 AM
            "0 5 * * 1": weekly_on("monday", 5),  # Weekly on Monday at 5:00 AM
            "0 5 1 * *": monthly_on_day(1, 5),  # Monthly on 1st at 5:00 AM
            "*/30 * * * *": every_n_minutes(30),  # Every 30 minutes
            "0 8 * * *": daily_at(8),  # Daily at 8:00 AM
        }

        for original, generated in original_schedules.items():
            self.assertEqual(
                original,
                generated,
                f"Generated schedule '{generated}' doesn't match original '{original}'",
            )

    def test_complex_schedules(self) -> None:
        """Test more complex schedule combinations."""
        # Business hours: Monday to Friday at 9 AM
        schedule = CronSchedule().weekly().on_weekday(1).at(9)  # Monday
        self.assertEqual(str(schedule), "0 9 * * 1")

        # Quarterly: 1st day of Jan, Apr, Jul, Oct at midnight
        # Note: This would need additional functionality for specific months
        # For now, test monthly on 1st
        schedule = CronSchedule().monthly().on_day(1).at(0)
        self.assertEqual(str(schedule), "0 0 1 * *")


class TestJitter(unittest.TestCase):
    """Test cases for deterministic jitter functionality."""

    def test_jitter_offset_range(self) -> None:
        """_jitter_offset always returns a value in [0, modulus)."""
        for modulus in [1, 5, 15, 30, 60]:
            for jitter in ["a", "b", "task-1", "my-unique-task-id", ""]:
                offset = _jitter_offset(jitter, modulus)
                self.assertGreaterEqual(offset, 0)
                self.assertLess(offset, modulus)

    def test_jitter_offset_determinism(self) -> None:
        """Same string + modulus always produces the same result."""
        for _ in range(10):
            self.assertEqual(_jitter_offset("test", 60), _jitter_offset("test", 60))

    def test_jitter_offset_pinned_values(self) -> None:
        """Pinned values for mod 60."""
        self.assertEqual(_jitter_offset("my-unique-task-id", 60), 33)
        self.assertEqual(_jitter_offset("some-other-task", 60), 55)
        self.assertEqual(_jitter_offset("test", 60), 12)
        self.assertEqual(_jitter_offset("", 60), 49)

    def test_at_with_jitter(self) -> None:
        """at() with jitter computes minute from hash."""
        schedule = CronSchedule().daily().at(12, jitter="my-unique-task-id")
        self.assertEqual(str(schedule), "33 12 * * *")

    def test_at_minute_and_jitter_raises(self) -> None:
        """at() with both minute and jitter raises ValueError."""
        with self.assertRaises(ValueError):
            CronSchedule().daily().at(12, 30, jitter="task")

    def test_at_default_minute_preserved(self) -> None:
        """at() without minute or jitter defaults minute to 0."""
        schedule = CronSchedule().daily().at(12)
        self.assertEqual(str(schedule), "0 12 * * *")

    def test_every_n_minutes_with_jitter(self) -> None:
        """every_n_minutes() with jitter uses offset/n format."""
        schedule = CronSchedule().every_n_minutes(15, jitter="my-unique-task-id")
        self.assertEqual(str(schedule), "3/15 * * * *")

    def test_every_n_minutes_jitter_ignored_for_1(self) -> None:
        """every_n_minutes(1) ignores jitter since every minute is every minute."""
        schedule = CronSchedule().every_n_minutes(1, jitter="task")
        self.assertEqual(str(schedule), "* * * * *")

    def test_every_n_hours_with_jitter(self) -> None:
        """every_n_hours() with jitter sets minute offset."""
        schedule = CronSchedule().every_n_hours(2, jitter="my-unique-task-id")
        self.assertEqual(str(schedule), "33 */2 * * *")

    def test_shortcut_daily_at_with_jitter(self) -> None:
        """daily_at shortcut with jitter."""
        self.assertEqual(daily_at(12, jitter="my-unique-task-id"), "33 12 * * *")

    def test_shortcut_weekly_on_with_jitter(self) -> None:
        """weekly_on shortcut with jitter."""
        self.assertEqual(
            weekly_on("monday", 12, jitter="my-unique-task-id"), "33 12 * * 1"
        )

    def test_shortcut_monthly_on_day_with_jitter(self) -> None:
        """monthly_on_day shortcut with jitter."""
        self.assertEqual(
            monthly_on_day(1, 12, jitter="my-unique-task-id"), "33 12 1 * *"
        )

    def test_shortcut_every_n_minutes_with_jitter(self) -> None:
        """every_n_minutes shortcut with jitter."""
        self.assertEqual(
            every_n_minutes(15, jitter="my-unique-task-id"), "3/15 * * * *"
        )

    def test_shortcut_every_n_hours_with_jitter(self) -> None:
        """every_n_hours shortcut with jitter."""
        self.assertEqual(every_n_hours(2, jitter="my-unique-task-id"), "33 */2 * * *")

    def test_shortcut_minute_and_jitter_raises(self) -> None:
        """Shortcuts reject minute + jitter together."""
        with self.assertRaises(ValueError):
            daily_at(12, 30, jitter="task")
        with self.assertRaises(ValueError):
            weekly_on("monday", 12, 30, jitter="task")
        with self.assertRaises(ValueError):
            monthly_on_day(1, 12, 30, jitter="task")
