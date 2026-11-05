"""Compatibility helpers for Spark Connect result schemas."""

_VARIANT_PROTO_BYTES = b"\xca\x01\x00"
_VARIANT = "variant"
_OTHER = "other"


def resolve_schema(dataframe):
    """Resolve a result schema, stringifying Spark 4 VARIANT columns when needed."""
    try:
        dataframe.schema
        return dataframe
    except Exception as original_error:
        if not _is_unsupported_type_error(original_error):
            raise

        try:
            raw_schema = _raw_schema(dataframe)
            variant_indexes = _variant_column_indexes(raw_schema)
            projected = _stringify_variant_columns(dataframe, raw_schema, variant_indexes)
            projected.schema
            return projected
        except Exception:
            raise original_error from None


def _is_unsupported_type_error(error):
    return type(error) is Exception and str(error).strip() == "Unsupported data type"


def _raw_schema(dataframe):
    client = dataframe.sparkSession.client
    plan = dataframe._plan.to_proto(client)
    request = client._analyze_plan_request_with_metadata()
    request.schema.plan.CopyFrom(plan)
    response = client._stub.AnalyzePlan(request, metadata=client._builder.metadata())

    if response.session_id != client._session_id or response.WhichOneof("result") != "schema":
        raise RuntimeError("Spark Connect returned an invalid schema response")
    return response.schema.schema


def _variant_column_indexes(raw_schema):
    if raw_schema.WhichOneof("kind") != "struct":
        raise RuntimeError("Spark Connect result schema is not a struct")

    variant_indexes = set()
    for index, field in enumerate(raw_schema.struct.fields):
        unknown_kinds = _unknown_kinds(field.data_type)
        if _OTHER in unknown_kinds:
            raise RuntimeError("Spark Connect schema contains an unknown non-VARIANT type")
        if _VARIANT in unknown_kinds:
            variant_indexes.add(index)

    if not variant_indexes:
        raise RuntimeError("Spark Connect schema does not contain VARIANT")
    return variant_indexes


def _unknown_kinds(data_type):
    kind = data_type.WhichOneof("kind")
    if kind is None:
        if data_type.SerializeToString() == _VARIANT_PROTO_BYTES:
            return frozenset({_VARIANT})
        return frozenset({_OTHER})

    if kind == "struct":
        return _merge_unknown_kinds(
            _unknown_kinds(field.data_type) for field in data_type.struct.fields
        )
    if kind == "array":
        return _unknown_kinds(data_type.array.element_type)
    if kind == "map":
        return _merge_unknown_kinds(
            (
                _unknown_kinds(data_type.map.key_type),
                _unknown_kinds(data_type.map.value_type),
            )
        )
    if kind == "udt" and data_type.udt.HasField("sql_type"):
        return _unknown_kinds(data_type.udt.sql_type)
    return frozenset()


def _merge_unknown_kinds(kind_sets):
    merged = set()
    for kinds in kind_sets:
        merged.update(kinds)
    return frozenset(merged)


def _stringify_variant_columns(dataframe, raw_schema, variant_indexes):
    from pyspark.sql import functions as spark_functions

    temporary_names = [
        f"__smus_variant_compat_{index}" for index in range(len(raw_schema.struct.fields))
    ]
    renamed = dataframe.toDF(*temporary_names)
    projections = []

    for index, field in enumerate(raw_schema.struct.fields):
        column = spark_functions.col(temporary_names[index])
        if index in variant_indexes:
            column = spark_functions.to_json(column)
        projections.append(column.alias(field.name))

    return renamed.select(*projections)
