import asyncio
import base64
import json
import time
from typing import Any, NamedTuple

import httpx
import pytest
from pydantic import SecretStr

from mistralai.workflows._mistral_http import MISTRAL_HTTP
from mistralai.workflows.client import _get_async_client, _get_sync_client, get_mistral_client
from mistralai.workflows.core import graph_summaries
from mistralai.workflows.core.auth import RunAs, StaticTokenProvider
from mistralai.workflows.core.config.config import config
from mistralai.workflows.core.temporal.context_handler_interceptor import define_context
from mistralai.workflows.core.worker_client import get_worker_client
from mistralai.workflows.exceptions import WorkflowError
from mistralai.workflows.models import WorkflowContext


def _context(token: str | None = None, *, obo: bool = True) -> WorkflowContext:
    return WorkflowContext(namespace="ns", execution_id=token or "deployment", execution_token=token, on_behalf_of=obo)


def _jwt(token: str) -> str:
    payload = base64.urlsafe_b64encode(json.dumps({"exp": time.time() + 3600, "sub": token}).encode()).rstrip(b"=")
    return f"header.{payload.decode()}.signature"


class AuthServer:
    def __init__(self):
        self.requests: list[Any] = []
        self.exchanges: list[str] = []
        self.tokens: dict[str, str] = {}
        self.reject_exchange = False

    def handle(self, request: Any, http: Any) -> Any:
        self.requests.append(request)
        if request.url.path.endswith("/executor-identity-token"):
            assert request.headers["Authorization"] == "Bearer deployment-key"
            token = json.loads(request.content)["execution_token"]
            self.exchanges.append(token)
            if self.reject_exchange:
                return http.Response(403, json={"detail": "Forbidden"})
            self.tokens.setdefault(token, _jwt(token))
            return http.Response(200, json={"token": self.tokens[token]})
        if request.url.path == "/redirect":
            return http.Response(302, headers={"Location": "https://foreign.example/target"})
        return http.Response(200, json={"data": [], "object": "list"})

    def transport(self, client_cls: type) -> Any:
        http = MISTRAL_HTTP if client_cls in (MISTRAL_HTTP.Client, MISTRAL_HTTP.AsyncClient) else httpx

        def handle(request: Any) -> Any:
            return self.handle(request, http)

        async def handle_async(request: Any) -> Any:
            await asyncio.sleep(0)
            return handle(request)

        return http.MockTransport(handle_async if client_cls is http.AsyncClient else handle)


@pytest.fixture
def server(monkeypatch):
    server = AuthServer()
    monkeypatch.setattr(config.http, "transport_factory", server.transport)
    monkeypatch.setattr(config.common, "mistral_api_key", None)
    monkeypatch.setattr(config.common, "mistral_sa_token_path", None)
    return server


async def _get(client, path="/resource"):
    url = f"https://api.example{path}"
    if isinstance(client, (httpx.AsyncClient, MISTRAL_HTTP.AsyncClient)):
        return await client.get(url)
    return await asyncio.to_thread(client.get, url)


async def _close(client):
    if isinstance(client, (httpx.AsyncClient, MISTRAL_HTTP.AsyncClient)):
        await client.aclose()
    else:
        client.close()


@pytest.fixture(params=[_get_sync_client, _get_async_client], ids=["sync", "async"])
async def client(request, server):
    client = request.param(
        server_url="https://api.example",
        token_provider=StaticTokenProvider("deployment-key"),
        run_as=RunAs.AUTO,
    )
    yield client
    await _close(client)


class TestAutoAuthentication:
    async def test_shared_client_resolves_each_execution_and_reuses_tokens(self, client, server):
        assert not server.requests
        contexts = [_context("alice"), _context(obo=False), _context("bob"), _context("alice")]
        expected = []
        for context in contexts:
            with define_context(context):
                await _get(client)
            expected.append(
                f"Bearer {server.tokens[context.execution_token]}" if context.on_behalf_of else "Bearer deployment-key"
            )
        calls = [req for req in server.requests if req.url.path == "/resource"]
        assert [req.headers["Authorization"] for req in calls] == expected
        assert server.exchanges == ["alice", "bob"]
        assert "Authorization" not in client.headers

    @pytest.mark.parametrize("previous_obo", [None, True, False], ids=["unused", "after-obo", "after-non-obo"])
    async def test_missing_context_never_sends_a_request(self, client, server, previous_obo):
        if previous_obo is not None:
            with define_context(_context("alice", obo=previous_obo)):
                await _get(client)
        request_count = len(server.requests)
        with define_context(None), pytest.raises(WorkflowError, match="AUTO requires a workflow context") as error:
            await _get(client)
        assert error.value.non_retryable
        assert len(server.requests) == request_count

    async def test_concurrent_executions_do_not_share_identity(self, client, server):
        async def send(name, obo):
            with define_context(_context(name, obo=obo)):
                await _get(client, f"/{name}")

        await asyncio.gather(send("alice", True), send("bob", True), send("deployment", False))
        calls = {req.url.path: req.headers["Authorization"] for req in server.requests}
        assert calls["/alice"] == f"Bearer {server.tokens['alice']}"
        assert calls["/bob"] == f"Bearer {server.tokens['bob']}"
        assert calls["/deployment"] == "Bearer deployment-key"

    async def test_missing_execution_token_never_falls_back(self, client, server):
        with define_context(_context()), pytest.raises(WorkflowError, match="execution_token"):
            await _get(client)
        assert not server.requests

    async def test_rejected_exchange_never_falls_back(self, client, server):
        server.reject_exchange = True
        with define_context(_context("alice")), pytest.raises(WorkflowError) as error:
            await _get(client)
        assert error.value.non_retryable
        assert all(req.url.path.endswith("/executor-identity-token") for req in server.requests)

    @pytest.mark.parametrize("obo", [True, False])
    async def test_redirect_does_not_forward_credentials(self, client, server, obo):
        with define_context(_context("alice", obo=obo)):
            await _get(client, "/redirect")
        foreign = [req for req in server.requests if req.url.host == "foreign.example"]
        assert len(foreign) == 1
        assert "Authorization" not in foreign[0].headers


class _Rejection(NamedTuple):
    context: WorkflowContext | None
    message: str


_STRICT_EXECUTOR_REJECTIONS = [
    pytest.param(_Rejection(_context("alice", obo=False), "on_behalf_of=True"), id="non-obo"),
    pytest.param(_Rejection(None, "workflow context"), id="no-context"),
    pytest.param(_Rejection(_context(), "execution_token"), id="obo-without-token"),
]


@pytest.fixture
async def make_client(factory, server):
    clients = []

    def make(**kwargs):
        clients.append(factory(server_url="https://api.example", **kwargs))
        return clients[-1]

    yield make
    for client in clients:
        await _close(client)


@pytest.mark.parametrize("factory", [_get_sync_client, _get_async_client], ids=["sync", "async"])
class TestAuthenticationPolicies:
    async def test_deployment_policy_ignores_execution_identity(self, make_client, server):
        client = make_client(token_provider=StaticTokenProvider("deployment-key"), run_as=RunAs.DEPLOYMENT)
        for context in [_context("alice"), _context(obo=False), None]:
            with define_context(context):
                await _get(client)
            assert server.requests[-1].headers["Authorization"] == "Bearer deployment-key"
        assert not server.exchanges

    @pytest.mark.parametrize("rejection", _STRICT_EXECUTOR_REJECTIONS)
    async def test_strict_executor_never_sends_without_identity(self, make_client, server, rejection):
        client = make_client(token_provider=StaticTokenProvider("deployment-key"), run_as=RunAs.EXECUTOR)
        with define_context(rejection.context), pytest.raises(WorkflowError, match=rejection.message) as error:
            await _get(client)
        assert error.value.non_retryable
        assert not server.requests

    async def test_auto_without_credentials_defers_failure_until_obo_request(self, make_client, server):
        client = make_client(run_as=RunAs.AUTO)
        with define_context(_context("alice")), pytest.raises(WorkflowError, match="token_provider"):
            await _get(client)
        assert not server.requests
        with define_context(_context(obo=False)):
            await _get(client)
        assert "Authorization" not in server.requests[-1].headers

    @pytest.mark.parametrize(
        "api_headers, token_provider, expected",
        [
            pytest.param(
                {"X-Deployment": "worker"},
                StaticTokenProvider("deployment-key"),
                {"x-deployment": "worker", "authorization": "Bearer deployment-key"},
                id="custom-header",
            ),
            pytest.param(
                {"Authorization": "Bearer header-key"},
                None,
                {"authorization": "Bearer header-key"},
                id="header-auth-no-key",
            ),
        ],
    )
    @pytest.mark.parametrize("run_as", [RunAs.DEPLOYMENT, RunAs.AUTO])
    async def test_non_obo_requests_carry_deployment_credentials(
        self, make_client, server, monkeypatch, api_headers, token_provider, expected, run_as
    ):
        monkeypatch.setattr(config.worker, "mistral_api_headers", api_headers)
        client = make_client(token_provider=token_provider, run_as=run_as)
        with define_context(_context(obo=False)):
            await _get(client)
        assert {name: server.requests[-1].headers.get(name) for name in expected} == expected

    def test_invalid_mode_is_rejected(self, factory, server):
        with pytest.raises(ValueError):
            factory(run_as="typo")

    def test_identity_must_be_chosen(self, factory, server):
        with pytest.raises(TypeError, match="run_as"):
            factory()


class TestMistralClient:
    def test_v3_positional_executor_flag_is_rejected(self, server):
        with pytest.raises(TypeError, match="positional"):
            get_mistral_client("https://api.example", "deployment-key", True)

    async def test_default_identity_follows_each_request_context_for_sync_and_async(self, server):
        client = get_mistral_client(
            server_url="https://api.example",
            token_provider=StaticTokenProvider("deployment-key"),
        )
        try:
            # mistralai 2.9.3 metadata uses httpx; client-python/pyproject.toml 3.x uses httpx2.
            assert isinstance(client.sdk_configuration.async_client, MISTRAL_HTTP.AsyncClient)
            assert isinstance(client.sdk_configuration.client, MISTRAL_HTTP.Client)
            for context in [_context("alice"), _context(obo=False), _context("bob")]:
                with define_context(context):
                    await client.models.list_async()
                    await asyncio.to_thread(client.models.list)
                calls = [req for req in server.requests if not req.url.path.endswith("/executor-identity-token")]
                expected = server.tokens[context.execution_token] if context.on_behalf_of else "deployment-key"
                assert [req.headers["Authorization"] for req in calls[-2:]] == [f"Bearer {expected}"] * 2
            with define_context(None), pytest.raises(WorkflowError, match="AUTO requires a workflow context"):
                await client.models.list_async()
        finally:
            await _close(client.sdk_configuration.async_client)
            client.sdk_configuration.client.close()


class TestOutOfWorkflowClients:
    @pytest.fixture(autouse=True)
    def deployment_config(self, server, monkeypatch):
        monkeypatch.setattr(config.common, "mistral_api_key", SecretStr("deployment-key"))
        monkeypatch.setattr(config.worker, "server_url", "https://api.example")
        monkeypatch.setattr(graph_summaries, "_cached_client", None)

    @pytest.mark.parametrize(
        "build", [get_worker_client, graph_summaries._get_client], ids=["worker-client", "graph-summaries"]
    )
    async def test_uses_deployment_identity_without_workflow_context(self, build, server):
        client = build().sdk_configuration.async_client
        try:
            with define_context(None):
                await _get(client)
        finally:
            await _close(client)
        assert server.requests[-1].headers["Authorization"] == "Bearer deployment-key"
