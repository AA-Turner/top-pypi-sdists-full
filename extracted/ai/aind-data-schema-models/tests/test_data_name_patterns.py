"""Tests classes in data_name_patterns module"""

import unittest
from datetime import datetime, timezone

from aind_data_schema_models.data_name_patterns import (
    DataRegex,
    DataRegexLegacy,
    RegexParts,
    build_data_name,
    datetime_from_name_string,
    datetime_to_name_string,
)


class TestRegexParts(unittest.TestCase):
    """Tests methods in RegexParts class"""

    def test_patterns_success(self):
        """Tests that the regex patterns match successfully."""

        input_date = "2020-10-19"
        input_time = "08-30-59"
        input_datetime = "2020-10-19_08-30-59"

        self.assertRegex(input_date, RegexParts.DATE)
        self.assertRegex(input_time, RegexParts.TIME)
        self.assertRegex(input_datetime, RegexParts.DATETIME)
        self.assertIsNotNone(datetime_from_name_string(input_datetime))

    def test_patterns_fail(self):
        """Tests that the regex patterns match unsuccessfully."""

        malformed_date = "10/19/2020"
        malformed_time = "8:30:59"

        self.assertNotRegex(malformed_date, RegexParts.DATE)
        self.assertNotRegex(malformed_time, RegexParts.TIME)


class TestDataRegex(unittest.TestCase):
    """Tests methods in DataRegex class"""

    def test_patterns_success(self):
        """Tests that the regex patterns match successfully."""

        data = "ecephys_2020-10-19_08-30-59"
        raw = "ecephys_123455_2020-10-19_08-30-59"
        derived = "ecephys_123455_2020-10-19_08-30-59_sorted_2020-11-21_09-31-58"
        analyzed = "project_analysis_3033-12-21_04-22-11"
        no_underscores = "abc-123<something>"
        no_special_chars = "abc-123"
        no_special_chars_except_space = "abc efg - 123"

        data_dt = "ecephys_2020-10-19_08-30-59"
        raw_dt = "ecephys_123455_2020-10-19_08-30-59"
        derived_dt = "ecephys_123455_2020-10-19_08-30-59_sorted_2020-11-21_09-31-58"
        analyzed_dt = "project_analysis_3033-12-21_04-22-11"

        self.assertRegex(data, DataRegexLegacy.DATA)
        self.assertRegex(raw, DataRegexLegacy.RAW)
        self.assertRegex(derived, DataRegexLegacy.DERIVED)
        self.assertRegex(analyzed, DataRegexLegacy.ANALYZED)
        self.assertRegex(no_underscores, DataRegex.NO_UNDERSCORES)
        self.assertRegex(no_special_chars, DataRegex.NO_SPECIAL_CHARS)
        self.assertRegex(no_special_chars_except_space, DataRegex.NO_SPECIAL_CHARS_EXCEPT_SPACE)

        self.assertRegex(data_dt, DataRegex.DATA)
        self.assertRegex(raw_dt, DataRegex.RAW)
        self.assertRegex(derived_dt, DataRegex.DERIVED)
        self.assertRegex(analyzed_dt, DataRegex.ANALYZED)

    def test_patterns_fail(self):
        """Tests that the regex patterns match unsuccessfully."""

        malformed_data = "ecephys_2020-10-19T08:30:59"
        malformed_raw = "ecephys_123455_2020-10-19T083059_test"
        malformed_derived = "ecephys_123455_2020-10-19T083059_sorted_2020-11-21T09:31:58"
        malformed_analyzed = "project_analysis_3033-12-21T042211_test"
        malformed_no_underscores = "abc_123<something>"
        special_chars = [
            "<",
            ">",
            ":",
            ";",
            '"',
            "/",
            "|",
            "?",
            " ",
            "\\",
            "_",
        ]

        self.assertNotRegex(malformed_data, DataRegex.DATA)
        self.assertNotRegex(malformed_raw, DataRegex.DATA)
        self.assertNotRegex(malformed_derived, DataRegex.DATA)
        self.assertNotRegex(malformed_analyzed, DataRegex.DATA)
        self.assertNotRegex(malformed_no_underscores, DataRegex.NO_UNDERSCORES)
        for c in special_chars:
            malformed_no_special_chars = f"abc-123{c}something{c}"
            self.assertNotRegex(malformed_no_special_chars, DataRegex.NO_SPECIAL_CHARS)
            if c == " ":
                continue
            malformed_no_special_chars_except_space = f"abc efg - 123 {c}something{c}"
            self.assertNotRegex(malformed_no_special_chars_except_space, DataRegex.NO_SPECIAL_CHARS_EXCEPT_SPACE)


class TestDataNamePatternsMethods(unittest.TestCase):
    """Tests methods in data_name_patterns module"""

    def test_datetime_to_name_string(self):
        """Tests datetime object is converted to string"""

        dt = datetime(2020, 12, 29, 1, 10, 50)
        actual_output = datetime_to_name_string(dt)
        self.assertEqual("2020-12-29_01-10-50", actual_output)

    def test_datetime_with_tz_to_name_string(self):
        """Tests datetime object with timezone is converted to string"""

        dt = datetime(2020, 12, 29, 1, 10, 50, tzinfo=timezone.utc)
        actual_output = datetime_to_name_string(dt)
        self.assertEqual("2020-12-29_01-10-50", actual_output)

    def test_datetime_from_name_string(self):
        """Tests date and time strings are converted to datetime object"""

        datetime_str = "2020-12-29_01-10-50"
        actual_output = datetime_from_name_string(datetime_str)
        dt = datetime(2020, 12, 29, 1, 10, 50)
        self.assertEqual(dt, actual_output)

    def test_build_data_name(self):
        """Tests datetime object is converted to string and attached to label"""

        subject_id = "123456"
        dt = datetime(2020, 12, 29, 1, 10, 50)
        actual_output = build_data_name(label=subject_id, creation_datetime=dt)

        self.assertEqual("123456_2020-12-29_01-10-50", actual_output)


if __name__ == "__main__":
    unittest.main()
