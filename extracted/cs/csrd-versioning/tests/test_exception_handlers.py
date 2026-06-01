"""Tests for exception handlers."""

import pytest
from fastapi import FastAPI, HTTPException
from httpx import ASGITransport, AsyncClient

from csrd.versioning.exception_handlers import EXCEPTION_HANDLERS


def _build_app() -> FastAPI:
    app = FastAPI(exception_handlers=EXCEPTION_HANDLERS)

    @app.get("/ok")
    async def ok():
        return {"status": "ok"}

    @app.get("/not-found")
    async def not_found():
        raise HTTPException(status_code=404, detail="Resource not found")

    @app.get("/server-error")
    async def server_error():
        raise HTTPException(status_code=500, detail="Something broke")

    @app.get("/unauthorized")
    async def unauthorized():
        raise HTTPException(status_code=401, detail="Unauthorized")

    @app.get("/items/{item_id}")
    async def get_item(item_id: int):
        return {"item_id": item_id}

    return app


@pytest.fixture
def app():
    return _build_app()


class TestExceptionHandlers:
    @pytest.mark.asyncio
    async def test_404_returns_structured_json(self, app):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            resp = await client.get("/not-found")
            assert resp.status_code == 404
            body = resp.json()
            assert "meta" in body
            assert body["meta"]["status"] == 404
            assert body["meta"]["error"] == "Resource not found"
            assert body["meta"]["path"] == "/not-found"
            assert "errors" in body

    @pytest.mark.asyncio
    async def test_500_returns_structured_json(self, app):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            resp = await client.get("/server-error")
            assert resp.status_code == 500
            body = resp.json()
            assert body["meta"]["status"] == 500

    @pytest.mark.asyncio
    async def test_401_returns_structured_json(self, app):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            resp = await client.get("/unauthorized")
            assert resp.status_code == 401
            body = resp.json()
            assert body["meta"]["status"] == 401

    @pytest.mark.asyncio
    async def test_validation_error_returns_400(self, app):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            resp = await client.get("/items/not-a-number")
            assert resp.status_code in (400, 422)
            body = resp.json()
            assert "meta" in body

    @pytest.mark.asyncio
    async def test_meta_contains_method(self, app):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            resp = await client.get("/not-found")
            body = resp.json()
            assert body["meta"]["method"] == "GET"

    @pytest.mark.asyncio
    async def test_meta_contains_timestamp(self, app):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            resp = await client.get("/not-found")
            body = resp.json()
            assert "timestamp" in body["meta"]

    @pytest.mark.asyncio
    async def test_meta_contains_api_version(self, app):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            resp = await client.get("/not-found")
            body = resp.json()
            assert "apiVersion" in body["meta"]

    @pytest.mark.asyncio
    async def test_nonexistent_route_returns_404(self, app):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            resp = await client.get("/does-not-exist")
            assert resp.status_code == 404
            body = resp.json()
            assert body["meta"]["status"] == 404
