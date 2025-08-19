"""
schema_detection.py
────────────────────
Infer Arrow/DuckDB schema for a *list* of S3 objects.
Content‑based detection – never trusts filenames.
"""

from __future__ import annotations

import io
import urllib.parse
from dataclasses import dataclass
from typing import Dict, Optional, Tuple

import boto3
import fastavro
import pyarrow as pa
from botocore.exceptions import ClientError
from loguru import logger
from mypy_boto3_s3 import S3Client
from pyarrow.orc import ORCFile

from gable.cli.helpers.data_asset_s3.compression_handler import (
    CompressionHandler,
    CompressionWrapper,
    FileFormat,
    FileTypeMetadata,
)
from gable.cli.helpers.data_asset_s3.duckdb_connection import get_resilient_duckdb
from gable.cli.helpers.data_asset_s3.native_s3_converter import (
    NativeS3Converter,
    merge_schemas,
)
from gable.cli.helpers.data_asset_s3.schema_profiler import (
    get_data_asset_field_profiles_for_data_asset,
)
from gable.openapi import DataAssetFieldsToProfilesMapping, S3SamplingParameters


@dataclass
class S3DetectionResult:
    schema: dict
    data_asset_fields_to_profiles_map: Optional[DataAssetFieldsToProfilesMapping] = None


# ───────────────────── DuckDB relation helper ────────────────────────


def _relation_from_path(path: str, fmt: FileFormat, rows: int):
    """
    Return a DuckDB relation that contains *rows* sample rows.
    """
    resilient_duckdb = get_resilient_duckdb()
    try:
        if fmt in (FileFormat.CSV, FileFormat.TSV, FileFormat.JSON):
            # Let DuckDB auto‑detect – no delimiter‑guessing headaches
            if fmt == FileFormat.CSV:
                q = f"SELECT * FROM read_csv_auto('{path}') LIMIT {rows}"
            elif fmt == FileFormat.TSV:
                q = "SELECT * FROM read_csv_auto(" f"'{path}', delim='\t') LIMIT {rows}"
            elif fmt == FileFormat.JSON:
                q = f"SELECT * FROM read_json_auto('{path}') LIMIT {rows}"
        elif fmt == FileFormat.PARQUET:
            q = f"SELECT * FROM read_parquet('{path}') LIMIT {rows}"
        elif fmt == FileFormat.ORC:
            with open(path, "rb") as f:
                table = ORCFile(f).read()
                resilient_duckdb.register("orc_table", table)
                q = f"SELECT * FROM orc_table LIMIT {rows}"  # type: ignore
        elif fmt == FileFormat.AVRO:
            q = f"SELECT * FROM read_avro('{path}') LIMIT {rows}"
        elif not q:  # type: ignore
            raise ValueError(f"Unsupported format: {fmt}")
        return resilient_duckdb.query(q)
    except Exception as e:
        raise Exception(f"Failed to read {path} with format {fmt}: {e}")


def read_s3_files_with_schema_inference(
    *,
    s3_urls: list[str],
    row_sample_count: int,
    event_name: str,
    recent_file_count: int,
    skip_profiling: bool = False,
    s3_client: Optional[S3Client] = None,
) -> Optional[S3DetectionResult]:
    s3 = s3_client or boto3.client("s3")
    handler = CompressionHandler()
    converter = NativeS3Converter()
    data_map: Dict[str, Tuple[pa.Table, dict]] = {}

    for url in s3_urls:
        bucket, key = _split_s3_url(url)
        if bucket is None:
            logger.error(f"[SchemaDetect] invalid S3 url: {url}")
            continue

        try:
            raw = s3.get_object(Bucket=bucket, Key=key)["Body"].read()  # type: ignore
            if not raw:
                logger.error(f"[SchemaDetect] skip {url}: empty object")
                continue
        except ClientError as exc:
            logger.error(f"[SchemaDetect] skip {url}: {exc}")
            continue

        meta: FileTypeMetadata = handler.get_file_type_metadata(raw)
        wrapper, fmt = meta.wrapper, meta.format

        # ───── direct AVRO branch (fast path) ─────────────────────────
        if fmt == FileFormat.AVRO and wrapper == CompressionWrapper.NONE:
            try:
                records = list(fastavro.reader(io.BytesIO(raw)))
                if not records:
                    raise ValueError("no records")
            except Exception as exc:
                logger.error(f"[SchemaDetect] skip {url}: {exc}")
                continue

            tbl = pa.Table.from_pylist(records[:row_sample_count])
            data_map[url] = (tbl, converter.to_recap(tbl, event_name))
            continue

        try:
            # write to local tmp and let DuckDB read
            path, local_meta = handler.decompress_s3_file_to_local(
                bucket,
                key,  # type: ignore
                compression_wrapper=wrapper,
                s3_client=s3_client,
                file_buff=raw,
            )
            try:
                rel = _relation_from_path(path, local_meta.format, row_sample_count)
            except Exception as exc:
                logger.error(f"[SchemaDetect] skip {url}: {exc}")
                continue

            if fmt in {FileFormat.CSV, FileFormat.TSV} and len(rel.columns) < 2:
                raise ValueError("degenerate text file – likely corrupted")
            # quick sanity check
            rel.aggregate("COUNT(*)").fetchone()

            # Convert to Arrow table immediately to avoid connection dependency issues
            arrow_table = rel.fetch_arrow_table()
            schema = converter.to_recap(arrow_table, event_name=event_name)
            data_map[url] = (arrow_table, schema)

        except Exception as exc:
            logger.error(f"[SchemaDetect] skip {url}: {exc}")
            continue

    if not data_map:
        return None

    merged_schema = merge_schemas([s for _, s in data_map.values()])

    if skip_profiling:
        return S3DetectionResult(merged_schema)

    try:
        profiles = get_data_asset_field_profiles_for_data_asset(
            merged_schema,
            {u: v[0] for u, v in data_map.items()},
            event_name,
            S3SamplingParameters(
                rowSampleCount=row_sample_count,
                recentFileCount=recent_file_count,
            ),
        )
        return S3DetectionResult(merged_schema, profiles)
    except Exception as exc:
        logger.error(f"[SchemaDetect] profiling failed for {event_name}: {exc}")
        return S3DetectionResult(merged_schema)


# ───────────────────────── misc utils ────────────────────────────────


def _split_s3_url(url: str) -> tuple[Optional[str], Optional[str]]:
    """Return (bucket, key) or (None, None) on parse failure."""
    pr = urllib.parse.urlparse(url)
    return (pr.netloc or None, pr.path.lstrip("/") or None)


def strip_s3_bucket_prefix(bucket: str) -> str:
    return bucket.removeprefix("s3://")


def append_s3_url_prefix(bucket: str, key: str) -> str:
    return key if key.startswith("s3://") else f"s3://{bucket}/{key.lstrip('/')}"
