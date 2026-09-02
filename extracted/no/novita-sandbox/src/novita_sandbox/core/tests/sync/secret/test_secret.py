"""Tests for the Secret resource API (no network; httpx client is stubbed)."""

import pytest

from novita_sandbox import Secret, SecretBinding
from novita_sandbox.core.exceptions import InvalidArgumentException


class _FakeResponse:
    def __init__(self, status_code, payload):
        self.status_code = status_code
        self._payload = payload
        self.content = b"{}"

    def json(self):
        return self._payload


class _FakeHttpx:
    def __init__(self, response):
        self._response = response
        self.calls = []

    def post(self, path, json=None):
        self.calls.append(("POST", path, json))
        return self._response

    def get(self, path):
        self.calls.append(("GET", path, None))
        return self._response

    def put(self, path, json=None):
        self.calls.append(("PUT", path, json))
        return self._response

    def delete(self, path):
        self.calls.append(("DELETE", path, None))
        return self._response


def _fake_with(monkeypatch, response):
    fake = _FakeHttpx(response)

    class _FakeApiClient:
        def get_httpx_client(self):
            return fake

    monkeypatch.setattr(
        "novita_sandbox.core.secret.secret_sync.get_api_client",
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


def test_create_allows_resource_names(monkeypatch):
    fake = _fake_with(monkeypatch, _FakeResponse(201, _binding_payload()))
    for name in ["openai-prod", "vendor.api_key", "github_token", "OPENAI_API_KEY"]:
        out = Secret.create(name=name, value="sk-real", hosts=["api.example.com"])
        assert out.name == "openai-prod"

    assert [call[2]["name"] for call in fake.calls] == [
        "openai-prod",
        "vendor.api_key",
        "github_token",
        "OPENAI_API_KEY",
    ]


def test_create_rejects_unsafe_name_before_network(monkeypatch):
    fake = _fake_with(monkeypatch, _FakeResponse(201, {}))
    for name in ["", "openai/prod", "openai prod", "openai?prod", "a" * 129]:
        with pytest.raises(InvalidArgumentException):
            Secret.create(name=name, value="sk-real", hosts=["api.example.com"])
    assert fake.calls == []


def test_create_requires_value(monkeypatch):
    fake = _fake_with(monkeypatch, _FakeResponse(201, {}))
    with pytest.raises(InvalidArgumentException):
        Secret.create(name="openai-prod", value="", hosts=["api.example.com"])
    assert fake.calls == []


def test_create_requires_hosts(monkeypatch):
    fake = _fake_with(monkeypatch, _FakeResponse(201, {}))
    with pytest.raises(InvalidArgumentException):
        Secret.create(name="openai-prod", value="sk-real", hosts=[])
    assert fake.calls == []


def test_create_normalizes_hosts(monkeypatch):
    fake = _fake_with(monkeypatch, _FakeResponse(201, _binding_payload()))

    Secret.create(
        name="openai-prod",
        value="sk-real",
        hosts=[" API.EXAMPLE.COM ", "api.example.com", "*.EXAMPLE.COM"],
    )

    assert fake.calls[0][2]["hosts"] == ["api.example.com", "*.example.com"]


def test_create_rejects_invalid_hosts_before_network(monkeypatch):
    fake = _fake_with(monkeypatch, _FakeResponse(201, {}))
    invalid_hosts = [
        "https://api.example.com",
        "api.example.com:443",
        "api.example.com/v1",
        "*foo.example.com",
        "*",
    ]

    for host in invalid_hosts:
        with pytest.raises(InvalidArgumentException):
            Secret.create(name="openai-prod", value="sk-real", hosts=[host])

    assert fake.calls == []


def test_create_ok(monkeypatch):
    fake = _fake_with(monkeypatch, _FakeResponse(201, _binding_payload()))
    out = Secret.create(
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
    method, path, body = fake.calls[0]
    assert method == "POST"
    assert path == "/secrets"
    assert body == {
        "name": "openai-prod",
        "value": "sk-real",
        "hosts": ["api.example.com"],
    }


def test_create_ok_with_description(monkeypatch):
    fake = _fake_with(
        monkeypatch,
        _FakeResponse(201, _binding_payload(description="Example API")),
    )
    out = Secret.create(
        name="openai-prod",
        value="sk-real",
        hosts=["api.example.com"],
        description="Example API",
    )
    assert out.description == "Example API"
    assert fake.calls[0][2]["description"] == "Example API"


def test_list_returns_metadata_no_values(monkeypatch):
    fake = _fake_with(
        monkeypatch,
        _FakeResponse(
            200,
            {"secrets": [_binding_payload(updatedAt="2026-01-01T00:00:00Z")]},
        ),
    )
    secrets = Secret.list()
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


def test_get_ok(monkeypatch):
    fake = _fake_with(monkeypatch, _FakeResponse(200, _binding_payload()))
    out = Secret.get("openai-prod")
    assert out.name == "openai-prod"
    assert fake.calls[0] == ("GET", "/secrets/openai-prod", None)


def test_update_ok(monkeypatch):
    fake = _fake_with(monkeypatch, _FakeResponse(200, _binding_payload()))
    out = Secret.update(
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


def test_update_requires_value(monkeypatch):
    fake = _fake_with(monkeypatch, _FakeResponse(200, {}))
    with pytest.raises(InvalidArgumentException):
        Secret.update(name="openai-prod", value="", hosts=["api.example.com"])
    assert fake.calls == []


def test_delete_ok(monkeypatch):
    fake = _fake_with(monkeypatch, _FakeResponse(200, {"deleted": "openai-prod"}))
    out = Secret.delete("openai-prod")
    assert out == "openai-prod"
    assert fake.calls[0] == ("DELETE", "/secrets/openai-prod", None)


def test_delete_empty_rejected(monkeypatch):
    fake = _fake_with(monkeypatch, _FakeResponse(200, {}))
    with pytest.raises(InvalidArgumentException):
        Secret.delete("")
    assert fake.calls == []
