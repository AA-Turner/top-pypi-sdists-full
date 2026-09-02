"""Tests for the async Secret resource API (no network; httpx client is stubbed)."""

import pytest

from novita_sandbox import AsyncSecret, SecretBinding
from novita_sandbox.core.exceptions import InvalidArgumentException


class _FakeResponse:
    def __init__(self, status_code, payload):
        self.status_code = status_code
        self._payload = payload
        self.content = b"{}"

    def json(self):
        return self._payload


class _FakeAsyncHttpx:
    def __init__(self, response):
        self._response = response
        self.calls = []

    async def post(self, path, json=None):
        self.calls.append(("POST", path, json))
        return self._response

    async def get(self, path):
        self.calls.append(("GET", path, None))
        return self._response

    async def put(self, path, json=None):
        self.calls.append(("PUT", path, json))
        return self._response

    async def delete(self, path):
        self.calls.append(("DELETE", path, None))
        return self._response


def _fake_with(monkeypatch, response):
    fake = _FakeAsyncHttpx(response)

    class _FakeApiClient:
        def get_async_httpx_client(self):
            return fake

    monkeypatch.setattr(
        "novita_sandbox.core.secret.secret_async.get_api_client",
        lambda config, **kw: _FakeApiClient(),
    )
    return fake


def _binding_payload(**overrides):
    payload = {
        "name": "openai-prod",
        "hosts": ["api.example.com"],
        "placeholder": "secret_placeholder_abcd",
        "description": None,
        "hasSecret": True,
        "status": "ready",
    }
    payload.update(overrides)
    return payload


@pytest.mark.asyncio
async def test_async_create_ok(monkeypatch):
    fake = _fake_with(monkeypatch, _FakeResponse(201, _binding_payload()))

    out = await AsyncSecret.create(
        name="openai-prod",
        value="sk-real",
        hosts=["api.example.com"],
        api_key="nvta_test",
        api_url="http://localhost:3000",
    )

    assert out == SecretBinding(
        name="openai-prod",
        hosts=["api.example.com"],
        placeholder="secret_placeholder_abcd",
        description=None,
        has_secret=True,
        status="ready",
    )
    assert fake.calls[0] == (
        "POST",
        "/secrets",
        {"name": "openai-prod", "value": "sk-real", "hosts": ["api.example.com"]},
    )


@pytest.mark.asyncio
async def test_async_list_returns_metadata_no_values(monkeypatch):
    fake = _fake_with(
        monkeypatch,
        _FakeResponse(
            200,
            {"secrets": [_binding_payload(updatedAt="2026-01-01T00:00:00Z")]},
        ),
    )

    secrets = await AsyncSecret.list()

    assert secrets == [
        SecretBinding(
            name="openai-prod",
            hosts=["api.example.com"],
            placeholder="secret_placeholder_abcd",
            description=None,
            has_secret=True,
            status="ready",
            updated_at="2026-01-01T00:00:00Z",
        )
    ]
    assert fake.calls[0] == ("GET", "/secrets", None)


@pytest.mark.asyncio
async def test_async_get_ok(monkeypatch):
    fake = _fake_with(monkeypatch, _FakeResponse(200, _binding_payload()))

    out = await AsyncSecret.get("openai-prod")

    assert out.name == "openai-prod"
    assert fake.calls[0] == ("GET", "/secrets/openai-prod", None)


@pytest.mark.asyncio
async def test_async_update_ok(monkeypatch):
    fake = _fake_with(monkeypatch, _FakeResponse(200, _binding_payload()))

    out = await AsyncSecret.update(
        name="openai-prod",
        value="sk-new",
        hosts=[" API.EXAMPLE.COM ", "api.example.com"],
        description="updated",
    )

    assert out.name == "openai-prod"
    assert fake.calls[0] == (
        "PUT",
        "/secrets/openai-prod",
        {"value": "sk-new", "hosts": ["api.example.com"], "description": "updated"},
    )


@pytest.mark.asyncio
async def test_async_delete_ok(monkeypatch):
    fake = _fake_with(monkeypatch, _FakeResponse(200, {"deleted": "openai-prod"}))

    out = await AsyncSecret.delete("openai-prod")

    assert out == "openai-prod"
    assert fake.calls[0] == ("DELETE", "/secrets/openai-prod", None)


@pytest.mark.asyncio
async def test_async_create_rejects_invalid_args_before_network(monkeypatch):
    fake = _fake_with(monkeypatch, _FakeResponse(201, {}))

    with pytest.raises(InvalidArgumentException):
        await AsyncSecret.create(name="openai/prod", value="sk-real", hosts=["api.example.com"])
    with pytest.raises(InvalidArgumentException):
        await AsyncSecret.create(name="openai-prod", value="", hosts=["api.example.com"])
    with pytest.raises(InvalidArgumentException):
        await AsyncSecret.create(name="openai-prod", value="sk-real", hosts=[])

    assert fake.calls == []
