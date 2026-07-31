import httpx
import pytest

from mistralai.workflows.core.auth import StaticTokenProvider
from mistralai.workflows.core.worker_client import get_worker_client
from mistralai.workflows.hooks.cross_origin_auth_guard import CrossOriginAuthGuardHook

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
