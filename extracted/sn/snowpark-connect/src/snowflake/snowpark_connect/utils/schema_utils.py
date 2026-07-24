#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

import copy

from snowflake import snowpark
from snowflake.snowpark._internal.analyzer.analyzer_utils import unquote_if_quoted
from snowflake.snowpark.types import (
    ArrayType,
    DataType,
    DecimalType,
    MapType,
    StructField,
    StructType,
    _IntegralType,
)


def datatypes_equal(
    dt1: DataType, dt2: DataType, ignore_nullable: bool = False
) -> bool:
    """
    Compare two Snowpark DataTypes for equality, with recursive handling of complex types.

    Handles StructType, ArrayType, MapType, DecimalType precision/scale,
    and unquoted field name comparison for StructFields.
    """
    if type(dt1) != type(dt2):
        return False

    if isinstance(dt1, StructType):
        return _struct_types_equal(dt1, dt2, ignore_nullable)

    if isinstance(dt1, ArrayType):
        return datatypes_equal(dt1.element_type, dt2.element_type, ignore_nullable)

    if isinstance(dt1, MapType):
        return datatypes_equal(
            dt1.key_type, dt2.key_type, ignore_nullable
        ) and datatypes_equal(dt1.value_type, dt2.value_type, ignore_nullable)

    if isinstance(dt1, DecimalType):
        return dt1.precision == dt2.precision and dt1.scale == dt2.scale

    if isinstance(dt1, _IntegralType):
        # Under integral type emulation two same-class integral types (e.g. two
        # LongTypes) can carry different ``_precision`` values that resolve to
        # different emulated types. ``_IntegralType.__eq__`` already compares
        # ``_precision`` when compatible mode is enabled and ignores it
        # otherwise, so delegate to it rather than treating them as equal.
        return dt1 == dt2

    return True


def _struct_types_equal(
    st1: StructType, st2: StructType, ignore_nullable: bool = False
) -> bool:
    if len(st1.fields) != len(st2.fields):
        return False

    for field1, field2 in zip(st1.fields, st2.fields):
        if not _struct_fields_equal(field1, field2, ignore_nullable):
            return False

    return True


def _struct_fields_equal(
    sf1: StructField, sf2: StructField, ignore_nullable: bool = False
) -> bool:
    if unquote_if_quoted(sf1.name) != unquote_if_quoted(sf2.name):
        return False

    if not ignore_nullable and sf1.nullable != sf2.nullable:
        return False

    return datatypes_equal(sf1.datatype, sf2.datatype, ignore_nullable)


def force_nullable_schema(df: snowpark.DataFrame) -> None:
    """Force top-level and nested nullability for new table creation.

    Operates directly on df._plan.attributes because that's the authoritative
    source Snowpark uses for DDL generation. Specifically:
    - Cast expressions only change the datatype, not the outer nullable flag
      on the Attribute, so wrapping columns in casts cannot fix nullability.
    - df.schema is a read-only derived view: StructType._from_attributes()
      rebuilds it from plan attributes on every access. Mutating the schema
      object has no effect because Snowpark's save_as_table path reads
      child.attributes directly (via attribute_to_schema_string) to emit
      NOT NULL constraints in CREATE TABLE DDL.
    """

    def force_nullable_type(data_type: DataType) -> DataType:
        """Recursively force nested composite-type nullability to True."""
        nullable_type = copy.deepcopy(data_type)

        if isinstance(nullable_type, StructType):
            for field in nullable_type.fields:
                field.datatype = force_nullable_type(field.datatype)
                field.nullable = True
        elif isinstance(nullable_type, ArrayType):
            if nullable_type.element_type:
                nullable_type.element_type = force_nullable_type(
                    nullable_type.element_type
                )
            nullable_type.contains_null = True
        elif isinstance(nullable_type, MapType):
            if nullable_type.key_type:
                nullable_type.key_type = force_nullable_type(nullable_type.key_type)
            if nullable_type.value_type:
                nullable_type.value_type = force_nullable_type(nullable_type.value_type)
            nullable_type.value_contains_null = True

        return nullable_type

    for attr in df._plan.attributes:
        attr.datatype = force_nullable_type(attr.datatype)
        attr.nullable = True
