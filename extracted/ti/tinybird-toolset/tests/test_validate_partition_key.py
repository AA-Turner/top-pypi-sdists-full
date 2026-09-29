import unittest
from chtoolset import query as chquery


class TestValidatePartitionKey(unittest.TestCase):
    def test_valid_empty_partition_key(self):
        self.assertIsNone(
            chquery.validate_partition_key(
                columns=[{"name": "ts", "type": "DateTime"}],
                partition_key="",
            )
        )

    def test_valid_hourly_partition_key(self):
        # Hour is the floor - allowed.
        self.assertIsNone(
            chquery.validate_partition_key(
                columns=[{"name": "ts", "type": "DateTime"}],
                partition_key="toStartOfHour(ts)",
            )
        )

    def test_valid_daily_partition_key(self):
        self.assertIsNone(
            chquery.validate_partition_key(
                columns=[{"name": "ts", "type": "DateTime"}],
                partition_key="toDate(ts)",
            )
        )

    def test_valid_monthly_partition_key(self):
        self.assertIsNone(
            chquery.validate_partition_key(
                columns=[{"name": "ts", "type": "DateTime"}],
                partition_key="toYYYYMM(ts)",
            )
        )

    def test_invalid_minute_partition_key(self):
        err = chquery.validate_partition_key(
            columns=[{"name": "ts", "type": "DateTime"}],
            partition_key="toStartOfMinute(ts)",
        )
        self.assertEqual(
            err,
            "Partition key granularity (Minute) on column 'ts' is finer than hourly. This tends to create a very "
            "large number of parts, which makes merges and queries expensive regardless of the table's TTL. Use "
            "an hourly or coarser partition key.",
        )

    def test_invalid_second_partition_key(self):
        err = chquery.validate_partition_key(
            columns=[{"name": "ts", "type": "DateTime"}],
            partition_key="toStartOfSecond(ts)",
        )
        self.assertEqual(
            err,
            "Partition key granularity (Second) on column 'ts' is finer than hourly. This tends to create a very "
            "large number of parts, which makes merges and queries expensive regardless of the table's TTL. Use "
            "an hourly or coarser partition key.",
        )

    def test_invalid_five_minute_partition_key(self):
        err = chquery.validate_partition_key(
            columns=[{"name": "ts", "type": "DateTime"}],
            partition_key="toStartOfFiveMinutes(ts)",
        )
        self.assertEqual(
            err,
            "Partition key granularity (Minute) on column 'ts' is finer than hourly. This tends to create a very "
            "large number of parts, which makes merges and queries expensive regardless of the table's TTL. Use "
            "an hourly or coarser partition key.",
        )

    def test_invalid_ten_minute_partition_key(self):
        err = chquery.validate_partition_key(
            columns=[{"name": "ts", "type": "DateTime"}],
            partition_key="toStartOfTenMinutes(ts)",
        )
        self.assertEqual(
            err,
            "Partition key granularity (Minute) on column 'ts' is finer than hourly. This tends to create a very "
            "large number of parts, which makes merges and queries expensive regardless of the table's TTL. Use "
            "an hourly or coarser partition key.",
        )

    def test_invalid_fifteen_minute_partition_key(self):
        err = chquery.validate_partition_key(
            columns=[{"name": "ts", "type": "DateTime"}],
            partition_key="toStartOfFifteenMinutes(ts)",
        )
        self.assertEqual(
            err,
            "Partition key granularity (Minute) on column 'ts' is finer than hourly. This tends to create a very "
            "large number of parts, which makes merges and queries expensive regardless of the table's TTL. Use "
            "an hourly or coarser partition key.",
        )

    def test_invalid_five_minute_singular_alias_partition_key(self):
        # toStartOfFiveMinute (singular) is a registered alias for toStartOfFiveMinutes.
        err = chquery.validate_partition_key(
            columns=[{"name": "ts", "type": "DateTime"}],
            partition_key="toStartOfFiveMinute(ts)",
        )
        self.assertEqual(
            err,
            "Partition key granularity (Minute) on column 'ts' is finer than hourly. This tends to create a very "
            "large number of parts, which makes merges and queries expensive regardless of the table's TTL. Use "
            "an hourly or coarser partition key.",
        )

    def test_invalid_millisecond_partition_key(self):
        err = chquery.validate_partition_key(
            columns=[{"name": "ts", "type": "DateTime64(3)"}],
            partition_key="toStartOfMillisecond(ts)",
        )
        self.assertEqual(
            err,
            "Partition key granularity (Millisecond) on column 'ts' is finer than hourly. This tends to create a "
            "very large number of parts, which makes merges and queries expensive regardless of the table's TTL. "
            "Use an hourly or coarser partition key.",
        )

    def test_invalid_microsecond_partition_key(self):
        err = chquery.validate_partition_key(
            columns=[{"name": "ts", "type": "DateTime64(6)"}],
            partition_key="toStartOfMicrosecond(ts)",
        )
        self.assertEqual(
            err,
            "Partition key granularity (Microsecond) on column 'ts' is finer than hourly. This tends to create a "
            "very large number of parts, which makes merges and queries expensive regardless of the table's TTL. "
            "Use an hourly or coarser partition key.",
        )

    def test_invalid_nanosecond_partition_key(self):
        err = chquery.validate_partition_key(
            columns=[{"name": "ts", "type": "DateTime64(9)"}],
            partition_key="toStartOfNanosecond(ts)",
        )
        self.assertEqual(
            err,
            "Partition key granularity (Nanosecond) on column 'ts' is finer than hourly. This tends to create a "
            "very large number of parts, which makes merges and queries expensive regardless of the table's TTL. "
            "Use an hourly or coarser partition key.",
        )

    def test_invalid_yyyymmddhhmmss_partition_key(self):
        # Packs the full date+time down to the second - no coarsening at all.
        err = chquery.validate_partition_key(
            columns=[{"name": "ts", "type": "DateTime"}],
            partition_key="toYYYYMMDDhhmmss(ts)",
        )
        self.assertEqual(
            err,
            "Partition key granularity (Second) on column 'ts' is finer than hourly. This tends to create a very "
            "large number of parts, which makes merges and queries expensive regardless of the table's TTL. Use "
            "an hourly or coarser partition key.",
        )

    def test_valid_skipped_for_composite_partition_key(self):
        self.assertIsNone(
            chquery.validate_partition_key(
                columns=[
                    {"name": "ts", "type": "DateTime"},
                    {"name": "k", "type": "String"},
                ],
                partition_key="toStartOfMinute(ts), k",
            )
        )

    def test_valid_skipped_for_unrecognized_function(self):
        self.assertIsNone(
            chquery.validate_partition_key(
                columns=[{"name": "ts", "type": "DateTime"}],
                partition_key="intDiv(toUInt32(ts), 60)",
            )
        )

    def test_valid_skipped_for_bare_column(self):
        self.assertIsNone(
            chquery.validate_partition_key(
                columns=[{"name": "k", "type": "String"}],
                partition_key="k",
            )
        )

    def test_invalid_bare_datetime_partition_key(self):
        err = chquery.validate_partition_key(
            columns=[{"name": "ts", "type": "DateTime"}],
            partition_key="ts",
        )
        self.assertEqual(
            err,
            "Partition key granularity (Second) on column 'ts' is finer than hourly. This tends to create a very "
            "large number of parts, which makes merges and queries expensive regardless of the table's TTL. Use "
            "an hourly or coarser partition key, e.g. toStartOfHour(ts), toYYYYMMDD(ts), or toYYYYMM(ts).",
        )

    def test_invalid_bare_datetime64_partition_key(self):
        err = chquery.validate_partition_key(
            columns=[{"name": "ts", "type": "DateTime64(3)"}],
            partition_key="ts",
        )
        self.assertEqual(
            err,
            "Partition key granularity (Millisecond) on column 'ts' is finer than hourly. This tends to create a "
            "very large number of parts, which makes merges and queries expensive regardless of the table's TTL. "
            "Use an hourly or coarser partition key, e.g. toStartOfHour(ts), toYYYYMMDD(ts), or toYYYYMM(ts).",
        )

    def test_valid_skipped_for_bare_date_column(self):
        self.assertIsNone(
            chquery.validate_partition_key(
                columns=[{"name": "d", "type": "Date"}],
                partition_key="d",
            )
        )


if __name__ == "__main__":
    unittest.main()
