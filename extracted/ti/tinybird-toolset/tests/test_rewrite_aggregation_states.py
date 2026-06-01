import unittest
from chtoolset import query as chquery


class TestGetLeftTable(unittest.TestCase):
    maxDiff = None

    def test_simple_rewrite(self):
        sql = "select avg(value) as t from table"
        expected = "select avgState(value) as t from table"
        self.assertEqual(chquery.format(chquery.rewrite_aggregation_states(sql)), chquery.format(expected))

        sql = "select toStartOfTenMinutes(rand()) as t, count() as c FROM table GROUP BY t"
        expected = "select toStartOfTenMinutes(rand()) as t, countState() as c FROM table GROUP BY t"
        self.assertEqual(chquery.format(chquery.rewrite_aggregation_states(sql)), chquery.format(expected))

        sql = "select AVG(value) as t, COUNT() as c FROM table GROUP BY n"
        expected = "select AVGState(value) as t, COUNTState() as c FROM table GROUP BY n"
        self.assertEqual(chquery.format(chquery.rewrite_aggregation_states(sql)), chquery.format(expected))

        sql = """
            SELECT
                key,
                toStartOfInterval(max(timestamp), toIntervalMonth(3)) AS trimester,
                argMax(promocode, visit_date) AS last_booking_promocode,
                max(visit_date) AS last_booking_date
            FROM retrieve
            GROUP BY key
        """
        expected = """
            SELECT
                key,
                toStartOfInterval(max(timestamp), toIntervalMonth(3)) AS trimester,
                argMaxState(promocode, visit_date) AS last_booking_promocode,
                maxState(visit_date) AS last_booking_date
            FROM retrieve
            GROUP BY key
        """
        self.assertEqual(chquery.format(chquery.rewrite_aggregation_states(sql)), chquery.format(expected))

        sql = """
            SELECT
                date,
                topK(10)(product_id) AS top_10,
                sum(price) AS total_sales
            FROM only_buy_events
            GROUP BY date
        """
        expected = """
            SELECT
                date,
                topKState(10)(product_id) AS top_10,
                sumState(price) AS total_sales
            FROM only_buy_events
            GROUP BY date
        """
        self.assertEqual(chquery.format(chquery.rewrite_aggregation_states(sql)), chquery.format(expected))

    def test_idempotence(self):
        sql = "select quantileState(0.10)(value) from table"
        self.assertEqual(chquery.format(chquery.rewrite_aggregation_states(sql)), chquery.format(sql))

        sql = """
        SELECT t.1 AS h
        FROM
        (
            SELECT arrayJoin(tt) AS t
            FROM test AS a
            ANY LEFT JOIN
            (
                SELECT
                    author_id,
                    groupArray(h) AS tt
                FROM test2
                GROUP BY author_id
            ) AS d ON a.id = d.author_id
        )
        """
        self.assertEqual(chquery.format(chquery.rewrite_aggregation_states(sql)), chquery.format(sql))

        sql = "select assumeNotNull(value) t FROM table"
        self.assertEqual(chquery.format(chquery.rewrite_aggregation_states(sql)), chquery.format(sql))

    def test_aggregation_inside_function(self):
        # These queries are invalid, but we don't try to detect it during parsing
        # Instead they are left as is (it will fail when we try to do anything / verify the query)

        sql = """select round(avgState(value)) t FROM table"""
        self.assertEqual(chquery.format(chquery.rewrite_aggregation_states(sql)), chquery.format(sql))
        sql = """select divide(round(avgState(value)), 1) t FROM table"""
        self.assertEqual(chquery.format(chquery.rewrite_aggregation_states(sql)), chquery.format(sql))
        sql = """select divide(round(avgIfState(value, 1)), 1) t FROM table"""
        self.assertEqual(chquery.format(chquery.rewrite_aggregation_states(sql)), chquery.format(sql))

    def test_existing_combinators_are_respected(self):
        sql = """select sumState(value, 1=1) t FROM table"""
        expected = """select sumState(value, 1=1) t FROM table"""
        self.assertEqual(chquery.format(chquery.rewrite_aggregation_states(sql)), chquery.format(expected))

        sql = """select sumIf(value, 1=1) t FROM table"""
        expected = """select sumIfState(value, 1=1) t FROM table"""
        self.assertEqual(chquery.format(chquery.rewrite_aggregation_states(sql)), chquery.format(expected))

        sql = """select sumOrNull(value) t FROM table"""
        expected = """select sumOrNullState(value) t FROM table"""
        self.assertEqual(chquery.format(chquery.rewrite_aggregation_states(sql)), chquery.format(expected))

        sql = """select sumOrNullState(value) t FROM table"""
        expected = """select sumOrNullState(value) t FROM table"""
        self.assertEqual(chquery.format(chquery.rewrite_aggregation_states(sql)), chquery.format(expected))

        sql = """select sumOrNullDistinct(value) t FROM table"""
        expected = """select sumOrNullDistinctState(value) t FROM table"""
        self.assertEqual(chquery.format(chquery.rewrite_aggregation_states(sql)), chquery.format(expected))

    def test_throws_with_invalid_query(self):
        with self.assertRaisesRegex(ValueError,
                                    "DB::Exception: Unknown function toStartOfTenMinute. "
                                    "Maybe you meant: \\['toStartOfTenMinutes','toStartOfMinute','toStartOfFiveMinute'\\]"):
            chquery.rewrite_aggregation_states("select toStartOfTenMinute(rand()) as t, count() as c FROM table GROUP BY t")

    def test_throws_with_blocked_function(self):
        sql = "select buildId() as t, count() as c FROM table GROUP BY t"
        with self.assertRaisesRegex(ValueError, "DB::Exception: Usage of function buildId is restricted"):
            chquery.rewrite_aggregation_states(sql)

        expected = "select buildId() as t, countState() as c FROM table GROUP BY t"
        self.assertEqual(chquery.format(chquery.rewrite_aggregation_states(sql, validate_functions=False)),
                         chquery.format(expected))

        self.assertEqual(chquery.format(chquery.rewrite_aggregation_states(sql, function_allow_list=['buildId'])),
                         chquery.format(expected))

        sql = "select concat('a', 'b') as t, count() as c FROM table GROUP BY t"
        with self.assertRaisesRegex(ValueError, "DB::Exception: Usage of function concat is restricted"):
            chquery.rewrite_aggregation_states(sql, function_deny_list=['concat'])

    def test_allows_with_allowed_function(self):
        sql = "select buildId() as t, count() as c FROM table GROUP BY t"
        expected = "select buildId() as t, countState() as c FROM table GROUP BY t"
        self.assertEqual(chquery.format(chquery.rewrite_aggregation_states(sql, validate_functions=False)),
                         chquery.format(expected))

        self.assertEqual(chquery.format(chquery.rewrite_aggregation_states(sql, function_allow_list=['buildId'])),
                         chquery.format(expected))

    def test_with_CTE(self):
        sql = "WITH t as (select value from table) SELECT avg(value) FROM t"
        expected = "WITH t as (select value from table) SELECT avgState(value) FROM t"
        self.assertEqual(chquery.format(chquery.rewrite_aggregation_states(sql)), chquery.format(expected))
