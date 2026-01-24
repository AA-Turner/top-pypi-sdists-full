#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

import threading

from snowflake import snowpark
from snowflake.snowpark.types import (
    ArrayType,
    ByteType,
    DataType,
    DecimalType,
    IntegerType,
    LongType,
    MapType,
    ShortType,
    StructField,
    StructType,
    _IntegralType,
)

_integral_types_conversion_enabled: bool = False
_client_mode_lock = threading.Lock()


def set_integral_types_conversion(enabled: bool) -> None:
    global _integral_types_conversion_enabled

    with _client_mode_lock:
        if _integral_types_conversion_enabled == enabled:
            return

        _integral_types_conversion_enabled = enabled

        if enabled:
            snowpark.context._integral_type_default_precision = {
                LongType: 19,
                IntegerType: 10,
                ShortType: 5,
                ByteType: 3,
            }
        else:
            snowpark.context._integral_type_default_precision = {}


def set_integral_types_for_client_default(is_python_client: bool) -> None:
    """
    Set integral types based on client type when config is 'client_default'.
    """
    from snowflake.snowpark_connect.config import global_config

    config_key = "snowpark.connect.integralTypesEmulation"
    if global_config.get(config_key) != "client_default":
        return

    # if client mode matches, no action needed (no lock overhead)
    if _integral_types_conversion_enabled == (not is_python_client):
        return

    set_integral_types_conversion(not is_python_client)


def emulate_integral_types(t: DataType) -> DataType:
    """
    Map LongType based on precision attribute to appropriate integral types.

    Mappings:
    - _IntegralType with precision=19 -> LongType
    - _IntegralType with precision=10 -> IntegerType
    - _IntegralType with precision=5 -> ShortType
    - _IntegralType with precision=3 -> ByteType
    - _IntegralType with other precision -> DecimalType(precision, 0)

    This conversion is controlled by the 'snowpark.connect.integralTypesEmulation' config.
    When disabled, the function returns the input type unchanged.

    Args:
        t: The DataType to transform

    Returns:
        The transformed DataType with integral type conversions applied based on precision.
    """
    global _integral_types_conversion_enabled

    with _client_mode_lock:
        enabled = _integral_types_conversion_enabled

    if not enabled or getattr(t, "_is_already_mapped", False):
        return t

    if isinstance(t, _IntegralType):
        precision = getattr(t, "_precision", None)

        if precision is None:
            ret = t
        elif precision == 19:
            ret = LongType()
        elif precision == 10:
            ret = IntegerType()
        elif precision == 5:
            ret = ShortType()
        elif precision == 3:
            ret = ByteType()
        else:
            ret = DecimalType(precision, 0)

    elif isinstance(t, StructType):
        new_fields = [
            StructField(
                field.name,
                emulate_integral_types(field.datatype),
                field.nullable,
                _is_column=field._is_column,
            )
            for field in t.fields
        ]
        ret = StructType(new_fields, structured=t.structured)

    elif isinstance(t, ArrayType):
        ret = ArrayType(
            emulate_integral_types(t.element_type),
            contains_null=t.contains_null,
            structured=t.structured,
        )

    elif isinstance(t, MapType):
        ret = MapType(
            emulate_integral_types(t.key_type),
            emulate_integral_types(t.value_type),
            value_contains_null=t.value_contains_null,
            structured=t.structured,
        )
    else:
        ret = t

    ret._is_already_mapped = True
    return ret
