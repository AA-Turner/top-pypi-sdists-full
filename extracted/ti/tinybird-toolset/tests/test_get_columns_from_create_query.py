import unittest
from chtoolset import query as chquery

import logging
logging.basicConfig(level=logging.DEBUG)


class TestGetColumnsFromCreateQuery(unittest.TestCase):

    def assertColumnEquals(self, col, expected):
        """Helper to assert all fields of a column match expected values."""
        self.assertEqual(col['name'], expected['name'])
        self.assertEqual(col['type'], expected['type'])
        self.assertEqual(col['nullable'], expected['nullable'])
        self.assertEqual(col['default_specifier'], expected['default_specifier'])
        self.assertEqual(col['default_expression'], expected['default_expression'])
        self.assertEqual(col['codec'], expected['codec'])
        self.assertEqual(col['comment'], expected['comment'])
        self.assertEqual(col['ttl'], expected['ttl'])
        self.assertEqual(col['is_primary_key'], expected['is_primary_key'])

    def test_simple_columns(self):
        """Test extracting columns from a simple CREATE TABLE"""
        sql = """
        CREATE TABLE test (
            id UInt64,
            name String,
            value Float64
        ) ENGINE = MergeTree() ORDER BY id
        """
        cols = chquery.get_columns_from_create_query(sql)
        self.assertEqual(len(cols), 3)

        self.assertColumnEquals(cols[0], {
            'name': 'id',
            'type': 'UInt64',
            'nullable': False,
            'default_specifier': '',
            'default_expression': None,
            'codec': None,
            'comment': None,
            'ttl': None,
            'is_primary_key': False,
        })

        self.assertColumnEquals(cols[1], {
            'name': 'name',
            'type': 'String',
            'nullable': False,
            'default_specifier': '',
            'default_expression': None,
            'codec': None,
            'comment': None,
            'ttl': None,
            'is_primary_key': False,
        })

        self.assertColumnEquals(cols[2], {
            'name': 'value',
            'type': 'Float64',
            'nullable': False,
            'default_specifier': '',
            'default_expression': None,
            'codec': None,
            'comment': None,
            'ttl': None,
            'is_primary_key': False,
        })

    def test_column_with_default(self):
        """Test extracting columns with DEFAULT expression"""
        sql = """
        CREATE TABLE test (
            id UInt64,
            name String DEFAULT 'unknown',
            column_as_default UInt64 DEFAULT id,
            created DateTime DEFAULT now()
        ) ENGINE = MergeTree() ORDER BY id
        """
        cols = chquery.get_columns_from_create_query(sql)
        self.assertEqual(len(cols), 4)

        self.assertColumnEquals(cols[0], {
            'name': 'id',
            'type': 'UInt64',
            'nullable': False,
            'default_specifier': '',
            'default_expression': None,
            'codec': None,
            'comment': None,
            'ttl': None,
            'is_primary_key': False,
        })

        self.assertColumnEquals(cols[1], {
            'name': 'name',
            'type': 'String',
            'nullable': False,
            'default_specifier': 'DEFAULT',
            'default_expression': "'unknown'",
            'codec': None,
            'comment': None,
            'ttl': None,
            'is_primary_key': False,
        })

        self.assertColumnEquals(cols[2], {
            'name': 'column_as_default',
            'type': 'UInt64',
            'nullable': False,
            'default_specifier': 'DEFAULT',
            'default_expression': 'id',
            'codec': None,
            'comment': None,
            'ttl': None,
            'is_primary_key': False,
        })

        self.assertColumnEquals(cols[3], {
            'name': 'created',
            'type': 'DateTime',
            'nullable': False,
            'default_specifier': 'DEFAULT',
            'default_expression': 'now()',
            'codec': None,
            'comment': None,
            'ttl': None,
            'is_primary_key': False,
        })

    def test_column_with_materialized(self):
        """Test extracting columns with MATERIALIZED expression"""
        sql = """
        CREATE TABLE test (
            id UInt64,
            created DateTime,
            date Date MATERIALIZED toDate(created)
        ) ENGINE = MergeTree() ORDER BY id
        """
        cols = chquery.get_columns_from_create_query(sql)
        self.assertEqual(len(cols), 3)

        self.assertColumnEquals(cols[2], {
            'name': 'date',
            'type': 'Date',
            'nullable': False,
            'default_specifier': 'MATERIALIZED',
            'default_expression': 'toDate(created)',
            'codec': None,
            'comment': None,
            'ttl': None,
            'is_primary_key': False,
        })

    def test_column_with_alias(self):
        """Test extracting columns with ALIAS expression"""
        sql = """
        CREATE TABLE test (
            id UInt64,
            first_name String,
            last_name String,
            full_name String ALIAS concat(first_name, ' ', last_name)
        ) ENGINE = MergeTree() ORDER BY id
        """
        cols = chquery.get_columns_from_create_query(sql)
        self.assertEqual(len(cols), 4)

        self.assertColumnEquals(cols[3], {
            'name': 'full_name',
            'type': 'String',
            'nullable': False,
            'default_specifier': 'ALIAS',
            'default_expression': "concat(first_name, ' ', last_name)",
            'codec': None,
            'comment': None,
            'ttl': None,
            'is_primary_key': False,
        })

    def test_column_with_ephemeral(self):
        """Test extracting columns with EPHEMERAL expression"""
        sql = """
        CREATE TABLE test (
            id UInt64,
            temp_data String EPHEMERAL
        ) ENGINE = MergeTree() ORDER BY id
        """
        cols = chquery.get_columns_from_create_query(sql)
        self.assertEqual(len(cols), 2)

        self.assertColumnEquals(cols[1], {
            'name': 'temp_data',
            'type': 'String',
            'nullable': False,
            'default_specifier': 'EPHEMERAL',
            'default_expression': "defaultValueOfTypeName('String')",
            'codec': None,
            'comment': None,
            'ttl': None,
            'is_primary_key': False,
        })

    def test_column_with_ephemeral_expression(self):
        """Test extracting columns with EPHEMERAL and default expression"""
        sql = """
        CREATE TABLE test (
            id UInt64,
            temp_data String EPHEMERAL 'temp_value'
        ) ENGINE = MergeTree() ORDER BY id
        """
        cols = chquery.get_columns_from_create_query(sql)
        self.assertEqual(len(cols), 2)

        self.assertColumnEquals(cols[1], {
            'name': 'temp_data',
            'type': 'String',
            'nullable': False,
            'default_specifier': 'EPHEMERAL',
            'default_expression': "'temp_value'",
            'codec': None,
            'comment': None,
            'ttl': None,
            'is_primary_key': False,
        })

    def test_column_with_comment(self):
        """Test extracting columns with COMMENT"""
        sql = """
        CREATE TABLE test (
            id UInt64 COMMENT 'Primary identifier',
            name String COMMENT 'User name'
        ) ENGINE = MergeTree() ORDER BY id
        """
        cols = chquery.get_columns_from_create_query(sql)
        self.assertEqual(len(cols), 2)

        self.assertColumnEquals(cols[0], {
            'name': 'id',
            'type': 'UInt64',
            'nullable': False,
            'default_specifier': '',
            'default_expression': None,
            'codec': None,
            'comment': "'Primary identifier'",
            'ttl': None,
            'is_primary_key': False,
        })

        self.assertColumnEquals(cols[1], {
            'name': 'name',
            'type': 'String',
            'nullable': False,
            'default_specifier': '',
            'default_expression': None,
            'codec': None,
            'comment': "'User name'",
            'ttl': None,
            'is_primary_key': False,
        })

    def test_column_with_codec(self):
        """Test extracting columns with CODEC"""
        sql = """
        CREATE TABLE test (
            id UInt64 CODEC(Delta, ZSTD),
            value Float64 CODEC(Gorilla, LZ4)
        ) ENGINE = MergeTree() ORDER BY id
        """
        cols = chquery.get_columns_from_create_query(sql)
        self.assertEqual(len(cols), 2)

        self.assertColumnEquals(cols[0], {
            'name': 'id',
            'type': 'UInt64',
            'nullable': False,
            'default_specifier': '',
            'default_expression': None,
            'codec': 'CODEC(Delta, ZSTD)',
            'comment': None,
            'ttl': None,
            'is_primary_key': False,
        })

        self.assertColumnEquals(cols[1], {
            'name': 'value',
            'type': 'Float64',
            'nullable': False,
            'default_specifier': '',
            'default_expression': None,
            'codec': 'CODEC(Gorilla, LZ4)',
            'comment': None,
            'ttl': None,
            'is_primary_key': False,
        })

    def test_column_with_ttl(self):
        """Test extracting columns with TTL"""
        sql = """
        CREATE TABLE test (
            id UInt64,
            created DateTime,
            data String TTL created + INTERVAL 1 DAY,
            data2 String TTL created + toIntervalHour(1)
        ) ENGINE = MergeTree() ORDER BY id
        """
        cols = chquery.get_columns_from_create_query(sql)
        self.assertEqual(len(cols), 4)

        self.assertColumnEquals(cols[0], {
            'name': 'id',
            'type': 'UInt64',
            'nullable': False,
            'default_specifier': '',
            'default_expression': None,
            'codec': None,
            'comment': None,
            'ttl': None,
            'is_primary_key': False,
        })

        self.assertColumnEquals(cols[1], {
            'name': 'created',
            'type': 'DateTime',
            'nullable': False,
            'default_specifier': '',
            'default_expression': None,
            'codec': None,
            'comment': None,
            'ttl': None,
            'is_primary_key': False,
        })

        # ClickHouse normalizes INTERVAL to toIntervalDay
        self.assertColumnEquals(cols[2], {
            'name': 'data',
            'type': 'String',
            'nullable': False,
            'default_specifier': '',
            'default_expression': None,
            'codec': None,
            'comment': None,
            'ttl': 'created + toIntervalDay(1)',
            'is_primary_key': False,
        })

        self.assertColumnEquals(cols[3], {
            'name': 'data2',
            'type': 'String',
            'nullable': False,
            'default_specifier': '',
            'default_expression': None,
            'codec': None,
            'comment': None,
            'ttl': 'created + toIntervalHour(1)',
            'is_primary_key': False,
        })

    def test_nullable_column_not_null(self):
        """Test extracting columns with NOT NULL modifier"""
        sql = """
        CREATE TABLE test (
            id UInt64 NOT NULL
        ) ENGINE = MergeTree() ORDER BY id
        """
        cols = chquery.get_columns_from_create_query(sql)
        self.assertEqual(len(cols), 1)

        self.assertColumnEquals(cols[0], {
            'name': 'id',
            'type': 'UInt64',
            'nullable': False,
            'default_specifier': '',
            'default_expression': None,
            'codec': None,
            'comment': None,
            'ttl': None,
            'is_primary_key': False,
        })

    def test_nullable_column_null(self):
        """Test extracting columns with NULL modifier"""
        sql = """
        CREATE TABLE test (
            value Float64 NULL
        ) ENGINE = MergeTree() ORDER BY tuple()
        """
        cols = chquery.get_columns_from_create_query(sql)
        self.assertEqual(len(cols), 1)

        self.assertColumnEquals(cols[0], {
            'name': 'value',
            'type': 'Float64',
            'nullable': True,
            'default_specifier': '',
            'default_expression': None,
            'codec': None,
            'comment': None,
            'ttl': None,
            'is_primary_key': False,
        })

    def test_nullable_type(self):
        """Test extracting columns with Nullable type wrapper"""
        sql = """
        CREATE TABLE test (
            name Nullable(String)
        ) ENGINE = MergeTree() ORDER BY tuple()
        """
        cols = chquery.get_columns_from_create_query(sql)
        self.assertEqual(len(cols), 1)

        # Nullable type wrapper makes the column nullable
        self.assertColumnEquals(cols[0], {
            'name': 'name',
            'type': 'Nullable(String)',
            'nullable': True,
            'default_specifier': '',
            'default_expression': None,
            'codec': None,
            'comment': None,
            'ttl': None,
            'is_primary_key': False,
        })

    def test_complex_column_all_attributes(self):
        """Test extracting column with multiple attributes combined"""
        sql = """
        CREATE TABLE test (
            id UInt64,
            name String DEFAULT 'unknown' COMMENT 'User name' CODEC(ZSTD)
        ) ENGINE = MergeTree() ORDER BY id
        """
        cols = chquery.get_columns_from_create_query(sql)
        self.assertEqual(len(cols), 2)

        self.assertColumnEquals(cols[1], {
            'name': 'name',
            'type': 'String',
            'nullable': False,
            'default_specifier': 'DEFAULT',
            'default_expression': "'unknown'",
            'codec': 'CODEC(ZSTD)',
            'comment': "'User name'",
            'ttl': None,
            'is_primary_key': False,
        })

    def test_nested_types(self):
        """Test extracting columns with nested/complex types"""
        sql = """
        CREATE TABLE test (
            id UInt64,
            tags Array(String),
            metadata Map(String, String),
            point Tuple(x Float64, y Float64)
        ) ENGINE = MergeTree() ORDER BY id
        """
        cols = chquery.get_columns_from_create_query(sql)
        self.assertEqual(len(cols), 4)

        self.assertColumnEquals(cols[1], {
            'name': 'tags',
            'type': 'Array(String)',
            'nullable': False,
            'default_specifier': '',
            'default_expression': None,
            'codec': None,
            'comment': None,
            'ttl': None,
            'is_primary_key': False,
        })

        self.assertColumnEquals(cols[2], {
            'name': 'metadata',
            'type': 'Map(String, String)',
            'nullable': False,
            'default_specifier': '',
            'default_expression': None,
            'codec': None,
            'comment': None,
            'ttl': None,
            'is_primary_key': False,
        })

        self.assertColumnEquals(cols[3], {
            'name': 'point',
            'type': 'Tuple(x Float64, y Float64)',
            'nullable': False,
            'default_specifier': '',
            'default_expression': None,
            'codec': None,
            'comment': None,
            'ttl': None,
            'is_primary_key': False,
        })

    def test_lowcardinality_type(self):
        """Test extracting columns with LowCardinality type"""
        sql = """
        CREATE TABLE test (
            id UInt64,
            status LowCardinality(String)
        ) ENGINE = MergeTree() ORDER BY id
        """
        cols = chquery.get_columns_from_create_query(sql)
        self.assertEqual(len(cols), 2)

        self.assertColumnEquals(cols[1], {
            'name': 'status',
            'type': 'LowCardinality(String)',
            'nullable': False,
            'default_specifier': '',
            'default_expression': None,
            'codec': None,
            'comment': None,
            'ttl': None,
            'is_primary_key': False,
        })

    def test_datetime_with_timezone(self):
        """Test extracting columns with DateTime timezone"""
        sql = """
        CREATE TABLE test (
            id UInt64,
            created DateTime('UTC'),
            updated DateTime64(3, 'America/New_York')
        ) ENGINE = MergeTree() ORDER BY id
        """
        cols = chquery.get_columns_from_create_query(sql)
        self.assertEqual(len(cols), 3)

        self.assertColumnEquals(cols[1], {
            'name': 'created',
            'type': "DateTime('UTC')",
            'nullable': False,
            'default_specifier': '',
            'default_expression': None,
            'codec': None,
            'comment': None,
            'ttl': None,
            'is_primary_key': False,
        })

        self.assertColumnEquals(cols[2], {
            'name': 'updated',
            'type': "DateTime64(3, 'America/New_York')",
            'nullable': False,
            'default_specifier': '',
            'default_expression': None,
            'codec': None,
            'comment': None,
            'ttl': None,
            'is_primary_key': False,
        })

    def test_decimal_type(self):
        """Test extracting columns with Decimal types"""
        sql = """
        CREATE TABLE test (
            id UInt64,
            price Decimal(10, 2),
            amount Decimal128(4)
        ) ENGINE = MergeTree() ORDER BY id
        """
        cols = chquery.get_columns_from_create_query(sql)
        self.assertEqual(len(cols), 3)

        self.assertColumnEquals(cols[1], {
            'name': 'price',
            'type': 'Decimal(10, 2)',
            'nullable': False,
            'default_specifier': '',
            'default_expression': None,
            'codec': None,
            'comment': None,
            'ttl': None,
            'is_primary_key': False,
        })

        self.assertColumnEquals(cols[2], {
            'name': 'amount',
            'type': 'Decimal128(4)',
            'nullable': False,
            'default_specifier': '',
            'default_expression': None,
            'codec': None,
            'comment': None,
            'ttl': None,
            'is_primary_key': False,
        })

    def test_fixedstring_type(self):
        """Test extracting columns with FixedString type"""
        sql = """
        CREATE TABLE test (
            id UInt64,
            code FixedString(3)
        ) ENGINE = MergeTree() ORDER BY id
        """
        cols = chquery.get_columns_from_create_query(sql)
        self.assertEqual(len(cols), 2)

        self.assertColumnEquals(cols[1], {
            'name': 'code',
            'type': 'FixedString(3)',
            'nullable': False,
            'default_specifier': '',
            'default_expression': None,
            'codec': None,
            'comment': None,
            'ttl': None,
            'is_primary_key': False,
        })

    def test_enum_type(self):
        """Test extracting columns with Enum types"""
        sql = """
        CREATE TABLE test (
            id UInt64,
            status Enum8('pending' = 1, 'active' = 2, 'inactive' = 3)
        ) ENGINE = MergeTree() ORDER BY id
        """
        cols = chquery.get_columns_from_create_query(sql)
        self.assertEqual(len(cols), 2)

        self.assertColumnEquals(cols[1], {
            'name': 'status',
            'type': "Enum8('pending' = 1, 'active' = 2, 'inactive' = 3)",
            'nullable': False,
            'default_specifier': '',
            'default_expression': None,
            'codec': None,
            'comment': None,
            'ttl': None,
            'is_primary_key': False,
        })

    def test_column_with_primary_key(self):
        """Test extracting columns with PRIMARY KEY specifier"""
        sql = """
        CREATE TABLE test (
            id UInt64 PRIMARY KEY,
            name String
        ) ENGINE = MergeTree()
        """
        cols = chquery.get_columns_from_create_query(sql)
        self.assertEqual(len(cols), 2)

        self.assertColumnEquals(cols[0], {
            'name': 'id',
            'type': 'UInt64',
            'nullable': False,
            'default_specifier': '',
            'default_expression': None,
            'codec': None,
            'comment': None,
            'ttl': None,
            'is_primary_key': True,
        })

        self.assertColumnEquals(cols[1], {
            'name': 'name',
            'type': 'String',
            'nullable': False,
            'default_specifier': '',
            'default_expression': None,
            'codec': None,
            'comment': None,
            'ttl': None,
            'is_primary_key': False,
        })

    def test_invalid_query(self):
        """Test that invalid queries raise appropriate errors"""
        with self.assertRaises(ValueError):
            chquery.get_columns_from_create_query("INVALID SQL QUERY")

    def test_non_create_query(self):
        """Test that non-CREATE queries raise appropriate errors"""
        with self.assertRaises(ValueError):
            chquery.get_columns_from_create_query("SELECT * FROM test")

    def test_empty_query(self):
        """Test that empty queries raise appropriate errors"""
        with self.assertRaises(ValueError):
            chquery.get_columns_from_create_query("")


if __name__ == '__main__':
    unittest.main()
