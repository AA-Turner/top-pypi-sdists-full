"""Sequential ``spider_id/run`` job ids when ingest uses search without SQL."""

from ..utils.job_id import cache_job_id, cached_job_id, format_session_job
from .job_sequence import resolve_configured_job_id


def resolve_job_key_search(client, settings, spider, job_key=None):
    job_key = job_key or resolve_configured_job_id(settings, spider) or cached_job_id(spider)
    if job_key:
        return cache_job_id(spider, job_key)
    spider_id = client.ensure_spider(settings, spider)
    job_key = format_session_job(spider_id, client.next_job_run(settings, spider_id))
    spider._ingest_spider_id = spider_id
    return cache_job_id(spider, job_key)
