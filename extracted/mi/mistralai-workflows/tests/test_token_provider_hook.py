import httpx
import pytest

from mistralai.workflows.core.auth import StaticTokenProvider, TokenWithMaxAge
from mistralai.workflows.core.worker_client import get_worker_client

_WHOAMI_RESPONSE = {
    "worker_id": "x",
    "executor_id": "y",
    "deployment_name": "z",
    "scheduler_url": "http://scheduler",
    "namespace": "ns",
}


class _SequenceTokenProvider:
    """Returns a different token on each call, to prove the hook re-reads per request."""

    def __init__(self, tokens: list[str]) -> None:
        self._tokens = iter(tokens)

    def get_token(self) -> str:
        return next(self._tokens)

    def get_token_with_max_age(self) -> TokenWithMaxAge:
        return TokenWithMaxAge(self.get_token(), 0.0)


class TestAuthHookInjection:
    @pytest.mark.asyncio
    async def test_sets_bearer_from_provider(self, monkeypatch):
        captured = {}

        async def capture_request(request: httpx.Request) -> httpx.Response:
            captured["authorization"] = request.headers.get("authorization")
            return httpx.Response(200, json=_WHOAMI_RESPONSE)

        client = get_worker_client(base_url="http://localhost", token_provider=StaticTokenProvider("static-token"))
        monkeypatch.setattr(client.sdk_configuration.async_client, "_transport", httpx.MockTransport(capture_request))

        async with client:
            await client.whoami_async()

        assert captured["authorization"] == "Bearer static-token"

    @pytest.mark.asyncio
    async def test_token_is_reread_per_request(self, monkeypatch):
        captured: list[str | None] = []

        async def capture_request(request: httpx.Request) -> httpx.Response:
            captured.append(request.headers.get("authorization"))
            return httpx.Response(200, json=_WHOAMI_RESPONSE)

        provider = _SequenceTokenProvider(["first-token", "rotated-token"])
        client = get_worker_client(base_url="http://localhost", token_provider=provider)
        monkeypatch.setattr(client.sdk_configuration.async_client, "_transport", httpx.MockTransport(capture_request))

        async with client:
            await client.whoami_async()
            await client.whoami_async()

        assert captured == ["Bearer first-token", "Bearer rotated-token"]
