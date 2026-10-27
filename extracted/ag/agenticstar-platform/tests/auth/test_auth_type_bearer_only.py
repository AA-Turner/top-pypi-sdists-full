"""auth_type は "bearer" だけ (agenticstar-platform 3.2.0)。

旧方式の auth_type="api_key" (X-Internal-API-Key ヘッダー) は受け口が既に無く使えなかったので削除した。
渡したら設定の誤り (AuthConfigError) として止まる。Bearer (静的トークン・token_provider) は今までどおり。

実行: cd sdk && python -m pytest tests/auth/test_auth_type_bearer_only.py -v
"""

from __future__ import annotations

import dataclasses
from types import SimpleNamespace

import httpx
import pytest

from agenticstar_platform.auth import (
    AgenticStarAuthClient,
    AgenticStarAuthConfig,
    AuthConfigError,
    AuthError,
)

BASE = "https://auth.example.com"


def test_api_key_mode_is_a_configuration_error():
    with pytest.raises(AuthConfigError) as ei:
        AgenticStarAuthConfig.create(base_url=BASE, api_key="k", auth_type="api_key")
    assert "removed" in str(ei.value) and "3.2.0" in str(ei.value)
    assert isinstance(ei.value, AuthError)
    # dataclass を直接作っても、token_provider があっても同じ
    with pytest.raises(AuthConfigError):
        AgenticStarAuthConfig(base_url=BASE, api_key="k", auth_type="api_key")
    with pytest.raises(AuthConfigError):
        AgenticStarAuthConfig.create(base_url=BASE, token_provider=lambda: "t", auth_type="api_key")


@pytest.mark.parametrize("value", ["Bearer", "basic", "", None, "api-key"])
def test_other_auth_types_are_rejected_without_echoing_the_value(value):
    with pytest.raises(AuthConfigError) as ei:
        AgenticStarAuthConfig.create(base_url=BASE, api_key="k", auth_type=value)
    assert "only 'bearer'" in str(ei.value)


def test_replace_into_api_key_mode_is_rejected():
    config = AgenticStarAuthConfig.create(base_url=BASE, api_key="k")
    with pytest.raises(AuthConfigError):
        dataclasses.replace(config, auth_type="api_key")


def test_client_rejects_a_config_changed_to_api_key_after_creation():
    config = AgenticStarAuthConfig.create(base_url=BASE, api_key="k")
    config.auth_type = "api_key"
    with pytest.raises(AuthConfigError):
        AgenticStarAuthClient(config)
    # 同じ形の別の設定オブジェクトでも断る
    duck = SimpleNamespace(base_url=BASE, api_key="k", auth_type="api_key", token_provider=None, timeout=5.0)
    with pytest.raises(AuthConfigError):
        AgenticStarAuthClient(duck)  # type: ignore[arg-type]


@pytest.mark.parametrize("explicit", [False, True])
def test_static_bearer_token_still_works(explicit):
    kwargs = {"auth_type": "bearer"} if explicit else {}
    config = AgenticStarAuthConfig.create(base_url=BASE, api_key="static-token", **kwargs)
    headers = AgenticStarAuthClient(config)._get_headers()
    assert headers["Authorization"] == "Bearer static-token"
    assert "X-Internal-API-Key" not in headers


def test_token_provider_still_works():
    calls = []

    def provider():
        calls.append(1)
        return "dynamic-token"

    config = AgenticStarAuthConfig.create(base_url=BASE, token_provider=provider)
    client = AgenticStarAuthClient(config)
    assert client._get_headers()["Authorization"] == "Bearer dynamic-token"
    assert client._get_headers()["Authorization"] == "Bearer dynamic-token"
    assert len(calls) == 2, "毎回呼ぶ (期限切れのトークンを更新できる)"


def test_from_config_is_bearer(tmp_path):
    path = tmp_path / "config.toml"
    path.write_text('[auth.agenticstar]\nbase_url = "https://auth.example.com"\napi_key = "file-token"\n')
    config = AgenticStarAuthConfig.from_config(path)
    assert config.auth_type == "bearer"
    assert AgenticStarAuthClient(config)._get_headers()["Authorization"] == "Bearer file-token"


async def test_requests_carry_only_the_bearer_header():
    seen = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(dict(request.headers))
        return httpx.Response(200, json={"success": True, "user": {"id": "u1"}})

    client = AgenticStarAuthClient(AgenticStarAuthConfig.create(base_url=BASE, token_provider=lambda: "t1"))
    client._http_client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    try:
        await client._request("GET", "/api/v1/users/u1")
    finally:
        await client.close()
    [headers] = seen
    assert headers["authorization"] == "Bearer t1"
    assert "x-internal-api-key" not in headers
