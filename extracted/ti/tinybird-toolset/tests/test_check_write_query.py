import unittest
from chtoolset import query


class TestGeneral(unittest.TestCase):
    def test_invalid_input_types(self):
        with self.assertRaises(TypeError):
            query.check_valid_write_query()

        with self.assertRaises(TypeError):
            query.check_valid_write_query(None)

        with self.assertRaises(TypeError):
            query.check_valid_write_query([0, 1, 3])

        with self.assertRaises(ValueError):
            query.check_valid_write_query("")

        with self.assertRaises(ValueError):
            query.check_valid_write_query("FROM table THIS IS NOT A QUERY")

    def test_invalid_query_type(self):
        queries = [
            "SELECT 1",
            "INSERT INTO test.table VALUES (1,2,3)",
            "DROP TABLE test",
            "SHOW DATABASES",
            "ALTER TABLE alter_test ADD COLUMN Added1 UInt32 FIRST",
            "EXCHANGE TABLES table_a AND table_b",
            "KILL QUERY WHERE query_id='hash'",
            "RENAME TABLE table_a TO table_b",
            "ALTER TABLE github_events ADD PROJECTION projection_user_sort ( SELECT * ORDER BY username );"
        ]
        for q in queries:
            with self.assertRaisesRegex(ValueError, 'Unsupported write query type'):
                query.check_valid_write_query(q)


class TestCreateTable(unittest.TestCase):
    maxDiff = None

    def test_invalid_create(self):
        with self.assertRaisesRegex(ValueError, 'Unsupported CREATE query type. Only CREATE TABLE is supported'):
            query.check_valid_write_query("CREATE DATABASE test")

        with self.assertRaisesRegex(ValueError, 'Unsupported CREATE query type. Only CREATE TABLE is supported'):
            query.check_valid_write_query("ATTACH DATABASE test")

        with self.assertRaisesRegex(ValueError, 'Unsupported CREATE query type. Only CREATE TABLE is supported'):
            query.check_valid_write_query("CREATE VIEW view AS SELECT * FROM mytable")

        with self.assertRaisesRegex(ValueError, 'Unsupported CREATE query type. Only CREATE TABLE is supported'):
            query.check_valid_write_query("ATTACH VIEW view AS SELECT * FROM mytable")

        with self.assertRaisesRegex(ValueError, 'Unsupported CREATE query type. Only CREATE TABLE is supported'):
            query.check_valid_write_query("""
                CREATE MATERIALIZED VIEW test_table_dependent_view_1.mv1 TO test_table_dependent_view_1.ds2 AS
                SELECT count(*) as count FROM test_table_dependent_view_1.ds1""")

        with self.assertRaisesRegex(ValueError, 'Unsupported CREATE query type. Only CREATE TABLE is supported'):
            query.check_valid_write_query("""
                ATTACH TABLE big_table (number Int64) ENGINE = MergeTree Order by tuple()""")

        with self.assertRaisesRegex(ValueError, 'Unsupported CREATE query type. Only CREATE TABLE is supported'):
            query.check_valid_write_query("""
                CREATE DICTIONARY dictionary_with_comment
                (
                    id UInt64,
                    value String
                )
                PRIMARY KEY id
                SOURCE(CLICKHOUSE(HOST 'localhost' PORT tcpPort() TABLE 'source_table'))
                LAYOUT(FLAT())
                LIFETIME(MIN 0 MAX 1000)
                COMMENT 'The temporary dictionary'""")

        with self.assertRaisesRegex(ValueError, 'Multi-statements are not allowed'):
            query.check_valid_write_query("""
                CREATE TABLE big_table (number Int64) ENGINE = MergeTree Order by tuple();
                CREATE TABLE hack (name String) Engine=MergeTree() order by tuple() AS Select name FROM system.tables""")

        self.assertTrue("CREATE TABLE big_table (number Int64) ENGINE = MergeTree Order by tuple()")

    def test_valid_create_table(self):
        q = 'CREATE TABLE big_table (number Int64) ENGINE = MergeTree Order by tuple()'
        self.assertEqual(query.format(query.check_valid_write_query(q)), query.format(q))

        q = 'CREATE OR REPLACE TABLE big_table (number Int64) ENGINE = MergeTree Order by tuple()'
        self.assertEqual(query.format(query.check_valid_write_query(q)), query.format(q))

        q = 'CREATE OR REPLACE TABLE big_table AS small_table'
        self.assertEqual(query.format(query.check_valid_write_query(q)), query.format(q))

        q = """CREATE TABLE visits
                (
                    `event_time` DateTime,
                    `query` String
                )
                ENGINE = MergeTree
                PARTITION BY toYYYYMM(event_time)
                ORDER BY event_time"""
        self.assertEqual(query.format(query.check_valid_write_query(q)), query.format(q))

        q = """CREATE TABLE visits
                (
                    `event_time` DateTime,
                    `query` String,
                    `tomorrow` DateTime MATERIALIZED toStartOfDay(`event_time`) + INTERVAL 1 DAY
                )
                ENGINE = MergeTree
                PARTITION BY toYYYYMM(event_time)
                ORDER BY event_time"""
        self.assertEqual(query.format(query.check_valid_write_query(q)), query.format(q))

        q = """CREATE TABLE visits6
                (
                    `event_time` DateTime,
                    `query` String,
                    `three` String
                )
                ENGINE = MergeTree
                PARTITION BY toYYYYMM(event_time)
                PRIMARY KEY (event_time, three)"""
        self.assertEqual(query.format(query.check_valid_write_query(q)), query.format(q))

        q = """
            CREATE TABLE d_e839af.t_14d2033fd3cb4cb796ae6c407ab46f76_quarantine UUID '81db5884-7661-496b-96f6-6a52e859cdf9'
            (
                `c__error_column` Array(String),
                `c__error` Array(String),
                `c__import_id` Nullable(String),
                `a` Nullable(String),
                `b` Nullable(String),
                `c` Nullable(String),
                `d` Nullable(String),
                `insertion_date` DateTime DEFAULT now()
            )
            ENGINE = ReplicatedMergeTree('/clickhouse/tables/{layer}-{shard}/d_e839af.t_14d2033fd3cb4cb796ae6c407ab46f76_quarantine', '{replica}')
            PARTITION BY toYear(insertion_date)
            ORDER BY insertion_date
        """
        self.assertEqual(query.format(query.check_valid_write_query(q)), query.format(q))

    def test_create_table_with_index(self):
        q = """
        CREATE TABLE table_name
        (
            u64 UInt64,
            i32 Int32,
            s String,
            INDEX a (u64 * i32, s) TYPE minmax333 GRANULARITY 3,
            INDEX b (u64 * length(s)) TYPE set(1000) GRANULARITY 4
        ) ENGINE = MergeTree()
        """
        self.assertEqual(query.format(query.check_valid_write_query(q)), query.format(q))

    def test_create_table_with_subqueries_in_alias_definition__is_ok(self):
        q = """
            CREATE TABLE visits4
            (
                `event_time` DateTime,
                `query` String,
                `three` String ALIAS event_time IN (SELECT event_time FROM visits)
            )
            ENGINE = MergeTree
            PARTITION BY toYYYYMM(event_time)
            ORDER BY event_time
        """
        self.assertEqual(query.format(query.check_valid_write_query(q)), query.format(q))

    # Since we are not using them and we would need to parse and secure them, disable constraints for now (2022-02)
    def test_create_table_with_constraints_is_forbidden(self):
        with self.assertRaisesRegex(ValueError, "CREATE TABLE with constraints is unsupported"):
            query.check_valid_write_query("""
                CREATE TABLE visits5
                (
                    `event_time` DateTime,
                    `query` String,
                    `three` String,
                    CONSTRAINT constraint_name_1 CHECK (event_time IN (SELECT event_time FROM visits))
                )
                ENGINE = MergeTree
                PARTITION BY toYYYYMM(event_time)
                ORDER BY event_time
            """)

    def test_create_table_with_primary_key_with_subquery(self):
        with self.assertRaisesRegex(ValueError, "CREATE TABLE: Unsupported subquery: in PRIMARY KEY declaration"):
            query.check_valid_write_query("""
                CREATE TABLE visits6
                (
                    `event_time` DateTime,
                    `query` String,
                    `three` String
                )
                ENGINE = MergeTree
                PARTITION BY toYYYYMM(event_time)
                PRIMARY KEY (event_time, (event_time IN (SELECT event_time FROM visits)))
            """)

        with self.assertRaisesRegex(ValueError, "CREATE TABLE: Unsupported subquery: in PRIMARY KEY declaration"):
            query.check_valid_write_query("""
                CREATE TABLE visits6
                (
                    `event_time` DateTime,
                    `query` String,
                    `three` String,
                    PRIMARY KEY (event_time, (event_time IN (SELECT event_time FROM visits)))
                )
                ENGINE = MergeTree
                PARTITION BY toYYYYMM(event_time)
            """)

    def test_create_table_with_projections_is_supported(self):
        q = '''
            CREATE TABLE default.github_events
            (
                `id` UInt32,
                `type` LowCardinality(String),
                `date` DateTime,
                `username` String,
                `repository` String,
                PROJECTION projection_user_sort
                (
                    SELECT *
                    ORDER BY username
                )
            )
            ENGINE = MergeTree
            PARTITION BY toYYYYMMDD(date)
            ORDER BY repository'''
        self.assertEqual(query.format(query.check_valid_write_query(q)), query.format(q))

    def test_create_table_with_projections_invalid_syntax(self):
        with self.assertRaisesRegex(ValueError, "Syntax error: failed at position"):
            query.check_valid_write_query("""
                CREATE TABLE default.github_events
                (
                    `id` UInt32,
                    PROJECTION projection_user_sort
                        (
                            SELECT * FROM other_table
                            ORDER BY username
                        )
                )
                ENGINE = MergeTree
                ORDER BY id
            """)

    def test_create_projection_with_forbidden_function(self):
        with self.assertRaisesRegex(ValueError, "Usage of function sleepEachRow is restricted"):
            query.check_valid_write_query("""
                CREATE TABLE github_events
                (
                    `id` UInt32,
                    PROJECTION projection_user_sort
                        (
                            SELECT *, sleepEachRow(0.1)
                            ORDER BY id
                        )
                )
                ENGINE = MergeTree
                ORDER BY id
            """)

    def test_create_table_with_join_engine_is_forbidden(self):
        with self.assertRaisesRegex(ValueError, "Creation of tables with ENGINE Join is not supported"):
            query.check_valid_write_query("""
                CREATE TABLE join_table
                (
                    `id` UInt32,
                    `val` String
                )
                ENGINE = Join(ANY, LEFT, id)
            """)

    def test_create_table_as_query_is_forbidden(self):
        with self.assertRaisesRegex(ValueError, "CREATE TABLE: Unsupported CREATE AS query"):
            query.check_valid_write_query("""
                CREATE TABLE visits2
                (
                    `event_time` DateTime,
                    `query` String
                )
                ENGINE = MergeTree
                PARTITION BY toYYYYMM(event_time)
                ORDER BY event_time AS
                SELECT
                    event_time,
                    query
                FROM system.query_log
                WHERE event_time > (now() - toIntervalMinute(1))
            """)

    def test_create_table_with_valid_settings_is_ok(self):
        q = 'CREATE TABLE big_table (number Int64) ENGINE = MergeTree Order by tuple() Settings index_granularity = 8192'
        self.assertEqual(query.format(query.check_valid_write_query(q)), query.format(q))

    def test_create_table_with_invalid_settings_is_forbidden(self):
        q = 'CREATE TABLE big_table (number Int64) ENGINE = MergeTree Order by tuple() ' \
            'SETTINGS disk = disk(type = local, path = \'/var/lib/clickhouse/disks/local/\')'
        with self.assertRaisesRegex(ValueError, "Usage of setting 'disk' is restricted"):
            query.check_valid_write_query(q)

    def test_create_table_with_mixed_settings_is_forbidden(self):
        q = 'CREATE TABLE big_table (number Int64) ENGINE = MergeTree Order by tuple() ' \
            'SETTINGS disk = disk(type = local, path = \'/var/lib/clickhouse/disks/local/\'), index_granularity = 8192'
        with self.assertRaisesRegex(ValueError, "Usage of setting 'disk' is restricted"):
            query.check_valid_write_query(q)

        q = 'CREATE TABLE big_table (number Int64) ENGINE = MergeTree Order by tuple() ' \
            'SETTINGS index_granularity = 8192, disk = disk(type = local, path = \'/var/lib/clickhouse/disks/local/\')'
        with self.assertRaisesRegex(ValueError, "Usage of setting 'disk' is restricted"):
            query.check_valid_write_query(q)

    def test_create_table_with_invalid_settings_can_be_cleaned(self):
        q = 'CREATE TABLE big_table (number Int64) ENGINE = MergeTree Order by tuple() ' \
            'SETTINGS disk = disk(type = local, path = \'/var/lib/clickhouse/disks/local/\')'

        expected = "CREATE TABLE big_table (number Int64) ENGINE = MergeTree Order by tuple()"
        result = query.check_valid_write_query(q, clean_table_settings=1)
        self.assertEqual(query.format(result), query.format(expected))

    def test_create_table_with_mixed_settings_can_be_cleaned(self):
        q = 'CREATE TABLE big_table (number Int64) ENGINE = MergeTree Order by tuple() ' \
            'SETTINGS disk = disk(type = local, path = \'/var/lib/clickhouse/disks/local/\'), index_granularity = 8192'

        expected = "CREATE TABLE big_table (number Int64) ENGINE = MergeTree Order by tuple() SETTINGS index_granularity = 8192"
        result = query.check_valid_write_query(q, clean_table_settings=1)
        self.assertEqual(query.format(result), query.format(expected))

        q = 'CREATE TABLE big_table (number Int64) ENGINE = MergeTree Order by tuple() ' \
            'SETTINGS index_granularity = 8192, disk = disk(type = local, path = \'/var/lib/clickhouse/disks/local/\')'

        expected = "CREATE TABLE big_table (number Int64) ENGINE = MergeTree Order by tuple() SETTINGS index_granularity = 8192"
        result = query.check_valid_write_query(q, clean_table_settings=1)
        self.assertEqual(query.format(result), query.format(expected))

    def test_create_table_with_invalid_setting_can_be_allowed(self):
        q = 'CREATE TABLE big_table (number Int64) ENGINE = MergeTree Order by tuple() ' \
            'SETTINGS disk = disk(type = local, path = \'/var/lib/clickhouse/disks/local/\')'

        self.assertEqual(query.format(query.check_valid_write_query(q, validate_table_settings=False)), query.format(q))
        self.assertEqual(query.format(query.check_valid_write_query(q, table_settings_allow_list=["disk"])), query.format(q))

    def test_create_table_with_valid_setting_can_be_disallowed(self):
        q = 'CREATE TABLE big_table (number Int64) ENGINE = MergeTree Order by tuple() Settings index_granularity = 8192'

        with self.assertRaisesRegex(ValueError, "Usage of setting 'index_granularity' is restricted"):
            query.check_valid_write_query(q, table_settings_deny_list=["index_granularity"])

    def test_create_table_with_valid_setting_can_be_cleaned(self):
        q = 'CREATE TABLE big_table (number Int64) ENGINE = MergeTree Order by tuple() Settings index_granularity = 8192'

        expected = "CREATE TABLE big_table (number Int64) ENGINE = MergeTree Order by tuple()"
        self.assertEqual(query.format(query.check_valid_write_query(q, clean_table_settings=True, table_settings_deny_list=["index_granularity"])),
                         query.format(expected))

    def test_create_table_with_valid_setting_but_invalid_value(self):
        q = 'CREATE TABLE big_table (number Int64) ENGINE = MergeTree Order by tuple() SETTINGS index_granularity = 0'
        with self.assertRaisesRegex(ValueError, "The value for 'index_granularity' is too small (.*). Contact .*"):
            query.check_valid_write_query(q)

        q = 'CREATE TABLE big_table (number Int64) ENGINE = MergeTree Order by tuple() SETTINGS index_granularity = 0, index_granularity = 12'
        with self.assertRaisesRegex(ValueError, "Setting 'index_granularity' is declared more than once. Contact"):
            query.check_valid_write_query(q)

        q = "CREATE TABLE big_table (number Int64) ENGINE = MergeTree Order by tuple() " \
            "SETTINGS index_granularity = 'tinybird_is_great'"
        with self.assertRaisesRegex(ValueError, "Cannot parse input: expected 'eof' before: 'tinybird_is_great'"):
            query.check_valid_write_query(q)

    def test_create_table_with_valid_setting_but_invalid_value_can_be_cleaned(self):
        q = 'CREATE TABLE big_table (number Int64) ENGINE = MergeTree Order by tuple() ' \
            'SETTINGS index_granularity = 0'

        expected = "CREATE TABLE big_table (number Int64) ENGINE = MergeTree Order by tuple()"
        result = query.check_valid_write_query(q, clean_table_settings=True)
        self.assertEqual(query.format(result), query.format(expected))

    def test_create_table_with_valid_setting_throws_with_duplicates(self):
        q = 'CREATE TABLE big_table (number Int64) ENGINE = MergeTree Order by tuple() ' \
            'SETTINGS index_granularity = 64, index_granularity = 512'

        with self.assertRaisesRegex(ValueError, "Setting 'index_granularity' is declared more than once. Contact"):
            query.check_valid_write_query(q)

    def test_merge_with_ttl_timeout_good(self):
        q = 'CREATE TABLE big_table (number Int64) ENGINE = MergeTree Order by tuple() ' \
            'SETTINGS merge_with_ttl_timeout = 1200, ttl_only_drop_parts = 1'

        result = query.check_valid_write_query(q)
        self.assertEqual(query.format(result), query.format(q))

    def test_merge_with_ttl_timeout_no_drop_parts(self):
        q = 'CREATE TABLE big_table (number Int64) ENGINE = MergeTree Order by tuple() ' \
            "SETTINGS merge_with_ttl_timeout = 1200, ttl_only_drop_parts = 0"

        error = "The value for 'merge_with_ttl_timeout' can only be reduced if 'ttl_only_drop_parts' is active. Contact.*"
        with self.assertRaisesRegex(ValueError, error):
            query.check_valid_write_query(q)

        q = 'CREATE TABLE big_table (number Int64) ENGINE = MergeTree Order by tuple() ' \
            "SETTINGS merge_with_ttl_timeout = 1200"
        with self.assertRaisesRegex(ValueError, error):
            query.check_valid_write_query(q)

        result = query.check_valid_write_query(q, clean_table_settings=True)
        expected = 'CREATE TABLE big_table (number Int64) ENGINE = MergeTree Order by tuple()'
        self.assertEqual(query.format(result), query.format(expected))

        q = 'CREATE TABLE big_table (number Int64) ENGINE = MergeTree Order by tuple() ' \
            "SETTINGS merge_with_ttl_timeout = 1200, ttl_only_drop_parts = 1"
        expected = 'CREATE TABLE big_table (number Int64) ENGINE = MergeTree Order by tuple() ' \
                   "SETTINGS merge_with_ttl_timeout = 1200, ttl_only_drop_parts = 1"
        result = query.check_valid_write_query(q)
        self.assertEqual(query.format(result), query.format(expected))

        # Raising it is ok
        q = 'CREATE TABLE big_table (number Int64) ENGINE = MergeTree Order by tuple() ' \
            'SETTINGS merge_with_ttl_timeout = 43200'

        result = query.check_valid_write_query(q)
        self.assertEqual(query.format(result), query.format(q))

    def test_wide_part(self):
        q = 'CREATE TABLE big_table (number Int64) ENGINE = MergeTree Order by tuple() Settings min_bytes_for_wide_part = 0'
        self.assertEqual(query.format(query.check_valid_write_query(q)), query.format(q))

        q = 'CREATE TABLE big_table (number Int64) ENGINE = MergeTree Order by tuple() Settings min_rows_for_wide_part = 0'
        self.assertEqual(query.format(query.check_valid_write_query(q)), query.format(q))

        q = 'CREATE TABLE big_table (number Int64) ENGINE = MergeTree Order by tuple() Settings min_rows_for_wide_part = 0, min_bytes_for_wide_part = 0'
        self.assertEqual(query.format(query.check_valid_write_query(q)), query.format(q))

        with self.assertRaisesRegex(ValueError, "Cannot parse input: expected 'eof' before: 'aaaa'"):
            q = "CREATE TABLE big_table (number Int64) ENGINE = MergeTree Order by tuple() Settings min_bytes_for_wide_part = 'aaaa'"
            query.check_valid_write_query(q)
