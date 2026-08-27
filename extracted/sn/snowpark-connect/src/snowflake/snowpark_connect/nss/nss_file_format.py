#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

"""Session-local temp FILE FORMAT for the ``STAGE_FILE_READER`` / ``INFER_STAGE_FILE_SCHEMA``
TVF path.

``STAGE_FILE_READER`` takes a ``FILE_FORMAT`` by name; the FILE FORMAT is consumed by the
TVF (at compile) and the XP external scanner (at read) — **not** by the sandbox Spark
reader, which decodes from ``READER_OPTIONS``. So the format only needs the stage/scanner
concerns: the file *type*, ``COMPRESSION``, ``MULTI_LINE``, and (CSV only)
``RECORD_DELIMITER``. Decoding options (field delimiters, mode, timestamp formats, …) are
intentionally omitted to avoid conflicting with the Spark reader options (see plan Q4) —
the clauses here are on the format because GS *reads them for splitability*, not because
the scanner decodes with them.

``COMPRESSION`` belongs on the format because the scanner splits files into byte chunks
*before* the sandbox sees them — a compressed stream cannot be decoded from an arbitrary
mid-file chunk, so the codec must be resolved at the scanner level. ``AUTO`` (the default)
detects the codec from the file extension, matching Spark's own read-side behavior.

``COMPRESSION``, ``MULTI_LINE``, and ``RECORD_DELIMITER`` are also *byte-range
parallel-scan eligibility* inputs, not just decoding concerns: GS decides splitability
from the FILE FORMAT's **declared** clauses, never from what the sandbox actually does at
read time (``ExternalScanInputMeta.getFileSplitabilityFor{Json,Csv}ParallelScan``).

* ``MULTI_LINE`` must be *explicitly* ``FALSE``. Snowflake defaults it to ``TRUE``, and an
  unset value reads as "not line-delimited, not eligible" for **both** JSON and CSV. Spark
  itself defaults ``multiLine`` to ``false``, so mirroring the caller's
  ``.option("multiLine", ...)`` onto the format both matches Spark semantics and unlocks
  eligibility for the common line-delimited case. A caller with genuinely
  pretty-printed/multi-line input sets ``.option("multiLine", "true")``, which correctly
  opts back out.
* ``COMPRESSION`` must be ``NONE`` to be unconditionally splittable. ``AUTO`` is splittable
  only where the ``ENABLE_PSCAN_AUTO_COMPRESSION_INFERENCE`` param is enabled (SNOW-3379656
  moved the decision to a per-file extension check, backed by an XP magic-byte safety net);
  where it is off, ``AUTO`` on a genuinely uncompressed dataset is *not* eligible even
  though the bytes would qualify, and such a caller can opt in with
  ``.option("compression", "none")``.
* ``RECORD_DELIMITER`` (CSV only) must match the caller's ``.option("lineSep", ...)``.
  ``getFileSplitabilityForCsvParallelScan`` reads the *declared* delimiter to place chunk
  boundaries, while ``lineSep`` reaches the sandbox reader through ``READER_OPTIONS``
  (``nss_scan_options._SPARK_CSV_READ_OPTIONS``). Leaving the clause unset makes the
  format carry Snowflake's default ``'\\n'``, so a custom-``lineSep`` read would have GS
  splitting on newline while the sandbox parses on the caller's separator — tearing
  records in half across the split, silently (a fragment's short token count is invisible
  under column pruning, and is merely reported as malformed without it). Declaring it
  keeps the two in step, and lets GS decline on its own terms via
  ``isFirstByteOfRecordDelimiterRepeated`` for separators it cannot chunk. JSON has no
  such property (NDJSON is newline-delimited by definition and
  ``getFileSplitabilityForJsonParallelScan`` has no ``RECORD_DELIMITER`` arm), so the
  clause is emitted for CSV only.

All three are resolved from the read's options by :func:`resolve_nss_compression_option`,
:func:`resolve_nss_multiline_option`, and :func:`resolve_nss_record_delimiter_option`, and
threaded through by the JSON/CSV NSS read branches.

None of this is observable on a local reg: both splitability helpers return
``NOT_SPLITTABLE`` for ``StorageType.LOCAL_FS`` (SNOW-1632351) before any clause is
examined, so a local run never splits regardless of what is declared.
"""

from snowflake import snowpark
from snowflake.snowpark_connect.error.error_codes import ErrorCodes
from snowflake.snowpark_connect.error.error_utils import attach_custom_error_code
from snowflake.snowpark_connect.relation.io_utils import (
    get_compression_for_source_and_options,
)
from snowflake.snowpark_connect.utils.snowpark_connect_logging import logger

_SF_FILE_TYPE = {"json": "JSON", "csv": "CSV"}

_TRUE_VALUES = frozenset({"true", "1"})
_FALSE_VALUES = frozenset({"false", "0", ""})


def resolve_nss_compression_option(reader_options: dict, fmt: str) -> str:
    """Resolve the caller's ``.option("compression", ...)`` to a FILE FORMAT
    ``COMPRESSION`` value for an NSS read.

    Delegates spelling, aliasing, and validation to
    :func:`~snowflake.snowpark_connect.relation.io_utils.get_compression_for_source_and_options`,
    the same helper the COPY read path uses — so ``uncompressed``/``bzip2`` normalize to
    ``NONE``/``BZ2`` and an unsupported codec raises the identical ``AnalysisException``
    on both paths, rather than NSS keeping a second allowlist that can drift.

    Note that a caller who declares ``NONE`` over data that *is* compressed makes the
    file splittable, which yields wrong rows rather than an error — the declared codec is
    taken at face value by the scanner.

    Args:
        reader_options: The read's ``options.config`` (Spark ``.option()`` values,
            lower-cased keys). ``compression`` is always present: ``map_read`` seeds the
            SCOS default and ``_resolve_read_compression`` may have already replaced it
            with a codec inferred from the file extensions.
        fmt: ``"json"`` or ``"csv"``.

    Returns:
        A Snowflake ``COMPRESSION`` value, upper-cased; ``"AUTO"`` when unset.
    """
    return (
        get_compression_for_source_and_options(fmt, reader_options, from_read=True)
        or "AUTO"
    )


def resolve_nss_multiline_option(reader_options: dict) -> str:
    """Resolve the caller's ``.option("multiLine", ...)`` to a FILE FORMAT ``MULTI_LINE``
    value for an NSS read.

    Defaults to ``"FALSE"``, matching Spark's own ``multiLine`` default (line-delimited)
    — a behavior *fix*, not just an opt-in, since Snowflake's own FILE FORMAT default is
    ``TRUE``. Non-boolean values raise: Spark parses this option with
    ``parameters.get("multiLine").map(_.toBoolean)`` in both ``JSONOptions`` and
    ``CSVOptions``, which throws, and SCOS's own ``str_to_bool`` rejects them on the COPY
    path. Coercing them to ``FALSE`` instead would silently declare a multi-line file
    splittable.

    Args:
        reader_options: The read's ``options.config`` (Spark ``.option()`` values,
            lower-cased keys).

    Returns:
        ``"TRUE"`` or ``"FALSE"``.
    """
    raw = reader_options.get("multiline", "false")
    value = str(raw).strip().lower()
    if value in _TRUE_VALUES:
        return "TRUE"
    if value in _FALSE_VALUES:
        return "FALSE"
    exception = ValueError(
        f"Invalid .option('multiLine', {raw!r}): expected a boolean value."
    )
    attach_custom_error_code(exception, ErrorCodes.INVALID_CONFIG_VALUE)
    raise exception


def resolve_nss_record_delimiter_option(
    reader_options: dict, user_option_keys: frozenset[str] | None
) -> str | None:
    """Resolve the caller's ``.option("lineSep", ...)`` to a CSV FILE FORMAT
    ``RECORD_DELIMITER`` value for an NSS read, or ``None`` to leave the clause unset.

    Returns ``None`` unless the caller actually passed ``lineSep``: SCOS seeds a
    ``"lineSep": "\\n"`` CSV default (``reader_config``) that
    ``nss_scan_options._CSV_DEFAULTS_CONTRADICTING_SPARK`` deliberately withholds from the
    sandbox, because Spark auto-detects ``\\r\\n``/``\\n``/``\\r`` when the option is
    absent. Declaring that leaked default would pin the format to ``'\\n'`` — which is
    already Snowflake's default, so omitting the clause keeps today's behavior for every
    read that does not ask for a separator.

    Escape sequences are translated with the COPY path's own
    ``reader_config.translate_csv_escape_literal`` (Spark's ``CSVExprUtils.toDelimiterStr``),
    so ``.option("lineSep", "\\t")`` — two characters on the wire — declares a real tab on
    both paths rather than a backslash followed by ``t``.

    No length or content validation is applied. Spark's own ``CSVOptions`` rejects an empty
    or over-long ``lineSep`` in the sandbox, and GS declines to chunk a separator it cannot
    place boundaries for (``isFirstByteOfRecordDelimiterRepeated``), so adding a third
    gate here could only reject reads that work today.

    Args:
        reader_options: The read's ``options.config`` (Spark ``.option()`` values,
            lower-cased keys).
        user_option_keys: Lower-cased keys the caller actually set
            (``ReaderWriterConfig.user_option_keys``). ``None`` — no provenance available —
            is treated as "not set", keeping the clause off rather than declaring a value
            that may be a SCOS default.

    Returns:
        The record delimiter to declare, or ``None`` to omit the clause.
    """
    if not user_option_keys or "linesep" not in user_option_keys:
        return None
    raw = reader_options.get("linesep")
    if raw is None or raw == "":
        return None
    from snowflake.snowpark_connect.relation.read.reader_config import (
        translate_csv_escape_literal,
    )

    return translate_csv_escape_literal(str(raw))


def _sql_escape_delimiter(value: str) -> str:
    """Escape ``value`` for the body of a single-quoted Snowflake string literal.

    Backslashes are doubled first, mirroring the COPY path's delimiter encoding
    (SNOW-3245108 / SNOW-3389608) — Snowflake unescapes ``\\`` inside the literal, so a
    separator containing one must arrive doubled to survive. Quote escaping runs *after*,
    via :func:`~snowflake.snowpark_connect.nss.nss_scan_options.sql_quote_literal`; doing it
    first would leave the ``\\`` it introduces to be doubled into a literal backslash and
    break out of the string.
    """
    from snowflake.snowpark_connect.nss.nss_scan_options import sql_quote_literal

    return sql_quote_literal(value.replace("\\", "\\\\"))


def _record_delimiter_token(record_delimiter: str | None) -> str:
    """Identifier-safe, collision-free encoding of ``record_delimiter`` for the format name.

    Hex of the UTF-8 bytes (``"|"`` -> ``RD7C``, ``"\\r\\n"`` -> ``RD0D0A``): the delimiter
    itself cannot go in an identifier, and a lossy token (e.g. a length) would let two
    different separators share one cached format.
    """
    if record_delimiter is None:
        return ""
    return "_RD" + record_delimiter.encode("utf-8").hex().upper()


def _format_name(
    fmt: str,
    compression: str,
    multi_line: str = "FALSE",
    record_delimiter: str | None = None,
) -> str:
    """Deterministic temp-format name per (type, compression, multi_line, record_delimiter).

    ``AUTO`` compression, ``MULTI_LINE = FALSE``, and an unset ``RECORD_DELIMITER`` keep the
    base name (``SNOWPARK_CONNECT_NSS_JSON_FF``); anything else gets its own object
    (``..._JSON_GZIP_MULTILINE_FF``, ``..._CSV_RD7C_FF``) so a cached format is never reused
    for a read that declared different clauses. Every clause that
    ``ensure_nss_temp_file_format`` emits must appear here, or ``CREATE ... IF NOT EXISTS``
    silently keeps the first read's format and the second read's options are dropped.
    """
    comp = compression.upper()
    suffix = "" if comp == "AUTO" else f"_{comp}"
    if multi_line.upper() == "TRUE":
        suffix += "_MULTILINE"
    suffix += _record_delimiter_token(record_delimiter)
    return f"SNOWPARK_CONNECT_NSS_{fmt.upper()}{suffix}_FF"


def ensure_nss_temp_file_format(
    session: snowpark.Session,
    fmt: str,
    compression: str = "AUTO",
    multi_line: str = "FALSE",
    record_delimiter: str | None = None,
) -> str:
    """Ensure a session-local temp FILE FORMAT for
    ``(fmt, compression, multi_line, record_delimiter)`` exists and return its name.

    The format is identical across reads with the same clauses, so it is created **once per
    session**: the name is cached on the session object and the ``CREATE`` (guarded by
    ``IF NOT EXISTS``) is issued only on first use, avoiding a DDL round-trip per read.

    Args:
        session: Active Snowpark session.
        fmt: ``"json"`` or ``"csv"``.
        compression: Snowflake ``COMPRESSION`` value (``AUTO`` by default; e.g. ``GZIP``,
            ``BZ2``, ``NONE``). ``AUTO`` detects the codec from the file extension.
        multi_line: Snowflake ``MULTI_LINE`` value (``"FALSE"`` by default, matching
            Spark's own ``multiLine`` default). Applies to both JSON and CSV.
        record_delimiter: Snowflake ``RECORD_DELIMITER`` value, or ``None`` (default) to
            omit the clause and keep Snowflake's ``'\\n'``. **CSV only** — a JSON FILE
            FORMAT has no such property, so a value passed with ``fmt="json"`` is ignored
            rather than producing invalid DDL.

    Returns:
        The temp FILE FORMAT name to pass as ``FILE_FORMAT``.
    """
    key = fmt.lower()
    sf_type = _SF_FILE_TYPE[key]
    comp = compression.upper()
    ml = multi_line.upper()
    rd = record_delimiter if key == "csv" else None
    name = _format_name(key, comp, ml, rd)

    # The cache check-then-create below is not locked. Two concurrent requests on
    # the same session could both issue the CREATE for the same format name — benign,
    # since the DDL is guarded by ``IF NOT EXISTS`` (a race causes at most redundant,
    # never conflicting, DDL). A lock would add lifecycle concerns for no correctness
    # gain.
    created = getattr(session, "_nss_temp_file_formats", None)
    if created is None:
        created = set()
        session._nss_temp_file_formats = created
    if name in created:
        return name

    sql = (
        f"CREATE TEMP FILE FORMAT IF NOT EXISTS {name} "
        f"TYPE = {sf_type} COMPRESSION = {comp} MULTI_LINE = {ml}"
    )
    if rd is not None:
        sql += f" RECORD_DELIMITER = '{_sql_escape_delimiter(rd)}'"
    # NSS read path: internal temp-FILE-FORMAT DDL. Keep the log, but keep the "NSS"
    # keyword out of the customer-visible message (reviewer request).
    logger.info(f"ensuring temp FILE FORMAT: {sql}")
    session.sql(sql).collect()
    created.add(name)
    return name
