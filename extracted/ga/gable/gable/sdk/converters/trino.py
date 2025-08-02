from typing import Any, Tuple, Union

from gable.sdk.models import TrinoDataType
from gable.sdk.schema import (
    AliasContractField,
    BoolContractField,
    BytesContractField,
    ContractField,
    IntContractField,
    ListContractField,
    LogicalEnumNumeric,
    LogicalEnumTemporal,
    LogicalEnumText,
    MapContractField,
    SchemaType,
    StringContractField,
    Unit,
    UnknownContractField,
)

DEFAULT_TIMESTAMP_PRECISION = 3
# https://github.com/trinodb/trino/wiki/Variable-precision-datetime-types
TRINO_TIMESTAMP_PRECISION_BITS_MAP = {
    0: 39,
    1: 42,
    2: 45,
    3: 49,
    4: 52,
    5: 55,
    6: 59,
    7: 62,
    8: 65,
    9: 69,
    10: 72,
    11: 75,
    12: 79,
}

TRINO_TIMESTAMP_UNIT_MAP = {
    0: Unit.second,
    1: Unit.second,
    2: Unit.second,
    3: Unit.millisecond,
    4: Unit.millisecond,
    5: Unit.millisecond,
    6: Unit.microsecond,
    7: Unit.microsecond,
    8: Unit.microsecond,
    9: Unit.nanosecond,
    10: Unit.nanosecond,
    11: Unit.nanosecond,
    12: Unit.picosecond,
}


def get_bits_for_timestamp_precision(precision: int) -> int:
    if precision not in TRINO_TIMESTAMP_PRECISION_BITS_MAP:
        raise ValueError(f"Invalid precision for time/timestamp: {precision}")
    return TRINO_TIMESTAMP_PRECISION_BITS_MAP[precision]


def get_unit_for_timestamp_precision(precision: int) -> Unit:
    if precision not in TRINO_TIMESTAMP_UNIT_MAP:
        raise ValueError(f"Invalid precision for time/timestamp: {precision}")
    return TRINO_TIMESTAMP_UNIT_MAP[precision]


def convert_trino_timestamp_to_spark_timestamp(
    time_or_timestamp: ContractField,
) -> ContractField:
    """Converts a Trino timestamp type to a Spark timestamp type by setting bits to 64 and unit to microsecond.
    If the input is not a timestamp type, it is returned as is."""
    if (
        time_or_timestamp.__root__.type != "int"
        or time_or_timestamp.__root__.logical
        not in [LogicalEnumTemporal.Time, LogicalEnumTemporal.Timestamp]
    ):
        return time_or_timestamp
    time_or_timestamp.__root__.bits = 64
    time_or_timestamp.__root__.unit = Unit.millisecond
    return time_or_timestamp


def trino_to_gable_type(
    field_name: str,
    trinoType: Union[str, TrinoDataType, Tuple[TrinoDataType, Tuple[Any, ...]]],
) -> ContractField:
    if isinstance(trinoType, str):
        trinoType = TrinoDataType.parse(trinoType)

    if isinstance(trinoType, Tuple):
        trinoType, args = trinoType
    else:
        args = ()

    if trinoType == TrinoDataType.VARCHAR:
        # If length is not provided, don't set it so it's ignored when doing the contract comparison
        length = args[0] if args else None
        return ContractField(
            __root__=StringContractField(
                type="string", name=field_name, bytes=length, variable=True
            )
        )
    elif trinoType == TrinoDataType.CHAR:
        length = args[0] if args else 1
        return ContractField(
            __root__=StringContractField(
                type="string", name=field_name, bytes=length, variable=False
            )
        )
    elif trinoType == TrinoDataType.BIGINT:
        return ContractField(__root__=AliasContractField(type="int64", name=field_name))
    elif trinoType in (TrinoDataType.INTEGER, TrinoDataType.INT):
        return ContractField(__root__=AliasContractField(type="int32", name=field_name))
    elif trinoType == TrinoDataType.SMALLINT:
        return ContractField(__root__=AliasContractField(type="int16", name=field_name))
    elif trinoType == TrinoDataType.TINYINT:
        return ContractField(__root__=AliasContractField(type="int8", name=field_name))
    elif trinoType == TrinoDataType.REAL:
        return ContractField(
            __root__=AliasContractField(type="float32", name=field_name)
        )
    elif trinoType == TrinoDataType.DOUBLE:
        return ContractField(
            __root__=AliasContractField(type="float64", name=field_name)
        )
    elif trinoType == TrinoDataType.DECIMAL:
        if not args:
            raise ValueError("Precision must be provided for DECIMAL type")
        precision = args[0]
        scale = args[1] if len(args) > 1 else 0
        return ContractField(
            __root__=BytesContractField(
                type="bytes",
                name=field_name,
                bytes=17,
                logical=LogicalEnumNumeric.Decimal,
                precision=precision,
                scale=scale,
            )
        )
    elif trinoType == TrinoDataType.VARBINARY:
        return ContractField(
            __root__=BytesContractField(
                type="bytes", bytes=2147483647, name=field_name, variable=True
            )
        )
    elif trinoType == TrinoDataType.JSON:
        return ContractField(
            __root__=StringContractField(
                type="string",
                name=field_name,
            )
        )
    elif trinoType == TrinoDataType.UUID:
        return ContractField(
            __root__=StringContractField(
                type="string", name=field_name, bytes=36, logical=LogicalEnumText.UUID
            )
        )
    elif trinoType == TrinoDataType.BOOLEAN:
        return ContractField(__root__=BoolContractField(type="bool", name=field_name))
    elif trinoType == TrinoDataType.DATE:
        return ContractField(
            __root__=IntContractField(
                type="int",
                bits=32,
                unit=Unit.day,
                name=field_name,
                logical=LogicalEnumTemporal.Date,
            )
        )
    elif trinoType == TrinoDataType.TIME:
        precision = args[0] if len(args) == 1 else DEFAULT_TIMESTAMP_PRECISION
        return ContractField(
            __root__=IntContractField(
                type="int",
                name=field_name,
                logical=LogicalEnumTemporal.Time,
                bits=get_bits_for_timestamp_precision(precision),
                unit=get_unit_for_timestamp_precision(precision),
            )
        )
    elif trinoType == TrinoDataType.TIME_WITH_TIME_ZONE:
        precision = args[0] if len(args) == 1 else DEFAULT_TIMESTAMP_PRECISION
        return ContractField(
            __root__=IntContractField(
                type="int",
                name=field_name,
                logical=LogicalEnumTemporal.Time,
                timezone="UTC",
                bits=get_bits_for_timestamp_precision(precision),
                unit=get_unit_for_timestamp_precision(precision),
            )
        )
    elif trinoType == TrinoDataType.TIMESTAMP:
        precision = args[0] if len(args) == 1 else 3
        return ContractField(
            __root__=IntContractField(
                type="int",
                name=field_name,
                logical=LogicalEnumTemporal.Timestamp,
                bits=get_bits_for_timestamp_precision(precision),
                unit=get_unit_for_timestamp_precision(precision),
            )
        )
    elif trinoType == TrinoDataType.TIMESTAMP_WITH_TIME_ZONE:
        precision = args[0] if len(args) == 1 else 3
        return ContractField(
            __root__=IntContractField(
                type="int",
                name=field_name,
                logical=LogicalEnumTemporal.Timestamp,
                timezone="UTC",
                bits=get_bits_for_timestamp_precision(precision),
                unit=get_unit_for_timestamp_precision(precision),
            )
        )
    elif trinoType == TrinoDataType.INTERVAL_YEAR_TO_MONTH:
        return ContractField(
            __root__=BytesContractField(
                type="bytes",
                name=field_name,
                logical=LogicalEnumNumeric.Interval,
                bytes=16,
            )
        )
    elif trinoType == TrinoDataType.INTERVAL_DAY_TO_SECOND:
        return ContractField(
            __root__=BytesContractField(
                type="bytes",
                name=field_name,
                logical=LogicalEnumNumeric.Interval,
                bytes=16,
            )
        )
    elif trinoType in (TrinoDataType.ARRAY, TrinoDataType.ROW):
        if len(args) == 1:
            array_trino_type = trino_to_gable_type("ignored", args[0]).__root__
            array_trino_type.name = None
        else:
            array_trino_type = UnknownContractField(
                type="unknown",
            )
        return ContractField(
            __root__=ListContractField(
                type="list",
                name=field_name,
                values=SchemaType(__root__=array_trino_type),
            )
        )
    elif trinoType == TrinoDataType.MAP:
        return ContractField(
            __root__=MapContractField(
                type="map",
                name=field_name,
                keys=SchemaType(
                    __root__=UnknownContractField(
                        type="unknown",
                    )
                ),
                values=SchemaType(
                    __root__=UnknownContractField(
                        type="unknown",
                    )
                ),
            )
        )
    elif trinoType == TrinoDataType.IPADDRESS:
        return ContractField(
            __root__=StringContractField(type="string", name=field_name, bytes=16)
        )
    else:
        print(f"{field_name} has unknown type: {trinoType}")
        return ContractField(
            __root__=UnknownContractField(
                type="unknown",
                name=field_name,
            )
        )
