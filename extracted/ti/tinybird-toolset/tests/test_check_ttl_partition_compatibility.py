import unittest
from chtoolset import query as chquery


class TestCheckTTLPartitionCompatibility(unittest.TestCase):
    def test_checked_and_compatible(self):
        result = chquery.check_ttl_partition_compatibility(
            columns=[{"name": "ts", "type": "DateTime"}],
            ttl="ts + INTERVAL 1 MONTH",
            sorting_key="ts",
            primary_key="ts",
            partition_key="toYYYYMM(ts)",
        )
        self.assertTrue(result["checked"])
        self.assertIsNone(result["error"])

    def test_checked_and_compatible_uses_interval_count(self):
        result = chquery.check_ttl_partition_compatibility(
            columns=[{"name": "ts", "type": "DateTime"}],
            ttl="ts + INTERVAL 90 DAY",
            sorting_key="ts",
            primary_key="ts",
            partition_key="toYYYYMM(ts)",
        )
        self.assertTrue(result["checked"])
        self.assertIsNone(result["error"])

    def test_checked_and_incompatible(self):
        result = chquery.check_ttl_partition_compatibility(
            columns=[{"name": "ts", "type": "DateTime"}],
            ttl="ts + INTERVAL 7 DAY",
            sorting_key="ts",
            primary_key="ts",
            partition_key="toYYYYMM(ts)",
        )
        self.assertTrue(result["checked"])
        self.assertIsNotNone(result["error"])
        self.assertIn("shorter than the partition key period", result["error"])

    def test_mixed_where_clause_ttl_is_not_checked(self):
        # A WHERE clause makes the whole statement ineligible for ttl_only_drop_parts,
        # including when it also contains an unconditional TTL.
        result = chquery.check_ttl_partition_compatibility(
            columns=[
                {"name": "ts", "type": "DateTime"},
                {"name": "status", "type": "String"},
            ],
            ttl="ts + INTERVAL 1 MONTH, ts + INTERVAL 1 DAY WHERE status = 'expired'",
            sorting_key="ts",
            primary_key="ts",
            partition_key="toYYYYMM(ts)",
        )
        self.assertFalse(result["checked"])
        self.assertIsNone(result["error"])

    def test_not_checked_when_a_ttl_clause_is_unrecognized(self):
        # An unrecognized unconditional TTL remains unchecked; the WHERE clause also makes the
        # whole statement ineligible for the optimization.
        result = chquery.check_ttl_partition_compatibility(
            columns=[
                {"name": "ts", "type": "DateTime"},
                {"name": "other_col", "type": "DateTime"},
                {"name": "flag", "type": "UInt8"},
            ],
            ttl="toDateTime(other_col) + INTERVAL 1 DAY, ts + INTERVAL 1 MONTH WHERE flag = 1",
            sorting_key="ts",
            primary_key="ts",
            partition_key="toYYYYMM(ts)",
        )
        self.assertFalse(result["checked"])
        self.assertIsNone(result["error"])

        # validate_ttl, by contrast, silently accepts it - confirming the gap this function closes.
        self.assertIsNone(
            chquery.validate_ttl(
                columns=[
                    {"name": "ts", "type": "DateTime"},
                    {"name": "other_col", "type": "DateTime"},
                    {"name": "flag", "type": "UInt8"},
                ],
                ttl="toDateTime(other_col) + INTERVAL 1 DAY, ts + INTERVAL 1 MONTH WHERE flag = 1",
                sorting_key="ts",
                primary_key="ts",
                partition_key="toYYYYMM(ts)",
            )
        )

    def test_not_checked_when_only_where_ttl_exists(self):
        result = chquery.check_ttl_partition_compatibility(
            columns=[
                {"name": "ts", "type": "DateTime"},
                {"name": "flag", "type": "UInt8"},
            ],
            ttl="ts + INTERVAL 1 DAY WHERE flag = 1",
            sorting_key="ts",
            primary_key="ts",
            partition_key="toYYYYMM(ts)",
        )
        self.assertFalse(result["checked"])
        self.assertIsNone(result["error"])

    def test_not_checked_when_ttl_column_differs_from_partition_column(self):
        result = chquery.check_ttl_partition_compatibility(
            columns=[
                {"name": "ts", "type": "DateTime"},
                {"name": "updated_at", "type": "DateTime"},
            ],
            ttl="updated_at + INTERVAL 7 DAY",
            sorting_key="ts",
            primary_key="ts",
            partition_key="toYYYYMM(ts)",
        )
        self.assertFalse(result["checked"])
        self.assertIsNone(result["error"])

    def test_not_checked_for_composite_partition_key(self):
        result = chquery.check_ttl_partition_compatibility(
            columns=[
                {"name": "ts", "type": "DateTime"},
                {"name": "k", "type": "String"},
            ],
            ttl="ts + INTERVAL 7 DAY",
            sorting_key="ts",
            primary_key="ts",
            partition_key="toYYYYMM(ts), k",
        )
        self.assertFalse(result["checked"])
        self.assertIsNone(result["error"])

    def test_not_checked_for_unrecognized_partition_function(self):
        result = chquery.check_ttl_partition_compatibility(
            columns=[{"name": "ts", "type": "DateTime"}],
            ttl="ts + INTERVAL 7 DAY",
            sorting_key="ts",
            primary_key="ts",
            partition_key="intDiv(toUInt32(ts), 86400)",
        )
        self.assertFalse(result["checked"])
        self.assertIsNone(result["error"])

    def test_not_checked_when_no_partition_key(self):
        result = chquery.check_ttl_partition_compatibility(
            columns=[{"name": "ts", "type": "DateTime"}],
            ttl="ts + INTERVAL 7 DAY",
            sorting_key="ts",
            primary_key="ts",
        )
        self.assertFalse(result["checked"])
        self.assertIsNone(result["error"])

    def test_not_checked_when_no_ttl(self):
        result = chquery.check_ttl_partition_compatibility(
            columns=[{"name": "ts", "type": "DateTime"}],
            ttl="",
            sorting_key="ts",
            primary_key="ts",
            partition_key="toYYYYMM(ts)",
        )
        self.assertFalse(result["checked"])
        self.assertIsNone(result["error"])

    def test_not_checked_on_malformed_ttl(self):
        result = chquery.check_ttl_partition_compatibility(
            columns=[{"name": "ts", "type": "DateTime"}],
            ttl="this is not a valid ttl !!!",
            sorting_key="ts",
            primary_key="ts",
            partition_key="toYYYYMM(ts)",
        )
        self.assertFalse(result["checked"])
        self.assertIsNone(result["error"])


if __name__ == "__main__":
    unittest.main()
