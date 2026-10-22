"""Map ingest/destination errors to dashboard HTTP responses."""

from __future__ import annotations

import logging
import re
import sqlite3
import time
from collections.abc import Callable
from typing import Any

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

from scrapy_ingest.exceptions import IngestError

logger = logging.getLogger(__name__)
_LOG_DEDUPE = 60.0
_log_at: dict[str, float] = {}

_DEST_HINTS = (
    (
        re.compile(r"no such table", re.I),
        "Ingest tables are not set up in this database yet. "
        "Run a spider with scrapy-ingest enabled, or verify DB_URL and table names.",
    ),
    (
        re.compile(r'relation ".+" does not exist', re.I),
        "Ingest tables are missing in this database. "
        "Run a crawl with scrapy-ingest enabled, or check DB_URL and schema.",
    ),
    (
        re.compile(r"index_not_found_exception|index_not_found|no such index", re.I),
        "Ingest search indexes are missing. "
        "Run a spider with scrapy-ingest enabled, or verify SEARCH_URL and index names "
        "(ingest_jobs, ingest_items, ingest_requests, ingest_logs).",
    ),
    (
        re.compile(r"packet sequence number wrong", re.I),
        "Database connection was interrupted. Refresh the page; if it persists, restart the dashboard.",
    ),
)


def _dest_message(exc: BaseException) -> str | None:
    msg = str(exc).strip()
    if not msg:
        return None
    for pat, text in _DEST_HINTS:
        if pat.search(msg):
            return text
    return None


def _503(detail: str) -> HTTPException:
    return HTTPException(status_code=503, detail=detail)


def http_exception_for(exc: BaseException) -> HTTPException:
    if hint := _dest_message(exc):
        return _503(hint)
    if isinstance(exc, IngestError):
        return _503(str(exc) or "Ingest error.")
    if isinstance(exc, sqlite3.Error):
        return _503(
            _dest_message(exc)
            or "Database error. Check DB_URL and that ingest tables exist."
        )
    try:
        import pymysql

        if isinstance(exc, pymysql.Error):
            return _503(
                _dest_message(exc)
                or "Database error. Check connection settings and ingest tables."
            )
    except ImportError:
        pass
    mod = type(exc).__module__ or ""
    if any(part in mod for part in ("psycopg2", "pymysql", "sqlite3")):
        return _503(
            _dest_message(exc)
            or "Database error. Check connection settings and ingest tables."
        )
    if "opensearch" in mod or "elasticsearch" in mod:
        hint = _dest_message(exc)
        detail = hint or "Search cluster error. Check SEARCH_URL and index setup."
        msg = str(exc).strip()
        if msg and msg not in detail:
            detail = f"{detail} ({type(exc).__name__}: {msg})"
        return _503(detail)
    if isinstance(exc, RuntimeError) and "No ingest destination" in str(exc):
        return _503(
            "No ingest destination configured. Set DB_URL or SEARCH_URL in Scrapy settings."
        )
    if isinstance(exc, (ConnectionError, TimeoutError, OSError)):
        return _503(
            "Could not reach the ingest destination. Check network and connection settings."
        )
    return HTTPException(
        status_code=500,
        detail="An unexpected error occurred while loading dashboard data.",
    )


def _warn_once(exc: BaseException, mapped: HTTPException) -> None:
    line = f"{mapped.detail} ({type(exc).__name__}: {exc or type(exc).__name__})"
    now = time.monotonic()
    if now - _log_at.get(line, 0) < _LOG_DEDUPE:
        return
    _log_at[line] = now
    logger.warning("%s", line)


def _handle(exc: BaseException) -> HTTPException:
    mapped = http_exception_for(exc)
    _warn_once(exc, mapped)
    return mapped


def _json_error(mapped: HTTPException) -> JSONResponse:
    detail = mapped.detail if isinstance(mapped.detail, str) else str(mapped.detail)
    return JSONResponse(status_code=mapped.status_code, content={"detail": detail})


def invoke_reader(func: Callable[..., Any], /, *args: Any, **kwargs: Any) -> Any:
    try:
        return func(*args, **kwargs)
    except HTTPException:
        raise
    except Exception as exc:
        raise _handle(exc) from None


class DashboardErrorsASGI:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        started = False

        async def send_wrapper(message):
            nonlocal started
            if message["type"] == "http.response.start":
                started = True
            await send(message)

        try:
            await self.app(scope, receive, send_wrapper)
        except Exception as exc:
            if started:
                raise
            mapped = exc if isinstance(exc, HTTPException) else _handle(exc)
            await _json_error(mapped)(scope, receive, send)


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(HTTPException)
    async def _http(_request: Request, exc: HTTPException) -> JSONResponse:
        return _json_error(exc)
