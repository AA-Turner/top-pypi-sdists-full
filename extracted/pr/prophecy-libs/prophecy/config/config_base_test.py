import unittest
from datetime import datetime, timezone, timedelta, date

from prophecy.config import ConfigBase
from test.workflow_unit_test.test_complex_reformat import Config


# --- Unit Tests ---
class TestGetTimestampValue(unittest.TestCase):

    def setUp(self):
        """Set up the test instance."""
        self.parser = ConfigBase()

    # --- Helper to create expected datetime objects ---
    def create_expected_dt(self, year, month, day, hour, minute, second, microsecond=0, tz_offset_hours=None):
        if tz_offset_hours is not None:
            tz = timezone(timedelta(hours=tz_offset_hours))
            return datetime(year, month, day, hour, minute, second, microsecond, tzinfo=tz)
        else:
            # Naive datetime
            return datetime(year, month, day, hour, minute, second, microsecond)

    # --- Tests for dd-mm-YYYY formats ---
    def test_format_dd_mm_YYYY_T_HMSf_z(self):
        ts_str = "27-10-2023T10:30:15.123456+0530"
        expected = self.create_expected_dt(2023, 10, 27, 10, 30, 15, 123456, tz_offset_hours=5.5)
        self.assertEqual(self.parser.get_timestamp_value(ts_str), expected)

    def test_format_dd_mm_YYYY_T_HMS_z(self):
        ts_str = "27-10-2023T10:30:15+0000"
        expected = self.create_expected_dt(2023, 10, 27, 10, 30, 15, 0, tz_offset_hours=0)
        self.assertEqual(self.parser.get_timestamp_value(ts_str), expected)

    def test_format_dd_mm_YYYY_T_HMS_z_1(self):
        ts_str = "27-10-2023T10:30:15Z+0000"
        expected = self.create_expected_dt(2023, 10, 27, 10, 30, 15, 0, tz_offset_hours=0)
        self.assertEqual(self.parser.get_timestamp_value(ts_str), expected)

    def test_format_dd_mm_YYYY_T_HMS_z_2(self):
        ts_str = "27-10-2023 10:30:15 +0000"
        expected = self.create_expected_dt(2023, 10, 27, 10, 30, 15, 0, tz_offset_hours=0)
        self.assertEqual(self.parser.get_timestamp_value(ts_str), expected)

    def test_format_dd_mm_YYYY_T_HMS_z(self):
        ts_str = "27-10-2023T10:30:15Z+0530"
        expected = self.create_expected_dt(2023, 10, 27, 10, 30, 15, 0, tz_offset_hours=5.5)
        self.assertEqual(self.parser.get_timestamp_value(ts_str), expected)

    def test_format_dd_mm_YYYY_space_HMSf_z(self):
        ts_str = "27-10-2023 10:30:15.123456-0700"
        expected = self.create_expected_dt(2023, 10, 27, 10, 30, 15, 123456, tz_offset_hours=-7)
        self.assertEqual(self.parser.get_timestamp_value(ts_str), expected)

    def test_format_dd_mm_YYYY_space_HMS_z(self):
        ts_str = "27-10-2023 10:30:15+0200"
        expected = self.create_expected_dt(2023, 10, 27, 10, 30, 15, 0, tz_offset_hours=2)
        self.assertEqual(self.parser.get_timestamp_value(ts_str), expected)

    def test_format_dd_mm_YYYY_T_HMSf_naive(self):
        ts_str = "27-10-2023T10:30:15.123456"
        expected = self.create_expected_dt(2023, 10, 27, 10, 30, 15, 123456)
        self.assertEqual(self.parser.get_timestamp_value(ts_str), expected)

    def test_format_dd_mm_YYYY_T_HMS_naive(self):
        ts_str = "27-10-2023T10:30:15"
        expected = self.create_expected_dt(2023, 10, 27, 10, 30, 15)
        self.assertEqual(self.parser.get_timestamp_value(ts_str), expected)

    def test_format_dd_mm_YYYY_space_HMSf_naive(self):
        ts_str = "27-10-2023 10:30:15.123456"
        expected = self.create_expected_dt(2023, 10, 27, 10, 30, 15, 123456)
        self.assertEqual(self.parser.get_timestamp_value(ts_str), expected)

    def test_format_dd_mm_YYYY_space_HMS_naive(self):
        ts_str = "27-10-2023 10:30:15"
        expected = self.create_expected_dt(2023, 10, 27, 10, 30, 15)
        self.assertEqual(self.parser.get_timestamp_value(ts_str), expected)

    # --- Tests for YYYY-mm-dd formats ---
    def test_format_YYYY_mm_dd_T_HMSf_z(self):
        ts_str = "2023-10-27T10:30:15.987654+0100"
        expected = self.create_expected_dt(2023, 10, 27, 10, 30, 15, 987654, tz_offset_hours=1)
        self.assertEqual(self.parser.get_timestamp_value(ts_str), expected)

    def test_format_YYYY_mm_dd_T_HMS_z(self):
        ts_str = "2023-10-27T10:30:15-0400"
        expected = self.create_expected_dt(2023, 10, 27, 10, 30, 15, 0, tz_offset_hours=-4)
        self.assertEqual(self.parser.get_timestamp_value(ts_str), expected)

    def test_format_YYYY_mm_dd_space_HMSf_z(self):
        ts_str = "2023-10-27 10:30:15.987654+0000"
        expected = self.create_expected_dt(2023, 10, 27, 10, 30, 15, 987654, tz_offset_hours=0)
        self.assertEqual(self.parser.get_timestamp_value(ts_str), expected)

    def test_format_YYYY_mm_dd_space_HMS_z(self):
        ts_str = "2023-10-27 10:30:15Z"
        ts_str_plus0000 = "2023-10-27 10:30:15+0000"
        expected = self.create_expected_dt(2023, 10, 27, 10, 30, 15, 0, tz_offset_hours=0)
        self.assertEqual(self.parser.get_timestamp_value(ts_str_plus0000), expected)
        self.assertEqual(self.parser.get_timestamp_value(ts_str), expected)

    def test_format_YYYY_mm_dd_T_HMSf_naive(self):
        ts_str = "2023-10-27T10:30:15.987654"
        expected = self.create_expected_dt(2023, 10, 27, 10, 30, 15, 987654)
        self.assertEqual(self.parser.get_timestamp_value(ts_str), expected)

    def test_format_YYYY_mm_dd_T_HMS_naive(self):
        ts_str = "2023-10-27T10:30:15"
        expected = self.create_expected_dt(2023, 10, 27, 10, 30, 15)
        self.assertEqual(self.parser.get_timestamp_value(ts_str), expected)

    def test_format_YYYY_mm_dd_space_HMSf_naive(self):
        ts_str = "2023-10-27 10:30:15.987654"
        expected = self.create_expected_dt(2023, 10, 27, 10, 30, 15, 987654)
        self.assertEqual(self.parser.get_timestamp_value(ts_str), expected)

    def test_format_YYYY_mm_dd_space_HMS_naive(self):
        ts_str = "2023-10-27 10:30:15"
        expected = self.create_expected_dt(2023, 10, 27, 10, 30, 15)
        self.assertEqual(self.parser.get_timestamp_value(ts_str), expected)

    # --- Tests for mm-dd-YYYY formats ---
    def test_format_mm_dd_YYYY_T_HMSf_z(self):
        ts_str = "10-27-2023T10:30:15.112233+0300"
        expected = self.create_expected_dt(2023, 10, 27, 10, 30, 15, 112233, tz_offset_hours=3)
        self.assertEqual(self.parser.get_timestamp_value(ts_str), expected)

    def test_format_mm_dd_YYYY_T_HMS_z(self):
        ts_str = "10-27-2023T10:30:15-0800"
        expected = self.create_expected_dt(2023, 10, 27, 10, 30, 15, 0, tz_offset_hours=-8)
        self.assertEqual(self.parser.get_timestamp_value(ts_str), expected)

    def test_format_mm_dd_YYYY_space_HMSf_z(self):
        ts_str = "10-27-2023 10:30:15.112233+0000"
        expected = self.create_expected_dt(2023, 10, 27, 10, 30, 15, 112233, tz_offset_hours=0)
        self.assertEqual(self.parser.get_timestamp_value(ts_str), expected)

    def test_format_mm_dd_YYYY_space_HMS_z(self):
        ts_str = "10-27-2023 10:30:15-0530"
        expected = self.create_expected_dt(2023, 10, 27, 10, 30, 15, 0, tz_offset_hours=-5.5)
        self.assertEqual(self.parser.get_timestamp_value(ts_str), expected)

    def test_format_mm_dd_YYYY_T_HMSf_naive(self):
        ts_str = "10-27-2023T10:30:15.112233"
        expected = self.create_expected_dt(2023, 10, 27, 10, 30, 15, 112233)
        self.assertEqual(self.parser.get_timestamp_value(ts_str), expected)

    def test_format_mm_dd_YYYY_T_HMS_naive(self):
        ts_str = "10-27-2023T10:30:15"
        expected = self.create_expected_dt(2023, 10, 27, 10, 30, 15)
        self.assertEqual(self.parser.get_timestamp_value(ts_str), expected)

    def test_format_mm_dd_YYYY_space_HMSf_naive(self):
        ts_str = "10-27-2023 10:30:15.112233"
        expected = self.create_expected_dt(2023, 10, 27, 10, 30, 15, 112233)
        self.assertEqual(self.parser.get_timestamp_value(ts_str), expected)

    def test_format_mm_dd_YYYY_space_HMS_naive(self):
        ts_str = "10-27-2023 10:30:15"
        expected = self.create_expected_dt(2023, 10, 27, 10, 30, 15)
        self.assertEqual(self.parser.get_timestamp_value(ts_str), expected)


    # --- Tests for Invalid Inputs ---
    def test_invalid_format_completely_wrong(self):
        ts_str = "not a timestamp"
        with self.assertRaisesRegex(ValueError, f"Timestamp string '{ts_str}' does not match any known formats."):
            self.parser.get_timestamp_value(ts_str)

    def test_invalid_format_wrong_separators(self):
        ts_str = "2023/10/27 10:30:15" # Uses slashes instead of dashes
        with self.assertRaisesRegex(ValueError, f"Timestamp string '{ts_str}' does not match any known formats."):
            self.parser.get_timestamp_value(ts_str)

    def test_invalid_format_wrong_date_order(self):
        ts_str = "2023-27-10T10:30:15" # YYYY-dd-mm - not supported
        with self.assertRaisesRegex(ValueError, f"Timestamp string '{ts_str}' does not match any known formats."):
            self.parser.get_timestamp_value(ts_str)

    def test_invalid_format_extra_characters(self):
        ts_str = "2023-10-27T10:30:15Z extra"
        with self.assertRaisesRegex(ValueError, f"Timestamp string '{ts_str}' does not match any known formats."):
            self.parser.get_timestamp_value(ts_str)

    def test_invalid_date_components(self):
        # Note: strptime itself raises ValueError for invalid dates/times before our function does.
        # This test confirms *a* ValueError is raised, likely from strptime.
        ts_str = "32-10-2023T10:30:15+0000" # Invalid day
        with self.assertRaises(ValueError):
            self.parser.get_timestamp_value(ts_str)

        ts_str = "2023-10-32T10:30:15+0000" # Invalid day
        with self.assertRaises(ValueError):
            self.parser.get_timestamp_value(ts_str)

        ts_str = "2023-10-32T10:30:15+000000000000000" # Invalid fraction
        with self.assertRaises(ValueError):
            self.parser.get_timestamp_value(ts_str)

        ts_str_hour = "01-12-2023T25:30:15+0000" # Invalid hour
        with self.assertRaises(ValueError):
            self.parser.get_timestamp_value(ts_str_hour)

    # --- Tests for Edge Cases ---
    def test_empty_string(self):
        ts_str = ""
        self.assertIsNone(self.parser.get_timestamp_value(ts_str))

    def test_get_config(self):
        print(self.parser.get_config_object(None, ["2025-01-01"], ["2025-01-01", "2025-01-01", "2025-01-01"], cls=date))

# --- Unit Tests ---
class TestGetDateValue(unittest.TestCase):

    def setUp(self):
        """Set up the test instance."""
        self.parser = ConfigBase()

    # Helper to create expected datetime objects (since strptime returns datetime)
    def create_expected_dt(self, year, month, day):
        return date(year, month, day) # Time defaults to 00:00:00

    # --- Tests for Valid Formats ---

    def test_format_yyyy_mm_dd_hyphen(self):
        date_str = "2023-10-27"
        expected = self.create_expected_dt(2023, 10, 27)
        result = self.parser.get_date_value(date_str)
        self.assertEqual(result, expected)
        self.assertIsInstance(result, date) # Check actual return type

    def test_format_mm_dd_yyyy_hyphen(self):
        date_str = "11-20-2024"
        expected = self.create_expected_dt(2024, 11, 20)
        self.assertEqual(self.parser.get_date_value(date_str), expected)

    def test_format_dd_mm_yyyy_hyphen(self):
        date_str = "15-01-2023"
        expected = self.create_expected_dt(2023, 1, 15)
        self.assertEqual(self.parser.get_date_value(date_str), expected)

    def test_format_yyyy_mm_dd_slash(self):
        date_str = "2023/10/27"
        expected = self.create_expected_dt(2023, 10, 27)
        self.assertEqual(self.parser.get_date_value(date_str), expected)

    def test_format_mm_dd_yyyy_slash(self):
        date_str = "11/20/2024"
        expected = self.create_expected_dt(2024, 11, 20)
        self.assertEqual(self.parser.get_date_value(date_str), expected)

    def test_format_dd_mm_yyyy_slash(self):
        date_str = "15/01/2023"
        expected = self.create_expected_dt(2023, 1, 15)
        self.assertEqual(self.parser.get_date_value(date_str), expected)

    # --- Tests for Invalid Inputs ---

    def test_invalid_format_completely_wrong(self):
        date_str = "not a date"
        with self.assertRaisesRegex(ValueError, f"Date string '{date_str}' does not match any known formats."):
            self.parser.get_date_value(date_str)

    def test_invalid_format_wrong_separator(self):
        date_str = "2023.10.27" # Uses dots
        with self.assertRaisesRegex(ValueError, f"Date string '{date_str}' does not match any known formats."):
            self.parser.get_date_value(date_str)

    def test_invalid_format_datetime_string(self):
        # This format is not in the list, should fail
        date_str = "2023-10-27T10:30:00"
        with self.assertRaisesRegex(ValueError, f"Date string '{date_str}' does not match any known formats."):
            self.parser.get_date_value(date_str)

    def test_invalid_format_incomplete_date(self):
        date_str = "2023-10"
        with self.assertRaisesRegex(ValueError, f"Date string '{date_str}' does not match any known formats."):
            self.parser.get_date_value(date_str)

    # --- Tests for Invalid Date Values (strptime raises ValueError) ---

    def test_invalid_day(self):
        date_str = "2023-10-32" # Matches %Y-%m-%d format structure
        # strptime itself will raise ValueError here
        with self.assertRaises(ValueError):
            self.parser.get_date_value(date_str)

    def test_invalid_month(self):
        date_str = "2023-13-01" # Matches %Y-%m-%d format structure
        with self.assertRaises(ValueError):
            self.parser.get_date_value(date_str)

    def test_invalid_day_for_month(self):
        date_str = "2023-04-31" # April only has 30 days
        with self.assertRaises(ValueError):
            self.parser.get_date_value(date_str)

    def test_invalid_leap_day_non_leap_year(self):
        date_str = "2023-02-29" # 2023 is not a leap year
        with self.assertRaises(ValueError):
            self.parser.get_date_value(date_str)

    # --- Tests for Edge Cases ---

    def test_empty_string(self):
        date_str = ""
        self.assertIsNone(self.parser.get_date_value(date_str))

    def test_valid_leap_year_date(self):
        date_str = "2024-02-29" # 2024 is a leap year
        expected = self.create_expected_dt(2024, 2, 29)
        self.assertEqual(self.parser.get_date_value(date_str), expected)

    def test_valid_leap_year_date_slash(self):
        date_str = "02/29/2020" # 2020 is a leap year
        expected = self.create_expected_dt(2020, 2, 29)
        self.assertEqual(self.parser.get_date_value(date_str), expected)

if __name__ == '__main__':
    unittest.main()