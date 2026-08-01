import json
from typing import Any
from unittest.mock import AsyncMock, patch

from connector.http_server import build_observations, create_asgi_app
from connector.oai.integration import DescriptionData, Integration
from pydantic import BaseModel, Field

FLOWS_V2_HEADER = "x-lumos-observability-flows_v2_execution_id"
DAGSTER_HEADER = "x-lumos-observability-dagster.run_id"


def make_integration() -> Integration:
    class MockSettings(BaseModel):
        normal_field: str = Field(default="", json_schema_extra={})

    return Integration(
        settings_model=MockSettings,
        app_id="test-app",
        version="1.0.0",
        exception_handlers=[],
        description_data=DescriptionData(
            user_friendly_name="Test Integration",
            description="Test integration for unit tests",
            categories=[],
        ),
    )


async def call_app(
    app: Any,
    method: str,
    path: str,
    body: bytes = b"",
    headers: dict[str, str] | None = None,
    parse_json: bool = True,
) -> tuple[int, Any]:
    scope = {
        "type": "http",
        "method": method,
        "path": path,
        "headers": [
            (key.lower().encode("latin-1"), value.encode("latin-1"))
            for key, value in (headers or {}).items()
        ],
    }
    incoming = [{"type": "http.request", "body": body, "more_body": False}]
    sent: list[dict[str, Any]] = []

    async def receive() -> dict[str, Any]:
        return incoming.pop(0)

    async def send(message: dict[str, Any]) -> None:
        sent.append(message)

    await app(scope, receive, send)

    status = sent[0]["status"]
    response_body = b"".join(
        message.get("body", b"") for message in sent if message["type"] == "http.response.body"
    )
    if not parse_json:
        return status, response_body.decode()
    return status, json.loads(response_body) if response_body else None


async def test_post_capability_dispatches() -> None:
    integration = make_integration()
    integration.capabilities["list_accounts"] = AsyncMock()
    app = create_asgi_app(integration)

    with patch.object(integration, "dispatch", AsyncMock(return_value='{"response": []}')) as mock:
        status, body = await call_app(app, "POST", "/list_accounts", body=b'{"request": {}}')

    assert status == 200
    assert body == {"response": []}
    mock.assert_awaited_once_with("list_accounts", '{"request": {}}')


async def test_hyphenated_capability_route_uses_underscores() -> None:
    integration = make_integration()
    integration.capabilities["some-capability"] = AsyncMock()
    app = create_asgi_app(integration)

    with patch.object(integration, "dispatch", AsyncMock(return_value='{"ok": true}')) as mock:
        status, body = await call_app(app, "POST", "/some_capability", body=b"{}")

    assert status == 200
    assert body == {"ok": True}
    mock.assert_awaited_once_with("some-capability", "{}")


async def test_unknown_path_returns_404() -> None:
    app = create_asgi_app(make_integration())
    status, body = await call_app(app, "POST", "/nonexistent")
    assert status == 404
    assert body == {"detail": "Not Found"}


async def test_wrong_method_returns_405() -> None:
    integration = make_integration()
    integration.capabilities["list_accounts"] = AsyncMock()
    app = create_asgi_app(integration)

    status, body = await call_app(app, "GET", "/list_accounts")
    assert status == 405
    assert body == {"detail": "Method Not Allowed"}


async def test_openapi_json_serves_schema() -> None:
    schema = {"openapi": "3.0.0", "info": {"title": "Test"}}
    app = create_asgi_app(make_integration(), schema=schema)

    status, body = await call_app(app, "GET", "/openapi.json")
    assert status == 200
    assert body == schema


async def test_docs_serves_swagger_ui() -> None:
    app = create_asgi_app(make_integration())

    status, body = await call_app(app, "GET", "/docs", parse_json=False)
    assert status == 200
    assert "test-app - Swagger UI" in body
    assert 'url: "/openapi.json"' in body
    assert "SwaggerUIBundle" in body


async def test_dispatch_error_returns_500() -> None:
    integration = make_integration()
    integration.capabilities["list_accounts"] = AsyncMock()
    app = create_asgi_app(integration)

    with patch.object(integration, "dispatch", AsyncMock(side_effect=RuntimeError("boom"))):
        status, body = await call_app(app, "POST", "/list_accounts", body=b"{}")

    assert status == 500
    assert body == {"detail": "boom"}


async def test_lifespan_protocol() -> None:
    app = create_asgi_app(make_integration())
    incoming = [{"type": "lifespan.startup"}, {"type": "lifespan.shutdown"}]
    sent: list[dict[str, Any]] = []

    async def receive() -> dict[str, Any]:
        return incoming.pop(0)

    async def send(message: dict[str, Any]) -> None:
        sent.append(message)

    await app({"type": "lifespan"}, receive, send)
    assert sent == [
        {"type": "lifespan.startup.complete"},
        {"type": "lifespan.shutdown.complete"},
    ]


def test_build_observations_with_headers() -> None:
    observations = build_observations(
        {
            FLOWS_V2_HEADER: "flow-123",
            DAGSTER_HEADER: "run-456",
        }
    )
    assert observations == {
        "flows_v2_execution_id": "flow-123",
        "dagster": {"run_id": "run-456"},
    }


def test_build_observations_without_headers() -> None:
    observations = build_observations({})
    assert observations == {"flows_v2_execution_id": ""}
