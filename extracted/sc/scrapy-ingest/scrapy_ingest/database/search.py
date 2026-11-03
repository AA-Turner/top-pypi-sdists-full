"""Bulk index ingest batches to Elasticsearch or OpenSearch."""

import logging
import warnings
from contextlib import contextmanager
from datetime import datetime

from opensearchpy import OpenSearch
from opensearchpy.exceptions import NotFoundError, OpenSearchWarning
from opensearchpy.helpers import bulk as os_bulk

from ..constants import CLIENT_NAME
from ..exceptions import IngestConnectionError
from ..utils.metrics import compute_errors_count, count_standalone_log_errors
from ..utils.serialization import json_safe
from ..utils.time import get_current_datetime

logger = logging.getLogger(__name__)


@contextmanager
def _ignore_cluster_warnings():
    """Elasticsearch may return advisory Warning headers (e.g. security disabled)."""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", OpenSearchWarning)
        yield


class SearchClient:
    """OpenSearch client wrapper (Elasticsearch-compatible REST API)."""

    def __init__(self, settings):
        url = settings.search_url.rstrip("/")
        kwargs = {
            "verify_certs": settings.search_ssl_verify,
            "ssl_show_warn": settings.search_ssl_verify,
            "use_ssl": url.startswith("https://"),
            "opaque_id": CLIENT_NAME,
        }
        if settings.search_user:
            kwargs["http_auth"] = (settings.search_user, settings.search_password or "")

        self._bulk = os_bulk
        self._client = OpenSearch(hosts=[url], **kwargs)
        self._ready = set()
        self.settings = settings

    def ping(self):
        with _ignore_cluster_warnings():
            ok = self._client.ping()
        if not ok:
            raise IngestConnectionError("Search cluster did not respond to ping")

    def close(self):
        self._client.close()

    def index_exists(self, name: str) -> bool:
        with _ignore_cluster_warnings():
            return bool(self._client.indices.exists(index=name))

    def index_has_documents(self, name: str) -> bool:
        if not self.index_exists(name):
            return False
        with _ignore_cluster_warnings():
            resp = self._client.count(index=name)
        return int(resp.get("count") or 0) > 0

    def sample_document(self, index: str):
        hits = self._search(index, {"size": 1, "query": {"match_all": {}}}).get(
            "hits", {}
        ).get("hits", [])
        if not hits:
            return None
        return hits[0].get("_source")

    def ensure_index(self, name):
        if name in self._ready:
            return
        with _ignore_cluster_warnings():
            if not self._client.indices.exists(index=name):
                from .search_mappings import index_create_body

                body = index_create_body(name, self.settings)
                if body:
                    self._client.indices.create(index=name, body=body)
                else:
                    self._client.indices.create(index=name)
        self._ready.add(name)

    def index(self, index, doc_id, doc):
        self.ensure_index(index)
        with _ignore_cluster_warnings():
            self._client.index(index=index, id=doc_id, body=json_safe(doc))

    def bulk(self, index, docs):
        if not docs:
            return
        self.ensure_index(index)
        actions = []
        for doc in docs:
            payload = json_safe(dict(doc))
            row_id = payload.get("id")
            action = {"_index": index, "_source": payload}
            if row_id is not None:
                action["_id"] = str(row_id)
            actions.append(action)
        with _ignore_cluster_warnings():
            _, errors = self._bulk(self._client, actions, raise_on_error=False)
        if errors:
            logger.warning("Search bulk had %s error(s)", len(errors))

    def _search(self, index, body):
        with _ignore_cluster_warnings():
            return self._client.search(index=index, body=body)

    @staticmethod
    def _should(field, value):
        return {"bool": {"should": [{"term": {field: value}}, {"term": {f"{field}.keyword": value}}], "minimum_should_match": 1}}

    @staticmethod
    def _wildcard(field, needle):
        pat = f"*{needle}*"
        return {"bool": {"should": [{"wildcard": {field: pat}}, {"wildcard": {f"{field}.keyword": pat}}], "minimum_should_match": 1}}

    def next_sequence_id(self, index: str) -> int:
        self.ensure_index(index)
        try:
            val = self._search(index, {"size": 0, "aggs": {"max_id": {"max": {"field": "id"}}}}).get(
                "aggregations", {}
            ).get("max_id", {}).get("value")
            if val is not None:
                return int(val) + 1
        except NotFoundError:
            pass
        except Exception:
            logger.debug("max id agg failed for %s", index, exc_info=True)
        return 1

    def allocate_ids(self, index: str, count: int) -> list[int]:
        if count <= 0:
            return []
        start = self.next_sequence_id(index)
        return list(range(start, start + count))

    def find_spider_by_name(self, index: str, name: str):
        hits = self._search(index, {"size": 1, "query": self._should("name", name)}).get("hits", {}).get("hits", [])
        return hits[0].get("_source") if hits else None

    def spider_ids_for_filter(self, index: str, needle: str) -> list[int]:
        hits = self._search(
            index,
            {"size": 500, "_source": ["id"], "query": self._wildcard("name", needle)},
        ).get("hits", {}).get("hits", [])
        return [int(h["_source"]["id"]) for h in hits if h.get("_source", {}).get("id") is not None]

    def spider_names_by_id(self, index: str, spider_ids: set[int]) -> dict[int, str]:
        ids = [int(x) for x in spider_ids if x is not None]
        if not ids:
            return {}
        hits = self._search(index, {"size": len(ids), "query": {"terms": {"id": ids}}}).get("hits", {}).get(
            "hits", []
        )
        return {
            int(src["id"]): src["name"]
            for h in hits
            if (src := h.get("_source")) and src.get("id") is not None and src.get("name")
        }

    def get_document(self, index, doc_id):
        """Return document ``_source`` or ``None`` if not found."""
        try:
            with _ignore_cluster_warnings():
                resp = self._client.get(index=index, id=doc_id)
            return resp.get("_source")
        except NotFoundError:
            return None

    def search_documents(self, index, *, size=50, sort_field="started_at", filters=()):
        """Return ``_source`` dicts, newest first. Optional *filters* are ES ``bool.filter`` clauses."""
        query = {"match_all": {}}
        if filters:
            query = {"bool": {"filter": list(filters)}}
        body = {
            "size": size,
            "sort": [{sort_field: {"order": "desc", "unmapped_type": "date"}}],
            "query": query,
        }
        return [hit["_source"] for hit in self._search(index, body).get("hits", {}).get("hits", [])]

    @staticmethod
    def _iso(value):
        if isinstance(value, datetime):
            return value.isoformat()
        return value

    def ensure_spider(self, settings, spider) -> int:
        from .search_documents import spider_row
        from .spiders import spider_class_path

        index = settings.db_spiders_table
        name = (getattr(spider, "name", None) or "spider").strip()[:255]
        path = spider_class_path(spider)[:512]
        now = get_current_datetime(settings)
        if existing := self.find_spider_by_name(index, name):
            row_id = int(existing["id"])
            self.index(
                index,
                str(row_id),
                spider_row(
                    row_id=row_id,
                    name=name,
                    class_path=path,
                    created_at=existing.get("created_at") or self._iso(now),
                    updated_at=self._iso(now),
                ),
            )
            return row_id
        row_id = self.next_sequence_id(index)
        self.index(
            index,
            str(row_id),
            spider_row(
                row_id=row_id,
                name=name,
                class_path=path,
                created_at=self._iso(now),
                updated_at=self._iso(now),
            ),
        )
        return row_id

    def next_job_run(self, settings, spider_id: int) -> int:
        from .search_helpers import parse_job_run

        index = settings.db_jobs_table
        self.ensure_index(index)
        prefix = f"{spider_id}/"
        body = {"size": 500, "query": {"prefix": {"job_id.keyword": prefix}}, "_source": ["job_id"]}
        try:
            hits = self._search(index, body).get("hits", {}).get("hits", [])
        except Exception:
            try:
                hits = self._search(
                    index, {"size": 500, "query": {"wildcard": {"job_id": f"{prefix}*"}}, "_source": ["job_id"]}
                ).get("hits", {}).get("hits", [])
            except Exception:
                return 1
        best = max(
            (r for h in hits if (r := parse_job_run((h.get("_source") or {}).get("job_id") or h.get("_id") or "", spider_id)) is not None),
            default=0,
        )
        return best + 1

    def iter_documents(
        self,
        index,
        *,
        query=None,
        size=500,
        sort=None,
    ):
        """Yield ``_source`` dicts using ``search_after`` pagination."""
        sort = sort or [{"created_at": {"order": "asc", "unmapped_type": "date"}}]
        search_after = None
        while True:
            body = {
                "size": size,
                "sort": sort,
                "query": query or {"match_all": {}},
            }
            if search_after is not None:
                body["search_after"] = search_after
            hits = self._search(index, body).get("hits", {}).get("hits", [])
            if not hits:
                break
            for hit in hits:
                if (source := hit.get("_source")) is not None:
                    yield source
            search_after = hits[-1].get("sort")


class SearchWriter:
    """Index collector batches into search indexes (same shape as SQL tables)."""

    def __init__(self, client, settings):
        self.client = client
        self.settings = settings
        self._counts = {
            "items_count": 0,
            "requests_count": 0,
            "success_requests": 0,
            "failed_requests": 0,
            "logs_count": 0,
            "errors_count": 0,
        }
        self._standalone_log_errors = 0
        self._started_at = None
        self._external_job_id = None
        self._job_pk = None
        self._meta_pk = None
        self._spider_id = None
        self._spider_args = None
        self._crawl_settings = None
        self._status = "running"
        from .search_helpers import ingest_search_indexes

        for table in ingest_search_indexes(settings):
            client.ensure_index(table)

    _iso = staticmethod(SearchClient._iso)

    def start_job(self, external_job_id, spider, job_pk=None):
        from .search_documents import collect_job_meta_from_spider, job_meta_row, job_row

        self._started_at = get_current_datetime(self.settings)
        self._counts = {key: 0 for key in self._counts}
        self._standalone_log_errors = 0
        self._external_job_id = external_job_id
        self._spider_id = self.client.ensure_spider(self.settings, spider)
        spider._ingest_spider_id = self._spider_id
        self._spider_args, self._crawl_settings = collect_job_meta_from_spider(spider)
        jobs = self.settings.db_jobs_table
        meta = self.settings.db_job_meta_table
        self._job_pk = int(job_pk) if job_pk is not None else self.client.next_sequence_id(jobs)
        self._meta_pk = self.client.next_sequence_id(meta)
        now = self._iso(self._started_at)
        self._status = "running"
        self.client.index(
            jobs,
            external_job_id,
            job_row(
                row_id=self._job_pk,
                job_id=external_job_id,
                spider_id=self._spider_id,
                status=self._status,
                started_at=now,
            ),
        )
        self.client.index(
            meta,
            str(self._meta_pk),
            job_meta_row(
                row_id=self._meta_pk,
                job_id=self._job_pk,
                spider_args=self._spider_args,
                crawl_settings=self._crawl_settings,
                updated_at=now,
            ),
        )
        return self._job_pk

    def write(self, data, external_job_id=None):
        from .search_documents import item_row, log_row_from, request_row_from

        if external_job_id and not self._external_job_id:
            self._external_job_id = external_job_id
        if self._job_pk is None:
            return
        stamp = self._iso(get_current_datetime(self.settings))
        job_pk = self._job_pk
        raw_items = data.get("items") or []
        raw_requests = data.get("requests") or []
        raw_logs = data.get("logs") or []
        item_docs = [
            item_row(row_id=rid, job_id=job_pk, item=item, created_at=stamp)
            for rid, item in zip(self.client.allocate_ids(self.settings.db_items_table, len(raw_items)), raw_items)
        ]
        request_docs = [
            request_row_from(rid, job_pk, req, stamp)
            for rid, req in zip(
                self.client.allocate_ids(self.settings.db_requests_table, len(raw_requests)), raw_requests
            )
        ]
        log_docs = [
            log_row_from(rid, job_pk, entry, self._iso)
            for rid, entry in zip(self.client.allocate_ids(self.settings.db_logs_table, len(raw_logs)), raw_logs)
        ]
        self.client.bulk(self.settings.db_items_table, item_docs)
        self.client.bulk(self.settings.db_requests_table, request_docs)
        self.client.bulk(self.settings.db_logs_table, log_docs)
        self._counts["items_count"] += len(item_docs)
        self._counts["requests_count"] += len(request_docs)
        self._counts["success_requests"] += sum(
            1 for req in request_docs if req.get("success")
        )
        self._counts["failed_requests"] += sum(
            1 for req in request_docs if req.get("success") is False
        )
        self._counts["logs_count"] += len(log_docs)
        self._standalone_log_errors += count_standalone_log_errors(log_docs)
        self._counts["errors_count"] = compute_errors_count(
            self._counts["failed_requests"],
            self._standalone_log_errors,
        )
        if not self._spider_args and request_docs:
            url = request_docs[0].get("url")
            if url:
                self._spider_args = {"url": url}
                self._save_meta(updated_at=stamp)
        self._save_job()

    def _elapsed(self, end_time=None):
        end = end_time or get_current_datetime(self.settings)
        if self._started_at is None:
            return 0.0, 0.0
        elapsed = max((end - self._started_at).total_seconds(), 0.0)
        if elapsed <= 0:
            return 0.0, 0.0
        return round(elapsed, 2), round(self._counts["items_count"] / elapsed * 60, 2)

    def _save_job(self, end_time=None, *, status=None, finished_at=None, finish_reason=None):
        from .search_documents import job_row

        if self._job_pk is None or not self._external_job_id:
            return
        elapsed, rate = self._elapsed(end_time)
        self.client.index(
            self.settings.db_jobs_table,
            self._external_job_id,
            job_row(
                row_id=self._job_pk,
                job_id=self._external_job_id,
                spider_id=self._spider_id,
                status=status or self._status,
                started_at=self._iso(self._started_at),
                finished_at=finished_at,
                finish_reason=finish_reason,
                **self._counts,
                items_per_min=rate,
                elapsed_seconds=elapsed,
            ),
        )

    def _save_meta(self, *, stats=None, updated_at=None):
        from .search_documents import job_meta_row

        if self._meta_pk is None or self._job_pk is None:
            return
        stamp = updated_at or self._iso(get_current_datetime(self.settings))
        self.client.index(
            self.settings.db_job_meta_table,
            str(self._meta_pk),
            job_meta_row(
                row_id=self._meta_pk,
                job_id=self._job_pk,
                spider_args=self._spider_args,
                crawl_settings=self._crawl_settings,
                stats=json_safe(stats) if stats else None,
                updated_at=stamp,
            ),
        )

    def finish_job(self, external_job_id=None, reason=None, stats=None):
        finished_at = get_current_datetime(self.settings)
        if stats and not reason:
            reason = stats.get("finish_reason")
        elapsed, rate = self._elapsed(finished_at)
        self._status = "finished"
        self._save_job(
            end_time=finished_at,
            status="finished",
            finished_at=self._iso(finished_at),
            finish_reason=reason,
        )
        self._save_meta(stats=stats, updated_at=self._iso(finished_at))
        return {
            **self._counts,
            "elapsed_seconds": elapsed,
            "items_per_min": rate,
            "reason": reason,
        }
