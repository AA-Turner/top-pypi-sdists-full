import concurrent.futures
import unittest
from chtoolset import query as chquery


class TestParseCache(unittest.TestCase):
    _, _, CURRENT_CACHE_CAPACITY, _ = chquery.parser_cache_info()
    maxDiff = None

    def setUp(self):
        chquery.parser_cache_reset()
        self.verify_empty()

    def verify_empty(self):
        self.verify_cache(hits=0, misses=0, current_size=0)

    def verify_cache(self, hits=0, misses=0, current_size=0):
        _hits, _misses, capacity, _current_size = chquery.parser_cache_info()
        self.assertEqual(hits, _hits)
        self.assertEqual(misses, _misses)
        self.assertEqual(capacity, self.CURRENT_CACHE_CAPACITY)
        self.assertEqual(current_size, _current_size)

    def test_works_with_format(self):
        # Format caches in both ways (on input and output)
        _ = chquery.format("Select 1")
        self.verify_cache(hits=0, misses=2, current_size=2)

        # Both input and output should hit cache
        formatted = chquery.format("Select 1")
        self.verify_cache(hits=2, misses=2, current_size=2)

        # Using the output as the next input should hit cache too
        _ = chquery.format(formatted)
        self.verify_cache(hits=4, misses=2, current_size=2)

    def test_works_with_tables(self):
        sql = "Select * from table"
        _ = chquery.tables(sql)
        self.verify_cache(hits=0, misses=1, current_size=1)

        _ = chquery.tables(sql)
        self.verify_cache(hits=1, misses=1, current_size=1)

        # Passing a reformatted query won't hit the cache
        _ = chquery.tables("SELECT * FROM table")
        self.verify_cache(hits=1, misses=2, current_size=2)

    def test_works_with_replace(self):
        sql = "Select * from datasource"
        replacements = {('default', 'datasource'): ('d_010101', 'table2')}
        result = chquery.replace_tables(sql, replacements, default_database='default')
        self.assertEqual(result, "SELECT *\nFROM d_010101.table2 AS datasource")
        self.verify_cache(hits=0, misses=2, current_size=2)

        # Verify that the queries are cached both ways
        result = chquery.replace_tables(sql, replacements, default_database='default')
        self.assertEqual(result, "SELECT *\nFROM d_010101.table2 AS datasource")
        self.verify_cache(hits=2, misses=2, current_size=2)

        # And the result is cached too for further changes
        result = chquery.replace_tables(result, {}, default_database='default')
        self.assertEqual(result, "SELECT *\nFROM d_010101.table2 AS datasource")
        self.verify_cache(hits=4, misses=2, current_size=2)

    def test_multiple_replaces_work_fine(self):
        source_sql = "Select * from datasource"
        replacement1 = {('default', 'datasource'): ('d_010101', 'table1')}
        replacement2 = {('default', 'datasource'): ('d_010101', 'table2')}

        r1 = chquery.replace_tables(source_sql, replacement1, default_database='default')
        self.assertEqual(r1, "SELECT *\nFROM d_010101.table1 AS datasource")
        self.verify_cache(hits=0, misses=2, current_size=2)

        r2 = chquery.replace_tables(source_sql, replacement2, default_database='default')
        self.assertEqual(r2, "SELECT *\nFROM d_010101.table2 AS datasource")
        self.verify_cache(hits=1, misses=3, current_size=3)

    def test_works_with_subqueries(self):
        sql = "SELECT * FROM datasource"
        replacements = {('default', 'datasource'): ('', '(SELECT * FROM table_2)')}

        # +3 failures (2 input, 1 output)
        _ = chquery.replace_tables(sql, replacements, default_database='default')
        self.verify_cache(hits=0, misses=3, current_size=3)

        # +3 hits (2 input, 1 output)
        _ = chquery.replace_tables(sql, replacements, default_database='default')
        self.verify_cache(hits=3, misses=3, current_size=3)

        # +2 hits (2 subqueries) +2 misses (new input, new output)
        sql = "SELECT * FROM datasource, datasource"
        result = chquery.replace_tables(sql, replacements, default_database='default')
        self.assertEqual(result, """SELECT *
FROM
(
    SELECT *
    FROM table_2
) AS datasource,
(
    SELECT *
    FROM table_2
) AS datasource""")
        self.verify_cache(hits=5, misses=5, current_size=5)

    def test_works_across_functions(self):
        sql = "Select * from table"

        _ = chquery.tables(sql)
        self.verify_cache(hits=0, misses=1, current_size=1)

        # +1 hit (input), +1 miss (output)
        replacements = {('default', 'table'): ('d_010101', 'table2')}
        result = chquery.replace_tables(sql, replacements, default_database='default')
        self.verify_cache(hits=1, misses=2, current_size=2)

        # +2 hits (input and output)
        _ = chquery.format(result)
        self.verify_cache(hits=3, misses=2, current_size=2)

    def test_works_fine_with_max_size(self):
        sql = "Select * from table"

        extra = 10
        for number in range(self.CURRENT_CACHE_CAPACITY + extra):
            _ = chquery.tables(f"{sql} LIMIT {number}")

        self.verify_cache(hits=0, misses=self.CURRENT_CACHE_CAPACITY + extra, current_size=self.CURRENT_CACHE_CAPACITY)

        # Retry now to verify that the expected / last elements are in cache
        for number in range(extra, self.CURRENT_CACHE_CAPACITY + extra):
            _ = chquery.tables(f"{sql} LIMIT {number}")

        self.verify_cache(hits=self.CURRENT_CACHE_CAPACITY,
                          misses=self.CURRENT_CACHE_CAPACITY + extra,
                          current_size=self.CURRENT_CACHE_CAPACITY)

    def test_cache_is_thread_specific(self):

        def do_stuff(iterations):
            self.verify_empty()

            for i in range(iterations):
                _ = chquery.tables(f"Select * from table LIMIT {i}")

            self.verify_cache(hits=0, misses=iterations, current_size=iterations)

            for i in range(iterations):
                _ = chquery.tables(f"Select * from table LIMIT {i}")

            self.verify_cache(hits=iterations, misses=iterations, current_size=iterations)

            chquery.parser_cache_reset()

        workers = 4
        with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
            items = range(50)
            for _ in executor.map(do_stuff, items):
                pass
