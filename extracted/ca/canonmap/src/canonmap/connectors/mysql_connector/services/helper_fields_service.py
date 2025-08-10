# src/canonmap/connectors/mysql_connector/services/helper_fields_service.py

from __future__ import annotations

import os
from typing import Any

from canonmap.connectors.mysql_connector.utils.sql_identifiers import quote_identifier as _q
from canonmap.connectors.mysql_connector.utils.db_metadata import get_primary_key_columns, column_exists
from canonmap.connectors.mysql_connector.utils.retry import with_retry
from canonmap.connectors.mysql_connector.utils.paging import fetch_chunk
from canonmap.connectors.mysql_connector.utils.dml import bulk_case_update_by_pk
from canonmap.connectors.mysql_connector.utils.transforms import to_initialism, to_phonetic, to_soundex
from canonmap.connectors.mysql_connector.models import (
    FieldTransformType,
    IfExists,
    CreateHelperFieldsPayload,
    TableFieldInput,
    TableField,
    CreateHelperFieldRequest,
)


TRANSFORM_MAP = {
    FieldTransformType.INITIALISM: to_initialism,
    FieldTransformType.PHONETIC: to_phonetic,
    FieldTransformType.SOUNDEX: to_soundex,
}


def make_helper_column_name(source_field_name: str, transform_value: str) -> str:
    return f"__{source_field_name}_{transform_value}__"


def ensure_helper_column(connector: Any, table_name: str, helper_field_name: str, mode: IfExists) -> None:
    table = _q(table_name)
    helper_col = _q(helper_field_name)
    exists = column_exists(connector, table_name, helper_field_name)
    if exists:
        if mode == IfExists.SKIP:
            return
        if mode == IfExists.ERROR:
            raise RuntimeError(f"Helper field {helper_field_name} already exists in {table_name}")
        if mode == IfExists.REPLACE:
            with_retry(lambda: connector.execute_query(f"ALTER TABLE {table} DROP COLUMN {helper_col}", allow_writes=True))
            with_retry(lambda: connector.execute_query(f"ALTER TABLE {table} ADD COLUMN {helper_col} VARCHAR(255)", allow_writes=True))
            return
    else:
        with_retry(lambda: connector.execute_query(f"ALTER TABLE {table} ADD COLUMN {helper_col} VARCHAR(255)", allow_writes=True))


def process_helper_for_field(
    connector: Any,
    table_name: str,
    source_field_name: str,
    transform_type: FieldTransformType,
    chunk_size: int,
    mode: IfExists,
) -> None:
    helper_field_name = make_helper_column_name(source_field_name, transform_type.value)
    table = _q(table_name)
    helper_col = _q(helper_field_name)
    pk_cols = get_primary_key_columns(connector, table_name)
    if not pk_cols:
        raise RuntimeError(f"Could not determine primary key for table '{table_name}'")
    pk_col_name = pk_cols[0]
    transform_fn = TRANSFORM_MAP[transform_type]

    ensure_helper_column(connector, table_name, helper_field_name, mode)

    last_pk = None
    total_updated = 0
    while True:
        rows = fetch_chunk(connector, table_name, pk_col_name, source_field_name, last_pk, chunk_size)
        if not rows:
            break
        updates: list[tuple[Any, Any]] = []
        for row in rows:
            original_value = row[source_field_name]
            transformed_value = transform_fn(original_value)
            updates.append((transformed_value, row[pk_col_name]))

        def _apply_updates() -> None:
            where_suffix = ""
            if mode in (IfExists.APPEND, IfExists.FILL_EMPTY):
                where_suffix = f" AND ({helper_col} IS NULL OR {helper_col} = '')"
            bulk_case_update_by_pk(
                connector,
                table_name,
                pk_col_name,
                helper_field_name,
                updates,
                where_suffix=where_suffix,
            )

        with_retry(_apply_updates)
        total_updated += len(updates)
        last_pk = rows[-1][pk_col_name]

    if hasattr(connector, "logger"):
        connector.logger.info(
            "Helper field %s populated for table %s: %d rows updated",
            helper_field_name,
            table_name,
            total_updated,
        )


def _normalize_dict_request(payload: dict):
    raw_table_fields: list[TableFieldInput] = payload.get("table_fields", [])
    converted_fields: list[TableField] = []
    for f in raw_table_fields:
        if isinstance(f, TableField):
            converted_fields.append(f)
        elif isinstance(f, dict):
            converted_fields.append(TableField(**f))
        elif isinstance(f, str):
            if "." in f:
                t, fld = f.split(".", 1)
            elif ":" in f:
                t, fld = f.split(":", 1)
            else:
                raise ValueError(
                    f"Malformed TableField string '{f}', expected 'table.field' or 'table:field'"
                )
            converted_fields.append(TableField(table_name=t.strip(), field_name=fld.strip()))
        else:
            raise ValueError(f"Malformed TableField: {f!r}")

    all_transforms = bool(payload.get("all_transforms", True))
    chunk_size = int(payload.get("chunk_size", 10000))
    parallel = bool(payload.get("parallel", False))
    if_helper_exists = payload.get("if_helper_exists", "error")
    if isinstance(if_helper_exists, str):
        if_helper_exists_enum = IfExists(if_helper_exists)
    elif isinstance(if_helper_exists, IfExists):
        if_helper_exists_enum = if_helper_exists
    else:
        raise ValueError(f"Malformed if_helper_exists: {if_helper_exists!r}")

    transform_type = None
    if not all_transforms:
        tt = payload.get("transform_type", FieldTransformType.INITIALISM)
        transform_type = FieldTransformType(tt) if isinstance(tt, str) else tt

    return converted_fields, all_transforms, transform_type, chunk_size, parallel, if_helper_exists_enum


def _create_helper_fields(connector: Any, payload: "dict | CreateHelperFieldsPayload") -> None:
    fields, all_transforms, transform_type, chunk_size, parallel, if_helper_exists_enum = _normalize_dict_request(payload)

    if not fields:
        raise ValueError("At least one TableField must be specified.")

    if all_transforms:
        transform_types = list(TRANSFORM_MAP.keys())
        tasks = [
            CreateHelperFieldRequest(
                table_field=field,
                transform_type=tt,
                chunk_size=chunk_size,
                if_helper_exists=if_helper_exists_enum,
            )
            for field in fields
            for tt in transform_types
        ]
    else:
        if transform_type is None:
            raise ValueError("transform_type must be specified when all_transforms is False")
        tasks = [
            CreateHelperFieldRequest(
                table_field=field,
                transform_type=transform_type,
                chunk_size=chunk_size,
                if_helper_exists=if_helper_exists_enum,
            )
            for field in fields
        ]

    if parallel:
        from concurrent.futures import ThreadPoolExecutor
        max_workers = max(1, min((os.cpu_count() or 4), 4))
        with ThreadPoolExecutor(max_workers=max_workers) as pool:
            list(
                pool.map(
                    lambda r: process_helper_for_field(
                        connector,
                        r.table_field.table_name,
                        r.table_field.field_name,
                        r.transform_type,
                        max(1, int(r.chunk_size)),
                        r.if_helper_exists,
                    ),
                    tasks,
                )
            )
    else:
        for r in tasks:
            process_helper_for_field(
                connector,
                r.table_field.table_name,
                r.table_field.field_name,
                r.transform_type,
                max(1, int(r.chunk_size)),
                r.if_helper_exists,
            )


def create_helper_fields(connector: Any, payload: "dict | CreateHelperFieldsPayload") -> None:
    """Public wrapper to create helper fields (non-underscored API)."""
    _create_helper_fields(connector, payload)

