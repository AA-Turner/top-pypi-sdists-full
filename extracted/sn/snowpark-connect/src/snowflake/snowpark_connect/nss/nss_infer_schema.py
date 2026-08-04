#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

"""Schema inference for the NSS read path via the official ``INFER_STAGE_FILE_SCHEMA`` TVF.

A schema-less file read needs a Spark schema up front (to build ``DATA_SCHEMA`` for
``STAGE_FILE_READER``). We infer it with Spark's *own* inference (via the TVF) rather than
Snowflake's ``INFER_SCHEMA`` — so the inferred types match exactly what the sandbox Spark
reader produces. The per-file inference + cross-file merge happen inside the TVF
(SNOW-3715056), so there is no manual aggregate / ``GROUP BY``.

The TVF's ``SPARK_TYPE`` (Spark ``DataType.json()``) is carried through **verbatim** as each
column's ``SPARK_DATA_TYPE`` — SCOS does not re-derive it or round-trip it through an
intermediate ``StructType``.
"""

import json

from snowflake import snowpark
from snowflake.snowpark_connect.nss.nss_scan_options import (
    NssColumn,
    _stringify_reader_option,
    build_spark_conf,
    quote_options_literal,
    sql_quote_literal,
)
from snowflake.snowpark_connect.utils.snowpark_connect_logging import logger


def infer_via_stage_file_schema(
    session: snowpark.Session,
    stage_path: str,
    file_format: str,
    infer_fqn: str = "INFER_STAGE_FILE_SCHEMA",
    multiline: str = "false",
    sampling_ratio: str = "1",
    mode: str = "PERMISSIVE",
    corrupt_record_column: str = "_corrupt_record",
    reader_options: dict | None = None,
    spark_conf: dict | None = None,
) -> list[NssColumn]:
    """Infer the column list via the official ``INFER_STAGE_FILE_SCHEMA`` TVF.

    Contract (SNOW-3715056): named args ``LOCATION`` / ``FILE_FORMAT`` / ``OPTIONS_JSON``
    (top-level ``sparkConf`` / ``readerOptions``, matched case-insensitively); output is one
    row per column ``(COLUMN_NAME, SPARK_TYPE, NULLABLE, ORDER_ID)`` sorted by ``ORDER_ID``.
    ``SPARK_TYPE`` (Spark ``DataType.json()``) is carried through verbatim. RAISES on empty
    rather than falling back to COPY, so NSS gaps surface in tests.
    """
    # Forward the caller's format reader options so inference splits/labels columns exactly
    # as the read will. For CSV this is essential: header/sep/delimiter/quote/escape drive
    # column detection — Spark's CSVInferSchema honors them (native-spark-sandbox-extensions
    # fileformat-csv README). Without them a non-default separator infers a single column
    # (later COLUMN_NOT_FOUND) and header rows leak into the data.
    reader_opts = {
        str(k): _stringify_reader_option(v) for k, v in (reader_options or {}).items()
    }
    lower = {k.lower(): k for k in reader_opts}
    # samplingRatio must be a JSON *number* in (0, 1] for GS
    # (InferStageFileSchemaImpl.validateReaderOptions -> value.isNumber()); a JSON string is
    # rejected at compile time. Honor the caller's option if set (CSV forwards it via
    # reader_options, JSON via the sampling_ratio arg), else full-sample.
    # TODO(SNOW-3717231): the JSON schema-less path forwards samplingRatio/multiLine/mode but
    # not its other JSONOptions (primitivesAsString, prefersDecimal, ...); explicit-schema
    # reads skip inference entirely. Forward the remaining JSON options for full parity.
    sampling_key = lower.get("samplingratio")
    sampling = reader_opts.pop(sampling_key) if sampling_key else sampling_ratio
    reader_opts["samplingRatio"] = float(sampling)
    # Set the infer defaults only when the caller didn't already supply them (case-insensitive),
    # so we never emit duplicate multiline/mode/... keys.
    if "multiline" not in lower:
        reader_opts["multiLine"] = multiline
    if "mode" not in lower:
        reader_opts["mode"] = mode
    if corrupt_record_column and "columnnameofcorruptrecord" not in lower:
        reader_opts["columnNameOfCorruptRecord"] = corrupt_record_column
    # Forward the same decoding-relevant spark.sql.* confs the read path sends (SPARK_CONF).
    # Chiefly spark.sql.timestampType: without it the sandbox infers TIMESTAMP_NTZ columns as
    # LTZ (SNOW-3861942) — the read path already forwards it, so inference must match or the
    # inferred DATA_SCHEMA disagrees with the read. Also carries timeZone / ANSI / etc.
    conf = build_spark_conf() if spark_conf is None else spark_conf
    opts = json.dumps({"sparkConf": conf, "readerOptions": reader_opts})
    # Escape single quotes in the raw-interpolated literals so a path/format name
    # containing a ``'`` cannot break out of the SQL string. OPTIONS_JSON is wrapped by
    # quote_options_literal, which is safe even when the payload contains ``$$`` —
    # ``corrupt_record_column`` (user-controllable) or an inferred name can.
    # SELECT * — the TVF's fixed output schema is (COLUMN_NAME, SPARK_TYPE, NULLABLE,
    # ORDER_ID), matching the native-spark-sandbox-extensions README; ORDER BY ORDER_ID
    # yields file column order. Rows are read positionally below in that declared order.
    query = (
        f"SELECT * FROM TABLE({infer_fqn}(\n"
        f"    LOCATION     => '{sql_quote_literal(stage_path)}',\n"
        f"    FILE_FORMAT  => '{sql_quote_literal(file_format)}',\n"
        f"    OPTIONS_JSON => {quote_options_literal(opts)}\n"
        ")) ORDER BY ORDER_ID"
    )
    # NSS schema-inference path (keyword kept out of the customer-visible log message)
    logger.info(f"INFER_STAGE_FILE_SCHEMA query: {query}")
    rows = session.sql(query).collect()
    if not rows:
        raise ValueError(
            f"NSS INFER_STAGE_FILE_SCHEMA returned no rows for {stage_path}."
        )
    return [
        NssColumn(
            name=row[0],
            spark_type=row[1],
            nullable=bool(row[2]) if row[2] is not None else True,
        )
        for row in rows
    ]
