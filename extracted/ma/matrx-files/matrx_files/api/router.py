"""The package's own API layer — mounted identically by host and standalone app.

Routers here are the package's public HTTP surface. Rules:
- Routers do NO work (thin: validate → call package service functions).
- Bare prefixes (host may strip a public /api/ itself).
- Every router added here must be mounted in standalone/app.py in the same
  change — a router that only exists in host mode violates INDEPENDENCE.md.
"""

from __future__ import annotations

from fastapi import APIRouter, Request, Response, status

from matrx_files._config import get_config
from matrx_files.cloud_sync.permissions import get_access_checker
from matrx_files.db.readiness import probe_database_readiness

# /files-service, NOT /files — build_file_router owns /files; this is the
# service-level health/identity router the independence gate probes.
router = APIRouter(prefix="/files-service", tags=["files-service"])


def _installed_version() -> str:
    from importlib.metadata import PackageNotFoundError, version

    try:
        return version("matrx-files")
    except PackageNotFoundError:
        return "0.0.0+unknown"


@router.get("/health")
async def health() -> dict[str, str]:
    get_config()  # proves the seam is wired; screams if not
    # `access_policy` is a standing alarm: "python-subset-fallback" means the
    # authoritative DB checker was never injected (configure_access_checker),
    # so container-derived files (crawl artifacts) 403 for legitimate users.
    # That exact state ran undetected on files.matrxserver.com (2026-07-29);
    # one curl now exposes it. `version` makes deploy verification external —
    # the FastAPI version string alone is invisible with docs disabled.
    return {
        "status": "ok",
        "package": "matrx-files",
        "version": _installed_version(),
        "access_policy": "db" if get_access_checker() is not None else "python-subset-fallback",
    }


@router.get("/ready")
async def readiness(response: Response, request: Request) -> dict[str, str]:
    response.headers["Cache-Control"] = "no-store"
    if getattr(request.app.state, "standalone_session_policy_required", False):
        from matrx_files.standalone.session_policy import session_policy_armed

        if not session_policy_armed(request.app):
            response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
            return {"status": "not_ready", "package": "matrx-files", "authority": "unconfigured"}
    probe = await probe_database_readiness()
    if not probe.ready:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return {
            "status": "not_ready",
            "package": "matrx-files",
            "database": "unavailable",
            "error_type": probe.error_type or "unknown",
        }
    if getattr(request.app.state, "standalone_session_policy_required", False):
        from matrx_files.standalone.preflight import verify_authority_contracts

        try:
            await verify_authority_contracts(request.app.state.file_session_policy)
        except Exception:
            response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
            return {"status": "not_ready", "package": "matrx-files", "authority": "unavailable"}
    return {"status": "ready", "package": "matrx-files", "database": "ok"}
