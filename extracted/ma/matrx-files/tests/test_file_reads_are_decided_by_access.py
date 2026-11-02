"""A file read is decided by ACCESS to the file, never refused for a missing organization.

Law: common-docs/policies/access-ladder.md §3/§4/§8 (Arman, 2026-09-23). Seen live
(GATES-TAIL, VERIFIER-21 #2, 2026-09-25): a fresh session with no organization picked opened
``/files/f/<id>`` and the standalone files service answered ``400 organization_required`` to
``GET /files/<id>`` and ``POST /files/session`` before any handler could decide access — while
``read_record`` decides it by ``files.has_access_for`` as the person, and the file-session
cookie is minted for the PERSON (``mint_session_cookie_value(user_id, …)``), not for an org.

Through the REAL routers and the REAL ``AuthMiddleware`` admission rule, configured by the
same ``admission_config`` the service boots with:

* the per-file reads and the session mint are admitted with no organization, and with an
  organization header the person is not a member of (the FILE's organization, which the
  frontend now sends for a file shared to her personally);
* every write and run beside them is still refused without one — the gate did not open.
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest
from fastapi import FastAPI
from matrx_connect.middleware.auth import AuthMiddleware
from starlette.requests import Request

from matrx_files.api import build_asset_router, build_file_router
from matrx_files.standalone.admission import admission_config

USER_ID = "11111111-1111-4111-8111-111111111111"
FILE = "7a2b3c4d-0000-4000-8000-00000000f001"


@pytest.fixture(scope="module")
def middleware() -> AuthMiddleware:
    app = FastAPI()
    service = SimpleNamespace()
    app.include_router(build_file_router(service))  # type: ignore[arg-type]
    app.include_router(build_asset_router(service))  # type: ignore[arg-type]

    async def _inner(scope, receive, send):  # pragma: no cover - never called
        raise AssertionError("admission is asked directly")

    return AuthMiddleware(
        _inner,
        jwt_secret="test-secret-do-not-use-in-prod-test-secret-do-not-use-in-prod-AB",
        **admission_config(app, public_paths=("/files-service/health",)),
    )


def _reason(mw: AuthMiddleware, method: str, path: str, *, admission: str = "none") -> str | None:
    request = Request(
        {
            "type": "http",
            "method": method,
            "path": path,
            "raw_path": path.encode(),
            "query_string": b"",
            "headers": [],
        }
    )
    ctx = SimpleNamespace(
        user_id=USER_ID,
        auth_type="jwt",
        organization_id=None,
        organization_admission=admission,
        claimed_organization_id=None,
    )
    return mw._organization_admission_reason(request, ctx)


ADMITTED = [
    ("GET", f"/files/{FILE}"),
    ("GET", f"/files/{FILE}/download"),
    ("GET", f"/files/{FILE}/asset"),
    ("GET", f"/assets/{FILE}"),
    ("POST", "/files/session"),
]


@pytest.mark.parametrize(("method", "path"), ADMITTED)
def test_a_file_read_and_the_session_are_admitted_without_an_organization(middleware, method, path):
    assert _reason(middleware, method, path) is None, (
        f"{method} {path} is refused for a missing organization; access is decided by the file."
    )


@pytest.mark.parametrize(("method", "path"), ADMITTED)
def test_a_file_read_is_admitted_with_the_files_organization_she_is_not_a_member_of(middleware, method, path):
    assert _reason(middleware, method, path, admission="denied") is None


STILL_REFUSED = [
    ("POST", "/files/upload"),
    ("PATCH", f"/files/{FILE}"),
    ("DELETE", f"/files/{FILE}"),
    ("POST", f"/files/{FILE}/restore"),
    ("POST", f"/files/{FILE}/share-links"),
    ("POST", f"/files/{FILE}/pdf-pages"),
    ("POST", "/files/bulk"),
    ("POST", "/assets"),
    # a GET declaration never admits another method on the same template
    ("POST", f"/files/{FILE}/download"),
    # not a sibling that shares a stem with the session path
    ("POST", "/files/session/extra"),
]


@pytest.mark.parametrize(("method", "path"), STILL_REFUSED)
def test_writes_and_runs_still_need_an_organization(middleware, method, path):
    assert _reason(middleware, method, path) is not None


def test_only_reads_are_declared(middleware):
    for entry in middleware._authenticated_resource_routes:
        assert entry.method in {"GET", "HEAD"}, entry


def test_the_marker_enforces_nothing_so_the_cookie_lane_keeps_rendering():
    """matrx-connect's authenticated_resource_bootstrap demands is_authenticated, which is False
    on the file-session cookie lane every <img> byte GET rides; the files marker must not."""
    import asyncio

    from matrx_files.api.read_by_access import file_read_decided_by_access

    assert asyncio.run(file_read_decided_by_access()) is None


def test_composition_refuses_a_declared_write_and_a_lost_canary():
    from fastapi import APIRouter, Depends

    from matrx_files.api.read_by_access import file_read_decided_by_access
    from matrx_files.standalone.admission import compose_file_reads

    app = FastAPI()
    router = APIRouter()

    @router.post("/files/{file_id}/thing", dependencies=[Depends(file_read_decided_by_access)])
    async def write_thing(file_id: str) -> None:  # pragma: no cover
        return None

    app.include_router(router)
    with pytest.raises(RuntimeError, match="not a read"):
        compose_file_reads(app)
    with pytest.raises(RuntimeError, match="lost known entries"):
        compose_file_reads(FastAPI())
