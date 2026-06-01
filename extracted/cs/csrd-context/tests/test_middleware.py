"""Tests for RequestContextMiddleware and HTTPLoggingMiddleware."""

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from csrd.context import RequestContextMiddleware, get_headers
from csrd.context._contextvars import reset_global_configuration


@pytest.fixture
def app():
    app = FastAPI()

    @app.get("/test")
    async def test_endpoint():
        headers = get_headers()
        return {
            "x-custom": headers.get("x-custom", "missing"),
            "has_headers": len(dict(headers)) > 0,
        }

    app.add_middleware(RequestContextMiddleware)
    return app


@pytest.fixture
def anyio_backend():
    return "asyncio"


class TestRequestContextMiddleware:
    @pytest.mark.asyncio
    async def test_headers_captured(self, app):
        reset_global_configuration()
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            resp = await client.get("/test", headers={"x-custom": "hello"})
            assert resp.status_code == 200
            data = resp.json()
            assert data["x-custom"] == "hello"
            assert data["has_headers"] is True
        reset_global_configuration()

    @pytest.mark.asyncio
    async def test_headers_isolated_between_requests(self, app):
        reset_global_configuration()
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            resp1 = await client.get("/test", headers={"x-custom": "first"})
            resp2 = await client.get("/test", headers={"x-custom": "second"})
            assert resp1.json()["x-custom"] == "first"
            assert resp2.json()["x-custom"] == "second"
        reset_global_configuration()
