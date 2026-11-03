"""FastAPI routes and static UI for scrapy-ingest dashboard."""

from __future__ import annotations

from pathlib import Path
from typing import Callable

from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from ..connection_info import build_connection_info
from ..queries import IngestReader
from ..settings_loader import load_ingest_settings
from .errors import DashboardErrorsASGI, invoke_reader, register_exception_handlers

_STATIC = Path(__file__).resolve().parent.parent / "static"
_FAVICON = _STATIC / "assets" / "branding" / "favicon.png"


def create_app(*, db_url: str | None = None, search_url: str | None = None) -> FastAPI:
    settings = load_ingest_settings(db_url=db_url, search_url=search_url)

    def get_reader():
        reader = IngestReader(settings)
        try:
            yield reader
        finally:
            reader.close()

    app = FastAPI(title="scrapy-ingest Dashboard")
    register_exception_handlers(app)

    def ensure_job(job_id: str, ingest: IngestReader) -> None:
        if invoke_reader(ingest.get_job, job_id) is None:
            raise HTTPException(status_code=404, detail="job not found")

    def job_page(
        loader: Callable,
        job_id: str,
        page: int,
        page_size: int,
        ingest: IngestReader,
        **extra,
    ):
        ensure_job(job_id, ingest)
        return invoke_reader(
            loader, job_id, page=page, page_size=page_size, **extra
        )

    @app.get("/api/health")
    def health():
        return build_connection_info(settings, uses_sql=settings.ingest_to_database)

    @app.get("/api/dashboard")
    def jobs_dashboard(
        ingest: IngestReader = Depends(get_reader),
        status: str | None = None,
        spider: str | None = None,
    ):
        return invoke_reader(ingest.jobs_dashboard, status=status, spider=spider)

    @app.get("/api/jobs")
    def list_jobs(
        ingest: IngestReader = Depends(get_reader),
        page: int = Query(1, ge=1),
        page_size: int = Query(25, ge=1, le=200),
        status: str | None = None,
        spider: str | None = None,
    ):
        return invoke_reader(
            ingest.list_jobs,
            page=page,
            page_size=page_size,
            status=status,
            spider=spider,
        )

    @app.get("/api/jobs/{job_id:path}/items")
    def list_items(
        job_id: str,
        ingest: IngestReader = Depends(get_reader),
        page: int = Query(1, ge=1),
        page_size: int = Query(50, ge=1, le=200),
    ):
        return job_page(ingest.list_items, job_id, page, page_size, ingest)

    @app.get("/api/jobs/{job_id:path}/requests")
    def list_requests(
        job_id: str,
        ingest: IngestReader = Depends(get_reader),
        page: int = Query(1, ge=1),
        page_size: int = Query(50, ge=1, le=200),
        success: bool | None = None,
        request_id: int | None = None,
    ):
        return job_page(
            ingest.list_requests,
            job_id,
            page,
            page_size,
            ingest,
            success=success,
            request_id=request_id,
        )

    @app.get("/api/jobs/{job_id:path}/logs")
    def list_logs(
        job_id: str,
        ingest: IngestReader = Depends(get_reader),
        page: int = Query(1, ge=1),
        page_size: int = Query(25, ge=1, le=500),
        level: str | None = None,
    ):
        return job_page(ingest.list_logs, job_id, page, page_size, ingest, level=level)

    @app.get("/api/jobs/{job_id:path}")
    def get_job(job_id: str, ingest: IngestReader = Depends(get_reader)):
        job = invoke_reader(ingest.get_job, job_id)
        if job is None:
            raise HTTPException(status_code=404, detail="job not found")
        return job

    app.mount("/assets", StaticFiles(directory=_STATIC / "assets"), name="assets")

    @app.get("/favicon.ico", include_in_schema=False)
    def favicon():
        return FileResponse(_FAVICON, media_type="image/png")

    @app.get("/")
    def index():
        return FileResponse(_STATIC / "index.html")

    return DashboardErrorsASGI(app)
