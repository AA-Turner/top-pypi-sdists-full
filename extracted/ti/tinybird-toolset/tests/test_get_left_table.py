import unittest
from chtoolset import query as chquery


class TestGetLeftTable(unittest.TestCase):

    scenarios = [
        ('select * from _table', ('', '_table', '')),
        ('select * from "aaaa.aaa.aaa"', ('', 'aaaa.aaa.aaa', '')),
        ('with t2 as (select * FROM _table) select * FROM t2', ('', '_table', '')),
        ('with t1 as (select * FROM _table), t2 as (select * from t) select * FROM t2', ('', 't', '')),
        ('select * from table join table2 using a', ('', 'table', '')),
        ('select * FROM db.table JOIN `table2` using b', ('db', 'table', '')),
        ('select 1', ()),
        ('select * from (select whatever from _table)', ('', '_table', '')),
        ('select * from (with (select avg(a) from _table) as tt select count() - sum(a) from table2)', ('', 'table2', '')),
        ('SELECT * FROM (\nSELECT * from `nytaxi`)', ('', 'nytaxi', '')),
        ('SELECT * FROM tt FORMAT JSON', ('', 'tt', '')),
        ('select count() c from test_table format JSON', ('', 'test_table', '')),
        ('select count() c from (select * from t_dd5b58f544c84d8487eb65c23fc5e497 where a < 4) inner join (select * from joined where b > 3.0) using a', ('', 't_dd5b58f544c84d8487eb65c23fc5e497', '')),
        ('SELECT finalizeAggregation(( SELECT countState(id) FROM join_test ))', ()),  # Matches CH behaviour
        ('SELECT finalizeAggregation(id) FROM (SELECT countState(id) as id FROM join_test )', ('', 'join_test', '')),
        ('SELECT arrayMap(x -> finalizeAggregation(x), state) FROM (SELECT sumStateResample(0, 20, 1)(id, id % 20) as state FROM default.join_test)', ('default', 'join_test', '')),
        ('Select array(join_test.id) from join_test', ('', 'join_test', '')),
    ]

    def test_simple_get_left_table(self):
        for (sql, expected_table) in self.scenarios:
            with self.subTest(sql=sql, expected_table=expected_table):
                self.assertEqual(chquery.get_left_table(sql), expected_table)

    def test_get_left_table_default_database(self):
        for (sql, expected_table) in self.scenarios:
            with self.subTest(sql=sql, expected_tables=expected_table):
                self.assertEqual(chquery.get_left_table(sql, default_database='d_012345'),
                                 (expected_table[0] or 'd_012345', expected_table[1], '') if expected_table else expected_table)
