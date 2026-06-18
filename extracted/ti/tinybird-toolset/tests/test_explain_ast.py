import unittest
from chtoolset import query as chquery

import logging
logging.basicConfig(level=logging.DEBUG)


class TestExplainAST(unittest.TestCase):
    def test_explain_simple_query(self):
        """Test EXPLAIN PLAN for a simple SELECT query"""
        sql = "SELECT * FROM table_a"
        result = chquery.explain_ast(sql)
        self.assertIsInstance(result, str)
        self.assertIn('SelectWithUnionQuery', result)
        self.assertIn('TableIdentifier table_a', result)

    def test_explain_join_query(self):
        """Test EXPLAIN PLAN for a query with JOIN"""
        sql = """
        SELECT t1.*, t2.name
        FROM table1 AS t1
        JOIN table2 AS t2 ON t1.id = t2.id
        """
        result = chquery.explain_ast(sql)
        self.assertIsInstance(result, str)
        self.assertTrue(any(line.rstrip().startswith('TableJoin') for line in result.split()))

    def test_explain_invalid_query(self):
        """Test that invalid queries raise appropriate errors"""
        with self.assertRaisesRegex(ValueError, 'Syntax error'):
            chquery.explain_ast("INVALID SQL QUERY")

    def test_explain_empty_query(self):
        """Test that empty queries raise appropriate errors"""
        with self.assertRaisesRegex(ValueError, 'Syntax error'):
            chquery.explain_ast("")


if __name__ == '__main__':
    unittest.main()
