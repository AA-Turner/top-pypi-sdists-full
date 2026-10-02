"""get_mcp_tokens の expires_at 契約テスト（PAT の期限なしトークン対応）。

MCP 認証プロファイル 3 本柱化で追加された個人トークン (PAT,
custom_config.authMode='api_token') は長期/無期限のため、供給 API
(chatboardlogin) が expires_at=null を明示返却する。0.5.33 までは
これを INVALID_TOKEN_DATA として provider 単位で破棄していた
（= PAT が一切使えない）。0.5.34 で null / キー欠損を「期限なし」の
正常形として受理する。null 以外の不正値は provider 単位の
INVALID_EXPIRES_AT に統一（意図的なエラーコード変更: 空文字・0 等の
falsy は従来 INVALID_TOKEN_DATA、truthy な非文字列は従来 broad except
へ漏れて取得全体が UNKNOWN_ERROR になっていた）。

実行: python -m pytest tests/auth/test_mcp_tokens_expiry.py -v
"""

from __future__ import annotations

from datetime import UTC, datetime

from agenticstar_platform.auth.client import AgenticStarAuthClient
from agenticstar_platform.auth.config import AgenticStarAuthConfig
from agenticstar_platform.auth.models import GetMCPTokensResult, MCPTokenInfo


def _client_returning(response: dict) -> AgenticStarAuthClient:
    """_request をスタブした client を返す（HTTP には出ない）。"""
    config = AgenticStarAuthConfig.create(
        base_url="https://auth.example.com", api_key="test-token"
    )
    client = AgenticStarAuthClient(config)

    async def _fake_request(*args, **kwargs):
        return response

    client._request = _fake_request  # type: ignore[method-assign]
    return client


def _token(**overrides) -> dict:
    base = {
        "access_token": "pat-secret",
        "token_type": "Bearer",
        "expires_at": None,
        "scopes": [],
    }
    base.update(overrides)
    return base


async def test_pat_null_expires_is_accepted_as_no_expiry():
    """PAT の expires_at=null（供給 API の明示 null）はトークンとして受理される。"""
    client = _client_returning({"tokens": {"github": _token()}})
    result = await client.get_mcp_tokens("user-1", ["github"])

    assert result.success
    assert result.errors is None
    token = result.tokens["github"]
    assert token.access_token == "pat-secret"
    assert token.token_type == "Bearer"
    assert token.expires_at is None


async def test_missing_expires_key_is_accepted_as_no_expiry():
    """expires_at キー自体の欠損も null と同じく「期限なし」として受理する。"""
    data = _token()
    del data["expires_at"]
    client = _client_returning({"tokens": {"github": data}})
    result = await client.get_mcp_tokens("user-1", ["github"])

    assert result.success
    assert result.tokens["github"].expires_at is None


async def test_valid_iso_expires_is_still_parsed():
    """既存挙動の維持: ISO 8601（Z 接尾辞）は datetime として解釈される。"""
    client = _client_returning(
        {"tokens": {"github": _token(expires_at="2026-08-24T12:00:00Z")}}
    )
    result = await client.get_mcp_tokens("user-1", ["github"])

    assert result.tokens["github"].expires_at == datetime(
        2026, 8, 24, 12, 0, 0, tzinfo=UTC
    )


async def test_malformed_expires_is_still_rejected():
    """既存挙動の維持: 不正な値は INVALID_EXPIRES_AT でその provider のみ破棄。"""
    client = _client_returning(
        {
            "tokens": {
                "github": _token(expires_at="not-a-date"),
                "slack": _token(),
            }
        }
    )
    result = await client.get_mcp_tokens("user-1", ["github", "slack"])

    assert result.success
    assert "github" not in result.tokens
    assert result.errors is not None
    assert result.errors["github"].code == "INVALID_EXPIRES_AT"
    # 他 provider は巻き添えにならない
    assert result.tokens["slack"].expires_at is None


async def test_empty_string_expires_is_rejected():
    """「期限なし」の表現は null のみ。空文字は不正値として fail-closed。"""
    client = _client_returning({"tokens": {"github": _token(expires_at="")}})
    result = await client.get_mcp_tokens("user-1", ["github"])

    assert "github" not in result.tokens
    assert result.errors is not None
    assert result.errors["github"].code == "INVALID_EXPIRES_AT"


async def test_non_string_expires_is_provider_scoped_error():
    """非文字列 (0/false/配列等) は provider 単位の INVALID_EXPIRES_AT に隔離される。

    isinstance ガードが無いと .replace() の AttributeError が broad except へ漏れ、
    取得全体が UNKNOWN_ERROR (success=False) になる (Codex レビュー指摘の回帰)。
    他 provider が巻き添えにならないことまで確認する。
    """
    for bad in (0, False, 123, ["2026-08-24"], {"iso": "2026-08-24"}):
        client = _client_returning(
            {"tokens": {"github": _token(expires_at=bad), "slack": _token()}}
        )
        result = await client.get_mcp_tokens("user-1", ["github", "slack"])

        assert result.success, f"expires_at={bad!r} が全体失敗に漏れた"
        assert result.error_code is None
        assert "github" not in result.tokens
        assert result.errors is not None
        assert result.errors["github"].code == "INVALID_EXPIRES_AT"
        # 他 provider は保持される
        assert result.tokens["slack"].access_token == "pat-secret"


def test_model_roundtrip_with_null_expires():
    """cli-api → worker の 2 段目検証の契約: 直列化 JSON に expires_at=null が
    含まれていても GetMCPTokensResult.model_validate が通ること
    （worker は cli-api の応答をこのモデルで再検証する）。"""
    payload = {
        "success": True,
        "tokens": {
            "github": {
                "access_token": "pat-secret",
                "token_type": "Bearer",
                "expires_at": None,
                "scopes": [],
            }
        },
        "errors": None,
    }
    result = GetMCPTokensResult.model_validate(payload)
    assert result.tokens["github"].expires_at is None

    # 再直列化しても null が保たれる（cli-api 側の出口の形）
    dumped = result.model_dump(mode="json")
    assert dumped["tokens"]["github"]["expires_at"] is None


def test_model_default_is_no_expiry():
    """MCPTokenInfo は expires_at 省略時 None（期限なし）で構築できる。"""
    token = MCPTokenInfo(access_token="t", token_type="Bearer", scopes=[])
    assert token.expires_at is None
