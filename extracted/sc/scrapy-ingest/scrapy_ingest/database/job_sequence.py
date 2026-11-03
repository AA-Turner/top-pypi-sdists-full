"""Job ids ``spider_id/run`` from ``ingest_spiders`` + ``ingest_jobs`` (no sequence table)."""

from __future__ import annotations

import logging
import time
from contextlib import contextmanager

from ..exceptions import DatabaseError
from ..utils.job_id import cache_job_id, cached_job_id, format_session_job
from .spiders import ensure_spider

logger = logging.getLogger(__name__)
_LOCK_KEY = "scrapy_ingest_job_id"
_PG_LOCK = 748901234


def resolve_configured_job_id(settings, spider):
    raw = settings.crawler_settings.get("JOB_ID")
    if raw in (None, ""):
        return None
    raw = str(raw).strip()
    if "/" in raw:
        return cache_job_id(spider, raw)
    sid = settings.job_session_id
    return cache_job_id(
        spider,
        format_session_job(sid, int(raw)) if sid is not None else raw,
    )


def resolve_job_key(db, settings, spider, job_key=None):
    job_key = job_key or resolve_configured_job_id(settings, spider) or cached_job_id(
        spider
    )
    if not job_key:
        job_key = allocate_job_id(db, settings, spider)
        cache_job_id(spider, job_key)
    return job_key


def allocate_job_id(db, settings, spider) -> str:
    sid = settings.job_session_id
    if sid is None:
        sid = (
            _max_session_prefix(db, settings) + 1
            if settings.job_new_session_per_crawl
            else ensure_spider(db, settings, spider)
        )
    return format_session_job(sid, _next_run(db, settings, sid))


def fallback_job_id_without_db(settings, spider) -> str:
    job_id = format_session_job(
        settings.job_session_id or 1, int(time.time() * 1000) % 1_000_000
    )
    logger.warning(
        "Sequential job ids require a database; using fallback job_id=%s", job_id
    )
    return cache_job_id(spider, job_id)


@contextmanager
def job_id_lock(db, settings):
    """Serialize id allocation + job row insert (parallel crawls)."""
    d = _dialect(db, settings)
    mysql_ok = False
    try:
        if d == "sqlite":
            db.execute("BEGIN IMMEDIATE")
        elif d == "postgres":
            db.execute("SELECT pg_advisory_xact_lock(%s)", (_PG_LOCK,))
        elif d == "mysql":
            row = db.execute("SELECT GET_LOCK(%s, 15)", (_LOCK_KEY,))
            mysql_ok = row is not None and int(row[0]) == 1
            if not mysql_ok:
                raise DatabaseError("Timed out waiting for job id lock")
        yield
    finally:
        if d == "mysql" and mysql_ok:
            db.execute("SELECT RELEASE_LOCK(%s)", (_LOCK_KEY,))


def _next_run(db, settings, sid: int) -> int:
    jobs = settings.db_jobs_table
    prefix = f"{sid}/"
    rows = db.fetchall(f"SELECT job_id FROM {jobs} WHERE job_id LIKE %s", (f"{prefix}%",))
    best = 0
    for (jid,) in rows or ():
        head, _, tail = str(jid).partition("/")
        if head == str(sid) and tail.isdigit():
            best = max(best, int(tail))
    return best + 1


def _max_session_prefix(db, settings) -> int:
    jobs = settings.db_jobs_table
    rows = db.fetchall(f"SELECT job_id FROM {jobs} WHERE job_id LIKE '%/%'")
    best = 0
    for (jid,) in rows or ():
        head, _, tail = str(jid).partition("/")
        if head.isdigit() and tail.isdigit():
            best = max(best, int(head))
    return best


def _dialect(db, settings) -> str:
    d = getattr(db, "_dialect", None)
    return d if d in ("postgres", "mysql", "sqlite") else settings.db_dialect
