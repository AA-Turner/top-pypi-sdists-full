import unittest
from chtoolset import query as chquery

import logging
logging.basicConfig(level=logging.DEBUG)


class TestInvalidSQLRaises(unittest.TestCase):
    sql = "WADUS QUERY"

    def test_format_query(self):
        with self.assertRaisesRegex(ValueError, 'Syntax error'):
            chquery.format(self.sql)

    def test_format_query_one_line(self):
        with self.assertRaisesRegex(ValueError, 'Syntax error'):
            chquery.format(self.sql, one_line=True)

    def test_extract_tables(self):
        with self.assertRaisesRegex(ValueError, 'Syntax error'):
            chquery.tables(self.sql)

    def test_replace(self):
        with self.assertRaisesRegex(ValueError, 'Syntax error'):
            chquery.replace_tables(self.sql, {})

    def test_replace_parsing_error(self):
        sql = r'select count() c from \`test_table\` format JSON'
        with self.assertRaisesRegex(ValueError, 'Syntax error'):
            chquery.replace_tables(sql, {
                ('', 'test_table'): ('', 'l1')
            })

    def test_error_for_invalid_key_type(self):
        with self.assertRaisesRegex(ValueError, 'Key replacement must be a tuple'):
            chquery.replace_tables('SELECT 1', {
                'test_table': 'l1'
            })

    def test_error_for_invalid_value_type(self):
        with self.assertRaisesRegex(ValueError, 'Value replacement must be a tuple'):
            chquery.replace_tables('SELECT 1', {
                ('', 'test_table'): 'l1'
            })

    def test_error_for_invalid_key_tuple_size(self):
        with self.assertRaisesRegex(ValueError, 'Key replacement must be a tuple containing database and table name'):
            chquery.replace_tables('SELECT 1', {
                ('test_table',): 'l1'
            })

    def test_error_for_invalid_value_tuple_size(self):
        with self.assertRaisesRegex(ValueError, 'Value replacement must be a tuple containing database and table name'):
            chquery.replace_tables('SELECT 1', {
                ('', 'test_table'): ('l1',)
            })


class TestBasicSQL(unittest.TestCase):
    sql = "SELECT * FROM table_a"

    def test_extract_tables(self):
        self.assertEqual(chquery.tables(self.sql), [('', 'table_a', '')])

    def test_extract_tables_default_database(self):
        self.assertEqual(chquery.tables(self.sql, default_database='d_012345'), [('d_012345', 'table_a', '')])

    def test_replace(self):
        replaced = chquery.replace_tables(self.sql, {
            ('', 'table_a'): ('', '__t_id_1')
        })
        self.assertEqual(replaced, chquery.format("SELECT * FROM __t_id_1 as table_a"))

    def test_replace_default_database(self):
        replaced = chquery.replace_tables(self.sql, {
            ('d_012345', 'table_a'): ('d_012345', '__t_id_1')
        }, default_database='d_012345')
        self.assertEqual(replaced, chquery.format("SELECT * FROM d_012345.__t_id_1 as table_a"))

    def test_replace_tuple(self):
        replaced = chquery.replace_tables("SELECT * FROM db_1.table_a", {
            ('db_1', 'table_a'): ('db_r', '__t_id_1')
        })
        self.assertEqual(replaced, chquery.format("SELECT * FROM db_r.__t_id_1 as table_a"))

    def test_table_if_is_simple_query(self):
        table = chquery.table_if_is_simple_query(self.sql)
        self.assertEqual(table, ('', 'table_a', ''))

    def test_table_if_is_simple_with_database(self):
        table = chquery.table_if_is_simple_query('Select * from db.t')
        self.assertEqual(table, ('db', 't', ''))

    def test_table_if_is_simple_query_default_database(self):
        table = chquery.table_if_is_simple_query(self.sql, default_database='d_012345')
        self.assertEqual(table, ('d_012345', 'table_a', ''))

    def test_table_if_is_simple_query_not_simple(self):
        table = chquery.table_if_is_simple_query("select * from table_z where 1=2")
        self.assertIsNone(table)

    def test_table_if_is_simple_query_not_simple_default_database(self):
        table = chquery.table_if_is_simple_query("select * from table_z where 1=2", default_database='d_012345')
        self.assertIsNone(table)

    def test_table_if_is_simple_query_with_table_function(self):
        table = chquery.table_if_is_simple_query("select * from numbers(10)", default_database='d_012345')
        self.assertIsNone(table)

    def test_table_if_is_simple_query_with_distinct_columns(self):
        table = chquery.table_if_is_simple_query("SELECT distinct n FROM node0", default_database='d_012345')
        self.assertIsNone(table)

    def test_table_if_is_simple_query_with_columns(self):
        table = chquery.table_if_is_simple_query("SELECT a FROM table_name", default_database='d_012345')
        self.assertIsNone(table)

    # If the table has an alias we can't simply replace it by `table_name`
    def test_table_if_is_simple_query_with_table_alias(self):
        table = chquery.table_if_is_simple_query("SELECT * FROM table_name as b", default_database='d_012345')
        self.assertIsNone(table)

        table = chquery.table_if_is_simple_query("SELECT * FROM db.table_name as b", default_database='d_012345')
        self.assertIsNone(table)


class TestTablenameWithDots(unittest.TestCase):
    sql = 'SELECT * FROM "aaaa.aaa.aaa"'

    def test_extract_tables(self):
        self.assertEqual(chquery.tables(self.sql), [('', 'aaaa.aaa.aaa', '')])

    def test_extract_tables_default_database(self):
        self.assertEqual(chquery.tables(self.sql, default_database='d_012345'), [('d_012345', 'aaaa.aaa.aaa', '')])

    def test_replace(self):
        replaced = chquery.replace_tables(self.sql, {
            ('', 'aaaa.aaa.aaa'): ('', 'bbbb.bbb.b')
        })
        self.assertEqual(replaced, chquery.format('SELECT * FROM "bbbb.bbb.b" as `aaaa.aaa.aaa`'))

    def test_replace_default_database(self):
        replaced = chquery.replace_tables(self.sql, {
            ('d_012345', 'aaaa.aaa.aaa'): ('d_012345', 'bbbb.bbb.b')
        }, default_database='d_012345')
        self.assertEqual(replaced, chquery.format("SELECT * FROM d_012345.`bbbb.bbb.b` as `aaaa.aaa.aaa`"))

    def test_replace_tuple(self):
        replaced = chquery.replace_tables("SELECT * FROM db_1.`aaaa.aaa.aaa`", {
            ('db_1', 'aaaa.aaa.aaa'): ('db_r', '__t_id_1')
        })
        self.assertEqual(replaced, chquery.format("SELECT * FROM db_r.__t_id_1 AS `aaaa.aaa.aaa`"))

    def test_replace_tuple_default_database(self):
        replaced = chquery.replace_tables("SELECT * FROM db_1.`aaaa.aaa.aaa`", {
            ('db_1', 'aaaa.aaa.aaa'): ('d_012345', '__t_id_1')
        }, default_database='d_012345')
        self.assertEqual(replaced, chquery.format("SELECT * FROM d_012345.__t_id_1 AS `aaaa.aaa.aaa`"))

    def test_table_if_is_simple_query(self):
        table = chquery.table_if_is_simple_query(self.sql)
        self.assertEqual(table, ('', 'aaaa.aaa.aaa', ''))

    def test_table_if_is_simple_query_default_database(self):
        table = chquery.table_if_is_simple_query(self.sql, default_database='d_012345')
        self.assertEqual(table, ('d_012345', 'aaaa.aaa.aaa', ''))

    def test_table_if_is_simple_query_not_simple(self):
        table = chquery.table_if_is_simple_query("select * from `aaaa.aaa.aaa` where 1=2")
        self.assertIsNone(table)

    def test_table_if_is_simple_query_not_simple_default_database(self):
        table = chquery.table_if_is_simple_query("select * from `aaaa.aaa.aaa` where 1=2", default_database='d_012345')
        self.assertIsNone(table)


class TestMultipleTablesSQL(unittest.TestCase):
    def test_extract_tables(self):
        sql = """
            SELECT
                db_1.table_a.*,
                table_a.col0,
                a.col1,
                b.col0
            FROM table_a as a any inner join (
                SELECT * FROM db_2.table_b
            ) as b USING unified
        """
        self.assertEqual(chquery.tables(sql), [('', 'table_a', ''), ('db_2', 'table_b', '')])

    def test_extract_tables_default_database(self):
        sql = """
            SELECT
                d_012345.table_a.*,
                table_a.col0,
                a.col1,
                b.col0
            FROM table_a as a any inner join (
                SELECT * FROM db_2.table_b
            ) as b USING unified
        """
        self.assertEqual(chquery.tables(sql, default_database='d_012345'),
                         [('d_012345', 'table_a', ''), ('db_2', 'table_b', '')])

    def test_replace_tables(self):
        sql = """
            SELECT
                table_a.*,
                table_a.col0,
                a.col1,
                b.col0
            FROM table_a as a any inner join (
                SELECT * FROM db_2.table_b
            ) as b USING unified
        """
        replaced = chquery.replace_tables(sql, {
            ('', 'table_a'): ('', '__t_id_1'),
            ('db_1', 'table_a'): ('', '__t_id_1'),
            ('db_2', 'table_b'): ('', '__t_id_2')
        })
        self.assertEqual(replaced, chquery.format("""
            SELECT
                __t_id_1.*,
                __t_id_1.col0,
                a.col1,
                b.col0
            FROM __t_id_1 as a any inner join (
                SELECT * FROM __t_id_2 as table_b
            ) as b USING unified
        """))

    def test_replace_tables_default_database(self):
        sql = """
            SELECT
                db_1.table_a.*,
                table_a.col0,
                a.col1,
                b.col0
            FROM table_a as a any inner join (
                SELECT * FROM db_2.table_b
            ) as b USING unified
        """
        replaced = chquery.replace_tables(sql, {
            ('db_1', 'table_a'): ('d_012345', '__t_id_1'),
            ('db_2', 'table_b'): ('d_012345', '__t_id_2')
        }, default_database='db_1')
        self.assertEqual(replaced, chquery.format("""
            SELECT
                d_012345.__t_id_1.*,
                __t_id_1.col0,
                a.col1,
                b.col0
            FROM d_012345.__t_id_1 as a any inner join (
                SELECT * FROM d_012345.__t_id_2 as table_b
            ) as b USING unified
        """))


class TestComplexSQL(unittest.TestCase):

    def test_extract_tables(self):
        sql = """
         -- precompute the growth year-to-year for July
        WITH (
          SELECT
            c_2018 / c_2017 ratio,
            countIf(toYear(tpep_pickup_datetime) == 2018) c_2018,
            countIf(toYear(tpep_pickup_datetime) == 2017) c_2017
          from `nytaxi`
          WHERE toMonth(tpep_pickup_datetime) == 7
        ) as growth

        -- compute diff between 2018 prediction and 2018 real data
        SELECT
            toDate('2018-01-01') + d as day,
            growth.1 as ratio,
            -- this is the actual model :)
            c_2017 * ratio as estimated,
            c_2018,
            abs(c_2018 - estimated) as abs_error,
            abs(c_2018 - estimated)/c_2018 as rel_error

        -- 2018 data to evaluate the model
        FROM (
            SELECT toInt32(toDayOfYear((tpep_pickup_datetime))) d, count(1) c_2018
            from `nytaxi2` WHERE toYYYYMM(tpep_pickup_datetime) == 201808
            GROUP BY d
        )

        -- 2017 data, note the 1-day offset
        ANY INNER JOIN
        (
            SELECT toDayOfYear((tpep_pickup_datetime)) - 1 d, count(1) c_2017
            from `nytaxi3` WHERE toYYYYMM(tpep_pickup_datetime) == 201708
            GROUP BY d
        )
        USING d
        ORDER BY day
        """
        tables = chquery.tables(sql)
        self.assertEqual(tables, [('', 'nytaxi', ''), ('', 'nytaxi2', ''), ('', 'nytaxi3', '')])
        tables = chquery.tables(sql, default_database='d_012345')
        self.assertEqual(tables, [('d_012345', 'nytaxi', ''), ('d_012345', 'nytaxi2', ''), ('d_012345', 'nytaxi3', '')])

    def test_extract_tables_1(self):
        sql = """
        select *
        from (
            select * from (
                select toDate(tpep_pickup_datetime) as d,
                count(1)
                from yellow_tripdata_2018_03 group by d
            ) as yellow_tr_4 join (
                select toDate(lpep_pickup_datetime) as d,
                count(1)
                from green_tripdata_2018_03 group by d
            ) as green_tri_3 on d
        )
        limit 100
        """
        tables = chquery.tables(sql)
        self.assertEqual(tables, [('', 'green_tripdata_2018_03', ''), ('', 'yellow_tripdata_2018_03', '')])
        tables = chquery.tables(sql, default_database='d_012345')
        self.assertEqual(tables, [('d_012345', 'green_tripdata_2018_03', ''), ('d_012345', 'yellow_tripdata_2018_03', '')])

    def test_replace_with_join(self):
        sql = """
        select * from (
            select * from (
                select * from listings where city like '_evill_'
            ) as f
            UNION ALL
            select * from (
                select * from checkings as cc any left join (
                    select unifiedid, city, bedrooms from listings where city = 'Seville'
                ) aa using unifiedid
            ) as l_13
        ) limit 100
        """
        replaced = chquery.replace_tables(sql, {
            ('', 'listings'): ('', 'l1'),
            ('', 'checkings'): ('', 'c1')
        })

        self.assertEqual(replaced, chquery.format("""
        select * from (
            select * from (
                select * from l1 as listings where city like '_evill_'
            ) as f
            UNION ALL
            select * from (
                select * from c1 as cc any left join (
                    select unifiedid, city, bedrooms from l1 as listings where city = 'Seville'
                ) aa using unifiedid
            ) as l_13
        ) limit 100
        """))

    def test_replace_with_join_default_database(self):
        sql = """
        select * from (
            select * from (
                select * from listings where city like '_evill_'
            ) as f
            UNION ALL
            select * from (
                select * from checkings as cc any left join (
                    select unifiedid, city, bedrooms from listings where city = 'Seville'
                ) aa using unifiedid
            ) as l_13
        ) limit 100
        """
        replaced = chquery.replace_tables(sql, {
            ('d_012345', 'listings'): ('d_012345', 'l1'),
            ('d_012345', 'checkings'): ('d_012345', 'c1')
        }, default_database='d_012345')
        self.assertEqual(replaced, chquery.format("""
        select * from (
            select * from (
                select * from d_012345.l1 as listings where city like '_evill_'
            ) as f
            UNION ALL
            select * from (
                select * from d_012345.c1 as cc any left join (
                    select unifiedid, city, bedrooms from d_012345.l1 as listings where city = 'Seville'
                ) aa using unifiedid
            ) as l_13
        ) limit 100
        """))

    def test_extract_tables_expression_list_database_default_database(self):
        sql = """
        select default.table_a.col2 FROM table_a
        """
        # Note: The toolset won't detect default.table_a because this query is invalid (and you won't ever access it)
        tables = chquery.tables(sql, default_database='d_012345')
        self.assertEqual(tables, [('d_012345', 'table_a', '')])

    def test_same_table_and_column_name(self):
        sql = """SELECT `cod_store`,`country_iso`,sum(stores_stock) as stores_stock from stores_stock group by `cod_store`,`country_iso`"""
        replaced = chquery.replace_tables(sql, {
            ('d_012345', 'stores_stock'): ('d_012345', 't_123')
        }, default_database='d_012345')
        self.assertEqual(replaced, chquery.format("""SELECT `cod_store`,`country_iso`,sum(stores_stock) as stores_stock from d_012345.t_123 as stores_stock group by `cod_store`,`country_iso`"""))

    def test_replace_cache(self):
        sql = "SELECT * FROM system.tables, system.tables"

        replaced = chquery.replace_tables(sql, {
            ('system', 'tables'): ('', '(SELECT * FROM system.parts)')
        }, default_database='d_012345')

        self.assertEqual(replaced, chquery.format("""SELECT *
        FROM
        (
            SELECT *
            FROM system.parts
        ) AS tables,
        (
            SELECT *
            FROM system.parts
        ) AS tables
        """))

    def test_query_get_type(self):
        queries_results = [("SELECT * FROM test.table", "SelectWithUnionQuery"),
                           ("INSERT INTO test.table VALUES (1,2,3)", "InsertQuery"),
                           ("RENAME DATABASE db_test TO db_test2", "RenameQuery"),
                           ("SHOW PROCESSLIST", "ShowProcesslistIDAndQueryNames"),
                           ("SHOW TABLES FROM db_test", "ShowTablesQuery"),
                           ("SHOW DATABASES", "ShowTablesQuery"),
                           ("DESC table_test", "DescribeQuery"),
                           ("CHECK TABLE table_test", "CheckTableQuery"),
                           ("SHOW CREATE table_test", "ShowCreateTableQueryIDAndQueryNames"),
                           ("DESCRIBE table_test", "DescribeQuery"),
                           ("DESCRIBE TABLE table_test", "DescribeQuery"),
                           ("CREATE TABLE table_test (`index` String) ENGINE = MergeTree ORDER BY index", "CreateQuery"),
                           ("ATTACH TABLE IF NOT EXISTS table_test", "CreateQuery"),
                           ("DROP TABLE table_test", "DropQuery"),
                           ("WITH now() AS ahora SELECT ahora", "SelectWithUnionQuery"),
                           ("EXISTS TABLE table_test", "ExistsTableQueryIDAndQueryNames"),
                           ("ALTER TABLE table_test ADD COLUMN column_test UInt32 FIRST", "AlterQuery"),
                           ("DETACH TABLE table_test", "DropQuery"),
                           ("TRUNCATE TABLE table_test", "DropQuery"),
                           ("SET ROLE TEST", "SetRoleQuery"),
                           ("GRANT SELECT ON *.* TO test", "GrantQuery"),
                           ("REVOKE SELECT ON db.table FROM test", "GrantQuery"),
                           ("DROP TABLE test", "DropQuery")]
        for query, result in queries_results:
            self.assertEqual(chquery.query_get_type(query), result)

        with self.assertRaisesRegex(ValueError, 'Syntax error'):
            chquery.query_get_type("NOT A QUERY")

    def test_format_patch_ASTWithAlias_is_applied(self):
        # Without the patch to ASTWithAlias CH automatically replaces same subqueries with alias
        # which is fine except it's bad for performance
        sql = """SELECT
    (
        SELECT max(value)
        FROM datasource
    ) AS max,
    (
        SELECT max(value)
        FROM datasource
    ) AS max"""
        # Without the patch the second subquery will be replaced by just "max"
        self.assertEqual(chquery.format(sql), sql)

    def test_format_one_line(self):
        sql = "SELECT max(value)\nFROM datasource\nWHERE value < 100"

        self.assertEqual(chquery.format(sql), sql)
        self.assertEqual(chquery.format(sql, one_line=True), "SELECT max(value) FROM datasource WHERE value < 100")


class TestStreamQueries(unittest.TestCase):

    def test_extract_tables_basic_stream(self):
        queries = [
            """
                SELECT
                    a
                FROM events STREAM TAIL
                WHERE 1 = 1
            """,
            """
                SELECT
                    a
                FROM events STREAM
                WHERE 1 = 1
            """
        ]

        for sql in queries:
            self.assertEqual(chquery.tables(sql, default_database='d_012345'),
                             [('d_012345', 'events', '')])

    def test_replace_stream(self):
        sql = "SELECT * FROM events STREAM TAIL WHERE 1 = 1"

        replaced = chquery.replace_tables(sql, {
            ('d_012345', 'events'): ('', '(SELECT * FROM d_012345.t_012345)')
        }, default_database='d_012345')

        self.assertEqual(replaced, chquery.format("SELECT * FROM (SELECT * FROM d_012345.t_012345) AS events STREAM TAIL WHERE 1 = 1"))


class TestJSONQueries(unittest.TestCase):
    def test_json_queries(self):
        queries = ["SELECT json.^a.b, json.^d.e.f FROM test;",
                   "SELECT json.a.b.:Float64, json.a.g.:Date, json.c.:String, json.d.:UInt8 FROM test",
                   "SELECT json.^a.b, json.^d.e.f FROM test;"]
        for sql in queries:
            replaced = chquery.replace_tables(sql, {
                ('d_012345', 'test'): ('', '(SELECT * FROM d_012345.t_012345)')
            }, default_database='d_012345')
            expected_sql = sql.replace("test", "(SELECT * FROM d_012345.t_012345) AS test")
        self.assertEqual(replaced, chquery.format(expected_sql))


class TestTrimFormatting(unittest.TestCase):
    """Verify TRIM functions with custom characters produce standard SQL syntax
    compatible with CH < 25.2 (where trimBoth only accepted 1 argument)."""

    def test_trim_both_with_chars(self):
        """TRIM(BOTH 'x' FROM s) must round-trip as TRIM(BOTH ... FROM ...), not trimBoth(s, 'x')"""
        sql = "SELECT TRIM(BOTH '\"' FROM api_key) FROM t"
        result = chquery.format(sql)
        self.assertIn("TRIM(BOTH", result)
        self.assertNotIn("trimBoth", result)

    def test_trim_leading_with_chars(self):
        sql = "SELECT TRIM(LEADING '0' FROM col) FROM t"
        result = chquery.format(sql)
        self.assertIn("TRIM(LEADING", result)
        self.assertNotIn("trimLeft", result)

    def test_trim_trailing_with_chars(self):
        sql = "SELECT TRIM(TRAILING ' ' FROM col) FROM t"
        result = chquery.format(sql)
        self.assertIn("TRIM(TRAILING", result)
        self.assertNotIn("trimRight", result)

    def test_trim_both_without_chars_unchanged(self):
        """1-arg trimBoth(s) should remain as trimBoth(s) - it works on all CH versions"""
        sql = "SELECT trimBoth(col) FROM t"
        result = chquery.format(sql)
        self.assertIn("trimBoth", result)

    def test_trim_no_custom_char(self):
        """1-arg trim (no custom char) should not produce 2-arg form"""
        sql = "SELECT trim(col) FROM t"
        result = chquery.format(sql)
        self.assertNotRegex(result, r'trimBoth\([^)]+,[^)]+\)')

    def test_trim_in_replace_tables(self):
        """Verify the fix works through replace_tables too"""
        sql = "SELECT TRIM(BOTH '\"' FROM api_key) FROM my_table"
        result = chquery.replace_tables(sql, {
            ('', 'my_table'): ('', 'other_table')
        })
        self.assertNotIn("trimBoth", result)

    def test_direct_trimboth_2arg(self):
        """Direct trimBoth(s, 'x') call also gets rewritten to TRIM syntax"""
        sql = "SELECT trimBoth(col, 'x') FROM t"
        result = chquery.format(sql)
        self.assertIn("TRIM(BOTH", result)

    def test_trim_function_rewrite_is_case_insensitive(self):
        sql = "SELECT TRIMBOTH(col, 'x'), TRIMLEFT(col, '0'), TRIMRIGHT(col, '0') FROM t"
        result = chquery.format(sql)
        self.assertIn("TRIM(BOTH", result)
        self.assertIn("TRIM(LEADING", result)
        self.assertIn("TRIM(TRAILING", result)
        self.assertNotIn("TRIMBOTH", result)
        self.assertNotIn("TRIMLEFT", result)
        self.assertNotIn("TRIMRIGHT", result)
        self.assertNotIn("trimBoth", result)
        self.assertNotIn("trimLeft", result)
        self.assertNotIn("trimRight", result)
