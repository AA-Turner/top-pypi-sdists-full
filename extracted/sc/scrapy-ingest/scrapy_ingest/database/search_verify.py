"""Verify Elasticsearch / OpenSearch indexes match scrapy-ingest 2.1+ layout."""

from __future__ import annotations

from .search_helpers import ingest_search_indexes


def verify_search_indexes(client, settings) -> list[tuple[str, str, str, str]]:
    """
    Return check-config table rows: (step, index, status, detail).

    ``WARN`` rows flag legacy pre-2.1 documents or missing ``ingest_job_meta`` /
    ``ingest_spiders`` while jobs data exists. Warnings do not fail the ping step.
    """
    rows: list[tuple[str, str, str, str]] = []
    indexes = ingest_search_indexes(settings)
    jobs_index = settings.db_jobs_table
    meta_index = settings.db_job_meta_table
    items_index = settings.db_items_table

    jobs_has_docs = False
    for index in indexes:
        if not client.index_exists(index):
            rows.append(("indexes", index, "info", "not found; created on first crawl"))
            continue
        rows.append(("indexes", index, "OK", "present"))
        if index == jobs_index and client.index_has_documents(index):
            jobs_has_docs = True

    if jobs_has_docs and client.index_exists(jobs_index):
        sample = client.sample_document(jobs_index)
        if sample is not None:
            if "spider_name" in sample and "spider_id" not in sample:
                rows.append(
                    (
                        "indexes",
                        jobs_index,
                        "WARN",
                        "legacy job docs use spider_name; re-crawl or reindex for 2.1+",
                    )
                )
            elif "spider_id" not in sample:
                rows.append(
                    (
                        "indexes",
                        jobs_index,
                        "WARN",
                        "job docs lack spider_id; re-crawl for 2.1+ layout",
                    )
                )

    if jobs_has_docs and not client.index_exists(meta_index):
        rows.append(
            (
                "indexes",
                meta_index,
                "WARN",
                "missing while jobs index has data; re-crawl for ingest_job_meta",
            )
        )

    spiders_index = settings.db_spiders_table
    if jobs_has_docs and not client.index_exists(spiders_index):
        rows.append(
            (
                "indexes",
                spiders_index,
                "WARN",
                "missing while jobs index has data; re-crawl for ingest_spiders",
            )
        )

    if client.index_exists(items_index) and client.index_has_documents(items_index):
        sample = client.sample_document(items_index)
        job_id = sample.get("job_id") if sample else None
        if isinstance(job_id, str) and job_id.strip():
            rows.append(
                (
                    "indexes",
                    items_index,
                    "WARN",
                    "legacy items use string job_id; re-crawl for integer jobs.id FK",
                )
            )

    return rows
