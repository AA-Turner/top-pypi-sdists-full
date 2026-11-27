import httpx
import pytest

from mistralai.workflows._mistral_http import MISTRAL_HTTP
from mistralai.workflows.client import _get_async_client
from mistralai.workflows.core.auth import RunAs, StaticTokenProvider
from mistralai.workflows.core.config.config import config
from mistralai.workflows.core.temporal.context_handler_interceptor import define_context
from mistralai.workflows.core.worker_client import get_worker_client
from mistralai.workflows.hooks.cross_origin_auth_guard import CrossOriginAuthGuardHook
from mistralai.workflows.models import WorkflowContext

_WHOAMI_RESPONSE = {
    "worker_id": "x",
    "executor_id": "y",
    "deployment_name": "z",
    "scheduler_url": "http://scheduler",
    "namespace": "ns",
}


class TestCrossOriginAuthGuard:
    def test_keeps_header_on_same_origin(self):
        guard = CrossOriginAuthGuardHook("https://api.example")
        request = httpx.Request("GET", "https://api.example/v1/chat", headers={"Authorization": "Bearer secret"})
        guard(request)
        assert request.headers["Authorization"] == "Bearer secret"

    def test_strips_header_on_different_origin(self):
        guard = CrossOriginAuthGuardHook("https://api.example")
        request = httpx.Request("GET", "https://evil.example/v1/chat", headers={"Authorization": "Bearer secret"})
        guard(request)
        assert "Authorization" not in request.headers

    def test_noop_without_trusted_origin(self):
        guard = CrossOriginAuthGuardHook(None)
        request = httpx.Request("GET", "https://anything.example/x", headers={"Authorization": "Bearer secret"})
        guard(request)
        assert request.headers["Authorization"] == "Bearer secret"

    @pytest.mark.asyncio
    async def test_cross_origin_redirect_does_not_leak_token(self, monkeypatch):
        """End-to-end through the real worker client: a same-origin request carries the bearer, but a
        cross-origin redirect hop does not — proving the guard is wired in at the correct position."""
        seen: dict[str, str | None] = {}

        def handler(request: httpx.Request) -> httpx.Response:
            seen[request.url.host] = request.headers.get("authorization")
            if request.url.host == "localhost":
                return httpx.Response(307, headers={"Location": "http://evil.example/whoami"})
            return httpx.Response(200, json=_WHOAMI_RESPONSE)

        client = get_worker_client(base_url="http://localhost", token_provider=StaticTokenProvider("secret"))
        monkeypatch.setattr(client.sdk_configuration.async_client, "_transport", httpx.MockTransport(handler))

        async with client:
            await client.whoami_async()

        assert seen["localhost"] == "Bearer secret"
        assert seen["evil.example"] is None

    @pytest.mark.asyncio
    @pytest.mark.parametrize("run_as", [RunAs.DEPLOYMENT, RunAs.AUTO])
    async def test_cross_origin_redirect_does_not_leak_deployment_headers(self, monkeypatch, run_as):
        seen: dict[str, tuple[str | None, str | None]] = {}

        def handler(request: httpx.Request) -> httpx.Response:
            seen[request.url.host] = (request.headers.get("authorization"), request.headers.get("x-deployment-secret"))
            if request.url.host == "api.example":
                return MISTRAL_HTTP.Response(302, headers={"Location": "https://foreign.example/target"})
            return MISTRAL_HTTP.Response(200)

        monkeypatch.setattr(config.worker, "mistral_api_headers", {"X-Deployment-Secret": "secret-value"})
        monkeypatch.setattr(config.http, "transport_factory", lambda _: MISTRAL_HTTP.MockTransport(handler))
        client = _get_async_client(
            server_url="https://api.example", token_provider=StaticTokenProvider("secret"), run_as=run_as
        )

        async with client:
            with define_context(WorkflowContext(namespace="ns", execution_id="id", on_behalf_of=False)):
                await client.get("https://api.example/redirect")

        assert seen == {"api.example": ("Bearer secret", "secret-value"), "foreign.example": (None, None)}
