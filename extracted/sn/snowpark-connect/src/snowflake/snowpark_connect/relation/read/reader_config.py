#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

from dataclasses import dataclass
from typing import Any

from snowflake.snowpark_connect.config import global_config, str_to_bool
from snowflake.snowpark_connect.date_time_format_mapping import (
    convert_java_datetime_format_for_fileformat,
)
from snowflake.snowpark_connect.utils.snowpark_connect_logging import logger


@dataclass
class _Config:
    default_config: dict[str, str]
    supported_options: set[str]
    boolean_config_list: list[str]
    int_config_list: list[str]
    float_config_list: list[str]


# TODO: There is a issue where we don't differentiate between our defaults, and what user has explicitly provided.
# For explicit options that are provided, a visible warning will be better.
class ReaderWriterConfig:

    # Default global configuration for Snowpark Connect.
    # All keys must be lowercase in order to preserve case configuration insensitivity.
    # This mimics how the Spark works.
    default_global_config = {
        # TODO: Snowpark does not support mode argument
        # "mode": "PERMISSIVE",
        # TODO: Snowpark does not support locale argument
        # "locale": "en-US",
        "compression": "auto",
    }

    def __init__(self, config: _Config, options: dict[str, str]) -> None:
        self.config = lowercase_dict_keys(
            self.default_global_config
        ) | lowercase_dict_keys(config.default_config)
        self.supported_options = {option.lower() for option in config.supported_options}
        self.boolean_config_list = [
            option.lower() for option in config.boolean_config_list
        ]
        self.int_config_list = [option.lower() for option in config.int_config_list]
        self.float_config_list = [option.lower() for option in config.float_config_list]

        for key, value in options.items():
            self.config[key.lower()] = value

    def _get_config_setting(self, key: str) -> bool | int | float | str | None:
        """Get the configuration setting for the key based on the setting type."""
        if key in self.boolean_config_list:
            return str_to_bool(self.config[key])
        elif key in self.int_config_list:
            return int(self.config[key])
        elif key in self.float_config_list:
            return float(self.config[key])
        else:
            return self.config[key]

    # TODO: When we convert into args, we cannot only convert the key, we need to adjust the value also.
    # For example, for differences in timestamp format.
    def convert_to_snowpark_args(self) -> dict[str, Any]:
        snowpark_config = {}

        for key, value in self.config.items():
            if key in self.supported_options:
                snowpark_config[key] = value
            else:
                logger.warning(
                    f"Reader option '{key}' is not supported and will be ignored. Results may differ from Spark."
                )

        for key in snowpark_config.keys():
            snowpark_config[key] = self._get_config_setting(key)
        return snowpark_config

    def get(self, key: str) -> str | None:
        return self.config.get(key.lower(), None)


def lowercase_dict_keys(d: dict[str, Any]) -> dict[str, Any]:
    """Convert all keys in the dictionary to lowercase."""
    return {key.lower(): value for key, value in d.items()}


def lowercase_set(s: set[str]) -> set[str]:
    return {value.lower() for value in s}


# Config has to be lowercased, because it is publicly available
CSV_READ_SUPPORTED_OPTIONS = lowercase_set(
    {
        "schema",
        "sep",
        "delimiter",  # Spark alias for sep
        "encoding",
        "charset",  # Spark alias for encoding
        "quote",
        # escape has different semantics in snowpark, but should work for standard use-cases
        "escape",
        # "comment", # Comment is not supported
        "header",
        "inferSchema",
        "ignoreLeadingWhiteSpace",
        "ignoreTrailingWhiteSpace",
        "nullValue",
        # "nanValue",
        # "positiveInf",
        # "negativeInf",
        "dateFormat",
        "timestampFormat",
        # "maxColumns",
        # "maxCharsPerColumn",
        # "maxMalformedLogPerPartition",
        # "mode",
        # "columnNameOfCorruptRecord",
        "multiLine",
        # "charToEscapeQuoteEscaping",
        # "samplingRatio",
        # "enforceSchema",
        # "emptyValue",
        # "locale",
        "lineSep",
        "pathGlobFilter",
        # "recursiveFileLookup",
        # "modifiedBefore",
        # "modifiedAfter",
        # "unescapedQuoteHandling",
        "compression",
        # "escapeQuotes",
        # "quoteAll",
        "rowsToInferSchema",  # Snowflake specific option, number of rows to infer schema
        "relaxTypesToInferSchema",  # Snowflake specific option, whether to relax types to infer schema
    }
)

# Config has to be lowercased, because it is publicly available
CSV_READ_DEFAULT_CONFIG = lowercase_dict_keys(
    {
        "header": "false",
        "inferSchema": "true",
        # TODO: This default is ok for reads, but it should be removed for writes because it will lead to
        # quoting even when it is not necessary.
        "quote": '"',
        "comment": "#",
        # TODO nullValue of "" is correct for Spark, Snowflake's default is \N.
        # However, Snowflake will refuse to write when nullValue is empty and fields aren't
        # optionally enclosed. Hence, we are not changing the default nullValue.
        # We need to look more to see if this is a good default for both write+read, or if we need to adjust.
        # "nullValue": "",
        # TODO: Snowpark does not support NaN value argument.
        # "nanValue": "NaN",
        "dateFormat": "yyyy-MM-dd",
        "timestampFormat": "yyyy-MM-dd HH:mm:ss.SSSSSS",
        # TODO: Snowpark does not support maxColumns argument
        # "maxColumns": "20480",
        # TODO: Snowpark does not support maxCharsPerColumn argument
        # "maxCharsPerColumn": "1000000",
        # TODO: Snowpark does not support maxMalformedLogPerPartition argument
        # "maxMalformedLogPerPartition": "10",
        "charset": "UTF-8",
        # TODO: Snowpark does not support multiLine argument
        "multiLine": "false",
        "ignoreLeadingWhiteSpace": "false",
        "ignoreTrailingWhiteSpace": "false",
        # TODO: Snowpark does not support samplingRatio argument
        # "samplingRatio": "1.0",
        # TODO: Snowpark does not support emptyValue argument
        # "emptyValue": "",
        "lineSep": "\n",
        "sep": ",",
        # TODO: Snowpark does not support escapeQuotes argument
        # "escapeQuotes": "true",
        # TODO: Snowpark does not support quoteAll argument
        # "quoteAll": "false",
        "escape": "\\\\",
    }
)


def apply_infer_schema_options(snowpark_config: dict[str, Any]) -> None:
    """Pop rowsToInferSchema and relaxTypesToInferSchema from config.

    If rowsToInferSchema is present and > 0, sets INFER_SCHEMA_OPTIONS
    with MAX_RECORDS_PER_FILE and USE_RELAXED_TYPES.

    Shared by CSV and JSON readers.
    """
    if "rowstoinferschema" not in snowpark_config:
        return

    rows_to_infer_schema = int(snowpark_config.pop("rowstoinferschema"))

    relax_types_to_infer_schema = True
    if "relaxtypestoinferschema" in snowpark_config:
        relax_types_to_infer_schema = str_to_bool(
            str(snowpark_config.pop("relaxtypestoinferschema"))
        )

    if rows_to_infer_schema > 0:
        snowpark_config["INFER_SCHEMA_OPTIONS"] = {
            "MAX_RECORDS_PER_FILE": rows_to_infer_schema,
            "USE_RELAXED_TYPES": relax_types_to_infer_schema,
        }


def csv_convert_to_snowpark_args(snowpark_config: dict[str, Any]) -> dict[str, Any]:
    renamed_args = {
        "inferSchema": "INFER_SCHEMA",
        # TODO: quote in Spark and FIELD_OPTIONALLY_ENCLOSED_BY in Snowflake are not actually the same.
        "quote": "FIELD_OPTIONALLY_ENCLOSED_BY",
        "nullValue": "NULL_IF",
        "dateFormat": "DATE_FORMAT",
        "timestampFormat": "TIMESTAMP_FORMAT",
        "lineSep": "RECORD_DELIMITER",
        "sep": "FIELD_DELIMITER",
        "header": "PARSE_HEADER",
        "pathGlobFilter": "PATTERN",
        "multiLine": "MULTI_LINE",
        "encoding": "ENCODING",
    }
    renamed_args = lowercase_dict_keys(renamed_args)

    # Handle 'delimiter' as Spark alias for 'sep'.
    # delimiter always overrides sep (including the default sep=",") because
    # when a user explicitly passes delimiter, that is the value they want.
    if "delimiter" in snowpark_config:
        snowpark_config["sep"] = snowpark_config["delimiter"]
        del snowpark_config["delimiter"]

    # Handle 'charset' as Spark alias for 'encoding'
    if "charset" in snowpark_config:
        if "encoding" not in snowpark_config:
            snowpark_config["encoding"] = snowpark_config["charset"]
        del snowpark_config["charset"]

    # Empty quote means no quoting — remove so Snowflake uses its default (NONE)
    if "quote" in snowpark_config and snowpark_config["quote"] == "":
        del snowpark_config["quote"]

    # spark does not escape unenclosed fields
    snowpark_config["ESCAPE_UNENCLOSED_FIELD"] = "NONE"
    snowpark_config["ERROR_ON_COLUMN_COUNT_MISMATCH"] = False
    # snowpark_config["EMPTY_FIELD_AS_NULL"] = True

    # Fix the escape character if it is provided.
    # TODO SNOW-2081726: This seems to be a Snowpark bug
    if snowpark_config.get("escape") and snowpark_config["escape"] == "\\":
        snowpark_config["escape"] = "\\\\"

    # If quote and escape are the same character, drop the escape.
    # Snowflake already handles escaping of FIELD_OPTIONALLY_ENCLOSED_BY by
    # doubling the character (e.g. "" inside a "-enclosed field), so setting
    # ESCAPE to the same value is redundant and causes a SQL compilation error.
    quote_char = snowpark_config.get("quote")
    escape_char = snowpark_config.get("escape")
    if quote_char and escape_char and quote_char == escape_char:
        del snowpark_config["escape"]

    # Map Spark's ignoreLeadingWhiteSpace / ignoreTrailingWhiteSpace to
    # Snowflake's TRIM_SPACE. Snowflake cannot trim only one side, so either
    # option being true enables TRIM_SPACE (D1 compatibility difference).
    ignore_leading = snowpark_config.pop("ignoreleadingwhitespace", False)
    ignore_trailing = snowpark_config.pop("ignoretrailingwhitespace", False)
    if ignore_leading or ignore_trailing:
        snowpark_config["TRIM_SPACE"] = True

    apply_infer_schema_options(snowpark_config)

    # Convert Java/Spark date and timestamp format strings to Snowflake equivalents.
    # Spark uses Java SimpleDateFormat patterns (e.g. dd/MM/yyyy HH:mm) while
    # Snowflake uses its own tokens (DD/MM/YYYY HH24:MI).
    for fmt_key in ("dateformat", "timestampformat"):
        if fmt_key in snowpark_config and snowpark_config[fmt_key]:
            try:
                snowpark_config[fmt_key] = convert_java_datetime_format_for_fileformat(
                    snowpark_config[fmt_key]
                )
            except Exception:
                pass

    # Rename the keys to match the Snowpark configuration.
    for spark_arg, snowpark_arg in renamed_args.items():
        if spark_arg not in snowpark_config:
            continue
        snowpark_config[snowpark_arg] = snowpark_config[spark_arg]
        del snowpark_config[spark_arg]

    return snowpark_config


class CsvReaderConfig(ReaderWriterConfig):
    # spark reader options that snowpark is able to handle.
    # Spark options are here: https://spark.apache.org/docs/latest/sql-data-sources-csv.html
    # Snowpark options are here: https://docs.snowflake.com/en/sql-reference/sql/create-file-format
    def __init__(self, options: dict[str, str]) -> None:
        super().__init__(
            _Config(
                default_config=CSV_READ_DEFAULT_CONFIG,
                supported_options=CSV_READ_SUPPORTED_OPTIONS,
                boolean_config_list=[
                    "header",
                    "inferSchema",
                    "multiLine",
                    "ignoreLeadingWhiteSpace",
                    "ignoreTrailingWhiteSpace",
                    "escapeQuotes",
                    "quoteAll",
                ],
                int_config_list=[
                    "maxColumns",
                    "maxCharsPerColumn",
                    "maxMalformedLogPerPartition",
                ],
                float_config_list=["samplingRatio"],
            ),
            options,
        )

    def convert_to_snowpark_args(self) -> dict[str, Any]:
        snowpark_config = super().convert_to_snowpark_args()
        return csv_convert_to_snowpark_args(snowpark_config)


# TODO: This is just a first pass, we need to differentiate more clearly between read and write configs.
class CsvWriterConfig(ReaderWriterConfig):
    # spark reader options that snowpark is able to handle.
    # Spark options are here: https://spark.apache.org/docs/latest/sql-data-sources-csv.html
    # Snowpark options are here: https://docs.snowflake.com/en/sql-reference/sql/create-file-format

    def __init__(self, options: dict[str, str]) -> None:
        super().__init__(
            _Config(
                default_config=dict(
                    {
                        key: value
                        for key, value in CSV_READ_DEFAULT_CONFIG.items()
                        # Quote is removed here because it behaves very differently in Snowpark compared to Spark.
                        if key
                        not in [
                            "quote",
                            "inferSchema",
                            "compression",
                            "rowstoinferschema",
                        ]
                    },
                    **(
                        {
                            "compression": "none"  # When writing files compression should be provided by the user
                        }
                    ),
                ),
                supported_options=CSV_READ_SUPPORTED_OPTIONS - {"inferSchema"},
                boolean_config_list=[
                    "header",
                    "multiLine",
                    "ignoreLeadingWhiteSpace",
                    "ignoreTrailingWhiteSpace",
                    "escapeQuotes",
                    "quoteAll",
                ],
                int_config_list=[
                    "maxColumns",
                    "maxCharsPerColumn",
                    "maxMalformedLogPerPartition",
                ],
                float_config_list=["samplingRatio"],
            ),
            options,
        )

    def convert_to_snowpark_args(self) -> dict[str, Any]:
        snowpark_config = super().convert_to_snowpark_args()
        return csv_convert_to_snowpark_args(snowpark_config)


class JsonReaderConfig(ReaderWriterConfig):
    def __init__(self, options: dict[str, str]) -> None:
        super().__init__(
            _Config(
                default_config={
                    # TODO: primitivesAsString: Union[bool, str, None] = None,
                    # TODO: prefersDecimal: Union[bool, str, None] = None,
                    # TODO: allowComments: Union[bool, str, None] = None,
                    # TODO: allowUnquotedFieldNames: Union[bool, str, None] = None,
                    # TODO: allowSingleQuotes: Union[bool, str, None] = None,
                    # TODO: allowNumericLeadingZero: Union[bool, str, None] = None,
                    # TODO: allowBackslashEscapingAnyCharacter: Union[bool, str, None] = None,
                    # TODO: columnNameOfCorruptRecord: Optional[str] = None,
                    "dateFormat": "auto",
                    "timestampFormat": "auto",
                    "mode": "PERMISSIVE",
                    "multiLine": "false",
                    # TODO: allowUnquotedControlChars: Union[bool, str, None] = None,
                    # TODO: lineSep: Optional[str] = None,
                    # TODO: samplingRatio: Union[str, float, None] = None,
                    # TODO: dropFieldIfAllNull: Union[bool, str, None] = None,
                    # TODO: encoding: Optional[str] = None,
                    # TODO: pathGlobFilter: Union[bool, str, None] = None,
                    # TODO: recursiveFileLookup: Union[bool, str, None] = None,
                    # TODO: modifiedBefore: Union[bool, str, None] = None,
                    # TODO: modifiedAfter: Union[bool, str, None] = None,
                    # TODO: allowNonNumericNumbers: Union[bool, str, None] = None,
                    "batchSize": 1000,
                    "processInBulk": "False",
                    "jsonFileParallelLoading": "False",
                    # this controls the number of rows to pull locally to infer nested schema. Once infer schema supports nested schema, this will be removed.
                    "jsonLocalRowsToInferSchema": 1000,
                    "splitSizeMb": 2,
                },
                supported_options={
                    "schema",
                    # "primitivesAsString",
                    # "prefersDecimal",
                    # "allowComments",
                    # "allowUnquotedFieldNames",
                    # "allowSingleQuotes",
                    # "allowNumericLeadingZero",
                    # "allowBackslashEscapingAnyCharacter",
                    "mode",
                    # "columnNameOfCorruptRecord",
                    "dateFormat",
                    "timestampFormat",
                    "multiLine",
                    # "allowUnquotedControlChars",
                    # "lineSep",
                    # "samplingRatio",
                    "dropFieldIfAllNull",
                    "encoding",
                    # "locale",
                    "pathGlobFilter",
                    # "recursiveFileLookup",
                    # "modifiedBefore",
                    # "modifiedAfter",
                    # "allowNonNumericNumbers",
                    "compression",
                    # "ignoreNullFields",
                    "rowsToInferSchema",
                    "relaxTypesToInferSchema",
                    # "inferTimestamp",
                    "batchSize",
                    "processInBulk",
                    "jsonFileParallelLoading",
                    "jsonLocalRowsToInferSchema",
                    "splitSizeMb",
                },
                boolean_config_list=[
                    "multiLine",
                    "dropFieldIfAllNull",
                    "processInBulk",
                    "jsonFileParallelLoading",
                ],
                int_config_list=[
                    "rowsToInferSchema",
                    "batchSize",
                    "splitSizeMb",
                    "jsonLocalRowsToInferSchema",
                ],
                float_config_list=["samplingRatio"],
            ),
            options,
        )

    def convert_to_snowpark_args(self) -> dict[str, Any]:
        renamed_args = {
            "inferSchema": "INFER_SCHEMA",
            "dateFormat": "DATE_FORMAT",
            "timestampFormat": "TIMESTAMP_FORMAT",
            "pathGlobFilter": "PATTERN",
        }
        renamed_args = lowercase_dict_keys(renamed_args)
        snowpark_config = super().convert_to_snowpark_args()

        apply_infer_schema_options(snowpark_config)

        # Rename the keys to match the Snowpark configuration.
        for spark_arg, snowpark_arg in renamed_args.items():
            if spark_arg not in snowpark_config:
                continue
            snowpark_config[snowpark_arg] = snowpark_config[spark_arg]
            del snowpark_config[spark_arg]

        # Spark's multiLine maps to both STRIP_OUTER_ARRAY and MULTI_LINE in Snowflake's JSON file format.
        multiline_key = "multiline"
        if multiline_key in snowpark_config:
            multi_line_value = snowpark_config.pop(multiline_key)
            snowpark_config["STRIP_OUTER_ARRAY"] = multi_line_value
            snowpark_config["MULTI_LINE"] = multi_line_value

        return snowpark_config


class ParquetReaderConfig(ReaderWriterConfig):
    def __init__(self, options: dict[str, str]) -> None:
        super().__init__(
            _Config(
                default_config={},
                supported_options={
                    # "mergeSchema",
                    "pathGlobFilter",
                    # "recursiveFileLookup",
                    # "modifiedBefore",
                    # "modifiedAfter",
                    # "datetimeRebaseMode",
                    # "int96RebaseMode",
                    # "mode",
                    "compression",
                    "rowsToInferSchema",
                },
                boolean_config_list=[],
                int_config_list=[],
                float_config_list=[],
            ),
            options,
        )

    def convert_to_snowpark_args(self) -> dict[str, Any]:
        renamed_args = {
            "pathGlobFilter": "PATTERN",
        }
        renamed_args = lowercase_dict_keys(renamed_args)
        snowpark_args = super().convert_to_snowpark_args()

        for spark_arg, snowpark_arg in renamed_args.items():
            if spark_arg not in snowpark_args:
                continue
            snowpark_args[snowpark_arg] = snowpark_args[spark_arg]
            del snowpark_args[spark_arg]

        # Should be determined by spark.sql.parquet.binaryAsString, but currently Snowpark Connect only supports
        # the default value (false). TODO: Add support for spark.sql.parquet.binaryAsString equal to "true".
        snowpark_args["BINARY_AS_TEXT"] = False

        # Set USE_VECTORIZED_SCANNER from global config. This will become the default in a future BCR.
        snowpark_args["USE_VECTORIZED_SCANNER"] = global_config._get_config_setting(
            "snowpark.connect.parquet.useVectorizedScanner"
        )

        # Set USE_LOGICAL_TYPE from global config to properly handle Parquet logical types like TIMESTAMP.
        # Without this, Parquet TIMESTAMP (INT64 physical) is incorrectly read as NUMBER(38,0).
        snowpark_args["USE_LOGICAL_TYPE"] = global_config._get_config_setting(
            "snowpark.connect.parquet.useLogicalType"
        )

        return snowpark_args


class XmlReaderConfig(ReaderWriterConfig):
    def __init__(self, options: dict[str, str]) -> None:
        super().__init__(
            _Config(
                default_config={
                    # TODO: samplingRatio: 1.0,
                    # TODO: inferSchema: true,
                    "attributePrefix": "_",
                    "valueTag": "_VALUE",
                    "mode": "PERMISSIVE",
                    "columnNameOfCorruptRecord": "_corrupt_record",
                    "nullValue": "",
                    "encoding": "UTF-8",
                    "excludeAttribute": "false",
                    "ignoreNamespace": "false",
                    "ignoreSurroundingSpaces": "false",
                    # TODO: timeZone: (spark.sql.session.timeZone),
                    # TODO: timestampFormat: yyyy-MM-dd'T'HH:mm:ss[.SSS][XXX],
                    # TODO: timestampNTZFormat: yyyy-MM-dd'T'HH:mm:ss[.SSS],
                    # TODO: dateFormat: yyyy-MM-dd,
                    # TODO: locale: en-US,
                    # TODO: wildcardColName: xs_any,
                },
                supported_options={
                    "rowTag",
                    # "samplingRatio",
                    "excludeAttribute",
                    "mode",
                    # "inferSchema",
                    "columnNameOfCorruptRecord",
                    "attributePrefix",
                    "valueTag",
                    "encoding",
                    "ignoreSurroundingSpaces",
                    "rowValidationXSDPath",
                    "ignoreNamespace",
                    # "timeZone",
                    # "timestampFormat",
                    # "timestampNTZFormat",
                    # "dateFormat",
                    # "locale",
                    # "rootTag",
                    # "declaration",
                    # "arrayElementName",
                    "nullValue",
                    # "wildcardColName",
                    "compression",  # not supported when rowTag is specified
                    # "validateName",
                    "pathGlobFilter",
                    # "recursiveFileLookup",
                    # "modifiedBefore",
                },
                boolean_config_list=[
                    "excludeAttribute",
                    "ignoreNamespace",
                    "ignoreSurroundingSpaces",
                ],
                int_config_list=[],
                float_config_list=[],
            ),
            options,
        )

    def convert_to_snowpark_args(self) -> dict[str, Any]:
        snowpark_config = super().convert_to_snowpark_args()

        # Rename Spark options to Snowpark equivalents
        renamed_args = {
            "encoding": "charset",
            "excludeAttribute": "excludeAttributes",
            "ignoreSurroundingSpaces": "ignoreSurroundingWhitespace",
            "pathGlobFilter": "PATTERN",
        }

        for spark_arg, snowpark_arg in renamed_args.items():
            if spark_arg in snowpark_config:
                snowpark_config[snowpark_arg] = snowpark_config[spark_arg]
                del snowpark_config[spark_arg]

        # Snowpark-specific
        snowpark_config["cacheResult"] = True

        return snowpark_config
