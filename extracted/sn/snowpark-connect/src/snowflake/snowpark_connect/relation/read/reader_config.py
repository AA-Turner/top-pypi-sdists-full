#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

import codecs
from dataclasses import dataclass
from typing import Any

from pyspark.errors.exceptions.base import IllegalArgumentException

from snowflake.snowpark_connect.config import global_config, str_to_bool
from snowflake.snowpark_connect.date_time_format_mapping import (
    convert_java_datetime_format_for_fileformat,
)
from snowflake.snowpark_connect.error.error_codes import ErrorCodes
from snowflake.snowpark_connect.error.error_utils import (
    UnsupportedCharsetException,
    attach_custom_error_code,
)
from snowflake.snowpark_connect.utils.snowpark_connect_logging import logger

DEFAULT_ROWS_TO_INFER_SCHEMA = 20000

# SNOW-3536373: PySpark lenient UTF-8 vs Snowflake COPY strict default.
DEFAULT_REPLACE_INVALID_CHARACTERS = "true"


def validate_json_charset_name(encoding: str) -> str:
    """Validate that ``encoding`` is a recognized charset and return its
    canonical uppercase name (e.g. ``"utf-8"`` → ``"UTF-8"``) — the form
    Snowflake's COPY INTO command expects.

    This is the side-effect-free, write-safe portion of SPARK-23723
    validation: it raises :class:`UnsupportedCharsetException` for unknown
    charset names (e.g. ``"UTF-128"``) but does **not** enforce SPARK-24190's
    read-only multiLine denyList — that restriction applies only when Spark
    is parsing files line-by-line and is meaningless on the write path.

    Used by :class:`JsonReaderConfig._validate_encoding` for reads and by the
    JSON write-options path in
    :mod:`snowflake.snowpark_connect.relation.write.map_write`.

    Args:
        encoding: User-supplied encoding name (case-insensitive, may use any
            alias accepted by :func:`codecs.lookup`).

    Returns:
        The canonical uppercase encoding name.

    Raises:
        UnsupportedCharsetException: If ``encoding`` is not a recognized
            charset alias.
    """
    try:
        canonical = codecs.lookup(encoding).name
    except LookupError:
        exception = UnsupportedCharsetException(encoding)
        attach_custom_error_code(exception, ErrorCodes.INVALID_FUNCTION_ARGUMENT)
        raise exception
    return canonical.upper()


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
        # Subclasses may set ``_INTERNALLY_CONSUMED_OPTIONS`` to options handled
        # upstream (e.g. ``recursiveFileLookup``); suppress the unsupported-option
        # warning for those keys (SNOW-3566246).
        internally_consumed = getattr(self, "_INTERNALLY_CONSUMED_OPTIONS", frozenset())

        for key, value in self.config.items():
            if key in self.supported_options:
                snowpark_config[key] = value
            elif key not in internally_consumed:
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
        # SNOW-3245116: nanValue/positiveInf/negativeInf are recognized and
        # handled in map_read_csv.py (positional CASE WHEN for float-preserving
        # reads; NULL_IF fallback otherwise). They are consumed internally via
        # CsvReaderConfig._INTERNALLY_CONSUMED_OPTIONS, not forwarded to Snowpark.
        "nanValue",
        "positiveInf",
        "negativeInf",
        "dateFormat",
        "timestampFormat",
        # "maxColumns",
        # "maxCharsPerColumn",
        # "maxMalformedLogPerPartition",
        "mode",
        "columnNameOfCorruptRecord",
        "multiLine",
        # "charToEscapeQuoteEscaping",
        # "samplingRatio",
        # enforceSchema is consumed by map_read_csv, not forwarded to Snowpark
        # "enforceSchema",
        # SNOW-3389610: no Snowflake equivalent; popped in csv_convert_to_snowpark_args,
        # projected in map_read_csv / rewrite_df. EMPTY_FIELD_AS_NULL stays TRUE.
        "emptyValue",
        # "locale",
        "lineSep",
        "pathGlobFilter",
        # "recursiveFileLookup",  # consumed by map_read._read_file / path_anchoring
        # "modifiedBefore",
        # "modifiedAfter",
        # "unescapedQuoteHandling",
        "compression",
        # "escapeQuotes",
        # "quoteAll",
        "rowsToInferSchema",  # Snowflake specific option, number of rows to infer schema
        "relaxTypesToInferSchema",  # Snowflake specific option, whether to relax types to infer schema
        "mergeSchema",  # SCOS: union CSV columns across multiple paths (not in OSS Spark CSV)
        # SNOW-3295599: SCOS-only per-read knob. Spark has no public CSV
        # ``skipBlankLines`` option (Univocity default = true), but SCOS exposes
        # one so power-users can opt out of Snowflake's SKIP_BLANK_LINES=TRUE.
        "skipBlankLines",
        # Snowflake-specific passthrough: replace invalid UTF-8 bytes with U+FFFD
        # instead of erroring. Spark's CSV reader is lenient on invalid UTF-8 by
        # default, so users that round-trip lone surrogates / truncated sequences
        # need this to match Spark's behavior.
        "replaceInvalidCharacters",
    }
)

# Config has to be lowercased, because it is publicly available
CSV_READ_DEFAULT_CONFIG = lowercase_dict_keys(
    {
        "header": "false",
        "inferSchema": "false",
        "enforceSchema": "true",
        # TODO: This default is ok for reads, but it should be removed for writes because it will lead to
        # quoting even when it is not necessary.
        "quote": '"',
        "comment": "#",
        # TODO nullValue of "" is correct for Spark, Snowflake's default is \N.
        # However, Snowflake will refuse to write when nullValue is empty and fields aren't
        # optionally enclosed. Hence, we are not changing the default nullValue.
        # We need to look more to see if this is a good default for both write+read, or if we need to adjust.
        # "nullValue": "",
        # SNOW-3245116: nanValue/positiveInf/negativeInf have no default here;
        # they are only applied when the user explicitly supplies them.
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
        "rowsToInferSchema": DEFAULT_ROWS_TO_INFER_SCHEMA,
    }
)


def _set_infer_schema_continue(options: dict[str, Any]) -> None:
    options.setdefault("INFER_SCHEMA_OPTIONS", {})["ON_ERROR"] = "CONTINUE"


def apply_drop_malformed_on_error(options: dict[str, Any]) -> None:
    """Set ON_ERROR=CONTINUE in both INFER_SCHEMA_OPTIONS and top-level options.

    Called when mode=DROPMALFORMED. Maps to Snowflake's ON_ERROR=CONTINUE
    which silently drops rows that fail to parse (SNOW-3308282).
    """
    _set_infer_schema_continue(options)
    options["ON_ERROR"] = "CONTINUE"


def apply_permissive_on_error(options: dict[str, Any]) -> None:
    """Set INFER_SCHEMA ON_ERROR=CONTINUE and COPY INTO ON_ERROR=PERMISSIVE.

    Used by the CSV reader (SNOW-3308282). INFER_SCHEMA does not accept
    PERMISSIVE, so it uses CONTINUE to skip bad rows during schema
    inference. COPY INTO uses PERMISSIVE, which null-pads short rows /
    truncates extras to match Spark's PERMISSIVE semantics.

    JSON uses ``apply_permissive_on_error_json`` instead — see that
    function for why JSON sets ON_ERROR at the COPY INTO call site.
    """
    _set_infer_schema_continue(options)
    options["ON_ERROR"] = "PERMISSIVE"


def apply_permissive_on_error_json(options: dict[str, Any]) -> None:
    """Set INFER_SCHEMA ON_ERROR=CONTINUE for JSON PERMISSIVE mode.

    Allows infer schema to skip bad rows and infer from good ones.
    Does NOT set top-level ON_ERROR — the JSON reader sets that on the
    COPY INTO call site after first guarding against the ``$1 VARIANT``
    fallback schema (see ``_is_variant_fallback_schema`` in
    map_read_json.py). Without that guard, structurally broken files
    (e.g. multi-line JSON without ``multiLine=true``) would silently
    produce NULLs instead of erroring as Spark does.
    """
    _set_infer_schema_continue(options)


def apply_infer_schema_options(snowpark_config: dict[str, Any]) -> None:
    """Pop rowsToInferSchema and relaxTypesToInferSchema from config.

    If rowsToInferSchema is present and > 0, sets INFER_SCHEMA_OPTIONS
    with MAX_RECORDS_PER_FILE and sets relaxtypestoinferschema for SAS
    to handle type widening (via relax_json_types in map_read_json.py).

    We intentionally do NOT use Snowpark's USE_RELAXED_TYPES option because
    Snowpark's most_permissive_type() maps all numerics to DoubleType, which
    doesn't match Spark's JSON inference rules (integers should be LongType,
    not DoubleType). Instead, SCOS applies its own Spark-compatible relaxation.

    Shared by CSV and JSON readers.
    """
    if "rowstoinferschema" not in snowpark_config:
        return

    rows_to_infer_schema = int(snowpark_config.pop("rowstoinferschema"))

    if "relaxtypestoinferschema" not in snowpark_config:
        snowpark_config["relaxtypestoinferschema"] = rows_to_infer_schema > 0

    if rows_to_infer_schema > 0:
        snowpark_config["INFER_SCHEMA_OPTIONS"] = {
            "MAX_RECORDS_PER_FILE": rows_to_infer_schema,
        }


# SNOW-3389608: Mirror Spark's ``CSVExprUtils.toDelimiterStr`` — walk the
# CSV ``sep`` / ``lineSep`` value chunk-by-chunk and translate each
# 2-char ``\\<x>`` escape to the corresponding 1-char value. Spark's
# ``toChar`` covers ``\\t \\r \\b \\f \\" \\' \\\\``; we accept the same
# set plus ``\\n``, ``\\0`` and ``\\uNNNN`` as SCOS-only conveniences.
# Without this, Scala raw-string delimiters such as ``"""_/-\\\\_"""``
# (6 chars from a SPARK-24540 test) reach Snowflake unchanged and
# tokenize on the wrong byte sequence.
_CSV_ESCAPE_LITERAL_PAIRS = {
    "t": "\t",
    "r": "\r",
    "b": "\b",
    "f": "\f",
    "n": "\n",
    "0": "\0",
    "\\": "\\",
    '"': '"',
    "'": "'",
}


def _translate_csv_escape_literal(s: str | None) -> str | None:
    """Translate Java/Spark string-literal escape sequences inside a CSV
    delimiter / line-separator option, chunk-by-chunk, mirroring Spark's
    ``CSVExprUtils.toDelimiterStr``.

    Handles both 1-char escapes (``"\\t"`` -> tab) and embedded escapes
    inside a longer delimiter (``"_/-\\\\_"`` 6 chars from a Scala raw
    triple-quoted string -> 5-char ``"_/-\\_"`` matching the test fixture).
    ``\\uNNNN`` Unicode escapes are accepted as a SCOS-only extension. A
    trailing solo backslash is left literal (Spark errors here, but
    downstream SQL escaping doubles it anyway).
    """
    if not s:
        return s
    out: list[str] = []
    i = 0
    while i < len(s):
        ch = s[i]
        if ch == "\\" and i + 1 < len(s):
            nxt = s[i + 1]
            if nxt == "u" and i + 5 < len(s):
                try:
                    out.append(chr(int(s[i + 2 : i + 6], 16)))
                    i += 6
                    continue
                except ValueError:
                    logger.warning(
                        f"Invalid unicode escape sequence \\u{s[i + 2 : i + 6]!r} "
                        "in CSV option; treating as literal characters."
                    )
            mapped = _CSV_ESCAPE_LITERAL_PAIRS.get(nxt)
            if mapped is not None:
                out.append(mapped)
                i += 2
                continue
        out.append(ch)
        i += 1
    return "".join(out)


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
        "replaceInvalidCharacters": "REPLACE_INVALID_CHARACTERS",
        "skipBlankLines": "SKIP_BLANK_LINES",
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

    # SNOW-3389608: Translate Spark/Java string-literal escape sequences in
    # ``sep`` and ``lineSep`` (e.g. ``"\\t"`` 2 chars -> tab; ``"_/-\\\\_"`` 6
    # chars from a Scala raw triple-quoted string -> 5-char ``"_/-\\_"``).
    # Mirrors Spark's ``CSVExprUtils.toDelimiterStr``. Must run before the
    # ``sep_is_backslash`` SQL-encoding rules below — those operate on the
    # post-translation value.
    for esc_key in ("sep", "linesep"):
        if esc_key in snowpark_config:
            snowpark_config[esc_key] = _translate_csv_escape_literal(
                snowpark_config[esc_key]
            )

    # SNOW-3245108: Logical '\' field delimiter must be represented as two
    # backslash characters for Snowflake's CREATE FILE FORMAT (SQL string encoding).
    # Clients may send one '\' (sep="\\" in Python) or two (PySpark: "pass two
    # backslashes in the option string" for a single '\' delimiter).
    # SNOW-3389608: the same SQL-encoding rule applies to multi-character
    # delimiters that contain a backslash (e.g. ``"_/-\\_"`` from
    # SPARK-24540). Without doubling, Snowflake unescapes ``\\`` and tokenizes
    # on a string the user did not intend.
    sep_val = snowpark_config.get("sep")
    sep_is_backslash = sep_val in ("\\", "\\\\")
    if sep_is_backslash:
        snowpark_config["sep"] = "\\\\"
    elif sep_val and "\\" in sep_val:
        snowpark_config["sep"] = sep_val.replace("\\", "\\\\")

    linesep_val = snowpark_config.get("linesep")
    if linesep_val and "\\" in linesep_val:
        snowpark_config["linesep"] = linesep_val.replace("\\", "\\\\")

    # Empty quote means no quoting — remove so Snowflake uses its default (NONE)
    if "quote" in snowpark_config and snowpark_config["quote"] == "":
        del snowpark_config["quote"]

    # spark does not escape unenclosed fields
    snowpark_config["ESCAPE_UNENCLOSED_FIELD"] = "NONE"
    # ``ERROR_ON_COLUMN_COUNT_MISMATCH = FALSE`` is required when we route
    # CSV through ``INCLUDE_METADATA + MATCH_BY_COLUMN_NAME`` (see
    # ``_load_file_with_copy_into`` and SNOW-3554281) -- the server would
    # otherwise raise spurious mismatches because the file's column count
    # is checked against the union of data + metadata columns. ``setdefault``
    # so an explicit user override still wins.
    snowpark_config.setdefault("ERROR_ON_COLUMN_COUNT_MISMATCH", False)
    # ``REPLACE_INVALID_CHARACTERS = TRUE`` matches Spark's effective
    # behavior: Spark's CSV parser tolerates malformed UTF-8 bytes (the
    # underlying Java input-stream decoder replaces them with U+FFFD),
    # whereas Snowflake's CSV default is to raise. Spark does not expose
    # a user-settable option to disable this, so we pin the SCOS-friendly
    # default unconditionally. ``setdefault`` is used for future-proofing
    # only — if a SCOS-specific opt-out knob is ever added it would slot
    # in here without further changes.
    snowpark_config.setdefault("REPLACE_INVALID_CHARACTERS", True)
    # SNOW-3389610: Spark's `emptyValue` option has no Snowflake counterpart.
    # The translation lives in `map_read_csv` (post-load projection of "" ->
    # emptyValue) and `rewrite_df` (pre-write "" -> emptyValue). Pop the key
    # here so it does not leak into Snowflake's COPY INTO file_format dict
    # (which would reject the unknown key). The original user value remains
    # accessible via `CsvReaderConfig.config["emptyvalue"]` /
    # `write_op.options["emptyValue"]` for the projection step.
    #
    # We intentionally do NOT flip EMPTY_FIELD_AS_NULL: with the default
    # (TRUE), Snowflake distinguishes a bare `,,` (-> NULL) from a quoted
    # `""` (-> empty string). That distinction matches Spark's behavior
    # under the default `nullValue=""`: the bare `,,` is treated as NULL
    # (matching nullValue), while `""` is the empty string that gets
    # rewritten to emptyValue by the projection. Forcing
    # EMPTY_FIELD_AS_NULL=FALSE would erase the distinction and rewrite
    # bare `,,` cells to emptyValue too, which Spark would not do.
    snowpark_config.pop("emptyvalue", None)
    # snowpark_config["EMPTY_FIELD_AS_NULL"] = True

    # Fix the escape character if it is provided.
    # TODO SNOW-2081726: This seems to be a Snowpark bug
    # SNOW-3245108: Do not double a one-char escape when FIELD_DELIMITER is also '\'
    # (see sep_is_backslash / FIELD_DELIMITER SQL encoding above).
    if (
        snowpark_config.get("escape")
        and snowpark_config["escape"] == "\\"
        and not sep_is_backslash
    ):
        snowpark_config["escape"] = "\\\\"

    # Snowflake rejects ESCAPE when FIELD_DELIMITER contains the escape character
    # (001118/001019 conflict: "ESCAPE: '\\x5c' can not be a substring of
    # FIELD_DELIMITER: ..."). We drop ESCAPE in this case since backslash is the
    # default escape character and Snowflake cannot have ESCAPE match — or be a
    # substring of — FIELD_DELIMITER.
    sep_contains_backslash = bool(sep_val) and "\\" in sep_val
    if sep_contains_backslash and "escape" in snowpark_config:
        del snowpark_config["escape"]

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

    # Pop Spark's 'mode' option so it doesn't pass through as a Snowflake option.
    # Actual handling happens in map_read_csv.py (same pattern as JSON).
    snowpark_config.pop("mode", None)

    # Convert Java/Spark date and timestamp format strings to Snowflake equivalents.
    # Spark uses Java SimpleDateFormat patterns (e.g. dd/MM/yyyy HH:mm) while
    # Snowflake uses its own tokens (DD/MM/YYYY HH24:MI). The literal value
    # "auto" is a Snowflake sentinel (TIMESTAMP_FORMAT='AUTO') that asks
    # Snowflake to detect the layout; pass it through unchanged.
    for fmt_key in ("dateformat", "timestampformat"):
        if fmt_key in snowpark_config and snowpark_config[fmt_key]:
            if str(snowpark_config[fmt_key]).lower() == "auto":
                snowpark_config[fmt_key] = "AUTO"
                continue
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

    # Options consumed by map_read_csv.py but not forwarded to Snowpark.
    _INTERNALLY_CONSUMED_OPTIONS = frozenset(
        {
            "enforceschema",
            "comment",
            "recursivefilelookup",
            # SNOW-3245116: NaN/Inf tokens handled in map_read_csv.py.
            "nanvalue",
            "positiveinf",
            "negativeinf",
        }
    )

    def __init__(self, options: dict[str, str]) -> None:
        # For READ: default dateFormat/timestampFormat to Snowflake AUTO so
        # that COPY INTO (which parses into typed columns) accepts the many
        # timestamp layouts Spark's default parser accepts (e.g. without
        # fractional seconds). The original Spark-default strings (yyyy-MM-dd,
        # yyyy-MM-dd HH:mm:ss.SSSSSS) would translate to strict Snowflake
        # format tokens and reject common layouts like "2023-01-01 10:30:00".
        # The writer keeps CSV_READ_DEFAULT_CONFIG unchanged.
        read_default_config = {
            **CSV_READ_DEFAULT_CONFIG,
            "dateformat": "auto",
            "timestampformat": "auto",
            "replaceInvalidCharacters": DEFAULT_REPLACE_INVALID_CHARACTERS,
        }
        super().__init__(
            _Config(
                default_config=read_default_config,
                supported_options=CSV_READ_SUPPORTED_OPTIONS,
                boolean_config_list=[
                    "header",
                    "inferSchema",
                    "enforceSchema",
                    "mergeSchema",
                    "multiLine",
                    "ignoreLeadingWhiteSpace",
                    "ignoreTrailingWhiteSpace",
                    "escapeQuotes",
                    "quoteAll",
                    "replaceInvalidCharacters",
                    "skipBlankLines",
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
        snowpark_config = {}
        for key, value in self.config.items():
            if key in self.supported_options:
                snowpark_config[key] = value
            elif key not in self._INTERNALLY_CONSUMED_OPTIONS:
                logger.warning(
                    f"Reader option '{key}' is not supported and will be ignored. Results may differ from Spark."
                )
        for key in snowpark_config.keys():
            snowpark_config[key] = self._get_config_setting(key)
        return csv_convert_to_snowpark_args(snowpark_config)


# TODO: This is just a first pass, we need to differentiate more clearly between read and write configs.
class CsvWriterConfig(ReaderWriterConfig):
    # spark reader options that snowpark is able to handle.
    # Spark options are here: https://spark.apache.org/docs/latest/sql-data-sources-csv.html
    # Snowpark options are here: https://docs.snowflake.com/en/sql-reference/sql/create-file-format

    # SNOW-3245116: nanValue/positiveInf/negativeInf are read-side-only options.
    # They are pulled in via ``CSV_READ_SUPPORTED_OPTIONS`` above, so exclude
    # them here so a write does not forward them to Snowflake as unknown
    # file-format parameters.
    _INTERNALLY_CONSUMED_OPTIONS = frozenset({"nanvalue", "positiveinf", "negativeinf"})

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
    # Options consumed upstream; suppress unsupported-option warning (SNOW-3566246).
    _INTERNALLY_CONSUMED_OPTIONS = frozenset({"recursivefilelookup"})

    # Encoding denyList for non-multiLine mode (SPARK-24190 / SNOW-3246417).
    #
    # Only the "UTF-16" and "UTF-32" charsets themselves are denied — the
    # explicit-endianness variants (UTF-16LE, UTF-16BE, UTF-32LE, UTF-32BE)
    # are *allowed* because they have no BOM and a known byte order, matching
    # Spark's behavior:
    #
    #     val isDenied = JSONOptionsInRead.denyList.contains(Charset.forName(enc))
    #     // denyList = Seq(Charset.forName("UTF-16"), Charset.forName("UTF-32"))
    #
    # Comparison is performed against the canonical name returned by
    # ``codecs.lookup().name`` so that all aliases (e.g. ``"utf16"``,
    # ``"UTF_16"``, ``"UTF-16"``) collapse to the same key.
    _ENCODING_DENYLIST = frozenset({"utf-16", "utf-32"})

    def __init__(self, options: dict[str, str]) -> None:
        super().__init__(
            _Config(
                default_config={
                    # TODO: primitivesAsString: Union[bool, str, None] = None,
                    # TODO: prefersDecimal: Union[bool, str, None] = None,
                    # TODO: allowComments: Union[bool, str, None] = None,
                    # TODO: allowUnquotedFieldNames: Union[bool, str, None] = None,
                    # TODO: allowSingleQuotes: Union[bool, str, None] = None,
                    # TODO: allowNumericLeadingZeros: Union[bool, str, None] = None,
                    # TODO: allowBackslashEscapingAnyCharacter: Union[bool, str, None] = None,
                    "columnNameOfCorruptRecord": "_corrupt_record",
                    "dateFormat": "auto",
                    "timestampFormat": "auto",
                    "mode": "PERMISSIVE",
                    "multiLine": "false",
                    # TODO: allowUnquotedControlChars: Union[bool, str, None] = None,
                    # TODO: lineSep: Optional[str] = None,
                    # TODO: samplingRatio: Union[str, float, None] = None,
                    # TODO: dropFieldIfAllNull: Union[bool, str, None] = None,
                    "encoding": "utf-8",
                    # TODO: pathGlobFilter: Union[bool, str, None] = None,
                    # TODO: recursiveFileLookup: Union[bool, str, None] = None,
                    # TODO: modifiedBefore: Union[bool, str, None] = None,
                    # TODO: modifiedAfter: Union[bool, str, None] = None,
                    # TODO: allowNonNumericNumbers: Union[bool, str, None] = None,
                    "batchSize": 1000,
                    "processInBulk": "True",
                    "jsonFileParallelLoading": "False",
                    # this controls the number of rows to pull locally to infer nested schema. Once infer schema supports nested schema, this will be removed.
                    "jsonLocalRowsToInferSchema": 1000,
                    "splitSizeMb": 2,
                    "rowsToInferSchema": DEFAULT_ROWS_TO_INFER_SCHEMA,
                    "replaceInvalidCharacters": DEFAULT_REPLACE_INVALID_CHARACTERS,
                },
                supported_options={
                    "schema",
                    # "primitivesAsString",
                    # "prefersDecimal",
                    # "allowComments",
                    # "allowUnquotedFieldNames",
                    # "allowSingleQuotes",
                    # "allowNumericLeadingZeros",
                    # "allowBackslashEscapingAnyCharacter",
                    "mode",
                    "columnNameOfCorruptRecord",
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
                    # "recursiveFileLookup",  # consumed by map_read._read_file / path_anchoring
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
                    # Snowflake-specific passthrough: replace invalid UTF-8 bytes
                    # with U+FFFD instead of erroring during the COPY INTO. Spark's
                    # default JSON parser is lenient on invalid UTF-8 so users that
                    # round-trip lone surrogates / truncated sequences need this to
                    # match Spark's behavior.
                    "replaceInvalidCharacters",
                },
                boolean_config_list=[
                    "multiLine",
                    "dropFieldIfAllNull",
                    "processInBulk",
                    "jsonFileParallelLoading",
                    "replaceInvalidCharacters",
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
        self._validate_encoding()

    def _validate_encoding(self) -> None:
        """
        Validate the encoding option for JSON reading.

        This implements two validations from Spark:
        1. SPARK-23723: Throw UnsupportedCharsetException for invalid charset names
        2. SPARK-24190: Throw IllegalArgumentException when UTF-16/32 is used with
           multiLine=false (these encodings use multi-byte line separators)

        Additionally canonicalizes the encoding name to the uppercase form Snowflake
        expects (e.g. "UTF8", "utf-8", "Utf-8" all become "UTF-8") using
        codecs.lookup().name and stores it back in self.config["encoding"].
        """
        encoding = self.config.get("encoding", "utf-8")

        # SPARK-23723: Validate the charset name and canonicalize it to the
        # uppercase form Snowflake's COPY INTO expects (e.g. "UTF-8" regardless
        # of how the user spelled it: "UTF8", "utf-8", "Utf-8", ...).
        canonical = validate_json_charset_name(encoding)
        self.config["encoding"] = canonical

        # SPARK-24190 / SNOW-3246417: Check encoding denyList for non-multiLine
        # mode. Use _get_config_setting to get the properly typed boolean value
        # (self.config stores raw strings, so "false" would be truthy).
        is_multiline = self._get_config_setting("multiline")
        if not is_multiline and canonical.lower() in self._ENCODING_DENYLIST:
            exception = IllegalArgumentException(
                f"encoding must not be included in the denyList when multiLine is disabled: {canonical}"
            )
            attach_custom_error_code(exception, ErrorCodes.INVALID_FUNCTION_ARGUMENT)
            raise exception

    def convert_to_snowpark_args(self) -> dict[str, Any]:
        renamed_args = {
            "inferSchema": "INFER_SCHEMA",
            "dateFormat": "DATE_FORMAT",
            "timestampFormat": "TIMESTAMP_FORMAT",
            "pathGlobFilter": "PATTERN",
            "replaceInvalidCharacters": "REPLACE_INVALID_CHARACTERS",
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

        # SPARK-12872: Normalize compression codec names to lowercase so that
        # user-supplied values like "gZiP" or "BZIP2" are accepted by both
        # Snowflake's FILE_FORMAT and the internal codec-check logic in
        # map_read_json.py. The default "auto" is already lowercase.
        if "compression" in snowpark_config:
            snowpark_config["compression"] = str(snowpark_config["compression"]).lower()

        # Spark's multiLine maps to both STRIP_OUTER_ARRAY and MULTI_LINE in Snowflake's JSON file format.
        multiline_key = "multiline"
        if multiline_key in snowpark_config:
            multi_line_value = snowpark_config.pop(multiline_key)
            snowpark_config["STRIP_OUTER_ARRAY"] = multi_line_value
            snowpark_config["MULTI_LINE"] = multi_line_value

        return snowpark_config


class ParquetReaderConfig(ReaderWriterConfig):
    # Options consumed upstream; suppress unsupported-option warning (SNOW-3566246).
    _INTERNALLY_CONSUMED_OPTIONS = frozenset({"recursivefilelookup"})

    def __init__(self, options: dict[str, str]) -> None:
        super().__init__(
            _Config(
                default_config={
                    "rowsToInferSchema": DEFAULT_ROWS_TO_INFER_SCHEMA,
                    "mergeSchema": "false",
                    "replaceInvalidCharacters": DEFAULT_REPLACE_INVALID_CHARACTERS,
                },
                supported_options={
                    "mergeSchema",  # SCOS: union schema across multiple parquet paths (not passed to Snowflake)
                    "pathGlobFilter",
                    # "recursiveFileLookup",  # consumed by map_read._read_file / path_anchoring
                    # "modifiedBefore",
                    # "modifiedAfter",
                    # "datetimeRebaseMode",
                    # "int96RebaseMode",
                    # "mode",
                    "compression",
                    "rowsToInferSchema",
                    # Snowflake-specific passthrough: replace invalid UTF-8 bytes
                    # in Parquet string columns with U+FFFD instead of erroring.
                    # Spark's Parquet reader is lenient on malformed UTF-8 by
                    # default, so this matches Spark's behavior.
                    "replaceInvalidCharacters",
                },
                boolean_config_list=["mergeSchema", "replaceInvalidCharacters"],
                int_config_list=["rowsToInferSchema"],
                float_config_list=[],
            ),
            options,
        )

    def convert_to_snowpark_args(self) -> dict[str, Any]:
        renamed_args = {
            "pathGlobFilter": "PATTERN",
            "replaceInvalidCharacters": "REPLACE_INVALID_CHARACTERS",
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

        # Always use the vectorized scanner. The non-vectorized path returns Parquet
        # MAP columns in their physical {"key_value": [...]} shape which
        # TRY_CAST(... AS MAP(K,V)) cannot unwrap, collapsing every map value to
        # NULL (see SNOW-3390852). Telemetry shows no external customer overrides
        # this, so the user-facing knob has been removed in favour of a hardcoded
        # TRUE here.
        snowpark_args["USE_VECTORIZED_SCANNER"] = True

        # Set USE_LOGICAL_TYPE from global config to properly handle Parquet logical types like TIMESTAMP.
        # Without this, Parquet TIMESTAMP (INT64 physical) is incorrectly read as NUMBER(38,0).
        snowpark_args["USE_LOGICAL_TYPE"] = global_config._get_config_setting(
            "snowpark.connect.parquet.useLogicalType"
        )

        return snowpark_args


class XmlReaderConfig(ReaderWriterConfig):
    # Options consumed upstream; suppress unsupported-option warning (SNOW-3566246).
    _INTERNALLY_CONSUMED_OPTIONS = frozenset({"recursivefilelookup"})

    def __init__(self, options: dict[str, str]) -> None:
        super().__init__(
            _Config(
                default_config={
                    "samplingRatio": "1.0",
                    "inferSchema": "true",
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
                    "samplingRatio",
                    "excludeAttribute",
                    "mode",
                    "inferSchema",
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
                    # "recursiveFileLookup",  # consumed by map_read._read_file / path_anchoring
                    # "modifiedBefore",
                },
                boolean_config_list=[
                    "excludeAttribute",
                    "ignoreNamespace",
                    "ignoreSurroundingSpaces",
                    "inferSchema",
                ],
                int_config_list=[],
                float_config_list=[
                    "samplingRatio",
                ],
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
