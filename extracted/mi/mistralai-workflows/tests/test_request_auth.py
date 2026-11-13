import asyncio
import base64
import json
import time
import warnings
from typing import Any, NamedTuple

import httpx
import pytest

from mistralai.workflows._mistral_http import MISTRAL_HTTP
from mistralai.workflows.client import (
    _get_async_client,
    _get_sync_client,
    get_mistral_client,
    should_use_executor_credentials,
)
from mistralai.workflows.core.auth import RunAs, StaticTokenProvider
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


_STRICT_EXECUTOR_POLICIES = [
    pytest.param({"run_as": RunAs.EXECUTOR}, id="executor"),
    pytest.param({"use_executor_credentials": True}, id="legacy-executor"),
]
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

    @pytest.mark.parametrize("policy", _STRICT_EXECUTOR_POLICIES)
    async def test_strict_executor_uses_executor_jwt(self, make_client, server, policy):
        client = make_client(token_provider=StaticTokenProvider("deployment-key"), **policy)
        with define_context(_context("alice")):
            await _get(client)
        assert server.requests[-1].headers["Authorization"] == f"Bearer {server.tokens['alice']}"

    @pytest.mark.parametrize("rejection", _STRICT_EXECUTOR_REJECTIONS)
    @pytest.mark.parametrize("policy", _STRICT_EXECUTOR_POLICIES)
    async def test_strict_executor_never_sends_without_identity(self, make_client, server, policy, rejection):
        client = make_client(token_provider=StaticTokenProvider("deployment-key"), **policy)
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

    @pytest.mark.parametrize("mode", list(RunAs))
    def test_conflicting_legacy_option_is_rejected(self, factory, mode, server):
        with pytest.raises(ValueError, match="conflicts"):
            factory(run_as=mode, use_executor_credentials=True)

    def test_invalid_mode_is_rejected(self, factory, server):
        with pytest.raises(ValueError):
            factory(run_as="typo")


@pytest.fixture
async def make_mistral_client(server):
    clients = []

    def make(**kwargs):
        kwargs.setdefault("token_provider", StaticTokenProvider("deployment-key"))
        clients.append(get_mistral_client(server_url="https://api.example", **kwargs))
        return clients[-1]

    yield make
    for client in clients:
        await _close(client.sdk_configuration.async_client)
        client.sdk_configuration.client.close()


class TestMistralClient:
    async def test_same_sdk_instance_uses_request_context_for_sync_and_async(self, make_mistral_client, server):
        client = make_mistral_client(run_as=RunAs.AUTO)
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


class _IdentityWarningCase(NamedTuple):
    run_as: RunAs | None
    context: WorkflowContext | None
    warning: str | None


_V4_IDENTITY_WARNING_CASES = [
    pytest.param(_IdentityWarningCase(None, _context("alice"), "on_behalf_of workflow"), id="default-obo"),
    pytest.param(_IdentityWarningCase(None, None, "outside a workflow execution"), id="default-no-context"),
    pytest.param(_IdentityWarningCase(None, _context(obo=False), None), id="default-non-obo"),
    pytest.param(_IdentityWarningCase(RunAs.DEPLOYMENT, _context("alice"), None), id="explicit-deployment"),
    pytest.param(_IdentityWarningCase(RunAs.DEPLOYMENT, None, None), id="explicit-deployment-no-context"),
]


class TestV4IdentityWarnings:
    @pytest.mark.parametrize("case", _V4_IDENTITY_WARNING_CASES)
    async def test_default_identity_warns_only_where_v4_differs(self, make_mistral_client, server, case):
        client = make_mistral_client(run_as=case.run_as)
        with define_context(case.context), warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            await client.models.list_async()
            client.models.list()

        future_warnings = [w for w in caught if issubclass(w.category, FutureWarning)]
        assert len(future_warnings) == (2 if case.warning else 0)
        assert all(case.warning in str(w.message) and w.filename == __file__ for w in future_warnings)
        assert [req.headers["Authorization"] for req in server.requests] == ["Bearer deployment-key"] * 2

    @pytest.mark.parametrize(
        "context,expected",
        [pytest.param(_context("alice"), True, id="obo"), pytest.param(_context(obo=False), False, id="non-obo")],
    )
    def test_should_use_executor_credentials_is_deprecated(self, context, expected):
        with define_context(context), pytest.warns(FutureWarning, match=r"run_as=RunAs\.AUTO"):
            assert should_use_executor_credentials() is expected

    def test_legacy_executor_flag_warns(self, make_mistral_client):
        with pytest.warns(FutureWarning, match=r"run_as=RunAs\.EXECUTOR"):
            make_mistral_client(use_executor_credentials=True)
