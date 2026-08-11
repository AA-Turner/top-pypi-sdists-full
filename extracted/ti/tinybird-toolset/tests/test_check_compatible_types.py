import unittest
from chtoolset import query as chquery
import json
from types import SimpleNamespace

# Types from
# ./clickhouse local --query "SELECT * from system.data_type_families ORDER BY name format JSONEachRow" | awk '{ print "'''\''" $0 "'''\''," }'
# Modified types that require parameters to have them
EXISTING_TYPES = [
    # '{"name":"AggregateFunction","case_insensitive":0,"alias_to":""}',
    # '{"name":"Array","case_insensitive":0,"alias_to":""}',
    '{"name":"BIGINT","case_insensitive":1,"alias_to":"Int64"}',
    '{"name":"BIGINT SIGNED","case_insensitive":1,"alias_to":"Int64"}',
    '{"name":"BIGINT UNSIGNED","case_insensitive":1,"alias_to":"UInt64"}',
    # '{"name":"BINARY","case_insensitive":1,"alias_to":"FixedString"}',
    '{"name":"BINARY LARGE OBJECT","case_insensitive":1,"alias_to":"String"}',
    '{"name":"BINARY VARYING","case_insensitive":1,"alias_to":"String"}',
    '{"name":"BIT","case_insensitive":1,"alias_to":"UInt64"}',
    '{"name":"BLOB","case_insensitive":1,"alias_to":"String"}',
    '{"name":"BYTE","case_insensitive":1,"alias_to":"Int8"}',
    '{"name":"BYTEA","case_insensitive":1,"alias_to":"String"}',
    '{"name":"Bool","case_insensitive":1,"alias_to":""}',
    '{"name":"CHAR","case_insensitive":1,"alias_to":"String"}',
    '{"name":"CHAR LARGE OBJECT","case_insensitive":1,"alias_to":"String"}',
    '{"name":"CHAR VARYING","case_insensitive":1,"alias_to":"String"}',
    '{"name":"CHARACTER","case_insensitive":1,"alias_to":"String"}',
    '{"name":"CHARACTER LARGE OBJECT","case_insensitive":1,"alias_to":"String"}',
    '{"name":"CHARACTER VARYING","case_insensitive":1,"alias_to":"String"}',
    '{"name":"CLOB","case_insensitive":1,"alias_to":"String"}',
    '{"name":"DEC","case_insensitive":1,"alias_to":"Decimal"}',
    '{"name":"DOUBLE","case_insensitive":1,"alias_to":"Float64"}',
    '{"name":"DOUBLE PRECISION","case_insensitive":1,"alias_to":"Float64"}',
    '{"name":"Date","case_insensitive":1,"alias_to":""}',
    '{"name":"Date32","case_insensitive":1,"alias_to":""}',
    '{"name":"DateTime","case_insensitive":1,"alias_to":""}',
    '{"name":"DateTime32","case_insensitive":1,"alias_to":""}',
    '{"name":"DateTime64","case_insensitive":1,"alias_to":""}',
    # '{"name":"Decimal","case_insensitive":1,"alias_to":""}',
    # '{"name":"Decimal128","case_insensitive":1,"alias_to":""}',
    # '{"name":"Decimal256","case_insensitive":1,"alias_to":""}',
    # '{"name":"Decimal32","case_insensitive":1,"alias_to":""}',
    # '{"name":"Decimal64","case_insensitive":1,"alias_to":""}',
    # '{"name":"ENUM","case_insensitive":1,"alias_to":"Enum"}',
    # '{"name":"Enum","case_insensitive":1,"alias_to":""}',
    # '{"name":"Enum16","case_insensitive":0,"alias_to":""}',
    # '{"name":"Enum8","case_insensitive":0,"alias_to":""}',
    # '{"name":"FIXED","case_insensitive":1,"alias_to":"Decimal"}',
    '{"name":"FLOAT","case_insensitive":1,"alias_to":"Float32"}',
    # '{"name":"FixedString","case_insensitive":0,"alias_to":""}',
    '{"name":"Float32","case_insensitive":0,"alias_to":""}',
    '{"name":"Float64","case_insensitive":0,"alias_to":""}',
    '{"name":"GEOMETRY","case_insensitive":1,"alias_to":"String"}',
    '{"name":"INET4","case_insensitive":1,"alias_to":"IPv4"}',
    '{"name":"INET6","case_insensitive":1,"alias_to":"IPv6"}',
    '{"name":"INT","case_insensitive":1,"alias_to":"Int32"}',
    '{"name":"INT SIGNED","case_insensitive":1,"alias_to":"Int32"}',
    '{"name":"INT UNSIGNED","case_insensitive":1,"alias_to":"UInt32"}',
    '{"name":"INT1","case_insensitive":1,"alias_to":"Int8"}',
    '{"name":"INT1 SIGNED","case_insensitive":1,"alias_to":"Int8"}',
    '{"name":"INT1 UNSIGNED","case_insensitive":1,"alias_to":"UInt8"}',
    '{"name":"INTEGER","case_insensitive":1,"alias_to":"Int32"}',
    '{"name":"INTEGER SIGNED","case_insensitive":1,"alias_to":"Int32"}',
    '{"name":"INTEGER UNSIGNED","case_insensitive":1,"alias_to":"UInt32"}',
    '{"name":"IPv4","case_insensitive":0,"alias_to":""}',
    '{"name":"IPv6","case_insensitive":0,"alias_to":""}',
    '{"name":"Int128","case_insensitive":0,"alias_to":""}',
    '{"name":"Int16","case_insensitive":0,"alias_to":""}',
    '{"name":"Int256","case_insensitive":0,"alias_to":""}',
    '{"name":"Int32","case_insensitive":0,"alias_to":""}',
    '{"name":"Int64","case_insensitive":0,"alias_to":""}',
    '{"name":"Int8","case_insensitive":0,"alias_to":""}',
    '{"name":"IntervalDay","case_insensitive":0,"alias_to":""}',
    '{"name":"IntervalHour","case_insensitive":0,"alias_to":""}',
    '{"name":"IntervalMicrosecond","case_insensitive":0,"alias_to":""}',
    '{"name":"IntervalMillisecond","case_insensitive":0,"alias_to":""}',
    '{"name":"IntervalMinute","case_insensitive":0,"alias_to":""}',
    '{"name":"IntervalMonth","case_insensitive":0,"alias_to":""}',
    '{"name":"IntervalNanosecond","case_insensitive":0,"alias_to":""}',
    '{"name":"IntervalQuarter","case_insensitive":0,"alias_to":""}',
    '{"name":"IntervalSecond","case_insensitive":0,"alias_to":""}',
    '{"name":"IntervalWeek","case_insensitive":0,"alias_to":""}',
    '{"name":"IntervalYear","case_insensitive":0,"alias_to":""}',
    '{"name":"Dynamic","case_insensitive":1,"alias_to":""}',
    '{"name":"Dynamic(max_types=1)","case_insensitive":1,"alias_to":""}',
    '{"name":"JSON","case_insensitive":1,"alias_to":""}',
    '{"name":"JSON(a.b UInt32, SKIP a.e)","case_insensitive":1,"alias_to":""}',
    '{"name":"JSON(max_dynamic_paths=1)","case_insensitive":1,"alias_to":""}',
    '{"name":"JSON(max_dynamic_paths=1, max_dynamic_types=1, a.b UInt32, SKIP a.e)","case_insensitive":1,"alias_to":""}',
    '{"name":"JSON(max_dynamic_types=1)","case_insensitive":1,"alias_to":""}',
    '{"name":"LONGBLOB","case_insensitive":1,"alias_to":"String"}',
    '{"name":"LONGTEXT","case_insensitive":1,"alias_to":"String"}',
    # '{"name":"LowCardinality","case_insensitive":0,"alias_to":""}',
    '{"name":"MEDIUMBLOB","case_insensitive":1,"alias_to":"String"}',
    '{"name":"MEDIUMINT","case_insensitive":1,"alias_to":"Int32"}',
    '{"name":"MEDIUMINT SIGNED","case_insensitive":1,"alias_to":"Int32"}',
    '{"name":"MEDIUMINT UNSIGNED","case_insensitive":1,"alias_to":"UInt32"}',
    '{"name":"MEDIUMTEXT","case_insensitive":1,"alias_to":"String"}',
    # '{"name":"Map","case_insensitive":0,"alias_to":""}',
    '{"name":"MultiPolygon","case_insensitive":0,"alias_to":""}',
    '{"name":"NATIONAL CHAR","case_insensitive":1,"alias_to":"String"}',
    '{"name":"NATIONAL CHAR VARYING","case_insensitive":1,"alias_to":"String"}',
    '{"name":"NATIONAL CHARACTER","case_insensitive":1,"alias_to":"String"}',
    '{"name":"NATIONAL CHARACTER LARGE OBJECT","case_insensitive":1,"alias_to":"String"}',
    '{"name":"NATIONAL CHARACTER VARYING","case_insensitive":1,"alias_to":"String"}',
    '{"name":"NCHAR","case_insensitive":1,"alias_to":"String"}',
    '{"name":"NCHAR LARGE OBJECT","case_insensitive":1,"alias_to":"String"}',
    '{"name":"NCHAR VARYING","case_insensitive":1,"alias_to":"String"}',
    # '{"name":"NUMERIC","case_insensitive":1,"alias_to":"Decimal"}',
    '{"name":"NVARCHAR","case_insensitive":1,"alias_to":"String"}',
    # '{"name":"Nested","case_insensitive":0,"alias_to":""}',
    '{"name":"Nothing","case_insensitive":0,"alias_to":""}',
    # '{"name":"Nullable","case_insensitive":0,"alias_to":""}',
    # '{"name":"Object","case_insensitive":0,"alias_to":""}',
    '{"name":"Point","case_insensitive":0,"alias_to":""}',
    '{"name":"Polygon","case_insensitive":0,"alias_to":""}',
    '{"name":"REAL","case_insensitive":1,"alias_to":"Float32"}',
    '{"name":"Ring","case_insensitive":0,"alias_to":""}',
    '{"name":"SET","case_insensitive":1,"alias_to":"UInt64"}',
    '{"name":"SIGNED","case_insensitive":1,"alias_to":"Int64"}',
    '{"name":"SINGLE","case_insensitive":1,"alias_to":"Float32"}',
    '{"name":"SMALLINT","case_insensitive":1,"alias_to":"Int16"}',
    '{"name":"SMALLINT SIGNED","case_insensitive":1,"alias_to":"Int16"}',
    '{"name":"SMALLINT UNSIGNED","case_insensitive":1,"alias_to":"UInt16"}',
    # '{"name":"SimpleAggregateFunction","case_insensitive":0,"alias_to":""}',
    '{"name":"String","case_insensitive":0,"alias_to":""}',
    '{"name":"TEXT","case_insensitive":1,"alias_to":"String"}',
    '{"name":"TIME","case_insensitive":1,"alias_to":"Int64"}',
    '{"name":"TIMESTAMP","case_insensitive":1,"alias_to":"DateTime"}',
    '{"name":"TINYBLOB","case_insensitive":1,"alias_to":"String"}',
    '{"name":"TINYINT","case_insensitive":1,"alias_to":"Int8"}',
    '{"name":"TINYINT SIGNED","case_insensitive":1,"alias_to":"Int8"}',
    '{"name":"TINYINT UNSIGNED","case_insensitive":1,"alias_to":"UInt8"}',
    '{"name":"TINYTEXT","case_insensitive":1,"alias_to":"String"}',
    # '{"name":"Tuple","case_insensitive":0,"alias_to":""}',
    '{"name":"UInt128","case_insensitive":0,"alias_to":""}',
    '{"name":"UInt16","case_insensitive":0,"alias_to":""}',
    '{"name":"UInt256","case_insensitive":0,"alias_to":""}',
    '{"name":"UInt32","case_insensitive":0,"alias_to":""}',
    '{"name":"UInt64","case_insensitive":0,"alias_to":""}',
    '{"name":"UInt8","case_insensitive":0,"alias_to":""}',
    '{"name":"UNSIGNED","case_insensitive":1,"alias_to":"UInt64"}',
    '{"name":"UUID","case_insensitive":0,"alias_to":""}',
    '{"name":"VARBINARY","case_insensitive":1,"alias_to":"String"}',
    '{"name":"VARCHAR","case_insensitive":1,"alias_to":"String"}',
    '{"name":"VARCHAR2","case_insensitive":1,"alias_to":"String"}',
    # '{"name":"Variant","case_insensitive":0,"alias_to":""}',
    '{"name":"YEAR","case_insensitive":1,"alias_to":"UInt16"}',
    '{"name":"bool","case_insensitive":1,"alias_to":"Bool"}',
    '{"name":"boolean","case_insensitive":1,"alias_to":"Bool"}',
]


class TestCast(unittest.TestCase):
    def test_invalid_params(self):
        with self.assertRaises(TypeError):
            chquery.check_compatible_types()

        with self.assertRaises(TypeError):
            chquery.check_compatible_types("Int64")

        with self.assertRaises(TypeError):
            chquery.check_compatible_types("Int64 Int64")

        with self.assertRaises(TypeError):
            chquery.check_compatible_types(None, "Int64")

        with self.assertRaises(TypeError):
            chquery.check_compatible_types(0, "Int64")

        with self.assertRaises(TypeError):
            chquery.check_compatible_types({0, 1, 3}, "Int64")

        with self.assertRaises(TypeError):
            chquery.check_compatible_types([0, 1, 2], "Int64")

        with self.assertRaises(TypeError):
            chquery.check_compatible_types(source="someType", notTheTarget="Other")

        with self.assertRaises(TypeError):
            chquery.check_compatible_types(notTheSource="someType", target="Other")

    def test_invalid_types(self):
        with self.assertRaisesRegex(ValueError, '^Unknown data type family: someType'):
            chquery.check_compatible_types(source="someType", target="Int64")

        with self.assertRaisesRegex(ValueError, '^Unknown data type family: someType'):
            chquery.check_compatible_types(source="Int64", target="someType")

        with self.assertRaisesRegex(ValueError,
                                    "Unknown data type family: Int60. Maybe you meant.*"):
            chquery.check_compatible_types(source="Int60", target="Int64")

        with self.assertRaisesRegex(ValueError, '^Illegal type Int64 of last argument for aggregate function with If '
                                                'suffix'):
            chquery.check_compatible_types(source="SimpleAggregateFunction(anyIf, String, Int64)", target="Int64")

    def test_cast_type_to_itself_should_be_ok(self):
        for json_string in EXISTING_TYPES:
            with self.subTest(json_string):
                ob = json.loads(json_string, object_hook=lambda d: SimpleNamespace(**d))
                self.assertTrue(chquery.check_compatible_types(ob.name, ob.name))

    def test_to_and_from_string(self):
        with self.assertRaisesRegex(ValueError, 'Automatic casting to String is disallowed'):
            chquery.check_compatible_types('Int64', 'String')
        with self.assertRaisesRegex(ValueError, 'Automatic casting to FixedString.* is disallowed'):
            chquery.check_compatible_types('Int64', 'FixedString(20)')
        with self.assertRaisesRegex(ValueError, 'String might contain values that won\'t fit inside a column of type Int64'):
            chquery.check_compatible_types('String', 'Int64')

        self.assertTrue(chquery.check_compatible_types('FixedString(20)', 'String'))
        with self.assertRaisesRegex(ValueError, 'String might contain values that won\'t fit inside a column of type FixedString.*'):
            chquery.check_compatible_types('String', 'FixedString(20)')

    def test_decimal_types_should_be_ok(self):
        self.assertTrue(chquery.check_compatible_types('Decimal(64, 3)', 'Decimal(64, 3)'))
        self.assertTrue(chquery.check_compatible_types('NUMERIC(64, 3)', 'NUMERIC(64, 3)'))
        self.assertTrue(chquery.check_compatible_types('Decimal32(1)', 'Decimal32(1)'))

        # Interaction with different scales is buggy: https://github.com/ClickHouse/ClickHouse/issues/29831
        # self.assertTrue(chquery.check_compatible_types('Decimal(64, 3)', 'Decimal(64, 6)'))
        # self.assertTrue(chquery.check_compatible_types('Decimal32(1)', 'Decimal32(3)'))
        # self.assertTrue(chquery.check_compatible_types('Decimal64(1)', 'Decimal64(3)'))
        # self.assertTrue(chquery.check_compatible_types('Decimal128(1)', 'Decimal128(3)'))
        # self.assertTrue(chquery.check_compatible_types('Decimal256(1)', 'Decimal256(3)'))
        self.assertTrue(chquery.check_compatible_types('Int64', 'Decimal64(0)'))
        # self.assertTrue(chquery.check_compatible_types('Int128', 'Decimal128(0)'))  # Not supported (23.2)
        # self.assertTrue(chquery.check_compatible_types('Int256', 'Decimal256(0)'))  # Not supported (23.2)

    def test_tuples(self):
        self.assertTrue(chquery.check_compatible_types('Tuple(Int64, String)', 'Tuple(Int64, String)'))
        self.assertTrue(chquery.check_compatible_types('Tuple(Int32, String)', 'Tuple(Int64, String)'))

        with self.assertRaisesRegex(ValueError, '.*might contain values that won\'t fit inside a column of type.*'):
            chquery.check_compatible_types('Tuple(Int64, String)', 'Tuple(Int32, String)')

    def test_cast_type_to_alias_should_be_ok(self):
        for json_string in EXISTING_TYPES:
            with self.subTest(json_string):
                ob = json.loads(json_string, object_hook=lambda d: SimpleNamespace(**d))
                if ob.alias_to:
                    self.assertTrue(chquery.check_compatible_types(ob.name, ob.alias_to))
                    self.assertTrue(chquery.check_compatible_types(ob.alias_to, ob.name))

    def test_source_larger_than_target(self):
        source = 'UInt256'
        for target in ['Int8', 'Int16', 'Int32', 'Int64', 'Int128', 'Int256',
                       'UInt8', 'UInt16', 'UInt32', 'UInt64', 'UInt128']:
            with self.subTest(target):
                with self.assertRaisesRegex(ValueError,
                                            "UInt256 might contain values that won't fit inside a column of type .*",
                                            msg=f"{source} + {target}"):
                    chquery.check_compatible_types(source=source, target=target)

    def test_floating_point_values(self):
        for valid_f32_source in ['UInt8', 'UInt16', 'Int8', 'Int16']:
            with self.subTest(valid_f32_source):
                self.assertTrue(chquery.check_compatible_types(valid_f32_source, 'Float32'), msg=valid_f32_source)

        for valid_f64_source in ['UInt8', 'UInt16', 'UInt32', 'Int8', 'Int16', 'Int32', 'Float32']:
            with self.subTest(valid_f64_source):
                self.assertTrue(chquery.check_compatible_types(valid_f64_source, 'Float64'))

        with self.assertRaisesRegex(ValueError,
                                    "Float64 might contain values that won't fit inside a column of type Float32"):
            self.assertTrue(chquery.check_compatible_types('Float64', 'Float32'))

        for invalid_f32_source in ['String', 'Int32', 'Int64', 'Int128', 'Int256', 'UInt32']:
            with self.subTest(invalid_f32_source):
                with self.assertRaisesRegex(ValueError, ".*"):
                    self.assertTrue(chquery.check_compatible_types(invalid_f32_source, 'Float32'))

    def test_compatible_types(self):
        source = 'UInt8'
        for target in ['Int16', 'Int32', 'Int64', 'Int128', 'Int256',
                       'UInt8', 'UInt16', 'UInt32', 'UInt64', 'UInt128',
                       'Float32', 'Float64']:
            with self.subTest(target):
                self.assertTrue(chquery.check_compatible_types(source, target), msg=f"{source} + {target}")

    def test_compatible_types_LowCardinality(self):
        source = 'UInt8'
        for target in ['Int16', 'Int32', 'Int64', 'Int128', 'Int256',
                       'UInt8', 'UInt16', 'UInt32', 'UInt64', 'UInt128',
                       'Float32', 'Float64']:
            with self.subTest(target):
                self.assertTrue(chquery.check_compatible_types(f"LowCardinality({source})", target), msg=f"{source} + {target}")
                self.assertTrue(chquery.check_compatible_types(source, f"LowCardinality({target})"), msg=f"{source} + {target}")

    def test_compatible_types_target_Nullable_are_ok(self):
        for source in ['UInt8', 'Nullable(UInt8)']:
            for target in ['Int16', 'Int32', 'Int64', 'Int128', 'Int256',
                           'UInt8', 'UInt16', 'UInt32', 'UInt64', 'UInt128',
                           'Float32', 'Float64']:
                with self.subTest(f"{source} to ${target}"):
                    self.assertTrue(chquery.check_compatible_types(source, f"Nullable({target})"), msg=f"{source} + {target}")

    def test_compatible_types_target_LowCardinality_Nullable(self):
        for source in ['UInt8', 'Nullable(UInt8)']:
            for target in ['Int16', 'Int32', 'Int64', 'Int128', 'Int256',
                           'UInt8', 'UInt16', 'UInt32', 'UInt64', 'UInt128',
                           'Float32', 'Float64']:
                with self.subTest(f"{source} to ${target}"):
                    self.assertTrue(chquery.check_compatible_types(source, f"LowCardinality(Nullable({target}))"),
                                    msg=f"{source} + {target}")

    def test_source_Nullable_but_not_target_should_fail(self):
        source = 'Nullable(UInt8)'
        for target in ['Int16', 'Int32', 'Int64', 'Int128', 'Int256',
                       'UInt8', 'UInt16', 'UInt32', 'UInt64', 'UInt128',
                       'Float32', 'Float64']:
            with self.subTest(f"{source} to ${target}"):
                with self.assertRaisesRegex(ValueError, "Nullable\\(UInt8\\) might contain values that won't fit "
                                                        "inside a column of type .*",
                                            msg=f"{source} + {target}"):
                    chquery.check_compatible_types(source=source, target=target)

    def test_works_with_datetime(self):
        self.assertTrue(chquery.check_compatible_types('DateTime', 'DateTime64'))
        self.assertTrue(chquery.check_compatible_types('DateTime32', 'DateTime64'))
        self.assertTrue(chquery.check_compatible_types("DateTime('UTC')", 'DateTime64'))
        self.assertTrue(chquery.check_compatible_types("DateTime32('Europe/Madrid')", "DateTime64(0, 'Europe/Moscow')"))
        self.assertTrue(chquery.check_compatible_types("DateTime64(2, 'UTC')", "DateTime64(5, 'Europe/Madrid')"))

    def test_fails_datetime64_to_datetime(self):
        with self.assertRaises(ValueError) as error:
            self.assertTrue(chquery.check_compatible_types('DateTime64', 'DateTime32'))
        self.assertEqual(str(error.exception),
                         """DateTime64 might contain values that won't fit inside a column of type DateTime32""")

        with self.assertRaises(ValueError) as error:
            self.assertTrue(chquery.check_compatible_types('DateTime64', 'DateTime'))
        self.assertEqual(str(error.exception),
                         """DateTime64 might contain values that won't fit inside a column of type DateTime""")

    def test_works_with_simple_aggregate_functions(self):
        self.assertTrue(chquery.check_compatible_types('SimpleAggregateFunction(groupArrayArray, Array(String))',
                                                       'SimpleAggregateFunction(groupArrayArray, Array(String))'))

        self.assertTrue(chquery.check_compatible_types('SimpleAggregateFunction(sum, Int64)',
                                                       'SimpleAggregateFunction(sum, Nullable(Int64))'))

    def test_works_with_aggregate_functions(self):
        self.assertTrue(chquery.check_compatible_types('AggregateFunction(sum, Int8)',
                                                       'AggregateFunction(sum, Int8)'))
        self.assertTrue(chquery.check_compatible_types('AggregateFunction(sum, Int16)',
                                                       'AggregateFunction(sum, SMALLINT)'))

    def test_rejects_incompatible_agg_functions(self):
        with self.assertRaises(ValueError) as error:
            chquery.check_compatible_types('AggregateFunction(sum, Int8)', 'AggregateFunction(avg, Int8)')
        self.assertEqual(str(error.exception),
                         """Incompatible aggregate functions: sum vs avg""")

    def test_rejects_if_agg_arguments_are_incompatible(self):
        with self.assertRaises(ValueError) as error:
            self.assertTrue(chquery.check_compatible_types('AggregateFunction(sum, Int16)', 'AggregateFunction(sum, Int8)'))
        self.assertEqual(str(error.exception), """Different #0 argument: Int16 vs Int8""")

    def test_works_with_aggregate_functions_over_json(self):
        # Regression test for PLTF-842: resolving an AggregateFunction/
        # SimpleAggregateFunction over a JSON value type used to segfault.
        # DataTypeObject::doGetDefaultSerialization() unconditionally
        # dereferences Context::getGlobalContextInstance() to read the
        # allow_simdjson setting, which is null since chtoolset never runs
        # a real clickhouse-server. See CheckCompatibleTypes.cpp.
        self.assertTrue(chquery.check_compatible_types(
            'AggregateFunction(argMax, JSON, DateTime)',
            'AggregateFunction(argMax, JSON, DateTime)'))

        self.assertTrue(chquery.check_compatible_types(
            'SimpleAggregateFunction(any, JSON)',
            'SimpleAggregateFunction(any, JSON)'))

    def test_rejects_if_agg_parameters_are_incompatible(self):
        with self.assertRaises(ValueError) as error:
            self.assertTrue(chquery.check_compatible_types('AggregateFunction(topK, String)', 'AggregateFunction(topK(100), String)'))
        self.assertEqual(str(error.exception), """Different number of parameters""")

        with self.assertRaises(ValueError) as error:
            self.assertTrue(chquery.check_compatible_types('AggregateFunction(topK(99), String)', 'AggregateFunction(topK(100), String)'))
        self.assertEqual(str(error.exception), """Different #0 parameter: 99 vs 100""")

    # Nested/composed types that must resolve without crashing. Covers PLTF-842
    # (JSON nested inside Array/Map/Tuple/Nested/AggregateFunction combinators,
    # which all previously segfaulted resolving JSON's default serialization
    # without a global ClickHouse Context) plus general composed-type coverage.
    NESTED_AND_COMPOSED_TYPES = [
        'Array(JSON)',
        'Map(String, JSON)',
        'Tuple(JSON, String)',
        'Tuple(a JSON, b String)',
        'Nullable(JSON)',
        'Nested(a JSON, b String)',
        'AggregateFunction(argMax, Array(JSON), DateTime)',
        'AggregateFunction(argMax, Map(String, JSON), DateTime)',
        'AggregateFunction(argMax, Tuple(JSON, String), DateTime)',
        'SimpleAggregateFunction(any, Array(JSON))',
        'Array(AggregateFunction(argMax, JSON, DateTime))',
        'Array(LowCardinality(String))',
        'Map(String, LowCardinality(String))',
        'Array(Nullable(Int64))',
        'Map(String, Nullable(Int64))',
        'Map(String, AggregateFunction(sum, Int64))',
        'Nested(a UInt64, b String)',
        'Tuple(x Float64, y Float64)',
        'Array(Tuple(UInt8, String))',
        'Array(Array(String))',
        'Map(String, Array(String))',
        'Map(String, Map(String, Int64))',
        'Variant(String, Int64)',
        'Dynamic',
        'LowCardinality(Nullable(String))',
    ]

    def test_nested_and_composed_types_self_compatible(self):
        for type_str in self.NESTED_AND_COMPOSED_TYPES:
            with self.subTest(type_str):
                self.assertTrue(chquery.check_compatible_types(type_str, type_str))

    def test_low_cardinality_of_json_is_rejected(self):
        with self.assertRaisesRegex(ValueError, 'DataTypeLowCardinality is supported only for'):
            chquery.check_compatible_types('LowCardinality(JSON)', 'LowCardinality(JSON)')
