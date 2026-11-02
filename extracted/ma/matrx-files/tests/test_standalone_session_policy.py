"""Actual standalone app composition; only DB/storage and remote authority are synthetic."""
from __future__ import annotations

import time
import json
from dataclasses import asdict
from types import SimpleNamespace

import httpx
import jwt
import pytest
from fastapi.middleware.cors import CORSMiddleware
from matrx_connect.middleware.auth import AuthMiddleware
from matrx_connect.middleware.file_session import FileSessionCredential, mint_bound_file_session_value
from matrx_connect.middleware.session_cookie import SESSION_COOKIE_NAME, mint_session_cookie_value, session_cookie_headers
from matrx_files._config import IndependenceConfigError
from matrx_files.standalone import app as module
from matrx_files.standalone.remote_mint import RemoteFileSessionMintMiddleware
from matrx_files.standalone.session_policy import session_policy_armed

ORIGINAL_CLIENT = httpx.AsyncClient
USER = "00000000-0000-4000-8000-000000000001"
SOURCE = "00000000-0000-4000-8000-000000000002"
SECRET = "synthetic-standalone-source-policy-signing-key"
CFG = {"db_host": "unreachable.invalid", "s3_bucket": "synthetic", "supabase_url": "https://identity.example",
       "jwt_secret": SECRET, "guest_fingerprint_secret": SECRET, "session_authority_url": "https://authority.example/auth/session/status",
       "file_session_authority_url": "https://authority.example/auth/file-session/status", "file_session_mint_url": "https://authority.example/files/session",
       "cors_allowed_origins": "https://browser.example", "cors_allowed_origin_regex": ""}


@pytest.fixture
def full_app(monkeypatch):
    state = {"kind": "login", "source": SOURCE, "active": True, "outage": False, "reads": [], "calls": []}
    now = int(time.time())
    def credential():
        return FileSessionCredential(USER, state["kind"], state["source"], now + 120)
    async def read_record(file_id, *, user_id):
        assert user_id == USER
        state["reads"].append(file_id)
        return {"file_name": "proof.txt", "mime_type": "text/plain", "storage_uri": "memory://proof", "size_bytes": 23}
    async def read_bytes(uri):
        assert uri == "memory://proof"
        return b"synthetic-private-bytes"
    service = SimpleNamespace(read_record=read_record, router=SimpleNamespace(read_async=read_bytes))
    monkeypatch.setattr(module, "_env_config", lambda: dict(CFG))
    for name in ["_configure_settings_for_standalone", "_configure_context_for_standalone", "_assert_organization_seam", "_assert_block_ledger_seam"]:
        monkeypatch.setattr(module, name, lambda: None)
    import matrx_files.db as db
    import matrx_files.blocks as blocks
    import matrx_files.standalone.access_checker as checker
    import matrx_files.upload_policy as upload
    from matrx_files.service import FileService
    monkeypatch.setattr(db, "bootstrap_db", lambda: None)
    monkeypatch.setattr(blocks, "configure_block_ledger", lambda: None)
    monkeypatch.setattr(checker, "install_standalone_access_checker", lambda: None)
    monkeypatch.setattr(FileService, "from_env", lambda **kwargs: service)
    monkeypatch.setattr(upload, "build_upload_policy", lambda *args, **kwargs: {"quota_checker": None, "finalize": None, "arming": "synthetic storage"})
    async def organization(*args):
        return None
    monkeypatch.setattr(module, "_standalone_resolve_active_organization", organization)
    from matrx_files.api import router as health
    from matrx_files.db.readiness import DatabaseReadiness
    async def ready():
        return DatabaseReadiness(True, time.monotonic())
    monkeypatch.setattr(health, "probe_database_readiness", ready)
    async def authority(request):
        state["calls"].append(request)
        if state["outage"]:
            return httpx.Response(503)
        if not state["active"] or "preflight-invalid" in request.headers.get("authorization", ""):
            return httpx.Response(401, headers={"Cache-Control": "no-store"})
        binding = credential()
        if request.method == "POST":
            value = mint_bound_file_session_value(binding, SECRET.encode())
            return httpx.Response(200, json={"ok": True, "expires_in": 120}, headers=[("Cache-Control", "no-store")]+[("Set-Cookie", c) for c in session_cookie_headers(value, ttl_seconds=120)])
        if request.url.path == "/auth/session/status":
            return httpx.Response(200, json={"user_id": USER, "session_id": SOURCE, "expires_at": now + 120})
        assert request.headers["authorization"] == "FileSession " + mint_bound_file_session_value(binding, SECRET.encode())
        return httpx.Response(200, json=asdict(binding))
    def client(**kwargs):
        return ORIGINAL_CLIENT(transport=httpx.MockTransport(authority), **kwargs)
    monkeypatch.setattr(httpx, "AsyncClient", client)
    app = module.create_app()
    state["app"] = app
    state["binding"] = credential
    from cryptography.hazmat.primitives.asymmetric import ec
    signing_key = ec.generate_private_key(ec.SECP256R1())
    jwk = jwt.PyJWK.from_dict({**json.loads(jwt.algorithms.ECAlgorithm.to_jwk(signing_key.public_key())), "kid": "synthetic-key"})
    monkeypatch.setattr(jwt.PyJWKClient, "get_signing_keys", lambda self, **kwargs: [jwk])
    state["token"] = jwt.encode({"sub": USER, "session_id": SOURCE, "aud": "authenticated", "exp": now + 120}, signing_key, algorithm="ES256", headers={"kid": "synthetic-key"})
    return state


@pytest.mark.asyncio
@pytest.mark.parametrize("kind,source,headers", [("login", SOURCE, {"Authorization": "Bearer one"}),
    ("api_key", "publicKey", {"Authorization": "Bearer mx_live_publicKey_secret"}),
    ("guest", SOURCE, {"X-Fingerprint-ID": "fingerprint"})])
async def test_actual_app_each_mint_to_private_byte_source_revocation(full_app, kind, source, headers):
    state = full_app
    state.update(kind=kind, source=source)
    app = state["app"]
    assert session_policy_armed(app)
    async with ORIGINAL_CLIENT(transport=httpx.ASGITransport(app), base_url="https://files.example") as client:
        minted = await client.post("/files/session", headers={**headers, "Origin": "https://browser.example"})
        assert minted.status_code == 200 and minted.headers["access-control-allow-origin"] == "https://browser.example"
        value = mint_bound_file_session_value(state["binding"](), SECRET.encode())
        response = await client.get("/files/proof/download", headers={"Cookie": f"{SESSION_COOKIE_NAME}={value}"})
        assert response.status_code == 200 and response.content == b"synthetic-private-bytes"
        assert state["reads"] == ["proof"]
        state["active"] = False
        assert (await client.get("/files/proof/download", headers={"Cookie": f"{SESSION_COOKIE_NAME}={value}"})).status_code == 401
        assert (await client.post("/files/session", headers=headers)).status_code == 401
        assert state["reads"] == ["proof"]


@pytest.mark.asyncio
async def test_actual_app_legacy_refusal_outage_jwt_and_readiness(full_app):
    state = full_app
    app = state["app"]
    async with ORIGINAL_CLIENT(transport=httpx.ASGITransport(app), base_url="https://files.example") as client:
        old = mint_session_cookie_value(USER, SECRET.encode())
        assert (await client.get("/files/proof/download", headers={"Cookie": f"{SESSION_COOKIE_NAME}={old}"})).status_code == 401
        response = await client.get("/files/proof/download", headers={"Authorization": "Bearer " + state["token"]})
        assert response.status_code == 200
        state["active"] = False
        assert (await client.get("/files/proof/download", headers={"Authorization": "Bearer " + state["token"]})).status_code == 401
        state["outage"] = True
        response = await client.get("/files/proof/download", headers={"Authorization": "Bearer " + state["token"]})
        assert response.status_code == 503 and response.headers["cache-control"] == "no-store"
        assert (await client.get("/files-service/ready")).status_code == 503
        assert (await client.get("/files-service/health")).status_code == 200
        state["outage"] = False
        ready = await client.get("/files-service/ready")
        assert ready.status_code == 200 and ready.headers["cache-control"] == "no-store"
        app.user_middleware[:] = [m for m in app.user_middleware if m.cls is not RemoteFileSessionMintMiddleware]
        assert (await client.get("/files-service/ready")).status_code == 503
        assert (await client.get("/files-service/health")).status_code == 200


@pytest.mark.parametrize("key", ["session_authority_url", "file_session_authority_url", "file_session_mint_url", "guest_fingerprint_secret"])
@pytest.mark.parametrize("value", [None, "", " "])
def test_missing_policy_refuses_before_bootstrap(monkeypatch, key, value):
    cfg = dict(CFG)
    cfg[key] = value
    monkeypatch.setattr(module, "_env_config", lambda: cfg)
    import matrx_files.db as db
    monkeypatch.setattr(db, "bootstrap_db", lambda: pytest.fail("must refuse before DB bootstrap"))
    with pytest.raises(IndependenceConfigError):
        module.create_app()


@pytest.mark.parametrize("key", ["session_authority_url", "file_session_authority_url", "file_session_mint_url"])
def test_invalid_policy_urls_refuse_without_exposing_values(monkeypatch, key):
    cfg = dict(CFG)
    cfg[key] = "http://private-sensitive-host.invalid/token?secret=value"
    monkeypatch.setattr(module, "_env_config", lambda: cfg)
    with pytest.raises(IndependenceConfigError) as error:
        module.create_app()
    assert "private-sensitive" not in str(error.value)


@pytest.mark.parametrize("removed", [AuthMiddleware, RemoteFileSessionMintMiddleware, CORSMiddleware])
def test_armed_guard_checks_installed_callbacks_and_order(full_app, removed):
    app = full_app["app"]
    assert session_policy_armed(app)
    app.user_middleware[:] = [m for m in app.user_middleware if m.cls is not removed]
    assert not session_policy_armed(app)


@pytest.mark.asyncio
async def test_candidate_preflight_requires_installed_armed_policy_and_real_refusal_contracts(full_app, monkeypatch):
    from matrx_files.standalone.preflight import verify_candidate
    import matrx_files.db.readiness as readiness
    async def database_ready(**kwargs):
        return readiness.DatabaseReadiness(True, time.monotonic())
    monkeypatch.setattr(readiness, "probe_database_readiness", database_ready)
    calls = []
    async def authority(request):
        calls.append(request)
        assert request.headers["authorization"].startswith(("Bearer preflight-invalid", "FileSession preflight-invalid"))
        return httpx.Response(401, headers={"Cache-Control": "no-store"})
    def client(**kwargs):
        return ORIGINAL_CLIENT(transport=httpx.MockTransport(authority), **kwargs)
    monkeypatch.setattr(httpx, "AsyncClient", client)
    await verify_candidate(full_app["app"])
    assert [r.method for r in calls] == ["GET", "GET", "POST"]
    full_app["app"].user_middleware[:] = []
    with pytest.raises(RuntimeError, match="not armed"):
        await verify_candidate(full_app["app"])


@pytest.mark.asyncio
@pytest.mark.parametrize("status,cache", [(200, "no-store"), (404, "no-store"), (503, "no-store"), (401, "public")])
async def test_candidate_preflight_refuses_inexact_central_contract(full_app, monkeypatch, status, cache):
    from matrx_files.standalone.preflight import verify_candidate
    import matrx_files.db.readiness as readiness
    async def database_ready(**kwargs):
        return readiness.DatabaseReadiness(True, time.monotonic())
    monkeypatch.setattr(readiness, "probe_database_readiness", database_ready)
    def client(**kwargs):
        return ORIGINAL_CLIENT(transport=httpx.MockTransport(lambda request: httpx.Response(status, headers={"Cache-Control": cache})), **kwargs)
    monkeypatch.setattr(httpx, "AsyncClient", client)
    with pytest.raises(RuntimeError, match="refusal contract"):
        await verify_candidate(full_app["app"])


@pytest.mark.asyncio
async def test_missing_remote_mint_wrapper_cannot_fall_back_to_legacy_cookie(full_app):
    app = full_app["app"]
    app.user_middleware[:] = [m for m in app.user_middleware if m.cls is not RemoteFileSessionMintMiddleware]
    async with ORIGINAL_CLIENT(transport=httpx.ASGITransport(app), base_url="https://files.example") as client:
        response = await client.post("/files/session", headers={"Authorization": "Bearer " + full_app["token"]})
    assert response.status_code == 503 and not response.headers.get_list("set-cookie")
    assert response.headers["cache-control"] == "no-store"


def test_authority_only_config_is_partial_not_smoke(monkeypatch):
    cfg = dict(CFG)
    for key in ["db_host", "s3_bucket", "supabase_url", "guest_fingerprint_secret"]:
        cfg[key] = None
    monkeypatch.setattr(module, "_env_config", lambda: cfg)
    with pytest.raises(IndependenceConfigError) as error:
        module.create_app()
    for name in ["SUPABASE_MATRIX_HOST", "AWS_S3_DEFAULT_BUCKET", "SUPABASE_URL", "GUEST_FINGERPRINT_SECRET"]:
        assert name in str(error.value)
