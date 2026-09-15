import asyncio
import base64
import json
import time

import httpx
import pytest

from mistralai.workflows.client import _get_async_client, _get_sync_client, get_mistral_client
from mistralai.workflows.core.auth import ConnectorRunAs, StaticTokenProvider
from mistralai.workflows.core.config.config import config
from mistralai.workflows.core.temporal.context_handler_interceptor import define_context
from mistralai.workflows.exceptions import WorkflowError
from mistralai.workflows.models import WorkflowContext


def _context(token: str | None = None, *, obo: bool = True) -> WorkflowContext:
    return WorkflowContext(namespace="ns", execution_id=token or "deployment", execution_token=token, on_behalf_of=obo)


def _jwt(token: str) -> str:
    payload = base64.urlsafe_b64encode(json.dumps({"exp": time.time() + 3600, "sub": token}).encode()).rstrip(b"=")
    return f"header.{payload.decode()}.signature"


class AuthServer:
    def __init__(self):
        self.requests: list[httpx.Request] = []
        self.exchanges: list[str] = []
        self.tokens: dict[str, str] = {}
        self.reject_exchange = False

    def handle(self, request: httpx.Request) -> httpx.Response:
        self.requests.append(request)
        if request.url.path.endswith("/executor-identity-token"):
            assert request.headers["Authorization"] == "Bearer deployment-key"
            token = json.loads(request.content)["execution_token"]
            self.exchanges.append(token)
            if self.reject_exchange:
                return httpx.Response(403, json={"detail": "Forbidden"})
            self.tokens.setdefault(token, _jwt(token))
            return httpx.Response(200, json={"token": self.tokens[token]})
        if request.url.path == "/redirect":
            return httpx.Response(302, headers={"Location": "https://foreign.example/target"})
        return httpx.Response(200, json={"data": [], "object": "list"})

    async def handle_async(self, request: httpx.Request) -> httpx.Response:
        await asyncio.sleep(0)
        return self.handle(request)

    def transport(self, client_cls):
        return httpx.MockTransport(self.handle_async if client_cls is httpx.AsyncClient else self.handle)


@pytest.fixture
def server(monkeypatch):
    server = AuthServer()
    monkeypatch.setattr(config.http, "transport_factory", server.transport)
    monkeypatch.setattr(config.common, "mistral_api_key", None)
    monkeypatch.setattr(config.common, "mistral_sa_token_path", None)
    return server


async def _get(client, path="/resource"):
    url = f"https://api.example{path}"
    if isinstance(client, httpx.AsyncClient):
        return await client.get(url)
    return await asyncio.to_thread(client.get, url)


async def _close(client):
    if isinstance(client, httpx.AsyncClient):
        await client.aclose()
    else:
        client.close()


@pytest.fixture(params=[_get_sync_client, _get_async_client], ids=["sync", "async"])
async def client(request, server):
    client = request.param(
        server_url="https://api.example",
        token_provider=StaticTokenProvider("deployment-key"),
        run_as=ConnectorRunAs.AUTO,
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


@pytest.mark.parametrize("factory", [_get_sync_client, _get_async_client], ids=["sync", "async"])
class TestAuthenticationPolicies:
    @pytest.mark.parametrize("executor", [False, True])
    async def test_deployment_policy_and_strict_executor_option(self, factory, executor, server):
        client = factory(
            server_url="https://api.example",
            token_provider=StaticTokenProvider("deployment-key"),
            use_executor_credentials=executor,
            run_as=None if executor else ConnectorRunAs.DEPLOYMENT,
        )
        try:
            with define_context(_context("alice")):
                await _get(client)
            request = server.requests[-1]
            expected = server.tokens["alice"] if executor else "deployment-key"
            assert request.headers["Authorization"] == f"Bearer {expected}"
            for context in [_context(obo=False), None]:
                with define_context(context):
                    if executor:
                        with pytest.raises(WorkflowError):
                            await _get(client)
                    else:
                        await _get(client)
                        assert server.requests[-1].headers["Authorization"] == "Bearer deployment-key"
        finally:
            await _close(client)

    async def test_auto_without_credentials_defers_failure_until_obo_request(self, factory, server):
        client = factory(server_url="https://api.example", run_as=ConnectorRunAs.AUTO)
        try:
            with define_context(_context("alice")), pytest.raises(WorkflowError, match="token_provider"):
                await _get(client)
            assert not server.requests
            with define_context(_context(obo=False)):
                await _get(client)
            assert "Authorization" not in server.requests[-1].headers
        finally:
            await _close(client)

    @pytest.mark.parametrize("mode", [ConnectorRunAs.AUTO, ConnectorRunAs.DEPLOYMENT])
    def test_conflicting_legacy_option_is_rejected(self, factory, mode, server):
        with pytest.raises(ValueError, match="conflicts"):
            factory(run_as=mode, use_executor_credentials=True)

    def test_invalid_mode_is_rejected(self, factory, server):
        with pytest.raises(ValueError):
            factory(run_as="typo")


class TestMistralClient:
    async def test_same_sdk_instance_uses_request_context_for_sync_and_async(self, server):
        client = get_mistral_client(
            server_url="https://api.example",
            token_provider=StaticTokenProvider("deployment-key"),
            run_as=ConnectorRunAs.AUTO,
        )
        try:
            for context in [_context("alice"), _context(obo=False), _context("bob")]:
                with define_context(context):
                    await client.models.list_async()
                    await asyncio.to_thread(client.models.list)
                calls = [req for req in server.requests if not req.url.path.endswith("/executor-identity-token")]
                expected = server.tokens[context.execution_token] if context.on_behalf_of else "deployment-key"
                assert [req.headers["Authorization"] for req in calls[-2:]] == [f"Bearer {expected}"] * 2
        finally:
            await _close(client.sdk_configuration.async_client)
            client.sdk_configuration.client.close()
