"""Job id helpers: ``spider_id/run`` format and legacy fallbacks."""

import time
import uuid


def format_session_job(session_id: int, run_seq: int) -> str:
    return f"{int(session_id)}/{int(run_seq)}"


def generate_job_id(spider_name):
    """Legacy fallback when no database is available (not sequential)."""
    return f"{spider_name}-{int(time.time())}-{uuid.uuid4().hex[:4]}"


def cache_job_id(spider, job_id):
    """Remember the resolved job_id on spider and crawler."""
    spider._ingest_job_id = job_id
    crawler = getattr(spider, "crawler", None)
    if crawler is not None:
        crawler.ingest_job_id = job_id
    return job_id


def cached_job_id(spider):
    crawler = getattr(spider, "crawler", None)
    if crawler is not None:
        raw = getattr(crawler, "ingest_job_id", None)
        if isinstance(raw, str) and raw.strip():
            return raw.strip()
    raw = getattr(spider, "_ingest_job_id", None)
    if isinstance(raw, str) and raw.strip():
        return raw.strip()
    return None
