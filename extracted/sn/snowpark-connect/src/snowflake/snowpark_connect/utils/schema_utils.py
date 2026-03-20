#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

from snowflake.snowpark._internal.analyzer.analyzer_utils import unquote_if_quoted
from snowflake.snowpark.types import (
    ArrayType,
    DataType,
    DecimalType,
    MapType,
    StructField,
    StructType,
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
