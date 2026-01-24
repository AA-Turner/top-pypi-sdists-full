#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

from dataclasses import dataclass
from typing import Any

from snowflake.snowpark_connect.config import global_config, str_to_bool
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
                logger.debug(f"unsupported reader option: {key}")

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
        "encoding",
        "quote",
        # escape has different semantics in snowpark, but should work for standard use-cases
        "escape",
        # "comment", # Comment is not supported
        "header",
        "inferSchema",
        # "ignoreLeadingWhiteSpace",
        # "ignoreTrailingWhiteSpace",
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
        "timestampFormat": "YYYY-MM-DD HH24:MI:SS.FF6",
        # TODO: Snowpark does not support maxColumns argument
        # "maxColumns": "20480",
        # TODO: Snowpark does not support maxCharsPerColumn argument
        # "maxCharsPerColumn": "1000000",
        # TODO: Snowpark does not support maxMalformedLogPerPartition argument
        # "maxMalformedLogPerPartition": "10",
        "charset": "UTF-8",
        # TODO: Snowpark does not support multiLine argument
        "multiLine": "false",
        # TODO: Snowpark does not support ignoreLeadingWhiteSpace argument
        # "ignoreLeadingWhiteSpace": "false",
        # TODO: Snowpark does not support ignoreTrailingWhiteSpace argument
        # "ignoreTrailingWhiteSpace": "false",
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
    }
    renamed_args = lowercase_dict_keys(renamed_args)

    # spark does not escape unenclosed fields
    snowpark_config["ESCAPE_UNENCLOSED_FIELD"] = "NONE"
    snowpark_config["ERROR_ON_COLUMN_COUNT_MISMATCH"] = False
    # snowpark_config["EMPTY_FIELD_AS_NULL"] = True

    # Fix the escape character if it is provided.
    # TODO SNOW-2081726: This seems to be a Snowpark bug
    if snowpark_config["escape"] and snowpark_config["escape"] == "\\":
        snowpark_config["escape"] = "\\\\"

    # Snowflake specific option, number of rows to infer schema for CSV files
    if "rowstoinferschema" in snowpark_config:
        rows_to_infer_schema = snowpark_config["rowstoinferschema"]
        del snowpark_config["rowstoinferschema"]
        relax_types_to_infer_schema = True
        if "relaxtypestoinferschema" in snowpark_config:
            relax_types_to_infer_schema = str_to_bool(
                str(snowpark_config["relaxtypestoinferschema"])
            )
            del snowpark_config["relaxtypestoinferschema"]
        snowpark_config["INFER_SCHEMA_OPTIONS"] = {
            "MAX_RECORDS_PER_FILE": int(rows_to_infer_schema),
            "USE_RELAXED_TYPES": relax_types_to_infer_schema,
        }

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
                        if key not in ["quote", "inferSchema", "compression"]
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
                    # TODO: multiLine: Union[bool, str, None] = None,
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
                    "rowsToInferSchema": 1000,
                    "batchSize": 1000,
                    "processInBulk": "False",
                    "bz2FileParallelLoading": "False",
                    "splitSizeMb": 2,
                    "additionalPaddingMb": 2,
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
                    # "mode",
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
                    # "inferTimestamp",
                    "batchSize",
                    "processInBulk",
                    "bz2FileParallelLoading",
                    "splitSizeMb",
                    "additionalPaddingMb",
                },
                boolean_config_list=[
                    "multiLine",
                    "dropFieldIfAllNull",
                    "processInBulk",
                    "bz2FileParallelLoading",
                ],
                int_config_list=[
                    "rowsToInferSchema",
                    "batchSize",
                    "splitSizeMb",
                    "additionalPaddingMb",
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
            "multiLine": "STRIP_OUTER_ARRAY",
            "pathGlobFilter": "PATTERN",
        }
        renamed_args = lowercase_dict_keys(renamed_args)
        snowpark_config = super().convert_to_snowpark_args()
        # Rename the keys to match the Snowpark configuration.
        for spark_arg, snowpark_arg in renamed_args.items():
            if spark_arg not in snowpark_config:
                continue
            snowpark_config[snowpark_arg] = snowpark_config[spark_arg]
            del snowpark_config[spark_arg]
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
