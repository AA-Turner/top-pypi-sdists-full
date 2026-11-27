"""Tests for ConnectorClient's gateway clients: identity wiring and lifecycle.

The HTTP and MCP behaviour itself belongs to the mistralai SDK helpers and is tested there.
"""

import base64
import json
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any
from unittest.mock import patch

import httpx
import pytest
from conftest import make_context
from mcp.types import TextContent
from mistralai.client import Mistral
from pydantic import SecretStr

from mistralai.workflows._mistral_http import MISTRAL_HTTP
from mistralai.workflows.core.config.config import config
from mistralai.workflows.core.temporal.context_handler_interceptor import define_context
from mistralai.workflows.exceptions import WorkflowError
from mistralai.workflows.plugins.mistralai import ConnectorClient
from mistralai.workflows.plugins.mistralai.connectors import gateway as gateway_module

_WORKER_KEY = "worker-key"
_EXECUTOR_JWT = "header.{}.signature".format(
    base64.urlsafe_b64encode(json.dumps({"exp": 4102444800}).encode()).rstrip(b"=").decode()
)
_API_URL = "https://api.example"

gateway_clients = pytest.mark.xfail(
    not gateway_module.sdk_supports_gateway_clients(),
    strict=True,
    raises=WorkflowError,
    reason="the installed mistralai connectors gateway helpers do not send through the SDK's configured client",
)

open_methods = pytest.mark.parametrize(
    "open_client", [ConnectorClient.http_client, ConnectorClient.mcp_client], ids=["http", "mcp"]
)


def _binding(**overrides: Any) -> dict[str, Any]:
    return {"connector_name": "github", "connector_id": "conn-123", "status": "ready", **overrides}


def _mcp_result(payload: dict[str, Any]) -> dict[str, Any] | None:
    method = payload["method"]
    if method == "initialize":
        return {
            "protocolVersion": payload["params"]["protocolVersion"],
            "capabilities": {},
            "serverInfo": {"name": "connectors-gateway", "version": "test"},
        }
    if method == "tools/call":
        return {"content": [{"type": "text", "text": "done"}], "isError": False}
    if method == "tools/list":
        return {"tools": [{"name": "create_issue", "inputSchema": {"type": "object"}}]}
    return None


@dataclass
class FakeApi:
    """Mocked Mistral API: answers executor token exchanges, the HTTP gateway and the MCP gateway."""

    requests: list[httpx.Request] = field(default_factory=list)

    def gateway_requests(self) -> list[httpx.Request]:
        return [request for request in self.requests if "/connectors-gateway/" in request.url.path]

    def handle(self, request: httpx.Request, http: Any) -> httpx.Response:
        self.requests.append(request)
        if request.url.path.endswith("/executor-identity-token"):
            return http.Response(200, json={"token": _EXECUTOR_JWT})
        if not request.url.path.endswith("/mcp"):
            return http.Response(200, json={"ok": True})
        if request.method != "POST":
            return http.Response(405)
        payload = json.loads(request.content)
        result = _mcp_result(payload)
        if result is None:
            return http.Response(202)
        return http.Response(
            200,
            headers={"content-type": "application/json"},
            json={"jsonrpc": "2.0", "id": payload["id"], "result": result},
        )


@pytest.fixture
def api(monkeypatch: pytest.MonkeyPatch) -> FakeApi:
    fake = FakeApi()

    def transport(client_cls: type) -> Any:
        http = MISTRAL_HTTP if client_cls in (MISTRAL_HTTP.Client, MISTRAL_HTTP.AsyncClient) else httpx
        return http.MockTransport(lambda request: fake.handle(request, http))

    monkeypatch.setattr(config.http, "transport_factory", transport)
    monkeypatch.setattr(config.worker, "server_url", _API_URL)
    monkeypatch.setattr(config.worker, "mistral_api_headers", {})
    monkeypatch.setattr(config.common, "mistral_sa_token_path", None)
    monkeypatch.setattr(config.common, "mistral_api_key", SecretStr(_WORKER_KEY))
    return fake


@pytest.fixture
def built_clients() -> Any:
    """Record the SDK clients the gateway builds, so tests can check they are closed."""
    built: list[Mistral] = []
    build = gateway_module._build_connector_client

    def recording_build(run_as: Any) -> Mistral:
        sdk = build(run_as)
        built.append(sdk)
        return sdk

    with patch.object(gateway_module, "_build_connector_client", recording_build):
        yield built


@open_methods
def test_refused_in_workflow_code(open_client: Callable[[ConnectorClient], Any]) -> None:
    with define_context(make_context([_binding()])), patch("temporalio.workflow.in_workflow", return_value=True):
        with pytest.raises(RuntimeError, match="not in workflow code"):
            open_client(ConnectorClient("github"))


@open_methods
@pytest.mark.asyncio
async def test_unsupported_sdk_raises_non_retryable_error(
    monkeypatch: pytest.MonkeyPatch, api: FakeApi, open_client: Callable[[ConnectorClient], Any]
) -> None:
    monkeypatch.setattr(gateway_module, "sdk_supports_gateway_clients", lambda: False)
    with define_context(make_context([_binding()])):
        with pytest.raises(WorkflowError, match="send through the SDK's configured client") as exc_info:
            async with open_client(ConnectorClient("github")):
                pass

    assert exc_info.value.non_retryable
    assert api.requests == []


@open_methods
@pytest.mark.asyncio
async def test_executor_binding_is_rejected(
    monkeypatch: pytest.MonkeyPatch, api: FakeApi, open_client: Callable[[ConnectorClient], Any]
) -> None:
    monkeypatch.setattr(gateway_module, "sdk_supports_gateway_clients", lambda: True)
    with define_context(make_context([_binding(run_as="executor")])):
        with pytest.raises(WorkflowError) as exc_info:
            async with open_client(ConnectorClient("github")):
                pass

    assert exc_info.value.non_retryable
    assert api.requests == []


@gateway_clients
@pytest.mark.parametrize(
    ("run_as", "on_behalf_of", "expected_token"),
    [("deployment", True, _WORKER_KEY), ("auto", False, _WORKER_KEY), ("auto", True, _EXECUTOR_JWT)],
    ids=["deployment", "auto-non-obo", "auto-obo"],
)
@pytest.mark.asyncio
async def test_http_client_sends_run_as_identity(
    api: FakeApi, built_clients: list[Mistral], run_as: str, on_behalf_of: bool, expected_token: str
) -> None:
    context = make_context(
        [_binding(run_as=run_as, credentials_name="gh_sa")],
        execution_token="execution-token",
        on_behalf_of=on_behalf_of,
    )
    with define_context(context):
        async with ConnectorClient("github").http_client() as http:
            response = await http.get("repos/mistralai/client-python")

    assert response.json() == {"ok": True}
    (request,) = api.gateway_requests()
    assert str(request.url) == f"{_API_URL}/v1/connectors-gateway/conn-123/http/repos/mistralai/client-python"
    assert request.headers["authorization"] == f"Bearer {expected_token}"
    assert request.headers["x-credentials-name"] == "gh_sa"
    (sdk,) = built_clients
    assert sdk.sdk_configuration.async_client is not None
    assert sdk.sdk_configuration.async_client.is_closed


@gateway_clients
@pytest.mark.asyncio
async def test_mcp_client_calls_tool_through_gateway(api: FakeApi, built_clients: list[Mistral]) -> None:
    context = make_context([_binding(run_as="deployment", credentials_name="gh_sa")], on_behalf_of=False)
    with define_context(context):
        async with ConnectorClient("github").mcp_client() as mcp:
            result = await mcp.call_tool("create_issue", {"title": "bug"})

    assert isinstance(result.content[0], TextContent)
    assert result.content[0].text == "done"
    requests = api.gateway_requests()
    assert requests
    for request in requests:
        assert request.url.path == "/v1/connectors-gateway/conn-123/mcp"
        assert request.headers["authorization"] == f"Bearer {_WORKER_KEY}"
        assert request.headers["x-credentials-name"] == "gh_sa"
    (sdk,) = built_clients
    assert sdk.sdk_configuration.async_client is not None
    assert sdk.sdk_configuration.async_client.is_closed
