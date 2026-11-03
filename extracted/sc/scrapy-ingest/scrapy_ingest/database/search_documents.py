"""Map ingest SQL table rows to Elasticsearch / OpenSearch documents."""

from __future__ import annotations

from typing import Any

from ..utils.serialization import json_safe, serialize_item_data
from .job_meta import collect_crawl_settings, collect_spider_args


def spider_row(*, row_id: int, name: str, class_path: str, created_at, updated_at) -> dict[str, Any]:
    return {
        "id": row_id,
        "name": name,
        "class_path": class_path,
        "created_at": created_at,
        "updated_at": updated_at,
    }


def job_row(
    *,
    row_id: int,
    job_id: str,
    spider_id: int,
    status: str,
    started_at,
    finished_at=None,
    finish_reason=None,
    requests_count=0,
    success_requests=0,
    failed_requests=0,
    items_count=0,
    logs_count=0,
    errors_count=0,
    items_per_min=0,
    elapsed_seconds=0,
) -> dict[str, Any]:
    return {
        "id": row_id,
        "job_id": job_id,
        "spider_id": spider_id,
        "status": status,
        "started_at": started_at,
        "finished_at": finished_at,
        "finish_reason": finish_reason,
        "requests_count": requests_count,
        "success_requests": success_requests,
        "failed_requests": failed_requests,
        "items_count": items_count,
        "logs_count": logs_count,
        "errors_count": errors_count,
        "items_per_min": items_per_min,
        "elapsed_seconds": elapsed_seconds,
    }


def job_meta_row(
    *,
    row_id: int,
    job_id: int,
    spider_args=None,
    crawl_settings=None,
    stats=None,
    updated_at=None,
) -> dict[str, Any]:
    return {
        "id": row_id,
        "job_id": job_id,
        "spider_args": json_safe(spider_args) if spider_args is not None else None,
        "crawl_settings": json_safe(crawl_settings) if crawl_settings is not None else None,
        "stats": json_safe(stats) if stats is not None else None,
        "updated_at": updated_at,
    }


def item_row(*, row_id: int, job_id: int, item, created_at) -> dict[str, Any]:
    return {
        "id": row_id,
        "job_id": job_id,
        "item": json_safe(serialize_item_data(item)),
        "created_at": created_at,
    }


def request_row_from(row_id: int, job_id: int, req: dict, created_at) -> dict[str, Any]:
    return request_row(
        row_id=row_id,
        job_id=job_id,
        url=req.get("url"),
        method=req.get("method"),
        status_code=req.get("status_code"),
        response_time_secs=req.get("response_time_secs"),
        response_size_bytes=req.get("response_size_bytes"),
        fingerprint=req.get("fingerprint"),
        parent_id=None,
        parent_url=req.get("parent_url"),
        error=req.get("error"),
        success=req.get("success"),
        created_at=created_at,
    )


def request_row(
    *,
    row_id: int,
    job_id: int,
    url,
    method,
    status_code,
    response_time_secs,
    response_size_bytes,
    fingerprint,
    parent_id,
    parent_url,
    error,
    success,
    created_at,
) -> dict[str, Any]:
    return {
        "id": row_id,
        "job_id": job_id,
        "url": url,
        "method": method,
        "status_code": status_code,
        "response_time_secs": response_time_secs,
        "response_size_bytes": response_size_bytes,
        "fingerprint": fingerprint,
        "parent_id": parent_id,
        "parent_url": parent_url,
        "error": error,
        "success": success,
        "created_at": created_at,
    }


def log_row_from(row_id: int, job_id: int, entry: dict, iso) -> dict[str, Any]:
    return log_row(
        row_id=row_id,
        job_id=job_id,
        time=iso(entry.get("time")),
        level=entry.get("level"),
        logger=entry.get("logger"),
        message=entry.get("message"),
        exception=entry.get("exception"),
    )


def log_row(*, row_id: int, job_id: int, time, level, logger, message, exception) -> dict[str, Any]:
    return {
        "id": row_id,
        "job_id": job_id,
        "time": time,
        "level": level,
        "logger": logger,
        "message": message,
        "exception": exception,
    }


def collect_job_meta_from_spider(spider) -> tuple[dict, dict | None]:
    args = collect_spider_args(spider)
    crawl = collect_crawl_settings(spider)
    return json_safe(args), json_safe(crawl) if crawl else None

