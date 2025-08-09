# src/canonmap/connectors/mysql_connector/utils/create_helper_fields_util.py

import os
import re
import time
from typing import Any, Callable, Optional

from mysql.connector import errors as mysql_errors

from canonmap.connectors.mysql_connector.models import (
    CreateHelperFieldsPayload,
    TableFieldInput,
    TableField,
    FieldTransformType,
    IfExists,
    CreateHelperFieldRequest,
)


def _create_helper_fields(connector: Any, payload: "dict | CreateHelperFieldsPayload") -> None:
    """Full helper-field creation logic. Accepts plain dict/TypedDict payload."""
    fields, all_transforms, transform_type, chunk_size, parallel, if_helper_exists_enum = _normalize_dict_request(connector, payload)

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
            list(pool.map(lambda r: _process_helper_for_field(connector, r), tasks))
    else:
        for req in tasks:
            _process_helper_for_field(connector, req)


# -----------------------
# Internal helpers
# -----------------------


def _process_helper_for_field(connector: Any, req: CreateHelperFieldRequest) -> None:
    table_name = req.table_field.table_name
    source_field_name = req.table_field.field_name
    transform_type = req.transform_type
    chunk_size = max(1, int(req.chunk_size))
    mode = req.if_helper_exists

    transform_fn = TRANSFORM_MAP[transform_type]
    # Helper columns must be wrapped with double underscores
    helper_field_name = _make_helper_column_name(source_field_name, transform_type.value)

    table = _quote_identifier(table_name)
    helper_col = _quote_identifier(helper_field_name)
    source_col = _quote_identifier(source_field_name)

    # Determine primary key column
    pk_col_name = _get_primary_key_column(connector, table_name)
    if not pk_col_name:
        raise RuntimeError(f"Could not determine primary key for table '{table_name}'")
    pk_col = _quote_identifier(pk_col_name)

    # Ensure helper column exists / handle existence policy
    exists = _column_exists(connector, table_name, helper_field_name)
    if exists:
        if mode == IfExists.SKIP:
            connector.logger.info("Skipping existing helper field %s in %s", helper_field_name, table_name) if hasattr(connector, "logger") else None
            return
        if mode == IfExists.ERROR:
            raise RuntimeError(f"Helper field {helper_field_name} already exists in {table_name}")
        if mode == IfExists.REPLACE:
            _with_retry(connector, lambda: connector.execute_query(
                f"ALTER TABLE {table} DROP COLUMN {helper_col}", allow_writes=True
            ))
            _with_retry(connector, lambda: connector.execute_query(
                f"ALTER TABLE {table} ADD COLUMN {helper_col} VARCHAR(255)", allow_writes=True
            ))
    else:
        # Add helper field column if missing
        _with_retry(connector, lambda: connector.execute_query(
            f"ALTER TABLE {table} ADD COLUMN {helper_col} VARCHAR(255)", allow_writes=True
        ))

    # Process rows in primary-key order, chunked
    last_pk = None
    total_updated = 0

    while True:
        rows = _fetch_chunk(connector, table_name, pk_col_name, source_field_name, last_pk, chunk_size)
        if not rows:
            break

        # Prepare transformed values
        updates: list[tuple[Any, Any]] = []  # (new_value, pk)
        for row in rows:
            original_value = row[source_field_name]
            transformed_value = transform_fn(original_value)
            updates.append((transformed_value, row[pk_col_name]))

        # Apply updates with retry and chunk-level transaction
        def _apply_updates() -> None:
            with connector.transaction() as conn:
                cursor = conn.cursor()
                # Build a single CASE-based update for efficiency
                pks = [pk for _, pk in updates]
                case_parts = []
                case_params: list[Any] = []
                for val, pk in updates:
                    case_parts.append("WHEN %s THEN %s")
                    case_params.extend([pk, val])

                in_params = pks
                where_suffix = ""
                if mode in (IfExists.APPEND, IfExists.FILL_EMPTY):
                    where_suffix = f" AND ({helper_col} IS NULL OR {helper_col} = '')"

                sql = (
                    f"UPDATE {table} "
                    f"SET {helper_col} = CASE {pk_col} " + " ".join(case_parts) + " END "
                    f"WHERE {pk_col} IN (" + ",".join(["%s"] * len(in_params)) + ")" + where_suffix
                )
                params = tuple(case_params + in_params)
                cursor.execute(sql, params)
                conn.commit()
                cursor.close()

        _with_retry(connector, _apply_updates)

        total_updated += len(updates)
        last_pk = rows[-1][pk_col_name]

    if hasattr(connector, "logger"):
        connector.logger.info(
            "Helper field %s populated for table %s: %d rows updated",
            helper_field_name,
            table_name,
            total_updated,
        )


def _normalize_dict_request(connector: Any, payload: dict):
    try:
        raw_table_fields: list[TableFieldInput] = payload.get("table_fields", [])
        converted_fields: list[TableField] = []
        for f in raw_table_fields:
            if isinstance(f, TableField):
                converted_fields.append(f)
            elif isinstance(f, dict):
                converted_fields.append(TableField(**f))
            # tuples are no longer an accepted public shape
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
    except Exception as exc:
        raise ValueError(f"Malformed CreateHelperFieldsRequest dict: {exc}")


def _quote_identifier(name: str) -> str:
    if not name or not name.replace("_", "").isalnum():
        raise ValueError(f"Invalid identifier: {name!r}")
    return f"`{name}`"


def _column_exists(connector: Any, table_name: str, column_name: str) -> bool:
    with connector.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT 1
            FROM information_schema.COLUMNS
            WHERE TABLE_SCHEMA = DATABASE()
              AND TABLE_NAME = %s
              AND COLUMN_NAME = %s
            LIMIT 1
            """,
            (table_name, column_name),
        )
        exists = cursor.fetchone() is not None
        cursor.close()
        return exists


def _get_primary_key_column(connector: Any, table_name: str) -> Optional[str]:
    with connector.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT k.COLUMN_NAME
            FROM information_schema.TABLE_CONSTRAINTS t
            JOIN information_schema.KEY_COLUMN_USAGE k
              ON k.CONSTRAINT_NAME = t.CONSTRAINT_NAME
             AND k.TABLE_SCHEMA = t.TABLE_SCHEMA
             AND k.TABLE_NAME = t.TABLE_NAME
            WHERE t.CONSTRAINT_TYPE = 'PRIMARY KEY'
              AND t.TABLE_SCHEMA = DATABASE()
              AND t.TABLE_NAME = %s
            LIMIT 1
            """,
            (table_name,),
        )
        row = cursor.fetchone()
        cursor.close()
        return row[0] if row else None


def _fetch_chunk(
    connector: Any,
    table_name: str,
    pk_col: str,
    source_col: str,
    last_pk: Optional[Any],
    limit: int,
) -> list[dict]:
    table = _quote_identifier(table_name)
    pk = _quote_identifier(pk_col)
    src = _quote_identifier(source_col)

    with connector.get_connection() as conn:
        cursor = conn.cursor(dictionary=True)
        if last_pk is None:
            sql = f"SELECT {pk} AS pk, {src} AS src FROM {table} ORDER BY {pk} ASC LIMIT %s"
            cursor.execute(sql, (limit,))
        else:
            sql = f"SELECT {pk} AS pk, {src} AS src FROM {table} WHERE {pk} > %s ORDER BY {pk} ASC LIMIT %s"
            cursor.execute(sql, (last_pk, limit))
        fetched = cursor.fetchall()
        cursor.close()

    rows: list[dict] = []
    for r in fetched:
        rows.append({pk_col: r["pk"], source_col: r["src"]})
    return rows


def _with_retry(connector: Any, fn: Callable[[], Any], *, max_attempts: int = 5, base_delay: float = 0.5) -> Any:
    attempt = 0
    while True:
        attempt += 1
        try:
            return fn()
        except Exception as exc:  # noqa: BLE001
            errno = getattr(exc, "errno", None)
            if isinstance(exc, mysql_errors.Error) and errno in {1205, 1213} and attempt < max_attempts:
                delay = base_delay * (2 ** (attempt - 1))
                time.sleep(min(delay, 5.0))
                continue
            raise


def _to_initialism(text: str | None) -> str | None:
    if not text:
        return None
    parts = re.findall(r"[A-Za-z]+", text)
    return "".join(p[0].upper() for p in parts) if parts else None


def _to_phonetic(text: str | None) -> str | None:
    if not text:
        return None
    try:
        from metaphone import doublemetaphone
    except ImportError:
        raise RuntimeError("metaphone package not installed")
    p, s = doublemetaphone(text)
    return p or s or None


def _to_soundex_py(text: str | None) -> str | None:
    if not text:
        return None
    try:
        import jellyfish
    except ImportError:
        raise RuntimeError("jellyfish package not installed for SOUNDEX")
    return jellyfish.soundex(text)


def _make_helper_column_name(source_field_name: str, transform_value: str) -> str:
    """Compose canonical helper column name with double underscores.

    Example: player + initialism -> __player_initialism__
    """
    return f"__{source_field_name}_{transform_value}__"


TRANSFORM_MAP: dict[FieldTransformType, Callable[[str | None], str | None]] = {
    FieldTransformType.INITIALISM: _to_initialism,
    FieldTransformType.PHONETIC: _to_phonetic,
    FieldTransformType.SOUNDEX: _to_soundex_py,
}

