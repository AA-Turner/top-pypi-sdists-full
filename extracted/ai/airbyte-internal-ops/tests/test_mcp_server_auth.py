# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Unit tests for branded transport-auth resolution in `server`.

These cover what this server owns: mapping its `AIRBYTE_MCP_*` env vars into the
typed `JWTAuthConfig` / `OIDCAuthConfig` objects it hands to
`fastmcp_extensions.build_mcp_auth`, the Airbyte Cloud defaults, blank-as-unset
handling, the signing-key precedence, and the durable-storage injection on the
interactive path. The generic verifier assembly and the client-credentials
middleware are tested in their own suites.
"""

from __future__ import annotations

from types import SimpleNamespace

import google.auth
import pytest
from fastmcp.server.auth import AccessToken
from fastmcp_extensions import JWTAuthConfig, OIDCAuthConfig
from google.auth.credentials import AnonymousCredentials
from key_value.aio.wrappers.encryption import FernetEncryptionWrapper

from airbyte_ops_mcp.mcp import server


@pytest.mark.parametrize(
    "value, expected",
    [
        pytest.param(None, "fallback", id="unset"),
        pytest.param("", "fallback", id="empty"),
        pytest.param("   ", "fallback", id="spaces"),
        pytest.param("\t", "fallback", id="tab"),
        pytest.param("\n ", "fallback", id="newline"),
        pytest.param("  actual  ", "actual", id="strips-and-returns"),
    ],
)
def test_env_or_default(
    value: str | None,
    expected: str,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Blank/unset values fall back to the default; real values are stripped.

    The default (`"fallback"`) is deliberately distinct from the stripped value
    (`"actual"`), so the `strips-and-returns` case fails if the env value is
    ignored and the default is returned instead.
    """
    if value is None:
        monkeypatch.delenv("SOME_VAR", raising=False)
    else:
        monkeypatch.setenv("SOME_VAR", value)
    assert server._env_or_default("SOME_VAR", "fallback") == expected


def test_jwt_claim_env_names_are_branded() -> None:
    """The headless JWT claim vars use this server's `AIRBYTE_MCP_*` namespace."""
    assert server.JWT_ISSUER_ENV == "AIRBYTE_MCP_AUTH_ISSUER"
    assert server.JWT_AUDIENCE_ENV == "AIRBYTE_MCP_AUTH_AUDIENCE"
    assert server.JWT_ALGORITHM_ENV == "AIRBYTE_MCP_AUTH_ALGORITHM"


def test_bearer_token_arg_ignores_raw_authorization_header() -> None:
    """The downstream bearer must come from the verified transport token, not the raw header.

    Behind `OAuthProxy`/`OIDCProxy` the raw `Authorization` header is the proxy's
    self-minted reference JWT, which Airbyte Cloud rejects with `401`. The
    `BEARER_TOKEN` arg must therefore expose no `http_header_key` and resolve via
    `_resolve_transport_bearer_token` (the verified `get_access_token` value).
    """
    config = server.app.x_mcp_server_config  # ty: ignore[unresolved-attribute]
    bearer_arg = next(
        arg
        for arg in config.config_args
        if arg.name == server.ServerConfigKey.BEARER_TOKEN
    )
    assert bearer_arg.http_header_key is None
    assert bearer_arg.default is server._resolve_transport_bearer_token


def test_resolve_signing_key_defaults_to_cloud_jwks(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv(server.JWKS_URI_ENV, raising=False)
    monkeypatch.delenv(server.JWT_PUBLIC_KEY_ENV, raising=False)
    jwks_uri, public_key = server._resolve_signing_key()
    assert jwks_uri == server.AIRBYTE_CLOUD_JWKS_URI
    assert public_key == ""


def test_resolve_signing_key_blank_values_fall_back_to_cloud(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv(server.JWKS_URI_ENV, "   ")
    monkeypatch.setenv(server.JWT_PUBLIC_KEY_ENV, "  ")
    jwks_uri, public_key = server._resolve_signing_key()
    assert jwks_uri == server.AIRBYTE_CLOUD_JWKS_URI
    assert public_key == ""


def test_resolve_signing_key_honors_explicit_jwks(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv(server.JWKS_URI_ENV, "https://self-hosted/jwks")
    monkeypatch.delenv(server.JWT_PUBLIC_KEY_ENV, raising=False)
    jwks_uri, _public_key = server._resolve_signing_key()
    assert jwks_uri == "https://self-hosted/jwks"


def test_resolve_signing_key_static_key_not_shadowed_by_cloud_jwks(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv(server.JWKS_URI_ENV, raising=False)
    monkeypatch.setenv(server.JWT_PUBLIC_KEY_ENV, "-----BEGIN PUBLIC KEY-----")
    jwks_uri, public_key = server._resolve_signing_key()
    # The Cloud JWKS default must not be injected when a static key is supplied.
    assert jwks_uri == ""
    assert public_key == "-----BEGIN PUBLIC KEY-----"


def _clear_all_auth_env(monkeypatch: pytest.MonkeyPatch) -> None:
    for name in (
        server.JWT_ISSUER_ENV,
        server.JWT_AUDIENCE_ENV,
        server.JWT_ALGORITHM_ENV,
        server.JWKS_URI_ENV,
        server.JWT_PUBLIC_KEY_ENV,
        server.OIDC_CLIENT_ID_ENV,
        server.OIDC_CLIENT_SECRET_ENV,
        server.OIDC_CONFIG_URL_ENV,
        server.OIDC_ENABLE_CIMD_ENV,
        server.MCP_SERVER_URL_ENV,
        "AIRBYTE_MCP_OIDC_STORAGE",
    ):
        monkeypatch.delenv(name, raising=False)


def _capture_build_mcp_auth(
    monkeypatch: pytest.MonkeyPatch,
) -> dict[str, object]:
    """Patch `build_mcp_auth` with a spy and return the dict it records into."""
    captured: dict[str, object] = {}

    def _capture(**kwargs: object) -> None:
        captured.update(kwargs)
        return None

    monkeypatch.setattr(server, "build_mcp_auth", _capture)
    return captured


def test_create_auth_defaults_to_bearer_verification(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """With zero auth env, HTTP transport still verifies bearer tokens."""
    _clear_all_auth_env(monkeypatch)
    auth = server._create_auth()
    # A verifier is always produced (Airbyte Cloud JWKS default), never `None`.
    assert auth is not None


def test_server_info_identity_uses_verified_token_claims(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        server,
        "get_access_token",
        lambda: AccessToken(
            token="secret",
            client_id="client",
            scopes=[],
            claims={"sub": "subject", "email": "user@example.com"},
        ),
    )

    assert server._server_info_identity() == server.ConnectedUser(
        sub="subject",
        email="user@example.com",
    )


def test_server_info_identity_is_empty_without_verified_token(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(server, "get_access_token", lambda: None)

    assert server._server_info_identity() is None


def test_server_info_provider_omits_missing_claims_and_handles_invalid_claims(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        server,
        "get_access_token",
        lambda: SimpleNamespace(claims={"email": "user@example.com"}),
    )

    assert server._server_info_provider() == {
        "connected_user": {"email": "user@example.com"}
    }

    monkeypatch.setattr(
        server,
        "get_access_token",
        lambda: SimpleNamespace(claims=["invalid"]),
    )

    assert server._server_info_identity() == server.ConnectedUser()


def test_create_auth_builds_cloud_jwt_defaults(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Zero auth env yields a JWT config carrying the Airbyte Cloud realm defaults."""
    _clear_all_auth_env(monkeypatch)
    captured = _capture_build_mcp_auth(monkeypatch)
    server._create_auth()

    jwt = captured["jwt"]
    assert isinstance(jwt, JWTAuthConfig)
    assert jwt.jwks_uri == server.AIRBYTE_CLOUD_JWKS_URI
    assert jwt.public_key is None
    assert jwt.issuer == server.AIRBYTE_CLOUD_ISSUER
    assert jwt.audience == server.AIRBYTE_CLOUD_AUDIENCE
    assert jwt.algorithm == server.AIRBYTE_CLOUD_ALGORITHM
    # No OIDC without client credentials.
    assert captured["oidc"] is None


def test_create_auth_overrides_jwt_claims_from_branded_env(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Branded `AIRBYTE_MCP_AUTH_*` env vars override the Cloud realm defaults."""
    _clear_all_auth_env(monkeypatch)
    monkeypatch.setenv(server.JWT_ISSUER_ENV, "https://self-hosted/realm")
    monkeypatch.setenv(server.JWT_AUDIENCE_ENV, "self-hosted-aud")
    monkeypatch.setenv(server.JWT_ALGORITHM_ENV, "ES256")
    captured = _capture_build_mcp_auth(monkeypatch)
    server._create_auth()

    jwt = captured["jwt"]
    assert isinstance(jwt, JWTAuthConfig)
    assert jwt.issuer == "https://self-hosted/realm"
    assert jwt.audience == "self-hosted-aud"
    assert jwt.algorithm == "ES256"


def test_create_auth_builds_oidc_when_credentials_present(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """OIDC client creds activate an `OIDCAuthConfig` defaulting to Airbyte Cloud."""
    _clear_all_auth_env(monkeypatch)
    monkeypatch.setenv(server.OIDC_CLIENT_ID_ENV, "cid")
    monkeypatch.setenv(server.OIDC_CLIENT_SECRET_ENV, "sec")
    captured = _capture_build_mcp_auth(monkeypatch)
    server._create_auth()

    oidc = captured["oidc"]
    assert isinstance(oidc, OIDCAuthConfig)
    assert oidc.client_id == "cid"
    assert oidc.client_secret == "sec"
    assert oidc.config_url == server.AIRBYTE_CLOUD_OIDC_CONFIG_URL
    # CIMD is opted into by default (Goose Desktop's URL `client_id` flow).
    assert oidc.enable_cimd is True
    # `openid` must be requested upstream, else Airbyte Cloud rejects the token.
    assert oidc.required_scopes == ["openid", "email", "profile"]
    # No durable store is built unless storage is explicitly opted into.
    assert oidc.client_storage is None


@pytest.mark.parametrize(
    "value,expected",
    [
        pytest.param("false", False, id="false"),
        pytest.param("0", False, id="0"),
        pytest.param("off", False, id="off"),
        pytest.param("true", True, id="true"),
        pytest.param("1", True, id="1"),
    ],
)
def test_create_auth_honors_cimd_override(
    monkeypatch: pytest.MonkeyPatch, value: str, expected: bool
) -> None:
    """An operator can force CIMD on/off with `AIRBYTE_MCP_OIDC_ENABLE_CIMD`."""
    _clear_all_auth_env(monkeypatch)
    monkeypatch.setenv(server.OIDC_CLIENT_ID_ENV, "cid")
    monkeypatch.setenv(server.OIDC_CLIENT_SECRET_ENV, "sec")
    monkeypatch.setenv(server.OIDC_ENABLE_CIMD_ENV, value)
    captured = _capture_build_mcp_auth(monkeypatch)
    server._create_auth()

    oidc = captured["oidc"]
    assert isinstance(oidc, OIDCAuthConfig)
    assert oidc.enable_cimd is expected


@pytest.mark.parametrize(
    "value",
    [
        pytest.param("flase", id="typo"),
        pytest.param("disabled", id="unsupported-word"),
        pytest.param("2", id="out-of-range-int"),
    ],
)
def test_create_auth_rejects_invalid_cimd_override(
    monkeypatch: pytest.MonkeyPatch, value: str
) -> None:
    """An unrecognized `AIRBYTE_MCP_OIDC_ENABLE_CIMD` fails fast, never silently off.

    A typo like `flase` must not be coerced to `False` (which would silently
    disable the Goose Desktop path); `_env_bool` raises so the misconfiguration
    surfaces at startup instead.
    """
    _clear_all_auth_env(monkeypatch)
    monkeypatch.setenv(server.OIDC_CLIENT_ID_ENV, "cid")
    monkeypatch.setenv(server.OIDC_CLIENT_SECRET_ENV, "sec")
    monkeypatch.setenv(server.OIDC_ENABLE_CIMD_ENV, value)
    _capture_build_mcp_auth(monkeypatch)
    with pytest.raises(ValueError, match=server.OIDC_ENABLE_CIMD_ENV):
        server._create_auth()


def test_create_auth_forwards_oidc_client_storage_when_configured(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """With OIDC creds + `firestore` storage, the store reaches `OIDCAuthConfig`."""
    _clear_all_auth_env(monkeypatch)
    # `FirestoreStore` resolves ADC on construction; point it at anonymous creds.
    monkeypatch.setattr(
        google.auth,
        "default",
        lambda *args, **kwargs: (AnonymousCredentials(), "stub-project"),
    )
    monkeypatch.setenv(server.OIDC_CLIENT_ID_ENV, "cid")
    monkeypatch.setenv(server.OIDC_CLIENT_SECRET_ENV, "sec")
    monkeypatch.setenv("AIRBYTE_MCP_OIDC_STORAGE", "firestore")
    captured = _capture_build_mcp_auth(monkeypatch)
    server._create_auth()

    oidc = captured["oidc"]
    assert isinstance(oidc, OIDCAuthConfig)
    assert isinstance(oidc.client_storage, FernetEncryptionWrapper)


def test_create_auth_omits_oidc_without_credentials(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Storage/OIDC are never built on the headless/bearer-only path."""
    _clear_all_auth_env(monkeypatch)
    monkeypatch.setenv("AIRBYTE_MCP_OIDC_STORAGE", "firestore")
    captured = _capture_build_mcp_auth(monkeypatch)
    server._create_auth()
    assert captured["oidc"] is None
