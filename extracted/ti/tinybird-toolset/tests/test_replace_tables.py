import unittest
from chtoolset import query as chquery

import logging

logging.basicConfig(level=logging.DEBUG)


class TestReplaceTables(unittest.TestCase):
    scenarios = [
        (
            "select * from tt",
            {("", "tt"): ("", "table2")},
            "select * from table2 as tt",
        ),
        (
            "select * from tt",
            {("", "tt"): ("", "(select a from table2 where a > 1)")},
            "select * from (select a from table2 where a > 1) AS tt",
        ),
        (
            "select tt.a from tt",
            {("", "tt"): ("", "(select a from table2 where a > 1)")},
            "select tt.a from (select a from table2 where a > 1) AS tt",
        ),
        (
            "select aa.a from tt AS aa",
            {("", "tt"): ("", "(select a from table2 where a > 1)")},
            "select aa.a from (select a from table2 where a > 1) AS aa",
        ),
        (
            "select * from database.tt",
            {("database", "tt"): ("", "(select a from table2 where a > 1)")},
            "select * from (select a from table2 where a > 1) AS tt",
        ),
        (
            "select * from database.`tt`",
            {("database", "tt"): ("", "(select a from table2 where a > 1)")},
            "select * from (select a from table2 where a > 1) AS tt",
        ),
        (
            "select * from `database`.`tt`",
            {("database", "tt"): ("", "(select a from table2 where a > 1)")},
            "select * from (select a from table2 where a > 1) AS tt",
        ),
        (
            "select * from tt inner join ttj using b",
            {("", "tt"): ("", "tt2"), ("", "ttj"): ("", "ttj2")},
            "select * from tt2 as tt inner join ttj2 as ttj using b",
        ),
        (
            "select * from tt inner join tt using b",
            {("", "tt"): ("", "tt2")},
            "select * from tt2 as tt inner join tt2 as tt using b",
        ),
        (
            "select count() c from test_table format JSON",
            {("", "test_table"): ("", "pepe")},
            "select count() c from pepe as test_table format JSON",
        ),
        (
            "select * from tt",
            {("", "tt"): ("d_012345", "table2")},
            "select * from d_012345.table2 as tt",
        ),
        (
            "select count() as t, t.record, avg(landing.timestamp) from landing t group by t.record",
            {("", "landing"): ("database", "t_01010101")},
            "select count() as t, t.record, avg(t_01010101.timestamp) from database.t_01010101 t group by t.record",
        ),
        (
            "select * from test",
            {
                ("", "test"): ("", "testing"),
            },
            "select * from testing as test",
        ),
        (
            "select * from test",
            {
                ("", "test"): ("", "(select * from testing)"),
            },
            "select * from (select * from testing) as test",
        ),
        (
            "SELECT finalizeAggregation(( SELECT countState(id) FROM join_test ))",
            {("", "join_test"): ("database", "t_01010101")},
            "SELECT finalizeAggregation(( SELECT countState(id) FROM database.t_01010101 as join_test ))",
        ),
        (
            "SELECT arrayMap(x -> finalizeAggregation(x), state) FROM (SELECT sumStateResample(0, 20, 1)(id, id % 20) as state FROM default.join_test)",
            {("default", "join_test"): ("database", "t_01010101")},
            "SELECT arrayMap(x -> finalizeAggregation(x), state) FROM (SELECT sumStateResample(0, 20, 1)(id, id % 20) as state FROM database.t_01010101 as join_test)",
        ),
        (
            "SELECT * FROM t WHERE (c1, c2) IN t2",
            {
                ("", "t"): ("database", "t_01010101"),
                ("", "t2"): ("database", "t_02020202"),
            },
            "SELECT * FROM database.t_01010101 AS t WHERE (c1, c2) IN database.t_02020202",
        ),
    ]

    def test_asterisks_no_database(self):
        sql = "select tt.* from tt"

        replacements = {("", "tt"): ("", "t2")}
        expected = "select t2.* from t2 as tt"
        self.assertEqual(
            chquery.replace_tables(sql, replacements), chquery.format(expected)
        )

        replacements = {("", "tt"): ("", "(Select * FROM t2)")}
        expected = "select tt.* FROM (Select * FROM t2) as tt"
        self.assertEqual(
            chquery.replace_tables(sql, replacements), chquery.format(expected)
        )

    def test_asterisk_with_transformers_no_database(self):
        sql = "SELECT tt.* EXCEPT a FROM tt"
        replacements = {("", "tt"): ("", "t2")}
        expected = "select t2.* EXCEPT a FROM t2 as tt"
        self.assertEqual(
            chquery.replace_tables(sql, replacements), chquery.format(expected)
        )

        replacements = {("", "tt"): ("", "(Select * FROM t2)")}
        expected = "select tt.* EXCEPT a FROM (Select * FROM t2) as tt"
        self.assertEqual(
            chquery.replace_tables(sql, replacements), chquery.format(expected)
        )

    def test_asterisks_with_database(self):
        sql = "select db.tt.* from tt"

        replacements = {("db", "tt"): ("db", "t2")}
        expected = "select db.t2.* from db.t2 as tt"
        self.assertEqual(
            chquery.replace_tables(sql, replacements, default_database="db"),
            chquery.format(expected),
        )

        replacements = {("db", "tt"): ("", "(Select * FROM t2)")}
        expected = "select tt.* FROM (Select * FROM t2) as tt"
        self.assertEqual(
            chquery.replace_tables(sql, replacements, default_database="db"),
            chquery.format(expected),
        )

    def test_asterisks_with_transformers_with_database(self):
        sql = "select db.tt.* EXCEPT a from tt"

        replacements = {("db", "tt"): ("db", "t2")}
        expected = "select db.t2.* EXCEPT a from db.t2 as tt"
        self.assertEqual(
            chquery.replace_tables(sql, replacements, default_database="db"),
            chquery.format(expected),
        )

        replacements = {("db", "tt"): ("", "(Select * FROM t2)")}
        expected = "select tt.* EXCEPT a FROM (Select * FROM t2) as tt"
        self.assertEqual(
            chquery.replace_tables(sql, replacements, default_database="db"),
            chquery.format(expected),
        )

    def test_replace(self):
        for sql, replacements, expected_query in self.scenarios:
            with self.subTest(sql=sql):
                self.assertEqual(
                    chquery.replace_tables(sql, replacements),
                    chquery.format(expected_query),
                )

    def test_replace_one_line(self):
        for sql, replacements, expected_query in self.scenarios:
            with self.subTest(sql=sql):
                self.assertEqual(
                    chquery.replace_tables(sql, replacements, one_line=True),
                    chquery.format(expected_query, one_line=True),
                )

    def test_alias(self):
        sql = """
        SELECT toStartOfFiveMinute(s.dt), c.name, s.product
        FROM sales s
        ANY INNER JOIN clients c
        ON c.client_id = s.client_id
        WHERE s.product = 'WADUS'
        """
        replacements = {
            ("", "clients"): ("", "(select * from clients where country = 'ES')"),
        }

        expected_query = """
        SELECT toStartOfFiveMinute(s.dt), c.name, s.product
        FROM sales s
        ANY INNER JOIN (select * from clients where country = 'ES') c
        ON c.client_id = s.client_id
        WHERE s.product = 'WADUS'
        """

        replaced = chquery.replace_tables(sql, replacements)
        self.assertEqual(replaced, chquery.format(expected_query))

    def test_alias_is_used_when_the_table_name_is_changed(self):
        sql = """
        SELECT toStartOfFiveMinute(s.dt), clients.name, s.product
        FROM sales s
        ANY INNER JOIN clients c
        ON clients.client_id = s.client_id
        WHERE s.product = 'WADUS'
        """
        replacements = {
            ("", "clients"): ("", "(select * from clients where country = 'ES')"),
        }

        # Note that the query replaces clients with c for all columns
        expected_query = """
        SELECT toStartOfFiveMinute(s.dt), c.name, s.product
        FROM sales s
        ANY INNER JOIN (select * from clients where country = 'ES') c
        ON c.client_id = s.client_id
        WHERE s.product = 'WADUS'
        """

        replaced = chquery.replace_tables(sql, replacements)
        self.assertEqual(replaced, chquery.format(expected_query))

    def test_alias_across_joins_works_fine(self):
        sql = """
            SELECT *
                FROM
                (
                    SELECT 1
                    FROM numbers(10) AS t_6c64478e93d244e3ada26aff731e9e8c
                ) AS a,
                (
                    SELECT *
                    FROM t_6c64478e93d244e3ada26aff731e9e8c
                    LIMIT 10
                )
        """

        replacements = {
            ("", "t_6c64478e93d244e3ada26aff731e9e8c"): ("", "internal_table"),
        }

        expected_query = """
            SELECT *
                FROM
                (
                    SELECT 1
                    FROM numbers(10) AS t_6c64478e93d244e3ada26aff731e9e8c
                ) AS a,
                (
                    SELECT *
                    FROM internal_table as t_6c64478e93d244e3ada26aff731e9e8c
                    LIMIT 10
                )
        """

        replaced = chquery.replace_tables(sql, replacements)
        self.assertEqual(replaced, chquery.format(expected_query))

    def test_alias_across_union_all_with_no_database(self):
        sql = """
                SELECT t2.*
                FROM
                (
                    SELECT * FROM t1 as t2
                    UNION ALL
                    SELECT * FROM t2
                ) t2
            """

        replacements = {
            ("db", "t1"): ("d_0101", "t_000001"),
            ("db", "t2"): ("d_0101", "t_000002"),
        }

        expected_query = """
                SELECT t2.*
                FROM
                (
                    SELECT * FROM d_0101.t_000001 as t2
                    UNION ALL
                    SELECT * FROM d_0101.t_000002 as t2
                ) t2
            """

        replaced = chquery.replace_tables(sql, replacements, default_database="db")
        self.assertEqual(replaced, chquery.format(expected_query))

    def test_alias_across_subqueries_with_inner_cte(self):
        sql = """
        SELECT
            *
        FROM
        (
            SELECT * FROM ( WITH t1 AS (SELECT * FROM table) SELECT * FROM t1)
            UNION ALL
            SELECT * FROM t1
        )
        """

        replacements = {
            ("db", "table"): ("d_0101", "t_000001"),
            ("db", "t1"): ("d_0101", "t_000002"),
        }

        expected_query = """
        SELECT
            *
        FROM
        (
            SELECT * FROM ( WITH t1 AS (SELECT * FROM d_0101.t_000001 AS table) SELECT * FROM t1)
            UNION ALL
            SELECT * FROM d_0101.t_000002 AS t1
        )
        """

        replaced = chquery.replace_tables(sql, replacements, default_database="db")
        self.assertEqual(replaced, chquery.format(expected_query))

    def test_other_database(self):
        sql = "select * from nyc_taxi"
        replacements = {("", "nyc_taxi"): ("", "(select * from public.nyc_taxi)")}

        expected_query = "select * from (select * from public.nyc_taxi) as nyc_taxi"

        replaced = chquery.replace_tables(sql, replacements)
        self.assertEqual(replaced, chquery.format(expected_query))

    def test_other_database_with_tuple(self):
        sql = "select * from nyc_taxi"
        replacements = {("", "nyc_taxi"): ("public", "nyc_taxi")}

        expected_query = "select * from public.nyc_taxi"

        replaced = chquery.replace_tables(sql, replacements)
        self.assertEqual(replaced, chquery.format(expected_query))

    def test_qualified_column_in_where(self):
        sql = """
            SELECT
                parent_partnumber,
                groupUniqArray(partnumber) partnumber
            FROM articles
            WHERE length(articles.partnumber) == 17
            GROUP BY parent_partnumber
        """

        replacements = {("d_012345", "articles"): ("d_012345", "t_id_abcd")}

        expected_query = """
            SELECT
                parent_partnumber,
                groupUniqArray(partnumber) partnumber
            FROM d_012345.t_id_abcd as articles
            WHERE length(t_id_abcd.partnumber) == 17
            GROUP BY parent_partnumber
        """

        replaced = chquery.replace_tables(
            sql, replacements, default_database="d_012345"
        )
        self.assertEqual(replaced, chquery.format(expected_query))

    def test_shared_ds_with_db_column(self):
        sql = """SELECT shared_ws.join_test.id FROM shared_ws.join_test"""
        replacements = {("shared_ws", "join_test"): ("d_01010101", "t_01010101")}
        expected_query = """SELECT d_01010101.t_01010101.id FROM d_01010101.t_01010101 as join_test"""

        replaced = chquery.replace_tables(
            sql, replacements, default_database="d_00000000"
        )  # Different from shared_ws
        self.assertEqual(replaced, chquery.format(expected_query))

    def test_shared_ds_without_db_column(self):
        sql = """SELECT join_test.id FROM shared_ws.join_test"""
        replacements = {("shared_ws", "join_test"): ("d_01010101", "t_01010101")}
        expected_query = (
            """SELECT t_01010101.id FROM d_01010101.t_01010101 as join_test"""
        )

        replaced = chquery.replace_tables(
            sql, replacements, default_database="d_00000000"
        )  # Different from shared_ws
        self.assertEqual(replaced, chquery.format(expected_query))

    # https://gitlab.com/tinybird/analytics/-/issues/492#note_871953336
    def test_shared_ds_without_db_column_2(self):
        sql = """
                SELECT
                    count() requests,
                    countIf(datasources_ops_log.result != 'ok' or error is not null) errors
                FROM tinybird.datasources_ops_log
                WHERE
                    timestamp > now() - interval 10 minute AND (error is null )
            """

        replacements = {
            ("tinybird", "datasources_ops_log"): (
                "public",
                "t_be0776b9841e4428a9857b33d06cabdc",
            )
        }
        replaced = chquery.replace_tables(
            sql, replacements, default_database="d_userdatabase"
        )
        expected_query = """
                SELECT
                count() requests,
                countIf(t_be0776b9841e4428a9857b33d06cabdc.result != 'ok' or error is not null) errors
            FROM public.t_be0776b9841e4428a9857b33d06cabdc as datasources_ops_log
            WHERE
            timestamp > now() - interval 10 minute AND (error is null )
        """
        self.assertEqual(replaced, chquery.format(expected_query))

    def test_column_uses_alias_source_different_from_from(self):
        """When the same target table has multiple source keys registered
        (e.g., workspace name and CH database name both pointing to the same
        physical table), a column qualified with one alias must still be
        rewritten even if the FROM matched a different alias key."""
        sql = "SELECT acme.events.id FROM events"
        replacements = {
            ("d_userdb", "events"): ("d_userdb", "t_xxx"),
            ("acme", "events"): ("d_userdb", "t_xxx"),
        }
        expected_query = "SELECT d_userdb.t_xxx.id FROM d_userdb.t_xxx AS events"
        replaced = chquery.replace_tables(
            sql, replacements, default_database="d_userdb"
        )
        self.assertEqual(replaced, chquery.format(expected_query))

    def test_self_join_with_subquery_target(self):
        """Self-join of a datasource that is replaced by a subquery. Each FROM
        leg gets its own cloned subquery and its own SQL alias; columns
        qualified by the SQL alias must keep their per-leg binding."""
        sql = """
            SELECT prev.value, curr.value
            FROM workspace_name.events AS prev
            JOIN workspace_name.events AS curr ON curr.id = prev.id + 1
        """
        replacements = {
            ("workspace_name", "events"): ("", "(SELECT * FROM raw_events)"),
            ("d_yyy", "events"): ("", "(SELECT * FROM raw_events)"),
        }
        expected_query = """
            SELECT prev.value, curr.value
            FROM (SELECT * FROM raw_events) AS prev
            INNER JOIN (SELECT * FROM raw_events) AS curr ON curr.id = (prev.id + 1)
        """
        replaced = chquery.replace_tables(
            sql, replacements, default_database="d_yyy"
        )
        self.assertEqual(replaced, chquery.format(expected_query))

    def test_qualified_asterisk_uses_alias_source_different_from_from(self):
        """Same as above but for qualified asterisks: SELECT acme.events.*"""
        sql = "SELECT acme.events.* FROM events"
        replacements = {
            ("d_userdb", "events"): ("d_userdb", "t_xxx"),
            ("acme", "events"): ("d_userdb", "t_xxx"),
        }
        expected_query = "SELECT d_userdb.t_xxx.* FROM d_userdb.t_xxx AS events"
        replaced = chquery.replace_tables(
            sql, replacements, default_database="d_userdb"
        )
        self.assertEqual(replaced, chquery.format(expected_query))

    def test_qualified_column_in_array(self):
        sql = """SELECT array(join_test.id) FROM default.join_test"""

        replacements = {("default", "join_test"): ("database", "t_01010101")}

        expected_query = (
            """SELECT array(t_01010101.id) FROM database.t_01010101 as join_test"""
        )

        replaced = chquery.replace_tables(sql, replacements, default_database="default")
        self.assertEqual(replaced, chquery.format(expected_query))

    def test_qualified_column_in_tuple(self):
        sql = """SELECT tuple(join_test.id, 0) FROM default.join_test"""

        replacements = {("default", "join_test"): ("database", "t_01010101")}

        expected_query = (
            """SELECT tuple(t_01010101.id, 0) FROM database.t_01010101 as join_test"""
        )

        replaced = chquery.replace_tables(sql, replacements, default_database="default")
        self.assertEqual(replaced, chquery.format(expected_query))

    def test_qualified_column_in_type_conversion(self):
        sql = """SELECT toNullable(join_test.id) FROM default.join_test"""
        replacements = {("default", "join_test"): ("database", "t_01010101")}
        expected_query = (
            """SELECT toNullable(t_01010101.id) FROM database.t_01010101 as join_test"""
        )
        replaced = chquery.replace_tables(sql, replacements, default_database="default")
        self.assertEqual(replaced, chquery.format(expected_query))

        sql = """SELECT toInt8(join_test.id) FROM default.join_test"""
        replacements = {("default", "join_test"): ("database", "t_01010101")}
        expected_query = (
            """SELECT toInt8(t_01010101.id) FROM database.t_01010101 as join_test"""
        )
        replaced = chquery.replace_tables(sql, replacements, default_database="default")
        self.assertEqual(replaced, chquery.format(expected_query))

        sql = """SELECT parseDateTimeBestEffortUSOrNull(join_test.id) FROM default.join_test"""
        replacements = {("default", "join_test"): ("database", "t_01010101")}
        expected_query = """SELECT parseDateTimeBestEffortUSOrNull(t_01010101.id) FROM database.t_01010101 as join_test"""
        replaced = chquery.replace_tables(sql, replacements, default_database="default")
        self.assertEqual(replaced, chquery.format(expected_query))

    def test_qualified_column_in_where_with_subquery(self):
        sql = """
            SELECT
                parent_partnumber,
                groupUniqArray(partnumber) partnumber
            FROM articles
            WHERE length(articles.partnumber) == 17
            GROUP BY parent_partnumber
        """

        replacements = {
            ("d_012345", "articles"): (
                "d_012345",
                "(select * from d_012345.t_id_abcd LIMIT 1)",
            )
        }

        expected_query = """
            SELECT
                parent_partnumber,
                groupUniqArray(partnumber) partnumber
            FROM (select * from d_012345.t_id_abcd LIMIT 1) as articles
            WHERE length(articles.partnumber) == 17
            GROUP BY parent_partnumber
        """

        replaced = chquery.replace_tables(
            sql, replacements, default_database="d_012345"
        )
        self.assertEqual(replaced, chquery.format(expected_query))

    def test_qualified_column_with_alias_in_where_with_subquery(self):
        sql = """
            SELECT
                parent_partnumber,
                groupUniqArray(partnumber) partnumber
            FROM articles as alias
            WHERE length(articles.partnumber) == 17
            GROUP BY parent_partnumber
        """

        replacements = {
            ("d_012345", "articles"): (
                "d_012345",
                "(select * from d_012345.t_id_abcd LIMIT 1)",
            )
        }

        expected_query = """
            SELECT
                parent_partnumber,
                groupUniqArray(partnumber) partnumber
            FROM (select * from d_012345.t_id_abcd LIMIT 1) as alias
            WHERE length(alias.partnumber) == 17
            GROUP BY parent_partnumber
        """

        replaced = chquery.replace_tables(
            sql, replacements, default_database="d_012345"
        )
        self.assertEqual(replaced, chquery.format(expected_query))

    def test_aliases_cross_join(self):
        sql = """
            select c1.a, c2.a, c1.a/c2.a
            from currencies as c1
            cross join currencies as c2
        """

        replacements = {("d_012345", "currencies"): ("d_012345", "t_wadus")}

        expected_query = """
            select c1.a, c2.a, c1.a/c2.a
            from d_012345.t_wadus as c1
            cross join d_012345.t_wadus as c2
        """

        replaced = chquery.replace_tables(
            sql, replacements, default_database="d_012345"
        )
        self.assertEqual(replaced, chquery.format(expected_query))

    def test_qualified_column_in_order_by(self):
        """Test that ORDER BY columns are properly replaced when tables are replaced"""
        sql = """
        SELECT db.my_table.id, count()
        FROM db.my_table
        WHERE db.my_table.id = 1
        GROUP BY db.my_table.id
        ORDER BY db.my_table.id
        """

        replacements = {("db", "my_table"): ("d_012345", "t_67890")}

        expected_query = """
        SELECT d_012345.t_67890.id, count()
        FROM d_012345.t_67890 as my_table
        WHERE d_012345.t_67890.id = 1
        GROUP BY d_012345.t_67890.id
        ORDER BY d_012345.t_67890.id ASC
        """

        replaced = chquery.replace_tables(sql, replacements)
        self.assertEqual(replaced, chquery.format(expected_query))

    # https://gitlab.com/tinybird/analytics/-/issues/823
    def test_with_fill(self):
        sql = """
        SELECT
            toDate(now()) - toIntervalDay(number) AS n,
            'original' AS source
        FROM table
        WHERE (number % 2) = 0
        ORDER BY n ASC WITH FILL FROM toDate(now()) - toIntervalDay(10) TO toDate(now()) STEP 1
        """

        replacements = {("d_012345", "table"): ("d_012345", "replaced_table")}

        expected_query = """
        SELECT
            toDate(now()) - toIntervalDay(number) AS n,
            'original' AS source
        FROM d_012345.replaced_table as table
        WHERE (number % 2) = 0
        ORDER BY n ASC WITH FILL FROM toDate(now()) - toIntervalDay(10) TO toDate(now()) STEP 1
        """

        replaced = chquery.replace_tables(
            sql, replacements, default_database="d_012345"
        )
        self.assertEqual(replaced, chquery.format(expected_query))

    def test_describe_table(self):
        sql = """
            DESCRIBE TABLE d_012345.currencies
        """
        replacements = {("d_012345", "currencies"): ("d_012345", "t_wadus")}
        expected_query = """
            DESCRIBE TABLE d_012345.t_wadus as currencies
        """
        replaced = chquery.replace_tables(
            sql, replacements, default_database="d_012345"
        )
        self.assertEqual(replaced, chquery.format(expected_query))

        sql = """
            DESCRIBE TABLE currencies
        """
        replacements = {("d_012345", "currencies"): ("d_012345", "t_wadus")}
        expected_query = """
            DESCRIBE TABLE d_012345.t_wadus as currencies
        """
        replaced = chquery.replace_tables(
            sql, replacements, default_database="d_012345"
        )
        self.assertEqual(replaced, chquery.format(expected_query))

    def test_describe_query(self):
        sql = """
            DESCRIBE TABLE ((SELECT table.col FROM table))
        """
        replacements = {("default", "table"): ("d_012345", "t_wadus")}
        expected_query = """
            DESCRIBE TABLE ((SELECT t_wadus.col FROM d_012345.t_wadus as table))
        """
        replaced = chquery.replace_tables(sql, replacements, default_database="default")
        self.assertEqual(replaced, chquery.format(expected_query))

    def test_replace_of_table_function_throws(self):
        sql = "SELECT * FROM numbers(10)"
        replacement = {("", "", "numbers"): ("", "", "one")}
        with self.assertRaisesRegex(
            ValueError,
            "Key replacement must be a tuple containing database and table name",
        ):
            chquery.replace_tables(sql, replacement, default_database="d_012345")

    def test_replace_with_3_element_tuple(self):
        sql = "SELECT * FROM db.table"
        replacement = {("db", "table", ""): ("db2", "table", "")}
        replaced = chquery.replace_tables(sql, replacement, default_database="d_012345")
        self.assertEqual(replaced, chquery.format("SELECT * FROM db2.table"))

        replacement = {("db", "table"): ("db2", "table", "")}
        replaced = chquery.replace_tables(sql, replacement, default_database="d_012345")
        self.assertEqual(replaced, chquery.format("SELECT * FROM db2.table"))

        replacement = {("db", "table", ""): ("db2", "table")}
        replaced = chquery.replace_tables(sql, replacement, default_database="d_012345")
        self.assertEqual(replaced, chquery.format("SELECT * FROM db2.table"))

    def test_replace_of_table_function_by_table_name(self):
        sql = "SELECT * FROM numbers(10)"
        replacement = {("", "numbers"): ("", "one")}
        replaced = chquery.replace_tables(sql, replacement)
        self.assertEqual(replaced, chquery.format(sql))

        sql = "SELECT * FROM numbers, numbers(10)"
        replacement = {("", "numbers"): ("", "numbers2")}
        replaced = chquery.replace_tables(sql, replacement)
        self.assertEqual(
            replaced, chquery.format("SELECT * FROM numbers2 as numbers, numbers(10)")
        )

        sql = "SELECT * FROM numbers, numbers(10)"
        replacement = {("", "numbers", ""): ("", "numbers2", "")}
        replaced = chquery.replace_tables(sql, replacement)
        self.assertEqual(
            replaced, chquery.format("SELECT * FROM numbers2 as numbers, numbers(10)")
        )

    # https://gitlab.com/tinybird/analytics/-/issues/1964
    def test_analytics_1964(self):
        test_pipe_2_sql = "SELECT count() FROM test_pipe_1"
        test_pipe_1_sql = "(SELECT distinct n FROM node0)"
        dt = chquery.table_if_is_simple_query(
            test_pipe_1_sql, default_database="default"
        )
        self.assertIsNone(dt)

        replacement = {("default", "test_pipe_1"): ("", test_pipe_1_sql)}
        test_pipe_2_replaced = chquery.replace_tables(
            test_pipe_2_sql, replacement, default_database="default"
        )
        self.assertEqual(
            chquery.format(test_pipe_2_replaced),
            chquery.format(
                "SELECT count() FROM (SELECT DISTINCT n FROM node0) AS test_pipe_1"
            ),
        )

    def test_throws_with_invalid_query_types(self):
        queries = [
            "INSERT INTO test.table VALUES (1,2,3)",
            "RENAME DATABASE db_test TO db_test2",
            "SHOW DATABASES",
            "SHOW TABLES",
            "ALTER TABLE table_test ADD COLUMN column_test UInt32 FIRST",
            "CREATE TABLE table_test (`index` String) ENGINE = MergeTree ORDER BY index",
            "DROP TABLE test",
        ]
        replacement = {("default", "test_pipe_1"): ("", "something_else")}
        for q in queries:
            with self.assertRaisesRegex(
                ValueError, "Only SELECT or DESCRIBE queries are supported. Got: .*"
            ):
                chquery.replace_tables(q, replacement)

    def test_broken_platform(self):
        self.maxDiff = None
        test_pipe_1_sql = """
SELECT
    start_datetime,
    workspace_name,
    status_code,
    method,
    url,
    error,
    JSONExtract(tags, 'traceback', 'Array(String)') traceback,
    logs,
    tags,
    operation_name
FROM Internal.spans
where start_datetime > now() - INTERVAL 1 day
and status_code >= 500
and kind = 'server'
and component = 'tornado'
ORDER BY start_datetime DESC
        """

        test_pipe_2_sql = """
SELECT
    count() as 500_errors_count,
    500_errors_count as k_500_errors_count,
    uniq(cityHash64(error, traceback)) as uniq_errors
FROM (
    SELECT * FROM untitled_pipe_7234_0
    WHERE start_datetime > now() - INTERVAL 1 day
) a
join (
    SELECT * FROM untitled_pipe_7234_0
    WHERE start_datetime > now() - INTERVAL 1 day
) b
using k_500_errors_count
WHERE 1
ORDER BY 500_errors_count DESC
        """

        replacement = {
            ("default", "untitled_pipe_7234_0"): ("", "(" + test_pipe_1_sql + ")")
        }
        test_pipe_2_replaced = chquery.replace_tables(
            test_pipe_2_sql, replacement, default_database="default"
        )
        self.assertEqual(
            chquery.format(test_pipe_2_replaced),
            chquery.format("""
SELECT
    count() AS `500_errors_count`,
    `500_errors_count` AS k_500_errors_count,
    uniq(cityHash64(error, traceback)) AS uniq_errors
FROM
(
    SELECT *
    FROM
    (
        SELECT
            start_datetime,
            workspace_name,
            status_code,
            method,
            url,
            error,
            JSONExtract(tags, 'traceback', 'Array(String)') AS traceback,
            logs,
            tags,
            operation_name
        FROM Internal.spans
        WHERE (start_datetime > (now() - toIntervalDay(1))) AND (status_code >= 500) AND (kind = 'server') AND (component = 'tornado')
        ORDER BY start_datetime DESC
    ) AS untitled_pipe_7234_0
    WHERE start_datetime > (now() - toIntervalDay(1))
) AS a
INNER JOIN
(
    SELECT *
    FROM
    (
        SELECT
            start_datetime,
            workspace_name,
            status_code,
            method,
            url,
            error,
            JSONExtract(tags, 'traceback', 'Array(String)') AS traceback,
            logs,
            tags,
            operation_name
        FROM Internal.spans
        WHERE (start_datetime > (now() - toIntervalDay(1))) AND (status_code >= 500) AND (kind = 'server') AND (component = 'tornado')
        ORDER BY start_datetime DESC
    ) AS untitled_pipe_7234_0
    WHERE start_datetime > (now() - toIntervalDay(1))
) AS b USING (k_500_errors_count)
WHERE 1
ORDER BY `500_errors_count` DESC
"""),
        )

    def test_multiple_caches_with_renames(self):
        self.maxDiff = None
        source_query = """
SELECT count() as cuenta FROM my_table
        """

        target_query = """
SELECT * FROM my_pipe
UNION ALL
SELECT * FROM my_pipe
UNION ALL
SELECT * FROM my_pipe
UNION ALL
SELECT * FROM my_pipe
UNION ALL
SELECT * FROM my_pipe
UNION ALL
SELECT * FROM my_pipe
        """

        replacement = {("default", "my_pipe"): ("", "(" + source_query + ")")}
        test_pipe_2_replaced = chquery.replace_tables(
            target_query, replacement, default_database="default"
        )
        self.assertEqual(
            chquery.format(test_pipe_2_replaced),
            chquery.format("""
SELECT * FROM (SELECT count() AS cuenta FROM my_table) AS my_pipe
UNION ALL
SELECT * FROM (SELECT count() AS cuenta FROM my_table) AS my_pipe
UNION ALL
SELECT * FROM (SELECT count() AS cuenta FROM my_table) AS my_pipe
UNION ALL
SELECT * FROM (SELECT count() AS cuenta FROM my_table) AS my_pipe
UNION ALL
SELECT * FROM (SELECT count() AS cuenta FROM my_table) AS my_pipe
UNION ALL
SELECT * FROM (SELECT count() AS cuenta FROM my_table) AS my_pipe
"""),
        )

    # https://gitlab.com/tinybird/analytics/-/issues/492#note_619760161
    def test_join_with_subquery_works_fine(self):
        sql = """
        SELECT borough, count()
        FROM yellow_tripdata
        ANY LEFT JOIN zones_sub
        ON zones_sub.locationid = yellow_tripdata.pulocationid
        WHERE toYYYYMM(tpep_pickup_datetime) = 201901
        GROUP BY borough
        """
        replacements = {
            ("user_database", "yellow_tripdata", ""): (
                "d_6eea10",
                "t_f518869ccadb4c7e87c936acb5dfe351",
            ),
            ("user_database", "zones_sub"): (
                "d_6eea10",
                "(SELECT locationid, borough FROM taxi_zone_lookup)",
            ),
        }

        expected = """
        SELECT borough, count()
        FROM d_6eea10.t_f518869ccadb4c7e87c936acb5dfe351 AS yellow_tripdata
        ANY LEFT JOIN (SELECT locationid, borough FROM taxi_zone_lookup) AS zones_sub
        ON zones_sub.locationid = t_f518869ccadb4c7e87c936acb5dfe351.pulocationid
        WHERE toYYYYMM(tpep_pickup_datetime) = 201901
        GROUP BY borough
        """
        self.assertEqual(
            chquery.format(expected),
            chquery.replace_tables(sql, replacements, default_database="user_database"),
        )


class TestDisabledFunctions(unittest.TestCase):
    def test_sleep(self):
        queries = [
            "SELECT sleep(3)",
            "SELECT sleepEachRow(1) FROM numbers(10000)",
            "SELECT sleepEachRow(number) FROM numbers(10000)",
            "SELECT sleepEachRow(number + 10) FROM numbers(10000)",
            "SELECT toInt64(sleepEachRow(number + 10)) FROM numbers(10000)",
            "SELECT toInt64(sleepEachRow(a.sleep_ms)) FROM a",
        ]
        replacements = {}
        for q in queries:
            with self.assertRaisesRegex(
                ValueError, "DB::Exception: Usage of function sleep.* is restricted"
            ):
                chquery.replace_tables(q, replacements)

    def test_sleep_in_replacements(self):
        sql = "SELECT * FROM a, a"
        replacement = {
            ("default", "a"): ("", "(SELECT sleepEachRow(number) from numbers(100))")
        }
        with self.assertRaisesRegex(
            ValueError, "DB::Exception: Usage of function sleepEachRow is restricted"
        ):
            chquery.replace_tables(sql, replacement, default_database="default")

    def test_disabled_functions_when_function_validation_is_off(self):
        sql = "SELECT * FROM a, a"
        replacement = {
            ("default", "a"): ("", "(SELECT sleepEachRow(number) from numbers(100))")
        }
        expected = (
            "SELECT * FROM (SELECT sleepEachRow(number) FROM numbers(100)) a,"
            "(SELECT sleepEachRow(number) FROM numbers(100)) a"
        )
        replaced = chquery.replace_tables(
            sql, replacement, default_database="default", validate_functions=False
        )
        self.assertEqual(chquery.format(expected), chquery.format(replaced))

    def test_allow_function(self):
        sql = "SELECT * FROM a, a"
        replacement = {
            ("default", "a"): ("", "(SELECT sleepEachRow(number) from numbers(100))")
        }
        expected = (
            "SELECT * FROM (SELECT sleepEachRow(number) FROM numbers(100)) a,"
            "(SELECT sleepEachRow(number) FROM numbers(100)) a"
        )
        replaced = chquery.replace_tables(
            sql,
            replacement,
            default_database="default",
            function_allow_list=["sleepEachRow"],
        )
        self.assertEqual(chquery.format(expected), chquery.format(replaced))

    def test_unknown_function(self):
        sql = "SELECT * FROM a, a"
        replacement = {
            ("default", "a"): (
                "",
                "(SELECT sleepEachRowDOESNOTEXIST(number) from numbers(100))",
            )
        }
        with self.assertRaisesRegex(
            ValueError, "Unknown function sleepEachRowDOESNOTEXIST"
        ):
            chquery.replace_tables(sql, replacement, default_database="default")

    def test_allow_unknown_function(self):
        sql = "SELECT * FROM a, a"
        replacement = {
            ("default", "a"): (
                "",
                "(SELECT sleepEachRowDOESNOTEXIST(number) from numbers(100))",
            )
        }
        expected = (
            "SELECT * FROM (SELECT sleepEachRowDOESNOTEXIST(number) FROM numbers(100)) a,"
            "(SELECT sleepEachRowDOESNOTEXIST(number) FROM numbers(100)) a"
        )

        replaced = chquery.replace_tables(
            sql, replacement, default_database="default", validate_functions=False
        )
        self.assertEqual(chquery.format(expected), chquery.format(replaced))

        replaced = chquery.replace_tables(
            sql,
            replacement,
            default_database="default",
            function_allow_list=["sleepEachRowDOESNOTEXIST"],
        )
        self.assertEqual(chquery.format(expected), chquery.format(replaced))

    def test_deny_function(self):
        sql = "SELECT avg(t) FROM table"
        replacement = {}
        with self.assertRaisesRegex(
            ValueError, "DB::Exception: Usage of function avg is restricted"
        ):
            chquery.replace_tables(
                sql, replacement, default_database="default", function_deny_list=["AVG"]
            )

        replacement = {("default", "a"): ("default", "b")}
        with self.assertRaisesRegex(
            ValueError, "DB::Exception: Usage of function avg is restricted"
        ):
            chquery.replace_tables(
                sql, replacement, default_database="default", function_deny_list=["AVG"]
            )

        sql = "SELECT * FROM table"
        replacement = {("default", "table"): ("", "(SELECT avg(t) FROM table2)")}
        with self.assertRaisesRegex(
            ValueError, "DB::Exception: Usage of function avg is restricted"
        ):
            chquery.replace_tables(
                sql, replacement, default_database="default", function_deny_list=["AVG"]
            )

    def test_disabled_functions_with_invalid_parameters(self):
        sql = "SELECT * FROM a, a"
        replacement = {
            ("default", "a"): ("", "(SELECT sleepEachRow(number) from numbers(100))")
        }
        with self.assertRaisesRegex(TypeError, "'*"):
            chquery.replace_tables(
                sql,
                replacement,
                default_database="default",
                validate_functions=["Please help"],
            )

        with self.assertRaisesRegex(TypeError, "'*"):
            chquery.replace_tables(
                sql,
                replacement,
                default_database="default",
                validate_functions="Please help",
            )

        with self.assertRaisesRegex(TypeError, "argument 5 must be list, not dict"):
            chquery.replace_tables(
                sql,
                replacement,
                default_database="default",
                function_deny_list={"potatoes": "are_great"},
            )

        with self.assertRaisesRegex(TypeError, "argument 5 must be list, not str"):
            chquery.replace_tables(
                sql, replacement, default_database="default", function_deny_list="sleep"
            )

        with self.assertRaisesRegex(
            TypeError, "Invalid type found: dict. Expected str"
        ):
            chquery.replace_tables(
                sql,
                replacement,
                default_database="default",
                function_deny_list=[{"potatoes": "are_great"}],
            )

        with self.assertRaisesRegex(TypeError, "argument 6 must be list, not dict"):
            chquery.replace_tables(
                sql,
                replacement,
                default_database="default",
                function_allow_list={"potatoes": "are_great"},
            )

        with self.assertRaisesRegex(TypeError, "argument 6 must be list, not str"):
            chquery.replace_tables(
                sql,
                replacement,
                default_database="default",
                function_allow_list="sleep",
            )

        with self.assertRaisesRegex(
            TypeError, "Invalid type found: dict. Expected str"
        ):
            chquery.replace_tables(
                sql,
                replacement,
                default_database="default",
                function_allow_list=[{"potatoes": "are_great"}],
            )

    def test_block_settings(self):
        sql = "SELECT * FROM a, a"
        replacement = {
            ("default", "a"): (
                "",
                "(SELECT count() from system.numbers LIMIT 2 SETTINGS max_block_size=1)",
            )
        }
        with self.assertRaisesRegex(
            ValueError,
            """DB::Exception: Usage of setting 'max_block_size' is restricted. Contact support@tinybird.co if you require access to this feature""",
        ):
            chquery.replace_tables(sql, replacement, default_database="default")

        sql = "SELECT * FROM a SETTINGS max_block_size=1"
        replacement = {
            ("default", "a"): ("", "(SELECT count() from system.numbers LIMIT 2)")
        }
        with self.assertRaisesRegex(
            ValueError,
            """DB::Exception: Usage of setting 'max_block_size' is restricted. Contact support@tinybird.co if you require access to this feature""",
        ):
            chquery.replace_tables(sql, replacement, default_database="default")

    def test_allow_ignoring_settings(self):
        sql = "SELECT * FROM a"
        replacement = {
            ("default", "a"): (
                "",
                "(SELECT count() from system.numbers LIMIT 2 SETTINGS max_block_size=1)",
            )
        }
        replaced = chquery.replace_tables(
            sql, replacement, default_database="default", validate_query_settings=False
        )
        expected = "SELECT * FROM (SELECT count() from system.numbers LIMIT 2 SETTINGS max_block_size=1) AS a"
        self.assertEqual(chquery.format(expected), chquery.format(replaced))

        sql = "SELECT * FROM a SETTINGS max_block_size=1"
        replacement = {
            ("default", "a"): ("", "(SELECT count() from system.numbers LIMIT 2)")
        }
        replaced = chquery.replace_tables(
            sql, replacement, default_database="default", validate_query_settings=False
        )
        expected = "SELECT * FROM (SELECT count() from system.numbers LIMIT 2) AS a SETTINGS max_block_size=1"
        self.assertEqual(chquery.format(expected), chquery.format(replaced))

    def test_allow_enabled_settings(self):
        sql = "SELECT * FROM a, a SETTINGS join_use_nulls=1"
        replacement = {
            ("default", "a"): ("", "(SELECT count() from system.numbers LIMIT 2)")
        }
        replaced = chquery.replace_tables(sql, replacement, default_database="default")
        expected = "SELECT * FROM (SELECT count() from system.numbers LIMIT 2) AS a, (SELECT count() from system.numbers LIMIT 2) AS a SETTINGS join_use_nulls = 1"
        self.assertEqual(chquery.format(expected), chquery.format(replaced))

    def test_allow_analytics_query_settings(self):
        sql = """SELECT * FROM a SETTINGS
            max_threads = 1,
            max_memory_usage = 1000000,
            max_execution_time = 60,
            use_query_condition_cache = 0,
            prefer_column_name_to_alias = 1
        """
        replacement = {("default", "a"): ("", "(SELECT count() FROM system.numbers LIMIT 1)")}
        replaced = chquery.replace_tables(sql, replacement, default_database="default")
        out = chquery.format(replaced)
        self.assertIn("system.numbers", out)
        for key in (
            "max_threads",
            "max_memory_usage",
            "max_execution_time",
            "use_query_condition_cache",
            "prefer_column_name_to_alias",
        ):
            self.assertIn(key, out)

    def test_disallow_enabled_settings(self):
        sql = "SELECT * FROM a, a SETTINGS join_use_nulls=1"
        replacement = {
            ("default", "a"): ("", "(SELECT count() from system.numbers LIMIT 2)")
        }
        with self.assertRaisesRegex(
            ValueError,
            """DB::Exception: Usage of setting 'join_use_nulls' is restricted. Contact support@tinybird.co if you require access to this feature""",
        ):
            chquery.replace_tables(
                sql,
                replacement,
                default_database="default",
                query_settings_deny_list=["join_use_nulls"],
            )

        sql = "SELECT * FROM a"
        replacement = {
            ("default", "a"): (
                "",
                "(SELECT * from b, c LIMIT 2 SETTINGS join_use_nulls = 1)",
            )
        }
        with self.assertRaisesRegex(
            ValueError,
            """DB::Exception: Usage of setting 'join_use_nulls' is restricted. Contact support@tinybird.co if you require access to this feature""",
        ):
            chquery.replace_tables(
                sql,
                replacement,
                default_database="default",
                query_settings_deny_list=["join_use_nulls"],
            )

    def test_allow_enabled_join_algorithm_settings(self):
        sql = "SELECT * FROM a, a SETTINGS join_algorithm='grace_hash'"
        replacement = {
            ("default", "a"): ("", "(SELECT count() from system.numbers LIMIT 2)")
        }
        replaced = chquery.replace_tables(sql, replacement, default_database="default")
        expected = "SELECT * FROM (SELECT count() from system.numbers LIMIT 2) AS a, (SELECT count() from system.numbers LIMIT 2) AS a SETTINGS join_algorithm='grace_hash'"
        self.assertEqual(chquery.format(expected), chquery.format(replaced))

        sql = "SELECT * FROM a, a SETTINGS join_algorithm='parallel_hash,auto,hash'"
        replacement = {
            ("default", "a"): ("", "(SELECT count() from system.numbers LIMIT 2)")
        }
        replaced = chquery.replace_tables(sql, replacement, default_database="default")
        expected = "SELECT * FROM (SELECT count() from system.numbers LIMIT 2) AS a, (SELECT count() from system.numbers LIMIT 2) AS a SETTINGS join_algorithm='parallel_hash,auto,hash'"
        self.assertEqual(chquery.format(expected), chquery.format(replaced))

    def test_disallow_enabled_join_algorithm_settings(self):
        sql = "SELECT * FROM a, a SETTINGS join_algorithm='tinybird'"
        replacement = {
            ("default", "a"): ("", "(SELECT count() from system.numbers LIMIT 2)")
        }
        with self.assertRaisesRegex(
            ValueError,
            r"DB::Exception: Unexpected value of JoinAlgorithm: 'tinybird'. Must be one of \['full_sorting_merge', 'grace_hash', 'parallel_hash', 'direct', 'prefer_partial_merge', 'hash', 'partial_merge', 'auto', 'default'\]",
        ):
            chquery.replace_tables(sql, replacement, default_database="default")

        sql = "SELECT * FROM a, a SETTINGS join_algorithm='direct'"
        replacement = {
            ("default", "a"): ("", "(SELECT count() from system.numbers LIMIT 2)")
        }
        with self.assertRaisesRegex(
            ValueError,
            r"DB::Exception: The value for 'join_algorithm' is not supported \('direct'\). Contact support@tinybird.co if you require access to this feature",
        ):
            chquery.replace_tables(sql, replacement, default_database="default")

        sql = "SELECT * FROM a, a SETTINGS join_algorithm='parallel_hash,auto,hash,direct'"
        replacement = {
            ("default", "a"): ("", "(SELECT count() from system.numbers LIMIT 2)")
        }
        with self.assertRaisesRegex(
            ValueError,
            r"DB::Exception: The value for 'join_algorithm' is not supported \('direct'\). Contact support@tinybird.co if you require access to this feature",
        ):
            chquery.replace_tables(sql, replacement, default_database="default")

    def test_allow_enabled_date_time_output_format_setting(self):
        sql = "SELECT now() from a SETTINGS date_time_output_format='iso'"
        replacement = {("default", "a"): ("", "(select 1 from system.numbers LIMIT 1)")}
        replaced = chquery.replace_tables(sql, replacement, default_database="default")
        expected = "SELECT now() FROM (SELECT 1 FROM system.numbers LIMIT 1) AS a SETTINGS date_time_output_format='iso'"
        self.assertEqual(chquery.format(expected), chquery.format(replaced))

    def test_cte_escape(self):
        replacements = {
            ("d_012345", "table1"): ("d_012345", "alibaba"),
        }
        query = "WITH table1 AS (SELECT * FROM table1) SELECT * FROM table1"
        replaced = chquery.replace_tables(
            query, replacements, default_database="d_012345"
        )
        expected_query = "WITH table1 AS (SELECT * FROM d_012345.alibaba AS table1) SELECT * FROM table1"
        self.assertEqual(replaced, chquery.format(expected_query))

    def test_cte_escape_nested(self):
        replacements = {
            ("d_012345", "table1"): ("d_012345", "alibaba"),
        }
        query = "WITH table1 AS (WITH table2 AS (SELECT * FROM table1) SELECT * FROM table2) SELECT * from table1"
        replaced = chquery.replace_tables(
            query, replacements, default_database="d_012345"
        )
        expected_query = "WITH table1 AS (WITH table2 AS (SELECT * FROM d_012345.alibaba AS table1) SELECT * FROM table2) SELECT * from table1"
        self.assertEqual(replaced, chquery.format(expected_query))

    def test_cte_escape_db(self):
        replacements = {
            ("other", "table1"): ("d_012345", "alibaba"),
        }
        query = "WITH table1 AS (SELECT * FROM other.table1) SELECT * FROM table1"
        replaced = chquery.replace_tables(
            query, replacements, default_database="d_012345"
        )
        expected_query = "WITH table1 AS (SELECT * FROM d_012345.alibaba AS table1) SELECT * FROM table1"
        self.assertEqual(replaced, chquery.format(expected_query))

    def test_cte_escape_db2(self):
        replacements = {
            ("other", "table2"): ("d_012345", "alibaba"),
        }
        query = "WITH table1 AS (SELECT * FROM other.table2) SELECT * FROM table1"
        replaced = chquery.replace_tables(
            query, replacements, default_database="d_012345"
        )
        expected_query = "WITH table1 AS (SELECT * FROM d_012345.alibaba AS table2) SELECT * FROM table1"
        self.assertEqual(replaced, chquery.format(expected_query))

    def test_cte_escape_scalar(self):
        replacements = {
            ("", "table2"): ("d_012345", "alibaba"),
        }
        query = "WITH (SELECT COUNT(*) FROM table2) as table2 SELECT table2"
        replaced = chquery.replace_tables(
            query, replacements, default_database="d_012345"
        )
        expected_query = "WITH (SELECT COUNT(*) FROM d_012345.alibaba AS table2) as table2 SELECT table2"
        self.assertEqual(replaced, chquery.format(expected_query))

    def test_cte_escape_scalar2(self):
        replacements = {
            ("d_012345", "table1"): ("d_012345", "alibaba"),
            ("d_012345", "table2"): ("d_012345", "alibabax"),
        }
        query = "WITH (SELECT COUNT(*) FROM table2) as table1 SELECT * FROM table1"
        replaced = chquery.replace_tables(
            query, replacements, default_database="d_012345"
        )
        expected_query = "WITH (SELECT COUNT(*) FROM d_012345.alibabax AS table2) as table1 SELECT * FROM d_012345.alibaba AS table1"
        self.assertEqual(replaced, chquery.format(expected_query))

    def test_in_operator_with_literals_alias(self):
        replacements = {
            ("d_012345", "a"): ("d_012345", "alibaba"),
        }
        query = "WITH [1, 2] AS a SELECT 1 as v WHERE v IN a"
        replaced = chquery.replace_tables(
            query, replacements, default_database="d_012345"
        )
        expected_query = "WITH [1, 2] AS a SELECT 1 as v WHERE v IN a"
        self.assertEqual(replaced, chquery.format(expected_query))

    def test_in_operator_with_subquery_alias_2(self):
        replacements = {
            ("d_012345", "a"): ("d_012345", "alibaba"),
        }
        query = "WITH a AS (SELECT * FROM a) SELECT 1 as v WHERE v IN a"
        replaced = chquery.replace_tables(
            query, replacements, default_database="d_012345"
        )
        expected_query = (
            "WITH a AS (SELECT * FROM d_012345.alibaba AS a) SELECT 1 as v WHERE v IN a"
        )
        self.assertEqual(replaced, chquery.format(expected_query))

    def test_in_operator_with_subquery_alias_3(self):
        replacements = {
            ("d_012345", "a"): ("d_012345", "alibaba"),
            ("d_012345", "table2"): ("d_012345", "alibabax"),
        }
        query = "WITH a AS (SELECT * FROM table2) SELECT 1 as v WHERE v IN a"
        replaced = chquery.replace_tables(
            query, replacements, default_database="d_012345"
        )
        expected_query = "WITH a AS (SELECT * FROM d_012345.alibabax AS table2) SELECT 1 as v WHERE v IN a"
        self.assertEqual(replaced, chquery.format(expected_query))

    def test_in_operator_with_scalar_subquery_alias(self):
        replacements = {("d_012345", "table2"): ("d_012345", "repl2")}
        query = "WITH (SELECT (a, b) FROM table1 as table2 ) AS table2 SELECT * FROM table1 WHERE (a, b) IN table2"
        replaced = chquery.replace_tables(
            query, replacements, default_database="d_012345"
        )
        expected_query = "WITH (SELECT (a, b) FROM table1 as table2 ) AS table2 SELECT * FROM table1 WHERE (a, b) IN table2"
        self.assertEqual(replaced, chquery.format(expected_query))

    def test_cte_siblings(self):
        replacements = {
            ("d_012345", "table1"): ("d_012345", "repl1"),
            ("d_012345", "alias1"): ("d_012345", "repl2"),
            ("d_012345", "alias2"): ("d_012345", "repl3"),
        }
        query = "WITH alias1 as (select * from table1), alias2 as (select * from alias1) select * from alias2"
        replaced = chquery.replace_tables(
            query, replacements, default_database="d_012345"
        )
        expected_query = "WITH alias1 as (select * from d_012345.repl1 as table1), alias2 as (select * from alias1) select * from alias2"
        self.assertEqual(replaced, chquery.format(expected_query))

    def test_cte_siblings_wrong_order(self):
        replacements = {
            ("d_012345", "table1"): ("d_012345", "repl1"),
            ("d_012345", "alias1"): ("d_012345", "repl2"),
            ("d_012345", "alias2"): ("d_012345", "repl3"),
        }
        query = "WITH alias2 as (select * from alias1), alias1 as (select * from table1) select * from alias2"
        replaced = chquery.replace_tables(
            query, replacements, default_database="d_012345"
        )
        expected_query = "WITH alias2 as (select * from d_012345.repl2 as alias1), alias1 as (select * from d_012345.repl1 as table1) select * from alias2"
        self.assertEqual(replaced, chquery.format(expected_query))

    def test_cte_homonym_aliases(self):
        replacements = {("d_012345", "table1"): ("d_012345", "repl1")}
        query = (
            "WITH 1 as table1, table1 as (select * from table1) select * from table1"
        )
        replaced = chquery.replace_tables(
            query, replacements, default_database="d_012345"
        )
        expected_query = "WITH 1 as table1, table1 as (select * from d_012345.repl1 as table1) select * from table1"
        self.assertEqual(replaced, chquery.format(expected_query))

    def test_cte_homonym_aliases2(self):
        replacements = {("d_012345", "table1"): ("d_012345", "repl1")}
        query = (
            "WITH table1 as (select * from table1), 1 as table1 select * from table1"
        )
        replaced = chquery.replace_tables(
            query, replacements, default_database="d_012345"
        )
        expected_query = "WITH table1 as (select * from d_012345.repl1 as table1), 1 as table1 select * from table1"
        self.assertEqual(replaced, chquery.format(expected_query))

    def test_cte_escape_literal(self):
        replacements = {
            ("", "table2"): ("d_012345", "alibaba"),
        }
        query = "WITH 1 as table2 SELECT table2"
        replaced = chquery.replace_tables(
            query, replacements, default_database="d_012345"
        )
        expected_query = "WITH 1 as table2 SELECT table2"
        self.assertEqual(replaced, chquery.format(expected_query))

    def test_cte_escape_literal2(self):
        replacements = {("d_012345", "table1"): ("d_012345", "alibaba")}
        query = "WITH 2 as table1 SELECT * FROM table1"
        replaced = chquery.replace_tables(
            query, replacements, default_database="d_012345"
        )
        expected_query = "WITH 2 as table1 SELECT * FROM d_012345.alibaba AS table1"
        self.assertEqual(replaced, chquery.format(expected_query))

    def test_cte_with_enable_global_with_statement_off(self):
        replacements = {
            ("d_012345", "table1"): ("d_012345", "repl1"),
            ("d_012345", "table2"): ("d_012345", "repl2"),
        }
        query = "WITH (select * from table2 limit 1) as table1 select * from (select 1 as v where v in table1)"
        replaced = chquery.replace_tables(
            query, replacements, default_database="d_012345"
        )
        expected_query = "WITH (select * from d_012345.repl2 as table2 limit 1) as table1 select * from (select 1 as v where v in d_012345.repl1)"
        self.assertEqual(replaced, chquery.format(expected_query))

    def test_cte_with_enable_global_with_statement_off2(self):
        replacements = {
            ("d_012345", "table1"): ("d_012345", "repl1"),
            ("d_012345", "table2"): ("d_012345", "repl2"),
        }
        query = "WITH (select * from table2 limit 1) as table1, (select 1 as v where v in table1) as x select x"
        replaced = chquery.replace_tables(
            query, replacements, default_database="d_012345"
        )
        expected_query = "WITH (select * from d_012345.repl2 as table2 limit 1) as table1, (select 1 as v where v in d_012345.repl1) as x select x"
        self.assertEqual(replaced, chquery.format(expected_query))
