"""Tests for connector manager OAuth configuration."""

from starlette.applications import Starlette
from starlette.testclient import TestClient

from airbyte_ops_webapp import serve as serve_module
from airbyte_ops_webapp import state as state_module
from airbyte_ops_webapp.auth import oauth as oauth_module
from airbyte_ops_webapp.serve import add_oauth_routes


def test_oauth_config_defaults_to_airbyte_realm_client(
    monkeypatch,
) -> None:
    monkeypatch.delenv(state_module.OAUTH_CLIENT_ID_ENV_VAR, raising=False)
    monkeypatch.delenv(state_module.OAUTH_ENABLED_ENV_VAR, raising=False)
    monkeypatch.delenv(state_module.OAUTH_ISSUER_ENV_VAR, raising=False)
    monkeypatch.delenv(state_module.OAUTH_PUBLIC_URL_ENV_VAR, raising=False)
    monkeypatch.delenv(state_module.OAUTH_REDIRECT_URI_ENV_VAR, raising=False)

    config = oauth_module.oauth_config()

    assert config["enabled"] is True
    assert config["issuer"] == "https://cloud.airbyte.com/auth/realms/airbyte"
    assert config["client_id"] == "airbyte-ops-webapp-client"
    assert config["redirect_uri"] == "http://localhost:3000/oauth/callback"
    assert (
        config["authorization_endpoint"]
        == "https://cloud.airbyte.com/auth/realms/airbyte/protocol/openid-connect/auth"
    )
    assert config["token_exchange_endpoint"] == "/oauth/token"


def test_oauth_redirect_uri_uses_public_url(
    monkeypatch,
) -> None:
    monkeypatch.delenv(state_module.OAUTH_REDIRECT_URI_ENV_VAR, raising=False)
    monkeypatch.setenv(
        state_module.OAUTH_PUBLIC_URL_ENV_VAR,
        "https://ops.internal.airbyte.ai/",
    )

    assert (
        oauth_module._oauth_redirect_uri()
        == "https://ops.internal.airbyte.ai/oauth/callback"
    )


def test_oauth_redirect_uri_override_wins(
    monkeypatch,
) -> None:
    monkeypatch.setenv(
        state_module.OAUTH_REDIRECT_URI_ENV_VAR,
        "http://localhost:3000/oauth/callback",
    )
    monkeypatch.setenv(
        state_module.OAUTH_PUBLIC_URL_ENV_VAR,
        "https://ops.internal.airbyte.ai",
    )

    assert oauth_module._oauth_redirect_uri() == "http://localhost:3000/oauth/callback"


def test_oauth_callback_html_exchanges_code_with_configured_client() -> None:
    config = {
        "enabled": True,
        "issuer": "https://cloud.airbyte.com/auth/realms/airbyte",
        "client_id": "airbyte-ops-webapp-client",
        "redirect_uri": "http://localhost:3000/oauth/callback",
        "authorization_endpoint": "https://cloud.airbyte.com/auth/realms/airbyte/protocol/openid-connect/auth",
        "token_endpoint": "https://cloud.airbyte.com/auth/realms/airbyte/protocol/openid-connect/token",
        "token_exchange_endpoint": "/oauth/token",
    }

    html = oauth_module._oauth_callback_html(config)

    assert "airbyte-ops-webapp-client" in html
    assert "http://localhost:3000/oauth/callback" in html
    assert "code_verifier" in html
    assert "token_exchange_endpoint" in html
    assert "airbyte_ops_webapp_nonce" in html
    assert "claims.nonce !== expectedNonce" in html
    assert "airbyte_ops_webapp_access_token" in html


def test_oauth_callback_csp_allows_only_self_and_configured_token_origin() -> None:
    config = {
        "enabled": True,
        "issuer": "https://cloud.airbyte.com/auth/realms/airbyte",
        "client_id": "airbyte-ops-webapp-client",
        "redirect_uri": "http://localhost:3000/oauth/callback",
        "authorization_endpoint": "https://cloud.airbyte.com/auth/realms/airbyte/protocol/openid-connect/auth",
        "token_endpoint": "https://cloud.airbyte.com/auth/realms/airbyte/protocol/openid-connect/token",
        "token_exchange_endpoint": "/oauth/token",
    }

    csp = oauth_module._oauth_callback_csp(config)

    assert "default-src 'none'" in csp
    assert "connect-src 'self'" in csp
    assert "script-src 'unsafe-inline'" in csp


def test_webapp_host_serves_oauth_routes(monkeypatch) -> None:
    monkeypatch.delenv(state_module.OAUTH_CLIENT_ID_ENV_VAR, raising=False)
    monkeypatch.delenv(state_module.OAUTH_ENABLED_ENV_VAR, raising=False)
    monkeypatch.delenv(state_module.OAUTH_ISSUER_ENV_VAR, raising=False)
    monkeypatch.delenv(state_module.OAUTH_PUBLIC_URL_ENV_VAR, raising=False)
    monkeypatch.delenv(state_module.OAUTH_REDIRECT_URI_ENV_VAR, raising=False)
    monkeypatch.setattr(
        oauth_module,
        "_exchange_oauth_token",
        lambda code, code_verifier: {
            "access_token": f"{code}-{code_verifier}",
            "id_token": "header.payload.signature",
            "expires_in": 180,
        },
    )
    app = Starlette()
    add_oauth_routes(app)

    client = TestClient(app)
    callback_response = client.get("/oauth/callback")
    token_response = client.post(
        "/oauth/token",
        json={"code": "code_value", "code_verifier": "verifier_value"},
    )

    assert callback_response.status_code == 200
    assert "Completing Airbyte sign-in" in callback_response.text
    assert token_response.status_code == 200
    assert token_response.json()["access_token"] == "code_value-verifier_value"
    assert token_response.headers["Cache-Control"] == "no-store"


def test_prefab_renderer_route_injects_oauth_js_handlers(monkeypatch) -> None:
    renderer_uri = "ui://prefab/tool/c10065b16275/renderer.html"

    async def read_resource(_mcp_url: str, uri: str) -> str | None:
        if uri == renderer_uri:
            return "<html><head></head><body>Prefab</body></html>"
        return None

    monkeypatch.setattr(serve_module, "_read_mcp_resource", read_resource)
    app = Starlette()
    serve_module.add_prefab_renderer_route(app, "http://localhost:8000/mcp")

    response = TestClient(app).get(
        "/ui-resource",
        params={"uri": renderer_uri},
    )

    assert response.status_code == 200
    assert "window.__prefab_handlers" in response.text
    assert "startOAuth" in response.text
    assert "hydrateOAuth" in response.text
    assert "logoutOAuth" in response.text
    assert "hydrateOAuth: (...args) =>" in response.text
    assert "logoutOAuth: () =>" in response.text
    assert "window.top?.crypto" in response.text
    assert "browserCrypto.subtle.digest" in response.text
    assert response.text.index("window.__prefab_handlers") < response.text.index(
        "</head>"
    )


def test_webapp_root_redirects_to_home_app() -> None:
    app = Starlette()
    serve_module.add_home_redirect_route(app)

    response = TestClient(app).get("/", follow_redirects=False)

    assert response.status_code == 307
    assert response.headers["location"] == "/launch?tool=ops_home&args=%7B%7D"


def test_local_display_url_uses_localhost() -> None:
    assert serve_module._local_display_url(3000) == "http://localhost:3000"
    assert "0.0.0.0" not in serve_module._local_display_url(3000)


def test_oauth_token_route_rejects_incomplete_payload() -> None:
    app = Starlette()
    add_oauth_routes(app)

    response = TestClient(app).post("/oauth/token", json={"code": "code_value"})

    assert response.status_code == 400
    assert response.json()["error"] == "invalid_request"
