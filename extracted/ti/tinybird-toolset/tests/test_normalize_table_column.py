import unittest

from chtoolset import query as chquery


class TestNormalizeTableColumn(unittest.TestCase):
    def test_normalizes_low_cardinality_with_nullable_flag(self):
        column = chquery.normalize_table_column(
            column={
                "name": "status",
                "type": "LowCardinality(String)",
                "nullable": True,
            },
        )

        self.assertEqual(column["name"], "status")
        self.assertEqual(column["type"], "LowCardinality(String)")
        self.assertTrue(column["nullable"])

    def test_uses_normalized_name_alias(self):
        column = chquery.normalize_table_column(
            column={"name": "Name", "normalized_name": "name", "type": "String"},
        )

        self.assertEqual(column["name"], "name")
        self.assertEqual(column["type"], "String")
        self.assertFalse(column["nullable"])

    def test_detects_nullable_simple_aggregate_function(self):
        column = chquery.normalize_table_column(
            column={
                "name": "metric",
                "type": "SimpleAggregateFunction(sum, Nullable(Int64))",
            },
        )

        self.assertEqual(
            column["type"], "SimpleAggregateFunction(sum, Nullable(Int64))"
        )
        self.assertTrue(column["nullable"])

    def test_plain_nullable_wrapper_does_not_force_nullable_flag(self):
        column = chquery.normalize_table_column(
            column={"name": "discount", "type": "Nullable(Decimal64(4))"},
        )

        self.assertEqual(column["type"], "Nullable(Decimal64(4))")
        self.assertTrue(column["nullable"])

    def test_normalizes_decimal_spacing(self):
        column = chquery.normalize_table_column(
            column={
                "name": "amount",
                "normalized_name": "amount",
                "type": "Decimal(18,4)",
                "nullable": False,
            },
        )

        self.assertEqual(column["type"], "Decimal(18, 4)")
        self.assertFalse(column["nullable"])

    def test_normalizes_decimal_spacing_with_nullable_flag(self):
        column = chquery.normalize_table_column(
            column={
                "name": "tax",
                "normalized_name": "tax",
                "type": "Decimal(10,2)",
                "nullable": True,
            },
        )

        self.assertEqual(column["type"], "Decimal(10, 2)")
        self.assertTrue(column["nullable"])

    def test_preserves_decimal64_alias(self):
        column = chquery.normalize_table_column(
            column={
                "name": "discount",
                "normalized_name": "discount",
                "type": "Nullable(Decimal64(4))",
                "nullable": False,
            },
        )

        self.assertEqual(column["type"], "Nullable(Decimal64(4))")
        self.assertTrue(column["nullable"])

    def test_preserves_datetime64_precision(self):
        column = chquery.normalize_table_column(
            column={
                "name": "created_at",
                "normalized_name": "created_at",
                "type": "DateTime64(3)",
                "nullable": False,
            },
        )

        self.assertEqual(column["type"], "DateTime64(3)")
        self.assertFalse(column["nullable"])

    def test_normalizes_json_dynamic_param_spacing(self):
        column = chquery.normalize_table_column(
            column={
                "name": "json",
                "normalized_name": "json",
                "type": "JSON(max_dynamic_types=2, max_dynamic_paths=16)",
                "nullable": False,
            },
        )

        self.assertEqual(
            column["type"], "JSON(max_dynamic_types = 2, max_dynamic_paths = 16)"
        )
        self.assertFalse(column["nullable"])

    def test_normalizes_nested_decimal_spacing(self):
        column = chquery.normalize_table_column(
            column={
                "name": "agg",
                "normalized_name": "agg",
                "type": "AggregateFunction(sum, Decimal(10,2))",
                "nullable": False,
            },
        )

        self.assertEqual(column["type"], "AggregateFunction(sum, Decimal(10, 2))")
        self.assertFalse(column["nullable"])

    def test_normalizes_multiline_complex_type_spacing(self):
        column = chquery.normalize_table_column(
            column={
                "name": "agg",
                "normalized_name": "agg",
                "type": """AggregateFunction(
                    argMax, Nullable(UUID), Tuple(UInt8, DateTime64(3), DateTime64(3), DateTime64(3))
                )""",
                "nullable": False,
            },
        )

        self.assertEqual(
            column["type"],
            "AggregateFunction(argMax, Nullable(UUID), Tuple(UInt8, DateTime64(3), DateTime64(3), DateTime64(3)))",
        )
        self.assertFalse(column["nullable"])

    def test_preserves_space_before_timezone_string(self):
        column = chquery.normalize_table_column(
            column={
                "name": "ts",
                "normalized_name": "ts",
                "type": "DateTime64(3, 'Europe/Vienna')",
                "nullable": False,
            },
        )

        self.assertEqual(column["type"], "DateTime64(3, 'Europe/Vienna')")
        self.assertFalse(column["nullable"])

    def test_nullable_flag_preserves_raw_type(self):
        column = chquery.normalize_table_column(
            column={
                "name": "reason",
                "normalized_name": "reason",
                "type": "String",
                "nullable": True,
            },
        )

        self.assertEqual(column["type"], "String")
        self.assertTrue(column["nullable"])

    def test_nullable_flag_preserves_low_cardinality_type(self):
        column = chquery.normalize_table_column(
            column={
                "name": "status",
                "normalized_name": "status",
                "type": "LowCardinality(String)",
                "nullable": True,
            },
        )

        self.assertEqual(column["type"], "LowCardinality(String)")
        self.assertTrue(column["nullable"])

    def test_preserves_existing_nullable_low_cardinality_wrapper(self):
        column = chquery.normalize_table_column(
            column={
                "name": "status",
                "normalized_name": "status",
                "type": "LowCardinality(Nullable(String))",
                "nullable": False,
            },
        )

        self.assertEqual(column["type"], "LowCardinality(Nullable(String))")
        self.assertTrue(column["nullable"])

    def test_normalizes_default_value_into_specifier_and_expression(self):
        column = chquery.normalize_table_column(
            column={
                "name": "created_at",
                "normalized_name": "created_at",
                "type": "DateTime64(3)",
                "nullable": False,
                "default_value": "DEFAULT now()",
            },
        )

        self.assertEqual(column["type"], "DateTime64(3)")
        self.assertEqual(column["default_specifier"], "DEFAULT")
        self.assertEqual(column["default_expression"], "now()")

    def test_preserves_split_default_specifier_and_expression(self):
        column = chquery.normalize_table_column(
            column={
                "name": "country",
                "normalized_name": "country",
                "type": "String",
                "nullable": False,
                "default_value": "DEFAULT 'Unknown'",
            },
        )

        self.assertEqual(column["default_specifier"], "DEFAULT")
        self.assertEqual(column["default_expression"], "'Unknown'")

    def test_normalizes_comment_codec_ttl_and_primary_key(self):
        column = chquery.normalize_table_column(
            column={
                "name": "ts",
                "normalized_name": "ts",
                "type": "DateTime64(3)",
                "nullable": False,
                "comment": "'event time'",
                "codec": "CODEC(ZSTD(1))",
                "ttl": "ts + toIntervalDay(30)",
                "is_primary_key": True,
            },
        )

        self.assertEqual(column["type"], "DateTime64(3)")
        self.assertEqual(column["comment"], "'event time'")
        self.assertEqual(column["codec"], "CODEC(ZSTD(1))")
        self.assertEqual(column["ttl"], "ts + toIntervalDay(30)")
        self.assertTrue(column["is_primary_key"])

    def test_preserves_normalized_name_for_output_name(self):
        column = chquery.normalize_table_column(
            column={
                "name": "CamelCase",
                "normalized_name": "camel_case",
                "type": "String",
            },
        )

        self.assertEqual(column["name"], "camel_case")
        self.assertEqual(column["type"], "String")

    def test_normalizes_string_scalar(self):
        column = chquery.normalize_table_column(
            column={
                "name": "id",
                "normalized_name": "id",
                "type": "String",
                "nullable": False,
            },
        )

        self.assertEqual(column["type"], "String")

    def test_normalizes_bool_scalar(self):
        column = chquery.normalize_table_column(
            column={
                "name": "is_active",
                "normalized_name": "is_active",
                "type": "Bool",
                "nullable": False,
            },
        )

        self.assertEqual(column["type"], "Bool")

    def test_normalizes_uint64_scalar(self):
        column = chquery.normalize_table_column(
            column={
                "name": "count",
                "normalized_name": "count",
                "type": "UInt64",
                "nullable": False,
            },
        )

        self.assertEqual(column["type"], "UInt64")

    def test_normalizes_array_payload(self):
        column = chquery.normalize_table_column(
            column={
                "name": "tags",
                "normalized_name": "tags",
                "type": "Array(String)",
                "nullable": False,
            },
        )

        self.assertEqual(column["type"], "Array(String)")

    def test_normalizes_map_payload(self):
        column = chquery.normalize_table_column(
            column={
                "name": "metadata",
                "normalized_name": "metadata",
                "type": "Map(String, String)",
                "nullable": False,
            },
        )

        self.assertEqual(column["type"], "Map(String, String)")

    def test_normalizes_low_cardinality_payload(self):
        column = chquery.normalize_table_column(
            column={
                "name": "category",
                "normalized_name": "category",
                "type": "LowCardinality(String)",
                "nullable": False,
            },
        )

        self.assertEqual(column["type"], "LowCardinality(String)")

    def test_normalizes_nullable_string_field(self):
        column = chquery.normalize_table_column(
            column={
                "name": "phone",
                "normalized_name": "phone",
                "type": "Nullable(String)",
                "nullable": False,
            },
        )

        self.assertEqual(column["type"], "Nullable(String)")

    def test_normalizes_nullable_datetime64_field(self):
        column = chquery.normalize_table_column(
            column={
                "name": "deleted_at",
                "normalized_name": "deleted_at",
                "type": "Nullable(DateTime64(3))",
                "nullable": False,
            },
        )

        self.assertEqual(column["type"], "Nullable(DateTime64(3))")

    def test_normalizes_decimal_business_field(self):
        column = chquery.normalize_table_column(
            column={
                "name": "price",
                "normalized_name": "price",
                "type": "Decimal(12,2)",
                "nullable": False,
            },
        )

        self.assertEqual(column["type"], "Decimal(12, 2)")

    def test_preserves_decimal64_business_field(self):
        column = chquery.normalize_table_column(
            column={
                "name": "amount",
                "normalized_name": "amount",
                "type": "Decimal64(4)",
                "nullable": False,
            },
        )

        self.assertEqual(column["type"], "Decimal64(4)")

    def test_normalizes_float64_business_field(self):
        column = chquery.normalize_table_column(
            column={
                "name": "score",
                "normalized_name": "score",
                "type": "Float64",
                "nullable": False,
            },
        )

        self.assertEqual(column["type"], "Float64")

    def test_aggregate_function_over_json_type(self):
        # Regression test for PLTF-842: normalizeColumnInfo() calls
        # columnInfoFromColumnDeclaration() (functions/NormalizeColumnsFromDict.cpp),
        # which used to segfault resolving an AggregateFunction over a JSON value
        # type via DataTypeFactory without a global ClickHouse Context.
        column = chquery.normalize_table_column(
            column={
                "name": "payload",
                "normalized_name": "payload",
                "type": "AggregateFunction(argMax, JSON, DateTime)",
                "nullable": False,
            },
        )

        self.assertEqual(column["type"], "AggregateFunction(argMax, JSON, DateTime)")
        self.assertFalse(column["nullable"])

    # Nested/composed type -> expected (normalized_type, nullable). Covers PLTF-842
    # (JSON nested inside Array/Map/Tuple/Nested/AggregateFunction combinators)
    # plus general composed-type coverage for normalizeColumnInfo()
    # (functions/NormalizeColumnsFromDict.cpp).
    NESTED_AND_COMPOSED_TYPES = [
        ('Array(JSON)', ('Array(JSON)', False)),
        ('Map(String, JSON)', ('Map(String, JSON)', False)),
        ('Tuple(JSON, String)', ('Tuple(JSON, String)', False)),
        ('Tuple(a JSON, b String)', ('Tuple(a JSON, b String)', False)),
        ('Nullable(JSON)', ('Nullable(JSON)', True)),
        ('Nested(a JSON, b String)', ('Nested(a JSON, b String)', False)),
        ('AggregateFunction(argMax, Array(JSON), DateTime)', ('AggregateFunction(argMax, Array(JSON), DateTime)', False)),
        ('AggregateFunction(argMax, Map(String, JSON), DateTime)', ('AggregateFunction(argMax, Map(String, JSON), DateTime)', False)),
        ('AggregateFunction(argMax, Tuple(JSON, String), DateTime)', ('AggregateFunction(argMax, Tuple(JSON, String), DateTime)', False)),
        ('SimpleAggregateFunction(any, JSON)', ('SimpleAggregateFunction(any, JSON)', False)),
        ('SimpleAggregateFunction(any, Array(JSON))', ('SimpleAggregateFunction(any, Array(JSON))', False)),
        ('Array(AggregateFunction(argMax, JSON, DateTime))', ('Array(AggregateFunction(argMax, JSON, DateTime))', False)),
        ('Array(LowCardinality(String))', ('Array(LowCardinality(String))', False)),
        ('Map(String, LowCardinality(String))', ('Map(String, LowCardinality(String))', False)),
        ('Array(Nullable(Int64))', ('Array(Nullable(Int64))', False)),
        ('Map(String, Nullable(Int64))', ('Map(String, Nullable(Int64))', False)),
        ('Map(String, AggregateFunction(sum, Int64))', ('Map(String, AggregateFunction(sum, Int64))', False)),
        ('Nested(a UInt64, b String)', ('Nested(a UInt64, b String)', False)),
        ('Tuple(x Float64, y Float64)', ('Tuple(x Float64, y Float64)', False)),
        ('Array(Tuple(UInt8, String))', ('Array(Tuple(UInt8, String))', False)),
        ('Array(Array(String))', ('Array(Array(String))', False)),
        ('Map(String, Array(String))', ('Map(String, Array(String))', False)),
        ('Map(String, Map(String, Int64))', ('Map(String, Map(String, Int64))', False)),
        ('Variant(String, Int64)', ('Variant(String, Int64)', False)),
        ('Dynamic', ('Dynamic', False)),
        ('LowCardinality(Nullable(String))', ('LowCardinality(Nullable(String))', True)),
    ]

    def test_nested_and_composed_types(self):
        for type_str, (expected_type, expected_nullable) in self.NESTED_AND_COMPOSED_TYPES:
            with self.subTest(type_str):
                column = chquery.normalize_table_column(
                    column={
                        "name": "col",
                        "normalized_name": "col",
                        "type": type_str,
                        "nullable": False,
                    },
                )
                self.assertEqual(column["type"], expected_type)
                self.assertEqual(column["nullable"], expected_nullable)

    def test_low_cardinality_of_json_is_rejected(self):
        with self.assertRaisesRegex(ValueError, 'DataTypeLowCardinality is supported only for'):
            chquery.normalize_table_column(
                column={
                    "name": "col",
                    "normalized_name": "col",
                    "type": "LowCardinality(JSON)",
                    "nullable": False,
                },
            )

    def test_default_now_for_created_at(self):
        column = chquery.normalize_table_column(
            column={
                "name": "created_at",
                "normalized_name": "created_at",
                "type": "DateTime64(3)",
                "nullable": False,
                "default_value": "DEFAULT now()",
            },
        )

        self.assertEqual(column["default_specifier"], "DEFAULT")
        self.assertEqual(column["default_expression"], "now()")

    def test_default_true_for_bool(self):
        column = chquery.normalize_table_column(
            column={
                "name": "is_active",
                "normalized_name": "is_active",
                "type": "Bool",
                "nullable": False,
                "default_value": "DEFAULT true",
            },
        )

        self.assertEqual(column["default_expression"], "true")

    def test_default_zero_for_retry_count(self):
        column = chquery.normalize_table_column(
            column={
                "name": "retry_count",
                "normalized_name": "retry_count",
                "type": "UInt32",
                "nullable": False,
                "default_value": "DEFAULT 0",
            },
        )

        self.assertEqual(column["default_expression"], "0")
