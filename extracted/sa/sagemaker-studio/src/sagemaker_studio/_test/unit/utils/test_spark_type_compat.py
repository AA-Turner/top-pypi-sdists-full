import unittest
from unittest.mock import MagicMock, Mock, PropertyMock, patch

import pyspark.sql.connect.proto as pb2

from sagemaker_studio.utils import spark_type_compat

_VARIANT_BYTES = bytes([0xCA, 0x01, 0x00])
_TIME_BYTES = bytes([0xE2, 0x01, 0x00])


def _schema(*fields):
    schema = pb2.DataType()
    for name, data_type in fields:
        field = schema.struct.fields.add()
        field.name = name
        field.data_type.CopyFrom(data_type)
    return schema


def _integer_type():
    data_type = pb2.DataType()
    data_type.integer.SetInParent()
    return data_type


def _unknown_type(wire_bytes):
    data_type = pb2.DataType()
    data_type.MergeFromString(wire_bytes)
    return data_type


class TestResolveSchema(unittest.TestCase):
    def test_returns_dataframe_when_schema_decodes(self):
        dataframe = Mock()
        type(dataframe).schema = PropertyMock(return_value=Mock())

        self.assertIs(spark_type_compat.resolve_schema(dataframe), dataframe)

    def test_reraises_non_compatibility_error(self):
        original = ValueError("table not found")
        dataframe = Mock()
        type(dataframe).schema = PropertyMock(side_effect=original)

        with self.assertRaises(ValueError) as raised:
            spark_type_compat.resolve_schema(dataframe)

        self.assertIs(raised.exception, original)

    @patch("sagemaker_studio.utils.spark_type_compat._raw_schema")
    def test_reraises_original_when_raw_schema_has_no_variant(self, raw_schema):
        original = Exception("Unsupported data type ")
        dataframe = Mock()
        type(dataframe).schema = PropertyMock(side_effect=original)
        raw_schema.return_value = _schema(("id", _integer_type()))

        with self.assertRaises(Exception) as raised:
            spark_type_compat.resolve_schema(dataframe)

        self.assertIs(raised.exception, original)

    @patch("sagemaker_studio.utils.spark_type_compat._stringify_variant_columns")
    @patch("sagemaker_studio.utils.spark_type_compat._raw_schema")
    def test_returns_projected_dataframe_for_variant(self, raw_schema, stringify):
        dataframe = Mock()
        type(dataframe).schema = PropertyMock(side_effect=Exception("Unsupported data type "))
        raw_schema.return_value = _schema(
            ("id", _integer_type()),
            ("payload", _unknown_type(_VARIANT_BYTES)),
        )
        projected = Mock()
        type(projected).schema = PropertyMock(return_value=Mock())
        stringify.return_value = projected

        result = spark_type_compat.resolve_schema(dataframe)

        self.assertIs(result, projected)
        stringify.assert_called_once_with(dataframe, raw_schema.return_value, {1})

    @patch("sagemaker_studio.utils.spark_type_compat._stringify_variant_columns")
    @patch("sagemaker_studio.utils.spark_type_compat._raw_schema")
    def test_reraises_original_when_projected_schema_fails(self, raw_schema, stringify):
        original = Exception("Unsupported data type ")
        dataframe = Mock()
        type(dataframe).schema = PropertyMock(side_effect=original)
        raw_schema.return_value = _schema(("payload", _unknown_type(_VARIANT_BYTES)))
        projected = Mock()
        type(projected).schema = PropertyMock(side_effect=RuntimeError("projection failed"))
        stringify.return_value = projected

        with self.assertRaises(Exception) as raised:
            spark_type_compat.resolve_schema(dataframe)

        self.assertIs(raised.exception, original)


class TestRawSchema(unittest.TestCase):
    def test_calls_analyze_plan_without_decoding_response(self):
        raw_schema = _schema(("payload", _unknown_type(_VARIANT_BYTES)))
        plan = Mock()
        request = Mock()
        response = Mock(session_id="session-1")
        response.WhichOneof.return_value = "schema"
        response.schema.schema = raw_schema

        client = Mock()
        client._session_id = "session-1"
        client._analyze_plan_request_with_metadata.return_value = request
        client._stub.AnalyzePlan.return_value = response
        client._builder.metadata.return_value = [("x-test", "value")]

        dataframe = Mock()
        dataframe.sparkSession.client = client
        dataframe._plan.to_proto.return_value = plan

        result = spark_type_compat._raw_schema(dataframe)

        self.assertIs(result, raw_schema)
        dataframe._plan.to_proto.assert_called_once_with(client)
        request.schema.plan.CopyFrom.assert_called_once_with(plan)
        client._stub.AnalyzePlan.assert_called_once_with(request, metadata=[("x-test", "value")])

    def test_rejects_response_for_another_session(self):
        client = Mock()
        client._session_id = "session-1"
        client._stub.AnalyzePlan.return_value = Mock(session_id="session-2")
        dataframe = Mock()
        dataframe.sparkSession.client = client

        with self.assertRaisesRegex(RuntimeError, "invalid schema response"):
            spark_type_compat._raw_schema(dataframe)


class TestUnknownKinds(unittest.TestCase):
    def test_classifies_variant_wire_field(self):
        self.assertEqual(
            spark_type_compat._unknown_kinds(_unknown_type(_VARIANT_BYTES)),
            frozenset({spark_type_compat._VARIANT}),
        )

    def test_rejects_other_unknown_wire_field(self):
        self.assertEqual(
            spark_type_compat._unknown_kinds(_unknown_type(_TIME_BYTES)),
            frozenset({spark_type_compat._OTHER}),
        )

    def test_finds_variant_nested_in_struct_array_and_map(self):
        variant = _unknown_type(_VARIANT_BYTES)

        nested_struct = _schema(("nested", variant))
        array = pb2.DataType()
        array.array.element_type.CopyFrom(variant)
        value_map = pb2.DataType()
        value_map.map.key_type.CopyFrom(_integer_type())
        value_map.map.value_type.CopyFrom(variant)

        for data_type in (nested_struct, array, value_map):
            with self.subTest(kind=data_type.WhichOneof("kind")):
                self.assertEqual(
                    spark_type_compat._unknown_kinds(data_type),
                    frozenset({spark_type_compat._VARIANT}),
                )

    def test_finds_variant_and_other_unknown_types_together(self):
        nested = _schema(
            ("variant", _unknown_type(_VARIANT_BYTES)),
            ("time", _unknown_type(_TIME_BYTES)),
        )

        self.assertEqual(
            spark_type_compat._unknown_kinds(nested),
            frozenset({spark_type_compat._VARIANT, spark_type_compat._OTHER}),
        )

    def test_variant_column_indexes_reject_other_unknown_types(self):
        raw_schema = _schema(("time", _unknown_type(_TIME_BYTES)))

        with self.assertRaisesRegex(RuntimeError, "unknown non-VARIANT"):
            spark_type_compat._variant_column_indexes(raw_schema)


class TestStringifyVariantColumns(unittest.TestCase):
    @patch("pyspark.sql.functions.to_json")
    @patch("pyspark.sql.functions.col")
    def test_renames_by_position_and_restores_original_names(self, col, to_json):
        raw_schema = _schema(
            ("duplicate", _integer_type()),
            ("duplicate", _unknown_type(_VARIANT_BYTES)),
            ("a.b", _integer_type()),
        )
        source_columns = [MagicMock(), MagicMock(), MagicMock()]
        aliased_columns = [Mock(), Mock(), Mock()]
        col.side_effect = source_columns
        source_columns[0].alias.return_value = aliased_columns[0]
        json_column = MagicMock()
        to_json.return_value = json_column
        json_column.alias.return_value = aliased_columns[1]
        source_columns[2].alias.return_value = aliased_columns[2]

        dataframe = Mock()
        renamed = Mock()
        projected = Mock()
        dataframe.toDF.return_value = renamed
        renamed.select.return_value = projected

        result = spark_type_compat._stringify_variant_columns(dataframe, raw_schema, {1})

        self.assertIs(result, projected)
        dataframe.toDF.assert_called_once_with(
            "__smus_variant_compat_0",
            "__smus_variant_compat_1",
            "__smus_variant_compat_2",
        )
        to_json.assert_called_once_with(source_columns[1])
        renamed.select.assert_called_once_with(*aliased_columns)
        source_columns[0].alias.assert_called_once_with("duplicate")
        json_column.alias.assert_called_once_with("duplicate")
        source_columns[2].alias.assert_called_once_with("a.b")


if __name__ == "__main__":
    unittest.main()
