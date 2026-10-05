"""get_mcp_tokens の rejected_token_sha256 (agenticstar-platform 3.0.10)。

接続先に 401 で拒否されたトークンの SHA-256 を provider ごとに渡すと、供給側 (chatboardlogin) は保存中のトークンが
同じなら期限前でも取り直す。値があるときだけ要求の body に載せる (無ければ今と同じ要求)。

実行: cd sdk && python -m pytest tests/auth/test_mcp_tokens_rejected.py -v
"""

from __future__ import annotations

import hashlib


def _sha(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()



async def test_sdk_puts_digests_in_the_body_only_when_given():
    from agenticstar_platform.auth.client import AgenticStarAuthClient
    from agenticstar_platform.auth.config import AgenticStarAuthConfig

    bodies = []
    client = AgenticStarAuthClient(AgenticStarAuthConfig.create(base_url="https://auth.example.com", api_key="k"))

    async def _fake_request(method, path, json_body=None, **kw):
        bodies.append((method, path, json_body))
        return {"tokens": {}}

    client._request = _fake_request  # type: ignore[method-assign]
    await client.get_mcp_tokens("u1", ["slack_mcp"], rejected_token_sha256={"slack_mcp": _sha("a")})
    await client.get_mcp_tokens("u1", ["slack_mcp"])
    assert bodies == [
        ("POST", "/api/v1/oauth/mcp/token", {"user_id": "u1", "providers": ["slack_mcp"],
                                             "rejected_token_sha256": {"slack_mcp": _sha("a")}}),
        ("POST", "/api/v1/oauth/mcp/token", {"user_id": "u1", "providers": ["slack_mcp"]}),
    ]
