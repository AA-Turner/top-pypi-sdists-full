"""Tests for the fastapi compatibility shim in ``connector.http_server``.

fastapi is not a runtime dependency of the SDK — ``collect_integration_routes``
imports it lazily, for host applications that mount connector capabilities into a
FastAPI app they already own. These tests live apart from ``test_http_server.py``,
behind an ``importorskip`` guard, so that the fastapi-free surface of the module
stays collectable in an environment where fastapi is not installed.
"""

from unittest.mock import AsyncMock, patch

import pytest
from connector.http_server import collect_integration_routes

from .test_http_server import make_integration

pytest.importorskip("fastapi")

from fastapi import FastAPI  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402


def test_collect_integration_routes_mounts_into_host_app() -> None:
    """The router returned by collect_integration_routes must work when included
    into a host FastAPI app, with app-id-prefixed routes."""
    integration = make_integration()
    integration.capabilities["list_accounts"] = AsyncMock()

    with patch.object(
        integration,
        "dispatch",
        AsyncMock(return_value='{"response": []}'),
    ) as mock:
        router = collect_integration_routes(integration, prefix_app_id=True, tags=["test-app"])
        host_app = FastAPI()
        host_app.include_router(router)
        client = TestClient(host_app)
        response = client.post("/test_app/list_accounts", content='{"request": {}}')

    assert response.status_code == 200
    assert response.json() == {"response": []}
    mock.assert_awaited_once_with("list_accounts", '{"request": {}}')
    openapi = host_app.openapi()
    assert openapi["paths"]["/test_app/list_accounts"]["post"]["tags"] == ["test-app"]
