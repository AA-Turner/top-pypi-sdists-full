"""Load items from SQL or search and export to CSV."""
from __future__ import annotations

import json
from typing import Any, Iterator

from ..exceptions import ConfigurationError
from ..jobs.show import (
    _fetchall,
    _search_list_filters,
    _with_search,
    fetch_job,
    fetch_job_search,
    fetch_jobs,
    fetch_jobs_search,
)
from .csv_writer import write_csv
from .flatten import flatten_value


def export_items_to_csv(
    settings,
    output_path: str,
    *,
    job_id: str | None = None,
    spider: str | None = None,
    fields: list[str] | None = None,
    utf8_sig: bool = False,
    batch_size: int = 500,
) -> tuple[int, list[str]]:
    """Export scraped items to CSV. Returns ``(count, columns)``."""
    _require_destination(settings)
    if job_id and spider:
        raise ConfigurationError("export items: use either --job-id or --spider, not both")
    if not job_id and not spider:
        raise ConfigurationError("export items requires --job-id or --spider")

    batch_size = max(1, batch_size)
    if job_id:
        _ensure_job_exists(settings, job_id)
        if settings.ingest_to_database:
            rows = list(_iter_sql_rows_for_job(settings, job_id, batch_size=batch_size))
        else:
            rows = list(_iter_search_rows_for_job(settings, job_id, batch_size=batch_size))
    else:
        if settings.ingest_to_database:
            rows = list(_iter_sql_rows_for_spider(settings, spider, batch_size=batch_size))
        else:
            rows = list(_iter_search_rows_for_spider(settings, spider, batch_size=batch_size))
        if not rows:
            _ensure_spider_has_jobs(settings, spider)

    return write_csv(output_path, rows, fields=fields, utf8_sig=utf8_sig)


def _require_destination(settings) -> None:
    if settings.ingest_to_database or settings.ingest_to_search:
        return
    raise ConfigurationError(
        "export requires a destination: set DB_URL (or DB_* fields), "
        "SEARCH_URL, or enable default SQLite"
    )


def _ensure_job_exists(settings, job_id: str) -> None:
    if settings.ingest_to_database:
        from ..database.connection import DatabaseConnection

        db = DatabaseConnection(settings.db_url)
        try:
            if not fetch_job(db, settings, job_id):
                raise ConfigurationError(f"job not found: {job_id}")
        finally:
            db.close()
        return

    with _with_search(settings) as client:
        if not fetch_job_search(client, settings, job_id):
            raise ConfigurationError(f"job not found: {job_id}")


def _ensure_spider_has_jobs(settings, spider: str) -> None:
    if settings.ingest_to_database:
        from ..database.connection import DatabaseConnection

        db = DatabaseConnection(settings.db_url)
        try:
            jobs = fetch_jobs(db, settings, limit=1, spider=spider)
        finally:
            db.close()
    else:
        with _with_search(settings) as client:
            jobs = fetch_jobs_search(client, settings, limit=1, spider=spider)
    if not jobs:
        raise ConfigurationError(f"no jobs found for spider: {spider}")


def _iter_sql_rows_for_job(
    settings,
    external_job_id: str,
    *,
    batch_size: int,
) -> Iterator[dict]:
    from ..database.connection import DatabaseConnection

    db = DatabaseConnection(settings.db_url)
    try:
        pk = _internal_job_pk(db, settings, external_job_id)
        if pk is None:
            raise ConfigurationError(f"job not found: {external_job_id}")
        table = settings.db_items_table
        last_id = 0
        while True:
            rows = _fetchall(
                db,
                f"SELECT id, item, created_at FROM {table} "
                f"WHERE job_id = %s AND id > %s ORDER BY id LIMIT %s",
                (pk, last_id, batch_size),
            )
            if not rows:
                break
            for row_id, item_raw, created_at in rows:
                last_id = row_id
                yield _row_dict(external_job_id, created_at, item_raw)
    finally:
        db.close()


def _iter_sql_rows_for_spider(
    settings,
    spider: str,
    *,
    batch_size: int,
) -> Iterator[dict]:
    from ..database.connection import DatabaseConnection

    db = DatabaseConnection(settings.db_url)
    try:
        items_table = settings.db_items_table
        jobs_table = settings.db_jobs_table
        last_id = 0
        while True:
            rows = _fetchall(
                db,
                f"SELECT i.id, j.job_id, i.item, i.created_at "
                f"FROM {items_table} i "
                f"INNER JOIN {jobs_table} j ON i.job_id = j.id "
                f"WHERE j.spider_name = %s AND i.id > %s "
                f"ORDER BY i.id LIMIT %s",
                (spider, last_id, batch_size),
            )
            if not rows:
                break
            for row_id, external_job_id, item_raw, created_at in rows:
                last_id = row_id
                yield _row_dict(external_job_id, created_at, item_raw)
    finally:
        db.close()


def _internal_job_pk(db, settings, external_job_id: str) -> int | None:
    row = db.execute(
        f"SELECT id FROM {settings.db_jobs_table} WHERE job_id = %s",
        (external_job_id,),
    )
    return row[0] if row else None


def _iter_search_rows_for_job(
    settings,
    external_job_id: str,
    *,
    batch_size: int,
) -> Iterator[dict]:
    with _with_search(settings) as client:
        index = settings.db_items_table
        for doc in client.iter_documents(
            index,
            query=_job_id_query(external_job_id),
            size=batch_size,
            sort=[
                {"created_at": {"order": "asc", "unmapped_type": "date"}},
                {"_id": "asc"},
            ],
        ):
            yield _row_dict(
                external_job_id,
                doc.get("created_at"),
                doc.get("item"),
            )


def _iter_search_rows_for_spider(
    settings,
    spider: str,
    *,
    batch_size: int,
) -> Iterator[dict]:
    with _with_search(settings) as client:
        job_ids = _search_job_ids_for_spider(client, settings, spider)
        if not job_ids:
            return
        index = settings.db_items_table
        for chunk in _chunks(job_ids, 500):
            for doc in client.iter_documents(
                index,
                query=_job_ids_query(chunk),
                size=batch_size,
                sort=[
                    {"created_at": {"order": "asc", "unmapped_type": "date"}},
                    {"_id": "asc"},
                ],
            ):
                yield _row_dict(
                    doc.get("job_id") or "",
                    doc.get("created_at"),
                    doc.get("item"),
                )


def _search_job_ids_for_spider(client, settings, spider: str) -> list[str]:
    jobs_index = settings.db_jobs_table
    filters = _search_list_filters(spider=spider)
    query: dict[str, Any]
    if filters:
        query = {"bool": {"filter": list(filters)}}
    else:
        query = {"match_all": {}}
    ids: list[str] = []
    for doc in client.iter_documents(
        jobs_index,
        query=query,
        size=500,
        sort=[
            {"started_at": {"order": "asc", "unmapped_type": "date"}},
            {"_id": "asc"},
        ],
    ):
        job_key = doc.get("job_id")
        if job_key:
            ids.append(str(job_key))
    return ids


def _job_id_query(external_job_id: str) -> dict:
    return {
        "bool": {
            "should": [
                {"term": {"job_id": external_job_id}},
                {"term": {"job_id.keyword": external_job_id}},
            ],
            "minimum_should_match": 1,
        }
    }


def _job_ids_query(job_ids: list[str]) -> dict:
    return {
        "bool": {
            "should": [
                {"terms": {"job_id": job_ids}},
                {"terms": {"job_id.keyword": job_ids}},
            ],
            "minimum_should_match": 1,
        }
    }


def _chunks(values: list[str], size: int) -> Iterator[list[str]]:
    for start in range(0, len(values), size):
        yield values[start : start + size]


def _row_dict(external_job_id: str, created_at: Any, item_raw: Any) -> dict:
    item = _parse_item(item_raw)
    flat = flatten_value(item)
    flat["job_id"] = external_job_id
    flat["created_at"] = _format_timestamp(created_at)
    return flat


def _parse_item(raw: Any) -> dict:
    if raw is None:
        return {}
    if isinstance(raw, dict):
        return raw
    if isinstance(raw, (bytes, bytearray)):
        raw = raw.decode("utf-8")
    if isinstance(raw, str):
        text = raw.strip()
        if not text:
            return {}
        return json.loads(text)
    return {}


def _format_timestamp(value: Any) -> str:
    if value is None:
        return ""
    return str(value).replace("T", " ")[:26]
