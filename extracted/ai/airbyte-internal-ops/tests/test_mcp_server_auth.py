# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Unit tests for branded transport-auth env resolution in `server`.

These cover what this server owns: the `AIRBYTE_MCP_*` env-name translation to
the generic names `fastmcp_extensions.resolve_mcp_auth` consumes, the Airbyte
Cloud defaults, blank-as-unset handling, and the signing-key precedence. The
generic verifier assembly and the client-credentials middleware are tested in
their own suites.
"""

from __future__ import annotations

import pytest

from airbyte_ops_mcp.mcp import server


def test_env_or_default_uses_default_when_unset(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("SOME_VAR", raising=False)
    assert server._env_or_default("SOME_VAR", "fallback") == "fallback"


@pytest.mark.parametrize(
    "blank",
    [
        pytest.param("", id="empty"),
        pytest.param("   ", id="spaces"),
        pytest.param("\t", id="tab"),
        pytest.param("\n ", id="newline"),
    ],
)
def test_env_or_default_treats_blank_as_unset(
    blank: str,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("SOME_VAR", blank)
    assert server._env_or_default("SOME_VAR", "fallback") == "fallback"


def test_env_or_default_strips_and_returns_value(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("SOME_VAR", "  actual  ")
    assert server._env_or_default("SOME_VAR", "fallback") == "actual"


def test_jwt_env_map_defaults_to_airbyte_cloud() -> None:
    """The branded JWT claim vars map to generic names with Cloud defaults."""
    assert server._JWT_ENV_MAP == {
        "AIRBYTE_MCP_AUTH_ISSUER": ("MCP_AUTH_ISSUER", server.AIRBYTE_CLOUD_ISSUER),
        "AIRBYTE_MCP_AUTH_AUDIENCE": (
            "MCP_AUTH_AUDIENCE",
            server.AIRBYTE_CLOUD_AUDIENCE,
        ),
        "AIRBYTE_MCP_AUTH_ALGORITHM": (
            "MCP_AUTH_ALGORITHM",
            server.AIRBYTE_CLOUD_ALGORITHM,
        ),
    }


def test_resolve_signing_key_defaults_to_cloud_jwks(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv(server.JWKS_URI_ENV, raising=False)
    monkeypatch.delenv(server.JWT_PUBLIC_KEY_ENV, raising=False)
    resolved = server._resolve_signing_key()
    assert resolved["MCP_AUTH_JWKS_URI"] == server.AIRBYTE_CLOUD_JWKS_URI
    assert resolved["MCP_AUTH_JWT_PUBLIC_KEY"] == ""


def test_resolve_signing_key_blank_values_fall_back_to_cloud(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv(server.JWKS_URI_ENV, "   ")
    monkeypatch.setenv(server.JWT_PUBLIC_KEY_ENV, "  ")
    resolved = server._resolve_signing_key()
    assert resolved["MCP_AUTH_JWKS_URI"] == server.AIRBYTE_CLOUD_JWKS_URI
    assert resolved["MCP_AUTH_JWT_PUBLIC_KEY"] == ""


def test_resolve_signing_key_honors_explicit_jwks(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv(server.JWKS_URI_ENV, "https://self-hosted/jwks")
    monkeypatch.delenv(server.JWT_PUBLIC_KEY_ENV, raising=False)
    resolved = server._resolve_signing_key()
    assert resolved["MCP_AUTH_JWKS_URI"] == "https://self-hosted/jwks"


def test_resolve_signing_key_static_key_not_shadowed_by_cloud_jwks(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv(server.JWKS_URI_ENV, raising=False)
    monkeypatch.setenv(server.JWT_PUBLIC_KEY_ENV, "-----BEGIN PUBLIC KEY-----")
    resolved = server._resolve_signing_key()
    # The Cloud JWKS default must not be injected when a static key is supplied.
    assert resolved["MCP_AUTH_JWKS_URI"] == ""
    assert resolved["MCP_AUTH_JWT_PUBLIC_KEY"] == "-----BEGIN PUBLIC KEY-----"


def _clear_all_auth_env(monkeypatch: pytest.MonkeyPatch) -> None:
    for name in (
        *server._JWT_ENV_MAP,
        server.JWKS_URI_ENV,
        server.JWT_PUBLIC_KEY_ENV,
        server.OIDC_CLIENT_ID_ENV,
        server.OIDC_CLIENT_SECRET_ENV,
        server.OIDC_CONFIG_URL_ENV,
        server.MCP_SERVER_URL_ENV,
    ):
        monkeypatch.delenv(name, raising=False)


def test_create_auth_defaults_to_bearer_verification(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """With zero auth env, HTTP transport still verifies bearer tokens."""
    _clear_all_auth_env(monkeypatch)
    monkeypatch.delenv(server.OIDC_CLIENT_ID_ENV, raising=False)
    monkeypatch.delenv(server.OIDC_CLIENT_SECRET_ENV, raising=False)
    auth = server._create_auth()
    # A verifier is always produced (Airbyte Cloud JWKS default), never `None`.
    assert auth is not None
