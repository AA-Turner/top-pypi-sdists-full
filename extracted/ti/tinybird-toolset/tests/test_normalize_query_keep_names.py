import unittest
from chtoolset import query as chquery


class TestNormalizeQueryKeepNames(unittest.TestCase):
    """Tests for the normalize_query_keep_names function."""

    def test_normalize_string_literals(self):
        """Test that string literals are replaced with ?"""
        sql = "SELECT * FROM events WHERE user_id = 'alice'"
        result = chquery.normalize_query_keep_names(sql)
        self.assertIn("?", result)
        self.assertNotIn("'alice'", result)
        self.assertIn("events", result)
        self.assertIn("user_id", result)

    def test_normalize_numeric_literals(self):
        """Test that numeric literals are replaced with ?"""
        sql = "SELECT * FROM events WHERE id = 123 LIMIT 10"
        result = chquery.normalize_query_keep_names(sql)
        self.assertNotIn("123", result)
        self.assertNotIn("10", result)
        self.assertIn("?", result)
        self.assertIn("events", result)

    def test_normalize_float_literals(self):
        """Test that float literals are replaced with ?"""
        sql = "SELECT * FROM metrics WHERE value > 3.14159"
        result = chquery.normalize_query_keep_names(sql)
        self.assertNotIn("3.14159", result)
        self.assertIn("?", result)
        self.assertIn("metrics", result)

    def test_preserve_table_names(self):
        """Test that table names are preserved"""
        sql = "SELECT * FROM my_table_123 WHERE id = 1"
        result = chquery.normalize_query_keep_names(sql)
        self.assertIn("my_table_123", result)

    def test_preserve_column_names(self):
        """Test that column names are preserved"""
        sql = "SELECT user_id, event_name FROM events WHERE timestamp > 1000"
        result = chquery.normalize_query_keep_names(sql)
        self.assertIn("user_id", result)
        self.assertIn("event_name", result)
        self.assertIn("timestamp", result)

    def test_preserve_database_qualified_names(self):
        """Test that database.table names are preserved"""
        sql = "SELECT * FROM my_database.my_table WHERE id = 'abc'"
        result = chquery.normalize_query_keep_names(sql)
        self.assertIn("my_database", result)
        self.assertIn("my_table", result)

    def test_same_structure_same_result(self):
        """Test that queries with same structure produce same normalized output"""
        sql1 = "SELECT * FROM events WHERE user_id = 'alice' LIMIT 10"
        sql2 = "SELECT * FROM events WHERE user_id = 'bob' LIMIT 20"
        sql3 = "SELECT * FROM events WHERE user_id = 'charlie' LIMIT 100"

        result1 = chquery.normalize_query_keep_names(sql1)
        result2 = chquery.normalize_query_keep_names(sql2)
        result3 = chquery.normalize_query_keep_names(sql3)

        self.assertEqual(result1, result2)
        self.assertEqual(result2, result3)

    def test_different_structure_different_result(self):
        """Test that queries with different structure produce different normalized output"""
        sql1 = "SELECT * FROM events WHERE user_id = 'alice'"
        sql2 = "SELECT * FROM logs WHERE user_id = 'alice'"

        result1 = chquery.normalize_query_keep_names(sql1)
        result2 = chquery.normalize_query_keep_names(sql2)

        self.assertNotEqual(result1, result2)

    def test_normalize_in_clause(self):
        """Test that IN clause with multiple values is normalized"""
        sql = "SELECT * FROM events WHERE id IN ('a', 'b', 'c')"
        result = chquery.normalize_query_keep_names(sql)
        # Multiple literals in sequence should be coalesced to ?.."
        self.assertIn("?..", result)
        self.assertNotIn("'a'", result)
        self.assertNotIn("'b'", result)
        self.assertNotIn("'c'", result)

    def test_normalize_join_query(self):
        """Test normalization of JOIN queries"""
        sql = """
        SELECT t1.id, t2.name
        FROM table1 AS t1
        JOIN table2 AS t2 ON t1.id = t2.id
        WHERE t1.value = 'test'
        """
        result = chquery.normalize_query_keep_names(sql)
        self.assertIn("table1", result)
        self.assertIn("table2", result)
        self.assertIn("t1", result)
        self.assertIn("t2", result)
        self.assertNotIn("'test'", result)

    def test_normalize_whitespace(self):
        """Test that whitespace is normalized"""
        sql1 = "SELECT   *   FROM    events    WHERE   id = 1"
        sql2 = "SELECT * FROM events WHERE id = 1"

        result1 = chquery.normalize_query_keep_names(sql1)
        result2 = chquery.normalize_query_keep_names(sql2)

        self.assertEqual(result1, result2)

    def test_empty_string(self):
        """Test that empty string returns empty string"""
        result = chquery.normalize_query_keep_names("")
        self.assertEqual(result, "")

    def test_preserve_function_names(self):
        """Test that function names are preserved"""
        sql = "SELECT count(*), sum(value) FROM events WHERE toDate(timestamp) = '2024-01-01'"
        result = chquery.normalize_query_keep_names(sql)
        self.assertIn("count", result)
        self.assertIn("sum", result)
        self.assertIn("toDate", result)

    def test_preserve_keywords(self):
        """Test that SQL keywords are preserved"""
        sql = "SELECT * FROM events WHERE id = 1 ORDER BY timestamp DESC LIMIT 10"
        result = chquery.normalize_query_keep_names(sql)
        self.assertIn("SELECT", result)
        self.assertIn("FROM", result)
        self.assertIn("WHERE", result)
        self.assertIn("ORDER", result)
        self.assertIn("BY", result)
        self.assertIn("DESC", result)
        self.assertIn("LIMIT", result)

    def test_complex_query(self):
        """Test normalization of a complex query"""
        sql = """
        WITH cte AS (
            SELECT user_id, count(*) as cnt
            FROM events
            WHERE timestamp >= '2024-01-01' AND timestamp < '2024-02-01'
            GROUP BY user_id
            HAVING count(*) > 5
        )
        SELECT * FROM cte WHERE cnt > 10 LIMIT 100
        """
        result = chquery.normalize_query_keep_names(sql)
        # Check structure is preserved
        self.assertIn("cte", result)
        self.assertIn("user_id", result)
        self.assertIn("events", result)
        self.assertIn("timestamp", result)
        self.assertIn("cnt", result)
        # Check literals are normalized
        self.assertNotIn("'2024-01-01'", result)
        self.assertNotIn("'2024-02-01'", result)
        self.assertNotIn(" 5", result)
        self.assertNotIn(" 10", result)
        self.assertNotIn(" 100", result)

    def test_negative_numbers(self):
        """Test that negative numbers are normalized"""
        sql = "SELECT * FROM events WHERE value > -100"
        result = chquery.normalize_query_keep_names(sql)
        self.assertNotIn("-100", result)
        self.assertIn("?", result)

    def test_heredoc_literals(self):
        """Test that heredoc literals are normalized"""
        sql = "SELECT * FROM events WHERE data = $heredoc$some long text$heredoc$"
        result = chquery.normalize_query_keep_names(sql)
        self.assertNotIn("some long text", result)
        self.assertIn("?", result)

    def test_cache_key_use_case(self):
        """Test the primary use case: generating cache keys for similar queries"""
        # These queries should all produce the same cache key
        queries = [
            "SELECT * FROM events WHERE user_id = 'user1' AND timestamp > 1000 LIMIT 10",
            "SELECT * FROM events WHERE user_id = 'user2' AND timestamp > 2000 LIMIT 20",
            "SELECT * FROM events WHERE user_id = 'user999' AND timestamp > 9999 LIMIT 100",
        ]

        normalized = [chquery.normalize_query_keep_names(q) for q in queries]

        # All should be equal
        self.assertEqual(normalized[0], normalized[1])
        self.assertEqual(normalized[1], normalized[2])

        # But a query with different structure should be different
        different_query = "SELECT * FROM logs WHERE user_id = 'user1' AND timestamp > 1000 LIMIT 10"
        different_normalized = chquery.normalize_query_keep_names(different_query)
        self.assertNotEqual(normalized[0], different_normalized)

    def test_invalid_sql(self):
        """Test behavior with invalid SQL (doesn't throw, does best-effort normalization).

        Unlike explain_ast which requires valid SQL, normalize_query_keep_names uses
        lexer-based tokenization rather than parsing. This means it can process any
        input and will still normalize literals even in syntactically invalid SQL.
        """
        sql = "INVALID SQL QUERY WITH 'literal' AND 123"
        result = chquery.normalize_query_keep_names(sql)
        # Should still normalize literals even in invalid SQL
        self.assertNotIn("'literal'", result)
        self.assertNotIn("123", result)
        self.assertIn("?", result)
        # Keywords/identifiers are preserved
        self.assertIn("INVALID", result)
        self.assertIn("SQL", result)
        self.assertIn("QUERY", result)

    def test_none_input_raises(self):
        """Test that None input raises ValueError."""
        with self.assertRaises(ValueError):
            chquery.normalize_query_keep_names(None)

    def test_non_string_input_raises(self):
        """Test that non-string input raises ValueError."""
        with self.assertRaises(ValueError):
            chquery.normalize_query_keep_names(123)
        with self.assertRaises(ValueError):
            chquery.normalize_query_keep_names(['SELECT * FROM t'])


if __name__ == '__main__':
    unittest.main()
