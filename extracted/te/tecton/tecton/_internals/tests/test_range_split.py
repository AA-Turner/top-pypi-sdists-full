from datetime import datetime
from datetime import timedelta
from unittest import TestCase

from tecton_core import conf
from tecton_core.data_processing_utils import split_range


class SplitRangeTest(TestCase):
    def test_split_range_even(self):
        conf.set("DUCKDB_RANGE_SPLIT_COUNT", 3)
        range_start = datetime(2024, 1, 1, 0, 0, 0)
        range_end = datetime(2024, 1, 1, 3, 0, 0)

        split_ranges = split_range(range_start, range_end, timedelta(hours=1))

        expected_ranges = [
            (datetime(2024, 1, 1, 0, 0, 0), datetime(2024, 1, 1, 1, 0, 0)),
            (datetime(2024, 1, 1, 1, 0, 0), datetime(2024, 1, 1, 2, 0, 0)),
            (datetime(2024, 1, 1, 2, 0, 0), datetime(2024, 1, 1, 3, 0, 0)),
        ]
        self.assertEqual(split_ranges, expected_ranges)

    def test_split_range_single_split(self):
        conf.set("DUCKDB_RANGE_SPLIT_COUNT", 1)
        range_start = datetime(2024, 1, 1, 0, 0, 0)
        range_end = datetime(2024, 2, 1, 0, 0, 0)

        split_ranges = split_range(range_start, range_end, timedelta(days=1))

        expected_ranges = [(range_start, range_end)]
        self.assertEqual(split_ranges, expected_ranges)
