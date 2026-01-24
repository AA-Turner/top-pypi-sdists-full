#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

import datetime
import decimal
from zoneinfo import ZoneInfo

import pyspark.sql.connect.proto.expressions_pb2 as expressions_proto
from tzlocal import get_localzone

from snowflake.snowpark_connect.config import global_config
from snowflake.snowpark_connect.error.error_codes import ErrorCodes
from snowflake.snowpark_connect.error.error_utils import attach_custom_error_code
from snowflake.snowpark_connect.utils.telemetry import (
    SnowparkConnectNotImplementedError,
)


def get_literal_field_and_name(literal: expressions_proto.Expression.Literal):
    match literal.WhichOneof("literal_type"):
        case "byte":
            return literal.byte, str(literal.byte)
        case "short":
            return literal.short, str(literal.short)
        case "integer":
            return literal.integer, str(literal.integer)
        case "long":
            return literal.long, str(literal.long)
        case "float":
            return (
                literal.float,
                str(literal.float) if literal.float == literal.float else "NaN",
            )
        case "double":
            return (
                literal.double,
                str(literal.double) if literal.double == literal.double else "NaN",
            )
        case "string":
            return literal.string, str(literal.string)
        case "boolean":
            return literal.boolean, str(literal.boolean)
        case "date":
            # Both snowflake and spark Date type don't consider time zones.
            # Don't use datetime.date.fromtimestamp, which depends on local timezone
            date = datetime.datetime.fromtimestamp(
                literal.date * 86400, tz=datetime.timezone.utc
            ).date()
            return date, f"DATE '{date}'"
        case "timestamp" | "timestamp_ntz" as t:
            local_tz = get_localzone()
            if t == "timestamp":
                microseconds = literal.timestamp
            else:
                microseconds = literal.timestamp_ntz

            dt_utc = datetime.datetime.fromtimestamp(
                microseconds // 1_000_000, tz=datetime.timezone.utc
            ) + datetime.timedelta(microseconds=microseconds % 1_000_000)

            if t == "timestamp_ntz":
                # For timestamp_ntz, display in UTC
                lit_dt = dt_utc.replace(tzinfo=None)
                tz_dt = dt_utc
            else:
                # For timestamp_ltz, always display in session timezone
                config_tz = global_config.spark_sql_session_timeZone
                display_tz = ZoneInfo(config_tz) if config_tz else local_tz
                tz_dt = dt_utc.astimezone(display_tz)
                lit_dt = tz_dt.replace(tzinfo=None)

            def _format_timestamp(dt) -> str:
                without_micros = f"{dt.year:04d}-{dt.month:02d}-{dt.day:02d} {dt.hour:02d}:{dt.minute:02d}:{dt.second:02d}"
                if dt.microsecond == 0:
                    return without_micros
                else:
                    base_format = f"{without_micros}.{dt.microsecond:06d}"
                    return base_format.rstrip("0").rstrip(".")

            return lit_dt, f"{t.upper()} '{_format_timestamp(tz_dt)}'"
        case "day_time_interval":
            # TODO(SNOW-1920942): Snowflake SQL is missing an "interval" type.
            timedelta = datetime.timedelta(
                seconds=literal.day_time_interval / 1_000_000
            )
            interval_seconds = f"{(literal.day_time_interval / 1_000_000):.6f}".rstrip(
                "0"
            ).rstrip(".")
            str_value = f"INTERVAL '{interval_seconds}' SECOND"
            return timedelta, str_value
        case "binary":
            return literal.binary, str(literal.binary)
        case "decimal":
            # literal.decimal.precision & scale are ignored, as decimal.Decimal doesn't accept them
            return decimal.Decimal(literal.decimal.value), literal.decimal.value
        case "array":
            array_values, element_names = zip(
                *(get_literal_field_and_name(e) for e in literal.array.elements)
            )
            return array_values, f"ARRAY({', '.join(element_names)})"
        case "struct":
            struct_key_names = [
                field.name for field in literal.struct.struct_type.struct.fields
            ]
            struct_values = [
                get_literal_field_and_name(el)[0] for el in literal.struct.elements
            ]

            struct_dict = dict(zip(struct_key_names, struct_values))

            struct_elements = [
                item for pair in zip(struct_key_names, struct_values) for item in pair
            ]

            return (
                struct_dict,
                f"OBJECT_CONSTRUCT_KEEP_NULL({', '.join(str(x) for x in struct_elements)})",
            )
        case "null" | None:
            return None, "NULL"
        case other:
            exception = SnowparkConnectNotImplementedError(
                f"Other Literal Type {other}"
            )
            attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
            raise exception
