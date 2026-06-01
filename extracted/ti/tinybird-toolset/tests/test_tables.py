import unittest
from chtoolset import query as chquery

import logging
logging.basicConfig(level=logging.DEBUG)


class TestTables(unittest.TestCase):

    scenarios = [
        ('select * from _table', [('', '_table', '')]),
        ('select * from "aaaa.aaa.aaa"', [('', 'aaaa.aaa.aaa', '')]),
        ('with t2 as (select * FROM _table) select * FROM t2', [('', '_table', '')]),
        ('select * from table join table2 using a', [('', 'table', ''), ('', 'table2', '')]),
        ('select * FROM db.table JOIN `table2` using b', [('', 'table2', ''), ('db', 'table', '')]),
        ('select 1', []),
        ('select * from (select whatever from _table)', [('', '_table', '')]),
        ('select * from (with (select avg(a) from _table) as tt select count() - sum(a) from table2)', [('', '_table', ''), ('', 'table2', '')]),
        ('SELECT * FROM (\nSELECT * from `nytaxi`)', [('', 'nytaxi', '')]),
        ('SELECT * FROM tt FORMAT JSON', [('', 'tt', '')]),
        ('select count() c from test_table format JSON', [('', 'test_table', '')]),
        ('select count() c from (select * from t_dd5b58f544c84d8487eb65c23fc5e497 where a < 4) inner join (select * from joined where b > 3.0) using a', [('', 'joined', ''), ('', 't_dd5b58f544c84d8487eb65c23fc5e497', '')]),
        ('SELECT finalizeAggregation(( SELECT countState(id) FROM join_test ))', [('', 'join_test', '')]),
        ('SELECT arrayMap(x -> finalizeAggregation(x), state) FROM (SELECT sumStateResample(0, 20, 1)(id, id % 20) as state FROM default.join_test)', [('default', 'join_test', '')]),
        ('Select array(join_test.id) from join_test', [('', 'join_test', '')]),
        ('Select a::DateTime from join_test', [('', 'join_test', '')]),
        ('SELECT * FROM t WHERE event_date IN system.query_log', [('', 't', ''), ('system', 'query_log', '')]),
        ('SELECT * FROM t WHERE event_date GLOBAL NOT IN system.query_log', [('', 't', ''), ('system', 'query_log', '')]),
        ('SELECT * FROM t WHERE event_date IN (Select * FROM system.query_log)', [('', 't', ''), ('system', 'query_log', '')]),
    ]

    def test_extract_tables(self):
        for (sql, expected_tables) in self.scenarios:
            with self.subTest(sql=sql, expected_tables=expected_tables):
                self.assertEqual(chquery.tables(sql), expected_tables, sql)

    def test_extract_tables_default_database(self):
        for (sql, expected_tables) in self.scenarios:
            with self.subTest(sql=sql, expected_tables=expected_tables):
                self.assertEqual(chquery.tables(sql, default_database='d_012345'), [(t[0] or 'd_012345', t[1], '') for t in expected_tables], sql)

    def test_same_table_and_column_name(self):
        self.assertEqual(chquery.tables(
            "SELECT `cod_store`,`country_iso`,sum(stores_stock) as stores_stock from stores_stock group by `cod_store`,`country_iso`"),
            [('', 'stores_stock', '')])

    def test_has_column_in_table(self):
        with self.assertRaisesRegex(ValueError, """DB::Exception: Usage of function hasColumnInTable is restricted"""):
            chquery.tables("Select hasColumnInTable('default', 'join_test', 'id')")

        with self.assertRaisesRegex(ValueError, """DB::Exception: Usage of function hasColumnInTable is restricted"""):
            chquery.tables("Select hasColumnInTable('127.0.0.1', 'default', 'join_test', 'id')")

    def test_column_has_a_point(self):
        tables = chquery.tables("""
SELECT *
        FROM
            (
            SELECT
        timestamp,
        event_type,
        datasource_id,
        datasource_name,
        result,
        elapsed_time,
        error,
        Options.Names,
        Options.Values,
        request_id,
        import_id,
        job_id,
        rows,
        rows_quarantine,
        blocks_ids
        FROM public.t_107b846f32f5412186dabfe81bedde81
        WHERE user_id = 'de311728-f73b-4df9-9eae-06c74ceddae4'
        ) AS datasources_ops_log
""")
        self.assertEqual(tables, [('public', 't_107b846f32f5412186dabfe81bedde81', '')])

    def test_column_in(self):
        tables = chquery.tables("Select * FROM table WHERE c in (Select a from t2)")
        self.assertEqual(tables, [('', 't2', ''), ('', 'table', '')])

    def test_column_with_self_alias(self):
        tables = chquery.tables("Select * from a as b")
        self.assertEqual(tables, [('', 'a', '')])

        tables = chquery.tables("Select * from a as a")
        self.assertEqual(tables, [('', 'a', '')])

    def test_alias_across_subqueries_with_no_database(self):
        tables = chquery.tables("""
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
            """, default_database="d_1234")
        self.assertEqual(tables, [('', '', 'numbers'), ('d_1234', 't_6c64478e93d244e3ada26aff731e9e8c', '')])

    def test_alias_across_subqueries_with_inner_cte(self):
        tables = chquery.tables("""
            SELECT
                *
            FROM
            (
                SELECT * FROM ( WITH t1 AS (SELECT * FROM table) SELECT * FROM t1)
                UNION ALL
                SELECT * FROM t1
            )
            """, default_database="d_1234")
        self.assertEqual(sorted(tables), sorted([('d_1234', 'table', ''), ('d_1234', 't1', '')]))

    def test_reusing_the_same_alias(self):
        tables = chquery.tables("""
            SELECT
                *
            FROM
            (
                SELECT * FROM ( WITH t1 AS (SELECT * FROM table1) SELECT * FROM t1)
                UNION ALL
                SELECT * FROM ( WITH t1 AS (SELECT * FROM table2) SELECT * FROM t1)
            )
            """, default_database="d_1234")
        self.assertEqual(sorted(tables), sorted([('d_1234', 'table1', ''), ('d_1234', 'table2', '')]))

    def test_alias_across_union_all_with_no_database(self):
        tables = chquery.tables("""
            SELECT *
            FROM
            (
                SELECT * FROM t1 as t2
                UNION ALL
                SELECT * FROM t2
            ) t2
        """, default_database="d_1234")
        self.assertEqual(tables, [('d_1234', 't1', ''), ('d_1234', 't2', '')])

    def test_alias_down(self):
        tables = chquery.tables("""
            SELECT * FROM (SELECT * FROM t1 as t2) as t1
        """, default_database="d_1234")
        self.assertEqual(tables, [('d_1234', 't1', '')])

    def test_column_with_self_alias_with_database(self):
        tables = chquery.tables("Select * from system.tables as t")
        self.assertEqual(tables, [('system', 'tables', '')])

        tables = chquery.tables("Select * from system.tables as tables")
        self.assertEqual(tables, [('system', 'tables', '')])

        tables = chquery.tables("Select * from (Select 1 from numbers(1) as tables) as a, (select * from system.tables as a) limit 10")
        self.assertEqual(tables, [('', '', 'numbers'), ('system', 'tables', '')])

        tables = chquery.tables("Select * from (Select 1 from numbers(10) as cluster) as a, (select * from cluster('audiense', 'system.tables'))")
        self.assertEqual(sorted(tables), sorted([('system', 'tables', 'cluster'), ('', '', 'numbers')]))

    def test_cluster_returns_remote_table(self):
        tables = chquery.tables("Select * from cluster('tinybird', 'public', 't_107b846f32f5412186dabfe81bedde81')")
        self.assertEqual(tables, [('public', 't_107b846f32f5412186dabfe81bedde81', 'cluster')])

        tables = chquery.tables("Select * from cluster('tinybird', 'public.t_107b846f32f5412186dabfe81bedde81')")
        self.assertEqual(tables, [('public', 't_107b846f32f5412186dabfe81bedde81', 'cluster')])

        tables = chquery.tables("(select start_datetime,pipe_id,pipe_name,token,token_name,duration,read_bytes,read_rows,url,error,status_code,request_id from cluster(tinybird, test_public_ca7e05ad1bcf4e42a5626cc31f53a23c.t_65dae0349978482388c2000e8d5fdcb8) where user_id = '3fa32e18-b163-4e5f-9aeb-67d63bac91d8' AND billable = 1)")
        self.assertEqual(tables, [('test_public_ca7e05ad1bcf4e42a5626cc31f53a23c', 't_65dae0349978482388c2000e8d5fdcb8', 'cluster')])

        tables = chquery.tables("(select * from cluster(tinybird, test_public_ca7e05ad1bcf4e42a5626cc31f53a23c, t_65dae0349978482388c2000e8d5fdcb8) where user_id = '3fa32e18-b163-4e5f-9aeb-67d63bac91d8' AND billable = 1)")
        self.assertEqual(tables, [('test_public_ca7e05ad1bcf4e42a5626cc31f53a23c', 't_65dae0349978482388c2000e8d5fdcb8', 'cluster')])

        with self.assertRaisesRegex(ValueError, 'DB::Exception: Could not parse cluster table function arguments: .*'):
            chquery.tables("Select * from cluster()")

        with self.assertRaisesRegex(ValueError, 'DB::Exception: Could not parse cluster table function arguments: .*'):
            chquery.tables("Select * from cluster('tinybird')")

        with self.assertRaisesRegex(ValueError, 'DB::Exception: Could not parse cluster table function arguments: .*'):
            chquery.tables("Select * from cluster('tinybird', 'table')")

        with self.assertRaisesRegex(ValueError, 'DB::Exception: Could not parse cluster table function arguments: .*'):
            chquery.tables("Select * from cluster('tinybird', identifier)")

    def test_extract_tables_from_subquery_aliased_with_table_name(self):
        sql_alias = """
            SELECT *
            FROM
            (
                SELECT a, b, c
                FROM table_name
                WHERE d = 'foo'
            ) AS table_name
        """
        tables = chquery.tables(sql_alias)
        self.assertEqual(tables, [('', 'table_name', '')])

    def test_extract_tables_from_subquery_aliased_with_db_table_name(self):
        sql = """
            SELECT a, b, c
            FROM my_db.table_name
            WHERE d = 'foo'
        """
        tables = chquery.tables(sql)
        self.assertEqual(tables, [('my_db', 'table_name', '')])

        sql_alias = f"""
            SELECT *
            FROM ({sql}) AS table_name
        """
        tables = chquery.tables(sql_alias)
        self.assertEqual(tables, [('my_db', 'table_name', '')])

    def test_extract_tables_with_aliases(self):
        sql = """Select * from (Select 1 from numbers(10) as tables) as a, (select * from system.tables LIMIT 10)"""
        tables = chquery.tables(sql)
        self.assertEqual(tables, [('', '', 'numbers'), ('system', 'tables', '')])

        sql = """Select * from (Select 1 from numbers(10) as tables) as a, (select * from system.tables LIMIT 10)"""
        tables = chquery.tables(sql, default_database="d_1234567")
        self.assertEqual(tables, [('', '', 'numbers'), ('system', 'tables', '')])

    def test_function_tables(self):
        self.assertEqual(chquery.tables("SELECT * FROM numbers(10)", default_database='d_012345'), [('', '', 'numbers')])
        self.assertEqual(chquery.tables(
            """SELECT * FROM url('http://127.0.0.1:8123/?query=INSERT+INTO+test_table+FORMAT+CSV', 'CSV', 'column1 String, column2 UInt32')""",
            default_database='d_012345', function_allow_list=['url']), [('', '', 'url')])
        self.assertEqual(chquery.tables("SELECT * FROM remote('127.0.0.1:9000', 'system', 'tables', rand())",
                                        default_database='d_012345', function_allow_list=['remote']), [('system', 'tables', 'remote')])
        self.assertEqual(chquery.tables("SELECT * FROM numbers_mt(10)", default_database='d_012345'), [('', '', 'numbers_mt')])

    def test_mix_table_name_and_function_table(self):
        sql = "SELECT * FROM public.numbers, numbers(10)"
        self.assertEqual(sorted(chquery.tables(sql)), sorted([('public', 'numbers', ''), ('', '', 'numbers')]))

        sql = "SELECT * FROM numbers, numbers(10)"
        self.assertEqual(sorted(chquery.tables(sql)), sorted([('', 'numbers', ''), ('', '', 'numbers')]))

        sql = "SELECT * FROM numbers, numbers(10)"
        self.assertEqual(sorted(chquery.tables(sql, default_database='d_012345')),
                         sorted([('d_012345', 'numbers', ''), ('', '', 'numbers')]))

    def test_describe_query(self):
        sql = """
            DESCRIBE TABLE ((SELECT table.col FROM table))
        """
        self.assertEqual(chquery.tables(sql), [('', 'table', '')])

    def test_throws_with_invalid_query_types(self):
        queries = [
            "INSERT INTO test.table VALUES (1,2,3)",
            "RENAME DATABASE db_test TO db_test2",
            "SHOW DATABASES",
            "SHOW TABLES",
            "ALTER TABLE table_test ADD COLUMN column_test UInt32 FIRST",
            "CREATE TABLE table_test (`index` String) ENGINE = MergeTree ORDER BY index",
            "DROP TABLE test"
        ]
        for q in queries:
            with self.assertRaisesRegex(ValueError, 'Only SELECT or DESCRIBE queries are supported. Got: .*'):
                chquery.tables(q)

    def test_throws_with_invalid_functions(self):
        with self.assertRaisesRegex(ValueError, 'DB::Exception: Unknown function doesNotExist'):
            chquery.tables("SELECT doesNotExist(number) from numbers(100)")

        with self.assertRaisesRegex(ValueError, """DB::Exception: Unknown function numbers2. Maybe you meant: \\['numbers','numbers_mt'\\]"""):
            chquery.tables("SELECT sum(number) from numbers2(100)")

        with self.assertRaisesRegex(ValueError, """DB::Exception: Unknown function avgg. Maybe you meant: \\['avg','SVG','age'\\]"""):
            chquery.tables("SELECT avgg(number) from numbers(100)")

    def test_throws_with_view(self):
        with self.assertRaisesRegex(ValueError, """DB::Exception: Usage of function view is restricted"""):
            chquery.tables("SELECT * FROM view(SELECT 1)")

        with self.assertRaisesRegex(ValueError, """DB::Exception: Usage of function viewIfPermitted is restricted"""):
            chquery.tables("SELECT * FROM viewIfPermitted(SELECT * FROM table1 ELSE null('x UInt32'))")

        # Implicit viewExplain
        with self.assertRaisesRegex(ValueError, """DB::Exception: Usage of function viewExplain is restricted"""):
            chquery.tables("SELECT * FROM (EXPLAIN PLAN header = 1 SELECT number FROM numbers(10))")

    def test_works_with_functions_from_plugins(self):
        self.assertEqual(chquery.tables("SELECT h3IsValid(number) from numbers(100)"), [('', '', 'numbers')])

    def test_works_with_random_case_functions(self):
        self.assertEqual(chquery.tables("SELECT AVG(number) from numbers(1)"), [('', '', 'numbers')])
        self.assertEqual(chquery.tables("SELECT Avg(number) from numbers(1)"), [('', '', 'numbers')])
        self.assertEqual(chquery.tables("SELECT Hour(now()) from numbers(1)"), [('', '', 'numbers')])
        self.assertEqual(chquery.tables("SELECT Hour(now()) from numbers(1)"), [('', '', 'numbers')])
        self.assertEqual(chquery.tables("SELECT CONCAT('a', 'b') from numbers(1)"), [('', '', 'numbers')])
        self.assertEqual(chquery.tables("SELECT NOW() from numbers(1)"), [('', '', 'numbers')])
        self.assertEqual(chquery.tables("SELECT IFNULL(number, 0) from numbers(1)"), [('', '', 'numbers')])
        self.assertEqual(chquery.tables("SELECT IF(number == 0, number, 0) from numbers(1)"), [('', '', 'numbers')])

        self.assertEqual(chquery.tables("""select * from (SELECT
                                            toISOWeek(survey_date) week,
                                            avgWeighted(1, weight)
                                            gender
                                            from rvu_2020
                                            group by week, gender
                                            ) LIMIT 20
                                            FORMAT JSON"""),
                         [('', 'rvu_2020', '')])

        # Check some aliases
        self.assertEqual(chquery.tables("SELECT BIT_AND(number) from numbers(1)"), [('', '', 'numbers')])
        self.assertEqual(chquery.tables("SELECT groupBitAnd(number) from numbers(1)"), [('', '', 'numbers')])

    def test_all_functions(self):
        """
        Extracted by listing all CH functions and removing some causing issues (special functions):

            ./clickhouse local --query "SELECT * FROM (Select name, case_insensitive, false as table_function from system.functions where name not in ['CAST'] UNION ALL (Select name, false, true as table_function from system.table_functions)) order by name format NDJSON;" | awk '{print $0 ","}' | sed -e  's/false/False/g;s/true/True/g'
        """
        CH_FUNCTIONS = [{"name":"BIT_AND","case_insensitive":1,"table_function":False},
                        {"name":"BIT_OR","case_insensitive":1,"table_function":False},
                        {"name":"BIT_XOR","case_insensitive":1,"table_function":False},
                        {"name":"BLAKE3","case_insensitive":0,"table_function":False},
                        {"name":"CHARACTER_LENGTH","case_insensitive":1,"table_function":False},
                        {"name":"CHAR_LENGTH","case_insensitive":1,"table_function":False},
                        {"name":"COVAR_POP","case_insensitive":1,"table_function":False},
                        {"name":"COVAR_SAMP","case_insensitive":1,"table_function":False},
                        {"name":"CRC32","case_insensitive":1,"table_function":False},
                        {"name":"CRC32IEEE","case_insensitive":1,"table_function":False},
                        {"name":"CRC64","case_insensitive":1,"table_function":False},
                        {"name":"DATABASE","case_insensitive":1,"table_function":False},
                        {"name":"DATE","case_insensitive":1,"table_function":False},
                        {"name":"DATE_DIFF","case_insensitive":0,"table_function":False},
                        {"name":"DATE_FORMAT","case_insensitive":0,"table_function":False},
                        {"name":"DATE_TRUNC","case_insensitive":1,"table_function":False},
                        {"name":"DAY","case_insensitive":1,"table_function":False},
                        {"name":"DAYOFMONTH","case_insensitive":1,"table_function":False},
                        {"name":"DAYOFWEEK","case_insensitive":1,"table_function":False},
                        {"name":"DAYOFYEAR","case_insensitive":1,"table_function":False},
                        {"name":"FORMAT_BYTES","case_insensitive":1,"table_function":False},
                        {"name":"FQDN","case_insensitive":1,"table_function":False},
                        {"name":"FROM_BASE64","case_insensitive":1,"table_function":False},
                        {"name":"FROM_DAYS","case_insensitive":1,"table_function":False},
                        {"name":"FROM_UNIXTIME","case_insensitive":0,"table_function":False},
                        {"name":"HOUR","case_insensitive":1,"table_function":False},
                        {"name":"INET6_ATON","case_insensitive":1,"table_function":False},
                        {"name":"INET6_NTOA","case_insensitive":1,"table_function":False},
                        {"name":"INET_ATON","case_insensitive":1,"table_function":False},
                        {"name":"INET_NTOA","case_insensitive":1,"table_function":False},
                        {"name":"IPv4CIDRToRange","case_insensitive":0,"table_function":False},
                        {"name":"IPv4NumToString","case_insensitive":0,"table_function":False},
                        {"name":"IPv4NumToStringClassC","case_insensitive":0,"table_function":False},
                        {"name":"IPv4StringToNum","case_insensitive":0,"table_function":False},
                        {"name":"IPv4StringToNumOrDefault","case_insensitive":0,"table_function":False},
                        {"name":"IPv4StringToNumOrNull","case_insensitive":0,"table_function":False},
                        {"name":"IPv4ToIPv6","case_insensitive":0,"table_function":False},
                        {"name":"IPv6CIDRToRange","case_insensitive":0,"table_function":False},
                        {"name":"IPv6NumToString","case_insensitive":0,"table_function":False},
                        {"name":"IPv6StringToNum","case_insensitive":0,"table_function":False},
                        {"name":"IPv6StringToNumOrDefault","case_insensitive":0,"table_function":False},
                        {"name":"IPv6StringToNumOrNull","case_insensitive":0,"table_function":False},
                        {"name":"JSONArrayLength","case_insensitive":0,"table_function":False},
                        {"name":"JSONExtract","case_insensitive":0,"table_function":False},
                        {"name":"JSONExtractArrayRaw","case_insensitive":0,"table_function":False},
                        {"name":"JSONExtractBool","case_insensitive":0,"table_function":False},
                        {"name":"JSONExtractFloat","case_insensitive":0,"table_function":False},
                        {"name":"JSONExtractInt","case_insensitive":0,"table_function":False},
                        {"name":"JSONExtractKeys","case_insensitive":0,"table_function":False},
                        {"name":"JSONExtractKeysAndValues","case_insensitive":0,"table_function":False},
                        {"name":"JSONExtractKeysAndValuesRaw","case_insensitive":0,"table_function":False},
                        {"name":"JSONExtractRaw","case_insensitive":0,"table_function":False},
                        {"name":"JSONExtractString","case_insensitive":0,"table_function":False},
                        {"name":"JSONExtractUInt","case_insensitive":0,"table_function":False},
                        {"name":"JSONHas","case_insensitive":0,"table_function":False},
                        {"name":"JSONKey","case_insensitive":0,"table_function":False},
                        {"name":"JSONLength","case_insensitive":0,"table_function":False},
                        {"name":"JSONType","case_insensitive":0,"table_function":False},
                        {"name":"JSON_ARRAY_LENGTH","case_insensitive":1,"table_function":False},
                        {"name":"JSON_EXISTS","case_insensitive":0,"table_function":False},
                        {"name":"JSON_QUERY","case_insensitive":0,"table_function":False},
                        {"name":"JSON_VALUE","case_insensitive":0,"table_function":False},
                        {"name":"L1Distance","case_insensitive":0,"table_function":False},
                        {"name":"L1Norm","case_insensitive":0,"table_function":False},
                        {"name":"L1Normalize","case_insensitive":0,"table_function":False},
                        {"name":"L2Distance","case_insensitive":0,"table_function":False},
                        {"name":"L2Norm","case_insensitive":0,"table_function":False},
                        {"name":"L2Normalize","case_insensitive":0,"table_function":False},
                        {"name":"L2SquaredDistance","case_insensitive":0,"table_function":False},
                        {"name":"L2SquaredNorm","case_insensitive":0,"table_function":False},
                        {"name":"LAST_DAY","case_insensitive":1,"table_function":False},
                        {"name":"LinfDistance","case_insensitive":0,"table_function":False},
                        {"name":"LinfNorm","case_insensitive":0,"table_function":False},
                        {"name":"LinfNormalize","case_insensitive":0,"table_function":False},
                        {"name":"LpDistance","case_insensitive":0,"table_function":False},
                        {"name":"LpNorm","case_insensitive":0,"table_function":False},
                        {"name":"LpNormalize","case_insensitive":0,"table_function":False},
                        {"name":"MACNumToString","case_insensitive":0,"table_function":False},
                        {"name":"MACStringToNum","case_insensitive":0,"table_function":False},
                        {"name":"MACStringToOUI","case_insensitive":0,"table_function":False},
                        {"name":"MAP_FROM_ARRAYS","case_insensitive":0,"table_function":False},
                        {"name":"MD4","case_insensitive":0,"table_function":False},
                        {"name":"MD5","case_insensitive":0,"table_function":False},
                        {"name":"MINUTE","case_insensitive":1,"table_function":False},
                        {"name":"MONTH","case_insensitive":1,"table_function":False},
                        {"name":"OCTET_LENGTH","case_insensitive":1,"table_function":False},
                        {"name":"QUARTER","case_insensitive":1,"table_function":False},
                        {"name":"REGEXP_EXTRACT","case_insensitive":1,"table_function":False},
                        {"name":"REGEXP_MATCHES","case_insensitive":1,"table_function":False},
                        {"name":"REGEXP_REPLACE","case_insensitive":1,"table_function":False},
                        {"name":"SCHEMA","case_insensitive":1,"table_function":False},
                        {"name":"SECOND","case_insensitive":1,"table_function":False},
                        {"name":"SHA1","case_insensitive":0,"table_function":False},
                        {"name":"SHA224","case_insensitive":0,"table_function":False},
                        {"name":"SHA256","case_insensitive":0,"table_function":False},
                        {"name":"SHA384","case_insensitive":0,"table_function":False},
                        {"name":"SHA512","case_insensitive":0,"table_function":False},
                        {"name":"SHA512_256","case_insensitive":0,"table_function":False},
                        {"name":"STD","case_insensitive":1,"table_function":False},
                        {"name":"STDDEV_POP","case_insensitive":1,"table_function":False},
                        {"name":"STDDEV_SAMP","case_insensitive":1,"table_function":False},
                        {"name":"SUBSTRING_INDEX","case_insensitive":1,"table_function":False},
                        {"name":"SVG","case_insensitive":0,"table_function":False},
                        {"name":"TIMESTAMP_DIFF","case_insensitive":0,"table_function":False},
                        {"name":"TO_BASE64","case_insensitive":1,"table_function":False},
                        {"name":"TO_DAYS","case_insensitive":1,"table_function":False},
                        {"name":"TO_UNIXTIME","case_insensitive":0,"table_function":False},
                        {"name":"ULIDStringToDateTime","case_insensitive":0,"table_function":False},
                        {"name":"URLHash","case_insensitive":0,"table_function":False},
                        {"name":"URLHierarchy","case_insensitive":0,"table_function":False},
                        {"name":"URLPathHierarchy","case_insensitive":0,"table_function":False},
                        {"name":"UTCTimestamp","case_insensitive":1,"table_function":False},
                        {"name":"UTC_timestamp","case_insensitive":1,"table_function":False},
                        {"name":"UUIDNumToString","case_insensitive":0,"table_function":False},
                        {"name":"UUIDStringToNum","case_insensitive":0,"table_function":False},
                        {"name":"VAR_POP","case_insensitive":1,"table_function":False},
                        {"name":"VAR_SAMP","case_insensitive":1,"table_function":False},
                        {"name":"YEAR","case_insensitive":1,"table_function":False},
                        {"name":"YYYYMMDDToDate","case_insensitive":0,"table_function":False},
                        {"name":"YYYYMMDDToDate32","case_insensitive":0,"table_function":False},
                        {"name":"YYYYMMDDhhmmssToDateTime","case_insensitive":0,"table_function":False},
                        {"name":"YYYYMMDDhhmmssToDateTime64","case_insensitive":0,"table_function":False},
                        {"name":"_CAST","case_insensitive":1,"table_function":False},
                        {"name":"__bitBoolMaskAnd","case_insensitive":0,"table_function":False},
                        {"name":"__bitBoolMaskOr","case_insensitive":0,"table_function":False},
                        {"name":"__bitSwapLastTwo","case_insensitive":0,"table_function":False},
                        {"name":"__bitWrapperFunc","case_insensitive":0,"table_function":False},
                        {"name":"__getScalar","case_insensitive":0,"table_function":False},
                        {"name":"abs","case_insensitive":1,"table_function":False},
                        {"name":"accurateCast","case_insensitive":0,"table_function":False},
                        {"name":"accurateCastOrDefault","case_insensitive":0,"table_function":False},
                        {"name":"accurateCastOrNull","case_insensitive":0,"table_function":False},
                        {"name":"acos","case_insensitive":1,"table_function":False},
                        {"name":"acosh","case_insensitive":0,"table_function":False},
                        {"name":"addDate","case_insensitive":1,"table_function":False},
                        {"name":"addDays","case_insensitive":0,"table_function":False},
                        {"name":"addHours","case_insensitive":0,"table_function":False},
                        {"name":"addInterval","case_insensitive":0,"table_function":False},
                        {"name":"addMicroseconds","case_insensitive":0,"table_function":False},
                        {"name":"addMilliseconds","case_insensitive":0,"table_function":False},
                        {"name":"addMinutes","case_insensitive":0,"table_function":False},
                        {"name":"addMonths","case_insensitive":0,"table_function":False},
                        {"name":"addNanoseconds","case_insensitive":0,"table_function":False},
                        {"name":"addQuarters","case_insensitive":0,"table_function":False},
                        {"name":"addSeconds","case_insensitive":0,"table_function":False},
                        {"name":"addTupleOfIntervals","case_insensitive":0,"table_function":False},
                        {"name":"addWeeks","case_insensitive":0,"table_function":False},
                        {"name":"addYears","case_insensitive":0,"table_function":False},
                        {"name":"addressToLine","case_insensitive":0,"table_function":False},
                        {"name":"addressToLineWithInlines","case_insensitive":0,"table_function":False},
                        {"name":"addressToSymbol","case_insensitive":0,"table_function":False},
                        {"name":"aes_decrypt_mysql","case_insensitive":0,"table_function":False},
                        {"name":"aes_encrypt_mysql","case_insensitive":0,"table_function":False},
                        {"name":"age","case_insensitive":1,"table_function":False},
                        {"name":"aggThrow","case_insensitive":0,"table_function":False},
                        {"name":"alphaTokens","case_insensitive":0,"table_function":False},
                        {"name":"analysisOfVariance","case_insensitive":1,"table_function":False},
                        {"name":"and","case_insensitive":0,"table_function":False},
                        {"name":"anova","case_insensitive":1,"table_function":False},
                        {"name":"any","case_insensitive":0,"table_function":False},
                        {"name":"anyHeavy","case_insensitive":0,"table_function":False},
                        {"name":"anyLast","case_insensitive":0,"table_function":False},
                        {"name":"anyLast_respect_nulls","case_insensitive":0,"table_function":False},
                        {"name":"any_respect_nulls","case_insensitive":0,"table_function":False},
                        {"name":"any_value","case_insensitive":1,"table_function":False},
                        {"name":"any_value_respect_nulls","case_insensitive":1,"table_function":False},
                        {"name":"appendTrailingCharIfAbsent","case_insensitive":0,"table_function":False},
                        {"name":"argMax","case_insensitive":0,"table_function":False},
                        {"name":"argMin","case_insensitive":0,"table_function":False},
                        {"name":"array","case_insensitive":0,"table_function":False},
                        {"name":"arrayAUC","case_insensitive":0,"table_function":False},
                        {"name":"arrayAll","case_insensitive":0,"table_function":False},
                        {"name":"arrayAvg","case_insensitive":0,"table_function":False},
                        {"name":"arrayCompact","case_insensitive":0,"table_function":False},
                        {"name":"arrayConcat","case_insensitive":0,"table_function":False},
                        {"name":"arrayCount","case_insensitive":0,"table_function":False},
                        {"name":"arrayCumSum","case_insensitive":0,"table_function":False},
                        {"name":"arrayCumSumNonNegative","case_insensitive":0,"table_function":False},
                        {"name":"arrayDifference","case_insensitive":0,"table_function":False},
                        {"name":"arrayDistinct","case_insensitive":0,"table_function":False},
                        {"name":"arrayDotProduct","case_insensitive":0,"table_function":False},
                        {"name":"arrayElement","case_insensitive":0,"table_function":False},
                        {"name":"arrayEnumerate","case_insensitive":0,"table_function":False},
                        {"name":"arrayEnumerateDense","case_insensitive":0,"table_function":False},
                        {"name":"arrayEnumerateDenseRanked","case_insensitive":0,"table_function":False},
                        {"name":"arrayEnumerateUniq","case_insensitive":0,"table_function":False},
                        {"name":"arrayEnumerateUniqRanked","case_insensitive":0,"table_function":False},
                        {"name":"arrayExists","case_insensitive":0,"table_function":False},
                        {"name":"arrayFill","case_insensitive":0,"table_function":False},
                        {"name":"arrayFilter","case_insensitive":0,"table_function":False},
                        {"name":"arrayFirst","case_insensitive":0,"table_function":False},
                        {"name":"arrayFirstIndex","case_insensitive":0,"table_function":False},
                        {"name":"arrayFirstOrNull","case_insensitive":0,"table_function":False},
                        {"name":"arrayFlatten","case_insensitive":0,"table_function":False},
                        {"name":"arrayFold","case_insensitive":0,"table_function":False},
                        {"name":"arrayIntersect","case_insensitive":0,"table_function":False},
                        {"name":"arrayJaccardIndex","case_insensitive":0,"table_function":False},
                        {"name":"arrayJoin","case_insensitive":0,"table_function":False},
                        {"name":"arrayLast","case_insensitive":0,"table_function":False},
                        {"name":"arrayLastIndex","case_insensitive":0,"table_function":False},
                        {"name":"arrayLastOrNull","case_insensitive":0,"table_function":False},
                        {"name":"arrayMap","case_insensitive":0,"table_function":False},
                        {"name":"arrayMax","case_insensitive":0,"table_function":False},
                        {"name":"arrayMin","case_insensitive":0,"table_function":False},
                        {"name":"arrayPartialReverseSort","case_insensitive":0,"table_function":False},
                        {"name":"arrayPartialShuffle","case_insensitive":1,"table_function":False},
                        {"name":"arrayPartialSort","case_insensitive":0,"table_function":False},
                        {"name":"arrayPopBack","case_insensitive":0,"table_function":False},
                        {"name":"arrayPopFront","case_insensitive":0,"table_function":False},
                        {"name":"arrayProduct","case_insensitive":0,"table_function":False},
                        {"name":"arrayPushBack","case_insensitive":0,"table_function":False},
                        {"name":"arrayPushFront","case_insensitive":0,"table_function":False},
                        {"name":"arrayRandomSample","case_insensitive":0,"table_function":False},
                        {"name":"arrayReduce","case_insensitive":0,"table_function":False},
                        {"name":"arrayReduceInRanges","case_insensitive":0,"table_function":False},
                        {"name":"arrayResize","case_insensitive":0,"table_function":False},
                        {"name":"arrayReverse","case_insensitive":0,"table_function":False},
                        {"name":"arrayReverseFill","case_insensitive":0,"table_function":False},
                        {"name":"arrayReverseSort","case_insensitive":0,"table_function":False},
                        {"name":"arrayReverseSplit","case_insensitive":0,"table_function":False},
                        {"name":"arrayRotateLeft","case_insensitive":0,"table_function":False},
                        {"name":"arrayRotateRight","case_insensitive":0,"table_function":False},
                        {"name":"arrayShiftLeft","case_insensitive":0,"table_function":False},
                        {"name":"arrayShiftRight","case_insensitive":0,"table_function":False},
                        {"name":"arrayShingles","case_insensitive":0,"table_function":False},
                        {"name":"arrayShuffle","case_insensitive":1,"table_function":False},
                        {"name":"arraySlice","case_insensitive":0,"table_function":False},
                        {"name":"arraySort","case_insensitive":0,"table_function":False},
                        {"name":"arraySplit","case_insensitive":0,"table_function":False},
                        {"name":"arrayStringConcat","case_insensitive":0,"table_function":False},
                        {"name":"arraySum","case_insensitive":0,"table_function":False},
                        {"name":"arrayUniq","case_insensitive":0,"table_function":False},
                        {"name":"arrayWithConstant","case_insensitive":0,"table_function":False},
                        {"name":"arrayZip","case_insensitive":0,"table_function":False},
                        {"name":"array_agg","case_insensitive":1,"table_function":False},
                        {"name":"array_concat_agg","case_insensitive":1,"table_function":False},
                        {"name":"ascii","case_insensitive":1,"table_function":False},
                        {"name":"asin","case_insensitive":1,"table_function":False},
                        {"name":"asinh","case_insensitive":0,"table_function":False},
                        {"name":"assumeNotNull","case_insensitive":0,"table_function":False},
                        {"name":"atan","case_insensitive":1,"table_function":False},
                        {"name":"atan2","case_insensitive":1,"table_function":False},
                        {"name":"atanh","case_insensitive":0,"table_function":False},
                        {"name":"avg","case_insensitive":1,"table_function":False},
                        {"name":"avgWeighted","case_insensitive":0,"table_function":False},
                        {"name":"azureBlobStorage","case_insensitive":0,"table_function":True},
                        {"name":"azureBlobStorageCluster","case_insensitive":0,"table_function":True},
                        {"name":"bar","case_insensitive":0,"table_function":False},
                        {"name":"base58Decode","case_insensitive":0,"table_function":False},
                        {"name":"base58Encode","case_insensitive":0,"table_function":False},
                        {"name":"base64Decode","case_insensitive":0,"table_function":False},
                        {"name":"base64Encode","case_insensitive":0,"table_function":False},
                        {"name":"basename","case_insensitive":0,"table_function":False},
                        {"name":"bin","case_insensitive":1,"table_function":False},
                        {"name":"bitAnd","case_insensitive":0,"table_function":False},
                        {"name":"bitCount","case_insensitive":0,"table_function":False},
                        {"name":"bitHammingDistance","case_insensitive":0,"table_function":False},
                        {"name":"bitNot","case_insensitive":0,"table_function":False},
                        {"name":"bitOr","case_insensitive":0,"table_function":False},
                        {"name":"bitPositionsToArray","case_insensitive":0,"table_function":False},
                        {"name":"bitRotateLeft","case_insensitive":0,"table_function":False},
                        {"name":"bitRotateRight","case_insensitive":0,"table_function":False},
                        {"name":"bitShiftLeft","case_insensitive":0,"table_function":False},
                        {"name":"bitShiftRight","case_insensitive":0,"table_function":False},
                        {"name":"bitSlice","case_insensitive":0,"table_function":False},
                        {"name":"bitTest","case_insensitive":0,"table_function":False},
                        {"name":"bitTestAll","case_insensitive":0,"table_function":False},
                        {"name":"bitTestAny","case_insensitive":0,"table_function":False},
                        {"name":"bitXor","case_insensitive":0,"table_function":False},
                        {"name":"bitmapAnd","case_insensitive":0,"table_function":False},
                        {"name":"bitmapAndCardinality","case_insensitive":0,"table_function":False},
                        {"name":"bitmapAndnot","case_insensitive":0,"table_function":False},
                        {"name":"bitmapAndnotCardinality","case_insensitive":0,"table_function":False},
                        {"name":"bitmapBuild","case_insensitive":0,"table_function":False},
                        {"name":"bitmapCardinality","case_insensitive":0,"table_function":False},
                        {"name":"bitmapContains","case_insensitive":0,"table_function":False},
                        {"name":"bitmapHasAll","case_insensitive":0,"table_function":False},
                        {"name":"bitmapHasAny","case_insensitive":0,"table_function":False},
                        {"name":"bitmapMax","case_insensitive":0,"table_function":False},
                        {"name":"bitmapMin","case_insensitive":0,"table_function":False},
                        {"name":"bitmapOr","case_insensitive":0,"table_function":False},
                        {"name":"bitmapOrCardinality","case_insensitive":0,"table_function":False},
                        {"name":"bitmapSubsetInRange","case_insensitive":0,"table_function":False},
                        {"name":"bitmapSubsetLimit","case_insensitive":0,"table_function":False},
                        {"name":"bitmapToArray","case_insensitive":0,"table_function":False},
                        {"name":"bitmapTransform","case_insensitive":0,"table_function":False},
                        {"name":"bitmapXor","case_insensitive":0,"table_function":False},
                        {"name":"bitmapXorCardinality","case_insensitive":0,"table_function":False},
                        {"name":"bitmaskToArray","case_insensitive":0,"table_function":False},
                        {"name":"bitmaskToList","case_insensitive":0,"table_function":False},
                        {"name":"blockNumber","case_insensitive":0,"table_function":False},
                        {"name":"blockSerializedSize","case_insensitive":0,"table_function":False},
                        {"name":"blockSize","case_insensitive":0,"table_function":False},
                        {"name":"boundingRatio","case_insensitive":0,"table_function":False},
                        {"name":"buildId","case_insensitive":0,"table_function":False},
                        {"name":"byteHammingDistance","case_insensitive":0,"table_function":False},
                        {"name":"byteSize","case_insensitive":0,"table_function":False},
                        {"name":"byteSwap","case_insensitive":1,"table_function":False},
                        {"name":"caseWithExpr","case_insensitive":0,"table_function":False},
                        {"name":"caseWithExpression","case_insensitive":0,"table_function":False},
                        {"name":"caseWithoutExpr","case_insensitive":0,"table_function":False},
                        {"name":"caseWithoutExpression","case_insensitive":0,"table_function":False},
                        {"name":"catboostEvaluate","case_insensitive":0,"table_function":False},
                        {"name":"categoricalInformationValue","case_insensitive":0,"table_function":False},
                        {"name":"cbrt","case_insensitive":0,"table_function":False},
                        {"name":"ceil","case_insensitive":1,"table_function":False},
                        {"name":"ceiling","case_insensitive":1,"table_function":False},
                        {"name":"char","case_insensitive":1,"table_function":False},
                        {"name":"cityHash64","case_insensitive":0,"table_function":False},
                        {"name":"cluster","case_insensitive":0,"table_function":True},
                        {"name":"clusterAllReplicas","case_insensitive":0,"table_function":True},
                        {"name":"coalesce","case_insensitive":1,"table_function":False},
                        {"name":"concat","case_insensitive":1,"table_function":False},
                        {"name":"concatAssumeInjective","case_insensitive":0,"table_function":False},
                        {"name":"concatWithSeparator","case_insensitive":0,"table_function":False},
                        {"name":"concatWithSeparatorAssumeInjective","case_insensitive":0,"table_function":False},
                        {"name":"concat_ws","case_insensitive":1,"table_function":False},
                        {"name":"connectionId","case_insensitive":1,"table_function":False},
                        {"name":"connection_id","case_insensitive":1,"table_function":False},
                        {"name":"contingency","case_insensitive":0,"table_function":False},
                        {"name":"convertCharset","case_insensitive":0,"table_function":False},
                        {"name":"corr","case_insensitive":1,"table_function":False},
                        {"name":"corrMatrix","case_insensitive":0,"table_function":False},
                        {"name":"corrStable","case_insensitive":0,"table_function":False},
                        {"name":"cos","case_insensitive":1,"table_function":False},
                        {"name":"cosh","case_insensitive":0,"table_function":False},
                        {"name":"cosineDistance","case_insensitive":0,"table_function":False},
                        {"name":"cosn","case_insensitive":0,"table_function":True},
                        {"name":"count","case_insensitive":1,"table_function":False},
                        {"name":"countDigits","case_insensitive":0,"table_function":False},
                        {"name":"countEqual","case_insensitive":0,"table_function":False},
                        {"name":"countMatches","case_insensitive":0,"table_function":False},
                        {"name":"countMatchesCaseInsensitive","case_insensitive":0,"table_function":False},
                        {"name":"countSubstrings","case_insensitive":1,"table_function":False},
                        {"name":"countSubstringsCaseInsensitive","case_insensitive":0,"table_function":False},
                        {"name":"countSubstringsCaseInsensitiveUTF8","case_insensitive":0,"table_function":False},
                        {"name":"covarPop","case_insensitive":0,"table_function":False},
                        {"name":"covarPopMatrix","case_insensitive":0,"table_function":False},
                        {"name":"covarPopStable","case_insensitive":0,"table_function":False},
                        {"name":"covarSamp","case_insensitive":0,"table_function":False},
                        {"name":"covarSampMatrix","case_insensitive":0,"table_function":False},
                        {"name":"covarSampStable","case_insensitive":0,"table_function":False},
                        {"name":"cramersV","case_insensitive":0,"table_function":False},
                        {"name":"cramersVBiasCorrected","case_insensitive":0,"table_function":False},
                        {"name":"curdate","case_insensitive":1,"table_function":False},
                        {"name":"currentDatabase","case_insensitive":0,"table_function":False},
                        {"name":"currentProfiles","case_insensitive":0,"table_function":False},
                        {"name":"currentRoles","case_insensitive":0,"table_function":False},
                        {"name":"currentSchemas","case_insensitive":1,"table_function":False},
                        {"name":"currentUser","case_insensitive":0,"table_function":False},
                        {"name":"current_database","case_insensitive":1,"table_function":False},
                        {"name":"current_date","case_insensitive":1,"table_function":False},
                        {"name":"current_schemas","case_insensitive":1,"table_function":False},
                        {"name":"current_timestamp","case_insensitive":1,"table_function":False},
                        {"name":"cutFragment","case_insensitive":0,"table_function":False},
                        {"name":"cutIPv6","case_insensitive":0,"table_function":False},
                        {"name":"cutQueryString","case_insensitive":0,"table_function":False},
                        {"name":"cutQueryStringAndFragment","case_insensitive":0,"table_function":False},
                        {"name":"cutToFirstSignificantSubdomain","case_insensitive":0,"table_function":False},
                        {"name":"cutToFirstSignificantSubdomainCustom","case_insensitive":0,"table_function":False},
                        {"name":"cutToFirstSignificantSubdomainCustomRFC","case_insensitive":0,"table_function":False},
                        {"name":"cutToFirstSignificantSubdomainCustomWithWWW","case_insensitive":0,"table_function":False},
                        {"name":"cutToFirstSignificantSubdomainCustomWithWWWRFC","case_insensitive":0,"table_function":False},
                        {"name":"cutToFirstSignificantSubdomainRFC","case_insensitive":0,"table_function":False},
                        {"name":"cutToFirstSignificantSubdomainWithWWW","case_insensitive":0,"table_function":False},
                        {"name":"cutToFirstSignificantSubdomainWithWWWRFC","case_insensitive":0,"table_function":False},
                        {"name":"cutURLParameter","case_insensitive":0,"table_function":False},
                        {"name":"cutWWW","case_insensitive":0,"table_function":False},
                        {"name":"damerauLevenshteinDistance","case_insensitive":0,"table_function":False},
                        {"name":"dateDiff","case_insensitive":1,"table_function":False},
                        {"name":"dateName","case_insensitive":1,"table_function":False},
                        {"name":"dateTime64ToSnowflake","case_insensitive":0,"table_function":False},
                        {"name":"dateTimeToSnowflake","case_insensitive":0,"table_function":False},
                        {"name":"dateTrunc","case_insensitive":0,"table_function":False},
                        {"name":"date_diff","case_insensitive":0,"table_function":False},
                        {"name":"decodeHTMLComponent","case_insensitive":0,"table_function":False},
                        {"name":"decodeURLComponent","case_insensitive":0,"table_function":False},
                        {"name":"decodeURLFormComponent","case_insensitive":0,"table_function":False},
                        {"name":"decodeXMLComponent","case_insensitive":0,"table_function":False},
                        {"name":"decrypt","case_insensitive":0,"table_function":False},
                        {"name":"defaultProfiles","case_insensitive":0,"table_function":False},
                        {"name":"defaultRoles","case_insensitive":0,"table_function":False},
                        {"name":"defaultValueOfArgumentType","case_insensitive":0,"table_function":False},
                        {"name":"defaultValueOfTypeName","case_insensitive":0,"table_function":False},
                        {"name":"degrees","case_insensitive":1,"table_function":False},
                        {"name":"deltaLake","case_insensitive":0,"table_function":True},
                        {"name":"deltaSum","case_insensitive":0,"table_function":False},
                        {"name":"deltaSumTimestamp","case_insensitive":0,"table_function":False},
                        {"name":"demangle","case_insensitive":0,"table_function":False},
                        {"name":"dense_rank","case_insensitive":1,"table_function":False},
                        {"name":"detectCharset","case_insensitive":0,"table_function":False},
                        {"name":"detectLanguage","case_insensitive":0,"table_function":False},
                        {"name":"detectLanguageMixed","case_insensitive":0,"table_function":False},
                        {"name":"detectLanguageUnknown","case_insensitive":0,"table_function":False},
                        {"name":"detectProgrammingLanguage","case_insensitive":0,"table_function":False},
                        {"name":"detectTonality","case_insensitive":0,"table_function":False},
                        {"name":"dictGet","case_insensitive":0,"table_function":False},
                        {"name":"dictGetAll","case_insensitive":0,"table_function":False},
                        {"name":"dictGetChildren","case_insensitive":0,"table_function":False},
                        {"name":"dictGetDate","case_insensitive":0,"table_function":False},
                        {"name":"dictGetDateOrDefault","case_insensitive":0,"table_function":False},
                        {"name":"dictGetDateTime","case_insensitive":0,"table_function":False},
                        {"name":"dictGetDateTimeOrDefault","case_insensitive":0,"table_function":False},
                        {"name":"dictGetDescendants","case_insensitive":0,"table_function":False},
                        {"name":"dictGetFloat32","case_insensitive":0,"table_function":False},
                        {"name":"dictGetFloat32OrDefault","case_insensitive":0,"table_function":False},
                        {"name":"dictGetFloat64","case_insensitive":0,"table_function":False},
                        {"name":"dictGetFloat64OrDefault","case_insensitive":0,"table_function":False},
                        {"name":"dictGetHierarchy","case_insensitive":0,"table_function":False},
                        {"name":"dictGetIPv4","case_insensitive":0,"table_function":False},
                        {"name":"dictGetIPv4OrDefault","case_insensitive":0,"table_function":False},
                        {"name":"dictGetIPv6","case_insensitive":0,"table_function":False},
                        {"name":"dictGetIPv6OrDefault","case_insensitive":0,"table_function":False},
                        {"name":"dictGetInt16","case_insensitive":0,"table_function":False},
                        {"name":"dictGetInt16OrDefault","case_insensitive":0,"table_function":False},
                        {"name":"dictGetInt32","case_insensitive":0,"table_function":False},
                        {"name":"dictGetInt32OrDefault","case_insensitive":0,"table_function":False},
                        {"name":"dictGetInt64","case_insensitive":0,"table_function":False},
                        {"name":"dictGetInt64OrDefault","case_insensitive":0,"table_function":False},
                        {"name":"dictGetInt8","case_insensitive":0,"table_function":False},
                        {"name":"dictGetInt8OrDefault","case_insensitive":0,"table_function":False},
                        {"name":"dictGetOrDefault","case_insensitive":0,"table_function":False},
                        {"name":"dictGetOrNull","case_insensitive":0,"table_function":False},
                        {"name":"dictGetString","case_insensitive":0,"table_function":False},
                        {"name":"dictGetStringOrDefault","case_insensitive":0,"table_function":False},
                        {"name":"dictGetUInt16","case_insensitive":0,"table_function":False},
                        {"name":"dictGetUInt16OrDefault","case_insensitive":0,"table_function":False},
                        {"name":"dictGetUInt32","case_insensitive":0,"table_function":False},
                        {"name":"dictGetUInt32OrDefault","case_insensitive":0,"table_function":False},
                        {"name":"dictGetUInt64","case_insensitive":0,"table_function":False},
                        {"name":"dictGetUInt64OrDefault","case_insensitive":0,"table_function":False},
                        {"name":"dictGetUInt8","case_insensitive":0,"table_function":False},
                        {"name":"dictGetUInt8OrDefault","case_insensitive":0,"table_function":False},
                        {"name":"dictGetUUID","case_insensitive":0,"table_function":False},
                        {"name":"dictGetUUIDOrDefault","case_insensitive":0,"table_function":False},
                        {"name":"dictHas","case_insensitive":0,"table_function":False},
                        {"name":"dictIsIn","case_insensitive":0,"table_function":False},
                        {"name":"dictionary","case_insensitive":0,"table_function":True},
                        {"name":"displayName","case_insensitive":0,"table_function":False},
                        {"name":"distanceL1","case_insensitive":1,"table_function":False},
                        {"name":"distanceL2","case_insensitive":1,"table_function":False},
                        {"name":"distanceL2Squared","case_insensitive":1,"table_function":False},
                        {"name":"distanceLinf","case_insensitive":1,"table_function":False},
                        {"name":"distanceLp","case_insensitive":1,"table_function":False},
                        {"name":"divide","case_insensitive":0,"table_function":False},
                        {"name":"divideDecimal","case_insensitive":0,"table_function":False},
                        {"name":"domain","case_insensitive":0,"table_function":False},
                        {"name":"domainRFC","case_insensitive":0,"table_function":False},
                        {"name":"domainWithoutWWW","case_insensitive":0,"table_function":False},
                        {"name":"domainWithoutWWWRFC","case_insensitive":0,"table_function":False},
                        {"name":"dotProduct","case_insensitive":0,"table_function":False},
                        {"name":"dumpColumnStructure","case_insensitive":0,"table_function":False},
                        {"name":"e","case_insensitive":0,"table_function":False},
                        {"name":"editDistance","case_insensitive":0,"table_function":False},
                        {"name":"empty","case_insensitive":0,"table_function":False},
                        {"name":"emptyArrayDate","case_insensitive":0,"table_function":False},
                        {"name":"emptyArrayDateTime","case_insensitive":0,"table_function":False},
                        {"name":"emptyArrayFloat32","case_insensitive":0,"table_function":False},
                        {"name":"emptyArrayFloat64","case_insensitive":0,"table_function":False},
                        {"name":"emptyArrayInt16","case_insensitive":0,"table_function":False},
                        {"name":"emptyArrayInt32","case_insensitive":0,"table_function":False},
                        {"name":"emptyArrayInt64","case_insensitive":0,"table_function":False},
                        {"name":"emptyArrayInt8","case_insensitive":0,"table_function":False},
                        {"name":"emptyArrayString","case_insensitive":0,"table_function":False},
                        {"name":"emptyArrayToSingle","case_insensitive":0,"table_function":False},
                        {"name":"emptyArrayUInt16","case_insensitive":0,"table_function":False},
                        {"name":"emptyArrayUInt32","case_insensitive":0,"table_function":False},
                        {"name":"emptyArrayUInt64","case_insensitive":0,"table_function":False},
                        {"name":"emptyArrayUInt8","case_insensitive":0,"table_function":False},
                        {"name":"enabledProfiles","case_insensitive":0,"table_function":False},
                        {"name":"enabledRoles","case_insensitive":0,"table_function":False},
                        {"name":"encodeURLComponent","case_insensitive":0,"table_function":False},
                        {"name":"encodeURLFormComponent","case_insensitive":0,"table_function":False},
                        {"name":"encodeXMLComponent","case_insensitive":0,"table_function":False},
                        {"name":"encrypt","case_insensitive":0,"table_function":False},
                        {"name":"endsWith","case_insensitive":0,"table_function":False},
                        {"name":"endsWithUTF8","case_insensitive":0,"table_function":False},
                        {"name":"entropy","case_insensitive":0,"table_function":False},
                        {"name":"equals","case_insensitive":0,"table_function":False},
                        {"name":"erf","case_insensitive":0,"table_function":False},
                        {"name":"erfc","case_insensitive":0,"table_function":False},
                        {"name":"errorCodeToName","case_insensitive":0,"table_function":False},
                        {"name":"evalMLMethod","case_insensitive":0,"table_function":False},
                        {"name":"executable","case_insensitive":0,"table_function":True},
                        {"name":"exp","case_insensitive":1,"table_function":False},
                        {"name":"exp10","case_insensitive":0,"table_function":False},
                        {"name":"exp2","case_insensitive":0,"table_function":False},
                        {"name":"exponentialMovingAverage","case_insensitive":0,"table_function":False},
                        {"name":"exponentialTimeDecayedAvg","case_insensitive":0,"table_function":False},
                        {"name":"exponentialTimeDecayedCount","case_insensitive":0,"table_function":False},
                        {"name":"exponentialTimeDecayedMax","case_insensitive":0,"table_function":False},
                        {"name":"exponentialTimeDecayedSum","case_insensitive":0,"table_function":False},
                        {"name":"extract","case_insensitive":0,"table_function":False},
                        {"name":"extractAll","case_insensitive":0,"table_function":False},
                        {"name":"extractAllGroups","case_insensitive":0,"table_function":False},
                        {"name":"extractAllGroupsHorizontal","case_insensitive":0,"table_function":False},
                        {"name":"extractAllGroupsVertical","case_insensitive":0,"table_function":False},
                        {"name":"extractGroups","case_insensitive":0,"table_function":False},
                        {"name":"extractKeyValuePairs","case_insensitive":0,"table_function":False},
                        {"name":"extractKeyValuePairsWithEscaping","case_insensitive":0,"table_function":False},
                        {"name":"extractTextFromHTML","case_insensitive":0,"table_function":False},
                        {"name":"extractURLParameter","case_insensitive":0,"table_function":False},
                        {"name":"extractURLParameterNames","case_insensitive":0,"table_function":False},
                        {"name":"extractURLParameters","case_insensitive":0,"table_function":False},
                        {"name":"factorial","case_insensitive":1,"table_function":False},
                        {"name":"farmFingerprint64","case_insensitive":0,"table_function":False},
                        {"name":"farmHash64","case_insensitive":0,"table_function":False},
                        {"name":"file","case_insensitive":0,"table_function":False},
                        {"name":"file","case_insensitive":0,"table_function":True},
                        {"name":"fileCluster","case_insensitive":0,"table_function":True},
                        {"name":"filesystemAvailable","case_insensitive":0,"table_function":False},
                        {"name":"filesystemCapacity","case_insensitive":0,"table_function":False},
                        {"name":"filesystemUnreserved","case_insensitive":0,"table_function":False},
                        {"name":"finalizeAggregation","case_insensitive":0,"table_function":False},
                        {"name":"firstLine","case_insensitive":0,"table_function":False},
                        {"name":"firstSignificantSubdomain","case_insensitive":0,"table_function":False},
                        {"name":"firstSignificantSubdomainCustom","case_insensitive":0,"table_function":False},
                        {"name":"firstSignificantSubdomainCustomRFC","case_insensitive":0,"table_function":False},
                        {"name":"firstSignificantSubdomainRFC","case_insensitive":0,"table_function":False},
                        {"name":"first_value","case_insensitive":1,"table_function":False},
                        {"name":"first_value_respect_nulls","case_insensitive":1,"table_function":False},
                        {"name":"flameGraph","case_insensitive":0,"table_function":False},
                        {"name":"flatten","case_insensitive":1,"table_function":False},
                        {"name":"flattenTuple","case_insensitive":0,"table_function":False},
                        {"name":"floor","case_insensitive":1,"table_function":False},
                        {"name":"format","case_insensitive":0,"table_function":False},
                        {"name":"format","case_insensitive":0,"table_function":True},
                        {"name":"formatDateTime","case_insensitive":0,"table_function":False},
                        {"name":"formatDateTimeInJodaSyntax","case_insensitive":0,"table_function":False},
                        {"name":"formatQuery","case_insensitive":0,"table_function":False},
                        {"name":"formatQueryOrNull","case_insensitive":0,"table_function":False},
                        {"name":"formatQuerySingleLine","case_insensitive":0,"table_function":False},
                        {"name":"formatQuerySingleLineOrNull","case_insensitive":0,"table_function":False},
                        {"name":"formatReadableDecimalSize","case_insensitive":0,"table_function":False},
                        {"name":"formatReadableQuantity","case_insensitive":0,"table_function":False},
                        {"name":"formatReadableSize","case_insensitive":0,"table_function":False},
                        {"name":"formatReadableTimeDelta","case_insensitive":0,"table_function":False},
                        {"name":"formatRow","case_insensitive":0,"table_function":False},
                        {"name":"formatRowNoNewline","case_insensitive":0,"table_function":False},
                        {"name":"fragment","case_insensitive":0,"table_function":False},
                        {"name":"fromDaysSinceYearZero","case_insensitive":0,"table_function":False},
                        {"name":"fromDaysSinceYearZero32","case_insensitive":0,"table_function":False},
                        {"name":"fromModifiedJulianDay","case_insensitive":0,"table_function":False},
                        {"name":"fromModifiedJulianDayOrNull","case_insensitive":0,"table_function":False},
                        {"name":"fromUTCTimestamp","case_insensitive":0,"table_function":False},
                        {"name":"fromUnixTimestamp","case_insensitive":0,"table_function":False},
                        {"name":"fromUnixTimestamp64Micro","case_insensitive":0,"table_function":False},
                        {"name":"fromUnixTimestamp64Milli","case_insensitive":0,"table_function":False},
                        {"name":"fromUnixTimestamp64Nano","case_insensitive":0,"table_function":False},
                        {"name":"fromUnixTimestampInJodaSyntax","case_insensitive":0,"table_function":False},
                        {"name":"from_utc_timestamp","case_insensitive":1,"table_function":False},
                        {"name":"fullHostName","case_insensitive":0,"table_function":False},
                        {"name":"fuzzBits","case_insensitive":0,"table_function":False},
                        {"name":"fuzzJSON","case_insensitive":0,"table_function":True},
                        {"name":"gccMurmurHash","case_insensitive":0,"table_function":False},
                        {"name":"gcd","case_insensitive":0,"table_function":False},
                        {"name":"gcs","case_insensitive":0,"table_function":True},
                        {"name":"generateRandom","case_insensitive":0,"table_function":True},
                        {"name":"generateRandomStructure","case_insensitive":0,"table_function":False},
                        {"name":"generateULID","case_insensitive":0,"table_function":False},
                        {"name":"generateUUIDv4","case_insensitive":0,"table_function":False},
                        {"name":"geoDistance","case_insensitive":0,"table_function":False},
                        {"name":"geoToH3","case_insensitive":0,"table_function":False},
                        {"name":"geoToS2","case_insensitive":0,"table_function":False},
                        {"name":"geohashDecode","case_insensitive":0,"table_function":False},
                        {"name":"geohashEncode","case_insensitive":0,"table_function":False},
                        {"name":"geohashesInBox","case_insensitive":0,"table_function":False},
                        {"name":"getMacro","case_insensitive":0,"table_function":False},
                        {"name":"getOSKernelVersion","case_insensitive":0,"table_function":False},
                        {"name":"getServerPort","case_insensitive":0,"table_function":False},
                        {"name":"getSetting","case_insensitive":0,"table_function":False},
                        {"name":"getSizeOfEnumType","case_insensitive":0,"table_function":False},
                        {"name":"getSubcolumn","case_insensitive":0,"table_function":False},
                        {"name":"getTypeSerializationStreams","case_insensitive":0,"table_function":False},
                        {"name":"globalIn","case_insensitive":0,"table_function":False},
                        {"name":"globalInIgnoreSet","case_insensitive":0,"table_function":False},
                        {"name":"globalNotIn","case_insensitive":0,"table_function":False},
                        {"name":"globalNotInIgnoreSet","case_insensitive":0,"table_function":False},
                        {"name":"globalNotNullIn","case_insensitive":0,"table_function":False},
                        {"name":"globalNotNullInIgnoreSet","case_insensitive":0,"table_function":False},
                        {"name":"globalNullIn","case_insensitive":0,"table_function":False},
                        {"name":"globalNullInIgnoreSet","case_insensitive":0,"table_function":False},
                        {"name":"globalVariable","case_insensitive":0,"table_function":False},
                        {"name":"greatCircleAngle","case_insensitive":0,"table_function":False},
                        {"name":"greatCircleDistance","case_insensitive":0,"table_function":False},
                        {"name":"greater","case_insensitive":0,"table_function":False},
                        {"name":"greaterOrEquals","case_insensitive":0,"table_function":False},
                        {"name":"greatest","case_insensitive":1,"table_function":False},
                        {"name":"groupArray","case_insensitive":0,"table_function":False},
                        {"name":"groupArrayInsertAt","case_insensitive":0,"table_function":False},
                        {"name":"groupArrayIntersect","case_insensitive":0,"table_function":False},
                        {"name":"groupArrayLast","case_insensitive":0,"table_function":False},
                        {"name":"groupArrayMovingAvg","case_insensitive":0,"table_function":False},
                        {"name":"groupArrayMovingSum","case_insensitive":0,"table_function":False},
                        {"name":"groupArraySample","case_insensitive":0,"table_function":False},
                        {"name":"groupArraySorted","case_insensitive":0,"table_function":False},
                        {"name":"groupBitAnd","case_insensitive":0,"table_function":False},
                        {"name":"groupBitOr","case_insensitive":0,"table_function":False},
                        {"name":"groupBitXor","case_insensitive":0,"table_function":False},
                        {"name":"groupBitmap","case_insensitive":0,"table_function":False},
                        {"name":"groupBitmapAnd","case_insensitive":0,"table_function":False},
                        {"name":"groupBitmapOr","case_insensitive":0,"table_function":False},
                        {"name":"groupBitmapXor","case_insensitive":0,"table_function":False},
                        {"name":"groupUniqArray","case_insensitive":0,"table_function":False},
                        {"name":"h3CellAreaM2","case_insensitive":0,"table_function":False},
                        {"name":"h3CellAreaRads2","case_insensitive":0,"table_function":False},
                        {"name":"h3Distance","case_insensitive":0,"table_function":False},
                        {"name":"h3EdgeAngle","case_insensitive":0,"table_function":False},
                        {"name":"h3EdgeLengthKm","case_insensitive":0,"table_function":False},
                        {"name":"h3EdgeLengthM","case_insensitive":0,"table_function":False},
                        {"name":"h3ExactEdgeLengthKm","case_insensitive":0,"table_function":False},
                        {"name":"h3ExactEdgeLengthM","case_insensitive":0,"table_function":False},
                        {"name":"h3ExactEdgeLengthRads","case_insensitive":0,"table_function":False},
                        {"name":"h3GetBaseCell","case_insensitive":0,"table_function":False},
                        {"name":"h3GetDestinationIndexFromUnidirectionalEdge","case_insensitive":0,"table_function":False},
                        {"name":"h3GetFaces","case_insensitive":0,"table_function":False},
                        {"name":"h3GetIndexesFromUnidirectionalEdge","case_insensitive":0,"table_function":False},
                        {"name":"h3GetOriginIndexFromUnidirectionalEdge","case_insensitive":0,"table_function":False},
                        {"name":"h3GetPentagonIndexes","case_insensitive":0,"table_function":False},
                        {"name":"h3GetRes0Indexes","case_insensitive":0,"table_function":False},
                        {"name":"h3GetResolution","case_insensitive":0,"table_function":False},
                        {"name":"h3GetUnidirectionalEdge","case_insensitive":0,"table_function":False},
                        {"name":"h3GetUnidirectionalEdgeBoundary","case_insensitive":0,"table_function":False},
                        {"name":"h3GetUnidirectionalEdgesFromHexagon","case_insensitive":0,"table_function":False},
                        {"name":"h3HexAreaKm2","case_insensitive":0,"table_function":False},
                        {"name":"h3HexAreaM2","case_insensitive":0,"table_function":False},
                        {"name":"h3HexRing","case_insensitive":0,"table_function":False},
                        {"name":"h3IndexesAreNeighbors","case_insensitive":0,"table_function":False},
                        {"name":"h3IsPentagon","case_insensitive":0,"table_function":False},
                        {"name":"h3IsResClassIII","case_insensitive":0,"table_function":False},
                        {"name":"h3IsValid","case_insensitive":0,"table_function":False},
                        {"name":"h3Line","case_insensitive":0,"table_function":False},
                        {"name":"h3NumHexagons","case_insensitive":0,"table_function":False},
                        {"name":"h3PointDistKm","case_insensitive":0,"table_function":False},
                        {"name":"h3PointDistM","case_insensitive":0,"table_function":False},
                        {"name":"h3PointDistRads","case_insensitive":0,"table_function":False},
                        {"name":"h3ToCenterChild","case_insensitive":0,"table_function":False},
                        {"name":"h3ToChildren","case_insensitive":0,"table_function":False},
                        {"name":"h3ToGeo","case_insensitive":0,"table_function":False},
                        {"name":"h3ToGeoBoundary","case_insensitive":0,"table_function":False},
                        {"name":"h3ToParent","case_insensitive":0,"table_function":False},
                        {"name":"h3ToString","case_insensitive":0,"table_function":False},
                        {"name":"h3UnidirectionalEdgeIsValid","case_insensitive":0,"table_function":False},
                        {"name":"h3kRing","case_insensitive":0,"table_function":False},
                        {"name":"halfMD5","case_insensitive":0,"table_function":False},
                        {"name":"has","case_insensitive":0,"table_function":False},
                        {"name":"hasAll","case_insensitive":0,"table_function":False},
                        {"name":"hasAny","case_insensitive":0,"table_function":False},
                        {"name":"hasColumnInTable","case_insensitive":0,"table_function":False},
                        {"name":"hasSubsequence","case_insensitive":1,"table_function":False},
                        {"name":"hasSubsequenceCaseInsensitive","case_insensitive":1,"table_function":False},
                        {"name":"hasSubsequenceCaseInsensitiveUTF8","case_insensitive":1,"table_function":False},
                        {"name":"hasSubsequenceUTF8","case_insensitive":1,"table_function":False},
                        {"name":"hasSubstr","case_insensitive":0,"table_function":False},
                        {"name":"hasThreadFuzzer","case_insensitive":0,"table_function":False},
                        {"name":"hasToken","case_insensitive":0,"table_function":False},
                        {"name":"hasTokenCaseInsensitive","case_insensitive":1,"table_function":False},
                        {"name":"hasTokenCaseInsensitiveOrNull","case_insensitive":1,"table_function":False},
                        {"name":"hasTokenOrNull","case_insensitive":0,"table_function":False},
                        {"name":"hdfs","case_insensitive":0,"table_function":True},
                        {"name":"hdfsCluster","case_insensitive":0,"table_function":True},
                        {"name":"hex","case_insensitive":1,"table_function":False},
                        {"name":"histogram","case_insensitive":0,"table_function":False},
                        {"name":"hive","case_insensitive":0,"table_function":True},
                        {"name":"hiveHash","case_insensitive":0,"table_function":False},
                        {"name":"hop","case_insensitive":0,"table_function":False},
                        {"name":"hopEnd","case_insensitive":0,"table_function":False},
                        {"name":"hopStart","case_insensitive":0,"table_function":False},
                        {"name":"hostName","case_insensitive":0,"table_function":False},
                        {"name":"hostname","case_insensitive":0,"table_function":False},
                        {"name":"hudi","case_insensitive":0,"table_function":True},
                        {"name":"hypot","case_insensitive":1,"table_function":False},
                        {"name":"iceberg","case_insensitive":0,"table_function":True},
                        {"name":"identity","case_insensitive":0,"table_function":False},
                        {"name":"idnaDecode","case_insensitive":0,"table_function":False},
                        {"name":"idnaEncode","case_insensitive":0,"table_function":False},
                        {"name":"if","case_insensitive":1,"table_function":False},
                        {"name":"ifNotFinite","case_insensitive":0,"table_function":False},
                        {"name":"ifNull","case_insensitive":1,"table_function":False},
                        {"name":"ignore","case_insensitive":0,"table_function":False},
                        {"name":"ilike","case_insensitive":0,"table_function":False},
                        {"name":"in","case_insensitive":0,"table_function":False},
                        {"name":"inIgnoreSet","case_insensitive":0,"table_function":False},
                        {"name":"indexHint","case_insensitive":0,"table_function":False},
                        {"name":"indexOf","case_insensitive":0,"table_function":False},
                        {"name":"initcap","case_insensitive":1,"table_function":False},
                        {"name":"initcapUTF8","case_insensitive":0,"table_function":False},
                        {"name":"initialQueryID","case_insensitive":0,"table_function":False},
                        {"name":"initial_query_id","case_insensitive":1,"table_function":False},
                        {"name":"initializeAggregation","case_insensitive":0,"table_function":False},
                        {"name":"input","case_insensitive":0,"table_function":True},
                        {"name":"instr","case_insensitive":1,"table_function":False},
                        {"name":"intDiv","case_insensitive":0,"table_function":False},
                        {"name":"intDivOrZero","case_insensitive":0,"table_function":False},
                        {"name":"intExp10","case_insensitive":0,"table_function":False},
                        {"name":"intExp2","case_insensitive":0,"table_function":False},
                        {"name":"intHash32","case_insensitive":0,"table_function":False},
                        {"name":"intHash64","case_insensitive":0,"table_function":False},
                        {"name":"intervalLengthSum","case_insensitive":0,"table_function":False},
                        {"name":"isConstant","case_insensitive":0,"table_function":False},
                        {"name":"isDecimalOverflow","case_insensitive":0,"table_function":False},
                        {"name":"isFinite","case_insensitive":0,"table_function":False},
                        {"name":"isIPAddressInRange","case_insensitive":0,"table_function":False},
                        {"name":"isIPv4String","case_insensitive":0,"table_function":False},
                        {"name":"isIPv6String","case_insensitive":0,"table_function":False},
                        {"name":"isInfinite","case_insensitive":0,"table_function":False},
                        {"name":"isNaN","case_insensitive":0,"table_function":False},
                        {"name":"isNotDistinctFrom","case_insensitive":0,"table_function":False},
                        {"name":"isNotNull","case_insensitive":0,"table_function":False},
                        {"name":"isNull","case_insensitive":1,"table_function":False},
                        {"name":"isNullable","case_insensitive":0,"table_function":False},
                        {"name":"isValidJSON","case_insensitive":0,"table_function":False},
                        {"name":"isValidUTF8","case_insensitive":0,"table_function":False},
                        {"name":"isZeroOrNull","case_insensitive":0,"table_function":False},
                        {"name":"jaroSimilarity","case_insensitive":0,"table_function":False},
                        {"name":"jaroWinklerSimilarity","case_insensitive":0,"table_function":False},
                        {"name":"javaHash","case_insensitive":0,"table_function":False},
                        {"name":"javaHashUTF16LE","case_insensitive":0,"table_function":False},
                        {"name":"jdbc","case_insensitive":0,"table_function":True},
                        {"name":"jsonMergePatch","case_insensitive":0,"table_function":False},
                        {"name":"jumpConsistentHash","case_insensitive":0,"table_function":False},
                        {"name":"kafkaMurmurHash","case_insensitive":0,"table_function":False},
                        {"name":"kolmogorovSmirnovTest","case_insensitive":1,"table_function":False},
                        {"name":"kostikConsistentHash","case_insensitive":0,"table_function":False},
                        {"name":"kql_array_sort_asc","case_insensitive":0,"table_function":False},
                        {"name":"kql_array_sort_desc","case_insensitive":0,"table_function":False},
                        {"name":"kurtPop","case_insensitive":0,"table_function":False},
                        {"name":"kurtSamp","case_insensitive":0,"table_function":False},
                        {"name":"lagInFrame","case_insensitive":0,"table_function":False},
                        {"name":"largestTriangleThreeBuckets","case_insensitive":0,"table_function":False},
                        {"name":"last_value","case_insensitive":1,"table_function":False},
                        {"name":"last_value_respect_nulls","case_insensitive":1,"table_function":False},
                        {"name":"lcase","case_insensitive":1,"table_function":False},
                        {"name":"lcm","case_insensitive":0,"table_function":False},
                        {"name":"leadInFrame","case_insensitive":0,"table_function":False},
                        {"name":"least","case_insensitive":1,"table_function":False},
                        {"name":"left","case_insensitive":1,"table_function":False},
                        {"name":"leftPad","case_insensitive":0,"table_function":False},
                        {"name":"leftPadUTF8","case_insensitive":0,"table_function":False},
                        {"name":"leftUTF8","case_insensitive":0,"table_function":False},
                        {"name":"lemmatize","case_insensitive":0,"table_function":False},
                        {"name":"length","case_insensitive":1,"table_function":False},
                        {"name":"lengthUTF8","case_insensitive":0,"table_function":False},
                        {"name":"less","case_insensitive":0,"table_function":False},
                        {"name":"lessOrEquals","case_insensitive":0,"table_function":False},
                        {"name":"levenshteinDistance","case_insensitive":0,"table_function":False},
                        {"name":"lgamma","case_insensitive":0,"table_function":False},
                        {"name":"like","case_insensitive":0,"table_function":False},
                        {"name":"ln","case_insensitive":1,"table_function":False},
                        {"name":"locate","case_insensitive":1,"table_function":False},
                        {"name":"log","case_insensitive":1,"table_function":False},
                        {"name":"log10","case_insensitive":1,"table_function":False},
                        {"name":"log1p","case_insensitive":0,"table_function":False},
                        {"name":"log2","case_insensitive":1,"table_function":False},
                        {"name":"logTrace","case_insensitive":0,"table_function":False},
                        {"name":"lowCardinalityIndices","case_insensitive":0,"table_function":False},
                        {"name":"lowCardinalityKeys","case_insensitive":0,"table_function":False},
                        {"name":"lower","case_insensitive":1,"table_function":False},
                        {"name":"lowerUTF8","case_insensitive":0,"table_function":False},
                        {"name":"lpad","case_insensitive":1,"table_function":False},
                        {"name":"ltrim","case_insensitive":0,"table_function":False},
                        {"name":"lttb","case_insensitive":0,"table_function":False},
                        {"name":"makeDate","case_insensitive":1,"table_function":False},
                        {"name":"makeDate32","case_insensitive":0,"table_function":False},
                        {"name":"makeDateTime","case_insensitive":0,"table_function":False},
                        {"name":"makeDateTime64","case_insensitive":0,"table_function":False},
                        {"name":"mannWhitneyUTest","case_insensitive":0,"table_function":False},
                        {"name":"map","case_insensitive":0,"table_function":False},
                        {"name":"mapAdd","case_insensitive":0,"table_function":False},
                        {"name":"mapAll","case_insensitive":0,"table_function":False},
                        {"name":"mapApply","case_insensitive":0,"table_function":False},
                        {"name":"mapConcat","case_insensitive":0,"table_function":False},
                        {"name":"mapContains","case_insensitive":0,"table_function":False},
                        {"name":"mapContainsKeyLike","case_insensitive":0,"table_function":False},
                        {"name":"mapExists","case_insensitive":0,"table_function":False},
                        {"name":"mapExtractKeyLike","case_insensitive":0,"table_function":False},
                        {"name":"mapFilter","case_insensitive":0,"table_function":False},
                        {"name":"mapFromArrays","case_insensitive":0,"table_function":False},
                        {"name":"mapFromString","case_insensitive":0,"table_function":False},
                        {"name":"mapKeys","case_insensitive":0,"table_function":False},
                        {"name":"mapPartialReverseSort","case_insensitive":0,"table_function":False},
                        {"name":"mapPartialSort","case_insensitive":0,"table_function":False},
                        {"name":"mapPopulateSeries","case_insensitive":0,"table_function":False},
                        {"name":"mapReverseSort","case_insensitive":0,"table_function":False},
                        {"name":"mapSort","case_insensitive":0,"table_function":False},
                        {"name":"mapSubtract","case_insensitive":0,"table_function":False},
                        {"name":"mapUpdate","case_insensitive":0,"table_function":False},
                        {"name":"mapValues","case_insensitive":0,"table_function":False},
                        {"name":"match","case_insensitive":0,"table_function":False},
                        {"name":"materialize","case_insensitive":0,"table_function":False},
                        {"name":"max","case_insensitive":1,"table_function":False},
                        {"name":"max2","case_insensitive":1,"table_function":False},
                        {"name":"maxIntersections","case_insensitive":0,"table_function":False},
                        {"name":"maxIntersectionsPosition","case_insensitive":0,"table_function":False},
                        {"name":"maxMappedArrays","case_insensitive":0,"table_function":False},
                        {"name":"meanZTest","case_insensitive":0,"table_function":False},
                        {"name":"median","case_insensitive":0,"table_function":False},
                        {"name":"medianBFloat16","case_insensitive":0,"table_function":False},
                        {"name":"medianBFloat16Weighted","case_insensitive":0,"table_function":False},
                        {"name":"medianDD","case_insensitive":0,"table_function":False},
                        {"name":"medianDeterministic","case_insensitive":0,"table_function":False},
                        {"name":"medianExact","case_insensitive":0,"table_function":False},
                        {"name":"medianExactHigh","case_insensitive":0,"table_function":False},
                        {"name":"medianExactLow","case_insensitive":0,"table_function":False},
                        {"name":"medianExactWeighted","case_insensitive":0,"table_function":False},
                        {"name":"medianGK","case_insensitive":0,"table_function":False},
                        {"name":"medianInterpolatedWeighted","case_insensitive":0,"table_function":False},
                        {"name":"medianTDigest","case_insensitive":0,"table_function":False},
                        {"name":"medianTDigestWeighted","case_insensitive":0,"table_function":False},
                        {"name":"medianTiming","case_insensitive":0,"table_function":False},
                        {"name":"medianTimingWeighted","case_insensitive":0,"table_function":False},
                        {"name":"merge","case_insensitive":0,"table_function":True},
                        {"name":"mergeTreeIndex","case_insensitive":0,"table_function":True},
                        {"name":"metroHash64","case_insensitive":0,"table_function":False},
                        {"name":"mid","case_insensitive":1,"table_function":False},
                        {"name":"min","case_insensitive":1,"table_function":False},
                        {"name":"min2","case_insensitive":1,"table_function":False},
                        {"name":"minMappedArrays","case_insensitive":0,"table_function":False},
                        {"name":"minSampleSizeContinous","case_insensitive":0,"table_function":False},
                        {"name":"minSampleSizeContinuous","case_insensitive":0,"table_function":False},
                        {"name":"minSampleSizeConversion","case_insensitive":0,"table_function":False},
                        {"name":"minus","case_insensitive":0,"table_function":False},
                        {"name":"mismatches","case_insensitive":0,"table_function":False},
                        {"name":"mod","case_insensitive":1,"table_function":False},
                        {"name":"modulo","case_insensitive":0,"table_function":False},
                        {"name":"moduloLegacy","case_insensitive":0,"table_function":False},
                        {"name":"moduloOrZero","case_insensitive":0,"table_function":False},
                        {"name":"mongodb","case_insensitive":0,"table_function":True},
                        {"name":"monthName","case_insensitive":1,"table_function":False},
                        {"name":"mortonDecode","case_insensitive":0,"table_function":False},
                        {"name":"mortonEncode","case_insensitive":0,"table_function":False},
                        {"name":"multiFuzzyMatchAllIndices","case_insensitive":0,"table_function":False},
                        {"name":"multiFuzzyMatchAny","case_insensitive":0,"table_function":False},
                        {"name":"multiFuzzyMatchAnyIndex","case_insensitive":0,"table_function":False},
                        {"name":"multiIf","case_insensitive":0,"table_function":False},
                        {"name":"multiMatchAllIndices","case_insensitive":0,"table_function":False},
                        {"name":"multiMatchAny","case_insensitive":0,"table_function":False},
                        {"name":"multiMatchAnyIndex","case_insensitive":0,"table_function":False},
                        {"name":"multiSearchAllPositions","case_insensitive":0,"table_function":False},
                        {"name":"multiSearchAllPositionsCaseInsensitive","case_insensitive":0,"table_function":False},
                        {"name":"multiSearchAllPositionsCaseInsensitiveUTF8","case_insensitive":0,"table_function":False},
                        {"name":"multiSearchAllPositionsUTF8","case_insensitive":0,"table_function":False},
                        {"name":"multiSearchAny","case_insensitive":0,"table_function":False},
                        {"name":"multiSearchAnyCaseInsensitive","case_insensitive":0,"table_function":False},
                        {"name":"multiSearchAnyCaseInsensitiveUTF8","case_insensitive":0,"table_function":False},
                        {"name":"multiSearchAnyUTF8","case_insensitive":0,"table_function":False},
                        {"name":"multiSearchFirstIndex","case_insensitive":0,"table_function":False},
                        {"name":"multiSearchFirstIndexCaseInsensitive","case_insensitive":0,"table_function":False},
                        {"name":"multiSearchFirstIndexCaseInsensitiveUTF8","case_insensitive":0,"table_function":False},
                        {"name":"multiSearchFirstIndexUTF8","case_insensitive":0,"table_function":False},
                        {"name":"multiSearchFirstPosition","case_insensitive":0,"table_function":False},
                        {"name":"multiSearchFirstPositionCaseInsensitive","case_insensitive":0,"table_function":False},
                        {"name":"multiSearchFirstPositionCaseInsensitiveUTF8","case_insensitive":0,"table_function":False},
                        {"name":"multiSearchFirstPositionUTF8","case_insensitive":0,"table_function":False},
                        {"name":"multiply","case_insensitive":0,"table_function":False},
                        {"name":"multiplyDecimal","case_insensitive":0,"table_function":False},
                        {"name":"murmurHash2_32","case_insensitive":0,"table_function":False},
                        {"name":"murmurHash2_64","case_insensitive":0,"table_function":False},
                        {"name":"murmurHash3_128","case_insensitive":0,"table_function":False},
                        {"name":"murmurHash3_32","case_insensitive":0,"table_function":False},
                        {"name":"murmurHash3_64","case_insensitive":0,"table_function":False},
                        {"name":"mysql","case_insensitive":0,"table_function":True},
                        {"name":"negate","case_insensitive":0,"table_function":False},
                        {"name":"neighbor","case_insensitive":0,"table_function":False},
                        {"name":"nested","case_insensitive":0,"table_function":False},
                        {"name":"netloc","case_insensitive":0,"table_function":False},
                        {"name":"ngramDistance","case_insensitive":0,"table_function":False},
                        {"name":"ngramDistanceCaseInsensitive","case_insensitive":0,"table_function":False},
                        {"name":"ngramDistanceCaseInsensitiveUTF8","case_insensitive":0,"table_function":False},
                        {"name":"ngramDistanceUTF8","case_insensitive":0,"table_function":False},
                        {"name":"ngramMinHash","case_insensitive":0,"table_function":False},
                        {"name":"ngramMinHashArg","case_insensitive":0,"table_function":False},
                        {"name":"ngramMinHashArgCaseInsensitive","case_insensitive":0,"table_function":False},
                        {"name":"ngramMinHashArgCaseInsensitiveUTF8","case_insensitive":0,"table_function":False},
                        {"name":"ngramMinHashArgUTF8","case_insensitive":0,"table_function":False},
                        {"name":"ngramMinHashCaseInsensitive","case_insensitive":0,"table_function":False},
                        {"name":"ngramMinHashCaseInsensitiveUTF8","case_insensitive":0,"table_function":False},
                        {"name":"ngramMinHashUTF8","case_insensitive":0,"table_function":False},
                        {"name":"ngramSearch","case_insensitive":0,"table_function":False},
                        {"name":"ngramSearchCaseInsensitive","case_insensitive":0,"table_function":False},
                        {"name":"ngramSearchCaseInsensitiveUTF8","case_insensitive":0,"table_function":False},
                        {"name":"ngramSearchUTF8","case_insensitive":0,"table_function":False},
                        {"name":"ngramSimHash","case_insensitive":0,"table_function":False},
                        {"name":"ngramSimHashCaseInsensitive","case_insensitive":0,"table_function":False},
                        {"name":"ngramSimHashCaseInsensitiveUTF8","case_insensitive":0,"table_function":False},
                        {"name":"ngramSimHashUTF8","case_insensitive":0,"table_function":False},
                        {"name":"ngrams","case_insensitive":0,"table_function":False},
                        {"name":"nonNegativeDerivative","case_insensitive":0,"table_function":False},
                        {"name":"normL1","case_insensitive":1,"table_function":False},
                        {"name":"normL2","case_insensitive":1,"table_function":False},
                        {"name":"normL2Squared","case_insensitive":1,"table_function":False},
                        {"name":"normLinf","case_insensitive":1,"table_function":False},
                        {"name":"normLp","case_insensitive":1,"table_function":False},
                        {"name":"normalizeL1","case_insensitive":1,"table_function":False},
                        {"name":"normalizeL2","case_insensitive":1,"table_function":False},
                        {"name":"normalizeLinf","case_insensitive":1,"table_function":False},
                        {"name":"normalizeLp","case_insensitive":1,"table_function":False},
                        {"name":"normalizeQuery","case_insensitive":0,"table_function":False},
                        {"name":"normalizeQueryKeepNames","case_insensitive":0,"table_function":False},
                        {"name":"normalizeUTF8NFC","case_insensitive":0,"table_function":False},
                        {"name":"normalizeUTF8NFD","case_insensitive":0,"table_function":False},
                        {"name":"normalizeUTF8NFKC","case_insensitive":0,"table_function":False},
                        {"name":"normalizeUTF8NFKD","case_insensitive":0,"table_function":False},
                        {"name":"normalizedQueryHash","case_insensitive":0,"table_function":False},
                        {"name":"normalizedQueryHashKeepNames","case_insensitive":0,"table_function":False},
                        {"name":"not","case_insensitive":1,"table_function":False},
                        {"name":"notEmpty","case_insensitive":0,"table_function":False},
                        {"name":"notEquals","case_insensitive":0,"table_function":False},
                        {"name":"notILike","case_insensitive":0,"table_function":False},
                        {"name":"notIn","case_insensitive":0,"table_function":False},
                        {"name":"notInIgnoreSet","case_insensitive":0,"table_function":False},
                        {"name":"notLike","case_insensitive":0,"table_function":False},
                        {"name":"notNullIn","case_insensitive":0,"table_function":False},
                        {"name":"notNullInIgnoreSet","case_insensitive":0,"table_function":False},
                        {"name":"nothing","case_insensitive":0,"table_function":False},
                        {"name":"nothingNull","case_insensitive":0,"table_function":False},
                        {"name":"nothingUInt64","case_insensitive":0,"table_function":False},
                        {"name":"now","case_insensitive":1,"table_function":False},
                        {"name":"now64","case_insensitive":1,"table_function":False},
                        {"name":"nowInBlock","case_insensitive":0,"table_function":False},
                        {"name":"nth_value","case_insensitive":1,"table_function":False},
                        {"name":"ntile","case_insensitive":1,"table_function":False},
                        {"name":"null","case_insensitive":0,"table_function":True},
                        {"name":"nullIf","case_insensitive":1,"table_function":False},
                        {"name":"nullIn","case_insensitive":0,"table_function":False},
                        {"name":"nullInIgnoreSet","case_insensitive":0,"table_function":False},
                        {"name":"numbers","case_insensitive":0,"table_function":True},
                        {"name":"numbers_mt","case_insensitive":0,"table_function":True},
                        {"name":"odbc","case_insensitive":0,"table_function":True},
                        {"name":"or","case_insensitive":0,"table_function":False},
                        {"name":"oss","case_insensitive":0,"table_function":True},
                        {"name":"parseDateTime","case_insensitive":0,"table_function":False},
                        {"name":"parseDateTime32BestEffort","case_insensitive":0,"table_function":False},
                        {"name":"parseDateTime32BestEffortOrNull","case_insensitive":0,"table_function":False},
                        {"name":"parseDateTime32BestEffortOrZero","case_insensitive":0,"table_function":False},
                        {"name":"parseDateTime64BestEffort","case_insensitive":0,"table_function":False},
                        {"name":"parseDateTime64BestEffortOrNull","case_insensitive":0,"table_function":False},
                        {"name":"parseDateTime64BestEffortOrZero","case_insensitive":0,"table_function":False},
                        {"name":"parseDateTime64BestEffortUS","case_insensitive":0,"table_function":False},
                        {"name":"parseDateTime64BestEffortUSOrNull","case_insensitive":0,"table_function":False},
                        {"name":"parseDateTime64BestEffortUSOrZero","case_insensitive":0,"table_function":False},
                        {"name":"parseDateTimeBestEffort","case_insensitive":0,"table_function":False},
                        {"name":"parseDateTimeBestEffortOrNull","case_insensitive":0,"table_function":False},
                        {"name":"parseDateTimeBestEffortOrZero","case_insensitive":0,"table_function":False},
                        {"name":"parseDateTimeBestEffortUS","case_insensitive":0,"table_function":False},
                        {"name":"parseDateTimeBestEffortUSOrNull","case_insensitive":0,"table_function":False},
                        {"name":"parseDateTimeBestEffortUSOrZero","case_insensitive":0,"table_function":False},
                        {"name":"parseDateTimeInJodaSyntax","case_insensitive":0,"table_function":False},
                        {"name":"parseDateTimeInJodaSyntaxOrNull","case_insensitive":0,"table_function":False},
                        {"name":"parseDateTimeInJodaSyntaxOrZero","case_insensitive":0,"table_function":False},
                        {"name":"parseDateTimeOrNull","case_insensitive":0,"table_function":False},
                        {"name":"parseDateTimeOrZero","case_insensitive":0,"table_function":False},
                        {"name":"parseTimeDelta","case_insensitive":0,"table_function":False},
                        {"name":"partitionId","case_insensitive":0,"table_function":False},
                        {"name":"path","case_insensitive":0,"table_function":False},
                        {"name":"pathFull","case_insensitive":0,"table_function":False},
                        {"name":"pi","case_insensitive":1,"table_function":False},
                        {"name":"plus","case_insensitive":0,"table_function":False},
                        {"name":"pmod","case_insensitive":1,"table_function":False},
                        {"name":"pointInEllipses","case_insensitive":0,"table_function":False},
                        {"name":"pointInPolygon","case_insensitive":0,"table_function":False},
                        {"name":"polygonAreaCartesian","case_insensitive":0,"table_function":False},
                        {"name":"polygonAreaSpherical","case_insensitive":0,"table_function":False},
                        {"name":"polygonConvexHullCartesian","case_insensitive":0,"table_function":False},
                        {"name":"polygonPerimeterCartesian","case_insensitive":0,"table_function":False},
                        {"name":"polygonPerimeterSpherical","case_insensitive":0,"table_function":False},
                        {"name":"polygonsDistanceCartesian","case_insensitive":0,"table_function":False},
                        {"name":"polygonsDistanceSpherical","case_insensitive":0,"table_function":False},
                        {"name":"polygonsEqualsCartesian","case_insensitive":0,"table_function":False},
                        {"name":"polygonsIntersectionCartesian","case_insensitive":0,"table_function":False},
                        {"name":"polygonsIntersectionSpherical","case_insensitive":0,"table_function":False},
                        {"name":"polygonsSymDifferenceCartesian","case_insensitive":0,"table_function":False},
                        {"name":"polygonsSymDifferenceSpherical","case_insensitive":0,"table_function":False},
                        {"name":"polygonsUnionCartesian","case_insensitive":0,"table_function":False},
                        {"name":"polygonsUnionSpherical","case_insensitive":0,"table_function":False},
                        {"name":"polygonsWithinCartesian","case_insensitive":0,"table_function":False},
                        {"name":"polygonsWithinSpherical","case_insensitive":0,"table_function":False},
                        {"name":"port","case_insensitive":0,"table_function":False},
                        {"name":"portRFC","case_insensitive":0,"table_function":False},
                        {"name":"position","case_insensitive":1,"table_function":False},
                        {"name":"positionCaseInsensitive","case_insensitive":0,"table_function":False},
                        {"name":"positionCaseInsensitiveUTF8","case_insensitive":0,"table_function":False},
                        {"name":"positionUTF8","case_insensitive":0,"table_function":False},
                        {"name":"positiveModulo","case_insensitive":1,"table_function":False},
                        {"name":"positive_modulo","case_insensitive":1,"table_function":False},
                        {"name":"postgresql","case_insensitive":0,"table_function":True},
                        {"name":"pow","case_insensitive":1,"table_function":False},
                        {"name":"power","case_insensitive":1,"table_function":False},
                        {"name":"proportionsZTest","case_insensitive":0,"table_function":False},
                        {"name":"protocol","case_insensitive":0,"table_function":False},
                        {"name":"punycodeDecode","case_insensitive":0,"table_function":False},
                        {"name":"punycodeEncode","case_insensitive":0,"table_function":False},
                        {"name":"quantile","case_insensitive":0,"table_function":False},
                        {"name":"quantileBFloat16","case_insensitive":0,"table_function":False},
                        {"name":"quantileBFloat16Weighted","case_insensitive":0,"table_function":False},
                        {"name":"quantileDD","case_insensitive":0,"table_function":False},
                        {"name":"quantileDeterministic","case_insensitive":0,"table_function":False},
                        {"name":"quantileExact","case_insensitive":0,"table_function":False},
                        {"name":"quantileExactExclusive","case_insensitive":0,"table_function":False},
                        {"name":"quantileExactHigh","case_insensitive":0,"table_function":False},
                        {"name":"quantileExactInclusive","case_insensitive":0,"table_function":False},
                        {"name":"quantileExactLow","case_insensitive":0,"table_function":False},
                        {"name":"quantileExactWeighted","case_insensitive":0,"table_function":False},
                        {"name":"quantileGK","case_insensitive":0,"table_function":False},
                        {"name":"quantileInterpolatedWeighted","case_insensitive":0,"table_function":False},
                        {"name":"quantileTDigest","case_insensitive":0,"table_function":False},
                        {"name":"quantileTDigestWeighted","case_insensitive":0,"table_function":False},
                        {"name":"quantileTiming","case_insensitive":0,"table_function":False},
                        {"name":"quantileTimingWeighted","case_insensitive":0,"table_function":False},
                        {"name":"quantiles","case_insensitive":0,"table_function":False},
                        {"name":"quantilesBFloat16","case_insensitive":0,"table_function":False},
                        {"name":"quantilesBFloat16Weighted","case_insensitive":0,"table_function":False},
                        {"name":"quantilesDD","case_insensitive":0,"table_function":False},
                        {"name":"quantilesDeterministic","case_insensitive":0,"table_function":False},
                        {"name":"quantilesExact","case_insensitive":0,"table_function":False},
                        {"name":"quantilesExactExclusive","case_insensitive":0,"table_function":False},
                        {"name":"quantilesExactHigh","case_insensitive":0,"table_function":False},
                        {"name":"quantilesExactInclusive","case_insensitive":0,"table_function":False},
                        {"name":"quantilesExactLow","case_insensitive":0,"table_function":False},
                        {"name":"quantilesExactWeighted","case_insensitive":0,"table_function":False},
                        {"name":"quantilesGK","case_insensitive":0,"table_function":False},
                        {"name":"quantilesInterpolatedWeighted","case_insensitive":0,"table_function":False},
                        {"name":"quantilesTDigest","case_insensitive":0,"table_function":False},
                        {"name":"quantilesTDigestWeighted","case_insensitive":0,"table_function":False},
                        {"name":"quantilesTiming","case_insensitive":0,"table_function":False},
                        {"name":"quantilesTimingWeighted","case_insensitive":0,"table_function":False},
                        {"name":"queryID","case_insensitive":0,"table_function":False},
                        {"name":"queryString","case_insensitive":0,"table_function":False},
                        {"name":"queryStringAndFragment","case_insensitive":0,"table_function":False},
                        {"name":"query_id","case_insensitive":1,"table_function":False},
                        {"name":"radians","case_insensitive":1,"table_function":False},
                        {"name":"rand","case_insensitive":1,"table_function":False},
                        {"name":"rand32","case_insensitive":0,"table_function":False},
                        {"name":"rand64","case_insensitive":0,"table_function":False},
                        {"name":"randBernoulli","case_insensitive":0,"table_function":False},
                        {"name":"randBinomial","case_insensitive":0,"table_function":False},
                        {"name":"randCanonical","case_insensitive":0,"table_function":False},
                        {"name":"randChiSquared","case_insensitive":0,"table_function":False},
                        {"name":"randConstant","case_insensitive":0,"table_function":False},
                        {"name":"randExponential","case_insensitive":0,"table_function":False},
                        {"name":"randFisherF","case_insensitive":0,"table_function":False},
                        {"name":"randLogNormal","case_insensitive":0,"table_function":False},
                        {"name":"randNegativeBinomial","case_insensitive":0,"table_function":False},
                        {"name":"randNormal","case_insensitive":0,"table_function":False},
                        {"name":"randPoisson","case_insensitive":0,"table_function":False},
                        {"name":"randStudentT","case_insensitive":0,"table_function":False},
                        {"name":"randUniform","case_insensitive":0,"table_function":False},
                        {"name":"randomFixedString","case_insensitive":0,"table_function":False},
                        {"name":"randomPrintableASCII","case_insensitive":0,"table_function":False},
                        {"name":"randomString","case_insensitive":0,"table_function":False},
                        {"name":"randomStringUTF8","case_insensitive":0,"table_function":False},
                        {"name":"range","case_insensitive":0,"table_function":False},
                        {"name":"rank","case_insensitive":1,"table_function":False},
                        {"name":"rankCorr","case_insensitive":0,"table_function":False},
                        {"name":"readWKTMultiPolygon","case_insensitive":0,"table_function":False},
                        {"name":"readWKTPoint","case_insensitive":0,"table_function":False},
                        {"name":"readWKTPolygon","case_insensitive":0,"table_function":False},
                        {"name":"readWKTRing","case_insensitive":0,"table_function":False},
                        {"name":"redis","case_insensitive":0,"table_function":True},
                        {"name":"regexpExtract","case_insensitive":0,"table_function":False},
                        {"name":"regexpQuoteMeta","case_insensitive":0,"table_function":False},
                        {"name":"regionHierarchy","case_insensitive":0,"table_function":False},
                        {"name":"regionIn","case_insensitive":0,"table_function":False},
                        {"name":"regionToArea","case_insensitive":0,"table_function":False},
                        {"name":"regionToCity","case_insensitive":0,"table_function":False},
                        {"name":"regionToContinent","case_insensitive":0,"table_function":False},
                        {"name":"regionToCountry","case_insensitive":0,"table_function":False},
                        {"name":"regionToDistrict","case_insensitive":0,"table_function":False},
                        {"name":"regionToName","case_insensitive":0,"table_function":False},
                        {"name":"regionToPopulation","case_insensitive":0,"table_function":False},
                        {"name":"regionToTopContinent","case_insensitive":0,"table_function":False},
                        {"name":"reinterpret","case_insensitive":0,"table_function":False},
                        {"name":"reinterpretAsDate","case_insensitive":0,"table_function":False},
                        {"name":"reinterpretAsDateTime","case_insensitive":0,"table_function":False},
                        {"name":"reinterpretAsFixedString","case_insensitive":0,"table_function":False},
                        {"name":"reinterpretAsFloat32","case_insensitive":0,"table_function":False},
                        {"name":"reinterpretAsFloat64","case_insensitive":0,"table_function":False},
                        {"name":"reinterpretAsInt128","case_insensitive":0,"table_function":False},
                        {"name":"reinterpretAsInt16","case_insensitive":0,"table_function":False},
                        {"name":"reinterpretAsInt256","case_insensitive":0,"table_function":False},
                        {"name":"reinterpretAsInt32","case_insensitive":0,"table_function":False},
                        {"name":"reinterpretAsInt64","case_insensitive":0,"table_function":False},
                        {"name":"reinterpretAsInt8","case_insensitive":0,"table_function":False},
                        {"name":"reinterpretAsString","case_insensitive":0,"table_function":False},
                        {"name":"reinterpretAsUInt128","case_insensitive":0,"table_function":False},
                        {"name":"reinterpretAsUInt16","case_insensitive":0,"table_function":False},
                        {"name":"reinterpretAsUInt256","case_insensitive":0,"table_function":False},
                        {"name":"reinterpretAsUInt32","case_insensitive":0,"table_function":False},
                        {"name":"reinterpretAsUInt64","case_insensitive":0,"table_function":False},
                        {"name":"reinterpretAsUInt8","case_insensitive":0,"table_function":False},
                        {"name":"reinterpretAsUUID","case_insensitive":0,"table_function":False},
                        {"name":"remote","case_insensitive":0,"table_function":True},
                        {"name":"remoteSecure","case_insensitive":0,"table_function":True},
                        {"name":"repeat","case_insensitive":1,"table_function":False},
                        {"name":"replace","case_insensitive":1,"table_function":False},
                        {"name":"replaceAll","case_insensitive":0,"table_function":False},
                        {"name":"replaceOne","case_insensitive":0,"table_function":False},
                        {"name":"replaceRegexpAll","case_insensitive":0,"table_function":False},
                        {"name":"replaceRegexpOne","case_insensitive":0,"table_function":False},
                        {"name":"replicate","case_insensitive":0,"table_function":False},
                        {"name":"retention","case_insensitive":0,"table_function":False},
                        {"name":"reverse","case_insensitive":1,"table_function":False},
                        {"name":"reverseUTF8","case_insensitive":0,"table_function":False},
                        {"name":"revision","case_insensitive":1,"table_function":False},
                        {"name":"right","case_insensitive":1,"table_function":False},
                        {"name":"rightPad","case_insensitive":0,"table_function":False},
                        {"name":"rightPadUTF8","case_insensitive":0,"table_function":False},
                        {"name":"rightUTF8","case_insensitive":0,"table_function":False},
                        {"name":"round","case_insensitive":1,"table_function":False},
                        {"name":"roundAge","case_insensitive":0,"table_function":False},
                        {"name":"roundBankers","case_insensitive":0,"table_function":False},
                        {"name":"roundDown","case_insensitive":0,"table_function":False},
                        {"name":"roundDuration","case_insensitive":0,"table_function":False},
                        {"name":"roundToExp2","case_insensitive":0,"table_function":False},
                        {"name":"rowNumberInAllBlocks","case_insensitive":0,"table_function":False},
                        {"name":"rowNumberInBlock","case_insensitive":0,"table_function":False},
                        {"name":"row_number","case_insensitive":1,"table_function":False},
                        {"name":"rpad","case_insensitive":1,"table_function":False},
                        {"name":"rtrim","case_insensitive":0,"table_function":False},
                        {"name":"runningAccumulate","case_insensitive":0,"table_function":False},
                        {"name":"runningConcurrency","case_insensitive":0,"table_function":False},
                        {"name":"runningDifference","case_insensitive":0,"table_function":False},
                        {"name":"runningDifferenceStartingWithFirstValue","case_insensitive":0,"table_function":False},
                        {"name":"s2CapContains","case_insensitive":0,"table_function":False},
                        {"name":"s2CapUnion","case_insensitive":0,"table_function":False},
                        {"name":"s2CellsIntersect","case_insensitive":0,"table_function":False},
                        {"name":"s2GetNeighbors","case_insensitive":0,"table_function":False},
                        {"name":"s2RectAdd","case_insensitive":0,"table_function":False},
                        {"name":"s2RectContains","case_insensitive":0,"table_function":False},
                        {"name":"s2RectIntersection","case_insensitive":0,"table_function":False},
                        {"name":"s2RectUnion","case_insensitive":0,"table_function":False},
                        {"name":"s2ToGeo","case_insensitive":0,"table_function":False},
                        {"name":"s3","case_insensitive":0,"table_function":True},
                        {"name":"s3Cluster","case_insensitive":0,"table_function":True},
                        {"name":"scalarProduct","case_insensitive":1,"table_function":False},
                        {"name":"sequenceCount","case_insensitive":0,"table_function":False},
                        {"name":"sequenceMatch","case_insensitive":0,"table_function":False},
                        {"name":"sequenceNextNode","case_insensitive":0,"table_function":False},
                        {"name":"seriesDecomposeSTL","case_insensitive":0,"table_function":False},
                        {"name":"seriesOutliersDetectTukey","case_insensitive":0,"table_function":False},
                        {"name":"seriesPeriodDetectFFT","case_insensitive":0,"table_function":False},
                        {"name":"serverTimeZone","case_insensitive":0,"table_function":False},
                        {"name":"serverTimezone","case_insensitive":0,"table_function":False},
                        {"name":"serverUUID","case_insensitive":0,"table_function":False},
                        {"name":"shardCount","case_insensitive":0,"table_function":False},
                        {"name":"shardNum","case_insensitive":0,"table_function":False},
                        {"name":"showCertificate","case_insensitive":0,"table_function":False},
                        {"name":"sigmoid","case_insensitive":0,"table_function":False},
                        {"name":"sign","case_insensitive":1,"table_function":False},
                        {"name":"simpleJSONExtractBool","case_insensitive":0,"table_function":False},
                        {"name":"simpleJSONExtractFloat","case_insensitive":0,"table_function":False},
                        {"name":"simpleJSONExtractInt","case_insensitive":0,"table_function":False},
                        {"name":"simpleJSONExtractRaw","case_insensitive":0,"table_function":False},
                        {"name":"simpleJSONExtractString","case_insensitive":0,"table_function":False},
                        {"name":"simpleJSONExtractUInt","case_insensitive":0,"table_function":False},
                        {"name":"simpleJSONHas","case_insensitive":0,"table_function":False},
                        {"name":"simpleLinearRegression","case_insensitive":0,"table_function":False},
                        {"name":"sin","case_insensitive":1,"table_function":False},
                        {"name":"singleValueOrNull","case_insensitive":0,"table_function":False},
                        {"name":"sinh","case_insensitive":0,"table_function":False},
                        {"name":"sipHash128","case_insensitive":0,"table_function":False},
                        {"name":"sipHash128Keyed","case_insensitive":0,"table_function":False},
                        {"name":"sipHash128Reference","case_insensitive":0,"table_function":False},
                        {"name":"sipHash128ReferenceKeyed","case_insensitive":0,"table_function":False},
                        {"name":"sipHash64","case_insensitive":0,"table_function":False},
                        {"name":"sipHash64Keyed","case_insensitive":0,"table_function":False},
                        {"name":"skewPop","case_insensitive":0,"table_function":False},
                        {"name":"skewSamp","case_insensitive":0,"table_function":False},
                        {"name":"sleep","case_insensitive":0,"table_function":False},
                        {"name":"sleepEachRow","case_insensitive":0,"table_function":False},
                        {"name":"snowflakeToDateTime","case_insensitive":0,"table_function":False},
                        {"name":"snowflakeToDateTime64","case_insensitive":0,"table_function":False},
                        {"name":"soundex","case_insensitive":1,"table_function":False},
                        {"name":"space","case_insensitive":1,"table_function":False},
                        {"name":"sparkBar","case_insensitive":0,"table_function":False},
                        {"name":"sparkbar","case_insensitive":0,"table_function":False},
                        {"name":"splitByAlpha","case_insensitive":0,"table_function":False},
                        {"name":"splitByChar","case_insensitive":0,"table_function":False},
                        {"name":"splitByNonAlpha","case_insensitive":0,"table_function":False},
                        {"name":"splitByRegexp","case_insensitive":0,"table_function":False},
                        {"name":"splitByString","case_insensitive":0,"table_function":False},
                        {"name":"splitByWhitespace","case_insensitive":0,"table_function":False},
                        {"name":"sqid","case_insensitive":0,"table_function":False},
                        {"name":"sqidDecode","case_insensitive":0,"table_function":False},
                        {"name":"sqidEncode","case_insensitive":0,"table_function":False},
                        {"name":"sqlite","case_insensitive":0,"table_function":True},
                        {"name":"sqrt","case_insensitive":1,"table_function":False},
                        {"name":"startsWith","case_insensitive":0,"table_function":False},
                        {"name":"startsWithUTF8","case_insensitive":0,"table_function":False},
                        {"name":"stddevPop","case_insensitive":0,"table_function":False},
                        {"name":"stddevPopStable","case_insensitive":0,"table_function":False},
                        {"name":"stddevSamp","case_insensitive":0,"table_function":False},
                        {"name":"stddevSampStable","case_insensitive":0,"table_function":False},
                        {"name":"stem","case_insensitive":0,"table_function":False},
                        {"name":"stochasticLinearRegression","case_insensitive":0,"table_function":False},
                        {"name":"stochasticLogisticRegression","case_insensitive":0,"table_function":False},
                        {"name":"str_to_date","case_insensitive":1,"table_function":False},
                        {"name":"str_to_map","case_insensitive":1,"table_function":False},
                        {"name":"stringJaccardIndex","case_insensitive":0,"table_function":False},
                        {"name":"stringJaccardIndexUTF8","case_insensitive":0,"table_function":False},
                        {"name":"stringToH3","case_insensitive":0,"table_function":False},
                        {"name":"structureToCapnProtoSchema","case_insensitive":0,"table_function":False},
                        {"name":"structureToProtobufSchema","case_insensitive":0,"table_function":False},
                        {"name":"studentTTest","case_insensitive":0,"table_function":False},
                        {"name":"subBitmap","case_insensitive":0,"table_function":False},
                        {"name":"subDate","case_insensitive":1,"table_function":False},
                        {"name":"substr","case_insensitive":1,"table_function":False},
                        {"name":"substring","case_insensitive":1,"table_function":False},
                        {"name":"substringIndex","case_insensitive":0,"table_function":False},
                        {"name":"substringIndexUTF8","case_insensitive":0,"table_function":False},
                        {"name":"substringUTF8","case_insensitive":0,"table_function":False},
                        {"name":"subtractDays","case_insensitive":0,"table_function":False},
                        {"name":"subtractHours","case_insensitive":0,"table_function":False},
                        {"name":"subtractInterval","case_insensitive":0,"table_function":False},
                        {"name":"subtractMicroseconds","case_insensitive":0,"table_function":False},
                        {"name":"subtractMilliseconds","case_insensitive":0,"table_function":False},
                        {"name":"subtractMinutes","case_insensitive":0,"table_function":False},
                        {"name":"subtractMonths","case_insensitive":0,"table_function":False},
                        {"name":"subtractNanoseconds","case_insensitive":0,"table_function":False},
                        {"name":"subtractQuarters","case_insensitive":0,"table_function":False},
                        {"name":"subtractSeconds","case_insensitive":0,"table_function":False},
                        {"name":"subtractTupleOfIntervals","case_insensitive":0,"table_function":False},
                        {"name":"subtractWeeks","case_insensitive":0,"table_function":False},
                        {"name":"subtractYears","case_insensitive":0,"table_function":False},
                        {"name":"sum","case_insensitive":1,"table_function":False},
                        {"name":"sumCount","case_insensitive":0,"table_function":False},
                        {"name":"sumKahan","case_insensitive":0,"table_function":False},
                        {"name":"sumMapFiltered","case_insensitive":0,"table_function":False},
                        {"name":"sumMapFilteredWithOverflow","case_insensitive":0,"table_function":False},
                        {"name":"sumMapWithOverflow","case_insensitive":0,"table_function":False},
                        {"name":"sumMappedArrays","case_insensitive":0,"table_function":False},
                        {"name":"sumWithOverflow","case_insensitive":0,"table_function":False},
                        {"name":"svg","case_insensitive":0,"table_function":False},
                        {"name":"synonyms","case_insensitive":1,"table_function":False},
                        {"name":"tan","case_insensitive":1,"table_function":False},
                        {"name":"tanh","case_insensitive":1,"table_function":False},
                        {"name":"tcpPort","case_insensitive":0,"table_function":False},
                        {"name":"tgamma","case_insensitive":0,"table_function":False},
                        {"name":"theilsU","case_insensitive":0,"table_function":False},
                        {"name":"throwIf","case_insensitive":0,"table_function":False},
                        {"name":"tid","case_insensitive":0,"table_function":False},
                        {"name":"timeDiff","case_insensitive":1,"table_function":False},
                        {"name":"timeSlot","case_insensitive":0,"table_function":False},
                        {"name":"timeSlots","case_insensitive":0,"table_function":False},
                        {"name":"timeZone","case_insensitive":0,"table_function":False},
                        {"name":"timeZoneOf","case_insensitive":0,"table_function":False},
                        {"name":"timeZoneOffset","case_insensitive":0,"table_function":False},
                        {"name":"timestamp","case_insensitive":1,"table_function":False},
                        {"name":"timestampDiff","case_insensitive":0,"table_function":False},
                        {"name":"timestamp_diff","case_insensitive":0,"table_function":False},
                        {"name":"timezone","case_insensitive":0,"table_function":False},
                        {"name":"timezoneOf","case_insensitive":0,"table_function":False},
                        {"name":"timezoneOffset","case_insensitive":0,"table_function":False},
                        {"name":"toBool","case_insensitive":0,"table_function":False},
                        {"name":"toColumnTypeName","case_insensitive":0,"table_function":False},
                        {"name":"toDate","case_insensitive":0,"table_function":False},
                        {"name":"toDate32","case_insensitive":0,"table_function":False},
                        {"name":"toDate32OrDefault","case_insensitive":0,"table_function":False},
                        {"name":"toDate32OrNull","case_insensitive":0,"table_function":False},
                        {"name":"toDate32OrZero","case_insensitive":0,"table_function":False},
                        {"name":"toDateOrDefault","case_insensitive":0,"table_function":False},
                        {"name":"toDateOrNull","case_insensitive":0,"table_function":False},
                        {"name":"toDateOrZero","case_insensitive":0,"table_function":False},
                        {"name":"toDateTime","case_insensitive":0,"table_function":False},
                        {"name":"toDateTime32","case_insensitive":0,"table_function":False},
                        {"name":"toDateTime64","case_insensitive":0,"table_function":False},
                        {"name":"toDateTime64OrDefault","case_insensitive":0,"table_function":False},
                        {"name":"toDateTime64OrNull","case_insensitive":0,"table_function":False},
                        {"name":"toDateTime64OrZero","case_insensitive":0,"table_function":False},
                        {"name":"toDateTimeOrDefault","case_insensitive":0,"table_function":False},
                        {"name":"toDateTimeOrNull","case_insensitive":0,"table_function":False},
                        {"name":"toDateTimeOrZero","case_insensitive":0,"table_function":False},
                        {"name":"toDayOfMonth","case_insensitive":0,"table_function":False},
                        {"name":"toDayOfWeek","case_insensitive":0,"table_function":False},
                        {"name":"toDayOfYear","case_insensitive":0,"table_function":False},
                        {"name":"toDaysSinceYearZero","case_insensitive":0,"table_function":False},
                        {"name":"toDecimal128","case_insensitive":0,"table_function":False},
                        {"name":"toDecimal128OrDefault","case_insensitive":0,"table_function":False},
                        {"name":"toDecimal128OrNull","case_insensitive":0,"table_function":False},
                        {"name":"toDecimal128OrZero","case_insensitive":0,"table_function":False},
                        {"name":"toDecimal256","case_insensitive":0,"table_function":False},
                        {"name":"toDecimal256OrDefault","case_insensitive":0,"table_function":False},
                        {"name":"toDecimal256OrNull","case_insensitive":0,"table_function":False},
                        {"name":"toDecimal256OrZero","case_insensitive":0,"table_function":False},
                        {"name":"toDecimal32","case_insensitive":0,"table_function":False},
                        {"name":"toDecimal32OrDefault","case_insensitive":0,"table_function":False},
                        {"name":"toDecimal32OrNull","case_insensitive":0,"table_function":False},
                        {"name":"toDecimal32OrZero","case_insensitive":0,"table_function":False},
                        {"name":"toDecimal64","case_insensitive":0,"table_function":False},
                        {"name":"toDecimal64OrDefault","case_insensitive":0,"table_function":False},
                        {"name":"toDecimal64OrNull","case_insensitive":0,"table_function":False},
                        {"name":"toDecimal64OrZero","case_insensitive":0,"table_function":False},
                        {"name":"toDecimalString","case_insensitive":1,"table_function":False},
                        {"name":"toFixedString","case_insensitive":0,"table_function":False},
                        {"name":"toFloat32","case_insensitive":0,"table_function":False},
                        {"name":"toFloat32OrDefault","case_insensitive":0,"table_function":False},
                        {"name":"toFloat32OrNull","case_insensitive":0,"table_function":False},
                        {"name":"toFloat32OrZero","case_insensitive":0,"table_function":False},
                        {"name":"toFloat64","case_insensitive":0,"table_function":False},
                        {"name":"toFloat64OrDefault","case_insensitive":0,"table_function":False},
                        {"name":"toFloat64OrNull","case_insensitive":0,"table_function":False},
                        {"name":"toFloat64OrZero","case_insensitive":0,"table_function":False},
                        {"name":"toHour","case_insensitive":0,"table_function":False},
                        {"name":"toIPv4","case_insensitive":0,"table_function":False},
                        {"name":"toIPv4OrDefault","case_insensitive":0,"table_function":False},
                        {"name":"toIPv4OrNull","case_insensitive":0,"table_function":False},
                        {"name":"toIPv4OrZero","case_insensitive":0,"table_function":False},
                        {"name":"toIPv6","case_insensitive":0,"table_function":False},
                        {"name":"toIPv6OrDefault","case_insensitive":0,"table_function":False},
                        {"name":"toIPv6OrNull","case_insensitive":0,"table_function":False},
                        {"name":"toIPv6OrZero","case_insensitive":0,"table_function":False},
                        {"name":"toISOWeek","case_insensitive":0,"table_function":False},
                        {"name":"toISOYear","case_insensitive":0,"table_function":False},
                        {"name":"toInt128","case_insensitive":0,"table_function":False},
                        {"name":"toInt128OrDefault","case_insensitive":0,"table_function":False},
                        {"name":"toInt128OrNull","case_insensitive":0,"table_function":False},
                        {"name":"toInt128OrZero","case_insensitive":0,"table_function":False},
                        {"name":"toInt16","case_insensitive":0,"table_function":False},
                        {"name":"toInt16OrDefault","case_insensitive":0,"table_function":False},
                        {"name":"toInt16OrNull","case_insensitive":0,"table_function":False},
                        {"name":"toInt16OrZero","case_insensitive":0,"table_function":False},
                        {"name":"toInt256","case_insensitive":0,"table_function":False},
                        {"name":"toInt256OrDefault","case_insensitive":0,"table_function":False},
                        {"name":"toInt256OrNull","case_insensitive":0,"table_function":False},
                        {"name":"toInt256OrZero","case_insensitive":0,"table_function":False},
                        {"name":"toInt32","case_insensitive":0,"table_function":False},
                        {"name":"toInt32OrDefault","case_insensitive":0,"table_function":False},
                        {"name":"toInt32OrNull","case_insensitive":0,"table_function":False},
                        {"name":"toInt32OrZero","case_insensitive":0,"table_function":False},
                        {"name":"toInt64","case_insensitive":0,"table_function":False},
                        {"name":"toInt64OrDefault","case_insensitive":0,"table_function":False},
                        {"name":"toInt64OrNull","case_insensitive":0,"table_function":False},
                        {"name":"toInt64OrZero","case_insensitive":0,"table_function":False},
                        {"name":"toInt8","case_insensitive":0,"table_function":False},
                        {"name":"toInt8OrDefault","case_insensitive":0,"table_function":False},
                        {"name":"toInt8OrNull","case_insensitive":0,"table_function":False},
                        {"name":"toInt8OrZero","case_insensitive":0,"table_function":False},
                        {"name":"toIntervalDay","case_insensitive":0,"table_function":False},
                        {"name":"toIntervalHour","case_insensitive":0,"table_function":False},
                        {"name":"toIntervalMicrosecond","case_insensitive":0,"table_function":False},
                        {"name":"toIntervalMillisecond","case_insensitive":0,"table_function":False},
                        {"name":"toIntervalMinute","case_insensitive":0,"table_function":False},
                        {"name":"toIntervalMonth","case_insensitive":0,"table_function":False},
                        {"name":"toIntervalNanosecond","case_insensitive":0,"table_function":False},
                        {"name":"toIntervalQuarter","case_insensitive":0,"table_function":False},
                        {"name":"toIntervalSecond","case_insensitive":0,"table_function":False},
                        {"name":"toIntervalWeek","case_insensitive":0,"table_function":False},
                        {"name":"toIntervalYear","case_insensitive":0,"table_function":False},
                        {"name":"toJSONString","case_insensitive":0,"table_function":False},
                        {"name":"toLastDayOfMonth","case_insensitive":0,"table_function":False},
                        {"name":"toLastDayOfWeek","case_insensitive":0,"table_function":False},
                        {"name":"toLowCardinality","case_insensitive":0,"table_function":False},
                        {"name":"toMinute","case_insensitive":0,"table_function":False},
                        {"name":"toModifiedJulianDay","case_insensitive":0,"table_function":False},
                        {"name":"toModifiedJulianDayOrNull","case_insensitive":0,"table_function":False},
                        {"name":"toMonday","case_insensitive":0,"table_function":False},
                        {"name":"toMonth","case_insensitive":0,"table_function":False},
                        {"name":"toNullable","case_insensitive":0,"table_function":False},
                        {"name":"toQuarter","case_insensitive":0,"table_function":False},
                        {"name":"toRelativeDayNum","case_insensitive":0,"table_function":False},
                        {"name":"toRelativeHourNum","case_insensitive":0,"table_function":False},
                        {"name":"toRelativeMinuteNum","case_insensitive":0,"table_function":False},
                        {"name":"toRelativeMonthNum","case_insensitive":0,"table_function":False},
                        {"name":"toRelativeQuarterNum","case_insensitive":0,"table_function":False},
                        {"name":"toRelativeSecondNum","case_insensitive":0,"table_function":False},
                        {"name":"toRelativeWeekNum","case_insensitive":0,"table_function":False},
                        {"name":"toRelativeYearNum","case_insensitive":0,"table_function":False},
                        {"name":"toSecond","case_insensitive":0,"table_function":False},
                        {"name":"toStartOfDay","case_insensitive":0,"table_function":False},
                        {"name":"toStartOfFifteenMinutes","case_insensitive":0,"table_function":False},
                        {"name":"toStartOfFiveMinute","case_insensitive":0,"table_function":False},
                        {"name":"toStartOfFiveMinutes","case_insensitive":0,"table_function":False},
                        {"name":"toStartOfHour","case_insensitive":0,"table_function":False},
                        {"name":"toStartOfISOYear","case_insensitive":0,"table_function":False},
                        {"name":"toStartOfInterval","case_insensitive":0,"table_function":False},
                        {"name":"toStartOfMicrosecond","case_insensitive":0,"table_function":False},
                        {"name":"toStartOfMillisecond","case_insensitive":0,"table_function":False},
                        {"name":"toStartOfMinute","case_insensitive":0,"table_function":False},
                        {"name":"toStartOfMonth","case_insensitive":0,"table_function":False},
                        {"name":"toStartOfNanosecond","case_insensitive":0,"table_function":False},
                        {"name":"toStartOfQuarter","case_insensitive":0,"table_function":False},
                        {"name":"toStartOfSecond","case_insensitive":0,"table_function":False},
                        {"name":"toStartOfTenMinutes","case_insensitive":0,"table_function":False},
                        {"name":"toStartOfWeek","case_insensitive":0,"table_function":False},
                        {"name":"toStartOfYear","case_insensitive":0,"table_function":False},
                        {"name":"toString","case_insensitive":0,"table_function":False},
                        {"name":"toStringCutToZero","case_insensitive":0,"table_function":False},
                        {"name":"toTime","case_insensitive":0,"table_function":False},
                        {"name":"toTimeZone","case_insensitive":0,"table_function":False},
                        {"name":"toTimezone","case_insensitive":0,"table_function":False},
                        {"name":"toTypeName","case_insensitive":0,"table_function":False},
                        {"name":"toUInt128","case_insensitive":0,"table_function":False},
                        {"name":"toUInt128OrNull","case_insensitive":0,"table_function":False},
                        {"name":"toUInt128OrZero","case_insensitive":0,"table_function":False},
                        {"name":"toUInt16","case_insensitive":0,"table_function":False},
                        {"name":"toUInt16OrDefault","case_insensitive":0,"table_function":False},
                        {"name":"toUInt16OrNull","case_insensitive":0,"table_function":False},
                        {"name":"toUInt16OrZero","case_insensitive":0,"table_function":False},
                        {"name":"toUInt256","case_insensitive":0,"table_function":False},
                        {"name":"toUInt256OrDefault","case_insensitive":0,"table_function":False},
                        {"name":"toUInt256OrNull","case_insensitive":0,"table_function":False},
                        {"name":"toUInt256OrZero","case_insensitive":0,"table_function":False},
                        {"name":"toUInt32","case_insensitive":0,"table_function":False},
                        {"name":"toUInt32OrDefault","case_insensitive":0,"table_function":False},
                        {"name":"toUInt32OrNull","case_insensitive":0,"table_function":False},
                        {"name":"toUInt32OrZero","case_insensitive":0,"table_function":False},
                        {"name":"toUInt64","case_insensitive":0,"table_function":False},
                        {"name":"toUInt64OrDefault","case_insensitive":0,"table_function":False},
                        {"name":"toUInt64OrNull","case_insensitive":0,"table_function":False},
                        {"name":"toUInt64OrZero","case_insensitive":0,"table_function":False},
                        {"name":"toUInt8","case_insensitive":0,"table_function":False},
                        {"name":"toUInt8OrDefault","case_insensitive":0,"table_function":False},
                        {"name":"toUInt8OrNull","case_insensitive":0,"table_function":False},
                        {"name":"toUInt8OrZero","case_insensitive":0,"table_function":False},
                        {"name":"toUTCTimestamp","case_insensitive":0,"table_function":False},
                        {"name":"toUUID","case_insensitive":0,"table_function":False},
                        {"name":"toUUIDOrDefault","case_insensitive":0,"table_function":False},
                        {"name":"toUUIDOrNull","case_insensitive":0,"table_function":False},
                        {"name":"toUUIDOrZero","case_insensitive":0,"table_function":False},
                        {"name":"toUnixTimestamp","case_insensitive":0,"table_function":False},
                        {"name":"toUnixTimestamp64Micro","case_insensitive":0,"table_function":False},
                        {"name":"toUnixTimestamp64Milli","case_insensitive":0,"table_function":False},
                        {"name":"toUnixTimestamp64Nano","case_insensitive":0,"table_function":False},
                        {"name":"toValidUTF8","case_insensitive":0,"table_function":False},
                        {"name":"toWeek","case_insensitive":0,"table_function":False},
                        {"name":"toYYYYMM","case_insensitive":0,"table_function":False},
                        {"name":"toYYYYMMDD","case_insensitive":0,"table_function":False},
                        {"name":"toYYYYMMDDhhmmss","case_insensitive":0,"table_function":False},
                        {"name":"toYear","case_insensitive":0,"table_function":False},
                        {"name":"toYearWeek","case_insensitive":0,"table_function":False},
                        {"name":"to_utc_timestamp","case_insensitive":1,"table_function":False},
                        {"name":"today","case_insensitive":0,"table_function":False},
                        {"name":"tokens","case_insensitive":0,"table_function":False},
                        {"name":"topK","case_insensitive":0,"table_function":False},
                        {"name":"topKWeighted","case_insensitive":0,"table_function":False},
                        {"name":"topLevelDomain","case_insensitive":0,"table_function":False},
                        {"name":"topLevelDomainRFC","case_insensitive":0,"table_function":False},
                        {"name":"transactionID","case_insensitive":0,"table_function":False},
                        {"name":"transactionLatestSnapshot","case_insensitive":0,"table_function":False},
                        {"name":"transactionOldestSnapshot","case_insensitive":0,"table_function":False},
                        {"name":"transform","case_insensitive":0,"table_function":False},
                        {"name":"translate","case_insensitive":0,"table_function":False},
                        {"name":"translateUTF8","case_insensitive":0,"table_function":False},
                        {"name":"trim","case_insensitive":0,"table_function":False},
                        {"name":"trimBoth","case_insensitive":0,"table_function":False},
                        {"name":"trimLeft","case_insensitive":0,"table_function":False},
                        {"name":"trimRight","case_insensitive":0,"table_function":False},
                        {"name":"trunc","case_insensitive":1,"table_function":False},
                        {"name":"truncate","case_insensitive":1,"table_function":False},
                        {"name":"tryBase58Decode","case_insensitive":0,"table_function":False},
                        {"name":"tryBase64Decode","case_insensitive":0,"table_function":False},
                        {"name":"tryDecrypt","case_insensitive":0,"table_function":False},
                        {"name":"tryIdnaEncode","case_insensitive":0,"table_function":False},
                        {"name":"tryPunycodeDecode","case_insensitive":0,"table_function":False},
                        {"name":"tumble","case_insensitive":0,"table_function":False},
                        {"name":"tumbleEnd","case_insensitive":0,"table_function":False},
                        {"name":"tumbleStart","case_insensitive":0,"table_function":False},
                        {"name":"tuple","case_insensitive":0,"table_function":False},
                        {"name":"tupleConcat","case_insensitive":0,"table_function":False},
                        {"name":"tupleDivide","case_insensitive":0,"table_function":False},
                        {"name":"tupleDivideByNumber","case_insensitive":0,"table_function":False},
                        {"name":"tupleElement","case_insensitive":0,"table_function":False},
                        {"name":"tupleHammingDistance","case_insensitive":0,"table_function":False},
                        {"name":"tupleIntDiv","case_insensitive":0,"table_function":False},
                        {"name":"tupleIntDivByNumber","case_insensitive":0,"table_function":False},
                        {"name":"tupleIntDivOrZero","case_insensitive":0,"table_function":False},
                        {"name":"tupleIntDivOrZeroByNumber","case_insensitive":0,"table_function":False},
                        {"name":"tupleMinus","case_insensitive":0,"table_function":False},
                        {"name":"tupleModulo","case_insensitive":0,"table_function":False},
                        {"name":"tupleModuloByNumber","case_insensitive":0,"table_function":False},
                        {"name":"tupleMultiply","case_insensitive":0,"table_function":False},
                        {"name":"tupleMultiplyByNumber","case_insensitive":0,"table_function":False},
                        {"name":"tupleNegate","case_insensitive":0,"table_function":False},
                        {"name":"tuplePlus","case_insensitive":0,"table_function":False},
                        {"name":"tupleToNameValuePairs","case_insensitive":0,"table_function":False},
                        {"name":"ucase","case_insensitive":1,"table_function":False},
                        {"name":"unbin","case_insensitive":1,"table_function":False},
                        {"name":"unhex","case_insensitive":1,"table_function":False},
                        {"name":"uniq","case_insensitive":0,"table_function":False},
                        {"name":"uniqCombined","case_insensitive":0,"table_function":False},
                        {"name":"uniqCombined64","case_insensitive":0,"table_function":False},
                        {"name":"uniqExact","case_insensitive":0,"table_function":False},
                        {"name":"uniqHLL12","case_insensitive":0,"table_function":False},
                        {"name":"uniqTheta","case_insensitive":0,"table_function":False},
                        {"name":"uniqThetaIntersect","case_insensitive":0,"table_function":False},
                        {"name":"uniqThetaNot","case_insensitive":0,"table_function":False},
                        {"name":"uniqThetaUnion","case_insensitive":0,"table_function":False},
                        {"name":"uniqUpTo","case_insensitive":0,"table_function":False},
                        {"name":"upper","case_insensitive":1,"table_function":False},
                        {"name":"upperUTF8","case_insensitive":0,"table_function":False},
                        {"name":"uptime","case_insensitive":0,"table_function":False},
                        {"name":"url","case_insensitive":0,"table_function":True},
                        {"name":"urlCluster","case_insensitive":0,"table_function":True},
                        {"name":"user","case_insensitive":1,"table_function":False},
                        {"name":"validateNestedArraySizes","case_insensitive":0,"table_function":False},
                        {"name":"values","case_insensitive":0,"table_function":True},
                        {"name":"varPop","case_insensitive":0,"table_function":False},
                        {"name":"varPopStable","case_insensitive":0,"table_function":False},
                        {"name":"varSamp","case_insensitive":0,"table_function":False},
                        {"name":"varSampStable","case_insensitive":0,"table_function":False},
                        {"name":"variantElement","case_insensitive":0,"table_function":False},
                        {"name":"variantType","case_insensitive":0,"table_function":False},
                        {"name":"vectorDifference","case_insensitive":1,"table_function":False},
                        {"name":"vectorSum","case_insensitive":1,"table_function":False},
                        {"name":"version","case_insensitive":1,"table_function":False},
                        {"name":"view","case_insensitive":0,"table_function":True},
                        {"name":"viewExplain","case_insensitive":0,"table_function":True},
                        {"name":"viewIfPermitted","case_insensitive":0,"table_function":True},
                        {"name":"visibleWidth","case_insensitive":0,"table_function":False},
                        {"name":"visitParamExtractBool","case_insensitive":0,"table_function":False},
                        {"name":"visitParamExtractFloat","case_insensitive":0,"table_function":False},
                        {"name":"visitParamExtractInt","case_insensitive":0,"table_function":False},
                        {"name":"visitParamExtractRaw","case_insensitive":0,"table_function":False},
                        {"name":"visitParamExtractString","case_insensitive":0,"table_function":False},
                        {"name":"visitParamExtractUInt","case_insensitive":0,"table_function":False},
                        {"name":"visitParamHas","case_insensitive":0,"table_function":False},
                        {"name":"week","case_insensitive":1,"table_function":False},
                        {"name":"welchTTest","case_insensitive":0,"table_function":False},
                        {"name":"widthBucket","case_insensitive":0,"table_function":False},
                        {"name":"width_bucket","case_insensitive":1,"table_function":False},
                        {"name":"windowFunnel","case_insensitive":0,"table_function":False},
                        {"name":"windowID","case_insensitive":0,"table_function":False},
                        {"name":"wkt","case_insensitive":0,"table_function":False},
                        {"name":"wordShingleMinHash","case_insensitive":0,"table_function":False},
                        {"name":"wordShingleMinHashArg","case_insensitive":0,"table_function":False},
                        {"name":"wordShingleMinHashArgCaseInsensitive","case_insensitive":0,"table_function":False},
                        {"name":"wordShingleMinHashArgCaseInsensitiveUTF8","case_insensitive":0,"table_function":False},
                        {"name":"wordShingleMinHashArgUTF8","case_insensitive":0,"table_function":False},
                        {"name":"wordShingleMinHashCaseInsensitive","case_insensitive":0,"table_function":False},
                        {"name":"wordShingleMinHashCaseInsensitiveUTF8","case_insensitive":0,"table_function":False},
                        {"name":"wordShingleMinHashUTF8","case_insensitive":0,"table_function":False},
                        {"name":"wordShingleSimHash","case_insensitive":0,"table_function":False},
                        {"name":"wordShingleSimHashCaseInsensitive","case_insensitive":0,"table_function":False},
                        {"name":"wordShingleSimHashCaseInsensitiveUTF8","case_insensitive":0,"table_function":False},
                        {"name":"wordShingleSimHashUTF8","case_insensitive":0,"table_function":False},
                        {"name":"wyHash64","case_insensitive":0,"table_function":False},
                        {"name":"xor","case_insensitive":0,"table_function":False},
                        {"name":"xxHash32","case_insensitive":0,"table_function":False},
                        {"name":"xxHash64","case_insensitive":0,"table_function":False},
                        {"name":"xxh3","case_insensitive":0,"table_function":False},
                        {"name":"yandexConsistentHash","case_insensitive":0,"table_function":False},
                        {"name":"yearweek","case_insensitive":1,"table_function":False},
                        {"name":"yesterday","case_insensitive":0,"table_function":False},
                        {"name":"zeros","case_insensitive":0,"table_function":True},
                        {"name":"zeros_mt","case_insensitive":0,"table_function":True},
                        {"name":"zookeeperSessionUptime","case_insensitive":0,"table_function":False},]

        for ob in CH_FUNCTIONS:
            name = ob['name']
            insensitive = ob['case_insensitive']
            table_function = ob['table_function']
            with self.subTest(name):
                try:
                    if table_function:
                        if name.startswith('view'):
                            pass  # Tested in test_throws_with_view
                        else:
                            chquery.tables(f"SELECT * FROM {name}('tinybird', 'public', 'table')")
                    else:
                        if name in ['ltrim', 'rtrim', 'trim']:
                            chquery.tables(f"SELECT {name}(number) from numbers(1)")
                        else:
                            chquery.tables(f"SELECT {name}(number, number) from numbers(1)")
                except Exception as e:
                    error_msg = str(e)
                    if not error_msg.endswith('is restricted. Contact support@tinybird.co if you require access to this feature'):
                        self.fail(f"{name} failed: {error_msg}")

                if insensitive:
                    try:
                        chquery.tables(f"SELECT {name.upper()}(number, number) from numbers(1)")
                    except Exception as e:
                        error_msg = str(e)
                        if not error_msg.endswith('is restricted. Contact support@tinybird.co if you require access to this feature'):
                            self.fail(f"{name} failed: {error_msg}")

                    try:
                        chquery.tables(f"SELECT {name.lower()}(number, number) from numbers(1)")
                    except Exception as e:
                        error_msg = str(e)
                        if not error_msg.endswith('is restricted. Contact support@tinybird.co if you require access to this feature'):
                            self.fail(f"{name} failed: {error_msg}")

                self.assertTrue(1)

    def test_special_functions(self):
        """Tests functions that are used in any special way inside ClickHouse"""

        # lambda
        self.assertEqual(chquery.tables("""
                            SELECT arrayMap(x -> finalizeAggregation(x), state)
                            FROM
                            (
                                SELECT sumStateResample(0, 20, 1)(id, id % 20) AS state
                                FROM default.join_test
                            )"""),
                         [('default', 'join_test', '')])

        # tuple
        self.assertEqual(chquery.tables("""SELECT (number, number) FROM numbers(1)"""),
                         [('', '', 'numbers')])

        # tupleElement
        self.assertEqual(chquery.tables("""SELECT tupleElement((number, number), 1) FROM numbers(1)"""),
                         [('', '', 'numbers')])

        # array
        self.assertEqual(chquery.tables("""SELECT [number] FROM numbers(1)"""),
                         [('', '', 'numbers')])

        # divide
        self.assertEqual(chquery.tables("""SELECT number / number FROM numbers(1)"""),
                         [('', '', 'numbers')])

        # arrayJoin
        self.assertEqual(chquery.tables("""SELECT arrayJoin([1, 2, 3] AS src) AS dst, 'Hello', src"""),
                         [])

        # and
        self.assertEqual(chquery.tables("""SELECT number and number FROM numbers(1)"""),
                         [('', '', 'numbers')])

        # or
        self.assertEqual(chquery.tables("""SELECT number or number FROM numbers(1)"""),
                         [('', '', 'numbers')])

        # untuple
        self.assertEqual(chquery.tables("""SELECT untuple(a) FROM (SELECT (1, 2) AS a)"""),
                         [])

        # exists
        self.assertEqual(chquery.tables("""SELECT count() FROM database1.table1 WHERE exists(SELECT id FROM database2.table2)"""),
                         [('database1', 'table1', ''), ('database2', 'table2', '')])

        # grouping
        self.assertEqual(chquery.tables("""
                            SELECT
                                if(grouping(pk2) = 1, 'pk1, pk2', 'pk1, pk3') AS name,
                                table1.pk1 AS pk1,
                                table1.pk2 AS pk2,
                                table1.pk3 AS pk3,
                                count()
                            FROM table1
                            GROUP BY
                                GROUPING SETS (
                                    (pk1, pk2),
                                    (pk1, pk3)
                                )
                         """), [('', 'table1', '')])

        # REGEXP can only used in Merge Engine declaration
        # self.assertEqual(chquery.tables("""CREATE TABLE all_visitors (id UInt32)
        #                                    ENGINE=Merge(REGEXP('ABC_*'), 'visitors')"""),
        #                  [('', '', '')])

        # indexHint
        with self.assertRaisesRegex(ValueError, """DB::Exception: Usage of function indexHint is restricted"""):
            chquery.tables("SELECT * FROM numbers(10) WHERE indexHint(number IN (SELECT * FROM table))")

    def test_blocked_functions(self):
        with self.assertRaisesRegex(ValueError, """DB::Exception: Usage of function currentUser is restricted"""):
            chquery.tables("SELECT currentUser() from numbers(11)")

    def test_disabled_functions_when_function_validation_is_off(self):
        self.assertEqual(chquery.tables("SELECT currentUser() from numbers(11)", validate_functions=False),
                         [('', '', 'numbers')])

    def test_allow_functions(self):
        self.assertEqual(chquery.tables("SELECT currentUser() from numbers(11)", function_allow_list=['currentUser']),
                         [('', '', 'numbers')])

        with self.assertRaisesRegex(ValueError, """DB::Exception: Usage of function currentUser is restricted"""):
            chquery.tables("SELECT currentUser() from numbers(11)", function_allow_list=['otherFunction'])

    def test_allow_unknown_function(self):
        self.assertEqual(chquery.tables("SELECT randomFunctionThatDoesNotExist() from numbers(11)",
                                        function_allow_list=['randomFunctionThatDoesNotExist']),
                         [('', '', 'numbers')])

    def test_deny_functions(self):
        with self.assertRaisesRegex(ValueError, """DB::Exception: Usage of function sum is restricted"""):
            chquery.tables("SELECT sum(number) from numbers(11)", function_deny_list=['AVG', 'sum', 'remote'])

    def test_block_settings(self):
        with self.assertRaisesRegex(ValueError, """DB::Exception: Usage of setting 'max_block_size' is restricted. Contact support@tinybird.co if you require access to this feature"""):
            chquery.tables("SELECT count() from system.numbers LIMIT 2 SETTINGS max_block_size=1")

        with self.assertRaisesRegex(ValueError, """DB::Exception: Usage of setting 'max_block_size' is restricted. Contact support@tinybird.co if you require access to this feature"""):
            chquery.tables("SELECT * FROM (SELECT count() from system.numbers LIMIT 2 SETTINGS max_block_size=1)")

        with self.assertRaisesRegex(ValueError, """DB::Exception: Usage of setting 'Join_use_nulls' is restricted. Contact support@tinybird.co if you require access to this feature"""):
            chquery.tables("SELECT count() from system.numbers LIMIT 2 SETTINGS Join_use_nulls=1")

    def test_allow_ignoring_settings(self):
        self.assertEqual(chquery.tables("SELECT count() from system.numbers LIMIT 2 SETTINGS max_block_size=1",
                                        validate_query_settings=False),
                         [('system', 'numbers', '')])

        self.assertEqual(chquery.tables("SELECT count() from system.numbers LIMIT 2 SETTINGS max_block_size=1",
                                        validate_query_settings=True, query_settings_allow_list=['max_block_size']),
                         [('system', 'numbers', '')])

    def test_allow_enabled_settings(self):
        self.assertEqual(chquery.tables("SELECT count() from system.numbers SETTINGS aggregate_functions_null_for_empty=1"),
                         [('system', 'numbers', '')])

    def test_allow_analytics_query_settings(self):
        sql = """SELECT count() FROM system.numbers LIMIT 1 SETTINGS
            max_threads = 1,
            max_memory_usage = 1000000,
            max_execution_time = 60,
            optimize_aggregation_in_order = 1,
            use_skip_indexes = 1,
            use_skip_indexes_if_final = 0,
            optimize_move_to_prewhere = 1,
            query_plan_optimize_lazy_materialization = 0,
            min_bytes_to_use_direct_io = 0,
            enable_filesystem_cache = 1,
            use_query_cache = 0,
            use_query_condition_cache = 0
        """
        self.assertEqual(chquery.tables(sql), [('system', 'numbers', '')])

    def test_disallow_blocked_settings(self):
        with self.assertRaisesRegex(ValueError, """DB::Exception: Usage of setting 'aggregate_functions_null_for_empty' is restricted. Contact support@tinybird.co if you require access to this feature"""):
            chquery.tables("SELECT count() from system.numbers SETTINGS aggregate_functions_null_for_empty=1",
                           query_settings_deny_list=['aggregate_functions_null_for_empty'])

    def test_disallow_invalid_value(self):
        with self.assertRaisesRegex(ValueError, """DB::Exception: Cannot parse bool from string 'aaaaaaa'"""):
            chquery.tables("SELECT count() from system.numbers SETTINGS aggregate_functions_null_for_empty='aaaaaaa'")

    def test_cte_escape(self):
        tables = chquery.tables("WITH table1 AS (SELECT * FROM table1) SELECT * FROM table1")
        self.assertEqual(tables, [('', 'table1', '')])

    def test_cte_escape_nested(self):
        tables = chquery.tables("WITH table1 AS (WITH table2 AS (SELECT * FROM table1) SELECT * FROM table2) SELECT * from table1")
        self.assertEqual(tables, [('', 'table1', '')])

    def test_cte_escape_db(self):
        tables = chquery.tables("WITH table1 AS (SELECT * FROM other.table1) SELECT * FROM table1")
        self.assertEqual(tables, [('other', 'table1', '')])

    def test_cte_escape_db2(self):
        tables = chquery.tables("WITH table1 AS (SELECT * FROM other.table2) SELECT * FROM table1")
        self.assertEqual(tables, [('other', 'table2', '')])

    def test_cte_escape_scalar(self):
        tables = chquery.tables("WITH (SELECT COUNT(*) FROM table2) as table2 SELECT table2")
        self.assertEqual(tables, [('', 'table2', '')])

    def test_cte_escape_scalar2(self):
        tables = chquery.tables("WITH (SELECT COUNT(*) FROM table2) as table1 SELECT * FROM table1")
        self.assertEqual(tables, [('', 'table1', ''), ('', 'table2', '')])

    def test_cte_siblings(self):
        tables = chquery.tables("WITH alias1 as (select * from table1), alias2 as (select * from alias1) select * from alias2")
        self.assertEqual(tables, [('', 'table1', '')])

    def test_cte_siblings_wrong_order(self):
        tables = chquery.tables("WITH alias2 as (select * from alias1), alias1 as (select * from table1) select * from alias2")
        self.assertEqual(tables, [('', 'alias1', ''), ('', 'table1', '')])

    def test_cte_homonym_aliases(self):
        tables = chquery.tables("WITH 1 as table1, table1 as (select * from table1) select * from table1")
        self.assertEqual(tables, [('', 'table1', '')])

    def test_cte_homonym_aliases2(self):
        tables = chquery.tables("WITH table1 as (select * from table1), 1 as table1 select * from table1")
        self.assertEqual(tables, [('', 'table1', '')])

    def test_cte_escape_literal(self):
        tables = chquery.tables("WITH 2 as table1 SELECT * FROM table1")
        self.assertEqual(tables, [('', 'table1', '')])

    def test_cte_escape_literal2(self):
        tables = chquery.tables("WITH 2 as table1 SELECT table1")
        self.assertEqual(tables, [])

    def test_cte_with_enable_global_with_statement_off(self):
        tables = chquery.tables("WITH (select * from table2 limit 1) as table1 select * from (select 1 as v where v in table1)")
        self.assertEqual(tables, [('', 'table1', ''), ('', 'table2', '')])

    def test_cte_with_enable_global_with_statement_off2(self):
        tables = chquery.tables("WITH (select * from table2 limit 1) as table1, (select 1 as v where v in table1) as x select x")
        self.assertEqual(tables, [('', 'table1', ''), ('', 'table2', '')])

    def test_recursive_cte(self):
        tables = chquery.tables("with recursive test_table as (select 1 as number union all select number + 1 from test_table where number < 100) select sum(number) from test_table")
        self.assertEqual(tables, [])

    def test_recursive_cte_with_table(self):
        tables = chquery.tables("with recursive accounts_tree as (select id, parent_id, 1 as depth from accounts where id = 1 union all select a.id, a.parent_id, accounts_tree.depth + 1 from accounts a join accounts_tree at on a.id = at.parent_id where depth < 3) select * from accounts")
        self.assertEqual(tables, [("", "accounts", "")])

    def test_recursive_cte_with_nested_cte(self):
        tables = chquery.tables("with recursive dept as (with recursive base as (select id, manager_id from employees where manager_id is null) select * from base union all select e.id, e.manager_id from employees e join dept d on e.manager_id = d.id) select * from dept")
        self.assertEqual(tables, [("", "employees", "")])

    def test_recursive_cte_with_nested_recursive_cte(self):
        tables = chquery.tables("with recursive t as (with recursive r as (select id, 1 as depth from test1 union all select id, depth+1 from test1 join r on r.id = test1.id where depth < 10) select * from r union all select id from test2) select * from t")
        self.assertEqual(tables, [("", "test1", ""), ("", "test2", "")])

    def test_recursive_cte_with_database_and_table(self):
        tables = chquery.tables("with recursive t as (select id from db1.start_points union all select s.id from db2.next_points s join t on s.prev = t.id) select * from t")
        self.assertEqual(tables, [("db1", "start_points", ""), ("db2", "next_points", "")])
