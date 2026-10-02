"""
Per-request Supabase client builder tests.

Validate: (1) injected user_supabase_factory takes precedence; (2)
env-based fallback runs when no factory is injected; (3) bearer-token
extraction logic.
"""

from __future__ import annotations

import os

import pytest


def test_make_user_client_uses_injected_factory(monkeypatch):
    """If the host injects user_supabase_factory, the package uses it."""
    import matrx_scheduler
    from matrx_scheduler.api.per_request import make_user_client

    received: dict[str, str] = {}

    def factory(jwt: str):
        received["jwt"] = jwt
        return ("fake-client", jwt)

    matrx_scheduler.configure(
        supabase_client="<scanner-client>",
        surface="test",
        user_supabase_factory=factory,
    )

    out = make_user_client("user-jwt-here")
    assert received["jwt"] == "user-jwt-here"
    assert out == ("fake-client", "user-jwt-here")


def test_make_user_client_falls_back_to_env(monkeypatch):
    """No injected factory + env vars set → default factory builds the client."""
    import matrx_scheduler
    from matrx_scheduler.api import per_request

    # Wipe any previously injected factory.
    matrx_scheduler.configure(
        supabase_client="<scanner-client>",
        surface="test",
        user_supabase_factory=None,
    )
    # Reset the lru_cache so the next call picks up our env.
    per_request._env_project_config.cache_clear()

    monkeypatch.setenv("SUPABASE_MATRIX_URL", "https://example.supabase.co")
    monkeypatch.setenv(
        "SUPABASE_MATRIX_PUBLISHABLE_KEY", "sb_publishable_test_key_value"
    )

    # We can't construct a real AsyncClient without the supabase library
    # being able to bind to httpx; if supabase is missing this test
    # short-circuits via importorskip in the inner import.
    pytest.importorskip("supabase")
    pytest.importorskip("httpx")

    client = per_request.make_user_client("user-jwt")
    # The class name should be AsyncClient
    assert client.__class__.__name__ == "AsyncClient"


def test_env_factory_rejects_missing_url(monkeypatch):
    import matrx_scheduler
    from matrx_scheduler.api import per_request

    matrx_scheduler.configure(
        supabase_client="<scanner-client>",
        surface="test",
        user_supabase_factory=None,
    )
    per_request._env_project_config.cache_clear()
    monkeypatch.delenv("SUPABASE_MATRIX_URL", raising=False)
    monkeypatch.delenv("SUPABASE_URL", raising=False)
    monkeypatch.setenv("SUPABASE_MATRIX_PUBLISHABLE_KEY", "sb_publishable_x")

    with pytest.raises(RuntimeError, match="SUPABASE_MATRIX_URL"):
        per_request.make_user_client("user-jwt")


def test_env_factory_rejects_legacy_anon_key(monkeypatch):
    """Legacy JWT-format anon keys must be rejected so RLS isn't weakened."""
    import matrx_scheduler
    from matrx_scheduler.api import per_request

    matrx_scheduler.configure(
        supabase_client="<scanner-client>",
        surface="test",
        user_supabase_factory=None,
    )
    per_request._env_project_config.cache_clear()
    monkeypatch.setenv("SUPABASE_MATRIX_URL", "https://example.supabase.co")
    monkeypatch.setenv(
        "SUPABASE_MATRIX_PUBLISHABLE_KEY",
        "eyJhbGc.fake-anon-jwt-style",  # legacy format
    )

    with pytest.raises(RuntimeError, match="sb_publishable_"):
        per_request.make_user_client("user-jwt")


def test_extract_jwt_ok():
    pytest.importorskip("fastapi")
    from starlette.datastructures import Headers
    from matrx_scheduler.api.per_request import extract_jwt

    class FakeReq:
        headers = Headers({"authorization": "Bearer abc.def.ghi"})

    assert extract_jwt(FakeReq()) == "abc.def.ghi"


def test_extract_jwt_missing_raises_401():
    pytest.importorskip("fastapi")
    from fastapi import HTTPException
    from starlette.datastructures import Headers
    from matrx_scheduler.api.per_request import extract_jwt

    class FakeReq:
        headers = Headers({})

    with pytest.raises(HTTPException) as exc_info:
        extract_jwt(FakeReq())
    assert exc_info.value.status_code == 401


def test_extract_jwt_wrong_scheme_raises_401():
    pytest.importorskip("fastapi")
    from fastapi import HTTPException
    from starlette.datastructures import Headers
    from matrx_scheduler.api.per_request import extract_jwt

    class FakeReq:
        headers = Headers({"authorization": "Basic abc"})

    with pytest.raises(HTTPException) as exc_info:
        extract_jwt(FakeReq())
    assert exc_info.value.status_code == 401
