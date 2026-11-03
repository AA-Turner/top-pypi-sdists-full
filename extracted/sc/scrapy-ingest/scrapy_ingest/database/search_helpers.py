"""Shared Elasticsearch / OpenSearch query helpers."""


def ingest_search_indexes(settings):
    return (
        settings.db_spiders_table,
        settings.db_jobs_table,
        settings.db_job_meta_table,
        settings.db_items_table,
        settings.db_requests_table,
        settings.db_logs_table,
    )


def search_job_filters(client, settings, *, status=None, spider=None):
    filters = []
    if status:
        filters.append({"term": {"status": status}})
    if spider and (needle := spider.strip()):
        ids = client.spider_ids_for_filter(settings.db_spiders_table, needle)
        filters.append({"terms": {"spider_id": ids}} if ids else {"term": {"spider_id": -1}})
    return filters


def search_jobs_query(client, settings, *, status=None, spider=None):
    filters = search_job_filters(client, settings, status=status, spider=spider)
    return {"match_all": {}} if not filters else {"bool": {"filter": filters}}


def parse_job_run(job_id: str, spider_id: int) -> int | None:
    head, _, tail = str(job_id).partition("/")
    if head == str(spider_id) and tail.isdigit():
        return int(tail)
    return None
