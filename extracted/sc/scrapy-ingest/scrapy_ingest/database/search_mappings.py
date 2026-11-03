"""Elasticsearch / OpenSearch index mappings aligned with SQL ingest tables."""

from __future__ import annotations

_LONG = {"type": "long"}
_KEYWORD = {"type": "keyword"}
_DATE = {"type": "date", "ignore_malformed": True}
_BOOL = {"type": "boolean"}
_FLOAT = {"type": "float"}

_ROLE_MAPPINGS: dict[str, dict] = {
    "spiders": {
        "properties": {
            "id": _LONG,
            "name": _KEYWORD,
            "class_path": _KEYWORD,
            "created_at": _DATE,
            "updated_at": _DATE,
        }
    },
    "jobs": {
        "properties": {
            "id": _LONG,
            "job_id": _KEYWORD,
            "spider_id": _LONG,
            "status": _KEYWORD,
            "started_at": _DATE,
            "finished_at": _DATE,
            "finish_reason": _KEYWORD,
            "requests_count": _LONG,
            "success_requests": _LONG,
            "failed_requests": _LONG,
            "items_count": _LONG,
            "logs_count": _LONG,
            "errors_count": _LONG,
            "items_per_min": _FLOAT,
            "elapsed_seconds": _FLOAT,
        }
    },
    "job_meta": {
        "properties": {
            "id": _LONG,
            "job_id": _LONG,
            "updated_at": _DATE,
        }
    },
    "items": {
        "properties": {
            "id": _LONG,
            "job_id": _LONG,
            "created_at": _DATE,
        }
    },
    "requests": {
        "properties": {
            "id": _LONG,
            "job_id": _LONG,
            "fingerprint": _KEYWORD,
            "method": _KEYWORD,
            "status_code": _LONG,
            "parent_id": _LONG,
            "success": _BOOL,
            "created_at": _DATE,
        }
    },
    "logs": {
        "properties": {
            "id": _LONG,
            "job_id": _LONG,
            "level": _KEYWORD,
            "logger": _KEYWORD,
            "time": _DATE,
        }
    },
}


def index_role(index_name: str, settings) -> str | None:
    if index_name == settings.db_spiders_table:
        return "spiders"
    if index_name == settings.db_jobs_table:
        return "jobs"
    if index_name == settings.db_job_meta_table:
        return "job_meta"
    if index_name == settings.db_items_table:
        return "items"
    if index_name == settings.db_requests_table:
        return "requests"
    if index_name == settings.db_logs_table:
        return "logs"
    return None


def index_create_body(index_name: str, settings) -> dict | None:
    """Return create-index body for known ingest indexes, else ``None`` (dynamic mapping)."""
    role = index_role(index_name, settings)
    if role is None:
        return None
    mapping = _ROLE_MAPPINGS.get(role)
    if mapping is None:
        return None
    return {"mappings": mapping}
