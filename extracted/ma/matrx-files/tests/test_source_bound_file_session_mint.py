"""Actual mint route and middleware, with explicit source policy and no host imports."""

import asyncio
import re
import time
from types import SimpleNamespace

import httpx
import pytest
from fastapi import FastAPI, Request

from matrx_connect.context.app_context import AppContext
from matrx_connect.emitters.console_emitter import ConsoleEmitter
from matrx_connect.middleware.file_session import (
    FileSessionCredential,
    classify_bound_file_session_value,
)
from matrx_connect.middleware import session_cookie as sc
from matrx_connect.middleware.session_cookie import (
    SESSION_COOKIE_NAME,
    register_session_cookie_secret,
)
from matrx_files.api.router_files import build_file_router
from matrx_files.file_session_mint import mint_file_session_response

USER = "00000000-0000-4000-8000-000000000001"
SOURCE = "00000000-0000-4000-8000-000000000002"
OTHER = "00000000-0000-4000-8000-000000000003"
SECRET = b"synthetic-shared-mint-secret-not-deployment-secret"


@pytest.fixture(autouse=True)
def signing_secret():
    saved = sc._registered_secret, sc._registered_secret_is_ephemeral
    register_session_cookie_secret(SECRET)
    yield
    sc._registered_secret, sc._registered_secret_is_ephemeral = saved


def context(kind="login", expiry=None):
    expiry = expiry or int(time.time()) + 300
    kwargs = {"user_id": USER, "emitter": ConsoleEmitter()}
    if kind == "login":
        kwargs.update(
            auth_type="token",
            is_authenticated=True,
            metadata={"jwt_claims": {"session_id": SOURCE}, "jwt_expires_at": expiry},
        )
    elif kind == "api_key":
        kwargs.update(
            auth_type="api_key",
            is_authenticated=True,
            metadata={"api_key_id": "publicKey", "api_key_expires_at": expiry},
        )
    else:
        kwargs.update(auth_type="fingerprint", fingerprint_id="synthetic-private-fingerprint")
    return AppContext(**kwargs)


def binding(kind="login", user=USER, source=None, expiry=None):
    return FileSessionCredential(
        user,
        kind,
        source or ("publicKey" if kind == "api_key" else SOURCE),
        expiry or int(time.time()) + 120,
    )


def application(ctx, resolver=None, required=False):
    app = FastAPI()

    @app.middleware("http")
    async def admission(request, call_next):
        request.state.context = ctx
        return await call_next(request)

    def user_id_dep(request: Request):
        return request.state.context.user_id

    app.include_router(
        build_file_router(
            None,
            user_id_dep=user_id_dep,
            file_session_source_resolver=resolver,
            require_file_session_source=required,
        )
    )
    return app


@pytest.mark.asyncio
@pytest.mark.parametrize("kind", ["login", "api_key", "guest"])
async def test_each_source_mints_matching_classic_and_partitioned_cookie_with_real_expiry(kind):
    ctx = context(kind)
    credential = binding(kind)
    calls = []

    async def resolver(admitted):
        calls.append(admitted)
        return credential

    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=application(ctx, resolver)), base_url="https://test"
    ) as client:
        response = await client.post("/files/session")
    assert response.status_code == 200
    headers = response.headers.get_list("set-cookie")
    assert len(headers) == 2
    values = [h.split(";", 1)[0].split("=", 1)[1] for h in headers]
    assert values[0] == values[1]
    assert classify_bound_file_session_value(values[0], SECRET)[0] == credential
    ttl = response.json()["expires_in"]
    assert 117 <= ttl <= 120
    assert all(f"Max-Age={ttl};" in h and "HttpOnly" in h and "Secure" in h for h in headers)
    assert "Partitioned" not in headers[0] and "Partitioned" in headers[1]
    assert response.json()["secret_source"] == "stable"
    assert response.headers["cache-control"] == "no-store"
    assert calls == [ctx]
    assert "guest_execution_id" not in ctx.metadata
    assert values[0] not in response.text
    assert "fingerprint" not in values[0]


@pytest.mark.asyncio
async def test_required_missing_resolver_is503_without_cookie_or_legacy_fallback():
    response = await mint_file_session_response(USER, context=context(), require_source=True)
    assert response.status_code == 503
    assert response.headers["retry-after"] == "1"
    assert "set-cookie" not in response.headers


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "ctx", [None, context().with_overrides(user_id=OTHER), SimpleNamespace(user_id=USER)]
)
async def test_missing_or_disagreeing_admission_refuses_before_source_callback(ctx):
    async def resolver(admitted):
        pytest.fail("wrong admission reached authority")

    from fastapi import HTTPException

    with pytest.raises(HTTPException) as error:
        await mint_file_session_response(USER, context=ctx, source_resolver=resolver)
    assert error.value.status_code == 401


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "credential",
    [
        binding(user=OTHER),
        binding(source=OTHER),
        binding("guest"),
        binding(expiry=int(time.time()) + 600),
        None,
    ],
)
async def test_wrong_subject_source_kind_expiry_or_result_never_mints(credential):
    async def resolver(ctx):
        return credential

    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=application(context(), resolver)), base_url="https://test"
    ) as client:
        response = await client.post("/files/session")
    assert response.status_code == 401
    assert "set-cookie" not in response.headers
    assert response.json() == {"detail": {"code": "file_session_source_refused"}}


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "ctx",
    [
        context().with_overrides(is_authenticated=False),
        context().with_overrides(auth_type="cookie"),
        context("guest").with_overrides(fingerprint_id=None),
    ],
)
async def test_unadmitted_or_cookie_derived_identity_cannot_remint(ctx):
    async def resolver(admitted):
        return binding("guest" if admitted.auth_type == "fingerprint" else "login")

    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=application(ctx, resolver)), base_url="https://test"
    ) as client:
        response = await client.post("/files/session")
    assert response.status_code == 401
    assert "set-cookie" not in response.headers


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "failure", ["refused", "unavailable", "timeout", "missing-secret", "provider-value-error"]
)
async def test_refused_or_unavailable_authority_produces_no_cookie(failure):
    async def resolver(ctx):
        if failure == "refused":
            raise PermissionError("synthetic-private-fingerprint-detail")
        if failure == "provider-value-error":
            raise ValueError("synthetic-private-provider-error")
        if failure == "timeout":
            await asyncio.sleep(1)
        if failure == "missing-secret":
            sc._registered_secret = None
            return binding()
        raise RuntimeError("synthetic-private-authority-detail")

    if failure == "timeout":
        response = await mint_file_session_response(
            USER, context=context(), source_resolver=resolver, timeout_seconds=0.01
        )
    else:
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=application(context(), resolver)),
            base_url="https://test",
        ) as client:
            response = await client.post("/files/session")
    assert response.status_code == (401 if failure == "refused" else 503)
    assert "set-cookie" not in response.headers
    content = response.text if hasattr(response, "text") else response.body.decode()
    assert "private" not in content


@pytest.mark.asyncio
async def test_cancellation_propagates_before_cookie_creation():
    async def resolver(ctx):
        raise asyncio.CancelledError

    with pytest.raises(asyncio.CancelledError):
        await mint_file_session_response(USER, context=context(), source_resolver=resolver)


@pytest.mark.asyncio
async def test_source_expiring_during_callback_cannot_mint():
    async def resolver(ctx):
        return FileSessionCredential(USER, "login", SOURCE, int(time.time()))

    from fastapi import HTTPException

    with pytest.raises(HTTPException) as error:
        await mint_file_session_response(USER, context=context(), source_resolver=resolver)
    assert error.value.status_code == 401


@pytest.mark.asyncio
async def test_legacy_standalone_and_main_response_shapes_are_retained():
    for include_source in (True, False):
        response = await mint_file_session_response(USER, include_secret_source=include_source)
        body = __import__("json").loads(response.body)
        assert body["expires_in"] == sc.SESSION_COOKIE_TTL_SECONDS
        assert ("secret_source" in body) == include_source
        assert all(
            re.match(f"{SESSION_COOKIE_NAME}=v1\\.", h)
            for h in response.headers.getlist("set-cookie")
        )


@pytest.mark.asyncio
async def test_each_remint_rechecks_current_source_after_previous_success():
    active = True
    calls = []

    async def resolver(ctx):
        calls.append(ctx.user_id)
        if not active:
            raise PermissionError("Source ended")
        return binding()

    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=application(context(), resolver)), base_url="https://test"
    ) as client:
        assert (await client.post("/files/session")).status_code == 200
        active = False
        response = await client.post("/files/session")
    assert response.status_code == 401
    assert "set-cookie" not in response.headers
    assert calls == [USER, USER]
