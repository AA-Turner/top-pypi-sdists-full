from typing import Any

from recap.converters.dbapi import DbapiConverter
from recap.types import (
    BoolType,
    BytesType,
    FloatType,
    IntType,
    RecapType,
    RecapTypeRegistry,
    StringType,
)

DEFAULT_NAMESPACE = "_root"
"""
Namespace to use when no namespace is specified in the schema.
"""


class MsSqlConverter(DbapiConverter):
    def __init__(
        self,
        namespace: str = DEFAULT_NAMESPACE,
    ):
        self.namespace = namespace
        self.registry = RecapTypeRegistry()

    def _parse_type(self, column_props: dict[str, Any]) -> RecapType:
        data_type = column_props["DATA_TYPE"].lower()
        octet_length = column_props["CHARACTER_OCTET_LENGTH"]
        precision = column_props["NUMERIC_PRECISION"]
        scale = column_props["NUMERIC_SCALE"]

        # https://learn.microsoft.com/en-us/sql/t-sql/data-types/data-types-transact-sql?view=sql-server-ver16
        if data_type == "bigint":
            base_type = IntType(bits=64, signed=True)
        elif data_type in ["int", "integer"]:
            base_type = IntType(bits=32, signed=True)
        elif data_type == "smallint":
            base_type = IntType(bits=16, signed=True)
        elif data_type == "tinyint":
            base_type = IntType(bits=8, signed=True)
        elif data_type == "float":
            base_type = FloatType(bits=64)
        elif data_type == "real" or (data_type == "float" and precision <= 24):
            base_type = FloatType(bits=32)
        elif data_type in [
            "text",
            "ntext",
            "json",
        ]:
            base_type = StringType(bytes_=octet_length, variable=True)
        elif data_type in [
            "varchar",
            "nvarchar",
        ]:
            bytes = (
                octet_length if octet_length != -1 else 2147483647
            )  # -1 is for nvarchar/varchar(max), which means max 2^31-1
            base_type = StringType(bytes_=bytes, variable=True)
        elif data_type in ["char", "nchar"]:
            base_type = StringType(bytes_=octet_length, variable=False)
        elif data_type in [
            "varbinary",
            "image",
        ]:
            base_type = BytesType(bytes_=2147483647, variable=True)
        elif data_type == "uniqueidentifier":
            base_type = StringType(
                logical="build.recap.UUID",
                bytes_=16,
                variable=False,
            )
        elif data_type in ["binary"]:
            base_type = BytesType(bytes_=octet_length, variable=False)
        elif data_type == "bit":
            base_type = BoolType()
        elif data_type in ["datetime", "datetime2", "timestamp"]:
            dt_precision = str(column_props["DATETIME_PRECISION"] or 5)
            unit = self._get_time_unit([dt_precision]) or "microsecond"
            if data_type == "datetime":
                bits = 64
            else:
                dt_precision = int(dt_precision)
                bits = 48 if dt_precision <= 2 else 56 if dt_precision <= 4 else 64
            base_type = IntType(
                bits=bits,
                logical="build.recap.Timestamp",
                unit=unit,
            )
        elif data_type in [
            "date",
        ]:
            dt_precision = column_props["DATETIME_PRECISION"]
            base_type = IntType(
                bits=24,
                logical="build.recap.Date",
                unit="day",
            )
        elif data_type in [
            "time",
        ]:
            dt_precision = column_props["DATETIME_PRECISION"]
            unit = self._get_time_unit([dt_precision]) or "microsecond"
            base_type = IntType(
                bits=40,
                logical="build.recap.Time",
                unit=unit,
            )
        elif data_type in ["decimal", "numeric"]:
            base_type = BytesType(
                logical="build.recap.Decimal",
                bytes_=(
                    5
                    if precision < 10
                    else 9 if precision < 20 else 13 if precision < 29 else 17
                ),
                variable=False,
                precision=precision,
                scale=scale,
            )
        else:
            raise ValueError(f"Unknown data type: {data_type}")

        return base_type
