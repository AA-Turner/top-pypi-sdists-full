import json
import time
import uuid

import httpx
import jwt
import pytest
from pydantic import SecretStr

from mistralai.workflows.client import get_mistral_client
from mistralai.workflows.core import _http_transport
from mistralai.workflows.core.auth import ConnectorRunAs, FileTokenProvider
from mistralai.workflows.core.config.config import config
from mistralai.workflows.core.temporal.context_handler_interceptor import define_context
from mistralai.workflows.exceptions import WorkflowError
from mistralai.workflows.models.payload import WorkflowContext
from mistralai.workflows.worker_client.errors import SDKError

_INTERNAL_URL = "http://abraxas.internal"
_PUBLIC_URL = "https://api.example.com"
_WORKER_HEADERS = {"x-consumer-custom-id": "builder-owner", "x-workspace-id": "builder-workspace"}


def _jwt(signature: str) -> str:
    return jwt.encode(
        {"exp": time.time() + 120, "sub": signature},
        "test-signing-key-not-verified-but-long-enough",
        algorithm="HS256",
    )


def _context(token: str) -> WorkflowContext:
    return WorkflowContext(namespace="shared", execution_id="session", execution_token=token, on_behalf_of=True)


@pytest.fixture
def worker_config(monkeypatch):
    monkeypatch.setattr(config.common, "mistral_api_key", None)
    monkeypatch.setattr(config.common, "mistral_sa_token_path", None)
    monkeypatch.setattr(config.worker, "server_url", _INTERNAL_URL)
    monkeypatch.setattr(config.worker, "mistral_api_headers", _WORKER_HEADERS)


@pytest.mark.usefixtures("worker_config")
@pytest.mark.parametrize("use_async", [False, True], ids=["sync", "async"])
class TestExecutorCredentialsTransport:
    @pytest.mark.parametrize("explicit_headers", [False, True])
    @pytest.mark.parametrize("worker_credential", ["none", "api_key", "configured_api_key", "service_account"])
    @pytest.mark.parametrize("run_as", [None, ConnectorRunAs.AUTO], ids=["strict", "auto"])
    async def test_internal_exchange_and_public_executor_requests(
        self, monkeypatch, tmp_path, use_async, explicit_headers, worker_credential, run_as
    ):
        api_key = "worker-api-key" if worker_credential == "api_key" else None
        if worker_credential == "configured_api_key":
            monkeypatch.setattr(config.common, "mistral_api_key", SecretStr("worker-api-key"))
        elif worker_credential == "service_account":
            token_file = tmp_path / "worker-token"
            token_file.write_text(_jwt("worker-service-account"))
            monkeypatch.setattr(config.common, "mistral_sa_token_path", str(token_file))
        tokens = [str(uuid.uuid4()), str(uuid.uuid4())]
        jwts = {token: _jwt(str(index)) for index, token in enumerate(tokens)}
        exchanges = []
        requests = []
        headers = {"x-internal-auth": "signed-worker-identity"} if explicit_headers else _WORKER_HEADERS

        def handler(request: httpx.Request) -> httpx.Response:
            if request.url.host == "abraxas.internal":
                assert request.url.path == "/v1/workflows/workers/executor-identity-token"
                assert "authorization" not in request.headers
                for name, value in headers.items():
                    assert request.headers[name] == value
                if explicit_headers:
                    assert "x-consumer-custom-id" not in request.headers
                token = json.loads(request.content)["execution_token"]
                exchanges.append(token)
                return httpx.Response(200, json={"token": jwts[token]})
            assert request.url.host == "api.example.com"
            assert not any(name in request.headers for name in [*headers, *_WORKER_HEADERS])
            requests.append(request.headers["authorization"])
            return httpx.Response(200, json={"object": "list", "data": []})

        self._mock_http(monkeypatch, handler)
        client = get_mistral_client(
            server_url=_PUBLIC_URL,
            api_key=api_key,
            use_executor_credentials=run_as is None,
            run_as=run_as,
            executor_credentials_server_url=_INTERNAL_URL,
            executor_credentials_headers=headers if explicit_headers else None,
        )
        for token in [tokens[0], tokens[0], tokens[1]]:
            with define_context(_context(token)):
                if use_async:
                    await client.models.list_async()
                else:
                    client.models.list()

        assert exchanges == tokens
        assert requests == [f"Bearer {jwts[token]}" for token in [tokens[0], tokens[0], tokens[1]]]

    async def test_auto_keeps_deployment_credentials_separate_from_header_exchange(self, monkeypatch, use_async):
        executor_jwt = _jwt("executor")
        exchanges = []
        requests = []

        def handler(request: httpx.Request) -> httpx.Response:
            if request.url.host == "abraxas.internal":
                assert "authorization" not in request.headers
                for name, value in _WORKER_HEADERS.items():
                    assert request.headers[name] == value
                exchanges.append(json.loads(request.content)["execution_token"])
                return httpx.Response(200, json={"token": executor_jwt})
            assert request.url.host == "api.example.com"
            assert not any(name in request.headers for name in _WORKER_HEADERS)
            requests.append(request.headers["authorization"])
            return httpx.Response(200, json={"object": "list", "data": []})

        self._mock_http(monkeypatch, handler)
        client = get_mistral_client(
            server_url=_PUBLIC_URL,
            api_key="deployment-key",
            run_as=ConnectorRunAs.AUTO,
            executor_credentials_server_url=_INTERNAL_URL,
        )
        context = _context(str(uuid.uuid4()))
        for obo in [False, True, False, True]:
            with define_context(context.model_copy(update={"on_behalf_of": obo})):
                if use_async:
                    await client.models.list_async()
                else:
                    client.models.list()

        assert exchanges == [context.execution_token]
        assert requests == ["Bearer deployment-key", f"Bearer {executor_jwt}"] * 2

    @pytest.mark.parametrize("explicit_empty_headers", [False, True])
    async def test_bearer_exchange_preserves_rotation_and_default_url(
        self, monkeypatch, tmp_path, use_async, explicit_empty_headers
    ):
        if not explicit_empty_headers:
            monkeypatch.setattr(config.worker, "mistral_api_headers", None)
        token_file = tmp_path / "worker-token"
        worker_tokens = [_jwt("worker-1"), _jwt("worker-2")]
        exchanges = []
        jwt = _jwt("executor")

        def handler(request: httpx.Request) -> httpx.Response:
            assert request.url.host == "api.example.com"
            assert not any(name in request.headers for name in _WORKER_HEADERS)
            if request.url.path.endswith("/executor-identity-token"):
                exchanges.append(request.headers["authorization"])
                return httpx.Response(200, json={"token": jwt})
            assert request.headers["authorization"] == f"Bearer {jwt}"
            return httpx.Response(200, json={"object": "list", "data": []})

        self._mock_http(monkeypatch, handler)
        client = get_mistral_client(
            server_url=_PUBLIC_URL,
            token_provider=FileTokenProvider(token_file, refresh_margin_seconds=300),
            use_executor_credentials=True,
            executor_credentials_headers={} if explicit_empty_headers else None,
        )
        for token in worker_tokens:
            token_file.write_text(token)
            with define_context(_context(str(uuid.uuid4()))):
                if use_async:
                    await client.models.list_async()
                else:
                    client.models.list()

        assert exchanges == [f"Bearer {token}" for token in worker_tokens]

    async def test_public_redirect_does_not_forward_executor_or_internal_auth(self, monkeypatch, use_async):
        jwt = _jwt("executor")
        seen = []

        def handler(request: httpx.Request) -> httpx.Response:
            if request.url.host == "abraxas.internal":
                return httpx.Response(200, json={"token": jwt})
            assert not any(name in request.headers for name in _WORKER_HEADERS)
            seen.append((request.url.host, request.headers.get("authorization")))
            if request.url.host == "api.example.com":
                return httpx.Response(307, headers={"location": "https://other.example.com/v1/models"})
            return httpx.Response(200, json={"object": "list", "data": []})

        self._mock_http(monkeypatch, handler)
        client = get_mistral_client(
            server_url=_PUBLIC_URL, use_executor_credentials=True, executor_credentials_server_url=_INTERNAL_URL
        )
        with define_context(_context(str(uuid.uuid4()))):
            if use_async:
                await client.models.list_async()
            else:
                client.models.list()

        assert seen == [("api.example.com", f"Bearer {jwt}"), ("other.example.com", None)]

    async def test_token_exchange_does_not_follow_redirects(self, monkeypatch, use_async):
        seen = []

        def handler(request: httpx.Request) -> httpx.Response:
            seen.append(request.url.host)
            return httpx.Response(307, headers={"location": "https://other.example.com/exchange"})

        self._mock_http(monkeypatch, handler)
        client = get_mistral_client(
            server_url=_PUBLIC_URL, use_executor_credentials=True, executor_credentials_server_url=_INTERNAL_URL
        )
        with define_context(_context(str(uuid.uuid4()))), pytest.raises(SDKError):
            if use_async:
                await client.models.list_async()
            else:
                client.models.list()

        assert seen == ["abraxas.internal"]

    @staticmethod
    def _mock_http(monkeypatch, handler):
        monkeypatch.setattr(_http_transport, "sync_transport", lambda: httpx.MockTransport(handler))
        monkeypatch.setattr(_http_transport, "async_transport", lambda: httpx.MockTransport(handler))
        monkeypatch.setattr(_http_transport, "sync_mounts", lambda: {})
        monkeypatch.setattr(_http_transport, "async_mounts", lambda: {})


def test_explicit_empty_exchange_headers_disable_worker_header_fallback(monkeypatch):
    monkeypatch.setattr(config.common, "mistral_api_key", None)
    monkeypatch.setattr(config.common, "mistral_sa_token_path", None)
    monkeypatch.setattr(config.worker, "mistral_api_headers", _WORKER_HEADERS)
    with pytest.raises(WorkflowError, match="authentication headers"):
        get_mistral_client(use_executor_credentials=True, executor_credentials_headers={})
