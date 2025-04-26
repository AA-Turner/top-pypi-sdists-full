import unittest

import pandas

from tecton.framework.data_frame import TectonDataFrame


class TestDataFrame(unittest.TestCase):
    def test_to_utc_aware_pandas_with_naive_timestamps(self):
        data = {"timestamp": ["2024-01-01 00:00:00", "2024-01-01 12:00:00"]}
        df = pandas.DataFrame(data)
        df["timestamp"] = pandas.to_datetime(df["timestamp"])

        result = TectonDataFrame._cast_timestamps_to_utc_aware_pandas(df)
        expected_data = {"timestamp": ["2024-01-01 00:00:00", "2024-01-01 12:00:00"]}
        expected = pandas.DataFrame(expected_data).astype(
            {
                "timestamp": "datetime64[us]",
            }
        )
        expected["timestamp"] = expected["timestamp"].dt.tz_localize("UTC")

        pandas.testing.assert_frame_equal(result, expected)

    def test_to_utc_aware_pandas_with_non_utc_timezone(self):
        data = {"timestamp": ["2024-01-01 05:00:00+05:00", "2024-01-01 17:00:00+05:00"]}
        df = pandas.DataFrame(data)
        df["timestamp"] = pandas.to_datetime(df["timestamp"]).astype(
            {
                "timestamp": "datetime64[us, America/New_York]",
            }
        )

        result = TectonDataFrame._cast_timestamps_to_utc_aware_pandas(df)
        expected_data = {"timestamp": ["2024-01-01 00:00:00", "2024-01-01 12:00:00"]}
        expected = pandas.DataFrame(expected_data).astype(
            {
                "timestamp": "datetime64[us]",
            }
        )
        expected["timestamp"] = expected["timestamp"].dt.tz_localize("UTC")
        pandas.testing.assert_frame_equal(result, expected)

    def test_to_utc_aware_pandas_with_mixed_timestamps(self):
        data = {
            "timestamp_naive": ["2024-01-01 00:00:00", "2024-01-01 12:00:00"],
            "timestamp_aware": ["2024-01-01 05:00:00+05:00", "2024-01-01 17:00:00+05:00"],
        }
        df = pandas.DataFrame(data)
        df["timestamp_naive"] = pandas.to_datetime(df["timestamp_naive"])
        df["timestamp_aware"] = pandas.to_datetime(df["timestamp_aware"])

        result = TectonDataFrame._cast_timestamps_to_utc_aware_pandas(df)
        expected_data = {
            "timestamp_naive": ["2024-01-01 00:00:00", "2024-01-01 12:00:00"],
            "timestamp_aware": ["2024-01-01 00:00:00", "2024-01-01 12:00:00"],
        }
        expected = pandas.DataFrame(expected_data).astype(
            {
                "timestamp_naive": "datetime64[us]",
                "timestamp_aware": "datetime64[us]",
            }
        )
        expected["timestamp_naive"] = expected["timestamp_naive"].dt.tz_localize("UTC")
        expected["timestamp_aware"] = expected["timestamp_aware"].dt.tz_localize("UTC")

        pandas.testing.assert_frame_equal(result, expected)

    def test_to_utc_aware_pandas_with_already_utc(self):
        data = {"timestamp": ["2024-01-01 00:00:00+00:00", "2024-01-01 12:00:00+00:00"]}
        df = pandas.DataFrame(data)
        df["timestamp"] = pandas.to_datetime(df["timestamp"]).astype(
            {
                "timestamp": "datetime64[us, UTC]",
            }
        )

        result = TectonDataFrame._cast_timestamps_to_utc_aware_pandas(df)
        expected_data = {"timestamp": ["2024-01-01 00:00:00", "2024-01-01 12:00:00"]}
        expected = pandas.DataFrame(expected_data).astype(
            {
                "timestamp": "datetime64[us]",
            }
        )
        expected["timestamp"] = expected["timestamp"].dt.tz_localize("UTC")

        pandas.testing.assert_frame_equal(result, expected)

    def test_to_utc_aware_pandas_with_incorrect_input(self):
        data = {
            "timestamp": ["2024-01-01 00:00:00", "2024-01-01 12:00:00"],
            "timestamp2": ["2024-01-01 00:00:00+00:00", "invalid_date"],
            "value": [10, None],
            "non_datetime": ["string1", "string2"],
        }
        df = pandas.DataFrame(data)
        df["timestamp"] = pandas.to_datetime(df["timestamp"])
        result = TectonDataFrame._cast_timestamps_to_utc_aware_pandas(df)
        expected_data = {
            "timestamp": ["2024-01-01 00:00:00", "2024-01-01 12:00:00"],
            "timestamp2": ["2024-01-01 00:00:00+00:00", "invalid_date"],
            "value": [10, None],
            "non_datetime": ["string1", "string2"],
        }
        expected = pandas.DataFrame(expected_data).astype(
            {
                "timestamp": "datetime64[us]",
                "value": "float64",
            }
        )
        expected["timestamp"] = expected["timestamp"].dt.tz_localize("UTC")
        pandas.testing.assert_frame_equal(result, expected)
