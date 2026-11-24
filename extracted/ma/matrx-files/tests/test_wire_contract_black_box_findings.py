"""Black-box findings against files.matrxserver.com (2026-10-30), pinned through the REAL routers.

Each test drives the package's own router factories — the SAME ones the standalone service and
the aidream host mount — with a stand-in ``FileService`` that records what it was asked:

1. active types (html/svg/xml/js) are never inline, never their real Content-Type, always
   nosniff — even with ``?inline=1``; image/PDF still render inline;
4. every failure is the ApiError envelope ``{error, message, user_message, details,
   request_id}`` — never ``{"detail": ...}`` or a raw 422 list;
5. a malformed id is a 404 ApiError before any handler runs — the service is never asked
   (the ORM's ParameterError, with SQL + args, used to leak verbatim);
2. ``POST /files/bulk`` answers with COUNTS (``BulkOperationResponse``);
14. a quote in a filename is encoded in Content-Disposition (RFC 6266/5987).
"""

from __future__ import annotations

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from matrx_files.api import build_file_router
from matrx_files.api.errors import install_error_handlers

FILE = "7a2b3c4d-0000-4000-8000-00000000f001"


class _Router:
    def is_configured(self, name: str) -> bool:
        return False

    async def read_async(self, uri: str) -> bytes:
        return b"<script>alert(1)</script>"


class _Service:
    def __init__(self, record: dict):
        self.record = record
        self.router = _Router()
        self.calls: list[str] = []

    async def read_record(self, file_id: str, *, user_id: str) -> dict:
        self.calls.append(f"read:{file_id}")
        return self.record

    async def soft_delete(self, file_id: str, *, user_id: str) -> bool:
        self.calls.append(f"delete:{file_id}")
        return True

    _fm = None

    async def bulk_op(self, **kw) -> dict:
        from matrx_files.service import FileService

        # The REAL envelope builder (ids validated first), no database.
        return await FileService.bulk_op(self, **kw)  # type: ignore[arg-type]


def _client(record: dict) -> tuple[TestClient, _Service]:
    service = _Service(record)
    app = FastAPI()
    install_error_handlers(app)
    app.include_router(build_file_router(service))  # type: ignore[arg-type]
    return TestClient(app, raise_server_exceptions=False), service


def _record(name: str, mime: str) -> dict:
    return {
        "id": FILE,
        "file_name": name,
        "file_path": f"docs/{name}",
        "mime_type": mime,
        "size_bytes": 0,
        "checksum": "abc",
        "storage_uri": f"s3://bucket/{FILE}",
    }


@pytest.mark.parametrize(
    ("name", "mime"),
    [
        ("evil.html", "text/html"),
        ("evil.svg", "image/svg+xml"),
        ("evil.xml", "application/xml"),
        ("evil.js", "application/javascript"),
    ],
)
@pytest.mark.parametrize("flag", ["true", "1"])
def test_active_types_are_never_inline(name: str, mime: str, flag: str) -> None:
    client, _ = _client(_record(name, mime))
    resp = client.get(f"/files/{FILE}/download?inline={flag}")
    assert resp.status_code == 200
    assert resp.headers["content-disposition"].startswith("attachment;")
    assert resp.headers["content-type"].startswith("application/octet-stream")
    assert resp.headers["x-content-type-options"] == "nosniff"


@pytest.mark.parametrize(
    ("name", "mime"), [("a.png", "image/png"), ("a.pdf", "application/pdf")]
)
def test_media_still_renders_inline(name: str, mime: str) -> None:
    client, _ = _client(_record(name, mime))
    resp = client.get(f"/files/{FILE}/download?inline=1")
    assert resp.headers["content-disposition"].startswith("inline;")
    assert resp.headers["content-type"].startswith(mime)


def test_text_is_attachment_even_when_inline_asked() -> None:
    client, _ = _client(_record("notes.txt", "text/plain"))
    resp = client.get(f"/files/{FILE}/download?inline=1")
    assert resp.headers["content-disposition"].startswith("attachment;")


def test_quote_in_filename_is_encoded() -> None:
    client, _ = _client(_record('say "hi".png', "image/png"))
    cd = client.get(f"/files/{FILE}/download").headers["content-disposition"]
    assert 'filename="say _hi_.png"' in cd
    assert "filename*=UTF-8''say%20%22hi%22.png" in cd


def _is_api_error(body: dict) -> None:
    assert set(body) == {"error", "message", "user_message", "details", "request_id"}, body
    assert "detail" not in body
    assert "\x1b[" not in body["message"]  # never ANSI-coloured ORM text


@pytest.mark.parametrize(
    ("method", "path"),
    [
        ("GET", "/files/zzz/download"),
        ("DELETE", "/files/zzz"),
        ("PATCH", "/files/zzz"),
        ("GET", "/files/not-a-uuid"),
    ],
)
def test_malformed_id_is_a_404_api_error_and_never_reaches_the_service(method, path) -> None:
    client, service = _client(_record("a.png", "image/png"))
    resp = client.request(method, path, json={})
    assert resp.status_code == 404, resp.text
    _is_api_error(resp.json())
    assert resp.json()["error"] == "not_found"
    assert service.calls == []


def test_validation_failure_is_a_400_api_error_not_a_422_list() -> None:
    client, _ = _client(_record("a.png", "image/png"))
    resp = client.post("/files/bulk", json={"ids": [], "op": "delete"})
    assert resp.status_code == 400
    body = resp.json()
    _is_api_error(body)
    assert body["error"] == "invalid_request"
    assert isinstance(body["details"]["errors"], list)


def test_bulk_with_a_non_uuid_id_is_400_never_orm_text() -> None:
    client, _ = _client(_record("a.png", "image/png"))
    resp = client.post("/files/bulk", json={"ids": ["zzz"], "op": "delete"})
    assert resp.status_code == 400, resp.text
    _is_api_error(resp.json())
    assert "UUID" in resp.json()["message"]


def test_bulk_route_answers_with_counts() -> None:
    client, _ = _client(_record("a.png", "image/png"))
    resp = client.post("/files/bulk", json={"ids": [FILE], "op": "delete"})
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert (body["total"], body["succeeded"], body["failed"]) == (1, 1, 0)
    assert body["results"] == [{"file_id": FILE, "ok": True, "error": None, "old_path": None, "new_path": None}]


@pytest.mark.asyncio
async def test_bulk_envelope_is_the_published_model() -> None:
    from matrx_files.asset_envelope import BulkOperationResponse
    from matrx_files.service import FileService

    class _Fake:
        _fm = None

        async def soft_delete(self, fid, *, user_id):
            if fid.endswith("2"):
                raise PermissionError("no")
            return True

    ids = [FILE, FILE[:-1] + "2"]
    env = await FileService.bulk_op(_Fake(), user_id="u", ids=ids, op="delete")  # type: ignore[arg-type]
    model = BulkOperationResponse.model_validate(env)
    assert (model.total, model.succeeded, model.failed) == (2, 1, 1)


@pytest.mark.asyncio
async def test_copy_always_creates_a_new_row_never_the_dedup_alias() -> None:
    """Law 9: dedup is root UPLOADS only — a copy rides force_new_copy, never implicit alias."""
    from types import SimpleNamespace

    from matrx_files.service import FileService

    asked: dict = {}

    class _Fake:
        db = SimpleNamespace(get_file_async=None)
        router = SimpleNamespace()
        sync_engine = SimpleNamespace()

    fake = _Fake()

    async def get_file_async(fid):
        return {"id": FILE, "file_path": "docs/a.png", "mime_type": "image/png", "storage_uri": "s3://b/k"}

    async def read_async(uri):
        return b"same-bytes"

    async def get_file_info_async(path):
        return None

    async def upload_with_intent(content, **kw):
        asked.update(kw)
        return {"result": SimpleNamespace(file_id="new-row-id", is_new=True)}

    fake.db.get_file_async = get_file_async
    fake.router.read_async = read_async
    fake.sync_engine.get_file_info_async = get_file_info_async
    fake.upload_with_intent = upload_with_intent

    result = await FileService.copy_file(fake, FILE, target_path="docs/b.png", user_id="u")  # type: ignore[arg-type]
    assert result.file_id == "new-row-id"
    assert asked["intent"] == "force_new_copy"
    assert asked["reason"]

    async def aliased(content, **kw):  # the inner write handed back the source
        return {"result": SimpleNamespace(file_id=FILE, is_new=False)}

    fake.upload_with_intent = aliased
    with pytest.raises(RuntimeError, match="did not create a new file row"):
        await FileService.copy_file(fake, FILE, target_path="docs/b.png", user_id="u")  # type: ignore[arg-type]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "published,shown,expect_pub,expect_shown",
    [(True, None, True, "type_default"), (False, "only_me", False, "only_me"), (False, None, False, "type_default"), (False, "org", False, "org")],
)
async def test_a_copy_keeps_the_originals_visibility_and_no_grants(published, shown, expect_pub, expect_shown) -> None:
    """A copy of a link/public/shared file used to come back personal; it keeps the source's access, never its grants."""
    from types import SimpleNamespace

    from matrx_files.service import FileService

    asked: dict = {}

    class _Fake:
        db = SimpleNamespace()
        router = SimpleNamespace()
        sync_engine = SimpleNamespace()

    fake = _Fake()

    async def get_file_async(fid):
        return {"id": FILE, "file_path": "a.png", "mime_type": "image/png", "storage_uri": "s3://b/k",
                "published_to_web": published, "shown_to": shown}

    async def read_async(uri):
        return b"x"

    async def upload_with_intent(content, **kw):
        asked.update(kw)
        return {"result": SimpleNamespace(file_id="new-row-id", is_new=True)}

    fake.db.get_file_async = get_file_async
    fake.router.read_async = read_async
    fake.upload_with_intent = upload_with_intent

    await FileService.copy_file(fake, FILE, target_path="b.png", user_id="u")  # type: ignore[arg-type]
    assert asked["published_to_web"] is expect_pub
    assert asked["shown_to"] == expect_shown
    assert not asked.get("share_with")


def test_a_unique_violation_names_the_real_path_never_postgres_text() -> None:
    """Finding 9: the 409 said "already exists at path '<duplicate key value violates…>'"."""
    from matrx_files.cloud_sync.db import conflicting_path
    from matrx_files.dedup import FilePathConflictError

    class _UniqueViolation(Exception):
        sqlstate = "23505"
        detail = "Key (owner_id, file_path)=(11111111-1111-4111-8111-111111111111, docs/a, b.txt) already exists."

    exc = _UniqueViolation('duplicate key value violates unique constraint "cld_files_owner_path_key"')
    assert conflicting_path(exc) == "docs/a, b.txt"
    err = FilePathConflictError(file_path=conflicting_path(exc))
    assert "duplicate key" not in str(err) and "docs/a, b.txt" in str(err)
    assert conflicting_path(Exception("duplicate key value")) == "the destination"


# --- findings 11 / 13: grants and share links ------------------------------------------


@pytest.mark.parametrize(
    ("expires_at", "max_uses"),
    [("2001-01-01T00:00:00Z", None), (None, 0), (None, -3)],
)
def test_a_dead_on_arrival_share_link_is_refused(expires_at, max_uses) -> None:
    from matrx_files.cloud_sync.permissions import validate_share_link_terms

    with pytest.raises(ValueError):
        validate_share_link_terms(expires_at=expires_at, max_uses=max_uses)


def test_a_live_share_link_is_accepted() -> None:
    from matrx_files.cloud_sync.permissions import validate_share_link_terms

    validate_share_link_terms(expires_at="2999-01-01T00:00:00Z", max_uses=1)
    validate_share_link_terms()


@pytest.mark.asyncio
async def test_a_link_or_grant_on_a_missing_file_is_404_not_403() -> None:
    from matrx_files.cloud_sync.permissions import PermissionsManager

    class _Db:
        async def get_file_async(self, fid):
            return None

    pm = PermissionsManager.__new__(PermissionsManager)
    pm._db = _Db()  # type: ignore[attr-defined]
    with pytest.raises(FileNotFoundError):
        await pm.create_share_link_async("file", FILE, expires_at=None, max_uses=None)
    with pytest.raises(FileNotFoundError):
        await pm.grant_async("file", FILE, "11111111-1111-4111-8111-111111111111")


def test_the_standalone_router_can_revoke_a_share_link() -> None:
    router = build_file_router(_Service(_record("a.png", "image/png")))  # type: ignore[arg-type]
    paths = {(r.path, tuple(sorted(r.methods))) for r in router.routes if hasattr(r, "methods")}
    assert ("/files/share-links/{token}", ("DELETE",)) in paths


# --- finding 12: an archived organization is ONE answer on both hosts -------------------


@pytest.mark.asyncio
async def test_the_standalone_resolver_names_an_archived_organization(monkeypatch) -> None:
    import matrx_orm
    from matrx_connect.middleware.auth import OrganizationArchived

    from matrx_files.standalone import app as standalone

    ORG = "884d1ce8-0000-4000-8000-000000000001"

    async def fake_call(db, schema, fn, *args, mode="scalar", **kw):
        if fn == "has_org_access_for":
            return False
        if fn == "archived_org_ids":
            return [{"archived_org_ids": ORG}]
        raise AssertionError(fn)

    monkeypatch.setattr(matrx_orm, "call_function", fake_call)
    with pytest.raises(OrganizationArchived):
        await standalone._standalone_resolve_active_organization("u", ORG)

    async def not_archived(db, schema, fn, *args, mode="scalar", **kw):
        return False if fn == "has_org_access_for" else []

    monkeypatch.setattr(matrx_orm, "call_function", not_archived)
    assert await standalone._standalone_resolve_active_organization("u", ORG) is None
