#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

# This file contains a basic mapping from Spark to Snowflake formats.
# Not everything works - this aims to cover most cases, but we need to fall back to UDF or new native implementation
# for full coverage.
# Things that will work differently:
#
# Padding: Spark's unpadded day (d -> 9), hour (h -> 3), second (s -> 1) will be zero-padded in Snowflake (DD -> 09, HH12 -> 03, SS -> 01).
# Full Day Name (EEEE): Spark EEEE (Thursday) becomes abbreviated in Snowflake (DY -> Thu).
# Timezone Offset (Z): Spark Z (e.g., -0500) becomes colon-separated in Snowflake (TZH:TZM -> -05:00).
#
# Things that aren't supported at all:
#
# Day of Year (D): Spark D (313) has no listed Snowflake equivalent (e.g., DDD).
# Quarter (Q, qqqq, etc.): Spark's numeric quarter (Q -> 4) or textual quarter (qqqq -> 4th quarter) have no Snowflake format specifier.
# Hour 0-11 (K, KK): Spark K (3) or KK (03) have no listed Snowflake equivalent.
# Aligned Day of Week in Month (F): Spark F (2) has no listed Snowflake equivalent.
#
# Note that especially these missing specifiers could be a good addition to the existing format because
# they will not lead to conflict.

from pyspark.errors.exceptions.base import DateTimeException

from snowflake.snowpark.types import DataType, StringType
from snowflake.snowpark_connect.error.error_codes import ErrorCodes
from snowflake.snowpark_connect.error.error_utils import attach_custom_error_code


# TODO: There are more patterns where spark may throw an error.
class _UnsupportedSparkFormatPattern:
    def __init__(self, message: str) -> None:
        self.message = message
        return


spark_to_snowflake_datetime_mapping = {
    # Year
    "y": "YYYY",  # Year, potentially without padding for single digit in Spark, but YYYY is standard in Snowflake
    "yy": "YY",  # Two-digit year
    "yyy": "YYYY",  # Four-digit year because Snowflake has no 3 digit year
    "yyyy": "YYYY",  # Four-digit year
    "YYYY": "YYYY",
    # TODO Quarter
    "q": None,
    "Q": None,
    "qq": None,
    "QQ": None,
    "qqq": None,
    "QQQ": None,
    "qqqq": None,
    "QQQQ": None,
    # Month
    "M": "MM",  # Month number, potentially without padding in Spark for 1-9, but MM is zero-padded in Snowflake
    "MM": "MM",  # Zero-padded month number
    "MMM": "MON",  # Abbreviated month name
    "MMMM": "MMMM",  # Full month name
    # TODO Spark's 'L' (stand-alone month) doesn't have a direct equivalent in Snowflake's common formats. But
    # this only matters for some languages...
    "L": "MM",  # Closest to numeric month
    "LL": "MM",  # Closest to zero-padded numeric month
    "LLL": "MON",  # Closest to abbreviated textual month
    "LLLL": "MMMM",
    # Day
    "d": "DD",  # Day of month, potentially without padding in Spark for 1-9, but DD is zero-padded in Snowflake
    "dd": "DD",  # Zero-padded day of month
    "D": None,  # No day of year
    "F": None,  # Aligned day of week in month - No direct equivalent
    "E": "DY",  # Day of week (text) - Spark's short/full text maps to Snowflake's abbreviated DY. Full name (EEEE) has no direct common equivalent.
    "EE": "DY",  # Abbreviated day of week
    "EEE": "DY",  # Abbreviated day of week
    "EEEE": "DY",  # TODO there is no full day of week
    # Week-based patterns like 'e' are unsupported in Spark 3.0+ for date_format
    "e": _UnsupportedSparkFormatPattern(
        "Unsupported Spark pattern 'e': All week-based patterns are unsupported since Spark 3.0. Please use the SQL function EXTRACT instead."
    ),
    # Hour
    "H": "HH24",  # Hour of day (0-23)
    "HH": "HH24",  # Zero-padded hour of day (00-23)
    # TODO this is an opportunity for SQL fixing
    "k": "HH24",  # Clock-hour of day (1-24) - Mapped to HH24, need to be mindful of 1-24 vs 0-23
    "kk": "HH24",  # Zero-padded clock-hour of day (01-24) - Mapped to HH24
    "h": "HH12",  # Clock-hour of am-pm (1-12)
    "hh": "HH12",  # Zero-padded clock-hour of am-pm (01-12)
    "K": None,  # Hour of am-pm (0-11) - No direct equivalent in common Snowflake formats
    "KK": None,  # Zero-padded hour of am-pm (00-11) - No direct equivalent
    # Minute
    "m": "MI",  # Minute of hour
    "mm": "MI",  # Zero-padded minute of hour
    # Second
    "s": "SS",  # TODO Second of minute
    "ss": "SS",  # Zero-padded second of minute
    # Fraction of second
    "S": "FF1",  # Fraction of second (Spark's S* maps to Snowflake's FF*)
    "SS": "FF2",
    "SSS": "FF3",
    "SSSS": "FF4",
    "SSSSS": "FF5",
    "SSSSSS": "FF6",
    "SSSSSSS": "FF7",
    "SSSSSSSS": "FF8",
    "SSSSSSSSS": "FF9",
    # AM/PM
    "a": "AM",  # AM/PM marker
    # Time Zone
    # For patterns that output offset WITH colon (and potentially seconds, which Snowflake will ignore)
    "XXX": "TZH:TZM",  # Spark: +01:30 or Z
    "xxx": "TZH:TZM",  # Spark: +01:30 or +00:00
    "XXXXX": "TZH:TZM",  # Spark: +01:30:15 or Z (Snowflake loses seconds)
    "xxxxx": "TZH:TZM",  # Spark: +01:30:15 or +00:00:00 (Snowflake loses seconds)
    "ZZZZZ": "TZH:TZM",  # Spark: +01:30:15 or Z (Snowflake loses seconds)
    # For patterns that output offset WITHOUT colon (and potentially seconds, which Snowflake will ignore)
    "XX": "TZHTZM",  # Spark: +0130 or Z
    "xx": "TZHTZM",  # Spark: +0130 or +0000
    "Z": "TZHTZM",  # Spark: +0130 (covers Z, ZZ, ZZZ as they have same output format)
    "ZZ": "TZHTZM",  # Explicit for matching order
    "ZZZ": "TZHTZM",  # Explicit for matching order
    "XXXX": "TZHTZM",  # Spark: +013015 or Z (Snowflake loses seconds)
    "xxxx": "TZHTZM",  # Spark: +013015 or +000000 (Snowflake loses seconds)
    # For single X/x (variable Spark output: +01 or +0130; Z or +00)
    # Mapping these to a fixed Snowflake pattern will always be a compromise.
    # TZH:TZM is a reasonable default to ensure minute information is present if available.
    "X": "TZH:TZM",
    "x": "TZH:TZM",
    # For localized offset text
    "ZZZZ": None,  # Spark: GMT-08:00 -> No direct Snowflake equivalent from your list
    # Other Spark timezone patterns not in the user-provided Snowflake list
    "O": None,
    "OOOO": None,  # Localized zone offset text
    "VV": None,  # Zone ID. Bust be two Vs, not just one.
    "z": None,
    "zzzz": None,  # Zone name (textual)
}

# Pre-sort the keys by length in descending order, so that we match longer patterns first.
_sorted_spark_keys = sorted(
    spark_to_snowflake_datetime_mapping.keys(), key=len, reverse=True
)

snowflake_time_format_separator = set(list(" :/-.,0123456789"))

snowflake_datetime_format_elements = {
    # Era
    "G",  # Era designator (AD, BC)
    # Year
    "y",
    "yy",
    "yyy",
    "yyyy",  # Year
    "Y",  # Week year (for ISO weeks)
    "x",  # ISO week-based year
    "X",  # ISO time zone (e.g., +01, +0100, +01:00)
    # Quarter
    "Q",
    "QQ",  # Quarter (1–4)
    "q",
    "qq",  # Standalone quarter
    # Month
    "M",
    "MM",
    "MMM",
    "MMMM",  # Month numeric, abbreviated, full
    "L",
    "LL",
    "LLL",
    "LLLL",  # Standalone month
    "RM",  # Roman numeral month
    # Week
    "w",  # Week of year
    "W",  # Week of month
    "F",  # Day of week in month (e.g., 2nd Monday)
    # Day
    "d",
    "dd",  # Day of month
    "D",
    "DD",
    "DDD",  # Day of year
    "E",
    "EE",
    "EEE",
    "EEEE",
    "EEEEE",  # Day name
    "e",  # Local day of week (1–7)
    # Day Period
    "a",  # AM/PM
    # Hour
    "h",
    "hh",  # Hour in am/pm (1–12)
    "H",
    "HH",  # Hour in day (0–23)
    "K",
    "KK",  # Hour in am/pm (0–11)
    "k",
    "kk",  # Hour in day (1–24)
    "HH12",  # Snowflake 12-hour
    "HH24",  # Snowflake 24-hour
    # Minute
    "m",
    "mm",  # Minute
    "MI",  # Snowflake's minute
    # Second
    "s",
    "ss",  # Seconds
    "SS",  # Snowflake seconds
    # Fractional Seconds
    "S",
    "SSS",
    "SSSSSS",  # Milliseconds or microseconds
    "FF1",
    "FF2",
    "FF3",
    "FF4",
    "FF5",
    "FF6",
    "FF7",
    "FF8",
    "FF9",  # Snowflake fractional seconds
    # Timezone
    "z",  # Time zone abbreviation (e.g., PST)
    "Z",  # Time zone offset (e.g., +0800)
    "O",  # Time zone short localized format (e.g., GMT+8)
    "v",  # Time zone long format
    "TZH",
    "TZM",
    "TZD",  # Snowflake-specific: hour/minute offset and name
}


def convert_spark_format_to_snowflake(
    spark_format,
    timestamp_input_type: DataType | None = None,
):
    if spark_format in {"Y", "w", "W"}:
        exception = DateTimeException(
            f"Fail to recognize '{spark_format}' pattern in the DateTimeFormatter."
        )
        attach_custom_error_code(exception, ErrorCodes.INVALID_FUNCTION_ARGUMENT)
        raise exception
    snowflake_format = ""
    i = 0
    n = len(spark_format)

    while i < n:
        char = spark_format[i]

        if char == "'":
            # Check if this is the specific Spark "''" sequence (literal apostrophe)
            if spark_format[i : i + 2] == "''":
                # It's the '' sequence, which means a single literal apostrophe.
                # For Snowflake, this is represented as "'".
                snowflake_format += (
                    '"\'"'  # Append the Snowflake literal for a single quote
                )
                i += 2  # Consume both ' characters
                continue
            else:
                # It's the start of a general quoted literal block 'text...'
                i += 1  # Consume the opening "'"
                literal_content = ""
                # Loop to extract the content of the Spark literal block
                while i < n:
                    current_literal_char = spark_format[i]
                    if current_literal_char == "'":
                        # Encountered a quote; is it an escaped '' or the closing quote?
                        if spark_format[i : i + 2] == "''":
                            # It's an escaped '' sequence inside the literal.
                            literal_content += "'"  # Add a single ' to the content
                            i += 2  # Consume both ' characters of this ''
                        else:
                            # It's a single ', which is the closing quote for this literal block.
                            i += 1  # Consume the closing "'"
                            break  # Exit literal content extraction
                    else:
                        # It's a regular character within the literal.
                        literal_content += current_literal_char
                        i += 1  # Move to the next character in the literal

                # For Snowflake, literals must be in double quotes.
                # Any actual double quote characters within literal_content also need to be escaped (by doubling).
                snowflake_safe_literal = literal_content.replace('"', '""')
                snowflake_format += f'"{snowflake_safe_literal}"'
                continue

        elif char == "[":
            # Optional section in Spark. Spark's date_format typically ignores the brackets for formatting.
            # Find the matching ']' and effectively skip the section for conversion.
            next_bracket_close = spark_format.find("]", i + 1)
            if next_bracket_close != -1:
                i = next_bracket_close + 1  # Skip content and brackets
            else:
                # Unclosed bracket. Treat '[' as a literal character for Snowflake.
                snowflake_format += f'"{char}"'  # Quote the '['
                i += 1
            continue
        elif char == "]":
            # Standalone ']' (not consumed by '[' logic). Treat as a literal for Snowflake.
            snowflake_format += f'"{char}"'
            i += 1
            continue
        else:  # Handles non-literal-delimiter characters: patterns or passthrough literals
            match char:
                case "a":
                    # Spark's 'a' would be at most 1 times
                    is_valid_a_pattern = spark_format[i : i + 2] != char * 2
                    if not is_valid_a_pattern:
                        exception = DateTimeException(
                            f"Fail to recognize '{spark_format}' pattern in the DateTimeFormatter"
                        )
                        attach_custom_error_code(
                            exception, ErrorCodes.INVALID_FUNCTION_ARGUMENT
                        )
                        raise exception
                case "h" | "K" | "k" | "H" | "m" | "s" | "d":
                    # Spark's characters would be at most 2 times
                    is_valid_2_patterns = spark_format[i : i + 3] != char * 3
                    if not is_valid_2_patterns:
                        exception = DateTimeException(
                            f"Fail to recognize '{spark_format}' pattern in the DateTimeFormatter"
                        )
                        attach_custom_error_code(
                            exception, ErrorCodes.INVALID_FUNCTION_ARGUMENT
                        )
                        raise exception
                case "D":
                    # Spark's 'D'' would be at most 3 times
                    is_valid_D_patterns = spark_format[i : i + 4] != char * 4
                    if not is_valid_D_patterns:
                        exception = DateTimeException(
                            f"Fail to recognize '{spark_format}' pattern in the DateTimeFormatter"
                        )
                        attach_custom_error_code(
                            exception, ErrorCodes.INVALID_FUNCTION_ARGUMENT
                        )
                        raise exception
                case "V":
                    # Spark's 'V' for Zone ID requires 'VV'. A single 'V' is invalid.
                    is_valid_vv_pattern = spark_format[i : i + 2] == "VV"
                    if not is_valid_vv_pattern:
                        exception = DateTimeException(
                            "Pattern letter count must be 2: V"
                        )
                        attach_custom_error_code(
                            exception, ErrorCodes.INVALID_FUNCTION_ARGUMENT
                        )
                        raise exception
                case "O":
                    # Spark's 'O' would be either 1 or 4.
                    is_valid_o_or_oooo_pattern = spark_format[i : i + 2] != "OO" or (
                        spark_format[i : i + 4] == "OOOO"
                        and spark_format[i : i + 5] != "OOOOO"
                    )
                    if not is_valid_o_or_oooo_pattern:
                        exception = DateTimeException(
                            "Pattern letter count must be 1 or 4: O"
                        )
                        attach_custom_error_code(
                            exception, ErrorCodes.INVALID_FUNCTION_ARGUMENT
                        )
                        raise exception
                case "q" | "Q" | "z" | "E":
                    # Spark's characters would be at most 4 times
                    is_valid_4_patterns = spark_format[i : i + 5] != char * 5
                    if not is_valid_4_patterns:
                        exception = DateTimeException(
                            f"Too many pattern letters: {char}"
                        )
                        attach_custom_error_code(
                            exception, ErrorCodes.INVALID_FUNCTION_ARGUMENT
                        )
                        raise exception
                case "x" | "X" | "Z":
                    # Spark's 'x' or 'X' or 'z' or 'Z' would be at most 5 times
                    is_valid_xz_pattern = spark_format[i : i + 6] != char * 6
                    if not is_valid_xz_pattern:
                        exception = DateTimeException(
                            f"Too many pattern letters: {char}"
                        )
                        attach_custom_error_code(
                            exception, ErrorCodes.INVALID_FUNCTION_ARGUMENT
                        )
                        raise exception
                case "y":
                    # Spark's 'y' would be at most 6 times
                    is_valid_y_pattern = spark_format[i : i + 7] != char * 7
                    if not is_valid_y_pattern:
                        exception = DateTimeException(
                            f"Fail to recognize '{spark_format}' pattern in the DateTimeFormatter"
                        )
                        attach_custom_error_code(
                            exception, ErrorCodes.INVALID_FUNCTION_ARGUMENT
                        )
                        raise exception
                case "C" | "I":
                    exception = DateTimeException(f"Unknown pattern letter: {char}")
                    attach_custom_error_code(
                        exception, ErrorCodes.INVALID_FUNCTION_ARGUMENT
                    )
                    raise exception

            if (
                spark_format[i : i + 5] in {"M" * 5, "L" * 5}
                or (
                    spark_format[i : i + 2] == "FF"
                    and spark_format[i : i + 3]
                    not in snowflake_datetime_format_elements
                )
                or spark_format[i : i + 4] == "DDDD"
                or spark_format[i : i + 3] in {"kkk", "KKK"}
                or spark_format[i : i + 10] == "SSSSSSSSSS"
            ):
                exception = DateTimeException(
                    f"Fail to recognize '{spark_format}' pattern in the DateTimeFormatter."
                )
                attach_custom_error_code(
                    exception, ErrorCodes.INVALID_FUNCTION_ARGUMENT
                )
                raise exception

            matched_pattern = False

            # We go through the pre-sorted keys to handle longer patterns first.
            for spark_key in _sorted_spark_keys:
                if spark_format[i:].startswith(spark_key):
                    snowflake_equivalent = spark_to_snowflake_datetime_mapping[
                        spark_key
                    ]
                    if isinstance(snowflake_equivalent, _UnsupportedSparkFormatPattern):
                        exception = DateTimeException(snowflake_equivalent.message)
                        attach_custom_error_code(
                            exception, ErrorCodes.UNSUPPORTED_OPERATION
                        )
                        raise exception
                    if snowflake_equivalent is not None:
                        snowflake_format += snowflake_equivalent
                    i += len(spark_key)
                    matched_pattern = True
                    break

            if not matched_pattern:
                # No multi-character Spark pattern matched. Treat this single 'char' as a literal.
                # Quote it for Snowflake to prevent misinterpretation.
                if (
                    isinstance(timestamp_input_type, StringType)
                    and char not in snowflake_time_format_separator
                ):
                    exception = DateTimeException(f"Illegal pattern character: {char}")
                    attach_custom_error_code(
                        exception, ErrorCodes.INVALID_FUNCTION_ARGUMENT
                    )
                    raise exception

                snowflake_format += f'"{char}"'
                i += 1

            continue

    return snowflake_format
