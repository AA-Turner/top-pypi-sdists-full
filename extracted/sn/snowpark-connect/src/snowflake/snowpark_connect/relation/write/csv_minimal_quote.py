#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#
"""Spark-minimal quoting for CSV writes without an explicit ``quote``.

Snowflake ``FIELD_OPTIONALLY_ENCLOSED_BY`` encloses every string on unload.
Spark quotes a field only when it contains the delimiter, the quote, or a
line break (univocity, ``quoteAll=false``). Putting ``quote='"'`` on the
writer therefore does not match Spark; that is why ``CsvWriterConfig`` omits
it, and why #3398 / #3490 were closed.

The default writer still sends ``escape='\\'``. With nothing to enclose the
field, COPY backslash-escapes the delimiter (``a\\,b``) and the read splits
the row (SNOW-3309109). Pre-quoting the column and leaving ``ESCAPE`` set
does the same thing to the quotes we just added (#3602).

This module quotes in the projection, then the caller drops ``ESCAPE`` so the
characters stay as written. An explicit ``quote`` option keeps today's path.
It is opt-in: ``snowpark.connect.csv.writeMinimalQuoting`` defaults to false.
"""

from __future__ import annotations

from typing import NamedTuple

from snowflake.snowpark import DataFrame
from snowflake.snowpark._internal.analyzer.analyzer_utils import (
    quote_name_without_upper_casing,
    unquote_if_quoted,
)
from snowflake.snowpark.functions import (
    Column,
    col,
    concat,
    contains,
    iff,
    lit,
    replace,
    sql_expr,
    startswith,
    to_char,
    to_varchar,
)
from snowflake.snowpark.types import (
    ArrayType,
    BinaryType,
    BooleanType,
    ByteType,
    DateType,
    DecimalType,
    DoubleType,
    FloatType,
    IntegerType,
    LongType,
    MapType,
    ShortType,
    StringType,
    StructField,
    StructType,
    TimestampType,
    TimeType,
    VariantType,
)
from snowflake.snowpark_connect.config import (
    is_csv_write_minimal_quoting_enabled,
    is_csv_write_spark_timestamp_format_enabled,
)
from snowflake.snowpark_connect.date_time_format_mapping import (
    convert_java_datetime_format_for_fileformat,
)
from snowflake.snowpark_connect.relation.read.reader_config import (
    CSV_READ_DEFAULT_CONFIG,
    SPARK_CSV_WRITE_TIMESTAMP_FORMAT,
    csv_null_if_sql_literal,
    csv_null_if_token,
    translate_csv_escape_literal,
)

_QUOTE = '"'
# rewrite_df stores a real empty string as this two-character token. It already
# contains a quote, so a second quoting pass would write "\"\"".
_DEFAULT_EMPTY_FILE_TOKEN = '""'


def _has_option(options: dict | None, name: str) -> bool:
    if not options:
        return False
    target = name.lower()
    return any(str(key).lower() == target for key in options)


def _last_option(options: dict | None, name: str, default: str) -> str:
    if not options:
        return default
    target = name.lower()
    found = default
    for key, value in options.items():
        if str(key).lower() == target:
            found = "" if value is None else str(value)
    return found


def csv_write_minimal_quoting_active(
    options: dict | None, *, enabled: bool | None = None
) -> bool:
    """True when this write should quote like Spark's default CSV writer.

    An explicit ``quote`` option skips this path. A non-empty quote keeps
    ``FIELD_OPTIONALLY_ENCLOSED_BY``. ``quote=''`` is deleted by
    ``csv_convert_to_snowpark_args``, so that write stays on the unquoted
    escape path rather than an enclosed one.

    A delimiter that contains a backslash also skips it. The CSV reader drops
    ``ESCAPE`` for such a delimiter (Snowflake rejects the pair), so it could
    not undo the ``\\"`` this path writes and would cut the field short.
    """
    if enabled is None:
        enabled = is_csv_write_minimal_quoting_enabled()
    if not enabled:
        return False
    if _has_option(options, "quote"):
        return False
    sep, _, _ = _resolved_quote_pieces(options)
    return "\\" not in sep


def _quote_mode(options: dict | None) -> tuple[bool, bool]:
    """``quoteAll`` and ``escapeQuotes``, with Spark's defaults (false, true)."""
    quote_all = _last_option(options, "quoteall", "false").strip().lower() == "true"
    escape_quotes = (
        _last_option(options, "escapequotes", "true").strip().lower() != "false"
    )
    return quote_all, escape_quotes


def _resolved_quote_pieces(options: dict | None) -> tuple[str, str, str]:
    """Delimiter, escape, and line separator, after Spark's escape translation.

    ``delimiter`` overrides ``sep``, matching ``csv_convert_to_snowpark_args``.
    The quote character stays ``"``: this path runs only when the caller did
    not set ``quote``.
    """
    sep = _last_option(options, "sep", ",")
    if _has_option(options, "delimiter"):
        sep = _last_option(options, "delimiter", sep)
    escape = _last_option(options, "escape", "\\")
    line_sep = _last_option(options, "linesep", "\n")
    return (
        translate_csv_escape_literal(sep) or "",
        translate_csv_escape_literal(escape) or "",
        translate_csv_escape_literal(line_sep) or "",
    )


class _QuoteSettings(NamedTuple):
    sep: str
    escape: str
    line_sep: str
    quote_all: bool
    escape_quotes: bool


def _quote_settings(options: dict | None) -> _QuoteSettings:
    """Quoting options, parsed once so a per-column loop does not rescan them."""
    return _QuoteSettings(*_resolved_quote_pieces(options), *_quote_mode(options))


def minimal_quote_text(
    value: str | None,
    *,
    sep: str = ",",
    escape: str = "\\",
    line_sep: str = "\n",
    quote: str = _QUOTE,
    quote_all: bool = False,
    escape_quotes: bool = True,
) -> str | None:
    """Python twin of :func:`minimal_quote_column`. Unit tests lock the rules.

    ``escape_quotes=False`` does not treat an embedded quote as a reason to
    quote. A value whose first character is the quote is still quoted, matching
    univocity. A field that is quoted still escapes its quotes.
    """
    if value is None:
        return None
    triggers, check_lead = _quote_triggers(
        sep, line_sep, escape_quotes=escape_quotes, quote=quote
    )
    needs_quotes = quote_all or any(piece in value for piece in triggers)
    if not needs_quotes and check_lead and value.startswith(quote):
        needs_quotes = True
    if not needs_quotes:
        return value
    escaped = value
    for old, new in _escape_steps(escape, quote):
        escaped = escaped.replace(old, new)
    return f"{quote}{escaped}{quote}"


def _triggers(sep: str, quote: str, line_sep: str) -> list[str]:
    seen: list[str] = []
    for piece in (sep, quote, "\n", "\r", line_sep):
        if piece and piece not in seen:
            seen.append(piece)
    return seen


# The trigger set and the escape order live in the two helpers below.
# minimal_quote_text (Python) and _minimal_quote (Column, used for every cell
# type) both use them; unit tests pin that the two agree.


def _quote_triggers(
    sep: str, line_sep: str, *, escape_quotes: bool, quote: str = _QUOTE
) -> tuple[list[str], bool]:
    """Substrings that make a field need quotes, and whether a leading quote does.

    With ``escapeQuotes=false`` an embedded quote is not a trigger, but
    univocity still quotes a value that starts with the quote character.
    """
    triggers = _triggers(sep, quote if escape_quotes else "", line_sep)
    return triggers, not escape_quotes and bool(quote)


def _escape_steps(escape: str, quote: str = _QUOTE) -> list[tuple[str, str]]:
    """``(old, new)`` replacements for a quoted field, in the order to apply them.

    ``escape`` equal to the quote doubles quotes. Any other escape is doubled
    first, then put in front of each quote.
    """
    if not escape:
        return []
    if escape == quote:
        return [(quote, quote + quote)]
    steps = [(escape, escape + escape)]
    if quote:
        steps.append((quote, escape + quote))
    return steps


def _quoted(column: Column, escape: str) -> Column:
    escaped = column
    for old, new in _escape_steps(escape):
        escaped = replace(escaped, lit(old), lit(new))
    return concat(lit(_QUOTE), escaped, lit(_QUOTE))


def minimal_quote_column(column: Column, options: dict | None) -> Column:
    """Quote ``column`` when Spark's default CSV writer would.

    One ``IFF`` per column. A NULL fails the ``CONTAINS`` test and stays NULL,
    so it needs no arm of its own.
    """
    return _minimal_quote(column, _quote_settings(options))


def _minimal_quote(column: Column, settings: _QuoteSettings) -> Column:
    quoted = _quoted(column, settings.escape)
    if settings.quote_all:
        return quoted
    triggers, check_lead = _quote_triggers(
        settings.sep, settings.line_sep, escape_quotes=settings.escape_quotes
    )
    needs = None
    if triggers:
        needs = contains(column, lit(triggers[0]))
        for piece in triggers[1:]:
            needs = needs | contains(column, lit(piece))
    # Univocity quotes a value that starts with the quote char even when
    # escapeQuotes is false. Without this, partitionBy peels "w" down to w.
    if check_lead:
        lead = startswith(column, lit(_QUOTE))
        needs = lead if needs is None else needs | lead
    if needs is None:
        return column
    return iff(needs, quoted, column)


def _datetime_charset(fmt: str) -> set[str]:
    """Characters a Java datetime format can emit. Pattern letters expand."""
    chars: set[str] = set()
    letters = set("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz")
    digits = set("0123456789")
    i = 0
    n = len(fmt)
    while i < n:
        ch = fmt[i]
        if ch == "'":
            i += 1
            while i < n:
                if fmt[i] == "'":
                    if i + 1 < n and fmt[i + 1] == "'":
                        chars.add("'")
                        i += 2
                        continue
                    i += 1
                    break
                chars.add(fmt[i])
                i += 1
            continue
        if ch.isalpha():
            j = i + 1
            while j < n and fmt[j] == ch:
                j += 1
            count = j - i
            if ch in ("M", "L") and count >= 3:
                chars.update(letters)
            elif ch in ("E", "G", "a", "z"):
                chars.update(letters)
            elif ch in ("Z", "X", "x"):
                chars.update(digits)
                chars.update("+-:Z")
            else:
                chars.update(digits)
            i = j
            continue
        chars.add(ch)
        i += 1
    return chars


def _java_datetime_format(options: dict | None, kind: str) -> str:
    # The defaults are CsvWriterConfig's, which COPY uses for unquoted cells.
    # Spark's timestampFormat is the default only with writeSparkTimestampFormat.
    if kind == "date":
        return _last_option(options, "dateformat", "yyyy-MM-dd")
    default = (
        SPARK_CSV_WRITE_TIMESTAMP_FORMAT
        if is_csv_write_spark_timestamp_format_enabled()
        else CSV_READ_DEFAULT_CONFIG["timestampformat"]
    )
    return _last_option(options, "timestampformat", default)


def _rendered_charset(datatype: object, options: dict | None) -> set[str] | None:
    """Characters this column's CSV text can contain, or None to leave it native."""
    if isinstance(datatype, DateType):
        return _datetime_charset(_java_datetime_format(options, "date"))
    if isinstance(datatype, TimestampType):
        return _datetime_charset(_java_datetime_format(options, "timestamp"))
    if isinstance(datatype, TimeType):
        return _datetime_charset("HH:mm:ss")
    if isinstance(datatype, BooleanType):
        return set("truefals")
    if isinstance(datatype, (FloatType, DoubleType)):
        return set("0123456789.+-eENaIfinty")
    if isinstance(datatype, DecimalType):
        chars = set("0123456789-")
        scale = getattr(datatype, "scale", None)
        if scale is None or scale != 0:
            chars.add(".")
        return chars
    if isinstance(datatype, (ByteType, ShortType, IntegerType, LongType)):
        return set("0123456789-")
    if isinstance(datatype, BinaryType):
        # COPY BINARY_FORMAT=HEX. A separator that is a hex digit splits the
        # field once ESCAPE is gone.
        return set("0123456789ABCDEFabcdef")
    return None


def _structured_csv_text(datatype: object) -> bool:
    """Array, map, struct, and variant text can contain the separator.

    COPY cannot union those types with a header string, and dropping ESCAPE
    lets a comma inside the text split the row. Render them to varchar first.
    """
    return isinstance(datatype, (ArrayType, MapType, StructType, VariantType))


def _rendered_text_can_split(
    datatype: object, options: dict | None, settings: _QuoteSettings
) -> bool:
    return _charset_can_split(_rendered_charset(datatype, options), settings)


def _charset_can_split(charset: set[str] | None, settings: _QuoteSettings) -> bool:
    if not charset:
        return False
    return any(
        piece and all(ch in charset for ch in piece)
        for piece in _triggers(settings.sep, _QUOTE, settings.line_sep)
    )


def _csv_text(datatype: object, column: Column, options: dict | None) -> Column:
    """Render a non-string the way COPY would, so quoting sees that text.

    FLOAT and DOUBLE use ``TO_CHAR``, which is the text COPY unloads for an
    unquoted cell (``1.5``, ``53``, ``1e+20``, ``NaN``, ``inf``), so quoting does
    not change the value. Spark's ``Double.toString`` text (``53.0``,
    ``1.0E20``) comes from the opt-in ``writeJavaFloatingFormat`` (default
    off); with it on, the float reaches this pass as a string and is quoted
    from that text.
    """
    if isinstance(datatype, DateType):
        fmt = convert_java_datetime_format_for_fileformat(
            _java_datetime_format(options, "date")
        )
        return to_char(column, fmt)
    if isinstance(datatype, TimestampType):
        fmt = convert_java_datetime_format_for_fileformat(
            _java_datetime_format(options, "timestamp")
        )
        return to_char(column, fmt)
    if isinstance(datatype, TimeType):
        return to_char(column, "HH24:MI:SS")
    if isinstance(datatype, BooleanType):
        return iff(column, lit("true"), lit("false"))
    if isinstance(datatype, BinaryType):
        # Emits TO_CHAR(col, 'HEX'), which matches COPY BINARY_FORMAT=HEX.
        return to_varchar(column, "HEX")
    return to_char(column)


def _structured_cell_text(field_name: str) -> Column:
    """Varchar text of an array, map, struct, or variant cell.

    ``CAST(array AS STRING)`` is rewritten to a ``VARCHAR`` that ``TO_VARCHAR``
    rejects (001007). ``TO_VARCHAR(TO_VARIANT(col))`` is the form Snowflake
    accepts for array, map, typed object, and variant.
    """
    ident = quote_name_without_upper_casing(unquote_if_quoted(field_name))
    return sql_expr(f"TO_VARCHAR(TO_VARIANT({ident}))")


def quote_csv_string_cells(
    fields: list[StructField],
    columns: list[Column],
    options: dict | None,
    empty_value: str | None,
    rendered_text: dict[int, tuple[Column, str]] | None = None,
) -> list[Column]:
    """Replace projection entries whose CSV text Spark would quote.

    ``fields`` and ``columns`` line up one to one. A string entry becomes one
    expression over the source column: ``''`` writes the empty token (the
    caller's ``emptyValue`` is quoted when it needs it; the default ``""`` is
    already Spark's text), other text goes through
    :func:`minimal_quote_column`. Building it from the source column keeps the
    projection one ``SELECT`` deep. A non-string is rendered and quoted when
    ``quoteAll`` is set, when it is an array, map, struct, or variant, or when
    its text can contain the separator, the quote, CR, LF, or lineSep.

    ``rendered_text`` maps a field index to text the caller already projected
    and the Java format that text follows. With writeSparkTimestampFormat on,
    ``rewrite_df`` passes its TIMESTAMP_NTZ ``TO_CHAR`` text here, which is
    authoritative (format, partition and empty-format cases). That entry is
    quoted as text, not rendered again: wrapping the aliased projection would
    put ``AS`` inside a function call. With the flag off, NTZ stays a timestamp
    and is rendered in timestampFormat like LTZ, as COPY's TIMESTAMP_FORMAT is.
    """
    settings = _quote_settings(options)
    token = _DEFAULT_EMPTY_FILE_TOKEN if empty_value is None else empty_value
    file_token = quote_text_after_empty_substitution(token, **settings._asdict())
    projected = list(columns)
    for index, field in enumerate(fields):
        if rendered_text and index in rendered_text:
            text, java_format = rendered_text[index]
            if settings.quote_all or _charset_can_split(
                _datetime_charset(java_format), settings
            ):
                projected[index] = _minimal_quote(text, settings).alias(field.name)
            continue
        if isinstance(field.datatype, StringType):
            source = col(field.name)
            projected[index] = iff(
                source == lit(""),
                lit(file_token),
                _minimal_quote(source, settings),
            ).alias(field.name)
            continue
        if _structured_csv_text(field.datatype):
            projected[index] = _minimal_quote(
                _structured_cell_text(field.name), settings
            ).alias(field.name)
            continue
        if settings.quote_all or _rendered_text_can_split(
            field.datatype, options, settings
        ):
            rendered = _csv_text(field.datatype, columns[index], options)
            projected[index] = _minimal_quote(rendered, settings).alias(field.name)
    return projected


def quote_text_after_empty_substitution(
    value: str | None,
    *,
    sep: str = ",",
    escape: str = "\\",
    line_sep: str = "\n",
    quote: str = _QUOTE,
    quote_all: bool = False,
    escape_quotes: bool = True,
) -> str | None:
    """Quote a cell after ``''`` has already been replaced.

    The default replacement is the two-character token ``""``. That token
    already contains a quote; wrapping it again writes ``"\\"\\""``. A caller
    token such as ``A,B`` is quoted here.
    """
    if value == _DEFAULT_EMPTY_FILE_TOKEN:
        return value
    return minimal_quote_text(
        value,
        sep=sep,
        escape=escape,
        line_sep=line_sep,
        quote=quote,
        quote_all=quote_all,
        escape_quotes=escape_quotes,
    )


def peel_partition_text(
    value: str | None, *, escape: str = "\\", quote: str = _QUOTE
) -> str | None:
    """Undo one round of :func:`minimal_quote_text` for a directory key.

    The default empty-string file token ``""`` is not a quoted field. Peeling
    it yields an empty segment (``s=``), which is a prefix of every other
    key. Return ``None`` so the directory stays ``__HIVE_DEFAULT_PARTITION__``.
    Escape pairs are undone in the order the writer applied them: the quote
    escape first, then a doubled escape character. ``escape='"'`` only
    undoubles quotes.
    """
    if value is None or value == _DEFAULT_EMPTY_FILE_TOKEN:
        return None
    if len(value) >= 2 and value.startswith(quote) and value.endswith(quote):
        interior = value[1:-1]
        if escape:
            if escape == quote:
                interior = interior.replace(quote + quote, quote)
            else:
                interior = interior.replace(escape + quote, quote)
                interior = interior.replace(escape + escape, escape)
        return interior
    return value


def _sql_chars(text: str) -> str:
    return " || ".join(f"CHR({ord(ch)})" for ch in text)


def _unescape_partition_sql(interior: str, escape: str) -> str:
    """SQL twin of the replacements in :func:`peel_partition_text`."""
    quote = "CHR(34)"
    if not escape:
        return interior
    if escape == _QUOTE:
        return f"REPLACE({interior}, {quote} || {quote}, {quote})"
    escaped = _sql_chars(escape)
    return (
        f"REPLACE(REPLACE({interior}, {escaped} || {quote}, {quote}), "
        f"{escaped} || {escaped}, {escaped})"
    )


def resolved_csv_escape(options: dict | None) -> str:
    """Escape character after Spark's translation. Parsed once per write."""
    _, escape, _ = _resolved_quote_pieces(options)
    return escape


def csv_partition_directory_expr(
    column_name: str,
    *,
    peel_quotes: bool,
    options: dict | None = None,
    identifier: str | None = None,
    escape: str | None = None,
) -> str:
    """SQL for one ``col=value`` directory segment.

    The file cell is the quoted projection, so a comma in the key does not
    split the row. ``partitionBy`` has to use the text from before that
    quoting. The empty token ``""`` and SQL null both become
    ``__HIVE_DEFAULT_PARTITION__``. ``identifier`` is the column's SQL name
    when :func:`quote_csv_header_names` renamed it.
    """
    value = csv_partition_key_text_sql(
        column_name,
        peel_quotes=peel_quotes,
        options=options,
        identifier=identifier,
        escape=escape,
    )
    return f"'{column_name}=' || COALESCE({value}, '__HIVE_DEFAULT_PARTITION__')"


def csv_partition_key_text_sql(
    column_name: str,
    *,
    peel_quotes: bool,
    options: dict | None = None,
    identifier: str | None = None,
    escape: str | None = None,
) -> str:
    """The key text of a directory segment: the file cell with quoting undone.

    NULL for SQL null and for the empty token ``""``. A caller that parses the
    text further (TIMESTAMP_NTZ partition keys) wraps this expression.
    """
    quoted = identifier or f'"{column_name}"'
    text = f"TO_VARCHAR({quoted})"
    if not peel_quotes:
        return text
    if escape is None:
        escape = resolved_csv_escape(options)
    interior = f"SUBSTRING({text}, 2, LENGTH({text}) - 2)"
    raw = _unescape_partition_sql(interior, escape)
    empty = "CHR(34) || CHR(34)"
    return (
        f"IFF({text} = {empty}, NULL, "
        f"IFF(STARTSWITH({text}, CHR(34)) AND ENDSWITH({text}, CHR(34)) "
        f"AND LENGTH({text}) >= 2, {raw}, {text}))"
    )


def adjust_csv_unload_for_minimal_quoting(
    format_options: dict, options: dict | None
) -> None:
    """Stop COPY from escaping the quotes this module already wrote.

    ``ESCAPE='\\'`` plus ``ESCAPE_UNENCLOSED_FIELD='NONE'`` still rewrites a
    comma to ``\\,`` because the field is not enclosed. Drop ``escape``.
    NULL is left to ``get_param_from_options`` and
    ``settle_unenclosed_null_token``: with ``writeNullAsEmpty`` this path gets
    SNOW-4209027's ``NULL_IF=''`` unless the caller set ``nullValue``; without
    it Snowflake's default ``\\N`` is unloaded unescaped.
    """
    format_options.pop("escape", None)
    format_options.pop("ESCAPE", None)


def settle_unenclosed_null_token(format_options: dict, options: dict | None) -> None:
    """Make the NULL file token unloadable once enclosure and ``ESCAPE`` are gone.

    Call this after ``get_param_from_options`` returns. ``NULL_IF=''`` without
    ``FIELD_OPTIONALLY_ENCLOSED_BY`` unloads only with
    ``EMPTY_FIELD_AS_NULL=FALSE`` (error 100093 otherwise), so set that and
    keep the bare empty field, which is Spark's NULL. That is the SNOW-4209027
    default and an explicit ``nullValue=""``. A non-empty caller ``nullValue``
    wins, quoted the way Spark quotes it when it contains the delimiter or a
    quote (``"a,b"``). Without ``ESCAPE`` the unload writes the token as given,
    so it is passed as a SQL string literal: ``nullValue='\\N'`` writes
    ``\\N``, as Spark does, not ``N``. Under ``legacyNullIfToken`` (default)
    a token whose raw and exact forms differ is sent raw and unquoted, as
    earlier releases did, so ``nullValue='\\N'`` keeps writing ``N``.
    """
    enclosed = format_options.get(
        "FIELD_OPTIONALLY_ENCLOSED_BY", format_options.get("quote")
    )
    if enclosed not in (None, "", "NONE"):
        return
    format_options.pop("escape", None)
    format_options.pop("ESCAPE", None)
    null_if = format_options.get("NULL_IF")
    if null_if == "":
        format_options["EMPTY_FIELD_AS_NULL"] = False
        return
    null_value = _last_option(options, "nullvalue", "")
    if _has_option(options, "nullvalue") and null_value != "":
        if csv_null_if_token(null_value) != csv_null_if_sql_literal(null_value):
            format_options["NULL_IF"] = null_value
            return
        sep, escape, line_sep = _resolved_quote_pieces(options)
        quote_all, escape_quotes = _quote_mode(options)
        quoted = minimal_quote_text(
            null_value,
            sep=sep,
            escape=escape,
            line_sep=line_sep,
            quote_all=quote_all,
            escape_quotes=escape_quotes,
        )
        format_options["NULL_IF"] = csv_null_if_sql_literal(quoted)


def quote_csv_header_names(
    df: DataFrame, options: dict | None, column_names: list[str] | None = None
) -> tuple[DataFrame, dict[str, str]]:
    """Alias columns whose header name contains the delimiter or a line break.

    With ``quoteAll`` every name is quoted, as Spark does.

    COPY prints each column name as the header and does not enclose it on this
    path, so ``a,b`` would split the header. The alias is Spark's quoted text,
    e.g. ``"a,b"``. A name whose only special character is ``"`` stays as is:
    unquoted it reads back on both engines, while the SCOS reader cannot infer
    a header that holds an escaped quote. For the same reason headers ignore
    ``escapeQuotes``: with ``escapeQuotes=false`` a name that needs quoting and
    starts with ``"`` is still written with the quote escaped. Returns the renamed frame and a map
    from the unquoted name to the new SQL identifier, for ``partitionBy``.
    Pass ``column_names`` when they are already known, to skip a describe.
    """
    sep, escape, line_sep = _resolved_quote_pieces(options)
    quote_all, _ = _quote_mode(options)
    splitters = [piece for piece in (sep, "\n", "\r", line_sep) if piece]
    renamed: dict[str, str] = {}
    projected: list[Column] = []
    for name in df.columns if column_names is None else column_names:
        raw = unquote_if_quoted(name)
        if not quote_all and not any(piece in raw for piece in splitters):
            projected.append(col(name))
            continue
        header = minimal_quote_text(
            raw, sep=sep, escape=escape, line_sep=line_sep, quote_all=quote_all
        )
        identifier = quote_name_without_upper_casing(header)
        renamed[raw] = identifier
        projected.append(col(name).alias(identifier))
    if not renamed:
        return df, renamed
    return df.select(projected), renamed
