"""get_user の user_id を URL の path に入れる前にエンコードする (SonarCloud S7044) の回帰テスト。

user_id に `/` や `..`・`?` が入っても、別の admin API のパスや query にならないこと。

実行: python -m pytest tests/auth/test_get_user_path_encoding.py -v
"""

from __future__ import annotations

from agenticstar_platform.auth.client import AgenticStarAuthClient
from agenticstar_platform.auth.config import AgenticStarAuthConfig


def _client_recording(calls: list) -> AgenticStarAuthClient:
    config = AgenticStarAuthConfig.create(
        base_url="https://auth.example.com", api_key="test-token"
    )
    client = AgenticStarAuthClient(config)

    async def _fake_request(method, endpoint, *args, **kwargs):
        calls.append((method, endpoint))
        return {"user": {"id": "u", "username": "u"}, "devices": [], "loginHistory": []}

    client._request = _fake_request  # type: ignore[method-assign]
    return client


async def test_get_user_encodes_path_separators_and_query():
    calls: list = []
    client = _client_recording(calls)

    await client.get_user("../users?x=1")

    assert calls == [("GET", "/api/v1/admin/users/..%2Fusers%3Fx%3D1")]


async def test_get_user_plain_id_unchanged():
    calls: list = []
    client = _client_recording(calls)

    await client.get_user("0f0f0f0f-0000-0000-0000-000000000001")

    assert calls == [("GET", "/api/v1/admin/users/0f0f0f0f-0000-0000-0000-000000000001")]


async def test_get_user_rejects_dot_segments():
    """`.` / `..` は quote しても残り、URL の正規化で親のパスになるので送らない。"""
    for bad in (".", ".."):
        calls: list = []
        client = _client_recording(calls)

        result = await client.get_user(bad)

        assert result.success is False
        assert result.error_code == "INVALID_PARAMETER"
        assert calls == []
