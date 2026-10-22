"""Read-only queries for the ingest dashboard (SQL or search)."""

from __future__ import annotations

import json
import threading
from typing import Any

from scrapy_ingest.export.items import _internal_job_pk, _job_id_query
from scrapy_ingest.jobs.show import (
    _fetchall,
    _KEYS,
    fetch_job,
)

from .serializers import serialize_value

_DASH_KEYS = (
    "total_jobs",
    "running",
    "finished",
    "total_items",
    "total_requests",
    "failed_requests",
    "total_errors",
    "spider_count",
)


def _clamp_page(page: int, page_size: int, *, max_size: int) -> tuple[int, int]:
    page = max(1, page)
    return page, min(max(1, page_size), max_size)


def _serialize_stats_value(value: Any) -> Any:
    if value is None:
        return None
    if isinstance(value, dict):
        return {str(k): _serialize_stats_value(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_serialize_stats_value(v) for v in value]
    return serialize_value(value)


def _parse_job_stats(raw: Any) -> dict[str, Any] | None:
    if raw is None:
        return None
    if isinstance(raw, str):
        try:
            raw = json.loads(raw)
        except json.JSONDecodeError:
            return None
    if not isinstance(raw, dict):
        return None
    return {str(k): _serialize_stats_value(v) for k, v in raw.items()}


def _logs_time_column(settings) -> str:
    return (
        "`time`" if getattr(settings, "db_dialect", "postgres") == "mysql" else "time"
    )


def _job_order_sql(settings) -> str:
    dialect = getattr(settings, "db_dialect", "postgres")
    if dialect in ("mysql", "sqlite"):
        return "started_at DESC, id DESC"
    return "started_at DESC NULLS LAST, id DESC"


def _like_pattern(value: str, dialect: str) -> str:
    if dialect == "sqlite":
        return f"%{value}%"
    escaped = value.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")
    return f"%{escaped}%"


def _dashboard_sql_list_filters(settings, status=None, spider=None):
    clauses, params = [], []
    if status:
        clauses.append("status = %s")
        params.append(status)
    if spider:
        needle = spider.strip()
        if needle:
            dialect = getattr(settings, "db_dialect", "postgres") or "postgres"
            pattern = _like_pattern(needle, dialect)
            if dialect == "postgres":
                clauses.append("spider_name ILIKE %s ESCAPE E'\\\\'")
            else:
                clauses.append("spider_name LIKE %s")
            params.append(pattern)
    if not clauses:
        return "", ()
    return f" WHERE {' AND '.join(clauses)}", tuple(params)


def _dashboard_search_filters(status=None, spider=None):
    filters = []
    if status:
        filters.append({"term": {"status": status}})
    if spider:
        needle = spider.strip()
        if needle:
            filters.append(
                {
                    "wildcard": {
                        "spider_name": {
                            "value": f"*{needle}*",
                            "case_insensitive": True,
                        }
                    }
                }
            )
    return filters


def _search_query(status=None, spider=None) -> dict[str, Any]:
    filters = _dashboard_search_filters(status, spider)
    if not filters:
        return {"match_all": {}}
    return {"bool": {"filter": list(filters)}}


def _page_payload(items, page, page_size, total):
    pages = max(1, (total + page_size - 1) // page_size) if total else 1
    return {
        "items": items,
        "page": page,
        "page_size": page_size,
        "total": total,
        "pages": pages,
    }


def _empty_dashboard():
    return dict.fromkeys(_DASH_KEYS, 0)


def _dashboard_payload(row):
    out = {}
    for i, key in enumerate(_DASH_KEYS):
        val = row[i] if i < len(row) else 0
        out[key] = int(val or 0)
    return out


def _search_page(client, index, query, page, page_size, sort):
    from opensearchpy.exceptions import NotFoundError, RequestError

    from scrapy_ingest.database.search import _ignore_cluster_warnings

    body = {
        "from": (page - 1) * page_size,
        "size": page_size,
        "sort": sort,
        "query": query,
    }

    def _run(payload):
        with _ignore_cluster_warnings():
            return client._client.search(index=index, body=payload)

    try:
        resp = _run(body)
    except NotFoundError:
        return [], 0
    except RequestError as exc:
        text = str(exc).lower()
        if "index_not_found" in text:
            return [], 0
        if sort and ("sort" in text or "no mapping" in text or "unknown field" in text):
            resp = _run({**body, "sort": ["_doc"]})
        else:
            raise
    hits = resp.get("hits", {}).get("hits", [])
    raw_total = resp.get("hits", {}).get("total", 0)
    total = raw_total["value"] if isinstance(raw_total, dict) else int(raw_total or 0)
    return [
        {**(hit.get("_source") or {}), "_id": hit.get("_id")} for hit in hits
    ], total


def _search_dashboard(client, index, query):
    from scrapy_ingest.database.search import _ignore_cluster_warnings

    body = {
        "size": 0,
        "query": query,
        "aggs": {
            "running": {"filter": {"term": {"status": "running"}}},
            "finished": {"filter": {"term": {"status": "finished"}}},
            "total_items": {"sum": {"field": "items_count"}},
            "total_requests": {"sum": {"field": "requests_count"}},
            "failed_requests": {"sum": {"field": "failed_requests"}},
            "total_errors": {"sum": {"field": "errors_count"}},
            "spiders": {"cardinality": {"field": "spider_name.keyword"}},
        },
    }
    with _ignore_cluster_warnings():
        resp = client._client.search(index=index, body=body)
    aggs = resp.get("aggregations", {})
    raw_total = resp.get("hits", {}).get("total", 0)
    total_jobs = (
        raw_total["value"] if isinstance(raw_total, dict) else int(raw_total or 0)
    )
    return {
        "total_jobs": total_jobs,
        "running": int(aggs.get("running", {}).get("doc_count") or 0),
        "finished": int(aggs.get("finished", {}).get("doc_count") or 0),
        "total_items": int(aggs.get("total_items", {}).get("value") or 0),
        "total_requests": int(aggs.get("total_requests", {}).get("value") or 0),
        "failed_requests": int(aggs.get("failed_requests", {}).get("value") or 0),
        "total_errors": int(aggs.get("total_errors", {}).get("value") or 0),
        "spider_count": int(aggs.get("spiders", {}).get("value") or 0),
    }


def _parse_json(raw: Any) -> Any:
    if raw is None:
        return None
    if isinstance(raw, (dict, list)):
        return raw
    if isinstance(raw, (bytes, bytearray)):
        raw = raw.decode()
    if isinstance(raw, str):
        text = raw.strip()
        if not text:
            return None
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            return raw
    return raw


class _LockedDB:
    """Serialize access to one DB connection from FastAPI worker threads."""

    __slots__ = ("_db", "_lock")

    _SQL = frozenset({"execute", "fetchall", "executemany", "commit", "rollback", "close"})

    def __init__(self, db, lock: threading.Lock):
        self._db = db
        self._lock = lock

    def __getattr__(self, name: str):
        attr = getattr(self._db, name)
        if name not in self._SQL:
            return attr

        def call(*args, **kwargs):
            with self._lock:
                return attr(*args, **kwargs)

        return call


class IngestReader:
    """Paginated reads against the configured ingest destination."""

    def __init__(self, settings):
        self.settings = settings
        self._db = None
        self._search = None
        if settings.ingest_to_database:
            from scrapy_ingest.database.connection import DatabaseConnection

            lock = threading.Lock()
            self._db = _LockedDB(
                DatabaseConnection.open(settings.db_url), lock
            )
        elif settings.ingest_to_search:
            from scrapy_ingest.database.search import SearchClient

            self._search = SearchClient(settings)
        else:
            raise RuntimeError("No ingest destination configured")

    def close(self) -> None:
        if self._db is not None:
            self._db.close()
            self._db = None
        if self._search is not None:
            self._search.close()
            self._search = None

    @property
    def uses_sql(self) -> bool:
        return self._db is not None

    def jobs_dashboard(self, *, status=None, spider=None):
        if self._db is not None:
            table = self.settings.db_jobs_table
            where, params = _dashboard_sql_list_filters(self.settings, status, spider)
            row = _fetchall(
                self._db,
                f"""
                SELECT
                    COUNT(*),
                    SUM(CASE WHEN LOWER(COALESCE(status, '')) = 'running' THEN 1 ELSE 0 END),
                    SUM(CASE WHEN LOWER(COALESCE(status, '')) = 'finished' THEN 1 ELSE 0 END),
                    COALESCE(SUM(items_count), 0),
                    COALESCE(SUM(requests_count), 0),
                    COALESCE(SUM(failed_requests), 0),
                    COALESCE(SUM(errors_count), 0),
                    COUNT(DISTINCT spider_name)
                FROM {table}{where}
                """,
                params,
            )
            return _dashboard_payload(row[0]) if row else _empty_dashboard()
        return _search_dashboard(
            self._search, self.settings.db_jobs_table, _search_query(status, spider)
        )

    def list_jobs(self, *, page=1, page_size=25, status=None, spider=None):
        page, page_size = _clamp_page(page, page_size, max_size=200)
        offset = (page - 1) * page_size
        if self._db is not None:
            table = self.settings.db_jobs_table
            where, params = _dashboard_sql_list_filters(self.settings, status, spider)
            total = int(
                (
                    _fetchall(self._db, f"SELECT COUNT(*) FROM {table}{where}", params)
                    or [(0,)]
                )[0][0]
            )
            rows = _fetchall(
                self._db,
                f"SELECT {', '.join(_KEYS)} FROM {table}{where} "
                f"ORDER BY {_job_order_sql(self.settings)} LIMIT %s OFFSET %s",
                params + (page_size, offset),
            )
            items = [
                {k: serialize_value(r[i]) for i, k in enumerate(_KEYS)} for r in rows
            ]
            return _page_payload(items, page, page_size, total)
        query = _search_query(status, spider)
        rows, total = _search_page(
            self._search,
            self.settings.db_jobs_table,
            query,
            page,
            page_size,
            sort=[{"started_at": {"order": "desc", "unmapped_type": "date"}}],
        )
        items = [{k: serialize_value(d.get(k)) for k in _KEYS} for d in rows]
        return _page_payload(items, page, page_size, total)

    def get_job(self, job_id: str):
        stats_raw = None
        if self._db is not None:
            job = fetch_job(self._db, self.settings, job_id)
            if not job:
                return None
            row = self._db.execute(
                f"SELECT stats FROM {self.settings.db_jobs_table} WHERE job_id = %s",
                (job_id,),
            )
            stats_raw = row[0] if row else None
        else:
            doc = self._search.get_document(self.settings.db_jobs_table, job_id)
            if not doc:
                return None
            job = {k: doc.get(k) for k in _KEYS}
            stats_raw = doc.get("stats")
        payload = {k: serialize_value(job.get(k)) for k in _KEYS}
        stats = _parse_job_stats(stats_raw)
        payload["stats"] = stats
        payload["stats_count"] = len(stats) if stats else 0
        return payload

    def list_items(self, job_id: str, *, page=1, page_size=50):
        page, page_size = _clamp_page(page, page_size, max_size=200)
        return self._list_items(job_id, page, page_size)

    def list_requests(
        self, job_id: str, *, page=1, page_size=50, success=None, request_id=None
    ):
        page, page_size = _clamp_page(page, page_size, max_size=200)
        return self._list_requests(job_id, page, page_size, success, request_id)

    def list_logs(self, job_id: str, *, page=1, page_size=100, level=None):
        page, page_size = _clamp_page(page, page_size, max_size=500)
        return self._list_logs(job_id, page, page_size, level)

    def _internal_pk(self, external_job_id: str) -> int | None:
        assert self._db is not None
        return _internal_job_pk(self._db, self.settings, external_job_id)

    def _list_items(self, external_job_id, page, page_size):
        if self._db is not None:
            pk = self._internal_pk(external_job_id)
            if pk is None:
                return _page_payload([], page, page_size, 0)
            table = self.settings.db_items_table
            total = int(
                (
                    _fetchall(
                        self._db,
                        f"SELECT COUNT(*) FROM {table} WHERE job_id = %s",
                        (pk,),
                    )
                    or [(0,)]
                )[0][0]
            )
            rows = _fetchall(
                self._db,
                f"SELECT id, item, created_at FROM {table} WHERE job_id = %s "
                f"ORDER BY id LIMIT %s OFFSET %s",
                (pk, page_size, (page - 1) * page_size),
            )
            items = [
                {
                    "id": r[0],
                    "created_at": serialize_value(r[2]),
                    "item": _parse_json(r[1]),
                }
                for r in rows
            ]
            return _page_payload(items, page, page_size, total)
        rows, total = _search_page(
            self._search,
            self.settings.db_items_table,
            _job_id_query(external_job_id),
            page,
            page_size,
            sort=[
                {"created_at": {"order": "asc", "unmapped_type": "date"}},
                {"_id": "asc"},
            ],
        )
        items = [
            {
                "id": d.get("_id"),
                "created_at": serialize_value(d.get("created_at")),
                "item": _parse_json(d.get("item")),
            }
            for d in rows
        ]
        return _page_payload(items, page, page_size, total)

    def _list_requests(self, external_job_id, page, page_size, success, request_id):
        if self._db is not None:
            pk = self._internal_pk(external_job_id)
            if pk is None:
                return _page_payload([], page, page_size, 0)
            table = self.settings.db_requests_table
            extra, params = self._request_filters(success, pk, request_id)
            total = int(
                (
                    _fetchall(
                        self._db,
                        f"SELECT COUNT(*) FROM {table} WHERE job_id = %s{extra}",
                        tuple(params),
                    )
                    or [(0,)]
                )[0][0]
            )
            rows = _fetchall(
                self._db,
                f"SELECT id, url, method, status_code, response_time_secs, "
                f"response_size_bytes, success, error, parent_url, parent_id, "
                f"fingerprint, created_at "
                f"FROM {table} WHERE job_id = %s{extra} ORDER BY id LIMIT %s OFFSET %s",
                tuple(params) + (page_size, (page - 1) * page_size),
            )
            items = [self._request_row(r) for r in rows]
            return _page_payload(items, page, page_size, total)
        query = _job_id_query(external_job_id)
        if success is not None:
            query = {"bool": {"must": [query, {"term": {"success": success}}]}}
        if request_id is not None:
            query = {"bool": {"must": [query, {"term": {"id": request_id}}]}}
        rows, total = _search_page(
            self._search,
            self.settings.db_requests_table,
            query,
            page,
            page_size,
            sort=[
                {"created_at": {"order": "asc", "unmapped_type": "date"}},
                {"_id": "asc"},
            ],
        )
        return _page_payload(
            [self._request_doc(d) for d in rows], page, page_size, total
        )

    def _list_logs(self, external_job_id, page, page_size, level):
        if self._db is not None:
            pk = self._internal_pk(external_job_id)
            if pk is None:
                return _page_payload([], page, page_size, 0)
            table = self.settings.db_logs_table
            time_col = _logs_time_column(self.settings)
            extra, params = ("", [pk])
            if level:
                extra, params = " AND level = %s", [pk, level]
            total = int(
                (
                    _fetchall(
                        self._db,
                        f"SELECT COUNT(*) FROM {table} WHERE job_id = %s{extra}",
                        tuple(params),
                    )
                    or [(0,)]
                )[0][0]
            )
            rows = _fetchall(
                self._db,
                f"SELECT id, {time_col}, level, logger, message, exception "
                f"FROM {table} WHERE job_id = %s{extra} ORDER BY id LIMIT %s OFFSET %s",
                tuple(params) + (page_size, (page - 1) * page_size),
            )
            return _page_payload(
                [self._log_row(r) for r in rows], page, page_size, total
            )
        query = _job_id_query(external_job_id)
        if level:
            query = {"bool": {"must": [query, {"term": {"level": level}}]}}
        rows, total = _search_page(
            self._search,
            self.settings.db_logs_table,
            query,
            page,
            page_size,
            sort=[{"time": {"order": "asc", "unmapped_type": "date"}}, {"_id": "asc"}],
        )
        return _page_payload([self._log_doc(d) for d in rows], page, page_size, total)

    def _success_clause(self, success, pk):
        params: list[Any] = [pk]
        if success is None:
            return "", params
        sqlite = getattr(self.settings, "db_dialect", "postgres") == "sqlite"
        if success is True:
            return (
                " AND success = %s" if sqlite else " AND success IS TRUE",
                params + ([1] if sqlite else []),
            )
        return (
            " AND success = %s" if sqlite else " AND success IS FALSE",
            params + ([0] if sqlite else []),
        )

    def _request_filters(self, success, pk, request_id):
        extra, params = self._success_clause(success, pk)
        if request_id is not None:
            extra += " AND id = %s"
            params = [*params, request_id]
        return extra, params

    @staticmethod
    def _request_row(row):
        return {
            "id": row[0],
            "url": row[1],
            "method": row[2],
            "status_code": row[3],
            "response_time_secs": row[4],
            "response_size_bytes": row[5],
            "success": row[6],
            "error": row[7],
            "parent_url": row[8],
            "parent_id": row[9],
            "fingerprint": row[10],
            "created_at": serialize_value(row[11]),
        }

    @staticmethod
    def _request_doc(doc):
        return {
            "id": doc.get("id", doc.get("_id")),
            "url": doc.get("url"),
            "method": doc.get("method"),
            "status_code": doc.get("status_code"),
            "response_time_secs": doc.get("response_time_secs"),
            "response_size_bytes": doc.get("response_size_bytes"),
            "success": doc.get("success"),
            "error": doc.get("error"),
            "parent_url": doc.get("parent_url"),
            "parent_id": doc.get("parent_id"),
            "fingerprint": doc.get("fingerprint"),
            "created_at": serialize_value(doc.get("created_at")),
        }

    @staticmethod
    def _log_row(row):
        return {
            "id": row[0],
            "time": serialize_value(row[1]),
            "level": row[2],
            "logger": row[3],
            "message": row[4],
            "exception": row[5],
        }

    @staticmethod
    def _log_doc(doc):
        return {
            "id": doc.get("_id"),
            "time": serialize_value(doc.get("time")),
            "level": doc.get("level"),
            "logger": doc.get("logger"),
            "message": doc.get("message"),
            "exception": doc.get("exception"),
        }
