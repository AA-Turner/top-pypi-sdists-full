import unittest
from chtoolset import query as chquery


class TestValidateTTL(unittest.TestCase):
    def test_empty_ttl_is_valid(self):
        self.assertIsNone(
            chquery.validate_ttl(
                ttl="",
                columns=[{"name": "ts", "type": "DateTime"}],
                sorting_key="ts",
                primary_key="ts",
            )
        )

    def test_valid_no_primary_key_uses_sorting_key(self):
        self.assertIsNone(
            chquery.validate_ttl(
                ttl="ts + INTERVAL 7 DAY",
                columns=[{"name": "ts", "type": "DateTime"}],
                sorting_key="ts",
            )
        )

    def test_valid_datetime_plus_interval(self):
        self.assertIsNone(
            chquery.validate_ttl(
                ttl="ts + INTERVAL 7 DAY",
                columns=[{"name": "ts", "type": "DateTime"}, {"name": "v", "type": "Int32"}],
                sorting_key="ts",
                primary_key="ts",
            )
        )

    def test_valid_datetime_plus_to_interval(self):
        self.assertIsNone(
            chquery.validate_ttl(
                ttl="ts + toIntervalDay(7)",
                columns=[{"name": "ts", "type": "DateTime"}],
                sorting_key="ts",
                primary_key="ts",
            )
        )

    def test_valid_date_column(self):
        self.assertIsNone(
            chquery.validate_ttl(
                ttl="d + INTERVAL 30 DAY",
                columns=[{"name": "d", "type": "Date"}],
                sorting_key="d",
                primary_key="d",
            )
        )

    def test_valid_wrapped_datetime64(self):
        self.assertIsNone(
            chquery.validate_ttl(
                ttl="toDateTime(event_time) + toIntervalDay(7)",
                columns=[{"name": "event_time", "type": "DateTime64(3)"}],
                sorting_key="event_time",
                primary_key="event_time",
            )
        )

    def test_invalid_non_date_result_type(self):
        err = chquery.validate_ttl(
            ttl="counter + toIntervalDay(7)",
            columns=[{"name": "counter", "type": "Int32"}],
            sorting_key="counter",
            primary_key="counter",
        )
        self.assertIsNotNone(err)
        self.assertIn("Illegal types", err)

    def test_valid_datetime_plus_integer_expression(self):
        self.assertIsNone(
            chquery.validate_ttl(
                ttl="ts + 7",
                columns=[{"name": "ts", "type": "DateTime"}],
                sorting_key="ts",
                primary_key="ts",
            )
        )

    def test_invalid_unwrapped_datetime64(self):
        err = chquery.validate_ttl(
            ttl="event_time + toIntervalDay(7)",
            columns=[{"name": "event_time", "type": "DateTime64(3)"}],
            sorting_key="event_time",
            primary_key="event_time",
        )
        self.assertIsNotNone(err)
        self.assertIn("TTL expression result column should have DateTime or Date type", err)

    def test_invalid_unknown_column(self):
        err = chquery.validate_ttl(
            ttl="missing + INTERVAL 7 DAY",
            columns=[{"name": "ts", "type": "DateTime"}],
            sorting_key="ts",
            primary_key="ts",
        )
        self.assertIsNotNone(err)
        self.assertIn("Missing columns: 'missing'", err)

    def test_invalid_malformed_ttl(self):
        err = chquery.validate_ttl(
            ttl="this is not a valid ttl !!!",
            columns=[{"name": "ts", "type": "DateTime"}],
            sorting_key="ts",
            primary_key="ts",
        )
        self.assertIsNotNone(err)
        self.assertIn("Syntax error", err)

    # --- Date/time functions supported by ClickHouse in TTL expressions ---
    def test_valid_from_unix_timestamp(self):
        self.assertIsNone(
            chquery.validate_ttl(
                ttl="fromUnixTimestamp(uts) + INTERVAL 7 DAY",
                columns=[{"name": "uts", "type": "UInt32"}],
                sorting_key="uts",
                primary_key="uts",
            )
        )

    def test_valid_from_unix_timestamp64_milli(self):
        self.assertIsNone(
            chquery.validate_ttl(
                ttl="toDateTime(fromUnixTimestamp64Milli(uts)) + INTERVAL 7 DAY",
                columns=[{"name": "uts", "type": "Int64"}],
                sorting_key="uts",
                primary_key="uts",
            )
        )

    def test_valid_from_unix_timestamp64_micro_and_nano(self):
        for fn in ("fromUnixTimestamp64Micro", "fromUnixTimestamp64Nano"):
            with self.subTest(fn=fn):
                self.assertIsNone(
                    chquery.validate_ttl(
                        ttl=f"toDateTime({fn}(uts)) + INTERVAL 1 DAY",
                        columns=[{"name": "uts", "type": "Int64"}],
                        sorting_key="uts",
                        primary_key="uts",
                    )
                )

    def test_valid_to_start_of_functions(self):
        for fn in (
            "toStartOfDay",
            "toStartOfHour",
            "toStartOfMinute",
            "toStartOfFifteenMinutes",
            "toStartOfMonth",
            "toStartOfQuarter",
            "toStartOfYear",
            "toStartOfWeek",
            "toMonday",
            "toLastDayOfMonth",
        ):
            with self.subTest(fn=fn):
                self.assertIsNone(
                    chquery.validate_ttl(
                        ttl=f"{fn}(ts) + INTERVAL 30 DAY",
                        columns=[{"name": "ts", "type": "DateTime"}],
                        sorting_key="ts",
                        primary_key="ts",
                    )
                )

    def test_valid_to_start_of_interval(self):
        self.assertIsNone(
            chquery.validate_ttl(
                ttl="toStartOfInterval(ts, INTERVAL 1 DAY) + INTERVAL 90 DAY",
                columns=[{"name": "ts", "type": "DateTime"}],
                sorting_key="ts",
                primary_key="ts",
            )
        )

    def test_valid_date_trunc(self):
        self.assertIsNone(
            chquery.validate_ttl(
                ttl="dateTrunc('month', ts) + INTERVAL 6 MONTH",
                columns=[{"name": "ts", "type": "DateTime"}],
                sorting_key="ts",
                primary_key="ts",
            )
        )

    def test_valid_to_timezone(self):
        self.assertIsNone(
            chquery.validate_ttl(
                ttl="toTimezone(ts, 'UTC') + INTERVAL 7 DAY",
                columns=[{"name": "ts", "type": "DateTime"}],
                sorting_key="ts",
                primary_key="ts",
            )
        )

    def test_valid_make_date(self):
        self.assertIsNone(
            chquery.validate_ttl(
                ttl="makeDate(y, m, d) + INTERVAL 7 DAY",
                columns=[
                    {"name": "y", "type": "UInt16"},
                    {"name": "m", "type": "UInt8"},
                    {"name": "d", "type": "UInt8"},
                ],
                sorting_key="y",
                primary_key="y",
            )
        )

    # --- Conditional / multi-clause TTLs ---
    def test_valid_ttl_with_where(self):
        self.assertIsNone(
            chquery.validate_ttl(
                ttl="ts + INTERVAL 7 DAY WHERE status = 'expired'",
                columns=[
                    {"name": "ts", "type": "DateTime"},
                    {"name": "status", "type": "String"},
                ],
                sorting_key="ts",
                primary_key="ts",
            )
        )

    def test_valid_ttl_with_where_numeric(self):
        self.assertIsNone(
            chquery.validate_ttl(
                ttl="ts + INTERVAL 30 DAY WHERE x % 10 == 0 AND y > 5",
                columns=[
                    {"name": "ts", "type": "DateTime"},
                    {"name": "x", "type": "Int32"},
                    {"name": "y", "type": "Int32"},
                ],
                sorting_key="ts",
                primary_key="ts",
            )
        )

    def test_invalid_ttl_where_unknown_column(self):
        err = chquery.validate_ttl(
            ttl="ts + INTERVAL 7 DAY WHERE missing = 1",
            columns=[{"name": "ts", "type": "DateTime"}],
            sorting_key="ts",
            primary_key="ts",
        )
        self.assertIsNotNone(err)
        self.assertIn("Missing columns: 'missing'", err)

    def test_valid_ttl_where_string_expression(self):
        self.assertIsNone(
            chquery.validate_ttl(
                ttl="ts + INTERVAL 7 DAY WHERE status",
                columns=[
                    {"name": "ts", "type": "DateTime"},
                    {"name": "status", "type": "String"},
                ],
                sorting_key="ts",
                primary_key="ts",
            )
        )

    def test_valid_multiple_ttls_comma_separated(self):
        self.assertIsNone(
            chquery.validate_ttl(
                ttl="ts + INTERVAL 7 DAY WHERE status = 'a', ts + INTERVAL 14 DAY WHERE status = 'b'",
                columns=[
                    {"name": "ts", "type": "DateTime"},
                    {"name": "status", "type": "String"},
                ],
                sorting_key="ts",
                primary_key="ts",
            )
        )

    def test_valid_ttl_group_by(self):
        # GROUP BY rollup; must group by a prefix of the primary key
        self.assertIsNone(
            chquery.validate_ttl(
                ttl="ts + INTERVAL 1 DAY GROUP BY k SET v = sum(v)",
                columns=[
                    {"name": "k", "type": "String"},
                    {"name": "ts", "type": "DateTime"},
                    {"name": "v", "type": "Int64"},
                ],
                sorting_key="k",
                primary_key="k",
            )
        )

    def test_invalid_ttl_group_by_not_in_primary_key(self):
        err = chquery.validate_ttl(
            ttl="ts + INTERVAL 1 DAY GROUP BY missing SET v = sum(v)",
            columns=[
                {"name": "k", "type": "String"},
                {"name": "ts", "type": "DateTime"},
                {"name": "v", "type": "Int64"},
            ],
            sorting_key="k",
            primary_key="k",
        )
        self.assertIsNotNone(err)
        self.assertIn("GROUP BY key should be a prefix of primary key", err)

    def test_valid_where_string_functions(self):
        columns = [
            {"name": "ts", "type": "DateTime"},
            {"name": "s", "type": "String"},
            {"name": "n", "type": "Int32"},
        ]
        predicates = {
            "concat": "concat(s, 'x') = 'ax'",
            "startsWith": "startsWith(s, 'a')",
            "endsWith": "endsWith(s, 'z')",
            "length": "length(s) > 3",
            "lower": "lower(s) = 'a'",
            "substring": "substring(s, 1, 2) = 'ab'",
            "match": "match(s, '^a')",
            "in": "n IN (1, 2, 3)",
        }
        for name, predicate in predicates.items():
            with self.subTest(fn=name):
                self.assertIsNone(
                    chquery.validate_ttl(
                        ttl=f"ts + INTERVAL 7 DAY WHERE {predicate}",
                        columns=columns,
                        sorting_key="ts",
                        primary_key="ts",
                    ),
                    f"{name} should be a known function in TTL WHERE clauses",
                )

    # --- Hash functions in sorting / primary keys (KeyDescription::parse) ---
    def test_valid_sorting_key_with_cityhash64(self):
        self.assertIsNone(
            chquery.validate_ttl(
                ttl="timestamp + INTERVAL 365 DAY",
                columns=[
                    {"name": "organizationId", "type": "String"},
                    {"name": "surfaceId", "type": "String"},
                    {"name": "timestamp", "type": "DateTime"},
                    {"name": "name", "type": "String"},
                    {"name": "traceId", "type": "String"},
                    {"name": "spanId", "type": "String"},
                    {"name": "eventIndex", "type": "UInt32"},
                ],
                sorting_key="organizationId, surfaceId, toDate(timestamp), name, cityHash64(traceId), spanId, eventIndex",
            )
        )

    # --- Arithmetic functions in TTL expressions ---
    def test_valid_ttl_with_int_div(self):
        # Reported failure: "Unknown function intDiv".
        self.assertIsNone(
            chquery.validate_ttl(
                ttl="toDateTime(intDiv(ts_server, 1000)) + INTERVAL 13 MONTH",
                columns=[{"name": "ts_server", "type": "Int64"}],
                sorting_key="ts_server",
            )
        )

    def test_valid_ttl_with_greatest(self):
        # Reported failure: "Unknown function greatest".
        self.assertIsNone(
            chquery.validate_ttl(
                ttl="greatest(departure_date, toDateTime(creation_date)) + toIntervalDay(2)",
                columns=[
                    {"name": "departure_date", "type": "DateTime"},
                    {"name": "creation_date", "type": "Date"},
                ],
                sorting_key="departure_date",
            )
        )

    # --- Input validation ---
    def test_columns_must_be_list_of_dicts(self):
        with self.assertRaises(TypeError):
            chquery.validate_ttl(ttl="ts + INTERVAL 7 DAY", columns="ts DateTime", sorting_key="ts", primary_key="ts")

    def test_column_dict_requires_name_and_type(self):
        with self.assertRaises((TypeError, ValueError)):
            chquery.validate_ttl(
                ttl="ts + INTERVAL 7 DAY",
                columns=[{"name": "ts"}],
                sorting_key="ts",
                primary_key="ts",
            )


    # --- Regression guard: sequential throwing calls must not crash ---
    def test_sequential_throwing_calls_do_not_crash(self):
        # A validate_ttl call that throws must not corrupt shared state and take
        # down a subsequent call. validateTTL parses against a private per-call
        # context copy (functions/ValidateTTL.cpp) precisely so this holds.
        # Run in a subprocess so a hypothetical crash doesn't kill pytest; the
        # child must exit 0.
        import signal
        import subprocess
        import sys
        import textwrap
        repro = textwrap.dedent("""\
            from chtoolset import query as q
            err1 = q.validate_ttl(
                ttl="counter + toIntervalDay(7)",
                columns=[{"name": "counter", "type": "Int32"}],
                sorting_key="counter",
                primary_key="counter",
            )
            assert err1 is not None and "Illegal types" in err1, (
                f"call 1 should return an 'Illegal types' error, got: {err1!r}")
            q.validate_ttl(
                ttl="ts + INTERVAL 7 DAY WHERE missing = 1",
                columns=[{"name": "ts", "type": "DateTime"}],
                sorting_key="ts",
                primary_key="ts",
            )
        """)
        result = subprocess.run([sys.executable, "-c", repro],
                                capture_output=True, text=True, timeout=30)
        if result.returncode != 0 and result.returncode != -signal.SIGABRT:
            raise RuntimeError(
                f"Unexpected subprocess exit {result.returncode} "
                f"(expected 0 or SIGABRT {-signal.SIGABRT})."
                f"\nSTDERR:\n{result.stderr}"
                f"\nSTDOUT:\n{result.stdout}")
        self.assertEqual(result.returncode, 0,
                         f"Subprocess crashed with SIGABRT."
                         f"\nSTDERR:\n{result.stderr}"
                         f"\nSTDOUT:\n{result.stdout}")


if __name__ == "__main__":
    unittest.main()
