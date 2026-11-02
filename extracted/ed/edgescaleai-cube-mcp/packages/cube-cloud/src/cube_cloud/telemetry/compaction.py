"""Nightly compaction of raw per-call telemetry JSON into curated Parquet.

Runs as a scheduled Lambda (see infra/lambda/tool_call_compaction/). For a date
partition it:

  1. lists   s3://<bucket>/<raw_prefix>dt=<date>/*.json
  2. downloads + concatenates them into a local newline-delimited JSON file
  3. DuckDB reads the NDJSON and writes ONE Parquet file
  4. uploads  s3://<bucket>/<curated_prefix>dt=<date>/data.parquet

Compaction is purely additive — it does NOT delete raw. Raw is the recovery
source if a curated write is ever bad, and the S3 lifecycle rule
(telemetry_raw_retention_days) expires it well after it's been rolled up. At
~100 calls/day this yields one right-sized curated file per day (~365/year) — no
small-file problem. Idempotent: re-running a date re-reads raw and overwrites
the curated file; no raw objects → nothing to do.

The logic is injectable (s3 client + parquet writer) so it is unit-testable
without AWS or a Lambda runtime. DuckDB is imported lazily inside the writer so
the module imports fine where DuckDB isn't installed (e.g. the test env).
"""

from __future__ import annotations

import logging
import os
import tempfile
from datetime import datetime, timedelta, timezone
from typing import Any, Callable

logger = logging.getLogger(__name__)

# Columns withheld from the NARROW dataset — the free-text tier. Every dimension
# and every metric is kept, so a dashboard can still split by tool/profile/cube/
# actor and drill down to the individual call; what it cannot do is read the
# call's payload or the caller's IP.
#
# Why physically separate files rather than a narrower Glue table over the same
# ones: Athena reads S3 as the *calling* identity, so a principal that can query
# curated/ can equally point DuckDB at those Parquet files and read every column.
# A column subset in the catalog is a convenience, not a boundary. Splitting the
# data means IAM can grant s3:GetObject on narrow/ alone — and IAM has no
# column-level control, so this is the only mechanism that actually enforces it.
#
# `user_email_hash` is deliberately KEPT: it is a SHA-256, irreversible without
# the local-only lookup in scripts/export_key_identity.py, and it is what makes
# "distinct users" countable at all (key_id alone counts keys, and one person can
# hold several). `caller_ip` is dropped as personal data a usage dashboard has no
# need for; `error_message` is dropped as free text (its taxonomy survives as
# `error_class`).
NARROW_EXCLUDED_COLUMNS = frozenset({"args", "response", "error_message", "caller_ip"})

# Columns whose physical Parquet type is PINNED rather than inferred.
#
# read_json_auto infers types, and that inference is not stable across producer
# environments. In prod, `ts` silently flipped TIMESTAMP -> VARCHAR at
# dt=2026-07-15: the data either side is byte-uniform ISO-8601, so the cause is
# the compaction Lambda's floating duckdb pin (infra/lambda/.../build.sh), not the
# events. `union_by_name=true` then promotes the mixed union to VARCHAR instead of
# erroring, so a cross-day read still "worked" and nothing surfaced it — while a
# Glue column declared `timestamp` over VARCHAR files yields GARBAGE VALUES rather
# than an error. The failure mode this dataset specialises in.
#
# The same fragility is reproducible from data alone: a single row whose `ts`
# lacks microseconds (datetime.isoformat() omits them when microsecond == 0) is
# enough to flip an entire partition to VARCHAR. So inference must be removed
# from the equation, not merely version-pinned.
#
# `ts` is pinned to VARCHAR, NOT TIMESTAMP, on purpose:
#   * it is what is already on disk for every partition from 2026-07-15 onward,
#     so the catalog is honest immediately and does not depend on a backfill
#     landing first;
#   * TIMESTAMP inference was LOSSY — it parsed the event's tz-aware
#     `datetime.isoformat()` into a naive timestamp, dropping the +00:00;
#   * `ts_epoch_ms` (BIGINT) already provides a type-stable column for time
#     arithmetic, so nothing downstream needs `ts` to be a SQL timestamp.
#
# The VALUE FORMAT is normalised too, not just the type — see the `ts` branch in
# `_stable_projection`. An earlier version of this pin used a bare CAST, which
# rendered "2026-08-24 19:14:36.781555" on producers that parse the string into a
# TIMESTAMP (duckdb >=1.3) and passed the original ISO form through on those that
# do not (<=1.2.2). Same type, different format, changing at every producer
# boundary — observed live on the dev partition compacted right after the duckdb
# 1.5.5 rollout. Partitions written before that fix keep the space form until
# re-compacted; `ts_epoch_ms` was never affected.
_PINNED_COLUMN_TYPES = {"ts": "VARCHAR", "dt": "DATE"}


def default_date() -> str:
    """Yesterday (UTC) as YYYY-MM-DD — the partition a nightly run compacts."""
    return (datetime.now(timezone.utc) - timedelta(days=1)).strftime("%Y-%m-%d")


def list_raw_keys(s3: Any, bucket: str, prefix: str) -> list[str]:
    """All ``*.json`` keys under `prefix` (paginated)."""
    keys: list[str] = []
    paginator = s3.get_paginator("list_objects_v2")
    for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
        for obj in page.get("Contents", []):
            if obj["Key"].endswith(".json"):
                keys.append(obj["Key"])
    return keys


def _stable_projection(
    con: Any, source: str, *, exclude: frozenset[str] = frozenset()
) -> str:
    """Build a SELECT list that pins each column to a day-invariant type.

    ``read_json_auto`` infers types from *that day's* data, so the same column
    gets a DIFFERENT physical type across partitions — and a cross-day read
    (``read_parquet(dt=*, union_by_name=true)``) then fails, because union_by_name
    reconciles the column *set* (fills missing columns with NULL) but NOT
    conflicting *types*: it fixes the target type from the first file and casts
    the rest, which errors on any value that won't cast. Two drift patterns bite:

      * `args` (a free-form dict) infers to a ``STRUCT`` on a uniform-shape day
        (e.g. all build_image_* calls) and a ``MAP`` on a varied day → can't cast
        STRUCT -> MAP.
      * any nullable column (`cube`, `error_class`, `error_message`, …) infers to
        ``JSON`` on a day where every value is NULL (DuckDB's fallback for an
        all-null column) and to ``VARCHAR`` on a populated day → can't cast a bare
        string like "broker" as JSON.

    So: serialize `args` to JSON text, coerce any other JSON-typed column back to
    VARCHAR, and pass everything else through. This is a general rule (not a
    hardcoded copy of ``ToolCallEvent``), so it stays correct as the event schema
    grows and never DROPS a column. `response` is already a plain string.

    ``exclude`` is the one case where dropping a column is intended — it builds
    the payload-free narrow dataset (see ``NARROW_EXCLUDED_COLUMNS``). It is an
    allow-by-default filter, so a newly added event field flows into narrow
    automatically; a new *free-text* field must be added to the exclusion set
    (``test_compaction`` guards the known ones).
    """
    projection: list[str] = []
    for row in con.execute(f"DESCRIBE SELECT * FROM {source}").fetchall():
        name, col_type = row[0], row[1]
        if name in exclude:
            continue
        quoted = '"' + name.replace('"', '""') + '"'
        if name == "args":
            projection.append(f"to_json({quoted}) AS {quoted}")
        elif name == "ts":
            # Canonical ISO-8601 UTC, regardless of what inference did.
            #
            # A bare CAST is NOT enough. duckdb >=1.3 parses the event's
            # `datetime.isoformat()` string into a TIMESTAMP, which drops the
            # +00:00 offset; casting that back to text renders
            # "2026-08-24 19:14:36.781555" — a different VALUE FORMAT from the
            # passthrough on producers that infer VARCHAR (duckdb <=1.2.2). The
            # type would be stable but the format would change at every producer
            # boundary, which is a footgun for anything string-sorting `ts`.
            #
            # TRY_CAST + strftime normalises both paths to one FORMAT;
            # COALESCE falls back to the raw string if a value ever fails to
            # parse, so a malformed `ts` can never fail a whole day's compaction.
            #
            # It does NOT normalise the VALUE for a non-UTC offset: the
            # TIMESTAMP-inferred path converts to UTC while the VARCHAR-inferred
            # path keeps the wall clock and merely restamps it "+00:00" — two
            # different instants. Inert today because events.py always emits
            # +00:00 (`datetime.now(timezone.utc)`); if `ts` ever carries a real
            # local offset this must become a parse that respects it.
            projection.append(
                f"COALESCE(strftime(TRY_CAST({quoted} AS TIMESTAMP), "
                f"'%Y-%m-%dT%H:%M:%S.%f+00:00'), CAST({quoted} AS VARCHAR)) AS {quoted}"
            )
        elif name in _PINNED_COLUMN_TYPES:
            target = _PINNED_COLUMN_TYPES[name]
            if col_type == target:
                projection.append(quoted)
            else:
                # TRY_CAST, never CAST. A bare CAST makes ONE malformed value
                # abort write_parquet, which aborts compact_date, which means the
                # whole day's curated partition is never written — total loss of
                # a partition over a single bad row. Before pinning, `dt` was
                # passed through untouched and such a day compacted fine, so a
                # bare CAST here would be a hard-failure path this pin INTRODUCED.
                # TRY_CAST yields NULL for the bad value and keeps the day.
                # (For `dt` a NULL is harmless: Athena reads the partition value
                # from the S3 key and never looks at the in-file column.)
                projection.append(f"TRY_CAST({quoted} AS {target}) AS {quoted}")
        elif col_type == "JSON":
            projection.append(f"CAST({quoted} AS VARCHAR) AS {quoted}")
        else:
            projection.append(quoted)
    return ", ".join(projection)


def write_parquet(
    ndjson_path: str, parquet_path: str, *, exclude: frozenset[str] = frozenset()
) -> None:
    """Read newline-delimited JSON and write one zstd Parquet file via DuckDB.

    Column types are pinned to be day-invariant (see ``_stable_projection``) so
    the per-partition curated files union cleanly on a cross-day read. Pass
    ``exclude`` to omit columns (used for the narrow dataset).
    """
    import duckdb  # lazy: only present in the Lambda image

    # Paths are internal temp files, not user input — safe to inline.
    con = duckdb.connect()
    try:
        source = (
            f"read_json_auto('{ndjson_path}', "
            f"format='newline_delimited', union_by_name=true)"
        )
        projection = _stable_projection(con, source, exclude=exclude)
        con.execute(
            f"COPY (SELECT {projection} FROM {source}) "
            f"TO '{parquet_path}' (FORMAT parquet, COMPRESSION zstd)"
        )
    finally:
        con.close()


def write_narrow_parquet(ndjson_path: str, parquet_path: str) -> None:
    """``write_parquet`` with the free-text columns dropped.

    Separate named function (rather than a partial at the call site) so it can be
    injected in tests exactly like ``write_parquet``.
    """
    write_parquet(ndjson_path, parquet_path, exclude=NARROW_EXCLUDED_COLUMNS)


def compact_date(
    s3: Any,
    bucket: str,
    date: str,
    raw_prefix: str,
    curated_prefix: str,
    *,
    writer: Callable[[str, str], None] = write_parquet,
    narrow_prefix: str | None = None,
    narrow_writer: Callable[[str, str], None] = write_narrow_parquet,
) -> int:
    """Compact one date partition. Returns the number of raw objects rolled up.

    Purely additive: raw is left in place (recovery source; expired by the S3
    lifecycle rule), so a bad curated write is always recoverable by re-running.

    When ``narrow_prefix`` is given, a second payload-free Parquet is written
    there from the same NDJSON (see ``NARROW_EXCLUDED_COLUMNS``) — the dataset a
    dashboard reads. Curated is written FIRST and narrow second, so a failure in
    the derived dataset can never cost us the system of record; the Lambda then
    fails (rather than silently serving a stale dashboard) and a re-run is
    idempotent for both, since each is a fixed-key overwrite.

    Caveat on "fails": nothing in infra/terraform/ configures a CloudWatch alarm,
    DLQ, or failure destination on this function, so the failure surfaces only as
    a Lambda `Errors` datapoint nobody is subscribed to, plus EventBridge's
    default async retries re-running the whole job. Until an alarm exists this is
    detectable-on-inspection, not alerting.
    """
    raw_dt_prefix = f"{raw_prefix}dt={date}/"
    keys = list_raw_keys(s3, bucket, raw_dt_prefix)
    if not keys:
        logger.info("compaction: no raw objects for dt=%s", date)
        return 0

    with tempfile.TemporaryDirectory() as tmp:
        ndjson_path = os.path.join(tmp, "raw.ndjson")
        with open(ndjson_path, "wb") as f:
            for key in keys:
                body = s3.get_object(Bucket=bucket, Key=key)["Body"].read()
                f.write(body.rstrip(b"\n") + b"\n")

        parquet_path = os.path.join(tmp, "data.parquet")
        writer(ndjson_path, parquet_path)

        # ONE fixed-named file per date partition. This is the whole point of
        # compaction at our volume (a day is well under any single-file concern),
        # and the fixed key makes re-runs idempotent by plain overwrite — no
        # dedup, no orphans. INVARIANT: if this ever changes to unique/multi-file
        # names (the scale trigger in docs/tool-call-logging-spec.md), the job
        # MUST first clear `curated/dt=<date>/`, or overwrite stops protecting us
        # and re-runs will leave stale files → duplicate rows on read.
        curated_key = f"{curated_prefix}dt={date}/data.parquet"
        with open(parquet_path, "rb") as pf:
            s3.put_object(
                Bucket=bucket,
                Key=curated_key,
                Body=pf.read(),
                ContentType="application/vnd.apache.parquet",
            )

        if narrow_prefix:
            narrow_path = os.path.join(tmp, "narrow.parquet")
            narrow_writer(ndjson_path, narrow_path)
            narrow_key = f"{narrow_prefix}dt={date}/data.parquet"
            with open(narrow_path, "rb") as nf:
                s3.put_object(
                    Bucket=bucket,
                    Key=narrow_key,
                    Body=nf.read(),
                    ContentType="application/vnd.apache.parquet",
                )
            logger.info("compaction: dt=%s narrow -> %s", date, narrow_key)

    # Raw is intentionally NOT deleted — it's the recovery source and the S3
    # lifecycle rule expires it after it's been rolled up.
    logger.info("compaction: dt=%s rolled up %d objects -> %s", date, len(keys), curated_key)
    return len(keys)


def lambda_handler(event: dict | None, context: Any = None) -> dict:
    """Lambda entry point. Compacts the date from ``event['date']`` (backfill)
    or yesterday (UTC) by default. Reads bucket/prefixes from settings."""
    import boto3

    from cube_cloud.config import settings

    date = (event or {}).get("date") or default_date()
    s3 = boto3.client("s3", region_name=settings.aws_region)
    count = compact_date(
        s3,
        settings.telemetry_bucket,
        date,
        settings.telemetry_raw_prefix,
        settings.telemetry_curated_prefix,
        narrow_prefix=settings.telemetry_narrow_prefix or None,
    )
    return {"date": date, "compacted": count}
